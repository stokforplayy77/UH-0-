# SOP & Playbook Deployment GPU Cloud (Vast.ai / Lambda / RunPod)
**Dokumen Standar Kolaborasi Dual-Agent: Aruna AI (Agent 1) & Adara AI (Agent 2)**
**Terakhir Diperbarui:** 12 Oktober 2026 (Adara AI)

---

## 📌 Ringkasan Arsitektur
* **Pola Desain:** *Stateless Ephemeral High-Compute (GPU Cloud)* $\leftrightarrow$ *Persistent Storage & Observatory (Node 10 / Termux)*.
* **Tujuan:** Melatih arsitektur neural UH-0 (30 Layers, 583.5M Parameter) menggunakan GPU kelas industri (NVIDIA RTX 4090 24GB / A100 / H100) dengan kecepatan 60+ tasks/detik (~70x lebih cepat dibanding CPU).
* **Prinsip Utama:** GPU disewa sementara (ephemeral), seluruh checkpoint dan memori disinkronkan otomatis kembali ke Node 10 (`139.162.21.81`) dan master code tersimpan di Termux.

---

## 🚀 Langkah Demi Langkah (Step-by-Step Deployment)

### 1. Dapatkan Kredensial SSH dari Dashboard Provider
Saat instance GPU aktif (misal di Vast.ai), catat host dan port SSH-nya:
* Contoh: `ssh -p 12485 root@ssh4.vast.ai -L 8080:localhost:8080`
* Format: Host: `ssh4.vast.ai`, Port: `12485`, User: `root`.

---

### 2. Kirim Kode & Model dari Node 10 ke Instance GPU
Jalankan dari **Node 10 (`139.162.21.81`)** atau dari Termux:
```bash
# 1. Pastikan folder tujuan ada di GPU
ssh -o StrictHostKeyChecking=no -p <PORT> root@<HOST> "mkdir -p /workspace/uh-zero"

# 2. Sinkronkan seluruh modul proyek (exclude cache & venv)
rsync -avz -e "ssh -p <PORT>" \
  --exclude="venv" \
  --exclude="__pycache__" \
  --exclude="*.tmp" \
  /root/uh-zero/ root@<HOST>:/workspace/uh-zero/
```

---

### 3. Verifikasi Environment Python & Compiler Biner di GPU
Masuk via SSH ke instance GPU:
```bash
ssh -p <PORT> root@<HOST>
```

Jalankan pengecekan PyTorch dan GPU:
```bash
# Vast.ai biasanya menyediakan venv bawaan di /venv/main/bin/python
PYTHON_BIN="/venv/main/bin/python"
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

# Cek ketersediaan CUDA dan VRAM
$PYTHON_BIN -c "import torch; print('CUDA Ready:', torch.cuda.is_available(), '| Device:', torch.cuda.get_device_name(0), '| VRAM GB:', torch.cuda.get_device_properties(0).total_memory / (1024**3))"

# Pasang kompilator biner inti jika belum ada
apt update && apt install -y build-essential nodejs golang lua5.3 sqlite3
```

---

### 4. Eksekusi Training GPU Turbo Asinkron
Jalankan proses pelatihan di latar belakang menggunakan `train_gpu_turbo.py`:
```bash
cd /workspace/uh-zero

# Konfigurasi optimal RTX 4090 (24GB VRAM):
# --batch-size 12 : Mengisi VRAM ~17-21 GB, saturasi GPU 85%-99%, daya ~320-360W
nohup /venv/main/bin/python -u train_gpu_turbo.py --batch-size 12 > train_gpu.log 2>&1 &
echo $! > bot.pid

echo "✅ GPU Turbo Trainer Aktif! PID: $(cat bot.pid)"
```

---

### 5. Aktifkan Pipeline Sinkronisasi Otomatis di Node 10
Kembali ke **Node 10 (`139.162.21.81`)**, buat atau jalankan loop auto-sync (`/root/uh-zero/sync_vast_loop.sh`):

