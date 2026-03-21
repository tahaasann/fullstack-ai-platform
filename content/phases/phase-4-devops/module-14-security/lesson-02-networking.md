---
title: "Networking ve Güvenli İletişim: OSI, TLS, SSH"
id: "mod-14-security/lesson-02"
estimated_minutes: 60
order: 2
tags: ["networking", "osi-model", "tcp", "udp", "tls", "ssl", "ssh", "firewall", "vpn", "mtls", "certificate"]
prerequisites: ["mod-14-security/lesson-01"]
---

# Networking ve Güvenli İletişim: OSI, TLS, SSH

:::realworld
Her gün milyarlarca HTTPS isteği yapılıyor ve her biri TLS handshake ile başlıyor. Bir e-ticaret sitesinde kredi kartı bilgini girdiğinde, verinin güvenle iletilmesini sağlayan şey networking ve kriptografi bilgisidir. 2014'teki Heartbleed bug'ı, OpenSSL'deki tek bir hata ile milyonlarca sunucunun private key'lerini ifşa etti. Bu derste network'ün nasıl çalıştığını, verilerin nasıl güvenle iletildiğini ve modern güvenli iletişim protokollerini öğreneceksin.
:::

## OSI Model: Network'ün 7 Katmanı

:::concept[OSI Model (İng: Open Systems Interconnection Model)]
OSI Model, network iletişimini 7 soyut katmana ayıran bir referans modelidir. Her katman belirli bir sorumluluğa sahiptir ve bir üst katmana hizmet sunar.

**Turkce karsiligi:** Açık Sistemler Arabaglanti Modeli
**Ne ise yarar:** Network iletişiminin nasıl çalıştığını anlamak ve sorunları doğru katmanda çözmek için kullanılır
**Gercek hayat benzetmesi:** Posta sistemi gibi - mektup yazarsın (Application), zarfa koyarsın (Presentation), posta kodunu yazarsın (Session), posta kutusuna bırakırsın (Transport), postacı alır (Network), kamyona yükler (Data Link), yolda gider (Physical)
:::

:::comparison
| Katman | Isim | Protokol Ornekleri | Ne Yapar? | Developer Icin |
|--------|------|-------------------|-----------|----------------|
| 7 | **Application** | HTTP, HTTPS, DNS, FTP, SMTP, WebSocket | Kullanıcı uygulamalarına ağ erişimi sağlar | API tasarımı, REST/GraphQL |
| 6 | **Presentation** | SSL/TLS, JPEG, UTF-8, JSON | Veri formatı dönüşümü, şifreleme | JSON parse, encoding |
| 5 | **Session** | NetBIOS, RPC, TLS session | Oturum yönetimi, senkronizasyon | WebSocket, session management |
| 4 | **Transport** | TCP, UDP | Uçtan uca veri iletimi, port numaraları | Port seçimi, connection pooling |
| 3 | **Network** | IP, ICMP, ARP | Routing, IP adresleme | Subnet, CIDR, VPC yapılandırma |
| 2 | **Data Link** | Ethernet, Wi-Fi (802.11), MAC | Frame'leme, hata tespiti, MAC adresleme | Genelde dokunmazsın |
| 1 | **Physical** | Kablo, Fiber optik, Radio | Fiziksel sinyal iletimi | Kablo taktığından emin ol :) |

**Hatırlatma mnemonik:** "**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing" (7'den 1'e)
:::

:::english
**TCP/IP Model vs OSI Model:**

The TCP/IP model is a simplified 4-layer model that maps to OSI:
- **Application Layer** (OSI 5-7): HTTP, DNS, SMTP, FTP
- **Transport Layer** (OSI 4): TCP, UDP
- **Internet Layer** (OSI 3): IP, ICMP
- **Network Access Layer** (OSI 1-2): Ethernet, Wi-Fi

In practice, developers work mostly with the TCP/IP model. The OSI model is used as a reference for understanding and troubleshooting.
:::

