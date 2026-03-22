---
id: mod-05-terminal/lesson-00
title: "Geliştirme Ortamı Kurulumu: Sıfırdan Profesyonel Setup"
estimated_minutes: 90
tags: ["setup", "git", "nodejs", "python", "vscode", "docker", "windows", "macos", "linux"]
prerequisites: []
order: 0
---

# Geliştirme Ortamı Kurulumu: Sıfırdan Profesyonel Setup

:::realworld
Bir yazılımcının ilk günü genellikle ortam kurulumu ile başlar. Yeni bir şirkete girdiğinde, yeni bir bilgisayar aldığında ya da bir open source projeye katkıda bulunmak istediğinde ilk yapacağın şey geliştirme ortamını kurmaktır. Bu ders, bilgisayarını sıfırdan profesyonel bir geliştirme makinesine dönüştürmeni sağlayacak. Kurulumu doğru yapmak, ileride saatlerce sürecek sorunları önler.
:::

## Neden Ortam Kurulumu Önemli?

Geliştirme ortamını doğru kurmak, bir inşaat projesinde temeli doğru atmak gibidir:

- **Versiyon uyumsuzlukları:** Yanlış Node.js veya Python sürümü yüzünden projeler çalışmaz
- **PATH sorunları:** Komut bulunamadı hataları en yaygın başlangıç sorunudur
- **Editör verimliliği:** Doğru yapılandırılmış bir VS Code, üretkenliğini 2-3 katına çıkarır
- **Takım uyumu:** Herkesin aynı araçları kullanması iş birliğini kolaylaştırır
- **Zaman kaybı:** Kurulum sorunlarıyla boğuşmak yerine kod yazmaya odaklanmalısın

:::deha-tip
Senior geliştiriciler ortam kurulumunu ciddiye alır. Dotfiles repo'ları oluşturur, setup script'leri yazar ve yeni bir makinede 30 dakikada tam çalışır ortama sahip olurlar. Bu derste sen de bu alışkanlığı edineceksin.
:::

---

## Bölüm 1: Windows 11 Kurulumu (Birincil)

Windows, dünya genelinde en yaygın kullanılan geliştirme platformudur. Modern Windows 11 ile profesyonel geliştirme ortamı kurmak oldukça kolaydır.

### 1.1 Windows Terminal Kurulumu

Windows Terminal, Microsoft'un modern terminal uygulamasıdır. Birden fazla sekme, profil ve özelleştirme sunar.

**Kurulum adımları:**

1. Microsoft Store'u aç
2. "Windows Terminal" ara
3. "Windows Terminal" uygulamasını yükle (Microsoft Corporation tarafından)
4. Yüklendikten sonra Başlat menüsünden "Terminal" yazarak aç

:::tip
Windows 11'de Windows Terminal zaten yüklü gelir. Eğer yoksa Microsoft Store'dan yükleyebilirsin. Bundan sonra tüm terminal işlemlerini Windows Terminal üzerinden yapacağız.
:::

**Varsayılan profili Git Bash olarak ayarlama (Git kurduktan sonra):**

1. Windows Terminal'i aç
2. Üst çubuktaki aşağı ok (v) ikonuna tıkla > "Ayarlar" (Settings)
3. "Başlangıç" (Startup) bölümünde "Varsayılan profil"i (Default profile) "Git Bash" olarak değiştir
4. Kaydet

### 1.2 Git Kurulumu ve Yapılandırma

Git, versiyon kontrol sistemidir ve her geliştiricinin ilk kurması gereken araçtır.

**Kurulum:**

1. https://git-scm.com/downloads/win adresine git
2. "Click here to download" butonuna tıkla
3. İndirilen `.exe` dosyasını çalıştır
4. Kurulum sihirbazında şu ayarları seç:
   - **Select Components:** Varsayılan ayarları koru, "Windows Explorer integration" seçili kalsın
   - **Default editor:** "Use Visual Studio Code as Git's default editor" seç
   - **Default branch name:** "Override the default branch name" seç, `main` yaz
   - **PATH environment:** "Git from the command line and also from 3rd-party software" seç
   - **Line ending:** "Checkout Windows-style, commit Unix-style line endings" seç
   - Diğer ayarları varsayılan bırak ve "Install" tıkla

**Kurulum doğrulama:**

:::code[bash]{title="Git Kurulum Doğrulama"}
# Windows Terminal'i aç ve şu komutları çalıştır:
git --version
# Beklenen çıktı: git version 2.47.1.windows.2 (veya daha yeni)

# Git'in PATH'te olduğunu doğrula
where git
# Beklenen çıktı: C:\Program Files\Git\cmd\git.exe
:::

**Git yapılandırma (zorunlu):**

:::code[bash]{title="Git Global Yapılandırma"}
# Adını ve e-posta adresini ayarla (GitHub hesabınla aynı olsun)
git config --global user.name "Senin Adın"
git config --global user.email "senin@email.com"

# Varsayılan branch adını main olarak ayarla
git config --global init.defaultBranch main

# VS Code'u varsayılan editör olarak ayarla
git config --global core.editor "code --wait"

# Renkli çıktıyı etkinleştir
git config --global color.ui auto

# Pull stratejisini rebase olarak ayarla (ileri seviye, ama doğru pratik)
git config --global pull.rebase true

# Yapılandırmayı kontrol et
git config --global --list
:::

