---
title: "CSS Layout: Box Model, Flexbox ve Grid"
id: "mod-06-css/lesson-02"
estimated_minutes: 55
order: 2
tags: ["css", "flexbox", "grid", "responsive", "box-model", "layout"]
prerequisites: ["mod-06-css/lesson-01"]
---

# CSS Layout: Box Model, Flexbox ve Grid

:::realworld
Modern web sayfalarının %90'ından fazlası Flexbox ve/veya CSS Grid kullanır. Bir dashboard tasarla, bir e-ticaret ürün listesi oluştur, bir blog layoutu kur - hepsinde bu iki layout sistemi karşına çıkar. Bu ders, Box Model'den başlayarak Flexbox ve Grid'i "deha seviyesinde" öğretir. Dersin sonunda herhangi bir tasarımı bakıp "bunu Flexbox mı Grid mi ile yapmalıyım?" sorusuna anında cevap verebileceksin.
:::

## Neden Layout Sistemlerini Derinlemesine Öğrenmelisin?

Layout CSS'in en temel yapı taşıdır. Bir developer olarak her gün layout yazarsın:

- **Navbar** düzeni → Flexbox
- **Ürün kartları** grid'i → CSS Grid
- **Form** hizalaması → Flexbox
- **Dashboard** panelleri → CSS Grid
- **Footer** linkleri → Flexbox

:::deha-tip
Deha seviyesi developer'lar her layout sorununda float veya position hack'lerine başvurmaz. Doğru aracı seçer: tek boyutlu hizalama için Flexbox, iki boyutlu grid yapıları için CSS Grid. Bu ders, bu seçimi bilinçli yapabilmeni sağlar.
:::

## Box Model

:::concept[Box Model (İng: Box Model)]
CSS Box Model, her HTML elemanının etrafındaki alanı tanımlayan dört katmanlı bir modeldir: content, padding, border, margin.

**Türkçe karşılığı:** Kutu Modeli
**Ne işe yarar:** Her elemanın boyutunu ve elemanlar arası mesafeyi kontrol eder
**Gerçek hayat benzetmesi:** Bir hediye paketi gibi - hediye (content), sünger koruma (padding), kutu (border), kutular arası boşluk (margin)
:::

:::code[css]{title="Box Model Temelleri"}
/* Varsayılan: content-box (genişlik sadece content'i kapsar) */
.box-default {
  width: 200px;
  padding: 20px;
  border: 5px solid black;
  margin: 10px;
  /* Toplam genişlik: 200 + 20*2 + 5*2 = 250px */
  /* Toplam kaplanan alan: 250 + 10*2 = 270px */
}

/* border-box: genişlik padding + border dahil */
.box-border {
  box-sizing: border-box;
  width: 200px;
  padding: 20px;
  border: 5px solid black;
  margin: 10px;
  /* Toplam genişlik: 200px (padding ve border dahil!) */
  /* Content alanı: 200 - 20*2 - 5*2 = 150px */
}

/* Global reset: Her projede bunu yap */
*, *::before, *::after {
  box-sizing: border-box;
}
:::

:::beginner-mistake
Yaygın hata: `box-sizing: border-box` resetini yapmamak. Varsayılan `content-box` modunda `width: 100%` verdiğin bir eleman padding ve border eklediğinde container'ından taşar. Her projenin başına `*, *::before, *::after { box-sizing: border-box; }` eklemeyi unutma!
:::

### Margin Collapse

:::code[css]{title="Margin Collapse Davranışı"}
/* Dikey margin'ler birleşir (collapse) */
.box-a { margin-bottom: 30px; }
.box-b { margin-top: 20px; }
/* Aralarındaki mesafe: 30px (büyük olan kazanır, 30+20=50 DEĞİL) */

/* Margin collapse'ı engelleyen durumlar: */
/* 1. Flexbox veya Grid container içindeki elemanlar */
/* 2. float edilmiş elemanlar */
/* 3. position: absolute veya fixed elemanlar */
/* 4. overflow: hidden/auto olan parent */
:::

## Flexbox

:::concept[Flexbox (İng: Flexible Box Layout)]
Flexbox, tek boyutlu (yatay VEYA dikey) layout oluşturmak için tasarlanmış CSS modülüdür.

**Türkçe karşılığı:** Esnek Kutu Düzeni
**Ne işe yarar:** Elemanları bir satır veya sütun boyunca hizalar ve aralarında boşluk dağıtır
**Gerçek hayat benzetmesi:** Bir rafta kitapları dizme gibi - kitapları sola yasla, ortala, aralarına eşit boşluk koy, sığmazsa alt rafa geç
:::

### Container (Parent) Özellikleri

:::code[css]{title="Flexbox Container Özellikleri"}
.flex-container {
  display: flex; /* Flexbox'ı aktifleştir */

  /* Ana eksen yönü */
  flex-direction: row;            /* ← Varsayılan: soldan sağa */
  flex-direction: row-reverse;    /* Sağdan sola */
  flex-direction: column;         /* Yukarıdan aşağı */
  flex-direction: column-reverse; /* Aşağıdan yukarı */

  /* Satır sarmalaması */
  flex-wrap: nowrap;  /* Varsayılan: tek satır (taşar) */
  flex-wrap: wrap;    /* Sığmazsa alt satıra geç */

  /* Ana eksen hizalaması (justify-content) */
  justify-content: flex-start;    /* Sola yasla (varsayılan) */
  justify-content: flex-end;      /* Sağa yasla */
  justify-content: center;        /* Ortala */
  justify-content: space-between; /* İlk ve son kenarda, aralar eşit */
  justify-content: space-around;  /* Her elemanın etrafında eşit boşluk */
  justify-content: space-evenly;  /* Tüm boşluklar tamamen eşit */

  /* Çapraz eksen hizalaması (align-items) */
  align-items: stretch;    /* Varsayılan: container yüksekliğine uzan */
  align-items: flex-start; /* Üste yasla */
  align-items: flex-end;   /* Alta yasla */
  align-items: center;     /* Dikey ortala */
  align-items: baseline;   /* Metin tabanına göre hizala */

  /* Birden fazla satır varken çapraz eksen hizalama */
  align-content: flex-start;
  align-content: center;
  align-content: space-between;

  /* Elemanlar arası boşluk */
  gap: 16px;        /* Satır ve sütun gap'i aynı */
  gap: 16px 24px;   /* Satır gap: 16px, Sütun gap: 24px */
  row-gap: 16px;
  column-gap: 24px;
}
:::

