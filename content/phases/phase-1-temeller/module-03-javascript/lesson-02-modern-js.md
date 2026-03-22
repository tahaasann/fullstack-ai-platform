---
id: mod-03-js/lesson-02
title: "Modern JavaScript: ES6+ ve Async Patterns"
estimated_minutes: 55
tags: ["es6+", "destructuring", "async/await", "promises", "spread", "modules"]
prerequisites: ["mod-03-js/lesson-01"]
order: 2
---

# Modern JavaScript: ES6+ ve Async Patterns

:::realworld
ES6 (2015) JavaScript'i tamamen dönüştürdü. Bugün yazılan profesyonel kodun %100'ü ES6+ syntax kullanıyor. React, Vue, Angular, Node.js - hepsi modern JavaScript üzerine inşa edildi. Bu derste, iş mülakatlarında ve günlük kodlamada karşına çıkacak her modern JS özelliğini derinlemesine öğreneceksin. Bir senior developer'ın "temiz kod" dediği şey, büyük ölçüde bu özelliklerin doğru kullanımıdır.
:::

## Neden Bu Konuyu Öğreniyorsun?

Modern JavaScript bilmeden bugünün ekosisteminde tek satır anlamlı kod yazamazsın. Framework'lerin dökümantasyonları, open source projeler ve iş ilanlarındaki teknik gereksinimler tamamen ES6+ üzerine kuruludur.

- Destructuring bilmeden React props ve state yönetemezsin
- async/await bilmeden API çağrısı yapamazsın
- Spread operator bilmeden immutable state güncelleyemezsin
- ES Modules bilmeden proje yapısı kuramazsın

:::deha-tip
Deha seviyesi geliştiriciler, her yeni ES özelliğini öğrenirken "Bu hangi problemi çözüyor?" sorusuyla başlar. Syntax ezberlemek yerine, o özelliğin neden var olduğunu anlarlar. Örneğin destructuring, deeply nested obje erişimini temizler; async/await ise callback hell'i ortadan kaldırır.
:::

## Destructuring: Verileri Parçalama

:::concept[Destructuring (İng: Destructuring Assignment)]
Destructuring, array veya object'ten değerleri çıkarıp ayrı değişkenlere atama işlemidir.

**Türkçe karşılığı:** Yapı Söküm / Parçalama Ataması
**Ne işe yarar:** Veri yapılarından ihtiyacın olan parçaları temiz şekilde çıkarırsın
**Gerçek hayat benzetmesi:** Bir bavuldan sadece ihtiyacın olan kıyafetleri çıkarmak gibi - her şeyi dökmeden istediğini alırsın
:::

### Object Destructuring

:::code[javascript]{title="Object Destructuring Temelleri"}
const user = {
  name: 'Ahmet',
  age: 28,
  city: 'Istanbul',
  role: 'developer'
};

// Eski yol (ES5)
var name = user.name;
var age = user.age;

// Modern yol (ES6+)
const { name, age, city } = user;

// Renaming: farklı isimle al
const { name: userName, age: userAge } = user;
console.log(userName); // 'Ahmet'

// Default values: yoksa varsayılan kullan
const { name, salary = 0 } = user;
console.log(salary); // 0 (user'da salary yok)

// Renaming + Default birlikte
const { role: userRole = 'guest' } = user;
:::

### Array Destructuring

:::code[javascript]{title="Array Destructuring"}
const colors = ['red', 'green', 'blue', 'yellow'];

// Sırayla al
const [first, second] = colors;
console.log(first);  // 'red'
console.log(second); // 'green'

// Atlama (skip)
const [, , third] = colors;
console.log(third); // 'blue'

// Rest ile kalanları topla
const [primary, ...others] = colors;
console.log(others); // ['green', 'blue', 'yellow']

// Swap (yer değiştirme) - temp değişken yok!
let a = 1, b = 2;
[a, b] = [b, a];
console.log(a, b); // 2, 1

// Default values
const [x = 10, y = 20] = [5];
console.log(x, y); // 5, 20
:::

### Nested Destructuring

:::code[javascript]{title="Nested (İç İçe) Destructuring"}
const company = {
  name: 'TechCorp',
  address: {
    city: 'Istanbul',
    district: 'Kadikoy',
    coordinates: {
      lat: 40.99,
      lng: 29.02
    }
  },
  employees: ['Ali', 'Veli', 'Ayse']
};

// Nested object destructuring
const {
  name: companyName,
  address: {
    city,
    coordinates: { lat, lng }
  },
  employees: [firstEmployee]
} = company;

console.log(city);          // 'Istanbul'
console.log(lat);           // 40.99
console.log(firstEmployee); // 'Ali'
:::

:::beginner-mistake
Yaygın hata: Nested destructuring'de üst property'yi de kullanmak isteyip hata almak. `address: { city }` yazdığında `address` değişkeni tanımlanmaz, sadece `city` tanımlanır. İkisini de istiyorsan: `address: { city }, address` yazamazsın. Bunun yerine ayrı satırda `const { address } = company` yap.
:::

### Function Parameter Destructuring

:::code[javascript]{title="Fonksiyon Parametrelerinde Destructuring"}
// API response'larını işlerken çok kullanılır
function displayUser({ name, age, role = 'user' }) {
  console.log(`${name} (${age}) - ${role}`);
}

displayUser({ name: 'Zeynep', age: 25 });
// "Zeynep (25) - user"

// React component'lerde her gün göreceksin:
// function UserCard({ name, avatar, isOnline = false }) { ... }
:::

## Spread ve Rest Operator (...)

:::concept[Spread/Rest Operator (İng: Spread/Rest)]
`...` operatörü iki farklı amaçla kullanılır: Spread (yayma) bir iterable'ı parçalarına ayırır, Rest (toplama) birden fazla elemanı bir araya toplar.

**Türkçe karşılığı:** Yayma / Toplama Operatörü
**Ne işe yarar:** Array ve object'leri kopyalar, birleştirir veya fonksiyon parametrelerini toplar
**Gerçek hayat benzetmesi:** Spread = bir kutu legoyu masaya dökmek. Rest = masadaki legoları kutuya toplamak
:::

:::code[javascript]{title="Spread Operator"}
// Array spread
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const merged = [...arr1, ...arr2];        // [1, 2, 3, 4, 5, 6]
const withNew = [...arr1, 99, ...arr2];   // [1, 2, 3, 99, 4, 5, 6]

// Array kopyalama (shallow copy)
const copy = [...arr1];

// Object spread
const defaults = { theme: 'dark', lang: 'tr', fontSize: 14 };
const userPrefs = { lang: 'en', fontSize: 16 };
const settings = { ...defaults, ...userPrefs };
// { theme: 'dark', lang: 'en', fontSize: 16 }
// Sonraki aynı key'ler öncekini ezer!

// React'te immutable state update:
// setState(prev => ({ ...prev, name: 'Yeni' }));
:::

:::code[javascript]{title="Rest Operator"}
// Function rest parameters
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}
sum(1, 2, 3, 4); // 10

// İlk parametreyi ayır, kalanını topla
function logFirst(first, ...rest) {
  console.log('First:', first);
  console.log('Rest:', rest);
}
logFirst('a', 'b', 'c'); // First: a, Rest: ['b', 'c']

// Object rest (belirli key'leri çıkar, kalanını al)
const { password, ...safeUser } = {
  name: 'Ali',
  email: 'ali@mail.com',
  password: '12345'
};
// safeUser = { name: 'Ali', email: 'ali@mail.com' }
// password bilgisini API response'dan temizlemek için harika!
:::

## Optional Chaining ve Nullish Coalescing

:::concept[Optional Chaining (İng: Optional Chaining)]
`?.` operatörü, bir property'ye erişirken null veya undefined kontrolü yapar. Eğer zincirdeki herhangi bir değer nullish ise, hata fırlatmak yerine `undefined` döner.

**Türkçe karşılığı:** Opsiyonel Zincirleme
**Ne işe yarar:** Deeply nested objelerde güvenli erişim sağlar, TypeError'dan korur
**Gerçek hayat benzetmesi:** Kapıyı çalmadan önce evin var mı diye kontrol etmek
:::

:::code[javascript]{title="Optional Chaining (?.)"}
const user = {
  name: 'Mehmet',
  address: {
    city: 'Ankara'
  }
};

// Eski yol - uzun ve çirkin
const zip = user && user.address && user.address.zipCode;