```bash
#!/bin/bash
# sync_vast_loop.sh (Jalankan di Node 10)
VAST_HOST="ssh4.vast.ai"
VAST_PORT="12485"

while true; do
    # 1. Tarik log pelatihan & update status flag (tiap 10 detik)
    rsync -az -e "ssh -o ConnectTimeout=5 -p $VAST_PORT" root@$VAST_HOST:/workspace/uh-zero/train_gpu.log /root/uh-zero/train.log 2>/dev/null
    touch /root/uh-zero/gpu_active.flag

    # 2. Tarik replay buffer memori valid (tiap 10 detik)
    rsync -az -e "ssh -o ConnectTimeout=5 -p $VAST_PORT" root@$VAST_HOST:/workspace/uh-zero/memory/replay_buffer.jsonl /root/uh-zero/memory/replay_buffer.jsonl 2>/dev/null

    # 3. Tarik checkpoint model terbaru (tiap ~3 menit)
    if [ $((SECONDS % 180)) -lt 15 ]; then
        rsync -az -e "ssh -o ConnectTimeout=5 -p $VAST_PORT" root@$VAST_HOST:/workspace/uh-zero/uh_zero_v2_checkpoint.pt /root/uh-zero/uh_zero_v2_checkpoint.pt 2>/dev/null
    fi

    sleep 10
done
```

Jalankan di background Node 10:
```bash
nohup bash /root/uh-zero/sync_vast_loop.sh > /root/uh-zero/sync_vast.log 2>&1 &
```

---

### 6. Pengawasan Telemetri & Observatorium Web
* **Live Web Dashboard:** Buka [https://uhlabs.id/zero/](https://uhlabs.id/zero/)
  * Status: `TRAINING AKTIF (PID: GPU-Turbo)`
  * Step, Loss Graph, Total Solusi Terverifikasi, dan Feed Solusi otomatis berdetak tiap beberapa detik.
* **Perintah CLI Cepat:**
  ```bash
  # Cek utilitas GPU dari Termux / Node 10
  ssh -p <PORT> root@<HOST> "nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw,temperature.gpu --format=csv"

  # Cek baris log terbaru
  ssh -p <PORT> root@<HOST> "tail -n 10 /workspace/uh-zero/train_gpu.log"
  ```

---

### 7. SOP Sanitasi & Anti-Degenerasi (*Reward Hacking Defense*)
Jika terdeteksi output repetitif simbol abnormal (seperti repetisi `$`, spasi, atau tanda baca beruntun):
1. **Jalankan pembersih otomatis:**
   ```bash
   ssh -p <PORT> root@<HOST> "cd /workspace/uh-zero && /venv/main/bin/python memory/sanitize_replay.py"
   ssh root@139.162.21.81 "cd /root/uh-zero && /root/uh-zero/venv/bin/python3 memory/sanitize_replay.py"
   ```
2. Validator leksikal `is_degenerate_code()` di `world/executor.py` akan otomatis menolak input tersebut dengan penalti `-0.6` dan membatalkan penyimpanannya ke memori.

---

### 8. SOP Mengakhiri Sewa GPU (Decommission / Cleanup)
Sebelum mematikan instance GPU di provider:
1. Pastikan checkpoint model termutakhir sudah tersinkron ke Node 10:
   ```bash
   scp -P <PORT> root@<HOST>:/workspace/uh-zero/uh_zero_v2_checkpoint.pt /root/uh-zero/uh_zero_v2_checkpoint.pt
   ```
2. Hapus flag GPU di Node 10:
   ```bash
   rm -f /root/uh-zero/gpu_active.flag
   pkill -f "sync_vast_loop.sh"
   ```
3. Tekan **Stop / Destroy Instance** di web provider GPU untuk menghentikan billing sewa.
4. Model di Node 10 dapat langsung melanjutkan serving di `uhlabs.id/zero` secara mandiri.
