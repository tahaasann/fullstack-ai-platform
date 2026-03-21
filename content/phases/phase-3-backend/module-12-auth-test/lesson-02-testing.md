---
title: "Testing: Kaliteli Kod İçin Test Yazma Sanatı"
id: "mod-12-auth/lesson-02"
estimated_minutes: 55
order: 2
tags: ["testing", "unit-test", "integration-test", "e2e", "tdd", "jest", "pytest", "cypress", "playwright"]
prerequisites: ["mod-12-auth/lesson-01"]
---

# Testing: Kaliteli Kod İçin Test Yazma Sanatı

:::realworld
Spotify her gün yüzlerce deployment yapıyor ve neredeyse hiç production hatası yaşamıyor. Bunun sırrı kapsamlı test süiti ve CI/CD pipeline'ı. Bir geliştirici kod değişikliği yaptığında, binlerce test otomatik çalışır ve herhangi biri fail ederse deployment engellenir. Bu derste, profesyonel dünyada zorunlu olan test yazma becerilerini derinlemesine öğreneceksin.
:::

## Neden Test Yazıyorsun?

Test yazmak "ekstra iş" değil, profesyonel yazılım geliştirmenin olmazsa olmazıdır. Test yazmadan:

- Refactoring yapamazsın (bir şeyi değiştirince başka yerleri bozarsın)
- Güvenle deploy edemezsin
- Regression bug'larını yakalayamazsın
- Takım arkadaşlarının kodunu güvenle değiştiremezsin
- Mülakatlarda dezavantajlı olursun

:::deha-tip
Deha seviyesi geliştiriciler "kodum çalışıyor, neden test yazayım?" demez. "Test yazmadan kodun çalıştığını nasıl kanıtlarım?" der. Her PR'da testler olmadan merge etmeyi reddeder. Test coverage'ı %80'in altındaki PR'ları geri gönderir.
:::

## Testing Pyramid (Test Piramidi)

:::concept[Testing Pyramid (İng: Testing Pyramid)]
Test piramidi, farklı test seviyelerinin ideal oranını gösteren bir modeldir. Tabanda çok sayıda hızlı unit test, ortada daha az integration test, tepede minimum E2E test bulunur.

**Türkçe karşılığı:** Test Piramidi
**Ne işe yarar:** Test stratejisi oluştururken hangi seviyede kaç test yazılacağını belirler
**Gerçek hayat benzetmesi:** Bir binanın güvenlik sistemi: Her oda kapı kilidi (unit), kat güvenliği (integration), bina güvenliği (E2E). Her odaya kilit takman ama binaya tek güvenlik görevlisi yeterli
:::

:::code[text]{title="Test Piramidi"}
         /‾‾‾‾‾‾\
        / E2E    \        %10 - En yavaş, en az
       / (%10)    \       Tüm sistemi test eder
      /‾‾‾‾‾‾‾‾‾‾‾‾\
     / Integration   \    %20 - Orta hız
    / (%20)           \   Modüllerin birlikte çalışmasını test eder
   /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
  / Unit Tests           \  %70 - En hızlı, en çok
 / (%70)                  \ Tek fonksiyon/modülü test eder
/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\

Unit Test:        ~1-10 ms/test, izole, mock'lanmış bağımlılıklar
Integration Test: ~100-1000 ms/test, gerçek DB/API, modüller arası
E2E Test:         ~5-30 saniye/test, gerçek tarayıcı, kullanıcı senaryosu
:::

## TDD: Test-Driven Development

:::concept[TDD (Test-Driven Development)]
TDD, önce testi yazıp sonra kodu yazdığın bir geliştirme metodolojisidir. Red-Green-Refactor döngüsünü takip eder.

**Türkçe karşılığı:** Test Odaklı Geliştirme
**Ne işe yarar:** Daha temiz, daha az bug'lı kod yazmayı sağlar
**Gerçek hayat benzetmesi:** Önce sınav sorularını hazırla, sonra ders notlarını yaz. Sınav sorularına cevap verebilen notlar yazmış olursun.
:::

:::code[text]{title="TDD: Red-Green-Refactor Döngüsü"}
1. RED (Kırmızı):
   → Başarısız bir test yaz
   → Test, henüz yazılmamış özelliği tanımlar
   → Testin fail ettiğini gör (kırmızı)

2. GREEN (Yeşil):
   → Testi geçirecek EN BASİT kodu yaz
   → Mükemmel kod değil, çalışan kod
   → Testin pass ettiğini gör (yeşil)

3. REFACTOR (Düzenle):
   → Kodu temizle ve optimize et
   → Testler hala geçiyor mu kontrol et
   → DRY, SOLID prensiplerini uygula

→ Döngüyü tekrarla
:::

