# FAZ 1–2 Analiz Raporu ve Teknik Mimari Önerisi

> Durum: **Taslak – kullanıcıdan bilgi bekleniyor.**
> **Temel ilke (kullanıcı kararı):** Robot, Open Hızlı Teklif'i **sizin yerinize, bir insan gibi**
> kullanır: ekranı görür (ekran görüntüsü + OCR + görüntü tanıma), klavye ve fareyle çalışır.
> Programın içine girilmez: program dosyalarına, veritabanına, ağ trafiğine, iç yapısına veya
> erişilebilirlik ağacına (UI Automation) dokunulmaz; programda hiçbir değişiklik yapılmaz.
>
> Bu belge kod yazmadan önce hazırlanan analiz ve mimari önerisidir. Open Hızlı Teklif
> ekranları görülmeden otomasyon kodu kesinleştirilmeyecektir (bkz. Bölüm 15 – Sorular).

---

## 1. Faz 1 – Ortam Analizi: Neyi analiz edebildim, neyi edemedim?

Bu çalışma bulut üzerindeki izole bir **Linux** konteynerinde yapılıyor. **Sizin Windows
bilgisayarınıza, ekranınıza veya Open Hızlı Teklif kurulumunuza erişimim yok.** Bu yüzden
Windows sürümü, ekran çözünürlüğü, kurulu programlar ve Open Hızlı Teklif'in UI yapısı hakkında
varsayım yapmıyorum.

| Bilgi | Durum |
|---|---|
| Geliştirme ortamı (bu konteyner) | Linux x86_64, Python 3.11.15, Node.js 22.22.2 |
| Sizin Windows sürümünüz | **Bilinmiyor** → `tools/ortam_analizi.py` ile toplanacak |
| Sizin Python / Node sürümünüz | **Bilinmiyor** → aynı betik |
| Ekran çözünürlüğü / DPI ölçekleme | **Bilinmiyor** → aynı betik |
| Tesseract / OCR kurulu mu | **Bilinmiyor** → aynı betik |
| Open Hızlı Teklif ekranları ve kullanım adımları | **Bilinmiyor** → ekran görüntüleri + ekran kaydı (sizden) |
| `robot` deposu | Boş (ilk commit bu rapor) |

### Robot bilgisayarı – ölçüm sonucu (27.09.2026, `ortam_analizi.py`)

| Bilgi | Sonuç | Değerlendirme |
|---|---|---|
| Windows | **Windows 11** (10.0.26200), 64-bit | Uygun |
| Ekran | **1920×1080**, tek monitör, **%100 ölçek (96 DPI)** | OCR ve görüntü tanıma için ideal |
| Python | **3.13.15** (64-bit) | Uygun |
| Node.js | 24.12.0 | Gerekmiyor, sorun değil |
| Tesseract OCR | **Kurulu değil** | Kodlama aşamasında kurulacak (Türkçe paketiyle) |
| Python kütüphaneleri | Hiçbiri kurulu değil | Kodlama aşamasında `requirements.txt` ile kurulacak |
| Open Hızlı Teklif | **v3**, MSI ile kurulu: `C:\Program Files\OPEN YAZILIM\Open Hizli Teklif\Open Hizli Teklif.exe` | Robot programı bu yoldan veya Başlat menüsü kısayolundan açacak |
| Open Acentem | **V3** kurulu (`C:\Program Files (x86)\OPEN YAZILIM\Open Acentem`) | Şimdilik kapsam dışı; ileride poliçe takibi için kullanılabilir |
| Doğanium Hızlı Teklif | Kurulu (`C:\Program Files (x86)\Doğanium Hızlı Teklif`) | **Kapsam dışı** (kullanıcı: robot yalnızca Open Hızlı Teklif kullanacak) |
| Ölçüm anında Open Hızlı Teklif | Çalışmıyordu | – |
| Bilgisayar türü | Günlük kullanım bilgisayarı gibi görünüyor (FreeCAD, FileZilla vb.) | Robot çalışırken fare/klavye kullanılamaz → ayrı PC/VM kararı gerekli |
| **Karar (kullanıcı)** | Üretimde robot **ayrı bir bilgisayar veya sanal makinede** çalışacak; geliştirme ve deneme şimdilik bu bilgisayarda | Kurulum adımları taşınabilir tutulacak (tek `requirements.txt` + kurulum betiği) |

### Yapmanız gereken (5 dakika)

Open Hızlı Teklif'in **kurulu olduğu Windows bilgisayarda**:

```powershell
# 1) Python 3.11+ kurulu değilse: https://www.python.org/downloads/windows/
# 2) İsteğe bağlı ama çok faydalı:
# 2) Çalıştırın (ek kurulum gerekmez):
python tools\ortam_analizi.py
```

