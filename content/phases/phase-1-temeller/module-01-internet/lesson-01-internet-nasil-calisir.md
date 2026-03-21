---
title: "İnternet Nasıl Çalışır? TCP/IP ve Protokol Stack"
estimated_minutes: 45
tags: ["tcp/ip", "networking", "protocols", "internet"]
prerequisites: []
---

# İnternet Nasıl Çalışır? TCP/IP ve Protokol Stack

:::realworld
Her gün kullandığın internet aslında muazzam derecede karmaşık bir mühendislik harikası. Bir web sayfasını açtığında, verin binlerce kilometre fiber optik kablo üzerinden, onlarca router'dan geçerek sana ulaşıyor. Bu derste, bu sürecin her adımını "deha seviyesinde" anlayacaksın. Mülakatların en klasik sorusu olan "Tarayıcıya URL yazdığında ne olur?" sorusuna 5-10 dakikalık detaylı cevap verebilecek seviyeye geleceksin.

**Gerçek Dünya Örnekleri:**
- **Netflix:** Tek bir film izlemek için istemcin ve Netflix sunucuları arasında yüzlerce TCP bağlantısı kurulur. Netflix, kendi CDN'i (Open Connect) ile içerikleri ISP'lerin veri merkezlerine yerleştirerek latency'yi minimize eder.
- **Google:** Google'ın arama sonucu sayfası ortalama 200ms'de yüklenir. Bu hızın sırrı: anycast DNS ile en yakın sunucuya yönlendirme, persistent TCP bağlantıları, QUIC protokolü (UDP tabanlı) ve agresif caching.
- **Cloudflare:** Global CDN olarak 300+ lokasyonda çalışır. Bir Türk kullanıcının isteği İstanbul POP'una (Point of Presence) gider, ABD'deki origin sunucuya gitmek zorunda kalmaz. DNS seviyesinde yük dengeleme yapar.
- **WhatsApp:** Mesajlar TCP üzerinden gönderilir (güvenilirlik gerekli), ancak sesli/görüntülü aramalar UDP üzerinden yapılır (düşük latency gerekli). Bir paket kaybolursa mesajda sorun olur ama aramada sadece küçük bir kesinti yaşanır.
:::

## Neden Bu Konuyu Öğreniyorsun?

Bir full stack developer olarak, yazdığın her kod sonuçta ağ üzerinden iletişim kurar. Bir API çağrısı yaptığında, bir form gönderdiğinde veya bir WebSocket bağlantısı kurduğunda, altta TCP/IP protokolü çalışıyor. Bu katmanları anlamadan:

- Neden bazen API çağrıların yavaş olduğunu anlayamazsın
- Network hatalarını debug edemezsin
- Güvenlik açıklarını fark edemezsin
- Sistem tasarımı mülakatlarında başarısız olursun

:::deha-tip
Deha seviyesi geliştiriciler, bir hata aldıklarında sadece error mesajına değil, network katmanına da bakar. Browser DevTools'un Network tab'ını her gün kullanırlar. "Bu request neden 3 saniye sürdü?" sorusuna TCP handshake, DNS resolution, TLS negotiation ve server processing sürelerini ayrı ayrı analiz ederek cevap verebilirler.
:::

## TCP/IP Protokol Stack: 5 Katman

İnternet iletişimi 5 katmanlı bir mimari üzerine kuruludur. Her katman belirli bir görevi üstlenir ve üstündeki katmana hizmet sunar.

:::concept[Protokol Stack (İng: Protocol Stack)]
Protokol stack, ağ iletişiminde verilerin nasıl hazırlanacağını, iletileceğini ve alınacağını belirleyen katmanlı bir yapıdır.

**Türkçe karşılığı:** Protokol Yığını / Katmanları
**Ne işe yarar:** Karmaşık ağ iletişimini yönetilebilir katmanlara böler
**Gerçek hayat benzetmesi:** Posta sistemi gibi düşün - zarfı yaz (uygulama), zarfı kapat (taşıma), adres yaz (ağ), postacıya ver (veri bağlantısı), postacı yürür (fiziksel)
:::

### Katman 5: Uygulama Katmanı (Application Layer)

Bu katmanda HTTP, HTTPS, FTP, SMTP, DNS gibi protokoller çalışır. Senin yazılımın (tarayıcı, API client) doğrudan bu katmanla etkileşim kurar.

:::code[text]{title="Uygulama Katmanı Protokolleri"}
HTTP/HTTPS  → Web sayfaları ve API'ler (port 80/443)
DNS         → Domain isimlerini IP adreslerine çevirme (port 53)
FTP         → Dosya transferi (port 21)
SMTP        → Email gönderme (port 25/587)
SSH         → Güvenli uzak bağlantı (port 22)
WebSocket   → Çift yönlü gerçek zamanlı iletişim (port 80/443)
:::

