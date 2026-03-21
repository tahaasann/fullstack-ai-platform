---
title: "RESTful API Tasarımı: Prensipler, Versioning ve Pagination"
id: mod-10-api/lesson-01
estimated_minutes: 50
order: 1
tags: ["rest", "api-design", "versioning", "pagination", "hateoas", "http"]
prerequisites: ["mod-09-node/lesson-01"]
---

# RESTful API Tasarımı: Prensipler, Versioning ve Pagination

:::realworld
Her modern uygulamanın arkasında API'ler var. Stripe'ın ödeme API'si, Twitter'ın tweet API'si, Google Maps'in harita API'si - hepsi RESTful prensiplerle tasarlanmış. İyi tasarlanmış bir API, geliştiricilerin dakikalar içinde entegre olmasını sağlar. Kötü tasarlanmış bir API ise destek taleplerini, hataları ve geliştirici memnuniyetsizliğini artırır. Bu derste, profesyonel ve uzun ömürlü API'ler tasarlamanın kurallarını öğreneceksin.
:::

## REST Nedir?

:::concept[REST (İng: Representational State Transfer)]
REST, web servisleri tasarlamak için kullanılan bir mimari stildir. Roy Fielding tarafından 2000 yılında doktora tezinde tanımlanmıştır.

**Türkçe karşılığı:** Temsili Durum Transferi
**Ne işe yarar:** Client-server iletişimi için tutarlı ve öngörülebilir bir arayüz sağlar
**Gerçek hayat benzetmesi:** Bir kütüphane sistemi gibi düşün - kitapları (resource) katalog numarasıyla (URL) bulursun, ödünç alırsın (GET), iade edersin (PUT), yeni kitap kaydedersin (POST), kaydı silersin (DELETE)
:::

### REST'in 6 Prensibi

:::code[text]{title="REST Kısıtlamaları (Constraints)"}
1. Client-Server    → İstemci ve sunucu birbirinden bağımsızdır
2. Stateless        → Her istek kendi başına yeterlidir (sunucu state tutmaz)
3. Cacheable        → Yanıtlar cache'lenebilir olarak işaretlenebilir
4. Uniform Interface → Tutarlı URL yapısı ve HTTP method kullanımı
5. Layered System   → Client, doğrudan sunucuyla mı proxy ile mi konuştuğunu bilmez
6. Code on Demand   → (Opsiyonel) Sunucu, istemciye çalıştırılabilir kod gönderebilir
:::

:::deha-tip
Deha seviyesi geliştiriciler, REST'i sadece "URL + HTTP method" olarak görmez. REST'in asıl gücü stateless ve uniform interface prensiplerindedir. Stateless olması sayesinde API horizontal olarak scale edilebilir (load balancer arkasına birden fazla sunucu koyabilirsin). Uniform interface sayesinde API'yi hiç görmemiş bir geliştirici bile URL yapısından ne yapacağını anlayabilir.
:::

## Resource Naming (URL Tasarımı)

:::code[text]{title="URL Tasarım Kuralları"}
✅ DOĞRU (İsimlendirme Kuralları):
GET    /api/v1/users              → Tüm kullanıcıları getir
GET    /api/v1/users/123          → ID=123 kullanıcıyı getir
POST   /api/v1/users              → Yeni kullanıcı oluştur
PUT    /api/v1/users/123          → Kullanıcı 123'ü tamamen güncelle
PATCH  /api/v1/users/123          → Kullanıcı 123'ü kısmen güncelle
DELETE /api/v1/users/123          → Kullanıcı 123'ü sil

GET    /api/v1/users/123/orders           → Kullanıcı 123'ün siparişleri
GET    /api/v1/users/123/orders/456       → Sipariş 456'nın detayı
POST   /api/v1/users/123/orders           → Kullanıcı 123 için yeni sipariş

❌ YANLIŞ (Bunları yapma):
GET    /api/v1/getUsers            → Fiil kullanma, isim kullan
GET    /api/v1/user                → Tekil değil çoğul kullan
POST   /api/v1/createUser          → HTTP method zaten eylemi belirtir
GET    /api/v1/Users               → Küçük harf kullan
GET    /api/v1/user_list           → Tire (-) kullan, alt tire (_) kullanma
DELETE /api/v1/deleteUser/123      → Fiili URL'den çıkar
:::

### HTTP Methods Mapping

