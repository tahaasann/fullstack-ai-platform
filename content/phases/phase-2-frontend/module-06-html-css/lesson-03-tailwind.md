---
title: "Tailwind CSS, CSS Mimarisi ve Modern CSS"
id: "mod-06-css/lesson-03"
estimated_minutes: 50
order: 3
tags: ["tailwind", "css-architecture", "css-variables", "animations", "modern-css", "bem"]
prerequisites: ["mod-06-css/lesson-02"]
---

# Tailwind CSS, CSS Mimarisi ve Modern CSS

:::realworld
CSS yazmak kolaydır ama ölçeklenebilir CSS yazmak zordur. 10 sayfalık bir projede `.card`, `.card-title`, `.card-body` yazarsın, 100 sayfalık projede isimlendirme kabusu başlar. Tailwind CSS, utility-first yaklaşımıyla bu sorunu kökten çözer ve şu an endüstride en popüler CSS framework'üdür. Bu ders Tailwind'i derinlemesine öğretir, CSS Custom Properties, animasyonlar ve modern CSS özelliklerini kapsar. Ayrıca farklı CSS mimarilerini karşılaştırarak bilinçli tercih yapabilmeni sağlar.
:::

## Neden CSS Mimarisi Önemli?

Projelerde CSS'in büyümesiyle karşılaşılan sorunlar:

- **İsim çakışması:** İki farklı yerde `.title` sınıfı, biri diğerini ezer
- **Specificity savaşları:** `!important` kullanma ihtiyacı → bakım kabusu
- **Ölü kod:** Hangi CSS'in kullanıldığını bilemezsin
- **Yeniden kullanılabilirlik:** Aynı stil farklı yerlerde kopyalanır

:::deha-tip
Deha seviyesi developer'lar CSS'i "küçükken düzenli tut" prensibiyle yazar. 5 satırlık bir component bile doğru mimariyle yazılırsa, 5000 satıra büyüdüğünde hala yönetilebilir kalır. CSS mimarisi seçimi projenin ömrünü belirler.
:::

## Tailwind CSS

:::concept[Tailwind CSS (İng: Tailwind CSS)]
Tailwind CSS, önceden tanımlanmış utility sınıfları kullanarak HTML içinde doğrudan stil yazmayı sağlayan bir CSS framework'üdür.

**Türkçe karşılığı:** Tailwind CSS (özel isim)
**Ne işe yarar:** Custom CSS yazmadan, HTML'de sınıf isimleriyle hızlıca stil oluşturur
**Gerçek hayat benzetmesi:** LEGO gibi düşün - hazır parçaları birleştirerek istediğin yapıyı oluşturursun. Her parça tek bir iş yapar (renk, boyut, boşluk) ve birleştirerek karmaşık tasarımlar elde edersin.
:::

### Utility-First Felsefesi

:::code[html]{title="Geleneksel CSS vs Tailwind CSS"}
<!-- Geleneksel CSS -->
<div class="card">
  <h2 class="card-title">Başlık</h2>
  <p class="card-text">Açıklama</p>
  <button class="card-button">Detay</button>
</div>

