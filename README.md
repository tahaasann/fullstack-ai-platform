<div align="center">

# 🚀 DevMaster — Full-Stack AI Developer Education Platform

**"Skip junior, think senior from day one"**

[🇹🇷 Türkçe](#-türkçe) · [🇬🇧 English](#-english)

![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 🇬🇧 English

### What is DevMaster?

DevMaster is a self-hosted, open-source education platform designed to take you from zero to a **Full Stack AI Engineer** — without ever thinking like a junior. Every lesson, project, and challenge is built with a senior-level mindset.

### Platform at a Glance

| Metric | Count |
|--------|-------|
| Structured Lessons | 48 |
| Hands-on Challenges | 60 (106 problems) |
| Interactive Quizzes | 20 (184 questions) |
| Portfolio Projects | 10 |
| Career Guides | 7 |
| English Vocabulary | 504 terms |
| Sentence Patterns | 195 |
| Work Scenarios | 77 |

### Curriculum

| Phase | Topic | Weeks |
|-------|-------|-------|
| 1 | **Fundamentals** — Internet, Python, JavaScript/TypeScript, Git, Terminal | 1-2 |
| 2 | **Frontend** — HTML5/CSS3, React + TypeScript, Tailwind CSS, Component Architecture | 3-5 |
| 3 | **Backend** — Node.js/Express, REST API, Databases, Auth, Testing | 5-7 |
| 4 | **DevOps** — Docker, CI/CD, Cloud (AWS), Security | 7-8 |
| 5 | **AI/ML** — ML Fundamentals, Deep Learning, LLM APIs, RAG, AI Agents | 8-10 |
| 6 | **Career** — System Design, DSA, Portfolio, Interview Prep | 10-12 |

### Key Features

- 🎯 **Senior-first mentality** — Every lesson includes "How a senior thinks" sections
- 🤖 **AI-guided learning** — Prompt templates for Claude, GPT, Gemini per lesson
- 💼 **10 portfolio projects** — From personal blog to AI code review tool
- 📝 **Career toolkit** — ATS-optimized CV templates, cover letter guides, interview prep
- 🌍 **Technical English** — 504 terms, 195 sentence patterns, 77 workplace scenarios
- 🏗️ **Real-world patterns** — Every concept tied to production use cases
- 🌙 **Dark theme** — Developer-friendly UI
- 📊 **Progress tracking** — Daily goals, streaks, completion stats

### Tech Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React 19, TypeScript, Tailwind CSS 4, Vite, Zustand |
| Backend | FastAPI, SQLAlchemy, SQLite |
| Content | Markdown with custom directives |
| DevOps | Docker, GitHub Actions |

### Quick Start

#### Prerequisites

- Python 3.13+
- Node.js 22+
- pnpm (recommended) or npm

#### Installation

```bash
# Clone
git clone https://github.com/tahaasann/fullstack-ai-platform.git
cd fullstack-ai-platform

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --port 8000 --reload
# Backend runs at http://localhost:8000

# Frontend (new terminal)
cd frontend
pnpm install
pnpm dev
# Frontend runs at http://localhost:5173
```

#### Docker

```bash
docker compose up --build
# Frontend: http://localhost:3000 | Backend: http://localhost:8000
```

### Project Structure

```
fullstack-ai-platform/
├── backend/                # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── models.py           # SQLAlchemy models
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── api/            # API client
│   │   └── types/          # TypeScript definitions
│   └── Dockerfile
├── content/                # Education content
│   ├── phases/             # 6 phases, 20 modules, 48 lessons
│   ├── projects/           # 10 project definitions
│   ├── career/             # Career guides (CV, LinkedIn, etc.)
│   └── english/            # Vocabulary, patterns, scenarios
├── docker-compose.yml
└── .github/workflows/      # CI/CD
```

### Contributing

Contributions are welcome! Whether it's fixing a typo, adding a new lesson, or improving the UI — feel free to open a PR.

### License

[MIT License](LICENSE) — free to use, modify, and distribute.

---

## 🇹🇷 Türkçe

### DevMaster Nedir?

DevMaster, sıfırdan **Full Stack AI Engineer** olmayı hedefleyen, açık kaynaklı bir eğitim platformudur. "Junior olmadan senior olmak" mentalitesiyle tasarlanmıştır. Her ders, proje ve challenge senior seviyesinde düşünmeyi öğretir.

### Platform Özeti

| Metrik | Sayı |
|--------|------|
| Yapılandırılmış Ders | 48 |
| Pratik Challenge | 60 (106 problem) |
| İnteraktif Quiz | 20 (184 soru) |
| Portfolyo Projesi | 10 |
| Kariyer Rehberi | 7 |
| İngilizce Kelime | 504 |
| Cümle Kalıbı | 195 |
| İş Senaryosu | 77 |

### Müfredat

| Faz | Konu | Hafta |
|-----|------|-------|
| 1 | **Temeller** — İnternet, Python, JavaScript/TypeScript, Git, Terminal | 1-2 |
| 2 | **Frontend** — HTML5/CSS3, React + TypeScript, Tailwind CSS, Component Mimarisi | 3-5 |
| 3 | **Backend** — Node.js/Express, REST API, Veritabanları, Auth, Testing | 5-7 |
| 4 | **DevOps** — Docker, CI/CD, Cloud (AWS), Güvenlik | 7-8 |
| 5 | **AI/ML** — ML Temelleri, Deep Learning, LLM API'leri, RAG, AI Agents | 8-10 |
| 6 | **Kariyer** — System Design, DSA, Portfolyo, Mülakat Hazırlığı | 10-12 |

### Temel Özellikler

- 🎯 **Senior-first mentalite** — Her derste "Senior nasıl düşünür" bölümleri
- 🤖 **AI rehberli öğrenme** — Her ders için Claude, GPT, Gemini prompt şablonları
- 💼 **10 portfolyo projesi** — Kişisel blogdan AI code review tool'a kadar
- 📝 **Kariyer araç seti** — ATS uyumlu CV şablonları, cover letter rehberi, mülakat hazırlığı
- 🌍 **Teknik İngilizce** — 504 terim, 195 cümle kalıbı, 77 iş senaryosu
- 🏗️ **Gerçek dünya pattern'leri** — Her kavram production kullanım senaryolarıyla
- 🌙 **Dark tema** — Göz yormayan, modern arayüz
- 📊 **İlerleme takibi** — Günlük hedefler, streak'ler, tamamlanma istatistikleri

### Teknoloji Yığını

| Katman | Teknolojiler |
|--------|-------------|
| Frontend | React 19, TypeScript, Tailwind CSS 4, Vite, Zustand |
| Backend | FastAPI, SQLAlchemy, SQLite |
| İçerik | Markdown (özel directive'lerle) |
| DevOps | Docker, GitHub Actions |

### Hızlı Başlangıç

#### Gereksinimler

- Python 3.13+
- Node.js 22+
- pnpm (önerilen) veya npm

#### Kurulum

```bash
# Klonla
git clone https://github.com/tahaasann/fullstack-ai-platform.git
cd fullstack-ai-platform

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --port 8000 --reload
# Backend: http://localhost:8000

# Frontend (yeni terminal)
cd frontend
pnpm install
pnpm dev
# Frontend: http://localhost:5173
```

#### Docker

```bash
docker compose up --build
# Frontend: http://localhost:3000 | Backend: http://localhost:8000
```

### Proje Yapısı

```
fullstack-ai-platform/
├── backend/                # FastAPI backend
│   ├── main.py             # Uygulama giriş noktası
│   ├── models.py           # SQLAlchemy modelleri
│   ├── routers/            # API endpoint'leri
│   ├── services/           # İş mantığı
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI bileşenleri
│   │   ├── pages/          # Sayfa bileşenleri
│   │   ├── hooks/          # Custom hook'lar
│   │   ├── api/            # API istemcisi
│   │   └── types/          # TypeScript tip tanımları
│   └── Dockerfile
├── content/                # Eğitim içeriği
│   ├── phases/             # 6 faz, 20 modül, 48 ders
│   ├── projects/           # 10 proje tanımı
│   ├── career/             # Kariyer rehberleri (CV, LinkedIn vb.)
│   └── english/            # Kelimeler, kalıplar, senaryolar
├── docker-compose.yml
└── .github/workflows/      # CI/CD
```

### Katkıda Bulunma

Katkılarınızı bekliyoruz! Yazım hatası düzeltmek, yeni ders eklemek veya UI geliştirmek — PR açmaktan çekinmeyin.

### Lisans

[MIT Lisansı](LICENSE) — özgürce kullanın, değiştirin ve dağıtın.

---

<div align="center">

**Built with ❤️ for developers who refuse to think like juniors.**

</div>