### Item (Child) Özellikleri

:::code[css]{title="Flexbox Item Özellikleri"}
.flex-item {
  /* flex-grow: Kalan alanı paylaşma oranı */
  flex-grow: 0;  /* Varsayılan: büyümez */
  flex-grow: 1;  /* Kalan alanı eşit paylaş */
  flex-grow: 2;  /* Diğerlerinin 2 katı kadar büyü */

  /* flex-shrink: Sığmadığında küçülme oranı */
  flex-shrink: 1;  /* Varsayılan: küçülür */
  flex-shrink: 0;  /* Küçülmez (minimum genişliğini korur) */

  /* flex-basis: Başlangıç boyutu */
  flex-basis: auto;   /* Varsayılan: içeriğe göre */
  flex-basis: 200px;  /* 200px başlangıç genişliği */
  flex-basis: 25%;    /* Container'ın %25'i */

  /* Kısayol: flex: grow shrink basis */
  flex: 0 1 auto;  /* Varsayılan */
  flex: 1;         /* flex: 1 1 0% (eşit genişlik paylaşımı) */
  flex: none;      /* flex: 0 0 auto (sabit boyut) */

  /* Tek item için çapraz eksen hizalama */
  align-self: auto;       /* Parent'ın align-items'ını kullan */
  align-self: center;     /* Sadece bu item'ı dikey ortala */
  align-self: flex-start;
  align-self: flex-end;
  align-self: stretch;

  /* Sıralama */
  order: 0;  /* Varsayılan */
  order: -1; /* En başa taşı */
  order: 1;  /* Sona taşı */
}
:::

### Flexbox Layout Kalıpları

:::code[css]{title="Yaygın Flexbox Kalıpları"}
/* 1. Navbar: Logo solda, linkler sağda */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

/* 2. Kartları ortala */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

/* 3. Sticky footer: Footer her zaman altta */
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.page > main {
  flex: 1; /* Kalan alanı kapla */
}

/* 4. Tam ortala (yatay + dikey) */
.center-everything {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

/* 5. Eşit genişlikte sütunlar */
.equal-columns {
  display: flex;
  gap: 16px;
}
.equal-columns > * {
  flex: 1;
}

/* 6. Sidebar + Content */
.layout {
  display: flex;
  gap: 24px;
}
.sidebar {
  flex: 0 0 250px; /* Sabit 250px, küçülmez */
}
.content {
  flex: 1; /* Kalan alanı kapla */
}
:::

## CSS Grid

:::concept[CSS Grid (İng: CSS Grid Layout)]
CSS Grid, iki boyutlu (satır VE sütun) layout oluşturmak için tasarlanmış CSS modülüdür.

**Türkçe karşılığı:** CSS Izgara Düzeni
**Ne işe yarar:** Satır ve sütunları aynı anda kontrol eder, karmaşık sayfa düzenleri oluşturur
**Gerçek hayat benzetmesi:** Bir Excel tablosu gibi - satır ve sütunlardan oluşan hücreler, hücreler birleştirilebilir, boyutlandırılabilir
:::

### Grid Container Özellikleri

:::code[css]{title="CSS Grid Container"}
.grid-container {
  display: grid;

  /* Sütun tanımları */
  grid-template-columns: 200px 1fr 200px;        /* 3 sütun */
  grid-template-columns: repeat(3, 1fr);           /* 3 eşit sütun */
  grid-template-columns: repeat(4, minmax(200px, 1fr)); /* Min 200px, max 1fr */

  /* auto-fill vs auto-fit */
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  /* auto-fill: Boş sütunlar için yer ayırır */
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  /* auto-fit: Boş sütunları daraltır, mevcutlar genişler */

  /* Satır tanımları */
  grid-template-rows: 80px 1fr auto;  /* 3 satır */
  grid-auto-rows: minmax(100px, auto); /* Otomatik satır yüksekliği */

  /* Gap (boşluk) */
  gap: 16px;
  gap: 16px 24px; /* row-gap column-gap */

  /* Template Areas */
  grid-template-areas:
    "header  header  header"
    "sidebar content content"
    "footer  footer  footer";

  /* Named lines */
  grid-template-columns: [sidebar-start] 250px [sidebar-end content-start] 1fr [content-end];
}
:::

### Grid Template Areas

:::code[css]{title="Grid Template Areas ile Sayfa Düzeni"}
.page-layout {
  display: grid;
  grid-template-areas:
    "header  header  header"
    "sidebar content content"
    "footer  footer  footer";
  grid-template-columns: 250px 1fr 1fr;
  grid-template-rows: 80px 1fr 60px;
  min-height: 100vh;
  gap: 0;
}

.page-header  { grid-area: header; }
.page-sidebar { grid-area: sidebar; }
.page-content { grid-area: content; }
.page-footer  { grid-area: footer; }

/* Responsive: Mobilde sidebar altına al */
@media (max-width: 768px) {
  .page-layout {
    grid-template-areas:
      "header"
      "content"
      "sidebar"
      "footer";
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto auto;
  }
}
:::

### Grid Item Özellikleri

:::code[css]{title="Grid Item Yerleştirme"}
.grid-item {
  /* Satır ve sütun pozisyonu */
  grid-column: 1 / 3;      /* 1. çizgiden 3. çizgiye kadar (2 sütun kapla) */
  grid-column: span 2;     /* 2 sütun kapla */
  grid-row: 1 / 4;         /* 3 satır kapla */

  /* Kısayol */
  grid-area: 1 / 1 / 3 / 4; /* row-start / col-start / row-end / col-end */

  /* Hücre içi hizalama */
  justify-self: start | end | center | stretch;  /* Yatay */
  align-self: start | end | center | stretch;    /* Dikey */
  place-self: center;  /* Her iki eksen */
}

/* Container seviyesinde tüm item'ları hizala */
.grid-container {
  justify-items: center;  /* Tüm item'ları yatay ortala */
  align-items: center;    /* Tüm item'ları dikey ortala */
  place-items: center;    /* İkisi birden */
}
:::

### Grid Layout Kalıpları

:::code[css]{title="Yaygın Grid Kalıpları"}
/* 1. Responsive kart grid'i */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

/* 2. Holy Grail Layout */
.holy-grail {
  display: grid;
  grid-template: auto 1fr auto / auto 1fr auto;
  min-height: 100vh;
}

/* 3. Masonry-benzeri layout (farklı yükseklikler) */
.masonry {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 10px;
  gap: 16px;
}
.masonry-item-small  { grid-row: span 15; }
.masonry-item-medium { grid-row: span 25; }
.masonry-item-large  { grid-row: span 35; }

/* 4. 12-sütunlu grid sistemi */
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 16px;
}
.col-6  { grid-column: span 6; }
.col-4  { grid-column: span 4; }
.col-3  { grid-column: span 3; }
.col-12 { grid-column: span 12; }

