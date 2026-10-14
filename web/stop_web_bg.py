#!/usr/bin/env python3
"""
Stopper latar belakang aman untuk UH-0 Web Observatory.
Menghentikan HANYA proses web berdasarkan PID file web.pid (Anti generic pkill).
"""

import os
import sys
import time
import signal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PID_FILE = BASE_DIR / "web.pid"


def stop_web():
    if not PID_FILE.exists():
        print("[-] File web.pid tidak ditemukan. Layanan web tampaknya tidak sedang berjalan.")
        return

    try:
        pid = int(PID_FILE.read_text().strip())
    except Exception as e:
        print(f"[!] Gagal membaca PID: {e}")
        PID_FILE.unlink(missing_ok=True)
        return

    print(f"[*] Menghentikan UH-0 Web Observatory (PID: {pid})...")
    try:
        os.kill(pid, signal.SIGTERM)
        for _ in range(10):
            time.sleep(0.3)
            try:
                os.kill(pid, 0)
            except (OSError, ProcessLookupError):
                break
        else:
            os.kill(pid, signal.SIGKILL)

        PID_FILE.unlink(missing_ok=True)
        print(f"✅ UH-0 Web Observatory (PID: {pid}) berhasil dihentikan dengan aman.")
    except (OSError, ProcessLookupError):
        PID_FILE.unlink(missing_ok=True)
        print(f"[-] Proses dengan PID {pid} sudah tidak aktif.")


if __name__ == "__main__":
    stop_web()
