---
title: "Üretim Ortamına Deployment: Kodunu Dünyaya Aç"
id: "mod-13-docker/lesson-03"
estimated_minutes: 90
order: 3
tags: ["deployment", "vercel", "railway", "aws", "ci-cd", "github-actions", "production", "devops", "cloud", "netlify", "monitoring"]
prerequisites: ["mod-13-docker/lesson-01"]
---

# Üretim Ortamına Deployment: Kodunu Dünyaya Aç

:::realworld
Spotify'ın mühendislik ekibi günde 100'den fazla deployment yapıyor. GitHub kendisi saatte birkaç kez production'a deploy ediyor. Netflix tek bir tıklamayla binlerce microservice'i güncelleyebiliyor. Kod yazmak işin yarısı — o kodu güvenli, hızlı ve kesintisiz şekilde kullanıcılara ulaştırmak asıl mühendislik. Portfolyo projeni localhost'ta gösteren junior developer ile "şu linke bak, canlıda çalışıyor" diyen developer arasındaki fark, iş teklifini belirliyor. Bu ders seni o farkın doğru tarafına koyacak.
:::

:::senior-learns
Senior developer deployment'ı bir "son adım" olarak görmez — projenin ilk gününde CI/CD pipeline'ını kurar, staging ortamını ayarlar ve her PR'ın otomatik preview deployment'ı olmasını sağlar. Deployment, development workflow'unun ayrılmaz parçasıdır.

**Karar Verme Sureci — Platform Secimi:**
- **Vercel/Netlify**: Frontend ve Next.js icin optimize, preview deployment, edge functions. Trade-off: Backend sinirli (serverless function limitleri), vendor lock-in riski, buyuk trafiklerde pahali olabilir. Kullanim: React/Next.js frontend, JAMstack siteleri.
- **Railway/Render**: Heroku alternatifi, container-based, kolay setup. Trade-off: AWS kadar esnek degil, buyuk olcekte maliyet kontrolu zor. Kullanim: MVP, startup, hizli prototip, kucuk-orta backend.
- **AWS (ECS/EKS/Lambda)**: Tam kontrol, her olcekte calisir, 200+ servis. Trade-off: Ogrenme egrisi cok dik, basit bir deploy icin bile IAM, VPC, security group, load balancer konfigurasyonu gerekir. Kullanim: Enterprise, buyuk olcek, compliance gereksinimleri.
- **Fly.io**: Container-based, global edge deployment, PostgreSQL built-in. Trade-off: AWS kadar olgun degil, community kucuk. Kullanim: Globally distributed API'ler, low-latency gereken servisler.
- **Senior karar agaci**: "Sadece frontend mi? Vercel. Backend + DB ile MVP mi? Railway. Enterprise, compliance, buyuk olcek mi? AWS. Global latency kritik mi? Fly.io."

**Anti-pattern Farkindaligi:**
- **"Works on my machine" deployment**: Docker kullanmadan direkt sunucuya kopyalamak. Environment farklilikları, dependency uyumsuzluklari. Bir keresinde production'da Python 3.9, development'ta 3.11 oldugu icin walrus operator (:=) kullanan kod production'da patladi. Docker ile environment tutarliligi sagla.
- **Manuel deployment**: SSH ile sunucuya girip `git pull && restart`. Kim ne zaman deploy etti belli degil, rollback imkansiz, gece 3'te deploy eden kisi hata yaparsa kimse bulamaz. CI/CD pipeline ile her deploy otomatik, loglanmis ve rollback edilebilir olmali.
- **Environment variable'lari koda gomme**: `.env` dosyasini git'e push etmek. Production secrets'lari GitHub'da. Cozum: platform-specific secret management (Vercel env, AWS Secrets Manager, Railway variables).

**Gercek Dunya Deneyimi:** Bir startup'ta 6 ay boyunca manuel deployment yaptik — SSH ile sunucuya girip `git pull`. Bir gece deploy sirasinda migration unutuldu, production DB schema uyumsuz kaldi, 4 saat downtime. Ertesi gun GitHub Actions + Docker + rolling deployment kurduk. Sonrasinda 200+ deployment, sifir downtime. Ders: CI/CD'ye harcanan 2 gun, ileride yuzlerce saat kurtarir.
:::

:::must-note
**Kesinlikle not al:** Deployment bilgisi mülakatlarda "bonus" değil, "eleme kriteri"dir. "Projeyi nasıl deploy edersin?" sorusuna "bilmiyorum" demek, o pozisyonu kaybetmek demektir. Bu derste öğrendiğin her platformu en az bir kez dene. Deneyim > teori.
:::

## 1. Frontend Deployment

Frontend deployment, modern web geliştirmenin en kolay ama en kritik parçasıdır. Doğru platform seçimi, projenin performansını ve developer deneyimini doğrudan etkiler.

### Vercel: Next.js & React Deployment

