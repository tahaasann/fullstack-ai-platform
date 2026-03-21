---
title: "Node.js Runtime ve Express.js Framework"
id: mod-09-node/lesson-01
estimated_minutes: 55
order: 1
tags: ["nodejs", "express", "event-loop", "middleware", "backend"]
prerequisites: ["mod-02-python/lesson-01"]
---

# Node.js Runtime ve Express.js Framework

:::realworld
Node.js, dünyanın en popüler backend runtime'larından biri. Netflix, PayPal, LinkedIn, Uber ve NASA gibi devler Node.js kullanıyor. PayPal, Java'dan Node.js'e geçtiğinde response time'ı %35 düşürdü ve geliştirme hızını 2 katına çıkardı. Bu derste Node.js'in neden bu kadar güçlü olduğunu, event loop mekanizmasını ve Express.js ile profesyonel web sunucular yazmayı öğreneceksin.
:::

## Neden Node.js?

Node.js, JavaScript'i tarayıcı dışında çalıştırmamızı sağlayan bir runtime environment'tır. Google Chrome'un V8 JavaScript engine'i üzerine inşa edilmiştir. Peki neden bir backend dili olarak JavaScript?

- **Tek dil:** Frontend ve backend aynı dilde yazılır (full-stack JavaScript)
- **Non-blocking I/O:** Binlerce eşzamanlı bağlantıyı tek thread ile yönetir
- **NPM ekosistemi:** 2 milyondan fazla paket ile dünyanın en büyük paket ekosistemi
- **Hızlı prototipleme:** Startup'lar ve MVP'ler için ideal geliştirme hızı

:::deha-tip
Deha seviyesi geliştiriciler, "Node.js tek thread'dir" cümlesini duyduklarında bunu bir dezavantaj olarak değil, mimari bir karar olarak değerlendirir. Event loop ve non-blocking I/O sayesinde Node.js, thread management overhead'ı olmadan binlerce concurrent bağlantıyı yönetir. Ama CPU-intensive işler için worker threads veya child process kullanmayı da bilirler.
:::

## Node.js Runtime: Event Loop

:::concept[Event Loop (İng: Event Loop)]
Event loop, Node.js'in non-blocking I/O operasyonlarını yönetmek için kullandığı mekanizmadır. Tek bir thread üzerinde çalışarak, asenkron işlemleri koordine eder.

**Türkçe karşılığı:** Olay Döngüsü
**Ne işe yarar:** I/O operasyonlarını (dosya okuma, veritabanı sorgusu, HTTP isteği) bloklamadan yönetir
**Gerçek hayat benzetmesi:** Bir restoran garsonu gibi düşün - garson sipariş alır, mutfağa iletir ve siparişin hazırlanmasını beklemeden diğer masalara geçer. Sipariş hazır olunca masaya servis yapar.
:::

:::code[text]{title="Event Loop Fazları"}
   ┌───────────────────────────┐
┌─>│         timers             │  → setTimeout, setInterval callback'leri
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks     │  → I/O callback'leri (önceki iterasyondan)
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare       │  → Dahili kullanım
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │          poll              │  → Yeni I/O event'lerini bekle ve işle
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │          check             │  → setImmediate callback'leri
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     close callbacks       │  → socket.on('close', ...) gibi
│  └─────────────┬─────────────┘
└─────────────────┘
:::

### Non-Blocking I/O

:::code[javascript]{title="Blocking vs Non-Blocking I/O"}
// ❌ BLOCKING (Senkron) - Diğer istekler bekler
const data = fs.readFileSync('/dosya.txt', 'utf8');
console.log(data);
console.log('Bu satır dosya okunana kadar bekler');

// ✅ NON-BLOCKING (Asenkron) - Diğer istekler etkilenmez
fs.readFile('/dosya.txt', 'utf8', (err, data) => {
  if (err) throw err;
  console.log(data);
});
console.log('Bu satır dosya okunmadan hemen çalışır');

