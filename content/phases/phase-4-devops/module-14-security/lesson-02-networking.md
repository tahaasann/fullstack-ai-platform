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

**Türkçe karsiligi:** Açık Sistemler Arabağlantı Modeli
**Ne ise yarar:** Network iletişiminin nasıl çalıştığını anlamak ve sorunları doğru katmanda çözmek için kullanılır
**Gercek hayat benzetmesi:** Posta sistemi gibi - mektup yazarsın (Application), zarfa koyarsın (Presentation), posta kodunu yazarsın (Session), posta kutusuna bırakırsın (Transport), postacı alır (Network), kamyona yükler (Data Link), yolda gider (Physical)
:::

:::comparison
| Katman | Isim | Protokol Örnekleri | Ne Yapar? | Developer Icin |
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

**Türkçe karsiligi:** İletim Kontrol Protokolü
**Ne ise yarar:** Verinin eksiksiz ve doğru sırada ulaşmasını garanti eder
**Gercek hayat benzetmesi:** Taahhütlü posta gibi - gönderdiğin her mektubun ulaştığından emin olursun, kaybolursa tekrar gönderilir
:::

:::concept[UDP (İng: User Datagram Protocol)]
UDP, bağlantısız (connectionless) ve hızlı bir transport protokolüdür. Veri iletimini garanti etmez ama çok düşük gecikme sağlar.

**Türkçe karsiligi:** Kullanıcı Datagram Protokolü
**Ne ise yarar:** Düşük gecikme gerektiren uygulamalarda (video, oyun) hızlı veri iletimi sağlar
**Gercek hayat benzetmesi:** Normal posta gibi - mektup gönderirsin ama ulaşıp ulaşmadığını bilmezsin. Hızlıdır ama garanti yoktur
:::

:::comparison
| Özellik | TCP | UDP |
|---------|-----|-----|
| Bağlantı | Connection-oriented (3-way handshake) | Connectionless |
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

**Türkçe karsiligi:** Güvenlik Duvarı
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

**Türkçe karsiligi:** Sanal Özel Ağ
**Ne ise yarar:** İnternet trafiğini şifreler, uzaktan özel ağlara güvenli erişim sağlar
**Gercek hayat benzetmesi:** İki bina arasında yeraltı tüneli gibi - dışarıdan kimse tünelin içinde ne geçtiğini göremez
:::

:::comparison
| VPN Turu | Kullanim | Protokol | Örnek |
|----------|----------|----------|-------|
| **Site-to-Site** | İki ofis ağını birleştirir | IPSec | AWS VPN Gateway |
| **Remote Access** | Uzak çalışanlar ofis ağına bağlanır | OpenVPN, WireGuard | Employee VPN |
| **Cloud VPN** | Cloud VPC'ye güvenli bağlantı | IPSec/IKEv2 | AWS Client VPN |

**Modern tercih:** WireGuard - daha hızlı, daha basit ve daha güvenli. OpenVPN'e kıyasla çok daha az kod satırı (4000 vs 70000+), daha iyi performans.
:::

## SSH (Secure Shell)

:::concept[SSH (İng: Secure Shell)]
SSH, güvenli olmayan ağ üzerinden güvenli uzak erişim sağlayan bir kriptografik ağ protokolüdür. Telnet'in güvenli alternatifidir.

**Türkçe karsiligi:** Güvenli Kabuk
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

**Türkçe karsiligi:** Taşıma Katmanı Güvenliği
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
| Özellik | TLS 1.2 | TLS 1.3 |
|---------|---------|---------|
| Handshake | 2-RTT | 1-RTT (0-RTT resumption) |
| Cipher suites | Çok fazla (bazıları zayıf) | Sadece güvenli olanlar |
| Forward secrecy | Opsiyonel | Zorunlu (ECDHE) |
| RSA key exchange | Destekler | Kaldırıldı (güvensiz) |
| Performance | Yavaş handshake | Hızlı handshake |
| Güvenlik | İyi | Çok İyi |

**Kural:** Yeni projelerde TLS 1.3 kullan. TLS 1.2'yi destekle (eski client'lar için). TLS 1.0 ve 1.1 ASLA kullanma (güvensiz). SSL ASLA kullanma (broken).
:::

