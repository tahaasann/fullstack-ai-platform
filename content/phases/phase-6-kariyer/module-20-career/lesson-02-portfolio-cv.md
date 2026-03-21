---
title: "Portfolio, CV ve Kariyer Stratejisi"
id: mod-20-career/lesson-02
estimated_minutes: 90
order: 2
tags: [portfolio, cv, resume, github, linkedin, career, job-search, freelancing, networking]
prerequisites: [mod-20-career/lesson-01]
---

# Portfolio, CV ve Kariyer Stratejisi

Teknik beceriler önemli ama onlari doğru şekilde sunabilmek de en az o kadar önemli. Bu derste GitHub portfolio'ndan CV yazimina, LinkedIn'den freelancing'e kadar kariyer stratejinin her alanini ogreneceksin.

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Bir yazılım muhendisi portfolyosunda projeler nasil sunulmali? STAR formati ile proje aciklamasi yazmayi, teknik karar sürecini anlatmayi ve metrikleri (performans iyilestirmesi, kullanıcı sayisi) kullanarak etki gostermeyi açıkla. GitHub profili, kisisel web sitesi ve LinkedIn arasindaki sinerjiyi anlat."

**2. Pratik Uygulama:**
> "CV'mi incele ve iyilestir: [CV icerigini yapistir]. ATS (Applicant Tracking System) uyumlu formata dönüştür, eylem fiilleri (implemented, designed, optimized) kullan, ölçülebilir basarilar (reduced load time by 40%) ekle ve gereksiz bilgileri çıkar. Turkiye ve global is piyasasi için iki farklı versiyon oluştur."
> Takip: "Şimdi LinkedIn profilimi optimize et: headline, about section, experience bolumu ve skill endorsement stratejisi için öneriler ver. Recruiter'larin arama algoritmasinda üst siralarda cikmak için anahtar kelime stratejisi oluştur."

**3. Mukemmellik Için:**
> "Is arama stratejisi oluştur: portfolio projesi secimi (3-4 showcase proje), GitHub contribution stratejisi (açık kaynak katılım), blog yazma plani (teknik içerik), networking stratejisi (tech meetup'lar, Twitter/X), cold outreach template'leri ve freelancing ile gelir oluşturma. 90 gunluk aksiyon plani yap."

### Pair Programming Ipucu
Portfolio projesi gelistirirken AI'a proje fikrini anlat ve sor: "Bu proje bir is basvurusunda etkileyici olur mu? Hangi teknolojileri kullanmaliyim? README nasil yazilmali? Live demo ve kod kalitesi acisindan nelere dikkat etmeliyim?"
:::

:::interview
## Mülakat Sorulari

**Soru 1: Portfolyonuzdaki en etkileyici projenizi anlatir misiniz?**
- **Junior cevabi:** Todo app yaptim, React ve Node.js kullandım, CRUD işlemleri var.
- **Senior cevabi:** Bir projeyi anlatirken STAR+teknik derinlik: "E-ticaret platformu gelistirdim (Situation). Performans sorunlari vardi (Task). Redis caching, CDN, lazy loading ve code splitting uygulayarak (Action) sayfa yuklenme suresini 4.2s'den 1.1s'ye dusurdum, Lighthouse skoru 45'ten 92'ye çıktı (Result)." Proje anlatiminda: mimari kararlarinizi NEDEN aldiginizi (trade-off analizi), karsilastiginiz zorluklar ve cozumlerinizi, ölçülebilir metrikleri ve projenin gerçek bir sorunu nasil cozdugunun anlatilmasi gerekir. README'de arsitektut diyagrami, kurulum talimatlari ve live demo linki olmali.

