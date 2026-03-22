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

MongoDB ve Mongoose kullanarak blog uygulamasi icin User, Post ve Comment modellerini oluştur.

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

**Beklenen Sonuc:** 3 model oluşturulmali. Post sorgularinda author bilgisi populate ile getirilmeli. Comment'ler post'a baglanmis olmali.
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

**Beklenen Sonuc:** 4 aggregation pipeline çalışmali ve dogru sonuc dondurmeli. $lookup ile JOIN benzeri islem yapilmis olmali. Sonuclar siralanmis ve formatlanmis olmali.
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

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "CAP teoremini bir dagitik sistem örneği ile acikla. MongoDB CP mi AP mi? Redis hangi kategoride? PostgreSQL? Her veritabaninin CAP trade-off'unu ve bunun uygulama tasarimini nasil etkiledigini gercek senaryolarla anlat. Ne zaman SQL, ne zaman NoSQL tercih etmeliyim?"

**2. Pratik Uygulama:**
> "Prisma ORM ile bir blog uygulamasinin veritabani katmanini oluştur: schema.prisma dosyasinda User, Post, Comment, Tag modelleri ve iliskileri tanimla. Migration oluştur, seed data ekle. CRUD operasyonlari icin service fonksiyonlari yaz. Prisma Client'in type-safe sorgularini goster."
> Takip: "Simdi ayni verileri Redis ile cache'le. Cache-aside pattern uygula: once Redis'e bak, yoksa PostgreSQL'den cek ve Redis'e yaz. Cache invalidation stratejisini belirle."

**3. Mukemmellik Icin:**
> "Bir SaaS urununde polyglot persistence stratejisi tasarliyorum. Kullanici verileri PostgreSQL'de, oturum verileri Redis'te, arama indexi Elasticsearch'te, dosya metadata'si MongoDB'de olacak. Bu coklu veritabani mimarisinde veri tutarliligi, transaction yonetimi ve migration stratejisi nasil olmali?"

### Pair Programming Ipucu
ORM kullanirken AI'a Prisma schema veya Mongoose model tanimini goster ve sor: "Bu model taniminda N+1 sorgu riski var mi? include/populate stratejim dogru mu? Hangi alanlara index eklemeliyim? Query performansini nasil optimize ederim?"
:::

