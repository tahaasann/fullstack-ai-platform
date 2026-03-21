---
id: "mod-02-python/lesson-01"
title: "Python Ortamı: Kurulum, Versiyon Yönetimi ve Modern Proje Yapısı"
description: "Python kurulumu, virtual environment, paket yöneticileri, pyproject.toml ve profesyonel proje yapısı"
estimated_minutes: 40
order: 1
tags: ["python", "venv", "uv", "pip", "poetry", "pyproject.toml", "virtual-environment"]
prerequisites: []
---

# Python Ortamı: Kurulum, Versiyon Yönetimi ve Modern Proje Yapısı

:::realworld
Python, 2026 itibarıyla dünyanın en çok kullanılan programlama dillerinden biri. AI/ML devriminin ana dili, backend geliştirmede FastAPI ile yükselişte, DevOps/scripting'de vazgeçilmez. Ama birçok geliştirici Python'u kurduğunda "hangi Python?", "pip mi poetry mi?", "neden virtual environment lazım?" sorularıyla boğuşuyor. Bu derste Python ortamını profesyonel seviyede kuracak, modern proje yapısını öğrenecek ve bir senior developer gibi environment yönetimi yapacaksın.
:::

## Python Nedir ve 2026'da Neden Önemli?

Python, 1991 yılında Guido van Rossum tarafından yaratılmış, okunabilirliği ön planda tutan, genel amaçlı bir programlama dilidir. 2026'da Python'un bu kadar güçlü olmasının somut nedenleri var:

- **AI/ML dominasyonu:** PyTorch, TensorFlow, scikit-learn, LangChain -- tüm AI ekosistemi Python üzerine kurulu
- **Backend geliştirme:** FastAPI ve Django ile yüksek performanslı API'ler
- **Veri bilimi:** pandas, NumPy, Jupyter -- veri dünyasının ana dili
- **Otomasyon ve scripting:** DevOps pipeline'ları, sistem yönetimi, web scraping
- **İş piyasası:** AI boom'u sayesinde Python developer talebi rekor seviyelerde

:::deha-tip
Deha seviyesi geliştiriciler bir dile "en iyi dil" demez, "bu problem için en uygun araç" der. Python'un gücü versatility'sidir: sabah bir ML modeli eğitir, öğleden sonra bir REST API yazar, akşam bir deployment scripti hazırlarsın. Ama CPU-intensive iş için Go veya Rust, frontend için JavaScript/TypeScript seçersin. Doğru aracı doğru iş için kullanmak senior developer'ın en temel becerisidir.
:::

## Python Kurulumu ve Versiyon Yönetimi

### Sistem Python'u vs Yönetilen Python

:::warning
**Asla** sistem Python'unu (macOS/Linux ile gelen `/usr/bin/python3`) doğrudan kullanma! Sistem Python'u, işletim sisteminin kendi araçları için kullanılır. Paketleri buraya kurarsan sistem araçlarını bozabilirsin. Bu hata yüzünden birçok geliştirici saatlerce debug yapmıştır.
:::

:::concept[pyenv (İng: Python Version Manager)]
pyenv, birden fazla Python versiyonunu aynı makinede yönetmeni sağlayan bir araçtır.

**Türkçe karşılığı:** Python Versiyon Yöneticisi
**Ne işe yarar:** Farklı projeler için farklı Python versiyonları kullanmanı sağlar
**Gerçek hayat benzetmesi:** Bir garaja birden fazla araba park etmek gibi -- hangi projeye gideceksen o arabayı çıkarırsın
:::

### pyenv ile Kurulum

:::code[bash]{title="pyenv Kurulumu ve Kullanımı"}
# macOS
brew install pyenv

# Linux
curl https://pyenv.run | bash

# Windows (pyenv-win)
# PowerShell ile:
# Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"

# Kullanılabilir versiyonları listele
pyenv install --list | grep "3.13"

# Python 3.13.x kur
pyenv install 3.13.2

# Global versiyon ayarla
pyenv global 3.13.2

# Belirli bir proje için lokal versiyon
cd my-project/
pyenv local 3.11.9    # .python-version dosyası oluşturur

# Kurulu versiyonları gör
pyenv versions
:::

:::beginner-mistake
Yaygın hata: `python` komutu yerine `python3` kullanmayı unutmak. Birçok sistemde `python` komutu hala Python 2'ye işaret eder veya hiç yoktur. Her zaman `python3` ve `pip3` kullan -- ya da pyenv ile yönetilen Python kullanarak bu karışıklıktan tamamen kurtul.
:::

:::code[bash]{title="Python Versiyonunu Doğrula"}
# Hangi Python çalışıyor?
which python3
python3 --version

