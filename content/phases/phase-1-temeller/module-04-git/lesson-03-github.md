---
id: mod-04-git/lesson-03
title: "GitHub, PR Workflow ve Takım İş Birliği"
estimated_minutes: 45
tags: ["github", "pull-request", "code-review", "github-actions", "open-source"]
prerequisites: ["mod-04-git/lesson-01", "mod-04-git/lesson-02"]
order: 3
---

# GitHub, PR Workflow ve Takım İş Birliği

:::realworld
Tek başına kod yazarken Git yeterli olabilir, ama profesyonel dünyada yazılım bir takım sporudur. GitHub, dünya genelinde 100 milyondan fazla developer'ın birlikte çalıştığı platformdur. İster bir startup'ta, ister büyük bir kurumda çalış -- Pull Request açmak, Code Review yapmak ve CI/CD pipeline'ları kurmak günlük iş akışının temel parçası olacak. Bu derste, GitHub'ı profesyonel seviyede kullanmayı ve takım iş birliği kültürünü öğreneceksin.
:::

## Neden Bu Konuyu Öğreniyorsun?

Modern yazılım geliştirmede GitHub sadece bir kod deposu değil, aynı zamanda proje yönetim aracı, CI/CD platformu ve developer topluluğunun merkezidir. GitHub'ı iyi bilmeden:

- Bir takıma katıldığında iş akışına uyum sağlayamazsın
- Açık kaynak projelere katkıda bulunamazsın
- Code Review süreçlerini yürütemezsin
- CI/CD pipeline'larını kuramazsın
- Portföyünü potansiyel işverenlere gösteremezsin

:::deha-tip
Deha seviyesi geliştiriciler, GitHub profillerini bir portfolyo gibi kullanır. Commit geçmişi düzenli, PR açıklamaları detaylı, Issue'lar net tanımlanmış olur. Bir hiring manager GitHub profiline baktığında, o kişinin nasıl çalıştığını, kod kalitesini ve iletişim becerilerini anında değerlendirebilir. GitHub profili, CV'den daha çok şey anlatır.
:::

## Git vs GitHub: Temel Fark

:::concept[GitHub (İng: GitHub)]
GitHub, Git repository'lerini barındıran (hosting), takım iş birliği araçları sunan ve CI/CD entegrasyonu sağlayan bulut tabanlı bir platformdur.

**Türkçe karşılığı:** GitHub (özel isim, çevrilmez)
**Ne işe yarar:** Git repository'lerini uzaktan barındırır, Pull Request, Issue, Actions gibi iş birliği araçları sunar
**Gerçek hayat benzetmesi:** Git bir kalem, GitHub ise Google Docs -- kalemle kağıda yazabilirsin ama Google Docs ile başkalarıyla aynı anda çalışabilirsin
:::

:::comparison
| Özellik | Git | GitHub |
|---------|-----|--------|
| Tür | Versiyon kontrol sistemi (araç) | Bulut platformu (hizmet) |
| Çalışma yeri | Lokal bilgisayar | Web üzerinde (remote) |
| İş birliği | Doğrudan yok | Pull Request, Issue, Review |
| CI/CD | Yok | GitHub Actions |
| Fiyat | Ücretsiz, açık kaynak | Ücretsiz + ücretli planlar |
| Alternatifler | - | GitLab, Bitbucket, Azure DevOps |

**Tavsiye:** Git, altta çalışan motor; GitHub ise o motorun üzerine inşa edilmiş araç seti. İkisini karıştırma -- Git bilmeden GitHub kullanmak, motor bilmeden araba tamir etmeye benzer.
:::

## Repository, Fork ve Clone

### Repository Oluşturma

GitHub'da yeni bir repository oluşturmak için iki yol vardır:

:::code[bash]{title="Yol 1: GitHub Web Arayüzünden"}
# github.com/new adresine git
# Repository adı, açıklama, public/private seç
# README, .gitignore ve License ekle
# "Create repository" butonuna tıkla
:::

:::code[bash]{title="Yol 2: CLI ile Oluştur ve Push Et"}
# Lokal proje oluştur
mkdir my-project && cd my-project
git init
echo "# My Project" > README.md
git add README.md
git commit -m "docs: initial commit with README"

# GitHub'da remote repo oluştur (gh CLI ile)
gh repo create my-project --public --source=. --push

# veya manuel olarak remote ekle
git remote add origin git@github.com:kullaniciadi/my-project.git
git push -u origin main
:::

### Fork ve Clone Farkı

:::concept[Fork (İng: Fork)]
Fork, başka birinin repository'sinin kendi GitHub hesabına bağımsız bir kopyasını oluşturma işlemidir.

**Türkçe karşılığı:** Çatal / Çatallama
**Ne işe yarar:** Başkasının projesinde değişiklik yapmak istediğinde, kendi kopyanı oluşturursun. Orijinal projeyi etkilemeden çalışırsın.
**Gerçek hayat benzetmesi:** Bir kitabın fotokopisini çekip, fotokopide not almak -- orijinal kitap değişmez
:::

:::code[bash]{title="Fork ve Clone İş Akışı"}
# 1. GitHub web arayüzünde "Fork" butonuna tıkla
# Bu, repo'yu kendi hesabına kopyalar

# 2. Kendi fork'unu lokal bilgisayarına klonla
git clone git@github.com:SENIN_KULLANICI_ADIN/proje.git
cd proje

# 3. Orijinal repo'yu "upstream" olarak ekle
git remote add upstream git@github.com:ORIJINAL_SAHIP/proje.git

# 4. Remote'ları kontrol et
git remote -v
# origin    git@github.com:SENIN_KULLANICI_ADIN/proje.git (fetch)
# origin    git@github.com:SENIN_KULLANICI_ADIN/proje.git (push)
# upstream  git@github.com:ORIJINAL_SAHIP/proje.git (fetch)
# upstream  git@github.com:ORIJINAL_SAHIP/proje.git (push)

# 5. Upstream'deki değişiklikleri çek (fork'unu güncel tut)
git fetch upstream
git merge upstream/main
:::

:::beginner-mistake
Yaygın hata: Fork ile Clone'u karıştırmak. Clone, bir repo'yu lokal bilgisayarına indirmektir. Fork ise GitHub sunucusunda kendi hesabına kopya oluşturmaktır. Açık kaynak projelere katkıda bulunurken her ikisini de kullanırsın: önce Fork, sonra Clone.
:::

## Pull Request (PR) Oluşturma ve Best Practices

:::concept[Pull Request / PR (İng: Pull Request)]
Pull Request, bir branch'teki değişikliklerin ana branch'e (genellikle main) birleştirilmesi için yapılan resmi istektir. Kod incelemesi (Code Review) bu süreçte gerçekleşir.

**Türkçe karşılığı:** Birleştirme İsteği / Çekme İsteği
**Ne işe yarar:** Değişikliklerini takıma gösterir, tartışma ortamı sağlar, otomatik testlerin çalışmasını tetikler
**Gerçek hayat benzetmesi:** Bir makaleyi editöre göndermek -- editör okur, düzeltme ister, onaylarsa yayınlanır
:::

### PR Açma Adımları

:::code[bash]{title="PR Açma Workflow'u"}
# 1. Yeni bir feature branch oluştur
git checkout -b feat/user-authentication

# 2. Değişikliklerini yap ve commit et
git add .
git commit -m "feat: add user login form with validation"

# 3. Branch'i remote'a push et
git push -u origin feat/user-authentication

# 4. GitHub CLI ile PR oluştur
gh pr create \
  --title "feat: Add user authentication" \
  --body "## Summary
- Implemented login form with email/password validation
- Added JWT token storage
- Created auth context for React

## Test Plan
- [ ] Manual login test
- [ ] Invalid credentials test
- [ ] Token expiration test

Closes #42"
:::

### PR Best Practices

