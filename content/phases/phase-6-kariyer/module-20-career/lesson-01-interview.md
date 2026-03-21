---
title: "Teknik Mulakat Hazirligi"
id: mod-20-career/lesson-01
estimated_minutes: 100
order: 1
tags: [interview, coding-interview, system-design-interview, behavioral, STAR, UMPIRE, career]
prerequisites: [mod-19-system-design/lesson-01, mod-19-system-design/lesson-02]
---

# Teknik Mülakat Hazirligi

Teknik mülakat süreci korkutucu gorunebilir ama aslinda sistematik bir hazirlikla basarisi arttirilabilir. Bu derste coding, system design ve behavioral interview'larin her birine nasil hazirlanacagini ogreneceksin.

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Teknik mülakat surecinin 4 asamasini (coding interview, system design interview, behavioral interview, take-home project) açıkla. Her asamada ne değerlendirilir? STAR metodu behavioral sorularda nasil uygulanır? UMPIRE framework'u system design'da nasil kullanılır? Her asama için hazirlik stratejisi oluştur."

**2. Pratik Uygulama:**
> "Bana bir mock coding interview yap: Bir medium difficulty LeetCode sorusu sor, cozumumu dinle, ipuclari ver, cozumumu optimize etmemi iste ve sonunda geri bildirim ver. Gerçek bir mulakatci gibi davran - zaman siniri koy (30 dakika), düşünme surecimi degerlendirmeni iste."
> Takip: "Şimdi bir system design mock interview yap: 'Design a real-time chat application like WhatsApp' sorusunu sor ve UMPIRE framework ile adim adim cozeyim. Her adimda soru sor ve yonlendir."

**3. Mukemmellik Için:**
> "FAANG seviyesinde bir teknik mülakat için 8 haftalik çalışma plani oluştur: haftalik DSA konulari (array, string, tree, graph, DP), gunluk LeetCode problem sayisi, system design çalışma stratejisi, behavioral soru bankasi ve mock interview programi. Zayif yonlerimi belirleyip onceliklendirme yap."

### Pair Programming Ipucu
Mülakat hazirliginda AI'a çözümünü göster ve sor: "Bu çözümü bir mulakatci olarak değerlendir. Iletişim kalitem, problem çözme yaklasimim ve kod kalitem nasil? Nereleri gelistirmeliyim? Gerçekçi puan ver (1-5)."
:::

:::interview
## Mülakat Sorulari

**Soru 1: Teknik mulakatda bir soruyu cozemezseniz ne yaparisiniz?**
- **Junior cevabi:** Dusunmeye devam ederim veya bilmedigimi soylerim.
- **Senior cevabi:** Önce soruyu tamamen anladigimdan emin olurum (UMPIRE: Understand). Sonra bildigim benzer problemleri iliskilendiririm (Match). Brute force çözümü bile olsa bir yaklaşım onerir ve sesli dusunurum (think aloud). Mulakatci ipucu verirse bunu kullanarak yonumu degistiririm. Tamamen takilsam bile: 1) Problemi küçük parcalara bolerim, 2) Edge case'leri tanimlayarak analitik düşünce gosterim, 3) Hangi yaklasimi neden denedigimi açık şekilde paylasirim. Mulakatcilar cozume ulasmaktan çok düşünce sürecini ve iletişim becerini degerledirir. Susma en kotu senaryo.

**Soru 2: Behavioral interview'da "Bana bir zorlukla karsilastigin durumu anlat" sorusuna nasil yaklasirsiniz?**
- **Junior cevabi:** Bir bug bulup duzelttigim durumu anlatirim.
- **Senior cevabi:** STAR metodu ile yapilandiririm: Situation (somut proje baglami, takim buyuklugu, timeline), Task (benim spesifik sorumlulugum), Action (hangi adimlari attim, neden o yaklasimi sectim, alternatifler neydi), Result (ölçülebilir sonuçlar: %40 performans iyilestirmesi, 2 gun erken teslim). Önemli: "biz" yerine "ben" diyerek bireysel katkimi vurgularim. Basarisizlik sorusunda da cevap veririm çünkü öğrenim gosterme firsatidir. 5-7 hazır STAR hikayesi olmalisi: conflict resolution, tight deadline, leadership, failure/learning, technical challenge, cross-team collaboration, disagreement with manager.
:::

