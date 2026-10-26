"""Trafik sigortası: talep türüne göre gerekli bilgiler ve müşteriye sorulacak sorular.

Kaynak: docs/03_is_kurallari.md. "(doğrulanacak)" notlu kurallar acenteyle teyit edilecek.
"""

from enum import Enum
from typing import Dict, List, Optional


class TalepTuru(str, Enum):
    YENILEME = "YENILEME"  # mevcut sahibin poliçesi yenileniyor → ruhsat sahibinin bilgileri
    YENI_ALIM = "YENI_ALIM"  # ikinci el araç satın alınıyor → alıcının bilgileri, satıcının ruhsatı
    SIFIR_ARAC = "SIFIR_ARAC"  # plakasız yeni araç → plaka = il kodu + 'YK'


TALEP_TURU_SORUSU = (
    "Aracınızın mevcut trafik sigortasını mı yenilemek istiyorsunuz, "
    "yoksa aracı yeni mi satın alıyorsunuz?"
)

# Alan adları workflow değişkenleriyle aynı: {{PLAKA}}, {{TC_KIMLIK}} ...
GEREKLI_ALANLAR: Dict[TalepTuru, List[str]] = {
    TalepTuru.YENILEME: ["AD_SOYAD", "PLAKA", "TC_KIMLIK", "DOGUM_TARIHI", "RUHSAT_BELGE"],
    # Alıcının TC + doğum tarihi; plaka ve belge seri satıcının ruhsatından (doğrulanacak).
    TalepTuru.YENI_ALIM: ["AD_SOYAD", "PLAKA", "RUHSAT_BELGE", "TC_KIMLIK", "DOGUM_TARIHI"],
    # Şasi/motor no gerekip gerekmediği doğrulanacak.
    TalepTuru.SIFIR_ARAC: ["AD_SOYAD", "IL_KODU", "TC_KIMLIK", "DOGUM_TARIHI"],
}

_SORULAR: Dict[TalepTuru, Dict[str, str]] = {
    TalepTuru.YENILEME: {
        "AD_SOYAD": "Araç sahibinin adı soyadı nedir?",
        "PLAKA": "Aracınızın plakası nedir?",
        "TC_KIMLIK": "Ruhsat sahibinin T.C. kimlik numarasını yazar mısınız?",
        "DOGUM_TARIHI": "Ruhsat sahibinin doğum tarihi nedir? (örnek: 08.08.1987)",
        "RUHSAT_BELGE": "Ruhsatın ön yüzündeki belge seri numarasını yazar mısınız? (örnek: AB 123456)",
    },
    TalepTuru.YENI_ALIM: {
        "AD_SOYAD": "Aracı satın alan kişinin adı soyadı nedir?",
        "PLAKA": "Satın aldığınız aracın plakası nedir?",
        "RUHSAT_BELGE": "Satıcının ruhsatındaki belge seri numarasını yazar mısınız? (örnek: AB 123456)",
        "TC_KIMLIK": "Aracı satın alan kişinin T.C. kimlik numarasını yazar mısınız?",
        "DOGUM_TARIHI": "Aracı satın alan kişinin doğum tarihi nedir? (örnek: 08.08.1987)",
    },
    TalepTuru.SIFIR_ARAC: {
        "AD_SOYAD": "Aracın adına kaydedileceği kişinin adı soyadı nedir?",
        "IL_KODU": "Araç hangi ilde tescil edilecek?",
        "TC_KIMLIK": "Aracın adına kaydedileceği kişinin T.C. kimlik numarasını yazar mısınız?",
        "DOGUM_TARIHI": "Aracın adına kaydedileceği kişinin doğum tarihi nedir? (örnek: 08.08.1987)",
    },
}


def eksik_alanlar(turu: Optional[TalepTuru], bilgiler: Dict[str, object]) -> List[str]:
    """Talep türü bilinmiyorsa önce o sorulur."""
    if turu is None:
        return ["TALEP_TURU"]
    return [a for a in GEREKLI_ALANLAR[turu] if bilgiler.get(a) in (None, "")]


def sonraki_soru(turu: Optional[TalepTuru], bilgiler: Dict[str, object]) -> Optional[str]:
    eksik = eksik_alanlar(turu, bilgiler)
    if not eksik:
        return None
    if eksik[0] == "TALEP_TURU":
        return TALEP_TURU_SORUSU
    return _SORULAR[turu][eksik[0]]


def talep_turu_degisti(eski: Optional[TalepTuru], yeni: TalepTuru, bilgiler: Dict[str, object]) -> Dict[str, object]:
    """Tür değişirse kişi ve belge bilgileri farklı kişiye ait olabilir → geçersiz sayılır."""
    if eski is None or eski is yeni:
        return dict(bilgiler)
    korunan = {"TELEFON"}
    return {k: v for k, v in bilgiler.items() if k in korunan}