### Certificate (Sertifika) Yönetimi

:::concept[TLS Certificate (İng: TLS/SSL Certificate)]
TLS sertifikası, bir web sitesinin kimliğini doğrulayan ve public key'ini içeren dijital bir belgedir. Certificate Authority (CA) tarafından imzalanır.

**Türkçe karsiligi:** Dijital Sertifika
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

**Türkçe karsiligi:** Karşılıklı TLS / İki Yönlü TLS
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

**Türkçe karsiligi:** Sıfır Güven Mimarisi
**Ne ise yarar:** İç ve dış tehditlere karşı koruma sağlar. Bir hacker ağa sızsa bile lateral movement yapamaz
**Gercek hayat benzetmesi:** Geleneksel güvenlik: binaya girdiysen her yere gidebilirsin. Zero Trust: her odaya girmek için ayrı ayrı kimlik kartı göstermen gerekir
:::

:::comparison
| Özellik | Geleneksel Model | Zero Trust |
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

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "OSI 7 katman modelini ve TCP/IP 4 katman modelini karsilastirarak acikla. TLS 1.3 handshake sürecini adim adim goster - Client Hello'dan sifreli iletisim baslayana kadar ne oluyor? TLS 1.2 ile 1.3 arasindaki performans ve güvenlik farklari neler? Certificate chain of trust nasil calisir?"

**2. Pratik Uygulama:**
> "SSH key pair oluştur (ed25519), bir sunucuya password'suz baglan, SSH config dosyasi yaz ve SSH tunneling ile uzak veritabanina guvenli eris. Let's Encrypt ile ucretsiz TLS sertifikasi al ve Nginx'te HTTPS konfigurasyonu yap. HSTS header'ini aktiflestir."
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

### Alistirma 2: HTTP Header Güvenlik Analizi
Populer web sitelerinin güvenlik header'larini kontrol edin:

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

**Beklenen sonuc:** En az 5 güvenlik header'ini aciklayabilmeli, eksik header'larin oluşturdugu riskleri belirtebilmeli.

### Alistirma 3: Basit Load Balancer Simulasyonu
Docker Compose ile basit bir load balancer ortamı kurun:

```yaml
# docker-compose.yml
# TODO: 3 adet Node.js backend container'i olusturun (her biri farkli port)
# TODO: Nginx reverse proxy ile round-robin load balancing yapin
# TODO: Health check endpoint'i ekleyin
# TODO: Bir container'i durdurun ve trafik dagitiminin degisimini gozlemleyin
```

**Beklenen sonuc:** Request'ler 3 backend arasinda esit dagilmali, bir backend durdugunca kalan ikisi trafigi almali.

---

### Alistirma 4: DNS Cozumleme Analizi (Kolay)

Farkli DNS sunuculari ile domain cozumleme surelerini karsilastir.

```bash
# 1. Farkli DNS sunuculari ile sorgula
nslookup google.com 8.8.8.8       # Google DNS
nslookup google.com 1.1.1.1       # Cloudflare DNS
nslookup google.com 208.67.222.222 # OpenDNS

# 2. Detayli DNS sorgusu
dig google.com +trace    # Tum cozumleme zincirini gor
dig google.com ANY       # Tum DNS kayitlarini listele

# 3. Response surelerini karsilastir
for dns in 8.8.8.8 1.1.1.1 208.67.222.222; do
  echo "=== $dns ==="
  dig @$dns google.com | grep "Query time"
done

# TODO: Kendi domain'in icin MX, TXT, CNAME kayitlarini sorgula
# TODO: TTL degerlerini incele ve cache etkisini anla
# TODO: DNSSEC dogrulamasini kontrol et: dig +dnssec example.com
```

**Beklenen Sonuc:** Farkli DNS sunuculari farkli response sureleri verebilir. DNS kayit turleri (A, AAAA, MX, CNAME, TXT) dogru listelenmeli.
**Ipucu:** Cloudflare DNS (1.1.1.1) genellikle en hizlidir. `dig +short` ile sadece IP adresini gor.

