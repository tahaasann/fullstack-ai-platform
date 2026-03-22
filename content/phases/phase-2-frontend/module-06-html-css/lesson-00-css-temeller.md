---
title: "CSS Temelleri: Box Model, Flexbox, Grid ve Responsive Design"
estimated_minutes: 90
tags: ["css", "box-model", "flexbox", "grid", "responsive", "selectors", "positioning"]
prerequisites: []
---

# CSS Temelleri: Box Model, Flexbox, Grid ve Responsive Design

:::realworld
CSS (Cascading Style Sheets) her web sayfasının görsel temelini oluşturur. Bir sayfayı açtığında gördüğün her renk, her boşluk, her hizalama CSS ile yapılıyor. Frontend developer olarak her gün yüzlerce satır CSS yazacaksın. Bu derste CSS'in temel yapı taşlarını "deha seviyesinde" öğreneceksin.

**Gerçek Dünya Örnekleri:**
- **Airbnb:** Kart tabanlı layout'ları CSS Grid ile yapılır. Her cihazda farklı kolon sayısı gösterilir (mobilde 1, tablette 2, desktop'ta 4 kolon). Grid'in `auto-fill` ve `minmax()` özellikleri sayesinde tek satır CSS ile responsive olur.
- **Spotify:** Sidebar + ana içerik layout'u Flexbox ile yapılır. Sol menü sabit genişlikte kalırken, ana içerik alanı `flex-grow: 1` ile kalan alanı doldurur. Çalma listesi grid'leri CSS Grid ile hizalanır.
- **Twitter/X:** Timeline'daki her tweet bir Flexbox container'dır: avatar sol tarafta, içerik sağ tarafta. İç içe flexbox kullanımı sayesinde kullanıcı adı, zaman, metin ve etkileşim butonları mükemmel hizalanır.
- **YouTube:** Video grid'i CSS Grid ile yapılır. `grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))` ile ekran genişliğine göre otomatik kolon sayısı ayarlanır.
:::

## Neden CSS'i Derinlemesine Öğrenmelisin?

Çoğu junior developer CSS'i "deneme yanılma" ile yazıyor. Bir şey çalışmayınca random property'ler deniyor. Bu yaklaşım seni asla senior seviyesine taşımaz. CSS'in temel kurallarını anlayınca:

- Layout sorunlarını 30 saniyede çözersin (saatler yerine)
- Responsive design'ı doğal olarak yaparsın
- Tailwind CSS gibi framework'leri çok daha etkili kullanırsın
- Pixel-perfect UI implementasyonu yapabilirsin

:::deha-tip
Senior developer'lar CSS yazarken **mental model** kullanır. Bir element'i gördüklerinde kafalarında box model'i, stacking context'i ve layout flow'u canlandırırlar. Bu ders boyunca bu mental modeli inşa edeceğiz. Her property'yi "neden böyle çalışıyor?" diye sorgula.
:::

:::senior-learns
Senior/CTO CSS'i öğrenirken spesifikasyonu okur. W3C CSS spesifikasyonu her property'nin tam davranışını tanımlar. `margin collapse` neden oluyor? Spesifikasyon diyor ki: "Adjoining margins of two or more boxes collapse into a single margin." Senior bunu bilir, junior "neden margin'im kayboldu?" diye şaşırır. Kaynak: https://www.w3.org/TR/CSS2/box.html
:::

## CSS Seçiciler ve Spesifite (Specificity)

CSS'in "Cascading" kısmı, birden fazla kural aynı elemente uygulandığında hangisinin kazanacağını belirler. Bu sistem **specificity** (özgüllük) ile çalışır.

### Temel Seçiciler

:::code[css]{title="CSS Seçici Türleri"}
/* Element (Type) Seçici - Specificity: 0-0-1 */
p {
  color: #d1d5db; /* gray-300 */
}

/* Class Seçici - Specificity: 0-1-0 */
.card {
  background: #111827; /* gray-900 */
  border-radius: 8px;
}

/* ID Seçici - Specificity: 1-0-0 */
#header {
  position: sticky;
  top: 0;
}

/* Attribute Seçici - Specificity: 0-1-0 */
input[type="email"] {
  border: 1px solid #4b5563;
}

/* Pseudo-class Seçici - Specificity: 0-1-0 */
a:hover {
  color: #34d399; /* emerald-400 */
}

/* Pseudo-element Seçici - Specificity: 0-0-1 */
p::first-line {
  font-weight: bold;
}

/* Universal Seçici - Specificity: 0-0-0 */
* {
  box-sizing: border-box;
}
:::

### Spesifite Hesaplama

:::concept[Specificity (İng: Specificity)]
Specificity, CSS'te birden fazla kuralın aynı elemente uygulanması durumunda hangi kuralın öncelikli olacağını belirleyen puanlama sistemidir.

**Türkçe karşılığı:** Özgüllük / Seçici Önceliği
**Ne işe yarar:** Çakışan CSS kuralları arasında hangisinin kazanacağını belirler
**Gerçek hayat benzetmesi:** Askeri rütbe sistemi gibi - General (ID) her zaman Albay'ı (class) yener, Albay da Er'i (element) yener
:::

:::code[css]{title="Specificity Puanlama: (ID - Class - Element)"}
/* Specificity: 0-0-1 (sadece element) */
h1 { color: red; }

/* Specificity: 0-1-0 (bir class) */
.title { color: blue; }

/* Specificity: 0-1-1 (bir class + bir element) */
h1.title { color: green; }

/* Specificity: 0-2-0 (iki class) */
.card .title { color: purple; }

/* Specificity: 1-0-0 (bir ID) */
#main-title { color: orange; }

/* Specificity: 1-1-1 (ID + class + element) */
div#main .title { color: pink; }

/* !important - Nuclear option (KULLANMA!) */
p { color: red !important; } /* Her şeyi yener */
:::

:::warning
`!important` kullanmak CSS'in specificity sistemini tamamen devre dışı bırakır. Bir kez kullanınca, onu override etmek için başka bir `!important` yazman gerekir ve bu kısır döngüye girer. Production kodunda `!important` kullanmak büyük bir code smell'dir. Tek istisna: third-party kütüphane CSS'ini override ederken bazen mecbur kalabilirsin.
:::

:::beginner-mistake
Yaygın hata: CSS kurallarının sırası her zaman önemlidir diye düşünmek. Sıra sadece specificity eşit olduğunda belirleyicidir. `#title { color: red; }` kuralı dosyanın başında olsa bile, alttaki `.title { color: blue; }` kuralını yener, çünkü ID seçici class seçiciden daha spesifiktir.
:::

### Birleştirici Seçiciler (Combinators)