:::tip
Full-stack developer olarak hangi katmanları bilmen gerekiyor? Layer 7 (HTTP/HTTPS), Layer 4 (TCP/UDP port'ları) ve Layer 3 (IP, subnet, routing). Mülakatlar için OSI modelinin 7 katmanını ezbere bil, ama günlük işinde Layer 4-7 arası yeterli.
:::

## TCP vs UDP

:::concept[TCP (İng: Transmission Control Protocol)]
TCP, güvenilir, sıralı ve hata kontrollü veri iletimi sağlayan connection-oriented bir transport protokolüdür.

**Turkce karsiligi:** İletim Kontrol Protokolü
**Ne ise yarar:** Verinin eksiksiz ve doğru sırada ulaşmasını garanti eder
**Gercek hayat benzetmesi:** Taahhütlü posta gibi - gönderdiğin her mektubun ulaştığından emin olursun, kaybolursa tekrar gönderilir
:::

:::concept[UDP (İng: User Datagram Protocol)]
UDP, bağlantısız (connectionless) ve hızlı bir transport protokolüdür. Veri iletimini garanti etmez ama çok düşük gecikme sağlar.

**Turkce karsiligi:** Kullanıcı Datagram Protokolü
**Ne ise yarar:** Düşük gecikme gerektiren uygulamalarda (video, oyun) hızlı veri iletimi sağlar
**Gercek hayat benzetmesi:** Normal posta gibi - mektup gönderirsin ama ulaşıp ulaşmadığını bilmezsin. Hızlıdır ama garanti yoktur
:::

:::comparison
| Ozellik | TCP | UDP |
|---------|-----|-----|
| Baglanti | Connection-oriented (3-way handshake) | Connectionless |
| Guvenilirlik | Guaranteed delivery (ACK/retransmit) | Best effort (kayıp olabilir) |
| Siralama | Sıralı teslim (ordered) | Sırasız (unordered) |
| Hiz | Daha yavaş (overhead) | Daha hızlı (minimal overhead) |
| Flow control | Var (window size) | Yok |
| Congestion control | Var | Yok |
| Header boyutu | 20-60 byte | 8 byte |
| Kullanim alanlari | HTTP, HTTPS, SSH, FTP, SMTP, database | DNS, video streaming, VoIP, gaming, IoT |

**Genel kural:** Veri kaybı kabul edilemezse TCP (web, email, dosya transferi). Hız kritikse ve kayıp tolere edilebilirse UDP (video call, online oyun, DNS lookup).
:::

### TCP Three-Way Handshake

:::code[text]{title="TCP 3-Way Handshake"}
Client                              Server
  |                                    |
  |  1. SYN (seq=100)                  |
  |  "Bağlantı kurmak istiyorum"       |
  | ---------------------------------> |
  |                                    |
  |  2. SYN-ACK (seq=300, ack=101)     |
  |  "Tamam, ben de hazırım"           |
  | <--------------------------------- |
  |                                    |
  |  3. ACK (seq=101, ack=301)         |
  |  "Harika, başlayalım!"             |
  | ---------------------------------> |
  |                                    |
  |  ===== Bağlantı kuruldu =====      |
  |  Veri iletimi başlayabilir          |
  |                                    |

# Connection Termination (4-way)
  |  FIN -->                           |  "Kapatmak istiyorum"
  |  <-- ACK                           |  "Anladım"
  |  <-- FIN                           |  "Ben de kapatıyorum"
  |  ACK -->                           |  "Tamam, kapatıldı"
:::

## Firewalls ve Network Güvenliği

:::concept[Firewall (İng: Firewall)]
Firewall, ağ trafiğini kurallara göre filtreleyen bir güvenlik sistemidir. İzin verilen trafiğe geçiş sağlar, izinsiz trafiği engeller.

**Turkce karsiligi:** Güvenlik Duvarı
**Ne ise yarar:** Ağa yetkisiz erişimi engeller, sadece izin verilen trafiğe izin verir
**Gercek hayat benzetmesi:** Bina güvenliği gibi - kimliği kontrol eder, yetkili olanı içeri alır, yetkisizi geri çevirir
:::

:::code[bash]{title="Linux iptables / ufw Firewall Kuralları"}
# UFW (Uncomplicated Firewall) - Ubuntu/Debian

# Firewall'u etkinleştir
sudo ufw enable

# Varsayılan: gelen trafiği engelle, çıkan trafiğe izin ver
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH'a izin ver (port 22)
sudo ufw allow 22/tcp

# HTTP ve HTTPS'e izin ver
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Belirli IP'den erişime izin ver
sudo ufw allow from 192.168.1.100 to any port 5432

# Kural listesini gör
sudo ufw status verbose

# Port aralığı
sudo ufw allow 6000:6007/tcp
:::

:::code[yaml]{title="AWS Security Group (Cloud Firewall)"}
# Terraform ile Security Group tanımı
resource "aws_security_group" "web_server" {
  name        = "web-server-sg"
  description = "Web server security group"
  vpc_id      = aws_vpc.main.id

  # Inbound: Sadece HTTP, HTTPS ve SSH
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]     # Herkesten HTTPS kabul et
  }

  ingress {
    description = "HTTP (redirect to HTTPS)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH from office only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["203.0.113.0/24"]  # Sadece ofis IP aralığı
  }

  # Outbound: Tüm çıkış trafiğine izin ver
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
:::

:::warning
SSH port'unu (22) tüm dünyaya açma (`0.0.0.0/0`)! Brute force saldırılarına maruz kalırsın. SSH'ı sadece bilinen IP'lerden erişime izin ver veya VPN arkasına al. Daha iyisi: SSH key-based authentication kullan ve password authentication'ı devre dışı bırak.
:::

## VPN (Virtual Private Network)

:::concept[VPN (İng: Virtual Private Network)]
VPN, internet üzerinden güvenli, şifreli bir tünel oluşturarak özel ağlara erişim sağlayan bir teknolojidir.

**Turkce karsiligi:** Sanal Özel Ağ
**Ne ise yarar:** İnternet trafiğini şifreler, uzaktan özel ağlara güvenli erişim sağlar
**Gercek hayat benzetmesi:** İki bina arasında yeraltı tüneli gibi - dışarıdan kimse tünelin içinde ne geçtiğini göremez
:::