1. **Küçük ve odaklı PR'lar aç** -- 400+ satırlık PR kimse review etmek istemez. Büyük feature'ları küçük PR'lara böl.
2. **Açıklayıcı başlık ve açıklama yaz** -- "Fix bug" yerine "fix: resolve null pointer in user profile when avatar is missing" yaz.
3. **İlgili Issue'yu bağla** -- `Closes #42` veya `Fixes #15` gibi keyword'ler kullanarak Issue'yu otomatik kapat.
4. **Self-review yap** -- PR açmadan önce kendi diff'ini oku. Gereksiz console.log, yorum satırı veya debug kodu bırakma.
5. **Screenshot / Video ekle** -- UI değişikliklerinde önce-sonra screenshot'ları ekle.
6. **Draft PR kullan** -- Henüz bitmemiş çalışmalar için Draft PR aç, erken feedback al.

:::tip
PR açıklamasında bir template kullan. Summary, Changes, Test Plan ve Screenshots bölümleri standart bir PR template'in parçası olmalı. Repository'ne `.github/pull_request_template.md` dosyası ekleyerek bunu otomatikleştirebilirsin.
:::

## Code Review Kültürü

Code Review, sadece bug bulmak değil; bilgi paylaşmak, kod kalitesini yükseltmek ve takım standartlarını korumaktır.

### Review Yaparken Dikkat Edilecekler

:::code[text]{title="Code Review Checklist"}
1. Doğruluk (Correctness)
   - Kod beklenen işi yapıyor mu?
   - Edge case'ler düşünülmüş mü?
   - Null/undefined kontrolleri var mı?

2. Okunabilirlik (Readability)
   - Değişken ve fonksiyon isimleri anlamlı mı?
   - Karmaşık logic yeterince yorumlanmış mı?
   - Fonksiyonlar tek bir iş mi yapıyor?

3. Performans (Performance)
   - Gereksiz döngü veya N+1 query var mı?
   - Büyük veri setleri için pagination düşünülmüş mü?

4. Güvenlik (Security)
   - SQL injection, XSS riski var mı?
   - Hassas veri loglanıyor mu?
   - Input validation yapılmış mı?

5. Test (Testing)
   - Yeterli test yazılmış mı?
   - Edge case testleri var mı?
:::

### Yapıcı Feedback Verme

:::comparison
| Kötü Feedback | İyi Feedback |
|---------------|-------------|
| "Bu kod kötü" | "Bu fonksiyon 50 satır olmuş. Validation logic'ini ayrı bir helper'a ayırsak okunabilirlik artar. Ne dersin?" |
| "Neden böyle yaptın?" | "Burada Map yerine Object kullanmanın bir sebebi var mı? Map bu use case için daha performanslı olabilir." |
| "Yanlış" | "Bu koşul `user.role === 'admin'` yerine `user.isAdmin()` ile kontrol edilse, role string'i değiştiğinde tek yerde güncellememiz yeterli olur." |
| (Sessiz onay, sadece "LGTM") | "LGTM! Özellikle error handling yaklaşımını beğendim. Custom error class'ları çok temiz olmuş." |

**Tavsiye:** Review sırasında koddan değil, yaklaşımdan bahset. Kişiye değil, koda odaklan. "Sen hata yaptın" yerine "Bu yaklaşımda şu risk var" de.
:::

:::beginner-mistake
Yaygın hata: Code Review'u sadece approve/reject olarak görmek. Review bir öğrenme ve öğretme fırsatıdır. Junior developer'lar senior'ların kodunu review ederek öğrenir, senior'lar da farklı bakış açıları kazanır. Review isteğini reddetme -- her PR bir öğrenme fırsatı.
:::

## Conventional Commits

Conventional Commits, commit mesajlarına standart bir format getiren bir convention'dır. Otomatik changelog oluşturma ve semantic versioning ile entegre çalışır.

:::concept[Conventional Commits (İng: Conventional Commits)]
Conventional Commits, commit mesajlarının belirli bir kurala göre yazılmasını sağlayan bir standart formatıdır.

**Türkçe karşılığı:** Geleneksel Commit Formatı
**Ne işe yarar:** Commit geçmişini okunabilir ve otomatik işlenebilir (parseable) yapar
**Gerçek hayat benzetmesi:** E-posta konu satırı formatı gibi -- "[ACIL] Toplantı iptal" gibi önek kullanmak, mesajın türünü anında belli eder
:::

:::code[text]{title="Conventional Commits Formatı"}
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]

# Temel Tipler:
feat:      Yeni özellik (MINOR version artırır)
fix:       Bug düzeltmesi (PATCH version artırır)
docs:      Sadece dokümantasyon değişiklikleri
style:     Kod formatı değişiklikleri (boşluk, noktalama -- logic değişmez)
refactor:  Ne bug fix ne feature olan kod değişiklikleri
test:      Test ekleme veya düzeltme
chore:     Build sistemi, CI config veya yardımcı araç değişiklikleri
perf:      Performans iyileştirmesi
ci:        CI/CD konfigürasyon değişiklikleri
build:     Build sistemi veya dış bağımlılık değişiklikleri

# Breaking Change (MAJOR version artırır):
feat!: add new authentication system
# veya footer'da:
BREAKING CHANGE: API endpoint format changed
:::

:::code[bash]{title="Conventional Commits Örnekleri"}
# Yeni özellik
git commit -m "feat(auth): add Google OAuth login support"

# Bug düzeltmesi
git commit -m "fix(cart): resolve total calculation with discount codes"

# Dokümantasyon
git commit -m "docs: update API endpoint documentation for v2"

# Refactoring
git commit -m "refactor(user): extract validation logic into separate module"

# Test
git commit -m "test(payment): add integration tests for Stripe webhook"

# Chore
git commit -m "chore: upgrade dependencies to latest versions"

# Style
git commit -m "style: apply prettier formatting to all components"

# Breaking change
git commit -m "feat(api)!: change response format from XML to JSON"
:::

:::tip
Commitlint ve Husky kullanarak Conventional Commits formatını zorunlu kılabilirsin. Yanlış formatta commit mesajı yazıldığında commit reddedilir, böylece takım disiplini sağlanır.
:::

## Branch Protection ve CODEOWNERS

### Branch Protection Rules

Branch protection rules, belirli branch'lere doğrudan push yapılmasını engelleyerek kod kalitesini korur.

:::code[text]{title="Önerilen Branch Protection Ayarları (main branch)"}
Settings → Branches → Add rule → Branch name pattern: main

1. [x] Require a pull request before merging
   - [x] Require approvals: 1 (veya 2 for critical repos)
   - [x] Dismiss stale pull request approvals when new commits are pushed

2. [x] Require status checks to pass before merging
   - [x] Require branches to be up to date before merging
   - Status checks: CI test suite, linting, type checking

3. [x] Require conversation resolution before merging

4. [x] Require signed commits (opsiyonel, ama önerilir)

5. [x] Do not allow bypassing the above settings
:::

### CODEOWNERS

:::code[text]{title=".github/CODEOWNERS Dosyası"}
# CODEOWNERS dosyası, hangi dosyaların kimin onayını gerektirdiğini belirler
# PR açıldığında ilgili kişiler otomatik reviewer olarak atanır

# Genel kural: tüm dosyalar için
* @team-lead

# Frontend dosyaları
/src/components/    @frontend-team
/src/pages/         @frontend-team
*.tsx               @frontend-team

# Backend dosyaları
/src/api/           @backend-team
/src/services/      @backend-team

# Altyapı ve DevOps
/infrastructure/    @devops-team
/.github/workflows/ @devops-team
Dockerfile          @devops-team

# Kritik dosyalar: birden fazla onay gerektirir
/src/auth/          @security-team @team-lead
package.json        @team-lead
:::

## GitHub Issues, Projects ve Proje Yönetimi

### Issues

GitHub Issues, bug raporları, feature request'ler ve görevleri takip etmek için kullanılır.

