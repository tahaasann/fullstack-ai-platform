---
title: "Debugging ve Troubleshooting: Hata Avlama Sanatı"
estimated_minutes: 90
tags: ["debugging", "devtools", "console", "breakpoints", "error-handling", "troubleshooting"]
prerequisites: ["terminal", "vscode"]
---

# Debugging ve Troubleshooting: Hata Avlama Sanatı

:::realworld
Bir developer'ın zamanının %50'den fazlası debug yaparak geçer. Kod yazmak kolaydır, ama neden çalışmadığını bulmak asıl ustalık gerektirir. Senior developer'ları junior'lardan ayıran en büyük fark budur: Senior bir hatayı 5 dakikada bulur, junior saatlerce uğraşır. Bu derste profesyonel debugging araçlarını ve tekniklerini öğreneceksin.

**Gerçek Dünya Örnekleri:**
- **Netflix:** Production'da bir performans sorunu çıktığında, Chrome DevTools Performance tab'ını kullanarak React component render sürelerini ölçerler. Flame graph'larla hangi component'in yavaş olduğunu tespit ederler.
- **Stripe:** API çağrılarında timeout hatası alındığında, Network tab'ında request timing breakdown'ına bakarlar: DNS lookup, TCP handshake, TTFB (Time to First Byte) ayrı ayrı analiz edilir.
- **Meta (Facebook):** React DevTools'un Profiler'ını kullanarak unnecessary re-render'ları tespit ederler. Bir component saniyede 60 kez render oluyorsa, Performance tab ile bunu yakalarlar.
- **Vercel:** Deployment hataları oluştuğunda, build log'larını satır satır okurlar. Stack trace'deki her satır, hatanın kaynağına bir ipucu taşır.
:::

## Neden Debugging Becerisi Kritik?

Debugging sadece hata bulmak değildir. Sistematik problem çözme yeteneğidir. Bu beceri:

- İş mülakatlarında live coding session'larında fark yaratır
- Production incident'larda hızlı çözüm üretmeni sağlar
- Başkalarının kodunu anlamanı kolaylaştırır
- Seni takımın "sorun çözen kişisi" yapar

:::deha-tip
Deha seviyesi developer'lar debugging'e sistematik yaklaşır. Asla "rastgele bir şeyler deneyip bakmak" yapmazlar. Bilimsel metodu uygularlar: (1) Sorunu tanımla, (2) Hipotez kur, (3) Test et, (4) Sonucu değerlendir. Bu döngüyü hata bulunana kadar tekrarla. `console.log` bile bilinçli ve stratejik kullanılır.
:::

:::senior-learns
Senior/CTO debugging'i öğrenirken, binary search debugging tekniğini kullanır. Kodun ortasına bir breakpoint koy: Eğer orada veri doğruysa hata sonrasında, yanlışsa öncesinde. Her adımda arama alanını yarıya indirirsin. 1000 satır kodda bile maximum 10 adımda (log2(1000)) hatayı bulabilirsin. Bu, O(log n) karmaşıklığında debugging demektir.
:::

## Chrome DevTools: Frontend Developer'ın Silahı

Chrome DevTools, frontend debugging'in temel aracıdır. `F12` veya `Ctrl+Shift+I` (Mac: `Cmd+Opt+I`) ile açılır.

### Elements Tab: DOM ve CSS İnceleme

:::concept[Elements Tab (İng: Elements Panel)]
Elements tab, sayfanın HTML yapısını (DOM tree) ve CSS stillerini gerçek zamanlı olarak inceleme ve düzenleme aracıdır.

**Türkçe karşılığı:** Elemanlar Paneli
**Ne işe yarar:** HTML yapısını gör, CSS'i düzenle, layout sorunlarını tespit et
**Gerçek hayat benzetmesi:** Bir binanın röntgen cihazı gibi - duvarların arkasını, boruları ve kabloları görebilirsin
:::

:::code[text]{title="Elements Tab Kullanım Rehberi"}
TEMEL İŞLEMLER:
1. Element Seçme:
   - Ctrl+Shift+C (Element picker) → Sayfada herhangi bir elemente tıkla
   - DOM tree'de elemente sağ tık → "Scroll into view" ile sayfada bul

2. CSS Düzenleme (Canlı):
   - Styles panelinde herhangi bir CSS değerini değiştir
   - Yeni property ekle: Boş alana tıkla ve yaz
   - Property'yi devre dışı bırak: Checkbox'ı kaldır
   - Computed tab: Elementin son hesaplanmış CSS değerleri

3. Box Model Görselleştirme:
   - Computed tab'ında Box Model diyagramını gör
   - Margin (turuncu), border (sarı), padding (yeşil), content (mavi)
   - Hover'da sayfada gerçek boyutları gösterir

4. Layout Debugging:
   - Flexbox/Grid badge'lerine tıkla → Overlay gösterir
   - Grid overlay: Satır/sütun çizgilerini ve numaraları gösterir
   - Flexbox overlay: Ana eksen ve çapraz ekseni gösterir

5. DOM Manipülasyonu:
   - Element sürükle-bırak ile sıralama değiştir
   - Sağ tık → "Edit as HTML" ile HTML düzenle
   - Sağ tık → "Force state" → :hover, :active, :focus durumlarını simüle et
:::

:::exercise
**Alıştırma 1: Elements Tab Keşfi**

Herhangi bir web sitesini aç (ör. github.com) ve şunları yap:

1. `Ctrl+Shift+C` ile element picker'ı aç, navbar'daki bir linke tıkla
2. Styles panelinde link rengini kırmızıya çevir
3. Computed tab'ında elementin box model'ini incele: padding, margin, border değerlerini not al
4. Sağ tık → "Force state" → `:hover` durumunu etkinleştir ve hover CSS'ini gör
5. Layout badge'ine tıklayıp Flexbox overlay'ini göster

