---
title: "Authentication & Authorization: Güvenli Kimlik Doğrulama"
id: "mod-12-auth/lesson-01"
estimated_minutes: 55
order: 1
tags: ["authentication", "authorization", "jwt", "oauth", "bcrypt", "rbac", "security"]
prerequisites: ["mod-11-db/lesson-01"]
---

# Authentication & Authorization: Güvenli Kimlik Doğrulama

:::realworld
Bir kullanıcı Instagram'a giriş yaptığında, arka planda düzinelerce güvenlik katmanı devreye girer: şifre hash'lenir, JWT token oluşturulur, her API isteğinde token doğrulanır, yetkilendirme kontrol edilir. Bir güvenlik açığı milyonlarca kullanıcının verilerini tehlikeye atar. 2024'te gerçekleşen büyük veri sızıntılarının %80'i zayıf authentication implementasyonlarından kaynaklandı. Bu derste, production-grade güvenlik sistemini sıfırdan kurabilecek bilgiyi kazanacaksın.
:::

## Neden Authentication Öğreniyorsun?

Her web uygulamasının olmazsa olmaz bileşeni güvenliktir. Authentication (kimlik doğrulama) ve authorization (yetkilendirme) bilmeden:

- Kullanıcı verilerini koruyamazsın
- KVKK/GDPR uyumluluğunu sağlayamazsın
- Güvenlik açığı olan kod yazarsın
- Mülakatlarda başarısız olursun (güvenlik soruları zorunlu)

:::deha-tip
Deha seviyesi geliştiriciler güvenliği "sonradan eklenecek özellik" olarak değil, "mimari kararın parçası" olarak görür. Her endpoint tasarlanırken "bu veriye kim erişebilmeli?" sorusu sorulur. Security-by-design prensibi ile kod yazılır.
:::

## Authentication vs Authorization

:::concept[Authentication (İng: Authentication)]
Authentication, kullanıcının kim olduğunu doğrulama sürecidir. "Sen kimsin?" sorusuna cevap verir.

**Türkçe karşılığı:** Kimlik Doğrulama
**Ne işe yarar:** Kullanıcının iddia ettiği kişi olup olmadığını doğrular
**Gerçek hayat benzetmesi:** Bina girişinde kimlik kartı göstermek - "Sen gerçekten bu binada çalışan Ahmet misin?"
:::

:::concept[Authorization (İng: Authorization)]
Authorization, doğrulanmış kullanıcının hangi kaynaklara erişim hakkına sahip olduğunu belirleme sürecidir. "Ne yapabilirsin?" sorusuna cevap verir.

**Türkçe karşılığı:** Yetkilendirme
**Ne işe yarar:** Kullanıcının hangi işlemleri yapabileceğini kontrol eder
**Gerçek hayat benzetmesi:** Bina içinde hangi katlara erişebildiğin - kimlik kartın seni tanıtır ama her kata girmene izin vermez
:::

:::comparison
| Özellik | Authentication (AuthN) | Authorization (AuthZ) |
|---------|----------------------|---------------------|
| Soru | "Kim?" | "Ne yapabilir?" |
| Zaman | Login sırasında | Her istek sırasında |
| Yöntem | Şifre, token, biometrik | Roller, izinler, politikalar |
| Başarısızlık | 401 Unauthorized | 403 Forbidden |
| **Örnek** | Email + şifre ile giriş | Admin paneline erişim kontrolü |

**Tavsiye:** İkisini karıştırma! 401 = "Kim olduğunu bilmiyorum", 403 = "Kim olduğunu biliyorum ama buna yetkin yok."
:::

## Password Hashing: Şifreleri Güvenle Sakla

:::concept[Password Hashing (İng: Password Hashing)]
Password hashing, kullanıcı şifresini tek yönlü bir fonksiyonla matematiksel olarak dönüştürerek saklamaktır. Hash'ten orijinal şifre geri elde edilemez.

**Türkçe karşılığı:** Şifre Özetleme / Hash'leme
**Ne işe yarar:** Veritabanı sızıntısında bile şifrelerin güvende kalmasını sağlar
**Gerçek hayat benzetmesi:** Kağıt öğütücü gibi - belgeyi parçalara ayırır ama parçalardan belgeyi geri oluşturamazsın
:::

:::code[javascript]{title="bcrypt ile Password Hashing (Node.js)"}
const bcrypt = require('bcrypt');

