---
title: "Semantic HTML5 ve Erişilebilirlik"
id: "mod-06-css/lesson-01"
estimated_minutes: 45
order: 1
tags: ["html5", "semantic", "accessibility", "seo", "aria", "forms"]
prerequisites: ["mod-01-internet/lesson-01"]
---

# Semantic HTML5 ve Erişilebilirlik

:::realworld
Bir web sayfası sadece "gözle güzel görünen" bir şey değil. Ekran okuyucu kullanan görme engelli bir kullanıcı, Google'ın sayfanı tarayan bot'u ve klavyeyle gezinen bir kullanıcı - hepsi aynı HTML'i farklı şekillerde tüketir. Semantic HTML yazmak, sayfanın hem insanlar hem de makineler tarafından anlaşılmasını sağlar. Bu ders, profesyonel seviyede HTML yazmayı, erişilebilirlik standartlarını ve SEO temellerini kapsar. Senior developer'ların "bu HTML'i kim yazdı?" diye sormayacağı kod yazacak seviyeye geleceksin.
:::

## Neden Semantic HTML?

Çoğu yeni başlayan developer her yere `<div>` ve `<span>` koyar. Ama bu yaklaşım ciddi sorunlar yaratır:

- **Erişilebilirlik:** Ekran okuyucular sayfanın yapısını anlayamaz
- **SEO:** Google, sayfanın hangi kısmının ana içerik olduğunu bilemez
- **Bakım:** 6 ay sonra kendi kodunu okuyamazsın
- **Performans:** Tarayıcı, sayfayı daha verimli render edemez

:::deha-tip
Deha seviyesi developer'lar HTML'i "belge yapısı" olarak düşünür, "görsel tasarım" olarak değil. Önce doğru HTML yapısını kurar, sonra CSS ile görselleştirir. Bu yaklaşıma "content-first development" denir ve büyük projelerde bakım maliyetini dramatik şekilde düşürür.
:::

## Semantic HTML5 Elemanları

### Sayfa Yapısı Elemanları

:::code[html]{title="Semantic Sayfa Yapısı"}
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sayfa Başlığı</title>
</head>
<body>
  <header>
    <nav aria-label="Ana Navigasyon">
      <ul>
        <li><a href="/">Ana Sayfa</a></li>
        <li><a href="/hakkinda">Hakkında</a></li>
        <li><a href="/iletisim">İletişim</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <h1>Makale Başlığı</h1>
      <section>
        <h2>Bölüm 1</h2>
        <p>İçerik buraya gelir.</p>
      </section>
      <section>
        <h2>Bölüm 2</h2>
        <p>Başka bir içerik bölümü.</p>
      </section>
    </article>

    <aside aria-label="İlgili Bağlantılar">
      <h2>İlgili Yazılar</h2>
      <ul>
        <li><a href="/yazi-1">Yazı 1</a></li>
        <li><a href="/yazi-2">Yazı 2</a></li>
      </ul>
    </aside>
  </main>

  <footer>
    <p>&copy; 2026 Şirket Adı</p>
  </footer>
</body>
</html>
:::

:::concept[Semantic Elements (İng: Semantic Elements)]
Semantic elemanlar, içeriklerinin anlamını tarayıcıya ve geliştiricilere bildiren HTML elemanlarıdır.

**Türkçe karşılığı:** Anlamsal Elemanlar
**Ne işe yarar:** İçeriğin yapısını ve amacını tanımlar
**Gerçek hayat benzetmesi:** Bir gazetedeki sütunlar gibi - manşet, ana haber, köşe yazısı, reklam alanı hepsi farklı bölümlerde ve herkes hangisinin ne olduğunu anlar
:::

### Her Elemanın Görevi

:::comparison
| Eleman | Kullanım Amacı | Ne Zaman Kullan |
|--------|---------------|-----------------|
| `<header>` | Sayfa veya bölüm başlığı, logo, navigasyon | Sayfanın üst kısmı, article başlığı |
| `<nav>` | Navigasyon bağlantıları | Ana menü, breadcrumb, sayfa içi linkler |
| `<main>` | Sayfanın ana içeriği (tek olmalı) | Sayfa başına yalnızca BİR tane |
| `<article>` | Bağımsız, kendi başına anlamlı içerik | Blog yazısı, haber, ürün kartı |
| `<section>` | Tematik gruplandırma | İçeriğin alt bölümleri |
| `<aside>` | Ana içerikle dolaylı ilişkili içerik | Sidebar, ilgili yazılar, reklam |
| `<footer>` | Sayfa veya bölüm alt bilgisi | Copyright, iletişim, sosyal medya |
| `<figure>` | Resim, grafik, kod bloğu + açıklama | Resim + alt yazı birlikte |
| `<time>` | Tarih/saat bilgisi | Yayın tarihi, etkinlik zamanı |

**Kural:** `<div>` sadece başka semantic eleman uygun olmadığında kullan!
:::

:::beginner-mistake
Yaygın hata: `<div class="header">` yazmak. Bunun yerine doğrudan `<header>` kullan. Aynı şekilde `<div class="nav">` yerine `<nav>`, `<div class="footer">` yerine `<footer>` kullan. Semantic elemanlar zaten bu anlamları taşır ve ekran okuyucular bunları otomatik tanır.
:::

## ARIA Roles ve Erişilebilirlik (Accessibility)

:::concept[ARIA (Accessible Rich Internet Applications)]
ARIA, HTML elemanlarına ek anlam ve davranış bilgisi ekleyen attribute'lar setidir. Özellikle dinamik içerik ve özel UI bileşenleri için erişilebilirliği artırır.

**Türkçe karşılığı:** Erişilebilir Zengin İnternet Uygulamaları
**Ne işe yarar:** Ekran okuyucular ve yardımcı teknolojiler için ek bağlam sağlar
**Gerçek hayat benzetmesi:** Bir binadaki Braille tabelalar gibi - görme engelli kişilerin binada yollarını bulmasını sağlar
:::

### Temel ARIA Attribute'ları

:::code[html]{title="ARIA Kullanım Örnekleri"}
<!-- aria-label: Görsel olmayan açıklama -->
<button aria-label="Menüyü aç">
  <svg><!-- hamburger icon --></svg>
</button>

<!-- aria-labelledby: Başka bir elemana referans -->
<h2 id="search-title">Ürün Ara</h2>
<input type="search" aria-labelledby="search-title">

<!-- aria-describedby: Ek açıklama -->
<input type="password" aria-describedby="pw-hint">
<span id="pw-hint">En az 8 karakter, 1 büyük harf</span>

<!-- aria-hidden: Ekran okuyucudan gizle -->
<span aria-hidden="true">🎉</span>
<span>Tebrikler!</span>

<!-- aria-live: Dinamik içerik değişikliğini duyur -->
<div aria-live="polite" role="status">
  3 yeni mesaj var
</div>

