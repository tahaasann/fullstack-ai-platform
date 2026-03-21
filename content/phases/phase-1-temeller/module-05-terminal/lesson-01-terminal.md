---
id: mod-05-terminal/lesson-01
title: "Terminal/CLI: Linux Komutları ve Shell Temelleri"
estimated_minutes: 50
tags: ["terminal", "cli", "linux", "bash", "shell-scripting", "tmux"]
prerequisites: ["mod-01-internet/lesson-01"]
order: 1
---

# Terminal/CLI: Linux Komutları ve Shell Temelleri

:::realworld
Her profesyonel geliştirici günün büyük bir bölümünü terminalde geçirir. Server'a bağlanmak, dosya yönetmek, Git komutları çalıştırmak, Docker container'ları yönetmek, CI/CD pipeline'ları debug etmek... Hepsi terminal üzerinden yapılır. GUI araçları hız ve verimlilik konusunda terminal'in yanına bile yaklaşamaz. Bu derste, terminal'i bir profesyonel gibi kullanmayı öğreneceksin. Mülakata girdiğinde "terminal kullanmayı biliyorum" demek ile gerçekten bilmek arasındaki farkı kapatacaksın.
:::

## Neden Terminal?

Bir full stack developer olarak terminal bilmek zorunludur, seçenek değil:

- **Server yönetimi:** Production server'larının %99'u Linux tabanlıdır ve sadece terminal erişimi vardır
- **Otomasyon:** Tekrarlayan görevleri script'lerle otomatikleştirebilirsin
- **Hız:** Fare ile 10 tıklama gerektiren işlemi tek komutla yapabilirsin
- **DevOps:** Docker, Kubernetes, CI/CD pipeline'ları terminal tabanlıdır
- **Debug:** Log dosyalarını analiz etmek, process'leri yönetmek terminal gerektirir

:::deha-tip
Deha seviyesi geliştiriciler terminal'i "yedek araç" olarak değil, "birincil araç" olarak kullanır. VS Code'un entegre terminal'ini her zaman açık tutarlar. Alias'lar ve shell script'ler ile kendi workflow'larını oluştururlar. Terminal, onların eli ayağıdır.
:::

## Temel Dosya ve Dizin Komutları

### ls - Dosya ve Dizin Listeleme

:::code[bash]{title="ls Komutu ve Flagleri"}
# Temel kullanım
ls                    # Mevcut dizindeki dosyaları listele
ls -l                 # Detaylı liste (izinler, boyut, tarih)
ls -la                # Gizli dosyalar dahil detaylı liste
ls -lh                # Boyutları okunabilir formatta göster (KB, MB, GB)
ls -lt                # Tarihe göre sırala (en yeni üstte)
ls -lR                # Alt dizinleri de recursive olarak listele
ls -S                 # Boyuta göre sırala (en büyük üstte)

# Pratik örnekler
ls -la ~/.ssh/        # SSH anahtarlarını kontrol et
ls -lh /var/log/      # Log dosyalarının boyutlarını gör
ls *.js               # Sadece JavaScript dosyalarını listele
:::

:::beginner-mistake
Yaygın hata: `ls -la` çıktısındaki izin bilgilerini okuyamamak. `-rw-r--r--` formatında ilk karakter dosya tipi (d=dizin, -=dosya, l=link), sonraki 9 karakter üçer grupla owner/group/others izinlerini gösterir.
:::

### cd - Dizin Değiştirme

:::code[bash]{title="cd Komutu"}
cd /home/user/projects    # Mutlak yol ile git
cd projects               # Göreceli yol ile git
cd ..                     # Bir üst dizine çık
cd ../..                  # İki üst dizine çık
cd ~                      # Home dizinine git
cd -                      # Önceki dizine geri dön
cd                        # Home dizinine git (cd ~ ile aynı)

# Tab completion kullan! Yazarken Tab tuşuna basarak otomatik tamamla
cd /ho<TAB>/us<TAB>/pro<TAB>
:::

### mkdir - Dizin Oluşturma

:::code[bash]{title="mkdir Komutu"}
mkdir my-project                      # Tek dizin oluştur
mkdir -p src/components/ui             # İç içe dizinleri oluştur (parent dahil)
mkdir -p {src,tests,docs,config}       # Birden fazla dizin oluştur
mkdir -p project/{src/{components,utils,styles},tests,docs}  # Karmaşık yapı

# Proje yapısı oluşturma
mkdir -p my-app/{src/{components,pages,hooks,utils,styles},public,tests/__tests__}
:::

### rm - Dosya ve Dizin Silme

:::code[bash]{title="rm Komutu - DİKKATLİ KULLAN!"}
rm file.txt               # Dosya sil (onay sormaz!)
rm -i file.txt             # Onay sorarak sil
rm -r my-folder/           # Dizini ve içindekileri recursive sil
rm -rf my-folder/          # Zorla sil (onay sormadan, hata vermeden)
rm *.log                   # Tüm .log dosyalarını sil
rm -rf node_modules/       # node_modules'ü sil (çok yaygın)

# GÜVENLİ SİLME
rm -ri important-folder/   # Recursive ama her dosya için onay iste
:::