:::must-note
DEFTERINE YAZ - Mülakat Kritik Noktalar:
1. **UMPIRE Method**: Understand → Match → Plan → Implement → Review → Evaluate - her coding sorusunda bu 6 adimi takip et
2. **STAR Method**: Situation → Task → Action → Result - behavioral sorularda bu format ile cevap ver
3. **Sesli düşün (think aloud)**: Interview'da susma! Düşünce sürecini paylasarak problem çözme becerine puanlarsunlar
4. **Brute force ile başla**: Önce çalışan çözümü yaz, sonra optimize et. Bos kagit kalma
5. **Soru sor, varsayim yapma**: Interview basinda en az 3-5 clarifying question sor
:::

:::senior-learns
**Senior/CTO Bu Konuyu Nasil Öğrenir?**

Senior muhendisler mülakat hazirligini **stratejik** yapar:
- Rastgele LeetCode grind etmezler, **pattern bazli** calisirlar (15-20 core pattern yeterli)
- Her problemi bir kez cozup gecmezler, **neden bu yaklaşım?** sorusunu sorarlar
- Mock interview yaparlar - gerçek interview kosusllarini simule ederler
- System design için **gerçek production deneyimlerini** hikaye olarak hazirlrlar
- Behavioral sorular için **STAR formatinda 8-10 hazır hikaye** tutarlar
- Şirket arastirmasi yaparlar - her sirketin interview stili farklıdır

**Yaklaşım**: Mülakat bir sinav değil, **iletişim becerisi** testidir. Çözümü bilmek kadar anlatabilmek de önemli.
:::

---

## 1. Teknik Mulakat Türleri

:::concept
### Interview Pipeline

Tipik bir tech sirketinin mulakat sureci:

```
1. Resume Screen          → CV/LinkedIn incelemesi
        ↓
2. Phone Screen           → 30-45 dk, HR veya teknik kisi
        ↓
3. Online Assessment      → HackerRank/Codility/Take-home
        ↓
4. Technical Interview(s) → 1-4 round, her biri 45-60 dk
   ├── Coding Interview   → Algorithm/DS problemleri
   ├── System Design      → Buyuk olcekli sistem tasarimi
   ├── Behavioral         → Kisilik, takim calismasi
   └── Domain Specific    → Frontend/Backend/DevOps ozel
        ↓
5. Hiring Committee       → Karar (1-2 hafta)
        ↓
6. Offer / Negotiation    → Maas muzakeresi
```

**Turkiye'de tipik süreç:**
- Startup'lar: Resume → 1 teknik → 1 culture fit → Offer (1-2 hafta)
- Büyük şirketler: Resume → HR → Online test → 2-3 teknik → Offer (3-6 hafta)
- Remote/Uluslararasi: Resume → Online test → 3-5 teknik → Offer (4-8 hafta)
:::

:::comparison
### Interview Türleri Karsilastirmasi

| Tür | Süre | Ne Degerlendirilir | Hazirlik |
|-----|------|-------------------|----------|
| Coding | 45-60 dk | Problem çözme, code quality | LeetCode, pattern'ler |
| System Design | 45-60 dk | Büyük resim, trade-off'lar | Gerçek sistemler, blog'lar |
| Behavioral | 30-45 dk | Iletişim, takim çalışması | STAR hikayeleri |
| Take-home | 4-8 saat | Proje geliştirme, code quality | Portfolio projeleri |
| Live Coding | 45-60 dk | Gerçek ortamda coding | IDE/editor bilgisi |
| Pair Programming | 60 dk | Işbirliği, iletişim | Açık iletişim pratiği |
:::

---

## 2. Coding Interview Stratejisi: UMPIRE Method

:::concept
### UMPIRE - 6 Adimli Yaklaşım

Her coding sorusunda bu framework'u kullan:

| Adim | Ingilizce | Turkce | Süre |
|------|-----------|--------|------|
| **U** | Understand | Problemi anla | 3-5 dk |
| **M** | Match | Bilinen pattern'e esle | 1-2 dk |
| **P** | Plan | Çözümü planla | 3-5 dk |
| **I** | Implement | Kodu yaz | 15-20 dk |
| **R** | Review | Kodu gözden gecir | 3-5 dk |
| **E** | Evaluate | Complexity analizi | 2-3 dk |
:::

