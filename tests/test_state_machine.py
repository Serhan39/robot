import pytest

from app.conversation.state_machine import Durum as D, GecersizGecis, TalepDurumu

MUTLU_YOL = [
    D.COLLECTING_INFORMATION, D.INFORMATION_COMPLETE, D.QUOTING, D.QUOTE_READY, D.QUOTE_SENT,
    D.WAITING_CUSTOMER, D.CUSTOMER_APPROVED, D.URGENT_NOTIFICATION, D.MANUAL_PROCESSING, D.COMPLETED,
]


def test_mutlu_yol_ve_gecmis():
    t = TalepDurumu()
    for d in MUTLU_YOL:
        t.gecis(d)
    assert t.durum is D.COMPLETED
    assert [o.sonraki for o in t.gecmis] == MUTLU_YOL


def test_onay_atlanamaz():
    t = TalepDurumu()
    for d in MUTLU_YOL[:6]:
        t.gecis(d)
    with pytest.raises(GecersizGecis):
        t.gecis(D.URGENT_NOTIFICATION)  # müşteri onayı olmadan acil bildirim yok


def test_teklif_bilgi_tamamlanmadan_baslamaz():
    t = TalepDurumu()
    t.gecis(D.COLLECTING_INFORMATION)
    with pytest.raises(GecersizGecis):
        t.gecis(D.QUOTING)


def test_hata_manuel_mudahale_ve_devam():
    t = TalepDurumu()
    t.gecis(D.INFORMATION_COMPLETE)
    t.gecis(D.QUOTING)
    t.hata("Araç sorgusu cevap vermedi")
    assert t.durum is D.MANUAL_INTERVENTION
    assert [o.sonraki for o in t.gecmis[-2:]] == [D.ERROR, D.MANUAL_INTERVENTION]
    t.devam_ettir()
    assert t.durum is D.QUOTING


def test_gecis_ile_error_da_manuel_mudahaleye_gider():
    t = TalepDurumu()
    t.gecis(D.ERROR, "beklenmeyen ekran")
    assert t.durum is D.MANUAL_INTERVENTION


def test_iptal_ve_son_durum_degismez():
    t = TalepDurumu()
    t.gecis(D.COLLECTING_INFORMATION)
    t.iptal_et()
    assert t.durum is D.CANCELLED
    for islem in (lambda: t.gecis(D.INFORMATION_COMPLETE), lambda: t.hata("x"), t.iptal_et):
        with pytest.raises(GecersizGecis):
            islem()


def test_devam_yalnizca_manuel_mudahaleden():
    with pytest.raises(GecersizGecis):
        TalepDurumu().devam_ettir()


def test_musteri_bilgi_degistirirse_basa_doner():
    t = TalepDurumu()
    for d in MUTLU_YOL[:6]:
        t.gecis(d)
    t.gecis(D.COLLECTING_INFORMATION, "müşteri: aslında aracı yeni aldım")
    assert t.durum is D.COLLECTING_INFORMATION
