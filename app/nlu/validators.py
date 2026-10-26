"""Kritik alanlar için deterministik doğrulayıcılar.

LLM'in çıkardığı hiçbir değer bu fonksiyonlardan geçmeden robota (Open Hızlı Teklif'e)
gönderilmez. Her fonksiyon `Sonuc` döner: `gecerli`, normalize edilmiş `deger` ve
geçersizse müşteriye gösterilebilecek Türkçe `hata` mesajı.
"""

import re
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Optional

_TR_UPPER = str.maketrans({"i": "İ", "ı": "I"})
_TR_LOWER = str.maketrans({"İ": "i", "I": "ı"})
_ASCII = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def tr_upper(metin: str) -> str:
    return metin.translate(_TR_UPPER).upper()


def tr_lower(metin: str) -> str:
    return metin.translate(_TR_LOWER).lower()


def ascii_katla(metin: str) -> str:
    """Türkçe karakterleri ASCII karşılığına çevirir (ş→s, ı→i ...)."""
    return metin.translate(_ASCII)


@dataclass(frozen=True)
class Sonuc:
    gecerli: bool
    deger: Any = None
    hata: Optional[str] = None
    ek: Optional[dict] = None

    @classmethod
    def ok(cls, deger, **ek):
        return cls(True, deger, None, ek or None)

    @classmethod
    def hatali(cls, hata):
        return cls(False, None, hata)


def _rakamlar(metin: str) -> str:
    return re.sub(r"[\s.\-]", "", metin or "")


# --- TC Kimlik No ------------------------------------------------------------

def tc_kimlik_dogrula(metin: str) -> Sonuc:
    tc = _rakamlar(metin)
    if not re.fullmatch(r"\d{11}", tc):
        return Sonuc.hatali("T.C. kimlik numarası 11 haneli olmalıdır.")
    d = [int(c) for c in tc]
    if d[0] == 0:
        return Sonuc.hatali("T.C. kimlik numarası 0 ile başlayamaz.")
    tek = d[0] + d[2] + d[4] + d[6] + d[8]
    cift = d[1] + d[3] + d[5] + d[7]
    if (tek * 7 - cift) % 10 != d[9] or sum(d[:10]) % 10 != d[10]:
        return Sonuc.hatali("T.C. kimlik numarası geçerli görünmüyor, lütfen kontrol eder misiniz?")
    return Sonuc.ok(tc)


# --- Vergi Kimlik No (tüzel kişi) -------------------------------------------

def vergi_no_dogrula(metin: str) -> Sonuc:
    """10 haneli VKN; GİB'in yaygın bilinen kontrol hanesi algoritması.

    Not: Algoritma gerçek bir VKN ile henüz doğrulanmadı (bkz. docs/03_is_kurallari.md).
    """
    vkn = _rakamlar(metin)
    if not re.fullmatch(r"\d{10}", vkn):
        return Sonuc.hatali("Vergi kimlik numarası 10 haneli olmalıdır.")
    d = [int(c) for c in vkn]
    toplam = 0
    for i in range(9):
        tmp = (d[i] + 9 - i) % 10
        tmp2 = (tmp * 2 ** (9 - i)) % 9
        if tmp != 0 and tmp2 == 0:
            tmp2 = 9
        toplam += tmp2
    if (10 - toplam % 10) % 10 != d[9]:
        return Sonuc.hatali("Vergi kimlik numarası geçerli görünmüyor, lütfen kontrol eder misiniz?")
    return Sonuc.ok(vkn)


# --- Plaka -------------------------------------------------------------------

_PLAKA = re.compile(r"(\d{2})([A-Z]{1,3})(\d{2,5})")
_YENI_KAYIT = re.compile(r"(\d{2})YK(\d{0,5})")
# Harf sayısına göre izin verilen rakam sayıları (TR plaka düzeni).
_RAKAM_SAYISI = {1: (4, 5), 2: (3, 4), 3: (2, 3)}


