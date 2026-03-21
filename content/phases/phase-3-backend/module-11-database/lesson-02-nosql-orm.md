---
title: "NoSQL Veritabanları ve ORM: MongoDB, Redis ve Modern Araçlar"
id: "mod-11-db/lesson-02"
estimated_minutes: 55
order: 2
tags: ["nosql", "mongodb", "redis", "orm", "prisma", "mongoose", "cap-theorem"]
prerequisites: ["mod-11-db/lesson-01"]
---

# NoSQL Veritabanları ve ORM: MongoDB, Redis ve Modern Araçlar

:::realworld
Instagram bir fotoğraf paylaştığında, beğeni sayısı Redis'te cache'lenir, kullanıcı profili MongoDB-benzeri document store'da saklanır, arkadaşlık ilişkileri graph database'de tutulur. Modern uygulamalar tek bir veritabanı ile sınırlı kalmaz. Bu derste NoSQL dünyasını derinlemesine öğrenecek, hangi veri için hangi veritabanını seçeceğini bilecek ve ORM araçlarıyla production-ready kod yazabileceksin.
:::

## Neden NoSQL Öğreniyorsun?

İlişkisel veritabanları her sorun için ideal değildir. Milyonlarca kullanıcıya hizmet veren uygulamalarda:

- Esnek şemaya ihtiyaç duyarsın (kullanıcı profilleri farklı alanlar içerebilir)
- Yatay ölçekleme gerekir (tek sunucu yetmez)
- Milisaniye seviyesinde cache gerekir
- Gerçek zamanlı veri akışı lazımdır

:::deha-tip
Deha seviyesi geliştiriciler "SQL mi NoSQL mi?" sorusuna "ikisi de" cevabını verir. Polyglot persistence yaklaşımıyla her veri tipi için en uygun veritabanını seçer. Kullanıcı bilgileri PostgreSQL'de, oturum verileri Redis'te, ürün katalogları MongoDB'de saklanır.
:::

## MongoDB: Document Database

:::concept[MongoDB (İng: MongoDB)]
MongoDB, JSON benzeri belgeler (documents) içinde veri saklayan, schema-flexible NoSQL veritabanıdır.

**Türkçe karşılığı:** Belge Tabanlı Veritabanı
**Ne işe yarar:** Yapısı değişken verileri esnek belgeler halinde saklar
**Gerçek hayat benzetmesi:** Dosya dolabında her klasörün farklı sayfa formatına sahip olabilmesi gibi - bazılarında 3 alan, bazılarında 10 alan olabilir
:::

### MongoDB CRUD İşlemleri

:::code[javascript]{title="MongoDB CRUD Temel İşlemler"}
// Bağlantı (Mongoose ile)
const mongoose = require('mongoose');
await mongoose.connect('mongodb://localhost:27017/myapp');

// Schema tanımla
const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  age: Number,
  hobbies: [String],
  address: {
    city: String,
    district: String,
    zipCode: String
  },
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// CREATE - Belge ekleme
const user = await User.create({
  name: 'Ahmet Yilmaz',
  email: 'ahmet@example.com',
  age: 28,
  hobbies: ['coding', 'gaming'],
  address: { city: 'Istanbul', district: 'Kadikoy' }
});

// READ - Belge sorgulama
const allUsers = await User.find();                           // Tümü
const activeUsers = await User.find({ age: { $gte: 18 } });  // age >= 18
const oneUser = await User.findById('64a1b2c3d4e5f6a7b8c9d0');
const byEmail = await User.findOne({ email: 'ahmet@example.com' });

// Projection (sadece istenen alanlar)
const names = await User.find({}, { name: 1, email: 1, _id: 0 });

// Sıralama, limit, skip
const paginated = await User.find()
  .sort({ createdAt: -1 })
  .skip(20)
  .limit(10);

// UPDATE - Belge güncelleme
await User.updateOne(
  { email: 'ahmet@example.com' },
  { $set: { age: 29 }, $push: { hobbies: 'reading' } }
);

// findOneAndUpdate: Güncellenmiş belgeyi döndür
const updated = await User.findOneAndUpdate(
  { email: 'ahmet@example.com' },
  { $inc: { age: 1 } },
  { new: true }  // Güncellenmiş halini döndür
);

// DELETE - Belge silme
await User.deleteOne({ email: 'ahmet@example.com' });
await User.deleteMany({ age: { $lt: 18 } });
:::

### MongoDB Query Operators

:::code[javascript]{title="MongoDB Query Operators"}
// Karşılaştırma operatörleri
await User.find({ age: { $gt: 25 } });     // greater than
await User.find({ age: { $gte: 25 } });    // greater than or equal
await User.find({ age: { $lt: 30 } });     // less than
await User.find({ age: { $lte: 30 } });    // less than or equal
await User.find({ age: { $ne: 25 } });     // not equal
await User.find({ age: { $in: [25, 30] } }); // in array

