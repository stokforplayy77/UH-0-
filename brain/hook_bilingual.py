with open('/teamspace/studios/this_studio/uh-zero/brain/notes_80_languages.py', 'r', encoding='utf-8') as f:
    text = f.read()

harvester_code = """
import json
from pathlib import Path

CONV_BILINGUAL_FILE = Path('/teamspace/studios/this_studio/uh-zero/data/conversations_bilingual.jsonl')
BILINGUAL_DIALOGUES = []
if CONV_BILINGUAL_FILE.exists():
    try:
        with open(CONV_BILINGUAL_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    BILINGUAL_DIALOGUES.append(json.loads(line))
        print(f'[*] Terbaca {len(BILINGUAL_DIALOGUES):,} dialog nyata (Indonesia & Inggris) untuk percakapan alami!')
    except Exception as e:
        print(f'[-] Error baca bilingual: {e}')
"""

if 'BILINGUAL_DIALOGUES' not in text:
    text = harvester_code + '\n' + text

old_diag = """        # 2. 20% WAKTU: Dialog Percakapan & Tanya Jawab Ramah
        if dice < 0.50 and self.dialogues:
            diag = random.choice(self.dialogues)"""

new_diag = """        # 2. 25% WAKTU: DIALOG PERCAKAPAN & CARA MENGOBROL NYATA (INDONESIA & INGGRIS ALAMI)
        if dice < 0.60:
            if BILINGUAL_DIALOGUES and random.random() < 0.85:
                diag = random.choice(BILINGUAL_DIALOGUES)
                d_lang = diag.get("lang", "id")
                lang_label = "Bahasa Indonesia" if d_lang == "id" else "English"
                prompt = (
                    f"<|im_start|>system\\n"
                    f"Kamu adalah UH-0 (Adara AI), asisten AI yang cerdas, memiliki adab berbicara yang sopan, ramah, dan artikulatif dalam {lang_label}.\\n"
                    f"Jawablah pertanyaan dan berinteraksilah dengan pengguna secara alami, berbobot, dan santun.<|im_end|>\\n"
                    f"<|im_start|>user\\n{diag['user']}<|im_end|>\\n"
                    f"<|im_start|>assistant\\n"
                )
                return {
                    "prompt": prompt,
                    "target_code": diag["assistant"],
                    "language": f"obrolan_{d_lang}",
                    "topic": f"Dialog Alami ({lang_label})",
                    "source": "bilingual_conversations_real"
                }
            elif self.dialogues:
                diag = random.choice(self.dialogues)"""

if old_diag in text:
    text = text.replace(old_diag, new_diag)
    with open('/teamspace/studios/this_studio/uh-zero/brain/notes_80_languages.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('[+] BERHASIL MENGINTEGRASIKAN 15.635 DIALOG PERCAKAPAN NYATA!')
else:
    print('[-] Pattern old_diag not found')