/* 5. Dashboard layout */
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(150px, auto);
  gap: 16px;
}
.widget-wide { grid-column: span 2; }
.widget-tall { grid-row: span 2; }
.widget-full { grid-column: 1 / -1; } /* Tüm sütunları kapla */
:::

## Responsive Design

:::concept[Responsive Design (İng: Responsive Design)]
Responsive Design, web sayfasının farklı ekran boyutlarına (mobil, tablet, desktop) otomatik olarak uyum sağlamasıdır.

**Türkçe karşılığı:** Duyarlı Tasarım
**Ne işe yarar:** Aynı HTML ile tüm cihazlarda iyi görünen sayfalar oluşturur
**Gerçek hayat benzetmesi:** Su gibi düşün - hangi kaba koyarsan onun şeklini alır
:::

### Media Queries ve Mobile-First

:::code[css]{title="Mobile-First Media Queries"}
/* Mobile-First: Önce mobil stil yaz, sonra büyük ekranlar için genişlet */

/* Taban: Mobil stiller (varsayılan) */
.container {
  padding: 16px;
  font-size: 16px;
}

.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* Tablet (768px ve üzeri) */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    max-width: 768px;
    margin: 0 auto;
  }

  .card-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* Desktop (1024px ve üzeri) */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
  }

  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Büyük ekran (1440px ve üzeri) */
@media (min-width: 1440px) {
  .container {
    max-width: 1400px;
  }

  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
:::

:::beginner-mistake
Yaygın hata: Desktop-first yaklaşım kullanmak (`max-width` ile). Mobile-first (`min-width`) yaklaşımı tercih et çünkü: 1) Mobil CSS daha basittir (tek sütun, az dekorasyon), 2) Tarayıcı gereksiz CSS'i indirmez, 3) Google mobile-first indexing kullanır.
:::

### Fluid Typography ve clamp()

:::code[css]{title="Fluid Typography"}
/* Sabit breakpoint'ler yerine akıcı tipografi */

/* Eski yöntem: Her breakpoint'te ayrı font-size */
h1 { font-size: 24px; }
@media (min-width: 768px) { h1 { font-size: 36px; } }
@media (min-width: 1024px) { h1 { font-size: 48px; } }

/* Modern yöntem: clamp() ile akıcı tipografi */
h1 {
  /* clamp(minimum, tercih edilen, maksimum) */
  font-size: clamp(1.5rem, 4vw, 3rem);
  /* 1.5rem (24px) altına düşmez */
  /* Viewport genişliğinin %4'ü kadar */
  /* 3rem (48px) üstüne çıkmaz */
}

p {
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  line-height: 1.6;
}

/* Fluid spacing */
.section {
  padding: clamp(1rem, 5vw, 4rem);
  margin-bottom: clamp(2rem, 8vw, 6rem);
}

/* Container genişliği */
.container {
  width: min(90%, 1200px);
  /* Ekranın %90'ı veya 1200px, hangisi küçükse */
  margin-inline: auto;
}
:::

### Container Queries

:::code[css]{title="Container Queries"}
/* Container query: Parent boyutuna göre stil değiştir */
/* Media query viewport'a bakar, container query parent'a bakar */

.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Container 400px'den geniş olduğunda */
@container card (min-width: 400px) {
  .card {
    display: flex;
    flex-direction: row;
    gap: 16px;
  }

  .card-image {
    width: 40%;
  }

  .card-content {
    width: 60%;
  }
}

/* Container 400px'den dar olduğunda (varsayılan) */
.card {
  display: flex;
  flex-direction: column;
}

.card-image {
  width: 100%;
}
:::

### :has() Selector

:::code[css]{title=":has() Selector - Parent Selector"}
/* :has() ile parent'ı child'a göre seç */

/* İçinde resim olan card'a farklı stil */
.card:has(img) {
  padding: 0;
}

.card:has(img) .card-content {
  padding: 16px;
}

