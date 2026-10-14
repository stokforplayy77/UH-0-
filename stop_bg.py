#!/usr/bin/env python3
"""
Penghenti proses latar belakang (Background Stopper) untuk UH-0 (Adara AI Zero)
Menghentikan proses hanya berdasarkan file PID tanpa perintah pematian generik.
"""

import os
import sys
import signal
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PID_FILE = BASE_DIR / "uh_zero.pid"


def stop():
    if not PID_FILE.exists():
        print("[-] File uh_zero.pid tidak ditemukan. UH-0 tidak sedang berjalan.")
        return

    try:
        pid = int(PID_FILE.read_text().strip())
    except ValueError:
        print("[-] PID file corrupt. Menghapus uh_zero.pid...")
        PID_FILE.unlink(missing_ok=True)
        return

    try:
        os.kill(pid, 0)
    except OSError:
        print(f"[-] Proses dengan PID {pid} sudah tidak aktif.")
        PID_FILE.unlink(missing_ok=True)
        return

    print(f"[*] Menghentikan proses UH-0 (PID: {pid})...")
    try:
        os.kill(pid, signal.SIGTERM)
        for _ in range(10):
            time.sleep(0.5)
            try:
                os.kill(pid, 0)
            except OSError:
                break
        else:
            os.kill(pid, signal.SIGKILL)
        print(f"✓ Proses UH-0 (PID: {pid}) berhasil dihentikan.")
    except Exception as e:
        print(f"[-] Gagal menghentikan proses: {e}")
    finally:
        PID_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    stop()