:::code[css]{title="CSS Combinators"}
/* Descendant (boşluk) - Tüm alt elemanlar */
.card p {
  margin-bottom: 8px;
}

/* Child (>) - Sadece direkt çocuklar */
.card > p {
  font-size: 14px;
}

/* Adjacent Sibling (+) - Hemen sonraki kardeş */
h2 + p {
  margin-top: 0; /* h2'den sonraki ilk p'nin üst boşluğunu kaldır */
}

/* General Sibling (~) - Sonraki tüm kardeşler */
h2 ~ p {
  color: #9ca3af;
}

/* Birden fazla seçiciyi grupla */
h1, h2, h3 {
  font-family: 'Inter', sans-serif;
}
:::

:::exercise
**Alıştırma 1: Specificity Hesaplama**

Aşağıdaki seçicilerin specificity değerlerini hesapla ve `h1` elementinin rengini belirle:

```css
h1 { color: red; }                     /* ? */
.header h1 { color: blue; }            /* ? */
#page .header h1 { color: green; }     /* ? */
.header h1.title { color: purple; }    /* ? */
```

```html
<div id="page">
  <header class="header">
    <h1 class="title">Merhaba</h1>
  </header>
</div>
```

**Beklenen cevap:** Her seçicinin specificity değerini hesapla ve en yüksek olanı bul. h1'in rengi hangi kural tarafından belirleniyor?

**Çözüm:**
- `h1` → 0-0-1 → red
- `.header h1` → 0-1-1 → blue
- `#page .header h1` → 1-1-1 → green (KAZANIR)
- `.header h1.title` → 0-2-1 → purple

Cevap: `h1` yeşil (green) olur çünkü `#page .header h1` en yüksek specificity'ye (1-1-1) sahip.
:::

## Box Model: CSS'in Temel Yapı Taşı

Her HTML elementi bir kutu (box) olarak render edilir. Bu kutunun 4 katmanı vardır:

:::concept[Box Model (İng: Box Model)]
Box Model, her HTML elementinin nasıl yer kapladığını tanımlayan temel CSS modelidir. Her element content (içerik), padding (iç boşluk), border (kenarlık) ve margin (dış boşluk) olmak üzere 4 katmandan oluşur.

**Türkçe karşılığı:** Kutu Modeli
**Ne işe yarar:** Elementlerin boyutunu ve aralarındaki boşlukları kontrol eder
**Gerçek hayat benzetmesi:** Bir hediye paketi: hediyenin kendisi (content), etrafındaki sünger (padding), kutu (border), kutular arası boşluk (margin)
:::

:::code[text]{title="Box Model Yapısı"}
┌─────────────────────────────────────────┐
│                 MARGIN                   │  ← Dış boşluk (şeffaf, tıklanamaz)
│   ┌─────────────────────────────────┐   │
│   │             BORDER               │   │  ← Kenarlık (görünür çizgi)
│   │   ┌─────────────────────────┐   │   │
│   │   │         PADDING          │   │   │  ← İç boşluk (arka plan rengi görünür)
│   │   │   ┌─────────────────┐   │   │   │
│   │   │   │                 │   │   │   │
│   │   │   │    CONTENT      │   │   │   │  ← İçerik (metin, resim vb.)
│   │   │   │                 │   │   │   │
│   │   │   └─────────────────┘   │   │   │
│   │   └─────────────────────────┘   │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
:::

:::code[css]{title="Box Model Özellikleri"}
.card {
  /* Content boyutu */
  width: 300px;
  height: 200px;

  /* Padding: İç boşluk (4 yön ayrı ayrı veya kısaltma) */
  padding-top: 20px;
  padding-right: 16px;
  padding-bottom: 20px;
  padding-left: 16px;
  /* Kısaltma: üst sağ alt sol (saat yönünde) */
  padding: 20px 16px 20px 16px;
  /* 2 değer: üst-alt sağ-sol */
  padding: 20px 16px;
  /* 1 değer: dört yön aynı */
  padding: 20px;

  /* Border: Kenarlık */
  border: 1px solid #374151;
  border-radius: 8px; /* Köşe yuvarlama */

  /* Margin: Dış boşluk */
  margin: 16px;
  margin: 0 auto; /* Yatay ortalama (block element) */
}
:::

### box-sizing: content-box vs border-box

:::code[css]{title="box-sizing Farkı"}
/* DEFAULT: content-box */
.box-content {
  box-sizing: content-box; /* Tarayıcı varsayılanı */
  width: 300px;
  padding: 20px;
  border: 2px solid black;
  /* Gerçek genişlik: 300 + 20*2 + 2*2 = 344px! */
}

/* ÖNERİLEN: border-box */
.box-border {
  box-sizing: border-box;
  width: 300px;
  padding: 20px;
  border: 2px solid black;
  /* Gerçek genişlik: 300px (padding ve border dahil) */
  /* Content alanı: 300 - 20*2 - 2*2 = 256px */
}

/* Global Reset - HER PROJEDE KULLAN */
*, *::before, *::after {
  box-sizing: border-box;
}
:::

:::must-note
**MUTLAKA NOT AL:** `box-sizing: border-box` her projenin CSS reset'inde olmalı. Bu olmadan width/height hesaplamaları sürekli yanlış çıkar. Tailwind CSS bunu otomatik ayarlar ama vanilla CSS'te sen eklemelisin. Bu tek satır CSS, saatlerce debug süresini kurtarır.
:::

### Margin Collapse

:::concept[Margin Collapse (İng: Margin Collapse)]
Dikey komşu margin'ler birleşir (collapse). İki elementin dikey margin'leri toplanmaz, büyük olan kazanır.

**Türkçe karşılığı:** Margin Çökmesi / Birleşmesi
**Ne işe yarar:** Dikey boşlukların beklediğinden farklı olmasının sebebi
**Gerçek hayat benzetmesi:** İki kişi arasındaki sosyal mesafe - her ikisi de 1 metre istiyorsa, aralarında 2 metre değil 1 metre olur
:::

:::code[css]{title="Margin Collapse Örnekleri"}
/* COLLAPSE OLUR: Dikey komşu margin'ler */
.box-1 { margin-bottom: 30px; }
.box-2 { margin-top: 20px; }
/* Aradaki boşluk: 30px (büyük olan kazanır, 50px DEĞİL!) */

/* COLLAPSE OLMAZ: Yatay margin'ler */
.left { margin-right: 30px; }
.right { margin-left: 20px; }
/* Aradaki boşluk: 50px (toplanır) */

/* COLLAPSE OLMAZ: Flexbox/Grid çocukları */
.flex-container { display: flex; flex-direction: column; }
.flex-container .item { margin: 20px 0; }
/* Her item arasında 40px boşluk olur (collapse yok!) */

