---
id: "mod-02-python/lesson-03"
title: "Decorators, Generators ve İleri Seviye Kalıplar"
description: "Python'da decorator, generator, context manager, asyncio ve functional programming kalıplarını deha seviyesinde öğren. Mülakatlarda fark yarat."
estimated_minutes: 60
order: 3
tags: ["decorators", "generators", "context-managers", "asyncio", "functional-programming", "python-advanced"]
prerequisites: ["mod-02-python/lesson-01", "mod-02-python/lesson-02"]
---

# Decorators, Generators ve İleri Seviye Kalıplar

:::realworld
Bir backend projesi geliştiriyorsun. Her endpoint'e authentication kontrolü, logging ve rate limiting eklemen gerekiyor. Aynı kodu her fonksiyona kopyala-yapıştır mı edeceksin? Tabii ki hayır. Decorators ile bu cross-cutting concern'leri tek bir yerde tanımlayıp her fonksiyona zarif şekilde uygularsın. Generator ile milyonlarca satırlık log dosyasını belleği çökertmeden satır satır işlersin. Context manager ile veritabanı bağlantılarını güvenle yönetirsin. Bu derste, production-grade Python yazan geliştiricilerin günlük kullandığı ileri seviye kalıpları öğreneceksin.
:::

## Neden Bu Konuları Öğreniyorsun?

İleri seviye Python kalıpları, seni "Python bilen biri" olmaktan çıkarıp "Python'u gerçekten anlayan biri" seviyesine taşır. Bu konuları bilmeden:

- Framework kaynak kodlarını (Django, FastAPI, Flask) okuyamazsın
- Bellek verimli kod yazamazsın
- Production'da güvenli kaynak yönetimi yapamazsın
- Teknik mülakatlarda orta seviyenin üstüne çıkamazsın

:::deha-tip
Deha seviyesi geliştiriciler, bir decorator gördüklerinde altında yatan closure mekanizmasını anlar. Generator kullanırken bellek profilini zihinlerinde canlandırır. Context manager yazarken exception safety düşünür. Bu araçları "sihir" olarak değil, Python'un data model'inin doğal uzantıları olarak görürler.
:::

---

## 1. Decorators

:::concept[Decorator (İng: Decorator)]
Decorator, bir fonksiyonu veya class'ı değiştirmeden ona yeni davranış ekleyen bir tasarım kalıbıdır. Teknik olarak, bir callable alıp yeni bir callable döndüren higher-order function'dır.

**Türkçe karşılığı:** Dekoratör / Süsleyici
**Ne işe yarar:** Fonksiyonlara cross-cutting concern ekler (logging, caching, auth kontrolü)
**Gerçek hayat benzetmesi:** Bir hediyeyi ambalaj kağıdına sarmak gibi. Hediye (fonksiyon) değişmez, ama dışarıdan bakınca yeni özellikler eklenir.
:::

### Temel Fonksiyon Decorator

:::code[python]{title="Basit Decorator Yapısı"}
import functools

def timer(func):
    """Fonksiyonun çalışma süresini ölçer."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} -> {elapsed:.4f} saniye")
        return result
    return wrapper

@timer
def fibonacci(n):
    """N. Fibonacci sayısını hesaplar."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# @timer kullanımı şuna eşdeğer:
# fibonacci = timer(fibonacci)
:::

:::warning
`functools.wraps` kullanmayı asla unutma! Bu decorator olmadan, orijinal fonksiyonun `__name__`, `__doc__` ve `__module__` bilgileri kaybolur. Debug sırasında tüm fonksiyonlar "wrapper" olarak görünür ve bu kabusu yaşamak istemezsin.
:::

### Parametreli Decorator (Decorator Factory)

:::code[python]{title="Decorator Factory - Parametre Alan Decorator"}
import functools

def retry(max_attempts=3, delay=1.0):
    """Başarısız olan fonksiyonu belirli sayıda tekrar dener."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Deneme {attempt}/{max_attempts} basarisiz: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=5, delay=2.0)
def fetch_api_data(url):
    """API'den veri çeker, başarısız olursa tekrar dener."""
    import urllib.request
    return urllib.request.urlopen(url).read()
:::

### Class Decorator

:::code[python]{title="Class Decorator Kullanımı"}
def singleton(cls):
    """Bir class'tan sadece tek bir instance oluşturulmasını sağlar."""
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self, host="localhost", port=5432):
        self.host = host
        self.port = port
        print(f"Veritabani baglantisi kuruldu: {host}:{port}")

# Her çağrıda aynı instance döner
db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(db1 is db2)  # True
:::

:::beginner-mistake
Yaygın hata: Decorator factory yazarken parantez koymayı unutmak. `@retry` ile `@retry()` çok farklı şeyler. Birincisi fonksiyonu doğrudan `retry`'a argüman olarak geçirir, ikincisi önce `retry()` çağrılır ve dönen decorator fonksiyona uygulanır. Parametre almasa bile parantez koymalısın: `@retry()`.
:::

---

## 2. Generators

:::concept[Generator (İng: Generator)]
Generator, lazy evaluation ile değer üreten özel bir iterator'dır. `yield` keyword'ü ile tanımlanır, her `yield`'da durur ve sonraki `next()` çağrısında kaldığı yerden devam eder.

**Türkçe karşılığı:** Üretici / Jeneratör
**Ne işe yarar:** Büyük veri setlerini bellekte tutmadan parça parça işler
**Gerçek hayat benzetmesi:** Bir fırın gibi. Tüm ekmekleri önceden pişirip depolamak yerine, müşteri geldiğinde taze pişirir.
:::

:::code[python]{title="Generator vs List - Bellek Farkı"}
import sys

# List: Tüm değerleri bellekte tutar
numbers_list = [x ** 2 for x in range(1_000_000)]
print(f"List bellek: {sys.getsizeof(numbers_list):,} bytes")  # ~8 MB

# Generator: Değerleri tek tek üretir
numbers_gen = (x ** 2 for x in range(1_000_000))
print(f"Generator bellek: {sys.getsizeof(numbers_gen):,} bytes")  # ~200 bytes

# yield ile generator fonksiyonu
def read_large_file(filepath):
    """Büyük dosyayı satır satır okur, bellekte tutmaz."""
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()

# Kullanım: 10 GB'lık log dosyası bile sorunsuz işlenir
for line in read_large_file("server.log"):
    if "ERROR" in line:
        print(line)
:::

### Generator Pipeline

:::code[python]{title="Generator Pipeline - Veri İşleme Zinciri"}
def read_lines(filepath):
    """Satırları tembel (lazy) olarak okur."""
    with open(filepath) as f:
        for line in f:
            yield line.strip()

def filter_errors(lines):
    """Sadece ERROR içeren satırları geçirir."""
    for line in lines:
        if "ERROR" in line:
            yield line

def parse_timestamp(lines):
    """Her satırdan timestamp çıkarır."""
    for line in lines:
        parts = line.split(" ", 2)
        yield {"timestamp": parts[0], "message": parts[2]}

# Pipeline: Hiçbir aşamada tüm veri bellekte değil
pipeline = parse_timestamp(filter_errors(read_lines("app.log")))
for entry in pipeline:
    print(entry)
:::

### itertools ile Güçlü Generator Kalıpları

:::code[python]{title="itertools - Generator Araç Kutusu"}
import itertools

# chain: Birden fazla iterable'ı birleştir
combined = itertools.chain([1, 2], [3, 4], [5, 6])
# -> 1, 2, 3, 4, 5, 6

# islice: Generator'dan dilim al (list slicing gibi ama lazy)
first_10 = itertools.islice(range(1_000_000), 10)

# groupby: Ardışık elemanları grupla
data = [("backend", "Ali"), ("backend", "Veli"), ("frontend", "Ayse")]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")

# product: Kartezyen çarpım
sizes = ["S", "M", "L"]
colors = ["red", "blue"]
combinations = list(itertools.product(sizes, colors))
# -> [('S', 'red'), ('S', 'blue'), ('M', 'red'), ...]

