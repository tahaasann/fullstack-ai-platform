---
id: "mod-02-python/lesson-02"
title: "Veri Tipleri, Type Hints ve OOP"
description: "Python'un veri tiplerini derinlemesine öğren, type hints ile güvenli kod yaz ve OOP prensiplerini profesyonel seviyede uygula."
estimated_minutes: 55
order: 2
tags: ["python", "data-types", "type-hints", "oop", "classes", "inheritance", "dataclasses"]
prerequisites: ["mod-02-python/lesson-01"]
---

# Veri Tipleri, Type Hints ve OOP

:::realworld
Bir backend API yazıyorsun. Kullanıcıdan gelen JSON verisini parse ediyorsun ama bir yerde `None` geldiğini fark etmeden `len()` çağırıyorsun ve production'da patlıyor. Veya bir dict'e yanlış key ile erişiyorsun, hata ancak canlıda ortaya çıkıyor. Bu tarz hataların %80'i veri tiplerini ve type hints'i doğru kullanmamaktan kaynaklanır. Bu derste Python'un tip sistemini derinlemesine öğrenecek, type hints ile hataları daha kod yazarken yakalayacak ve OOP ile profesyonel, bakımı kolay kod yazmayı öğreneceksin.
:::

## Python Veri Tipleri Derinlemesine

Python'da her şey bir object'tir. Bir `int` bile aslında bir sınıfın instance'ıdır. Bu felsefeyi anlamak, Python'u gerçekten kavramanın temelidir.

:::concept[Dinamik Tipleme (İng: Dynamic Typing)]
Python, değişkenin tipini çalışma zamanında (runtime) belirler, derleme zamanında (compile time) değil. Bir değişkene önce `int`, sonra `str` atayabilirsin.

**Türkçe karşılığı:** Dinamik Tipleme
**Ne işe yarar:** Hızlı prototipleme sağlar ama büyük projelerde hatalara yol açabilir
**Gerçek hayat benzetmesi:** Etiket yapıştırmak gibi - aynı kutuya önce "elma" etiketi yapıştırırsın, sonra söküp "portakal" yapıştırabilirsin. Kutu aynı ama içerik ve etiket değişir.
:::

### Temel Tipler (Primitive-like Types)

:::code[python]{title="Temel Veri Tipleri"}
# int - Tam sayılar (sınırsız büyüklük!)
sayi: int = 42
buyuk_sayi: int = 10 ** 100  # Python'da integer overflow yok!
binary: int = 0b1010         # 10
hexadecimal: int = 0xFF      # 255
octal: int = 0o17            # 15
okunabilir: int = 1_000_000  # Alt çizgi ile okunabilirlik (1 milyon)

# float - Ondalıklı sayılar (IEEE 754 double-precision)
pi: float = 3.14159
bilimsel: float = 2.5e10     # 25000000000.0
sonsuz: float = float('inf') # Sonsuz
nan: float = float('nan')    # Not a Number

# str - String (immutable, Unicode destekli)
isim: str = "Python"
emoji: str = "Merhaba 🐍"    # Unicode tam destek
cok_satirli: str = """
Bu bir
çok satırlı
string'dir.
"""

# bool - True veya False (int'in alt sınıfı!)
aktif: bool = True
print(True + True)   # 2! Çünkü bool, int'ten türer
print(isinstance(True, int))  # True

# None - Değer yokluğu (null'un Python karşılığı)
sonuc: None = None
print(type(None))    # <class 'NoneType'>
:::

:::warning
`float` hassasiyet sorunu her dilde var ama Python'da özellikle dikkat et:
```python
print(0.1 + 0.2)          # 0.30000000000000004
print(0.1 + 0.2 == 0.3)   # False!

# Çözüm 1: decimal modülü
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))  # True

# Çözüm 2: math.isclose
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```
Finansal hesaplamalarda KESİNLİKLE `Decimal` kullan. `float` ile para hesabı yapma!
:::

### Collection Tipleri

:::code[python]{title="Collection Veri Tipleri"}
# list - Sıralı, değiştirilebilir (mutable), tekrar eden öğeler olabilir
sayilar: list[int] = [1, 2, 3, 4, 5]
karisik: list = [1, "iki", 3.0, True, None]  # Farklı tipler olabilir

# tuple - Sıralı, değiştirilemez (immutable)
koordinat: tuple[float, float] = (41.0, 29.0)
tek_elemanli: tuple[int] = (42,)  # Virgül şart! (42) sadece parantez içi int'tir

# dict - Anahtar-değer çifti, sıralı (Python 3.7+)
kullanici: dict[str, str] = {
    "ad": "Taha",
    "sehir": "Trabzon",
    "meslek": "Developer"
}

# set - Sırasız, benzersiz öğeler, mutable
diller: set[str] = {"Python", "JavaScript", "TypeScript"}
diller.add("Go")
diller.add("Python")  # Zaten var, eklenmez
print(len(diller))    # 4

# frozenset - Immutable set (dict key'i olarak kullanılabilir)
sabit_set: frozenset[int] = frozenset([1, 2, 3])
# sabit_set.add(4)  # AttributeError! Değiştirilemez.
:::

### Mutable vs Immutable

:::concept[Mutable vs Immutable (İng: Mutable vs Immutable)]
Mutable (değiştirilebilir) objeler oluşturulduktan sonra değiştirilebilir. Immutable (değiştirilemez) objeler oluşturulduktan sonra değiştirilemez; yeni bir obje yaratılır.

**Türkçe karşılığı:** Değiştirilebilir vs Değiştirilemez
**Ne işe yarar:** Veri güvenliği, hashability, thread safety sağlar
**Gerçek hayat benzetmesi:** Mutable = beyaz tahta (silip tekrar yazabilirsin), Immutable = basılmış kitap (değiştirmek için yeni baskı yapman gerek)
:::

:::comparison
| Immutable (Değiştirilemez) | Mutable (Değiştirilebilir) |
|---------------------------|--------------------------|
| `int`, `float`, `str`, `bool` | `list`, `dict`, `set` |
| `tuple`, `frozenset`, `bytes` | `bytearray` |
| Hashable (dict key olabilir) | Hashable değil (dict key olamaz) |
| Thread-safe | Thread-safe değil |
| Bellekte paylaşılabilir | Her instance ayrı |

**Neden önemli?** Immutable objeler dict key'i ve set elemanı olarak kullanılabilir. Mutable objeler ise beklenmedik side effect'lere yol açabilir.
:::

:::beginner-mistake
Mutable default argument tuzağı Python'un en meşhur gotcha'sıdır:
```python
# YANLIŞ - Aynı liste her çağrıda paylaşılır!
def listeye_ekle(eleman, liste=[]):
    liste.append(eleman)
    return liste

print(listeye_ekle(1))  # [1]
print(listeye_ekle(2))  # [1, 2] - BUG! [2] beklenirdi

# DOĞRU - None kullan, fonksiyon içinde oluştur
def listeye_ekle(eleman, liste=None):
    if liste is None:
        liste = []
    liste.append(eleman)
    return liste
```
Bu hata junior'ların mülakatlarında en sık karşılaştığı sorulardan biridir!
:::

## Type Hints ve mypy

:::concept[Type Hints (İng: Type Annotations)]
Type hints, Python 3.5+ ile gelen ve değişkenlerin, fonksiyon parametrelerinin ve dönüş değerlerinin beklenen tipini belirten syntax'tır. Runtime'da zorlama yapılmaz ama mypy gibi araçlarla statik analiz yapılabilir.

