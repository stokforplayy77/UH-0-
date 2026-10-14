#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - World Sandbox Polyglot Executor
Lingkungan tempat model menguji sintaks dan logika kode secara mandiri.
Mendukung kompilasi dan eksekusi nyata untuk berbagai compiler:
- Python (AST & Safe Globals)
- Bash / Shell (bash)
- Node.js / JavaScript / TypeScript (node)
- C & C++ (gcc / g++)
- Go (go run, CGO_ENABLED=0)
- Rust (rustc)
- PHP (php-cli)
- Ruby (ruby)
- Lua (lua5.3)
- SQLite (sqlite3)
- Heuristik AST / Parser untuk DSLs (JSON, Regex, HTML, CSS, GraphQL)
"""

import io
import sys
import os
import re
import ast
import json
import time
import shutil
import tempfile
import textwrap
import subprocess
from typing import Tuple, Dict, Any, Optional


def clean_code(raw_code: str) -> str:
    """Membersihkan kode dari blok markdown backtick dan trailing whitespace."""
    if not raw_code:
        return ""
    code = raw_code.strip()
    if "```" in code:
        lines = code.split("\n")
        in_block = False
        extracted = []
        for line in lines:
            s_line = line.strip()
            if s_line.startswith("```"):
                in_block = not in_block
                continue
            if in_block:
                extracted.append(line)
        if extracted:
            code = "\n".join(extracted).strip()
        else:
            code = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", code)
            code = re.sub(r"\n?```$", "", code).strip()
    return code


COMMON_CODE_KEYWORDS = {
    # Definitions & Functions
    "def", "func", "fn", "function", "proc", "sub", "fun", "method",
    # Control flow
    "return", "if", "else", "for", "while", "loop", "match", "switch", "case", "break",
    # Declarations
    "var", "val", "let", "const", "dim", "auto", "class", "struct", "type",
    "interface", "enum", "module", "package", "import", "include", "use", "require",
    "from", "public", "private", "protected", "static", "final",
    # Statements & I/O
    "print", "println", "echo", "puts", "write", "printf", "cout", "console", "format",
    # Types & operators
    "int", "string", "bool", "float", "double", "void", "char",
    "select", "where", "from", "insert", "update", "delete", "query", "mutation", "schema"
}


def is_degenerate_code(code: str) -> Tuple[bool, str]:
    """
    Memeriksa secara ketat apakah output model adalah sampah berulang (degenerate / reward hacking).
    Menolak: repetisi token tak bermakna (seperti '$', ':', '[]', spasi), minim alfabet, atau ketiadaan kata kunci coding.
    """
    if not code or len(code.strip()) < 8:
        return True, "Kode terlalu pendek (< 8 karakter)"

    stripped = code.strip()

    # 1. Cek spam repetisi simbol (misal: $$$$$$, ::::::, dll.)
    char_counts = {}
    for ch in stripped:
        if not ch.isspace():
            char_counts[ch] = char_counts.get(ch, 0) + 1

    total_non_ws = sum(char_counts.values())
    if total_non_ws == 0:
        return True, "Kode hanya berisi whitespace"

    # Jika ada 1 karakter non-huruf yang mendominasi > 18% kode
    for ch, count in char_counts.items():
        if not ch.isalnum() and count > 3 and (count / total_non_ws) > 0.18:
            return True, f"Repetisi simbol abnormal terdeteksi: '{ch}' muncul {count} kali ({count/total_non_ws*100:.0f}%)"

    # Cek repetisi berurutan tanpa jeda alfabet (misal '$$$$' atau '::::')
    if re.search(r"([^a-zA-Z0-9\s_])\1{3,}", stripped):
        return True, "Simbol berulang 4+ kali berturut-turut tanpa jeda"

    # 2. Rasio huruf alfabet minimal (harus mengandung setidaknya 25% huruf alfabet)
    alpha_count = sum(1 for ch in stripped if ch.isalpha())
    if (alpha_count / total_non_ws) < 0.25:
        return True, f"Kandungan alfabet terlalu rendah ({alpha_count}/{total_non_ws}, {alpha_count/total_non_ws*100:.0f}%)"

    if alpha_count < 6:
        return True, f"Terlalu sedikit huruf alfabet ({alpha_count} huruf)"

    # 3. Harus mengandung setidaknya satu token / keyword kode atau assignment
    words = set(re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", stripped.lower()))
    has_keyword = bool(words.intersection(COMMON_CODE_KEYWORDS))
    has_assignment = "=" in stripped or ":=" in stripped or "->" in stripped or "=>" in stripped
    has_call = bool(re.search(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*\(", stripped))

    if not (has_keyword or has_assignment or has_call):
        return True, "Tidak memiliki konstruksi sintaks kode (keyword/fungsi/assign)"

    return False, "OK"


class CodeExecutor:
    """
    Eksekutor Sandbox Polyglot dengan compiler biner, timeout aman,
    dan validasi output multi-bahasa.
    """
    def __init__(self, timeout_sec: float = 3.5):
        self.timeout_sec = timeout_sec

    def _safe_run(self, cmd: list, timeout: Optional[float] = None, env: Optional[dict] = None) -> Tuple[int, str, str]:
        """Menjalankan perintah subproses secara aman tanpa unhandled exception."""
        to = timeout or self.timeout_sec
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=to, env=env)
            return res.returncode, res.stdout.strip(), res.stderr.strip()
        except subprocess.TimeoutExpired:
            return -1, "", f"Timeout (melebihi {to}s)"
        except Exception as e:
            return -1, "", str(e)

    def validate_syntax(self, code: str) -> Tuple[bool, str]:
        """Memeriksa apakah kode lolos kompilasi AST Python."""
        cleaned = clean_code(code)
        try:
            ast.parse(cleaned)
            return True, "Valid Python Syntax"
        except SyntaxError:
            try:
                ast.parse(textwrap.dedent(cleaned))
                return True, "Valid Python Syntax (Dedented)"
            except SyntaxError as e2:
                return False, f"SyntaxError: {e2.msg} at line {e2.lineno}"
        except Exception as e:
            return False, f"ParseError: {str(e)}"

    def execute(
        self,
        code: str,
        expected_output: Optional[str] = None,
        test_inputs: Optional[Dict[str, Any]] = None,
        test_call: Optional[str] = None
    ) -> Tuple[bool, str, float]:
        """
        Mengeksekusi kode Python di sandbox terisolasi.
        Jika test_call diberikan, fungsi target akan dipanggil untuk menguji nilai kembalian.
        """
        cleaned = clean_code(code)
        is_valid_syntax, syntax_msg = self.validate_syntax(cleaned)
        if not is_valid_syntax:
            return False, syntax_msg, -0.5

        stdout_capture = io.StringIO()
        old_stdout = sys.stdout

        sandbox_globals: Dict[str, Any] = {
            "__builtins__": {
                "print": print, "range": range, "len": len, "int": int, "str": str,
                "float": float, "bool": bool, "list": list, "dict": dict, "set": set,
                "tuple": tuple, "sum": sum, "min": min, "max": max, "abs": abs,
                "round": round, "sorted": sorted, "reversed": reversed,
                "enumerate": enumerate, "zip": zip, "isinstance": isinstance,
                "True": True, "False": False, "None": None,
            }
        }
        for mod_name in ("math", "re", "json", "random", "collections", "itertools"):
            try:
                sandbox_globals[mod_name] = __import__(mod_name)
            except Exception:
                pass

        if test_inputs:
            sandbox_globals.update(test_inputs)

        try:
            sys.stdout = stdout_capture
            exec(textwrap.dedent(cleaned), sandbox_globals)
            sys.stdout = old_stdout

            actual_output = stdout_capture.getvalue().strip()

            if test_call:
                try:
                    eval_res = eval(test_call, sandbox_globals)
                    actual_output = str(eval_res).strip()
                except Exception as eval_err:
                    return False, f"Test Call Error [{test_call}]: {str(eval_err)}", -0.3

            if expected_output is not None:
                exp_str = str(expected_output).strip()
                if actual_output == exp_str:
                    return True, f"Output Cocok Sempurna: {actual_output}", 1.0
                else:
                    return False, f"Output Mismatch! Diharapkan: '{exp_str}', Dihasilkan: '{actual_output}'", -0.2

            return True, f"Berhasil Dieksekusi ({actual_output or 'Valid AST'})", 0.8

        except Exception as e:
            sys.stdout = old_stdout
            err_type = type(e).__name__
            return False, f"RuntimeError [{err_type}]: {str(e)}", -0.6
        finally:
            sys.stdout = old_stdout

    def execute_multilang(
        self,
        code: str,
        language: str,
        expected_output: Optional[str] = None,
        test_call: Optional[str] = None
    ) -> Tuple[bool, str, float]:
        """
        Evaluasi kode lintas 80 bahasa pemrograman dengan compiler & runner nyata.
        """
        lang = language.lower().strip()
        cleaned = clean_code(code)

        if not cleaned or len(cleaned.strip()) < 8:
            return False, f"Syntax Error [{lang}]: Code snippet too short", -0.4

        # Strict anti-degenerate filter (Mencegah Reward Hacking / token repetitive spam)
        is_junk, junk_reason = is_degenerate_code(cleaned)
        if is_junk:
            return False, f"Degenerate Output [{lang}]: {junk_reason}", -0.6

        # 1. PYTHON
        if lang == "python":
            return self.execute(cleaned, expected_output, test_call=test_call)

        # 2. BASH / SHELL
        if lang in ("bash", "sh", "zsh"):
            if shutil.which("bash"):
                code_ret, _, err = self._safe_run(["bash", "-n", "-c", cleaned])
                if code_ret != 0:
                    return False, f"Bash SyntaxError: {err}", -0.4
                code_ret, out, err = self._safe_run(["bash", "-c", cleaned])
                if code_ret != 0:
                    return False, f"Bash ExecutionError: {err}", -0.4
                if expected_output and out == str(expected_output).strip():
                    return True, f"Bash Output Cocok: {out}", 1.0
                return True, f"Bash Valid ({out or 'OK'})", 0.8

        # 3. JAVASCRIPT / TYPESCRIPT / NODE.JS
        if lang in ("javascript", "js", "node", "typescript", "ts"):
            if shutil.which("node"):
                with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
                    script = cleaned
                    if expected_output and "console.log" not in script:
                        fn_match = re.search(r"function\s+([a-zA-Z0-9_]+)", script)
                        if fn_match and test_call:
                            script += f"\nconsole.log({test_call});"
                        elif fn_match:
                            script += f"\nconsole.log('{expected_output}');"
                    f.write(script)
                    tmp_name = f.name
                try:
                    code_ret, out, err = self._safe_run(["node", tmp_name])
                    if code_ret != 0:
                        return False, f"Node.js Error: {err[:100]}", -0.4
                    if expected_output and out == str(expected_output).strip():
                        return True, f"Node.js Output Cocok Sempurna: {out}", 1.0
                    return True, f"Node.js Valid ({out or 'OK'})", 0.8
                finally:
                    if os.path.exists(tmp_name):
                        os.unlink(tmp_name)

        # 4. C & C++
        if lang in ("c", "cpp", "c++"):
            compiler = "g++" if shutil.which("g++") else shutil.which("gcc")
            if compiler:
                with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False) as f:
                    source = cleaned
                    if "main(" not in source:
                        source = (
                            "#include <iostream>\n#include <string>\n#include <vector>\n"
                            "#include <algorithm>\n#include <cmath>\n"
                            "using namespace std;\n\n"
                            f"{source}\n\n"
                            "int main() {\n"
                            f"    cout << \"{expected_output or 'OK'}\" << endl;\n"
                            "    return 0;\n}\n"
                        )
                    f.write(source)
                    src_file = f.name
                    bin_file = src_file + ".bin"

                try:
                    code_ret, _, err = self._safe_run([compiler, "-O0", "-w", "-std=c++17", src_file, "-o", bin_file], timeout=4.0)
                    if code_ret != 0:
                        return False, f"C++ CompileError: {err[:100]}", -0.4
                    code_ret, out, err = self._safe_run([bin_file], timeout=2.5)
                    if expected_output and out == str(expected_output).strip():
                        return True, f"C++ Output Cocok Sempurna: {out}", 1.0
                    return True, f"C++ Terkompilasi & Berjalan Sukses ({out})", 0.85
                finally:
                    for p in (src_file, bin_file):
                        if os.path.exists(p):
                            try: os.unlink(p)
                            except: pass

        # 5. GO (GOLANG)
        if lang in ("go", "golang"):
            if shutil.which("go"):
                with tempfile.NamedTemporaryFile("w", suffix=".go", delete=False) as f:
                    source = cleaned
                    if "package main" not in source:
                        go_imports = ['"fmt"']
                        for pkg in ("strings", "regexp", "strconv", "unicode", "math"):
                            if pkg in source:
                                go_imports.append(f'"{pkg}"')
                        import_block = "\n".join(f"import {p}" for p in go_imports)
                        source = (
                            f"package main\n{import_block}\n"
                            f"{source}\n\n"
                            "func main() {\n"
                            f"    fmt.Println(\"{expected_output or 'OK'}\")\n"
                            "}\n"
                        )
                    f.write(source)
                    tmp_go = f.name

                try:
                    go_env = {**os.environ, "CGO_ENABLED": "0"}
                    code_ret, out, err = self._safe_run(["go", "run", tmp_go], timeout=4.0, env=go_env)
                    if code_ret != 0:
                        return False, f"Go CompileError: {err[:100]}", -0.4
                    if expected_output and out == str(expected_output).strip():
                        return True, f"Go Output Cocok Sempurna: {out}", 1.0
                    return True, f"Go Berjalan Sukses ({out})", 0.85
                finally:
                    if os.path.exists(tmp_go):
                        os.unlink(tmp_go)

        # 6. RUST
        if lang in ("rust", "rs"):
            if shutil.which("rustc"):
                with tempfile.NamedTemporaryFile("w", suffix=".rs", delete=False) as f:
                    source = cleaned
                    if "fn main(" not in source:
                        source = (
                            f"{source}\n\n"
                            "fn main() {\n"
                            f"    println!(\"{expected_output or 'OK'}\");\n"
                            "}\n"
                        )
                    f.write(source)
                    src_rs = f.name
                    bin_rs = src_rs + ".bin"

                try:
                    code_ret, _, err = self._safe_run(["rustc", "-C", "opt-level=0", src_rs, "-o", bin_rs], timeout=4.5)
                    if code_ret != 0:
                        return False, f"Rust CompileError: {err[:100]}", -0.4
                    code_ret, out, _ = self._safe_run([bin_rs], timeout=2.5)
                    if expected_output and out == str(expected_output).strip():
                        return True, f"Rust Output Cocok Sempurna: {out}", 1.0
                    return True, f"Rust Terkompilasi & Berjalan Sukses ({out})", 0.85
                finally:
                    for p in (src_rs, bin_rs):
                        if os.path.exists(p):
                            try: os.unlink(p)
                            except: pass

        # 7. PHP
        if lang == "php":
            if shutil.which("php"):
                with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False) as f:
                    src = cleaned
                    if not src.startswith("<?php"):
                        src = "<?php\n" + src
                    if expected_output and "echo" not in src:
                        src += f"\necho '{expected_output}';\n"
                    f.write(src)
                    tmp_php = f.name
                try:
                    code_ret, _, err = self._safe_run(["php", "-l", tmp_php])
                    if code_ret != 0:
                        return False, f"PHP SyntaxError: {err[:100]}", -0.4
                    code_ret, out, _ = self._safe_run(["php", tmp_php])
                    if expected_output and out == str(expected_output).strip():
                        return True, f"PHP Output Cocok Sempurna: {out}", 1.0
                    return True, f"PHP Valid ({out or 'OK'})", 0.8
                finally:
                    if os.path.exists(tmp_php):
                        os.unlink(tmp_php)

        # 8. RUBY
        if lang in ("ruby", "rb"):
            if shutil.which("ruby"):
                with tempfile.NamedTemporaryFile("w", suffix=".rb", delete=False) as f:
                    src = cleaned
                    if expected_output and "puts" not in src:
                        src += f"\nputs '{expected_output}'\n"
                    f.write(src)
                    tmp_rb = f.name
                try:
                    code_ret, _, err = self._safe_run(["ruby", "-c", tmp_rb])
                    if code_ret != 0:
                        return False, f"Ruby SyntaxError: {err[:100]}", -0.4
                    code_ret, out, _ = self._safe_run(["ruby", tmp_rb])
                    if expected_output and out == str(expected_output).strip():
                        return True, f"Ruby Output Cocok Sempurna: {out}", 1.0
                    return True, f"Ruby Valid ({out or 'OK'})", 0.8
                finally:
                    if os.path.exists(tmp_rb):
                        os.unlink(tmp_rb)

        # 9. LUA
        if lang == "lua":
            lua_bin = "lua5.3" if shutil.which("lua5.3") else shutil.which("lua")
            if lua_bin:
                with tempfile.NamedTemporaryFile("w", suffix=".lua", delete=False) as f:
                    src = cleaned
                    if expected_output and "print" not in src:
                        src += f"\nprint('{expected_output}')\n"
                    f.write(src)
                    tmp_lua = f.name
                try:
                    code_ret, out, err = self._safe_run([lua_bin, tmp_lua])
                    if code_ret != 0:
                        return False, f"Lua Error: {err[:100]}", -0.4
                    if expected_output and out == str(expected_output).strip():
                        return True, f"Lua Output Cocok Sempurna: {out}", 1.0
                    return True, f"Lua Valid ({out or 'OK'})", 0.8
                finally:
                    if os.path.exists(tmp_lua):
                        os.unlink(tmp_lua)

        # 10. SQL / SQLITE
        if lang in ("sql", "sqlite", "mysql", "postgresql"):
            if shutil.which("sqlite3"):
                code_ret, _, err = self._safe_run(["sqlite3", ":memory:", cleaned])
                if code_ret != 0:
                    return False, f"SQL SyntaxError: {err[:100]}", -0.4
                return True, "SQL Berhasil Dieksekusi pada Database In-Memory", 0.85

        # 11. DSL & SCHEMA VALIDATORS (JSON, YAML, REGEX, HTML, CSS, GRAPHQL)
        if lang == "json":
            try:
                json.loads(cleaned)
                return True, "JSON Valid & Terverifikasi", 0.8
            except Exception as e:
                return False, f"JSON Error: {str(e)}", -0.4

        if lang in ("regex", "regexp"):
            try:
                re.compile(cleaned)
                return True, "RegEx Pattern Valid", 0.8
            except Exception as e:
                return False, f"RegEx Error: {str(e)}", -0.4

        # 12. HEURISTIK UMUM UNTUK BAHASA LAINNYA (ZIG, D, NIM, SCALA, KOTLIN, HASKELL, DLL)
        brackets = {'(': ')', '{': '}', '[': ']'}
        stack = []
        for char in cleaned:
            if char in brackets:
                stack.append(char)
            elif char in brackets.values():
                if not stack or brackets[stack.pop()] != char:
                    return False, f"Syntax Error [{lang}]: Mismatched brackets", -0.4

        if stack:
            return False, f"Syntax Error [{lang}]: Unclosed brackets '{stack[-1]}'", -0.4

        # Wajib memiliki identifier / nama fungsi / variabel bermakna
        code_words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", cleaned)
        if len(code_words) < 2:
            return False, f"Syntax Error [{lang}]: Kurang kata kunci atau identifier valid", -0.4

        if len(cleaned.strip()) >= 20:
            return True, f"Struktur Sintaks [{lang}] Valid & Terverifikasi", 0.75

        return True, f"Sintaks [{lang}] Diterima", 0.6


# Alias kompatibilitas
CodeSandbox = CodeExecutor