:::beginner-mistake
**UYARI:** `rm -rf /` komutu TÜM sistemi siler! `rm -rf` komutunu kullanırken yolu mutlaka kontrol et. Production server'da bu komut felaket olabilir. Alışkanlık olarak önce `ls` ile sileceklerin dosyaları görüntüle, sonra `rm` ile sil.
:::

### cp ve mv - Kopyalama ve Taşıma

:::code[bash]{title="cp ve mv Komutları"}
# Kopyalama
cp file.txt backup.txt              # Dosya kopyala
cp -r src/ src-backup/              # Dizini recursive kopyala
cp -i file.txt dest/                # Üzerine yazacaksa sor
cp file.txt file2.txt dest/         # Birden fazla dosyayı kopyala

# Taşıma / Yeniden adlandırma
mv old-name.txt new-name.txt        # Dosyayı yeniden adlandır
mv file.txt ~/Documents/            # Dosyayı taşı
mv -i file.txt dest/                # Üzerine yazacaksa sor
mv src/old-component.jsx src/NewComponent.jsx  # Component dosyasını yeniden adlandır
:::

### cat - Dosya İçeriğini Görüntüleme

:::code[bash]{title="cat ve Alternatifler"}
cat file.txt                  # Dosya içeriğini göster
cat -n file.txt               # Satır numaralarıyla göster
cat file1.txt file2.txt       # İki dosyayı birleştirerek göster
cat > new-file.txt            # Yeni dosya oluştur (Ctrl+D ile bitir)
cat >> existing.txt           # Dosyanın sonuna ekle

# Büyük dosyalar için alternatifler
head -20 file.txt             # İlk 20 satırı göster
tail -20 file.txt             # Son 20 satırı göster
tail -f /var/log/syslog       # Canlı log takibi (follow mode)
less file.txt                 # Sayfalayarak oku (q ile çık)
wc -l file.txt                # Satır sayısını göster
:::

## Arama Komutları

### grep - Metin Arama

:::code[bash]{title="grep Komutu - Metin Arama Silahın"}
# Temel arama
grep "error" log.txt                    # Dosyada "error" ara
grep -i "error" log.txt                 # Büyük/küçük harf duyarsız
grep -r "TODO" src/                     # Dizinde recursive ara
grep -rn "console.log" src/             # Satır numarası ile ara
grep -c "error" log.txt                 # Eşleşme sayısını göster

# Regex ile arama
grep -E "error|warning|fatal" log.txt   # Birden fazla pattern (OR)
grep -v "debug" log.txt                 # Eşleşmeyen satırları göster
grep -l "import React" src/**/*.jsx     # Sadece dosya adlarını göster
grep -A 3 "error" log.txt              # Eşleşmeden sonra 3 satır göster
grep -B 2 "error" log.txt              # Eşleşmeden önce 2 satır göster

# Pratik kullanımlar
grep -rn "API_KEY" .                    # Kodda API key aramak
grep -r "useState" src/components/      # React hook kullanımı aramak
ps aux | grep node                      # Çalışan node process'leri bul
history | grep "docker"                 # Geçmişte docker komutlarını bul
:::

:::tip
Modern alternatif: `ripgrep (rg)` komutu grep'ten çok daha hızlıdır ve .gitignore'u otomatik olarak tanır. Kurulum: `cargo install ripgrep` veya `apt install ripgrep`.
:::

### find - Dosya Arama

:::code[bash]{title="find Komutu - Dosya Sistemi Arama"}
# İsme göre ara
find . -name "*.js"                     # .js dosyalarını bul
find . -name "*.test.js"                # Test dosyalarını bul
find . -iname "readme*"                 # Büyük/küçük harf duyarsız

# Tipe göre ara
find . -type f                          # Sadece dosyalar
find . -type d                          # Sadece dizinler
find . -type l                          # Sadece symbolic linkler

# Boyut ve zaman filtreleri
find . -size +100M                      # 100MB'dan büyük dosyalar
find . -mtime -7                        # Son 7 günde değişen dosyalar
find . -newer reference.txt             # reference.txt'den yeni dosyalar

# find + exec (bulduklarına komut uygula)
find . -name "*.log" -delete            # Tüm log dosyalarını sil
find . -name "*.js" -exec wc -l {} \;   # JS dosyalarının satır sayısı
find . -name "node_modules" -type d -prune -exec rm -rf {} \;  # Tüm node_modules sil

# Hariç tutma
find . -name "*.js" -not -path "*/node_modules/*"  # node_modules hariç JS dosyaları
:::

## Dosya İzinleri

### chmod - İzin Değiştirme

:::concept[File Permissions (İng: Dosya İzinleri)]
Linux'ta her dosyanın owner (sahip), group (grup) ve others (diğerleri) için ayrı read (okuma), write (yazma) ve execute (çalıştırma) izinleri vardır.

**Türkçe karşılığı:** Dosya İzinleri / Erişim Hakları
**Ne işe yarar:** Dosyalara kimin erişebileceğini ve ne yapabileceğini kontrol eder
**Gerçek hayat benzetmesi:** Bir binadaki kapı kartı sistemi - herkesin farklı odalara erişimi var
:::

:::code[bash]{title="chmod ve chown Komutları"}
# Sembolik mod
chmod +x script.sh                # Çalıştırma izni ekle
chmod u+x script.sh               # Sadece owner'a çalıştırma izni
chmod go-w file.txt                # Group ve others'dan yazma izni kaldır
chmod u+rwx,go+rx file.txt         # Owner: rwx, diğerleri: rx