**Soru 2: Teknik CV'de en sik yapılan hatalar nelerdir?**
- **Junior cevabi:** Çok uzun yazmak, gereksiz bilgi eklemek.
- **Senior cevabi:** En büyük hatalar: 1) Teknoloji listesi yazmak ama ne yaptiginizi gostermemek ("React kullandım" yerine "React ile 50K MAU'lu dashboard gelistirdim, render suresini %60 azalttim"), 2) ATS uyumsuz format (tablolar, kolonlar, grafikler ATS'i kirar), 3) Tek CV ile her yere basvurmak (her pozisyon için keyword'leri job description'dan alinarak customize edilmeli), 4) Kisisel projeler yazmamak (is deneyimi yoksa 3-5 kaliteli proje is deneyimi yerine geçer), 5) GitHub linkini vermemek veya bos GitHub profili. CV tek sayfa olmali, eylem fiilleri ile baslamali (designed, implemented, optimized, reduced, increased).
:::

:::must-note
DEFTERINE YAZ - Kariyer Kritik Noktalar:
1. **GitHub = Dijital CV'n**: Her gun commit at (yesil kare grafigi bos olmasin), README'leri ozenle yaz, 3-5 vitrin projesi ol
2. **ATS-friendly CV**: Tek sayfa, basit format (tablo/kolon yok), keyword'leri job posting'den al, PDF olarak gönder
3. **LinkedIn Optimizasyonu**: Headline'da "Full Stack Developer | React | Node.js | Python" yaz, "Open to Work" ac, haftada 2-3 post at
4. **Is arama stratejisi**: %60 networking + %30 direkt basvuru + %10 recruiter = en etkili kombinasyon
5. **Sürekli öğrenme**: Bootcamp bitmesi ogrenmenin bitmesi değil - her gun 1 saat coding, haftada 1 blog yazisi, ayda 1 side project
:::

:::senior-learns
**Senior/CTO Bu Konuyu Nasil Öğrenir?**

Senior muhendisler kariyerlerini **şirket içinde değil, industri içinde** konumlandirir:
- GitHub'da sadece kod değil, **dokümantasyon kalitesi** ile one cikarlar
- CV'lerini **impact bazli** yazarlar: "React kullandım" değil "React ile checkout flow'u yeniden yazarak conversion'i %15 artirdim"
- LinkedIn'de **thought leadership** yaparlar - teknik yazilar, deneyim paylasimi
- **Network'leri** en büyük varliklaridir - konferanslara katilir, meetup'lara giderler
- Her projeyi bir **öğrenme firsati** olarak gorurler

**Yaklaşım**: Kendin bir urun gibi düşün. Portfolio = showroom, CV = brosur, LinkedIn = reklam kanali.
:::

---

## 1. GitHub Portfolio Stratejisi

:::concept
### GitHub Profilin = Dijital Vitrin

Recruiter'lar ve hiring manager'lar ilk GitHub profilinie bakar.

**Ideal GitHub Profili:**

```
┌─────────────────────────────────────────────┐
│  Taha Arslan                                │
│  Full Stack Developer | AI Enthusiast       │
│                                             │
│  📍 Istanbul, Turkey                        │
│  🔗 portfolio-site.com                      │
│  📧 taha@email.com                          │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │ Contribution Graph                    │   │
│  │ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ │   │
│  │ ██ ░░ ██ ░░ ██ ██ ██ ░░ ██ ██ ██ ██ │   │
│  │ ██ ██ ██ ██ ██ ░░ ██ ██ ██ ░░ ██ ██ │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  Pinned Repositories:                       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │ Project1│ │ Project2│ │ Project3│       │
│  │ ⭐ 45   │ │ ⭐ 23   │ │ ⭐ 12   │      │
│  └─────────┘ └─────────┘ └─────────┘      │
└─────────────────────────────────────────────┘
```
:::

:::tip
### GitHub'da One Cikma Taktikleri

**1. Profil README'si oluştur:**
```markdown
# Merhaba, ben Taha! 👋

Full Stack Developer olarak React, Node.js ve Python ile
web uygulamalari gelistiriyorum.

## 🛠 Tech Stack
- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, Python, FastAPI
- **Database**: PostgreSQL, MongoDB, Redis
- **DevOps**: Docker, AWS, GitHub Actions

## 📊 GitHub Stats
[GitHub stats widget ekle]

## 📫 Iletisim
- LinkedIn: [link]
- Portfolio: [link]
```

**2. Pinned repo'lari secerken:**
- En iyi 3-6 projeni pin'le
- Farkli teknolojileri goster (frontend + backend + fullstack)
- Star ve fork sayisi yüksek olanlari one al

**3. Contribution graph'i yesil tut:**
- Her gun en az 1 commit
- Küçük de olsa gunluk coding aliskanligi
- Open source contributon'lar da sayilir

**4. Her projede profesyonel README:**
- Proje ne yapıyor? (1-2 cumle)
- Screenshot/demo GIF
- Teknolojiler listesi
- Kurulum adimlari
- Canli demo linki
:::

:::code
### Mukemmel README Sablonu

```markdown
# 🚀 ProjeAdi

Kisa aciklama - bu proje ne yapiyor ve neden onemli.

![Demo](./screenshots/demo.gif)

## ✨ Ozellikler

- [x] Kullanici kayit ve giris (JWT authentication)
- [x] Gercek zamanli bildirimler (WebSocket)
- [x] Responsive tasarim (mobile-first)
- [x] Dark mode destegi
- [ ] Payment entegrasyonu (devam ediyor)

## 🛠 Teknolojiler

| Alan | Teknoloji |
|------|-----------|
| Frontend | React 19, TypeScript, Tailwind CSS |
| Backend | Node.js, Express, Prisma ORM |
| Database | PostgreSQL, Redis |
| DevOps | Docker, GitHub Actions, AWS |

## 🚀 Baslangic

### Gereksinimler
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Kurulum

    git clone https://github.com/username/proje.git
    cd proje
    pnpm install
    cp .env.example .env  # Environment degiskenlerini ayarla
    pnpm run dev

## 📁 Proje Yapisi

    src/
    ├── components/     # React componentleri
    ├── pages/          # Sayfa componentleri
    ├── hooks/          # Custom React hooks
    ├── services/       # API servisleri
    ├── utils/          # Yardimci fonksiyonlar
    └── types/          # TypeScript tipleri

## 🤝 Katki

Katkilariniz memnuniyetle karsilanir!
1. Fork edin
2. Feature branch olusturun
3. PR gonderin

## 📝 Lisans

MIT License
```
:::

:::concept
### Vitrin Projeleri - Ne Olusturmali?

3-5 proje yeterli ama **kaliteli** olmali:

| Proje | Gosterdigi Beceri | Teknolojiler |
|-------|-------------------|--------------|
| Full-stack e-ticaret | CRUD, auth, payment | React + Node + PostgreSQL |
| Real-time chat | WebSocket, scaling | Next.js + Socket.io + Redis |
| AI-powered app | API integration, ML | Python + FastAPI + OpenAI |
| CLI tool / package | Problem solving, DX | Node.js/Python, npm/PyPI |
| Open source contribution | Collaboration | Herhangi bir populer proje |

**Her projede olmasi gerekenler:**
- Canli demo (Vercel, Netlify, Railway)
- Temiz kod + test'ler
- CI/CD pipeline
- Profesyonel README
- Responsive design
:::

---

## 2. ATS-Friendly CV Yazimi

:::concept
### ATS Nedir?

**ATS (Applicant Tracking System)** = Şirketlerin basvurulari filtrelemek için kullandigi yazılım.

```
CV Gonderildi
     │
     ▼
┌──────────────┐
│ ATS Sistemi  │ ← Keyword taramasi yapar
│              │ ← Formatlamayi parse eder
│              │ ← Puana gore siralar
└──────────────┘
     │
     ├── Yuksek Puan → HR'a iletilir
     │
     └── Dusuk Puan → Reddedilir (insan gormeden!)

Istatistik: CV'lerin %75'i bir insan tarafindan gorulmeden
            ATS tarafindan elenirr.
```

**ATS-Friendly Olmak Için:**
- Basit format (fancy design YAPMA)
- Tablo, kolon, grafik KULLANMA
- Keyword'leri job posting'den al
- PDF olarak gönder (Word değil)
- Standard basliklar kullan (Experience, Education, Skills)
:::

:::realworld
### CV Şablonu - Full Stack Developer

```
====================================
TAHA ARSLAN
Full Stack Developer
====================================

Istanbul, Turkey | taha@email.com | github.com/taha
linkedin.com/in/taha | portfolio.com

------------------------------------
SUMMARY
------------------------------------
Full Stack Developer with experience in React, Node.js,
and Python. Built and deployed 5+ web applications with
focus on performance and user experience. Passionate about
clean code and continuous learning.

------------------------------------
TECHNICAL SKILLS
------------------------------------
Languages:     JavaScript, TypeScript, Python, SQL
Frontend:      React, Next.js, Tailwind CSS, Redux
Backend:       Node.js, Express, FastAPI, REST API, GraphQL
Database:      PostgreSQL, MongoDB, Redis
DevOps:        Docker, GitHub Actions, AWS (EC2, S3, RDS)
Tools:         Git, VS Code, Postman, Figma

------------------------------------
PROJECTS
------------------------------------

E-Commerce Platform | React, Node.js, PostgreSQL
github.com/taha/ecommerce | demo: ecommerce.vercel.app
- Developed a full-stack e-commerce platform with JWT
  authentication, product catalog, and Stripe payment
- Implemented Redis caching reducing API response time
  by 60% (from 500ms to 200ms)
- Wrote 85+ unit and integration tests with Jest
- Deployed on AWS using Docker containers and CI/CD

Real-Time Chat Application | Next.js, Socket.io, Redis
github.com/taha/chat-app | demo: chat.vercel.app
- Built a real-time messaging app supporting 1000+
  concurrent users with WebSocket
- Designed message persistence with MongoDB and
  Redis pub/sub for multi-server scaling
- Achieved 99.5% uptime over 3 months of production use

AI Content Generator | Python, FastAPI, React
github.com/taha/ai-content | demo: ai-content.vercel.app
- Created an AI-powered content generation tool using
  OpenAI API with streaming responses
- Implemented rate limiting (token bucket) handling
  500+ daily active users
- Reduced API costs by 40% through prompt optimization
  and response caching

------------------------------------
EDUCATION
------------------------------------
B.S. Computer Engineering
Karadeniz Technical University (KTU), 2020

------------------------------------
CERTIFICATIONS & ACTIVITIES
------------------------------------
- AWS Cloud Practitioner (2026)
- Open source contributor: [proje adi] (5 PRs merged)
- Technical blog: blog.taha.dev (20+ articles)
```
:::

:::warning
### CV Hatalari

**FORMAT HATALARI:**
- 2+ sayfa CV (tek sayfa yeterli, max 2)
- Fancy grafik/tablo/kolon tasarım (ATS okuyamaz)
- Fotograf ekleme (Turkiye'de yaygin ama uluslararasi'da ekleme)
- Word dosyasi gönderme (PDF gondeer)

**Içerik HATALARI:**
- "Responsible for..." kullanma → "Developed...", "Implemented...", "Improved..." kullan
- Teknoloji listesi ama proje yok (ne yaptiigini göster)
- Kisisel bilgiler (dogum tarihi, medeni durum, askerlik - uluslararasi'da ekleme)
- Hedef yerine özet yok ("Objective: To find a good job" YAZMA)

**STRATEJIK HATALAR:**
- Ayni CV'yi her yere gönderme → Her basvuru için customize et
- Keyword uyumsuzlugu → Job posting'deki terimleri kullan
- Rakam vermemek → "Improved performance" değil "Reduced load time by 60%"
:::

:::tip
### CV'de Power Words

```
Teknik Eylemler:        Impact Gosterme:
- Developed             - Reduced ... by X%
- Implemented           - Improved ... by X%
- Designed              - Increased ... by X%
- Architected           - Served X users
- Built                 - Processed X requests/second
- Deployed              - Achieved X% uptime
- Optimized             - Saved X hours/week
- Automated             - Decreased ... by X%
- Integrated            - Grew ... from X to Y
- Migrated              - Handled X concurrent users

YANLIS: "I was responsible for the frontend"
DOGRU:  "Developed React frontend serving 10K daily users,
         reducing page load time from 4s to 1.2s"
```
:::

---

## 3. LinkedIn Optimizasyonu

:::concept
### LinkedIn = Profesyonel Sosyal Medya

LinkedIn'de aktif olmak is bulma sansini **3x** arttirir.

**Profile Optimization Checklist:**

```
[ ] Profesyonel fotograf (yuz gorunen, temiz arka plan)
[ ] Banner image (tech temalı veya kendi tasarimin)
[ ] Headline: "Full Stack Developer | React | Node.js | Python"
    (sadece "Looking for job" YAZMA)
[ ] About section: 3-5 paragraf, teknik + kisisel
[ ] Experience: Her proje icin bullet points
[ ] Skills: En az 10 skill ekle, endorsement iste
[ ] Recommendations: 2-3 kişiden referans al
[ ] Featured: Portfolio, blog yazilari, projeler
[ ] "Open to Work" badge'i AC (recruiters only veya public)
[ ] Custom URL: linkedin.com/in/taha-arslan
```
:::

:::tip
### LinkedIn Içerik Stratejisi

**Haftada 2-3 post at:**

```
Pazartesi: Teknik ogrenme paylaşimi
"Bu hafta Redis caching'i derinlemesine ogrendim.
En onemli 3 takeaway:
1. Cache-aside pattern cogu use case icin en iyisi
2. TTL her zaman belirle - stale data tehlikeli
3. Thundering herd problemi icin mutex lock kullan
#Redis #Caching #WebDevelopment"

Carsamba: Proje update'i
"Side project'imi yayinladim! 🚀
AI-powered blog ozetleyici:
- React + FastAPI + OpenAI API
- Streaming responses ile gercek zamanli
- Demo: [link]
- GitHub: [link]
Ne dusunuyorsunuz? Feedbackleriniz hos gelir!
#React #Python #AI #SideProject"

Cuma: Dusunce/deneyim paylasimi
"Junior developer olarak en cok yaptigim 3 hata
ve nasil duzelttigim:
1. Her seyi ezberlemeyee calisiyordum → Pattern ogrenmeye gectim
2. Dokumantasyon okumuyordum → Artik ilk is docs okumak
3. Yardim istemekten cekiniyordum → Artik 30 dk takilinca soruyorum
Siz hangi hatalari yaptiniz? 👇
#JuniorDeveloper #LearningToCode #TechCareer"
```

**Engagement artirmak için:**
- Baskalarinin postlarina yorum yap (sadece "harika" değil, degerli yorum)
- Turkiye'deki tech community'lerle etkilesime gec
- Hashtag kullan ama abartma (3-5 hashtag yeterli)
- Recruiterlara InMail gondermekten cekinme
:::

---

## 4. Cover Letter (On Yazi)

:::code
### Cover Letter Şablonu

```text
Subject: Application for Full Stack Developer - [Sirket Adi]

Sayin Hiring Team,

[Sirket Adi]'ndaki Full Stack Developer pozisyonu icin
basvuruyorum. [Sirketin ne yaptigini bil ve neden ilgini
cektigini acikla - 1-2 cumle].

Son [X] yildir React, Node.js ve Python ile web uygulamalari
gelistiriyorum. En son projemde [spesifik proje + sonuc].
Ornegin, [proje adi]'nda Redis caching implementasyonu ile
API response suresini %60 azalttim.

Pozisyon gereksinimlerindeki [spesifik teknoloji/beceri]
konusunda deneyimim var. [Kisa ornek ver]. Ayrica [sirketin
deger verdigi bir sey]'e olan tutkunum, bu pozisyonu benim
icin ideal kiliyor.

Portfolyomu [link] adresinde ve GitHub profilimi
[github.com/username] adresinde inceleyebilirsiniz.

Mulakat firsati icin sizi sabırsizlikla bekliyorum.

Saygilarimla,
[Ad Soyad]
[Telefon] | [Email]
[LinkedIn] | [Portfolio]
```
:::

:::warning
### Cover Letter Hatalari

- **Generic göndermek**: Her sirkete ayni yazi → Sirkete ozel yaz
- **CV'yi tekrarlamak**: Cover letter ≠ CV ozeti → Motivasyonunu anlat
- **Çok uzun yazmak**: Max 250-300 kelime → Kısa ve oz
- **"Dear Sir/Madam"**: Mumkunse isim bul → LinkedIn'den hiring manager'i ara
- **Turkce/Ingilizce karışık**: Tutarli ol → Pozisyon diline gore yaz
:::

---

## 5. Is Arama Stratejisi

:::concept
### Çok Kanalli Is Arama

```
Is Arama Kanallari (etkililik sirasina gore):

1. NETWORKING (%60 etkili)
   ├── LinkedIn baglantilari
   ├── Meetup'lar ve konferanslar
   ├── Universite alumni aglari
   ├── Discord/Slack communityleri
   └── Referral (tavsiye) programlari

2. DIREKT BASVURU (%30 etkili)
   ├── Sirket kariyer sayfalari
   ├── LinkedIn Jobs
   ├── Indeed / Glassdoor
   ├── Kariyer.net / Yenibiris.com (Turkiye)
   └── AngelList / Wellfound (startup)

3. RECRUITER (%10 etkili)
   ├── LinkedIn recruiter mesajlari
   ├── Headhunter ajanslari
   └── Tech recruiting platformlari

GunlMk Hedef: 5-10 basvuru/gun + 3-5 networking mesaji/gun
```
:::

:::realworld
### Turkiye ve Uluslararasi Pazar

**Turkiye'de Is Arama:**

| Platform | Tür | Ipucu |
|----------|-----|-------|
| LinkedIn | Her tür | Turkce + Ingilizce profil |
| Kariyer.net | Büyük şirketler | ATS-friendly CV yükle |
| Kommunity | Startup'lar | Turkiye startup ekosistemi |
| TopTal Turkiye | Freelance | Test-based giriş |
| Turkcell, Trendyol, Getir | Büyük tech | Kariyer sayfalarindan |

**Uluslararasi Remote Is:**

| Platform | Tür | Ipucu |
|----------|-----|-------|
| LinkedIn | Her tür | "Remote" filtresi kullan |
| RemoteOK | Remote-only | Startup agirlikli |
| We Work Remotely | Remote-only | Kaliteli şirketler |
| Turing | Remote | Test + interview |
| Toptal | Freelance/Contract | Elit, zor giriş |
| Upwork | Freelance | Portfolyo ile başla |

**Remote is için avantajlar:**
- USD/EUR maas = Turkiye'de yüksek yasam standardi
- Global deneyim
- Esnek çalışma saatleri

**Remote is için zorluklar:**
- Zaman farki (US = gece calismak gerekebilir)
- Iletişim tamamen Ingilizce
- Kendi disiplinini yönetmek
- Sosyal izolasyon riski
:::

:::tip
### Networking Stratejisi

```
1. LINKEDIN NETWORKING
   - Hedef: Haftada 20 yeni baglanti
   - Baglanti istegine kisisel not ekle:
     "Merhaba [isim], ben de [teknoloji] ile calisan
      bir developer'im. Projelerinizi begendim,
      baglanmak ister misiniz?"
   - Baglanti kabul edilince tesekkur mesaji gonder

2. COMMUNITY KATILIMI
   - Discord: Reactiflux, Python, TypeScript
   - Slack: DevTr, Istanbul Coders
   - Meetup: Istanbul Tech Talks, Ankara Dev Meetup
   - Twitter/X: Tech community'yi takip et

3. OPEN SOURCE
   - "good first issue" label'li issue'lar bul
   - Dokumantasyon duzeltmeleri bile degerli
   - PR gonder, review al, ogren
   - Contributon = network + beceri + CV malzemesi

4. BLOG YAZMA
   - Dev.to, Medium, Hashnode
   - Haftada 1 teknik yazi
   - Ogrendigini payllas - baskalarina ogretmek en iyi ogrenme
   - Yazilarin LinkedIn'de paylas
```
:::

---

## 6. Freelancing

:::concept
### Freelancing Başlangıç Rehberi

**Freelancing Platformlari:**

| Platform | Seviye | Komisyon | Ipucu |
|----------|--------|----------|-------|
| Upwork | Başlangıç | %20 → %5 | Portfolio ile basvur |
| Fiverr | Başlangıç | %20 | Gig oluştur, bekle |
| Toptal | Ileri | %0 (şirket oder) | Zorlu giriş süreci |
| Freelancer.com | Başlangıç | %10 | Yaris formati |

**Ilk Freelance Projeyi Almak:**

```
1. Profil Olustur
   - Portfolio link'lerini ekle
   - Skill test'lerini gec (Upwork)
   - Profesyonel aciklama yaz

2. Ilk 3-5 Proje (dusuk fiyat, yuksek kalite)
   - Piyasanin altinda teklif ver (deneyim icin)
   - Musteteri memnuniyetine odaklan
   - 5 yildiz review topla

3. Fiyat Artir
   - Review'lar birikince fiyati artir
   - Niiche belirle (React developer, API developer)
   - Uzun vadeli musteriler edin

4. Buyume
   - Saatlik → Proje bazli fiyatlamaya gec
   - Kendi web sitenle musteri bul
   - Referral aglari kur
```
:::

:::comparison
### Full-time vs Freelancing

| Özellik | Full-time | Freelancing |
|---------|-----------|-------------|
| Gelir | Sabit, düzenli | Değişken, potansiyel yüksek |
| Güvenlik | Yüksek | Düşük (kendi sorumlulugunda) |
| Esneklik | Sınırlı | Yüksek |
| Öğrenme | Şirket içinde | Kendi kendine |
| Sosyal | Takimmdaslar | Izolasyon riski |
| Vergi | Şirket yatirir | Kendin yatirirsin |
| Kariyer | Linear ilerleme | Portfolio bazli |
| Başlangıç | Kolay | Zor (ilk musteriler) |

**Tavsiye**: Tam zamanli is + yan freelancing ile başla. Freelancing gelirin %80+ olunca tam zamanli gecebiirsin.
:::

---

## 7. Open Source Contribution

:::concept
### Neden Open Source?

Open source katkisi sana şu avantajlari sağlar:

```
1. TEKNIK BECERI
   - Buyuk codebase'lerde calismak
   - Code review almak/vermek
   - Git workflow (branching, PR, merge)
   - Testing ve CI/CD

2. NETWORK
   - Global developer community
   - Maintainer'larla tanismak
   - Referans kazanmak

3. CV/PORTFOLIO
   - "Contributed to [populer proje]" cok guclu
   - GitHub contribution graph yesillenir
   - Gercek production kodu deneyimi

4. OGRENME
   - En iyi pratikleri gormek
   - Farkli coding style'lari
   - Buyuk olcekli mimari
```
:::

:::tip
### Open Source'a Nasil Başlanır?

**Adim 1: Kolay issue'lar bul**
```
GitHub'da su label'lari ara:
- "good first issue"
- "beginner friendly"
- "help wanted"
- "documentation"
- "easy"

Ornek: github.com/[proje]/issues?q=label:"good+first+issue"
```

**Adim 2: Küçük başla**
```
- Typo duzeltme (README'de yazim hatasi)
- Dokumantasyon ekleme/iyilestirme
- Test ekleme
- Kucuk bug fix
- Ceviriler (Turkce ceviriye katki)
```

**Adim 3: PR göndermek için workflow**
```
1. Projeyi fork et
2. Clone et: git clone [fork URL]
3. Branch olustur: git checkout -b fix/typo-readme
4. Degisiklikleri yap
5. Commit et: git commit -m "Fix typo in README"
6. Push et: git push origin fix/typo-readme
7. GitHub'da PR olustur
8. Aciklama yaz + ilgili issue'yu referans ver
9. Review feedback'i uygula
10. Merge edilmesini bekle!
```

**Başlangıç için uygun projeler:**
- first-contributions (pratik için)
- freeCodeCamp
- Developer Roadmap (Turkce çeviri)
- Herhangi bir kullandigin framework/library
:::

---

## 8. Personal Branding

:::concept
### Kisisel Marka Oluşturma

```
ONLINE VARLIK HARITASI:

           LinkedIn
              │
    Portfolio ─┼─ GitHub
              │
        Blog ─┼─ Twitter/X
              │
         YouTube / Twitch
              │
     Meetup / Conference Speaker

Her kanal farkli amaca hizmet eder:
- LinkedIn: Profesyonel network ve is arama
- GitHub: Teknik beceri kaniti
- Blog: Dusunce liderligi ve ogretme
- Twitter: Hizli paylasim ve community
- Portfolio: Projeleri gosterme
```
:::

:::tip
### Blog Yazma Stratejisi

**Neden blog yaz?**
1. Ogrendigini pekistirirsin (ogretmek = en iyi öğrenme)
2. Google'da bulunursun (SEO)
3. Interview'da "Blog'umda yazdim" dersin
4. Community'de taninirsin

**Ne hakkinda yaz?**
```
Yeni baslayanlar icin (en populer):
- "React'te State Management: Redux vs Context vs Zustand"
- "Docker'a Yeni Baslayanlr icin Rehber"
- "Git Branch Stratejileri: GitFlow vs Trunk-Based"

Tutorial (her zaman aranan):
- "Next.js ile Full Stack Blog Nasil Yapilir"
- "Python FastAPI ile REST API Olusturma"
- "PostgreSQL Performance Optimization Ipuclari"

Deneyim paylasimi:
- "Junior Developer Olarak Ilk 6 Ayda Ogrendiklerim"
- "Bootcamp'ten Sonra Is Bulma Hikayem"
- "Remote Calissmanin Avantaj ve Dezavantajlari"

Debugging hikayeleri (cok ilgi ceker):
- "Production'da Memory Leak Nasil Bulduk ve Cozcduk"
- "N+1 Query Problemi Nasil Performansi Oldurur"
```

**Nerede yaz?**
- **Dev.to**: En kolay başlangıç, hazır audience
- **Hashnode**: Kendi domain'inle blog
- **Medium**: Geniş okuyucu kitlesi (ama paywall)
- **Kendi siten**: En profesyonel ama traffic zor
:::

---

## 9. Bootcamp Sonrası Öğrenme Yol Haritasi

:::concept
### Sürekli Öğrenme Plani

```
AYLIK OGRENME DONGUSU:

Hafta 1: Yeni Teknoloji Ogrenme
├── Dokumantasyon oku
├── Tutorial takip et
├── Kucuk proje yap
└── Blog yazisi yaz

Hafta 2: Derinlesme
├── Advanced konular
├── Best practices
├── Performance optimization
└── Testing stratejileri

Hafta 3: Proje Gelistirme
├── Side project'e devam
├── Yeni ozellik ekle
├── Code refactoring
└── Deploy et

Hafta 4: Community & Network
├── Open source contribution
├── Meetup/konferans
├── Blog yazisi yaz
└── LinkedIn icerik paylas
```
:::

:::realworld
### 2025-2026 Ogrenmmen Gereken Teknolojiler

```
MUST LEARN (Mutlaka ogren):
├── AI/LLM Integration
│   ├── OpenAI API / Claude API
│   ├── LangChain / LlamaIndex
│   ├── RAG (Retrieval Augmented Generation)
│   └── AI Agents
│
├── Modern Full Stack
│   ├── Next.js 16 (App Router)
│   ├── Server Components / Server Actions
│   ├── Edge Functions
│   └── Serverless Architecture
│
└── DevOps Essentials
    ├── Docker & Kubernetes basics
    ├── CI/CD (GitHub Actions)
    ├── Cloud (AWS/GCP basics)
    └── Monitoring (basic observability)

NICE TO HAVE (Avantaj saglar):
├── WebAssembly (Wasm)
├── Rust (sistem programlama)
├── Web3 basics (blockchain, smart contracts)
├── Mobile (React Native / Flutter)
└── Data Engineering basics
```
:::

:::deha-tip
### Kariyer Hizlandirici Stratejiler

**1. "T-shaped Developer" ol:**
```
Genis bilgi (breadth):
Frontend ─── Backend ─── DevOps ─── Database ─── AI

Derin uzmanlik (depth):
                │
                │ React Ecosystem
                │ ├── Next.js
                │ ├── State Management
                │ ├── Testing (RTL, Cypress)
                │ ├── Performance Optimization
                │ └── Accessibility
                ▼
```

**2. "Build in Public" yap:**
- Side project'ini herkese açık gelistir
- Her adimi Twitter/LinkedIn'de paylaş
- Hatalari ve ogrendiklerini anlat
- Community feedback al

**3. "1% Rule" uygula:**
- Her gun %1 daha iyi ol
- 1 yilda %37x buyume (bileşik)
- Küçük ama tutarli adimlar

**4. Mentorluk al ve ver:**
- Senior developer'lardan mentorluk iste
- Senden junior olanlara yardim et
- Ogretmek = 2x öğrenme
:::

:::knowledge-check
### Bilgi Kontrolu

1. ATS nedir ve CV'nin ATS-friendly olmasi için ne yapmalisin?
2. GitHub profilinde en az kac vitrin projesi olmali ve ne gostermeli?
3. LinkedIn headline'inda ne yazmalisin?
4. Is arama kanallarindan hangisi en etkilidir?
5. Open source'a katkida bulunmanin 3 avantajini say.
:::

:::exercise
### Uygulama: Kariyer Hazirlik Paketi

**Görev 1: GitHub Profili Optimize Et**
1. Profile README.md oluştur (yukardaki şablonu kullan)
2. En iyi 3-6 projeni pin'le
3. Her projede README'yi güncelle (screenshot + demo link ekle)
4. Contribution graph'i kontrol et

**Görev 2: ATS-Friendly CV Yaz**
1. Yukardaki şablonu kullanarak kendi CV'ni yaz
2. En az 3 projeyi bullet point'lerle anlat
3. Her bullet'ta rakam kullan (improved X by Y%)
4. PDF olarak kaydet

**Görev 3: LinkedIn Profili Optimize Et**
1. Headline'i güncelle (title + tech stack)
2. About section yaz (3 paragraf)
3. Experience'a projeleri ekle
4. "Open to Work" badge'ini ac
5. 10 skill ekle

**Görev 4: Ilk Hafta Eylem Plani**
1. 10 sirkete basvuru hazirla (CV + cover letter)
2. 20 LinkedIn bağlantı istegi gönder (kisisel not ile)
3. 1 blog yazisi yaz ve paylaş
4. 1 open source issue'ya yorum yaz veya PR gönder
5. 1 mock interview yap (Pramp veya arkadasinla)
:::

:::external-resource
### Ek Kaynaklar

- [GitHub Profile README Generator](https://rahuldkjain.github.io/gh-profile-readme-generator/) - README şablonu
- [Resume Worded](https://resumeworded.com/) - CV puanlama araci
- [Overleaf](https://www.overleaf.com/) - LaTeX ile profesyonel CV
- [Carbon](https://carbon.now.sh/) - Kod screenshot araci
- [Dev.to](https://dev.to/) - Teknik blog platformu
- [Pramp](https://www.pramp.com/) - Ücretsiz mock interview
- [roadmap.sh](https://roadmap.sh/) - Developer yol haritasi
- [first-contributions](https://github.com/firstcontributions/first-contributions) - Open source başlangıç
:::

---

## Özet

| Konu | Ana Fikir |
|------|-----------|
| GitHub | Yesil kare grafigi, 3-5 vitrin projesi, profesyonel README |
| CV | ATS-friendly, tek sayfa, rakamlarla impact göster |
| LinkedIn | Headline optimizasyonu, haftada 2-3 post, networking |
| Cover Letter | Sirkete ozel, 250-300 kelime, motivasyonu anlat |
| Is Arama | %60 networking + %30 direkt basvuru + %10 recruiter |
| Freelancing | Upwork/Fiverr'dan başla, review topla, fiyat artir |
| Open Source | "good first issue" ile başla, PR gönder, network kur |
| Personal Brand | Blog + LinkedIn + GitHub = dijital varligin |
| Sürekli Öğrenme | AI/LLM + Modern Full Stack + DevOps = 2025-2026 |

**Tebrikler!** Bu egitim serisini tamamladiniz. Şimdi ogrrendiklerini uygulamaya koyma zamani. Her gun bir adim at, tutarli ol ve unutma: en iyi developer dun baslayan değil, bugun devam edendir.