:::code[markdown]{title="Issue Template Örneği: Bug Report"}
---
name: Bug Report
about: Report a bug to help us improve
labels: bug, triage
---

## Describe the Bug
A clear description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g. macOS 14.0]
- Browser: [e.g. Chrome 120]
- Version: [e.g. 2.1.0]
:::

### Projects (Kanban Board)

GitHub Projects, Issue'ları ve PR'ları Kanban board'unda organize etmeni sağlar.

:::code[text]{title="Tipik Kanban Kolonları"}
| Backlog | Todo | In Progress | In Review | Done |
|---------|------|-------------|-----------|------|
| Planlanan | Sıradaki | Üzerinde   | PR açılmış| Tamamlanan |
| görevler  | görevler | çalışılan  | review    | görevler   |
|           |          | görevler   | bekliyor  |            |
:::

### Labels ve Milestones

:::code[text]{title="Önerilen Label Sistemi"}
# Tür
bug           (kırmızı)   → Hata bildirimi
feature       (yeşil)     → Yeni özellik
enhancement   (mavi)      → Mevcut özellik iyileştirmesi
documentation (mor)       → Dokümantasyon

# Öncelik
priority:high   (turuncu) → Acil
priority:medium (sarı)    → Normal
priority:low    (gri)     → Düşük

# Durum
good first issue (açık yeşil) → Yeni katılımcılar için uygun
help wanted      (açık mor)   → Yardım aranıyor
wontfix          (beyaz)      → Düzeltilmeyecek

# Milestone örneği:
# v1.0.0 Release → Due date: 2026-04-01
# İçindeki issue'lar tamamlandığında milestone kapanır
:::

## GitHub Actions Temelleri

:::concept[GitHub Actions (İng: GitHub Actions)]
GitHub Actions, repository'deki olaylara (push, PR, schedule) tepki veren otomatik iş akışları (workflow) oluşturmanı sağlayan CI/CD platformudur.

**Türkçe karşılığı:** GitHub Eylemleri / Otomasyonları
**Ne işe yarar:** Test çalıştırma, build alma, deploy etme gibi tekrarlayan işleri otomatikleştirir
**Gerçek hayat benzetmesi:** Bir fabrikadaki montaj hattı gibi -- her adım otomatik olarak bir öncekinin bitiminde başlar
:::

:::code[yaml]{title=".github/workflows/ci.yml -- Temel CI Workflow"}
name: CI Pipeline

# Trigger: Ne zaman çalışsın?
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# Jobs: Hangi işler yapılsın?
jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      # Step 1: Kodu checkout et
      - name: Checkout code
        uses: actions/checkout@v4

      # Step 2: Node.js kur
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          # 📌 2026: pnpm kullanıyorsan cache: 'pnpm' ve pnpm/action-setup@v4 ekle
          cache: 'pnpm'

      - name: Setup pnpm
        uses: pnpm/action-setup@v4

      # Step 3: Bağımlılıkları yükle
      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      # Step 4: Linting
      - name: Run linter
        run: pnpm lint

      # Step 5: Type checking
      - name: Type check
        run: pnpm type-check

      # Step 6: Testleri çalıştır
      - name: Run tests
        run: pnpm test -- --coverage

      # Step 7: Build
      - name: Build project
        run: pnpm build

  deploy:
    name: Deploy to Production
    needs: test  # test job'u başarılı olmalı
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy
        run: echo "Deploying to production..."
        # Gerçek deploy komutları buraya gelir
:::

:::code[text]{title="GitHub Actions Temel Kavramlar"}
Workflow  → .github/workflows/ altındaki YAML dosyası
Trigger   → Workflow'u başlatan olay (push, PR, schedule, manual)
Job       → Bir sanal makinede çalışan iş birimi
Step      → Job içindeki tek bir adım (komut veya action)
Action    → Başkaları tarafından yazılmış tekrar kullanılabilir step
Runner    → Job'ların çalıştığı sanal makine (ubuntu, windows, macos)
Artifact  → Job'lar arasında paylaşılan dosyalar (test raporu, build çıktısı)
Secret    → Şifrelenmiş ortam değişkenleri (API key, token)

# Yaygın Trigger'lar:
on: push                          # Her push'ta
on: pull_request                  # Her PR'da
on: schedule: cron: '0 9 * * 1'  # Her Pazartesi 09:00'da
on: workflow_dispatch             # Manuel tetikleme
:::

## SSH Key ve Authentication

:::code[bash]{title="SSH Key Oluşturma ve GitHub'a Ekleme"}
# 1. SSH key oluştur
ssh-keygen -t ed25519 -C "email@example.com"
# Enter tuşuna bas (varsayılan konum: ~/.ssh/id_ed25519)
# Passphrase gir (opsiyonel ama önerilir)

# 2. SSH agent'ı başlat
eval "$(ssh-agent -s)"

# 3. Key'i agent'a ekle
ssh-add ~/.ssh/id_ed25519

# 4. Public key'i kopyala
cat ~/.ssh/id_ed25519.pub
# Windows: clip < ~/.ssh/id_ed25519.pub
# macOS:   pbcopy < ~/.ssh/id_ed25519.pub

# 5. GitHub'a ekle:
# GitHub → Settings → SSH and GPG Keys → New SSH Key
# Title: "My Laptop" gibi tanımlayıcı bir isim
# Key: Kopyaladığın public key'i yapıştır

# 6. Bağlantıyı test et
ssh -T git@github.com
# "Hi username! You've successfully authenticated..." mesajı almalısın
:::

:::beginner-mistake
Yaygın hata: HTTPS yerine SSH kullanmamak. HTTPS ile her push/pull'da kullanıcı adı ve token girmen gerekir (veya credential helper kurman gerekir). SSH key kurulumu bir kez yapılır ve sonra her işlem sorunsuz çalışır. Profesyonel iş ortamlarında SSH tercih edilir.
:::

## GitHub Pages ve Gist

### GitHub Pages

GitHub Pages, static web sitelerini doğrudan repository'den yayınlamana olanak tanır.

:::code[text]{title="GitHub Pages Kullanım Alanları"}
1. Kişisel portfolyo sitesi    → username.github.io
2. Proje dokümantasyonu         → username.github.io/project-name
3. Blog (Jekyll, Hugo ile)      → Static site generator'lar ile

# Etkinleştirme:
# Settings → Pages → Source: Deploy from a branch
# Branch: main (veya gh-pages), Folder: / (root) veya /docs
:::

### Gist

:::code[text]{title="Gist Kullanım Alanları"}
# Gist = Tek dosyalık mini repository
# Hızlıca kod paylaşmak için idealdir

# Kullanım senaryoları:
- Kod snippet'leri paylaşma
- Konfigürasyon dosyaları saklama
- Hızlı notlar ve cheatsheet'ler
- Markdown ile formatlanmış dökümanlar

# CLI ile Gist oluşturma:
gh gist create my-script.js --public --desc "Utility functions"
:::

## Açık Kaynak Katkı Workflow'u

Açık kaynak projelere katkıda bulunmak, hem öğrenme hem de profesyonel ağ kurma açısından kritik bir beceridir.

:::code[bash]{title="Açık Kaynak Katkı Adımları (Fork → Branch → PR)"}
# 1. CONTRIBUTING.md dosyasını oku (her projenin kuralları farklıdır)

# 2. Repository'yi fork et (GitHub web arayüzünde "Fork" butonu)

# 3. Fork'unu klonla
git clone git@github.com:SENIN_ADIN/proje.git
cd proje

# 4. Upstream remote ekle
git remote add upstream git@github.com:ORIJINAL_SAHIP/proje.git

# 5. Main branch'i güncel tut
git fetch upstream
git checkout main
git merge upstream/main

# 6. Feature branch oluştur (açıklayıcı isim ver)
git checkout -b fix/typo-in-readme