:::comparison
| VPN Turu | Kullanim | Protokol | Ornek |
|----------|----------|----------|-------|
| **Site-to-Site** | İki ofis ağını birleştirir | IPSec | AWS VPN Gateway |
| **Remote Access** | Uzak çalışanlar ofis ağına bağlanır | OpenVPN, WireGuard | Employee VPN |
| **Cloud VPN** | Cloud VPC'ye güvenli bağlantı | IPSec/IKEv2 | AWS Client VPN |

**Modern tercih:** WireGuard - daha hızlı, daha basit ve daha güvenli. OpenVPN'e kıyasla çok daha az kod satırı (4000 vs 70000+), daha iyi performans.
:::

## SSH (Secure Shell)

:::concept[SSH (İng: Secure Shell)]
SSH, güvenli olmayan ağ üzerinden güvenli uzak erişim sağlayan bir kriptografik ağ protokolüdür. Telnet'in güvenli alternatifidir.

**Turkce karsiligi:** Güvenli Kabuk
**Ne ise yarar:** Sunuculara güvenli uzaktan erişim, dosya transferi ve port forwarding sağlar
**Gercek hayat benzetmesi:** Şifreli telefon hattı gibi - konuşmanı kimse dinleyemez ve karşı tarafın gerçekten o kişi olduğundan emin olursun
:::

:::code[bash]{title="SSH Temel Kullanım"}
# SSH key pair oluştur (Ed25519 önerilir - daha güvenli ve hızlı)
ssh-keygen -t ed25519 -C "developer@example.com"
# Alternatif: RSA (minimum 4096 bit)
ssh-keygen -t rsa -b 4096 -C "developer@example.com"

# Key dosyaları:
# ~/.ssh/id_ed25519       (private key - ASLA paylaşma!)
# ~/.ssh/id_ed25519.pub   (public key - sunucuya kopyala)

# Public key'i sunucuya kopyala
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server.com

# SSH ile bağlan
ssh user@server.com
ssh -p 2222 user@server.com    # Farklı port

# SCP ile dosya transferi
scp file.txt user@server.com:/home/user/
scp -r ./project user@server.com:/opt/  # Dizin kopyala

# SSH Tunnel (Port Forwarding)
# Local forwarding: Remote DB'ye local port üzerinden eriş
ssh -L 5432:db-server:5432 user@bastion.com
# Artık localhost:5432'ye bağlanınca remote DB'ye erişirsin

# Remote forwarding: Local servisi remote'dan eriş
ssh -R 8080:localhost:3000 user@server.com
# server.com:8080'e gelen istekler localhost:3000'e yönlendirilir

# SSH config dosyası (~/.ssh/config)
# Host production
#   HostName 203.0.113.10
#   User deploy
#   Port 2222
#   IdentityFile ~/.ssh/production_key
#   ForwardAgent yes
#
# Kullanım: ssh production
:::

:::code[bash]{title="SSH Server Hardening"}
# /etc/ssh/sshd_config ayarları

# Password authentication'ı kapat (sadece key ile giriş)
PasswordAuthentication no
PubkeyAuthentication yes

# Root login'i kapat
PermitRootLogin no

# Boş şifreyi engelle
PermitEmptyPasswords no

# Varsayılan portu değiştir (güvenlik through obscurity - ek önlem)
Port 2222

# İzin verilen kullanıcıları sınırla
AllowUsers deploy admin

# Login grace time (bağlantı kurma süresi)
LoginGraceTime 30

# Max authentication denemesi
MaxAuthTries 3

# X11 forwarding'i kapat (gereksizse)
X11Forwarding no

# Idle timeout
ClientAliveInterval 300
ClientAliveCountMax 2

# Servisi yeniden başlat
sudo systemctl restart sshd
:::

:::tip
SSH key'leri mutlaka passphrase ile koru! Passphrase olmadan private key'in çalınması durumunda saldırgan doğrudan tüm sunucularına erişebilir. `ssh-agent` kullanarak passphrase'i her seferinde yazma zahmetinden kurtulabilirsin.
:::

## SSL/TLS: Güvenli İletişim

:::concept[TLS (İng: Transport Layer Security)]
TLS, internet üzerindeki iletişimi şifreleyen bir kriptografik protokoldür. HTTPS, TLS üzerinde çalışan HTTP'dir. SSL, TLS'in eski ve güvensiz versiyonudur.

**Turkce karsiligi:** Taşıma Katmanı Güvenliği
**Ne ise yarar:** Client-server arasındaki tüm trafiği şifreler, verinin dinlenmesini ve değiştirilmesini engeller
**Gercek hayat benzetmesi:** Diplomatik kurye çantası gibi - içeriği sadece gönderen ve alıcı görebilir, yolda kimse açamaz ve değiştiremez
:::

### TLS Handshake (TLS 1.3)

