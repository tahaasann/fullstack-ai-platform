---
title: "Design Patterns ve SOLID"
id: mod-18-architecture/lesson-02
estimated_minutes: 95
order: 2
tags: [design-patterns, solid, singleton, factory, observer, strategy, adapter, decorator, clean-code, anti-patterns]
prerequisites: [mod-18-architecture/lesson-01]
---

# Design Patterns ve SOLID

**Design patterns**, yazılım geliştirmede tekrar eden problemlere **kanıtlanmış çözümlerdir**. SOLID prensipleri ise bu pattern'ların temelini oluşturan tasarım ilkeleridir. Bu ders, sadece pattern'ları ezberlemek değil — **ne zaman, neden ve nasıl** kullanılacağını öğretecek. Her pattern'ı JavaScript ve Python'da gerçek dünya örnekleriyle göreceksin.

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "SOLID prensiplerinin her birini (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion) gerçek TypeScript/Python örnekleriyle açıkla. Her prensibi ihlal eden kodu göster, sonra SOLID'e uygun refactor edilmis versiyonunu yaz. Neden bu prensipler büyük projelerde kritik?"

**2. Pratik Uygulama:**
> "Bir bildirim sistemi tasarla: Strategy pattern ile farklı bildirim kanallari (email, SMS, push notification), Observer pattern ile event-driven bildirim tetikleme, Factory pattern ile bildirim nesnesi oluşturma. TypeScript ile implement et ve her pattern'in seçim nedenini açıkla."
> Takip: "Şimdi bu sisteme Decorator pattern ile bildirim zenginlestirme (logging, retry, rate limiting) ekle. Adapter pattern ile farklı email provider'lari (SendGrid, AWS SES) arasinda geçiş yap."

**3. Mukemmellik Için:**
> "Anti-pattern'leri tani ve coz: God Object, Spaghetti Code, Shotgun Surgery, Feature Envy ve Primitive Obsession. Her anti-pattern için gerçek kod örneği göster, hangi design pattern veya refactoring teknigi ile cozulecegini açıkla. Martin Fowler'in refactoring katalogundan ilgili teknikleri referans al."

### Pair Programming Ipucu
Kod yazarken AI'a class veya fonksiyon yapisini göster ve sor: "Bu kod SOLID prensiplerini ihlal ediyor mu? Hangi design pattern uygulanmali? Refactoring onerilerin neler? Clean Code standartlarina gore iyilestirmeler yap."
:::

:::must-note
## Defterine Yaz!

1. **SOLID = 5 temel prensip.** S(ingle Responsibility), O(pen/Closed), L(iskov Substitution), I(nterface Segregation), D(ependency Inversion). Bu prensipleri bilmeden pattern kullanmak, temelsiz bina yapmaktır.
2. **Pattern kullanmanın amacı "pattern kullanmak" değil.** Gerçek bir problemi çözmek. Gereksiz pattern kullanmak (over-engineering) anti-pattern'dır.
3. **Strategy Pattern = if/else cehenneminden kurtuluş.** Birden fazla algoritma/davranış arasında runtime'da seçim yapmak gerektiğinde kullan.
4. **Observer Pattern = Event system'in temeli.** EventEmitter, pub/sub, reactive programming — hepsi Observer pattern'ının varyasyonları.
5. **Factory Pattern = Object creation'ı soyutla.** "new" keyword'ünü doğrudan kullanmak yerine factory üzerinden oluştur. Bu testing ve flexibility kazandırır.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir

Senior developer design patterns öğrenirken:

1. **Problem-first approach**: "Bu pattern hangi problemi çözüyor?" — pattern'ı değil problemi öğrenir
2. **Tradeoff analysis**: Her pattern'ın eklediği complexity'yi benefit'iyle karşılaştırır
3. **Language idioms**: Pattern'ın o dildeki idiomatik implementasyonunu bilir (Python'da decorator, JS'de closure)
4. **Refactoring to patterns**: Sıfırdan pattern ile yazmak yerine, gerektiğinde mevcut kodu pattern'a refactor eder
5. **Composition over inheritance**: Modern yaklaşımda inheritance yerine composition tercih eder

**Karar Verme Sureci — Pattern Ne Zaman Kullanilmali?**
- **Singleton**: Global state yonetimi (DB connection pool, logger, config). Trade-off: Test edilmesi zor, hidden dependency olusturur. Modern alternatif: Dependency Injection. "Singleton kullanmadan once DI dusun" kurali.
- **Strategy**: Calisma zamaninda algoritma degistirme (odeme yontemi, siralama). Trade-off: Basit if/else ile cozulebilecek durumda over-engineering. Kural: 3+ strateji varsa veya yeni stratejiler eklenecekse kullan.
- **Observer/Event-driven**: Loose coupling. Trade-off: Debug etmesi zor, event storm olusabilir. Kural: Event sayisi kontrolsuz buyuyorsa event catalog + schema registry kur.
- **Factory**: Karmasik nesne olusturma mantigi. Trade-off: Basit constructor yeterliyken gereksiz soyutlama. Kural: Nesne olusturma mantigi degisebiliyorsa factory kullan.

**Anti-pattern Farkindaligi:**
- **"Pattern-driven development"**: Her kodu bir pattern'e oturtmaya calismak. Basit CRUD uygulamasinda Abstract Factory + Strategy + Observer kullanmak. Sonuc: 50 satirlik is 500 satir oluyor. Kural: "Pattern'i kodun gerektirdigi zaman ekle, onceden degil."
- **Inheritance hierarchy cehennemi**: `BaseService > AuthenticatedService > CRUDService > UserService > AdminUserService`. 5 seviye inheritance, bir method'u override edince 3 seviye yukaridaki davranisi bozuyor. Cozum: Composition + mixins + dependency injection.
- **God Object / God Class**: Tek class'ta 2000+ satir, 50+ method. Production'da gorduk: bir bug fix icin 3 gun harcandi cunku her sey birbiriyle bagli. SRP uygulandiginda 6 kucuk class'a ayrildi, bug 15 dakikada bulundu.

**Gercek Dunya Deneyimi:** Bir odeme sisteminde tek bir `PaymentProcessor` class'i vardi — Stripe, PayPal, havale hepsini handle ediyordu. 2000+ satir, her yeni odeme yontemi regresyon cikartiyordu. Strategy pattern ile refactor ettik: her odeme yontemi ayri class, ortak interface, factory ile secim. Yeni odeme yontemi eklemek 2 gunluk isten 2 saatlik ise donustu. Ders: pattern'i dogru zamanda ekle — ne cok erken ne cok gec.
:::

---

## 1. SOLID Prensipleri

### 1.1 S — Single Responsibility Principle (SRP)

:::concept
## Single Responsibility Principle

**Bir class'ın değişmesi için tek bir nedeni olmalıdır.** Yani bir class tek bir işten sorumlu olmalı.

SRP ihlali genellikle "God Class" (her şeyi yapan dev class) ile sonuçlanır.
:::

:::code
## SRP — Öncesi ve Sonrası

```python
# BAD — SRP ihlali ❌
class UserService:
    def create_user(self, name, email):
        # User oluştur
        user = {"name": name, "email": email}
        # Database'e kaydet (DB responsibility)
        self._save_to_db(user)
        # Email gönder (Notification responsibility)
        self._send_welcome_email(user)
        # Log yaz (Logging responsibility)
        self._write_log(f"User created: {email}")
        # Report oluştur (Reporting responsibility)
        self._update_analytics(user)
        return user

    def _save_to_db(self, user): ...
    def _send_welcome_email(self, user): ...
    def _write_log(self, message): ...
    def _update_analytics(self, user): ...


# GOOD — SRP uygulanmış ✅
class UserService:
    def __init__(self, repo, notifier, logger, analytics):
        self._repo = repo
        self._notifier = notifier
        self._logger = logger
        self._analytics = analytics

    def create_user(self, name: str, email: str) -> dict:
        user = {"name": name, "email": email}
        self._repo.save(user)
        self._notifier.send_welcome(user)
        self._logger.info(f"User created: {email}")
        self._analytics.track("user_created", user)
        return user

class UserRepository:
    """Sadece data persistence"""
    def save(self, user): ...
    def find_by_id(self, user_id): ...

class EmailNotifier:
    """Sadece notification"""
    def send_welcome(self, user): ...

class AppLogger:
    """Sadece logging"""
    def info(self, message): ...

class AnalyticsTracker:
    """Sadece analytics"""
    def track(self, event, data): ...
```

