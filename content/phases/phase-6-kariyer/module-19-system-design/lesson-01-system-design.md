---
title: "System Design Temelleri"
id: mod-19-system-design/lesson-01
estimated_minutes: 120
order: 1
tags: [system-design, scalability, load-balancing, caching, database, cap-theorem, interview]
prerequisites: [mod-18-architecture/lesson-01, mod-18-architecture/lesson-02]
---

# System Design Temelleri

System design interview'lar, senior-level pozisyonlarda en kritik asamalardan biridir. Bu derste, büyük ölçekli sistemleri nasil tasarlayacagini, interview'larda nasil yaklasacagini ve temel kavramlari ogreneceksin.

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "CAP teoremini, BASE ve ACID kavramlarini gerçek sistem örnekleriyle açıkla. Bir sosyal medya uygulamasinda consistency mi availability mi daha önemli? Eventual consistency ne demek ve kullanıcı deneyimini nasil etkiler? Database sharding stratejilerini (range, hash, directory) karşılaştır."

**2. Pratik Uygulama:**
> "Bir URL kısaltma servisi (TinyURL) tasarla: fonksiyonel/non-fonksiyonel gereksinimler, kapasite tahmini (QPS, storage), API tasarımı, veritabanı secimi, hash algoritmasi, caching stratejisi (Redis), load balancing ve CDN. Her tasarım kararinin nedenini açıkla. UMPIRE framework'unu kullan."
> Takip: "Şimdi bu sisteme analitik ekle (link tiklanma sayisi, cografi dagilim). Real-time analytics için Kafka + ClickHouse pipeline'i tasarla."

**3. Mukemmellik Için:**
> "Twitter/X'in home timeline'ini tasarla: fan-out-on-write vs fan-out-on-read trade-off'u, celebrity problem, real-time feed siralamaisi, notification sistemi, media storage (S3 + CDN), search (Elasticsearch). 500M aktif kullanıcı için ölçeklenebilir bir mimari ciz ve her component'in seçim nedenini açıkla."

### Pair Programming Ipucu
System design çalışırken AI'a cizdigin mimari diyagramini anlat ve sor: "Bu tasarimda single point of failure var mi? Bottleneck nerede? 10x trafik artisinda hangi component'ler cope edemez? Ölçeklendirme stratejisi öner."
:::

:::must-note
DEFTERINE YAZ - System Design Kritik Noktalar:
1. **CAP Theorem**: Consistency, Availability, Partition Tolerance - ayni anda sadece 2'sini garanti edebilirsin
2. **Horizontal vs Vertical Scaling**: Horizontal = makine ekle, Vertical = makineyi guclendir. Production'da her zaman horizontal tercih edilir
3. **Back-of-envelope calculations**: 1 gun = 86,400 saniye (~100K), 1 ay = 2.5M saniye, 1 yil = 31M saniye
4. **Caching stratejisi**: Cache-aside (lazy loading) en yaygin pattern, TTL her zaman belirle
5. **Database sharding**: Shard key secimi en kritik karar - değiştirmek çok zor
:::

:::senior-learns
**Senior/CTO Bu Konuyu Nasil Öğrenir?**

Senior muhendisler system design'i sadece kitaptan değil, **gerçek production sorunlarindan** ogrenirler:
- Bir servisin crash ettiginde ne olacagini dusunurler (failure modes)
- Her kararin **trade-off**'unu analiz ederler
- "Bu tasarım 10x trafik artisinda ne olur?" sorusunu sorarlar
- Önceki projelerdeki **hatalari** dokumante ederler
- System design blog'larini okurlar: Netflix Tech Blog, Uber Engineering, Discord Blog
- Production incident report'larini incelerler (postmortem)

**Yaklaşım**: Her konuyu "benim sistemim bu durumda ne yapar?" diye düşün.
:::

---

## 1. System Design Interview Yaklasimi

:::concept
### Interview'da Sistematik Yaklaşım

System design interview'lar open-ended sorulardir. "Doğru cevap" yoktur, **düşünme surecin** degerlendirilir.

**4 Adimli Framework:**

| Adim | Süre | Ne Yapılır |
|------|------|------------|
| 1. Requirements | 5 dk | Functional & non-functional requirements belirleme |
| 2. Estimation | 5 dk | Back-of-envelope hesaplamalar |
| 3. High-Level Design | 15 dk | Temel komponentleri cizme |
| 4. Deep Dive | 15 dk | Belirli alanlara derinlesme |

**Toplam**: ~40 dakika (genellikle 45-60 dk interview)
:::

:::tip
### Requirements Toplama Sanati

Interview'da ilk is **soru sormak**. Hemen cozume atlamak en büyük hata.

Sorulacak sorular:
- Kac kullanıcı var? (DAU - Daily Active Users)
- Read-heavy mi write-heavy mi?
- Availability mi consistency mi daha önemli?
- Hangi özellikler MVP için gerekli?
- Latency gereksinimleri neler?
- Data ne kadar surede saklanmali?
:::

:::english
**Teknik Terimler:**
- **Scalability** = Ölçeklenebilirlik: Sistemin artan yuku kaldirabilme kapasitesi
- **Throughput** = Verim: Birim zamanda islenen istek sayisi
- **Latency** = Gecikme: Bir istegin cevap süresi
- **Availability** = Erisebilirlik: Sistemin çalışır durumda olma yuzdesi
- **Consistency** = Tutarlilik: Tüm node'larin ayni veriyi gormesi
- **Partition Tolerance** = Bolunme toleransi: Network kesintilerine dayaniklilik
- **Trade-off** = Odunlesim: Bir seyi kazanmak için baska birinden vazgecme
:::

---

## 2. Back-of-Envelope Calculations

:::concept
### Tahmin Hesaplamalari

System design interview'larda büyüklük siralari (orders of magnitude) hesaplamak kritiktir.

**Temel Sayilar (Ezberle!):**

```
Hafiza / Storage:
- 1 KB  = 1,000 bytes (kisa metin)
- 1 MB  = 1,000 KB (buyuk resim)
- 1 GB  = 1,000 MB (kisa film)
- 1 TB  = 1,000 GB (buyuk veritabani)
- 1 PB  = 1,000 TB (buyuk sirket verisi)

Zaman:
- 1 gun    = 86,400 saniye  ≈ ~100K saniye
- 1 ay     = 2,500,000 saniye ≈ ~2.5M saniye
- 1 yil    = 31,000,000 saniye ≈ ~31M saniye

Latency (yaklasik):
- L1 cache reference:          0.5 ns
- L2 cache reference:          7 ns
- RAM reference:               100 ns
- SSD random read:             150 us
- HDD random read:             10 ms
- Network round trip (ayni DC): 0.5 ms
- Network round trip (farkli DC): 150 ms

Availability (yillik downtime):
- 99%     = 3.65 gun
- 99.9%   = 8.76 saat
- 99.99%  = 52.6 dakika
- 99.999% = 5.26 dakika
```
:::

:::code
### Örnek: Twitter-Benzeri Sistem Hesaplamasi

```python
# Twitter-benzeri bir sistem icin back-of-envelope hesaplama

# Kullanici sayilari
total_users = 500_000_000        # 500M toplam kullanici
daily_active_users = 200_000_000 # 200M DAU
avg_tweets_per_day = 2           # kullanici basina gunluk tweet

# Tweet hesaplamalari
daily_tweets = daily_active_users * avg_tweets_per_day
# = 400,000,000 = 400M tweet/gun

tweets_per_second = daily_tweets / 86400
# = 400M / 86400 ≈ 4,630 TPS (tweets per second)

# Peak trafik (genellikle 2-3x ortalama)
peak_tps = tweets_per_second * 3
# ≈ 13,890 TPS

# Storage hesaplama (tweet basina)
tweet_size = {
    "tweet_id": 8,           # bytes (int64)
    "user_id": 8,            # bytes
    "text": 280,             # bytes (max 280 karakter)
    "timestamp": 8,          # bytes
    "metadata": 200,         # bytes (likes, retweets, etc.)
}
avg_tweet_bytes = sum(tweet_size.values())
# = 504 bytes ≈ 500 bytes per tweet

# Gunluk storage
daily_storage = daily_tweets * avg_tweet_bytes
# = 400M * 500 bytes = 200 GB/gun

# Yillik storage
yearly_storage = daily_storage * 365
# = 200 GB * 365 = 73 TB/yil

# Media eklenirse (resim: ~200KB, video: ~2MB)
# Kullanicilarin %10'u media paylasirsa:
daily_media_storage = daily_tweets * 0.10 * 200_000  # 200KB ortalama
# = 400M * 0.10 * 200KB = 8 TB/gun media
# Yillik: 8 TB * 365 = 2.92 PB/yil media

# Read/Write orani
# Her kullanici gunluk ~100 tweet okur (timeline)
daily_reads = daily_active_users * 100
# = 20 Milyar read/gun
reads_per_second = daily_reads / 86400
# ≈ 231,481 RPS

# Read/Write orani = 231K / 4.6K ≈ 50:1
# Bu HEAVILY read-heavy bir sistem

print(f"""
=== Twitter System Design Tahminleri ===
Gunluk Tweet: {daily_tweets:,}
TPS (ortalama): {tweets_per_second:,.0f}
TPS (peak): {peak_tps:,.0f}
Gunluk Storage: {daily_storage / 1e9:.0f} GB
Yillik Storage: {yearly_storage / 1e12:.1f} TB
RPS (read): {reads_per_second:,.0f}
Read/Write Ratio: ~50:1
""")
```
:::