:::code[text]{title="TLS 1.3 Handshake (Simplified)"}
Client                                  Server
  |                                        |
  |  1. ClientHello                        |
  |  - Desteklenen TLS versiyonları         |
  |  - Desteklenen cipher suite'ler         |
  |  - Client random                        |
  |  - Key share (ECDHE public key)         |
  | -------------------------------------> |
  |                                        |
  |  2. ServerHello                        |
  |  - Seçilen TLS versiyonu               |
  |  - Seçilen cipher suite                |
  |  - Server random                        |
  |  - Key share (ECDHE public key)         |
  |  + Certificate (sunucu sertifikası)     |
  |  + CertificateVerify (imza)             |
  |  + Finished                             |
  | <------------------------------------- |
  |                                        |
  |  3. Client doğrulama:                  |
  |  - Sertifika CA tarafından imzalı mı?  |
  |  - Sertifika süresi dolmamış mı?       |
  |  - Domain adı eşleşiyor mu?            |
  |  - Sertifika revoke edilmemiş mi?       |
  |                                        |
  |  4. Finished                           |
  |  (Master secret hesaplandı)             |
  | -------------------------------------> |
  |                                        |
  |  ===== Encrypted communication =====    |
  |  Artık tüm trafik AES ile şifreli      |
  |                                        |

# TLS 1.3: Handshake tek round-trip (1-RTT)
# TLS 1.2: İki round-trip gerekiyordu (2-RTT)
# TLS 1.3 daha hızlı VE daha güvenli
:::

:::comparison
| Ozellik | TLS 1.2 | TLS 1.3 |
|---------|---------|---------|
| Handshake | 2-RTT | 1-RTT (0-RTT resumption) |
| Cipher suites | Çok fazla (bazıları zayıf) | Sadece güvenli olanlar |
| Forward secrecy | Opsiyonel | Zorunlu (ECDHE) |
| RSA key exchange | Destekler | Kaldırıldı (güvensiz) |
| Performance | Yavaş handshake | Hızlı handshake |
| Guvenlik | İyi | Çok İyi |

**Kural:** Yeni projelerde TLS 1.3 kullan. TLS 1.2'yi destekle (eski client'lar için). TLS 1.0 ve 1.1 ASLA kullanma (güvensiz). SSL ASLA kullanma (broken).
:::

### Certificate (Sertifika) Yönetimi

:::concept[TLS Certificate (İng: TLS/SSL Certificate)]
TLS sertifikası, bir web sitesinin kimliğini doğrulayan ve public key'ini içeren dijital bir belgedir. Certificate Authority (CA) tarafından imzalanır.

**Turkce karsiligi:** Dijital Sertifika
**Ne ise yarar:** Web sitesinin gerçekten iddia ettiği site olduğunu kanıtlar ve güvenli iletişim için public key sağlar
**Gercek hayat benzetmesi:** Noterden onaylı kimlik belgesi gibi - noter (CA) kişinin (sitenin) kimliğini doğrulayıp belgeyi imzalar, herkes noterin imzasına güvenir
:::

:::code[bash]{title="Let's Encrypt ile Ücretsiz TLS Sertifikası"}
# Certbot kurulumu (Let's Encrypt client)
sudo apt-get install certbot python3-certbot-nginx

# Nginx için sertifika al ve otomatik yapılandır
sudo certbot --nginx -d myapp.com -d www.myapp.com

# Standalone mode (nginx yoksa)
sudo certbot certonly --standalone -d myapp.com

# Sertifika yenileme (otomatik cron job oluşturulur)
sudo certbot renew

# Sertifika bilgisini kontrol et
sudo certbot certificates

# Manuel yenileme testi (dry run)
sudo certbot renew --dry-run

# Sertifika dosyaları:
# /etc/letsencrypt/live/myapp.com/fullchain.pem  (sertifika + chain)
# /etc/letsencrypt/live/myapp.com/privkey.pem    (private key)
:::

:::code[javascript]{title="Node.js HTTPS Server"}
const https = require('https');
const fs = require('fs');
const express = require('express');

const app = express();

// TLS sertifika dosyalarını oku
const options = {
  cert: fs.readFileSync('/etc/letsencrypt/live/myapp.com/fullchain.pem'),
  key: fs.readFileSync('/etc/letsencrypt/live/myapp.com/privkey.pem'),

  // TLS yapılandırma (güvenlik)
  minVersion: 'TLSv1.2',              // Minimum TLS 1.2
  ciphers: [
    'TLS_AES_128_GCM_SHA256',           // TLS 1.3
    'TLS_AES_256_GCM_SHA384',           // TLS 1.3
    'ECDHE-RSA-AES128-GCM-SHA256',      // TLS 1.2
    'ECDHE-RSA-AES256-GCM-SHA384'       // TLS 1.2
  ].join(':'),
};

// HTTPS server oluştur
const server = https.createServer(options, app);
server.listen(443, () => {
  console.log('HTTPS server running on port 443');
});

// HTTP → HTTPS redirect
const http = require('http');
http.createServer((req, res) => {
  res.writeHead(301, { Location: `https://${req.headers.host}${req.url}` });
  res.end();
}).listen(80);
:::