# Sayısal mod (Octal)
# r=4, w=2, x=1 → topla
chmod 755 script.sh                # rwxr-xr-x (owner: tam, diğerleri: oku+çalıştır)
chmod 644 file.txt                 # rw-r--r-- (owner: oku+yaz, diğerleri: sadece oku)
chmod 600 ~/.ssh/id_rsa            # rw------- (sadece owner okuyup yazabilir)
chmod 777 file.txt                 # rwxrwxrwx (BUNU YAPMA! Güvenlik riski!)

# Sahiplik değiştirme
chown user:group file.txt          # Dosya sahibini ve grubunu değiştir
chown -R user:group project/       # Recursive olarak değiştir
chown user file.txt                # Sadece sahibi değiştir
:::

:::beginner-mistake
`chmod 777` asla production'da kullanma! Bu herkesin dosyayı okuyup, yazıp, çalıştırabileceği anlamına gelir. SSH key'lerin 600, script'lerin 755, config dosyalarının 644 olması gerekir.
:::

## Pipe ve Redirection

### Pipe ( | ) - Komutları Zincirleme

:::concept[Pipe (İng: Pipe)]
Pipe operatörü (|), bir komutun çıktısını (stdout) başka bir komutun girdisi (stdin) olarak yönlendirir. Komutları bir boru hattı gibi birbirine bağlar.

**Türkçe karşılığı:** Boru / Boru Hattı
**Ne işe yarar:** Birden fazla komutu zincirleme bağlayarak güçlü komut kombinasyonları oluşturur
**Gerçek hayat benzetmesi:** Fabrikada montaj hattı - her istasyon bir işlem yapar ve sonucu bir sonraki istasyona iletir
:::

:::code[bash]{title="Pipe Örnekleri"}
# Temel pipe kullanımı
ls -la | grep ".js"                     # JS dosyalarını filtrele
cat log.txt | grep "error" | wc -l      # Hata sayısını say
ps aux | grep node | awk '{print $2}'   # Node process ID'lerini al

# Sıralama ve tekil
cat names.txt | sort                    # Alfabetik sırala
cat names.txt | sort | uniq             # Tekrarları kaldır
cat names.txt | sort | uniq -c | sort -rn  # En çok tekrarlananı bul

# Pratik geliştirici kullanımları
history | grep "git" | tail -20         # Son 20 git komutunu gör
find . -name "*.js" | wc -l             # JS dosya sayısını say
cat package.json | python3 -m json.tool  # JSON'u güzel formatla
du -sh */ | sort -rh | head -10         # En büyük 10 dizini bul
pnpm list --depth=0 2>/dev/null | grep -v "^$"  # Kurulu paketleri listele
:::

### Redirection - Yönlendirme

:::code[bash]{title="Redirection Operatörleri"}
# Stdout yönlendirme
echo "Hello" > file.txt                 # Dosyaya yaz (üzerine yazar!)
echo "World" >> file.txt                # Dosyanın sonuna ekle
ls -la > directory-listing.txt          # Komut çıktısını dosyaya kaydet

# Stdin yönlendirme
sort < unsorted.txt                     # Dosyayı input olarak ver
mysql database < backup.sql             # SQL dosyasını veritabanına yükle

# Stderr yönlendirme
command 2> errors.log                   # Hataları dosyaya yönlendir
command 2>&1                            # Stderr'i stdout'a yönlendir
command > output.log 2>&1               # Her şeyi tek dosyaya yönlendir
command > /dev/null 2>&1                # Tüm çıktıyı sessize al

# Pratik kullanımlar
pnpm install 2>&1 | tee install.log      # Hem ekranda göster hem dosyaya kaydet
find / -name "*.conf" 2>/dev/null       # Permission denied hatalarını gizle
curl -s https://api.example.com | jq '.' > response.json  # API yanıtını kaydet
:::

:::comparison
| Operatör | İşlev | Örnek |
|----------|-------|-------|
| `>` | Stdout'u dosyaya yaz (üzerine yazar) | `echo "hi" > file.txt` |
| `>>` | Stdout'u dosyaya ekle (append) | `echo "hi" >> file.txt` |
| `<` | Dosyayı stdin olarak oku | `sort < list.txt` |
| `|` | Stdout'u başka komutun stdin'ine bağla | `cat file | grep "x"` |
| `2>` | Stderr'i dosyaya yönlendir | `cmd 2> err.log` |
| `2>&1` | Stderr'i stdout'a yönlendir | `cmd > all.log 2>&1` |
| `/dev/null` | Çıktıyı yok say (kara delik) | `cmd > /dev/null` |

**Tavsiye:** `>` ile `>>` farkını her zaman aklında tut. `>` dosyanın mevcut içeriğini siler!
:::

## Shell Scripting Temelleri

### Değişkenler

:::code[bash]{title="Bash Değişkenleri"}
# Değişken tanımlama (= etrafında boşluk OLMAMALI!)
name="Ahmet"
age=25
project_dir="/home/user/projects"

# Değişken kullanma
echo "Merhaba $name"
echo "Yaş: ${age}"
echo "Proje dizini: ${project_dir}"

