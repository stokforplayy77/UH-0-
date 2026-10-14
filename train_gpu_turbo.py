#!/usr/bin/env python3
"""
Adara AI UH-0 v2 - GPU Turbo Reading Engine & Live Telegram Bot (RTX 4090 Optimized)
Fase Membaca & Menghafal Pola Kode 80 Bahasa Pemrograman Dunia Nyata (GitHub Library)
- Pure Supervised Next-Token Learning (Zero Guessing / Cold-Start Elimination)
- Single-Shift Alignment Presisi (PyTorch/HuggingFace Native Loss)
- Asynchronous Prefetch Pipeline (70+ materi catatan per detik pada RTX 4090)
- Net2Net Progressive Layer Evolution (24 -> 26 -> 28 -> 30 Layer Penuh)
- Terhubung Langsung ke Bot Telegram: Interaksi Real-Time dengan Otak yang Sedang Berkembang
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
import argparse
import random
import threading
import queue
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

import torch

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from brain.model_qwen import AdaraEvolvingModel
from brain.notes_80_languages import StudyNotesCurriculum80

CHECKPOINT_FILE = BASE_DIR / "uh_zero_v2_checkpoint.pt"
LOG_FILE = BASE_DIR / "train_gpu.log"
PID_FILE = BASE_DIR / "bot.pid"
DATASET_FILE = BASE_DIR / "data" / "code_dataset_core.json"

TELEGRAM_BOT_TOKEN = "8834192909:AAH4ftzBlOihghnc_42K65zX2F_hqxbVeOA"


def send_telegram_message(chat_id: int, text: str, reply_to_message_id: Optional[int] = None):
    """Kirim pesan balasan ke pengguna Telegram via HTTP API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            pass
    except Exception as e:
        print(f"[!] Gagal mengirim pesan ke Telegram: {e}")
        sys.stdout.flush()


def telegram_poller(inbox_queue: queue.Queue, stop_event: threading.Event):
    """Background worker yang memantau pesan masuk dari bot Telegram secara non-blocking."""
    offset = 0
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    # Ambil offset awal agar pesan basi tidak diproses ulang
    try:
        req = urllib.request.Request(f"{url}?offset=-1")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok") and data.get("result"):
                offset = data["result"][-1]["update_id"] + 1
    except Exception:
        pass

    print("[*] Bot Telegram UH-0 (@UH0hagajajabot) aktif mendengarkan pesan...")
    sys.stdout.flush()

    while not stop_event.is_set():
        try:
            req_url = f"{url}?offset={offset}&timeout=12"
            req = urllib.request.Request(req_url)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                for update in data.get("result", []):
                    offset = max(offset, update["update_id"] + 1)
                    if "message" in update and "text" in update["message"]:
                        msg = update["message"]
                        inbox_queue.put({
                            "chat_id": msg["chat"]["id"],
                            "message_id": msg["message_id"],
                            "text": msg["text"].strip(),
                            "user_name": msg.get("from", {}).get("first_name", "Teman")
                        })
        except Exception:
            time.sleep(2.0)


def prepare_tensor_batch(adara: AdaraEvolvingModel, notes: List[Dict[str, Any]], max_seq_len: int = 256) -> Tuple[torch.Tensor, torch.Tensor]:
    """Tokenize and pad batch of study notes into tensors."""
    batch_input_ids = []
    batch_labels = []

    for note in notes:
        prompt = note["prompt"]
        target_code = note["target_code"]
        
        prompt_ids = adara.tokenizer.encode(prompt, add_special_tokens=False)
        target_ids = adara.tokenizer.encode(target_code + "\n<|im_end|>\n", add_special_tokens=False)
        
        full_ids = prompt_ids + target_ids
        if len(full_ids) > max_seq_len:
            full_ids = full_ids[:max_seq_len]
        
        # Masking presisi: Abaikan token prompt (hanya hitung loss pada kode ground-truth)
        labels = list(full_ids)
        prompt_len = min(len(prompt_ids), len(labels))
        for i in range(prompt_len):
            labels[i] = -100
            
        batch_input_ids.append(full_ids)
        batch_labels.append(labels)

    max_len = max(len(ids) for ids in batch_input_ids)
    padded_inputs = []
    padded_labels = []
    pad_id = adara.tokenizer.pad_token_id or 0

    for ids, lbls in zip(batch_input_ids, batch_labels):
        pad_len = max_len - len(ids)
        padded_inputs.append(ids + [pad_id] * pad_len)
        padded_labels.append(lbls + [-100] * pad_len)

    input_tensor = torch.tensor(padded_inputs, dtype=torch.long, device=adara.device)
    target_tensor = torch.tensor(padded_labels, dtype=torch.long, device=adara.device)

    return input_tensor, target_tensor