// Modern yol
const zip = user?.address?.zipCode;        // undefined (hata yok!)
const street = user?.address?.street?.name; // undefined

// Array elemanlarında
const users = [{ name: 'Ali' }];
const second = users?.[1]?.name;           // undefined

// Fonksiyon çağrısında
const result = user?.getProfile?.();       // undefined (method yoksa)
:::

:::code[javascript]{title="Nullish Coalescing (??)"}
// ?? sadece null ve undefined'da fallback kullanır
// || ise tüm falsy değerlerde (0, '', false) fallback kullanır

const count = 0;
console.log(count || 10);  // 10  (yanlış! 0 geçerli bir değer)
console.log(count ?? 10);  // 0   (doğru! 0 null/undefined değil)

const text = '';
console.log(text || 'default');  // 'default' (yanlış olabilir)
console.log(text ?? 'default');  // ''         (doğru)

// Pratikte birlikte kullanımı
const config = response?.data?.settings?.theme ?? 'light';
:::

:::beginner-mistake
Yaygın hata: `||` ile `??` farkını bilmemek. `const port = config.port || 3000` yazarsan ve `config.port = 0` ise, port 3000 olur (yanlış!). `??` kullan: `const port = config.port ?? 3000` - bu durumda port 0 kalır.
:::

## Template Literals ve Tagged Templates

:::code[javascript]{title="Template Literals"}
const name = 'Ayse';
const age = 30;

// String interpolation
const greeting = `Merhaba ${name}, ${age} yasindasin!`;

// Multi-line strings
const html = `
  <div class="card">
    <h2>${name}</h2>
    <p>Yas: ${age}</p>
  </div>
`;

// Expression kullanabilirsin
const message = `Durum: ${age >= 18 ? 'Yetiskin' : 'Cocuk'}`;
const total = `Toplam: ${(19.99 * 3).toFixed(2)} TL`;
:::

:::code[javascript]{title="Tagged Templates (İleri Seviye)"}
// Tagged template = template literal'i fonksiyonla isleme
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i] !== undefined ? `<mark>${values[i]}</mark>` : '';
    return result + str + value;
  }, '');
}

const product = 'Laptop';
const price = 15000;
const output = highlight`Urun: ${product}, Fiyat: ${price} TL`;
// "Urun: <mark>Laptop</mark>, Fiyat: <mark>15000</mark> TL"

// Gercek dunyada: styled-components, GraphQL (gql`...`), i18n
:::

## Array Methods Derinlemesine

:::concept[Higher-Order Functions (İng: Higher-Order Functions)]
Higher-order function, parametre olarak fonksiyon alan veya fonksiyon döndüren fonksiyondur. Array method'ları (map, filter, reduce) bunun en yaygın örnekleridir.

**Türkçe karşılığı:** Üst Düzey Fonksiyonlar
**Ne işe yarar:** Veri dönüşümlerini deklaratif (ne yapılacağını belirterek) şekilde ifade eder
**Gerçek hayat benzetmesi:** Fabrika bantı gibi - her istasyon (method) veriye bir işlem uygular ve sonraki istasyona geçirir
:::

:::code[javascript]{title="map, filter, reduce - Kutsal Üçlü"}
const products = [
  { name: 'Laptop', price: 15000, category: 'electronics' },
  { name: 'Kalem', price: 5, category: 'office' },
  { name: 'Mouse', price: 200, category: 'electronics' },
  { name: 'Defter', price: 15, category: 'office' },
  { name: 'Klavye', price: 500, category: 'electronics' }
];

// map: her elemanı dönüştür (1-1 eşleme)
const names = products.map(p => p.name);
// ['Laptop', 'Kalem', 'Mouse', 'Defter', 'Klavye']

// filter: koşula uyanları filtrele
const electronics = products.filter(p => p.category === 'electronics');
// [{ name: 'Laptop', ... }, { name: 'Mouse', ... }, { name: 'Klavye', ... }]

// reduce: tek bir değere indirge
const totalPrice = products.reduce((sum, p) => sum + p.price, 0);
// 15720

// Zincirleme (chaining) - çok güçlü!
const electronicsTotal = products
  .filter(p => p.category === 'electronics')
  .map(p => p.price)
  .reduce((sum, price) => sum + price, 0);
// 15700
:::

:::code[javascript]{title="find, some, every"}
const users = [
  { id: 1, name: 'Ali', active: true },
  { id: 2, name: 'Veli', active: false },
  { id: 3, name: 'Ayse', active: true }
];

// find: koşula uyan İLK elemanı döndür (veya undefined)
const veli = users.find(u => u.name === 'Veli');
// { id: 2, name: 'Veli', active: false }

// some: en az biri koşulu sağlıyor mu? (boolean)
const hasInactive = users.some(u => !u.active);   // true

// every: hepsi koşulu sağlıyor mu? (boolean)
const allActive = users.every(u => u.active);      // false
:::

:::code[javascript]{title="flat, flatMap, at"}
// flat: iç içe array'leri düzleştirir
const nested = [1, [2, 3], [4, [5, 6]]];
nested.flat();     // [1, 2, 3, 4, [5, 6]]  (1 seviye)
nested.flat(2);    // [1, 2, 3, 4, 5, 6]    (2 seviye)
nested.flat(Infinity); // tamamen düzleştir

// flatMap: map + flat(1) - tek adımda
const sentences = ['Merhaba dunya', 'Nasilsin'];
const words = sentences.flatMap(s => s.split(' '));
// ['Merhaba', 'dunya', 'Nasilsin']

// at: negatif index ile sondan erişim
const arr = [10, 20, 30, 40, 50];
arr.at(0);   // 10
arr.at(-1);  // 50 (son eleman!)
arr.at(-2);  // 40
// arr[-1] çalışmaz (undefined döner), at() kullan
:::

:::beginner-mistake
Yaygın hata: `map` ile `forEach` karıştırmak. `map` yeni array döndürür, `forEach` undefined döndürür. Dönüşüm istiyorsan `map`, sadece yan etki (side effect) istiyorsan `forEach` kullan. Ayrıca `find` ile `filter` karıştırmak: `find` tek eleman, `filter` array döndürür.
:::

## Object Methods

:::code[javascript]{title="Object.keys, Object.values, Object.entries"}
const config = {
  host: 'localhost',
  port: 3000,
  debug: true
};

Object.keys(config);    // ['host', 'port', 'debug']
Object.values(config);  // ['localhost', 3000, true]
Object.entries(config); // [['host','localhost'], ['port',3000], ['debug',true]]

// entries ile destructuring - çok kullanışlı
for (const [key, value] of Object.entries(config)) {
  console.log(`${key}: ${value}`);
}

// Object.fromEntries: entries'i objeye çevir (ters işlem)
const doubled = Object.fromEntries(
  Object.entries(config)
    .filter(([key]) => key !== 'debug')
);
// { host: 'localhost', port: 3000 }
:::

:::code[javascript]{title="Object.assign ve Object.freeze"}
// Object.assign: objeleri birleştir (mutate eder!)
const target = { a: 1, b: 2 };
Object.assign(target, { b: 3, c: 4 });
// target artık { a: 1, b: 3, c: 4 }

// Kopyalama için boş objeyle başla
const copy = Object.assign({}, target, { d: 5 });
// Ama spread daha temiz: const copy = { ...target, d: 5 };

// Object.freeze: objeyi dondur (immutable yap)
const frozen = Object.freeze({ name: 'Ali', age: 25 });
frozen.name = 'Veli';  // Sessizce başarısız olur (strict mode'da hata)
console.log(frozen.name); // 'Ali'

// DİKKAT: freeze shallow'dur, nested objeler değişebilir!
const deep = Object.freeze({ inner: { value: 1 } });
deep.inner.value = 99; // Bu çalışır! Sadece üst seviye donmuş
:::

## Async Patterns: Callback'ten async/await'e Evrim

:::concept[Asynchronous Programming (İng: Asynchronous)]
Asenkron programlama, uzun süren işlemlerin (API çağrısı, dosya okuma) ana thread'i bloklamadan çalışmasını sağlar.

**Türkçe karşılığı:** Eş Zamanlı Olmayan Programlama
**Ne işe yarar:** UI donmadan arka planda işlem yürütür
**Gerçek hayat benzetmesi:** Restoranda yemek siparişi ver, masada otur ve bekle - mutfak (async işlem) hazırlarken sen sohbet edebilirsin (main thread boşta)
:::

