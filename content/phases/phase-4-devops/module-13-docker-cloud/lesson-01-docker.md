---
title: "Docker & Containerization: Uygulamaları Taşınabilir Yap"
id: "mod-13-docker/lesson-01"
estimated_minutes: 65
order: 1
tags: ["docker", "containerization", "dockerfile", "docker-compose", "containers", "devops", "multi-stage-build"]
prerequisites: ["mod-12-auth/lesson-01"]
---

# Docker & Containerization: Uygulamaları Taşınabilir Yap

:::realworld
Netflix her gün milyonlarca container çalıştırıyor. Spotify, Uber, Airbnb... Hepsi Docker kullanıyor. "Benim bilgisayarımda çalışıyordu" cümlesi Docker ile tarihe karıştı. Bir Node.js uygulamasını development'tan production'a taşırken environment farklılıkları yüzünden saatler harcadıysan, Docker tam sana göre. Container teknolojisi modern yazılım geliştirmenin temel taşı haline geldi ve DevOps mühendisliğinin olmazsa olmazıdır.
:::

## Why Docker? Neden Container Kullanıyoruz?

Geleneksel deployment sürecinde şu sorunlarla karşılaşırsın:

- **Environment inconsistency:** Development'ta Node 22, production'da Node 20 yüklü
- **Dependency conflicts:** İki proje farklı Python versiyonu istiyor
- **Setup complexity:** Yeni bir developer projeye başlamak için 2 gün harcıyor
- **Scaling difficulties:** Sunucu başına bir uygulama, kaynak israfı

Docker bu sorunların hepsini **containerization** ile çözer.

:::deha-tip
Senior developer'lar sadece "Docker kullanmayı" bilmez, container orchestration, image optimization, security scanning ve multi-stage build stratejilerini de bilir. Docker'ı bir araç olarak değil, deployment pipeline'ının temel parçası olarak görürler. Her projede ilk yapılan iş Dockerfile yazmaktır.
:::

## Container vs Virtual Machine

:::concept[Container (İng: Container)]
Container, bir uygulamayı ve tüm dependency'lerini (kütüphaneler, runtime, system tools) izole bir ortamda paketleyen lightweight bir sanallaştırma teknolojisidir.

**Türkçe karsiligi:** Konteyner / Kapsayıcı
**Ne ise yarar:** Uygulamayı her ortamda aynı şekilde çalıştırır
**Gercek hayat benzetmesi:** Nakliye konteyneri gibi - içinde ne olursa olsun her gemiye, trene, kamyona sığar ve içindekiler korunur
:::

:::concept[Virtual Machine (İng: Virtual Machine / VM)]
Virtual Machine, fiziksel bir bilgisayar üzerinde yazılımsal olarak oluşturulmuş tam bir bilgisayar simülasyonudur. Kendi işletim sistemi, kernel'i ve kaynaklara sahiptir.

**Türkçe karsiligi:** Sanal Makine
**Ne ise yarar:** Bir fiziksel sunucuda birden fazla izole işletim sistemi çalıştırır
**Gercek hayat benzetmesi:** Bir bina içinde tamamen bağımsız daireler gibi - her dairenin kendi mutfağı, banyosu, elektriği var
:::

:::comparison
| Özellik | Container | Virtual Machine |
|---------|-----------|----------------|
| Başlatma suresi | Saniyeler | Dakikalar |
| Boyut | MB'lar (10-500MB) | GB'lar (1-20GB) |
| OS | Host OS kernel'ini paylaşır | Kendi OS kernel'i |
| İzolasyon | Process-level | Hardware-level |
| Performance | Native'e yakın | Overhead var |
| Kaynak tuketimi | Düşük | Yüksek |
| Tasinabilirlik | Çok yüksek | Orta |
| Güvenlik izolasyonu | Orta (namespace/cgroup) | Yüksek (hypervisor) |

**Özet:** Container = lightweight, hızlı, paylaşımlı kernel. VM = ağır ama tam izolasyon. Modern uygulamalarda container tercih edilir, compliance gerektiren durumlarda VM kullanılır.
:::

:::english
**Container:** A lightweight, standalone, executable package that includes everything needed to run a piece of software - code, runtime, system tools, libraries, and settings.

**Image vs Container:** An image is a read-only template. A container is a running instance of an image. You can create many containers from one image. Think of it like: Image = Class, Container = Object.

**Docker Daemon:** The background service running on the host that manages building, running, and distributing Docker containers.

**Docker Registry:** A repository for Docker images. Docker Hub is the default public registry, like npm for Node packages.
:::

## Docker Temelleri

### Docker Architecture

Docker uç temel bileşenden oluşur:

1. **Docker Client** - CLI komutlarını çalıştırdığın araç (`docker build`, `docker run`)
2. **Docker Daemon (dockerd)** - Container'ları yöneten background service
3. **Docker Registry** - Image'ların saklandığı depo (Docker Hub, GitHub Container Registry)

:::code[bash]{title="Docker Temel Komutları"}
# Docker version kontrolü
docker --version
docker info

# Image çekme (Docker Hub'dan)
docker pull node:20-alpine
docker pull postgres:16

# Mevcut image'ları listele
docker images
# veya
docker image ls

# Container çalıştır
docker run hello-world

# Interaktif container (shell aç)
docker run -it node:20-alpine sh

# Detached mode (arka planda çalıştır)
docker run -d --name my-postgres postgres:16

# Çalışan container'ları listele
docker ps

# Tüm container'ları listele (durmuş dahil)
docker ps -a

# Container durdur
docker stop my-postgres

# Container sil
docker rm my-postgres

# Image sil
docker rmi node:20-alpine

# Tüm durmuş container'ları temizle
docker container prune

# Tüm kullanılmayan kaynakları temizle
docker system prune -a
:::

:::warning
`docker system prune -a` komutu TÜM kullanılmayan image'ları, container'ları ve network'leri siler. Production sunucuda dikkatli kullan! Özellikle cache'lenmiş build layer'ları da silinir ve sonraki build'ler daha uzun sürer.
:::

### Port Mapping ve Environment Variables

:::code[bash]{title="Port Mapping ve Env Variables"}
# Port mapping: host:container
# Localhost:3000'e gelen istekler container'ın 3000 portuna yönlendirilir
docker run -d -p 3000:3000 --name my-app my-node-app

# Farklı port mapping
# Host'ta 8080, container'da 3000
docker run -d -p 8080:3000 --name my-app my-node-app

# Environment variable
docker run -d \
  -p 5432:5432 \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secretpass \
  -e POSTGRES_DB=myapp \
  --name my-db \
  postgres:16

# Env file kullanımı
docker run -d --env-file .env --name my-app my-node-app

# Birden fazla port
docker run -d -p 3000:3000 -p 9229:9229 --name my-app my-node-app
:::

:::tip
Port mapping sırasını karıştırma: `-p HOST:CONTAINER`. Host tarafındaki port senin makinendeki port, container tarafındaki port uygulamanın dinlediği port. `-p 8080:3000` demek "benim 8080 portumu container'ın 3000 portuna bağla" demektir.
:::

## Dockerfile Yazma

:::concept[Dockerfile (İng: Dockerfile)]
Dockerfile, bir Docker image'ı oluşturmak için gereken adımları tanımlayan bir text dosyasıdır. Her satır bir "layer" oluşturur ve Docker bu layer'ları cache'ler.

