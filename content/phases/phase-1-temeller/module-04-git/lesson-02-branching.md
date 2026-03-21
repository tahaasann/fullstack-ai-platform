---
id: "mod-04-git/lesson-02"
title: "Branching, Merging ve Profesyonel Git Stratejileri"
estimated_minutes: 50
order: 2
tags: ["git", "branching", "merge", "rebase", "cherry-pick", "git-flow", "conflict-resolution"]
prerequisites: ["mod-04-git/lesson-01"]
---

# Branching, Merging ve Profesyonel Git Stratejileri

:::realworld
Profesyonel yazılım gelistirmede hicbir ciddi ekip tek bir branch üzerinde çalışmaz. Branch'ler, Git'in en güçlü ozelligidir ve doğru kullanildiginda ekip uyelerinin birbirini engellemeden paralel çalışmasını sağlar. Bu derste branch olusturmaktan merge conflict cozmeye, rebase stratejilerinden Git Flow'a kadar her seyi ogreneceksin. Bir is mulakatinda "Git workflow'unuz nasil?" sorusuna profesyonelce cevap verebilecek seviyeye geleceksin.
:::

## Branch Nedir, Neden Kullanılır?

:::concept[Branch (Ing: Branch)]
Branch, mevcut kodun bağımsız bir kopyasi üzerinde calismanizi sağlayan isaretcidir (pointer). Aslinda dosyalari kopyalamaz, sadece commit gecmisinde yeni bir yol oluşturur.

**Turkce karsiligi:** Dal / Dallanma
**Ne ise yarar:** Ana kodu bozmadan yeni özellik geliştirme, hata duzeltme veya deney yapma imkani verir
**Gerçek hayat benzetmesi:** Bir kitabin fotokopisini alip üzerinde değişiklik yapmak gibi. Begenmezsen fotokopisi atarsin, begenirsen orijinaline işlenir.
:::

Branch'lerin temel kullanım alanlari:

- **Feature development:** Yeni özellik geliştirmek için ayrı branch
- **Bug fix:** Hata duzeltmesi için izole çalışma alani
- **Experiment:** Deney yapmak için riskli değişiklikleri ana koddan ayirma
- **Release management:** Sürüm hazirligi için stabilizasyon branch'i

:::deha-tip
Deha seviyesi geliştiriciler branch'leri ucuz ve hızlı oldugunu bilir. Git'te branch oluşturmak sadece 41 byte'lik bir dosya yazmak demektir (bir commit hash'i). Bu yuzden her küçük is için bile branch acmaktan cekinmezler. "Branch acmak ucuz, hata duzeltmek pahali" prensibiyle hareket ederler.
:::

## Branch Oluşturma, Değiştirme ve Silme

### Temel Branch Komutlari

:::code[bash]{title="Branch Işlemleri"}
# Mevcut branch'leri listele
git branch                    # Yerel branch'ler
git branch -r                 # Remote branch'ler
git branch -a                 # Tüm branch'ler

# Yeni branch oluştur (geçiş yapmadan)
git branch feature/login

# Yeni branch oluştur ve geçiş yap (eski yöntem)
git checkout -b feature/login

# Yeni branch oluştur ve geçiş yap (modern yöntem - Git 2.23+)
git switch -c feature/login

# Branch'ler arası geçiş
git checkout main             # Eski yöntem
git switch main               # Modern yöntem

# Branch silme
git branch -d feature/login   # Merge edilmis branch'i sil
git branch -D feature/login   # Merge edilmemis olsa bile zorla sil

# Remote branch silme
git push origin --delete feature/login

# Branch'i yeniden adlandir
git branch -m eski-isim yeni-isim
:::

:::beginner-mistake
Yaygin hata: `git checkout` komutunu hem branch değiştirmek hem dosya geri yüklemek için kullanmak. Git 2.23'ten itibaren `git switch` (branch değiştirme) ve `git restore` (dosya geri yükleme) olarak ayrildi. Modern komutlari kullan, daha güvenli ve anlasilir.
:::

### Branch Adlandirma Konvansiyonlari

:::code[text]{title="Profesyonel Branch Isimlendirme"}
feature/kullanıcı-girişi       # Yeni özellik
bugfix/login-hatasi            # Hata duzeltme
hotfix/güvenlik-acigi          # Acil üretim hatasi
release/v2.1.0                 # Sürüm hazirligi
chore/bağımlılık-güncelleme    # Bakim isleri
docs/api-dokümantasyonu        # Dokümantasyon
refactor/auth-modulu           # Yeniden yapılandırma

# Ticket numarasi ile
feature/JIRA-1234-login-sayfasi
bugfix/GH-567-null-pointer
:::

:::tip
Branch isimlerinde Turkce karakter (i, s, c, g, u, o) kullanma. Küçük harf, tire (-) veya slash (/) ayirici kullan. Kısa ve aciklayici isimler seç.
:::

## Merge: Branch'leri Birleştirme

### Fast-Forward Merge