# 7. Değişikliklerini yap
# ... kod değişiklikleri ...

# 8. Conventional Commits ile commit et
git add .
git commit -m "fix: correct typo in installation instructions"

# 9. Fork'una push et
git push origin fix/typo-in-readme

# 10. GitHub'da orijinal repo'ya PR aç
# PR açıklamasında:
# - Ne değiştiğini açıkla
# - İlgili Issue varsa referans ver
# - CONTRIBUTING.md kurallarına uyduğunu belirt

# 11. Review feedback'ini uygula
# Maintainer'lar değişiklik isteyebilir
# Aynı branch'e yeni commit'ler ekle, PR otomatik güncellenir

# 12. PR merge edildikten sonra
git checkout main
git pull upstream main
git branch -d fix/typo-in-readme
:::

:::tip
İlk katkın için "good first issue" label'ına sahip issue'ları ara. Bu issue'lar yeni katkıda bulunanlar için tasarlanmıştır ve genellikle daha basit görevlerdir. GitHub'da `is:open is:issue label:"good first issue" language:javascript` şeklinde arama yapabilirsin.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: GitHub Repository ve SSH Kurulumu (Kolay)

GitHub hesabini yapilandir, SSH key olustur ve ilk repository'ni push et.

```bash
# 1. SSH key olustur
ssh-keygen -t ed25519 -C "senin@email.com"
# Enter'a bas (varsayilan konum)
# Passphrase gir (opsiyonel ama onerilir)

# 2. Public key'i kopyala
cat ~/.ssh/id_ed25519.pub
# Bu ciktiyi GitHub > Settings > SSH Keys > New SSH Key'e yapistir

# 3. Baglantiyi test et
ssh -T git@github.com
# "Hi username! You've successfully authenticated" mesaji gelmeli

# 4. Yeni repo olustur ve push et
mkdir my-first-repo && cd my-first-repo && git init
echo "# Ilk Repom" > README.md
echo "node_modules/" > .gitignore
git add . && git commit -m "initial commit"

# 5. GitHub'da repo olustur (github.com/new) sonra:
git remote add origin git@github.com:USERNAME/my-first-repo.git
git push -u origin main

# 6. Dogrula
git remote -v  # origin URL'ini goster
git log --oneline  # push edilen commit'i gor
```

**Beklenen Sonuc:** SSH ile GitHub'a basariyla baglanmali. Repository GitHub'da gorunmeli. `git remote -v` dogru URL'i gostermeli.
**Ipucu:** SSH key zaten varsa yeniden olusturmana gerek yok. `ls ~/.ssh/` ile kontrol et.

---

### Alistirma 2: Pull Request Workflow (Orta)

Bir feature branch olustur, degisiklik yap, GitHub'a push et ve Pull Request ac.

```bash
# 1. Onceki repo'da devam et (veya yeni bir repo clone et)
cd my-first-repo

# 2. Feature branch olustur
git checkout -b feature/add-about-page

# 3. Degisiklikler yap
cat > about.html << 'EOF'
<!DOCTYPE html>
<html lang="tr">
<head><title>Hakkimda</title></head>
<body>
  <h1>Hakkimda</h1>
  <p>Junior Full-Stack Developer</p>
</body>
</html>
EOF

# README'ye de bir sey ekle
echo -e "\n## Sayfalar\n- [Hakkimda](about.html)" >> README.md

# 4. Conventional Commit ile commit et
git add about.html && git commit -m "feat: add about page"
git add README.md && git commit -m "docs: add pages section to README"

# 5. Branch'i GitHub'a push et
git push -u origin feature/add-about-page

# 6. GitHub'da PR ac:
# - github.com/USERNAME/my-first-repo adresine git
# - "Compare & pull request" butonuna tikla
# - PR basligi: "feat: Add about page"
# - Aciklama yaz: Ne degisti, neden degisti
# - "Create pull request" tikla

# 7. PR'i incele ve merge et (GitHub web arayuzunden)
```

**Beklenen Sonuc:** GitHub'da PR basariyla acilmali. PR sayfasinda dosya degisiklikleri gorunmeli. Merge sonrasi main branch guncel olmali.
**Ipucu:** PR aciklamasinda "Closes #issue-number" yazarsan, merge sonrasi issue otomatik kapanir.

---

### Alistirma 3: GitHub Actions ile CI Pipeline (Zor)

Basit bir CI workflow olustur: her push'ta lint ve test calistiran bir GitHub Actions pipeline yaz.

```yaml
# .github/workflows/ci.yml dosyasini olustur:
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      # TODO: Asagidaki adimlari tamamla:
      # - name: Install dependencies
      #   run: npm ci
      #
      # - name: Run linter
      #   run: npm run lint
      #
      # - name: Run tests
      #   run: npm test

      - name: Build check
        run: echo "Build basarili!"
```

```bash
# 1. Workflow dosyasini olustur
mkdir -p .github/workflows
# Yukaridaki YAML'i .github/workflows/ci.yml olarak kaydet

# 2. Commit ve push et
git add .github/ && git commit -m "ci: add GitHub Actions workflow"
git push origin main

# 3. GitHub > Actions tab'inda workflow'un calistigini gor
# 4. Yesil tik (basarili) veya kirmizi X (basarisiz) gorunmeli

# BONUS: PR actiginda workflow otomatik calisir mi? Test et:
git checkout -b test/ci-trigger
echo "test" > test.txt && git add . && git commit -m "test: trigger CI"
git push -u origin test/ci-trigger
# GitHub'da PR ac ve Actions tab'ini kontrol et
```

**Beklenen Sonuc:** Her push ve PR'da workflow otomatik tetiklenmeli. Actions tab'inda calisma logu gorunmeli. Basarili ise yesil tik, basarisiz ise kirmizi X gorunmeli.
**Ipucu:** Workflow dosyasi `.github/workflows/` dizininde olmali ve `.yml` uzantili olmali. `on` bolumunde hangi event'lerde calisacagini belirtirsin.
:::

:::knowledge-check
type: multiple_choice
question: "Conventional Commits formatında, mevcut bir API endpoint'inin response yapısını değiştiren (breaking change) bir commit nasıl yazılır?"
options:
  - "breaking: change API response format"
  - "feat!: change API response format"
  - "fix: BREAKING CHANGE change API response format"
  - "change: update API response format"
correct: 1
explanation: "Breaking change, commit tipinden sonra ünlem işareti (!) ile belirtilir: feat!:, fix!: gibi. Alternatif olarak commit body'sinde BREAKING CHANGE: footer'ı kullanılabilir."
:::

:::knowledge-check
type: multiple_choice
question: "GitHub Actions workflow dosyası nereye konulmalıdır?"
options:
  - "Projenin root dizinine (.github-actions.yml)"
  - ".github/workflows/ dizinine (.yml uzantılı dosya)"
  - "package.json içine actions bölümüne"
  - ".github/ dizinine (actions.json)"
correct: 1
explanation: "GitHub Actions workflow dosyaları .github/workflows/ dizini altına YAML formatında (.yml veya .yaml) konulmalıdır. GitHub bu dizini otomatik olarak tarar ve workflow'ları tanır."
:::

:::knowledge-check
type: multiple_choice
question: "Bir açık kaynak projeye katkıda bulunurken doğru sıra hangisidir?"
options:
  - "Clone → Branch → Commit → Push → PR"
  - "Fork → Clone → Branch → Commit → Push → PR"
  - "Branch → Fork → Clone → Commit → PR"
  - "Fork → Branch → Commit → Clone → PR"
correct: 1
explanation: "Açık kaynak katkı workflow'u: Önce Fork (kendi hesabına kopyala), sonra Clone (lokale indir), Branch oluştur, Commit yap, Push et ve orijinal repoya PR aç. Fork adımı kritiktir çünkü başkasının repo'suna doğrudan push yapamazsın."
:::