:::beginner-mistake
`git config --global user.name` ve `user.email` ayarlamadan commit yapmaya çalışırsan Git hata verir. Bu ayarları kurulumdan hemen sonra yap. E-posta adresinin GitHub hesabındaki ile aynı olması gerekir, yoksa commit'lerin GitHub profilinle eşleşmez.
:::

:::exercise
### Alıştırma 1: Git Kurulumu ve Yapılandırma

Git'i kur ve yapılandır. Aşağıdaki adımları takip et:

```bash
# 1. Git sürümünü kontrol et
git --version

# 2. Global yapılandırmayı ayarla (kendi bilgilerinle değiştir)
git config --global user.name "Kendi Adın"
git config --global user.email "kendi@emailin.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --global color.ui auto

# 3. Yapılandırmayı doğrula
git config --global --list

# Beklenen çıktı (kendi bilgilerin görünecek):
# user.name=Kendi Adın
# user.email=kendi@emailin.com
# init.defaultbranch=main
# core.editor=code --wait
# color.ui=auto

# 4. Git'in çalıştığını test et
mkdir ~/test-git && cd ~/test-git
git init
git status
# Beklenen: "On branch main" ve "No commits yet" mesajı

# 5. Temizlik
cd ~ && rm -rf ~/test-git
```
:::

### 1.3 Node.js Kurulumu (nvm-windows ile)

Node.js'i doğrudan yüklemek yerine **nvm-windows** (Node Version Manager) kullanacağız. Bu sayede birden fazla Node.js sürümünü yönetebilirsin.

**Neden nvm?**
- Farklı projeler farklı Node.js sürümleri gerektirebilir
- Sürümler arası kolayca geçiş yapabilirsin
- Yeni sürümleri test edebilir, sorun olursa geri dönebilirsin

**nvm-windows kurulumu:**

1. https://github.com/coreybutler/nvm-windows/releases adresine git
2. En son sürümdeki `nvm-setup.exe` dosyasını indir
3. Kurulum sihirbazını çalıştır, varsayılan ayarlarla yükle
4. **Terminal'i kapat ve yeniden aç** (PATH güncellemesi için zorunlu)

:::code[bash]{title="nvm-windows ile Node.js Kurulumu"}
# nvm'in kurulduğunu doğrula
nvm version
# Beklenen çıktı: 1.2.2 (veya daha yeni)

# Mevcut Node.js sürümlerini listele
nvm list available
# LTS sütunundaki en üst sürümü not et (ör: 22.14.0)

# Node.js 22 LTS sürümünü kur
nvm install 22
# Beklenen: Downloading node.js version 22.x.x ... Complete.

# Kurduğun sürümü aktif et
nvm use 22
# Beklenen: Now using node v22.x.x (64-bit)

# Doğrulama
node --version
# Beklenen: v22.14.0 (veya 22.x.x)

npm --version
# Beklenen: 10.x.x

# nvm ile yüklü sürümleri gör
nvm list
# Aktif sürümün yanında * işareti olacak
:::

:::beginner-mistake
`nvm install` veya `nvm use` komutları çalışmıyorsa, terminal'i **yönetici olarak** (Run as Administrator) çalıştırmayı dene. Windows'ta nvm bazı işlemler için yönetici yetkisi gerektirir. Ayrıca nvm kurduktan sonra terminal'i kapatıp açmayı unutma.
:::

### 1.4 pnpm Kurulumu

pnpm, npm'e göre çok daha hızlı ve disk alanından tasarruf eden paket yöneticisidir.

:::code[bash]{title="pnpm Kurulumu"}
# npm ile pnpm'i global olarak kur
npm install -g pnpm

# Doğrulama
pnpm --version
# Beklenen: 9.x.x veya 10.x.x

# pnpm'in düzgün çalıştığını test et
mkdir ~/test-pnpm && cd ~/test-pnpm
pnpm init
# Beklenen: package.json dosyası oluşturuldu

# Bir paket yükleyerek test et
pnpm add lodash
# Beklenen: Packages: +1, Progress: resolved 1, reused 0, downloaded 1, added 1

# Temizlik
cd ~ && rm -rf ~/test-pnpm
:::

:::tip
pnpm, node_modules klasöründe sembolik linkler (symlinks) kullanır. Bu sayede aynı paketi birden fazla projede kullandığında diskten sadece bir kez yer kaplar. Büyük projelerde bu fark gigabaytlarca olabilir.
:::

### 1.5 Python 3.13 Kurulumu

Python, backend geliştirme, otomasyon ve veri işleme için kullanacağız.

**Kurulum:**

1. https://www.python.org/downloads/ adresine git
2. "Download Python 3.13.x" butonuna tıkla
3. İndirilen `.exe` dosyasını çalıştır
4. **ÖNEMLİ:** Kurulum ekranının altındaki **"Add python.exe to PATH"** kutucuğunu mutlaka işaretle
5. "Install Now" tıkla
6. Kurulum tamamlandığında "Disable path length limit" seçeneği çıkarsa, ona da tıkla

:::code[bash]{title="Python Kurulum Doğrulama"}
# Terminal'i kapat ve yeniden aç (PATH güncellemesi için)

python --version
# Beklenen: Python 3.13.x

pip --version
# Beklenen: pip 24.x.x from ... (python 3.13)

# Python'un çalıştığını test et
python -c "print('Merhaba Dünya!')"
# Beklenen: Merhaba Dünya!
:::

