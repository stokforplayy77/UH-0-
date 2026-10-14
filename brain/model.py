"""
UH-0 (UH Labs Zero) - Neural Architecture
Self-Evolving Miniature Transformer for Autonomous Code Learning
Starts at ~1M parameters (dim=192, 4 layers, byte-level tokenizer)
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple


class ByteTokenizer:
    """
    Byte-level Tokenizer with zero external dependencies.
    Maps any Python code string to token IDs (0-255: raw bytes, 256: PAD, 257: BOS, 258: EOS)
    Vocab size: 260
    """
    PAD_ID = 256
    BOS_ID = 257
    EOS_ID = 258
    VOCAB_SIZE = 260

    def encode(self, text: str, add_bos: bool = True, add_eos: bool = False) -> list[int]:
        tokens = list(text.encode("utf-8"))
        if add_bos:
            tokens = [self.BOS_ID] + tokens
        if add_eos:
            tokens = tokens + [self.EOS_ID]
        return tokens

    def decode(self, tokens: list[int]) -> str:
        valid_bytes = [t for t in tokens if 0 <= t < 256]
        return bytes(valid_bytes).decode("utf-8", errors="ignore")


class CausalSelfAttention(nn.Module):
    def __init__(self, dim: int, n_heads: int = 4, max_seq_len: int = 512):
        super().__init__()
        assert dim % n_heads == 0, f"dim {dim} must be divisible by n_heads {n_heads}"
        self.dim = dim
        self.n_heads = n_heads
        self.head_dim = dim // n_heads

        self.q_proj = nn.Linear(dim, dim, bias=False)
        self.k_proj = nn.Linear(dim, dim, bias=False)
        self.v_proj = nn.Linear(dim, dim, bias=False)
        self.out_proj = nn.Linear(dim, dim, bias=False)

        # Causal mask buffer
        mask = torch.tril(torch.ones(max_seq_len, max_seq_len)).bool()
        self.register_buffer("mask", mask)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.size()

        q = self.q_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)

        # Scaled dot-product attention
        scores = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        scores = scores.masked_fill(~self.mask[:T, :T], float("-inf"))
        attn_weights = F.softmax(scores, dim=-1)

        out = (attn_weights @ v).transpose(1, 2).contiguous().view(B, T, C)
        return self.out_proj(out)


class MLP(nn.Module):
    def __init__(self, dim: int, mlp_dim: int):
        super().__init__()
        self.dim = dim
        self.mlp_dim = mlp_dim
        self.fc1 = nn.Linear(dim, mlp_dim, bias=False)
        self.fc2 = nn.Linear(mlp_dim, dim, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc2(F.gelu(self.fc1(x)))


class TransformerBlock(nn.Module):
    def __init__(self, dim: int, n_heads: int = 4, mlp_dim: Optional[int] = None):
        super().__init__()
        mlp_dim = mlp_dim or dim * 2
        self.dim = dim
        self.attn_norm = nn.LayerNorm(dim)
        self.attn = CausalSelfAttention(dim, n_heads=n_heads)
        self.mlp_norm = nn.LayerNorm(dim)
        self.mlp = MLP(dim, mlp_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.attn_norm(x))
        x = x + self.mlp(self.mlp_norm(x))
        return x


class UHZero(nn.Module):
    """
    UH-0 Transformer: Miniature, self-growing neural brain.
    Initial configuration: dim=192, 4 layers, n_heads=4 -> ~1.1M parameters.
    """
    def __init__(
        self,
        vocab_size: int = ByteTokenizer.VOCAB_SIZE,
        dim: int = 192,
        n_layers: int = 4,
        n_heads: int = 4,
        max_seq_len: int = 512
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.dim = dim
        self.n_layers = n_layers
        self.n_heads = n_heads
        self.max_seq_len = max_seq_len

        self.tok_embed = nn.Embedding(vocab_size, dim)
        self.pos_embed = nn.Embedding(max_seq_len, dim)

        self.layers = nn.ModuleList([
            TransformerBlock(dim, n_heads=n_heads, mlp_dim=dim * 2)
            for _ in range(n_layers)
        ])
        self.norm = nn.LayerNorm(dim)
        self.head = nn.Linear(dim, vocab_size, bias=False)

        # Weight tying (embedding and output head)
        self.head.weight = self.tok_embed.weight

        self.tokenizer = ByteTokenizer()

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters())

    def get_config(self) -> dict:
        return {
            "dim": self.dim,
            "n_layers": self.n_layers,
            "n_heads": self.n_heads,
            "max_seq_len": self.max_seq_len,
            "vocab_size": self.vocab_size
        }

    def forward(self, idx: torch.Tensor, targets: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        B, T = idx.size()
        assert T <= self.max_seq_len, f"Sequence length {T} exceeds maximum {self.max_seq_len}"

        pos = torch.arange(0, T, dtype=torch.long, device=idx.device)
        x = self.tok_embed(idx) + self.pos_embed(pos)

        for block in self.layers:
            x = block(x)

        x = self.norm(x)
        logits = self.head(x)

        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, self.vocab_size), targets.view(-1), ignore_index=-100)

        return logits, loss

    @torch.no_grad()
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 120,
        temperature: float = 0.7,
        top_k: int = 20,
        repetition_penalty: float = 1.25,
        device: str = "cpu"
    ) -> str:
        self.eval()
        tokens = self.tokenizer.encode(prompt, add_bos=True)
        idx = torch.tensor([tokens], dtype=torch.long, device=device)

        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.max_seq_len:]
            logits, _ = self.forward(idx_cond)
            logits = logits[:, -1, :].clone()

            # Terapkan Repetition Penalty agar tidak looping karakter
            if repetition_penalty != 1.0 and idx.size(1) > len(tokens):
                recent_generated = set(idx[0, len(tokens):].tolist())
                for tid in recent_generated:
                    if logits[0, tid] < 0:
                        logits[0, tid] *= repetition_penalty
                    else:
                        logits[0, tid] /= repetition_penalty

            logits = logits / max(temperature, 1e-5)

            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = -float("Inf")

            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)

            if idx_next.item() == ByteTokenizer.EOS_ID:
                break

            idx = torch.cat((idx, idx_next), dim=1)

        new_tokens = idx[0, len(tokens):].tolist()
        return self.tokenizer.decode(new_tokens)