:::ai-guidance
title: Bu Derste AI ile Öğren
content: GitHub workflow'larini, PR best practice'lerini ve CI/CD pipeline kurulumunu AI destegi ile ogrenip uygula.
model_recommendation: Claude Sonnet 4.5
prompts:
  - prompt: "Profesyonel bir Pull Request nasil yazilir? Baslik, aciklama, test plani ve screenshot'lar dahil ornek bir PR template olustur. Code Review sirasinda yapici feedback verme ornekleri goster."
    why: "PR kalitesi profesyonel yazilim gelistirmenin temel olcutudur. Iyi PR yazmak hem kod kalitesini hem de takim iletisimini guclendirir."
    follow_up: "GitHub Actions ile basit bir CI pipeline yazalim: push'ta lint, type-check ve test calistirsin. YAML syntax'ini ve her adimdaki mantigi acikla."
  - prompt: "Bir acik kaynak projeye katkida bulunmak istiyorum. Fork, clone, upstream ekleme, branch olusturma, commit, push ve PR acma adimlarini sirala. CONTRIBUTING.md okuma ve 'good first issue' bulma ipuclari ver."
    why: "Acik kaynak katki deneyimi portfolyo icin cok degerli ve is mulakatlarinda avantaj saglar."
pair_programming_tip: "GitHub Actions workflow'u yazarken AI'a YAML dosyani yapistir: 'Bu CI pipeline'i incele. Eksik adimlar var mi? Cache kullanimi optimize edilebilir mi? Matrix strategy ile birden fazla Node versiyonunda test calistirmali miyim?'"
:::

:::interview
## Mulakat Sorulari

**Soru 1: Pull Request (PR) review surecinde nelere dikkat edersiniz?**
- **Junior cevabi:** Kodun calisip calismadigina ve syntax hatarina bakarim.
- **Senior cevabi:** Iyi bir PR review'da: 1) Is mantigi dogru mu (requirements karsilaniyor mu), 2) Edge case'ler handle ediliyor mu, 3) Test coverage yeterli mi, 4) Naming convention ve kod standartlarina uyuluyor mu, 5) Performance impact var mi, 6) Security vulnerability olusturuyor mu, 7) Breaking change var mi. Ayrica PR boyutu 200-400 satiri gecmemeli, buyuk degisiklikler parca parca review edilmeli. LGTM (Looks Good To Me) demek sorumluluk almak demektir.

**Soru 2: GitHub Actions ile CI/CD pipeline nasil kurulur?**
- **Junior cevabi:** YAML dosyasiyla test ve deploy islemlerini otomatiklestiririz.
- **Senior cevabi:** `.github/workflows/` altinda YAML dosyalari ile tanimlanir. Temel pipeline: PR acildiginda lint + test + build calisir, main'e merge edildiginde deploy tetiklenir. Matrix strategy ile birden fazla Node/Python versiyonunda test edilir. Cache kullanarak (actions/cache) CI suresi %50-70 azaltilir. Branch protection rules ile CI gecmeyen PR'lar merge edilemez. Secrets management ile API key'ler guvenli saklanir. Self-hosted runner'lar ile ozel ortamlarda calistirilabilir.
:::

:::exercise
### Alıştırma 4: GitHub Actions CI Pipeline

**Görev:** Bir Node.js projesi için basit bir GitHub Actions CI pipeline'ı yaz.

**Başlangıç kodu:**
```yaml
# .github/workflows/ci.yml dosyasini olustur
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      # TODO: Node.js kur
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      # TODO: Bagimliliklari yukle
      - name: Install dependencies
        run: npm ci

      # TODO: Lint calistir
      - name: Lint
        run: npm run lint

      # TODO: Testleri calistir
      - name: Test
        run: npm test

      # TODO: Build
      - name: Build
        run: npm run build
```

**Beklenen çıktı:**
```
CI Pipeline calisiyor:
  Node 18: Lint OK, Test OK, Build OK
  Node 20: Lint OK, Test OK, Build OK
  Node 22: Lint OK, Test OK, Build OK
```

**İpucu:** `npm ci` `npm install`'dan daha hızlıdır ve `package-lock.json`'ı birebir kullanır. `strategy.matrix` ile birden fazla versiyonda test edilir.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: PR Template Oluşturma

**Görev:** Profesyonel bir Pull Request template'i ve Issue template'leri oluştur.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir github-templates && cd github-templates && git init

# PR template
mkdir -p .github
cat > .github/pull_request_template.md << 'EOF'
## Degisiklik Ozeti
<!-- Bu PR ne yapiyor? Neden gerekli? -->


## Degisiklik Tipi
- [ ] Bug fix (mevcut davranisi duzeltir)
- [ ] Yeni ozellik (yeni islevsellik ekler)
- [ ] Refactoring (davranisi degistirmeden kodu iyilestirir)
- [ ] Dokumantasyon
- [ ] Test ekleme/duzeltme

## Test Plani
<!-- Bu degisikligi nasil test ettin? -->
- [ ] Unit testler eklendi/guncellendi
- [ ] Manuel test yapildi
- [ ] Mevcut testler hala geciyor

## Checklist
- [ ] Kodum lint kurallarini geciyor
- [ ] Self-review yaptim
- [ ] Gerekli yorumlari ekledim
- [ ] Dokumantasyonu guncelledim
- [ ] Degisikliklerim yeni uyari/hata uretmiyor

## Ekran Goruntuleri (varsa)
<!-- UI degisiklikleri icin once/sonra ekran goruntuleri -->

## Iliskili Issue
<!-- Closes #123 veya Fixes #456 -->
EOF

# Bug report template
# TODO: .github/ISSUE_TEMPLATE/bug_report.md olustur
mkdir -p .github/ISSUE_TEMPLATE
cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug Report
about: Bir hata bildirmek icin
title: '[BUG] '
labels: bug
---

## Hata Aciklamasi
<!-- Net ve kisa bir aciklama -->

## Tekrarlama Adimlari
1. '...' sayfasina git
2. '...' butonuna tikla
3. Hata gorunur

## Beklenen Davranis
<!-- Ne olmasini bekliyordun? -->

## Gerceklesen Davranis
<!-- Ne oldu? -->

## Ortam Bilgileri
- OS: [ornegin macOS 14.2]
- Browser: [ornegin Chrome 120]
- Node: [ornegin v20.10.0]
EOF

git add . && git commit -m "chore: add PR and issue templates"

echo "=== Olusturulan dosyalar ==="
find .github -type f
```

**Beklenen çıktı:**
```
=== Olusturulan dosyalar ===
.github/pull_request_template.md
.github/ISSUE_TEMPLATE/bug_report.md
```

**İpucu:** GitHub PR template'i her yeni PR açıldığında otomatik doldurulur. Issue template'leri kullanıcıyı doğru formatta bilgi vermeye yönlendirir.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 6: gh CLI ile GitHub İşlemleri

**Görev:** GitHub CLI (`gh`) kullanarak repo, issue ve PR işlemlerini terminalden yönet.

**Başlangıç kodu:**
```bash
#!/bin/bash

# gh CLI komutlari (gercek bir repo'da calistir)

echo "=== Repo Bilgileri ==="
# gh repo view --json name,description,stargazerCount

echo -e "\n=== Issue Islemleri ==="
# Yeni issue olustur
# gh issue create --title "Bug: Login sayfasi cokiyor" \
#   --body "Login sayfasinda form submit edildiginde 500 hatasi" \
#   --label "bug" --assignee "@me"

# Issue listele
# gh issue list --state open --label "bug"

# Issue kapat
# gh issue close 1 --reason "completed" --comment "Fix merged in PR #5"

echo -e "\n=== PR Islemleri ==="
# PR olustur
# gh pr create --title "feat: add user dashboard" \
#   --body "## Ozet\n- Dashboard component eklendi\n- API entegrasyonu yapildi" \
#   --base main --head feature/dashboard \
#   --reviewer "teammate1,teammate2"

