#!/usr/bin/env python3
"""
Autonomous AI Code Curator Daemon
Powered by Qwen2.5-Coder-7B-Instruct (Node 6 @ port 80).
Timeout extended to 5 minutes (300s) to allow thorough generation without cutoff.
"""

import os
import sys
import ast
import json
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path("/root/uh-zero")
INPUT_DATASET = BASE_DIR / "data" / "github_verified_dataset.jsonl"
CURATED_DATASET = BASE_DIR / "data" / "github_curated_verified.jsonl"
PROGRESS_FILE = BASE_DIR / "data" / "curator_progress.json"
LOG_FILE = BASE_DIR / "data" / "curator.log"
PID_FILE = BASE_DIR / "data" / "curator.pid"

LLM_ENDPOINT = "http://94.237.69.121/v1/chat/completions"
TIMEOUT_SECONDS = 300  # 5 minutes full generation window

def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def is_valid_syntax(code_str: str, lang: str) -> bool:
    if lang == "Python":
        try:
            ast.parse(code_str)
            return True
        except Exception:
            return False
    # Bracket matching guard
    brackets = {'(': ')', '{': '}', '[': ']'}
    stack = []
    for char in code_str:
        if char in brackets.keys():
            stack.append(char)
        elif char in brackets.values():
            if not stack or brackets[stack.pop()] != char:
                return False
    return len(stack) == 0

def call_qwen_curator(instruction: str, code_raw: str, lang: str) -> str:
    system_prompt = (
        f"Anda adalah Senior Principal Engineer dan AI Dataset Curator ahli untuk bahasa {lang}.\n"
        "Tugas Anda: Format ulang, rapikan, dan buat kode berikut menjadi mahakarya clean-code kelas dunia.\n"
        "WAJIB:\n"
        "1. Tambahkan type hinting lengkap, docstring penjelasan fungsi, dan komentar alur logika.\n"
        "2. Tuliskan implementasi LENGKAP tanpa terpotong di dalam markdown block ```" + lang.lower() + " ... ```.\n"
        "3. JANGAN tambahkan teks pengantar atau penutup apa pun."
    )
    
    # Send clean slice under 1500 chars to guarantee model responds well within 3-4 mins on CPU
    user_prompt = f"Instruksi: {instruction}\n\nKode Asli:\n{code_raw[:1800]}"
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.15,
        "max_tokens": 1200
    }
    
    req = urllib.request.Request(
        LLM_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log(f"⚠️ Error memanggil Qwen Coder: {e}")
        return ""

def main():
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
        
    log("🚀 Memulai AI Code Curator Daemon (Timeout: 5 Menit / 300s)...")
    
    curated_sources = set()
    if PROGRESS_FILE.exists():
        try:
            curated_sources = set(json.loads(PROGRESS_FILE.read_text(encoding="utf-8")).get("curated_sources", []))
        except Exception:
            pass
            
    if not INPUT_DATASET.exists():
        log(f"❌ Input dataset {INPUT_DATASET} tidak ditemukan.")
        return
        
    count = 0
    with open(INPUT_DATASET, "r", encoding="utf-8") as in_f, \
         open(CURATED_DATASET, "a", encoding="utf-8") as out_f:
         
        for line in in_f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except Exception:
                continue
                
            src = item.get("source", "")
            if src in curated_sources:
                continue
                
            lang = item.get("language", "Python")
            raw_code = item.get("output", "")
            clean_raw = raw_code.replace(f"```{lang.lower()}", "").replace("```", "").strip()
            
            # Filter ideal size (under 1800 chars for quality refactoring)
            if len(clean_raw) < 80 or len(clean_raw) > 1800:
                continue
                
            instruction = item.get("instruction", f"Implementasi {lang}")
            log(f"⚡ [Proses Dimulai] Mengkurasi ({lang}) {src} (Tunggu inferensi ~1-3 mnt)...")
            start_t = time.time()
            
            curated_output = call_qwen_curator(instruction, clean_raw, lang)
            dur = time.time() - start_t
            
            if not curated_output or len(curated_output) < 80:
                log(f"[-] Ditolak: Output kosong/gagal (Durasi: {dur:.1f}s).")
                continue
                
            code_only = curated_output.replace(f"```{lang.lower()}", "").replace("```", "").strip()
            if not is_valid_syntax(code_only, lang):
                log(f"[-] Ditolak: Gagal sintaks/terpotong (Durasi: {dur:.1f}s).")
                continue
                
            curated_item = {
                "source": src,
                "language": lang,
                "instruction": instruction,
                "input": "",
                "output": curated_output,
                "verified": True,
                "curated_by": "Qwen2.5-Coder-7B-Instruct",
                "curated_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            out_f.write(json.dumps(curated_item, ensure_ascii=False) + "\n")
            out_f.flush()
            curated_sources.add(src)
            count += 1
            
            log(f"✨ BERHASIL DIKURASI! ({src}) dalam {dur:.1f} detik. Total tersimpan: {count}")
            PROGRESS_FILE.write_text(json.dumps({"curated_sources": list(curated_sources)}), encoding="utf-8")
            
            time.sleep(2)
            
    log(f"🎉 Sesi kurasi selesai! Total item baru: {count}")

if __name__ == "__main__":
    main()