// Mantıksal operatörler
await User.find({
  $and: [{ age: { $gte: 18 } }, { city: 'Istanbul' }]
});

await User.find({
  $or: [{ city: 'Istanbul' }, { city: 'Ankara' }]
});

// Array operatörleri
await User.find({ hobbies: { $all: ['coding', 'gaming'] } }); // Hepsini içeren
await User.find({ hobbies: { $size: 3 } });                    // 3 elemanlı

// Nested object sorgulama
await User.find({ 'address.city': 'Istanbul' });

// Regex ile arama
await User.find({ name: { $regex: /^Ahmet/i } });
:::

### Aggregation Pipeline

:::code[javascript]{title="MongoDB Aggregation Pipeline"}
// Aggregation Pipeline: Verileri aşamalar halinde işle
const result = await Order.aggregate([
  // Stage 1: Filtrele
  { $match: { status: 'completed', createdAt: { $gte: new Date('2024-01-01') } } },

  // Stage 2: İlişkili tabloyu birleştir (SQL JOIN gibi)
  { $lookup: {
      from: 'users',
      localField: 'userId',
      foreignField: '_id',
      as: 'user'
  }},

  // Stage 3: Array'i düzleştir
  { $unwind: '$user' },

  // Stage 4: Grupla ve hesapla
  { $group: {
      _id: '$user.city',
      totalRevenue: { $sum: '$amount' },
      orderCount: { $sum: 1 },
      avgOrderValue: { $avg: '$amount' }
  }},

  // Stage 5: Sırala
  { $sort: { totalRevenue: -1 } },

  // Stage 6: Limit
  { $limit: 10 },

  // Stage 7: Çıktıyı biçimlendir
  { $project: {
      city: '$_id',
      totalRevenue: { $round: ['$totalRevenue', 2] },
      orderCount: 1,
      avgOrderValue: { $round: ['$avgOrderValue', 2] },
      _id: 0
  }}
]);
:::

:::beginner-mistake
Yaygın hata: MongoDB'de JOIN yapılamaz sanmak. $lookup ile JOIN yapılabilir ancak performansı SQL JOIN'lerinden daha düşüktür. Eğer sık sık JOIN yapıyorsan, büyük ihtimalle MongoDB yerine PostgreSQL kullanmalısın.
:::

### Mongoose Schema ve Middleware

:::code[javascript]{title="Mongoose İleri Seviye Özellikler"}
const productSchema = new mongoose.Schema({
  name: { type: String, required: [true, 'Ürün adı zorunludur'], trim: true },
  price: { type: Number, min: [0, 'Fiyat negatif olamaz'] },
  category: { type: String, enum: ['electronics', 'clothing', 'books'] },
  slug: String,
  reviews: [{
    user: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    rating: { type: Number, min: 1, max: 5 },
    comment: String
  }]
}, { timestamps: true }); // createdAt ve updatedAt otomatik

// Virtual field (DB'de saklanmaz)
productSchema.virtual('priceWithTax').get(function() {
  return this.price * 1.18; // %18 KDV
});

// Pre-save middleware
productSchema.pre('save', function(next) {
  this.slug = this.name.toLowerCase().replace(/ /g, '-');
  next();
});

// Index tanımla
productSchema.index({ name: 'text', category: 1 });
productSchema.index({ price: 1, category: 1 });

// Populate: İlişkili veriyi getir (SQL JOIN benzeri)
const product = await Product.findById(id)
  .populate('reviews.user', 'name email');
:::

## Redis: In-Memory Data Store

:::concept[Redis (İng: Redis - Remote Dictionary Server)]
Redis, bellekte (RAM) çalışan, anahtar-değer (key-value) tabanlı veri yapısı deposudur. Milisaniyenin altında okuma/yazma performansı sağlar.

**Türkçe karşılığı:** Bellek İçi Veri Deposu
**Ne işe yarar:** Caching, session yönetimi, gerçek zamanlı özellikler, rate limiting
**Gerçek hayat benzetmesi:** Masanın üzerindeki not kağıtları gibi - hızlı erişim ama sınırlı alan. Dolap (disk) daha fazla tutar ama daha yavaş.
:::

### Redis Veri Yapıları ve Kullanım Alanları

:::code[javascript]{title="Redis Temel Kullanım (Node.js - ioredis)"}
const Redis = require('ioredis');
const redis = new Redis(); // localhost:6379

// STRING - En basit yapı
await redis.set('user:1:name', 'Ahmet');
await redis.get('user:1:name'); // 'Ahmet'
await redis.set('session:abc123', JSON.stringify(userData), 'EX', 3600); // 1 saat TTL
await redis.incr('page:views');  // Atomik sayaç