// ✅ Modern async/await yaklaşımı
const { readFile } = require('fs/promises');

async function dosyaOku() {
  try {
    const data = await readFile('/dosya.txt', 'utf8');
    console.log(data);
  } catch (err) {
    console.error('Dosya okunamadı:', err.message);
  }
}
:::

:::beginner-mistake
Yaygın hata: Event loop'u "çoklu thread" ile karıştırmak. Node.js ana thread'i tektir. Ancak libuv kütüphanesi aracılığıyla arka planda bir thread pool (varsayılan 4 thread) kullanır. Bu thread pool dosya sistemi operasyonları ve DNS lookup gibi işler için kullanılır. Network I/O ise OS kernel'in asenkron mekanizmalarıyla (epoll, kqueue, IOCP) yönetilir.
:::

## Streams ve Buffers

:::concept[Stream (İng: Stream)]
Stream, veriyi parça parça (chunk) işlemek için kullanılan bir soyutlamadır. Büyük dosyaları tamamını belleğe yüklemeden işlemeyi sağlar.

**Türkçe karşılığı:** Akış
**Ne işe yarar:** Büyük veri setlerini bellek verimli şekilde işler
**Gerçek hayat benzetmesi:** YouTube videosu gibi - videonun tamamının inmesini beklemezsin, gelen parçalar anında oynatılır
:::

:::code[javascript]{title="Stream Türleri ve Kullanımı"}
const fs = require('fs');
const { pipeline } = require('stream/promises');
const zlib = require('zlib');

// 4 tür stream vardır:
// 1. Readable  - Veri okunabilir (fs.createReadStream, HTTP request)
// 2. Writable  - Veri yazılabilir (fs.createWriteStream, HTTP response)
// 3. Duplex    - Hem okunabilir hem yazılabilir (TCP socket)
// 4. Transform - Veriyi dönüştüren (zlib compression, crypto)

// Büyük dosyayı stream ile kopyalama
const readStream = fs.createReadStream('buyuk-dosya.csv');
const writeStream = fs.createWriteStream('kopya.csv');

readStream.pipe(writeStream);

// Modern pipeline kullanımı (hata yönetimi dahil)
async function kompresEt() {
  await pipeline(
    fs.createReadStream('veri.json'),
    zlib.createGzip(),
    fs.createWriteStream('veri.json.gz')
  );
  console.log('Dosya sıkıştırıldı');
}
:::

:::concept[Buffer (İng: Buffer)]
Buffer, binary veriyi temsil eden sabit boyutlu bir bellek alanıdır. Dosya okuma, network iletişimi ve kriptografi işlemlerinde kullanılır.

**Türkçe karşılığı:** Tampon Bellek
**Ne işe yarar:** Raw binary veriyi (resimler, dosyalar, network paketleri) JavaScript'te işlemeyi sağlar
**Gerçek hayat benzetmesi:** Kargo deposu gibi - paketler gelir, geçici olarak depolanır ve sırayla işlenir
:::

:::code[javascript]{title="Buffer Kullanımı"}
// Buffer oluşturma
const buf1 = Buffer.from('Merhaba Dünya', 'utf8');
const buf2 = Buffer.alloc(10); // 10 byte sıfırlanmış buffer
const buf3 = Buffer.allocUnsafe(10); // Hızlı ama temizlenmemiş

console.log(buf1.toString());        // 'Merhaba Dünya'
console.log(buf1.length);            // 15 (UTF-8'de Türkçe karakterler 2 byte)
console.log(buf1.toString('base64')); // Base64 encoding

// Buffer birleştirme
const combined = Buffer.concat([buf1, Buffer.from(' - Node.js')]);
:::

## Express.js: Web Framework

Express.js, Node.js için minimal ve esnek bir web uygulama framework'üdür. HTTP sunucu oluşturmayı ve route yönetimini kolaylaştırır.