:::comparison
| HTTP Method | CRUD | Örnek | Idempotent | Safe |
|-------------|------|-------|------------|------|
| **GET** | Read | Kullanıcı bilgisi getir | Evet | Evet |
| **POST** | Create | Yeni kullanıcı oluştur | Hayır | Hayır |
| **PUT** | Update (Full) | Tüm alanları güncelle | Evet | Hayır |
| **PATCH** | Update (Partial) | Sadece belirli alanları güncelle | Hayır* | Hayır |
| **DELETE** | Delete | Kullanıcıyı sil | Evet | Hayır |
| **HEAD** | Metadata | Sadece header'ları getir (body yok) | Evet | Evet |
| **OPTIONS** | Info | Desteklenen method'ları sor (CORS preflight) | Evet | Evet |

*PATCH idempotent olabilir ama spesifikasyon bunu garanti etmez.
**Safe** = Sunucu state'ini değiştirmez. **Idempotent** = Aynı isteği tekrarlasan aynı sonucu alırsın.
:::

:::concept[Idempotency (İng: Idempotency)]
Bir operasyonun birden fazla kez uygulanmasının, bir kez uygulanmasıyla aynı sonucu vermesi demektir.

**Türkçe karşılığı:** Etkisizlik / Aynı sonucu verme özelliği
**Ne işe yarar:** Ağ hatalarında isteğin güvenle tekrar gönderilebilmesini sağlar
**Gerçek hayat benzetmesi:** Asansör düğmesine birden fazla basmak gibi - kaçıncı basışta olursan ol, asansör aynı kata gelir
:::

:::code[javascript]{title="Idempotency Örnekleri"}
// PUT idempotent'tir - aynı isteği 10 kez gönder, sonuç aynı
// PUT /api/users/123  body: { name: "Ali", email: "ali@test.com" }
// 1. istek: name="Ali" olarak günceller
// 2. istek: name zaten "Ali", aynı kalır

// POST idempotent DEĞİLDİR - her istek yeni kayıt oluşturur
// POST /api/users  body: { name: "Ali" }
// 1. istek: Ali (id=1) oluşturur
// 2. istek: Ali (id=2) oluşturur ← Duplicate!

// Idempotency key ile POST'u güvenli yapma
app.post('/api/payments', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];

  if (idempotencyKey) {
    const existing = await Payment.findOne({
      where: { idempotencyKey }
    });
    if (existing) {
      return res.json(existing); // Aynı sonucu döndür
    }
  }

  const payment = await Payment.create({
    ...req.body,
    idempotencyKey,
  });
  res.status(201).json(payment);
});
:::

## HTTP Status Codes

:::code[text]{title="Sık Kullanılan HTTP Status Code'ları"}
2xx - Başarı
  200 OK              → GET, PUT, PATCH başarılı
  201 Created         → POST ile yeni kayıt oluşturuldu
  204 No Content      → DELETE başarılı (body yok)

3xx - Yönlendirme
  301 Moved Permanently → Kaynak kalıcı olarak taşındı
  304 Not Modified      → Cache'deki versiyon güncel

4xx - Client Hatası
  400 Bad Request     → Geçersiz istek (validation hatası)
  401 Unauthorized    → Kimlik doğrulama gerekli (giriş yapılmamış)
  403 Forbidden       → Yetki yok (giriş yapılmış ama izin yok)
  404 Not Found       → Kaynak bulunamadı
  405 Method Not Allowed → Bu URL'de bu HTTP method desteklenmiyor
  409 Conflict        → Çakışma (duplicate email gibi)
  422 Unprocessable Entity → Veri formatı doğru ama semantik hatalı
  429 Too Many Requests → Rate limit aşıldı

5xx - Server Hatası
  500 Internal Server Error → Sunucu hatası (beklenmeyen)
  502 Bad Gateway          → Proxy/gateway arkasındaki sunucu yanıt vermedi
  503 Service Unavailable  → Sunucu geçici olarak kullanılamıyor
  504 Gateway Timeout      → Proxy/gateway timeout
:::

:::beginner-mistake
Yaygın hata: Her hatada 200 OK döndürüp body'de `{ success: false, error: "..." }` yazmak. Bu anti-pattern'dir. HTTP status code'ları tam olarak bu amaç için tasarlanmıştır. Client tarafı (axios, fetch) status code'a göre hata yönetimi yapar. 200 dönersen client hata olduğunu anlayamaz.
:::

