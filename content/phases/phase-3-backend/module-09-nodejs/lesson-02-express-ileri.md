---
title: "Express.js İleri Seviye: Validation, Upload, Logging ve Proje Yapısı"
id: mod-09-node/lesson-02
estimated_minutes: 50
order: 2
tags: ["express", "validation", "multer", "winston", "project-structure", "backend"]
prerequisites: ["mod-09-node/lesson-01"]
---

# Express.js İleri Seviye: Validation, Upload, Logging ve Proje Yapısı

:::realworld
Production'da çalışan bir Express.js uygulaması, basit route tanımlarından çok daha fazlasını gerektirir. Kullanıcıdan gelen verileri doğrulamak, dosya yüklemelerini güvenli yönetmek, her isteği loglamak ve projeyi sürdürülebilir bir yapıda tutmak zorundasın. Bu derste, Express.js uygulamanı production-ready hale getiren araçları ve pratikleri öğreneceksin.
:::

## Neden Bu Konuları Öğreniyorsun?

Bir API yazdığında, dışarıdan gelen her veri potansiyel bir tehdit veya hatadır. Validation yapmadan gelen veriyi veritabanına yazarsan SQL injection, XSS veya veri bütünlüğü sorunlarıyla karşılaşırsın. Logging olmadan production'da hata ayıklayamazsın. Proje yapısı kötüyse, 3 ay sonra kendi kodunu anlayamazsın.

:::deha-tip
Deha seviyesi geliştiriciler, "kod çalışıyor" demekle yetinmez. "Kod production'da güvenli mi? Hata olduğunda debug edebilir miyim? Yeni bir geliştirici projeye hızla adapte olabilir mi?" sorularını sorar. Bu derste öğreneceğin her şey bu soruların cevabıdır.
:::

## Input Validation

### express-validator

:::code[javascript]{title="express-validator ile Validation"}
const { body, param, query, validationResult } = require('express-validator');

// Validation kuralları middleware olarak tanımlanır
const createUserValidation = [
  body('name')
    .trim()
    .notEmpty().withMessage('İsim zorunludur')
    .isLength({ min: 2, max: 50 }).withMessage('İsim 2-50 karakter olmalı'),

  body('email')
    .isEmail().withMessage('Geçerli bir email giriniz')
    .normalizeEmail(),

  body('password')
    .isLength({ min: 8 }).withMessage('Şifre en az 8 karakter olmalı')
    .matches(/[A-Z]/).withMessage('En az bir büyük harf gerekli')
    .matches(/[0-9]/).withMessage('En az bir rakam gerekli')
    .matches(/[!@#$%^&*]/).withMessage('En az bir özel karakter gerekli'),

  body('age')
    .optional()
    .isInt({ min: 18, max: 120 }).withMessage('Yaş 18-120 arasında olmalı'),

  body('role')
    .isIn(['user', 'admin', 'editor']).withMessage('Geçersiz rol'),
];

// Validation sonuçlarını kontrol eden middleware
function validate(req, res, next) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      status: 'error',
      errors: errors.array().map(err => ({
        field: err.path,
        message: err.msg,
      })),
    });
  }
  next();
}

// Route'ta kullanım
app.post('/api/users', createUserValidation, validate, async (req, res) => {
  // Buraya sadece valid veri ulaşır
  const user = await User.create(req.body);
  res.status(201).json(user);
});
:::

### Zod ile Schema-Based Validation

:::code[javascript]{title="Zod ile Type-Safe Validation"}
const { z } = require('zod');

// Schema tanımlama
const createUserSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  password: z.string()
    .min(8)
    .regex(/[A-Z]/, 'En az bir büyük harf gerekli')
    .regex(/[0-9]/, 'En az bir rakam gerekli'),
  age: z.number().int().min(18).max(120).optional(),
  role: z.enum(['user', 'admin', 'editor']).default('user'),
  address: z.object({
    street: z.string(),
    city: z.string(),
    zipCode: z.string().regex(/^\d{5}$/),
  }).optional(),
  tags: z.array(z.string()).max(10).optional(),
});

// Zod middleware factory
function validateBody(schema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        status: 'error',
        errors: result.error.issues.map(issue => ({
          field: issue.path.join('.'),
          message: issue.message,
        })),
      });
    }
    req.body = result.data; // Parsed ve type-safe veri
    next();
  };
}

// Kullanım
app.post('/api/users', validateBody(createUserSchema), async (req, res) => {
  // req.body artık type-safe ve validate edilmiş
  const user = await User.create(req.body);
  res.status(201).json(user);
});
:::

:::comparison
| Özellik | express-validator | Zod |
|---------|------------------|-----|
| **Yaklaşım** | Middleware-based, chain API | Schema-based, declarative |
| **TypeScript** | Kısıtlı tip çıkarımı | Tam tip çıkarımı (z.infer) |
| **Öğrenme eğrisi** | Düşük | Orta |
| **Esneklik** | Çok esnek, custom validator kolay | Schema composition güçlü |
| **Kullanım alanı** | Sadece Express | Framework bağımsız |
| **Performans** | Hızlı | Hızlı |

**Tavsiye:** TypeScript projelerinde Zod tercih et (tip güvenliği için). JavaScript projelerinde express-validator yeterli.
:::

## File Uploads (Multer)

:::concept[Multer (İng: Multer)]
Multer, Express.js için multipart/form-data formatındaki dosya yüklemelerini yöneten bir middleware'dir.