:::code
### UMPIRE Uygulamali Örnek

```python
"""
SORU: "Given an array of integers, find two numbers that add up to a target."

=====================================================
U - UNDERSTAND (Anla)
=====================================================
Clarifying questions soralim:
- Array'de negatif sayi olabilir mi? (Evet)
- Array sorted mi? (Hayir)
- Ayni elemani iki kez kullanabilir miyiz? (Hayir)
- Birden fazla cozum varsa ne dondureyim? (Herhangi birini)
- Array bos olabilir mi? (Evet, bos ise [] dondur)
- Cozum garanti mi? (Garanti, her zaman 1 cozum var)

Edge cases:
- Bos array → []
- Tek elemanli array → cozum yok
- Negatif sayilar → [-1, 3], target=2

=====================================================
M - MATCH (Esle)
=====================================================
Bu pattern'i tanidigim problemler:
- Two Sum → Hash Map pattern!
- Sorted array olsaydi → Two Pointers kullanirdim
- Hash map ile O(n) cozum mumkun

=====================================================
P - PLAN (Planla)
=====================================================
1. Bos dictionary olustur (seen = {})
2. Array'i dolas:
   a. complement = target - current_number
   b. complement seen'da varsa → cozum bulundu, index'leri dondur
   c. Yoksa current_number'i seen'a ekle (value: index)
3. Cozum bulunamazsa bos liste dondur

=====================================================
I - IMPLEMENT (Kodla)
=====================================================
"""

def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}  # sayi -> index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []

"""
=====================================================
R - REVIEW (Gozden gecir)
=====================================================
- Edge case: bos array → for dongusu calismiyor → [] dondurur ✓
- Ayni elemani 2 kez kullanma: Once complement'i kontrol ediyoruz,
  sonra ekliyoruz, yani ayni index kullanilmaz ✓
- Negatif sayilar: Hash map negatif key destekler ✓
- Off-by-one: enumerate 0'dan baslar, dogru ✓

Dry run: nums=[2,7,11,15], target=9
  i=0: num=2, comp=7, seen={} → 7 yok, seen={2:0}
  i=1: num=7, comp=2, seen={2:0} → 2 VAR! return [0,1] ✓

=====================================================
E - EVALUATE (Degerlendir)
=====================================================
Time Complexity: O(n) - array bir kez dolasiliyor
Space Complexity: O(n) - worst case tum elemanlar hash map'te
Optimizasyon: Bu zaten optimal cozum.
Sorted olsaydi: Two pointers ile O(1) space mumkun olurdu.
"""

# Test cases
print(two_sum([2, 7, 11, 15], 9))    # [0, 1]
print(two_sum([3, 2, 4], 6))          # [1, 2]
print(two_sum([-1, 0, 1, 2], 1))      # [0, 3] veya [2, 3]
print(two_sum([], 5))                  # []
```
:::

:::warning
### Coding Interview'da Yapilmamasi Gerekenler

1. **Hemen kod yazmaya başlamak** - Önce anla ve planla!
2. **Susmak** - Dusunurken bile sesli düşün
3. **Brute force'u atlamak** - "O(n^2) cozumum var ama optimize edebilirim" de
4. **Edge case'leri unutmak** - Null, bos, tek eleman, negatif
5. **Syntax'a takilmak** - Küçük hatalar sorun değil, mantık önemli
6. **"Bilmiyorum" dememek** - "Şu yaklasimi dusunuyorum..." de
7. **Ipucunu reddetmek** - Interviewer ipucu veriyorsa al, bu zayiflik değil
:::

---

## 3. Live Coding Ipuclari

:::tip
### Interview'da Etkili Coding

**Başlangıç:**
```python
# 1. Fonksiyon imzasini yaz ve input/output'u belirt
def solve(nums: list[int], target: int) -> list[int]:
    """
    Input: Sirali olmayan integer array ve target sayi
    Output: Toplami target olan iki sayinin index'leri
    """
    pass

# 2. Once brute force'u soyle
# "Brute force: iki nested loop ile O(n^2).
#  Optimize edersek hash map ile O(n) yapabiliriz."

# 3. Plan yap (pseudocode olarak)
# - Hash map olustur
# - Her eleman icin complement'i kontrol et
# - Bulursa dondur

# 4. Kodu yaz (aciklayarak)
```