Oluşan `ortam_raporu_*.json` dosyasını bana gönderin. Betik yalnızca bilgisayar bilgilerini
(Windows/Python sürümü, ekran çözünürlüğü, DPI, kurulu kütüphaneler) toplar; Open Hızlı Teklif'e
dokunmaz, ekran görüntüsü almaz.

---

## 2. Faz 2 – Open Hızlı Teklif Ön Analizi (açık kaynaklardan)

Üreticinin sitesinden ve basından doğrulayabildiklerim:

| Bulgu | Kaynak | Otomasyona etkisi |
|---|---|---|
| Üretici: **Open Yazılım** (Düzce) | openyazilim.com | – |
| Kurulum: **Windows x64 MSI** ve **ClickOnce** | ürün sayfası | Program büyük olasılıkla bir **Windows masaüstü uygulaması** → robot aynı Windows oturumunda ekranı görüp klavye/fare kullanacak. |
| Branşlar: Trafik, Kasko, TSS, Konut, DASK, İMM | ürün sayfası | Workflow motoru ürün bazlı olmalı. |
| Çoklu şirketten otomatik teklif ("robot teknolojisi") | basın | Sonuç ekranı muhtemelen **birden çok şirketin fiyatını içeren bir tablo (grid)**. Tek satır değil, liste okunacak. |
| **Fiyatları dışa aktarma** | ürün sayfası | Sonuçları OCR yerine **dışa aktarılan dosyadan (Excel/PDF) okumak** en güvenilir yol olabilir. Doğrulanmalı. |
| **İki faktörlü doğrulama (2FA)** | ürün sayfası | Girişin tam otomatik yapılması mümkün/uygun olmayabilir. Oturum açık tutulmalı; 2FA istenirse robot **MANUEL MÜDAHALE**'ye geçip sizi uyarmalı. |
| Uygulama içinden **poliçeleştirme** mümkün | basın ("teklif alıp poliçeleştirebildiği") | **Kritik risk.** Robotun "Poliçeleştir / Satın Al / Onayla" gibi düğmelere basması motor seviyesinde **yasaklanmalı** (bkz. 8.3). |
| QR ile ruhsat okuma, Tramer entegrasyonu | ürün sayfası | Plaka + TC/VKN + belge seri no ile araç bilgisi otomatik gelebilir → müşteriden daha az bilgi istemek yeterli olabilir. Doğrulanmalı. |
| Mobil/tablet üzerinden kullanım | basın | Bir **web/mobil arayüzü** de olabilir. Varsa Playwright ile web otomasyonu masaüstünden daha sağlam olabilir → **size soruyorum** (Soru 2). |
| Resmi **API**: yok (sizin bilginiz) | – | API varmış gibi davranılmayacak. |

**Ekran görüntüleri ve kayıt ile kontrol edilecekler:**
- Alanlar arasında **Tab** ile sırayla gezilebiliyor mu? Sıra sabit mi? (İnsan gibi en sağlam yol)
- Klavye kısayolları var mı (ör. F-tuşları, Alt+harf, Enter ile "Teklif Al")?
- Açılır listeler klavyeyle (harf yazarak) seçilebiliyor mu?
- Sonuç tablosu ekranda okunaklı mı, kaydırma gerekiyor mu? Dışa aktarma menüsü nerede?
- Sigorta şirketlerinden sonuçlar asenkron mu geliyor (tek tek mi doluyor)? → "bekle" koşulu buna göre yazılacak.

---

## 3. Teknoloji Seçimi ve Gerekçeler