# Komut çıktısını değişkene atama
current_date=$(date +%Y-%m-%d)
file_count=$(ls -1 | wc -l)
git_branch=$(git branch --show-current)

echo "Tarih: $current_date"
echo "Dosya sayısı: $file_count"
echo "Branch: $git_branch"

# Ortam değişkenleri
export API_KEY="my-secret-key"
export NODE_ENV="development"
echo $PATH                      # PATH değişkenini göster
echo $HOME                      # Home dizinini göster
:::

:::beginner-mistake
En sık yapılan hata: `name = "Ahmet"` yazmak. Bash'te değişken atamasında `=` etrafında boşluk olmamalı! `name="Ahmet"` doğru kullanımdır. Boşluk koyarsan Bash bunu komut olarak çalıştırmaya çalışır.
:::

### Koşullar (if/else)

:::code[bash]{title="if/else Yapısı"}
#!/bin/bash

# Dosya kontrolü
if [ -f "package.json" ]; then
    echo "Node.js projesi tespit edildi"
    pnpm install
elif [ -f "requirements.txt" ]; then
    echo "Python projesi tespit edildi"
    uv pip install -r requirements.txt
else
    echo "Proje türü belirlenemedi"
fi

# String karşılaştırma
env="production"
if [ "$env" = "production" ]; then
    echo "Production ortamındasın, dikkatli ol!"
fi

# Sayı karşılaştırma
count=$(ls -1 *.js 2>/dev/null | wc -l)
if [ "$count" -gt 10 ]; then
    echo "10'dan fazla JS dosyası var: $count"
fi

# Dosya ve dizin kontrolleri
# -f : dosya var mı?
# -d : dizin var mı?
# -e : dosya veya dizin var mı?
# -r : okunabilir mi?
# -w : yazılabilir mi?
# -x : çalıştırılabilir mi?
# -s : dosya boş değil mi?
:::

### Döngüler (for/while)

:::code[bash]{title="for ve while Döngüleri"}
#!/bin/bash

# for döngüsü - dosyalar üzerinde
for file in *.js; do
    echo "JS dosyası: $file"
    wc -l "$file"
done

# for döngüsü - liste üzerinde
for lang in "JavaScript" "Python" "Go" "Rust"; do
    echo "Dil: $lang"
done

# for döngüsü - sayı aralığı
for i in {1..5}; do
    echo "Sunucu $i kontrol ediliyor..."
    # ping -c 1 server$i.example.com
done

# while döngüsü
counter=0
while [ $counter -lt 5 ]; do
    echo "Deneme: $counter"
    counter=$((counter + 1))
done

# Dosya satır satır okuma
while IFS= read -r line; do
    echo "Satır: $line"
done < input.txt

# Sonsuz döngü (servis izleme)
# while true; do
#     curl -s https://api.example.com/health || echo "UYARI: API çöktü!"
#     sleep 30
# done
:::

### Fonksiyonlar

:::code[bash]{title="Bash Fonksiyonları"}
#!/bin/bash

# Basit fonksiyon
greet() {
    echo "Merhaba, $1!"
}
greet "Dünya"

# Parametreli fonksiyon
create_component() {
    local component_name=$1
    local dir="src/components/${component_name}"

    mkdir -p "$dir"
    cat > "$dir/${component_name}.jsx" << EOF
import React from 'react';
import './${component_name}.css';

const ${component_name} = () => {
  return (
    <div className="${component_name}">
      <h1>${component_name}</h1>
    </div>
  );
};

export default ${component_name};
EOF

    cat > "$dir/${component_name}.css" << EOF
.${component_name} {
  /* styles */
}
EOF

    echo "Component oluşturuldu: $dir"
}

# Kullanım
create_component "Header"
create_component "Footer"

# Return değeri olan fonksiyon
is_git_repo() {
    if [ -d ".git" ]; then
        return 0  # true (bash'te 0 = başarılı)
    else
        return 1  # false
    fi
}

if is_git_repo; then
    echo "Git repository'sindesin"
fi
:::

### Pratik Script Örneği: Proje Kurulum Script'i

:::code[bash]{title="setup.sh - Proje Kurulum Script'i"}
#!/bin/bash

# Renkli çıktı
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Node.js kontrolü
if ! command -v node &> /dev/null; then
    log_error "Node.js bulunamadı! Lütfen yükleyin: https://nodejs.org"
    exit 1
fi

log_info "Node.js versiyonu: $(node --version)"

# Bağımlılıkları yükle
if [ -f "package.json" ]; then
    log_info "Bağımlılıklar yükleniyor..."
    pnpm install
else
    log_error "package.json bulunamadı!"
    exit 1
fi

# .env dosyası oluştur
if [ ! -f ".env" ]; then
    log_warn ".env dosyası bulunamadı, örnek oluşturuluyor..."
    cp .env.example .env 2>/dev/null || echo "PORT=3000" > .env
    log_info ".env dosyası oluşturuldu. Lütfen düzenleyin."
fi

log_info "Kurulum tamamlandı!"
:::

## tmux - Terminal Multiplexer

:::concept[tmux (İng: Terminal Multiplexer)]
tmux, tek bir terminal penceresinde birden fazla terminal oturumu oluşturup yönetmeni sağlar. SSH bağlantısı kopsa bile oturum devam eder.

