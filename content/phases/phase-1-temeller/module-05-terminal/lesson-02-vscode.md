---
id: mod-05-terminal/lesson-02
title: "VS Code Mastery ve Geliştirici Araçları"
estimated_minutes: 40
tags: ["vscode", "ide", "debugging", "npm", "yarn", "pnpm", "developer-tools"]
prerequisites: ["mod-05-terminal/lesson-01"]
order: 2
---

# VS Code Mastery ve Geliştirici Araçları

:::realworld
VS Code, dünya genelinde geliştiricilerin %70'inden fazlasının tercih ettiği editördür. Ama çoğu geliştirici VS Code'un gücünün %10'unu bile kullanmıyor. Doğru shortcut'ları bilmek, debugging araçlarını etkin kullanmak ve editörü kendi ihtiyaçlarına göre yapılandırmak seni ortalama bir geliştiriciden 2-3 kat daha hızlı yapar. Bu derste VS Code'u bir profesyonel gibi kullanmayı öğreneceksin.
:::

## Neden VS Code?

- **Ücretsiz ve açık kaynak** - Microsoft destekli, sürekli güncelleniyor
- **Extension ekosistemi** - 50.000+ eklenti ile her dile ve framework'e uyarlanabilir
- **Entegre terminal** - Editörden çıkmadan terminal komutları çalıştır
- **Git entegrasyonu** - Yerleşik Git desteği ile versiyon kontrolü
- **IntelliSense** - Akıllı kod tamamlama ve hata tespiti
- **Remote development** - SSH, Container ve WSL üzerinden uzak geliştirme

:::deha-tip
Deha seviyesi geliştiriciler fareye minimum dokunur. Her işlem için keyboard shortcut bilirler. VS Code'un Command Palette'i (`Ctrl+Shift+P`) onların en yakın dostudur. Yeni bir shortcut öğrenmek, kariyerin boyunca binlerce fare tıklamasını ortadan kaldırır.
:::

## Temel Keyboard Shortcut'lar

### Dosya ve Editör Yönetimi