```javascript
// JavaScript — SRP Uygulanmış ✅

// BAD — Tek class her şeyi yapıyor ❌
class UserService {
  createUser(name, email) {
    const user = { name, email };
    db.save(user);                    // DB
    sendEmail(email, 'Welcome!');     // Notification
    console.log(`User created: ${email}`); // Logging
    analytics.track('user_created');  // Analytics
    return user;
  }
}

// GOOD — Her class tek sorumluluk ✅
class UserRepository {
  save(user) { /* DB işlemi */ }
  findById(id) { /* DB sorgusu */ }
}

class EmailNotifier {
  sendWelcome(user) { /* Email gönderimi */ }
}

class AppLogger {
  info(message) { console.log(`[INFO] ${message}`); }
}

class UserService {
  constructor(repo, notifier, logger) {
    this.repo = repo;
    this.notifier = notifier;
    this.logger = logger;
  }

  createUser(name, email) {
    const user = { name, email };
    this.repo.save(user);
    this.notifier.sendWelcome(user);
    this.logger.info(`User created: ${email}`);
    return user;
  }
}
```
:::

### 1.2 O — Open/Closed Principle (OCP)

:::concept
## Open/Closed Principle

**Sınıflar genişletmeye AÇIK, değiştirmeye KAPALI olmalıdır.** Yeni davranış eklemek için mevcut kodu değiştirmek yerine, yeni kod ekle.
:::

:::code
## OCP — Öncesi ve Sonrası

```python
# BAD — Her yeni ödeme yöntemi için mevcut kodu değiştirmek gerekiyor ❌
class PaymentProcessor:
    def process(self, payment_type: str, amount: float):
        if payment_type == "credit_card":
            # Credit card logic
            print(f"Credit card payment: {amount}")
        elif payment_type == "paypal":
            # PayPal logic
            print(f"PayPal payment: {amount}")
        elif payment_type == "crypto":
            # Her yeni tip için buraya ekleme yapılır...
            print(f"Crypto payment: {amount}")
        # elif ... elif ... elif ... SONSUZ if/else!


# GOOD — Yeni ödeme yöntemi = yeni class, mevcut koda dokunma ✅
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool: ...

    @abstractmethod
    def refund(self, amount: float) -> bool: ...

class CreditCardPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        print(f"Processing credit card payment: {amount}")
        return True

    def refund(self, amount: float) -> bool:
        print(f"Refunding credit card: {amount}")
        return True

class PayPalPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        print(f"Processing PayPal payment: {amount}")
        return True

    def refund(self, amount: float) -> bool:
        print(f"Refunding PayPal: {amount}")
        return True

# Yeni ödeme yöntemi eklemek = yeni class yazmak, mevcut koda DOKUNMAMAK
class CryptoPayment(PaymentMethod):
    def process(self, amount: float) -> bool:
        print(f"Processing crypto payment: {amount}")
        return True

    def refund(self, amount: float) -> bool:
        print(f"Refunding crypto: {amount}")
        return True

class PaymentProcessor:
    def process_payment(self, method: PaymentMethod, amount: float):
        return method.process(amount)
```

```javascript
// JavaScript — OCP Uygulanmış ✅

// BAD — Her yeni ödeme yöntemi için if/else eklenmeli ❌
class PaymentProcessor {
  process(type, amount) {
    if (type === 'credit_card') { /* ... */ }
    else if (type === 'paypal') { /* ... */ }
    // Sonsuz if/else!
  }
}

// GOOD — Yeni ödeme yöntemi = yeni class ✅
class CreditCardPayment {
  process(amount) { console.log(`CC payment: ${amount}`); return true; }
  refund(amount) { console.log(`CC refund: ${amount}`); return true; }
}

class PayPalPayment {
  process(amount) { console.log(`PayPal payment: ${amount}`); return true; }
  refund(amount) { console.log(`PayPal refund: ${amount}`); return true; }
}

// Yeni ödeme yöntemi eklemek = yeni class yazmak
class CryptoPayment {
  process(amount) { console.log(`Crypto payment: ${amount}`); return true; }
  refund(amount) { console.log(`Crypto refund: ${amount}`); return true; }
}

function processPayment(method, amount) {
  return method.process(amount);
}

// Kullanim
processPayment(new CreditCardPayment(), 100);
processPayment(new CryptoPayment(), 50);
```
:::

### 1.3 L — Liskov Substitution Principle (LSP)

:::concept
## Liskov Substitution Principle

**Alt sınıflar, üst sınıflarının yerine kullanılabilir olmalıdır.** Yani bir `Bird` bekleyen yere `Penguin` gönderdiğinde program bozulmamalı.
:::

:::code
## LSP — Klasik İhlal Örneği

```python
# BAD — LSP ihlali ❌
class Bird:
    def fly(self):
        return "Flying high!"

class Eagle(Bird):
    def fly(self):
        return "Soaring through the sky!"

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")  # LSP ihlali!

def make_bird_fly(bird: Bird):
    print(bird.fly())  # Penguin gelince patlıyor!


# GOOD — LSP uyumlu ✅
class Bird:
    def move(self):
        raise NotImplementedError

class FlyingBird(Bird):
    def move(self):
        return "Flying!"

    def fly(self):
        return "Taking off!"

class SwimmingBird(Bird):
    def move(self):
        return "Swimming!"

    def swim(self):
        return "Diving in!"

class Eagle(FlyingBird):
    def move(self):
        return "Soaring through the sky!"

class Penguin(SwimmingBird):
    def move(self):
        return "Waddling and swimming!"

def make_bird_move(bird: Bird):
    print(bird.move())  # Her Bird move edebilir, sorun yok!
```

```javascript
// JavaScript — LSP Uyumlu ✅

// BAD — LSP ihlali ❌
class Bird {
  fly() { return "Flying!"; }
}

class Penguin extends Bird {
  fly() { throw new Error("Penguins can't fly!"); } // LSP ihlali!
}

// GOOD — LSP uyumlu ✅
class Bird {
  move() { throw new Error("Subclass must implement"); }
}

class FlyingBird extends Bird {
  move() { return "Flying!"; }
  fly() { return "Taking off!"; }
}

class SwimmingBird extends Bird {
  move() { return "Swimming!"; }
  swim() { return "Diving in!"; }
}

class Eagle extends FlyingBird {
  move() { return "Soaring through the sky!"; }
}

class Penguin extends SwimmingBird {
  move() { return "Waddling and swimming!"; }
}

// Her Bird move() edebilir — sorun yok!
function makeBirdMove(bird) {
  console.log(bird.move());
}

makeBirdMove(new Eagle());   // "Soaring through the sky!"
makeBirdMove(new Penguin()); // "Waddling and swimming!"
```
:::

### 1.4 I — Interface Segregation Principle (ISP)

:::concept
## Interface Segregation Principle

**Client'lar, kullanmadıkları interface'lere bağımlı olmamalıdır.** Büyük, şişman interface'ler yerine küçük, odaklı interface'ler oluştur.
:::

:::code
## ISP — Öncesi ve Sonrası

```python
# BAD — Fat interface ❌
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self): ...

    @abstractmethod
    def eat(self): ...

    @abstractmethod
    def sleep(self): ...

class Robot(Worker):
    def work(self):
        return "Working..."

    def eat(self):
        raise Exception("Robots don't eat!")  # Gereksiz method!

    def sleep(self):
        raise Exception("Robots don't sleep!")  # Gereksiz method!


# GOOD — Segregated interfaces ✅
class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class Sleepable(ABC):
    @abstractmethod
    def sleep(self): ...

class Human(Workable, Eatable, Sleepable):
    def work(self): return "Human working"
    def eat(self): return "Human eating"
    def sleep(self): return "Human sleeping"

class Robot(Workable):  # Sadece work!
    def work(self): return "Robot working 24/7"
```

```javascript
// JavaScript — ISP Uygulanmış ✅

// BAD — Fat interface ❌
class Robot {
  work() { return "Working..."; }
  eat() { throw new Error("Robots don't eat!"); }  // Gereksiz!
  sleep() { throw new Error("Robots don't sleep!"); }  // Gereksiz!
}

// GOOD — Segregated interfaces (mixin pattern ile) ✅
const Workable = {
  work() { return `${this.name} working`; }
};

const Eatable = {
  eat() { return `${this.name} eating`; }
};

const Sleepable = {
  sleep() { return `${this.name} sleeping`; }
};

class Human {
  constructor(name) { this.name = name; }
}
Object.assign(Human.prototype, Workable, Eatable, Sleepable);

class Robot {
  constructor(name) { this.name = name; }
}
Object.assign(Robot.prototype, Workable); // Sadece work!

const human = new Human("Ali");
console.log(human.work());  // "Ali working"
console.log(human.eat());   // "Ali eating"

const robot = new Robot("R2D2");
console.log(robot.work());  // "R2D2 working"
// robot.eat() → undefined (zorunlu değil, hata fırlatmaz)
```
:::

### 1.5 D — Dependency Inversion Principle (DIP)

:::concept
## Dependency Inversion Principle

**Yüksek seviyeli modüller, düşük seviyeli modüllere bağımlı olmamalıdır. İkisi de abstraction'lara bağımlı olmalıdır.**