**Kodlama sırasında:**
- Değişken isimlerini anlamli sec (`seen` > `d`, `complement` > `c`)
- Helper function kullan - "Bu kismi ayri bir fonksiyona alayim"
- Magic number kullanma - sabit değerleri acikla
- Her blogu acikla - "Şimdi array'i dolasip..."

**Bitirince:**
- Dry run yap (örnek input ile kodu satirlar üzerinden izle)
- Edge case'leri test et
- Time/Space complexity şöyle
- "Daha da optimize edebilirdim..." de (varsa)
:::

:::deha-tip
### Interview'da One Cikan Yaklaşımlar

1. **Trade-off'lari belirt**: "Bu çözüm O(n) time ama O(n) space. Space'i optimize etmek istersek O(n log n) time'a geceriz sorting ile."

2. **Alternatifleri bildir**: "Bunu BFS ile de DFS ile de cozebiliriz. BFS en kisa yolu garanti eder, DFS daha az memory kullanir."

3. **Production kodu yaz**: "Gerçek projede burada exception handling ve input validation eklerim."

4. **Test case'leri sen oluştur**: Sorulmadan "Şu edge case'leri test edelim..." de

5. **Ölçekleme düşün**: "Bu 10M data için çalışır mi? Calismazsa şu yaklasimi dusunurum..."
:::

---

## 4. System Design Interview Framework

:::concept
### 4 Adimli System Design Yaklasimi

```
Adim 1: REQUIREMENTS (5 dk)
├── Functional: Ne yapacak?
├── Non-functional: Scale, latency, availability?
└── Clarifying questions

Adim 2: ESTIMATION (5 dk)
├── DAU/MAU
├── Read/Write ratio
├── Storage hesaplama
└── Bandwidth hesaplama

Adim 3: HIGH-LEVEL DESIGN (15 dk)
├── API endpoints
├── Database schema
├── Sistem diagrami
└── Temel komponentler

Adim 4: DEEP DIVE (15 dk)
├── Bottleneck'ler
├── Scaling stratejisi
├── Caching
├── Database secimi
└── Trade-off'lar
```
:::

:::code
### System Design Örnek: "Design a URL Shortener"

```python
"""
=====================================================
ADIM 1: REQUIREMENTS
=====================================================

Sorular:
Q: Gunluk kac URL kisaltilacak?
A: 100M yeni URL/gun

Q: URL'lerin omru ne kadar?
A: Sonsuza kadar (expire etmez)

Q: Custom short URL destegi?
A: Evet, opsiyonel

Q: Analytics gerekli mi?
A: Temel - tiklanma sayisi

Functional Requirements:
- URL kisaltma (long -> short)
- URL yonlendirme (short -> long, 301 redirect)
- Custom alias (opsiyonel)
- Tiklanma sayaci

Non-functional Requirements:
- High availability (99.9%+)
- Low latency redirect (< 100ms)
- Short URL tahmin edilememeli (guvenlik)

=====================================================
ADIM 2: ESTIMATION
=====================================================
"""

# Back-of-envelope hesaplama
daily_writes = 100_000_000  # 100M URL/gun
write_qps = daily_writes / 86400  # ~1,160 QPS

# Read/Write ratio = 10:1
read_qps = write_qps * 10  # ~11,600 QPS
peak_read_qps = read_qps * 3  # ~34,800 QPS (peak)

# Storage (5 yillik)
url_size = 500  # bytes (short + long URL + metadata)
yearly_storage = daily_writes * 365 * url_size
# = 100M * 365 * 500 = 18.25 TB/yil
five_year_storage = yearly_storage * 5  # ~91 TB

# Short URL uzunlugu
# Base62: [a-zA-Z0-9] = 62 karakter
# 62^7 = 3.5 trilyon > 100M * 365 * 10 yil = 365B (yeterli!)

"""
=====================================================
ADIM 3: HIGH-LEVEL DESIGN
=====================================================

API Endpoints:
POST /api/shorten
  Body: {"url": "https://...", "custom_alias": "optional"}
  Response: {"short_url": "https://short.ly/abc1234"}

GET /{short_code}
  Response: 301 Redirect to original URL

GET /api/stats/{short_code}
  Response: {"clicks": 12345, "created_at": "..."}

Database Schema:
┌─────────────────────────────────┐
│ urls                            │
├─────────────────────────────────┤
│ short_code  VARCHAR(7) PK       │
│ original_url TEXT NOT NULL       │
│ user_id     INT (nullable)      │
│ created_at  TIMESTAMP           │
│ click_count INT DEFAULT 0       │
│ expires_at  TIMESTAMP (nullable)│
└─────────────────────────────────┘

System Diagram:

Client → DNS → Load Balancer → API Servers (stateless)
                                    ├── Redis (cache)
                                    ├── Database (NoSQL)
                                    └── Kafka → Analytics Service

=====================================================
ADIM 4: DEEP DIVE
=====================================================

1. ID Generation: Snowflake ID → Base62 encode
   - Distributed, unique, sortable
   - 7 karakter yeterli (3.5T kombinasyon)

2. Database: Cassandra veya DynamoDB
   - Key-value pattern'e uygun
   - High write throughput
   - Easy horizontal scaling

3. Caching: Redis
   - Hot URL'ler icin (80/20 rule)
   - Cache-aside pattern
   - TTL: 24 saat

4. Rate Limiting: Token bucket
   - IP bazli: 100 req/dk
   - User bazli: 1000 URL/gun

Trade-offs:
- NoSQL vs SQL: NoSQL daha hizli scale eder ama JOIN yok
- 301 vs 302 redirect: 301 browser cache'ler (hizli ama analytics eksik)
"""
```
:::

