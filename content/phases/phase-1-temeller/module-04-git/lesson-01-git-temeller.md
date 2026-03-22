---
id: mod-04-git/lesson-01
title: "Git Temelleri ve Günlük İş Akışı"
estimated_minutes: 45
tags: ["git", "version-control", "cli", "workflow"]
prerequisites: ["mod-01-internet/lesson-01"]
order: 1
---

# Git Temelleri ve Günlük İş Akışı

:::realworld
Bir projede 3 gün önce çalışan kodu degistirdin ve her sey bozuldu. "Keske geri alabilsem" diye dusunduysen, version control tam da bunun için var. Profesyonel yazılım dunyasinda Git bilmeden is yapmak mumkun değil. Her gun commit atacaksin, branch olusturacaksin, conflict cozeceksin. Bu derste Git'i sadece "kullanmak" değil, "anlamak" seviyesine geleceksin. Mulakatlarda "Git workflow'unuz nedir?" sorusuna profesyonel cevap verebileceksin.
:::

## Neden Version Control?

Yazılım geliştirme surecinde kodun sürekli değişir. Version control olmadan:

- Hangi değişikliği ne zaman yaptığını bilemezsin
- Bozulan kodu geri alamazsin
- Takim arkadaslarinla ayni dosya üzerinde çalışmak kabus olur
- "final_v2_gerçek_son_hali.zip" gibi dosya isimlendirme facialari yasarsin
- Production'da bir bug ciktiginda hangi degisikligin soruna yol actigini bulamazsin

:::concept[Version Control System (VCS)]
Version Control System, dosyalardaki değişiklikleri zaman içinde kaydeden ve istedigin zaman önceki bir versiyona donmeni sağlayan bir sistemdir.

**Türkçe karsiligi:** Sürüm Kontrol Sistemi
**Ne ise yarar:** Kodun her aninin fotografini ceker, istedigin ana geri donebilirsin
**Gerçek hayat benzetmesi:** Bir belgedeki "Geri Al" (Ctrl+Z) ozelliginin tüm proje genelinde, tüm ekip için çalışan hali
:::

:::deha-tip
Deha seviyesi geliştiriciler, Git'i sadece "kod yedekleme araci" olarak gormez. Git onlar için bir iletişim aracidir. Commit mesajlari, code review surecindeki yorumlar ve branch stratejileri, takimla iletisimin bir parcasidir. Iyi bir Git geçmişi, projenin hikayesini anlatir.
:::

## Git Nedir?

Git, 2005 yilinda Linus Torvalds tarafindan Linux kernel'ini yönetmek için geliştirilmiş bir distributed version control system'dir.

### Snapshots vs Diffs

Diger VCS'ler (SVN gibi) dosyalardaki değişiklikleri (diff/delta) kaydeder. Git ise her commit'te projenin tamaminin bir snapshot'ini (anlık goruntu) alir.

:::code[text]{title="Diger VCS'ler: Delta Tabanlı"}
Versiyon 1:  [Dosya A v1] [Dosya B v1] [Dosya C v1]
Versiyon 2:  [  delta A ] [Dosya B v1] [  delta C ]
Versiyon 3:  [  delta A ] [  delta B ] [Dosya C v2]
:::

:::code[text]{title="Git: Snapshot Tabanlı"}
Versiyon 1:  [Dosya A v1] [Dosya B v1] [Dosya C v1]
Versiyon 2:  [Dosya A v2] [Dosya B v1] [Dosya C v2]  (değişmeyen dosya için referans)
Versiyon 3:  [Dosya A v3] [Dosya B v2] [Dosya C v2]
:::

:::beginner-mistake
Yanlis düşünce: "Git her commit'te tüm dosyalari kopyaliyor, çok yer kaplar." Hayir! Git değişmeyen dosyalar için sadece önceki snapshot'a bir referans (pointer) tutar. Bu sayede hem hızlı hem de verimlidir.
:::

### Git'in 3 Alani

Git'te her dosya 3 alan arasinda hareket eder. Bu 3 alani anlamak Git'i anlamanin temelidir:

:::code[text]{title="Git'in 3 Temel Alanı"}
  Working Directory          Staging Area           Repository (.git)
  (Çalışma Dizini)          (Hazırlık Alanı)        (Yerel Depo)
  ┌─────────────┐          ┌─────────────┐         ┌─────────────┐
  │             │  git add  │             │ git     │             │
  │  Dosyalarini│ ───────> │  Commit'e   │ commit  │  Kalici     │
  │  duzenle    │          │  hazırla    │ ──────> │  geçmiş     │
  │             │          │             │         │             │
  └─────────────┘          └─────────────┘         └─────────────┘

  Dosyalar burada            "Sahneye al"           Projenin tüm
  değiştirilir               (stage)                tarihcesi burada
:::

:::concept[Staging Area (İng: Staging Area / Index)]
Staging Area, commit'e dahil edilecek degisikliklerin hazirlandigi ara bolge dir.

**Türkçe karsiligi:** Hazırlama / Sahneleme Alani
**Ne ise yarar:** Hangi degisikliklerin bir sonraki commit'e dahil edilecegini secmeni sağlar
**Gerçek hayat benzetmesi:** Bir kolinin içine koyacagin esyalari oncesinde masanin üzerine ayirmak gibi. Önce secersin, sonra paketi kapatirsin (commit).
:::

## Git Kurulumu ve Ilk Ayarlar

:::code[bash]{title="Git Kurulum Kontrolü"}
# Git'in yuklu olup olmadigini kontrol et
git --version
# Örnek çıktı: git version 2.43.0

# Yoksa:
# Windows: https://git-scm.com/download/win
# macOS: brew install git
# Linux: sudo apt install git
:::

:::code[bash]{title="Zorunlu İlk Ayarlar (git config)"}
# Kim oldugunu Git'e tanit (her commit'te bu bilgiler kullanılır)
git config --global user.name "Taha Arslan"
git config --global user.email "taha@example.com"

# Varsayılan branch ismini ayarla (modern standart: main)
git config --global init.defaultBranch main

# Varsayılan editor'u ayarla
git config --global core.editor "code --wait"  # VS Code

# Ayarlarini kontrol et
git config --list

# Belirli bir ayari gor
git config user.name
:::

:::tip
`--global` flag'i bu ayarlari tüm projeler için yapar. Belirli bir projeye ozel ayar yapmak için `--global` olmadan çalıştır. Proje bazli config, global config'i override eder.
:::

## Temel Komutlar

### git init - Yeni Repo Oluşturma

:::code[bash]{title="Yeni Bir Git Deposu Oluşturma"}
# Yeni proje klasoru oluştur ve içine gir
mkdir my-project
cd my-project

# Git deposu başlatır (.git klasoru oluşur)
git init

# Sonuç: Initialized empty Git repository in /path/my-project/.git/
:::

### git clone - Var Olan Repo'yu Kopyalama

:::code[bash]{title="Uzak Depoyu Klonlama"}
# GitHub'dan bir projeyi klonla
git clone https://github.com/kullanıcı/repo.git

