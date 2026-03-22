---
title: "Agile/Scrum Temelleri: Profesyonel Yazılım Geliştirme Süreci"
estimated_minutes: 75
tags: ["agile", "scrum", "kanban", "sprint", "user-story", "jira", "project-management"]
prerequisites: []
---

# Agile/Scrum Temelleri: Profesyonel Yazılım Geliştirme Süreci

:::realworld
İş hayatında tek başına kod yazmak yetmez. Bir takımla birlikte, organize bir şekilde çalışman gerekir. Dünyada yazılım şirketlerinin %95'inden fazlası Agile metodoloji kullanıyor. İlk günden itibaren sprint planning, daily standup, retro gibi toplantılara katılacaksın. Bu kavramları bilmezsen takıma uyum sağlaman haftalar alır.

**Gerçek Dünya Örnekleri:**
- **Spotify:** "Squad" modeliyle çalışır. Her squad (5-8 kişi) kendi ürün alanına sahiptir. Squad'lar otonom çalışır, kendi sprint'lerini yönetir. Birden fazla squad aynı projede çalışıyorsa "Tribe" olarak koordine olur.
- **Amazon:** "Two Pizza Team" kuralı - bir takım iki pizza ile doyurulamıyorsa çok büyüktür. Küçük, otonom takımlar 2 haftalık sprint'lerle çalışır. Her takım kendi microservice'inden sorumludur.
- **Atlassian (Jira'nın yapımcısı):** Kendi ürünlerini Scrum ile geliştirirler. Sprint planning'de story point estimation yaparlar. Her sprint sonunda "Ship It Day" ile tamamlanan feature'ları deploy ederler.
- **Türk Startup Ekosistemi:** Trendyol, Getir, Hepsiburada gibi şirketler 2 haftalık sprint'ler kullanır. Daily standup'lar genelde sabah 10:00'da yapılır. JIRA veya Linear kullanılır. Junior developer olarak ilk gününden itibaren bu süreçlere katılırsın.
:::

## Neden Agile Öğrenmelisin?

Agile sadece bir "proje yönetim metodu" değildir. Yazılım geliştirme kültürüdür. Bu kültürü bilmezsen:

- İş mülakatlarında "Agile deneyimin var mı?" sorusuna cevap veremezsin
- Takıma katıldığında sprint, story point, velocity gibi terimleri anlamazsın
- Daily standup'ta ne söylemen gerektiğini bilemezsin
- Görev tahminlerinde sürekli yanılırsın

:::deha-tip
Deha seviyesi developer'lar teknik becerinin yanında süreç bilgisine de sahiptir. Bir feature'ı sadece kodlayabilmek yetmez - o feature'ın user story'sini yazabilmek, acceptance criteria'larını tanımlayabilmek, sprint planning'de doğru tahmin verebilmek ve retro'da yapıcı geri bildirim sunabilmek gerekir. Bu "soft skill"ler seni takımın en değerli üyesi yapar.
:::

:::senior-learns
Senior/CTO Agile'ı öğrenirken, Agile Manifesto'nun arkasındaki felsefeyi anlar. 2001'de 17 yazılımcı Utah'da buluşup bu manifestoyu yazdığında, Waterfall'ın katılığına karşı bir devrim başlattılar. Senior, Agile'ı dogma olarak değil, takımın ihtiyacına göre adapte eder. Bazı takımlarda Scrum iyi çalışır, bazılarında Kanban. "Agile olmak" kuralları takip etmek değil, değişime hızlı adapte olmaktır.
:::

## Agile Manifesto ve İlkeleri

:::concept[Agile Manifesto (İng: Agile Manifesto)]
Agile Manifesto, 2001 yılında 17 yazılım geliştiricisi tarafından yazılmış, yazılım geliştirme sürecinde neyin daha önemli olduğunu belirleyen temel ilkeler belgesidir.

**Türkçe karşılığı:** Çevik Yazılım Manifestosu
**Ne işe yarar:** Yazılım geliştirme sürecinde öncelikleri belirler
**Gerçek hayat benzetmesi:** Bir yemek tarifinin "tam bu malzemeleri kullan" yerine "taze malzeme kullan, tadına bakarak ayarla" demesi gibi - sonuca odaklan, süreci esnek tut
:::

:::code[text]{title="Agile Manifesto - 4 Temel Değer"}
Biz, yazılım geliştirmenin daha iyi yollarını ortaya çıkarıyoruz.
Bu süreçte şunlara daha fazla değer veriyoruz:

┌─────────────────────────────────────────────────────────┐
│ Bireyler ve etkileşimler    >  Süreçler ve araçlar      │
│ Çalışan yazılım             >  Kapsamlı dokümantasyon   │
│ Müşteri ile işbirliği       >  Sözleşme pazarlığı       │
│ Değişime yanıt vermek       >  Planı takip etmek        │
└─────────────────────────────────────────────────────────┘

NOT: Sağdakilerin de değerli olduğunu kabul etmekle birlikte,
     soldakileri daha değerli buluyoruz.
:::

:::code[text]{title="Agile'ın 12 İlkesi (Özet)"}
1.  En önemli öncelik, müşteriye sürekli ve erken değer sunmak
2.  Değişen gereksinimler geliştirme sürecinin sonunda bile karşılanabilir
3.  Çalışan yazılımı sık teslim et (haftalar, aylar değil)
4.  İş insanları ve geliştiriciler birlikte günlük çalışmalı
5.  Projeleri motive olmuş bireyler etrafında kur, onlara güven
6.  En verimli iletişim yüz yüze iletişimdir
7.  Çalışan yazılım, ilerlemenin temel ölçüsüdür
8.  Sürdürülebilir geliştirme hızını koru
9.  Teknik mükemmelliğe ve iyi tasarıma sürekli dikkat et
10. Sadelik - yapılmayan işin miktarını maximize et
11. En iyi tasarımlar, mimariler kendi kendini organize eden takımlardan çıkar
12. Düzenli aralıklarla takım nasıl daha etkili olabilir diye düşünür ve davranışını ayarlar
:::

:::warning
Agile Manifesto "dokümantasyon yazmayın" veya "plan yapmayın" demiyor! Soldaki değerlerin sağdakilerden **daha önemli** olduğunu söylüyor. Yani dokümantasyon yazacaksın ama çalışan yazılım her zaman öncelikli. Plan yapacaksın ama değişime açık olacaksın. Bu ayrımı anlamayan takımlar Agile'ı yanlış uygular.
:::

### Waterfall vs Agile

:::code[text]{title="Waterfall vs Agile Karşılaştırması"}
WATERFALL (Şelale Modeli):
Gereksinimler → Tasarım → Geliştirme → Test → Deploy → Bakım
     2 ay         1 ay      4 ay       2 ay   1 ay
     ════════════════════════════════════════════
     Toplam: 10 ay sonra ilk çalışan ürün
     Sorun: 10. ayda müşteri "Ben bunu istememiştim" derse?

AGILE (Çevik):
Sprint 1 (2 hafta): Temel özellik → Test → Deploy → Geri bildirim
Sprint 2 (2 hafta): Yeni özellik  → Test → Deploy → Geri bildirim
Sprint 3 (2 hafta): İyileştirme   → Test → Deploy → Geri bildirim
...
     ════════════════════════════════════════════
     İlk çalışan ürün: 2 hafta sonra!
     Her sprint'te müşteri geri bildirimi → Yanlış yöne gitmek imkansız

NEDEN AGILE KAZANDI?
- Waterfall'da 10 ay sonra "yanlış şeyi yaptık" riski var
- Agile'da her 2 haftada geri bildirim alırsın
- Değişen gereksinimlere anında uyum sağlarsın
- Müşteri sürekli görerek yönlendirir
:::

:::exercise
**Alıştırma 1: Agile vs Waterfall Senaryosu**

Bir e-ticaret sitesi geliştiriyorsun. Müşteri şu özellikleri istiyor:
- Ürün listeleme
- Arama
- Sepet
- Ödeme
- Kullanıcı hesabı
- Favoriler
- Kampanyalar

**Waterfall yaklaşımında:** Tüm özellikleri 6 ayda geliştirip teslim edersin. 6. ayda müşteri "Aslında favori özelliği değil, ürün karşılaştırma istiyordum" der. 3 hafta fazladan çalışırsın.

**Agile yaklaşımında:** Bu özellikleri sprint'lere nasıl bölersin? İlk 3 sprint'te hangi özellikleri yaparsın ve neden?

**Çözüm:**
- Sprint 1: Ürün listeleme + basit arama (MVP - kullanıcı ürünleri görebilsin)
- Sprint 2: Sepet + kullanıcı hesabı (alışveriş yapılabilsin)
- Sprint 3: Ödeme entegrasyonu (para akışı başlasın)
- Sonraki sprint'ler: Favoriler, kampanyalar, gelişmiş arama (geri bildirime göre önceliklendir)

**Neden bu sıra?** Çünkü her sprint sonunda "çalışan bir ürün" olmalı. Sprint 1 sonunda kullanıcı ürünleri görebilir, Sprint 2 sonunda sepete ekleyebilir, Sprint 3 sonunda satın alabilir. Müşteri her sprint'te geri bildirim verir.
:::

## Scrum Framework

:::concept[Scrum (İng: Scrum)]
Scrum, Agile'ın en yaygın framework'üdür. Sabit süreli iterasyonlar (sprint'ler) halinde çalışarak düzenli aralıklarla çalışan yazılım teslim etmeyi hedefler.

**Türkçe karşılığı:** Scrum (çeviri yok, terim olarak kullanılır)
**Ne işe yarar:** Yazılım geliştirme sürecini düzenli, ölçülebilir ve öngörülebilir hale getirir
**Gerçek hayat benzetmesi:** Maraton yerine 100 metre sprint'ler koşmak gibi - her sprint'te tam güçle koş, sonra değerlendir ve tekrarla
:::

### Scrum Roller

:::code[text]{title="Scrum Takımındaki 3 Rol"}
1. PRODUCT OWNER (PO) - Ürün Sahibi
   ─────────────────────────────────
   Kim: Ürünün ne olması gerektiğine karar veren kişi
   Görevleri:
   - Product Backlog'u oluşturur ve önceliklendirir
   - User story'leri yazar
   - Acceptance criteria belirler
   - Sprint sonunda "done" mı değil mi karar verir
   - Stakeholder'larla iletişim kurar

   Benzetme: Restoranın sahibi - menüyü (backlog) belirler,
             müşteri isteklerini (requirements) toplar

2. SCRUM MASTER (SM)
   ─────────────────
   Kim: Scrum sürecinin doğru uygulanmasını sağlayan kişi
   Görevleri:
   - Sprint seremonilerini kolaylaştırır (facilitate)
   - Takımın önündeki engelleri kaldırır (impediment removal)
   - Scrum kurallarının uygulanmasını sağlar
   - Takımı korur (dışarıdan gelen baskılara karşı)
   - Sürekli iyileştirme kültürü oluşturur

   Benzetme: Antrenör - maçı oynamaz ama takımı en iyi
             performansa hazırlar, sorunları çözer

3. DEVELOPMENT TEAM - Geliştirme Takımı
   ─────────────────────────────────────
   Kim: Ürünü geliştiren 3-9 kişilik çapraz fonksiyonlu takım
   Kimler var:
   - Frontend developer (SEN!)
   - Backend developer
   - QA engineer (tester)
   - UI/UX designer (bazen)
   - DevOps engineer (bazen)
   Görevleri:
   - Sprint'teki işleri tamamlar
   - Tahmin (estimation) yapar
   - Kendi aralarında organize olur
   - Kaliteden sorumludur

   Benzetme: Mutfaktaki aşçılar - yemeği (ürünü) birlikte pişirirler,
             her biri kendi uzmanlık alanında çalışır
:::

### Sprint ve Sprint Seremonileri

:::concept[Sprint (İng: Sprint)]
Sprint, Scrum'da sabit süreli (genelde 2 hafta) geliştirme döngüsüdür. Her sprint sonunda potansiyel olarak yayınlanabilir bir ürün artışı (increment) teslim edilir.

**Türkçe karşılığı:** Sprint (çeviri yok)
**Ne işe yarar:** Büyük projeleri küçük, yönetilebilir parçalara böler
**Gerçek hayat benzetmesi:** Okuldaki sınav dönemleri gibi - 2 haftada belirli konuları bitir, sınav ol (demo), sonuçları değerlendir (retro), sonraki döneme hazırlan
:::

:::code[text]{title="Sprint Döngüsü"}
Sprint Döngüsü (2 Haftalık Tipik Sprint):

PAZARTESI (Sprint Başlangıcı)
┌─────────────────────────────────────────────────────┐
│  Sprint Planning (2-4 saat)                         │
│  - Product Owner backlog'daki önemli item'ları sunar│
│  - Takım hangi item'ları bu sprint'e alacağına      │
│    karar verir                                      │
│  - Her item için "nasıl yapacağız?" konuşulur       │
│  - Sprint Goal belirlenir                           │
└─────────────────────────────────────────────────────┘

HER GÜN (Pazartesi-Cuma)
┌─────────────────────────────────────────────────────┐
│  Daily Standup (15 dakika, ayakta)                  │
│  Her kişi 3 soruyu yanıtlar:                       │
│  1. Dün ne yaptım?                                 │
│  2. Bugün ne yapacağım?                             │
│  3. Önümde bir engel var mı?                        │
└─────────────────────────────────────────────────────┘

CUMA (Sprint Sonu)
┌─────────────────────────────────────────────────────┐
│  Sprint Review / Demo (1-2 saat)                    │
│  - Tamamlanan işler stakeholder'lara gösterilir     │
│  - Geri bildirim alınır                             │
│  - "Bitti" kabul edilen item'lar belirlenir         │
│                                                     │
│  Sprint Retrospective (1-1.5 saat)                  │
│  - Ne iyi gitti?                                    │
│  - Ne kötü gitti?                                   │
│  - Nasıl iyileştirebiliriz?                         │
│  - Action item'lar belirlenir                       │
└─────────────────────────────────────────────────────┘
:::

:::must-note
**MUTLAKA NOT AL:** Daily Standup'ta uzun uzun anlatma. Her kişi maximum 2 dakika konuşmalı. "Dün login API'yi bitirdim, bugün dashboard'a başlayacağım, engelim yok" gibi kısa ve öz. Detaylı tartışmalar standup'tan sonra yapılır ("parking lot" denir). Standup'ta oturmak yasak - ayakta durmak toplantıyı kısa tutar.
:::

:::exercise
**Alıştırma 2: Daily Standup Simülasyonu**

Sen bir frontend developer'sın. Bir e-ticaret projesinde çalışıyorsun. Şu durumdasın:
- Dün ürün detay sayfasının responsive tasarımını bitirdin
- Bugün sepet sayfasına başlayacaksın
- API'den gelen ürün verisi eksik alanlar içeriyor (fotoğraf URL'si bazen null geliyor)

Daily standup'ta ne söylersin? 2 dakikada bitecek şekilde yaz.

**Çözüm:**
"Merhaba. Dün ürün detay sayfasının responsive tasarımını tamamladım, mobil ve tablet görünümleri hazır. Code review'a açtım. Bugün sepet sayfasının UI implementasyonuna başlayacağım. Bir engelim var: API'den gelen ürün verisinde fotoğraf URL'si bazen null geliyor, bu yüzden fallback image logic'i eklemem gerekiyor. Backend takımıyla bu konuyu konuşmam lazım."

**Neden bu format?**
- Kısa ve öz (30 saniye)
- 3 soruyu da yanıtladı (dün/bugün/engel)
- Engeli net tanımladı ve çözüm önerdi
- Detaya girmedi (API sorununun detayı standup sonrası konuşulur)
:::

### Product Backlog ve Sprint Backlog

:::code[text]{title="Backlog Yapısı"}
PRODUCT BACKLOG (Ürün İş Listesi)
═══════════════════════════════════
Product Owner tarafından yönetilir.
Tüm yapılacak işlerin önceliklendirilmiş listesi.

Öncelik  │ User Story                          │ Story Point
─────────┼─────────────────────────────────────┼────────────
  P1     │ Kullanıcı giriş yapabilmeli         │     5
  P1     │ Ürün listesi görüntülenebilmeli     │     8
  P2     │ Ürün arama yapılabilmeli            │     5
  P2     │ Sepete ürün eklenebilmeli           │     8
  P3     │ Ödeme yapılabilmeli                 │    13
  P3     │ Sipariş takibi yapılabilmeli        │     8
  P4     │ Favorilere ekleme yapılabilmeli     │     3
  P5     │ Ürün yorumu yazılabilmeli           │     5
  ...    │ ...                                 │    ...

SPRINT BACKLOG (Sprint İş Listesi)
════════════════════════════════════
Bu sprint'te yapılacak seçilmiş işler:

Sprint 3 Goal: "Kullanıcılar ürün arayıp sepete ekleyebilmeli"

┌──────────────────────────────────────────────────────┐
│ User Story: Ürün arama yapılabilmeli (5 SP)          │
│ Tasks:                                               │
│ ☑ Search input component'i oluştur        (2 saat)  │
│ ☑ Search API endpoint'i implement et      (4 saat)  │
│ ☐ Arama sonuçları listesini göster        (3 saat)  │
│ ☐ Debounce ekle (300ms)                   (1 saat)  │
│ ☐ No results state'i ekle                 (1 saat)  │
├──────────────────────────────────────────────────────┤
│ User Story: Sepete ürün eklenebilmeli (8 SP)         │
│ Tasks:                                               │
│ ☐ Cart context/store oluştur              (3 saat)  │
│ ☐ "Sepete Ekle" butonu implement et       (2 saat)  │
│ ☐ Cart badge (sepet sayacı) ekle          (1 saat)  │
│ ☐ Cart page layout'u oluştur              (4 saat)  │
│ ☐ Miktar artır/azalt fonksiyonu           (2 saat)  │
│ ☐ Sepetten ürün silme                     (1 saat)  │
│ ☐ Cart API entegrasyonu                   (3 saat)  │
└──────────────────────────────────────────────────────┘
:::

## User Story ve Acceptance Criteria

:::concept[User Story (İng: User Story)]
User story, bir özelliğin kullanıcı perspektifinden yazılmış kısa açıklamasıdır. Kim, ne istiyor ve neden istediğini tanımlar.

**Türkçe karşılığı:** Kullanıcı Hikayesi
**Ne işe yarar:** Teknik gereksinimleri kullanıcı ihtiyacına bağlar
**Gerçek hayat benzetmesi:** Restoranda "Garson, ben aç olduğum için sıcak bir çorba istiyorum" demek gibi - kim (ben), ne (çorba), neden (açım)
:::

:::code[text]{title="User Story Formatı"}
TEMPLATE:
"[Bir kullanıcı/rol] olarak,
 [bir şey] yapabilmek istiyorum,
 böylece [bir fayda] elde edebilirim."

İngilizce: "As a [role], I want [feature], so that [benefit]."

ÖRNEKLER:

✅ İYİ USER STORY:
"Bir müşteri olarak,
 ürünleri fiyata göre sıralayabilmek istiyorum,
 böylece bütçeme uygun ürünleri kolayca bulabilirim."

✅ İYİ USER STORY:
"Bir yönetici olarak,
 günlük satış raporunu dashboard'da görmek istiyorum,
 böylece iş performansını hızlıca değerlendirebilirim."

❌ KÖTÜ USER STORY:
"Sıralama özelliği eklenecek."
→ Kim için? Neden? Ne tür sıralama? Belirsiz.

❌ KÖTÜ USER STORY:
"Kullanıcı, ürünleri fiyat, isim, tarih, kategori, renk,
 marka, stok durumu ve popülerliğe göre sıralayabilmeli,
 ayrıca çoklu sıralama da yapabilmeli."
→ Çok büyük! Birden fazla story'ye bölünmeli.
:::

:::code[text]{title="Acceptance Criteria (Kabul Kriterleri)"}
User Story: "Bir müşteri olarak, ürünleri sepete ekleyebilmek
istiyorum, böylece toplu alışveriş yapabilirim."

ACCEPTANCE CRITERIA (Given-When-Then formatı):

AC1: Ürün sepete eklenebilmeli
  Given: Kullanıcı ürün detay sayfasında
  When:  "Sepete Ekle" butonuna tıklar
  Then:  Ürün sepete eklenir ve sepet sayacı güncellenir

AC2: Aynı üründen birden fazla eklenebilmeli
  Given: Sepette zaten 1 adet ürün var
  When:  Aynı ürünü tekrar sepete ekler
  Then:  Mevcut ürünün miktarı 2'ye çıkar (yeni satır eklenmez)

AC3: Stokta yoksa eklenmemeli
  Given: Ürünün stok durumu 0
  When:  "Sepete Ekle" butonuna tıklar
  Then:  "Stokta yok" mesajı gösterilir, ürün eklenmez

AC4: Sepet badge'i güncellenmeli
  Given: Sepette 3 farklı ürün var
  When:  Yeni bir ürün eklenir
  Then:  Navbar'daki sepet ikonunda "4" rakamı görünür

AC5: Giriş yapmayan kullanıcı da ekleyebilmeli
  Given: Kullanıcı giriş yapmamış
  When:  "Sepete Ekle" butonuna tıklar
  Then:  Ürün localStorage'da tutulur, giriş yapınca senkronize edilir
:::

:::must-note
**MUTLAKA NOT AL:** Acceptance criteria, bir story'nin "bitti" sayılması için karşılanması gereken koşullardır. Developer olarak AC'leri okumadan koda başlama! AC'ler sana tam olarak neyi implement etmen gerektiğini söyler. Eksik AC varsa Product Owner'a sor. "Benim anladığım doğru mu?" diye onaylat. Yanlış anlamayla yazılan kod = boşa harcanan sprint.
:::

:::exercise
**Alıştırma 3: User Story Yazma**

Aşağıdaki özellikler için user story ve en az 3 acceptance criteria yaz:

1. **Şifre sıfırlama:** Kullanıcı şifresini unuttuğunda email ile sıfırlayabilmeli.
2. **Ürün yorumu:** Kullanıcılar satın aldıkları ürünlere yorum ve yıldız puanı verebilmeli.

**Çözüm:**

**1. Şifre Sıfırlama:**
User Story: "Bir kullanıcı olarak, şifremi unuttığımda email ile sıfırlayabilmek istiyorum, böylece hesabıma tekrar erişebilirim."

AC1: Given: Giriş sayfasında. When: "Şifremi Unuttum" linkine tıklar. Then: Email giriş formu gösterilir.
AC2: Given: Email formuna kayıtlı email girildi. When: "Gönder" butonuna tıklar. Then: Sıfırlama linki email'e gönderilir ve bilgi mesajı gösterilir.
AC3: Given: Geçerli sıfırlama linkine tıklandı. When: Yeni şifre girilir. Then: Şifre güncellenir ve giriş sayfasına yönlendirilir.
AC4: Given: Sıfırlama linki 24 saatten eski. When: Linke tıklanır. Then: "Link süresi dolmuş" mesajı gösterilir.

**2. Ürün Yorumu:**
User Story: "Bir müşteri olarak, satın aldığım ürünlere yorum ve puan verebilmek istiyorum, böylece diğer kullanıcıların doğru karar vermesine yardımcı olabilirim."

AC1: Given: Ürünü satın almış kullanıcı. When: Ürün sayfasında "Yorum Yaz" butonuna tıklar. Then: Yorum formu açılır (1-5 yıldız + metin alanı).
AC2: Given: Ürünü satın almamış kullanıcı. When: "Yorum Yaz" butonuna tıklar. Then: "Bu ürünü satın almanız gerekiyor" mesajı gösterilir.
AC3: Given: Yorum formu dolu. When: Gönder butonuna tıklar. Then: Yorum ürün sayfasında görünür, ortalama puan güncellenir.
:::

## Estimation: Tahmin Yöntemleri

:::concept[Story Points (İng: Story Points)]
Story points, bir user story'nin karmaşıklığını, eforunu ve riskini ölçen soyut bir birimdir. Saat veya gün değil, göreli zorluk ifade eder.

**Türkçe karşılığı:** Hikaye Puanı
**Ne işe yarar:** İşlerin ne kadar zor olduğunu takım olarak tahmin eder
**Gerçek hayat benzetmesi:** Dağ tırmanışı zorluk dereceleri gibi - Kolay (1-2), Orta (3-5), Zor (8-13). Bir dağın zorluğu süre değil karmaşıklıkla ölçülür.
:::

:::code[text]{title="Fibonacci Story Points"}
FIBONACCI SERİSİ: 1, 2, 3, 5, 8, 13, 21

Neden Fibonacci? Büyük işlerdeki belirsizliği yansıtır.
5 ile 8 arasında büyük fark yok, ama 13 ile 21 arasında çok var.

REFERANS TABLO:

1 SP  → Çok basit, kesin bilinen iş
        Örnek: Buton rengini değiştir, typo düzelt

2 SP  → Basit, az efor
        Örnek: Yeni bir input field ekle, validasyon ekle

3 SP  → Orta zorlukta, bilinen pattern
        Örnek: Yeni bir CRUD form oluştur, API endpoint ekle

5 SP  → Orta-üstü, birden fazla component etkileniyor
        Örnek: Arama özelliği ekle (frontend + backend)

8 SP  → Karmaşık, araştırma gerekebilir
        Örnek: Ödeme entegrasyonu, file upload sistemi

13 SP → Çok karmaşık, belirsizlik yüksek
        Örnek: Real-time notification sistemi, OAuth entegrasyonu

21 SP → Epik seviyesinde, BÖLÜNMELI!
        Örnek: Bu tek story değil, birden fazla story'ye ayrılmalı
:::

:::code[text]{title="Planning Poker Süreci"}
PLANNING POKER (Sprint Planning'de kullanılır):

1. Product Owner story'yi okur ve açıklar
2. Takım soruları sorar (AC'ler netleşir)
3. Herkes aynı anda kartını gösterir:

   Ali: 5    Ayşe: 8    Mehmet: 5    Zeynep: 13

4. En düşük ve en yüksek tahmin eden açıklar:
   - Ali (5): "Daha önce benzer bir şey yaptık,
              arama component'i hazır, sadece API bağlayacağız"
   - Zeynep (13): "Ama fuzzy search isteniyor,
                   Elasticsearch entegrasyonu gerekebilir"

5. Tartışma sonrası tekrar oy:
   Ali: 8    Ayşe: 8    Mehmet: 8    Zeynep: 8

6. Konsensüs: 8 Story Point

T-SHIRT SIZING (Hızlı tahmin için):
XS = 1 SP    → Önemsiz değişiklik
S  = 2-3 SP  → Küçük iş
M  = 5 SP    → Orta iş
L  = 8 SP    → Büyük iş
XL = 13+ SP  → Çok büyük, bölünmeli
:::

:::beginner-mistake
Yaygın hata: Story point'leri saate çevirmek. "5 story point = 2 gün" diye düşünmek yanlış. Story point'ler göreceli karmaşıklığı ölçer. Aynı 5 SP'lik iş bir junior'a 3 gün, senior'a 1 gün sürebilir. Ama her ikisi de "bu 5 SP'lik bir iş" der çünkü karmaşıklığı aynı. Takımın velocity'si zamanla ne kadar SP yapabildiğini gösterir.
:::

:::exercise
**Alıştırma 4: Story Point Tahmini**

Aşağıdaki user story'lere story point ver (Fibonacci: 1, 2, 3, 5, 8, 13). Nedenini açıkla.

1. "Login formu için 'Beni Hatırla' checkbox'ı ekle"
2. "Kullanıcı profil fotoğrafı yükleyebilmeli (crop, resize dahil)"
3. "Ürün listesi sayfasına infinite scroll ekle"
4. "Footer'daki telif hakkı yılını 2025'ten 2026'ya güncelle"
5. "Google ile giriş (OAuth 2.0) entegrasyonu"

**Çözüm:**
1. **2 SP** - Checkbox ekle, localStorage'a kaydet, sayfa yüklendiğinde kontrol et. Basit, bilinen pattern.
2. **8 SP** - File upload, image crop (third-party library), resize, S3/cloud storage entegrasyonu, preview. Birden fazla component ve backend değişikliği.
3. **5 SP** - Intersection Observer API veya library, pagination API, loading state, scroll position yönetimi. Orta karmaşıklıkta.
4. **1 SP** - Tek satır değişiklik, risk yok.
5. **13 SP** - OAuth flow, Google Console konfigürasyonu, token yönetimi, mevcut auth sistemiyle entegrasyon, edge case'ler (hesap birleştirme). Yüksek karmaşıklık ve belirsizlik.
:::

## Sprint Velocity ve Burndown Chart

:::concept[Velocity (İng: Velocity)]
Velocity, bir takımın bir sprint'te tamamladığı toplam story point sayısıdır. Gelecek sprint'lerin planlanmasında referans olarak kullanılır.

**Türkçe karşılığı:** Hız / Takım Hızı
**Ne işe yarar:** Takımın ne kadar iş yapabildiğini ölçer ve gelecek sprint'leri planlamada kullanılır
**Gerçek hayat benzetmesi:** Bir koşucunun ortalama tempo'su gibi - son 5 koşuda km başına 5 dakika sürdüyse, sonraki koşuda da benzer tempo beklenir
:::

:::code[text]{title="Velocity Hesaplama"}
VELOCITY TARİHÇESİ:

Sprint 1:  Planlanan: 30 SP  │  Tamamlanan: 24 SP  │  Velocity: 24
Sprint 2:  Planlanan: 28 SP  │  Tamamlanan: 28 SP  │  Velocity: 28
Sprint 3:  Planlanan: 30 SP  │  Tamamlanan: 26 SP  │  Velocity: 26
Sprint 4:  Planlanan: 28 SP  │  Tamamlanan: 30 SP  │  Velocity: 30
Sprint 5:  Planlanan: 30 SP  │  Tamamlanan: 27 SP  │  Velocity: 27

Ortalama Velocity: (24 + 28 + 26 + 30 + 27) / 5 = 27 SP/Sprint

Sprint 6 için planlama: ~27 SP civarında iş al
(Çok fazla alırsan bitiremezsin, az alırsan boş kalırsın)
:::

:::code[text]{title="Burndown Chart"}
BURNDOWN CHART: Sprint'teki kalan iş miktarını gösterir

Story Points
  30 │ ■
     │ ■ ·
  25 │   ■ ·
     │   ■   ·
  20 │     ■   ·
     │       ■   ·
  15 │       ■     ·
     │         ■     ·
  10 │           ■     ·
     │             ■     ·
   5 │               ■     ·
     │                 ■     ·
   0 │─────────────────────■──·──
     └────┬────┬────┬────┬────┬──
      Pzt  Sal  Çar  Per  Cum
          (Sprint günleri)

■ = Gerçek ilerleme
· = İdeal çizgi (eşit tempo)

YORUMLAMA:
- Çizgi idealin altında → Sprint'te arkada kalıyoruz (acil aksiyon)
- Çizgi idealin üstünde → İyi gidiyoruz (fazla iş alabiliriz)
- Düz çizgi (plateau) → Bir şey tıkanmış (blocker var)
- Son gün ani düşüş → İşler son gün tamamlanıyor (kötü işaret)
:::

:::exercise
**Alıştırma 5: Velocity Analizi**

Bir takımın son 5 sprint'teki velocity'si: 20, 25, 22, 18, 25

1. Ortalama velocity nedir?
2. Sprint 6'da kaç SP'lik iş planlanmalı?
3. Product Backlog'da toplam 200 SP kaldı. Yaklaşık kaç sprint sürecek?
4. Sprint 4'te velocity neden düşmüş olabilir?

**Çözüm:**
1. (20 + 25 + 22 + 18 + 25) / 5 = **22 SP**
2. **20-22 SP** arası (ortalamaya yakın, biraz konservatif)
3. 200 / 22 = **yaklaşık 9 sprint** (18 hafta / 4.5 ay)
4. Olası nedenler:
   - Takımdan biri izindeydi
   - Teknik borç / altyapı çalışması yapıldı
   - Beklenmeyen production bug'ları çıktı
   - Sprint'teki story'ler tahmin edilenden karmaşık çıktı
   - Dış bağımlılık (başka takım, 3rd party API) gecikti
:::

## Kanban

:::concept[Kanban (İng: Kanban)]
Kanban, işleri görsel bir tahta üzerinde sütunlarla takip eden, sprint'siz çalışan bir Agile yöntemidir. İşler sürekli akış halinde ilerler.

**Türkçe karşılığı:** Kanban (Japonca, "sinyal kartı" anlamında)
**Ne işe yarar:** İşlerin durumunu görselleştirir, darboğazları tespit eder
**Gerçek hayat benzetmesi:** Restoran mutfağı - siparişler gelir, hazırlanır, servis edilir. Aynı anda kaç sipariş hazırlanabileceğinin limiti vardır (WIP limit)
:::

:::code[text]{title="Kanban Board"}
KANBAN TAHTASI:

┌────────────┬────────────┬────────────┬────────────┬────────────┐
│  BACKLOG   │    TODO    │IN PROGRESS │  REVIEW    │    DONE    │
│            │  (Limit:5) │  (Limit:3) │  (Limit:2) │            │
├────────────┼────────────┼────────────┼────────────┼────────────┤
│ ┌────────┐ │ ┌────────┐ │ ┌────────┐ │ ┌────────┐ │ ┌────────┐ │
│ │Search  │ │ │Payment │ │ │Cart    │ │ │Login   │ │ │Signup  │ │
│ │Filter  │ │ │Page    │ │ │Page    │ │ │Form    │ │ │Flow    │ │
│ └────────┘ │ └────────┘ │ │(Ali)   │ │ │(Zeynep)│ │ └────────┘ │
│ ┌────────┐ │ ┌────────┐ │ └────────┘ │ └────────┘ │ ┌────────┐ │
│ │Wishlist│ │ │Profile │ │ ┌────────┐ │            │ │Product │ │
│ │Feature │ │ │Page    │ │ │User    │ │            │ │List    │ │
│ └────────┘ │ └────────┘ │ │API     │ │            │ └────────┘ │
│ ┌────────┐ │ ┌────────┐ │ │(Mehmet)│ │            │            │
│ │Reviews │ │ │Order   │ │ └────────┘ │            │            │
│ │System  │ │ │History │ │            │            │            │
│ └────────┘ │ └────────┘ │            │            │            │
│ ...        │            │            │            │            │
└────────────┴────────────┴────────────┴────────────┴────────────┘

WIP (Work In Progress) LİMİTİ:
- In Progress sütununda maximum 3 iş olabilir
- Limit doluysa yeni iş başlayamaz → Önce mevcut işi bitir
- Bu, multitasking'i önler ve kaliteyi artırır
:::

:::code[text]{title="Scrum vs Kanban"}
┌──────────────────┬──────────────────────┬──────────────────────┐
│ Özellik          │ SCRUM                │ KANBAN               │
├──────────────────┼──────────────────────┼──────────────────────┤
│ Zaman kutusu     │ Sprint (2 hafta)     │ Yok (sürekli akış)   │
│ Roller           │ PO, SM, Dev Team     │ Zorunlu rol yok       │
│ Seremoniler      │ Planning, Daily,     │ Zorunlu seremoni yok  │
│                  │ Review, Retro        │ (isteğe bağlı)       │
│ Tahmin           │ Story Points         │ Genelde yok           │
│ İş limiti        │ Sprint kapasitesi    │ WIP limit (sütun)     │
│ Değişiklik       │ Sprint içinde olmaz  │ Her an olabilir       │
│ Board sıfırlama  │ Her sprint başında   │ Hiç sıfırlanmaz       │
│ Metrikler        │ Velocity             │ Lead time, Cycle time │
│ Ne zaman kullan  │ Ürün geliştirme,     │ Destek, bakım,        │
│                  │ yeni özellikler      │ sürekli deployment    │
└──────────────────┴──────────────────────┴──────────────────────┘

PRATİKTE: Çoğu takım ikisinin karışımını kullanır ("Scrumban")
- Sprint'ler var ama WIP limit de var
- Daily standup var ama strict tahmin yok
:::

:::exercise
**Alıştırma 6: Kanban Board Tasarla**

Bir teknik destek takımı için Kanban board tasarla. Sütunlar, WIP limitleri ve örnek kartlar oluştur.

**Çözüm:**
```
Sütunlar ve WIP limitleri:
1. Incoming (yeni gelen talepler) - Limitsiz
2. Triage (önceliklendirme) - WIP: 5
3. In Progress (çalışılıyor) - WIP: 3
4. Waiting on Customer (müşteri yanıtı bekleniyor) - WIP: 5
5. Testing (test ediliyor) - WIP: 2
6. Resolved (çözüldü) - Limitsiz

Örnek kartlar:
- [Urgent] Ödeme sayfası 500 hatası veriyor → In Progress
- [High] Kullanıcı profil fotoğrafı yüklenmiyor → Triage
- [Medium] Dashboard grafikleri yavaş yükleniyor → Waiting on Customer
- [Low] Footer'daki link kırık → Incoming
```
:::

## JIRA / Linear Kullanımı

:::code[text]{title="JIRA Workflow (Tipik)"}
JIRA ISSUE TİPLERİ:

🏔 EPIC: Büyük özellik grubu (ör: "Kullanıcı Yönetimi")
  │
  ├── 📋 STORY: Kullanıcı perspektifinden özellik
  │     │       (ör: "Kullanıcı giriş yapabilmeli")
  │     │
  │     ├── ✅ TASK: Teknik iş parçası
  │     │         (ör: "Login form component'i oluştur")
  │     │
  │     └── ✅ TASK: Teknik iş parçası
  │               (ör: "Auth API endpoint'i implement et")
  │
  ├── 📋 STORY: Başka bir özellik
  │
  └── 🐛 BUG: Hata raporu
              (ör: "Login'de şifre alanı boş gönderiliyor")

JIRA WORKFLOW:
  Open → In Progress → In Review → QA → Done

JIRA BOARD GÖRÜNÜMLERİ:
- Board View: Kanban tahtası
- Backlog View: Tüm story'lerin listesi
- Timeline View: Gantt chart benzeri zaman çizelgesi
- Reports: Velocity chart, burndown chart, sprint report

LINEAR (Modern Alternatif):
- Daha hızlı ve minimalist arayüz
- Keyboard shortcuts ile hızlı navigasyon
- GitHub entegrasyonu (PR → issue bağlama)
- Cycle'lar (sprint benzeri)
- Startup'lar ve modern takımlar tarafından tercih edilir
:::

:::code[text]{title="Tipik Developer JIRA Workflow'u"}
GÜNLÜK JIRA KULLANIMI (Developer olarak):

1. SABAH (Sprint Board'a bak):
   - Hangi task'lar "In Progress"ta?
   - Bugün hangi task'a devam edeceğim?
   - Yeni atanan task var mı?

2. İŞE BAŞLARKEN:
   - Task'ı "In Progress"a taşı
   - Branch oluştur: feature/PROJ-123-login-form
   - (PROJ-123 = JIRA ticket numarası)

3. İŞ YAPARKEN:
   - Task'a comment ekle (ilerleme notu)
   - Blocker varsa JIRA'da belirt
   - Subtask'ları tamamla

4. İŞ BİTİNCE:
   - PR aç, commit mesajında ticket numarası olsun:
     "feat(auth): implement login form [PROJ-123]"
   - Task'ı "In Review"a taşı
   - Reviewer ata

5. CODE REVIEW SONRASI:
   - Değişiklik istendiyse düzelt
   - Approve alınca merge et
   - Task'ı "QA"ya taşı (veya "Done")

PR → JIRA BAĞLANTISI:
- Commit mesajında PROJ-123 yazarsan
- JIRA otomatik olarak PR'ı ticket'a bağlar
- PR merge olunca ticket otomatik "Done"a geçer (opsiyonel)
:::

:::exercise
**Alıştırma 7: JIRA Ticket Yazma**

Aşağıdaki senaryo için bir JIRA ticket (story + acceptance criteria + subtask'lar) oluştur:

**Senaryo:** Ürün listesi sayfasına "Yeniden Sırala" (sort) özelliği eklenmesi gerekiyor. Kullanıcı fiyata göre artan/azalan ve isme göre A-Z/Z-A sıralayabilmeli.

**Çözüm:**

**STORY: PROJ-456 - Ürün Sıralama Özelliği**
Type: Story
Priority: Medium
Sprint: Sprint 7
Story Points: 5

Description:
"Bir müşteri olarak, ürün listesini fiyata ve isme göre sıralayabilmek istiyorum, böylece aradığım ürünü daha hızlı bulabilirim."

Acceptance Criteria:
- AC1: Ürün listesinin üstünde "Sırala" dropdown'ı görünür
- AC2: Sıralama seçenekleri: Fiyat (Artan), Fiyat (Azalan), İsim (A-Z), İsim (Z-A)
- AC3: Seçim yapıldığında liste anında güncellenir
- AC4: Sayfa yenilendiğinde sıralama tercihi korunur (URL query param)
- AC5: Mobilde de dropdown düzgün görünür

Subtasks:
- [ ] PROJ-457: Sort dropdown component'i oluştur (2 saat)
- [ ] PROJ-458: Backend sort API parametresi ekle (2 saat)
- [ ] PROJ-459: Frontend sort state yönetimi + API entegrasyonu (3 saat)
- [ ] PROJ-460: URL query parameter senkronizasyonu (1 saat)
- [ ] PROJ-461: Unit test'ler yaz (2 saat)
:::

## Retrospective (Retro)

:::code[text]{title="Sprint Retrospective Formatları"}
1. START-STOP-CONTINUE

   🟢 START (Yapmaya başlayalım):
   - Pair programming yapalım
   - PR template kullanalım
   - Sprint başında technical spike yapalım

   🔴 STOP (Yapmayı bırakalım):
   - Sprint ortasında scope eklemeyi bırakalım
   - Code review'sız merge etmeyi bırakalım
   - Meeting'lerde laptop açmayı bırakalım

   🟡 CONTINUE (Devam edelim):
   - Daily standup'ları 15 dakikada bitirmeye devam
   - Sprint demo'larını kaydetmeye devam
   - Tech debt'i her sprint'e eklemeye devam

2. GLAD-SAD-MAD

   😊 GLAD (Mutlu olduğumuz):
   - Sprint goal'ünü tuturduk
   - Yeni CI/CD pipeline harika çalışıyor
   - Takıma yeni katılan arkadaş hızla adapte oldu

   😢 SAD (Üzüldüğümüz):
   - 3 bug production'a kaçtı
   - Bir story tahmin ettiğimizin 2 katı sürdü
   - Design'lar geç geldi, geliştirme gecikti

   😡 MAD (Kızdığımız):
   - Sprint ortasında 2 yeni story eklendi
   - Code review'lar 3 gün bekliyor
   - Staging ortamı sürekli çöküyor

3. 4L's (Liked, Learned, Lacked, Longed For)

   ❤️ Liked: Pair programming session'ları
   📚 Learned: React Query caching stratejisi
   ⚠️ Lacked: QA ortamı yoktu, manual test ettik
   🌟 Longed For: Otomatik E2E testler
:::

:::exercise
**Alıştırma 8: Retro Senaryosu**

Sprint 5 bitti. Şu durumlar yaşandı:
- 5 story'den 4'ü tamamlandı, 1'i yarım kaldı
- Production'da 1 critical bug çıktı, 1 gün düzeltilmesi sürdü
- Yeni takım arkadaşı (junior) ilk sprint'ini tamamladı
- Backend API değişti, frontend'de 2 gün ekstra çalışma oldu
- Code review'lar ortalama 4 saat içinde tamamlandı

Start-Stop-Continue formatında retro notları yaz.

**Çözüm:**

🟢 START:
- API değişikliklerini önceden haber veren bir contract/document oluşturalım
- Critical bug'lar için hotfix süreci tanımlayalım (direk fix + deploy)
- Junior developer için buddy/mentor sistemi kuralım

🔴 STOP:
- Sprint ortasında backend API'yi kıran değişiklikler yapmayı bırakalım
- Story'leri yeterli AC olmadan sprint'e almayı bırakalım (yarım kalan story bundan kaynaklı olabilir)

🟡 CONTINUE:
- 4 saat içinde code review tamamlamaya devam (harika tempo)
- Junior developer'a sabırlı ve destekleyici yaklaşmaya devam
- Sprint goal odaklı çalışmaya devam (4/5 story iyi bir oran)
:::

## Developer'ın Scrum'daki Rolü

:::code[text]{title="Sprint Planning'de Developer Ne Yapar?"}
SPRINT PLANNING'DE SENİN GÖREVLERİN:

1. SORU SOR (En önemli görevin):
   - "Bu story'de kullanıcı login olmadan da yapabilecek mi?"
   - "Mobil tasarım var mı, yoksa sadece desktop mı?"
   - "Edge case: 0 ürün olunca ne göstereceğiz?"
   - "Bu API endpoint zaten var mı, yoksa backend de mi yapacak?"

2. TEKNİK FEASIBILITY DEĞERLENDİR:
   - "Bu story mevcut altyapıyla yapılabilir"
   - "Bu story için önce X kütüphanesini kurmamız lazım"
   - "Bu story aslında 2 ayrı story olmalı çünkü bağımsız deploy edilebilir"

3. TAHMİN VER (Planning Poker):
   - Karmaşıklığı değerlendir, saat değil story point ver
   - Emin değilsen yüksek ver, düşük tahmin risklidir
   - "Bu daha önce yaptığımız X'e benziyor, o 5'ti, bu da 5"

4. TASK'LARA BÖL:
   - Story'yi teknik subtask'lara ayır
   - Her subtask'a saat tahmini ver
   - Bağımlılıkları belirle ("Önce API olmalı, sonra frontend")

5. KAPASİTENİ BİLDİR:
   - "Bu sprint'te 2 gün izindeyim"
   - "Önceki sprint'ten carry-over 1 story var"
   - "Bu sprint'te tech debt çalışması da yapmam lazım"
:::

:::exercise
**Alıştırma 9: Sprint Planning Simülasyonu**

Product Owner şu story'yi sundu:

**Story:** "Bir kullanıcı olarak, sipariş geçmişimi görmek istiyorum, böylece önceki alışverişlerimi takip edebilirim."

Sen frontend developer'sın. Şu soruları cevapla:

1. Product Owner'a hangi soruları sorarsın? (En az 5 soru)
2. Bu story'ye kaç story point verirsin? Neden?
3. Hangi subtask'lara bölersin?

**Çözüm:**

1. **Sorular:**
   - Siparişler listesinde hangi bilgiler görünecek? (tarih, tutar, ürünler, durum?)
   - Sipariş detayına tıklayınca ne göreceğiz? (ayrı sayfa mı, modal mı?)
   - Pagination olacak mı? Kaç sipariş gösterilecek?
   - Filtreleme var mı? (tarihe göre, duruma göre)
   - Sipariş durumları neler? (Hazırlanıyor, Kargoda, Teslim Edildi, İptal)
   - Mobil tasarım var mı?

2. **Story Point: 8**
   Neden: API entegrasyonu, liste sayfası, detay sayfası, pagination, responsive tasarım. Birden fazla component ve sayfa gerekiyor.

3. **Subtask'lar:**
   - [ ] Sipariş listesi sayfası layout + UI (3 saat)
   - [ ] Sipariş listesi API entegrasyonu + loading state (2 saat)
   - [ ] Pagination component'i (2 saat)
   - [ ] Sipariş detay sayfası/modal (3 saat)
   - [ ] Sipariş durumu badge component'i (1 saat)
   - [ ] Responsive tasarım (2 saat)
   - [ ] Unit testler (2 saat)
:::

:::exercise
**Alıştırma 10: Sprint Review Demo**

Sprint 5'te şu story'leri tamamladın:
1. Ürün arama özelliği (frontend + backend)
2. Sepet sayfa tasarımı (responsive)

Sprint Review'da bu işleri stakeholder'lara (CEO, ürün müdürü, pazarlama) nasıl demo yaparsın? Demo senaryonu yaz.

**Çözüm:**

"Merhaba, bu sprint'te iki özellik tamamladık. Göstereyim:

**Demo 1 - Ürün Arama (2 dakika):**
1. Ana sayfayı açıyorum. Üstte arama çubuğunu görüyorsunuz.
2. 'laptop' yazıyorum - yazdıkça otomatik sonuçlar geliyor (debounce ile 300ms gecikme var, gereksiz API çağrısı yapılmıyor).
3. Enter'a basıyorum - arama sonuçları sayfası açılıyor.
4. Sonuç yoksa 'Sonuç bulunamadı' mesajı ve popüler ürünler öneriliyor.
5. Mobilde de göstereyim - arama ikonu var, tıklayınca tam ekran arama açılıyor.

**Demo 2 - Sepet Sayfası (2 dakika):**
1. Birkaç ürün sepete ekliyorum - navbar'daki badge güncelleniyor.
2. Sepet sayfasını açıyorum - ürünler, miktarlar ve toplam tutar görünüyor.
3. Miktar artır/azalt butonlarıyla miktarı değiştiriyorum - toplam anında güncelleniyor.
4. Ürünü siliyorum - silme animasyonu ile kaldırılıyor.
5. Mobil görünümü göstereyim - kartlar dikey diziliyor, butonlar büyük ve tıklanabilir.

Sorularınız var mı?"
:::

:::exercise
**Alıştırma 11: Blocker Yönetimi**

Bir story üzerinde çalışıyorsun ama takıldın. Backend takımının API'si henüz hazır değil ve sen frontend'i bitiremedin. Bu durumda ne yaparsın?

**Çözüm:**

1. **Daily Standup'ta bildir:** "Backend API henüz hazır değil, bu story block oldu."
2. **JIRA'da blocker flag ekle:** Story'nin status'ünü "Blocked" yap, neden açıklamasını yaz.
3. **Scrum Master'ı bilgilendir:** Backend takımıyla koordinasyonu sağlamasını iste.
4. **Boş durma, başka iş al:**
   - Mock data ile frontend'i tamamla (API gelince bağlarsın)
   - Sprint backlog'dan başka bir story al
   - Tech debt veya test yazma işi yap
5. **Backend ile anlaş:** API contract'ı (request/response formatı) üzerinde anlaş. Interface'i biliyorsan mock ile çalışabilirsin.
6. **Sprint Review'da bildir:** "Bu story block oldu, sebebi X, çözüm olarak mock ile frontend'i tamamladım, API gelince entegre edeceğiz."
:::

:::exercise
**Alıştırma 12: Tam Sprint Simülasyonu**

2 haftalık bir sprint planla. Takımın:
- 2 frontend developer (sen + Ali)
- 1 backend developer (Mehmet)
- 1 QA (Zeynep)
- Velocity: 30 SP

Product Backlog'dan seçilebilecek story'ler:
1. Kullanıcı profil sayfası (8 SP)
2. Ürün filtreleme (fiyat aralığı, kategori) (13 SP)
3. Sipariş onay emaili (5 SP)
4. Dashboard grafikler (8 SP)
5. Password reset flow (5 SP)
6. Ürün detay sayfası redesign (3 SP)
7. Admin kullanıcı listesi (8 SP)

Hangi story'leri bu sprint'e alırsın? Sprint goal ne olur?

**Çözüm:**

**Sprint Goal:** "Kullanıcı hesap yönetimi ve ürün keşfini iyileştirmek"

**Alınan story'ler (toplam: 29 SP):**
1. Kullanıcı profil sayfası (8 SP) - Sprint goal ile uyumlu
2. Ürün filtreleme (13 SP) - Sprint goal ile uyumlu, yüksek iş değeri
3. Password reset flow (5 SP) - Sprint goal ile uyumlu (hesap yönetimi)
4. Ürün detay sayfası redesign (3 SP) - Küçük, sprint goal ile uyumlu

**Neden bu seçim?**
- 29 SP, velocity'ye (30) uygun
- Story'ler birbiriyle ilişkili (hesap yönetimi teması)
- Mix: büyük (13), orta (8, 5), küçük (3) - risk dağılımı iyi
- 13 SP'lik story riskli ama sprint'in ana hedefi

**Alınmayan story'ler:**
- Sipariş onay emaili: Sprint goal dışı, sonraki sprint
- Dashboard grafikler: Sprint goal dışı
- Admin kullanıcı listesi: Sprint goal dışı
:::

## Interview Soruları

:::interview
**Soru 1:** Agile ve Scrum arasındaki fark nedir?
**Cevap:** Agile bir yazılım geliştirme felsefesi ve değerler bütünüdür (Agile Manifesto). Scrum ise bu felsefeyi uygulayan somut bir framework'tür. Agile "ne yapalım" der, Scrum "nasıl yapalım" der. Scrum dışında Kanban, XP, Lean gibi başka Agile framework'ler de vardır. Bir takım Agile olabilir ama Scrum kullanmayabilir.

**Soru 2:** Sprint planning'de ne yaparsın?
**Cevap:** Product Owner'ın sunduğu story'leri dinlerim, netleştirici sorular sorarım (edge case'ler, tasarım, API bağımlılıkları). Planning poker ile story point tahmini veririm. Alınan story'leri teknik subtask'lara bölerim. Kapasitemi bildiririm (izin, carry-over vb.). Sprint goal'ünün gerçekçi olduğundan emin olurum.

**Soru 3:** Daily standup'ta ne söylersin?
**Cevap:** 3 soruyu yanıtlarım: Dün ne yaptım, bugün ne yapacağım, engelim var mı. Maximum 2 dakikada bitiririm. Detaylı teknik tartışmaları standup sonrasına bırakırım. Eğer bir blocker varsa net olarak belirtirim ve yardım isterim.

**Soru 4:** Story point nedir? Neden saat yerine story point kullanılır?
**Cevap:** Story point, bir işin karmaşıklığını, eforunu ve riskini ölçen soyut bir birimdir. Saat yerine kullanılır çünkü: aynı iş farklı kişilere farklı sürede sürer ama karmaşıklığı aynıdır, zaman tahmini psikolojik baskı yaratır, story point'ler zamanla tutarlı hale gelir (velocity). Fibonacci serisi kullanılır çünkü büyük işlerdeki belirsizliği yansıtır.

**Soru 5:** Bir sprint'te görev yarım kalırsa ne olur?
**Cevap:** Yarım kalan story bir sonraki sprint'e carry-over edilir. Sprint review'da neden tamamlanamadığı açıklanır. Retro'da kök neden analizi yapılır. Eğer story çok büyükse bölünmesi düşünülür. Velocity hesaplamasında sadece tamamlanan story'ler sayılır, yarım kalan sayılmaz. Bu, gelecek sprint planlamasında daha gerçekçi kapasiteyle çalışmamızı sağlar.
:::

:::ai-guidance
**AI ile Agile Pratiği:**

1. **User Story Yazma:** AI'ya bir özellik anlat ve "Bunu user story formatında yaz" de. AC'leri de yazdır. AI'nın yazdığı AC'leri eleştir ve iyileştir.

2. **Sprint Planning Simülasyonu:** AI'dan "Product Owner rolü oyna ve bana 5 user story sun" de. Sen takım olarak soru sor, tahmin ver, story'leri sprint'e al.

3. **Retro Pratiği:** AI'ya bir sprint senaryosu anlat ve "Bu sprint için retro yap" de. Start-Stop-Continue formatında tartış.

4. **Estimation Pratiği:** AI'dan rastgele feature'lar iste ve story point tahmini yap. AI'nın değerlendirmesiyle karşılaştır.

5. **JIRA Ticket Yazma:** AI'ya eksik yazılmış bir JIRA ticket göster ve "Bu ticket'ı nasıl iyileştiririm?" diye sor.
:::

:::senior-learns
Senior/CTO Agile'da "metriklerin kötüye kullanımını" bilir. Velocity bir **planlama aracıdır**, performans değerlendirme aracı DEĞİLDİR. Takımın velocity'sini artırmak için story point'leri şişirmek (point inflation), gerçekte done olmayan story'leri done saymak (fake velocity) gibi anti-pattern'ler takımı yok eder. Doğru metrikler: customer satisfaction, deployment frequency, lead time for changes, mean time to recovery (DORA metrics).
:::

## Özet ve Yol Haritası

Bu derste Agile ve Scrum'ın temellerini öğrendin:

1. **Agile Manifesto** - 4 değer, 12 ilke, Waterfall'dan farkı
2. **Scrum Rolleri** - Product Owner, Scrum Master, Development Team
3. **Sprint Döngüsü** - Planning, Daily Standup, Review, Retrospective
4. **User Story** - Format, acceptance criteria, Given-When-Then
5. **Estimation** - Story points, Fibonacci, Planning Poker, T-shirt sizing
6. **Velocity & Burndown** - Takım hızı ölçümü, ilerleme takibi
7. **Kanban** - Board, WIP limit, sürekli akış
8. **JIRA/Linear** - Ticket tipleri, workflow, developer kullanımı
9. **Retrospective** - Start-Stop-Continue, Glad-Sad-Mad, 4L's
10. **Developer'ın Rolü** - Sprint'teki görevler, blocker yönetimi

İlk işine başladığında bu kavramları bilmek seni diğer junior'lardan ayırır. Takım arkadaşların "Bu adam/kadın Scrum biliyor, ilk günden katkı sağlıyor" diyecek. Bu, iş mülakatlarında da büyük avantaj: "Agile deneyimin var mı?" sorusuna güvenle "Evet, sprint planning yapabilir, user story yazabilir, tahmin verebilirim" diyebilirsin.