<!-- aria-expanded: Açılır menü durumu -->
<button aria-expanded="false" aria-controls="menu">
  Kategoriler
</button>
<ul id="menu" hidden>
  <li>Elektronik</li>
  <li>Giyim</li>
</ul>

<!-- role: Elemanın rolünü belirt -->
<div role="alert">Hata: Geçersiz email adresi</div>
<div role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
  %75 tamamlandı
</div>
:::

### Klavye Navigasyonu

:::code[html]{title="Klavye Erişilebilirliği"}
<!-- tabindex: Tab sırasını kontrol et -->
<div tabindex="0">Bu div'e tab ile ulaşılabilir</div>
<div tabindex="-1">Programatik olarak focus edilebilir ama tab sırasında değil</div>

<!-- Skip navigation link -->
<a href="#main-content" class="skip-link">
  Ana içeriğe atla
</a>
<!-- ... header ve nav ... -->
<main id="main-content">
  <!-- ana içerik -->
</main>

<!-- Özel buton erişilebilirliği -->
<div role="button" tabindex="0"
     onkeydown="if(event.key==='Enter'||event.key===' ') this.click()">
  Özel Buton
</div>
<!-- DAHA İYİSİ: Doğrudan <button> kullan! -->
<button>Doğru Buton</button>
:::

:::tip
Erişilebilirlik kuralı #1: Eğer bir HTML elemanı zaten istediğin davranışa sahipse (button, a, input), onu kullan. Bir `<div>`'i butona çevirmeye çalışma. Native HTML elemanları klavye, focus ve ekran okuyucu desteğini otomatik sağlar.
:::

## SEO Temelleri

### Meta Tags ve Open Graph

:::code[html]{title="SEO için Meta Tags"}
<head>
  <!-- Temel Meta Tags -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Bu sayfa hakkında 150-160 karakter açıklama.
    Google arama sonuçlarında bu metin görünür.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://example.com/sayfa">
  <title>Sayfa Başlığı | Site Adı</title>

  <!-- Open Graph (Facebook, LinkedIn) -->
  <meta property="og:title" content="Paylaşım Başlığı">
  <meta property="og:description" content="Paylaşıldığında görünecek açıklama">
  <meta property="og:image" content="https://example.com/image.jpg">
  <meta property="og:url" content="https://example.com/sayfa">
  <meta property="og:type" content="article">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Twitter Başlığı">
  <meta name="twitter:description" content="Twitter açıklaması">
  <meta name="twitter:image" content="https://example.com/image.jpg">
</head>
:::

### Structured Data (JSON-LD)

:::code[html]{title="JSON-LD Structured Data"}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Semantic HTML5 Rehberi",
  "author": {
    "@type": "Person",
    "name": "Yazar Adı"
  },
  "datePublished": "2026-03-20",
  "image": "https://example.com/resim.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Site Adı",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
</script>
:::

:::concept[Structured Data (İng: Structured Data)]
Structured Data, arama motorlarının sayfa içeriğini daha iyi anlamasını sağlayan makine tarafından okunabilir veri formatıdır.

**Türkçe karşılığı:** Yapılandırılmış Veri
**Ne işe yarar:** Google'da zengin sonuçlar (rich snippets) elde etmeni sağlar - yıldız puanı, fiyat, tarih gibi bilgiler arama sonuçlarında görünür
**Gerçek hayat benzetmesi:** Bir kitabın arka kapağındaki ISBN, yazar, yayınevi bilgileri gibi - makine tarafından okunabilir metadata
:::

### Heading Hiyerarşisi

:::code[html]{title="Doğru Heading Yapısı"}
<!-- YANLIŞ: Heading sırası atlanmış -->
<h1>Ana Başlık</h1>
<h3>Alt başlık</h3>  <!-- h2 atlandı! -->
<h5>Detay</h5>       <!-- h3, h4 atlandı! -->

<!-- DOĞRU: Sıralı heading hiyerarşisi -->
<h1>Ana Başlık</h1>
  <h2>Bölüm 1</h2>
    <h3>Alt Bölüm 1.1</h3>
    <h3>Alt Bölüm 1.2</h3>
  <h2>Bölüm 2</h2>
    <h3>Alt Bölüm 2.1</h3>
:::

:::beginner-mistake
Yaygın hata: Heading etiketlerini font büyüklüğü için kullanmak. `<h3>` sadece daha küçük yazı istediğin için değil, gerçekten üçüncü seviye başlık olduğu için kullanılır. Font büyüklüğü için CSS kullan, heading'ler belge yapısı içindir.
:::

## Form Best Practices

:::code[html]{title="Erişilebilir Form Örneği"}
<form action="/kayit" method="POST" novalidate>
  <!-- Her input'un label'ı olmalı -->
  <div>
    <label for="email">Email Adresi</label>
    <input
      type="email"
      id="email"
      name="email"
      required
      autocomplete="email"
      placeholder="örnek@mail.com"
      aria-describedby="email-help"
    >
    <small id="email-help">Kurumsal email tercih edin</small>
  </div>

  <div>
    <label for="password">Şifre</label>
    <input
      type="password"
      id="password"
      name="password"
      required
      minlength="8"
      autocomplete="new-password"
      aria-describedby="pw-rules"
    >
    <small id="pw-rules">En az 8 karakter, 1 büyük harf, 1 rakam</small>
  </div>

  <!-- HTML5 Input Tipleri -->
  <div>
    <label for="tel">Telefon</label>
    <input type="tel" id="tel" name="tel" pattern="[0-9]{10}">
  </div>

  <div>
    <label for="birthday">Doğum Tarihi</label>
    <input type="date" id="birthday" name="birthday">
  </div>

  <div>
    <label for="website">Web Sitesi</label>
    <input type="url" id="website" name="website" placeholder="https://">
  </div>

  <div>
    <label for="age">Yaş Aralığı</label>
    <input type="range" id="age" name="age" min="18" max="65" value="25">
  </div>

  <div>
    <label for="color">Tema Rengi</label>
    <input type="color" id="color" name="color" value="#3b82f6">
  </div>

  <!-- Fieldset ile gruplandırma -->
  <fieldset>
    <legend>Bildirim Tercihleri</legend>
    <label>
      <input type="checkbox" name="notif" value="email"> Email
    </label>
    <label>
      <input type="checkbox" name="notif" value="sms"> SMS
    </label>
    <label>
      <input type="checkbox" name="notif" value="push"> Push
    </label>
  </fieldset>

  <button type="submit">Kayıt Ol</button>
</form>
:::

### HTML5 Validation Attribute'ları