:::code[text]{title="Dosya ve Editör Shortcut'ları (Windows/Linux)"}
Ctrl+P              → Quick Open (dosya adıyla hızlı aç)
Ctrl+Shift+P        → Command Palette (tüm komutlara eriş)
Ctrl+Shift+N        → Yeni pencere aç
Ctrl+N              → Yeni dosya oluştur
Ctrl+W              → Aktif tab'ı kapat
Ctrl+Tab            → Açık tab'lar arası geç
Ctrl+\              → Editörü yan yana böl (split)
Ctrl+1/2/3          → Editör grupları arası geç
Ctrl+B              → Sidebar'ı aç/kapat
Ctrl+J              → Terminal panel'i aç/kapat
Ctrl+`              → Entegre terminal'i aç/kapat
Ctrl+Shift+E        → Explorer panel'i aç
Ctrl+Shift+F        → Global arama aç
Ctrl+Shift+G        → Git panel'i aç
Ctrl+Shift+X        → Extensions panel'i aç
:::

### Kod Düzenleme

:::code[text]{title="Kod Düzenleme Shortcut'ları"}
Ctrl+D              → Seçili kelimeyi bul ve bir sonrakini de seç (multi-select)
Ctrl+Shift+L        → Seçili kelimenin TÜM tekrarlarını seç
Alt+Click           → Multi-cursor: her tıklanan yere cursor ekle
Ctrl+Alt+Up/Down    → Üst/alt satıra cursor ekle
Alt+Up/Down         → Satırı yukarı/aşağı taşı
Alt+Shift+Up/Down   → Satırı kopyala (duplicate)
Ctrl+Shift+K        → Satırı sil
Ctrl+/              → Satırı yorum satırına çevir/geri al
Ctrl+Shift+A        → Blok yorum (/* */ veya <!-- -->)
Ctrl+L              → Tüm satırı seç
Ctrl+Shift+[/]      → Kod bloğunu katla/aç (fold/unfold)
Ctrl+H              → Bul ve değiştir
Ctrl+Shift+H        → Tüm dosyalarda bul ve değiştir
F2                  → Sembol yeniden adlandır (rename symbol)
Ctrl+.              → Quick Fix / Code Action
Ctrl+Space          → IntelliSense'i tetikle
:::

:::tip
`Ctrl+D` shortcut'u refactoring için inanılmaz güçlüdür. Bir değişken adını seçip `Ctrl+D` ile tüm kullanımlarını seçerek aynı anda değiştirebilirsin. Ama `F2` (Rename Symbol) daha güvenlidir çünkü semantic olarak doğru yeniden adlandırma yapar.
:::

### Multi-Cursor Editing

:::code[text]{title="Multi-Cursor Teknikleri"}
# Senaryo 1: Aynı kelimeyi birden fazla yerde değiştir
# 1. Kelimeyi seç
# 2. Ctrl+D ile sıradaki eşleşmeyi ekle (istemediğini Ctrl+K Ctrl+D ile atla)
# 3. Hepsini seçince yeni değeri yaz

# Senaryo 2: Birden fazla satırın başına/sonuna ekleme
# 1. İlk satıra tıkla
# 2. Ctrl+Alt+Down ile aşağıya cursor ekle
# 3. Home/End ile satır başı/sonu
# 4. Yazmaya başla - tüm satırlara aynı anda yazılır

# Senaryo 3: Regex ile çoklu seçim
# 1. Ctrl+H ile Find and Replace aç
# 2. Regex modunu aç (Alt+R)
# 3. Pattern yaz, Ctrl+Alt+Enter ile tüm eşleşmeleri seç

# Örnek: Tüm const'ları let'e çevir
# Ctrl+H → const → let → Ctrl+Alt+Enter
:::

## VS Code Debugging

:::concept[Debugging (İng: Debugging)]
Debugging, koddaki hataları (bug) bulmak ve düzeltmek için adım adım kod çalıştırma, değişken değerlerini inceleme ve programın akışını izleme sürecidir.

**Türkçe karşılığı:** Hata Ayıklama
**Ne işe yarar:** console.log yerine profesyonel hata ayıklama araçlarıyla kodun iç dünyasını keşfetmeni sağlar
**Gerçek hayat benzetmesi:** Bir doktorun röntgen ve MR ile hastayı incelemesi gibi - içerideki sorunu görmek için doğru araçları kullanmak
:::

### Breakpoints

:::code[text]{title="Breakpoint Türleri"}
# Temel Breakpoint
# Satır numarasının soluna tıkla (kırmızı nokta oluşur)
# Program bu satıra geldiğinde durur

# Conditional Breakpoint (Koşullu)
# Satır numarasına sağ tıkla → "Add Conditional Breakpoint"
# Örnek: i > 100 (sadece i 100'den büyükken dur)

# Logpoint (Log Noktası)
# Breakpoint gibi ama programı durdurmaz, console'a yazar
# Sağ tıkla → "Add Logpoint"
# Mesaj: "Kullanıcı ID: {userId}, İsim: {userName}"

# Hit Count Breakpoint
# Belirli sayıda çalıştıktan sonra dur
# Sağ tıkla → "Add Hit Count Breakpoint" → "5" (5. çalışmada dur)

# Exception Breakpoint
# Debug panel → Breakpoints → "Caught Exceptions" veya "Uncaught Exceptions"
# Hata fırlatıldığında otomatik dur
:::

### Debug Controls

:::code[text]{title="Debug Kontrolleri"}
F5                  → Debug başlat / devam et (Continue)
F10                 → Step Over (fonksiyonun içine girmeden sonraki satır)
F11                 → Step Into (fonksiyonun içine gir)
Shift+F11           → Step Out (fonksiyondan çık)
Ctrl+Shift+F5       → Debug'ı yeniden başlat (Restart)
Shift+F5            → Debug'ı durdur (Stop)
F9                  → Breakpoint ekle/kaldır (toggle)
:::

### Debug Panelleri

:::code[text]{title="Debug Panelleri ve Kullanımları"}
# 1. VARIABLES (Değişkenler)
# Mevcut scope'taki tüm değişkenleri ve değerlerini gösterir
# Local, Closure ve Global scope'ları ayrı ayrı gösterir

# 2. WATCH (İzleme)
# Belirli ifadeleri sürekli izle
# + butonuyla ekle: user.name, items.length, arr[0].id
# Karmaşık ifadeler de yazabilirsin: items.filter(x => x.active).length

# 3. CALL STACK (Çağrı Yığını)
# Fonksiyonların çağrılma sırasını gösterir
# Hangi fonksiyondan hangi fonksiyona gelindiğini takip eder
# Stack overflow hatalarını anlamak için kritik

# 4. BREAKPOINTS
# Tüm breakpoint'leri listeler
# Tek tek etkinleştir/devre dışı bırak
# "Caught Exceptions" ile try-catch içindeki hataları yakala

# 5. DEBUG CONSOLE
# Debug sırasında JavaScript ifadelerini çalıştır
# Değişken değerlerini sorgula: myVariable
# Fonksiyon çağır: calculateTotal(items)
:::

### launch.json Konfigürasyonu

:::code[json]{title=".vscode/launch.json Örnekleri"}
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Node.js: Current File",
      "type": "node",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Node.js: Express App",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/src/server.js",
      "env": {
        "NODE_ENV": "development",
        "PORT": "3000"
      },
      "console": "integratedTerminal"
    },
    {
      "name": "Chrome: React App",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/src"
    },
    {
      "name": "Node.js: Attach",
      "type": "node",
      "request": "attach",
      "port": 9229
    }
  ]
}
:::

:::beginner-mistake
En yaygın hata: Hala `console.log` ile debug yapmak. `console.log("buraya geldi")`, `console.log("x degeri:", x)` yazmak yerine breakpoint koy, Watch'a ekle ve Call Stack'i incele. Debugger sana çok daha fazla bilgi verir ve kodu kirletmez.
:::

## Temel VS Code Extensions

:::comparison
| Extension | Kategori | Açıklama |
|-----------|----------|----------|
| ESLint | Linting | JavaScript/TypeScript hata ve stil kontrolü |
| Prettier | Formatting | Otomatik kod formatlama |
| GitLens | Git | Git blame, history, compare - satır bazında git geçmişi |
| Thunder Client | API | VS Code içinde API test etme (Postman alternatifi) |
| Auto Rename Tag | HTML | HTML tag'lerini otomatik eşleştirme |
| Error Lens | Debug | Hataları satırın yanında gösterme |
| Path Intellisense | Productivity | Dosya yollarını otomatik tamamlama |
| Live Server | Web | HTML dosyalarını canlı sunucu ile görüntüleme |
| Docker | DevOps | Docker container yönetimi |
| Remote - SSH | Remote | SSH üzerinden uzak geliştirme |
| GitHub Copilot | AI | AI destekli kod tamamlama |
| Material Icon Theme | UI | Dosya ikonları |

**Tavsiye:** Çok fazla extension yükleme! Sadece ihtiyacın olanları yükle. Fazla extension VS Code'u yavaşlatır.
:::

## settings.json - VS Code Yapılandırma

:::code[json]{title="Önerilen settings.json"}
{
  // Editör
  "editor.fontSize": 14,
  "editor.fontFamily": "'Fira Code', 'Cascadia Code', Consolas, monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 2,
  "editor.wordWrap": "on",
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.cursorBlinking": "smooth",
  "editor.smoothScrolling": true,
  "editor.linkedEditing": true,
  "editor.suggestSelection": "first",
  "editor.inlineSuggest.enabled": true,

  // Terminal
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.defaultProfile.windows": "Git Bash",

  // Dosya
  "files.autoSave": "onFocusChange",
  "files.exclude": {
    "**/node_modules": true,
    "**/.git": true,
    "**/dist": true,
    "**/.DS_Store": true
  },
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,

  // Arama
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true,
    "**/.next": true
  },

  // Emmet
  "emmet.includeLanguages": {
    "javascript": "javascriptreact",
    "typescript": "typescriptreact"
  },

  // Git
  "git.autofetch": true,
  "git.confirmSync": false,

  // Prettier
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
:::

:::tip
`Ctrl+Shift+P` → "Preferences: Open Settings (JSON)" yazarak settings.json'a hızlıca erişebilirsin. GUI ayarlar yerine JSON'u öğren, çünkü settings'i başka bilgisayara taşımak ve versiyon kontrole almak daha kolaydır.
:::

## tasks.json - Görev Otomasyonu

:::code[json]{title=".vscode/tasks.json Örnekleri"}
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Dev Server",
      "type": "npm",
      "script": "dev",
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      },
      "group": "build"
    },
    {
      "label": "Run Tests",
      "type": "npm",
      "script": "test",
      "problemMatcher": [],
      "group": {
        "kind": "test",
        "isDefault": true
      }
    },
    {
      "label": "Build Production",
      "type": "npm",
      "script": "build",
      "problemMatcher": ["$tsc"],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "label": "Lint Fix",
      "type": "shell",
      "command": "pnpm exec eslint --fix src/",
      "problemMatcher": ["$eslint-stylish"]
    }
  ]
}
:::

## Code Snippets - Kod Parçacıkları

:::code[json]{title="Kullanıcı Snippet'ları (.vscode/snippets.code-snippets)"}
{
  "React Functional Component": {
    "prefix": "rfc",
    "body": [
      "import React from 'react';",
      "",
      "const ${1:ComponentName} = (${2:props}) => {",
      "  return (",
      "    <div>",
      "      $0",
      "    </div>",
      "  );",
      "};",
      "",
      "export default ${1:ComponentName};"
    ],
    "description": "React Functional Component oluştur"
  },
  "Console Log": {
    "prefix": "clg",
    "body": "console.log('${1:label}:', ${2:value});",
    "description": "console.log kısayolu"
  },
  "Try Catch": {
    "prefix": "trycatch",
    "body": [
      "try {",
      "  $1",
      "} catch (error) {",
      "  console.error('${2:Hata}:', error.message);",
      "  $0",
      "}"
    ],
    "description": "Try-catch bloğu"
  },
  "Arrow Function": {
    "prefix": "af",
    "body": "const ${1:name} = (${2:params}) => ${3:{$0}};",
    "description": "Arrow function"
  }
}
:::

:::tip
Snippet oluşturmak için: `Ctrl+Shift+P` → "Snippets: Configure User Snippets" → dil seç. Sık kullandığın kod yapılarını snippet'e çevir. Snippet Generator: https://snippet-generator.app/ sitesini kullan.
:::

## Workspace Settings

:::code[json]{title=".vscode/settings.json (Workspace Level)"}
{
  // Proje bazlı ayarlar (global ayarları override eder)
  "editor.tabSize": 2,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,

  // TypeScript
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.suggest.autoImports": true,

  // Dosya ilişkilendirme
  "files.associations": {
    "*.css": "tailwindcss",
    ".env*": "dotenv"
  },

  // Önerilen extensions
  "extensions.recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "eamodio.gitlens",
    "bradlc.vscode-tailwindcss"
  ]
}
:::

## Package Managers: npm vs yarn vs pnpm

:::concept[Package Manager (İng: Paket Yöneticisi)]
Package manager, projenin bağımlılıklarını (dependency) yönetir: indirme, güncelleme, versiyon kontrolü ve silme işlemlerini otomatikleştirir.

**Türkçe karşılığı:** Paket Yöneticisi
**Ne işe yarar:** Projede kullanılan kütüphaneleri otomatik olarak yönetir
**Gerçek hayat benzetmesi:** Bir mutfakta tarif için gerekli malzemeleri otomatik olarak sipariş eden bir sistem
:::

:::comparison
| Özellik | npm | yarn | pnpm |
|---------|-----|------|------|
| **Hız** | Yavaş (v7 ile iyileşti) | Hızlı (parallel download) | En hızlı (hardlink kullanır) |
| **Disk alanı** | Her projede ayrı kopya | Her projede ayrı kopya | Tek global store, hardlink |
| **Lock dosyası** | package-lock.json | yarn.lock | pnpm-lock.yaml |
| **Workspace** | npm workspaces (v7+) | yarn workspaces | pnpm workspaces |
| **Güvenlik** | npm audit | yarn audit | pnpm audit |
| **Node.js ile gelir** | Evet | Hayır (ayrıca yükle) | Hayır (ayrıca yükle) |
| **Phantom deps** | Var (hoisting sorunu) | Var (hoisting sorunu) | Yok (strict by default) |
| **Monorepo desteği** | Temel | İyi | En iyi |
| **Kurulum** | Node.js ile gelir | `corepack enable && corepack prepare yarn@stable` | `corepack enable && corepack prepare pnpm@latest` |

**Tavsiye (📌 2026):** Direkt pnpm ile basla -- `corepack enable && corepack prepare pnpm@latest` ile kur. Daha hizli, disk verimli ve strict dependency resolution sayesinde phantom dependency sorunlari yok. npm bilgisi de faydali ama yeni projelerde pnpm tercih et.
:::

:::code[bash]{title="Package Manager Komut Karşılaştırması"}
# Proje başlatma
npm init -y                    | yarn init -y              | pnpm init
# Paket yükleme
npm install express            | yarn add express           | pnpm add express
# Dev dependency
npm install -D jest            | yarn add -D jest           | pnpm add -D jest
# Global yükleme
npm install -g nodemon         | yarn global add nodemon    | pnpm add -g nodemon
# Paket kaldırma
npm uninstall express          | yarn remove express        | pnpm remove express
# Tüm bağımlılıkları yükle
npm install                    | yarn install (veya yarn)   | pnpm install
# Script çalıştırma
npm run dev                    | yarn dev                   | pnpm dev
# Güncelleme kontrolü
npm outdated                   | yarn outdated              | pnpm outdated
# Güvenlik taraması
npm audit                      | yarn audit                 | pnpm audit
# Cache temizle
npm cache clean --force        | yarn cache clean           | pnpm store prune
:::

:::beginner-mistake
Yaygın hata: Bir projede hem npm hem pnpm (veya yarn) kullanmak. Bu, farklı lock dosyaları oluşturur ve takım üyeleri arasında bağımlılık uyumsuzluğuna neden olur. Bir proje bir package manager seçmeli ve herkes onu kullanmalı. Lock dosyasını (pnpm-lock.yaml / package-lock.json / yarn.lock) Git'e commit edin!
:::

## Verimlilik İpuçları

:::code[text]{title="VS Code Pro Tips"}
# 1. Zen Mode - Dikkat dağıtıcıları kaldır
Ctrl+K Z              → Zen Mode (çık: Esc Esc)

# 2. Emmet - HTML/CSS hızlı yazma
div.container>ul>li*5  → Tab ile genişlet

# 3. Quick Fix
Ctrl+.                → Hızlı düzeltme önerileri

# 4. Go to Definition
F12                   → Tanıma git
Alt+F12               → Peek Definition (küçük pencerede göster)
Ctrl+Shift+F12        → Go to Implementation

# 5. Breadcrumbs
# Dosya yolunu editörün üstünde gösterir
# Ctrl+Shift+. ile breadcrumb'a odaklan ve navigasyon yap

# 6. Timeline
# Explorer'da dosyanın Git geçmişini gösterir
# Dosyaya sağ tıkla → "Timeline" paneli

# 7. Multiple Terminals
Ctrl+Shift+`          → Yeni terminal oluştur
# Terminal panelinde split ile yan yana terminaller aç