### Evrim: Callbacks -> Promises -> async/await

:::code[javascript]{title="1. Callback Hell (Eski Yol - Kaçın!)"}
// Her async işlem bir callback alır, iç içe girer
getUser(userId, function(user) {
  getOrders(user.id, function(orders) {
    getOrderDetails(orders[0].id, function(details) {
      getShippingInfo(details.shippingId, function(shipping) {
        console.log(shipping);
        // "Pyramid of doom" - okunamaz!
      });
    });
  });
});
:::

:::code[javascript]{title="2. Promises (Daha İyi)"}
getUser(userId)
  .then(user => getOrders(user.id))
  .then(orders => getOrderDetails(orders[0].id))
  .then(details => getShippingInfo(details.shippingId))
  .then(shipping => console.log(shipping))
  .catch(error => console.error('Hata:', error));
// Düz zincir, okunabilir, tek catch tüm hataları yakalar
:::

:::code[javascript]{title="3. async/await (En İyi - Bunu Kullan!)"}
async function getShippingDetails(userId) {
  try {
    const user = await getUser(userId);
    const orders = await getOrders(user.id);
    const details = await getOrderDetails(orders[0].id);
    const shipping = await getShippingInfo(details.shippingId);
    return shipping;
  } catch (error) {
    console.error('Hata:', error);
    throw error; // Gerekirse tekrar fırlat
  }
}
// Senkron kod gibi okunur ama asenkron çalışır!
:::

### Promise Birleştiricileri

:::code[javascript]{title="Promise.all, race, allSettled, any"}
const fetchUser = fetch('/api/user').then(r => r.json());
const fetchPosts = fetch('/api/posts').then(r => r.json());
const fetchComments = fetch('/api/comments').then(r => r.json());

// Promise.all: HEPSİ başarılı olursa çözülür, biri fail olursa reject
const [user, posts, comments] = await Promise.all([
  fetchUser, fetchPosts, fetchComments
]);
// Paralel çalışır! 3 ardışık await'ten çok daha hızlı

// Promise.race: İLK tamamlanan (başarılı veya başarısız)
const fastest = await Promise.race([
  fetch('/api/server1'),
  fetch('/api/server2')
]);
// Timeout pattern:
const withTimeout = Promise.race([
  fetch('/api/data'),
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout!')), 5000)
  )
]);

// Promise.allSettled: Hepsi tamamlanana kadar bekle (fail olsa bile)
const results = await Promise.allSettled([
  fetchUser, fetchPosts, fetchComments
]);
// results: [
//   { status: 'fulfilled', value: {...} },
//   { status: 'rejected', reason: Error },
//   { status: 'fulfilled', value: {...} }
// ]
// Hangisi başarılı, hangisi başarısız ayrı ayrı kontrol et

// Promise.any: İLK BAŞARILI olan (tüm reject olursa AggregateError)
const firstSuccess = await Promise.any([
  fetch('/mirror1/data'),
  fetch('/mirror2/data'),
  fetch('/mirror3/data')
]);
:::

:::comparison
| Method | Davranış | Ne Zaman Kullan |
|--------|----------|-----------------|
| `Promise.all` | Hepsi başarılı olmalı, biri fail = tümü fail | Birbiriyle ilişkili paralel istekler |
| `Promise.race` | İlk tamamlanan (başarılı/başarısız) kazanır | Timeout, en hızlı mirror |
| `Promise.allSettled` | Hepsini bekle, sonuçları ayrı ayrı kontrol et | Bağımsız istekler, partial failure kabul |
| `Promise.any` | İlk başarılı olan kazanır | Fallback mirror'lar, redundancy |
:::

## Error Handling in Async Code

:::code[javascript]{title="try/catch ile Async Hata Yönetimi"}
// Temel pattern
async function fetchData(url) {
  try {
    const response = await fetch(url);

    // HTTP hata kontrolü (fetch 404'te reject olmaz!)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    if (error.name === 'TypeError') {
      // Network hatası (sunucu kapalı, internet yok)
      console.error('Network hatasi:', error.message);
    } else {
      console.error('Genel hata:', error.message);
    }
    throw error; // Yukarıya ilet (çağıran fonksiyon da yakalasın)
  }
}

// Birden fazla async işlemde selective try/catch
async function processOrder(orderId) {
  // Kritik: hata olursa dur
  const order = await fetchData(`/api/orders/${orderId}`);

  // Kritik değil: hata olursa devam et
  let recommendations = [];
  try {
    recommendations = await fetchData(`/api/recommendations/${orderId}`);
  } catch {
    // Öneriler yüklenemezse sorun değil, boş array ile devam
  }

  return { order, recommendations };
}
:::

:::beginner-mistake
Yaygın hata: `fetch` fonksiyonunun 404 veya 500 durumlarında reject olmadığını bilmemek. `fetch` sadece network hatalarında (sunucuya ulaşılamadığında) reject olur. HTTP hatalarını `response.ok` veya `response.status` ile kendin kontrol etmelisin.
:::

## ES Modules vs CommonJS

:::code[javascript]{title="ES Modules (import/export) - Modern Standart"}
// named export (birden fazla olabilir)
// utils.js
export const PI = 3.14159;
export function calculateArea(r) {
  return PI * r * r;
}
export class Circle {
  constructor(r) { this.radius = r; }
}

// named import
import { PI, calculateArea } from './utils.js';
import { calculateArea as calcArea } from './utils.js'; // renaming

// default export (dosya başına tek)
// logger.js
export default class Logger {
  log(msg) { console.log(msg); }
}

// default import (istediğin isimle)
import Logger from './logger.js';
import MyLogger from './logger.js'; // farklı isim de olur

// hepsini al
import * as Utils from './utils.js';
Utils.PI; // 3.14159
:::

:::code[javascript]{title="CommonJS (require) - Node.js Eski Sistem"}
// module.exports ile export
// utils.js
const PI = 3.14159;
function calculateArea(r) { return PI * r * r; }
module.exports = { PI, calculateArea };

// require ile import
const { PI, calculateArea } = require('./utils');

// Tek şey export
// logger.js
module.exports = class Logger { /* ... */ };

// require ile al
const Logger = require('./logger');
:::

:::comparison
| Özellik | ES Modules | CommonJS |
|---------|-----------|----------|
| Syntax | `import/export` | `require/module.exports` |
| Loading | Statik (compile time) | Dinamik (runtime) |
| Tree-shaking | Destekler (kullanılmayan kod atılır) | Desteklemez |
| Top-level await | Destekler | Desteklemez |
| Tarayıcı desteği | Evet (`<script type="module">`) | Hayır (bundler gerekir) |
| Node.js | `.mjs` veya `"type": "module"` | Varsayılan |

**Tavsiye:** Yeni projelerde her zaman ES Modules kullan. CommonJS'i sadece eski Node.js projelerinde göreceksin.
:::

## Map, Set, WeakMap, WeakSet

:::concept[Map ve Set (İng: Map, Set)]
Map, key-value çiftleri saklayan koleksiyondur (herhangi bir tip key olabilir). Set, benzersiz (unique) değerler saklayan koleksiyondur.

**Türkçe karşılığı:** Eşleşme / Küme
**Ne işe yarar:** Map - Object'in aksine herhangi bir tipi key olarak kullanır. Set - otomatik benzersizlik sağlar
**Gerçek hayat benzetmesi:** Map = telefon rehberi (isim-numara eşleşmesi). Set = davetli listesi (aynı kişi iki kez eklenemez)
:::

:::code[javascript]{title="Map"}
const map = new Map();

// Herhangi bir tip key olabilir (Object'te sadece string/symbol)
map.set('name', 'Ali');
map.set(42, 'sayı key');
map.set(true, 'boolean key');

const objKey = { id: 1 };
map.set(objKey, 'obje key bile olabilir!');

map.get('name');     // 'Ali'
map.has(42);         // true
map.size;            // 4
map.delete(true);

// Iterasyon
for (const [key, value] of map) {
  console.log(`${key}: ${value}`);
}

// Object'ten Map'e
const obj = { a: 1, b: 2 };
const fromObj = new Map(Object.entries(obj));

// Map'ten Object'e
const backToObj = Object.fromEntries(map);
:::

:::code[javascript]{title="Set"}
const set = new Set([1, 2, 3, 3, 3]);
console.log(set.size); // 3 (tekrarlar otomatik silindi)

