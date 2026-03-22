---
id: mod-03-js/lesson-01
title: "JavaScript Temelleri: Scope, Closures ve Event Loop"
estimated_minutes: 55
tags: ["javascript", "scope", "closures", "event-loop", "this", "prototypes", "dom"]
prerequisites: ["mod-01-internet/lesson-01"]
order: 1
---

# JavaScript Temelleri: Scope, Closures ve Event Loop

:::realworld
JavaScript, 2026 itibarıyla frontend geliştirmenin %95'ini oluşturuyor. Brendan Eich tarafından 1995'te sadece 10 günde tasarlanan bu dil, bugün tarayıcılardan sunuculara, mobil uygulamalardan IoT cihazlarına kadar her yerde çalışıyor. Bu derste JS'in en kritik temel kavramlarını deha seviyesinde öğreneceksin. Scope, closures, event loop, this keyword ve prototypal inheritance gibi konular mülakatlarda en sık sorulan ve en çok elek yapan konulardır. Bunları gerçekten anlayan developer, sıradan developer'dan ayrışır.
:::

## Neden Bu Konuyu Öğreniyorsun?

JavaScript'in syntax'ını öğrenmek kolay, ama dilini gerçekten anlamak bambaşka bir seviye. Framework'ler (React, Vue, Angular) hep değişir ama JavaScript'in temel mekanizmaları aynı kalır. Bu temelleri anlamadan:

- Closure bug'larını debug edemezsin
- Asenkron kodda neden beklenmeyen davranışlar oluştuğunu anlayamazsın
- `this` keyword'ünün neden bazen `undefined` döndüğünü çözemezsin
- Senior mülakatlarda elenir ve junior seviyesinde kalırsın

:::deha-tip
Deha seviyesi geliştiriciler, bir JavaScript bug'ı gördüklerinde hemen Stack Overflow'a koşmaz. Önce sorunun hangi temel mekanizmadan kaynaklandığını düşünürler: "Bu bir scope sorunu mu? Closure mı? Event loop sıralaması mı? `this` binding mi?" Bu derste öğreneceğin kavramlar, her JS problemini doğru katmanda analiz etmeni sağlayacak.
:::

## JavaScript Nedir?

JavaScript, dinamik tipli, prototip tabanlı, multi-paradigm (fonksiyonel + nesne yönelimli) bir programlama dilidir. Tarayıcıda çalışan tek programlama dili olması onu web'in vazgeçilmezi yapar.

:::concept[JavaScript Engine (İng: JavaScript Engine)]
JavaScript Engine, JS kodunu alıp makine koduna çeviren ve çalıştıran yazılımdır. Her tarayıcının kendi engine'i vardır.

**Türkçe karşılığı:** JavaScript Motoru
**Ne işe yarar:** JS kodunu yorumlar, optimize eder ve çalıştırır
**Gerçek hayat benzetmesi:** Bir tercüman gibi - senin yazdığın kodu bilgisayarın anlayacağı dile çevirir

**Önemli Engine'ler:**
- V8 (Chrome, Node.js, Deno)
- SpiderMonkey (Firefox)
- JavaScriptCore (Safari)
:::

## Scope: Değişkenlerin Erişim Alanı

Scope, bir değişkenin kodun hangi bölümlerinden erişilebilir olduğunu belirler. JavaScript'te 3 tür scope vardır.

### Global Scope

En dış katmanda tanımlanan değişkenler global scope'tadır. Her yerden erişilebilir.

:::code[javascript]{title="Global Scope"}
var globalVar = "Ben global'im";
let globalLet = "Ben de global'im";

function herYerdenErisebilirsin() {
  console.log(globalVar); // "Ben global'im"
  console.log(globalLet); // "Ben de global'im"
}

// Tarayıcıda var ile tanımlanan global değişkenler window objesine eklenir
console.log(window.globalVar); // "Ben global'im"
console.log(window.globalLet); // undefined (let window'a eklenmez!)
:::

### Function Scope

`var` ile tanımlanan değişkenler function scope'a sahiptir. Fonksiyonun her yerinden erişilebilir ama dışından erişilemez.

:::code[javascript]{title="Function Scope - var"}
function ornekFonksiyon() {
  var fonksiyonDegiskeni = "Sadece burada yaşarım";

  if (true) {
    var ifIcinde = "Ben de fonksiyon scope'tayım!";
    // var, block scope oluşturmaz - dikkat!
  }

  console.log(ifIcinde); // "Ben de fonksiyon scope'tayım!" (Erişilebilir!)
}

console.log(fonksiyonDegiskeni); // ReferenceError: fonksiyonDegiskeni is not defined
:::

### Block Scope (let ve const)

`let` ve `const` ile tanımlanan değişkenler block scope'a sahiptir. `{}` süslü parantezlerle sınırlıdır.

:::code[javascript]{title="Block Scope - let ve const"}
function blockScopeOrnegi() {
  if (true) {
    let blockLet = "Sadece bu blokta yaşarım";
    const blockConst = "Ben de sadece burada";
    var blockVar = "Ama ben fonksiyon scope'tayım";
  }

  console.log(blockVar);   // "Ama ben fonksiyon scope'tayım" (Erişilebilir)
  console.log(blockLet);   // ReferenceError!
  console.log(blockConst); // ReferenceError!
}

// for döngüsü ile klasik hata
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Çıktı: 3, 3, 3 (Hepsi 3! Çünkü var function scope)

for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log(j), 100);
}
// Çıktı: 0, 1, 2 (Doğru! Çünkü let block scope)
:::

:::comparison
| Özellik | var | let | const |
|---------|-----|-----|-------|
| Scope | Function scope | Block scope | Block scope |
| Hoisting | Evet (undefined) | Evet (TDZ) | Evet (TDZ) |
| Yeniden tanımlama | Evet | Hayır | Hayır |
| Yeniden atama | Evet | Evet | Hayır |
| window'a eklenir mi | Evet (global) | Hayır | Hayır |
| **2026 tavsiyesi** | KULLANMA | Varsayılan seçim | Değişmeyecek değerler |

**Kural:** Önce `const` kullan. Değerin değişeceğinden eminsen `let` kullan. `var` asla kullanma.
:::

:::beginner-mistake
Yaygın hata: `const` ile tanımlanan bir object veya array'in immutable (değiştirilemez) olduğunu sanmak. `const` sadece referansı kilitler, içeriği değil!

```javascript
const user = { name: "Taha" };
user.name = "Ali";    // SORUN YOK! Object içeriği değişebilir
user = { name: "Veli" }; // TypeError! Referans değiştirilemez

const arr = [1, 2, 3];
arr.push(4);          // SORUN YOK! Array içeriği değişebilir
arr = [5, 6];         // TypeError! Referans değiştirilemez
```
:::

## Hoisting: Kodun Yukarı Taşınması

:::concept[Hoisting (İng: Hoisting)]
Hoisting, JavaScript engine'in derleme aşamasında değişken ve fonksiyon tanımlamalarını scope'un en üstüne taşıması mekanizmasıdır.

