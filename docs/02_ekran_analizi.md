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
| Düğme | `Giriş Yap V3` | Kırmızı düğme | |
| Düğme | `İptal` | Beyaz düğme | |
| Sosyal medya düğmeleri | Facebook, Instagram, Linkedin, Twitter, Web, Whatsapp | Düğme | Robot **tıklamaz** (yasak bölge). |

**Gözlemler**
- Alanlar boş açılıyor → program bilgileri hatırlamıyor gibi görünüyor (kullanıcıya teyit ettirilecek).
- İki faktörlü doğrulama: **SMS veya Google Authenticator**.

**Robotun giriş planı (taslak – doğrulanacak)**
1. `Hoş Geldiniz V3.` yazısını OCR ile gör → giriş ekranı.
2. Odak Acente Kodu'nda → `{{SECRET:acente_kodu}}` yaz → **Tab** → `{{SECRET:kullanici_adi}}` → **Tab** → `{{SECRET:sifre}}`.
3. `Giriş Yap V3` düğmesini OCR ile bul ve tıkla (veya Enter – teyit edilecek).
4. Her alan doldurulduktan sonra (şifre hariç) alan bölgesi OCR ile geri okunup doğrulanır.
5. Bilgiler Windows Credential Manager'da saklanır; kodda/logda yer almaz.

**İki faktörlü doğrulama seçenekleri**
- **SMS:** Robot kodu göremez → giriş gerektiğinde **MANUEL MÜDAHALE** + size bildirim; siz kodu girersiniz.
  Oturum açık kaldığı sürece robot çalışmaya devam eder.
- **Google Authenticator:** Kurulumdaki gizli anahtar robot makinesine (Credential Manager) verilirse
  robot kodu kendisi üretebilir. Ancak bu, 2FA'nın korumasını robot makinesine taşır → **yalnızca
  kullanıcı açıkça isterse**. Varsayılan: SMS ile aynı, manuel.

**Açık sorular**
- Hangi 2FA yöntemi kullanılıyor, ne sıklıkla soruluyor?
- Tab sırası Acente Kodu → Kullanıcı Adı → Şifre mi? Şifre alanında Enter girişi başlatıyor mu?