:::comparison
| Attribute | Açıklama | Örnek |
|-----------|----------|-------|
| `required` | Zorunlu alan | `<input required>` |
| `minlength` / `maxlength` | Metin uzunluğu limiti | `minlength="3" maxlength="50"` |
| `min` / `max` | Sayı veya tarih aralığı | `min="0" max="100"` |
| `pattern` | Regex pattern | `pattern="[0-9]{3}"` |
| `type="email"` | Email formatı kontrolü | Otomatik @ kontrolü |
| `type="url"` | URL formatı kontrolü | Otomatik http:// kontrolü |
| `step` | Sayı artış miktarı | `step="0.01"` (kuruş hassasiyeti) |
| `autocomplete` | Tarayıcı otomatik doldurma ipucu | `autocomplete="email"` |

**Not:** `novalidate` attribute'u form'a eklenirse HTML validation devre dışı kalır. Bu, JavaScript ile custom validation yapacağın zaman kullanışlıdır.
:::

## HTML5 APIs

### localStorage ve sessionStorage

:::code[javascript]{title="Web Storage API"}
// localStorage: Tarayıcı kapatılsa bile kalır
localStorage.setItem('theme', 'dark');
const theme = localStorage.getItem('theme'); // 'dark'
localStorage.removeItem('theme');
localStorage.clear(); // Tüm verileri sil

// sessionStorage: Sekme kapatılınca silinir
sessionStorage.setItem('tempData', JSON.stringify({ step: 3 }));
const data = JSON.parse(sessionStorage.getItem('tempData'));

// Storage event: Diğer sekmelerdeki değişiklikleri dinle
window.addEventListener('storage', (e) => {
  console.log(`${e.key} değişti: ${e.oldValue} → ${e.newValue}`);
});
:::

### Geolocation API

:::code[javascript]{title="Geolocation API"}
// Kullanıcının konumunu al (izin gerektirir)
if ('geolocation' in navigator) {
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      console.log(`Konum: ${latitude}, ${longitude}`);
    },
    (error) => {
      switch (error.code) {
        case error.PERMISSION_DENIED:
          console.log('Kullanıcı konum iznini reddetti');
          break;
        case error.POSITION_UNAVAILABLE:
          console.log('Konum bilgisi alınamıyor');
          break;
        case error.TIMEOUT:
          console.log('Konum isteği zaman aşımına uğradı');
          break;
      }
    },
    { enableHighAccuracy: true, timeout: 5000 }
  );
}
:::

### Canvas API (Genel Bakış)

:::code[html]{title="Canvas API Temel Kullanım"}
<canvas id="myCanvas" width="400" height="300"></canvas>

<script>
const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');

// Dikdörtgen çiz
ctx.fillStyle = '#3b82f6';
ctx.fillRect(50, 50, 200, 100);

// Metin yaz
ctx.font = '20px Arial';
ctx.fillStyle = '#000';
ctx.fillText('Merhaba Canvas!', 70, 110);

// Çizgi çiz
ctx.beginPath();
ctx.moveTo(50, 200);
ctx.lineTo(350, 200);
ctx.strokeStyle = '#ef4444';
ctx.lineWidth = 3;
ctx.stroke();
</script>
:::

### Web Workers (Genel Bakış)

:::code[javascript]{title="Web Worker Temel Kullanım"}
// main.js - Ana thread
const worker = new Worker('worker.js');

worker.postMessage({ data: [1, 2, 3, 4, 5], operation: 'sum' });

worker.onmessage = (e) => {
  console.log('Worker sonucu:', e.data); // 15
};

worker.onerror = (e) => {
  console.error('Worker hatası:', e.message);
};

// worker.js - Arka plan thread
self.onmessage = (e) => {
  const { data, operation } = e.data;
  let result;

  if (operation === 'sum') {
    result = data.reduce((acc, val) => acc + val, 0);
  }

  self.postMessage(result);
};
:::

:::concept[Web Workers (İng: Web Workers)]
Web Workers, JavaScript kodunu ana thread'den (UI thread) ayrı bir arka plan thread'inde çalıştırmayı sağlar.

**Türkçe karşılığı:** Web İşçileri / Arka Plan İş Parçacıkları
**Ne işe yarar:** Ağır hesaplamalar ana thread'i bloklamaz, UI donmaz
**Gerçek hayat benzetmesi:** Bir restoranda garson (ana thread) siparişleri alırken, mutfak (worker) yemekleri hazırlar. Garson mutfakta yemek pişirmeye kalkarsa müşteriler bekler.
:::

:::tip
HTML5 API'leri hakkında şunu unutma: localStorage'da hassas veri (token, şifre) saklamak güvenlik açığıdır. Bunun yerine httpOnly cookie'ler kullan. localStorage sadece tema tercihi, dil seçimi gibi hassas olmayan veriler için uygundur.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Semantik HTML ile Sayfa Yapisi (Kolay)

Bir kisisel portfoy sayfasinin HTML iskeletini semantik etiketler kullanarak oluştur. `div` yerine anlamli HTML5 etiketleri kullan.

```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portfoyum</title>
</head>
<body>
  <!-- TODO: Asagidaki yapida DIV yerine dogru semantik etiketleri kullan -->

  <!-- Navigasyon: nav -->
  <div class="navigation">
    <div class="logo">Ahmet Y.</div>
    <div class="menu">
      <a href="#about">Hakkimda</a>
      <a href="#projects">Projeler</a>
      <a href="#contact">Iletisim</a>
    </div>
  </div>

  <!-- Ana icerik: main, section, article -->
  <div class="main-content">
    <div class="about-section" id="about">
      <div class="section-title">Hakkimda</div>
      <div class="text">Junior Full-Stack Developer</div>
    </div>

    <div class="projects-section" id="projects">
      <div class="section-title">Projeler</div>
      <!-- Her proje bir article olmali -->
      <div class="project">
        <div class="project-title">E-Ticaret Sitesi</div>
        <div class="project-date">Mart 2026</div>
        <div class="description">React + Node.js ile gelismis e-ticaret</div>
      </div>
    </div>
  </div>

  <!-- Alt bilgi: footer -->
  <div class="footer">
    <div class="copyright">2026 Ahmet Y.</div>
  </div>
</body>
</html>

<!-- DOGRU CEVAP icin her div'i su etiketlerle degistir:
nav, header, main, section, article, h1, h2, p, time, footer, small -->
```

**Beklenen Sonuc:** Sayfada hicbir gereksiz `div` kalmamali. Lighthouse Accessibility skoru 90+ olmali. Ekran okuyucu ile gezindiginde anlamli bir yapi sunmali.
**Ipucu:** `header` sayfa veya section basligini, `nav` navigasyonu, `main` ana icerigi, `article` bagimsiz icerigi, `section` tematik gruplari temsil eder.

---

### Alistirma 2: Erisilebilir Form Oluşturma (Orta)

HTML5 input type'lari, ARIA attribute'leri ve form validasyonu kullanarak erisilebilir bir iletisim formu oluştur.

