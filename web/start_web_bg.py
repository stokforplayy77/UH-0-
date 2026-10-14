#!/usr/bin/env python3
"""
Launcher latar belakang aman untuk UH-0 Web Observatory.
Menggunakan PID file web.pid (Anti generic pkill).
"""

import os
import sys
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PID_FILE = BASE_DIR / "web.pid"
LOG_FILE = BASE_DIR / "web.log"


def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def start_web(port: int = 8099):
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if is_running(pid):
                print(f"[!] UH-0 Web Observatory sudah aktif berjalan dengan PID: {pid}")
                return
            else:
                PID_FILE.unlink(missing_ok=True)
        except Exception:
            PID_FILE.unlink(missing_ok=True)

    cmd = [
        sys.executable,
        str(BASE_DIR / "web" / "server.py"),
        "--port", str(port),
        "--host", "0.0.0.0"
    ]

    with open(LOG_FILE, "a") as log_out:
        proc = subprocess.Popen(
            cmd,
            cwd=str(BASE_DIR),
            stdout=log_out,
            stderr=subprocess.STDOUT,
            start_new_session=True
        )

    PID_FILE.write_text(str(proc.pid))
    time.sleep(1)

    if is_running(proc.pid):
        print(f"=========================================================")
        print(f"✅ UH-0 Web Observatory BERHASIL DINYALAKAN!")
        print(f"   PID        : {proc.pid}")
        print(f"   Port       : {port}")
        print(f"   Log File   : {LOG_FILE}")
        print(f"=========================================================")
    else:
        print(f"❌ Gagal menyalakan UH-0 Web Observatory. Periksa {LOG_FILE}")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8099
    start_web(port)
