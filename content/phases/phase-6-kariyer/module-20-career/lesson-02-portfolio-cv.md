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
### Vitrin Projeleri - Ne Oluşturmali?

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
- Recruiterlara InMail göndermekten cekinme
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
- **CV'yi tekrarlamak**: Cover letter ≠ CV özeti → Motivasyonunu anlat
- **Çok uzun yazmak**: Max 250-300 kelime → Kısa ve oz
- **"Dear Sir/Madam"**: Mumkunse isim bul → LinkedIn'den hiring manager'i ara
- **Türkçe/Ingilizce karışık**: Tutarli ol → Pozisyon diline gore yaz
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
| LinkedIn | Her tür | Türkçe + Ingilizce profil |
| Kariyer.net | Büyük şirketler | ATS-friendly CV yükle |
| Kommunity | Startup'lar | Turkiye startup ekosistemi |
| TopTal Turkiye | Freelance | Test-based giriş |
| Türkçell, Trendyol, Getir | Büyük tech | Kariyer sayfalarindan |

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
- Zaman farki (US = gece çalışmak gerekebilir)
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
- Developer Roadmap (Türkçe çeviri)
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

---

### Alistirma 2: Proje README Sablon Oluşturma (Kolay)

GitHub projelerinin her biri icin profesyonel README yaz.