**Türkçe karşılığı:** Terminal Çoklayıcı
**Ne işe yarar:** Birden fazla terminal oturumunu tek pencerede yönetir, oturumları kalıcı kılar
**Gerçek hayat benzetmesi:** Bir masaüstünde birden fazla monitör kullanmak gibi - her ekranda farklı iş yapabilirsin
:::

:::code[bash]{title="tmux Temel Komutları"}
# Oturum yönetimi
tmux                              # Yeni oturum başlat
tmux new -s myproject             # İsimli oturum başlat
tmux ls                           # Oturumları listele
tmux attach -t myproject          # Oturuma bağlan
tmux kill-session -t myproject    # Oturumu kapat

# tmux içindeki kısayollar (Prefix = Ctrl+b)
# Ctrl+b, d          → Oturumdan ayrıl (detach) - oturum devam eder!
# Ctrl+b, c          → Yeni pencere oluştur
# Ctrl+b, n          → Sonraki pencereye geç
# Ctrl+b, p          → Önceki pencereye geç
# Ctrl+b, %          → Dikey bölme (split vertical)
# Ctrl+b, "          → Yatay bölme (split horizontal)
# Ctrl+b, o          → Bölmeler arası geçiş
# Ctrl+b, x          → Mevcut bölmeyi kapat
# Ctrl+b, z          → Bölmeyi tam ekran yap/geri al (zoom)
# Ctrl+b, [          → Scroll moduna geç (q ile çık)
:::

:::tip
tmux, SSH ile uzak sunucuda çalışırken hayat kurtarır. İnternet bağlantın kopsa bile tmux oturumun sunucuda çalışmaya devam eder. `tmux attach` ile geri bağlanabilirsin. Uzun süren işlemler (build, deployment) için vazgeçilmez.
:::

## Faydalı Komut Kombinasyonları

:::code[bash]{title="Günlük Geliştirici Komut Setleri"}
# Disk kullanımı analizi
du -sh */                                # Her dizinin boyutu
df -h                                    # Disk alanı özeti
ncdu .                                   # İnteraktif disk kullanımı (yüklemen gerekir)

# Process yönetimi
ps aux                                   # Tüm process'leri listele
ps aux | grep node                       # Node process'lerini bul
kill -9 <PID>                            # Process'i zorla kapat
lsof -i :3000                            # 3000 portunu kullanan process'i bul
killall node                             # Tüm node process'lerini kapat

# Ağ komutları
curl -I https://example.com              # HTTP header'larını gör
curl -s https://api.example.com | jq '.' # API yanıtını güzel formatla
wget https://example.com/file.zip        # Dosya indir
netstat -tlnp                            # Açık portları listele
ss -tlnp                                 # netstat'ın modern alternatifi

# Metin işleme
awk '{print $1, $3}' file.txt            # 1. ve 3. sütunları yazdır
sed 's/old/new/g' file.txt               # Metin değiştir
cut -d',' -f1,3 data.csv                 # CSV'den sütun seç
tr '[:lower:]' '[:upper:]' < file.txt    # Küçük harfleri büyüğe çevir
sort file.txt | uniq -c | sort -rn       # Frekans analizi

# Arşiv işlemleri
tar -czf backup.tar.gz project/          # Sıkıştır
tar -xzf backup.tar.gz                   # Aç
zip -r archive.zip project/              # ZIP oluştur
unzip archive.zip                        # ZIP aç
:::

## Alias ve .bashrc Konfigürasyonu

:::code[bash]{title="~/.bashrc veya ~/.zshrc Alias'ları"}
# Git alias'ları
alias gs="git status"
alias ga="git add"
alias gc="git commit"
alias gp="git push"
alias gl="git log --oneline --graph --all"
alias gd="git diff"
alias gb="git branch"

# Navigasyon alias'ları
alias ..="cd .."
alias ...="cd ../.."
alias ll="ls -lah"
alias la="ls -la"

# Proje alias'ları (📌 2026: pnpm kullanıyorsan run gerekmez)
alias dev="pnpm dev"
alias build="pnpm build"
alias test="pnpm test"

# Güvenlik alias'ları
alias rm="rm -i"                # Silmeden önce her zaman sor
alias cp="cp -i"                # Üzerine yazmadan önce sor
alias mv="mv -i"                # Üzerine yazmadan önce sor

# Fonksiyon alias'ları
mkcd() { mkdir -p "$1" && cd "$1"; }     # Dizin oluştur ve gir
extract() {                                # Her türlü arşivi aç
    case "$1" in
        *.tar.gz)  tar xzf "$1" ;;
        *.tar.bz2) tar xjf "$1" ;;
        *.zip)     unzip "$1" ;;
        *.gz)      gunzip "$1" ;;
        *)         echo "Bilinmeyen format: $1" ;;
    esac
}
:::

:::exercise
### Alistirma 1: Dosya ve Klasor Yonetimi (Kolay)

Terminal komutlariyla bir proje yapisi olustur, dosyalari yonet ve iceriklerini incele.

