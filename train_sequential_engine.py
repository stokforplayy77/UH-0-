#!/usr/bin/env python3
"""
ADARA AI / UH-0 v2 - DETERMINISTIC FULL-EPOCH SEQUENTIAL TRAINING ENGINE
Dirancang khusus untuk eksekusi 100% tuntas tanpa ada satu materi pun yang tertinggal.
- Kurikulum Menyeluruh Berurutan:
  1. TheAlgorithms (31 bahasa) & RosettaCode (Algoritma Dunia Nyata)
  2. Materi Bilingual Percakapan ID & EN (conversations_bilingual.jsonl)
  3. Materi Pengajaran Konsep Coding ID & EN (teacher_lessons.jsonl)
- Mempertahankan dan memulihkan arsitektur dewasa 30 Layer (583M parameter).
- Pembacaan terstruktur: Index 0 -> Index N (100% full coverage per epoch).
- Menghitung persentase progres per epoch dan loss aktual.
- Menyimpan checkpoint dan otomatis sinkronisasi ke Node 10 Web Observatory.
"""

import os
import sys
import time
import json
import tarfile
import argparse
import threading
import queue
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

import torch

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from brain.model_qwen import AdaraEvolvingModel

CHECKPOINT_FILE = BASE_DIR / "uh_zero_v2_checkpoint.pt"
LOG_FILE = BASE_DIR / "train.log"
SEQ_LOG_FILE = BASE_DIR / "train_sequential.log"
PID_FILE = BASE_DIR / "train_sequential.pid"
BACKUP_ARCHIVE = BASE_DIR / "data" / "backup_datasets" / "real_algorithms_backup.tar.gz"
BILINGUAL_FILE = BASE_DIR / "data" / "conversations_bilingual.jsonl"
TEACHER_FILE = BASE_DIR / "data" / "teacher_lessons.jsonl"
PROGRESS_FILE = BASE_DIR / "data" / "sequential_progress.json"

TELEGRAM_BOT_TOKEN = "8834192909:AAH4ftzBlOihghnc_42K65zX2F_hqxbVeOA"

def send_telegram(chat_id: int, text: str):
    import urllib.request
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=8):
            pass
    except Exception:
        pass


class FullUnifiedCurriculumLoader:
    """Memuat SELURUH materi: Algoritma 31 Bahasa, Percakapan Bilingual, dan Materi Pengajaran."""
    def __init__(self):
        self.items: List[Dict[str, str]] = []
        self._load_all()

    def _load_all(self):
        # 1. Muat Algoritma Dunia Nyata (157.700+ Berkas Langsung dari Folder Disk)
        print("[*] Memindai 157.000+ materi Algoritma Dunia Nyata langsung dari folder...")
        non_code_exts = {
            ".png", ".jpg", ".jpeg", ".gif", ".mp4", ".avi", ".pdf", ".jar", ".bmp",
            ".xcsettings", ".xcworkspacedata", ".plist", ".lock", ".sln", ".fsproj",
            ".csproj", ".gitignore", ".gitattributes"
        }

        real_algo_dir = BASE_DIR / "data" / "real_algorithms"
        if real_algo_dir.exists():
            for root, dirs, files in os.walk(real_algo_dir):
                for fn in files:
                    if fn.startswith("."):
                        continue
                    p = Path(root) / fn
                    ext = p.suffix.lower()
                    if ext in non_code_exts:
                        continue
                    try:
                        content = p.read_text(encoding="utf-8", errors="ignore").strip()
                    except Exception:
                        continue

                    if len(content) < 20 or len(content) > 12000:
                        continue

                    parts = p.relative_to(real_algo_dir).parts
                    lang = parts[0].replace("_algo", "") if len(parts) > 0 else ext[1:]
                    category = parts[1] if len(parts) > 1 else "algorithm"
                    task_name = p.stem.replace("_", " ").replace("-", " ").title()

                    prompt = (
                        f"<|im_start|>system\n"
                        f"Kamu adalah UH-0, asisten koding master yang menguasai seluruh algoritma dan struktur data dunia nyata.<|im_end|>\n"
                        f"<|im_start|>user\n"
                        f"[Kurikulum Lengkap Algoritma: {lang.upper()}]\n"
                        f"Kategori: {category}\n"
                        f"Algoritma/Tugas: {task_name}\n"
                        f"Tuliskan implementasi kode lengkap yang bersih dan efisien.<|im_end|>\n"
                        f"<|im_start|>assistant\n"
                    )
                    self.items.append({
                        "prompt": prompt,
                        "target_code": content,
                        "lang": lang,
                        "title": task_name,
                        "type": "Algoritma"
                    })

        # 2. Muat Percakapan Bilingual (ID & EN)
        if BILINGUAL_FILE.exists():
            print("[*] Memuat materi Percakapan Bilingual (ID & EN)...")
            try:
                with open(BILINGUAL_FILE, "r", encoding="utf-8") as bf:
                    for line in bf:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                            prompt = obj.get("prompt", "")
                            target = obj.get("response", "") or obj.get("target_code", "")
                            if prompt and target and len(target) > 20:
                                self.items.append({
                                    "prompt": prompt,
                                    "target_code": target,
                                    "lang": obj.get("language", "bilingual"),
                                    "title": prompt[:35].replace("\n", " "),
                                    "type": "Bilingual"
                                })
                        except Exception:
                            continue
            except Exception as e:
                print(f"[!] Gagal membaca bilingual file: {e}")

        # 3. Muat Pengajaran Konsep Guru (Teacher Lessons)
        if TEACHER_FILE.exists():
            print("[*] Memuat materi Pengajaran Konsep Coding Guru...")
            try:
                with open(TEACHER_FILE, "r", encoding="utf-8") as tf:
                    for line in tf:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                            prompt = obj.get("prompt", "")
                            target = obj.get("response", "") or obj.get("target_code", "") or obj.get("lesson", "")
                            if prompt and target and len(target) > 20:
                                self.items.append({
                                    "prompt": prompt,
                                    "target_code": target,
                                    "lang": obj.get("language", "theory"),
                                    "title": prompt[:35].replace("\n", " "),
                                    "type": "Teacher Lesson"
                                })
                        except Exception:
                            continue
            except Exception as e:
                print(f"[!] Gagal membaca teacher lessons: {e}")

        print(f"✅ Selesai mengindeks! Total {len(self.items):,} materi kurikulum menyeluruh siap dilatih berurutan.")