/* İçinde hata mesajı olan form grubuna kırmızı border */
.form-group:has(.error) {
  border-color: red;
}

.form-group:has(.error) label {
  color: red;
}

/* Checkbox seçiliyken yanındaki label'ı yeşil yap */
label:has(input:checked) {
  color: green;
  font-weight: bold;
}

/* Boş input'u olan form'a uyarı stili */
form:has(input:placeholder-shown) .submit-btn {
  opacity: 0.5;
  cursor: not-allowed;
}
:::

## Flexbox vs Grid: Ne Zaman Hangisi?

:::comparison
| Kriter | Flexbox | CSS Grid |
|--------|---------|----------|
| Boyut | **Tek boyut** (satır VEYA sütun) | **İki boyut** (satır VE sütun) |
| Yaklaşım | İçerikten dışarı (content-out) | Dışarıdan içeriye (layout-in) |
| Hizalama | Tek eksen boyunca güçlü | İki eksen boyunca güçlü |
| Kullanım | Navbar, buton grupları, form satırları | Sayfa düzeni, dashboard, kart grid'leri |
| Boyutlandırma | İçeriğe göre esner | Tanımlanan grid yapısına uyar |
| Template areas | Yok | Var (grid-template-areas) |
| Named lines | Yok | Var |
| Örtüşme (overlap) | Zor (position gerekir) | Kolay (aynı hücreye yerleştir) |

**Pratik Kurallar:**
- **Tek satır/sütundaki hizalama** → Flexbox
- **Navbar, footer, buton grupları** → Flexbox
- **2D grid yapısı** → CSS Grid
- **Sayfa iskelet yapısı** → CSS Grid
- **Responsive kart listesi** → CSS Grid (`auto-fit`/`auto-fill`)
- **Dikey ve yatay ortalama** → Her ikisi de, ama Flexbox daha basit
- **Karmaşık dashboard** → CSS Grid (template areas ile)
- **İkisi birlikte** → Grid sayfa düzeninde, Flexbox component içinde
:::

:::tip
Flexbox ve Grid birbirinin alternatifi değil, tamamlayıcısıdır. Sayfa düzenini Grid ile kur (header, sidebar, content, footer), her bölümün içindeki elemanları Flexbox ile hizala. Bu "Grid for layout, Flexbox for alignment" yaklaşımı en yaygın ve en iyi pratiktir.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Flexbox ile Navbar ve Kart Layout (Kolay)

Flexbox kullanarak responsive bir navbar ve yatay kart dizilimi oluştur.

```html
<style>
/* TODO: Asagidaki CSS'i tamamla */

/* Navbar: logo solda, menu ortada, buton sagda */
.navbar {
  display: flex;
  /* TODO: justify-content, align-items, padding */
  background: #1a1a2e;
  color: white;
}

.navbar__logo { font-size: 1.5rem; font-weight: bold; }
.navbar__menu { display: flex; gap: 1.5rem; list-style: none; }
.navbar__btn { background: #e94560; padding: 0.5rem 1rem; border-radius: 4px; }

/* Kart container: 3 kart yan yana, esnek genislik */
.card-container {
  display: flex;
  /* TODO: gap, flex-wrap, justify-content */
}

.card {
  /* TODO: flex ozelliklerini ayarla
     - Minimum 280px genislik
     - Kalan alani esit paylas
     - Maksimum 400px genislik */
  border: 1px solid #333;
  border-radius: 8px;
  padding: 1.5rem;
}

/* Mobil: kartlar alt alta */
@media (max-width: 768px) {
  .card-container {
    /* TODO: flex-direction degistir */
  }
  .card {
    /* TODO: tam genislik yap */
  }
}
</style>

<nav class="navbar">
  <div class="navbar__logo">Logo</div>
  <ul class="navbar__menu">
    <li>Ana Sayfa</li>
    <li>Urunler</li>
    <li>Hakkimizda</li>
  </ul>
  <button class="navbar__btn">Giris Yap</button>
</nav>

<div class="card-container">
  <div class="card"><h3>Kart 1</h3><p>Aciklama</p></div>
  <div class="card"><h3>Kart 2</h3><p>Aciklama</p></div>
  <div class="card"><h3>Kart 3</h3><p>Aciklama</p></div>
</div>
```

**Beklenen Sonuc:** Navbar'da logo sol, menu orta, buton sag tarafta olmali. Kartlar 3'lu yan yana dizilmeli, mobilde alt alta gecmeli.
**Ipucu:** Kartlar icin `flex: 1 1 280px` kullan — minimum 280px, kalan alani esit paylas. `max-width: 400px` ile asiri genislemeyi onle.

---

### Alistirma 2: CSS Grid ile Dashboard Layout (Orta)

CSS Grid kullanarak bir admin dashboard layout'u oluştur: sidebar, header, ana icerik ve footer.

```html
<style>
.dashboard {
  display: grid;
  /* TODO: 2 kolonlu layout tanimla
     - Sidebar: 250px sabit
     - Ana icerik: kalan alan (1fr) */
  grid-template-columns: /* TODO */;

  /* TODO: 3 satirli layout
     - Header: 60px
     - Icerik: kalan alan (1fr)
     - Footer: 40px */
  grid-template-rows: /* TODO */;

  /* TODO: Grid template areas tanimla */
  grid-template-areas:
    "sidebar header"
    "sidebar main"
    "sidebar footer";

  min-height: 100vh;
}

.sidebar { grid-area: sidebar; background: #16213e; }
.header  { grid-area: header;  background: #0f3460; }
.main    { grid-area: main;    background: #1a1a2e; padding: 1rem; }
.footer  { grid-area: footer;  background: #0f3460; }

/* Ana icerik icinde: istatistik kartlari grid'i */
.stats-grid {
  display: grid;
  /* TODO: auto-fill ile responsive grid
     - Minimum 200px, maksimum 1fr
     - 1rem gap */
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: #16213e;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

/* Tablet: sidebar gizle */
@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header"
      "main"
      "footer";
  }
  .sidebar { display: none; }
}
</style>

<div class="dashboard">
  <aside class="sidebar">Sidebar</aside>
  <header class="header">Header</header>
  <main class="main">
    <div class="stats-grid">
      <div class="stat-card"><h3>1,234</h3><p>Kullanicilar</p></div>
      <div class="stat-card"><h3>567</h3><p>Siparisler</p></div>
      <div class="stat-card"><h3>89%</h3><p>Memnuniyet</p></div>
      <div class="stat-card"><h3>$12K</h3><p>Gelir</p></div>
    </div>
  </main>
  <footer class="footer">Footer</footer>
</div>
```