# 8. Sticky Scroll
# settings.json: "editor.stickyScroll.enabled": true
# Uzun dosyalarda hangi fonksiyon/class'ta olduğunu gösterir
:::

:::exercise
### Alistirma 1: VS Code Shortcut'lari ile Hizli Duzenleme (Kolay)

Asagidaki kodu VS Code'da acarak shortcut'lari pratik yap.

```javascript
// Bu kodu VS Code'da bir dosyaya yapistir ve asagidaki gorevleri yap:

function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total = total + items[i].price;
  }
  return total;
}

function calculateTax(total) {
  return total * 0.18;
}

function calculateGrandTotal(items) {
  const total = calculateTotal(items);
  const tax = calculateTax(total);
  return total + tax;
}

// GOREVLER (shortcut'lari kullanarak yap):
// 1. Ctrl+D ile "calculate" kelimesini sec, 3 kez daha Ctrl+D bas
//    → Tum "calculate" kelimelerini ayni anda sec ve "compute" olarak degistir
//
// 2. Alt+Up/Down ile calculateTax fonksiyonunu calculateTotal'in USTUNE tasi
//
// 3. Alt+Shift+Down ile calculateGrandTotal fonksiyonunun
//    ilk satirini kopyala (asagiya duplicate)
//
// 4. Ctrl+/ ile calculateTax fonksiyonunu tamamen yorum satirina cevir
//
// 5. Ctrl+Shift+K ile bos satirlari sil
//
// 6. Ctrl+H ile "total" kelimesini "sum" ile degistir (Replace All)
```