**Türkçe karşılığı:** Yukarı Taşıma / Kaldırma
**Ne işe yarar:** Kodun çalışma sırasını anlamak için kritik
**Gerçek hayat benzetmesi:** Bir sınıfta yoklama almak gibi - öğretmen önce tüm isimleri (tanımlamaları) kaydeder, sonra dersi (çalışmayı) başlatır
:::

### Variable Hoisting

:::code[javascript]{title="var Hoisting"}
console.log(x); // undefined (tanım yukarı taşınır, değer değil)
var x = 5;
console.log(x); // 5

// JavaScript engine bunu şöyle görür:
var x;            // Tanım yukarı taşındı
console.log(x);  // undefined
x = 5;           // Atama yerinde kaldı
console.log(x);  // 5
:::

### Temporal Dead Zone (TDZ)

`let` ve `const` da hoist edilir ama Temporal Dead Zone (Geçici Ölü Bölge) nedeniyle, tanımlanmadan önce erişilemez.

:::code[javascript]{title="TDZ - Temporal Dead Zone"}
// TDZ burada başlıyor (scope'un başlangıcı)
console.log(a); // ReferenceError: Cannot access 'a' before initialization
let a = 10;     // TDZ burada bitiyor

// typeof bile TDZ'de hata verir
console.log(typeof undeclaredVar); // "undefined" (tanımsız değişken sorun değil)
console.log(typeof b);            // ReferenceError! (TDZ'de olan değişken)
let b = 20;
:::

### Function Hoisting

:::code[javascript]{title="Function Hoisting"}
// Function declaration: Tamamen hoist edilir (hem tanım hem gövde)
selamVer(); // "Merhaba!" - Tanımdan önce çağırılabilir!

function selamVer() {
  console.log("Merhaba!");
}

// Function expression: Sadece değişken hoist edilir
sayHello(); // TypeError: sayHello is not a function

var sayHello = function() {
  console.log("Hello!");
};

// Arrow function: Function expression gibi davranır
greet(); // TypeError: greet is not a function

var greet = () => console.log("Hi!");
:::

:::beginner-mistake
Yaygın hata: `let` ve `const` hoist edilmez sanmak. Hoist edilir ama TDZ yüzünden erişilemez. Fark önemli: eğer hoist edilmeseydi, dış scope'taki aynı isimli değişkene erişebilirdin.

```javascript
let x = "dış";
{
  console.log(x); // ReferenceError! (TDZ)
  // Eğer hoist edilmeseydi "dış" yazardı
  let x = "iç";
}
```
:::

## Closures: JavaScript'in En Güçlü Silahı

:::concept[Closure (İng: Closure)]
Closure, bir fonksiyonun kendi scope'u dışındaki değişkenlere erişebilme ve onları hatırlayabilme yeteneğidir. Fonksiyon, tanımlandığı scope'un referansını "kapatır" (close over).

**Türkçe karşılığı:** Kapanış / Kapama
**Ne işe yarar:** Data privacy, state management, factory pattern, memoization
**Gerçek hayat benzetmesi:** Bir sırt çantası gibi - fonksiyon nereye giderse gitsin, tanımlandığı yerdeki değişkenleri sırt çantasında taşır
:::

:::code[javascript]{title="Closure Temeli"}
function disKapsam() {
  let sayac = 0; // Bu değişken closure sayesinde hayatta kalır

  function artir() {
    sayac++; // Dış scope'taki değişkene erişiyor
    return sayac;
  }

  return artir;
}

const sayacFn = disKapsam(); // disKapsam çalıştı ve bitti ama...
console.log(sayacFn()); // 1 - sayac hala yaşıyor!
console.log(sayacFn()); // 2 - ve her çağrıda güncelleniyor
console.log(sayacFn()); // 3

const baskaSayac = disKapsam(); // Yeni bir closure, yeni bir sayac
console.log(baskaSayac()); // 1 - bağımsız sayac
:::

### Closure'ın Pratik Kullanım Alanları

:::code[javascript]{title="1. Data Privacy (Module Pattern)"}
function createBankAccount(initialBalance) {
  let balance = initialBalance; // Private değişken - dışarıdan erişilemez

  return {
    deposit(amount) {
      balance += amount;
      return `Yatırıldı: ${amount}. Bakiye: ${balance}`;
    },
    withdraw(amount) {
      if (amount > balance) return "Yetersiz bakiye!";
      balance -= amount;
      return `Çekildi: ${amount}. Bakiye: ${balance}`;
    },
    getBalance() {
      return balance;
    }
  };
}

const hesap = createBankAccount(1000);
console.log(hesap.deposit(500));    // "Yatırıldı: 500. Bakiye: 1500"
console.log(hesap.withdraw(200));   // "Çekildi: 200. Bakiye: 1300"
console.log(hesap.balance);        // undefined! (Private - erişilemez)
:::

:::code[javascript]{title="2. Memoization (Sonuç Önbellekleme)"}
function memoize(fn) {
  const cache = {}; // Closure ile korunan cache

  return function(...args) {
    const key = JSON.stringify(args);
    if (cache[key]) {
      console.log("Cache'ten geldi!");
      return cache[key];
    }
    const result = fn(...args);
    cache[key] = result;
    return result;
  };
}

const agirHesaplama = memoize((n) => {
  console.log("Hesaplanıyor...");
  return n * n;
});

agirHesaplama(5); // "Hesaplanıyor..." → 25
agirHesaplama(5); // "Cache'ten geldi!" → 25 (tekrar hesaplamadı)
:::

## "this" Keyword: Bağlam Kralı

`this` keyword'ü, fonksiyonun nasıl çağrıldığına bağlı olarak farklı değerlere sahip olur. Bu, JavaScript'in en kafa karıştıran konularından biridir.

:::code[javascript]{title="this - Farklı Bağlamlar"}
// 1. Global context
console.log(this); // window (tarayıcıda), global (Node.js'te)

// 2. Object method
const user = {
  name: "Taha",
  greet() {
    console.log(`Merhaba, ${this.name}`); // this = user objesi
  }
};
user.greet(); // "Merhaba, Taha"

// 3. Sorun: Method'u ayrı çağırmak
const greetFn = user.greet;
greetFn(); // "Merhaba, undefined" (this = window, strict mode'da undefined)

// 4. Arrow function: Kendi this'i yok, dış scope'un this'ini kullanır
const team = {
  name: "Frontend Takımı",
  members: ["Ali", "Ayse"],
  showMembers() {
    // Arrow function: this = team objesi (lexical this)
    this.members.forEach((member) => {
      console.log(`${member} - ${this.name}`);
    });
  }
};
team.showMembers();
// "Ali - Frontend Takımı"
// "Ayse - Frontend Takımı"

// 5. Normal function kullanılsaydı:
const team2 = {
  name: "Backend Takımı",
  members: ["Veli", "Fatma"],
  showMembers() {
    this.members.forEach(function(member) {
      console.log(`${member} - ${this.name}`); // this = window/undefined!
    });
  }
};
team2.showMembers();
// "Veli - undefined" (HATA!)
:::

### bind, call, apply

:::code[javascript]{title="this'i Manuel Bağlama"}
function introduce(greeting, punctuation) {
  console.log(`${greeting}, ben ${this.name}${punctuation}`);
}