**Beklenen Sonuc:** Sidebar 250px sabit, icerik kalan alani kaplayacak. Istatistik kartlari ekran boyutuna gore otomatik satirlanacak. Tablet'te sidebar gizlenecek.
**Ipucu:** `grid-template-areas` ile her alana isim ver, sonra `grid-area` ile elemanlari yerlesitir. `repeat(auto-fill, minmax(200px, 1fr))` responsive grid icin sihirli formuldur.

---

### Alistirma 3: Box Model ve Responsive Design Debuglama (Zor)

DevTools kullanarak box model sorunlarini tespit et ve responsive tasarim hatalarini duzelt.

```html
<style>
/* BU CSS'TE KASITLI HATALAR VAR — DUZELT */

/* HATA 1: Box sizing — padding genisligi asiyor */
.container {
  width: 100%;
  padding: 20px;
  /* TODO: box-sizing ekle ki padding genisligi asmasin */
}

/* HATA 2: Margin collapse — iki eleman arasi bosluk beklenenden farkli */
.section-a { margin-bottom: 30px; background: #333; padding: 1rem; }
.section-b { margin-top: 20px; background: #444; padding: 1rem; }
/* Soru: Aralarindaki bosluk 50px mi yoksa 30px mi? Neden? */
/* TODO: Margin collapse'i onle (hangi yontem tercih edilir?) */

/* HATA 3: Overflow — icerik tasıyor */
.text-box {
  width: 200px;
  height: 100px;
  /* TODO: overflow ayarla — scroll mu, hidden mi, auto mu? */
}

/* HATA 4: Responsive resim — container'dan tasiyor */
.image-container { width: 300px; }
.image-container img {
  /* TODO: max-width ve height ayarla */
  /* Resim container'dan tasmamali ama oranini koromali */
}

/* HATA 5: Z-index calismıyor */
.modal {
  position: relative;  /* TODO: Dogru position ne olmali? */
  z-index: 1000;
  /* Neden modal arka planda kaliyor? */
}

/* GOREV: DevTools ile dogrula */
/* 1. Her elemana tikla, Computed tab'inda Box Model diyagramini incele */
/* 2. margin, border, padding degerlerini gozlemle */
/* 3. Layout Shift var mi kontrol et (Performance tab) */
</style>

<div class="container">
  <div class="section-a">Section A</div>
  <div class="section-b">Section B</div>
  <div class="text-box">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Bu metin kutudan tasiyor mu?</div>
  <div class="image-container">
    <img src="https://via.placeholder.com/800x600" alt="Test resim">
  </div>
</div>
```

**Beklenen Sonuc:** Tum 5 CSS hatasi duzeltilmis olmali. Box-sizing ile padding sorunu cozulmeli. Margin collapse aciklanabilmeli. Overflow dogru yonetilmeli. Resim responsive olmali.
**Ipucu:** Global olarak `*, *::before, *::after { box-sizing: border-box; }` ekle. Margin collapse icin parent'a `display: flow-root` veya iki eleman arasina `gap` kullan.
:::

:::knowledge-check
type: multiple_choice
question: "flex: 1 kısayolu neyin karşılığıdır?"
options:
  - "flex-grow: 1; flex-shrink: 1; flex-basis: auto;"
  - "flex-grow: 1; flex-shrink: 1; flex-basis: 0%;"
  - "flex-grow: 1; flex-shrink: 0; flex-basis: 100%;"
  - "flex-grow: 0; flex-shrink: 1; flex-basis: 1px;"
correct: 1
explanation: "flex: 1 kısayolu flex-grow: 1, flex-shrink: 1, flex-basis: 0% anlamına gelir. Bu, elemanın kalan alanı eşit paylaşmasını sağlar. flex-basis: 0% önemlidir çünkü elemanların içerik boyutundan bağımsız olarak eşit genişlikte olmasını garanti eder."
:::

:::knowledge-check
type: multiple_choice
question: "auto-fill ve auto-fit arasındaki fark nedir?"
options:
  - "Fark yoktur, aynı şeydir"
  - "auto-fill boş sütunlar için yer ayırır, auto-fit boş sütunları daraltıp mevcut elemanları genişletir"
  - "auto-fit sadece Grid'de çalışır, auto-fill sadece Flexbox'ta"
  - "auto-fill daha performanslıdır"
correct: 1
explanation: "auto-fill, yeterli eleman olmasa bile boş sütunlar için grid track'ler oluşturur. auto-fit ise boş track'leri 0 genişliğe daraltır ve mevcut elemanların genişlemesine izin verir. Genellikle auto-fit tercih edilir çünkü elemanlar mevcut alana yayılır."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Flexbox ve CSS Grid arasindaki temel farki 'tek boyut vs iki boyut' otesinde acikla. Icerikten disari (content-out) vs disaridan iceri (layout-in) yaklasimlarini gercek layout örnekleriyle karsilastir. Ne zaman ikisini birlikte kullanmam gerekir?"

