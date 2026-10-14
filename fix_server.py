with open("/root/uh-zero/web/server.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'self.wfile.write(b"{"status": "ok"}")' in line:
        new_lines.append("                self.wfile.write(b'{\"status\": \"ok\"}')\n")
    else:
        new_lines.append(line)

with open("/root/uh-zero/web/server.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("SUCCESS REPLACING")
