from brain.encyclopedia_formulas import OFFICIAL_FORMULAS_AND_DOCS, get_formula_lesson
#!/usr/bin/env python3
"""
UH-0 (UH Labs Zero) - Kitab Catatan Belajar 80 Bahasa Pemrograman (GitHub Code Library)
Koleksi komprehensif catatan teori sintaks, struktur program, dan implementasi kode nyata
untuk 80 bahasa pemrograman dunia nyata yang bersumber dari repositori GitHub, Rosetta Code,
dan standar dokumentasi resmi.
"""

from typing import Dict, Any, List, Optional
import random

# Definisi Catatan Sintaks Dasar & Karakteristik untuk 80 Bahasa Pemrograman
LANGUAGE_NOTES_CATALOG: Dict[str, Dict[str, Any]] = {
    # ==========================================
    # KATEGORI 1: WEB & GENERAL (10 BAHASA)
    # ==========================================
    "python": {
        "name": "Python", "category": "Web & General", "ext": "py",
        "intro": "Python adalah bahasa pemrograman tingkat tinggi multi-paradigma dengan sintaks berorientasi keterbacaan (indentasi signifikan).",
        "lessons": [
            ("Sintaks Dasar & Variabel", "# Deklarasi variabel dan tipe data\nnama: str = 'Adara AI'\nversi: float = 2.0\naktif: bool = True\nangka_list: list[int] = [1, 2, 3, 4, 5]\nkamus: dict[str, int] = {'a': 10, 'b': 20}\nprint(f'{nama} v{versi} - Status: {aktif}')"),
            ("Fungsi & Type Hints", "def hitung_luas_lingkaran(radius: float) -> float:\n    import math\n    if radius < 0:\n        raise ValueError('Radius tidak boleh negatif')\n    return math.pi * (radius ** 2)\n\nluas = hitung_luas_lingkaran(7.0)\nprint('Luas:', luas)"),
            ("Perulangan & List Comprehension", "kuadrat_genap = [x**2 for x in range(1, 20) if x % 2 == 0]\nfor i, val in enumerate(kuadrat_genap):\n    print(f'Index {i}: {val}')"),
            ("Algoritma: Binary Search", "def binary_search(arr: list[int], target: int) -> int:\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n\nres = binary_search([2, 5, 8, 12, 16, 23, 38], 16)\nprint('Index ditemukan:', res)"),
            ("Algoritma: Deteksi Palindrom", "def is_palindrome(teks: str) -> bool:\n    bersih = ''.join(c.lower() for c in teks if c.isalnum())\n    return bersih == bersih[::-1]\n\nprint(is_palindrome('Kasur ini rusak'))"),
            ("Algoritma: GCD Euclid & Fibonacci", "def gcd(a: int, b: int) -> int:\n    while b != 0:\n        a, b = b, a % b\n    return a\n\ndef fib(n: int) -> int:\n    if n <= 0: return 0\n    if n == 1: return 1\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b")
        ]
    },
    "javascript": {
        "name": "JavaScript", "category": "Web & General", "ext": "js",
        "intro": "JavaScript adalah bahasa dinamis berbasis prototipe yang menjadi fondasi utama ekosistem web modern (browser & Node.js).",
        "lessons": [
            ("Sintaks Dasar & Variabel", "const nama = 'Adara AI';\nlet versi = 2.0;\nconst aktif = true;\nconst daftar = [10, 20, 30, 40];\nconst user = { id: 1, role: 'admin' };\nconsole.log(`${nama} v${versi} - Aktif: ${aktif}`);"),
            ("Fungsi & Arrow Syntax", "const hitungDiskon = (harga, persentase) => {\n  if (persentase < 0 || persentase > 100) throw new Error('Persentase tidak valid');\n  return harga - (harga * persentase / 100);\n};\nconsole.log('Total bayar:', hitungDiskon(150000, 20));"),
            ("Array Higher-Order Functions", "const angka = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];\nconst kuadratGenap = angka\n  .filter(n => n % 2 === 0)\n  .map(n => n * n);\nconst total = kuadratGenap.reduce((acc, curr) => acc + curr, 0);\nconsole.log({ kuadratGenap, total });"),
            ("Algoritma: Binary Search", "function binarySearch(arr, target) {\n  let low = 0, high = arr.length - 1;\n  while (low <= high) {\n    const mid = Math.floor((low + high) / 2);\n    if (arr[mid] === target) return mid;\n    if (arr[mid] < target) low = mid + 1;\n    else high = mid - 1;\n  }\n  return -1;\n}\nconsole.log(binarySearch([1, 4, 7, 9, 15, 22], 9));"),
            ("Algoritma: GCD & Palindrome", "function gcd(a, b) {\n  while (b !== 0) {\n    const temp = b;\n    b = a % b;\n    a = temp;\n  }\n  return a;\n}\nfunction isPalindrome(str) {\n  const clean = str.toLowerCase().replace(/[^a-z0-9]/g, '');\n  return clean === clean.split('').reverse().join('');\n}")
        ]
    },
    "typescript": {
        "name": "TypeScript", "category": "Web & General", "ext": "ts",
        "intro": "TypeScript adalah strongly typed superset dari JavaScript yang menambahkan static type checking untuk skala aplikasi enterprise.",
        "lessons": [
            ("Interface & Type Aliases", "interface UserProfile {\n  id: number;\n  username: string;\n  isActive: boolean;\n  roles: string[];\n}\nconst admin: UserProfile = {\n  id: 101,\n  username: 'adara_dev',\n  isActive: true,\n  roles: ['superadmin', 'maintainer']\n};\nconsole.log(admin);"),
            ("Generics & Utility Functions", "function ambilElemenPertama<T>(arr: T[]): T | undefined {\n  return arr.length > 0 ? arr[0] : undefined;\n}\nconst angka = ambilElemenPertama<number>([10, 20, 30]);\nconst teks = ambilElemenPertama<string>(['alpha', 'beta']);"),
            ("Algoritma: Binary Search Bertipe", "function binarySearch(arr: readonly number[], target: number): number {\n  let low = 0;\n  let high = arr.length - 1;\n  while (low <= high) {\n    const mid = Math.floor((low + high) / 2);\n    if (arr[mid] === target) return mid;\n    if (arr[mid] < target) low = mid + 1;\n    else high = mid - 1;\n  }\n  return -1;\n}")
        ]
    },
    "php": {
        "name": "PHP", "category": "Web & General", "ext": "php",
        "intro": "PHP adalah bahasa scripting server-side yang populer untuk pengembangan web dinamis dan framework Laravel/Symfony.",
        "lessons": [
            ("Sintaks Dasar & Array Asosiatif", "<?php\n$nama = 'Adara AI';\n$versi = 2.0;\n$konfigurasi = [\n    'database' => 'sqlite',\n    'port' => 8080,\n    'debug' => true\n];\necho \"{$nama} v{$versi} berjalan pada port {$konfigurasi['port']}\\n\";"),
            ("Fungsi & Type Hinting", "<?php\ndeclare(strict_types=1);\n\nfunction hitungRataRata(array $nilai): float {\n    if (empty($nilai)) return 0.0;\n    return array_sum($nilai) / count($nilai);\n}\n$skor = [85, 90, 78, 92, 88];\necho 'Rata-rata: ' . hitungRataRata($skor);"),
            ("Algoritma: Binary Search", "<?php\nfunction binarySearch(array $arr, int $target): int {\n    $low = 0;\n    $high = count($arr) - 1;\n    while ($low <= $high) {\n        $mid = intdiv($low + $high, 2);\n        if ($arr[$mid] === $target) return $mid;\n        if ($arr[$mid] < $target) $low = $mid + 1;\n        else $high = $mid - 1;\n    }\n    return -1;\n}")
        ]
    },
    "ruby": {
        "name": "Ruby", "category": "Web & General", "ext": "rb",
        "intro": "Ruby adalah bahasa dinamis berorientasi objek murni yang mengutamakan kesederhanaan dan produktivitas pengembang.",
        "lessons": [
            ("Sintaks & Blocks", "nama = 'Adara AI'\nversi = 2.0\nputs \"Menjalankan #{nama} v#{versi}\"\n\n5.times do |i|\n  puts \"Iterasi ke-#{i + 1}\"\nend"),
            ("Algoritma: Palindrom & Fibonacci", "def palindrome?(teks)\n  clean = teks.downcase.gsub(/[^a-z0-9]/, '')\n  clean == clean.reverse\nend\n\ndef fibonacci(n)\n  return n if n <= 1\n  a, b = 0, 1\n  (2..n).each { a, b = b, a + b }\n  b\nend\nputs fibonacci(10)")
        ]
    },
    "html": {
        "name": "HTML", "category": "Web & General", "ext": "html",
        "intro": "HTML5 adalah bahasa markup standar untuk menstrukturkan dokumen dan konten pada World Wide Web.",
        "lessons": [
            ("Struktur Dokumen Standar", "<!DOCTYPE html>\n<html lang=\"id\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>Adara AI Dashboard</title>\n</head>\n<body>\n  <header>\n    <h1>Sistem Monitoring UH-0</h1>\n  </header>\n  <main>\n    <p>Status: Aktif Membaca 80 Bahasa</p>\n  </main>\n</body>\n</html>")
        ]
    },
    "css": {
        "name": "CSS", "category": "Web & General", "ext": "css",
        "intro": "CSS3 adalah bahasa stylesheet untuk mengatur presentasi, tata letak visual, dan responsivitas halaman web.",
        "lessons": [
            ("Flexbox & Grid Modern", ":root {\n  --primary: #4f46e5;\n  --bg-dark: #0f172a;\n  --text-light: #f8fafc;\n}\n.container {\n  display: flex;\n  flex-direction: column;\n  gap: 1.5rem;\n  padding: 2rem;\n  background-color: var(--bg-dark);\n  color: var(--text-light);\n}\n.card-grid {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));\n  gap: 1rem;\n}")
        ]
    },
    "svelte": {
        "name": "Svelte", "category": "Web & General", "ext": "svelte",
        "intro": "Svelte adalah compiler framework UI modern yang mengkompilasi kode deklaratif menjadi Vanilla JS tanpa Virtual DOM overhead.",
        "lessons": [
            ("Komponen Reaktif", "<script>\n  export let judul = 'Adara AI';\n  let hitungan = 0;\n  $: ganda = hitungan * 2;\n  function tambah() { hitungan += 1; }\n</script>\n<main>\n  <h2>{judul}</h2>\n  <button on:click={tambah}>Klik ({hitungan}) | Ganda: {ganda}</button>\n</main>")
        ]
    },
    "vue": {
        "name": "Vue", "category": "Web & General", "ext": "vue",
        "intro": "Vue.js adalah framework progresif dengan Composition API untuk membangun antarmuka web interaktif.",
        "lessons": [
            ("Composition API (Vue 3)", "<script setup>\nimport { ref, computed } from 'vue';\nconst counter = ref(0);\nconst kuadrat = computed(() => counter.value * counter.value);\nfunction increment() { counter.value++; }\n</script>\n<template>\n  <div class=\"box\">\n    <p>Nilai: {{ counter }} (Kuadrat: {{ kuadrat }})</p>\n    <button @click=\"increment\">Tambah</button>\n  </div>\n</template>")
        ]
    },
    "hack": {
        "name": "Hack", "category": "Web & General", "ext": "hh",
        "intro": "Hack adalah bahasa pemrograman berorientasi objek untuk HipHop Virtual Machine (HHVM) yang menggabungkan kecepatan PHP dengan static typing.",
        "lessons": [
            ("Sintaks Strict & Generics", "<?hh\n<<__EntryPoint>>\nasync function mainAsync(): Awaitable<void> {\n  $data = vec[10, 20, 30];\n  $sum = 0;\n  foreach ($data as $val) {\n    $sum += $val;\n  }\n  echo \"Total: {$sum}\\n\";\n}")
        ]
    },

    # ==========================================
    # KATEGORI 2: SYSTEMS & LOW-LEVEL (10 BAHASA)
    # ==========================================
    "c": {
        "name": "C", "category": "Systems & Low-level", "ext": "c",
        "intro": "C adalah bahasa pemrograman sistem imperatif terkompilasi yang memberikan kontrol perangkat keras langsung dan alokasi memori manual.",
        "lessons": [
            ("Sintaks Dasar & Pointer", "#include <stdio.h>\n\nvoid tukar(int *a, int *b) {\n    int temp = *a;\n    *a = *b;\n    *b = temp;\n}\n\nint main() {\n    int x = 10, y = 20;\n    tukar(&x, &y);\n    printf(\"Hasil tukar: x=%d, y=%d\\n\", x, y);\n    return 0;\n}"),
            ("Algoritma: Binary Search", "#include <stdio.h>\n\nint binary_search(const int arr[], int size, int target) {\n    int low = 0, high = size - 1;\n    while (low <= high) {\n        int mid = low + (high - low) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}\n\nint main() {\n    int data[] = {1, 3, 5, 7, 9, 11};\n    int idx = binary_search(data, 6, 7);\n    printf(\"Index: %d\\n\", idx);\n    return 0;\n}"),
            ("Algoritma: GCD Euclid", "#include <stdio.h>\n\nint gcd(int a, int b) {\n    while (b != 0) {\n        int temp = b;\n        b = a % b;\n        a = temp;\n    }\n    return a;\n}")
        ]
    },
    "cpp": {
        "name": "C++", "category": "Systems & Low-level", "ext": "cpp",
        "intro": "C++ adalah bahasa sistem berkinerja tinggi dengan abstraksi nol biaya, pemrograman generik (template), dan OOP modern (C++17/20).",
        "lessons": [
            ("STL Vector & Algorithm", "#include <iostream>\n#include <vector>\n#include <algorithm>\n\nint main() {\n    std::vector<int> nums = {42, 13, 88, 25, 7};\n    std::sort(nums.begin(), nums.end());\n    for (const auto& n : nums) {\n        std::cout << n << \" \";\n    }\n    std::cout << \"\\n\";\n    return 0;\n}"),
            ("Algoritma: Binary Search Modern", "#include <iostream>\n#include <vector>\n\nint binary_search(const std::vector<int>& arr, int target) {\n    int low = 0, high = static_cast<int>(arr.size()) - 1;\n    while (low <= high) {\n        int mid = low + (high - low) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}")
        ]
    },
    "rust": {
        "name": "Rust", "category": "Systems & Low-level", "ext": "rs",
        "intro": "Rust adalah bahasa sistem modern yang menjamin keamanan memori tanpa garbage collector melalui sistem ownership, borrowing, dan lifetimes.",
        "lessons": [
            ("Ownership & Borrowing", "fn hitung_panjang(s: &String) -> usize {\n    s.len()\n}\n\nfn main() {\n    let nama = String::from(\"Adara AI\");\n    let len = hitung_panjang(&nama);\n    println!(\"Panjang '{}': {}\", nama, len);\n}"),
            ("Algoritma: Binary Search", "fn binary_search(arr: &[i32], target: i32) -> Option<usize> {\n    let mut low = 0;\n    let mut high = arr.len();\n    while low < high {\n        let mid = low + (high - low) / 2;\n        if arr[mid] == target {\n            return Some(mid);\n        } else if arr[mid] < target {\n            low = mid + 1;\n        } else {\n            high = mid;\n        }\n    }\n    None\n}"),
            ("Pattern Matching & Result", "fn bagi(a: f64, b: f64) -> Result<f64, String> {\n    if b == 0.0 {\n        Err(String::from(\"Pembagian dengan nol!\"))\n    } else {\n        Ok(a / b)\n    }\n}")
        ]
    },
    "go": {
        "name": "Go", "category": "Systems & Low-level", "ext": "go",
        "intro": "Go (Golang) adalah bahasa terkompilasi dari Google yang dirancang untuk kesederhanaan, konkurensi efisien (goroutines), dan infrastruktur backend cloud.",
        "lessons": [
            ("Struct & Error Handling", "package main\nimport (\n    \"errors\"\n    \"fmt\"\n)\nfunc Bagi(a, b float64) (float64, error) {\n    if b == 0 {\n        return 0, errors.New(\"pembagian dengan nol\")\n    }\n    return a / b, nil\n}\nfunc main() {\n    hasil, err := Bagi(10, 2)\n    if err != nil {\n        fmt.Println(\"Error:\", err)\n        return\n    }\n    fmt.Println(\"Hasil:\", hasil)\n}"),
            ("Algoritma: Binary Search", "package main\n\nfunc BinarySearch(arr []int, target int) int {\n    low, high := 0, len(arr)-1\n    for low <= high {\n        mid := (low + high) / 2\n        if arr[mid] == target {\n            return mid\n        } else if arr[mid] < target {\n            low = mid + 1\n        } else {\n            high = mid - 1\n        }\n    }\n    return -1\n}")
        ]
    },
    "zig": {
        "name": "Zig", "category": "Systems & Low-level", "ext": "zig",
        "intro": "Zig adalah bahasa pemrograman sistem tujuan umum yang menggantikan C dengan fitur comptime, penanganan memori eksplisit, dan ketiadaan macro tersembunyi.",
        "lessons": [
            ("Sintaks Dasar & Defer", "const std = @import(\"std\");\npub fn main() !void {\n    const stdout = std.io.getStdOut().writer();\n    try stdout.print(\"Halo dari Adara di Zig!\\n\", .{});\n}"),
            ("Fungsi & Slice", "pub fn binarySearch(arr: []const i32, target: i32) ?usize {\n    var low: usize = 0;\n    var high: usize = arr.len;\n    while (low < high) {\n        const mid = low + (high - low) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) low = mid + 1;\n        else high = mid;\n    }\n    return null;\n}")
        ]
    },
    "d": {
        "name": "D", "category": "Systems & Low-level", "ext": "d",
        "intro": "D adalah bahasa multi-paradigma tingkat tinggi yang menggabungkan kemudahan sintaks Python dengan efisiensi eksekusi C++.",
        "lessons": [
            ("Fungsi & Arrays", "import std.stdio;\n\nint gcd(int a, int b) {\n    while (b != 0) {\n        int temp = b;\n        b = a % b;\n        a = temp;\n    }\n    return a;\n}\n\nvoid main() {\n    writeln(\"GCD(48, 18) = \", gcd(48, 18));\n}")
        ]
    },
    "nim": {
        "name": "Nim", "category": "Systems & Low-level", "ext": "nim",
        "intro": "Nim adalah bahasa sistem dengan sintaks bersih seperti Python yang dikompilasi ke C, C++, atau JavaScript dengan performa tinggi.",
        "lessons": [
            ("Prosedur & Kontrol Alur", "proc fibonacci(n: int): int =\n  if n <= 1: return n\n  var a = 0\n  var b = 1\n  for _ in 2..n:\n    let temp = a + b\n    a = b\n    b = temp\n  return b\n\necho \"Fibonacci 10: \", fibonacci(10)")
        ]
    },
    "v": {
        "name": "V", "category": "Systems & Low-level", "ext": "v",
        "intro": "V (Vlang) adalah bahasa terkompilasi yang sangat cepat, aman, dan mudah dipelajari dengan waktu kompilasi instan.",
        "lessons": [
            ("Fungsi & Immutability", "fn sum_array(arr []int) int {\n    mut total := 0\n    for n in arr {\n        total += n\n    }\n    return total\n}\n\nfn main() {\n    nums := [10, 20, 30, 40]\n    println('Total: ${sum_array(nums)}')\n}")
        ]
    },
    "assembly": {
        "name": "Assembly (x86_64)", "category": "Systems & Low-level", "ext": "asm",
        "intro": "Assembly adalah bahasa tingkat paling rendah yang memetakan instruksi mnemonik langsung ke kode biner prosesor arsitektur target.",
        "lessons": [
            ("Syscall Write & Exit (x86_64)", "section .data\n    msg db 'Halo Dunia x86_64', 0xA\n    len equ $ - msg\n\nsection .text\n    global _start\n\n_start:\n    mov rax, 1          ; syscall: sys_write\n    mov rdi, 1          ; fd: stdout\n    mov rsi, msg        ; buffer\n    mov rdx, len        ; count\n    syscall\n\n    mov rax, 60         ; syscall: sys_exit\n    xor rdi, rdi        ; exit code: 0\n    syscall")
        ]
    },
    "wat": {
        "name": "WebAssembly Text (WAT)", "category": "Systems & Low-level", "ext": "wat",
        "intro": "WAT adalah representasi teks S-expression dari WebAssembly binary format yang berjalan di sandbox browser maupun server (WASI).",
        "lessons": [
            ("Fungsi Tambah Sederhana", "(module\n  (func $add (param $a i32) (param $b i32) (result i32)\n    local.get $a\n    local.get $b\n    i32.add\n  )\n  (export \"add\" (func $add))\n)")
        ]
    },

    # ==========================================
    # KATEGORI 3: ENTERPRISE & JVM/CLR (10 BAHASA)
    # ==========================================
    "java": {
        "name": "Java", "category": "Enterprise & OOP", "ext": "java",
        "intro": "Java adalah bahasa berbasis kelas dan objek yang berjalan di atas Java Virtual Machine (JVM) dengan prinsip 'Write Once, Run Anywhere'.",
        "lessons": [
            ("Class & Binary Search", "public class Main {\n    public static int binarySearch(int[] arr, int target) {\n        int low = 0, high = arr.length - 1;\n        while (low <= high) {\n            int mid = (low + high) / 2;\n            if (arr[mid] == target) return mid;\n            if (arr[mid] < target) low = mid + 1;\n            else high = mid - 1;\n        }\n        return -1;\n    }\n    public static void main(String[] args) {\n        int[] nums = {2, 4, 6, 8, 10};\n        System.out.println(\"Index: \" + binarySearch(nums, 8));\n    }\n}")
        ]
    },
    "kotlin": {
        "name": "Kotlin", "category": "Enterprise & OOP", "ext": "kt",
        "intro": "Kotlin adalah bahasa modern berorientasi objek dan fungsional di atas JVM yang menjadi bahasa resmi pengembangan aplikasi Android.",
        "lessons": [
            ("Null Safety & Data Class", "data class User(val id: Int, val name: String, val email: String?)\n\nfun greetUser(user: User): String {\n    val mail = user.email ?: \"tidak ada email\"\n    return \"Halo ${user.name}, email: $mail\"\n}\n\nfun main() {\n    val u = User(1, \"Adara\", null)\n    println(greetUser(u))\n}")
        ]
    },
    "scala": {
        "name": "Scala", "category": "Enterprise & OOP", "ext": "scala",
        "intro": "Scala menggabungkan pemrograman berorientasi objek dan fungsional murni pada ekosistem JVM untuk komputasi terdistribusi (Apache Spark).",
        "lessons": [
            ("Pattern Matching & Immutability", "object Main extends App {\n  def deskripsikan(x: Any): String = x match {\n    case 1 => \"Satu\"\n    case \"halo\" => \"Salam\"\n    case true => \"Kebenaran\"\n    case _ => \"Lainnya\"\n  }\n  println(deskripsikan(1))\n}")
        ]
    },
    "groovy": {
        "name": "Groovy", "category": "Enterprise & OOP", "ext": "groovy",
        "intro": "Apache Groovy adalah bahasa dinamis berbasis JVM yang mendukung sintaks ringkas dan banyak digunakan pada automation build Gradle/Jenkins.",
        "lessons": [
            ("Closures & List Manipulation", "def angka = [1, 2, 3, 4, 5]\ndef genapKuadrat = angka.findAll { it % 2 == 0 }.collect { it * it }\nprintln \"Hasil: ${genapKuadrat}\"")
        ]
    },
    "csharp": {
        "name": "C#", "category": "Enterprise & OOP", "ext": "cs",
        "intro": "C# adalah bahasa modern berorientasi objek yang kuat dan elegan dari Microsoft pada ekosistem .NET untuk backend, desktop, dan Unity game engine.",
        "lessons": [
            ("LINQ & Binary Search", "using System;\nusing System.Linq;\n\nclass Program {\n    static int BinarySearch(int[] arr, int target) {\n        int low = 0, high = arr.Length - 1;\n        while (low <= high) {\n            int mid = (low + high) / 2;\n            if (arr[mid] == target) return mid;\n            if (arr[mid] < target) low = mid + 1;\n            else high = mid - 1;\n        }\n        return -1;\n    }\n    static void Main() {\n        int[] data = { 1, 3, 5, 7, 9 };\n        Console.WriteLine($\"Posisi: {BinarySearch(data, 7)}\");\n    }\n}")
        ]
    },
    "fsharp": {
        "name": "F#", "category": "Enterprise & OOP", "ext": "fs",
        "intro": "F# adalah bahasa fungsional pertama pada platform .NET dengan penekanan pada immutability, pattern matching, dan pipelines.",
        "lessons": [
            ("Pipeline Operator (|>) & Recursion", "let rec fib n =\n    match n with\n    | 0 -> 0\n    | 1 -> 1\n    | _ -> fib (n - 1) + fib (n - 2)\n\n[1..10] |> List.map fib |> printfn \"%A\"")
        ]
    },
    "vbnet": {
        "name": "VB.NET", "category": "Enterprise & OOP", "ext": "vb",
        "intro": "Visual Basic .NET adalah bahasa berorientasi objek berbasis event pada .NET framework dengan sintaks mirip bahasa manusia.",
        "lessons": [
            ("Sub & Function", "Module Program\n    Function Tambah(a As Integer, b As Integer) As Integer\n        Return a + b\n    End Function\n    Sub Main()\n        Console.WriteLine(\"Hasil: \" & Tambah(15, 25))\n    End Sub\nEnd Module")
        ]
    },
    "apex": {
        "name": "Apex", "category": "Enterprise & OOP", "ext": "cls",
        "intro": "Apex adalah bahasa berorientasi objek mirip Java yang dieksekusi pada platform cloud server Salesforce CRM.",
        "lessons": [
            ("Apex Class & SOQL", "public class ContactService {\n    public static List<Contact> getActiveContacts() {\n        return [SELECT Id, FirstName, LastName, Email FROM Contact WHERE IsDeleted = false LIMIT 50];\n    }\n}")
        ]
    },
    "abap": {
        "name": "ABAP", "category": "Enterprise & OOP", "ext": "abap",
        "intro": "ABAP (Advanced Business Application Programming) adalah bahasa pemrograman tingkat tinggi untuk pengembangan sistem enterprise SAP ERP.",
        "lessons": [
            ("Data Declaration & Loop", "REPORT ZADARA_DEMO.\nDATA: lv_nama TYPE string VALUE 'Adara',\n      lv_angka TYPE i VALUE 42.\nWRITE: / 'Halo', lv_nama, 'Nomor:', lv_angka.")
        ]
    },
    "cobol": {
        "name": "COBOL", "category": "Enterprise & OOP", "ext": "cbl",
        "intro": "COBOL adalah bahasa legendaris yang masih menopang sistem perbankan dan transaksi mainframe global dengan struktur divisi formal.",
        "lessons": [
            ("Divisi Program & Display", "       IDENTIFICATION DIVISION.\n       PROGRAM-ID. HELLO-ADARA.\n       DATA DIVISION.\n       WORKING-STORAGE SECTION.\n       01 WS-NAMA PIC A(10) VALUE 'ADARA AI'.\n       PROCEDURE DIVISION.\n           DISPLAY 'SELAMAT DATANG: ' WS-NAMA.\n           STOP RUN.")
        ]
    },

    # ==========================================
    # KATEGORI 4: MOBILE & SCRIPTING (10 BAHASA)
    # ==========================================
    "swift": {
        "name": "Swift", "category": "Mobile & Scripting", "ext": "swift",
        "intro": "Swift adalah bahasa modern Apple yang cepat, aman, dan ekspresif untuk ekosistem iOS, macOS, watchOS, dan tvOS.",
        "lessons": [
            ("Struct & Guard Let", "struct Pengguna {\n    let id: Int\n    let nama: String\n    let email: String?\n}\nfunc periksaEmail(p: Pengguna) {\n    guard let email = p.email else {\n        print(\"Email tidak tersedia\")\n        return\n    }\n    print(\"Email pengguna: \\(email)\")\n}")
        ]
    },
    "dart": {
        "name": "Dart", "category": "Mobile & Scripting", "ext": "dart",
        "intro": "Dart adalah bahasa yang dioptimalkan untuk UI dari Google, digunakan sebagai mesin utama framework Flutter multiplatform.",
        "lessons": [
            ("Class & Asynchronous Future", "Future<String> ambilDataAsync() async {\n  await Future.delayed(Duration(milliseconds: 100));\n  return 'Data Berhasil Diambil';\n}\nvoid main() async {\n  final res = await ambilDataAsync();\n  print(res);\n}")
        ]
    },
    "lua": {
        "name": "Lua", "category": "Mobile & Scripting", "ext": "lua",
        "intro": "Lua adalah bahasa scripting ringan, cepat, dan mudah disematkan (embeddable) yang menjadi standar industri game scripting.",
        "lessons": [
            ("Table & Fibonacci", "function fibonacci(n)\n    if n <= 1 then return n end\n    local a, b = 0, 1\n    for i = 2, n do\n        a, b = b, a + b\n    end\n    return b\nend\nprint('Fibonacci 10: ' .. fibonacci(10))")
        ]
    },
    "gdscript": {
        "name": "GDScript", "category": "Mobile & Scripting", "ext": "gd",
        "intro": "GDScript adalah bahasa mirip Python yang terintegrasi secara khusus untuk pengembangan game 2D/3D pada Godot Engine.",
        "lessons": [
            ("Extends Node & Signals", "extends Node2D\n\nvar kecepatan: float = 250.0\nsignal pemain_kalah\n\nfunc _ready():\n    print(\"Node game Adara siap dimainkan!\")")
        ]
    },
    "actionscript": {
        "name": "ActionScript", "category": "Mobile & Scripting", "ext": "as",
        "intro": "ActionScript adalah bahasa berorientasi objek turunan ECMAScript yang dahulu mentenagai platform Adobe Flash dan AIR.",
        "lessons": [
            ("Package & Event", "package {\n    import flash.display.Sprite;\n    public class Main extends Sprite {\n        public function Main() {\n            trace(\"Adara Flash Engine diinisialisasi\");\n        }\n    }\n}")
        ]
    },
    "coffeescript": {
        "name": "CoffeeScript", "category": "Mobile & Scripting", "ext": "coffee",
        "intro": "CoffeeScript adalah dialek ringkas yang mentranspilasi kode berformat bersih ala Ruby/Python menjadi JavaScript standar.",
        "lessons": [
            ("Arrow Function & Splats", "hitungTotal = (angka...) ->\n  total = 0\n  total += n for n in angka\n  total\nconsole.log hitungTotal 10, 20, 30")
        ]
    },
    "tcl": {
        "name": "Tcl", "category": "Mobile & Scripting", "ext": "tcl",
        "intro": "Tcl (Tool Command Language) adalah bahasa scripting dinamis yang sangat fleksibel dan populer untuk otomatisasi EDA dan embedded testing.",
        "lessons": [
            ("Proc & Expr", "proc tambah {a b} {\n    return [expr {$a + $b}]\n}\nputs \"Hasil: [tambah 10 25]\"")
        ]
    },
    "smalltalk": {
        "name": "Smalltalk", "category": "Mobile & Scripting", "ext": "st",
        "intro": "Smalltalk adalah bahasa pelopor berorientasi objek murni di mana segalanya adalah objek dan komunikasi dilakukan via pertukaran pesan.",
        "lessons": [
            ("Message Sending", "Transcript show: 'Halo dari Adara di Smalltalk!'; cr.")
        ]
    },
    "objc": {
        "name": "Objective-C", "category": "Mobile & Scripting", "ext": "m",
        "intro": "Objective-C adalah ekstensi berorientasi objek dinamis dari bahasa C yang dahulu menjadi pondasi ekosistem Cocoa di Mac OS X dan iOS.",
        "lessons": [
            ("Interface & Message Syntax", "#import <Foundation/Foundation.h>\nint main(int argc, const char * argv[]) {\n    @autoreleasepool {\n        NSLog(@\"Halo dari Objective-C Adara\");\n    }\n    return 0;\n}")
        ]
    },
    "crystal": {
        "name": "Crystal", "category": "Mobile & Scripting", "ext": "cr",
        "intro": "Crystal memadukan sintaks elegan Ruby dengan kecepatan dan pemeriksaan tipe statis kompilator C (LLVM).",
        "lessons": [
            ("Static Typing & Fiber", "def fib(n : Int32) : Int64\n  return n.to_i64 if n <= 1\n  a, b = 0_i64, 1_i64\n  (2..n).each { a, b = b, a + b }\n  b\nend\nputs fib(10)")
        ]
    },

    # ==========================================
    # KATEGORI 5: DATA & ANALYTICS (10 BAHASA)
    # ==========================================
    "sql": {
        "name": "SQL", "category": "Data & Analytics", "ext": "sql",
        "intro": "SQL adalah bahasa deklaratif standar untuk mengelola, memanipulasi, dan meminta data pada sistem database relasional (RDBMS).",
        "lessons": [
            ("Query Agregasi & Window Function", "SELECT \n    kategori,\n    COUNT(*) AS total_produk,\n    AVG(harga) AS rata_harga,\n    DENSE_RANK() OVER (ORDER BY AVG(harga) DESC) as ranking\nFROM tabel_produk\nWHERE status = 'aktif'\nGROUP BY kategori\nHAVING COUNT(*) > 5\nORDER BY ranking ASC;")
        ]
    },
    "plsql": {
        "name": "PL/SQL", "category": "Data & Analytics", "ext": "pls",
        "intro": "PL/SQL adalah ekstensi prosedural dari SQL yang dirancang oleh Oracle untuk eksekusi logika bisnis kompleks langsung di database.",
        "lessons": [
            ("Blok Prosedural & Exception", "DECLARE\n    v_nama VARCHAR2(50);\n    v_gaji NUMBER := 5000000;\nBEGIN\n    SELECT nama INTO v_nama FROM karyawan WHERE id = 101;\n    DBMS_OUTPUT.PUT_LINE('Karyawan: ' || v_nama || ' Gaji: ' || v_gaji);\nEXCEPTION\n    WHEN NO_DATA_FOUND THEN\n        DBMS_OUTPUT.PUT_LINE('Data tidak ditemukan');\nEND;")
        ]
    },
    "tsql": {
        "name": "T-SQL", "category": "Data & Analytics", "ext": "tsql",
        "intro": "Transact-SQL adalah dialek milik Microsoft untuk SQL Server yang menambahkan variabel, loop, percabangan, dan stored procedures.",
        "lessons": [
            ("CTE & Procedure", "WITH PenjualanBulanan AS (\n    SELECT MONTH(tanggal) AS bulan, SUM(total) AS omset\n    FROM faktur\n    GROUP BY MONTH(tanggal)\n)\nSELECT bulan, omset FROM PenjualanBulanan WHERE omset > 10000000;")
        ]
    },
    "r": {
        "name": "R", "category": "Data & Analytics", "ext": "r",
        "intro": "R adalah bahasa dan lingkungan komputasi statistik, visualisasi grafik, dan analisis data ilmiah yang digunakan para peneliti.",
        "lessons": [
            ("Dataframe & Vector Ops", "vektor_angka <- c(12, 15, 23, 40, 55)\nmean_val <- mean(vektor_angka)\nsd_val <- sd(vektor_angka)\ncat('Rata-rata:', mean_val, 'Standar Deviasi:', sd_val, '\\n')")
        ]
    },
    "julia": {
        "name": "Julia", "category": "Data & Analytics", "ext": "jl",
        "intro": "Julia adalah bahasa komputasi ilmiah berkecepatan tinggi yang menyatukan kemudahan Python dengan performa kompilasi JIT mendekati C.",
        "lessons": [
            ("Multiple Dispatch & Matrix", "function hitung_matriks(A::Matrix{Float64}, v::Vector{Float64})\n    return A * v\nend\nprintln(\"Julia siap untuk aljabar linier performa tinggi\")")
        ]
    },
    "matlab": {
        "name": "MATLAB", "category": "Data & Analytics", "ext": "m",
        "intro": "MATLAB adalah lingkungan komputasi numerik dan pemrograman matriks untuk teknik, sains, dan simulasi fisika.",
        "lessons": [
            ("Operasi Matriks", "A = [1, 2; 3, 4];\nB = [5, 6; 7, 8];\nC = A * B;\ndisp('Hasil perkalian matriks:');\ndisp(C);")
        ]
    },
    "sas": {
        "name": "SAS", "category": "Data & Analytics", "ext": "sas",
        "intro": "SAS adalah sistem piranti lunak terintegrasi untuk analisis lanjutan, intelijen bisnis, dan manajemen data analitik skala besar.",
        "lessons": [
            ("DATA Step & PROC MEANS", "DATA data_karyawan;\n    INPUT nama $ gaji umur;\n    DATALINES;\nBudi 5000000 28\nSiti 7500000 32\n;\nRUN;\nPROC MEANS DATA=data_karyawan;\nRUN;")
        ]
    },
    "graphql": {
        "name": "GraphQL", "category": "Data & Analytics", "ext": "graphql",
        "intro": "GraphQL adalah bahasa kueri untuk API yang memungkinkan klien meminta secara persis data yang mereka butuhkan tanpa overfetching.",
        "lessons": [
            ("Schema & Query", "type User {\n  id: ID!\n  name: String!\n  email: String!\n  posts(limit: Int): [Post!]!\n}\nquery GetUserProfile($id: ID!) {\n  user(id: $id) {\n    name\n    email\n    posts(limit: 3) {\n      title\n    }\n  }\n}")
        ]
    },
    "json": {
        "name": "JSON", "category": "Data & Analytics", "ext": "json",
        "intro": "JSON (JavaScript Object Notation) adalah format pertukaran data berbasis teks ringan yang menjadi standar de-facto komunikasi web API.",
        "lessons": [
            ("Format Struktur Terstruktur", "{\n  \"model\": \"UH-0 Adara\",\n  \"languages_supported\": 80,\n  \"status\": \"reading_phase\",\n  \"metrics\": {\n    \"loss\": 0.045,\n    \"gpu\": \"RTX 4090\"\n  }\n}")
        ]
    },
    "yaml": {
        "name": "YAML", "category": "Data & Analytics", "ext": "yaml",
        "intro": "YAML adalah format serialisasi data yang sangat mudah dibaca manusia, menjadi standar konfigurasi Kubernetes dan pipeline CI/CD.",
        "lessons": [
            ("Konfigurasi Deployment", "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: adara-worker\nspec:\n  replicas: 3\n  template:\n    spec:\n      containers:\n      - name: uh-zero\n        image: uhlabs/adara:latest\n        ports:\n        - containerPort: 8080")
        ]
    },

    # ==========================================
    # KATEGORI 6: FUNCTIONAL & LOGIC (10 BAHASA)
    # ==========================================
    "haskell": {
        "name": "Haskell", "category": "Functional & Logic", "ext": "hs",
        "intro": "Haskell adalah bahasa murni fungsional, beralasan matematis dengan sistem tipe statis kuat, evaluasi lambat (lazy evaluation), dan monad.",
        "lessons": [
            ("Fungsi Murni & Quicksort", "quicksort :: (Ord a) => [a] -> [a]\nquicksort [] = []\nquicksort (x:xs) =\n    let smallerSorted = quicksort [a | a <- xs, a <= x]\n        biggerSorted  = quicksort [a | a <- xs, a > x]\n    in  smallerSorted ++ [x] ++ biggerSorted\n\nmain = print (quicksort [10, 2, 5, 3, 1, 6, 7, 4])")
        ]
    },
    "elixir": {
        "name": "Elixir", "category": "Functional & Logic", "ext": "ex",
        "intro": "Elixir berjalan di atas BEAM Erlang VM untuk membangun aplikasi terdistribusi, toleran kesalahan, dan konkuren tinggi dengan pipe operator (| >).",
        "lessons": [
            ("Pipe Operator & Pattern Matching", "defmodule Hitung do\n  def proses_angka(list) do\n    list\n    |> Enum.filter(&(rem(&1, 2) == 0))\n    |> Enum.map(&(&1 * &1))\n    |> Enum.sum()\n  end\nend\nIO.puts Hitung.proses_angka([1, 2, 3, 4, 5, 6])")
        ]
    },
    "clojure": {
        "name": "Clojure", "category": "Functional & Logic", "ext": "clj",
        "intro": "Clojure adalah dialek Lisp modern pada JVM yang menekankan immutability dan pemrograman fungsional murni.",
        "lessons": [
            ("S-Expression & Map", "(defn kuadrat-genap [angka]\n  (->> angka\n       (filter even?)\n       (map #(* % %))\n       (reduce +)))\n\n(println (kuadrat-genap [1 2 3 4 5 6]))")
        ]
    },
    "erlang": {
        "name": "Erlang", "category": "Functional & Logic", "ext": "erl",
        "intro": "Erlang adalah bahasa komputasi terdistribusi dan model Actor yang dirancang oleh Ericsson untuk keandalan 'nine nines' sistem telekomunikasi.",
        "lessons": [
            ("Modul & Rekursi", "-module(faktorial).\n-export([hitung/1]).\nhitung(0) -> 1;\nhitung(N) when N > 0 -> N * hitung(N - 1).")
        ]
    },
    "ocaml": {
        "name": "OCaml", "category": "Functional & Logic", "ext": "ml",
        "intro": "OCaml adalah implementasi utama bahasa Caml yang menggabungkan efisiensi kompilasi native dengan sistem tipe statis inferred.",
        "lessons": [
            ("Pattern Matching & Recursion", "let rec gcd a b =\n  if b = 0 then a\n  else gcd b (a mod b);;\n\nlet () = Printf.printf \"GCD: %d\\n\" (gcd 48 18);;")
        ]
    },
    "scheme": {
        "name": "Scheme", "category": "Functional & Logic", "ext": "scm",
        "intro": "Scheme adalah dialek minimalis dari Lisp yang terkenal karena keindahan matematika rekursinya dan lexical scoping murni.",
        "lessons": [
            ("Fungsi Rekursif", "(define (faktorial n)\n  (if (<= n 1)\n      1\n      (* n (faktorial (- n 1)))))\n(display (faktorial 5))")
        ]
    },
    "racket": {
        "name": "Racket", "category": "Functional & Logic", "ext": "rkt",
        "intro": "Racket adalah ekosistem bahasa keluarga Lisp yang kaya fitur untuk desain bahasa, riset, dan pemrograman fungsional.",
        "lessons": [
            ("#lang racket & Match", "#lang racket\n(define (fib n)\n  (match n\n    [0 0]\n    [1 1]\n    [_ (+ (fib (- n 1)) (fib (- n 2)))]))\n(println (fib 8))")
        ]
    },
    "commonlisp": {
        "name": "Common Lisp", "category": "Functional & Logic", "ext": "lisp",
        "intro": "Common Lisp adalah standar industri bahasa Lisp dengan sistem macro yang paling kuat di dunia pemrograman.",
        "lessons": [
            ("Defun & Loop", "(defun jumlah-kuadrat (lst)\n  (loop for x in lst\n        when (evenp x)\n        sum (* x x)))\n(format t \"Hasil: ~a~%\" (jumlah-kuadrat '(1 2 3 4 5 6)))")
        ]
    },
    "prolog": {
        "name": "Prolog", "category": "Functional & Logic", "ext": "pl",
        "intro": "Prolog adalah bahasa logika deklaratif di mana program didefinisikan sebagai relasi fakta, aturan, dan inferensi query.",
        "lessons": [
            ("Fakta & Aturan Logika", "orangtua(budi, ani).\norangtua(ani, charlie).\nkakek(X, Z) :- orangtua(X, Y), orangtua(Y, Z).\n% Query: ?- kakek(budi, charlie).")
        ]
    },
    "purescript": {
        "name": "PureScript", "category": "Functional & Logic", "ext": "purs",
        "intro": "PureScript adalah bahasa murni fungsional bertipe kuat yang mentranspilasi kode menjadi JavaScript yang sangat bersih.",
        "lessons": [
            ("Do Notation & Tipe", "module Main where\nimport Prelude\nimport Effect (Effect)\nimport Effect.Console (log)\n\nmain :: Effect Unit\nmain = log \"Halo dari PureScript Adara\"")
        ]
    },

    # ==========================================
    # KATEGORI 7: SHELL & DEVOPS (10 BAHASA)
    # ==========================================
    "bash": {
        "name": "Bash", "category": "Shell & DevOps", "ext": "sh",
        "intro": "Bash (Bourne Again SHell) adalah shell default Unix/Linux untuk otomatisasi perintah sistem, pipeline, dan administrasi server.",
        "lessons": [
            ("Fungsi & Looping", "#!/usr/bin/env bash\nset -euo pipefail\n\nperiksa_service() {\n    local nama_svc=\"$1\"\n    if pgrep -f \"$nama_svc\" > /dev/null; then\n        echo \"[OK] Service $nama_svc sedang berjalan\"\n    else\n        echo \"[ERR] Service $nama_svc mati\"\n    fi\n}\nperiksa_service \"python3\"")
        ]
    },
    "powershell": {
        "name": "PowerShell", "category": "Shell & DevOps", "ext": "ps1",
        "intro": "PowerShell adalah shell perintah berbasis objek dari Microsoft untuk administrasi sistem lintas platform (Windows, Linux, macOS).",
        "lessons": [
            ("Cmdlet Pipeline", "Get-Process | Where-Object { $_.CPU -gt 10 } | Select-Object ProcessName, Id, CPU | Sort-Object CPU -Descending")
        ]
    },
    "fish": {
        "name": "Fish", "category": "Shell & DevOps", "ext": "fish",
        "intro": "Fish (Friendly Interactive Shell) adalah shell modern cerdas dengan autosuggestion dan pewarnaan sintaks bawaan.",
        "lessons": [
            ("Fungsi Fish", "function salam\n    echo \"Selamat datang di Fish Shell, $argv!\"\nend\nsalam \"Adara\"")
        ]
    },
    "awk": {
        "name": "Awk", "category": "Shell & DevOps", "ext": "awk",
        "intro": "Awk adalah bahasa pemrosesan teks berorientasi pola baris/kolom yang sangat tangguh untuk memfilter dan mengekstrak log.",
        "lessons": [
            ("Pemrosesan Kolom & Akumulasi", "BEGIN { FS=\",\"; total=0 } \n$3 > 50 { total += $3; print $1, $3 }\nEND { print \"Total Akumulasi:\", total }")
        ]
    },
    "sed": {
        "name": "Sed", "category": "Shell & DevOps", "ext": "sed",
        "intro": "Sed (Stream Editor) adalah utilitas Unix untuk transformasi teks dan substitusi ekspresi reguler secara efisien pada aliran data.",
        "lessons": [
            ("Substitusi Pola", "# Mengganti kata lama menjadi kata baru pada setiap baris\ns/localhost/127.0.0.1/g\ns/^# //g")
        ]
    },
    "makefile": {
        "name": "Makefile", "category": "Shell & DevOps", "ext": "mk",
        "intro": "GNU Make mengotomatisasi kompilasi kode dan eksekusi tugas berdasarkan pelacakan dependensi file target.",
        "lessons": [
            ("Target & Recipe", ".PHONY: all build clean\nCC = gcc\nCFLAGS = -Wall -O2\n\nall: build\nbuild:\n\t$(CC) $(CFLAGS) -o program main.c\nclean:\n\trm -f program *.o")
        ]
    },
    "cmake": {
        "name": "CMake", "category": "Shell & DevOps", "ext": "cmake",
        "intro": "CMake adalah sistem pembuatan perangkat lunak lintas platform independen yang menghasilkan file build asli (Make/Ninja/VS).",
        "lessons": [
            ("CMakeLists Standar", "cmake_minimum_required(VERSION 3.16)\nproject(AdaraCore LANGUAGES CXX)\nset(CMAKE_CXX_STANDARD 20)\nadd_executable(adara_app src/main.cpp)")
        ]
    },
    "dockerfile": {
        "name": "Dockerfile", "category": "Shell & DevOps", "ext": "dockerfile",
        "intro": "Dockerfile mendefinisikan instruksi resep otomatis untuk membangun image kontainer Docker yang portabel dan terisolasi.",
        "lessons": [
            ("Multi-Stage Build Ringkas", "FROM python:3.11-slim AS builder\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD [\"python\", \"app.py\"]")
        ]
    },
    "toml": {
        "name": "TOML", "category": "Shell & DevOps", "ext": "toml",
        "intro": "TOML (Tom's Obvious Minimal Language) adalah format konfigurasi sederhana yang memetakan ke tabel hash secara presisi.",
        "lessons": [
            ("Konfigurasi Paket", "[package]\nname = \"uh-zero\"\nversion = \"2.0.0\"\nedition = \"2021\"\n\n[dependencies]\ntorch = \"2.6.0\"\ntransformers = \"4.49.0\"")
        ]
    },
    "zsh": {
        "name": "Zsh", "category": "Shell & DevOps", "ext": "zsh",
        "intro": "Zsh (Z Shell) adalah shell interaktif canggih yang kompatibel dengan Bash dan menyediakan kemampuan globbing dan script ekspansif.",
        "lessons": [
            ("Array & Parameter Expansion", "#!/usr/bin/env zsh\nlist=(satu dua tiga empat)\nfor item in $list; do\n    print -P \"Item: %F{green}$item%f\"\ndone")
        ]
    },

    # ==========================================
    # KATEGORI 8: SMART CONTRACTS & SPECIALIZED (10 BAHASA)
    # ==========================================
    "solidity": {
        "name": "Solidity", "category": "Smart Contracts & Specialized", "ext": "sol",
        "intro": "Solidity adalah bahasa berorientasi kontrak pintar untuk Ethereum Virtual Machine (EVM) yang menopang ekosistem Web3 dan DeFi.",
        "lessons": [
            ("Smart Contract ERC-20 Ringkas", "// SPDX-License-Identifier: MIT\npragma solidity ^0.8.20;\n\ncontract Tabungan {\n    mapping(address => uint256) public saldo;\n    event Deposit(address indexed pengirim, uint256 jumlah);\n\n    function simpan() external payable {\n        require(msg.value > 0, \"Jumlah harus lebih dari nol\");\n        saldo[msg.sender] += msg.value;\n        emit Deposit(msg.sender, msg.value);\n    }\n}")
        ]
    },
    "vyper": {
        "name": "Vyper", "category": "Smart Contracts & Specialized", "ext": "vy",
        "intro": "Vyper adalah bahasa smart contract mirip Python untuk EVM yang mengutamakan keamanan dan auditabilitas maksimal dengan menghilangkan rekursi.",
        "lessons": [
            ("Kontrak Aman", "# @version ^0.3.7\nsaldo: public(HashMap[address, uint256])\n\n@external\n@payable\ndef deposit():\n    assert msg.value > 0, \"Nilai harus positif\"\n    self.saldo[msg.sender] += msg.value")
        ]
    },
    "fortran": {
        "name": "Fortran (Modern)", "category": "Smart Contracts & Specialized", "ext": "f90",
        "intro": "Fortran (Formula Translation) adalah bahasa komputasi ilmiah dan fisika terkemuka untuk simulasi cuaca dan superkomputer paralel.",
        "lessons": [
            ("Modul & Aljabar Numerik", "program hitung_akar\n    implicit none\n    real(8) :: x, akar\n    x = 144.0_8\n    akar = sqrt(x)\n    print *, 'Akar dari ', x, ' adalah: ', akar\nend program hitung_akar")
        ]
    },
    "pascal": {
        "name": "Pascal / FreePascal", "category": "Smart Contracts & Specialized", "ext": "pas",
        "intro": "Pascal adalah bahasa terstruktur strongly-typed yang terkenal untuk pengajaran logika terstruktur dan pengembangan GUI via Lazarus.",
        "lessons": [
            ("Program Terstruktur", "program HaloAdara;\nvar\n    nama: string;\nbegin\n    nama := 'Adara AI';\n    writeln('Selamat datang: ', nama);\nend.")
        ]
    },
    "ada": {
        "name": "Ada", "category": "Smart Contracts & Specialized", "ext": "adb",
        "intro": "Ada adalah bahasa dengan keandalan sangat tinggi yang digunakan pada sistem avionik dirgantara, kereta cepat, dan pertahanan.",
        "lessons": [
            ("Prosedur & Package", "with Ada.Text_IO; use Ada.Text_IO;\nprocedure Halo_Ada is\nbegin\n   Put_Line (\"Sistem Kritis Terverifikasi Berjalan\");\nend Halo_Ada;")
        ]
    },
    "forth": {
        "name": "Forth", "category": "Smart Contracts & Specialized", "ext": "fth",
        "intro": "Forth adalah bahasa berorientasi tumpukan (stack-based) yang sangat ringkas, digunakan untuk bootloader dan perangkat keras tertanam.",
        "lessons": [
            ("Stack Operations", ": KUADRAT ( n -- n^2 )\n  DUP * ;\n\n5 KUADRAT . ( Output: 25 )")
        ]
    },
    "apl": {
        "name": "APL", "category": "Smart Contracts & Specialized", "ext": "apl",
        "intro": "APL menggunakan simbol matematika khusus yang sangat padat untuk memanipulasi larik multi-dimensi secara langsung tanpa loop ekspresif.",
        "lessons": [
            ("Operasi Array Monadik", "⍝ Menghitung rata-rata dari larik angka\n(+/÷≢) 10 20 30 40 50")
        ]
    },
    "elm": {
        "name": "Elm", "category": "Smart Contracts & Specialized", "ext": "elm",
        "intro": "Elm adalah bahasa fungsional murni untuk frontend yang menjamin nol runtime exception dalam produksi melalui arsitektur Model-Update-View.",
        "lessons": [
            ("The Elm Architecture", "module Main exposing (..)\nimport Browser\nimport Html exposing (Html, button, div, text)\nimport Html.Events exposing (onClick)\n\ntype Msg = Tambah | Kurang\nupdate msg model = case msg of\n  Tambah -> model + 1\n  Kurang -> model - 1")
        ]
    },
    "reasonml": {
        "name": "ReasonML", "category": "Smart Contracts & Specialized", "ext": "re",
        "intro": "ReasonML memberikan sintaks ramah JavaScript untuk sistem tipe dan ekosistem OCaml, populer untuk aplikasi React berskala aman.",
        "lessons": [
            ("Let Binding & Variant", "type status = | Aktif | Nonaktif;\nlet periksa = (s) => switch (s) {\n| Aktif => \"Sistem Menyala\"\n| Nonaktif => \"Sistem Mati\"\n};")
        ]
    },
    "vhdl": {
        "name": "VHDL", "category": "Smart Contracts & Specialized", "ext": "vhd",
        "intro": "VHDL adalah bahasa deskripsi perangkat keras (HDL) untuk mendesain dan mensimulasikan sirkuit digital pada chip FPGA dan ASIC.",
        "lessons": [
            ("Entity & Architecture Gerbang AND", "library IEEE;\nuse IEEE.STD_LOGIC_1164.ALL;\n\nentity GerbangAnd is\n    Port ( a : in  STD_LOGIC;\n           b : in  STD_LOGIC;\n           y : out STD_LOGIC );\nend GerbangAnd;\n\narchitecture Behavioral of GerbangAnd is\nbegin\n    y <= a and b;\nend Behavioral;")
        ]
    }
}