```bash
# 1. Proje yapisi olustur (tek komutla)
mkdir -p ~/terminal-practice/{src,tests,docs,config}

# 2. Dosyalar olustur
touch ~/terminal-practice/src/{index.js,app.js,utils.js}
touch ~/terminal-practice/tests/{index.test.js,app.test.js}
touch ~/terminal-practice/config/{.env,.env.example}
echo "# Terminal Practice" > ~/terminal-practice/README.md

# 3. Yapiyi goruntule
ls -laR ~/terminal-practice/

# GOREV: Asagidaki komutlari calistir ve ciktilari yorumla:
find ~/terminal-practice -name "*.js" | wc -l       # Kac JS dosyasi var?
find ~/terminal-practice -name "*.js" -path "*/tests/*"  # Sadece test dosyalari
find ~/terminal-practice -type f -empty              # Bos dosyalar
du -sh ~/terminal-practice/                          # Toplam boyut

# 4. Dosya icerigi yazma ve okuma
echo "console.log('Hello World');" > ~/terminal-practice/src/index.js
echo "module.exports = { add: (a, b) => a + b };" > ~/terminal-practice/src/utils.js
cat ~/terminal-practice/src/index.js

# 5. Dosyalarda arama
grep -rn "console" ~/terminal-practice/src/
grep -rn "module" ~/terminal-practice/src/
```

**Beklenen Sonuc:** 5 JS dosyasi bulunmali (3 src + 2 test). `find` ile farkli filtreleme yapilabilmeli. `grep -rn` satir numaralariyla eslesen satirlari gostermeli.
**Ipucu:** `mkdir -p` ic ice klasorleri olusturur, `{}` ile birden fazla klasor tek satirda yapilir.

---

### Alistirma 2: Bash Script Yazma (Orta)

Bir proje setup script'i yaz: ortam kontrolu, bagimliliklari yukleme ve proje baslatma islemlerini otomatiklestir.

```bash
# setup.sh dosyasini olustur:
cat > ~/terminal-practice/setup.sh << 'SCRIPT'
#!/bin/bash

echo "=== Proje Kurulum Script'i ==="
echo ""

# 1. Node.js kontrolu
if command -v node &> /dev/null; then
    echo "Node.js bulundu: $(node --version)"
else
    echo "HATA: Node.js kurulu degil!"
    echo "Kurmak icin: https://nodejs.org"
    exit 1
fi

# 2. Git kontrolu
if command -v git &> /dev/null; then
    echo "Git bulundu: $(git --version)"
else
    echo "UYARI: Git kurulu degil"
fi

# TODO: 3. Python kontrolu ekle
# TODO: 4. .env dosyasi yoksa .env.example'dan kopyala
# TODO: 5. node_modules klasoru yoksa npm install calistir
# TODO: 6. Kurulum ozeti yazdir (hangi araclar bulundu, hangileri eksik)

echo ""
echo "=== Kurulum tamamlandi ==="
SCRIPT

# Calistirma izni ver ve calistir
chmod +x ~/terminal-practice/setup.sh
~/terminal-practice/setup.sh
```

**Beklenen Sonuc:** Script kurulu araclari tespit edip versiyonlarini gostermeli. Eksik araclari uyarmali. .env dosyasi yoksa .env.example'dan olusturmali.
**Ipucu:** `command -v program` komutu program'in kurulu olup olmadigini kontrol eder. `$?` son komutun cikis kodunu verir (0=basarili).

---

### Alistirma 3: Pipe, Redirection ve Text Processing (Zor)

Pipe (`|`) ve redirection (`>`, `>>`, `<`) kullanarak karmasik veri isleme zincirleri olustur.

```bash
# 1. Ornek log dosyasi olustur
cat > ~/terminal-practice/app.log << 'EOF'
2026-03-21 10:00:01 INFO Server started on port 3000
2026-03-21 10:00:05 INFO User login: ahmet@test.com
2026-03-21 10:00:12 ERROR Database connection failed
2026-03-21 10:00:15 INFO Retrying database connection...
2026-03-21 10:00:18 INFO Database connected
2026-03-21 10:01:30 WARN High memory usage: 85%
2026-03-21 10:02:00 INFO User login: ayse@test.com
2026-03-21 10:02:45 ERROR API timeout: /api/products
2026-03-21 10:03:00 INFO User logout: ahmet@test.com
2026-03-21 10:04:12 ERROR Disk space low: 95%
2026-03-21 10:05:00 INFO Scheduled backup started
EOF

# GOREV 1: Sadece ERROR satirlarini bul ve errors.log'a kaydet
grep "ERROR" ~/terminal-practice/app.log > ~/terminal-practice/errors.log
cat ~/terminal-practice/errors.log
# Kac hata var?
wc -l ~/terminal-practice/errors.log

# GOREV 2: Her log seviyesinin kac kez gectigini say
cat ~/terminal-practice/app.log | awk '{print $3}' | sort | uniq -c | sort -rn
# Beklenen: INFO en fazla, ERROR ikinci, WARN en az

# GOREV 3: Login olan kullanicilari listele (tekrarsiz)
grep "User login" ~/terminal-practice/app.log | awk '{print $NF}' | sort -u
# Beklenen: ahmet@test.com ve ayse@test.com

# GOREV 4: Saat bazinda log sayisi
cat ~/terminal-practice/app.log | awk '{print substr($2,1,5)}' | sort | uniq -c

# GOREV 5: Son 3 satiri goster, ilk 3 satiri goster
tail -3 ~/terminal-practice/app.log
head -3 ~/terminal-practice/app.log

# BONUS: Gercel zamanli log izleme simulasyonu
# tail -f ~/terminal-practice/app.log
# (Baska terminal'de dosyaya yeni satirlar eklendikce gorunur)
```

