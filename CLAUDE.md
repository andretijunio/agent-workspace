# Workspace Riset, Kerja & Tesis

User adalah pekerja sekaligus mahasiswa. Bahasa utama: Indonesia.

## Subagent (`.claude/agents/`)
- `mandor-tesis` — perencanaan & pelacakan tesis. Panggil di awal/akhir sesi kerja tesis.
- `peneliti` — riset literatur & pencarian sumber → `riset/`
- `penulis-paper` — outline, draf, revisi tulisan → `paper/` atau `tesis/bab/`
- `validator-dokumen` — cek sitasi, fakta, konsistensi, pedoman → `validasi/`

Alur tipikal: mandor-tesis → peneliti → penulis-paper → validator-dokumen → mandor-tesis (update progres).

## Aturan bersama
- Jangan pernah mengarang sumber, kutipan, data, atau angka. Tandai yang belum terverifikasi.
- Bedakan fakta, inferensi, dan tebakan.
- Tantang asumsi yang lemah sebelum membantu menyempurnakan.
- `tesis/PROGRESS.md` adalah sumber kebenaran status tesis.