:::exercise
### Alıştırma 4: MongoDB CRUD İşlemleri
**Görev:** MongoDB shell komutları ile temel CRUD işlemlerini yap.
**Başlangıç kodu:**
```javascript
// Koleksiyon: products

// TODO 1: Yeni ürün ekle (insertOne)
// TODO 2: Fiyatı 100-500 arası olan ürünleri bul
// TODO 3: Kategorisi "electronics" olan ürünlerin fiyatını %10 artır
// TODO 4: Stoku 0 olan ürünleri sil
// TODO 5: Aggregation ile kategori bazlı ortalama fiyat hesapla
```
**Beklenen çıktı:**
```javascript
// 1. Insert
db.products.insertOne({
  name: "Wireless Mouse",
  price: 199.99,
  category: "electronics",
  stock: 50,
  tags: ["wireless", "mouse", "computer"],
  specs: { color: "black", weight: "80g" },
  createdAt: new Date(),
});

// 2. Find with range
db.products.find({
  price: { $gte: 100, $lte: 500 }
}).sort({ price: 1 });

// 3. Update many
db.products.updateMany(
  { category: "electronics" },
  { $mul: { price: 1.10 } }  // %10 artır
);

// 4. Delete many
db.products.deleteMany({ stock: 0 });

// 5. Aggregation pipeline
db.products.aggregate([
  { $group: {
    _id: "$category",
    avgPrice: { $avg: "$price" },
    count: { $sum: 1 },
    maxPrice: { $max: "$price" },
  }},
  { $sort: { avgPrice: -1 } },
]);
```
**İpucu:** MongoDB'de `$gte` (>=), `$lte` (<=), `$mul` (çarpma), `$inc` (artırma). Aggregation pipeline aşamaları sırayla çalışır: `$match` -> `$group` -> `$sort`.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: Mongoose Schema ve Model
**Görev:** Mongoose ile TypeScript uyumlu schema, model ve ilişkilendirme (populate) yaz.
**Başlangıç kodu:**
```typescript
import mongoose, { Schema, Document } from "mongoose";

// TODO: User ve Post schema/model tanımla
// - User: name, email (unique), password, role (enum), posts (ref)
// - Post: title, content, author (ref: User), tags, published
// - Virtual field: User.fullUrl
// - Middleware: pre('save') ile şifre hashleme
// - Populate ile kullanım
```
**Beklenen çıktı:**
```typescript
interface IUser extends Document {
  name: string;
  email: string;
  password: string;
  role: "user" | "admin";
  createdAt: Date;
}

const userSchema = new Schema<IUser>({
  name: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true, minlength: 8, select: false },
  role: { type: String, enum: ["user", "admin"], default: "user" },
}, { timestamps: true, toJSON: { virtuals: true } });

// Virtual: User'ın post'ları
userSchema.virtual("posts", {
  ref: "Post",
  localField: "_id",
  foreignField: "author",
});

// Middleware: şifre hashleme
userSchema.pre("save", async function(next) {
  if (!this.isModified("password")) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

const User = mongoose.model<IUser>("User", userSchema);

// Post schema
const postSchema = new Schema({
  title: { type: String, required: true },
  content: { type: String, required: true },
  author: { type: Schema.Types.ObjectId, ref: "User", required: true },
  tags: [{ type: String }],
  published: { type: Boolean, default: false },
}, { timestamps: true });

const Post = mongoose.model("Post", postSchema);

// Populate kullanımı
const user = await User.findById(id).populate("posts");
const post = await Post.findById(id).populate("author", "name email");
```
**İpucu:** `select: false` ile password varsayılan sorgularda gelmez. `populate("author", "name email")` ile sadece belirli alanları getir. Virtual populate ile ilişki kurulabilir.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: Redis Veri Yapıları ve Kullanım Senaryoları
**Görev:** Redis'in farklı veri yapılarını gerçek senaryolarda kullan.
**Başlangıç kodu:**
```javascript
const Redis = require("ioredis");
const redis = new Redis();

// TODO 1: String - API response cache'le (TTL ile)
// TODO 2: Hash - Kullanıcı oturumu sakla
// TODO 3: List - Bildirim kuyruğu
// TODO 4: Sorted Set - Leaderboard (en yüksek puan sıralaması)
// TODO 5: Set - Online kullanıcılar listesi
```
**Beklenen çıktı:**
```javascript
// 1. String - Cache
async function getCachedProducts(category) {
  const cacheKey = `products:${category}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const products = await db.products.find({ category });
  await redis.set(cacheKey, JSON.stringify(products), "EX", 3600); // 1 saat TTL
  return products;
}

// 2. Hash - Oturum
async function createSession(userId, data) {
  const sessionId = crypto.randomUUID();
  await redis.hset(`session:${sessionId}`, {
    userId: userId.toString(),
    email: data.email,
    role: data.role,
    createdAt: Date.now().toString(),
  });
  await redis.expire(`session:${sessionId}`, 86400); // 24 saat
  return sessionId;
}

// 3. List - Bildirim kuyruğu
await redis.lpush(`notifications:${userId}`, JSON.stringify({
  type: "new_order", message: "Yeni sipariş!", timestamp: Date.now()
}));
const notifications = await redis.lrange(`notifications:${userId}`, 0, 9); // Son 10

// 4. Sorted Set - Leaderboard
await redis.zadd("leaderboard", score, `user:${userId}`);
const top10 = await redis.zrevrange("leaderboard", 0, 9, "WITHSCORES");

// 5. Set - Online kullanıcılar
await redis.sadd("online_users", userId);
await redis.srem("online_users", userId); // Çıkış
const onlineCount = await redis.scard("online_users");
const isOnline = await redis.sismember("online_users", friendId);
```
**İpucu:** String = cache, Hash = profil/oturum (alan bazlı erişim), List = kuyruk/bildirim, Set = benzersiz koleksiyon, Sorted Set = sıralı veri (leaderboard). Her yapı farklı use-case için optimize.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: Cache-Aside Pattern Uygulaması
**Görev:** Express middleware olarak Cache-Aside (Lazy Loading) pattern'ini uygula.
**Başlangıç kodu:**
```javascript
// TODO: Cache middleware yaz
// 1. Request gelince Redis'te cache'e bak
// 2. Cache'te varsa direkt döndür
// 3. Yoksa route handler çalışsın, response'u cache'le
// 4. Cache invalidation stratejisi