/* COLLAPSE OLMAZ: Padding veya border varsa */
.parent {
  padding-top: 1px; /* Bu bile collapse'u engeller */
}
:::

:::beginner-mistake
Yaygın hata: "İki element arasında margin-bottom: 20px ve margin-top: 20px koydum, 40px boşluk olmalı" diye düşünmek. Hayır! Dikey margin'ler collapse eder, sadece 20px olur. Bu davranışı istemiyorsan Flexbox/Grid kullan veya parent'a padding/border ekle.
:::

:::exercise
**Alıştırma 2: Box Model Hesaplama**

Aşağıdaki CSS ile bir element'in gerçek boyutlarını hesapla:

```css
.box {
  width: 400px;
  height: 250px;
  padding: 24px 32px;
  border: 3px solid #374151;
  margin: 16px;
}
```

1. `box-sizing: content-box` (varsayılan) ile gerçek genişlik ve yükseklik ne olur?
2. `box-sizing: border-box` ile content alanının genişliği ve yüksekliği ne olur?

**Çözüm:**
1. content-box:
   - Genişlik: 400 + 32*2 + 3*2 = 470px
   - Yükseklik: 250 + 24*2 + 3*2 = 304px
   - (Margin dahil değil - margin elementin dışındaki boşluk)

2. border-box:
   - Toplam: 400px x 250px (değişmez)
   - Content genişliği: 400 - 32*2 - 3*2 = 330px
   - Content yüksekliği: 250 - 24*2 - 3*2 = 196px
:::

## Display Türleri

Her HTML elementinin varsayılan bir display değeri vardır. Bu değer elementin sayfa üzerinde nasıl davranacağını belirler.

:::code[css]{title="Display Türleri ve Davranışları"}
/* BLOCK: Yeni satırda başlar, tüm genişliği kaplar */
/* Varsayılan block elementler: div, p, h1-h6, section, article, form */
.block-element {
  display: block;
  width: 100%;          /* Tüm genişliği kaplar (varsayılan) */
  /* width/height ayarlanabilir */
  /* margin/padding 4 yönde çalışır */
}

/* INLINE: Satır içinde kalır, metin gibi davranır */
/* Varsayılan inline elementler: span, a, strong, em, img */
.inline-element {
  display: inline;
  /* width/height ÇALIŞMAZ! */
  /* margin-top/margin-bottom ÇALIŞMAZ! */
  /* padding-top/bottom çalışır ama layout'u etkilemez */
}

/* INLINE-BLOCK: Satır içinde kalır ama block gibi boyutlandırılır */
.inline-block-element {
  display: inline-block;
  width: 150px;          /* Çalışır */
  height: 40px;          /* Çalışır */
  margin: 8px;           /* 4 yönde çalışır */
  padding: 12px;         /* 4 yönde çalışır */
  vertical-align: middle; /* Dikey hizalama yapılabilir */
}

/* NONE: Elementi tamamen kaldırır (yer kaplamaz) */
.hidden {
  display: none;
}

/* FLEX ve GRID: Aşağıda detaylı anlatılacak */
.flex-container { display: flex; }
.grid-container { display: grid; }
:::

:::exercise
**Alıştırma 3: Display Davranışları**

Aşağıdaki HTML'de her elementin nasıl görüneceğini tahmin et:

```html
<div style="background: #1f2937; padding: 16px;">
  <span style="width: 200px; height: 50px; background: #059669; margin: 20px;">
    Span 1
  </span>
  <span style="display: inline-block; width: 200px; height: 50px; background: #2563eb; margin: 20px;">
    Span 2
  </span>
</div>
```

**Soru:** Span 1 ve Span 2 arasındaki fark nedir? Hangisinin width/height'ı çalışır?

**Çözüm:**
- **Span 1:** `inline` olduğu için `width: 200px` ve `height: 50px` **çalışmaz**. Sadece içeriği kadar yer kaplar. `margin-top` ve `margin-bottom` da **çalışmaz**.
- **Span 2:** `inline-block` olduğu için `width: 200px` ve `height: 50px` **çalışır**. 200x50px'lik bir kutu olarak görünür. Margin 4 yönde çalışır.
:::

## Flexbox: Tek Boyutlu Layout

Flexbox, elementleri tek bir eksen boyunca (yatay veya dikey) hizalamak için kullanılır. Modern CSS layout'unun temel taşıdır.

:::concept[Flexbox (İng: Flexible Box Layout)]
Flexbox, bir container içindeki elementleri esnek bir şekilde hizalamak ve dağıtmak için kullanılan CSS layout modülüdür. Tek bir eksen (ana eksen) boyunca çalışır.

**Türkçe karşılığı:** Esnek Kutu Düzeni
**Ne işe yarar:** Elementleri yatay veya dikey olarak hizalar, aralarında boşluk dağıtır, responsive layout yapar
**Gerçek hayat benzetmesi:** Kitaplıktaki kitapları düşün - soldan sağa dizebilirsin, ortaya toplayabilirsin, eşit aralıklarla yerleştirebilirsin, hatta ters çevirebilirsin
:::

:::code[text]{title="Flexbox Eksen Yapısı"}
flex-direction: row (varsayılan)
┌─────────────────────────────────────────────┐
│ ←  ←  ←  ←  ←  MAIN AXIS (Ana Eksen)  →  →│
│ ┌──────┐  ┌──────┐  ┌──────┐               │ ↑
│ │Item 1│  │Item 2│  │Item 3│               │ │ CROSS AXIS
│ └──────┘  └──────┘  └──────┘               │ │ (Çapraz Eksen)
│                                             │ ↓
└─────────────────────────────────────────────┘

flex-direction: column
┌──────────────────┐
│ ↑ MAIN AXIS      │← CROSS AXIS →
│ ┌──────────────┐ │
│ │   Item 1     │ │
│ └──────────────┘ │
│ ┌──────────────┐ │
│ │   Item 2     │ │
│ └──────────────┘ │
│ ┌──────────────┐ │
│ │   Item 3     │ │
│ └──────────────┘ │
│ ↓                │
└──────────────────┘
:::

### Flex Container Özellikleri