**Türkçe karşılığı:** Dosya yükleme middleware'i
**Ne işe yarar:** Kullanıcıların dosya (resim, PDF, video vb.) yüklemesini güvenli şekilde yönetir
**Gerçek hayat benzetmesi:** Bina girişindeki güvenlik taraması gibi - gelen paketi kontrol eder (boyut, tür), izin verilen paketleri içeri alır, tehlikeli olanları reddeder
:::

:::code[javascript]{title="Multer ile Dosya Yükleme"}
const multer = require('multer');
const path = require('path');
const crypto = require('crypto');

// Storage konfigürasyonu
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    // Güvenli dosya adı oluştur (orijinal adı kullanma!)
    const uniqueName = crypto.randomUUID();
    const ext = path.extname(file.originalname);
    cb(null, `${uniqueName}${ext}`);
  },
});

// Dosya filtresi
const fileFilter = (req, file, cb) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('Sadece JPEG, PNG ve WebP dosyaları kabul edilir'), false);
  }
};

// Multer instance
const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 5 * 1024 * 1024, // 5 MB
    files: 5,                   // Maksimum 5 dosya
  },
});

// Tek dosya yükleme
app.post('/api/avatar', upload.single('avatar'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'Dosya gerekli' });
  }
  res.json({
    message: 'Avatar yüklendi',
    filename: req.file.filename,
    size: req.file.size,
  });
});

// Çoklu dosya yükleme
app.post('/api/gallery', upload.array('photos', 5), (req, res) => {
  res.json({
    message: `${req.files.length} dosya yüklendi`,
    files: req.files.map(f => f.filename),
  });
});
:::

:::beginner-mistake
Yaygın hata: Kullanıcının gönderdiği orijinal dosya adını doğrudan kullanmak. Bu, path traversal saldırılarına açık kapı bırakır (örn: `../../etc/passwd`). Her zaman benzersiz, güvenli bir dosya adı oluştur (UUID veya hash kullanarak).
:::

## Rate Limiting

:::code[javascript]{title="Rate Limiting Uygulaması"}
const rateLimit = require('express-rate-limit');

// Genel rate limiter
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 dakika
  max: 100,                  // Her IP için 100 istek
  standardHeaders: true,     // RateLimit-* header'ları
  legacyHeaders: false,
  message: {
    status: 'error',
    message: 'Çok fazla istek gönderdiniz, 15 dakika sonra tekrar deneyin',
  },
});

// Auth endpoint'leri için daha katı limit
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 15 dakikada en fazla 5 login denemesi
  message: {
    status: 'error',
    message: 'Çok fazla giriş denemesi, 15 dakika sonra tekrar deneyin',
  },
});

app.use('/api/', generalLimiter);
app.use('/api/auth/login', authLimiter);
:::

## CORS Konfigürasyonu

:::code[javascript]{title="CORS Detaylı Konfigürasyon"}
const cors = require('cors');

// Development
app.use(cors()); // Tüm origin'lere izin ver (sadece development!)

// Production - Whitelist yaklaşımı
const allowedOrigins = [
  'https://myapp.com',
  'https://admin.myapp.com',
  'https://staging.myapp.com',
];

app.use(cors({
  origin: (origin, callback) => {
    // origin undefined olabilir (server-to-server, Postman)
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('CORS politikası tarafından engellendi'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true, // Cookie gönderimi için
  maxAge: 86400,     // Preflight cache süresi (24 saat)
}));
:::

## Logging (Winston ve Pino)

:::code[javascript]{title="Winston Logger Kurulumu"}
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'my-api' },
  transports: [
    // Hataları ayrı dosyaya yaz
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 5,
    }),
    // Tüm logları combined dosyasına yaz
    new winston.transports.File({
      filename: 'logs/combined.log',
      maxsize: 5242880,
      maxFiles: 5,
    }),
  ],
});

// Development'ta console'a da yaz
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    ),
  }));
}

// Kullanım
logger.info('Sunucu başlatıldı', { port: 3000 });
logger.warn('Rate limit aşıldı', { ip: '192.168.1.1' });
logger.error('Veritabanı bağlantı hatası', { error: err.message });

// HTTP request logger middleware
function httpLogger(req, res, next) {
  const start = Date.now();
  res.on('finish', () => {
    logger.info('HTTP Request', {
      method: req.method,
      url: req.originalUrl,
      status: res.statusCode,
      duration: `${Date.now() - start}ms`,
      ip: req.ip,
      userAgent: req.get('user-agent'),
    });
  });
  next();
}

app.use(httpLogger);
:::

:::code[javascript]{title="Pino - Yüksek Performanslı Logger"}
const pino = require('pino');
const pinoHttp = require('pino-http');

// Pino, Winston'dan ~5x daha hızlıdır
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV !== 'production'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
});

// Express middleware olarak kullanım
app.use(pinoHttp({ logger }));

// Route'ta kullanım
app.get('/api/users', (req, res) => {
  req.log.info('Kullanıcı listesi istendi');
  res.json(users);
});
:::

:::comparison
| Özellik | Winston | Pino |
|---------|---------|------|
| **Performans** | Orta | Çok yüksek (~5x hızlı) |
| **Çıktı formatı** | Çoklu format desteği | JSON-first |
| **Transport** | Çok sayıda (file, console, HTTP vb.) | Child process transport |
| **Esneklik** | Çok esnek, custom formatlar | Hız odaklı, daha az esnek |
| **Popülerlik** | Çok yaygın | Hızla büyüyen |

**Tavsiye:** Performans kritikse Pino, esneklik ve çeşitli transport gerekiyorsa Winston tercih et.
:::

## Environment Variables ve Config Management