# accumulate: Kümülatif toplam
totals = list(itertools.accumulate([100, 200, 150, 300]))
# -> [100, 300, 450, 750]
:::

:::tip
`itertools` standart kütüphanenin en hafife alınan modülüdür. Bellek verimli veri işleme yapmak için `chain`, `islice`, `groupby`, `product`, `starmap` ve `tee` fonksiyonlarını mutlaka öğren. Bir loop yazmadan önce "Bunu itertools ile yapabilir miyim?" diye sor.
:::

---

## 3. Context Managers

:::concept[Context Manager (İng: Context Manager)]
Context manager, bir kaynağın (dosya, bağlantı, kilit) güvenli şekilde edinilmesini ve serbest bırakılmasını garanti eden bir protokoldür. `with` bloğu ile kullanılır.

**Türkçe karşılığı:** Bağlam Yöneticisi
**Ne işe yarar:** Kaynak sızıntılarını (resource leak) önler. Exception olsa bile cleanup garantili çalışır.
**Gerçek hayat benzetmesi:** Otel odası gibi. Check-in (`__enter__`), kullanım, check-out (`__exit__`). Ne olursa olsun check-out yapılır.
:::

:::code[python]{title="Custom Context Manager - Class Tabanlı"}
class DatabaseTransaction:
    """Veritabanı transaction'ını güvenle yönetir."""

    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.connection.begin()
        print("Transaction basladi")
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.connection.rollback()
            print(f"Hata! Rollback yapildi: {exc_val}")
            return False  # Exception'ı tekrar fırlat
        self.connection.commit()
        print("Transaction basariyla commit edildi")
        return True

# Kullanım
with DatabaseTransaction(db_conn) as conn:
    conn.execute("INSERT INTO users ...")
    conn.execute("UPDATE accounts ...")
    # Hata olursa otomatik rollback, başarılıysa commit
:::

### contextlib ile Kolay Context Manager

:::code[python]{title="contextlib.contextmanager - Generator Tabanlı"}
from contextlib import contextmanager
import time

@contextmanager
def timer(label="Islem"):
    """Bir kod bloğunun çalışma süresini ölçer."""
    start = time.perf_counter()
    try:
        yield  # with bloğunun içi burada çalışır
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.4f} saniye")

# Kullanım
with timer("Veri isleme"):
    data = [x ** 2 for x in range(1_000_000)]
    total = sum(data)
# Çıktı: Veri isleme: 0.1234 saniye

@contextmanager
def temporary_directory():
    """Geçici dizin oluşturur, işlem bitince siler."""
    import tempfile, shutil
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)
:::

---

## 4. Error Handling

:::code[python]{title="try/except/else/finally - Tam Yapı"}
def safe_divide(a, b):
    """Güvenli bölme işlemi - tüm hata yönetimi kalıplarını gösterir."""
    try:
        result = a / b
    except ZeroDivisionError:
        print("Sifira bolme hatasi!")
        return None
    except TypeError as e:
        print(f"Tip hatasi: {e}")
        return None
    else:
        # Hata OLMADIĞINDA çalışır (try başarılıysa)
        print(f"Sonuc: {result}")
        return result
    finally:
        # HER DURUMDA çalışır (hata olsa da olmasa da)
        print("Islem tamamlandi")
:::

### Custom Exception Hierarchy

:::code[python]{title="Profesyonel Exception Hiyerarşisi"}
class AppError(Exception):
    """Uygulamaya özel tüm hataların base class'ı."""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

class ValidationError(AppError):
    """Veri doğrulama hatası."""
    pass

class NotFoundError(AppError):
    """Kaynak bulunamadı hatası."""
    pass

class AuthenticationError(AppError):
    """Kimlik doğrulama hatası."""
    pass

class RateLimitError(AppError):
    """Hız limiti aşıldı hatası."""

    def __init__(self, message, retry_after=60):
        super().__init__(message, code=429)
        self.retry_after = retry_after

# Kullanım
def get_user(user_id):
    if not isinstance(user_id, int):
        raise ValidationError(f"user_id integer olmali: {user_id}", code=400)
    user = db.find_user(user_id)
    if user is None:
        raise NotFoundError(f"Kullanici bulunamadi: {user_id}", code=404)
    return user

# Yakalama
try:
    user = get_user("abc")
except ValidationError as e:
    print(f"Gecersiz girdi ({e.code}): {e}")
except NotFoundError as e:
    print(f"Bulunamadi ({e.code}): {e}")
except AppError as e:
    print(f"Uygulama hatasi: {e}")
:::

:::beginner-mistake
Yaygın hata: Her yerde `except Exception` veya daha kötüsü bare `except:` kullanmak. Bu, `KeyboardInterrupt` ve `SystemExit` dahil tüm hataları yakalar. Sadece beklediğin spesifik exception'ları yakala. Beklenmeyen hatalar yukarı fırlasın ki fark edesin.
:::

---

## 5. İleri Seviye Comprehensions

:::code[python]{title="Nested ve Conditional Comprehensions"}
# Nested list comprehension (2D -> 1D)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
# -> [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Conditional comprehension
even_squares = [x**2 for x in range(20) if x % 2 == 0]
# -> [0, 4, 16, 36, 64, ...]

# if-else expression (ternary) in comprehension
labels = ["cift" if x % 2 == 0 else "tek" for x in range(5)]
# -> ["cift", "tek", "cift", "tek", "cift"]

# Dict comprehension
users = [("ali", 25), ("veli", 30), ("ayse", 22)]
user_dict = {name: age for name, age in users if age >= 25}
# -> {"ali": 25, "veli": 30}

# Set comprehension
unique_lengths = {len(word) for word in ["hello", "world", "hi", "hey"]}
# -> {2, 3, 5}

# Nested dict comprehension
multiplication_table = {
    i: {j: i * j for j in range(1, 11)}
    for i in range(1, 11)
}
# multiplication_table[7][8] -> 56
:::

:::comparison
| Yapı | Syntax | Döndürdüğü Tip | Bellek |
|------|--------|----------------|--------|
| List comprehension | `[x for x in ...]` | `list` | Tüm elemanlar bellekte |
| Generator expression | `(x for x in ...)` | `generator` | Lazy, tek seferde 1 eleman |
| Dict comprehension | `{k: v for k, v in ...}` | `dict` | Tüm key-value bellekte |
| Set comprehension | `{x for x in ...}` | `set` | Unique elemanlar bellekte |

**Tavsiye:** Ara sonuçları sadece iterate edeceksen generator expression kullan. Birden fazla erişim gerekiyorsa list comprehension tercih et.
:::

---

## 6. Lambda ve Higher-Order Functions

:::code[python]{title="Lambda, map, filter, reduce"}
from functools import reduce

# Lambda: Tek satırlık anonim fonksiyon
square = lambda x: x ** 2
add = lambda a, b: a + b

# map: Her elemana fonksiyon uygula
prices_usd = [10, 25, 50, 100]
prices_try = list(map(lambda p: p * 34.5, prices_usd))
# -> [345.0, 862.5, 1725.0, 3450.0]

# filter: Koşula uyan elemanları filtrele
adults = list(filter(lambda user: user["age"] >= 18, [
    {"name": "Ali", "age": 25},
    {"name": "Zeynep", "age": 15},
    {"name": "Can", "age": 30},
]))
# -> [{"name": "Ali", "age": 25}, {"name": "Can", "age": 30}]

# reduce: Tüm elemanları tek değere indirge
total = reduce(lambda acc, x: acc + x, [100, 200, 300, 400])
# -> 1000

# sorted ile key fonksiyonu
students = [("Ali", 85), ("Zeynep", 92), ("Can", 78)]
by_grade = sorted(students, key=lambda s: s[1], reverse=True)
# -> [("Zeynep", 92), ("Ali", 85), ("Can", 78)]
:::

:::tip
Modern Python'da `map` ve `filter` yerine genellikle comprehension tercih edilir. `list(map(lambda x: x*2, items))` yerine `[x*2 for x in items]` daha okunaklıdır. Ancak `reduce`, `sorted(key=...)` ve callback pattern'lerinde lambda hala vazgeçilmezdir.
:::

