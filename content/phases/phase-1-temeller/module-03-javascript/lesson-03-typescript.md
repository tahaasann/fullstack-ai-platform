---
id: mod-03-js/lesson-03
title: "TypeScript: Profesyonel Tip Sistemi"
estimated_minutes: 60
order: 3
tags: ["typescript", "type-system", "generics", "utility-types", "static-typing"]
prerequisites: ["mod-03-js/lesson-01", "mod-03-js/lesson-02"]
---

# TypeScript: Profesyonel Tip Sistemi

:::realworld
2026'da TypeScript bilmeden profesyonel frontend veya backend geliştirici olmak neredeyse imkansiz. GitHub'daki en populer 100 JavaScript projesinin %95'inden fazlasi TypeScript'e geçiş yapti. React, Next.js, Angular, Vue 3, NestJS, tRPC, Prisma -- hepsi TypeScript-first. Is ilanlarinda "JavaScript" yazsa bile, mülakatta TypeScript soruyorlar. Bu ders seni TypeScript'in temellerinden ileri seviye tip sistemine kadar tasiyacak. Sadece syntax değil, "neden boyle tasarlanmis" perspektifini kazanacaksin.
:::

## Neden TypeScript Zorunlu?

TypeScript, JavaScript'e statik tip sistemi ekleyen bir superset dildir. Microsoft tarafindan gelistirilir ve açık kaynaktir. Peki neden 2026'da zorunlu?

- **Hatalari derleme zamaninda yakalar:** Runtime'da patlayan bug'lar yerine, kod yazarken IDE seni uyarir
- **IDE destegi muhtesem:** Autocomplete, refactoring, go-to-definition -- hepsi tip bilgisiyle çalışıyor
- **Dokümantasyon görevi gorur:** Fonksiyonun ne alip ne dondurdugunu tip imzasindan anlayabilirsin
- **Takim çalışmasını kolaylastirir:** Başkasının yazdığı kodu anlamak için tiplere bakmak yeterli
- **Sektor standardi:** Büyük şirketlerin %90'dan fazlasi TypeScript kullanıyor

:::deha-tip
Deha seviyesi geliştiriciler TypeScript'i "ekstra is" olarak değil, "güvenlik agi" olarak gorur. Tipleri önce yazar, sonra implementasyonu yapar. Bu yaklasima "Type-Driven Development" denir. Bir API endpoint'i yazarken önce request/response tiplerini tanımla, sonra business logic'i yaz. Boylece hem dokümantasyon hem de güvenlik saglanmis olur.
:::

## TypeScript Kurulumu ve tsconfig.json

:::code[bash]{title="TypeScript Kurulumu"}
# 📌 2026: pnpm önerilen paket yöneticisi (daha hızlı, disk verimli)
# Global kurulum (tek seferlik)
pnpm add -g typescript

# Proje bazli kurulum (önerilen)
pnpm add -D typescript

# TypeScript versiyonunu kontrol et
pnpm exec tsc --version

# Yeni proje için tsconfig.json oluştur
pnpm exec tsc --init
:::

:::code[json]{title="Önerilen tsconfig.json (2026 Modern Proje)"}
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
:::

:::beginner-mistake
Yaygin hata: `strict: false` ayariyla başlamak. "Sonra acarim" dersin ama asla acmazsin. Her zaman `strict: true` ile başla. Hata alirsan o hatayi coz, strict mode'u kapatma. Strict mode olmadan TypeScript, sadece "suslenmis JavaScript" olur.
:::

## Temel Tipler

:::code[typescript]{title="Primitive Tipler"}
// String
let isim: string = "Ahmet";

// Number (integer ve float ayirimi yok)
let yas: number = 28;
let maas: number = 45_000.50; // separator kullanabilirsin

// Boolean
let aktif: boolean = true;

// Null ve Undefined
let bos: null = null;
let tanimsiz: undefined = undefined;
:::

:::code[typescript]{title="Array ve Tuple"}
// Array - iki syntax
let sayilar: number[] = [1, 2, 3];
let isimler: Array<string> = ["Ali", "Veli"]; // Generic syntax

// Tuple - sabit uzunluk ve tip sirasi
let kullanıcı: [string, number] = ["Ahmet", 28];
// kullanıcı[0] -> string, kullanıcı[1] -> number

// Labeled Tuple (okunabilirlik için)
type KoordinatTuple = [x: number, y: number, z?: number];
let nokta: KoordinatTuple = [10, 20];
:::

:::code[typescript]{title="Enum"}
// Numeric Enum
enum Yonler {
  Kuzey,     // 0
  Guney,     // 1
  Dogu,      // 2
  Bati       // 3
}

// String Enum (önerilen - debug'da okunabilir)
enum HttpStatus {
  OK = "OK",
  NotFound = "NOT_FOUND",
  ServerError = "SERVER_ERROR"
}

// const enum (derleme zamaninda inline edilir, daha performansli)
const enum Renk {
  Kirmizi = "RED",
  Mavi = "BLUE",
  Yesil = "GREEN"
}
:::

:::code[typescript]{title="any, unknown, void, never"}
// any - tip kontrolunu tamamen devre disi bırakır (KACINILMALI)
let tehlikeli: any = "hersey olabilir";
tehlikeli.varolmayanMetot(); // Hata VERMEZ, runtime'da patlar!

// unknown - güvenli any alternatifi (tip kontrolu zorunlu)
let güvenli: unknown = "hersey olabilir";
// güvenli.toUpperCase(); // HATA! Önce tip kontrolu yap
if (typeof güvenli === "string") {
  güvenli.toUpperCase(); // Artik güvenli
}