// HASH - Object benzeri (user profili için ideal)
await redis.hset('user:1', { name: 'Ahmet', email: 'ahmet@ex.com', age: '28' });
await redis.hget('user:1', 'name');      // 'Ahmet'
await redis.hgetall('user:1');           // { name, email, age }
await redis.hincrby('user:1', 'age', 1); // age = 29

// LIST - Sıralı liste (son aktiviteler, kuyruk)
await redis.lpush('notifications:1', JSON.stringify(notification));
await redis.lrange('notifications:1', 0, 9);  // Son 10 bildirim
await redis.ltrim('notifications:1', 0, 99);  // Sadece son 100 tut

// SET - Benzersiz eleman kümesi (etiketler, online kullanıcılar)
await redis.sadd('online:users', 'user:1', 'user:2', 'user:3');
await redis.sismember('online:users', 'user:1'); // true
await redis.scard('online:users');                // 3
await redis.smembers('online:users');            // ['user:1', 'user:2', 'user:3']

// SORTED SET - Sıralı küme (leaderboard, trending)
await redis.zadd('leaderboard', 1500, 'player:1', 2000, 'player:2');
await redis.zrevrange('leaderboard', 0, 9, 'WITHSCORES'); // Top 10
await redis.zincrby('leaderboard', 50, 'player:1');        // Skor artır
:::

### Redis Caching Patterns

:::code[javascript]{title="Cache-Aside (Lazy Loading) Pattern"}
async function getUser(userId) {
  const cacheKey = `user:${userId}`;

  // 1. Önce cache'e bak
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached); // Cache HIT
  }

  // 2. Cache'de yoksa veritabanından al
  const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

  // 3. Cache'e yaz (TTL ile)
  await redis.set(cacheKey, JSON.stringify(user), 'EX', 3600); // 1 saat

  return user; // Cache MISS
}

// Cache invalidation: Veri değiştiğinde cache'i temizle
async function updateUser(userId, data) {
  await db.query('UPDATE users SET ... WHERE id = $1', [userId]);
  await redis.del(`user:${userId}`); // Cache'i sil
}
:::

:::code[javascript]{title="Write-Through Pattern"}
async function updateProduct(productId, data) {
  // 1. Veritabanını güncelle
  const product = await db.query(
    'UPDATE products SET ... WHERE id = $1 RETURNING *',
    [productId]
  );

  // 2. Cache'i de güncelle (silme yerine)
  await redis.set(
    `product:${productId}`,
    JSON.stringify(product),
    'EX', 3600
  );

  return product;
}
:::

### Redis Session Storage

:::code[javascript]{title="Express.js ile Redis Session"}
const session = require('express-session');
const RedisStore = require('connect-redis').default;

app.use(session({
  store: new RedisStore({ client: redis }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,      // HTTPS only
    httpOnly: true,     // JS erişemez
    maxAge: 86400000,   // 24 saat
    sameSite: 'strict'
  }
}));
:::

### Redis Pub/Sub ve Rate Limiting

:::code[javascript]{title="Redis Pub/Sub (Gerçek Zamanlı Mesajlaşma)"}
// Publisher (mesaj gönderen)
await redis.publish('chat:room:1', JSON.stringify({
  user: 'Ahmet',
  message: 'Merhaba!',
  timestamp: Date.now()
}));

// Subscriber (mesaj dinleyen)
const subscriber = new Redis();
subscriber.subscribe('chat:room:1');
subscriber.on('message', (channel, message) => {
  const data = JSON.parse(message);
  console.log(`[${channel}] ${data.user}: ${data.message}`);
});
:::

:::code[javascript]{title="Redis Rate Limiting (Sliding Window)"}
async function rateLimiter(userId, limit = 100, windowSec = 60) {
  const key = `rate:${userId}`;
  const now = Date.now();
  const windowStart = now - windowSec * 1000;

  // Pipeline ile atomik işlem
  const pipeline = redis.pipeline();
  pipeline.zremrangebyscore(key, 0, windowStart);  // Eski kayıtları sil
  pipeline.zadd(key, now, `${now}`);                // Yeni isteği ekle
  pipeline.zcard(key);                               // Toplam istek sayısı
  pipeline.expire(key, windowSec);                   // TTL ayarla

  const results = await pipeline.exec();
  const requestCount = results[2][1];

  return {
    allowed: requestCount <= limit,
    remaining: Math.max(0, limit - requestCount),
    resetAt: new Date(now + windowSec * 1000)
  };
}
:::

:::tip
Redis verisi RAM'de yaşar. Sunucu kapanınca veri kaybolabilir. Kalıcı veri için RDB (snapshot) veya AOF (append-only file) persistence ayarlarını etkinleştir. Kritik veriyi asla yalnızca Redis'te tutma.
:::

## ORMs: Prisma vs Drizzle vs Sequelize