---

## 5. Behavioral Interview: STAR Method

:::concept
### STAR Formati

Behavioral sorulari STAR formatiyla cevapla:

```
S - Situation (Durum):  Ne oldu? Baglam ver.
T - Task (Gorev):       Senin gorev/sorumlulugumm neydi?
A - Action (Eylem):     Sen ne yaptin? (spesifik adimlar)
R - Result (Sonuc):     Sonuc ne oldu? (rakamlarla)
```

**Örnek Soru**: "Tell me about a time you dealt with a difficult technical challenge."

**STAR Cevap**:
- **S**: "E-ticaret projemizde Black Friday'de checkout sayfasi 30 saniyede cevaap veriyordu, normal zamanda 2 saniyeydi."
- **T**: "Backend developer olarak checkout API'nin performansini iyilestirmem gerekiyordu. 48 saat içinde çözüm bulmam lazimdi."
- **A**: "Database query'leri profiling yaptim, N+1 query problemi buldum. Query'leri optimize ettim, Redis cache ekledim ve database index'leri olusturdum."
- **R**: "Checkout süresi 30 saniyeden 1.5 saniyeye dustu. Black Friday'de hic downtime olmadi ve satis %25 artti."
:::

:::tip
### Hazir STAR Hikayeleri

Bu kategorilerde en az 2'ser hikaye hazirla:

| Kategori | Örnek Soru |
|----------|------------|
| Technical Challenge | "En zor teknik problemi anlat" |
| Teamwork | "Takimda anlasamadigin bir durumu anlat" |
| Leadership | "Bir projeyi yonettigin zamani anlat" |
| Failure | "Başarısız oldugun bir projeden ne ogrendin?" |
| Conflict | "Bir is arkadasiyla catismayi nasil cozaun?" |
| Time Pressure | "Deadline baskisi altinda nasil calistin?" |
| Learning | "Yeni bir teknolojiyi hizla ogrendigin zamani anlat" |
| Initiative | "Kendi inisiyatifinle baslattigin bir projeyi anlat" |

**Ipucu**: Her hikayeyi 2-3 farkli soruya adapte edebilirsin. 8-10 hazir hikaye yeterli.
:::

:::realworld
### Turkiye'de Sik Sorulan Behavioral Sorular

