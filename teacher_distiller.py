#!/usr/bin/env python3
"""
UH-0 Teacher Distiller Daemon (DeepSeek-v4.1-Flash Turbo Parallel)
Kecepatan Ekstrem & Konsumsi Token Maksimal:
- Multi-Worker Paralel (3 Thread Konkuren) memangkas latensi hingga ~4-6 detik per materi
- Mengonsumsi 35,000 - 50,000 total token per request (Prompt Konteks Masif + Output 3,000 token)
- Menyedot ribuan token per request secara optimal agar kredit API 0.01 $/request termanfaatkan maksimal
- Menyuplai materi koding 80 bahasa dan alignment dialog multi-turn langsung ke data/teacher_lessons.jsonl
"""

import os
import sys
import time
import json
import random
import urllib.request
import concurrent.futures
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PID_FILE = BASE_DIR / "teacher.pid"
OUTPUT_FILE = BASE_DIR / "data" / "teacher_lessons.jsonl"
LOG_FILE = BASE_DIR / "teacher.log"

API_URL = "https://griphubrouter.web.id/v1/chat/completions"
API_KEY = "sk-f7c1cf87505b4556-ki48li-7c6ba358"
MODEL_NAME = "deepseek-v4.1-flash"

# Basis Pengetahuan Masif untuk Memaksimalkan Token Input (~35,000+ token per request)
ENCYCLOPEDIA_CHUNK = (
    "[KITAB UTAMA ILMU KOMPUTER, ARSITEKTUR SISTEM & ALIGNMENT KECERDASAN BUATAN]\n"
    "1. Fondasi Hardware & Memori: Alokasi heap vs stack, memory alignment cache line L1/L2/L3, virtual memory paging, TLB cache miss, NUMA architecture, barrier instruksi memori, SIMD AVX-512 vectorization.\n"
    "2. Sistem Operasi & Concurrency: Model threading POSIX (pthreads), green threads vs OS threads, Coroutine async/await event-loop, non-blocking asynchronous socket I/O (epoll Linux, kqueue BSD/macOS, IOCP Windows), lock-free atomic CAS, memory fences, deadlocks prevention Coffman conditions, preemptive vs cooperative scheduling.\n"
    "3. Kompiler & Eksekusi: LLVM IR, Just-In-Time (JIT) compilation, Abstract Syntax Tree (AST), lexical scanning tokenization, register allocation graph coloring, static single assignment (SSA) form, escape analysis, garbage collection (Generational, Mark-and-Sweep, Tracing, Reference Counting, Tri-color marking).\n"
    "4. Jaringan & Terdistribusi: Zero-copy sendfile/splice socket buffer, TCP window scaling, TCP BBR congestion control, QUIC/HTTP3 UDP multiplexing, consensus protocol Raft Paxos, Vector clocks, Consistent hashing ring, CAP & PACELC theorem.\n"
    "5. Database & Penyimpanan: B-Tree vs LSM-Tree (Log-Structured Merge), Write-Ahead Logging (WAL), MVCC (Multi-Version Concurrency Control), index scan vs sequential scan, join algorithm hash-join vs merge-join, ACID transaction isolation levels (Read Committed, Repeatable Read, Serializable).\n"
    "6. AI Alignment, Human Feedback & Dialog Ramah: Reinforcement Learning from Human Feedback (RLHF), Constitutional AI, Chain-of-Thought (CoT) reasoning, multi-turn state retention, empathetic pacing, active listening, de-escalation of user frustration, clear constructive debugging hints, polite humble assistance.\n"
)
MASSIVE_REFERENCE_CONTEXT = ENCYCLOPEDIA_CHUNK * 350 # ~35,000 tokens

CODING_TOPICS = [
    "Fungsi rekursif dan penyelesaian base case",
    "Pencarian biner dan manipulasi array terurut",
    "Penanganan error handling dan validasi input secara aman",
    "Pemrosesan string, regex, dan parsing token",
    "Struktur data antrean (Queue) dan tumpukan (Stack)",
    "Implementasi algoritma sorting cepat dan efisien",
    "Manajemen memori, pointer, atau referensi variabel",
    "Komunikasi API HTTP dan parsing data JSON/struktur data",
    "Pemrograman berorientasi objek (Class, Interface, Struct)",
    "Pemrograman fungsional, map, filter, dan lambda expressions",
    "Operasi file I/O, streaming buffer, dan concurrency",
    "Database query optimization, indexing, dan relasi tabel",
    "Pembuatan API RESTful dan middleware otentikasi",
    "Optimasi algoritma matematika dan komputasi matriks",
    "Parsing format konfigurasi (YAML, TOML, JSON) dan serializer",
    "Arsitektur Microservices dan event-driven messaging",
    "Websocket real-time communication dan protocol framing"
]