:::concept[ORM (Object-Relational Mapping)]
ORM, veritabanı tablolarını programlama dilindeki nesnelere (object) eşleyen araçtır. SQL yazmadan veritabanı işlemleri yapmanı sağlar.

**Türkçe karşılığı:** Nesne-İlişkisel Eşleme
**Ne işe yarar:** Veritabanı işlemlerini programlama dili ile yapmayı sağlar
**Gerçek hayat benzetmesi:** Tercüman gibi - sen Türkçe konuşursun, o SQL'e çevirir
:::

:::comparison
| Özellik | Prisma | Drizzle | Sequelize |
|---------|--------|---------|-----------|
| Tip güvenliği | Otomatik, mükemmel | TypeScript-first | Sınırlı |
| Öğrenme eğrisi | Orta | Düşük (SQL benzeri) | Orta-yüksek |
| Schema tanımı | Prisma Schema (DSL) | TypeScript | JavaScript/TS |
| Migration | Otomatik (prisma migrate) | Kit ile | CLI ile |
| Raw SQL | Destekler | Doğal destek | Destekler |
| Performans | İyi | Çok iyi (hafif) | Orta |
| **Ne zaman kullan** | Yeni projeler, hızlı geliştirme | Performans kritik, SQL seven | Legacy projeler |
| Ekosistem | Prisma Studio, Accelerate | Drizzle Studio, Kit | Geniş community |

**Tavsiye:** Yeni projeler için Prisma veya Drizzle kullan. Prisma developer experience'ta, Drizzle performansta öne çıkar.
:::

### Prisma Kullanımı

:::code[prisma]{title="Prisma Schema (schema.prisma)"}
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int       @id @default(autoincrement())
  email     String    @unique
  name      String
  role      Role      @default(USER)
  posts     Post[]
  profile   Profile?
  orders    Order[]
  createdAt DateTime  @default(now())
  updatedAt DateTime  @updatedAt

  @@index([email])
  @@map("users")
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  tags      Tag[]
  createdAt DateTime @default(now())

  @@index([authorId])
  @@map("posts")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
:::

:::code[typescript]{title="Prisma Client Kullanımı"}
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

// CREATE
const user = await prisma.user.create({
  data: {
    name: 'Ahmet',
    email: 'ahmet@example.com',
    profile: { create: { bio: 'Full-stack developer' } }
  },
  include: { profile: true }
});

// READ (type-safe sorgular)
const users = await prisma.user.findMany({
  where: {
    role: 'ADMIN',
    createdAt: { gte: new Date('2024-01-01') }
  },
  include: { posts: { where: { published: true } } },
  orderBy: { createdAt: 'desc' },
  take: 10,
  skip: 0
});

// UPDATE
const updated = await prisma.user.update({
  where: { email: 'ahmet@example.com' },
  data: { name: 'Ahmet Yilmaz' }
});

// DELETE
await prisma.user.delete({ where: { id: 1 } });

// Transaction
const [order, payment] = await prisma.$transaction([
  prisma.order.create({ data: { userId: 1, total: 150 } }),
  prisma.payment.create({ data: { userId: 1, amount: 150 } })
]);

// Raw SQL (gerektiğinde)
const result = await prisma.$queryRaw`
  SELECT u.name, COUNT(o.id) as order_count
  FROM users u
  LEFT JOIN orders o ON u.id = o.user_id
  GROUP BY u.name
  HAVING COUNT(o.id) > 5
`;
:::

### Drizzle ORM Kullanımı

:::code[typescript]{title="Drizzle ORM (SQL-Benzeri API)"}
import { pgTable, serial, varchar, integer, timestamp } from 'drizzle-orm/pg-core';
import { drizzle } from 'drizzle-orm/node-postgres';
import { eq, gt, desc, sql } from 'drizzle-orm';

// Schema tanımı (TypeScript)
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 255 }).notNull(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  age: integer('age'),
  createdAt: timestamp('created_at').defaultNow()
});

export const orders = pgTable('orders', {
  id: serial('id').primaryKey(),
  userId: integer('user_id').references(() => users.id),
  total: integer('total').notNull(),
  createdAt: timestamp('created_at').defaultNow()
});

const db = drizzle(pool);

// SELECT (SQL'e çok benzer)
const result = await db.select().from(users).where(eq(users.email, 'ahmet@ex.com'));

// JOIN
const usersWithOrders = await db
  .select({
    name: users.name,
    orderTotal: orders.total
  })
  .from(users)
  .leftJoin(orders, eq(users.id, orders.userId))
  .where(gt(orders.total, 100))
  .orderBy(desc(orders.total));

// INSERT
await db.insert(users).values({ name: 'Ahmet', email: 'ahmet@ex.com' });

// UPDATE
await db.update(users).set({ name: 'Ahmet Y.' }).where(eq(users.id, 1));

// DELETE
await db.delete(users).where(eq(users.id, 1));
:::

## N+1 Query Problemi ve Çözümleri