:::beginner-mistake
Python kurulumunda **"Add python.exe to PATH"** kutucuğunu işaretlemeyi unutmak en yaygın hatadır. Bu kutucuğu işaretlemezsen `python` komutu terminal'de tanınmaz. Unutursan, Python'u kaldırıp yeniden kur ve bu sefer kutucuğu işaretle.
:::

:::exercise
### Alıştırma 2: Node.js ve Python Kurulum Doğrulama

Kurduğun araçların doğru çalıştığını doğrula:

```bash
# 1. Tüm araçların sürümlerini kontrol et
echo "=== Geliştirme Araçları Sürüm Kontrolü ==="
git --version
node --version
npm --version
pnpm --version
python --version
pip --version

# 2. Node.js REPL (interaktif mod) test et
node -e "console.log('Node.js çalışıyor! Sürüm:', process.version)"
# Beklenen: Node.js çalışıyor! Sürüm: v22.x.x

# 3. Python interaktif test
python -c "import sys; print(f'Python çalışıyor! Sürüm: {sys.version}')"
# Beklenen: Python çalışıyor! Sürüm: 3.13.x ...

# 4. pnpm global dizinini kontrol et
pnpm config get store-dir
# pnpm'in paket deposunun konumunu gösterir
```
:::

### 1.6 VS Code Kurulumu ve Eklentiler

Visual Studio Code, modern web geliştirmenin standart editörüdür.

**Kurulum:**

1. https://code.visualstudio.com/ adresine git
2. "Download for Windows" butonuna tıkla
3. İndirilen `.exe` dosyasını çalıştır
4. Kurulum sihirbazında şu ek seçenekleri işaretle:
   - **"Add to PATH"** (komut satırından `code .` ile açmak için)
   - **"Register Code as an editor for supported file types"**
   - **"Add 'Open with Code' action to Windows Explorer file context menu"**
   - **"Add 'Open with Code' action to Windows Explorer directory context menu"**
5. Kur ve bitir

**Kurulum doğrulama:**

:::code[bash]{title="VS Code Komut Satırı Doğrulama"}
# Terminal'i kapat ve yeniden aç
code --version
# Beklenen: 1.96.x (veya daha yeni)
# Sürüm numarası, commit hash ve platform bilgisi gösterilir

# VS Code'u mevcut dizinde aç
code .
# VS Code açılmalı
:::

**Temel eklentiler (Extensions):**

VS Code'u aç, sol taraftaki Extensions ikonuna tıkla (veya `Ctrl+Shift+X`) ve şu eklentileri yükle:

:::code[bash]{title="VS Code Eklentileri - Komut Satırından Kurulum"}
# Eklentileri komut satırından yükleyebilirsin:

# 1. ESLint - JavaScript/TypeScript hata kontrolü
code --install-extension dbaeumer.vscode-eslint

# 2. Prettier - Kod formatlama
code --install-extension esbenp.prettier-vscode

# 3. Tailwind CSS IntelliSense - Tailwind otomatik tamamlama
code --install-extension bradlc.vscode-tailwindcss

# 4. Python - Python dil desteği
code --install-extension ms-python.python

# 5. GitLens - Git geçmişi ve blame görünümü
code --install-extension eamodio.gitlens

# 6. Auto Rename Tag - HTML/JSX tag'lerini otomatik yeniden adlandır
code --install-extension formulahendry.auto-rename-tag

# 7. Error Lens - Hataları satır içinde göster
code --install-extension usernamehw.errorlens

# 8. Thunder Client - API test aracı (Postman alternatifi)
code --install-extension rangav.vscode-thunder-client

# 9. Material Icon Theme - Dosya ikonları
code --install-extension pkief.material-icon-theme

# 10. Docker - Docker dosyaları için destek
code --install-extension ms-azuretools.vscode-docker

# Yüklü eklentileri listele
code --list-extensions
:::

:::exercise
### Alıştırma 3: VS Code Eklenti Kurulumu

Yukarıdaki komutları tek tek çalıştırarak tüm eklentileri kur. Sonra doğrula:

```bash
# Tüm eklentileri kur (tek komutla)
code --install-extension dbaeumer.vscode-eslint && \
code --install-extension esbenp.prettier-vscode && \
code --install-extension bradlc.vscode-tailwindcss && \
code --install-extension ms-python.python && \
code --install-extension eamodio.gitlens && \
code --install-extension formulahendry.auto-rename-tag && \
code --install-extension usernamehw.errorlens && \
code --install-extension rangav.vscode-thunder-client && \
code --install-extension pkief.material-icon-theme && \
code --install-extension ms-azuretools.vscode-docker

# Yüklü eklentileri doğrula (en az 10 tane olmalı)
code --list-extensions | wc -l
# Beklenen: 10 veya daha fazla

# Eklenti listesini gör
code --list-extensions
```
:::

### 1.7 Docker Desktop Kurulumu

Docker, uygulamaları container'lar içinde çalıştırmana olanak tanır. Veritabanları, servisler ve tüm geliştirme ortamını container olarak çalıştırabilirsin.

**Ön koşul: WSL 2 (Windows Subsystem for Linux)**

Docker Desktop, WSL 2 backend kullanır. Önce WSL'i etkinleştir:

:::code[bash]{title="WSL 2 Etkinleştirme (PowerShell - Yönetici olarak)"}
# PowerShell'i Yönetici olarak aç (Başlat > "PowerShell" ara > Yönetici olarak çalıştır)

# WSL'i etkinleştir ve varsayılan olarak Ubuntu kur
wsl --install