<style>
.card { background: white; border-radius: 8px; padding: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.card-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 8px; }
.card-text { color: #6b7280; margin-bottom: 16px; }
.card-button { background: #3b82f6; color: white; padding: 8px 16px; border-radius: 4px; }
</style>

<!-- Tailwind CSS - Aynı sonuç -->
<div class="bg-white rounded-lg p-6 shadow-md">
  <h2 class="text-xl font-bold mb-2">Başlık</h2>
  <p class="text-gray-500 mb-4">Açıklama</p>
  <button class="bg-blue-500 text-white px-4 py-2 rounded">Detay</button>
</div>
<!-- Ayrı CSS dosyası yazmaya gerek yok! -->
:::

### Kurulum ve Konfigürasyon

:::code[bash]{title="Tailwind CSS Kurulumu"}
# 📌 2026: pnpm önerilen paket yöneticisi (daha hızlı, disk verimli)
# Vite + Tailwind (en yaygın kurulum)
pnpm create vite@latest my-project --template react-ts
cd my-project

# Tailwind v4 kurulumu (2025+)
pnpm install tailwindcss @tailwindcss/vite

# vite.config.js'e plugin ekle
:::

:::code[javascript]{title="vite.config.js"}
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
:::

:::code[css]{title="app.css - Tailwind Import"}
/* Tailwind v4: Tek satır import */
@import "tailwindcss";

/* Tailwind v3 (eski projeler): */
/* @tailwind base; */
/* @tailwind components; */
/* @tailwind utilities; */
:::

### Temel Utility Sınıfları

:::code[html]{title="Tailwind Utility Sınıfları Rehberi"}
<!-- SPACING: p (padding), m (margin) -->
<!-- Ölçek: 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8, 10, 12, 16, 20, 24 -->
<!-- 1 birim = 4px (0.25rem) -->
<div class="p-4">         <!-- padding: 16px (tüm yönler) -->
<div class="px-4 py-2">   <!-- padding: 8px 16px (yatay/dikey) -->
<div class="pt-2 pb-4">   <!-- padding-top: 8px, padding-bottom: 16px -->
<div class="m-auto">      <!-- margin: auto -->
<div class="mt-4 mb-8">   <!-- margin-top: 16px, margin-bottom: 32px -->
<div class="space-y-4">   <!-- Child elemanlar arası dikey 16px boşluk -->

<!-- TYPOGRAPHY -->
<p class="text-sm">       <!-- font-size: 0.875rem -->
<p class="text-base">     <!-- font-size: 1rem (varsayılan) -->
<p class="text-lg">       <!-- font-size: 1.125rem -->
<p class="text-xl">       <!-- font-size: 1.25rem -->
<p class="text-2xl">      <!-- font-size: 1.5rem -->
<p class="font-bold">     <!-- font-weight: 700 -->
<p class="font-semibold"> <!-- font-weight: 600 -->
<p class="leading-tight"> <!-- line-height: 1.25 -->
<p class="tracking-wide"> <!-- letter-spacing: 0.025em -->
<p class="text-center">   <!-- text-align: center -->
<p class="truncate">      <!-- overflow: hidden; text-overflow: ellipsis; white-space: nowrap -->

<!-- COLORS -->
<div class="text-gray-500">    <!-- Gri metin -->
<div class="bg-blue-500">      <!-- Mavi arka plan -->
<div class="border-red-300">   <!-- Kırmızı border -->
<!-- Ton ölçeği: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950 -->

<!-- LAYOUT -->
<div class="flex">              <!-- display: flex -->
<div class="grid grid-cols-3">  <!-- display: grid; 3 sütun -->
<div class="hidden">            <!-- display: none -->
<div class="block">             <!-- display: block -->
<div class="w-full">            <!-- width: 100% -->
<div class="h-screen">          <!-- height: 100vh -->
<div class="max-w-xl">          <!-- max-width: 36rem -->
<div class="min-h-screen">      <!-- min-height: 100vh -->

<!-- FLEXBOX -->
<div class="flex items-center justify-between gap-4">
<div class="flex-1">            <!-- flex: 1 1 0% -->
<div class="flex-shrink-0">     <!-- flex-shrink: 0 -->

<!-- BORDERS & EFFECTS -->
<div class="rounded-lg">        <!-- border-radius: 0.5rem -->
<div class="border border-gray-200"> <!-- 1px solid gri border -->
<div class="shadow-md">         <!-- orta gölge -->
<div class="opacity-50">        <!-- opacity: 0.5 -->
:::

### Responsive Prefixes

:::code[html]{title="Responsive Design ile Tailwind"}
<!-- Mobile-first: Prefix olmadan mobil, prefix ile büyük ekranlar -->
<div class="
  grid
  grid-cols-1        /* Mobil: 1 sütun */
  sm:grid-cols-2     /* ≥640px: 2 sütun */
  md:grid-cols-3     /* ≥768px: 3 sütun */
  lg:grid-cols-4     /* ≥1024px: 4 sütun */
  xl:grid-cols-5     /* ≥1280px: 5 sütun */
  2xl:grid-cols-6    /* ≥1536px: 6 sütun */
  gap-4
">
  <!-- Kartlar buraya -->
</div>

<!-- Responsive text -->
<h1 class="text-2xl md:text-4xl lg:text-6xl font-bold">
  Responsive Başlık
</h1>

<!-- Responsive padding -->
<section class="px-4 md:px-8 lg:px-16">
  <!-- İçerik -->
</section>

<!-- Responsive görünürlük -->
<div class="hidden md:block">  <!-- Mobilde gizle, tablet+ göster -->
<div class="md:hidden">        <!-- Tablet+ gizle, sadece mobilde göster -->
:::

### Dark Mode ve State Variants

:::code[html]{title="Dark Mode ve Hover/Focus States"}
<!-- Dark Mode -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <h2 class="text-gray-800 dark:text-gray-100">Başlık</h2>
  <p class="text-gray-600 dark:text-gray-400">Açıklama</p>
</div>

<!-- Hover, Focus, Active states -->
<button class="
  bg-blue-500
  hover:bg-blue-600
  focus:ring-2 focus:ring-blue-300 focus:outline-none
  active:bg-blue-700
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors duration-200
  text-white px-4 py-2 rounded-lg
">
  Tıkla
</button>

<!-- Group hover: Parent hover olunca child'ı değiştir -->
<div class="group p-4 hover:bg-gray-100 rounded-lg cursor-pointer">
  <h3 class="group-hover:text-blue-500 transition-colors">Başlık</h3>
  <p class="text-gray-500 group-hover:text-gray-700">Açıklama</p>
</div>

<!-- Peer: Sibling durumuna göre stil -->
<input type="email" class="peer" placeholder="Email">
<p class="hidden peer-invalid:block text-red-500 text-sm">
  Geçerli bir email girin
</p>

<!-- First, last, odd, even child -->
<ul>
  <li class="first:pt-0 last:pb-0 odd:bg-gray-50 even:bg-white py-2">
    Liste öğesi
  </li>
</ul>
:::

### Custom Theme ve @apply

:::code[css]{title="Tailwind Tema Özelleştirme ve @apply"}
/* tailwind.config.js veya CSS içinde tema özelleştirme */
/* Tailwind v4: CSS-native config */
@theme {
  --color-brand: #6366f1;
  --color-brand-light: #818cf8;
  --color-brand-dark: #4f46e5;
  --font-family-display: "Inter", sans-serif;
  --breakpoint-3xl: 1920px;
}

/* @apply ile tekrar eden utility gruplarını sınıfa çıkar */
/* DİKKAT: @apply'ı az kullan, çok kullanmak utility-first felsefesine aykırı */
.btn {
  @apply px-4 py-2 rounded-lg font-semibold transition-colors duration-200;
}

.btn-primary {
  @apply btn bg-blue-500 text-white hover:bg-blue-600;
}

.btn-secondary {
  @apply btn bg-gray-200 text-gray-800 hover:bg-gray-300;
}

/* Component extraction: React/Vue component tercih et */
/* @apply yerine component oluşturmak daha iyi bir yaklaşım */
:::

:::beginner-mistake
Yaygın hata: Her yerde `@apply` kullanmak. Bu, Tailwind'in avantajını yok eder ve tekrar geleneksel CSS'e dönersin. `@apply` sadece 3+ yerde tekrar eden ve component'a çıkaramayacağın kalıplar için kullan. Component-based framework (React, Vue) kullanıyorsan, component kendisi zaten soyutlama katmanıdır.
:::

## CSS Custom Properties (CSS Variables)

:::code[css]{title="CSS Custom Properties"}
/* Değişken tanımlama */
:root {
  /* Renkler */
  --color-primary: #3b82f6;
  --color-primary-dark: #2563eb;
  --color-text: #1f2937;
  --color-text-muted: #6b7280;
  --color-bg: #ffffff;
  --color-surface: #f9fafb;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'Fira Code', monospace;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 300ms ease;
}

/* Dark mode: Değişkenleri override et */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #f9fafb;
    --color-text-muted: #9ca3af;
    --color-bg: #111827;
    --color-surface: #1f2937;
    --color-primary: #60a5fa;
  }
}

