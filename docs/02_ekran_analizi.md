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