# Bilgisayarı yeniden başlat (zorunlu)
# Yeniden başlatma sonrası Ubuntu kurulumu otomatik başlayacak
# Kullanıcı adı ve şifre belirlemeniz istenecek
:::

**Docker Desktop kurulumu:**

1. https://www.docker.com/products/docker-desktop/ adresine git
2. "Download for Windows" butonuna tıkla
3. İndirilen `.exe` dosyasını çalıştır
4. "Use WSL 2 instead of Hyper-V" seçeneğinin işaretli olduğundan emin ol
5. Kurulumu tamamla ve bilgisayarı yeniden başlat

:::code[bash]{title="Docker Kurulum Doğrulama"}
# Docker sürümünü kontrol et
docker --version
# Beklenen: Docker version 27.x.x, build xxxxxxx

# Docker Compose sürümünü kontrol et
docker compose version
# Beklenen: Docker Compose version v2.x.x

# Docker'ın çalıştığını test et
docker run hello-world
# Beklenen: "Hello from Docker!" mesajı ve açıklama metni

# Çalışan container'ları listele
docker ps
# Beklenen: Boş tablo (henüz çalışan container yok)
:::

:::beginner-mistake
Docker Desktop çalışmıyorsa ve "WSL 2 is not installed" hatası alıyorsan, önce PowerShell'i yönetici olarak açıp `wsl --install` komutunu çalıştır ve bilgisayarı yeniden başlat. Docker Desktop, WSL 2 olmadan Windows'ta çalışmaz.
:::

:::exercise
### Alıştırma 4: Docker Test

Docker'ın doğru çalıştığını test et:

```bash
# 1. Docker servisinin çalıştığını kontrol et
docker info | head -5
# Beklenen: Server bilgileri görünmeli

# 2. hello-world container'ını çalıştır
docker run hello-world
# Beklenen: "Hello from Docker!" mesajı

# 3. Bir nginx web sunucusu başlat
docker run -d -p 8080:80 --name test-nginx nginx
# Beklenen: Container ID (uzun hex string)

# 4. Tarayıcıda http://localhost:8080 adresini aç
# "Welcome to nginx!" sayfası görünmeli

# 5. Çalışan container'ları gör
docker ps
# Beklenen: test-nginx container'ı listede

# 6. Container'ı durdur ve sil
docker stop test-nginx
docker rm test-nginx

# 7. hello-world ve nginx image'lerini temizle
docker image rm hello-world nginx
```
:::

### 1.8 Tüm Windows Araçlarının Özet Doğrulaması

:::exercise
### Alıştırma 5: Windows Ortam Doğrulama (Kapsamlı)

Tüm kurulumları tek seferde doğrula:

```bash
echo "========================================="
echo "  Geliştirme Ortamı Durum Raporu"
echo "========================================="
echo ""

echo "--- Git ---"
git --version

echo ""
echo "--- Node.js ---"
node --version

echo ""
echo "--- npm ---"
npm --version

echo ""
echo "--- pnpm ---"
pnpm --version

echo ""
echo "--- Python ---"
python --version

echo ""
echo "--- pip ---"
pip --version

echo ""
echo "--- VS Code ---"
code --version | head -1

echo ""
echo "--- Docker ---"
docker --version

echo ""
echo "--- Docker Compose ---"
docker compose version

echo ""
echo "========================================="
echo "  Tüm araçlar kontrol edildi!"
echo "========================================="

# Her komut bir sürüm numarası döndürüyorsa ortamın hazır demektir.
# "command not found" hatası alan araçları yeniden kur.
```
:::

---

## Bölüm 2: macOS Kurulumu

macOS kullanıyorsan bu bölümü takip et. macOS'ta araç kurulumu genellikle **Homebrew** paket yöneticisi üzerinden yapılır.

### 2.1 Homebrew Kurulumu

Homebrew, macOS'un resmi olmayan ama fiilen standart paket yöneticisidir.

:::code[bash]{title="Homebrew Kurulumu - macOS"}
# Homebrew'ı kur (Terminal.app'i aç ve yapıştır)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Kurulum sonrası PATH'e ekle (M1/M2/M3 Mac için)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Doğrulama
brew --version
# Beklenen: Homebrew 4.x.x
:::

### 2.2 Temel Araçlar (Homebrew ile)

:::code[bash]{title="macOS Araç Kurulumu"}
# Git (macOS'ta Xcode CLI tools ile gelir, ama güncelleyelim)
brew install git

# Git yapılandırma (Windows bölümündeki ile aynı)
git config --global user.name "Senin Adın"
git config --global user.email "senin@email.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"

# nvm kurulumu (Node.js sürüm yöneticisi)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Terminal'i kapat ve yeniden aç, sonra:
nvm install 22
nvm use 22
nvm alias default 22

# Doğrulama
node --version   # v22.x.x
npm --version    # 10.x.x

# pnpm
npm install -g pnpm

# pyenv kurulumu (Python sürüm yöneticisi)
brew install pyenv

# Shell yapılandırmasına ekle
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Terminal'i yeniden aç
pyenv install 3.13
pyenv global 3.13

# Doğrulama
python --version   # Python 3.13.x

# VS Code
brew install --cask visual-studio-code

# Docker Desktop
brew install --cask docker

# Tek seferde birden fazla araç da kurabilirsin:
# brew install git pyenv
# brew install --cask visual-studio-code docker
:::