# Farklı isimle klonla
git clone https://github.com/kullanıcı/repo.git my-local-name

# Belirli bir branch'i klonla
git clone -b develop https://github.com/kullanıcı/repo.git
:::

### git status - Durumu Gorme

:::code[bash]{title="Çalışma Dizininin Durumu"}
git status

# Örnek çıktı:
# On branch main
# Changes not staged for commit:
#   modified:   index.html
#
# Untracked files:
#   style.css

# Kısa format (daha okunakli)
git status -s
# M  index.html    (Modified - degistirilmis)
# ?? style.css     (Untracked - takip edilmiyor)
:::

### git add - Staging Area'ya Ekleme

:::code[bash]{title="Değişiklikleri Sahneye Alma"}
# Tek dosya ekle
git add index.html

# Birden fazla dosya ekle
git add index.html style.css

# Tüm değişiklikleri ekle (dikkatli kullan!)
git add .

# Belirli bir klasordeki tüm dosyalari ekle
git add src/

# Interaktif ekleme (parcali stage)
git add -p
# Her değişiklik blogu (hunk) için y/n secersin
:::

:::beginner-mistake
`git add .` kullanimina dikkat! Bu komut tüm değişiklikleri ekler. Eger .env dosyan, node_modules klasorun veya büyük binary dosyalarin varsa ve .gitignore düzgün ayarlanmamissa, bunlar da commit'e girebilir. Aliskanlık olarak önce `git status` ile ne ekleyeceğini gor, sonra `git add` yap.
:::

### git commit - Değişiklikleri Kaydetme

:::code[bash]{title="Commit Oluşturma"}
# Mesaj ile commit
git commit -m "feat: add user login page"

# Detayli mesaj yaz (editor açılır)
git commit

# Stage + commit tek adimda (sadece TRACKED dosyalar için)
git commit -am "fix: resolve navbar alignment issue"
:::

### git log - Geçmişi Görüntüleme

:::code[bash]{title="Commit Geçmişi"}
# Tam log
git log

# Tek satırda özet
git log --oneline

# Görsel branch yapısı
git log --oneline --graph --all

# Son 5 commit
git log -5

# Belirli bir dosyanin geçmişi
git log -- src/app.js

# Tarih araligi ile filtreleme
git log --since="2024-01-01" --until="2024-06-01"

# Belirli bir yazarin commit'leri
git log --author="Taha"
:::

### git diff - Değişiklikleri Karşılaştırma

:::code[bash]{title="Farkları Görme"}
# Working directory vs staging area (henuz stage edilmemis değişiklikler)
git diff

# Staging area vs son commit (stage edilmis ama commit edilmemis)
git diff --staged

# Iki commit arasindaki fark
git diff abc123 def456

# Belirli bir dosyadaki değişiklikler
git diff -- src/app.js

# Sadece değişen dosyalarin isimlerini gor
git diff --name-only
:::

### git show - Commit Detayi

:::code[bash]{title="Commit Detayını Görme"}
# Son commit'in detayi
git show

# Belirli bir commit'in detayi
git show abc123

# Sadece değişen dosyalari gor
git show --stat abc123
:::

## .gitignore Best Practices

`.gitignore` dosyasi, Git'in takip etmemesi gereken dosya ve klasorleri belirtir. Her projede doğru bir `.gitignore` oluşturmak kritik oneme sahiptir.

:::code[text]{title=".gitignore Örneği (Node.js Projesi)"}
# Bağımlılıklar (Dependencies)
node_modules/
bower_components/

# Ortam Değişkenleri (ASLA commit'leme!)
.env
.env.local
.env.production

# Build çıktıları
dist/
build/
.next/
out/

# IDE / Editor dosyaları
.vscode/settings.json
.idea/
*.swp
*.swo
*~

# İşletim sistemi dosyaları
.DS_Store
Thumbs.db
desktop.ini

# Log dosyaları
*.log
npm-debug.log*
yarn-error.log*

# Test coverage
coverage/

# Geçici dosyalar
*.tmp
*.temp
:::

:::tip
gitignore.io (toptal.com/developers/gitignore) sitesinden diline, framework'une ve IDE'ne gore otomatik .gitignore olusturabilirsin. Örneğin "Node, React, VSCode, macOS" secersen hazır bir şablon üretir.
:::

:::beginner-mistake
.env dosyasini commit'lemek en yaygin ve en tehlikeli hatalardan biridir. API key'lerin, database sifrelerin ve secret'larin herkese açık hale gelir. .env dosyasini MUTLAKA .gitignore'a ekle. Eger yanlislikla commit'lediysen, sadece silmek yetmez - Git gecmisinde hala durur! Bu durumda secret'lari degistirmen ve `git filter-branch` veya BFG Repo-Cleaner kullanman gerekir.
:::

## Git Stash: Geçici Değişiklik Saklama

Üzerinde çalıştığın bir özellik var ama acil bir bug fix yapman gerekiyor. Değişikliklerini commit etmek istemiyorsun çünkü henuz hazır değil. Iste `git stash` tam bu an için:

:::concept[Stash (Ing: Stash)]
Stash, çalışmakta oldugum değişiklikleri geçici olarak bir kenara koymami ve temiz bir working directory ile başka bir ise gecmemi sağlar.

**Türkçe karsiligi:** Zula / Geçici Depo
**Ne ise yarar:** Yarım kalmis isi kaydetmeden bir kenara koyar, sonra geri alirsin
**Gerçek hayat benzetmesi:** Masa üzerinde çalışmakta oldugun kagitlari bir cekmece'ye koyup masayi temizlemek, sonra tekrar cikarip devam etmek
:::

:::code[bash]{title="Git Stash Kullanımı"}
# Değişiklikleri stash'e koy
git stash

# Mesaj ile stash'e koy (çok tavsiye edilir)
git stash push -m "login form validation WIP"

# Untracked dosyalari da dahil et
git stash -u

# Stash listesini gor
git stash list
# stash@{0}: On main: login form validation WIP
# stash@{1}: WIP on main: abc123 previous work

# Son stash'i geri yükle ve listeden sil
git stash pop

# Son stash'i geri yükle ama listeden silme
git stash apply

# Belirli bir stash'i geri yükle
git stash apply stash@{1}

# Belirli bir stash'i sil
git stash drop stash@{0}

# Tüm stash'leri temizle
git stash clear
:::

:::tip
`git stash pop` = `git stash apply` + `git stash drop`. Stash'i geri yukleyince conflict cikarsa, `pop` stash'i silmez (veri kaybini onler). Bu durumda conflict'i coz, sonra `git stash drop` ile elle sil.
:::

## Git Reset vs Revert

Bir commit'i geri almak istiyorsun. Iki farklı yol var ve hangisini sectigin çok önemli:

