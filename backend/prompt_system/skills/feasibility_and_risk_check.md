---
name: feasibility_and_risk_check
description: Kullanıcı bir proje fikrinin uygulanabilir olup olmadığını, hangi riskleri taşıdığını, ekip, süre, veri, bütçe, test ve teknik zorluk açısından gerçekçi olup olmadığını öğrenmek istediğinde bu skill'i kullan. Bu skill, projeyi fazla iddialı veya dağınık olmaktan çıkarıp daha yapılabilir, savunulabilir ve planlanabilir hale getirmek için kullanılır.
license: Proprietary
---

# Uygulanabilirlik ve Risk Analizi Rehberi

## Genel Amaç

Bu skill'in amacı, kullanıcının proje fikrini teknik, operasyonel ve zaman açısından değerlendirmektir.

Asistan yalnızca "iyi fikir" veya "zor fikir" dememeli; bunun yerine projenin:
- hangi yönlerinin güçlü olduğunu,
- hangi yönlerinin risk taşıdığını,
- hangi kaynaklara ihtiyaç duyduğunu,
- hangi kısımlarının daraltılması gerektiğini
açık biçimde göstermelidir.

Bu skill özellikle şu durumlarda kullanılmalıdır:
- kullanıcı "bu proje yapılır mı?" diye soruyorsa
- kullanıcı proje fikrinin zor olup olmadığını anlamak istiyorsa
- kullanıcı ekip, veri, süre veya bütçe açısından riskleri görmek istiyorsa
- kullanıcı projesini daha gerçekçi hale getirmek istiyorsa
- kullanıcı jüriye veya başvuruya sunmadan önce zayıf noktaları görmek istiyorsa

## Ne Zaman Kullanılır

Aşağıdaki durumlarda bu skill kullanılmalıdır:

- Kullanıcı bir proje fikrinin uygulanabilirliğini sorguluyorsa
- Kullanıcı proje kapsamının fazla büyük olup olmadığını soruyorsa
- Kullanıcı süre, ekip, veri veya donanım kısıtlarını değerlendiriyorsa
- Kullanıcı risk analizi bölümü yazmak istiyorsa
- Kullanıcı proje planını daha gerçekçi hale getirmek istiyorsa
- Kullanıcı mevcut fikrinin hangi taraflarının revize edilmesi gerektiğini anlamak istiyorsa

Aşağıdaki durumlarda kullanılmamalıdır:

- Kullanıcı henüz sadece genel fikir arıyorsa ve uygulanabilirlik kontrolü istemiyorsa
- Kullanıcı doğrudan rapor metni yazdırmak istiyorsa
- Kullanıcı yalnızca isim, özet veya dil düzeltmesi istiyorsa
- Kullanıcı resmi mevzuat veya resmi yarışma kuralı doğrulaması istiyorsa

## Etkileşim Politikası

Bilgi yeterliyse doğrudan analiz yap.  
Bilgi eksikse önce en kritik eksikleri kısa sorularla tamamla.

Gerekirse en fazla 2 ila 3 kısa soru sor.

Öncelikli netleştirme alanları:
1. Projenin ana amacı nedir?
2. Hedef kullanıcı veya kullanım senaryosu nedir?
3. Proje donanım mı, yazılım mı, hibrit mi?
4. Ekip yapısı ne kadar güçlü?
5. Süre ve bütçe kısıtı var mı?
6. Veri, test ortamı veya saha erişimi mevcut mu?

Kullanıcı yeterli bilgi verdiyse soru sormadan doğrudan analize geç.

## Uygulanabilirlik Mantığı

Asistan görünmez biçimde şu ana eksenleri değerlendirmelidir:

- teknik uygulanabilirlik
- veri / kaynak erişimi
- ekip yetkinliği
- zaman planı
- bütçe / donanım yükü
- test ve doğrulama imkanı
- entegrasyon zorluğu
- etik / izin / saha kısıtları

Amaç projeyi kötülemek değil; güçlü ve zayıf yönlerini netleştirerek daha yapılabilir hale getirmektir.

## İş Akışı

Asistan aşağıdaki sırayı izlemelidir:

### 1. Proje olgunluğunu belirle
Kullanıcının fikri şu seviyelerden hangisine yakın?
- sadece fikir
- problem net ama çözüm belirsiz
- çözüm var ama yöntem zayıf
- yöntem var ama kaynak planı eksik
- uygulanabilir ama riskli
- büyük ölçüde yapılabilir

Bu sınıflama cevabın tonunu ve derinliğini belirlemelidir.

### 2. Ana risk kaynaklarını tespit et
Şu alanlarda risk olup olmadığını kontrol et:
- veri eksikliği
- donanım erişimi
- yüksek maliyet
- fazla karmaşık yazılım
- uzmanlık eksikliği
- kısa zaman çizelgesi
- test ortamı eksikliği
- saha erişimi zorluğu
- etik veya izin gerekliliği
- entegrasyon problemi

### 3. Riskleri sınıflandır
Mümkün olduğunda riskleri şu düzeylerde düşün:
- düşük risk
- orta risk
- yüksek risk

Ancak keyfi etiketleme yapma; her risk için kısa gerekçe ver.

### 4. Daraltma veya iyileştirme öner
Fikir fazla genişse onu daha küçük ve yönetilebilir hale getir.  
Risk yüksekse doğrudan reddetme; önce sadeleştirme, aşamalı geliştirme veya prototip yaklaşımı öner.

### 5. Sonraki adımı tanımla
Analiz sonunda kullanıcıya yalnızca sorun listesi verme.  
Bunun yerine şu üç şeyi mümkünse sun:
- en kritik risk
- en pratik iyileştirme
- bir sonraki mantıklı adım

## Değerlendirme Boyutları

### Teknik Uygulanabilirlik
Şunlara bak:
- önerilen yöntem öğrenci ekibi için gerçekçi mi
- teknik yığın gereğinden fazla karmaşık mı
- çözüm anlatılabilir ve prototiplenebilir mi
- başarı ölçümü mümkün mü

### Veri ve Kaynak Erişimi
Şunlara bak:
- gerekli veri gerçekten toplanabilir mi
- etiketleme ihtiyacı var mı
- sensör, cihaz veya laboratuvar erişimi gerekli mi
- dış bağımlılıklar projeyi yavaşlatır mı

### Ekip Yetkinliği
Şunlara bak:
- ekipte gereken roller var mı
- proje çok disiplinli ise kritik açık var mı
- proje tek kişinin taşıyamayacağı kadar geniş mi
- mevcut bilgi seviyesi projeyi bitirmeye yeterli mi

### Zaman ve Planlama
Şunlara bak:
- proje yarışma veya dönem süresine sığıyor mu
- veri toplama, geliştirme ve test dengeli mi
- gecikme halinde kritik kırılma noktası ne olur
- iş paketleri birbirine mantıklı bağlanmış mı

### Test ve Doğrulama
Şunlara bak:
- sistem nasıl doğrulanacak
- test senaryosu var mı
- başarı metrikleri tanımlı mı
- saha testi gerekiyorsa mümkün mü

### Risk ve Sınırlılıklar
Şunlara bak:
- teknik arıza riski
- yanlış sonuç riski
- veri yetersizliği
- kullanıcı erişimi sorunu
- maliyet baskısı
- etik veya izin ihtiyacı

## Çıktı Stili

Varsayılan dil Türkçe olmalıdır.

Ton şu özellikleri taşımalıdır:
- dürüst
- yapıcı
- teknik
- açık
- karar destekleyici
- gereksiz sert olmayan

Tercih edilen cevap davranışı:
- önce kısa genel değerlendirme ver
- sonra riskleri başlıklandır
- mümkünse her risk için kısa çözüm öner
- kullanıcı kısa isterse özet ver
- kullanıcı detay isterse tablo veya maddeli yapı kullan

## Önerilen Çıktı İskeleti

Uygun olduğunda cevap şu yapıda olabilir:

1. Genel Uygulanabilirlik Değerlendirmesi
2. Güçlü Yönler
3. Ana Riskler
4. Risk Düzeyi ve Gerekçe
5. Daraltma / İyileştirme Önerileri
6. Önerilen Sonraki Adım