:::code[javascript]{title="Express.js Temel Kurulum"}
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Built-in middleware'ler
app.use(express.json());               // JSON body parsing
app.use(express.urlencoded({ extended: true })); // URL-encoded form data
app.use(express.static('public'));      // Statik dosya servisi

// Basit route
app.get('/', (req, res) => {
  res.json({ message: 'Merhaba Dünya!' });
});

// Sunucuyu başlat
app.listen(PORT, () => {
  console.log(`Sunucu http://localhost:${PORT} adresinde çalışıyor`);
});
:::

### Routing

:::code[javascript]{title="Express Routing Detaylı"}
const express = require('express');
const router = express.Router();

// HTTP Method'ları ile CRUD işlemleri
router.get('/users', (req, res) => {
  // Query parameters: /users?page=1&limit=10
  const { page = 1, limit = 10 } = req.query;
  res.json({ page: Number(page), limit: Number(limit) });
});

router.get('/users/:id', (req, res) => {
  // URL parameters: /users/123
  const { id } = req.params;
  res.json({ userId: id });
});

router.post('/users', (req, res) => {
  // Request body
  const { name, email } = req.body;
  res.status(201).json({ message: 'Kullanıcı oluşturuldu', name, email });
});

router.put('/users/:id', (req, res) => {
  res.json({ message: `Kullanıcı ${req.params.id} güncellendi` });
});

router.patch('/users/:id', (req, res) => {
  res.json({ message: `Kullanıcı ${req.params.id} kısmen güncellendi` });
});

router.delete('/users/:id', (req, res) => {
  res.status(204).send(); // No Content
});

// Router'ı ana uygulamaya bağla
app.use('/api/v1', router);
// Sonuç: /api/v1/users, /api/v1/users/:id
:::

### Request ve Response Objeleri

:::code[javascript]{title="Request ve Response API"}
app.get('/example', (req, res) => {
  // REQUEST objesi - Gelen istek bilgileri
  console.log(req.method);          // 'GET'
  console.log(req.url);             // '/example?key=val'
  console.log(req.path);            // '/example'
  console.log(req.query);           // { key: 'val' }
  console.log(req.params);          // Route parametreleri
  console.log(req.body);            // POST/PUT body
  console.log(req.headers);         // Tüm header'lar
  console.log(req.get('Content-Type')); // Belirli header
  console.log(req.ip);              // Client IP adresi
  console.log(req.cookies);         // Cookie'ler (cookie-parser ile)

  // RESPONSE objesi - Yanıt gönderme
  res.status(200);                  // Status code ayarla
  res.set('X-Custom-Header', 'value'); // Header ekle
  res.json({ data: 'JSON yanıt' }); // JSON gönder
  // res.send('Text yanıt');        // Text gönder
  // res.sendFile('/path/to/file'); // Dosya gönder
  // res.redirect('/other-route');  // Yönlendir
  // res.download('/path/to/file'); // Dosya indirtir
});
:::

## Middleware Pattern

:::concept[Middleware (İng: Middleware)]
Middleware, request ve response arasında çalışan fonksiyonlardır. Her middleware, request objesini (req), response objesini (res) ve bir sonraki middleware'e geçiş fonksiyonunu (next) alır.

**Türkçe karşılığı:** Ara Katman Yazılımı
**Ne işe yarar:** İstek işleme hattına modüler fonksiyonlar ekler (auth, logging, validation vb.)
**Gerçek hayat benzetmesi:** Havalimanı güvenlik kontrolleri gibi - pasaport kontrolü, bagaj taraması, biniş kartı kontrolü sırayla yapılır. Her kontrol noktası bir middleware'dir.
:::

:::code[text]{title="Middleware Zinciri (Chain)"}
Request → [Logger] → [Auth] → [Validator] → [Route Handler] → Response
           next()    next()     next()          res.json()

Her middleware ya next() çağırarak bir sonrakine geçer,
ya da response göndererek zinciri sonlandırır.
:::

### Built-in Middleware