Kısacası: Concrete class'lara değil, interface/abstract class'lara bağlan.
:::

:::code
## DIP — Öncesi ve Sonrası

```python
# BAD — High-level directly depends on low-level ❌
class MySQLDatabase:
    def query(self, sql):
        return f"MySQL: {sql}"

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Doğrudan MySQL'e bağımlı!

    def get_user(self, user_id):
        return self.db.query(f"SELECT * FROM users WHERE id={user_id}")


# GOOD — Both depend on abstraction ✅
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def query(self, sql: str): ...

class MySQLDatabase(Database):
    def query(self, sql: str):
        return f"MySQL: {sql}"

class PostgreSQLDatabase(Database):
    def query(self, sql: str):
        return f"PostgreSQL: {sql}"

class UserService:
    def __init__(self, db: Database):  # Abstraction'a bağımlı!
        self.db = db

    def get_user(self, user_id: str):
        return self.db.query(f"SELECT * FROM users WHERE id={user_id}")

# İstediğin DB'yi inject et
service_mysql = UserService(MySQLDatabase())
service_pg = UserService(PostgreSQLDatabase())
```

```javascript
// JavaScript — DIP Uygulanmış ✅

// BAD — High-level doğrudan low-level'a bağımlı ❌
class UserService {
  constructor() {
    this.db = new MySQLDatabase(); // Doğrudan MySQL'e bağımlı!
  }
  getUser(id) { return this.db.query(`SELECT * FROM users WHERE id=${id}`); }
}

// GOOD — Abstraction'a bağımlı ✅
// Database "interface" (duck typing ile)
class MySQLDatabase {
  query(sql) { return `MySQL: ${sql}`; }
}

class PostgreSQLDatabase {
  query(sql) { return `PostgreSQL: ${sql}`; }
}

class UserService {
  constructor(db) {  // Abstraction inject edilir
    this.db = db;
  }
  getUser(id) { return this.db.query(`SELECT * FROM users WHERE id=${id}`); }
}

// İstediğin DB'yi inject et
const mysqlService = new UserService(new MySQLDatabase());
const pgService = new UserService(new PostgreSQLDatabase());

console.log(mysqlService.getUser(1));  // "MySQL: SELECT..."
console.log(pgService.getUser(1));     // "PostgreSQL: SELECT..."
```
:::

---

## 2. Creational Patterns — Nesne Oluşturma

### 2.1 Singleton Pattern

:::concept
## Singleton Pattern

**Bir class'tan sadece bir instance oluşturulmasını garantiler** ve bu instance'a global erişim sağlar.

**Ne zaman kullan**: Database connection pool, configuration manager, logger, cache manager
**Dikkat**: Global state oluşturduğu için testing'i zorlaştırabilir!
:::

:::code
## Singleton — Python & JavaScript

```python
# Python — Thread-Safe Singleton
import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-check locking
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.connection = "Connected to DB"
        print("Database connection created (only once!)")

    def query(self, sql: str):
        return f"Executing: {sql}"

# Test
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(f"Same instance: {db1 is db2}")  # True

# Python — Daha Pythonic yol: module-level instance
# config.py
class _Config:
    def __init__(self):
        self.debug = False
        self.db_url = "postgresql://localhost/mydb"

config = _Config()  # Module import edildiğinde bir kez oluşur
```

```javascript
// JavaScript — Singleton with Closure
class Logger {
  static #instance = null;

  constructor() {
    if (Logger.#instance) {
      return Logger.#instance;
    }
    this.logs = [];
    Logger.#instance = this;
  }

  log(message) {
    const entry = `[${new Date().toISOString()}] ${message}`;
    this.logs.push(entry);
    console.log(entry);
  }

  static getInstance() {
    if (!Logger.#instance) {
      new Logger();
    }
    return Logger.#instance;
  }
}

// Test
const logger1 = Logger.getInstance();
const logger2 = Logger.getInstance();
console.log(logger1 === logger2); // true

// Module pattern (daha yaygın JS yaklaşımı)
// logger.js
const logs = [];
export const logger = {
  log: (msg) => { logs.push(msg); console.log(msg); },
  getLogs: () => [...logs],
};
```
:::

### 2.2 Factory Pattern

:::concept
## Factory Pattern

**Object oluşturma logic'ini client'tan gizler.** Client hangi concrete class'ın oluşturulduğunu bilmez, sadece interface'i kullanır.

**Ne zaman kullan**: Oluşturulacak nesne tipi runtime'da belirleniyor, complex initialization gerekiyor, veya nesne oluşturma logic'ini değiştirmek istiyorsan.
:::

:::code
## Factory Pattern — Notification System

```python
from abc import ABC, abstractmethod

# Product interface
class Notification(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> bool: ...

    @abstractmethod
    def get_cost(self) -> float: ...

# Concrete products
class EmailNotification(Notification):
    def send(self, to: str, message: str) -> bool:
        print(f"[EMAIL] To: {to} | Message: {message}")
        return True

    def get_cost(self) -> float:
        return 0.001  # $0.001 per email

class SMSNotification(Notification):
    def send(self, to: str, message: str) -> bool:
        print(f"[SMS] To: {to} | Message: {message[:160]}")
        return True

    def get_cost(self) -> float:
        return 0.05  # $0.05 per SMS

class PushNotification(Notification):
    def send(self, to: str, message: str) -> bool:
        print(f"[PUSH] To: {to} | Message: {message}")
        return True

    def get_cost(self) -> float:
        return 0.0001  # Almost free

class SlackNotification(Notification):
    def send(self, to: str, message: str) -> bool:
        print(f"[SLACK] Channel: {to} | Message: {message}")
        return True

    def get_cost(self) -> float:
        return 0.0  # Free

# Factory
class NotificationFactory:
    """Factory — client hangi class'ın oluşturulduğunu bilmez"""

    _registry: dict[str, type[Notification]] = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
        "slack": SlackNotification,
    }

    @classmethod
    def create(cls, channel: str) -> Notification:
        notification_class = cls._registry.get(channel)
        if not notification_class:
            raise ValueError(f"Unknown channel: {channel}. Available: {list(cls._registry.keys())}")
        return notification_class()

    @classmethod
    def register(cls, channel: str, notification_class: type[Notification]):
        """Yeni notification tipi ekle — OCP uyumlu!"""
        cls._registry[channel] = notification_class

# Kullanım — client concrete class'ları bilmez
def notify_user(channel: str, user: str, message: str):
    notification = NotificationFactory.create(channel)
    notification.send(user, message)
    print(f"  Cost: ${notification.get_cost()}")

notify_user("email", "ali@test.com", "Siparişiniz onaylandı!")
notify_user("sms", "+905551234567", "Kargo yola çıktı")
notify_user("push", "device_token_123", "Yeni kampanya!")
notify_user("slack", "#orders", "Yeni sipariş geldi")
```
:::

---

## 3. Structural Patterns — Yapısal Pattern'lar

### 3.1 Adapter Pattern

:::concept
## Adapter Pattern

**Uyumsuz interface'leri uyumlu hale getirir.** Mevcut bir class'ın interface'ini, client'ın beklediği interface'e dönüştürür. Gerçek hayat: priz adaptörü gibi.

**Ne zaman kullan**: 3rd party library'nin interface'i senin sistemine uymuyor, legacy code'u yeni sisteme entegre ediyorsun.
:::

:::code
## Adapter Pattern — Payment Gateway

```python
from abc import ABC, abstractmethod

# Senin sisteminin beklediği interface
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, currency: str, card_token: str) -> dict: ...

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> dict: ...

# 3rd party library'ler — farklı interface'leri var

class StripeSDK:
    """Stripe'ın kendi SDK'sı — farklı method isimleri"""
    def create_charge(self, amount_cents: int, currency: str, source: str):
        return {"id": "ch_stripe_123", "status": "succeeded", "amount": amount_cents}

    def create_refund(self, charge_id: str, amount_cents: int):
        return {"id": "re_stripe_456", "status": "succeeded"}

class IyzicoSDK:
    """iyzico SDK — tamamen farklı yapı"""
    def initialize_payment(self, price: str, currency: str, card_token: str):
        return {"paymentId": "iyz_789", "status": "SUCCESS", "paidPrice": price}

    def cancel_payment(self, payment_id: str):
        return {"paymentId": payment_id, "status": "SUCCESS"}

# Adapter'lar — uyumsuz interface'leri uyumlu hale getirir

class StripeAdapter(PaymentGateway):
    def __init__(self):
        self._stripe = StripeSDK()

    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        # Stripe cent cinsinden istiyor, biz TL cinsinden veriyoruz
        result = self._stripe.create_charge(
            amount_cents=int(amount * 100),
            currency=currency.lower(),
            source=card_token
        )
        return {
            "transaction_id": result["id"],
            "status": "success" if result["status"] == "succeeded" else "failed",
            "amount": amount
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        result = self._stripe.create_refund(transaction_id, int(amount * 100))
        return {
            "refund_id": result["id"],
            "status": "success" if result["status"] == "succeeded" else "failed"
        }

class IyzicoAdapter(PaymentGateway):
    def __init__(self):
        self._iyzico = IyzicoSDK()

    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        result = self._iyzico.initialize_payment(
            price=str(amount),
            currency=currency,
            card_token=card_token
        )
        return {
            "transaction_id": result["paymentId"],
            "status": "success" if result["status"] == "SUCCESS" else "failed",
            "amount": float(result["paidPrice"])
        }

    def refund(self, transaction_id: str, amount: float) -> dict:
        result = self._iyzico.cancel_payment(transaction_id)
        return {
            "refund_id": result["paymentId"],
            "status": "success" if result["status"] == "SUCCESS" else "failed"
        }

# Client — adapter sayesinde hangi payment provider olduğunu bilmez
def process_payment(gateway: PaymentGateway, amount: float):
    result = gateway.charge(amount, "TRY", "card_token_xxx")
    print(f"Payment: {result}")
    return result

# Stripe ile
process_payment(StripeAdapter(), 150.00)

# iyzico ile — aynı client code!
process_payment(IyzicoAdapter(), 150.00)
```
:::