**Türkçe karşılığı:** Tip İpuçları / Tip Belirleyiciler
**Ne işe yarar:** Hataları daha kod yazarken yakalar, IDE otomatik tamamlamayı güçlendirir, dokümantasyon görevi görür
**Gerçek hayat benzetmesi:** Bir kutunun üzerine "Sadece kitap koyun" yazmak gibi - kimse seni fiziksel olarak engellemez ama uyarı vardır
:::

:::tip
2026 itibarıyla Python ekosisteminde type hints neredeyse zorunlu hale geldi. FastAPI, Pydantic, SQLModel gibi modern framework'ler type hints üzerine kurulu. Büyük şirketlerin CI/CD pipeline'larında mypy kontrolü standart. Type hints'siz Python kodu yazmak artık "unprofessional" kabul ediliyor.
:::

:::code[python]{title="Type Hints Kullanımı"}
from typing import Optional, Union

# Temel type hints
isim: str = "Taha"
yas: int = 28
aktif: bool = True

# Fonksiyon type hints
def selamla(isim: str, resmi: bool = False) -> str:
    if resmi:
        return f"Sayın {isim}, hoş geldiniz."
    return f"Merhaba {isim}!"

# Collection type hints (Python 3.9+ built-in syntax)
sayilar: list[int] = [1, 2, 3]
kullanici: dict[str, str | int] = {"ad": "Taha", "yas": 28}
koordinat: tuple[float, float] = (41.0, 29.0)
diller: set[str] = {"Python", "JS"}

# Optional - None olabilir demek (Union[X, None] kısaltması)
sonuc: Optional[str] = None         # str veya None
# Python 3.10+ alternatif syntax:
sonuc2: str | None = None

# Union - birden fazla tip olabilir
deger: Union[int, float] = 3.14
# Python 3.10+ alternatif:
deger2: int | float = 3.14