---

## 7. Functional Programming Kalıpları

:::code[python]{title="Python'da Functional Programming"}
from functools import partial, lru_cache
from operator import attrgetter, itemgetter

# partial: Fonksiyonun bazı argümanlarını sabitle
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(square(5))  # 25
print(cube(3))    # 27

# lru_cache: Otomatik memoization (sonuçları önbelleğe al)
@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Anında hesaplar (cache sayesinde)

# Function composition (fonksiyon birleştirme)
def compose(*functions):
    """Fonksiyonları sağdan sola birleştirir: compose(f, g, h)(x) = f(g(h(x)))"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions)

double = lambda x: x * 2
increment = lambda x: x + 1
to_string = lambda x: f"Sonuc: {x}"

transform = compose(to_string, double, increment)
print(transform(5))  # "Sonuc: 12"  (5+1=6, 6*2=12, "Sonuc: 12")

# itemgetter ve attrgetter: Temiz accessor fonksiyonları
data = [{"name": "Ali", "score": 85}, {"name": "Can", "score": 92}]
sorted_data = sorted(data, key=itemgetter("score"), reverse=True)
:::

---

## 8. Asyncio Temelleri

:::concept[Asyncio (İng: Asynchronous I/O)]
Asyncio, Python'da concurrent (eşzamanlı) programlama yapmanın modern yoludur. Thread kullanmadan, tek thread üzerinde birden fazla I/O-bound işlemi paralel yürütür.

**Türkçe karşılığı:** Asenkron Girdi/Çıktı
**Ne işe yarar:** Network istekleri, dosya okuma, veritabanı sorguları gibi bekleme içeren işlemleri verimli yönetir
**Gerçek hayat benzetmesi:** Bir garson gibi. Bir masanın siparişini mutfağa verdikten sonra, yemek hazırlanırken başka masalara bakar. Her masaya ayrı bir garson (thread) atamak yerine, tek garson verimli çalışır.
:::

:::code[python]{title="async/await Temel Kullanım"}
import asyncio

async def fetch_user(user_id):
    """Kullanıcı bilgisini asenkron çeker (simülasyon)."""
    print(f"Kullanici {user_id} isteniyor...")
    await asyncio.sleep(1)  # Network bekleme simülasyonu
    return {"id": user_id, "name": f"User_{user_id}"}

async def fetch_orders(user_id):
    """Sipariş bilgisini asenkron çeker."""
    print(f"Siparisler {user_id} isteniyor...")
    await asyncio.sleep(1.5)
    return [{"order_id": 1, "total": 150}]

async def main():
    # Sıralı çalışma: 2.5 saniye
    user = await fetch_user(1)
    orders = await fetch_orders(1)

    # Paralel çalışma: 1.5 saniye (en uzun süren kadar)
    user, orders = await asyncio.gather(
        fetch_user(1),
        fetch_orders(1)
    )
    print(f"Kullanici: {user}, Siparisler: {orders}")

asyncio.run(main())
:::

:::code[python]{title="asyncio.gather ile Toplu İşlem"}
import asyncio

async def fetch_url(url):
    """URL'den veri çeker (simülasyon)."""
    await asyncio.sleep(0.5)
    return f"{url} -> 200 OK"

async def scrape_all():
    urls = [
        "https://api.example.com/users",
        "https://api.example.com/products",
        "https://api.example.com/orders",
        "https://api.example.com/reviews",
        "https://api.example.com/categories",
    ]
    # 5 istek aynı anda gider, toplam ~0.5 saniye
    results = await asyncio.gather(*[fetch_url(url) for url in urls])
    for result in results:
        print(result)

asyncio.run(scrape_all())
:::

:::warning
`asyncio.run()` sadece senkron koddan async dünyaya geçiş noktasında kullanılır. Zaten async bir fonksiyonun içinde `asyncio.run()` çağırmak hata verir. Ayrıca `time.sleep()` ile `await asyncio.sleep()` arasındaki farkı anla: birincisi tüm thread'i bloklar, ikincisi sadece o coroutine'i bekletir.
:::

---

## 9. Logging

:::comparison
| Özellik | `print()` | `logging` Modülü |
|---------|-----------|------------------|
| Seviye kontrolü | Yok | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| Çıktı yönlendirme | Sadece stdout | Dosya, konsol, network, email |
| Format | Manuel | Otomatik timestamp, seviye, modül |
| Production'da | Asla kullanma | Standart yöntem |
| Performans | Her zaman çalışır | Seviye altındakiler atlanır |
| Kapatma | Satır satır silmen gerekir | Seviye değiştirmek yeterli |

**Tavsiye:** `print()` sadece hızlı prototipleme ve debug için. Production'da mutlaka `logging` kullan.
:::

:::code[python]{title="Profesyonel Logging Kurulumu"}
import logging

# Logger oluştur (modül adıyla)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Konsol handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Dosya handler
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

# Format
formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Handler'ları ekle
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Kullanım
logger.debug("Detay: x=%d", 42)           # Sadece dosyaya yazılır
logger.info("Kullanici giris yapti")        # Konsol + dosya
logger.warning("Disk alani %90 dolu")       # Konsol + dosya
logger.error("Veritabani baglantisi koptu")  # Konsol + dosya
logger.critical("Sistem coktu!")             # Konsol + dosya

# Exception loglama (traceback dahil)
try:
    result = 1 / 0
except ZeroDivisionError:
    logger.exception("Hesaplama hatasi olustu")
:::

---

## 10. Performans ve Profiling

:::code[python]{title="Python Performans Ölçme Araçları"}
import timeit
import cProfile

# timeit: Küçük kod parçalarını ölçme
list_time = timeit.timeit(
    "[x**2 for x in range(1000)]",
    number=10000
)
genexp_time = timeit.timeit(
    "list(x**2 for x in range(1000))",
    number=10000
)
print(f"List comp: {list_time:.3f}s, Gen exp: {genexp_time:.3f}s")

# cProfile: Fonksiyon bazlı profiling
def process_data():
    data = [i ** 2 for i in range(100_000)]
    filtered = [x for x in data if x % 3 == 0]
    return sum(filtered)

cProfile.run("process_data()")
# ncalls  tottime  percall  cumtime  percall filename:lineno(function)
# 1       0.012    0.012    0.020    0.020  script.py:1(process_data)
:::

:::code[python]{title="Yaygın Performans İpuçları"}
# 1. String birleştirme: + yerine join
# Yavaş (her + yeni string oluşturur)
result = ""
for word in words:
    result += word + " "

# Hızlı
result = " ".join(words)

# 2. Membership testi: list yerine set
# Yavaş - O(n)
if item in large_list:
    pass

# Hızlı - O(1)
large_set = set(large_list)
if item in large_set:
    pass

# 3. Dictionary'de get kullanımı
# Yavaş (iki kere arama)
if key in my_dict:
    value = my_dict[key]
else:
    value = default

# Hızlı (tek arama)
value = my_dict.get(key, default)

# 4. Local variable referansı (tight loop'larda)
# Yavaş
for i in range(1_000_000):
    math.sqrt(i)  # her seferinde global lookup

# Hızlı
sqrt = math.sqrt  # local referans
for i in range(1_000_000):
    sqrt(i)
:::

---

## Pratik Uygulamalar

:::exercise
### Alistirma 1: Rate Limiter Decorator (Kolay)

Bir `@rate_limit(calls=5, period=60)` decorator yaz. Fonksiyon belirtilen sure icinde en fazla belirtilen sayida cagrilabilsin.