```html
<!-- TODO: Bu formu tamamla -->
<form id="contact-form" novalidate>
  <!-- Her input icin label olmali (for + id eslesmesi) -->
  <div class="form-group">
    <label for="name">Ad Soyad *</label>
    <input
      type="text"
      id="name"
      name="name"
      required
      minlength="2"
      maxlength="50"
      aria-required="true"
      aria-describedby="name-help"
    />
    <small id="name-help">En az 2 karakter girin</small>
  </div>

  <!-- TODO: Email alani ekle (type="email", required) -->
  <!-- TODO: Telefon alani ekle (type="tel", pattern ile format belirt) -->
  <!-- TODO: Konu secimi ekle (select ile 3-4 secenek) -->
  <!-- TODO: Mesaj alani ekle (textarea, minlength="10") -->

  <!-- TODO: Checkbox — KVKK onayi (required) -->
  <div class="form-group">
    <input type="checkbox" id="consent" required aria-required="true" />
    <label for="consent">KVKK metnini okudum ve onayliyorum *</label>
  </div>

  <button type="submit">Gonder</button>
</form>

<script>
// TODO: Form validasyonu yaz
// - Bos alan kontrolu
// - Email format kontrolu
// - Hata mesajlarini aria-live="polite" ile duyur
// - Basarili gonderimde tesekkur mesaji goster
document.getElementById("contact-form").addEventListener("submit", (e) => {
  e.preventDefault();
  // Validation logic...
});
</script>
```

**Beklenen Sonuc:** Tab ile tum form elemanlarina ulasabilmeli. Hata mesajlari ekran okuyucu tarafindan okunabilmeli. HTML5 native validasyon calisirken, JavaScript ile ek kontrol de yapilmali.
**Ipucu:** `aria-describedby` ile yardim metinlerini input'a bagla. `aria-invalid="true"` ile hatali alanlari isaretleyin.

---

### Alistirma 3: Accessibility Audit ve Tab Navigation (Zor)

Bir web sayfasinin erisebilirligini test et: Lighthouse audit, Tab navigasyonu ve ekran okuyucu uyumlulugu.

```html
<!-- test-page.html — Bu sayfa kasitli erisebilirlik hatalari iceriyor -->
<!-- GOREV: Hatalari bul ve duzelt -->
<!DOCTYPE html>
<html>  <!-- HATA 1: lang attribute eksik -->
<head><title>Test</title></head>
<body>
  <!-- HATA 2: Baslik hiyerarsisi yanlis (h1 yok, h3 ile basliyor) -->
  <h3>Hosgeldiniz</h3>

  <!-- HATA 3: Resimde alt attribute yok -->
  <img src="hero.jpg">

  <!-- HATA 4: Link'te anlamli metin yok -->
  <a href="/about">Tiklayin</a>

  <!-- HATA 5: Buton div ile yapilmis, keyboard erisilemez -->
  <div onclick="handleClick()" style="cursor: pointer;">Gonder</div>

  <!-- HATA 6: Kontrast orani dusuk -->
  <p style="color: #ccc; background: #fff;">Acik gri metin</p>

  <!-- HATA 7: Form input'unda label yok -->
  <input type="text" placeholder="Adinizi girin">

  <!-- HATA 8: Autoplaying video -->
  <video autoplay src="intro.mp4"></video>
</body>
</html>

<!-- GOREVLER:
1. Yukaridaki 8 hatayi duzelt
2. Lighthouse Accessibility skorunu 100'e cikar
3. Tab ile tum interaktif elemanlara ulasildigini dogrula
4. :focus-visible ile gorunen focus ring ekle
5. Skip navigation link ekle (ekran okuyucu kullanicilari icin)
-->
```

**Beklenen Sonuc:** Tum 8 hata duzeltilmis olmali. Lighthouse Accessibility skoru 100 olmali. Tab ile gezinme sorunsuz çalışmali. Focus ring gorunur olmali.
**Ipucu:** Hata 5 icin `div` yerine `button` kullan. Hata 6 icin WCAG AA kontrast oranini sagla (4.5:1). Skip link icin `<a href="#main" class="skip-link">Ana iceriye atla</a>` kullan.
:::

:::knowledge-check
type: multiple_choice
question: "Bir sayfada kaç tane <main> elemanı olmalıdır?"
options:
  - "Sınırsız sayıda olabilir"
  - "Yalnızca 1 tane"
  - "Her section için 1 tane"
  - "En az 2 tane"
correct: 1
explanation: "Bir HTML sayfasında yalnızca 1 tane <main> elemanı olmalıdır. Bu eleman, sayfanın birincil içeriğini tanımlar ve ekran okuyucuların ana içeriğe hızlıca atlamasını sağlar."
:::

:::knowledge-check
type: multiple_choice
question: "aria-hidden='true' attribute'u ne işe yarar?"
options:
  - "Elemanı CSS ile gizler (display: none)"
  - "Elemanı DOM'dan tamamen kaldırır"
  - "Elemanı ekran okuyuculardan gizler ama görsel olarak görünür kalır"
  - "Elemanı yalnızca mobilde gizler"
correct: 2
explanation: "aria-hidden='true' elemanı ekran okuyuculardan gizler ama görsel olarak görünür kalır. Dekoratif ikonlar, emoji'ler gibi ekran okuyucunun okumasının gereksiz olduğu içerikler için kullanılır."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Semantic HTML5 elemanlarini (header, nav, main, article, section, aside, footer) bir gazete sayfasi analojisiyle acikla. Her elemanin ekran okuyucular tarafindan nasil yorumlandigini ve ARIA landmark role'leri ile iliskisini detayli anlat."

**2. Pratik Uygulama:**
> "Bana bir e-ticaret urun detay sayfasi icin semantic HTML5 iskeleti oluştur. Breadcrumb, urun resmi, aciklama, fiyat, yorum bolumu ve ilgili urunler kismi olsun. Her eleman icin neden o semantic etiketi sectigini acikla."
> Takip: "Simdi bu sayfaya ARIA attribute'lari ekle ve Lighthouse accessibility skorunu 100 yapacak iyilestirmeleri goster."

**3. Mukemmellik Icin:**
> "WCAG 2.1 AA uyumlu bir form tasarliyorum. Label-input eslestirme, aria-describedby ile hata mesajlari, fieldset-legend gruplama, skip navigation ve focus management gibi tum erisilebilirlik gereksinimlerini karsilayan bir kayit formu örneği oluştur ve her karari acikla."

### Pair Programming Ipucu
HTML yazilarken AI'a Lighthouse accessibility raporu ciktisini yapistir ve sor: "Bu rapordaki erisilebilirlik sorunlarini analiz et. Her sorunu severity sirasina gore listele ve semantic HTML ile nasil cozecegimi goster."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Semantic HTML nedir ve neden onemlidir?**
- **Junior cevabi:** Semantic HTML anlamli etiketler kullanmaktir, div yerine header, nav gibi.
- **Senior cevabi:** Semantic HTML uc temel alanda fark yaratir: 1) Accessibility: screen reader'lar landmark role'leri kullanarak sayfa yapisi hakkinda gorme engelli kullanicilara bilgi verir. `<nav>` otomatik olarak navigation landmark olur. 2) SEO: arama motorlari `<article>`, `<main>` gibi etiketlerle icerigin onemini anlar, heading hierarchy (h1-h6) sayfa yapisini gosterir. 3) Maintainability: kod okunakliligini arttirir. `<div class="nav">` yerine `<nav>` ne oldugunu aninda belli eder. WCAG 2.1 AA uyumlulugu cogu ulkede yasal zorunluluktur.