**Beklenen Sonuc:** Tum degisiklikler fare kullanmadan, sadece klavye shortcut'lari ile yapilmis olmali. Multi-cursor editing ile ayni anda birden fazla yerde degisiklik yapabilmeli.
**Ipucu:** Ctrl+D tekrar tekrar basarak ayni kelimeyi secmeye devam edersin. Esc ile multi-cursor modundan cikarsin.

---

### Alistirma 2: VS Code Debugging (Orta)

Bir Node.js uygulamasini VS Code debugger ile adim adim calistir ve hata bul.

```javascript
// debug-practice.js dosyasini olustur:
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

function findMax(arr) {
  let max = arr[0];
  for (let i = 0; i < arr.length; i++) {  // BUG: i = 0 yerine i = 1 olmali mi?
    if (arr[i] > max) {
      max = arr[i];
    }
  }
  return max;
}

function processData(data) {
  const results = [];
  for (const item of data) {
    const fib = fibonacci(item.value);
    results.push({
      name: item.name,
      original: item.value,
      fibonacci: fib,
    });
  }
  return results;
}

// Test verisi
const testData = [
  { name: "A", value: 5 },
  { name: "B", value: 8 },
  { name: "C", value: 3 },
  { name: "D", value: 10 },
];

const processed = processData(testData);
console.log("Islenenmis veri:", processed);

const maxValue = findMax(testData.map(d => d.value));
console.log("Max deger:", maxValue);

// DEBUGGING GOREVLERI:
// 1. processData fonksiyonunun ilk satirina breakpoint koy (F9)
// 2. F5 ile debug baslat (Node.js secenegi)
// 3. Watch paneline "item.name" ve "fib" ekle
// 4. F10 (Step Over) ile dongu icinde ilerle
// 5. fibonacci(8) cagirisinda F11 (Step Into) ile fonksiyonun icine gir
// 6. Call Stack panelinde recursive cagrilari gozlemle
// 7. Debug Console'da "results.length" yaz ve degerini gor
```

**Beklenen Sonuc:** Breakpoint'te durdugundan sonra Watch panelinde degiskenlerin degerlerini gorebilmeli. Step Into ile recursive fonksiyon icine girebilmeli. fibonacci(8) = 21 olmali.
**Ipucu:** launch.json olmadan F5'e basinca VS Code otomatik Node.js debug konfigurasyonu olusturur.

---

### Alistirma 3: Custom Snippets ve Workspace Ayarlari (Zor)

VS Code'u projene ozel olarak yapilandir: custom snippet'ler, workspace settings ve extension onerileri olustur.

```json
// GOREV 1: Custom Snippet olustur
// File > Preferences > Configure User Snippets > javascript.json
// Asagidaki snippet'i ekle:
{
  "React Functional Component": {
    "prefix": "rfc",
    "body": [
      "import React from 'react';",
      "",
      "interface ${1:ComponentName}Props {",
      "  $2",
      "}",
      "",
      "export function ${1:ComponentName}({ $3 }: ${1:ComponentName}Props) {",
      "  return (",
      "    <div>",
      "      <h1>${1:ComponentName}</h1>",
      "      $0",
      "    </div>",
      "  );",
      "}",
      ""
    ],
    "description": "React Functional Component with TypeScript"
  },
  "Console Log Variable": {
    "prefix": "clv",
    "body": "console.log('${1:variable}:', ${1:variable});",
    "description": "Console log with variable name"
  }
}

// GOREV 2: Workspace Settings olustur
// .vscode/settings.json:
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "files.exclude": {
    "node_modules": true,
    "dist": true
  }
}

// GOREV 3: Extension onerileri olustur
// .vscode/extensions.json:
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss"
    // TODO: 2-3 extension daha ekle
  ]
}

// Test: Yeni bir .tsx dosyasi ac, "rfc" yaz ve Tab'a bas
// → Component sablonu otomatik olusturulmali
```

**Beklenen Sonuc:** "rfc" yazip Tab'a basinca React component sablonu olusturulmali. Kaydettiginde dosya otomatik formatlanmali. Takim arkadaslarin projeyi actiginda onerilecek extension'lari gormeli.
**Ipucu:** Snippet'lerde `$1`, `$2` tab stop'lardir (Tab ile aralarinda gecis yapilir). `${1:default}` varsayilan degerdir. `$0` son cursor pozisyonudur.
:::

:::knowledge-check
type: multiple_choice
question: "VS Code'da Ctrl+Shift+P ne yapar?"
options:
  - "Dosyayı yazdırır (print)"
  - "Projeyi paketler"
  - "Command Palette açar - tüm VS Code komutlarına erişim sağlar"
  - "Push yapar (git push)"
correct: 2
explanation: "Command Palette, VS Code'un en güçlü özelliğidir. Tüm komutlara, ayarlara ve işlevlere buradan erişebilirsin. Bir shortcut'u bilmiyorsan Command Palette'e yaz."
:::