## API Versioning

:::code[text]{title="API Versioning Stratejileri"}
1. URL Versioning (En yaygın)
   GET /api/v1/users
   GET /api/v2/users
   ✅ Basit, açık, cache-friendly
   ❌ URL kirliliği

2. Header Versioning
   GET /api/users
   Accept: application/vnd.myapi.v1+json
   ✅ Temiz URL'ler
   ❌ Test ve debug zor, tarayıcıdan test edilemez

3. Query Parameter Versioning
   GET /api/users?version=1
   GET /api/users?version=2
   ✅ Basit
   ❌ Cache sorunları, opsiyonel olabilir

4. Content Negotiation
   GET /api/users
   Accept: application/json; version=1
   ✅ HTTP standardına uygun
   ❌ Karmaşık
:::

:::code[javascript]{title="Express'te URL Versioning"}
const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// v1/routes/users.js
router.get('/users', (req, res) => {
  res.json(users.map(u => ({
    id: u.id,
    name: u.name,
    email: u.email,
  })));
});

// v2/routes/users.js - Yeni alan eklendi
router.get('/users', (req, res) => {
  res.json(users.map(u => ({
    id: u.id,
    fullName: u.name, // alan adı değişti
    email: u.email,
    avatar: u.avatar, // yeni alan
    createdAt: u.createdAt,
  })));
});
:::

:::tip
API versioning stratejisi olarak URL versioning tavsiye edilir. Basit, açık ve en yaygın yöntemdir. Stripe, GitHub, Google ve Twitter gibi büyük şirketler URL versioning kullanır. Eski versiyonları en az 12-24 ay destekle ve deprecation notice ile kullanıcıları bilgilendir.
:::

## Pagination

:::concept[Pagination (İng: Pagination)]
Büyük veri setlerini sayfalara bölerek sunma tekniğidir. API'den binlerce kaydı tek seferde döndürmek hem sunucu hem client için verimsizdir.

**Türkçe karşılığı:** Sayfalama
**Ne işe yarar:** Büyük veri setlerini yönetilebilir parçalara böler
**Gerçek hayat benzetmesi:** Bir kitabın sayfa numaraları gibi - tüm kitabı tek sayfada okuyamazsın, sayfalara bölünerek okunabilir hale gelir
:::

:::comparison
| Özellik | Offset-Based | Cursor-Based |
|---------|-------------|--------------|
| **Kullanım** | `?page=2&limit=20` | `?cursor=abc123&limit=20` |
| **Performans** | Büyük offset'lerde yavaşlar (OFFSET 10000) | Her zaman hızlı |
| **Tutarlılık** | Yeni kayıt eklenince sayfa kayar | Her zaman tutarlı |
| **Toplam sayfa** | Kolay hesaplanır (COUNT) | Zor/imkansız |
| **Rastgele sayfa** | Mümkün (?page=50) | Mümkün değil |
| **Kullanım alanı** | Admin paneli, basit listeler | Feed, timeline, sonsuz scroll |

**Tavsiye:** Basit CRUD uygulamalar için offset-based, büyük veri setleri ve real-time feed'ler için cursor-based kullan.
:::

:::code[javascript]{title="Offset-Based Pagination"}
// GET /api/users?page=2&limit=20
app.get('/api/users', async (req, res) => {
  const page = Math.max(1, parseInt(req.query.page) || 1);
  const limit = Math.min(100, Math.max(1, parseInt(req.query.limit) || 20));
  const offset = (page - 1) * limit;

  const { count, rows } = await User.findAndCountAll({
    offset,
    limit,
    order: [['createdAt', 'DESC']],
  });

  const totalPages = Math.ceil(count / limit);

  res.json({
    data: rows,
    pagination: {
      currentPage: page,
      totalPages,
      totalItems: count,
      itemsPerPage: limit,
      hasNextPage: page < totalPages,
      hasPrevPage: page > 1,
    },
  });
});
:::