:::concept[Fast-Forward Merge (Ing: Fast-Forward Merge)]
Hedef branch'te, kaynak branch'ten ayrildigindan beri hicbir yeni commit yoksa, Git sadece isaretciyi (pointer) ileri tasir. Yeni bir merge commit oluşturmaz.

**Turkce karsiligi:** Hızlı Ileri Sarma
**Ne ise yarar:** Temiz, duz bir commit geçmişi oluşturur
**Gerçek hayat benzetmesi:** Bir kitabin sonuna yeni sayfalar eklemek gibi - arada değişen bir sey yoksa sadece ekleme yapılır
:::

:::code[bash]{title="Fast-Forward Merge Örneği"}
# Senaryo: main'den ayrildin, 3 commit attin, main'de değişiklik yok
git switch main
git merge feature/login
# Sonuç: Fast-forward (merge commit yok, temiz geçmiş)

# Grafik görünüm:
# Önce:
# main:    A---B
#                \
# feature:        C---D---E
#
# Sonra (fast-forward):
# main:    A---B---C---D---E
:::

### 3-Way Merge

:::concept[3-Way Merge (Ing: Three-Way Merge)]
Her iki branch'te de ayrilma noktasindan sonra yeni commit'ler varsa, Git üç noktayi kullanır: ortak ata (common ancestor), her iki branch'in son hali. Sonucta yeni bir merge commit oluşturur.

**Turkce karsiligi:** Üç Yonlu Birleştirme
**Ne ise yarar:** Paralel calismalarim birlestirilmesini sağlar
**Gerçek hayat benzetmesi:** Iki kisinin ayni dokumani ayrı ayrı duzenleyip sonra değişiklikleri birde birlestirmesi gibi
:::

:::code[bash]{title="3-Way Merge Örneği"}
# Senaryo: Sen feature branch'te çalışırken main'e de commit'ler gelmis
git switch main
git merge feature/login
# Sonuç: Merge commit oluşturulur

# Grafik görünüm:
# Önce:
# main:    A---B---F---G
#                \
# feature:        C---D---E
#
# Sonra (3-way merge):
# main:    A---B---F---G---M  (M = merge commit)
#                \         /
# feature:        C---D---E

# Fast-forward'u engelleyip her zaman merge commit oluştur
git merge --no-ff feature/login
:::

:::comparison
| Özellik | Fast-Forward Merge | 3-Way Merge |
|---------|-------------------|-------------|
| Merge commit | Oluşturmaz | Oluşturur |
| Geçmiş | Duz (linear) | Dallanmali |
| Ne zaman olur | Hedef branch'te değişiklik yoksa | Her iki branch'te değişiklik varsa |
| `--no-ff` | Zorla merge commit oluşturur | Zaten merge commit oluşturur |
| **Avantaj** | Temiz geçmiş | Branch geçmişi korunur |
| **Dezavantaj** | Branch'in varligi kaybolur | Geçmiş karmaşık gorunebilir |

**Tavsiye:** Ekip calismalarinda `--no-ff` kullanarak feature branch'lerin gecmiste görünür kalmasini sagla. Kisisel branch'lerde fast-forward tercih edebilirsin.
:::

### Merge Conflict Çözme

Iki branch ayni dosyanin ayni satirlarini degistirmisse, Git otomatik birlestiremez ve conflict (çatışma) oluşur.

:::code[text]{title="Conflict Isaretleri"}
<<<<<<< HEAD
// main branch'teki kod
const API_URL = "https://api.production.com";
=======
// feature branch'teki kod
const API_URL = "https://api.staging.com";
>>>>>>> feature/login
:::

:::code[bash]{title="Conflict Çözme Adimlari"}
# 1. Merge'i başlat
git merge feature/login
# CONFLICT (content): Merge conflict in src/config.js

# 2. Conflict olan dosyalari gor
git status

# 3. Dosyayi ac, conflict isaretlerini kaldir, doğru kodu seç
# <<<<<<< HEAD, =======, >>>>>>> isaretlerini sil

# 4. Cozulmus dosyayi stage'le
git add src/config.js

# 5. Merge'i tamamla
git commit
# (Git otomatik merge commit mesaji oluşturur)

# Merge'i iptal etmek istersen
git merge --abort
:::

:::beginner-mistake
Yaygin hata: Conflict isaretlerini (<<<, ===, >>>) dosyada birakarak commit etmek. Conflict cozulurken bu isaretlerin tamamen kaldirildigini kontrol et. Iyi bir IDE bu isaretleri renklendirerek gösterir ve seçim yapmani kolaylastirir.
:::

## Rebase: Commit Geçmişini Yeniden Yazmak

:::concept[Rebase (Ing: Rebase)]
Rebase, bir branch'in commit'lerini başka bir branch'in ucuna tasir. Commit'lerin base'ini (temelini) değiştirir, bu yuzden "re-base" adi verilmistir.

**Turkce karsiligi:** Yeniden Temellendirme
**Ne ise yarar:** Duz (linear) ve temiz bir commit geçmişi oluşturur
**Gerçek hayat benzetmesi:** Bir kitabin 5. bolumunu yazmissin ama yazarin 4. bolume ekleme yaptığını farkettin. Senin bolumu sifirdan, yeni 4. bolumun üzerine yeniden yazman gibi.
:::