:::code[css]{title="Flex Container (Parent) Özellikleri"}
.flex-container {
  display: flex;

  /* 1. flex-direction: Ana eksen yönü */
  flex-direction: row;            /* Soldan sağa (varsayılan) */
  flex-direction: row-reverse;    /* Sağdan sola */
  flex-direction: column;         /* Yukarıdan aşağı */
  flex-direction: column-reverse; /* Aşağıdan yukarı */

  /* 2. justify-content: Ana eksende hizalama */
  justify-content: flex-start;    /* Başa yasla (varsayılan) */
  justify-content: flex-end;      /* Sona yasla */
  justify-content: center;        /* Ortala */
  justify-content: space-between; /* İlk ve son kenarda, aralar eşit */
  justify-content: space-around;  /* Her item etrafında eşit boşluk */
  justify-content: space-evenly;  /* Tüm boşluklar eşit */

  /* 3. align-items: Çapraz eksende hizalama */
  align-items: stretch;           /* Tüm yüksekliği kapla (varsayılan) */
  align-items: flex-start;        /* Üste yasla */
  align-items: flex-end;          /* Alta yasla */
  align-items: center;            /* Ortala */
  align-items: baseline;          /* Metin tabanına hizala */

  /* 4. flex-wrap: Taşma davranışı */
  flex-wrap: nowrap;              /* Tek satırda sığdır (varsayılan) */
  flex-wrap: wrap;                /* Alt satıra geç */
  flex-wrap: wrap-reverse;       /* Üst satıra geç */

  /* 5. gap: Elemanlar arası boşluk (modern yöntem) */
  gap: 16px;                      /* Tüm yönlerde */
  gap: 16px 24px;                 /* satır-arası kolon-arası */
  row-gap: 16px;                  /* Sadece satır arası */
  column-gap: 24px;               /* Sadece kolon arası */

  /* 6. align-content: Birden fazla satırda dağılım (wrap gerekli) */
  align-content: flex-start;
  align-content: center;
  align-content: space-between;
}
:::

### Flex Item Özellikleri

:::code[css]{title="Flex Item (Child) Özellikleri"}
.flex-item {
  /* 1. flex-grow: Kalan boşluktan ne kadar alacak */
  flex-grow: 0;     /* Büyüme (varsayılan) */
  flex-grow: 1;     /* Kalan boşluğu paylaş */

  /* 2. flex-shrink: Yer azalınca ne kadar küçülecek */
  flex-shrink: 1;   /* Normal küçülme (varsayılan) */
  flex-shrink: 0;   /* Küçülme, sabit kal */

  /* 3. flex-basis: Başlangıç boyutu */
  flex-basis: auto;   /* İçeriğe göre (varsayılan) */
  flex-basis: 200px;  /* 200px ile başla */
  flex-basis: 25%;    /* Container'ın %25'i */

  /* Kısaltma: flex: grow shrink basis */
  flex: 0 1 auto;    /* Varsayılan */
  flex: 1;           /* flex: 1 1 0% - Eşit genişlik paylaş */
  flex: 1 0 300px;   /* 300px'den başla, büyüyebilir, küçülemez */

  /* 4. align-self: Bu item'ın çapraz eksen hizalamasını override et */
  align-self: center;

  /* 5. order: Görsel sıralama (DOM sırası değişmez) */
  order: 0;   /* Varsayılan */
  order: -1;  /* En başa taşı */
  order: 1;   /* Sona taşı */
}
:::

:::must-note
**MUTLAKA NOT AL:** `flex: 1` kısaltması en sık kullanılan Flexbox pattern'idir. Anlamı: "kalan boşluğu eşit olarak paylaş." Sidebar + main content layout'unda main'e `flex: 1` verirsen, sidebar sabit genişlikte kalırken main kalan alanı doldurur. Bu pattern'i her gün kullanacaksın.
:::

### Flexbox Layout Kalıpları (Patterns)

:::code[css]{title="En Sık Kullanılan Flexbox Pattern'leri"}
/* 1. Dikey ve Yatay Ortalama (Centering) */
.center-everything {
  display: flex;
  justify-content: center;  /* Yatay ortala */
  align-items: center;      /* Dikey ortala */
  min-height: 100vh;        /* Tam ekran yüksekliği */
}

/* 2. Navbar Layout */
.navbar {
  display: flex;
  justify-content: space-between; /* Logo sol, menü sağ */
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

/* 3. Sidebar + Main Content */
.app-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 260px;          /* Sabit genişlik */
  flex-shrink: 0;        /* Küçülmesin */
}
.main-content {
  flex: 1;               /* Kalan alanı doldur */
}