:::code[javascript]{title="Cursor-Based Pagination"}
// GET /api/posts?cursor=2024-01-15T10:30:00Z&limit=20
app.get('/api/posts', async (req, res) => {
  const limit = Math.min(100, parseInt(req.query.limit) || 20);
  const cursor = req.query.cursor; // Son görülen kaydın tarihi

  const where = cursor
    ? { createdAt: { [Op.lt]: new Date(cursor) } }
    : {};

  const posts = await Post.findAll({
    where,
    limit: limit + 1, // Bir fazla çek (hasMore kontrolü için)
    order: [['createdAt', 'DESC']],
  });

  const hasMore = posts.length > limit;
  const data = hasMore ? posts.slice(0, limit) : posts;
  const nextCursor = hasMore
    ? data[data.length - 1].createdAt.toISOString()
    : null;

  res.json({
    data,
    pagination: {
      nextCursor,
      hasMore,
      limit,
    },
  });
});
:::

## Error Response Standardizasyonu (RFC 7807)

:::concept[RFC 7807 - Problem Details (İng: Problem Details for HTTP APIs)]
RFC 7807, API hata yanıtları için standart bir format tanımlar. Bu sayede farklı API'ler tutarlı hata formatı kullanır.

**Türkçe karşılığı:** HTTP API'ler İçin Problem Detayları
**Ne işe yarar:** Tüm hata yanıtlarını standart bir formatta döndürerek client tarafının hata işlemesini kolaylaştırır
**Gerçek hayat benzetmesi:** Hastane raporları gibi - hangi hastaneye gidersen git, rapor formatı standarttır (hasta bilgileri, teşhis, tedavi)
:::

:::code[javascript]{title="RFC 7807 Problem Details Formatı"}
// Standart hata yanıt formatı
const errorResponse = {
  type: 'https://api.myapp.com/errors/validation-error',
  title: 'Validation Error',
  status: 400,
  detail: 'Email alanı geçerli bir email adresi olmalıdır',
  instance: '/api/v1/users',
  // Ek alanlar (extension members)
  errors: [
    {
      field: 'email',
      message: 'Geçerli bir email adresi giriniz',
      value: 'invalid-email',
    },
    {
      field: 'password',
      message: 'Şifre en az 8 karakter olmalı',
    },
  ],
  timestamp: '2024-01-15T10:30:00Z',
  requestId: '550e8400-e29b-41d4-a716-446655440000',
};

// Express'te RFC 7807 implementasyonu
class ApiError extends Error {
  constructor(status, title, detail, errors = []) {
    super(detail);
    this.status = status;
    this.title = title;
    this.detail = detail;
    this.errors = errors;
  }
}

app.use((err, req, res, next) => {
  const status = err.status || 500;

  res.status(status).json({
    type: `https://api.myapp.com/errors/${err.title?.toLowerCase().replace(/\s+/g, '-') || 'internal-error'}`,
    title: err.title || 'Internal Server Error',
    status,
    detail: err.detail || err.message,
    instance: req.originalUrl,
    errors: err.errors || [],
    timestamp: new Date().toISOString(),
    requestId: req.id,
  });
});
:::

## HATEOAS

:::concept[HATEOAS (İng: Hypermedia As The Engine Of Application State)]
HATEOAS, API yanıtlarına ilişkili kaynakların linklerini ekleyerek client'ın API'yi keşfetmesini sağlayan bir prensiptir.

**Türkçe karşılığı:** Uygulama Durumunun Motoru Olarak Hipermedia
**Ne işe yarar:** Client'ın URL'leri hardcode etmeden, API yanıtındaki linkler üzerinden gezinmesini sağlar
**Gerçek hayat benzetmesi:** Bir web sitesindeki linkler gibi - ana sayfadan linklere tıklayarak tüm siteyi gezebilirsin, URL'leri ezberlemeye gerek yok
:::

:::code[javascript]{title="HATEOAS Örneği"}
// GET /api/v1/users/123 yanıtı
{
  "id": 123,
  "name": "Ali Yılmaz",
  "email": "ali@example.com",
  "_links": {
    "self": { "href": "/api/v1/users/123", "method": "GET" },
    "update": { "href": "/api/v1/users/123", "method": "PUT" },
    "delete": { "href": "/api/v1/users/123", "method": "DELETE" },
    "orders": { "href": "/api/v1/users/123/orders", "method": "GET" },
    "avatar": { "href": "/api/v1/users/123/avatar", "method": "GET" }
  }
}

// GET /api/v1/users?page=2 yanıtı
{
  "data": [...],
  "pagination": { ... },
  "_links": {
    "self": { "href": "/api/v1/users?page=2" },
    "first": { "href": "/api/v1/users?page=1" },
    "prev": { "href": "/api/v1/users?page=1" },
    "next": { "href": "/api/v1/users?page=3" },
    "last": { "href": "/api/v1/users?page=10" }
  }
}
:::

