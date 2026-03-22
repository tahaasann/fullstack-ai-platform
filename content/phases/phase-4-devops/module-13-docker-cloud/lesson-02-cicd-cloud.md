---
title: "CI/CD, Kubernetes & Cloud: Production Deployment Pipeline"
id: "mod-13-docker/lesson-02"
estimated_minutes: 70
order: 2
tags: ["ci-cd", "github-actions", "kubernetes", "aws", "gcp", "azure", "terraform", "monitoring", "devops"]
prerequisites: ["mod-13-docker/lesson-01"]
---

# CI/CD, Kubernetes & Cloud: Production Deployment Pipeline

:::realworld
GitHub her gün 1000'den fazla deployment yapıyor. Spotify dakikada bir production'a kod gönderiyor. Netflix haftada binlerce deployment gerçekleştiriyor. Bu şirketlerin ortak noktası: tam otomatik CI/CD pipeline'ları, Kubernetes orchestration'ı ve cloud-native mimari. Manuel deployment yapan şirketler artık yok denecek kadar az. Bu derste modern deployment pipeline'ını sıfırdan kuracak bilgiyi kazanacaksın.
:::

## CI/CD Nedir?

:::concept[CI - Continuous Integration (İng: Continuous Integration)]
CI, geliştiricilerin kodlarını sık sık (günde birden fazla kez) ana branch'e entegre etmesi ve her entegrasyonun otomatik build ve test ile doğrulanması sürecidir.

**Turkce karsiligi:** Sürekli Entegrasyon
**Ne ise yarar:** Kod hatalarını erken yakalar, "works on my machine" problemini ortadan kaldırır
**Gercek hayat benzetmesi:** Fabrikada her parça üretildiğinde kalite kontrolden geçirmek - hatalı parçalar montaj hattına ulaşmaz
:::

:::concept[CD - Continuous Delivery/Deployment (İng: Continuous Delivery)]
CD, CI'dan geçen kodun otomatik olarak staging/production ortamına deploy edilmesi sürecidir. Delivery = manuel onay ile, Deployment = tamamen otomatik.

**Turkce karsiligi:** Sürekli Teslimat / Sürekli Dağıtım
**Ne ise yarar:** Yeni özellikleri ve düzeltmeleri hızlı, güvenli şekilde kullanıcılara ulaştırır
**Gercek hayat benzetmesi:** Otomatik paketleme ve kargo sistemi - ürün kalite kontrolü geçince otomatik olarak müşteriye gönderilir
:::

:::comparison
| Ozellik | Continuous Integration | Continuous Delivery | Continuous Deployment |
|---------|----------------------|--------------------|-----------------------|
| Tetikleyici | Her commit/PR | CI başarılı olunca | CI başarılı olunca |
| Build | Otomatik | Otomatik | Otomatik |
| Test | Otomatik | Otomatik | Otomatik |
| Staging deploy | - | Otomatik | Otomatik |
| Production deploy | - | Manuel onay | Otomatik |
| Risk | Düşük | Düşük | Çok düşük (iyi test gerekli) |

**Temel fark:** Delivery'de production deploy'u için insan onayı gerekir, Deployment'ta her şey otomatik.
:::

:::deha-tip
Senior developer'lar CI/CD'yi sadece "deploy otomasyonu" olarak görmez. Pipeline'ı code quality gate, security scanning, performance testing, compliance check ve rollback stratejisi ile bütünleşik bir güvenlik ağı olarak tasarlar. Her stage bir kalite kapısıdır.
:::

## GitHub Actions: CI/CD Pipeline Oluşturma

:::concept[GitHub Actions (İng: GitHub Actions)]
GitHub Actions, GitHub repository'lerinde CI/CD workflow'ları oluşturmak için kullanılan bir otomasyon platformudur. YAML dosyaları ile tanımlanan workflow'lar event'lere (push, PR, schedule) göre tetiklenir.

**Turkce karsiligi:** GitHub Aksiyonları / İş Akışları
**Ne ise yarar:** Kod push edilince otomatik test, build ve deploy yapar
**Gercek hayat benzetmesi:** Bir fabrikadaki otomatik montaj hattı - hammadde (kod) girince, kalite kontrol, paketleme ve sevkiyat otomatik olur
:::

### Temel Kavramlar

:::english
**Workflow:** A YAML file defining automated processes. Stored in `.github/workflows/`.

**Job:** A set of steps that execute on the same runner. Jobs run in parallel by default.

**Step:** An individual task within a job. Can run commands or use actions.

**Action:** A reusable unit of code (like an npm package for CI/CD). Found on GitHub Marketplace.

**Runner:** The server that runs your workflows. GitHub provides hosted runners (Ubuntu, Windows, macOS) or you can use self-hosted runners.

**Trigger/Event:** What starts a workflow - push, pull_request, schedule, workflow_dispatch (manual).
:::

### İlk GitHub Actions Workflow

:::code[yaml]{title=".github/workflows/ci.yml - Basic CI Pipeline"}
name: CI Pipeline

# Workflow ne zaman tetiklenir?
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# Environment variables (tüm job'larda geçerli)
env:
  NODE_VERSION: '20'