/* 4. Card Footer (alt kısıma yapışık) */
.card {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.card-body {
  flex: 1;               /* İçerik alanı büyüsün */
}
.card-footer {
  margin-top: auto;      /* Alta yapış */
}

/* 5. Eşit Genişlikte Kolonlar */
.equal-columns {
  display: flex;
  gap: 16px;
}
.equal-columns > * {
  flex: 1;               /* Her kolon eşit genişlik */
}
:::

:::exercise
**Alıştırma 4: Flexbox Navbar**

Aşağıdaki HTML için CSS yaz. Navbar'da logo sol tarafta, navigasyon linkleri ortada, kullanıcı avatarı sağ tarafta olsun:

```html
<nav class="navbar">
  <div class="logo">DevPlatform</div>
  <ul class="nav-links">
    <li><a href="#">Ana Sayfa</a></li>
    <li><a href="#">Kurslar</a></li>
    <li><a href="#">Blog</a></li>
  </ul>
  <div class="user-avatar">
    <img src="avatar.jpg" alt="User" />
  </div>
</nav>
```

**İpucu:** `justify-content: space-between` veya üç bölümü ayrı flex-grow ile çözebilirsin.

**Çözüm:**
```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  height: 64px;
  background: #111827;
}

.nav-links {
  display: flex;
  gap: 24px;
  list-style: none;
}

.nav-links a {
  color: #d1d5db;
  text-decoration: none;
}

.nav-links a:hover {
  color: #34d399;
}

.user-avatar img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
}
```
:::

:::exercise
**Alıştırma 5: Flexbox Ortalama**

Bir login formunu sayfanın tam ortasında (hem yatay hem dikey) göstermek istiyorsun. Container'ın CSS'ini yaz.

```html
<div class="login-container">
  <form class="login-form">
    <h2>Giriş Yap</h2>
    <input type="email" placeholder="Email" />
    <input type="password" placeholder="Şifre" />
    <button type="submit">Giriş</button>
  </form>
</div>
```

**Çözüm:**
```css
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #030712;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 32px;
  background: #111827;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
}
```
:::

## CSS Grid: İki Boyutlu Layout

Grid, Flexbox'tan farklı olarak iki boyutlu (satır VE sütun) layout yapmanı sağlar.

:::concept[CSS Grid (İng: CSS Grid Layout)]
CSS Grid, iki boyutlu (satır ve sütun) layout sistemidir. Sayfa düzenini satır ve sütunlara bölerek karmaşık layout'ları basit CSS ile oluşturmayı sağlar.

**Türkçe karşılığı:** CSS Izgara Düzeni
**Ne işe yarar:** Karmaşık sayfa düzenleri, kart grid'leri, dashboard layout'ları
**Gerçek hayat benzetmesi:** Excel tablosu gibi - satırlar ve sütunlar var, hücreler birleştirilebilir, boyutları ayarlanabilir
:::

:::code[text]{title="Flexbox vs Grid: Ne Zaman Hangisi?"}
FLEXBOX (Tek Boyutlu):
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ Item │ │ Item │ │ Item │ │ Item │  → Tek satır/sütun
└──────┘ └──────┘ └──────┘ └──────┘

CSS GRID (İki Boyutlu):
┌──────┬──────┬──────┐
│ Item │ Item │ Item │  → Satır 1
├──────┼──────┼──────┤
│ Item │ Item │ Item │  → Satır 2
├──────┼──────┼──────┤
│ Item │ Item │ Item │  → Satır 3
└──────┴──────┴──────┘
  ↑ Col1  ↑ Col2  ↑ Col3

KARAR KURALI:
- Tek eksen? → Flexbox
- İki eksen? → Grid
- Navbar, card içi → Flexbox
- Sayfa layout'u, kart grid'i → Grid
- Emin değilsen → Flexbox'la başla, gerekirse Grid'e geç
:::

### Grid Container Özellikleri

:::code[css]{title="Grid Container (Parent) Özellikleri"}
.grid-container {
  display: grid;

  /* 1. grid-template-columns: Sütun tanımları */
  grid-template-columns: 200px 200px 200px;          /* 3 sabit kolon */
  grid-template-columns: 1fr 1fr 1fr;                /* 3 eşit kolon */
  grid-template-columns: 1fr 2fr 1fr;                /* Orta kolon 2x geniş */
  grid-template-columns: 250px 1fr;                  /* Sidebar + main */
  grid-template-columns: repeat(3, 1fr);             /* 3 eşit kolon (kısaltma) */
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* Responsive! */

  /* 2. grid-template-rows: Satır tanımları */
  grid-template-rows: 64px 1fr 60px;                 /* Header + main + footer */
  grid-template-rows: auto;                          /* İçeriğe göre */
  grid-template-rows: repeat(3, 200px);              /* 3 sabit satır */

  /* 3. gap: Satır ve sütun arası boşluk */
  gap: 16px;              /* Tüm yönlerde */
  gap: 16px 24px;         /* satır-arası kolon-arası */
  row-gap: 16px;
  column-gap: 24px;

  /* 4. justify-items / align-items: Hücre içi hizalama */
  justify-items: stretch;  /* Yatay (varsayılan: hücreyi doldur) */
  align-items: stretch;    /* Dikey (varsayılan: hücreyi doldur) */
  justify-items: center;   /* Her item'ı hücresinde ortala */
  align-items: center;

  /* 5. justify-content / align-content: Grid'i container içinde hizala */
  justify-content: center;
  align-content: center;
}
:::

:::deha-tip
`repeat(auto-fill, minmax(300px, 1fr))` modern CSS'in en güçlü tek satırıdır. Bu pattern, media query yazmadan responsive grid oluşturur. Ekran genişledikçe kolon ekler, daraldıkça kaldırır. YouTube, Pinterest, Airbnb gibi sitelerin kart grid'leri bu pattern ile yapılır. Bu satırı ezberle.
:::

### Grid Item Özellikleri

:::code[css]{title="Grid Item (Child) Özellikleri"}
.grid-item {
  /* 1. grid-column: Hangi kolonları kapsasın */
  grid-column: 1 / 3;        /* 1. kolondan 3. çizgiye kadar (2 kolon kapla) */
  grid-column: 1 / -1;       /* Tüm kolonları kapla */
  grid-column: span 2;       /* 2 kolon kapla (başlangıç fark etmez) */

  /* 2. grid-row: Hangi satırları kapsasın */
  grid-row: 1 / 3;           /* 2 satır kapla */
  grid-row: span 3;          /* 3 satır kapla */

  /* 3. grid-area: Kısaltma (row-start / col-start / row-end / col-end) */
  grid-area: 1 / 1 / 3 / 3;  /* 2x2 alan kapla */

  /* 4. justify-self / align-self: Bu item'ın hizalamasını override et */
  justify-self: end;
  align-self: center;
}
:::

### Grid Template Areas

:::code[css]{title="Grid Template Areas ile Sayfa Layout'u"}
.page-layout {
  display: grid;
  grid-template-columns: 250px 1fr 300px;
  grid-template-rows: 64px 1fr 60px;
  grid-template-areas:
    "header  header  header"
    "sidebar main   aside"
    "footer  footer  footer";
  min-height: 100vh;
  gap: 0;
}

.header  { grid-area: header;  background: #111827; }
.sidebar { grid-area: sidebar; background: #1f2937; }
.main    { grid-area: main;    background: #030712; }
.aside   { grid-area: aside;   background: #1f2937; }
.footer  { grid-area: footer;  background: #111827; }
:::

:::code[html]{title="Grid Template Areas HTML"}
<div class="page-layout">
  <header class="header">Header</header>
  <nav class="sidebar">Sidebar</nav>
  <main class="main">Main Content</main>
  <aside class="aside">Aside</aside>
  <footer class="footer">Footer</footer>
</div>
:::

:::exercise
**Alıştırma 6: Responsive Kart Grid'i**

Aşağıdaki HTML için CSS yaz. Kartlar responsive olsun: mobilde 1 kolon, tablette 2 kolon, desktop'ta 3 kolon. **Media query kullanmadan** çöz.

```html
<div class="card-grid">
  <div class="card">Kart 1</div>
  <div class="card">Kart 2</div>
  <div class="card">Kart 3</div>
  <div class="card">Kart 4</div>
  <div class="card">Kart 5</div>
  <div class="card">Kart 6</div>
</div>
```

**Çözüm:**
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  padding: 24px;
}

.card {
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 12px;
  padding: 24px;
  min-height: 200px;
}
```

Bu tek satır `grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))` ile:
- Ekran 300px'den küçükse: 1 kolon
- 600-900px arası: 2 kolon
- 900px+ : 3 kolon
- 1200px+ : 4 kolon (otomatik!)
:::

:::exercise
**Alıştırma 7: Dashboard Layout**

Bir dashboard layout'u oluştur: üstte tam genişlik header, solda sidebar, ortada geniş main content, sağda dar bir aside panel, altta footer. `grid-template-areas` kullan.

**Çözüm:**
```css
.dashboard {
  display: grid;
  grid-template-columns: 240px 1fr 280px;
  grid-template-rows: 64px 1fr 48px;
  grid-template-areas:
    "header  header  header"
    "sidebar main   aside"
    "footer  footer  footer";
  min-height: 100vh;
}

/* Mobilde tek kolon layout'a geç */
@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-rows: 64px auto 1fr auto 48px;
    grid-template-areas:
      "header"
      "sidebar"
      "main"
      "aside"
      "footer";
  }
}
```
:::

## Positioning: Elementlerin Konumlandırılması

:::concept[CSS Positioning (İng: CSS Positioning)]
CSS positioning, elementlerin normal sayfa akışından çıkartılarak belirli bir konuma yerleştirilmesini sağlar.

**Türkçe karşılığı:** CSS Konumlandırma
**Ne işe yarar:** Elementleri sabit menü, tooltip, modal, sticky header gibi özel konumlara yerleştirir
**Gerçek hayat benzetmesi:** Bir masadaki kağıtlar - normal sırayla dizilirler (static), ama birini alıp masanın köşesine sabitleyebilirsin (fixed), veya biraz kaydırabilirsin (relative)
:::

:::code[css]{title="Position Değerleri"}
/* 1. STATIC (Varsayılan) */
/* Normal sayfa akışında kalır. top/right/bottom/left çalışmaz. */
.static {
  position: static;
}

/* 2. RELATIVE: Kendi normal konumuna göre kaydırır */
/* Sayfa akışında yeri korunur (boşluk kalır) */
.relative {
  position: relative;
  top: 10px;     /* Aşağı 10px kayar */
  left: 20px;    /* Sağa 20px kayar */
  /* z-index kullanılabilir */
}

/* 3. ABSOLUTE: En yakın positioned parent'a göre konumlanır */
/* Sayfa akışından ÇIKAR (yer kaplamaz) */
.parent {
  position: relative; /* Absolute child'ın referans noktası */
}
.absolute {
  position: absolute;
  top: 0;
  right: 0;      /* Parent'ın sağ üst köşesi */
}

/* 4. FIXED: Viewport'a (ekrana) göre sabitlenir */
/* Scroll'da bile yerinde kalır */
.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
}

/* 5. STICKY: Normal akışta kalır, scroll'da yapışır */
.sticky-nav {
  position: sticky;
  top: 0;         /* Üst kenara ulaşınca yapışır */
  z-index: 40;
}
:::

:::warning
`position: absolute` kullandığında element normal akıştan çıkar. Parent'ında `position: relative` yoksa, element `<html>` elementine göre konumlanır ve beklenmedik sonuçlar ortaya çıkar. **Her absolute child'ın parent'ına `position: relative` eklemeyi unutma!**
:::

### Positioning Kalıpları

:::code[css]{title="Yaygın Positioning Pattern'leri"}
/* 1. Badge / Notification Dot */
.avatar-wrapper {
  position: relative;
  display: inline-block;
}
.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 12px;
  height: 12px;
  background: #ef4444;
  border-radius: 50%;
  border: 2px solid #111827;
}

/* 2. Overlay / Modal Backdrop */
.overlay {
  position: fixed;
  inset: 0;              /* top:0 right:0 bottom:0 left:0 kısaltması */
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

/* 3. Tooltip */
.tooltip-wrapper {
  position: relative;
}
.tooltip {
  position: absolute;
  bottom: 100%;          /* Elementin üstüne yerleş */
  left: 50%;
  transform: translateX(-50%); /* Tam ortala */
  padding: 8px 12px;
  background: #374151;
  border-radius: 6px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}
.tooltip-wrapper:hover .tooltip {
  opacity: 1;
}

/* 4. Sticky Sidebar */
.sidebar-content {
  position: sticky;
  top: 80px;             /* Header yüksekliği + biraz boşluk */
  max-height: calc(100vh - 80px);
  overflow-y: auto;
}
:::

:::exercise
**Alıştırma 8: Notification Badge**

Bir kullanıcı avatarının sağ üst köşesine kırmızı bildirim noktası (badge) ekle:

```html
<div class="avatar-container">
  <img src="avatar.jpg" alt="User" class="avatar" />
  <span class="notification-badge">3</span>
</div>
```

**Çözüm:**
```css
.avatar-container {
  position: relative;
  display: inline-block;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

.notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 20px;
  height: 20px;
  background: #ef4444;
  color: white;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  padding: 0 6px;
  border: 2px solid #111827;
}
```
:::

## Responsive Design: Farklı Ekranlara Uyum

:::concept[Responsive Design (İng: Responsive Web Design)]
Responsive design, web sayfalarının farklı ekran boyutlarında (mobil, tablet, desktop) düzgün görünmesini sağlayan tasarım yaklaşımıdır.

**Türkçe karşılığı:** Duyarlı Tasarım
**Ne işe yarar:** Aynı web sitesinin telefonda, tablette ve bilgisayarda düzgün görünmesini sağlar
**Gerçek hayat benzetmesi:** Su gibi - hangi kaba koyarsan onun şeklini alır
:::

### Mobile-First Yaklaşımı

:::code[css]{title="Mobile-First Media Queries"}
/* Mobile-First: Önce mobil tasarla, sonra büyük ekranlar için ekle */

/* Temel stiller (mobil - 320px+) */
.container {
  padding: 16px;
  max-width: 100%;
}

.card-grid {
  display: grid;
  grid-template-columns: 1fr; /* Mobilde tek kolon */
  gap: 16px;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    max-width: 768px;
    margin: 0 auto;
  }

  .card-grid {
    grid-template-columns: repeat(2, 1fr); /* 2 kolon */
    gap: 24px;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }

  .card-grid {
    grid-template-columns: repeat(3, 1fr); /* 3 kolon */
  }
}

/* Geniş Desktop (1280px+) */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }

  .card-grid {
    grid-template-columns: repeat(4, 1fr); /* 4 kolon */
  }
}
:::

:::must-note
**MUTLAKA NOT AL:** Mobile-first yaklaşımda `min-width` kullan. Desktop-first yaklaşımda `max-width` kullan. Tailwind CSS mobile-first kullanır: `sm:`, `md:`, `lg:`, `xl:` prefix'leri `min-width` media query'lere karşılık gelir. Sektör standardı mobile-first'tür.
:::

### Responsive Birimler

:::code[css]{title="CSS Birimleri ve Kullanım Alanları"}
/* PX: Sabit piksel - border, shadow, küçük spacing */
border: 1px solid #374151;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);

/* REM: Root font-size'a göre (genelde 16px) */
/* Accessibility için font-size'da rem kullan */
font-size: 1rem;      /* 16px */
font-size: 0.875rem;  /* 14px */
font-size: 1.25rem;   /* 20px */
padding: 1.5rem;      /* 24px */

/* EM: Parent font-size'a göre (iç içe sorun yaratabilir) */
/* Genelde padding/margin'de kullanılır */
.button {
  font-size: 1rem;
  padding: 0.5em 1em;  /* Font boyutuna orantılı */
}

/* % : Parent'a göre yüzde */
.child { width: 50%; }   /* Parent genişliğinin yarısı */

/* VW/VH: Viewport genişlik/yükseklik */
.hero { height: 100vh; }         /* Tam ekran yüksekliği */
.full-width { width: 100vw; }    /* Tam ekran genişliği */
font-size: clamp(1rem, 2.5vw, 3rem); /* Responsive font */

/* FR: Grid'de fraction (kesir) birimi */
grid-template-columns: 1fr 2fr;  /* 1/3 ve 2/3 oran */

/* CH: Karakter genişliği - Metin okunabilirliği */
.article { max-width: 65ch; }    /* İdeal satır uzunluğu */

/* CLAMP: min, ideal, max - Responsive değerler */
font-size: clamp(1rem, 2vw + 0.5rem, 2rem);
width: clamp(300px, 50%, 800px);
padding: clamp(16px, 4vw, 48px);
:::

:::deha-tip
`clamp()` fonksiyonu modern CSS'in en güçlü araçlarından biri. `clamp(min, ideal, max)` yapısıyla media query yazmadan responsive değerler oluşturabilirsin. Özellikle `font-size` ve `padding` için harika. `font-size: clamp(1rem, 2.5vw, 3rem)` yazarsan, font küçük ekranda 1rem'den küçük olmaz, büyük ekranda 3rem'den büyük olmaz, aradaki değerlerde viewport'a orantılı büyür.
:::

:::exercise
**Alıştırma 9: Responsive Hero Section**

Bir landing page hero section'ı tasarla. Mobilde dikey (metin üstte, resim altta), desktop'ta yatay (metin solda, resim sağda) olsun. Mobile-first yaklaşım kullan.

```html
<section class="hero">
  <div class="hero-content">
    <h1>Modern Web Geliştirme</h1>
    <p>Full stack developer olmak için gereken her şey.</p>
    <button class="cta-button">Hemen Başla</button>
  </div>
  <div class="hero-image">
    <img src="hero.jpg" alt="Hero" />
  </div>
</section>
```

**Çözüm:**
```css
.hero {
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding: clamp(24px, 5vw, 64px);
  min-height: 80vh;
  align-items: center;
  justify-content: center;
}

.hero-content {
  text-align: center;
}

.hero h1 {
  font-size: clamp(1.75rem, 4vw, 3.5rem);
  color: #f9fafb;
  margin-bottom: 16px;
}

.hero p {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: #9ca3af;
  margin-bottom: 24px;
}

.hero-image img {
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
}

@media (min-width: 768px) {
  .hero {
    flex-direction: row;
    text-align: left;
  }

  .hero-content {
    flex: 1;
    text-align: left;
  }

  .hero-image {
    flex: 1;
  }
}
```
:::

:::exercise
**Alıştırma 10: Responsive Navigation**

Bir responsive navbar yap. Desktop'ta yatay linkler göster, mobilde hamburger menü ikonu göster (JS olmadan sadece CSS ile menüyü aç/kapa - checkbox hack kullan).

```html
<nav class="responsive-nav">
  <div class="nav-brand">Logo</div>
  <input type="checkbox" id="nav-toggle" class="nav-toggle" />
  <label for="nav-toggle" class="nav-toggle-label">
    <span></span>
  </label>
  <ul class="nav-menu">
    <li><a href="#">Ana Sayfa</a></li>
    <li><a href="#">Hakkında</a></li>
    <li><a href="#">İletişim</a></li>
  </ul>
</nav>
```

**Çözüm:**
```css
.responsive-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  padding: 0 24px;
  height: 64px;
  background: #111827;
}