:::code[bash]{title="Rebase Temel Kullanım"}
# Senaryo: feature branch'tesin, main'e yeni commit'ler gelmis
git switch feature/login
git rebase main

# Grafik görünüm:
# Önce:
# main:    A---B---F---G
#                \
# feature:        C---D---E
#
# Sonra (rebase):
# main:    A---B---F---G
#                        \
# feature:                C'--D'--E'
# (C', D', E' yeni commit hash'lerine sahip)

# Sonra main'e merge edildiginde fast-forward olur:
git switch main
git merge feature/login
# main:    A---B---F---G---C'--D'--E'  (duz geçmiş!)
:::

:::code[bash]{title="Rebase Conflict Çözme"}
# Rebase sırasında conflict cikarsa:
git rebase main
# CONFLICT in src/config.js

# 1. Conflict'i coz (dosyayi duzenle)
# 2. Stage'le
git add src/config.js

# 3. Rebase'e devam et
git rebase --continue

# 4. Rebase'i iptal etmek için
git rebase --abort
:::

### Merge vs Rebase Karşılaştırma

:::comparison
| Özellik | Merge | Rebase |
|---------|-------|--------|
| Geçmiş | Dallanmali (non-linear) | Duz (linear) |
| Commit hash | Değişmez | Değişir (yeni hash) |
| Merge commit | Oluşturur (3-way) | Oluşturmaz |
| Güvenlik | Daha güvenli (geçmişi değiştirmez) | Riskli (geçmişi yeniden yazar) |
| Paylasilmis branch | Guvenle kullanılabilir | TEHLIKELI - asla paylasilmis branch'te rebase yapma |
| Conflict çözme | Tek seferde | Her commit için ayrı ayrı |
| **Ne zaman kullan** | Public branch, ekip çalışması | Kisisel branch, temiz geçmiş istiyorsan |

**Altin Kural:** "Public branch'lere push edilmis commit'leri asla rebase etme!" Çünkü diger ekip uyelerinin geçmişini bozarsin.

**Tavsiye:** Kendi feature branch'ini main'e merge etmeden önce `git rebase main` yaparak guncellemeni al. Sonra `git merge --no-ff` ile merge et. Bu yöntem hem temiz geçmiş hem de branch gorunurlugu sağlar.
:::

## Interactive Rebase: Commit Geçmişini Düzenleme

Interactive rebase, Git'in en güçlü araclarindan biridir. Commit'leri birleştirme, silme, mesajini değiştirme ve sıralama imkani sunar.

:::code[bash]{title="Interactive Rebase Başlatma"}
# Son 4 commit'i duzenle
git rebase -i HEAD~4

# Veya belirli bir commit'ten itibaren
git rebase -i abc123^

# Acilan editorde şu komutlari kullanabilirsin:
# pick   = commit'i oldugu gibi kullan
# reword = commit mesajini değiştir
# edit   = commit'i duzenle (dosya değişikliği yapabilirsin)
# squash = önceki commit ile birleştir (mesajlari birleştir)
# fixup  = önceki commit ile birleştir (bu commit'in mesajini at)
# drop   = commit'i tamamen sil
:::

:::code[text]{title="Interactive Rebase Örneği"}
# Editorunde şu gorunumu gorursun:
pick a1b2c3d feat: login sayfasi eklendi
pick e4f5g6h fix: login typo duzeltildi
pick i7j8k9l fix: login buton rengi
pick m0n1o2p feat: logout özelliği eklendi

# Typo ve buton duzeltmesini login commit'ine birleştirmek için:
pick a1b2c3d feat: login sayfasi eklendi
fixup e4f5g6h fix: login typo duzeltildi
fixup i7j8k9l fix: login buton rengi
pick m0n1o2p feat: logout özelliği eklendi

# Sonuç: 2 temiz commit kalir
# feat: login sayfasi eklendi (3 commit birlesik)
# feat: logout özelliği eklendi
:::

:::code[bash]{title="Her Interactive Rebase Komutu Detayli"}
# SQUASH: Commit'leri birleştir, mesajlari birleştir
# fixup ile ayni ama squash'ta her iki mesaji da duzenlersin
pick abc123 feat: user model eklendi
squash def456 feat: user validation eklendi
# -> Editorde iki mesaji birlestirmen istenir

# EDIT: Commit icerigini değiştir
pick abc123 feat: auth modulu
edit def456 feat: API endpoint'leri
# -> def456'da duraklar, değişiklik yap, git add, git rebase --continue

# REWORD: Sadece commit mesajini değiştir
reword abc123 feat: yanlis mesaj
# -> Editorde mesaji duzenlemen istenir

# DROP: Commit'i tamamen sil
pick abc123 feat: kalacak commit
drop def456 test: deneme commit'i (silinecek)
:::

:::tip
Interactive rebase'i push etmeden önce kullan. "WIP", "fixup", "typo fix" gibi commit'leri squash/fixup ile temizle. PR acmadan önce commit geçmişini düzenleme aliskanligi edin.
:::