**Türkçe karsiligi:** Docker yapılandırma dosyası
**Ne ise yarar:** Image'ın nasıl oluşturulacağını adım adım tanımlar
**Gercek hayat benzetmesi:** Yemek tarifi gibi - malzemeleri ve adımları sırayla yazar, her seferinde aynı sonucu alırsın
:::

:::code[dockerfile]{title="Basic Node.js Dockerfile"}
# Base image seç - Alpine Linux (küçük boyut)
FROM node:20-alpine

# Çalışma dizinini ayarla
WORKDIR /app

# Önce package dosyalarını kopyala (layer caching için)
COPY package*.json ./

# Dependency'leri yükle (pnpm — 2026 standardı)
RUN corepack enable && pnpm install --frozen-lockfile --prod

# Uygulama kodunu kopyala
COPY . .

# Container'ın hangi portu dinleyeceğini belirt (dokümantasyon amaçlı)
EXPOSE 3000

# Container başladığında çalışacak komut
CMD ["node", "server.js"]
:::

### Dockerfile Komutları Detaylı

:::code[dockerfile]{title="Tüm Dockerfile Komutları"}
# FROM: Base image belirler (her Dockerfile FROM ile başlamalı)
FROM node:20-alpine

# WORKDIR: Çalışma dizini ayarlar (yoksa oluşturur)
WORKDIR /app

# COPY: Host'tan container'a dosya kopyalar
COPY package.json ./              # Tek dosya
COPY package.json pnpm-lock.yaml ./     # Birden fazla dosya (pnpm projelerinde)
COPY . .                          # Tüm dizin (dikkat: .dockerignore kullan!)
COPY --chown=node:node . .        # Sahiplik belirterek kopyala

# ADD: COPY gibi ama URL'den indirebilir ve tar dosyalarını açar
ADD https://example.com/file.tar.gz /tmp/  # URL'den indir
ADD archive.tar.gz /app/                    # Otomatik tar açar

# RUN: Build sırasında komut çalıştırır (yeni layer oluşturur)
RUN corepack enable && pnpm install --frozen-lockfile --prod
RUN apt-get update && apt-get install -y curl  # Komutları birleştir

# ENV: Environment variable tanımlar
ENV NODE_ENV=production
ENV PORT=3000

# ARG: Build-time variable (image içinde kalmaz)
ARG NODE_VERSION=20
FROM node:${NODE_VERSION}-alpine

# EXPOSE: Container'ın dinleyeceği portu belirtir (sadece dokümantasyon)
EXPOSE 3000

# CMD: Container başladığında çalışacak varsayılan komut
CMD ["node", "server.js"]         # Exec form (önerilen)
CMD node server.js                # Shell form

# ENTRYPOINT: Container'ın ana komutunu belirler (CMD ile birlikte)
ENTRYPOINT ["node"]
CMD ["server.js"]                 # node server.js çalışır

# USER: Container'ı çalıştıracak kullanıcı (güvenlik için root kullanma!)
USER node

# HEALTHCHECK: Container sağlık kontrolü
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# LABEL: Image'a metadata ekler
LABEL maintainer="developer@example.com"
LABEL version="1.0"
:::

:::beginner-mistake
**Hata:** Her COPY ve RUN komutu yeni bir layer oluşturur. Çok fazla layer = büyük image.

**Yanlış:**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get clean
```

**Doğru:**
```dockerfile
RUN apt-get update && \
    apt-get install -y curl vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

RUN komutlarını `&&` ile birleştir ve gereksiz dosyaları aynı layer'da temizle. Böylece image boyutu küçülür.
:::

### .dockerignore

:::code[text]{title=".dockerignore Dosyası"}
# .dockerignore - Docker build context'ten çıkarılacak dosyalar
# .gitignore ile aynı sözdizimi

# Dependency klasörleri
node_modules
npm-debug.log*

# Build çıktıları
dist
build
coverage

# Versiyon kontrol
.git
.gitignore

# IDE dosyaları
.vscode
.idea
*.swp
*.swo

# Docker dosyaları
Dockerfile*
docker-compose*
.dockerignore

# Environment dosyaları (GÜVENLİK!)
.env
.env.local
.env.production

# Test dosyaları (production image'da gereksiz)
__tests__
*.test.js
*.spec.js
jest.config.js

# Dokümantasyon
README.md
docs/
:::

:::warning
`.env` dosyasını **ASLA** Docker image'a dahil etme! `.dockerignore`'a eklemeyi unutursan, environment secret'ların image'a gömülür ve Docker Hub'a push edildiğinde herkes görebilir. Environment variable'ları runtime'da `-e` flag'i veya Docker Compose ile geçir.
:::

## Layer Caching: Build Hızını Optimize Et

Docker her Dockerfile komutunu bir "layer" olarak cache'ler. Bir layer değiştiğinde, ondan sonraki TÜM layer'lar yeniden build edilir.

:::code[dockerfile]{title="Layer Caching Optimizasyonu"}
# ❌ KOTU: Her kod degisikliginde pnpm install tekrar calisir
FROM node:20-alpine
WORKDIR /app
COPY . .                    # Kod degisti -> bu layer degisti
RUN corepack enable && pnpm install --frozen-lockfile  # -> Bu da tekrar calisir (cache miss)
CMD ["node", "server.js"]

# ✅ IYI: Sadece package.json degistiginde pnpm install calisir
FROM node:20-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml ./  # Sadece package dosyalari (nadiren degisir)
RUN corepack enable && pnpm install --frozen-lockfile  # Cache'ten gelir (package degismediyse)
COPY . .                    # Kod degisse bile pnpm install tekrar çalışmaz
CMD ["node", "server.js"]
:::

:::concept[Layer Caching (İng: Layer Caching)]
Docker, Dockerfile'daki her komutu bir layer olarak saklar ve cache'ler. Build sırasında değişmeyen layer'lar cache'ten alınır, sadece değişen layer'lar yeniden oluşturulur.

**Türkçe karsiligi:** Katman Önbellekleme
**Ne ise yarar:** Build süresini dramatik şekilde kısaltır
**Gercek hayat benzetmesi:** Bir bina inşa ederken temeli tekrar atmazsın - sadece değişen katı yeniden yaparsın
:::

:::tip
**Layer caching altın kuralı:** En az değişen dosyaları EN ÜSTTE, en çok değişen dosyaları EN ALTTA kopyala. `package.json` nadiren değişir, uygulama kodu sürekli değişir. Bu sıralama build süresini 5 dakikadan 15 saniyeye düşürebilir.
:::

## Multi-Stage Build

Multi-stage build, Docker image boyutunu dramatik şekilde küçülten bir tekniktir. Build aşamasında gerekli ama production'da gereksiz olan tool'ları (compiler, dev dependency'ler) final image'dan çıkarır.

:::code[dockerfile]{title="Multi-Stage Build: Node.js + TypeScript"}
# ============ Stage 1: Builder ============
# TypeScript derleme ve dependency yükleme
FROM node:20-alpine AS builder

WORKDIR /app

# Dependency'leri yükle
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

# TypeScript kaynak kodunu kopyala ve derle
COPY tsconfig.json ./
COPY src/ ./src/
RUN pnpm build

# Production dependency'lerini ayrı yükle
RUN pnpm install --frozen-lockfile --prod && pnpm store prune

# ============ Stage 2: Production ============
# Sadece derlenen JS ve production dependency'leri
FROM node:20-alpine AS production

# Güvenlik: root kullanıcı kullanma
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

WORKDIR /app

# Builder'dan sadece gerekli dosyaları kopyala
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# Non-root kullanıcıya geç
USER nextjs

EXPOSE 3000

# Health check ekle
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]
:::