const person = { name: "Taha" };

// call: Argümanları tek tek verir
introduce.call(person, "Selam", "!");    // "Selam, ben Taha!"

// apply: Argümanları array olarak verir
introduce.apply(person, ["Merhaba", "."]); // "Merhaba, ben Taha."

// bind: Yeni fonksiyon döndürür (hemen çalıştırmaz)
const boundFn = introduce.bind(person, "Hey");
boundFn("?"); // "Hey, ben Taha?"
:::

:::comparison
| Durum | this Değeri |
|-------|-------------|
| Global (non-strict) | window / global |
| Global (strict mode) | undefined |
| Object method | Object'in kendisi |
| Arrow function | Lexical (dış scope'un this'i) |
| call / apply | İlk argüman |
| bind | İlk argüman (kalıcı) |
| new keyword | Yeni oluşturulan obje |
| Event handler (DOM) | Event'i alan element |

**Kural:** Arrow function ile `this` sorunu çözülür. Method tanımlarken normal function, callback'lerde arrow function kullan.
:::

## Prototypal Inheritance vs Class Syntax

JavaScript'te "gerçek" class yoktur. ES6 class syntax'ı, prototypal inheritance üzerinde bir syntax sugar'dır (güzel görünüm).

:::code[javascript]{title="Prototypal Inheritance"}
// Prototype chain
function Animal(name) {
  this.name = name;
}

Animal.prototype.speak = function() {
  return `${this.name} ses çıkarıyor`;
};

function Dog(name, breed) {
  Animal.call(this, name); // Super constructor
  this.breed = breed;
}

Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.bark = function() {
  return `${this.name} havlıyor!`;
};

const buddy = new Dog("Buddy", "Golden");
console.log(buddy.speak()); // "Buddy ses çıkarıyor" (Animal'dan miras)
console.log(buddy.bark());  // "Buddy havlıyor!" (Dog'a ait)
:::

:::code[javascript]{title="ES6 Class Syntax (Aynı Şey, Daha Temiz)"}
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    return `${this.name} ses çıkarıyor`;
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name); // Animal constructor'ını çağır
    this.breed = breed;
  }

  bark() {
    return `${this.name} havlıyor!`;
  }
}

const buddy = new Dog("Buddy", "Golden");
console.log(buddy.speak()); // "Buddy ses çıkarıyor"
console.log(buddy.bark());  // "Buddy havlıyor!"

// Ama altta yatan mekanizma aynı:
console.log(typeof Dog);    // "function" (class değil!)
console.log(buddy.__proto__ === Dog.prototype); // true
:::

## Event Loop: JavaScript'in Kalp Atışı

:::concept[Event Loop (İng: Event Loop)]
Event Loop, JavaScript'in tek thread'li olmasına rağmen asenkron işlemleri yönetmesini sağlayan mekanizmadır.

**Türkçe karşılığı:** Olay Döngüsü
**Ne işe yarar:** Call stack boşaldığında, kuyruktan sıradaki görevi alıp çalıştırır
**Gerçek hayat benzetmesi:** Bir restoran garsonu gibi - tek garson var ama siparişleri sıraya koyup, mutfaktan hazır olanları masalara taşıyarak tüm müşterilere hizmet veriyor
:::

:::code[text]{title="Event Loop Bileşenleri"}
┌─────────────────────────────────┐
│          CALL STACK             │  ← Senkron kod burada çalışır
│  (Tek seferde 1 iş yapılır)    │
└──────────┬──────────────────────┘
           │ Boşaldığında kontrol et
           ▼
┌─────────────────────────────────┐
│      MICROTASK QUEUE            │  ← Öncelik bu kuyrukta!
│  (Promise.then, queueMicrotask, │     Tüm microtask'lar bitmeden
│   MutationObserver)             │     macrotask'a geçilmez
└──────────┬──────────────────────┘
           │ Microtask queue boşsa
           ▼
┌─────────────────────────────────┐
│      MACROTASK QUEUE            │  ← Sonra buraya bakılır
│  (setTimeout, setInterval,      │
│   DOM events, fetch callback)   │
└─────────────────────────────────┘

   Web APIs: setTimeout, fetch, DOM events gibi
   asenkron işlemleri tarayıcı arka planda yönetir,
   bitince ilgili kuyruğa koyar.
:::

### Microtasks vs Macrotasks

:::code[javascript]{title="Sıralama Bulmacası (Mülakat Klasiği!)"}
console.log("1: Senkron başla");

setTimeout(() => {
  console.log("2: setTimeout (macrotask)");
}, 0);

Promise.resolve().then(() => {
  console.log("3: Promise.then (microtask)");
});

queueMicrotask(() => {
  console.log("4: queueMicrotask (microtask)");
});

console.log("5: Senkron bitir");

// Çıktı sırası:
// 1: Senkron başla
// 5: Senkron bitir
// 3: Promise.then (microtask)
// 4: queueMicrotask (microtask)
// 2: setTimeout (macrotask)
:::

:::beginner-mistake
Yaygın hata: `setTimeout(fn, 0)` deyince "hemen çalışır" sanmak. Sıfır milisaniye bile olsa, macrotask queue'ya gider ve tüm senkron kod + tüm microtask'lar bittikten sonra çalışır. `Promise.then` her zaman `setTimeout(fn, 0)`'dan önce çalışır.
:::

:::code[javascript]{title="Daha Karmaşık Event Loop Senaryosu"}
console.log("Start");

setTimeout(() => {
  console.log("Timeout 1");
  Promise.resolve().then(() => console.log("Promise inside Timeout"));
}, 0);

Promise.resolve().then(() => {
  console.log("Promise 1");
  setTimeout(() => console.log("Timeout inside Promise"), 0);
});

Promise.resolve().then(() => console.log("Promise 2"));

console.log("End");

// Çıktı:
// Start
// End
// Promise 1
// Promise 2
// Timeout 1
// Promise inside Timeout
// Timeout inside Promise
:::

## DOM Manipulation Temelleri

:::concept[DOM (İng: Document Object Model)]
DOM, HTML belgesinin tarayıcı tarafından oluşturulan ağaç yapısındaki temsilidir. JavaScript ile bu ağacı okuyabilir ve değiştirebilirsin.

**Türkçe karşılığı:** Belge Nesne Modeli
**Ne işe yarar:** HTML elemanlarını JavaScript ile dinamik olarak oluşturma, değiştirme, silme
**Gerçek hayat benzetmesi:** HTML dosyası binanın mimari planı, DOM ise binanın kendisi. Planı değiştiremezsin ama binada tadilat yapabilirsin
:::

:::code[javascript]{title="DOM Seçiciler ve Manipülasyon"}
// Element seçme
const title = document.getElementById("main-title");
const buttons = document.querySelectorAll(".btn");
const firstBtn = document.querySelector(".btn");

// İçerik değiştirme
title.textContent = "Yeni Başlık";        // Sadece metin
title.innerHTML = "<em>Yeni Başlık</em>"; // HTML olarak

// Stil değiştirme
title.style.color = "blue";
title.classList.add("active");
title.classList.remove("hidden");
title.classList.toggle("dark-mode");

