from datetime import date

import pytest

from app.nlu import validators as v

BUGUN = date(2026, 10, 26)


def tc_uret(ilk9: str) -> str:
    d = [int(c) for c in ilk9]
    d10 = ((d[0] + d[2] + d[4] + d[6] + d[8]) * 7 - (d[1] + d[3] + d[5] + d[7])) % 10
    d11 = (sum(d) + d10) % 10
    return f"{ilk9}{d10}{d11}"


class TestTC:
    def test_bilinen_gecerli(self):
        assert v.tc_kimlik_dogrula("10000000146").deger == "10000000146"

    def test_bosluklu_girdi(self):
        tc = tc_uret("123456789")
        assert v.tc_kimlik_dogrula(" ".join([tc[:3], tc[3:6], tc[6:]])).gecerli

    @pytest.mark.parametrize("girdi", ["", "1234567890", "123456789012", "abcdefghijk", "01234567890"])
    def test_bicim_hatali(self, girdi):
        assert not v.tc_kimlik_dogrula(girdi).gecerli

    def test_kontrol_hanesi_hatali(self):
        tc = tc_uret("123456789")
        bozuk = tc[:10] + str((int(tc[10]) + 1) % 10)
        sonuc = v.tc_kimlik_dogrula(bozuk)
        assert not sonuc.gecerli and "geçerli görünmüyor" in sonuc.hata


class TestVKN:
    def test_kendi_kendine_tutarli(self):
        # Gerçek VKN ile doğrulanana kadar: 9 hane için tek bir geçerli kontrol hanesi olmalı.
        gecerli = [d for d in "0123456789" if v.vergi_no_dogrula("123456789" + d).gecerli]
        assert len(gecerli) == 1

    def test_bicim(self):
        assert not v.vergi_no_dogrula("12345").gecerli


class TestPlaka:
    @pytest.mark.parametrize("girdi,beklenen,gorunum", [
        ("34 ABC 123", "34ABC123", "34 ABC 123"),
        ("07mys57", "07MYS57", "07 MYS 57"),
        ("06 a 1234", "06A1234", "06 A 1234"),
        ("35-ab-1234", "35AB1234", "35 AB 1234"),
        ("01 i 12345", "01İ12345", None),
    ])
    def test_gecerli(self, girdi, beklenen, gorunum):
        s = v.plaka_dogrula(girdi)
        if beklenen == "01İ12345":  # Türkçe harf plakada kullanılmaz
            assert not s.gecerli
            return
        assert s.gecerli and s.deger == beklenen and s.ek["gorunum"] == gorunum
        assert s.ek["yeni_kayit"] is False

    @pytest.mark.parametrize("girdi", ["", "00ABC123", "82ABC123", "34ABCD12", "34A12", "34ABC1234", "ABC123"])
    def test_gecersiz(self, girdi):
        assert not v.plaka_dogrula(girdi).gecerli

    def test_yeni_kayit(self):
        s = v.plaka_dogrula("34 yk")
        assert s.gecerli and s.ek["yeni_kayit"] and s.ek["il_kodu"] == 34
        assert v.yeni_kayit_plakasi(7) == "07YK"
        with pytest.raises(ValueError):
            v.yeni_kayit_plakasi(82)


class TestBelgeSeri:
    @pytest.mark.parametrize("girdi", ["HS 321022", "hs321022", "AB-123456"])
    def test_gecerli(self, girdi):
        s = v.belge_seri_dogrula(girdi)
        assert s.gecerli and len(s.deger["seri"]) == 2 and len(s.deger["no"]) == 6

    def test_ayrisma(self):
        assert v.belge_seri_dogrula("hs 321022").deger == {"seri": "HS", "no": "321022"}

    @pytest.mark.parametrize("girdi", ["", "H 321022", "HS 32102", "HS3210221", "123456"])
    def test_gecersiz(self, girdi):
        assert not v.belge_seri_dogrula(girdi).gecerli


class TestTarih:
    @pytest.mark.parametrize("girdi", ["08.08.1987", "08/08/1987", "08-08-1987", "1987-08-08"])
    def test_bicimler(self, girdi):
        assert v.dogum_tarihi_dogrula(girdi, BUGUN).deger == date(1987, 8, 8)

    def test_bugun_varsayilani_reddedilir(self):
        # Open Hızlı Teklif alanı bugünün tarihiyle gelir; bu asla geçerli doğum tarihi değildir.
        assert not v.dogum_tarihi_dogrula("26.10.2026", BUGUN).gecerli

    def test_18_yas_siniri(self):
        assert v.dogum_tarihi_dogrula("26.10.2008", BUGUN).gecerli
        assert not v.dogum_tarihi_dogrula("27.10.2008", BUGUN).gecerli

    @pytest.mark.parametrize("girdi", ["", "31.02.1990", "dün", "01.01.1900"])
    def test_gecersiz(self, girdi):
        assert not v.dogum_tarihi_dogrula(girdi, BUGUN).gecerli

    def test_model_yili(self):
        assert v.model_yili_dogrula("2020", BUGUN).deger == 2020
        assert v.model_yili_dogrula(2027, BUGUN).gecerli
        assert not v.model_yili_dogrula(2028, BUGUN).gecerli
        assert not v.model_yili_dogrula("yirmi", BUGUN).gecerli


class TestTelefon:
    @pytest.mark.parametrize("girdi", ["0532 123 45 67", "+90 532 123 45 67", "5321234567", "(0532) 123-45-67"])
    def test_normalize(self, girdi):
        assert v.telefon_normalize(girdi).deger == "905321234567"

    @pytest.mark.parametrize("girdi", ["0212 123 45 67", "123", ""])
    def test_gecersiz(self, girdi):
        assert not v.telefon_normalize(girdi).gecerli


def test_maskele():
    assert v.maskele("10000000146") == "*******0146"
    assert v.maskele("12") == "**"


def test_turkce_buyuk_harf():
    assert v.tr_upper("istanbul ılgaz") == "İSTANBUL ILGAZ"