// Bonus: Cache key'i nasıl oluşturulur? (URL + query params)
```
**Beklenen çıktı:**
```javascript
function cacheMiddleware(ttl = 300) {
  return async (req, res, next) => {
    if (req.method !== "GET") return next();

    const cacheKey = `cache:${req.originalUrl}`;

    try {
      const cached = await redis.get(cacheKey);
      if (cached) {
        return res.json(JSON.parse(cached));
      }
    } catch (err) {
      console.error("Redis cache hatası:", err);
    }

    // Response'u yakalayıp cache'le
    const originalJson = res.json.bind(res);
    res.json = (body) => {
      redis.set(cacheKey, JSON.stringify(body), "EX", ttl).catch(console.error);
      return originalJson(body);
    };

    next();
  };
}

// Cache invalidation
function invalidateCache(pattern) {
  return async (req, res, next) => {
    res.on("finish", async () => {
      if (res.statusCode >= 200 && res.statusCode < 300) {
        const keys = await redis.keys(`cache:${pattern}`);
        if (keys.length) await redis.del(...keys);
      }
    });
    next();
  };
}

// Kullanım
app.get("/api/products", cacheMiddleware(600), getProducts);
app.post("/api/products", invalidateCache("/api/products*"), createProduct);
```
**İpucu:** GET istekleri cache'le, POST/PUT/DELETE sonrası ilgili cache'i invalidate et. Redis bağlantısı koparsa cache'siz devam et (graceful degradation).
**Zorluk:** Zor
:::

:::exercise
### Alıştırma 8: Prisma ORM ile CRUD
**Görev:** Prisma schema tanımla ve type-safe CRUD operasyonları yaz.
**Başlangıç kodu:**
```prisma
// TODO: schema.prisma dosyasını tamamla
// User, Post, Comment modelleri
// İlişkiler: User -> Post (1:N), Post -> Comment (1:N), User -> Comment (1:N)
```
**Beklenen çıktı:**
```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int       @id @default(autoincrement())
  email     String    @unique
  name      String
  password  String
  posts     Post[]
  comments  Comment[]
  createdAt DateTime  @default(now()) @map("created_at")
  updatedAt DateTime  @updatedAt @map("updated_at")

  @@map("users")
}

model Post {
  id        Int       @id @default(autoincrement())
  title     String
  content   String
  published Boolean   @default(false)
  author    User      @relation(fields: [authorId], references: [id])
  authorId  Int       @map("author_id")
  comments  Comment[]
  createdAt DateTime  @default(now())

  @@index([authorId])
  @@map("posts")
}

model Comment {
  id       Int    @id @default(autoincrement())
  text     String
  post     Post   @relation(fields: [postId], references: [id], onDelete: Cascade)
  postId   Int
  author   User   @relation(fields: [authorId], references: [id])
  authorId Int

  @@map("comments")
}
```
```typescript
// Prisma CRUD
// Create
const user = await prisma.user.create({
  data: { name: "Ali", email: "ali@test.com", password: hashedPw },
});

// Read with relations
const post = await prisma.post.findUnique({
  where: { id: 1 },
  include: { author: { select: { name: true, email: true } }, comments: true },
});

// Update
await prisma.post.update({
  where: { id: 1 },
  data: { published: true },
});

// Delete with cascade
await prisma.post.delete({ where: { id: 1 } }); // comments da silinir

// Transaction
await prisma.$transaction([
  prisma.user.update({ where: { id: 1 }, data: { name: "Yeni Ad" } }),
  prisma.post.updateMany({ where: { authorId: 1 }, data: { published: false } }),
]);
```
**İpucu:** Prisma type-safe: yanlış alan adı veya tip kullanırsan TypeScript derleme hatası verir. `include` ile ilişkili veriyi getir, `select` ile sadece belirli alanları al.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: N+1 Query Tespiti ve Çözümü
**Görev:** ORM kullanırken N+1 query problemini tespit et ve çöz.
**Başlangıç kodu:**
```typescript
// YANLIŞ: N+1 problemi var
async function getUsersWithPosts() {
  const users = await prisma.user.findMany(); // 1 sorgu

  for (const user of users) {
    // Her user için ayrı sorgu (N sorgu!)
    const posts = await prisma.post.findMany({
      where: { authorId: user.id },
    });
    user.posts = posts;
  }

  return users;
}