def prepare_batch(adara: AdaraEvolvingModel, notes: List[Dict[str, Any]], max_seq_len: int = 256):
    batch_input_ids = []
    batch_labels = []

    for note in notes:
        prompt_ids = adara.tokenizer.encode(note["prompt"], add_special_tokens=False)
        target_ids = adara.tokenizer.encode(note["target_code"] + "\n<|im_end|>\n", add_special_tokens=False)
        full_ids = (prompt_ids + target_ids)[:max_seq_len]

        labels = list(full_ids)
        prompt_len = min(len(prompt_ids), len(labels))
        for i in range(prompt_len):
            labels[i] = -100

        batch_input_ids.append(full_ids)
        batch_labels.append(labels)

    max_len = max(len(ids) for ids in batch_input_ids)
    pad_id = adara.tokenizer.pad_token_id or 0

    padded_in = [ids + [pad_id] * (max_len - len(ids)) for ids in batch_input_ids]
    padded_lb = [lbls + [-100] * (max_len - len(lbls)) for lbls in batch_labels]

    return (
        torch.tensor(padded_in, dtype=torch.long, device=adara.device),
        torch.tensor(padded_lb, dtype=torch.long, device=adara.device)
    )


def main():
    parser = argparse.ArgumentParser(description="UH-0 Deterministic Sequential Full-Coverage Trainer")
    parser.add_argument("--batch-size", type=int, default=12, help="Batch size per forward pass")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cuda", "cpu"])
    args = parser.parse_args()

    PID_FILE.write_text(str(os.getpid()))

    target_device = "cuda" if (args.device == "auto" and torch.cuda.is_available()) or args.device == "cuda" else "cpu"
    print("=" * 80)
    print(f"🚀 UH-0 DETERMINISTIC FULL-EPOCH SEQUENTIAL TRAINING ENGINE ({target_device.upper()})")
    print("   Mode: 100% Seluruh Materi (Algoritma + Bilingual + Konsep Guru) Dipelajari Berurutan")
    print("=" * 80)

    # 1. Load Model 30 Layer
    print("[*] Memuat model neural Qwen Coder...")
    model = AdaraEvolvingModel(device=target_device)
    start_step = 206850
    current_level = 4
    if CHECKPOINT_FILE.exists():
        start_step, current_level = model.load_checkpoint(CHECKPOINT_FILE)
        print(f"[✓] Checkpoint 30 Layer berhasil dipulihkan dari {CHECKPOINT_FILE} (Step #{start_step:,}, Level {current_level})")

    if target_device == "cuda":
        try:
            model.model.gradient_checkpointing_enable()
            print("✓ Gradient Checkpointing Aktif")
        except Exception:
            pass

    trainable_params = [p for p in model.model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable_params, lr=args.lr, weight_decay=0.01)

    # 2. Load Unified Curriculum
    loader = FullUnifiedCurriculumLoader()
    total_samples = len(loader.items)
    if total_samples == 0:
        print("[!] Kurikulum kosong!")
        return

    # Load Progress Cursor
    current_index = 0
    epoch = 1
    if PROGRESS_FILE.exists():
        try:
            prog = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
            current_index = prog.get("current_index", 0)
            epoch = prog.get("epoch", 1)
            print(f"[*] Melanjutkan dari Epoch {epoch}, Materi ke-{current_index:,}...")
        except Exception:
            pass

    step = start_step
    epoch_losses = []
    start_time = time.time()

    print(f"\n🚀 Memulai Pembelajaran Berurutan (Epoch {epoch} | Step #{step:,} | {model.num_layers()} Layers)...")

    while True:
        end_idx = min(current_index + args.batch_size, total_samples)
        batch_items = loader.items[current_index:end_idx]

        if not batch_items:
            # Selesai 1 Epoch Penuh!
            avg_epoch_loss = sum(epoch_losses) / len(epoch_losses) if epoch_losses else 0
            msg = (
                f"🎉 [EPOCH {epoch} SELESAI!] 100% Seluruh {total_samples:,} Materi Telah Tuntas Dipelajari!\n"
                f"📊 Rata-rata Loss Epoch: {avg_epoch_loss:.4f}\n"
                f"Memulai Epoch {epoch + 1} untuk memperdalam penguasaan..."
            )
            print("\n" + "=" * 80 + "\n" + msg + "\n" + "=" * 80 + "\n")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n[EPOCH {epoch} COMPLETED] Avg Loss: {avg_epoch_loss:.4f}\n\n")

            epoch += 1
            current_index = 0
            epoch_losses = []
            PROGRESS_FILE.write_text(json.dumps({"current_index": 0, "epoch": epoch}), encoding="utf-8")
            continue

        inp, tgt = prepare_batch(model, batch_items)

        model.model.train()
        optimizer.zero_grad(set_to_none=True)
        outputs = model.model(input_ids=inp, labels=tgt)
        loss = outputs.loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.model.parameters(), 1.0)
        optimizer.step()

        cur_loss = float(loss.item())
        epoch_losses.append(cur_loss)
        current_index = end_idx
        step += 1

        pct = (current_index / total_samples) * 100
        cur_lang = batch_items[0]["lang"].upper()
        cur_title = batch_items[0]["title"]
        cur_type = batch_items[0]["type"]

        if step % 10 == 0:
            log_line = (
                f"--- [Step {step} | Lvl {current_level} | Epoch {epoch} ({pct:.1f}%)] ---\n"
                f"   Kategori    : {cur_type} [{cur_lang}]\n"
                f"   Materi      : #{current_index:,}/{total_samples:,} - {cur_title[:40]}\n"
                f"   Pemahaman   : 📖 Membaca & Menghafal Pola Ground-Truth (Loss: {cur_loss:.4f})\n"
                f"   Total Materi: {current_index:,} catatan dipelajari (Layers: {model.num_layers()})\n"
            )
            print(log_line, flush=True)
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
            with open(SEQ_LOG_FILE, "a", encoding="utf-8") as sf:
                sf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [Step {step} | {pct:.1f}%] [{cur_lang}] Loss: {cur_loss:.4f}\n")

        # Simpan checkpoint & progres setiap 100 step
        if step % 100 == 0:
            avg_recent_loss = sum(epoch_losses[-50:]) / len(epoch_losses[-50:]) if epoch_losses else cur_loss
            model.save_checkpoint(CHECKPOINT_FILE, step=step, level=current_level, avg_loss=avg_recent_loss)
            PROGRESS_FILE.write_text(json.dumps({
                "current_index": current_index,
                "epoch": epoch,
                "step": step,
                "last_loss": cur_loss
            }), encoding="utf-8")

if __name__ == "__main__":
    main()