**Amaç:** Elements tab'ı ile CSS'i canlı olarak nasıl debug edeceğini öğrenmek.
:::

### Console Tab: JavaScript Debugging

:::concept[Console Tab (İng: Console Panel)]
Console tab, JavaScript kodunu çalıştırma, hata mesajlarını görme ve uygulama durumunu inceleme aracıdır.

**Türkçe karşılığı:** Konsol Paneli
**Ne işe yarar:** JS hatalarını gör, kod çalıştır, veri yapılarını incele
**Gerçek hayat benzetmesi:** Doktorun stetoskopu gibi - uygulamanın kalbini dinlersin
:::

:::code[javascript]{title="Console Metodları - Temel"}
// 1. console.log() - Genel amaçlı loglama
console.log("Merhaba Dünya");
console.log("Kullanıcı:", user);
console.log("Değer:", value, "Tip:", typeof value);

// 2. console.error() - Hata mesajı (kırmızı, stack trace ile)
console.error("API çağrısı başarısız:", error.message);

// 3. console.warn() - Uyarı mesajı (sarı)
console.warn("Deprecated API kullanılıyor. v3'e geçin.");

// 4. console.info() - Bilgi mesajı (mavi ikon)
console.info("Uygulama başlatıldı, port:", 3000);

// 5. console.debug() - Debug seviyesi (verbose filtre gerektirir)
console.debug("Cache hit, key:", cacheKey);
:::

:::code[javascript]{title="Console Metodları - İleri Seviye"}
// 6. console.table() - Veriyi tablo formatında göster
const users = [
  { name: "Ali", age: 28, role: "developer" },
  { name: "Ayşe", age: 32, role: "designer" },
  { name: "Mehmet", age: 25, role: "developer" },
];
console.table(users);
// Tablo olarak güzel bir şekilde gösterir:
// ┌─────────┬──────────┬─────┬─────────────┐
// │ (index) │   name   │ age │    role      │
// ├─────────┼──────────┼─────┼─────────────┤
// │    0    │  'Ali'   │ 28  │ 'developer' │
// │    1    │  'Ayşe'  │ 32  │ 'designer'  │
// │    2    │ 'Mehmet' │ 25  │ 'developer' │
// └─────────┴──────────┴─────┴─────────────┘

// 7. console.group() / console.groupEnd() - Logları grupla
console.group("API Request");
console.log("URL:", url);
console.log("Method:", method);
console.log("Body:", body);
console.groupEnd();
// Console'da katlanabilir grup olarak gösterir

// 8. console.time() / console.timeEnd() - Süre ölç
console.time("dataFetch");
const data = await fetchData();
console.timeEnd("dataFetch");
// Çıktı: "dataFetch: 234.56ms"

// 9. console.count() - Kaç kez çağrıldığını say
function handleClick() {
  console.count("click");
}
// Çıktı: "click: 1", "click: 2", "click: 3"...

// 10. console.assert() - Koşul false ise hata göster
console.assert(user !== null, "Kullanıcı null olamaz!");
console.assert(items.length > 0, "Liste boş!");
// Koşul true ise hiçbir şey göstermez, false ise error yazdırır

// 11. console.trace() - Stack trace göster
function innerFunction() {
  console.trace("Buraya nasıl geldik?");
}
// Çağrı zincirini gösterir: innerFunction < outerFunction < onClick

// 12. console.dir() - Object'i detaylı göster
console.dir(document.body);
// DOM elementini JS object olarak gösterir (property'leri ile)
:::

:::must-note
**MUTLAKA NOT AL:** `console.table()` array'leri ve object'leri tablo formatında gösterir - API response debug ederken hayat kurtarır. `console.time()/timeEnd()` performans ölçümü için kullan. `console.group()` ile logları düzenli tut. Bu 3 metod junior'ları senior'dan ayırır - senior sadece `console.log` kullanmaz.
:::

:::beginner-mistake
Yaygın hata: Her yere `console.log` bırakmak ve sonra hangisinin hangi veriyi bastığını karıştırmak. **Çözüm:** Her log'a context ver: `console.log("[UserService] fetchUser result:", data)`. Prefix kullanmak, yüzlerce log arasında aradığını bulmayı kolaylaştırır. Production'a console.log göndermek de bir başka hata - ESLint kuralı ile engellenmelidir.
:::

:::exercise
**Alıştırma 2: Console Metodları Pratiği**

Tarayıcı console'unu aç (F12 → Console) ve şunları çalıştır:

```javascript
// 1. Bir array'i table olarak göster
const products = [
  { name: "Laptop", price: 15000, stock: 5 },
  { name: "Mouse", price: 250, stock: 100 },
  { name: "Keyboard", price: 500, stock: 45 },
];
console.table(products);

// 2. Bir işlemin süresini ölç
console.time("loop");
for (let i = 0; i < 1000000; i++) { Math.sqrt(i); }
console.timeEnd("loop");

// 3. Gruplu loglama yap
console.group("Kullanıcı Bilgileri");
console.log("Ad:", "Ali");
console.log("Email:", "ali@example.com");
console.warn("Email doğrulanmamış!");
console.groupEnd();

// 4. Assert ile kontrol yap
const age = 15;
console.assert(age >= 18, "Kullanıcı 18 yaşından küçük!");
```

**Amaç:** Console'un sadece `log`'dan ibaret olmadığını görmek.
:::

### Network Tab: API ve Ağ Debugging

:::concept[Network Tab (İng: Network Panel)]
Network tab, sayfanın yaptığı tüm HTTP isteklerini (API çağrıları, dosya yüklemeleri, resimler vb.) izleme ve analiz etme aracıdır.

**Türkçe karşılığı:** Ağ Paneli
**Ne işe yarar:** API çağrılarını izle, response'ları incele, performans sorunlarını bul
**Gerçek hayat benzetmesi:** Kargonun takip numarası gibi - paketin (verinin) nerede olduğunu, ne zaman yola çıktığını, ne kadar sürede ulaştığını görürsün
:::

