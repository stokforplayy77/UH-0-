import os
import io
import pickle
import zipfile
import torch
import numpy as np
from pathlib import Path

BASE_DIR = Path("/root/uh-zero")

# Inisialisasi arsitektur dasar Qwen Coder
from brain.model_qwen import AdaraEvolvingModel

adara = AdaraEvolvingModel(device="cpu")
# Tumbuhkan ke 30 layer penuh (tambah 6 layer)
adara.grow_deeper(additional_layers=6)
print(f"✓ Arsitektur 30 Layer diinisialisasi: {adara.count_parameters():,} parameter ({adara.num_layers()} layers)")

# Muat metadata
def fake_rebuild(storage, storage_offset, size, stride, requires_grad=False, backward_hooks=None):
    return (storage, size, stride)

import torch._utils
orig_rebuild = torch._utils._rebuild_tensor_v2
torch._utils._rebuild_tensor_v2 = fake_rebuild

class InspectionUnpickler(pickle.Unpickler):
    def persistent_load(self, pid):
        return pid

with zipfile.ZipFile(BASE_DIR / 'reconstructed_checkpoint.pt') as z:
    pkl_bytes = z.read('uh_zero_v2_checkpoint/data.pkl')
    unpickler = InspectionUnpickler(io.BytesIO(pkl_bytes))
    meta = unpickler.load()

torch._utils._rebuild_tensor_v2 = orig_rebuild

sd_meta = meta['model_state_dict']

# Ekstrak semua binary chunk 0 s/d 321
chunks = {}
with zipfile.ZipFile(BASE_DIR / 'reconstructed_checkpoint.pt') as z:
    for i in range(322):
        chunks[str(i)] = z.read(f'uh_zero_v2_checkpoint/data/{i}')

print(f"✓ Berhasil mengekstrak {len(chunks)} raw binary storage weights!")

# Mapping state dict model yang ada saat ini
model_sd = adara.model.state_dict()
recovered_count = 0

for param_name, meta_val in sd_meta.items():
    if param_name not in model_sd:
        continue
    storage_tuple = meta_val[0]
    storage_key = str(storage_tuple[2])
    size = meta_val[1]
    
    if storage_key in chunks:
        raw_b = chunks[storage_key]
        # Buat tensor bfloat16
        t = torch.frombuffer(bytearray(raw_b), dtype=torch.bfloat16).reshape(size).clone()
        model_sd[param_name].copy_(t)
        recovered_count += 1

print(f"🎉 SUKSES BESAR! Berhasil memulihkan {recovered_count}/{len(model_sd)} bobot transformer terlatih!")

# Simpan checkpoint utuh baru 30 layer Step #206850
step = meta.get("step", 206850)
level = meta.get("level", 4)
loss = meta.get("loss", 0.392)

save_path = BASE_DIR / "uh_zero_30layers_recovered.pt"
save_data = {
    "step": step,
    "level": level,
    "loss": loss,
    "num_layers": adara.num_layers(),
    "num_parameters": adara.count_parameters(),
    "model_state_dict": adara.model.state_dict(),
    "config": adara.model.config.to_dict()
}
torch.save(save_data, save_path)
print(f"💾 Checkpoint 30 Layer berhasil disimpan ke {save_path} ({save_path.stat().st_size / (1024*1024):.1f} MB)!")

# Salin juga ke link statis web
ln_cmd = f"cp {save_path} {BASE_DIR}/uh_zero_v2_checkpoint.pt && cp {save_path} {BASE_DIR}/web/static/uh_zero_v2_checkpoint.pt"
os.system(ln_cmd)
print("✓ Checkpoint aktif di Node 10 telah diperbarui!")