| Katman | Seçim | Neden | Elenen / ikincil |
|---|---|---|---|
| Ana dil | **Python 3.11+** | Ekran okuma (OpenCV, OCR), klavye/fare, FastAPI ve LLM SDK'larının hepsi aynı dilde; tek dil = kolay bakım. | Node.js yalnızca gerekirse (ör. panel build). |
| Ekranı görme | **mss** (hızlı ekran görüntüsü) + OCR + OpenCV | Robot sizin gördüğünüzü görür; programın içine girilmez. | UI Automation / program içi erişim: **kullanılmayacak** (kullanıcı kararı). |
| Web otomasyon (program web ise) | **Playwright** | Otomatik bekleme, sağlam seçiciler, iz (trace) kaydı. | Selenium: daha kırılgan, bekleme yönetimi zayıf. |
| OCR | **Tesseract (tur)** + ön işleme | Hafif, yerel çalışır (KVKK), Türkçe dil paketi var. UI yazıları için yeterli. | **PaddleOCR**: daha isabetli ama ağır; Tesseract yetersiz kalırsa eklenti olarak. EasyOCR: PlakaTanima'da kullanılıyor ama UI metninde Tesseract+ön işleme yeterli. |
| Görüntü tanıma | **OpenCV** çok ölçekli şablon eşleştirme | Düğme ikonlarını DPI/çözünürlük değişse de bulmak için. | – |
| Klavye/fare | **pynput** (eğitimde kayıt + oynatma) | Tıklama/tuşları kaydeder ve insan gibi tekrar eder; Türkçe karakterleri doğru yazar. | PyAutoGUI: Türkçe karakter ve DPI sorunları → ikincil. |
| API / panel backend | **FastAPI** | Webhook, panel API'si, tip güvenliği (pydantic). | – |
| Veritabanı | **SQLite (WAL) → PostgreSQL'e hazır**, SQLAlchemy + Alembic | Tek Windows PC için kurulum gerektirmez; ORM sayesinde Postgres'e geçiş tek ayar. | Doğrudan Postgres: ikinci makine/robot eklenince. |
| İş kuyruğu | **Veritabanı tabanlı kuyruk** (`jobs` tablosu, kiralama + heartbeat) | **Celery Windows'u resmi olarak desteklemiyor**; Redis Windows'ta resmi değil. Robot zaten tek-işlem (tek masaüstü) olduğu için DB kuyruğu yeterli, ek servis yok, kalıcı ve denetlenebilir. | Redis+RQ/Celery: robotlar ayrı Linux sunuculara taşınırsa. |
| LLM | **Claude API** – yapılandırılmış çıktı (tool use / JSON şema) | Türkçe anlama iyi; JSON şemaya zorlanabilir. Çıktı her zaman deterministik doğrulayıcılardan geçer. | Sağlayıcı soyutlama katmanı ile değiştirilebilir. |
| Yönetim paneli | **FastAPI + Jinja2 + HTMX** (sunucu tarafı) | Build zinciri yok, tek süreç, hızlı geliştirme; basit ama kullanışlı. | React/Next.js: panel çok büyürse. |
| Sır yönetimi | `.env` (geliştirme) + **Windows Credential Manager** (`keyring`) üretimde | Kod içinde hiçbir sır yok; Open Hızlı Teklif şifresi işletim sistemi kasasında. | – |
| Şifreleme | `cryptography` (Fernet) alan bazlı | TC kimlik, doğum tarihi vb. DB'de şifreli. | – |

---

## 4. WhatsApp Entegrasyon Seçenekleri

| Seçenek | Artı | Eksi | Öneri |
|---|---|---|---|
| **WhatsApp Business Platform – Cloud API (Meta, resmi)** | Resmi, ban riski yok, webhook ile anlık mesaj, şablon mesajlar. | Meta Business doğrulaması, internetten erişilebilir HTTPS webhook gerekir; **24 saat kuralı**: müşterinin son mesajından 24 saat sonra yalnızca onaylı şablonla yazılabilir; konuşma başı ücret olabilir. | **Önerilen.** |
| Cloud API + **Coexistence** (WhatsApp Business uygulaması ile aynı numara) | Mevcut numaranızı telefondaki WhatsApp Business uygulamasıyla birlikte kullanmaya devam edebilirsiniz. | Ülke/hesap uygunluğu ve bazı kısıtlar değişkendir; kurulumda doğrulanmalı. | Numaranızı değiştirmek istemiyorsanız ilk bakılacak yol. |
| BSP (360dialog, Twilio vb.) üzerinden Cloud API | Kurulum desteği, panel. | Aracı maliyeti. | Meta kurulumu zor gelirse. |
| Resmi olmayan (whatsapp-web.js, Baileys, WhatsApp Web RPA) | Hızlı, ücretsiz. | WhatsApp kullanım şartlarına aykırı, **numara kapatılma riski**, kırılgan. | **Üretimde önerilmez.** Yalnızca siz açıkça isterseniz, riskleri kabul edilerek. |

**Webhook erişimi:** Windows PC'yi internete açmak yerine **Cloudflare Tunnel** (ücretsiz, port açmadan HTTPS) veya küçük bir VPS'te sadece webhook alıcısı önerilir.

**Size gelecek ACİL bildirim kanalı:** Kendi numaranıza Cloud API ile mesaj atmak 24 saat
kuralına takılabilir (şablon gerekir). **Telegram Bot** ücretsiz, anlık ve güvenilir; ek olarak
Windows masaüstü bildirimi + e-posta yedek. Bildirim katmanı çok kanallı tasarlanacak (Soru 10).

---

## 5. Genel Mimari