---

### Alistirma 5: TLS Sertifika Analizi (Kolay)

Bir web sitesinin TLS sertifikasini ve güvenlik yapılandırmasini incele.

```bash
# 1. Sertifika bilgilerini gor
openssl s_client -connect google.com:443 -servername google.com </dev/null 2>/dev/null | \
  openssl x509 -noout -text | head -30

# 2. Sertifika zincirini incele
openssl s_client -connect google.com:443 -showcerts </dev/null 2>/dev/null

# 3. Sertifika gecerlilik tarihlerini kontrol et
echo | openssl s_client -connect google.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# 4. Desteklenen TLS versiyonlarini test et
nmap --script ssl-enum-ciphers -p 443 google.com

# TODO: Kendi deploy ettigin sitenin sertifikasini incele
# TODO: Self-signed sertifika olustur ve farkini anla
# TODO: SSL Labs API ile sertifika notu al
```

**Beklenen Sonuc:** Sertifika zinciri (leaf → intermediate → root CA) gorunmeli. TLS 1.3 desteklenmeli. Sertifika gecerlilik tarihleri dogru olmali.
**Ipucu:** Let's Encrypt sertifikalari 90 gun gecerlidir ve otomatik yenilenir. `certbot` ile kolayca yonetilebilir.

---

### Alistirma 6: Wireshark ile Paket Analizi (Orta)

Network trafigini yakalayip HTTP ve TCP paketlerini analiz et.

```bash
# tcpdump ile terminal bazli paket yakalama
# 1. HTTP trafigini yakala
sudo tcpdump -i any -A port 80 -c 20

# 2. Belirli bir host'a giden trafigi yakala
sudo tcpdump -i any host api.example.com -w capture.pcap

# 3. TCP handshake'i gozlemle
sudo tcpdump -i any 'tcp[tcpflags] & (tcp-syn|tcp-ack|tcp-fin) != 0' -c 10

# 4. DNS trafigini yakala
sudo tcpdump -i any port 53 -c 10
```

```python
# Python ile basit paket analizi (scapy)
from scapy.all import sniff, IP, TCP

def packet_callback(packet):
    if IP in packet:
        print(f"{packet[IP].src} -> {packet[IP].dst} | "
              f"Proto: {packet[IP].proto} | Size: {len(packet)}")

# TODO: 20 paket yakala ve analiz et
# TODO: TCP SYN paketlerini filtrele
# TODO: HTTP GET request'lerini bul
# TODO: Ortalama paket boyutunu hesapla
```

**Beklenen Sonuc:** TCP 3-way handshake (SYN, SYN-ACK, ACK) gozlemlenmeli. HTTP request/response icerigi okunabilmeli. HTTPS trafiginde icerik sifreli gorunmeli.
**Ipucu:** Wireshark GUI kullanirken `http` veya `tcp.port == 443` filtresi ile trafigi daralt. HTTPS icerigi decrypt etmek icin SSLKEYLOGFILE gerekir.

---

### Alistirma 7: Reverse Proxy Yapılandırmasi (Orta)

Nginx reverse proxy ile SSL termination, caching ve gzip compression yapilandir.

```nginx
# nginx.conf
upstream backend {
    server api:3000;
    server api2:3000;
    keepalive 32;
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/fullchain.pem;
    ssl_certificate_key /etc/ssl/private/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Gzip compression
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;
    gzip_min_length 1000;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;

    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # TODO: Static dosyalar icin cache kurallari ekle (images, css, js)
    # TODO: Rate limiting ekle (limit_req_zone)
    # TODO: WebSocket proxy yapilandirmasi ekle
    # TODO: Access log formatini JSON olarak yapilandir
}
```

**Beklenen Sonuc:** HTTP→HTTPS yonlendirmesi çalışmali. Gzip ile response boyutu kuculmus olmali. Backend'e X-Real-IP header'i ile gercek IP iletilmeli.
**Ipucu:** `nginx -t` ile konfigurasyonu dogrula. `curl -I https://example.com` ile response header'larini kontrol et.

---

### Alistirma 8: SSH Tunnel ve Port Forwarding (Orta)