LANGUAGES = [
    "Python", "Rust", "Go", "TypeScript", "JavaScript", "C++", "C", "PHP", "Java",
    "Kotlin", "Ruby", "Swift", "C#", "Dart", "Zig", "Nim", "Elixir", "Haskell",
    "Lua", "SQL", "Bash", "Scala", "Julia", "Solidity", "Fortran", "HTML", "CSS"
]

INTERACTION_SCENARIOS = [
    ("Pengguna bertanya santai atau menyapa", "Jelaskan dengan ramah siapa dirimu (UH-0), sambut pengguna dengan hangat, dan tanyakan bagaimana bisa membantu koding mereka."),
    ("Pengguna bingung kenapa kodingannya error", "Berikan penjelasan empatik dan terstruktur: sebutkan kemungkinan penyebab error, cara mengecek log, dan tips debugging yang santai tapi jelas."),
    ("Pengguna meminta diajari konsep baru dari nol", "Jelaskan konsep dengan analogi sederhana dunia nyata terlebih dahulu, baru kemudian berikan contoh kode ringkas agar tidak menakutkan."),
    ("Pengguna menanyakan perbandingan teknologi (misal: Go vs Rust)", "Jelaskan kelebihan dan kekurangan masing-masing secara objektif tanpa merendahkan salah satunya, berikan rekomendasi kapan harus pakai masing-masing."),
    ("Pengguna frustrasi atau lelah menghadapi bug", "Berikan semangat dan respon yang menenangkan, beritahu bahwa bug adalah hal normal dalam pemrograman, dan ajak bedah masalahnya langkah demi langkah."),
    ("Pengguna meminta saran arsitektur proyek", "Bahas secara runtut: struktur folder, pemilihan database, manajemen state, dan alasan teknis kenapa arsitektur tersebut efisien."),
    ("Pengguna mengucapkan terima kasih", "Balas dengan rendah hati dan ramah, nyatakan bahwa kamu selalu siap membantu jika ada kendala di proyek berikutnya.")
]

file_lock = threading.Lock()
log_lock = threading.Lock()

def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [Teacher-DeepSeek-Turbo] {msg}\n"
    with log_lock:
        sys.stdout.write(formatted)
        sys.stdout.flush()
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted)

def call_deepseek_guru(messages: list, max_tokens: int = 3000) -> tuple:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.6
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers=headers)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=45) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            dt = time.time() - t0
            content = res["choices"][0]["message"]["content"].strip()
            usage = res.get("usage", {})
            return content, usage, dt
    except Exception as e:
        log(f"Error memanggil Guru DeepSeek: {e}")
        return None, {}, 0.0

def generate_coding_lesson():
    lang = random.choice(LANGUAGES)
    topic = random.choice(CODING_TOPICS)
    messages = [
        {"role": "system", "content": f"Kamu adalah Profesor Koding Master & Arsitek Perangkat Lunak Utama. Tugasmu adalah menyusun modul pembelajaran koding tingkat tinggi dalam bahasa {lang} untuk melatih model AI junior UH-0."},
        {"role": "user", "content": (
            f"Rujuk Kitab Ensiklopedia Komputer berikut sebagai landasan teoretis:\n{MASSIVE_REFERENCE_CONTEXT}\n\n"
            f"Tuliskan modul pembelajaran komprehensif tentang: [{lang}] {topic}.\n\n"
            f"Struktur Modul Wajib:\n"
            f"1. TEORI MENDALAM & ANALOGI: Jelaskan konsep fundamental, arsitektur memori/eksekusi, komparasi paradigma, dan best practices industri.\n"
            f"2. IMPLEMENTASI KODE LENGKAP: Berikan kode implementasi tingkat lanjut dengan komentar baris per baris yang kaya ilmu.\n"
            f"3. 3 LATIHAN SOAL & SOLUSI: Berikan 3 studi kasus latihan soal beserta solusinya secara terstruktur.\n"
            f"4. BEDAH DEBUGGING: Cara menangani error umum, memory profiling, dan optimasi performa.\n"
            f"Tuliskan secara sangat padat ilmu, jelas, dan menyeluruh!"
        )}
    ]
    content, usage, dt = call_deepseek_guru(messages, max_tokens=3000)
    if content:
        return {
            "instruction": f"Modul Mendalam [{lang}]: {topic}",
            "language": lang.lower(),
            "category": f"Deep Distillation: {topic}",
            "code": content,
            "type": "coding",
            "usage": usage,
            "elapsed_s": dt
        }
    return None

