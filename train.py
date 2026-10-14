#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - Autonomous Continuous Life Engine
24/7 Fully Autonomous Self-Evolving Training Loop
- Automatically loads checkpoints & resumes where it left off
- Periodically auto-saves state to uh_zero_checkpoint.pt
- Multi-stage Net2Net expansion (Wider & Deeper) across 80 programming languages
- Evaluates code in Sandbox and memorizes successes in Replay Buffer
"""

import os
import sys
import time
import argparse
from pathlib import Path
import torch
import torch.optim as optim

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from brain.model import UHZero, ByteTokenizer
from brain.grow import grow_wider, grow_deeper
from brain.languages import LANGUAGES_CATALOG
from world.executor import CodeExecutor
from world.tasks import TaskCurriculum
from memory.replay_buffer import ExperienceReplay

CHECKPOINT_FILE = BASE_DIR / "uh_zero_checkpoint.pt"
tokenizer = ByteTokenizer()


def encode_text(text: str, max_len: int = 256) -> torch.Tensor:
    tokens = tokenizer.encode(text, add_bos=True)
    if len(tokens) > max_len:
        tokens = tokens[:max_len]
    return torch.tensor(tokens, dtype=torch.long)


def train_step(model, optimizer, prompt, target_code, device):
    prompt_tokens = tokenizer.encode(prompt, add_bos=True)
    target_tokens = tokenizer.encode(target_code + "\n", add_bos=False, add_eos=True)
    full_tokens = prompt_tokens + target_tokens
    if len(full_tokens) > model.max_seq_len:
        full_tokens = full_tokens[:model.max_seq_len]

    tokens = torch.tensor(full_tokens, dtype=torch.long, device=device)
    if len(tokens) < 2:
        return 0.0

    inputs = tokens[:-1].unsqueeze(0)
    targets = tokens[1:].clone().unsqueeze(0)

    # Prompt masking: Abaikan loss pada token soal/prompt
    prompt_len = min(len(prompt_tokens) - 1, targets.size(1))
    if prompt_len > 0:
        targets[0, :prompt_len] = -100

    model.train()
    optimizer.zero_grad()
    logits, loss = model(inputs, targets=targets)
    if loss is not None:
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        return loss.item()
    return 0.0


def save_checkpoint(model, optimizer, step, level, loss_val):
    tmp_path = CHECKPOINT_FILE.with_suffix(".tmp")
    data = {
        "config": model.get_config(),
        "model_state_dict": model.state_dict(),
        "step": step,
        "level": level,
        "loss": loss_val,
        "timestamp": time.time()
    }
    torch.save(data, tmp_path)
    tmp_path.replace(CHECKPOINT_FILE)


def main():
    parser = argparse.ArgumentParser(description="UH-0 Autonomous 24/7 Life Engine")
    parser.add_argument("--steps", type=int, default=0, help="0 untuk loop kehidupan 24/7 tanpa henti")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate awal")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    print("=" * 65)
    print("🌟 UH-0 (UH LABS ZERO) - 24/7 AUTONOMOUS LIFE ENGINE")
    print("   Evolusi Mandiri 80 Bahasa Pemrograman • Auto-Resume & Auto-Growth")
    print(f"   Device Komputasi: {args.device.upper()}")
    print("=" * 65)

    start_step = 0
    current_level = 1
    model = None

    # 1. Cek apakah ada Checkpoint Tersimpan (Auto-Resume)
    if CHECKPOINT_FILE.exists():
        try:
            print(f"[*] Menemukan checkpoint tersimpan: {CHECKPOINT_FILE}")
            ckpt = torch.load(CHECKPOINT_FILE, map_location=args.device)
            cfg = ckpt.get("config", {"dim": 128, "n_layers": 4, "n_heads": 4})
            model = UHZero(**cfg).to(args.device)
            model.load_state_dict(ckpt["model_state_dict"])
            start_step = ckpt.get("step", 0)
            current_level = ckpt.get("level", 1)
            print(f"✓ Berhasil memulihkan ingatan! Melanjutkan dari Step #{start_step}, Level {current_level}")
            print(f"  Parameter Aktif: {model.count_parameters():,}")
        except Exception as e:
            print(f"[-] Gagal memuat checkpoint ({e}), memulai dari Genesis...")

    if model is None:
        # Inisialisasi Genesis: Fase Bayi (dim=128, 4 layers, ~592K params)
        model = UHZero(vocab_size=ByteTokenizer.VOCAB_SIZE, dim=128, n_layers=4, n_heads=4, max_seq_len=256).to(args.device)
        print(f"\n[👶 Genesis Dimulai] Otak lahir dengan {model.count_parameters():,} parameter.")

    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    curriculum = TaskCurriculum()
    executor = CodeExecutor()
    memory = ExperienceReplay(memory_dir=str(BASE_DIR / "memory"))

    step = start_step
    recent_losses = []
    consecutive_success = 0
    initial_params = model.count_parameters()

    # Track growth stages
    growth_history = []

    try:
        while True:
            step += 1
            if args.steps > 0 and step > (start_step + args.steps):
                break

            # A. Buat Soal dari Kurikulum (Multilang 80 bahasa) + 10% Replay Memory
            raw_tasks = [curriculum.generate_task(level=current_level)]
            mixed_tasks = memory.mix_batch(raw_tasks, replay_ratio=0.1)
            task = mixed_tasks[0]

            prompt = task["prompt"]
            ground_truth = task["ground_truth"]
            expected_out = task["expected_output"]
            task_lang = task.get("language", "python")

            # B. Langkah Pembelajaran (Supervised Priming)
            loss_val = train_step(model, optimizer, prompt, ground_truth, args.device)
            recent_losses.append(loss_val)
            if len(recent_losses) > 30:
                recent_losses.pop(0)

            # C. Setiap 25 Step: Evaluasi di Sandbox Dunia Nyata
            if step % 25 == 0 or step == (start_step + 1):
                model.eval()
                generated_ans = model.generate(prompt, max_new_tokens=48, temperature=0.6, repetition_penalty=1.25, device=args.device)
                
                code_attempt = generated_ans[len(prompt):].strip() if generated_ans.startswith(prompt) else generated_ans.strip()
                if "\n" in code_attempt:
                    code_lines = [l for l in code_attempt.split("\n") if l.strip() and not l.startswith(("#", "//", "/*", "--"))]
                    eval_code = "\n".join(code_lines[:3]) if code_lines else code_attempt
                else:
                    eval_code = code_attempt

                # Eksekusi di Sandbox Multi-Bahasa
                success, feedback, reward = executor.execute_multilang(eval_code, task_lang, expected_output=expected_out)
                avg_loss = sum(recent_losses) / max(1, len(recent_losses))
                status_icon = "✅" if success else "❌"

                print(f"--- [Step {step:05d} | Level {current_level} | Params: {model.count_parameters():,}] ---")
                print(f"   Bahasa      : {task.get('language_name', task_lang.title())} ({task_lang})")
                print(f"   Soal        : {prompt.strip()[:65]}...")
                print(f"   Sandbox     : {status_icon} {feedback} (Reward: {reward:+.1f} | Loss: {avg_loss:.4f})")

                if success:
                    consecutive_success += 1
                    if "Error" not in feedback and len(eval_code.strip()) >= 3:
                        memory.save_experience(prompt, eval_code, expected_out, current_level, language=task_lang, language_name=task.get('language_name', task_lang.title()))
                    if consecutive_success >= 3 and current_level < 4:
                        current_level += 1
                        consecutive_success = 0
                        print(f"\n🎉 [NAIK TINGKAT!] Model berevolusi ke Level {current_level}: {curriculum.level_names.get(current_level, 'Level ' + str(current_level))}\n")
                else:
                    consecutive_success = max(0, consecutive_success - 1)

            # D. AUTO-GROWTH NET2NET (TUMBUH OTOMATIS SAAT BATAS TERCAPAI)
            # Stage 1: Step 250 -> Perlebar dimensi (128 -> 256)
            if step == 250 and model.dim == 128:
                print("\n" + "=" * 65)
                print(f"⚡ [EVOLUSI NET2NET TAHAP 1] Otak di step {step} bertransisi ke Fase Balita!")
                print(f"   Memperlebar Dimensi Neuron: 128 -> 256...")
                print("=" * 65)
                model = grow_wider(model, target_dim=256).to(args.device)
                optimizer = optim.AdamW(model.parameters(), lr=args.lr * 0.8, weight_decay=0.01)
                save_checkpoint(model, optimizer, step, current_level, avg_loss)
                print(f"🚀 [KAPASITAS BARU] {model.count_parameters():,} parameter aktif!\n")

            # Stage 2: Step 1000 -> Tambah layer (4 -> 6 layer)
            elif step == 1000 and model.n_layers == 4:
                print("\n" + "=" * 65)
                print(f"⚡ [EVOLUSI NET2NET TAHAP 2] Otak di step {step} bertransisi ke Fase Anak SD!")
                print(f"   Memperdalam Lapisan Pemikiran: 4 -> 6 Layers...")
                print("=" * 65)
                model = grow_deeper(model, additional_layers=2).to(args.device)
                optimizer = optim.AdamW(model.parameters(), lr=args.lr * 0.7, weight_decay=0.01)
                save_checkpoint(model, optimizer, step, current_level, avg_loss)
                print(f"🚀 [KAPASITAS BARU] {model.count_parameters():,} parameter aktif!\n")

            # Stage 3: Step 3000 -> Perlebar lagi (256 -> 384)
            elif step == 3000 and model.dim == 256:
                print("\n" + "=" * 65)
                print(f"⚡ [EVOLUSI NET2NET TAHAP 3] Otak di step {step} bertransisi ke Fase Remaja!")
                print(f"   Memperlebar Dimensi Neuron: 256 -> 384...")
                print("=" * 65)
                model = grow_wider(model, target_dim=384).to(args.device)
                optimizer = optim.AdamW(model.parameters(), lr=args.lr * 0.6, weight_decay=0.01)
                save_checkpoint(model, optimizer, step, current_level, avg_loss)
                print(f"🚀 [KAPASITAS BARU] {model.count_parameters():,} parameter aktif!\n")

            # E. PERIODIC AUTO-SAVE CHECKPOINT (Setiap 50 Step)
            if step % 50 == 0:
                avg_l = sum(recent_losses) / max(1, len(recent_losses))
                save_checkpoint(model, optimizer, step, current_level, avg_l)

            # Istirahat mikro untuk efisiensi CPU
            time.sleep(0.003)

    except KeyboardInterrupt:
        print("\n[!] Loop kehidupan dijeda.")

    # Simpan checkpoint final saat dihentikan
    avg_l = sum(recent_losses) / max(1, len(recent_losses)) if recent_losses else 0.0
    save_checkpoint(model, optimizer, step, current_level, avg_l)

    final_params = model.count_parameters()
    print("\n" + "=" * 65)
    print("🏁 HASIL SIKLUS KEHIDUPAN UH-0 (UH LABS ZERO)")
    print(f"   Step Terakhir  : #{step}")
    print(f"   Parameter Awal : {initial_params:,}")
    print(f"   Parameter Akhir: {final_params:,} (Tumbuh {final_params/initial_params:.1f}x)")
    print(f"   Level Tercapai : Level {current_level} ({curriculum.level_names.get(current_level, 'Level ' + str(current_level))})")
    print(f"   Checkpoint     : Tersimpan aman di {CHECKPOINT_FILE}")
    print("=" * 65)


if __name__ == "__main__":
    main()