Vercel, Next.js'in yaratıcıları tarafından geliştirilen bir platformdur. React, Next.js, Svelte ve diğer modern framework'ler için optimize edilmiştir.

:::code[Vercel ile Next.js Deploy Etme]
```bash
# 1. Vercel CLI'ı global olarak kur
pnpm add -g vercel

# 2. Proje dizinine git
cd my-nextjs-app

# 3. Vercel'e login ol
vercel login

# 4. İlk deployment — interaktif wizard başlar
vercel

# Sorular:
# ? Set up and deploy? → Y
# ? Which scope? → Kendi hesabın
# ? Link to existing project? → N
# ? What's your project's name? → my-nextjs-app
# ? In which directory is your code located? → ./
# ? Want to modify these settings? → N

# 5. Production deployment (preview değil, gerçek production)
vercel --prod

# 6. Environment variable ekleme
vercel env add DATABASE_URL production
vercel env add NEXT_PUBLIC_API_URL production

# 7. Environment variable'ları listeleme
vercel env ls
```
:::

:::code[vercel.json Konfigürasyonu]
```json
{
  "buildCommand": "pnpm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["fra1"],
  "env": {
    "NEXT_PUBLIC_APP_ENV": "production"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store, max-age=0" }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```
:::

**Vercel Preview Deployments:** Her PR açtığında Vercel otomatik olarak bir preview URL oluşturur. Bu URL'i PR'da paylaşarak ekip arkadaşlarının değişiklikleri canlı görmesini sağlarsın. Merge edildiğinde otomatik olarak production'a deploy olur.

### Netlify: Static & SSG Sites

Netlify, statik siteler ve JAMstack uygulamaları için mükemmeldir. Drag & drop deployment bile destekler ama CLI üzerinden yapmak profesyonel yaklaşımdır.

:::code[Netlify ile Deploy Etme]
```bash
# 1. Netlify CLI kur
pnpm add -g netlify-cli

# 2. Login ol
netlify login

# 3. Yeni site oluştur ve deploy et
netlify init

# 4. Build komutunu ayarla
# Build command: pnpm run build
# Publish directory: dist (Vite) veya build (CRA) veya out (Next.js export)

# 5. Manuel deploy (test amaçlı)
netlify deploy --dir=dist

# 6. Production deploy
netlify deploy --prod --dir=dist

# 7. Environment variable ekleme (Netlify UI'dan veya CLI)
netlify env:set API_URL "https://api.example.com"
netlify env:set NODE_ENV "production"
```
:::

:::code[netlify.toml Konfigürasyonu]
```toml
[build]
  command = "pnpm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

# SPA routing — tüm route'ları index.html'e yönlendir
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# API proxy — CORS sorunlarını çözer
[[redirects]]
  from = "/api/*"
  to = "https://api.example.com/:splat"
  status = 200
  force = true

# Custom headers
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Content-Security-Policy = "default-src 'self'"

# Cache static assets agresif şekilde
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```
:::

### Custom Domain & DNS Konfigürasyonu

:::code[DNS Konfigürasyonu]
```
# Vercel veya Netlify için DNS kayıtları (domain sağlayıcında ayarla)

# A Record — root domain (example.com)
Type: A
Name: @
Value: 76.76.21.21  (Vercel'in IP'si — platformuna göre değişir)

# CNAME Record — www subdomain
Type: CNAME
Name: www
Value: cname.vercel-dns.com  (veya platformun verdiği değer)

# CNAME Record — API subdomain
Type: CNAME
Name: api
Value: api-server.railway.app

# DNS propagation kontrol (terminalde)
# dig komutu ile DNS kaydının yayılıp yayılmadığını kontrol et
dig example.com A +short
dig www.example.com CNAME +short

# Alternatif: nslookup
nslookup example.com
```
:::

:::beginner-mistake
**Hata:** Domain'i ekleyip SSL sertifikasının otomatik oluşmasını beklememek. DNS kayıtlarını ekledikten sonra SSL sertifikası 5-30 dakika içinde otomatik oluşur (Let's Encrypt). Bu sürede "güvenli değil" uyarısı görebilirsin — panik yapma, bekle. Propagation 24-48 saat sürebilir ama genelde 10 dakikada tamamlanır.
:::

## 2. Backend Deployment

Backend deployment, frontend'den daha karmaşıktır çünkü sürekli çalışan bir process, veritabanı bağlantıları ve environment variable'lar gerektirir.

### Railway: FastAPI & Express Deployment

Railway, backend uygulamalarını deploy etmek için en kolay platformlardan biridir. GitHub repo'sundan otomatik deploy, veritabanı provisioning ve environment variable yönetimi sunar.