# PR listele
# gh pr list --state open

# PR review et
# gh pr review 5 --approve --body "LGTM!"

# PR merge et
# gh pr merge 5 --squash --delete-branch

echo -e "\n=== Workflow/Actions ==="
# Workflow calistir
# gh workflow run ci.yml

# Workflow durumu
# gh run list --limit 5

# Workflow loglarini gor
# gh run view <run-id> --log

echo -e "\n=== Faydali Kisa Yollar ==="
echo "gh repo clone owner/repo     # Repo clone et"
echo "gh pr checkout 42            # PR'in branch'ini checkout et"
echo "gh pr diff                   # Mevcut PR'in diff'ini gor"
echo "gh issue view 15 --web       # Issue'yu tarayicida ac"
echo "gh api repos/{owner}/{repo}  # GitHub API'yi direkt cagir"
```

**Beklenen çıktı:**
```
=== Faydali Kisa Yollar ===
gh repo clone owner/repo     # Repo clone et
gh pr checkout 42            # PR'in branch'ini checkout et
gh pr diff                   # Mevcut PR'in diff'ini gor
gh issue view 15 --web       # Issue'yu tarayicida ac
gh api repos/{owner}/{repo}  # GitHub API'yi direkt cagir
```

**İpucu:** `gh auth login` ile ilk kez giriş yap. `gh auth status` ile durumu kontrol et.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 7: Branch Protection Rules Simülasyonu

**Görev:** Bir branch protection rule konfigürasyonu oluştur ve kuralları test et.

**Başlangıç kodu:**
```bash
#!/bin/bash

# Branch protection kurallarini simule eden bir script
cat > branch_protection.json << 'EOF'
{
  "branch": "main",
  "rules": {
    "require_pull_request": true,
    "required_approvals": 2,
    "dismiss_stale_reviews": true,
    "require_status_checks": ["ci/test", "ci/lint", "ci/build"],
    "require_branches_up_to_date": true,
    "enforce_admins": true,
    "restrict_pushes": true,
    "allow_force_push": false,
    "allow_deletions": false,
    "require_signed_commits": false,
    "require_linear_history": true
  }
}
EOF

# Protection rule kontrolcusu
cat > check_protection.py << 'PYTHON'
import json

def check_merge_allowed(rules: dict, pr: dict) -> dict:
    """PR'in merge edilip edilemeyecegini kontrol et."""
    errors = []

    # TODO: Her kurali kontrol et
    if rules["require_pull_request"] and not pr.get("is_pr"):
        errors.append("Direct push not allowed - PR required")

    if pr.get("approvals", 0) < rules["required_approvals"]:
        errors.append(f"Need {rules['required_approvals']} approvals, have {pr.get('approvals', 0)}")

    failed_checks = [c for c in rules["require_status_checks"] if c not in pr.get("passed_checks", [])]
    if failed_checks:
        errors.append(f"Status checks failing: {', '.join(failed_checks)}")

    if rules["require_branches_up_to_date"] and not pr.get("up_to_date"):
        errors.append("Branch is not up to date with base")

    return {"allowed": len(errors) == 0, "errors": errors}

# Test senaryolari
with open("branch_protection.json") as f:
    config = json.load(f)

test_prs = [
    {"name": "Tam uyumlu PR", "is_pr": True, "approvals": 2, "passed_checks": ["ci/test", "ci/lint", "ci/build"], "up_to_date": True},
    {"name": "Eksik onay", "is_pr": True, "approvals": 1, "passed_checks": ["ci/test", "ci/lint", "ci/build"], "up_to_date": True},
    {"name": "CI basarisiz", "is_pr": True, "approvals": 2, "passed_checks": ["ci/test"], "up_to_date": True},
    {"name": "Direct push", "is_pr": False, "approvals": 0, "passed_checks": [], "up_to_date": True},
]

for pr in test_prs:
    result = check_merge_allowed(config["rules"], pr)
    status = "ALLOWED" if result["allowed"] else "BLOCKED"
    print(f"\n{pr['name']}: {status}")
    for error in result["errors"]:
        print(f"  - {error}")
PYTHON

python3 check_protection.py
```

**Beklenen çıktı:**
```
Tam uyumlu PR: ALLOWED

Eksik onay: BLOCKED
  - Need 2 approvals, have 1

CI basarisiz: BLOCKED
  - Status checks failing: ci/lint, ci/build

Direct push: BLOCKED
  - Direct push not allowed - PR required
  - Need 2 approvals, have 0
  - Status checks failing: ci/test, ci/lint, ci/build
```

**İpucu:** GitHub'da Settings > Branches > Branch protection rules'dan bu kuralları yapılandırabilirsin.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Git Hooks ile Conventional Commits

**Görev:** Commit mesajlarının Conventional Commits formatına uygunluğunu kontrol eden bir commit-msg hook yaz.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir conventional-lab && cd conventional-lab && git init

# commit-msg hook
cat > .git/hooks/commit-msg << 'HOOK'
#!/bin/bash

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Conventional Commits formati:
# type(scope): description
# type: feat, fix, docs, style, refactor, test, chore, ci, perf, build
# scope: opsiyonel
# description: kucuk harfle baslar, nokta ile bitmez

PATTERN="^(feat|fix|docs|style|refactor|test|chore|ci|perf|build)(\([a-z]+\))?: .{1,72}$"

if ! echo "$COMMIT_MSG" | head -1 | grep -qE "$PATTERN"; then
    echo "HATA: Commit mesaji Conventional Commits formatina uymuyor!"
    echo ""
    echo "Dogru format: type(scope): description"
    echo ""
    echo "Tipler: feat, fix, docs, style, refactor, test, chore, ci, perf, build"
    echo ""
    echo "Ornekler:"
    echo "  feat(auth): add login page"
    echo "  fix(api): resolve timeout issue"
    echo "  docs: update README"
    echo "  refactor(db): simplify query builder"
    echo ""
    echo "Mevcut mesaj: '$COMMIT_MSG'"
    exit 1
fi
HOOK
chmod +x .git/hooks/commit-msg

# Test: Gecerli commit'ler
echo "code" > app.js && git add .
git commit -m "feat(auth): add login functionality" && echo "OK: feat"

echo "fix" >> app.js && git add .
git commit -m "fix: resolve null pointer error" && echo "OK: fix"

echo "docs" >> app.js && git add .
git commit -m "docs(api): update endpoint documentation" && echo "OK: docs"

# Test: Gecersiz commit'ler
echo "bad" >> app.js && git add .
git commit -m "added some stuff" 2>&1 || echo "REDDEDILDI: format yok"

echo "bad2" >> app.js && git add .
git commit -m "FEAT: uppercase type" 2>&1 || echo "REDDEDILDI: buyuk harf"

echo "=== Basarili commit'ler ==="
git log --oneline
```

**Beklenen çıktı:**
```
OK: feat
OK: fix
OK: docs
HATA: Commit mesaji Conventional Commits formatina uymuyor!
REDDEDILDI: format yok
HATA: Commit mesaji Conventional Commits formatina uymuyor!
REDDEDILDI: buyuk harf

=== Basarili commit'ler ===
abc1234 docs(api): update endpoint documentation
def5678 fix: resolve null pointer error
ghi9012 feat(auth): add login functionality
```

**İpucu:** `grep -qE` extended regex ile sessiz kontrol yapar. Commit mesajının ilk satırı 72 karakteri geçmemeli.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: Fork ve Upstream Sync Workflow

**Görev:** Açık kaynak projeye katkıda bulunma iş akışını simüle et: fork, branch, commit, PR ve upstream sync.