:::concept[N+1 Query Problem (İng: N+1 Query Problem)]
N+1 problemi, bir ana sorgu (1) ve her sonuç satırı için ayrı ayrı çalıştırılan N ek sorgu ile toplamda N+1 sorgu yapılmasıdır.

**Türkçe karşılığı:** N+1 Sorgu Problemi
**Ne işe yarar:** Bu problemi tanımak ve çözmek performansı dramatik artırır
**Gerçek hayat benzetmesi:** 30 kişilik sınıfta yoklama almak: Her öğrenciye tek tek "geldin mi?" diye sormak (N+1) vs listeyi bir kerede okumak (batch)
:::

:::code[javascript]{title="N+1 Problemi ve Çözümü"}
// KÖTÜ: N+1 Query (1 + N sorgu)
const orders = await Order.find();  // 1 sorgu: tüm siparişler
for (const order of orders) {
  order.user = await User.findById(order.userId); // N sorgu: her sipariş için 1
}
// 100 sipariş = 101 veritabanı sorgusu!

// İYİ: Eager Loading / Populate (2 sorgu)
const orders = await Order.find().populate('userId'); // MongoDB
// 1. SELECT * FROM orders
// 2. SELECT * FROM users WHERE id IN (1, 2, 3, ..., 100)

// İYİ: Prisma include (otomatik optimize)
const orders = await prisma.order.findMany({
  include: { user: true }
});

// İYİ: Drizzle JOIN (tek sorgu)
const orders = await db
  .select()
  .from(ordersTable)
  .leftJoin(users, eq(ordersTable.userId, users.id));

// İYİ: DataLoader pattern (batch + cache)
const userLoader = new DataLoader(async (userIds) => {
  const users = await User.find({ _id: { $in: userIds } });
  const userMap = new Map(users.map(u => [u.id.toString(), u]));
  return userIds.map(id => userMap.get(id.toString()));
});

// Her yerde userLoader.load(userId) kullan - otomatik batch'ler
:::

## SQL vs NoSQL Karar Matrisi

:::comparison
| Kriter | SQL (PostgreSQL) | NoSQL (MongoDB) |
|--------|-----------------|-----------------|
| Veri yapısı | Sabit şema, ilişkisel | Esnek şema, belge tabanlı |
| İlişkiler | JOIN ile güçlü | $lookup ile sınırlı |
| Ölçekleme | Dikey (daha güçlü sunucu) | Yatay (daha fazla sunucu) |
| Tutarlılık | Güçlü (ACID) | Eventual consistency (BASE) |
| Sorgulama | SQL (çok güçlü) | MQL (esnek) |
| **E-ticaret** | Sipariş, ödeme, stok | Ürün katalog, yorumlar |
| **Sosyal medya** | Kullanıcı ilişkileri | Feed, mesajlar, profiller |
| **Finans** | İşlemler, hesaplar | Log, audit trail |
| **IoT** | Raporlama | Sensör verisi akışı |

**Karar kuralı:** Verin ilişkisel mi? ACID gerekli mi? → SQL. Esnek şema mi? Yatay ölçekleme mi? → NoSQL. Emin değilsen → PostgreSQL ile başla.
:::

### CAP Theorem

:::concept[CAP Theorem (İng: CAP Theorem)]
CAP teoremi, dağıtık bir sistemin aynı anda en fazla üç özellikten ikisini garanti edebileceğini söyler: Consistency, Availability, Partition Tolerance.

**Türkçe karşılığı:** CAP Teoremi
**Ne işe yarar:** Dağıtık veritabanı seçerken trade-off'ları anlamayı sağlar
**Gerçek hayat benzetmesi:** Hızlı, kaliteli ve ucuz - üçünden en fazla ikisini seçebilirsin
:::

:::code[text]{title="CAP Theorem"}
C - Consistency (Tutarlılık):
    Her okuma en güncel veriyi döndürür.
    "Her şube aynı bakiyeyi gösterir."

A - Availability (Erişilebilirlik):
    Her istek bir yanıt alır (hata olmadan).
    "Banka her zaman açık."

P - Partition Tolerance (Bölünme Toleransı):
    Ağ bölünmelerinde sistem çalışmaya devam eder.
    "Şubeler arası iletişim kopsa bile çalışır."

Dağıtık sistemlerde P zorunludur → CP veya AP seçmelisin:
  CP: PostgreSQL, MongoDB (default) → Tutarlılık + bölünme toleransı
  AP: Cassandra, DynamoDB → Erişilebilirlik + bölünme toleransı
:::

:::interview
**Mülakat Sorusu:** "SQL ve NoSQL arasındaki farkları açıkla. Hangi durumda hangisini kullanırsın?"

**Beklenen cevap:**
SQL ilişkisel veri modeli kullanır, ACID uyumludur ve karmaşık JOIN'ler ile güçlü sorgulama sunar. NoSQL esnek şema, yatay ölçeklenebilirlik ve farklı veri modelleri (document, key-value, graph) sunar.

