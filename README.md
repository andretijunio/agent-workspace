# agent-workspace

Subagent Claude Code untuk riset, validasi dokumen, penulisan paper, dan tesis. Ada satu **mandor** yang memeriksa setiap hasil kerja terhadap instruksi tugas.

## Alur
```
Instruksi dosen → mandor (buat BRIEF) → agent pekerja → mandor (review)
                                             ↑              │
                                             └── REVISI ────┘  (maks 2x, lalu ke kamu)
```

## Struktur
```
.claude/agents/          mandor, peneliti, penulis-paper, validator-dokumen
tugas/DAFTAR.md          semua tugas + prioritas
tugas/_template/BRIEF.md template brief
tugas/<slug>/            satu folder per tugas (BRIEF, riset, draf, REVIEW)
tesis/                   BRIEF.md, PROGRESS.md, bab/, catatan/
```

## Contoh perintah
- "Tugas baru: <salin-tempel instruksi dosen>. Deadline Jumat."
- "Kerjakan tugas/metopen-week5 sampai lolos mandor."
- "Mandor, minggu ini aku cuma punya 6 jam. Apa yang dikerjakan duluan?"

Folder lama `riset/`, `paper/`, `validasi/` sudah tidak dipakai dan boleh dihapus.