**2. Pratik Uygulama:**
> "Bana bir dashboard layoutu oluştur: ust kisimda navbar (Flexbox), sol tarafta sidebar (sabit 250px), ortada 3 sutunlu kart gridi (CSS Grid auto-fit), altta footer. Responsive olsun - mobilde sidebar gizlensin ve kartlar tek sutun olsun. Kodunu ve her CSS kararinin nedenini yaz."
> Takip: "Simdi bu layouta container queries ekleyerek kartlarin sidebar'da dar, ana alanda genis gorunmesini sagla."

**3. Mukemmellik Icin:**
> "Bir e-ticaret sitesinde CLS (Cumulative Layout Shift) sorunlari yasiyorum. Resimler yuklenirken sayfa kayiyor, font swap oluyor ve skeleton loader'lar dogru boyutta degil. CSS Grid, aspect-ratio, content-visibility ve font-display kullanarak CLS'i sifira yakin nasil dusurrum?"

### Pair Programming Ipucu
Layout sorunlarinda AI'a DevTools'tan alinan computed styles veya element screenshot'ini goster ve sor: "Bu layout neden kirildi? Flexbox/Grid inspector ciktisina bakarak sorunun kaynagini bul ve coz."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Flexbox ve CSS Grid arasindaki fark nedir? Ne zaman hangisini kullanirsiniz?**
- **Junior cevabi:** Flexbox tek yonlu, Grid iki yonlu layout icindir.
- **Senior cevabi:** Flexbox 1 boyutlu (row VEYA column) icerik dagitimi icindir: navbar, card row, centering. Grid 2 boyutlu (row VE column) sayfa layout'u icindir: dashboard, gallery, complex page layout. Pratikte birlikte kullanilirlar: Grid ile genel sayfa yapisi, Flexbox ile grid hucrelerinin icindeki icerik dizilimi yapilir. Grid'in `fr` birimi responsive layout'u kolaylastirir. `auto-fit` ve `minmax()` ile media query'siz responsive grid oluşturulabilir. Accessibility acisindan visual order ile DOM order uyumlu olmalidir.

**Soru 2: CSS specificity nasil calisir?**
- **Junior cevabi:** ID > class > element seklinde oncelik sirasi vardir.
- **Senior cevabi:** Specificity (a,b,c) seklinde hesaplanir: a=ID sayisi, b=class/attribute/pseudo-class, c=element/pseudo-element. `#nav .link:hover` = (1,2,0). Esit specificity'de son yazilan kazanir (cascade). `!important` tum specificity'yi ezer ama bakim kabusuna yol acar, sadece utility class'larda kabul edilebilir. Modern yaklasim: BEM metodolojisi ile flat specificity (tek class), CSS Modules veya Tailwind ile scope izolasyonu. Specificity savaslari mimari sorununun belirtisidir.
:::

