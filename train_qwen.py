#!/usr/bin/env python3
"""
UH-0 v2 (Adara AI Self-Evolving Engine) - 24/7 Life Engine
Siklus Kehidupan Otonom Multi-Bahasa (80 Bahasa Pemrograman Nyata):
- Melatih langsung bobot neural network (Continual Weight Training - BUKAN LoRA)
- Menumbuhkan layer secara berkala (Net2Net Layer Growth: 494M -> 530M -> 566M -> 602M params)
- Menguji kode di Sandbox Multi-Bahasa secara real-time
- Menyimpan ingatan skill ke Replay Buffer dan checkpoint otomatis
"""

import os
import sys
import time
import argparse
from pathlib import Path
import torch

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from brain.model_qwen import AdaraEvolvingModel
from world.github_curriculum import GitHubCurriculum80
from world.executor import CodeExecutor
from memory.replay_buffer import ExperienceReplay

CHECKPOINT_FILE = BASE_DIR / "uh_zero_v2_checkpoint.pt"
LOG_FILE = BASE_DIR / "train.log"


def main():
    parser = argparse.ArgumentParser(description="Adara AI UH-0 v2 Continuous Evolving Engine")
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--lr", type=float, default=1.5e-5)
    parser.add_argument("--steps", type=int, default=0)
    args = parser.parse_args()

    print("=" * 70)
    print("🌟 ADARA AI - UH-0 v2 CONTINUOUS SELF-EVOLVING LIFE ENGINE")
    print("   Pondasi Cerdas 80 Bahasa Pemrograman • Net2Net Layer Growth")
    print(f"   Device Komputasi: {args.device.upper()} | LR: {args.lr}")
    print("=" * 70)

    # Multi-Core CPU Thread Scaling & Memory Optimization
    cpu_count = os.cpu_count() or 4
    torch.set_num_threads(cpu_count)
    if hasattr(torch, "set_num_interop_threads"):
        try:
            torch.set_num_interop_threads(min(4, cpu_count))
        except RuntimeError:
            pass
    print(f"[*] Thread Komputasi PyTorch: {torch.get_num_threads()} CPU Cores")

    # 1. Inisialisasi Model Evolving
    adara = AdaraEvolvingModel(device=args.device)
    start_step, current_level = adara.load_checkpoint(CHECKPOINT_FILE)

    trainable_params = [p for p in adara.model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable_params, lr=args.lr, weight_decay=0.01)
    curriculum = GitHubCurriculum80()
    executor = CodeExecutor()
    memory = ExperienceReplay(memory_dir=str(BASE_DIR / "memory"))

    step = start_step
    recent_losses = []
    consecutive_success = 0

    print(f"\n[🚀 Memulai Siklus Hidup] Step #{step + 1} | Parameter Aktif: {adara.count_parameters():,} ({adara.num_layers()} Layers)")

    try:
        while True:
            step += 1
            if args.steps > 0 and step > (start_step + args.steps):
                break

            # A. Ambil Soal Coding Nyata dari Kurikulum 80 Bahasa (90% baru, 10% review)
            raw_tasks = [curriculum.sample_task()]
            mixed_tasks = memory.mix_batch(raw_tasks, replay_ratio=0.1)
            task = mixed_tasks[0]

            prompt = task["prompt"]
            ground_truth = task["ground_truth"]
            task_lang = task.get("language", "python")
            task_name = task.get("language_name", task_lang.title())

            # B. Langkah Pembelajaran Langsung pada Bobot Transformer (Continual Weight Training)
            loss_val = adara.train_step(optimizer, prompt, ground_truth, max_seq_len=256)
            recent_losses.append(loss_val)
            if len(recent_losses) > 20:
                recent_losses.pop(0)

            # C. Setiap 15 Step: Evaluasi Hasil Generasi di Sandbox Multi-Bahasa
            if step % 15 == 0 or step == (start_step + 1):
                generated_code = adara.generate(prompt, max_new_tokens=120, temperature=0.6)
                
                # Uji di Sandbox
                expected_out = task.get("expected_py")
                test_call = task.get("test_call_py")
                success, feedback, reward = executor.execute_multilang(generated_code, task_lang, expected_output=expected_out, test_call=test_call)
                avg_loss = sum(recent_losses) / max(1, len(recent_losses))
                status_icon = "✅" if success else "❌"

                log_entry = (
                    f"--- [Step {step:05d} | Level {current_level} | Params: {adara.count_parameters():,} | Layers: {adara.num_layers()}] ---\n"
                    f"   Bahasa      : {task_name} ({task_lang})\n"
                    f"   Topik       : {task.get('title', 'Coding Function')}\n"
                    f"   Sandbox     : {status_icon} {feedback} (Reward: {reward:+.1f} | Loss: {avg_loss:.4f})\n"
                )
                print(log_entry.strip())
                sys.stdout.flush()



                if success:
                    consecutive_success += 1
                    if "Error" not in feedback and len(generated_code.strip()) >= 5:
                        memory.save_experience(prompt, generated_code, str(expected_out or "success"), current_level, language=task_lang, language_name=task_name)
                    if consecutive_success >= 3 and current_level < 4:
                        current_level += 1
                        consecutive_success = 0
                        print(f"\n🎉 [NAIK TINGKAT!] Adara AI berevolusi ke Level {current_level}!\n")
                else:
                    consecutive_success = max(0, consecutive_success - 1)

            # D. NET2NET LAYER GROWTH (PERTUMBUHAN ARSITEKTUR FISIK)
            # Tahap 1: Di Step 150 -> Tambah 2 Layer (24 -> 26 Layer, +36M Parameter!)
            if step == 150 and adara.num_layers() == 24:
                adara.grow_deeper(additional_layers=2)
                optimizer = torch.optim.AdamW([p for p in adara.model.parameters() if p.requires_grad], lr=args.lr * 0.8, weight_decay=0.01)
                adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, avg_loss)
                print(f"🚀 [KAPASITAS BARU] Otak Adara membesar menjadi {adara.count_parameters():,} parameter ({adara.num_layers()} Layers)!\n")

            # Tahap 2: Di Step 500 -> Tambah 2 Layer (26 -> 28 Layer, +36M Parameter!)
            elif step == 500 and adara.num_layers() == 26:
                adara.grow_deeper(additional_layers=2)
                optimizer = torch.optim.AdamW([p for p in adara.model.parameters() if p.requires_grad], lr=args.lr * 0.7, weight_decay=0.01)
                adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, avg_loss)
                print(f"🚀 [KAPASITAS BARU] Otak Adara membesar menjadi {adara.count_parameters():,} parameter ({adara.num_layers()} Layers)!\n")

            # Tahap 3: Di Step 1500 -> Tambah 2 Layer (28 -> 30 Layer, +36M Parameter!)
            elif step == 1500 and adara.num_layers() == 28:
                adara.grow_deeper(additional_layers=2)
                optimizer = torch.optim.AdamW([p for p in adara.model.parameters() if p.requires_grad], lr=args.lr * 0.6, weight_decay=0.01)
                adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, avg_loss)
                print(f"🚀 [KAPASITAS BARU] Otak Adara membesar menjadi {adara.count_parameters():,} parameter ({adara.num_layers()} Layers)!\n")

            # Simpan checkpoint berkala setiap 50 step
            if step % 50 == 0:
                adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, sum(recent_losses) / max(1, len(recent_losses)))

    except KeyboardInterrupt:
        print("\n[!] Dihentikan pengguna, menyimpan checkpoint...")
        adara.save_checkpoint(CHECKPOINT_FILE, step, current_level, 0.0)


if __name__ == "__main__":
    main()