:::code[text]{title="Network Tab Kullanım Rehberi"}
TEMEL İŞLEMLER:

1. Filtreleme:
   - All: Tüm istekler
   - Fetch/XHR: Sadece API çağrıları (EN ÇOK KULLANACAĞIN)
   - JS: JavaScript dosyaları
   - CSS: Stil dosyaları
   - Img: Resimler
   - Filter kutusu: URL'ye göre filtrele (ör: "/api/users")

2. Request Detayları (bir isteğe tıkla):
   - Headers: Request/Response header'ları
   - Preview: Response'un formatlanmış görünümü
   - Response: Ham response verisi
   - Timing: İsteğin zamanlama breakdown'ı
   - Cookies: İstekle gönderilen/alınan cookie'ler

3. Timing Breakdown:
   - Queueing: İstek kuyruğunda bekleme
   - DNS Lookup: Domain çözümleme
   - Initial Connection: TCP handshake
   - SSL: TLS handshake
   - TTFB (Time to First Byte): Sunucunun işleme süresi
   - Content Download: Veri indirme süresi

4. Throttling (Yavaş Ağ Simülasyonu):
   - Online → Fast 3G → Slow 3G → Offline
   - Yavaş bağlantıda uygulamanın nasıl davrandığını test et
   - Loading state'leri ve error handling'i kontrol et

5. Preserve Log:
   - Sayfa yenilendiğinde logları koru
   - Redirect zincirlerini izlemek için kullanışlı
:::

:::code[text]{title="HTTP Status Kodları - Hızlı Referans"}
2xx Başarılı:
  200 OK              → İstek başarılı
  201 Created          → Yeni kaynak oluşturuldu (POST sonrası)
  204 No Content       → Başarılı ama response body yok (DELETE sonrası)

3xx Yönlendirme:
  301 Moved Permanently → Kalıcı yönlendirme (SEO için önemli)
  302 Found            → Geçici yönlendirme
  304 Not Modified     → Cache'den kullan (sunucu değişmedi diyor)

4xx Client Hatası (SENİN HATAN):
  400 Bad Request      → İstek formatı yanlış (validation hatası)
  401 Unauthorized     → Giriş yapman gerekiyor (token yok/geçersiz)
  403 Forbidden        → Giriş yaptın ama yetkin yok
  404 Not Found        → Kaynak bulunamadı (yanlış URL)
  405 Method Not Allowed → Yanlış HTTP metodu (GET yerine POST vb.)
  409 Conflict         → Kaynak çakışması (duplicate entry)
  422 Unprocessable    → Veri formatı doğru ama içerik geçersiz
  429 Too Many Requests → Rate limit aşıldı

5xx Server Hatası (SUNUCU HATASI):
  500 Internal Server  → Sunucuda beklenmeyen hata
  502 Bad Gateway      → Proxy/load balancer upstream'e ulaşamadı
  503 Service Unavailable → Sunucu geçici olarak kullanılamıyor
  504 Gateway Timeout  → Upstream sunucu zaman aşımı
:::

:::warning
**401 vs 403 farkı** mülakata sık sorulan sorulardandır. **401 Unauthorized**: Kimliğin doğrulanmadı (token yok veya geçersiz). **403 Forbidden**: Kimliğin doğrulandı ama bu kaynağa erişim yetkin yok. Örnek: Giriş yapmamışsın → 401. Giriş yaptın ama admin sayfasına erişiyorsun → 403.
:::

:::exercise
**Alıştırma 3: Network Tab ile API Debugging**

1. Tarayıcıda Network tab'ını aç, "Fetch/XHR" filtresini seç
2. Console'a şu kodu yapıştır ve çalıştır:

```javascript
// Başarılı istek
fetch("https://jsonplaceholder.typicode.com/users/1")
  .then(r => r.json())
  .then(data => console.log("User:", data));

// 404 hatası
fetch("https://jsonplaceholder.typicode.com/users/999999")
  .then(r => console.log("Status:", r.status));

// POST isteği
fetch("https://jsonplaceholder.typicode.com/posts", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "Test", body: "Deneme", userId: 1 })
}).then(r => r.json()).then(data => console.log("Created:", data));
```

3. Network tab'ında her isteğe tıkla ve şunları incele:
   - Headers tab: Request method, URL, headers
   - Response tab: Dönen JSON verisi
   - Timing tab: İsteğin ne kadar sürdüğü

**Amaç:** Network tab'ını kullanarak API isteklerini debug edebilmek.
:::

### CORS Hataları

:::concept[CORS (İng: Cross-Origin Resource Sharing)]
CORS, bir web sayfasının farklı bir domain'den veri istemesini kontrol eden güvenlik mekanizmasıdır.

**Türkçe karşılığı:** Çapraz Kaynak Paylaşımı
**Ne işe yarar:** Tarayıcı, güvenlik nedeniyle farklı domain'lerden gelen istekleri engelleyebilir. CORS bu engeli kontrollü şekilde kaldırır.
**Gerçek hayat benzetmesi:** Pasaport kontrolü gibi - senin (frontend) ülkenden, başka bir ülkeye (backend) gidebilmen için o ülkenin sana vize (CORS header) vermesi gerekir
:::

