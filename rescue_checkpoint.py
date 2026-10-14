import os
import io
import pickle
import zipfile
import torch
from pathlib import Path

print("[*] Memulai pemulihan bobot otak 30 Layer (Step #206.850)...")

# 1. Muat metadata
def fake_rebuild(storage, storage_offset, size, stride, requires_grad=False, backward_hooks=None):
    return (storage, size, stride)

import torch._utils
torch._utils._rebuild_tensor_v2 = fake_rebuild

class InspectionUnpickler(pickle.Unpickler):
    def persistent_load(self, pid):
        return pid

with zipfile.ZipFile('/root/uh-zero/reconstructed_checkpoint.pt') as z:
    pkl_bytes = z.read('uh_zero_v2_checkpoint/data.pkl')
    unpickler = InspectionUnpickler(io.BytesIO(pkl_bytes))
    meta = unpickler.load()

# Model state dict mapping
sd_meta = meta['model_state_dict']

# Baca semua data chunks yang berhasil diselamatkan (0 sampai 321)
extracted_chunks = {}
with zipfile.ZipFile('/root/uh-zero/reconstructed_checkpoint.pt') as z:
    for i in range(322):
        extracted_chunks[str(i)] = z.read(f'uh_zero_v2_checkpoint/data/{i}')

print(f"[✓] Berhasil memulihkan {len(extracted_chunks)} tensor bobot asli (Layer 0 s/d 26 awal)!")