```
                ┌───────────────────────── Windows PC (acente) ─────────────────────────┐
 Müşteri        │                                                                       │
 WhatsApp ──► Meta Cloud API ──► Cloudflare Tunnel ──► [FastAPI: webhook + panel]       │
                │                                          │                             │
                │                                   Mesaj Analizi (LLM + doğrulayıcılar) │
                │                                          │                             │
                │                                  Konuşma State Machine                 │
                │                                          │                             │
                │                                  jobs tablosu (DB kuyruğu)             │
                │                                          │  (tek tek)                  │
                │                              [Robot Worker süreci]                     │
                │                                          │                             │
                │                               Workflow Motoru ─► Sürücüler:            │
                │                                 Klavye ► OCR ► Görüntü ► Pencere-oransal  │
                │                                          │                             │
                │                                  Open Hızlı Teklif                     │
                │                                          │                             │
                │                               Sonuç okuma ► Eşleştirme kontrolü        │
                │                                          │                             │
 Müşteri ◄──── WhatsApp gönderici (TEST'te sadece log) ◄───┘                             │
 onayı ───────► Onay sınıflandırıcı ─► ACİL bildirim ─► Telegram / masaüstü / e-posta ──► SİZ
                └───────────────────────────────────────────────────────────────────────┘
```

Süreçler:
1. **api** – FastAPI (webhook, panel). Robotu asla doğrudan çağırmaz, sadece iş kuyruğa ekler.
2. **robot-worker** – kuyruktan tek iş alır, workflow'u çalıştırır. Masaüstü oturumu açık
   (kilitli olmayan) kullanıcı oturumunda çalışmalıdır; UI otomasyonu kilitli ekranda çalışmaz.
3. **notifier** – giden mesaj/bildirim kuyruğunu işler (yeniden deneme ile).

Her süreç Windows'ta Görev Zamanlayıcı veya NSSM ile servisleştirilebilir.

### Önerilen klasör yapısı

```
robot/
  app/
    api/            # FastAPI router'ları (webhook, panel, admin)
    panel/          # Jinja2 şablonları + HTMX
    channels/       # whatsapp_cloud.py, telegram.py, email.py, console.py (TEST)
    nlu/            # llm_extractor.py, validators.py (TC, plaka, yıl), approval_classifier.py
    conversation/   # state_machine.py, templates (mesaj şablonları DB'de)
    queue/          # db_queue.py (kiralama, heartbeat, retry)
    db/             # models.py, migrations/ (Alembic)
    security/       # crypto.py, secrets.py (keyring), redaction.py
    notifications/  # urgent.py
  automation/
    core/           # workflow_engine.py, actions.py, locators.py, verify.py, safety.py
    drivers/        # screen.py (görüntü al), input.py (klavye/fare), ocr_driver.py, vision_driver.py, coord_driver.py
    training/       # recorder.py, element_capture.py, workflow_builder.py
    open_hizli_teklif/
      login.py navigation.py customer.py vehicle.py quotation.py
      result.py screenshots.py recovery.py
      workflows/    # trafik_sigorta_teklifi.json, kasko_teklifi.json ...
      locators/     # hedef isim → çoklu locator tanımları (JSON)
  tools/ortam_analizi.py
  tests/
  config/settings.yaml   # retry sayıları, zaman aşımları, modlar (sır içermez)
  .env.example
```

---

## 6. Konuşma State Machine

```
NEW → COLLECTING_INFORMATION ⇄ (eksik bilgi sor/al)
    → INFORMATION_COMPLETE → QUOTING (kuyrukta/işleniyor)
    → QUOTE_READY → (eşleştirme kontrolü) → QUOTE_SENT → WAITING_CUSTOMER
    → CUSTOMER_APPROVED → URGENT_NOTIFICATION → MANUAL_PROCESSING (siz) → COMPLETED
Herhangi bir durum → ERROR → MANUAL_INTERVENTION → (Robotu Devam Ettir | İşlemi İptal Et)
WAITING_CUSTOMER → (belirsiz cevap) → WAITING_CUSTOMER + netleştirme sorusu
WAITING_CUSTOMER → (ret / zaman aşımı) → CLOSED
```

- Geçişler bir tablo ile tanımlanır; izin verilmeyen geçiş **istisna fırlatır** ve loglanır.
- Her geçiş `request_events` (işlem geçmişi) tablosuna yazılır.
- Bir müşterinin aynı anda birden fazla açık talebi olabilir; gelen mesaj hangi talebe ait
  belli değilse sistem **sorar**, tahmin etmez.

---

## 7. Yapay Zeka Katmanı ve Doğrulama

1. **Önce deterministik çıkarım:** Plaka, TC kimlik, telefon, model yılı regex ile yakalanır.
   TC kimlik **LLM'e gönderilmeden önce maskelenir** (`[TC_1]`) → veri minimizasyonu.
