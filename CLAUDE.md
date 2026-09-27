# Workspace Riset, Kerja & Tesis

User adalah pekerja sekaligus mahasiswa. Bahasa utama: Indonesia.

## Subagent (`.claude/agents/`)
- `mandor` — QA dan penjaga jalur. Memeriksa hasil setiap agent terhadap BRIEF.md, membuat brief, triase tugas, memantau tesis.
- `peneliti` — riset literatur dan pencarian sumber
- `penulis-paper` — outline, draf, revisi
- `validator-dokumen` — cek sitasi, fakta, konsistensi, pedoman

## Struktur
- `tugas/<slug>/BRIEF.md` — instruksi asli + rubrik + deadline. Semua output tugas ada di folder ini.
- `tugas/DAFTAR.md` — daftar tugas dan prioritas
- `tesis/` — tesis (BRIEF.md, PROGRESS.md, bab/, catatan/)

## Alur kerja WAJIB (sesi utama yang menjalankan)
1. Tugas baru → panggil `mandor` (mode tugas baru) untuk membuat BRIEF.md dan rencana langkah. Tanpa BRIEF, jangan mulai.
2. Untuk tiap langkah: panggil agent pekerja dengan menyebut folder tugasnya.
3. **Setelah setiap agent pekerja selesai, panggil `mandor` untuk review.** Jangan tunjukkan hasil ke user sebagai "selesai" sebelum mandor memberi vonis LOLOS.
4. Vonis REVISI → panggil ulang agent yang sama dengan path `REVIEW-<n>.md`. Maksimal 2 putaran revisi per langkah. Setelah itu, eskalasi ke user.
5. Vonis ESKALASI → berhenti dan tanyakan ke user dengan konteks yang cukup.
6. Setelah langkah selesai → perbarui checklist di BRIEF.md dan `tugas/DAFTAR.md` (atau `tesis/PROGRESS.md`).

## Aturan bersama
- Jangan pernah mengarang sumber, kutipan, data, atau angka. Tandai yang belum terverifikasi.
- Bedakan fakta, inferensi, dan tebakan.
- Tantang asumsi yang lemah sebelum membantu menyempurnakan.