### Katman 4: Taşıma Katmanı (Transport Layer)

:::concept[TCP (Transmission Control Protocol)]
TCP, güvenilir veri iletimi sağlayan bir protokoldür. Veriyi parçalara (segment) böler, sıralı olarak gönderir, kayıp paketleri tekrar gönderir.

**Türkçe karşılığı:** İletim Kontrol Protokolü
**Ne işe yarar:** Verinin eksiksiz ve sıralı olarak karşı tarafa ulaşmasını garanti eder
**Gerçek hayat benzetmesi:** Kargoya kitap gönderirken, her sayfayı ayrı zarfta numaralandırıp göndermek ve karşı tarafın eksik sayfaları bildirmesi gibi
:::

:::comparison
| Özellik | TCP | UDP |
|---------|-----|-----|
| Güvenilirlik | Garantili teslimat | Garantisiz |
| Sıralama | Sıralı | Sırasız |
| Hız | Daha yavaş (overhead) | Daha hızlı |
| Bağlantı | Connection-oriented (3-way handshake) | Connectionless |
| **Ne zaman kullan** | Web, email, dosya transferi, API | Video streaming, online oyun, DNS sorgusu |
| Protokol örnekleri | HTTP, HTTPS, FTP, SMTP | DNS, DHCP, VoIP, video conferencing |

**Tavsiye:** Web geliştirmede %99 TCP kullanacaksın (HTTP/HTTPS üzerinden). UDP'yi bilmen, sistem tasarımı mülakatlarında sana avantaj sağlar.
:::

#### TCP 3-Way Handshake

TCP bağlantısı kurmak için 3 adımlı bir el sıkışma yapılır:

:::code[text]{title="TCP 3-Way Handshake"}
Client                    Server
  |                         |
  |---- SYN (seq=100) ----->|   1. "Bağlanmak istiyorum"
  |                         |
  |<--- SYN-ACK (seq=300,  |   2. "Tamam, ben de hazırım"
  |     ack=101) -----------|
  |                         |
  |---- ACK (ack=301) ----->|   3. "Harika, başlayalım"
  |                         |
  |===== VERİ TRANSFERİ ===|   Artık veri gönderilebilir
:::

:::beginner-mistake
Yaygın hata: "TCP yavaş çünkü 3-way handshake var" demek. Evet handshake ek gecikme ekler (1 RTT = Round Trip Time), ama bu güvenilirlik için ödenen küçük bir bedel. HTTP/2 ve HTTP/3 bu maliyeti azaltmak için optimizasyonlar içerir.
:::

#### TCP Bağlantı Sonlandırma (4-Way Teardown)

Bağlantı kapanırken 4 adımlı bir süreç izlenir:

:::code[text]{title="TCP 4-Way Teardown"}
Client                    Server
  |                         |
  |---- FIN (seq=500) ----->|   1. "Göndericek verim bitti"
  |                         |
  |<--- ACK (ack=501) ------|   2. "Tamam, aldım" (Server hala gönderebilir)
  |                         |
  |<--- FIN (seq=700) ------|   3. "Ben de bitirdim"
  |                         |
  |---- ACK (ack=701) ----->|   4. "Tamam, bağlantı kapandı"
  |                         |
  [TIME_WAIT - 2*MSL]          Client son ACK'in kaybolma ihtimaline
                                karşı bir süre bekler
:::

#### TCP vs UDP: Detaylı Karşılaştırma

:::code[text]{title="Paket Yapısı Karşılaştırması"}
TCP Segment Header (20-60 byte):
┌─────────────────┬─────────────────┐
│  Source Port     │  Dest Port      │  ← Hangi uygulamadan, hangi uygulamaya
├─────────────────┴─────────────────┤
│         Sequence Number           │  ← Paket sırası (sıralama için)
├───────────────────────────────────┤
│      Acknowledgment Number        │  ← Hangi paketi aldığını onaylar
├──────┬───────────┬────────────────┤
│Offset│  Flags    │    Window      │  ← SYN, ACK, FIN flag'leri
├──────┴───────────┴────────────────┤
│   Checksum      │  Urgent Ptr     │
└───────────────────────────────────┘

UDP Datagram Header (8 byte - çok daha basit!):
┌─────────────────┬─────────────────┐
│  Source Port     │  Dest Port      │
├─────────────────┼─────────────────┤
│    Length        │   Checksum      │
└─────────────────┴─────────────────┘
:::

:::deha-tip
TCP header'ı 20-60 byte, UDP header'ı sadece 8 byte. Bu "overhead" farkı, yüksek frekanslı veri gönderiminde (online oyun: saniyede 60+ paket) büyük fark yaratır. Her pakete 20 byte ekstra eklemek, saniyede binlerce paketle çarpıldığında ciddi bant genişliği kaybıdır.
:::