2. **LLM** (JSON şema zorunlu): sigorta türü, marka, model, motor, yakıt, kişi adı, niyet.
3. **Doğrulayıcılar** (LLM çıktısı asla doğrudan robota gitmez):
   - TC kimlik: 11 hane, ilk hane ≠ 0, **resmi sağlama algoritması** (10. ve 11. hane kontrolü).
   - Plaka: il kodu 01–81 + harf grubu + rakam grubu (TR formatları), boşluk normalizasyonu.
   - Model yılı: 1950 ≤ yıl ≤ bu yıl + 1.
   - Marka/model: Open Hızlı Teklif'in kendi listesiyle eşleştirme (robot okuyabilirse).
4. **Eksik bilgi → soru üretimi:** Ürün bazlı "zorunlu alan" listesi config'ten; soru metni
   şablondan (LLM yalnızca doğal dil cilası için, istenirse).
5. **Onay sınıflandırıcı** (iki katmanlı, muhafazakâr):
   - Kural katmanı: açık onay ifadeleri (onaylıyorum, tamam, olur, yapalım, devam edelim,
     poliçeyi kesebilirsiniz…) **ve** olumsuzluk/soru/erteleme işaretinin **olmaması**
     ("değil", "mı/mi", "?", "düşüneyim", "sorayım", "yarın", "sonra"…).
   - LLM katmanı: `APPROVED | REJECTED | AMBIGUOUS` + gerekçe.
   - **Sadece iki katman da APPROVED derse onay.** Aksi halde netleştirme sorusu gönderilir.
   - Onay her zaman **belirli bir teklif ID'sine** bağlanır; müşterinin birden fazla açık teklifi
     varsa hangisi olduğu sorulur.

---

## 8. Teklif Robotu ve Workflow Motoru

### 8.1 Locator (hedef bulma) stratejisi — öncelik sırası

Robot hedefi bir insanın bulacağı gibi bulur. Her hedef (ör. `plaka`, `teklif_al`) birden
fazla yolla tanımlanır; motor sırayla dener:

1. **Klavye:** kısayol veya Tab sırası (ör. "Plaka" alanına formu açtıktan sonra 3×Tab).
   Ekrandaki yerleşimden bağımsızdır, en sağlam yoldur. Her tuştan sonra ekranla doğrulanır.
2. **Ekrandaki yazı (OCR):** "Teklif Al" yazısını bul, üstüne tıkla; "Plaka" etiketini bul,
   yanındaki kutuya tıkla.
3. **Görüntü:** düğme/ikon görüntüsünü çok ölçekli ara (çözünürlük/DPI değişse de bulur).
4. **Pencereye göre oransal konum:** son çare; kullanılınca log'a uyarı düşer.

```json
{
  "teklif_al": [
    {"by": "keys", "keys": "F5"},
    {"by": "ocr", "text": "Teklif Al", "region": "window"},
    {"by": "image", "template": "teklif_al.png", "scales": [0.75, 1.0, 1.25, 1.5]},
    {"by": "coord", "rel_x": 0.82, "rel_y": 0.91}
  ]
}
```

Koordinatlar ekrana değil **pencereye göre oransal** saklanır ve yalnızca son çaredir; kullanıldığında log'a uyarı düşülür.

### 8.2 Aksiyonlar ve zorunlu doğrulama

| Aksiyon | Doğrulama |
|---|---|
| `open_application` | Süreç ve ana pencere belirdi mi; giriş ekranı mı ana ekran mı? |
| `click` | Beklenen etki oldu mu (yeni pencere/sekme, odak değişimi, öğe durumu) — adım tanımında `expect` alanı. |
| `input` | Alanın bulunduğu bölge OCR ile okunup yazılan değerle karşılaştırılır. |
| `select` | Seçili öğe geri okunur. |
| `wait_for` | Koşul + zaman aşımı; süre dolarsa hata, **asla sonsuz bekleme yok.** |
| `extract` | Şema doğrulaması (prim > 0, sayı formatı, tarih formatı, şirket adı boş değil). |
| `screenshot` | Maskeli ekran görüntüsü (bkz. 10). |

Doğrulama başarısızsa adım **geçilmez**: `retry` (config'teki sayıda) → `recovery` (pencereyi
öne getir, ESC ile diyalog kapat, ekranı yenile, gerekirse programı yeniden başlat) →
hâlâ olmuyorsa `MANUAL_INTERVENTION` + hata ekran görüntüsü.

### 8.3 Güvenlik kilidi (poliçe kesme yasağı)

`automation/core/safety.py` içinde **kod seviyesinde** bir yasak listesi olacak:
"Poliçeleştir", "Poliçe Kes", "Satın Al", "Ödeme", "Tahsilat", "Onayla ve Bitir" vb.
Her tıklamadan (ve Enter tuşundan) önce hedef bölge OCR ile okunur; metin bu listeye uyuyorsa işlem **reddedilir**, iş durur ve
size bildirim gider. Bu kontrol workflow dosyasıyla kapatılamaz.