## Cherry-Pick: Secici Commit Tasima

:::concept[Cherry-Pick (Ing: Cherry-Pick)]
Cherry-pick, başka bir branch'teki belirli bir commit'i secip mevcut branch'ine uygular. Tüm branch'i merge etmek yerine sadece ihtiyacin olan commit'i alirsin.

**Turkce karsiligi:** Secici Alma
**Ne ise yarar:** Belirli bir değişikliği izole olarak başka bir branch'e tasir
**Gerçek hayat benzetmesi:** Bir agactan sadece olgun meyveleri toplamak gibi - tüm agaci sokmuyorsun, sadece ihtiyacin olani aliyorsun
:::

:::code[bash]{title="Cherry-Pick Kullanımı"}
# Belirli bir commit'i mevcut branch'ine uygula
git cherry-pick abc1234

# Birden fazla commit cherry-pick
git cherry-pick abc1234 def5678

# Commit araligini cherry-pick (A haric, B dahil)
git cherry-pick A..B

# Commit yapmadan değişiklikleri stage'e al
git cherry-pick --no-commit abc1234

# Cherry-pick'i iptal et
git cherry-pick --abort
:::

Cherry-pick ne zaman kullanılır:

- **Hotfix:** Production'da acil hata duzeltmesi gerektiginde, feature branch'teki fix commit'ini main'e cherry-pick
- **Yanlis branch:** Commit'i yanlis branch'e attiysan, doğru branch'e cherry-pick yap
- **Secici release:** Bazi özellikleri release'e dahil etmek istiyorsan

:::beginner-mistake
Yaygin hata: Cherry-pick'i sürekli kullanmak. Cherry-pick ayni değişikliği iki branch'te ayrı commit olarak oluşturur. Eger sonra bu branch'leri merge edersen conflict çıkar. Cherry-pick'i istisnai durumlarda kullan, rutin is akisi için merge veya rebase tercih et.
:::

## Git Bisect: Binary Search ile Bug Bulma

:::concept[Git Bisect (Ing: Git Bisect)]
Git bisect, binary search algoritmasi kullanarak bir bug'in hangi commit'te ortaya ciktigini bulur. Yuzlerce commit arasinda hata tespiti için muhtesem bir aractir.

**Turkce karsiligi:** Ikili Arama ile Hata Bulma
**Ne ise yarar:** Hangi commit'in hataya neden oldugunu hizlica bulur
**Gerçek hayat benzetmesi:** 1000 sayfali bir kitapta belirli bir cumleyi bulmak için ortadan acip, cumlenin önce mi sonra mi olduguna bakarak aramak gibi
:::

:::code[bash]{title="Git Bisect Kullanımı"}
# 1. Bisect'i başlat
git bisect start

# 2. Suanki durumu (hatali) isaretle
git bisect bad

# 3. Çalışan son bilinen commit'i isaretle
git bisect good v1.0.0    # veya commit hash

# 4. Git ortadaki commit'e geçiş yapar
# Test yap ve sonucu bildir:
git bisect good    # Bu commit'te hata yok
# veya
git bisect bad     # Bu commit'te hata var

# 5. Git sonraki commit'e geçer, tekrarla
# Ta ki hatali commit bulunana kadar

# 6. Bisect'i bitir ve orijinal branch'e don
git bisect reset

# OTOMATIK bisect (bir test komutu ile):
git bisect start HEAD v1.0.0
git bisect run pnpm test
# Git otomatik olarak her commit'te testi çalıştırır
# ve hatali commit'i bulur!
:::

:::code[text]{title="Bisect Örneği: 1024 Commit Arasinda Bug Bulma"}
# 1024 commit varsa:
# Binary search: log2(1024) = 10 adim
# Sadece 10 test ile 1024 commit arasinda hatali commit bulunur!

# Karşılaştırma:
# Tek tek kontrol: Ortalama 512 test
# Binary search:   Sadece 10 test
# Verimlilik:      50x daha hızlı!
:::

:::tip
`git bisect run` komutu ile bisect'i tamamen otomatize edebilirsin. Bir test script'i yaz ve Git her commit'te otomatik calistirsin. "Bu test geciyorsa good, gecmiyorsa bad" mantigi ile hatali commit dakikalar içinde bulunur.
:::

## Branching Stratejileri

### Git Flow