# pyenv kullanıyorsan
pyenv which python
python --version   # pyenv shim üzerinden doğru versiyona yönlendirilir
:::

## Virtual Environment (venv)

:::concept[Virtual Environment (İng: Virtual Environment)]
Virtual environment, bir Python projesi için izole edilmiş bir paket ortamıdır. Her proje kendi bağımsız paketlerine sahip olur.

**Türkçe karşılığı:** Sanal Ortam
**Ne işe yarar:** Projelerin paket bağımlılıklarını birbirinden izole eder
**Gerçek hayat benzetmesi:** Her proje kendi mutfağına sahip bir restoran gibi -- birinin malzemeleri diğerini etkilemez
:::

### Neden Virtual Environment Gerekli?

Diyelim ki iki projen var:
- **Proje A:** Django 4.2 kullanıyor
- **Proje B:** Django 5.1 kullanıyor

Virtual environment olmadan ikisi aynı Django'yu paylaşır -- biri çalışırken diğeri bozulur. venv ile her proje kendi Django versiyonunu kullanır.

:::code[python]{title="venv Oluşturma ve Kullanma"}
# Virtual environment oluştur
python3 -m venv .venv

# Aktif et
# macOS/Linux:
source .venv/bin/activate

# Windows (Git Bash):
source .venv/Scripts/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Aktif olduğunu doğrula (prompt başında (.venv) yazar)
which python        # .venv içindeki Python'u gösterir
uv pip list         # Sadece bu ortamdaki paketleri gösterir

# Paket kur (artık sadece bu ortama kurulur)
uv pip install fastapi uvicorn

# Deaktif et
deactivate
:::

:::tip
Virtual environment klasör adı olarak `.venv` kullan (nokta ile başlayan). Bu, klasörün gizli kalmasını ve `.gitignore`'da kolayca hariç tutulmasını sağlar. `env`, `venv`, `myenv` gibi isimler kullanma -- `.venv` endüstri standardıdır.
:::

:::beginner-mistake
Yaygın hata: Virtual environment'ı aktif etmeyi unutmak. `uv pip install` yapıyorsun ama paket global Python'a kuruluyor. Her terminal açtığında `source .venv/bin/activate` komutunu çalıştırmayı unutma. Prompt'ta `(.venv)` yazısını görmelisin. (Not: uv kullanıyorsan `uv run` ile venv aktif etmeye gerek kalmaz.)
:::

## Package Manager Karşılaştırması

:::comparison
| Özellik | pip + venv | Poetry | Pipenv | Conda |
|---------|-----------|--------|--------|-------|
| **Kurulum** | Python ile gelir | Ayrı kurulum | Ayrı kurulum | Ayrı kurulum (Anaconda/Miniconda) |
| **Lock file** | requirements.txt (manual) | poetry.lock (otomatik) | Pipfile.lock (otomatik) | environment.yml |
| **Dependency resolution** | Basit | Gelişmiş (SAT solver) | Orta | Gelişmiş |
| **Proje yapısı** | Manuel | pyproject.toml (otomatik) | Pipfile | environment.yml |
| **Paket yayınlama** | twine ile ayrı | Built-in (`poetry publish`) | Yok | conda-build |
| **Virtual env yönetimi** | Manuel (venv) | Otomatik | Otomatik | Otomatik (conda env) |
| **Kullanım alanı** | Her yerde, basit projeler | Modern Python projeleri | Web projeleri | Data science, ML |
| **2026 trendi** | Legacy, hala yaygın | Yükselişte | Düşüşte | Data science'da güçlü |

📌 **2026 Güncellemesi:** Tabloda `uv` yok çünkü aşağıda ayrı bir bölümde detaylı anlatılıyor. **uv**, 2024'te Astral tarafından çıkarıldı ve 2026 itibarıyla Python ekosisteminin en hızlı büyüyen aracı. pip'in 10-100x hızlısı, Rust ile yazılmış, lockfile desteği var. Yeni projelerde uv kullanmanı öneririz.

**Tavsiye:** Yeni başlayanlar pip + venv ile temeli öğrensin, sonra **uv'ye geçsin** (2026 standardı). Poetry ciddi projeler için hala güçlü bir seçenek. Data science yapacaksan Conda'yı da öğren. Pipenv artık pek tercih edilmiyor.
:::

### pip: Temel Paket Yöneticisi

:::code[bash]{title="pip ile Çalışmak (Legacy — eski projelerde karşına çıkacak)"}
# ⚠️ Aşağıdaki komutlar eski projelerde karşına çıkacak.
# Yeni projelerde uv kullan (bir sonraki bölüme bak).

# Paket kur
uv pip install requests

# Belirli versiyon kur
uv pip install requests==2.31.0

# Minimum versiyon
uv pip install "requests>=2.28"