:::tip
macOS'ta Homebrew, Windows'taki "tek tek indirip kur" sürecini otomatikleştirir. `brew install` komutuyla neredeyse her aracı kurabilirsin. `brew update && brew upgrade` ile tüm araçlarını güncel tutabilirsin.
:::

---

## Bölüm 3: Linux Kurulumu (Kısa)

Linux (Ubuntu/Debian) kullanıyorsan, çoğu araç `apt` paket yöneticisi veya doğrudan indirme ile kurulur.

:::code[bash]{title="Linux (Ubuntu/Debian) Araç Kurulumu"}
# Sistem paketlerini güncelle
sudo apt update && sudo apt upgrade -y

# Git
sudo apt install -y git
git config --global user.name "Senin Adın"
git config --global user.email "senin@email.com"
git config --global init.defaultBranch main

# nvm ile Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22

# pnpm
npm install -g pnpm

# pyenv ile Python
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
  libffi-dev liblzma-dev

curl https://pyenv.run | bash

# ~/.bashrc sonuna ekle:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

pyenv install 3.13
pyenv global 3.13

# VS Code
sudo apt install -y software-properties-common apt-transport-https wget
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt update
sudo apt install -y code

# Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Oturumu kapat ve yeniden aç (docker komutunu sudo olmadan kullanmak için)
:::

---

## Bölüm 4: VS Code Yapılandırması

VS Code'u doğru yapılandırmak, geliştirme hızını dramatik şekilde artırır.

### 4.1 settings.json Ayarları

VS Code'da `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`) tuşlarına bas, "Preferences: Open User Settings (JSON)" yaz ve seç.

:::code[json]{title="VS Code settings.json - Önerilen Ayarlar"}
{
  // Editör Temel Ayarları
  "editor.fontSize": 15,
  "editor.fontFamily": "'Cascadia Code', 'Fira Code', Consolas, monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.wordWrap": "on",
  "editor.minimap.enabled": false,
  "editor.lineNumbers": "on",
  "editor.renderWhitespace": "selection",
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "editor.linkedEditing": true,
  "editor.stickyScroll.enabled": true,
  "editor.cursorBlinking": "smooth",
  "editor.cursorSmoothCaretAnimation": "on",
  "editor.smoothScrolling": true,

  // Kaydetme Ayarları
  "editor.formatOnSave": true,
  "editor.formatOnPaste": false,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "files.autoSave": "onFocusChange",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,

  // Terminal Ayarları
  "terminal.integrated.fontSize": 14,
  "terminal.integrated.defaultProfile.windows": "Git Bash",
  "terminal.integrated.cursorBlinking": true,

  // Dosya Gezgini
  "explorer.confirmDelete": false,
  "explorer.confirmDragAndDrop": false,
  "explorer.compactFolders": false,

  // Tema ve Görünüm
  "workbench.iconTheme": "material-icon-theme",
  "workbench.colorTheme": "One Dark Pro",
  "workbench.startupEditor": "none",

  // Dil Ayarları
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.tabSize": 4
  },
  "[markdown]": {
    "editor.wordWrap": "on"
  },

  // Emmet
  "emmet.includeLanguages": {
    "javascript": "javascriptreact"
  },

  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true
}
:::

:::exercise
### Alıştırma 6: VS Code settings.json Yapılandırma

VS Code ayarlarını yapılandır:

```
1. VS Code'u aç
2. Ctrl+Shift+P tuşlarına bas
3. "Preferences: Open User Settings (JSON)" yaz ve seç
4. Yukarıdaki JSON'u dosyaya yapıştır
5. Ctrl+S ile kaydet
6. VS Code'u kapat ve yeniden aç

Doğrulama:
- Yeni bir .js dosyası oluştur ve kaydet. Prettier otomatik formatlama yapmalı.
- Terminal panelini aç (Ctrl+`). Git Bash açılmalı.
- Bir JSON dosyası oluştur, kaydet. Otomatik formatlanmalı.
```
:::

### 4.2 Klavye Kısayolları (Keyboard Shortcuts)

Bu kısayolları ezberle - her gün yüzlerce kez kullanacaksın:

:::code[text]{title="VS Code Temel Klavye Kısayolları"}
=== Dosya İşlemleri ===
Ctrl+N            Yeni dosya oluştur
Ctrl+O            Dosya aç
Ctrl+S            Kaydet
Ctrl+Shift+S      Farklı kaydet
Ctrl+W            Sekmeyi kapat
Ctrl+Shift+T      Son kapatılan sekmeyi aç

=== Düzenleme ===
Ctrl+X            Satırı kes (seçim yoksa tüm satır)
Ctrl+C            Satırı kopyala (seçim yoksa tüm satır)
Ctrl+Shift+K      Satırı sil
Alt+Yukarı/Aşağı  Satırı yukarı/aşağı taşı
Shift+Alt+Yukarı  Satırı yukarı kopyala
Shift+Alt+Aşağı   Satırı aşağı kopyala
Ctrl+D            Sonraki aynı kelimeyi seç (multi-cursor)
Ctrl+Shift+L      Tüm aynı kelimeleri seç
Ctrl+/            Satırı yorum satırı yap/geri al
Ctrl+Z            Geri al
Ctrl+Shift+Z      İleri al

=== Navigasyon ===
Ctrl+P            Hızlı dosya aç (dosya adı yaz)
Ctrl+Shift+P      Komut paleti
Ctrl+G            Satır numarasına git
Ctrl+Shift+F      Tüm dosyalarda ara
Ctrl+Shift+E      Dosya gezginini aç/kapat
Ctrl+Shift+X      Eklentiler panelini aç
Ctrl+`            Terminal panelini aç/kapat
Ctrl+B            Yan çubuğu aç/kapat