### DNS Resolution Süreci (Detaylı)

Bir domain adını IP adresine çevirmek, sandığından daha karmaşık bir süreçtir:

:::code[text]{title="DNS Resolution Akışı"}
Kullanıcı: "google.com'un IP adresi ne?"

1. Browser Cache     → Daha önce çözdüysem, cached IP'yi kullan (TTL süresi içinde)
     ↓ (bulamadı)
2. OS Cache          → İşletim sistemi DNS cache'ine bak
     ↓ (bulamadı)
3. Router Cache      → Ev/ofis router'ının cache'ine bak
     ↓ (bulamadı)
4. ISP DNS Resolver  → Türk Telekom / Vodafone'un DNS sunucusu
     ↓ (bulamadı)
5. Root DNS Server   → "Bilmiyorum ama .com'un nameserver'ını biliyorum"
     ↓
6. TLD DNS Server    → ".com nameserver: google.com'un NS kaydı şurada"
     ↓
7. Authoritative NS  → "google.com = 142.250.185.206" (gerçek cevap)
     ↓
8. Response geri gelir → Her aracı cache'ler (TTL süresince)
:::

:::code[bash]{title="DNS Çözümleme Pratiği - Terminalde Dene"}
# Basit DNS sorgusu
$ nslookup google.com
Server:  8.8.8.8
Address: 8.8.8.8#53

Non-authoritative answer:
Name:    google.com
Address: 142.250.185.206

# Detaylı DNS sorgusu (tüm adımları gör)
$ dig google.com +trace
; <<>> DiG 9.18.12 <<>> google.com +trace
.                  518400  IN  NS  a.root-servers.net.  ← Root server
com.               172800  IN  NS  a.gtld-servers.net.  ← TLD server
google.com.        172800  IN  NS  ns1.google.com.      ← Authoritative
google.com.        300     IN  A   142.250.185.206       ← Sonuç!

# Farklı DNS sunucusu ile sorgula
$ nslookup google.com 1.1.1.1    # Cloudflare DNS
$ nslookup google.com 8.8.8.8    # Google DNS
:::

### HTTP Request/Response Döngüsü

DNS çözümlendi, TCP bağlantısı kuruldu. Şimdi asıl veri transferi başlıyor:

:::code[text]{title="HTTP Request/Response Döngüsü (Detaylı)"}
Client (Tarayıcı)                        Server (Web Sunucusu)
     |                                        |
     |  -------- HTTP Request -------->        |
     |  GET /index.html HTTP/1.1               |
     |  Host: www.example.com                  |
     |  User-Agent: Chrome/120.0               |
     |  Accept: text/html                      |
     |  Accept-Language: tr-TR,tr;q=0.9        |
     |  Accept-Encoding: gzip, deflate, br     |
     |  Connection: keep-alive                 |
     |  Cookie: session=abc123                 |
     |                                        |
     |                            [Sunucu isteği işler]
     |                            [Dosyayı bulur]
     |                            [HTML'i hazırlar]
     |                                        |
     |  <------- HTTP Response --------        |
     |  HTTP/1.1 200 OK                        |
     |  Content-Type: text/html; charset=utf-8 |
     |  Content-Length: 5421                    |
     |  Cache-Control: max-age=3600            |
     |  Content-Encoding: gzip                 |
     |  Set-Cookie: session=abc123; HttpOnly   |
     |                                        |
     |  <!DOCTYPE html>                        |
     |  <html>...</html>                       |
     |                                        |
:::

:::code[bash]{title="curl ile HTTP Request/Response Detayını Gör"}
# -v flag'i ile tüm detayları göster
$ curl -v https://httpbin.org/get 2>&1

*   Trying 34.227.213.82:443...          ← IP adresi çözümlendi
* Connected to httpbin.org (34.227.213.82) port 443  ← TCP bağlantısı kuruldu
* TLS 1.3 (OUT), TLS handshake          ← TLS handshake başladı
* SSL connection using TLS_AES_256_GCM_SHA384  ← Şifreleme seçildi
> GET /get HTTP/2                         ← HTTP Request gönderildi
> Host: httpbin.org
> User-Agent: curl/8.1.2
> Accept: */*
>
< HTTP/2 200                              ← HTTP Response alındı
< content-type: application/json
< content-length: 256
<
{
  "headers": {
    "Host": "httpbin.org",
    "User-Agent": "curl/8.1.2"
  },
  "origin": "85.96.xxx.xxx",              ← Senin IP adresin
  "url": "https://httpbin.org/get"
}

# Sadece response header'larını göster
$ curl -I https://example.com

# POST request ile JSON gönder
$ curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "Ali", "role": "developer"}'

# Redirect'leri takip et
$ curl -L -v http://github.com 2>&1 | head -20
# HTTP 301 → https://github.com (HTTP'den HTTPS'e yönlendirme)
:::

### TLS Handshake (HTTPS)

Modern web'de neredeyse tüm trafik HTTPS üzerinden akar. TLS katmanı TCP'nin üstüne eklenir:

:::code[text]{title="TLS 1.3 Handshake (Basitleştirilmiş)"}
Client                                 Server
  |                                      |
  |--- ClientHello ------------------>   |
  |    (desteklenen cipher suite'lar,    |
  |     key share, supported versions)   |
  |                                      |
  |<-- ServerHello + Certificate -----   |
  |    (seçilen cipher suite,            |
  |     server key share,               |
  |     server sertifikası)              |
  |                                      |
  [Client sertifikayı doğrular]          |
  [CA chain kontrolü yapılır]            |
  [Ortak session key hesaplanır]         |
  |                                      |
  |--- Finished (encrypted) -------->   |
  |                                      |
  |<-- Finished (encrypted) ---------   |
  |                                      |
  |===== ŞİFRELİ VERİ TRANSFERİ =====  |
:::

:::code[text]{title="HTTP vs HTTPS Bağlantı Süresi Karşılaştırması"}
HTTP Bağlantısı:
  DNS Lookup:      ~50ms
  TCP Handshake:   ~30ms (1 RTT)
  HTTP Request:    ~30ms
  TOPLAM:          ~110ms

HTTPS Bağlantısı:
  DNS Lookup:      ~50ms
  TCP Handshake:   ~30ms (1 RTT)
  TLS Handshake:   ~30ms (TLS 1.3 = 1 RTT)
  HTTP Request:    ~30ms
  TOPLAM:          ~140ms (+30ms güvenlik maliyeti)

NOT: TLS 1.2'de handshake 2 RTT sürerdi (+60ms).
     TLS 1.3 bunu 1 RTT'ye düşürdü.
     0-RTT resumption ile tekrar bağlantılarda 0 ek maliyet!
:::

### Katman 3: Ağ Katmanı (Network Layer)

:::concept[IP (Internet Protocol)]
IP, verilerin ağ üzerinde yönlendirilmesini (routing) sağlar. Her cihaza benzersiz bir IP adresi atar.

**Türkçe karşılığı:** İnternet Protokolü
**Ne işe yarar:** Veri paketlerinin doğru hedefe ulaşmasını sağlar (yönlendirme)
**Gerçek hayat benzetmesi:** Mektubun üzerindeki adres gibi - postane bu adrese bakarak mektubu doğru yere yönlendirir
:::

:::code[text]{title="IP Adresi Formatları"}
IPv4: 192.168.1.1       → 32 bit, ~4.3 milyar adres (tükeniyor!)
IPv6: 2001:db8::1       → 128 bit, 340 undecillion adres (yeterli)

Özel IP aralıkları (internete çıkmaz):
10.0.0.0/8              → Büyük ağlar
172.16.0.0/12           → Orta ağlar
192.168.0.0/16          → Ev/küçük ofis ağları
127.0.0.1               → Localhost (kendi bilgisayarın)
:::

### Katman 2: Veri Bağlantı Katmanı (Data Link Layer)

Bu katman, aynı yerel ağdaki cihazlar arasında veri iletimini sağlar. MAC adresleri burada kullanılır. Ethernet ve Wi-Fi bu katmanda çalışır.

### Katman 1: Fiziksel Katman (Physical Layer)

Verilerin fiziksel ortamda (kablolar, fiber optik, radyo dalgaları) iletilmesini sağlar. Bit'lerin elektrik sinyallerine veya ışık darbelerine dönüştürülmesi burada yapılır.

## HTTP Versiyonları: 1.1 → 2 → 3

:::code[text]{title="HTTP Versiyonları Karşılaştırması"}
HTTP/1.1 (1997):
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Request 1│  │ Request 2│  │ Request 3│  ← Her istek sırayla (Head-of-Line Blocking)
│  ████    │  │  ████    │  │  ████    │  ← Önceki bitmeden sonraki başlamaz
└──────────┘  └──────────┘  └──────────┘
|____100ms____|____100ms____|____100ms____| = 300ms toplam

HTTP/2 (2015):
┌──────────┬──────────┬──────────┐
│ Request 1│ Request 2│ Request 3│  ← Aynı TCP bağlantısında multiplexing
│  ████    │  ████    │  ████    │  ← Paralel gönderilebilir
└──────────┴──────────┴──────────┘
|____________100ms________________| = 100ms toplam

HTTP/3 (2022) - QUIC tabanlı:
┌──────────┬──────────┬──────────┐
│ Request 1│ Request 2│ Request 3│  ← UDP üzerinde, 0-RTT bağlantı
│  ████    │  ████    │  ████    │  ← Paket kaybı sadece o stream'i etkiler
└──────────┴──────────┴──────────┘
|____________80ms_________________| = Daha hızlı (TCP handshake yok)
:::

:::deha-tip
HTTP/2'nin en büyük yeniliği **multiplexing**: tek TCP bağlantısında birden fazla request paralel gönderilebilir. HTTP/3 ise TCP'yi tamamen bırakıp UDP tabanlı QUIC protokolünü kullanır. Google, YouTube, Gmail zaten HTTP/3 kullanıyor. `curl -I` ile bir sitenin HTTP versiyonunu kontrol edebilirsin.
:::

## Veri Bir Katmandan Nasıl Geçer?

:::concept[Encapsulation (İng: Encapsulation)]
Her katman, üst katmandan gelen veriye kendi başlık bilgisini (header) ekler. Bu işleme encapsulation (kapsülleme) denir.

**Türkçe karşılığı:** Kapsülleme
**Ne işe yarar:** Her katman sadece kendi göreviyle ilgilenir, üst katmanların verisiyle uğraşmaz
**Gerçek hayat benzetmesi:** Bir mektup: yazıyı yaz → zarfa koy → adres yaz → posta kutusuna at → postacı al
:::

:::code[text]{title="Encapsulation Süreci"}
[Uygulama]  HTTP Request (GET /index.html)
     ↓
[Taşıma]    TCP Header + HTTP Data = Segment
     ↓
[Ağ]        IP Header + Segment = Packet (Paket)
     ↓
[Veri Bağ]  Frame Header + Packet + Frame Trailer = Frame
     ↓
[Fiziksel]  Bit dizisi → Elektrik/Işık sinyalleri
:::

## Port Kavramı

:::concept[Port (İng: Port)]
Port, bir bilgisayardaki belirli bir uygulamayı tanımlayan sayısal bir adrestir (0-65535).

**Türkçe karşılığı:** Port / Bağlantı Noktası
**Ne işe yarar:** Aynı IP adresindeki farklı uygulamaları ayırt eder
**Gerçek hayat benzetmesi:** IP adresi binanın adresi, port ise kat/daire numarası
:::

:::code[text]{title="Yaygın Port Numaraları (Bunları Ezberle!)"}
80    → HTTP
443   → HTTPS
22    → SSH
21    → FTP
25    → SMTP (email gönderme)
53    → DNS
3000  → Yaygın geliştirme portu (Node.js, React dev server)
5173  → Vite dev server
5432  → PostgreSQL
3306  → MySQL
27017 → MongoDB
6379  → Redis
8000  → Yaygın API portu (FastAPI, Django)
8080  → Alternatif HTTP portu
:::

:::tip
Developer olarak en sık 80, 443, 3000, 5173, 5432, 8000 portlarını kullanacaksın. Bunları gördüğünde anında ne olduğunu bilmelisin.
:::

## Wireshark ile Paket Analizi (Simülasyon)

Gerçek bir TCP bağlantısının Wireshark çıktısı şöyle görünür:

:::code[text]{title="Wireshark Benzeri Çıktı: google.com'a Bağlantı"}
No.  Time     Source          Dest            Protocol  Info
---  ----     ------          ----            --------  ----
1    0.000    192.168.1.5     8.8.8.8         DNS       Standard query A google.com
2    0.023    8.8.8.8         192.168.1.5     DNS       Response: A 142.250.185.206
3    0.024    192.168.1.5     142.250.185.206 TCP       SYN [Seq=0]
4    0.055    142.250.185.206 192.168.1.5     TCP       SYN-ACK [Seq=0, Ack=1]
5    0.055    192.168.1.5     142.250.185.206 TCP       ACK [Seq=1, Ack=1]
6    0.056    192.168.1.5     142.250.185.206 TLS       Client Hello
7    0.087    142.250.185.206 192.168.1.5     TLS       Server Hello, Certificate
8    0.088    192.168.1.5     142.250.185.206 TLS       Finished
9    0.118    142.250.185.206 192.168.1.5     TLS       Finished
10   0.119    192.168.1.5     142.250.185.206 HTTP      GET / HTTP/2
11   0.156    142.250.185.206 192.168.1.5     HTTP      HTTP/2 200 OK (text/html)

Timeline:
0ms    - DNS sorgusu gönderildi
23ms   - DNS cevabı alındı (IP öğrenildi)
24ms   - TCP SYN gönderildi
55ms   - TCP bağlantısı kuruldu (3-way handshake tamamlandı)
56ms   - TLS handshake başladı
118ms  - TLS handshake tamamlandı (şifreli kanal hazır)
119ms  - HTTP GET isteği gönderildi
156ms  - HTTP response alındı (sayfa verileri geldi)
:::

Bu çıktıdan önemli gözlemler:
- DNS çözümleme 23ms sürdü (cached olabilir)
- TCP handshake 31ms sürdü (1 RTT = sunucu uzaklığı)
- TLS handshake 62ms sürdü (2 RTT, TLS 1.2 olabilir)
- Toplam "ilk byte'a kadar" süre: ~156ms

## Network Debugging: Gerçek Hayat Senaryoları

:::code[bash]{title="Senaryo 1: 'Site Yavaş' Şikayeti - Sorun Nerede?"}
# Adım 1: DNS mi sorun?
$ time nslookup slow-site.com
# Eğer > 500ms → DNS sunucu sorunlu. DNS değiştir (1.1.1.1 veya 8.8.8.8)

# Adım 2: Sunucuya ulaşabiliyor muyuz?
$ ping slow-site.com
# Eğer timeout → Sunucu kapalı veya firewall engelliyor
# Eğer latency > 200ms → Sunucu coğrafi olarak uzak

# Adım 3: Hangi aşama yavaş?
$ curl -w "DNS: %{time_namelookup}s\nTCP: %{time_connect}s\nTLS: %{time_appconnect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" -o /dev/null -s https://slow-site.com

# Çıktı örneği:
# DNS:  0.050s    ← Normal
# TCP:  0.180s    ← Normal (uzak sunucu)
# TLS:  0.380s    ← Normal
# TTFB: 2.500s    ← SORUN BURADA! Sunucu 2 saniye düşünüyor
# Total: 2.800s

# Sonuç: Sorun network'te değil, sunucu tarafında (yavaş veritabanı sorgusu?)
:::

:::code[bash]{title="Senaryo 2: 'API Çağrısı Timeout Oluyor'"}
# Adım 1: Port açık mı kontrol et
$ nc -zv api.example.com 443
# Connection to api.example.com 443 port [tcp/https] succeeded!

# Adım 2: SSL sertifikası geçerli mi?
$ curl -vI https://api.example.com 2>&1 | grep -E "SSL|certificate|expire"
# SSL certificate verify ok.
# expire date: Mar 15 2027

# Adım 3: DNS çözümlemesi doğru mu?
$ nslookup api.example.com
# Farklı IP dönüyorsa → DNS değişmiş, /etc/hosts kontrolü yap
:::

## Pratik: URL'den Sayfaya Tam Yolculuk

:::interview
**Mülakat Sorusu:** "Tarayıcıya google.com yazdığında ne olur?"

**Beklenen cevap (özetlenmiş):**

1. **DNS Resolution:** Tarayıcı, google.com'un IP adresini bulmak için DNS sunucusuna sorar
2. **TCP Handshake:** IP adresi bulunduktan sonra 3-way handshake ile TCP bağlantısı kurulur
3. **TLS Handshake:** HTTPS ise, şifreli bağlantı kurulur (ek 1-2 RTT)
4. **HTTP Request:** Tarayıcı GET / HTTP/1.1 isteği gönderir
5. **Server Processing:** Sunucu isteği işler, HTML yanıtı hazırlar
6. **HTTP Response:** Sunucu 200 OK ile HTML'i gönderir
7. **Rendering:** Tarayıcı HTML'i parse eder, CSS ve JS dosyalarını indirir, DOM oluşturur ve sayfayı render eder

Bu konuyu bir sonraki derste (DNS) ve üçüncü derste (tarayıcı rendering) çok daha detaylı ele alacağız.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Ping ve Traceroute ile Network Keşfi

Terminali aç ve şu komutları sırayla çalıştır:

```bash
# 1. Ping ile latency ölç
ping google.com        # Ctrl+C ile durdur, ortalama latency'yi not et
ping -c 5 google.com   # 5 paket gönder (Mac/Linux)
ping -n 5 google.com   # 5 paket gönder (Windows)

# 2. Farklı sitelerin latency'sini karşılaştır
ping cloudflare.com    # Genelde düşük (CDN)
ping amazon.com        # ABD'deki sunucu (daha yüksek)

# 3. Veri yolunu takip et
tracert google.com     # Windows
traceroute google.com  # Mac/Linux

# Çıktıda her satır bir "hop" = bir router
# İlk hop: Ev router'ın (192.168.x.x)
# Sonraki: ISP router'ları
# Son: Google sunucusu
```

**Beklenen sonuç:** Türkiye'den google.com'a genelde 10-30ms latency, 8-15 hop olmalı. Cloudflare gibi CDN'ler daha az hop'ta ulaşılır.

### Alistirma 2: HTTP Header Analizi

```bash
# 1. curl ile HTTP header'larını incele
curl -I https://github.com
# Dikkat et: content-type, server, x-github-request-id, strict-transport-security

curl -I https://google.com
# Dikkat et: HTTP/2, server: gws, cache-control, alt-svc (QUIC desteği)

# 2. Detaylı bağlantı bilgilerini gör
curl -v https://example.com 2>&1 | head -25
# TLS versiyonu, cipher suite, sertifika bilgilerini not et

# 3. Yönlendirmeleri takip et
curl -L -v http://github.com 2>&1
# HTTP → HTTPS yönlendirmesini gör (301 Moved Permanently)

# 4. Timing bilgilerini ölç
curl -w "\n\
DNS Lookup:    %{time_namelookup}s\n\
TCP Connect:   %{time_connect}s\n\
TLS Handshake: %{time_appconnect}s\n\
TTFB:          %{time_starttransfer}s\n\
Total:         %{time_total}s\n" \
  -o /dev/null -s https://google.com
```

**Beklenen sonuç:** DNS lookup < 100ms, TCP connect < 100ms, TLS < 200ms. Bu süreleri farklı siteler için karşılaştırarak hangi aşamanın darboğaz olduğunu belirleyebilmelisin.

### Alistirma 3: DNS Lookup ve Cache Analizi

```bash
# 1. Farklı DNS sunucularını karşılaştır
nslookup google.com              # Varsayılan DNS (ISP)
nslookup google.com 8.8.8.8     # Google DNS
nslookup google.com 1.1.1.1     # Cloudflare DNS

# 2. DNS çözümleme süresini ölç
# İlk sorgu (cache'de yok):
time nslookup example.com
# İkinci sorgu (artık cache'de):
time nslookup example.com
# Süre farkını gör!

# 3. DNS kayıt tiplerini sorgula
nslookup -type=MX google.com    # Mail sunucuları
nslookup -type=NS google.com    # Name server'lar
nslookup -type=TXT google.com   # SPF, DKIM vs.
nslookup -type=CNAME www.github.com  # Alias

# 4. Tarayıcıda F12 → Network tab → bir siteye gir
# İlk request'in "Timing" bölümünü incele
# DNS Lookup, Initial Connection, TLS Handshake sürelerini not et
# Sayfayı yenile (Ctrl+R) ve sürelerin nasıl değiştiğini gör (cache etkisi)
```

**Beklenen sonuç:** İkinci DNS sorgusunun ilkinden çok daha hızlı olduğunu görmelisin (cache etkisi). MX kayıtlarını sorgulayarak bir domain'in email sunucularını bulabilmelisin.
:::

:::knowledge-check
type: multiple_choice
question: "TCP 3-way handshake'in doğru sırası hangisidir?"
options:
  - "ACK → SYN → SYN-ACK"
  - "SYN → SYN-ACK → ACK"
  - "SYN → ACK → SYN-ACK"
  - "SYN-ACK → SYN → ACK"
correct: 1
explanation: "TCP bağlantısı SYN → SYN-ACK → ACK sırasıyla kurulur. İstemci SYN gönderir, sunucu SYN-ACK ile hem onaylar hem kendi bağlantı isteğini gönderir, istemci ACK ile tamamlar."
:::

:::knowledge-check
type: multiple_choice
question: "Video streaming için neden TCP yerine UDP tercih edilir?"
options:
  - "UDP daha güvenlidir"
  - "UDP kayıp paketleri tekrar gönderir"
  - "UDP daha hızlıdır çünkü güvenilirlik kontrolü yapmaz, birkaç kayıp kare fark edilmez"
  - "TCP video desteklemez"
correct: 2
explanation: "Video streaming'de hız, güvenilirlikten önemlidir. Birkaç kayıp video karesi fark edilmez ama TCP'nin yeniden gönderme mekanizması gecikmeye neden olur. Bu yüzden UDP tercih edilir."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6

### Prompt Ornekleri

**1. Konuyu Derinlemesine Anla:**
> "TCP/IP katman modelini bir mektup gonderme analojisiyle acikla. Her katmanda (Application, Transport, Network, Link) neler oluyor? Her katmanin eklediği header bilgisi ne ise yariyor?"

*Neden:* Soyut network kavramlarini somut orneklerle anlamak, encapsulation surecini kalici hale getirir

**2. Pratik Uygulama:**
> "curl ile bir HTTP request attigimda arka planda neler oluyor? DNS cozumlemesinden TCP 3-way handshake'e kadar adim adim anlat ve her adimda hangi port ve protokol kullanildigini belirt."

*Follow-up:* "Ayni istegi HTTPS ile gonderseydim fark ne olurdu? TLS handshake adimlarini da ekle."

**3. Mukemmellik Icin:**
> "Bir video streaming uygulamasi tasarliyorum. TCP yerine UDP secmemin teknik nedenlerini, paket kaybi durumunda ne oldugunu ve QUIC protokolunun bu sorunu nasil cozdugunu karsilastirmali anlat."

### Pair Programming Ipucu
Network debugging yaparken AI'a DevTools Network tab ciktini yapistir ve sor: "Bu request'in timing breakdown'ini analiz et. DNS lookup, TCP handshake ve TTFB surelerinden hangisi darbogazda? Nasil optimize ederim?"
:::

:::must-note
- TCP/IP 5 katman sırası: Physical → Data Link → Network → Transport → Application
- TCP = güvenilir (3-way handshake: SYN → SYN-ACK → ACK), UDP = hızlı ama güvenilir değil
- Encapsulation sırası: Data → Segment (TCP header eklenir) → Packet (IP header eklenir) → Frame → Bits
- Port numaraları: HTTP=80, HTTPS=443, SSH=22, DNS=53, FTP=21, SMTP=25
- Geliştirici portları: Node.js/React=3000, Vite=5173, PostgreSQL=5432, MySQL=3306, Redis=6379
- IP adresi = binanın adresi, Port = daire numarası (aynı IP'de farklı uygulamalar farklı portlarda çalışır)
- IPv4 = 32 bit (~4.3 milyar, tükeniyor), IPv6 = 128 bit (yeterli)
- Özel IP aralıkları: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1 (localhost)
- TCP paket kaybında tekrar gönderir (reliable), UDP görmezden gelir (fast)
- URL yolculuğu sırası: DNS Resolution → TCP Handshake → TLS Handshake → HTTP Request → Response → Rendering
:::

:::senior-learns
Bir Senior Developer veya CTO, internet ve TCP/IP konusunu öğrenirken şu yaklaşımı benimser:

1. **RFC dökümanlarından öğrenir** - RFC 793 (TCP), RFC 791 (IP), RFC 768 (UDP) gibi orijinal spesifikasyonları okur. "Bir blog yazısı sana özeti verir, RFC sana gerçeği verir" prensibiyle hareket eder.
2. **Wireshark ile gerçek trafiği yakalar** - Kendi bilgisayarında Wireshark açıp bir web sitesine girdiğinde oluşan TCP handshake'i, DNS sorgusunu ve HTTP request/response'ları packet seviyesinde inceler. Teoriyi gözle görür.
3. **Kendi TCP server/client'ını yazar** - Python'da `socket` modülü veya Node.js'te `net` modülü ile basit bir TCP echo server yazar. Raw socket programlama yaparak protokolün nasıl çalıştığını derinden anlar.
4. **Production sorunlarından öğrenir** - "Bu API neden 3 saniye sürüyor?" sorusuna cevap ararken tcpdump, netstat, ss gibi araçlarla network katmanını analiz eder. Her production incident bir öğrenme fırsatıdır.
5. **Network tab'ını günlük iş akışına entegre eder** - Her gün DevTools Network tab'ını açık tutar. Waterfall grafiğini okuyarak DNS, TCP, TLS ve TTFB (Time to First Byte) sürelerini ayrı ayrı analiz eder.
6. **Öğrendiğini dokümante eder ve anlatır** - Takım içi tech talk yapar, internal wiki'ye yazar. "Eğer birine anlatamazsan, gerçekten anlamamışsındır" prensibi.

**Profesyonel Mindset:** "Networking bilgisi, bir developer'ın en güçlü debug silahıdır. Production'da bir timeout hatası aldığında, TCP handshake ve connection pooling'i anlayan mühendis sorunu dakikalar içinde izole eder. Anlamayan ise saatlerce application kodunda hata arar. Katmanları bil, problemi doğru katmanda çöz."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Protocol** (proh-tuh-kol) → Protokol
   *"TCP is a connection-oriented protocol that ensures reliable data delivery."*

2. **Handshake** (hænd-ʃeɪk) → El sıkışma / Bağlantı kurma
   *"The TCP three-way handshake establishes a connection before data transfer."*

3. **Packet** (pæk-ɪt) → Paket / Veri paketi
   *"Each packet contains a header with routing information and a payload with actual data."*

4. **Latency** (leɪ-tən-si) → Gecikme süresi
   *"High latency causes slow page loads and poor user experience."*

5. **Port** (pɔːrt) → Port / Bağlantı noktası
   *"The web server listens on port 443 for HTTPS connections."*

**Okuma Egzersizi:** MDN'de "How does the Internet work?" makalesinin ilk 3 paragrafını İngilizce oku: https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/How_does_the_Internet_work

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "İnternet temelleri dersini tamamladım"
→ Örnek: `docs: complete internet fundamentals lesson notes`
:::

:::external-resource
- 📺 **freeCodeCamp:** "Computer Networking Fundamentals" (12 saat, YouTube, ücretsiz)
- 📖 **MDN Web Docs:** "How does the Internet work?" (İngilizce, ücretsiz)
- 🎮 **How DNS Works:** howdns.works (interaktif çizgi roman, ücretsiz)
- 📖 **Google/Coursera:** "The Bits and Bytes of Computer Networking" (ücretsiz audit)
:::