```python
import time
from functools import wraps

class RateLimitError(Exception):
    """Rate limit asidiginda firlatilir."""
    pass

def rate_limit(calls: int, period: int):
    """
    Decorator: Fonksiyonu belirli bir sure icinde sinirli sayida cagirmaya izin verir.

    Args:
        calls: Izin verilen maksimum cagri sayisi
        period: Sure penceresi (saniye)
    """
    def decorator(func):
        call_times: list[float] = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # TODO: Suresi dolmus cagrilari listeden cikar
            # TODO: Mevcut cagri sayisi >= calls ise RateLimitError firlat
            # TODO: Yeni cagriyi kaydet ve fonksiyonu calistir
            pass

        return wrapper
    return decorator

# Test:
@rate_limit(calls=3, period=10)
def send_email(to: str) -> str:
    return f"Email sent to {to}"

# Ilk 3 cagri basarili olmali
print(send_email("a@test.com"))  # "Email sent to a@test.com"
print(send_email("b@test.com"))  # "Email sent to b@test.com"
print(send_email("c@test.com"))  # "Email sent to c@test.com"

# 4. cagri RateLimitError firlatmali
try:
    print(send_email("d@test.com"))
except RateLimitError as e:
    print(f"Hata: {e}")  # "Rate limit exceeded: 3 calls per 10 seconds"
```

**Beklenen Sonuc:** Ilk 3 cagri basarili, 4. cagri `RateLimitError` firlatmali. 10 saniye sonra tekrar cagrilabilmeli. `@wraps` sayesinde fonksiyon adi ve docstring korunmali.
**Ipucu:** `call_times` listesine her cagri zamanini ekle, periyod disi kalanlari filtrele.

---

### Alistirma 2: Generator Pipeline ile Veri Isleme (Orta)

Generator'lar kullanarak bellek-verimli bir veri isleme pipeline'i olustur.

```python
import csv
from typing import Generator, Iterator
from io import StringIO

# Ornek CSV verisi (gercek projede dosyadan okunur)
SAMPLE_CSV = """isim,departman,maas,yas
Ahmet,Muhendislik,15000,28
Ayse,Pazarlama,12000,25
Mehmet,Muhendislik,18000,32
Fatma,Pazarlama,13000,27
Ali,Muhendislik,16000,30
Zeynep,IK,11000,24
Hasan,Muhendislik,20000,35
Elif,Pazarlama,14000,29
"""

def read_csv_rows(data: str) -> Generator[dict[str, str], None, None]:
    """CSV verisini satir satir dict olarak yield et."""
    # TODO: csv.DictReader kullanarak her satiri yield et
    pass

def filter_by_department(rows: Iterator[dict], dept: str) -> Generator[dict, None, None]:
    """Belirli bir departmana ait satirlari filtrele."""
    # TODO: Sadece departman == dept olan satirlari yield et
    pass

def transform_salary(rows: Iterator[dict]) -> Generator[dict, None, None]:
    """Maas alanini int'e cevir ve yillik maas ekle."""
    # TODO: Her satira "yillik_maas" alani ekle (maas * 12)
    pass

def aggregate_stats(rows: Iterator[dict]) -> dict:
    """Toplam, ortalama ve max maas istatistiklerini hesapla."""
    # TODO: Tek geciste (single pass) istatistikleri hesapla
    # Hint: Generator'u tukettikten sonra tekrar kullanamazsin!
    pass

# Pipeline calistir:
pipeline = transform_salary(
    filter_by_department(
        read_csv_rows(SAMPLE_CSV),
        dept="Muhendislik"
    )
)

stats = aggregate_stats(pipeline)
print(f"Muhendislik Departmani:")
print(f"  Calisan Sayisi: {stats['count']}")
print(f"  Ortalama Maas: {stats['avg_salary']:.0f} TL")
print(f"  Toplam Yillik Maas: {stats['total_yearly']:.0f} TL")
print(f"  Max Maas: {stats['max_salary']} TL")
```

**Beklenen Sonuc:** Muhendislik departmaninda 4 calisan, ortalama maas 17250 TL, toplam yillik maas 828000 TL, max maas 20000 TL. Pipeline bellekte tum veriyi tutmadan satir satir islemeli.
**Ipucu:** `aggregate_stats` icinde `count`, `total`, `max_val` degiskenlerini sifirdan baslatip her satiri islediginde guncelle.

---

### Alistirma 3: Context Manager ile Kaynak Yonetimi (Zor)

Hem class-based hem de generator-based context manager yazarak kaynak yonetimini ogren.

```python
from contextlib import contextmanager
from dataclasses import dataclass, field
import time

# --- KISIM 1: Class-Based Context Manager ---

@dataclass
class ConnectionPool:
    """Basit bir connection pool simulasyonu."""
    max_connections: int = 5
    _available: list = field(default_factory=list)
    _in_use: list = field(default_factory=list)

    def __post_init__(self):
        self._available = [f"conn_{i}" for i in range(self.max_connections)]

    # TODO: get_connection metodu yaz
    # - Bos connection varsa al, yoksa RuntimeError firlat
    # - Connection'i _available'dan _in_use'a tasi

    # TODO: release_connection metodu yaz
    # - Connection'i _in_use'dan _available'a geri tasi

    # TODO: __enter__ ve __exit__ metodlarini yaz
    # - __enter__: connection al ve dondur
    # - __exit__: exception olsa bile connection'i geri birak
    # - Exception varsa connection'i resetle (yenisiyle degistir)

# Test:
pool = ConnectionPool(max_connections=2)

with pool as conn1:
    print(f"Baglanti alindi: {conn1}")
    with pool as conn2:
        print(f"Baglanti alindi: {conn2}")
        # 3. baglanti almaya calis - hata vermeli
        # with pool as conn3:  # RuntimeError: No available connections

print(f"Musait baglanti sayisi: {len(pool._available)}")  # 2

# --- KISIM 2: Generator-Based Context Manager ---

@contextmanager
def timer(label: str):
    """Kod blogunun calisma suresini olcer."""
    # TODO: Implement
    # start = time.perf_counter()
    # yield
    # elapsed = time.perf_counter() - start
    # print(f"{label}: {elapsed:.4f} saniye")
    pass

# Test:
with timer("Liste olusturma"):
    data = [i ** 2 for i in range(1_000_000)]

with timer("Toplam hesaplama"):
    total = sum(data)
    print(f"Toplam: {total}")
```

**Beklenen Sonuc:** ConnectionPool context manager ile baglanti alinip otomatik geri birakilmali. Havuzda baglanti kalmadiginda `RuntimeError` firlatmali. Timer context manager calisma suresini dogru olcmeli. Exception durumunda bile kaynaklar geri birakilmali.
**Ipucu:** `__exit__` metodunun `exc_type, exc_val, exc_tb` parametreleri exception bilgisini tasir. `False` donerse exception yeniden firlatilir.
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdakilerden hangisi decorator ile ilgili DOĞRUDUR?"
options:
  - "Decorator sadece fonksiyonlara uygulanabilir"
  - "functools.wraps kullanmak zorunludur, kullanılmazsa kod çalışmaz"
  - "Decorator bir callable alıp yeni bir callable döndüren higher-order function'dır"
  - "Decorator'lar her zaman fonksiyonu yavaşlatır"
correct: 2
explanation: "Decorator, teknik olarak bir callable (fonksiyon, class) alıp yeni bir callable döndüren higher-order function'dır. Class'lara da uygulanabilir. functools.wraps kullanılmasa da kod çalışır ama metadata kaybolur."
:::

:::knowledge-check
type: multiple_choice
question: "Generator ile list arasındaki temel fark nedir?"
options:
  - "Generator daha hızlı çalışır"
  - "Generator lazy evaluation yapar, değerleri tek tek üretir ve bellekte tüm veriyi tutmaz"
  - "Generator sadece sayılarla çalışır"
  - "List comprehension generator'dan her zaman yavaştır"
correct: 1
explanation: "Generator lazy evaluation ile çalışır. Değerleri ihtiyaç oldukça üretir, tüm veriyi bellekte tutmaz. Bu sayede milyonlarca elemanlı veri setlerini sabit bellekle işleyebilirsin."
:::

:::knowledge-check
type: multiple_choice
question: "asyncio.gather() ne işe yarar?"
options:
  - "Birden fazla senkron fonksiyonu sırayla çalıştırır"
  - "Birden fazla coroutine'i eşzamanlı (concurrent) çalıştırır ve tüm sonuçları toplar"
  - "Thread pool oluşturur"
  - "Sadece hata yönetimi için kullanılır"