def plaka_dogrula(metin: str) -> Sonuc:
    """TR plaka. Plakasız (sıfır) araçta acente il kodu + 'YK' (yeni kayıt) girer: '34YK'."""
    p = re.sub(r"[\s\-]", "", tr_upper(metin or ""))
    yk = _YENI_KAYIT.fullmatch(p)
    if yk:
        il = int(yk.group(1))
        if not 1 <= il <= 81:
            return Sonuc.hatali("Plakadaki il kodu 01 ile 81 arasında olmalıdır.")
        return Sonuc.ok(p, il_kodu=il, yeni_kayit=True, gorunum=f"{yk.group(1)} YK {yk.group(2)}".strip())
    m = _PLAKA.fullmatch(p)
    if not m:
        return Sonuc.hatali("Plaka geçerli görünmüyor (örnek: 34 ABC 123).")
    il, harf, rakam = int(m.group(1)), m.group(2), m.group(3)
    if not 1 <= il <= 81:
        return Sonuc.hatali("Plakadaki il kodu 01 ile 81 arasında olmalıdır.")
    en_az, en_cok = _RAKAM_SAYISI[len(harf)]
    if not en_az <= len(rakam) <= en_cok:
        return Sonuc.hatali("Plaka geçerli görünmüyor (örnek: 34 ABC 123).")
    return Sonuc.ok(p, il_kodu=il, yeni_kayit=False, gorunum=f"{m.group(1)} {harf} {rakam}")


def yeni_kayit_plakasi(il_kodu: int) -> str:
    if not 1 <= il_kodu <= 81:
        raise ValueError("il kodu 1-81 olmalı")
    return f"{il_kodu:02d}YK"


# --- Ruhsat belge seri / no --------------------------------------------------

def belge_seri_dogrula(metin: str) -> Sonuc:
    """Araç tescil belgesi (ruhsat) 'Belge Seri': 2 harf + 6 rakam (ör. 'AB 123456').

    Değer `{'seri': 'AB', 'no': '123456'}` olarak döner; Open Hızlı Teklif'te iki ayrı kutuya girilir.
    """
    b = re.sub(r"[\s\-/]", "", tr_upper(metin or ""))
    m = re.fullmatch(r"([A-ZÇĞİÖŞÜ]{2})(\d{6})", b)
    if not m:
        return Sonuc.hatali(
            "Ruhsat belge seri numarası 2 harf ve 6 rakamdan oluşur (örnek: AB 123456). "
            "Ruhsatın ön yüzünde 'Belge Seri' olarak yazar."
        )
    return Sonuc.ok({"seri": m.group(1), "no": m.group(2)})


# --- Tarihler ----------------------------------------------------------------

_TARIH_BICIMLERI = ("%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d %m %Y")


def tarih_coz(metin: str) -> Optional[date]:
    t = (metin or "").strip()
    for bicim in _TARIH_BICIMLERI:
        try:
            return datetime.strptime(t, bicim).date()
        except ValueError:
            continue
    return None


def dogum_tarihi_dogrula(metin: str, bugun: Optional[date] = None) -> Sonuc:
    bugun = bugun or date.today()
    d = tarih_coz(metin)
    if d is None:
        return Sonuc.hatali("Doğum tarihini gün.ay.yıl şeklinde yazar mısınız? (örnek: 08.08.1987)")
    yas = bugun.year - d.year - ((bugun.month, bugun.day) < (d.month, d.day))
    if d >= bugun or yas < 18:
        return Sonuc.hatali("Araç sahibinin 18 yaşından büyük olması gerekir; doğum tarihini kontrol eder misiniz?")
    if yas > 110:
        return Sonuc.hatali("Doğum tarihi geçerli görünmüyor, kontrol eder misiniz?")
    return Sonuc.ok(d)


def model_yili_dogrula(metin, bugun: Optional[date] = None) -> Sonuc:
    bugun = bugun or date.today()
    try:
        yil = int(str(metin).strip())
    except ValueError:
        return Sonuc.hatali("Model yılı 4 haneli olmalıdır (örnek: 2020).")
    if not 1950 <= yil <= bugun.year + 1:
        return Sonuc.hatali("Model yılı geçerli görünmüyor.")
    return Sonuc.ok(yil)


# --- Telefon -----------------------------------------------------------------

def telefon_normalize(metin: str) -> Sonuc:
    """Türkiye cep telefonu → '905XXXXXXXXX' (WhatsApp formatı)."""
    t = re.sub(r"[^\d]", "", metin or "")
    if t.startswith("90") and len(t) == 12:
        t = t[2:]
    elif t.startswith("0") and len(t) == 11:
        t = t[1:]
    if not re.fullmatch(r"5\d{9}", t):
        return Sonuc.hatali("Cep telefonu numarası geçerli görünmüyor (örnek: 0532 123 45 67).")
    return Sonuc.ok("90" + t)


# --- Maskeleme (log / panel) -------------------------------------------------

def maskele(deger: str, acik: int = 4) -> str:
    """Loglarda kişisel veriyi gizler: '54691206272' → '*******6272'."""
    s = str(deger or "")
    if len(s) <= acik:
        return "*" * len(s)
    return "*" * (len(s) - acik) + s[-acik:]
