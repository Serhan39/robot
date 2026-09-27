# Open Hızlı Teklif v3 – Ekran Analizi

Kullanıcının gönderdiği ekran görüntülerinden çıkarılan bilgiler. Görüntüler `docs/ekranlar/`
altında tutulur ve **müşteri verisi içermez**. Bu dosya, robotun hedef tanımlarının
(klavye sırası / ekrandaki yazı / görüntü) kaynağıdır.

---

## Ekran 01 – Giriş (`ekranlar/01_giris.png`)

Pencere yaklaşık 906×622 piksel. Solda kırmızı tanıtım paneli (Open Yazılım logosu, ürün listesi,
"SMS / Google Authenticator"), sağda giriş formu.

| Öğe | Ekrandaki yazı | Tür | Not |
|---|---|---|---|
| Başlık | `Hoş Geldiniz V3.` | Etiket | **Ekran tanıma işareti:** robot bu yazıyı OCR ile görürse giriş ekranındadır. |
| Alan 1 | `Acente Kodu:` | Metin kutusu | Açılışta **imleç burada** (odak bu alanda). |
| Alan 2 | `Kullanıcı Adı:` | Metin kutusu | |
| Alan 3 | `Şifre:` | Şifre kutusu | Şifre **asla** loglanmaz / kaydedilmez. |
| Bağlantı | `Şifremi Unuttum` | Link | Robot **tıklamaz**. |
| Düğme | `Giriş Yap V3` | Kırmızı düğme | Robot **tıklamaz** (giriş kullanıcıda). |
| Düğme | `İptal` | Beyaz düğme | |
| Sosyal medya düğmeleri | Facebook, Instagram, Linkedin, Twitter, Web, Whatsapp | Düğme | Robot **tıklamaz** (yasak bölge). |

**Gözlemler**
- Alanlar boş açılıyor → program bilgileri hatırlamıyor gibi görünüyor (kullanıcıya teyit ettirilecek).
- İki faktörlü doğrulama: **SMS veya Google Authenticator**.

**Karar (kullanıcı): Programı ve girişi kullanıcı yapar.**
- Robot Open Hızlı Teklif'i **açmaz** ve **giriş yapmaz**; acente kodu, kullanıcı adı, şifre ve
  2FA kodu robota hiç verilmez, hiçbir yerde saklanmaz.
- Robot her işten önce kontrol eder:
  - Open Hızlı Teklif penceresi açık ve **giriş yapılmış** mı? → işe başla.
  - Pencere yok **veya** `Hoş Geldiniz V3.` (giriş ekranı) görünüyor → işi kuyrukta beklet,
    durumu **MANUEL MÜDAHALE – Programı açıp giriş yapın** yap ve size bildirim gönder.
    Siz giriş yapıp panelden "Robotu Devam Ettir"e basınca robot kaldığı yerden devam eder.
- İş sırasında oturum düşerse (giriş ekranı belirirse) aynı şekilde durur, işi yarıda bırakıp
  bildirir; yeniden denemeyi siz onaylarsınız.

**Açık sorular**
- Giriş yapıldıktan sonra oturum ne kadar açık kalıyor (gün boyu mu, belli süre sonra düşüyor mu)?

---

## Ekran 02 – Ana ekran / teklif ekranı (`ekranlar/02_ana_ekran.png`)

Tam ekran (1920×1080), giriş yapılmış hâl. Teklif işlemi **tek ekranda** yapılıyor:
solda şirket/fiyat tablosu, sağda müşteri/araç formu ve komut düğmeleri.

### Ekran tanıma işaretleri
- Pencere başlığı: `Open Hızlı Teklif Sistemi V3 - Ana Acente : … - Sürüm : 3.0.0.443 | Connected`
  → Başlıkta **`Connected`** varsa program bağlı ve hazır. (Sürüm: **3.0.0.443**)
- Üst sekme `ANA EKRAN` seçili.

### Üst sekmeler
`ANA EKRAN` · `ŞİRKETLER (ROBOT)` · `TEKLİFLER` · `POLİÇELERİM` · `Raporlar` · `Destek Taleplerim` ·
`Ajanda / Yenileme` · `Duyurular` · `CANLI ÜRETİM` · `CANLI DESTEK`
→ Robot yalnızca `ANA EKRAN`'da çalışır; `POLİÇELERİM` ve `CANLI ÜRETİM` **yasak bölge**.