=== Multi-Cursor (Çoklu İmleç) ===
Alt+Tıklama       Tıklanan yere ek imleç ekle
Ctrl+Alt+Yukarı   Üst satıra imleç ekle
Ctrl+Alt+Aşağı    Alt satıra imleç ekle
Ctrl+D            Seçili kelimeyi bul, bir sonrakini de seç
:::

### 4.3 Multi-Cursor Editing

Multi-cursor, VS Code'un en güçlü özelliklerinden biridir. Birden fazla yeri aynı anda düzenleyebilirsin.

:::exercise
### Alıştırma 7: Multi-Cursor Pratik

VS Code'da yeni bir dosya oluştur ve aşağıdaki metni yapıştır, sonra görevleri yap:

```javascript
// Bu dosyayı VS Code'da oluştur: multi-cursor-test.js

const user1 = "Ali";
const user2 = "Ayşe";
const user3 = "Mehmet";
const user4 = "Fatma";
const user5 = "Ahmet";
```

Görevler:
1. "user" kelimesinin birini seç, sonra Ctrl+D ile tüm "user" kelimelerini seç.
   Hepsini "person" olarak değiştir.

2. İlk satıra tıkla, Ctrl+Alt+Aşağı ile 5 imleç oluştur.
   Tüm satırların sonuna "; // değiştirildi" ekle.

3. Alt+Tıklama ile 3 farklı yere imleç koy ve aynı anda yazı yaz.

4. Ctrl+Shift+L ile dosyadaki tüm "const" kelimelerini seç ve "let" olarak değiştir.
:::

### 4.4 Terminal Entegrasyonu

VS Code'un entegre terminali, editör ve komut satırını tek pencerede birleştirir.

:::code[text]{title="VS Code Terminal Kısayolları"}
Ctrl+`               Terminal panelini aç/kapat
Ctrl+Shift+`         Yeni terminal oluştur
Ctrl+Shift+5         Terminal'i böl (yan yana iki terminal)
Ctrl+PageUp/Down     Terminal sekmeleri arasında geçiş
Alt+Yukarı/Aşağı     Terminal boyutunu ayarla (sürükle)

# Terminal'de çalışırken:
# Metin seçmek için: Shift+Yukarı/Aşağı veya fare ile seç
# Kopyalamak için: Ctrl+C (komut çalışmıyorken) veya Ctrl+Shift+C
# Yapıştırmak için: Ctrl+V veya Ctrl+Shift+V
:::

:::tip
VS Code'da birden fazla terminal açabilirsin. Bir terminal'de frontend sunucunu çalıştırırken diğerinde backend sunucunu, üçüncüsünde Git komutlarını kullanabilirsin. Her terminal'e isim de verebilirsin (terminal sekmesine sağ tıkla > "Rename").
:::

---

## Bölüm 5: İlk Proje Oluşturma Testi

Tüm araçları kurdun, şimdi gerçekten çalıştıklarını kanıtlayalım.

### 5.1 Node.js Projesi Oluştur ve Çalıştır

:::exercise
### Alıştırma 8: İlk Node.js Projesi

Sıfırdan bir Node.js projesi oluştur ve çalıştır:

```bash
# 1. Proje dizini oluştur
mkdir ~/projects
mkdir ~/projects/merhaba-node
cd ~/projects/merhaba-node

# 2. Node.js projesi başlat
pnpm init
# Beklenen: package.json dosyası oluşturuldu

# 3. Ana dosyayı oluştur
cat > index.js << 'EOF'
// İlk Node.js programın
const http = require("http");

const PORT = 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
  res.end("<h1>Merhaba Dünya!</h1><p>Node.js sunucun çalışıyor.</p>");
});

server.listen(PORT, () => {
  console.log(`Sunucu http://localhost:${PORT} adresinde çalışıyor`);
});
EOF

# 4. Projeyi çalıştır
node index.js
# Beklenen: Sunucu http://localhost:3000 adresinde çalışıyor

# 5. Tarayıcıda http://localhost:3000 adresini aç
# "Merhaba Dünya!" yazısını görmelisin

# 6. Terminal'de Ctrl+C ile sunucuyu durdur

# 7. package.json'a start script'i ekle
# package.json dosyasını VS Code'da aç ve "scripts" bölümüne ekle:
#   "start": "node index.js"

# 8. Script ile çalıştır
pnpm start
# Aynı sonucu görmeli
# Ctrl+C ile durdur
```
:::

### 5.2 Python Projesi Oluştur ve Çalıştır

:::exercise
### Alıştırma 9: İlk Python Projesi

Sıfırdan bir Python projesi oluştur ve çalıştır:

```bash
# 1. Proje dizini oluştur
mkdir ~/projects/merhaba-python
cd ~/projects/merhaba-python

# 2. Virtual environment oluştur (Python'da izole ortam)
python -m venv venv

# 3. Virtual environment'ı aktifleştir
# Windows (Git Bash):
source venv/Scripts/activate
# macOS/Linux:
# source venv/bin/activate

# Beklenen: Terminal'de (venv) ön eki görünür

# 4. requirements.txt oluştur
cat > requirements.txt << 'EOF'
flask==3.1.0
EOF