### 3.2 Decorator Pattern

:::concept
## Decorator Pattern

**Bir nesneye runtime'da yeni davranışlar ekler** — miras (inheritance) kullanmadan. Sarmalama (wrapping) prensibiyle çalışır.

**Ne zaman kullan**: Mevcut class'a yeni özellikler eklemek ama class'ı değiştirmemek istiyorsan, özellik kombinasyonları çok fazlaysa (inheritance explosion).
:::

:::code
## Decorator Pattern — Logger Enhancement

```python
from abc import ABC, abstractmethod
from datetime import datetime
import json
import time

# Base interface
class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None: ...

# Concrete component
class ConsoleLogger(Logger):
    def log(self, message: str) -> None:
        print(message)

# Decorators — her biri yeni davranış ekler

class TimestampDecorator(Logger):
    def __init__(self, logger: Logger):
        self._logger = logger

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._logger.log(f"[{timestamp}] {message}")

class JsonDecorator(Logger):
    def __init__(self, logger: Logger):
        self._logger = logger

    def log(self, message: str) -> None:
        log_entry = json.dumps({"message": message, "level": "INFO"})
        self._logger.log(log_entry)

class UpperCaseDecorator(Logger):
    def __init__(self, logger: Logger):
        self._logger = logger

    def log(self, message: str) -> None:
        self._logger.log(message.upper())

# Decorator'ları compose et
logger = ConsoleLogger()
logger.log("Basic log")
# Output: Basic log

logger_with_ts = TimestampDecorator(ConsoleLogger())
logger_with_ts.log("With timestamp")
# Output: [2024-01-15 14:30:00] With timestamp

# Decorator'ları chain'le!
fancy_logger = TimestampDecorator(UpperCaseDecorator(ConsoleLogger()))
fancy_logger.log("chained decorators")
# Output: [2024-01-15 14:30:00] CHAINED DECORATORS
```

```javascript
// JavaScript — Function Decorator Pattern
function withLogging(fn) {
  return function (...args) {
    console.log(`Calling ${fn.name} with args:`, args);
    const result = fn(...args);
    console.log(`${fn.name} returned:`, result);
    return result;
  };
}

function withTiming(fn) {
  return function (...args) {
    const start = performance.now();
    const result = fn(...args);
    const elapsed = performance.now() - start;
    console.log(`${fn.name} took ${elapsed.toFixed(2)}ms`);
    return result;
  };
}

function withRetry(fn, maxRetries = 3) {
  return function (...args) {
    for (let i = 0; i < maxRetries; i++) {
      try {
        return fn(...args);
      } catch (error) {
        console.log(`Retry ${i + 1}/${maxRetries} for ${fn.name}`);
        if (i === maxRetries - 1) throw error;
      }
    }
  };
}

// Compose decorators
function fetchData(url) {
  // Simulate API call
  return { data: "result", url };
}

const enhancedFetch = withTiming(withLogging(withRetry(fetchData)));
enhancedFetch("https://api.example.com/data");
```
:::

---

## 4. Behavioral Patterns — Davranışsal Pattern'lar

### 4.1 Strategy Pattern

:::concept
## Strategy Pattern

**Bir algoritma ailesini tanımlar, her birini encapsulate eder ve runtime'da birbiriyle değiştirilebilir yapar.** if/else zincirlerinin OCP-uyumlu alternatifi.

**Ne zaman kullan**: Birden fazla algoritma/davranış var ve runtime'da seçim gerekiyor. Discount hesaplama, sorting algoritması seçimi, validation stratejileri.
:::

:::code
## Strategy Pattern — Discount System

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Strategy interface
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, price: float) -> float:
        """İndirimli fiyatı döndür"""
        ...

    @abstractmethod
    def description(self) -> str: ...

# Concrete strategies
class NoDiscount(DiscountStrategy):
    def calculate(self, price: float) -> float:
        return price

    def description(self) -> str:
        return "No discount"

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self._percentage = percentage

    def calculate(self, price: float) -> float:
        return price * (1 - self._percentage / 100)

    def description(self) -> str:
        return f"{self._percentage}% discount"

class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self._amount = amount

    def calculate(self, price: float) -> float:
        return max(0, price - self._amount)

    def description(self) -> str:
        return f"{self._amount} TL discount"

class BuyOneGetOneFree(DiscountStrategy):
    def calculate(self, price: float) -> float:
        return price / 2

    def description(self) -> str:
        return "Buy 1 Get 1 Free"

class VIPDiscount(DiscountStrategy):
    """VIP müşteri: %20 indirim + min 50 TL indirim garanti"""
    def calculate(self, price: float) -> float:
        percentage_price = price * 0.80
        fixed_price = price - 50
        return min(percentage_price, fixed_price)  # Hangisi daha avantajlıysa

    def description(self) -> str:
        return "VIP Discount (best of 20% or 50 TL off)"

# Context — strategy'yi kullanan class
@dataclass
class ShoppingCart:
    items: list[dict]
    discount_strategy: DiscountStrategy = None

    def __post_init__(self):
        if self.discount_strategy is None:
            self.discount_strategy = NoDiscount()

    @property
    def subtotal(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)

    @property
    def total(self) -> float:
        return self.discount_strategy.calculate(self.subtotal)

    @property
    def savings(self) -> float:
        return self.subtotal - self.total

    def set_discount(self, strategy: DiscountStrategy):
        """Runtime'da strategy değiştir"""
        self.discount_strategy = strategy

    def checkout_summary(self):
        print(f"Subtotal:  {self.subtotal:.2f} TL")
        print(f"Discount:  {self.discount_strategy.description()}")
        print(f"Savings:   -{self.savings:.2f} TL")
        print(f"Total:     {self.total:.2f} TL")

# Kullanım
cart = ShoppingCart(items=[
    {"name": "Laptop", "price": 15000, "quantity": 1},
    {"name": "Mouse", "price": 500, "quantity": 2},
])

print("=== No Discount ===")
cart.checkout_summary()

print("\n=== 10% Off ===")
cart.set_discount(PercentageDiscount(10))
cart.checkout_summary()

print("\n=== VIP Customer ===")
cart.set_discount(VIPDiscount())
cart.checkout_summary()

print("\n=== BOGO ===")
cart.set_discount(BuyOneGetOneFree())
cart.checkout_summary()
```
:::

### 4.2 Observer Pattern

:::concept
## Observer Pattern

**Bir nesnedeki değişikliği, ona bağlı tüm nesnelere otomatik olarak bildirir.** Publish-subscribe mekanizmasının temelidir.

**Ne zaman kullan**: Bir değişiklik birden fazla yeri etkiliyorsa. Event system, state management, real-time updates.
:::

:::code
## Observer Pattern — Event System

```python
from abc import ABC, abstractmethod
from typing import Callable
from dataclasses import dataclass, field

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data: dict) -> None: ...

# Subject (Observable)
class EventEmitter:
    """Generic event system — Node.js EventEmitter benzeri"""

    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable):
        """Event'e listener ekle"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
        return self  # Method chaining

    def off(self, event: str, callback: Callable):
        """Listener'ı kaldır"""
        if event in self._listeners:
            self._listeners[event].remove(callback)
        return self

    def emit(self, event: str, data: dict = None):
        """Event'i tüm listener'lara bildir"""
        for callback in self._listeners.get(event, []):
            callback(data or {})

    def once(self, event: str, callback: Callable):
        """Sadece bir kez çalışan listener"""
        def wrapper(data):
            callback(data)
            self.off(event, wrapper)
        self.on(event, wrapper)