:::knowledge-check
type: multiple_choice
question: "Debugging sırasında F10 (Step Over) ve F11 (Step Into) arasındaki fark nedir?"
options:
  - "F10 programı durdurur, F11 devam ettirir"
  - "F10 fonksiyonun içine girmeden sonraki satıra geçer, F11 fonksiyonun içine girer"
  - "F10 breakpoint ekler, F11 breakpoint kaldırır"
  - "Aralarında fark yoktur"
correct: 1
explanation: "Step Over (F10), fonksiyon çağrısını tek adımda geçer. Step Into (F11), fonksiyonun içine girerek satır satır çalıştırır. Step Out (Shift+F11) ise fonksiyondan çıkar. Bu üç kontrol debugging'in temelini oluşturur."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Gunluk gelistirme workflow'unuzda hangi IDE/editor araclarini kullaniyorsunuz?**
- **Junior cevabi:** VS Code kullaniyorum, extension'lar yukluyorum.
- **Senior cevabi:** VS Code'da verimlilik icin: multi-cursor editing (Alt+Click), Emmet ile hizli HTML, GitLens ile blame/history, ESLint + Prettier entegrasyonu (format on save), debugger ile breakpoint debugging (console.log yerine), integrated terminal ile context switch'i azaltma, workspace settings ile proje bazli konfigurasyonlar. Remote Development extension'i ile SSH uzerinden sunucuda calisma, Dev Containers ile tutarli gelistirme ortami. Sonuc olarak editor ustaligi gunluk uretkenlige direkt etkilidir.

**Soru 2: Debugging icin console.log yerine ne kullanilmali?**
- **Junior cevabi:** Debugger kullanilabilir ama console.log da ise yarar.
- **Senior cevabi:** Breakpoint debugging console.log'dan ustundur cunku: 1) Call stack'i gorursun (fonksiyona nereden gelindigini), 2) Scope'daki tum degiskenleri inceleyebilirsin, 3) Watch expression'larla kosullu izleme yapabilirsin, 4) Step over/into/out ile akisi takip edebilirsin, 5) Conditional breakpoint ile sadece belirli kosullarda durabilirsin. Ancak production'da structured logging (Winston, Pino) ile log level'lar (error, warn, info, debug) kullanilir. console.log production kodda kalmamalidir, lint rule'lariyla engellenir.
:::

:::ai-guidance
### 🤖 AI ile Öğren

**Önerilen Model:** Claude Sonnet 4.5 veya GPT-4o

**Prompt Örnekleri:**

1. **Derinlemesine Anla:** "VS Code'un multi-cursor editing, snippet sistemi ve workspace settings yapısını detaylıca açıkla. Her birinin günlük geliştirme akışını nasıl hızlandırdığını örneklerle göster."

2. **Pratik Uygulama:** "VS Code'da bir React + TypeScript projesi için ideal extension listesi, settings.json konfigürasyonu ve keyboard shortcut'ları öner. Sonra bu setup'ı adım adım uygulamamda bana yardım et."

3. **Mükemmellik İçin:** "Senior developer'ların VS Code'u nasıl kullandığını anlat — debugging workflow, Git integration, terminal multiplexing, remote development. Junior ve senior kullanım farkını göster."

> **Pair Programming İpucu:** AI'a VS Code'da yavaş hissettiğin bir işlemi anlat. Daha hızlı yapmanın yolunu ve ilgili shortcut'ları öğren.
:::

:::exercise
### Alıştırma 4: Multi-Cursor ile Toplu Düzenleme

**Görev:** VS Code multi-cursor özelliklerini kullanarak bir dosyayı verimli şekilde düzenle.

**Başlangıç kodu:**
```javascript
// Bu kodu VS Code'da ac ve asagidaki gorevleri yap

// GOREV 1: Tum "var" kelimelerini "const" yap (Ctrl+D)
var name = "Ahmet";
var age = 25;
var email = "ahmet@test.com";
var city = "Istanbul";
var role = "developer";

// GOREV 2: Her satirin sonuna noktalı virgul ekle (Alt+Shift+I ile satir sonlarina cursor koy)
const items = [
  { id: 1, name: "Laptop", price: 15000 }
  { id: 2, name: "Phone", price: 8000 }
  { id: 3, name: "Tablet", price: 5000 }
  { id: 4, name: "Monitor", price: 3000 }
]

// GOREV 3: Her objenin "price" anahtarini "cost" olarak degistir
// Ctrl+Shift+L ile tum "price" secimlerini yap, sonra "cost" yaz

// GOREV 4: Satir numaralarini ekle (Alt+Click ile multi-cursor)
function processItem(item) {}
function validateItem(item) {}
function saveItem(item) {}
function deleteItem(item) {}
function updateItem(item) {}

// Her fonksiyonun basina yorum olarak numara ekle:
// // 1. processItem
// // 2. validateItem
// vb.
```

**Beklenen çıktı:**
```
Tum degisiklikler fare kullanmadan sadece klavye ile yapilmis.
- 5 "var" -> "const" donusumu (Ctrl+D ile)
- 4 satir sonuna "," eklenmis (Alt+Shift+I ile)
- 4 "price" -> "cost" degisimi (Ctrl+Shift+L ile)
```

**İpucu:** `Ctrl+D` = sonraki eşleşmeyi ekle. `Alt+Shift+I` = seçili satırların sonlarına cursor koy. `Alt+Click` = istediğin yere cursor ekle.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: VS Code Snippet Oluşturma

**Görev:** Kendi özel code snippet'lerini oluştur ve kullan.

**Başlangıç kodu:**
```json
// VS Code: Ctrl+Shift+P -> "Preferences: Configure User Snippets"
// javascript.json secilecek

// GOREV: Asagidaki snippet'leri ekle:

{
  "React Functional Component": {
    "prefix": "rfc",
    "body": [
      "import React from 'react';",
      "",
      "interface ${1:ComponentName}Props {",
      "  $2",
      "}",
      "",
      "export const ${1:ComponentName}: React.FC<${1:ComponentName}Props> = ({ $3 }) => {",
      "  return (",
      "    <div>",
      "      <h1>${1:ComponentName}</h1>",
      "      $0",
      "    </div>",
      "  );",
      "};",
      "",
      "export default ${1:ComponentName};"
    ],
    "description": "React functional component with TypeScript"
  },

  "Console Log Variable": {
    "prefix": "clv",
    "body": "console.log('${1:variable}:', ${1:variable});",
    "description": "Console log with variable name"
  },

  "Try-Catch Async": {
    "prefix": "tca",
    "body": [
      "try {",
      "  const result = await ${1:asyncFunction}($2);",
      "  $0",
      "} catch (error) {",
      "  console.error('${1:asyncFunction} failed:', error);",
      "  throw error;",
      "}"
    ],
    "description": "Try-catch wrapper for async function"
  }
}
```