:::code[text]{title="Git Flow Branch Yapısı"}
main (production)
  |
  |--- develop (geliştirme)
  |       |
  |       |--- feature/login
  |       |--- feature/dashboard
  |       |
  |       |--- release/v2.0
  |       |       |
  |       |       |--- (bug fix'ler)
  |       |       |
  |       |-------|--- (release tamamlandi)
  |       |
  |--- hotfix/critical-bug
        |
        |--- (acil duzeltme, hem main hem develop'a merge)
:::

Git Flow branch'leri:
- **main:** Production kodu, her zaman stabil
- **develop:** Geliştirme branch'i, feature'lar buraya merge edilir
- **feature/\*:** Yeni özellikler için (develop'tan dallanir)
- **release/\*:** Sürüm hazirligi (develop'tan dallanir, hem main hem develop'a merge)
- **hotfix/\*:** Acil üretim duzeltmeleri (main'den dallanir)

### GitHub Flow

:::code[text]{title="GitHub Flow (Basitlesti rilmis)"}
main (her zaman deploy edilebilir)
  |
  |--- feature/login
  |       |
  |       |--- PR ac, code review, CI kontrol
  |       |
  |-------|--- merge (main'e deploy)
  |
  |--- bugfix/header
  |       |
  |       |--- PR ac, code review, CI kontrol
  |       |
  |-------|--- merge (main'e deploy)
:::

GitHub Flow kurallari:
- **main** her zaman deploy edilebilir durumda
- Yeni is için **main'den** branch ac
- Düzenli olarak push et
- **Pull Request** ac
- Code review'dan sonra **main'e** merge et
- Hemen **deploy** et

### Trunk-Based Development

:::code[text]{title="Trunk-Based Development"}
main (trunk - herkes buraya commit eder)
  |
  |--- (kısa omurlu branch, 1-2 gun max)
  |       |
  |-------|--- merge
  |
  |--- (feature flag ile büyük özellikler gizlenir)
  |
  |--- release/v2.0 (sadece release için dallanir)
:::

Trunk-Based Development özellikleri:
- Herkes doğrudan **main'e** commit eder (veya çok kısa omurlu branch'ler)
- **Feature flag** ile tamamlanmamis özellikler gizlenir
- **Continuous Integration** zorunlu
- Branch'ler maksimum 1-2 gun yasinda

### Strateji Karşılaştırma

:::comparison
| Özellik | Git Flow | GitHub Flow | Trunk-Based |
|---------|----------|-------------|-------------|
| Karmaşıklık | Yüksek | Düşük | Orta |
| Branch sayisi | Çok (5 tür) | Az (2 tür) | Minimum |
| Release döngüsü | Planli, yavas | Sürekli | Sürekli |
| Ekip buyuklugu | Büyük ekipler | Küçük-orta | Her boyut |
| CI/CD gereksinimi | Opsiyonel | Önemli | Zorunlu |
| **En uygun** | Planli release, mobil uygulamalar | Web uygulamalar, SaaS | Yüksek performansli ekipler |
| **Kullanan şirketler** | Geleneksel yazılım sirketleri | GitHub, Basecamp | Google, Facebook, Netflix |

**Tavsiye:** Yeni baslayanlar için GitHub Flow en uygun secenektir. Basit, anlasilir ve modern web geliştirme için ideal. Git Flow'u planli release döngüsü olan projelerde kullan.
:::

## Conflict Resolution Stratejileri ve Araclari

### Conflict Onleme Stratejileri

1. **Küçük ve sik merge:** Branch'ini gunluk olarak main ile güncelle
2. **Küçük commit'ler:** Büyük değişiklikler yerine küçük, odakli commit'ler at
3. **Kod sahipligi:** Ayni dosyayi ayni anda birden fazla kisi duzenlemesin
4. **Iletişim:** Büyük refactoring oncesinde ekibi bilgilendir

### Conflict Çözme Araclari

:::code[bash]{title="Conflict Çözme Araclari"}
# VS Code ile conflict çözme (dahili destek)
# Accept Current Change | Accept Incoming Change | Accept Both | Compare

# Git mergetool kullanımı
git mergetool

# Mergetool ayarlama
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait --merge $REMOTE $LOCAL $BASE $MERGED'

# Belirli bir strateji ile merge
git merge -X ours feature/login     # Conflict'te bizim kodu seç
git merge -X theirs feature/login   # Conflict'te gelen kodu seç

# Merge sırasında belirli dosyayi bizimkiyle değiştir
git checkout --ours src/config.js
git checkout --theirs src/config.js
:::

:::code[bash]{title="Gelişmiş Conflict Çözme"}
# Rerere: Ayni conflict'i tekrar çözme (REuse REcorded REsolution)
git config --global rerere.enabled true
# Git, cozdugun conflict'leri hatirlar ve tekrar ayni conflict cikarsa
# otomatik olarak ayni çözümü uygular

# Merge'i test et (gerçekten merge etmeden)
git merge --no-commit --no-ff feature/login
# Conflict var mi kontrol et
git diff --check
# Iptal et
git merge --abort

# 3-way diff ile conflict'i anla
git diff --merge
:::

:::beginner-mistake
Yaygin hata: Conflict'te panic yapip `git merge --abort` ile vazgecmek. Conflict normal bir durumdur, korkma. VS Code'un dahili conflict çözme arayüzü ile Accept Current, Accept Incoming veya Accept Both seceneklerini kullanarak hizlica cozebilirsin.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Feature Branch ve Merge Turleri (Kolay)

Feature branch olusturup fast-forward ve no-fast-forward merge farklarini gozlemle.

```bash
# 1. Repo olustur
mkdir branch-lab && cd branch-lab && git init
echo "# Proje" > README.md && git add . && git commit -m "initial commit"
echo "Aciklama" >> README.md && git add . && git commit -m "docs: add description"
echo "Kurulum" >> README.md && git add . && git commit -m "docs: add setup"

# 2. Feature branch olustur ve commit at
git checkout -b feature/login
echo "login" > login.html && git add . && git commit -m "feat: add login"
echo "style" > login.css && git add . && git commit -m "feat: add login styles"

# 3. main'e don ve merge et
git checkout main
git merge feature/login
git log --oneline --graph  # Fast-forward merge — duz cizgi

# 4. --no-ff ile merge dene
git checkout -b feature/signup
echo "signup" > signup.html && git add . && git commit -m "feat: add signup"
git checkout main
git merge --no-ff feature/signup -m "merge: add signup feature"
git log --oneline --graph  # Merge commit ile dallanma gorunur
```

**Beklenen Sonuc:** Fast-forward'da duz cizgi, --no-ff'de merge commit ve dallanma gorunmeli. `git log --oneline --graph` ile farki net gorebilmelisin.
**Ipucu:** Fast-forward, main'de yeni commit yoksa otomatik olur. Gercek projelerde --no-ff tercih edilir (branch gecmisini korur).

---

### Alistirma 2: Merge Conflict Cozme Pratigi (Orta)

Kasitli bir merge conflict olustur ve VS Code ile coz.

```bash
# 1. Repo ve baslangic dosyasi
mkdir conflict-lab && cd conflict-lab && git init
cat > app.js << 'EOF'
function greet(name) {
  return "Hello, " + name;
}
module.exports = { greet };
EOF
git add . && git commit -m "initial: add greet function"

# 2. feature/turkish branch'i — Turkce yap
git checkout -b feature/turkish
sed -i 's/Hello/Merhaba/' app.js
git add . && git commit -m "feat: turkish greeting"

# 3. main'de farkli degisiklik — emoji ekle
git checkout main
sed -i 's/"Hello, " + name/"Hello, " + name + " 👋"/' app.js
git add . && git commit -m "feat: add emoji"

# 4. Merge et — CONFLICT!
git merge feature/turkish

# TODO:
# a) git status ile conflict'li dosyayi gor
# b) Dosyayi ac, <<<<<<< ve >>>>>>> isaretlerini bul
# c) Iki degisikligi birlestir: "Merhaba, " + name + " 👋"
# d) git add app.js && git commit
# e) git log --oneline --graph ile merge commit'i dogrula
```

**Beklenen Sonuc:** Conflict basariyla cozulmeli. Son fonksiyon hem Turkce hem emoji icermeli. Conflict marker'lari dosyada kalmamali.
**Ipucu:** VS Code "Accept Both Changes" secenegi sunar. Manuel cozmek icin `<<<<<<<`, `=======`, `>>>>>>>` isaretlerini sil ve son halini yaz.

---

### Alistirma 3: Git Bisect ile Bug Hunting (Zor)

10 commit'lik bir gecmiste gizli bir hata bul. Hem manuel hem otomatik bisect kullan.

```bash
# 1. Repo olustur ve 10 commit at (5. commit'te hata ekle)
mkdir bisect-lab && cd bisect-lab && git init
for i in $(seq 1 10); do
  if [ $i -eq 5 ]; then
    echo "function add(a, b) { return a - b; }" > math.js  # BUG: + yerine -
  else
    echo "function add(a, b) { return a + b; }" > math.js
  fi
  echo "// v$i" >> math.js
  git add . && git commit -m "commit $i"
done

# 2. Manuel bisect
git bisect start
git bisect bad HEAD       # Son commit hatali
git bisect good HEAD~9    # Ilk commit dogru
# Her adimda test et:
# node -e "require('./math.js'); console.log(add(2,3))"
# Sonuc 5 ise: git bisect good
# Sonuc 5 degilse: git bisect bad
# Kac adimda bulundu? (log2(10) = ~3-4 adim bekleniyor)

# 3. Otomatik bisect
git bisect reset
git bisect start HEAD HEAD~9
git bisect run sh -c 'node -e "const r=require(\"./math.js\"); process.exit(0)"'

# 4. Sonucu dogrula
git bisect reset
```

**Beklenen Sonuc:** Bisect 3-4 adimda commit #5'i hatali olarak tanimlamali. Otomatik mod tek komutla ayni sonuca ulasmali.
**Ipucu:** `git bisect run` 0 dondurulurse "good", baska deger dondurulurse "bad" olarak isaretler.
:::

:::knowledge-check
type: multiple_choice
question: "Main branch'e push edilmis commit'leri neden rebase etmemelisin?"
options:
  - "Rebase yavas çalıştığı için"
  - "Rebase sadece küçük branch'lerde çalışır"
  - "Rebase commit hash'lerini değiştirir, diger ekip uyelerinin geçmişini bozar"
  - "Rebase merge conflict oluşturur"
correct: 2
explanation: "Rebase commit'lerin hash'lerini değiştirir (yeni commit'ler oluşturur). Eger bu commit'ler zaten push edilmisse, diger ekip uyeleri farklı bir geçmiş gorur ve büyük karışıklık çıkar. Bu yuzden sadece henuz push edilmemis, kisisel branch'lerde rebase kullan."
:::

:::knowledge-check
type: multiple_choice
question: "1024 commit arasinda hatali commit'i bulmak için git bisect en fazla kac adim gerektirir?"
options:
  - "1024 adim"
  - "512 adim"
  - "10 adim"
  - "32 adim"
correct: 2
explanation: "Git bisect binary search kullanır. log2(1024) = 10 adim. Her adimda arama alanini yarisina indirdigin için 1024 commit'i 10 adimda tararsin. Bu binary search'un gücü!"
:::

:::knowledge-check
type: multiple_choice
question: "Hangisi GitHub Flow'un temel kuralidir?"
options:
  - "Develop branch'i her zaman olmalidir"
  - "Release branch'leri zorunludur"
  - "Main branch her zaman deploy edilebilir durumdadir"
  - "Hotfix branch'leri main'den dallanir"
correct: 2
explanation: "GitHub Flow'un temel prensibi main'in her zaman deploy edilebilir olmasi. Feature branch'ler main'den dallanir, PR ile review edilir ve main'e merge edildikten sonra hemen deploy edilir. Git Flow'daki develop, release, hotfix gibi ek branch türleri yoktur."
:::

:::ai-guidance
title: Bu Derste AI ile Öğren
content: Branching, merging ve rebase gibi Git stratejilerini anlamak için AI'dan görsel aciklamalar ve senaryo bazli rehberlik al.
model_recommendation: Claude Opus 4.6
prompts:
  - prompt: "Git'te merge ve rebase arasindaki farki görsel olarak açıkla. Ayni senaryoda her ikisini de uygulayarak commit gecmisinin nasil degistigini adim adim göster. Hangi durumda hangisini secmeliyim?"
    why: "Merge ve rebase secimi ekip calismasinda en kritik Git kararidir. Görsel açıklama ile farklar kalici olarak öğrenir."
    follow_up: "Interactive rebase ile 5 commit'i 2 temiz commit'e nasil birlestiririm? Squash ve fixup farki ne?"
  - prompt: "Şu senaryoyu adim adim coz: Feature branch'imde çalışırken main'e yeni commit'ler geldi. Merge conflict çıktı. Conflict isaretlerini açıkla, VS Code'da nasil cozecegimi ve git komutlarini sırala."
    why: "Merge conflict çözümü junior developer'larin en çok zorlandigi konudur. Pratik senaryo ile ozguven kazanirsin."
pair_programming_tip: "Git branch sorunlariyla karsilastiginda AI'a `git log --oneline --graph --all` ve `git status` ciktisini yapistir: 'Branch yapimi analiz et. Rebase mi merge mi yapmaliyim? Conflict nasil cozerim?'"
:::

:::interview
## Mülakat Sorulari

**Soru 1: Git Flow, GitHub Flow ve Trunk-Based Development arasindaki farklar nelerdir?**
- **Junior cevabi:** Farklı branch stratejileridir, Git Flow daha karmaşık, GitHub Flow daha basittir.
- **Senior cevabi:** Git Flow (main/develop/feature/release/hotfix) büyük release cycle'lari olan projeler içindir ama fazla karmasiktir. GitHub Flow (main + feature branch + PR) çoğu web uygulaması için idealdir çünkü CI/CD ile sürekli deploy yapılır. Trunk-Based Development ise herkesin main'e sik commit yaptigidir, feature flag'lerle kontrol edilir. Google, Facebook gibi büyük şirketler trunk-based kullanır çünkü merge conflict'leri minimuma indirir ve deployment frequency'yi arttırır.

**Soru 2: Merge conflict nasil cozulur? Conflict'leri minimize etmek için ne yapılır?**
- **Junior cevabi:** Conflict isaretlerini bulur, doğru kodu secip kaydederim.
- **Senior cevabi:** `<<<<<<<`, `=======`, `>>>>>>>` isaretleri conflict bolgesini gösterir. VS Code gibi editor'lerin merge tool'lari ile görsel olarak cozulebilir. Conflict'leri minimize etmek için: küçük, focused PR'lar acilmali, feature branch'ler kısa omurlu olmali (1-2 gun), main'den sik pull/rebase yapilmali, büyük refactoring'ler ayrı PR'da yapilmali. `git rerere` (reuse recorded resolution) tekrarlayan conflict'leri otomatik çözer.
:::

:::must-note
- Branch oluşturma: `git switch -c branch-adi` (modern), `git checkout -b branch-adi` (eski)
- Fast-forward merge: Hedef branch'te değişiklik yoksa pointer ileri tasir, merge commit oluşturmaz
- 3-way merge: Her iki branch'te değişiklik varsa merge commit oluşturur (common ancestor + iki branch ucu)
- Rebase: Commit'leri başka branch'in ucune tasir, duz geçmiş oluşturur. ASLA paylasilmis branch'te yapma!
- Interactive rebase komutlari: pick (kullan), reword (mesaj değiştir), squash (birleştir + mesaj), fixup (birleştir + mesaji at), edit (duzenle), drop (sil)
- Cherry-pick: Belirli bir commit'i secip başka branch'e uygular. Istisnai durumlarda kullan
- Git bisect: Binary search ile hatali commit'i bulur. N commit için log2(N) adimda bulur
- Merge conflict isaretleri: <<<<<<< HEAD, =======, >>>>>>> branch-adi - hepsini sil, doğru kodu seç
- Git Flow: main + develop + feature + release + hotfix (karmaşık, planli release)
- GitHub Flow: main + feature branch + PR (basit, sürekli deploy)
- Trunk-Based: Herkes main'e commit, feature flag, kısa branch (en hızlı, CI/CD zorunlu)
- Conflict onleme: Sik merge, küçük commit, iletişim, `rerere.enabled true`
- `git merge -X ours/theirs`: Conflict'te otomatik taraf secimi
- Branch isimlendirme: feature/, bugfix/, hotfix/ on ekleri, tire ayirici, Turkce karakter yok
:::

:::senior-learns
Bir Senior Developer veya CTO, branching ve merge stratejilerini ogrenirken şu yaklasimi benimser:

1. **Ekip buyuklugune gore strateji seçer** - 2-3 kisilik ekipte Git Flow gereksiz karmaşıklık ekler. Trunk-Based Development veya GitHub Flow yeterlidir. 20+ kisilik ekipte ise Git Flow'un yapısal disiplini degerli olabilir. Doğru stratejiyi seçmek, doğru kodu yazmak kadar önemlidir.

2. **Merge politikasi oluşturur** - "Squash merge mi, merge commit mi, rebase mi?" sorusuna ekip için tek bir cevap belirler ve bunu dokumante eder. Tutarsiz merge stratejisi git log'u okunamaz hale getirir. Örneğin: "Feature branch'ler squash merge, release branch'ler merge commit" gibi net kurallar koyar.

3. **Branch protection kurallarini konfigure eder** - main branch'e doğrudan push'u engeller, PR zorunlulugu koyar, CI check'lerinin gecmesini şart kosar, minimum reviewer sayisi belirler. Bu kurallar "guven ama doğrula" prensibinin teknik uygulamasidir.

4. **Conflict resolution kulturunu oluşturur** - Conflict cikmasi basarisizlik değil, paralel calismanin dogal sonucudur. Ekibe conflict çözme egitimi verir, pair programming ile zor conflict'leri birlikte çözer. `rerere` gibi araclari ekip genelinde aktiflestirir.

5. **Commit geçmişini bir iletişim araci olarak gorur** - `git log --oneline --graph` ciktisi projenin hikayesini anlatmalidir. Her commit mesaji "neden" sorusuna cevap vermeli. Interactive rebase ile PR'daki commit'leri temizlemeyi takim kulturu haline getirir.

6. **Feature flag disiplini uygular** - Trunk-Based Development'ta büyük özellikleri feature flag arkasinda gelistirir. Bu sayede tamamlanmamis kod production'da olabilir ama kullaniciya gorunmez. LaunchDarkly veya kendi flag sistemiyle feature rollout'u kontrol eder.

**Profesyonel Mindset:** "Branching stratejisi bir teknik karar değil, organizasyonel bir karardir. Ekibinin deploy sikligi, test otomasyonu seviyesi ve iletişim kalitesi hangi stratejinin uygun oldugunu belirler. Doğru araclari kullanmak önemli ama doğru süreci tasarlamak daha önemli. En iyi branch stratejisi, ekibinin en hızlı ve güvenli şekilde değer uretmesini sağlayan stratejidir."
:::

:::english
**Teknik Ingilizce - Bu Dersteki Terimler:**

1. **Branch** (brantsh) - Dal / Dallanma
   *"I created a new branch to work on the login feature."*

2. **Merge** (murj) - Birleştirme
   *"We need to merge the feature branch into main before the release."*

3. **Rebase** (ri-beys) - Yeniden Temellendirme
   *"I rebased my branch on top of main to get the latest changes."*

4. **Conflict** (kon-flikt) - Çatışma
   *"There's a merge conflict in the config file that needs manual resolution."*

5. **Cherry-pick** (che-ri-pik) - Secici Alma
   *"Let's cherry-pick that hotfix commit into the release branch."*

**Okuma Egzersizi:** Atlassian'in Git branching rehberini Ingilizce oku: https://www.atlassian.com/git/tutorials/using-branches

**Yazma Pratigi:** Aşağıdaki commit mesajlarini Ingilizce yaz: "Login branch'ini main'e merge ettim"
-> Örnek: `merge: integrate login feature branch into main`
:::

:::external-resource
- **Atlassian Git Tutorials:** "Git Branch" ve "Merging vs Rebasing" rehberleri (Ingilizce, ücretsiz)
- **Learn Git Branching:** learngitbranching.js.org (interaktif, görsel, ücretsiz)
- **Oh My Git!:** Oyun ile Git öğrenme (ücretsiz, açık kaynak)
- **Git Flow cheatsheet:** danielkummer.github.io/git-flow-cheatsheet (görsel referans)
- **Pro Git Book:** git-scm.com/book - Bolum 3: Git Branching (ücretsiz, Ingilizce)
:::