Seçim kriterleri:
- Veri ilişkileri güçlüyse (e-ticaret sipariş sistemi) → PostgreSQL
- Esnek şemaya ihtiyaç varsa (CMS, kullanıcı profili) → MongoDB
- Yüksek performanslı cache gerekiyorsa → Redis
- Her ikisini birlikte kullan (polyglot persistence)
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Mongoose ile Blog API Modelleri (Kolay)

MongoDB ve Mongoose kullanarak blog uygulamasi icin User, Post ve Comment modellerini olustur.

```javascript
const mongoose = require("mongoose");

// TODO: User schema
const userSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true, minlength: 2 },
  email: { type: String, required: true, unique: true, lowercase: true },
  // TODO: password (select: false ile varsayilan sorgularda gizle)
  // TODO: role: "admin" | "author" | "reader" (default: "reader")
  // TODO: createdAt (timestamps: true ile otomatik)
});

// TODO: Post schema — virtual populate ile comments
const postSchema = new mongoose.Schema({
  title: { type: String, required: true, maxlength: 200 },
  content: { type: String, required: true },
  author: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  tags: [{ type: String }],
  status: { type: String, enum: ["draft", "published"], default: "draft" },
  // TODO: viewCount (default: 0)
}, { timestamps: true });

// TODO: Comment schema — Post ve User referanslari
const commentSchema = new mongoose.Schema({
  // TODO: text, author (ref: User), post (ref: Post), createdAt
});

// TODO: Modelleri olustur ve CRUD islemleri test et:
// 1. Yeni user olustur
// 2. User id ile yeni post olustur
// 3. Post'a yorum ekle
// 4. Post'u populate ile author ve comments getir
const User = mongoose.model("User", userSchema);
const Post = mongoose.model("Post", postSchema);
const Comment = mongoose.model("Comment", commentSchema);
```

**Beklenen Sonuc:** 3 model olusturulmali. Post sorgularinda author bilgisi populate ile getirilmeli. Comment'ler post'a baglanmis olmali.
**Ipucu:** `Post.find().populate("author", "name email")` ile sadece ihtiyac duyulan alanlari getir.

---

### Alistirma 2: MongoDB Aggregation Pipeline (Orta)

Aggregation pipeline kullanarak karmasik veri analizi sorgulari yaz.

```javascript
// GOREV: Asagidaki aggregation pipeline'lari yaz

// 1. En cok yorum alan 5 yazi
const topCommentedPosts = await Post.aggregate([
  // TODO: $lookup ile comments koleksiyonunu birlestir
  // TODO: $addFields ile commentCount hesapla
  // TODO: $sort ile commentCount'a gore azalan sirala
  // TODO: $limit 5
  // TODO: $project ile sadece title, commentCount, author dondur
]);

// 2. Her author'un yazi sayisi ve toplam goruntuleme
const authorStats = await Post.aggregate([
  // TODO: $group — _id: "$author", postCount: $sum, totalViews: $sum
  // TODO: $lookup ile User bilgisini getir
  // TODO: $sort — totalViews'e gore azalan
]);

// 3. Tag bazli istatistikler
const tagStats = await Post.aggregate([
  // TODO: $unwind — tags arrayini parcala
  // TODO: $group — her tag icin post sayisi ve ortalama goruntuleme
  // TODO: $sort — postCount azalan
]);

// 4. Aylik yazi istatistikleri (son 6 ay)
const monthlyStats = await Post.aggregate([
  // TODO: $match — son 6 ay icindeki yazilar
  // TODO: $group — yil-ay bazinda gruplama, postCount hesaplama
  // TODO: $sort — tarih sirasina gore
]);

console.log("Top Posts:", topCommentedPosts);
console.log("Author Stats:", authorStats);
console.log("Tag Stats:", tagStats);
console.log("Monthly Stats:", monthlyStats);
```

**Beklenen Sonuc:** 4 aggregation pipeline calismali ve dogru sonuc dondurmeli. $lookup ile JOIN benzeri islem yapilmis olmali. Sonuclar siralanmis ve formatlanmis olmali.
**Ipucu:** `$lookup` ile baska koleksiyonu birlestir, `$unwind` array'i parcala, `$group` ile gruplama yap, `$project` ile ciktiya sekil ver.

---

### Alistirma 3: Redis Cache ve N+1 Cozumu (Zor)

Blog API'ne Redis cache ekle ve Mongoose populate ile N+1 problemini coz.