SSH tunnel ile uzak servislere guvenli erisim sagla.

```bash
# 1. Local port forwarding (uzak DB'ye lokal erisim)
ssh -L 5433:localhost:5432 user@remote-server
# Simdi localhost:5433 uzerinden uzak PostgreSQL'e baglanabilirsin

# 2. Remote port forwarding (lokal servisi disariya ac)
ssh -R 8080:localhost:3000 user@remote-server
# Simdi remote-server:8080 uzerinden lokal app'ine erisilir

# 3. Dynamic port forwarding (SOCKS proxy)
ssh -D 9090 user@remote-server
# Tarayicida SOCKS proxy olarak localhost:9090 kullan

# 4. SSH config dosyasi ile kolaylastir
cat >> ~/.ssh/config << 'EOF'
Host production-db
    HostName 10.0.1.50
    User deploy
    LocalForward 5433 localhost:5432
    IdentityFile ~/.ssh/id_ed25519
EOF

# TODO: SSH key pair olustur (ed25519 algoritmasiyla)
# TODO: Password authentication'i kapat, sadece key authentication kalsın
# TODO: Jump host (bastion server) uzerinden ic aga eris
# TODO: sshfs ile uzak dosya sistemini mount et
```

**Beklenen Sonuc:** Lokal porttan uzak veritabanina baglanilabilmeli. SSH key ile sifresiz erisim saglanmali. Config dosyasi ile tek komutla bağlantı kurulmali.
**Ipucu:** `ssh-keygen -t ed25519` modern ve guvenli key oluşturur. `ssh-copy-id user@server` ile public key'i kolayca yukle.

---

### Alistirma 9: Network Guvenligi Audit Scripti (Zor)

Bir sunucunun network güvenliğini otomatik kontrol eden script yaz.

```bash
#!/bin/bash
# security-audit.sh

echo "=== Network Security Audit ==="
echo "Tarih: $(date)"
echo ""

# 1. Acik portlari tara
echo "--- Acik Portlar ---"
ss -tlnp | grep LISTEN

# 2. Firewall kurallarini kontrol et
echo "--- Firewall Kurallari ---"
sudo iptables -L -n --line-numbers 2>/dev/null || sudo ufw status verbose

# 3. Dinleyen servisleri listele
echo "--- Dinleyen Servisler ---"
ss -tlnp | awk 'NR>1 {print $4, $7}'

# 4. SSL/TLS yapilandirmasini kontrol et
echo "--- TLS Kontrolu ---"
echo | openssl s_client -connect localhost:443 2>/dev/null | grep "Protocol\|Cipher"

# TODO: Zayif SSH konfigurasyonlarini kontrol et
# TODO: Default credentials kontrolu (common username/password)
# TODO: Gereksiz servisleri tespit et ve raporla
# TODO: DNS leak testi yap
# TODO: Sonuclari JSON formatinda kaydet
```

**Beklenen Sonuc:** Raporda acik portlar, firewall durumu, TLS versiyonu ve potansiyel güvenlik riskleri listelenmeli.
**Ipucu:** Production sunucularda sadece gerekli portlar acik olmali (22, 80, 443). `nmap -sV localhost` ile servis versiyonlarini tespit et.

---

### Alistirma 10: WebSocket Guvenli Iletisim (Zor)

WebSocket üzerinden guvenli real-time iletisim kur.

```javascript
// server.js
const { WebSocketServer } = require("ws");
const jwt = require("jsonwebtoken");

const wss = new WebSocketServer({ noServer: true });

// HTTP upgrade sirasinda authentication
server.on("upgrade", (request, socket, head) => {
  const token = new URL(request.url, "http://localhost").searchParams.get("token");
  try {
    const user = jwt.verify(token, process.env.JWT_SECRET);
    wss.handleUpgrade(request, socket, head, (ws) => {
      ws.user = user;
      wss.emit("connection", ws, request);
    });
  } catch (err) {
    socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
    socket.destroy();
  }
});

wss.on("connection", (ws) => {
  console.log(`User connected: ${ws.user.id}`);

  ws.on("message", (data) => {
    const message = JSON.parse(data);
    // TODO: Message validation ve sanitization
    // TODO: Rate limiting (saniyede max 10 mesaj)
    // TODO: Room/channel bazli yetkilendirme
    // TODO: Mesaj boyut limiti (max 4KB)
  });

  // Heartbeat mekanizmasi
  ws.isAlive = true;
  ws.on("pong", () => { ws.isAlive = true; });
});

// Dead connection temizligi
setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);
```