// Kayıt sırasında: Şifreyi hash'le
async function registerUser(email, password) {
  // Salt rounds: 12 önerilir (10-14 arası)
  // Her artış hesaplama süresini 2x yapar
  const saltRounds = 12;
  const hashedPassword = await bcrypt.hash(password, saltRounds);

  // Veritabanına hash'lenmiş şifreyi kaydet
  await db.query(
    'INSERT INTO users (email, password_hash) VALUES ($1, $2)',
    [email, hashedPassword]
  );
  // hashedPassword: $2b$12$LJ3m6Gq... (60 karakter)
}

// Giriş sırasında: Şifreyi doğrula
async function loginUser(email, password) {
  const user = await db.query(
    'SELECT * FROM users WHERE email = $1',
    [email]
  );

  if (!user) {
    throw new Error('Kullanıcı bulunamadı');
  }

  // bcrypt.compare hash'i çözmez, girilen şifreyi aynı salt ile
  // hash'leyip karşılaştırır
  const isValid = await bcrypt.compare(password, user.password_hash);

  if (!isValid) {
    throw new Error('Geçersiz şifre');
  }

  return user;
}
:::

:::code[python]{title="Argon2 ile Password Hashing (Python)"}
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=3,      # İterasyon sayısı
    memory_cost=65536, # 64MB bellek kullanımı
    parallelism=4      # Paralel thread sayısı
)

# Hash'le
hashed = ph.hash("kullanici_sifresi")
# $argon2id$v=19$m=65536,t=3,p=4$...

# Doğrula
try:
    ph.verify(hashed, "kullanici_sifresi")  # True
except Exception:
    print("Geçersiz şifre")

# Rehash gerekli mi kontrol et (parametreler değiştiyse)
if ph.check_needs_rehash(hashed):
    new_hash = ph.hash("kullanici_sifresi")
:::

:::comparison
| Özellik | bcrypt | Argon2 | SHA-256 | MD5 |
|---------|--------|--------|---------|-----|
| Güvenlik | Yüksek | En yüksek | Düşük (şifre için) | Çok düşük |
| Salt | Otomatik | Otomatik | Manuel | Manuel |
| GPU direnci | Orta | Çok yüksek | Yok | Yok |
| Bellek kullanımı | Düşük | Yüksek (ayarlanabilir) | Düşük | Düşük |
| **Şifre için kullan** | Evet | Evet (önerilen) | Hayır | Asla |

**Tavsiye:** Yeni projeler için Argon2id kullan. bcrypt de hala güvenlidir. SHA-256 ve MD5'i şifre hash'leme için asla kullanma.
:::

:::beginner-mistake
Yaygın hata: Şifreleri plain text veya MD5/SHA-256 ile saklamak. Veritabanı sızıntısında tüm şifreler ifşa olur. MUTLAKA bcrypt veya Argon2 kullan. Ayrıca kendi hash fonksiyonunu yazmaya çalışma - kriptografi uzmanlarının yazdığı kütüphaneleri kullan.
:::

## JWT (JSON Web Token)

:::concept[JWT (JSON Web Token)]
JWT, iki taraf arasında güvenli bilgi aktarımı için kullanılan, imzalanmış ve self-contained bir token formatıdır.

**Türkçe karşılığı:** JSON Web Token / JSON Web Jetonu
**Ne işe yarar:** Stateless authentication sağlar - sunucu session saklamak zorunda kalmaz
**Gerçek hayat benzetmesi:** Konser bileti gibi - biletin üzerinde adın, koltuğun ve etkinlik bilgisi yazılı. Kapıdaki görevli bileti okuyarak seni tanır, her seferinde organizatörü aramak zorunda kalmaz
:::

### JWT Yapısı

:::code[text]{title="JWT Token Yapısı (3 Parça)"}
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.     ← HEADER (Base64)
eyJ1c2VySWQiOjEsInJvbGUiOiJhZG1pbiJ9.     ← PAYLOAD (Base64)
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c  ← SIGNATURE

HEADER (Algoritma ve tip):
{
  "alg": "HS256",    // İmza algoritması
  "typ": "JWT"       // Token tipi
}

PAYLOAD (Veri / Claims):
{
  "userId": 1,
  "role": "admin",
  "email": "ahmet@example.com",
  "iat": 1700000000,  // Issued At (oluşturulma zamanı)
  "exp": 1700003600   // Expiration (son kullanma: 1 saat sonra)
}

SIGNATURE (İmza):
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
:::