### 8.4 Workflow formatı (örnek)

```json
{
  "workflow": "trafik_sigorta_teklifi",
  "version": 1,
  "application": "open_hizli_teklif",
  "required_variables": ["PLAKA", "TC_KIMLIK", "RUHSAT_SERI_NO"],
  "steps": [
    {"id": "s01", "action": "open_application", "target": "Open Hizli Teklif"},
    {"id": "s02", "action": "click", "target": "yeni_teklif", "expect": {"visible": "teklif_formu"}},
    {"id": "s03", "action": "select", "target": "brans", "value": "Trafik"},
    {"id": "s04", "action": "input", "target": "plaka", "value": "{{PLAKA}}", "verify": "readback"},
    {"id": "s05", "action": "input", "target": "tc_kimlik", "value": "{{TC_KIMLIK}}", "sensitive": true},
    {"id": "s06", "action": "click", "target": "teklif_al"},
    {"id": "s07", "action": "wait_for", "target": "teklif_sonucu", "timeout_s": 180},
    {"id": "s08", "action": "extract", "target": "teklif_sonucu", "schema": "quote_results"},
    {"id": "s09", "action": "screenshot", "name": "quote_result", "mask": ["tc_kimlik"]}
  ]
}
```

Farklı ürünler (Kasko, DASK, Konut, TSS…) = farklı workflow JSON'ları; motor aynı.
Farklı program = yeni `automation/<program_adi>/` paketi + locator dosyası.

### 8.5 Teklif sonucu okuma — öncelik

1. **Programın dışa aktarma menüsü** (bir insanın yapacağı gibi menüden "Dışa Aktar"a tıklayıp
   Excel/PDF kaydetmek) → dosya okunur → en güvenilir. Programın içine girilmez, sadece
   programın zaten sunduğu çıktı kullanılır.
2. **Ekrandaki tablonun OCR ile okunması** (bölge tespiti, ön işleme, sütun hizalama, gerekirse
   kaydırarak) → doğrulayıcılarla.

Çıktı (her şirket için bir kayıt):

```json
{"company": "ABC Sigorta", "premium": 8750.00, "currency": "TRY",
 "quotation_number": "12345678", "valid_until": "2026-09-27", "source": "export|ocr",
 "confidence": 0.98}
```

OCR kaynaklı ve düşük güvenli sonuçlar müşteriye **otomatik gönderilmez**; panelde onayınıza düşer (ayarlanabilir).

---

## 9. Robot Eğitim Modu (Training Mode)

**Kayıt sırasında her olay için:**
- zaman damgası ve önceki adımdan beri geçen süre (bekleme tahmini için),
- aktif pencere (başlık, süreç, pencere dikdörtgeni),
- öğenin çevresinden kırpılmış görüntü (şablon eşleştirme için),
- öğe çevresinin OCR metni,
- pencereye göre oransal koordinat,
- klavye girdisi: **ardışık tuşlar birleştirilip tek INPUT adımı** yapılır.

**Gizlilik:**
- Eğitimi **test müşteri verileriyle** yaparsınız. Kaydedici, girilen değeri test profilindeki
  değerlerle karşılaştırıp otomatik olarak `{{PLAKA}}`, `{{TC_KIMLIK}}`… değişkenine çevirir.
  Eşleşmeyen serbest metin için panel "Bu değer sabit mi, değişken mi?" diye sorar.
- **Giriş ekranında kayıt duraklatılır**; şifre hiçbir zaman kaydedilmez, workflow'da `{{SECRET:login_password}}` olur.
- Eğitim ekran görüntüleri test verisiyle alındığı için saklanabilir; yine de maskelenir.

**Kayıttan workflow'a:** Kaydedici ham olay günlüğü üretir → `workflow_builder` bunu
CLICK/INPUT/SELECT/WAIT adımlarına ve locator listelerine dönüştürür → panelde düzenleyip
"Teklif Sonucu Göründü" gibi bekleme koşullarını ve hedef isimlerini (Türkçe etiket) verirsiniz →
kuru çalıştırma (dry-run) ile test → yayımla (versiyonlu).

---

## 10. Yanlış Müşteri / Yanlış Teklif Önleme

1. Her iş `request_id` + `job_id` ile başlar; robot, formu doldurmadan önce ekranı **temiz**
   duruma getirir (önceki müşterinin verisi kalmamalı — doğrulanır).
2. Sonuç okunduktan sonra ekrandaki **plaka / TC son 4 hane geri okunup** talep ile karşılaştırılır.
3. Teklif kaydı `request_id`'ye bağlanır; `quote_results` tablosunda `request_id` yabancı anahtar.
4. Gönderimden hemen önce **gönderim bekçisi**: `quote.request_id == request.id`,
   `request.customer_id == hedef_telefonun_customer_id`, plaka eşleşmesi, teklif ID eşleşmesi.
   Bir tutarsızlıkta gönderim iptal + MANUEL MÜDAHALE.