// void - fonksiyon değer dondurmez
function logla(mesaj: string): void {
  console.log(mesaj);
}

// never - fonksiyon asla tamamlanmaz
function hataFirlat(mesaj: string): never {
  throw new Error(mesaj);
}

function sonsuzDongu(): never {
  while (true) {
    // asla bitmez
  }
}
:::

:::tip
`any` kullanmak, TypeScript'in sunduklarini cop kutusuna atmak demektir. Eger bir tipi bilmiyorsan `unknown` kullan ve type narrowing ile daralt. `any` sadece JavaScript'ten TypeScript'e geçiş doneminde, geçici olarak kabul edilebilir.
:::

## Type vs Interface

Bu, TypeScript'in en çok tartisilan konularindan biridir. Ikisi de obje tiplerini tanımlar ama önemli farklari vardir.

:::code[typescript]{title="Interface Kullanımı"}
// Interface - obje yapilarini tanımlamak için
interface Kullanıcı {
  id: number;
  isim: string;
  email: string;
  yas?: number; // opsiyonel (? isareti)
  readonly olusturulmaTarihi: Date; // değiştirilemez
}

// Interface extends (kalitim)
interface Admin extends Kullanıcı {
  yetki: string[];
  superAdmin: boolean;
}

// Declaration merging (ayni isimde tekrar tanımlanabilir)
interface Kullanıcı {
  telefon?: string; // Mevcut interface'e eklenir
}
:::

:::code[typescript]{title="Type Alias Kullanımı"}
// Type - her turlu tip için alias tanımlar
type ID = string | number; // Union type

type Kullanıcı2 = {
  id: ID;
  isim: string;
  email: string;
};

// Intersection ile birleştirme
type Admin2 = Kullanıcı2 & {
  yetki: string[];
  superAdmin: boolean;
};

// Type ile yapilabilip Interface ile yapilamayanlar:
type StringVeyaNumber = string | number; // Union
type Koordinat = [number, number];       // Tuple alias
type Callback = (data: string) => void;  // Function type
type Literal = "GET" | "POST" | "PUT";   // Literal union
:::

:::comparison
| Özellik | Interface | Type |
|---------|-----------|------|
| Obje tipleri | Evet | Evet |
| Extends/kalitim | `extends` keyword | `&` intersection |
| Declaration merging | Evet (ayni isimde tekrar tanımlanır) | Hayir (hata verir) |
| Union types | Hayir | Evet (`string \| number`) |
| Tuple types | Hayir | Evet |
| Primitive alias | Hayir | Evet (`type ID = string`) |
| Computed properties | Hayir | Evet |
| **Ne zaman kullan** | API kontrati, obje yapısı, class implement | Union, intersection, karmaşık tip işlemleri |

**2026 Genel Kurali:** Obje yapısı tanimliyorsan `interface`, diger her sey için `type` kullan. Takim içinde tutarlilik en onemlisi.
:::

## Union Types ve Intersection Types

:::code[typescript]{title="Union Types (|) - VEYA mantigi"}
// Değişken birden fazla tipte olabilir
type Sonuç = string | number | boolean;

// Literal Union - belirli degerlerle sinirla
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
type StatusCode = 200 | 201 | 400 | 404 | 500;

function apiCagir(url: string, method: HttpMethod): void {
  // method sadece belirtilen degerlerden biri olabilir
}

apiCagir("/users", "GET");    // OK
// apiCagir("/users", "HACK"); // HATA! "HACK" geçerli değil
:::

:::code[typescript]{title="Intersection Types (&) - VE mantigi"}
// Birden fazla tipi birleştirir
type Isim = { isim: string; soyisim: string };
type Iletişim = { email: string; telefon: string };

type Kisi = Isim & Iletişim;
// Kisi artik hem isim, soyisim hem de email, telefon icermeli

const kisi: Kisi = {
  isim: "Ahmet",
  soyisim: "Yilmaz",
  email: "ahmet@mail.com",
  telefon: "555-1234"
};
:::

## Type Narrowing ve Type Guards

TypeScript'in en güçlü özelliklerinden biri: bir degiskenin tipini daraltarak güvenli erişim sağlamak.

:::code[typescript]{title="typeof ile Type Guard"}
function isle(değer: string | number): string {
  // typeof ile tip kontrolu
  if (typeof değer === "string") {
    // Bu blokta TypeScript değer'in string oldugunu bilir
    return değer.toUpperCase();
  }
  // Burada değer kesinlikle number
  return değer.toFixed(2);
}
:::

:::code[typescript]{title="instanceof ile Type Guard"}
class Kopek {
  havla() { return "Hav hav!"; }
}

class Kedi {
  miyavla() { return "Miyav!"; }
}

function sesVer(hayvan: Kopek | Kedi): string {
  if (hayvan instanceof Kopek) {
    return hayvan.havla(); // TypeScript Kopek oldugunu bilir
  }
  return hayvan.miyavla(); // Burada kesinlikle Kedi
}
:::

:::code[typescript]{title="in operatoru ve Custom Type Guard"}
// 'in' operatoru - property kontrolu
interface Kus { üç(): void; kanatAcikligi: number; }
interface Balik { yuz(): void; derinlik: number; }

function hareketEt(hayvan: Kus | Balik): void {
  if ("üç" in hayvan) {
    hayvan.üç(); // Kus
  } else {
    hayvan.yuz(); // Balik
  }
}