// Element oluşturma ve ekleme
const newDiv = document.createElement("div");
newDiv.textContent = "Dinamik element";
newDiv.classList.add("card");
document.body.appendChild(newDiv);

// Element silme
const eskiElement = document.querySelector(".old");
eskiElement.remove();
:::

:::tip
Modern framework'ler (React, Vue) DOM manipülasyonunu senin yerine yapar. Ama altta ne olduğunu bilmek, performans sorunlarını anlamak ve framework'süz çalışabilmek için DOM API'sini bilmelisin.
:::

## Event Handling ve Event Delegation

### Event Handling

:::code[javascript]{title="Event Listener'lar"}
const button = document.querySelector("#myBtn");

// Event listener ekleme
button.addEventListener("click", function(event) {
  console.log("Tıklandı!", event.target);
});

// Arrow function ile
button.addEventListener("click", (e) => {
  e.preventDefault(); // Varsayılan davranışı engelle
  console.log("Tıklandı!");
});

// Event listener kaldırma (named function gerekli)
function handleClick(e) {
  console.log("Tıklandı!");
}
button.addEventListener("click", handleClick);
button.removeEventListener("click", handleClick);
:::

### Event Bubbling ve Delegation

:::concept[Event Delegation (İng: Event Delegation)]
Event Delegation, her child elemente ayrı event listener eklemek yerine, parent elemente tek bir listener ekleyip event bubbling ile olayları yakalama tekniğidir.

**Türkçe karşılığı:** Olay Delegasyonu / Yetki Devri
**Ne işe yarar:** Performansı artırır, dinamik eklenen elementler için listener sorununu çözer
**Gerçek hayat benzetmesi:** Her çalışana ayrı telefon vermek yerine, departman telefonuna tek sekreter koymak - gelen çağrıyı doğru kişiye yönlendirir
:::

:::code[javascript]{title="Event Delegation Örneği"}
// KOTU: Her butona ayrı listener (1000 buton = 1000 listener)
document.querySelectorAll(".item-btn").forEach(btn => {
  btn.addEventListener("click", (e) => {
    console.log("Tıklandı:", e.target.textContent);
  });
});

// IYI: Parent'a tek listener (Event Delegation)
document.querySelector("#item-list").addEventListener("click", (e) => {
  // Tıklanan element .item-btn ise işle
  if (e.target.matches(".item-btn")) {
    console.log("Tıklandı:", e.target.textContent);
  }

  // closest() ile daha esnek kontrol
  const card = e.target.closest(".card");
  if (card) {
    console.log("Card tıklandı:", card.dataset.id);
  }
});

// Avantaj: Sonradan eklenen elementler de otomatik çalışır!
const newBtn = document.createElement("button");
newBtn.classList.add("item-btn");
newBtn.textContent = "Yeni Buton";
document.querySelector("#item-list").appendChild(newBtn);
// Bu butona tıklayınca da event delegation çalışır - ekstra listener gerekmez!
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Scope ve Closure — Ciktiyi Tahmin Et (Kolay)

Asagidaki kodlarin ciktisini calismadan once tahmin et, sonra calistirarak dogrula.

```javascript
// Senaryo 1: var vs let scope farki
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log("var:", i), 100);
}
for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log("let:", j), 100);
}
// Soru: var dongusunde neden hep ayni sayi basilir?
// Soru: let dongusunde neden farkli sayilar basilir?

// Senaryo 2: Closure ile counter
function createCounter(start = 0) {
  let count = start;
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count,
  };
}

const counter = createCounter(10);
console.log(counter.increment()); // ?
console.log(counter.increment()); // ?
console.log(counter.decrement()); // ?
console.log(counter.getCount());  // ?

// Senaryo 3: Event loop sirasi
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve().then(() => console.log("C"));
console.log("D");
// Sira: ?
```

**Beklenen Sonuc:** var dongusu 3,3,3 basar (function scope). let dongusu 0,1,2 basar (block scope). Counter 11,12,11,11 dondurur. Event loop sirasi A,D,C,B olur (sync > microtask > macrotask).
**Ipucu:** var function scope, let block scope olusturur. setTimeout macrotask queue'ya, Promise.then microtask queue'ya gider.

---

### Alistirma 2: Array Metodlari ile Veri Isleme (Orta)

Bir ogrenci listesi uzerinde filter, map, reduce ve sort metodlarini zincirleyerek veri analizi yap.

```javascript
const students = [
  { name: "Ahmet", grade: 85, department: "CS", year: 3 },
  { name: "Ayse", grade: 92, department: "CS", year: 4 },
  { name: "Mehmet", grade: 67, department: "EE", year: 2 },
  { name: "Fatma", grade: 78, department: "CS", year: 3 },
  { name: "Ali", grade: 95, department: "EE", year: 4 },
  { name: "Zeynep", grade: 88, department: "CS", year: 2 },
  { name: "Hasan", grade: 45, department: "ME", year: 1 },
  { name: "Elif", grade: 73, department: "EE", year: 3 },
];

// GOREV 1: CS bolumundeki gecen ogrencilerin (grade >= 60) isimlerini
// nota gore buyukten kucuge siralayip dondur
const csPassingStudents = students
  // TODO: filter, sort, map zinciri
  ;
console.log(csPassingStudents);
// Beklenen: ["Ayse", "Zeynep", "Ahmet", "Fatma"]

// GOREV 2: Her bolumun ortalama notunu hesapla
const departmentAverages = students.reduce((acc, student) => {
  // TODO: Her departman icin toplam ve sayi tut, sonra ortalama hesapla
}, {});
console.log(departmentAverages);
// Beklenen: { CS: 85.75, EE: 78.67, ME: 45 }

// GOREV 3: Not dagilimini hesapla (A: 90+, B: 80-89, C: 70-79, D: 60-69, F: <60)
const gradeDistribution = students.reduce((acc, student) => {
  // TODO: Implement
}, { A: 0, B: 0, C: 0, D: 0, F: 0 });
console.log(gradeDistribution);
// Beklenen: { A: 2, B: 2, C: 2, D: 1, F: 1 }
```