# Kullanım — E-commerce Order System
class OrderSystem(EventEmitter):
    def __init__(self):
        super().__init__()
        self._orders = {}

    def create_order(self, order_id: str, user_id: str, total: float):
        order = {"order_id": order_id, "user_id": user_id, "total": total, "status": "created"}
        self._orders[order_id] = order
        self.emit("order:created", order)
        return order

    def complete_order(self, order_id: str):
        order = self._orders[order_id]
        order["status"] = "completed"
        self.emit("order:completed", order)

    def cancel_order(self, order_id: str, reason: str):
        order = self._orders[order_id]
        order["status"] = "cancelled"
        order["cancel_reason"] = reason
        self.emit("order:cancelled", order)

# Observers (listeners)
def email_notification(data):
    print(f"[Email] Order {data['order_id']} notification sent to user {data['user_id']}")

def inventory_update(data):
    print(f"[Inventory] Updating stock for order {data['order_id']}")

def analytics_track(data):
    print(f"[Analytics] Tracking order {data['order_id']}: {data['status']}")

def accounting_record(data):
    print(f"[Accounting] Recording {data['total']} TL for order {data['order_id']}")

# Wire up
system = OrderSystem()
system.on("order:created", email_notification)
system.on("order:created", inventory_update)
system.on("order:created", analytics_track)
system.on("order:created", accounting_record)
system.on("order:completed", email_notification)
system.on("order:completed", analytics_track)
system.on("order:cancelled", email_notification)
system.on("order:cancelled", inventory_update)  # Stok geri ekleme

# Test
print("=== Creating Order ===")
system.create_order("ord_001", "user_123", 15000)

print("\n=== Completing Order ===")
system.complete_order("ord_001")
```
:::

### 4.3 Command Pattern

:::concept
## Command Pattern

**Bir isteği (request) bir nesne olarak encapsulate eder.** Bu sayede undo/redo, queue, logging gibi özellikler eklenebilir.

**Ne zaman kullan**: Undo/redo desteği, command queue, macro recording, transaction management.
:::

:::code
## Command Pattern — Undo/Redo Text Editor

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...

class TextEditor:
    def __init__(self):
        self.content = ""
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: "Command"):
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self):
        if not self._history:
            print("Nothing to undo!")
            return
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self):
        if not self._redo_stack:
            print("Nothing to redo!")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)

class InsertTextCommand(Command):
    def __init__(self, editor: TextEditor, text: str, position: int):
        self._editor = editor
        self._text = text
        self._position = position

    def execute(self):
        self._editor.content = (
            self._editor.content[:self._position]
            + self._text
            + self._editor.content[self._position:]
        )

    def undo(self):
        self._editor.content = (
            self._editor.content[:self._position]
            + self._editor.content[self._position + len(self._text):]
        )

class DeleteTextCommand(Command):
    def __init__(self, editor: TextEditor, position: int, length: int):
        self._editor = editor
        self._position = position
        self._length = length
        self._deleted_text = ""

    def execute(self):
        self._deleted_text = self._editor.content[self._position:self._position + self._length]
        self._editor.content = (
            self._editor.content[:self._position]
            + self._editor.content[self._position + self._length:]
        )

    def undo(self):
        self._editor.content = (
            self._editor.content[:self._position]
            + self._deleted_text
            + self._editor.content[self._position:]
        )

# Test
editor = TextEditor()

editor.execute(InsertTextCommand(editor, "Hello ", 0))
print(f"After insert: '{editor.content}'")  # "Hello "

editor.execute(InsertTextCommand(editor, "World", 6))
print(f"After insert: '{editor.content}'")  # "Hello World"

editor.undo()
print(f"After undo:   '{editor.content}'")  # "Hello "

editor.redo()
print(f"After redo:   '{editor.content}'")  # "Hello World"

editor.execute(DeleteTextCommand(editor, 5, 6))
print(f"After delete: '{editor.content}'")  # "Hello"

editor.undo()
print(f"After undo:   '{editor.content}'")  # "Hello World"
```
:::

---

## 5. Anti-Patterns — Ne Yapmamalı

:::warning
## Yaygın Anti-Patterns

### 1. God Object / God Class
Tek bir class her şeyi yapıyor. Binlerce satır, düzinelerce method.
**Çözüm**: SRP uygula, class'ı sorumluluklar bazında böl.

### 2. Spaghetti Code
Kontrol akışı karmaşık, goto benzeri atlamalar, iç içe callback'ler.
**Çözüm**: Fonksiyonlara böl, design pattern uygula.

### 3. Golden Hammer
"Her şeyi X ile çözerim" — favori tool/pattern her yerde kullanılıyor.
**Çözüm**: Probleme göre araç seç, "when to use" kriterlerini öğren.

### 4. Premature Optimization
Henüz performans problemi olmadan optimize etmek.
**Çözüm**: "Make it work, make it right, make it fast" — bu sırayla.