:::code[javascript]{title="dotenv ve Config Yönetimi"}
// .env dosyası (GIT'E EKLEME!)
// PORT=3000
// NODE_ENV=development
// DATABASE_URL=postgres://user:pass@localhost:5432/mydb
// JWT_SECRET=super-secret-key-change-this
// REDIS_URL=redis://localhost:6379

// config.js - Merkezi konfigürasyon
require('dotenv').config();

const config = {
  port: parseInt(process.env.PORT, 10) || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  db: {
    url: process.env.DATABASE_URL,
    pool: {
      min: parseInt(process.env.DB_POOL_MIN, 10) || 2,
      max: parseInt(process.env.DB_POOL_MAX, 10) || 10,
    },
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '24h',
  },
  cors: {
    origins: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3000'],
  },
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW, 10) || 15 * 60 * 1000,
    max: parseInt(process.env.RATE_LIMIT_MAX, 10) || 100,
  },
};

// Zorunlu değişkenleri kontrol et
const requiredEnvVars = ['DATABASE_URL', 'JWT_SECRET'];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`${envVar} environment variable tanımlanmamış!`);
  }
}

module.exports = config;
:::

:::code[text]{title=".env.example Dosyası (Git'e ekle)"}
# Server
PORT=3000
NODE_ENV=development

# Database
DATABASE_URL=postgres://user:password@localhost:5432/mydb

# Authentication
JWT_SECRET=change-this-to-a-secure-random-string
JWT_EXPIRES_IN=24h

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Rate Limiting
RATE_LIMIT_WINDOW=900000
RATE_LIMIT_MAX=100
:::

:::tip
Her zaman `.env.example` dosyası oluştur ve git'e ekle. Bu dosya gerçek değerler yerine placeholder'lar içerir ve yeni geliştiricilere hangi environment variable'ların gerekli olduğunu gösterir. `.env` dosyasını asla git'e ekleme - `.gitignore`'a ekle.
:::

## Project Structure Best Practices

:::code[text]{title="Layered Architecture - Proje Yapısı"}
my-express-app/
├── src/
│   ├── config/
│   │   ├── index.js          # Merkezi konfigürasyon
│   │   └── database.js       # Veritabanı bağlantısı
│   ├── middleware/
│   │   ├── auth.js            # Authentication middleware
│   │   ├── validate.js        # Validation middleware
│   │   ├── errorHandler.js    # Error handling middleware
│   │   └── rateLimiter.js     # Rate limiting
│   ├── routes/
│   │   ├── index.js           # Route birleştirici
│   │   ├── auth.routes.js     # Auth route'ları
│   │   └── user.routes.js     # User route'ları
│   ├── controllers/
│   │   ├── auth.controller.js # Auth iş mantığı (ince katman)
│   │   └── user.controller.js # User iş mantığı
│   ├── services/
│   │   ├── auth.service.js    # Auth business logic
│   │   └── user.service.js    # User business logic
│   ├── models/
│   │   └── user.model.js      # Veritabanı modeli
│   ├── validators/
│   │   ├── auth.validator.js  # Auth validation şemaları
│   │   └── user.validator.js  # User validation şemaları
│   ├── utils/
│   │   ├── AppError.js        # Custom error sınıfı
│   │   ├── asyncHandler.js    # Async wrapper
│   │   └── logger.js          # Logger konfigürasyonu
│   └── app.js                 # Express app oluşturma
├── tests/
│   ├── unit/
│   └── integration/
├── uploads/                   # Yüklenen dosyalar
├── logs/                      # Log dosyaları
├── .env                       # Environment variables (gitignore!)
├── .env.example               # Örnek env dosyası
├── .gitignore
├── package.json
└── server.js                  # Entry point (app.listen)
:::

:::code[javascript]{title="Layered Architecture Örneği"}
// ===== routes/user.routes.js =====
const router = require('express').Router();
const userController = require('../controllers/user.controller');
const { authenticate } = require('../middleware/auth');
const { validateBody } = require('../middleware/validate');
const { createUserSchema, updateUserSchema } = require('../validators/user.validator');

router.get('/', authenticate, userController.getAll);
router.get('/:id', authenticate, userController.getById);
router.post('/', validateBody(createUserSchema), userController.create);
router.put('/:id', authenticate, validateBody(updateUserSchema), userController.update);
router.delete('/:id', authenticate, userController.remove);

module.exports = router;

// ===== controllers/user.controller.js =====
const userService = require('../services/user.service');
const asyncHandler = require('../utils/asyncHandler');

// Controller: HTTP request/response ile ilgilenir
// Business logic'i service katmanına devreder
exports.getAll = asyncHandler(async (req, res) => {
  const { page, limit } = req.query;
  const users = await userService.findAll({ page, limit });
  res.json(users);
});

exports.getById = asyncHandler(async (req, res) => {
  const user = await userService.findById(req.params.id);
  res.json(user);
});

exports.create = asyncHandler(async (req, res) => {
  const user = await userService.create(req.body);
  res.status(201).json(user);
});

// ===== services/user.service.js =====
const User = require('../models/user.model');
const AppError = require('../utils/AppError');

// Service: Business logic burada
// Veritabanı erişimi ve iş kuralları
class UserService {
  async findAll({ page = 1, limit = 10 }) {
    const offset = (page - 1) * limit;
    return User.findAll({ offset, limit });
  }

  async findById(id) {
    const user = await User.findByPk(id);
    if (!user) throw new AppError('Kullanıcı bulunamadı', 404);
    return user;
  }

  async create(data) {
    const existing = await User.findOne({ where: { email: data.email } });
    if (existing) throw new AppError('Bu email zaten kayıtlı', 409);
    return User.create(data);
  }
}