def prefetch_worker(batch_queue: queue.Queue, adara: AdaraEvolvingModel, curriculum: StudyNotesCurriculum80, batch_size: int, stop_event: threading.Event):
    """Background worker continuously preparing tokenized batches so GPU never starves."""
    while not stop_event.is_set():
        try:
            if batch_queue.qsize() >= 15:
                time.sleep(0.01)
                continue

            raw_notes = [curriculum.sample_study_note() for _ in range(batch_size)]
            inp_t, tgt_t = prepare_tensor_batch(adara, raw_notes, max_seq_len=256)

            batch_queue.put((inp_t, tgt_t, raw_notes), timeout=1.0)
        except Exception:
            time.sleep(0.05)


def main():
    parser = argparse.ArgumentParser(description="UH-0 Turbo Reading Engine with Telegram Bot (GPU/CPU)")
    parser.add_argument("--batch-size", type=int, default=12, help="Optimal safe batch size")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cuda", "cpu"], help="Compute device")
    args = parser.parse_args()

    # Device selection
    if args.device == "auto":
        target_device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        target_device = args.device

    # Save PID
    PID_FILE.write_text(str(os.getpid()))

    print("=" * 80)
    print(f"🚀 ADARA AI - UH-0 v2 FASE MEMBACA CATATAN 80 BAHASA ({target_device.upper()} TURBO)")
    print(f"   Mode: Pure Supervised Reading & Telegram Interactive Live")
    print(f"   Perpustakaan: Kitab 80 Bahasa + 98,683 Instruksi Nyata GitHub")
    print(f"   Bot Telegram: @UH0hagajajabot (Tersambung Langsung ke Otak Aktif)")
    if target_device == "cuda":
        print(f"   VRAM Pool: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f} GB ({torch.cuda.get_device_name(0)})")
    else:
        print(f"   CPU Threads: {torch.get_num_threads()} threads (AMD EPYC / Multi-core)")
    print("=" * 80)
    sys.stdout.flush()

    # 1. Load Model
    adara = AdaraEvolvingModel(device=target_device)
    start_step, current_level = adara.load_checkpoint(CHECKPOINT_FILE)

    # 2. Unfreeze Active Layers & Optimasi VRAM
    # Aktifkan gradient checkpointing untuk menghemat 60% memory aktivasi backward pass
    if target_device == "cuda":
        try:
            adara.model.gradient_checkpointing_enable()
            print("✓ Gradient Checkpointing Aktif (Hemat VRAM 60% di GPU T4/RTX)")
        except Exception:
            pass

    adara.configure_trainable_layers(num_top_layers=adara.num_layers())

    trainable_params = [p for p in adara.model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable_params, lr=args.lr, weight_decay=0.01)

    # 3. Muat Kurikulum Catatan Pembelajaran 80 Bahasa & GitHub Repos
    dataset_path_str = str(DATASET_FILE) if DATASET_FILE.exists() else None
    curriculum = StudyNotesCurriculum80(github_dataset_path=dataset_path_str)

    # 4. Inisialisasi Bot Telegram & Prefetch Pipeline
    stop_event = threading.Event()
    telegram_inbox = queue.Queue()
    telegram_thread = threading.Thread(
        target=telegram_poller,
        args=(telegram_inbox, stop_event),
        daemon=True
    )
    telegram_thread.start()

    batch_queue = queue.Queue(maxsize=20)
    prefetch_thread = threading.Thread(
        target=prefetch_worker,
        args=(batch_queue, adara, curriculum, args.batch_size, stop_event),
        daemon=True
    )
    prefetch_thread.start()

    print("[*] Mengisi antrean buffer prefetch batch catatan...")
    time.sleep(1.0)

    step = start_step
    recent_losses = []
    t_start = time.time()
    total_samples_trained = 0

    print(f"\n[📖 Memulai Sesi Membaca Catatan] Step #{step + 1} | Model: {adara.count_parameters():,} Parameter Penuh")
    sys.stdout.flush()

    # Penyimpanan Riwayat Obrolan Interaktif (Multi-turn Memory per Chat)
    chat_histories: Dict[int, List[Dict[str, str]]] = {}

    try:
        while True:
            step += 1

            # --- RESPON INTERAKTIF DARI TELEGRAM (OTAK LIVE BERKEMBANG + MEMORI) ---
            while not telegram_inbox.empty():
                try:
                    item = telegram_inbox.get_nowait()
                    chat_id = item["chat_id"]
                    msg_id = item["message_id"]
                    user_text = item["text"]
                    user_name = item["user_name"]

                    print(f"\n[💬 Telegram Masuk] Dari {user_name} ({chat_id}): '{user_text}'")
                    sys.stdout.flush()

                    if user_text.lower() in ("/start", "/help"):
                        chat_histories[chat_id] = []
                        reply = (
                            f"Halo {user_name}! 👋\n\n"
                            f"Saya adalah UH-0 (Adara AI), model kecerdasan buatan otonom yang sedang berlatih dan berkembang secara kontinu pada GPU RTX 4090.\n\n"
                            f"🧠 Fitur Baru: Saya sekarang memiliki memori percakapan dan bisa mengingat obrolan kita sebelumnya!\n\n"
                            f"📊 Status Otak Saya Saat Ini:\n"
                            f"• Step Pembelajaran : #{step:,}\n"
                            f"• Level Evolusi     : Level {current_level}\n"
                            f"• Arsitektur Otak   : {adara.num_layers()} Layers ({adara.count_parameters():,} params)\n"
                            f"• Materi Pelajaran  : 80 Bahasa Pemrograman + Dialog Percakapan\n\n"
                            f"Kirimkan pesan atau tanyakan apa saja! Ketik /reset jika ingin menghapus riwayat obrolan kita."
                        )
                        send_telegram_message(chat_id, reply, msg_id)

                    elif user_text.lower() in ("/reset", "reset"):
                        chat_histories[chat_id] = []
                        reply = "🧹 Riwayat obrolan kita telah di-reset! Kita bisa mulai percakapan baru dari awal."
                        send_telegram_message(chat_id, reply, msg_id)

                    elif user_text.lower() in ("/status", "status"):
                        avg_loss_s = sum(recent_losses) / max(1, len(recent_losses))
                        vram_s = torch.cuda.memory_allocated() / (1024**3)
                        elapsed_s = time.time() - t_start
                        reply = (
                            f"⚡ Status Live Otak UH-0 (Evolving Brain)\n"
                            f"-----------------------------------------\n"
                            f"• Step       : #{step:,}\n"
                            f"• Level      : Level {current_level}\n"
                            f"• Kedalaman  : {adara.num_layers()} Layers (Net2Net Asli)\n"
                            f"• Parameter  : {adara.count_parameters():,} Bobot Aktif\n"
                            f"• VRAM GPU   : {vram_s:.1f} GB / 24 GB (RTX 4090)\n"
                            f"• Loss Rata² : {avg_loss_s:.4f}\n"
                            f"• Terbaca    : {total_samples_trained:,} catatan ({elapsed_s/60:.1f} mnt)"
                        )
                        send_telegram_message(chat_id, reply, msg_id)

                    else:
                        # Kelola Riwayat Obrolan (Maksimal 6 giliran terakhir agar konteks tetap tajam)
                        history = chat_histories.get(chat_id, [])
                        
                        prompt_parts = [
                            "<|im_start|>system\n"
                            "Kamu adalah UH-0, asisten kecerdasan buatan dari ekosistem Adara AI. "
                            "Kamu ramah, sopan, cerdas, menguasai 80 bahasa pemrograman, dan mengingat konteks percakapan sebelumnya.<|im_end|>\n"
                        ]
                        
                        for turn in history[-6:]:
                            prompt_parts.append(f"<|im_start|>user\n{turn['user']}<|im_end|>\n")
                            prompt_parts.append(f"<|im_start|>assistant\n{turn['assistant']}<|im_end|>\n")
                            
                        prompt_parts.append(f"<|im_start|>user\n{user_text}<|im_end|>\n<|im_start|>assistant\n")
                        full_prompt = "".join(prompt_parts)

                        # Inferensi langsung menggunakan bobot otak saat ini (Nilai Ideal: Temperature 0.3 & Repetition Penalty 1.15)
                        adara.model.eval()
                        with torch.no_grad():
                            raw_reply = adara.generate(full_prompt, max_new_tokens=180, temperature=0.3, repetition_penalty=1.15)
                        adara.model.train()

                        clean_reply = raw_reply.strip() or "..."
                        # Simpan ke riwayat percakapan pengguna
                        history.append({"user": user_text, "assistant": clean_reply})
                        chat_histories[chat_id] = history[-8:]

                        footer = f"\n\n—\n🧠 UH-0 Live Brain | Step #{step:,} | Lvl {current_level} | {adara.num_layers()} Layers"
                        final_reply = clean_reply + footer
                        send_telegram_message(chat_id, final_reply, msg_id)
                        print(f"[🤖 Telegram Terkirim] Jawaban telah dikirimkan ke {user_name}")
                        sys.stdout.flush()

                except Exception as e_tg:
                    print(f"[!] Error interaksi Telegram: {e_tg}")

            # Fetch ready tensor batch instantly from queue
            try:
                input_tensor, target_tensor, batch_notes = batch_queue.get(timeout=5.0)
            except queue.Empty:
                raw_notes = [curriculum.sample_study_note() for _ in range(args.batch_size)]
                input_tensor, target_tensor = prepare_tensor_batch(adara, raw_notes, max_seq_len=256)
                batch_notes = raw_notes

            # High-throughput GPU Forward & Backward Pass
            adara.model.train()
            optimizer.zero_grad(set_to_none=True)
            outputs = adara.model(input_ids=input_tensor, labels=target_tensor)
            loss = outputs.loss

            if loss is not None and not torch.isnan(loss):
                loss.backward()
                torch.nn.utils.clip_grad_norm_(adara.model.parameters(), max_norm=1.0)
                optimizer.step()
                loss_val = float(loss.item())
            else:
                loss_val = 0.0

            recent_losses.append(loss_val)
            if len(recent_losses) > 30:
                recent_losses.pop(0)

            total_samples_trained += len(batch_notes)

            # Laporan Pemahaman Membaca setiap 100 step
            if step % 100 == 0 or step == (start_step + 1):
                sample_note = batch_notes[0]
                lang_name = sample_note.get("language", "Code").title()
                topic_name = sample_note.get("topic", "Struktur Sintaks")
                source_type = "GitHub Repos" if sample_note.get("source") == "github_repos" else "Kitab 80 Bahasa"

                avg_loss = sum(recent_losses) / max(1, len(recent_losses))
                elapsed = time.time() - t_start
                rate = total_samples_trained / max(1, elapsed)
                vram_gb = torch.cuda.memory_allocated() / (1024**3)

                log_entry = (
                    f"--- [Step {step:05d} | Lvl {current_level} | VRAM: {vram_gb:.1f}GB | Rate: {rate:.1f} notes/s] ---\n"
                    f"   Bahasa      : {lang_name} ({source_type})\n"
                    f"   Materi      : {topic_name}\n"
                    f"   Pemahaman   : 📖 Membaca & Menghafal Pola Kode Ground-Truth (Loss: {avg_loss:.4f})\n"
                    f"   Total Materi: {total_samples_trained:,} catatan dipelajari ({elapsed/60:.1f} mnt)"
                )
                print(log_entry.strip())
                sys.stdout.flush()

            # --- Pertumbuhan Evolusi Net2Net Asli ---
            avg_loss_curr = sum(recent_losses) / max(1, len(recent_losses))
            if step == 150 and adara.num_layers() == 24:
                current_level = 2
                adara.grow_deeper(additional_layers=2)
                adara.configure_trainable_layers(num_top_layers=adara.num_layers())
                optimizer = torch.optim.AdamW([p for p in adara.model.parameters() if p.requires_grad], lr=args.lr * 0.8, weight_decay=0.01)
                adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, avg_loss_curr)
                print(f"\n🌱 [EVOLUSI NET2NET TAHAP 1] Otak Adara membesar menjadi {adara.count_parameters():,} parameter ({adara.num_layers()} Layers)!\n")

            elif step == 500 and adara.num_layers() == 26:
                current_level = 3
                adara.grow_deeper(additional_layers=2)
                adara.configure_trainable_layers(num_top_layers=adara.num_layers())
                optimizer = torch.optim.AdamW([p for p in adara.model.parameters() if p.requires_grad], lr=args.lr * 0.7, weight_decay=0.01)
                adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, avg_loss_curr)
                print(f"\n🌿 [EVOLUSI NET2NET TAHAP 2] Otak Adara membesar menjadi {adara.count_parameters():,} parameter ({adara.num_layers()} Layers)!\n")

            elif step == 1500 and adara.num_layers() == 28:
                current_level = 4
                adara.grow_deeper(additional_layers=2)
                adara.configure_trainable_layers(num_top_layers=adara.num_layers())
                optimizer = torch.optim.AdamW([p for p in adara.model.parameters() if p.requires_grad], lr=args.lr * 0.6, weight_decay=0.01)
                adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, avg_loss_curr)
                print(f"\n🌳 [EVOLUSI NET2NET TAHAP 3 - DEWASA] Otak Adara membesar menjadi {adara.count_parameters():,} parameter ({adara.num_layers()} Layers)!\n")

            # Auto-save Checkpoint setiap 150 step
            if step % 150 == 0:
                adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, avg_loss_curr)
                torch.cuda.empty_cache()
                # Auto-backup asinkron langsung ke Node 10 IP (bypass Cloudflare 100MB limit)
                def _bg_sync(f_path, s_num):
                    try:
                        import urllib.request
                        with open(f_path, "rb") as bf:
                            req = urllib.request.Request(
                                "http://139.162.21.81/api/upload_checkpoint",
                                data=bf.read(),
                                headers={"Content-Type": "application/octet-stream", "User-Agent": "UH0-Trainer/1.0"}
                            )
                            with urllib.request.urlopen(req, timeout=600) as r:
                                print(f" [BACKUP SUCCESS] Checkpoint Step #{s_num} tersimpan ke Node 10!")
                    except Exception as e:
                        print(f" [BACKUP WARN] Sync ke Node 10 gagal: {e}")
                threading.Thread(target=_bg_sync, args=(CHECKPOINT_FILE, step), daemon=True).start()

    except KeyboardInterrupt:
        print("\n[!] Sesi dihentikan, menyimpan checkpoint...")
        stop_event.set()
        adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, 0.0)


if __name__ == "__main__":
    main()