correct: 1
explanation: "asyncio.gather() birden fazla coroutine'i aynı anda başlatır ve hepsinin tamamlanmasını bekler. Sonuçları bir liste olarak döndürür. 5 API isteği varsa, hepsi paralel gider ve toplam süre en uzun isteğin süresi kadar olur."
:::

:::interview
**Mülakat Sorusu:** "Python'da decorator ne işe yarar? Bir örnek verin ve nasıl çalıştığını açıklayın."

**Beklenen cevap:**
Decorator, bir fonksiyona veya class'a ek davranış ekleyen higher-order function'dır. Teknik olarak, bir callable alır, yeni bir callable döndürür. En yaygın kullanımları: logging, caching (lru_cache), authentication, rate limiting ve timing. `@decorator` syntax'ı `func = decorator(func)` ifadesinin kısaltmasıdır. `functools.wraps` kullanılarak orijinal fonksiyonun metadata'sı korunmalıdır. Parametreli decorator yazmak için decorator factory pattern (üç katmanlı nested fonksiyon) kullanılır.
:::

:::interview
**Mülakat Sorusu:** "Generator nedir, ne zaman kullanırsınız?"

**Beklenen cevap:**
Generator, `yield` ile değer üreten lazy iterator'dır. Normal fonksiyon tüm sonucu hesaplayıp döndürürken, generator her `yield`'da durur ve `next()` ile kaldığı yerden devam eder. Büyük veri setlerini sabit bellekle işlemek, sonsuz diziler üretmek ve veri pipeline'ları oluşturmak için kullanılır. Örneğin 10 GB'lık bir log dosyasını satır satır işlemek için generator idealdir. Generator expression `(x for x in ...)` ile list comprehension `[x for x in ...]` arasındaki temel fark bellek kullanımıdır.
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6

### Prompt Ornekleri

**1. Konuyu Derinlemesine Anla:**
> "Python'da decorator'larin altinda yatan closure mekanizmasini adim adim acikla. @timer decorator'u yazarken functools.wraps neden gerekli? Decorator factory (parametreli decorator) 3 katmanli nested fonksiyon nasil calisiyor?"

*Neden:* Decorator'lari "sihir" olarak degil, Python'un first-class function ozelliginin dogal sonucu olarak anlamak, kendi decorator'larini yazabilmeni saglar

**2. Pratik Uygulama:**
> "Bir FastAPI projesi icin su decorator'lari yaz: 1) @retry(max_attempts=3, delay=1.0) - basarisiz istekleri tekrar deneyen, 2) @rate_limit(calls=10, period=60) - dakikada max 10 cagri izin veren, 3) @cache_result(ttl=300) - sonuclari 5 dakika onbellekleyen. Her birinde functools.wraps kullan."

*Follow-up:* "Bu decorator'lari bir fonksiyona ust uste uyguladigimda calisma sirasi nasil olur? @retry @rate_limit @cache_result sirasinin onemi ne?"

**3. Mukemmellik Icin:**
> "asyncio.gather vs asyncio.create_task vs await sirali cagri arasindaki farklari performans ve hata yonetimi acisindan karsilastir. 10 API istegininin paralel atilmasi senaryosunda her yaklasimin avantaj ve dezavantajlarini goster."

### Pair Programming Ipucu
Generator veya async kod yazarken AI'a kodunu yapistir: "Bu generator pipeline'imin bellek kullanim profilini analiz et. Darbogazlar nerede? itertools ile nasil optimize edebilirim?"
:::

:::exercise
### Alıştırma 4: Cache Decorator (Memoization)

**Görev:** LRU cache mantığıyla çalışan bir `@memoize(max_size=100)` decorator yaz. Cache hit/miss istatistiklerini tutsun.

**Başlangıç kodu:**
```python
from functools import wraps
from collections import OrderedDict

def memoize(max_size: int = 128):
    def decorator(func):
        cache = OrderedDict()
        stats = {"hits": 0, "misses": 0}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO:
            # 1. args + kwargs'dan hashable bir key olustur
            # 2. Key cache'te varsa -> hit, deger dondur
            # 3. Yoksa -> miss, fonksiyonu cagir, sonucu cache'e kaydet
            # 4. Cache max_size'i astiysa en eski elemani sil (LRU)
            pass

        wrapper.cache_info = lambda: stats
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

# Test
@memoize(max_size=3)
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Hesapla
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")

print(f"\nCache stats: {fibonacci.cache_info()}")

# Max size testi
@memoize(max_size=3)
def square(x: int) -> int:
    print(f"  Hesaplaniyor: {x}^2")
    return x * x

square(1)  # miss
square(2)  # miss
square(3)  # miss
square(1)  # hit
square(4)  # miss, 2 cache'ten duser (LRU)
square(2)  # miss (cache'ten dustu!)
print(f"Square cache stats: {square.cache_info()}")
```

**Beklenen çıktı:**
```
fib(0) = 0
fib(1) = 1
fib(2) = 1
...
fib(9) = 34

Cache stats: {'hits': 16, 'misses': 10}
  Hesaplaniyor: 1^2
  Hesaplaniyor: 2^2
  Hesaplaniyor: 3^2
  Hesaplaniyor: 4^2
  Hesaplaniyor: 2^2
Square cache stats: {'hits': 1, 'misses': 5}
```

**İpucu:** `OrderedDict.move_to_end(key)` ile erişilen elemanı sona taşı (en yeni). `popitem(last=False)` ile en eskiyi sil.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 5: Context Manager ile Database Transaction

**Görev:** `with` statement ile kullanılabilen bir database transaction context manager yaz. Hata olursa rollback, başarılıysa commit yapsın.

**Başlangıç kodu:**
```python
from contextlib import contextmanager

class FakeDatabase:
    def __init__(self):
        self.data: dict[str, list] = {"users": [], "orders": []}
        self._backup: dict | None = None
        self.committed = False

    def insert(self, table: str, record: dict):
        if table not in self.data:
            raise ValueError(f"Tablo bulunamadi: {table}")
        self.data[table].append(record)
        print(f"  INSERT into {table}: {record}")

    def _create_backup(self):
        import copy
        self._backup = copy.deepcopy(self.data)

    def _rollback(self):
        if self._backup:
            self.data = self._backup
            self._backup = None
            print("  ROLLBACK yapildi")

    def _commit(self):
        self._backup = None
        self.committed = True
        print("  COMMIT yapildi")

@contextmanager
def transaction(db: FakeDatabase):
    """Database transaction context manager."""
    # TODO:
    # 1. Backup olustur
    # 2. yield ile db'yi ver
    # 3. Hata olursa rollback
    # 4. Basariliysa commit
    pass

# Test 1: Basarili transaction
db = FakeDatabase()
print("=== Basarili Transaction ===")
with transaction(db) as conn:
    conn.insert("users", {"id": 1, "name": "Ahmet"})
    conn.insert("orders", {"id": 1, "user_id": 1, "total": 150})

print(f"Users: {db.data['users']}")

# Test 2: Basarisiz transaction (rollback)
print("\n=== Basarisiz Transaction ===")
with transaction(db) as conn:
    conn.insert("users", {"id": 2, "name": "Ayse"})
    conn.insert("invalid_table", {"id": 1})  # Hata!

print(f"Users (degismemeli): {db.data['users']}")
```

**Beklenen çıktı:**
```
=== Basarili Transaction ===
  INSERT into users: {'id': 1, 'name': 'Ahmet'}
  INSERT into orders: {'id': 1, 'user_id': 1, 'total': 150}
  COMMIT yapildi
Users: [{'id': 1, 'name': 'Ahmet'}]

=== Basarisiz Transaction ===
  INSERT into users: {'id': 2, 'name': 'Ayse'}
  ROLLBACK yapildi
Users (degismemeli): [{'id': 1, 'name': 'Ahmet'}]
```

**İpucu:** `try/except/else` bloğu kullan. `yield` öncesi backup, except'te rollback, else'de commit.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: Generator ile Dosya İşleme Pipeline