**Soru 2: `<div>` ve `<section>` arasindaki fark nedir? Ne zaman hangisi kullanilir?**
- **Junior cevabi:** Section semantik, div semantik degildir.
- **Senior cevabi:** `<div>` saf container'dir, anlamsal degeri yoktur, sadece gruplama ve styling icindir. `<section>` tematik bir icerigi gruplar ve bir heading (h2-h6) icermelidir. `<article>` ise bagimsiz, kendi basina anlam ifade eden icerik icindir (blog post, yorum, urun karti). Genel kural: icerik RSS feed'de tek basina anlam ifade ediyorsa article, sayfanin bir bolumu ise section, sadece stil icinse div kullanin. Gereksiz section kullanimi accessibility sorunlarina yol acar.
:::

:::exercise
### Alıştırma 4: Erişilebilir Form Oluşturma

**Görev:** Tamamen erişilebilir bir kayıt formu oluştur. ARIA attributeleri, doğru label eşleştirmesi ve klavye navigasyonu destekle.

**Başlangıç kodu:**
```html
<!-- GOREV: Bu formu erisilebilir hale getir -->
<form>
  <div>
    <span>Ad Soyad</span>
    <input type="text">
  </div>

  <div>
    <span>Email</span>
    <input type="text">
  </div>

  <div>
    <span>Sifre</span>
    <input type="text">
  </div>

  <div>
    <span>Cinsiyet</span>
    <input type="radio" name="gender"> Erkek
    <input type="radio" name="gender"> Kadin
    <input type="radio" name="gender"> Belirtmek istemiyorum
  </div>

  <div>
    <span>Sehir</span>
    <select>
      <option>Istanbul</option>
      <option>Ankara</option>
      <option>Izmir</option>
    </select>
  </div>

  <div>
    <input type="checkbox"> Kosullari kabul ediyorum
  </div>

  <div>
    <button>Kayit Ol</button>
  </div>
</form>
```

**Beklenen çıktı:**
```html
<form novalidate aria-labelledby="form-title">
  <h2 id="form-title">Kayit Formu</h2>

  <div>
    <label for="fullname">Ad Soyad <span aria-hidden="true">*</span></label>
    <input type="text" id="fullname" name="fullname" required
           aria-required="true" autocomplete="name">
  </div>

  <div>
    <label for="email">Email <span aria-hidden="true">*</span></label>
    <input type="email" id="email" name="email" required
           aria-required="true" aria-describedby="email-hint" autocomplete="email">
    <small id="email-hint">ornek: ahmet@email.com</small>
  </div>

  <!-- ... devami -->
</form>
```

**İpucu:** Her `<input>` bir `<label for="id">` ile eşleşmeli. `aria-required`, `aria-describedby` ile ekran okuyucu desteği sağla. `type="email"` mobilde doğru klavyeyi açar.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: SEO-Optimize Edilmiş Blog Sayfası

**Görev:** SEO için optimize edilmiş bir blog yazısı sayfası oluştur. Doğru heading hiyerarşisi, meta taglar ve yapısal veri kullan.

**Başlangıç kodu:**
```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- TODO: SEO meta taglari ekle -->
  <!-- title, description, og:title, og:description, og:image, twitter:card -->

  <title><!-- TODO --></title>
</head>
<body>
  <!-- TODO: Semantik HTML ile blog sayfasi olustur -->
  <!-- header > nav -->
  <!-- main > article > (header, sections, footer) -->
  <!-- aside (ilgili yazilar) -->
  <!-- footer -->

  <!-- TODO: Schema.org yapısal veri ekle (JSON-LD) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "React Hooks Rehberi",
    "author": {
      "@type": "Person",
      "name": "Ahmet Yilmaz"
    },
    "datePublished": "2026-03-22",
    "image": "https://example.com/react-hooks.jpg"
  }
  </script>
</body>
</html>
```

**Beklenen çıktı:**
```
Lighthouse SEO skoru: 100/100
- title etiketi var ve 60 karakterden kisa
- meta description var ve 160 karakterden kisa
- Open Graph taglari var (sosyal medya paylasimi icin)
- h1 -> h2 -> h3 hiyerarsisi dogru
- Schema.org yapısal veri var
- lang attribute dogru
```

**İpucu:** `<meta name="description">` arama sonuçlarında gösterilir. Open Graph (`og:`) tagları sosyal medya paylaşımında kullanılır.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 6: Tablo Erişilebilirliği

**Görev:** Karmaşık bir veri tablosunu erişilebilir hale getir. `caption`, `thead`, `scope`, `aria-sort` kullan.

**Başlangıç kodu:**
```html
<!-- GOREV: Bu tabloyu erisilebilir hale getir -->
<table>
  <tr>
    <td>Urun</td>
    <td>Kategori</td>
    <td>Fiyat</td>
    <td>Stok</td>
    <td>Durum</td>
  </tr>
  <tr>
    <td>Laptop</td>
    <td>Elektronik</td>
    <td>15000</td>
    <td>5</td>
    <td>Aktif</td>
  </tr>
  <tr>
    <td>Phone</td>
    <td>Elektronik</td>
    <td>8000</td>
    <td>0</td>
    <td>Tukendi</td>
  </tr>
  <tr>
    <td>T-Shirt</td>
    <td>Giyim</td>
    <td>200</td>
    <td>50</td>
    <td>Aktif</td>
  </tr>
</table>
```

**Beklenen çıktı:**
```html
<table aria-label="Urun Listesi">
  <caption>Magazadaki Urunler - Mart 2026</caption>
  <thead>
    <tr>
      <th scope="col" aria-sort="none">Urun</th>
      <th scope="col">Kategori</th>
      <th scope="col" aria-sort="descending">Fiyat (TL)</th>
      <th scope="col">Stok</th>
      <th scope="col">Durum</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Laptop</th>
      <td>Elektronik</td>
      <td>15.000</td>
      <td>5</td>
      <td><span aria-label="Stokta var">Aktif</span></td>
    </tr>
    <!-- ... -->
  </tbody>
</table>
```

**İpucu:** `<th scope="col">` sütun başlığı, `<th scope="row">` satır başlığı. `<caption>` tablo açıklaması ekler. `<thead>`/`<tbody>` semantik gruplama sağlar.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: HTML5 Dialog ve Modal

**Görev:** Native HTML5 `<dialog>` elemanı kullanarak erişilebilir bir modal oluştur.

