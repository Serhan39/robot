"""Sigorta talebi durum makinesi.

İzin verilmeyen geçiş `GecersizGecis` fırlatır; her geçiş geçmişe (işlem geçmişi) yazılır.
Kalıcılık (veritabanı) sonraki fazda eklenecek; bu sınıf saf iş kuralıdır.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional


class Durum(str, Enum):
    NEW = "NEW"
    COLLECTING_INFORMATION = "COLLECTING_INFORMATION"
    INFORMATION_COMPLETE = "INFORMATION_COMPLETE"
    QUOTING = "QUOTING"
    QUOTE_READY = "QUOTE_READY"
    QUOTE_SENT = "QUOTE_SENT"
    WAITING_CUSTOMER = "WAITING_CUSTOMER"
    CUSTOMER_APPROVED = "CUSTOMER_APPROVED"
    URGENT_NOTIFICATION = "URGENT_NOTIFICATION"
    MANUAL_PROCESSING = "MANUAL_PROCESSING"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"  # müşteri reddetti / zaman aşımı
    CANCELLED = "CANCELLED"  # acente iptal etti
    ERROR = "ERROR"
    MANUAL_INTERVENTION = "MANUAL_INTERVENTION"


D = Durum
SON_DURUMLAR = frozenset({D.COMPLETED, D.CLOSED, D.CANCELLED})

GECISLER = {
    D.NEW: {D.COLLECTING_INFORMATION, D.INFORMATION_COMPLETE},
    D.COLLECTING_INFORMATION: {D.INFORMATION_COMPLETE, D.CLOSED},
    D.INFORMATION_COMPLETE: {D.QUOTING, D.COLLECTING_INFORMATION},
    D.QUOTING: {D.QUOTE_READY},
    D.QUOTE_READY: {D.QUOTE_SENT},
    D.QUOTE_SENT: {D.WAITING_CUSTOMER},
    # Müşteri bilgi değiştirirse (ör. "aslında aracı yeni aldım") baştan bilgi toplanır.
    D.WAITING_CUSTOMER: {D.CUSTOMER_APPROVED, D.CLOSED, D.COLLECTING_INFORMATION},
    D.CUSTOMER_APPROVED: {D.URGENT_NOTIFICATION},
    D.URGENT_NOTIFICATION: {D.MANUAL_PROCESSING},
    D.MANUAL_PROCESSING: {D.COMPLETED},
    D.ERROR: {D.MANUAL_INTERVENTION},
    D.MANUAL_INTERVENTION: set(),  # yalnızca devam_ettir() veya iptal_et()
}


class GecersizGecis(Exception):
    pass


@dataclass(frozen=True)
class Olay:
    zaman: datetime
    onceki: Durum
    sonraki: Durum
    neden: str


@dataclass
class TalepDurumu:
    durum: Durum = D.NEW
    gecmis: List[Olay] = field(default_factory=list)
    _hata_oncesi: Optional[Durum] = None

    def _kaydet(self, yeni: Durum, neden: str) -> None:
        self.gecmis.append(Olay(datetime.now(timezone.utc), self.durum, yeni, neden))
        self.durum = yeni

    def gecis(self, yeni: Durum, neden: str = "") -> None:
        if self.durum in SON_DURUMLAR:
            raise GecersizGecis(f"{self.durum.value} son durumdur; değiştirilemez")
        if yeni is D.ERROR:
            return self.hata(neden)
        if yeni is D.CANCELLED:
            return self.iptal_et(neden)
        if yeni not in GECISLER[self.durum]:
            raise GecersizGecis(f"{self.durum.value} → {yeni.value} geçişine izin yok")
        self._kaydet(yeni, neden)

    def hata(self, neden: str) -> None:
        """Herhangi bir durumdan ERROR → MANUAL_INTERVENTION. Sistem durmaz, talep bekler."""
        if self.durum in SON_DURUMLAR:
            raise GecersizGecis(f"{self.durum.value} son durumdur; değiştirilemez")
        if self.durum not in (D.ERROR, D.MANUAL_INTERVENTION):
            self._hata_oncesi = self.durum
        self._kaydet(D.ERROR, neden)
        self._kaydet(D.MANUAL_INTERVENTION, "manuel müdahale bekleniyor")

    def devam_ettir(self, neden: str = "Robotu Devam Ettir") -> None:
        if self.durum is not D.MANUAL_INTERVENTION or self._hata_oncesi is None:
            raise GecersizGecis("yalnızca MANUAL_INTERVENTION durumundan devam ettirilebilir")
        onceki, self._hata_oncesi = self._hata_oncesi, None
        self._kaydet(onceki, neden)

    def iptal_et(self, neden: str = "İşlemi İptal Et") -> None:
        if self.durum in SON_DURUMLAR:
            raise GecersizGecis(f"{self.durum.value} son durumdur; değiştirilemez")
        self._kaydet(D.CANCELLED, neden)