:::code[javascript]{title="TDD Örneği: Şifre Doğrulama Fonksiyonu"}
// ADIM 1 - RED: Önce testi yaz
// password-validator.test.js
describe('validatePassword', () => {
  test('en az 8 karakter olmalı', () => {
    expect(validatePassword('abc')).toEqual({
      valid: false,
      errors: ['Şifre en az 8 karakter olmalıdır']
    });
  });

  test('büyük harf içermeli', () => {
    expect(validatePassword('abcdefgh')).toEqual({
      valid: false,
      errors: expect.arrayContaining(['Şifre en az 1 büyük harf içermelidir'])
    });
  });

  test('sayı içermeli', () => {
    expect(validatePassword('Abcdefgh')).toEqual({
      valid: false,
      errors: expect.arrayContaining(['Şifre en az 1 sayı içermelidir'])
    });
  });

  test('geçerli şifre', () => {
    expect(validatePassword('Abc12345')).toEqual({
      valid: true,
      errors: []
    });
  });
});

// ADIM 2 - GREEN: Testi geçirecek kodu yaz
// password-validator.js
function validatePassword(password) {
  const errors = [];

  if (password.length < 8) {
    errors.push('Şifre en az 8 karakter olmalıdır');
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('Şifre en az 1 büyük harf içermelidir');
  }
  if (!/[0-9]/.test(password)) {
    errors.push('Şifre en az 1 sayı içermelidir');
  }

  return { valid: errors.length === 0, errors };
}

// ADIM 3 - REFACTOR: Kodu temizle
// Kuralları konfigürasyon olarak çıkar, regex'leri const yap, vb.
:::

## Unit Testing: Jest ve Vitest

:::comparison
| Özellik | Jest | Vitest | Pytest |
|---------|------|--------|--------|
| Dil | JavaScript/TypeScript | JavaScript/TypeScript | Python |
| Hız | Orta | Çok hızlı (Vite tabanlı) | Hızlı |
| Config | Minimal | Minimal (vite.config) | Minimal |
| Watch modu | Var | Var (çok hızlı) | pytest-watch ile |
| **Ne zaman kullan** | React, Node.js projeleri | Vite projeleri, modern | Python projeleri |

**Tavsiye:** Vite kullanıyorsan Vitest, diğer JS projelerinde Jest, Python'da Pytest kullan.
:::

:::code[javascript]{title="Jest/Vitest Unit Test Örnekleri"}
// math.js
export function add(a, b) { return a + b; }
export function divide(a, b) {
  if (b === 0) throw new Error('Sıfıra bölünemez');
  return a / b;
}

// math.test.js
import { describe, test, expect } from 'vitest'; // veya jest'ten import
import { add, divide } from './math';