**Başlangıç kodu:**
```bash
#!/bin/bash

# Upstream repo simulasyonu
mkdir upstream-repo && cd upstream-repo && git init --bare
cd ..

# "Fork" olustur (clone)
git clone upstream-repo forked-repo
cd forked-repo

# Baslangic commit
echo "# Open Source Project" > README.md
echo "v1" > app.js
git add . && git commit -m "initial: project setup"
git push origin main

# Fork'u simule et (ikinci clone)
cd ..
git clone upstream-repo my-fork
cd my-fork

# Upstream remote ekle
git remote add upstream ../upstream-repo

echo "=== Remote'lar ==="
git remote -v

# Feature branch olustur
git checkout -b feature/improve-docs

cat >> README.md << 'EOF'

## Kurulum
npm install

## Kullanim
npm start
EOF
git add . && git commit -m "docs: add installation and usage sections"

echo -e "\n=== Feature branch push ==="
# git push origin feature/improve-docs
echo "git push origin feature/improve-docs"

# Upstream'de degisiklik oldu (baska birisi commit atti)
cd ../forked-repo
echo "v2 - updated" > app.js
git add . && git commit -m "feat: update to v2"
git push origin main
cd ../my-fork

# GOREV: Upstream ile sync ol
echo -e "\n=== Upstream Sync ==="
echo "1. git fetch upstream"
echo "2. git checkout main"
echo "3. git merge upstream/main"
echo "4. git push origin main"
echo "5. git checkout feature/improve-docs"
echo "6. git rebase main  (feature branch'i guncelle)"

git fetch upstream 2>/dev/null || git fetch origin
git checkout main
git merge origin/main 2>/dev/null
echo "Sync tamamlandi!"
```

**Beklenen çıktı:**
```
=== Remote'lar ===
origin    ../upstream-repo (fetch)
origin    ../upstream-repo (push)
upstream  ../upstream-repo (fetch)
upstream  ../upstream-repo (push)

=== Upstream Sync ===
1. git fetch upstream
2. git checkout main
3. git merge upstream/main
...
Sync tamamlandi!
```

**İpucu:** `upstream` = orijinal repo, `origin` = senin fork'un. Düzenli olarak `git fetch upstream && git merge upstream/main` ile güncel kal.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: GitHub API ile Repo Analizi

**Görev:** GitHub API ve `gh` CLI kullanarak bir repo'nun istatistiklerini çıkaran bir script yaz.

**Başlangıç kodu:**
```bash
#!/bin/bash

# GitHub API ile repo analizi (gh CLI gerekli)
REPO="${1:-facebook/react}"

echo "=== $REPO Analizi ==="

# 1. Repo bilgileri
echo -e "\n--- Repo Bilgileri ---"
# gh api repos/$REPO --jq '.full_name, .description, .stargazers_count, .forks_count, .language'
echo "Stars: (gh api ile alinir)"
echo "Forks: (gh api ile alinir)"

# 2. Son 5 release
echo -e "\n--- Son 5 Release ---"
# gh api repos/$REPO/releases --jq '.[:5] | .[] | "\(.tag_name) - \(.published_at[:10])"'
echo "(gh api repos/$REPO/releases komutu ile)"

# 3. Acik issue sayisi
echo -e "\n--- Issue Istatistikleri ---"
# gh api repos/$REPO --jq '"Open issues: \(.open_issues_count)"'
echo "(gh api ile alinir)"

# 4. En cok katki yapanlar
echo -e "\n--- Top 5 Contributor ---"
# gh api repos/$REPO/contributors --jq '.[:5] | .[] | "\(.login): \(.contributions) commit"'
echo "(gh api repos/$REPO/contributors komutu ile)"

# 5. Haftalik commit aktivitesi
echo -e "\n--- Haftalik Aktivite ---"
# gh api repos/$REPO/stats/participation --jq '.all[-4:]'

# Python ile analiz (opsiyonel)
cat > analyze_repo.py << 'PYTHON'
import json
import subprocess

def get_repo_stats(repo: str) -> dict:
    """gh CLI ile repo istatistiklerini al."""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}", "--jq",
             '{name: .name, stars: .stargazers_count, forks: .forks_count, issues: .open_issues_count, language: .language}'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    return {"name": repo, "stars": "N/A", "forks": "N/A", "issues": "N/A", "language": "N/A"}

# Test
stats = get_repo_stats("facebook/react")
print(f"\nRepo: {stats['name']}")
print(f"Stars: {stats['stars']}")
print(f"Forks: {stats['forks']}")
print(f"Open Issues: {stats['issues']}")
print(f"Language: {stats['language']}")
PYTHON

python3 analyze_repo.py 2>/dev/null || echo "(Python veya gh CLI kurulu degilse calismaz)"
```

**Beklenen çıktı:**
```
=== facebook/react Analizi ===

--- Repo Bilgileri ---
Stars: 230000+
Forks: 47000+

--- Top 5 Contributor ---
(gh api repos/facebook/react/contributors komutu ile)
```

**İpucu:** `gh api` doğrudan GitHub REST API'ye erişim sağlar. `--jq` flag'i ile JSON çıktıyı filtrele. Authentication `gh auth login` ile yapılır.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Changelog Otomatik Oluşturucu

**Görev:** Conventional Commits formatındaki git geçmişinden otomatik CHANGELOG oluşturan bir script yaz.

**Başlangıç kodu:**
```python
import subprocess
import re
from collections import defaultdict

def get_commits(since_tag: str = "") -> list[dict]:
    """Git log'dan commit'leri al."""
    cmd = ["git", "log", "--oneline", "--format=%s"]
    if since_tag:
        cmd.append(f"{since_tag}..HEAD")
    result = subprocess.run(cmd, capture_output=True, text=True)
    commits = []
    pattern = r"^(feat|fix|docs|style|refactor|test|chore|ci|perf|build)(\([\w-]+\))?: (.+)$"
    for line in result.stdout.strip().split("\n"):
        match = re.match(pattern, line)
        if match:
            commits.append({
                "type": match.group(1),
                "scope": match.group(2)[1:-1] if match.group(2) else None,
                "message": match.group(3),
            })
    return commits

def generate_changelog(commits: list[dict], version: str) -> str:
    """Commit'lerden CHANGELOG olustur."""
    sections = defaultdict(list)
    type_labels = {
        "feat": "Yeni Ozellikler",
        "fix": "Hata Duzeltmeleri",
        "docs": "Dokumantasyon",
        "refactor": "Refactoring",
        "perf": "Performans",
        "test": "Testler",
    }
    for c in commits:
        label = type_labels.get(c["type"], "Diger")
        scope = f"**{c['scope']}:** " if c["scope"] else ""
        sections[label].append(f"- {scope}{c['message']}")

    lines = [f"## [{version}] - 2026-03-22\n"]
    for section, items in sections.items():
        lines.append(f"### {section}\n")
        lines.extend(items)
        lines.append("")
    return "\n".join(lines)

# Test (simule edilmis veri)
test_commits = [
    {"type": "feat", "scope": "auth", "message": "add login page"},
    {"type": "feat", "scope": "api", "message": "add user endpoints"},
    {"type": "fix", "scope": "auth", "message": "fix token expiration"},
    {"type": "docs", "scope": None, "message": "update README"},
    {"type": "refactor", "scope": "db", "message": "simplify query builder"},
]

changelog = generate_changelog(test_commits, "1.2.0")
print(changelog)
```

**Beklenen çıktı:**
```
## [1.2.0] - 2026-03-22

### Yeni Ozellikler
- **auth:** add login page
- **api:** add user endpoints

### Hata Duzeltmeleri
- **auth:** fix token expiration

### Dokumantasyon
- update README

### Refactoring
- **db:** simplify query builder
```

**İpucu:** `git log --format=%s` sadece commit mesajlarını verir. Regex ile Conventional Commits formatını parse et.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 12: GitHub Release Otomasyonu

**Görev:** Semantic versioning ile otomatik release oluşturan bir script yaz.