:::comparison
| Özellik | git reset | git revert |
|---------|-----------|------------|
| Ne yapar | Commit'leri gecmisten siler | Değişikliği geri alan YENI bir commit oluşturur |
| Geçmiş | Commit geçmişi değişir (rewrite) | Geçmiş korunur, yeni commit eklenir |
| Paylasilmis branch | TEHLIKELI (baskalarinin geçmişini bozar) | Güvenli (geçmiş bozulmaz) |
| Ne zaman kullan | Sadece YEREL, push edilmemis commit'lerde | Push edilmis, paylasilmis commit'lerde |

**Altin Kural:** Push ettiysen `revert`, push etmediysen `reset` kullan.
:::

:::code[bash]{title="Git Reset Kullanımı"}
# Son commit'i geri al, değişiklikleri staging area'da tut
git reset --soft HEAD~1

# Son commit'i geri al, değişiklikleri working directory'de tut
git reset --mixed HEAD~1    # (varsayılan)
# veya kısaca:
git reset HEAD~1

# Son commit'i geri al, değişiklikleri TAMAMEN SIL (dikkatli ol!)
git reset --hard HEAD~1

# Belirli bir commit'e don (sonraki tüm commit'ler silinir)
git reset --hard abc123
:::

:::code[bash]{title="Git Revert Kullanımı"}
# Belirli bir commit'in değişikliklerini geri alan yeni commit oluştur
git revert abc123

# Birden fazla commit'i revert et
git revert abc123 def456

# Commit mesaji sormadan (editor acmadan) revert et
git revert --no-edit abc123
:::

:::beginner-mistake
`git reset --hard` kullanırken çok dikkatli ol! Bu komut değişiklikleri KALICI olarak siler. Eger yanlislikla calistirdiysan, `git reflog` ile kurtarabilirsin (Git her HEAD degisikligini 30 gun boyunca saklar). Ama reflog da yoksa, veri geri gelmez.
:::

## Git Log Gelişmiş Kullanım

:::code[bash]{title="Gelişmiş Log Komutları"}
# Tek satirlik özet (en çok kullanılan)
git log --oneline
# abc1234 feat: add user dashboard
# def5678 fix: resolve login bug

# Görsel branch grafigi
git log --oneline --graph --all --decorate
# * abc1234 (HEAD -> main) Merge branch 'feature'
# |\
# | * def5678 (feature) feat: add sidebar
# | * ghi9012 feat: add header
# |/
# * jkl3456 initial commit

# Ozellestrilmis format
git log --pretty=format:"%h - %an, %ar : %s"
# abc1234 - Taha, 2 hours ago : feat: add dashboard

# Değişen dosyalarin istatistigi
git log --stat

# Commit iceriginde arama (pickaxe)
git log -S "useState"  # "useState" eklenen/silinen commit'leri bul

# Commit mesajinda arama
git log --grep="fix"  # mesajinda "fix" gecen commit'ler
:::

:::tip
Sik kullandığın log formatini alias olarak kaydet:
`git config --global alias.lg "log --oneline --graph --all --decorate"`
Artik `git lg` yazman yeterli.
:::

## Commit Best Practices

### Atomic Commits

Her commit TEK BIR mantıksal değişiklik icermelidir. "Login sayfasi eklendi ve ayrica footer rengi degisti ve bir de README guncellendi" seklinde bir commit YAPMA.

:::code[text]{title="Kötü vs İyi Commit Yaklaşımı"}
# KOTU: Her seyi tek commit'e tikmak
git add .
git commit -m "bir suru sey yaptim"

# IYI: Mantıksal olarak ayirmak
git add src/components/Login.jsx src/components/Login.css
git commit -m "feat: add login page component"

git add src/components/Footer.jsx
git commit -m "style: update footer background color"

git add README.md
git commit -m "docs: add setup instructions to README"
:::

### Conventional Commits

Profesyonel projelerde commit mesajlari belirli bir formata uyar:

:::code[text]{title="Conventional Commit Formatı"}
<type>(<scope>): <description>

Yaygin type'lar:
feat:     Yeni özellik
fix:      Bug duzeltme
docs:     Dokümantasyon değişikliği
style:    Kod formatlama (logic değişmez)
refactor: Kod yeniden yapılandırma (davranis değişmez)
test:     Test ekleme/duzeltme
chore:    Build, CI/CD, dependency güncelleme

Örnekler:
feat(auth): add Google OAuth login
fix(cart): resolve quantity update race condition
docs(api): add endpoint documentation for /users
refactor(db): extract database connection to separate module
test(auth): add unit tests for password validation
chore(deps): upgrade React from 18.2 to 18.3
:::

:::beginner-mistake
Commit mesajlarinda "değişiklik yapildi", "guncellendi", "fix" gibi anlamsiz mesajlar yazma. 6 ay sonra git log'a baktiginda bu mesajlar hicbir sey ifade etmez. Her commit mesaji "Bu commit ne yapiyor?" sorusuna net cevap vermeli.
:::

## Git Internals Temelleri

Git'in içinde neler dondugunu anlamak, Git'i gerçekten anlamak demektir.

### Git Objects

Git'in 3 temel object tipi vardir:

:::code[text]{title="Git Object Tipleri"}
1. Blob   → Dosya icerigini tutar (dosya adi TUTMAZ)
2. Tree   → Klasor yapisini tutar (dosya adlari + blob referanslari)
3. Commit → Snapshot'a işaret eder (tree + yazar + mesaj + parent commit)

Her object bir SHA-1 hash ile tanımlanır (40 karakter hex):
Örnek: e83c5163316f89bfbde7d9ab23ca2e25604af290
:::

:::code[bash]{title="Git Internals Komutları"}
# .git klasorunun içeriği
ls .git/
# HEAD, config, objects/, refs/, hooks/...

# Bir object'in tipini gor
git cat-file -t abc1234

# Bir object'in icerigini gor
git cat-file -p abc1234

# Tüm referanslari listele
git show-ref
:::

### HEAD, Refs ve Branches

:::code[text]{title="HEAD ve References"}
HEAD
 └── Suanki branch'i veya commit'i gösterir
     Genellikle: ref: refs/heads/main

refs/heads/
 ├── main      → main branch'in son commit'inin hash'i
 ├── develop   → develop branch'in son commit'inin hash'i
 └── feature   → feature branch'in son commit'inin hash'i

refs/tags/
 └── v1.0.0    → Belirli bir commit'e kalici işaret

refs/remotes/origin/
 ├── main      → Remote'daki main'in bilinen son durumu
 └── develop   → Remote'daki develop'in bilinen son durumu
:::

:::concept[HEAD (Ing: HEAD)]
HEAD, suanda üzerinde çalıştığın commit'i veya branch'i gosteren ozel bir referanstir.

**Türkçe karsiligi:** Bas / Aktif Referans
**Ne ise yarar:** Git'e "şu an neredesin" bilgisini verir
**Gerçek hayat benzetmesi:** Bir kitapta kullandığın yer imi (bookmark). Kitabin neresinde oldugunu gösterir.
:::

:::tip
`git reflog` komutu HEAD'in tüm hareketlerini gösterir. Eger yanlislikla bir commit kaybettiysen, `git reflog` ile hash'ini bulup `git checkout` veya `git reset` ile kurtarabilirsin. Reflog senin "geri alma" güvenlik agin.
:::

