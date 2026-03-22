#!/usr/bin/env python3
"""
Rewrite ALL substeps in project-05.json to follow the REAL senior developer workflow.
"""

import json
import sys

def main():
    with open("content/projects/project-05.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # ============================================================
    # MILESTONE 1: Proje Altyapısı ve Veri Mimarisi
    # ============================================================

    # M1.S1: Monorepo Proje Yapısı (step 1)
    data["milestones"][0]["steps"][0]["substeps"] = [
        {
            "order": "1.1",
            "action": "Proje kök dizinini oluştur ve içine gir",
            "type": "terminal",
            "command": "mkdir analytics-dashboard && cd analytics-dashboard",
            "expected_output": "Klasör oluşturuldu",
            "why": "Her şey bu klasörün içinde yaşayacak. Temiz bir başlangıç noktası — senior'lar her zaman izole bir proje diziniyle başlar."
        },
        {
            "order": "1.2",
            "action": "pnpm ile root package.json oluştur",
            "type": "terminal",
            "command": "pnpm init",
            "expected_output": "Wrote to /path/to/analytics-dashboard/package.json",
            "why": "Monorepo'nun kalbi package.json. pnpm init bize temel bir manifest dosyası verir, üzerine inşa edeceğiz."
        },
        {
            "order": "1.3",
            "action": "package.json dosyasını AÇ → private ve scripts alanını yaz",
            "type": "code_write",
            "file": "package.json",
            "code": "{\n  \"name\": \"analytics-dashboard\",\n  \"private\": true,\n  \"scripts\": {\n    \"dev\": \"concurrently \\\"pnpm run dev:api\\\" \\\"pnpm run dev:dashboard\\\"\"\n  }\n}",
            "why": "private: true bu paketin npm'e yayınlanmasını engeller — monorepo root'u hiçbir zaman publish edilmez. concurrently ile iki servisi tek komutla başlatacağız ama henüz kurmadık, sıra gelecek."
        },
        {
            "order": "1.4",
            "action": "package.json'a GERİ DÖN → dev:api ve dev:dashboard scriptlerini ekle",
            "type": "code_write",
            "file": "package.json",
            "code": "\"dev:api\": \"cd packages/api && pnpm run dev\",\n\"dev:dashboard\": \"cd packages/dashboard && pnpm run dev\"",
            "why": "Her alt paketi kendi dizininden başlatıyoruz. İleride packages/api ve packages/dashboard dizinlerini oluşturacağız — şimdi sadece script'leri hazırlıyoruz."
        },
        {
            "order": "1.5",
            "action": "BAŞKA DOSYA OLUŞTUR: pnpm-workspace.yaml",
            "type": "code_write",
            "file": "pnpm-workspace.yaml",
            "code": "packages:\n  - \"packages/*\"",
            "why": "Bu dosya pnpm'e 'packages/ altındaki her klasör bağımsız bir paket' diyor. Monorepo'nun beyni bu dosya — yoksa pnpm alt paketleri tanımaz."
        },
        {
            "order": "1.6",
            "action": "Alt paket dizinlerini oluştur",
            "type": "terminal",
            "command": "mkdir -p packages/api packages/dashboard",
            "expected_output": "Dizinler oluşturuldu",
            "why": "1.5'te tanımladığımız packages/* pattern'ına uygun dizinleri oluşturuyoruz. api backend'i, dashboard frontend'i barındıracak."
        },
        {
            "order": "1.7",
            "action": "concurrently paketini root workspace'e kur",
            "type": "terminal",
            "command": "pnpm add -D concurrently -w",
            "expected_output": "devDependencies:\n+ concurrently",
            "why": "1.3'te script'e yazdığımız concurrently'yi şimdi kuruyoruz. -w flag'i 'root workspace'e kur' demek — alt paketlere değil."
        },
        {
            "order": "1.8",
            "action": ".gitignore dosyası oluştur",
            "type": "code_write",
            "file": ".gitignore",
            "code": "node_modules\ndist\n.env\n*.log",
            "why": "node_modules ve .env dosyaları git'e eklenmemeli. Senior'lar projenin ilk adımında .gitignore oluşturur — sonra unutulur."
        },
        {
            "order": "1.9",
            "action": "git init ile versiyon kontrolünü başlat",
            "type": "terminal",
            "command": "git init && git add . && git commit -m \"chore: initial monorepo setup\"",
            "expected_output": "Initialized empty Git repository",
            "why": "Her milestone'dan sonra commit atmak yerine, en baştan git başlatıyoruz. İlk commit projenin 'sıfır noktası' — geri dönülecek yer."
        },
        {
            "order": "1.10",
            "action": "Doğrulama: pnpm-workspace.yaml ve dizin yapısını kontrol et",
            "type": "validate",
            "validation": "ls packages/ komutu ile api ve dashboard klasörlerini gör. cat pnpm-workspace.yaml ile packages/* tanımını doğrula. pnpm ls komutu hata vermemeli.",
            "why": "Monorepo yapısının doğru kurulduğunu kanıtlamadan ilerlemek tehlikeli — sonraki adımlarda anlaşılmaz hatalar alırsın."
        }
    ]

    # M1.S2: PostgreSQL Time-Series Schema (step 2)
    data["milestones"][0]["steps"][1]["substeps"] = [
        {
            "order": "2.1",
            "action": "PostgreSQL veritabanını oluştur",
            "type": "terminal",
            "command": "createdb analytics_dashboard",
            "expected_output": "Veritabanı oluşturuldu (çıktı yok ise başarılı)",
            "why": "Her proje kendi veritabanına sahip olmalı. analytics_dashboard ismi projeyle birebir eşleşiyor — senior'lar veritabanı isimlerinde proje adını kullanır."
        },
        {
            "order": "2.2",
            "action": "Migrations dizinini oluştur",
            "type": "terminal",
            "command": "mkdir -p packages/api/migrations",
            "expected_output": "Dizin oluşturuldu",
            "why": "Schema değişikliklerini SQL dosyalarında tutmak production standardı. 'migrations' ismi Rails/Django dünyasından gelir, endüstri standardı."
        },
        {
            "order": "2.3",
            "action": "DOSYA AÇ: 001_create_metrics.sql → önce CREATE TABLE iskeletini yaz",
            "type": "code_write",
            "file": "packages/api/migrations/001_create_metrics.sql",
            "code": "CREATE TABLE metrics (\n  id BIGSERIAL PRIMARY KEY,\n  source VARCHAR(100) NOT NULL,\n  metric_name VARCHAR(200) NOT NULL,\n  value DOUBLE PRECISION NOT NULL,\n  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),\n  metadata JSONB DEFAULT '{}'\n);",
            "why": "Önce tablonun iskeletini yazıyoruz — sütunlar ve tipler. BIGSERIAL büyük veri setleri için şart. TIMESTAMPTZ timezone-aware — TIMESTAMP kullanma, global kullanıcılarda sorun çıkarır."
        },
        {
            "order": "2.4",
            "action": "Aynı dosyanın ALTINA → unique constraint ekle",
            "type": "code_write",
            "file": "packages/api/migrations/001_create_metrics.sql",
            "code": "ALTER TABLE metrics ADD CONSTRAINT idx_source_metric_time\n  UNIQUE (source, metric_name, timestamp);",
            "why": "2.3'te yarattığımız tabloya unique constraint ekliyoruz. Aynı source + metric + timestamp kombinasyonu iki kez eklenmesin — veri bütünlüğü için kritik."
        },
        {
            "order": "2.5",
            "action": "Aynı dosyanın ALTINA → performans index'lerini ekle",
            "type": "code_write",
            "file": "packages/api/migrations/001_create_metrics.sql",
            "code": "CREATE INDEX idx_metrics_timestamp\n  ON metrics (timestamp DESC);\n\nCREATE INDEX idx_metrics_source\n  ON metrics (source, timestamp DESC);",
            "why": "Dashboard sorguları hep 'son X saat/gün' şeklinde olacak. timestamp DESC index'i bu sorguları 100x hızlandırır. source + timestamp composite index ise filtrelemeli sorgular için."
        },
        {
            "order": "2.6",
            "action": "Migration dosyasını PostgreSQL'de çalıştır",
            "type": "terminal",
            "command": "psql -d analytics_dashboard -f packages/api/migrations/001_create_metrics.sql",
            "expected_output": "CREATE TABLE\nALTER TABLE\nCREATE INDEX\nCREATE INDEX",
            "why": "2.3-2.5'te yazdığımız SQL'i çalıştırıyoruz. Her CREATE ifadesi için ayrı bir başarı mesajı görmelisin."
        },
        {
            "order": "2.7",
            "action": "Tablo yapısını doğrula",
            "type": "terminal",
            "command": "psql -d analytics_dashboard -c \"\\d metrics\"",
            "expected_output": "Table \"public.metrics\" ile sütun listesi görünmeli",
            "why": "\\d komutu PostgreSQL'in 'describe' komutu. Sütun isimlerinin, tiplerinin ve default değerlerin doğru olduğunu kontrol ediyoruz."
        },
        {
            "order": "2.8",
            "action": "Test verisi ekle ve sorgula",
            "type": "terminal",
            "command": "psql -d analytics_dashboard -c \"INSERT INTO metrics (source, metric_name, value) VALUES ('web-app', 'cpu_usage', 45.2); SELECT * FROM metrics;\"",
            "expected_output": "INSERT 0 1 ve eklenen satır görünmeli",
            "why": "Schema'nın gerçekten çalıştığını kanıtlıyoruz. DEFAULT NOW() ile timestamp otomatik dolmuş olmalı. Bu 'smoke test' pattern'ı senior'ların vazgeçilmezi."
        },
        {
            "order": "2.9",
            "action": "Index'lerin oluştuğunu doğrula",
            "type": "terminal",
            "command": "psql -d analytics_dashboard -c \"\\di\"",
            "expected_output": "idx_metrics_timestamp ve idx_metrics_source index'leri listelenmiş olmalı",
            "why": "Index'ler sorgu performansının anahtarı. 2.5'te oluşturduğumuz index'lerin gerçekten var olduğunu doğruluyoruz."
        },
        {
            "order": "2.10",
            "action": "Doğrulama: timestamp range query çalışıyor mu?",
            "type": "validate",
            "validation": "psql -d analytics_dashboard -c \"SELECT * FROM metrics WHERE timestamp > NOW() - INTERVAL '1 hour';\" komutu ile son 1 saatteki veriyi çekebilmelisin. Sonuç dönmeli.",
            "why": "Dashboard'ın temel sorgusu bu: 'son X süredeki veriyi getir'. Bu sorgu çalışmazsa dashboard'un hiçbir özelliği çalışmaz."
        }
    ]

    # M1.S3: Express API ve Aggregation Endpoint'leri (step 3)
    data["milestones"][0]["steps"][2]["substeps"] = [
        {
            "order": "3.1",
            "action": "API paketini başlat ve bağımlılıkları kur",
            "type": "terminal",
            "command": "cd packages/api && pnpm init && pnpm add express pg dotenv cors && pnpm add -D typescript ts-node @types/express @types/cors @types/pg nodemon",
            "expected_output": "dependencies: + express + pg + dotenv + cors",
            "why": "API paketi kendi package.json'ına sahip — monorepo'da her paket bağımsız. express web framework, pg PostgreSQL client, dotenv ortam değişkenleri için."
        },
        {
            "order": "3.2",
            "action": "DOSYA AÇ: tsconfig.json → TypeScript ayarlarını yaz",
            "type": "code_write",
            "file": "packages/api/tsconfig.json",
            "code": "{\n  \"compilerOptions\": {\n    \"target\": \"ES2020\",\n    \"module\": \"commonjs\",\n    \"outDir\": \"./dist\",\n    \"rootDir\": \"./src\",\n    \"strict\": true,\n    \"esModuleInterop\": true,\n    \"resolveJsonModule\": true\n  },\n  \"include\": [\"src/**/*\"]\n}",
            "why": "strict: true tüm tip kontrollerini aktif eder — senior standart. esModuleInterop CommonJS modüllerini import sözdizimi ile kullanmayı sağlar."
        },
        {
            "order": "3.3",
            "action": "Kaynak dizin yapısını oluştur",
            "type": "terminal",
            "command": "mkdir -p packages/api/src/routes",
            "expected_output": "Dizinler oluşturuldu",
            "why": "src/ kaynak kodlar, routes/ API endpoint tanımları. Bu Express projelerinde standart dizin yapısı."
        },
        {
            "order": "3.4",
            "action": "DOSYA AÇ: src/index.ts → Express sunucu İSKELETİNİ yaz",
            "type": "code_write",
            "file": "packages/api/src/index.ts",
            "code": "import express from 'express';\n\nconst app = express();\n\napp.get('/health', (req, res) => {\n  res.json({ status: 'ok' });\n});\n\nconst PORT = 4000;\napp.listen(PORT, () => console.log(`API: port ${PORT}`));",
            "why": "Önce çalışan en basit sunucuyu yazıyoruz — sadece health endpoint. Senior'lar her zaman 'önce çalışsın, sonra zenginleştir' der."
        },
        {
            "order": "3.5",
            "action": "Dosyanın ÜSTÜNE ÇIK → cors ve pg import'larını ekle",
            "type": "code_write",
            "file": "packages/api/src/index.ts",
            "code": "import express from 'express';\nimport cors from 'cors';\nimport { Pool } from 'pg';\nimport dotenv from 'dotenv';\n\ndotenv.config();",
            "why": "3.4'te iskelet çalıştıktan sonra şimdi gerçek bağımlılıkları ekliyoruz. dotenv.config() en üstte çağrılmalı — sonraki kodlar process.env'e bağlı."
        },
        {
            "order": "3.6",
            "action": "Fonksiyona GERİ DÖN → middleware ve pool ekle",
            "type": "code_write",
            "file": "packages/api/src/index.ts",
            "code": "const app = express();\nexport const pool = new Pool({\n  connectionString: process.env.DATABASE_URL\n});\n\napp.use(cors());\napp.use(express.json());",
            "why": "3.5'te import ettiğimiz Pool'u şimdi kullanıyoruz. Pool singleton pattern — uygulama boyunca tek bir bağlantı havuzu. export ediyoruz çünkü route dosyaları da kullanacak."
        },
        {
            "order": "3.7",
            "action": "DOSYA AÇ: .env → veritabanı bağlantı bilgisini yaz",
            "type": "code_write",
            "file": "packages/api/.env",
            "code": "DATABASE_URL=postgresql://localhost:5432/analytics_dashboard\nPORT=4000",
            "why": "3.6'da process.env.DATABASE_URL kullandık — şimdi değerini tanımlıyoruz. Bağlantı bilgisi asla kod içinde hardcode edilmez."
        },
        {
            "order": "3.8",
            "action": "BAŞKA DOSYAYA GEÇ: src/routes/metrics.ts → route İSKELETİNİ yaz",
            "type": "code_write",
            "file": "packages/api/src/routes/metrics.ts",
            "code": "import { Router } from 'express';\n\nconst router = Router();\n\nrouter.get('/metrics', async (req, res) => {\n  res.json({ message: 'metrics endpoint hazır' });\n});\n\nexport default router;",
            "why": "Önce çalışan boş bir endpoint yazıyoruz. Import, Router oluştur, bir route tanımla, export et — Express route dosyasının temel iskeleti bu."
        },
        {
            "order": "3.9",
            "action": "Dosyanın ÜSTÜNE ÇIK → pool import'unu ekle",
            "type": "code_write",
            "file": "packages/api/src/routes/metrics.ts",
            "code": "import { Router } from 'express';\nimport { pool } from '../index';",
            "why": "3.8'de iskelet çalıştı, şimdi gerçek veritabanı sorgusu yazacağız. Bunun için 3.6'da export ettiğimiz pool'u import ediyoruz."
        },
        {
            "order": "3.10",
            "action": "Route handler'a GERİ DÖN → INTERVAL_MAP ve validation yaz",
            "type": "code_write",
            "file": "packages/api/src/routes/metrics.ts",
            "code": "const INTERVAL_MAP: Record<string, string> = {\n  '1h': 'hour', '1d': 'day',\n  '1w': 'week', '1m': 'month',\n};\n\nrouter.get('/metrics', async (req, res) => {\n  const { source, metric, from, to, interval = '1h' } = req.query;\n  const pgInterval = INTERVAL_MAP[interval as string];\n  if (!pgInterval) {\n    return res.status(400).json({ error: 'Geçersiz interval' });\n  }\n});",
            "why": "Kullanıcı '1h' gönderir, PostgreSQL 'hour' bekler. INTERVAL_MAP bu dönüşümü yapar. Geçersiz interval'de 400 döndürüyoruz — input validation senior standardı."
        },
        {
            "order": "3.11",
            "action": "Route handler'ın İÇİNE → PostgreSQL aggregation sorgusunu ekle",
            "type": "code_write",
            "file": "packages/api/src/routes/metrics.ts",
            "code": "  const result = await pool.query(\n    `SELECT date_trunc($1, timestamp) as bucket,\n     AVG(value) as avg_value,\n     MIN(value) as min_value,\n     MAX(value) as max_value,\n     COUNT(*) as count\n     FROM metrics WHERE source = $2 AND metric_name = $3\n     AND timestamp BETWEEN $4 AND $5\n     GROUP BY bucket ORDER BY bucket ASC`,\n    [pgInterval, source, metric, from, to]\n  );\n  res.json(result.rows);",
            "why": "date_trunc PostgreSQL'in time-series süper gücü — milyonlarca satırı saniyeler içinde gruplar. $1, $2... parametreli sorgular SQL injection'a karşı korur."
        },
        {
            "order": "3.12",
            "action": "index.ts'e GERİ DÖN → metrics route'unu bağla",
            "type": "code_write",
            "file": "packages/api/src/index.ts",
            "code": "import metricsRouter from './routes/metrics';\napp.use('/api', metricsRouter);",
            "why": "3.8-3.11'de yazdığımız route'u Express uygulamasına mount ediyoruz. /api prefix'i ile endpoint /api/metrics olacak."
        },
        {
            "order": "3.13",
            "action": "package.json'a dev script ekle",
            "type": "code_write",
            "file": "packages/api/package.json",
            "code": "\"scripts\": {\n  \"dev\": \"nodemon --exec ts-node src/index.ts\",\n  \"build\": \"tsc\",\n  \"start\": \"node dist/index.js\"\n}",
            "why": "nodemon dosya değişikliklerinde otomatik restart yapar. ts-node TypeScript'i derlemeden çalıştırır — geliştirme döngüsünü hızlandırır."
        },
        {
            "order": "3.14",
            "action": "Sunucuyu başlat ve health endpoint'ini test et",
            "type": "terminal",
            "command": "cd packages/api && pnpm run dev",
            "expected_output": "API: port 4000",
            "why": "Her şeyin bağlandığını doğruluyoruz. curl http://localhost:4000/health ile {\"status\":\"ok\"} dönmeli."
        },
        {
            "order": "3.15",
            "action": "Doğrulama: metrics endpoint'ini test et",
            "type": "validate",
            "validation": "curl 'http://localhost:4000/api/metrics?source=web-app&metric=cpu_usage&from=2024-01-01&to=2025-01-01&interval=1h' komutu ile aggregated veri dönmeli. Parametresiz çağrıda hata mesajı dönmeli.",
            "why": "3.10'da yazdığımız validation ve 3.11'deki aggregation sorgusunun ikisinin de çalıştığını kanıtlıyoruz."
        }
    ]

    # M1.S4: React Dashboard Scaffolding (step 4)
    data["milestones"][0]["steps"][3]["substeps"] = [
        {
            "order": "4.1",
            "action": "Vite ile React + TypeScript projesi oluştur",
            "type": "terminal",
            "command": "cd packages && pnpm create vite dashboard --template react-ts",
            "expected_output": "Scaffolding project in packages/dashboard",
            "why": "Vite modern build aracı — CRA'ya göre 10x hızlı dev server. react-ts template'i TypeScript ile gelir."
        },
        {
            "order": "4.2",
            "action": "Bağımlılıkları kur: recharts ve react-grid-layout",
            "type": "terminal",
            "command": "cd packages/dashboard && pnpm install && pnpm add recharts react-grid-layout && pnpm add -D @types/react-grid-layout",
            "expected_output": "dependencies: + recharts + react-grid-layout",
            "why": "Recharts React ekosistemiyle tam uyumlu chart kütüphanesi. react-grid-layout widget'ları sürükle-bırak ile düzenlemeyi sağlar."
        },
        {
            "order": "4.3",
            "action": "Klasör yapısını oluştur",
            "type": "terminal",
            "command": "cd packages/dashboard && mkdir -p src/components src/hooks src/pages src/utils src/types",
            "expected_output": "Dizinler oluşturuldu",
            "why": "components UI bileşenleri, hooks özel hook'lar, pages sayfa bileşenleri, utils yardımcı fonksiyonlar, types tip tanımları — standart React proje yapısı."
        },
        {
            "order": "4.4",
            "action": "DOSYA AÇ: ChartWidget.tsx → component İSKELETİNİ yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/ChartWidget.tsx",
            "code": "export function ChartWidget() {\n  return (\n    <div className=\"bg-gray-800 rounded-lg shadow p-4\">\n      <h3 className=\"text-sm text-gray-300\">Chart Placeholder</h3>\n    </div>\n  );\n}",
            "why": "Senior yaklaşım: önce ekranda BİR ŞEY göster. İskelet hazır, import yok, props yok — sadece çalışan bir kutu."
        },
        {
            "order": "4.5",
            "action": "Dosyanın ÜSTÜNE ÇIK → Recharts import'larını ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/components/ChartWidget.tsx",
            "code": "import {\n  ResponsiveContainer, LineChart, Line,\n  XAxis, YAxis, Tooltip\n} from 'recharts';",
            "why": "4.4'te iskelet çalıştı, şimdi grafik kütüphanesini ekliyoruz. ResponsiveContainer parent boyutuna göre otomatik resize yapar — chart'larda ZORUNLU."
        },
        {
            "order": "4.6",
            "action": "Fonksiyona GERİ DÖN → props interface ve chart JSX'ini yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/ChartWidget.tsx",
            "code": "interface ChartWidgetProps {\n  title: string;\n  data: Array<{ bucket: string; avg_value: number }>;\n  color?: string;\n}\n\nexport function ChartWidget({ title, data, color = '#8884d8' }: ChartWidgetProps) {\n  return (\n    <div className=\"bg-gray-800 rounded-lg shadow p-4\">\n      <h3 className=\"text-sm font-medium text-gray-300 mb-2\">{title}</h3>\n      <ResponsiveContainer width=\"100%\" height={200}>\n        <LineChart data={data}>\n          <XAxis dataKey=\"bucket\" />\n          <YAxis />\n          <Tooltip />\n          <Line type=\"monotone\" dataKey=\"avg_value\" stroke={color} dot={false} />\n        </LineChart>\n      </ResponsiveContainer>\n    </div>\n  );\n}",
            "why": "4.5'te import ettiğimiz Recharts component'lerini kullanıyoruz. TypeScript interface ile prop tipleri güvenli. color default değeri ile opsiyonel prop pattern'ı."
        },
        {
            "order": "4.7",
            "action": "BAŞKA DOSYAYA GEÇ: App.tsx → mock veri ile test sayfası yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/App.tsx",
            "code": "import { ChartWidget } from './components/ChartWidget';\n\nconst mockData = Array.from({ length: 24 }, (_, i) => ({\n  bucket: String(i).padStart(2, '0') + ':00',\n  avg_value: 40 + Math.random() * 40,\n}));\n\nfunction App() {\n  return (\n    <div className=\"min-h-screen bg-gray-900 p-6\">\n      <h1 className=\"text-2xl font-bold text-white mb-6\">\n        Analytics Dashboard\n      </h1>\n      <div className=\"grid grid-cols-2 gap-4\">\n        <ChartWidget title=\"CPU Kullanımı\" data={mockData} color=\"#8884d8\" />\n        <ChartWidget title=\"Bellek\" data={mockData} color=\"#82ca9d\" />\n      </div>\n    </div>\n  );\n}\n\nexport default App;",
            "why": "4.4-4.6'da yazdığımız ChartWidget'ı gerçek kullanımda test ediyoruz. Mock veri ile backend hazır olmadan frontend geliştirme — paralel çalışma senior pattern'ı."
        },
        {
            "order": "4.8",
            "action": "Dashboard'u başlat ve tarayıcıda kontrol et",
            "type": "terminal",
            "command": "cd packages/dashboard && pnpm run dev",
            "expected_output": "Local: http://localhost:5173",
            "why": "Vite dev server'ı başlatarak 4.7'de yazdığımız sayfanın tarayıcıda doğru göründüğünü kontrol ediyoruz."
        },
        {
            "order": "4.9",
            "action": "Doğrulama: dark tema ve chart render kontrolü",
            "type": "validate",
            "validation": "http://localhost:5173 adresinde koyu arka planlı dashboard açılmalı. İki line chart mock veri ile görünmeli. Chart'ların üzerine gelince tooltip çalışmalı. Tarayıcı konsolunda hata olmamalı.",
            "why": "ResponsiveContainer doğru çalışmazsa chart boyutu 0x0 olur ve hiçbir şey görünmez. Bu doğrulama ile hem layout hem chart render'ı kanıtlıyoruz."
        }
    ]

    # ============================================================
    # MILESTONE 2: Veri Toplama ve Redis Cache
    # ============================================================

    # M2.S1: Veri Simülasyonu ve Seed (step 1)
    data["milestones"][1]["steps"][0]["substeps"] = [
        {
            "order": "1.1",
            "action": "Scripts dizinini oluştur",
            "type": "terminal",
            "command": "mkdir -p packages/api/scripts",
            "expected_output": "Dizin oluşturuldu",
            "why": "Seed ve migration script'lerini ayrı bir dizinde tutmak proje organizasyonunu temiz tutar. src/ uygulama kodu, scripts/ yardımcı script'ler."
        },
        {
            "order": "1.2",
            "action": "DOSYA AÇ: scripts/seed.ts → İSKELET fonksiyonu yaz",
            "type": "code_write",
            "file": "packages/api/scripts/seed.ts",
            "code": "async function seedMetrics() {\n  console.log('Seeding başlıyor...');\n  // TODO: veri üretimi\n  console.log('Seeding tamamlandı');\n}\n\nseedMetrics().catch(console.error);",
            "why": "Önce çalışan boş bir iskelet. async fonksiyon + .catch pattern'ı — top-level async'in doğru hata yakalama yöntemi."
        },
        {
            "order": "1.3",
            "action": "Dosyanın ÜSTÜNE ÇIK → pg ve dotenv import'larını ekle",
            "type": "code_write",
            "file": "packages/api/scripts/seed.ts",
            "code": "import { Pool } from 'pg';\nimport dotenv from 'dotenv';\n\ndotenv.config();\n\nconst pool = new Pool({\n  connectionString: process.env.DATABASE_URL\n});",
            "why": "1.2'deki iskelet çalıştı, şimdi veritabanı bağlantısı ekliyoruz. M1.S3'te oluşturduğumuz .env dosyasındaki DATABASE_URL'yi kullanıyoruz."
        },
        {
            "order": "1.4",
            "action": "Fonksiyona GERİ DÖN → source ve metric tanımlarını ekle",
            "type": "code_write",
            "file": "packages/api/scripts/seed.ts",
            "code": "const sources = ['web-app', 'mobile-app', 'api-gateway'];\nconst metrics = [\n  'cpu_usage', 'memory_usage', 'response_time',\n  'error_rate', 'request_count'\n];\n\nfunction getBaseValue(metric: string): number {\n  const bases: Record<string, number> = {\n    cpu_usage: 55, memory_usage: 70,\n    response_time: 150, error_rate: 2,\n    request_count: 1000,\n  };\n  return bases[metric] || 50;\n}",
            "why": "3 source x 5 metric = 15 kombinasyon. Her metriğin gerçekçi bir base değeri var — CPU %55 civarı, response_time 150ms gibi. Bu değerler gerçek dünya verilerine yakın."
        },
        {
            "order": "1.5",
            "action": "seedMetrics fonksiyonunun İÇİNE → veri üretim döngüsünü yaz",
            "type": "code_write",
            "file": "packages/api/scripts/seed.ts",
            "code": "  const now = Date.now();\n  const thirtyDaysAgo = now - 30 * 24 * 60 * 60 * 1000;\n  let count = 0;\n\n  for (const source of sources) {\n    for (const metric of metrics) {\n      const baseValue = getBaseValue(metric);\n      const values: string[] = [];",
            "why": "Son 30 günlük veri üretiyoruz, 5 dakika aralıklarla. Nested loop: her source için her metric. values array'ini batch insert için topluyoruz."
        },
        {
            "order": "1.6",
            "action": "İç döngüye → gerçekçi değer üretimi ekle",
            "type": "code_write",
            "file": "packages/api/scripts/seed.ts",
            "code": "      for (let ts = thirtyDaysAgo; ts < now; ts += 5 * 60 * 1000) {\n        const hour = new Date(ts).getHours();\n        const daily = Math.sin((hour - 6) * Math.PI / 12) * 0.2;\n        const noise = (Math.random() - 0.5) * 0.1;\n        const spike = Math.random() > 0.995 ? Math.random() * 0.5 : 0;\n        const value = baseValue * (1 + daily + noise + spike);\n        values.push(\n          `('${source}','${metric}',${value.toFixed(4)},'${new Date(ts).toISOString()}')`\n        );\n        count++;\n      }",
            "why": "sin() ile günlük pattern (gündüz yüksek, gece düşük), noise ile doğal varyasyon, spike ile nadir anomaliler. Bu 3 katman gerçekçi time-series verisi üretir."
        },
        {
            "order": "1.7",
            "action": "Döngü sonrasına → batch insert ve cleanup ekle",
            "type": "code_write",
            "file": "packages/api/scripts/seed.ts",
            "code": "      const batchSize = 1000;\n      for (let i = 0; i < values.length; i += batchSize) {\n        const batch = values.slice(i, i + batchSize);\n        await pool.query(\n          `INSERT INTO metrics (source, metric_name, value, timestamp)\n           VALUES ${batch.join(',')}\n           ON CONFLICT DO NOTHING`\n        );\n      }\n    }\n  }\n  console.log(`${count} metrik eklendi`);\n  await pool.end();",
            "why": "1000'er satırlık batch insert — tek seferde 130K satır eklemek bellek taşırır. ON CONFLICT DO NOTHING tekrar çalıştırıldığında duplicate hatası vermez."
        },
        {
            "order": "1.8",
            "action": "package.json'a seed script'i ekle",
            "type": "code_modify",
            "file": "packages/api/package.json",
            "code": "\"seed\": \"ts-node scripts/seed.ts\"",
            "why": "pnpm run seed komutu ile seed'i kolayca çalıştırabilmek için. Script'leri package.json'da tanımlamak takım çalışmasında herkesin aynı komutu kullanmasını sağlar."
        },
        {
            "order": "1.9",
            "action": "Seed script'ini çalıştır",
            "type": "terminal",
            "command": "cd packages/api && pnpm run seed",
            "expected_output": "129600 metrik eklendi (yaklaşık)",
            "why": "3 source x 5 metric x 8640 zaman noktası (30 gün, 5 dk aralık) = ~129600 satır. Dashboard'un gerçekçi görünmesi için yeterli veri."
        },
        {
            "order": "1.10",
            "action": "Doğrulama: veri sayısı ve dağılımı",
            "type": "validate",
            "validation": "psql -d analytics_dashboard -c \"SELECT COUNT(*) FROM metrics;\" ile 100K+ satır. psql -d analytics_dashboard -c \"SELECT source, metric_name, COUNT(*) FROM metrics GROUP BY source, metric_name;\" ile 15 satır, her biri yaklaşık eşit.",
            "why": "1.6'da eklediğimiz spike'lar (anomaliler) M4'te anomali tespiti için kullanılacak. Veri dağılımının dengeli olduğunu şimdi doğruluyoruz."
        }
    ]

    # M2.S2: Redis Cache Katmanı (step 2)
    data["milestones"][1]["steps"][1]["substeps"] = [
        {
            "order": "2.1",
            "action": "Redis'i başlat",
            "type": "terminal",
            "command": "redis-server --daemonize yes",
            "expected_output": "Redis server started",
            "why": "Redis in-memory veri deposu — cache katmanı olarak kullanacağız. Dashboard sorguları tekrar tekrar aynı veriyi çeker, Redis ile response time 200ms'den 5ms'e düşer."
        },
        {
            "order": "2.2",
            "action": "ioredis paketini kur",
            "type": "terminal",
            "command": "cd packages/api && pnpm add ioredis && pnpm add -D @types/ioredis",
            "expected_output": "dependencies: + ioredis",
            "why": "ioredis Node.js için en performanslı Redis client'ı. Built-in TypeScript desteği ve otomatik reconnect özelliği var."
        },
        {
            "order": "2.3",
            "action": ".env dosyasına Redis URL ekle",
            "type": "code_modify",
            "file": "packages/api/.env",
            "code": "REDIS_URL=redis://localhost:6379",
            "why": "M1.S3'te oluşturduğumuz .env dosyasına Redis bağlantısını ekliyoruz. Production'da farklı bir adres olacak."
        },
        {
            "order": "2.4",
            "action": "Middleware dizinini oluştur",
            "type": "terminal",
            "command": "mkdir -p packages/api/src/middleware",
            "expected_output": "Dizin oluşturuldu",
            "why": "Cache middleware'ini ayrı dizinde tutuyoruz — Express'te middleware'ler route'lardan ayrı yaşar."
        },
        {
            "order": "2.5",
            "action": "DOSYA AÇ: middleware/cache.ts → Redis bağlantısı ve İSKELET yaz",
            "type": "code_write",
            "file": "packages/api/src/middleware/cache.ts",
            "code": "import Redis from 'ioredis';\nimport { Request, Response, NextFunction } from 'express';\n\nconst redis = new Redis(process.env.REDIS_URL);\n\nexport function cacheMiddleware(ttlFn: (req: Request) => number) {\n  return async (req: Request, res: Response, next: NextFunction) => {\n    next();\n  };\n}\n\nexport { redis };",
            "why": "Önce çalışan bir iskelet — middleware var ama sadece next() çağırıyor. Redis bağlantısı hazır, ttlFn parametresi farklı endpoint'ler için farklı cache süresi sağlayacak."
        },
        {
            "order": "2.6",
            "action": "Fonksiyona GERİ DÖN → cache okuma ve X-Cache header logic'ini ekle",
            "type": "code_write",
            "file": "packages/api/src/middleware/cache.ts",
            "code": "  return async (req: Request, res: Response, next: NextFunction) => {\n    const key = `dashboard:${req.originalUrl}`;\n    const cached = await redis.get(key);\n    if (cached) {\n      res.setHeader('X-Cache', 'HIT');\n      return res.json(JSON.parse(cached));\n    }\n    next();\n  };",
            "why": "Cache key olarak URL kullanıyoruz — farklı filtreler farklı cache entry'leri. X-Cache: HIT header'ı debug için altın değerinde. Cache varsa DB'ye hiç gitmeden döndürüyoruz."
        },
        {
            "order": "2.7",
            "action": "next() çağrısından ÖNCE → res.json override ile cache yazma ekle",
            "type": "code_write",
            "file": "packages/api/src/middleware/cache.ts",
            "code": "    const originalJson = res.json.bind(res);\n    res.json = (body: any) => {\n      const ttl = ttlFn(req);\n      redis.setex(key, ttl, JSON.stringify(body));\n      res.setHeader('X-Cache', 'MISS');\n      return originalJson(body);\n    };\n    next();",
            "why": "res.json'ı override ediyoruz — route handler res.json() çağırdığında otomatik olarak Redis'e yazıyoruz. .bind(res) ile this context'i koruyoruz, yoksa TypeError alırsın."
        },
        {
            "order": "2.8",
            "action": "BAŞKA DOSYAYA GEÇ: routes/metrics.ts → cache middleware'ini bağla",
            "type": "code_write",
            "file": "packages/api/src/routes/metrics.ts",
            "code": "import { cacheMiddleware } from '../middleware/cache';\n\nrouter.get('/metrics', cacheMiddleware(req => {\n  const from = new Date(req.query.from as string).getTime();\n  const to = new Date(req.query.to as string).getTime();\n  const range = to - from;\n  if (range < 3600000) return 30;\n  if (range < 86400000) return 300;\n  return 1800;\n}), async (req, res) => {\n  // mevcut handler kodu\n});",
            "why": "2.5-2.7'de yazdığımız cache middleware'ini route'a ekliyoruz. TTL stratejisi: son 1 saat -> 30sn, son 1 gün -> 5dk, daha eski -> 30dk. Kısa aralık sık değişir, uzun aralık nadiren."
        },
        {
            "order": "2.9",
            "action": "Cache'in çalıştığını test et — iki istek at",
            "type": "terminal",
            "command": "curl -v 'http://localhost:4000/api/metrics?source=web-app&metric=cpu_usage&from=2024-01-01&to=2024-01-02&interval=1h' 2>&1 | grep X-Cache",
            "expected_output": "İlk istekte X-Cache: MISS, ikinci istekte X-Cache: HIT",
            "why": "2.6'da eklediğimiz X-Cache header'ını kontrol ediyoruz. İlk istek DB'ye gider (MISS), ikinci istek Redis'ten döner (HIT)."
        },
        {
            "order": "2.10",
            "action": "Redis CLI ile cache key'lerini kontrol et",
            "type": "terminal",
            "command": "redis-cli KEYS 'dashboard:*'",
            "expected_output": "dashboard:/api/metrics?... şeklinde key'ler listelenmiş olmalı",
            "why": "Cache'in gerçekten Redis'e yazıldığını doğruluyoruz. Bu debug tekniği production'da da kullanılır."
        },
        {
            "order": "2.11",
            "action": "Doğrulama: cache mekanizması tam çalışıyor",
            "type": "validate",
            "validation": "İlk API isteğinde X-Cache: MISS, tekrarında X-Cache: HIT. TTL süresi geçtikten sonra tekrar MISS dönmeli. redis-cli TTL komutu ile kalan süreyi görebilmelisin.",
            "why": "Cache HIT/MISS, TTL ve key yapısının üçünün de doğru çalıştığını kanıtlıyoruz."
        }
    ]

    # M2.S3: Multi-Source Data Aggregation API (step 3)
    data["milestones"][1]["steps"][2]["substeps"] = [
        {
            "order": "3.1",
            "action": "Utils dizinini oluştur",
            "type": "terminal",
            "command": "mkdir -p packages/api/src/utils",
            "expected_output": "Dizin oluşturuldu",
            "why": "Yardımcı fonksiyonları utils/ dizininde tutuyoruz. Route handler'lar şişmesin — logic ayrı, routing ayrı."
        },
        {
            "order": "3.2",
            "action": "DOSYA AÇ: utils/metrics.ts → aggregation helper İSKELETİNİ yaz",
            "type": "code_write",
            "file": "packages/api/src/utils/metrics.ts",
            "code": "export async function getAggregatedMetric(\n  metricName: string, from: string, to: string\n) {\n  return { latest: 0, trend: 0, status: 'healthy', series: [] };\n}",
            "why": "Önce fonksiyon imzası ve dönüş tipini belirliyoruz — iskelet. Dashboard overview endpoint'i bu fonksiyonu her metrik için çağıracak."
        },
        {
            "order": "3.3",
            "action": "Dosyanın ÜSTÜNE ÇIK → pool import'unu ekle",
            "type": "code_write",
            "file": "packages/api/src/utils/metrics.ts",
            "code": "import { pool } from '../index';",
            "why": "3.2'deki iskelet hazır, şimdi gerçek DB sorgusu ekleyeceğiz. M1.S3'te export ettiğimiz pool'u import ediyoruz."
        },
        {
            "order": "3.4",
            "action": "Fonksiyona GERİ DÖN → gerçek DB sorgusu ve hesaplamaları yaz",
            "type": "code_write",
            "file": "packages/api/src/utils/metrics.ts",
            "code": "export async function getAggregatedMetric(\n  metricName: string, from: string, to: string\n) {\n  const result = await pool.query(\n    `SELECT date_trunc('hour', timestamp) as bucket,\n     AVG(value) as avg_value\n     FROM metrics WHERE metric_name = $1\n     AND timestamp BETWEEN $2 AND $3\n     GROUP BY bucket ORDER BY bucket ASC`,\n    [metricName, from, to]\n  );\n  const series = result.rows;\n  const latest = series.length > 0\n    ? series[series.length - 1].avg_value : 0;\n  const prev = series.length > 1\n    ? series[series.length - 2].avg_value : latest;\n  return {\n    latest, trend: latest - prev,\n    status: latest > 90 ? 'critical'\n      : latest > 75 ? 'warning' : 'healthy',\n    series\n  };\n}",
            "why": "3.2'deki iskeletin yerine gerçek implementasyonu koyuyoruz. trend = son değer - önceki değer. status threshold'ları metriğe göre belirleniyor."
        },
        {
            "order": "3.5",
            "action": "BAŞKA DOSYAYA GEÇ: routes/dashboard.ts → route İSKELETİNİ yaz",
            "type": "code_write",
            "file": "packages/api/src/routes/dashboard.ts",
            "code": "import { Router } from 'express';\n\nconst router = Router();\n\nrouter.get('/overview', async (req, res) => {\n  res.json({ message: 'overview endpoint hazır' });\n});\n\nexport default router;",
            "why": "Önce çalışan boş bir endpoint. 3.2-3.4'te yazdığımız helper fonksiyonu burada kullanacağız ama önce route'un kendisi çalışsın."
        },
        {
            "order": "3.6",
            "action": "Dosyanın ÜSTÜNE ÇIK → helper ve cache import'larını ekle",
            "type": "code_write",
            "file": "packages/api/src/routes/dashboard.ts",
            "code": "import { Router } from 'express';\nimport { getAggregatedMetric } from '../utils/metrics';\nimport { cacheMiddleware } from '../middleware/cache';",
            "why": "3.4'te yazdığımız getAggregatedMetric ve M2.S2'de yazdığımız cacheMiddleware'i import ediyoruz."
        },
        {
            "order": "3.7",
            "action": "Route handler'a GERİ DÖN → Promise.all ile paralel sorgular yaz",
            "type": "code_write",
            "file": "packages/api/src/routes/dashboard.ts",
            "code": "router.get('/overview', cacheMiddleware(() => 60), async (req, res) => {\n  const { from = new Date(Date.now() - 86400000).toISOString(),\n    to = new Date().toISOString() } = req.query;\n  const [cpu, mem, err, lat] = await Promise.all([\n    getAggregatedMetric('cpu_usage', from as string, to as string),\n    getAggregatedMetric('memory_usage', from as string, to as string),\n    getAggregatedMetric('error_rate', from as string, to as string),\n    getAggregatedMetric('response_time', from as string, to as string),\n  ]);\n  res.json({\n    summary: { cpu, memory: mem, errors: err, latency: lat },\n    charts: { cpu: cpu.series, memory: mem.series,\n      errors: err.series, latency: lat.series }\n  });\n});",
            "why": "Promise.all ile 4 DB sorgusunu paralel çalıştırıyoruz — sequential'e göre 4x hızlı. Dashboard API'lerinde bu pattern zorunlu."
        },
        {
            "order": "3.8",
            "action": "BAŞKA DOSYAYA GEÇ: index.ts → dashboard route'unu bağla",
            "type": "code_write",
            "file": "packages/api/src/index.ts",
            "code": "import dashboardRouter from './routes/dashboard';\napp.use('/api/dashboard', dashboardRouter);",
            "why": "3.5-3.7'de yazdığımız dashboard route'unu Express uygulamasına mount ediyoruz. URL: /api/dashboard/overview"
        },
        {
            "order": "3.9",
            "action": "Overview endpoint'ini test et",
            "type": "terminal",
            "command": "curl http://localhost:4000/api/dashboard/overview | python -m json.tool | head -20",
            "expected_output": "JSON response: summary ve charts objesi",
            "why": "3.7'de yazdığımız endpoint'in 4 metriğin hem summary hem chart verisini tek response'ta döndürdüğünü doğruluyoruz."
        },
        {
            "order": "3.10",
            "action": "Doğrulama: cache ve paralel sorguların performansı",
            "type": "validate",
            "validation": "İlk istek ~200ms sürmeli (DB), ikinci istek ~5ms (cache). Response'ta summary.cpu.status 'healthy'/'warning'/'critical' değerlerinden biri olmalı.",
            "why": "Promise.all performansı ve cache TTL'inin doğru çalıştığını kanıtlıyoruz."
        }
    ]

    # ============================================================
    # MILESTONE 3: İnteraktif Dashboard Frontend
    # ============================================================

    # M3.S1: useMetrics Custom Hook (step 1)
    data["milestones"][2]["steps"][0]["substeps"] = [
        {
            "order": "1.1",
            "action": "DOSYA AÇ: types/metrics.ts → tip tanımlarını yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/types/metrics.ts",
            "code": "export interface MetricPoint {\n  bucket: string;\n  avg_value: number;\n  min_value?: number;\n  max_value?: number;\n  count?: number;\n}\n\nexport interface MetricSummary {\n  current: number;\n  trend: number;\n  status: 'healthy' | 'warning' | 'critical';\n}",
            "why": "TypeScript'te önce tipler tanımlanır. API response yapısını interface ile tanımlıyoruz — yanlış property erişimi derleme zamanında yakalanır."
        },
        {
            "order": "1.2",
            "action": "Aynı dosyaya → DashboardOverview tipini ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/types/metrics.ts",
            "code": "export interface DashboardOverview {\n  summary: Record<string, MetricSummary>;\n  charts: Record<string, MetricPoint[]>;\n}",
            "why": "1.1'deki MetricSummary ve MetricPoint'i kullanan üst düzey tip. M2.S3'te yazdığımız overview endpoint'inin response yapısıyla birebir eşleşiyor."
        },
        {
            "order": "1.3",
            "action": "BAŞKA DOSYAYA GEÇ: hooks/useMetrics.ts → hook İSKELETİNİ yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useMetrics.ts",
            "code": "export function useMetrics() {\n  return { data: [], loading: true, error: null };\n}",
            "why": "Senior yaklaşım: önce hook'un dönüş şeklini belirle. Dışarıdan { data, loading, error } şeklinde kullanılacak — bu pattern React'te standart."
        },
        {
            "order": "1.4",
            "action": "Dosyanın ÜSTÜNE ÇIK → React hook import'larını ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useMetrics.ts",
            "code": "import { useState, useEffect, useRef } from 'react';\nimport { MetricPoint } from '../types/metrics';",
            "why": "1.3'teki iskelet hazır, şimdi state yönetimi için React hook'larını ekliyoruz. 1.1'de tanımladığımız MetricPoint tipini import ediyoruz."
        },
        {
            "order": "1.5",
            "action": "Fonksiyona GERİ DÖN → parametre interface ve state tanımlarını yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useMetrics.ts",
            "code": "interface UseMetricsOptions {\n  source: string;\n  metric: string;\n  from: Date;\n  to: Date;\n  interval?: string;\n  refreshInterval?: number;\n}\n\nexport function useMetrics(options: UseMetricsOptions) {\n  const [data, setData] = useState<MetricPoint[]>([]);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState<Error | null>(null);\n  const staleData = useRef<MetricPoint[]>([]);",
            "why": "1.4'te import ettiğimiz useState, useRef'i kullanıyoruz. staleData SWR pattern'ı için — eski veriyi gösterirken yeni veri yüklenir."
        },
        {
            "order": "1.6",
            "action": "State tanımlarının ALTINA → useEffect ile veri çekme logic'ini yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useMetrics.ts",
            "code": "  useEffect(() => {\n    const fetchData = async () => {\n      try {\n        if (staleData.current.length > 0) {\n          setData(staleData.current);\n          setLoading(false);\n        }\n        const params = new URLSearchParams({\n          source: options.source, metric: options.metric,\n          from: options.from.toISOString(),\n          to: options.to.toISOString(),\n          interval: options.interval || '1h',\n        });\n        const res = await fetch(`/api/metrics?${params}`);\n        const json = await res.json();\n        setData(json);\n        staleData.current = json;\n        setError(null);\n      } catch (err) {\n        setError(err as Error);\n      } finally {\n        setLoading(false);\n      }\n    };\n    fetchData();\n  }, [options.source, options.metric,\n    options.from.getTime(), options.to.getTime()]);",
            "why": "SWR pattern: eski veriyi hemen göster, arka planda yeni veri çek. useEffect dependency array'inde Date objesi değil getTime() kullanıyoruz — Date referans karşılaştırması yapar."
        },
        {
            "order": "1.7",
            "action": "useEffect'in ALTINA → refreshInterval desteği ve return ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useMetrics.ts",
            "code": "  useEffect(() => {\n    if (!options.refreshInterval) return;\n    const timer = setInterval(() => {\n      // fetchData tekrar çağrılacak\n    }, options.refreshInterval);\n    return () => clearInterval(timer);\n  }, [options.refreshInterval]);\n\n  return { data, loading, error };",
            "why": "Dashboard'lar gerçek zamanlı güncellenir. refreshInterval ile belirlenen aralıkta otomatik veri yenileme. return () => clearInterval cleanup fonksiyonu bellek sızıntısını önler."
        },
        {
            "order": "1.8",
            "action": "BAŞKA DOSYAYA GEÇ: App.tsx → useMetrics hook'unu test et",
            "type": "code_write",
            "file": "packages/dashboard/src/App.tsx",
            "code": "import { useMetrics } from './hooks/useMetrics';\nimport { ChartWidget } from './components/ChartWidget';\n\nfunction App() {\n  const { data, loading, error } = useMetrics({\n    source: 'web-app',\n    metric: 'cpu_usage',\n    from: new Date(Date.now() - 86400000),\n    to: new Date(),\n  });\n\n  if (loading) return <div className=\"text-white\">Yükleniyor...</div>;\n  if (error) return <div className=\"text-red-400\">Hata: {error.message}</div>;\n\n  return (\n    <div className=\"min-h-screen bg-gray-900 p-6\">\n      <ChartWidget title=\"CPU Kullanımı\" data={data} />\n    </div>\n  );\n}",
            "why": "1.3-1.7'de yazdığımız hook'u gerçek kullanımda test ediyoruz. loading ve error state'lerinin doğru çalıştığını görsel olarak kontrol ediyoruz."
        },
        {
            "order": "1.9",
            "action": "Doğrulama: hook ile veri çekme ve loading state",
            "type": "validate",
            "validation": "Tarayıcıda 'Yükleniyor...' yazısı kısa süre görünmeli, sonra chart verisi ile grafik render olmalı. Network tab'da /api/metrics isteği görünmeli.",
            "why": "useMetrics hook'unun API'den veri çektiğini, loading -> data geçişinin düzgün çalıştığını kanıtlıyoruz."
        }
    ]

    # M3.S2: Multi-Chart Dashboard Layout (step 2)
    data["milestones"][2]["steps"][1]["substeps"] = [
        {
            "order": "2.1",
            "action": "DOSYA AÇ: components/SummaryCard.tsx → İSKELET yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/SummaryCard.tsx",
            "code": "export function SummaryCard() {\n  return (\n    <div className=\"bg-gray-800 rounded-lg p-4\">\n      <p className=\"text-gray-400\">Placeholder</p>\n    </div>\n  );\n}",
            "why": "Dashboard'un üstündeki KPI kartları — CPU: %55, Memory: %70 gibi. Önce boş bir kutu, sonra zenginleştireceğiz."
        },
        {
            "order": "2.2",
            "action": "Fonksiyona GERİ DÖN → props ve içerik ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/components/SummaryCard.tsx",
            "code": "interface SummaryCardProps {\n  title: string;\n  value: number;\n  unit: string;\n  trend: number;\n  status: 'healthy' | 'warning' | 'critical';\n}\n\nconst STATUS_COLORS = {\n  healthy: 'text-emerald-400',\n  warning: 'text-yellow-400',\n  critical: 'text-red-400',\n};\n\nexport function SummaryCard({ title, value, unit, trend, status }: SummaryCardProps) {\n  return (\n    <div className=\"bg-gray-800 rounded-lg p-4\">\n      <p className=\"text-sm text-gray-400\">{title}</p>\n      <p className={`text-2xl font-bold ${STATUS_COLORS[status]}`}>\n        {value.toFixed(1)}{unit}\n      </p>\n      <p className={`text-sm ${trend > 0 ? 'text-red-400' : 'text-emerald-400'}`}>\n        {trend > 0 ? '\u2191' : '\u2193'} {Math.abs(trend).toFixed(1)}\n      </p>\n    </div>\n  );\n}",
            "why": "2.1'deki iskeletin yerine gerçek içerik. status'e göre renk değişiyor — critical kırmızı, warning sarı, healthy yeşil."
        },
        {
            "order": "2.3",
            "action": "DOSYA AÇ: components/DateRangePicker.tsx → tarih filtresi İSKELETİ yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/DateRangePicker.tsx",
            "code": "export function DateRangePicker() {\n  return (\n    <div className=\"flex gap-2\">\n      <button className=\"px-3 py-1 bg-gray-700 text-gray-300 rounded\">\n        Placeholder\n      </button>\n    </div>\n  );\n}",
            "why": "Dashboard'da 'Son 1 saat', 'Son 24 saat' gibi filtreler olacak. Önce iskelet."
        },
        {
            "order": "2.4",
            "action": "Fonksiyona GERİ DÖN → preset butonları ve callback ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/components/DateRangePicker.tsx",
            "code": "interface DateRangePickerProps {\n  onChange: (from: Date, to: Date) => void;\n}\n\nconst PRESETS = [\n  { label: 'Son 1 Saat', hours: 1 },\n  { label: 'Son 24 Saat', hours: 24 },\n  { label: 'Son 7 G\u00fcn', hours: 168 },\n  { label: 'Son 30 G\u00fcn', hours: 720 },\n];\n\nexport function DateRangePicker({ onChange }: DateRangePickerProps) {\n  return (\n    <div className=\"flex gap-2\">\n      {PRESETS.map(p => (\n        <button key={p.hours}\n          className=\"px-3 py-1 bg-gray-700 text-gray-300 rounded\n            hover:bg-gray-600 transition-colors\"\n          onClick={() => onChange(\n            new Date(Date.now() - p.hours * 3600000),\n            new Date()\n          )}>\n          {p.label}\n        </button>\n      ))}\n    </div>\n  );\n}",
            "why": "2.3't\u00fcki placeholder'\u0131 ger\u00e7ek butonlarla de\u011fi\u015ftirdik. PRESETS array'i ile yeni tarih aral\u0131\u011f\u0131 eklemek tek sat\u0131r."
        },
        {
            "order": "2.5",
            "action": "DOSYA A\u00c7: components/SourceFilter.tsx \u2192 kaynak filtresi yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/SourceFilter.tsx",
            "code": "interface SourceFilterProps {\n  sources: string[];\n  selected: string;\n  onChange: (source: string) => void;\n}\n\nexport function SourceFilter({ sources, selected, onChange }: SourceFilterProps) {\n  return (\n    <div className=\"flex gap-2\">\n      {sources.map(s => (\n        <button key={s}\n          className={`px-3 py-1 rounded transition-colors ${\n            s === selected\n              ? 'bg-blue-600 text-white'\n              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'\n          }`}\n          onClick={() => onChange(s)}>\n          {s}\n        </button>\n      ))}\n    </div>\n  );\n}",
            "why": "web-app, mobile-app, api-gateway aras\u0131nda ge\u00e7i\u015f yapmak i\u00e7in. Se\u00e7ili kaynak mavi, di\u011ferleri gri \u2014 g\u00f6rsel geri bildirim UX i\u00e7in kritik."
        },
        {
            "order": "2.6",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: pages/Dashboard.tsx \u2192 ana dashboard \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "export default function Dashboard() {\n  return (\n    <div className=\"min-h-screen bg-gray-900 p-6\">\n      <h1 className=\"text-2xl font-bold text-white mb-6\">\n        Analytics Dashboard\n      </h1>\n      <p className=\"text-gray-400\">\u0130\u00e7erik gelecek...</p>\n    </div>\n  );\n}",
            "why": "Ana sayfa iskeleti. \u00d6nce layout ve ba\u015fl\u0131k, sonra component'leri ekleyece\u011fiz."
        },
        {
            "order": "2.7",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 gerekli import'lar\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "import { useState } from 'react';\nimport { useMetrics } from '../hooks/useMetrics';\nimport { SummaryCard } from '../components/SummaryCard';\nimport { ChartWidget } from '../components/ChartWidget';\nimport { DateRangePicker } from '../components/DateRangePicker';\nimport { SourceFilter } from '../components/SourceFilter';",
            "why": "2.1-2.5'te yazd\u0131\u011f\u0131m\u0131z t\u00fcm component'leri ve M3.S1'deki useMetrics hook'unu import ediyoruz."
        },
        {
            "order": "2.8",
            "action": "Fonksiyona GER\u0130 D\u00d6N \u2192 state ve hook \u00e7a\u011fr\u0131lar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "  const [source, setSource] = useState('web-app');\n  const [dateRange, setDateRange] = useState({\n    from: new Date(Date.now() - 86400000),\n    to: new Date()\n  });\n  const cpu = useMetrics({ source, metric: 'cpu_usage', ...dateRange });\n  const mem = useMetrics({ source, metric: 'memory_usage', ...dateRange });\n  const err = useMetrics({ source, metric: 'error_rate', ...dateRange });\n  const lat = useMetrics({ source, metric: 'response_time', ...dateRange });",
            "why": "2.7'de import etti\u011fimiz useState ve useMetrics'i kullan\u0131yoruz. 4 metrik i\u00e7in 4 hook \u00e7a\u011fr\u0131s\u0131 \u2014 her biri ba\u011f\u0131ms\u0131z loading state'ine sahip."
        },
        {
            "order": "2.9",
            "action": "Return JSX'ini G\u00dcNCELLE \u2192 filtreler, summary kartlar\u0131 ve chart'lar\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "  return (\n    <div className=\"min-h-screen bg-gray-900 p-6\">\n      <div className=\"flex justify-between items-center mb-6\">\n        <h1 className=\"text-2xl font-bold text-white\">Analytics Dashboard</h1>\n        <DateRangePicker onChange={(from, to) => setDateRange({ from, to })} />\n      </div>\n      <SourceFilter\n        sources={['web-app', 'mobile-app', 'api-gateway']}\n        selected={source}\n        onChange={setSource}\n      />\n      <div className=\"grid grid-cols-4 gap-4 mt-4\">\n        <SummaryCard title=\"CPU\" value={55} unit=\"%\" trend={2.1} status=\"healthy\" />\n        <SummaryCard title=\"Bellek\" value={70} unit=\"%\" trend={-1.5} status=\"warning\" />\n        <SummaryCard title=\"Hata Oran\u0131\" value={1.2} unit=\"%\" trend={0.3} status=\"healthy\" />\n        <SummaryCard title=\"Gecikme\" value={145} unit=\"ms\" trend={-5} status=\"healthy\" />\n      </div>\n      <div className=\"grid grid-cols-2 gap-4 mt-4\">\n        <ChartWidget title=\"CPU Kullan\u0131m\u0131\" data={cpu.data} color=\"#8884d8\" />\n        <ChartWidget title=\"Bellek Kullan\u0131m\u0131\" data={mem.data} color=\"#82ca9d\" />\n        <ChartWidget title=\"Hata Oran\u0131\" data={err.data} color=\"#ff7300\" />\n        <ChartWidget title=\"Yan\u0131t S\u00fcresi\" data={lat.data} color=\"#ffc658\" />\n      </div>\n    </div>\n  );",
            "why": "2.1-2.5'teki component'ler ve 2.8'deki hook verileri bir araya geldi. 4 summary kart \u00fcstte, 4 chart altta \u2014 profesyonel dashboard layout'u."
        },
        {
            "order": "2.10",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: App.tsx \u2192 Dashboard sayfas\u0131n\u0131 kullan",
            "type": "code_write",
            "file": "packages/dashboard/src/App.tsx",
            "code": "import Dashboard from './pages/Dashboard';\n\nfunction App() {\n  return <Dashboard />;\n}\n\nexport default App;",
            "why": "App.tsx sadece routing yapacak, as\u0131l i\u00e7erik pages/ alt\u0131nda. \u015eimdilik tek sayfa var ama ileride eklenebilir."
        },
        {
            "order": "2.11",
            "action": "Do\u011frulama: dashboard layout ve filtreleme",
            "type": "validate",
            "validation": "4 summary kart \u00fcstte grid halinde g\u00f6r\u00fcnmeli. 4 chart altta 2x2 grid'de render olmal\u0131. DateRangePicker butonlar\u0131 \u00e7al\u0131\u015fmal\u0131 \u2014 t\u0131klan\u0131nca chart'lar g\u00fcncellenmeli.",
            "why": "T\u00fcm component'lerin bir arada \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131, filtrelemenin hook'lar\u0131 tetikledi\u011fini kan\u0131tl\u0131yoruz."
        }
    ]

    # M3.S3: Advanced Chart Features (step 3)
    data["milestones"][2]["steps"][2]["substeps"] = [
        {
            "order": "3.1",
            "action": "DOSYA A\u00c7: components/AdvancedChart.tsx \u2192 \u0130SKELET yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/AdvancedChart.tsx",
            "code": "export function AdvancedChart() {\n  return (\n    <div className=\"bg-gray-800 rounded-lg p-4\">\n      <p className=\"text-gray-400\">Advanced chart placeholder</p>\n    </div>\n  );\n}",
            "why": "ChartWidget basit chart'lar i\u00e7indi. AdvancedChart zoom, brush, custom tooltip gibi ileri \u00f6zellikler ekleyecek."
        },
        {
            "order": "3.2",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 Recharts import'lar\u0131n\u0131 ekle (Brush dahil)",
            "type": "code_write",
            "file": "packages/dashboard/src/components/AdvancedChart.tsx",
            "code": "import {\n  ResponsiveContainer, ComposedChart, Line, Area,\n  XAxis, YAxis, Tooltip, Brush, CartesianGrid,\n  Legend, ReferenceLine\n} from 'recharts';\nimport { MetricPoint } from '../types/metrics';",
            "why": "3.1'deki iskelet haz\u0131r, \u015fimdi ileri Recharts component'lerini ekliyoruz. Brush zoom \u00f6zelli\u011fi, ReferenceLine threshold \u00e7izgisi i\u00e7in."
        },
        {
            "order": "3.3",
            "action": "Fonksiyona GER\u0130 D\u00d6N \u2192 custom tooltip component'ini yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/AdvancedChart.tsx",
            "code": "function CustomTooltip({ active, payload, label }: any) {\n  if (!active || !payload?.length) return null;\n  return (\n    <div className=\"bg-gray-900 border border-gray-700 p-3 rounded\">\n      <p className=\"text-gray-400 text-sm\">{label}</p>\n      {payload.map((p: any) => (\n        <p key={p.name} style={{ color: p.color }} className=\"text-sm\">\n          {p.name}: {Number(p.value).toFixed(2)}\n        </p>\n      ))}\n    </div>\n  );\n}",
            "why": "Recharts'\u0131n default tooltip'i dark tema ile uyumsuz. Custom tooltip ile gray-900 arka plan kullanarak tutarl\u0131 dark tema sa\u011fl\u0131yoruz."
        },
        {
            "order": "3.4",
            "action": "AdvancedChart component'ini \u2192 props ve tam chart JSX ile yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/AdvancedChart.tsx",
            "code": "interface AdvancedChartProps {\n  title: string;\n  data: MetricPoint[];\n  color?: string;\n  threshold?: number;\n  showBrush?: boolean;\n}\n\nexport function AdvancedChart({\n  title, data, color = '#8884d8',\n  threshold, showBrush = true\n}: AdvancedChartProps) {\n  return (\n    <div className=\"bg-gray-800 rounded-lg p-4\">\n      <h3 className=\"text-sm font-medium text-gray-300 mb-2\">{title}</h3>\n      <ResponsiveContainer width=\"100%\" height={300}>\n        <ComposedChart data={data}>\n          <CartesianGrid strokeDasharray=\"3 3\" stroke=\"#374151\" />\n          <XAxis dataKey=\"bucket\" stroke=\"#9CA3AF\" />\n          <YAxis stroke=\"#9CA3AF\" />\n          <Tooltip content={<CustomTooltip />} />\n          <Legend />\n          <Area type=\"monotone\" dataKey=\"avg_value\" fill={color}\n            fillOpacity={0.1} stroke=\"none\" />\n          <Line type=\"monotone\" dataKey=\"avg_value\" stroke={color}\n            dot={false} name=\"Ortalama\" />\n          {threshold && <ReferenceLine y={threshold}\n            stroke=\"#EF4444\" strokeDasharray=\"5 5\"\n            label=\"E\u015fik\" />}\n          {showBrush && <Brush dataKey=\"bucket\" height={30}\n            stroke=\"#6B7280\" fill=\"#1F2937\" />}\n        </ComposedChart>\n      </ResponsiveContainer>\n    </div>\n  );\n}",
            "why": "3.2'deki import'lar\u0131 ve 3.3'teki custom tooltip'i kullan\u0131yoruz. ComposedChart Line + Area bir arada. Brush alt k\u0131s\u0131mda zoom kontrol\u00fc sa\u011flar."
        },
        {
            "order": "3.5",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: pages/Dashboard.tsx \u2192 AdvancedChart'\u0131 import et ve kullan",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "import { AdvancedChart } from '../components/AdvancedChart';",
            "why": "3.1-3.4'te yazd\u0131\u011f\u0131m\u0131z AdvancedChart'\u0131 dashboard'a ekliyoruz."
        },
        {
            "order": "3.6",
            "action": "Dashboard'daki ChartWidget'lar\u0131 AdvancedChart ile de\u011fi\u015ftir",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "        <AdvancedChart title=\"CPU Kullan\u0131m\u0131\" data={cpu.data}\n          color=\"#8884d8\" threshold={80} />\n        <AdvancedChart title=\"Bellek Kullan\u0131m\u0131\" data={mem.data}\n          color=\"#82ca9d\" threshold={90} />\n        <AdvancedChart title=\"Hata Oran\u0131\" data={err.data}\n          color=\"#ff7300\" threshold={5} />\n        <AdvancedChart title=\"Yan\u0131t S\u00fcresi\" data={lat.data}\n          color=\"#ffc658\" threshold={200} />",
            "why": "3.5'te import etti\u011fimiz AdvancedChart'\u0131 kullan\u0131yoruz. Her metrik i\u00e7in farkl\u0131 threshold \u2014 CPU %80, bellek %90, hata %5, gecikme 200ms."
        },
        {
            "order": "3.7",
            "action": "Do\u011frulama: brush zoom ve custom tooltip",
            "type": "validate",
            "validation": "Chart'lar\u0131n alt\u0131nda brush (kayd\u0131rma \u00e7ubu\u011fu) g\u00f6r\u00fcnmeli. Brush'\u0131 s\u00fcr\u00fckleyerek zoom yapabilmelisin. Tooltip dark temada do\u011fru renklerde g\u00f6r\u00fcnmeli. ReferenceLine k\u0131rm\u0131z\u0131 kesikli \u00e7izgi olarak threshold'u g\u00f6stermeli.",
            "why": "3.2'deki Brush, 3.3'teki CustomTooltip ve 3.4'teki ReferenceLine'\u0131n hepsinin do\u011fru \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 do\u011fruluyoruz."
        }
    ]

    # ============================================================
    # MILESTONE 4: AI Anomali Tespiti
    # ============================================================

    # M4.S1: \u0130statistiksel Anomali Tespiti (Z-Score)
    data["milestones"][3]["steps"][0]["substeps"] = [
        {
            "order": "1.1",
            "action": "ML service dizinini olu\u015ftur",
            "type": "terminal",
            "command": "mkdir -p packages/ml-service",
            "expected_output": "Dizin olu\u015fturuldu",
            "why": "Anomali tespiti Python ile yap\u0131lacak \u2014 ayr\u0131 bir servis. Node.js ve Python'un g\u00fc\u00e7l\u00fc yanlar\u0131n\u0131 birle\u015ftiriyoruz."
        },
        {
            "order": "1.2",
            "action": "DOSYA A\u00c7: ml-service/requirements.txt \u2192 ba\u011f\u0131ml\u0131l\u0131klar\u0131 yaz",
            "type": "code_write",
            "file": "packages/ml-service/requirements.txt",
            "code": "fastapi==0.104.1\nuvicorn==0.24.0\nscikit-learn==1.3.2\nnumpy==1.26.2\npandas==2.1.4\npsycopg2-binary==2.9.9\npython-dotenv==1.0.0",
            "why": "FastAPI web framework, scikit-learn ML k\u00fct\u00fcphanesi, pandas veri i\u015fleme, psycopg2 PostgreSQL ba\u011flant\u0131s\u0131. Versiyon pinleme production standard\u0131."
        },
        {
            "order": "1.3",
            "action": "Ba\u011f\u0131ml\u0131l\u0131klar\u0131 kur",
            "type": "terminal",
            "command": "cd packages/ml-service && pip install -r requirements.txt",
            "expected_output": "Successfully installed fastapi scikit-learn ...",
            "why": "1.2'de tan\u0131mlad\u0131\u011f\u0131m\u0131z ba\u011f\u0131ml\u0131l\u0131klar\u0131 kuruyoruz. Virtual environment kullanman \u00f6nerilir: python -m venv venv"
        },
        {
            "order": "1.4",
            "action": "DOSYA A\u00c7: ml-service/main.py \u2192 FastAPI \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/ml-service/main.py",
            "code": "from fastapi import FastAPI\n\napp = FastAPI(title=\"Anomaly Detection Service\")\n\n@app.get(\"/health\")\ndef health():\n    return {\"status\": \"ok\"}",
            "why": "\u00d6nce \u00e7al\u0131\u015fan en basit FastAPI uygulamas\u0131 \u2014 sadece health endpoint. Senior yakla\u015f\u0131m: iskelet \u00e7al\u0131\u015ft\u0131r, sonra zenginle\u015ftir."
        },
        {
            "order": "1.5",
            "action": "BA\u015eKA DOSYA A\u00c7: ml-service/anomaly_detector.py \u2192 Z-Score s\u0131n\u0131f\u0131 \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/ml-service/anomaly_detector.py",
            "code": "class ZScoreDetector:\n    def __init__(self, threshold: float = 3.0):\n        self.threshold = threshold\n\n    def detect(self, values: list[float]) -> list[bool]:\n        return [False] * len(values)",
            "why": "\u00d6nce s\u0131n\u0131f iskeleti ve imzas\u0131. detect metodu bir de\u011fer listesi al\u0131r, her de\u011fer i\u00e7in anomali mi de\u011fil mi d\u00f6nd\u00fcr\u00fcr. Threshold 3.0 istatistikte standart."
        },
        {
            "order": "1.6",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 numpy import'unu ekle",
            "type": "code_write",
            "file": "packages/ml-service/anomaly_detector.py",
            "code": "import numpy as np",
            "why": "1.5'teki iskelet haz\u0131r, \u015fimdi ger\u00e7ek Z-Score hesaplamas\u0131 i\u00e7in numpy laz\u0131m. Z-Score = (de\u011fer - ortalama) / standart sapma"
        },
        {
            "order": "1.7",
            "action": "detect metoduna GER\u0130 D\u00d6N \u2192 ger\u00e7ek Z-Score hesaplamas\u0131n\u0131 yaz",
            "type": "code_write",
            "file": "packages/ml-service/anomaly_detector.py",
            "code": "    def detect(self, values: list[float]) -> list[dict]:\n        arr = np.array(values)\n        mean = np.mean(arr)\n        std = np.std(arr)\n        if std == 0:\n            return [{\"is_anomaly\": False, \"z_score\": 0.0, \"value\": v} for v in values]\n        z_scores = (arr - mean) / std\n        return [\n            {\n                \"is_anomaly\": bool(abs(z) > self.threshold),\n                \"z_score\": round(float(z), 4),\n                \"value\": float(v)\n            }\n            for z, v in zip(z_scores, values)\n        ]",
            "why": "1.6'da import etti\u011fimiz numpy ile Z-Score form\u00fcl\u00fcn\u00fc uyguluyor\u00faz. std == 0 kontrol\u00fc \u2014 t\u00fcm de\u011ferler ayn\u0131ysa b\u00f6lme hatas\u0131 olur."
        },
        {
            "order": "1.8",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: main.py \u2192 Z-Score endpoint'ini ekle",
            "type": "code_write",
            "file": "packages/ml-service/main.py",
            "code": "from anomaly_detector import ZScoreDetector\nfrom pydantic import BaseModel\n\ndetector = ZScoreDetector(threshold=3.0)\n\nclass DetectRequest(BaseModel):\n    values: list[float]\n    threshold: float = 3.0\n\n@app.post(\"/api/anomalies/zscore\")\ndef detect_zscore(req: DetectRequest):\n    detector.threshold = req.threshold\n    results = detector.detect(req.values)\n    anomalies = [r for r in results if r[\"is_anomaly\"]]\n    return {\n        \"total\": len(results),\n        \"anomaly_count\": len(anomalies),\n        \"results\": results\n    }",
            "why": "1.5-1.7'de yazd\u0131\u011f\u0131m\u0131z ZScoreDetector'\u0131 API endpoint'i olarak sunuyoruz. Pydantic BaseModel ile request validation otomatik."
        },
        {
            "order": "1.9",
            "action": "FastAPI sunucusunu ba\u015flat ve test et",
            "type": "terminal",
            "command": "cd packages/ml-service && uvicorn main:app --port 8001 --reload",
            "expected_output": "Uvicorn running on http://0.0.0.0:8001",
            "why": "ML service'i ayr\u0131 port'ta \u00e7al\u0131\u015ft\u0131r\u0131yoruz (8001). --reload ile dosya de\u011fi\u015fikliklerinde otomatik restart."
        },
        {
            "order": "1.10",
            "action": "Z-Score endpoint'ini test et",
            "type": "terminal",
            "command": "curl -X POST http://localhost:8001/api/anomalies/zscore -H 'Content-Type: application/json' -d '{\"values\": [10, 12, 11, 10, 50, 11, 12, 10]}'",
            "expected_output": "anomaly_count: 1 (50 de\u011feri anomali olarak i\u015faretlenmeli)",
            "why": "1.7'de yazd\u0131\u011f\u0131m\u0131z Z-Score hesaplamas\u0131n\u0131n ger\u00e7ekten \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 test ediyoruz. 50 de\u011feri di\u011ferlerinden \u00e7ok farkl\u0131 \u2014 anomali olarak yakalanmal\u0131."
        },
        {
            "order": "1.11",
            "action": "Do\u011frulama: Z-Score anomali tespiti do\u011frulu\u011fu",
            "type": "validate",
            "validation": "Normal de\u011ferler (10-12 aral\u0131\u011f\u0131) is_anomaly: false olmal\u0131. Ayk\u0131r\u0131 de\u011fer (50) is_anomaly: true olmal\u0131. z_score de\u011ferleri mant\u0131kl\u0131 olmal\u0131 (normal: -1 ile 1 aras\u0131, anomali: 3+).",
            "why": "M2.S1'de seed veriye ekledi\u011fimiz spike'lar\u0131 yakalayabilmemiz i\u00e7in Z-Score'un do\u011fru \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 kan\u0131tl\u0131yoruz."
        }
    ]

    # M4.S2: Isolation Forest ile ML Anomali Tespiti
    data["milestones"][3]["steps"][1]["substeps"] = [
        {
            "order": "2.1",
            "action": "DOSYA A\u00c7: anomaly_detector.py \u2192 IsolationForestDetector \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/ml-service/anomaly_detector.py",
            "code": "class IsolationForestDetector:\n    def __init__(self, contamination: float = 0.05):\n        self.contamination = contamination\n        self.model = None\n\n    def train(self, features):\n        pass\n\n    def predict(self, features):\n        return []",
            "why": "Z-Score tek de\u011fi\u015fkenli anomalileri yakalar ama CPU d\u00fc\u015f\u00fckken error y\u00fcksek gibi \u00e7ok de\u011fi\u015fkenli anomalileri ka\u00e7\u0131r\u0131r. Isolation Forest bunu \u00e7\u00f6zer."
        },
        {
            "order": "2.2",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 scikit-learn import'unu ekle",
            "type": "code_write",
            "file": "packages/ml-service/anomaly_detector.py",
            "code": "import numpy as np\nfrom sklearn.ensemble import IsolationForest\nfrom sklearn.preprocessing import StandardScaler",
            "why": "2.1'deki iskelet haz\u0131r, \u015fimdi ger\u00e7ek ML bile\u015fenlerini ekliyoruz. StandardScaler feature'lar\u0131 normalize eder."
        },
        {
            "order": "2.3",
            "action": "IsolationForestDetector s\u0131n\u0131f\u0131na GER\u0130 D\u00d6N \u2192 scaler ekle ve train metodunu yaz",
            "type": "code_write",
            "file": "packages/ml-service/anomaly_detector.py",
            "code": "    def __init__(self, contamination: float = 0.05):\n        self.contamination = contamination\n        self.model = IsolationForest(\n            contamination=contamination,\n            random_state=42,\n            n_estimators=100\n        )\n        self.scaler = StandardScaler()\n\n    def train(self, features: np.ndarray):\n        scaled = self.scaler.fit_transform(features)\n        self.model.fit(scaled)\n        return self",
            "why": "2.2'de import etti\u011fimiz IsolationForest ve StandardScaler'\u0131 kullan\u0131yoruz. contamination=0.05 \u2192 verinin %5'inin anomali olmas\u0131n\u0131 bekliyoruz."
        },
        {
            "order": "2.4",
            "action": "predict metodunu G\u00dcNCELLE \u2192 anomali skoru ve sonu\u00e7lar\u0131 d\u00f6nd\u00fcr",
            "type": "code_write",
            "file": "packages/ml-service/anomaly_detector.py",
            "code": "    def predict(self, features: np.ndarray) -> list[dict]:\n        scaled = self.scaler.transform(features)\n        predictions = self.model.predict(scaled)\n        scores = self.model.score_samples(scaled)\n        return [\n            {\n                \"is_anomaly\": bool(pred == -1),\n                \"anomaly_score\": round(float(score), 4),\n                \"features\": row.tolist()\n            }\n            for pred, score, row in zip(predictions, scores, features)\n        ]",
            "why": "2.3'te e\u011fitti\u011fimiz modelle tahmin yap\u0131yoruz. Isolation Forest -1 d\u00f6nd\u00fcr\u00fcrse anomali, 1 ise normal."
        },
        {
            "order": "2.5",
            "action": "BA\u015eKA DOSYA A\u00c7: ml-service/feature_engineering.py \u2192 feature \u00e7\u0131karma \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/ml-service/feature_engineering.py",
            "code": "def extract_features(data):\n    return []",
            "why": "Isolation Forest'a raw de\u011ferler yerine m\u00fchendislik yap\u0131lm\u0131\u015f feature'lar vermek do\u011frulu\u011fu art\u0131r\u0131r."
        },
        {
            "order": "2.6",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 pandas import'unu ekle, fonksiyonu yaz",
            "type": "code_write",
            "file": "packages/ml-service/feature_engineering.py",
            "code": "import pandas as pd\nimport numpy as np\n\ndef extract_features(df: pd.DataFrame) -> np.ndarray:\n    features = pd.DataFrame()\n    features['value'] = df['value']\n    features['hour'] = pd.to_datetime(df['timestamp']).dt.hour\n    features['rolling_mean'] = df['value'].rolling(12).mean()\n    features['rolling_std'] = df['value'].rolling(12).std()\n    features['diff'] = df['value'].diff()\n    features['is_weekend'] = pd.to_datetime(\n        df['timestamp']).dt.dayofweek >= 5\n    features = features.fillna(0)\n    return features.values",
            "why": "2.5'teki iskeletin yerine ger\u00e7ek feature engineering. rolling_mean/std son 1 saatlik trend, hour/is_weekend zamansal pattern'lar\u0131 yakalar."
        },
        {
            "order": "2.7",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: main.py \u2192 veritaban\u0131ndan veri \u00e7ekme fonksiyonu ekle",
            "type": "code_write",
            "file": "packages/ml-service/main.py",
            "code": "import psycopg2\nimport pandas as pd\nimport os\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\ndef fetch_metrics(metric_name: str, hours: int = 24) -> pd.DataFrame:\n    conn = psycopg2.connect(os.getenv('DATABASE_URL'))\n    query = \"\"\"\n        SELECT value, timestamp FROM metrics\n        WHERE metric_name = %s\n        AND timestamp > NOW() - INTERVAL '%s hours'\n        ORDER BY timestamp ASC\n    \"\"\"\n    df = pd.read_sql(query, conn, params=[metric_name, hours])\n    conn.close()\n    return df",
            "why": "ML modeli ger\u00e7ek veritaban\u0131 verisiyle \u00e7al\u0131\u015facak. M2.S1'de seed'ledi\u011fimiz veriyi \u00e7ekiyoruz."
        },
        {
            "order": "2.8",
            "action": "main.py'de \u2192 Isolation Forest train ve predict endpoint'lerini ekle",
            "type": "code_write",
            "file": "packages/ml-service/main.py",
            "code": "from anomaly_detector import IsolationForestDetector\nfrom feature_engineering import extract_features\n\nforest_detector = IsolationForestDetector(contamination=0.05)\n\n@app.post(\"/api/anomalies/train\")\ndef train_model(metric_name: str = \"cpu_usage\", hours: int = 168):\n    df = fetch_metrics(metric_name, hours)\n    features = extract_features(df)\n    forest_detector.train(features)\n    return {\"status\": \"trained\", \"samples\": len(df)}\n\n@app.post(\"/api/anomalies/detect\")\ndef detect_anomalies(metric_name: str = \"cpu_usage\", hours: int = 24):\n    df = fetch_metrics(metric_name, hours)\n    features = extract_features(df)\n    results = forest_detector.predict(features)\n    anomalies = [r for r in results if r[\"is_anomaly\"]]\n    return {\n        \"total\": len(results),\n        \"anomaly_count\": len(anomalies),\n        \"anomalies\": anomalies\n    }",
            "why": "2.3-2.4'teki IsolationForestDetector ve 2.6'daki extract_features'\u0131 API olarak sunuyoruz. Train: son 1 hafta veriyle e\u011fit. Detect: son 24 saatteki anomalileri bul."
        },
        {
            "order": "2.9",
            "action": ".env dosyas\u0131 olu\u015ftur",
            "type": "code_write",
            "file": "packages/ml-service/.env",
            "code": "DATABASE_URL=postgresql://localhost:5432/analytics_dashboard",
            "why": "2.7'de os.getenv('DATABASE_URL') kulland\u0131k \u2014 de\u011ferini tan\u0131ml\u0131yoruz."
        },
        {
            "order": "2.10",
            "action": "Modeli e\u011fit ve anomali tespiti yap",
            "type": "terminal",
            "command": "curl -X POST 'http://localhost:8001/api/anomalies/train?metric_name=cpu_usage&hours=168' && curl -X POST 'http://localhost:8001/api/anomalies/detect?metric_name=cpu_usage&hours=24'",
            "expected_output": "train: {status: trained, samples: 2000+}, detect: anomaly_count > 0",
            "why": "2.8'de yazd\u0131\u011f\u0131m\u0131z endpoint'leri test ediyoruz. \u00d6nce e\u011fit, sonra tespit et."
        },
        {
            "order": "2.11",
            "action": "Do\u011frulama: Isolation Forest vs Z-Score kar\u015f\u0131la\u015ft\u0131rmas\u0131",
            "type": "validate",
            "validation": "Isolation Forest'\u0131n Z-Score'dan daha fazla anomali yakalamas\u0131 beklenir \u00e7\u00fcnk\u00fc \u00e7ok de\u011fi\u015fkenli pattern'lar\u0131 anl\u0131yor. anomaly_score de\u011ferleri mant\u0131kl\u0131 olmal\u0131. /docs endpoint'inde Swagger UI a\u00e7\u0131lmal\u0131.",
            "why": "\u0130ki y\u00f6ntemin kar\u015f\u0131la\u015ft\u0131r\u0131lmas\u0131 ML projelerinde standart. Isolation Forest'\u0131n ek de\u011fer sa\u011flad\u0131\u011f\u0131n\u0131 kan\u0131tl\u0131yoruz."
        }
    ]

    # M4.S3: Anomali G\u00f6rselle\u015ftirme ve Alert
    data["milestones"][3]["steps"][2]["substeps"] = [
        {
            "order": "3.1",
            "action": "DOSYA A\u00c7: hooks/useAnomalies.ts \u2192 anomali veri hook \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useAnomalies.ts",
            "code": "export function useAnomalies() {\n  return { anomalies: [], loading: true };\n}",
            "why": "Chart'larda anomali noktalar\u0131n\u0131 g\u00f6stermek i\u00e7in ML service'ten veri \u00e7ekmemiz gerekiyor. \u00d6nce hook iskeleti."
        },
        {
            "order": "3.2",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 React import'lar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useAnomalies.ts",
            "code": "import { useState, useEffect } from 'react';",
            "why": "3.1'deki iskelet haz\u0131r, \u015fimdi state y\u00f6netimi ve veri \u00e7ekme i\u00e7in React hook'lar\u0131n\u0131 ekliyoruz."
        },
        {
            "order": "3.3",
            "action": "Fonksiyona GER\u0130 D\u00d6N \u2192 ML service'ten anomali verisi \u00e7ekme logic'ini yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useAnomalies.ts",
            "code": "interface Anomaly {\n  is_anomaly: boolean;\n  anomaly_score: number;\n  timestamp?: string;\n}\n\nexport function useAnomalies(metric: string) {\n  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);\n  const [loading, setLoading] = useState(true);\n\n  useEffect(() => {\n    fetch(`http://localhost:8001/api/anomalies/detect?metric_name=${metric}`)\n      .then(res => res.json())\n      .then(data => {\n        setAnomalies(data.anomalies || []);\n        setLoading(false);\n      })\n      .catch(() => setLoading(false));\n  }, [metric]);\n\n  return { anomalies, loading };\n}",
            "why": "3.2'de import etti\u011fimiz useState ve useEffect ile M4.S2'de yazd\u0131\u011f\u0131m\u0131z ML service endpoint'inden anomali verisi \u00e7ekiyoruz."
        },
        {
            "order": "3.4",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: components/AnomalyChart.tsx \u2192 anomali g\u00f6rselle\u015ftirmesi \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/AnomalyChart.tsx",
            "code": "export function AnomalyChart() {\n  return (\n    <div className=\"bg-gray-800 rounded-lg p-4\">\n      <p className=\"text-gray-400\">Anomaly chart placeholder</p>\n    </div>\n  );\n}",
            "why": "Anomali noktalar\u0131n\u0131 k\u0131rm\u0131z\u0131 dot olarak g\u00f6steren \u00f6zel bir chart component'i. \u00d6nce iskelet."
        },
        {
            "order": "3.5",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 Recharts ve tip import'lar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/components/AnomalyChart.tsx",
            "code": "import {\n  ResponsiveContainer, ComposedChart, Line, Scatter,\n  XAxis, YAxis, Tooltip, CartesianGrid\n} from 'recharts';\nimport { MetricPoint } from '../types/metrics';",
            "why": "3.4'teki iskelet haz\u0131r. Scatter component anomali noktalar\u0131n\u0131 ayr\u0131 renkte g\u00f6stermek i\u00e7in kullan\u0131lacak."
        },
        {
            "order": "3.6",
            "action": "Fonksiyona GER\u0130 D\u00d6N \u2192 anomali chart'\u0131n\u0131 tam olarak yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/AnomalyChart.tsx",
            "code": "interface AnomalyChartProps {\n  title: string;\n  data: MetricPoint[];\n  anomalyIndices: number[];\n  color?: string;\n}\n\nexport function AnomalyChart({\n  title, data, anomalyIndices, color = '#8884d8'\n}: AnomalyChartProps) {\n  const enriched = data.map((d, i) => ({\n    ...d,\n    anomaly: anomalyIndices.includes(i) ? d.avg_value : null\n  }));\n\n  return (\n    <div className=\"bg-gray-800 rounded-lg p-4\">\n      <h3 className=\"text-sm text-gray-300 mb-2\">{title}\n        <span className=\"ml-2 text-red-400 text-xs\">\n          {anomalyIndices.length} anomali\n        </span>\n      </h3>\n      <ResponsiveContainer width=\"100%\" height={300}>\n        <ComposedChart data={enriched}>\n          <CartesianGrid strokeDasharray=\"3 3\" stroke=\"#374151\" />\n          <XAxis dataKey=\"bucket\" stroke=\"#9CA3AF\" />\n          <YAxis stroke=\"#9CA3AF\" />\n          <Tooltip />\n          <Line type=\"monotone\" dataKey=\"avg_value\" stroke={color} dot={false} />\n          <Scatter dataKey=\"anomaly\" fill=\"#EF4444\" />\n        </ComposedChart>\n      </ResponsiveContainer>\n    </div>\n  );\n}",
            "why": "3.5'teki Scatter component'i anomali noktalar\u0131n\u0131 k\u0131rm\u0131z\u0131 (#EF4444) olarak g\u00f6steriyor. enriched array'de anomali olmayan noktalar\u0131n anomaly de\u011feri null \u2014 Scatter bunlar\u0131 atlar."
        },
        {
            "order": "3.7",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: components/AnomalyDetail.tsx \u2192 t\u0131klama detay\u0131 component'ini yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/AnomalyDetail.tsx",
            "code": "interface AnomalyDetailProps {\n  timestamp: string;\n  value: number;\n  score: number;\n  onClose: () => void;\n}\n\nexport function AnomalyDetail({ timestamp, value, score, onClose }: AnomalyDetailProps) {\n  return (\n    <div className=\"bg-gray-800 border border-red-500 rounded-lg p-4 mt-2\">\n      <div className=\"flex justify-between\">\n        <h4 className=\"text-red-400 font-bold\">Anomali Detay\u0131</h4>\n        <button onClick={onClose} className=\"text-gray-400 hover:text-white\">\u2715</button>\n      </div>\n      <p className=\"text-gray-300 text-sm mt-2\">Zaman: {timestamp}</p>\n      <p className=\"text-gray-300 text-sm\">De\u011fer: {value.toFixed(2)}</p>\n      <p className=\"text-gray-300 text-sm\">Anomali Skoru: {score.toFixed(4)}</p>\n    </div>\n  );\n}",
            "why": "Anomali noktas\u0131na t\u0131kland\u0131\u011f\u0131nda detay g\u00f6steren panel. M4.S2'deki detect endpoint'inden gelen verileri g\u00f6steriyor."
        },
        {
            "order": "3.8",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: pages/Dashboard.tsx \u2192 AnomalyChart'\u0131 import et ve kullan",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "import { AnomalyChart } from '../components/AnomalyChart';\nimport { useAnomalies } from '../hooks/useAnomalies';",
            "why": "3.1-3.7'de yazd\u0131\u011f\u0131m\u0131z anomali component'lerini dashboard'a ekliyoruz."
        },
        {
            "order": "3.9",
            "action": "Do\u011frulama: anomali noktalar\u0131 g\u00f6r\u00fcn\u00fcyor mu?",
            "type": "validate",
            "validation": "Chart'larda k\u0131rm\u0131z\u0131 noktalar (anomaliler) g\u00f6r\u00fcnmeli. Anomali say\u0131s\u0131 ba\u015fl\u0131kta yazmal\u0131. M2.S1'de seed'e ekledi\u011fimiz spike'lar yakalanm\u0131\u015f olmal\u0131.",
            "why": "3.6'daki Scatter component'inin ve 3.3'teki useAnomalies hook'unun birlikte \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 kan\u0131tl\u0131yoruz."
        }
    ]

    # M4.S4: Model Performans De\u011ferlendirme
    data["milestones"][3]["steps"][3]["substeps"] = [
        {
            "order": "4.1",
            "action": "DOSYA A\u00c7: ml-service/evaluation.py \u2192 de\u011ferlendirme \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/ml-service/evaluation.py",
            "code": "def evaluate_model(predictions, labels):\n    return {\"precision\": 0, \"recall\": 0, \"f1\": 0}",
            "why": "ML modelinin ne kadar iyi \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 \u00f6l\u00e7meden production'a almak tehlikeli. \u00d6nce fonksiyon iskeleti."
        },
        {
            "order": "4.2",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 sklearn metrics import'unu ekle",
            "type": "code_write",
            "file": "packages/ml-service/evaluation.py",
            "code": "from sklearn.metrics import (\n    precision_score, recall_score, f1_score,\n    confusion_matrix, classification_report\n)\nimport numpy as np",
            "why": "4.1'deki iskelet haz\u0131r, \u015fimdi ger\u00e7ek metrikleri hesaplayaca\u011f\u0131z."
        },
        {
            "order": "4.3",
            "action": "Fonksiyona GER\u0130 D\u00d6N \u2192 ger\u00e7ek de\u011ferlendirme hesaplamalar\u0131n\u0131 yaz",
            "type": "code_write",
            "file": "packages/ml-service/evaluation.py",
            "code": "def evaluate_model(\n    predictions: list[bool],\n    labels: list[bool]\n) -> dict:\n    y_pred = np.array(predictions, dtype=int)\n    y_true = np.array(labels, dtype=int)\n    return {\n        \"precision\": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),\n        \"recall\": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),\n        \"f1\": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),\n        \"confusion_matrix\": confusion_matrix(y_true, y_pred).tolist(),\n        \"report\": classification_report(y_true, y_pred, output_dict=True)\n    }",
            "why": "4.2'de import etti\u011fimiz metrikleri kullan\u0131yoruz. precision y\u00fcksek = az false alarm. recall y\u00fcksek = \u00e7o\u011fu anomaliyi yakal\u0131yor. F1 ikisinin dengesi."
        },
        {
            "order": "4.4",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: main.py \u2192 evaluation endpoint'ini ekle",
            "type": "code_write",
            "file": "packages/ml-service/main.py",
            "code": "from evaluation import evaluate_model\n\n@app.post(\"/api/anomalies/evaluate\")\ndef evaluate(metric_name: str = \"cpu_usage\", hours: int = 168):\n    df = fetch_metrics(metric_name, hours)\n    features = extract_features(df)\n    results = forest_detector.predict(features)\n    labels = [abs(r[\"anomaly_score\"]) > 0.3 for r in results]\n    predictions = [r[\"is_anomaly\"] for r in results]\n    return evaluate_model(predictions, labels)",
            "why": "4.1-4.3'te yazd\u0131\u011f\u0131m\u0131z evaluate_model'\u0131 API endpoint'i olarak sunuyoruz."
        },
        {
            "order": "4.5",
            "action": "De\u011ferlendirme endpoint'ini test et",
            "type": "terminal",
            "command": "curl -X POST 'http://localhost:8001/api/anomalies/evaluate?metric_name=cpu_usage'",
            "expected_output": "precision, recall, f1 de\u011ferleri ve confusion_matrix",
            "why": "4.4'te yazd\u0131\u011f\u0131m\u0131z endpoint'in \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 do\u011fruluyoruz."
        },
        {
            "order": "4.6",
            "action": "Do\u011frulama: model performans\u0131 yeterli mi?",
            "type": "validate",
            "validation": "F1 score 0.7'nin \u00fczerinde olmal\u0131. Precision ve recall dengeli olmal\u0131. Confusion matrix'te false positive say\u0131s\u0131 toplam anomalinin %5'inden az olmal\u0131.",
            "why": "Projenin AI requirement'\u0131: false positive oran\u0131 < %5. Bu do\u011frulama ile modelin production'a haz\u0131r oldu\u011funu kan\u0131tl\u0131yoruz."
        }
    ]

    # ============================================================
    # MILESTONE 5: Export, Alert Sistemi ve Heatmap
    # ============================================================

    # M5.S1: CSV ve PDF Export
    data["milestones"][4]["steps"][0]["substeps"] = [
        {
            "order": "1.1",
            "action": "Export ba\u011f\u0131ml\u0131l\u0131klar\u0131n\u0131 kur",
            "type": "terminal",
            "command": "cd packages/dashboard && pnpm add papaparse jspdf html2canvas && pnpm add -D @types/papaparse",
            "expected_output": "dependencies: + papaparse + jspdf + html2canvas",
            "why": "papaparse CSV olu\u015fturma, jspdf PDF \u00fcretimi, html2canvas DOM'u canvas'a \u00e7evirme \u2014 bu \u00fc\u00e7l\u00fc export stack'inin standard\u0131."
        },
        {
            "order": "1.2",
            "action": "DOSYA A\u00c7: utils/export.ts \u2192 export fonksiyonu \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/utils/export.ts",
            "code": "export function exportToCSV(data: any[], filename: string) {\n  console.log('CSV export placeholder');\n}\n\nexport function exportToPDF(elementId: string, filename: string) {\n  console.log('PDF export placeholder');\n}",
            "why": "\u00d6nce iki fonksiyonun imzas\u0131n\u0131 belirliyoruz. CSV \u2192 veri array'ini dosyaya d\u00f6n\u00fc\u015ft\u00fcr. PDF \u2192 DOM elementini g\u00f6r\u00fcnt\u00fc olarak yakala ve PDF'e koy."
        },
        {
            "order": "1.3",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 papaparse import'unu ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/utils/export.ts",
            "code": "import Papa from 'papaparse';",
            "why": "1.2'deki iskelet haz\u0131r, \u015fimdi CSV fonksiyonunu implement edece\u011fiz."
        },
        {
            "order": "1.4",
            "action": "exportToCSV fonksiyonuna GER\u0130 D\u00d6N \u2192 ger\u00e7ek implementasyonu yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/utils/export.ts",
            "code": "export function exportToCSV(data: any[], filename: string) {\n  const csv = Papa.unparse(data);\n  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });\n  const url = URL.createObjectURL(blob);\n  const link = document.createElement('a');\n  link.href = url;\n  link.download = `${filename}.csv`;\n  link.click();\n  URL.revokeObjectURL(url);\n}",
            "why": "1.3'te import etti\u011fimiz Papa.unparse data array'ini CSV string'e \u00e7evirir. Blob \u2192 URL \u2192 invisible link \u2192 click pattern'\u0131 browser'da dosya indirmenin standart yolu."
        },
        {
            "order": "1.5",
            "action": "exportToPDF fonksiyonunun \u00dcST\u00dcNE \u2192 jspdf ve html2canvas import'lar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/utils/export.ts",
            "code": "import Papa from 'papaparse';\nimport jsPDF from 'jspdf';\nimport html2canvas from 'html2canvas';",
            "why": "PDF export i\u00e7in iki k\u00fct\u00fcphane birlikte \u00e7al\u0131\u015f\u0131yor: html2canvas DOM'u g\u00f6r\u00fcnt\u00fcye \u00e7evirir, jsPDF g\u00f6r\u00fcnt\u00fcy\u00fc PDF'e koyar."
        },
        {
            "order": "1.6",
            "action": "exportToPDF fonksiyonuna GER\u0130 D\u00d6N \u2192 ger\u00e7ek implementasyonu yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/utils/export.ts",
            "code": "export async function exportToPDF(elementId: string, filename: string) {\n  const element = document.getElementById(elementId);\n  if (!element) return;\n  const canvas = await html2canvas(element, {\n    backgroundColor: '#111827', scale: 2\n  });\n  const imgData = canvas.toDataURL('image/png');\n  const pdf = new jsPDF('l', 'mm', 'a4');\n  const width = pdf.internal.pageSize.getWidth();\n  const height = (canvas.height * width) / canvas.width;\n  pdf.addImage(imgData, 'PNG', 0, 0, width, height);\n  pdf.save(`${filename}.pdf`);\n}",
            "why": "1.5'te import etti\u011fimiz k\u00fct\u00fcphaneleri kullan\u0131yoruz. backgroundColor dark tema rengi. scale: 2 retina kalitesi. 'l' landscape y\u00f6nlendirme."
        },
        {
            "order": "1.7",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: pages/Dashboard.tsx \u2192 export butonlar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "import { exportToCSV, exportToPDF } from '../utils/export';",
            "why": "1.2-1.6'da yazd\u0131\u011f\u0131m\u0131z export fonksiyonlar\u0131n\u0131 dashboard'a ekliyoruz."
        },
        {
            "order": "1.8",
            "action": "Dashboard header'a \u2192 CSV ve PDF butonlar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "        <div className=\"flex gap-2\">\n          <button\n            onClick={() => exportToCSV(cpu.data, 'cpu-metrics')}\n            className=\"px-3 py-1 bg-emerald-600 text-white rounded text-sm\">\n            CSV \u0130ndir\n          </button>\n          <button\n            onClick={() => exportToPDF('dashboard-charts', 'dashboard-report')}\n            className=\"px-3 py-1 bg-blue-600 text-white rounded text-sm\">\n            PDF \u0130ndir\n          </button>\n        </div>",
            "why": "1.4'teki exportToCSV cpu verisiyle, 1.6'daki exportToPDF dashboard-charts ID'li element ile \u00e7al\u0131\u015f\u0131yor."
        },
        {
            "order": "1.9",
            "action": "Do\u011frulama: CSV ve PDF indirme \u00e7al\u0131\u015f\u0131yor mu?",
            "type": "validate",
            "validation": "CSV butonuna t\u0131klay\u0131nca .csv dosyas\u0131 inmeli \u2014 dosyay\u0131 a\u00e7\u0131nca bucket ve avg_value s\u00fctunlar\u0131 g\u00f6r\u00fcnmeli. PDF butonuna t\u0131klay\u0131nca .pdf dosyas\u0131 inmeli.",
            "why": "1.4 ve 1.6'daki implementasyonlar\u0131n taray\u0131c\u0131da ger\u00e7ekten dosya indirdi\u011fini kan\u0131tl\u0131yoruz."
        }
    ]

    # M5.S2: Heatmap Vizualizasyonu
    data["milestones"][4]["steps"][1]["substeps"] = [
        {
            "order": "2.1",
            "action": "DOSYA A\u00c7: hooks/useHeatmap.ts \u2192 heatmap veri hook \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useHeatmap.ts",
            "code": "export function useHeatmap() {\n  return { data: [], loading: true };\n}",
            "why": "Heatmap g\u00fcn-saat baz\u0131nda veri g\u00f6sterecek. \u00d6nce hook iskeleti."
        },
        {
            "order": "2.2",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 React import'lar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useHeatmap.ts",
            "code": "import { useState, useEffect } from 'react';",
            "why": "2.1'deki iskelet haz\u0131r, state y\u00f6netimi ve veri \u00e7ekme i\u00e7in hook'lar laz\u0131m."
        },
        {
            "order": "2.3",
            "action": "Fonksiyona GER\u0130 D\u00d6N \u2192 heatmap veri \u00e7ekme ve d\u00f6n\u00fc\u015ft\u00fcrme logic'ini yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/hooks/useHeatmap.ts",
            "code": "interface HeatmapCell {\n  day: number; hour: number;\n  value: number; label: string;\n}\n\nexport function useHeatmap(metric: string, source: string) {\n  const [data, setData] = useState<HeatmapCell[]>([]);\n  const [loading, setLoading] = useState(true);\n\n  useEffect(() => {\n    const from = new Date(Date.now() - 7 * 86400000).toISOString();\n    const to = new Date().toISOString();\n    fetch(`/api/metrics?source=${source}&metric=${metric}&from=${from}&to=${to}&interval=1h`)\n      .then(res => res.json())\n      .then(rows => {\n        const cells = rows.map((r: any) => {\n          const d = new Date(r.bucket);\n          return {\n            day: d.getDay(), hour: d.getHours(),\n            value: r.avg_value,\n            label: ['Paz','Pzt','Sal','\u00c7ar','Per','Cum','Cmt'][d.getDay()]\n          };\n        });\n        setData(cells);\n        setLoading(false);\n      });\n  }, [metric, source]);\n\n  return { data, loading };\n}",
            "why": "2.2'de import etti\u011fimiz hook'larla API'den son 7 g\u00fcnl\u00fck veriyi \u00e7ekip g\u00fcn-saat matrisine d\u00f6n\u00fc\u015ft\u00fcr\u00fcyoruz. T\u00fcrk\u00e7e g\u00fcn isimleri kullan\u0131yoruz."
        },
        {
            "order": "2.4",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: components/Heatmap.tsx \u2192 \u0130SKELET yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/Heatmap.tsx",
            "code": "export function Heatmap() {\n  return (\n    <div className=\"bg-gray-800 rounded-lg p-4\">\n      <p className=\"text-gray-400\">Heatmap placeholder</p>\n    </div>\n  );\n}",
            "why": "7x24 grid ile saat baz\u0131nda pattern'lar\u0131 g\u00f6steren heatmap. GitHub'\u0131n contribution graph'\u0131 gibi \u2014 \u00f6nce iskelet."
        },
        {
            "order": "2.5",
            "action": "Fonksiyona GER\u0130 D\u00d6N \u2192 props ve heatmap grid'ini yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/Heatmap.tsx",
            "code": "interface HeatmapProps {\n  data: Array<{ day: number; hour: number; value: number; label: string }>;\n  title: string;\n}\n\nfunction getColor(value: number, max: number): string {\n  const intensity = Math.min(value / max, 1);\n  const r = Math.round(16 + intensity * 223);\n  const g = Math.round(185 - intensity * 150);\n  return `rgb(${r}, ${g}, 60)`;\n}\n\nexport function Heatmap({ data, title }: HeatmapProps) {\n  const max = Math.max(...data.map(d => d.value), 1);\n  const days = ['Paz', 'Pzt', 'Sal', '\u00c7ar', 'Per', 'Cum', 'Cmt'];\n\n  return (\n    <div className=\"bg-gray-800 rounded-lg p-4\">\n      <h3 className=\"text-sm text-gray-300 mb-3\">{title}</h3>\n      <div className=\"grid gap-1\"\n        style={{ gridTemplateColumns: 'auto repeat(24, 1fr)' }}>\n        {days.map((day, di) => (\n          <div key={di} className=\"contents\">\n            <span className=\"text-xs text-gray-400 pr-2\">{day}</span>\n            {Array.from({ length: 24 }, (_, h) => {\n              const cell = data.find(d => d.day === di && d.hour === h);\n              return (\n                <div key={`${di}-${h}`}\n                  className=\"w-4 h-4 rounded-sm cursor-pointer\"\n                  style={{ backgroundColor: cell\n                    ? getColor(cell.value, max) : '#374151' }}\n                  title={cell\n                    ? `${day} ${h}:00 - ${cell.value.toFixed(1)}`\n                    : 'Veri yok'}\n                />\n              );\n            })}\n          </div>\n        ))}\n      </div>\n    </div>\n  );\n}",
            "why": "getColor fonksiyonu de\u011fer yo\u011funlu\u011funa g\u00f6re ye\u015filden k\u0131rm\u0131z\u0131ya renk \u00fcretir. 7 g\u00fcn x 24 saat = 168 h\u00fccre. Hover'da tooltip ile de\u011fer g\u00f6steriliyor."
        },
        {
            "order": "2.6",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: pages/Dashboard.tsx \u2192 Heatmap'i import et ve kullan",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "import { Heatmap } from '../components/Heatmap';\nimport { useHeatmap } from '../hooks/useHeatmap';",
            "why": "2.1-2.5'te yazd\u0131\u011f\u0131m\u0131z heatmap component ve hook'unu dashboard'a ekliyoruz."
        },
        {
            "order": "2.7",
            "action": "Dashboard'a heatmap section ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "      <div className=\"mt-6\">\n        <Heatmap data={heatmapData.data}\n          title=\"CPU Kullan\u0131m\u0131 - Haftal\u0131k Pattern\" />\n      </div>",
            "why": "2.6'da import etti\u011fimiz component'i kullan\u0131yoruz. Heatmap chart'lar\u0131n alt\u0131nda ayr\u0131 bir section olarak duracak."
        },
        {
            "order": "2.8",
            "action": "Do\u011frulama: heatmap g\u00f6rsel kontrol\u00fc",
            "type": "validate",
            "validation": "7 g\u00fcn x 24 saat grid do\u011fru render olmal\u0131. Renk yo\u011funlu\u011fu veriyle uyumlu olmal\u0131 (g\u00fcnd\u00fcz saatleri daha yo\u011fun). Hover'da tooltip ile de\u011fer g\u00f6r\u00fcnmeli. T\u00fcrk\u00e7e g\u00fcn isimleri do\u011fru olmal\u0131.",
            "why": "2.5'teki getColor fonksiyonu ve grid layout'unun do\u011fru \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 kan\u0131tl\u0131yoruz."
        }
    ]

    # ============================================================
    # MILESTONE 6: Docker, Test ve Production Haz\u0131rl\u0131k
    # ============================================================

    # M6.S1: Docker Compose Setup
    data["milestones"][5]["steps"][0]["substeps"] = [
        {
            "order": "1.1",
            "action": "DOSYA A\u00c7: docker-compose.yml \u2192 \u0130SKELET servis tan\u0131mlar\u0131n\u0131 yaz",
            "type": "code_write",
            "file": "docker-compose.yml",
            "code": "version: '3.8'\nservices:\n  postgres:\n    image: postgres:16-alpine\n    ports:\n      - '5432:5432'\n    environment:\n      POSTGRES_DB: analytics_dashboard\n      POSTGRES_PASSWORD: postgres",
            "why": "\u00d6nce en basit servis \u2014 PostgreSQL. Docker Compose 4 servisi bir araya getirecek ama \u00f6nce birer birer ekliyoruz."
        },
        {
            "order": "1.2",
            "action": "Ayn\u0131 dosyaya \u2192 Redis ve volume tan\u0131m\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "docker-compose.yml",
            "code": "  redis:\n    image: redis:7-alpine\n    ports:\n      - '6379:6379'\n\nvolumes:\n  pgdata:",
            "why": "1.1'deki PostgreSQL'e Redis ekliyoruz. Volume tan\u0131m\u0131 PostgreSQL verilerinin container silinse bile kaybolmamas\u0131n\u0131 sa\u011flar."
        },
        {
            "order": "1.3",
            "action": "PostgreSQL servisine \u2192 volume ve healthcheck ekle",
            "type": "code_write",
            "file": "docker-compose.yml",
            "code": "    volumes:\n      - pgdata:/var/lib/postgresql/data\n    healthcheck:\n      test: ['CMD-SHELL', 'pg_isready -U postgres']\n      interval: 5s\n      timeout: 5s\n      retries: 5",
            "why": "1.2'deki volume'\u00fc PostgreSQL'e ba\u011fl\u0131yoruz. Healthcheck ZORUNLU \u2014 depends_on tek ba\u015f\u0131na yetmez."
        },
        {
            "order": "1.4",
            "action": "BA\u015eKA DOSYA A\u00c7: packages/api/Dockerfile \u2192 API Dockerfile'\u0131n\u0131 yaz",
            "type": "code_write",
            "file": "packages/api/Dockerfile",
            "code": "FROM node:20-alpine\nWORKDIR /app\nCOPY package.json pnpm-lock.yaml ./\nRUN npm install -g pnpm && pnpm install --frozen-lockfile\nCOPY . .\nRUN pnpm build\nEXPOSE 4000\nCMD [\"node\", \"dist/index.js\"]",
            "why": "--frozen-lockfile ile lock dosyas\u0131n\u0131 de\u011fi\u015ftirmeden kurulum yapar \u2014 CI/CD g\u00fcvenli\u011fi."
        },
        {
            "order": "1.5",
            "action": "BA\u015eKA DOSYA A\u00c7: packages/dashboard/Dockerfile \u2192 Dashboard Dockerfile'\u0131n\u0131 yaz",
            "type": "code_write",
            "file": "packages/dashboard/Dockerfile",
            "code": "FROM node:20-alpine AS build\nWORKDIR /app\nCOPY package.json pnpm-lock.yaml ./\nRUN npm install -g pnpm && pnpm install --frozen-lockfile\nCOPY . .\nRUN pnpm build\n\nFROM nginx:alpine\nCOPY --from=build /app/dist /usr/share/nginx/html\nEXPOSE 80\nCMD [\"nginx\", \"-g\", \"daemon off;\"]",
            "why": "Frontend i\u00e7in multi-stage build \u015eART \u2014 build stage'de derle, production stage'de sadece Nginx ile sun. Final image ~25MB."
        },
        {
            "order": "1.6",
            "action": "BA\u015eKA DOSYA A\u00c7: packages/ml-service/Dockerfile \u2192 ML service Dockerfile'\u0131n\u0131 yaz",
            "type": "code_write",
            "file": "packages/ml-service/Dockerfile",
            "code": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nEXPOSE 8001\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8001\"]",
            "why": "python:3.11-slim light image. --no-cache-dir pip cache'ini temizler. --host 0.0.0.0 container d\u0131\u015f\u0131ndan eri\u015fim i\u00e7in ZORUNLU."
        },
        {
            "order": "1.7",
            "action": "docker-compose.yml'e GER\u0130 D\u00d6N \u2192 API, dashboard ve ML service'lerini ekle",
            "type": "code_write",
            "file": "docker-compose.yml",
            "code": "  api:\n    build: ./packages/api\n    ports:\n      - '4000:4000'\n    environment:\n      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/analytics_dashboard\n      REDIS_URL: redis://redis:6379\n    depends_on:\n      postgres:\n        condition: service_healthy\n      redis:\n        condition: service_started\n\n  dashboard:\n    build: ./packages/dashboard\n    ports:\n      - '80:80'\n    depends_on:\n      - api\n\n  ml-service:\n    build: ./packages/ml-service\n    ports:\n      - '8001:8001'\n    environment:\n      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/analytics_dashboard\n    depends_on:\n      postgres:\n        condition: service_healthy",
            "why": "1.4-1.6'da yazd\u0131\u011f\u0131m\u0131z Dockerfile'lar\u0131 docker-compose'a ba\u011fl\u0131yoruz. Container i\u00e7inde hostname olarak servis ad\u0131n\u0131 kullan\u0131yoruz."
        },
        {
            "order": "1.8",
            "action": "Docker Compose'u ba\u015flat",
            "type": "terminal",
            "command": "docker-compose up --build -d",
            "expected_output": "Creating ... done t\u00fcm servisler i\u00e7in",
            "why": "1.1-1.7'de yazd\u0131\u011f\u0131m\u0131z t\u00fcm konfig\u00fcrasyonu test ediyoruz. --build image'lar\u0131 yeniden derler."
        },
        {
            "order": "1.9",
            "action": "T\u00fcm servislerin \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 do\u011frula",
            "type": "terminal",
            "command": "docker-compose ps && curl http://localhost:4000/health && curl http://localhost:8001/health",
            "expected_output": "4 servis Up durumunda. Her iki health endpoint {\"status\":\"ok\"} d\u00f6nmeli.",
            "why": "1.8'de ba\u015flatt\u0131\u011f\u0131m\u0131z servislerin hepsinin sa\u011fl\u0131kl\u0131 \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 do\u011fruluyoruz."
        },
        {
            "order": "1.10",
            "action": "Do\u011frulama: container'lar aras\u0131 ileti\u015fim",
            "type": "validate",
            "validation": "docker-compose ps ile t\u00fcm servisler Up olmal\u0131. http://localhost:80 adresinde dashboard a\u00e7\u0131lmal\u0131. docker-compose logs ile hata olmamal\u0131.",
            "why": "T\u00fcm servislerin Docker i\u00e7inde birbirleriyle ileti\u015fim kurabildi\u011fini kan\u0131tl\u0131yoruz."
        }
    ]

    # M6.S2: Performance Optimization
    data["milestones"][5]["steps"][1]["substeps"] = [
        {
            "order": "2.1",
            "action": "DOSYA A\u00c7: components/LazyChart.tsx \u2192 lazy loading \u0130SKELET\u0130N\u0130 yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/LazyChart.tsx",
            "code": "export function LazyChart({ children }: { children: React.ReactNode }) {\n  return <div>{children}</div>;\n}",
            "why": "Ekran\u0131n alt\u0131ndaki chart'lar\u0131 hemen render etmek gereksiz \u2014 IntersectionObserver ile sadece g\u00f6r\u00fcnen chart'lar\u0131 render edece\u011fiz."
        },
        {
            "order": "2.2",
            "action": "Dosyan\u0131n \u00dcST\u00dcNE \u00c7IK \u2192 React import'lar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "packages/dashboard/src/components/LazyChart.tsx",
            "code": "import { useRef, useState, useEffect, ReactNode } from 'react';",
            "why": "2.1'deki iskelet haz\u0131r, IntersectionObserver ile lazy loading implement edece\u011fiz."
        },
        {
            "order": "2.3",
            "action": "Fonksiyona GER\u0130 D\u00d6N \u2192 IntersectionObserver logic'ini yaz",
            "type": "code_write",
            "file": "packages/dashboard/src/components/LazyChart.tsx",
            "code": "export function LazyChart({ children }: { children: ReactNode }) {\n  const ref = useRef<HTMLDivElement>(null);\n  const [isVisible, setIsVisible] = useState(false);\n\n  useEffect(() => {\n    const observer = new IntersectionObserver(\n      ([entry]) => {\n        if (entry.isIntersecting) {\n          setIsVisible(true);\n          observer.disconnect();\n        }\n      },\n      { threshold: 0.1 }\n    );\n    if (ref.current) observer.observe(ref.current);\n    return () => observer.disconnect();\n  }, []);\n\n  return (\n    <div ref={ref} className=\"min-h-[200px]\">\n      {isVisible ? children : (\n        <div className=\"h-[200px] bg-gray-800 rounded-lg animate-pulse\" />\n      )}\n    </div>\n  );\n}",
            "why": "2.2'de import etti\u011fimiz hook'larla IntersectionObserver pattern'\u0131. threshold: 0.1 \u2192 element %10 g\u00f6r\u00fcn\u00fcr oldu\u011funda tetikle. animate-pulse y\u00fckleme animasyonu."
        },
        {
            "order": "2.4",
            "action": "BA\u015eKA DOSYAYA GE\u00c7: pages/Dashboard.tsx \u2192 React.memo ile gereksiz re-render'\u0131 \u00f6nle",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "import { LazyChart } from '../components/LazyChart';\nimport React from 'react';\n\nconst MemoizedChart = React.memo(AdvancedChart);",
            "why": "2.1-2.3'te yazd\u0131\u011f\u0131m\u0131z LazyChart'\u0131 ve React.memo'yu ekliyoruz. memo ile props de\u011fi\u015fmedi\u011finde chart re-render olmaz."
        },
        {
            "order": "2.5",
            "action": "Dashboard'daki chart'lar\u0131 LazyChart ile sar",
            "type": "code_write",
            "file": "packages/dashboard/src/pages/Dashboard.tsx",
            "code": "        <LazyChart>\n          <MemoizedChart title=\"CPU Kullan\u0131m\u0131\" data={cpu.data}\n            color=\"#8884d8\" threshold={80} />\n        </LazyChart>\n        <LazyChart>\n          <MemoizedChart title=\"Bellek\" data={mem.data}\n            color=\"#82ca9d\" threshold={90} />\n        </LazyChart>",
            "why": "2.3'teki LazyChart ve 2.4'teki MemoizedChart birlikte \u00e7al\u0131\u015f\u0131yor. Ekranda olmayan chart'lar render edilmez."
        },
        {
            "order": "2.6",
            "action": "Vite config'e \u2192 bundle splitting ekle",
            "type": "code_write",
            "file": "packages/dashboard/vite.config.ts",
            "code": "import { defineConfig } from 'vite';\nimport react from '@vitejs/plugin-react';\n\nexport default defineConfig({\n  plugins: [react()],\n  build: {\n    rollupOptions: {\n      output: {\n        manualChunks: {\n          vendor: ['react', 'react-dom'],\n          charts: ['recharts'],\n        }\n      }\n    }\n  }\n});",
            "why": "manualChunks ile b\u00fcy\u00fck k\u00fct\u00fcphaneleri ayr\u0131 dosyalara b\u00f6l\u00fcyoruz. Recharts ~300KB \u2014 ana bundle'dan ayr\u0131l\u0131nca ilk y\u00fckleme h\u0131zlan\u0131r."
        },
        {
            "order": "2.7",
            "action": "Bundle boyutunu analiz et",
            "type": "terminal",
            "command": "cd packages/dashboard && pnpm build && ls -la dist/assets/",
            "expected_output": "vendor chunk, charts chunk ve main chunk ayr\u0131 dosyalar olarak g\u00f6r\u00fcnmeli",
            "why": "2.6'da yapt\u0131\u011f\u0131m\u0131z chunk splitting'in \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 dosya boyutlar\u0131yla do\u011fruluyoruz."
        },
        {
            "order": "2.8",
            "action": "Do\u011frulama: Lighthouse performance audit",
            "type": "validate",
            "validation": "Chrome DevTools \u2192 Lighthouse \u2192 Performance audit. Skor 80+ olmal\u0131. \u0130lk y\u00fcklemede sadece g\u00f6r\u00fcnen chart'lar render olmal\u0131. React DevTools Profiler'da gereksiz re-render olmamal\u0131.",
            "why": "2.3'teki lazy loading, 2.4'teki memo ve 2.6'daki chunk splitting'in hep birlikte performans\u0131 art\u0131rd\u0131\u011f\u0131n\u0131 kan\u0131tl\u0131yoruz."
        }
    ]

    # ============================================================
    # MILESTONE 7: Deployment ve Portfolio Showcase
    # ============================================================

    # M7.S1: Production Build
    data["milestones"][6]["steps"][0]["substeps"] = [
        {
            "order": "1.1",
            "action": "TypeScript hata kontrol\u00fc \u00e7al\u0131\u015ft\u0131r",
            "type": "terminal",
            "command": "cd packages/api && npx tsc --noEmit && cd ../dashboard && npx tsc --noEmit",
            "expected_output": "Hata yok \u2014 \u00e7\u0131kt\u0131 bo\u015f olmal\u0131",
            "why": "Production build'den \u00f6nce tip hatalar\u0131n\u0131 yakal\u0131yoruz. --noEmit sadece kontrol yapar, dosya \u00fcretmez."
        },
        {
            "order": "1.2",
            "action": "API build'ini \u00e7al\u0131\u015ft\u0131r",
            "type": "terminal",
            "command": "cd packages/api && pnpm build",
            "expected_output": "dist/ dizininde compiled JS dosyalar\u0131 olu\u015fmal\u0131",
            "why": "TypeScript'i JavaScript'e derliyoruz. Production'da ts-node yerine derlenmi\u015f JS \u00e7al\u0131\u015f\u0131r \u2014 5x daha h\u0131zl\u0131 ba\u015flar."
        },
        {
            "order": "1.3",
            "action": "Dashboard build'ini \u00e7al\u0131\u015ft\u0131r",
            "type": "terminal",
            "command": "cd packages/dashboard && pnpm build",
            "expected_output": "dist/ dizininde index.html ve assets/ klas\u00f6r\u00fc olu\u015fmal\u0131",
            "why": "Vite production build: minification, tree shaking, asset optimization. M6.S2'deki chunk splitting de burada devreye girer."
        },
        {
            "order": "1.4",
            "action": "Build \u00e7\u0131kt\u0131lar\u0131n\u0131 kontrol et",
            "type": "terminal",
            "command": "ls -la packages/api/dist/ && ls -la packages/dashboard/dist/assets/",
            "expected_output": "API: JS dosyalar\u0131. Dashboard: JS/CSS chunk'lar\u0131",
            "why": "1.2 ve 1.3'teki build'lerin ba\u015far\u0131l\u0131 oldu\u011funu dosya listesiyle do\u011fruluyoruz."
        },
        {
            "order": "1.5",
            "action": "Production modda test et",
            "type": "terminal",
            "command": "cd packages/api && NODE_ENV=production node dist/index.js",
            "expected_output": "API: port 4000 (production)",
            "why": "Derlenmi\u015f kodun ger\u00e7ekten \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 do\u011fruluyoruz."
        },
        {
            "order": "1.6",
            "action": "Do\u011frulama: production build tam \u00e7al\u0131\u015f\u0131yor",
            "type": "validate",
            "validation": "API health endpoint \u00e7al\u0131\u015fmal\u0131. Dashboard statik dosyalar\u0131 bir HTTP server ile servis edildi\u011finde a\u00e7\u0131lmal\u0131. T\u00fcm \u00f6zellikler production build'de de \u00e7al\u0131\u015fmal\u0131.",
            "why": "Development'ta \u00e7al\u0131\u015f\u0131p production'da \u00e7al\u0131\u015fmayan kod en tehlikeli hata t\u00fcr\u00fc. \u015eimdi kan\u0131tla, deploy'da s\u00fcrpriz ya\u015fama."
        }
    ]

    # M7.S2: Deploy
    data["milestones"][6]["steps"][1]["substeps"] = [
        {
            "order": "2.1",
            "action": ".dockerignore dosyas\u0131n\u0131 olu\u015ftur",
            "type": "code_write",
            "file": ".dockerignore",
            "code": "node_modules\ndist\n.env\n*.log\n.git",
            "why": "Docker build context'ine gereksiz dosyalar\u0131 eklememek build s\u00fcresini ve image boyutunu k\u00fc\u00e7\u00fclt\u00fcr."
        },
        {
            "order": "2.2",
            "action": "Docker image'lar\u0131n\u0131 build et",
            "type": "terminal",
            "command": "docker-compose build",
            "expected_output": "Successfully built ... t\u00fcm servisler i\u00e7in",
            "why": "M6.S1'de yazd\u0131\u011f\u0131m\u0131z Dockerfile'lar ile production image'lar\u0131n\u0131 olu\u015fturuyoruz."
        },
        {
            "order": "2.3",
            "action": "Production ortam\u0131n\u0131 docker-compose ile ba\u015flat",
            "type": "terminal",
            "command": "docker-compose up -d",
            "expected_output": "T\u00fcm container'lar Up durumunda",
            "why": "2.2'de build etti\u011fimiz image'lar\u0131 \u00e7al\u0131\u015ft\u0131r\u0131yoruz. -d detached modda arka planda \u00e7al\u0131\u015f\u0131r."
        },
        {
            "order": "2.4",
            "action": "Health check'leri \u00e7al\u0131\u015ft\u0131r",
            "type": "terminal",
            "command": "curl http://localhost:4000/health && curl http://localhost:8001/health && curl -s http://localhost:80 | head -5",
            "expected_output": "API: {status: ok}, ML: {status: ok}, Dashboard: HTML d\u00f6nd\u00fcrmeli",
            "why": "2.3'te ba\u015flatt\u0131\u011f\u0131m\u0131z t\u00fcm servislerin sa\u011fl\u0131kl\u0131 \u00e7al\u0131\u015ft\u0131\u011f\u0131n\u0131 do\u011fruluyoruz."
        },
        {
            "order": "2.5",
            "action": "Seed verilerini production DB'ye ekle",
            "type": "terminal",
            "command": "docker-compose exec api pnpm run seed",
            "expected_output": "Seeded metrics",
            "why": "Production veritaban\u0131 bo\u015f \u2014 M2.S1'deki seed script'ini container i\u00e7inde \u00e7al\u0131\u015ft\u0131rarak demo verisi ekliyoruz."
        },
        {
            "order": "2.6",
            "action": "Do\u011frulama: tam end-to-end test",
            "type": "validate",
            "validation": "http://localhost:80 adresinde dashboard a\u00e7\u0131lmal\u0131. Chart'lar veri g\u00f6stermeli. Filtreler \u00e7al\u0131\u015fmal\u0131. Export butonlar\u0131 dosya indirmeli. Anomali noktalar\u0131 g\u00f6r\u00fcnmeli.",
            "why": "Deployment'\u0131n ba\u015far\u0131l\u0131 oldu\u011funu t\u00fcm \u00f6zellikleri test ederek kan\u0131tl\u0131yoruz."
        }
    ]

    # M7.S3: Profesyonel README
    data["milestones"][6]["steps"][2]["substeps"] = [
        {
            "order": "3.1",
            "action": "Screenshot dizinini olu\u015ftur",
            "type": "terminal",
            "command": "mkdir -p docs/screenshots",
            "expected_output": "Dizin olu\u015fturuldu",
            "why": "README'deki g\u00f6rseller projeyi portfolio'da \u00f6ne \u00e7\u0131kar\u0131r. Recruiter'lar kodu okumaz, g\u00f6rsel etkiye bakar."
        },
        {
            "order": "3.2",
            "action": "DOSYA A\u00c7: README.md \u2192 proje tan\u0131t\u0131m\u0131n\u0131 yaz",
            "type": "code_write",
            "file": "README.md",
            "code": "# Analytics Dashboard + AI Anomaly Detection\n\nGer\u00e7ek zamanl\u0131 veri g\u00f6rselle\u015ftirme ve ML tabanl\u0131 anomali tespiti yapan profesyonel analytics dashboard.\n\n## \u00d6zellikler\n- \u0130nteraktif line/area/bar chart'lar (Recharts)\n- Redis cache ile < 5ms response time\n- Isolation Forest anomali tespiti\n- CSV ve PDF export\n- Docker Compose ile tek komut deployment",
            "why": "README projenin vitrini. \u0130lk 5 sat\u0131rda ne yapt\u0131\u011f\u0131n\u0131, hangi teknolojileri kulland\u0131\u011f\u0131n\u0131 ve neden \u00f6nemli oldu\u011funu anlatmal\u0131."
        },
        {
            "order": "3.3",
            "action": "README'ye \u2192 kurulum ve kullan\u0131m talimatlar\u0131n\u0131 ekle",
            "type": "code_write",
            "file": "README.md",
            "code": "## H\u0131zl\u0131 Ba\u015flang\u0131\u00e7\n\n```bash\ngit clone <repo-url>\ncd analytics-dashboard\ndocker-compose up --build -d\n```\n\nDashboard: http://localhost:80\nAPI: http://localhost:4000\nML Service: http://localhost:8001/docs\n\n## Tech Stack\n- **Frontend**: React, TypeScript, Recharts\n- **Backend**: Express, PostgreSQL, Redis\n- **ML**: FastAPI, scikit-learn (Isolation Forest)\n- **DevOps**: Docker Compose",
            "why": "3 komutla \u00e7al\u0131\u015ft\u0131r\u0131labilir proje \u2014 recruiter veya ba\u015fka developer deneyebilsin."
        },
        {
            "order": "3.4",
            "action": "Do\u011frulama: README tam ve profesyonel",
            "type": "validate",
            "validation": "README.md'de proje a\u00e7\u0131klamas\u0131, \u00f6zellik listesi, kurulum talimatlar\u0131 ve tech stack b\u00f6l\u00fcmleri olmal\u0131. Markdown format\u0131 do\u011fru render olmal\u0131.",
            "why": "Portfolio projelerinde README kalitesi de\u011ferlendirme kriterlerinden biri."
        }
    ]

    # M7.S4: Demo Video (Opsiyonel)
    data["milestones"][6]["steps"][3]["substeps"] = [
        {
            "order": "4.1",
            "action": "Demo senaryosunu planla",
            "type": "code_write",
            "file": "docs/demo-script.md",
            "code": "# Demo Senaryo\n1. Dashboard a\u00e7\u0131l\u0131\u015f\u0131 ve genel bak\u0131\u015f (10sn)\n2. Tarih filtresi de\u011fi\u015ftir (5sn)\n3. Kaynak filtresi ile kar\u015f\u0131la\u015ft\u0131r (5sn)\n4. Brush ile zoom (5sn)\n5. Anomali noktas\u0131na t\u0131kla (5sn)\n6. CSV export (5sn)\n7. Heatmap inceleme (5sn)",
            "why": "Demo video 30-45 saniye olmal\u0131. Senaryo olmadan \u00e7ekim yap\u0131l\u0131rsa da\u011f\u0131n\u0131k olur."
        },
        {
            "order": "4.2",
            "action": "Ekran kayd\u0131 al",
            "type": "validate",
            "validation": "OBS Studio veya Chrome Screen Recorder ile 4.1'deki senaryoyu kaydet. 1080p \u00e7\u00f6z\u00fcn\u00fcrl\u00fck, 30fps yeterli. Dosya boyutu 10MB alt\u0131nda olmal\u0131.",
            "why": "GIF yerine MP4 tercih et \u2014 daha k\u00fc\u00e7\u00fck dosya boyutu, daha iyi kalite."
        },
        {
            "order": "4.3",
            "action": "Demo thumbnail'\u0131 olu\u015ftur",
            "type": "terminal",
            "command": "echo 'Dashboard ekran g\u00f6r\u00fcnt\u00fcs\u00fcn\u00fc docs/demo-thumbnail.png olarak kaydet'",
            "expected_output": "Thumbnail kaydedildi",
            "why": "Video \u00f6nizlemesi README'de t\u0131klanabilir bir g\u00f6r\u00fcnt\u00fc olarak g\u00f6r\u00fcnecek."
        },
        {
            "order": "4.4",
            "action": "README'ye demo linkini ekle",
            "type": "code_write",
            "file": "README.md",
            "code": "## Demo\n[![Demo Video](docs/demo-thumbnail.png)](demo-video-link)",
            "why": "4.2'de \u00e7ekti\u011fimiz videoyu ve 4.3'teki thumbnail'\u0131 README'ye ekliyoruz."
        },
        {
            "order": "4.5",
            "action": "Do\u011frulama: demo materyalleri tam",
            "type": "validate",
            "validation": "docs/screenshots/ dizininde en az 3 ekran g\u00f6r\u00fcnt\u00fcs\u00fc olmal\u0131. Demo video (varsa) 30-45 saniye ve 10MB alt\u0131nda olmal\u0131. README'deki t\u00fcm g\u00f6rseller ve linkler \u00e7al\u0131\u015fmal\u0131.",
            "why": "Portfolio sunumunda g\u00f6rsel materyaller teknik becerilerden daha \u00e7ok dikkat \u00e7eker."
        }
    ]

    # Save the modified JSON
    with open("content/projects/project-05.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Rewrite complete!")

    # Validate
    with open("content/projects/project-05.json", "r", encoding="utf-8") as f:
        validated = json.load(f)

    total_substeps = 0
    for mi, m in enumerate(validated["milestones"]):
        for si, s in enumerate(m["steps"]):
            subs = s.get("substeps", [])
            total_substeps += len(subs)
            print(f"M{mi+1}.S{si+1}: {s['title']} -> {len(subs)} substeps")

    print(f"\nTotal substeps: {total_substeps}")
    print("JSON validation: OK")

if __name__ == "__main__":
    main()