**Başlangıç kodu:**
```bash
#!/bin/bash

# Mevcut versiyonu al
get_current_version() {
    git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0"
}

# Sonraki versiyonu hesapla
next_version() {
    local current=$1
    local bump_type=$2  # major, minor, patch

    # v prefix'ini kaldir
    current=${current#v}
    IFS='.' read -r major minor patch <<< "$current"

    case $bump_type in
        major) echo "v$((major + 1)).0.0" ;;
        minor) echo "v${major}.$((minor + 1)).0" ;;
        patch) echo "v${major}.${minor}.$((patch + 1))" ;;
    esac
}

# Commit'lerden bump tipini belirle
determine_bump() {
    local since=${1:-$(get_current_version)}
    if git log "$since"..HEAD --oneline | grep -qE "^.+ feat!|BREAKING CHANGE"; then
        echo "major"
    elif git log "$since"..HEAD --oneline | grep -qE "^.+ feat"; then
        echo "minor"
    else
        echo "patch"
    fi
}

# Test
echo "=== Semantic Versioning ==="
echo "Mevcut: $(get_current_version)"

for bump in patch minor major; do
    echo "  $bump bump: $(next_version "v1.2.3" $bump)"
done

echo -e "\n=== Release Adimlari ==="
echo "1. VERSION=$(next_version \$(get_current_version) \$(determine_bump))"
echo '2. git tag -a $VERSION -m "Release $VERSION"'
echo '3. git push origin $VERSION'
echo '4. gh release create $VERSION --generate-notes'
```

**Beklenen çıktı:**
```
=== Semantic Versioning ===
Mevcut: v0.0.0
  patch bump: v1.2.4
  minor bump: v1.3.0
  major bump: v2.0.0

=== Release Adimlari ===
1. VERSION=...
2. git tag -a $VERSION -m "Release $VERSION"
3. git push origin $VERSION
4. gh release create $VERSION --generate-notes
```

**İpucu:** Semantic Versioning: `MAJOR.MINOR.PATCH`. Breaking change = major, yeni özellik = minor, bug fix = patch. `gh release create` GitHub release oluşturur.

**Zorluk:** Zor
:::

:::must-note
- Git = versiyon kontrol aracı (lokal), GitHub = bulut platform (remote + iş birliği araçları)
- Fork = GitHub'da kendi hesabına kopya, Clone = lokal bilgisayara indirme. Açık kaynak katkıda: Fork, sonra Clone
- PR best practices: Küçük ve odaklı ol, açıklayıcı başlık yaz, self-review yap, Issue bağla (Closes #42)
- Code Review: Koda odaklan kişiye değil. Yapıcı feedback ver. "Bu yaklaşımda risk" de, "Sen hata yaptın" deme
- Conventional Commits tipleri: feat (yeni), fix (düzeltme), docs, style, refactor, test, chore, perf, ci, build
- Breaking change: `feat!:` veya footer'da `BREAKING CHANGE:` ile belirtilir
- Branch protection: PR zorunlu, approval gerekli, status check'ler geçmeli, stale approval dismiss edilmeli
- CODEOWNERS: Hangi dosya kimin onayını gerektirir -- otomatik reviewer atanır
- GitHub Actions: `.github/workflows/*.yml` dosyaları, on (trigger) + jobs + steps yapısı
- Actions trigger'lar: push, pull_request, schedule (cron), workflow_dispatch (manuel)
- SSH key: `ssh-keygen -t ed25519` ile oluştur, public key'i GitHub'a ekle, `ssh -T git@github.com` ile test et
- GitHub Pages: Static site hosting (username.github.io), Gist: Tek dosyalık mini repo (snippet paylaşımı)
- Açık kaynak katkı sırası: CONTRIBUTING.md oku, Fork, Clone, upstream ekle, branch oluştur, commit, push, PR aç
- İlk katkı için "good first issue" label'lı issue'ları ara
:::

:::senior-learns
Bir Senior Developer veya CTO, GitHub ve takım iş birliği konusunu öğrenirken şu yaklaşımı benimser:

1. **Trunk-based development vs GitFlow'u karşılaştırır** -- Hangi branching stratejisinin hangi takım büyüklüğü ve release döngüsü için uygun olduğunu deneyimleyerek öğrenir. Küçük takımlar için trunk-based, büyük ve kompleks projeler için GitFlow veya GitHub Flow tercih eder.

2. **PR Review süresini metrik olarak takip eder** -- PR'ların ortalama review süresini, merge time'ını ve review cycle sayısını ölçer. "PR açıldıktan sonra 24 saat içinde ilk review yapılmalı" gibi SLA'lar belirler. Uzun süre açık kalan PR'lar teknik borç kaynağıdır.

3. **GitHub Actions'ı sadece CI/CD değil, geliştirici deneyimi (DX) için de kullanır** -- Auto-labeling, stale issue kapatma, dependency update (Dependabot), release note oluşturma, PR size check gibi otomasyon workflow'ları kurar. Developer'ların manuel yapması gereken her tekrarlayan iş bir Action adayıdır.

4. **Monorepo ve multi-repo stratejilerini değerlendirir** -- Projenin ölçeğine göre monorepo (Nx, Turborepo) veya multi-repo yapısını seçer. CODEOWNERS dosyasını monorepo'larda takım sınırlarını belirlemek için kullanır.

5. **Inner source kültürü oluşturur** -- Şirket içi projeleri açık kaynak prensipleriyle yönetir: PR zorunluluğu, Code Review kültürü, CONTRIBUTING.md, iyi dokümantasyon. Her ekip, diğer ekiplerin projelerine PR açabilmelidir.

6. **Security-first yaklaşım benimser** -- GitHub Advanced Security, Dependabot alerts, secret scanning ve code scanning'i aktif eder. `.env` dosyalarının commit edilmesini `.gitignore` ve pre-commit hook'larla engeller. Leaked secret'ları anında rotate eder.

**Profesyonel Mindset:** "GitHub sadece bir araç değil, takımın yazılım mühendisliği olgunluk seviyesinin göstergesidir. Branch protection olmayan bir repo, kilidi olmayan bir kapı gibidir. Code Review yapılmayan bir takım, birbirinden öğrenmeyen bir takımdır. CI/CD pipeline'ı olmayan bir proje, her deploy'da Rus ruleti oynuyor demektir. Araçları doğru kur, süreçleri otomatikleştir, kültürü inşa et."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Repository** (ri-poz-i-tor-i) → Depo / Kod deposu
   *"I created a new repository on GitHub for our project."*

2. **Pull Request** (pul ri-kwest) → Birleştirme isteği
   *"Can you review my pull request? I've added input validation to the login form."*

3. **Fork** (fork) → Çatallamak
   *"I forked the repository to contribute a bug fix."*

4. **Code Review** (kohd ri-vyuu) → Kod incelemesi
   *"We require at least one code review before merging any pull request."*

5. **Workflow** (werk-flow) → İş akışı
   *"Our CI workflow runs tests on every push to the main branch."*

**Okuma Egzersizi:** GitHub'ın resmi dokümantasyonunda "About Pull Requests" sayfasını İngilizce oku: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests

**Yazma Pratiği:** Aşağıdaki PR açıklamasını İngilizce yaz: "Kullanıcı giriş formuna e-posta doğrulaması ekledim"
-> Örnek: `feat(auth): add email validation to user login form`
:::

:::external-resource
- **GitHub Docs:** "Getting Started with GitHub" (resmi dokümantasyon, ucretsiz)
- **GitHub Skills:** skills.github.com (interaktif GitHub egzersizleri, ucretsiz)
- **Conventional Commits:** conventionalcommits.org (resmi spesifikasyon, ucretsiz)
- **How to Contribute to Open Source:** opensource.guide (GitHub'ın acik kaynak rehberi, ucretsiz)
- **GitHub Actions Marketplace:** github.com/marketplace (hazir action'lar, ucretsiz)
:::