```
1. "Kendinizi tanitir misiniz?" (Her zaman ilk soru)
   → 2 dk elevator pitch hazirla
   → Teknik beceriler + projeler + motivasyon

2. "Neden bu sirkette calismak istiyorsunuz?"
   → Sirket arastirmasi yap
   → Teknik stack'lerini bil

3. "5 yil sonra kendinizi nerede goruyorsunuz?"
   → "Senior developer olarak buyuk olcekli sistemler tasarlamak
      ve junior'lara mentorluk yapmak istiyorum"

4. "En buyuk zafiiyetiniz nedir?"
   → Gercek ama iyilestirmek icin ugrastigin bir sey
   → "Bazen cok detaya dalip buyuk resmi kacirabiliyorum,
      bunun icin sprint planning'de onceliklendirme yapiyorum"

5. "Bize bir sey sormak ister misiniz?"
   → HER ZAMAN soru sor! Sormamak ilgisizlik gosterir
   → "Takimda agile nasil uygulanıyor?"
   → "Junior developer'lar icin mentorluk programiniz var mi?"
   → "Teknik stack'te yakin zamanda degisiklik planliyor musunuz?"
```
:::

---

## 6. Şirket Bazli Hazirlik

:::comparison
### FAANG vs Startup Interview Farklari

| Özellik | FAANG/Big Tech | Startup |
|---------|---------------|---------|
| Süre | 4-8 hafta, 5-6 round | 1-2 hafta, 2-3 round |
| Coding | LeetCode Medium-Hard | Pratik problem solving |
| System Design | Soyut büyük sistemler | Kendi urunleriyle ilgili |
| Behavioral | STAR format, liderlik | Culture fit, motivasyon |
| Take-home | Nadir | Yaygin |
| Bar | Çok yüksek | Potansiyele bakar |
| Salary | Çok yüksek (equity dahil) | Daha düşük (equity olabilir) |

**Turkiye ozel:**
- Büyük Turk sirketleri (Trendyol, Getir, Hepsiburada): FAANG-light process
- Startup'lar: Take-home + culture fit agirlikli
- Danismanlik/outsource: Teknik test + CV agirlikli
- Remote uluslararasi: Full FAANG-style process
:::

:::concept
### Şirket Arastirmasi Checklist

Interview'dan önce mutlaka yap:

```
[ ] Sirketin ne yaptiiğini anla (urun/servis)
[ ] Teknik stack'i ogren (job posting'den)
[ ] Engineering blog'unu oku (varsa)
[ ] Glassdoor/Blind'da interview deneyimlerini oku
[ ] Son haberleri takip et (buyume, yatirim, sorunlar)
[ ] Rakiplerini bil
[ ] Interview process'i hakkinda bilgi edin
[ ] LinkedIn'den interviewer'lari araştır
```
:::

---

## 7. Yaygin Hatalar ve Çözümleri

:::beginner-mistake
### Interview Hatalari

**Hata 1: Soru sormadan kodlamaya başlamak**
```
YANLIS: "Tamam, iki nested loop ile cozeyim..."
DOGRU:  "Birkaç sorum var: Array sorted mi?
         Negatif sayi olabilir mi?
         Birden fazla cozum varsa ne dondureyim?"
```

**Hata 2: Susmak**
```
YANLIS: *5 dakika sessizce dusunur*
DOGRU:  "Simdi bu problemi dusunuyorum.
         Ilk akla gelen brute force yaklasim O(n^2),
         ama hash map kullanarak optimize edebilirim.
         Cunku..."
```

**Hata 3: Stuck kalinca paniklemek**
```
YANLIS: "Bilmiyorum, yapamiyorum..."
DOGRU:  "Su ana kadar su yaklasimi denedim ama X noktasinda
         takiliyorum. Belki farkli bir aci dusunmeliyim.
         Bir ipucu verebilir misiniz?"
```

**Hata 4: Sadece cozumu yazip bitirmek**
```
YANLIS: *kodu yazar* "Bitti."
DOGRU:  *kodu yazar*
        "Simdi dry run yapayim: [2,7,11], target=9
         i=0: num=2, comp=7, seen'da yok, seen={2:0}
         i=1: num=7, comp=2, seen'da var! return [0,1]

         Time: O(n), Space: O(n).
         Edge case: bos array icin [] doner. ✓"
```

**Hata 5: Maas beklentisini hemen soylemek**
```
YANLIS: "40.000 TL istiyorum" (interview basinda)
DOGRU:  "Maas beklentimi offer asamasinda detayli konusabiliriz.
         Sirketin bu pozisyon icin belirlediği aralikli
         ogrenebilir miyim?"
```
:::

---

