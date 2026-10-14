#!/usr/bin/env python3
"""
Launcher latar belakang (Background Daemon) untuk UH-0 (Adara AI Zero)
Menyimpan PID ke uh_zero.pid dan log ke train.log secara aman.
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PID_FILE = BASE_DIR / "uh_zero.pid"
LOG_FILE = BASE_DIR / "train.log"


def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def start():
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if is_running(pid):
                print(f"[!] UH-0 sudah berjalan di latar belakang dengan PID: {pid}")
                return
        except ValueError:
            pass

    # Tentukan interpreter python (gunakan venv jika ada)
    venv_python = Path("/root/adara-ai/venv/bin/python3")
    py_exec = str(venv_python) if venv_python.exists() else sys.executable

    train_script = BASE_DIR / "train.py"
    log_fp = open(LOG_FILE, "a", encoding="utf-8")

    cmd = [py_exec, str(train_script), "--steps", "0", "--grow_at", "150"]
    proc = subprocess.Popen(
        cmd,
        cwd=str(BASE_DIR),
        stdout=log_fp,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setpgrp
    )

    PID_FILE.write_text(str(proc.pid))
    print(f"✓ UH-0 (Adara AI Zero) berhasil dijalankan di latar belakang!")
    print(f"  PID     : {proc.pid}")
    print(f"  Log File: {LOG_FILE}")
    print(f"  Perintah Pantau: tail -f {LOG_FILE}")


if __name__ == "__main__":
    start()