**Başlangıç kodu:**
```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>Dialog Ornegi</title>
  <style>
    dialog {
      border: 2px solid #333;
      border-radius: 8px;
      padding: 24px;
      max-width: 500px;
    }
    dialog::backdrop {
      background: rgba(0, 0, 0, 0.5);
    }
  </style>
</head>
<body>
  <h1>HTML5 Dialog</h1>

  <button id="openBtn">Kayit Formunu Ac</button>

  <!-- TODO: Erisilebilir dialog olustur -->
  <dialog id="registerDialog" aria-labelledby="dialog-title">
    <form method="dialog">
      <h2 id="dialog-title">Kayit Ol</h2>

      <div>
        <label for="dialog-name">Ad</label>
        <input type="text" id="dialog-name" required autofocus>
      </div>

      <div>
        <label for="dialog-email">Email</label>
        <input type="email" id="dialog-email" required>
      </div>

      <div style="display: flex; gap: 8px; justify-content: flex-end;">
        <button type="button" id="cancelBtn">Iptal</button>
        <button type="submit" value="confirm">Kayit Ol</button>
      </div>
    </form>
  </dialog>

  <p id="result"></p>

  <script>
    const dialog = document.getElementById('registerDialog');
    const openBtn = document.getElementById('openBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const result = document.getElementById('result');

    // TODO: Dialog ac/kapat islemlerini yaz
    openBtn.addEventListener('click', () => {
      dialog.showModal(); // Modal olarak ac (backdrop + focus trap)
    });

    cancelBtn.addEventListener('click', () => {
      dialog.close('cancel');
    });

    dialog.addEventListener('close', () => {
      if (dialog.returnValue === 'confirm') {
        result.textContent = 'Kayit basarili!';
      } else {
        result.textContent = 'Kayit iptal edildi.';
      }
    });

    // ESC ile kapatmayi handle et
    dialog.addEventListener('cancel', (e) => {
      result.textContent = 'Dialog ESC ile kapatildi.';
    });
  </script>
</body>
</html>
```

**Beklenen çıktı:**
```
- "Kayit Formunu Ac" butonuna tikla -> Modal acilir
- ESC ile veya "Iptal" ile kapatilabilir
- Tab ile sadece modal icinde gezinilir (focus trap)
- Backdrop tiklama ile kapanmaz (showModal)
- Ekran okuyucu dialog'u dogru anons eder
```

**İpucu:** `dialog.showModal()` modal olarak açar (focus trap + backdrop). `dialog.show()` ise non-modal açar. `method="dialog"` form submit'inde dialog'u kapatır.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Picture ve Responsive Images

**Görev:** `<picture>`, `srcset` ve `sizes` kullanarak responsive ve performanslı resim yükleme sistemi oluştur.

**Başlangıç kodu:**
```html
<!-- GOREV: Bu img'i responsive ve performansli hale getir -->
<img src="hero-large.jpg" alt="Hero image">

<!-- Hedef: -->
<!-- 1. Farkli ekran boyutlari icin farkli boyut resimler -->
<!-- 2. WebP destegi (fallback olarak JPEG) -->
<!-- 3. Dark mode icin farkli resim -->
<!-- 4. Lazy loading -->
```

**Beklenen çıktı:**
```html
<!-- Tam responsive resim -->
<picture>
  <!-- Dark mode -->
  <source media="(prefers-color-scheme: dark)"
          srcset="hero-dark-400.webp 400w,
                  hero-dark-800.webp 800w,
                  hero-dark-1200.webp 1200w"
          sizes="(max-width: 600px) 100vw,
                 (max-width: 1200px) 50vw,
                 33vw"
          type="image/webp">

  <!-- WebP (light mode) -->
  <source srcset="hero-400.webp 400w,
                  hero-800.webp 800w,
                  hero-1200.webp 1200w"
          sizes="(max-width: 600px) 100vw,
                 (max-width: 1200px) 50vw,
                 33vw"
          type="image/webp">

  <!-- JPEG fallback -->
  <img src="hero-800.jpg"
       srcset="hero-400.jpg 400w,
              hero-800.jpg 800w,
              hero-1200.jpg 1200w"
       sizes="(max-width: 600px) 100vw,
              (max-width: 1200px) 50vw,
              33vw"
       alt="Modern web gelistirme ortami gorseli"
       loading="lazy"
       decoding="async"
       width="1200"
       height="630">
</picture>
```

**İpucu:** `srcset` ile farklı boyutlar sun, tarayıcı ekrana uygununu seçer. `sizes` tarayıcıya resmin viewport'un ne kadarını kaplayacağını söyler. `loading="lazy"` sayfa yüklenirken görünmeyen resimleri yüklemez.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: Micro-data ve Schema.org

**Görev:** Bir ürün sayfası için Schema.org yapısal verisi ekle. Google arama sonuçlarında zengin snippet gösterilmesini sağla.

**Başlangıç kodu:**
```html
<!-- GOREV: Schema.org micro-data ekle -->
<div>
  <h1>Samsung Galaxy S24 Ultra</h1>
  <img src="s24-ultra.jpg" alt="Samsung Galaxy S24 Ultra">

  <div>
    <span>Fiyat: 54.999 TL</span>
    <span>Stokta var</span>
  </div>

  <div>
    <span>4.5 / 5</span>
    <span>(128 degerlendirme)</span>
  </div>

  <p>Samsung'un amiral gemisi telefonu. 200MP kamera, S Pen destegi...</p>
</div>

<!-- GOREV: JSON-LD formatinda da ekle -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Samsung Galaxy S24 Ultra",
  "image": "https://example.com/s24-ultra.jpg",
  "description": "Samsung amiral gemisi telefonu",
  "brand": {
    "@type": "Brand",
    "name": "Samsung"
  },
  "offers": {
    "@type": "Offer",
    "price": "54999",
    "priceCurrency": "TRY",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "TechShop"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "128"
  }
}
</script>
```

**Beklenen çıktı:**
```
Google Rich Results Test sonucu:
- Product: Samsung Galaxy S24 Ultra
- Price: 54,999 TRY
- Availability: In Stock
- Rating: 4.5/5 (128 reviews)
- Tum alanlar gecerli, hata yok
```

**İpucu:** `schema.org/Product` en yaygın yapısal veri tipi. Google Rich Results Test aracı ile doğrula. JSON-LD formatı Google tarafından tercih edilir.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: ARIA Live Regions ile Dinamik İçerik

**Görev:** Ekran okuyucuların dinamik içerik değişikliklerini duyurmasını sağlayan ARIA live region'lar oluştur.