5. Giden mesaj **sadece DB'deki talep kaydından** üretilir; robot hiçbir zaman telefon numarası üretmez.
6. Robot tek seferde **tek iş** işler (kuyruk kilidi), iki müşterinin verisi aynı ekranda karışamaz.

---

## 11. Veritabanı (özet)

`customers` (telefon hash + şifreli telefon, ad), `conversations`, `messages`,
`insurance_requests` (ürün, durum, `required_fields`, `missing_fields`), `request_fields`
(alan bazlı, hassaslar şifreli), `quotes` (robot çalıştırması başına), `quote_results`
(şirket bazlı satırlar), `workflow_definitions` (versiyonlu JSON), `workflow_runs`,
`workflow_steps` (adım, locator türü, süre, sonuç, ekran görüntüsü yolu), `jobs` (kuyruk),
`approvals` (mesaj ID, sınıflandırıcı sonuçları, teklif ID), `notifications`, `errors`,
`message_templates` (panelden düzenlenir), `settings`, `audit_log`.

**KVKK:**
- Sadece teklif için gerekli alanlar istenir/saklanır; ürün bazlı zorunlu alan listesi.
- TC kimlik, doğum tarihi, ruhsat seri no → **alan bazlı şifreli**; loglarda maskeli (`*******1234`).
- Loglarda şifre/token/tam TC **yazılmaz** (merkezi redaksiyon filtresi).
- Ekran görüntülerinde hassas alanlar (eğitimde işaretlenen bölgeler + OCR ile bulunan TC/plaka) **bulanıklaştırılır**;
  saklama süresi config'ten (ör. 30 gün) sonra otomatik silinir.
- LLM sağlayıcısına veri **yurt dışına aktarım** sayılabilir: TC vb. maskelenerek gönderilir;
  aydınlatma metni ve gerekiyorsa açık rıza/aktarım mekanizması için hukuki kontrol önerilir.
- Müşteriye ilk mesajda kısa KVKK aydınlatma bağlantısı.

---

## 12. Test / Dry-Run / Modlar

| Mod | WhatsApp | Robot | Poliçe |
|---|---|---|---|
| `DRY_RUN` | Konsola/log'a yazar | Gerçek UI'a dokunmaz; her adımı çözümler (locator bulunuyor mu) ve raporlar | Asla |
| `TEST` | Log (veya sadece izinli test numaralarına) | Gerçek programda **test müşteri verisi** ile | Asla |
| `LIVE` | Gerçek | Gerçek | **Asla** (poliçe her modda insan işi) |

Birim testleri: doğrulayıcılar, onay sınıflandırıcı (onay/ret/belirsiz örnek seti), state machine,
gönderim bekçisi. Entegrasyon: sahte (mock) Open Hızlı Teklif penceresi (küçük bir WinForms/Tk
uygulaması) üzerinde workflow motoru testi. Uçtan uca: WhatsApp Cloud API test numarası.

---

## 13. Teknik Riskler / Engeller

| Risk | Etki | Önlem |
|---|---|---|
| **2FA / oturum zaman aşımı** | Giriş otomatikleşmeyebilir | Oturumu açık tut; giriş ekranı algılanınca size bildirim + MANUEL |
| Windows oturumu kilitli/ekran koruyucu | Ekran görülemez, klavye/fare çalışmaz | Robot PC'sinde kilitlenme kapalı ayrı kullanıcı oturumu (veya VM/RDP'de ayrı oturum) |
| Sanal makineye **RDP** ile bağlanıp pencere küçültülünce ekran çizilmez | Robot ekranı göremez | VM konsolu/otomatik oturum açma veya RDP oturumunu kapatırken `tscon` ile konsola devretme; kurulumda ayrıca belgelenecek |
| Yeni bilgisayarda Open Hızlı Teklif lisansı / 2FA | Robot makinesinde giriş yapılamaz | Lisansın ikinci makineye taşınabilirliği Open Yazılım'a sorulmalı |
| Program güncellemesi ekranı değiştirir | Locator kırılır | Çoklu locator + "ekran değişti" algılama + yeniden eğitim |
| Sonuç tablosu küçük yazı/kaydırmalı | OCR hatası | Dışa aktarma menüsü; OCR'da ön işleme + doğrulayıcılar |
| Sigorta şirketi cevap vermez / yavaş | Eksik sonuç | Zaman aşımı + kısmi sonuçla "gelenler" veya MANUEL (sizin tercihiniz) |
| CAPTCHA | Otomasyon durur | Çözmeye çalışılmaz; MANUEL |
| DPI ölçekleme (%125/%150) | Koordinat/şablon kayar | Process DPI-aware, çok ölçekli şablon, oransal koordinat |
| WhatsApp 24 saat kuralı | Geç teklif gönderilemez | Onaylı "teklifiniz hazır" şablonu |