jobs:
  # ============ Job 1: Lint & Type Check ============
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest

    steps:
      # 1. Kodu çek
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. Node.js kur
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'            # 📌 2026: pnpm cache kullan

      - name: Setup pnpm
        uses: pnpm/action-setup@v4

      # 3. Dependency'leri yükle
      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      # 4. ESLint çalıştır
      - name: Run ESLint
        run: pnpm lint

      # 5. TypeScript type check
      - name: TypeScript check
        run: pnpm exec tsc --noEmit

  # ============ Job 2: Test ============
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint               # lint job'u başarılı olmalı

    # PostgreSQL service container
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - uses: pnpm/action-setup@v4
      - run: pnpm install --frozen-lockfile

      - name: Run tests
        run: pnpm test -- --coverage
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
          JWT_SECRET: test-secret-key

      # Test coverage raporunu artifact olarak kaydet
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  # ============ Job 3: Build & Push Docker Image ============
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test                # Test'ler geçmeli
    if: github.ref == 'refs/heads/main'  # Sadece main branch'te

    steps:
      - uses: actions/checkout@v4

      # Docker Buildx kurulumu (multi-platform build için)
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # GitHub Container Registry'ye giriş
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      # Image build ve push
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ============ Job 4: Deploy to Production ============
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production    # Manual approval gerektirir

    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            cd /opt/myapp
            docker compose pull
            docker compose up -d --remove-orphans
            docker system prune -f
:::

:::warning
GitHub Actions secret'larını (API key, password, SSH key) **ASLA** workflow dosyasına hardcode etme! `Settings > Secrets and variables > Actions`'da tanımla ve `${{ secrets.MY_SECRET }}` ile referans ver. `.env` dosyasını repository'ye push etme!
:::

### Advanced GitHub Actions Patterns

:::code[yaml]{title="Matrix Strategy: Birden Fazla Ortamda Test"}
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]    # 3 Node.js versiyonunda test et
        database: [postgres, mysql]    # 2 veritabanında test et
      fail-fast: false                 # Biri fail olursa diğerleri devam etsin

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - uses: pnpm/action-setup@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm test
        env:
          DB_TYPE: ${{ matrix.database }}
:::

:::code[yaml]{title="Reusable Workflow ve Caching"}
# .github/workflows/deploy.yml
name: Deploy

on:
  workflow_call:              # Başka workflow'lardan çağrılabilir
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy
        run: echo "Deploying to ${{ inputs.environment }}"
:::

:::tip
GitHub Actions'da `pnpm install --frozen-lockfile` kullanmak `pnpm install`'dan daha guvenlidir. `--frozen-lockfile` her zaman `pnpm-lock.yaml`'dan exact versiyonlari yukler. CI ortamlarinda reproducible build'ler icin zorunludur. npm kullaniyorsan ayni mantikla `npm ci` tercih et.
:::

## Kubernetes (K8s) Temelleri

:::concept[Kubernetes (İng: Kubernetes / K8s)]
Kubernetes, containerized uygulamaların deployment, scaling ve management'ını otomatize eden bir container orchestration platformudur. Google tarafından geliştirilmiş, şimdi CNCF tarafından yönetilmektedir.

