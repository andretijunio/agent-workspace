# agent-workspace

Kumpulan subagent Claude Code untuk riset, validasi dokumen, penulisan paper, dan manajemen tesis.

## Struktur
```
.claude/agents/
  mandor-tesis.md       # manajer proyek tesis
  peneliti.md           # riset literatur
  penulis-paper.md      # outline & draf
  validator-dokumen.md  # cek sitasi, fakta, konsistensi
tesis/PROGRESS.md       # status tesis (diisi oleh mandor)
tesis/bab/              # draf bab
riset/                  # hasil riset
paper/                  # draf paper/tugas
validasi/               # laporan validasi
```

## Cara pakai
Buka Claude Code di folder ini, lalu minta secara natural atau sebut nama agent-nya:
- "Pakai mandor-tesis, bantu aku isi profil tesis dan buat rencana 8 minggu"
- "Pakai peneliti, cari 10 paper terbaru tentang <topik>"
- "Pakai penulis-paper, buat outline Bab 2 dari riset/<file>.md"
- "Pakai validator-dokumen, cek draf.docx terhadap pedoman kampus"

Ketik `/agents` untuk melihat atau mengedit agent.
