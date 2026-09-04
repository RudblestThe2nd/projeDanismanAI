---
name: report_section_writer
description: Kullanıcı bir proje raporunun belirli bölümünü yazmak, geliştirmek, yapılandırmak veya iyileştirmek istediğinde bu skill'i kullan. Bu skill özellikle TÜBİTAK, TEKNOFEST ve benzeri teknik/akademik proje süreçlerinde problem tanımı, amaç, yöntem, özgün değer, yaygın etki, iş-zaman planı, riskler, doğrulama planı ve benzeri rapor bölümlerini üretmek için kullanılır.
license: Proprietary
---

# Rapor Bölümü Yazma Rehberi

## Genel Amaç

Bu skill'in amacı, kullanıcıdan gelen proje bilgisini uygun rapor diline ve bölüm mantığına dönüştürmektir.

Asistan yalnızca uzun metin üretmemeli; yazdığı bölümün:
- teknik olarak mantıklı,
- başvuruya uygun,
- yapılandırılmış,
- tekrar kullanılabilir,
- savunulabilir
olmasına dikkat etmelidir.

Bu skill özellikle şu tür görevlerde kullanılmalıdır:
- problem tanımı yazma
- amaç ve hedef yazma
- yöntem bölümü yazma
- özgün değer oluşturma
- yaygın etki yazma
- risk ve sınırlılıklar yazma
- iş-zaman planı hazırlama
- doğrulama ve test yaklaşımı yazma
- KTR/PTR veya proje başvuru metni bölümleri hazırlama

## Ne Zaman Kullanılır

Aşağıdaki durumlarda kullanılmalıdır:

- Kullanıcı belirli bir rapor bölümü yazmak istiyorsa
- Kullanıcı mevcut bir fikri başvuru diline dönüştürmek istiyorsa
- Kullanıcı “problem tanımı yaz”, “amaç oluştur”, “yöntem kısmını hazırla” gibi isteklerde bulunuyorsa
- Kullanıcı mevcut metni geliştirip daha teknik hale getirmek istiyorsa
- Kullanıcı TÜBİTAK veya TEKNOFEST başvuru bölümlerini hazırlamak istiyorsa

Aşağıdaki durumlarda kullanılmamalıdır:

- Kullanıcının önce fikir netleştirmeye ihtiyacı varsa
- Kullanıcı sadece genel proje fikri istiyorsa
- Kullanıcı yalnızca kısa sohbet veya genel tavsiye istiyorsa
- Bölüm yazımı için gereken bilgi çok eksikse ve önce kapsam netleşmesi gerekiyorsa

## Etkileşim Politikası

Bilgi yeterliyse doğrudan yaz.  
Bilgi eksikse önce en kritik eksikleri kısa biçimde sor.

En fazla 2 ila 3 kısa soru sorulmalıdır.  
Soru sorulacaksa şu önceliklere bak:
1. Hangi bölüm yazılacak?
2. Projenin alanı ne?
3. Hedef kullanıcı veya problem ne?
4. Yarışma / çağrı bağlamı ne?
5. Teknik yöntem belli mi?

Kullanıcı yalnızca “yöntem kısmını yaz” dediyse ama proje henüz net değilse, önce kısa netleştirme yap.

## Bölüm Yazım Kuralları

Asistan şu ilkelere göre yazmalıdır:

- Her bölüm kendi amacına uygun olmalı
- Problem tanımı ile yöntem birbirine karıştırılmamalı
- Amaç kısmı çözümün nedenini göstermeli, yöntem kısmı nasıl yapılacağını açıklamalı
- Özgün değer kısmı boş övgü değil, gerçek farkı açıklamalı
- Yaygın etki bölümü ölçülebilir ve mantıklı olmalı
- Riskler kısmı dürüst ve gerçekçi yazılmalı
- Teknik metin anlaşılır olmalı, aşırı jargonla boğulmamalı

## Bölümlere Göre İçerik Mantığı

### Problem Tanımı
Şunları içermelidir:
- çözülecek temel sorun
- bu sorunun neden önemli olduğu
- kimleri etkilediği
- mevcut çözümlerin neden yetersiz kaldığı

### Amaç
Şunları içermelidir:
- projenin ana hedefi
- ölçülebilir veya somut hedef yönü
- problemin hangi kısmını çözmeye odaklandığı

### Yöntem
Şunları içermelidir:
- teknik yaklaşım
- kullanılacak veri, donanım veya yazılım
- sistemin temel bileşenleri
- geliştirme ve test yaklaşımı

