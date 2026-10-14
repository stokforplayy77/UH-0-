#!/usr/bin/env python3
"""
UH-0 v2 (Adara AI Self-Evolving Engine) - Neural Architecture
Menggabungkan Pondasi Cerdas Qwen-0.5B dengan Mekanisme Pertumbuhan Lapisan Nyata (Net2Net Layer Stacking).
BUKAN sekadar LoRA adapter: Bobot neuron transformer intinya diperbarui secara langsung (Continual Training)
dan arsitekturnya dapat menambah lapisan Transformer Block baru secara fisik seiring waktu.
"""

import copy
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, Dict, Any
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig


MODEL_NAME = "Qwen/Qwen2.5-Coder-0.5B-Instruct"


class AdaraEvolvingModel:
    def __init__(self, model_name: str = MODEL_NAME, device: str = "cpu"):
        self.device = device
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
        except Exception:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        if device == "cuda":
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        else:
            dtype = torch.float32
        print(f"[*] Memuat pondasi neural Qwen Coder ({model_name}) ke {device} ({dtype})...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=dtype,
                low_cpu_mem_usage=True,
                local_files_only=True
            ).to(device)
        except Exception:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=dtype,
                low_cpu_mem_usage=True
            ).to(device)

        # Konfigurasi bobot transformer yang dilatih langsung (Top Transformer Blocks)
        self.configure_trainable_layers(num_top_layers=4)
        print(f"✓ Model aktif: {self.count_parameters():,} parameter ({self.num_layers()} layers)")

    def configure_trainable_layers(self, num_top_layers: int = 4):
        """
        Melatih secara langsung (unfrozen) N blok Transformer Layer teratas + layer Net2Net baru.
        Mencegah swap thrashing di CPU sambil tetap memperbarui bobot transformer secara nyata (Bukan LoRA).
        """
        for param in self.model.parameters():
            param.requires_grad = False

        for layer in self.model.model.layers[-num_top_layers:]:
            for param in layer.parameters():
                param.requires_grad = True

        trainable = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        print(f"✓ Bobot aktif dilatih: {trainable:,} parameter nyata pada {num_top_layers} blok Transformer teratas")

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.model.parameters())

    def num_layers(self) -> int:
        return len(self.model.model.layers)

    def grow_deeper(self, additional_layers: int = 2) -> int:
        """
        Net2Net Layer Expansion:
        Menambahkan blok Transformer Layer baru secara fisik ke dalam arsitektur model.
        Inisialisasi residual projection dengan scaling mendekati 0 agar fungsi awal tidak amnesia.
        """
        initial_layers = self.num_layers()
        initial_params = self.count_parameters()
        print(f"\n[🌱 Net2Net Growth] Memperdalam Lapisan Otak: {initial_layers} -> {initial_layers + additional_layers} Layers...")

        template_layer = self.model.model.layers[-1]

        for _ in range(additional_layers):
            new_layer = copy.deepcopy(template_layer)
            # Identity initialization agar output stabil saat baru lahir
            with torch.no_grad():
                if hasattr(new_layer.self_attn, "o_proj"):
                    new_layer.self_attn.o_proj.weight.mul_(0.02)
                if hasattr(new_layer.mlp, "down_proj"):
                    new_layer.mlp.down_proj.weight.mul_(0.02)
            
            # Pasang layer baru ke jaringan saraf
            self.model.model.layers.append(new_layer)

        # Update konfigurasi arsitektur
        self.model.config.num_hidden_layers = len(self.model.model.layers)
        if hasattr(self.model.config, "layer_types") and isinstance(self.model.config.layer_types, list):
            while len(self.model.config.layer_types) < len(self.model.model.layers):
                self.model.config.layer_types.append("full_attention")

        new_params = self.count_parameters()

        # Pastikan layer baru dan top layers aktif dilatih
        self.configure_trainable_layers(num_top_layers=4 + additional_layers)

        print(f"✓ Pertumbuhan Berhasil! Parameter Baru: {new_params:,} (+{new_params - initial_params:,} parameter aktif)")
        return new_params

    def train_step(self, optimizer, prompt: str, target_code: str, max_seq_len: int = 512) -> float:
        """
        Langkah pembelajaran langsung pada bobot transformer dengan Prompt Masking.
        Hanya token target code yang dihitung loss-nya, kalimat prompt diabaikan (ignore_index=-100).
        """
        self.model.train()
        
        prompt_ids = self.tokenizer.encode(prompt, add_special_tokens=False)
        target_ids = self.tokenizer.encode(target_code + "\n<|im_end|>\n", add_special_tokens=False)

        full_ids = prompt_ids + target_ids
        if len(full_ids) > max_seq_len:
            full_ids = full_ids[:max_seq_len]

        input_tensor = torch.tensor([full_ids[:-1]], dtype=torch.long, device=self.device)
        target_tensor = torch.tensor([full_ids[1:]], dtype=torch.long, device=self.device)

        # Mask prompt tokens
        prompt_len = min(len(prompt_ids) - 1, target_tensor.size(1))
        if prompt_len > 0:
            target_tensor[0, :prompt_len] = -100

        optimizer.zero_grad()
        outputs = self.model(input_ids=input_tensor, labels=target_tensor)
        loss = outputs.loss

        if loss is not None and not torch.isnan(loss):
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            optimizer.step()
            return float(loss.item())

        return 0.0

    @torch.no_grad()
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 160,
        temperature: float = 0.6,
        repetition_penalty: float = 1.15
    ) -> str:
        """Menghasilkan kode dengan autoregressive sampling dan repetition penalty."""
        self.model.eval()
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True if temperature > 0 else False,
            top_p=0.9,
            repetition_penalty=repetition_penalty,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id
        )

        prompt_len = inputs["input_ids"].shape[1]
        gen_tokens = output_ids[0, prompt_len:]
        return self.tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()

    def save_checkpoint(self, path: Path, step: int, level: int, avg_loss: float):
        """Menyimpan seluruh bobot arsitektur yang telah berevolusi."""
        data = {
            "step": step,
            "level": level,
            "loss": avg_loss,
            "num_layers": self.num_layers(),
            "num_parameters": self.count_parameters(),
            "model_state_dict": self.model.state_dict(),
            "config": self.model.config.to_dict()
        }
        tmp_path = path.with_suffix(".tmp")
        torch.save(data, tmp_path)
        tmp_path.replace(path)
        print(f"[💾 Checkpoint] Otak Adara tersimpan ({self.count_parameters():,} params, Layer: {self.num_layers()})")

    def load_checkpoint(self, path) -> Tuple[int, int]:
        """Memulihkan ingatan dan arsitektur model."""
        path = Path(path)
        if not path.exists():
            return 0, 1
        print(f"[*] Memulihkan checkpoint Adara dari {path}...")
        ckpt = torch.load(path, map_location=self.device)
        saved_layers = ckpt.get("num_layers", 24)
        current_layers = self.num_layers()

        # Jika sebelumnya model sudah bertambah layer, samakan arsitekturnya dulu
        if saved_layers > current_layers:
            self.grow_deeper(additional_layers=saved_layers - current_layers)

        self.model.load_state_dict(ckpt["model_state_dict"])
        if self.device == "cpu":
            self.model.to(torch.float32)
        step = ckpt.get("step", 0)
        level = ckpt.get("level", 1)
        print(f"✓ Berhasil memulihkan Adara di Step #{step}, Level {level} ({self.count_parameters():,} params)")
        return step, level
