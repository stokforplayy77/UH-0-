#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - Web Observatory & Multi-Language Code Dashboard
Provides real-time telemetry, Net2Net growth monitoring, 80 programming languages matrix,
sandbox code verification, and interactive inference playground.
"""

import os
import sys
import json
import time
import subprocess
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

try:
    from brain.languages import LANGUAGES_CATALOG, get_categories, get_all_languages
except ImportError:
    LANGUAGES_CATALOG = {}
    def get_categories(): return {}
    def get_all_languages(): return []

try:
    from world.executor import is_degenerate_code
except ImportError:
    def is_degenerate_code(code: str): return False, "OK"

PID_FILE = BASE_DIR / "uh_zero.pid"
WEB_PID_FILE = BASE_DIR / "web.pid"
LOG_FILE = BASE_DIR / "train.log"
REPLAY_FILE = BASE_DIR / "memory" / "replay_buffer.jsonl"
SKILL_DIR = BASE_DIR / "memory" / "skill_library"

# Cache for inference model to avoid reloading each request
_cached_model = None
_cached_device = None


def is_training_active() -> bool:
    # 0. Cek GPU training active flag
    gpu_flag = BASE_DIR / "gpu_active.flag"
    if gpu_flag.exists():
        try:
            if (time.time() - gpu_flag.stat().st_mtime) < 180:
                return True
        except Exception:
            pass

    # 1. Cek status systemd service
    try:
        res = subprocess.run(["systemctl", "is-active", "uh-zero-trainer.service"], capture_output=True, text=True, timeout=1)
        if res.returncode == 0 and res.stdout.strip() == "active":
            return True
    except Exception:
        pass

    # 2. Cek PID file
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)
            return True
        except (ValueError, OSError):
            pass
    return False


def get_telemetry_status():
    training = is_training_active()
    training_pid = "GPU-Turbo" if (BASE_DIR / "gpu_active.flag").exists() else None
    if training and not training_pid:
        try:
            res = subprocess.run(["systemctl", "show", "--property", "MainPID", "--value", "uh-zero-trainer.service"], capture_output=True, text=True, timeout=1)
            if res.returncode == 0 and res.stdout.strip().isdigit() and int(res.stdout.strip()) > 0:
                training_pid = int(res.stdout.strip())
        except Exception:
            pass

        if not training_pid and PID_FILE.exists():
            try:
                training_pid = int(PID_FILE.read_text().strip())
            except Exception:
                pass

    # Read latest lines from train.log for steps and loss
    latest_step = 0
    latest_loss = 0.0
    latest_level = 4
    total_params = 583507072
    hidden_dim = 128
    loss_history = []
    param_history = [{"step": 0, "params": 592640, "event": "Genesis (Bayi)"}]

    if LOG_FILE.exists():
        try:
            lines = LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
            for line in lines[-300:]:
                if "Step" in line and ("Params:" in line or "Lvl" in line or "Level" in line):
                    # e.g.: --- [Step 0025 | Level 1 | Params: 592,640] ---
                    # or:   --- [Step 43100 | Lvl 4 | VRAM: 3.6GB | Rate: 28.5 tasks/s] ---
                    parts = line.split("|")
                    for p in parts:
                        p_str = p.strip()
                        if "Step" in p_str:
                            try:
                                latest_step = int(p_str.replace("Step", "").replace("--- [", "").strip())
                            except Exception:
                                pass
                        elif "Level" in p_str or "Lvl" in p_str:
                            try:
                                latest_level = int(p_str.replace("Level", "").replace("Lvl", "").strip())
                            except Exception:
                                pass
                        elif "Params:" in p_str:
                            try:
                                total_params = int(p_str.replace("Params:", "").replace("]", "").replace("---", "").replace(",", "").strip())
                            except Exception:
                                pass
                    if latest_level == 4:
                        total_params = 583507072
                if "Loss:" in line:
                    try:
                        loss_val = float(line.split("Loss:")[-1].replace(")", "").strip())
                        latest_loss = loss_val
                        loss_history.append({"step": latest_step, "loss": loss_val})
                    except Exception:
                        pass
                if "Pertumbuhan Sukses!" in line and "Parameter Baru:" in line:
                    try:
                        new_p = int(line.split("Parameter Baru:")[-1].split()[0].replace(",", "").strip())
                        param_history.append({"step": latest_step, "params": new_p, "event": "Net2Net Wider Growth"})
                    except Exception:
                        pass
        except Exception as e:
            pass

    # Baca step dari checkpoint uh_zero_v2_checkpoint.pt (untuk sinkronisasi real-time dari Google Colab)
    v2_ckpt = BASE_DIR / "uh_zero_v2_checkpoint.pt"
    if v2_ckpt.exists():
        try:
            import torch
            ckpt_meta = torch.load(v2_ckpt, map_location="cpu")
            ckpt_step = ckpt_meta.get("step", 0)
            ckpt_loss = ckpt_meta.get("loss", 0.0)
            if ckpt_step > latest_step:
                latest_step = ckpt_step
                latest_loss = ckpt_loss
                training = True
                training_pid = "Colab-GPU-T4"
        except Exception:
            pass

    # List trained skills in library
    skills = []
    if SKILL_DIR.exists():
        for f in SKILL_DIR.glob("*.pt"):
            skills.append({"name": f.name, "size_kb": round(f.stat().st_size / 1024, 2)})

    # Count verified clean replay buffer (filter out degenerate/junk)
    replay_count = 0
    if REPLAY_FILE.exists():
        try:
            with open(REPLAY_FILE, "r", encoding="utf-8") as rf:
                for line in rf:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        is_j, _ = is_degenerate_code(obj.get("code", ""))
                        if not is_j:
                            replay_count += 1
                    except Exception:
                        pass
        except Exception:
            pass

    return {
        "status": "online",
        "training_active": training,
        "training_pid": training_pid,
        "latest_step": latest_step,
        "latest_loss": round(latest_loss, 4),
        "latest_level": latest_level,
        "total_parameters": total_params,
        "hidden_dim": hidden_dim,
        "languages_count": len(LANGUAGES_CATALOG),
        "replay_buffer_count": replay_count,
        "skills_count": len(skills),
        "skills": skills,
        "loss_history": loss_history[-30:],
        "param_history": param_history,
        "system_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def execute_inference(prompt_text: str, language: str = "python", max_new_tokens: int = 120):
    """Run generation using Adara AI UH-0 v2 Qwen Evolving Model with sandbox evaluation."""
    global _cached_model, _cached_device, _model_type
    try:
        import torch
        from world.executor import CodeExecutor

        device = "cuda" if torch.cuda.is_available() else "cpu"
        v2_ckpt = BASE_DIR / "uh_zero_v2_checkpoint.pt"

        if _cached_model is None:
            try:
                from brain.model_qwen import AdaraEvolvingModel
                adara = AdaraEvolvingModel(device=device)
                if v2_ckpt.exists():
                    adara.load_checkpoint(v2_ckpt)
                _cached_model = adara
                _cached_device = device
                _model_type = "qwen"
            except Exception as e:
                from brain.model import UHZero, ByteTokenizer
                ckpt_path = BASE_DIR / "uh_zero_checkpoint.pt"
                if ckpt_path.exists():
                    data = torch.load(ckpt_path, map_location=device)
                    model_cfg = data.get("config", {"dim": 128, "n_layers": 4, "n_heads": 4})
                    model = UHZero(**model_cfg).to(device)
                    model.load_state_dict(data["model_state_dict"])
                else:
                    model = UHZero(vocab_size=ByteTokenizer.VOCAB_SIZE, dim=128, n_layers=4, n_heads=4).to(device)
                model.eval()
                _cached_model = model
                _cached_device = device
                _model_type = "mini"
        else:
            adara = _cached_model
            device = _cached_device

        if globals().get("_model_type") == "qwen":
            raw_gen = _cached_model.generate(prompt_text, max_new_tokens=max_new_tokens, temperature=0.6)
            generated_code = raw_gen
        else:
            raw_gen = _cached_model.generate(prompt_text, max_new_tokens=max_new_tokens, temperature=0.7, top_k=20, repetition_penalty=1.25, device=device)
            if raw_gen.startswith(prompt_text):
                generated_code = raw_gen[len(prompt_text):].strip()
            else:
                generated_code = raw_gen.strip()

        # Run Sandbox Evaluation
        executor = CodeExecutor()
        success, feedback, reward = executor.execute_multilang(generated_code, language)

        return {
            "success": True,
            "prompt": prompt_text,
            "language": language,
            "generated_code": generated_code,
            "full_output": raw_gen,
            "sandbox_valid": success,
            "sandbox_feedback": feedback,
            "reward": reward
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


class UHZeroWebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR / "web" / "static"), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/zero/"):
            path = path[5:]
        elif path == "/zero":
            path = "/"

        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            data = get_telemetry_status()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        elif path == "/api/languages":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            langs = [
                {
                    "id": l.id,
                    "name": l.name,
                    "category": l.category,
                    "extension": l.extension,
                    "paradigm": l.paradigm,
                    "print_statement": l.print_statement,
                    "sample_code": l.sample_code,
                    "description": l.description
                }
                for l in get_all_languages()
            ]
            self.wfile.write(json.dumps({"count": len(langs), "languages": langs}).encode("utf-8"))
            return

        elif path == "/api/logs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            log_lines = []
            if LOG_FILE.exists():
                try:
                    all_lines = LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
                    log_lines = all_lines[-80:]
                except Exception:
                    pass
            self.wfile.write(json.dumps({"lines": log_lines}).encode("utf-8"))
            return

        elif path == "/api/solutions":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            solutions = []
            total_count = 0
            if REPLAY_FILE.exists():
                try:
                    with open(REPLAY_FILE, "r", encoding="utf-8") as rf:
                        for line in rf:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                obj = json.loads(line)
                                code_str = obj.get("code", "")
                                is_j, _ = is_degenerate_code(code_str)
                                if is_j:
                                    continue
                                total_count += 1
                                solutions.append({
                                    "language": obj.get("language", "code"),
                                    "language_name": obj.get("language_name", obj.get("language", "Code")),
                                    "level": obj.get("level", 1),
                                    "prompt": obj.get("prompt", ""),
                                    "code": code_str,
                                    "expected_output": obj.get("expected_output", "")
                                })
                            except Exception:
                                pass
                except Exception:
                    pass
            recent = solutions[-30:]
            recent.reverse()
            self.wfile.write(json.dumps({"total_count": total_count, "recent": recent}).encode("utf-8"))
            return

        elif path == "/api/download_checkpoint":
            ckpt_path = BASE_DIR / "uh_zero_v2_checkpoint.pt"
            if ckpt_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", 'attachment; filename="uh_zero_v2_checkpoint.pt"')
                self.send_header("Content-Length", str(ckpt_path.stat().st_size))
                self.end_headers()
                with open(ckpt_path, "rb") as f:
                    while chunk := f.read(1024 * 1024):
                        self.wfile.write(chunk)
                return
            else:
                self.send_response(404)
                self.end_headers()
                return

        # Explicitly serve index.html with no-cache headers
        if path in ("/", "/index.html"):
            index_path = BASE_DIR / "web" / "static" / "index.html"
            if index_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.end_headers()
                self.wfile.write(index_path.read_bytes())
                return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/zero/"):
            path = path[5:]
        elif path == "/zero":
            path = "/"
        length = int(self.headers.get("Content-Length", 0))

        if path == "/api/upload_checkpoint":
            ckpt_path = BASE_DIR / "uh_zero_v2_checkpoint.pt"
            tmp_path = BASE_DIR / "uh_zero_v2_checkpoint.pt.tmp"
            try:
                with open(tmp_path, "wb") as f:
                    remaining = length
                    while remaining > 0:
                        chunk_size = min(remaining, 1024 * 1024)
                        chunk = self.rfile.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        remaining -= len(chunk)
                tmp_path.replace(ckpt_path)
                resp = {"status": "success", "message": f"Checkpoint {ckpt_path.stat().st_size} bytes tersimpan."}
                self.send_response(200)
            except Exception as e:
                resp = {"status": "error", "message": str(e)}
                self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            req_data = {}

        if path == "/api/generate":
            prompt = req_data.get("prompt", "print('halo')")
            lang = req_data.get("language", "python")
            max_tokens = int(req_data.get("max_tokens", 48))
            res = execute_inference(prompt, lang, max_tokens)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        elif path == "/api/train/start":
            steps = int(req_data.get("steps", 500))
            grow_at = int(req_data.get("grow_at", 200))
            if is_training_active():
                resp = {"status": "already_running", "message": "Training loop sudah aktif berjalan."}
            else:
                cmd = [sys.executable, str(BASE_DIR / "start_bg.py")]
                subprocess.run(cmd, cwd=str(BASE_DIR))
                resp = {"status": "started", "message": "Proses latihan otonom UH-0 berhasil dinyalakan."}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        elif path == "/api/train/stop":
            cmd = [sys.executable, str(BASE_DIR / "stop_bg.py")]
            subprocess.run(cmd, cwd=str(BASE_DIR))
            resp = {"status": "stopped", "message": "Proses latihan otonom UH-0 berhasil dihentikan dengan aman."}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        elif path == "/api/upload_checkpoint":
            ckpt_path = BASE_DIR / "uh_zero_v2_checkpoint.pt"
            tmp_path = BASE_DIR / "uh_zero_v2_checkpoint.pt.tmp"
            try:
                with open(tmp_path, "wb") as f:
                    remaining = length
                    while remaining > 0:
                        chunk_size = min(remaining, 1024 * 1024)
                        chunk = self.rfile.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        remaining -= len(chunk)
                tmp_path.replace(ckpt_path)
                resp = {"status": "success", "message": f"Checkpoint {ckpt_path.stat().st_size} bytes tersimpan."}
                self.send_response(200)
            except Exception as e:
                resp = {"status": "error", "message": str(e)}
                self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def run_web_server(port: int = 8099, host: str = "0.0.0.0"):
    static_dir = BASE_DIR / "web" / "static"
    static_dir.mkdir(parents=True, exist_ok=True)

    # Save PID
    WEB_PID_FILE.write_text(str(os.getpid()))

    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, UHZeroWebHandler)
    print(f"=========================================================")
    print(f"🚀 UH-0 Web Observatory Online")
    print(f"   Listening on: http://{host}:{port}")
    print(f"   80 Programming Languages Hub Active ({len(LANGUAGES_CATALOG)} languages)")
    print(f"=========================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if WEB_PID_FILE.exists():
            WEB_PID_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="UH-0 Web Observatory")
    parser.add_argument("--port", type=int, default=8099, help="Port server (default 8099)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address (default 0.0.0.0)")
    args = parser.parse_args()
    run_web_server(port=args.port, host=args.host)