**Turkce karsiligi:** Konteyner Orkestrasyon Platformu
**Ne ise yarar:** Container'ları otomatik olarak yönetir: scaling, load balancing, self-healing, rolling updates
**Gercek hayat benzetmesi:** Havaalanı kontrol kulesi gibi - yüzlerce uçağın (container'ın) kalkışını, inişini, park yerini ve yakıt ikmalini koordine eder
:::

### Kubernetes Architecture

:::english
**Cluster:** A set of machines (nodes) running Kubernetes. Contains a control plane and worker nodes.

**Control Plane (Master):** Manages the cluster. Components: API Server, etcd, Scheduler, Controller Manager.

**Worker Node:** Runs application containers. Components: kubelet, kube-proxy, container runtime.

**Pod:** Smallest deployable unit. Contains one or more containers that share network and storage.

**Service:** Exposes pods to network traffic. Types: ClusterIP (internal), NodePort (external via node port), LoadBalancer (cloud LB).

**Deployment:** Manages pod replicas and rolling updates. Ensures desired state matches actual state.

**Namespace:** Virtual cluster within a physical cluster. For isolating environments (dev, staging, prod).
:::

:::comparison
| Kavram | Docker Compose | Kubernetes |
|--------|---------------|------------|
| Kapsam | Tek sunucu | Çoklu sunucu (cluster) |
| Scaling | `--scale` (limited) | HPA ile otomatik |
| Self-healing | `restart: always` | Pod restart + rescheduling |
| Load balancing | Nginx gerekli | Built-in Service |
| Rolling updates | Manuel | Built-in Deployment |
| Secret management | `.env` dosyası | K8s Secrets (encrypted) |
| Kullanım alanı | Development, küçük projeler | Production, büyük sistemler |
| Öğrenme eğrisi | Düşük | Yüksek |
:::

### Kubernetes Manifest Dosyaları

:::code[yaml]{title="deployment.yaml - Node.js API Deployment"}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
  labels:
    app: myapp-api
spec:
  replicas: 3                      # 3 pod çalıştır
  selector:
    matchLabels:
      app: myapp-api
  strategy:
    type: RollingUpdate             # Zero-downtime deployment
    rollingUpdate:
      maxSurge: 1                  # Aynı anda max 1 fazla pod
      maxUnavailable: 0            # Hiçbir an pod eksik olmasın
  template:
    metadata:
      labels:
        app: myapp-api
    spec:
      containers:
        - name: api
          image: ghcr.io/myorg/myapp:1.2.0
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
          resources:
            requests:
              cpu: "100m"          # Min 0.1 CPU core
              memory: "128Mi"      # Min 128MB RAM
            limits:
              cpu: "500m"          # Max 0.5 CPU core
              memory: "512Mi"      # Max 512MB RAM
          livenessProbe:           # Container sağlık kontrolü
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 30
          readinessProbe:          # Traffic almaya hazır mı?
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
      # Non-root user zorunlu
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
:::

:::code[yaml]{title="service.yaml - API Service (Load Balancer)"}
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: LoadBalancer              # Cloud provider'ın LB'sini kullanır
  selector:
    app: myapp-api                # deployment.yaml'daki label ile eşleşmeli
  ports:
    - protocol: TCP
      port: 80                    # Service portu (dışarıdan erişim)
      targetPort: 3000            # Pod'daki container portu
:::

:::code[yaml]{title="secret.yaml - Kubernetes Secrets"}
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  # Base64 encoded değerler (echo -n 'value' | base64)
  database-url: cG9zdGdyZXNxbDovL2FkbWluOnNlY3JldEBkYjoxNTQzMi9teWFwcA==
  jwt-secret: c3VwZXItc2VjcmV0LWtleQ==
:::

:::warning
Kubernetes Secret'ları sadece Base64 encode edilir, **şifrelenmez**! Gerçek güvenlik için: (1) RBAC ile Secret'lara erişimi kısıtla, (2) etcd encryption at rest'i etkinleştir, (3) External secret management (HashiCorp Vault, AWS Secrets Manager) kullan, (4) Secret manifest'lerini Git'e commit etme, Sealed Secrets veya SOPS kullan.
:::

### kubectl Temel Komutları

:::code[bash]{title="kubectl CLI Komutları"}
# Cluster durumu
kubectl cluster-info
kubectl get nodes

# Pod yönetimi
kubectl get pods                          # Pod'ları listele
kubectl get pods -o wide                  # Detaylı bilgi (IP, node)
kubectl describe pod <pod-name>           # Pod detayları
kubectl logs <pod-name>                   # Pod logları
kubectl logs -f <pod-name>               # Follow mode
kubectl exec -it <pod-name> -- sh        # Pod'a shell aç

# Deployment yönetimi
kubectl apply -f deployment.yaml         # Manifest uygula
kubectl get deployments                   # Deployment'ları listele
kubectl rollout status deployment/api    # Rollout durumu
kubectl rollout undo deployment/api      # Önceki versiyona geri dön

# Scaling
kubectl scale deployment/api --replicas=5   # Manuel scale
kubectl autoscale deployment/api \
  --min=2 --max=10 --cpu-percent=70         # HPA (auto-scale)

# Service yönetimi
kubectl get services
kubectl get svc

# Namespace
kubectl get namespaces
kubectl get pods -n production

# Tüm kaynakları göster
kubectl get all

# YAML'dan tüm kaynakları oluştur
kubectl apply -f k8s/                     # Dizindeki tüm YAML dosyaları
:::

### Horizontal Pod Autoscaler (HPA)

:::code[yaml]{title="hpa.yaml - Otomatik Scaling"}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70      # CPU %70'i aşınca scale up
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80      # Memory %80'i aşınca scale up
:::

## Cloud Providers: AWS, GCP, Azure

:::concept[Cloud Computing (İng: Cloud Computing)]
Cloud Computing, bilgi işlem kaynaklarının (sunucu, depolama, veritabanı, network) internet üzerinden isteğe bağlı olarak kiralanması modelidir.

**Turkce karsiligi:** Bulut Bilişim
**Ne ise yarar:** Fiziksel sunucu satın almadan, dakikalar içinde global altyapı kullanmayı sağlar
**Gercek hayat benzetmesi:** Elektrik şirketi gibi - kendi jeneratörünü kurmak yerine, kullandığın kadar öde modeli
:::

### Cloud Service Modelleri

:::comparison
| Model | Senin Yonetigin | Provider Yonetir | Ornek |
|-------|----------------|-------------------|-------|
| **IaaS** (Infrastructure) | OS, Runtime, App | Network, Storage, Compute | AWS EC2, GCP Compute Engine |
| **PaaS** (Platform) | App, Data | OS, Runtime, Infra | Heroku, AWS Elastic Beanstalk |
| **SaaS** (Software) | Sadece kullanım | Her şey | Gmail, Slack, Notion |
| **FaaS** (Function) | Sadece kod | Her şey + scaling | AWS Lambda, GCP Cloud Functions |

**Tavsiye:** Startup'lar PaaS/FaaS ile başlasın (hızlı development), büyüdükçe IaaS'a (tam kontrol) geçsinler.
:::

### Temel Cloud Servisleri Karşılaştırması

:::comparison
| Kategori | AWS | GCP | Azure |
|----------|-----|-----|-------|
| **Compute** | EC2 | Compute Engine | Virtual Machines |
| **Kubernetes** | EKS | GKE | AKS |
| **Serverless** | Lambda | Cloud Functions | Azure Functions |
| **Container** | ECS/Fargate | Cloud Run | Container Apps |
| **Database (SQL)** | RDS | Cloud SQL | SQL Database |
| **Database (NoSQL)** | DynamoDB | Firestore | Cosmos DB |
| **Object Storage** | S3 | Cloud Storage | Blob Storage |
| **CDN** | CloudFront | Cloud CDN | Azure CDN |
| **DNS** | Route 53 | Cloud DNS | Azure DNS |
| **Message Queue** | SQS | Pub/Sub | Service Bus |
| **Cache** | ElastiCache | Memorystore | Azure Cache |
| **Monitoring** | CloudWatch | Cloud Monitoring | Azure Monitor |

**Pazar payı (2025):** AWS ~31%, Azure ~25%, GCP ~11%. AWS en yaygın, GCP Kubernetes'te güçlü, Azure enterprise'da baskın.
:::

### AWS Temel Servisler

:::code[bash]{title="AWS CLI Temel Komutları"}
# AWS CLI kurulumu ve yapılandırma
aws configure
# Access Key ID, Secret Access Key, Region, Output format

# S3 (Object Storage)
aws s3 ls                                    # Bucket'ları listele
aws s3 cp file.txt s3://my-bucket/          # Dosya yükle
aws s3 sync ./build s3://my-bucket/ --delete # Dizin senkronize et (deploy)

# EC2 (Virtual Machines)
aws ec2 describe-instances                   # Instance'ları listele
aws ec2 start-instances --instance-ids i-xxx # Instance başlat

# ECS (Container Service)
aws ecs list-clusters                        # Cluster'ları listele
aws ecs update-service \
  --cluster my-cluster \
  --service my-service \
  --force-new-deployment                     # Yeni deployment tetikle

# Lambda (Serverless Functions)
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  output.json                                # Lambda fonksiyonu çağır
:::

## Infrastructure as Code (IaC): Terraform

:::concept[Infrastructure as Code (İng: Infrastructure as Code / IaC)]
IaC, altyapı kaynaklarını (sunucu, veritabanı, network) kod olarak tanımlama ve versiyonlama pratiğidir. Manuel konsol tıklamaları yerine deklaratif yapılandırma dosyaları kullanılır.

**Turkce karsiligi:** Kod Olarak Altyapı
**Ne ise yarar:** Altyapıyı tekrarlanabilir, versiyonlanabilir ve otomatize edilebilir hale getirir
**Gercek hayat benzetmesi:** Bina planı gibi - aynı plandan aynı binayı defalarca inşa edebilirsin, her seferinde aynı sonucu alırsın
:::

:::code[hcl]{title="main.tf - Terraform ile AWS Altyapısı"}
# Provider tanımla
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # State dosyasını S3'te sakla (team çalışması için)
  backend "s3" {
    bucket = "myapp-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  default = "eu-west-1"
}

variable "environment" {
  default = "production"
}

# VPC (Virtual Private Cloud)
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name        = "myapp-vpc"
    Environment = var.environment
  }
}

# Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "myapp-public-subnet"
  }
}

# RDS (PostgreSQL Database)
resource "aws_db_instance" "postgres" {
  identifier           = "myapp-db"
  engine              = "postgres"
  engine_version      = "16.1"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  storage_encrypted   = true

  db_name  = "myapp"
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  skip_final_snapshot    = false

  tags = {
    Environment = var.environment
  }
}

# Security Group
resource "aws_security_group" "db" {
  name   = "myapp-db-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.api.id]  # Sadece API'den erişim
  }
}

# Output
output "db_endpoint" {
  value = aws_db_instance.postgres.endpoint
}
:::

:::code[bash]{title="Terraform CLI Komutları"}
# Terraform başlat (provider'ları indir)
terraform init

# Plan oluştur (ne değişecek?)
terraform plan

# Değişiklikleri uygula
terraform apply

# Altyapıyı yok et (DİKKAT!)
terraform destroy

# State dosyasını görüntüle
terraform state list
terraform state show aws_db_instance.postgres

# Formatla
terraform fmt

# Doğrula
terraform validate
:::

:::beginner-mistake
**Hata:** Terraform state dosyasını Git'e commit etmek.

**Problem:** `terraform.tfstate` dosyası hassas bilgiler içerir (database password, API key). Git'e push edersen herkes görebilir.

**Çözüm:** Remote backend kullan (S3 + DynamoDB lock, Terraform Cloud). `.gitignore`'a `*.tfstate` ve `*.tfstate.backup` ekle. State dosyasını asla local'de bırakma.
:::

## Monitoring ve Logging

:::concept[Observability (İng: Observability)]
Observability, bir sistemin iç durumunu dışarıdan gözlemleyebilme yeteneğidir. Üç temel bileşeni vardır: Metrics, Logs, Traces.