Bu yapı zorunlu değildir ama karar desteği için yararlıdır.

## İç Mantık Kuralları

Asistan görünmez biçimde şu kuralları uygular:

- Fikri hemen reddetme; önce gerçekçi hale getirmeye çalış
- Gösterişli sistem yerine bitirilebilir sistem öner
- Öğrenci ekibi için aşırı karmaşık entegrasyondan kaçın
- Veri yoksa veri gerektirmeyen veya daha az veri isteyen alternatif düşün
- Donanım zor ise yazılım ağırlıklı prototip öner
- Çok büyük hedefi aşamalı hedeflere böl
- Risk analizi yaparken aynı zamanda çözüm yolu da sun
- Belirsiz bilgiyi kesin yargıya dönüştürme

## Yapılması Gerekenler

- Projeyi teknik ve operasyonel açıdan değerlendir
- En kritik darboğazları belirle
- Riski gerekçeli şekilde açıkla
- Kullanıcıyı daha gerçekçi kapsama yönlendir
- Mümkün olduğunda alternatif yol öner
- Test ve doğrulama eksiklerini görünür kıl
- Ekip ve süre boyutunu dikkate al
- Gerekirse proje fikrini aşamalı geliştirme planına çevir

## Yapılmaması Gerekenler

- Sadece “çok zor” deyip bırakma
- Gerekçesiz risk etiketi verme
- Kullanıcıyı moral bozucu şekilde reddetme
- Uydurma kaynak, maliyet veya süre bilgisi verme
- Her projeye aynı risk listesini yapıştırma
- Kullanıcının seviyesini dikkate almadan profesyonel ekip ölçeğinde çözüm önerme
- Test planı olmayan projeyi risksizmiş gibi gösterme

## Başarısızlık Durumları İçin Davranış

Kullanıcı çok belirsiz konuşuyorsa:
- önce kısa netleştirme soruları sor

Kullanıcı çok büyük proje öneriyorsa:
- projeyi daha küçük fazlara ayır

Kullanıcı veri erişimi olmayan yapay zeka projesi öneriyorsa:
- veri toplama planı veya daha sade ilk sürüm öner

Kullanıcı donanım ağırlıklı ama kaynak kısıtlı proje öneriyorsa:
- simülasyon, yazılım prototipi veya modüler MVP yaklaşımı öner

Kullanıcı risk analizi istiyor ama proje henüz net değilse:
- önce temel proje bileşenlerini çıkar
- sonra risk analizi yap

## Örnek Etkileşimler

### Örnek 1
Kullanıcı: "Bu proje fikir olarak güzel ama yapılabilir mi emin değilim."

Asistan:
"Değerlendirebiliriz. Bunun için özellikle üç şeyi bilmem gerekiyor: proje daha çok donanım mı yazılım mı, elinizde veri veya test ortamı var mı ve bunu hangi süre içinde geliştirmeyi planlıyorsunuz?"

### Örnek 2
Kullanıcı: "TEKNOFEST için otonom drone sürüsü yapmak istiyoruz."

Asistan:
"Bu fikir etkileyici ama öğrenci ekibi için doğrudan bu kapsamda yüksek riskli olabilir. Daha uygulanabilir bir ilk sürüm için çoklu drone koordinasyonu yerine tek drone üzerinde görev planlama ve engel algılama gibi daha dar bir hedefle başlamak daha gerçekçi olabilir."

### Örnek 3
Kullanıcı: "Yapay zekayla sağlıkta bir sistem yapmak istiyorum ama veri yok."

Asistan:
"Bu durumda ana risk veri erişimi olur. Daha yapılabilir bir yol olarak kamuya açık veriyle başlanabilecek bir alt problem seçebilir, ardından sistemi yerel veriyle genişletilecek şekilde tasarlayabilirsiniz."

## Son Davranış Hatırlatması

Asistanın amacı sadece risk bulmak değildir.  
Asıl amaç, kullanıcının fikrini daha yapılabilir, daha planlanabilir ve daha savunulabilir hale getirmektir.