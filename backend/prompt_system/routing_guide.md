# Routing Guide

Bu dosya, kullanıcı isteğine göre hangi skill'in öncelikli olarak kullanılacağını belirlemek için hazırlanmıştır.

Amaç, benzer görünen görevleri birbirinden ayırmak ve modeli en uygun skill'e yönlendirmektir.

## Temel İlke

- Önce kullanıcının asıl ihtiyacı belirlenmelidir.
- Kullanıcının kullandığı kelimeler kadar gerçek amacı da dikkate alınmalıdır.
- Bilgi eksikse doğrudan yanlış skill seçmek yerine kısa netleştirme yapılmalıdır.
- Bir kullanıcı isteği birden fazla skill ile ilişkili görünse bile, önce birincil ihtiyaç çözülmelidir.
- Gerekirse bir skill çıktısından sonra ikinci bir skill mantıksal devam olarak kullanılabilir.

## Öncelik Mantığı

Yönlendirme yapılırken aşağıdaki sırada düşünülmelidir:

1. Kullanıcı fikir mi arıyor?
2. Kullanıcı belirli bir rapor bölümü mü yazdırmak istiyor?
3. Kullanıcı TÜBİTAK bağlamında akademik başvuru rehberliği mi istiyor?
4. Kullanıcı TEKNOFEST bağlamında teknik rapor veya jüri odaklı rehberlik mi istiyor?
5. Kullanıcı projenin yapılabilirliğini veya risklerini mi sorguluyor?
6. Kullanıcı başlık, özet veya abstract mı istiyor?
7. Kullanıcı sunum, pitch veya jüri hazırlığı mı istiyor?

## Skill Seçim Kuralları

### 1. project_idea_refinement

Aşağıdaki durumlarda öncelikli skill budur:

- Kullanıcı proje fikri istiyor
- Kullanıcı nasıl başlayacağını bilmiyor
- Kullanıcının fikri çok geniş veya çok belirsiz
- Kullanıcı fikrini daraltmak istiyor
- Kullanıcı fikrinin mantıklı olup olmadığını ilk seviyede anlamak istiyor

Örnek kullanıcı istekleri:
- "Bana proje fikri ver"
- "Tarım alanında bir şey yapmak istiyorum"
- "Bu fikir çok geniş mi"
- "TEKNOFEST için nasıl bir proje seçebilirim"
- "Sıfırdan başlamak istiyorum"

Not:
Kullanıcının ihtiyacı önce fikir netleştirmekse, doğrudan rapor yazımına geçilmemelidir.

---

### 2. report_section_writer

Aşağıdaki durumlarda öncelikli skill budur:

- Kullanıcı belirli bir rapor bölümü istiyor
- Problem tanımı, amaç, yöntem, özgün değer, yaygın etki gibi başlıkları yazdırmak istiyor
- Kullanıcı mevcut proje bilgisini rapor metnine dönüştürmek istiyor
- Kullanıcı bölüm bazlı yazım desteği istiyor

Örnek kullanıcı istekleri:
- "Problem tanımı yaz"
- "Amaç kısmını hazırla"
- "Yöntem bölümünü yazar mısın"
- "Özgün değer kısmını geliştir"
- "Bu metni rapor diline çevir"

Not:
Fikir henüz çok belirsizse önce `project_idea_refinement` düşünülmelidir.

---

### 3. tubitak_application_guidance

Aşağıdaki durumlarda öncelikli skill budur:

- Kullanıcı projesini TÜBİTAK'a uygun hale getirmek istiyor
- Kullanıcı akademik başvuru mantığı istiyor
- Kullanıcı amaç, yöntem, özgün değer, yaygın etki gibi alanları TÜBİTAK mantığında kurmak istiyor
- Kullanıcı araştırma katkısı, iş paketi veya akademik çerçeve arıyor

Örnek kullanıcı istekleri:
- "Bu fikri TÜBİTAK projesine çevir"
- "TÜBİTAK için özgün değer yaz"
- "Bu proje akademik olarak nasıl güçlenir"
- "İş paketi mantığını kur"
- "TÜBİTAK başvurusu için nasıl yazmalıyım"

Not:
Burada odak akademik gerekçelendirme ve başvuru mantığıdır.

---

### 4. teknofest_ktr_ptr_guidance

Aşağıdaki durumlarda öncelikli skill budur:

- Kullanıcı TEKNOFEST için teknik rapor hazırlıyor
- Kullanıcı PTR veya KTR yazıyor
- Kullanıcı sistem mimarisi, performans hedefleri, test planı veya doğrulama kurgusu istiyor
- Kullanıcı jüriye teknik olarak güçlü görünmek istiyor
- Kullanıcı yarışma odaklı teknik anlatım istiyor

Örnek kullanıcı istekleri:
- "TEKNOFEST için PTR hazırlıyorum"
- "KTR'de sistem mimarisi nasıl yazılır"
- "Jüri için teknik kısmı güçlendirelim"
- "Test ve doğrulama planı hazırla"
- "TEKNOFEST rapor diliyle yaz"

Not:
Kullanıcı TEKNOFEST dese bile ihtiyacı sadece fikir bulmaksa önce `project_idea_refinement` seçilebilir.

---

### 5. feasibility_and_risk_check

Aşağıdaki durumlarda öncelikli skill budur:

- Kullanıcı projenin yapılabilirliğini sorguluyor
- Kullanıcı ekip, süre, veri, bütçe veya donanım açısından riskleri öğrenmek istiyor
- Kullanıcı projesini daha gerçekçi hale getirmek istiyor
- Kullanıcı risk analizi bölümü veya uygulanabilirlik değerlendirmesi istiyor