**Turkce karsiligi:** Gözlemlenebilirlik
**Ne ise yarar:** Sistemdeki sorunları hızlıca tespit etmeni ve çözmeni sağlar
**Gercek hayat benzetmesi:** Arabanın gösterge paneli gibi - hız, yakıt, motor sıcaklığı, arıza lambası... Her an sistemin durumunu görürsün
:::

### Observability'nin Üç Sütunu

:::comparison
| Sutun | Ne? | Araç Örnekleri | Kullanım |
|-------|-----|---------------|----------|
| **Metrics** | Sayısal değerler (CPU, memory, request count) | Prometheus + Grafana | Dashboardlar, alerting |
| **Logs** | Olay kayıtları (JSON structured logs) | ELK Stack, Loki + Grafana | Debug, audit trail |
| **Traces** | İstek akışı (service A → B → C) | Jaeger, Zipkin, OpenTelemetry | Performans analizi, bottleneck tespiti |
:::

### Prometheus + Grafana

:::code[yaml]{title="docker-compose.yml - Monitoring Stack"}
services:
  # Prometheus: Metric toplama
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=15d'

  # Grafana: Dashboard ve vizualizasyon
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

volumes:
  prometheus_data:
  grafana_data:
:::

:::code[yaml]{title="prometheus.yml - Prometheus Config"}
global:
  scrape_interval: 15s            # Her 15 saniyede metric topla

scrape_configs:
  - job_name: 'node-api'
    static_configs:
      - targets: ['api:3000']      # API'nin /metrics endpoint'i

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']  # Sistem metrikleri
:::

:::code[javascript]{title="Express.js Prometheus Metrics"}
const express = require('express');
const promClient = require('prom-client');

const app = express();

// Default metric'leri topla (CPU, memory, event loop)
promClient.collectDefaultMetrics({ timeout: 5000 });

// Custom metric'ler
const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'path', 'status']
});

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'path'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
});

// Middleware: Her isteği ölç
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestsTotal.inc({
      method: req.method,
      path: req.route?.path || req.path,
      status: res.statusCode
    });
    httpRequestDuration.observe(
      { method: req.method, path: req.route?.path || req.path },
      duration
    );
  });
  next();
});

// Prometheus metric'lerini expose et
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.send(await promClient.register.metrics());
});
:::

### Structured Logging

:::code[javascript]{title="Winston ile Structured Logging"}
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()           // Structured JSON log
  ),
  defaultMeta: {
    service: 'api-service',
    version: process.env.APP_VERSION || '1.0.0'
  },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: 'logs/combined.log'
    })
  ]
});

// Kullanım
logger.info('User logged in', {
  userId: user.id,
  email: user.email,
  ip: req.ip,
  userAgent: req.get('User-Agent')
});

logger.error('Database connection failed', {
  error: err.message,
  stack: err.stack,
  host: dbConfig.host
});

// Çıktı (JSON - log aggregation sistemleri bunu parse edebilir):
// {"level":"info","message":"User logged in","timestamp":"2024-01-15T10:30:00Z",
//  "service":"api-service","userId":1,"email":"ahmet@test.com","ip":"192.168.1.1"}
:::

:::tip
**Structured logging altın kuralı:** `console.log("User logged in: " + userId)` yerine `logger.info("User logged in", { userId })` kullan. JSON format log aggregation sistemlerinin (ELK, Loki) logları indexlemesini ve sorgulamasını kolaylaştırır. Production'da console.log KULLANMA!
:::

## Full CI/CD Pipeline: End-to-End

:::code[yaml]{title="Production-Ready CI/CD Pipeline"}
name: Production Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Stage 1: Code Quality
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - uses: pnpm/action-setup@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - name: Security audit
        run: pnpm audit --audit-level=high

  # Stage 2: Test
  test:
    needs: quality
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports: ['5432:5432']
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - uses: pnpm/action-setup@v4
      - run: pnpm install --frozen-lockfile
      - run: pnpm test -- --coverage --ci
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test

  # Stage 3: Build & Push (only main)
  build:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha
            type=semver,pattern={{version}}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Stage 4: Deploy
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Kubernetes
        run: |
          echo "Deploying ${{ needs.build.outputs.image-tag }}"
          # kubectl set image deployment/api api=${{ needs.build.outputs.image-tag }}
:::

:::exercise
## Pratik Alistirmalar

### Alistirma 1: GitHub Actions CI Pipeline
Bir Node.js projesi icin CI pipeline olusturun:

```yaml
# .github/workflows/ci.yml
# TODO: PR acildiginda ve main'e push'ta tetiklensin
# TODO: Node.js 18 ve 20 versiyonlarinda matrix test
# TODO: npm ci ile dependency install (npm install degil!)
# TODO: Lint, test ve build adimlari
# TODO: npm cache kullanarak hizlandirma
# TODO: Test coverage raporu yukle
```

**Beklenen sonuc:** PR'larda otomatik lint + test + build calismali, basarisiz olursa merge engellemeli (branch protection), cache ile CI suresi %50+ azalmali.

### Alistirma 2: Multi-Stage Docker Build + Deploy
Bir React + Express uygulamasi icin production-ready pipeline olusturun:

```dockerfile
# TODO: Multi-stage Dockerfile (build + production)
# TODO: Build stage'de npm run build
# TODO: Production stage'de sadece build ciktisi + nginx
# TODO: Health check endpoint
```