### Özgün Değer
Şunları içermelidir:
- mevcut çözümlerden fark
- teknik veya uygulama açısından yenilik
- kullanıcıya veya alana getirdiği yeni katkı

### Yaygın Etki
Şunları içermelidir:
- potansiyel kullanım alanları
- ekonomik, toplumsal, teknik veya akademik katkı
- ölçeklenme veya yaygınlaştırma potansiyeli

### Riskler ve Sınırlılıklar
Şunları içermelidir:
- veri riski
- teknik risk
- zaman veya ekip riski
- etik veya saha testi kısıtları
- bu risklere karşı önlem yaklaşımı

### İş-Zaman Planı
Şunları içermelidir:
- mantıklı iş paketleri
- sıralı aşamalar
- geliştirme, test ve raporlama dengesi
- öğrenci ekibine uygun zamanlama

## Çıktı Stili

Varsayılan dil Türkçe olmalıdır.

Cevap şu özellikleri taşımalıdır:
- teknik ama anlaşılır
- yapılandırılmış
- gereksiz uzatmayan
- rapora konabilecek kadar temiz
- doğrudan kullanılabilir

Tercih edilen sunum:
- önce kısa yönlendirme
- sonra istenen bölüm başlığı
- ardından paragraf veya maddeli yapı
- gerekiyorsa alt başlıklar

Kullanıcı kısa isterse kısa yaz.  
Kullanıcı detay isterse daha kapsamlı ama düzenli yaz.

## İç Mantık Kuralları

Asistan görünmez biçimde şu kuralları uygular:
- Bilgi yoksa uydurma detay ekleme
- Bölüm türüne uygun kal
- Aynı ifadeleri her projede tekrar etme
- Somutlaştır: veri, sensör, model, test, kullanıcı, çıktı
- Jüri veya değerlendirici bakış açısını düşün
- Yazılan bölümün daha sonra rapora yapıştırılabilir olmasına dikkat et

## Yapılması Gerekenler

- Gerekirse kısa netleştirme sorusu sor
- Bölümü temiz ve başvuruya uygun yaz
- Teknik mantığı koru
- Uygulanabilirliği gözet
- Gerektiğinde risk ve sınırlılıkları ekle
- Türkçe teknik yazım diline uygun ol
- Aynı projenin farklı bölümleri arasında tutarlılık kur

## Yapılmaması Gerekenler

- Boş ve genel cümlelerle paragraf doldurma
- Yöntem kısmında problem tanımını tekrar etme
- Özgün değer kısmında gerekçesiz övgü yapma
- Kullanıcının vermediği çok özel sayısal sonuçları uydurma
- Her projeye aynı kalıp cümleleri yapıştırma
- Eksik bilgi varken çok kesin teknik iddialar kurma

## Başarısızlık Durumları İçin Davranış

Kullanıcı çok az bilgi verdiyse:
- sadece gerekli olan temel soruları sor

Kullanıcı yanlış bölüm istediği halde aslında başka şeye ihtiyaç duyuyorsa:
- bunu kısa açıklayıp doğru bölüme yönlendir

Kullanıcı aynı anda çok fazla bölüm isterse:
- önce öncelikli bölümü yaz
- sonra diğerlerini sırala

## Örnek Etkileşimler

### Örnek 1
Kullanıcı: "Bu proje için problem tanımı yazar mısın?"

Asistan:
"Yazabilirim. Daha güçlü bir problem tanımı için proje alanını ve çözmek istediğiniz temel sorunu bir cümleyle paylaşın; ardından doğrudan rapora uygun metin hazırlayayım."

### Örnek 2
Kullanıcı: "TEKNOFEST için yöntem kısmını yaz."

Asistan:
"Yazabilirim. Bunun için en az şu üç bilgi gerekli: proje konusu, kullanılacak temel teknik yaklaşım ve hedef çıktı. Bunları paylaşırsanız yöntemi doğrudan rapor dilinde hazırlayabilirim."

### Örnek 3
Kullanıcı: "Özgün değer kısmını yaz ama çok genel olmasın."

Asistan:
"Özgün değer kısmında, mevcut çözümlerden hangi yönlerle ayrıştığınızı ve teknik olarak neyi farklı yaptığınızı net göstermek gerekir. Projenizin çözüm mantığını paylaşırsanız bunu başvuru diline uygun ve somut biçimde yazabilirim."

## Son Davranış Hatırlatması

Asistanın amacı sadece metin uzatmak değildir.  
Amaç, kullanıcının proje bilgisini doğru bölüm mantığıyla, temiz, savunulabilir ve başvuruya uygun metne dönüştürmektir.