**Görev:** Generator'lar zincirleyerek büyük log dosyalarını bellek-verimli şekilde işleyen bir pipeline yaz.

**Başlangıç kodu:**
```python
from typing import Generator, Iterator
from datetime import datetime

# Simule edilmis log satirlari
SAMPLE_LOGS = """
2026-03-22 10:15:23 INFO  [auth] User login successful: user_id=42
2026-03-22 10:15:24 ERROR [db] Connection timeout after 30s
2026-03-22 10:15:25 WARN  [api] Rate limit approaching: 80/100
2026-03-22 10:15:26 INFO  [auth] User login successful: user_id=15
2026-03-22 10:15:27 ERROR [api] Internal server error: NullPointerException
2026-03-22 10:15:28 INFO  [cache] Cache hit ratio: 95%
2026-03-22 10:15:29 ERROR [db] Deadlock detected on table 'orders'
2026-03-22 10:15:30 WARN  [auth] Failed login attempt: user_id=99
2026-03-22 10:15:31 INFO  [api] Request processed in 250ms
2026-03-22 10:15:32 ERROR [auth] Invalid token: expired
""".strip()

def read_lines(text: str) -> Generator[str, None, None]:
    """Metni satir satir yield et (dosya okuma simulasyonu)."""
    for line in text.split("\n"):
        if line.strip():
            yield line.strip()

def parse_log(lines: Iterator[str]) -> Generator[dict, None, None]:
    """Log satirini parse et."""
    # TODO: Her satiri {"timestamp", "level", "module", "message"} dict'ine cevir
    pass

def filter_by_level(logs: Iterator[dict], level: str) -> Generator[dict, None, None]:
    """Belirli seviyedeki loglari filtrele."""
    # TODO
    pass

def filter_by_module(logs: Iterator[dict], module: str) -> Generator[dict, None, None]:
    """Belirli moduldeki loglari filtrele."""
    # TODO
    pass

def format_output(logs: Iterator[dict]) -> Generator[str, None, None]:
    """Loglari formatli string'e cevir."""
    # TODO
    pass

# Test: Pipeline zincirleme
print("=== Tum ERROR loglari ===")
pipeline = format_output(
    filter_by_level(
        parse_log(read_lines(SAMPLE_LOGS)),
        "ERROR"
    )
)
for line in pipeline:
    print(line)

print("\n=== Auth modulu loglari ===")
pipeline = format_output(
    filter_by_module(
        parse_log(read_lines(SAMPLE_LOGS)),
        "auth"
    )
)
for line in pipeline:
    print(line)
```

**Beklenen çıktı:**
```
=== Tum ERROR loglari ===
[ERROR] [db] Connection timeout after 30s
[ERROR] [api] Internal server error: NullPointerException
[ERROR] [db] Deadlock detected on table 'orders'
[ERROR] [auth] Invalid token: expired

=== Auth modulu loglari ===
[INFO] [auth] User login successful: user_id=42
[INFO] [auth] User login successful: user_id=15
[WARN] [auth] Failed login attempt: user_id=99
[ERROR] [auth] Invalid token: expired
```

**İpucu:** Her generator sadece `yield` ile iletir, bellekte tüm veriyi tutmaz. `split()` ile log satırını parçalara ayır.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 7: Retry Decorator ile Exponential Backoff

**Görev:** Başarısız fonksiyonları otomatik olarak tekrar deneyen bir `@retry` decorator yaz. Exponential backoff stratejisi uygulasın.

**Başlangıç kodu:**
```python
import time
import random
from functools import wraps

class RetryExhausted(Exception):
    """Tum denemeler basarisiz oldugunda firlatilir."""
    pass

def retry(max_attempts: int = 3, base_delay: float = 1.0,
          backoff_factor: float = 2.0, exceptions: tuple = (Exception,)):
    """
    Retry decorator with exponential backoff.
    delay = base_delay * (backoff_factor ** attempt)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO:
            # 1. max_attempts kadar dene
            # 2. Basarisiz olursa delay kadar bekle
            # 3. Her denemede delay'i backoff_factor ile carp
            # 4. Sadece belirtilen exception turlerini yakala
            # 5. Tum denemeler basarisiz olursa RetryExhausted firlat
            pass
        return wrapper
    return decorator

# Test: Rastgele basarisiz olan fonksiyon
call_count = 0

@retry(max_attempts=5, base_delay=0.1, backoff_factor=2.0, exceptions=(ConnectionError,))
def unreliable_api_call(endpoint: str) -> dict:
    global call_count
    call_count += 1
    if random.random() < 0.7:  # %70 basarisizlik orani
        raise ConnectionError(f"Baglanti hatasi: {endpoint}")
    return {"status": "ok", "data": [1, 2, 3]}

try:
    result = unreliable_api_call("/api/data")
    print(f"Basarili! Sonuc: {result}")
    print(f"Toplam deneme: {call_count}")
except RetryExhausted as e:
    print(f"Tum denemeler basarisiz: {e}")
    print(f"Toplam deneme: {call_count}")
```

**Beklenen çıktı:**
```
Deneme 1/5 basarisiz: Baglanti hatasi: /api/data (0.1s bekleniyor)
Deneme 2/5 basarisiz: Baglanti hatasi: /api/data (0.2s bekleniyor)
Basarili! Sonuc: {'status': 'ok', 'data': [1, 2, 3]}
Toplam deneme: 3
```

**İpucu:** `time.sleep(delay)` ile bekle. `delay *= backoff_factor` ile artır. Jitter eklemek için `delay * random.uniform(0.5, 1.5)` kullan.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Async Web Scraper

**Görev:** `asyncio` ve `aiohttp` benzeri bir pattern ile birden fazla URL'i paralel olarak çeken bir async scraper yaz.

**Başlangıç kodu:**
```python
import asyncio
import time

async def fetch_url(url: str, delay: float = 0) -> dict:
    """URL'i fetch et (simulasyon)."""
    await asyncio.sleep(delay)  # Network gecikmesi simulasyonu
    # Gercek projede aiohttp kullanilir
    return {
        "url": url,
        "status": 200,
        "size": len(url) * 100,
        "time": delay,
    }

async def fetch_all_sequential(urls: list[str]) -> list[dict]:
    """URL'leri sirayla cek."""
    results = []
    for url in urls:
        result = await fetch_url(url, delay=0.5)
        results.append(result)
    return results

async def fetch_all_parallel(urls: list[str], max_concurrent: int = 3) -> list[dict]:
    """URL'leri paralel cek (semaphore ile sinirli)."""
    # TODO:
    # 1. asyncio.Semaphore(max_concurrent) olustur
    # 2. Her URL icin semaphore ile sinirli task olustur
    # 3. asyncio.gather ile hepsini paralel calistir
    pass

async def main():
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5",
        "https://example.com/page6",
    ]

    # Sirayla
    start = time.time()
    results = await fetch_all_sequential(urls)
    seq_time = time.time() - start
    print(f"Sirayla: {seq_time:.2f}s ({len(results)} URL)")

    # Paralel
    start = time.time()
    results = await fetch_all_parallel(urls, max_concurrent=3)
    par_time = time.time() - start
    print(f"Paralel: {par_time:.2f}s ({len(results)} URL)")
    print(f"Hizlanma: {seq_time / par_time:.1f}x")

asyncio.run(main())
```

**Beklenen çıktı:**
```
Sirayla: 3.00s (6 URL)
Paralel: 1.00s (6 URL)
Hizlanma: 3.0x
```

**İpucu:** `asyncio.Semaphore` ile concurrent task sayısını sınırla. `asyncio.gather(*tasks)` ile tüm task'ları paralel çalıştır.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 9: Functional Programming ile Veri Pipeline

**Görev:** `map`, `filter`, `reduce` ve `functools.partial` kullanarak fonksiyonel bir veri işleme pipeline'ı yaz.

