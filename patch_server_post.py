with open("/root/uh-zero/web/server.py", "r", encoding="utf-8") as f:
    code = f.read()

target = 'length = int(self.headers.get("Content-Length", 0))'
replacement = """length = int(self.headers.get("Content-Length", 0))

        if path == "/api/append_log":
            try:
                log_p = BASE_DIR / "train.log"
                data = self.rfile.read(length)
                with open(log_p, "wb") as lf:
                    lf.write(data)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
                return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                return"""

if "if path == \"/api/append_log\":" not in code:
    code = code.replace(target, replacement, 1)
    with open("/root/uh-zero/web/server.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("PATCHED SUCCESSFULLY")
else:
    print("ALREADY PATCHED")