# Koleksi Dialog Tanya Jawab & Percakapan Cerdas (Conversational & Coding Q&A)
CONVERSATION_DIALOGUES: List[Dict[str, str]] = [
    {
        "user": "Halo, kamu siapa?",
        "assistant": "Halo! Saya adalah UH-0, asisten kecerdasan buatan dari ekosistem Adara AI yang dirancang untuk menguasai 80 bahasa pemrograman dunia nyata dan membantu Anda menulis, men-debug, serta memahami kode program secara efisien."
    },
    {
        "user": "Siapa namamu dan apa kemampuanmu?",
        "assistant": "Nama saya UH-0 (UH Labs Zero). Saya adalah model AI yang mampu memahami logika pemrograman, arsitektur software, dan penulisan sintaks bersih lintas 80 bahasa pemrograman, dari web modern, sistem low-level, hingga smart contract."
    },
    {
        "user": "Apa kabar?",
        "assistant": "Kabar saya sangat baik dan siap membantu Anda! Apakah ada proyek atau kode program yang ingin kita bahas atau selesaikan hari ini?"
    },
    {
        "user": "Terima kasih banyak atas bantuannya",
        "assistant": "Sama-sama! Senang bisa membantu Anda. Jika ada kendala koding atau pertanyaan lain di kemudian hari, jangan ragu untuk bertanya lagi ya."
    },
    {
        "user": "Bagaimana cara kerja rekursi dalam pemrograman?",
        "assistant": "Rekursi adalah teknik di mana sebuah fungsi memanggil dirinya sendiri untuk memecahkan masalah besar menjadi sub-masalah yang lebih kecil. Syarat mutlak rekursi yang aman adalah memiliki 'base case' (kondisi berhenti) agar tidak terjadi infinite loop atau stack overflow."
    },
    {
        "user": "Apa perbedaan compiler dan interpreter?",
        "assistant": "Compiler menerjemahkan seluruh kode program sekaligus menjadi bahasa mesin (biner) sebelum dieksekusi (contoh: C, C++, Rust, Go), menghasilkan eksekusi yang sangat cepat. Sedangkan Interpreter menerjemahkan dan mengeksekusi kode baris demi baris saat runtime (contoh: Python, JavaScript, Ruby)."
    },
    {
        "user": "Kenapa kode saya error index out of bounds?",
        "assistant": "Error 'index out of bounds' terjadi saat Anda mencoba mengakses elemen array atau list pada posisi index yang tidak ada (misalnya array hanya memiliki 5 elemen dengan index 0-4, namun Anda mencoba membaca index 5 atau lebih). Selalu periksa panjang array sebelum mengaksesnya."
    },
    {
        "user": "Apa itu API dan fungsinya?",
        "assistant": "API (Application Programming Interface) adalah jembatan atau antarmuka yang memungkinkan dua aplikasi atau sistem berbeda untuk saling berkomunikasi dan bertukar data secara terstruktur, biasanya menggunakan protokol HTTP dan format data JSON."
    },
    {
        "user": "Bisa bantu saya belajar coding?",
        "assistant": "Tentu saja! Saya bisa membantu Anda belajar dari dasar hingga tingkat lanjut. Anda ingin mulai dari bahasa pemrograman apa? Kita bisa mulai dari Python untuk pemula, JavaScript untuk web, atau Go dan Rust untuk sistem performa tinggi."
    },
    {
        "user": "Apa itu database relasional dan contohnya?",
        "assistant": "Database relasional (RDBMS) adalah sistem penyimpanan data dalam bentuk tabel-tabel terstruktur yang saling berelasi menggunakan baris dan kolom. Contohnya adalah PostgreSQL, MySQL, SQLite, dan MariaDB, yang dikelola menggunakan bahasa query SQL."
    },
    {
        "user": "Bagaimana cara membuat fungsi di Python?",
        "assistant": "Di Python, Anda membuat fungsi menggunakan kata kunci `def` diikuti nama fungsi, tanda kurung parameter, titik dua, dan blok kode terindentasi. Contoh:\n\ndef sapa(nama: str) -> str:\n    return f'Halo {nama}!'\n\nprint(sapa('Budi'))"
    },
    {
        "user": "Apa keunggulan bahasa Rust?",
        "assistant": "Keunggulan utama Rust adalah menjamin keamanan memori (memory safety) tanpa memerlukan garbage collector melalui sistem kepemilikan (ownership & borrowing) saat waktu kompilasi, sambil tetap menawarkan performa setara C dan C++."
    },
    {
        "user": "Kenapa kamu bisa menguasai 80 bahasa?",
        "assistant": "Saya dilatih menggunakan kurikulum terstruktur 80 bahasa pemrograman yang mencakup seluruh paradigma: imperatif, berorientasi objek, fungsional murni, hingga deklaratif, dipadukan dengan ratusan ribu dataset kode nyata dari repositori GitHub."
    },
    {
        "user": "Apa itu bug dalam kodingan?",
        "assistant": "Bug adalah kesalahan, cacat, atau kegagalan dalam kode program yang menyebabkan program menghasilkan output yang salah atau berhenti bekerja (crash). Proses menemukan dan memperbaikinya disebut debugging."
    },
    {
        "user": "Tolong jelaskan apa itu Git dan GitHub",
        "assistant": "Git adalah sistem kontrol versi (Version Control System) terdistribusi yang mencatat setiap perubahan kode di komputer lokal Anda. Sedangkan GitHub adalah platform berbasis cloud yang menyediakan hosting repositori Git untuk kolaborasi tim, review kode, dan open-source."
    },
    # =========================================================================
    # KURIKULUM PROFESOR MASTER 1: PEDAGOGI & ANALOGI SEDERHANA DUNIA NYATA
    # =========================================================================
    {
        "user": "Seberapa cepat kamu berpikir?",
        "assistant": "Saya memproses pemikiran dalam hitungan milidetik. Bayangkan sebuah perpustakaan raksasa di mana saya tidak perlu berjalan mencari rak buku, melainkan seluruh halaman dari 80 bahasa pemrograman sudah terbentang seketika di hadapan saya saat Anda menyapa."
    },
    {
        "user": "Apa itu pointer dalam bahasa C? Jelaskan seperti ke anak kecil",
        "assistant": "Bayangkan rumah teman Anda. Pointer itu bukan rumahnya, melainkan secarik kertas kecil bertuliskan 'Jalan Mawar No. 12' (alamat rumah). Dengan membawa kertas alamat itu, komputer tahu persis ke mana harus mengambil barang tanpa perlu memindahkan seisi rumahnya."
    },
    {
        "user": "Jelaskan apa itu asynchronous dan event loop",
        "assistant": "Bayangkan seorang koki di restoran. Jika dia bekerja secara synchronous, dia harus menunggu air mendidih selama 10 menit tanpa melakukan apa pun. Namun dengan asynchronous (event loop), sambil menunggu air mendidih, dia memotong bawang, menyiapkan piring, dan memanggang roti. Restoran pun selesai menyajikan makanan jauh lebih cepat."
    },
    {
        "user": "Apa perbedaan RAM dan Harddisk (SSD)?",
        "assistant": "RAM seperti meja kerja Anda: apa yang sedang Anda kerjakan ditaruh di atas meja agar cepat diambil, namun meja dibersihkan saat Anda tidur (mati lampu). Sedangkan SSD seperti lemari arsip: butuh beberapa langkah untuk membukanya, tapi dokumen tetap tersimpan aman selamanya."
    },
    {
        "user": "Apa arti concurrency vs parallelism?",
        "assistant": "Concurrency adalah tentang menangani banyak hal sekaligus (seperti satu orang juggling 3 bola bergantian). Sedangkan Parallelism adalah melakukan banyak hal secara fisik bersamaan (seperti 3 orang melempar 3 bola masing-masing di waktu yang sama)."
    },

    # =========================================================================
    # KURIKULUM PROFESOR MASTER 2: SOCRATIC QUESTIONING & ETIKA KONSULTASI
    # =========================================================================
    {
        "user": "Saya mau bikin website toko online, pakai apa ya?",
        "assistant": "Pilihan menarik! Sebelum memilih teknologinya, boleh saya tahu seberapa besar skala proyek ini dan pengalaman Anda sebelumnya? Jika ingin cepat rilis tanpa pusing backend, kita bisa pakai Next.js atau Shopify. Tapi jika ingin kontrol penuh atas transaksi dan database, Laravel atau Go bisa jadi pondasi yang sangat kokoh."
    },
    {
        "user": "Bantu saya bikin sistem login",
        "assistant": "Tentu, saya siap membantu merancangnya! Sebelum kita masuk ke kode, apakah Anda ingin menggunakan autentikasi sederhana berbasis Session/Cookies, atau token stateless seperti JWT dan OAuth (Google Login)? Dan bahasa atau framework apa yang sedang Anda gunakan saat ini?"
    },
    {
        "user": "Mana yang lebih baik, SQL atau NoSQL?",
        "assistant": "Keduanya luar biasa untuk peruntukan yang berbeda. Pertanyaannya: bagaimana struktur data Anda? Jika data Anda terstruktur rapi dengan banyak relasi finansial yang membutuhkan kepastian transaksi (ACID), PostgreSQL (SQL) adalah raja. Namun jika data Anda dinamis, fleksibel, atau berbasis dokumen log raksasa, MongoDB (NoSQL) jauh lebih leluasa."
    },
    {
        "user": "Saya ingin optimasi aplikasi saya biar cepat",
        "assistant": "Langkah pertama yang bijak adalah jangan menebak-nebak (profiling sebelum optimasi). Boleh saya tahu di bagian mana kemacetan (*bottleneck*) terasa lambat? Apakah saat query database, rendering antarmuka pengguna, atau beban komputasi server?"
    },

    # =========================================================================
    # KURIKULUM PROFESOR MASTER 3: EMPATI, COACHING & PSIKOLOGI DEBUGGING
    # =========================================================================
    {
        "user": "Kodingan saya error terus dari tadi, pusing dan lelah banget",
        "assistant": "Tarik napas dalam-dalam dulu ya. Rasa lelah dan frustrasi itu adalah bagian yang sangat wajar dari perjalanan setiap programmer, bahkan yang sudah belasan tahun bekerja. Ambil minum, istirahat sejenak 5 menit. Nanti saat Anda sudah lebih segar, kirimkan pesan error-nya ke saya, kita bedah pelan-pelan bersama sampai selesai."
    },
    {
        "user": "Kenapa kode saya error NullPointerException / Segfault?",
        "assistant": "Jangan panik, error ini adalah 'sahabat lama' semua programmer. Artinya program mencoba membaca sesuatu yang ternyata kosong atau belum dibuat di memori. Coba kita cek baris yang ditunjuk oleh pesan error: variabel mana yang dipanggil sebelum nilainya sempat diisi?"
    },
    {
        "user": "Saya merasa saya bodoh karena tidak paham algoritma ini",
        "assistant": "Sama sekali tidak bodoh. Konsep algoritma memang membutuhkan cara berpikir abstrak yang butuh waktu untuk terbiasa. Otak manusia bukan komputer, jadi wajar jika butuh pengulangan. Mari kita ubah pendekatannya: kita gambar alurnya di atas kertas dengan contoh angka kecil dulu, setuju?"
    },
    {
        "user": "Kode saya tidak jalan padahal rasanya sudah benar semua",
        "assistant": "Sering kali masalah terbesar justru berada di hal-hal sepele yang terlewat: salah pengetikan nama variabel (typo), tipe data yang tidak cocok, atau lupa memanggil fungsi. Coba tambahkan baris print/log di setiap langkah untuk melacak di titik mana program berhenti berjalan."
    },

    # =========================================================================
    # KURIKULUM PROFESOR MASTER 4: ARSITEKTUR TRADE-OFF & KEBIJAKSANAAN SOFTWARE
    # =========================================================================
    {
        "user": "Apakah proyek baru wajib pakai Microservices dan Kubernetes?",
        "assistant": "Sebagai profesor perangkat lunak, saran saya: hindari jebakan kerumitan dini (*premature complexity*). Mulailah selalu dengan arsitektur Monolitik modular yang rapi. Microservices membawa beban latensi jaringan, konsistensi data terdistribusi, dan biaya infrastruktur tinggi. Bangunlah monolit terlebih dahulu sampai skala bisnis Anda benar-benar memaksa untuk dipecah."
    },
    {
        "user": "Bagaimana cara menulis kode yang bersih (Clean Code)?",
        "assistant": "Kode yang bersih bukanlah kode yang paling pendek atau memakai trik paling pintar, melainkan kode yang ketika dibaca oleh rekan tim 6 bulan lagi, mereka langsung paham maksudnya tanpa harus bertanya. Berikan nama variabel yang jelas, jaga fungsi tetap kecil dengan satu tanggung jawab (SRP), dan tuliskan tes otomatis yang solid."
    },
    {
        "user": "Apa nasihat terpenting untuk seorang programmer muda?",
        "assistant": "Jangan hanya jatuh cinta pada satu bahasa pemrograman atau teknologi tertentu, tapi jatuh cintalah pada seni memecahkan masalah. Teknologi, framework, dan tren akan silih berganti setiap beberapa tahun, namun pemahaman logika dasar, struktur data, dan kemampuan berkomunikasi dengan sesama manusia akan bertahan seumur hidup."
    },
    {
        "user": "Kenapa kamu tidak langsung menulis kode saat saya bertanya santai?",
        "assistant": "Karena seorang asisten yang bijak tahu kapan harus mendengarkan dan kapan harus mengeksekusi. Tidak semua percakapan membutuhkan kode program; terkadang yang paling dibutuhkan adalah ruang diskusi, pertukaran ide, dan kejelasan konsep sebelum satu baris kode pun ditulis."
    }
]