set.add(4);
set.has(2);    // true
set.delete(1);

// En yaygın kullanım: array'den tekrarları kaldır
const arr = [1, 2, 2, 3, 3, 3, 4];
const unique = [...new Set(arr)]; // [1, 2, 3, 4]

// İki array'in kesişimi
const a = new Set([1, 2, 3, 4]);
const b = new Set([3, 4, 5, 6]);
const intersection = [...a].filter(x => b.has(x)); // [3, 4]
:::

:::code[javascript]{title="WeakMap ve WeakSet"}
// WeakMap: key'ler sadece object olabilir, garbage collection'ı engellemez
const cache = new WeakMap();

function processElement(element) {
  if (cache.has(element)) {
    return cache.get(element); // Cached sonuç
  }
  const result = /* ağır hesaplama */ element.id * 2;
  cache.set(element, result);
  return result;
}
// element DOM'dan kaldırılınca WeakMap'ten de otomatik silinir
// Memory leak önler!

// WeakSet: aynı mantık, sadece varlık kontrolü
const visited = new WeakSet();

function trackVisit(user) {
  if (visited.has(user)) {
    console.log('Tekrar ziyaret');
  } else {
    visited.add(user);
    console.log('Ilk ziyaret');
  }
}
// user objesi başka yerde referanssız kalınca WeakSet'ten de silinir
:::

:::comparison
| Özellik | Map vs Object | Set vs Array |
|---------|--------------|--------------|
| Key tipi | Map: herhangi tip / Object: string/symbol | - |
| Sıralama | Map: ekleme sırası garantili | Set: ekleme sırası garantili |
| Size | `map.size` | `set.size` |
| Performans | Map: sık ekleme/silmede daha hızlı | Set: `has()` O(1), Array `includes()` O(n) |
| Iterasyon | Map: doğrudan iterable | Set: doğrudan iterable |
| Kullanım | Config, cache, metadata | Benzersiz değerler, membership testi |
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: Destructuring ve Spread ile API Verisi Isleme (Kolay)

Bir API response'unu destructuring ile parcala ve spread operator ile yeni objeler oluştur.

```javascript
// Simule edilmis API response
const apiResponse = {
  status: 200,
  data: {
    user: {
      id: 42,
      profile: {
        firstName: "Ahmet",
        lastName: "Yilmaz",
        contact: {
          email: "ahmet@example.com",
          phone: "+90-555-1234567",
          address: {
            city: "Istanbul",
            district: "Kadikoy",
            country: "Turkey",
          },
        },
      },
      settings: {
        theme: "dark",
        language: "tr",
        notifications: { email: true, push: false, sms: true },
      },
    },
    posts: [
      { id: 1, title: "JavaScript Temeller", likes: 42 },
      { id: 2, title: "React Hooks", likes: 128 },
      { id: 3, title: "Node.js Guide", likes: 95 },
    ],
  },
};

// GOREV 1: Nested destructuring ile su degiskenleri cikar:
// firstName, email, city, theme
const {
  // TODO: Implement
} = apiResponse;
console.log(firstName, email, city, theme);
// Beklenen: "Ahmet" "ahmet@example.com" "Istanbul" "dark"

// GOREV 2: Posts'tan en cok like alan yaziyi bul (destructuring + reduce)
const mostLiked = apiResponse.data.posts.reduce(
  // TODO: Implement
);
console.log(mostLiked); // { id: 2, title: "React Hooks", likes: 128 }

// GOREV 3: Spread ile user'in settings'ini guncelle (immutable)
const updatedSettings = {
  // TODO: Mevcut settings'i spread et, theme'i "light" yap,
  // notifications icinde push'u true yap
};
console.log(updatedSettings);
// Beklenen: { theme: "light", language: "tr", notifications: { email: true, push: true, sms: true } }
```

**Beklenen Sonuc:** Nested destructuring ile derin veriye tek satirda erisebilmeli. Spread operator ile orijinal obje degismeden yeni versiyonu oluşturabilmeli.
**Ipucu:** Nested destructuring: `const { data: { user: { profile: { firstName } } } } = apiResponse`

---

### Alistirma 2: Async/Await ile Paralel API Cagrilari (Orta)

async/await, Promise.all ve Promise.allSettled kullanarak birden fazla API'den veri cek ve performans farklarini olc.

```javascript
// JSONPlaceholder API endpoint'leri
const endpoints = {
  users: "https://jsonplaceholder.typicode.com/users",
  posts: "https://jsonplaceholder.typicode.com/posts?_limit=5",
  todos: "https://jsonplaceholder.typicode.com/todos?_limit=5",
};

// GOREV 1: Sirayla (sequential) veri cek — suresi olc
async function fetchSequential() {
  console.time("Sequential");
  // TODO: Her endpoint'i sirayla fetch et (await ile)
  // Her birinin sonucunu bir objeye kaydet
  console.timeEnd("Sequential");
  // return { users, posts, todos }
}

// GOREV 2: Paralel (concurrent) veri cek — suresi olc
async function fetchParallel() {
  console.time("Parallel");
  // TODO: Promise.all ile 3 fetch'i ayni anda baslat
  console.timeEnd("Parallel");
  // return { users, posts, todos }
}

// GOREV 3: Hata toleransli paralel fetch
async function fetchWithFallback() {
  const urls = [
    "https://jsonplaceholder.typicode.com/users/1",
    "https://invalid-url.example.com/fail",  // Bu hata verecek
    "https://jsonplaceholder.typicode.com/posts/1",
  ];

  // TODO: Promise.allSettled kullan
  // Basarili olanlarin verisini, basarisiz olanlarin hatasini goster
  // Promise.all kullansaydin ne olurdu? (hepsi reject olurdu!)
}

// Calistir ve sureleri karsilastir:
fetchSequential().then((data) => console.log("Sequential sonuc:", Object.keys(data)));
fetchParallel().then((data) => console.log("Parallel sonuc:", Object.keys(data)));
fetchWithFallback();
```

**Beklenen Sonuc:** Paralel fetch, sirayl fetch'ten en az 2-3x daha hizli olmali. `Promise.allSettled` ile basarisiz istekler digerleri engellemeden raporlanmali.
**Ipucu:** `Promise.allSettled` her zaman resolve olur ve her sonuc `{ status: 'fulfilled', value }` veya `{ status: 'rejected', reason }` formatindadir.

---

### Alistirma 3: Set ve Map ile Veri Analizi (Zor)

Set ve Map yapilarini kullanarak iki veri seti arasinda kume islemleri yap ve performans karsilastirmasi yap.

```javascript
// Iki farkli kaynak sistemi
const systemA_users = ["ahmet@x.com", "ayse@x.com", "mehmet@x.com", "fatma@x.com", "ali@x.com"];
const systemB_users = ["ayse@x.com", "fatma@x.com", "zeynep@x.com", "hasan@x.com", "ali@x.com"];

// GOREV 1: Set ile kume islemleri
function setOperations(arrA, arrB) {
  const setA = new Set(arrA);
  const setB = new Set(arrB);

  // TODO: Union — her iki sistemde olan tum kullanicilar
  const union = // ...

  // TODO: Intersection — her iki sistemde ortak kullanicilar
  const intersection = // ...

  // TODO: Difference (A - B) — sadece A'da olan kullanicilar
  const onlyInA = // ...

  // TODO: Symmetric Difference — sadece birinde olan kullanicilar
  const symmetricDiff = // ...

  return { union, intersection, onlyInA, symmetricDiff };
}

const result = setOperations(systemA_users, systemB_users);
console.log("Union:", result.union);               // 7 eleman
console.log("Intersection:", result.intersection); // 3 eleman (ayse, fatma, ali)
console.log("Only in A:", result.onlyInA);         // 2 eleman (ahmet, mehmet)
console.log("Symmetric Diff:", result.symmetricDiff); // 4 eleman

// GOREV 2: Map ile frequency counter
const words = "bir iki bir uc bir iki dort bir iki bir".split(" ");

function wordFrequency(words) {
  // TODO: Map kullanarak her kelimenin frekansini hesapla
  // TODO: En cok tekrar eden kelimeyi bul
  // TODO: Frekansi 2'den fazla olanlari filtrele
}

const freq = wordFrequency(words);
console.log(freq);
// Beklenen: Map { "bir" => 5, "iki" => 3, "uc" => 1, "dort" => 1 }

// GOREV 3: Performans karsilastirmasi
// 100.000 elemanli array'de eleman arama:
// Array.includes() vs Set.has() suresini olc
const bigArray = Array.from({ length: 100_000 }, (_, i) => `item_${i}`);
const bigSet = new Set(bigArray);
const searchItem = "item_99999";

console.time("Array.includes");
bigArray.includes(searchItem);
console.timeEnd("Array.includes");

console.time("Set.has");
bigSet.has(searchItem);
console.timeEnd("Set.has");
// Hangisi daha hizli? Neden?
```