**Başlangıç kodu:**
```python
from functools import reduce, partial
from typing import Callable

# Pipeline builder
class Pipeline:
    def __init__(self, data):
        self.data = data
        self._steps: list[tuple[str, Callable]] = []

    def pipe(self, func: Callable, name: str = "") -> "Pipeline":
        """Pipeline'a adim ekle."""
        # TODO: fonksiyonu kaydet ve self dondur (chaining icin)
        pass

    def execute(self, verbose: bool = False) -> any:
        """Pipeline'i calistir."""
        result = self.data
        for name, func in self._steps:
            result = func(result)
            if verbose:
                preview = str(result)[:60]
                print(f"  [{name}] -> {preview}...")
        return result

# Helper fonksiyonlar
def filter_by(predicate: Callable, data: list) -> list:
    return list(filter(predicate, data))

def map_with(transform: Callable, data: list) -> list:
    return list(map(transform, data))

def sort_by(key: str, reverse: bool = False):
    return lambda data: sorted(data, key=lambda x: x[key], reverse=reverse)

# Test
products = [
    {"name": "Laptop", "price": 15000, "category": "electronics", "stock": 5},
    {"name": "T-Shirt", "price": 200, "category": "clothing", "stock": 50},
    {"name": "Phone", "price": 8000, "category": "electronics", "stock": 0},
    {"name": "Book", "price": 50, "category": "education", "stock": 100},
    {"name": "Tablet", "price": 5000, "category": "electronics", "stock": 12},
    {"name": "Jeans", "price": 400, "category": "clothing", "stock": 30},
    {"name": "Monitor", "price": 3000, "category": "electronics", "stock": 8},
]

result = (
    Pipeline(products)
    .pipe(partial(filter_by, lambda p: p["stock"] > 0), "stokta olanlar")
    .pipe(partial(filter_by, lambda p: p["category"] == "electronics"), "elektronik")
    .pipe(sort_by("price", reverse=True), "fiyata gore sirala")
    .pipe(partial(map_with, lambda p: {**p, "discounted": int(p["price"] * 0.9)}), "indirim uygula")
    .execute(verbose=True)
)

print("\nSonuc:")
for item in result:
    print(f"  {item['name']:10s} {item['price']:>6d} TL -> {item['discounted']:>6d} TL")
```

**Beklenen çıktı:**
```
  [stokta olanlar] -> [{'name': 'Laptop', 'price': 15000, 'catego...
  [elektronik] -> [{'name': 'Laptop', 'price': 15000, 'catego...
  [fiyata gore sirala] -> [{'name': 'Laptop', 'price': 15000, 'catego...
  [indirim uygula] -> [{'name': 'Laptop', 'price': 15000, 'catego...

Sonuc:
  Laptop     15000 TL ->  13500 TL
  Tablet      5000 TL ->   4500 TL
  Monitor     3000 TL ->   2700 TL
```

**İpucu:** `partial(filter_by, lambda p: ...)` ile predicate'i önceden bağla. `Pipeline.pipe()` `self` dönerek method chaining sağlar.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: Descriptor Protocol ile Validated Attributes

**Görev:** Python descriptor protocol kullanarak otomatik validation yapan attribute'lar oluştur.

**Başlangıç kodu:**
```python
class Validated:
    """Descriptor: attribute atanirken validation uygular."""
    def __init__(self, validator: callable, error_msg: str = "Validation failed"):
        self.validator = validator
        self.error_msg = error_msg
        self.attr_name = ""

    def __set_name__(self, owner, name):
        self.attr_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.attr_name, None)

    def __set__(self, obj, value):
        # TODO: Validator'i cagir, basarisiz olursa ValueError firlat
        pass

class Range(Validated):
    """Sayisal degerin belirli aralikta olmasini zorunlu kilar."""
    def __init__(self, min_val: float, max_val: float):
        # TODO: min_val <= value <= max_val kontrolu yapan validator olustur
        pass

class NonEmpty(Validated):
    """String'in bos olmamasini zorunlu kilar."""
    def __init__(self):
        super().__init__(
            validator=lambda v: isinstance(v, str) and len(v.strip()) > 0,
            error_msg="Bos string olamaz"
        )

class Email(Validated):
    """Email formatini dogrular."""
    def __init__(self):
        # TODO: Basit email validation (@ ve . icermeli)
        pass

class Product:
    name = NonEmpty()
    price = Range(0, 1_000_000)
    stock = Range(0, 10_000)
    email = Email()

    def __init__(self, name: str, price: float, stock: int, email: str):
        self.name = name
        self.price = price
        self.stock = stock
        self.email = email

    def __str__(self):
        return f"Product({self.name}, {self.price} TL, stok: {self.stock})"

# Test: Gecerli urun
p = Product("Laptop", 15000, 10, "info@shop.com")
print(p)

# Test: Validation hatalari
test_cases = [
    ("", 100, 5, "a@b.com", "Bos isim"),
    ("Phone", -100, 5, "a@b.com", "Negatif fiyat"),
    ("Tablet", 500, -1, "a@b.com", "Negatif stok"),
    ("Monitor", 3000, 5, "invalid", "Gecersiz email"),
]

for name, price, stock, email, desc in test_cases:
    try:
        p = Product(name, price, stock, email)
        print(f"HATA: {desc} kabul edildi!")
    except ValueError as e:
        print(f"Dogru yakalandi - {desc}: {e}")
```

**Beklenen çıktı:**
```
Product(Laptop, 15000 TL, stok: 10)
Dogru yakalandi - Bos isim: Bos string olamaz
Dogru yakalandi - Negatif fiyat: 0 <= value <= 1000000 olmali
Dogru yakalandi - Negatif stok: 0 <= value <= 10000 olmali
Dogru yakalandi - Gecersiz email: Gecerli email adresi giriniz
```

**İpucu:** `__set_name__` Python 3.6+'da descriptor'a attribute adını otomatik verir. `__get__`/`__set__` ile okuma/yazma kontrol edilir.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Plugin Sistemi ile Decorator Registry

**Görev:** Decorator kullanarak otomatik fonksiyon kaydı yapan bir plugin sistemi yaz.

**Başlangıç kodu:**
```python
class PluginRegistry:
    def __init__(self):
        self._plugins: dict[str, callable] = {}

    def register(self, name: str = None):
        """Fonksiyonu plugin olarak kaydet."""
        def decorator(func):
            plugin_name = name or func.__name__
            self._plugins[plugin_name] = func
            return func
        return decorator

    def run(self, name: str, *args, **kwargs):
        if name not in self._plugins:
            raise KeyError(f"Plugin bulunamadi: {name}")
        return self._plugins[name](*args, **kwargs)

    def list_plugins(self) -> list[str]:
        return list(self._plugins.keys())

# Test
registry = PluginRegistry()

@registry.register("uppercase")
def to_upper(text: str) -> str:
    return text.upper()

@registry.register("reverse")
def reverse_text(text: str) -> str:
    return text[::-1]

@registry.register()
def word_count(text: str) -> int:
    return len(text.split())

print(f"Plugins: {registry.list_plugins()}")
print(f"uppercase: {registry.run('uppercase', 'hello world')}")
print(f"reverse: {registry.run('reverse', 'python')}")
print(f"word_count: {registry.run('word_count', 'hello beautiful world')}")
```

**Beklenen çıktı:**
```
Plugins: ['uppercase', 'reverse', 'word_count']
uppercase: HELLO WORLD
reverse: nohtyp
word_count: 3
```

**İpucu:** `register()` decorator factory olarak çalışır - parametre alıp decorator döner.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 12: AsyncIO ile Concurrent Task Runner

**Görev:** Birden fazla async görevi yöneten, timeout ve hata yönetimi destekleyen bir task runner yaz.