:::code[text]{title="CORS Hatası ve Çözümü"}
HATA MESAJI (Console'da kırmızı):
"Access to fetch at 'https://api.example.com/data' from origin
'http://localhost:3000' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present."

NEDEN OLUŞUR?
- Frontend: http://localhost:3000
- Backend:  http://localhost:8000
- Farklı port = farklı origin = CORS engeli

ÇÖZÜM (Backend tarafında):

# Python FastAPI:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Node.js Express:
const cors = require("cors");
app.use(cors({
  origin: ["http://localhost:3000", "http://localhost:5173"],
  credentials: true,
}));

PREFLIGHT REQUEST (OPTIONS):
- Tarayıcı, asıl isteği göndermeden önce "izin var mı?" diye sorar
- Bu OPTIONS isteğine "preflight" denir
- Network tab'ında aynı URL'ye iki istek görürsen: ilki OPTIONS, ikincisi asıl istek
:::

:::beginner-mistake
Yaygın hata: CORS hatasını frontend'de çözmeye çalışmak. CORS bir **tarayıcı güvenlik mekanizmasıdır** ve **backend tarafında** çözülür. Frontend'de header eklemek, proxy ayarlamak (development hariç) veya no-cors mode kullanmak doğru çözüm değildir. Backend'e CORS middleware ekletmelisin. Development ortamında Vite/CRA proxy kullanabilirsin ama production'da backend CORS header'ları zorunludur.
:::

:::exercise
**Alıştırma 4: CORS Hatası Simülasyonu**

Console'da şu kodu çalıştır ve CORS hatasını gözlemle:

```javascript
// Bu CORS hatası verecek (farklı origin)
fetch("https://www.google.com")
  .then(r => r.text())
  .then(data => console.log(data))
  .catch(err => console.error("CORS Hatası:", err));
```

1. Console'daki hata mesajını oku
2. Network tab'ında isteği bul ve status'ünü kontrol et
3. Şimdi CORS'a izin veren bir API ile dene:

```javascript
// Bu çalışacak (CORS header'ları var)
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then(r => r.json())
  .then(data => console.log("Başarılı:", data));
```

**Amaç:** CORS hatasını tanıyabilmek ve nedenini anlayabilmek.
:::

### Sources Tab: Breakpoint Debugging

:::concept[Breakpoint (İng: Breakpoint)]
Breakpoint, kodun belirli bir satırında durmasını sağlayan işaretçidir. Kod bu noktada durunca tüm değişkenlerin değerlerini inceleyebilirsin.

**Türkçe karşılığı:** Durma Noktası / Kesme Noktası
**Ne işe yarar:** Kodun çalışma anında değişkenlerin değerlerini görmeni sağlar
**Gerçek hayat benzetmesi:** Bir filmi pause'a almak gibi - o anda her şey dondurulur ve her detayı inceleyebilirsin
:::

:::code[text]{title="Sources Tab - Breakpoint Debugging Rehberi"}
BREAKPOINT TÜRLERİ:

1. Line Breakpoint (Satır):
   - Sources tab'ında dosyayı bul → Satır numarasına tıkla
   - Mavi nokta = aktif breakpoint
   - Kod bu satıra geldiğinde durur

2. Conditional Breakpoint (Koşullu):
   - Satır numarasına sağ tıkla → "Add conditional breakpoint"
   - Koşul: `userId === 5` veya `items.length > 100`
   - Sadece koşul true olduğunda durur

3. DOM Breakpoint:
   - Elements tab'ında elemente sağ tıkla → "Break on..."
   - subtree modifications: Alt elementler değiştiğinde
   - attribute modifications: Attribute değiştiğinde
   - node removal: Element silindiğinde

4. XHR/Fetch Breakpoint:
   - Sources tab → XHR/Fetch Breakpoints
   - URL pattern ekle (ör: "/api/users")
   - Bu URL'ye istek yapıldığında durur

5. Event Listener Breakpoint:
   - Sources tab → Event Listener Breakpoints
   - Mouse > click, Keyboard > keydown vb.
   - İlgili event tetiklendiğinde durur

DEBUGGING KONTROLLER:
   ▶ Resume (F8)        → Bir sonraki breakpoint'e kadar devam et
   ⏭ Step Over (F10)    → Mevcut satırı çalıştır, fonksiyon içine girme
   ⏬ Step Into (F11)    → Fonksiyon çağrısının içine gir
   ⏫ Step Out (Shift+F11) → Mevcut fonksiyondan çık
   ⏹ Deactivate         → Tüm breakpoint'leri geçici kapat

SCOPE PANELİ (Sağ taraf):
   - Local: Mevcut fonksiyonun değişkenleri
   - Closure: Closure üzerinden erişilen değişkenler
   - Global: window objesi
   - Watch: İzlemek istediğin ifadeler (ör: user.name, items.length)
:::

:::code[javascript]{title="debugger Keyword"}
// Kodda programmatic olarak breakpoint koy
function processOrder(order) {
  const total = order.items.reduce((sum, item) => sum + item.price, 0);

  // DevTools açıksa burada durur
  debugger;

  if (total > 1000) {
    applyDiscount(order);
  }

  return total;
}

// Koşullu debugger
function fetchUser(id) {
  const user = getFromCache(id);
  if (!user) {
    debugger; // Sadece cache miss olduğunda dur
  }
  return user || fetchFromAPI(id);
}
:::

:::must-note
**MUTLAKA NOT AL:** `debugger;` statement'ı kodda bırakılmamalıdır. Development sırasında kullan, commit etmeden önce kaldır. ESLint `no-debugger` kuralı ile otomatik yakalanabilir. Production'da `debugger` statement'ı tarayıcının DevTools'u kapalıysa görmezden gelinir ama açıksa uygulamayı durdurur.
:::

:::exercise
**Alıştırma 5: Breakpoint ile Debugging**

1. Aşağıdaki kodu bir JS dosyasına kaydet veya Console'da çalıştır:

```javascript
function findBug(numbers) {
  let sum = 0;
  for (let i = 0; i <= numbers.length; i++) { // Bug burada!
    sum += numbers[i];
  }
  return sum;
}

const result = findBug([10, 20, 30, 40, 50]);
console.log("Toplam:", result); // NaN çıkıyor!
```

2. Sources tab'ında `sum += numbers[i]` satırına breakpoint koy
3. Kodu tekrar çalıştır ve her adımda `i`, `numbers[i]`, ve `sum` değerlerini izle
4. `i === 5` olduğunda `numbers[5]` değerinin `undefined` olduğunu gör
5. Bug'ı bul: `i <= numbers.length` yerine `i < numbers.length` olmalı

**Amaç:** Breakpoint kullanarak off-by-one hatasını tespit etmek.
:::

### Performance Tab: Performans Analizi

:::code[text]{title="Performance Tab Kullanım Rehberi"}
PERFORMANS KAYDI ALMA:

1. Performance tab'ını aç
2. Record (⚫) butonuna tıkla
3. Sayfada etkileşimde bulun (tıkla, scroll yap, sayfa geç)
4. Stop butonuna tıkla
5. Flame chart'ı analiz et

FLAME CHART OKUMA:
┌─────────────────────────────────────────────┐
│ Main Thread                                  │
│ ┌─────────────────────────────────┐          │
│ │ Task (200ms)                     │          │
│ │ ┌───────────────────────┐       │          │
│ │ │ Function Call (150ms) │       │          │
│ │ │ ┌─────────┐┌────────┐│       │          │
│ │ │ │render() ││layout()││       │          │
│ │ │ │  80ms   ││ 70ms   ││       │          │
│ │ │ └─────────┘└────────┘│       │          │
│ │ └───────────────────────┘       │          │
│ └─────────────────────────────────┘          │
└─────────────────────────────────────────────┘

- Geniş bloklar = uzun süren işlemler
- Kırmızı üçgen = long task (50ms+)
- Sarı = JavaScript çalışması
- Mor = Layout/Rendering
- Yeşil = Paint

ÖNEMLİ METRİKLER:
- FCP (First Contentful Paint): İlk içerik gösterilme süresi
- LCP (Largest Contentful Paint): En büyük içerik gösterilme süresi
- CLS (Cumulative Layout Shift): Sayfa kayma miktarı
- TBT (Total Blocking Time): Ana thread'in bloklandığı toplam süre
:::

:::exercise
**Alıştırma 6: Performans Analizi**

1. Performance tab'ını aç
2. "Record" butonuna tıkla
3. Console'da bu yavaş kodu çalıştır:

```javascript
// Kasıtlı olarak yavaş bir işlem
function slowFunction() {
  const start = performance.now();
  let result = 0;
  for (let i = 0; i < 50000000; i++) {
    result += Math.sqrt(i);
  }
  console.log(`Süre: ${(performance.now() - start).toFixed(2)}ms`);
  return result;
}
slowFunction();
```

4. "Stop" butonuna tıkla
5. Flame chart'ta sarı JavaScript bloğunu bul - `slowFunction` adını gör
6. Bottom-Up tab'ında hangi fonksiyonun en çok zaman harcadığını gör

**Amaç:** Performance tab ile yavaş kod tespit etmeyi öğrenmek.
:::

## Node.js Debugging

### Node.js --inspect Flag

:::code[bash]{title="Node.js Debugger Başlatma"}
# 1. Inspect mode ile başlat
$ node --inspect server.js
# Çıktı: Debugger listening on ws://127.0.0.1:9229/xxxx

# 2. İlk satırda dur (breakpoint olmadan)
$ node --inspect-brk server.js
# Kod ilk satırda durur, breakpoint koyabilirsin

# 3. Chrome'da debug et
# chrome://inspect adresine git
# "Open dedicated DevTools for Node" tıkla
# Sources tab'ında breakpoint koy ve debug et

# 4. VS Code ile debug et (EN PRATİK YÖNTEM)
# launch.json oluştur (aşağıda detaylı)
:::

### VS Code Debugger

:::code[json]{title="VS Code launch.json Konfigürasyonları"}
{
  "version": "0.2.0",
  "configurations": [
    // 1. Node.js uygulamasını debug et
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Node App",
      "program": "${workspaceFolder}/server.js",
      "env": {
        "NODE_ENV": "development",
        "PORT": "8000"
      }
    },

    // 2. Mevcut çalışan Node process'e bağlan
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Process",
      "port": 9229
    },

    // 3. Jest testlerini debug et
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Jest Tests",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["--runInBand", "--no-cache", "${file}"],
      "console": "integratedTerminal"
    },

    // 4. Next.js uygulamasını debug et
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Next.js",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 9229,
      "console": "integratedTerminal"
    },

    // 5. Python FastAPI debug et
    {
      "type": "debugpy",
      "request": "launch",
      "name": "Debug FastAPI",
      "module": "uvicorn",
      "args": ["main:app", "--reload", "--port", "8000"],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    }
  ]
}
:::

