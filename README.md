# 🌟 UH-0 (UH Labs Zero) - Self-Evolving AI Coding Engine

> **Adara AI Core Engine** — Model AI yang lahir dari 0 (Fase Bayi ~1M parameter), mengevaluasi kodenya sendiri di Sandbox, dan secara otonom melipatgandakan parameternya sendiri (**Net2Net Function-Preserving Parameter Growth**) seiring waktu tanpa amnesia (*Catastrophic Forgetting*).

---

## 🏛️ Arsitektur & Struktur Folder

```text
/uh-zero/
├── brain/
│   ├── model.py            # Otak utama: Autoregressive Mini-Transformer (Byte-level, 1M params)
│   ├── grow.py             # Logika Net2Net: Net-Wider-Net & Net-Deeper-Net (f_new(x) = f_old(x))
│   └── router.py           # Dynamic LoRA & Mixture-of-Experts (MoE) Skill Router
├── world/
│   ├── executor.py         # Sandbox eksekusi kode Python (syntax & runtime error feedback)
│   └── tasks.py            # Generator kurikulum soal tak terbatas (Fase Bayi -> Balita -> SD)
├── memory/
│   ├── skill_library/      # Tempat penyimpanan checkpoint bobot & LoRA adapter skill baru
│   └── replay_buffer.jsonl # Experience Replay Buffer (10% ingatan lama untuk anti-amnesia)
├── data/
│   └── dataset_struk.jsonl # Dataset spesialisasi domain (parsing struk belanja & data ongkir)
├── train.py                # Loop kehidupan utama (Autonomous Curriculum + Net2Net Growth)
└── train_lora.py           # Fine-tuner keahlian khusus cepat (<30 menit) via LoRA
```

---

## 🚀 Cara Menjalankan

### 1. Loop Kehidupan Utama (Evolusi Mandiri dari 0):
```bash
# Jalankan 500 langkah dengan pemicu pertumbuhan parameter otomatis di step 200
python3 train.py --steps 500 --grow_at 200

# Atau biarkan hidup selamanya di latar belakang
python3 train.py --steps 0 --grow_at 1000
```
* **Apa yang terjadi:**
  1. Model mulai dari ~1.2 Juta parameter (Fase Bayi: `dim=128`, 4 layer).
  2. Model menerima soal dari generator kurikulum (`print`, aritmatika).
  3. Model mencoba menjawab dan kodenya langsung dieksekusi di Sandbox `world/executor.py`.
  4. Begitu mencapai step 200 (atau saat otak jenuh), **Net2Net** otomatis memicu penggandaan dimensi (`dim=128` $\to$ `256`), melipatgandakan parameter menjadi **~4.5 Juta parameter secara live** tanpa kehilangan kemampuan sebelumnya!

### 2. Fine-Tuning Keahlian Khusus (Parsing Struk & Ongkir):
```bash
python3 train_lora.py --epochs 30 --dataset data/dataset_struk.jsonl
```
* Model dasar dibekukan (*frozen*), hanya melatih parameter LoRA adaptif (<2% parameter), menghasilkan spesialis parsing data belanja tanpa *overfitting*.

---

## 📈 Roadmap Evolusi

1. **Fase Bayi (Minggu 1-2 | ~1M params):**
   * Sintaks dasar: `print("halo")`, operasi aritmatika integer `a + b`, `a * b`.
2. **Fase Balita (Minggu 3-4 | ~5M - 10M params via Net2Net):**
   * Variabel, percabangan `if/else`, perulangan `for i in range()`.
3. **Fase Anak SD (Bulan 2 | ~20M - 50M params via Net2Net + Depth):**
   * Pembuatan fungsi `def`, manipulasi string, ekstraksi JSON, dan parsing struk belanja Indonesia.
