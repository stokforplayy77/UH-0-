"""
UH-0 (UH Labs Zero) - 80 Programming Languages Registry & Knowledge Base
Maps syntax hallmarks, paradigms, and procedural templates for 80 programming languages.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ProgrammingLanguage:
    id: str
    name: str
    category: str
    extension: str
    paradigm: str
    comment_single: str
    print_statement: str
    variable_decl: str
    function_decl: str
    loop_sample: str
    sample_code: str
    description: str


# 80 Programming Languages across 8 distinct categories (10 languages each)
LANGUAGES_CATALOG: Dict[str, ProgrammingLanguage] = {
    # --- Category 1: Web & Modern Fullstack (10) ---
    "python": ProgrammingLanguage(
        id="python", name="Python", category="Web & General", extension=".py",
        paradigm="Multi-paradigm, Dynamic", comment_single="#",
        print_statement='print("Hello, World!")',
        variable_decl="x = 42",
        function_decl="def tambah(a, b):\n    return a + b",
        loop_sample="for i in range(5):\n    print(i)",
        sample_code="def main():\n    print('Halo dari Adara Python')",
        description="Bahasa serba guna dengan keterbacaan tinggi dan ekosistem AI/Data masif."
    ),
    "javascript": ProgrammingLanguage(
        id="javascript", name="JavaScript", category="Web & General", extension=".js",
        paradigm="Event-driven, Functional, Imperative", comment_single="//",
        print_statement='console.log("Hello, World!");',
        variable_decl="const x = 42;",
        function_decl="function tambah(a, b) {\n    return a + b;\n}",
        loop_sample="for (let i = 0; i < 5; i++) {\n    console.log(i);\n}",
        sample_code="function main() {\n    console.log('Halo dari Adara JS');\n}",
        description="Bahasa utama ekosistem web modern, browser, dan runtime Node.js."
    ),
    "typescript": ProgrammingLanguage(
        id="typescript", name="TypeScript", category="Web & General", extension=".ts",
        paradigm="Static Typed Superset of JS", comment_single="//",
        print_statement='console.log("Hello, World!");',
        variable_decl="const x: number = 42;",
        function_decl="function tambah(a: number, b: number): number {\n    return a + b;\n}",
        loop_sample="for (let i: number = 0; i < 5; i++) {\n    console.log(i);\n}",
        sample_code="const pesan: string = 'Halo TS';\nconsole.log(pesan);",
        description="JavaScript dengan sistem tipe statis kuat untuk aplikasi enterprise berskala besar."
    ),
    "php": ProgrammingLanguage(
        id="php", name="PHP", category="Web & General", extension=".php",
        paradigm="Server-side Web Scripting", comment_single="//",
        print_statement='echo "Hello, World!";',
        variable_decl="$x = 42;",
        function_decl="function tambah($a, $b) {\n    return $a + $b;\n}",
        loop_sample="for ($i = 0; $i < 5; $i++) {\n    echo $i;\n}",
        sample_code="<?php\necho 'Halo dari PHP';\n?>",
        description="Bahasa backend pondasi web global yang mentenagai WordPress dan Laravel."
    ),
    "ruby": ProgrammingLanguage(
        id="ruby", name="Ruby", category="Web & General", extension=".rb",
        paradigm="Pure Object-Oriented", comment_single="#",
        print_statement='puts "Hello, World!"',
        variable_decl="x = 42",
        function_decl="def tambah(a, b)\n  a + b\nend",
        loop_sample="5.times do |i|\n  puts i\nend",
        sample_code="puts 'Halo dari Ruby on Rails'",
        description="Bahasa elegan yang berfokus pada kebahagiaan developer dan framework Rails."
    ),
    "html": ProgrammingLanguage(
        id="html", name="HTML5", category="Web & General", extension=".html",
        paradigm="Markup Language", comment_single="<!--",
        print_statement='<p>Hello, World!</p>',
        variable_decl='<meta name="app" content="UH-0">',
        function_decl='<template id="card"><div>Content</div></template>',
        loop_sample='<ul><li>1</li><li>2</li></ul>',
        sample_code='<!DOCTYPE html><html><body><h1>Halo UH-0</h1></body></html>',
        description="Standar markup struktur universal seluruh halaman web di dunia."
    ),
    "css": ProgrammingLanguage(
        id="css", name="CSS3", category="Web & General", extension=".css",
        paradigm="Style Sheet Language", comment_single="/*",
        print_statement='body::after { content: "Hello"; }',
        variable_decl='--primary: #6366f1;',
        function_decl='@keyframes pulse { 0% { opacity: 0; } 100% { opacity: 1; } }',
        loop_sample='div:nth-child(n) { margin: 4px; }',
        sample_code='body { background: #0f172a; color: #38bdf8; font-family: sans-serif; }',
        description="Bahasa penataan gaya, tata letak, dan animasi visual antarmuka web."
    ),
    "svelte": ProgrammingLanguage(
        id="svelte", name="Svelte", category="Web & General", extension=".svelte",
        paradigm="Compiler-based Reactive UI", comment_single="<!--",
        print_statement='<script>let msg = "Hello";</script><p>{msg}</p>',
        variable_decl='let count = $state(0);',
        function_decl='function inc() { count += 1; }',
        loop_sample='{#each items as item}<li>{item}</li>{/each}',
        sample_code='<script>let n = 1;</script><button on:click={() => n++}>{n}</button>',
        description="Framework frontend kompilasi reaktif tanpa overhead Virtual DOM."
    ),
    "vue": ProgrammingLanguage(
        id="vue", name="Vue Template", category="Web & General", extension=".vue",
        paradigm="Progressive Component-based UI", comment_single="<!--",
        print_statement='<template><div>{{ msg }}</div></template>',
        variable_decl='const count = ref(0);',
        function_decl='const tambah = (a, b) => a + b;',
        loop_sample='<div v-for="i in 5" :key="i">{{ i }}</div>',
        sample_code='<template><p>Halo Vue</p></template><script setup></script>',
        description="Ekosistem UI progresif yang intuitif dan reaktif dengan Single File Component."
    ),
    "hack": ProgrammingLanguage(
        id="hack", name="Hack", category="Web & General", extension=".hack",
        paradigm="Gradual Typing for HHVM", comment_single="//",
        print_statement='echo "Hello, World!\n";',
        variable_decl='int $x = 42;',
        function_decl='function tambah(int $a, int $b): int {\n    return $a + $b;\n}',
        loop_sample='for ($i = 0; $i < 5; $i++) { echo $i; }',
        sample_code='<<__EntryPoint>>\nfunction main(): void {\n  echo "Halo Hack HHVM";\n}',
        description="Dialek PHP bertipe statis ketat buatan Meta untuk performa mesin virtual HHVM."
    ),

    # --- Category 2: Systems & High-Performance (10) ---
    "c": ProgrammingLanguage(
        id="c", name="C", category="Systems & Native", extension=".c",
        paradigm="Imperative, Procedural", comment_single="//",
        print_statement='printf("Hello, World!\\n");',
        variable_decl="int x = 42;",
        function_decl="int tambah(int a, int b) {\n    return a + b;\n}",
        loop_sample="for (int i = 0; i < 5; i++) {\n    printf(\"%d\\n\", i);\n}",
        sample_code='#include <stdio.h>\nint main() {\n    printf("Halo dari C\\n");\n    return 0;\n}',
        description="Pondasi seluruh sistem operasi modern, kernel Linux, dan runtime embedded."
    ),
    "cpp": ProgrammingLanguage(
        id="cpp", name="C++", category="Systems & Native", extension=".cpp",
        paradigm="Multi-paradigm, OOP, Generic", comment_single="//",
        print_statement='std::cout << "Hello, World!" << std::endl;',
        variable_decl="int x = 42;",
        function_decl="int tambah(int a, int b) {\n    return a + b;\n}",
        loop_sample="for (int i = 0; i < 5; ++i) {\n    std::cout << i << std::endl;\n}",
        sample_code='#include <iostream>\nint main() {\n    std::cout << "Halo C++23" << std::endl;\n    return 0;\n}',
        description="Bahasa performa ultra-tinggi untuk game engine, browser core, dan sistem finansial."
    ),
    "rust": ProgrammingLanguage(
        id="rust", name="Rust", category="Systems & Native", extension=".rs",
        paradigm="Memory Safe, Concurrent, Functional", comment_single="//",
        print_statement='println!("Hello, World!");',
        variable_decl="let x: i32 = 42;",
        function_decl="fn tambah(a: i32, b: i32) -> i32 {\n    a + b\n}",
        loop_sample="for i in 0..5 {\n    println!(\"{}\", i);\n}",
        sample_code='fn main() {\n    println!("Halo Rust Memory Safe!");\n}',
        description="Bahasa sistem modern tanpa garbage collector dengan garansi memory safety via borrow checker."
    ),
    "go": ProgrammingLanguage(
        id="go", name="Go (Golang)", category="Systems & Native", extension=".go",
        paradigm="Concurrent, Imperative", comment_single="//",
        print_statement='fmt.Println("Hello, World!")',
        variable_decl="x := 42",
        function_decl="func tambah(a int, b int) int {\n    return a + b\n}",
        loop_sample="for i := 0; i < 5; i++ {\n    fmt.Println(i)\n}",
        sample_code='package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Halo Go Goroutines")\n}',
        description="Bahasa cloud-native dan backend microservice Google dengan concurrency super ringan."
    ),
    "zig": ProgrammingLanguage(
        id="zig", name="Zig", category="Systems & Native", extension=".zig",
        paradigm="Pragmatic Systems Programming", comment_single="//",
        print_statement='std.debug.print("Hello, World!\\n", .{});',
        variable_decl="const x: i32 = 42;",
        function_decl="fn tambah(a: i32, b: i32) i32 {\n    return a + b;\n}",
        loop_sample="for (0..5) |i| {\n    std.debug.print(\"{d}\\n\", .{i});\n}",
        sample_code='const std = @import("std");\npub fn main() void {\n    std.debug.print("Halo Zig\\n", .{});\n}',
        description="Alternatif C modern tanpa hidden control flow dan integrasi toolchain kompilasi luar biasa."
    ),
    "d": ProgrammingLanguage(
        id="d", name="D", category="Systems & Native", extension=".d",
        paradigm="Multi-paradigm Systems", comment_single="//",
        print_statement='writeln("Hello, World!");',
        variable_decl="int x = 42;",
        function_decl="int tambah(int a, int b) {\n    return a + b;\n}",
        loop_sample="foreach (i; 0 .. 5) {\n    writeln(i);\n}",
        sample_code='import std.stdio;\nvoid main() {\n    writeln("Halo D Language");\n}',
        description="Evolusi C++ dengan produktivitas tinggi, metaprogramming canggih, dan opsi GC fleksibel."
    ),
    "nim": ProgrammingLanguage(
        id="nim", name="Nim", category="Systems & Native", extension=".nim",
        paradigm="Expressive Systems Language", comment_single="#",
        print_statement='echo "Hello, World!"',
        variable_decl="var x: int = 42",
        function_decl="proc tambah(a, b: int): int =\n  return a + b",
        loop_sample="for i in 0 ..< 5:\n  echo i",
        sample_code='proc main() =\n  echo "Halo Nim C-backend"\nmain()',
        description="Sintaks seindah Python yang dikompilasi langsung ke kode C/C++ native berkecepatan tinggi."
    ),
    "v": ProgrammingLanguage(
        id="v", name="V (Vlang)", category="Systems & Native", extension=".v",
        paradigm="Fast, Simple Systems", comment_single="//",
        print_statement='println("Hello, World!")',
        variable_decl="x := 42",
        function_decl="fn tambah(a int, b int) int {\n    return a + b\n}",
        loop_sample="for i in 0 .. 5 {\n    println(i)\n}",
        sample_code='fn main() {\n    println("Halo V Language")\n}',
        description="Bahasa ultra-cepat yang bisa mengkompilasi 1 juta baris kode dalam hitungan detik."
    ),
    "assembly": ProgrammingLanguage(
        id="assembly", name="Assembly (x86_64)", category="Systems & Native", extension=".s",
        paradigm="Low-level Machine Code", comment_single=";",
        print_statement='mov rax, 1 ; sys_write',
        variable_decl="section .data\n  x dq 42",
        function_decl="tambah:\n  add rdi, rsi\n  mov rax, rdi\n  ret",
        loop_sample=".loop:\n  dec rcx\n  jnz .loop",
        sample_code='global _start\nsection .text\n_start:\n  mov rax, 60\n  xor rdi, rdi\n  syscall',
        description="Instruksi mesin tingkat perangkat keras paling mendasar untuk arsitektur CPU prosesor."
    ),
    "wat": ProgrammingLanguage(
        id="wat", name="WebAssembly (WAT)", category="Systems & Native", extension=".wat",
        paradigm="Stack-based Bytecode Text", comment_single=";;",
        print_statement='(call $print (i32.const 42))',
        variable_decl='(local $x i32)',
        function_decl='(func $tambah (param $a i32) (param $b i32) (result i32)\n  local.get $a\n  local.get $b\n  i32.add)',
        loop_sample='(loop $my_loop\n  ;; loop body\n)',
        sample_code='(module\n  (func $main (result i32)\n    i32.const 42\n  )\n)',
        description="Representasi teks biner WebAssembly untuk komputasi native portable lintas browser."
    ),

    # --- Category 3: Enterprise & JVM / .NET (10) ---
    "java": ProgrammingLanguage(
        id="java", name="Java", category="Enterprise & JVM/.NET", extension=".java",
        paradigm="Class-based Object-Oriented", comment_single="//",
        print_statement='System.out.println("Hello, World!");',
        variable_decl="int x = 42;",
        function_decl="public static int tambah(int a, int b) {\n    return a + b;\n}",
        loop_sample="for (int i = 0; i < 5; i++) {\n    System.out.println(i);\n}",
        sample_code='public class Main {\n    public static void main(String[] args) {\n        System.out.println("Halo Java 21");\n    }\n}',
        description="Standar industri enterprise global, perbankan, dan ekosistem backend terandal."
    ),
    "kotlin": ProgrammingLanguage(
        id="kotlin", name="Kotlin", category="Enterprise & JVM/.NET", extension=".kt",
        paradigm="Multi-paradigm, Concise OOP/Functional", comment_single="//",
        print_statement='println("Hello, World!")',
        variable_decl="val x: Int = 42",
        function_decl="fun tambah(a: Int, b: Int): Int = a + b",
        loop_sample="for (i in 0 until 5) {\n    println(i)\n}",
        sample_code='fun main() {\n    println("Halo Kotlin Android & Backend")\n}',
        description="Bahasa resmi utama Google untuk Android dan backend modern yang bebas NullPointerException."
    ),
    "scala": ProgrammingLanguage(
        id="scala", name="Scala", category="Enterprise & JVM/.NET", extension=".scala",
        paradigm="Functional & Object-Oriented", comment_single="//",
        print_statement='println("Hello, World!")',
        variable_decl="val x: Int = 42",
        function_decl="def tambah(a: Int, b: Int): Int = a + b",
        loop_sample="for (i <- 0 until 5) println(i)",
        sample_code='object Main extends App {\n  println("Halo Scala 3 & Apache Spark")\n}',
        description="Penggabungan sempurna OOP dan Functional programming di balik mesin big data Apache Spark."
    ),
    "groovy": ProgrammingLanguage(
        id="groovy", name="Groovy", category="Enterprise & JVM/.NET", extension=".groovy",
        paradigm="Dynamic JVM Scripting", comment_single="//",
        print_statement='println "Hello, World!"',
        variable_decl="def x = 42",
        function_decl="def tambah(a, b) { a + b }",
        loop_sample="5.times { println it }",
        sample_code='println "Halo Groovy Gradle Automation"',
        description="Bahasa scripting dinamis untuk JVM yang menjadi fondasi otomasi build Gradle dan Jenkins."
    ),
    "csharp": ProgrammingLanguage(
        id="csharp", name="C#", category="Enterprise & JVM/.NET", extension=".cs",
        paradigm="Multi-paradigm, Component-oriented", comment_single="//",
        print_statement='Console.WriteLine("Hello, World!");',
        variable_decl="int x = 42;",
        function_decl="public static int Tambah(int a, int b) => a + b;",
        loop_sample="for (int i = 0; i < 5; i++) {\n    Console.WriteLine(i);\n}",
        sample_code='using System;\nclass Program {\n    static void Main() {\n        Console.WriteLine("Halo C# 12 .NET 8");\n    }\n}',
        description="Bahasa andalan ekosistem Microsoft .NET, cloud Azure, dan game engine Unity."
    ),
    "fsharp": ProgrammingLanguage(
        id="fsharp", name="F#", category="Enterprise & JVM/.NET", extension=".fs",
        paradigm="Functional-first .NET", comment_single="//",
        print_statement='printfn "Hello, World!"',
        variable_decl="let x = 42",
        function_decl="let tambah a b = a + b",
        loop_sample="for i in 0 .. 4 do printfn \"%d\" i",
        sample_code='[<EntryPoint>]\nlet main argv =\n    printfn "Halo F# Functional"\n    0',
        description="Bahasa functional-first pada runtime .NET untuk komputasi finansial dan analisis data terstruktur."
    ),
    "vbnet": ProgrammingLanguage(
        id="vbnet", name="Visual Basic .NET", category="Enterprise & JVM/.NET", extension=".vb",
        paradigm="Event-driven, Object-Oriented", comment_single="'",
        print_statement='Console.WriteLine("Hello, World!")',
        variable_decl="Dim x As Integer = 42",
        function_decl="Function Tambah(a As Integer, b As Integer) As Integer\n    Return a + b\nEnd Function",
        loop_sample="For i As Integer = 0 To 4\n    Console.WriteLine(i)\nNext",
        sample_code='Module Program\n    Sub Main()\n        Console.WriteLine("Halo VB.NET")\n    End Sub\nEnd Module',
        description="Bahasa ramah pembaca untuk ekosistem aplikasi enterprise Windows dan perkantoran."
    ),
    "apex": ProgrammingLanguage(
        id="apex", name="Apex", category="Enterprise & JVM/.NET", extension=".cls",
        paradigm="Cloud Database OOP", comment_single="//",
        print_statement='System.debug(\'Hello, World!\');',
        variable_decl="Integer x = 42;",
        function_decl="public static Integer tambah(Integer a, Integer b) {\n    return a + b;\n}",
        loop_sample="for (Integer i = 0; i < 5; i++) {\n    System.debug(i);\n}",
        sample_code='public class Halo {\n    public static void run() {\n        System.debug(\'Halo Salesforce Apex\');\n    }\n}',
        description="Bahasa pemrograman cloud backend khusus platform CRM Salesforce."
    ),
    "abap": ProgrammingLanguage(
        id="abap", name="ABAP", category="Enterprise & JVM/.NET", extension=".abap",
        paradigm="Business Application Language", comment_single="*",
        print_statement='WRITE: / \'Hello, World!\'.',
        variable_decl="DATA: lv_x TYPE i VALUE 42.",
        function_decl="FORM tambah USING p_a TYPE i p_b TYPE i CHANGING p_res TYPE i.\n  p_res = p_a + p_b.\nENDFORM.",
        loop_sample="DO 5 TIMES.\n  WRITE: / sy-index.\nENDDO.",
        sample_code='REPORT z_halo.\nSTART-OF-SELECTION.\n  WRITE: / \'Halo SAP ABAP Enterprise\'.',
        description="Bahasa pemrograman resmi sistem ERP bisnis enterprise SAP di seluruh dunia."
    ),
    "cobol": ProgrammingLanguage(
        id="cobol", name="COBOL", category="Enterprise & JVM/.NET", extension=".cbl",
        paradigm="Procedural, Business Data Processing", comment_single="*",
        print_statement='DISPLAY "Hello, World!".',
        variable_decl="01 WS-X PIC 9(2) VALUE 42.",
        function_decl="ADD-NUMBERS.\n    ADD WS-A TO WS-B GIVING WS-RESULT.",
        loop_sample="PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 5\n    DISPLAY WS-I\nEND-PERFORM.",
        sample_code='IDENTIFICATION DIVISION.\nPROGRAM-ID. HELLO.\nPROCEDURE DIVISION.\n    DISPLAY "Halo COBOL Mainframe".\n    STOP RUN.',
        description="Pondasi legendaris sistem mainframe perbankan dan transaksi keuangan global."
    ),

    # --- Category 4: Mobile, Games & Scripting (10) ---
    "swift": ProgrammingLanguage(
        id="swift", name="Swift", category="Mobile & Games", extension=".swift",
        paradigm="Protocol-oriented, Functional, OOP", comment_single="//",
        print_statement='print("Hello, World!")',
        variable_decl="let x: Int = 42",
        function_decl="func tambah(_ a: Int, _ b: Int) -> Int {\n    return a + b\n}",
        loop_sample="for i in 0..<5 {\n    print(i)\n}",
        sample_code='import Foundation\nprint("Halo Swift Apple Ecosystem")',
        description="Bahasa resmi Apple untuk ekosistem iOS, iPadOS, macOS, watchOS, dan visionOS."
    ),
    "dart": ProgrammingLanguage(
        id="dart", name="Dart", category="Mobile & Games", extension=".dart",
        paradigm="Class-based, Single-inheritance OOP", comment_single="//",
        print_statement='print("Hello, World!");',
        variable_decl="int x = 42;",
        function_decl="int tambah(int a, int b) => a + b;",
        loop_sample="for (var i = 0; i < 5; i++) {\n    print(i);\n}",
        sample_code='void main() {\n    print("Halo Dart Flutter Cross-Platform");\n}',
        description="Bahasa di balik framework Flutter untuk membangun UI multi-platform dari satu basis kode."
    ),
    "lua": ProgrammingLanguage(
        id="lua", name="Lua", category="Mobile & Games", extension=".lua",
        paradigm="Lightweight Multi-paradigm Scripting", comment_single="--",
        print_statement='print("Hello, World!")',
        variable_decl="local x = 42",
        function_decl="function tambah(a, b)\n    return a + b\nend",
        loop_sample="for i = 1, 5 do\n    print(i)\nend",
        sample_code='function main()\n    print("Halo Lua Neovim & Roblox Engine")\nend\nmain()',
        description="Bahasa scripting ultra-ringan dan cepat yang menjadi standar integrasi game engine (Roblox, Defold)."
    ),
    "gdscript": ProgrammingLanguage(
        id="gdscript", name="GDScript", category="Mobile & Games", extension=".gd",
        paradigm="High-level Game Scripting", comment_single="#",
        print_statement='print("Hello, World!")',
        variable_decl="var x: int = 42",
        function_decl="func tambah(a: int, b: int) -> int:\n    return a + b",
        loop_sample="for i in range(5):\n    print(i)",
        sample_code='extends Node\nfunc _ready():\n    print("Halo Godot Engine 4")',
        description="Bahasa scripting bawaan game engine Godot 4 dengan sintaks bersih mirip Python."
    ),
    "actionscript": ProgrammingLanguage(
        id="actionscript", name="ActionScript 3", category="Mobile & Games", extension=".as",
        paradigm="OOP Scripting for Flash/AIR", comment_single="//",
        print_statement='trace("Hello, World!");',
        variable_decl="var x:int = 42;",
        function_decl="function tambah(a:int, b:int):int {\n    return a + b;\n}",
        loop_sample="for (var i:int = 0; i < 5; i++) {\n    trace(i);\n}",
        sample_code='package {\n    import flash.display.Sprite;\n    public class Main extends Sprite {\n        public function Main() { trace("Halo AS3"); }\n    }\n}',
        description="Bahasa animasi dan game interaktif legendaris platform Adobe Flash dan AIR."
    ),
    "coffeescript": ProgrammingLanguage(
        id="coffeescript", name="CoffeeScript", category="Mobile & Games", extension=".coffee",
        paradigm="Golden Rule JS Dialect", comment_single="#",
        print_statement='console.log "Hello, World!"',
        variable_decl="x = 42",
        function_decl="tambah = (a, b) -> a + b",
        loop_sample="console.log i for i in [0...5]",
        sample_code='pesan = "Halo CoffeeScript"\nconsole.log pesan',
        description="Transpiler awal yang menginspirasi banyak fitur modern pada JavaScript ES6."
    ),
    "tcl": ProgrammingLanguage(
        id="tcl", name="Tcl", category="Mobile & Games", extension=".tcl",
        paradigm="Command-driven Tool Scripting", comment_single="#",
        print_statement='puts "Hello, World!"',
        variable_decl="set x 42",
        function_decl="proc tambah {a b} {\n    expr {$a + $b}\n}",
        loop_sample="for {set i 0} {$i < 5} {incr i} {\n    puts $i\n}",
        sample_code='puts "Halo Tcl/Tk GUI Scripting"',
        description="Bahasa otomasi command-driven yang populer untuk pembuatan GUI instan Tk dan tool EDA."
    ),
    "smalltalk": ProgrammingLanguage(
        id="smalltalk", name="Smalltalk", category="Mobile & Games", extension=".st",
        paradigm="Pure Message-Passing OOP", comment_single='"',
        print_statement='Transcript show: \'Hello, World!\'; cr.',
        variable_decl="x := 42.",
        function_decl="tambah: a with: b\n    ^ a + b",
        loop_sample="1 to: 5 do: [ :i | Transcript show: i printString; cr ].",
        sample_code='Transcript show: \'Halo Pure OOP Smalltalk\'; cr.',
        description="Pelopor sejati konsep Object-Oriented Programming murni dengan pesan grafis dinamis."
    ),
    "objc": ProgrammingLanguage(
        id="objc", name="Objective-C", category="Mobile & Games", extension=".m",
        paradigm="Reflective, Class-based OOP", comment_single="//",
        print_statement='NSLog(@"Hello, World!");',
        variable_decl="int x = 42;",
        function_decl="- (int)tambah:(int)a withB:(int)b {\n    return a + b;\n}",
        loop_sample="for (int i = 0; i < 5; i++) {\n    NSLog(@\"%d\", i);\n}",
        sample_code='#import <Foundation/Foundation.h>\nint main() {\n    NSLog(@"Halo Obj-C Legacy");\n    return 0;\n}',
        description="Bahasa historis ekosistem Apple yang memadukan komputasi C dengan dynamic messaging ala Smalltalk."
    ),
    "crystal": ProgrammingLanguage(
        id="crystal", name="Crystal", category="Mobile & Games", extension=".cr",
        paradigm="Statically Typed, Compiled Ruby-syntax", comment_single="#",
        print_statement='puts "Hello, World!"',
        variable_decl="x = 42",
        function_decl="def tambah(a : Int32, b : Int32) : Int32\n  a + b\nend",
        loop_sample="5.times do |i|\n  puts i\nend",
        sample_code='puts "Halo Crystal: Secepat C, Semanis Ruby"',
        description="Sintaks seindah Ruby dengan kecepatan eksekusi native dan tipe statis secepat C."
    ),

    # --- Category 5: Data Science, Database & Markup (10) ---
    "sql": ProgrammingLanguage(
        id="sql", name="SQL (ANSI Standard)", category="Data & Storage", extension=".sql",
        paradigm="Declarative Query Language", comment_single="--",
        print_statement='SELECT "Hello, World!" AS greeting;',
        variable_decl="SET @x = 42;",
        function_decl="CREATE FUNCTION tambah(a INT, b INT) RETURNS INT\nBEGIN\n    RETURN a + b;\nEND;",
        loop_sample="SELECT number FROM numbers WHERE number < 5;",
        sample_code='SELECT id, nama, email FROM users WHERE aktif = 1 ORDER BY id DESC;',
        description="Standar universal untuk menyimpan, memanipulasi, dan meminta data relasional."
    ),
    "plsql": ProgrammingLanguage(
        id="plsql", name="PL/SQL (Oracle)", category="Data & Storage", extension=".pls",
        paradigm="Procedural Extension for SQL", comment_single="--",
        print_statement='DBMS_OUTPUT.PUT_LINE(\'Hello, World!\');',
        variable_decl="x NUMBER := 42;",
        function_decl="FUNCTION tambah(a NUMBER, b NUMBER) RETURN NUMBER IS\nBEGIN\n    RETURN a + b;\nEND;",
        loop_sample="FOR i IN 1..5 LOOP\n    DBMS_OUTPUT.PUT_LINE(i);\nEND LOOP;",
        sample_code='BEGIN\n    DBMS_OUTPUT.PUT_LINE(\'Halo Oracle PL/SQL\');\nEND;',
        description="Ekstensi prosedural tangguh untuk database Oracle enterprise."
    ),
    "tsql": ProgrammingLanguage(
        id="tsql", name="T-SQL (SQL Server)", category="Data & Storage", extension=".sql",
        paradigm="Procedural SQL Extension", comment_single="--",
        print_statement='PRINT \'Hello, World!\';',
        variable_decl="DECLARE @x INT = 42;",
        function_decl="CREATE FUNCTION dbo.Tambah(@a INT, @b INT) RETURNS INT AS\nBEGIN\n    RETURN @a + @b;\nEND;",
        loop_sample="WHILE @i < 5 BEGIN PRINT @i; SET @i = @i + 1; END",
        sample_code='SELECT TOP 10 * FROM Transaksi WHERE Tanggal >= GETDATE();',
        description="Dialek SQL Microsoft SQL Server dengan logika prosedural dan transaksi ketat."
    ),
    "r": ProgrammingLanguage(
        id="r", name="R", category="Data & Storage", extension=".r",
        paradigm="Statistical Computing", comment_single="#",
        print_statement='print("Hello, World!")',
        variable_decl="x <- 42",
        function_decl="tambah <- function(a, b) {\n    return(a + b)\n}",
        loop_sample="for (i in 1:5) {\n    print(i)\n}",
        sample_code='data <- c(12, 15, 18, 22)\ncat("Rataan:", mean(data), "\n")',
        description="Bahasa utama para analis data, statistikawan, dan bioinformatika dunia."
    ),
    "julia": ProgrammingLanguage(
        id="julia", name="Julia", category="Data & Storage", extension=".jl",
        paradigm="High-performance Technical Computing", comment_single="#",
        print_statement='println("Hello, World!")',
        variable_decl="x = 42",
        function_decl="function tambah(a::Int, b::Int)::Int\n    return a + b\nend",
        loop_sample="for i in 1:5\n    println(i)\nend",
        sample_code='println("Halo Julia Scientific Computing")',
        description="Menyelesaikan masalah dua bahasa: kecepatan komputasi numerik C dengan kemudahan Python."
    ),
    "matlab": ProgrammingLanguage(
        id="matlab", name="MATLAB / Octave", category="Data & Storage", extension=".m",
        paradigm="Matrix-based Computation", comment_single="%",
        print_statement='disp(\'Hello, World!\');',
        variable_decl="x = 42;",
        function_decl="function c = tambah(a, b)\n    c = a + b;\nend",
        loop_sample="for i = 1:5\n    disp(i);\nend",
        sample_code='A = [1 2; 3 4];\ndisp(det(A));',
        description="Standar industri komputasi matriks, simulasi teknik, dan pemrosesan sinyal."
    ),
    "sas": ProgrammingLanguage(
        id="sas", name="SAS", category="Data & Storage", extension=".sas",
        paradigm="Statistical Analysis System", comment_single="*",
        print_statement='%put Hello, World!;',
        variable_decl="DATA _NULL_; x = 42; RUN;",
        function_decl="%macro tambah(a, b);\n    %sysevalf(&a + &b)\n%mend;",
        loop_sample="DO i = 1 TO 5; OUTPUT; END;",
        sample_code='DATA test;\n    SET source;\n    WHERE status = \'ACTIVE\';\nRUN;',
        description="Bahasa analisis statistik dominan di sektor farmasi, uji klinis, dan perbankan."
    ),
    "graphql": ProgrammingLanguage(
        id="graphql", name="GraphQL", category="Data & Storage", extension=".graphql",
        paradigm="API Query Language", comment_single="#",
        print_statement='query { greeting }',
        variable_decl='query GetUser($id: ID!) { user(id: $id) { name } }',
        function_decl='type Query {\n    tambah(a: Int!, b: Int!): Int!\n}',
        loop_sample='query { users { id name email } }',
        sample_code='type User {\n  id: ID!\n  username: String!\n  email: String!\n}',
        description="Bahasa kueri deklaratif untuk API modern yang menghindari over-fetching data."
    ),
    "json": ProgrammingLanguage(
        id="json", name="JSON / JSON5", category="Data & Storage", extension=".json",
        paradigm="Data Interchange Standard", comment_single="//",
        print_statement='{"message": "Hello, World!"}',
        variable_decl='{"x": 42}',
        function_decl='{"schema": {"type": "function", "name": "tambah"}}',
        loop_sample='[1, 2, 3, 4, 5]',
        sample_code='{\n  "service": "UH-0",\n  "version": "1.0",\n  "languages": 80\n}',
        description="Format pertukaran data paling populer dan universal dalam komunikasi web dan API."
    ),
    "yaml": ProgrammingLanguage(
        id="yaml", name="YAML", category="Data & Storage", extension=".yaml",
        paradigm="Human-friendly Data Serialization", comment_single="#",
        print_statement='message: Hello, World!',
        variable_decl='x: 42',
        function_decl='steps:\n  - name: run\n    command: python3 train.py',
        loop_sample='items:\n  - item1\n  - item2',
        sample_code='server:\n  host: 127.0.0.1\n  port: 8099\n  active: true',
        description="Format konfigurasi standar industri untuk Kubernetes, Docker Compose, dan GitHub Actions."
    ),

    # --- Category 6: Functional & Logic Paradigms (10) ---
    "haskell": ProgrammingLanguage(
        id="haskell", name="Haskell", category="Functional & Logic", extension=".hs",
        paradigm="Pure Functional, Lazy Evaluation", comment_single="--",
        print_statement='putStrLn "Hello, World!"',
        variable_decl="x :: Int\nx = 42",
        function_decl="tambah :: Int -> Int -> Int\ntambah a b = a + b",
        loop_sample="mapM_ print [0..4]",
        sample_code='main :: IO ()\nmain = putStrLn "Halo Haskell Pure Functional"',
        description="Standar emas pemrograman fungsional murni dengan sistem tipe matematis ketat."
    ),
    "elixir": ProgrammingLanguage(
        id="elixir", name="Elixir", category="Functional & Logic", extension=".ex",
        paradigm="Functional, Concurrent, Actor Model", comment_single="#",
        print_statement='IO.puts("Hello, World!")',
        variable_decl="x = 42",
        function_decl="def tambah(a, b) do\n  a + b\nend",
        loop_sample="Enum.each(0..4, &IO.puts/1)",
        sample_code='defmodule Halo do\n  def run, do: IO.puts("Halo Elixir Phoenix BEAM")\nend',
        description="Bahasa fungsional elegan di atas Erlang BEAM dengan skalabilitas masif juta koneksi serentak."
    ),
    "clojure": ProgrammingLanguage(
        id="clojure", name="Clojure", category="Functional & Logic", extension=".clj",
        paradigm="Dynamic Functional Lisp for JVM", comment_single=";",
        print_statement='(println "Hello, World!")',
        variable_decl="(def x 42)",
        function_decl="(defn tambah [a b]\n  (+ a b))",
        loop_sample="(doseq [i (range 5)]\n  (println i))",
        sample_code='(defn -main []\n  (println "Halo Clojure Data-as-Code"))',
        description="Dialek modern Lisp pada JVM dengan struktur data persisten yang tidak dapat diubah (immutable)."
    ),
    "erlang": ProgrammingLanguage(
        id="erlang", name="Erlang", category="Functional & Logic", extension=".erl",
        paradigm="Actor Model, Fault-Tolerant Concurrent", comment_single="%",
        print_statement='io:format("Hello, World!~n").',
        variable_decl="X = 42.",
        function_decl="tambah(A, B) -> A + B.",
        loop_sample="lists:foreach(fun(I) -> io:format(\"~p~n\", [I]) end, lists:seq(0, 4)).",
        sample_code='-module(halo).\n-export([main/0]).\nmain() -> io:format("Halo Erlang BEAM 99.9999999% uptime~n").',
        description="Pondasi telekomunikasi dunia dengan arsitektur ketahanan gangguan luar biasa (Let it crash)."
    ),
    "ocaml": ProgrammingLanguage(
        id="ocaml", name="OCaml", category="Functional & Logic", extension=".ml",
        paradigm="Typed Functional with Imperative/OOP", comment_single="(*",
        print_statement='print_endline "Hello, World!";;',
        variable_decl="let x = 42;;",
        function_decl="let tambah a b = a + b;;",
        loop_sample="for i = 0 to 4 do print_int i; print_newline () done;;",
        sample_code='let () = print_endline "Halo OCaml Type Inference";;',
        description="Bahasa fungsional berkinerja tinggi yang menjadi dasar kompilator Rust awal dan ekosistem Coq."
    ),
    "scheme": ProgrammingLanguage(
        id="scheme", name="Scheme", category="Functional & Logic", extension=".scm",
        paradigm="Minimalist Functional Lisp", comment_single=";",
        print_statement='(display "Hello, World!") (newline)',
        variable_decl="(define x 42)",
        function_decl="(define (tambah a b)\n  (+ a b))",
        loop_sample="(do ((i 0 (+ i 1))) ((= i 5)) (display i) (newline))",
        sample_code='(define (main)\n  (display "Halo Scheme SICP")\n  (newline))',
        description="Dialek Lisp minimalis dan elegan yang diabadikan dalam buku legendaris ilmu komputer SICP."
    ),
    "racket": ProgrammingLanguage(
        id="racket", name="Racket", category="Functional & Logic", extension=".rkt",
        paradigm="Language-oriented Programming", comment_single=";",
        print_statement='(displayln "Hello, World!")',
        variable_decl="(define x 42)",
        function_decl="(define (tambah a b)\n  (+ a b))",
        loop_sample="(for ([i 5])\n  (displayln i))",
        sample_code='#lang racket\n(displayln "Halo Racket Language Design")',
        description="Platform perancangan bahasa pemrograman dan metaprogramming berbasis ekosistem Lisp."
    ),
    "commonlisp": ProgrammingLanguage(
        id="commonlisp", name="Common Lisp", category="Functional & Logic", extension=".lisp",
        paradigm="Multi-paradigm Symbolic Lisp", comment_single=";",
        print_statement='(format t "Hello, World!~%")',
        variable_decl="(defparameter *x* 42)",
        function_decl="(defun tambah (a b)\n  (+ a b))",
        loop_sample="(loop for i from 0 below 5 do (print i))",
        sample_code='(defun main ()\n  (format t "Halo Common Lisp Macros~%"))',
        description="Bahasa simbolik pelopor kecerdasan buatan dengan sistem macro paling kuat dalam sejarah komputasi."
    ),
    "prolog": ProgrammingLanguage(
        id="prolog", name="Prolog", category="Functional & Logic", extension=".pl",
        paradigm="Logic Programming, Constraint-based", comment_single="%",
        print_statement='write(\'Hello, World!\'), nl.',
        variable_decl="x(42).",
        function_decl="tambah(A, B, Res) :- Res is A + B.",
        loop_sample="between(1, 5, I), writeln(I), fail; true.",
        sample_code='main :- write(\'Halo Prolog Knowledge Inference\'), nl.',
        description="Bahasa pemrograman logika deklaratif berdasarkan relasi fakta, aturan, dan mesin inferensi."
    ),
    "purescript": ProgrammingLanguage(
        id="purescript", name="PureScript", category="Functional & Logic", extension=".purs",
        paradigm="Pure Functional compiling to JS", comment_single="--",
        print_statement='log "Hello, World!"',
        variable_decl="x :: Int\nx = 42",
        function_decl="tambah :: Int -> Int -> Int\ntambah a b = a + b",
        loop_sample='for_ (0 .. 4) logShow',
        sample_code='module Main where\nimport Effect.Console (log)\nmain = log "Halo PureScript Web"',
        description="Bahasa fungsional murni mirip Haskell yang dikompilasi langsung ke kode JavaScript bersih."
    ),

    # --- Category 7: DevOps, Shell & Infrastructure (10) ---
    "bash": ProgrammingLanguage(
        id="bash", name="Bash", category="DevOps & Shell", extension=".sh",
        paradigm="Unix Shell Scripting", comment_single="#",
        print_statement='echo "Hello, World!"',
        variable_decl="x=42",
        function_decl="tambah() {\n    echo $(($1 + $2))\n}",
        loop_sample="for i in {0..4}; do\n    echo $i\ndone",
        sample_code='#!/bin/bash\necho "Halo dari Shell Bash Linux"',
        description="Standar otomasi administrasi sistem Unix/Linux di jutaan server dunia."
    ),
    "powershell": ProgrammingLanguage(
        id="powershell", name="PowerShell", category="DevOps & Shell", extension=".ps1",
        paradigm="Object-oriented Command Shell", comment_single="#",
        print_statement='Write-Output "Hello, World!"',
        variable_decl="$x = 42",
        function_decl="function Tambah($a, $b) {\n    return $a + $b\n}",
        loop_sample="0..4 | ForEach-Object { Write-Output $_ }",
        sample_code='Write-Host "Halo PowerShell .NET Pipeline"',
        description="Shell otomasi berbasis objek dari Microsoft untuk administrasi cloud lintas OS."
    ),
    "fish": ProgrammingLanguage(
        id="fish", name="Fish Shell", category="DevOps & Shell", extension=".fish",
        paradigm="User-friendly Command Shell", comment_single="#",
        print_statement='echo "Hello, World!"',
        variable_decl="set x 42",
        function_decl="function tambah\n    math $argv[1] + $argv[2]\nend",
        loop_sample="for i in (seq 0 4); echo $i; end",
        sample_code='echo "Halo Smart Interactive Fish Shell"',
        description="Shell interaktif modern dengan fitur auto-suggestion dan konfigurasi intuitif."
    ),
    "awk": ProgrammingLanguage(
        id="awk", name="AWK", category="DevOps & Shell", extension=".awk",
        paradigm="Pattern-directed Text Processing", comment_single="#",
        print_statement='print "Hello, World!"',
        variable_decl="x = 42",
        function_decl="function tambah(a, b) {\n    return a + b\n}",
        loop_sample="for (i = 0; i < 5; i++) print i",
        sample_code='BEGIN { print "Halo AWK Stream Processor" }',
        description="Bahasa pengolahan teks berbasis baris dan kolom yang sangat cepat di lingkungan Unix."
    ),
    "sed": ProgrammingLanguage(
        id="sed", name="Sed", category="DevOps & Shell", extension=".sed",
        paradigm="Stream Editor Language", comment_single="#",
        print_statement='1i\\\nHello, World!',
        variable_decl='s/lama/baru/g',
        function_decl=':loop; n; b loop',
        loop_sample='1,5p',
        sample_code='s/foo/bar/g',
        description="Editor aliran teks legendaris untuk transformasi pola teks secara on-the-fly."
    ),
    "makefile": ProgrammingLanguage(
        id="makefile", name="Makefile (GNU Make)", category="DevOps & Shell", extension="",
        paradigm="Declarative Build Automation", comment_single="#",
        print_statement='@echo "Hello, World!"',
        variable_decl="X = 42",
        function_decl="build:\n\t@echo \"Building...\"",
        loop_sample="test: ; @for i in 1 2 3 4 5; do echo $$i; done",
        sample_code='all: build run\nbuild:\n\tgcc main.c -o app\nrun:\n\t./app',
        description="Standar otomasi orkestrasi build dan dependensi kompilasi perangkat lunak."
    ),
    "cmake": ProgrammingLanguage(
        id="cmake", name="CMake", category="DevOps & Shell", extension=".cmake",
        paradigm="Cross-platform Build Generator", comment_single="#",
        print_statement='message("Hello, World!")',
        variable_decl="set(X 42)",
        function_decl="function(tambah a b)\n  math(EXPR res \"${a} + ${b}\")\nendfunction()",
        loop_sample="foreach(i RANGE 0 4)\n  message(\"${i}\")\nendforeach()",
        sample_code='cmake_minimum_required(VERSION 3.20)\nproject(UH0Project CXX)\nadd_executable(app main.cpp)',
        description="Generator sistem build lintas platform untuk proyek C/C++ modern berskala besar."
    ),
    "dockerfile": ProgrammingLanguage(
        id="dockerfile", name="Dockerfile", category="DevOps & Shell", extension="",
        paradigm="Container Image Specification", comment_single="#",
        print_statement='RUN echo "Hello, World!"',
        variable_decl="ENV X=42",
        function_decl="HEALTHCHECK CMD curl -f http://localhost/ || exit 1",
        loop_sample='RUN for i in 1 2 3; do echo $i; done',
        sample_code='FROM python:3.12-slim\nWORKDIR /app\nCOPY . .\nCMD ["python3", "train.py"]',
        description="Spesifikasi cetak biru kontainerisasi aplikasi Docker yang terisolasi."
    ),
    "toml": ProgrammingLanguage(
        id="toml", name="TOML", category="DevOps & Shell", extension=".toml",
        paradigm="Minimal Config Specification", comment_single="#",
        print_statement='message = "Hello, World!"',
        variable_decl='x = 42',
        function_decl='[package]\nname = "uh-zero"\nversion = "1.0.0"',
        loop_sample='numbers = [1, 2, 3, 4, 5]',
        sample_code='[model]\ndim = 128\nlayers = 4\nlanguages = 80',
        description="Format konfigurasi sederhana yang digunakan luas oleh Cargo Rust dan pyproject.toml."
    ),
    "zsh": ProgrammingLanguage(
        id="zsh", name="Zsh (Z Shell)", category="DevOps & Shell", extension=".zsh",
        paradigm="Enhanced Unix Shell", comment_single="#",
        print_statement='print "Hello, World!"',
        variable_decl="typeset -i x=42",
        function_decl="tambah() { print $(($1 + $2)) }",
        loop_sample="repeat 5 print $i",
        sample_code='#!/bin/zsh\nprint "Halo Oh-My-Zsh Developer Experience"',
        description="Shell default di macOS dan alternatif populer pengembang dengan plugin dan autokomplet canggih."
    ),

    # --- Category 8: Hardware, Smart Contracts & Emerging (10) ---
    "solidity": ProgrammingLanguage(
        id="solidity", name="Solidity", category="Emerging & Specialized", extension=".sol",
        paradigm="Contract-oriented Smart Contracts", comment_single="//",
        print_statement='emit Log("Hello, World!");',
        variable_decl="uint256 public x = 42;",
        function_decl="function tambah(uint256 a, uint256 b) public pure returns (uint256) {\n    return a + b;\n}",
        loop_sample="for (uint i = 0; i < 5; i++) { /* loop */ }",
        sample_code='// SPDX-License-Identifier: MIT\npragma solidity ^0.8.20;\ncontract Halo {\n    string public pesan = "Halo EVM Blockchain";\n}',
        description="Bahasa utama penulisan smart contract di jaringan Ethereum dan blockchain EVM."
    ),
    "vyper": ProgrammingLanguage(
        id="vyper", name="Vyper", category="Emerging & Specialized", extension=".vy",
        paradigm="Pythonic Smart Contracts", comment_single="#",
        print_statement='log LogEvent("Hello, World!")',
        variable_decl="x: public(uint256)",
        function_decl="@external\n@pure\ndef tambah(a: uint256, b: uint256) -> uint256:\n    return a + b",
        loop_sample="for i: uint256 in range(5):\n    pass",
        sample_code='# @version ^0.3.7\npesan: public(String[100])\n@external\ndef __init__():\n    self.pesan = "Halo Vyper Secure Smart Contract"',
        description="Alternatif smart contract bergaya Python dengan fokus maksimal pada audit keamanan kode."
    ),
    "fortran": ProgrammingLanguage(
        id="fortran", name="Fortran (Modern 2018)", category="Emerging & Specialized", extension=".f90",
        paradigm="Numerical & Scientific Computing", comment_single="!",
        print_statement='print *, "Hello, World!"',
        variable_decl="integer :: x = 42",
        function_decl="function tambah(a, b) result(res)\n    integer, intent(in) :: a, b\n    integer :: res\n    res = a + b\nend function",
        loop_sample="do i = 1, 5\n    print *, i\nend do",
        sample_code='program hello\n    implicit none\n    print *, "Halo Fortran Supercomputer Weather Forecasting"\nend program hello',
        description="Pondasi utama simulasi fisika dan komputasi superkomputer cuaca di dunia."
    ),
    "pascal": ProgrammingLanguage(
        id="pascal", name="Pascal / FreePascal", category="Emerging & Specialized", extension=".pas",
        paradigm="Structured Procedural", comment_single="//",
        print_statement='writeln(\'Hello, World!\');',
        variable_decl="var x: Integer = 42;",
        function_decl="function Tambah(a, b: Integer): Integer;\nbegin\n    Tambah := a + b;\nend;",
        loop_sample="for i := 1 to 5 do writeln(i);",
        sample_code='program Halo;\nbegin\n    writeln(\'Halo Pascal Struktur Kuat\');\nend.',
        description="Pelopor pengajaran pemrograman terstruktur yang melahirkan Delphi dan FreePascal."
    ),
    "ada": ProgrammingLanguage(
        id="ada", name="Ada (SPARK)", category="Emerging & Specialized", extension=".adb",
        paradigm="High-integrity Safety-critical", comment_single="--",
        print_statement='Put_Line ("Hello, World!");',
        variable_decl="X : Integer := 42;",
        function_decl="function Tambah (A, B : Integer) return Integer is\nbegin\n    return A + B;\nend Tambah;",
        loop_sample="for I in 1 .. 5 loop\n    Put (I);\nend loop;",
        sample_code='with Ada.Text_IO; use Ada.Text_IO;\nprocedure Hello is\nbegin\n    Put_Line ("Halo Ada Avionic Safety Critical");\nend Hello;',
        description="Bahasa dengan sertifikasi keamanan tertinggi untuk sistem penerbangan (avionik) dan militer."
    ),
    "forth": ProgrammingLanguage(
        id="forth", name="Forth", category="Emerging & Specialized", extension=".fth",
        paradigm="Stack-based Concatenative", comment_single="\\",
        print_statement='." Hello, World!" cr',
        variable_decl="42 VALUE x",
        function_decl=": TAMBAH ( a b -- c ) + ;",
        loop_sample="5 0 DO I . LOOP",
        sample_code=': HALO ." Halo Forth Stack Engine" CR ;',
        description="Bahasa berbasis tumpukan (stack) ultra-minimalis yang digunakan pada firmware hardware."
    ),
    "apl": ProgrammingLanguage(
        id="apl", name="APL", category="Emerging & Specialized", extension=".apl",
        paradigm="Array-oriented Symbolic", comment_single="⍝",
        print_statement='\'Hello, World!\'',
        variable_decl="x ← 42",
        function_decl="tambah ← {⍺ + ⍵}",
        loop_sample="⍳5",
        sample_code='⍝ Komputasi rata-rata vektor array\n{(+/⍵)÷⍴⍵} 1 2 3 4 5',
        description="Bahasa simbolik berbasis array ringkas yang mampu menyelesaikan kalkulasi kompleks dalam satu baris."
    ),
    "elm": ProgrammingLanguage(
        id="elm", name="Elm", category="Emerging & Specialized", extension=".elm",
        paradigm="Pure Functional Frontend Architecture", comment_single="--",
        print_statement='text "Hello, World!"',
        variable_decl="x : Int\nx = 42",
        function_decl="tambah : Int -> Int -> Int\ntambah a b = a + b",
        loop_sample="List.map String.fromInt (List.range 0 4)",
        sample_code='import Html exposing (text)\nmain = text "Halo Elm Zero Runtime Exception"',
        description="Bahasa frontend yang menjamin 0 kesalahan runtime (No runtime exceptions in production)."
    ),
    "reasonml": ProgrammingLanguage(
        id="reasonml", name="ReasonML / ReScript", category="Emerging & Specialized", extension=".re",
        paradigm="OCaml for JS Ecosystem", comment_single="//",
        print_statement='Js.log("Hello, World!");',
        variable_decl="let x = 42;",
        function_decl="let tambah = (a, b) => a + b;",
        loop_sample="for (i in 0 to 4) { Js.log(i); };",
        sample_code='let pesan = "Halo ReScript React Fast Compile";\nJs.log(pesan);',
        description="Sintaks JavaScript di atas fondasi OCaml yang mengkompilasi React sangat cepat."
    ),
    "vhdl": ProgrammingLanguage(
        id="vhdl", name="VHDL / Verilog", category="Emerging & Specialized", extension=".vhd",
        paradigm="Hardware Description Language", comment_single="--",
        print_statement='report "Hello, World!";',
        variable_decl="signal x : integer := 42;",
        function_decl="function tambah(a, b : integer) return integer is\nbegin return a + b; end;",
        loop_sample="for i in 0 to 4 loop null; end loop;",
        sample_code='entity HALO is end entity;\narchitecture BEHAVIOR of HALO is\nbegin\n  process begin\n    report "Halo VHDL Silicon Synthesis";\n    wait;\n  end process;\nend architecture;',
        description="Bahasa deskripsi perangkat keras untuk merancang sirkuit chip prosesor dan FPGA."
    ),
}


def get_all_languages() -> List[ProgrammingLanguage]:
    return list(LANGUAGES_CATALOG.values())


def get_language(lang_id: str) -> Optional[ProgrammingLanguage]:
    return LANGUAGES_CATALOG.get(lang_id.lower())


def get_categories() -> Dict[str, List[ProgrammingLanguage]]:
    cats: Dict[str, List[ProgrammingLanguage]] = {}
    for lang in LANGUAGES_CATALOG.values():
        cats.setdefault(lang.category, []).append(lang)
    return cats