**Başlangıç kodu:**
```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>ARIA Live Regions</title>
</head>
<body>
  <h1>Alısveris Sepeti</h1>

  <!-- Urun listesi -->
  <div>
    <button onclick="addToCart('Laptop', 15000)">Laptop Ekle (15.000 TL)</button>
    <button onclick="addToCart('Phone', 8000)">Phone Ekle (8.000 TL)</button>
    <button onclick="addToCart('Mouse', 200)">Mouse Ekle (200 TL)</button>
  </div>

  <!-- TODO: aria-live="polite" ile sepet guncelleme bildirimi -->
  <div id="cart-status" role="status" aria-live="polite" aria-atomic="true">
    Sepet bos
  </div>

  <!-- TODO: aria-live="assertive" ile hata bildirimi -->
  <div id="error-msg" role="alert" aria-live="assertive" hidden>
  </div>

  <!-- Sepet ozeti -->
  <div id="cart-summary" aria-label="Sepet ozeti">
    <h2>Sepetim</h2>
    <ul id="cart-items" role="list"></ul>
    <p id="cart-total">Toplam: 0 TL</p>
  </div>

  <script>
    const cart = [];

    function addToCart(name, price) {
      // TODO:
      // 1. Urunu sepete ekle
      // 2. cart-status'u guncelle (ekran okuyucu duyuracak)
      // 3. Stok yoksa error-msg'i goster (assertive - hemen duyurulur)
      // 4. Sepet listesini guncelle

      cart.push({ name, price });
      const total = cart.reduce((sum, item) => sum + item.price, 0);

      // Status guncelle (polite - siradaki bosluktaduyurulur)
      document.getElementById('cart-status').textContent =
        `${name} sepete eklendi. Toplam: ${total.toLocaleString('tr-TR')} TL`;

      // Liste guncelle
      const list = document.getElementById('cart-items');
      const li = document.createElement('li');
      li.textContent = `${name} - ${price.toLocaleString('tr-TR')} TL`;
      list.appendChild(li);

      document.getElementById('cart-total').textContent =
        `Toplam: ${total.toLocaleString('tr-TR')} TL`;
    }

    function showError(message) {
      const errorEl = document.getElementById('error-msg');
      errorEl.textContent = message;
      errorEl.hidden = false;
      // 3 saniye sonra gizle
      setTimeout(() => { errorEl.hidden = true; }, 3000);
    }
  </script>
</body>
</html>
```

**Beklenen çıktı:**
```
"Laptop Ekle" butonuna tikla:
  Gorsel: "Laptop sepete eklendi. Toplam: 15.000 TL"
  Ekran okuyucu: "Laptop sepete eklendi. Toplam: 15.000 TL" (polite - siradaki boslukta)

Stok hatasi durumunda:
  Ekran okuyucu: "Urun stokta yok!" (assertive - hemen duyurulur)

ARIA live region tipleri:
  polite = mevcut konusma bittikten sonra duyur
  assertive = hemen duyur (acil mesajlar icin)
  off = duyurma
```

**İpucu:** `aria-live="polite"` rutin güncellemeler, `role="alert"` + `aria-live="assertive"` acil bildirimler için. `aria-atomic="true"` tüm bölgeyi tekrar okur.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Landmark Navigation Testi

**Görev:** Bir web sayfasının ARIA landmark'larını test eden bir JavaScript script yaz.

**Başlangıç kodu:**
```html
<!DOCTYPE html>
<html lang="tr">
<head><title>Landmark Test</title></head>
<body>
  <!-- TODO: Bu sayfaya dogru landmark'lari ekle -->
  <div id="header">
    <div id="nav">
      <a href="/">Ana Sayfa</a>
      <a href="/about">Hakkimda</a>
    </div>
  </div>
  <div id="content">
    <div id="article">
      <h1>Blog Yazisi</h1>
      <p>Icerik buraya...</p>
    </div>
    <div id="sidebar">
      <h2>Ilgili Yazilar</h2>
    </div>
  </div>
  <div id="footer">
    <p>2026 Tum haklar saklidir</p>
  </div>

  <script>
  // Landmark kontrol script'i
  function checkLandmarks() {
    const landmarks = {
      banner: document.querySelector('header, [role="banner"]'),
      navigation: document.querySelector('nav, [role="navigation"]'),
      main: document.querySelector('main, [role="main"]'),
      contentinfo: document.querySelector('footer, [role="contentinfo"]'),
      complementary: document.querySelector('aside, [role="complementary"]'),
    };

    console.log("=== Landmark Kontrolu ===");
    let score = 0;
    for (const [name, element] of Object.entries(landmarks)) {
      const status = element ? "OK" : "EKSIK";
      if (element) score++;
      console.log(`  ${name}: ${status}`);
    }

    // Ek kontroller
    const h1Count = document.querySelectorAll('h1').length;
    console.log(`\n  h1 sayisi: ${h1Count} (${h1Count === 1 ? 'OK' : 'HATALI - tek olmali'})`);

    const mainCount = document.querySelectorAll('main').length;
    console.log(`  main sayisi: ${mainCount} (${mainCount === 1 ? 'OK' : 'HATALI - tek olmali'})`);

    console.log(`\n  Skor: ${score}/5 landmark`);
  }

  checkLandmarks();
  </script>
</body>
</html>
```

**Beklenen çıktı:**
```
=== Landmark Kontrolu ===
  banner: EKSIK (header etiketi kullanilmali)
  navigation: EKSIK (nav etiketi kullanilmali)
  main: EKSIK (main etiketi kullanilmali)
  contentinfo: EKSIK (footer etiketi kullanilmali)
  complementary: EKSIK (aside etiketi kullanilmali)

GOREV: div'leri semantic etiketlerle degistir ve 5/5 skor al
```

**İpucu:** Her landmark sadece 1 kez kullanılmalı (navigation hariç, birden fazla olabilir). `<main>` sayfada sadece 1 tane olmalı.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 12: Erişilebilirlik Denetim Aracı

**Görev:** Bir HTML sayfasındaki erişilebilirlik sorunlarını otomatik tespit eden bir JavaScript aracı yaz.

**Başlangıç kodu:**
```html
<!DOCTYPE html>
<html>
<head><title>A11y Checker</title></head>
<body>
  <!-- Kasitli hatali sayfa -->
  <img src="photo.jpg">
  <input type="text" placeholder="Adiniz">
  <a href="#">Tikla</a>
  <div onclick="handleClick()">Buton Gibi Div</div>
  <p style="color: #ccc; background: #fff;">Dusuk kontrast metin</p>
  <table><tr><td>Veri 1</td><td>Veri 2</td></tr></table>

  <script>
  function auditAccessibility() {
    const issues = [];

    // 1. Alt attribute eksik img'ler
    document.querySelectorAll('img:not([alt])').forEach((img) => {
      issues.push({level: "error", rule: "img-alt", message: "img alt attribute eksik", element: img.outerHTML.slice(0, 50)});
    });

    // 2. Label'siz input'lar
    document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])').forEach((input) => {
      const label = document.querySelector(`label[for="${input.id}"]`);
      if (!label && !input.closest('label')) {
        issues.push({level: "error", rule: "input-label", message: "input icin label eksik", element: input.outerHTML.slice(0, 50)});
      }
    });

    // 3. Bos link'ler
    document.querySelectorAll('a').forEach((a) => {
      if (a.textContent.trim().length < 2 || a.textContent.trim() === "Tikla") {
        issues.push({level: "warning", rule: "link-text", message: "Link metni aciklayici degil", element: a.outerHTML.slice(0, 50)});
      }
    });

    // TODO: 4. role="button" olmayan tikanabilir div'ler
    // TODO: 5. thead'siz tablo'lar
    // TODO: 6. html lang attribute kontrolu

    console.log("=== Erisebilirlik Denetimi ===");
    console.log(`Toplam: ${issues.length} sorun bulundu\n`);

    issues.forEach((issue, i) => {
      const icon = issue.level === "error" ? "HATA" : "UYARI";
      console.log(`${i+1}. [${icon}] ${issue.rule}: ${issue.message}`);
      console.log(`   Element: ${issue.element}`);
    });
  }

  auditAccessibility();
  </script>
</body>
</html>
```