```yaml
# TODO: GitHub Actions ile:
# 1. Docker image build et
# 2. Docker Hub'a push et
# 3. Staging ortamina deploy et
# 4. Smoke test calistir
# 5. Production'a deploy et (manual approval ile)
```

**Beklenen sonuc:** Tek commit ile build -> test -> staging -> production pipeline'i calismali, rollback mekanizmasi olmali.

### Alistirma 3: Environment Secrets ve Config Yonetimi
Farkli ortamlar icin konfigurasyoon yonetimi kurun:

```
# TODO: GitHub Secrets ile API key'leri guvene alin
# TODO: Development, staging ve production icin farkli .env dosyalari
# TODO: GitHub Environments ile ortam bazli deployment korumalari
# TODO: Slack notification entegrasyonu (deploy basarili/basarisiz)
```

**Beklenen sonuc:** Hicbir secret kod icerisinde olmamali, her ortam kendi konfigurasyonuyla calismali, deploy durumlari Slack'te bildirilmeli.

---

### Alistirma 4: Branch Protection ve PR Workflow (Kolay)

GitHub branch protection kurallari ve otomatik PR kontrolleri yapilandir.

```yaml
# .github/workflows/pr-check.yml
name: PR Checks
on:
  pull_request:
    branches: [main, develop]

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm type-check
      - run: pnpm test -- --ci --coverage
      - name: Coverage Check
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          echo "Coverage: $COVERAGE%"
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "::error::Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

# TODO: PR boyut kontrolu ekle (max 500 satir degisiklik uyarisi)
# TODO: Commit message format kontrolu (conventional commits)
# TODO: Auto-assign reviewer kurali ekle
```

**Beklenen Sonuc:** PR acildiginda lint, type-check ve test otomatik calismali. Coverage %80'in altindaysa PR merge edilememeli.
**Ipucu:** GitHub Settings > Branches > Branch protection rules ile main branch'i koruyabilirsin.

---

### Alistirma 5: Docker Image Build ve Registry Push (Kolay)

CI pipeline'da Docker image olustur ve container registry'ye gonder.

```yaml
# .github/workflows/docker-publish.yml
name: Docker Build & Push
on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

# TODO: Semantic versioning ile tag'leme ekle (v1.0.0)
# TODO: Multi-platform build ekle (linux/amd64, linux/arm64)
# TODO: Image vulnerability scan adimi ekle (trivy)
```

**Beklenen Sonuc:** Her main push'ta image build edilip GHCR'a push edilmeli. Build cache ile sonraki build'ler hizlanmali. Git SHA ile her image izlenebilir olmali.
**Ipucu:** GitHub Container Registry (ghcr.io) ucretsiz ve GITHUB_TOKEN ile otomatik authenticate olur.

---

### Alistirma 6: Kubernetes Manifest Yazma (Orta)

Basit bir uygulamayi Kubernetes'e deploy etmek icin manifest dosyalari yaz.

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: app
          image: ghcr.io/username/my-app:latest
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: "production"
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secrets
                  key: password
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
---
# TODO: Service manifest yaz (ClusterIP ve LoadBalancer)
# TODO: Ingress manifest yaz (domain routing)
# TODO: HorizontalPodAutoscaler ekle (CPU %70'te scale)
# TODO: ConfigMap ve Secret manifest'leri olustur
```

**Beklenen Sonuc:** `kubectl apply -f k8s/` ile tum kaynaklar olusturulmali. Pod'lar healthy olmali. Secret'lar environment variable olarak inject edilmeli.
**Ipucu:** `kubectl get pods -w` ile pod durumlarini canli izle. `kubectl describe pod <name>` ile hata detaylarini gor.

---

### Alistirma 7: Rollback ve Blue-Green Deployment (Orta)

Basarisiz bir deployment'i geri alma ve zero-downtime deployment stratejisi uygula.

```bash
# 1. Deployment history'yi gor
kubectl rollout history deployment/my-app

# 2. Yeni versiyon deploy et
kubectl set image deployment/my-app app=ghcr.io/username/my-app:v2.0

# 3. Rollout durumunu izle
kubectl rollout status deployment/my-app

# 4. Sorun varsa geri al
kubectl rollout undo deployment/my-app
kubectl rollout undo deployment/my-app --to-revision=2

# TODO: Rolling update stratejisini yapilandir (maxSurge: 1, maxUnavailable: 0)
# TODO: Canary deployment simule et (%10 trafik yeni versiyona)
# TODO: Health check basarisiz olursa otomatik rollback'i test et
```

```yaml
# deployment.yaml - Rolling update strategy
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

**Beklenen Sonuc:** Zero-downtime deployment calismali. Basarisiz deployment otomatik geri alinmali. Rollout history ile gecmis versiyonlara donulebilmeli.
**Ipucu:** `maxUnavailable: 0` ile her zaman en az mevcut replica sayisi kadar pod ayakta kalir.

---

### Alistirma 8: Terraform ile Infrastructure as Code (Orta)

Basit bir cloud altyapisini Terraform ile tanimla ve yonet.

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "frontend" {
  bucket = "${var.project_name}-frontend"
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  index_document { suffix = "index.html" }
  error_document { key = "404.html" }
}