:::exercise
### Alıştırma 4: Flexbox ile Centering Teknikleri
**Görev:** Aşağıdaki 4 farklı senaryoda elementleri Flexbox ile ortala.
**Başlangıç kodu:**
```css
/* Senaryo 1: Hem yatay hem dikey ortala (tam sayfa) */
.center-page {
  height: 100vh;
  /* TODO: Flexbox ile ortala */
}

/* Senaryo 2: Sadece yatay ortala */
.center-horizontal {
  /* TODO */
}

/* Senaryo 3: Son elemanı sağa yapıştır */
.space-between-row {
  display: flex;
  /* TODO: İlk 2 eleman solda, son eleman sağda */
}

/* Senaryo 4: Flex item'ı kendi satırında ortala */
.self-center {
  /* TODO: Sadece bu item dikey ortada */
}
```
**Beklenen çıktı:**
```
Senaryo 1: justify-content: center + align-items: center
Senaryo 2: justify-content: center
Senaryo 3: .last-item { margin-left: auto; }
Senaryo 4: align-self: center
```
**İpucu:** `margin-left: auto` bir Flexbox item'ını sağa iterken çok kullanışlıdır.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: Flex-grow, Flex-shrink, Flex-basis Hesaplama
**Görev:** Aşağıdaki kodda her elemanın son genişliğini hesapla.
**Başlangıç kodu:**
```css
.container {
  display: flex;
  width: 600px;
}

.item-a { flex: 2 1 100px; } /* flex-grow:2, shrink:1, basis:100px */
.item-b { flex: 1 1 100px; } /* flex-grow:1, shrink:1, basis:100px */
.item-c { flex: 1 1 200px; } /* flex-grow:1, shrink:1, basis:200px */

/* Toplam basis = 100 + 100 + 200 = 400px */
/* Kalan alan = 600 - 400 = 200px */
/* Toplam grow = 2 + 1 + 1 = 4 */

/* TODO: Her item'ın son genişliğini hesapla */
```
**Beklenen çıktı:**
```
item-a: 100 + (200 * 2/4) = 200px
item-b: 100 + (200 * 1/4) = 150px
item-c: 200 + (200 * 1/4) = 250px
Toplam: 200 + 150 + 250 = 600px ✓
```
**İpucu:** Kalan alan = container genişliği - toplam basis. Her item'a grow oranına göre dağıtılır.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: CSS Grid ile Fotoğraf Galerisi
**Görev:** CSS Grid kullanarak Pinterest tarzı masonry-benzeri bir fotoğraf galerisi oluştur.
**Başlangıç kodu:**
```css
.gallery {
  display: grid;
  /* TODO: 3 sütunlu grid, her sütun eşit genişlikte */
  grid-template-columns: /* ? */;
  gap: 10px;
  /* TODO: Satır yüksekliğini otomatik ayarla */
  grid-auto-rows: /* ? */;
}

.gallery-item:nth-child(1) {
  /* TODO: 2 satır kaplasın (dikey uzun fotoğraf) */
  grid-row: /* ? */;
}

.gallery-item:nth-child(4) {
  /* TODO: 2 sütun kaplasın (yatay geniş fotoğraf) */
  grid-column: /* ? */;
}
```
**Beklenen çıktı:**
```
grid-template-columns: repeat(3, 1fr);
grid-auto-rows: 200px;
grid-row: span 2;
grid-column: span 2;
```
**İpucu:** `span 2` ile bir grid item'ı 2 satır veya 2 sütun kaplayabilir. `grid-auto-rows` otomatik oluşan satırların yüksekliğini belirler.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: Grid Template Areas ile Blog Layout
**Görev:** `grid-template-areas` kullanarak responsive bir blog sayfası düzeni oluştur.
**Başlangıç kodu:**
```css
.blog-layout {
  display: grid;
  gap: 20px;
  /* TODO: Desktop layout tanımla
     header  header  header
     sidebar content content
     sidebar content content
     footer  footer  footer  */
  grid-template-areas:
    /* ? */;
  grid-template-columns: /* ? */;
}

.blog-header  { grid-area: /* ? */; }
.blog-sidebar { grid-area: /* ? */; }
.blog-content { grid-area: /* ? */; }
.blog-footer  { grid-area: /* ? */; }

/* TODO: Mobilde sidebar üstte, content altta olacak şekilde düzenle */
@media (max-width: 768px) {
  .blog-layout {
    grid-template-areas:
      /* ? */;
    grid-template-columns: /* ? */;
  }
}
```
**Beklenen çıktı:**
```css
/* Desktop */
grid-template-areas:
  "header header header"
  "sidebar content content"
  "sidebar content content"
  "footer footer footer";
grid-template-columns: 250px 1fr 1fr;

/* Mobil */
grid-template-areas:
  "header"
  "sidebar"
  "content"
  "footer";
grid-template-columns: 1fr;
```
**İpucu:** `grid-template-areas` her satırı tırnak içinde yaz. Alan isimleri tekrar ederse birleşir.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Flexbox Order ve Reverse
**Görev:** HTML değiştirmeden CSS ile elemanların sırasını değiştir.
**Başlangıç kodu:**
```html
<div class="flex-container">
  <div class="item" id="a">A</div>
  <div class="item" id="b">B</div>
  <div class="item" id="c">C</div>
  <div class="item" id="d">D</div>
</div>
```
```css
.flex-container {
  display: flex;
}

/* TODO 1: Sırayı D, C, B, A yap (tümünü ters çevir) */
/* TODO 2: Sadece C'yi en başa getir (C, A, B, D) */
/* TODO 3: Sırayı B, D, A, C yap (her birini ayrı order ile) */
```
**Beklenen çıktı:**
```css
/* TODO 1 */
.flex-container { flex-direction: row-reverse; }

/* TODO 2 */
#c { order: -1; }

/* TODO 3 */
#b { order: 1; }
#d { order: 2; }
#a { order: 3; }
#c { order: 4; }
```
**İpucu:** `order` varsayılan 0'dır. Negatif değerler elemanı öne taşır. `flex-direction: row-reverse` tüm sırayı tersler.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 9: Responsive Grid - auto-fit vs auto-fill
**Görev:** `auto-fit` ve `auto-fill` arasındaki farkı gözlemle ve doğru olanı seç.
**Başlangıç kodu:**
```css
/* Senaryo: 1200px container'da sadece 2 kart var */

.grid-autofill {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.grid-autofit {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

/* TODO: Her iki grid için kaç sütun oluşur?
   1200px / 250px = 4 sütun potansiyel

   auto-fill: Kaç sütun? Kartlar ne kadar geniş?
   auto-fit:  Kaç sütun? Kartlar ne kadar geniş?
*/
```
**Beklenen çıktı:**
```
auto-fill: 4 sütun oluşur, 2 kart ilk 2 sütunda (250px), 2 boş sütun ayrılır
auto-fit:  Boş sütunlar daraltılır, 2 kart eşit genişlikte yayılır (~592px)

Sonuç: Kartlar yayılsın istiyorsan → auto-fit
        Grid yapısı sabit kalsın istiyorsan → auto-fill
```
**İpucu:** DevTools'ta Grid inspector açarak sütun çizgilerini gözlemle. `auto-fill` boş track oluşturur, `auto-fit` oluşturmaz.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: Karmaşık Layout - Holy Grail Pattern
**Görev:** CSS Grid ve Flexbox birlikte kullanarak "Holy Grail" layout'unu oluştur: header, footer, sol sidebar, sağ sidebar ve ortada ana içerik. Responsive olmalı.
**Başlangıç kodu:**
```css
.holy-grail {
  display: grid;
  min-height: 100vh;
  /* TODO: 3 sütunlu layout:
     - Sol sidebar: 200px
     - Ana içerik: kalan alan
     - Sağ sidebar: 200px */
  grid-template-columns: /* ? */;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    /* TODO: Header tüm genişlikte
       Sol sidebar | main | Sağ sidebar
       Footer tüm genişlikte */;
}

/* TODO: İçerik alanında Flexbox ile kart dizilimi */
.main-content {
  grid-area: main;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px;
}

.content-card {
  /* TODO: Minimum 300px, eşit genişlik paylaşımı */
  flex: /* ? */;
}

/* TODO: Tablet - sağ sidebar gizle */
@media (max-width: 1024px) {
  .holy-grail {
    grid-template-columns: /* ? */;
    grid-template-areas: /* ? */;
  }
  .right-sidebar { display: none; }
}

/* TODO: Mobil - her şey tek sütun */
@media (max-width: 768px) {
  .holy-grail {
    grid-template-columns: /* ? */;
    grid-template-areas: /* ? */;
  }
  .left-sidebar { display: none; }
}
```
**Beklenen çıktı:**
```css
grid-template-columns: 200px 1fr 200px;
grid-template-areas:
  "header header header"
  "left-sidebar main right-sidebar"
  "footer footer footer";

.content-card { flex: 1 1 300px; }

/* Tablet */
grid-template-columns: 200px 1fr;
grid-template-areas:
  "header header"
  "left-sidebar main"
  "footer footer";

/* Mobil */
grid-template-columns: 1fr;
grid-template-areas: "header" "main" "footer";
```
**İpucu:** Grid ile genel sayfa yapısını, Flexbox ile içerik alanındaki kartları düzenle. Bu "Grid dışı, Flexbox içi" yaklaşımı en yaygın production pattern'idir.
**Zorluk:** Zor
:::