// Custom Type Guard (is keyword)
interface ApiBasari<T> { success: true; data: T; }
interface ApiHata { success: false; error: string; }
type ApiSonuc<T> = ApiBasari<T> | ApiHata;

function başarılımı<T>(sonuç: ApiSonuc<T>): sonuç is ApiBasari<T> {
  return sonuç.success === true;
}

// Kullanım
function kullaniciGetir(sonuç: ApiSonuc<Kullanıcı>) {
  if (başarılımı(sonuç)) {
    console.log(sonuç.data.isim); // TypeScript data'nin varligini bilir
  } else {
    console.error(sonuç.error); // TypeScript error'un varligini bilir
  }
}
:::

## Generics

Generics, tipleri parametre olarak gecirmenizi sağlar. Kod tekrarini onler ve tip güvenliğini korur.

:::concept[Generic (Ing: Generic)]
Generic, bir fonksiyon, class veya interface'in çalışmak isteyecegi tipi parametre olarak almasi demektir.

**Turkce karsiligi:** Jenerik Tip / Tip Parametresi
**Ne ise yarar:** Ayni kodu farklı tiplerle tekrar kullanmani sağlar, tip güvenliğinden odun vermeden
**Gerçek hayat benzetmesi:** Bir kutu düşün. Kutu her seyi tasiyabilir ama içine ne koyduysan, cikardiginda da o tipi alirsin. "String kutusu"ndan string çıkar, "number kutusu"ndan number çıkar.
:::

:::code[typescript]{title="Generic Fonksiyonlar"}
// Generic olmadan - tip güvenliğini kaybedersin
function ilkElemanAny(dizi: any[]): any {
  return dizi[0]; // Donen tipi bilmiyoruz!
}

// Generic ile - tip güvenli
function ilkEleman<T>(dizi: T[]): T | undefined {
  return dizi[0];
}

const sayi = ilkEleman([1, 2, 3]);       // number | undefined
const kelime = ilkEleman(["a", "b"]);    // string | undefined

// Birden fazla generic parametre
function ciftOlustur<A, B>(a: A, b: B): [A, B] {
  return [a, b];
}

const çift = ciftOlustur("merhaba", 42); // [string, number]
:::

:::code[typescript]{title="Generic Constraint (Kısıtlama)"}
// T'nin en azindan belirli bir yapiya sahip olmasini zorunlu kil
interface Uzunluklu {
  length: number;
}

function uzunlukYaz<T extends Uzunluklu>(değer: T): T {
  console.log(`Uzunluk: ${değer.length}`);
  return değer;
}

uzunlukYaz("merhaba");   // OK, string'in length'i var
uzunlukYaz([1, 2, 3]);   // OK, array'in length'i var
// uzunlukYaz(123);       // HATA! number'in length'i yok

// keyof ile constraint
function degerGetir<T, K extends keyof T>(obj: T, anahtar: K): T[K] {
  return obj[anahtar];
}

const kisi2 = { isim: "Ali", yas: 25 };
const isim = degerGetir(kisi2, "isim"); // string
const yas = degerGetir(kisi2, "yas");   // number
// degerGetir(kisi2, "adres");           // HATA! "adres" kisi2'de yok
:::