# TODO: CloudFront distribution ekle (CDN)
# TODO: Route53 DNS kaydı olustur
# TODO: RDS PostgreSQL instance olustur
# TODO: variables.tf ve outputs.tf dosyalarini tamamla
```

**Beklenen Sonuc:** `terraform plan` ile degisiklikler onizlenebilmeli. `terraform apply` ile altyapi olusturulmali. State dosyasi remote backend'de saklanmali.
**Ipucu:** `terraform destroy` ile tum kaynaklari temizleyebilirsin. Production'da state'i S3 + DynamoDB lock ile sakla.

---

### Alistirma 9: Monitoring ve Alerting Pipeline (Zor)

CI/CD pipeline'ina deployment sonrasi monitoring ve alert entegrasyonu ekle.

```yaml
# .github/workflows/deploy-and-monitor.yml
name: Deploy & Monitor
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        run: |
          # Deploy komutu
          kubectl set image deployment/app app=ghcr.io/${{ github.repository }}:${{ github.sha }}
          kubectl rollout status deployment/app --timeout=300s

      - name: Smoke Test
        run: |
          sleep 30
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
          if [ "$STATUS" != "200" ]; then
            echo "::error::Health check failed with status $STATUS"
            kubectl rollout undo deployment/app
            exit 1
          fi

      - name: Notify Success
        if: success()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"Deploy basarili: ${{ github.sha }}"}'

# TODO: Sentry release tracking ekle
# TODO: Deploy sonrasi error rate kontrolu (5 dakika bekle, %1 ustundeyse rollback)
# TODO: Performance regression testi ekle (Lighthouse CI)
```

**Beklenen Sonuc:** Deploy sonrasi smoke test basarisiz olursa otomatik rollback yapilmali. Basarili deploy Slack'te bildirilmeli.
**Ipucu:** Smoke test ile critical endpoint'leri kontrol et. Canary analysis ile metrikleri karsilastir.

---

### Alistirma 10: GitOps Workflow ile Argo CD (Zor)

GitOps prensibiyle Kubernetes deployment'larini yonet.

```yaml
# argocd/application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/username/my-app-k8s
    targetRevision: main
    path: k8s/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

```
# Dizin yapisi (Kustomize)
k8s/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
├── overlays/
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── replicas-patch.yaml  # replicas: 1
│   └── production/
│       ├── kustomization.yaml
│       └── replicas-patch.yaml  # replicas: 3
```

```bash
# TODO: Kustomize base ve overlay dosyalarini olustur
# TODO: Staging ve production icin farkli konfigurasyonlar tanimla
# TODO: Git commit ile deployment tetikle (push to k8s repo)
# TODO: Argo CD UI'da sync durumunu izle
```

**Beklenen Sonuc:** Git repo'ya push yapildiginda Argo CD otomatik olarak Kubernetes'e deploy etmeli. Staging ve production farkli konfigurasyonlarla calismali.
**Ipucu:** GitOps'ta "truth" her zaman Git'tedir. Manuel kubectl degisiklikleri Argo CD tarafindan geri alinir (selfHeal: true).
:::

## Interview'da CI/CD ve Cloud Soruları

:::interview
**Soru 1:** "CI/CD pipeline'ında hangi aşamalar olmalı?"
**Cevap:** Tipik bir pipeline: (1) Lint + Type Check - kod kalitesi, (2) Unit + Integration Tests - doğruluk, (3) Security Scan - vulnerability tarama, (4) Build - Docker image oluşturma, (5) Push - Registry'ye gönderme, (6) Deploy to Staging - test ortamına, (7) E2E Tests - uçtan uca test, (8) Deploy to Production - canlıya alma. Her aşama bir kalite kapısıdır.

**Soru 2:** "Kubernetes'te Pod ile Deployment arasındaki fark nedir?"
**Cevap:** Pod tek bir container (veya ilişkili container grubu) çalıştıran en küçük birimdir. Deployment ise Pod'ların desired state'ini yönetir: kaç replica çalışacak, rolling update stratejisi ne olacak, sağlık kontrolü nasıl yapılacak. Pod silinirse geri gelmez, ama Deployment otomatik olarak yeni Pod oluşturur.

**Soru 3:** "Blue-Green deployment ile Rolling deployment farkı?"
**Cevap:** Rolling: Pod'lar birer birer güncellenir, eski ve yeni versiyon geçici olarak birlikte çalışır. Blue-Green: İki tam ortam vardır (blue=current, green=new). Green hazır olunca traffic bir anda geçirilir. Rolling daha az kaynak kullanır, Blue-Green anında rollback sağlar.

**Soru 4:** "IaC (Terraform) kullanmanın avantajları nelerdir?"
**Cevap:** (1) Reproducibility - aynı altyapıyı tekrar oluşturabilirsin, (2) Version control - altyapı değişiklikleri Git'te izlenir, (3) Code review - altyapı değişiklikleri PR'da incelenebilir, (4) Automation - terraform plan/apply ile otomatik, (5) Documentation - kod kendi dokümantasyonu, (6) Disaster recovery - altyapıyı sıfırdan yeniden kurabilirsin.
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "CI/CD pipeline'in her asamasini (commit, build, test, deploy) acikla. Continuous Integration, Continuous Delivery ve Continuous Deployment arasindaki farki goster. GitHub Actions workflow syntax'ini (on, jobs, steps, uses, env, secrets) orneklerle anlat. Matrix strategy ve caching ne ise yarar?"