**Beklenen Sonuc:** Kume islemleri dogru sonuclari dondurmeli. Set.has() Array.includes()'tan cok daha hizli olmali (O(1) vs O(n)). Map ile frekans analizi tek geciste yapilmali.
**Ipucu:** Set'te union icin spread operator kullanabilirsin: `new Set([...setA, ...setB])`. Intersection icin filter ve has kombinasyonu.
:::

:::knowledge-check
type: multiple_choice
question: "const { a: x = 5 } = { a: undefined }; x'in değeri nedir?"
options:
  - "undefined"
  - "5"
  - "{ a: undefined }"
  - "ReferenceError"
correct: 1
explanation: "Destructuring'de default value, değer undefined olduğunda devreye girer. a: x = 5 ifadesi a'yı x olarak rename eder ve default 5 verir. a'nın değeri undefined olduğu için x = 5 olur."
:::

:::knowledge-check
type: multiple_choice
question: "Promise.all([p1, p2, p3]) ifadesinde p2 reject olursa ne olur?"
options:
  - "Sadece p2 hata döner, p1 ve p3 devam eder"
  - "Tüm Promise.all reject olur, ilk reject edilen error ile"
  - "undefined döner"
  - "p1 ve p3'ün sonuçlarını döner, p2'yi atlar"
correct: 1
explanation: "Promise.all fail-fast davranışı gösterir. Herhangi biri reject olursa, tüm Promise.all o hata ile reject olur. Partial failure istiyorsan Promise.allSettled kullan."
:::

:::knowledge-check
type: multiple_choice
question: "const a = 0 ?? 42; ve const b = 0 || 42; değerleri nedir?"
options:
  - "a = 42, b = 42"
  - "a = 0, b = 0"
  - "a = 0, b = 42"
  - "a = 42, b = 0"
correct: 2
explanation: "?? (nullish coalescing) sadece null ve undefined'da sağ tarafı kullanır. 0 nullish değildir, bu yüzden a = 0. || (logical OR) ise tüm falsy değerlerde (0, '', false, null, undefined) sağ tarafı kullanır. 0 falsy olduğu için b = 42."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6

### Prompt Örnekleri

**1. Konuyu Derinlemesine Anla:**
> "JavaScript'te Promise.all, Promise.race, Promise.allSettled ve Promise.any arasindaki farklari gercek dunya senaryolariyla acikla. Bir e-ticaret uygulamasinda hangi durumda hangisini kullanmaliyim? Her birinin hata yonetimi nasil farklilik gosteriyor?"

*Neden:* Async pattern'leri dogru secmek, production'da resilient ve performansli kod yazmanin temelidir

**2. Pratik Uygulama:**
> "Bir API client modulu yaz. fetch ile GET, POST, PUT, DELETE method'larini desteklesin. async/await ve try/catch ile hata yonetimi, timeout desteği (Promise.race ile), response.ok kontrolu ve JSON parse icersin. ES Modules ile export et."

*Follow-up:* "Bu API client'a retry logic (exponential backoff) ve request interceptor desteği ekle."

**3. Mukemmellik Icin:**
> "WeakMap ve WeakRef'in garbage collection ile iliskisini acikla. Bir DOM element cache mekanizmasi tasarla: element DOM'dan kaldirildiginda cache'ten de otomatik silinsin. Normal Map ile WeakMap kullanmanin bellek etkisini karsilastir."

### Pair Programming Ipucu
Async kod yazarken AI'a kodunu yapistir: "Bu async fonksiyondaki hata yonetimini incele. Hangi hatalari yakalamam gerekiyor? Promise.all mi yoksa Promise.allSettled mi kullanmaliyim? fetch'in 404'te reject olmadigini handle ediyor muyum?"
:::

:::interview
## Mulakat Sorulari

**Soru 1: Promise, async/await ve callback arasindaki farklar nelerdir?**
- **Junior cevabi:** Callback eski yontem, Promise zincirleme yapar, async/await daha okunaklı.
- **Senior cevabi:** Callback'ler callback hell ve inversion of control sorunlari yaratir. Promise'ler microtask queue'da calisir, zincirleme ve hata yonetimi (catch) saglar. async/await syntactic sugar'dir ama try/catch ile hata yonetimi, paralel çalıştırma (Promise.all vs Promise.allSettled), ve error propagation acisindan onemli farklari vardir. Promise.all fail-fast yapar, allSettled tum sonuclari bekler. Unhandled rejection'lar Node.js'te process'i sonlandirir.

**Soru 2: Spread operator ve rest parameter arasindaki fark nedir?**
- **Junior cevabi:** Uc nokta (...) spread acmak, rest toplamak icindir.
- **Senior cevabi:** Spread ve rest ayni syntax'i kullanir ama farkli context'lerde farkli is yapar. Spread, iterable'lari acar (shallow copy oluşturur, deep clone degil). Rest ise fonksiyon parametrelerinde veya destructuring'de kalan elemanlari toplar. Object spread ile Object.assign benzerdir ama spread daha okunaklidir. Performance-critical kodda spread'in yeni nesne oluşturma maliyetine dikkat edilmelidir.
:::

:::exercise
### Alıştırma 4: Promise.all, race, allSettled Karşılaştırması

**Görev:** `Promise.all`, `Promise.race` ve `Promise.allSettled` arasındaki farkları gösteren senaryolar yaz.

**Başlangıç kodu:**
```javascript
// API simulasyonlari
function fetchUser(id) {
  return new Promise((resolve, reject) => {
    const delay = Math.random() * 1000;
    setTimeout(() => {
      if (id === 3) reject(new Error(`User ${id} not found`));
      else resolve({ id, name: `User_${id}`, delay: Math.round(delay) });
    }, delay);
  });
}

async function testPromiseAll() {
  console.log("=== Promise.all (hepsi basarili olmali) ===");
  try {
    const results = await Promise.all([fetchUser(1), fetchUser(2)]);
    results.forEach(u => console.log(`  ${u.name} (${u.delay}ms)`));
  } catch (e) {
    console.log(`  Hata: ${e.message}`);
  }

  console.log("\n=== Promise.all (biri basarisiz) ===");
  // TODO: fetchUser(1), fetchUser(3), fetchUser(2) ile test et
  // Bir tanesi reject olunca hepsi basarisiz olur
}

async function testPromiseRace() {
  console.log("\n=== Promise.race (ilk tamamlanan kazanir) ===");
  // TODO: 3 fetch baslat, ilk tamamlanani yazdir
}

async function testPromiseAllSettled() {
  console.log("\n=== Promise.allSettled (hepsini bekle, basarisiz olsa bile) ===");
  // TODO: fetchUser(1), fetchUser(3), fetchUser(2) ile test et
  // Her birinin durumunu (fulfilled/rejected) goster
}

// Bonus: Kendi Promise.allSettled implementasyonun
function myAllSettled(promises) {
  // TODO: Her promise'i catch ile sarmalayarak hepsinin sonucunu topla
}

testPromiseAll()
  .then(testPromiseRace)
  .then(testPromiseAllSettled);
```

**Beklenen çıktı:**
```
=== Promise.all (hepsi basarili olmali) ===
  User_1 (234ms)
  User_2 (567ms)

=== Promise.all (biri basarisiz) ===
  Hata: User 3 not found

=== Promise.race (ilk tamamlanan kazanir) ===
  Kazanan: User_1 (123ms)

=== Promise.allSettled (hepsini bekle, basarisiz olsa bile) ===
  User_1: fulfilled
  User_3: rejected - User 3 not found
  User_2: fulfilled
```

**İpucu:** `Promise.allSettled` ES2020 ile geldi. Sonuçlar `{status: "fulfilled", value}` veya `{status: "rejected", reason}` formatında.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: Async Iterator ile Sayfalı API

**Görev:** `async function*` (async generator) kullanarak sayfalı API verilerini otomatik çeken bir iterator yaz.