:::must-note
- Box Model: content + padding + border + margin. Her zaman `box-sizing: border-box` kullan
- Margin collapse: Dikey margin'ler birleşir (büyük olan kazanır). Flexbox/Grid içinde collapse olmaz
- Flexbox container: display: flex, flex-direction, justify-content, align-items, gap
- Flexbox item: flex-grow, flex-shrink, flex-basis, align-self, order
- flex: 1 = flex: 1 1 0% (eşit genişlik paylaşımı)
- Grid container: display: grid, grid-template-columns/rows, grid-template-areas, gap
- fr birimi: Kalan alanı orantısal böler (1fr 2fr = %33 ve %66)
- repeat(auto-fit, minmax(250px, 1fr)): Responsive grid tek satırda
- auto-fill: boş sütun yer ayırır, auto-fit: boş sütun daraltır ve mevcut elemanları genişletir
- Mobile-first: min-width ile media query yaz (768px tablet, 1024px desktop)
- clamp(min, preferred, max): Fluid typography ve spacing için
- Container queries: Parent boyutuna göre stil. Media query'den daha component-odaklı
- :has(): Parent selector. "İçinde X olan Y'yi seç" mantığı
- Flexbox = tek boyut (navbar, buton grubu), Grid = iki boyut (sayfa düzeni, dashboard)
- Grid for layout, Flexbox for alignment: İkisini birlikte kullan
:::

:::senior-learns
Bir Senior Developer, CSS Layout konusunda şu yaklaşımı benimser:

1. **Design system ile çalışır** - Spacing scale (4, 8, 12, 16, 24, 32, 48, 64px), breakpoint'ler ve grid yapısını design token olarak tanımlar. Her yerde aynı spacing kullanarak görsel tutarlılık sağlar.
2. **Intrinsic design yaklaşımını benimser** - Jen Simmons'ın öncülük ettiği "Intrinsic Web Design" felsefesiyle, sabit breakpoint'ler yerine içeriğin doğal akışını kullanır. clamp(), min(), max(), auto-fit/auto-fill ile breakpoint sayısını minimumda tutar.
3. **Container queries ile component-odaklı düşünür** - Viewport yerine container'a göre responsive olan component'lar yazar. Bu sayede aynı component farklı layout'larda (sidebar vs. ana alan) farklı davranır.
4. **Layout shift'leri önler** - CLS (Cumulative Layout Shift) metriğini takip eder. Resimlere aspect-ratio verir, skeleton loader kullanır, font swap stratejisi uygular.
5. **CSS Grid subgrid'i kullanır** - Nested grid'lerde parent'ın grid çizgilerini child'a aktararak hizalama tutarlılığı sağlar.
6. **Performance-aware layout yazar** - will-change, contain, content-visibility gibi CSS özelliklerini kullanarak rendering performansını optimize eder. Gereksiz reflow'lardan kaçınır.

**Profesyonel Mindset:** "Layout yazmak sadece 'doğru görünüyor' ile bitmez. Responsive mi? Accessible mi? Performanslı mı? Bakımı kolay mı? Bu 4 sorunun cevabı 'evet' olduğunda layout tamamdır. Tarayıcının layout engine'ini anlayan developer, CSS'i savaşmak yerine onunla çalışır."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Layout** (leɪ-aʊt) → Düzen / Sayfa düzeni
   *"CSS Grid is ideal for creating complex two-dimensional layouts."*

2. **Responsive** (rɪ-spɒn-sɪv) → Duyarlı
   *"A responsive design adapts to different screen sizes using media queries."*

3. **Viewport** (vjuː-pɔːrt) → Görüntüleme alanı
   *"Media queries check the viewport width to apply different styles."*

4. **Breakpoint** (breɪk-pɔɪnt) → Kırılma noktası
   *"We set our first breakpoint at 768px for tablet devices."*

5. **Alignment** (ə-laɪn-mənt) → Hizalama
   *"Flexbox provides powerful alignment capabilities along both axes."*

**Okuma Egzersizi:** CSS-Tricks'te "A Complete Guide to Flexbox" makalesini İngilizce oku: https://css-tricks.com/snippets/css/a-guide-to-flexbox/

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Responsive grid layout'u uyguladım"
→ Örnek: `feat: implement responsive grid layout with CSS Grid and media queries`
:::

:::external-resource
- 📖 **CSS-Tricks:** "A Complete Guide to Flexbox" ve "A Complete Guide to Grid" (ücretsiz)
- 🎮 **Flexbox Froggy:** flexboxfroggy.com (interaktif Flexbox oyunu, ücretsiz)
- 🎮 **Grid Garden:** cssgridgarden.com (interaktif Grid oyunu, ücretsiz)
- 📺 **Kevin Powell:** YouTube CSS Layout videoları (ücretsiz)
- 📖 **Web.dev:** "Learn CSS" (Google, ücretsiz)
- 🔧 **Grid Generator:** cssgrid-generator.netlify.app (görsel grid oluşturucu)
:::