.nav-brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #f9fafb;
}

.nav-toggle {
  display: none; /* Checkbox'ı gizle */
}

.nav-toggle-label {
  display: none; /* Desktop'ta hamburger gizli */
  cursor: pointer;
}

.nav-toggle-label span,
.nav-toggle-label span::before,
.nav-toggle-label span::after {
  display: block;
  width: 24px;
  height: 2px;
  background: #d1d5db;
  position: relative;
}

.nav-toggle-label span::before,
.nav-toggle-label span::after {
  content: '';
  position: absolute;
}

.nav-toggle-label span::before { top: -7px; }
.nav-toggle-label span::after { top: 7px; }

.nav-menu {
  display: flex;
  gap: 24px;
  list-style: none;
}

.nav-menu a {
  color: #d1d5db;
  text-decoration: none;
}

/* Mobil */
@media (max-width: 767px) {
  .nav-toggle-label {
    display: block;
  }

  .nav-menu {
    display: none;
    flex-direction: column;
    width: 100%;
    padding: 16px 0;
    gap: 16px;
  }

  .nav-toggle:checked ~ .nav-menu {
    display: flex;
  }
}
```
:::

## İleri Seviye CSS Konuları

### CSS Custom Properties (Variables)

:::code[css]{title="CSS Değişkenleri (Custom Properties)"}
/* Değişkenleri tanımla */
:root {
  /* Renkler */
  --color-bg-primary: #030712;
  --color-bg-secondary: #111827;
  --color-bg-tertiary: #1f2937;
  --color-text-primary: #f9fafb;
  --color-text-secondary: #d1d5db;
  --color-text-muted: #9ca3af;
  --color-accent: #34d399;
  --color-accent-hover: #6ee7b7;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
}

/* Değişkenleri kullan */
.card {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  transition: transform var(--transition-normal);
}

.card:hover {
  transform: translateY(-2px);
}

/* Fallback değer */
.element {
  color: var(--color-accent, #34d399);
}

/* Component seviyesinde override */
.card--featured {
  --color-accent: #3b82f6; /* Bu card'da accent mavi olur */
}
:::

### Geçiş ve Animasyonlar (Transitions & Animations)

:::code[css]{title="CSS Transitions"}
/* Temel Transition */
.button {
  background: #059669;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  /* Veya spesifik property'ler: */
  transition: background 0.2s ease, transform 0.15s ease;
}

.button:hover {
  background: #047857;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
}

.button:active {
  transform: translateY(0);
}

/* Card Hover Efekti */
.card {
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 12px;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
  border-color: #4b5563;
}
:::

:::code[css]{title="CSS Animations"}
/* Keyframes tanımla */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Animasyon uygula */
.card {
  animation: fadeIn 0.3s ease forwards;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #374151;
  border-top-color: #34d399;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.skeleton {
  background: linear-gradient(
    90deg,
    #1f2937 25%,
    #374151 50%,
    #1f2937 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
:::

:::exercise
**Alıştırma 11: Loading Spinner**

Sadece CSS ile bir loading spinner oluştur. Yeşil renkli, dönen bir halka olsun.

**Çözüm:**
```css
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #374151;
  border-top-color: #34d399;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```