**Başlangıç kodu:**
```javascript
// Sayfalı API simulasyonu
function fetchPage(page, pageSize = 3) {
  const totalItems = 10;
  const start = (page - 1) * pageSize;
  const items = [];
  for (let i = start; i < Math.min(start + pageSize, totalItems); i++) {
    items.push({ id: i + 1, title: `Item ${i + 1}` });
  }
  return new Promise((resolve) =>
    setTimeout(() => resolve({
      data: items,
      page,
      totalPages: Math.ceil(totalItems / pageSize),
      hasMore: page * pageSize < totalItems,
    }), 100)
  );
}

async function* paginatedFetch(fetchFn, pageSize = 3) {
  // TODO:
  // 1. page = 1'den basla
  // 2. Her sayfayi fetch et
  // 3. Sayfa verilerini yield et
  // 4. hasMore false olana kadar devam et
}

// Test: for await...of ile kullan
async function main() {
  console.log("=== Sayfali API Verisi ===");
  let totalItems = 0;

  for await (const page of paginatedFetch(fetchPage, 3)) {
    console.log(`Sayfa ${page.page}/${page.totalPages}:`);
    page.data.forEach((item) => {
      console.log(`  - ${item.title}`);
      totalItems++;
    });
  }

  console.log(`\nToplam: ${totalItems} item`);
}

main();
```

**Beklenen çıktı:**
```
=== Sayfali API Verisi ===
Sayfa 1/4:
  - Item 1
  - Item 2
  - Item 3
Sayfa 2/4:
  - Item 4
  - Item 5
  - Item 6
Sayfa 3/4:
  - Item 7
  - Item 8
  - Item 9
Sayfa 4/4:
  - Item 10

Toplam: 10 item
```

**İpucu:** `async function*` ile async generator tanımlanır. `yield` ile her sayfayı dışarı ver. `for await...of` ile consume et.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: Map, Set ve WeakMap Kullanım Senaryoları

**Görev:** Map, Set ve WeakMap'in gerçek kullanım senaryolarını gösteren örnekler yaz.

**Başlangıç kodu:**
```javascript
// Senaryo 1: Map ile object key kullanma (Object ile yapilamaz)
function testMapWithObjectKeys() {
  const userPermissions = new Map();
  const user1 = { id: 1, name: "Ahmet" };
  const user2 = { id: 2, name: "Ayse" };

  // TODO: Her user objesini key olarak kullanarak permission ata
  // user1 -> ["read", "write"]
  // user2 -> ["read"]

  console.log("=== Map ile Object Key ===");
  console.log(`${user1.name}: ${userPermissions.get(user1)}`);
  console.log(`${user2.name}: ${userPermissions.get(user2)}`);
}

// Senaryo 2: Set ile benzersiz deger toplama
function testSetOperations() {
  const setA = new Set([1, 2, 3, 4, 5]);
  const setB = new Set([4, 5, 6, 7, 8]);

  // TODO: union, intersection, difference islemleri yaz
  const union = new Set([...setA, ...setB]);
  const intersection = new Set(/* TODO */);
  const difference = new Set(/* TODO */);

  console.log("\n=== Set Islemleri ===");
  console.log(`A: ${[...setA]}`);
  console.log(`B: ${[...setB]}`);
  console.log(`Union: ${[...union]}`);
  console.log(`Intersection: ${[...intersection]}`);
  console.log(`Difference (A-B): ${[...difference]}`);
}

// Senaryo 3: WeakMap ile metadata cache
function testWeakMapCache() {
  const cache = new WeakMap();

  function processUser(user) {
    if (cache.has(user)) {
      console.log(`  Cache hit: ${user.name}`);
      return cache.get(user);
    }
    const result = { ...user, processed: true, timestamp: Date.now() };
    cache.set(user, result);
    console.log(`  Processed: ${user.name}`);
    return result;
  }

  console.log("\n=== WeakMap Cache ===");
  let user = { id: 1, name: "Ahmet" };
  processUser(user);  // miss
  processUser(user);  // hit
  // user = null; -> garbage collection sonrasi cache'ten otomatik silinir
}

testMapWithObjectKeys();
testSetOperations();
testWeakMapCache();
```

**Beklenen çıktı:**
```
=== Map ile Object Key ===
Ahmet: read,write
Ayse: read

=== Set Islemleri ===
A: 1,2,3,4,5
B: 4,5,6,7,8
Union: 1,2,3,4,5,6,7,8
Intersection: 4,5
Difference (A-B): 1,2,3

=== WeakMap Cache ===
  Processed: Ahmet
  Cache hit: Ahmet
```

**İpucu:** Intersection: `[...setA].filter(x => setB.has(x))`. Difference: `[...setA].filter(x => !setB.has(x))`.

**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 7: ES Module Sistemi Simülasyonu

**Görev:** ES module sisteminin import/export mekanizmasını simüle eden bir mini module loader yaz.

**Başlangıç kodu:**
```javascript
class ModuleLoader {
  constructor() {
    this.modules = new Map();
    this.cache = new Map();
  }

  define(name, dependencies, factory) {
    // TODO: Modulu kaydet
    // name: modul adi
    // dependencies: bagimli modul adlari listesi
    // factory: modul fonksiyonu (dependency exports'larini alir)
    this.modules.set(name, { dependencies, factory });
  }

  require(name) {
    // TODO:
    // 1. Cache'te varsa dondur
    // 2. Modulu bul
    // 3. Dependency'leri recursive olarak resolve et
    // 4. Factory'yi cagir ve sonucu cache'le
    if (this.cache.has(name)) return this.cache.get(name);

    const mod = this.modules.get(name);
    if (!mod) throw new Error(`Module not found: ${name}`);

    const deps = mod.dependencies.map((dep) => this.require(dep));
    const exports = mod.factory(...deps);
    this.cache.set(name, exports);
    return exports;
  }
}

// Test
const loader = new ModuleLoader();

// Modul tanimlari
loader.define("utils", [], () => ({
  capitalize: (s) => s.charAt(0).toUpperCase() + s.slice(1),
  sum: (arr) => arr.reduce((a, b) => a + b, 0),
}));

loader.define("validator", ["utils"], (utils) => ({
  isValidName: (name) => name.length >= 2 && utils.capitalize(name) === name,
  isValidAge: (age) => age > 0 && age < 150,
}));

loader.define("userService", ["utils", "validator"], (utils, validator) => ({
  createUser: (name, age) => {
    if (!validator.isValidAge(age)) throw new Error("Invalid age");
    return {
      name: utils.capitalize(name),
      age,
      displayName: `${utils.capitalize(name)} (${age})`,
    };
  },
}));

// Kullanim
const userService = loader.require("userService");
const user = userService.createUser("ahmet", 25);
console.log(`User: ${user.displayName}`);

const utils = loader.require("utils");
console.log(`Sum: ${utils.sum([1, 2, 3, 4, 5])}`);
console.log(`Capitalize: ${utils.capitalize("javascript")}`);
```

**Beklenen çıktı:**
```
User: Ahmet (25)
Sum: 15
Capitalize: Javascript
```

**İpucu:** Circular dependency'lere dikkat. Cache kullanarak aynı modülün birden fazla kez yüklenmesini önle.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Array Method Chaining ile Veri Analizi

**Görev:** Karmaşık bir veri seti üzerinde `filter`, `map`, `reduce`, `sort`, `flatMap` ve `groupBy` kullanarak analiz yap.

**Başlangıç kodu:**
```javascript
const orders = [
  { id: 1, customer: "Ahmet", items: [{ name: "Laptop", price: 15000, qty: 1 }, { name: "Mouse", price: 200, qty: 2 }], date: "2026-01-15" },
  { id: 2, customer: "Ayse", items: [{ name: "Phone", price: 8000, qty: 1 }], date: "2026-01-20" },
  { id: 3, customer: "Ahmet", items: [{ name: "Keyboard", price: 500, qty: 1 }, { name: "Monitor", price: 3000, qty: 1 }], date: "2026-02-10" },
  { id: 4, customer: "Mehmet", items: [{ name: "Tablet", price: 5000, qty: 2 }], date: "2026-02-15" },
  { id: 5, customer: "Ayse", items: [{ name: "Headphones", price: 1000, qty: 1 }, { name: "Cable", price: 50, qty: 3 }], date: "2026-03-01" },
];

// GOREV 1: Her siparişin toplam tutarini hesapla
const orderTotals = orders.map((order) => ({
  // TODO: id, customer, total (items icindeki price * qty toplami)
}));
console.log("=== Siparis Toplamlari ===");
orderTotals.forEach((o) => console.log(`  #${o.id} ${o.customer}: ${o.total} TL`));