### Access Token ve Refresh Token

:::code[javascript]{title="JWT Access + Refresh Token Implementasyonu"}
const jwt = require('jsonwebtoken');

const ACCESS_SECRET = process.env.JWT_ACCESS_SECRET;
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET;

// Token oluşturma
function generateTokens(user) {
  // Access Token: Kısa ömürlü (15 dakika)
  const accessToken = jwt.sign(
    { userId: user.id, role: user.role },
    ACCESS_SECRET,
    { expiresIn: '15m' }
  );

  // Refresh Token: Uzun ömürlü (7 gün)
  const refreshToken = jwt.sign(
    { userId: user.id, tokenVersion: user.tokenVersion },
    REFRESH_SECRET,
    { expiresIn: '7d' }
  );

  return { accessToken, refreshToken };
}

// Login endpoint
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await findUserByEmail(email);
  if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
    return res.status(401).json({ error: 'Geçersiz email veya şifre' });
  }

  const { accessToken, refreshToken } = generateTokens(user);

  // Refresh token'ı httpOnly cookie'de sakla
  res.cookie('refreshToken', refreshToken, {
    httpOnly: true,     // JavaScript erişemez (XSS koruması)
    secure: true,       // Sadece HTTPS
    sameSite: 'strict', // CSRF koruması
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7 gün
    path: '/api/auth/refresh' // Sadece refresh endpoint'ine gönderilir
  });

  res.json({ accessToken });
});

// Token yenileme endpoint
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.cookies;

  if (!refreshToken) {
    return res.status(401).json({ error: 'Refresh token bulunamadı' });
  }

  try {
    const decoded = jwt.verify(refreshToken, REFRESH_SECRET);
    const user = await findUserById(decoded.userId);

    // Token version kontrolü (logout sonrası geçersizleştirme)
    if (user.tokenVersion !== decoded.tokenVersion) {
      return res.status(401).json({ error: 'Token geçersiz' });
    }

    const tokens = generateTokens(user);

    res.cookie('refreshToken', tokens.refreshToken, {
      httpOnly: true, secure: true, sameSite: 'strict',
      maxAge: 7 * 24 * 60 * 60 * 1000,
      path: '/api/auth/refresh'
    });

    res.json({ accessToken: tokens.accessToken });
  } catch (error) {
    return res.status(401).json({ error: 'Geçersiz refresh token' });
  }
});

// Middleware: Token doğrulama
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Token gerekli' });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, ACCESS_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token süresi dolmuş', code: 'TOKEN_EXPIRED' });
    }
    return res.status(401).json({ error: 'Geçersiz token' });
  }
}

// Korumalı endpoint
app.get('/api/profile', authenticate, async (req, res) => {
  const user = await findUserById(req.user.userId);
  res.json(user);
});
:::

### JWT Best Practices ve Güvenli Saklama

:::code[text]{title="JWT Güvenlik Kuralları"}
1. ACCESS TOKEN SAKLAMA:
   ✓ Bellekte (JavaScript değişkeni / React state) → En güvenli
   ✗ localStorage → XSS saldırısına açık
   ✗ sessionStorage → XSS saldırısına açık
   △ httpOnly cookie → CSRF riski var ama XSS'e karşı güvenli

2. REFRESH TOKEN SAKLAMA:
   ✓ httpOnly + secure + sameSite cookie → En güvenli
   ✗ localStorage → Asla!
   ✗ JavaScript'ten erişilebilir yer → Asla!

3. TOKEN SÜRELERİ:
   Access Token: 15 dakika (kısa!)
   Refresh Token: 7-30 gün
   Neden kısa? → Token çalınsa bile 15 dakika sonra geçersiz olur.

4. PAYLOAD'DA SAKLAMA:
   ✓ userId, role, permissions
   ✗ Şifre, kredi kartı, kişisel veri
   Not: JWT payload Base64 ile encode edilir, şifrelenmez!
       Herkes decode edip okuyabilir. Hassas veri koyma!

5. GEÇERSİZLEŞTİRME (INVALIDATION):
   - Refresh token rotation: Her kullanımda yeni token ver, eskiyi geçersiz kıl
   - Token version: Kullanıcı tablosunda versiyon tut, logout'ta artır
   - Token blacklist: Redis'te geçersiz token'ları tut (kısa TTL)
:::

:::tip
Access token'ı localStorage'a koyma! XSS açığıyla çalınabilir. En güvenli yol: access token bellekte, refresh token httpOnly cookie'de. Sayfa yenilendiğinde refresh endpoint'i ile yeni access token al.
:::