**Beklenen Sonuc:** JWT olmadan WebSocket bağlantısi reddedilmeli. Heartbeat ile olü bağlantılar temizlenmeli. Mesaj boyut ve hiz limitleri uygulanmali.
**Ipucu:** WebSocket URL'inde token göndermek yerine, ilk mesajda authentication yapmak daha guvenlidir (URL server loglarinda gorunur).
:::

:::exercise
### Alistirma 11: OSI Katmanlari Analizi (Kolay)

Bir HTTP isteginin OSI katmanlarindan gecisini adim adim analiz et.

```bash
# TODO: Her katmani belirle ve acikla:
# Layer 7 (Application): HTTP GET /index.html
# Layer 4 (Transport): TCP, hedef port: 80
# Layer 3 (Network): IP adresleri
# Layer 2 (Data Link): MAC adresleri
# Layer 1 (Physical): Ethernet frame

# TODO: Ayni analizi HTTPS icin yap — hangi katmanlarda fark var?
# TODO: DNS cozumleme surecini katmanlarla eslestir
# TODO: tcpdump ile bir HTTP istegini yakala ve katmanlari gozlemle
# sudo tcpdump -i any -n -A port 80 -c 10
```

**Beklenen Sonuc:** Her katmanin gorevi aciklanmali. HTTP vs HTTPS arasindaki katman farklari belirtilmeli.
**Ipucu:** Gercek hayatta TCP/IP modeli (4 katman) kullanilir ama mulakatlarda OSI (7 katman) sorulur!
:::

:::exercise
### Alistirma 12: DNS Cozumleme Sureci (Kolay)

DNS sorgulama surecini adim adim incele.

```bash
# DNS sorgulama araclari
nslookup example.com
dig example.com +trace

# TODO: Farkli DNS kayit tiplerini sorgula
# dig example.com A      # IPv4
# dig example.com AAAA   # IPv6
# dig example.com MX     # Mail sunucusu
# dig example.com CNAME  # Alias
# dig example.com TXT    # SPF, DKIM
# dig example.com NS     # Name server

# TODO: DNS cache'i kontrol et
# TODO: DNS over HTTPS (DoH) vs DNS over TLS (DoT) karsilastir
```

**Beklenen Sonuc:** DNS cozumleme adimlarini (recursive -> root -> TLD -> authoritative) aciklayabilmeli.
**Ipucu:** `dig +trace` tum DNS yolculugunu gosterir: root (.) -> com. -> example.com. -> IP adresi.
:::

:::exercise
### Alistirma 13: TCP Handshake ve Baglanti Analizi (Kolay)

TCP 3-way handshake surecini incele.

```bash
# TCP baglanti adimlari:
# 1. SYN: Client -> Server (seq: x)
# 2. SYN-ACK: Server -> Client (seq: y, ack: x+1)
# 3. ACK: Client -> Server (seq: x+1, ack: y+1)

# TODO: Baglanti durumlarini gozlemle
# netstat -an | grep ESTABLISHED
# ss -tunap

# TODO: TCP vs UDP karsilastirma tablosu olustur
# | Ozellik   | TCP            | UDP            |
# |-----------|----------------|----------------|
# | Baglanti  | Connection     | Connectionless |
# | Guvenilir | Evet           | Hayir          |
# | Kullanim  | HTTP, SSH      | DNS, Video     |

# TODO: TIME_WAIT durumunu acikla
```

**Beklenen Sonuc:** 3-way handshake adimlarini aciklayabilmeli. TCP ve UDP farklarini bilmeli.
**Ipucu:** TIME_WAIT durumu baglanti kapandiktan sonra ~60sn surer. Cok sayida TIME_WAIT performans sorununa isaret eder.
:::