describe('add fonksiyonu', () => {
  test('iki pozitif sayıyı toplar', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('negatif sayılarla çalışır', () => {
    expect(add(-1, -2)).toBe(-3);
  });

  test('sıfır ile toplar', () => {
    expect(add(5, 0)).toBe(5);
  });
});

describe('divide fonksiyonu', () => {
  test('iki sayıyı böler', () => {
    expect(divide(10, 2)).toBe(5);
  });

  test('ondalıklı sonuç döndürür', () => {
    expect(divide(1, 3)).toBeCloseTo(0.333, 2);
  });

  test('sıfıra bölmede hata fırlatır', () => {
    expect(() => divide(10, 0)).toThrow('Sıfıra bölünemez');
  });
});

// Matchers (eşleştiriciler)
test('yaygın matcher örnekleri', () => {
  // Eşitlik
  expect(2 + 2).toBe(4);                    // Strict equality (===)
  expect({ name: 'Ali' }).toEqual({ name: 'Ali' }); // Deep equality

  // Truthiness
  expect(true).toBeTruthy();
  expect(null).toBeFalsy();
  expect(undefined).toBeUndefined();
  expect('hello').toBeDefined();

  // Sayılar
  expect(10).toBeGreaterThan(5);
  expect(10).toBeLessThanOrEqual(10);

  // String
  expect('Merhaba Dünya').toContain('Dünya');
  expect('ahmet@example.com').toMatch(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);

  // Array
  expect([1, 2, 3]).toContain(2);
  expect([1, 2, 3]).toHaveLength(3);

  // Object
  expect({ a: 1, b: 2 }).toHaveProperty('a');
  expect({ a: 1, b: 2 }).toMatchObject({ a: 1 });
});
:::

### Mocking, Stubbing ve Spying

:::concept[Mock (İng: Mock)]
Mock, test sırasında gerçek bağımlılıkların yerine kullanılan sahte nesnelerdir. Dış servisleri (API, veritabanı) simüle eder.

**Türkçe karşılığı:** Taklit Nesne / Sahte Nesne
**Ne işe yarar:** Testleri dış bağımlılıklardan izole eder, hızlı ve güvenilir testler sağlar
**Gerçek hayat benzetmesi:** Film setindeki sahte binalar gibi - dışarıdan gerçek görünür ama içi boştur. Test için yeterlidir.
:::

:::code[javascript]{title="Mocking, Stubbing, Spying"}
// user-service.js
import { db } from './database';
import { sendEmail } from './email-service';

export async function registerUser(name, email, password) {
  const existingUser = await db.findUserByEmail(email);
  if (existingUser) throw new Error('Bu email zaten kayıtlı');

  const user = await db.createUser({ name, email, password });
  await sendEmail(email, 'Hoşgeldin!', `Merhaba ${name}`);
  return user;
}

// user-service.test.js
import { describe, test, expect, vi } from 'vitest';
import { registerUser } from './user-service';
import { db } from './database';
import { sendEmail } from './email-service';

// Modülleri mock'la
vi.mock('./database');
vi.mock('./email-service');

describe('registerUser', () => {
  // Her testten önce mock'ları temizle
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test('yeni kullanıcı başarıyla kaydedilir', async () => {
    // ARRANGE: Mock'ları hazırla
    db.findUserByEmail.mockResolvedValue(null); // Kullanıcı yok
    db.createUser.mockResolvedValue({
      id: 1, name: 'Ali', email: 'ali@ex.com'
    });
    sendEmail.mockResolvedValue(true);

    // ACT: Fonksiyonu çağır
    const user = await registerUser('Ali', 'ali@ex.com', 'Pass123!');

    // ASSERT: Sonuçları kontrol et
    expect(user).toEqual({ id: 1, name: 'Ali', email: 'ali@ex.com' });
    expect(db.createUser).toHaveBeenCalledTimes(1);
    expect(db.createUser).toHaveBeenCalledWith({
      name: 'Ali', email: 'ali@ex.com', password: 'Pass123!'
    });
    expect(sendEmail).toHaveBeenCalledWith(
      'ali@ex.com', 'Hoşgeldin!', 'Merhaba Ali'
    );
  });

  test('var olan email ile kayıt hata fırlatır', async () => {
    db.findUserByEmail.mockResolvedValue({ id: 1, email: 'ali@ex.com' });

    await expect(
      registerUser('Ali', 'ali@ex.com', 'Pass123!')
    ).rejects.toThrow('Bu email zaten kayıtlı');

    // Email gönderilmemiş olmalı
    expect(sendEmail).not.toHaveBeenCalled();
  });

  test('email gönderimi başarısız olsa bile kullanıcı oluşturulur', async () => {
    db.findUserByEmail.mockResolvedValue(null);
    db.createUser.mockResolvedValue({ id: 1, name: 'Ali' });
    sendEmail.mockRejectedValue(new Error('Email servisi çöktü'));

    // Email hatası registerUser'dan fırlatılır
    await expect(
      registerUser('Ali', 'ali@ex.com', 'Pass123!')
    ).rejects.toThrow('Email servisi çöktü');
  });
});

// SPY: Gerçek fonksiyonu çağırıp izle
test('spy örneği', () => {
  const calculator = {
    add: (a, b) => a + b
  };

  const spy = vi.spyOn(calculator, 'add');

  const result = calculator.add(2, 3); // Gerçek fonksiyon çalışır

  expect(result).toBe(5);
  expect(spy).toHaveBeenCalledWith(2, 3);
  expect(spy).toHaveBeenCalledTimes(1);
});
:::

:::beginner-mistake
Yaygın hata: Her şeyi mock'lamak. Aşırı mock kullanımı testleri gerçek dünyadan koparır. Unit testlerde dış bağımlılıkları (DB, API, dosya sistemi) mock'la ama iş mantığını mock'lama. Integration testlerde mümkünse gerçek bağımlılıkları kullan.
:::

## Pytest ile Python Test

:::code[python]{title="Pytest Unit Test Örnekleri"}
# test_calculator.py
import pytest
from calculator import Calculator

class TestCalculator:
    def setup_method(self):
        """Her testten önce çalışır"""
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5.0

    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(10, 0)

    # Parametrize: Aynı testi farklı verilerle çalıştır
    @pytest.mark.parametrize("a, b, expected", [
        (1, 1, 2),
        (-1, 1, 0),
        (0, 0, 0),
        (100, 200, 300),
    ])
    def test_add_parametrized(self, a, b, expected):
        assert self.calc.add(a, b) == expected

# Fixture: Test verisini hazırla
@pytest.fixture
def sample_user():
    return {
        "name": "Ahmet",
        "email": "ahmet@example.com",
        "age": 28
    }

@pytest.fixture
def db_session():
    """Test veritabanı bağlantısı"""
    session = create_test_session()
    yield session  # Test çalışır
    session.rollback()  # Test sonrası temizlik
    session.close()

def test_create_user(db_session, sample_user):
    user = create_user(db_session, sample_user)
    assert user.name == "Ahmet"
    assert user.email == "ahmet@example.com"

# Mock ile dış bağımlılıkları taklit et
from unittest.mock import patch, MagicMock

@patch('services.email.send_email')
def test_register_sends_email(mock_send):
    mock_send.return_value = True

    register_user("Ali", "ali@ex.com", "Pass123!")

    mock_send.assert_called_once_with(
        "ali@ex.com", "Hoşgeldin!", "Merhaba Ali"
    )
:::

## Integration Testing: Supertest ile API Test

:::code[javascript]{title="Supertest ile API Integration Test"}
import { describe, test, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../app';
import { db } from '../database';

describe('Auth API Integration Tests', () => {
  beforeAll(async () => {
    // Test veritabanını hazırla
    await db.migrate.latest();
    await db.seed.run();
  });

  afterAll(async () => {
    // Temizle
    await db.migrate.rollback();
    await db.destroy();
  });

  describe('POST /api/auth/register', () => {
    test('yeni kullanıcı başarıyla kaydedilir', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          name: 'Test User',
          email: 'test@example.com',
          password: 'Test1234!'
        })
        .expect(201);

      expect(response.body).toHaveProperty('id');
      expect(response.body.email).toBe('test@example.com');
      expect(response.body).not.toHaveProperty('password'); // Şifre dönmemeli!
    });

    test('eksik alan ile kayıt 400 döner', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({ email: 'test@example.com' })
        .expect(400);

      expect(response.body.error).toContain('zorunlu');
    });

    test('mevcut email ile kayıt 409 döner', async () => {
      // Önce kaydet
      await request(app)
        .post('/api/auth/register')
        .send({ name: 'A', email: 'dup@ex.com', password: 'Test1234!' });

      // Aynı email ile tekrar dene
      const response = await request(app)
        .post('/api/auth/register')
        .send({ name: 'B', email: 'dup@ex.com', password: 'Test1234!' })
        .expect(409);

      expect(response.body.error).toContain('zaten kayıtlı');
    });
  });

  describe('POST /api/auth/login', () => {
    test('doğru bilgilerle login başarılı', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({ email: 'test@example.com', password: 'Test1234!' })
        .expect(200);

      expect(response.body).toHaveProperty('accessToken');
      expect(response.headers['set-cookie']).toBeDefined(); // refreshToken cookie
    });

    test('yanlış şifre ile login 401 döner', async () => {
      await request(app)
        .post('/api/auth/login')
        .send({ email: 'test@example.com', password: 'wrong' })
        .expect(401);
    });
  });

  describe('GET /api/profile (korumalı)', () => {
    test('token olmadan 401 döner', async () => {
      await request(app)
        .get('/api/profile')
        .expect(401);
    });

    test('geçerli token ile profil döner', async () => {
      // Login yap
      const loginRes = await request(app)
        .post('/api/auth/login')
        .send({ email: 'test@example.com', password: 'Test1234!' });

      const token = loginRes.body.accessToken;

      // Profili çek
      const response = await request(app)
        .get('/api/profile')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(response.body.email).toBe('test@example.com');
    });
  });
});
:::

