#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - Dynamic LoRA & MoE Expert Router
Modul perutean adaptif untuk memilih atau memadukan skill expert
secara dinamis sesuai domain soal (Aritmatika, Logika, Syntax, Struk Parsing).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple


class LoRALinear(nn.Module):
    """Low-Rank Adaptation (LoRA) layer pembantu untuk adapter skill."""
    def __init__(self, base_linear: nn.Linear, rank: int = 4, alpha: float = 8.0):
        super().__init__()
        self.base = base_linear
        # Bekukan base linear
        self.base.weight.requires_grad = False
        
        in_dim = base_linear.in_features
        out_dim = base_linear.out_features
        self.rank = rank
        self.scaling = alpha / rank

        self.lora_A = nn.Parameter(torch.randn(rank, in_dim) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(out_dim, rank))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        base_out = self.base(x)
        lora_out = (x @ self.lora_A.t() @ self.lora_B.t()) * self.scaling
        return base_out + lora_out


class DynamicSkillRouter(nn.Module):
    """
    Router yang memetakan embedding representasi ke bobot perutean MoE (Mixture of Experts)
    atau memilih skill library yang sesuai.
    """
    def __init__(self, dim: int, num_skills: int = 3):
        super().__init__()
        self.dim = dim
        self.num_skills = num_skills
        self.gate = nn.Linear(dim, num_skills)
        self.skill_names = ["Aritmatika", "Sintaks_Python", "Parsing_Data"]

    def forward(self, hidden_states: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # hidden_states: (B, T, C) -> mean pooling ke (B, C)
        pooled = hidden_states.mean(dim=1)
        logits = self.gate(pooled)
        weights = F.softmax(logits, dim=-1)
        selected_skill = torch.argmax(weights, dim=-1)
        return weights, selected_skill
