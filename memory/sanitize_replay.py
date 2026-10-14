#!/usr/bin/env python3
"""
Sanitizer script for UH-0 Replay Buffer.
Removes degenerate, repetitive, and junk tokens from memory/replay_buffer.jsonl.
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from world.executor import is_degenerate_code

BUFFER_FILE = BASE_DIR / "memory" / "replay_buffer.jsonl"


def sanitize():
    if not BUFFER_FILE.exists():
        print("[-] Replay buffer file not found.")
        return

    original_count = 0
    clean_items = []

    with open(BUFFER_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            original_count += 1
            try:
                item = json.loads(line)
                code_str = item.get("code", "")
                is_junk, reason = is_degenerate_code(code_str)
                if not is_junk:
                    clean_items.append(item)
            except Exception:
                pass

    # Backup original
    backup_file = BUFFER_FILE.with_suffix(".jsonl.bak")
    BUFFER_FILE.rename(backup_file)

    # Write clean items
    with open(BUFFER_FILE, "w", encoding="utf-8") as f:
        for item in clean_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"[✓] Sanitasi Selesai!")
    print(f"    Total Awal    : {original_count} entri")
    print(f"    Sampah Dibuang: {original_count - len(clean_items)} entri")
    print(f"    Bersih Tersisa: {len(clean_items)} entri")


if __name__ == "__main__":
    sanitize()