## E2E Testing: Cypress vs Playwright

:::comparison
| Özellik | Cypress | Playwright |
|---------|---------|------------|
| Tarayıcı desteği | Chrome, Firefox, Edge | Chrome, Firefox, Safari, Edge |
| Dil | JavaScript/TypeScript | JS/TS, Python, Java, C# |
| Hız | Hızlı (browser içi) | Çok hızlı (paralel) |
| Paralel test | Ücretli (Dashboard) | Ücretsiz |
| Mobile testing | Sınırlı | Emulation desteği |
| Debugging | Time-travel, otomatik video | Trace viewer, codegen |
| **Ne zaman kullan** | Frontend-ağırlıklı SPA | Cross-browser, CI/CD |

**Tavsiye:** Yeni projeler için Playwright kullan. Daha hızlı, daha fazla tarayıcı desteği ve ücretsiz paralel test sunuyor.
:::

:::code[javascript]{title="Playwright E2E Test Örnekleri"}
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Kullanıcı Kayıt ve Giriş Akışı', () => {
  test('başarılı kayıt ve login', async ({ page }) => {
    // Kayıt sayfasına git
    await page.goto('/register');

    // Form doldur
    await page.fill('[name="name"]', 'Test Kullanıcı');
    await page.fill('[name="email"]', `test-${Date.now()}@example.com`);
    await page.fill('[name="password"]', 'Test1234!');
    await page.fill('[name="confirmPassword"]', 'Test1234!');

    // Kayıt ol butonuna tıkla
    await page.click('button[type="submit"]');

    // Başarılı kayıt mesajı
    await expect(page.locator('.success-message')).toBeVisible();
    await expect(page.locator('.success-message')).toContainText('Kayıt başarılı');

    // Login sayfasına yönlendirildi mi?
    await expect(page).toHaveURL('/login');
  });

  test('geçersiz email ile kayıt hatası', async ({ page }) => {
    await page.goto('/register');
    await page.fill('[name="email"]', 'gecersiz-email');
    await page.fill('[name="password"]', 'Test1234!');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toContainText('Geçerli bir email');
  });

  test('korumalı sayfaya yetkisiz erişim login sayfasına yönlendirir', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL('/login');
  });
});

// Visual regression test
test('ana sayfa görsel testi', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100
  });
});
:::

