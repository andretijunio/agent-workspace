"""
Buat voice over bahasa Indonesia dengan Kokoro TTS.

Kokoro TIDAK resmi mendukung bahasa Indonesia. Skrip ini memakai espeak-ng
(bahasa 'id') untuk mengubah teks menjadi fonem, lalu fonem itu dibacakan
oleh suara Kokoro dari bahasa lain. Hasilnya bisa terdengar beraksen asing,
jadi dengarkan dulu sampelnya sebelum dipakai.

Cara pakai (Google Colab atau laptop):
    pip install --no-deps kokoro==0.9.4 misaki==0.9.4
    pip install loguru num2words phonemizer-fork espeakng-loader addict soundfile huggingface_hub torch transformers
    # Linux/Colab: apt-get install -y espeak-ng

    python buat_vo.py sampel            # scene 1 dengan beberapa suara -> pilih yang terbaik
    python buat_vo.py semua ef_dora     # semua scene -> vo01.wav ... vo09.wav + vo-byd.zip
    python buat_vo.py semua ef_dora 0.95   # opsional: kecepatan bicara (default 1.0)

Hasil vo01..vo09 bisa langsung dimuat di Studio VO lewat "Muat 9 file per scene".
"""
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import soundfile as sf

# 'spacy' hanya dipakai modul bahasa Inggris Kokoro dan sering gagal diinstal; ganti dengan modul kosong.
if importlib.util.find_spec("spacy") is None:
    import types
    sys.modules["spacy"] = types.ModuleType("spacy")

from kokoro import KPipeline
from misaki import espeak

HERE = Path(__file__).parent
NASKAH = HERE / "naskah-byd.json"
PENGUCAPAN = HERE / "pengucapan.json"
SR = 24000

# Suara yang dicoba di mode sampel. Kode huruf pertama = bahasa asal suara.
SAMPEL_SUARA = ["ef_dora", "em_alex", "if_sara", "im_nicola", "pf_dora", "af_heart"]


def perbaiki_ucapan(teks, kamus):
    # Ganti istilah asing/singkatan dengan ejaan bunyi Indonesia (kunci terpanjang dulu).
    for asal in sorted(kamus, key=len, reverse=True):
        teks = re.sub(re.escape(asal), kamus[asal], teks, flags=re.IGNORECASE)
    return teks


def per_kalimat(teks):
    # Jalur espeak di Kokoro bisa memotong teks panjang, jadi pisahkan per kalimat dengan '\n'.
    return "\n".join(s.strip() for s in re.split(r"(?<=[.?!])\s+", teks) if s.strip())


_pipelines = {}


def pipeline_untuk(suara):
    lang = suara[0]
    if lang not in _pipelines:
        p = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
        p.g2p = espeak.EspeakG2P(language="id")  # paksa fonem bahasa Indonesia
        _pipelines[lang] = p
    return _pipelines[lang]


def sintesis(teks, suara, speed=1.0, jeda=0.35):
    p = pipeline_untuk(suara)
    potongan = []
    diam = np.zeros(int(SR * jeda), dtype=np.float32)
    for _, _, audio in p(teks, voice=suara, speed=speed, split_pattern=r"\n+"):
        potongan += [audio.numpy(), diam]
    return np.concatenate(potongan) if potongan else np.zeros(1, dtype=np.float32)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "sampel"
    naskah = json.loads(NASKAH.read_text(encoding="utf-8"))
    kamus = json.loads(PENGUCAPAN.read_text(encoding="utf-8")) if PENGUCAPAN.exists() else {}
    keluar = HERE / "hasil"
    keluar.mkdir(exist_ok=True)

    if mode == "sampel":
        teks = per_kalimat(perbaiki_ucapan(naskah[0]["text"], kamus))
        for suara in SAMPEL_SUARA:
            audio = sintesis(teks, suara)
            sf.write(keluar / f"sampel_{suara}.wav", audio, SR)
            print(f"sampel_{suara}.wav  {len(audio)/SR:.1f} dtk")
        print("Dengarkan file di folder hasil/, lalu jalankan: python buat_vo.py semua <suara>")
        return

    suara = sys.argv[2] if len(sys.argv) > 2 else "ef_dora"
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    berkas = []
    for sc in naskah:
        teks = per_kalimat(perbaiki_ucapan(sc["text"], kamus))
        audio = sintesis(teks, suara, speed)
        nama = keluar / f"vo{sc['id']:02d}.wav"
        sf.write(nama, audio, SR)
        berkas.append(nama)
        print(f"{nama.name}  {sc['title']:<30} {len(audio)/SR:5.1f} dtk")
    with zipfile.ZipFile(keluar / "vo-byd.zip", "w") as z:
        for b in berkas:
            z.write(b, b.name)
    print(f"Selesai: {keluar/'vo-byd.zip'}")


if __name__ == "__main__":
    main()