:::warning
### Hesaplama Hatalari

- **Kesin sayi vermeye çalışma**: "4,630 TPS" yerine "yaklaşık 5K TPS" de
- **Peak trafik unutma**: Ortalama * 2-3x peak olarak hesapla
- **Media/attachment hesaplama**: Text-only hesap yaparsan storage'i 10x az hesaplarsin
- **Read vs Write**: Çoğu sistem read-heavy, bunu belirtmezsen eksik kalir
:::

---

## 3. Scalability: Horizontal vs Vertical

:::concept
### Ölçekleme Stratejileri

```
Vertical Scaling (Scale Up):
┌─────────────────────┐
│   Daha guclu makine  │
│   CPU: 4 → 64 core  │
│   RAM: 8 → 512 GB   │
│   Disk: SSD → NVMe  │
│                      │
│   Sinirlari var!     │
└─────────────────────┘

Horizontal Scaling (Scale Out):
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ App1 │ │ App2 │ │ App3 │ │ App4 │
└──────┘ └──────┘ └──────┘ └──────┘
    │        │        │        │
    └────────┴────────┴────────┘
                 │
          ┌──────────┐
          │   Load   │
          │ Balancer │
          └──────────┘
```

| Özellik | Vertical | Horizontal |
|---------|----------|------------|
| Maliyet | Üst sinir pahali | Linear artis |
| Sinir | Fiziksel sinir var | Teorik olarak sinirsiz |
| Downtime | Upgrade için downtime | Zero downtime mumkun |
| Karmasiklik | Basit | Distributed system karmasikligi |
| Veri tutarliligi | Kolay | Zor (distributed state) |
| Failover | Single point of failure | Otomatik failover |
:::

:::comparison
### Ne Zaman Hangisi?

**Vertical Scaling Sec:**
- Küçük-orta projeler
- Database'in hala tek makinede kaldirabilecegi yuk
- Basit mimari istiyorsan
- Startup MVP asamasi

**Horizontal Scaling Sec:**
- Production büyük ölçekli sistemler
- High availability gerektiren uygulamalar
- Stateless servisler
- Microservice mimarisi

**Gerçek Dunya**: Çoğu şirket ikisini birlikte kullanir. Örneğin database için vertical (güçlü makine) + application layer için horizontal (çok makine).
:::

---

## 4. Load Balancing

:::concept
### Load Balancer Nedir?

Load balancer, gelen istekleri birden fazla sunucuya dagitan bilesendir.

```
                    Clients
                      │
                      ▼
              ┌──────────────┐
              │ Load Balancer │
              │  (L4 / L7)   │
              └──────────────┘
              ╱       │       ╲
             ▼        ▼        ▼
         ┌──────┐ ┌──────┐ ┌──────┐
         │ Srv1 │ │ Srv2 │ │ Srv3 │
         │ OK   │ │ OK   │ │ FAIL │
         └──────┘ └──────┘ └──────┘
              │        │      ✗ (trafik yonlendirilmez)
              ▼        ▼
           ┌──────────────┐
           │   Database    │
           └──────────────┘
```

**L4 vs L7 Load Balancing:**
- **L4 (Transport Layer)**: IP + Port bazli yönlendirme, hızlı, TCP/UDP seviyesi
- **L7 (Application Layer)**: HTTP header, URL, cookie bazli yönlendirme, daha akilli
:::

:::code
### Load Balancing Algoritmalari

```python
import random
import hashlib
from collections import defaultdict

class LoadBalancer:
    """Farkli load balancing algoritmalarini gosteren sinif"""

    def __init__(self, servers: list[str]):
        self.servers = servers
        self.current_index = 0
        self.weights = {}
        self.connections = defaultdict(int)

    # 1. Round Robin
    def round_robin(self) -> str:
        """Sirayla her sunucuya yonlendir"""
        server = self.servers[self.current_index % len(self.servers)]
        self.current_index += 1
        return server

    # 2. Weighted Round Robin
    def weighted_round_robin(self) -> str:
        """Agirliga gore yonlendir (guclu sunuculara daha fazla)"""
        # weights: {"server1": 3, "server2": 1, "server3": 2}
        weighted_list = []
        for server in self.servers:
            weight = self.weights.get(server, 1)
            weighted_list.extend([server] * weight)

        server = weighted_list[self.current_index % len(weighted_list)]
        self.current_index += 1
        return server

    # 3. Least Connections
    def least_connections(self) -> str:
        """En az baglantisi olan sunucuya yonlendir"""
        return min(self.servers, key=lambda s: self.connections[s])

    # 4. Random
    def random_select(self) -> str:
        """Rastgele sunucu sec"""
        return random.choice(self.servers)

    # 5. IP Hash
    def ip_hash(self, client_ip: str) -> str:
        """Ayni IP her zaman ayni sunucuya gider (session affinity)"""
        hash_val = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        index = hash_val % len(self.servers)
        return self.servers[index]


# Kullanim
lb = LoadBalancer(["web-01", "web-02", "web-03"])

# Round Robin
for i in range(6):
    print(f"Request {i+1} -> {lb.round_robin()}")
# web-01, web-02, web-03, web-01, web-02, web-03

# IP Hash - ayni kullanici ayni sunucuya
print(lb.ip_hash("192.168.1.100"))  # her zaman ayni sonuc
print(lb.ip_hash("192.168.1.100"))  # her zaman ayni sonuc
```
:::

:::tip
### Hangi Algoritmayı Seç?

- **Round Robin**: Basit, sunucular esit kapasitede
- **Weighted Round Robin**: Sunucular farklı kapasitede
- **Least Connections**: Long-lived connection'lar (WebSocket)
- **IP Hash**: Session persistence gerektiginde
- **Random**: Basit, uniform dagiliyor

**Production'da**: AWS ALB, Nginx, HAProxy gibi araclar kullanılır. Interview'da bunlari bilmek yeterli.
:::

---

## 5. Caching Strategies

:::concept
### Neden Cache?

Database çok yavas, network çok yavas. Cache = hızlı erişim katmani.

```
Latency Karsilastirmasi:
- RAM (cache):     ~100 nanosecond
- SSD (database):  ~100 microsecond  (1000x yavas)
- Network (API):   ~100 millisecond  (1,000,000x yavas)
```

**Cache Katmanlari:**

```
Browser Cache (client)
    │
    ▼
CDN Cache (edge)
    │
    ▼
API Gateway Cache
    │
    ▼
Application Cache (Redis/Memcached)
    │
    ▼
Database Query Cache
    │
    ▼
Database (source of truth)
```
:::

:::code
### Caching Patterns