**Beklenen çıktı:**
```
"rfc" yazip Tab'a bastiginda:
  React component sablonu olusuyor
  Tab ile placeholder'lar arasinda geziniliyor
  Component adi otomatik her yere yansıyor

"clv" yazip Tab'a bastiginda:
  console.log('variable:', variable); olusuyor
  Variable adini yazinca her iki yerde de degisiyor
```

**İpucu:** `$1` ilk placeholder, `$0` son cursor pozisyonu. `${1:default}` varsayılan değerli placeholder. Aynı numara = aynı anda değişir.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 6: VS Code Debugger ile Karmaşık Bug Bulma

**Görev:** VS Code debugger kullanarak çok adımlı bir bug'ı tespit et ve düzelt.

**Başlangıç kodu:**
```javascript
// debug-challenge.js
// Bu kodda 3 bug var. Debugger ile bul!

class ShoppingCart {
  constructor() {
    this.items = [];
    this.discount = 0;
  }

  addItem(name, price, quantity) {
    this.items.push({ name, price, quantity });
  }

  removeItem(name) {
    // BUG 1: Nerede?
    this.items = this.items.filter(item => item.name !== name);
  }

  applyDiscount(percentage) {
    // BUG 2: Nerede?
    this.discount = percentage;
  }

  getTotal() {
    let total = 0;
    for (let i = 0; i <= this.items.length; i++) {  // BUG 3: Nerede?
      total += this.items[i].price * this.items[i].quantity;
    }
    return total * (1 - this.discount / 100);
  }

  getSummary() {
    return {
      itemCount: this.items.length,
      total: this.getTotal(),
      discount: `${this.discount}%`,
      items: this.items.map(i => `${i.name} x${i.quantity}`),
    };
  }
}

// Test
const cart = new ShoppingCart();
cart.addItem("Laptop", 15000, 1);
cart.addItem("Mouse", 200, 2);
cart.addItem("Keyboard", 500, 1);

console.log("Before discount:", cart.getSummary());

cart.applyDiscount(10);
console.log("After 10% discount:", cart.getSummary());

cart.removeItem("Mouse");
console.log("After remove Mouse:", cart.getSummary());

// GOREV: VS Code'da:
// 1. F5 ile debug baslat (launch.json olustur)
// 2. getTotal() icine breakpoint koy
// 3. Step over (F10) ile satir satir ilerle
// 4. Variables panelinde i, total, this.items degerlerini izle
// 5. 3 bug'i bul ve duzelt
```

**Beklenen çıktı:**
```
HATALI: TypeError veya yanlis toplam (bug'lar yuzunden)

DUZELTILMIS:
Before discount: { itemCount: 3, total: 15900, discount: '0%' }
After 10% discount: { itemCount: 3, total: 14310, discount: '10%' }
After remove Mouse: { itemCount: 2, total: 13950, discount: '10%' }
```

**İpucu:** Bug 3: `i <= this.items.length` off-by-one hatası (`<` olmalı). Debugger'da Variables paneli ile `i` değerini izle.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: VS Code Tasks ile Otomasyon

**Görev:** `tasks.json` ile proje görevlerini otomatize et.

**Başlangıç kodu:**
```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Dev Server",
      "type": "shell",
      "command": "npm run dev",
      "group": "build",
      "isBackground": true,
      "problemMatcher": [],
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "npm test",
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "problemMatcher": ["$jest"]
    },
    {
      "label": "Lint Fix",
      "type": "shell",
      "command": "npx eslint --fix src/",
      "problemMatcher": ["$eslint-stylish"]
    },
    {
      "label": "Build & Test",
      "dependsOn": ["Lint Fix", "Run Tests"],
      "dependsOrder": "sequence",
      "group": "build"
    }
  ]
}
```

**Beklenen çıktı:**
```
Tasks:
- "Dev Server" -> npm run dev (arka planda calisir)
- "Run Tests" -> npm test (Ctrl+Shift+B ile calistirilir)
- "Lint Fix" -> eslint --fix
- "Build & Test" -> Lint + Test sirayla calisir
```

**İpucu:** `Ctrl+Shift+B` ile build task çalıştırılır. `dependsOn` ile task'lar zincirlenir. `isBackground` arka plan task'ları için kullanılır.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 8: VS Code Extensions Yapılandırması

**Görev:** Takım standardı olarak kullanılacak extension listesi ve ayarları oluştur.

**Başlangıç kodu:**
```json
// .vscode/extensions.json - Takima onerilen extension'lar
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense",
    "usernamehw.errorlens",
    "eamodio.gitlens",
    "pkief.material-icon-theme",
    "github.copilot"
  ],
  "unwantedRecommendations": [
    "hookyqr.beautify"
  ]
}
```

```json
// .vscode/settings.json - Proje ayarlari
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit",
    "source.organizeImports": "explicit"
  },
  "editor.tabSize": 2,
  "editor.rulers": [80, 120],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "typescript.preferences.importModuleSpecifier": "relative",
  "emmet.includeLanguages": {
    "javascript": "javascriptreact",
    "typescript": "typescriptreact"
  }
}
```

**Beklenen çıktı:**
```
Proje acildiginda:
- VS Code onerilen extension'lari kurmasi icin bildirim gosterir
- formatOnSave aktif, her kayitte kod formatlanir
- ESLint hatalari aninda duzeltilir
- Import'lar otomatik organize edilir
```

**İpucu:** `.vscode/` dizini repo'ya dahil edilir. `settings.json` proje bazlı ayarları, `extensions.json` takım extension'larını tanımlar.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 9: VS Code Remote Development

**Görev:** VS Code'un Remote SSH ve Dev Containers özelliklerini yapılandır.

**Başlangıç kodu:**
```json
// .devcontainer/devcontainer.json
{
  "name": "Node.js Development",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "forwardPorts": [3000, 5173, 8080],
  "postCreateCommand": "npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
      }
    }
  }
}
```