## Pratik Uygulama

:::exercise
1. Yeni bir klasor oluştur ve `git init` ile depo başlatır
2. `git config` ile ad ve email'ini ayarla (local scope)
3. Bir `index.html` dosyasi oluştur, icerigine basit bir HTML yapısı yaz
4. `git status` ile durumu gor, `git add` ile stage et, `git commit` ile kaydet
5. Dosyayi değiştir, `git diff` ile farki gor, yeni commit oluştur
6. `git log --oneline --graph` ile geçmişi görüntüle
7. Bir `.gitignore` dosyasi oluştur, içine `node_modules/` ve `.env` ekle
8. `git stash` ile bir değişikliği geçici olarak sakla, sonra `git stash pop` ile geri al
9. `git reset --soft HEAD~1` ile son commit'i geri al (değişiklikler staging'de kalir)
10. `git reflog` ile HEAD hareketlerini incele

---

### Alıştırma 2: .gitignore Patterns — Python + Node Projesi (Kolay)

Aşağıdaki proje yapısı için kapsamlı bir `.gitignore` dosyası yaz:

```
fullstack-project/
├── backend/           # Python (FastAPI)
│   ├── venv/
│   ├── __pycache__/
│   ├── .env
│   ├── *.pyc
│   └── db.sqlite3
├── frontend/          # Node (React)
│   ├── node_modules/
│   ├── dist/
│   ├── .env.local
│   └── coverage/
├── .idea/             # IDE
├── .vscode/
│   └── settings.json
├── *.log
└── .DS_Store
```

**Görev:**
1. Yukarıdaki tüm gereksiz dosya/klasörleri kapsayan `.gitignore` yaz
2. `.vscode/settings.json`'ı ignore et AMA `.vscode/extensions.json`'ı ETME (takım standardı)
3. `.env` ve `.env.local` ignore edilmeli ama `.env.example` EDİLMEMELİ
4. Gitignore'u test et: `git status` ile hiçbir ignore edilmesi gereken dosya görünmemeli

**Beklenen sonuç:** `git check-ignore -v <dosya>` ile her pattern'in doğru çalıştığını doğrula. Negation pattern (`!`) kullanımını göster.

---

### Alıştırma 3: Branch Yönetimi ve Merge Conflict Çözme (Orta)

Aşağıdaki senaryoyu adım adım uygula:

```bash
# 1. Yeni bir repo oluştur ve initial commit yap
mkdir conflict-lab && cd conflict-lab && git init
echo "# Proje" > README.md
git add README.md && git commit -m "initial commit"

# 2. feature/header branch'i oluştur ve değişiklik yap
git checkout -b feature/header
# README.md'ye "## Header Section" ekle
# Commit et

# 3. main'e dön ve AYNI SATIRDA farklı değişiklik yap
git checkout main
# README.md'ye "## Navigation Section" ekle (aynı satıra)
# Commit et

# 4. feature/header'ı main'e merge et
git merge feature/header
# CONFLICT oluşacak!

# TODO: Conflict'i çöz:
#   a) Dosyayı aç, <<<<<<< ve >>>>>>> işaretlerini bul
#   b) İki değişikliği de içeren son halini yaz
#   c) git add + git commit ile merge'i tamamla

# 5. git log --oneline --graph ile merge geçmişini görüntüle
```

**Beklenen sonuç:** Merge conflict başarıyla çözülmeli. `git log --oneline --graph` çıktısında merge commit'i ve iki branch'in birleştiği görülmeli. Conflict marker'ları (`<<<<<<<`, `=======`, `>>>>>>>`) dosyada kalmamalı.
:::

:::knowledge-check
type: multiple_choice
question: "Git'in 3 temel alanı hangileridir?"
options:
  - "Local, Remote, Cloud"
  - "Working Directory, Staging Area, Repository"
  - "Source, Build, Deploy"
  - "Init, Commit, Push"
correct: 1
explanation: "Git'in 3 temel alani Working Directory (dosyalari duzenlersin), Staging Area (commit'e hazirlarsin) ve Repository (kalici geçmiş) olarak adlandirilir. Dosyalar bu 3 alan arasinda git add ve git commit ile hareket eder."
:::

:::knowledge-check
type: multiple_choice
question: "Push edilmiş bir commit'i güvenli şekilde geri almak için hangi komut kullanılmalıdır?"
options:
  - "git reset --hard HEAD~1"
  - "git revert <commit-hash>"
  - "git delete <commit-hash>"
  - "git undo <commit-hash>"
correct: 1
explanation: "Push edilmis commit'lerde git revert kullanılır çünkü bu komut geçmişi bozmaz, değişikliği geri alan YENI bir commit oluşturur. git reset ise geçmişi değiştirir ve paylasilmis branch'lerde diger gelistiricilerin geçmişini bozar."
:::

:::knowledge-check
type: multiple_choice
question: "git stash push -m 'WIP feature' komutu ne yapar?"
options:
  - "Yeni bir branch oluşturur"
  - "Değişiklikleri commit eder"
  - "Çalışmakta olan değişiklikleri mesaj ile birlikte geçici olarak saklar"
  - "Remote'a push eder"
correct: 2
explanation: "git stash, working directory ve staging area'daki değişiklikleri geçici bir alana saklar ve çalışma dizinini temizler. -m flag'i ile aciklayici bir mesaj eklenir, bu da git stash list ile baktiginda hangi stash'in ne oldugunu anlamani sağlar."
:::

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6

### Prompt Örnekleri

**1. Konuyu Derinlemesine Anla:**
> "Git'in 3 temel alanini (Working Directory, Staging Area, Repository) detayli açıkla. Bir dosya bu alanlar arasinda nasil hareket ediyor? git add, git commit ve git reset komutlarinin bu alanlara etkisini göster. Staging area neden var, doğrudan commit etmek yerine neden bu ara adim gerekli?"

*Neden:* Git'in veri modelini anlamak, karışık durumlarda (merge conflict, detached HEAD) ne yapman gerektigini bilmeni sağlar

**2. Pratik Uygulama:**
> "Şu senaryoyu adim adim coz: 3 dosyada değişiklik yaptim ama sadece 2'sini commit etmek istiyorum. Ucuncuyu stash'lemek istiyorum. Sonra başka bir branch'a gecip acil bir fix yapip geri donmek istiyorum. Tüm git komutlarini sırala."

*Follow-up:* "Yanlislikla git reset --hard yaptim ve commit'imi kaybettim. git reflog ile nasil kurtaririm? Adim adim göster."

**3. Mukemmellik Için:**
> "Conventional Commits formatini kullanarak bir haftalik geliştirme surecinin commit geçmişini örnekle. feat, fix, refactor, docs, test, chore type'larini kullan. Bu gecmisin git log ve CHANGELOG oluşturma acisindan neden önemli oldugunu açıkla."