:::code[javascript]{title="Express Built-in Middleware'ler"}
const express = require('express');
const app = express();

// JSON body parser - Content-Type: application/json
app.use(express.json({ limit: '10mb' }));

// URL-encoded parser - HTML form verileri
app.use(express.urlencoded({ extended: true }));

// Statik dosya servisi - public/ klasörü
app.use(express.static('public'));
// /images/logo.png → public/images/logo.png dosyasını sunar
:::

### Third-Party Middleware

:::code[javascript]{title="Popüler Third-Party Middleware'ler"}
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');

// CORS - Cross-Origin Resource Sharing
app.use(cors({
  origin: ['http://localhost:3000', 'https://myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,
}));

// Helmet - HTTP güvenlik header'ları
app.use(helmet());

// Morgan - HTTP request logger
app.use(morgan('combined'));      // Production
app.use(morgan('dev'));           // Development

// Compression - Gzip sıkıştırma
app.use(compression());
:::

### Custom Middleware Yazma

:::code[javascript]{title="Custom Middleware Örnekleri"}
// 1. Request Logger Middleware
function requestLogger(req, res, next) {
  const start = Date.now();

  // Response tamamlandığında süreyi logla
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(
      `${req.method} ${req.originalUrl} ${res.statusCode} - ${duration}ms`
    );
  });

  next(); // Bir sonraki middleware'e geç
}

// 2. Auth Middleware
function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Token gerekli' });
    // next() çağrılMIYOR - zincir burada durur
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded; // Request objesine kullanıcı bilgisi ekle
    next(); // Doğrulandı, devam et
  } catch (err) {
    return res.status(403).json({ error: 'Geçersiz token' });
  }
}

// 3. Role-based Authorization Middleware (Factory Pattern)
function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Yetkiniz yok' });
    }
    next();
  };
}

// Middleware'leri kullanma
app.use(requestLogger); // Tüm route'lara uygula

app.get('/profile', authenticate, (req, res) => {
  res.json({ user: req.user });
});

app.delete('/users/:id', authenticate, authorize('admin'), (req, res) => {
  res.json({ message: 'Kullanıcı silindi' });
});
:::

:::tip
Middleware sırası çok önemlidir. `app.use()` ile eklenen middleware'ler, tanımlandıkları sırada çalışır. Örneğin, logger middleware'ini auth middleware'inden önce tanımlamalısın ki başarısız auth denemelerini de loglayabilesin.
:::

## Error Handling Middleware

:::code[javascript]{title="Express Error Handling"}
// Custom Error Sınıfı
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Route'larda hata fırlatma
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      throw new AppError('Kullanıcı bulunamadı', 404);
    }
    res.json(user);
  } catch (err) {
    next(err); // Error middleware'ine yönlendir
  }
});

// Async handler wrapper (try-catch tekrarını önler)
function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// asyncHandler ile temiz kullanım
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) throw new AppError('Kullanıcı bulunamadı', 404);
  res.json(user);
}));

// ERROR HANDLING MIDDLEWARE (4 parametre - Express bunu error handler olarak tanır)
app.use((err, req, res, next) => {
  console.error('Hata:', err.message);

  // Operational error (beklenen)
  if (err.isOperational) {
    return res.status(err.statusCode).json({
      status: 'error',
      message: err.message,
    });
  }

  // Programming error (beklenmeyen) - detay gösterme
  res.status(500).json({
    status: 'error',
    message: 'Sunucu hatası oluştu',
  });
});

// 404 handler (tüm route'lardan sonra tanımla)
app.use('*', (req, res) => {
  res.status(404).json({
    status: 'error',
    message: `${req.originalUrl} bulunamadı`,
  });
});
:::

:::beginner-mistake
Yaygın hata: Error handling middleware'inde 3 parametre kullanmak. Express, error middleware'ini 4 parametre ile tanır: `(err, req, res, next)`. 3 parametre yazarsan normal middleware olarak çalışır ve hatalar yakalanmaz. `next` kullanmasan bile parametre olarak yazmalısın.
:::

