#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - Experience Replay & Memory Engine
Mencegah Catastrophic Forgetting dengan mencampur 10% pengalaman masa lalu
ke setiap batch pembelajaran baru, serta menyimpan checkpoints ke skill_library/.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional


class ExperienceReplay:
    def __init__(self, memory_dir: Optional[str] = None, max_size: int = 5000):
        if memory_dir is None:
            self.memory_dir = Path(__file__).resolve().parent
        else:
            self.memory_dir = Path(memory_dir)
            
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.buffer_file = self.memory_dir / "replay_buffer.jsonl"
        self.skill_dir = self.memory_dir / "skill_library"
        self.skill_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_size = max_size
        self.buffer: List[Dict[str, Any]] = []
        self._load_buffer()

    def _load_buffer(self):
        if self.buffer_file.exists():
            try:
                from world.executor import is_degenerate_code
                with open(self.buffer_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            item = json.loads(line.strip())
                            is_junk, _ = is_degenerate_code(item.get("code", ""))
                            if not is_junk:
                                self.buffer.append(item)
                print(f"[🧠 Memory] Memuat {len(self.buffer)} ingatan bersih tervalidasi dari {self.buffer_file.name}")
            except Exception as e:
                print(f"[!] Gagal membaca replay buffer: {e}")

    def save_experience(
        self,
        prompt: str,
        code: str,
        expected_output: str,
        level: int,
        language: str = "python",
        language_name: str = "Python"
    ):
        """Menyimpan pengalaman yang berhasil ke ingatan jangka panjang tanpa duplikasi dan anti-sampah."""
        try:
            from world.executor import is_degenerate_code
            is_junk, _ = is_degenerate_code(code)
            if is_junk:
                return
        except Exception:
            pass

        # Hindari duplikat persis prompt dan code agar buffer bervariasi
        for existing in self.buffer[-50:]:
            if existing.get("prompt") == prompt and existing.get("code") == code:
                return

        item = {
            "prompt": prompt,
            "code": code,
            "expected_output": expected_output,
            "level": level,
            "language": language,
            "language_name": language_name
        }
        self.buffer.append(item)
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)

        # Append ke file jsonl
        try:
            with open(self.buffer_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def mix_batch(self, new_tasks: List[Dict[str, Any]], replay_ratio: float = 0.1) -> List[Dict[str, Any]]:
        """
        Mencampur batch baru dengan ingatan masa lalu (Anti-Catastrophic Forgetting).
        Jika batch size = 1, gunakan probabilitas acak replay_ratio (misal 10% kemungkinan review masa lalu).
        Jika batch size > 1, campur proporsional.
        """
        if not self.buffer or replay_ratio <= 0:
            return new_tasks

        # Untuk batch size 1 (single-task loop): 90% ambil soal baru dari kurikulum, 10% review ingatan lama
        if len(new_tasks) == 1:
            if random.random() < replay_ratio:
                r = random.choice(self.buffer)
                return [{
                    "prompt": r["prompt"],
                    "ground_truth": r["code"],
                    "expected_output": r["expected_output"],
                    "level": r.get("level", 1),
                    "language": r.get("language", "python"),
                    "language_name": r.get("language_name", "Python"),
                    "is_replay": True
                }]
            return new_tasks

        n_replay = max(1, int(len(new_tasks) * replay_ratio))
        replays = random.sample(self.buffer, min(n_replay, len(self.buffer)))
        
        replay_tasks = [
            {
                "prompt": r["prompt"],
                "ground_truth": r["code"],
                "expected_output": r["expected_output"],
                "level": r.get("level", 1),
                "language": r.get("language", "python"),
                "language_name": r.get("language_name", "Python"),
                "is_replay": True
            }
            for r in replays
        ]
        
        mixed = new_tasks[:max(1, len(new_tasks) - len(replay_tasks))] + replay_tasks
        random.shuffle(mixed)
        return mixed

    def count(self) -> int:
        return len(self.buffer)