:::code[typescript]{title="Generic Interface ve Class"}
// Generic Interface
interface Repository<T> {
  getAll(): Promise<T[]>;
  getById(id: string): Promise<T | null>;
  create(item: T): Promise<T>;
  update(id: string, item: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

// Generic Class
class InMemoryRepository<T extends { id: string }> implements Repository<T> {
  private items: Map<string, T> = new Map();

  async getAll(): Promise<T[]> {
    return Array.from(this.items.values());
  }

  async getById(id: string): Promise<T | null> {
    return this.items.get(id) ?? null;
  }

  async create(item: T): Promise<T> {
    this.items.set(item.id, item);
    return item;
  }

  async update(id: string, updates: Partial<T>): Promise<T> {
    const mevcut = this.items.get(id);
    if (!mevcut) throw new Error("Bulunamadi");
    const güncellenmiş = { ...mevcut, ...updates };
    this.items.set(id, güncellenmiş);
    return güncellenmiş;
  }

  async delete(id: string): Promise<void> {
    this.items.delete(id);
  }
}

// Kullanım
interface Urun { id: string; ad: string; fiyat: number; }
const urunRepo = new InMemoryRepository<Urun>();
:::

## Utility Types

TypeScript, mevcut tiplerden yeni tipler turetmek için yerlesik utility type'lar sunar. Bunlari bilmek, kod tekrarini büyük ölçüde azaltır.

:::code[typescript]{title="Partial, Required, Readonly"}
interface Kullanıcı {
  id: number;
  isim: string;
  email: string;
  bio?: string;
}

// Partial<T> - tüm property'leri opsiyonel yapar
type KullaniciGuncelleme = Partial<Kullanıcı>;
// { id?: number; isim?: string; email?: string; bio?: string; }

// Required<T> - tüm property'leri zorunlu yapar
type KullaniciZorunlu = Required<Kullanıcı>;
// { id: number; isim: string; email: string; bio: string; }

// Readonly<T> - tüm property'leri değiştirilemez yapar
type SabitKullanici = Readonly<Kullanıcı>;
const k: SabitKullanici = { id: 1, isim: "Ali", email: "a@b.com" };
// k.isim = "Veli"; // HATA! readonly
:::

:::code[typescript]{title="Pick, Omit, Record"}
interface Kullanıcı {
  id: number;
  isim: string;
  email: string;
  şifre: string;
  olusturulmaTarihi: Date;
}

// Pick<T, K> - sadece belirli property'leri seç
type KullaniciOnizleme = Pick<Kullanıcı, "id" | "isim">;
// { id: number; isim: string; }

// Omit<T, K> - belirli property'leri çıkar
type KullaniciPublic = Omit<Kullanıcı, "şifre">;
// { id: number; isim: string; email: string; olusturulmaTarihi: Date; }

// Record<K, V> - key-value map oluştur
type HataKodlari = Record<number, string>;
const hatalar: HataKodlari = {
  400: "Bad Request",
  404: "Not Found",
  500: "Internal Server Error"
};

type SayfaDurumlari = Record<"yukleniyor" | "başarılı" | "hata", boolean>;
:::

:::code[typescript]{title="ReturnType, Parameters, Awaited"}
function kullaniciOlustur(isim: string, yas: number) {
  return { id: Math.random(), isim, yas, aktif: true };
}

// ReturnType<T> - fonksiyonun dönüş tipini al
type YeniKullanici = ReturnType<typeof kullaniciOlustur>;
// { id: number; isim: string; yas: number; aktif: boolean; }

// Parameters<T> - fonksiyonun parametre tiplerini tuple olarak al
type OlusturParams = Parameters<typeof kullaniciOlustur>;
// [isim: string, yas: number]

// Awaited<T> - Promise'in cozulmus tipini al
type ApiResponse = Promise<{ data: Kullanıcı[] }>;
type CozulmusTip = Awaited<ApiResponse>;
// { data: Kullanıcı[] }
:::

## Discriminated Unions (Tagged Unions)

Discriminated union, union type'larin en güçlü pattern'idir. Her tip bir "tag" (ayirt edici) property'e sahiptir.

:::code[typescript]{title="Discriminated Union Örneği"}
// Her tip'in ortak bir "kind" veya "type" property'si var
interface YuklenmeDurumu {
  durum: "yukleniyor";
}

interface BasariDurumu<T> {
  durum: "başarılı";
  data: T;
}

interface HataDurumu {
  durum: "hata";
  mesaj: string;
  kod: number;
}

type AsyncDurum<T> = YuklenmeDurumu | BasariDurumu<T> | HataDurumu;

// Kullanım - TypeScript her case'de tipi otomatik daraltir
function durumGoster<T>(durum: AsyncDurum<T>): string {
  switch (durum.durum) {
    case "yukleniyor":
      return "Yukleniyor...";
    case "başarılı":
      return `Başarılı: ${JSON.stringify(durum.data)}`; // data erişilebilir
    case "hata":
      return `Hata ${durum.kod}: ${durum.mesaj}`; // mesaj ve kod erişilebilir
  }
}

// Gerçek dunya örneği: Redux action'lari
type KullaniciAction =
  | { type: "Kullanıcı_Yükle" }
  | { type: "Kullanıcı_Başarı"; payload: Kullanıcı }
  | { type: "Kullanıcı_HATA"; error: string };
:::

:::tip
Discriminated union kullandiginda `default` case'e `never` ata. Boylece yeni bir variant eklediginde TypeScript seni uyarir:
```typescript
function exhaustiveCheck(x: never): never {
  throw new Error(`Beklenmeyen deger: ${x}`);
}
```
:::

## Mapped Types ve Conditional Types

:::code[typescript]{title="Mapped Types"}
// Mevcut bir tipin tüm property'lerini dönüştür
type Opsiyonel<T> = {
  [K in keyof T]?: T[K];
};

type Değişmez<T> = {
  readonly [K in keyof T]: T[K];
};

// Sadece string property'leri seç
type StringPropertyler<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};

interface Urun {
  id: number;
  ad: string;
  açıklama: string;
  fiyat: number;
}

type UrunStringler = StringPropertyler<Urun>;
// { ad: string; açıklama: string; }
:::

:::code[typescript]{title="Conditional Types"}
// T extends U ? X : Y
type MetinMi<T> = T extends string ? "evet" : "hayir";

type Test1 = MetinMi<string>;  // "evet"
type Test2 = MetinMi<number>;  // "hayir"

// infer keyword - tipten bilgi çıkar
type DiziElemani<T> = T extends (infer U)[] ? U : never;

type Eleman1 = DiziElemani<string[]>;  // string
type Eleman2 = DiziElemani<number[]>;  // number

// Promise'in ic tipini çıkar
type PromiseIci<T> = T extends Promise<infer U> ? U : T;

type Sonuç1 = PromiseIci<Promise<string>>;  // string
type Sonuç2 = PromiseIci<number>;           // number (Promise değilse kendisi)

// Fonksiyon dönüş tipini çıkar (ReturnType'in implementasyonu)
type DonusTipi<T> = T extends (...args: any[]) => infer R ? R : never;
:::

## Type Assertion vs Type Casting

:::code[typescript]{title="Type Assertion (as keyword)"}
// Type assertion: "Ben bu tipi biliyorum" diye TypeScript'e soylersin
const girdi = document.getElementById("email") as HTMLInputElement;
girdi.value = "test@mail.com";

// Alternatif syntax (JSX ile uyumsuz, onerilmez)
const girdi2 = <HTMLInputElement>document.getElementById("email");

// Dikkat: Type assertion tip kontrolu yapmaz, sorumluluk sende!
const tehlikeli = "merhaba" as unknown as number;
// Bu çalışmaz ama TypeScript hata vermez!

// Doğru yaklaşım: önce kontrol et, sonra assertion
const eleman = document.getElementById("form");
if (eleman instanceof HTMLFormElement) {
  // Artik güvenli, assertion gereksiz
  eleman.submit();
}
:::

:::beginner-mistake
Type assertion ile type casting ayni sey Değildir. Type assertion (as) sadece derleme zamaninda TypeScript'e "bu tipi bil" der, runtime'da hicbir sey değiştirmez. Type casting (Number("42") gibi) ise runtime'da gerçekten veriyi dönüştürür. `"42" as number` yazamazsin ve yazsan bile string'i number'a cevirmez.
:::

## TypeScript vs Flow vs JSDoc

:::comparison
| Özellik | TypeScript | Flow | JSDoc |
|---------|-----------|------|-------|
| Geliştirici | Microsoft | Meta/Facebook | Topluluk standardi |
| Popularite (2026) | Pazar lideri (%95+) | Neredeyse terk edildi | Niş kullanım |
| Kurulum | Ayrı derleme adimi gerektirir | Ayrı derleme adimi | Ek arac gereksiz |
| Syntax | Ayrı `.ts` dosyalari | Ayrı `.js.flow` veya yorum içinde | JSDoc yorumlari içinde |
| IDE Destegi | Mükemmel | Sınırlı | Iyi (VS Code) |
| Ekosistem | Devasa (DefinitelyTyped) | Küçük | Sınırlı |
| Öğrenme egrisi | Orta | Orta | Düşük |
| **2026 tavsiyesi** | **Yeni proje = TypeScript** | Mevcut projede varsa gocur | Küçük scriptler için kabul edilebilir |

**Verdict:** 2026'da yeni proje basliyorsan TypeScript kullan. Flow'dan kacin. JSDoc sadece tip dosyasi oluşturmak istemedigin küçük utility scriptler için kabul edilebilir.
:::

## Gerçek Proje Örneği: API Response Typing

:::code[typescript]{title="Profesyonel API Response Tipleri"}
// Genel API response yapısı
interface ApiResponse<T> {
  success: boolean;
  data: T;
  meta?: {
    sayfa: number;
    sayfaBasi: number;
    toplam: number;
    toplamSayfa: number;
  };
}

interface ApiError {
  success: false;
  error: {
    kod: string;
    mesaj: string;
    detaylar?: Record<string, string[]>;
  };
}

// Kullanıcı tipleri
interface Kullanıcı {
  id: string;
  isim: string;
  email: string;
  rol: "admin" | "kullanıcı" | "moderator";
  profil: {
    avatar?: string;
    bio?: string;
    konum?: string;
  };
  oluşturulma: string; // ISO date string
  güncelleme: string;
}

// Yeni kullanıcı oluşturma için gerekli alanlar
type KullaniciOlustur = Pick<Kullanıcı, "isim" | "email"> & {
  şifre: string;
  rol?: Kullanıcı["rol"];
};

// Kullanıcı güncelleme için (hepsi opsiyonel, id haric)
type KullaniciGuncelle = Partial<Omit<Kullanıcı, "id" | "oluşturulma">> & {
  şifre?: string;
};

// Liste response
type KullaniciListeResponse = ApiResponse<Kullanıcı[]>;

// Tek kullanıcı response
type KullaniciDetayResponse = ApiResponse<Kullanıcı>;

// API fonksiyonu
async function kullanicilariGetir(
  sayfa: number = 1,
  sayfaBasi: number = 20
): Promise<KullaniciListeResponse | ApiError> {
  const response = await fetch(
    `/api/kullanıcılar?sayfa=${sayfa}&sayfaBasi=${sayfaBasi}`
  );

  const json = await response.json();

  if (!response.ok) {
    return json as ApiError;
  }

  return json as KullaniciListeResponse;
}

// Type guard ile güvenli kullanım
function apiBasarili<T>(
  sonuç: ApiResponse<T> | ApiError
): sonuç is ApiResponse<T> {
  return sonuç.success === true;
}

// Kullanım
async function sayfayiYukle() {
  const sonuç = await kullanicilariGetir(1, 10);

  if (apiBasarili(sonuç)) {
    // TypeScript burada sonuç.data'nin Kullanıcı[] oldugunu bilir
    sonuç.data.forEach(k => {
      console.log(`${k.isim} (${k.rol})`);
    });

    if (sonuç.meta) {
      console.log(`Toplam: ${sonuç.meta.toplam} kullanıcı`);
    }
  } else {
    // TypeScript burada sonuç'un ApiError oldugunu bilir
    console.error(`Hata: ${sonuç.error.mesaj}`);
  }
}
:::

:::exercise
### Alistirma 1: Interface ve Utility Type'lar ile Veri Modeli (Kolay)

Bir blog uygulamasi icin tip-guvenli veri modeli olustur ve Utility Type'lari kullan.

```typescript
// 1. User interface'i tanimla
interface User {
  id: number;
  username: string;
  email: string;
  role: "admin" | "editor" | "reader";
  createdAt: Date;
}

// 2. Post interface'i tanimla
interface Post {
  id: number;
  title: string;
  content: string;
  author: User;
  tags: string[];
  status: "draft" | "published" | "archived";
  publishedAt?: Date;
}

// TODO: Utility type'larla turetilmis tipler olustur:
type CreateUserInput = // Omit<User, "id" | "createdAt"> kullan
type UpdatePostInput = // Partial<Pick<Post, "title" | "content" | "tags" | "status">> kullan
type PostSummary = // Pick<Post, "id" | "title" | "status"> & { authorName: string } kullan

// TODO: Fonksiyonlari yaz:
function createUser(input: CreateUserInput): User {
  // id ve createdAt otomatik atanmali
  return { ...input, id: Math.random(), createdAt: new Date() };
}

function getPostSummaries(posts: Post[]): PostSummary[] {
  // Her post'tan sadece ozet bilgilerini cikar
  return posts.map((p) => ({
    id: p.id,
    title: p.title,
    status: p.status,
    authorName: p.author.username,
  }));
}

// Test — bu satirlar DERLEME HATASI vermeli:
// createUser({ username: "test" }); // email ve role eksik
// const u: User = { ...newUser, role: "superadmin" }; // gecersiz role
```

**Beklenen Sonuc:** `tsc --strict` ile hatasiz derlenme. Yanlis tiplerle cagrildiginda derleme hatasi alinmali.
**Ipucu:** `Omit` belirtilen key'leri cikarir, `Pick` sadece belirtilenleri alir, `Partial` tum alanlari optional yapar.

---

### Alistirma 2: Generic Repository Class'i (Orta)

Generic type'lar kullanarak tip-guvenli ve yeniden kullanilabilir bir repository olustur.

```typescript
type Result<T, E = string> =
  | { success: true; data: T }
  | { success: false; error: E };

class Repository<T extends { id: number }> {
  private items: Map<number, T> = new Map();
  private nextId: number = 1;

  // TODO: add — yeni item ekle, id otomatik atansin
  add(item: Omit<T, "id">): T {
    // Hint: { ...item, id: this.nextId++ } as T
  }

  // TODO: getById — bulunamazsa Result ile hata dondur
  getById(id: number): Result<T> { }

  // TODO: update — kismen guncelle
  update(id: number, data: Partial<Omit<T, "id">>): Result<T> { }

  // TODO: delete
  delete(id: number): Result<T> { }

  // TODO: find — kosulu saglayanlari dondur
  find(predicate: (item: T) => boolean): T[] { }

  getAll(): T[] {
    return Array.from(this.items.values());
  }
}

// Test — farkli tiplerle kullan:
interface Product { id: number; name: string; price: number; }
interface Task { id: number; title: string; completed: boolean; priority: "low" | "medium" | "high"; }

const products = new Repository<Product>();
products.add({ name: "Laptop", price: 15000 });
products.add({ name: "Mouse", price: 200 });

const result = products.getById(1);
if (result.success) {
  console.log(result.data.name); // TypeScript data'nin Product oldugunu bilir
}

const tasks = new Repository<Task>();
tasks.add({ title: "TS ogren", completed: false, priority: "high" });
const highPriority = tasks.find((t) => t.priority === "high");
```

**Beklenen Sonuc:** Ayni class farkli tiplerle (Product, Task) calismali. Result tipi ile type narrowing (success kontrolu) calismali.
**Ipucu:** `T extends { id: number }` kisitlamasi T'nin id alani oldugunu garanti eder.

---

### Alistirma 3: Discriminated Union ile State Machine (Zor)

Bir siparis sistemi icin tip-guvenli state machine olustur. Gecersiz state gecisleri derleme zamaninda yakalanmali.

```typescript
// State'ler
interface OrderPending {
  status: "pending";
  orderId: string;
  items: { productId: string; quantity: number }[];
  createdAt: Date;
}

interface OrderConfirmed {
  status: "confirmed";
  orderId: string;
  items: { productId: string; quantity: number }[];
  createdAt: Date;
  confirmedAt: Date;
}

interface OrderShipped {
  status: "shipped";
  orderId: string;
  items: { productId: string; quantity: number }[];
  createdAt: Date;
  confirmedAt: Date;
  shippedAt: Date;
  trackingNumber: string;
}

interface OrderCancelled {
  status: "cancelled";
  orderId: string;
  cancelledAt: Date;
  reason: string;
}

type Order = OrderPending | OrderConfirmed | OrderShipped | OrderCancelled;

// TODO: Sadece dogru state'ten gecis yapan fonksiyonlar yaz
function confirmOrder(order: OrderPending): OrderConfirmed {
  return { ...order, status: "confirmed", confirmedAt: new Date() };
}

function shipOrder(order: OrderConfirmed, trackingNumber: string): OrderShipped {
  // TODO: Implement
}

function cancelOrder(order: OrderPending | OrderConfirmed, reason: string): OrderCancelled {
  // TODO: Implement — shipped order iptal edilemez!
}

// TODO: Exhaustive switch ile durum mesaji
function getStatusMessage(order: Order): string {
  switch (order.status) {
    case "pending": return `Siparis #${order.orderId} onay bekliyor`;
    case "confirmed": return `Onaylandi: ${order.confirmedAt.toISOString()}`;
    // TODO: Diger case'ler
    // default: const _exhaustive: never = order; return _exhaustive;
  }
}