module.exports = new UserService();

// ===== app.js =====
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const config = require('./config');
const { httpLogger } = require('./utils/logger');
const { errorHandler } = require('./middleware/errorHandler');
const routes = require('./routes');

const app = express();

// Global middleware'ler
app.use(helmet());
app.use(cors({ origin: config.cors.origins }));
app.use(express.json());
app.use(httpLogger);

// Route'lar
app.use('/api/v1', routes);

// Error handling (en sonda)
app.use(errorHandler);

module.exports = app;
:::

:::beginner-mistake
Yaygın hata: Tüm kodu tek bir dosyaya (app.js veya server.js) yazmak. Bu yaklaşım küçük projeler için çalışır ama büyüdükçe bakımı imkansız hale gelir. Her katmanın (route, controller, service, model) ayrı dosyalarda olması gerekir. Controller HTTP ile, service business logic ile, model veritabanı ile ilgilenir.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Layered Architecture Donusumu (Kolay)

Mevcut tek dosyali Express uygulamani Controller-Service-Repository katmanli mimariye donustur.

```
project/
├── src/
│   ├── routes/userRoutes.js        # Route tanimlari
│   ├── controllers/userController.js # HTTP req/res isleme
│   ├── services/userService.js     # Is mantigi
│   ├── repositories/userRepo.js    # Veri erisimi
│   ├── middlewares/validate.js     # Validation middleware
│   └── app.js                      # Express konfigurasyonu
├── .env
├── .env.example
└── package.json
```

```javascript
// TODO: services/userService.js — Is mantigi burada
class UserService {
  constructor(userRepo) {
    this.userRepo = userRepo;
  }

  async getAllUsers() { return this.userRepo.findAll(); }

  async createUser(data) {
    // TODO: Is kurallari: email benzersiz mi kontrol et
    const existing = await this.userRepo.findByEmail(data.email);
    if (existing) throw new Error("Email already exists");
    return this.userRepo.create(data);
  }
}

// TODO: controllers/userController.js — Ince katman
// req/res isler, service'i cagir, response dondur
```

**Beklenen Sonuc:** Her katman tek sorumluluga sahip olmali. Service katmani HTTP'den bagimsiz test edilebilmeli. Yeni bir endpoint eklemek icin sadece ilgili katmanlara kod eklenmeli.
**Ipucu:** Controller asla dogrudan veritabanina erismemeli — her zaman service üzerinden gitmeli.

---

### Alistirma 2: Zod ile Request Validation (Orta)

Zod kullanarak tip-guvenli request validation middleware'i oluştur.

```javascript
const { z } = require("zod");

// Schemas
const createUserSchema = z.object({
  body: z.object({
    name: z.string().min(2, "Ad en az 2 karakter").max(50),
    email: z.string().email("Gecerli email girin"),
    age: z.number().int().min(18).max(120).optional(),
  }),
});

const getUsersSchema = z.object({
  query: z.object({
    page: z.coerce.number().int().min(1).default(1),
    limit: z.coerce.number().int().min(1).max(100).default(20),
    search: z.string().optional(),
  }),
});

// TODO: Generic validation middleware
function validate(schema) {
  return (req, res, next) => {
    try {
      // TODO: schema.parse({ body: req.body, query: req.query, params: req.params })
      // TODO: Basarili ise parse edilmis degerleri req'e ata
      // TODO: Hatada ZodError'dan okunabilir mesaj olustur ve 400 dondur
    } catch (err) {
      // ...
    }
  };
}

// Kullanim:
app.post("/api/users", validate(createUserSchema), userController.create);
app.get("/api/users", validate(getUsersSchema), userController.getAll);
```

**Beklenen Sonuc:** Gecersiz body/query icin 400 + detayli hata mesaji donmeli. Gecerli veriler otomatik parse edilmeli (örneğin string "5" -> number 5 coerce ile). Schema'dan TypeScript tipleri turetilmeli.
**Ipucu:** `z.coerce.number()` string'i otomatik number'a cevirir. ZodError'un `errors` arrayi ile alan bazli hata mesajlari elde edilir.

---

### Alistirma 3: Rate Limiting ve CORS Konfigurasyonu (Zor)

Farkli endpoint'ler icin farkli rate limit'ler ayarla ve CORS'u guvenli sekilde konfigure et.

```javascript
const rateLimit = require("express-rate-limit");
const cors = require("cors");

// TODO: Genel rate limiter (tum endpoint'ler)
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 dakika
  max: 100,
  // TODO: standardHeaders ve legacyHeaders ayarla
  // TODO: Custom mesaj: { error: "Too many requests", retryAfter: ... }
});

// TODO: Login icin siki rate limiter
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 15 dakikada en fazla 5 deneme
  // TODO: skipSuccessfulRequests: true — basarili login'ler sayilmasin
});

// TODO: CORS konfigurasyonu
const corsOptions = {
  // TODO: Sadece belirli origin'lere izin ver
  origin: ["http://localhost:5173", "https://myapp.com"],
  // TODO: credentials, methods, allowedHeaders ayarla
  // TODO: Preflight cache suresi maxAge: 86400
};

app.use(generalLimiter);
app.use(cors(corsOptions));
app.post("/api/auth/login", loginLimiter, authController.login);

// Test:
// curl -v http://localhost:3000/api/users → CORS header'larini kontrol et
// 6 kez login denemesi yap → 429 Too Many Requests almalisin
```