**Beklenen Sonuc:** Uc gorev de dogru sonuclari dondurmeli. Mutation olmamali (orijinal students array'i degismemeli). Method chaining okunabilir olmali.
**Ipucu:** `reduce`'da accumulator'un yapisini iyi tasarla. Ortalama icin hem toplam hem sayi tutman gerekir.

---

### Alistirma 3: this Keyword ve Event Delegation (Zor)

`this` keyword'unun farkli baglamlardaki davranisini test et ve event delegation ile dinamik bir liste olustur.

```javascript
// KISIM 1: this davranisi
const user = {
  name: "Ahmet",
  // Regular function — this objeye bagli
  greet() {
    console.log(`Merhaba, ${this.name}`);
  },
  // Arrow function — this lexical scope'tan gelir
  greetArrow: () => {
    console.log(`Merhaba, ${this.name}`); // this ne olur?
  },
  // Delayed greet
  delayedGreet() {
    // TODO: setTimeout icinde this'in kaybolma problemini 3 farkli yolla coz:
    // Yol 1: Arrow function
    // Yol 2: bind
    // Yol 3: const self = this
  },
};

user.greet();       // "Merhaba, Ahmet"
user.greetArrow();  // "Merhaba, undefined" — Neden?

const greetFn = user.greet;
greetFn();          // ? — this ne olur?
greetFn.bind(user)(); // ? — simdi ne olur?

// KISIM 2: Event Delegation ile TODO List
// Asagidaki HTML yapisini JavaScript ile olustur:
/*
<div id="app">
  <input id="todo-input" placeholder="Yeni gorev..." />
  <button id="add-btn">Ekle</button>
  <ul id="todo-list"></ul>
</div>
*/

// TODO: addEventListener'i sadece #todo-list'e ekle (event delegation)
// TODO: Her <li> icinde bir "Sil" butonu olsun
// TODO: Event delegation ile sil butonuna tiklayinca ilgili <li>'yi kaldir
// TODO: Bos input'ta ekleme yapilmasin

// Ornek:
// document.getElementById("todo-list").addEventListener("click", (e) => {
//   if (e.target.matches(".delete-btn")) {
//     e.target.closest("li").remove();
//   }
// });
```

**Beklenen Sonuc:** `this` farklarini aciklayabilmeli: regular function'da objeye, arrow function'da lexical scope'a bagli. Event delegation ile her yeni eklenen eleman icin ayri listener eklemeye gerek kalmamali.
**Ipucu:** Arrow function kendi `this`'ini olusturmaz, tanimlandigi scope'taki `this`'i kullanir. `e.target` tiklanan elemani, `e.target.closest()` en yakin parent'i bulur.
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdaki kodun çıktısı nedir?\nconsole.log('A');\nsetTimeout(() => console.log('B'), 0);\nPromise.resolve().then(() => console.log('C'));\nconsole.log('D');"
options:
  - "A, B, C, D"
  - "A, D, B, C"
  - "A, D, C, B"
  - "A, C, D, B"
correct: 2
explanation: "Senkron kod önce çalışır (A, D). Sonra microtask queue (Promise.then = C). En son macrotask queue (setTimeout = B). Sıra: A, D, C, B."
:::

:::knowledge-check
type: multiple_choice
question: "Closure nedir?"
options:
  - "Bir fonksiyonun sadece kendi scope'undaki değişkenlere erişebilmesi"
  - "Bir fonksiyonun tanımlandığı scope'taki değişkenlere, o scope kapandıktan sonra bile erişebilmesi"
  - "Global değişkenlerin her fonksiyondan erişilebilir olması"
  - "var ile tanımlanan değişkenlerin block scope oluşturmaması"
correct: 1
explanation: "Closure, bir fonksiyonun lexical scope'undaki (tanımlandığı yerdeki) değişkenlere, o scope'taki fonksiyon çalışmasını bitirdikten sonra bile erişebilme yeteneğidir. Bu sayede data privacy ve state management mümkün olur."
:::

:::knowledge-check
type: multiple_choice
question: "Arrow function'da this neyi referans eder?"
options:
  - "Arrow function'ın çağrıldığı objeyi"
  - "window/global objeyi"
  - "Lexical scope'taki (tanımlandığı yerdeki) this değerini"
  - "undefined"
correct: 2
explanation: "Arrow function'ların kendi this binding'i yoktur. this değerini lexical scope'tan (tanımlandıkları bağlamdan) alırlar. Bu yüzden callback'lerde this sorununu çözmek için idealdir."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6

### Prompt Ornekleri

**1. Konuyu Derinlemesine Anla:**
> "JavaScript'te closure'un calisma mekanizmasini adim adim acikla. Lexical scope nedir? Bir fonksiyon return edildikten sonra dis scope'taki degiskenler neden garbage collect edilmiyor? Closure'un bellekte nasil tutuldugunu goster."

*Neden:* Closure'u derinden anlamak, React hooks, memoization ve module pattern gibi modern JS kaliplarinin temelini kavramani saglar

**2. Pratik Uygulama:**
> "Su kodun ciktisini adim adim acikla: console.log('A'); setTimeout(() => console.log('B'), 0); Promise.resolve().then(() => console.log('C')); console.log('D'); -- Call stack, microtask queue ve macrotask queue'nun her adimda durumunu goster."

*Follow-up:* "setTimeout icinde bir Promise.then olsaydi, ve Promise.then icinde bir setTimeout olsaydi, cikti sirasi nasil degisirdi?"

**3. Mukemmellik Icin:**
> "JavaScript'te this keyword'unun 7 farkli binding kuralini (global, method, arrow, call/apply/bind, new, event handler, class) orneklerle acikla. Her durumda this neye isaret eder ve neden?"

### Pair Programming Ipucu
JS bug'i debug ederken AI'a hata mesajini ve kodu yapistir: "Bu kodda 'this' undefined donuyor. Sorunun scope, closure veya this binding'den hangisinden kaynaklandigini analiz et ve cozum oner."
:::

:::interview
## Mulakat Sorulari

**Soru 1: JavaScript'te closure nedir ve nerede kullanilir?**
- **Junior cevabi:** Closure, ic fonksiyonun dis fonksiyonun degiskenlerine erisebilmesidir.
- **Senior cevabi:** Closure, bir fonksiyonun olusturuldugu lexical scope'u hatirlamasidir. Pratikte data privacy (module pattern), event handler'larda state tutma, partial application ve currying icin kullanilir. Ancak dikkat edilmezse memory leak'e yol acabilir cunku closure referans tuttugu scope'u garbage collection'dan korur.

**Soru 2: == ve === arasindaki fark nedir? Neden sadece === kullanilmali?**
- **Junior cevabi:** == tip donusumu yapar, === yapmaz.
- **Senior cevabi:** == (loose equality) type coercion uygular ve beklenmeyen sonuclar uretir: `"" == false` true doner, `0 == ""` true doner. === (strict equality) hem tip hem deger kontrolu yapar. Pratikte her zaman === kullanilir. Tek istisna: `value == null` kontrolu hem null hem undefined'i yakalar, bu ESLint'te bile kabul edilen bir pattern'dir.
:::

:::exercise
### Alıştırma 4: Closure ile Private Counter Modülü

**Görev:** Closure kullanarak private state'e sahip bir counter modülü yaz. Dışarıdan doğrudan erişilemez olsun.

**Başlangıç kodu:**
```javascript
function createCounterModule(initialValue = 0, step = 1) {
  // TODO: Private degiskenler (closure ile gizli)
  // let count = initialValue;
  // let history = [];

  return {
    increment() { /* TODO */ },
    decrement() { /* TODO */ },
    reset() { /* TODO */ },
    getCount() { /* TODO */ },
    getHistory() { /* TODO: history'nin kopyasini dondur (orijinali degil) */ },
    undo() { /* TODO: son islemi geri al */ },
  };
}

// Test
const counter = createCounterModule(0, 5);

counter.increment();
counter.increment();
counter.increment();
console.log(counter.getCount());  // 15

counter.decrement();
console.log(counter.getCount());  // 10

counter.undo();
console.log(counter.getCount());  // 15

console.log(counter.getHistory());
// [0, 5, 10, 15, 10, 15]

// Private'a direkt erisim yok:
console.log(counter.count);     // undefined
console.log(counter.history);   // undefined

counter.reset();
console.log(counter.getCount());  // 0
```

**Beklenen çıktı:**
```
15
10
15
[0, 5, 10, 15, 10, 15]
undefined
undefined
0
```

**İpucu:** `getHistory()` orijinal array referansı yerine `[...history]` dönsün, dışarıdan mutate edilmesin.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: Event Loop Sıralama Tahmini

**Görev:** Aşağıdaki kodların çıktı sırasını tahmin et ve nedenlerini açıkla. Her birini önce tahmin et, sonra çalıştır.

**Başlangıç kodu:**
```javascript
// Senaryo 1: Karisik async
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
setTimeout(() => console.log("4"), 0);
Promise.resolve().then(() => {
  console.log("5");
  Promise.resolve().then(() => console.log("6"));
});
console.log("7");
// Tahmin: ?

// Senaryo 2: Nested setTimeout ve Promise
console.log("A");
setTimeout(() => {
  console.log("B");
  Promise.resolve().then(() => console.log("C"));
}, 0);
Promise.resolve().then(() => {
  console.log("D");
  setTimeout(() => console.log("E"), 0);
});
console.log("F");
// Tahmin: ?

// Senaryo 3: queueMicrotask
console.log("X");
queueMicrotask(() => console.log("Y"));
setTimeout(() => console.log("Z"), 0);
queueMicrotask(() => {
  console.log("W");
  queueMicrotask(() => console.log("V"));
});
console.log("U");
// Tahmin: ?
```

**Beklenen çıktı:**
```
Senaryo 1: 1, 7, 3, 5, 6, 2, 4
Senaryo 2: A, F, D, B, C, E
Senaryo 3: X, U, Y, W, V, Z
```

**İpucu:** Sıra: Sync kodu -> Microtask queue (Promise.then, queueMicrotask) -> Macrotask queue (setTimeout). Microtask'lar boşalana kadar macrotask çalışmaz.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: this Bağlamı Bulmaca

**Görev:** Aşağıdaki `this` senaryolarının çıktısını tahmin et. Arrow function, bind, call, apply farklarını göster.

**Başlangıç kodu:**
```javascript
const user = {
  name: "Ahmet",
  greet() {
    console.log(`Merhaba, ${this.name}`);
  },
  greetDelayed() {
    setTimeout(function () {
      console.log(`Delayed: ${this.name}`);
    }, 100);
  },
  greetDelayedArrow() {
    setTimeout(() => {
      console.log(`Arrow: ${this.name}`);
    }, 100);
  },
};

// Senaryo 1: Normal cagri
user.greet(); // ?

// Senaryo 2: Referans olarak atama
const greetFn = user.greet;
greetFn(); // ?

// Senaryo 3: bind ile
const boundGreet = user.greet.bind({ name: "Ayse" });
boundGreet(); // ?

// Senaryo 4: call ile
user.greet.call({ name: "Mehmet" }); // ?

// Senaryo 5: setTimeout icinde
user.greetDelayed(); // ?

// Senaryo 6: Arrow function ile
user.greetDelayedArrow(); // ?

// GOREV: Her senaryonun ciktisini tahmin et ve NEDENINI yaz
// Arrow: this = lexical scope (tanimlandigi yerdeki this)
// Regular: this = cagri noktasina bagli (dynamic)
```

**Beklenen çıktı:**
```
Merhaba, Ahmet
Merhaba, undefined
Merhaba, Ayse
Merhaba, Mehmet
Delayed: undefined
Arrow: Ahmet
```

**İpucu:** Arrow function kendi `this`'ini oluşturmaz, tanımlandığı scope'un `this`'ini kullanır. Regular function'da `this` çağrı şekline bağlıdır.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: Prototype Chain Keşfi

**Görev:** Prototype chain'i gösteren bir `inspectPrototypeChain` fonksiyonu yaz. Herhangi bir objenin prototype zincirini listesin.

**Başlangıç kodu:**
```javascript
function inspectPrototypeChain(obj) {
  // TODO:
  // 1. Object.getPrototypeOf() ile zinciri takip et
  // 2. Her seviyede prototype'in constructor adini ve property'lerini listele
  // 3. null'a ulasana kadar devam et
  const chain = [];
  let current = obj;

  while (current !== null) {
    const proto = Object.getPrototypeOf(current);
    chain.push({
      constructor: current.constructor?.name || "null",
      ownProps: Object.getOwnPropertyNames(current),
      level: chain.length,
    });
    current = proto;
  }

  return chain;
}

// Test 1: Array
console.log("=== Array Prototype Chain ===");
const arr = [1, 2, 3];
inspectPrototypeChain(arr).forEach((level) => {
  console.log(`  Level ${level.level}: ${level.constructor}`);
  console.log(`    Props: ${level.ownProps.slice(0, 5).join(", ")}...`);
});

// Test 2: Custom class
class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    return `${this.name} ses cikarir`;
  }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name);
    this.breed = breed;
  }
  bark() {
    return "Hav hav!";
  }
}

console.log("\n=== Dog Prototype Chain ===");
const dog = new Dog("Karabas", "Golden");
inspectPrototypeChain(dog).forEach((level) => {
  console.log(`  Level ${level.level}: ${level.constructor} -> [${level.ownProps.join(", ")}]`);
});

// Test 3: Method resolution
console.log(`\ndog.bark(): ${dog.bark()}`);
console.log(`dog.speak(): ${dog.speak()}`);
console.log(`dog.toString(): ${dog.toString()}`);
console.log(`dog.hasOwnProperty("name"): ${dog.hasOwnProperty("name")}`);
```

**Beklenen çıktı:**
```
=== Array Prototype Chain ===
  Level 0: Array
    Props: 0, 1, 2, length...
  Level 1: Array
    Props: length, constructor, concat, copyWithin, fill...
  Level 2: Object
    Props: constructor, __defineGetter__, __defineSetter__...

=== Dog Prototype Chain ===
  Level 0: Dog -> [name, breed]
  Level 1: Dog -> [constructor, bark]
  Level 2: Animal -> [constructor, speak]
  Level 3: Object -> [constructor, __defineGetter__, ...]

dog.bark(): Hav hav!
dog.speak(): Karabas ses cikarir
dog.toString(): [object Object]
dog.hasOwnProperty("name"): true
```

**İpucu:** `Object.getPrototypeOf(obj)` ile bir üst prototype'a geç. Chain `null`'a ulaşana kadar devam eder.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Debounce ve Throttle Implementasyonu

**Görev:** `debounce` ve `throttle` fonksiyonlarını sıfırdan yaz. Arama kutusu ve scroll event senaryolarında test et.

**Başlangıç kodu:**
```javascript
function debounce(func, delay) {
  // TODO:
  // 1. Her cagridiginda onceki timer'i iptal et (clearTimeout)
  // 2. Yeni timer baslat
  // 3. delay ms boyunca yeni cagri gelmezse fonksiyonu calistir
  let timerId;
  return function (...args) {
    // TODO
  };
}

function throttle(func, limit) {
  // TODO:
  // 1. Son cagri zamanini takip et
  // 2. limit ms icinde sadece bir kez calistir
  // 3. Aradaki cagrilari atla
  let lastCall = 0;
  return function (...args) {
    // TODO
  };
}

// Test: Debounce
const searchAPI = debounce((query) => {
  console.log(`API cagrildi: "${query}"`);
}, 300);

// Hizli ardisik cagrilar (sadece sonuncusu calismali)
console.log("=== Debounce Test ===");
searchAPI("j");
searchAPI("ja");
searchAPI("jav");
searchAPI("java");
searchAPI("javas");
searchAPI("javasc");
searchAPI("javascript"); // Sadece bu calismali

// Test: Throttle
let scrollCount = 0;
const handleScroll = throttle(() => {
  scrollCount++;
  console.log(`Scroll handled: ${scrollCount}`);
}, 100);

console.log("\n=== Throttle Test ===");
// 10 hizli cagri simulasyonu
for (let i = 0; i < 10; i++) {
  handleScroll();
}
// Sadece 1 kez calismali (ilk cagri)
```

**Beklenen çıktı:**
```
=== Debounce Test ===
API cagrildi: "javascript"

=== Throttle Test ===
Scroll handled: 1
```

**İpucu:** Debounce: `clearTimeout(timerId); timerId = setTimeout(...)`. Throttle: `Date.now() - lastCall >= limit` kontrolü.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: Mini DOM Manipülasyon Kütüphanesi

**Görev:** jQuery benzeri zincirleme (chaining) destekleyen basit bir DOM manipülasyon kütüphanesi yaz.

**Başlangıç kodu:**
```javascript
// Not: Bu kodu bir HTML dosyasinda <script> icinde calistir
function $(selector) {
  const elements =
    typeof selector === "string"
      ? document.querySelectorAll(selector)
      : [selector];

  const api = {
    elements: Array.from(elements),

    css(property, value) {
      // TODO: Her elemana style uygula, chaining icin this dondur
    },

    text(content) {
      // TODO: content verilmisse set et, verilmemisse get et
    },

    addClass(className) {
      // TODO: Her elemana class ekle
    },

    removeClass(className) {
      // TODO: Her elemandan class kaldir
    },

    on(event, callback) {
      // TODO: Her elemana event listener ekle
    },

    html(content) {
      // TODO: innerHTML set/get
    },

    each(callback) {
      // TODO: Her eleman icin callback cagir
    },

    hide() {
      return this.css("display", "none");
    },

    show() {
      return this.css("display", "");
    },
  };

  return api;
}

// Test (console'da calistir)
// $("p").css("color", "red").css("font-size", "18px").addClass("highlight");
// $(".btn").on("click", (e) => console.log("Tiklandi!"));
// $("h1").text("Yeni Baslik");

// Node.js ile test (DOM simulasyonu)
console.log("Mini DOM kutuphanesi hazirlandi");
console.log("Ornekler:");
console.log('  $("p").css("color", "red").addClass("highlight")');
console.log('  $("h1").text("Yeni Baslik")');
console.log('  $(".btn").on("click", handler).hide()');
```

**Beklenen çıktı:**
```
Mini DOM kutuphanesi hazirlandi
Ornekler:
  $("p").css("color", "red").addClass("highlight")
  $("h1").text("Yeni Baslik")
  $(".btn").on("click", handler).hide()
```

**İpucu:** Her metod `this` (api nesnesini) dönerek method chaining sağlar. `elements.forEach()` ile tüm eşleşen elemanları dolaş.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 10: Custom Promise Implementasyonu

**Görev:** `Promise`'in basitleştirilmiş bir versiyonunu sıfırdan yaz. `then`, `catch` ve `resolve`/`reject` desteklesin.

**Başlangıç kodu:**
```javascript
class MyPromise {
  constructor(executor) {
    this.state = "pending"; // pending, fulfilled, rejected
    this.value = undefined;
    this.callbacks = [];

    const resolve = (value) => {
      // TODO: state'i fulfilled yap, value'yu kaydet, callback'leri cagir
    };

    const reject = (reason) => {
      // TODO: state'i rejected yap, reason'i kaydet, callback'leri cagir
    };

    try {
      executor(resolve, reject);
    } catch (error) {
      reject(error);
    }
  }

  then(onFulfilled, onRejected) {
    // TODO:
    // 1. Yeni MyPromise dondur (chaining icin)
    // 2. State fulfilled ise onFulfilled'i hemen cagir
    // 3. State pending ise callback listesine ekle
    // 4. onFulfilled'in donusu sonraki then'e gecmeli
  }

  catch(onRejected) {
    return this.then(null, onRejected);
  }

  static resolve(value) {
    return new MyPromise((resolve) => resolve(value));
  }

  static reject(reason) {
    return new MyPromise((_, reject) => reject(reason));
  }
}

// Test 1: Basit resolve
new MyPromise((resolve) => {
  setTimeout(() => resolve(42), 100);
})
  .then((value) => {
    console.log(`Resolved: ${value}`); // 42
    return value * 2;
  })
  .then((value) => {
    console.log(`Chained: ${value}`); // 84
  });

// Test 2: Error handling
new MyPromise((_, reject) => {
  setTimeout(() => reject("Hata olustu!"), 100);
}).catch((error) => {
  console.log(`Caught: ${error}`);
});

// Test 3: Sync resolve
MyPromise.resolve("hemen")
  .then((v) => console.log(`Static resolve: ${v}`));
```

**Beklenen çıktı:**
```
Static resolve: hemen
Resolved: 42
Chained: 84
Caught: Hata olustu!
```

**İpucu:** `then()` her zaman yeni MyPromise döner. State zaten fulfilled ise callback'i `queueMicrotask` veya `setTimeout` ile async çağır.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Curry ve Partial Application

**Görev:** `curry` fonksiyonu yaz. Herhangi bir fonksiyonu curried versiyonuna çevirsin.

**Başlangıç kodu:**
```javascript
function curry(fn) {
  // TODO: fn'in tum argumanlari gelene kadar yeni fonksiyon dondur
  // Tum argumanlar geldiginde fonksiyonu calistir
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return function (...args2) {
      return curried.apply(this, args.concat(args2));
    };
  };
}

// Test
const add = curry((a, b, c) => a + b + c);
console.log(add(1)(2)(3));     // 6
console.log(add(1, 2)(3));     // 6
console.log(add(1)(2, 3));     // 6
console.log(add(1, 2, 3));     // 6

const multiply = curry((a, b) => a * b);
const double = multiply(2);
const triple = multiply(3);
console.log(double(5));   // 10
console.log(triple(5));   // 15

// Pratik kullanim
const filter = curry((predicate, arr) => arr.filter(predicate));
const map = curry((transform, arr) => arr.map(transform));

const getAdults = filter(p => p.age >= 18);
const getNames = map(p => p.name);

const people = [{name:"Ali",age:25},{name:"Can",age:15},{name:"Eda",age:30}];
console.log(getNames(getAdults(people))); // ["Ali", "Eda"]
```

**Beklenen çıktı:**
```
6
6
6
6
10
15
["Ali", "Eda"]
```

**İpucu:** `fn.length` fonksiyonun beklediği parametre sayısını döner. Yeterli argüman gelmediyse yeni fonksiyon döndür.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 12: WeakRef ile Memory-Safe Cache

**Görev:** `WeakRef` kullanarak garbage collection'a izin veren bir cache sistemi yaz.

**Başlangıç kodu:**
```javascript
class WeakCache {
  constructor() {
    this.cache = new Map();
    this.registry = new FinalizationRegistry((key) => {
      console.log(`  [GC] Cache'ten silindi: ${key}`);
      this.cache.delete(key);
    });
  }

  set(key, value) {
    const ref = new WeakRef(value);
    this.cache.set(key, ref);
    this.registry.register(value, key);
  }

  get(key) {
    const ref = this.cache.get(key);
    if (!ref) return undefined;
    const value = ref.deref();
    if (!value) {
      this.cache.delete(key);
      return undefined;
    }
    return value;
  }

  get size() {
    return this.cache.size;
  }
}