```python
import time
import json
from typing import Any, Optional

# ============================================
# 1. CACHE-ASIDE (Lazy Loading) - En Yaygin
# ============================================
class CacheAside:
    """
    Uygulama cache'i yonetir.
    Read: Once cache'e bak, yoksa DB'den oku, cache'e yaz
    Write: DB'ye yaz, cache'i invalidate et
    """

    def __init__(self, cache, database):
        self.cache = cache  # Redis
        self.database = database  # PostgreSQL

    def get(self, key: str) -> Optional[Any]:
        # 1. Cache'e bak
        value = self.cache.get(key)
        if value is not None:
            print(f"Cache HIT: {key}")
            return json.loads(value)

        # 2. Cache MISS - DB'den oku
        print(f"Cache MISS: {key}")
        value = self.database.query(f"SELECT * FROM items WHERE id = {key}")

        if value:
            # 3. Cache'e yaz (TTL ile)
            self.cache.setex(key, 3600, json.dumps(value))  # 1 saat TTL

        return value

    def update(self, key: str, data: dict):
        # 1. DB'yi guncelle
        self.database.update(key, data)

        # 2. Cache'i sil (invalidate)
        self.cache.delete(key)
        # NOT: Cache'i guncellemek yerine silmek daha guvenli
        # Bir sonraki read'de cache yeniden doldurulur


# ============================================
# 2. WRITE-THROUGH
# ============================================
class WriteThrough:
    """
    Her write isleminde hem cache hem DB guncellenir.
    Pro: Cache her zaman guncel
    Con: Write latency artar (2x write)
    """

    def get(self, key: str) -> Optional[Any]:
        # Cache-aside ile ayni
        value = self.cache.get(key)
        if value:
            return json.loads(value)
        value = self.database.query(key)
        if value:
            self.cache.setex(key, 3600, json.dumps(value))
        return value

    def update(self, key: str, data: dict):
        # Hem DB hem cache ayni anda guncellenir
        self.database.update(key, data)
        self.cache.setex(key, 3600, json.dumps(data))


# ============================================
# 3. WRITE-BEHIND (Write-Back)
# ============================================
class WriteBehind:
    """
    Write islemleri once cache'e yapilir,
    sonra asenkron olarak DB'ye yazilir.
    Pro: Cok hizli write
    Con: Data loss riski (cache crash olursa)
    """

    def __init__(self, cache, database, queue):
        self.cache = cache
        self.database = database
        self.queue = queue  # Message queue (RabbitMQ, Kafka)

    def update(self, key: str, data: dict):
        # 1. Cache'e yaz (aninda)
        self.cache.setex(key, 3600, json.dumps(data))

        # 2. Queue'ya at (asenkron DB write)
        self.queue.publish({
            "operation": "update",
            "key": key,
            "data": data,
            "timestamp": time.time()
        })

    def _background_writer(self):
        """Background worker - queue'dan okuyup DB'ye yazar"""
        while True:
            message = self.queue.consume()
            self.database.update(message["key"], message["data"])
```
:::

:::comparison
### Caching Pattern Karsilastirmasi

| Pattern | Read Perf | Write Perf | Consistency | Use Case |
|---------|-----------|------------|-------------|----------|
| Cache-Aside | Iyi | Orta | Eventual | Genel amacli, en yaygin |
| Write-Through | Iyi | Yavas | Strong | Consistency önemli |
| Write-Behind | Iyi | Çok hızlı | Weak | Write-heavy, risk kabul |
| Read-Through | Iyi | - | Eventual | Cache-aside'in soyutlanmisi |

**Interview Cevabi**: "Cache-aside kullanirdim çünkü en basit ve en yaygin pattern. Write islemlerinde cache'i invalidate ederim. TTL ile stale data sorununu minimize ederim."
:::

:::realworld
### Redis Caching - Gerçek Dunyada

```python
import redis
import json
from functools import wraps

# Redis baglantisi
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# ============================================
# Dekorator ile Cache
# ============================================
def cache_result(ttl=3600, prefix="cache"):
    """Fonksiyon sonuclarini Redis'te cache'le"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Cache key olustur
            key = f"{prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

            # Cache'te var mi?
            cached = r.get(key)
            if cached:
                return json.loads(cached)

            # Fonksiyonu calistir
            result = func(*args, **kwargs)

            # Sonucu cache'le
            r.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(ttl=300)  # 5 dakika cache
def get_user_profile(user_id: int) -> dict:
    """Veritabanindan kullanici profili getir"""
    # Pahalı DB sorgusu
    return db.query("SELECT * FROM users WHERE id = %s", user_id)

@cache_result(ttl=60)  # 1 dakika cache
def get_trending_topics() -> list:
    """Trending konulari hesapla (pahalı aggregation)"""
    return db.query("""
        SELECT topic, COUNT(*) as count
        FROM tweets
        WHERE created_at > NOW() - INTERVAL '1 hour'
        GROUP BY topic
        ORDER BY count DESC
        LIMIT 10
    """)

# ============================================
# Cache Invalidation Stratejileri
# ============================================
def invalidate_user_cache(user_id: int):
    """Kullanıcı guncellendiginde ilgili tum cache'leri temizle"""
    # Pattern ile toplu silme
    pattern = f"cache:get_user_profile:({user_id},)*"
    keys = r.keys(pattern)
    if keys:
        r.delete(*keys)

def invalidate_by_tag(tag: str):
    """Tag bazli cache invalidation"""
    # Redis Set ile tag tracking
    tagged_keys = r.smembers(f"tag:{tag}")
    if tagged_keys:
        r.delete(*tagged_keys)
        r.delete(f"tag:{tag}")
```
:::

:::beginner-mistake
### Cache Hatalari

**Hata 1: Cache'i hicbir zaman expire etmemek**
```python
# YANLIS - TTL yok, data sonsuza kadar stale kalabilir
cache.set("user:123", user_data)

# DOGRU - Her zaman TTL belirle
cache.setex("user:123", 3600, user_data)  # 1 saat
```

**Hata 2: Thundering Herd Problem**
```python
# Populer bir key expire olunca binlerce request ayni anda DB'ye gider

# COZUM: Mutex/lock ile sadece 1 request DB'ye gider
def get_with_lock(key):
    value = cache.get(key)
    if value:
        return value

    # Lock al - sadece 1 thread cache'i doldurur
    lock_key = f"lock:{key}"
    if cache.set(lock_key, "1", nx=True, ex=5):
        try:
            value = database.query(key)
            cache.setex(key, 3600, value)
            return value
        finally:
            cache.delete(lock_key)
    else:
        # Lock alan baskasi var, kisa bekle ve tekrar dene
        time.sleep(0.1)
        return get_with_lock(key)
```

**Hata 3: Cache ve DB arasinda inconsistency**
- DB güncelle -> Cache sil (bu sira önemli!)
- Tersi yapilirsa: Cache silindi, DB henuz guncellenmedi, baskasi eski veriyi cache'e koyar
:::

---

## 6. CDN (Content Delivery Network)

:::concept
### CDN Nasil Çalışır?

CDN, statik içerikleri kullaniciya yakin edge server'lardan sunar.

```
Turkiye'deki kullanici  ──→  Istanbul CDN Edge  (5ms)
                              Cache HIT? ──→ Evet ──→ Hemen dondur
                                          ──→ Hayir ──→ Origin'den al, cache'le

ABD Origin Server (200ms round trip gitmeden cevap alinir!)

CDN'siz: Turkiye → ABD → Turkiye = 400ms
CDN ile:  Turkiye → Istanbul Edge = 10ms
```

**CDN Kullanım Alanlari:**
- Statik dosyalar (JS, CSS, resimler)
- Video streaming
- API response caching
- DDoS koruması

**Popular CDN Provider'lar**: Cloudflare, AWS CloudFront, Akamai, Fastly
:::

---

## 6.5 Cache Invalidation Stratejileri

:::concept
### Cache Invalidation — "En Zor Problem"

Phil Karlton: "Bilgisayar biliminde iki zor şey var: cache invalidation ve isimlendirme."

Cache invalidation, cache'teki verinin ne zaman ve nasıl güncelleneceğini belirler. Yanlış strateji = stale data veya tutarsızlık.
:::

:::architecture[Cache Invalidation Stratejileri]
```
WRITE-THROUGH:
  App ──write──► Cache ──sync write──► DB
  Okuma: Cache'ten (her zaman güncel)
  Yazma: Cache + DB aynı anda güncellenir
  ✅ Cache her zaman güncel
  ❌ Write latency 2x (iki yere yazılıyor)

WRITE-BEHIND (Write-Back):
  App ──write──► Cache ──async──► Queue ──batch write──► DB
  Okuma: Cache'ten
  Yazma: Önce cache, sonra asenkron DB'ye
  ✅ Çok hızlı write
  ❌ Cache crash = data loss riski

WRITE-AROUND:
  App ──write──► DB (cache atlanır)
  App ──read──► Cache MISS ──► DB ──► Cache'e yaz
  Okuma: Cache-aside ile lazy loading
  Yazma: Sadece DB'ye
  ✅ Write-once-read-never veri için ideal
  ❌ İlk okuma her zaman cache miss
```
:::

:::comparison
### Ne Zaman Hangi Strateji?

