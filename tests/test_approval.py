import pytest

from app.nlu.approval import Karar, OnaySonucu, birlestir, kural_ile_siniflandir

ONAY = [
    "onaylıyorum", "ONAYLIYORUM", "onayliyorum", "Onay", "tamam", "Tamamdır", "olur",
    "yapalım", "devam edelim", "poliçeyi kesebilirsiniz", "evet", "kabul ediyorum",
    "Tamam yapalım", "👍", "onaylıyorum.",
]
BELIRSIZ = [
    "fiyat iyi mi?", "bir düşüneyim", "eşime sorayım", "yarın dönüş yaparım",
    "tamam ama biraz pahalı", "olur mu?", "tamam, bir düşüneyim", "onaylıyor musunuz",
    "merhaba", "", "kesin değil", "belki yaparız", "tamam akşam haber veririm",
    "onaylıyorum ama önce eşimle konuşayım", "indirim olur mu", "tamam değil",
]
RET = ["istemiyorum", "vazgeçtim", "gerek yok teşekkürler", "hayır", "onaylamıyorum", "iptal"]


@pytest.mark.parametrize("mesaj", ONAY)
def test_onay(mesaj):
    assert kural_ile_siniflandir(mesaj).karar is Karar.ONAYLANDI, mesaj


@pytest.mark.parametrize("mesaj", BELIRSIZ)
def test_belirsiz(mesaj):
    assert kural_ile_siniflandir(mesaj).karar is Karar.BELIRSIZ, mesaj


@pytest.mark.parametrize("mesaj", RET)
def test_ret(mesaj):
    assert kural_ile_siniflandir(mesaj).karar is Karar.REDDEDILDI, mesaj


def test_onay_ve_ret_birlikte_belirsiz():
    assert kural_ile_siniflandir("hayır hayır tamam onaylıyorum").karar is Karar.BELIRSIZ


def _s(k):
    return OnaySonucu(k, "test")


def test_birlestir_iki_katman_onay_gerekir():
    assert birlestir(_s(Karar.ONAYLANDI), _s(Karar.ONAYLANDI)).karar is Karar.ONAYLANDI
    assert birlestir(_s(Karar.ONAYLANDI), _s(Karar.BELIRSIZ)).karar is Karar.BELIRSIZ
    assert birlestir(_s(Karar.BELIRSIZ), _s(Karar.ONAYLANDI)).karar is Karar.BELIRSIZ
    assert birlestir(_s(Karar.ONAYLANDI), _s(Karar.REDDEDILDI)).karar is Karar.BELIRSIZ


def test_birlestir_llm_yoksa_onay_yok():
    assert birlestir(_s(Karar.ONAYLANDI), None).karar is Karar.BELIRSIZ
    assert birlestir(_s(Karar.REDDEDILDI), None).karar is Karar.REDDEDILDI


def test_birlestir_ret():
    assert birlestir(_s(Karar.BELIRSIZ), _s(Karar.REDDEDILDI)).karar is Karar.REDDEDILDI