## 8. Maas Muzakeresi Temelleri

:::concept
### Negotiation Stratejisi

**Altin Kurallar:**
1. **Ilk rakami sen soyeme** - Sirketten range isteyin
2. **Her zaman negotiate et** - Ilk teklif nadiren final'dir
3. **Toplam paketi değer** - Base + bonus + equity + benefits
4. **Alternatiflerin olsun** - Birden fazla offer = güç

**Turkiye Piyasasi (2025-2026 araligi, yaklaşık):**

| Seviye | Turkiye (TL/ay) | Remote/Uluslararasi (USD/yil) |
|--------|----------------|-------------------------------|
| Junior (0-2 yil) | 25K-50K | $30K-60K |
| Mid (2-5 yil) | 50K-100K | $60K-100K |
| Senior (5+ yil) | 100K-200K | $100K-180K |
| Lead/Staff | 200K+ | $150K-250K+ |

*Not: Bu rakamlar şirket, sehir ve teknolojiye gore değişir*
:::

:::tip
### Negotiation Ipuclari

```
1. Offer aldiktan sonra hemen "evet" deme
   → "Bu harika bir firsat, detaylari inceleyip
      size 2-3 gun icinde donebilir miyim?"

2. Counter-offer yaparken gerekce goster
   → "Piyasa arastirmama gore bu pozisyon icin
      X-Y araligi normal. Benim Z deneyimim ve
      W becerilerim bu araligin ust kisminni hak ediyor."

3. Base salary disindaki seyleri de negotiate et
   → Remote calisma gunleri
   → Egitim butcesi
   → Bilgisayar/ekipman
   → Tatil gunleri
   → Signing bonus

4. Written offer iste
   → Sozlu offer yeterli degil
   → "Bunu mail olarak alabilir miyim?"
```
:::

---

## 9. Interview Hazirlik Plani

:::concept
### 4 Haftalik Hazirlik Plani

```
HAFTA 1: Temeller
├── Gun 1-2: Big-O ve array problemleri (5 problem/gun)
├── Gun 3-4: Hash map ve string problemleri
├── Gun 5: Stack/Queue problemleri
├── Gun 6: Linked list problemleri
└── Gun 7: Review + mock interview

HAFTA 2: Orta Seviye
├── Gun 1-2: Tree/BST problemleri
├── Gun 3-4: Graph (BFS/DFS) problemleri
├── Gun 5: Dynamic programming (easy-medium)
├── Gun 6: Sliding window + Two pointers
└── Gun 7: Review + mock interview

HAFTA 3: Ileri Seviye
├── Gun 1-2: System design temelleri
├── Gun 3: System design pratik (URL Shortener)
├── Gun 4: System design pratik (Chat System)
├── Gun 5: Behavioral STAR hikayeleri hazirla
├── Gun 6: Company research
└── Gun 7: Full mock interview (tum turler)

HAFTA 4: Son Hazirlik
├── Gun 1-3: Zayif alanlara odaklan
├── Gun 4: Populer medium-hard problemler
├── Gun 5: System design review
├── Gun 6: Behavioral review + soru listesi
└── Gun 7: Dinlen, erken yat, kendine guven!
```
:::

:::realworld
### Gunluk Çalışma Rutini

```
Sabah (1 saat):
- 1 LeetCode Easy (15 dk)
- 1 LeetCode Medium (30 dk)
- Cozumleri review et (15 dk)

Ogle (30 dk):
- System design notlarini oku
- 1 concept derinles (caching, sharding, etc.)

Aksam (1 saat):
- 1 LeetCode Medium/Hard (45 dk)
- Behavioral soru pratigi (15 dk)

Hafta sonu (2 saat):
- Full mock interview
- Zayif alanlari belirle
- Gelecek hafta plani yap
```
:::

---

## 10. Interview Gunu

:::tip
### Interview Gunu Checklist

**Oncesinde:**
```
[ ] Erken yat (en az 7 saat uyku)
[ ] Sabah kahvaltini yap
[ ] Kiyafet hazirla (business casual - uzaktan bile)
[ ] Bilgisayar sarji + yedek sarj aleti
[ ] Internet baglantisi test et (online ise)
[ ] IDE/editor'u hazirla
[ ] Su ve kagit-kalem hazirla
[ ] 10 dk once hazir ol
```