| Strateji | Write Hızı | Read Hızı | Tutarlılık | Risk | Kullanım |
|----------|-----------|-----------|------------|------|----------|
| **Write-Through** | Yavaş | Hızlı | Güçlü | Düşük | Banka, finans |
| **Write-Behind** | Çok hızlı | Hızlı | Zayıf | Data loss | Gaming leaderboard |
| **Write-Around** | Hızlı | İlk miss | Orta | Düşük | Log, archival data |
| **Cache-Aside** | Orta | Hızlı | Eventual | Stale data | Genel amaçlı (en yaygın) |
:::

:::realworld
### Discord — Cache Invalidation

Discord, milyarlarca mesajı yönetirken cache invalidation için hibrit yaklaşım kullanır: Sık erişilen channel'lar için Write-Through, eski mesajlar için Write-Around. Her guild (sunucu) için ayrı cache partition'ı tutulur. Hot partition sorunu için consistent hashing ile cache node'ları dağıtılır. Cache miss oranını %5'in altında tutmak SLO hedefleri arasındadır.
:::

---

## 6.6 Message Queue Derinlemesine: Kafka vs RabbitMQ vs SQS

:::concept
### Doğru Message Queue Seçimi

Message queue seçimi sistemin en kritik kararlarından biridir. Yanlış seçim, sonradan değiştirmesi çok maliyetli olan teknik borç yaratır.
:::

:::architecture[Message Queue Karşılaştırma]
```
RABBITMQ (Smart Broker / Dumb Consumer):
  Producer ──► Exchange ──routing──► Queue ──push──► Consumer
                 │
            ┌────┼────┐
            ▼    ▼    ▼
         Queue1 Queue2 Queue3

  - Message consume edilince silinir
  - Complex routing (topic, fanout, headers)
  - Per-message acknowledgment

KAFKA (Dumb Broker / Smart Consumer):
  Producer ──► Topic ──► Partition 0 [msg1, msg2, msg3, ...]
                    ──► Partition 1 [msg4, msg5, msg6, ...]
                    ──► Partition 2 [msg7, msg8, msg9, ...]
                              │
                    Consumer Group (her partition tek consumer)

  - Message silinmez (retention period boyunca kalır)
  - Consumer offset ile kendi ilerlemesini takip eder
  - Replay mümkün (event sourcing uyumlu)

AWS SQS (Managed / Serverless):
  Producer ──► SQS Queue ──poll──► Lambda / Consumer
                    │
              Standard Queue: At-least-once, sırasız
              FIFO Queue: Exactly-once, sıralı (düşük throughput)

  - Zero ops (AWS yönetir)
  - Auto-scaling
  - 14 gün retention
```
:::

:::comparison
### Kafka vs RabbitMQ vs SQS — Detaylı Karşılaştırma

| Kriter | Kafka | RabbitMQ | AWS SQS |
|--------|-------|----------|---------|
| **Throughput** | 1M+ msg/s | 50K msg/s | 3K msg/s (FIFO) |
| **Latency** | ms düzeyinde | sub-ms | 10-100ms |
| **Message Retention** | Configurable (günler/haftalar) | Consume edilince silinir | 14 güne kadar |
| **Ordering** | Partition başına garanti | Queue başına garanti | FIFO queue ile |
| **Delivery** | At-least-once | At-least-once / at-most-once | At-least-once / exactly-once (FIFO) |
| **Replay** | Evet (offset reset) | Hayır | Hayır |
| **Routing** | Topic + partition | Exchange types (fanout, topic, direct) | Basit queue |
| **Ops Burden** | Yüksek (ZooKeeper/KRaft) | Orta | Sıfır (managed) |
| **Maliyet** | Altyapı + ops | Altyapı + ops | Pay-per-request |
| **Best For** | Event streaming, log aggregation, real-time analytics | Task queue, RPC, microservice iletişimi | Serverless, basit queue ihtiyacı |
:::

:::deha-tip
### Karar Rehberi: Hangi Queue Ne Zaman?

**Kafka seç eğer:**
- Event streaming / log aggregation yapıyorsan
- Event replay gerekiyorsa (event sourcing)
- Çok yüksek throughput (100K+ msg/s)
- Birden fazla consumer aynı veriyi okuyacaksa

**RabbitMQ seç eğer:**
- Geleneksel task queue gerekiyorsa
- Complex routing kuralları varsa
- RPC pattern kullanıyorsan
- Sub-millisecond latency kritikse

**SQS seç eğer:**
- AWS ekosistemindeysen
- Ops yükü istemiyorsan
- Lambda ile serverless mimari kuruyorsan
- Basit queue yeterli ve ölçekleme otomatik olsun istiyorsan
:::

---

## 6.7 Consensus Temelleri — Raft Algoritması

:::concept
### Distributed Consensus Nedir?

Distributed sistemlerde birden fazla node'un **aynı değer üzerinde anlaşması** gerekir. Lider seçimi, konfigürasyon değişiklikleri, distributed lock gibi işlemler consensus gerektirir.

**Raft**, anlaşılması kolay bir consensus algoritmasıdır. Paxos'un daha basit alternatifidir.
:::

:::architecture[Raft Algoritması — Basitleştirilmiş]
```
RAFT STATE MACHINE:

  ┌──────────┐    timeout     ┌────────────┐   çoğunluk oyu
  │ Follower │──────────────►│ Candidate  │──────────────►┌──────────┐
  │          │◄──────────────│            │               │  Leader  │
  └──────────┘  yeni lider   └────────────┘               └──────────┘
       ▲          bulundu          ▲                            │
       │                           │   oy kaybedildi           │
       │                           └───────────────────────────│
       │                                                       │
       └───────────── heartbeat gelmezse ──────────────────────┘


LOG REPLICATION (3 node örneği):

  Leader:    [cmd1] [cmd2] [cmd3] [cmd4]  ← client yazma buraya
                │      │      │      │
                ▼      ▼      ▼      ▼
  Follower1: [cmd1] [cmd2] [cmd3] [cmd4]  ← replicate edilir
  Follower2: [cmd1] [cmd2] [cmd3]         ← biraz geride olabilir

  COMMIT RULE: Çoğunluk (2/3 node) kabul ettiyse → committed
               Leader + 1 Follower yeterli (quorum)
```
:::

:::code
### Raft — Basitleştirilmiş Python Modeli

```python
import random
import time
from enum import Enum

class NodeState(Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"

class RaftNode:
    """Basitleştirilmiş Raft node simülasyonu"""

    def __init__(self, node_id: str, peers: list[str]):
        self.node_id = node_id
        self.peers = peers
        self.state = NodeState.FOLLOWER
        self.current_term = 0
        self.voted_for = None
        self.log: list[dict] = []
        self.commit_index = -1

    def start_election(self):
        """Follower → Candidate geçişi ve oy isteme"""
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        votes_received = 1  # Kendine oy verir

        print(f"[{self.node_id}] Election started for term {self.current_term}")

        # Diğer node'lardan oy iste (simülasyon)
        for peer in self.peers:
            # Gerçekte RPC ile oy istenir
            vote_granted = random.random() > 0.3  # %70 oy verme olasılığı
            if vote_granted:
                votes_received += 1
                print(f"  [{peer}] Voted YES for {self.node_id}")

        # Çoğunluk kontrolü
        total_nodes = len(self.peers) + 1
        if votes_received > total_nodes // 2:
            self.state = NodeState.LEADER
            print(f"[{self.node_id}] Became LEADER (term {self.current_term}, "
                  f"votes: {votes_received}/{total_nodes})")
        else:
            self.state = NodeState.FOLLOWER
            print(f"[{self.node_id}] Election failed, back to FOLLOWER")

    def append_entry(self, command: str) -> bool:
        """Leader'a yeni entry ekleme"""
        if self.state != NodeState.LEADER:
            print(f"[{self.node_id}] Not leader, cannot append")
            return False

        entry = {
            "term": self.current_term,
            "command": command,
            "index": len(self.log)
        }
        self.log.append(entry)

        # Çoğunluk replicate edince commit et
        replicated = 1  # Leader'ın kendisi
        for peer in self.peers:
            # Gerçekte AppendEntries RPC ile replicate edilir
            success = random.random() > 0.1  # %90 başarı
            if success:
                replicated += 1

        total = len(self.peers) + 1
        if replicated > total // 2:
            self.commit_index = len(self.log) - 1
            print(f"[{self.node_id}] Entry committed: '{command}' "
                  f"(replicated: {replicated}/{total})")
            return True

        return False

# Simülasyon
node = RaftNode("node-1", ["node-2", "node-3", "node-4", "node-5"])
node.start_election()

if node.state == NodeState.LEADER:
    node.append_entry("SET user:1 Ali")
    node.append_entry("SET user:2 Ayse")
```
:::

