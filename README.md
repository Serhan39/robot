# robot

WhatsApp → Open Hızlı Teklif (RPA) → Müşteri Onayı → Acil Bildirim otomasyon sistemi.

**Durum:** Faz 1–2 (analiz). Kod yazımı, Open Hızlı Teklif ekranları ve aşağıdaki
sorular yanıtlandıktan sonra başlayacak.

- Analiz ve mimari: [docs/01_analiz_ve_mimari.md](docs/01_analiz_ve_mimari.md)
- Windows ortam analizi betiği: `python tools/ortam_analizi.py`

Robot Open Hızlı Teklif'i sizin yerinize bir insan gibi kullanır: ekranı görür, klavye ve
fareyle çalışır; programın içine girilmez.

Temel kural: sistem **hiçbir zaman** poliçe kesmez/satın almaz; müşteri onayından sonra
insana acil bildirim gönderir.