### Pair Programming Ipucu
Git sorunlariyla karsilastiginda AI'a `git status` ve `git log --oneline` ciktisini yapistir: "Şu anki Git durumumu analiz et. Merge conflict çözümü / branch stratejisi / commit geçmişi temizligi için ne yapmaliyim?"
:::

:::interview
## Mülakat Sorulari

**Soru 1: git merge ve git rebase arasindaki fark nedir? Hangisini ne zaman kullanirsiniz?**
- **Junior cevabi:** Merge birleştirme yapar, rebase commitleri tekrar uygular.
- **Senior cevabi:** Merge, merge commit oluşturarak iki branch'in geçmişini korur. Rebase ise commitleri hedef branch'in ucuna tasiyarak lineer geçmiş oluşturur. Public branch'lerde (main, develop) her zaman merge kullanılır çünkü rebase geçmişi yeniden yazar ve diger gelistiricilerin force-pull yapmasini gerektirir. Feature branch'lerde rebase tercih edilir çünkü temiz geçmiş sağlar. Golden rule: Başkasının çalıştığı branch'i asla rebase etme.

**Soru 2: Staging area (index) ne ise yarar? Neden direkt commit yapamiyoruz?**
- **Junior cevabi:** `git add` ile dosyalari commit'e hazirlariz.
- **Senior cevabi:** Staging area, commit'e neyin dahil edilecegini kontrol etmenizi sağlar. Büyük değişiklikleri mantıksal commit'lere ayirabilirsiniz: `git add -p` ile ayni dosyanin farklı parcalarini farklı commit'lere koyabilirsiniz. Bu atomic commit prensibini destekler: her commit tek bir mantıksal değişikliği temsil etmelidir. Code review ve git bisect gibi işlemler için temiz commit geçmişi kritiktir.
:::

:::exercise
### Alıştırma 4: Git Log Analiz Aracı

**Görev:** `git log` çıktısını parse eden ve commit istatistikleri çıkaran bir bash script yaz.

**Başlangıç kodu:**
```bash
#!/bin/bash

# Ornek bir repo uzerinde calis
mkdir git-stats-lab && cd git-stats-lab && git init

# Ornek commit'ler olustur
for i in {1..10}; do
    echo "Line $i" >> file.txt
    git add file.txt
    git commit -m "feat: add line $i" --date="2026-03-$(printf '%02d' $i) 10:00:00"
done

# TODO: Istatistikleri hesapla
echo "=== Git Istatistikleri ==="

# 1. Toplam commit sayisi
TOTAL=$(git rev-list --count HEAD)
echo "Toplam commit: $TOTAL"

# 2. Son 7 gundeki commit sayisi
# TODO: git log --since="7 days ago" --oneline | wc -l

# 3. En cok commit atan yazar
# TODO: git shortlog -sn | head -3

# 4. Dosya basina commit sayisi
# TODO: git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -5

# 5. Gune gore commit dagilimi
# TODO: git log --format='%ad' --date=format:'%A' | sort | uniq -c | sort -rn
```

**Beklenen çıktı:**
```
=== Git Istatistikleri ===
Toplam commit: 10
Son 7 gun: 7
En aktif yazar: Your Name (10)
En cok degisen dosya: file.txt (10)
```

**İpucu:** `git log --format='%an'` yazar adını, `--format='%ad'` commit tarihini verir.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: Interactive Staging Simülasyonu

**Görev:** Bir dosyadaki farklı değişiklikleri ayrı commit'lere bölme pratiği yap.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir staging-lab && cd staging-lab && git init

# Baslangic dosyasi
cat > app.py << 'EOF'
def greet(name):
    return f"Hello, {name}"

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
EOF

git add app.py && git commit -m "initial: add math and greet functions"

# Birden fazla degisiklik yap
cat > app.py << 'EOF'
def greet(name):
    """Kullaniciyi selamla."""
    return f"Merhaba, {name}!"

def add(a, b):
    """Iki sayiyi topla."""
    return a + b

def multiply(a, b):
    """Iki sayiyi carp."""
    return a * b

def subtract(a, b):
    """Iki sayinin farkini al."""
    return a - b
EOF

# GOREV: Bu degisiklikleri 3 ayri commit'e bol:
# Commit 1: greet fonksiyonu Turkceye cevrild  + docstring
# Commit 2: add ve multiply fonksiyonlarina docstring eklendi
# Commit 3: subtract fonksiyonu eklendi

# Ipucu: git add -p ile hunk'lari secerek stage et
# y = bu hunk'i stage et
# n = bu hunk'i atlat
# s = daha kucuk hunk'lara bol

echo "GOREV: Asagidaki komutlari kullanarak 3 ayri commit yap:"
echo "1. git add -p app.py  (sadece greet degisikliklerini sec)"
echo "2. git commit -m 'refactor: convert greet to Turkish'"
echo "3. git add -p app.py  (sadece docstring'leri sec)"
echo "4. git commit -m 'docs: add docstrings to math functions'"
echo "5. git add app.py && git commit -m 'feat: add subtract function'"

git diff
```

**Beklenen çıktı:**
```
3 commit olusturulduktan sonra:
$ git log --oneline
abc1234 feat: add subtract function
def5678 docs: add docstrings to math functions
ghi9012 refactor: convert greet to Turkish
```

**İpucu:** `git add -p` komutu her değişiklik bloğu (hunk) için y/n/s sorar. `s` ile hunk'ı daha küçük parçalara bölebilirsin.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: Git Alias Koleksiyonu

**Görev:** Günlük Git iş akışını hızlandıran alias'lar oluştur ve test et.

**Başlangıç kodu:**
```bash
#!/bin/bash

# Git alias'lari tanimla
git config --global alias.st "status -sb"
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 --stat"
git config --global alias.unstage "restore --staged"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.branches "branch -a -v"
git config --global alias.contributors "shortlog -sn --all"

# TODO: Bu alias'lari da ekle:
# git undo -> son commit'i geri al (degisiklikler working directory'de kalsin)
# git wip -> hizli "work in progress" commit
# git cleanup -> merged branch'leri sil
# git find -> commit mesajinda arama yap

# Test
mkdir alias-lab && cd alias-lab && git init

echo "# Proje" > README.md && git add . && git commit -m "initial commit"
echo "Icerik" >> README.md && git add . && git commit -m "feat: add content"

echo "=== git st ==="
git st

echo -e "\n=== git lg ==="
git lg

echo -e "\n=== git last ==="
git last

echo -e "\n=== git branches ==="
git branches

echo -e "\n=== git contributors ==="
git contributors
```

**Beklenen çıktı:**
```
=== git st ===
## main

=== git lg ===
* abc1234 (HEAD -> main) feat: add content
* def5678 initial commit

=== git last ===
commit abc1234
  feat: add content
  README.md | 1 +

=== git branches ===
* main abc1234 feat: add content

=== git contributors ===
  2  Your Name