:::tip
HATEOAS, REST'in en az uygulanan ama en güçlü prensibidir. Pratikte çoğu API tam HATEOAS uygulamaz. Ancak en azından pagination linkleri ve ilişkili kaynak linklerini eklemek, API'nin kullanılabilirliğini önemli ölçüde artırır. GitHub API, HATEOAS'ın iyi bir örneğidir.
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: E-Ticaret REST API Tasarimi (Kolay)

Bir e-ticaret uygulamasi icin RESTful URL yapisi tasarla ve endpoint listesi olustur.

```
# GOREV: Asagidaki kaynaklarin CRUD endpoint'lerini tasarla
# Her endpoint icin HTTP metodu, URL ve aciklama yaz

# Urunler
GET    /api/v1/products              # Tum urunleri listele (pagination, filtreleme)
GET    /api/v1/products/:id          # Tek urun detayi
POST   /api/v1/products              # Yeni urun olustur
PUT    /api/v1/products/:id          # Urunu guncelle
DELETE /api/v1/products/:id          # Urunu sil

# TODO: Kategoriler
# GET    /api/v1/categories           # ...
# GET    /api/v1/categories/:id/products  # Bir kategorinin urunleri (alt kaynak)

# TODO: Siparisler
# GET    /api/v1/orders               # Tum siparisler (admin)
# GET    /api/v1/users/:id/orders     # Bir kullanicinin siparisleri (alt kaynak)
# POST   /api/v1/orders               # Yeni siparis
# PATCH  /api/v1/orders/:id/status    # Siparis durumunu guncelle

# TODO: Kullanicilar — en az 5 endpoint tanimla

# Filtreleme ve Pagination ornekleri:
# GET /api/v1/products?category=electronics&minPrice=100&maxPrice=500&sort=-price&page=2&limit=20
```

**Beklenen Sonuc:** En az 20 endpoint tanimlanmis olmali. URL'ler RESTful kurallara uygun olmali (fiil degil isim, cogul isim). Alt kaynaklar dogru modellenemis olmali.
**Ipucu:** PUT tum kaynagi degistirir, PATCH sadece belirtilen alanlari gunceller. Alt kaynaklar icin `/users/:id/orders` seklinde nested URL kullan.

---

### Alistirma 2: Pagination ve Filtreleme Implementasyonu (Orta)

Offset-based ve cursor-based pagination ile filtreleme/siralama ozelligi ekle.

```javascript
// TODO: Pagination middleware
function paginate(defaultLimit = 20) {
  return (req, res, next) => {
    const page = Math.max(1, parseInt(req.query.page) || 1);
    const limit = Math.min(100, Math.max(1, parseInt(req.query.limit) || defaultLimit));
    const offset = (page - 1) * limit;

    req.pagination = { page, limit, offset };
    next();
  };
}

// TODO: GET /api/v1/products ile kullanim
app.get("/api/v1/products", paginate(20), async (req, res) => {
  const { page, limit, offset } = req.pagination;
  const { category, minPrice, maxPrice, sort } = req.query;

  // TODO: Filtreleme uygula
  let filtered = products;
  if (category) filtered = filtered.filter(p => p.category === category);
  if (minPrice) filtered = filtered.filter(p => p.price >= parseFloat(minPrice));
  if (maxPrice) filtered = filtered.filter(p => p.price <= parseFloat(maxPrice));

  // TODO: Siralama uygula (sort=-price -> fiyata gore azalan)

  const total = filtered.length;
  const data = filtered.slice(offset, offset + limit);

  // TODO: Response formatini tamamla
  res.json({
    data,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
      hasNext: page * limit < total,
      hasPrev: page > 1,
    },
    // TODO: HATEOAS linkleri ekle
    links: {
      self: `/api/v1/products?page=${page}&limit=${limit}`,
      // next, prev, first, last
    },
  });
});
```

**Beklenen Sonuc:** `?page=2&limit=10` ile 2. sayfa gorunmeli. Filtreleme ve siralama birlikte calismali. Response'ta pagination metadata ve HATEOAS linkleri olmali.
**Ipucu:** Sort parametresinde `-` prefix'i descending, prefix'siz ascending anlamina gelir: `sort=-price,name`.

---

### Alistirma 3: RFC 7807 Error Response Middleware (Zor)