:::code[text]{title="VS Code Debugger Kullanımı"}
VS CODE DEBUGGER KISA YOLLARI:

F5            → Debug başlat / devam et (Resume)
F9            → Breakpoint koy / kaldır (Toggle)
F10           → Step Over (sonraki satıra geç)
F11           → Step Into (fonksiyon içine gir)
Shift+F11     → Step Out (fonksiyondan çık)
Shift+F5      → Debug durdur

SOL PANELDEKİ BÖLÜMLER:
1. Variables:  Mevcut scope'taki tüm değişkenler
2. Watch:      İzlemek istediğin ifadeler (sağ tık → Add Watch)
3. Call Stack: Fonksiyon çağrı zinciri
4. Breakpoints: Tüm breakpoint'ler listesi

DEBUG CONSOLE (Alt panel):
- Breakpoint'te durduğunda expression çalıştırabilirsin
- Değişken değerlerini sorgulayabilirsin
- Fonksiyon çağırabilirsin
:::

:::exercise
**Alıştırma 7: VS Code Debugger Pratiği**

1. Yeni bir dosya oluştur: `debug-practice.js`

```javascript
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

function processNumbers(numbers) {
  const results = [];
  for (const num of numbers) {
    const fib = fibonacci(num);
    results.push({ number: num, fibonacci: fib });
  }
  return results;
}

const input = [5, 8, 12, 3, 7];
const output = processNumbers(input);
console.log("Sonuçlar:", output);
```