## OAuth 2.0 ve OpenID Connect

:::concept[OAuth 2.0 (İng: OAuth 2.0)]
OAuth 2.0, üçüncü parti uygulamaların kullanıcı adına sınırlı kaynaklara erişmesini sağlayan yetkilendirme framework'üdür.

**Türkçe karşılığı:** Açık Yetkilendirme 2.0
**Ne işe yarar:** "Google ile giriş yap" gibi üçüncü parti kimlik doğrulama
**Gerçek hayat benzetmesi:** Otel vale hizmeti gibi - arabanın anahtarını vale'ye verirsin ama vale sadece arabayı park edebilir, bagajı açamaz. Sınırlı erişim yetkisi
:::

:::code[text]{title="OAuth 2.0 Authorization Code Flow"}
1. Kullanıcı "Google ile Giriş Yap" butonuna tıklar
        ↓
2. Uygulama, kullanıcıyı Google'a yönlendirir:
   https://accounts.google.com/o/oauth2/auth?
     client_id=YOUR_CLIENT_ID
     &redirect_uri=https://yourapp.com/callback
     &response_type=code
     &scope=openid email profile
     &state=random_csrf_token
        ↓
3. Kullanıcı Google'da oturum açar ve izin verir
        ↓
4. Google, kullanıcıyı geri yönlendirir:
   https://yourapp.com/callback?code=AUTHORIZATION_CODE&state=random_csrf_token
        ↓
5. Backend, code'u Google'a gönderip token alır:
   POST https://oauth2.googleapis.com/token
   { code, client_id, client_secret, redirect_uri, grant_type }
        ↓
6. Google access_token ve id_token döndürür
        ↓
7. Backend, id_token'dan kullanıcı bilgilerini alır
   veya /userinfo endpoint'ini çağırır
        ↓
8. Kullanıcıyı oluştur/güncelle, JWT token ver
:::

:::code[javascript]{title="Google OAuth 2.0 (Passport.js)"}
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL: '/api/auth/google/callback'
}, async (accessToken, refreshToken, profile, done) => {
  try {
    // Kullanıcıyı bul veya oluştur
    let user = await findUserByGoogleId(profile.id);

    if (!user) {
      user = await createUser({
        googleId: profile.id,
        email: profile.emails[0].value,
        name: profile.displayName,
        avatar: profile.photos[0]?.value
      });
    }

    done(null, user);
  } catch (error) {
    done(error, null);
  }
}));

// Routes
app.get('/api/auth/google',
  passport.authenticate('google', { scope: ['openid', 'email', 'profile'] })
);

app.get('/api/auth/google/callback',
  passport.authenticate('google', { session: false }),
  (req, res) => {
    const { accessToken, refreshToken } = generateTokens(req.user);

    res.cookie('refreshToken', refreshToken, {
      httpOnly: true, secure: true, sameSite: 'lax',
      maxAge: 7 * 24 * 60 * 60 * 1000
    });

    // Frontend'e yönlendir
    res.redirect(`${FRONTEND_URL}/auth/success?token=${accessToken}`);
  }
);
:::

## Session-Based vs Token-Based Authentication