**Beklenen Sonuc:** 100'den fazla istekte 429 donmeli. Login'de 5 basarisiz denemeden sonra kilitlenmeli. Izin verilmeyen origin'lerden gelen istekler CORS hatasi almali. Response header'larinda rate limit bilgileri gorunmeli.
**Ipucu:** `X-RateLimit-Limit`, `X-RateLimit-Remaining` ve `X-RateLimit-Reset` header'lari otomatik eklenir.
:::

:::knowledge-check
type: multiple_choice
question: "Layered architecture'da business logic (iş kuralları) hangi katmanda yazılır?"
options:
  - "Route katmanı"
  - "Controller katmanı"
  - "Service katmanı"
  - "Middleware katmanı"
correct: 2
explanation: "Service katmanı business logic'in yaşadığı yerdir. Controller HTTP request/response ile ilgilenir (ince katman), service ise iş kurallarını ve veritabanı operasyonlarını yönetir. Bu ayırım sayesinde service katmanı HTTP'den bağımsız olarak test edilebilir."
:::

:::knowledge-check
type: multiple_choice
question: "Zod ile validate edilmiş bir schema'dan TypeScript tipi elde etmek için hangi yöntem kullanılır?"
options:
  - "z.type(schema)"
  - "z.infer<typeof schema>"
  - "schema.toType()"
  - "z.extract(schema)"
correct: 1
explanation: "z.infer<typeof schema> kullanılarak bir Zod schema'sından TypeScript tipi çıkarılabilir. Bu, validation ve type safety'yi tek bir yerde tanımlamamızı sağlar - DRY (Don't Repeat Yourself) prensibiyle hem runtime validation hem compile-time type checking yapılır."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Layered Architecture'da Route, Controller, Service ve Model katmanlarinin sorumluluk sinirlarini acikla. Controller neden 'ince katman' olmali? Service katmaninda business logic nasil test edilebilir hale gelir? Dependency Injection bu katmanlar arasinda nasil uygulanir?"

**2. Pratik Uygulama:**
> "Zod ile bir kullanici kayit schema'si oluştur (isim, email, sifre, yas, rol). Bu schema'dan TypeScript tipi cikar (z.infer). validateBody middleware factory fonksiyonunu yaz ve Express route'larinda kullan. Multer ile profil resmi yukleme endpoint'i ekle (max 2MB, sadece JPEG/PNG, UUID ile dosya adi)."
> Takip: "Winston ile structured JSON logger kur, her HTTP istegini logla ve correlation ID ile request izleme ekle."

**3. Mukemmellik Icin:**
> "12-Factor App prensiplerini bir Express.js projesine nasil uygularim? Config management, logging, port binding, concurrency, dev/prod parity ve graceful shutdown konularini pratikte goster. Docker container icinde calisacak sekilde uyarla."

### Pair Programming Ipucu
Proje yapisini oluşturken AI'a mevcut kodunu goster ve sor: "Bu tek dosyadaki Express uygulamasini layered architecture'a donustur. Route, controller, service, model, middleware ve validator dosyalarini ayir. Her katmanin sorumlulugunu belirle."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Backend uygulamasinda hata yonetimini nasil yapilandirirsiniz?**
- **Junior cevabi:** try/catch ile hatalari yakalayip res.status(500) gonderirim.
- **Senior cevabi:** Katmanli hata yonetimi: 1) Custom error class'lari oluşturulur (AppError extends Error, statusCode ve isOperational flag'i ile), 2) Async handler wrapper ile her route'da try/catch tekrarindan kacinilir, 3) Global error handler middleware'i (4 param) tum hatalari yakalar, 4) Operational error'lar (validation, not found) istemciye anlamli mesaj doner, programming error'lar (TypeError, null reference) generic mesaj doner ve loglanir, 5) Unhandled rejection ve uncaught exception handler'lari process seviyesinde yakalanir. Production'da error tracking (Sentry) ve structured logging (Pino) kullanilir.

**Soru 2: Bir Express uygulamasini nasil yapilandirirsiniz (proje yapisi)?**
- **Junior cevabi:** Routes, controllers ve models klasorleri oluştururum.
- **Senior cevabi:** Layered architecture: routes (HTTP endpoint tanimlari), controllers (request/response handling), services (is mantigi), repositories (data access), middleware (cross-cutting concerns), validators (input validation). Her katman sadece altindaki katmani cagirir. Dependency injection ile test edilebilirlik saglanir. Config management: environment-based (.env, config/), secrets icin vault. Modular yaklasim: feature-based klasor yapisi (users/, products/) buyuk projelerde tercih edilir. index.ts barrel export ile temiz import'lar saglanir.
:::

