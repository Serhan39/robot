# İş Kuralları – Trafik Sigortası (ilk aşama)

Kullanıcıdan (acente) alınan bilgilere göre. Robot ve WhatsApp katmanı bu kurallara göre
müşteriden bilgi ister. **Doğrulanmamış maddeler "(soru)" ile işaretlidir.**

## 1. Önce talep türü belirlenir

Müşteriye ilk sorulacak şey:

> "Aracınızın mevcut trafik sigortasını mı **yenilemek** istiyorsunuz, yoksa aracı **yeni mi
> satın alıyorsunuz**?"

LLM mesajdan bunu çıkarabilirse (ör. "sigortam bitiyor", "yeni araba aldım") ayrıca sormaz,
ama emin değilse **mutlaka sorar**; tahmin etmez.

| Durum | Kimin bilgileri girilir |
|---|---|
| **Yenileme** | **Mevcut araç sahibinin** (ruhsat sahibi) bilgileri |
| **Yeni alım** (araç yeni satın alınıyor / devir) | **Aracı alacak kişinin** bilgileri |

## 2. Gerekli bilgiler

| Bilgi | Yenileme | Yeni alım (ikinci el) | Sıfır araç (plakasız) | Doğrulama |
|---|---|---|---|---|
| Plaka | ✅ | ✅ satıcının ruhsatındaki | **il kodu + `YK`** (ör. `34YK`) – acente bilgisi | TR plaka düzeni / `NNYK` |
| TC Kimlik No | ✅ araç sahibi | ✅ **alıcı** | ✅ aracın kaydedileceği kişi | Resmi kontrol hanesi algoritması |
| Doğum tarihi | ✅ araç sahibi | ✅ alıcı | ✅ | Geçerli tarih, 18+ yaş, bugünün tarihi olamaz |
| Ruhsat belge seri + no | ✅ | ✅ **satıcının ruhsatındaki** (araştırma) | – (ruhsat yok) | 2 harf + 6 rakam (ör. `AB 123456`) |
| Ad Soyad | ✅ | ✅ alıcı | ✅ | – |
| Tescil il kodu | – | – | ✅ | 01–81 |
| Telefon | WhatsApp numarasından | aynı | aynı | TR cep → `905XXXXXXXXX` |

Programın formundaki `Doğum T.` alanı **varsayılan olarak bugünün tarihiyle** gelir → robot bu
alanı **her zaman** doldurur ve geri okuyarak doğrular; bugünün tarihi asla geçerli sayılmaz.

## 3. Araştırma notları (26.10.2026)

- **Belge seri:** Araç tescil belgesinin (ruhsat) ön yüzündeki "Belge Seri" = 2 harf + 6 rakam.
  Programda iki ayrı kutuya girilir (seri / no). Gönderilen ekranda da bu biçim görüldü.
- **Yeni alım (ikinci el):** Yaygın uygulama: poliçe **alıcının** TC'si ile, araç bilgileri ise
  **satıcının ruhsatından** (plaka, belge seri, tescil tarihi) girilir; noter satışı poliçe olmadan
  yapılmaz. Satıştan sonra yeni ruhsat bilgileriyle zeyil yapılır. 5 Aralık 2024 Anayasa Mahkemesi
  kararıyla eski sahibin poliçesini 15 gün kullanma uygulaması kalktı. Kaynak: sigorta şirketi /
  acente blogları (resmî mevzuat değil) → **acente teyidi gerekli.**
- **Sıfır araç:** Acente bilgisi: plaka yerine **il kodu + `YK`** (yeni kayıt) girilir. Forum
  kaynakları da `34 YK 001` gibi poliçeleri ve sonradan plaka zeyli yapıldığını anlatıyor.
  Şasi / motor no gerekip gerekmediği **açık soru**.
- **Şirket adına (tüzel kişi):** TC yerine **vergi kimlik numarası (10 hane)** girildiği doğrulandı
  (AXA, SBM formları). Doğum tarihi yerine ne girildiğine dair kaynak **bulunamadı** → acenteye sorulacak.
  Tüzel kişi akışı ilk aşamada **kapsam dışı**: robot VKN'li talepleri MANUEL'e düşürür.
- **TC girince bilgilerin dolması:** Üretici sayfası doğum tarihinin ve marka/model kodlarının
  (Tramer) sigorta şirketi entegrasyonlarıyla otomatik getirildiğini söylüyor; ad soyad ve il/ilçe
  için bilgi yok → acente ekranda deneyip söyleyecek. Robot her durumda kendi verisini yazar ve
  ekrandaki değeri geri okuyup karşılaştırır (uyuşmazlık → MANUEL).

## 4. Konuşma akışı etkisi

`COLLECTING_INFORMATION` durumunda önce **talep türü** (yenileme / yeni alım / sıfır), sonra o türün
eksik alanları sırayla sorulur (`app/insurance/trafik.py`). Talep türü değişirse daha önce alınan
kişi ve belge bilgileri **geçersiz sayılır** ve yeniden istenir (yalnızca telefon korunur).

## 5. Açık sorular
- Sıfır araçta şasi no / motor no isteniyor mu? Plaka tam olarak `34YK` mı, `34YK001` gibi mi?
- Şirket adına (VKN) araçlarda doğum tarihi alanına ne giriliyor?
- TC girilince ad soyad / il / ilçe kendiliğinden doluyor mu?
- Yeni alımda belge seri satıcının ruhsatından mı giriliyor? (araştırma: evet – teyit)