:::code[Railway ile FastAPI Deploy Etme]
```bash
# 1. Railway CLI kur
pnpm add -g @railway/cli

# 2. Login ol
railway login

# 3. Yeni proje oluştur
railway init

# 4. GitHub repo'sunu bağla
railway link

# 5. PostgreSQL veritabanı ekle
railway add --plugin postgresql

# 6. Redis ekle (opsiyonel — cache, session, queue için)
railway add --plugin redis

# 7. Environment variable ekle
railway variables set DATABASE_URL="${{Postgres.DATABASE_URL}}"
railway variables set SECRET_KEY="super-secret-key-change-this"
railway variables set ALLOWED_ORIGINS="https://myapp.vercel.app"

# 8. Deploy et
railway up

# 9. Logları izle
railway logs
```
:::

:::code[FastAPI Production Konfigürasyonu — Procfile ve pyproject.toml]
```
# Procfile (Railway/Render için)
web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4
```

```toml
# pyproject.toml
[project]
name = "my-api"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "psycopg2-binary>=2.9.9",
    "python-dotenv>=1.0.0",
    "pydantic-settings>=2.1.0",
    "httpx>=0.26.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff>=0.2.0",
]
```

```python
# backend/config.py — Production-ready settings
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    allowed_origins: str = "http://localhost:5173"
    environment: str = "development"
    debug: bool = False

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

```python
# backend/main.py — Production-ready FastAPI app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: veritabanı bağlantısı, cache warmup vb.
    print(f"Starting in {settings.environment} mode")
    yield
    # Shutdown: bağlantıları kapat
    print("Shutting down gracefully")


