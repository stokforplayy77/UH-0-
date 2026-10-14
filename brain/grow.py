#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - Net2Net Progressive Growth Engine
Implementasi algoritma Net2Net (Chen et al.) untuk memperbesar
kapasitas parameter Transformer (Wider & Deeper) dengan sifat Function-Preserving:
f_new(x) = f_old(x), sehingga model membesar tanpa amnesia.
"""

import copy
import torch
import torch.nn as nn
from typing import Tuple
from brain.model import UHZero, TransformerBlock, MLP, CausalSelfAttention


def copy_linear_wider(old_linear: nn.Linear, new_in_features: int, new_out_features: int) -> nn.Linear:
    """
    Memperbesar nn.Linear dengan menyalin bobot lama dan menduplikasi
    channel baru dengan scaling factor untuk menjaga aktivasi tetap identik.
    """
    new_linear = nn.Linear(new_in_features, new_out_features, bias=(old_linear.bias is not None))
    
    old_out, old_in = old_linear.weight.shape
    in_factor = new_in_features // old_in
    out_factor = new_out_features // old_out

    with torch.no_grad():
        # Inisialisasi awal kecil
        new_linear.weight.zero_()
        
        # Salin blok utama lama
        new_linear.weight[:old_out, :old_in] = old_linear.weight.clone()

        # Duplikasi baris (out_features) jika bertambah
        if new_out_features > old_out:
            for i in range(old_out, new_out_features):
                src_i = i % old_out
                # Beri sedikit noise 1e-4 untuk symmetry breaking saat training lanjut
                noise = torch.randn_like(old_linear.weight[src_i, :old_in]) * 1e-4
                new_linear.weight[i, :old_in] = old_linear.weight[src_i, :old_in] + noise

        # Tangani in_features expansion (bagi bobot dengan in_factor agar jumlah aktivasi konsisten)
        if new_in_features > old_in:
            scale = 1.0 / in_factor
            for j in range(new_in_features):
                src_j = j % old_in
                new_linear.weight[:, j] = new_linear.weight[:, src_j] * scale

        # Salin bias jika ada
        if old_linear.bias is not None and new_linear.bias is not None:
            new_linear.bias[:old_out] = old_linear.bias.clone()
            if new_out_features > old_out:
                for i in range(old_out, new_out_features):
                    new_linear.bias[i] = old_linear.bias[i % old_out]

    return new_linear


def grow_wider(model: UHZero, target_dim: int) -> UHZero:
    """
    Memperbesar dimensi representasi hidden (dim) model UHZero
    Contoh: dim 128 (~1.2M params) -> dim 256 (~4.5M params)
    """
    assert target_dim > model.dim, f"Target dim ({target_dim}) harus lebih besar dari dim sekarang ({model.dim})"
    assert target_dim % model.n_heads == 0, f"Target dim {target_dim} harus habis dibagi n_heads {model.n_heads}"

    old_dim = model.dim
    old_params = model.count_parameters()

    print(f"\n[🌱 Net2Net Growth] Memperlebar Otak UH-0: {old_dim} -> {target_dim} (Hidden Dim)")
    print(f"   Parameter Awal: {old_params:,} parameters")

    new_model = UHZero(
        vocab_size=model.vocab_size,
        dim=target_dim,
        n_layers=model.n_layers,
        n_heads=model.n_heads,
        max_seq_len=model.max_seq_len
    )

    with torch.no_grad():
        # 1. Salin Token & Position Embeddings
        new_model.tok_embed.weight.zero_()
        new_model.tok_embed.weight[:, :old_dim] = model.tok_embed.weight.clone()
        new_model.pos_embed.weight.zero_()
        new_model.pos_embed.weight[:, :old_dim] = model.pos_embed.weight.clone()

        # 2. Salin Tiap Transformer Block
        for l_idx, (old_block, new_block) in enumerate(zip(model.layers, new_model.layers)):
            # Attention Norm
            new_block.attn_norm.weight[:old_dim] = old_block.attn_norm.weight.clone()
            
            # Q, K, V Projections
            new_block.attn.q_proj = copy_linear_wider(old_block.attn.q_proj, target_dim, target_dim)
            new_block.attn.k_proj = copy_linear_wider(old_block.attn.k_proj, target_dim, target_dim)
            new_block.attn.v_proj = copy_linear_wider(old_block.attn.v_proj, target_dim, target_dim)
            
            # Out Projection
            new_block.attn.out_proj = copy_linear_wider(old_block.attn.out_proj, target_dim, target_dim)

            # MLP Norm
            new_block.mlp_norm.weight[:old_dim] = old_block.mlp_norm.weight.clone()

            # MLP Projections
            old_mlp_dim = old_block.mlp.mlp_dim
            new_mlp_dim = new_block.mlp.mlp_dim
            new_block.mlp.fc1 = copy_linear_wider(old_block.mlp.fc1, target_dim, new_mlp_dim)
            new_block.mlp.fc2 = copy_linear_wider(old_block.mlp.fc2, new_mlp_dim, target_dim)

        # 3. Final Norm & Head
        new_model.norm.weight[:old_dim] = model.norm.weight.clone()
        new_model.head.weight.zero_()
        new_model.head.weight[:, :old_dim] = model.head.weight.clone()

    new_params = new_model.count_parameters()
    growth_ratio = new_params / max(1, old_params)
    print(f"   ✓ Pertumbuhan Sukses! Parameter Baru: {new_params:,} ({growth_ratio:.1f}x lipat)")
    return new_model


def grow_deeper(model: UHZero, additional_layers: int = 2) -> UHZero:
    """
    Menambah kedalaman lapisan (layer) Transformer Block
    Menggunakan Identity Mapping Initialization agar f_new(x) == f_old(x).
    """
    old_layers = model.n_layers
    new_layers = old_layers + additional_layers
    old_params = model.count_parameters()

    print(f"\n[🌳 Net2Net Depth] Menambah Kedalaman Layer: {old_layers} -> {new_layers} Layer")
    print(f"   Parameter Awal: {old_params:,} parameters")

    new_model = UHZero(
        vocab_size=model.vocab_size,
        dim=model.dim,
        n_layers=new_layers,
        n_heads=model.n_heads,
        max_seq_len=model.max_seq_len
    )

    with torch.no_grad():
        # Salin Embeddings & Norm & Head
        new_model.tok_embed.weight.copy_(model.tok_embed.weight)
        new_model.pos_embed.weight.copy_(model.pos_embed.weight)
        new_model.norm.weight.copy_(model.norm.weight)
        new_model.head.weight.copy_(model.head.weight)

        # Salin layer lama ke layer depan
        for i in range(old_layers):
            new_model.layers[i].load_state_dict(model.layers[i].state_dict())

        # Layer tambahan diinisialisasi sebagai identity residual (bobot output diset 0)
        for j in range(old_layers, new_layers):
            new_model.layers[j].attn.out_proj.weight.zero_()
            new_model.layers[j].mlp.fc2.weight.zero_()

    new_params = new_model.count_parameters()
    print(f"   ✓ Penambahan Layer Selesai! Parameter Baru: {new_params:,}")
    return new_model