README icermeli:
1. **Proje Basligi** ve kisa aciklama (1 cumle)
2. **Screenshot/Demo GIF** (en az 2)
3. **Tech Stack** (badge'lerle)
4. **Özellikler** (bullet list)
5. **Kurulum** (adim adim)
6. **Mimari** (basit diyagram)
7. **Ogrenilen Dersler** (2-3 madde)

```markdown
# 🎯 Proje Adi

Kisa aciklama — bu proje ne yapar ve neden onemli.

![Demo](./screenshots/demo.gif)

## Tech Stack
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript)

## Kurulum
# TODO: Adim adim kurulum talimatlari yaz
```

**Beklenen Sonuc:** Her proje README'si 200+ kelime olmali. Screenshot veya GIF icermeli. Kurulum talimatlari ile herkes projeyi çalıştırabilmeli.

---

### Alistirma 3: ATS-Uyumlu CV Yazma (Kolay)

ATS (Applicant Tracking System) tarafindan okunabilir CV yaz.

Kurallar:
1. Basit format (sutun yok, tablo yok, grafik yok)
2. Standard basliklar: Experience, Education, Skills, Projects
3. Her madde STAR formatinda, rakamlarla
4. Anahtar kelimeler job description'dan alinmali
5. PDF olarak kaydet (Word degil)

Kotu örnek: "Web geliştirme yaptim"
Iyi örnek: "React ve TypeScript ile e-ticaret platformu gelistirdim. Lighthouse performans skorunu 45'ten 92'ye cikardim. 3 ayda 15K kullanici edindik."

**Beklenen Sonuc:** CV tek sayfa olmali. En az 3 proje bullet point'lerle anlatilmali. Her bullet'ta rakamsal impact olmali. Yazim hatasi sifir olmali.

---

### Alistirma 4: LinkedIn Profil Optimizasyonu (Kolay)

LinkedIn profilini is arama icin optimize et.

1. **Headline:** "Junior Developer" yerine → "Full Stack Developer | React, Node.js, Python | Building production-ready web apps"
2. **About:** 3 paragraf — kim oldugun, ne yaptigin, ne istedigin
3. **Experience:** Projeleri experience olarak ekle (freelance/personal project)
4. **Skills:** 10+ skill ekle ve endorsement iste
5. **Featured:** En iyi 3 projeyi pin'le (live demo linkleriyle)
6. **Activity:** Haftada 2 post paylas (ogrendigini anlat)

**Beklenen Sonuc:** Headline'da en az 3 anahtar kelime olmali. About section 150+ kelime olmali. En az 3 proje experience olarak eklenmeli. "Open to Work" badge'i aktif olmali.

---

### Alistirma 5: Cover Letter Sablonu (Orta)

3 farkli sirket tipi icin cover letter sablonu oluştur.

**Startup icin:**
- Hizli ogrenme yeteneginizi vurgula
- Side project'lerden örnekler ver
- "Wear many hats" yaklasiminizi goster

**Buyuk sirket icin:**
- Teknik derinlik ve best practice bilgisini vurgula
- Olceklenebilirlik deneyiminden bahset
- Takim çalışmasi ve sureclerden örnekler ver

**Uzaktan çalışma icin:**
- Asenkron iletisim becerini goster
- Self-management ve zaman yonetimi örnekleri ver
- Timezone farklarinda çalışma deneyimi

**Beklenen Sonuc:** Her cover letter 250-300 kelime olmali. Sirkete ozel referanslar icermeli (sirketi arastir). Neden o sirket/rol oldugunu aciklamali. Genel degil, spesifik örnekler vermeli.

---

### Alistirma 6: Portfolio Sitesi Icerigi (Orta)

Portfolio sitesinin her boluimu icin icerik hazirla.

1. **Hero Section:** Kisa tanitim + CTA (CV indir, iletisim)
2. **About:** Profesyonel hikaye (3 paragraf)
3. **Projects:** En az 5 proje (screenshot + tech stack + live link + code link)
4. **Blog:** 2 teknik yazi (ogrendiklerini anlat)
5. **Contact:** Email + LinkedIn + GitHub linkleri

Her proje icin yaz:
- Problem: Ne sorunu cozuyor?
- Cozum: Nasil cozduun?
- Sonuc: Rakamsal impact (kullanici sayisi, performans, vb.)
- Tech Stack: Hangi teknolojileri kullandin?

**Beklenen Sonuc:** Portfolio'da en az 5 proje sergilenmeli. Her projenin live demo'su veya video'su olmali. Blog kisminda en az 2 teknik yazi olmali.

---

### Alistirma 7: GitHub Contribution Stratejisi (Orta)

30 gunluk GitHub aktivite plani oluştur.

**Hafta 1-2: Kendi projelerine odaklan**
- Her gun en az 1 commit (kucuk de olsa)
- README ve dokumantasyon iyilestirmeleri
- CI/CD pipeline ekle

**Hafta 3: Open source katkida bulun**
- "good first issue" etiketli 3 repo bul
- En az 1 PR gonder (dokumantasyon, bug fix, veya kucuk feature)
- Baskalarinin PR'larina code review yap

**Hafta 4: Gorunurluk**
- 1 blog yazisi yaz ve GitHub'da paylas
- Dev.to veya Hashnode'da crosspost et
- Twitter/LinkedIn'de paylasarak network genislet

**Beklenen Sonuc:** 30 gun sonunda contribution graph yesil olmali. En az 1 open source PR merge edilmis olmali. Profile'da pin'lenmis 3-5 vitrin proje olmali.

---

### Alistirma 8: Freelance Profil Oluşturma (Orta)

Upwork ve Fiverr'da rekabetci bir profil oluştur.

1. **Profil Basligi:** "Full Stack Web Developer | React, Node.js, Python | Production-Ready Applications"
2. **Profil Özeti:** 200 kelime — specialization, deneyim, çalışma sekli
3. **Portfolio:** 3-5 proje (screenshot + aciklama)
4. **Fiyatlandirma:** Piyasa arastirmasi yap, baslangic fiyatini belirle
5. **Ilk 3 proje:** Dusuk fiyatla review toplama stratejisi

**Beklenen Sonuc:** Profil metni tamamlanmis olmali. En az 3 portfolio örneği eklenmis olmali. Fiyat araligi piyasayla uyumlu olmali. Ilk proje arama stratejisi yazilmis olmali.

---

### Alistirma 9: Networking Email Sablonlari (Zor)

Farkli senaryolar icin networking email/mesaj sablonlari hazirla.

**Cold outreach (hedef sirketteki myhendise):**
"Merhaba [isim], [sirket]'teki [proje/blog/talk]'inizi gordum ve cok ilham verici buldum. Ben de [benzer konu]'da calisiiyorum. [Spesifik soru]? 15 dakikalik bir gorusme yapma imkanimiz olur mu?"

**Referral isteme:**
"Merhaba [isim], [sirket]'te [pozisyon] acik pozisyonunu gordum. Sizi [nereden/nasil] taniyorum. Bu rol icin referans olmayinii mumkun mudur? CV'mi ekte paylasiyorum."

**Thank you note (interview sonrasi):**
"Merhaba [isim], bugunku gorusme icin tesekkur ederim. [Konusmamizdan spesifik bir konu]'yu tartismak cok degerli oldu. [Rolun spesifik bir yonu]'nu dusundukce daha da heyecanliyim."

**Beklenen Sonuc:** Her sablon kisisellestirilmis olmali (copy-paste degil). Kisa ve net olmali (max 150 kelime). Spesifik referans icermeli (sirketi/kisiyi arastir). Kibbar ama ozguvenli ton tasimsali.

---

### Alistirma 10: Kariyer 90 Gunluk Eylem Plani (Zor)

Is bulma sürecini proje gibi yonet: 90 gunluk detayli plan oluştur.

**Ay 1: Hazirlik**
- Hafta 1: CV, LinkedIn, Portfolio guncellemesi
- Hafta 2: GitHub profilini optimize et, 2 projeyi canlandir
- Hafta 3: Interview hazirlik basla (gunluk 2 LeetCode + 1 system design)
- Hafta 4: 20 hedef sirket listesi oluştur, her birini arastir

**Ay 2: Basvuru ve Networking**
- Haftada 10 basvuru gonder (iş ilanlari + cold outreach)
- Haftada 5 LinkedIn bağlantı istegi (kisiisel not ile)
- Haftada 2 mock interview yap
- Dev topluluk etkinliklerine katil (meetup, conference)

**Ay 3: Interview ve Karar**
- Interview'lari takip et (spreadsheet ile)
- Teklifleri degerlendir (maas + kultur + buyume + remote)
- Maas muzakere yap
- Kabul/red kararini ver

Haftalik metrikler:
- Basvuru sayisi
- Geri donus orani
- Interview daveti orani
- Teklif sayisi

**Beklenen Sonuc:** Her hafta icin spesifik, olculebilir hedefler olmali. Tracking spreadsheet sablonu hazirlanmali. Haftalik retrospektif plani dahil olmali. Acil durum plani (3 ayda is bulamazsa ne yapacak) tanimlanmali.
:::

:::exercise
### Alistirma 11: GitHub Profil Optimizasyonu (Kolay)

GitHub profilini profesyonel seviyeye getir.

```markdown
# TODO: GitHub profil checklist

## Profile README (username/username repo)
# - [ ] Kisa bio ve uzmanlik alanlari
# - [ ] Tech stack badgeleri (shields.io)
# - [ ] GitHub stats karti
# - [ ] En onemli 3 proje linki
# - [ ] Iletisim bilgileri

## Pinned Repositories (6 adet)
# TODO: 6 pinned repo sec ve her biri icin:
# 1. [Proje adi] - [tek cumlede aciklama]
# 2. ...

## Repository Kalitesi
# - [ ] Her repo'da README.md var mi?
# - [ ] .gitignore dogru mu?
# - [ ] License ekli mi?
# - [ ] Commit mesajlari temiz mi?

## Contribution Graph
# - [ ] Son 1 yil aktif mi?
# - [ ] Duzanli commit var mi?

# TODO: Guncellenmis profil screenshot'i al
```

**Beklenen Sonuc:** Profesyonel GitHub profili olusturulmali. 6 pinned repo secilmeli. README hazirlanmali.
**Ipucu:** Recruiter'lar GitHub profiline 30 saniye bakar. Pinned repo'lar, README kalitesi ve commit duzenliligini hemen gorur.
:::

:::exercise
### Alistirma 12: Proje Showcase README Yazma (Kolay)

Portfolio projesi icin etkileyici README yaz.

```markdown
# TODO: README sablonu

# Proje Adi
> Tek cumlede ne yaptigini acikla

## Demo
[Canli Demo](link) | [Video Demo](link)
![Screenshot](screenshot.png)

## Ozellikler
- [ ] Feature 1: Aciklama
- [ ] Feature 2: Aciklama

## Tech Stack
- Frontend: React, TypeScript, Tailwind CSS
- Backend: Node.js, Express, PostgreSQL
- DevOps: Docker, GitHub Actions

## Kurulum
# TODO: Adim adim kurulum talimatlari

## Mimari
# TODO: Basit mimari diyagram

## Ogrendiklerim
# TODO: Bu projede ogrendigin 3 seyi yaz

## Lisans
MIT
```

**Beklenen Sonuc:** Kapsamli ve goze hitap eden README yazilmali. Screenshot/demo linki olmali.
**Ipucu:** README'de ilk 3 saniye kritik — baslik, tek cumle aciklama ve screenshot hemen gorunmeli. Wall of text yazma.
:::

:::exercise
### Alistirma 13: ATS-Uyumlu CV Olusturma (Kolay)

ATS (Applicant Tracking System) uyumlu CV yaz.

```markdown
# TODO: CV sablonu (1 sayfa)

## [Ad Soyad]
[Email] | [Telefon] | [LinkedIn] | [GitHub] | [Portfolio]

## Ozet (2-3 cumle)
# TODO: Pozisyona ozel ozet yaz
# "X yil deneyimli Full-Stack Developer. React, Node.js ve PostgreSQL
#  ile olceklenebilir web uygulamalari gelistirdim. Y projede Z sonuc elde ettim."

## Teknik Beceriler
# Frontend: React, TypeScript, Next.js, Tailwind CSS
# Backend: Node.js, Express, PostgreSQL, Redis
# DevOps: Docker, GitHub Actions, AWS
# TODO: Is ilanindaki anahtar kelimeleri ekle

## Projeler (en onemli 2-3)
# [Proje Adi] | [Tech Stack] | [Link]
# - Olculebilir sonuc 1 (X% iyilesme)
# - Olculebilir sonuc 2

## Egitim
# [Universite] - [Bolum] - [Yil]

# TODO: ATS kontrol listesi
# - [ ] PDF formatinda
# - [ ] Tablo/grafik YOK (ATS okuyamaz)
# - [ ] Is ilanindaki anahtar kelimeler var
# - [ ] Tarihler tutarli
# - [ ] Iletisim bilgileri header'da
```

**Beklenen Sonuc:** 1 sayfalik ATS uyumlu CV hazirlanmali. Is ilanina ozel customize edilmeli.
**Ipucu:** ATS sistemleri tablolari, grafikleri ve fancy formatlari okuyamaz. Basit, temiz format kullan. Anahtar kelimeleri is ilanindan al.
:::

:::exercise
### Alistirma 14: LinkedIn Profil Optimizasyonu (Orta)

LinkedIn profilini is arama icin optimize et.

```markdown
# TODO: LinkedIn Checklist

## Headline (120 karakter)
# YANLIS: "Is ariyorum"
# DOGRU: "Full-Stack Developer | React & Node.js | Open to Work"
# TODO: Kendi headline'ini yaz

## About (2000 karakter max)
# TODO: 3 paragraf yaz:
# 1. Ne yapiyorsun ve neden tutkuya sahipsin
# 2. Teknik beceriler ve deneyim
# 3. Ne ariyorsun + CTA (iletisime gec)

## Experience
# TODO: Her deneyim icin impact-driven bullet point'ler
# YANLIS: "React ile frontend gelistirdim"
# DOGRU: "React ile e-ticaret frontend'ini yeniden yazarak sayfa yukleme suresini %40 azalttim"

## Skills
# TODO: En az 20 skill ekle (is ilaniyla eslesen)
# TODO: Endorsement iste (3+ kisi)

## Featured
# TODO: En iyi 3 projeyi veya blog yazilarini ekle

# TODO: #OpenToWork cercevesini aktif et
# TODO: Haftada 3 post/yorum stratejisi planla
```

**Beklenen Sonuc:** Tum LinkedIn bolumler doldurulmali. Impact-driven aciklamalar yazilmali. OpenToWork aktif olmali.
**Ipucu:** LinkedIn algoritması aktif kullanicilari one cikarir. Haftada 2-3 post veya yorum yap — sadece profil doldurmak yetmez.
:::

:::exercise
### Alistirma 15: Portfolio Web Sitesi Icerigi (Orta)

Kisisel portfolio sitesinin icerik planini olustur.

```markdown
# TODO: Portfolio sitesi sayfalari

## Ana Sayfa (Hero Section)
# - Isim ve unvan
# - Tek cumlede ne yaptigini anlat
# - CTA butonlari: "Projelerim" ve "Iletisim"
# TODO: Hero metnini yaz

## Projeler Sayfasi
# TODO: 3-5 proje icin kart icerigi hazirla
# Her kart: Baslik, Screenshot, Tech stack, Kisa aciklama, Demo + GitHub linkleri

## Hakkimda
# TODO: Profesyonel hikayeni yaz (200 kelime)
# - Neden yazilim? Motivasyonun ne?
# - Guclu yonlerin
# - Hedeflerin

## Blog (opsiyonel ama etkili)
# TODO: 3 blog yazisi konusu planla
# 1. Teknik ogrenme yazisi
# 2. Proje post-mortem
# 3. Problem cozum hikayelsi

## Iletisim
# - Email formu
# - LinkedIn ve GitHub linkleri
```

**Beklenen Sonuc:** Tum sayfalarin icerigi yazilmali. En az 3 proje showcase hazir olmali.
**Ipucu:** Portfolio sitesi seni "satmali" — teknik beceri + kisilik + profesyonellik. Minimalist tasarim en iyisi, kompleks animasyonlar dikkat dagitir.
:::

:::exercise
### Alistirma 16: Cover Letter Sablonu (Orta)

Pozisyona ozel cover letter yaz.

```markdown
# TODO: Cover Letter sablonu (250-350 kelime)

## Paragraf 1: Hook (neden bu sirket)
# "X sirketinin [spesifik proje/urun]'u dikkatimi cekti cunku [neden].
#  [Pozisyon] icin basvuruyorum."
# TODO: Arastirma yapip spesifik bir detay bul

## Paragraf 2: Deger Onerim (ne katabilirim)
# "Son projemde [proje] ile [sonuc] elde ettim. Bu deneyim
#  [sirketin ihtiyaci]'na direkt katkı saglayacak."
# TODO: Is ilaniyla eslesen 2 basari hikayesi yaz

## Paragraf 3: Kulturel Uyum
# "[Sirketin degeri/kulturu] benim calisma tarzimla uyumlu.
#  [Ornek vererek acikla]."

## Paragraf 4: CTA
# "Gorusme firsati icin sabirmisizlikla bekliyorum.
#  Portfolyom: [link]. Saygilarimla, [isim]"

# TODO: 3 farkli is ilani icin customize edilmis cover letter yaz
# TODO: Her birinde sirket-spesifik detay olmali
```

**Beklenen Sonuc:** 3 farkli cover letter yazilmali. Her biri sirket-spesifik olmali. 250-350 kelime sinirinda olmali.
**Ipucu:** Generic cover letter gonderme — recruiter hemen anlar. "X sirketini sectim cunku..." cumlesi sirket-spesifik olmalm. Web sitesini, blog'u, urunleri arastir.
:::

:::exercise
### Alistirma 17: Freelance ve Remote Is Stratejisi (Orta)

Freelance ve remote is bulma stratejisi olustur.

```markdown
# TODO: Platform profilleri olustur

## Upwork Profili
# - Profesyonel baslik
# - 300 kelime portfolio ozeti
# - Skills (React, Node.js, TypeScript...)
# - Saatlik ucret belirleme
# TODO: Profil metnini yaz

## Toptal/Turing Basvurusu
# TODO: Teknik mulakat hazirlik plani

## Freelance Fiyatlandirma
# Junior: $15-25/saat
# Mid: $30-50/saat
# TODO: Kendi fiyatini belirle ve gerekcelendir

## Ilk Musteri Stratejisi
# TODO: Ilk 3 isi dusuk fiyatla alip portfolio olustur
# TODO: Musteri iletisim sablonu yaz
# TODO: Sozlesme sablonu hazirla

## Remote Is Platformlari
# - We Work Remotely
# - Remote OK
# - AngelList
# TODO: Her platformda profil olustur
```

**Beklenen Sonuc:** En az 2 platformda profil olusturulmali. Fiyatlandirma belirlenmeli. Musteri iletisim sablonu hazir olmali.
**Ipucu:** Ilk 3 freelance isi referans icin cok onemli — dusuk fiyat ver ama kaliteli is cikart. 5 yildiz review'lar gelecek islerin kapisinmi acar.
:::

:::exercise
### Alistirma 18: Networking ve Community Katilimi (Zor)

Profesyonel ag olusturma stratejisi gelistir.

```markdown
# TODO: Haftalik networking rutini

## Online
# - [ ] LinkedIn'de 3 post yorum yaz (degerli yorum, "harika" degil)
# - [ ] Twitter/X'te 2 teknik tweet paylas
# - [ ] Dev.to veya Medium'da ayda 1 blog yazisi
# - [ ] Open source projeye ayda 1 PR gonder

## Offline
# - [ ] Ayda 1 meetup'a katil (GDG, DevIstanbul, vb.)
# - [ ] Konferans izle (JSConf, DevFest)
# - [ ] Universite/bootcamp etkinliklerine katil

## Stratejik Networking
# TODO: 10 hedef kisi listesi olustur (LinkedIn'den)
# TODO: Cold outreach email sablonu yaz:
# "Merhaba [isim], [sirket]'teki [proje] calismanizi takip ediyorum.
#  [Spesifik soru]. 15 dakikalik bir gorussme yapabilir miyiz?"

# TODO: Bilgi gorusmesi (informational interview) soru listesi
# 1. "Tipik bir gununuz nasil geciyor?"
# 2. "Bu alana girmek icin en onemli tavsiyeniz ne olur?"
# 3. "Hangi becerileri gelistirmemi onerirsiniz?"
```

**Beklenen Sonuc:** Haftalik networking rutini olusturulmali. Cold outreach sablonu hazir olmali.
**Ipucu:** "Ag kurmak" degil "deger saglamak" dusuncesiyle yaklas. Baskalarina yardim et (soru cevapla, kaynak paylas) — karsilik dogal gelir.
:::

:::exercise
### Alistirma 19: 90 Gunluk Kariyer Eylem Plani (Zor)

3 aylik detayli kariyer eylem plani olustur.

```markdown
# TODO: 90 Gunluk Plan

## Hafta 1-4: Temel Hazirhk
# - [ ] Portfolio sitesini tamamla
# - [ ] CV'yi 3 versiyonda hazirla (genel, frontend, fullstack)
# - [ ] LinkedIn profilini optimize et
# - [ ] GitHub'i temizle ve 6 proje pin'le
# - [ ] 2 showcase proje tamamla
# TODO: Her hafta icin spesifik gorevler yaz

## Hafta 5-8: Aktif Basvuru
# - [ ] Gunluk 5 is basvurusu (toplam 100+)
# - [ ] Her basvuruyu spreadsheet'te takip et
# - [ ] Haftada 2 mock interview yap
# - [ ] Networking etkinliklerine katil
# TODO: Basvuru tracking spreadsheet sablonu olustur

## Hafta 9-12: Yogunlastirma
# - [ ] Gelen teklifleri degerlendir
# - [ ] Muzakere pratigi yap
# - [ ] Zayif alanlari gelistir
# - [ ] Plan B: Freelance veya staj seceicnekleri
# TODO: Haftalik retrospektif sablonu olustur

## Metrikler
# - Basvuru sayisi: ___
# - Geri donus orani: ___%
# - Interview sayisi: ___
# - Teklif sayisi: ___
```

**Beklenen Sonuc:** 12 haftalik detayli plan hazirlanmali. Haftalik olculebilir hedefler olmali. Tracking sistemi kurulmali.
**Ipucu:** Is arama bir sayi oyunudur — 100 basvuru, 20 geri donus, 10 interview, 2-3 teklif. Duzenli ve sistematik ol. Haftada retrospektif yap.
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