Standart hata formatinda (RFC 7807 Problem Details) error response middleware'i yaz.

```javascript
// RFC 7807 Problem Details formatı:
// {
//   "type": "https://api.example.com/errors/validation",
//   "title": "Validation Error",
//   "status": 400,
//   "detail": "Name field is required",
//   "instance": "/api/v1/users",
//   "errors": [{ "field": "name", "message": "Required" }]
// }

class ApiError extends Error {
  constructor(status, title, detail, errors = []) {
    super(detail);
    this.status = status;
    this.title = title;
    this.detail = detail;
    this.errors = errors;
  }
}

// TODO: Error factory fonksiyonlari
const errors = {
  validation: (detail, fieldErrors) =>
    new ApiError(400, "Validation Error", detail, fieldErrors),
  notFound: (resource) =>
    new ApiError(404, "Not Found", `${resource} not found`),
  unauthorized: (detail = "Authentication required") =>
    new ApiError(401, "Unauthorized", detail),
  forbidden: (detail = "Insufficient permissions") =>
    new ApiError(403, "Forbidden", detail),
  conflict: (detail) =>
    new ApiError(409, "Conflict", detail),
};

// TODO: Error handling middleware — RFC 7807 formatinda response dondur
function errorHandler(err, req, res, next) {
  const status = err.status || 500;

  res.status(status).json({
    type: `https://api.example.com/errors/${err.title?.toLowerCase().replace(/ /g, "-") || "internal"}`,
    title: err.title || "Internal Server Error",
    status,
    detail: err.detail || err.message,
    instance: req.originalUrl,
    timestamp: new Date().toISOString(),
    ...(err.errors?.length && { errors: err.errors }),
    ...(process.env.NODE_ENV === "development" && { stack: err.stack }),
  });
}

