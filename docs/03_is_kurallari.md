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

| Bilgi | Yenileme | Yeni alım | Doğrulama |
|---|---|---|---|
| Plaka | ✅ | ✅ (soru: sıfır araçta plaka yoksa?) | TR plaka formatı |
| TC Kimlik No (veya VKN) | ✅ araç sahibi | ✅ alıcı | TC sağlama algoritması / VKN 10 hane |
| Doğum tarihi | ✅ araç sahibi | ✅ alıcı | Geçerli tarih, 18+ yaş (soru: tüzel kişide?) |
| Ruhsat belge seri + no | ✅ | (soru: satıcının ruhsatı mı, gerekmiyor mu?) | Seri: 2 harf, No: 6 hane (soru) |
| Ad Soyad | ✅ (hitap + `Müşteri` alanı) | ✅ alıcı | – |
| Telefon | WhatsApp numarasından otomatik | aynı | – |

Programın formundaki `Doğum T.` alanı **varsayılan olarak bugünün tarihiyle** gelir → robot bu
alanı **her zaman** doldurur ve geri okuyarak doğrular; boş/varsayılan bırakılırsa teklif hatalı olur.

## 3. Konuşma akışı etkisi

`COLLECTING_INFORMATION` durumunda önce **talep türü** (yenileme / yeni alım), sonra o türün
eksik alanları sorulur. Talep türü değişirse (müşteri "aslında yeni aldım" derse) daha önce
alınan kişi bilgileri **geçersiz sayılır** ve yeniden istenir.

## 4. Açık sorular
- Yeni alımda plaka ve ruhsat belge seri/no nasıl giriliyor? (satıcının ruhsatı / noter satış belgesi / boş)
- Sıfır (galeriden yeni) araçta plaka yoksa programda ne giriliyor (şasi no, motor no)?
- Şirket adına (VKN) araçlarda doğum tarihi yerine ne giriliyor?
