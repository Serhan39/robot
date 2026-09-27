"""FAZ 1-2 ortam analizi.

Open Hizli Teklif'in kurulu oldugu Windows bilgisayarda calistirin:

    python tools/ortam_analizi.py --pencere "Teklif"

Toplananlar: Windows/Python/Node surumleri, ekran ve DPI, kurulu RPA/OCR
kutuphaneleri, Open Hizli Teklif ile ilgili surecler/kisayollar ve (pywinauto
kuruluysa) eslesen pencerenin UI Automation agaci.

Okunmayanlar: alan degerleri (ValuePattern), sifreler, pano. 6+ haneli sayi
dizileri maskelenir. Yine de ciktiyi gondermeden once gozden gecirin ve analizi
gercek musteri verisi gorunmeyen bir ekranda yapin.
"""

import argparse
import csv
import ctypes
import importlib.util
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ANAHTAR_KELIMELER = ("open", "hizli", "hızlı", "teklif")

KUTUPHANELER = (
    "pywinauto", "comtypes", "uiautomation", "pyautogui", "pynput", "psutil",
    "cv2", "PIL", "mss", "pytesseract", "paddleocr", "easyocr",
    "playwright", "selenium", "fastapi", "sqlalchemy", "keyring", "cryptography",
)

_UZUN_SAYI = re.compile(r"\d{6,}")


def maskele(metin):
    if not metin:
        return metin
    return _UZUN_SAYI.sub(lambda m: "*" * (len(m.group()) - 2) + m.group()[-2:], str(metin))


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


def ust_pencereler():
    try:
        from pywinauto import Desktop
    except ImportError:
        return "<pywinauto kurulu degil: pip install pywinauto>"
    pencereler = []
    for pencere in Desktop(backend="uia").windows():
        bilgi = pencere.element_info
        if bilgi.name:
            pencereler.append({
                "baslik": maskele(bilgi.name),
                "sinif": bilgi.class_name,
                "framework": bilgi.framework_id,
                "pid": bilgi.process_id,
            })
    return pencereler


def uia_agaci(baslik_deseni, max_derinlik, max_oge):
    try:
        from pywinauto import Desktop
    except ImportError:
        return "<pywinauto kurulu degil: pip install pywinauto>"
    desen = re.compile(baslik_deseni, re.IGNORECASE)
    adaylar = [p for p in Desktop(backend="uia").windows() if desen.search(p.element_info.name or "")]
    if not adaylar:
        return f"<'{baslik_deseni}' ile eslesen pencere yok>"

    sayac = {"n": 0}

    def dugum(sarmalayici, derinlik):
        sayac["n"] += 1
        bilgi = sarmalayici.element_info
        r = bilgi.rectangle
        kayit = {
            "tip": bilgi.control_type,
            "ad": maskele(bilgi.name),
            "automation_id": bilgi.automation_id,
            "sinif": bilgi.class_name,
            "framework": bilgi.framework_id,
            "etkin": bilgi.enabled,
            "gorunur": bilgi.visible,
            "dikdortgen": [r.left, r.top, r.right, r.bottom],
        }
        if derinlik < max_derinlik and sayac["n"] < max_oge:
            try:
                cocuklar = sarmalayici.children()
            except Exception:  # bazi 3. parti kontroller UIA'da hata verir
                kayit["cocuklar"] = "<okunamadi>"
                return kayit
            if cocuklar:
                kayit["cocuklar"] = [dugum(c, derinlik + 1) for c in cocuklar if sayac["n"] < max_oge]
        return kayit

    return [dugum(p, 0) for p in adaylar]


def main():
    ayrac = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ayrac.add_argument("--pencere", help="UIA agaci dokulecek pencere basligi (regex), orn. 'Teklif'")
    ayrac.add_argument("--derinlik", type=int, default=25)
    ayrac.add_argument("--max-oge", type=int, default=5000)
    ayrac.add_argument("--cikti", default=f"ortam_raporu_{datetime.now():%Y%m%d_%H%M%S}.json")
    args = ayrac.parse_args()

    rapor = {
        "olusturma": datetime.now().isoformat(timespec="seconds"),
        "sistem": sistem_bilgisi(),
        "kutuphaneler": kutuphaneler(),
        "ilgili_surecler": ilgili_surecler(),
        "ilgili_kurulumlar": ilgili_kurulumlar(),
        "ust_pencereler": ust_pencereler() if os.name == "nt" else None,
    }
    if args.pencere:
        rapor["uia_agaci"] = uia_agaci(args.pencere, args.derinlik, args.max_oge)

    Path(args.cikti).write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rapor yazildi: {Path(args.cikti).resolve()}")
    if os.name != "nt":
        print("Uyari: Windows disinda calisti; pencere/UIA bilgisi toplanmadi.")


if __name__ == "__main__":
    main()