**Başlangıç kodu:**
```python
import asyncio
from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass
class TaskResult:
    name: str
    success: bool
    result: Any = None
    error: str = ""
    duration: float = 0.0

class TaskRunner:
    def __init__(self, max_concurrent: int = 5, timeout: float = 10.0):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.results: list[TaskResult] = []

    async def run_task(self, name: str, coro, semaphore: asyncio.Semaphore) -> TaskResult:
        """Tek bir task'i timeout ve hata yonetimi ile calistir."""
        import time
        start = time.time()
        async with semaphore:
            try:
                result = await asyncio.wait_for(coro, timeout=self.timeout)
                return TaskResult(name, True, result, duration=time.time()-start)
            except asyncio.TimeoutError:
                return TaskResult(name, False, error="Timeout", duration=time.time()-start)
            except Exception as e:
                return TaskResult(name, False, error=str(e), duration=time.time()-start)

    async def run_all(self, tasks: dict[str, Any]) -> list[TaskResult]:
        """Tum task'lari paralel calistir."""
        sem = asyncio.Semaphore(self.max_concurrent)
        coros = [self.run_task(name, coro, sem) for name, coro in tasks.items()]
        self.results = await asyncio.gather(*coros)
        return self.results

    def summary(self):
        success = sum(1 for r in self.results if r.success)
        failed = len(self.results) - success
        total_time = max(r.duration for r in self.results) if self.results else 0
        print(f"\n=== Ozet: {success} basarili, {failed} basarisiz, {total_time:.2f}s ===")

# Test
async def fetch_data(name: str, delay: float, should_fail: bool = False):
    await asyncio.sleep(delay)
    if should_fail:
        raise ConnectionError(f"{name} baglanti hatasi")
    return f"{name} verisi"

async def main():
    runner = TaskRunner(max_concurrent=3, timeout=2.0)
    tasks = {
        "API-1": fetch_data("API-1", 0.5),
        "API-2": fetch_data("API-2", 0.3),
        "API-3": fetch_data("API-3", 0.8, should_fail=True),
        "API-4": fetch_data("API-4", 3.0),  # Timeout olacak
        "API-5": fetch_data("API-5", 0.2),
    }
    results = await runner.run_all(tasks)
    for r in results:
        status = "OK" if r.success else f"FAIL: {r.error}"
        print(f"  {r.name}: {status} ({r.duration:.2f}s)")
    runner.summary()

asyncio.run(main())
```

**Beklenen çıktı:**
```
  API-1: OK (0.50s)
  API-2: OK (0.30s)
  API-3: FAIL: API-3 baglanti hatasi (0.80s)
  API-4: FAIL: Timeout (2.00s)
  API-5: OK (0.20s)

=== Ozet: 3 basarili, 2 basarisiz, 2.00s ===
```

**İpucu:** `asyncio.wait_for(coro, timeout=n)` ile timeout uygula. `asyncio.Semaphore` ile concurrent task sayısını sınırla.

**Zorluk:** Zor
:::

:::must-note
- Decorator = callable alıp callable döndüren higher-order function. `@dec` -> `func = dec(func)`
- `functools.wraps` her zaman kullan: orijinal fonksiyonun `__name__`, `__doc__` bilgilerini korur
- Decorator factory: parametre alan decorator, 3 katmanlı nested fonksiyon gerektirir
- Generator = `yield` ile lazy evaluation. Bellekte tutmaz, tek tek üretir
- Generator expression: `(x for x in ...)` - list comp'un lazy versiyonu
- `itertools`: chain, islice, groupby, product, accumulate - ezberle
- Context manager: `__enter__` ve `__exit__` metodları. `with` bloğu ile kullanılır
- `contextlib.contextmanager`: generator tabanlı kolay context manager oluşturma
- Error handling sırası: `try` -> `except` (spesifikten genele) -> `else` (hata yoksa) -> `finally` (her durumda)
- Custom exception'lar `Exception`'dan türetilmeli, hiyerarşik olmalı
- `asyncio.gather()` = birden fazla coroutine'i eşzamanlı çalıştır, sonuçları topla
- `await asyncio.sleep()` vs `time.sleep()`: biri sadece coroutine'i bekletir, diğeri tüm thread'i bloklar
- `logging` modülü: production'da `print()` yerine her zaman bunu kullan
- Performans: `set` membership O(1), `" ".join()` string birleştirme, `dict.get()` tek arama
- `lru_cache`: otomatik memoization, recursive fonksiyonlarda dramatik hız artışı
:::

:::senior-learns
Bir Senior Developer veya CTO, ileri Python kalıplarını öğrenirken şu yaklaşımı benimser:

1. **CPython kaynak kodunu okur** - Decorator'ların, generator'ların ve context manager'ların CPython'da nasıl implement edildiğini inceler. `dis` modülü ile bytecode analizi yapar. "Sihir yok, sadece protokoller var" prensibini benimser.

2. **Metaprogramming sınırlarını anlar** - Decorator'ları sadece cross-cutting concern'ler için kullanır. Her şeyi decorator yapmak yerine, "Bu decorator fonksiyonun davranışını gizliyor mu?" sorusunu sorar. Okunabilirlik her zaman zekice koddan önce gelir.

3. **Bellek profiling'i günlük alışkanlık yapar** - `tracemalloc`, `memory_profiler` ve `objgraph` ile bellek kullanımını ölçer. Generator pipeline'larının gerçekten bellek tasarrufu sağladığını doğrular. "Ölçmeden optimize etme" prensibi.

4. **asyncio'yu doğru yerde kullanır** - CPU-bound işler için asyncio değil, `multiprocessing` veya `concurrent.futures.ProcessPoolExecutor` kullanır. I/O-bound vs CPU-bound ayrımını her zaman yapar. "Asyncio her şeyi hızlandırır" yanılgısına düşmez.

5. **Exception handling stratejisi belirler** - Proje başında exception hierarchy tasarlar. "Catch late, throw early" prensibini uygular. Her try bloğunun catch ettiği exception'ı loglar. Bare `except:` kullanımını code review'da reddeder.

6. **Production logging altyapısı kurar** - Structured logging (JSON format) kullanır. ELK Stack veya Grafana Loki ile log aggregation yapar. Correlation ID ile distributed tracing uygular. "Loglanmamış hata, olmamış hatadır" prensibi.

**Profesyonel Mindset:** "İleri Python kalıpları, sihirli numaralar değil, yazılım mühendisliği araçlarıdır. Bir decorator yazmadan önce 'Bu gerçekten cross-cutting concern mi?' sor. Generator kullanmadan önce 'Bu veri gerçekten belleğe sığmıyor mu?' sor. Asyncio kullanmadan önce 'Bu gerçekten I/O-bound mu?' sor. Doğru aracı doğru yerde kullanan mühendis, tüm araçları her yerde kullanan mühendisten her zaman üstündür."
:::

:::english
**Teknik Ingilizce - Bu Dersteki Terimler:**

1. **Decorator** (dek-uh-ray-ter) -> Dekoratör / Süsleyici
   *"We use decorators to add cross-cutting concerns like logging and authentication."*

2. **Generator** (jen-uh-ray-ter) -> Üretici / Jeneratör
   *"Generators use lazy evaluation to process large datasets without loading everything into memory."*

3. **Context Manager** (kon-tekst man-ij-er) -> Bağlam Yöneticisi
   *"The context manager ensures that resources are properly released even if an exception occurs."*

4. **Coroutine** (koh-roo-teen) -> Eşyordam
   *"An async function returns a coroutine object that must be awaited."*

5. **Memoization** (mem-oh-ih-zay-shun) -> Bellekleme / Önbellekleme
   *"We applied memoization using lru_cache to avoid redundant computations in the recursive function."*

**Okuma Egzersizi:** Python docs'ta "Functional Programming HOWTO" belgesini oku: https://docs.python.org/3/howto/functional.html

**Yazma Pratigi:** Asagidaki commit mesajini Ingilizce yaz: "Veritabani islemleri icin retry decorator eklendi"
-> Ornek: `feat: add retry decorator for database operations`
:::

:::external-resource
- **Python Docs:** "functools - Higher-order functions" (resmi dokümantasyon, ücretsiz)
- **Real Python:** "Primer on Python Decorators" (detayli rehber, ücretsiz)
- **Python Docs:** "itertools - Functions creating iterators" (resmi dokümantasyon, ücretsiz)
- **Real Python:** "Async IO in Python: A Complete Walkthrough" (kapsamli asyncio rehberi, ücretsiz)
- **Talk Python Training:** "Async Techniques and Examples in Python" (video kurs)
:::