:::

:::exercise
**Alıştırma 12: Skeleton Loading**

İçerik yüklenirken gösterilecek bir skeleton loading kartı oluştur. Üstte büyük dikdörtgen (resim placeholder), altında 2 satır metin placeholder olsun. Shimmer animasyonu ekle.

**Çözüm:**
```css
.skeleton-card {
  background: #1f2937;
  border-radius: 12px;
  padding: 16px;
  overflow: hidden;
}

.skeleton-image {
  height: 180px;
  border-radius: 8px;
}

.skeleton-text {
  height: 16px;
  border-radius: 4px;
  margin-top: 12px;
}

.skeleton-text:last-child {
  width: 60%;
}

.skeleton-image,
.skeleton-text {
  background: linear-gradient(
    90deg,
    #374151 25%,
    #4b5563 50%,
    #374151 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```
:::

## Interview Soruları

:::interview
**Soru 1:** CSS Specificity nedir ve nasıl hesaplanır?
**Cevap:** Specificity, birden fazla CSS kuralı aynı elemente uygulandığında hangisinin kazanacağını belirleyen puanlama sistemidir. Üç seviyeli bir puanlama var: ID seçiciler (1-0-0), class/attribute/pseudo-class seçiciler (0-1-0), element/pseudo-element seçiciler (0-0-1). Inline style her şeyi yener, `!important` ise en yüksek önceliğe sahiptir ama kullanımı önerilmez.