:::realworld
### etcd ve Kubernetes — Raft Kullanımı

Kubernetes'in kalbi olan etcd, cluster state'ini (pod tanımları, config'ler, secret'lar) saklamak için Raft consensus kullanır. 3 veya 5 etcd node'u çalışır. Herhangi bir node çökse bile çoğunluk (quorum) sağlandığı sürece cluster çalışmaya devam eder. Bu yüzden production Kubernetes cluster'larında tek sayıda etcd node'u (3, 5, 7) kullanılır — çift sayıda node ile quorum avantajı yoktur.
:::

---

## 7. Database Sharding & Replication

:::concept
### Database Replication

```
Master-Slave (Primary-Replica) Replication:

     ┌──────────────┐
     │   Primary    │ ◄── Tum WRITE islemleri
     │  (Master)    │
     └──────────────┘
      │           │
      ▼           ▼
┌──────────┐ ┌──────────┐
│ Replica1 │ │ Replica2 │ ◄── READ islemleri
│ (Slave)  │ │ (Slave)  │
└──────────┘ └──────────┘

Avantajlar:
- Read performansi artar (replica'lara dagitilir)
- High availability (master olurse replica promote edilir)
- Backup almak kolaylasir

Dezavantajlar:
- Write hala tek master uzerinden
- Replication lag (replica'lar geride kalabilir)
```
:::

:::concept
### Database Sharding

```
Sharding: Veriyi parcalara bolup farkli sunuculara dagitma

Shard Key: user_id

user_id % 4 = shard_index

Shard 0        Shard 1        Shard 2        Shard 3
(user_id%4=0)  (user_id%4=1)  (user_id%4=2)  (user_id%4=3)
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ User 4   │   │ User 1   │   │ User 2   │   │ User 3   │
│ User 8   │   │ User 5   │   │ User 6   │   │ User 7   │
│ User 12  │   │ User 9   │   │ User 10  │   │ User 11  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

**Sharding Stratejileri:**

| Strateji | Açıklama | Avantaj | Dezavantaj |
|----------|----------|---------|------------|
| Hash-based | key % shard_count | Esit dağıtım | Reshard zor |
| Range-based | A-F shard1, G-M shard2 | Range query kolay | Hotspot riski |
| Directory-based | Lookup table | Esnek | Single point of failure |
| Geo-based | Bolgeye gore | Düşük latency | Cross-region query zor |
:::

:::code
### Consistent Hashing

```python
import hashlib
from bisect import bisect_right
from collections import defaultdict

class ConsistentHash:
    """
    Consistent Hashing: Node eklenip cikarildiginda
    sadece K/N key yer degistirir (K=key sayisi, N=node sayisi)

    Normal hash'te: Node degisince BUTUN key'ler yer degistirir
    Consistent hash'te: Sadece komsulara ait key'ler yer degistirir

    Kullanim: Cache sharding, database sharding, load balancing
    """

    def __init__(self, num_replicas: int = 150):
        self.num_replicas = num_replicas  # Virtual node sayisi
        self.ring = []          # Sorted hash degerleri
        self.ring_map = {}      # hash -> node mapping
        self.node_keys = defaultdict(set)  # node -> hash'ler

    def _hash(self, key: str) -> int:
        """String'i 32-bit integer hash'e cevir"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node: str):
        """Ring'e yeni bir node ekle"""
        for i in range(self.num_replicas):
            # Her node icin birden fazla virtual node olustur
            virtual_key = f"{node}:vn{i}"
            hash_val = self._hash(virtual_key)

            self.ring.append(hash_val)
            self.ring_map[hash_val] = node
            self.node_keys[node].add(hash_val)

        # Ring'i sirala
        self.ring.sort()
        print(f"Node eklendi: {node} ({self.num_replicas} virtual node)")

    def remove_node(self, node: str):
        """Ring'den bir node cikar"""
        for hash_val in self.node_keys[node]:
            self.ring.remove(hash_val)
            del self.ring_map[hash_val]

        del self.node_keys[node]
        print(f"Node cikarildi: {node}")

    def get_node(self, key: str) -> str:
        """Bir key icin hangi node'a gidecegini bul"""
        if not self.ring:
            return None

        hash_val = self._hash(key)

        # Binary search ile saat yonunde ilk node'u bul
        idx = bisect_right(self.ring, hash_val)

        # Sona geldiysek basa don (ring!)
        if idx == len(self.ring):
            idx = 0

        return self.ring_map[self.ring[idx]]


# Kullanim
ch = ConsistentHash(num_replicas=150)

# Node'lari ekle
ch.add_node("cache-server-1")
ch.add_node("cache-server-2")
ch.add_node("cache-server-3")

# Key'lerin dagitimini goz
keys = ["user:1001", "user:1002", "user:1003", "product:500", "session:abc"]
print("\n--- Key Dagitimi ---")
for key in keys:
    node = ch.get_node(key)
    print(f"{key} -> {node}")

# Yeni node ekle - sadece bazi key'ler yer degistirir
print("\n--- Yeni node ekleniyor ---")
ch.add_node("cache-server-4")

print("\n--- Yeni Key Dagitimi ---")
for key in keys:
    node = ch.get_node(key)
    print(f"{key} -> {node}")
# Cogu key ayni node'da kalir, sadece bazilari 4. node'a gider
```
:::

:::warning
### Sharding Zorliklari

1. **Cross-shard query**: JOIN yapmak çok zor - farkli shard'lardaki veriyi birleştirmek
2. **Resharding**: Shard sayisini degistirmek çok maliyetli (veri tasima)
3. **Hotspot**: Bazi shard'lar daha fazla trafik alabilir (unlu kullanıcı)
4. **Referential integrity**: Foreign key'ler shard'lar arasinda calismaz
5. **Distributed transactions**: ACID garantileri zorlaşir

**Interview Tavsiyesi**: "Sharding son care. Önce vertical scaling, caching, read replica denerim. Hala yetmezse sharding yaparim."
:::

---

## 8. CAP Theorem

:::concept
### CAP Theorem Nedir?

Distributed bir sistemde ayni anda sadece 3 ozellikten 2'sini garanti edebilirsin:

```
          Consistency (C)
             ╱╲
            ╱  ╲
           ╱    ╲
          ╱  CP  ╲
         ╱        ╲
        ╱──────────╲
       ╱     CA     ╲
      ╱    (teorik)   ╲
     ╱                  ╲
    ╱________AP__________╲
Availability (A)    Partition Tolerance (P)
```

**Açıklama:**
- **Consistency (C)**: Tüm node'lar ayni anda ayni veriyi gorur
- **Availability (A)**: Her request bir response alir (hata olmadan)
- **Partition Tolerance (P)**: Sistem, network bolunmelerine ragmen çalışır

**Gerçek**: Network partition'lar kacinilamaz, yani **P her zaman gerekli**. Dolayisiyla asil seçim **CP vs AP**:

| Tip | Açıklama | Örnek |
|-----|----------|-------|
| **CP** | Consistency + Partition Tolerance | Banka transferi, ZooKeeper, HBase |
| **AP** | Availability + Partition Tolerance | Sosyal medya, Cassandra, DynamoDB |
| **CA** | Teorik (partition olmayan ortam) | Tek makine RDBMS (distributed değil) |
:::

:::deha-tip
### PACELC Theorem

CAP'in genişletilmiş versiyonu. Daha gerçekçi:

**P**artition durumunda **A** mi **C** mi seç?
**E**lse (partition yokken) **L**atency mi **C**onsistency mi seç?

```
Partition var mi?
├── EVET → A (Availability) mi C (Consistency) mi? (CAP)
└── HAYIR → L (Latency) mi C (Consistency) mi? (yeni!)