### Sağ panel – form (yukarıdan aşağı)
| Etiket | Tür | Varsayılan | Robot için değişken |
|---|---|---|---|
| `Teklif ID :` | Etiket | 0 | Sorgu sonrası okunacak (teklif ID eşleştirmesi) |
| Ürün seçici | Açılır liste | `TRAFIK` | `{{URUN}}` (ilk aşama: TRAFIK) |
| `Tarayıcı 1` | Açılır liste | Tarayıcı 1 | Dokunulmaz |
| `Plaka` + ☑ `Varsa Getir` | Metin + onay kutusu | işaretli | `{{PLAKA}}` |
| `TC / Vergi` + ☐ | Metin + onay kutusu | boş | `{{TC_KIMLIK}}` / `{{VERGI_NO}}` |
| `Belge Seri` | İki metin kutusu (seri kodu + no) | boş | `{{RUHSAT_SERI}}`, `{{RUHSAT_NO}}` |
| `Doğum T.` | Tarih | bugünün tarihi | `{{DOGUM_TARIHI}}` (gerekli mi? – soru) |
| `DT Şirketi` | Açılır liste | BEREKET | Dokunulmaz (ne işe yaradığı sorulacak) |
| `Müşteri` | Metin | boş | `{{AD_SOYAD}}` |
| `Meslek` | Açılır liste | Seçiniz | isteğe bağlı |
| `Telefon` + WhatsApp simgesi + ☐ `Kullan` | Maskeli metin | boş | `{{TELEFON}}`; programın kendi WhatsApp'ı **kullanılmaz** |
| `İl Seçin` / `İlçe Seçin` | Açılır liste | Seçiniz | isteğe bağlı |
| `Açıklama` | Çok satırlı metin | boş | Robot buraya **talep ID** yazabilir (eşleştirme için – önerilir) |
| ☐ `Kısa Vadeli Poliçe Çalış`, ☐ `Trafik Engelli Araç` | Onay kutusu | boş | Dokunulmaz |

### Sağ panel – alt sekmeler (araç)
`Araç Bilgileri` · `Trafik Pol. Bilgisi` · `Kasko Pol. Bilgisi`
Araç Bilgileri: `Kullanım Tarzı`, `Marka`, `Tip`, `Model Yılı`, `Kasko Değeri`, `Tescil Tarihi`,
`Koltuk Sayısı`, `Motor No`, `LPG`, `Şasi No`.
→ Büyük olasılıkla **`Varsa Getir`** işaretliyken plakadan (Tramer/EGM) otomatik doluyor – doğrulanacak.

### Komut düğmeleri
| Düğme | Robot kullanır mı? |
|---|---|
| `Sorguyu Başlat` | **Evet** – teklif al |
| `Temizle` | **Evet** – her işten önce formu temizler (önceki müşteri verisi kalmasın) |
| `Yeni Sorgu Kaydet` | Belki (teklifi programda kaydetmek için – sorulacak) |
| `Kuyruklama Sorgu`, `Duraklat / Devam Et` | Hayır (ilk aşama) |
| `Ruhsat QR`, `Sbm Sorgu`, `Webcam QR Oku`, `Pdf Yükle`, `2. Tarayıcıları Kapat` | Hayır |

### Sol panel – şirket / fiyat tablosu
- Satırlar: `AK`, `AXA`, `BEREKET`, `QUICK_PORT…`, `SOMPO` (her birinde ☑ seçim kutusu).
- Sütunlar: `Şirket`, 4 simge sütunu, `Trafik`, `Sbm`, `Kasko`, `TSS Ayak.`, `TSS Yat.`, `Konut`, `Dask`,
  `IMM`, `%`, `Uyarı`, `Kategori`, `T.Koms`, `K.Koms`, `Knt.Koms`, `IMM Kom…`
- Trafik teklifinde fiyat **`Trafik` sütununa** gelir; **`Uyarı`** sütunu hata/red mesajı için okunacak.
- **Komisyon sütunları (`T.Koms` vb.) müşteriye asla gönderilmez.**
- Not satırı: "Şirket ismi KIRMIZI olduğunda Yeni JET API sisteminden fiyat alınmıştır."
- Araç çubuğu: `Diğer Fiyatları Göster`, `Jet API ile Fiyat Çalış` (açılır liste), `Alt Fiyat`,
  **`PDF Aktar`**, yeşil (muhtemelen **Excel**) simgesi, kopyala, `+`, kırmızı simge.
  → Sonuç okumada **Excel dışa aktarma** en güvenilir yol olabilir (doğrulanacak).
- ⚠️ **Satırlardaki 4 simge** (biri kalem/imza görünümlü) ne işe yarıyor bilinmiyor; biri
  poliçeleştirme olabilir. Öğrenilene kadar robot bu simge sütunlarına **hiç tıklamaz**.

### Alt durum çubuğu
`Tramer` · `Egm` · `Sanal T.` · `Dışa Al` · `Ram` göstergesi · `Yönetici` · `Eğitim (YENİ)` · `OpenDesk`

### Taslak trafik teklifi akışı (doğrulanacak)
1. Başlıkta `Connected` ve `ANA EKRAN` seçili mi kontrol et.
2. `Temizle`.
3. Ürün = `TRAFIK`.
4. `Plaka` ← `{{PLAKA}}` (Varsa Getir işaretli) → araç bilgileri gelene kadar bekle.
5. `TC / Vergi` ← `{{TC_KIMLIK}}`; `Belge Seri` ← `{{RUHSAT_SERI}}` + `{{RUHSAT_NO}}`.
6. `Müşteri` ← `{{AD_SOYAD}}`, `Açıklama` ← `TALEP-{{TALEP_ID}}`.
7. Her alan OCR ile geri okunup doğrulanır.
8. `Sorguyu Başlat` → `Trafik` sütunu dolana / zaman aşımına kadar bekle.
9. `Teklif ID` + tablo okunur (Excel dışa aktarma veya OCR), plaka tekrar doğrulanır.