// GOREV 2: Musteriye gore grupla ve toplam harcamayi hesapla
const customerSpending = orders.reduce((acc, order) => {
  // TODO: { customer: totalSpending } objesi olustur
}, {});
console.log("\n=== Musteri Harcamalari ===");
Object.entries(customerSpending)
  .sort(([, a], [, b]) => b - a)
  .forEach(([customer, total]) => console.log(`  ${customer}: ${total} TL`));

// GOREV 3: Tum urunleri flatMap ile tek listeye cevir, fiyata gore sirala
const allProducts = orders.flatMap((order) =>
  // TODO: Her item'i { name, price, qty, customer, orderId } formatina cevir
  []
);
console.log("\n=== En Pahali 3 Urun ===");
allProducts
  .sort((a, b) => b.price - a.price)
  .slice(0, 3)
  .forEach((p) => console.log(`  ${p.name}: ${p.price} TL (${p.customer})`));

// GOREV 4: Aylik siparis sayisi
const monthlyOrders = orders.reduce((acc, order) => {
  // TODO: { "2026-01": 2, "2026-02": 2, ... }
}, {});
console.log("\n=== Aylik Siparis Sayisi ===");
Object.entries(monthlyOrders).forEach(([month, count]) =>
  console.log(`  ${month}: ${count} siparis`)
);
```

**Beklenen çıktı:**
```
=== Siparis Toplamlari ===
  #1 Ahmet: 15400 TL
  #2 Ayse: 8000 TL
  #3 Ahmet: 3500 TL
  #4 Mehmet: 10000 TL
  #5 Ayse: 1150 TL

=== Musteri Harcamalari ===
  Ahmet: 18900 TL
  Mehmet: 10000 TL
  Ayse: 9150 TL

=== En Pahali 3 Urun ===
  Laptop: 15000 TL (Ahmet)
  Phone: 8000 TL (Ayse)
  Tablet: 5000 TL (Mehmet)

=== Aylik Siparis Sayisi ===
  2026-01: 2 siparis
  2026-02: 2 siparis
  2026-03: 1 siparis
```

**İpucu:** `flatMap` nested array'leri tek seviyeye indirir. `reduce` ile gruplama yaparken accumulator'ü `{}` olarak başlat.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: Proxy ile Reactive Data Binding

**Görev:** ES6 Proxy kullanarak basit bir reactive veri bağlama sistemi yaz. Veri değiştiğinde otomatik UI güncellemesi tetiklensin.

**Başlangıç kodu:**
```javascript
function reactive(target, onChange) {
  // TODO: Proxy ile target objesini sarmala
  // Her set isleminde onChange callback'ini cagir
  // Nested objeler icin de proxy olustur (deep reactivity)
  return new Proxy(target, {
    get(obj, prop) {
      const value = obj[prop];
      // TODO: Eger value obje ise, onu da reactive yap
      return value;
    },
    set(obj, prop, value) {
      const oldValue = obj[prop];
      obj[prop] = value;
      // TODO: Degisiklik varsa onChange cagir
      return true;
    },
  });
}

// Test
const state = reactive(
  {
    user: { name: "Ahmet", age: 25 },
    count: 0,
    items: [],
  },
  (path, oldVal, newVal) => {
    console.log(`  Degisiklik: ${path} = ${JSON.stringify(oldVal)} -> ${JSON.stringify(newVal)}`);
  }
);

console.log("=== Reactive State ===");
state.count = 1;
state.count = 2;
state.user.name = "Mehmet";
state.user.age = 30;
state.items.push("item1");
```

**Beklenen çıktı:**
```
=== Reactive State ===
  Degisiklik: count = 0 -> 1
  Degisiklik: count = 1 -> 2
  Degisiklik: user.name = "Ahmet" -> "Mehmet"
  Degisiklik: user.age = 25 -> 30
  Degisiklik: items.0 = undefined -> "item1"
```

**İpucu:** Nested reactivity için `get` trap'inde obje dönerken onu da `new Proxy()` ile sar. Path bilgisini parent'tan child'a aktarmak için closure kullan.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 10: Error Handling Best Practices

**Görev:** Custom error sınıfları ve kapsamlı hata yönetim stratejileri gösteren bir modül yaz.

**Başlangıç kodu:**
```javascript
// Custom error siniflari
class AppError extends Error {
  constructor(message, code, details = {}) {
    super(message);
    this.name = "AppError";
    this.code = code;
    this.details = details;
    this.timestamp = new Date().toISOString();
  }
}