**Beklenen Sonuc:** 3 ERROR satiri errors.log'a kaydedilmeli. Log seviyesi dagilimi: INFO=7, ERROR=3, WARN=1. 2 benzersiz kullanici login olmali. Pipe zinciri ile karmasik islemler tek satirda yapilabilmeli.
**Ipucu:** `awk '{print $3}'` her satirin 3. alanini alir (boslukla ayrilmis). `sort | uniq -c` tekrarlayan satirlari sayar.
:::

:::knowledge-check
type: multiple_choice
question: "chmod 755 script.sh komutu ne yapar?"
options:
  - "Dosyayı siler ve 755 boyutunda yeniden oluşturur"
  - "Owner'a rwx (okuma+yazma+çalıştırma), group ve others'a rx (okuma+çalıştırma) izni verir"
  - "Dosyanın boyutunu 755 KB'ye sınırlar"
  - "Dosyayı 755 kez kopyalar"
correct: 1
explanation: "chmod'da sayılar: r=4, w=2, x=1. 7=4+2+1=rwx (owner), 5=4+1=rx (group), 5=4+1=rx (others). Yani owner tam yetki, diğerleri okuyup çalıştırabilir."
:::

:::knowledge-check
type: multiple_choice
question: "cat error.log | grep 'FATAL' | wc -l komutu ne yapar?"
options:
  - "error.log dosyasını siler"
  - "error.log'daki FATAL satırlarını yeni bir dosyaya yazar"
  - "error.log'da 'FATAL' içeren satırların sayısını verir"
  - "FATAL kelimesini error.log'a yazar"
correct: 2
explanation: "Pipe zinciri: cat dosyayı okur → grep 'FATAL' sadece FATAL içeren satırları filtreler → wc -l filtrelenmiş satırların sayısını verir. Bu, log analizi için çok yaygın bir pattern'dır."
:::

:::ai-guidance
title: Bu Derste AI ile Öğren
content: Terminal komutlarini ve shell scripting'i AI ile pratik yaparak ogren. Karmasik komut zincirlerini aciklat ve kendi otomasyon scriptlerini yazdir.
model_recommendation: Claude Sonnet 4.5
prompts:
  - prompt: "Su pipe zincirinin her adimini acikla: find . -name '*.js' -not -path '*/node_modules/*' | xargs wc -l | sort -rn | head -20. Her komutun ne yaptigini, veri akisini ve ciktiyi adim adim goster."
    why: "Pipe zincirlerini okuyup yazmak terminal ustaliginin temelidir. Her komutu ayri ayri anlamak, karmasik zincirleri kendin kurmani saglar."
    follow_up: "Bir proje icin otomasyon scripti yaz: Node.js kurulu mu kontrol et, bagimliliklaEri yukle, .env dosyasi yoksa ornekten kopyala, dev server'i baslat. Renkli cikti ve hata yonetimi ekle."
  - prompt: "chmod 755, 644 ve 600 izinlerinin farkini acikla. Hangi dosya turunde hangi izni kullanmaliyim? Bir web sunucusunda dosya izinlerinin yanlis ayarlanmasi hangi guvenlik risklerine yol acar?"
    why: "Dosya izinleri server yonetiminde kritik oneme sahiptir. Yanlis izinler guvenlik aciklarinin en yaygin nedenlerinden biridir."
pair_programming_tip: "Terminal'de karmasik bir islem yapmak istediginde AI'a amacini anlat: 'Projede tum console.log satirlarini bul, hangi dosyada kac tane oldugunu goster ve en cok olandan en aza sirala.' AI sana dogru komut zincirini olusturur."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Linux dosya izinleri nasil calisir? chmod 755 ne anlama gelir?**
- **Junior cevabi:** chmod dosya izinlerini degistirir, 755 okuma-yazma-calistirma iznidir.
- **Senior cevabi:** Unix izinleri 3 grup (owner/group/others) ve 3 izin (read=4, write=2, execute=1) icerir. 755 = owner rwx (7), group rx (5), others rx (5). Yani sahibi her seyi yapabilir, digerler okuyabilir ve calistirabilir. Script dosyalari icin 755 (calistiriabilir), config dosyalari icin 644 (sadece owner yazar), secret dosyalar icin 600 (sadece owner erisir). Web server'da yanlis izinler security breach'e yol acar. `chmod -R` recursive, setuid/setgid ise privilege escalation riski tasidigidan dikkatle kullanilmalidir.

**Soru 2: Pipe (|) ve redirection (>, >>) arasindaki fark nedir?**
- **Junior cevabi:** Pipe bir komutun ciktisini digerine gonderir, > dosyaya yazar.
- **Senior cevabi:** Pipe (|) stdout'u bir sonraki komutun stdin'ine baglar, Unix felsefesinin temelidir: kucuk programlar birlestirilerek karmasik islemler yapilir. `>` stdout'u dosyaya yazar (uzerine), `>>` ekler. `2>` stderr'i yonlendirir, `2>&1` stderr'i stdout'a birlesitirir. `tee` komutu hem ekrana hem dosyaya yazar. Ornek: `find / -name "*.log" 2>/dev/null | xargs grep "error" | sort | uniq -c | sort -rn | head -10` en cok tekrar eden 10 hatayi bulur.
:::

