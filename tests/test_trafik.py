from app.insurance.trafik import (
    TALEP_TURU_SORUSU, TalepTuru, eksik_alanlar, sonraki_soru, talep_turu_degisti,
)


def test_once_talep_turu_sorulur():
    assert eksik_alanlar(None, {"PLAKA": "34ABC123"}) == ["TALEP_TURU"]
    assert sonraki_soru(None, {}) == TALEP_TURU_SORUSU


def test_yenileme_eksikler_sirayla():
    bilgi = {"AD_SOYAD": "Ahmet Yılmaz", "PLAKA": "34ABC123"}
    assert eksik_alanlar(TalepTuru.YENILEME, bilgi) == ["TC_KIMLIK", "DOGUM_TARIHI", "RUHSAT_BELGE"]
    assert "Ruhsat sahibinin" in sonraki_soru(TalepTuru.YENILEME, bilgi)


def test_yeni_alimda_alici_sorulur():
    bilgi = {"AD_SOYAD": "x", "PLAKA": "34ABC123", "RUHSAT_BELGE": {"seri": "AB", "no": "123456"}}
    assert "satın alan" in sonraki_soru(TalepTuru.YENI_ALIM, bilgi)


def test_sifir_aracta_plaka_istenmez():
    assert "PLAKA" not in eksik_alanlar(TalepTuru.SIFIR_ARAC, {})


def test_tamamlaninca_soru_yok():
    bilgi = {"AD_SOYAD": "x", "PLAKA": "y", "TC_KIMLIK": "z", "DOGUM_TARIHI": "d", "RUHSAT_BELGE": "b"}
    assert sonraki_soru(TalepTuru.YENILEME, bilgi) is None


def test_tur_degisirse_kisi_bilgileri_silinir():
    bilgi = {"TELEFON": "905321234567", "TC_KIMLIK": "10000000146", "PLAKA": "34ABC123"}
    yeni = talep_turu_degisti(TalepTuru.YENILEME, TalepTuru.YENI_ALIM, bilgi)
    assert yeni == {"TELEFON": "905321234567"}
    assert talep_turu_degisti(None, TalepTuru.YENILEME, bilgi) == bilgi