```javascript
const Redis = require("ioredis");
const redis = new Redis(); // localhost:6379

// Cache-Aside Pattern
async function getPostWithCache(postId) {
  const cacheKey = `post:${postId}`;

  // TODO: 1. Once cache'e bak
  const cached = await redis.get(cacheKey);
  if (cached) {
    console.log("Cache HIT");
    return JSON.parse(cached);
  }

  // TODO: 2. Cache'te yoksa DB'den getir
  console.log("Cache MISS");
  const post = await Post.findById(postId)
    .populate("author", "name email")
    .lean(); // plain object dondur (daha hizli)

  // TODO: 3. Cache'e kaydet (TTL: 5 dakika)
  if (post) {
    await redis.set(cacheKey, JSON.stringify(post), "EX", 300);
  }

  return post;
}

// TODO: Cache invalidation — post guncellendiginde cache'i temizle
async function updatePost(postId, data) {
  const post = await Post.findByIdAndUpdate(postId, data, { new: true });
  // TODO: Ilgili cache key'i sil
  await redis.del(`post:${postId}`);
  return post;
}

// N+1 Problemi — KOTU:
// const posts = await Post.find();
// for (const post of posts) {
//   post.author = await User.findById(post.author); // Her post icin ayri sorgu!
// }

// N+1 Cozumu — IYI:
async function getPostsWithAuthors() {
  // TODO: populate ile tek sorguda author bilgisini getir
  return Post.find()
    .populate("author", "name email")
    .sort("-createdAt")
    .limit(20);
}
```

**Beklenen Sonuc:** Ilk istekte "Cache MISS" logu gorunmeli, ikincisinde "Cache HIT". Post guncellendiginde cache temizlenmeli. N+1 cozumu ile sorgu sayisi 1'e dusmeli.
**Ipucu:** `docker run -p 6379:6379 redis:7` ile Redis baslat. `.lean()` Mongoose document yerine plain object dondurur (cache icin gerekli).
:::

:::knowledge-check
type: multiple_choice
question: "Redis'in en temel kullanım alanı hangisidir?"
options:
  - "Büyük dosya depolama"
  - "In-memory caching ve session storage"
  - "Karmaşık JOIN sorguları"
  - "Video streaming"
correct: 1
explanation: "Redis, RAM'de çalışan key-value store olarak en çok caching (veritabanı sorgularını cache'leme), session storage (kullanıcı oturumu) ve gerçek zamanlı özellikler (pub/sub, rate limiting) için kullanılır."
:::

:::knowledge-check
type: multiple_choice
question: "N+1 query probleminin çözümü hangisidir?"
options:
  - "Her sorguyu ayrı ayrı çalıştırmak"
  - "Veritabanı bağlantısını kapatmamak"
  - "Eager loading, batch queries veya DataLoader kullanmak"
  - "Daha hızlı sunucu kullanmak"
correct: 2
explanation: "N+1 problemi, ilişkili verileri teker teker sorgulamaktan kaynaklanır. Çözüm: Eager loading (Prisma include, Mongoose populate), batch queries (WHERE id IN (...)), veya DataLoader ile istekleri otomatik batch'lemek."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "CAP teoremini bir dagitik sistem ornegi ile acikla. MongoDB CP mi AP mi? Redis hangi kategoride? PostgreSQL? Her veritabaninin CAP trade-off'unu ve bunun uygulama tasarimini nasil etkiledigini gercek senaryolarla anlat. Ne zaman SQL, ne zaman NoSQL tercih etmeliyim?"

**2. Pratik Uygulama:**
> "Prisma ORM ile bir blog uygulamasinin veritabani katmanini olustur: schema.prisma dosyasinda User, Post, Comment, Tag modelleri ve iliskileri tanimla. Migration olustur, seed data ekle. CRUD operasyonlari icin service fonksiyonlari yaz. Prisma Client'in type-safe sorgularini goster."
> Takip: "Simdi ayni verileri Redis ile cache'le. Cache-aside pattern uygula: once Redis'e bak, yoksa PostgreSQL'den cek ve Redis'e yaz. Cache invalidation stratejisini belirle."

**3. Mukemmellik Icin:**
> "Bir SaaS urununde polyglot persistence stratejisi tasarliyorum. Kullanici verileri PostgreSQL'de, oturum verileri Redis'te, arama indexi Elasticsearch'te, dosya metadata'si MongoDB'de olacak. Bu coklu veritabani mimarisinde veri tutarliligi, transaction yonetimi ve migration stratejisi nasil olmali?"

### Pair Programming Ipucu
ORM kullanirken AI'a Prisma schema veya Mongoose model tanimini goster ve sor: "Bu model taniminda N+1 sorgu riski var mi? include/populate stratejim dogru mu? Hangi alanlara index eklemeliyim? Query performansini nasil optimize ederim?"
:::