/* Kullanım */
.card {
  background: var(--color-surface);
  color: var(--color-text);
  padding: var(--space-lg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  font-family: var(--font-sans);
  transition: box-shadow var(--transition-normal);
}

.card:hover {
  box-shadow: var(--shadow-md);
}

/* Fallback değer */
.element {
  color: var(--color-accent, #3b82f6);
  /* --color-accent tanımlı değilse #3b82f6 kullanılır */
}

/* Scoped variables: Belirli bir component için */
.alert {
  --alert-color: #ef4444;
  --alert-bg: #fef2f2;
  color: var(--alert-color);
  background: var(--alert-bg);
  padding: var(--space-md);
  border-left: 4px solid var(--alert-color);
}

.alert.success {
  --alert-color: #22c55e;
  --alert-bg: #f0fdf4;
}

.alert.warning {
  --alert-color: #f59e0b;
  --alert-bg: #fffbeb;
}
:::

:::concept[CSS Custom Properties (İng: CSS Custom Properties)]
CSS Custom Properties (CSS Variables), CSS içinde değişken tanımlayıp yeniden kullanmayı sağlayan native CSS özelliğidir.

**Türkçe karşılığı:** CSS Özel Özellikleri / CSS Değişkenleri
**Ne işe yarar:** Renk, boyut, spacing gibi değerleri tek yerden yönetir. Tema değişikliğini kolaylaştırır
**Gerçek hayat benzetmesi:** Bir restoranın tarif defteri - "1 ölçü tuz" dediğinde, ölçüyü değiştirince tüm tarifler güncellenir
:::

## CSS Animations ve Transitions

:::code[css]{title="CSS Transitions"}
/* Transition: Durum değişikliğinde yumuşak geçiş */
.button {
  background: #3b82f6;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  /* transition: property duration timing-function delay */
  transition: all 300ms ease;
  /* Daha spesifik (daha performanslı): */
  transition: background-color 200ms ease, transform 200ms ease, box-shadow 200ms ease;
}

.button:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.button:active {
  transform: translateY(0);
}

/* Timing functions */
.ease-in     { transition-timing-function: ease-in; }     /* Yavaş başla, hızlı bitir */
.ease-out    { transition-timing-function: ease-out; }    /* Hızlı başla, yavaş bitir */
.ease-in-out { transition-timing-function: ease-in-out; } /* Yavaş başla, yavaş bitir */
.linear      { transition-timing-function: linear; }       /* Sabit hız */
.custom      { transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55); } /* Bounce efekti */
:::

:::code[css]{title="CSS Keyframe Animations"}
/* @keyframes ile animasyon tanımla */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* Animasyonu uygula */
.fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

.spinner {
  animation: spin 1s linear infinite;
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}

/* Animasyon kısayol: name duration timing-function delay iteration-count direction fill-mode */
.complex-animation {
  animation: bounce 1s ease-in-out 0.5s infinite alternate both;
}

/* Birden fazla animasyon */
.multi-animate {
  animation:
    fadeIn 0.5s ease-out forwards,
    pulse 2s ease-in-out 1s infinite;
}
:::

:::tip
Animasyon performansı: Sadece `transform` ve `opacity` özelliklerini animate et. Bunlar GPU tarafından işlenir ve performanslıdır. `width`, `height`, `top`, `left`, `margin`, `padding` gibi özellikleri animate etmek layout recalculation tetikler ve performansı düşürür.
:::

## CSS Mimarisi Karşılaştırması

:::comparison
| Yaklaşım | Nasıl Çalışır | Avantajları | Dezavantajları | Ne Zaman Kullan |
|----------|--------------|-------------|----------------|-----------------|
| **BEM** | `.block__element--modifier` | Anlaşılır, isimlendirme standardı | Uzun sınıf adları, hala global CSS | Küçük-orta projeler, framework yok |
| **CSS Modules** | `.card { }` → `card_abc123` | Otomatik scope, çakışma yok | Build tool gerektirir, geleneksel CSS yazarsın | React/Vue projeleri |
| **Tailwind** | `class="px-4 py-2 bg-blue-500"` | Hızlı geliştirme, tutarlılık, küçük bundle | HTML kalabalık, öğrenme eğrisi | Her boyut proje, hızlı geliştirme |
| **styled-components** | CSS-in-JS template literals | JS ile dinamik stiller, tam scope | Runtime overhead, bundle size, SSR karmaşıklığı | Dinamik tema gerektiren React projeleri |
| **Vanilla Extract** | TypeScript ile CSS, zero-runtime | Type-safe, zero-runtime, tüm CSS özellikleri | Kurulum karmaşıklığı, TypeScript zorunlu | Büyük TypeScript projeleri |

**2025+ Trendi:** Tailwind + CSS Custom Properties kombinasyonu en popüler yaklaşım. CSS-in-JS (styled-components) popülerliğini kaybediyor, zero-runtime çözümler yükselişte.
:::

:::code[css]{title="BEM Örneği"}
/* BEM: Block__Element--Modifier */
.card { }
.card__title { }
.card__body { }
.card__button { }
.card__button--primary { }
.card__button--disabled { }

/* Kullanım */
/* <div class="card">
     <h2 class="card__title">Başlık</h2>
     <div class="card__body">İçerik</div>
     <button class="card__button card__button--primary">Tıkla</button>
   </div> */
:::

## Modern CSS Özellikleri

### CSS Nesting

:::code[css]{title="CSS Nesting (Native)"}
/* Artık Sass/Less'e gerek yok - native CSS nesting */
.card {
  background: white;
  padding: 24px;
  border-radius: 8px;

  /* Nested seçiciler */
  & .title {
    font-size: 1.25rem;
    font-weight: bold;
  }

  & .body {
    color: #6b7280;
    margin-top: 8px;
  }

  /* Hover state */
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  /* Media query nesting */
  @media (min-width: 768px) {
    padding: 32px;
  }
}
:::

### Subgrid

:::code[css]{title="CSS Subgrid"}
/* Parent grid'in çizgilerini child'a aktar */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.card {
  display: grid;
  /* Parent'ın satır çizgilerini kullan */
  grid-template-rows: subgrid;
  grid-row: span 3; /* 3 satır kapla: resim, başlık, buton */
}

/* Sonuç: Tüm kartların başlıkları ve butonları aynı hizada */
/* Subgrid olmadan: her kartın içerik yüksekliği farklı olunca hizalama bozulur */
:::

### Container Queries ve :has() (Detay)

:::code[css]{title="Container Queries ile Component Tasarımı"}
/* Container queries, component'ları bağlamdan bağımsız yapar */
.widget-container {
  container-type: inline-size;
  container-name: widget;
}

/* Widget dar alanda (sidebar) */
@container widget (max-width: 300px) {
  .widget {
    flex-direction: column;
    text-align: center;
  }
  .widget-icon { font-size: 2rem; }
}

/* Widget geniş alanda (ana içerik) */
@container widget (min-width: 301px) {
  .widget {
    flex-direction: row;
    align-items: center;
    gap: 16px;
  }
  .widget-icon { font-size: 1.5rem; }
}

/* :has() ile akıllı form stilleri */
.form-field {
  margin-bottom: 16px;

  /* İçinde focus olan input varken */
  &:has(input:focus) {
    .label { color: #3b82f6; }
    .border { border-color: #3b82f6; }
  }

  /* İçinde geçerli input varken */
  &:has(input:valid:not(:placeholder-shown)) {
    .icon-check { display: block; }
  }

  /* İçinde geçersiz input varken */
  &:has(input:invalid:not(:placeholder-shown)) {
    .error-message { display: block; }
    .label { color: #ef4444; }
  }
}
:::

:::beginner-mistake
Yaygın hata: Modern CSS özelliklerini tarayıcı desteğini kontrol etmeden kullanmak. Container queries, :has(), nesting gibi özellikler 2025+ modern tarayıcılarda desteklenir. Production'da kullanmadan önce caniuse.com'da kontrol et ve gerekirse @supports ile fallback yaz.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Tailwind ile Responsive Kart Grid (Kolay)

Tailwind CSS kullanarak responsive bir urun karti grid'i olustur.

```html
<!-- TODO: Tailwind class'lari ile tamamla -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
  <!-- Kart 1 -->
  <div class="bg-gray-800 rounded-lg overflow-hidden shadow-lg">
    <img src="https://via.placeholder.com/400x200" class="w-full h-48 object-cover" alt="Urun" />
    <div class="p-6">
      <h3 class="text-xl font-bold text-white">Urun Adi</h3>
      <p class="text-gray-400 mt-2">Kisa aciklama metni.</p>
      <div class="flex items-center justify-between mt-4">
        <span class="text-2xl font-bold text-emerald-400">₺1,299</span>
        <!-- TODO: Hover efektli buton ekle -->
        <!-- bg-emerald-600 hover:bg-emerald-700 transition text-white px-4 py-2 rounded-lg -->
      </div>
    </div>
  </div>
  <!-- TODO: 2 kart daha ekle, farkli urun bilgileriyle -->
</div>
```

**Beklenen Sonuc:** Mobilde 1 sutun, tablette 2, masaustunde 3 sutun gorunmeli. Buton hover'da renk degistirmeli.
**Ipucu:** `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` mobile-first responsive pattern'dir.

---

### Alistirma 2: Dark Mode Toggle Sistemi (Orta)

Tailwind dark mode ve localStorage ile kalici tema degisimi olustur.

```html
<!-- tailwind.config.js'te darkMode: 'class' ayarla -->
<div class="bg-white dark:bg-gray-900 min-h-screen transition-colors">
  <button id="theme-toggle" class="fixed top-4 right-4 p-2 rounded-lg bg-gray-200 dark:bg-gray-700">
    <span class="dark:hidden">🌙</span>
    <span class="hidden dark:inline">☀️</span>
  </button>

  <div class="max-w-md mx-auto mt-20 p-6 rounded-xl bg-gray-100 dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700">
    <h2 class="text-xl font-bold text-gray-900 dark:text-white">Dark Mode Karti</h2>
    <p class="mt-2 text-gray-600 dark:text-gray-400">Light ve dark modda farkli gorunur.</p>
    <!-- TODO: dark mode destekli input ve badge elementleri ekle -->
  </div>
</div>

<script>
// TODO: Toggle logic:
// 1. document.documentElement.classList.toggle('dark')
// 2. localStorage'a kaydet
// 3. Sayfa yuklendiginde localStorage'dan oku
// 4. prefers-color-scheme ile sistem tercihini kontrol et
</script>
```

**Beklenen Sonuc:** Toggle ile tum sayfa tema degistirmeli. Tercih localStorage'da saklanip sayfa yenilendiginde korunmali.
**Ipucu:** `document.documentElement.classList.toggle('dark')` ile html'e dark class'i ekle/cikar.

---

### Alistirma 3: CSS Animation ve Group Hover Pattern (Zor)

Tailwind animation, group hover ve custom keyframes ile interaktif UI elementleri olustur.

```html
<style>
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

<!-- GOREV 1: Loading Skeleton -->
<div class="max-w-sm p-4 space-y-4">
  <!-- TODO: animate-pulse ile skeleton satirlari olustur -->
  <!-- h-6 w-3/4 rounded bg-gray-700 animate-pulse -->
  <!-- h-4 w-full rounded bg-gray-700 animate-pulse (3 satir) -->
  <!-- h-48 w-full rounded bg-gray-700 animate-pulse (resim placeholder) -->
</div>

<!-- GOREV 2: Hover Overlay Karti -->
<div class="group cursor-pointer max-w-sm">
  <div class="relative overflow-hidden rounded-xl transition-all duration-300 group-hover:shadow-2xl group-hover:-translate-y-1">
    <img src="https://via.placeholder.com/400x250" class="w-full" alt="Proje">
    <!-- TODO: Hover'da gorunen overlay -->
    <!-- absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity -->
    <!-- Overlay icinde ortalanmis "Detaylari Gor" butonu -->
    <div class="p-4 bg-gray-800">
      <h3 class="font-bold text-white group-hover:text-emerald-400 transition-colors">Proje Adi</h3>
    </div>
  </div>
</div>

<!-- GOREV 3: Animated Toast Notification -->
<!-- TODO: fixed bottom-4 right-4, fadeInUp animasyonu, kapatma butonu -->
```

**Beklenen Sonuc:** Skeleton pulsing animasyonu calismali. Kart hover'inda overlay ve golge gorunmeli. Toast asagidan yukari kayarak gelmeli. Tum gecisler smooth olmali.
**Ipucu:** `group` parent'a, `group-hover:` child'a eklenir. `transition-all duration-300` ile animasyonlu gecis saglanir.
:::

:::knowledge-check
type: multiple_choice
question: "Tailwind CSS'te 'md:flex-row' ne anlama gelir?"
options:
  - "Orta büyüklükteki elemanları flex-row yapar"
  - "768px ve üzeri ekranlarda flex-direction: row uygular"
  - "Markdown formatında flex-row uygular"
  - "Medium dark modda flex-row uygular"
correct: 1
explanation: "md: prefix'i min-width: 768px media query'sine karşılık gelir. Mobile-first yaklaşımla, 768px ve üzeri ekranlarda flex-direction: row uygulanır. Varsayılan (mobil) stil prefix olmadan yazılır."
:::

:::knowledge-check
type: multiple_choice
question: "CSS animasyonlarında hangisi GPU ile hızlandırılır ve performanslıdır?"
options:
  - "width ve height"
  - "margin ve padding"
  - "transform ve opacity"
  - "top ve left"
correct: 2
explanation: "transform ve opacity GPU tarafından compositor thread'inde işlenir ve layout recalculation tetiklemez. Bu yüzden en performanslı animasyon özellikleridir. width, height, margin, padding, top, left gibi özellikler layout'u değiştirir ve reflow'a neden olur."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "Tailwind CSS'in utility-first yaklasimini BEM ve CSS Modules ile karsilastir. Her yaklasimin specificity yonetimi, bundle size, developer experience ve takim olceklenmesi acisindan avantaj ve dezavantajlarini tablo halinde goster. Neden 2025'te Tailwind endüstri standardi oldu?"

**2. Pratik Uygulama:**
> "Tailwind CSS ile dark mode destekli bir pricing card component'i olustur. 3 plan (Basic, Pro, Enterprise) olsun. Hover efektleri, group-hover ile icerik degisimi, responsive tasarim (mobilde tek sutun, desktopte yan yana) ve animasyonlar icersin. Her utility class'in ne yaptigini acikla."
> Takip: "Bu component'i @apply kullanmadan React component'ine donustur ve neden @apply yerine component abstraction tercih ettigini acikla."

**3. Mukemmellik Icin:**
> "Buyuk bir SaaS projesinde Tailwind CSS ile design token sistemi kuruyorum. CSS Custom Properties ile renk, spacing ve typography token'larini tanimla, Tailwind theme'e entegre et ve dark/light mode arasinda gecis yapan bir sistem tasarla. Figma token'lariyla senkronizasyonu nasil saglarim?"

### Pair Programming Ipucu
Tailwind class'larini yazarken AI'a UI screenshot veya Figma tasarimini goster ve sor: "Bu tasarimi Tailwind utility class'lariyla implement et. Responsive breakpoint'leri, dark mode varyantlarini ve hover state'lerini dahil et."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Utility-first CSS yaklasiminin avantaj ve dezavantajlari nelerdir?**
- **Junior cevabi:** Avantaji hizli yazilmasi, dezavantaji HTML'in karisik gorunmesi.
- **Senior cevabi:** Avantajlar: dead CSS problemi ortadan kalkar (sadece kullanilan class'lar bundle'a girer), naming fatigue yoktur (class ismi dusunmeye gerek yok), design system token'lari enforce edilir (spacing, color scale tutarli olur), responsive ve dark mode kolaydir. Dezavantajlar: ogrenme egrisi vardir, uzun class listeleri okunabilirlik sorununa yol acar (ama @apply veya component extraction ile cozulur). Trade-off: geleneksel CSS'te stil dosyasi buyur ama HTML temiz kalir; Tailwind'de HTML karisir ama CSS dosyasi minimal olur. Buyuk projelerde Tailwind PurgeCSS ile production bundle'i 10KB'in altinda kalir.

**Soru 2: Tailwind'de responsive tasarim nasil yapilir?**
- **Junior cevabi:** sm:, md:, lg: gibi prefix'ler kullanilir.
- **Senior cevabi:** Tailwind mobile-first yaklasimi benimser: prefix'siz class'lar tum ekranlarda gecerlidir, sm: (640px+), md: (768px+), lg: (1024px+), xl: (1280px+) buyuyen ekranlara uygulanir. Ornegin `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3` mobilde tek sutun, tablette 2, desktop'ta 3 sutun olusturur. Container query'ler (@container) ile parent boyutuna gore responsive tasarim yapilabilir. Custom breakpoint'ler tailwind.config.js'te tanimlanir. Responsive debugging icin dev tools'un device emulation'i kullanilir.
:::

:::must-note
- Tailwind CSS utility-first yaklaşım: HTML'de sınıflarla stil yazarsın, ayrı CSS dosyası gerekmez
- Tailwind spacing: 1 birim = 4px (p-4 = 16px, m-8 = 32px)
- Responsive prefixes: sm: (640px), md: (768px), lg: (1024px), xl: (1280px), 2xl: (1536px)
- Dark mode: dark: prefix (dark:bg-gray-900, dark:text-white)
- State variants: hover:, focus:, active:, disabled:, group-hover:, peer-invalid:
- @apply: Tekrar eden utility gruplarını CSS sınıfına çıkar (az kullan)
- CSS Custom Properties: --degisken-adi: deger; kullanım: var(--degisken-adi)
- Dark mode değişkenleri: @media (prefers-color-scheme: dark) ile override et
- Animasyonlarda sadece transform ve opacity kullan (GPU-accelerated, performanslı)
- @keyframes: Animasyon tanımla, animation: ile uygula
- Transition: Durum değişikliğinde yumuşak geçiş (hover, focus, active)
- BEM: .block__element--modifier (isim standardı, global scope)
- CSS Modules: Otomatik scope, React/Vue ile popüler
- Tailwind 2025+ en popüler CSS yaklaşımı, CSS-in-JS popülerliğini kaybediyor
- CSS Nesting: Native & ile iç içe seçiciler (Sass'a gerek yok)
- Subgrid: Parent grid çizgilerini child'a aktarır (kart hizalama için kritik)
- Container queries: Parent boyutuna göre responsive (viewport yerine)
- :has(): Parent selector, "içinde X olan Y" seçimi
:::

:::senior-learns
Bir Senior Developer, CSS mimarisi ve Tailwind konusunda şu yaklaşımı benimser:

1. **Design token sistemi kurar** - Renk, spacing, typography, shadow gibi değerleri CSS Custom Properties veya Tailwind theme olarak tanımlar. Figma'daki design token'lar ile kod tarafındaki token'lar senkronize olur. Style Dictionary veya benzeri araçlarla otomatize eder.
2. **Tailwind'i component abstraction ile kullanır** - Uzun utility chain'lerini React/Vue component'larına soyutlar. `@apply` yerine component composition tercih eder. Headless UI veya Radix UI gibi unstyled component kütüphaneleriyle birlikte kullanır.
3. **CSS performansını ölçer** - Chrome DevTools Performance tab'ında layout shift, paint ve composite sürelerini analiz eder. `content-visibility: auto` ile off-screen rendering'i optimize eder. `will-change` ile animasyon performansını artırır ama gereksiz kullanımından kaçınır.
4. **Progressive enhancement uygular** - `@supports` ile modern CSS özelliklerinin varlığını kontrol eder. Fallback stiller sağlar. Core deneyim her tarayıcıda çalışır, modern tarayıcılarda zenginleştirilmiş deneyim sunar.
5. **CSS bundle size'ı optimize eder** - Tailwind'in purge mekanizmasıyla kullanılmayan utility'leri siler. Code splitting ile sayfa bazlı CSS yükler. Critical CSS'i inline eder.
6. **CSS-in-JS'ten uzaklaşır** - Runtime CSS-in-JS (styled-components, emotion) yerine zero-runtime alternatifler (Vanilla Extract, Panda CSS) veya Tailwind tercih eder. Server Components ve streaming SSR ile uyumluluk sorunlarını önceden düşünür.

**Profesyonel Mindset:** "CSS mimarisi seçimi, projenin ölçeğine, takım büyüklüğüne ve teknoloji stack'ine bağlıdır. 3 kişilik bir takımda Tailwind mükemmel çalışır. 30 kişilik bir takımda design token sistemi ve strict component library şarttır. Doğru araç, doğru bağlamda kullanılan araçtır."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Utility-first** (juː-tɪl-ɪ-ti fɜːrst) → Yardımcı sınıf öncelikli
   *"Tailwind's utility-first approach eliminates the need for custom CSS classes."*

2. **Design token** (dɪ-zaɪn toʊ-kən) → Tasarım jetonu/değişkeni
   *"We store all design tokens as CSS custom properties for consistent theming."*

3. **Animation** (æn-ɪ-meɪ-ʃən) → Animasyon
   *"CSS animations using transform and opacity are GPU-accelerated."*

4. **Specificity** (spes-ɪ-fɪs-ɪ-ti) → Özgüllük/Seçicilik ağırlığı
   *"Tailwind avoids specificity wars by using single-class utility selectors."*

5. **Purge** (pɜːrdʒ) → Temizleme/Arındırma
   *"Tailwind purges unused CSS classes to minimize the final bundle size."*

**Okuma Egzersizi:** Tailwind CSS resmi dokümanını İngilizce oku: https://tailwindcss.com/docs

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Tailwind CSS konfigürasyonunu ve dark mode desteğini ekledim"
→ Örnek: `feat: configure Tailwind CSS with custom theme and dark mode support`
:::

:::external-resource
- 📖 **Tailwind CSS Docs:** tailwindcss.com/docs (resmi doküman, ücretsiz)
- 📺 **Tailwind Labs:** YouTube kanalı (resmi videolar, ücretsiz)
- 🎮 **Tailwind Play:** play.tailwindcss.com (online deneme alanı, ücretsiz)
- 📖 **Every Layout:** every-layout.dev (modern CSS layout kalıpları)
- 📖 **Modern CSS:** moderncss.dev (modern CSS teknikleri, ücretsiz)
- 🔧 **Can I Use:** caniuse.com (tarayıcı destek tablosu, ücretsiz)
:::