# 5. Bağımlılıkları yükle
pip install -r requirements.txt
# Beklenen: Flask ve bağımlılıkları yüklenir

# 6. Ana dosyayı oluştur
cat > app.py << 'EOF'
from flask import Flask

app = Flask(__name__)

@app.route("/")
def merhaba():
    return "<h1>Merhaba Dünya!</h1><p>Python Flask sunucun çalışıyor.</p>"

@app.route("/api/durum")
def durum():
    return {"durum": "aktif", "mesaj": "API çalışıyor"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
EOF

# 7. Uygulamayı çalıştır
python app.py
# Beklenen: * Running on http://127.0.0.1:5000

# 8. Tarayıcıda http://localhost:5000 adresini aç
# "Merhaba Dünya!" yazısını görmelisin

# 9. http://localhost:5000/api/durum adresini de kontrol et
# JSON çıktısı: {"durum": "aktif", "mesaj": "API çalışıyor"}

# 10. Ctrl+C ile durdur

# 11. Virtual environment'tan çık
deactivate
```
:::

### 5.3 Git Repo Oluştur, Commit, Push

:::exercise
### Alıştırma 10: Git Workflow (Tam Döngü)

Node.js projenle Git workflow'unu test et:

```bash
# 1. Proje dizinine git
cd ~/projects/merhaba-node

# 2. .gitignore dosyası oluştur
cat > .gitignore << 'EOF'
node_modules/
.env
.DS_Store
*.log
dist/
EOF

# 3. Git repo'su başlat
git init
# Beklenen: Initialized empty Git repository in ...

# 4. Durumu kontrol et
git status
# Beklenen: Untracked files listesi (index.js, package.json, .gitignore)

# 5. Dosyaları staging'e ekle
git add .

# 6. İlk commit
git commit -m "feat: ilk Node.js projesi oluşturuldu"
# Beklenen: [main (root-commit) xxxxxxx] feat: ilk Node.js projesi oluşturuldu

# 7. Commit geçmişini gör
git log --oneline
# Beklenen: xxxxxxx feat: ilk Node.js projesi oluşturuldu

# 8. Bir değişiklik yap
cat >> index.js << 'EOF'

// Sunucu bilgisi endpoint'i
console.log("Node.js sürümü:", process.version);
EOF

# 9. Değişikliği gör
git diff
# Beklenen: Eklenen satırlar yeşil ile gösterilir

# 10. İkinci commit
git add .
git commit -m "feat: sunucu bilgisi log'u eklendi"

# 11. Geçmişi gör
git log --oneline
# Beklenen: İki commit görünmeli

# === GitHub'a Push (opsiyonel - GitHub hesabın varsa) ===
# 12. GitHub'da yeni repo oluştur (github.com > New Repository)
# 13. Remote ekle ve push et:
# git remote add origin https://github.com/KULLANICI/merhaba-node.git
# git push -u origin main
```
:::

### 5.4 Docker ile Basit Container Çalıştır

:::exercise
### Alıştırma 11: Docker ile Container Çalıştırma

Node.js projeni Docker container'ı olarak çalıştır:

```bash
# 1. Proje dizinine git
cd ~/projects/merhaba-node

# 2. Dockerfile oluştur
cat > Dockerfile << 'EOF'
FROM node:22-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "index.js"]
EOF

# 3. .dockerignore dosyası oluştur
cat > .dockerignore << 'EOF'
node_modules
.git
.gitignore
EOF

# 4. Docker image'ı oluştur (build et)
docker build -t merhaba-node .
# Beklenen: Successfully built xxxxxxxx
# Beklenen: Successfully tagged merhaba-node:latest

# 5. Container'ı çalıştır
docker run -d -p 3000:3000 --name merhaba-app merhaba-node
# Beklenen: Container ID (uzun hex string)

# 6. Tarayıcıda http://localhost:3000 aç
# "Merhaba Dünya!" sayfası görünmeli

# 7. Container loglarını gör
docker logs merhaba-app
# Beklenen: Sunucu http://localhost:3000 adresinde çalışıyor

# 8. Container'ı durdur ve sil
docker stop merhaba-app
docker rm merhaba-app