```

**İpucu:** `git config --global alias.undo "reset --soft HEAD~1"` ile son commit geri alınır ama değişiklikler staging'de kalır.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 7: Git Bisect ile Bug Bulma

**Görev:** `git bisect` kullanarak bir bug'ın hangi commit'te girdiğini bulma pratiği yap.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir bisect-lab && cd bisect-lab && git init

# 10 commit olustur, 5. commit'te bug gir
for i in {1..10}; do
    if [ $i -lt 5 ]; then
        echo "function calculate() { return 2 + 2; }" > app.js
    else
        # Bug: 5. commit'ten itibaren yanlis hesaplama
        echo "function calculate() { return 2 + 3; }" > app.js
    fi
    git add app.js
    git commit -m "commit $i: update calculation"
done

# Test script'i: cikti 4 olmali, degilse bug var
cat > test.sh << 'SCRIPT'
#!/bin/bash
result=$(node -e "$(cat app.js); console.log(calculate())")
if [ "$result" = "4" ]; then
    exit 0  # iyi commit
else
    exit 1  # bug var
fi
SCRIPT
chmod +x test.sh

# GOREV: git bisect ile bug'i bul
echo "=== Git Bisect ile Bug Bulma ==="
echo "1. git bisect start"
echo "2. git bisect bad HEAD          # son commit'te bug var"
echo "3. git bisect good HEAD~9       # ilk commit iyiydi"
echo "4. git bisect run ./test.sh     # otomatik bisect"
echo ""
echo "Veya manuel:"
echo "  git bisect start && git bisect bad && git bisect good HEAD~9"
echo "  Her adimda ./test.sh calistir, sonuca gore git bisect good/bad yaz"

# Otomatik bisect
git bisect start
git bisect bad HEAD
git bisect good HEAD~9
git bisect run ./test.sh 2>/dev/null
echo ""
echo "Bug ilk kez yukaridaki commit'te girdi!"
git bisect reset
```

**Beklenen çıktı:**
```
=== Git Bisect ile Bug Bulma ===
Bisecting: ... revisions left to test
...
abc1234 is the first bad commit
commit abc1234
  commit 5: update calculation

Bug ilk kez yukaridaki commit'te girdi!
```

**İpucu:** `git bisect run script.sh` ile otomatik bisect yapılır. Script exit 0 = iyi, exit 1 = kötü.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Git Hooks ile Commit Kalitesi

**Görev:** Pre-commit hook yazarak commit öncesi kod kalitesini kontrol eden otomatik kurallar oluştur.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir hooks-lab && cd hooks-lab && git init

# Pre-commit hook olustur
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash

echo "=== Pre-commit Kontroller ==="

# 1. Debug/console satirlari kontrolu
if git diff --cached --name-only | xargs grep -l "console.log\|debugger\|print(" 2>/dev/null; then
    echo "HATA: Debug satirlari bulundu! Commit oncesi temizle."
    echo "Ipucu: git diff --cached ile kontrol et"
    exit 1
fi

# TODO: 2. Dosya boyutu kontrolu (1MB'den buyuk dosya commit'lenmesin)

# TODO: 3. Commit mesaji formati kontrolu (prepare-commit-msg hook ile)
# Format: type(scope): description
# Ornekler: feat(auth): add login page
#           fix(api): resolve timeout issue

# TODO: 4. Belirli dosyalarin commit'lenmesini engelle (.env, secrets, *.log)

echo "Tum kontrollar basarili!"
exit 0
HOOK
chmod +x .git/hooks/pre-commit

# Test 1: Temiz commit
echo "const x = 42;" > clean.js
git add clean.js && git commit -m "feat: add clean code"
echo "Sonuc: Basarili"

# Test 2: Debug kodu ile commit denemesi
echo "console.log('debug');" > dirty.js
git add dirty.js
git commit -m "feat: add dirty code" || echo "Sonuc: Reddedildi (beklenen)"

# Temizle ve tekrar dene
echo "const y = 100;" > dirty.js
git add dirty.js && git commit -m "feat: add clean replacement"
```

**Beklenen çıktı:**
```
=== Pre-commit Kontroller ===
Tum kontrollar basarili!
[main abc1234] feat: add clean code

=== Pre-commit Kontroller ===
HATA: Debug satirlari bulundu! Commit oncesi temizle.
Sonuc: Reddedildi (beklenen)
```

**İpucu:** Hook'lar `.git/hooks/` dizininde bulunur. `exit 1` commit'i engeller, `exit 0` izin verir.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: Git Stash İleri Kullanım

**Görev:** `git stash` komutunun ileri özelliklerini kullanarak karmaşık senaryoları yönet.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir stash-lab && cd stash-lab && git init

echo "# Project" > README.md && git add . && git commit -m "initial"
echo "code" > main.js && git add . && git commit -m "feat: add main"

# Senaryo 1: Birden fazla stash yonetimi
echo "feature-1 code" > feature1.js
git stash push -m "WIP: feature 1 in progress"

echo "hotfix code" > hotfix.js
git stash push -m "WIP: urgent hotfix"

echo "feature-2 code" > feature2.js
git stash push -m "WIP: feature 2 started"

# GOREV 1: Stash listesini goster
echo "=== Stash Listesi ==="
git stash list

# GOREV 2: Belirli bir stash'i uygula (hotfix)
# TODO: git stash apply stash@{1}

# GOREV 3: Stash icerigi goruntuleme
echo -e "\n=== Stash Icerigi ==="
git stash show -p stash@{0}

# Senaryo 2: Partial stash (sadece bazi dosyalari stash'le)
git stash pop stash@{0}
echo "extra code" >> main.js
echo "new feature" > feature3.js

# TODO: Sadece feature3.js'i stash'le, main.js'deki degisiklikler kalsin
# git stash push -m "WIP: feature 3" -- feature3.js

# Senaryo 3: Stash'ten branch olusturma
# TODO: git stash branch feature/from-stash stash@{0}
echo -e "\n=== Stash'ten Branch ==="
echo "git stash branch feature/from-stash stash@{0}"

echo -e "\n=== Final Stash Listesi ==="
git stash list
```

**Beklenen çıktı:**
```
=== Stash Listesi ===
stash@{0}: On main: WIP: feature 2 started
stash@{1}: On main: WIP: urgent hotfix
stash@{2}: On main: WIP: feature 1 in progress

=== Stash Icerigi ===
diff --git a/feature2.js b/feature2.js
+feature-2 code
```

**İpucu:** `git stash push -m "mesaj" -- dosya.js` ile sadece belirli dosyaları stash'le. `stash@{n}` ile belirli stash'e eriş.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 10: Git Reflog ile Kayıp Commit Kurtarma

**Görev:** `git reflog` kullanarak yanlışlıkla silinen commit'leri kurtarma pratiği yap.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir reflog-lab && cd reflog-lab && git init

# Degerli commit'ler olustur
echo "v1" > important.txt && git add . && git commit -m "feat: version 1"
echo "v2" > important.txt && git add . && git commit -m "feat: version 2"
echo "v3" > important.txt && git add . && git commit -m "feat: version 3 (very important!)"

echo "=== Commit gecmisi ==="
git log --oneline