:::must-note
- `ls -la` → gizli dosyalar dahil detaylı listeleme, dosya izinlerini okumayı öğren
- `cd -` → önceki dizine geri dön, `cd ~` → home dizini
- `mkdir -p` → iç içe dizinleri tek komutla oluştur
- `rm -rf` → dikkatli kullan! Geri dönüşü yok. Önce `ls` ile kontrol et
- `grep -rn "pattern" dir/` → recursive arama + satır numarası (her gün kullanacaksın)
- `find . -name "*.ext"` → dosya arama, `-exec` ile komut zinciri
- `chmod 755` → script çalıştırma izni, `chmod 600` → sadece owner okusun (SSH key)
- Pipe `|` → komutları zincirleme bağla: `cmd1 | cmd2 | cmd3`
- `>` üzerine yazar, `>>` sonuna ekler, `2>&1` stderr'i stdout'a yönlendir
- `$()` → komut çıktısını değişkene ata: `result=$(command)`
- Bash'te `=` etrafında boşluk olmamalı: `name="value"` (boşluk koyarsan hata alırsın)
- `if [ -f "file" ]` → dosya var mı kontrol et, `-d` dizin, `-e` herhangi biri
- tmux: `Ctrl+b, d` → detach (oturum devam eder), `tmux attach` → geri bağlan
- Alias'ları `~/.bashrc` veya `~/.zshrc` dosyasına yaz, `source ~/.bashrc` ile aktifleştir
- `tail -f logfile` → canlı log takibi (production debug için kritik)
:::

:::senior-learns
Bir Senior Developer terminal kullanırken şu yaklaşımı benimser:

1. **Shell'ini customize eder** - Oh My Zsh veya Starship prompt kullanır. Custom alias'lar ve fonksiyonlar yazar. `.bashrc`/`.zshrc` dosyasını version control'e alır (dotfiles repo). Her yeni makinede 5 dakikada aynı ortamı kurar.
2. **Her şeyi script'ler** - Tekrarlayan bir işi 3. kez manuel yapıyorsa, script yazar. CI/CD pipeline'ları, deployment script'leri, database migration'ları hep bash/shell script ile başlar.
3. **Pipe master'ıdır** - `awk`, `sed`, `jq`, `xargs` gibi araçları zincirleme kullanarak karmaşık veri dönüşümlerini tek satırda yapar. Log analizi, data processing, bulk file operations hep pipe ile yapılır.
4. **tmux veya screen kullanır** - SSH oturumlarında tmux ile birden fazla pencere yönetir. Uzun süren işlemleri tmux'ta başlatır ve bağlantı kopsa bile devam eder. tmux config dosyasını customize eder.
5. **Man page okumayı bilir** - `man grep`, `man find` komutlarıyla her aracın tüm seçeneklerini keşfeder. Stack Overflow'a gitmeden önce man page'e bakar. `tldr` aracını kullanarak kısa özetlere hızlıca erişir.
6. **Shell history'yi etkin kullanır** - `Ctrl+R` ile reverse search yapar. `history | grep` ile geçmiş komutları bulur. `.bash_history` boyutunu artırır. `HISTIGNORE` ile gereksiz komutları filtreler.

**Profesyonel Mindset:** "Terminal, geliştiricinin en güçlü silahıdır. GUI araçları seni sınırlar, terminal seni özgürleştirir. Bir komutu bilmemek sorun değil, ama terminal'den korkmak bir profesyonel için kabul edilemez. Her gün en az bir yeni komut veya flag öğren. 6 ay sonra terminal'de su gibi akacaksın."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **CLI** (siː-el-aɪ) → Command Line Interface / Komut Satırı Arayüzü
   *"Every developer should be comfortable using the CLI for daily tasks."*

2. **Shell** (ʃel) → Kabuk (komut yorumlayıcı)
   *"Bash is the most common shell on Linux systems."*

3. **Pipe** (paɪp) → Boru (komut zincirleme operatörü)
   *"Use pipes to chain commands together for powerful data processing."*

4. **Redirect** (riː-daɪ-rekt) → Yönlendirme
   *"Redirect the output to a file using the > operator."*

5. **Permission** (pər-mɪ-ʃən) → İzin / Yetki
   *"Set file permissions to 600 for SSH private keys."*

**Okuma Egzersizi:** Linux man page'lerini İngilizce okumaya alış: `man ls`, `man grep`, `man find`

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Shell script temelleri dersini tamamladım"
→ Örnek: `docs: complete shell scripting fundamentals lesson`
:::

:::external-resource
- 📺 **freeCodeCamp:** "Linux Command Line for Beginners" (3 saat, YouTube, ücretsiz)
- 📖 **Linux Journey:** linuxjourney.com (interaktif, ücretsiz)
- 🎮 **OverTheWire Bandit:** overthewire.org/wargames/bandit (terminal wargame)
- 📖 **The Linux Command Line:** William Shotts (ücretsiz e-book, linuxcommand.org)
- 📺 **tmux Crash Course:** "Learn tmux in 15 Minutes" (YouTube, ücretsiz)
:::