```bash
#!/bin/bash
echo "=== Dev Container Kullanimi ==="
echo "1. VS Code'da F1 -> 'Dev Containers: Reopen in Container'"
echo "2. Docker container icinde VS Code acilir"
echo "3. Tum extension'lar ve ayarlar otomatik yuklenir"
echo "4. Port forwarding ile localhost:3000'e erisim"

echo -e "\n=== Remote SSH Kullanimi ==="
echo "1. VS Code'da F1 -> 'Remote-SSH: Connect to Host'"
echo "2. ~/.ssh/config'deki host'lardan birini sec"
echo "3. Uzak sunucuda VS Code acilir"
echo "4. Terminal, debugger, extension'lar uzakta calisir"

echo -e "\n=== GOREV ==="
echo "1. devcontainer.json dosyasini projene ekle"
echo "2. Docker kurulu ise 'Reopen in Container' yap"
echo "3. Container icinde terminal ac ve node --version calistir"
echo "4. Port 3000'de bir server baslat ve tarayicida ac"
```

**Beklenen çıktı:**
```
=== Dev Container Kullanimi ===
1. Docker container icinde calisma ortami hazir
2. Tum takım ayni ortamda calisir ("works on my machine" yok)
3. Yeni gelistirici 1 komutla baslar

=== Remote SSH Kullanimi ===
1. Uzak sunucuda lokal gibi gelistirme
```

**İpucu:** Dev Container'lar Docker kullanır. `"postCreateCommand"` container oluşturulduktan sonra çalışır. `"forwardPorts"` ile container portları lokale yönlendirilir.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: launch.json ile Gelişmiş Debug Konfigürasyonu

**Görev:** Farklı senaryolar için debug konfigürasyonları oluştur: Node.js, fullstack, test debugging.

**Başlangıç kodu:**
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Node.js: Current File",
      "type": "node",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "name": "Node.js: Backend API",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/backend/src/index.js",
      "env": {
        "NODE_ENV": "development",
        "PORT": "8000",
        "DB_HOST": "localhost"
      },
      "console": "integratedTerminal"
    },
    {
      "name": "Jest: Current Test File",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": [
        "${relativeFile}",
        "--config", "jest.config.js",
        "--no-coverage"
      ],
      "console": "integratedTerminal"
    },
    {
      "name": "Chrome: Frontend",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/frontend/src",
      "sourceMaps": true
    }
  ],
  "compounds": [
    {
      "name": "Fullstack: Backend + Frontend",
      "configurations": ["Node.js: Backend API", "Chrome: Frontend"],
      "stopAll": true
    }
  ]
}
```

```bash
echo "=== Debug Konfigurasyonlari ==="
echo "F5 ile debug baslat, dropdown'dan konfigurasyon sec:"
echo ""
echo "1. Node.js: Current File   -> Acik dosyayi debug et"
echo "2. Node.js: Backend API    -> Backend'i env vars ile debug et"
echo "3. Jest: Current Test File  -> Acik test dosyasini debug et"
echo "4. Chrome: Frontend        -> Frontend'i Chrome ile debug et"
echo "5. Fullstack               -> Backend + Frontend birlikte"

echo -e "\n=== GOREV ==="
echo "1. Bir JS dosyasi ac, breakpoint koy (satir numarasina tikla)"
echo "2. F5 ile 'Current File' konfigurasyonu ile baslat"
echo "3. Variables panelinde degiskenleri incele"
echo "4. Watch paneline 'this.items.length' gibi ifadeler ekle"
echo "5. Call Stack panelinde fonksiyon cagri zincirini gor"
echo "6. Debug Console'da runtime ifadeler yaz"
```

**Beklenen çıktı:**
```
=== Debug Konfigurasyonlari ===
F5 ile debug baslat, dropdown'dan konfigurasyon sec:

1. Node.js: Current File   -> Acik dosyayi debug et
2. Node.js: Backend API    -> Backend'i env vars ile debug et
3. Jest: Current Test File  -> Acik test dosyasini debug et
4. Chrome: Frontend        -> Frontend'i Chrome ile debug et
5. Fullstack               -> Backend + Frontend birlikte
```

**İpucu:** `compounds` birden fazla debug session'ı aynı anda başlatır. `skipFiles` ile node_modules içine girmekten kaçın. `env` ile ortam değişkenlerini override et.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: VS Code Workspace Yapılandırması

**Görev:** Multi-root workspace ve proje bazlı ayarlar oluştur.

**Başlangıç kodu:**
```json
// myproject.code-workspace
{
  "folders": [
    { "path": "frontend", "name": "Frontend (React)" },
    { "path": "backend", "name": "Backend (Python)" },
    { "path": "shared", "name": "Shared Libraries" }
  ],
  "settings": {
    "files.exclude": {
      "**/node_modules": true,
      "**/__pycache__": true,
      "**/.pytest_cache": true
    },
    "search.exclude": {
      "**/dist": true,
      "**/build": true,
      "**/coverage": true
    },
    "[python]": {
      "editor.defaultFormatter": "ms-python.black-formatter",
      "editor.formatOnSave": true,
      "editor.rulers": [88]
    },
    "[typescript]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode",
      "editor.formatOnSave": true
    },
    "[typescriptreact]": {
      "editor.defaultFormatter": "esbenp.prettier-vscode"
    }
  },
  "launch": {
    "configurations": [],
    "compounds": []
  }
}
```

**Beklenen çıktı:**
```
Workspace acildiginda:
- Sol panelde 3 ayri klasor gorunur
- Python dosyalari black ile formatlanir (88 karakter siniri)
- TypeScript dosyalari prettier ile formatlanir
- node_modules ve __pycache__ gizlenir
- Arama sonuclarinda dist/build/coverage cikartilir
```

**İpucu:** `.code-workspace` dosyasını `File > Open Workspace from File` ile aç. Her klasöre özel ayarlar `[python]` gibi dil bazlı yapılabilir.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 12: Refactoring Araçları ile Kod İyileştirme

**Görev:** VS Code'un refactoring araçlarını kullanarak kodu iyileştir.

**Başlangıç kodu:**
```javascript
// refactor-practice.js
// Bu kodu VS Code'da ac ve refactoring araclarini kullan

// GOREV 1: "Extract Function" (F2 veya sag tik > Refactor)
function processOrder(order) {
  // Bu blogu sec ve "Extract Function" yap -> "calculateTotal"
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
    if (item.discount) {
      total -= item.price * item.quantity * item.discount / 100;
    }
  }

  // Bu blogu sec ve "Extract Function" yap -> "applyTax"
  const taxRate = 0.18;
  const tax = total * taxRate;
  const grandTotal = total + tax;

  return { total, tax, grandTotal };
}

// GOREV 2: "Rename Symbol" (F2)
// "processOrder" fonksiyonunu "calculateOrderTotal" olarak yeniden adlandir
// Tum referanslar otomatik guncellenir

// GOREV 3: "Extract Variable"
function getUserDisplayName(user) {
  // Bu uzun ifadeyi sec -> "Extract Variable"
  return `${user.firstName} ${user.lastName} (${user.role === 'admin' ? 'Yonetici' : 'Kullanici'})`;
}