# Kurulu paketleri gör
uv pip list
uv pip freeze

# requirements.txt oluştur
uv pip freeze > requirements.txt

# requirements.txt'ten kur
uv pip install -r requirements.txt

# Paket kaldır
uv pip uninstall requests

# Paket bilgisi
uv pip show requests
:::

### uv: 2026'nın En Hızlı Python Paket Yöneticisi

:::concept[uv (İng: Universal Virtualenv / Ultra-fast)]
uv, Astral (Ruff'ı yapan ekip) tarafından Rust ile yazılmış, pip'in 10-100x hızlı çalışan modern alternatifidir.

**Türkçe karşılığı:** Ultra Hızlı Python Paket Yöneticisi
**Ne işe yarar:** pip, venv, pip-tools ve virtualenv'in yaptığı her şeyi tek araçta, çok daha hızlı yapar
**Gerçek hayat benzetmesi:** pip bir bisiklet, uv bir spor araba -- aynı yere gidiyorsun ama 100 kat hızlı
:::

:::code[bash]{title="uv Kurulumu ve Kullanımı"}
# uv kur
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Proje oluştur (venv + pyproject.toml otomatik)
uv init my-project
cd my-project

# Paket ekle (pip install yerine)
uv add fastapi uvicorn
uv add sqlalchemy pydantic

# Dev dependency ekle
uv add --dev pytest ruff mypy

# Paketleri kur (lockfile'dan)
uv sync

# Komut çalıştır (venv aktif etmeye gerek yok!)
uv run python main.py
uv run pytest
uv run ruff check .

# pip uyumlu mod (mevcut projelerde geçiş için)
uv pip install requests
uv pip install -r requirements.txt
uv pip freeze
:::

📌 **2026 Notu:** `uv` neden pip'ten daha iyi?
- **10-100x hızlı** — Rust ile yazıldığı için paket kurulumu saniyeler sürüyor (pip'te dakikalar)
- **Lockfile desteği** — `uv.lock` dosyası ile reproducible builds (pip'te `pip freeze` manuel)
- **Tek araç** — venv oluşturma, paket kurma, script çalıştırma hepsi bir arada
- **pip uyumlu** — `uv pip install` ile mevcut projelerde sorunsuz kullanabilirsin
- **pyproject.toml native** — Modern Python standartlarıyla tam uyumlu

:::beginner-mistake
"pip zaten çalışıyor, neden uv'ye geçeyim?" diyebilirsin. pip hala çalışır ve öğrenmen gerekir (eski projelerde karşına çıkacak). Ama yeni projelerde uv kullan — CI/CD pipeline'ların 10x hızlanır, lockfile sayesinde "bende çalışıyor ama production'da çalışmıyor" sorununu yaşamazsın. Sektör hızla uv'ye geçiyor.
:::

### Poetry: Modern Python Paket Yöneticisi

:::code[bash]{title="Poetry ile Çalışmak"}
# Poetry kur
curl -sSL https://install.python-poetry.org | python3 -

# Yeni proje oluştur
poetry new my-project

# Mevcut projeye Poetry ekle
poetry init

# Paket ekle
poetry add fastapi
poetry add uvicorn

# Dev dependency ekle
poetry add --group dev pytest black ruff mypy

# Paketleri kur (poetry.lock'tan)
poetry install

# Virtual env içinde komut çalıştır
poetry run python main.py
poetry run pytest

# Poetry shell (venv aktif et)
poetry shell
:::

## pyproject.toml ve Modern Proje Yapısı

:::concept[pyproject.toml (İng: Project Configuration File)]
pyproject.toml, Python projelerinin tüm yapılandırmasını tek bir dosyada toplayan modern standarttır (PEP 518, PEP 621).

**Türkçe karşılığı:** Proje Yapılandırma Dosyası
**Ne işe yarar:** Bağımlılıklar, build ayarları, linter/formatter yapılandırması -- hepsini tek dosyada yönetir
**Gerçek hayat benzetmesi:** Bir evin tapusu gibi -- evin tüm bilgileri (sahibi, adresi, özellikleri) tek belgede
:::

### requirements.txt vs pyproject.toml

:::comparison
| Özellik | requirements.txt | pyproject.toml |
|---------|-----------------|----------------|
| **Format** | Düz metin, sadece paket listesi | TOML formatı, yapılandırılmış |
| **Dev dependencies** | Ayrı dosya gerekir (dev-requirements.txt) | `[tool.poetry.group.dev.dependencies]` |
| **Proje metadata** | Yok (ayrı setup.py/setup.cfg gerekir) | Built-in (`[project]` bölümü) |
| **Tool yapılandırması** | Ayrı dosyalar (pytest.ini, .flake8, vb.) | Tek dosyada (`[tool.pytest]`, `[tool.ruff]`) |
| **Lock file** | Yok (pip freeze çıktısı) | poetry.lock / pdm.lock |
| **Standart** | De facto standart | PEP 518/621 resmi standart |
| **2026 durumu** | Hala yaygın, basit projeler için yeterli | Modern standart, tercih edilen |

**Tavsiye:** Yeni projelerde pyproject.toml kullan. requirements.txt'i sadece deployment veya Docker gibi basitlik gereken yerlerde kullan.
:::

:::code[toml]{title="Örnek pyproject.toml (Poetry ile)"}
[tool.poetry]
name = "my-awesome-api"
version = "0.1.0"
description = "FastAPI ile RESTful API"
authors = ["Taha <taha@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.13"
fastapi = "^0.115.0"
uvicorn = {extras = ["standard"], version = "^0.34.0"}
sqlalchemy = "^2.0"
pydantic = "^2.10"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-cov = "^6.0"
ruff = "^0.9.0"
mypy = "^1.14"
pre-commit = "^4.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# Ruff yapılandırması (linter + formatter)
[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

# Pytest yapılandırması
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
addopts = "-v --cov=src --cov-report=term-missing"

# MyPy yapılandırması
[tool.mypy]
python_version = "3.13"
strict = true
:::

### Profesyonel Proje Klasör Yapısı

:::code[text]{title="Modern Python Proje Yapısı"}
my-awesome-api/
├── .venv/                  # Virtual environment (git'e EKLEME)
├── .env                    # Ortam değişkenleri (git'e EKLEME)
├── .env.example            # .env şablonu (git'e EKLE)
├── .gitignore              # Git'ten hariç tutulacak dosyalar
├── .python-version         # pyenv versiyon dosyası (3.13.2)
├── pyproject.toml          # Proje yapılandırması (ana dosya)
├── poetry.lock             # Kilit dosyası (git'e EKLE)
├── README.md               # Proje dokümantasyonu
├── Makefile                # Sık kullanılan komutlar
├── Dockerfile              # Container yapılandırması
├── docker-compose.yml      # Servis orkestrasyonu
├── src/
│   └── my_awesome_api/
│       ├── __init__.py     # Paket tanımı
│       ├── main.py         # Uygulama giriş noktası
│       ├── config.py       # Yapılandırma yönetimi
│       ├── models/         # Veritabanı modelleri
│       │   ├── __init__.py
│       │   └── user.py
│       ├── routes/         # API endpoint'leri
│       │   ├── __init__.py
│       │   └── auth.py
│       ├── services/       # İş mantığı
│       │   ├── __init__.py
│       │   └── auth_service.py
│       └── utils/          # Yardımcı fonksiyonlar
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures
│   ├── test_auth.py
│   └── test_models.py
├── scripts/                # Yardımcı scriptler
│   └── seed_db.py
└── docs/                   # Dokümantasyon
    └── api.md
:::

## .gitignore ve .env Best Practices

:::code[text]{title="Python Projesi .gitignore"}
# Virtual environment
.venv/
venv/
env/

# Python cache
__pycache__/
*.py[cod]
*.pyo
*.egg-info/
dist/
build/

# Environment variables (GİZLİ BİLGİLER!)
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Test / Coverage
.coverage
htmlcov/
.pytest_cache/

# MyPy
.mypy_cache/

# Ruff
.ruff_cache/
:::

:::warning
`.env` dosyasını **asla** Git'e ekleme! API anahtarları, veritabanı şifreleri gibi hassas bilgiler bu dosyada bulunur. Bunun yerine `.env.example` dosyası oluştur ve şablonu paylaş. Bu hata birçok şirketin güvenlik ihlali yaşamasına neden olmuştur.
:::

:::code[bash]{title=".env ve .env.example Kullanımı"}
# .env.example (git'e EKLE -- şablon, gerçek değerler yok)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
REDIS_URL=redis://localhost:6379
DEBUG=true

# .env (git'e EKLEME -- gerçek değerler)
DATABASE_URL=postgresql://taha:gercek_sifre@localhost:5432/myapp
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k_cok_gizli_anahtar
REDIS_URL=redis://localhost:6379
DEBUG=true
:::

## Python vs Diğer Diller: Ne Zaman Hangisi?

:::comparison
| Kriter | Python | JavaScript/TypeScript | Go | Java |
|--------|--------|----------------------|-----|------|
| **Öğrenme kolaylığı** | Kolay | Orta | Orta | Zor |
| **Performans** | Yavaş (interpreted) | Orta (V8 JIT) | Hızlı (compiled) | Hızlı (JVM JIT) |
| **AI/ML** | Dominant | Sınırlı | Sınırlı | Orta |
| **Web Backend** | FastAPI, Django | Express, Next.js | Gin, Fiber | Spring Boot |
| **Frontend** | Yok | Dominant (React, Vue) | Yok | Yok |
| **DevOps/Scripting** | Mükemmel | Orta | İyi (tek binary) | Kötü |
| **Concurrency** | Zayıf (GIL) | Event loop (iyi) | Goroutines (mükemmel) | Thread (iyi) |
| **Tip sistemi** | Dynamic (+ type hints) | Dynamic (TS: static) | Static | Static |
| **Startup time** | Yavaş | Hızlı | Çok hızlı | Yavaş (JVM) |
| **Ne zaman kullan** | AI/ML, data, scripting, hızlı prototip, backend API | Full stack web, frontend | Microservices, CLI tools, yüksek performans | Enterprise, büyük ekipler, Android |

**Tavsiye:** "Her dili öğrenmem lazım" sendromuna kapılma. Python + JavaScript/TypeScript ikilisi 2026'da iş piyasasının büyük çoğunluğunu kapsar. Go ve Java'yı ihtiyaç olduğunda öğrenirsin.
:::

## Python REPL ve Debugging Temelleri

:::concept[REPL (İng: Read-Eval-Print Loop)]
REPL, Python kodunu satır satır yazıp anında sonucunu görmenizi sağlayan interaktif ortamdır.

**Türkçe karşılığı:** Oku-Değerlendir-Yazdır Döngüsü
**Ne işe yarar:** Hızlı denemeler, kod test etme, API'leri keşfetme
**Gerçek hayat benzetmesi:** Bir hesap makinesi gibi -- yaz, enter'a bas, sonucu gör
:::

:::code[bash]{title="Python REPL Kullanımı"}
# Standart REPL
python3

# Gelişmiş REPL (IPython) -- renklendirme, tab completion, magic commands
uv add ipython
ipython

# REPL içinde hızlı öğrenme
>>> import requests
>>> dir(requests)          # Modülün tüm özelliklerini gör
>>> help(requests.get)     # Fonksiyon dokümantasyonu
>>> type(requests.get)     # Tip bilgisi

# REPL'den çıkış
>>> exit()
# veya Ctrl+D (macOS/Linux), Ctrl+Z + Enter (Windows)
:::

### Debugging Temelleri

:::code[python]{title="Python Debugging Yöntemleri"}
# 1. print() debugging (en basit ama etkili)
def calculate_total(items):
    total = 0
    for item in items:
        print(f"DEBUG: item={item}, total={total}")  # debug print
        total += item["price"] * item["quantity"]
    print(f"DEBUG: final total={total}")
    return total

# 2. breakpoint() -- Python 3.7+ built-in debugger
def calculate_total(items):
    total = 0
    for item in items:
        breakpoint()  # Burada durur, değişkenleri inceleyebilirsin
        total += item["price"] * item["quantity"]
    return total

# 3. logging modülü (production'da print yerine bunu kullan)
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def calculate_total(items):
    logger.debug("calculate_total çağrıldı, %d item", len(items))
    total = 0
    for item in items:
        logger.debug("İşlenen item: %s", item)
        total += item["price"] * item["quantity"]
    logger.info("Toplam hesaplandı: %.2f", total)
    return total
:::

:::code[bash]{title="breakpoint() Kullanımı (pdb komutları)"}
# breakpoint() durduğunda kullanacağın komutlar:
# n (next)     → Bir sonraki satıra geç
# s (step)     → Fonksiyonun içine gir
# c (continue) → Bir sonraki breakpoint'e kadar devam et
# p variable   → Değişkenin değerini yazdır
# l (list)     → Mevcut kodu göster
# q (quit)     → Debugger'dan çık
# h (help)     → Yardım
:::

:::tip
Production kodunda `print()` debugging bırakma. `breakpoint()` veya `logging` modülünü kullan. VS Code kullanıyorsan launch.json ile visual debugger kur -- breakpoint koyma, değişken izleme ve call stack görüntüleme gibi özellikler çok daha verimli debug yapmanı sağlar.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Python Ortamini Kurup Dogrulama (Kolay)

Python'u pyenv ile kurup, versiyonu dogrulayin ve ilk script'inizi calistirin.

```bash
# 1. pyenv ile Python kur
pyenv install 3.13.2
pyenv global 3.13.2

# 2. Dogrula
python --version   # Python 3.13.2 ciktisi olmali
which python       # pyenv shims yolunu gostermeli

# 3. Ilk script'ini yaz ve calistir
cat > hello.py << 'EOF'
import sys
import platform

print(f"Python Versiyon: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Calisma Dizini: {__file__}")
print("Merhaba Dunya! Python ortamin hazir!")
EOF

python hello.py
```

**Beklenen Sonuc:** Python 3.13.2 versiyonu gorunmeli, script hatasiz calismali ve platform bilgisini gostermeli.
**Ipucu:** pyenv kurulu degilse once `curl https://pyenv.run | bash` ile kur (Linux/Mac) veya pyenv-win kullan (Windows).

---

### Alistirma 2: Virtual Environment ve Paket Yonetimi (Orta)

uv ve venv kullanarak izole bir proje ortami olustur, paketleri yukle ve requirements.txt ile paylasimli hale getir.

```bash
# 1. Proje klasoru olustur
mkdir api-test-project && cd api-test-project

# 2. Virtual environment olustur ve aktive et
python -m venv .venv
source .venv/bin/activate   # Windows: source .venv/Scripts/activate

# 3. Paketleri yukle
uv pip install requests httpx python-dotenv

# 4. Yuklu paketleri listele ve kaydet
uv pip freeze > requirements.txt
cat requirements.txt

# 5. Test script'i yaz
cat > test_api.py << 'EOF'
import requests

# JSONPlaceholder API'den veri cek
response = requests.get("https://jsonplaceholder.typicode.com/users/1")
user = response.json()

print(f"Status Code: {response.status_code}")
print(f"Kullanici: {user['name']}")
print(f"Email: {user['email']}")
print(f"Sehir: {user['address']['city']}")
EOF

python test_api.py

# 6. Ortami deaktive et
deactivate

# 7. Ayni ortami baska bir yerde yeniden olustur
# mkdir /tmp/test-env && cd /tmp/test-env
# python -m venv .venv && source .venv/bin/activate
# uv pip install -r /path/to/requirements.txt
```

**Beklenen Sonuc:** API'den kullanici bilgisi basariyla cekilmeli. requirements.txt'te requests, httpx ve python-dotenv paketleri ve versiyonlari listelenmeli. Baska bir ortamda requirements.txt ile ayni paketler yuklenebilmeli.
**Ipucu:** `.venv` klasorunu `.gitignore`'a eklemeyi unutma! Sadece `requirements.txt` veya `pyproject.toml` paylasilmali.

---

### Alistirma 3: pyproject.toml ile Modern Proje Yapisi (Zor)

uv veya Poetry kullanarak modern Python proje yapisini kurup, linter ve formatter ayarla.

```bash
# 1. uv ile proje olustur
uv init modern-python-project
cd modern-python-project

# 2. Bagimliliklari ekle
uv add requests httpx
uv add --dev pytest ruff mypy

# 3. pyproject.toml'u incele ve asagidaki ayarlari ekle:
# [tool.ruff]
# line-length = 88
# target-version = "py312"
#
# [tool.ruff.lint]
# select = ["E", "F", "I", "N", "W"]
#
# [tool.mypy]
# python_version = "3.13"
# strict = true

# 4. src/ klasorune ornek kod yaz:
mkdir -p src/modern_python_project
cat > src/modern_python_project/main.py << 'EOF'
def greet(name: str) -> str:
    """Kullaniciyi selamla."""
    return f"Merhaba, {name}!"

def add(a: int, b: int) -> int:
    """Iki sayiyi topla."""
    return a + b

if __name__ == "__main__":
    print(greet("Dunya"))
    print(f"2 + 3 = {add(2, 3)}")
EOF

# 5. Linter ve type checker calistir
uv run ruff check .
uv run mypy src/

# 6. Test yaz ve calistir
mkdir tests
cat > tests/test_main.py << 'EOF'
from modern_python_project.main import greet, add

def test_greet():
    assert greet("Ali") == "Merhaba, Ali!"

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
EOF

uv run pytest tests/ -v
```

**Beklenen Sonuc:** `ruff check` hata vermemeli, `mypy --strict` tip hatasiz gecmeli, `pytest` tum testler gecmeli. pyproject.toml'da tum proje ayarlari tek bir dosyada tanimlanmis olmali.
**Ipucu:** `uv init` otomatik olarak pyproject.toml olusturur. Ek ayarlari dosyayi editleyerek ekle.

5. **.gitignore ve .env.example oluştur:**
   - Yukarıdaki .gitignore şablonunu kullan
   - `.env.example` dosyası oluştur

6. **REPL ve Debugging:**
   - Python REPL'de `import this` yaz (The Zen of Python)
   - Basit bir fonksiyon yaz, `breakpoint()` ekle, pdb komutlarını dene
   - Aynı fonksiyonda `logging` modülünü kullanarak debug output yaz
:::

:::knowledge-check
type: multiple_choice
question: "Neden her Python projesi için ayrı virtual environment oluşturmalısın?"
options:
  - "Python daha hızlı çalışır"
  - "Projelerin paket bağımlılıklarını birbirinden izole etmek için -- farklı projeler farklı versiyon paketler kullanabilir"
  - "Python bunu zorunlu kılıyor, venv olmadan çalışmaz"
  - "Güvenlik nedeniyle, virüsleri engellemek için"
correct: 1
explanation: "Virtual environment her projenin kendi bağımsız paket ortamına sahip olmasını sağlar. Proje A Django 4.2, Proje B Django 5.1 kullanabilir. venv olmadan tüm paketler global Python'a kurulur ve versiyon çatışmaları kaçınılmaz olur."
:::

:::knowledge-check
type: multiple_choice
question: "pyproject.toml'un requirements.txt'e göre en büyük avantajı nedir?"
options:
  - "Daha küçük dosya boyutu"
  - "Sadece Poetry ile kullanılabilir"
  - "Bağımlılıklar, build ayarları, linter/formatter yapılandırması gibi tüm proje yapılandırmasını tek dosyada toplar"
  - "requirements.txt'ten daha hızlı paket kurar"
correct: 2
explanation: "pyproject.toml (PEP 518/621), sadece bağımlılıkları değil, proje metadata'sını, build ayarlarını, pytest/ruff/mypy yapılandırmasını tek dosyada toplar. Bu sayede setup.py, setup.cfg, pytest.ini, .flake8 gibi ayrı dosyalara gerek kalmaz."
:::

:::interview
**Mülakat Sorusu:** "Python'da virtual environment nedir ve neden gereklidir? Bir projede nasıl yönetirsiniz?"

**Beklenen cevap (özetlenmiş):**

1. **Tanım:** Virtual environment, bir Python projesi için izole edilmiş paket ortamıdır. Sistem Python'undan bağımsız çalışır.
2. **Neden gerekli:** Farklı projelerin farklı paket versiyonlarını kullanabilmesi, sistem Python'unun bozulmaması ve reproducible build'ler için.
3. **Nasıl oluşturulur:** `python3 -m venv .venv` ile oluşturulur, `source .venv/bin/activate` ile aktif edilir.
4. **Best practices:** `.venv` adlandırması, `.gitignore`'a eklenmesi, `requirements.txt` veya `poetry.lock` ile bağımlılık takibi.
5. **Modern alternatifler:** Poetry otomatik venv yönetimi sunar. Docker container'ları da izolasyon sağlar.

**Bonus puan:** "Production'da Docker kullandığımızda bile, local geliştirmede venv kullanırız çünkü IDE entegrasyonu ve hızlı iterasyon için gereklidir" dersen artı puan alırsın.
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6

### Prompt Ornekleri

**1. Konuyu Derinlemesine Anla:**
> "Python'da virtual environment neden gerekli? Sistem Python'u ile venv arasindaki farki, paket izolasyonunun nasil calistigini ve .venv klasorunun icinde neler oldugunu detayli anlat. PATH degiskeninin bu sureceteki rolu ne?"

*Neden:* Virtual environment'in sadece nasil kullanildigini degil, neden var oldugunu anlamak kalici ogrenme saglar

**2. Pratik Uygulama:**
> "Sifirdan bir Python projesi kuruyorum. uv ile proje olusturma, bagimliliklari ekleme, pyproject.toml yapilandirma, .gitignore ve .env.example olusturma adimlarini sirala. Her adimda neden o komutu kullandigimi acikla."

*Follow-up:* "Bu projeye pre-commit hooks (ruff + mypy) eklemek istesem adimlar ne olur? Makefile'a hangi target'lari eklemeliyim?"

**3. Mukemmellik Icin:**
> "pip, poetry ve uv arasindaki farklari dependency resolution, lockfile yonetimi, performans ve CI/CD entegrasyonu acisindan karsilastir. 2026'da yeni bir production projesi icin hangisini neden secmeliyim?"

### Pair Programming Ipucu
Proje kurarken AI'a pyproject.toml dosyani yapistir: "Bu pyproject.toml yapilandirmasini incele. Eksik veya iyilestirilmesi gereken ayarlar var mi? ruff, mypy ve pytest konfigurasyonu icin best practice onerilerin neler?"
:::

:::must-note
- Virtual environment: `python3 -m venv .venv` ile oluştur, `source .venv/bin/activate` ile aktif et
- **Asla** sistem Python'una paket kurma -- her zaman venv veya pyenv kullan
- `.env` dosyasını Git'e **asla** ekleme -- `.env.example` şablonu paylaş
- **uv = 2026 standardı**: `uv init`, `uv add paket`, `uv add --dev paket`, `uv sync`, `uv run`
- pyproject.toml = modern standart (PEP 518/621), requirements.txt = legacy ama hala yaygın
- Poetry: `poetry add paket`, `poetry add --group dev paket`, `poetry install`, `poetry run`
- pip (legacy): `uv pip install paket`, `uv pip freeze > requirements.txt` (eski projelerde karşına çıkacak, bilmen gerekir)
- Proje yapısı: `src/paket_adi/`, `tests/`, `.venv/`, `pyproject.toml`, `.gitignore`, `.env.example`
- Debug araclari: `print()` (basit), `breakpoint()` (pdb), `logging` (production)
- pdb komutlari: n=next, s=step, c=continue, p=print, l=list, q=quit
- Python REPL'de: `dir(obj)` ozellikleri gor, `help(func)` dokumantasyon oku, `type(obj)` tipini gor
:::

:::senior-learns
Bir Senior Developer, Python ortamını öğrenirken şu yaklaşımı benimser:

1. **PEP'leri okur** - PEP 518 (pyproject.toml), PEP 621 (project metadata), PEP 723 (inline script metadata) gibi orijinal spesifikasyonları inceler. Bir blog yazısı yerine kaynağa gider. "Bu özellik neden bu şekilde tasarlandı?" sorusuna PEP'teki Motivation bölümünden cevap bulur.
2. **Farklı tool chain'leri dener** - pip + venv, Poetry, PDM, Hatch, uv gibi alternatifleri küçük bir projede dener. Her birinin trade-off'larını firsthand experience ile öğrenir. 2026'da `uv` (Astral) gibi yeni araçları da takip eder.
3. **Makefile veya taskfile yazar** - Sık kullanılan komutları (`make lint`, `make test`, `make run`) otomatize eder. Yeni bir takım üyesi projeye dahil olduğunda `make setup` ile her şeyin kurulmasını sağlar. Developer experience (DX) her zaman önceliğidir.
4. **Docker ile entegrasyonu düşünür** - "Local'de venv, CI/CD'de Docker" stratejisini benimser. Multi-stage Docker build ile production image'ını küçültür. `.dockerignore` dosyasını `.gitignore` kadar ciddiye alır.
5. **pre-commit hooks kurar** - Ruff (linting + formatting), mypy (type checking), pytest (testler) gibi araçları pre-commit hook olarak yapılandırır. Kod kalitesini commit seviyesinde garanti altına alır.
6. **Takım için standart oluşturur** - `CONTRIBUTING.md` ile geliştirme ortamı kurulumunu dokümante eder. pyproject.toml'daki tool yapılandırmalarıyla tüm takımın aynı linter/formatter kurallarını kullanmasını sağlar.

**Profesyonel Mindset:** "Python ortamı kurulumu, projenin temelini atar. Senior developer, projeye başlarken ilk 30 dakikasını pyproject.toml, .gitignore, pre-commit hooks ve CI pipeline'ını kurmaya ayırır. Bu yatırım, projenin ömrü boyunca kendini yüzlerce kat geri öder. Acemi projeye hemen kod yazarak başlar, senior ise ortamı kurarak başlar."
:::

:::english
**Teknik Ingilizce - Bu Dersteki Terimler:**

1. **Virtual Environment** (vir-choo-ul en-vai-run-ment) --> Sanal Ortam
   *"Always create a virtual environment before installing project dependencies."*

2. **Dependency** (dih-pen-den-si) --> Bagimlili
   *"FastAPI is a dependency of our project, listed in pyproject.toml."*

3. **Package Manager** (pak-ij man-ij-er) --> Paket Yoneticisi
   *"Poetry is a modern Python package manager that handles dependency resolution automatically."*

4. **Lock File** (lok fail) --> Kilit Dosyasi
   *"The poetry.lock file ensures all developers use the exact same dependency versions."*

5. **Interpreter** (in-tur-preh-ter) --> Yorumlayici
   *"Python is an interpreted language -- the interpreter executes code line by line."*

**Okuma Egzersizi:** Python Packaging User Guide'in "Managing Dependencies" bolumunu Ingilizce oku: https://packaging.python.org/en/latest/tutorials/managing-dependencies/

**Yazma Pratigi:** Asagidaki commit mesajini Ingilizce yaz: "Proje ortamini ve bagimlilik yapilandirmasini kurdum"
--> Ornek: `chore: set up project environment and dependency configuration`
:::

:::external-resource
- **Python Resmi Docs:** "venv - Virtual Environments" (docs.python.org, Ingilizce, ucretsiz)
- **Poetry Dokumantasyonu:** python-poetry.org (Ingilizce, ucretsiz)
- **Real Python:** "Python Virtual Environments: A Primer" (realpython.com, Ingilizce, ucretsiz)
- **Hynek Schlawack:** "Python Packaging" blog serisi (hynek.me, Ingilizce, ucretsiz)
- **Astral uv:** "An extremely fast Python package installer" (github.com/astral-sh/uv, ucretsiz)
:::