## Framework Karşılaştırması

:::comparison
| Özellik | Express.js | Fastify | Koa | NestJS | FastAPI (Python) |
|---------|-----------|---------|-----|--------|-----------------|
| **Dil** | JavaScript/TS | JavaScript/TS | JavaScript/TS | TypeScript | Python |
| **Performans** | Orta | Yüksek (~2x Express) | Orta | Orta (Express üzeri) | Yüksek |
| **Mimari** | Minimal, unopinionated | Plugin-based | Minimal | Opinionated (Angular-like) | Opinionated |
| **Öğrenme eğrisi** | Düşük | Düşük-Orta | Düşük | Yüksek | Orta |
| **TypeScript** | Opsiyonel | Opsiyonel | Opsiyonel | Native | Type hints |
| **Validation** | Harici (express-validator) | Built-in (JSON Schema) | Harici | Built-in (class-validator) | Built-in (Pydantic) |
| **Ekosistem** | Çok geniş | Büyüyen | Orta | Büyük | Büyük |
| **Kullanım alanı** | Her yer | Yüksek performans API | Lightweight API | Enterprise, büyük proje | Modern Python API |

**Tavsiye:**
- **Öğrenmeye başla:** Express.js (en geniş ekosistem, en çok kaynak)
- **Performans kritikse:** Fastify (JSON schema validation dahil)
- **Enterprise proje:** NestJS (dependency injection, modüler mimari)
- **Python tercih ediyorsan:** FastAPI (modern, hızlı, type-safe)
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Express ile CRUD API (Kolay)

Express.js ile basit bir kullanici yonetim API'si olustur.

```javascript
const express = require("express");
const app = express();
app.use(express.json());

// In-memory veri
let users = [
  { id: 1, name: "Ahmet", email: "ahmet@test.com" },
  { id: 2, name: "Ayse", email: "ayse@test.com" },
];
let nextId = 3;

// TODO: GET /api/health — { status: "ok", timestamp: Date.now(), uptime: process.uptime() }

// TODO: GET /api/users — Tum kullanicilari dondur

// TODO: GET /api/users/:id — Tek kullanici getir (yoksa 404)

// TODO: POST /api/users — Yeni kullanici ekle (name ve email zorunlu, yoksa 400)

// TODO: PUT /api/users/:id — Kullanici guncelle

// TODO: DELETE /api/users/:id — Kullanici sil

app.listen(3000, () => console.log("Server running on port 3000"));
```

**Beklenen Sonuc:** `curl http://localhost:3000/api/users` tum kullanicilari dondurmeli. POST ile yeni kullanici eklenebilmeli. Olmayan id icin 404 donmeli.
**Ipucu:** `app.get("/api/users/:id", (req, res) => { const user = users.find(u => u.id === parseInt(req.params.id)); ... })`

---

### Alistirma 2: Custom Logger Middleware (Orta)

Tum HTTP isteklerini loglayan ve response suresini olcen bir middleware yaz.

