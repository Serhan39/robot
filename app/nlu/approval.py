"""Müşteri onayı sınıflandırma – kural katmanı.

Muhafazakâr tasarım: yalnızca açık bir onay ifadesi varsa VE mesajda soru, tereddüt,
erteleme, olumsuzluk veya "ama" gibi karşıtlık yoksa ONAYLANDI döner. Şüphede BELIRSIZ.

Nihai karar `birlestir()` ile verilir: kural katmanı ve LLM katmanı **ikisi de** ONAYLANDI
demedikçe onay sayılmaz. Onay olsa bile sistem poliçe kesmez; yalnızca acenteye acil
bildirim gider.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from app.nlu.validators import ascii_katla, tr_lower


class Karar(str, Enum):
    ONAYLANDI = "ONAYLANDI"
    REDDEDILDI = "REDDEDILDI"
    BELIRSIZ = "BELIRSIZ"


@dataclass(frozen=True)
class OnaySonucu:
    karar: Karar
    gerekce: str


NETLESTIRME_MESAJI = "İşlemi başlatmamız için onayınızı netleştirir misiniz?"

# Desenler ASCII'ye katlanmış, küçük harf metin üzerinde çalışır ("onaylıyorum" → "onayliyorum").
_RET = [
    r"\bonaylami", r"\bonaylamay", r"\bistemiyor", r"\bistemem\b", r"\bvazgec",
    r"\bgerek yok\b", r"\bhayir\b", r"\byapmay", r"\biptal\b", r"\bolmaz\b",
    r"\bkabul etmiyor", r"\bdevam etmeyelim\b", r"\bkesmeyin\b", r"\bbaska yerden\b",
]
_TEREDDUT = [
    r"\bdusun", r"\bsoray", r"\bdanisay", r"\bkonusay", r"\byarin\b", r"\bsonra\b",
    r"\bbakaca", r"\bbakariz\b", r"\bbakay", r"\bhaber veri", r"\bdonus yap", r"\bdonerim\b",
    r"\bemin degil", r"\bbilmiyorum\b", r"\bdegil\b", r"\bama\b", r"\bfakat\b", r"\bancak\b",
    r"\byalniz\b", r"\bbelki\b", r"\bsimdilik\b", r"\bbekle", r"\bpahali", r"\bindirim",
]
_SORU = [r"\?", r"\b(mi|mu|misin|misiniz|miyim|miyiz|midir|mudur|musun|musunuz)\b", r"\bne zaman\b", r"\bnasil\b", r"\bneden\b"]
_ONAY = [
    r"\bonay(liyorum|liyoruz|ladim|ladik|larim|layin)?\b", r"\btamam(dir)?\b", r"\bolur\b",
    r"\byapalim\b", r"\byapin\b", r"\byapabilirsiniz\b", r"\bdevam(\s+edelim|\s+edin|\s+ediyorum)?\b",
    r"\bkesebilirsiniz\b", r"\bkesin\b", r"\bpoliceyi kes", r"\bevet\b", r"\bkabul( ediyorum| ediyoruz)?\b",
    r"\buygun(dur)?\b", r"\banlastik\b", r"\bhalledelim\b", "\U0001F44D",
]


def _normalize(metin: str) -> str:
    return re.sub(r"\s+", " ", ascii_katla(tr_lower(metin or ""))).strip()


def _bul(desenler, metin) -> Optional[str]:
    for d in desenler:
        m = re.search(d, metin)
        if m:
            return m.group(0)
    return None


def kural_ile_siniflandir(metin: str) -> OnaySonucu:
    t = _normalize(metin)
    if not t:
        return OnaySonucu(Karar.BELIRSIZ, "boş mesaj")
    onay = _bul(_ONAY, t)
    ret = _bul(_RET, t)
    if ret and not onay:
        return OnaySonucu(Karar.REDDEDILDI, f"ret ifadesi: {ret!r}")
    if ret and onay:
        return OnaySonucu(Karar.BELIRSIZ, f"onay ({onay!r}) ve ret ({ret!r}) birlikte")
    if not onay:
        return OnaySonucu(Karar.BELIRSIZ, "açık onay ifadesi yok")
    engel = _bul(_SORU, t) or _bul(_TEREDDUT, t)
    if engel:
        return OnaySonucu(Karar.BELIRSIZ, f"onay ({onay!r}) var ama soru/tereddüt ({engel!r}) de var")
    if len(t.split()) > 12:
        return OnaySonucu(Karar.BELIRSIZ, "uzun mesaj; kural katmanı tek başına karar vermez")
    return OnaySonucu(Karar.ONAYLANDI, f"açık onay: {onay!r}")


def birlestir(kural: OnaySonucu, llm: Optional[OnaySonucu]) -> OnaySonucu:
    """İki katmanın ortak kararı. LLM sonucu yoksa (servis kapalı vb.) onay verilmez."""
    if llm is None:
        if kural.karar is Karar.REDDEDILDI:
            return kural
        return OnaySonucu(Karar.BELIRSIZ, "LLM katmanı sonucu yok; tek katmanla onay verilmez")
    if kural.karar is Karar.ONAYLANDI and llm.karar is Karar.ONAYLANDI:
        return OnaySonucu(Karar.ONAYLANDI, "kural ve LLM katmanı onay dedi")
    if Karar.REDDEDILDI in (kural.karar, llm.karar) and Karar.ONAYLANDI not in (kural.karar, llm.karar):
        return OnaySonucu(Karar.REDDEDILDI, f"kural: {kural.gerekce}; llm: {llm.gerekce}")
    return OnaySonucu(Karar.BELIRSIZ, f"kural: {kural.karar.value}; llm: {llm.karar.value}")