:::exercise
### Alıştırma 4: Zod ile Request Validation
**Görev:** Zod kullanarak bir kullanıcı kayıt endpoint'i için request body validasyonu yaz.
**Başlangıç kodu:**
```typescript
import { z } from "zod";
import { Request, Response, NextFunction } from "express";

// TODO: Zod schema tanımla
const registerSchema = z.object({
  // username: 3-20 karakter, sadece harf/rakam/alt çizgi
  // email: geçerli email formatı
  // password: min 8, en az 1 büyük harf, 1 rakam, 1 özel karakter
  // age: opsiyonel, 18-120 arası
  // role: "user" veya "admin" (varsayılan "user")
});

// TODO: Zod schema'dan TypeScript tipi çıkar
type RegisterInput = ???;

// TODO: Validation middleware yaz
function validate(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    // schema.safeParse ile doğrula
    // Hata varsa 400 döndür (detaylı hata mesajları ile)
    // Başarılıysa req.body'yi parse edilmiş veri ile değiştir
  };
}

app.post("/api/register", validate(registerSchema), (req, res) => {
  // req.body artık tip güvenli
});
```
**Beklenen çıktı:**
```typescript
const registerSchema = z.object({
  username: z.string()
    .min(3, "Kullanıcı adı en az 3 karakter")
    .max(20, "Kullanıcı adı en fazla 20 karakter")
    .regex(/^[a-zA-Z0-9_]+$/, "Sadece harf, rakam ve alt çizgi"),
  email: z.string().email("Geçerli bir email girin"),
  password: z.string()
    .min(8, "Şifre en az 8 karakter")
    .regex(/[A-Z]/, "En az 1 büyük harf")
    .regex(/[0-9]/, "En az 1 rakam")
    .regex(/[!@#$%^&*]/, "En az 1 özel karakter"),
  age: z.number().int().min(18).max(120).optional(),
  role: z.enum(["user", "admin"]).default("user"),
});

type RegisterInput = z.infer<typeof registerSchema>;

function validate(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        error: "Validation hatası",
        details: result.error.flatten().fieldErrors,
      });
    }
    req.body = result.data;
    next();
  };
}
```
**İpucu:** `z.infer<typeof schema>` ile Zod schema'dan TypeScript tipi otomatik çıkarılır. `safeParse` exception fırlatmaz, result döndürür.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 5: Multer ile Güvenli Dosya Yükleme
**Görev:** Multer kullanarak profil resmi yükleme endpoint'i yaz. Güvenlik kontrollerini uygula.
**Başlangıç kodu:**
```javascript
const multer = require("multer");
const path = require("path");
const crypto = require("crypto");

// TODO: Storage konfigürasyonu
// - Dosyaları uploads/ klasörüne kaydet
// - Orijinal dosya adını KULLANMA (UUID ile yeniden adlandır)
// - Dosya uzantısını koru

// TODO: File filter
// - Sadece resim dosyalarına izin ver (jpeg, png, gif, webp)
// - MIME type VE uzantı kontrolü yap (ikisi de eşleşmeli)

// TODO: Limits
// - Maksimum 5MB dosya boyutu
// - Tek seferde 1 dosya

// TODO: Upload endpoint
// POST /api/profile/avatar
```
**Beklenen çıktı:**
```javascript
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, "uploads/"),
  filename: (req, file, cb) => {
    const uniqueName = crypto.randomUUID() + path.extname(file.originalname);
    cb(null, uniqueName);
  },
});

const allowedMimeTypes = ["image/jpeg", "image/png", "image/gif", "image/webp"];
const allowedExtensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"];

const fileFilter = (req, file, cb) => {
  const ext = path.extname(file.originalname).toLowerCase();
  if (allowedMimeTypes.includes(file.mimetype) && allowedExtensions.includes(ext)) {
    cb(null, true);
  } else {
    cb(new Error("Sadece resim dosyaları kabul edilir"), false);
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: { fileSize: 5 * 1024 * 1024, files: 1 },
});

app.post("/api/profile/avatar", upload.single("avatar"), (req, res) => {
  if (!req.file) return res.status(400).json({ error: "Dosya yüklenmedi" });
  res.json({ url: `/uploads/${req.file.filename}` });
});
```
**İpucu:** Orijinal dosya adını ASLA kullanma - path traversal saldırısı riski var. UUID ile yeniden adlandır. Hem MIME type hem uzantı kontrol et.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: Winston ile Structured Logging
**Görev:** Winston logger konfigürasyonu yaz: development'ta renkli console, production'da JSON dosya.
**Başlangıç kodu:**
```javascript
const winston = require("winston");

// TODO: Logger konfigürasyonu oluştur
// Development: renkli, okunabilir console çıktısı
// Production: JSON formatında dosyaya yaz
//   - error.log: sadece error seviyesi
//   - combined.log: tüm seviyeler
// Her log'da: timestamp, seviye, mesaj, metadata

// TODO: Request logging middleware yaz
// Her istek için: method, url, status, response time
```
**Beklenen çıktı:**
```javascript
const logger = winston.createLogger({
  level: process.env.NODE_ENV === "production" ? "info" : "debug",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: "logs/error.log", level: "error" }),
    new winston.transports.File({ filename: "logs/combined.log" }),
  ],
});

if (process.env.NODE_ENV !== "production") {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    ),
  }));
}

// Request logging middleware
function requestLogger(req, res, next) {
  const start = Date.now();
  res.on("finish", () => {
    logger.info("HTTP Request", {
      method: req.method,
      url: req.originalUrl,
      status: res.statusCode,
      duration: `${Date.now() - start}ms`,
      ip: req.ip,
    });
  });
  next();
}
```
**İpucu:** `res.on("finish")` response tamamlandığında çalışır - bu sayede status code ve duration bilgisine erişirsin. Production'da asla console.log kullanma, her zaman logger kullan.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: Environment Variables Yönetimi
**Görev:** Environment variables'ı güvenli yöneten bir config modülü yaz. Zorunlu değişkenler eksikse uygulama başlamasın.
**Başlangıç kodu:**
```typescript
// TODO: config.ts modülü yaz
// - .env dosyasından değişkenleri oku
// - Zorunlu değişkenler eksikse hata fırlat
// - Tip güvenli erişim sağla
// - Varsayılan değerler belirle
```
**Beklenen çıktı:**
```typescript
import dotenv from "dotenv";
dotenv.config();

function getEnv(key: string, defaultValue?: string): string {
  const value = process.env[key] || defaultValue;
  if (value === undefined) {
    throw new Error(`Zorunlu environment variable eksik: ${key}`);
  }
  return value;
}

function getEnvNumber(key: string, defaultValue?: number): number {
  const value = process.env[key];
  if (value === undefined && defaultValue !== undefined) return defaultValue;
  const num = Number(value);
  if (isNaN(num)) throw new Error(`${key} geçerli bir sayı değil`);
  return num;
}

export const config = {
  port: getEnvNumber("PORT", 3000),
  nodeEnv: getEnv("NODE_ENV", "development"),
  db: {
    host: getEnv("DB_HOST"),
    port: getEnvNumber("DB_PORT", 5432),
    name: getEnv("DB_NAME"),
    user: getEnv("DB_USER"),
    password: getEnv("DB_PASSWORD"),
  },
  jwt: {
    secret: getEnv("JWT_SECRET"),
    expiresIn: getEnv("JWT_EXPIRES_IN", "15m"),
  },
} as const;
```
**İpucu:** Uygulama başlangıcında tüm zorunlu değişkenleri kontrol et. Runtime'da eksik değişken bulmak yerine başlangıçta hata ver. `.env` dosyasını ASLA git'e commit etme.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 8: Custom Error Class'ları
**Görev:** Katmanlı hata yönetimi için custom error class'ları ve global error handler yaz.
**Başlangıç kodu:**
```typescript
// TODO: AppError base class
// TODO: NotFoundError, ValidationError, UnauthorizedError alt class'ları
// TODO: Global error handler middleware
// - Operational error'lar: kullanıcıya anlamlı mesaj
// - Programming error'lar: generic mesaj + loglama
```
**Beklenen çıktı:**
```typescript
class AppError extends Error {
  public readonly statusCode: number;
  public readonly isOperational: boolean;

  constructor(message: string, statusCode: number, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} bulunamadı`, 404);
  }
}

