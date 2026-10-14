with open("/root/uh-zero/web/server.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'length = int(self.headers.get("Content-Length", 0))' in line:
        insert = """
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
                return
"""
        new_lines.append(insert)

with open("/root/uh-zero/web/server.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("INSERTED append_log HANDLER DIRECTLY!")