class ValidationError extends AppError {
  constructor(field, message) {
    super(message, "VALIDATION_ERROR", { field });
    this.name = "ValidationError";
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} not found: ${id}`, "NOT_FOUND", { resource, id });
    this.name = "NotFoundError";
  }
}

// TODO: AuthenticationError ve RateLimitError siniflarini yaz

// Error handler
function handleError(error) {
  // TODO: Hata tipine gore uygun response olustur
  // ValidationError -> 400
  // NotFoundError -> 404
  // AuthenticationError -> 401
  // RateLimitError -> 429
  // Bilinmeyen -> 500
  const response = {
    status: 500,
    error: { code: "UNKNOWN", message: "Internal server error" },
  };

  if (error instanceof ValidationError) {
    response.status = 400;
    response.error = { code: error.code, message: error.message, field: error.details.field };
  }
  // TODO: Diger hata tiplerini handle et

  return response;
}

// Test
const errors = [
  new ValidationError("email", "Gecersiz email formati"),
  new NotFoundError("User", 42),
  new AppError("Sunucu hatasi", "SERVER_ERROR"),
];

errors.forEach((err) => {
  const response = handleError(err);
  console.log(`${err.name}: ${response.status} -> ${JSON.stringify(response.error)}`);
});

// Async error handling pattern
async function safeFetch(url) {
  try {
    // Simulasyon
    if (url.includes("404")) throw new NotFoundError("Page", url);
    if (url.includes("auth")) throw new AppError("Unauthorized", "AUTH_ERROR");
    return { data: "success" };
  } catch (error) {
    const response = handleError(error);
    console.log(`safeFetch error: ${response.status}`);
    return null;
  }
}

safeFetch("/api/users/404");
safeFetch("/api/auth/login");
```

**Beklenen çıktı:**
```
ValidationError: 400 -> {"code":"VALIDATION_ERROR","message":"Gecersiz email formati","field":"email"}
NotFoundError: 404 -> {"code":"NOT_FOUND","message":"User not found: 42"}
AppError: 500 -> {"code":"UNKNOWN","message":"Internal server error"}
safeFetch error: 404
safeFetch error: 500
```

**İpucu:** `instanceof` ile hata tipini kontrol et. Custom error'larda `this.name` ayarlamayı unutma.

**Zorluk:** Zor
:::

:::exercise
### Alıştırma 11: Observable Pattern ile Reactive Store

**Görev:** ES6+ özellikleri kullanarak basit bir reactive state management store yaz.

**Başlangıç kodu:**
```javascript
class Store {
  #state;
  #listeners;

  constructor(initialState) {
    this.#state = structuredClone(initialState);
    this.#listeners = new Map();
  }

  getState() {
    return structuredClone(this.#state);
  }

  setState(updater) {
    const oldState = this.#state;
    this.#state = typeof updater === "function"
      ? { ...this.#state, ...updater(this.#state) }
      : { ...this.#state, ...updater };
    this.#notify(oldState, this.#state);
  }

  subscribe(key, callback) {
    if (!this.#listeners.has(key)) {
      this.#listeners.set(key, new Set());
    }
    this.#listeners.get(key).add(callback);
    return () => this.#listeners.get(key)?.delete(callback);
  }

  #notify(oldState, newState) {
    for (const [key, callbacks] of this.#listeners) {
      if (oldState[key] !== newState[key]) {
        callbacks.forEach((cb) => cb(newState[key], oldState[key]));
      }
    }
  }
}

// Test
const store = new Store({ count: 0, user: null, theme: "dark" });

const unsub = store.subscribe("count", (newVal, oldVal) => {
  console.log(`  count: ${oldVal} -> ${newVal}`);
});

store.subscribe("user", (newVal) => {
  console.log(`  user: ${newVal?.name ?? "null"}`);
});

console.log("=== State Degisiklikleri ===");
store.setState({ count: 1 });
store.setState((s) => ({ count: s.count + 1 }));
store.setState({ user: { name: "Ahmet" } });
store.setState({ theme: "light" }); // theme listener yok

unsub(); // count listener'i kaldir
store.setState({ count: 99 }); // Bildirim gelmemeli
console.log("Final state:", store.getState());
```

**Beklenen çıktı:**
```
=== State Degisiklikleri ===
  count: 0 -> 1
  count: 1 -> 2
  user: Ahmet
Final state: { count: 99, user: { name: 'Ahmet' }, theme: 'light' }
```

**İpucu:** `#` ile private field tanımla. `structuredClone()` deep copy yapar. `subscribe()` unsubscribe fonksiyonu döner.

**Zorluk:** Orta
:::

:::exercise
### Alıştırma 12: Tagged Template Literal ile SQL Builder

**Görev:** Tagged template literal kullanarak SQL injection'a karşı güvenli bir query builder yaz.

**Başlangıç kodu:**
```javascript
function sql(strings, ...values) {
  // TODO:
  // 1. String parcalarini ve degerleri birlestir
  // 2. Degerleri parametrize et ($1, $2, ...)
  // 3. SQL injection'a karsi guvenli query olustur
  const params = [];
  let query = "";

  strings.forEach((str, i) => {
    query += str;
    if (i < values.length) {
      params.push(values[i]);
      query += `$${params.length}`;
    }
  });

  return { query: query.trim(), params };
}

// Test: Guvenli sorgular
const userId = 42;
const role = "admin";
const minAge = 18;

const q1 = sql`SELECT * FROM users WHERE id = ${userId}`;
console.log(q1);
// { query: "SELECT * FROM users WHERE id = $1", params: [42] }

const q2 = sql`SELECT * FROM users WHERE role = ${role} AND age > ${minAge}`;
console.log(q2);
// { query: "SELECT * FROM users WHERE role = $1 AND age > $2", params: ["admin", 18] }

// SQL Injection denemesi - guvenli!
const malicious = "'; DROP TABLE users; --";
const q3 = sql`SELECT * FROM users WHERE name = ${malicious}`;
console.log(q3);
// Deger parametrize edildigi icin SQL injection calismaz
console.log("SQL Injection engellendi!");
```

**Beklenen çıktı:**
```
{ query: 'SELECT * FROM users WHERE id = $1', params: [ 42 ] }
{ query: 'SELECT * FROM users WHERE role = $1 AND age > $2', params: [ 'admin', 18 ] }
{ query: "SELECT * FROM users WHERE name = $1", params: ["'; DROP TABLE users; --"] }
SQL Injection engellendi!
```

**İpucu:** Tagged template literal'da `strings` array'i sabit metin parçalarını, `values` interpolated değerleri içerir. Değerleri query string'e yerleştirmek yerine parametre olarak ayır.

**Zorluk:** Orta
:::

:::must-note
- Destructuring: `const { name: n = 'default' } = obj` - rename + default birlikte kullanılabilir
- Spread yayar (`[...arr]`), Rest toplar (`function(...args)`) - aynı syntax, farklı amaç
- `?.` (optional chaining): null/undefined'da hata yerine undefined döner
- `??` sadece null/undefined, `||` tüm falsy (0, '', false) değerlerde fallback kullanır
- `map` yeni array döner, `forEach` undefined döner - dönüşüm istiyorsan `map`
- `reduce` akümülatörün initial value'sunu (ikinci parametre) MUTLAKA ver
- `find` tek eleman (veya undefined), `filter` array döner
- `Promise.all` = fail-fast (biri fail = hepsi fail), `Promise.allSettled` = hepsini bekle
- `fetch` 404/500'de reject OLMAZ, `response.ok` kontrol et
- ES Modules statik (tree-shaking destekler), CommonJS dinamik (runtime)
- `Map` herhangi tip key alır (Object sadece string/symbol), `Set` otomatik benzersizlik sağlar
- `WeakMap/WeakSet` garbage collection'ı engellemez, memory leak önler
- `arr.at(-1)` son eleman, `arr[-1]` undefined döner - `at()` kullan
- async/await her zaman try/catch ile sar, hataları yukarıya ilet (`throw error`)
:::

:::senior-learns
Bir Senior Developer veya CTO, modern JavaScript özelliklerini öğrenirken şu yaklaşımı benimser:

1. **TC39 proposal sürecini takip eder** - Yeni özelliklerin Stage 0'dan Stage 4'e (standart) nasıl ilerlediğini bilir. github.com/tc39/proposals reposunu takip eder. Bir özellik Stage 3'e geldiğinde production'da kullanmaya başlar (Babel/TypeScript desteği genelde burada gelir).

2. **Engine seviyesinde anlar** - V8 (Chrome/Node.js), SpiderMonkey (Firefox) motorlarının async/await'i nasıl optimize ettiğini bilir. Microtask queue, event loop, call stack ilişkisini derinlemesine anlar. `queueMicrotask` vs `setTimeout` farkını pratik örneklerle deneyimler.

3. **Performans implikasyonlarını ölçer** - `Promise.all` vs ardışık `await` arasındaki performans farkını gerçek uygulamada benchmark yapar. Spread operator'ın büyük array'lerde O(n) olduğunu bilir ve gerektiğinde alternatif kullanır. `Object.freeze` vs Immer vs structuredClone karşılaştırmasını yapar.

4. **Error handling stratejisi tasarlar** - Uygulamanın hata yönetim mimarisini kurar: global error boundary, retry logic (exponential backoff), circuit breaker pattern. Custom Error class'ları oluşturur (`class ApiError extends Error`). Hangi hataların loglanacağını, hangilerinin kullanıcıya gösterileceğini belirler.

5. **Module mimarisini planlayabilir** - Barrel exports (`index.js` re-export), circular dependency tespiti, dynamic `import()` ile code splitting, tree-shaking'in nasıl çalıştığını ve neden side-effect free modüller yazılması gerektiğini bilir.

6. **WeakRef ve FinalizationRegistry bilir** - ES2021 ile gelen bu yapılarla gelişmiş cache mekanizmaları tasarlar. Memory profiling araçlarıyla (Chrome DevTools Memory tab) leak tespiti yapar.

**Profesyonel Mindset:** "Modern JavaScript özellikleri birer syntax şekeri değildir. Her biri belirli bir mimari problemi çözer. Destructuring okunabilirliği artırır, async/await karmaşıklığı azaltır, ES Modules ölçeklenebilirliği sağlar. Bu özellikleri 'ne zaman kullanmayacağını' bilmek, 'nasıl kullanacağını' bilmekten daha değerlidir. Over-engineering'den kaçın, kodun basit kalsın."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Destructuring** (dih-struk-chur-ing) - Yapı sökümü
   *"We use destructuring to extract values from objects and arrays."*

2. **Spread Operator** (spred op-uh-rey-ter) - Yayma operatörü
   *"The spread operator creates a shallow copy of the array."*

3. **Optional Chaining** (op-shuh-nl cheyn-ing) - Opsiyonel zincirleme
   *"Optional chaining prevents TypeError when accessing nested properties."*

4. **Asynchronous** (ey-sin-kruh-nuhs) - Eş zamanlı olmayan
   *"Async functions always return a Promise."*

5. **Module** (mod-yool) - Modül
   *"ES Modules support static analysis and tree-shaking."*

**Okuma Egzersizi:** MDN'de "JavaScript Modules" sayfasını İngilizce oku: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Async fonksiyonlara hata yönetimi ekledim"
-> Örnek: `feat: add error handling to async functions with try/catch`
:::

:::external-resource
- **MDN Web Docs:** "JavaScript Reference" - her özellik için en güvenilir kaynak (ücretsiz)
- **javascript.info:** "The Modern JavaScript Tutorial" - interaktif örneklerle öğren (ücretsiz)
- **ES6 Features:** es6-features.org - ES6 özelliklerinin ES5 karşılıkları (ücretsiz)
- **Fireship:** "JavaScript Pro Tips" serisi (YouTube, ücretsiz)
- **You Don't Know JS (YDKJS):** Kyle Simpson - derinlemesine JS kitap serisi (GitHub'da ücretsiz)
:::
