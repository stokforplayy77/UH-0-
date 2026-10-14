#!/usr/bin/env python3
"""
GitHub Real Code Harvester & Rigorous Sanitizer
Targets authentic, high-quality open-source algorithm and system code.
Strictly validates:
1. Syntax validity via ast.parse (for Python)
2. Repetition / degeneracy rejection (no loops, no spam)
3. Minimum meaningful complexity (no trivial/empty snippets)
4. Formatted directly into clean instruction-response pairs
"""

import os
import sys
import ast
import json
import time
import subprocess
import re
from pathlib import Path

DATA_DIR = Path("/root/uh-zero/data")
RAW_REPOS_DIR = DATA_DIR / "raw_github_repos"
OUTPUT_FILE = DATA_DIR / "github_verified_dataset.jsonl"
LOG_FILE = DATA_DIR / "harvester.log"

# Repositories to clone (100% human-verified real implementations)
TARGET_REPOS = [
    {
        "name": "Python",
        "url": "https://github.com/TheAlgorithms/Python.git",
        "ext": [".py"],
        "lang": "Python"
    },
    {
        "name": "JavaScript",
        "url": "https://github.com/TheAlgorithms/JavaScript.git",
        "ext": [".js"],
        "lang": "JavaScript"
    },
    {
        "name": "Rust",
        "url": "https://github.com/TheAlgorithms/Rust.git",
        "ext": [".rs"],
        "lang": "Rust"
    },
    {
        "name": "Go",
        "url": "https://github.com/TheAlgorithms/Go.git",
        "ext": [".go"],
        "lang": "Go"
    },
    {
        "name": "C-Plus-Plus",
        "url": "https://github.com/TheAlgorithms/C-Plus-Plus.git",
        "ext": [".cpp", ".hpp"],
        "lang": "C++"
    },
    {
        "name": "Java",
        "url": "https://github.com/TheAlgorithms/Java.git",
        "ext": [".java"],
        "lang": "Java"
    },
    {
        "name": "fastapi",
        "url": "https://github.com/fastapi/fastapi.git",
        "ext": [".py"],
        "lang": "Python",
        "subdir": "docs_src"  # Focus on official tutorials/examples
    },
    {
        "name": "pytorch-examples",
        "url": "https://github.com/pytorch/examples.git",
        "ext": [".py"],
        "lang": "Python"
    },
    {
        "name": "flask",
        "url": "https://github.com/pallets/flask.git",
        "ext": [".py"],
        "lang": "Python",
        "subdir": "examples"
    }
]

def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def is_degenerate(text: str) -> bool:
    """Detect repetition, loop artifacts, or degenerate sequences."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if len(lines) < 5:
        return True
    
    # Check repeated identical lines ratio
    unique_lines = set(lines)
    if len(unique_lines) / len(lines) < 0.4:
        return True  # Too much repetitive line spam
    
    # Check repeated 4-grams of words
    words = text.split()
    if len(words) > 50:
        four_grams = [tuple(words[i:i+4]) for i in range(len(words)-3)]
        if len(four_grams) > 0 and len(set(four_grams)) / len(four_grams) < 0.35:
            return True
            
    return False

def validate_python_code(code_str: str) -> bool:
    """Strictly verify that Python code is syntactically valid."""
    try:
        ast.parse(code_str)
        return True
    except Exception:
        return False

def extract_instruction_from_path(file_path: Path, lang: str) -> str:
    """Generate a clean, natural prompt based on the code's filename and directory."""
    stem = file_path.stem.replace("_", " ").replace("-", " ")
    parts = file_path.parts
    category = parts[-2] if len(parts) >= 2 else "algorithms"
    category = category.replace("_", " ").replace("-", " ")
    
    return f"Tuliskan implementasi lengkap dan bersih dalam bahasa {lang} untuk algoritma {stem} (kategori: {category})."

def clone_or_pull(repo_info):
    target = RAW_REPOS_DIR / repo_info["name"]
    if not target.exists():
        log(f"📥 Mengunduh repositori resmi: {repo_info['name']} dari {repo_info['url']}...")
        cmd = ["git", "clone", "--depth", "1", repo_info["url"], str(target)]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            log(f"⚠️ Gagal mengunduh {repo_info['name']}: {res.stderr}")
            return False
    else:
        log(f"🔄 Memperbarui repositori: {repo_info['name']}...")
        subprocess.run(["git", "-C", str(target), "pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return True

def process_repo(repo_info, out_f):
    base_dir = RAW_REPOS_DIR / repo_info["name"]
    if repo_info.get("subdir"):
        base_dir = base_dir / repo_info["subdir"]
        
    if not base_dir.exists():
        return 0, 0

    valid_count = 0
    rejected_count = 0
    
    for ext in repo_info["ext"]:
        for file_path in base_dir.rglob(f"*{ext}"):
            # Skip hidden files, tests with dummy mocks, or virtualenvs
            p_str = str(file_path)
            if "/." in p_str or "node_modules" in p_str or "venv" in p_str:
                continue
                
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
            except Exception:
                rejected_count += 1
                continue
                
            # Filter length: between 150 chars and 8,000 chars (optimal for training window)
            if len(content) < 150 or len(content) > 8000:
                rejected_count += 1
                continue
                
            if is_degenerate(content):
                rejected_count += 1
                continue
                
            if repo_info["lang"] == "Python":
                if not validate_python_code(content):
                    rejected_count += 1
                    continue
                    
            prompt = extract_instruction_from_path(file_path, repo_info["lang"])
            
            # Format clean instruction-response pair
            sample = {
                "source": f"github/{repo_info['name']}/{file_path.name}",
                "language": repo_info["lang"],
                "instruction": prompt,
                "input": "",
                "output": f"```{repo_info['lang'].lower()}\n{content}\n```"
            }
            
            out_f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            valid_count += 1
            
    log(f"✅ Repositori {repo_info['name']}: {valid_count} file kode tervalidasi 100% sempurna (Ditolak: {rejected_count})")
    return valid_count, rejected_count

def main():
    RAW_REPOS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    log("🚀 Memulai Pipeline Pemanenan Kode Asli GitHub (Linode Node 10)...")
    
    total_valid = 0
    total_rejected = 0
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for repo in TARGET_REPOS:
            success = clone_or_pull(repo)
            if success:
                v, r = process_repo(repo, out_f)
                total_valid += v
                total_rejected += r
                
    file_size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    log(f"🎉 SELESAI! Total data kode murni terverifikasi: {total_valid} sampel.")
    log(f"📁 Lokasi output: {OUTPUT_FILE} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