# Callable type hint
from typing import Callable
def uygula(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# TypeAlias (Python 3.12+ 'type' keyword)
type KullaniciDict = dict[str, str | int | None]
type Koordinat = tuple[float, float]
:::

:::code[python]{title="mypy ile Statik Tip Kontrolü"}
# dosya: hesapla.py
def bolme(a: int, b: int) -> float:
    return a / b

sonuc: str = bolme(10, 3)  # mypy HATA: float tipini str'ye atayamazsın

# Terminal:
# $ uv add mypy
# $ uv run mypy hesapla.py
# hesapla.py:4: error: Incompatible types in assignment
#   (expression has type "float", variable has type "str")

# mypy.ini veya pyproject.toml konfigürasyonu:
# [mypy]
# strict = true
# warn_return_any = true
# disallow_untyped_defs = true
:::

## String İşlemleri ve f-strings

:::code[python]{title="f-strings ve String Formatting"}
isim = "Taha"
yas = 28
maas = 45000.5678

# f-string (Python 3.6+) - EN ÇOK KULLANILAN
print(f"Merhaba {isim}, yaşın {yas}")
print(f"Maaş: {maas:.2f} TL")           # Maaş: 45000.57 TL
print(f"Maaş: {maas:,.2f} TL")          # Maaş: 45,000.57 TL
print(f"{'Sol':>20}")                     # 20 karakter sağa yasla
print(f"Debug: {isim!r}")               # Debug: 'Taha' (repr çıktısı)
print(f"{yas = }")                       # yas = 28 (debug için harika!)

# f-string içinde expression
print(f"Sonuç: {2 ** 10}")              # Sonuç: 1024
print(f"Büyük: {isim.upper()}")          # Büyük: TAHA

# Çok satırlı f-string
mesaj = (
    f"Kullanıcı: {isim}\n"
    f"Yaş: {yas}\n"
    f"Durum: {'Aktif' if yas > 18 else 'Pasif'}"
)

# String methods
metin = "  Merhaba Dünya  "
print(metin.strip())           # "Merhaba Dünya"
print(metin.lower())           # "  merhaba dünya  "
print(metin.upper())           # "  MERHABA DÜNYA  "
print(metin.replace("Dünya", "Python"))
print("Merhaba".startswith("Mer"))  # True
print("Dünya".endswith("nya"))      # True
print("a-b-c".split("-"))          # ["a", "b", "c"]
print("-".join(["a", "b", "c"]))   # "a-b-c"
print("python".capitalize())       # "Python"
print("Hello World".title())       # "Hello World" -> Her kelimenin ilk harfi büyük
:::

## Comprehensions

:::code[python]{title="List, Dict ve Set Comprehensions"}
# List comprehension
kareler = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Filtreleme ile
cift_kareler = [x ** 2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# Dict comprehension
ogrenciler = ["Ali", "Veli", "Ayşe"]
notlar = [85, 92, 78]
not_dict = {isim: not_ for isim, not_ in zip(ogrenciler, notlar)}
# {"Ali": 85, "Veli": 92, "Ayşe": 78}

# Set comprehension
harfler = {harf.lower() for harf in "Merhaba Dünya"}
# {'m', 'e', 'r', 'h', 'a', 'b', ' ', 'd', 'ü', 'n', 'y'}

# Nested comprehension (matris oluşturma)
matris = [[i * j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [4, 5, 6], [7, 8, 9]] -- çarpım tablosu gibi

# Generator expression (bellek dostu - lazy evaluation)
toplam = sum(x ** 2 for x in range(1_000_000))
# Liste oluşturmaz, tek tek hesaplar - bellek tasarrufu!
:::

:::tip
Comprehension'lar güçlüdür ama okunabilirliği korumalısın. 2 satırdan fazla veya anlaşılması 5 saniyeden uzun süren comprehension'ları normal döngüye çevir. Takımda herkesin anlayacağı kod, zekice yazılmış ama anlaşılmaz koddan her zaman daha iyidir.
:::

## OOP: Object-Oriented Programming

### Class Tanımı ve Temel Yapı

:::concept[Class (İng: Class)]
Class, bir veri yapısı ve bu veriler üzerinde çalışan fonksiyonları bir arada tutan şablondur. Instance ise bu şablondan oluşturulan somut nesnelerdir.

**Türkçe karşılığı:** Sınıf
**Ne işe yarar:** Kodu organize eder, yeniden kullanılabilirlik sağlar, gerçek dünya kavramlarını modeller
**Gerçek hayat benzetmesi:** Class = araba tasarım çizimi, Instance = o çizimden üretilen gerçek araba
:::

:::code[python]{title="Class Tanımı ve __init__"}
class Kullanici:
    # Class variable - tüm instance'lar paylaşır
    platform: str = "DevPortal"
    toplam_kullanici: int = 0

    def __init__(self, isim: str, email: str, yas: int) -> None:
        # Instance variables - her instance'a özel
        self.isim: str = isim
        self.email: str = email
        self.yas: int = yas
        self._aktif: bool = True          # Convention: "private" (erişilebilir ama dokunma)
        self.__sifre: str = "gizli123"    # Name mangling: _Kullanici__sifre olarak saklanır
        Kullanici.toplam_kullanici += 1

    def selamla(self) -> str:
        return f"Merhaba, ben {self.isim}!"

    def bilgi(self) -> dict[str, str | int]:
        return {
            "isim": self.isim,
            "email": self.email,
            "yas": self.yas,
            "platform": self.platform
        }

# Instance oluşturma
taha = Kullanici("Taha", "taha@example.com", 28)
ayse = Kullanici("Ayşe", "ayse@example.com", 25)

print(taha.selamla())           # Merhaba, ben Taha!
print(Kullanici.toplam_kullanici)  # 2 (class variable)
print(taha.platform)            # DevPortal (class variable'a instance üzerinden erişim)
:::

:::beginner-mistake
`self` sadece bir convention, özel bir keyword değil. Ama KESİNLİKLE `self` kullan, başka isim vermek (mesela `this`) topluluk normlarına aykırıdır ve code review'da reddedilir. Ayrıca `__init__` içinde `self.x = x` yazmayı unutmak en yaygın hatadır - parametreyi alırsın ama instance'a atamazsın, sonra `AttributeError` alırsın.
:::

### Kalıtım (Inheritance)

:::code[python]{title="Single ve Multiple Inheritance"}
# Single Inheritance
class Calisan(Kullanici):
    def __init__(self, isim: str, email: str, yas: int, departman: str) -> None:
        super().__init__(isim, email, yas)  # Parent'ın __init__'ini çağır
        self.departman: str = departman

    def selamla(self) -> str:  # Method overriding
        return f"{super().selamla()} {self.departman} departmanındayım."


# Multiple Inheritance
class Loglayici:
    def log(self, mesaj: str) -> None:
        print(f"[LOG] {mesaj}")

class Bildirimci:
    def bildir(self, mesaj: str) -> None:
        print(f"[BILDIRIM] {mesaj}")

class Yonetici(Calisan, Loglayici, Bildirimci):
    def __init__(self, isim: str, email: str, yas: int, departman: str) -> None:
        super().__init__(isim, email, yas, departman)
        self.takim: list[Calisan] = []

    def eleman_ekle(self, calisan: Calisan) -> None:
        self.takim.append(calisan)
        self.log(f"{calisan.isim} takıma eklendi")
        self.bildir(f"Yeni eleman: {calisan.isim}")

# MRO (Method Resolution Order)
print(Yonetici.__mro__)
# Yonetici -> Calisan -> Kullanici -> Loglayici -> Bildirimci -> object
:::

:::warning
Multiple inheritance güçlü ama tehlikelidir. "Diamond Problem" olarak bilinen karmaşık kalıtım ağaçlarından kaçın. Python MRO (C3 Linearization) ile bunu çözer ama kodun okunabilirliğini ciddi şekilde düşürür. Pratikte composition (bileşim) genellikle inheritance'tan (kalıtım) daha iyidir: "Favor composition over inheritance" prensibi.
:::

### Polimorfizm, Encapsulation, Abstraction

:::code[python]{title="OOP'nin Üç Temel Prensibi"}
from abc import ABC, abstractmethod

# ABSTRACTION - Abstract Base Class
class Sekil(ABC):
    @abstractmethod
    def alan(self) -> float:
        pass

    @abstractmethod
    def cevre(self) -> float:
        pass

    def bilgi(self) -> str:
        return f"Alan: {self.alan():.2f}, Çevre: {self.cevre():.2f}"

# POLYMORPHISM - Aynı interface, farklı davranış
class Dikdortgen(Sekil):
    def __init__(self, en: float, boy: float) -> None:
        self.en = en
        self.boy = boy

    def alan(self) -> float:
        return self.en * self.boy

    def cevre(self) -> float:
        return 2 * (self.en + self.boy)

class Daire(Sekil):
    def __init__(self, yaricap: float) -> None:
        self.yaricap = yaricap

    def alan(self) -> float:
        import math
        return math.pi * self.yaricap ** 2

    def cevre(self) -> float:
        import math
        return 2 * math.pi * self.yaricap

# Polimorfizm: farklı sınıflar, aynı arayüz
sekiller: list[Sekil] = [Dikdortgen(5, 3), Daire(7)]
for sekil in sekiller:
    print(sekil.bilgi())  # Her biri kendi alan/çevre'sini hesaplar

# ENCAPSULATION - Property decorator ile
class BankaHesabi:
    def __init__(self, sahip: str, bakiye: float = 0) -> None:
        self._sahip = sahip
        self._bakiye = bakiye  # "protected"

    @property
    def bakiye(self) -> float:
        return self._bakiye

    @bakiye.setter
    def bakiye(self, miktar: float) -> None:
        if miktar < 0:
            raise ValueError("Bakiye negatif olamaz!")
        self._bakiye = miktar

    def para_yatir(self, miktar: float) -> None:
        if miktar <= 0:
            raise ValueError("Yatırılacak miktar pozitif olmalı!")
        self._bakiye += miktar

hesap = BankaHesabi("Taha", 1000)
print(hesap.bakiye)     # 1000 (property getter)
hesap.para_yatir(500)
print(hesap.bakiye)     # 1500
# hesap.bakiye = -100   # ValueError: Bakiye negatif olamaz!
:::

### Magic Methods (Dunder Methods)

:::code[python]{title="Magic Methods"}
class Urun:
    def __init__(self, isim: str, fiyat: float, stok: int = 0) -> None:
        self.isim = isim
        self.fiyat = fiyat
        self.stok = stok

    def __str__(self) -> str:
        """Kullanıcıya gösterilecek güzel string (print, f-string)"""
        return f"{self.isim} - {self.fiyat:.2f} TL"

    def __repr__(self) -> str:
        """Geliştiriciye gösterilecek debug string (terminal, log)"""
        return f"Urun(isim='{self.isim}', fiyat={self.fiyat}, stok={self.stok})"

    def __eq__(self, other: object) -> bool:
        """Eşitlik kontrolü (==)"""
        if not isinstance(other, Urun):
            return NotImplemented
        return self.isim == other.isim and self.fiyat == other.fiyat

    def __len__(self) -> int:
        """len() fonksiyonu ile kullanım"""
        return self.stok

    def __iter__(self):
        """Ürün bilgilerini iterate etme"""
        yield ("isim", self.isim)
        yield ("fiyat", self.fiyat)
        yield ("stok", self.stok)

    def __lt__(self, other: "Urun") -> bool:
        """Karşılaştırma: < operatörü (sıralama için)"""
        return self.fiyat < other.fiyat

    def __add__(self, other: "Urun") -> float:
        """Toplama: + operatörü"""
        return self.fiyat + other.fiyat

# Kullanım
laptop = Urun("Laptop", 35000, stok=10)
telefon = Urun("Telefon", 25000, stok=20)

print(str(laptop))        # Laptop - 35000.00 TL
print(repr(laptop))       # Urun(isim='Laptop', fiyat=35000, stok=10)
print(len(laptop))        # 10 (stok)
print(laptop == telefon)  # False
print(laptop + telefon)   # 60000
print(sorted([laptop, telefon]))  # Telefon önce (fiyata göre sıralama)

for key, val in laptop:
    print(f"{key}: {val}")
:::

:::deha-tip
`__repr__` her zaman tanımla, `__str__` opsiyonel. Eğer sadece birini tanımlayacaksan `__repr__` olsun. Çünkü `__str__` yoksa Python otomatik olarak `__repr__`'ı kullanır ama tersi geçerli değil. `__repr__` çıktısı ideal olarak `eval()` ile tekrar obje oluşturabilecek formatta olmalıdır: `Urun(isim='Laptop', fiyat=35000, stok=10)`.
:::

### Dataclasses

:::code[python]{title="@dataclass ile Modern Class Tanımı"}
from dataclasses import dataclass, field

# Geleneksel yol: 20+ satır boilerplate
# @dataclass ile: 5 satır, aynı işlevsellik

@dataclass
class Kullanici:
    isim: str
    email: str
    yas: int
    aktif: bool = True
    roller: list[str] = field(default_factory=list)  # Mutable default için field kullan!

    def tam_bilgi(self) -> str:
        return f"{self.isim} ({self.email})"

# Otomatik olarak şunları alırsın:
# - __init__ (tüm field'ları parametre olarak alır)
# - __repr__ (debug-friendly string)
# - __eq__ (field'lara göre eşitlik karşılaştırması)

k1 = Kullanici("Taha", "taha@dev.com", 28)
k2 = Kullanici("Taha", "taha@dev.com", 28)
print(k1)          # Kullanici(isim='Taha', email='taha@dev.com', yas=28, aktif=True, roller=[])
print(k1 == k2)    # True (otomatik __eq__)

# Frozen dataclass - Immutable (Hashable olur!)
@dataclass(frozen=True)
class Koordinat:
    x: float
    y: float

k = Koordinat(41.0, 29.0)
# k.x = 50  # FrozenInstanceError! Değiştirilemez.

# Sıralama desteği
@dataclass(order=True)
class Ogrenci:
    not_ortalamasi: float
    isim: str = field(compare=False)  # Sıralamada ismi kullanma

ogrenciler = [
    Ogrenci(3.5, "Ali"),
    Ogrenci(3.9, "Veli"),
    Ogrenci(3.2, "Ayşe")
]
print(sorted(ogrenciler))  # not_ortalamasi'na göre sıralı
:::

:::tip
2026'da yeni Python projelerinde basit veri taşıyıcı sınıflar için `@dataclass` kullan. Validation gerekiyorsa Pydantic `BaseModel` kullan. Manual `__init__`, `__repr__`, `__eq__` yazmak artık gereksiz boilerplate. `frozen=True` ile immutable, hashable objeler elde edebilirsin.
:::

## Python vs JavaScript OOP Karşılaştırması

:::comparison
| Özellik | Python | JavaScript |
|---------|--------|------------|
| Class syntax | `class Foo:` | `class Foo {}` |
| Constructor | `__init__(self)` | `constructor()` |
| Instance referans | `self` (explicit) | `this` (implicit, context'e bağlı) |
| Private field | `_convention` / `__name_mangling` | `#privateField` (ES2022+) |
| Abstract class | `ABC` + `@abstractmethod` | Yok (TypeScript'te var) |
| Multiple inheritance | Destekler (MRO ile) | Desteklemez (mixin pattern ile taklit) |
| Static method | `@staticmethod` | `static methodName()` |
| Class method | `@classmethod` | Yok (workaround'lar var) |
| Property | `@property` decorator | `get` / `set` keyword |
| Dataclass | `@dataclass` | Yok (TypeScript interface/type var) |
| Type system | Type hints + mypy (opsiyonel) | TypeScript (ayrı dil) |

**Temel fark:** Python'da `self` açıkça her metoda parametre olarak yazılır. JavaScript'te `this` otomatik bağlanır ama context kaybı sorunu yaşanabilir (arrow function çözümü). Python'un `self`'i daha açık ve güvenlidir.
:::

:::interview
**Mülakat Sorusu:** "Python'da mutable default argument tehlikesi nedir? Örnek verin."

**Beklenen cevap:**
Python'da fonksiyon tanımı bir kez değerlendirilir (evaluate edilir). Default argüman olarak mutable bir obje (list, dict, set) verirseniz, bu obje fonksiyon tanımlanırken bir kez oluşturulur ve her çağrıda aynı obje paylaşılır. Bu, beklenmedik davranışlara yol açar. Çözüm olarak `None` default değer verilir ve fonksiyon içinde yeni obje oluşturulur. Bu konu Python'un "gotcha" listesinin en başında gelir.

**Mülakat Sorusu:** "Bir class'ın `__eq__` metodunu override ettiğinizde `__hash__` metodu ne olur?"

**Beklenen cevap:**
Python'da `__eq__` override edildiğinde `__hash__` otomatik olarak `None` yapılır ve obje unhashable olur (set'e eklenemez, dict key'i olamaz). Eğer objenin hashable olmasını istiyorsanız, `__hash__`'i de tanımlamanız gerekir. `@dataclass(frozen=True)` bunu otomatik olarak halleder.
:::

:::exercise
1. Bir `Kitap` dataclass'ı oluştur: `baslik`, `yazar`, `sayfa_sayisi`, `fiyat`, `yayinevi` field'ları olsun. `frozen=True` kullan.
2. 5 kitap oluştur ve bir listeye ekle. `sorted()` ile fiyata göre sırala.
3. Bir `Kutuphane` sınıfı yaz: kitap ekleme, arama (başlık veya yazar ile), toplam kitap sayısı (`__len__`), ve string temsili (`__str__`) magic method'larını implement et.
4. `Kutuphane` sınıfına `__contains__` magic method'u ekle: `kitap in kutuphane` syntax'ı ile kitap arama yapılabilsin.
5. Tüm fonksiyonlara ve parametrelere type hints ekle. `mypy --strict` ile kontrol et.

---

### Alıştırma 2: Immutable vs Mutable — Çıktıyı Tahmin Et (Kolay)

Aşağıdaki kodun çıktısını **çalıştırmadan** tahmin et. Sonra çalıştırarak doğrula:

```python
# Senaryo 1: Shallow copy tuzağı
original = [[1, 2, 3], [4, 5, 6]]
kopya = original.copy()
kopya[0].append(99)
print(original)  # Çıktı ne olur?
print(kopya)     # Çıktı ne olur?

# Senaryo 2: Tuple içindeki mutable eleman
t = (1, [2, 3], "hello")
# t[1].append(4)  # Bu çalışır mı? Neden?
# t[0] = 10       # Bu çalışır mı? Neden?

# Senaryo 3: Mutable default argument tuzağı
def ekle(eleman, liste=[]):
    liste.append(eleman)
    return liste

print(ekle(1))       # Çıktı?
print(ekle(2))       # Çıktı?
print(ekle(3, []))   # Çıktı?
print(ekle(4))       # Çıktı?
```

**Beklenen sonuç:** Her senaryonun çıktısını doğru tahmin et ve **neden** o çıktıyı verdiğini açıkla. Senaryo 3'ü `None` default ile düzelt.

---

### Alıştırma 3: Dataclass ile Validation ve Protocol (Zor)

```python
from dataclasses import dataclass, field
from typing import Protocol
from decimal import Decimal

# 1. Aşağıdaki Product dataclass'ını tamamla:
@dataclass
class Product:
    name: str
    price: Decimal
    stock: int
    category: str
    # TODO: __post_init__ ile validation ekle:
    #   - price negatif olamaz
    #   - stock negatif olamaz
    #   - name boş string olamaz
    #   - category şu değerlerden biri olmalı: "electronics", "clothing", "food"

# 2. Bir Discountable Protocol tanımla:
class Discountable(Protocol):
    """Indirim uygulanabilir herhangi bir nesne"""
    # TODO: apply_discount(self, percentage: float) -> Decimal metodunu tanımla

# 3. Product'a Discountable Protocol'ü uygula (explicit inheritance OLMADAN)

# 4. Bir apply_bulk_discount fonksiyonu yaz:
def apply_bulk_discount(items: list[Discountable], percentage: float) -> list[Decimal]:
    """Herhangi bir Discountable nesnesine toplu indirim uygula"""
    # TODO: Implement
    pass

# Test:
p1 = Product("Laptop", Decimal("15000.00"), 10, "electronics")
p2 = Product("T-Shirt", Decimal("200.00"), 50, "clothing")
# apply_bulk_discount([p1, p2], 15.0) → [Decimal("12750.00"), Decimal("170.00")]
# Product("", Decimal("-100"), -5, "invalid") → ValueError fırlatmalı
```

**Beklenen sonuç:** `mypy --strict` ile hatasız geçmeli. Protocol ile structural subtyping çalışmalı. Geçersiz veriler `ValueError` fırlatmalı.
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdakilerden hangisi immutable bir veri tipidir?"
options:
  - "list"
  - "dict"
  - "tuple"
  - "set"
correct: 2
explanation: "tuple immutable'dır - oluşturulduktan sonra elemanları değiştirilemez, eklenemez veya çıkarılamaz. list, dict ve set ise mutable'dır."
:::

:::knowledge-check
type: multiple_choice
question: "@dataclass decorator'ı otomatik olarak hangi magic method'ları oluşturur?"
options:
  - "Sadece __init__"
  - "__init__, __repr__ ve __eq__"
  - "__init__, __str__ ve __hash__"
  - "__init__, __repr__, __eq__ ve __lt__"
correct: 1
explanation: "@dataclass varsayılan olarak __init__, __repr__ ve __eq__ oluşturur. __lt__ (sıralama) için order=True, __hash__ için frozen=True veya unsafe_hash=True gerekir. __str__ oluşturulmaz, __repr__ kullanılır."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6

### Prompt Ornekleri

**1. Konuyu Derinlemesine Anla:**
> "Python'da mutable ve immutable tiplerin bellek yonetimi acisindan farklarini anlat. Neden tuple list'ten daha hizli? Mutable default argument tuzagi neden olusur ve CPython bu default degerleri nerede saklar?"

*Neden:* Tip sisteminin iç isleyisini anlamak, production'da rastlanan gotcha'lari onceden fark etmeni saglar

**2. Pratik Uygulama:**
> "Bir e-ticaret uygulamasi icin Urun, Sepet ve Siparis siniflarini @dataclass kullanarak tasarla. Type hints ekle, __str__ ve __eq__ magic method'larini implement et. frozen=True ne zaman kullanmaliyim?"

*Follow-up:* "Bu siniflar arasindaki iliskiyi composition ile kur. Neden inheritance yerine composition tercih etmeliyim?"

**3. Mukemmellik Icin:**
> "Python'da Protocol (typing.Protocol) ile ABC arasindaki farklari structural subtyping ve nominal subtyping acisindan acikla. Hangi durumda hangisini kullanmaliyim? Go'nun interface yaklasimi ile karsilastir."

### Pair Programming Ipucu
OOP tasarimi yaparken AI'a class kodunu yapistir: "Bu sinif tasarimimi incele. SOLID prensiplerine uygun mu? Type hints eksik mi? @dataclass kullanarak nasil basitlestirebilirim?"
:::

:::exercise
### Alıştırma 4: Type-Safe Dictionary Wrapper

**Görev:** Python dictionary'sini type-safe bir şekilde kullanan bir wrapper sınıfı yaz. Yanlış tipte değer atanmaya çalışılırsa hata fırlatsın.

**Başlangıç kodu:**
```python
from typing import TypeVar, Generic

T = TypeVar("T")

class TypedDict(Generic[T]):
    def __init__(self, value_type: type):
        self.value_type = value_type
        self._data: dict[str, T] = {}

    def set(self, key: str, value: T) -> None:
        # TODO: value'nun tipi self.value_type degilse TypeError firlat
        pass

    def get(self, key: str, default: T = None) -> T | None:
        return self._data.get(key, default)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __str__(self) -> str:
        return f"TypedDict[{self.value_type.__name__}]({self._data})"

# Test
scores = TypedDict(int)
scores.set("math", 95)
scores.set("physics", 87)
print(scores)
print(f"math: {scores.get('math')}")
print(f"Toplam: {len(scores)} ders")

try:
    scores.set("english", "ninety")  # TypeError firlatmali!
except TypeError as e:
    print(f"Hata yakalandi: {e}")

names = TypedDict(str)
names.set("user1", "Ahmet")
print(f"\n{names}")
```

**Beklenen çıktı:**
```
TypedDict[int]({'math': 95, 'physics': 87})
math: 95
Toplam: 2 ders
Hata yakalandi: Expected int, got str
TypedDict[str]({'user1': 'Ahmet'})
```

**İpucu:** `isinstance(value, self.value_type)` ile tip kontrolü yap.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: Linked List Implementasyonu

**Görev:** Type hints ile tam donanımlı bir Singly Linked List implementasyonu yaz. `__iter__`, `__len__`, `__contains__` magic method'larını desteklesin.

**Başlangıç kodu:**
```python
from typing import TypeVar, Generic, Iterator

T = TypeVar("T")

class Node(Generic[T]):
    def __init__(self, data: T):
        self.data = data
        self.next: Node[T] | None = None

class LinkedList(Generic[T]):
    def __init__(self):
        self.head: Node[T] | None = None
        self._size: int = 0

    def append(self, data: T) -> None:
        """Sona eleman ekle."""
        # TODO
        pass

    def prepend(self, data: T) -> None:
        """Basa eleman ekle."""
        # TODO
        pass

    def delete(self, data: T) -> bool:
        """Ilk eslesen elemani sil. Silindiyse True dondur."""
        # TODO
        pass

    def reverse(self) -> None:
        """Listeyi yerinde tersine cevir."""
        # TODO
        pass

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        # TODO: yield ile her eleman uzerinden gec
        pass

    def __contains__(self, data: T) -> bool:
        # TODO
        pass

    def __str__(self) -> str:
        return " -> ".join(str(item) for item in self) + " -> None"

# Test
ll = LinkedList[int]()
for num in [10, 20, 30, 40, 50]:
    ll.append(num)

print(f"Liste: {ll}")
print(f"Uzunluk: {len(ll)}")
print(f"30 var mi: {30 in ll}")

ll.prepend(5)
print(f"Prepend 5: {ll}")

ll.delete(30)
print(f"Delete 30: {ll}")

ll.reverse()
print(f"Reversed: {ll}")
```

**Beklenen çıktı:**
```
Liste: 10 -> 20 -> 30 -> 40 -> 50 -> None
Uzunluk: 5
30 var mi: True
Prepend 5: 5 -> 10 -> 20 -> 30 -> 40 -> 50 -> None
Delete 30: 5 -> 10 -> 20 -> 40 -> 50 -> None
Reversed: 50 -> 40 -> 20 -> 10 -> 5 -> None
```

**İpucu:** `reverse()` için üç pointer kullan: `prev`, `current`, `next_node`. Her adımda `current.next = prev` yap.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: Mixin ile Loglama ve Serialization

**Görev:** Mixin pattern kullanarak modüler sınıflar oluştur. LogMixin, SerializerMixin ve ValidatorMixin yaz.

**Başlangıç kodu:**
```python
import json
from datetime import datetime

class LogMixin:
    """Her metodun cagrilisini logla."""
    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.__class__.__name__}: {message}")

class SerializerMixin:
    """Objeyi JSON'a cevir ve JSON'dan olustur."""
    def to_json(self) -> str:
        # TODO: __dict__'i JSON string'e cevir
        pass

    @classmethod
    def from_json(cls, json_str: str):
        # TODO: JSON string'den obje olustur
        pass

class ValidatorMixin:
    """Alanlari dogrula."""
    _validators: dict = {}

    def validate(self) -> list[str]:
        """Tum validation kurallarini kontrol et. Hata mesajlarini dondur."""
        errors = []
        # TODO: _validators dict'indeki kurallari uygula
        pass
        return errors

class User(LogMixin, SerializerMixin, ValidatorMixin):
    _validators = {
        "name": lambda v: len(v) >= 2,
        "email": lambda v: "@" in v,
        "age": lambda v: 0 < v < 150,
    }

    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age

    def update_email(self, new_email: str):
        self.log(f"Email guncelleniyor: {self.email} -> {new_email}")
        self.email = new_email

# Test
user = User("Ahmet", "ahmet@test.com", 25)
user.log("Kullanici olusturuldu")

# Serialization
json_str = user.to_json()
print(f"JSON: {json_str}")

user2 = User.from_json(json_str)
print(f"From JSON: {user2.name}, {user2.email}")

# Validation
user.update_email("invalid-email")
errors = user.validate()
print(f"Validation hatalari: {errors}")

# Gecerli kullanici
user.update_email("ahmet@valid.com")
errors = user.validate()
print(f"Validation hatalari: {errors}")
```

**Beklenen çıktı:**
```
[HH:MM:SS] User: Kullanici olusturuldu
JSON: {"name": "Ahmet", "email": "ahmet@test.com", "age": 25}
From JSON: Ahmet, ahmet@test.com
[HH:MM:SS] User: Email guncelleniyor: ahmet@test.com -> invalid-email
Validation hatalari: ['email: validation failed']
[HH:MM:SS] User: Email guncelleniyor: invalid-email -> ahmet@valid.com
Validation hatalari: []
```

**İpucu:** `to_json()` için `json.dumps(self.__dict__)` kullan. `from_json()` için `cls(**json.loads(json_str))`.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: Immutable Stack ve Queue

**Görev:** `@dataclass(frozen=True)` kullanarak immutable Stack ve Queue veri yapıları oluştur. Her operasyon yeni bir nesne dönsün.

**Başlangıç kodu:**
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutableStack:
    _items: tuple = ()

    def push(self, item) -> "ImmutableStack":
        """Yeni eleman eklenmiş yeni stack dondur."""
        # TODO: Mevcut tuple'a eleman ekle, yeni ImmutableStack olustur
        pass

    def pop(self) -> tuple:  # (item, new_stack)
        """Ust elemani cikar, (eleman, yeni_stack) dondur."""
        # TODO: Son elemani cikar, kalan elemanlarla yeni stack olustur
        pass

    def peek(self):
        """Ust elemani dondur (cikarma)."""
        # TODO
        pass

    @property
    def size(self) -> int:
        return len(self._items)

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __str__(self) -> str:
        return f"Stack({list(reversed(self._items))})"

# Test
s = ImmutableStack()
s1 = s.push(10)
s2 = s1.push(20)
s3 = s2.push(30)
print(f"s3: {s3}")
print(f"s3 peek: {s3.peek()}")

item, s4 = s3.pop()
print(f"Pop: {item}, kalan: {s4}")

# Orijinal stack degismedi!
print(f"s3 hala: {s3}")
print(f"s (bos): {s}")
```

**Beklenen çıktı:**
```
s3: Stack([30, 20, 10])
s3 peek: 30
Pop: 30, kalan: Stack([20, 10])
s3 hala: Stack([30, 20, 10])
s (bos): Stack([])
```

**İpucu:** `frozen=True` olduğu için `self._items` değiştirilemez. Her operasyonda yeni `ImmutableStack(_items=...)` oluştur.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Abstract Factory ile Veritabanı Bağlantısı

**Görev:** Abstract Factory pattern kullanarak farklı veritabanı bağlantı nesneleri oluşturan bir sistem yaz.

**Başlangıç kodu:**
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

class DatabaseConnection(ABC):
    @abstractmethod
    def connect(self) -> str: ...

    @abstractmethod
    def execute(self, query: str) -> str: ...

    @abstractmethod
    def close(self) -> str: ...

class PostgresConnection(DatabaseConnection):
    def __init__(self, host: str, port: int, db: str):
        self.host = host
        self.port = port
        self.db = db

    def connect(self) -> str:
        return f"PostgreSQL baglantisi: {self.host}:{self.port}/{self.db}"

    def execute(self, query: str) -> str:
        return f"PostgreSQL sorgusu: {query}"

    def close(self) -> str:
        return "PostgreSQL baglantisi kapatildi"

# TODO: SQLiteConnection ve MongoConnection siniflarini yaz

class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self, **kwargs) -> DatabaseConnection: ...

# TODO: PostgresFactory, SQLiteFactory, MongoFactory siniflarini yaz

def get_factory(db_type: str) -> DatabaseFactory:
    """Veritabani tipine gore uygun factory dondur."""
    # TODO: db_type'a gore factory sec
    pass

# Test
for db_type in ["postgres", "sqlite", "mongo"]:
    factory = get_factory(db_type)
    conn = factory.create_connection(
        host="localhost", port=5432, db="myapp"
    )
    print(conn.connect())
    print(conn.execute("SELECT * FROM users"))
    print(conn.close())
    print()
```

**Beklenen çıktı:**
```
PostgreSQL baglantisi: localhost:5432/myapp
PostgreSQL sorgusu: SELECT * FROM users
PostgreSQL baglantisi kapatildi

SQLite baglantisi: myapp.db
SQLite sorgusu: SELECT * FROM users
SQLite baglantisi kapatildi

MongoDB baglantisi: mongodb://localhost:27017/myapp
MongoDB sorgusu: db.users.find({})
MongoDB baglantisi kapatildi
```

**İpucu:** Her veritabanı tipi için Connection ve Factory sınıfı çifti oluştur. `get_factory()` basit bir dictionary mapping kullanabilir.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 9: Deep Copy ve Shallow Copy Görselleştirici

**Görev:** Nested veri yapılarında shallow copy vs deep copy farkını görselleştiren bir program yaz.

**Başlangıç kodu:**
```python
import copy

def visualize_copies(original: dict) -> None:
    """
    Original, shallow copy ve deep copy'nin bellek iliskisini goster.
    id() ile ayni objeye mi isaret ettiklerini kontrol et.
    """
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)

    print("=== Bellek Analizi ===\n")

    def compare_ids(path: str, orig_val, shallow_val, deep_val):
        """Uc kopyanin id'lerini karsilastir."""
        same_shallow = "AYNI" if id(orig_val) == id(shallow_val) else "FARKLI"
        same_deep = "AYNI" if id(orig_val) == id(deep_val) else "FARKLI"
        print(f"{path:30s} | Shallow: {same_shallow:7s} | Deep: {same_deep:7s}")

    # TODO:
    # 1. Root objelerin id'lerini karsilastir
    # 2. Her ic ice objenin id'lerini recursive olarak karsilastir
    # 3. Immutable degerler (str, int) icin id'lerin ayni oldugunu goster
    # 4. Mutable degerler (list, dict) icin farkli oldugunu goster

    compare_ids("root", original, shallow, deep)
    for key in original:
        val = original[key]
        compare_ids(f"  [{key}]", val, shallow[key], deep[key])
        if isinstance(val, (list, dict)):
            if isinstance(val, list):
                for i, item in enumerate(val):
                    compare_ids(f"    [{key}][{i}]", item, shallow[key][i], deep[key][i])

# Test
data = {
    "name": "Ahmet",       # str (immutable)
    "age": 25,             # int (immutable)
    "scores": [85, 90],    # list (mutable)
    "address": {           # dict (mutable)
        "city": "Istanbul",
        "district": "Kadikoy",
    },
    "hobbies": ["coding", "reading"],  # list (mutable)
}

visualize_copies(data)

# Mutation testi
print("\n=== Mutation Testi ===")
original = {"items": [1, 2, 3], "nested": {"x": 10}}
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow["items"].append(4)
print(f"Shallow'a ekleme sonrasi original: {original['items']}")  # [1,2,3,4] !
print(f"Deep copy etkilendi mi: {deep['items']}")  # [1,2,3]
```

**Beklenen çıktı:**
```
=== Bellek Analizi ===

root                           | Shallow: FARKLI | Deep: FARKLI
  [name]                       | Shallow: AYNI   | Deep: AYNI
  [age]                        | Shallow: AYNI   | Deep: AYNI
  [scores]                     | Shallow: AYNI   | Deep: FARKLI
    [scores][0]                | Shallow: AYNI   | Deep: AYNI
    [scores][1]                | Shallow: AYNI   | Deep: AYNI
  [address]                    | Shallow: AYNI   | Deep: FARKLI
  [hobbies]                    | Shallow: AYNI   | Deep: FARKLI

=== Mutation Testi ===
Shallow'a ekleme sonrasi original: [1, 2, 3, 4]
Deep copy etkilendi mi: [1, 2, 3]
```

**İpucu:** `id()` fonksiyonu objenin bellek adresini döner. Immutable objeler (str, int) Python tarafından paylaşılır (interning).

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 10: Event Sistemi ile Observer Pattern

**Görev:** Type hints ile tam donanımlı bir Event/Observer sistemi yaz. Birden fazla listener desteklesin, event data taşısın.

**Başlangıç kodu:**
```python
from typing import Callable, Any
from dataclasses import dataclass, field

@dataclass
class Event:
    name: str
    data: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__("time").time())

class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event_name: str, callback: Callable) -> None:
        """Event listener kaydet."""
        # TODO
        pass

    def off(self, event_name: str, callback: Callable) -> None:
        """Event listener'i kaldir."""
        # TODO
        pass

    def emit(self, event_name: str, **data) -> int:
        """Event'i tetikle, cagrilan listener sayisini dondur."""
        # TODO: Kayitli tum listener'lari cagir
        pass

    def once(self, event_name: str, callback: Callable) -> None:
        """Sadece bir kez calisacak listener kaydet."""
        # TODO: Calistiktan sonra kendini kaldiracak wrapper olustur
        pass

# Test
emitter = EventEmitter()

# Listener'lari kaydet
def on_user_created(event: Event):
    print(f"  Kullanici olusturuldu: {event.data.get('name')}")

def on_user_created_log(event: Event):
    print(f"  [LOG] Yeni kullanici: {event.data}")

def on_login_once(event: Event):
    print(f"  Ilk giris bildirimi: {event.data.get('name')}")

emitter.on("user:created", on_user_created)
emitter.on("user:created", on_user_created_log)
emitter.once("user:login", on_login_once)

print("Event: user:created")
count = emitter.emit("user:created", name="Ahmet", email="ahmet@test.com")
print(f"  {count} listener cagrildi\n")

print("Event: user:login (1. kez)")
emitter.emit("user:login", name="Ahmet")

print("\nEvent: user:login (2. kez - once listener calismamali)")
count = emitter.emit("user:login", name="Ahmet")
print(f"  {count} listener cagrildi")
```

**Beklenen çıktı:**
```
Event: user:created
  Kullanici olusturuldu: Ahmet
  [LOG] Yeni kullanici: {'name': 'Ahmet', 'email': 'ahmet@test.com'}
  2 listener cagrildi

Event: user:login (1. kez)
  Ilk giris bildirimi: Ahmet

Event: user:login (2. kez - once listener calismamali)
  0 listener cagrildi
```

**İpucu:** `once()` için inner function tanımla, bu function çalıştıktan sonra `self.off()` ile kendini kaldırsın.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Custom Collection ile __getitem__ ve Slicing

**Görev:** `__getitem__`, `__setitem__` ve slicing destekleyen custom bir collection sınıfı yaz.

**Başlangıç kodu:**
```python
class SortedList:
    """Her zaman sirali kalan bir liste."""
    def __init__(self):
        self._items: list = []

    def add(self, item):
        """Elemani dogru pozisyona ekle (sira bozulmasin)."""
        # TODO: bisect modulu ile dogru pozisyonu bul ve ekle
        import bisect
        bisect.insort(self._items, item)

    def __getitem__(self, index):
        """Index veya slice ile erisim."""
        # TODO: int ise tek eleman, slice ise yeni SortedList dondur
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        # TODO: Binary search ile hizli arama
        import bisect
        i = bisect.bisect_left(self._items, item)
        return i < len(self._items) and self._items[i] == item

    def __str__(self):
        return f"SortedList({self._items})"

# Test
sl = SortedList()
for num in [5, 2, 8, 1, 9, 3, 7, 4, 6]:
    sl.add(num)

print(sl)                    # SortedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
print(f"sl[0] = {sl[0]}")   # 1
print(f"sl[-1] = {sl[-1]}") # 9
print(f"sl[2:5] = {sl[2:5]}")  # [3, 4, 5]
print(f"5 in sl: {5 in sl}")   # True
print(f"10 in sl: {10 in sl}") # False
print(f"len: {len(sl)}")       # 9
```

**Beklenen çıktı:**
```
SortedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
sl[0] = 1
sl[-1] = 9
sl[2:5] = [3, 4, 5]
5 in sl: True
10 in sl: False
len: 9
```

**İpucu:** `bisect.insort()` sıralı listeye eleman ekler. `bisect.bisect_left()` ile O(log n) arama yapılır.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 12: Money Class ile Operatör Overloading

**Görev:** Para hesaplamları için `Decimal` tabanlı bir `Money` sınıfı yaz. Aritmetik operatörleri ve karşılaştırmaları desteklesin.

**Başlangıç kodu:**
```python
from decimal import Decimal
from functools import total_ordering

@total_ordering
class Money:
    def __init__(self, amount: str | int | float, currency: str = "TRY"):
        self.amount = Decimal(str(amount))
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        # TODO: Ayni para birimi kontrolu, toplama
        pass

    def __sub__(self, other: "Money") -> "Money":
        pass

    def __mul__(self, multiplier: int | float) -> "Money":
        # TODO: Sayi ile carpma (Money * 3)
        pass

    def __eq__(self, other: "Money") -> bool:
        pass

    def __lt__(self, other: "Money") -> bool:
        pass

    def __str__(self) -> str:
        return f"{self.amount:,.2f} {self.currency}"

    def __repr__(self) -> str:
        return f"Money('{self.amount}', '{self.currency}')"

# Test
price = Money("15000.00")
tax = Money("2700.00")
total = price + tax
print(f"Fiyat: {price}")
print(f"KDV:   {tax}")
print(f"Toplam: {total}")

discount = Money("1500")
final = total - discount
print(f"Indirimli: {final}")

unit_price = Money("49.99")
bulk = unit_price * 100
print(f"Toptan: {bulk}")

print(f"Karsilastirma: {price} > {tax} = {price > tax}")

try:
    usd = Money(100, "USD")
    result = price + usd  # Hata!
except ValueError as e:
    print(f"Hata: {e}")
```

**Beklenen çıktı:**
```
Fiyat: 15,000.00 TRY
KDV:   2,700.00 TRY
Toplam: 17,700.00 TRY
Indirimli: 16,200.00 TRY
Toptan: 4,999.00 TRY
Karsilastirma: 15,000.00 TRY > 2,700.00 TRY = True
Hata: Cannot add TRY and USD
```

**İpucu:** `@total_ordering` sadece `__eq__` ve `__lt__` tanımlanınca diğer karşılaştırmaları otomatik oluşturur. `Decimal` ile float hassasiyet sorunlarından kaçın.

**Zorluk:** Orta
:::

:::must-note
- **Immutable:** int, float, str, bool, tuple, frozenset, bytes / **Mutable:** list, dict, set, bytearray
- Mutable default argument tuzağı: `def f(x=[])` yapma, `def f(x=None)` yap
- `float` ile para hesabı yapma, `Decimal` kullan
- Type hints 2026'da neredeyse zorunlu: `def fonk(x: int) -> str:` formatı
- `mypy --strict` ile statik tip kontrolü yap, CI/CD'ye ekle
- f-string: `f"{degisken = }"` debug için, `f"{fiyat:,.2f}"` formatlama için
- Comprehension: okunabilirliği koruyacak kadar basit tut, karmaşıksa döngü yaz
- `self` her instance method'un ilk parametresi olmalı (convention, keyword değil)
- `__repr__` her zaman tanımla, `eval()` ile geri oluşturulabilir formatta olsun
- `@dataclass` boilerplate'i yok eder: `__init__`, `__repr__`, `__eq__` otomatik gelir
- `@dataclass(frozen=True)` = immutable + hashable
- `@property` ile getter/setter: encapsulation sağla, doğrudan attribute erişimi gibi kullan
- Abstract class: `ABC` + `@abstractmethod` ile interface tanımla
- Composition > Inheritance: "has-a" ilişkisi genellikle "is-a"dan daha iyidir
- MRO (C3 Linearization): `ClassName.__mro__` ile kalıtım sırasını kontrol et
- `__eq__` override edersen `__hash__` None olur, hashable istiyorsan `__hash__`'i de tanımla
:::

:::senior-learns
Bir Senior Developer, Python veri tipleri ve OOP konusunu öğrenirken şu yaklaşımı benimser:

1. **CPython kaynak kodunu inceler** - `int`, `str`, `list` gibi tiplerin C implementasyonunu okur. Neden `tuple`'ın `list`'ten daha hızlı olduğunu memory layout seviyesinde anlar. `Objects/listobject.c` ve `Objects/tupleobject.c` dosyalarını karşılaştırır.
2. **`dis` modülü ile bytecode analiz eder** - `dis.dis(fonksiyon)` ile Python kodunun nasıl bytecode'a derlendiğini inceler. Bir list comprehension'ın normal for döngüsünden neden daha hızlı olduğunu bytecode seviyesinde görür.
3. **Protocol ve Structural Subtyping kullanır** - ABC yerine `typing.Protocol` ile duck typing'i type-safe hale getirir. Bu, Go'nun interface mantığına çok benzer ve daha esnek bir OOP modeli sunar.
4. **`__slots__` ile bellek optimize eder** - `__dict__` yerine `__slots__` kullanarak her instance başına %30-40 bellek tasarrufu sağlar. Binlerce instance oluşturulan veri yoğun uygulamalarda kritik fark yaratır.
5. **Descriptor Protocol'ü anlar** - `@property`'nin aslında bir descriptor olduğunu bilir. `__get__`, `__set__`, `__delete__` metodlarıyla kendi descriptor'larını yazar. ORM framework'lerinin field tanımlarının nasıl çalıştığını kavrar.
6. **Pydantic v2 ile runtime validation yapar** - Dataclass'lar compile-time check sağlarken Pydantic hem compile-time hem runtime validation sunar. API input validation, config management ve data parsing için Pydantic `BaseModel` kullanır.

**Karar Verme Sureci — Dataclass vs Pydantic vs NamedTuple vs TypedDict:**
- **NamedTuple**: Immutable, hafif, sadece veri tasiyan yapilar icin. Trade-off: method ekleyemezsin, inheritance sinirli. Kullanim: fonksiyon return degerleri, config sabitleri.
- **dataclass**: Mutable veya immutable, method eklenebilir, default degerler. Trade-off: runtime validation yok, sadece type checker (mypy) ile statik kontrol. Kullanim: domain modelleri, internal veri yapilari.
- **Pydantic BaseModel**: Runtime validation + serialization + deserialization. Trade-off: ~10-50x dataclass'tan yavas (Pydantic v2 ile fark cok azaldi ama hala var), dependency ekliyor. Kullanim: API boundary, disaridan gelen veri, config dosyalari.
- **TypedDict**: Sadece type hint, runtime etkisi sifir. Trade-off: validation yok, sadece IDE/mypy icin. Kullanim: JSON response tipleri, legacy dict-based kodlari tiplemek.
- **Senior karar agaci**: "Veri disaridan mi geliyor? Pydantic. Internal mi? dataclass. Immutable mi? NamedTuple. Legacy dict mi? TypedDict."

**Anti-pattern Farkindaligi:**
- **God Class**: 500+ satirlik tek class, 10+ method, birden fazla sorumluluk. Production'da gordugum en kotu ornek: bir `UserManager` class'i hem auth, hem email, hem billing, hem logging yapiyordu. Bir hatayi fix etmek icin 3 gun harcandik cunku her sey birbiriyle bagli.
- **Inheritance zinciri**: 4+ seviye derin kalitim. `Animal > Mammal > Pet > Dog > GoldenRetriever` — bunu debug etmek kabusa doner. MRO (Method Resolution Order) hatalari cok zor bulunur. Cozum: Composition + Protocol. Python'un `super()` sirasi C3 Linearization ile belirlenir ve 4+ seviyede bunu kafadan takip edemezsin.
- **Premature `__slots__`**: 100 instance'in varken `__slots__` eklemek over-engineering. 100K+ instance veya memory-critical durumlarda dusun.

**Gercek Dunya Deneyimi:** Production'da bir e-ticaret API'sinde `dict` ile basladik. 6 ay sonra 200+ endpoint, hic bir yerde type safety yok, runtime'da `KeyError` patlak veriyor. Pydantic'e gecis 2 hafta surdu ama sonrasinda bug orani %40 dustu. Ders: Type safety'yi projenin basindan koy, sonradan eklemek cok pahali.

**Profesyonel Mindset:** "Type hints sadece hata yakalamak için değil, kodun canlı dokümantasyonudur. Bir fonksiyonun type signature'ı, o fonksiyonun ne yaptığını anlatır. `def process(data: list[dict[str, Any]]) -> Result | None` yazan bir fonksiyon, docstring okumadan bile ne beklediğini ve ne döndüğünü söyler. Tip sistemi ile çalışmak yavaşlatmaz, uzun vadede hızlandırır."
:::

:::english
**Teknik Ingilizce - Bu Dersteki Terimler:**

1. **Mutable** (myoo-tuh-buhl) → Değiştirilebilir
   *"Lists are mutable, meaning you can add, remove, or change elements after creation."*

2. **Immutable** (ih-myoo-tuh-buhl) → Değiştirilemez
   *"Tuples are immutable — once created, their elements cannot be modified."*

3. **Inheritance** (in-her-uh-tuhns) → Kalıtım
   *"Python supports multiple inheritance, but favor composition over inheritance."*

4. **Polymorphism** (pol-ee-mor-fiz-uhm) → Çok biçimlilik
   *"Polymorphism allows different classes to implement the same interface with different behavior."*

5. **Type Annotation** (tahyp an-oh-tey-shuhn) → Tip belirteci
   *"Type annotations help catch bugs early and improve IDE autocompletion."*

**Okuma Egzersizi:** Python resmi dokümantasyonundan "Data Model" bölümünü oku: https://docs.python.org/3/reference/datamodel.html

**Yazma Pratiği:** Aşağıdaki commit mesajını Ingilizce yaz: "Kullanıcı sınıfına type hints ve dataclass desteği eklendi"
→ Örnek: `refactor: add type hints and convert User class to dataclass`
:::

:::external-resource
- 📺 **Corey Schafer:** "Python OOP Tutorials" (6 video, YouTube, ucretsiz)
- 📖 **Real Python:** "Python Data Classes Guide" (detaylı rehber, ucretsiz)
- 📖 **mypy docs:** "Getting Started with mypy" (resmi dokumantasyon, ucretsiz)
- 📺 **ArjanCodes:** "Python Dataclasses Are AMAZING" (YouTube, ucretsiz)
- 📖 **Python Docs:** "Built-in Types" (resmi referans, ucretsiz)
:::