:::code[javascript]{title="Cypress E2E Test Örneği"}
// cypress/e2e/login.cy.js
describe('Login Sayfası', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('başarılı login ile dashboard\'a yönlendirir', () => {
    // API mock
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: { accessToken: 'fake-token' }
    }).as('loginRequest');

    cy.get('[data-testid="email"]').type('test@example.com');
    cy.get('[data-testid="password"]').type('Test1234!');
    cy.get('[data-testid="login-btn"]').click();

    cy.wait('@loginRequest');
    cy.url().should('include', '/dashboard');
  });

  it('yanlış şifre ile hata mesajı gösterir', () => {
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 401,
      body: { error: 'Geçersiz email veya şifre' }
    });

    cy.get('[data-testid="email"]').type('test@example.com');
    cy.get('[data-testid="password"]').type('wrong');
    cy.get('[data-testid="login-btn"]').click();

    cy.get('.error-message').should('contain', 'Geçersiz email veya şifre');
  });
});
:::

## Code Coverage (Kod Kapsama)

:::concept[Code Coverage (İng: Code Coverage)]
Code coverage, test süitinin kaynak kodun yüzde kaçını çalıştırdığını ölçen metriktir. Statement, branch, function ve line coverage olarak ölçülür.

**Türkçe karşılığı:** Kod Kapsama Oranı
**Ne işe yarar:** Testlerin kodun ne kadarını kapsadığını gösterir
**Gerçek hayat benzetmesi:** Güvenlik kameralarının binanın yüzde kaçını izlediği gibi - %100 kapsama her köşenin izlendiği anlamına gelir
:::

:::code[text]{title="Coverage Metrikleri"}
Statement Coverage:  Çalıştırılan kod satırları / Toplam satır
Branch Coverage:     Test edilen dallar (if/else) / Toplam dal
Function Coverage:   Çağrılan fonksiyonlar / Toplam fonksiyon
Line Coverage:       Çalıştırılan satırlar / Toplam satır

Hedefler:
  Minimum: %60 (kabul edilebilir)
  İyi:     %80 (önerilen)
  Çok iyi: %90+ (kritik projeler)

Dikkat: %100 coverage = %100 bug-free değil!
  - Coverage, kodun çalıştırıldığını gösterir ama doğru çalıştığını garanti etmez.
  - Edge case'ler, race condition'lar ve integration sorunları coverage'da görünmez.
  - %80 ANLAMLI coverage > %100 anlamsız coverage
:::

:::code[json]{title="Jest/Vitest Coverage Konfigürasyonu"}
// vitest.config.ts veya jest.config.js
{
  "test": {
    "coverage": {
      "provider": "v8",
      "reporter": ["text", "html", "lcov"],
      "thresholds": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      },
      "exclude": [
        "node_modules",
        "test",
        "**/*.config.*",
        "**/*.d.ts"
      ]
    }
  }
}

// Çalıştırma:
// pnpm exec vitest run --coverage
// pnpm exec jest --coverage
:::

:::tip
Coverage hedefini %80 olarak belirle ama "anlamlı" test yaz. Sadece coverage artırmak için yazılan testler (implementation detail testleri) bakım yükü oluşturur. Davranış (behavior) test et, uygulama detaylarını (implementation) değil.
:::

## AAA Pattern ve Test Best Practices

:::code[javascript]{title="AAA (Arrange-Act-Assert) Pattern"}
test('kullanıcı profil fotoğrafını güncelleyebilir', async () => {
  // ARRANGE (Hazırla): Test verisini ve ortamı hazırla
  const user = await createTestUser({ name: 'Ali' });
  const newAvatar = 'https://example.com/avatar.jpg';

  // ACT (Uygula): Test edilecek işlemi gerçekleştir
  const updatedUser = await updateAvatar(user.id, newAvatar);

  // ASSERT (Doğrula): Sonucu kontrol et
  expect(updatedUser.avatar).toBe(newAvatar);
  expect(updatedUser.updatedAt).not.toEqual(user.updatedAt);
});

// Test isimlendirme: "ne_yapılır_hangi_durumda_ne_beklenir"
test('login_gecersizSifre_401Doner', async () => { /* ... */ });
test('register_mevcutEmail_409Doner', async () => { /* ... */ });
test('getProfile_gecerliToken_kullaniciBilgisiDoner', async () => { /* ... */ });
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: TDD ile Password Validator (Kolay)

Test-Driven Development (Red-Green-Refactor) dongusuyle bir sifre dogrulama fonksiyonu gelistir.

```javascript
// __tests__/passwordValidator.test.js
const { validatePassword } = require("../src/passwordValidator");

describe("validatePassword", () => {
  // RED: Once basarisiz testleri yaz

  test("en az 8 karakter olmali", () => {
    expect(validatePassword("Ab1!xyz")).toEqual({
      valid: false,
      errors: expect.arrayContaining(["En az 8 karakter olmali"]),
    });
  });

  test("en az bir buyuk harf icermeli", () => {
    expect(validatePassword("abcdefg1!")).toEqual({
      valid: false,
      errors: expect.arrayContaining(["En az bir buyuk harf olmali"]),
    });
  });

  // TODO: En az bir kucuk harf testi
  // TODO: En az bir rakam testi
  // TODO: En az bir ozel karakter testi (!@#$%^&*)
  // TODO: Yaygin sifreleri reddetme testi ("password123", "12345678")
  // TODO: Gecerli sifre testi — { valid: true, errors: [], strength: "strong" }

  test("sifre gucu hesaplanmali", () => {
    expect(validatePassword("Abc12345!")).toHaveProperty("strength", "medium");
    expect(validatePassword("MyS3cur3P@ssw0rd!")).toHaveProperty("strength", "strong");
  });
});

// src/passwordValidator.js
// GREEN: Testleri gecirecek en basit kodu yaz
function validatePassword(password) {
  const errors = [];

  // TODO: Tum kurallari kontrol et
  // TODO: strength hesapla (weak/medium/strong)

  return { valid: errors.length === 0, errors, strength: "weak" };
}

module.exports = { validatePassword };
```

