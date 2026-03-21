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
