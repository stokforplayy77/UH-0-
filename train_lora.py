#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - Skill Fine-Tuning via LoRA Adapter
Melatih skill spesifik (seperti Parsing Struk Belanja & Ongkir) pada model 1M
menggunakan Low-Rank Adaptation (LoRA) tanpa merusak pengetahuan dasar.
"""

import os
import sys
import json
import argparse
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from brain.model import UHZero, ByteTokenizer
from brain.router import LoRALinear


def encode_text(model: UHZero, text: str) -> torch.Tensor:
    tokens = model.tokenizer.encode(text, add_bos=True, add_eos=True)
    if len(tokens) > model.max_seq_len:
        tokens = tokens[:model.max_seq_len]
    return torch.tensor(tokens, dtype=torch.long)


def apply_lora_to_model(model: UHZero, rank: int = 4, alpha: float = 8.0):
    """Memasang layer LoRA pada q_proj dan v_proj di setiap Transformer block."""
    lora_params = []
    for layer in model.layers:
        layer.attn.q_proj = LoRALinear(layer.attn.q_proj, rank=rank, alpha=alpha)
        layer.attn.v_proj = LoRALinear(layer.attn.v_proj, rank=rank, alpha=alpha)
        lora_params.extend([
            layer.attn.q_proj.lora_A, layer.attn.q_proj.lora_B,
            layer.attn.v_proj.lora_A, layer.attn.v_proj.lora_B
        ])
    return lora_params


def load_dataset(dataset_path: Path):
    samples = []
    if not dataset_path.exists():
        print(f"[!] File dataset {dataset_path} tidak ditemukan!")
        return samples
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line.strip())
                    samples.append((data["input"], data["output"]))
                except Exception:
                    pass
    return samples


def main():
    parser = argparse.ArgumentParser(description="UH-0 LoRA Fine-Tuner")
    parser.add_argument("--epochs", type=int, default=20, help="Jumlah epoch training")
    parser.add_argument("--lr", type=float, default=2e-3, help="Learning rate untuk LoRA")
    parser.add_argument("--dataset", type=str, default=str(BASE_DIR / "data" / "dataset_struk.jsonl"))
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    print("=" * 65)
    print("🏷️  UH-0 (UH LABS ZERO) - LORA SPECIALIZED SKILL TRAINER")
    print("   Melatih Keahlian Khusus Parsing Struk & Ekstraksi Data")
    print(f"   Dataset: {args.dataset}")
    print(f"   Device : {args.device.upper()}")
    print("=" * 65)

    # 1. Inisialisasi Model Dasar (1.2M params)
    model = UHZero(vocab_size=ByteTokenizer.VOCAB_SIZE, dim=128, n_layers=4, n_heads=4, max_seq_len=256).to(args.device)
    base_params = model.count_parameters()

    # 2. Pasang LoRA Adapter
    lora_params = apply_lora_to_model(model, rank=4, alpha=8.0)
    trainable_lora_params = sum(p.numel() for p in lora_params if p.requires_grad)

    print(f"\n[🔧 Arsitektur Adapter] Parameter Dasar Beku : {base_params:,}")
    print(f"   Parameter Aktif LoRA       : {trainable_lora_params:,} ({trainable_lora_params/base_params*100:.2f}%)")

    # 3. Muat Dataset
    dataset = load_dataset(Path(args.dataset))
    print(f"[📦 Dataset] Memuat {len(dataset)} contoh data latih spesifik.")
    if not dataset:
        return

    optimizer = optim.AdamW(lora_params, lr=args.lr, weight_decay=0.01)

    print("\n[🚀 Memulai Fine-Tuning LoRA...]")
    for epoch in range(1, args.epochs + 1):
        total_loss = 0.0
        for inp, outp in dataset:
            text = f"Input: {inp}\nOutput: {outp}\n"
            tokens = encode_text(model, text).to(args.device)
            if len(tokens) < 2:
                continue

            inputs = tokens[:-1].unsqueeze(0)
            targets = tokens[1:].unsqueeze(0)

            model.train()
            optimizer.zero_grad()
            logits, loss = model(inputs, targets=targets)
            if loss is not None:
                loss.backward()
                optimizer.step()
                total_loss += loss.item()

        avg_loss = total_loss / max(1, len(dataset))
        if epoch % 5 == 0 or epoch == 1:
            print(f"   Epoch {epoch:02d}/{args.epochs:02d} | Avg Loss: {avg_loss:.4f}")

    # Simpan Adapter ke skill_library
    save_path = BASE_DIR / "memory" / "skill_library" / "lora_struk_adapter.pt"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "lora_state": [p.data for p in lora_params],
        "rank": 4,
        "alpha": 8.0,
        "skill": "struk_and_shipping_parser"
    }, save_path)
    print(f"\n✅ [SUKSES] Skill baru berhasil disimpan ke: {save_path.relative_to(BASE_DIR)}")

    # Uji coba inferensi dengan skill baru
    print("\n[🧪 Pengujian Inferensi Skill Baru]:")
    model.eval()
    test_prompt = "Input: struk: INDOMARET TOTAL Rp 28.500\nOutput: "
    generated = model.generate(test_prompt, max_new_tokens=40, temperature=0.3, device=args.device)
    print(f"   Prompt : {test_prompt.strip()}")
    print(f"   Hasil  : {generated.strip()}")
    print("=" * 65)


if __name__ == "__main__":
    main()