### 5. Over-Engineering
Basit problemlere karmaşık çözümler — 3 class'lık iş için 15 class, 5 interface, 3 abstract class.
**Çözüm**: YAGNI (You Aren't Gonna Need It). Şu an gerekmeyen şeyi yapma.

### 6. Copy-Paste Programming
Kodu kopyalayıp yapıştırarak geliştirme. Bir yerde fix, diğer 10 yerde unutma.
**Çözüm**: DRY (Don't Repeat Yourself). Ortak logic'i extract et.

### 7. Cargo Cult Programming
Neden kullanıldığını anlamadan pattern/practice kopyalamak.
**Çözüm**: Her pattern'ın "hangi problemi çözdüğünü" öğren.
:::

:::beginner-mistake
## Pattern Seçim Hataları

**Hata 1: Her yere Singleton koymak**
Singleton global state demek = testing nightmare. Dependency injection tercih et.

**Hata 2: Inheritance over composition**
"is-a" ilişkisi yoksa inheritance kullanma. "has-a" ilişkisinde composition kullan.

**Hata 3: Pattern'ı probleme uymadan zorlamak**
Pattern problemi çözmek için var, koda pattern koymak için değil.

**Hata 4: Abstract sınıf kullanmadan doğrudan concrete class'a bağlanmak**
Bağımlılıkları interface üzerinden yönet, test edilebilirlik artar.
:::

---

## 6. Pattern'lar Birlikte Nasıl Çalışır?

:::code
## Composite Example: Strategy + Factory + Observer

```python
from abc import ABC, abstractmethod
from typing import Callable

# === Strategy: Pricing Algorithms ===
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base_price: float, quantity: int) -> float: ...

class StandardPricing(PricingStrategy):
    def calculate(self, base_price: float, quantity: int) -> float:
        return base_price * quantity

class BulkPricing(PricingStrategy):
    def calculate(self, base_price: float, quantity: int) -> float:
        discount = 0.1 if quantity >= 10 else 0.05 if quantity >= 5 else 0
        return base_price * quantity * (1 - discount)

class PremiumPricing(PricingStrategy):
    def calculate(self, base_price: float, quantity: int) -> float:
        return base_price * quantity * 1.2  # %20 premium markup

# === Factory: Strategy Selection ===
class PricingFactory:
    @staticmethod
    def create(customer_type: str) -> PricingStrategy:
        strategies = {
            "standard": StandardPricing,
            "bulk": BulkPricing,
            "premium": PremiumPricing,
        }
        cls = strategies.get(customer_type, StandardPricing)
        return cls()

# === Observer: Price Change Notifications ===
class PriceObserver:
    def __init__(self):
        self._listeners: list[Callable] = []

    def subscribe(self, listener: Callable):
        self._listeners.append(listener)

    def notify(self, event: dict):
        for listener in self._listeners:
            listener(event)

# === Orchestration ===
class OrderProcessor:
    def __init__(self):
        self.observer = PriceObserver()

    def process(self, customer_type: str, product: str, base_price: float, quantity: int):
        # Factory — doğru strategy'yi seç
        strategy = PricingFactory.create(customer_type)

        # Strategy — fiyat hesapla
        total = strategy.calculate(base_price, quantity)

        order = {
            "product": product,
            "customer_type": customer_type,
            "base_price": base_price,
            "quantity": quantity,
            "total": total,
            "strategy": strategy.__class__.__name__
        }

        # Observer — notify
        self.observer.notify(order)

        return order

# Setup
processor = OrderProcessor()
processor.observer.subscribe(
    lambda e: print(f"[LOG] {e['product']}: {e['total']:.2f} TL ({e['strategy']})")
)
processor.observer.subscribe(
    lambda e: print(f"[ANALYTICS] Customer type: {e['customer_type']}, Total: {e['total']:.2f}")
)

# Test
processor.process("standard", "Widget", 100, 3)
processor.process("bulk", "Widget", 100, 15)
processor.process("premium", "Widget", 100, 2)
```
:::

---

## 7. JavaScript/TypeScript'te Patterns

:::code
## Modern JavaScript Design Patterns

```javascript
// === Strategy Pattern with Functions ===
// JS'de class gerekmez — fonksiyonlar first-class citizen!

const strategies = {
  percentage: (price, discount) => price * (1 - discount / 100),
  fixed: (price, amount) => Math.max(0, price - amount),
  bogo: (price) => price / 2,
};

function applyDiscount(strategy, price, ...args) {
  const fn = strategies[strategy];
  if (!fn) throw new Error(`Unknown strategy: ${strategy}`);
  return fn(price, ...args);
}

console.log(applyDiscount("percentage", 1000, 10)); // 900
console.log(applyDiscount("fixed", 1000, 150));      // 850
console.log(applyDiscount("bogo", 1000));             // 500


// === Observer Pattern — Custom EventEmitter ===
class EventEmitter {
  #listeners = new Map();

  on(event, callback) {
    if (!this.#listeners.has(event)) {
      this.#listeners.set(event, []);
    }
    this.#listeners.get(event).push(callback);
    return () => this.off(event, callback); // Return unsubscribe function
  }

  off(event, callback) {
    const callbacks = this.#listeners.get(event);
    if (callbacks) {
      const index = callbacks.indexOf(callback);
      if (index > -1) callbacks.splice(index, 1);
    }
  }

  emit(event, data) {
    const callbacks = this.#listeners.get(event) || [];
    callbacks.forEach((cb) => cb(data));
  }
}

// Usage
const emitter = new EventEmitter();
const unsubscribe = emitter.on("userCreated", (user) => {
  console.log(`Welcome email sent to ${user.email}`);
});
emitter.emit("userCreated", { email: "ali@test.com" });
unsubscribe(); // Cleanup


// === Middleware Pattern (Express.js style) ===
function createPipeline() {
  const middlewares = [];

  return {
    use(fn) {
      middlewares.push(fn);
    },
    async execute(context) {
      let index = 0;

      async function next() {
        if (index < middlewares.length) {
          const middleware = middlewares[index++];
          await middleware(context, next);
        }
      }

      await next();
      return context;
    },
  };
}

const pipeline = createPipeline();

pipeline.use(async (ctx, next) => {
  console.log("Auth check...");
  ctx.user = { id: 1, role: "admin" };
  await next();
});

pipeline.use(async (ctx, next) => {
  console.log("Logging...");
  ctx.timestamp = Date.now();
  await next();
});

pipeline.use(async (ctx, next) => {
  console.log("Handler: processing request");
  ctx.result = "Success";
  await next();
});

pipeline.execute({}).then((ctx) => console.log("Final:", ctx));
```
:::

---

## 8. Hands-On Exercise

:::exercise
## Mini Proje: Refactoring with Patterns

Aşağıdaki "kötü kodu" design pattern'larla refactor et:

### Mevcut Kod (Kötü):
```python
class OrderProcessor:
    def process_order(self, order):
        # Fiyat hesaplama — if/else cehennemi
        if order["customer_type"] == "regular":
            total = order["price"] * order["quantity"]
        elif order["customer_type"] == "premium":
            total = order["price"] * order["quantity"] * 0.9
        elif order["customer_type"] == "vip":
            total = order["price"] * order["quantity"] * 0.8
        elif order["customer_type"] == "wholesale":
            if order["quantity"] >= 100:
                total = order["price"] * order["quantity"] * 0.6
            else:
                total = order["price"] * order["quantity"] * 0.75

        # Notification — if/else cehennemi
        if order["notify_via"] == "email":
            print(f"Email sent: Order total {total}")
        elif order["notify_via"] == "sms":
            print(f"SMS sent: Order total {total}")
        elif order["notify_via"] == "push":
            print(f"Push notification: Order total {total}")
        elif order["notify_via"] == "slack":
            print(f"Slack message: Order total {total}")

        # Logging — hardcoded
        print(f"LOG: Order processed, total={total}")

        # Analytics — hardcoded
        print(f"ANALYTICS: revenue={total}")

        return total
```

### Refactored Edilmiş Kod Gereksinimleri:
1. **Strategy Pattern**: Pricing logic'i strategy olarak ayır
2. **Factory Pattern**: Strategy'leri factory ile oluştur
3. **Observer Pattern**: Notification, logging, analytics'i observer olarak ekle
4. **SRP**: Her class tek sorumluluk
5. **OCP**: Yeni pricing veya notification tipi eklemek mevcut kodu değiştirmemeli
6. **DIP**: Concrete class'lara değil, interface'lere bağlan

### Test Senaryoları:
```python
processor = OrderProcessor(...)

# Farklı müşteri tipleri
processor.process({"customer_type": "vip", "price": 100, "quantity": 5})
processor.process({"customer_type": "wholesale", "price": 100, "quantity": 150})

# Yeni pricing strategy ekleme (mevcut koda dokunmadan)
# Yeni notification channel ekleme (mevcut koda dokunmadan)
```

---

### Alıştırma 2: Observer Pattern — Event System (Orta)

Bir bildirim servisi için event-driven mimari oluştur:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

class EventType(Enum):
    USER_REGISTERED = "user_registered"
    ORDER_PLACED = "order_placed"
    PAYMENT_COMPLETED = "payment_completed"
    ORDER_SHIPPED = "order_shipped"

@dataclass
class Event:
    type: EventType
    data: dict
    timestamp: str  # ISO format

# TODO: EventBus class'ı oluştur
class EventBus:
    """Publish-Subscribe event sistemi"""

    def __init__(self):
        # TODO: event_type → list[handler] mapping'i tut
        pass

    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Bir event type'a handler kaydet"""
        # TODO: Implement
        pass

    def unsubscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        """Handler kaydını sil"""
        # TODO: Implement
        pass

    def publish(self, event: Event):
        """Event'i tüm subscriber'lara gönder"""
        # TODO: Implement — handler hata fırlatırsa diğerleri etkilenmemeli
        pass

# Handler'lar (her biri bağımsız bir modül gibi düşün):
def email_handler(event: Event):
    print(f"📧 Email gönderildi: {event.type.value} → {event.data}")

def sms_handler(event: Event):
    print(f"📱 SMS gönderildi: {event.type.value} → {event.data}")

def analytics_handler(event: Event):
    print(f"📊 Analytics kaydedildi: {event.type.value}")

def inventory_handler(event: Event):
    if event.type == EventType.ORDER_PLACED:
        print(f"📦 Stok güncellendi: {event.data.get('product_id')}")

# Test senaryosu:
bus = EventBus()
bus.subscribe(EventType.USER_REGISTERED, email_handler)
bus.subscribe(EventType.ORDER_PLACED, email_handler)
bus.subscribe(EventType.ORDER_PLACED, sms_handler)
bus.subscribe(EventType.ORDER_PLACED, inventory_handler)
bus.subscribe(EventType.PAYMENT_COMPLETED, analytics_handler)

# Bu event yayınlandığında hangi handler'lar çağrılmalı?
bus.publish(Event(
    type=EventType.ORDER_PLACED,
    data={"order_id": 123, "product_id": "P001", "user": "Ahmet"},
    timestamp="2026-03-21T10:30:00"
))
# Beklenen: email_handler, sms_handler, inventory_handler çağrılmalı
```

**Beklenen sonuç:** EventBus loosely coupled olmalı. Yeni handler eklemek mevcut kodu değiştirmemeli (OCP). Handler hatası diğer handler'ları durdurmamalı.

---

### Alıştırma 3: Repository + Unit of Work Pattern (Zor)

Veritabanı erişimini soyutlayan pattern'ları implement et:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass
class User:
    id: int | None
    name: str
    email: str

@dataclass
class Product:
    id: int | None
    name: str
    price: float

# TODO: Generic Repository interface'i tanımla
class Repository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: int) -> T | None: ...

    @abstractmethod
    def get_all(self) -> list[T]: ...

    @abstractmethod
    def add(self, entity: T) -> T: ...

    @abstractmethod
    def update(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, id: int) -> bool: ...

# TODO: In-Memory implementasyon (test için)
class InMemoryUserRepository(Repository[User]):
    def __init__(self):
        self._store: dict[int, User] = {}
        self._next_id = 1
    # TODO: Tüm metodları implement et

# TODO: Unit of Work pattern'ı
class UnitOfWork:
    """Transaction yönetimi — ya hepsi başarılı ya hiçbiri"""
    def __init__(self):
        self._new: list = []
        self._dirty: list = []
        self._deleted: list = []

    def register_new(self, entity): ...
    def register_dirty(self, entity): ...
    def register_deleted(self, entity): ...
    def commit(self): ...
    def rollback(self): ...

# TODO: Service layer (Repository + UoW kullanarak)
class UserService:
    def __init__(self, repo: Repository[User], uow: UnitOfWork):
        self.repo = repo
        self.uow = uow

    def create_user(self, name: str, email: str) -> User:
        # TODO: Implement (email unique olmalı)
        pass

    def transfer_ownership(self, from_user_id: int, to_user_id: int, product_id: int):
        # TODO: İki kullanıcı arasında ürün transferi (UoW ile atomik)
        pass

# Test:
repo = InMemoryUserRepository()
uow = UnitOfWork()
service = UserService(repo, uow)

user1 = service.create_user("Ahmet", "ahmet@mail.com")
user2 = service.create_user("Mehmet", "mehmet@mail.com")
# service.create_user("Ayse", "ahmet@mail.com") → ValueError (duplicate email)
assert repo.get_all() == [user1, user2]
```

**Beklenen sonuç:** Repository pattern ile data access soyutlanmalı. InMemory implementasyon testlerde kullanılabilir olmalı. UnitOfWork ile birden fazla değişiklik atomik olarak commit/rollback edilebilmeli.
:::

:::interview
## Mülakat Soruları — Junior vs Senior Cevap Karşılaştırması

**S1**: "SOLID prensiplerini açıklayın ve gerçek bir projede nasıl uyguladığınızı anlatın."

**Junior cevap**: "S single responsibility, O open closed..." (tanımları sayar ama gerçek örnek veremez)

**Senior cevap**: Her prensibi kısaca açıklar + bir gerçek örnek verir. SRP: "User class'ını UserService ve UserRepository olarak ayırdım — test yazarken DB'yi mock'lamak çok kolaylaştı." OCP: "Yeni ödeme yöntemi eklerken PaymentStrategy interface'i kullandım, mevcut koda dokunmadan iyzico entegrasyonunu 2 saatte bitirdim." DIP: "Database'e doğrudan bağlanmak yerine Repository interface'i inject ettim — PostgreSQL'den MongoDB'ye geçişte sadece adapter değiştirdim."

---

**S2**: "Strategy pattern ne zaman kullanılır? Observer pattern'dan farkı nedir?"

**Junior cevap**: "Strategy if/else yerine kullanılır. Observer event'ler için."

**Senior cevap**: Strategy: Birden fazla algoritma arasında runtime'da seçim. 1-1 ilişki — bir context bir strategy kullanır. Observer: Bir değişikliği birden fazla yere bildirme. 1-N ilişki — bir subject'in birden fazla observer'ı olabilir. Gerçek dünyada ikisi birlikte kullanılır: Strategy ile pricing algoritması seçilir, Observer ile fiyat değişikliği analytics, notification ve inventory service'lerine bildirilir.

---

**S3**: "Over-engineering nedir? Nasıl önlersin?"

**Junior cevap**: "Çok fazla kod yazmak."

**Senior cevap**: "Basit bir probleme gereksiz karmaşık çözüm uygulamak. Örneğin 3 endpoint'lik bir API'ye Abstract Factory + Strategy + Observer + CQRS uygulamak. YAGNI (You Aren't Gonna Need It) prensibi ile önlerim. Refactoring-to-patterns yaklaşımını tercih ederim: önce basit yaz, karmaşıklık arttığında pattern uygula. Martin Fowler'ın dediği gibi: 'Rule of three — aynı şeyi 3. kez yaparken refactor et.'"

---

**S4**: "Dependency Injection nedir? Neden önemlidir?"

**Junior cevap**: "Constructor'a parametre geçmek."

**Senior cevap**: "DI, bağımlılıkları dışarıdan inject etme prensibidir. Bunu yapmazsanız class'lar birbirine sıkı bağlı olur (tight coupling) ve test edemezsiniz. DI ile UserService'in database'ini test ortamında InMemoryRepository ile değiştirebilirim — gerçek DB'ye ihtiyaç duymadan. Production'da ise PostgresRepository inject ederim. DI container'lar (Python'da dependency-injector, JS'de InversifyJS) bunu otomatize eder."
:::

:::exercise
## Ek Pratik Alıştırmalar

### Alıştırma 4: Decorator Pattern — API Middleware
Bir REST API için Decorator pattern ile middleware zinciri oluşturun. Her decorator bağımsız ve compose edilebilir olmalı:

```python
# Aşağıdaki decorator'ları implement edin:
# 1. AuthDecorator — JWT token kontrolü
# 2. LoggingDecorator — request/response logging
# 3. CachingDecorator — GET request sonuçlarını cache'leme
# 4. RateLimitDecorator — IP bazlı rate limiting
#
# Compose edilmiş hali:
# handler = RateLimitDecorator(
#     AuthDecorator(
#         CachingDecorator(
#             LoggingDecorator(actual_handler)
#         )
#     )
# )
#
# Her decorator'ın sorumluluğu tekil olmalı (SRP)
# Yeni decorator eklemek mevcut kodu değiştirmemeli (OCP)
```

### Alıştırma 5: Pattern Tanıma
Aşağıdaki gerçek dünya senaryolarında hangi design pattern kullanılmalı? Her biri için neden o pattern'ı seçtiğinizi açıklayın:

1. E-ticaret sitesinde farklı kargo firmaları (Yurtiçi, MNG, Aras) arasında seçim
2. Bir text editor'de Ctrl+Z ile geri alma özelliği
3. Birden fazla log kaynağından (file, console, database) aynı anda log yazma
4. Farklı veritabanları (MySQL, PostgreSQL, MongoDB) ile çalışabilen bir ORM katmanı
5. Bir e-posta gönderme sisteminde retry mekanizması ve rate limiting ekleme
6. Kullanıcı kaydı sonrası email gönderme, analytics kaydetme ve stok güncelleme

**Beklenen cevaplar:** (1) Strategy, (2) Command, (3) Observer veya Strategy, (4) Adapter + Factory, (5) Decorator, (6) Observer/Event-driven

---

### Alıştırma 6: Command Pattern — Undo/Redo Sistemi (Orta)

Bir text editor icin command pattern ile undo/redo ozelligini implement edin.

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self): pass
    @abstractmethod
    def undo(self): pass

class TextEditor:
    def __init__(self):
        self.content = ""
        self.history = []
        self.redo_stack = []

    def execute(self, command):
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()

    def undo(self):
        if self.history:
            cmd = self.history.pop()
            cmd.undo()
            self.redo_stack.append(cmd)

    def redo(self):
        if self.redo_stack:
            cmd = self.redo_stack.pop()
            cmd.execute()
            self.history.append(cmd)

class InsertTextCommand(Command):
    def __init__(self, editor, text, position):
        self.editor = editor
        self.text = text
        self.position = position

    def execute(self):
        self.editor.content = (
            self.editor.content[:self.position] +
            self.text +
            self.editor.content[self.position:]
        )

    def undo(self):
        self.editor.content = (
            self.editor.content[:self.position] +
            self.editor.content[self.position + len(self.text):]
        )

# TODO: DeleteTextCommand implement et
# TODO: ReplaceTextCommand implement et
# TODO: Macro command ekle (birden fazla komutu tek undo ile geri al)
# TODO: History limit ekle (max 50 undo)

editor = TextEditor()
editor.execute(InsertTextCommand(editor, "Hello ", 0))
editor.execute(InsertTextCommand(editor, "World", 6))
print(editor.content)  # "Hello World"
editor.undo()
print(editor.content)  # "Hello "
editor.redo()
print(editor.content)  # "Hello World"
```

**Beklenen Sonuc:** Undo ve redo sinirsiz sayida calismali. Macro command birden fazla islemi tek adimda geri alabilmeli.
**Ipucu:** Command pattern her islemi nesne olarak saklar. Bu sayede undo, redo, replay ve audit trail mumkun olur.

---

### Alıştırma 7: Factory + Strategy — Odeme Sistemi (Orta)

Factory ve Strategy pattern'larini birlikte kullanarak genisletilebilir bir odeme sistemi tasarlayin.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PaymentResult:
    success: bool
    transaction_id: str
    message: str

class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, amount: float) -> PaymentResult: pass
    @abstractmethod
    def refund(self, transaction_id: str) -> PaymentResult: pass

class CreditCardPayment(PaymentStrategy):
    def process(self, amount):
        # Kredi karti odeme islemi
        return PaymentResult(True, "CC-12345", f"{amount} TL kredi karti ile odendi")
    def refund(self, transaction_id):
        return PaymentResult(True, transaction_id, "Iade yapildi")

class PaymentFactory:
    _strategies = {}

    @classmethod
    def register(cls, name, strategy_class):
        cls._strategies[name] = strategy_class

    @classmethod
    def create(cls, name) -> PaymentStrategy:
        if name not in cls._strategies:
            raise ValueError(f"Bilinmeyen odeme yontemi: {name}")
        return cls._strategies[name]()

PaymentFactory.register("credit_card", CreditCardPayment)

# TODO: BankTransferPayment implement et ve register et
# TODO: DigitalWalletPayment implement et (Papara, Tosla)
# TODO: PaymentProcessor class'i yaz (strategy secimi + validation + logging)
# TODO: Yeni odeme yontemi eklemek icin mevcut kodu DEGISTIRMEDEN sadece register et (OCP)
```

**Beklenen Sonuc:** Yeni odeme yontemi eklemek sadece yeni class + register gerektirmeli. Mevcut kod degistirilmemeli (Open/Closed Principle).

---

### Alıştırma 8: Builder Pattern — Query Builder (Zor)

Karmasik SQL sorgulari olusturmak icin fluent API ile builder pattern implement edin.

```python
class QueryBuilder:
    def __init__(self):
        self._select = []
        self._from = ""
        self._where = []
        self._join = []
        self._order_by = []
        self._limit = None
        self._offset = None
        self._params = []

    def select(self, *columns):
        self._select.extend(columns)
        return self

    def from_table(self, table):
        self._from = table
        return self

    def where(self, condition, *params):
        self._where.append(condition)
        self._params.extend(params)
        return self

    def join(self, table, on):
        self._join.append(f"JOIN {table} ON {on}")
        return self

    def order_by(self, column, direction="ASC"):
        self._order_by.append(f"{column} {direction}")
        return self

    def limit(self, n):
        self._limit = n
        return self

    def build(self):
        parts = [f"SELECT {', '.join(self._select) or '*'}"]
        parts.append(f"FROM {self._from}")
        parts.extend(self._join)
        if self._where:
            parts.append(f"WHERE {' AND '.join(self._where)}")
        if self._order_by:
            parts.append(f"ORDER BY {', '.join(self._order_by)}")
        if self._limit:
            parts.append(f"LIMIT {self._limit}")
        return " ".join(parts), self._params

# Kullanim
query, params = (QueryBuilder()
    .select("u.name", "u.email", "COUNT(o.id) as order_count")
    .from_table("users u")
    .join("orders o", "u.id = o.user_id")
    .where("u.active = %s", True)
    .where("o.created_at > %s", "2024-01-01")
    .order_by("order_count", "DESC")
    .limit(10)
    .build())
print(query)

# TODO: GROUP BY ve HAVING destegi ekle
# TODO: Subquery destegi ekle
# TODO: INSERT, UPDATE, DELETE builder'lari yaz
# TODO: SQL injection korunmasi icin parameterized query kullan
```

**Beklenen Sonuc:** Fluent API ile okunabilir sorgu olusturulmali. Parameterized query ile SQL injection onlenmeli.

---

### Alıştırma 9: Mediator Pattern — Event Bus (Zor)

Loose coupling saglayan bir event bus sistemi implement edin.

```python
from typing import Callable, Any
from collections import defaultdict
import asyncio

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
        self._middleware: list[Callable] = []

    def on(self, event_name: str, handler: Callable):
        self._handlers[event_name].append(handler)
        return self

    def off(self, event_name: str, handler: Callable):
        self._handlers[event_name].remove(handler)
        return self

    def use(self, middleware: Callable):
        self._middleware.append(middleware)
        return self

    def emit(self, event_name: str, data: Any = None):
        # Middleware chain
        for mw in self._middleware:
            data = mw(event_name, data)
            if data is None:
                return  # Middleware engelledi

        for handler in self._handlers[event_name]:
            handler(data)

    def once(self, event_name: str, handler: Callable):
        def wrapper(data):
            handler(data)
            self.off(event_name, wrapper)
        self.on(event_name, wrapper)

# Kullanim
bus = EventBus()

# Logging middleware
bus.use(lambda event, data: (print(f"[LOG] {event}: {data}"), data)[1])

# Handler'lar
bus.on("user:registered", lambda user: print(f"Welcome email: {user['email']}"))
bus.on("user:registered", lambda user: print(f"Analytics: new user {user['id']}"))
bus.on("order:placed", lambda order: print(f"Stock update: {order['items']}"))

bus.emit("user:registered", {"id": 1, "email": "test@test.com"})

# TODO: Async handler destegi ekle
# TODO: Priority-based handler siralama ekle
# TODO: Error handling (bir handler fail ederse digerlerine etkisi olmamali)
# TODO: Dead letter queue ekle (handle edilmeyen event'ler)
# TODO: TypedEvent class'i ile type-safe event tanimlama
```

**Beklenen Sonuc:** Event emit edildiginde tum handler'lar calismali. Middleware chain ile cross-cutting concern'ler uygulanmali. once() ile tek seferlik handler calismali.

---

### Alıştırma 10: Anti-Pattern Refactoring Challenge (Zor)

Asagidaki anti-pattern'leri tespit edin ve dogru pattern ile refactor edin.

```python
# Anti-pattern 1: God Object
class ApplicationManager:
    def __init__(self):
        self.users = []
        self.orders = []
        self.products = []
        self.emails_sent = []
        self.logs = []

    def create_user(self, name, email): pass
    def delete_user(self, user_id): pass
    def create_order(self, user_id, products): pass
    def process_payment(self, order_id, amount): pass
    def send_email(self, to, subject, body): pass
    def generate_report(self, type): pass
    def update_inventory(self, product_id, qty): pass
    def log_action(self, action): pass
    # ... 50+ method daha

# Anti-pattern 2: Callback Hell
def process_order(order):
    validate_order(order, lambda valid:
        check_inventory(order, lambda available:
            process_payment(order, lambda paid:
                update_inventory(order, lambda updated:
                    send_confirmation(order, lambda sent:
                        log_order(order, lambda logged:
                            print("Done!")))))))

# Anti-pattern 3: Primitive Obsession
def create_user(name, email, phone, street, city, zip_code, country,
                card_number, card_expiry, card_cvv, role, department):
    pass  # 12 parametre!

# TODO: God Object'i Single Responsibility ile parcala (UserService, OrderService, EmailService...)
# TODO: Callback Hell'i async/await veya Pipeline pattern ile duzelt
# TODO: Primitive Obsession'i Value Object'ler ile coz (Address, CreditCard, UserRole)
# TODO: Her refactoring icin SOLID prensiplerinin hangisini uyguladiginizi belirtin
```

**Beklenen Sonuc:** Her anti-pattern icin dogru pattern uygulanmali. God Object en az 4 ayri servise parcalanmali. Callback hell okunabilir pipeline'a donusmeli. 12 parametreli fonksiyon 3-4 Value Object alacak sekilde refactor edilmeli.
:::

:::knowledge-check
## Bilgi Kontrolü

1. SOLID'in her harfi ne anlama gelir?
2. Singleton pattern'ın dezavantajı nedir?
3. Factory pattern ne zaman kullanılır?
4. Strategy pattern if/else'den neden daha iyi?
5. Observer pattern'da subject ve observer arasındaki ilişki nedir?
6. Adapter pattern gerçek hayattan hangi duruma benzer?
7. Decorator pattern inheritance'dan neden daha esnek?
8. Command pattern undo/redo'yu nasıl mümkün kılar?
9. Over-engineering nedir ve nasıl önlenir?
10. Composition over inheritance ne demek?
:::

:::english
## Key Terms

| Term | Pronunciation | Turkish | Description |
|------|--------------|---------|-------------|
| Design Pattern | /dɪˈzaɪn ˈpæt.ɚn/ | Tasarım Kalıbı | Tekrar eden problemlere kanıtlanmış çözüm |
| Singleton | /ˈsɪŋ.ɡəl.tən/ | Tekil | Tek instance garanti eden pattern |
| Factory | /ˈfæk.tɚ.i/ | Fabrika | Nesne oluşturmayı soyutlayan pattern |
| Observer | /əbˈzɝː.vɚ/ | Gözlemci | Değişiklikleri dinleyen pattern |
| Strategy | /ˈstræt.ə.dʒi/ | Strateji | Algoritma ailesini değiştirilebilir yapan pattern |
| Adapter | /əˈdæp.tɚ/ | Adaptör | Uyumsuz interface'leri uyumlu yapan pattern |
| Decorator | /ˈdek.ə.reɪ.tɚ/ | Dekoratör | Runtime'da davranış ekleyen pattern |
| Encapsulation | /ɪnˌkæp.sjəˈleɪ.ʃən/ | Kapsülleme | Detayları gizleme |
| Abstraction | /æbˈstræk.ʃən/ | Soyutlama | Karmaşıklığı gizleme |
| Anti-pattern | /ˈæn.ti ˈpæt.ɚn/ | Kötü pratik | Yaygın ama zararlı yaklaşım |
:::

:::external-resource
## Ek Kaynaklar

- [Refactoring Guru — Design Patterns](https://refactoring.guru/design-patterns)
- [Python Design Patterns](https://python-patterns.guide/)
- [JavaScript Design Patterns](https://www.patterns.dev/)
- [SOLID Principles — Uncle Bob](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html)
- [Head First Design Patterns](https://www.oreilly.com/library/view/head-first-design/9781492077992/)
- [Martin Fowler — Refactoring](https://refactoring.com/)
:::