```javascript
// TODO: Logger middleware yaz
function logger(req, res, next) {
  const start = Date.now();
  const method = req.method;
  const url = req.originalUrl;

  // Response bittiginde loglama yap
  res.on("finish", () => {
    const duration = Date.now() - start;
    const status = res.statusCode;
    const color = status >= 400 ? "\x1b[31m" : "\x1b[32m"; // kirmizi veya yesil
    console.log(`${color}${method} ${url} ${status} ${duration}ms\x1b[0m`);
  });

  next();
}

// TODO: Request body validator middleware yaz
function validateBody(schema) {
  // schema: { name: "string", email: "string" } gibi basit bir yapi
  return (req, res, next) => {
    // TODO: req.body'de schema'daki tum alanlar var mi kontrol et
    // TODO: Eksik alan varsa 400 + { error: "Missing field: name" } dondur
    // TODO: Tumu varsa next() cagir
  };
}

// Kullanim:
app.use(logger);
app.post("/api/users",
  validateBody({ name: "string", email: "string" }),
  (req, res) => {
    // Controller logic...
  }
);
```

**Beklenen Sonuc:** Her istek renkli olarak loglanmali (basarili=yesil, hatali=kirmizi). Eksik body field'lari icin 400 donmeli. Middleware zinciri dogru calismali.
**Ipucu:** `res.on("finish", callback)` response gonderildikten sonra calisir. `next()` cagirmayi unutma, yoksa request asili kalir.

---

### Alistirma 3: Error Handling ve Async Wrapper (Zor)

Global error handling middleware ve async route'lar icin wrapper fonksiyonu yaz.

```javascript
// Custom error class'lari
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}

class NotFoundError extends AppError {
  constructor(resource = "Resource") {
    super(`${resource} not found`, 404);
  }
}

class ValidationError extends AppError {
  constructor(message) {
    super(message, 400);
  }
}

// TODO: Async wrapper — try/catch'i otomatik yap
const asyncHandler = (fn) => (req, res, next) => {
  // TODO: fn(req, res, next).catch(next) ile hatalari yakala
};

// TODO: Global error handling middleware (4 parametre!)
function errorHandler(err, req, res, next) {
  // TODO: AppError ise statusCode ve mesaji dondur
  // TODO: Diger hatalar icin 500 Internal Server Error dondur
  // TODO: Development'ta stack trace goster, production'da gizle
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    error: {
      message: err.message,
      status: statusCode,
      ...(process.env.NODE_ENV === "development" && { stack: err.stack }),
    },
  });
}

// Kullanim:
app.get("/api/users/:id", asyncHandler(async (req, res) => {
  const user = await findUserById(req.params.id); // Simule edilmis async islem
  if (!user) throw new NotFoundError("User");
  res.json(user);
}));

// 404 handler (tum route'lardan sonra)
app.use((req, res) => {
  throw new NotFoundError("Route");
});

app.use(errorHandler); // En sona ekle!
```

**Beklenen Sonuc:** async route'larda try/catch yazmaya gerek kalmamali (asyncHandler yonetiyor). Custom error class'lari dogru status code'lari dondurmeli. Bilinmeyen route'lar 404 dondurmeli.
**Ipucu:** Error handling middleware MUTLAKA 4 parametre almali (err, req, res, next) — Express bunu bu sekilde taniyor. `app.use(errorHandler)` en son tanimlanmali.
:::

:::knowledge-check
type: multiple_choice
question: "Express.js'te error handling middleware'ini normal middleware'den ayıran şey nedir?"
options:
  - "try-catch bloğu kullanması"
  - "4 parametre alması: (err, req, res, next)"
  - "app.error() ile tanımlanması"
  - "async fonksiyon olması"
correct: 1
explanation: "Express, error handling middleware'ini parametre sayısına göre tanır. 4 parametre (err, req, res, next) alan middleware otomatik olarak error handler olarak kabul edilir. next kullanılmasa bile parametre olarak yazılmalıdır."
:::

:::knowledge-check
type: multiple_choice
question: "Node.js event loop'unda bir I/O operasyonu (dosya okuma) tamamlandığında callback hangi fazda çalıştırılır?"
options:
  - "timers fazı"
  - "poll fazı"
  - "check fazı"
  - "close callbacks fazı"
correct: 1
explanation: "I/O callback'leri poll fazında işlenir. timers fazı setTimeout/setInterval callback'leri için, check fazı setImmediate callback'leri için, close callbacks fazı ise socket.on('close') gibi kapatma event'leri içindir."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "Node.js event loop'unu 6 fazini (timers, pending callbacks, idle/prepare, poll, check, close) bir restoran garsonu analojisiyle acikla. setTimeout, setImmediate ve process.nextTick arasindaki oncelik sirasini orneklerle goster. libuv thread pool ne zaman devreye girer?"

**2. Pratik Uygulama:**
> "Express.js ile bir RESTful API olustur: custom logger middleware, JWT authentication middleware, role-based authorization middleware ve merkezi error handling middleware zincirini kur. asyncHandler wrapper ile try-catch tekrarini onle. Her middleware'in neden o sirada oldugunu acikla."
> Takip: "Simdi bu API'ye stream kullanarak buyuk bir CSV dosyasini parse eden bir endpoint ekle. Dosyayi bellege yuklemeden satir satir isle."

**3. Mukemmellik Icin:**
> "Production'da bir Node.js uygulamasinda memory leak tespit ettim. process.memoryUsage(), --inspect flag'i ile Chrome DevTools heap snapshot ve clinic.js ile profiling yaparak memory leak'i nasil bulurum? Yaygin memory leak kaynaklarini (closure'lar, event listener temizlenmemesi, global degiskenler) ve cozumlerini acikla."

### Pair Programming Ipucu
Express middleware yazarken AI'a hata loglarini goster ve sor: "Bu error stack trace'i analiz et. Hangi middleware'de hata olustu? Error handling middleware'im neden bu hatayi yakalayamadi? 4 parametreli error handler'imi kontrol et."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Node.js'in event loop'u nasil calisir?**
- **Junior cevabi:** Node.js tek thread'dir, event loop async islemleri yonetir.
- **Senior cevabi:** Event loop 6 fazdan olusur: timers (setTimeout/setInterval), pending callbacks, idle/prepare, poll (I/O), check (setImmediate), close callbacks. Her faz kendi FIFO kuyrugundan callback'leri calistirir. Microtask'lar (Promise.then, process.nextTick) her faz gecisinde oncelikli calisir. process.nextTick microtask queue'da Promise'den once gelir. Uzun sureli senkron islemler event loop'u bloke eder, bu yuzden CPU-intensive isler worker_threads veya child_process ile ayrilir. libuv 4 thread'lik pool ile file I/O, DNS lookup gibi islemleri handle eder.

**Soru 2: Express.js'te middleware ne ise yarar ve nasil calisir?**
- **Junior cevabi:** Middleware request ve response arasinda calistirilan fonksiyonlardir.
- **Senior cevabi:** Middleware (req, res, next) imzasina sahiptir ve request pipeline'inda sirayla calisir. Sira onemlidir: CORS middleware auth'dan once gelmeli, error handler en sonda olmalidir (4 parametre: err, req, res, next). Yaygin pattern'ler: authentication (JWT verify), authorization (role check), validation (input sanitize), logging (request/response log), rate limiting, compression. app.use() global, router.use() route-specific middleware atar. next('route') ile ayni route'un bir sonraki handler'ina atlanir.
:::

:::must-note
- Node.js tek thread çalışır ama libuv thread pool (4 thread) ve OS async mekanizmalarıyla non-blocking I/O sağlar
- Event Loop fazları: timers → pending callbacks → idle/prepare → poll → check → close callbacks
- Stream türleri: Readable, Writable, Duplex, Transform - büyük veriyi chunk'lar halinde işler
- Buffer = binary veri temsili, Stream = veriyi parça parça (chunk) işleme
- Express middleware sırası önemlidir: tanımlanma sırasına göre çalışır
- Middleware ya next() çağırır ya da response göndererek zinciri sonlandırır
- Error middleware = 4 parametre (err, req, res, next), normal middleware = 3 parametre
- asyncHandler wrapper fonksiyonu try-catch tekrarını önler
- express.json() → JSON body parse, express.urlencoded() → form data parse, express.static() → dosya servisi
- Router ile modüler route tanımlama: express.Router() → app.use('/prefix', router)
- AppError sınıfı ile operational (beklenen) ve programming (beklenmeyen) hataları ayır
- 404 handler tüm route tanımlarından SONRA yazılmalı
- HTTP method'ları: GET=oku, POST=oluştur, PUT=tamamen güncelle, PATCH=kısmen güncelle, DELETE=sil
:::

:::senior-learns
Bir Senior Developer veya CTO, Node.js ve Express konusunu öğrenirken şu yaklaşımı benimser:

1. **Node.js internals'ı kaynak koddan öğrenir** - libuv'un event loop implementasyonunu, V8'in memory management'ını (heap, stack, garbage collection) ve Node.js'in C++ binding katmanını inceler. `node --inspect` ile Chrome DevTools'u kullanarak memory leak'leri ve CPU profiling yapar.
2. **Cluster modülü ve worker threads kullanır** - Production'da `cluster.fork()` ile CPU core sayısı kadar worker process oluşturur. CPU-intensive işleri (resim işleme, şifreleme) worker threads'e devreder. PM2 gibi process manager'lar ile zero-downtime deployment yapar.
3. **Middleware'i architectural pattern olarak düşünür** - Express middleware zincirini Chain of Responsibility pattern'ı olarak görür. Her middleware'in single responsibility'si olmasını sağlar. Middleware'leri fonksiyonel programlama prensiplerine göre compose eder.
4. **Backpressure ve stream optimization yapar** - Büyük dosya transferlerinde stream backpressure mekanizmasını kontrol eder. `highWaterMark` değerini workload'a göre ayarlar. Memory usage'ı `process.memoryUsage()` ile monitor eder.
5. **Security middleware stack'i oluşturur** - Helmet, CORS, rate limiter, CSRF protection, input sanitization gibi güvenlik middleware'lerini katmanlı olarak uygular. OWASP Top 10'u referans alarak her saldırı vektörü için koruma ekler.
6. **Graceful shutdown implementasyonu yapar** - SIGTERM/SIGINT sinyallerini yakalar, yeni istekleri kabul etmeyi durdurur, mevcut isteklerin tamamlanmasını bekler, veritabanı bağlantılarını kapatır ve process'i temiz şekilde sonlandırır.

**Profesyonel Mindset:** "Express.js'in gücü sadeliğinde. Ama production-ready bir uygulama yazmak, framework'ü bilmekten çok daha fazlasını gerektirir. Error handling strategy'n, logging altyapın, graceful shutdown mekanizman ve security middleware stack'in olmalı. Framework seçiminden çok, bu cross-cutting concern'leri ne kadar iyi implement ettiğin seni junior'dan senior'a taşır."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Runtime** (rʌn-taɪm) → Çalışma zamanı ortamı
   *"Node.js is a JavaScript runtime built on Chrome's V8 engine."*

2. **Event Loop** (ɪ-vent luːp) → Olay döngüsü
   *"The event loop handles asynchronous operations without blocking the main thread."*

3. **Middleware** (mɪd-l-wɛr) → Ara katman yazılımı
   *"Authentication middleware validates the JWT token before the request reaches the route handler."*

4. **Non-blocking I/O** (nɒn-blɒk-ɪŋ aɪ-oʊ) → Bloklamayan giriş/çıkış
   *"Non-blocking I/O allows Node.js to handle thousands of concurrent connections efficiently."*

5. **Stream** (striːm) → Akış
   *"Use streams to process large files without loading them entirely into memory."*

**Okuma Egzersizi:** Node.js resmi dokümantasyonunda "Event Loop" sayfasını oku: https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Express sunucusu kuruldu ve middleware eklendi"
→ Örnek: `feat: set up Express server with logging and auth middleware`
:::

:::external-resource
- 📺 **freeCodeCamp:** "Node.js and Express.js Full Course" (8 saat, YouTube, ücretsiz)
- 📖 **Node.js Docs:** nodejs.org/en/docs (resmi dokümantasyon, ücretsiz)
- 📖 **Express.js Guide:** expressjs.com/en/guide (resmi rehber, ücretsiz)
- 🎮 **NodeSchool:** nodeschool.io (interaktif workshop'lar, ücretsiz)
- 📖 **MDN:** "Express web framework" tutorial serisi (ücretsiz)
:::