:::exercise
### Alistirma 14: TLS/SSL Sertifika Analizi (Orta)

Bir web sitesinin TLS sertifikasini incele.

```bash
# TODO: Sertifika bilgilerini goster
# openssl s_client -connect google.com:443 < /dev/null 2>/dev/null | openssl x509 -text -noout

# TODO: Sertifika zincirini kontrol et
# openssl s_client -connect example.com:443 -showcerts

# TODO: Sertifika surum tarihini kontrol et
# echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# TODO: Self-signed sertifika olustur (gelistirme icin)
# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# TODO: Let's Encrypt ile ucretsiz sertifika alma adimlarini yaz
```

**Beklenen Sonuc:** Sertifika bilgileri (issuer, subject, validity) okunabilmeli. Sertifika zinciri anlasilmali.
**Ipucu:** TLS 1.3 en guncel ve guvenli versiyondur. TLS 1.0 ve 1.1 kullanimdisi. Her zaman TLS 1.2+ kullan.
:::

:::exercise
### Alistirma 15: SSH Key Yonetimi ve Guvenlik (Orta)

SSH anahtar cifti olustur ve guvenli yapilandir.

```bash
# TODO: Ed25519 SSH key olustur
# ssh-keygen -t ed25519 -C "email@example.com"

# TODO: SSH config dosyasi olustur
# Host production
#   HostName 192.168.1.100
#   User deploy
#   IdentityFile ~/.ssh/id_project
#   Port 2222

# TODO: SSH hardening (sshd_config)
# PermitRootLogin no
# PasswordAuthentication no
# MaxAuthTries 3

# TODO: SSH tunnel olustur (port forwarding)
# ssh -L 5432:localhost:5432 production
```

**Beklenen Sonuc:** SSH key pair olusturulabilmeli. Root login ve parola ile giris engellenmeli.
**Ipucu:** Ed25519 RSA'dan daha kisa ve guvenlidir. SSH agent ile passphrase'i her seferinde girmekten kurtul.
:::

:::exercise
### Alistirma 16: Firewall ve Port Yonetimi (Orta)

Temel firewall kurallari olustur.

```bash
# TODO: Acik portlari tara
# nmap -sT localhost

# TODO: UFW ile firewall kurallari
# sudo ufw default deny incoming
# sudo ufw default allow outgoing
# sudo ufw allow 22/tcp
# sudo ufw allow 80/tcp
# sudo ufw allow 443/tcp
# sudo ufw deny 3306/tcp
# sudo ufw enable

# TODO: iptables ile ayni kurallari yaz
# TODO: Port forwarding konfigurasyonu olustur
# TODO: Bastion host (jump server) mimarisi ciz
```

**Beklenen Sonuc:** Sadece gerekli portlar acik olmali. Varsayilan politika "deny" olmali.
**Ipucu:** "En az yetki" prensibi: sadece gerekli portlari ac. Production'da SSH portu IP kisitlamali olmali.
:::

:::exercise
### Alistirma 17: HTTP/HTTPS Protokol Analizi (Orta)

HTTP istek ve yanitlarini detayli analiz et.

```bash
# TODO: HTTP istek detaylarini goster
# curl -v https://httpbin.org/get

# TODO: Farkli HTTP metodlarini test et
# curl -X POST httpbin.org/post -d '{"name":"test"}' -H 'Content-Type: application/json'
# curl -X PUT httpbin.org/put
# curl -X DELETE httpbin.org/delete

# TODO: HTTP response header'larini analiz et
# curl -I https://example.com

# TODO: HTTP/1.1 vs HTTP/2 vs HTTP/3 karsilastirmasi yap
# - Multiplexing, Header compression, Server push, QUIC

# TODO: CORS header'larini test et
```

**Beklenen Sonuc:** HTTP metodlarini ve durum kodlarini bilmeli. HTTP/2 avantajlarini listelemeli.
**Ipucu:** HTTP/2 tek TCP baglantisi uzerinden paralel istekler gonderir (multiplexing).
:::

:::exercise
### Alistirma 18: VPN ve Proxy Mimarisi (Zor)