2. `fibonacci` fonksiyonunun `return` satırına breakpoint koy
3. F5 ile debug başlat
4. Call Stack panelinde recursive çağrıları gözlemle
5. Variables panelinde `n` değerini her adımda kontrol et
6. Watch'a `n <= 1` ifadesini ekle

**Amaç:** VS Code debugger ile recursive fonksiyonları debug etmek.
:::

## Hata Mesajlarını Okuma Sanatı

### JavaScript Error Türleri

:::code[javascript]{title="Yaygın JavaScript Hataları"}
// 1. TypeError - Yanlış tip üzerinde işlem yapma
const user = null;
console.log(user.name);
// TypeError: Cannot read properties of null (reading 'name')
// ÇÖZÜM: Optional chaining kullan: user?.name

const num = 42;
num.toUpperCase();
// TypeError: num.toUpperCase is not a function
// ÇÖZÜM: Tip kontrolü yap veya doğru metodu kullan

// 2. ReferenceError - Tanımlanmamış değişken kullanma
console.log(undefinedVar);
// ReferenceError: undefinedVar is not defined
// ÇÖZÜM: Değişkeni tanımla veya yazım hatasını düzelt

// 3. SyntaxError - Kod yazım hatası
// JSON.parse('{"name": "Ali",}');
// SyntaxError: Unexpected token } in JSON
// ÇÖZÜM: Trailing comma'yı kaldır

// const x = ;
// SyntaxError: Unexpected token ;
// ÇÖZÜM: Değer ata

// 4. RangeError - Geçersiz aralık
const arr = new Array(-1);
// RangeError: Invalid array length
// ÇÖZÜM: Pozitif sayı kullan

// 5. URIError - Geçersiz URI işlemi
decodeURIComponent('%');
// URIError: URI malformed
// ÇÖZÜM: Geçerli encoded string kullan
:::

### Stack Trace Okuma

:::code[text]{title="Stack Trace Nasıl Okunur"}
HATA MESAJI:
TypeError: Cannot read properties of undefined (reading 'email')
    at getUserEmail (user-service.js:25:18)
    at processUser (app.js:42:12)
    at handleSubmit (form.js:15:5)
    at HTMLFormElement.<anonymous> (form.js:8:3)

OKUMA SIRASI (AŞAĞIDAN YUKARI):

4. form.js:8:3    → Form'un submit event listener'ı çalıştı
3. form.js:15:5   → handleSubmit fonksiyonu çağrıldı
2. app.js:42:12   → processUser fonksiyonu çağrıldı
1. user-service.js:25:18 → getUserEmail fonksiyonunda HATA oluştu

HATA ANALİZİ:
- "Cannot read properties of undefined" → Bir değişken undefined
- "(reading 'email')" → undefined olan şeyin .email property'sine erişmeye çalışıyor
- "user-service.js:25:18" → Dosya: user-service.js, Satır: 25, Karakter: 18
- O satıra git ve hangi değişkenin undefined olduğunu bul
:::

:::must-note
**MUTLAKA NOT AL:** Stack trace'i **yukarıdan aşağı** oku ama **aşağıdan yukarı** analiz et. En üstteki satır hatanın oluştuğu yer, alttakiler onu çağıran fonksiyonlar. Hata mesajının 3 parçası var: (1) Hata tipi (TypeError), (2) Açıklama (Cannot read properties of undefined), (3) Detay (reading 'email'). Bu 3 parçayı anlamak hatanın %80'ini çözer.
:::

:::exercise
**Alıştırma 8: Stack Trace Okuma Pratiği**

Aşağıdaki hata mesajını oku ve soruları cevapla:

```
Uncaught TypeError: items.filter is not a function
    at filterActiveItems (utils.js:34:22)
    at Dashboard.render (Dashboard.jsx:67:15)
    at finishClassComponent (react-dom.development.js:17485:31)
    at updateClassComponent (react-dom.development.js:17435:24)
```

1. Hata hangi dosyada, hangi satırda oluştu?
2. Hatanın sebebi nedir?
3. Muhtemel çözüm nedir?
4. React framework kodu (react-dom) satırlarını dikkate almalı mısın?

**Çözümler:**
1. `utils.js` dosyası, satır 34
2. `items` değişkeni üzerinde `.filter()` çağrılıyor ama `items` bir array değil (muhtemelen undefined, null veya string)
3. `items`'ın gerçekten bir array olduğundan emin ol: `Array.isArray(items) ? items.filter(...) : []` veya veriyi kontrol et
4. Hayır, `react-dom` satırları framework'ün iç çalışmasıdır. Senin kodun `utils.js:34` ve `Dashboard.jsx:67`'de
:::

## React DevTools

:::concept[React DevTools (İng: React Developer Tools)]
React DevTools, React uygulamalarını debug etmek için kullanılan tarayıcı eklentisidir. Component tree'yi, props'ları, state'i ve hook'ları incelemenizi sağlar.

**Türkçe karşılığı:** React Geliştirici Araçları
**Ne işe yarar:** React component'lerini, props/state'i ve re-render'ları debug et
**Gerçek hayat benzetmesi:** Bir saatin arkasını açıp çarkları görmek gibi - uygulamanın iç mekanizmasını görürsün
:::

:::code[text]{title="React DevTools Kullanım Rehberi"}
KURULUM:
- Chrome Web Store'dan "React Developer Tools" eklentisini kur
- DevTools'ta 2 yeni tab belirir: Components ve Profiler

COMPONENTS TAB:
1. Component Tree:
   - Tüm React component'lerin hiyerarşisini gösterir
   - Component'e tıkla → sağda props, state, hooks görünür
   - Filtreleme: Component adına göre ara

2. Props İnceleme:
   - Her component'in aldığı props'ları gösterir
   - Props değerlerini canlı olarak değiştirebilirsin
   - "Rendered by" ile parent component'i gör