:::comparison
| Özellik | Single-Stage Build | Multi-Stage Build |
|---------|-------------------|-------------------|
| Image boyutu | 800MB - 1.5GB | 100MB - 200MB |
| Dev dependencies | Image'da kalır | Çıkarılır |
| Build tools | Image'da kalır | Çıkarılır |
| Source code | Image'da kalır | Sadece compiled output |
| Security | Geniş attack surface | Minimal attack surface |
| Build süresi | Tek aşama | İlk build biraz uzun, sonrakiler cache'li |

**Kural:** Production image'lar her zaman multi-stage build kullanmalı. Dev dependency'ler, TypeScript compiler, test framework'leri production'da bulunmamalı.
:::

:::code[dockerfile]{title="Multi-Stage Build: React Frontend"}
# ============ Stage 1: Build React App ============
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

# ============ Stage 2: Nginx ile Serve Et ============
FROM nginx:alpine AS production

# Custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Build çıktısını nginx'e kopyala
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
:::

:::tip
React/Vue/Angular gibi SPA'lar için multi-stage build ZORUNLUDUR. Build stage'de Node.js ile webpack/vite çalıştırırsın, production stage'de sadece nginx ile static dosyaları serve edersin. Image boyutu: ~1.2GB yerine ~25MB!
:::

## Docker Compose

:::concept[Docker Compose (İng: Docker Compose)]
Docker Compose, çoklu container uygulamalarını tanımlamak ve çalıştırmak için kullanılan bir araçtır. YAML dosyasında service'leri, network'leri ve volume'ları tanımlarsın.