# Yanlis islem: Son 2 commit'i hard reset ile sil
echo -e "\n=== Yanlis islem: git reset --hard HEAD~2 ==="
git reset --hard HEAD~2

echo "Kalan commit'ler:"
git log --oneline
echo "important.txt icerigi: $(cat important.txt)"  # v1 (v3 kayboldu!)

# KURTARMA: reflog ile kayip commit'leri bul
echo -e "\n=== Reflog ==="
git reflog --oneline | head -5

# GOREV: v3 commit'ini kurtarma yontemleri:

# Yontem 1: Cherry-pick ile belirli commit'i geri al
# TODO: git cherry-pick <commit-hash>

# Yontem 2: Reset ile o noktaya don
# TODO: git reset --hard <commit-hash>

# Yontem 3: Yeni branch ile kurtarma
# TODO: git branch recovery <commit-hash>

echo -e "\n=== Kurtarma sonrasi ==="
# Reflog'dan v3 commit hash'ini bul ve kurtarma yap
V3_HASH=$(git reflog --oneline | grep "version 3" | head -1 | cut -d' ' -f1)
echo "Kurtarilacak commit: $V3_HASH"

git cherry-pick $V3_HASH 2>/dev/null || git reset --hard $V3_HASH
echo "important.txt icerigi: $(cat important.txt)"  # v3 geri geldi!
git log --oneline
```

**Beklenen çıktı:**
```
=== Commit gecmisi ===
abc1234 feat: version 3 (very important!)
def5678 feat: version 2
ghi9012 feat: version 1

=== Yanlis islem: git reset --hard HEAD~2 ===
Kalan commit'ler:
ghi9012 feat: version 1
important.txt icerigi: v1

=== Reflog ===
ghi9012 HEAD@{0}: reset: moving to HEAD~2
abc1234 HEAD@{1}: commit: feat: version 3 (very important!)
...

=== Kurtarma sonrasi ===
important.txt icerigi: v3
```

**İpucu:** `git reflog` tüm HEAD hareketlerini kaydeder. Silinen commit'ler 90 gün boyunca reflog'da kalır. `git fsck --lost-found` ile orphan commit'leri de bulabilirsin.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Git Diff Analiz Aracı

**Görev:** `git diff` çıktısını parse edip özet bilgi çıkaran bir bash script yaz.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir diff-lab && cd diff-lab && git init

cat > app.py << 'EOF'
def hello():
    print("Hello World")

def add(a, b):
    return a + b
EOF
git add . && git commit -m "initial"

cat > app.py << 'EOF'
def hello(name="World"):
    """Kullaniciyi selamla."""
    print(f"Hello, {name}!")

def add(a, b):
    """Iki sayiyi topla."""
    return a + b

def subtract(a, b):
    """Fark hesapla."""
    return a - b
EOF

echo "=== Diff Ozeti ==="
echo "Eklenen satirlar: $(git diff --numstat | awk '{sum+=$1} END {print sum}')"
echo "Silinen satirlar: $(git diff --numstat | awk '{sum+=$2} END {print sum}')"
echo "Degisen dosyalar: $(git diff --name-only | wc -l)"

echo -e "\n=== Dosya bazinda degisiklikler ==="
git diff --stat

echo -e "\n=== Sadece eklenen satirlar ==="
git diff | grep "^+" | grep -v "^+++" | head -10

echo -e "\n=== Sadece silinen satirlar ==="
git diff | grep "^-" | grep -v "^---" | head -10
```

**Beklenen çıktı:**
```
=== Diff Ozeti ===
Eklenen satirlar: 10
Silinen satirlar: 3
Degisen dosyalar: 1

=== Dosya bazinda degisiklikler ===
 app.py | 13 ++++++++++---
```

**İpucu:** `git diff --numstat` eklenen/silinen satır sayılarını verir. `git diff --stat` dosya bazında özet gösterir.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 12: Git Clean ve Reset Senaryoları

**Görev:** `git clean`, `git reset` ve `git restore` komutlarının farklı modlarını karşılaştır.

**Başlangıç kodu:**
```bash
#!/bin/bash
mkdir reset-lab && cd reset-lab && git init

echo "v1" > tracked.txt && git add . && git commit -m "v1"
echo "v2" > tracked.txt && git add . && git commit -m "v2"
echo "v3" > tracked.txt && git add . && git commit -m "v3"

# Untracked dosya olustur
echo "temp" > untracked.txt
echo "build output" > dist.js

# Staged degisiklik
echo "v4" > tracked.txt && git add tracked.txt

echo "=== Baslangic Durumu ==="
git status -sb

echo -e "\n=== Komut Karsilastirmasi ==="
echo "git restore tracked.txt           -> Working directory'deki degisikligi geri al"
echo "git restore --staged tracked.txt  -> Staging'den cikar (unstage)"
echo "git reset --soft HEAD~1           -> Son commit'i geri al, degisiklikler staged'de"
echo "git reset --mixed HEAD~1          -> Son commit'i geri al, degisiklikler unstaged'de"
echo "git reset --hard HEAD~1           -> Son commit'i geri al, degisiklikler SILINIR"
echo "git clean -fd                     -> Untracked dosyalari sil"
echo "git clean -fxd                    -> Untracked + gitignore'd dosyalari sil"

# Gosterim
echo -e "\n=== Reset --soft HEAD~1 ==="
git reset --soft HEAD~1
git status -sb
echo "tracked.txt icerigi: $(cat tracked.txt)"

echo -e "\n=== Reset --mixed (geri al) ==="
git commit -m "v3 restored" && git reset --mixed HEAD~1
git status -sb

echo -e "\n=== Clean (dry run) ==="
git clean -n  # Nelerin silinecegini goster (silmeden)
```

**Beklenen çıktı:**
```
=== Baslangic Durumu ===
## main
M  tracked.txt
?? dist.js
?? untracked.txt

=== Reset --soft HEAD~1 ===
## main
M  tracked.txt
tracked.txt icerigi: v4

=== Clean (dry run) ===
Would remove dist.js
Would remove untracked.txt
```

**İpucu:** `git clean -n` dry run yapar (silmez, ne silineceğini gösterir). `--soft` commit'i geri alır ama değişiklikler staged kalır.

**Zorluk:** Orta
:::

:::must-note
- Version control = kodun zaman içindeki tüm değişikliklerini takip eden sistem
- Git snapshot tabanlıdir (delta değil), değişmeyen dosyalar için referans tutar
- 3 alan: Working Directory (duzenle) → Staging Area (git add) → Repository (git commit)
- Zorunlu ilk ayar: `git config --global user.name` ve `user.email`
- Temel akis: `git status` → `git add` → `git commit -m "mesaj"` → `git log`
- `git diff` = stage edilmemis değişiklikler, `git diff --staged` = stage edilmis değişiklikler
- .gitignore'a MUTLAKA ekle: node_modules/, .env, IDE dosyalari, build ciktilari, log dosyalari
- `git stash` = değişiklikleri geçici sakla, `git stash pop` = geri yükle ve sil
- Push ettiysen `git revert`, push etmediysen `git reset` kullan (altin kural)
- `git reset --soft` = değişiklikleri staging'de tutar, `--mixed` = working dir'de tutar, `--hard` = SILER
- `git log --oneline --graph --all` = branch yapisini görsel olarak gor
- Commit best practices: atomic commits (tek mantıksal değişiklik), Conventional Commits formati (feat/fix/docs/refactor)
- Git internals: Blob (dosya içeriği), Tree (klasor yapısı), Commit (snapshot + meta)
- HEAD = şu an üzerinde oldugun commit/branch, `git reflog` = HEAD geçmişi (kurtarma için)
- `git reflog` ile kaybettigin commit'leri 30 gun icerisinde kurtarabilirsin
:::