3. State ve Hooks:
   - useState, useReducer değerlerini gösterir
   - useEffect dependency array'ini gösterir
   - State değerlerini canlı olarak değiştirebilirsin

4. Highlight Updates:
   - Settings → "Highlight updates when components render"
   - Re-render olan component'ler yanıp söner
   - Gereksiz re-render'ları tespit et

PROFILER TAB:
1. Record butonuna tıkla
2. Uygulamada etkileşimde bulun
3. Stop butonuna tıkla
4. Her commit'te hangi component'lerin render olduğunu gör
5. Render süresini ölç (sarı = yavaş, mavi = hızlı)
6. "Why did this render?" seçeneğini aç
:::

:::exercise
**Alıştırma 9: React DevTools Pratiği**

Herhangi bir React uygulamasını çalıştır (veya react.dev sitesine git) ve:

1. Components tab'ında component tree'yi gez
2. Bir component seçip props ve state'ini incele
3. State değerini canlı olarak değiştir ve UI'ın güncellendiğini gör
4. Settings'ten "Highlight updates" özelliğini aç
5. Sayfada bir butona tıkla ve hangi component'lerin re-render olduğunu izle
6. Profiler tab'ında bir kayıt al ve en yavaş component'i bul

**Amaç:** React uygulamalarını debug edebilmek.
:::

## Sistematik Debugging Yaklaşımı

:::code[text]{title="Debugging Metodoloisi: 6 Adım"}
ADIM 1: SORUNU TANIMLA
- Tam olarak ne oluyor? Ne olması gerekiyor?
- Hata mesajı var mı? Tam metnini kopyala
- Her seferinde mi oluyor, ara sıra mı?
- Hangi tarayıcıda/cihazda? Sadece belirli koşullarda mı?

ADIM 2: YENİDEN ÜRET (REPRODUCE)
- Hatayı güvenilir şekilde tekrarlayabilmeli misin?
- Minimum adımları bul (en az kaç adımda hata oluşuyor?)
- İzole et: Başka değişkenleri ortadan kaldır

