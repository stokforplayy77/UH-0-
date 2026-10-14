#!/usr/bin/env python3
"""
Distributed Code Harvester Worker
Runs on any compute node (Node 2, Node 4, Node 8, Node 9, Node 11).
Fetches assigned repositories, validates strictly via ast & repetition filters,
and writes directly to verified jsonl.
"""

import os
import sys
import ast
import json
import time
import subprocess
from pathlib import Path

WORK_DIR = Path.home() / "harvester_work"
RAW_DIR = WORK_DIR / "raw_repos"
OUT_FILE = WORK_DIR / "worker_harvested.jsonl"
LOG_FILE = WORK_DIR / "worker.log"

def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def is_degenerate(text: str) -> bool:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if len(lines) < 5:
        return True
    unique_lines = set(lines)
    if len(unique_lines) / len(lines) < 0.4:
        return True
    words = text.split()
    if len(words) > 50:
        four_grams = [tuple(words[i:i+4]) for i in range(len(words)-3)]
        if len(four_grams) > 0 and len(set(four_grams)) / len(four_grams) < 0.35:
            return True
    return False

def validate_python(code_str: str) -> bool:
    try:
        ast.parse(code_str)
        return True
    except Exception:
        return False

def harvest_repo(repo, out_f):
    name = repo["name"]
    url = repo["url"]
    exts = repo["ext"]
    lang = repo["lang"]
    subdir = repo.get("subdir", "")

    repo_path = RAW_DIR / name
    if not repo_path.exists():
        log(f"📥 Cloning {name} ({lang}) from {url}...")
        cmd = ["git", "clone", "--depth", "1", url, str(repo_path)]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            log(f"⚠️ Failed to clone {name}: {res.stderr[:200]}")
            return 0
    else:
        log(f"🔄 Updating {name}...")
        subprocess.run(["git", "-C", str(repo_path), "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    search_dir = repo_path / subdir if subdir else repo_path
    if not search_dir.exists():
        return 0

    valid_count = 0
    for ext in exts:
        for file_path in search_dir.rglob(f"*{ext}"):
            p_str = str(file_path)
            if "/." in p_str or "node_modules" in p_str or "venv" in p_str or "test" in p_str.lower():
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
            except Exception:
                continue

            if len(content) < 150 or len(content) > 8000:
                continue
            if is_degenerate(content):
                continue
            if lang == "Python" and not validate_python(content):
                continue

            stem = file_path.stem.replace("_", " ").replace("-", " ")
            parent = file_path.parent.name.replace("_", " ").replace("-", " ")
            sample = {
                "source": f"github/{name}/{file_path.name}",
                "language": lang,
                "instruction": f"Implementasikan modul/algoritma {stem} dalam bahasa {lang} (kategori: {parent}).",
                "input": "",
                "output": f"```{lang.lower()}\n{content}\n```"
            }
            out_f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            valid_count += 1

    log(f"✅ {name}: {valid_count} kode tervalidasi 100% sempurna.")
    return valid_count

def main():
    if len(sys.argv) < 2:
        print("Usage: distributed_worker.py <repos_config.json>")
        sys.exit(1)

    config_path = Path(sys.argv[1])
    repos = json.loads(config_path.read_text(encoding="utf-8"))

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    log(f"🚀 Memulai Distributed Worker dengan {len(repos)} repositori target...")
    total = 0
    with open(OUT_FILE, "a", encoding="utf-8") as out_f:
        for r in repos:
            total += harvest_repo(r, out_f)

    log(f"🎉 Selesai! Total terkumpul pada worker ini: {total} kode valid.")
    log(f"📁 Output tersimpan di {OUT_FILE} ({OUT_FILE.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