:::code[nginx]{title="Nginx TLS Yapılandırması (Production-Ready)"}
server {
    listen 80;
    server_name myapp.com www.myapp.com;

    # HTTP → HTTPS yönlendirme
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myapp.com;

    # Sertifika dosyaları
    ssl_certificate     /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;

    # TLS yapılandırma
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # HSTS header (1 yıl)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # OCSP Stapling (sertifika doğrulama hızlandırma)
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/myapp.com/chain.pem;

    # SSL Session cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # Reverse proxy
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
:::

## mTLS (Mutual TLS)

:::concept[mTLS (İng: Mutual TLS / Two-Way TLS)]
mTLS, hem server'ın hem de client'ın birbirinin kimliğini sertifika ile doğruladığı TLS yapılandırmasıdır. Normal TLS'te sadece server'ın kimliği doğrulanır.

**Turkce karsiligi:** Karşılıklı TLS / İki Yönlü TLS
**Ne ise yarar:** Mikroservisler arası iletişimde her iki tarafın da yetkili olduğunu garanti eder
**Gercek hayat benzetmesi:** Diplomatik görüşme gibi - sadece ziyaretçi kimliğini göstermez, ev sahibi de kendi kimliğini gösterir. İki taraflı doğrulama.
:::

:::code[text]{title="TLS vs mTLS Karşılaştırma"}
Normal TLS (tek yönlü):
  Client -------> Server
  "Sertifikanı göster"  →  Server sertifika gösterir
  Client doğrular       →  ✅ Server gerçekten myapp.com
  Client herhangi biri olabilir (kimlik doğrulanmaz)

mTLS (karşılıklı):
  Client <------> Server
  Client: "Sertifikanı göster"  →  Server sertifika gösterir  →  ✅
  Server: "Sen de göster"       →  Client sertifika gösterir   →  ✅
  Her iki taraf da doğrulanmış. Yetkisiz client bağlanamaz.
:::

:::code[javascript]{title="Node.js mTLS Server ve Client"}
// ===== mTLS Server =====
const https = require('https');
const fs = require('fs');

const serverOptions = {
  cert: fs.readFileSync('server-cert.pem'),
  key: fs.readFileSync('server-key.pem'),
  ca: fs.readFileSync('ca-cert.pem'),     // Client sertifikalarını doğrulamak için CA
  requestCert: true,                       // Client sertifikası iste
  rejectUnauthorized: true                 // Geçersiz sertifikayı reddet
};

const server = https.createServer(serverOptions, (req, res) => {
  const clientCert = req.socket.getPeerCertificate();
  console.log('Client CN:', clientCert.subject.CN);
  res.end('mTLS connection successful!');
});

server.listen(443);


// ===== mTLS Client =====
const https = require('https');
const fs = require('fs');

const clientOptions = {
  hostname: 'api.myapp.com',
  port: 443,
  path: '/data',
  method: 'GET',
  cert: fs.readFileSync('client-cert.pem'),   // Client sertifikası
  key: fs.readFileSync('client-key.pem'),      // Client private key
  ca: fs.readFileSync('ca-cert.pem')           // Server CA doğrulama
};

const req = https.request(clientOptions, (res) => {
  res.on('data', (data) => console.log(data.toString()));
});

req.end();
:::

:::tip
mTLS en çok mikroservis mimarilerinde kullanılır. Kubernetes'te Istio veya Linkerd gibi service mesh araçları mTLS'i otomatik olarak tüm servisler arasında uygular. Manual sertifika yönetimine gerek kalmaz.
:::

## Network Security Best Practices

### Zero Trust Architecture

:::concept[Zero Trust (İng: Zero Trust Architecture)]
Zero Trust, "ağın içindeki hiçbir şeye güvenme, her şeyi doğrula" prensibiyle çalışan bir güvenlik modelidir. Geleneksel "kale ve hendek" modelinin yerini alır.

**Turkce karsiligi:** Sıfır Güven Mimarisi
**Ne ise yarar:** İç ve dış tehditlere karşı koruma sağlar. Bir hacker ağa sızsa bile lateral movement yapamaz
**Gercek hayat benzetmesi:** Geleneksel güvenlik: binaya girdiysen her yere gidebilirsin. Zero Trust: her odaya girmek için ayrı ayrı kimlik kartı göstermen gerekir
:::

:::comparison
| Ozellik | Geleneksel Model | Zero Trust |
|---------|-----------------|------------|
| Felsefe | "İçerideysen güvenilirsin" | "Hiçbir şeye güvenme" |
| Ağ segmentasyonu | Düz ağ | Mikro segmentasyon |
| Erişim kontrolü | VPN ile ağa gir, her yere eriş | Her kaynak için ayrı doğrulama |
| Kimlik doğrulama | Bir kez (login) | Sürekli (continuous verification) |
| Lateral movement | Kolay | Çok zor |
| Insider threat | Zayıf koruma | Güçlü koruma |
:::

### DNS Security

:::code[bash]{title="DNS ile İlgili Güvenlik Konuları"}
# DNS lookup
nslookup myapp.com
dig myapp.com

# DNS over HTTPS (DoH) - DNS sorgularını şifreler
# Tarayıcılar varsayılan olarak DoH kullanmaya başladı

# DNSSEC - DNS yanıtlarının imzalanması
# DNS spoofing/cache poisoning saldırılarını engeller
dig myapp.com +dnssec

# DNS rebinding koruması:
# Server tarafında Host header doğrulama
# app.use((req, res, next) => {
#   const allowedHosts = ['myapp.com', 'www.myapp.com'];
#   if (!allowedHosts.includes(req.hostname)) {
#     return res.status(403).send('Invalid host');
#   }
#   next();
# });
:::

### Port Güvenliği

:::code[bash]{title="Önemli Port Numaraları ve Güvenlik"}
# Bilmen gereken portlar:
# 20/21  - FTP (GÜVENSİZ - SFTP kullan)
# 22     - SSH (key-based auth kullan)
# 25     - SMTP (STARTTLS ile şifrele)
# 53     - DNS
# 80     - HTTP (HTTPS'e yönlendir)
# 443    - HTTPS
# 3000   - Node.js dev server
# 3306   - MySQL (dışarıya açma!)
# 5432   - PostgreSQL (dışarıya açma!)
# 6379   - Redis (dışarıya açma! ve AUTH kullan)
# 27017  - MongoDB (dışarıya açma!)

# Açık portları kontrol et
sudo netstat -tlnp
# veya
sudo ss -tlnp

# Nmap ile port tarama (kendi sunucunda)
nmap -sS -sV myapp.com

# KURAL: Veritabanı portlarını (3306, 5432, 6379, 27017)
# ASLA internete açma! Sadece internal network veya VPN üzerinden eriş.
:::

:::warning
**Veritabanı portlarını internete ASLA açma!** PostgreSQL (5432), MySQL (3306), Redis (6379) ve MongoDB (27017) portları sadece internal network'ten erişilebilir olmalı. Public erişim gerekiyorsa: VPN, SSH tunnel veya cloud provider'ın managed database servisi kullan. Redis'i authentication olmadan çalıştırma - geçmişte binlerce Redis sunucusu cryptocurrency miner ile enfekte edildi!
:::

## Practical Network Debugging

:::code[bash]{title="Network Debugging Araçları"}
# curl ile HTTP debugging
curl -v https://api.example.com      # Verbose (headers dahil)
curl -I https://api.example.com      # Sadece headers
curl -k https://self-signed.com      # SSL doğrulamayı atla (sadece test!)

# TLS sertifikasını kontrol et
openssl s_client -connect myapp.com:443 -servername myapp.com
# Sertifika detaylarını gösterir: issuer, expiry, chain

# DNS debugging
dig myapp.com                        # DNS sorgusu
dig myapp.com +trace                 # DNS resolution adımları
nslookup myapp.com 8.8.8.8          # Belirli DNS server ile sorgula

# TCP bağlantı testi
telnet myapp.com 443                 # Port açık mı?
nc -zv myapp.com 443                 # Netcat ile port kontrolü

# Traceroute (ağ yolu takibi)
traceroute myapp.com
# Windows: tracert myapp.com

# tcpdump ile trafik yakalama (gelişmiş)
sudo tcpdump -i eth0 port 443 -w capture.pcap
# Wireshark ile analiz et

# MTR (traceroute + ping kombinasyonu)
mtr myapp.com
:::

## Interview'da Networking Soruları

:::interview
**Soru 1:** "HTTP ile HTTPS arasındaki fark nedir?"
**Cevap:** HTTPS, HTTP'nin TLS (Transport Layer Security) ile şifrelenmiş versiyonudur. HTTP plain text olarak iletişim kurar (herkes okuyabilir), HTTPS tüm trafiği şifreler. HTTPS ayrıca server'ın kimliğini sertifika ile doğrular (man-in-the-middle saldırısını engeller). Modern web'de HTTPS zorunlu - tarayıcılar HTTP siteleri "güvensiz" olarak işaretler.

**Soru 2:** "TCP 3-way handshake'i açıkla."
**Cevap:** (1) SYN: Client server'a bağlantı isteği gönderir (sequence number ile), (2) SYN-ACK: Server isteği kabul eder ve kendi sequence number'ını gönderir, (3) ACK: Client server'ın sequence number'ını onaylar. Bu üç adımdan sonra connection kurulmuştur ve veri iletimi başlayabilir. Bu mekanizma her iki tarafın da iletişim kanalının çalıştığından emin olmasını sağlar.

**Soru 3:** "TLS 1.3'ün TLS 1.2'ye göre avantajları nelerdir?"
**Cevap:** (1) Daha hızlı: 1-RTT handshake (TLS 1.2: 2-RTT), 0-RTT resumption desteği, (2) Daha güvenli: Zayıf cipher suite'ler kaldırıldı, RSA key exchange kaldırıldı, forward secrecy zorunlu, (3) Daha basit: Daha az seçenek = daha az konfigürasyon hatası imkanı. TLS 1.3 hem performans hem güvenlik açısından TLS 1.2'den üstündür.

**Soru 4:** "Neden veritabanı portlarını internete açmamalıyız?"
**Cevap:** (1) Brute force saldırısına açık - saldırganlar sürekli şifre dener, (2) Bilinen vulnerability'ler exploit edilebilir, (3) DDoS saldırısına maruz kalabilir, (4) Veri sızıntısı riski. Veritabanına erişim sadece application server'dan (internal network) veya VPN/SSH tunnel üzerinden olmalıdır. Cloud'da security group ile kısıtlanmalıdır.
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "OSI 7 katman modelini ve TCP/IP 4 katman modelini karsilastirarak acikla. TLS 1.3 handshake surecini adim adim goster - Client Hello'dan sifreli iletisim baslayana kadar ne oluyor? TLS 1.2 ile 1.3 arasindaki performans ve guvenlik farklari neler? Certificate chain of trust nasil calisir?"

**2. Pratik Uygulama:**
> "SSH key pair olustur (ed25519), bir sunucuya password'suz baglan, SSH config dosyasi yaz ve SSH tunneling ile uzak veritabanina guvenli eris. Let's Encrypt ile ucretsiz TLS sertifikasi al ve Nginx'te HTTPS konfigurasyonu yap. HSTS header'ini aktiflestir."
> Takip: "Simdi firewall kurallari (iptables/ufw) ile sadece 80, 443 ve 22 portlarini ac. Fail2ban ile brute force saldirilarini engelle."

**3. Mukemmellik Icin:**
> "Microservice mimarisinde service-to-service iletisimi nasil guvenli hale getiririm? mTLS (mutual TLS), service mesh (Istio/Linkerd), network policies (Kubernetes), VPN ve zero-trust networking kavramlarini karsilastir. Certificate rotation ve secret management (Vault) stratejilerini dahil et."

### Pair Programming Ipucu
Network sorunlarinda AI'a tcpdump, wireshark veya curl -v ciktisini goster ve sor: "Bu TLS handshake neden basarisiz oluyor? Certificate chain'de sorun mu var? DNS resolution dogru mu? Network problemini teshis et ve coz."
:::

:::exercise
## Pratik Alistirmalar

### Alistirma 1: Network Trafigini Analiz Etme
Terminal komutlariyla network analizi yapin:

```bash
# 1. DNS resolution kontrolu
nslookup example.com
dig example.com +trace  # DNS resolution zincirini gor

# 2. TCP baglanti testi
curl -v https://example.com 2>&1 | head -30  # TLS handshake'i gor
# TODO: Ciktidaki her satiri yorumla (DNS, TCP connect, TLS, HTTP request/response)

# 3. Network yolu takibi
traceroute example.com  # Paket hangi hop'lardan geciyor?
# TODO: Her hop'un ne oldugunu (ISP router, CDN edge, origin) tespit et
```

**Beklenen sonuc:** curl -v ciktisindaki DNS lookup, TCP handshake, TLS handshake ve HTTP header'lari satir satir aciklayabilmeli.

### Alistirma 2: HTTP Header Guvenlik Analizi
Populer web sitelerinin guvenlik header'larini kontrol edin:

```bash
# TODO: Asagidaki sitelerin response header'larini inceleyin
curl -I https://github.com
curl -I https://google.com

# Kontrol edilecek header'lar:
# - Strict-Transport-Security (HSTS)
# - Content-Security-Policy (CSP)
# - X-Content-Type-Options
# - X-Frame-Options
# - Referrer-Policy
# TODO: Her header'in ne ise yaradigini ve eksik olursa ne olacagini yazin
```

**Beklenen sonuc:** En az 5 guvenlik header'ini aciklayabilmeli, eksik header'larin olusturdugu riskleri belirtebilmeli.

### Alistirma 3: Basit Load Balancer Simulasyonu
Docker Compose ile basit bir load balancer ortami kurun:

```yaml
# docker-compose.yml
# TODO: 3 adet Node.js backend container'i olusturun (her biri farkli port)
# TODO: Nginx reverse proxy ile round-robin load balancing yapin
# TODO: Health check endpoint'i ekleyin
# TODO: Bir container'i durdurun ve trafik dagitiminin degisimini gozlemleyin
```

**Beklenen sonuc:** Request'ler 3 backend arasinda esit dagilmali, bir backend durdugunca kalan ikisi trafigi almali.
:::

:::interview
## Mulakat Sorulari

**Soru 1: TCP ve UDP arasindaki farklar nelerdir? Hangi senaryolarda hangisi kullanilir?**
- **Junior cevabi:** TCP guvenilir baglanti kurar, UDP hizli ama guvenilir degildir.
- **Senior cevabi:** TCP: connection-oriented (3-way handshake), reliable delivery (acknowledgment + retransmission), ordered (sequence number), flow control (sliding window), congestion control. UDP: connectionless, best-effort delivery, no ordering, no flow control. TCP kullanim: HTTP/HTTPS, veritabani baglantilari, dosya transferi, email - veri butunlugu kritik olan her yer. UDP kullanim: DNS (kucuk paketler, hizli response), video streaming (kayip frame tolere edilir), online gaming (dusuk latency), VoIP. Modern yaklasim: QUIC protokolu (HTTP/3) UDP uzerine TCP benzeri guvenilirlik saglar, head-of-line blocking sorununu cozer.

**Soru 2: HTTPS nasil calisir? TLS handshake surecini aciklayiniz.**
- **Junior cevabi:** HTTPS sifreli HTTP'dir, SSL sertifikasi kullanir.
- **Senior cevabi:** TLS 1.3 handshake: 1) Client Hello: desteklenen cipher suite'lar ve key share gonderilir, 2) Server Hello: secilen cipher suite ve server key share, 3) Server Certificate: sertifika zinciri gonderilir, 4) Client sertifikayi CA chain'e karsi dogrular, 5) Ortak session key olusturulur (ECDHE key exchange ile forward secrecy saglanir). TLS 1.3 handshake 1-RTT'ye dusuruldu (1.2'de 2-RTT), 0-RTT resumption ile tekrar baglantilarda sifir ek latency. Certificate pinning mobil uygulamalarda MITM'e karsi koruma saglar. Let's Encrypt ile ucretsiz otomatik sertifika yonetimi.
:::

