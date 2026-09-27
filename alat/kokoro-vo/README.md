# Kokoro VO (bahasa Indonesia)

Membuat voice over untuk video BYD dengan [Kokoro TTS](https://github.com/hexgrad/kokoro) (lisensi Apache).

> ⚠️ **Status: BELUM DIUJI.** Sesi Claude yang membuat skrip ini tidak bisa mengunduh model dari HuggingFace karena diblokir jaringan.
> Kokoro juga tidak resmi mendukung bahasa Indonesia. Skrip ini mengakalinya dengan fonem espeak-ng `id` yang dibacakan oleh suara bahasa lain, jadi aksennya bisa terdengar asing.

## File
- `naskah-byd.json` — naskah 9 scene, diambil dari artifact Studio VO BYD Indonesia
- `pengucapan.json` — perbaikan pengucapan istilah asing dan angka. Edit kalau ada kata yang terdengar salah.
- `buat_vo.py` — skrip generator

## Jalankan di Google Colab (gratis, tanpa instal di laptop)
1. Buka https://colab.research.google.com, lalu buat notebook baru.
2. Unggah ketiga file di atas lewat panel Files di kiri.
3. Jalankan:
```
!apt-get -qq -y install espeak-ng > /dev/null
!pip install -q kokoro soundfile
!python buat_vo.py sampel
```
4. Dengarkan `hasil/sampel_*.wav`, lalu pilih suara terbaik. `ef_dora` dan `em_alex` adalah suara Spanyol, yang menurut dugaan bunyinya paling dekat dengan bahasa Indonesia, tapi ini belum dibuktikan.
5. Jalankan untuk semua scene:
```
!python buat_vo.py semua ef_dora
```
6. Unduh `hasil/vo-byd.zip`, ekstrak, lalu di Studio VO klik **"Muat 9 file per scene"** dan pilih vo01–vo09.

## Kalau hasilnya jelek
- Ada kata yang salah ucap: tambahkan ke `pengucapan.json` dengan format `"asli": "ejaan bunyi"`.
- Terlalu cepat: `!python buat_vo.py semua ef_dora 0.9`
- Aksen tidak bisa diterima: Kokoro memang tidak cocok untuk bahasa Indonesia. Pertimbangkan TTS yang resmi mendukung bahasa Indonesia.