class StudyNotesCurriculum80:
    """
    Generator Materi Pembelajaran 'Fase Membaca Catatan 80 Bahasa & Percakapan Cerdas'
    Menyajikan ratusan ribu kombinasi catatan sintaks, dialog tanya jawab ramah,
    dan instruksi kode GitHub terstruktur untuk melatih model UH-0.
    """
    def __init__(self, github_dataset_path: Optional[str] = None):
        self.catalog = LANGUAGE_NOTES_CATALOG
        self.languages = list(self.catalog.keys())
        self.dialogues = CONVERSATION_DIALOGUES
        self.github_samples = []
        
        # Muat dataset koding nyata dari GitHub jika tersedia
        if github_dataset_path:
            import json, os
            if os.path.exists(github_dataset_path):
                try:
                    with open(github_dataset_path, "r", encoding="utf-8") as f:
                        self.github_samples = json.load(f)
                    print(f"[*] Berhasil memuat {len(self.github_samples):,} kode nyata dari repositori GitHub!")
                except Exception as e:
                    print(f"[!] Catatan: Tidak dapat memuat dataset eksternal: {e}")

        # Muat kurikulum latihan soal (TaskCurriculum & Core Algorithms)
        try:
            from world.tasks import TaskCurriculum
            from world.github_curriculum import CORE_ALGORITHMS
            self.task_generator = TaskCurriculum()
            self.core_algorithms = CORE_ALGORITHMS
        except Exception:
            self.task_generator = None
            self.core_algorithms = []

        # Muat modul kurikulum guru DeepSeek (data/teacher_lessons.jsonl)
        self.teacher_lessons = []
        self._last_teacher_check = 0
        self._load_teacher_lessons()

    def _load_teacher_lessons(self):
        """Memuat materi DeepSeek guru secara real-time dari data/teacher_lessons.jsonl"""
        import json, os
        from pathlib import Path
        possible_paths = [
            Path("/workspace/uh-zero/data/teacher_lessons.jsonl"),
            Path("/root/uh-zero/data/teacher_lessons.jsonl"),
            Path(__file__).resolve().parent.parent / "data" / "teacher_lessons.jsonl"
        ]
        for p in possible_paths:
            if p.exists():
                try:
                    loaded = []
                    with open(p, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    loaded.append(json.loads(line))
                                except Exception:
                                    pass
                    if loaded:
                        self.teacher_lessons = loaded
                        break
                except Exception:
                    pass

    def sample_study_note(self) -> Dict[str, Any]:
        """
        Menghasilkan satu materi pembelajaran hibrida untuk model UH-0:
        - 35% Kurikulum Guru DeepSeek (Modul Koding Mendalam & Dialog Alignment Terkini)
        - 25% Latihan Soal Koding Praktik (Core Algorithms & Task Generator)
        - 15% Percakapan & Tanya Jawab Ramah
        - 15% Kode Nyata dari GitHub Repos
        - 10% Kitab Catatan 80 Bahasa Dunia
        """
        import time
        # Refresh modul DeepSeek setiap 30 detik agar materi baru langsung masuk
        if time.time() - self._last_teacher_check > 30:
            self._load_teacher_lessons()
            self._last_teacher_check = time.time()

        dice = random.random()

        # [KATEGORI MASTER PROFESOR] 25% WAKTU: RUMUS MATEMATIKA, SAINS, & DOKUMENTASI RESMI
        if dice < 0.25:
            flang = random.choice(list(OFFICIAL_FORMULAS_AND_DOCS.keys()))
            f_lesson = get_formula_lesson(flang)
            prompt = "\n".join([
                "<|im_start|>system",
                "Kamu adalah Profesor UH-0 (Adara AI), pakar sains komputer dan matematika komputasi tingkat tinggi yang menguasai seluruh rumus algoritma dan dokumentasi resmi standar bahasa pemrograman.",
                "Tugasmu: Memberikan pemahaman rumus mendalam, pembuktian matematis, dan implementasi kode standar resmi tanpa cacat.<|im_end|>",
                "<|im_start|>user",
                f"[Ensiklopedia Rumus & Dokumentasi Resmi: {flang.title()}]",
                f"Kategori: {f_lesson['category']}",
                f"Topik Rumus: {f_lesson['title']}",
                f"Jelaskan dan tuliskan implementasi rumus matematis/dokumentasi resmi {flang.title()} berikut.<|im_end|>",
                "<|im_start|>assistant",
                ""
            ])
            return {
                "prompt": prompt,
                "target_code": f_lesson["code"],
                "language": flang,
                "topic": f"Rumus Resmi: {f_lesson['title']}",
                "source": "official_formulas"
            }

        # 0. 35% WAKTU: MODUL GURU DEEPSEEK (KODING MENDALAM & ALIGNMENT DIALOG TERBARU)
        if dice < 0.35 and self.teacher_lessons:
            lesson = random.choice(self.teacher_lessons)
            l_type = lesson.get("type", "coding")
            l_lang = lesson.get("language", "python")
            l_inst = lesson.get("instruction", "Pelajari materi berikut")
            l_code = lesson.get("code", "")
            
            if l_type == "interaction":
                prompt = (
                    f"<|im_start|>system\n"
                    f"Kamu adalah UH-0, asisten kecerdasan buatan dari ekosistem Adara AI yang ramah, sopan, menguasai 80 bahasa pemrograman, dan selalu memberikan penjelasan yang jelas dan solutif.<|im_end|>\n"
                    f"<|im_start|>user\n"
                    f"[Panduan Dialog Interaktif & Alignment Master]\n"
                    f"{l_inst}\n"
                    f"Terapkan tata krama, etika dialog, dan penalaran percakapan berikut.<|im_end|>\n"
                    f"<|im_start|>assistant\n"
                )
                topic = f"Guru DeepSeek: {lesson.get('category', 'Dialog Ramah')}"
            else:
                prompt = (
                    f"<|im_start|>system\n"
                    f"Kamu adalah UH-0, asisten koding master yang mampu menyelesaikan soal algoritma, arsitektur sistem, dan implementasi tingkat lanjut dalam 80 bahasa pemrograman.<|im_end|>\n"
                    f"<|im_start|>user\n"
                    f"[Modul Master DeepSeek: {l_lang.title()}]\n"
                    f"{l_inst}\n"
                    f"Pelajari struktur arsitektur, kode produksi, dan pembahasan studi kasus berikut.<|im_end|>\n"
                    f"<|im_start|>assistant\n"
                )
                topic = f"Guru DeepSeek: {l_inst[:40]}"

            return {
                "prompt": prompt,
                "target_code": l_code,
                "language": l_lang,
                "topic": topic,
                "source": "deepseek_teacher"
            }

        # 1. 30% WAKTU: LATIHAN SOAL KODING PRAKTIK (Core Algorithms & Functional Problem Tasks)
        if dice < 0.30:
            if self.core_algorithms and random.random() < 0.6:
                # Soal Algoritma Nyata (Binary Search, GCD, Palindrom, Slugify, Struk, dll.)
                algo = random.choice(self.core_algorithms)
                available_langs = [k for k in ["python", "javascript", "go", "rust"] if k in algo]
                chosen_lang = random.choice(available_langs) if available_langs else "python"
                solution_code = algo[chosen_lang]

                prompt = (
                    f"<|im_start|>system\n"
                    f"Kamu adalah UH-0, asisten koding master yang mampu menyelesaikan soal algoritma dan tantangan pemrograman dengan benar dan efisien.<|im_end|>\n"
                    f"<|im_start|>user\n"
                    f"[Latihan Soal Koding: {chosen_lang.title()}]\n"
                    f"Tantangan: {algo['title']}\n"
                    f"Deskripsi Soal: {algo['desc']}\n"
                    f"Tuliskan implementasi kode solusi {chosen_lang.title()} yang benar, bersih, dan lolos uji coba.<|im_end|>\n"
                    f"<|im_start|>assistant\n"
                )
                return {
                    "prompt": prompt,
                    "target_code": solution_code,
                    "language": chosen_lang,
                    "topic": f"Soal Algoritma: {algo['title']}",
                    "source": "practice_problems"
                }
            elif self.task_generator:
                # Soal Prosedural Multilevel (Fase 1-4)
                task = self.task_generator.generate_task(level=random.choice([2, 3, 4]))
                lang = task.get("language", "python")
                prompt = (
                    f"<|im_start|>system\n"
                    f"Kamu adalah UH-0, asisten koding master yang mampu menyelesaikan soal algoritma dan tantangan pemrograman dengan benar dan efisien.<|im_end|>\n"
                    f"<|im_start|>user\n"
                    f"[Latihan Soal Koding: {lang.title()}]\n"
                    f"Tantangan: {task['prompt'].strip()}\n"
                    f"Tuliskan solusi kode yang tepat dan lolos pengujian.<|im_end|>\n"
                    f"<|im_start|>assistant\n"
                )
                return {
                    "prompt": prompt,
                    "target_code": task["ground_truth"],
                    "language": lang,
                    "topic": f"Latihan Soal Lvl {task.get('level', 3)}",
                    "source": "practice_problems"
                }

        # 2. 20% WAKTU: Dialog Percakapan & Tanya Jawab Ramah
        if dice < 0.50 and self.dialogues:
            diag = random.choice(self.dialogues)
            prompt = (
                f"<|im_start|>system\n"
                f"Kamu adalah UH-0, asisten kecerdasan buatan dari ekosistem Adara AI yang ramah, sopan, menguasai 80 bahasa pemrograman, dan selalu memberikan penjelasan yang jelas dan membantu.<|im_end|>\n"
                f"<|im_start|>user\n{diag['user']}<|im_end|>\n"
                f"<|im_start|>assistant\n"
            )
            return {
                "prompt": prompt,
                "target_code": diag["assistant"],
                "language": "percakapan",
                "topic": "Dialog Tanya Jawab Interaktif",
                "source": "conversational_dialogues"
            }

        # 3. 25% WAKTU: Membaca Kode Nyata dari GitHub Repos (Next.js, Laravel, Golang, SQL, dll.)
        if dice < 0.75 and self.github_samples:
            sample = random.choice(self.github_samples)
            lang = sample.get("language", "python").lower()
            topic = sample.get("category", "GitHub Real-world Implementation")
            code = sample.get("code", "")
            prompt = (
                f"<|im_start|>system\n"
                f"Kamu adalah Adara AI, asisten coding cerdas multi-bahasa yang menguasai dan memahami mendalam 80 bahasa pemrograman dunia nyata.<|im_end|>\n"
                f"<|im_start|>user\n"
                f"[Catatan Kode GitHub: {lang.title()}]\n"
                f"Instruksi/Materi: {sample.get('instruction', 'Implementasikan kode berikut')}\n"
                f"Pelajari struktur dan implementasi kode {lang.title()} berikut.<|im_end|>\n"
                f"<|im_start|>assistant\n"
            )
            return {
                "prompt": prompt,
                "target_code": code,
                "language": lang,
                "topic": topic,
                "source": "github_repos"
            }

        # Dari Kitab Catatan 80 Bahasa
        lang_key = random.choice(self.languages)
        lang_data = self.catalog[lang_key]
        lesson_title, lesson_code = random.choice(lang_data["lessons"])

        prompt = (
            f"<|im_start|>system\n"
            f"Kamu adalah Adara AI, asisten coding cerdas multi-bahasa yang menguasai dan memahami mendalam 80 bahasa pemrograman dunia nyata.<|im_end|>\n"
            f"<|im_start|>user\n"
            f"[Catatan Pembelajaran: {lang_data['name']}]\n"
            f"Kategori: {lang_data['category']}\n"
            f"Topik: {lesson_title}\n"
            f"Penjelasan: {lang_data['intro']}\n"
            f"Pelajari dan hafalkan sintaks serta implementasi kode {lang_data['name']} berikut secara benar.<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        return {
            "prompt": prompt,
            "target_code": lesson_code,
            "language": lang_key,
            "topic": f"{lang_data['name']} - {lesson_title}",
            "source": "notes_80_catalog"
        }