# 9. Image'ı sil (opsiyonel)
docker image rm merhaba-node
```
:::

---

## Sık Karşılaşılan Sorunlar ve Çözümleri

### "command not found" Hatası

:::code[bash]{title="PATH Sorunları ve Çözümleri"}
# Sorun: git, node, python gibi komutlar tanınmıyor
# Neden: Araç PATH ortam değişkenine eklenmemiş

# Windows'ta PATH'i kontrol et (PowerShell):
# $env:PATH -split ";" | Select-String "git"
# $env:PATH -split ";" | Select-String "node"

# Git Bash'te PATH'i kontrol et:
echo $PATH | tr ':' '\n' | grep -i git
echo $PATH | tr ':' '\n' | grep -i node
echo $PATH | tr ':' '\n' | grep -i python

# Çözüm 1: Terminal'i kapat ve yeniden aç
# (Çoğu kurulum PATH'i günceller ama aktif terminal'e yansımaz)

# Çözüm 2: Bilgisayarı yeniden başlat
# (Bazen sadece terminal yeniden başlatma yetmez)

# Çözüm 3: Manuel PATH ekleme (Windows)
# Başlat > "Ortam değişkenleri" ara > "Sistem ortam değişkenlerini düzenle"
# > "Ortam Değişkenleri" > "Path" > "Düzenle" > "Yeni"
# > Aracın yolunu ekle (ör: C:\Program Files\Git\cmd)
:::

### Node.js / npm Sorunları

:::code[bash]{title="Node.js Sorun Giderme"}
# Sorun: "nvm is not recognized"
# Çözüm: Terminal'i kapat, yeniden aç. Hâlâ yoksa nvm'i yeniden kur.

# Sorun: "npm ERR! EACCES permission denied"
# Çözüm: Windows'ta Terminal'i yönetici olarak çalıştır

# Sorun: node_modules sorunları
# Çözüm: Sil ve yeniden kur
rm -rf node_modules
rm -f pnpm-lock.yaml   # veya package-lock.json
pnpm install            # veya npm install

# Sorun: "The engine 'node' is incompatible"
# Çözüm: Doğru Node.js sürümünü kullan
nvm install 22
nvm use 22
:::

### Python Sorunları

:::code[bash]{title="Python Sorun Giderme"}
# Sorun: "python" komutu çalışmıyor ama "python3" çalışıyor (macOS/Linux)
# Çözüm: Alias ekle
echo 'alias python=python3' >> ~/.bashrc
echo 'alias pip=pip3' >> ~/.bashrc
source ~/.bashrc

# Sorun: "pip" ModuleNotFoundError
# Çözüm:
python -m ensurepip --upgrade

# Sorun: Virtual environment aktifleşmiyor (Windows)
# Çözüm: Git Bash'te:
source venv/Scripts/activate
# PowerShell'de:
# .\venv\Scripts\Activate.ps1
# CMD'de:
# venv\Scripts\activate.bat
:::

### Docker Sorunları

:::code[bash]{title="Docker Sorun Giderme"}
# Sorun: "docker: command not found"
# Çözüm: Docker Desktop'ın çalıştığından emin ol (sistem tepsisindeki ikon)

# Sorun: "Cannot connect to the Docker daemon"
# Çözüm: Docker Desktop'ı başlat ve tamamen yüklenmesini bekle (1-2 dakika)

# Sorun: "WSL 2 installation is incomplete"
# Çözüm (PowerShell - Yönetici):
# wsl --update
# Bilgisayarı yeniden başlat

# Sorun: Port çakışması ("port is already in use")
# Çözüm: O portu kullanan process'i bul ve durdur
# Windows:
# netstat -ano | findstr :3000
# taskkill /PID <PID> /F
# macOS/Linux:
# lsof -i :3000
# kill -9 <PID>
:::

### VS Code Sorunları

:::code[bash]{title="VS Code Sorun Giderme"}
# Sorun: "code" komutu çalışmıyor
# Çözüm 1: VS Code'u aç > Ctrl+Shift+P > "Shell Command: Install 'code' command in PATH"
# Çözüm 2: Terminal'i yeniden başlat

# Sorun: Eklenti yüklenmiyor
# Çözüm: VS Code'u yönetici olarak çalıştır ve tekrar dene

# Sorun: Prettier formatlamıyor
# Kontrol 1: Dosya sağ alt köşesinde formatter'ı kontrol et
# Kontrol 2: Ctrl+Shift+P > "Format Document With..." > Prettier seç
# Kontrol 3: settings.json'da "editor.formatOnSave": true olduğundan emin ol

# Sorun: Terminal'de Git Bash görünmüyor
# Çözüm: settings.json'a ekle:
# "terminal.integrated.defaultProfile.windows": "Git Bash"
:::

---

## Özet ve Kontrol Listesi

Ortamının hazır olduğunu doğrulamak için bu kontrol listesini kullan:

:::code[text]{title="Ortam Kurulum Kontrol Listesi"}
[Temel Araçlar]
[ ] Git kuruldu ve yapılandırıldı (user.name, user.email)
[ ] Node.js 22 LTS kuruldu (nvm ile)
[ ] pnpm kuruldu
[ ] Python 3.13 kuruldu
[ ] VS Code kuruldu ve PATH'te

[VS Code Eklentileri]
[ ] ESLint
[ ] Prettier
[ ] Tailwind CSS IntelliSense
[ ] Python
[ ] GitLens
[ ] Auto Rename Tag
[ ] Error Lens
[ ] Thunder Client
[ ] Material Icon Theme
[ ] Docker

[VS Code Ayarları]
[ ] settings.json yapılandırıldı
[ ] Format on save aktif
[ ] Terminal varsayılan profili Git Bash
[ ] Font ve tema ayarlandı

[Docker]
[ ] Docker Desktop kuruldu
[ ] WSL 2 etkin (Windows)
[ ] docker run hello-world çalışıyor

[Test Projeleri]
[ ] Node.js projesi çalıştı (localhost:3000)
[ ] Python projesi çalıştı (localhost:5000)
[ ] Git repo oluşturuldu ve commit yapıldı
[ ] Docker container çalıştırıldı

Tüm kutucuklar işaretliyse, geliştirme ortamın hazır!
Bir sonraki ders: Terminal/CLI komutlarını öğrenmeye başla.
:::

:::deha-tip
Ortam kurulumunu bir kere doğru yap ve bunu belgele. İleride yeni bir bilgisayara geçtiğinde veya ortamını sıfırdan kurmak istediğinde bu belgeye dönebilirsin. Hatta daha iyisi: kurulum adımlarını bir shell script'e dönüştür ve otomatikleştir. Bu, DevOps düşüncesinin ilk adımıdır.
:::