VPN ve proxy kavramlarini anla ve konfigur et.

```nginx
# TODO: Nginx reverse proxy konfigurasyonu
# server {
#   listen 80;
#   server_name api.example.com;
#   location / {
#     proxy_pass http://localhost:3000;
#     proxy_set_header Host $host;
#     proxy_set_header X-Real-IP $remote_addr;
#     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#   }
# }
```

```markdown
# TODO: Forward proxy vs reverse proxy karsilastirmasi yaz
# Forward: Client -> Proxy -> Internet (istemci gizlenir)
# Reverse: Internet -> Proxy -> Server (sunucu gizlenir)

# TODO: VPN vs Proxy vs TOR karsilastirmasi yaz
# TODO: Corporate network mimarisi ciz (DMZ, internal, VPN)
# TODO: WireGuard VPN kurulumu arastir
```

**Beklenen Sonuc:** Forward/reverse proxy farki aciklanmali. VPN tunel mekanizmasi anlasilmali.
**Ipucu:** Nginx reverse proxy arkasinda Node.js calistirmak production standarttidir.
:::

:::exercise
### Alistirma 19: Network Guvenligi Degerlendirmesi (Zor)

Bir ag icin temel network security degerlendirmesi yap.

```bash
# TODO: Network kesfini yap
# nmap -sn 192.168.1.0/24  # Ping sweep
# nmap -sV -sC target-ip   # Service detection

# TODO: Guvenlik kontrol listesi olustur
# [ ] Acik portlar minimum mu?
# [ ] Gereksiz servisler kapatildi mi?
# [ ] Default sifre kullanan servis var mi?
# [ ] SSL/TLS versiyonu guncel mi?
# [ ] DNS zone transfer engellendi mi?

# TODO: testssl.sh ile SSL konfigurasyonunu test et
# TODO: Bulgu raporu yaz (Kritik/Yuksek/Orta/Dusuk)
```

**Beklenen Sonuc:** Tum aktif cihazlar ve servisler listelenmeli. Guvenlik riskleri onceliklendirilmeli.
**Ipucu:** nmap taramalarini SADECE kendi aglarina yap. Izinsiz tarama yasalara aykiridir!
:::


:::interview
## Mulakat Sorulari

**Soru 1: TCP ve UDP arasindaki farklar nelerdir? Hangi senaryolarda hangisi kullanilir?**
- **Junior cevabi:** TCP guvenilir bağlantı kurar, UDP hizli ama guvenilir degildir.
- **Senior cevabi:** TCP: connection-oriented (3-way handshake), reliable delivery (acknowledgment + retransmission), ordered (sequence number), flow control (sliding window), congestion control. UDP: connectionless, best-effort delivery, no ordering, no flow control. TCP kullanim: HTTP/HTTPS, veritabani bağlantılari, dosya transferi, email - veri butunlugu kritik olan her yer. UDP kullanim: DNS (kucuk paketler, hizli response), video streaming (kayip frame tolere edilir), online gaming (dusuk latency), VoIP. Modern yaklasim: QUIC protokolu (HTTP/3) UDP uzerine TCP benzeri guvenilirlik saglar, head-of-line blocking sorununu cozer.

**Soru 2: HTTPS nasil calisir? TLS handshake sürecini aciklayiniz.**
- **Junior cevabi:** HTTPS sifreli HTTP'dir, SSL sertifikasi kullanir.
- **Senior cevabi:** TLS 1.3 handshake: 1) Client Hello: desteklenen cipher suite'lar ve key share gonderilir, 2) Server Hello: secilen cipher suite ve server key share, 3) Server Certificate: sertifika zinciri gonderilir, 4) Client sertifikayi CA chain'e karsi dogrular, 5) Ortak session key oluşturulur (ECDHE key exchange ile forward secrecy saglanir). TLS 1.3 handshake 1-RTT'ye dusuruldu (1.2'de 2-RTT), 0-RTT resumption ile tekrar bağlantılarda sifir ek latency. Certificate pinning mobil uygulamalarda MITM'e karsi koruma saglar. Let's Encrypt ile ucretsiz otomatik sertifika yonetimi.
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