ADIM 3: HİPOTEZ KUR
- "Muhtemelen X yüzünden oluyor" de
- En olası nedeni düşün:
  - Veri yanlış mı? (API response'u kontrol et)
  - Tip yanlış mı? (typeof ile kontrol et)
  - Zamanlama sorunu mu? (async/await eksik mi?)
  - Koşul yanlış mı? (if/else logic kontrol et)

ADIM 4: TEST ET
- Hipotezini doğrula veya çürüt
- console.log / breakpoint ile veriyi kontrol et
- Binary search: Kodun ortasına log koy,
  doğruysa alt yarıda, yanlışsa üst yarıda ara

ADIM 5: DÜZELT
- Root cause'u bul, semptoma değil nedene müdahale et
- Düzeltmeden önce test yaz (TDD)
- Düzeltmenin başka bir şeyi bozmadığını kontrol et

ADIM 6: ÖĞREN VE BELGELE
- Bu hatadan ne öğrendin?
- Aynı hatayı önleyecek bir test var mı?
- Takıma paylaşılacak bir ders var mı?
:::

:::exercise
**Alıştırma 10: Bug Hunt Challenge**

Aşağıdaki kodda 5 bug var. Hepsini bul ve düzelt:

```javascript
async function fetchUserData(userId) {
  const response = fetch(`/api/users/${userId}`);  // Bug 1

  if (response.status === 200) {
    const data = response.json();  // Bug 2
    return {
      name: data.name,
      email: data.email,
      age: data.age,
      isAdult: data.age > 18,  // Bug 3
    };
  } else {
    console.log("Hata olustu");  // Bug 4
    return null;
  }
}

// Kullanım
const user = fetchUserData(1);  // Bug 5
console.log(user.name);
```

**Çözümler:**

Bug 1: `fetch` async fonksiyondur, `await` eksik
```javascript
const response = await fetch(`/api/users/${userId}`);
```

Bug 2: `.json()` da async, `await` eksik
```javascript
const data = await response.json();
```

Bug 3: 18 yaşındaki kişi yetişkindir, `>=` olmalı
```javascript
isAdult: data.age >= 18,
```

Bug 4: Hata durumunda `console.error` kullanılmalı ve hata bilgisi verilmeli
```javascript
console.error(`API Error: ${response.status} ${response.statusText}`);
```

Bug 5: `fetchUserData` async fonksiyon, `await` ile çağrılmalı
```javascript
const user = await fetchUserData(1);
// veya
fetchUserData(1).then(user => console.log(user?.name));
```
:::

:::exercise
**Alıştırma 11: Gerçek Dünya Debugging Senaryosu**

Bir e-ticaret sitesinde kullanıcılar "Sepete Ekle" butonuna tıklıyor ama sepet güncellenmiyor. Nasıl debug edersin? Adım adım yaz.

**Çözüm Adımları:**

1. **Console'u kontrol et:** Kırmızı hata mesajı var mı?
2. **Network tab'ını aç:** "Add to cart" API isteği gidiyor mu?
   - İstek gitmiyor → Event listener çalışmıyor (Elements tab'ında kontrol et)
   - İstek gidiyor, 4xx/5xx → Backend hatası (response body'yi oku)
   - İstek gidiyor, 200 → Response doğru mu kontrol et
3. **React DevTools:** Cart component'inin state'ini kontrol et
   - State güncellenmiyor → setState/dispatch çağrısını kontrol et
   - State güncelleniyor ama UI değişmiyor → Re-render sorunu (prop drilling, context)
4. **Breakpoint koy:** "Add to cart" handler fonksiyonuna breakpoint koy
   - Fonksiyon çağrılıyor mu?
   - Parametreler doğru mu? (productId, quantity)
5. **Network response'u kontrol et:**
   - Response'ta expected veri var mı?
   - Veri formatı frontend'in beklediğiyle uyuşuyor mu?
:::

:::exercise
**Alıştırma 12: DevTools Keyboard Shortcuts**

Aşağıdaki keyboard shortcut'ları ezberle ve her birini en az 3 kez dene:

| Kısayol | İşlev |
|---------|-------|
| `F12` veya `Ctrl+Shift+I` | DevTools aç/kapat |
| `Ctrl+Shift+C` | Element picker |
| `Ctrl+Shift+J` | Console'a doğrudan git |
| `Ctrl+Shift+M` | Responsive mode (device toolbar) |
| `Ctrl+L` (Console'da) | Console'u temizle |
| `Ctrl+P` (Sources'ta) | Dosya ara |
| `Ctrl+Shift+F` | Tüm dosyalarda ara |
| `Esc` | Drawer paneli aç/kapat |
| `Ctrl+[` / `Ctrl+]` | Tab'lar arası geç |

**Amaç:** DevTools'u mouse kullanmadan hızlıca kontrol edebilmek.
:::

## Interview Soruları

:::interview
**Soru 1:** Bir web sayfası yavaş yükleniyor. Nasıl debug edersin?
**Cevap:** Network tab'ında Waterfall sütununa bakarak en uzun süren istekleri bulurum. Performance tab ile flame chart kaydı alırım. Core Web Vitals (LCP, FID, CLS) metriklerini kontrol ederim. Lighthouse audit çalıştırırım. Özellikle bundle size, gereksiz API çağrıları, render-blocking kaynaklar ve büyük resim dosyalarını kontrol ederim.

**Soru 2:** CORS nedir ve nasıl çözersin?
**Cevap:** CORS, tarayıcının farklı origin'den gelen istekleri engellemesidir. Origin = protocol + domain + port. Çözüm backend tarafındadır: Response header'larına `Access-Control-Allow-Origin` eklenir. Development'ta proxy kullanılabilir. Preflight (OPTIONS) request'leri de handle edilmelidir. Frontend'de CORS çözülmez.

**Soru 3:** `TypeError: Cannot read properties of undefined` hatasını nasıl çözersin?
**Cevap:** Stack trace'den hatanın oluştuğu satırı bulurum. O satırda hangi değişkenin undefined olduğunu tespit ederim. Genellikle API response'u beklediğimiz formatta gelmemiştir veya nested object erişiminde ara bir property undefined'dır. Optional chaining (?.), nullish coalescing (??), veya veri validasyonu ile çözülür.

**Soru 4:** React component'inin gereksiz re-render olduğunu nasıl tespit edersin?
**Cevap:** React DevTools'un Profiler tab'ını kullanırım. "Highlight updates" özelliğini açarım. "Why did this render?" bilgisine bakarım. Genellikle props referansının her render'da değişmesi (inline object/function), context değişimi veya parent re-render'ı sebeptir. Çözüm: React.memo, useMemo, useCallback kullanımı.

**Soru 5:** Production'da bir hata oluştuğunda nasıl debug edersin?
**Cevap:** Önce error monitoring tool'daki (Sentry, LogRocket) hata raporuna bakarım. Stack trace, kullanıcı bilgisi, tarayıcı bilgisi ve hata öncesi kullanıcı aksiyonlarını incelerim. Hatayı local'de reproduce etmeye çalışırım. Source map'ler ile minified kodun orijinal satırını bulurum. Gerekirse feature flag ile hotfix deploy ederim.
:::

:::ai-guidance
**AI ile Debugging Pratiği:**

1. **Hata Mesajı Analizi:** AI'ya console'daki hata mesajını yapıştır ve "Bu hatanın sebebi ve çözümü ne?" diye sor.

2. **Code Review:** Yazdığın kodu AI'ya gönder ve "Bu kodda potansiyel buglar var mı?" diye sor.

3. **Debug Senaryosu:** AI'dan "Bana bir debugging senaryosu ver" de. AI sana bozuk kod verir, sen debug edersin.

4. **Stack Trace Pratiği:** AI'ya stack trace'ler gönder ve "Bu stack trace ne diyor?" diye sor. Zamanla stack trace okumayı öğrenirsin.

5. **Performance Analizi:** AI'ya yavaş kodunu gönder ve "Bu kodu nasıl optimize ederim?" diye sor.
:::

:::senior-learns
Senior/CTO debugging'de **observability** kavramını bilir. Production debugging üç bacak üzerinde durur:
- **Logs:** Structured logging (JSON format), log levels (debug, info, warn, error), correlation ID ile request tracking
- **Metrics:** Response time, error rate, throughput, CPU/memory usage - Prometheus/Grafana ile
- **Traces:** Distributed tracing (OpenTelemetry) ile microservice'ler arası request akışını izleme

Bu üçlü olmadan production debugging kör uçuştur. Development'ta DevTools yeterlidir, ama production'da bu araçlar hayat kurtarır.
:::

## Özet ve Yol Haritası

Bu derste debugging ve troubleshooting becerilerini öğrendin:

1. **Chrome DevTools** - Elements, Console, Network, Sources, Performance tab'ları
2. **Console Metodları** - log, error, table, time, group, assert, trace
3. **Breakpoint Debugging** - Line, conditional, DOM, XHR breakpoint'ler
4. **Node.js Debugging** - --inspect flag, VS Code debugger
5. **Hata Mesajları** - TypeError, ReferenceError, SyntaxError okuma
6. **Stack Trace** - Yukarıdan aşağı oku, aşağıdan yukarı analiz et
7. **CORS Debugging** - CORS hatalarını anlama ve çözme
8. **React DevTools** - Component tree, props, state, Profiler
9. **Network Debugging** - Status kodları, timing, throttling
10. **Sistematik Yaklaşım** - Tanımla, reproduce et, hipotez kur, test et, düzelt

Debugging bir kas gibidir - ne kadar çok pratik yaparsan o kadar güçlenir. Her gün DevTools'u açarak çalış, her hatayı bir öğrenme fırsatı olarak gör.