**Beklenen çıktı:**
```
=== Erisebilirlik Denetimi ===
Toplam: 5 sorun bulundu

1. [HATA] img-alt: img alt attribute eksik
   Element: <img src="photo.jpg">
2. [HATA] input-label: input icin label eksik
   Element: <input type="text" placeholder="Adiniz">
3. [UYARI] link-text: Link metni aciklayici degil
   Element: <a href="#">Tikla</a>
4. [HATA] div-button: Tikanabilir div role="button" olmali
   Element: <div onclick="handleClick()">
5. [HATA] table-header: Tablo thead/th eksik
   Element: <table><tr><td>...
```

**İpucu:** Her `img` bir `alt` attribute'u olmalı. Her `input` bir `label` ile eşleştirilmeli. Tıklanabilir `div`'ler `role="button"` ve `tabindex="0"` olmalı.

**Zorluk:** Zor
:::

:::must-note
- Semantic HTML elemanları: header, nav, main (sayfada 1 tane), article, section, aside, footer
- `<div>` yerine uygun semantic eleman kullan - erişilebilirlik ve SEO için kritik
- Her `<input>`'un mutlaka bir `<label>` ile eşleştirilmesi gerekir (for + id)
- ARIA kuralı: Native HTML elemanı varsa onu kullan, ARIA son çare olsun
- aria-label: görünmez açıklama, aria-hidden="true": ekran okuyucudan gizle
- aria-live="polite": dinamik içerik değişikliğini ekran okuyucuya duyur
- Heading hiyerarşisini atlama (h1 > h3): SEO ve erişilebilirlik hatası
- Meta description: 150-160 karakter, Open Graph: sosyal medya paylaşım önizlemesi
- JSON-LD structured data: Google rich snippets (yıldız, fiyat, tarih)
- HTML5 input types: email, tel, url, date, range, color - mobilde özel klavye açar
- localStorage: kalıcı, sessionStorage: sekme kapanınca silinir, hassas veri saklanmaz
- Web Workers: ağır hesaplamaları arka planda çalıştır, UI donmasını engelle
- Canvas API: 2D grafik çizimi, oyun ve veri görselleştirme için kullanılır
- autocomplete attribute'u: tarayıcının doğru otomatik doldurma önerileri sunmasını sağlar
:::

:::senior-learns
Bir Senior Developer, HTML ve erişilebilirlik konusunda şu yaklaşımı benimser:

1. **WCAG 2.1 AA standartlarını bilir** - Web Content Accessibility Guidelines'ı okur ve projelerinde uygular. Kontrast oranları (4.5:1 minimum), focus indicator'lar ve skip navigation link'leri standart pratiğidir.
2. **Axe veya Lighthouse ile otomatik test yapar** - Her PR'da accessibility audit çalıştırır. CI/CD pipeline'ına axe-core veya pa11y entegre eder. Manuel testleri de ihmal etmez - Tab navigasyonu ve screen reader testi yapar.
3. **Component library'de erişilebilirliği zorunlu kılar** - Radix UI, Headless UI gibi accessible-by-default kütüphaneler tercih eder. Custom component yazarken WAI-ARIA Authoring Practices'ı referans alır.
4. **SEO'yu teknik borç olarak görmez** - Structured data (JSON-LD), canonical URL'ler, proper heading hierarchy ve meta tag'leri baştan doğru kurar. "Sonra ekleriz" demez.
5. **HTML'i progressive enhancement ile yazar** - JavaScript devre dışı kalsa bile temel işlevselliğin çalışmasını sağlar. Form validation hem client-side hem server-side yapılır.
6. **Performance'ı HTML seviyesinde optimize eder** - `loading="lazy"` ile resimleri lazy load eder, `<link rel="preload">` ile kritik kaynakları önceden yükler, `fetchpriority="high"` ile LCP elemanını önceliklendirir.

**Profesyonel Mindset:** "Erişilebilirlik bir özellik değil, kalite standardıdır. Tıpkı güvenlik gibi, sonradan eklenemez - baştan tasarlanmalıdır. Dünyada 1 milyardan fazla engelli birey var. Erişilebilir kod yazmak hem etik bir sorumluluk hem de yasal bir gereklilik (ADA, EAA). Ayrıca erişilebilir kod her zaman daha iyi, daha bakımı kolay koddur."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Semantic** (sɪ-mæn-tɪk) → Anlamsal
   *"Using semantic HTML elements improves accessibility and SEO."*

2. **Accessibility** (æk-ses-ə-bɪl-ɪ-ti) → Erişilebilirlik
   *"We must ensure our web application meets WCAG accessibility guidelines."*

3. **Screen reader** (skriːn riː-dər) → Ekran okuyucu
   *"A screen reader announces the page structure using ARIA landmarks."*

4. **Structured data** (strʌk-tʃərd deɪ-tə) → Yapılandırılmış veri
   *"Adding structured data helps search engines understand your content."*

5. **Validation** (væl-ɪ-deɪ-ʃən) → Doğrulama
   *"HTML5 provides built-in form validation with the required attribute."*

**Okuma Egzersizi:** MDN'de "HTML elements reference" sayfasını İngilizce oku: https://developer.mozilla.org/en-US/docs/Web/HTML/Element

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Semantic HTML yapısını ve erişilebilirlik özelliklerini ekledim"
→ Örnek: `feat: add semantic HTML structure and accessibility improvements`
:::

:::external-resource
- 📖 **MDN Web Docs:** "HTML elements reference" (İngilizce, ücretsiz)
- 📺 **Web.dev:** "Learn Accessibility" (Google, ücretsiz)
- 🎮 **A11y Project:** a11yproject.com (erişilebilirlik kontrol listesi, ücretsiz)
- 📖 **Schema.org:** schema.org (structured data referansı, ücretsiz)
- 🔧 **Axe DevTools:** Chrome extension (erişilebilirlik test aracı, ücretsiz)
:::