// TODO: N+1 problemini 3 farklı yöntemle çöz
```
**Beklenen çıktı:**
```typescript
// Yöntem 1: Prisma include (eager loading)
async function getUsersWithPosts_v1() {
  return prisma.user.findMany({
    include: { posts: true },
  });
  // Arka planda 2 sorgu: SELECT users + SELECT posts WHERE author_id IN (...)
}

// Yöntem 2: Prisma select (sadece gerekli alanlar)
async function getUsersWithPosts_v2() {
  return prisma.user.findMany({
    select: {
      id: true,
      name: true,
      posts: {
        select: { id: true, title: true },
        take: 5, // Her user'dan max 5 post
      },
    },
  });
}

// Yöntem 3: Manuel batch (DataLoader benzeri)
async function getUsersWithPosts_v3() {
  const users = await prisma.user.findMany();
  const userIds = users.map(u => u.id);

  const posts = await prisma.post.findMany({
    where: { authorId: { in: userIds } },
  });

  const postsByUser = posts.reduce((acc, post) => {
    if (!acc[post.authorId]) acc[post.authorId] = [];
    acc[post.authorId].push(post);
    return acc;
  }, {} as Record<number, typeof posts>);

  return users.map(u => ({ ...u, posts: postsByUser[u.id] || [] }));
}
```
**İpucu:** N+1 tespit: DB query loglarını aç ve aynı tabloya N kez sorgu gittiğini gör. Çözüm: eager loading (include), batch loading (IN query), veya DataLoader.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: SQL vs NoSQL Karar Verme
**Görev:** Aşağıdaki senaryolar için doğru veritabanını seç ve nedenini açıkla.
**Başlangıç kodu:**
```
Senaryolar:
1. Bankacılık işlemleri (para transferi, hesap bakiyesi)
2. Sosyal medya kullanıcı profilleri (değişken alanlar)
3. IoT sensör verileri (saniyede binlerce veri noktası)
4. E-ticaret ürün kataloğu (farklı kategorilerin farklı özellikleri)
5. Oturum yönetimi (milisaniye seviyesinde erişim)
6. Log analizi (büyük hacimli, zamana dayalı veri)
7. Öneri sistemi (kullanıcı-ürün ilişkileri)
8. Gerçek zamanlı skor tablosu

TODO: Her biri için PostgreSQL/MongoDB/Redis/Elasticsearch/Neo4j seç
```
**Beklenen çıktı:**
```
1. Bankacılık → PostgreSQL ✓
   Neden: ACID transaction'lar zorunlu, veri tutarlılığı kritik

2. Kullanıcı profilleri → MongoDB ✓
   Neden: Esnek şema (biyografi, sosyal linkler kullanıcıya göre değişir)

3. IoT sensör verileri → TimescaleDB (PostgreSQL) veya InfluxDB
   Neden: Zaman serisi optimizasyonu, otomatik partitioning

4. E-ticaret ürün kataloğu → MongoDB ✓ (veya PostgreSQL JSONB)
   Neden: Telefon specs ≠ kıyafet specs, esnek şema gerekli

5. Oturum yönetimi → Redis ✓
   Neden: Sub-millisecond erişim, TTL ile otomatik expire

6. Log analizi → Elasticsearch ✓
   Neden: Full-text search, aggregation, Kibana ile görselleştirme

7. Öneri sistemi → Neo4j (Graph DB) ✓
   Neden: "Bu ürünü alanlar bunları da aldı" = graph traversal

8. Gerçek zamanlı skor tablosu → Redis Sorted Set ✓
   Neden: ZADD/ZRANGE O(log N), anında sıralama
```
**İpucu:** Tek veritabanı her sorunu çözmez. Polyglot persistence: ana veri PostgreSQL'de, cache Redis'te, arama Elasticsearch'te, ilişki analizi Neo4j'de olabilir.
**Zorluk:** Kolay
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