class ValidationError extends AppError {
  constructor(message: string, public details?: Record<string, string[]>) {
    super(message, 400);
  }
}

class UnauthorizedError extends AppError {
  constructor(message = "Yetkilendirme gerekli") {
    super(message, 401);
  }
}

// Global Error Handler
function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { message: err.message, ...(err instanceof ValidationError && { details: err.details }) },
    });
  }
  // Programming error
  console.error("Unexpected error:", err);
  res.status(500).json({ error: { message: "Sunucu hatası" } });
}
```
**İpucu:** `isOperational` flag'i ile beklenen hatalar (validation, not found) ve beklenmeyen hatalar (null pointer, type error) ayrımı yap. Production'da sadece operational error detayı göster.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: CORS Konfigürasyonu
**Görev:** Farklı ortamlar için (development, staging, production) CORS ayarlarını yapılandır.
**Başlangıç kodu:**
```javascript
const cors = require("cors");

// TODO: Ortama göre CORS ayarla
// Development: tüm origin'lere izin ver
// Production: sadece belirli domain'lere izin ver
// Credentials (cookie) desteği
// İzin verilen HTTP metodları ve header'lar
```
**Beklenen çıktı:**
```javascript
const allowedOrigins = {
  development: ["http://localhost:3000", "http://localhost:5173"],
  production: ["https://myapp.com", "https://admin.myapp.com"],
};

const corsOptions = {
  origin: (origin, callback) => {
    const env = process.env.NODE_ENV || "development";
    const origins = allowedOrigins[env] || allowedOrigins.development;

    // origin undefined olabilir (Postman, server-to-server)
    if (!origin || origins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error(`CORS: ${origin} izin verilmedi`));
    }
  },
  credentials: true,
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"],
  maxAge: 86400, // Preflight cache: 24 saat
};

app.use(cors(corsOptions));
```
**İpucu:** `credentials: true` ise `origin: "*"` KULLANILMAZ - spesifik origin belirtmek zorunlu. `maxAge` ile preflight (OPTIONS) isteklerini cache'le.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 10: Production-Ready Proje Yapısı
**Görev:** Express projesini katmanlı mimariye (layered architecture) göre organize et.
**Başlangıç kodu:**
```
TODO: Aşağıdaki monolitik kodu katmanlı yapıya dönüştür

// YANLIŞ: Her şey tek dosyada
app.post("/api/users", async (req, res) => {
  const { name, email, password } = req.body;
  if (!name || !email) return res.status(400).json({error: "..."});
  const hashedPassword = await bcrypt.hash(password, 12);
  const user = await db.query("INSERT INTO users ...", [name, email, hashedPassword]);
  const token = jwt.sign({ id: user.id }, SECRET);
  res.status(201).json({ user, token });
});

TODO: Şu katmanlara ayır:
- Route → Controller → Service → Repository
```
**Beklenen çıktı:**
```
Dosya yapısı:
src/
  routes/userRoutes.ts       → HTTP endpoint tanımları
  controllers/userController.ts → Request/Response handling
  services/userService.ts    → İş mantığı
  repositories/userRepo.ts   → Veritabanı işlemleri
  middleware/validate.ts     → Validation
  validators/userValidator.ts → Zod schema'lar

// routes/userRoutes.ts
router.post("/", validate(registerSchema), userController.register);

// controllers/userController.ts
async register(req, res) {
  const user = await userService.register(req.body);
  res.status(201).json(user);
}

// services/userService.ts
async register(data) {
  const hashedPassword = await bcrypt.hash(data.password, 12);
  const user = await userRepo.create({ ...data, password: hashedPassword });
  const token = jwt.sign({ id: user.id }, config.jwt.secret);
  return { user, token };
}