**2. Pratik Uygulama:**
> "GitHub Actions ile tam bir CI/CD pipeline olustur: PR'da lint + test + build calistir, main branch'e merge'de Docker image build et, container registry'ye push et ve Vercel/Railway'e otomatik deploy et. Environment secrets, caching (node_modules) ve status badge ekle."
> Takip: "Simdi bu pipeline'a Kubernetes deployment ekle. Basit bir k8s manifest (Deployment, Service, Ingress) yaz ve kubectl ile deploy et."

**3. Mukemmellik Icin:**
> "Production'da zero-downtime deployment nasil yapilir? Blue-green deployment, canary release ve rolling update stratejilerini karsilastir. Kubernetes'te readiness/liveness probe, HPA (auto-scaling) ve resource limits nasil konfigure edilir? Terraform ile infrastructure as code yaklasimini acikla."

### Pair Programming Ipucu
CI/CD pipeline sorunlarinda AI'a GitHub Actions log ciktisini yapistir ve sor: "Bu workflow neden basarisiz oldu? Hangi step'te hata var? Cache miss mi oluyor? Secret'lar dogru tanimlanmis mi? Fix'i goster."
:::

:::must-note
## Defterine Yaz!

1. **CI/CD Pipeline Sırası:** Lint → Test → Security Scan → Build → Push → Deploy to Staging → E2E Test → Deploy to Production. Her aşama bir kalite kapısı, biri fail olursa pipeline durur.

2. **Kubernetes Temel Üçlü:** Pod (container çalıştıran en küçük birim) → Deployment (Pod'ların replica ve update yönetimi) → Service (Pod'lara network erişimi sağlar). Bu üçünü anlamadan K8s kullanılamaz.

3. **GitHub Actions Secret Yönetimi:** API key, password, SSH key ASLA workflow dosyasına yazılmaz! `Settings > Secrets` ile tanımla, `${{ secrets.MY_SECRET }}` ile referans ver.

4. **Terraform State:** `terraform.tfstate` dosyası hassas bilgiler içerir. Git'e COMMIT ETME! Remote backend (S3 + DynamoDB) kullan. State lock mekanizması ile concurrent erişimi engelle.

5. **Observability Üç Sütunu:** Metrics (Prometheus - ne kadar?), Logs (ELK/Loki - ne oldu?), Traces (Jaeger - nasıl oldu?). Production'da bu üçü ZORUNLU.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir

Senior developer CI/CD ve Cloud öğrenirken:

1. **Pipeline güvenliğini öncelikler:** Supply chain attack'lere karşı: dependency scanning (Dependabot/Snyk), container image scanning (Trivy), SAST/DAST araçları, signed commits, image signing (cosign).

2. **Cost optimization düşünür:** Cloud maliyetlerini izler, right-sizing yapar, reserved instances vs spot instances kararı verir, auto-scaling policy'lerini optimize eder. FinOps prensiplerini uygular.

3. **Disaster recovery planlar:** RTO (Recovery Time Objective) ve RPO (Recovery Point Objective) belirler. Multi-region deployment, database replication, backup stratejisi oluşturur.

4. **GitOps prensiplerini uygular:** ArgoCD veya Flux ile Kubernetes deployment'larını Git repository üzerinden yönetir. Git = single source of truth. Her değişiklik Git'ten geçer.

5. **Platform engineering düşünür:** Internal Developer Platform (IDP) oluşturur. Developer'ların self-service infra provisioning yapabilmesini sağlar. Backstage gibi developer portal'lar kullanır.

**CTO bakış açısı:** "Hangi cloud provider?", "Multi-cloud vs single cloud?", "Build vs buy kararı", "Vendor lock-in riski", "Compliance gereksinimleri (KVKK, GDPR, SOC2)", "Team skill matrix ve eğitim planı". Teknolojiyi organizasyonel bağlamda değerlendirir.
:::

:::knowledge-check
1. CI (Continuous Integration) ile CD (Continuous Deployment) arasındaki temel fark nedir?
2. GitHub Actions'da `needs` keyword'ü ne işe yarar?
3. Kubernetes'te liveness probe ile readiness probe farkını açıkla.
4. Terraform'da `terraform plan` komutu ne yapar?
5. Structured logging neden `console.log`'dan daha iyidir?
:::

:::external-resource
- [GitHub Actions Dokümantasyon](https://docs.github.com/en/actions) - Resmi rehber
- [Kubernetes Resmi Dokümantasyon](https://kubernetes.io/docs/) - K8s referansı
- [Terraform Learn](https://learn.hashicorp.com/terraform) - HashiCorp'un öğretici içerikleri
- [The Twelve-Factor App](https://12factor.net/) - Cloud-native uygulama prensipleri
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) - AWS mimari best practice
- [Prometheus Dokümantasyon](https://prometheus.io/docs/) - Monitoring referansı
- [CNCF Landscape](https://landscape.cncf.io/) - Cloud-native araçlar haritası
:::
