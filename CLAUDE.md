# Workspace Riset, Kerja & Tesis

User adalah pekerja sekaligus mahasiswa. Bahasa utama: Indonesia.

## Subagent (`.claude/agents/`)
- `mandor` — QA dan penjaga jalur. Memeriksa hasil terhadap BRIEF.md, membuat brief, triase tugas, memantau tesis.
- `peneliti` — riset literatur dan pencarian sumber
- `penulis-paper` — outline, draf, revisi
- `validator-dokumen` — cek sitasi, fakta, konsistensi, pedoman

Semua subagent memakai model `sonnet` supaya kuota lebih hemat. Setiap subagent tetap memakai kuota yang sama dengan sesi utama. Subagent BUKAN cara gratis, jadi panggil hanya kalau perlu.

## Struktur
- `tugas/<slug>/BRIEF.md` — instruksi asli + rubrik + deadline. Semua output tugas ada di folder ini.
- `tugas/DAFTAR.md` — daftar tugas dan prioritas
- `tesis/` — tesis (BRIEF.md, PROGRESS.md, bab/, catatan/)

## Kapan TIDAK memakai subagent
Pertanyaan singkat, edit kecil, satu paragraf, atau cek cepat → kerjakan langsung di sesi utama. Memanggil subagent untuk hal kecil justru lebih boros dan lebih lambat.

## Mode kerja
Default **mode hemat**. Pakai **mode ketat** hanya jika user bilang "mode ketat" atau tugasnya bernilai besar (tesis, tugas akhir, bobot ≥ 30%).

### Mode hemat (default)
1. Tugas baru → buat BRIEF.md dari template (sesi utama boleh membuatnya sendiri; panggil `mandor` hanya jika instruksinya panjang/ambigu). Tanpa BRIEF, jangan mulai.
2. **Riset paralel:** pecah pertanyaan riset menjadi 2–3 sub-topik yang independen, lalu panggil beberapa `peneliti` **sekaligus dalam satu giliran** (bukan satu per satu). Maksimal 3 sekaligus.
3. `penulis-paper` menulis dari file `riset-*.md`.
4. `mandor` mereview **sekali di akhir** atas hasil akhir. Maksimal **1 putaran revisi**; kalau masih REVISI, eskalasi ke user dengan ringkasan masalahnya.
5. Perbarui checklist di BRIEF.md dan `tugas/DAFTAR.md` (atau `tesis/PROGRESS.md`).

### Mode ketat
Sama seperti mode hemat, tetapi `mandor` mereview **setelah setiap langkah**, dan maksimal **2 putaran revisi** per langkah sebelum eskalasi.

### Aturan vonis
- Jangan tunjukkan hasil ke user sebagai "selesai" sebelum mandor memberi vonis LOLOS.
- REVISI → panggil ulang agent yang sama dengan path `REVIEW-<n>.md`.
- ESKALASI → berhenti dan tanyakan ke user dengan konteks yang cukup.

## Hemat konteks
- Subagent membalas ringkas (≤ ~150 kata + path file). Sesi utama jangan membaca ulang file lengkap kecuali perlu.
- Jangan mengulang riset yang sudah ada di `riset-*.md`. Baca dulu sebelum memanggil `peneliti`.

## Aturan bersama
- Jangan pernah mengarang sumber, kutipan, data, atau angka. Tandai yang belum terverifikasi.
- Bedakan fakta, inferensi, dan tebakan.
- Tantang asumsi yang lemah sebelum membantu menyempurnakan.