// GOREV 4: "Move to New File"
// getUserDisplayName fonksiyonunu sec -> "Move to New File"
// VS Code otomatik import ekler

console.log("Refactoring gorevlerini VS Code ile yap:");
console.log("1. Kod blogunu sec > Sag tik > Refactor > Extract Function");
console.log("2. Degisken/fonksiyon adina tikla > F2 > Yeni ad yaz");
console.log("3. Ifadeyi sec > Sag tik > Refactor > Extract Variable");
console.log("4. Fonksiyonu sec > Sag tik > Refactor > Move to New File");
```

**Beklenen çıktı:**
```
Refactoring sonrasi kod:
1. calculateTotal() ve applyTax() fonksiyonlari cikarilmis
2. processOrder -> calculateOrderTotal olarak yeniden adlandirilmis
3. Uzun ifade bir degiskene atanmis
4. getUserDisplayName ayri dosyaya tasinmis ve import eklenmis
```

**İpucu:** `F2` = Rename Symbol (tüm referansları günceller). `Ctrl+.` = Quick Fix menüsü (extract function, extract variable vb.). VS Code TypeScript/JavaScript dosyalarında en iyi refactoring desteği sunar.

**Zorluk:** Orta
:::

:::must-note
- `Ctrl+P` → dosya hızlı aç, `Ctrl+Shift+P` → Command Palette (en önemli shortcut!)
- `Ctrl+D` → kelimeyi seç + sonraki eşleşmeyi ekle (multi-cursor editing)
- `Ctrl+Shift+L` → tüm eşleşmeleri seç (toplu değiştirme)
- `Alt+Up/Down` → satır taşı, `Alt+Shift+Up/Down` → satır kopyala
- `F2` → rename symbol (tüm referansları güvenle yeniden adlandır)
- `F5` → debug başlat, `F9` → breakpoint, `F10` → step over, `F11` → step into
- Conditional Breakpoint: belirli koşulda dur (sağ tıkla → Add Conditional Breakpoint)
- Watch panel: ifadeleri sürekli izle (debug sırasında değişken takibi)
- Call Stack: fonksiyon çağrı zincirini gösterir (stack trace analizi)
- settings.json > GUI ayarlar (taşınabilir, versiyon kontrole alınabilir)
- `"editor.formatOnSave": true` + Prettier = otomatik kod formatlama
- pnpm: en hızlı + disk tasarrufu (2026 önerilen), npm: Node.js ile gelir (alternatif)
- Lock dosyasını (pnpm-lock.yaml / package-lock.json / yarn.lock) Git'e commit et
- Bir projede tek package manager kullan, karıştırma!
- Snippet'ler tekrar eden kodu hızlandırır: `Ctrl+Shift+P` → "Configure User Snippets"
:::

:::senior-learns
Bir Senior Developer VS Code ve geliştirici araçlarını şu seviyede kullanır:

1. **Keybinding'leri customize eder** - keybindings.json dosyasında kendi kısayollarını tanımlar. En sık kullandığı işlemler için hızlı erişim oluşturur. Vi/Vim keybindings kullanabilir (VSCodeVim extension).
2. **Debugging'i master eder** - `console.log` yerine her zaman debugger kullanır. Compound launch configuration ile frontend ve backend'i aynı anda debug eder. Remote debugging ile production-like ortamları inceler.
3. **Workspace'leri organize eder** - Multi-root workspace kullanarak ilgili projeleri tek pencerede açar. Her proje için ayrı `.vscode/settings.json` ile tutarlı kod stili sağlar. `extensions.json` ile takımın gerekli extension'larını tanımlar.
4. **Task runner'ları entegre eder** - tasks.json ile build, test, lint, deploy işlemlerini VS Code içinden çalıştırır. Problem matcher'lar ile hataları otomatik olarak editörde gösterir. Compound task'lar ile birden fazla görevi paralel çalıştırır.
5. **pnpm ve monorepo yönetir** - pnpm workspaces ile monorepo yapısı kurar. Shared package'lar oluşturur. Changeset veya Lerna ile versiyon yönetimi yapar. CI/CD pipeline'ında cache stratejileri uygular.
6. **DevContainer ve Remote Development kullanır** - `.devcontainer/devcontainer.json` ile tüm takım aynı geliştirme ortamında çalışır. Docker container içinde geliştirme yapar. SSH üzerinden uzak sunucularda kod yazar.

**Profesyonel Mindset:** "Araçlarını tanı, sınırlarını bil, ihtiyacın olmayanı yükleme. VS Code hafif başlar ama extension'larla ağırlaşır. Her extension bir maliyet: startup süresi, bellek, karmaşıklık. Sadece gerçekten kullandıklarını tut. Debugging ise en önemli yetkinliktir. console.log'la debug yapmak, stethoscope yerine kulağını göğse dayamak gibidir. Çalışır ama profesyonel değildir."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **IDE** (aɪ-diː-iː) → Integrated Development Environment / Tümleşik Geliştirme Ortamı
   *"VS Code is not technically an IDE, but with extensions it functions like one."*

2. **Breakpoint** (breɪk-pɔɪnt) → Durma Noktası
   *"Set a breakpoint on line 42 to inspect the variable values at that point."*

3. **Debugging** (diː-bʌɡ-ɪŋ) → Hata Ayıklama
   *"Effective debugging skills are more important than writing code fast."*

4. **Extension** (ɪk-sten-ʃən) → Eklenti
   *"Install the ESLint extension for automatic code quality checks."*

5. **Package Manager** (pæk-ɪdʒ mæn-ɪ-dʒər) → Paket Yöneticisi
   *"pnpm is the fastest package manager with the best disk space efficiency."*

**Okuma Egzersizi:** VS Code resmi dokümantasyonunu İngilizce oku: https://code.visualstudio.com/docs

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "VS Code debug ayarlarını yapılandırdım"
→ Örnek: `chore: configure VS Code debug settings`
:::

:::external-resource
- 📺 **Fireship:** "25 VS Code Productivity Tips" (12 dk, YouTube, ücretsiz)
- 📖 **VS Code Docs:** code.visualstudio.com/docs (resmi dokümantasyon)
- 📺 **James Q Quick:** "Debug JavaScript in VS Code" (YouTube, ücretsiz)
- 🎮 **VS Code Can Do That:** vscodecandothat.com (interaktif ipuçları)
- 📖 **pnpm Docs:** pnpm.io (resmi dokümantasyon)
:::
