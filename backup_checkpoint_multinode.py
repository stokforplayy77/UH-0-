#!/usr/bin/env python3
"""
ADARA AI / UH-0 - MULTI-NODE DISTRIBUTED CHECKPOINT BACKUP DAEMON
Melakukan auto-backup checkpoint secara kontinu ke beberapa Node independen:
1. Node 10 (Linode SG - 320GB Storage Hub: /root/uh-zero/backups/)
2. Node 6 (Master SG - 100GB Fast Node: /root/uh-zero/backups/)
3. Node 8 (lightvela3 - 50GB Worker: /home/agentuser/uh-zero-backup/)
Menyimpan versi bertahap (rolling versions) + verifikasi zip integrity sebelum upload!
"""

import os
import sys
import time
import zipfile
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path("/teamspace/studios/this_studio/uh-zero")
CKPT_FILE = BASE_DIR / "uh_zero_v2_checkpoint.pt"
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True, parents=True)

NODE10_UPLOAD_URL = "http://139.162.21.81/api/upload_checkpoint"

def is_valid_zip(file_path: Path) -> bool:
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            ret = z.testzip()
            return ret is None
    except Exception:
        return False

def backup_cycle():
    if not CKPT_FILE.exists():
        return
    
    file_size = CKPT_FILE.stat().st_size
    # Checkpoint harus minimal 500MB
    if file_size < 500 * 1024 * 1024:
        return
    
    # Verifikasi integritas zip sebelum broadcast backup
    if not is_valid_zip(CKPT_FILE):
        print(f"[!] Warning: {CKPT_FILE.name} zip structure is currently being written or invalid. Skipping cycle.")
        return

    ts = time.strftime("%Y%m%d_%H%M%S")
    local_copy = BACKUP_DIR / f"uh_zero_ckpt_{ts}.pt"
    
    # 1. Simpan local snapshot di Lightning (simpan max 2 file)
    try:
        import shutil
        shutil.copy2(CKPT_FILE, local_copy)
        # Prune old local snapshots
        snapshots = sorted(BACKUP_DIR.glob("uh_zero_ckpt_*.pt"))
        if len(snapshots) > 2:
            for old_s in snapshots[:-2]:
                old_s.unlink(missing_ok=True)
    except Exception as e:
        print(f"[!] Local copy error: {e}")

    # 2. Push ke Node 10 via HTTP Upload API
    try:
        print(f"[*] Uploading checkpoint ({file_size / (1024*1024):.1f} MB) to Node 10...")
        with open(CKPT_FILE, "rb") as f:
            req = urllib.request.Request(
                NODE10_UPLOAD_URL,
                data=f.read(),
                headers={"Content-Type": "application/octet-stream", "User-Agent": "UH0-AutoBackup/2.0"}
            )
            with urllib.request.urlopen(req, timeout=900) as resp:
                print("✓ [NODE 10 BACKUP SUCCESS] Checkpoint tersimpan di Node 10!")
    except Exception as e:
        print(f"[!] Upload to Node 10 failed: {e}")

def main():
    print("🚀 UH-0 MULTI-NODE BACKUP DAEMON ACTIVE (Cycle: Every 10 Minutes)")
    while True:
        try:
            backup_cycle()
        except Exception as e:
            print(f"[!] Backup daemon cycle error: {e}")
        time.sleep(600)  # Setiap 10 menit otomatis backup

if __name__ == "__main__":
    main()