// Kullanim:
app.post("/api/v1/users", (req, res) => {
  if (!req.body.email) {
    throw errors.validation("Invalid input", [
      { field: "email", message: "Email is required" },
    ]);
  }
});
app.use(errorHandler);
```

**Beklenen Sonuc:** Tum hatalar RFC 7807 formatinda donmeli. Status code'a gore farkli error type URL'leri uretilmeli. Development'ta stack trace, production'da gizli olmali. Validation hatalari alan bazli detay icermeli.
**Ipucu:** Content-Type header'ini `application/problem+json` olarak ayarla (RFC 7807 standardi).
:::

:::knowledge-check
type: multiple_choice
question: "Cursor-based pagination'ın offset-based'e göre en büyük avantajı nedir?"
options:
  - "Toplam sayfa sayısını hesaplayabilmesi"
  - "Rastgele bir sayfaya atlayabilmesi"
  - "Büyük veri setlerinde tutarlı performans ve kayma (drift) olmaması"
  - "Daha az kod gerektirmesi"
correct: 2
explanation: "Cursor-based pagination, büyük veri setlerinde bile tutarlı performans sağlar çünkü OFFSET kullanmaz. Ayrıca yeni kayıt eklendiğinde sayfa kayması (drift) sorunu yaşanmaz. Offset-based'de OFFSET 10000 gibi büyük değerlerde veritabanı performansı düşer ve yeni kayıtlar eklenince aynı kayıt iki kez görünebilir."
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdaki URL tasarımlarından hangisi RESTful prensiplere uygundur?"
options:
  - "GET /api/getAllUsers"
  - "POST /api/users/create"
  - "GET /api/v1/users/123/orders"
  - "DELETE /api/deleteUser?id=123"
correct: 2
explanation: "GET /api/v1/users/123/orders RESTful tasarıma uygundur: çoğul isim (users, orders), hiyerarşik ilişki (kullanıcının siparişleri), versiyon prefix'i (v1) ve fiil içermeyen URL. Diğer seçeneklerde URL'de fiil (getAll, create, delete) kullanılmış ki bu anti-pattern'dir - HTTP method zaten eylemi belirtir."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "REST'in stateless prensibini derinlemesine acikla. Neden her istek kendi basina yeterli olmali? Bu prensip horizontal scaling'i nasil kolaylastirir? Session-based authentication stateless prensibini ihlal eder mi? JWT bu sorunu nasil cozer? Idempotency kavramini odeme API'si ornegi ile acikla."

**2. Pratik Uygulama:**
> "Bir e-ticaret API'si icin tam URL yapisi tasarla: urunler, kategoriler, siparisler, kullanicilar ve yorumlar icin CRUD endpoint'leri. Nested resource'lar (kullanicinin siparisleri), cursor-based pagination, filtering (?category=electronics&min_price=100) ve sorting (?sort=-price,name) dahil et. RFC 7807 hata formati ile error response'lari yaz."
> Takip: "Simdi bu API'nin v1 ve v2 versiyonlarini olustur. v2'de bir alan adi degisikligini backward-compatible sekilde nasil yaparsin?"

**3. Mukemmellik Icin:**
> "Stripe API'sinin tasarim kalitesini analiz et: URL yapisi, versioning stratejisi, idempotency key kullanimi, pagination, error format ve rate limiting. Bu tasarim prensiplerini kendi API'me nasil uyarlarim? OpenAPI spec ile contract-first development surecini acikla."

### Pair Programming Ipucu
API tasarlarken AI'a endpoint listeni goster ve sor: "Bu API tasarimimi RESTful prensiplere gore denetle. URL isimlendirme, HTTP method kullanimi, status code secimi ve response formatinda hatalar var mi? Stripe ve GitHub API standartlarina gore iyilestirmeler oner."
:::

:::interview
## Mulakat Sorulari

**Soru 1: RESTful API tasarlarken en onemli prensipler nelerdir?**
- **Junior cevabi:** Dogru HTTP method'lari kullanmak, JSON dondurmek ve anlamli URL'ler olusturmak.
- **Senior cevabi:** REST'in temel prensipleri: 1) Statelessness: her istek kendi basina yeterli olmali, sunucu session tutmamali. 2) Resource-based URL'ler: fiiller degil isimler (`/users/123` not `/getUser`), cogul isimler, nested resource'lar max 2 seviye. 3) HTTP method semantics: GET idempotent ve cacheable, POST yaratir, PUT tamamen degistirir (idempotent), PATCH kismen degistirir, DELETE siler. 4) HATEOAS: response'da iliskili resource link'leri sunulur. 5) Versioning: URL (`/v1/`) veya header (Accept) ile. 6) Pagination: cursor-based (buyuk veri) veya offset (kucuk veri). Stripe ve GitHub API'lari industry standard olarak incelenmeli.

**Soru 2: REST API'de hata dondurme best practice'leri nelerdir?**
- **Junior cevabi:** Hata oldugunda uygun status code ile hata mesaji donerim.
- **Senior cevabi:** Tutarli error response formati: `{ error: { code: "VALIDATION_ERROR", message: "...", details: [...] } }`. Status code'lar: 400 (bad input), 401 (not authenticated), 403 (not authorized), 404 (not found), 409 (conflict), 422 (unprocessable), 429 (rate limit), 500 (server error). Detayli hata mesajlari development'ta, generic mesajlar production'da donmeli. Validation error'larda hangi field'in neden gecersiz oldugu belirtilmeli. Stack trace asla client'a gonderilmemeli. Error code'lar (string) status code'lardan daha spesifik olabilir.
:::

:::must-note
- REST 6 prensibi: Client-Server, Stateless, Cacheable, Uniform Interface, Layered System, Code on Demand (opsiyonel)
- URL kuralları: çoğul isim kullan (users), fiil kullanma (GET zaten okuma demek), küçük harf, tire ile ayır
- HTTP Methods: GET=oku, POST=oluştur, PUT=tamamen güncelle, PATCH=kısmen güncelle, DELETE=sil
- Idempotent: GET, PUT, DELETE (aynı isteği tekrarlasan aynı sonuç). POST idempotent DEĞİL
- Safe: GET, HEAD, OPTIONS (sunucu state'ini değiştirmez)
- Status code kuralları: 2xx=başarı, 4xx=client hatası, 5xx=server hatası. Her hatada 200 dönme!
- 200=OK, 201=Created, 204=No Content, 400=Bad Request, 401=Unauthorized, 403=Forbidden, 404=Not Found, 409=Conflict, 429=Too Many Requests
- API versioning: URL versioning (/api/v1/) en yaygın ve tavsiye edilen yöntem
- Offset-based pagination: basit, toplam sayfa hesaplanabilir ama büyük offset'lerde yavaş
- Cursor-based pagination: tutarlı performans, drift yok ama rastgele sayfa atlama yok
- RFC 7807: type, title, status, detail, instance alanlarıyla standart hata formatı
- HATEOAS: yanıta _links ekleyerek client'ın API'yi keşfetmesini sağla
- Idempotency key ile POST'u güvenli tekrarlanabilir yap (ödeme API'lerinde kritik)
:::

:::senior-learns
Bir Senior Developer veya CTO, REST API tasarımını öğrenirken şu yaklaşımı benimser:

1. **API-First Design uygular** - Kod yazmadan önce API contract'ını OpenAPI (Swagger) spec ile tanımlar. Frontend ve backend ekipleri bu contract üzerinde anlaşır. Contract değişiklikleri versiyon kontrollü yapılır. Mock server ile frontend geliştirmesi API hazır olmadan başlar.
2. **Richardson Maturity Model'i bilir** - Level 0 (tek URL, tek method), Level 1 (resource'lar), Level 2 (HTTP methods), Level 3 (HATEOAS). Çoğu API Level 2'dedir. Level 3 tam REST'tir ama pratikte nadiren uygulanır. Hangi seviyede olduğunu bilmek, bilinçli tasarım kararları vermeni sağlar.
3. **API Gateway pattern uygular** - Rate limiting, authentication, request transformation, caching, logging gibi cross-cutting concern'leri API Gateway'de merkezi olarak yönetir. Kong, AWS API Gateway veya custom gateway kullanır.
4. **Backward compatibility ve deprecation stratejisi belirler** - Breaking change'leri yeni versiyon ile sunar. Eski versiyonlara sunset header'ı ekler. Deprecation timeline ve migration guide yayınlar. Semantic versioning ile API contract değişikliklerini yönetir.
5. **Pagination, filtering ve sorting'i tutarlı standartlarla yapar** - Tüm list endpoint'leri aynı pagination formatını kullanır. Filter syntax'ı tutarlıdır (OData veya custom). Sort parametresi standart bir formattadır (`?sort=-createdAt,name`). Partial response desteği (`?fields=id,name,email`) ile payload boyutunu azaltır.
6. **API metrics ve SLA tanımlar** - Response time (p50, p95, p99), availability (99.9%), error rate gibi metrikleri ölçer. Rate limit'leri tier-based yapar (free: 100/saat, premium: 10000/saat). API kullanım analitikleri ile en çok kullanılan endpoint'leri ve hata oranlarını izler.

**Profesyonel Mindset:** "API tasarımı, bir kez yayınladığında geri almak çok zor olan bir karardır. URL yapısını, response formatını, hata kodlarını ilk seferde doğru yapmak, ileride binlerce geliştirici-saatlik migration çalışmasını önler. 'Bunu sonra düzeltiriz' demek yerine, 'Bu API'yi 5 yıl boyunca destekleyebilir miyiz?' sorusunu sor."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Endpoint** (ɛnd-pɔɪnt) → Uç nokta
   *"The /api/v1/users endpoint returns a paginated list of users."*

2. **Idempotent** (aɪ-dem-poʊ-tənt) → Etkisiz / Tekrarlanabilir
   *"PUT requests are idempotent, meaning multiple identical requests produce the same result."*

3. **Pagination** (pædʒ-ɪ-neɪ-ʃən) → Sayfalama
   *"Cursor-based pagination provides consistent performance regardless of dataset size."*

4. **Versioning** (vɜːr-ʒən-ɪŋ) → Sürümleme
   *"API versioning through URL prefixes is the most common approach."*

5. **Deprecation** (dep-rɪ-keɪ-ʃən) → Kullanımdan kaldırma
   *"The v1 API will be deprecated on March 2025; please migrate to v2."*

**Okuma Egzersizi:** GitHub API dokümantasyonunu incele: https://docs.github.com/en/rest

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "REST API tasarımı ve pagination implementasyonu eklendi"
→ Örnek: `feat: implement REST API design with cursor-based pagination`
:::

:::external-resource
- 📖 **Microsoft REST API Guidelines:** github.com/microsoft/api-guidelines (ücretsiz)
- 📖 **Google API Design Guide:** cloud.google.com/apis/design (ücretsiz)
- 📖 **RFC 7807:** tools.ietf.org/html/rfc7807 (Problem Details standardı)
- 📺 **Traversy Media:** "REST API Design Best Practices" (YouTube, ücretsiz)
- 📖 **Stripe API Docs:** stripe.com/docs/api (mükemmel API tasarım örneği)
:::