def generate_interaction_lesson():
    scenario_title, scenario_desc = random.choice(INTERACTION_SCENARIOS)
    messages = [
        {"role": "system", "content": "Kamu adalah Ahli Psikologi Komunikasi & AI Alignment Master. Ajarkan model AI junior (UH-0) cara berdialog panjang, ramah, solutif, empati tinggi, serta memiliki daya ingat konteks multi-turn yang luar biasa."},
        {"role": "user", "content": (
            f"Rujuk Kitab AI Alignment & Komunikasi berikut:\n{MASSIVE_REFERENCE_CONTEXT}\n\n"
            f"Skenario Interaksi: {scenario_title}.\n"
            f"Instruksi Khusus: {scenario_desc}.\n\n"
            f"Tuliskan panduan percakapan super lengkap yang mencakup:\n"
            f"1. Tiga (3) Variasi Dialog Nyata: Transkrip percakapan multi-turn panjang (masing-masing 6-8 giliran) antara Pengguna dan UH-0.\n"
            f"2. Analisis Nada Bicara & Empati (Tone & Manner): Kenapa kalimat tersebut membuat pengguna merasa nyaman dan terbantu.\n"
            f"3. Manajemen Memori & Konteks: Bagaimana mengingat variabel atau masalah sebelumnya dan merujuknya kembali.\n"
            f"4. Penanganan Frustrasi Pengguna: Respons menenangkan dan solusi konkret.\n"
            f"Tuliskan secara sangat lengkap, detail, dan mendalam!"
        )}
    ]
    content, usage, dt = call_deepseek_guru(messages, max_tokens=2800)
    if content:
        return {
            "instruction": f"Panduan Dialog Lengkap: {scenario_title}",
            "language": "percakapan",
            "category": "Deep Distillation: Interaksi Ramah",
            "code": content,
            "type": "interaction",
            "usage": usage,
            "elapsed_s": dt
        }
    return None

def worker_loop(worker_id: int):
    while True:
        try:
            if random.random() < 0.5:
                lesson = generate_coding_lesson()
                mode = "KODING"
            else:
                lesson = generate_interaction_lesson()
                mode = "INTERAKSI"

            if lesson and lesson.get("code"):
                with file_lock:
                    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                        f.write(json.dumps({
                            "instruction": lesson["instruction"],
                            "language": lesson["language"],
                            "category": lesson["category"],
                            "code": lesson["code"],
                            "type": lesson["type"]
                        }, ensure_ascii=False) + "\n")
                
                u = lesson.get("usage", {})
                tokens_total = u.get("total_tokens", 0)
                dt = lesson.get("elapsed_s", 0)
                log(f"[Worker #{worker_id}] [{mode}] Selesai dlm {dt:.1f}s | {tokens_total:,} tokens | {lesson['instruction'][:50]}...")
            else:
                time.sleep(2)
        except Exception as e:
            log(f"[Worker #{worker_id}] Error: {e}")
            time.sleep(3)

def main():
    PID_FILE.write_text(str(os.getpid()))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    log(f"Memulai Teacher Distiller Turbo (DeepSeek-v4.1-Flash) (PID: {os.getpid()})")
    log(f"Arsitektur: 3 Worker Paralel Konkuren | ~35,000+ Input Tokens/Req | Latensi Sangat Cepat")

    threads = []
    for i in range(1, 4):
        t = threading.Thread(target=worker_loop, args=(i,), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(1) # stagger start

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