:::comparison
| Özellik | Session-Based | Token-Based (JWT) |
|---------|-------------|-------------------|
| Durum | Stateful (sunucu saklar) | Stateless (token'da saklanır) |
| Saklama | Sunucu belleği / Redis | Client (cookie/memory) |
| Ölçekleme | Paylaşımlı session store gerekir | Kolay (sunucu bağımsız) |
| Güvenlik | Session hijacking riski | Token çalınma riski |
| Geçersizleştirme | Sunucudan anında silinebilir | Expire olana kadar geçerli (blacklist ile çözülebilir) |
| Mobil uyum | Zor (cookie desteği sınırlı) | Kolay (header'da gönderilir) |
| **Ne zaman kullan** | Server-rendered uygulamalar, basit web | SPA, mobil, microservice |

**Tavsiye:** Modern uygulamalar için JWT + refresh token pattern kullan. Server-rendered MPA'lar için session-based da uygun.
:::

## RBAC (Role-Based Access Control)

:::concept[RBAC (Role-Based Access Control)]
RBAC, kullanıcılara roller atayarak ve bu rollere izinler tanımlayarak erişim kontrolü sağlayan modeldir.

**Türkçe karşılığı:** Rol Tabanlı Erişim Kontrolü
**Ne işe yarar:** Kullanıcıların sadece yetkili oldukları işlemleri yapmasını sağlar
**Gerçek hayat benzetmesi:** Bir şirketteki organizasyon şeması - stajyer sadece görevlerini yapar, müdür departmanı yönetir, CEO her şeye erişir
:::

:::code[javascript]{title="RBAC Implementasyonu"}
// Roller ve izinler tanımla
const ROLES = {
  ADMIN: 'admin',
  MODERATOR: 'moderator',
  USER: 'user',
  GUEST: 'guest'
};

const PERMISSIONS = {
  // Kaynak: [izin verilen roller]
  'users:read':    [ROLES.ADMIN, ROLES.MODERATOR, ROLES.USER],
  'users:write':   [ROLES.ADMIN],
  'users:delete':  [ROLES.ADMIN],
  'posts:read':    [ROLES.ADMIN, ROLES.MODERATOR, ROLES.USER, ROLES.GUEST],
  'posts:write':   [ROLES.ADMIN, ROLES.MODERATOR, ROLES.USER],
  'posts:delete':  [ROLES.ADMIN, ROLES.MODERATOR],
  'admin:access':  [ROLES.ADMIN],
  'reports:read':  [ROLES.ADMIN, ROLES.MODERATOR]
};

// Authorization middleware
function authorize(...requiredPermissions) {
  return (req, res, next) => {
    const userRole = req.user?.role;

    if (!userRole) {
      return res.status(401).json({ error: 'Kimlik doğrulama gerekli' });
    }

    const hasPermission = requiredPermissions.every(permission => {
      const allowedRoles = PERMISSIONS[permission];
      return allowedRoles?.includes(userRole);
    });

    if (!hasPermission) {
      return res.status(403).json({
        error: 'Bu işlem için yetkiniz bulunmamaktadır'
      });
    }

    next();
  };
}

// Kullanım
app.get('/api/users', authenticate, authorize('users:read'), getUsers);
app.delete('/api/users/:id', authenticate, authorize('users:delete'), deleteUser);
app.get('/api/admin/dashboard', authenticate, authorize('admin:access'), adminDashboard);

// Kaynak sahipliği kontrolü (kendi verisini düzenleme)
function authorizeOwnerOrAdmin(resourceField = 'userId') {
  return (req, res, next) => {
    const resourceOwnerId = req.params[resourceField] || req.body[resourceField];

    if (req.user.role === ROLES.ADMIN || req.user.userId === parseInt(resourceOwnerId)) {
      return next();
    }

    return res.status(403).json({ error: 'Bu kaynağa erişim yetkiniz yok' });
  };
}

// Kullanıcı kendi profilini veya admin herkesin profilini görebilir
app.get('/api/users/:userId/profile',
  authenticate,
  authorizeOwnerOrAdmin('userId'),
  getUserProfile
);
:::

:::interview
**Mülakat Sorusu:** "JWT token'ı nasıl güvenli saklarsın ve geçersizleştirirsin?"

**Beklenen cevap:**
Saklama: Access token bellekte (React state/context), refresh token httpOnly + secure + sameSite cookie'de. localStorage'a koymam, XSS riski var.

Geçersizleştirme stratejileri:
1. Token rotation: Her refresh'te yeni refresh token ver, eskiyi geçersiz kıl
2. Token version: User tablosunda tokenVersion tut, logout'ta artır
3. Redis blacklist: Geçersiz access token'ları Redis'te tut, TTL = token'ın kalan ömrü
4. Short-lived access: 15 dakika gibi kısa ömür, doğal geçersizleşme
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: JWT Authentication API (Kolay)

Express.js ile register ve login endpoint'leri yaz. bcrypt ile sifre hash'le, JWT ile token uret.

```javascript
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

const JWT_SECRET = process.env.JWT_SECRET || "super-secret-key";
const users = []; // In-memory (gercek projede DB)

// TODO: POST /register
app.post("/api/auth/register", async (req, res) => {
  const { name, email, password } = req.body;

  // TODO: Email benzersizlik kontrolu
  // TODO: Sifreyi bcrypt ile hash'le (salt rounds: 12)
  const hashedPassword = await bcrypt.hash(password, 12);

  // TODO: Kullaniciyi kaydet
  // TODO: JWT token uret ve dondur (expiresIn: "15m")
  const token = jwt.sign({ userId: user.id, email }, JWT_SECRET, { expiresIn: "15m" });

  res.status(201).json({ token, user: { id: user.id, name, email } });
});

// TODO: POST /login
app.post("/api/auth/login", async (req, res) => {
  const { email, password } = req.body;

  // TODO: Kullaniciyi bul
  // TODO: Sifreyi bcrypt.compare ile dogrula
  // TODO: Access token (15m) + Refresh token (7d) uret
  // TODO: Refresh token'i httpOnly cookie ile gonder
});

// TODO: Auth middleware yaz
function authenticate(req, res, next) {
  // TODO: Authorization header'dan Bearer token'i al
  // TODO: jwt.verify ile dogrula
  // TODO: Basarili ise req.user'a payload'i ata ve next() cagir
  // TODO: Basarisiz ise 401 dondur
}

// Korunmali endpoint
app.get("/api/profile", authenticate, (req, res) => {
  res.json({ user: req.user });
});
```

**Beklenen Sonuc:** Register ile yeni kullanici olusturulabilmeli. Login ile token alinabilmeli. Token olmadan /profile'a erisilemememeli (401). Token ile erisim saglanmali.
**Ipucu:** `bcrypt.hash(password, 12)` salt rounds ne kadar yuksekse o kadar guvenli ama yavas. 12 iyi bir denge.

---

### Alistirma 2: Refresh Token ve RBAC (Orta)

Refresh token rotation ve rol tabanli erisim kontrolu (RBAC) implement et.

```javascript
// Refresh token storage (gercek projede Redis veya DB)
const refreshTokens = new Map();

// TODO: POST /refresh — Token yenileme
app.post("/api/auth/refresh", (req, res) => {
  const { refreshToken } = req.cookies; // httpOnly cookie'den

  // TODO: Refresh token gecerli mi kontrol et
  // TODO: Token rotation: eski token'i sil, yenisini olustur
  // TODO: Yeni access + refresh token dondur
});

// TODO: POST /logout — Refresh token gecersizlestirme
app.post("/api/auth/logout", authenticate, (req, res) => {
  // TODO: Kullanicinin refresh token'ini sil
  // TODO: Cookie'yi temizle
  res.json({ message: "Logged out" });
});

// TODO: RBAC middleware
function authorize(...roles) {
  return (req, res, next) => {
    // TODO: req.user.role, izin verilen roller arasinda mi kontrol et
    // TODO: Degilse 403 Forbidden dondur
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: "Insufficient permissions" });
    }
    next();
  };
}

// Kullanim:
app.get("/api/admin/users", authenticate, authorize("admin"), (req, res) => {
  res.json({ users });
});

app.delete("/api/posts/:id", authenticate, authorize("admin", "moderator"), (req, res) => {
  // Admin ve moderator silebilir, normal user silemez
});
```

**Beklenen Sonuc:** Refresh token ile access token yenilenebilmeli. Eski refresh token gecersiz olmali (rotation). Admin endpoint'ine normal user erisememeli (403). Logout sonrasi token'lar gecersiz olmali.
**Ipucu:** Token rotation'da eski token'i hemen sil. Eger biri eski token'i kullanirsa, muhtemelen calinan bir token'dir — tum token'lari gecersiz kil.

---

### Alistirma 3: Guvenlik En Iyi Uygulamalari (Zor)

Helmet, rate limiting, input sanitization ve guvenli cookie ayarlari ile API'yi guclendir.

```javascript
const helmet = require("helmet");
const rateLimit = require("express-rate-limit");
const mongoSanitize = require("express-mongo-sanitize");

// TODO: Helmet — guvenlik header'lari
app.use(helmet());

// TODO: Login rate limiting (5 deneme / 15 dakika)
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: { error: "Too many login attempts, try again after 15 minutes" },
  skipSuccessfulRequests: true,
});

// TODO: MongoDB injection korunmasi
app.use(mongoSanitize());

// TODO: Guvenli cookie ayarlari
const cookieOptions = {
  httpOnly: true,     // JavaScript ile erisilemez (XSS korunmasi)
  secure: process.env.NODE_ENV === "production",  // Sadece HTTPS
  sameSite: "strict", // CSRF korunmasi
  maxAge: 7 * 24 * 60 * 60 * 1000, // 7 gun
};

// TODO: Account lockout — 5 basarisiz denemeden sonra hesabi kilitle
const loginAttempts = new Map(); // userId -> { count, lockedUntil }

async function loginWithLockout(email, password) {
  const user = await User.findOne({ email });
  if (!user) throw new Error("Invalid credentials");

  // TODO: Hesap kilitli mi kontrol et
  const attempts = loginAttempts.get(user.id) || { count: 0, lockedUntil: null };
  if (attempts.lockedUntil && attempts.lockedUntil > Date.now()) {
    throw new Error(`Account locked. Try again after ${new Date(attempts.lockedUntil)}`);
  }

  const isValid = await bcrypt.compare(password, user.password);
  if (!isValid) {
    // TODO: Basarisiz deneme sayisini artir
    // TODO: 5'e ulasirsa 15 dakika kilitle
    throw new Error("Invalid credentials");
  }

  // TODO: Basarili login — deneme sayisini sifirla
  loginAttempts.delete(user.id);
  return user;
}
```

**Beklenen Sonuc:** Helmet guvenlik header'larini eklemeli. 5 basarisiz login'den sonra hesap 15 dakika kilitlenmeli. NoSQL injection saldirisi engellenebilmeli. Cookie'ler httpOnly ve secure olmali.
**Ipucu:** Helmet otomatik olarak X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security gibi header'lari ekler.
:::

:::knowledge-check
type: multiple_choice
question: "JWT access token'ı nerede saklamak en güvenlidir?"
options:
  - "localStorage"
  - "sessionStorage"
  - "Bellekte (JavaScript değişkeni / React state)"
  - "URL parametresinde"
correct: 2
explanation: "Bellekte (JavaScript değişkeni/React state) saklamak en güvenlidir çünkü XSS saldırısıyla doğrudan çalınamaz. localStorage ve sessionStorage XSS'e açıktır. URL parametresi ise server log'larında ve tarayıcı geçmişinde görünür."
:::

:::knowledge-check
type: multiple_choice
question: "HTTP 401 ve 403 status kodları arasındaki fark nedir?"
options:
  - "İkisi de aynı anlama gelir"
  - "401 = Kimlik doğrulanmamış (kim olduğun belli değil), 403 = Yetkisiz (kim olduğun belli ama yetkin yok)"
  - "401 = Sunucu hatası, 403 = İstemci hatası"
  - "401 = Yetki yok, 403 = Kimlik doğrulanmamış"
correct: 1
explanation: "401 Unauthorized: Kullanıcının kimliği doğrulanmamış (token yok veya geçersiz). 403 Forbidden: Kullanıcının kimliği doğrulanmış ama bu kaynağa erişim yetkisi yok (ör: normal kullanıcı admin paneline erişmeye çalışıyor)."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "JWT token'in Header.Payload.Signature yapisini adim adim acikla. Payload neden sifrelenmemis (sadece Base64)? HMAC-SHA256 ile RSA-SHA256 arasindaki fark nedir? Access token bellekte, refresh token httpOnly cookie'de saklamanin guvenlik gerekceleri neler? XSS ve CSRF saldirilarinda her yaklasimin riski ne?"

**2. Pratik Uygulama:**
> "Express.js ile tam bir authentication sistemi kur: bcrypt ile kayit, JWT access + refresh token ile giris, refresh token rotation, RBAC (admin/moderator/user) middleware, Google OAuth 2.0 (Passport.js). Rate limiting ile brute force korumasini ekle. Her adimdaki guvenlik kararlarini acikla."
> Takip: "Simdi bu sisteme 'kullanici kendi profilini gorebilir ama baskasininki icin admin olmali' seklinde resource ownership kontrolu ekle."

**3. Mukemmellik Icin:**
> "Bir microservice mimarisinde authentication nasil merkezi yonetilir? Auth service'i ayir, JWT'yi servisler arasi nasil dogrula, mTLS ile service-to-service authentication, API Gateway'de token validation ve Zero Trust architecture prensiplerini acikla. Token rotation, key management (Vault) ve audit logging stratejilerini dahil et."

### Pair Programming Ipucu
Authentication kodunu yazarken AI'a JWT token'ini jwt.io'da decode ederek goster ve sor: "Bu token'in payload'inda hassas veri var mi? Token suresi uygun mu? Refresh token rotation dogru calisiyor mu? OWASP Authentication Cheat Sheet'e gore eksiklerim ne?"
:::

:::must-note
- Authentication = "Sen kimsin?" (401), Authorization = "Ne yapabilirsin?" (403)
- Şifre hash'leme: bcrypt (saltRounds: 12) veya Argon2id kullan. MD5/SHA-256 şifre için ASLA kullanma
- JWT yapısı: Header.Payload.Signature (Base64 encode, şifrelenmemiş! Hassas veri koyma)
- Token süreleri: Access = 15 dakika, Refresh = 7-30 gün. Kısa access = çalınsa bile kısa süre geçerli
- Token saklama: Access → bellekte (state), Refresh → httpOnly + secure + sameSite cookie
- Token geçersizleştirme: token rotation, tokenVersion (DB), Redis blacklist
- OAuth 2.0 Authorization Code Flow: client redirect → auth server → code → token exchange → user info
- Session vs Token: Session = stateful (server saklar), JWT = stateless (token'da saklanır)
- RBAC: Roller (admin, user) + İzinler (posts:read, users:delete). Middleware ile kontrol
- Güvenlik kuralları: HTTPS zorunlu, CORS ayarla, rate limiting uygula, brute force koruması ekle
:::

:::senior-learns
Bir Senior Developer veya CTO, authentication konusunu öğrenirken şu yaklaşımı benimser:

1. **Threat modeling yapar** - OWASP Top 10'u ezberden bilir. Her authentication flow için tehdit modellemesi yapar: XSS, CSRF, token theft, brute force, credential stuffing. Her tehdide karşı savunma mekanizması tasarlar.
2. **Zero-trust architecture uygular** - "Hiçbir isteğe güvenme, her şeyi doğrula" prensibiyle çalışır. Internal servisler arası iletişimde bile mTLS ve service mesh authentication kullanır.
3. **Key rotation ve secret management yapar** - JWT secret'larını düzenli döndürür (rotate). HashiCorp Vault veya AWS Secrets Manager ile secret'ları yönetir. Environment variable'larda bile hardcoded secret bırakmaz.
4. **Auth servisini izole eder** - Authentication'ı ayrı bir mikroservis olarak tasarlar. Single Sign-On (SSO) implementasyonu yapar. Auth servisi giderse bile diğer servisler kısa süre çalışabilir (graceful degradation).
5. **Compliance gereksinimlerini bilir** - KVKK, GDPR, SOC2, PCI-DSS gereksinimlerini anlar. Audit log tutar: kim, ne zaman, hangi kaynağa erişti. Data residency ve encryption at rest politikalarını uygular.
6. **Pentest ve security audit yaptırır** - Kendi koduna penetration test yaptırır. Bug bounty programı düşünür. Dependency vulnerability scanning (Snyk, pnpm audit) CI/CD'ye entegre eder.

**Profesyonel Mindset:** "Güvenlik bir özellik değil, bir kültürdür. Tek bir zayıf halka tüm sistemi çökertir. Kendi crypto'nu yazma, battle-tested kütüphaneleri kullan, her kararı 'saldırgan olsam ne yapardım?' sorusuyla test et. Security review'suz hiçbir PR merge etme."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Authentication** (aw-then-tih-key-shun) → Kimlik Doğrulama
   *"The API requires authentication before accessing protected resources."*

2. **Authorization** (aw-thuh-rih-zey-shun) → Yetkilendirme
   *"Role-based authorization ensures users can only access permitted resources."*

3. **Token** (toh-kun) → Jeton / Token
   *"The JWT access token expires after 15 minutes for security purposes."*

4. **Hash** (hæʃ) → Özet / Hash
   *"User passwords are hashed with bcrypt before storing in the database."*

5. **Middleware** (mid-wehr) → Ara Yazılım
   *"The authentication middleware validates the JWT token on every request."*

**Okuma Egzersizi:** Auth0 Blog'da "JWT Handbook" makalesini İngilizce oku: https://auth0.com/resources/ebooks/jwt-handbook

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "JWT refresh token rotation eklendi"
→ Örnek: `feat: implement JWT refresh token rotation for enhanced security`
:::

:::external-resource
- 📺 **Web Dev Simplified:** "JWT Authentication Tutorial" (YouTube, ücretsiz)
- 📖 **OWASP:** "Authentication Cheat Sheet" (owasp.org, ücretsiz)
- 📖 **Auth0 Docs:** "Introduction to Identity" (auth0.com/docs, ücretsiz)
- 📖 **JWT.io:** jwt.io (JWT debugger ve kütüphane listesi, ücretsiz)
- 📺 **Fireship:** "Session vs Token Authentication" (10 dakika, YouTube, ücretsiz)
:::