Ornekler:
- DynamoDB:  PA/EL  (partition'da available, normalde low latency)
- Cassandra: PA/EL  (partition'da available, normalde low latency)
- MongoDB:   PC/EC  (partition'da consistent, normalde consistent)
- MySQL:     PA/EC  (partition'da available, normalde consistent)
```

Interview'da CAP yerine PACELC'den bahsetmek seni one çıkarır.
:::

---

## 9. Rate Limiting

:::concept
### Rate Limiting Neden Gerekli?

- DDoS koruması
- API kotu kullanimini onleme
- Kaynak adaletli dagitimi
- Maliyet kontrolu

**Popular Algoritmalar:**

| Algoritma | Açıklama | Avantaj | Dezavantaj |
|-----------|----------|---------|------------|
| Token Bucket | Kovada token'lar birikir | Burst trafige izin verir | Karmasik |
| Leaky Bucket | Sabit hizda isler | Duz trafik | Burst isleyemez |
| Fixed Window | Sabit zaman penceresi | Basit | Pencere sinirinda spike |
| Sliding Window | Kayan zaman penceresi | Duz limit | Daha fazla hafiza |

:::architecture[Rate Limiting Algoritmaları — Görsel Karşılaştırma]
```
TOKEN BUCKET:
  ┌─────────────┐
  │ Bucket      │  Capacity: 10 tokens
  │ ●●●●●●●●   │  Refill: 2 tokens/sec
  │             │
  │  [Request]──┤──► Token var? → ALLOW (token -1)
  │             │──► Token yok? → REJECT (429)
  └─────────────┘
  Burst'e izin verir: Biriken token'lar hızlı tüketilebilir

LEAKY BUCKET:
  ┌─────────────┐
  │ Queue       │  Queue size: 10
  │ ■ ■ ■ ■ ■   │
  │             │
  │  [Request]──┤──► Queue dolu? → REJECT
  │             │──► Queue boş? → Ekle
  └──────┬──────┘
         │ Sabit hız (1 req/sec)
         ▼
     [İşleniyor]
  Burst yok: Her zaman sabit hızda işler

SLIDING WINDOW:
  ←────────── 60 saniye pencere ──────────►
  [■][■][■][ ][ ][ ][■][■][ ][ ][■][ ][ ][■][NOW]
   ↑                                           ↑
   Pencere başlangıcı                    Şu an
   (eski request'ler düşer)

  Penceredeki request sayısı < limit? → ALLOW
```
:::
:::

:::code
### Rate Limiting Implementasyonu

```python
import time
from collections import defaultdict

# ============================================
# 1. TOKEN BUCKET
# ============================================
class TokenBucket:
    """
    Kovaya belirli hizda token eklenir.
    Her request bir token tuketir.
    Kova doluysa burst trafik islenebilir.
    """

    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity        # Maksimum token
        self.refill_rate = refill_rate  # Saniyede eklenen token
        self.tokens = capacity
        self.last_refill = time.time()

    def allow_request(self) -> bool:
        now = time.time()
        elapsed = now - self.last_refill

        # Token ekle
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )
        self.last_refill = now

        # Token var mi?
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


# ============================================
# 2. SLIDING WINDOW COUNTER
# ============================================
class SlidingWindowCounter:
    """
    Redis SORTED SET kullanarak sliding window rate limiting.
    Daha hassas, fixed window'daki edge case yok.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)  # user_id -> [timestamps]

    def allow_request(self, user_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        # Eski requestleri temizle
        self.requests[user_id] = [
            ts for ts in self.requests[user_id]
            if ts > window_start
        ]

        # Limit kontrolu
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True

        return False

    def get_retry_after(self, user_id: str) -> float:
        """Kac saniye sonra tekrar denenmeli"""
        if not self.requests[user_id]:
            return 0

        oldest = min(self.requests[user_id])
        return oldest + self.window_seconds - time.time()


# ============================================
# 3. DISTRIBUTED RATE LIMITER (Redis)
# ============================================
class RedisRateLimiter:
    """
    Production-ready Redis-based rate limiter.
    Lua script ile atomic islem.
    """

    def __init__(self, redis_client, max_requests=100, window=60):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window

        # Lua script - atomic islem (race condition yok)
        self.lua_script = """
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        -- Eski kayitlari sil
        redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

        -- Mevcut sayiyi al
        local count = redis.call('ZCARD', key)

        if count < limit then
            -- Izin ver ve kaydet
            redis.call('ZADD', key, now, now .. ':' .. math.random())
            redis.call('EXPIRE', key, window)
            return 1
        else
            return 0
        end
        """

    def is_allowed(self, identifier: str) -> bool:
        key = f"rate_limit:{identifier}"
        result = self.redis.eval(
            self.lua_script,
            1,        # key sayisi
            key,      # KEYS[1]
            self.max_requests,  # ARGV[1]
            self.window,        # ARGV[2]
            time.time()         # ARGV[3]
        )
        return bool(result)


# Test
limiter = SlidingWindowCounter(max_requests=5, window_seconds=60)

for i in range(7):
    allowed = limiter.allow_request("user_123")
    print(f"Request {i+1}: {'ALLOWED' if allowed else 'RATE LIMITED'}")
# Ilk 5: ALLOWED, son 2: RATE LIMITED
```
:::

---

## 10. System Design Örnekleri

:::concept
### Örnek 1: URL Shortener Tasarımı (bit.ly benzeri)

**Requirements:**
- Uzun URL'i kısa URL'e cevir
- Kısa URL'e tiklayinca orijinal URL'e redirect
- Custom short URL destegi
- Analytics (kac kez tiklanmis)
- 100M URL/ay, 10:1 read/write ratio

**Hesaplama:**
```
Write: 100M / (30 * 86400) ≈ 40 URL/saniye
Read:  40 * 10 = 400 redirect/saniye
Storage: 100M * 500 bytes = 50 GB/ay ≈ 600 GB/yil

Short URL uzunlugu:
Base62 (a-z, A-Z, 0-9) = 62 karakter
62^7 = 3.5 trilyon kombinasyon (yeterli)
```

**High-Level Design:**
```
Client
  │
  ▼
┌──────────┐     ┌──────────────┐
│   API    │────▶│  App Server  │
│ Gateway  │     │  (Stateless) │
└──────────┘     └──────┬───────┘
                        │
              ┌─────────┼──────────┐
              ▼         ▼          ▼
        ┌──────────┐ ┌───────┐ ┌──────┐
        │ Redis    │ │ DB    │ │ Kafka│
        │ (cache)  │ │(NoSQL)│ │(anal)│
        └──────────┘ └───────┘ └──────┘
```

**Key Decisions:**
1. **ID generation**: Distributed unique ID (Snowflake) + Base62 encode
2. **Database**: NoSQL (Cassandra/DynamoDB) - basit key-value, yüksek throughput
3. **Cache**: Redis - populer URL'ler için (80/20 kurali)
4. **Analytics**: Kafka ile async event processing
:::

:::code
### URL Shortener - Core Logic

```python
import hashlib
import string
import time
from dataclasses import dataclass

# Base62 encoding
BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase

@dataclass
class URLMapping:
    short_code: str
    original_url: str
    created_at: float
    click_count: int = 0
    user_id: str = None

class URLShortener:
    """Basit URL Shortener implementasyonu"""

    def __init__(self, cache, database):
        self.cache = cache
        self.database = database
        self.counter = 0  # Simple ID generator (production'da Snowflake)

    def _base62_encode(self, num: int) -> str:
        """Sayi -> Base62 string"""
        if num == 0:
            return BASE62_CHARS[0]

        result = []
        while num > 0:
            result.append(BASE62_CHARS[num % 62])
            num //= 62

        return ''.join(reversed(result))

    def _generate_short_code(self, url: str) -> str:
        """URL icin unique kisa kod olustur"""
        self.counter += 1
        # Counter + timestamp ile unique ID
        unique_id = self.counter * 1000 + int(time.time() * 1000) % 1000
        return self._base62_encode(unique_id).ljust(7, '0')[:7]

    def shorten(self, original_url: str, custom_code: str = None) -> str:
        """URL'i kisalt"""
        # Custom code kontrolu
        if custom_code:
            if self.database.exists(custom_code):
                raise ValueError("Bu kisa kod zaten kullaniliyor")
            short_code = custom_code
        else:
            short_code = self._generate_short_code(original_url)

        # DB'ye kaydet
        mapping = URLMapping(
            short_code=short_code,
            original_url=original_url,
            created_at=time.time()
        )
        self.database.save(short_code, mapping)

        # Cache'e ekle
        self.cache.setex(
            f"url:{short_code}",
            86400,  # 24 saat
            original_url
        )

        return f"https://short.ly/{short_code}"

    def redirect(self, short_code: str) -> str:
        """Kisa kod -> orijinal URL"""
        # 1. Cache'e bak
        cached_url = self.cache.get(f"url:{short_code}")
        if cached_url:
            # Async click count artir
            self._increment_click_async(short_code)
            return cached_url

        # 2. DB'den oku
        mapping = self.database.get(short_code)
        if not mapping:
            raise ValueError("URL bulunamadi - 404")

        # 3. Cache'e ekle
        self.cache.setex(f"url:{short_code}", 86400, mapping.original_url)

        self._increment_click_async(short_code)
        return mapping.original_url

    def _increment_click_async(self, short_code: str):
        """Click sayisini async artir (Kafka/queue kullan)"""
        # Production'da burasi message queue'ya event gonderir
        pass
```
:::

:::concept
### Örnek 2: Chat Sistemi Tasarımı (WhatsApp benzeri)

**Requirements:**
- 1-to-1 mesajlasma
- Grup mesajlasma (max 500 kisi)
- Online/offline durum
- Mesaj iletim durumu (sent, delivered, read)
- 500M DAU, kullanıcı basina 50 mesaj/gun

**Hesaplama:**
```
Mesaj sayisi: 500M * 50 = 25B mesaj/gun
TPS: 25B / 86400 ≈ 290K mesaj/saniye
Storage: 25B * 100 bytes = 2.5 TB/gun

WebSocket baglantisi: 500M concurrent connection
Her baglanti ~10KB RAM = 5 TB RAM (binlerce sunucu gerekli)
```

**High-Level Design:**
```
Client A                              Client B
    │                                     ▲
    │ WebSocket                           │ WebSocket
    ▼                                     │
┌───────────┐                       ┌───────────┐
│  Chat     │                       │  Chat     │
│ Server 1  │                       │ Server 2  │
└─────┬─────┘                       └─────┬─────┘
      │                                   │
      ▼                                   ▼
┌──────────────────────────────────────────────┐
│           Message Queue (Kafka)              │
└──────────────────────────────────────────────┘
      │                    │
      ▼                    ▼
┌──────────┐        ┌──────────────┐
│ Message  │        │  Presence    │
│ Store    │        │  Service     │
│ (Cassandra)       │  (Redis)     │
└──────────┘        └──────────────┘
```

**Key Decisions:**
1. **Protocol**: WebSocket (bidirectional, low latency)
2. **Message Store**: Cassandra (write-heavy, partitioned by chat_id)
3. **Presence**: Redis (in-memory, fast read/write)
4. **Message Queue**: Kafka (decouple sender and receiver)
5. **Push Notifications**: Offline kullanicilara FCM/APNs ile bildirim
:::

---

## 11. Designing Twitter (Timeline)

:::concept
### Twitter Timeline: Fan-out Problem

**En zor problem**: Bir kullanıcı tweet attiginda, takipcilerinin timeline'ina nasil ulasir?

**Yaklaşım 1: Fan-out on Read (Pull Model)**
```
Tweet atiyor → DB'ye kaydedilir
Timeline isteniyor → Takip ettiklerinin tweetlerini DB'den cek, merge et, sirala

Pro: Write basit, storage az
Con: Read cok yavas (her timeline isteginde N query)
```

**Yaklaşım 2: Fan-out on Write (Push Model)**
```
Tweet atiyor → Her takipcinin timeline cache'ine push edilir
Timeline isteniyor → Cache'ten oku (cok hizli!)

Pro: Read cok hizli (pre-computed)
Con: Write pahali (10M takipci = 10M write), storage fazla
```

**Twitter'in Gerçek Cozumu: Hybrid**
```
Normal kullanicilar → Fan-out on Write (push)
Unlu kullanicilar (10M+ takipci) → Fan-out on Read (pull)

Timeline olusturma:
1. Cache'teki pre-computed timeline'i al (push model)
2. Takip edilen unlu kullanicilarin tweetlerini DB'den cek (pull model)
3. Merge et ve sirala
```
:::

:::interview
### System Design Interview Checklist

Interview'da şunları mutlaka belirt:

**1. Requirements Phase:**
- [ ] Functional requirements (ne yapacak?)
- [ ] Non-functional requirements (scale, latency, availability)
- [ ] Back-of-envelope hesaplamalari

**2. High-Level Design:**
- [ ] API design (endpoint'ler)
- [ ] Database schema (temel tablolar)
- [ ] Sistem diagrami (komponentler + bağlantılar)

**3. Deep Dive:**
- [ ] Bottleneck'ler nerede?
- [ ] Database secimi ve neden (SQL vs NoSQL)
- [ ] Caching stratejisi
- [ ] Load balancing
- [ ] Data partitioning (sharding)

**4. Trade-offs:**
- [ ] Her kararin neden alindigini acikla
- [ ] Alternatifleri ve dezavantajlarini belirt
- [ ] "Bu tasarım X durumunda sorun yasayabilir, cozumu Y olur" de

**5. Bonus:**
- [ ] Monitoring ve alerting
- [ ] Security (authentication, rate limiting)
- [ ] Testing stratejisi
:::

:::interview
### System Design Mülakat Soruları — Junior vs Senior

**S1**: "Cache invalidation stratejilerini açıklayın."

**Junior cevap**: "TTL koyarız, süresi dolunca cache temizlenir."

**Senior cevap**: "Dört temel strateji var: Write-Through (cache + DB aynı anda yazılır, consistency güçlü ama write yavaş), Write-Behind (cache'e yazılır, DB'ye async yazılır — çok hızlı ama crash'te data loss riski), Write-Around (DB'ye yazılır, cache atlanır — write-once-read-never veri için ideal), ve Cache-Aside (en yaygın — read'de cache miss olunca DB'den oku, cache'e yaz). Thundering herd problemini mutex/lock ile çözerim. Cache ve DB arasında race condition'ı önlemek için 'DB güncelle → cache sil' sırası kritiktir."

---

**S2**: "Kafka ile RabbitMQ arasında nasıl seçim yaparsın?"

**Junior cevap**: "Kafka daha popüler, onu kullanırım."

**Senior cevap**: "İhtiyaca göre değişir. Event streaming, log aggregation veya event sourcing yapıyorsam Kafka — çünkü message retention ve replay özelliği var. Geleneksel task queue, RPC veya complex routing gerekiyorsa RabbitMQ — exchange types ile esnek routing sağlar. AWS ekosisteminde basit queue yeterliyse SQS — zero ops. Throughput ihtiyacı da belirleyici: Kafka 1M+ msg/s, RabbitMQ 50K msg/s. Trade-off: Kafka'nın operational complexity'si yüksek (ZooKeeper/KRaft yönetimi)."

---

**S3**: "Distributed sistemlerde consensus neden gerekli?"

**Junior cevap**: "Node'ların anlaşması için."

**Senior cevap**: "Distributed sistemlerde birden fazla node'un aynı state üzerinde tutarlı olması gerekir. Leader election (hangi node master?), configuration changes ve distributed lock gibi işlemler consensus gerektirir. Raft algoritması bunu sağlar: bir leader seçilir, client yazmaları leader'a gider, leader çoğunluğa (quorum) replicate eder, çoğunluk onaylarsa commit eder. etcd (Kubernetes'in state store'u) Raft kullanır. 2n+1 node ile n hata tolere edilir — bu yüzden production'da 3 veya 5 node kullanılır."

---

**S4**: "Rate limiting neden gerekli ve hangi algoritmayı seçersin?"

**Junior cevap**: "DDoS koruması için. Fixed window kullanırım."

**Senior cevap**: "Rate limiting dört amaç için gerekli: DDoS koruması, API kötüye kullanımını önleme, kaynak adaletli dağıtımı ve maliyet kontrolü. Token Bucket tercih ederim çünkü burst trafiğe izin verir — normal zamanda token birikir, anlık trafik artışında bu token'lar tüketilir. Sliding Window daha hassas ama daha fazla memory kullanır. Production'da Redis-based distributed rate limiter kullanırım (Lua script ile atomic işlem, race condition yok). API Gateway seviyesinde (Kong/Nginx) uygulanır."
:::

:::knowledge-check
### Bilgi Kontrolu

1. Cache-aside pattern'de write işlemi nasil yapılır?
2. CAP theorem'de neden CA sistemi pratikte mumkun değildir?
3. Consistent hashing'in normal hashing'e gore avantaji nedir?
4. Twitter'in hybrid fan-out modelini acikla.
5. Rate limiting için token bucket ve sliding window arasindaki fark nedir?
:::

:::exercise
### Alistirma 1: Back-of-Envelope Hesaplama (Kolay)

Bir sosyal medya uygulamasi icin kapasite ve kaynak hesaplamasi yap.

```
SENARYO: Instagram benzeri bir uygulama
- 100M gunluk aktif kullanici (DAU)
- Her kullanici gunde ortalama 5 foto goruntulur
- Her kullanici gunde ortalama 0.5 foto yukler
- Ortalama foto boyutu: 2MB (original), 200KB (thumbnail)

GOREV 1: Trafik hesaplama
- Gunluk foto yukleme sayisi = ?
- Gunluk foto goruntuleme sayisi = ?
- Saniye basina goruntuleme (QPS) = ? (gunluk / 86400)
- Peak QPS (2x ortalama) = ?

GOREV 2: Depolama hesaplama
- Gunluk yeni depolama ihtiyaci = ? (original + thumbnail)
- Yillik depolama ihtiyaci = ?
- 5 yillik toplam = ?

GOREV 3: Bant genisligi hesaplama
- Gunluk yukleme bant genisligi = ?
- Gunluk indirme bant genisligi = ?
- Saniye basina bant genisligi = ?

GOREV 4: Sunucu sayisi tahmini
- Bir sunucu saniyede 500 istek handle ediyorsa
- Peak QPS icin kac sunucu gerekir?
- %20 fazla kapasite ile kac sunucu?

# CEVAP SABLONU:
# | Metrik              | Deger         |
# |---------------------|---------------|
# | Gunluk yukleme      | 50M foto      |
# | Gunluk goruntuleme  |               |
# | QPS (ortalama)      |               |
# | Peak QPS            |               |
# | Gunluk depolama     |               |
# | Yillik depolama     |               |
# | Sunucu sayisi       |               |
```

**Beklenen Sonuc:** Gunluk 50M foto yukleme, 500M goruntuleme. QPS yaklasik 5800, peak ~11600. Gunluk depolama ~110TB. Yillik ~40PB. Bu buyuklukteki sistem icin CDN ve object storage (S3) zorunlu.
**Ipucu:** Hesaplamalarda basitlestirme yap: 1 gun = ~100K saniye (86400'u yuvarla). QPS = gunluk istek / 100K.

---

### Alistirma 2: URL Shortener Sistem Tasarimi (Orta)

Bir URL kisaltma servisi (bit.ly benzeri) icin uçtan uca sistem tasarimi yap.

```
ADIM 1: Requirements
Functional:
- Uzun URL -> kisa URL olustur
- Kisa URL -> uzun URL yonlendirmesi (301/302)
- Custom alias destegi (opsiyonel)
- Suresi dolma (TTL) destegi

Non-functional:
- Yuksek erisilebilirlik (99.9%)
- Dusuk latency (<100ms redirect)
- Kisa URL'ler benzersiz olmali

ADIM 2: Back-of-Envelope
- Gunluk 1M URL kisaltma, 100M redirect
- Read:Write orani = 100:1 (read heavy)
- Kisa URL uzunlugu: 7 karakter (base62 = 62^7 = 3.5 trilyon kombinasyon)

ADIM 3: High-Level Design
TODO: Asagidaki komponentleri ciz ve bagla:
- Client -> Load Balancer -> API Server
- API Server -> Database (URL mapping)
- API Server -> Cache (Redis — hot URL'ler)
- API Server -> ID Generator (unique short code)

ADIM 4: Database Schema
TODO: Hangi DB? (SQL vs NoSQL) Neden?
- urls tablosu: id, short_code, original_url, created_at, expires_at, click_count
- short_code uzerinde unique index

ADIM 5: Short Code Generation
TODO: 3 yaklasimdan birini sec ve acikla:
1. Counter-based (auto-increment ID -> base62)
2. Hash-based (MD5/SHA256 -> ilk 7 karakter)
3. Pre-generated keys (onceden uretilmis havuz)

ADIM 6: Caching Stratejisi
- Cache-aside pattern ile en cok tiklanan URL'leri Redis'te tut
- Cache TTL: 24 saat
- Cache boyutu: top %20 URL'ler (Pareto prensibi — %20 URL, %80 trafik)

ADIM 7: Olcekleme
- 10x scale icin ne degisir?
- Database sharding (short_code'un ilk harfine gore)
- Cache cluster (Redis Cluster)
- Rate limiting (IP basina limit)
```

**Beklenen Sonuc:** 7 adimin tamamini cevaplayabilmeli. Trade-off'lari aciklayabilmeli (ornegin hash collision vs counter single point of failure). Caching ve sharding stratejileri mantikli olmali.
**Ipucu:** Read-heavy sistemlerde caching kritik. base62 encoding: [a-zA-Z0-9] ile 7 karakter 3.5 trilyon kombinasyon saglar.

---

### Alistirma 3: Chat Uygulamasi Tasarimi (Zor)

WhatsApp benzeri bir mesajlasma uygulamasi icin detayli sistem tasarimi yap.

```
REQUIREMENTS:
- 1-1 mesajlasma
- Grup mesajlasma (max 256 uye)
- Mesaj durumu: sent, delivered, read
- Online/offline durumu
- Medya paylasimi (resim, video, dosya)
- End-to-end encryption

GOREV: Asagidaki her bolumu detayli tasarla

1. MESSAGING PROTOCOL
   - WebSocket mi HTTP Long Polling mi? Neden?
   - Baglanti yonetimi (reconnection, heartbeat)
   - Mesaj formati (JSON schema)

2. MESSAGE DELIVERY
   - Kullanici online ise: WebSocket ile aninda ilet
   - Kullanici offline ise: Queue'da beklet, online olunca ilet
   - Mesaj siralama garantisi (message ordering)

3. DATABASE DESIGN
   - messages tablosu: id, sender_id, conversation_id, content, type, status, created_at
   - conversations tablosu: id, type (1-1/group), participants
   - Hangi DB? (Cassandra — write-heavy, time-series data icin ideal)
   - Partitioning stratejisi: conversation_id ile

4. GROUP MESSAGING
   - Fan-out on write vs Fan-out on read?
   - 256 kisilik grupta her mesaj 256 kopya mi olusturulur?
   - Notification stratejisi

5. MEDIA HANDLING
   - Buyuk dosyalar icin: pre-signed URL ile dogrudan S3'e yukle
   - Thumbnail generation (async — message queue ile)
   - CDN ile dagitim

6. SCALABILITY
   - 500M aktif kullanici icin kac WebSocket sunucusu?
   - Service discovery: kullanicinin hangi sunucuya bagli oldugu
   - Cross-datacenter replication

# Cevaplari sema ve aciklama olarak yaz
# Her kararda trade-off'lari belirt
```

**Beklenen Sonuc:** WebSocket tercih edilmeli (dusuk latency, bidirectional). Fan-out on write kucuk gruplar icin, fan-out on read buyuk gruplar icin uygun. Cassandra veya ScyllaDB mesaj depolama icin ideal. Her bolumde trade-off analizi yapilmali.
**Ipucu:** WhatsApp her mesaji her cihaz icin ayri queue'da tutar. Online olunca queue'dan teslim eder. Bu "inbox model" olarak bilinir.
:::

:::external-resource
### Ek Kaynaklar

- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer) - En kapsamli kaynak
- [Designing Data-Intensive Applications (Martin Kleppmann)](https://dataintensive.net/) - Kitap
- [ByteByteGo (YouTube)](https://www.youtube.com/@ByteByteGo) - Görsel anlatim
- [Redis Documentation](https://redis.io/docs/) - Caching için
- [CAP Theorem Explained](https://www.ibm.com/topics/cap-theorem) - IBM
:::

---

## Özet

Bu derste system design'in temel kavramlarini öğrendik:

| Konu | Ana Fikir |
|------|-----------|
| Interview Yaklasimi | 4 adim: Requirements → Estimation → Design → Deep Dive |
| Scalability | Horizontal (makine ekle) > Vertical (guclendir) |
| Load Balancing | Round Robin, Least Connections, IP Hash |
| Caching | Cache-aside en yaygin, TTL her zaman belirle |
| CDN | Statik içeriği edge'de sun, latency dusur |
| Sharding | Son care, shard key secimi kritik |
| CAP Theorem | CP vs AP - gercekte P zorunlu |
| Rate Limiting | Token Bucket veya Sliding Window |
| URL Shortener | Base62 + NoSQL + Redis cache |
| Chat System | WebSocket + Kafka + Cassandra |
| Twitter Timeline | Hybrid fan-out (push + pull) |

Bir sonraki derste Data Structures & Algorithms konusuna geciyoruz - interview'larin diger büyük ayagi.