---

## 14. Faz Planı (öneri)

| Faz | İçerik | Bağımlılık |
|---|---|---|
| 1–2 | Bu rapor + `ortam_analizi.py` çıktısı + ekran görüntüleri/kayıt | **Sizden bilgi** |
| 3 | WhatsApp kanal soyutlaması + Cloud API + konsol (TEST) kanalı | Soru 4–6 |
| 4 | DB modelleri + Alembic + şifreleme + redaksiyon | – |
| 5 | Eğitim modu kaydedici | Ekran görüntüleri/kayıt |
| 6 | Workflow motoru + sürücüler + güvenlik kilidi + dry-run | – |
| 7–8 | Open Hızlı Teklif paketi + sonuç okuma | Ekran görüntüleri, eğitim kaydı |
| 9–11 | Müşteri mesajları, onay sınıflandırıcı, acil bildirim | Soru 10 |
| 12–13 | Panel + log/hata ekranları | – |
| 14–15 | Test seti, güvenlik/KVKK kontrolü | – |

Faz 3, 4, 6 ve 9–11'in büyük kısmı Open Hızlı Teklif ekranlarını beklemeden (sahte pencere ve
DRY_RUN ile) geliştirilebilir. **Faz 7–8 ekranlar görülmeden kesinleştirilmeyecek.**

---

## 15. Sizden İstenen Bilgiler

1. Open Hızlı Teklif'in tam adı ve **versiyonu** (Yardım → Hakkında). MSI mi ClickOnce ile mi kurulu?
2. Yalnızca **Windows masaüstü** programını mı kullanıyorsunuz, yoksa **web/mobil** arayüzü de var mı?
   (Web arayüzü varsa ekran görüntüsü + adres.)
3. Giriş nasıl yapılıyor? Kullanıcı adı/şifre + **2FA (SMS/uygulama)** var mı? Oturum ne kadar açık kalıyor?
4. WhatsApp'ı şu an nasıl kullanıyorsunuz: kişisel WhatsApp / **WhatsApp Business uygulaması** / Business API?
5. **Meta Business hesabınız** var mı, doğrulanmış mı? Aynı numarayı telefonda kullanmaya devam etmek istiyor musunuz?
6. Gelen mesajlar bugün nasıl işleniyor (kaç mesaj/gün, kaç kişi bakıyor, sesli mesaj/fotoğraf — ör. ruhsat fotoğrafı — geliyor mu)?
7. İlk aşamada otomatikleştirilecek ürün(ler): yalnızca **Trafik** ile başlamayı öneririm; Kasko da olsun mu?
8. Trafik teklifi için programın **zorunlu tuttuğu alanlar** neler? (Plaka, TC/VKN, ruhsat seri no, doğum tarihi…?) Tramer/QR ile araç bilgisi otomatik geliyor mu?
9. Ekran görüntüleri (gerçek müşteri verisi **olmadan**): giriş, ana ekran, yeni teklif, müşteri/araç formu, "Teklif Al" sonrası bekleme, **sonuç tablosu**, hata örnekleri, dışa aktarma menüsü.
10. ACİL bildirim hangi kanaldan gelsin? (Önerim: **Telegram** + masaüstü bildirimi; WhatsApp da olabilir.)
11. Bir teklif işleminin **ekran kaydı** (test verisiyle, Win+G veya OBS).
12. Test için **sahte müşteri verileri** (TC algoritmasına uygun test TC, test plakası) — veya gerçek test aracınız/kendi aracınız?
13. Müşteriye birden fazla şirketin teklifi mi gönderilsin, yalnızca en ucuzu mu, en ucuz 3 mü?
14. Robot hangi bilgisayarda çalışacak: sizin günlük kullandığınız PC mi (robot çalışırken fareyi kullanamazsınız), ayrı bir PC/VM mi?
15. `tools/ortam_analizi.py` çıktısı (sadece bilgisayar bilgisi).

---

## Kaynaklar

- [Open Hızlı Teklif – Open Yazılım ürün sayfası](https://openyazilim.com/urunler/open-hizli-teklif)
- [Open Yazılım'dan Hızlı Teklif Sistemi'nde 'Tarih Bazlı Analiz' Özelliği – Sigorta Life Dergi](https://www.sigortalifedergi.com/open-yazilimda-hizli-teklif-sistemi)
- [Open Yazılım – LinkedIn](https://tr.linkedin.com/company/openyazilim)
