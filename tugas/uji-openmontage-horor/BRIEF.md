# BRIEF: Uji coba OpenMontage untuk short horor

- Mata kuliah / pekerjaan: Eksperimen pribadi (alur produksi video)
- Dari: User
- Deadline: tidak ada
- Bobot nilai / pentingnya: rendah (eksperimen); keputusan akhir: pakai OpenMontage atau tidak
- Jenis output: 1 video short horor percobaan + catatan evaluasi
- Format: 30–45 detik, vertikal 9:16 (ASUMSI, belum dikonfirmasi user), bahasa Inggris untuk narasi (ASUMSI: dukungan Piper TTS untuk Bahasa Indonesia belum diverifikasi)
- Aturan AI dari dosen: tidak berlaku

## Instruksi asli
"Aku mau coba short horor beb" (konteks: repo https://github.com/calesthio/OpenMontage, commit d21f5d4, di-clone ke /home/user/calesthio/openmontage). Lalu: "Yuk coba".

## Rubrik penilaian
Pembanding: satu video dari alur horor lama user (skill `paket-short-horor-sekali-jalan` dll.) dengan tema sama. Nilai: atmosfer, ritme, konsistensi visual, biaya, waktu, usaha manual.

## Batasan yang diketahui
- Sandbox TIDAK punya API key (fal, Kling, ElevenLabs, Google, Pexels, dll.) -> hanya jalur gratis: Piper TTS, Archive.org/NASA/Wikimedia, Remotion/HyperFrames, FFmpeg.
- Jalur gratis kemungkinan menghasilkan montage footage arsip, bukan klip horor generatif. Itu bukan perbandingan adil dengan alur berbayar.
- Pipeline paling dekat: `cinematic` (tidak ada pipeline horor khusus).
- `make setup` hanya dijalankan di sandbox, bukan mesin utama.

## File pendukung
- catatan-evaluasi.md (diisi setelah percobaan)

## Rencana langkah
- [x] 1. Jalankan `make setup` di sandbox, catat error — agent: sesi utama
- [x] 2. Cek support envelope tool (tool apa yang aktif tanpa key) — agent: sesi utama
- [ ] 3. Satu percobaan pipeline `cinematic`/`documentary-montage` bertema horor, real footage only, tanpa narasi atau dengan Piper — agent: sesi utama
- [ ] 4. Catat hasil, waktu, masalah di catatan-evaluasi.md — agent: sesi utama
- [ ] 5. Review hasil terhadap brief — agent: mandor

## Catatan / keputusan user
- Pertanyaan belum dijawab: bahasa/platform, gaya, key dan batas biaya. Asumsi di atas dipakai sampai dikoreksi.