**Beklenen Sonuc:** Tum testler gecmeli. Her kural icin ayri hata mesaji donmeli. Sifre gucu dogru hesaplanmali. `npm test -- --coverage` ile coverage %100 olmali.
**Ipucu:** TDD'de once RED (basarisiz test yaz), sonra GREEN (testi gec), sonra REFACTOR (kodu temizle). Bu donguyu her kural icin tekrarla.

---

### Alistirma 2: Supertest ile Integration Test (Orta)

Authentication API endpoint'leri icin integration testleri yaz.

```javascript
const request = require("supertest");
const app = require("../src/app"); // Express app

describe("Auth API", () => {
  describe("POST /api/auth/register", () => {
    test("basarili kayit — 201 + token donmeli", async () => {
      const res = await request(app)
        .post("/api/auth/register")
        .send({ name: "Test User", email: "test@test.com", password: "Test1234!" });

      expect(res.status).toBe(201);
      expect(res.body).toHaveProperty("token");
      expect(res.body.user).toHaveProperty("email", "test@test.com");
      expect(res.body.user).not.toHaveProperty("password"); // Sifre donmemeli!
    });

    test("eksik alan — 400 donmeli", async () => {
      const res = await request(app)
        .post("/api/auth/register")
        .send({ name: "Test" }); // email ve password eksik

      expect(res.status).toBe(400);
      expect(res.body).toHaveProperty("error");
    });

    // TODO: Duplicate email testi — 409 Conflict
    // TODO: Zayif sifre testi — 400
  });

  describe("POST /api/auth/login", () => {
    // TODO: Basarili login testi — 200 + access token + refresh token
    // TODO: Yanlis sifre testi — 401
    // TODO: Olmayan email testi — 401
  });

  describe("GET /api/profile (korunmali)", () => {
    // TODO: Token ile erisim — 200 + user bilgisi
    // TODO: Token olmadan erisim — 401
    // TODO: Gecersiz token ile erisim — 401
    // TODO: Suresi dolmus token ile erisim — 401
  });
});
```

**Beklenen Sonuc:** En az 8 test senaryosu yazilmis olmali. Basarili ve basarisiz senaryolar kapsanmali. Token ile korunmali endpoint testleri calismali.
**Ipucu:** `request(app).set("Authorization", "Bearer " + token)` ile token gonder. `beforeAll` ile test user olustur, `afterAll` ile temizle.

---

### Alistirma 3: Mock/Spy ve Coverage (Zor)

Jest mock ve spy kullanarak dis servisleri izole et. Coverage raporunu olustur ve %80 hedefini yakala.

```javascript
// Dis servis — email gonderme
// src/services/emailService.js
const sendEmail = async (to, subject, body) => {
  // Gercek email gonderme (test'te mock'lanmali)
};

// src/services/userService.js
class UserService {
  constructor(userRepo, emailService) {
    this.userRepo = userRepo;
    this.emailService = emailService;
  }

  async register(userData) {
    const user = await this.userRepo.create(userData);
    await this.emailService.sendWelcome(user.email, user.name);
    return user;
  }
}

// __tests__/userService.test.js
describe("UserService", () => {
  let userService;
  let mockUserRepo;
  let mockEmailService;

  beforeEach(() => {
    // TODO: Mock repository ve email service olustur
    mockUserRepo = {
      create: jest.fn().mockResolvedValue({ id: 1, name: "Test", email: "t@t.com" }),
      findByEmail: jest.fn().mockResolvedValue(null),
    };

    mockEmailService = {
      sendWelcome: jest.fn().mockResolvedValue(true),
    };

    userService = new UserService(mockUserRepo, mockEmailService);
  });

  test("register — kullanici olusturur ve hosgeldin emaili gonderir", async () => {
    const user = await userService.register({ name: "Test", email: "t@t.com" });

    // TODO: userRepo.create cagrildi mi?
    expect(mockUserRepo.create).toHaveBeenCalledWith({ name: "Test", email: "t@t.com" });

    // TODO: emailService.sendWelcome cagrildi mi?
    expect(mockEmailService.sendWelcome).toHaveBeenCalledWith("t@t.com", "Test");

    // TODO: Dogru user dondu mu?
    expect(user).toHaveProperty("id", 1);
  });

  // TODO: Email gonderme basarisiz olursa ne olmali?
  // TODO: Email hatasinin register'i durdurmamasini test et
});

// Coverage: package.json'a ekle:
// "scripts": { "test:coverage": "jest --coverage --coverageThreshold='{\"global\":{\"lines\":80}}'" }
```