// Test
const cache = new WeakCache();
let user1 = { id: 1, name: "Ahmet", data: new Array(1000).fill("x") };
let user2 = { id: 2, name: "Ayse", data: new Array(1000).fill("y") };

cache.set("user:1", user1);
cache.set("user:2", user2);

console.log("Cache size:", cache.size);
console.log("user:1:", cache.get("user:1")?.name);

// Referansi kaldir (GC'ye hazir)
user1 = null;
// GC tetiklenmesi garanti degil ama WeakRef bunu mumkun kilar

console.log("user:2:", cache.get("user:2")?.name);
console.log("WeakRef cache hafiza-guvenli!");
```

**Beklenen çıktı:**
```
Cache size: 2
user:1: Ahmet
user:2: Ayse
WeakRef cache hafiza-guvenli!
```

**İpucu:** `WeakRef` objeye zayıf referans tutar, GC'yi engellemez. `FinalizationRegistry` obje GC tarafından temizlendiğinde callback çağırır.

**Zorluk:** Zor
:::

:::must-note
- **Scope:** var = function scope, let/const = block scope. Önce const, gerekirse let kullan, var asla
- **Hoisting:** var tanımı yukarı taşınır (undefined), let/const da hoist edilir ama TDZ nedeniyle erişilemez
- **TDZ (Temporal Dead Zone):** let/const scope başlangıcından tanıma kadar olan erişilemez bölge
- **Closure:** Fonksiyonun dış scope'taki değişkenleri hatırlaması. Kullanım: data privacy, memoization, factory pattern
- **this kuralları:** Object method = obje, arrow function = lexical this, call/apply/bind = manuel bağlama, global = window
- **Prototypal Inheritance:** JS'te gerçek class yok, ES6 class syntax prototype üzerinde syntax sugar
- **Event Loop sırası:** Call Stack (senkron) > Microtask Queue (Promise.then) > Macrotask Queue (setTimeout)
- **Microtask vs Macrotask:** Promise.then, queueMicrotask = microtask. setTimeout, setInterval, DOM event = macrotask
- **DOM Seçiciler:** getElementById, querySelector (tek), querySelectorAll (çoklu)
- **Event Delegation:** Parent'a tek listener, event.target ile child kontrolü. Performans + dinamik element desteği
- **const object/array:** Referans kilitlenir, içerik değiştirilebilir (immutable DEĞİL)
- **for + var + setTimeout:** Klasik closure hatası. let kullanarak veya IIFE ile çözülür
:::

:::senior-learns
Bir Senior Developer veya CTO, JavaScript temellerini öğrenirken şu yaklaşımı benimser:

1. **ECMAScript spesifikasyonunu okur** - tc39.es/ecma262 adresindeki resmi spesifikasyonu referans alır. "MDN sana nasıl kullanacağını söyler, spec sana neden böyle çalıştığını söyler" prensibiyle hareket eder.
2. **V8 engine blog'unu takip eder** - v8.dev/blog adresinde yayınlanan makalelerden JS engine'in kodu nasıl optimize ettiğini (hidden classes, inline caching, JIT compilation) öğrenir. Performans optimizasyonunu engine seviyesinde anlar.
3. **Memory leak'leri profiler ile avlar** - Chrome DevTools Memory tab'ında heap snapshot alarak closure kaynaklı memory leak'leri tespit eder. Detached DOM node'ları ve event listener leak'lerini bulur. `performance.mark()` ve `performance.measure()` ile custom metrikler oluşturur.
4. **Microtask timing'ini production'da kullanır** - Promise.resolve().then() ile DOM update sonrası hesaplama yapmak, queueMicrotask ile batch update yapmak gibi ileri seviye pattern'leri uygular. React'in fiber architecture'ının neden microtask/macrotask ayrımını kullandığını anlar.
5. **Prototype chain'i debug eder** - Object.getPrototypeOf(), hasOwnProperty() vs in operatörü farkını bilir. Performans kritik kodda prototype lookup maliyetini anlar ve gerektiğinde property'leri doğrudan objeye kopyalar.
6. **WeakRef ve FinalizationRegistry kullanır** - ES2021 ile gelen zayıf referansları anlar. Cache mekanizmalarında memory-friendly çözümler üretir. Garbage collector'ın nasıl çalıştığını bilir.

**Profesyonel Mindset:** "JavaScript'in quirk'lerini (tuhaf davranışlarını) ezberlemek değil, neden öyle davrandığını anlamak önemli. Scope chain nasıl çözümlenir, closure neden bir object reference tutar, event loop neden microtask'lara öncelik verir - bunları anladığında her yeni JS özelliğini saniyeler içinde kavrayabilirsin. Framework'ler değişir, engine mekanizmaları kalır."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Scope** (skoʊp) → Kapsam / Erişim alanı
   *"Variables declared with let have block scope, meaning they are only accessible within the enclosing block."*

2. **Hoisting** (hɔɪstɪŋ) → Yukarı taşıma
   *"Due to hoisting, function declarations can be called before they appear in the code."*

3. **Closure** (kloʊʒər) → Kapanış
   *"A closure gives you access to an outer function's scope from an inner function."*

4. **Event Loop** (ɪˈvent luːp) → Olay döngüsü
   *"The event loop continuously checks if the call stack is empty and then processes the next task from the queue."*

5. **Prototype** (proʊtətaɪp) → Prototip
   *"Every JavaScript object has a prototype from which it can inherit properties and methods."*

**Okuma Egzersizi:** MDN'de "Closures" makalesini İngilizce oku: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "JavaScript scope ve closure örneklerini ekledim"
→ Örnek: `feat: add JavaScript scope and closure examples`
:::

:::external-resource
- 📺 **Fireship:** "JavaScript in 100 Seconds" + "The JavaScript Survival Guide" (YouTube, ücretsiz)
- 📖 **javascript.info:** "The Modern JavaScript Tutorial" - Closure ve Scope bölümleri (ücretsiz)
- 📺 **Philip Roberts:** "What the heck is the event loop anyway?" (JSConf, YouTube, 26 dk, ücretsiz)
- 📖 **MDN Web Docs:** "JavaScript Guide" (İngilizce, ücretsiz)
- 📖 **Kyle Simpson:** "You Don't Know JS" serisi (GitHub'da ücretsiz)
:::