:::must-note
- MongoDB: document-based, esnek şema, BSON formatı, $lookup ile JOIN, aggregation pipeline ile karmaşık sorgular
- Redis veri yapıları: String (cache), Hash (profil), List (kuyruk/bildirim), Set (benzersiz), Sorted Set (leaderboard)
- Caching pattern'leri: Cache-Aside (lazy load), Write-Through (yazarken cache'le), Write-Behind (asenkron)
- Redis TTL (Time To Live): set key value EX 3600 → 1 saat sonra otomatik silinir
- ORM karşılaştırma: Prisma (type-safe, otomatik migration), Drizzle (hafif, SQL-benzeri), Sequelize (legacy)
- N+1 problemi: 100 satır = 101 sorgu. Çözüm: include/populate/JOIN/DataLoader
- CAP teoremi: C (tutarlılık) + A (erişilebilirlik) + P (bölünme toleransı) - en fazla ikisini seç. P zorunlu → CP veya AP
- SQL vs NoSQL karar: ilişkisel veri + ACID → SQL, esnek şema + yatay ölçek → NoSQL, cache → Redis
- Polyglot persistence: farklı veriler için farklı veritabanları (PostgreSQL + Redis + MongoDB)
- MongoDB index'leri: createIndex, compound index, text index. explain() ile sorgu planı kontrol et
:::

:::senior-learns
Bir Senior Developer veya CTO, NoSQL ve ORM konusunu öğrenirken şu yaklaşımı benimser:

1. **Veri modelleme ile başlar** - Hangi veriyi nasıl sorgulayacağını önceden düşünür. MongoDB'de "query-driven design" yapar: önce sorguları belirle, sonra schema'yı ona göre tasarla. Denormalizasyon kararlarını bilinçli verir.
2. **Cache invalidation stratejisi geliştirir** - "Cache invalidation bilgisayar biliminin en zor iki probleminden biridir." TTL-based, event-driven ve tag-based invalidation'ı duruma göre seçer. Stale data toleransını iş birimleriyle konuşur.
3. **Redis'i production'da yönetir** - Redis Sentinel veya Redis Cluster ile high availability sağlar. Memory policy (maxmemory-policy) ayarlar: allkeys-lru, volatile-ttl. Redis Streams ile event sourcing yapar.
4. **ORM'un sınırlarını bilir** - Complex query'ler için raw SQL yazmaktan çekinmez. ORM'un ürettiği sorguyu logging ile izler. Prisma'da $queryRaw, Drizzle'da sql template kullanır.
5. **Database per service pattern uygular** - Microservice mimarisinde her servisin kendi veritabanı olur. Event-driven communication ile servisler arası veri senkronizasyonu sağlar. CQRS ve Event Sourcing pattern'lerini değerlendirir.
6. **Monitoring ve performance tuning yapar** - MongoDB'de profiler, Redis'te SLOWLOG, PostgreSQL'de pg_stat_statements ile yavaş sorguları tespit eder. Connection pool size, query timeout, retry logic ayarlarını production yüküne göre optimize eder.

**Profesyonel Mindset:** "Veritabanı seçimi, projenin en kritik kararlarından biridir ve sonradan değiştirmesi en zor olanıdır. Her veritabanının güçlü ve zayıf yönlerini bil, iş gereksinimlerini analiz et, prototip yap ve benchmark al. 'Herkes MongoDB kullanıyor' veya 'SQL eski teknoloji' gibi klişelere kanma - verin doğası ve sorgu pattern'lerin karar verici olmalı."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Document** (dok-yoo-ment) → Belge
   *"MongoDB stores data as JSON-like documents in collections."*

2. **Cache** (kæʃ) → Önbellek
   *"We implemented a Redis cache layer to reduce database load by 80%."*

3. **Schema** (skee-muh) → Şema / Veri yapısı
   *"MongoDB is schema-flexible, allowing different document structures in the same collection."*

4. **Pipeline** (payp-layn) → Boru Hattı / İşlem Hattı
   *"The aggregation pipeline processes documents through a sequence of stages."*

5. **Persistence** (pur-sis-tens) → Kalıcılık
   *"Redis supports data persistence through RDB snapshots and AOF logging."*

**Okuma Egzersizi:** MongoDB resmi dökümanında "Introduction to MongoDB" bölümünü İngilizce oku: https://www.mongodb.com/docs/manual/introduction/

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Kullanıcı API'sine Redis cache ekledim"
→ Örnek: `perf: add Redis caching layer to user API endpoints`
:::

:::external-resource
- 📺 **Traversy Media:** "MongoDB Crash Course" (1 saat, YouTube, ücretsiz)
- 📖 **MongoDB University:** learn.mongodb.com (resmi kurslar, ücretsiz)
- 📖 **Redis University:** university.redis.com (resmi kurslar, ücretsiz)
- 📖 **Prisma Docs:** prisma.io/docs (resmi, ücretsiz)
- 📖 **Drizzle Docs:** orm.drizzle.team (resmi, ücretsiz)
- 🎮 **Try Redis:** try.redis.io (interaktif Redis öğrenme, ücretsiz)
:::