**Sırasında:**
```
[ ] Gulus ve pozitif ol
[ ] Soru sor (en az 3-5 clarifying question)
[ ] Sesli dusun - surecini payllas
[ ] Brute force'u belirt, sonra optimize et
[ ] Edge case'leri kontrol et
[ ] Dry run yap
[ ] Complexity'yi soyle
[ ] Sonunda sirkete sorularin ol
```

**Sonrasinda:**
```
[ ] Thank you email gonder (24 saat icinde)
[ ] Sorulari ve cevaplarini not et
[ ] Ne iyi gitti, ne kotuyu yaz
[ ] Bir sonraki interview icin iyilestirme plani
```
:::

:::english
**Teknik Terimler:**
- **Mock Interview** = Sahte/pratik mülakat
- **Whiteboard Coding** = Beyaz tahta üzerinde kodlama
- **Take-home Assignment** = Eve verilen odev projesi
- **Behavioral Question** = Davranissal soru
- **Culture Fit** = Şirket kulturune uyum
- **Offer Letter** = Is teklif mektubu
- **Counter-offer** = Karsi teklif
- **Compensation Package** = Ucret paketi (maas + bonus + yan haklar)
- **Equity/Stock Options** = Hisse senedi/opsiyon
- **Signing Bonus** = Imza bonusu
:::

:::knowledge-check
### Bilgi Kontrolu

1. UMPIRE method'un 6 adimini say.
2. STAR method'da "A" ne anlama gelir ve neden önemlidir?
3. Coding interview'da brute force çözümü neden belirtilmelidir?
4. System design interview'da ilk 5 dakikada ne yapılır?
5. Maas muzakeresinde neden ilk rakami sen soylememelisin?
:::

:::exercise
### Uygulama: Mock Interview Hazirlik

**Görev 1: STAR Hikayeleri**
Aşağıdaki 5 kategori için birer STAR hikayesi yaz:
1. Teknik bir zorlugu astigin bir an
2. Takim icerisinde bir catismayi cozdugun bir an
3. Bir projede liderlik yaptığın bir an
4. Başarısız oldugun ve ders cikardigin bir an
5. Yeni bir teknolojiyi hızla ogrendigin bir an

**Görev 2: Elevator Pitch**
Kendini 2 dakikada tanitan bir pitch yaz. Icermeli:
- Kim oldugun (isim, egitim, deneyim)
- Ne yaptığın (teknik beceriler)
- Ne istedigin (hedef pozisyon)
- Neden sen (fark yaratan ozelligin)

**Görev 3: Mock Coding Interview**
Bir arkadasinla veya timer ile şu problemi UMPIRE method ile coz:
- LeetCode #15 - 3Sum
- 45 dakika süre ver
- Sesli düşün (kayıt al)
- Sonra kendini değerlendir
:::

:::external-resource
### Ek Kaynaklar

- [Pramp](https://www.pramp.com/) - Ücretsiz mock interview platformu
- [interviewing.io](https://interviewing.io/) - Anonim mock interview
- [LeetCode](https://leetcode.com/) - Coding pratik
- [NeetCode 150](https://neetcode.io/practice) - Curated problem list
- [Blind 75](https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions) - En önemli 75 problem
- [Glassdoor](https://www.glassdoor.com/) - Şirket interview deneyimleri
- [levels.fyi](https://www.levels.fyi/) - Maas karşılaştırma
:::

---

## Özet

| Konu | Ana Fikir |
|------|-----------|
| Interview Türleri | Coding + System Design + Behavioral |
| UMPIRE | Understand → Match → Plan → Implement → Review → Evaluate |
| STAR | Situation → Task → Action → Result |
| Live Coding | Sesli düşün, brute force belirt, edge case test et |
| System Design | Requirements → Estimation → Design → Deep Dive |
| Behavioral | 8-10 hazir STAR hikayesi tut |
| FAANG vs Startup | FAANG: algorithmic, Startup: practical |
| Maas | Ilk rakami soyletme, toplam paketi değer |
| Hazirlik | 4 hafta sistematik plan |
| Interview Gunu | Soru sor, sesli düşün, pozitif ol |

Bir sonraki derste Portfolio, CV ve Kariyer Stratejisi'ni ogreneceksin.