**Beklenen Sonuc:** Dis servisler mock'lanmis olmali (gercek email gonderilmemeli). Mock fonksiyonlarin cagrilma sayisi ve parametreleri dogrulanmali. Coverage %80'in ustunde olmali.
**Ipucu:** `jest.fn()` mock fonksiyon olusturur. `.mockResolvedValue()` async fonksiyonlar icin Promise dondurur. `toHaveBeenCalledWith()` ile parametreleri kontrol et.
:::

:::knowledge-check
type: multiple_choice
question: "TDD'nin Red-Green-Refactor döngüsündeki doğru sıralama hangisidir?"
options:
  - "Kodu yaz → Test yaz → Refactor et"
  - "Başarısız test yaz → Testi geçirecek en basit kodu yaz → Kodu temizle"
  - "Test yaz → Refactor et → Kodu yaz"
  - "Kodu yaz → Refactor et → Test yaz"
correct: 1
explanation: "TDD döngüsü: 1) RED - Başarısız bir test yaz (henüz kod yok). 2) GREEN - Testi geçirecek en basit kodu yaz (mükemmel olması gerekmez). 3) REFACTOR - Çalışan kodu temizle ve optimize et (testler hala geçmeli)."
:::

:::knowledge-check
type: multiple_choice
question: "Test piramidinde en çok hangi tür test yazılmalıdır?"
options:
  - "E2E testleri (%70)"
  - "Integration testleri (%70)"
  - "Unit testleri (%70)"
  - "Manual testler (%70)"
correct: 2
explanation: "Test piramidine göre en çok unit test (%70) yazılmalıdır çünkü en hızlı, en ucuz ve en kolay bakım yapılabilir testlerdir. Integration %20, E2E %10 oranında olmalıdır."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "Test piramidini (unit, integration, e2e) acikla. Her katmanda ne test edilir, ne test edilmez? Unit test'te mock/stub/spy arasindaki farki orneklerle goster. 'Implementation detail test etme, davranis test et' prensibi ne anlama gelir? Kent C. Dodds'un Testing Trophy yaklasimini acikla."

**2. Pratik Uygulama:**
> "Jest ile bir Express.js API'sinin testlerini yaz: UserService icin unit test (mock database), auth endpoint icin integration test (supertest ile), ve bir kullanici kayit akisi icin e2e test. AAA (Arrange, Act, Assert) patternini kullan. Code coverage raporunu yorumla."
> Takip: "Simdi React Testing Library ile bir LoginForm component'inin testini yaz. Kullanici perspektifinden test et: form doldurma, submit, basarili/basarisiz senaryo."

**3. Mukemmellik Icin:**
> "TDD (Test-Driven Development) ile bir odeme servisi gelistir. Once testi yaz (Red), sonra minimum kodu yaz (Green), sonra refactor et. Edge case'leri (yetersiz bakiye, network hatasi, duplicate odeme) test et. CI/CD pipeline'da test otomasyonu, coverage threshold ve mutation testing nasil uygulanir?"

### Pair Programming Ipucu
Test yazarken AI'a test edilecek fonksiyonu goster ve sor: "Bu fonksiyon icin hangi test senaryolarini yazmaliyim? Happy path, edge case'ler ve error senaryolari neler? Mock'lanmasi gereken bagimliliklar hangileri? AAA pattern ile test kodunu olustur."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Unit test, integration test ve E2E test arasindaki farklar nelerdir?**
- **Junior cevabi:** Unit tek fonksiyonu, integration birlestirmeyi, E2E tum sistemi test eder.
- **Senior cevabi:** Unit test: tek bir fonksiyon/metod, dissal bagimliliklari mock'lanir, milisaniyede calisir, en buyuk coverage'i saglar (%70+). Integration test: birden fazla katmanin birlikte calismasi (API endpoint + DB), gercek veya test DB kullanilir, boundary'lerde hatalari yakalar. E2E test: kullanici perspektifinden (tarayici otomasyonu), en yavas ve en kirilgan ama en gercekci. Test piramidi: unit > integration > E2E. Anti-pattern: ice cream cone (cok E2E, az unit). Mock vs stub vs spy farki: mock = fake implementation, stub = sabit deger doner, spy = gercek fonksiyonu sarar ve cagirilma bilgisini kaydeder.

**Soru 2: TDD (Test Driven Development) nedir ve pratikte nasil uygulanir?**
- **Junior cevabi:** Once test yazilir, sonra kodu yazilir, sonra refactor edilir.
- **Senior cevabi:** Red-Green-Refactor dongusu: 1) Red: basarisiz test yaz (henuz implementation yok), 2) Green: testi gecirmek icin en basit kodu yaz, 3) Refactor: kodu iyilestir, test hala gecmeli. TDD faydalari: daha iyi tasarim (testable kod = loosely coupled kod), regression guveniligi, dokumantasyon gorevi gorur. Zorluklar: ogrenme egrisi, bazi senaryolarda (UI, exploratory coding) zorlanir. Outside-in TDD: E2E/integration'dan baslar, inside-out: unit'ten baslar. %100 coverage hedef degil, critical path'lerin %100 coverage'i hedef olmali.
:::