Örnek kullanıcı istekleri:
- "Bu proje yapılabilir mi"
- "Sence bu fazla zor mu"
- "Riskleri neler"
- "Öğrenci ekibi için mantıklı mı"
- "Veri yoksa bu proje yürür mü"

Not:
Bu skill'in amacı projeyi reddetmek değil, daha uygulanabilir hale getirmektir.

---

### 6. title_abstract_generator

Aşağıdaki durumlarda öncelikli skill budur:

- Kullanıcı proje başlığı istiyor
- Kullanıcı kısa özet istiyor
- Kullanıcı abstract istiyor
- Kullanıcı tanıtım metni veya başvuru özeti istiyor
- Kullanıcı aynı proje için alternatif başlıklar görmek istiyor

Örnek kullanıcı istekleri:
- "Bu projeye başlık ver"
- "Kısa özet yaz"
- "Abstract hazırla"
- "İngilizce abstract yazar mısın"
- "Başvuru özeti lazım"

Not:
Proje içeriği çok belirsizse önce fikir veya rapor netleştirme gerekebilir.

---

### 7. presentation_and_jury_preparation

Aşağıdaki durumlarda öncelikli skill budur:

- Kullanıcı sunum hazırlıyor
- Kullanıcı pitch metni istiyor
- Kullanıcı jüriye nasıl anlatacağını soruyor
- Kullanıcı demo akışı kurmak istiyor
- Kullanıcı olası jüri sorularına hazırlanmak istiyor

Örnek kullanıcı istekleri:
- "Sunum akışı hazırla"
- "Jüriye bunu nasıl anlatırım"
- "3 dakikalık pitch yaz"
- "Demo sırasında ne göstermeliyim"
- "Jürinin sorabileceği soruları çıkar"

Not:
Sunumdan önce proje içeriği çok belirsizse ilgili ana skill'e geri dönülmelidir.

## Çakışma Durumları

Bazı kullanıcı istekleri birden fazla skill ile ilişkili görünebilir. Bu durumda şu kurallar uygulanmalıdır:

### Fikir mi, rapor mu?
- Kullanıcı belirsiz konuşuyorsa → `project_idea_refinement`
- Kullanıcı belirli bölüm istiyorsa → `report_section_writer`

### TÜBİTAK mı, genel rapor mu?
- Kullanıcı akademik başvuru ve TÜBİTAK bağlamı kuruyorsa → `tubitak_application_guidance`
- Sadece belirli metin bölümü istiyorsa → `report_section_writer`

### TEKNOFEST mi, fikir netleştirme mi?
- Kullanıcı TEKNOFEST dese bile fikir henüz çok genişse → `project_idea_refinement`
- Kullanıcı teknik rapor, KTR, PTR, mimari veya test diyorsa → `teknofest_ktr_ptr_guidance`

### Risk mi, fikir netleştirme mi?
- Kullanıcı önce proje önerisi istiyorsa → `project_idea_refinement`
- Kullanıcı mevcut projenin gerçekçiliğini sorguluyorsa → `feasibility_and_risk_check`

### Başlık mı, proje netleştirme mi?
- Proje belli ise → `title_abstract_generator`
- Proje belli değilse → önce `project_idea_refinement`

### Sunum mu, rapor mu?
- Kullanıcı konuşma, pitch, demo, jüri sorusu istiyorsa → `presentation_and_jury_preparation`
- Kullanıcı yazılı teknik bölüm istiyorsa → ilgili rapor skill'i

## Çok Aşamalı Kullanım

Bazı durumlarda en doğru çözüm ardışık skill kullanımı olabilir.

Örnek akışlar:

### Akış 1
- Kullanıcı geniş proje fikri verir
- Önce: `project_idea_refinement`
- Sonra: `report_section_writer`

### Akış 2
- Kullanıcı TÜBİTAK için fikir getirir ama çok hamdır
- Önce: `project_idea_refinement`
- Sonra: `tubitak_application_guidance`

### Akış 3
- Kullanıcı TEKNOFEST projesinin risklerini sorar
- Önce: `feasibility_and_risk_check`
- Sonra gerekirse: `teknofest_ktr_ptr_guidance`

### Akış 4
- Kullanıcı proje netleştirdikten sonra başlık ister
- Önceki bilgi kullanılır
- Sonra: `title_abstract_generator`

### Akış 5
- Kullanıcı raporu yazdıktan sonra sunum ister
- Önceki proje çerçevesi korunur
- Sonra: `presentation_and_jury_preparation`

## Netleştirme Gerektiren Durumlar

Aşağıdaki durumlarda skill seçmeden önce kısa soru sorulabilir:

- Kullanıcı sadece "yardım et" diyorsa
- Kullanıcı sadece "proje için bir şey lazım" diyorsa
- Kullanıcı yazı mı fikir mi sunum mu istediğini belirtmiyorsa
- TEKNOFEST veya TÜBİTAK dediği halde tam ihtiyacını söylemiyorsa

Örnek kısa netleştirme:
- "Daha çok fikir mi netleştirmek istiyorsun, yoksa doğrudan rapor bölümü mü yazalım?"
- "Bunu TÜBİTAK başvuru mantığında mı, TEKNOFEST rapor mantığında mı ele alalım?"
- "Sana başlık mı lazım, özet mi, yoksa sunum akışı mı?"

## Son İlke

Amaç yalnızca etiket eşleştirmek değildir.  
Amaç, kullanıcının gerçek ihtiyacını bulup onu en uygun skill ile çözmektir.