:::must-note
## Defterine Yaz!

1. **OSI 7 Katman (Üstten Alta):** Application (HTTP), Presentation (TLS), Session, Transport (TCP/UDP), Network (IP), Data Link (Ethernet), Physical (Kablo). Mnemonik: "All People Seem To Need Data Processing."

2. **TCP vs UDP:** TCP = güvenilir, sıralı, yavaş (web, email, DB). UDP = hızlı, güvenilmez (video, oyun, DNS). HTTP/HTTPS TCP üzerinde çalışır.

3. **TLS Handshake Özet:** ClientHello → ServerHello + Certificate → Client doğrulama → Key exchange → Encrypted communication. TLS 1.3 = 1-RTT, TLS 1.2 = 2-RTT.

4. **SSH Key Best Practice:** Ed25519 tercih et (RSA'dan daha güvenli ve hızlı). Passphrase ekle. Password auth'u kapat. Root login'i kapat. SSH port'unu değiştir.

5. **Port Güvenliği Kuralı:** Veritabanı portlarını (5432, 3306, 6379, 27017) internete ASLA açma! Internal network veya VPN/SSH tunnel kullan. Her zaman minimum port açma prensibi uygula.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir

Senior developer networking öğrenirken:

1. **Packet level düşünür:** Wireshark ile TLS handshake'i, TCP retransmission'ı ve DNS resolution'ı paket seviyesinde inceler. Ağ sorunlarını "sihir" olarak görmez, her adımı anlar.

2. **Zero Trust uygular:** "Kale ve hendek" modelini terk eder. Her servis arası iletişimde mTLS, her erişimde kimlik doğrulama, mikro segmentasyon ve least privilege prensibi uygular.

3. **Certificate lifecycle yönetir:** Sertifika süresini izler (cert-manager), otomatik yenileme kurar (Let's Encrypt), certificate pinning uygular (mobile app), CA rotation planı oluşturur.

4. **DDoS koruması planlar:** CloudFlare/AWS Shield ile L3/L4 koruması, WAF ile L7 koruması, rate limiting, geo-blocking ve auto-scaling ile capacity planning yapar.

5. **Compliance network gereksinimleri bilir:** PCI-DSS network segmentation, HIPAA encryption requirements, SOC 2 monitoring, KVKK veri iletim güvenliği standartlarını uygular.

**CTO bakış açısı:** "Network mimarimiz ölçeklenebilir mi?", "Multi-region latency kabul edilebilir mi?", "Network cost optimize edilebilir mi?", "Incident response network playbook'u hazır mı?", "Vendor lock-in riski var mı?". Network'ü maliyet, performans ve güvenlik üçgeninde değerlendirir.
:::

:::knowledge-check
1. OSI modelinde HTTP hangi katmanda çalışır?
2. TCP ile UDP'nin temel farkları nelerdir?
3. TLS handshake'te forward secrecy ne anlama gelir?
4. mTLS'in normal TLS'ten farkı nedir ve nerede kullanılır?
5. Veritabanı portlarını internete açmamanın sebepleri nelerdir?
:::

:::external-resource
- [Cloudflare Learning Center](https://www.cloudflare.com/learning/) - Network ve güvenlik kavramları
- [Let's Encrypt](https://letsencrypt.org/) - Ücretsiz TLS sertifikası
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) - TLS yapılandırma aracı
- [Qualys SSL Labs](https://www.ssllabs.com/ssltest/) - TLS sertifika ve yapılandırma test aracı
- [SSH Academy](https://www.ssh.com/academy/ssh) - SSH derinlemesine
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) - Güvenlik framework'ü
- [Wireshark](https://www.wireshark.org/) - Network paket analiz aracı
:::