**Türkçe karsiligi:** Docker Kompozisyon / Çoklu Konteyner Yönetimi
**Ne ise yarar:** Birden fazla container'ı tek komutla ayağa kaldırır (app + database + cache + ...)
**Gercek hayat benzetmesi:** Orkestra şefi gibi - tüm müzisyenlerin (container'ların) ne zaman, nasıl çalacağını koordine eder
:::

:::code[yaml]{title="docker-compose.yml: Full-Stack Uygulama"}
# Docker Compose version (v2+ sözdizimiyle)
version: '3.8'

services:
  # ============ Node.js API ============
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: production          # Multi-stage build'de hangi stage
    container_name: myapp-api
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://admin:secret@db:5432/myapp
      - REDIS_URL=redis://cache:6379
      - JWT_SECRET=${JWT_SECRET}   # Host'taki .env'den okur
    depends_on:
      db:
        condition: service_healthy  # DB hazır olana kadar bekle
      cache:
        condition: service_started
    restart: unless-stopped
    networks:
      - backend
    volumes:
      - ./logs:/app/logs           # Log dosyaları persist etsin
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  # ============ PostgreSQL Database ============
  db:
    image: postgres:16-alpine
    container_name: myapp-db
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data    # Named volume
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # İlk kurulumda çalışır
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - backend

  # ============ Redis Cache ============
  cache:
    image: redis:7-alpine
    container_name: myapp-cache
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - backend

  # ============ Nginx Reverse Proxy ============
  nginx:
    image: nginx:alpine
    container_name: myapp-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - backend

# ============ Named Volumes ============
volumes:
  postgres_data:          # PostgreSQL verileri persist edilir
    driver: local
  redis_data:             # Redis verileri persist edilir
    driver: local

# ============ Networks ============
networks:
  backend:
    driver: bridge
:::

### Docker Compose Komutları

:::code[bash]{title="Docker Compose CLI"}
# Tüm servisleri başlat (detached mode)
docker compose up -d

# Build edip başlat (Dockerfile değişikliklerinde)
docker compose up -d --build

# Logları izle
docker compose logs -f
docker compose logs -f api        # Sadece api servisinin logları

# Servisleri durdur
docker compose down

# Servisleri durdur VE volume'ları sil (veritabanı verileri gider!)
docker compose down -v

# Belirli bir servisi yeniden başlat
docker compose restart api

# Çalışan bir container'da komut çalıştır
docker compose exec api sh                          # Shell aç
docker compose exec db psql -U admin -d myapp       # PostgreSQL'e bağlan

# Servislerin durumunu kontrol et
docker compose ps

# Sadece belirli servisleri başlat
docker compose up -d db cache

# Scale (aynı servisten birden fazla instance)
docker compose up -d --scale api=3
:::

:::warning
`docker compose down -v` komutu volume'ları da siler! Bu demek ki PostgreSQL veritabanındaki TÜM veriler silinir. Production'da bu komutu ASLA kullanma. Development'ta bile dikkatli ol - saatlerdir oluşturduğun test verileri gidebilir.
:::

## Container Networking

Docker container'lar arasında iletişim sağlamak için network sistemi kullanır.

:::concept[Docker Network (İng: Docker Network)]
Docker Network, container'lar arasında izole iletişim kanalları oluşturan bir sanal ağ yapısıdır.

**Türkçe karsiligi:** Docker Ağı
**Ne ise yarar:** Container'ların birbirleriyle güvenli ve izole şekilde iletişim kurmasını sağlar
**Gercek hayat benzetmesi:** Şirket içi telefon sistemi gibi - dışarıdan aranamaz ama dahili numaralarla herkes birbirini arayabilir
:::

:::code[bash]{title="Docker Network Yönetimi"}
# Network listele
docker network ls

# Yeni network oluştur
docker network create myapp-network

# Container'ı network'e bağla
docker run -d --network myapp-network --name api my-api
docker run -d --network myapp-network --name db postgres:16

# Artık api container'ı db'ye hostname ile ulaşabilir:
# postgresql://admin:pass@db:5432/myapp
# "db" burada container name = hostname

# Network'ün detaylarını gör
docker network inspect myapp-network

# Network sil
docker network rm myapp-network
:::

:::tip
Docker Compose kullandığında network otomatik oluşturulur. Aynı `docker-compose.yml` dosyasındaki servisler birbirlerine **service name** ile ulaşabilir. Yani `db` servisi `db:5432` adresiyle erişilebilir. Localhost değil, servis adını kullan!
:::

### Network Türleri

:::code[bash]{title="Docker Network Drivers"}
# Bridge (varsayılan): İzole network, container'lar arası iletişim
docker network create --driver bridge my-bridge

# Host: Container host'un network'ünü paylaşır (port mapping gerekmez)
docker run --network host my-app

# None: Hiç network erişimi yok (güvenlik için)
docker run --network none my-secure-app

# Overlay: Swarm modunda birden fazla host arası network
docker network create --driver overlay my-overlay
:::

## Volume Mounts: Verileri Kalıcı Yap

:::concept[Docker Volume (İng: Docker Volume)]
Docker Volume, container verilerini kalıcı hale getiren bir mekanizmadır. Container silinse bile veriler korunur.

**Türkçe karsiligi:** Docker Birim / Kalıcı Depolama
**Ne ise yarar:** Veritabanı dosyaları, upload'lar, log'lar gibi verilerin container yaşam döngüsünden bağımsız olmasını sağlar
**Gercek hayat benzetmesi:** Kira kontratı bitince evden çıkarsın ama eşyaların depoda kalır
:::

:::code[bash]{title="Docker Volume Türleri"}
# 1. Named Volume (önerilen): Docker tarafından yönetilir
docker volume create myapp-data
docker run -v myapp-data:/var/lib/postgresql/data postgres:16

# 2. Bind Mount: Host dosya sistemini doğrudan bağlar
# Development'ta live reload için ideal
docker run -v $(pwd)/src:/app/src my-app

# 3. tmpfs: Bellekte kalır, disk'e yazılmaz (hassas veriler için)
docker run --tmpfs /tmp my-app

# Volume listele
docker volume ls

# Volume detayları
docker volume inspect myapp-data

# Kullanılmayan volume'ları temizle
docker volume prune
:::

:::code[yaml]{title="docker-compose.yml'da Volume Kullanımı"}
services:
  api:
    build: .
    volumes:
      # Development: Host dosyalarını container'a bağla (live reload)
      - ./src:/app/src                   # Bind mount
      - /app/node_modules                # Anonymous volume (node_modules korunsun)

  db:
    image: postgres:16
    volumes:
      # Production: Named volume ile veri kalıcılığı
      - postgres_data:/var/lib/postgresql/data
      # İlk kurulumda SQL dosyası çalıştır
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql:ro

volumes:
  postgres_data:
:::

:::beginner-mistake
**Hata:** Development'ta bind mount kullanırken `node_modules`'u override etmek.

**Problem:**
```yaml
volumes:
  - .:/app    # Tüm dizini bağlar - host'taki node_modules container'dakini ezer!
```

**Çözüm:**
```yaml
volumes:
  - .:/app
  - /app/node_modules    # Anonymous volume: container'ın kendi node_modules'unu korur
```

Anonymous volume ile `node_modules` container içinde kalır, host'taki boş/farklı `node_modules` onu ezmez.
:::

## Docker Best Practices

### 1. Minimal Base Image Kullan

:::code[dockerfile]{title="Base Image Seçimi"}
# ❌ Full OS - 900MB+
FROM node:20

# ⚠️ Slim variant - 200MB
FROM node:20-slim

# ✅ Alpine Linux - 50MB (önerilen)
FROM node:20-alpine

# ✅✅ Distroless - 30MB (en güvenli, shell yok)
FROM gcr.io/distroless/nodejs20
:::

### 2. Non-Root User Kullan

:::code[dockerfile]{title="Non-Root User (Güvenlik)"}
FROM node:20-alpine

# node kullanıcısı Alpine image'larda zaten var
WORKDIR /app

COPY --chown=node:node package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile --prod

COPY --chown=node:node . .

# Root'tan node kullanıcısına geç
USER node

EXPOSE 3000
CMD ["node", "server.js"]
:::

:::warning
Container'ları **ASLA root kullanıcı** ile çalıştırma! Eğer container'da bir güvenlik açığı varsa, attacker root yetkileriyle host sistemine erişebilir. `USER` komutu ile non-root kullanıcıya geç. Kubernetes'te de `runAsNonRoot: true` zorunlu tutulmalıdır.
:::

### 3. HEALTHCHECK Ekle

:::code[dockerfile]{title="Health Check Patterns"}
# HTTP endpoint kontrolü (Node.js)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# curl ile (curl yüklüyse)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1

# TCP port kontrolü
HEALTHCHECK --interval=30s --timeout=3s \
  CMD nc -z localhost 3000 || exit 1

# Database health check (PostgreSQL)
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U postgres || exit 1
:::

### 4. Security Scanning

:::code[bash]{title="Image Security Scanning"}
# Docker Scout ile vulnerability tarama
docker scout cves my-app:latest

# Trivy ile tarama (açık kaynak, çok popüler)
trivy image my-app:latest

# Snyk ile tarama
snyk container test my-app:latest

# Hadolint ile Dockerfile linting
hadolint Dockerfile
:::

### 5. Image Boyutunu Küçült

:::code[dockerfile]{title="Optimized Production Dockerfile"}
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build && pnpm prune --prod

# Production stage
FROM node:20-alpine
RUN apk add --no-cache tini
WORKDIR /app

# Sadece gerekli dosyaları kopyala
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/package.json ./

USER node
EXPOSE 3000

# tini ile process yönetimi (zombie process'leri önler)
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/server.js"]
:::

:::tip
`tini` kullanmak önemlidir! Node.js container'larda `PID 1` olarak çalışan process SIGTERM sinyallerini düzgün yakalayamayabilir. `tini` init process olarak görev yaparak graceful shutdown sağlar ve zombie process'leri temizler.
:::

## Development vs Production Docker Setup

:::comparison
| Özellik | Development | Production |
|---------|------------|------------|
| Base image | `node:20-alpine` | `node:20-alpine` + multi-stage |
| Volumes | Bind mount (live reload) | Named volume (data only) |
| Environment | `.env` file | Secrets manager / env vars |
| Build | `docker compose up --build` | CI/CD pipeline |
| Restart | `restart: no` | `restart: unless-stopped` |
| Logging | Console | Log aggregation (ELK/Loki) |
| Debugging | Port 9229 açık | Port kapalı |
| Source code | Mount edilmiş | Image'a baked |
:::

:::code[yaml]{title="docker-compose.dev.yml - Development Override"}
# docker compose -f docker-compose.yml -f docker-compose.dev.yml up
version: '3.8'

services:
  api:
    build:
      context: .
      target: development           # Dev stage kullan
    volumes:
      - ./src:/app/src               # Live reload
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    ports:
      - "3000:3000"
      - "9229:9229"                  # Debug port
    command: pnpm exec nodemon --inspect=0.0.0.0:9229 src/server.js

  db:
    ports:
      - "5432:5432"                  # Host'tan erişim (dev tools için)
:::

## Pratik: Full-Stack Docker Setup

:::exercise
### Alistirma 1: Dockerfile Yazma ve Optimize Etme (Kolay)

Bir Node.js uygulamasi icin multi-stage Dockerfile yaz ve image boyutunu optimize et.

```dockerfile
# TODO: Multi-stage Dockerfile tamamla

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

# TODO: Non-root user olustur
# RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# TODO: Sadece gerekli dosyalari kopyala
# COPY --from=builder /app/dist ./dist
# COPY --from=builder /app/node_modules ./node_modules
# COPY --from=builder /app/package.json ./

# TODO: Non-root user'a gec
# USER appuser

EXPOSE 3000
# TODO: Healthcheck ekle
# HEALTHCHECK --interval=30s --timeout=3s CMD wget -q --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

```bash
# Build ve test et
docker build -t my-api:v1 .
docker images my-api  # Boyutu kontrol et (hedef: <200MB)
docker run -p 3000:3000 my-api:v1
curl http://localhost:3000/health
```

**Beklenen Sonuc:** Multi-stage build ile image boyutu 200MB altinda olmali. Non-root user ile çalışmali. Healthcheck tanimli olmali.
**Ipucu:** `.dockerignore` dosyasina `node_modules`, `.git`, `dist` ekle. Layer caching icin package.json'i COPY . 'dan once kopyala.

---

### Alistirma 2: Docker Compose ile Multi-Service Setup (Orta)

Express API, PostgreSQL ve Redis'i Docker Compose ile birlestir.

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:secret@db:5432/myapp
      - REDIS_URL=redis://cache:6379
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    # TODO: restart policy ekle

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
      # TODO: init.sql dosyasini mount et
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    # TODO: redis.conf ile memory limit ayarla

volumes:
  postgres_data:
  redis_data:

# TODO: docker-compose.dev.yml olustur
# - api'de volume mount (live reload icin)
# - nodemon ile calistir
# - Debug portu ac (9229)
```

**Beklenen Sonuc:** `docker compose up` ile 3 servis ayaga kalkmali. API, DB'ye ve Redis'e baglanabilmeli. Healthcheck'ler gecmeli. `docker compose ps` ile tum servislerin "healthy" oldugunu gormeli.
**Ipucu:** `depends_on` ile healthcheck'leri birlestirerek servislerin dogru sirada baslamasini sagla.

---

### Alistirma 3: Docker Debugging ve Optimizasyon (Zor)

Docker image boyutunu kucult, layer caching'i optimize et ve container'lari debug et.

```bash
# GOREV 1: Image boyutu analizi
docker images my-api
docker history my-api:v1  # Her layer'in boyutunu gor

# Dive araci ile detayli analiz (opsiyonel):
# docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive my-api:v1

# GOREV 2: Layer caching testi
# Sadece src/ klasorunde degisiklik yap ve tekrar build et
# Hangi layer'lar cache'ten geldi, hangileri yeniden build edildi?
time docker build -t my-api:v2 .
# "CACHED" yazan satirlari gozlemle

# GOREV 3: Container debugging
# Calisan container'in icine gir
docker exec -it my-api-container sh
# Dosya sistemini incele, process listesini gor, network baglantisini test et
ps aux
wget -q --spider http://localhost:3000/health && echo "OK" || echo "FAIL"

# GOREV 4: Log analizi
docker logs my-api-container --tail 50
docker logs my-api-container -f  # Canli log izle

# GOREV 5: Resource limit ayarla
# docker-compose.yml'da:
# deploy:
#   resources:
#     limits:
#       memory: 512M
#       cpus: "0.5"

# GOREV 6: Docker network incelemesi
docker network ls
docker network inspect my-app_default
# Servisler birbirleriyle nasil iletisim kuruyor?
```

**Beklenen Sonuc:** Image boyutu Alpine kullanarak ve multi-stage build ile minimize edilmis olmali. Layer caching ile src degisikliginde sadece ilgili layer'lar yeniden build edilmeli. Container icinden DB ve Redis'e erisim dogrulanmali.
**Ipucu:** `docker system df` ile disk kullanimini gor. `docker builder prune` ile build cache'ini temizle. `docker compose logs -f service_name` ile tek servisin logunu izle.

---

### Alistirma 4: .dockerignore ve Güvenlik Taramasi (Kolay)

Docker image'inda gereksiz ve hassas dosyalarin bulunmadigini dogrula.

```bash
# 1. .dockerignore dosyasi olustur
cat > .dockerignore << 'EOF'
node_modules
.git
.env
.env.*
*.md
tests/
coverage/
.vscode/
docker-compose*.yml
EOF

# 2. Image'i build et ve icerigini incele
docker build -t my-app:secure .
docker run --rm my-app:secure ls -la /app/

# TODO: .env dosyasinin image'da OLMADIGINI dogrula
# TODO: node_modules'un host'tan degil, build sirasinda yuklendigini kontrol et
# TODO: docker scout cves my-app:secure ile guvenlik taramasi yap
# TODO: Trivy ile alternatif tarama: trivy image my-app:secure
```

**Beklenen Sonuc:** .env, .git, node_modules gibi dosyalar image'da bulunmamali. Güvenlik taramasinda kritik CVE olmamali.
**Ipucu:** `docker history my-app:secure` ile her layer'in ne yaptigini gor. Secret'lari build-time'da ARG olarak gecme, runtime'da environment variable kullan.

---

### Alistirma 5: Docker Volume ve Persistent Data (Kolay)

Container silinse bile verilerin kaybolmamasini saglayan volume yapılandırmasi yap.

```bash
# 1. Named volume ile PostgreSQL
docker volume create pgdata
docker run -d \
  --name postgres-test \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine

# 2. Veri ekle
docker exec -it postgres-test psql -U postgres -c "
  CREATE TABLE test_data (id SERIAL, name TEXT);
  INSERT INTO test_data (name) VALUES ('container silinse bile kalacak');
"

# 3. Container'i sil ve yeniden olustur
docker stop postgres-test && docker rm postgres-test
docker run -d --name postgres-test2 -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16-alpine

# TODO: Verinin hala mevcut oldugunu dogrula (SELECT * FROM test_data)
# TODO: docker volume inspect pgdata ile volume bilgilerini incele
# TODO: Bind mount vs named volume farklarini dene
```

**Beklenen Sonuc:** Container silinip yeniden oluşturulsa bile veriler korunmali. Volume inspect ile mount point ve boyut bilgileri gorunmeli.
**Ipucu:** Named volume'lar Docker tarafindan yonetilir ve production'da tercih edilir. Bind mount'lar development'ta (hot reload) kullanilir.

---

### Alistirma 6: Multi-Stage Build ile Image Optimizasyonu (Orta)

Ayni uygulamayi farkli build stratejileriyle karsilastir.

```dockerfile
# Dockerfile.naive — Kotu ornek
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]

# Dockerfile.optimized — Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY src/ ./src/

FROM node:20-alpine AS runner
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/src ./src
USER appuser
EXPOSE 3000
CMD ["node", "src/server.js"]
```

```bash
# Her iki image'i build et ve karsilastir
docker build -f Dockerfile.naive -t app:naive .
docker build -f Dockerfile.optimized -t app:optimized .
docker images | grep app

# TODO: Image boyutlarini karsilastir (naive vs optimized)
# TODO: Layer sayisini karsilastir: docker history app:naive vs app:optimized
# TODO: Non-root user ile calistigini dogrula: docker run app:optimized whoami
# TODO: Distroless base image ile ucuncu bir varyant dene
```

**Beklenen Sonuc:** Optimized image en az %50 daha kucuk olmali. Non-root user ile çalışmali. Gereksiz build araclari final image'da bulunmamali.
**Ipucu:** `npm ci --only=production` devDependencies'i atlar. `USER appuser` ile root yetkisiyle çalışmak engellenir.

---

### Alistirma 7: Docker Network ve Container Iletisimi (Orta)

Birden fazla container'in ozel bir network üzerinden iletisim kurmasini sagla.

```bash
# 1. Custom bridge network olustur
docker network create --driver bridge app-network

# 2. Backend container'i baslat
docker run -d --name api --network app-network -e DB_HOST=db node-api:latest

# 3. Database container'i baslat
docker run -d --name db --network app-network \
  -e POSTGRES_PASSWORD=secret postgres:16-alpine

# 4. Frontend container'i baslat (farkli network'te)
docker run -d --name web --network app-network -p 80:80 nginx:alpine

# TODO: api container'indan db'ye ping at: docker exec api ping db
# TODO: Container DNS cozumlemesini test et: docker exec api nslookup db
# TODO: Network inspect ile bagli container'lari listele
# TODO: Farkli network'teki container'larin birbirini goremedigini dogrula
```

**Beklenen Sonuc:** Ayni network'teki container'lar birbirlerini isimle bulabilmeli. Farkli network'teki container'lar izole olmali.
**Ipucu:** Docker Compose otomatik olarak bir bridge network oluşturur. Service isimleri DNS olarak cozumlenir.

---

### Alistirma 8: Docker Health Check ve Restart Policy (Orta)

Container saglik kontrolu ve otomatik yeniden baslatma yapilandir.

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY src/ ./src/

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

EXPOSE 3000
CMD ["node", "src/server.js"]
```

```bash
# Restart policy ile calistir
docker run -d \
  --name resilient-app \
  --restart unless-stopped \
  --memory 512m \
  --cpus 0.5 \
  app:healthcheck

# TODO: docker inspect resilient-app | grep -A5 Health ile saglik durumunu gor
# TODO: Container icindeki process'i kill et ve otomatik restart'i gozlemle
# TODO: Memory limitini as ve OOM killer'in devreye girmesini gozlemle
# TODO: docker stats ile resource kullanimini izle
```

**Beklenen Sonuc:** Health check basarisiz olursa container "unhealthy" durumuna gecmeli. Restart policy ile otomatik yeniden baslatilmali. Kaynak limitleri asildinda uygun davranis sergilenmeli.
**Ipucu:** `--restart unless-stopped` production'da standart politikadir. `docker events` ile container lifecycle olaylarini izleyebilirsin.

---

### Alistirma 9: Docker Compose ile Development Ortamı (Zor)

Production benzeri bir development ortamı kur: hot reload, debug, seeding.

```yaml
# docker-compose.dev.yml
services:
  api:
    build:
      context: ./backend
      target: development
    volumes:
      - ./backend/src:/app/src  # Hot reload
      - /app/node_modules       # node_modules'u koru
    environment:
      - NODE_ENV=development
      - DB_HOST=db
      - REDIS_URL=redis://cache:6379
    ports:
      - "3000:3000"
      - "9229:9229"  # Node.js debugger
    depends_on:
      db:
        condition: service_healthy
    command: node --inspect=0.0.0.0:9229 src/server.js

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: devdb
      POSTGRES_PASSWORD: devpass
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # Seed data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # TODO: pgAdmin servisi ekle (web UI ile DB yonetimi)
  # TODO: Mailhog servisi ekle (development email testi)
  # TODO: api servisi icin Dockerfile.dev yaz (development target)

volumes:
  pgdata:
```

**Beklenen Sonuc:** `docker compose -f docker-compose.dev.yml up` ile tum ortam ayaga kalkmali. Backend kodu degistiginde hot reload çalışmali. Debugger VS Code'dan baglanabilir olmali.
**Ipucu:** `target: development` multi-stage build'de development stage'ini kullanir. `depends_on.condition` ile saglikli servisleri bekleyebilirsin.

---

### Alistirma 10: Container Logging ve Monitoring (Zor)

Centralized logging ve basit monitoring yapılandırmasi kur.

```yaml
# docker-compose.monitoring.yml
services:
  app:
    image: my-app:latest
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
        tag: "{{.Name}}/{{.ID}}"

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:3000']
    metrics_path: '/metrics'
```

```bash
# TODO: App'e /metrics endpoint'i ekle (prom-client kullanarak)
# TODO: Grafana'da dashboard olustur (CPU, memory, request count)
# TODO: docker compose logs --since 1h app ile son 1 saatin loglarini gor
# TODO: Alert rule ekle: response time > 500ms ise bildirim
```

**Beklenen Sonuc:** Prometheus app'ten metrikleri toplamalı. Grafana'da gorsel dashboard oluşturulmali. Log rotation ile disk dolmasi onlenmeli.
**Ipucu:** `prom-client` Node.js icin Prometheus metrikleri oluşturur. Grafana'da hazir dashboard'lar import edebilirsin (ID: 1860 — Node.js).
:::

:::exercise
### Alistirma 11: Docker Layer Analizi ve Cache Debugging (Kolay)

Docker image'inin layer yapisini analiz et ve cache sorunlarini tespit et.

```bash
# Image'i build et ve layer'lari incele
docker build -t layer-test:v1 .
docker history layer-test:v1

# TODO: Dive araci ile layer analizi yap
# docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive layer-test:v1
# TODO: Dockerfile'i optimize et — package.json'i COPY . .'dan once kopyala
# TODO: Yeniden build et ve cache hit/miss farkini gozlemle
# TODO: docker system df ile disk kullanimini analiz et
```

**Beklenen Sonuc:** Optimize edilmis Dockerfile'da package.json degismediginde npm install layer'i cache'ten gelmeli. Layer sayisi ve toplam boyut azalmali.
**Ipucu:** `docker history --no-trunc` ile her layer'in tam komutunu gor. Buyuk layer'lar genellikle gereksiz dosya kopyalamalarindan kaynaklanir.
:::

:::exercise
### Alistirma 12: Docker Environment ve Secret Yonetimi (Kolay)

Docker'da environment variable ve secret yonetimini guvenli sekilde uygula.

```yaml
# docker-compose.yml
version: "3.8"
services:
  app:
    image: node:20-alpine
    env_file:
      - .env
    environment:
      - NODE_ENV=production
    # TODO: Docker secrets kullan
    # secrets:
    #   - db_password
# TODO: secrets tanimla
# secrets:
#   db_password:
#     file: ./secrets/db_password.txt
```

```bash
# TODO: .env dosyasini .dockerignore'a ekle
# TODO: Build-time secret icin --secret flag kullan
# docker build --secret id=mysecret,src=secret.txt -t secure-app .
# TODO: docker inspect ile env variable'lari kontrol et
```

**Beklenen Sonuc:** Secret'lar image layer'larinda gorunmemeli. Runtime'da environment variable olarak erisilebilir olmali.
**Ipucu:** Secret'lar `/run/secrets/` altinda dosya olarak mount edilir. ENV ile secret tanimlamak image layer'larinda kalici iz birakir.
:::

:::exercise
### Alistirma 13: Docker Resource Limitleri (Kolay)

Container'lara CPU ve memory limitleri koy.

```bash
# Memory limitli container
docker run -d --name mem-test --memory=256m --memory-swap=512m node:20-alpine sleep 3600

# CPU limitli container
docker run -d --name cpu-test --cpus=0.5 node:20-alpine sleep 3600

# TODO: docker stats ile resource kullanimini izle
# TODO: Stress test yap: apk add stress-ng && stress-ng --vm 1 --vm-bytes 200M
# TODO: Memory limiti asildiginda OOMKilled durumunu gozlemle
# docker inspect mem-test --format='{{.State.OOMKilled}}'
```

**Beklenen Sonuc:** Memory limiti asildiginda container OOMKilled olmali. CPU limiti ile container belirlenen paydan fazlasini kullanamamali.
**Ipucu:** `--memory-reservation` soft limit, `--memory` hard limittir. Production'da her zaman memory limiti koy.
:::

:::exercise
### Alistirma 14: Docker Build Context Optimizasyonu (Orta)

.dockerignore ile build context boyutunu minimize et.

```text
# .dockerignore icerigi olustur
.git
node_modules
dist
.env
.env.*
*.pem
*.key
.vscode
coverage
__tests__
*.test.ts
docs
README.md
Dockerfile*
docker-compose*
```

```bash
# TODO: Build context boyutunu olc (oncesi ve sonrasi)
# du -sh . --exclude=.git
# TODO: .dockerignore olmadan build et ve "Sending build context" boyutunu not et
# TODO: .dockerignore ekle ve tekrar build et, boyut farkini karsilastir
# TODO: Gereksiz dosyalarin image icinde olmadigini dogrula
# docker run --rm app ls -la /app
```

**Beklenen Sonuc:** .dockerignore ile build context boyutu %50+ azalmali. Build suresi kisalmali.
**Ipucu:** `docker build` ciktisinin ilk satirinda "Sending build context to Docker daemon" boyutunu gosterir.
:::

:::exercise
### Alistirma 15: Docker Multi-Container Networking (Orta)

Custom network ile container'lar arasi guvenli iletisim kur.

```bash
# Custom network olustur
docker network create my-app-network

# API ve Frontend container'larini ayni network'e ekle
docker run -d --name api --network my-app-network nginx:alpine
docker run -d --name frontend --network my-app-network -p 3000:80 nginx:alpine

# TODO: Container'lar arasi iletisimi test et
# docker exec frontend ping -c 3 api
# docker exec frontend wget -qO- http://api:80

# TODO: Izole network olustur ve erisim kontrolunu test et
# docker network create isolated-net
# docker run -d --name db --network isolated-net postgres:16-alpine
# docker exec frontend ping -c 1 db  # Basarisiz olmali!

# TODO: Container'i iki network'e bagla
# docker network connect my-app-network db
```

**Beklenen Sonuc:** Ayni network'teki container'lar isimle birbirini bulmali. Farkli network'tekiler erisememeli.
**Ipucu:** Docker embedded DNS (127.0.0.11) container isimlerini otomatik cozer.
:::

:::exercise
### Alistirma 16: Docker Volume Backup ve Restore (Orta)

Docker volume'larini yedekle ve geri yukle.

```bash
# Test veritabani ile volume olustur
docker volume create db-data
docker run -d --name test-db -v db-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=test123 postgres:16-alpine

# TODO: Volume'u tar ile yedekle
# docker run --rm -v db-data:/source:ro -v $(pwd)/backup:/backup \
#   alpine tar czf /backup/db-backup.tar.gz -C /source .

# TODO: Yeni volume olustur ve yedegi geri yukle
# docker volume create db-data-restored
# docker run --rm -v db-data-restored:/target -v $(pwd)/backup:/backup \
#   alpine tar xzf /backup/db-backup.tar.gz -C /target

# TODO: Restore edilen veriyi dogrula
```

**Beklenen Sonuc:** Yedeklenen volume tam olarak geri yuklenmeli. Tum veriler korunmali.
**Ipucu:** `:ro` flag'i volume'u read-only mount eder. Buyuk veritabanlarinda `pg_dump` kullanmak daha guvenlidir.
:::

:::exercise
### Alistirma 17: Docker Container Lifecycle Management (Orta)

Container yasam dongusunu yonet: restart policy, graceful shutdown, temizlik.

```bash
# Farkli restart policy'ler
docker run -d --name always-up --restart=always nginx:alpine
docker run -d --name on-fail --restart=on-failure:3 nginx:alpine

# TODO: Container'i durdur ve restart davranisini gozlemle
# docker stop always-up && sleep 3 && docker ps | grep always-up

# TODO: Olu container'lari temizle
# docker container prune -f

# TODO: Tum kullanilmayan kaynaklari temizle
# docker system prune -a --volumes

# TODO: Container event'lerini izle
# docker events --filter type=container --since 5m

# TODO: Graceful shutdown test et (SIGTERM handler)
```

**Beklenen Sonuc:** `always` policy ile container otomatik yeniden baslamali. Graceful shutdown sirasinda cleanup tamamlanmali.
**Ipucu:** `--stop-timeout` SIGTERM'den SIGKILL'e kadar bekleme suresidir (varsayilan 10sn).
:::

:::exercise
### Alistirma 18: Dockerfile Security Scanning (Zor)

Dockerfile'i guvenlik aciklarina karsi tara ve sertlestir.

```dockerfile
# Guvensiz Dockerfile — sorunlari bul ve duzelt!
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
ENV API_KEY=sk-secret123
USER root
EXPOSE 3000 22
CMD ["node", "index.js"]
```

```bash
# TODO: Hadolint ile Dockerfile'i tara
# docker run --rm -i hadolint/hadolint < Dockerfile

# TODO: Trivy ile image guvenlik taramasi yap
# docker run --rm aquasec/trivy image my-app

# TODO: Guvenli versiyon yaz:
# - alpine veya distroless base image
# - Non-root user (addgroup + adduser)
# - ENV'de secret yok
# - Multi-stage build
# - Sadece gereken dosyalari COPY
# - Port 22 kaldir
```

**Beklenen Sonuc:** Hadolint en az 5 uyari vermeli. Guvenli versiyonda tum uyarilar giderilmeli.
**Ipucu:** Distroless image'lar shell bile icermez. `COPY --chown=node:node` ile dosya sahipligini non-root user'a ata.
:::

:::exercise
### Alistirma 19: Docker Production Deployment Simulasyonu (Zor)

Rolling update, health check ve load balancing ile production deployment simule et.

```yaml
# docker-compose.prod.yml
version: "3.8"
services:
  app:
    build: .
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
      restart_policy:
        condition: on-failure
        max_attempts: 3
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 30s
    # TODO: Resource limitleri ekle
    # TODO: Logging driver konfigurasyonu ekle

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      app:
        condition: service_healthy
    # TODO: nginx.conf ile upstream load balancing ekle
    # TODO: Rate limiting konfigur et
```

```bash
# TODO: Zero-downtime deployment test et
# Surekli health check yaparak yeni versiyon deploy et
# Hicbir istek basarisiz olmamali!
```

**Beklenen Sonuc:** Rolling update sirasinda zero downtime saglanmali. Health check basarisiz olan container'lar otomatik restart edilmeli.
**Ipucu:** `order: start-first` yeni container'i once baslatir, saglikli oldugunu dogruladiktan sonra eskiyi kaldirir.
:::

## Debugging Docker

:::code[bash]{title="Docker Debugging Komutları"}
# Container loglarını göster
docker logs my-container
docker logs -f my-container          # Follow mode (canlı)
docker logs --tail 100 my-container  # Son 100 satır

# Container içine shell aç
docker exec -it my-container sh      # Alpine
docker exec -it my-container bash    # Debian/Ubuntu

# Container detaylarını incele
docker inspect my-container

# Container resource kullanımı (CPU, RAM)
docker stats
docker stats my-container

# Container'daki process'leri gör
docker top my-container

# Container filesystem değişikliklerini gör
docker diff my-container

# Image layer'larını incele
docker history my-image:latest

# Build cache'i temizle
docker builder prune
:::

:::tip
Debugging sırasında `docker exec -it <container> sh` ile container'a girip dosya sistesini, environment variable'ları ve process'leri inceleyebilirsin. Ama production'da shell bulunmamasını sağla (distroless image kullan).
:::

## Docker Image Registry

:::code[bash]{title="Docker Hub ve Registry İşlemleri"}
# Docker Hub'a giriş
docker login

# Image'ı tag'le (registry/repo:tag formatı)
docker tag my-app:latest username/my-app:1.0.0
docker tag my-app:latest username/my-app:latest

# Image'ı push et
docker push username/my-app:1.0.0
docker push username/my-app:latest

# GitHub Container Registry (ghcr.io)
docker tag my-app:latest ghcr.io/username/my-app:1.0.0
docker push ghcr.io/username/my-app:1.0.0

# Private registry'den image çek
docker pull registry.company.com/my-app:latest
:::

:::english
**Image Tag Strategy:**
- `latest` - Most recent build (avoid in production)
- `1.0.0` - Semantic versioning (recommended for production)
- `abc123` - Git commit SHA (for traceability)
- `main-20260115` - Branch + date (for staging)

**Best Practice:** Never use `latest` tag in production. Always pin to a specific version like `node:22.12.0-alpine` instead of `node:22-alpine`.
:::

## Interview'da Docker Soruları

:::interview
**Soru 1:** "Docker image ile container arasındaki fark nedir?"
**Cevap:** Image read-only bir template'tir (class gibi), container ise image'ın çalışan bir instance'ıdır (object gibi). Bir image'dan birden fazla container oluşturabilirsiniz. Image Dockerfile'dan build edilir, container `docker run` ile başlatılır.

**Soru 2:** "Multi-stage build ne işe yarar ve neden kullanırız?"
**Cevap:** Multi-stage build, image boyutunu küçültmek ve güvenliği artırmak için kullanılır. Build aşamasında gerekli olan compiler, dev dependency'ler ve kaynak kod final image'a dahil edilmez. Tipik olarak 1GB+ image 100MB'a düşürülebilir. Ayrıca attack surface'i azaltır çünkü production image'da gereksiz tool'lar bulunmaz.

**Soru 3:** "Docker Compose'da `depends_on` ile `healthcheck` farkı nedir?"
**Cevap:** `depends_on` sadece container'ın başlatılma sırasını belirler, servisin hazır olduğunu garanti etmez. PostgreSQL container'ı başlamış olabilir ama henüz connection kabul etmiyor olabilir. `healthcheck` ile birlikte `condition: service_healthy` kullanarak servisin gerçekten hazır olduğundan emin oluruz.

**Soru 4:** "Container'ları neden root olarak çalıştırmamalıyız?"
**Cevap:** Container escape vulnerability durumunda, root yetkisiyle çalışan container host sistemine root erişimi sağlayabilir. Non-root user ile çalıştırmak, defense-in-depth prensibinin bir parçasıdır ve container breakout'un etkisini minimize eder.
:::

## Gerçek Dünya Docker Mimarileri

:::realworld
Modern bir SaaS uygulamasının Docker mimarisi tipik olarak şöyle görünür:

**Mikroservis Mimarisi:**
- API Gateway (nginx/envoy) - reverse proxy
- Auth Service - JWT/OAuth yönetimi
- User Service - kullanıcı CRUD
- Payment Service - ödeme işlemleri
- Notification Service - email/push
- PostgreSQL - ana veritabanı
- Redis - cache + session store
- RabbitMQ/Kafka - message queue
- Elasticsearch - full-text search
- Prometheus + Grafana - monitoring

Her biri ayrı bir container'da çalışır, Docker Compose (development) veya Kubernetes (production) ile orchestrate edilir.
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Docker'da container, image ve layer kavramlarini acikla. Union file system nasil calisir? Dockerfile'daki her instruction neden ayri bir layer oluşturur? Layer caching mekanizmasi build suresini nasil etkiler? Multi-stage build ile final image boyutunu nasil minimize ederim?"

**2. Pratik Uygulama:**
> "Bir Node.js + PostgreSQL + Redis uygulamasi icin Docker ortamı kur: Multi-stage Dockerfile (builder + runner), docker-compose.yml (3 servis, network, volume), .dockerignore, environment variables ve health check. Production-ready Dockerfile best practice'lerini uygula (non-root user, minimal base image, layer ordering)."
> Takip: "Simdi bu Docker setup'ina hot-reload ekle (development mode) ve production build ile development build arasindaki farklari docker-compose.override.yml ile yonet."

**3. Mukemmellik Icin:**
> "Docker image güvenliğini nasil saglarsim? Alpine vs distroless base image karsilastirmasi, multi-stage build ile secret yonetimi, image scanning (Trivy/Snyk), non-root user, read-only filesystem ve Docker Bench Security kullanarak container hardening checklist'i oluştur."

### Pair Programming Ipucu
Docker sorunlarinda AI'a docker logs, docker inspect veya Dockerfile ciktisini goster ve sor: "Container neden crash oluyor? Bu Dockerfile'da layer caching neden calismiyor? Image boyutum neden 1.2GB? Optimize et."
:::

:::must-note
## Defterine Yaz!

1. **Image vs Container:** Image = read-only template (class), Container = running instance (object). Dockerfile'dan image build edilir, image'dan container çalıştırılır.

2. **Layer Caching Sıralaması:** En az değişen dosyaları ÜSTTE kopyala. `COPY package.json pnpm-lock.yaml` → `RUN pnpm install --frozen-lockfile` → `COPY . .` sıralaması build süresini dramatik şekilde kısaltır.

3. **Multi-Stage Build:** Production image'larda ZORUNLU. Builder stage'de derleme yap, production stage'de sadece output'u al. Image boyutu 10x küçülür, güvenlik artar.

4. **Docker Compose `depends_on` + `healthcheck`:** Sadece `depends_on` yetmez! Database container'ı başlamış ama hazır olmayabilir. `condition: service_healthy` ile gerçek hazırlığı kontrol et.

5. **Güvenlik Üçlüsü:** Non-root user (`USER node`), `.dockerignore`'da `.env`, minimal base image (`alpine` veya `distroless`). Bu üçünü her Dockerfile'da uygula.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir

Senior developer Docker öğrenirken:

1. **"Neden?" ile başlar:** Container teknolojisinin altındaki Linux namespace'leri ve cgroup'ları anlar. `unshare` ve `nsenter` komutlarıyla container'ın aslında ne olduğunu kavrar.

2. **Security-first düşünür:** Image'ı Trivy/Snyk ile tarar, non-root user kullanır, distroless image'ları tercih eder, secret management'ı Docker Secrets veya HashiCorp Vault ile yapar.

3. **Production-ready Dockerfile yazar:** Multi-stage build, health check, tini init process, graceful shutdown handler, proper signal handling (SIGTERM/SIGINT).

4. **Build pipeline entegrasyonu yapar:** Dockerfile'ı CI/CD pipeline'ına entegre eder, image'ı vulnerability scan'den geçirir, semantic versioning ile tag'ler, immutable tag policy uygular.

5. **Monitoring düşünür:** Container metric'lerini Prometheus ile toplar, log'ları centralized log system'a gönderir (ELK/Loki), alerting kurar.

**CTO bakış açısı:** Docker sadece bir araç değil, deployment strategisi. "Hangi orchestrator (Kubernetes vs ECS vs Nomad)?", "Image registry güvenliği?", "Container runtime seçimi (containerd vs cri-o)?", "Cost optimization (right-sizing)?". Teknolojiyi mimari kararların bir parçası olarak değerlendirir.
:::

:::knowledge-check
1. Docker image ile container arasındaki temel fark nedir?
2. Dockerfile'da `COPY package*.json ./` komutunu `COPY . .`'den önce yazmanın sebebi nedir?
3. Multi-stage build kullanmadan bir Node.js + TypeScript uygulamasının image boyutu yaklaşık ne olur?
4. `docker compose down -v` komutunun `docker compose down`'dan farkı nedir?
5. Neden container'ları root kullanıcı ile çalıştırmamalıyız?
:::

:::external-resource
- [Docker Resmi Dokümantasyon](https://docs.docker.com/) - Kapsamlı referans
- [Docker Hub](https://hub.docker.com/) - Public image registry
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) - Resmi best practice rehberi
- [Docker Compose Spesifikasyonu](https://docs.docker.com/compose/compose-file/) - Compose dosyası referansı
- [Hadolint](https://github.com/hadolint/hadolint) - Dockerfile linter
- [Dive](https://github.com/wagoodman/dive) - Docker image layer analizi
- [Trivy](https://github.com/aquasecurity/trivy) - Container vulnerability scanner
:::
