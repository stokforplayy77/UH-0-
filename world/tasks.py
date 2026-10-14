#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - Multi-Language Curriculum Task Generator
Generates infinite procedural coding tasks across 80 Programming Languages.
Supports progressive stages:
- Level 1 (Fase Bayi): Basic syntax, output/print, and arithmetic operations
- Level 2 (Fase Balita): Variables, data types, if/else conditionals, loops
- Level 3 (Fase Anak SD): Function declarations, return values, string/data parsing
- Level 4 (Fase Remaja): Multi-language algorithms & data structures
"""

import random
from typing import Dict, Any, List, Optional
import os
import sys

# Ensure brain package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from brain.languages import LANGUAGES_CATALOG, ProgrammingLanguage, get_language
except ImportError:
    LANGUAGES_CATALOG = {}


class TaskCurriculum:
    def __init__(self):
        self.level_names = {
            1: "Fase Bayi (Sintaks Dasar & Aritmatika 80 Bahasa)",
            2: "Fase Balita (Variabel, If-Else, For Loop 80 Bahasa)",
            3: "Fase Anak SD (Fungsi, Return, & Parsing Struk/Data)",
            4: "Fase Remaja (Algoritma Multi-Bahasa & Struktur Data)"
        }
        self.languages_list = list(LANGUAGES_CATALOG.keys()) if LANGUAGES_CATALOG else ["python"]

    def generate_task(self, level: int = 1, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Menghasilkan satu task pembelajaran sesuai level dan bahasa target.
        Jika language=None, secara default memprioritaskan Python (60%) atau
        mengambil acak salah satu dari 80 bahasa (40%).
        """
        if not language:
            if random.random() < 0.6:
                lang_key = "python"
            else:
                lang_key = random.choice(self.languages_list)
        else:
            lang_key = language.lower() if language.lower() in LANGUAGES_CATALOG else "python"

        lang_meta = LANGUAGES_CATALOG.get(lang_key)

        if lang_key == "python":
            if level <= 1:
                task = self._generate_python_level_1()
            elif level == 2:
                task = self._generate_python_level_2()
            else:
                task = self._generate_python_level_3()
            task["language"] = "python"
            task["language_name"] = "Python"
            return task

        # Non-Python Multi-Language Generation
        return self._generate_multilang_task(lang_key, lang_meta, level)

    def _generate_python_level_1(self) -> Dict[str, Any]:
        """Fase Bayi: print string sederhana & operasi aritmatika Python."""
        subtask = random.choice(["print_string", "addition", "multiplication", "subtraction"])
        
        if subtask == "print_string":
            words = ["halo", "dunia", "adara", "python", "uhlabs", "zero", "bisa", "sukses"]
            word = random.choice(words)
            prompt = f'# [Python] Tulis kode untuk mencetak kata "{word}"\n'
            gt = f'print("{word}")'
            expected = word
        elif subtask == "addition":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            prompt = f'# [Python] Hitung dan cetak hasil dari {a} + {b}\n'
            gt = f'print({a} + {b})'
            expected = str(a + b)
        elif subtask == "multiplication":
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            prompt = f'# [Python] Hitung dan cetak hasil dari {a} * {b}\n'
            gt = f'print({a} * {b})'
            expected = str(a * b)
        else:
            a = random.randint(15, 30)
            b = random.randint(1, 14)
            prompt = f'# [Python] Hitung dan cetak hasil dari {a} - {b}\n'
            gt = f'print({a} - {b})'
            expected = str(a - b)

        return {
            "prompt": prompt,
            "ground_truth": gt,
            "expected_output": expected,
            "level": 1
        }

    def _generate_python_level_2(self) -> Dict[str, Any]:
        """Fase Balita: Variabel, If-Else, dan Loop sederhana Python."""
        subtask = random.choice(["variable", "if_else", "for_loop"])

        if subtask == "variable":
            val = random.randint(10, 100)
            prompt = f'# [Python] Buat variabel x = {val} lalu cetak x\n'
            gt = f'x = {val}\nprint(x)'
            expected = str(val)
        elif subtask == "if_else":
            val = random.choice([5, -3, 10, -7])
            cond_str = "positif" if val > 0 else "negatif"
            prompt = f'# [Python] Jika angka {val} lebih besar dari 0 cetak "positif", selain itu "negatif"\n'
            gt = f'n = {val}\nif n > 0:\n    print("positif")\nelse:\n    print("negatif")'
            expected = cond_str
        else:
            limit = random.randint(3, 5)
            prompt = f'# [Python] Cetak angka dari 0 sampai {limit - 1} menggunakan for loop\n'
            gt = f'for i in range({limit}):\n    print(i)'
            expected = "\n".join([str(i) for i in range(limit)])

        return {
            "prompt": prompt,
            "ground_truth": gt,
            "expected_output": expected,
            "level": 2
        }

    def _generate_python_level_3(self) -> Dict[str, Any]:
        """Fase Anak SD: Pembuatan fungsi def & Parsing struk belanja mini."""
        subtask = random.choice(["function_def", "struk_parsing"])

        if subtask == "function_def":
            a = random.randint(5, 15)
            b = random.randint(5, 15)
            prompt = f'# [Python] Buat fungsi tambah(a, b) dan cetak tambah({a}, {b})\n'
            gt = f'def tambah(a, b):\n    return a + b\nprint(tambah({a}, {b}))'
            expected = str(a + b)
        else:
            stores = ["ALFAMART", "INDOMARET", "WARUNG"]
            store = random.choice(stores)
            prices = [15000, 25000, 50000, 12000]
            price = random.choice(prices)
            prompt = f'# [Python] Ekstrak total harga integer dari teks struk "{store} Rp {price}" dan cetak\n'
            gt = f'teks = "{store} Rp {price}"\ntotal = int(teks.split()[-1])\nprint(total)'
            expected = str(price)

        return {
            "prompt": prompt,
            "ground_truth": gt,
            "expected_output": expected,
            "level": 3
        }

    def _generate_multilang_task(self, lang_key: str, lang_meta: Any, level: int) -> Dict[str, Any]:
        """Menghasilkan task untuk bahasa selain Python dari katalog 80 bahasa."""
        name = lang_meta.name if lang_meta else lang_key.title()
        comment = lang_meta.comment_single if lang_meta else "//"

        if level <= 1:
            # Level 1: Basic print / hello world or sample code
            prompt = f"{comment} [{name}] Tulis kode untuk mencetak pesan 'Hello, World!' dalam bahasa {name}:\n"
            gt = lang_meta.print_statement if lang_meta else f'print("Hello, World!")'
            expected = "Hello, World!"
        elif level == 2:
            # Level 2: Variable declaration & loop
            sub = random.choice(["var", "loop"])
            if sub == "var":
                prompt = f"{comment} [{name}] Deklarasikan variabel x bernilai 42 dalam bahasa {name}:\n"
                gt = lang_meta.variable_decl if lang_meta else "x = 42"
                expected = "42"
            else:
                prompt = f"{comment} [{name}] Buat struktur perulangan loop 0 sampai 4 dalam bahasa {name}:\n"
                gt = lang_meta.loop_sample if lang_meta else "for i in 0..4"
                expected = "loop"
        else:
            # Level 3: Function declaration
            prompt = f"{comment} [{name}] Buat fungsi penjumlahan tambah(a, b) dalam bahasa {name}:\n"
            gt = lang_meta.function_decl if lang_meta else "function tambah(a, b) { return a + b; }"
            expected = "function"

        return {
            "prompt": prompt,
            "ground_truth": gt,
            "expected_output": expected,
            "level": level,
            "language": lang_key,
            "language_name": name
        }


def get_task_generator() -> TaskCurriculum:
    return TaskCurriculum()
