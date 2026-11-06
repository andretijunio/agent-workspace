# Catatan evaluasi OpenMontage (commit d21f5d4, sandbox tanpa API key)

## Fakta terverifikasi (dijalankan di sandbox)
- `make setup`: sukses tanpa error, ~66 detik (Python 3.13, Node 22).
- Tool registry: 37 tool tersedia, 117 tidak tersedia, 1 degraded.
- Tersedia: ffmpeg/Remotion/HyperFrames compose, subtitle_gen, pixabay_music, threejs_world, character_rig_renderer, video_analyzer.
- TIDAK tersedia tanpa setup/key: `piper_tts` (model suara belum diunduh), `clip_search` (butuh torch + transformers + corpus), `pexels_video` (butuh PEXELS_API_KEY), semua generator video/gambar AI.
- `corpus_builder` degraded: butuh minimal satu sumber stok terkonfigurasi (Pexels/Unsplash) + opencv/torch/transformers.

## Selisih dengan klaim README (README: "zero keys" jalur footage nyata)
- Dari registry yang saya lihat, tool bernama archive_org / nasa / wikimedia tidak muncul. Mungkin ada di tempat lain (belum saya telusuri). Jangan simpulkan klaimnya salah; baru "belum terverifikasi".
- Jalur footage nyata di praktik tampaknya butuh PEXELS_API_KEY (gratis) dan dependensi berat (torch).

## Belum diketahui
- Apakah unduhan model Piper dan Hugging Face bisa lewat proxy sandbox.
- Dukungan Piper untuk Bahasa Indonesia.
- Kualitas output sebenarnya (belum ada render).
