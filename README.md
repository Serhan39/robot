# robot

WhatsApp → Open Hızlı Teklif (RPA) → Müşteri Onayı → Acil Bildirim otomasyon sistemi.

**Durum:** Faz 1–2 (analiz). Kod yazımı, Open Hızlı Teklif ekranları ve aşağıdaki
sorular yanıtlandıktan sonra başlayacak.

- Analiz ve mimari: [docs/01_analiz_ve_mimari.md](docs/01_analiz_ve_mimari.md)
- Ekran analizi: [docs/02_ekran_analizi.md](docs/02_ekran_analizi.md)
- İş kuralları: [docs/03_is_kurallari.md](docs/03_is_kurallari.md)
- Windows ortam analizi betiği: `python tools/ortam_analizi.py`

Robot Open Hızlı Teklif'i sizin yerinize bir insan gibi kullanır: ekranı görür, klavye ve
fareyle çalışır; programın içine girilmez.

Temel kural: sistem **hiçbir zaman** poliçe kesmez/satın almaz; müşteri onayından sonra
insana acil bildirim gönderir.

## Geliştirilen modüller (ekranlardan bağımsız)

| Modül | İçerik |
|---|---|
| `app/nlu/validators.py` | TC kimlik (kontrol hanesi), VKN, plaka (+ `YK` sıfır araç), ruhsat belge seri, doğum tarihi, model yılı, telefon, maskeleme |
| `app/nlu/approval.py` | Müşteri onayı kural katmanı + LLM ile birleştirme (ikisi de onay demeden onay yok) |
| `app/conversation/state_machine.py` | Talep durum makinesi (NEW → … → COMPLETED, hata → MANUEL MÜDAHALE → devam/iptal) |
| `app/insurance/trafik.py` | Trafik: yenileme / yeni alım / sıfır araç için gerekli bilgiler ve sorular |

Testleri çalıştırmak:

```
pip install -r requirements-dev.txt
python -m pytest
```