app = FastAPI(
    title="My API",
    docs_url="/docs" if settings.debug else None,  # Production'da docs kapat
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}
```
:::

### Render: Alternatif Backend Platform

Render, Railway'e benzer ama free tier'ı daha cömerttir. Web service, cron job, static site ve veritabanı barındırabilir.

:::code[Render Konfigürasyonu — render.yaml]
```yaml
# render.yaml — Infrastructure as Code
services:
  - type: web
    name: my-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: my-db
          property: connectionURI
      - key: SECRET_KEY
        generateValue: true
      - key: ENVIRONMENT
        value: production
    healthCheckPath: /health
    autoDeploy: true

  - type: web
    name: my-frontend
    runtime: static
    buildCommand: pnpm install && pnpm run build
    staticPublishPath: ./dist
    headers:
      - path: /*
        name: X-Frame-Options
        value: DENY
    routes:
      - type: rewrite
        source: /*
        destination: /index.html

databases:
  - name: my-db
    plan: free
    databaseName: myapp
    postgresMajorVersion: "16"
```
:::

### Veritabanı Hosting

:::code[Neon PostgreSQL — Serverless Postgres]
```bash
# Neon: Serverless PostgreSQL — cold start'sız, branch desteği ile
# 1. neon.tech'te hesap oluştur
# 2. Proje ve veritabanı oluştur
# 3. Connection string'i al:

# Connection string formatı
DATABASE_URL="postgresql://user:password@ep-cool-name-123456.eu-central-1.aws.neon.tech/mydb?sslmode=require"

# Neon'un avantajı: branch desteği (Git gibi veritabanı branching)
# Main branch = production
# Dev branch = development (production verisiyle test et)
```
:::

:::code[Upstash Redis — Serverless Redis]
```python
# Upstash: Serverless Redis — per-request pricing, REST API desteği
# upstash.com'dan Redis instance oluştur

# Python ile kullanım
import redis

# Upstash connection (REST-based, serverless uyumlu)
r = redis.from_url(
    "rediss://default:your-password@eu1-sunny-cat-12345.upstash.io:6379"
)

# Cache örneği
def get_user_cached(user_id: str):
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    user = db.query(User).filter(User.id == user_id).first()
    r.setex(f"user:{user_id}", 3600, json.dumps(user.dict()))  # 1 saat TTL
    return user
```
:::

:::beginner-mistake
**Hata:** Veritabanı connection string'ini koda hardcode etmek veya Git'e push etmek. Bir kez GitHub'a push edilen secret, botlar tarafından saniyeler içinde taranır ve kötüye kullanılır. Her zaman environment variable kullan, `.env` dosyasını `.gitignore`'a ekle. Eğer yanlışlıkla push ettiysen, sadece commit'i silmek yetmez — secret'ı hemen rotate et (yeni password oluştur).
:::

## 3. AWS Temelleri — Senior Seviye

AWS, endüstri standardıdır. Büyük şirketlerin çoğu AWS kullanır. Her servisin ne yaptığını bilmek, senior pozisyonlar için zorunludur.

:::deha-tip
AWS'i öğrenirken "hepsini bilmeliyim" baskısına kapılma. Bir senior bile AWS'in 200+ servisinin hepsini bilmez. Şu 5 servisi iyi öğren: EC2, S3, RDS, Lambda, IAM. Bu beşli, mülakatlarda sorulan AWS sorularının %80'ini kapsar. Geri kalanını ihtiyaç oldukça öğrenirsin. AWS'i öğrenmenin en iyi yolu, kendi projeni deploy etmektir — free tier ile başla.
:::

:::code[AWS CLI Kurulum ve Yapılandırma]
```bash
# 1. AWS CLI kurulumu (resmi yöntem)
# macOS/Linux:
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Windows: AWS website'den MSI installer indir

# 2. Credentials yapılandırma
aws configure
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: wJal...
# Default region name: eu-central-1
# Default output format: json

# 3. Doğrulama
aws sts get-caller-identity
```
:::

### EC2: Virtual Server

:::code[EC2 Instance Oluşturma ve Konfigürasyonu]
```bash
# 1. Key pair oluştur (SSH erişimi için)
aws ec2 create-key-pair \
  --key-name my-app-key \
  --query 'KeyMaterial' \
  --output text > my-app-key.pem

chmod 400 my-app-key.pem

# 2. Security group oluştur (firewall kuralları)
aws ec2 create-security-group \
  --group-name my-app-sg \
  --description "Security group for my app"

# SSH (22), HTTP (80), HTTPS (443) portlarını aç
aws ec2 authorize-security-group-ingress \
  --group-name my-app-sg \
  --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-name my-app-sg \
  --protocol tcp --port 80 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-name my-app-sg \
  --protocol tcp --port 443 --cidr 0.0.0.0/0

# 3. EC2 instance başlat (Ubuntu 22.04, t2.micro = free tier)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name my-app-key \
  --security-groups my-app-sg \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-app-server}]'

# 4. SSH ile bağlan
ssh -i my-app-key.pem ubuntu@<EC2-PUBLIC-IP>

# 5. Sunucuyu hazırla
sudo apt update && sudo apt upgrade -y
sudo apt install -y nginx python3.13 python3.13-venv

# 6. Uygulamayı deploy et
git clone https://github.com/username/my-api.git
cd my-api
python3.13 -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt  # uv tercih edilir, yoksa pip de kullanılabilir

# 7. systemd service oluştur (uygulama crash olursa otomatik restart)
sudo tee /etc/systemd/system/myapp.service << 'UNIT'
[Unit]
Description=My FastAPI App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/my-api
ExecStart=/home/ubuntu/my-api/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3
Environment=ENVIRONMENT=production
EnvironmentFile=/home/ubuntu/my-api/.env

[Install]
WantedBy=multi-user.target
UNIT

sudo systemctl enable myapp
sudo systemctl start myapp
sudo systemctl status myapp
```
:::

### S3: Static File Hosting & Storage

:::code[S3 ile Static Website Hosting]
```bash
# 1. Bucket oluştur
aws s3 mb s3://my-app-frontend-2026 --region eu-central-1

# 2. Static website hosting'i etkinleştir
aws s3 website s3://my-app-frontend-2026 \
  --index-document index.html \
  --error-document index.html

# 3. Bucket policy — public read erişimi
aws s3api put-bucket-policy --bucket my-app-frontend-2026 --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-app-frontend-2026/*"
  }]
}'

# 4. Build dosyalarını yükle
pnpm run build
aws s3 sync dist/ s3://my-app-frontend-2026 --delete

# 5. Cache header'ları ayarla
aws s3 sync dist/assets/ s3://my-app-frontend-2026/assets/ \
  --cache-control "public, max-age=31536000, immutable"

aws s3 cp dist/index.html s3://my-app-frontend-2026/index.html \
  --cache-control "no-cache, no-store, must-revalidate"
```
:::

### Lambda: Serverless Functions

:::code[AWS Lambda ile Serverless API]
```python
# lambda_function.py
import json


def lambda_handler(event, context):
    """AWS Lambda handler — her request'te bu fonksiyon çağrılır."""
    http_method = event.get("httpMethod", "GET")
    path = event.get("path", "/")
    body = json.loads(event.get("body", "{}")) if event.get("body") else {}

    if path == "/api/hello" and http_method == "GET":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"message": "Hello from Lambda!"}),
        }

    if path == "/api/process" and http_method == "POST":
        result = process_data(body)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result),
        }

    return {
        "statusCode": 404,
        "body": json.dumps({"error": "Not found"}),
    }


def process_data(data: dict) -> dict:
    return {"processed": True, "input_keys": list(data.keys())}
```

```bash
# Lambda deployment
# 1. Kodu zip'le
zip -r function.zip lambda_function.py

# 2. Lambda fonksiyonu oluştur
aws lambda create-function \
  --function-name my-api-handler \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::123456789:role/lambda-execution-role \
  --timeout 30 \
  --memory-size 256

# 3. API Gateway ile HTTP endpoint oluştur (AWS Console'dan daha kolay)
# API Gateway → Create API → HTTP API → Lambda integration
```
:::

### IAM: Güvenlik Temelleri

:::warning
AWS IAM yanlış yapılandırıldığında faturan binlerce dolara çıkabilir. Root hesabı günlük işler için kullanma, her zaman IAM user oluştur. MFA (Multi-Factor Authentication) aktif et. Access key'leri asla Git'e push etme. Billing alert kur — free tier limitini aştığında mail alsın.
:::

:::code[IAM Best Practices]
```bash
# 1. IAM user oluştur (root hesap yerine)
aws iam create-user --user-name developer

# 2. Programmatic access için access key oluştur
aws iam create-access-key --user-name developer

# 3. Policy oluştur — minimum yetki prensibi (Least Privilege)
aws iam put-user-policy --user-name developer --policy-name dev-policy --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-app-frontend-2026",
        "arn:aws:s3:::my-app-frontend-2026/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "lambda:UpdateFunctionCode",
        "lambda:InvokeFunction"
      ],
      "Resource": "arn:aws:iam::123456789:function:my-api-*"
    }
  ]
}'

# 4. Billing alarm oluştur (CloudWatch)
aws cloudwatch put-metric-alarm \
  --alarm-name "billing-alarm-10usd" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:123456789:billing-alerts
```
:::

## 4. CI/CD Pipeline — GitHub Actions

CI/CD (Continuous Integration / Continuous Deployment), her kod değişikliğinin otomatik olarak test edilip deploy edilmesi sürecidir. Manuel deployment yapan ekip = hata yapan ekip.

:::code[Full-Stack CI/CD Pipeline — GitHub Actions]
```yaml
# .github/workflows/deploy.yml
name: Build, Test & Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: "20"
  PYTHON_VERSION: "3.11"

jobs:
  # ========== FRONTEND ==========
  frontend-test:
    name: Frontend - Lint & Test
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend

    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: "pnpm"
          cache-dependency-path: frontend/pnpm-lock.yaml

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm run lint

      - name: Type check
        run: pnpm run typecheck

      - name: Run tests
        run: pnpm run test -- --coverage

      - name: Build
        run: pnpm run build

  # ========== BACKEND ==========
  backend-test:
    name: Backend - Lint & Test
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./backend

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Setup Python
        run: uv python install ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: uv sync

      - name: Lint with ruff
        run: uv run ruff check .

      - name: Format check
        run: uv run ruff format --check .

      - name: Run tests
        run: uv run pytest --cov=. --cov-report=xml -v
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
          SECRET_KEY: test-secret-key
          ENVIRONMENT: test

  # ========== DEPLOY ==========
  deploy-frontend:
    name: Deploy Frontend to Vercel
    needs: [frontend-test]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: "--prod"
          working-directory: ./frontend

  deploy-backend:
    name: Deploy Backend to Railway
    needs: [backend-test]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: pnpm add -g @railway/cli

      - name: Deploy to Railway
        run: railway up --service my-api
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```
:::

### Environment Secrets Management

:::code[GitHub Secrets Yönetimi]
```bash
# GitHub CLI ile secret ekleme
gh secret set VERCEL_TOKEN --body "your-vercel-token"
gh secret set RAILWAY_TOKEN --body "your-railway-token"
gh secret set DATABASE_URL --body "postgresql://..."

# Environment-specific secrets (staging vs production)
# GitHub → Settings → Environments → New environment

# staging environment
gh secret set DATABASE_URL --env staging --body "postgresql://staging-db..."
gh secret set API_URL --env staging --body "https://staging-api.example.com"

# production environment
gh secret set DATABASE_URL --env production --body "postgresql://prod-db..."
gh secret set API_URL --env production --body "https://api.example.com"
```
:::

:::code[Staging vs Production Workflow]
```yaml
# .github/workflows/staging.yml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging  # GitHub environment protection rules

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        run: |
          echo "Deploying to staging..."
          railway up --service my-api --environment staging
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

      - name: Run smoke tests
        run: |
          # Deployment'ın başarılı olduğunu doğrula
          sleep 10
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://staging-api.example.com/health)
          if [ "$STATUS" != "200" ]; then
            echo "Smoke test failed! Status: $STATUS"
            exit 1
          fi
          echo "Smoke test passed!"

      - name: Notify on Slack (opsiyonel)
        if: success()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"Staging deployment successful for commit ${{ github.sha }}"}'
```
:::

### Rollback Stratejisi

:::code[Rollback Mekanizması]
```bash
# Git-based rollback — en basit ve güvenilir yöntem

# 1. Son başarılı deployment'ı bul
git log --oneline -10

# 2. O commit'e geri dön (yeni commit oluşturarak — history'yi korur)
git revert HEAD --no-edit
git push origin main
# CI/CD otomatik olarak revert'i deploy eder

# 3. Birden fazla commit geri almak gerekirse
git revert HEAD~3..HEAD --no-edit
git push origin main

# Vercel'de rollback
vercel rollback  # Son başarılı deployment'a döner

# Railway'de rollback
railway rollback  # Önceki deployment'a döner
```
:::

:::beginner-mistake
**Hata:** Rollback planı olmadan production'a deploy etmek. "Bir şey olursa düzeltiriz" yaklaşımı gece 3'te pager çaldığında işe yaramaz. Her deployment'tan önce "bu deployment başarısız olursa nasıl geri dönerim?" sorusunu sor. Cevabını bilmiyorsan deploy etme.
:::

## 5. Production Checklist

Production'a çıkmadan önce kontrol etmen gereken her şey. Bu listeyi her deployment'tan önce gözden geçir.

### Environment Variables Yönetimi

:::code[.env Dosya Yapısı ve Yönetimi]
```bash
# .env.example — Git'e commit edilir, gerçek değerler yerine placeholder'lar
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
SECRET_KEY=change-me-in-production
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=http://localhost:5173
ENVIRONMENT=development
SENTRY_DSN=
SMTP_HOST=
SMTP_PORT=

# .env — Git'e ASLA commit edilmez
# Bu dosya .gitignore'da olmalı

# .gitignore
.env
.env.local
.env.production
*.pem
*.key
```
:::

### Monitoring & Logging

:::code[Sentry ile Error Tracking (Python)]
```python
# backend/main.py — Sentry entegrasyonu
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from config import get_settings

settings = get_settings()

if settings.environment == "production":
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.1,  # %10 transaction trace et (maliyet kontrolü)
        profiles_sample_rate=0.1,
        environment=settings.environment,
    )


# Uptime monitoring — health check endpoint
@app.get("/health")
async def health_check():
    """External monitoring servisleri bu endpoint'i kontrol eder."""
    try:
        # Veritabanı bağlantısını test et
        await db.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "version": settings.app_version,
        "environment": settings.environment,
    }
```
:::

:::code[Structured Logging]
```python
# backend/logging_config.py
import logging
import json
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Production-grade JSON log formatter."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id

        return json.dumps(log_entry)


def setup_logging(environment: str):
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    if environment == "production":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )

    logger.addHandler(handler)
    return logger
```
:::

### Performance: CDN, Caching, Compression

:::code[Nginx Reverse Proxy + Cache + Compression]
```nginx
# /etc/nginx/sites-available/myapp
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL (Let's Encrypt / Certbot)
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Gzip compression — response boyutunu %70-80 küçültür
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
    gzip_min_length 1000;
    gzip_comp_level 6;

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Static files — agresif cache
    location /assets/ {
        root /var/www/myapp;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # API proxy — backend'e yönlendir
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Rate limiting
        limit_req zone=api burst=20 nodelay;
    }

    # Frontend SPA
    location / {
        root /var/www/myapp;
        try_files $uri $uri/ /index.html;
    }
}

# Rate limiting zone (http bloğunda tanımla)
# limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
```
:::

### Security Hardening

:::code[Production Security Checklist — Kod ile]
```python
# backend/middleware/security.py
from fastapi import Request, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Basit in-memory rate limiter. Production'da Redis kullan."""

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Eski istekleri temizle
        self.requests[client_ip] = [
            t for t in self.requests[client_ip]
            if now - t < self.window_seconds
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests")

        self.requests[client_ip].append(now)
        response = await call_next(request)
        return response


# main.py'de kullanım
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
```
:::

## 6. Zero-Downtime Deployment

Kullanıcıların hiçbir kesinti yaşamadan yeni versiyonu alması. Bu, production-grade deployment'ın temel gereksinimi.

### Blue-Green Deployment

Blue-green deployment'ta iki özdeş ortam vardır:
- **Blue:** Şu an production trafiğini alan ortam
- **Green:** Yeni versiyonun deploy edildiği ortam

Yeni versiyon green ortama deploy edilir, test edilir, başarılıysa trafik green'e yönlendirilir. Sorun olursa anında blue'ya geri dönülür.

:::code[Blue-Green Deployment — Nginx ile]
```nginx
# /etc/nginx/conf.d/upstream.conf
# Blue-green deployment: iki backend arasında geçiş

# Aktif olan ortam (blue veya green)
upstream backend_active {
    server 127.0.0.1:8000;  # blue
}

upstream backend_standby {
    server 127.0.0.1:8001;  # green
}

# Geçiş yapmak için:
# 1. Yeni versiyonu standby'a deploy et
# 2. Standby'ı test et (health check)
# 3. upstream'leri swap et
# 4. nginx -s reload
```

```bash
#!/bin/bash
# scripts/blue-green-deploy.sh

ACTIVE_PORT=$(cat /tmp/active_port 2>/dev/null || echo "8000")

if [ "$ACTIVE_PORT" = "8000" ]; then
    DEPLOY_PORT="8001"
    DEPLOY_ENV="green"
else
    DEPLOY_PORT="8000"
    DEPLOY_ENV="blue"
fi

echo "Deploying to $DEPLOY_ENV (port $DEPLOY_PORT)..."

# 1. Yeni versiyonu deploy et
cd /home/ubuntu/my-api-$DEPLOY_ENV
git pull origin main
source .venv/bin/activate
uv pip install -r requirements.txt
sudo systemctl restart myapp-$DEPLOY_ENV

# 2. Health check — yeni versiyon hazır mı?
echo "Waiting for health check..."
for i in $(seq 1 30); do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$DEPLOY_PORT/health)
    if [ "$STATUS" = "200" ]; then
        echo "Health check passed!"
        break
    fi
    if [ "$i" = "30" ]; then
        echo "Health check failed! Aborting deployment."
        exit 1
    fi
    sleep 2
done

# 3. Trafiği yeni versiyona yönlendir
sudo sed -i "s/server 127.0.0.1:$ACTIVE_PORT/server 127.0.0.1:$DEPLOY_PORT/" \
    /etc/nginx/conf.d/upstream.conf
sudo nginx -s reload

# 4. Aktif portu kaydet
echo "$DEPLOY_PORT" > /tmp/active_port
echo "Deployment to $DEPLOY_ENV complete! Traffic switched to port $DEPLOY_PORT"
echo "Rollback: change upstream back to port $ACTIVE_PORT"
```
:::

### Rolling Updates & Health Checks

:::code[Docker Compose ile Rolling Update]
```yaml
# docker-compose.prod.yml
services:
  api:
    image: myapp/api:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1        # Bir seferde 1 container güncelle
        delay: 10s             # Güncellemeler arası 10 saniye bekle
        failure_action: rollback
        order: start-first     # Yeni container başlat, sonra eskiyi durdur
      rollback_config:
        parallelism: 0
        order: stop-first
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s       # İlk 30 saniye health check yapma (startup süresi)
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      api:
        condition: service_healthy
```
:::

:::deha-tip
Zero-downtime deployment'ın sırrı health check'tir. Health check olmadan load balancer, henüz hazır olmayan bir container'a trafik yönlendirebilir. Health check endpoint'in sadece HTTP 200 dönmemeli — veritabanı bağlantısını, cache bağlantısını ve kritik dependency'leri de kontrol etmeli. Shallow health check (sadece 200 dönmek) yetmez, deep health check (tüm bağımlılıkları kontrol etmek) gerekir.
:::

## Mülakat Soruları

:::interview
**Soru 1:** "Bir web uygulamasını production'a deploy etme sürecini baştan sona anlatır mısın? CI/CD pipeline nasıl kurarsın?"

**Beklenen cevap:** Bu soru end-to-end bilgiyi test eder. Güçlü bir cevap şunları kapsar:

1. **Kod yönetimi:** Feature branch → PR → code review → merge to main
2. **CI pipeline:** GitHub Actions ile lint → type check → unit test → integration test
3. **CD pipeline:** Test'ler geçtikten sonra staging'e otomatik deploy → smoke test → production'a deploy
4. **Infrastructure:** Frontend (Vercel/CDN) + Backend (Railway/AWS) + Database (Neon/RDS) + Cache (Upstash/Redis)
5. **Güvenlik:** Environment variables management, secrets rotation, HTTPS, security headers
6. **Monitoring:** Error tracking (Sentry), uptime monitoring, structured logging
7. **Rollback:** Sorun olduğunda önceki versiyona hızlı dönüş stratejisi

Bu soruya "Vercel'e push ederim" demek junior cevabı. Tüm pipeline'ı anlatan kişi senior cevabı verir.
:::

:::interview
**Soru 2:** "Production'daki bir API aniden yavaşladı. Nasıl debug edersin ve çözersin?"

**Beklenen cevap:** Sistematik yaklaşım beklenir:

1. **Monitoring kontrol:** Grafana/CloudWatch dashboard'larına bak — CPU, memory, disk I/O normal mi?
2. **Log analizi:** Son deployment'tan sonra mı başladı? Error rate arttı mı? Structured log'larda pattern ara
3. **APM kontrol:** Sentry/New Relic'te hangi endpoint yavaş? N+1 query var mı?
4. **Veritabanı:** Slow query log'larına bak, EXPLAIN ANALYZE çalıştır, connection pool doluluk oranına bak
5. **External dependencies:** Üçüncü parti API'lar yavaşladı mı? Timeout'lar arttı mı?
6. **Quick fixes:** Cache ekle, query optimize et, index ekle, horizontal scale yap
7. **Rollback:** Son deployment suçluysa hemen geri al, sonra root cause analizi yap

"Sunucuyu yeniden başlatırım" cevabı kırmızı bayraktır. Sistematik debug sürecini anlatan kişi alınır.
:::

## Egzersizler

:::exercise[Egzersiz 1: Frontend'i Vercel'e Deploy Et]
**Görev:** Bir React/Next.js uygulaması oluştur ve Vercel'e deploy et.

**Adımlar:**
1. `pnpm create next-app@latest my-deploy-test` ile proje oluştur
2. GitHub'a push et
3. Vercel CLI ile deploy et: `vercel --prod`
4. Custom bir environment variable ekle ve sayfada göster
5. Bir değişiklik yap, push et — preview deployment URL'ini kontrol et
6. Production'a merge et — otomatik deploy'u doğrula

**Başarı kriterleri:**
- Canlı URL'den siteye erişilebilmeli
- Environment variable doğru çalışmalı
- Preview deployment ve production deployment ayrı URL'lerde olmalı
:::

:::exercise[Egzersiz 2: Full-Stack Deployment — Backend + Database]
**Görev:** FastAPI backend'ini Railway'e, PostgreSQL veritabanıyla birlikte deploy et.

**Adımlar:**
1. Basit bir FastAPI uygulaması oluştur (CRUD endpoints + health check)
2. `pyproject.toml` ve `Procfile` hazırla
3. Railway'de PostgreSQL veritabanı oluştur
4. Backend'i Railway'e deploy et
5. Frontend'den API'ya istek at — CORS ayarlarını yap
6. Logları kontrol et, health check endpoint'ini test et

**Başarı kriterleri:**
- API canlıda çalışmalı ve `/health` endpoint'i 200 dönmeli
- Veritabanı bağlantısı çalışmalı (CRUD operasyonları)
- Frontend'den API'ya başarılı istek atılabilmeli
:::

:::exercise[Egzersiz 3: CI/CD Pipeline Kur]
**Görev:** GitHub Actions ile otomatik test ve deployment pipeline'ı kur.

**Adımlar:**
1. `.github/workflows/deploy.yml` dosyası oluştur
2. Frontend: pnpm install → lint → test → build adımlarını ekle
3. Backend: uv sync → ruff check → pytest adımlarını ekle
4. Main branch'e push'ta otomatik deploy tetiklensin
5. PR açıldığında sadece test çalışsın (deploy olmasın)
6. GitHub Secrets'a gerekli token'ları ekle

**Başarı kriterleri:**
- PR açıldığında testler otomatik çalışmalı
- Main'e merge'de deployment tetiklenmeli
- Testler fail ederse deployment olmamalı
:::

:::exercise[Egzersiz 4: Production Readiness Audit]
**Görev:** Mevcut bir projeyi production-ready hale getir.

**Checklist:**
1. `.env.example` dosyası oluştur, `.env`'yi `.gitignore`'a ekle
2. Health check endpoint'i ekle (DB bağlantısını da kontrol etsin)
3. CORS ayarlarını sıkılaştır (wildcard `*` yerine specific origin)
4. Security header'ları ekle (X-Frame-Options, CSP, HSTS)
5. Rate limiting middleware ekle
6. Structured logging ekle (JSON format)
7. Error tracking entegrasyonu (Sentry free tier)
8. README'ye deployment dokümantasyonu ekle

**Başarı kriterleri:**
- Güvenlik header'ları response'larda görünmeli
- Rate limiting çalışmalı (çok fazla istekte 429 dönmeli)
- Sentry'de test error'u görünmeli
- Health check tüm dependency'leri kontrol etmeli
:::

## Özet: Deployment Karar Ağacı

Hangi platformu ne zaman kullanacağını bilmek, deployment bilgisinin yarısıdır:

| Senaryo | Platform | Neden |
|---------|----------|-------|
| React/Next.js frontend | Vercel | Next.js optimizasyonu, preview deployments, edge functions |
| Static site / blog | Netlify | Kolay setup, form handling, CMS entegrasyonu |
| FastAPI/Express backend | Railway | Kolay DB provisioning, GitHub entegrasyonu |
| Startup MVP — hızlı çıkış | Railway + Vercel | Dakikalar içinde full-stack deploy |
| Büyük şirket / enterprise | AWS | Tam kontrol, compliance, ölçeklenebilirlik |
| Serverless API | AWS Lambda / Vercel Functions | Pay-per-request, sıfır yönetim |
| Microservices | AWS ECS / Kubernetes | Container orchestration, service mesh |

:::ai-guidance
Bu dersteki platformların hepsini ezberlemene gerek yok. Önemli olan deployment konseptlerini anlamaktır: CI/CD, environment management, health checks, rollback, monitoring. Platform değişir, konseptler aynı kalır. AI araçlarına "set up a CI/CD pipeline for my FastAPI app with GitHub Actions" diyerek başlangıç template'i alabilirsin, ama o template'in her satırını anlamadan production'a koyma. AI ile ürettiğin her konfigürasyonu satır satır oku ve anla.
:::

:::must-note
**Kesinlikle not al — Senior Deployment Kuralları:**
1. **Localhost'ta çalışan proje = bitmemiş proje.** Deploy etmeden portfolyöne koyma.
2. **Manuel deployment = insan hatası.** CI/CD olmadan production'a kod gönderme.
3. **Secret'lar kodda değil, environment'ta yaşar.** Tek bir sızdırılmış API key = güvenlik felaketi.
4. **Rollback planı olmadan deploy etme.** "Bir şey olursa düzeltiriz" strateji değil, kumar.
5. **Monitoring olmadan production yok.** Hatayı kullanıcıdan önce sen yakalamalısın.
6. **Health check = deployment'ın kalp atışı.** Her servisin bir health check'i olmalı.
:::