// Test — bu satirlar DERLEME HATASI vermeli:
const pending: OrderPending = {
  status: "pending", orderId: "ORD-1",
  items: [{ productId: "P1", quantity: 2 }], createdAt: new Date()
};
const confirmed = confirmOrder(pending);
// shipOrder(pending, "TR-123"); // HATA: pending ship edilemez
// cancelOrder(shipped, "iade"); // HATA: shipped iptal edilemez
```

**Beklenen Sonuc:** Gecersiz state transition'lar derleme zamaninda hata vermeli. Exhaustive switch tum durumlari handle etmeli.
**Ipucu:** `default: const _exhaustive: never = order;` ile switch'in tum case'leri kapsadigini garanti edebilirsin.
:::

:::knowledge-check
type: multiple_choice
question: "interface ile type arasindaki en kritik fark hangisidir?"
options:
  - "interface daha hızlıdır"
  - "type sadece primitive tipler içindir"
  - "interface declaration merging destekler, type union/intersection destekler"
  - "Aralarinda hicbir fark yoktur"
correct: 2
explanation: "Interface ayni isimde tekrar tanımlanabilir (declaration merging) ve extends ile kalitim destekler. Type ise union (|), intersection (&), tuple alias, primitive alias gibi daha esnek tip işlemleri destekler. Obje yapısı için interface, karmaşık tip işlemleri için type kullanılır."
:::

:::knowledge-check
type: multiple_choice
question: "Asagidakilerden hangisi doğru bir type guard'dir?"
options:
  - "if (değer as string) { ... }"
  - "if (typeof değer === 'string') { ... }"
  - "if (değer.type === string) { ... }"
  - "if (değer is string) { ... }"
correct: 1
explanation: "typeof operatoru runtime'da degerin tipini kontrol eder ve TypeScript bunu type narrowing için kullanır. 'as' bir assertion'dir (runtime kontrolu yapmaz), 'is' keyword'u sadece fonksiyon dönüş tipinde kullanılır (custom type guard), üçüncü secenek ise syntax olarak yanlistir."
:::

:::knowledge-check
type: multiple_choice
question: "Partial<T> utility type'i ne yapar?"
options:
  - "T tipinin tüm property'lerini siler"
  - "T tipinin tüm property'lerini opsiyonel (?) yapar"
  - "T tipinin tüm property'lerini readonly yapar"
  - "T tipinin sadece string property'lerini seçer"
correct: 1
explanation: "Partial<T>, T tipindeki tüm property'leri opsiyonel yapar. Bu, özellikle update/patch islemlerinde çok kullanislidir çünkü sadece değiştirmek istedigin alanlari gonderebilirsin."
:::

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6

### Prompt Örnekleri

**1. Konuyu Derinlemesine Anla:**
> "TypeScript'te Generics'in nasil çalıştığını bir Repository pattern örneği ile açıkla. Generic constraint (extends), keyof, ve conditional types'i bir arada kullanan gerçekçi bir örnek göster. <T extends { id: string }> gibi kisitlamalarin neden önemli oldugunu açıkla."

*Neden:* Generics'i anlamak, tekrar kullanılabilir ve tip-güvenli kod yazabilmenin anahtaridir. Framework'lerin kaynak kodunu okuyabilmek için şart

**2. Pratik Uygulama:**
> "Bir REST API için tam tip tanimlari yaz: ApiResponse<T> generic interface, ApiError type, discriminated union ile başarı/hata durumu, ve type guard fonksiyonu. Kullanıcı CRUD işlemleri için Pick, Omit ve Partial utility type'larini kullan."

*Follow-up:* "Bu tipleri frontend ve backend arasinda paylasilan bir shared types paketi olarak nasil yapilandirmaliyim? Monorepo'da tip senkronizasyonu nasil sağlanır?"

**3. Mukemmellik Için:**
> "TypeScript'te mapped types ve template literal types kullanarak type-safe bir API route builder yaz. Örneğin: defineRoute('/users/:id/posts/:postId') cagrisi otomatik olarak { id: string; postId: string } parametrelerini cikarsin. infer keyword'unu nasil kullanacagini göster."

### Pair Programming Ipucu
TypeScript hatalariyla karsilastiginda AI'a hata mesajini yapistir: "Bu TypeScript hatasini açıkla ve coz. 'Type X is not assignable to type Y' hatasinin kokeni ne? Type narrowing veya type assertion ile nasil duzeltmeliyim?"
:::

:::interview
## Mülakat Sorulari

**Soru 1: TypeScript'te interface ve type arasindaki fark nedir?**
- **Junior cevabi:** Ikisi de tip tanımlamak içindir, interface extend edilebilir.
- **Senior cevabi:** interface declaration merging destekler (ayni isimle birden fazla tanımlama birlestirilir), bu özellikle library type augmentation için kritiktir. type alias ise union, intersection, mapped types ve conditional types gibi gelişmiş tip islemlerini destekler. Pratikte object shape'ler için interface, utility tipler ve union'lar için type kullanılır. Interface'ler extends ile, type'lar & (intersection) ile birlestirilebilir.

**Soru 2: Generic'ler nedir ve ne zaman kullanılır?**
- **Junior cevabi:** Generic'ler tip parametresi alan fonksiyonlar ve siniflardir.
- **Senior cevabi:** Generic'ler type-safe ve reusable kod yazmanin temelidir. `Array<T>`, `Promise<T>` gibi built-in tipler generic'tir. Constraints ile (`T extends HasId`) tip güvenliğini korurken esneklik sağlanır. Örneğin bir API response wrapper `ApiResponse<T>` ile tüm endpoint'lerin return tipini type-safe yapabilirsiniz. Overuse'dan kacinmak gerekir, çünkü gereksiz generic'ler kodu okunakligi dusurur.
:::

:::must-note
- TypeScript = JavaScript + statik tip sistemi. Her geçerli JS, geçerli TS'dir
- `strict: true` ile başla, asla kapatma. Bu ayar TypeScript'in gucunu verir
- `any` KACINILMALI, `unknown` + type narrowing kullan
- Interface = obje yapıları ve declaration merging için. Type = union, intersection, tuple, primitive alias için
- Union type (|) = A veya B. Intersection type (&) = hem A hem B
- Type narrowing: typeof (primitive), instanceof (class), in (property), custom guard (is)
- Generics: `<T>` ile tip parametresi al, `extends` ile kisitla, `keyof` ile key'lere eris
- Utility Types: Partial (hepsi opsiyonel), Required (hepsi zorunlu), Pick (seç), Omit (çıkar), Record (map), Readonly (değiştirilemez), ReturnType (dönüş tipi), Parameters (parametre tipleri)
- Discriminated union: ortak tag property + switch/case = tip-güvenli pattern matching
- Type assertion (as) runtime'da hicbir sey yapmaz, sadece derleyiciye bilgi verir
- Mapped types: `[K in keyof T]` ile tüm property'leri dönüştür
- Conditional types: `T extends U ? X : Y` ile tip seviyesinde if-else yap
- `infer` keyword: conditional type içinde tip bilgisi çıkar (örneğin Promise'in ic tipi)
- 2026'da TypeScript sektor standardi. Flow terk edildi, JSDoc niche kalacak
:::

:::senior-learns
Bir Senior Developer veya CTO, TypeScript konusunu ogrenirken şu yaklasimi benimser:

1. **Type-Driven Development uygular** - Önce tipleri yazar, sonra implementasyonu yapar. Bir API endpoint'i tasarlarken ilk is request/response tiplerini tanimlamaktir. Bu yaklasimiyla hem dokümantasyon hem de derleme zamani güvenlik sağlar. Tipler anlasmaindir: frontend-backend arasindaki kontrat.

2. **TypeScript derleyici kaynak kodunu inceler** - `lib.es5.d.ts` ve `lib.dom.d.ts` dosyalarini okuyarak Utility Type'larin nasil implemente edildigini anlar. Örneğin `Partial<T>` aslinda basit bir mapped type'dir: `{ [K in keyof T]?: T[K] }`. Bu bilgiyle kendi utility type'larini yazabilir.

3. **Tip seviyesinde programlama yapar** - Conditional types, mapped types ve template literal types kullanarak "tip seviyesinde fonksiyonlar" yazar. Path parsing, SQL query builder, API route typing gibi ileri seviye tip işlemleri yapar. TypeScript'in tip sistemi aslinda Turing-complete bir dildir.

4. **Strict mode'u takimda zorunlu kilar** - `strict: true`, `noImplicitAny: true`, `strictNullChecks: true` ayarlarini proje baslangicinda aktif eder. ESLint ile `@typescript-eslint/no-explicit-any` kuralini "error" olarak ayarlar. Tip güvenliğinden odun vermez.

5. **Monorepo'da paylasilan tip paketleri oluşturur** - Frontend, backend ve mobile projeleri arasinda paylasilan tip tanimlari için ayrı bir paket oluşturur. Bu sayede API kontrati tek bir yerde tanımlanır ve tüm projeler güncel kalir. tRPC veya GraphQL codegen ile otomatik tip senkronizasyonu sağlar.

6. **Performance etkisini olcer** - Büyük projelerde TypeScript derleme suresini `tsc --diagnostics` ile izler. `isolatedModules`, `skipLibCheck`, Project References ve incremental build kullanarak derleme suresini optimize eder. Slow type'lari tespit edip basitlestirir.

**Profesyonel Mindset:** "TypeScript tip sistemi, kodun doğru calistiginin matematiksel ispatini sağlayan bir aractir. Tipleriniz ne kadar kesinse, runtime hatalariniz o kadar az olur. Amac `any` sifir olan bir codebase'dir. Her `any` bir potansiyel bug'dir. Senior mühendis, tip sistemini kodu yavaslatan bir engel değil, kodu hizlandiran bir rehber olarak gorur."
:::

:::english
**Teknik Ingilizce - Bu Dersteki Terimler:**

1. **Type System** (taɪp sɪs-təm) - Tip Sistemi
   *"TypeScript's type system catches errors at compile time instead of runtime."*

2. **Generic** (dʒə-nɛr-ɪk) - Jenerik / Genel Tip
   *"We use generics to create reusable components that work with multiple types."*

3. **Type Narrowing** (taɪp næ-roʊ-ɪŋ) - Tip Daraltma
   *"Type narrowing allows TypeScript to infer a more specific type within a conditional block."*

4. **Union Type** (juː-njən taɪp) - Birlesim Tipi
   *"A union type represents a value that can be one of several types."*

5. **Utility Type** (juː-tɪl-ə-ti taɪp) - Yardimci Tip
   *"Partial, Pick, and Omit are commonly used utility types for transforming existing types."*

**Okuma Egzersizi:** TypeScript resmi handbook'un "Everyday Types" bolumunu Ingilizce oku: https://www.typescriptlang.org/docs/handbook/2/everyday-types.html

**Yazma Pratigi:** Aşağıdaki commit mesajini Ingilizce yaz: "Kullanıcı API'si için TypeScript tiplerini ekledim"
-> Örnek: `feat: add TypeScript types for user API endpoints`
:::

:::external-resource
- TypeScript Handbook (resmi dokümantasyon, ücretsiz): https://www.typescriptlang.org/docs/handbook/
- Total TypeScript by Matt Pocock (ileri seviye egitim): https://www.totaltypescript.com/
- Type Challenges (interaktif tip bulmacalari): https://github.com/type-challenges/type-challenges
- TypeScript Playground (tarayicida dene): https://www.typescriptlang.org/play
:::
