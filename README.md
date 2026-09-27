# agent-workspace

Subagent Claude Code untuk riset, validasi dokumen, penulisan paper, dan tesis. Ada satu **mandor** yang memeriksa setiap hasil kerja terhadap instruksi tugas.

## Alur
```
Instruksi dosen → BRIEF → peneliti ×2–3 (paralel) → penulis-paper → mandor (review akhir)
                                                        ↑                   │
                                                        └──── REVISI ───────┘  (hemat: maks 1x, ketat: maks 2x)
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
- "Kerjakan tugas/uas-pemasaran, mode ketat."
- "Mandor, minggu ini aku cuma punya 6 jam. Apa yang dikerjakan duluan?"

## Soal kuota
Subagent **tidak** membuat pemakaian lebih kecil secara total. Setiap subagent mulai dari nol dan memakai kuota sendiri. Yang dihemat adalah konteks sesi utama. Penghematan nyata di workspace ini datang dari: model `sonnet` untuk subagent, review mandor sekali di akhir (mode hemat), balasan subagent yang ringkas, dan tidak memakai subagent untuk tugas kecil.
