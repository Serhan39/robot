"""FAZ 1 ortam analizi.

Robotun calisacagi Windows bilgisayarda calistirin:

    python tools/ortam_analizi.py

Toplananlar: Windows/Python/Node surumleri, ekran cozunurlugu ve DPI olcegi,
kurulu ekran okuma/OCR/klavye-fare kutuphaneleri, Open Hizli Teklif'in kurulu
oldugu yer ve calisip calismadigi.

Open Hizli Teklif'in icine girilmez: programa, dosyalarina veya pencere
icerigine dokunulmaz, ekran goruntusu alinmaz.
"""

import argparse
import csv
import ctypes
import importlib.util
import io
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ANAHTAR_KELIMELER = ("open", "hizli", "hızlı", "teklif")

KUTUPHANELER = (
    "pyautogui", "pynput", "psutil",
    "cv2", "PIL", "mss", "pytesseract", "paddleocr", "easyocr",
    "playwright", "selenium", "fastapi", "sqlalchemy", "keyring", "cryptography",
)

def komut(args):
    try:
        cikti = subprocess.run(args, capture_output=True, text=True, timeout=20)
        return (cikti.stdout or cikti.stderr).strip()
    except (OSError, subprocess.SubprocessError) as hata:
        return f"<calismadi: {hata.__class__.__name__}>"


def sistem_bilgisi():
    bilgi = {
        "platform": platform.platform(),
        "windows_surumu": platform.win32_ver() if os.name == "nt" else None,
        "makine": platform.machine(),
        "python": sys.version,
        "python_yolu": sys.executable,
        "node": komut(["node", "--version"]) if shutil.which("node") else None,
        "tesseract": komut(["tesseract", "--version"]).splitlines()[:1] if shutil.which("tesseract") else None,
        "tesseract_diller": komut(["tesseract", "--list-langs"]).splitlines()[1:] if shutil.which("tesseract") else None,
    }
    if os.name == "nt":
        try:
            user32 = ctypes.windll.user32
            gdi32 = ctypes.windll.gdi32
            user32.SetProcessDPIAware()
            hdc = user32.GetDC(0)
            bilgi["ekran"] = {
                "genislik": user32.GetSystemMetrics(0),
                "yukseklik": user32.GetSystemMetrics(1),
                "monitor_sayisi": user32.GetSystemMetrics(80),
                "dpi": gdi32.GetDeviceCaps(hdc, 88),  # LOGPIXELSX; 96 = %100
            }
            user32.ReleaseDC(0, hdc)
        except (AttributeError, OSError) as hata:
            bilgi["ekran"] = f"<okunamadi: {hata}>"
    return bilgi


def kutuphaneler():
    return {ad: importlib.util.find_spec(ad) is not None for ad in KUTUPHANELER}


def ilgili_surecler():
    if os.name != "nt":
        return []
    satirlar = csv.reader(io.StringIO(komut(["tasklist", "/fo", "csv", "/nh"])))
    return sorted({
        satir[0] for satir in satirlar
        if satir and any(k in satir[0].lower() for k in ANAHTAR_KELIMELER)
    })


def ilgili_kurulumlar():
    """Baslat menusu kisayollari ve ClickOnce klasorunde ilgili exe'ler."""
    if os.name != "nt":
        return {}
    kokler = {
        "baslat_menusu": [
            Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
            Path(os.environ.get("PROGRAMDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
        ],
        "clickonce": [Path(os.environ.get("LOCALAPPDATA", "")) / "Apps/2.0"],
        "program_files": [
            Path(os.environ.get("PROGRAMFILES", "")),
            Path(os.environ.get("PROGRAMFILES(X86)", "")),
        ],
    }
    sonuc = {}
    for tur, dizinler in kokler.items():
        bulunan = []
        for dizin in dizinler:
            if not dizin.is_dir():
                continue
            derinlik = 2 if tur == "program_files" else 6
            for yol in _gez(dizin, derinlik):
                if any(k in yol.name.lower() for k in ANAHTAR_KELIMELER) and \
                        yol.suffix.lower() in (".lnk", ".exe", ".appref-ms", ""):
                    bulunan.append(str(yol))
                    if len(bulunan) >= 50:
                        break
        sonuc[tur] = bulunan
    return sonuc


def _gez(dizin, derinlik):
    try:
        for yol in dizin.iterdir():
            yield yol
            if derinlik > 0 and yol.is_dir():
                yield from _gez(yol, derinlik - 1)
    except OSError:
        return


def main():
    ayrac = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ayrac.add_argument("--cikti", default=f"ortam_raporu_{datetime.now():%Y%m%d_%H%M%S}.json")
    args = ayrac.parse_args()

    rapor = {
        "olusturma": datetime.now().isoformat(timespec="seconds"),
        "sistem": sistem_bilgisi(),
        "kutuphaneler": kutuphaneler(),
        "ilgili_surecler": ilgili_surecler(),
        "ilgili_kurulumlar": ilgili_kurulumlar(),
    }

    Path(args.cikti).write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rapor yazildi: {Path(args.cikti).resolve()}")
    if os.name != "nt":
        print("Uyari: Windows disinda calisti; ekran ve kurulum bilgisi toplanmadi.")


if __name__ == "__main__":
    main()