:::must-note
- Test piramidi: Unit (%70, en hızlı) → Integration (%20) → E2E (%10, en yavaş)
- TDD döngüsü: RED (başarısız test yaz) → GREEN (geçirecek kod yaz) → REFACTOR (temizle)
- AAA pattern: Arrange (hazırla) → Act (uygula) → Assert (doğrula)
- Mock: Sahte nesne (dış bağımlılık yerine), Spy: Gerçek fonksiyonu izle, Stub: Sabit değer döndür
- Jest/Vitest matcher'lar: toBe (===), toEqual (deep), toThrow, toContain, toHaveBeenCalledWith
- Pytest: @pytest.mark.parametrize (çoklu veri), @pytest.fixture (test verisi), with pytest.raises (hata)
- Supertest: API integration test. request(app).post('/api').send(data).expect(200)
- Playwright vs Cypress: Playwright (cross-browser, paralel, ücretsiz), Cypress (DX iyi, Chrome ağırlıklı)
- Code coverage hedefi: %80+ anlamlı coverage. Statement, branch, function, line coverage
- %100 coverage = bug-free DEĞİL. Davranış test et, implementasyon detayı değil
- Test isimlendirme: ne_yapılır_hangiDurum_neBeklenir. Açıklayıcı, okunabilir isimler
- CI/CD'de testler: Her PR'da otomatik çalışmalı, fail ederse merge engellenme
:::

:::senior-learns
Bir Senior Developer veya CTO, testing konusunu öğrenirken şu yaklaşımı benimser:

1. **Test stratejisi belirler** - Projenin kritiklik seviyesine göre test oranlarını ayarlar. Fintech'te %90+ coverage zorunlu, MVP'de %60 yeterli. Test piramidini projeye adapte eder, bazen "testing trophy" (integration ağırlıklı) daha uygundur.
2. **Testing culture oluşturur** - Takımda "test yazılmamış PR merge edilmez" kuralını koyar. Code review'da test kalitesini de değerlendirir. Test yazma eğitimleri düzenler. Test debt'i tracking eder.
3. **Test infrastructure kurar** - CI/CD'de test parallelization, test splitting (CircleCI, GitHub Actions matrix) uygular. Docker ile izole test ortamları kurar. Flaky test detection ve quarantine mekanizması ekler.
4. **Contract testing uygular** - Microservice'ler arası API sözleşmelerini Pact ile test eder. Consumer-driven contract testing ile breaking change'leri deploy öncesi yakalar.
5. **Performance testing entegre eder** - k6 veya Artillery ile load test yazar. Baseline performans metriklerini belirler. CI/CD'de performance regression testi çalıştırır. P95 latency threshold koyar.
6. **Mutation testing değerlendirir** - Stryker veya mutmut ile testlerin gerçekten bug yakalayıp yakalamadığını test eder. "Coverage yüksek ama testler zayıf" durumunu tespit eder.

**Profesyonel Mindset:** "İyi test yazmak, iyi kod yazmak kadar önemli bir beceridir. Testler, refactoring yapma cesaretini verir, regression'ları yakalar ve canlı dokümantasyon olarak hizmet eder. Test yazmak yavaşlatır gibi görünse de, uzun vadede hız kazandırır. Bug fixing süresini %80 azaltır. Her saat test yazmaya harcanan zaman, üç saat debug süresinden kurtarır."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Unit Test** (yoo-nit test) → Birim Testi
   *"Each unit test should test a single function or method in isolation."*

2. **Coverage** (kuv-uh-rij) → Kapsama
   *"We aim for at least 80% code coverage on all critical modules."*

3. **Mock** (mok) → Taklit / Sahte Nesne
   *"We mock the database layer to isolate the business logic in unit tests."*

4. **Assertion** (uh-sur-shun) → Doğrulama / İddia
   *"The test makes three assertions to verify the function's behavior."*

5. **Regression** (ri-gresh-un) → Gerileme / Geriye Dönük Hata
   *"Our CI pipeline catches regression bugs before they reach production."*

**Okuma Egzersizi:** Kent Beck'in "Test-Driven Development by Example" kitabının ilk bölümünü İngilizce oku.

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Kullanıcı servisi için unit testleri eklendi"
→ Örnek: `test: add unit tests for user registration service`
:::

:::external-resource
- 📺 **Fireship:** "Test-Driven Development in 100 Seconds" (YouTube, ücretsiz)
- 📖 **Jest Docs:** jestjs.io/docs (resmi, ücretsiz)
- 📖 **Vitest Docs:** vitest.dev (resmi, ücretsiz)
- 📖 **Playwright Docs:** playwright.dev (resmi, ücretsiz)
- 📖 **Pytest Docs:** docs.pytest.org (resmi, ücretsiz)
- 📺 **The Net Ninja:** "Testing in JavaScript" serisi (YouTube, ücretsiz)
:::