:::senior-learns
Bir Senior Developer veya CTO, Git konusunu ogrenirken şu yaklasimi benimser:

1. **Git internals'i derinlemesine öğrenir** - `.git` klasorunun icerigini inceleyerek blob, tree ve commit object'lerinin nasil çalıştığını anlar. `git cat-file -p HEAD` gibi low-level komutlarla Git'in veri modelini icerideki öğrenir. "Git bir content-addressable filesystem'dir" cumlesini aciklayabilir.
2. **Commit geçmişini bir iletişim araci olarak kullanır** - Her commit mesaji, gelecekteki developer'a (belki kendisine) yazilmis bir mektuptur. "fix bug" yerine "fix: resolve race condition in cart quantity update when concurrent requests overlap" yazar. 6 ay sonra `git blame` ile bakan kisi ne yapildigini aninda anlar.
3. **git bisect ile bug avlar** - Production'da bir bug ciktiginda, `git bisect` ile binary search yaparak bug'i oluşturan commit'i bulur. 1000 commit arasinda 10 adimda sorunu izole eder. Bu, saatlerce kod okumaktan çok daha verimlidir.
4. **Interactive rebase ile geçmişi temizler** - Feature branch'ini merge etmeden önce `git rebase -i` ile commit'leri squash eder, siralar ve mesajlari duzeltir. Temiz bir geçmiş, code review'i kolaylastirir. Ama push edilmis commit'leri ASLA rebase etmez.
5. **Git hooks ile otomasyonu kurar** - `pre-commit` hook ile lint, format ve test kontrolu yapar. `commit-msg` hook ile commit mesaji formatini zorlar. Husky ve lint-staged gibi araclarla takim genelinde standart sağlar.
6. **Reflog'u güvenlik agi olarak bilir** - `git reflog` ile her HEAD hareketini takip edebilecegini bilir. Yanlislikla yapılan `reset --hard` veya silinen branch'i kurtarmak için reflog kullanır. "Git'te veri kaybi neredeyse imkansizdir, yeter ki reflog'u bilin" der.

**Karar Verme Sureci — Merge vs Rebase vs Squash:**
- **Merge commit (--no-ff)**: Her feature branch'in baslangic ve bitis noktasi gorulur. Trade-off: gecmis karisik gorunebilir ama tam izlenebilirlik saglar. Buyuk takimlarda tercih edilir cunku her PR'in sinirlari net.
- **Rebase**: Lineer gecmis, temiz goruntu. Trade-off: shared branch'lerde tehlikeli (force push gerektirir), conflict resolution her commit icin tekrarlanir. Kisisel feature branch'lerde kullan, main'e yapma.
- **Squash merge**: Tum feature tek commit olur. Trade-off: granular gecmis kaybolur ama main branch temiz kalir. Kucuk-orta takimlarda en populer strateji.
- **Senior karar agaci**: "Takim 5 kisiden azsa ve herkes rebase biliyorsa -> rebase. 5+ kisilik takim -> squash merge. Regulated industry (finans, saglik) -> merge commit (audit trail icin)."

**Anti-pattern Farkindaligi:**
- **"Mega commit" anti-pattern'i**: 50 dosya degisen tek commit. Code review imkansiz, bisect ile bug bulunamaz, revert riski yuksek. Production'da 2000 satir degisiklikli bir commit'te gizli bir bug vardi, bulmamiz 3 gun surdu. 10 kucuk commit olsaydi bisect ile 10 dakikada bulurduk.
- **Branch cehennemi**: 3 haftadir merge edilmemis 15 feature branch. Merge conflict'ler o kadar buyur ki kimse merge etmek istemez. Cozum: trunk-based development — kucuk, sik merge'ler, feature flag'ler ile incomplete feature'lari gizle.
- **Force push to main**: Production branch'ine force push, tum takimin local repo'sunu bozar. Ilk is `main` branch'ine protection rule ekle.

**Gercek Dunya Deneyimi:** Bir startup'ta 8 kisilik takimda herkes farkli branching stratejisi kullaniyordu. Biri rebase, biri merge, biri direkt main'e push. 3 ayda main branch'in gecmisi okunamaz hale geldi. Tum takimi toplayip "Trunk-based + squash merge + conventional commits" standardina gecirdik. 1 hafta sonra code review suresi %50 dustu, deployment confidence %80 artti.

**Profesyonel Mindset:** "Git sadece bir versiyon kontrol araci değil, bir iletişim aracidir. Commit gecmisin, projenin hikayesini anlatir. Temiz bir geçmiş yazan ekip, kodu da temiz yazar. Her commit mesajini, senden sonra gelecek developer'a yazilmis bir not olarak düşün. O developer, 6 ay sonra 'bu değişiklik neden yapildi?' sorusuna cevap ariyor olacak."
:::

:::english
**Teknik Ingilizce - Bu Dersteki Terimler:**

1. **Repository** (ri-poz-i-to-ri) → Depo / Kod deposu
   *"Clone the repository and install the dependencies before running the project."*

2. **Commit** (kuh-mit) → Kayıt / Işleme
   *"Each commit should represent a single logical change to the codebase."*

3. **Staging Area** (stey-jing eh-ri-uh) → Hazırlama alani
   *"Use git add to move changes to the staging area before committing."*

4. **Branch** (braench) → Dal / Dallanma
   *"Create a new branch for each feature to keep the main branch stable."*

5. **Diff** (dif) → Fark / Değişiklik farki
   *"Review the diff carefully before committing to avoid unintended changes."*

**Okuma Egzersizi:** Git resmi dokumantasyonundan "Getting Started" bolumunu Ingilizce oku: https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control

**Yazma Pratigi:** Aşağıdaki commit mesajini Ingilizce yaz: "Kullanıcı giriş formuna validasyon eklendi"
→ Örnek: `feat(auth): add form validation to user login page`
:::

:::external-resource
- **Pro Git Book:** git-scm.com/book/en/v2 (ücretsiz, Git'in resmi kitabi)
- **Learn Git Branching:** learngitbranching.js.org (interaktif, görsel Git öğrenme)
- **Oh My Git!:** ohmygit.org (Git öğrenme oyunu, ücretsiz)
- **Conventional Commits:** conventionalcommits.org (commit mesaji standardi)
- **gitignore.io:** toptal.com/developers/gitignore (otomatik .gitignore uretici)
:::