// repositories/userRepo.ts
async create(data) {
  return db.query("INSERT INTO users ...", [data.name, data.email, data.password]);
}
```
**İpucu:** Her katman sadece altındaki katmanı çağırır. Controller asla doğrudan DB'ye erişmez. Service katmanı iş kurallarını içerir. Bu yapı test edilebilirliği ve bakımı kolaylaştırır.
**Zorluk:** Zor
:::

:::must-note
- express-validator = middleware-based, chain API; Zod = schema-based, TypeScript-friendly
- Zod'da `z.infer<typeof schema>` ile TypeScript tipi çıkarılır (DRY prensibi)
- Multer: dosya yükleme için kullan, orijinal dosya adını ASLA kullanma (UUID ile yeniden adlandır)
- Multer konfigürasyonu: storage (nereye kaydet), fileFilter (hangi türler), limits (boyut/sayı sınırı)
- Rate limiting: genel API = 100 istek/15dk, auth endpoint = 5 istek/15dk (brute-force koruması)
- CORS: development'ta `cors()`, production'da whitelist yaklaşımı kullan
- Winston = esnek, çok transport; Pino = ~5x daha hızlı, JSON-first
- Log seviyeleri: error > warn > info > http > verbose > debug > silly
- .env dosyasını git'e EKLEME, .env.example dosyasını git'e EKLE
- Zorunlu environment variable'ları uygulama başlangıcında kontrol et
- Layered Architecture: Route → Controller → Service → Model
- Controller ince katman (HTTP ile ilgilenir), Service kalın katman (business logic)
- app.js = Express konfigürasyonu, server.js = app.listen (entry point)
- tests/ klasörü: unit/ ve integration/ olarak ayır
:::

:::senior-learns
Bir Senior Developer veya CTO, Express ileri konularını öğrenirken şu yaklaşımı benimser:

1. **Validation katmanını schema-driven yapar** - Runtime validation ve TypeScript tiplerini tek bir schema'dan üretir (Zod veya io-ts). API contract'ları OpenAPI spec ile dokümante eder ve contract-first development yapar. Schema'lar shared package olarak frontend ve backend arasında paylaşılır.
2. **Structured logging ve observability kurar** - JSON formatında structured log üretir. Correlation ID ile request zincirini izler (distributed tracing). Log aggregation (ELK Stack, Datadog) ve alerting sistemi kurar. Log seviyelerini environment'a göre dinamik ayarlar.
3. **Security katmanını defense-in-depth yaklaşımıyla tasarlar** - Rate limiting, input validation, output encoding, CORS, helmet, CSRF protection katmanlarını birlikte uygular. Dependency audit (pnpm audit) ve SAST/DAST araçlarını CI/CD pipeline'a entegre eder.
4. **12-Factor App prensiplerini uygular** - Config'i environment variable'lardan alır, bağımlılıkları açıkça deklare eder, port binding ile servis yapar, concurrency'yi process model ile yönetir. Dev/prod parity'yi container'lar ile sağlar.
5. **Clean Architecture veya Hexagonal Architecture uygular** - Domain logic'i framework'ten bağımsız tutar. Dependency inversion ile dış bağımlılıkları (veritabanı, API) soyutlar. Her katmanın test edilebilirliğini garanti eder.
6. **Graceful degradation ve circuit breaker pattern uygular** - Harici servislerin arızalanmasına karşı fallback mekanizmaları kurar. Circuit breaker ile cascading failure'ları önler. Health check endpoint'leri ile servis sağlığını monitor eder.

**Profesyonel Mindset:** "İyi bir backend mimarisi, değişiklik maliyetini minimize eder. Bugün yazdığın controller'ı yarın değiştirebilmelisin ama service katmanına dokunmamalısın. Bugünkü veritabanını yarın değiştirebilmelisin ama business logic'e dokunmamalısın. Katmanlar arası bağımlılıkları tek yönlü tut: Route → Controller → Service → Repository. Asla tersine bağımlılık oluşturma."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Validation** (væl-ɪ-deɪ-ʃən) → Doğrulama
   *"Input validation ensures that user-submitted data meets the expected format and constraints."*

2. **Rate Limiting** (reɪt lɪm-ɪ-tɪŋ) → İstek hız sınırlama
   *"Rate limiting prevents abuse by restricting the number of requests a client can make."*

3. **Logging** (lɒɡ-ɪŋ) → Kayıt tutma / Loglama
   *"Structured logging with correlation IDs enables effective debugging in distributed systems."*

4. **Layered Architecture** (leɪ-ərd ɑːr-kɪ-tek-tʃər) → Katmanlı mimari
   *"The layered architecture separates concerns into routes, controllers, services, and models."*

5. **Environment Variable** (ɪn-vaɪ-rən-mənt vɛr-i-ə-bəl) → Ortam değişkeni
   *"Never hardcode secrets; use environment variables for sensitive configuration."*

**Okuma Egzersizi:** Express.js resmi rehberinde "Error Handling" sayfasını oku: https://expressjs.com/en/guide/error-handling.html

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Input validation ve rate limiting eklendi"
→ Örnek: `feat: add input validation with Zod and rate limiting middleware`
:::

:::external-resource
- 📖 **Zod Docs:** zod.dev (resmi dokümantasyon, ücretsiz)
- 📖 **express-validator:** express-validator.github.io (ücretsiz)
- 📖 **Winston Docs:** github.com/winstonjs/winston (ücretsiz)
- 📺 **Traversy Media:** "Express.js Crash Course" (YouTube, ücretsiz)
- 📖 **12-Factor App:** 12factor.net (metodoloji rehberi, ücretsiz)
:::