**Soru 2:** Box Model nedir? `box-sizing: border-box` ne yapar?
**Cevap:** Box Model, her HTML elementinin content, padding, border ve margin katmanlarından oluşan yapısıdır. Varsayılan `content-box`'ta width/height sadece content alanını kapsar, padding ve border eklendikçe element büyür. `border-box`'ta ise width/height padding ve border dahil toplam boyutu belirler, content alanı otomatik küçülür. Modern projelerde `border-box` standart olarak kullanılır.

**Soru 3:** Flexbox ile Grid arasındaki fark nedir? Ne zaman hangisini kullanırsın?
**Cevap:** Flexbox tek boyutlu layout sistemidir (ya satır ya sütun). Grid iki boyutlu layout sistemidir (satır VE sütun aynı anda). Navbar, card içi layout, tek sıra butonlar gibi tek eksen ihtiyaçlarında Flexbox; sayfa layout'u, kart grid'leri, dashboard gibi iki eksen ihtiyaçlarında Grid kullanırım. Pratikte ikisi birlikte kullanılır: Grid ile sayfa layout'u, Flexbox ile component layout'u.

**Soru 4:** `position: sticky` ne yapar? `fixed`'den farkı nedir?
**Cevap:** `sticky`, element scroll ile belirli bir eşiğe ulaşana kadar normal akışta kalır, eşiğe ulaşınca yapışır. `fixed` ise her zaman viewport'a göre sabit kalır ve normal akıştan çıkar (yer kaplamaz). Sticky, parent container'ı terk etmez; fixed viewport'a bağlıdır. Sticky header, table header'ları gibi yerlerde kullanılır.

**Soru 5:** Mobile-first nedir ve neden tercih edilir?
**Cevap:** Mobile-first, CSS'i önce mobil cihazlar için yazıp, sonra `min-width` media query'lerle büyük ekranlar için özelleştirmektir. Tercih edilme sebepleri: performans (mobilde gereksiz CSS yüklenmez), önceliklendirme (en önemli içerik önce tasarlanır), bakım kolaylığı (daha az override). Tailwind CSS dahil modern framework'ler mobile-first kullanır.
:::

:::ai-guidance
**AI ile Pratik Yapma Rehberi:**

1. **Layout Challenge:** AI'dan "Şu web sitesinin layout'unu CSS ile yeniden oluştur" diye iste. Herhangi bir site URL'si ver ve AI sana adım adım CSS yazma konusunda yardımcı olsun.

2. **Specificity Quiz:** AI'dan rastgele CSS seçici specificity soruları sor. "Bana 5 tane specificity sorusu ver" de ve çöz.

3. **Debug Pratiği:** AI'ya "Şu CSS neden çalışmıyor?" diye hatalı kodlar gönder. AI sana hatayı bulsun ve nedenini açıklasın.

4. **Responsive Challenge:** AI'dan "Şu desktop tasarımı mobilde nasıl görünmeli?" diye sor. Mobile-first CSS yazma pratiği yap.

5. **Code Review:** Kendi yazdığın CSS'i AI'ya gönder ve "Senior bir developer bu CSS hakkında ne der?" diye sor. AI sana best practice önerileri verecektir.
:::

:::senior-learns
Senior/CTO CSS öğrenirken, rendering pipeline'ı anlar. CSS property'leri 3 kategoride maliyete sahiptir:
- **Layout (reflow):** width, height, margin, padding, display, position - EN pahalı, tüm layout yeniden hesaplanır
- **Paint:** color, background, border-radius, box-shadow - Orta maliyet, piksel boyama yeniden yapılır
- **Composite:** transform, opacity - EN ucuz, GPU hızlandırmalı, sadece katman birleştirme

Bu yüzden animasyonlarda `transform` ve `opacity` kullan, `width`/`height`/`margin` animasyonu yapma. `will-change: transform` ile GPU katmanı oluştur. Chrome DevTools > Performance tab ile rendering süresini ölç.
:::

## Özet ve Yol Haritası

Bu derste CSS'in temellerini öğrendin:

1. **Selectors & Specificity** - CSS kurallarının öncelik sistemi
2. **Box Model** - Content, padding, border, margin katmanları
3. **Display Types** - Block, inline, inline-block, flex, grid
4. **Flexbox** - Tek boyutlu layout (navbar, card, centering)
5. **CSS Grid** - İki boyutlu layout (sayfa layout'u, kart grid'leri)
6. **Positioning** - Static, relative, absolute, fixed, sticky
7. **Responsive Design** - Mobile-first, media queries, modern birimler
8. **CSS Variables** - Tema ve design token yönetimi
9. **Transitions & Animations** - Hover efektleri, loading spinner'lar

Bir sonraki adım: **HTML Semantic** dersinde HTML'in yapısal elemanlarını, ardından **CSS Layout** dersinde bu bilgileri gerçek proje layout'larına uygulayacaksın. Son olarak **Tailwind CSS** ile bu tüm CSS bilgisini utility-first yaklaşımla nasıl hızlıca uygulayacağını öğreneceksin.
