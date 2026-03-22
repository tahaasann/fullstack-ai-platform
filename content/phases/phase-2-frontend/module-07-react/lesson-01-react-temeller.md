---
title: "React Temelleri: Component, Hooks ve TypeScript"
id: "mod-07-react/lesson-01"
estimated_minutes: 60
order: 1
tags: ["react", "hooks", "typescript", "jsx", "components", "virtual-dom"]
prerequisites: ["mod-06-typescript/lesson-01"]
---

# React Temelleri: Component, Hooks ve TypeScript

:::realworld
React, dünyanın en popüler frontend kütüphanesidir. Meta (Facebook), Instagram, Netflix, Airbnb, Discord gibi devler React kullanır. Bir iş ilanı sitesinde "Frontend Developer" aratığında karşına çıkan pozisyonların büyük çoğunluğu React bilgisi ister. Bu derste React'in temellerini sıfırdan öğrenecek, hooks sistemini derinlemesine kavrayacak ve TypeScript ile birlikte nasıl kullanılacağını anlayacaksın. Bu ders bittiğinde kendi component'lerini yazabilecek, state yönetebilecek ve custom hook'lar oluşturabilecek seviyeye geleceksin.
:::

## React Nedir?

React, kullanıcı arayüzleri oluşturmak için kullanılan bir JavaScript kütüphanesidir (framework değil). 2013 yılında Meta tarafından açık kaynak olarak yayınlandı. React'in temel felsefesi **declarative** (bildirimsel) programlamadır: "Bu veriye sahipsen, arayüz böyle görünsün" dersin, React gerisini halleder.

:::concept[Virtual DOM (İng: Virtual DOM)]
Virtual DOM, gerçek DOM'un hafif bir JavaScript kopyasıdır. React, state değiştiğinde önce Virtual DOM'u günceller, ardından gerçek DOM ile karşılaştırır (diffing) ve sadece değişen kısımları günceller (reconciliation).

**Türkçe karşılığı:** Sanal DOM
**Ne işe yarar:** DOM manipülasyonlarını minimize ederek performansı artırır
**Gerçek hayat benzetmesi:** Bir binayı yeniden boyarken tüm binayı sökmek yerine, sadece boyası dökülen duvarları boyamak gibi
:::

:::deha-tip
React 19 (2025) ile gelen en önemli yenilikler: React Compiler (otomatik memoization - artık useMemo/useCallback'e çoğu yerde gerek yok), Server Components (sunucuda render), Actions (form işlemleri için), useOptimistic ve useFormStatus hook'ları. React 19 ile birçok manuel optimizasyon artık otomatik yapılıyor. Ancak altta yatan kavramları bilmek hala kritik - compiler ne yaptığını anlamak için useMemo/useCallback mantığını bilmelisin.
:::

### Proje Oluşturma

:::code[bash]{title="React + TypeScript Projesi Oluşturma"}
# 📌 2026: pnpm önerilen paket yöneticisi (daha hızlı, disk verimli)
# Vite ile proje oluştur (önerilen yol)
pnpm create vite@latest my-app --template react-ts
cd my-app
pnpm install
pnpm dev

# Next.js ile proje oluştur (full-stack için)
pnpm dlx create-next-app@latest my-app --typescript --tailwind --app
:::

## JSX: JavaScript + XML

JSX, JavaScript içinde HTML benzeri sözdizimi yazmanı sağlayan bir syntax extension'dır. Tarayıcı JSX'i anlamaz; Babel veya SWC gibi araçlar JSX'i `React.createElement()` çağrılarına dönüştürür.

### JSX Kuralları

:::code[tsx]{title="JSX Kuralları ve Örnekler"}
// 1. Tek bir kök element döndürmelisin
// YANLIŞ:
// return (<h1>Başlık</h1><p>Paragraf</p>)

// DOĞRU: Fragment kullan
function App() {
  return (
    <>
      <h1>Başlık</h1>
      <p>Paragraf</p>
    </>
  );
}

// 2. HTML attribute isimleri farklıdır
// class → className, for → htmlFor, tabindex → tabIndex
<label htmlFor="email" className="input-label" tabIndex={0}>Email</label>

// 3. JavaScript ifadeleri süslü parantez {} içinde yazılır
const isim = "Ahmet";
<h1>Merhaba, {isim}!</h1>
<p>2 + 2 = {2 + 2}</p>

// 4. Style objesi kullanılır (camelCase)
<div style={{ backgroundColor: "blue", fontSize: "16px" }}>Styled</div>

// 5. Tüm tag'ler kapatılmalıdır
<img src="photo.jpg" alt="Fotoğraf" />  // Self-closing
<br />
<input type="text" />

// 6. Conditional rendering
{isLoggedIn && <Dashboard />}
{isAdmin ? <AdminPanel /> : <UserPanel />}

// 7. Liste rendering (key zorunlu!)
{users.map((user) => (
  <UserCard key={user.id} name={user.name} />
))}
:::

:::beginner-mistake
Yaygın hata: Liste render ederken `key` prop'unu unutmak veya index kullanmak. Key, React'in hangi elemanın değiştiğini takip etmesini sağlar. Index kullanırsan, liste sırası değiştiğinde React yanlış elemanları güncelleyebilir. Her zaman benzersiz ve sabit bir id kullan.
:::

## Fonksiyonel Componentler ve TypeScript

React'te component'ler JavaScript fonksiyonlarıdır. JSX döndürürler ve büyük harfle başlamalıdırlar.

:::code[tsx]{title="Component Tanımlama ve Props Typing"}
// Props interface tanımla
interface UserCardProps {
  name: string;
  age: number;
  email?: string;           // Opsiyonel prop
  role: "admin" | "user";   // Union type
  onEdit: (id: number) => void;  // Callback prop
  children: React.ReactNode;     // Children prop
}

// Fonksiyonel component
function UserCard({ name, age, email, role, onEdit, children }: UserCardProps) {
  return (
    <div className="user-card">
      <h2>{name}</h2>
      <p>Yaş: {age}</p>
      {email && <p>Email: {email}</p>}
      <span className={`badge badge-${role}`}>{role}</span>
      <button onClick={() => onEdit(1)}>Düzenle</button>
      <div className="card-content">{children}</div>
    </div>
  );
}

// Kullanımı
<UserCard name="Ali" age={25} role="admin" onEdit={(id) => console.log(id)}>
  <p>Kullanıcı detayları burada</p>
</UserCard>

// Default props ile
interface ButtonProps {
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

function Button({
  variant = "primary",
  size = "md",
  disabled = false,
  children,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
:::

:::tip
TypeScript ile React kullanırken `React.FC` (Function Component) tipini kullanma. Bu tip eski bir pattern'dir ve implicit children, defaultProps sorunları yaratır. Bunun yerine props'u doğrudan parametre olarak tip belirt.
:::

## useState: State Yönetimi

State, component'in zaman içinde değişebilen verisidir. State değiştiğinde component yeniden render olur.

:::code[tsx]{title="useState Hook - Temel ve İleri Kullanım"}
import { useState } from "react";

// Temel kullanım
function Counter() {
  const [count, setCount] = useState<number>(0);  // TypeScript ile tip belirtme

  return (
    <div>
      <p>Sayaç: {count}</p>
      <button onClick={() => setCount(count + 1)}>Artır</button>
    </div>
  );
}

// Updater function: önceki state'e bağlı güncellemeler
function BatchCounter() {
  const [count, setCount] = useState(0);

  const handleTripleIncrement = () => {
    // YANLIŞ: Üçü de aynı "count" değerini kullanır, sadece 1 artar
    // setCount(count + 1);
    // setCount(count + 1);
    // setCount(count + 1);

    // DOĞRU: Updater function ile her biri önceki değeri kullanır
    setCount((prev) => prev + 1);
    setCount((prev) => prev + 1);
    setCount((prev) => prev + 1);
    // Sonuç: count 3 artar
  };

  return <button onClick={handleTripleIncrement}>+3</button>;
}

// Lazy initialization: Ağır hesaplamalar için
function ExpensiveComponent() {
  // YANLIŞ: Her render'da hesaplanır
  // const [data, setData] = useState(expensiveCalculation());

  // DOĞRU: Sadece ilk render'da çalışır (fonksiyon geçirilir)
  const [data, setData] = useState(() => expensiveCalculation());

  return <div>{data}</div>;
}

// Obje state yönetimi (spread operator ile immutability)
interface User {
  name: string;
  email: string;
  age: number;
}

function UserForm() {
  const [user, setUser] = useState<User>({
    name: "",
    email: "",
    age: 0,
  });

  const updateName = (newName: string) => {
    // YANLIŞ: Doğrudan mutasyon
    // user.name = newName;

    // DOĞRU: Yeni obje oluştur
    setUser((prev) => ({ ...prev, name: newName }));
  };

  return (
    <input
      value={user.name}
      onChange={(e) => updateName(e.target.value)}
    />
  );
}

// Array state yönetimi
function TodoList() {
  const [todos, setTodos] = useState<string[]>([]);

  const addTodo = (todo: string) => {
    setTodos((prev) => [...prev, todo]);  // Ekleme
  };

  const removeTodo = (index: number) => {
    setTodos((prev) => prev.filter((_, i) => i !== index));  // Silme
  };

  const updateTodo = (index: number, newValue: string) => {
    setTodos((prev) =>
      prev.map((todo, i) => (i === index ? newValue : todo))  // Güncelleme
    );
  };

  return <div>{/* render */}</div>;
}
:::

:::beginner-mistake
Yaygın hata: State'i doğrudan mutasyona uğratmak. `user.name = "Ali"` yazmak React'in değişikliği fark etmesini engeller. Her zaman setter fonksiyonunu kullan ve yeni bir referans oluştur (spread operator veya map/filter ile). React, referans eşitliği (===) ile değişiklik kontrolü yapar.
:::

## useEffect: Yan Etkiler

useEffect, component'in dış dünya ile etkileşimini yönetir: API çağrıları, event listener'lar, timer'lar, DOM manipülasyonları.

:::code[tsx]{title="useEffect Hook - Tüm Kullanım Şekilleri"}
import { useState, useEffect } from "react";

// 1. Her render'da çalışır (dependency array yok - genellikle YANLIŞ)
useEffect(() => {
  console.log("Her render'da çalışır");
});

// 2. Sadece mount'ta çalışır (boş dependency array)
useEffect(() => {
  console.log("Component mount olduğunda bir kez çalışır");
}, []);

// 3. Belirli değerler değiştiğinde çalışır
useEffect(() => {
  console.log(`userId değişti: ${userId}`);
  fetchUserData(userId);
}, [userId]);

// 4. Cleanup fonksiyonu (unmount veya dependency değiştiğinde)
useEffect(() => {
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener("resize", handleResize);

  // Cleanup: event listener'ı temizle
  return () => {
    window.removeEventListener("resize", handleResize);
  };
}, []);

// 5. Data fetching pattern (doğru yol)
interface Post {
  id: number;
  title: string;
  body: string;
}

function PostDetail({ postId }: { postId: number }) {
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;  // Race condition önleme

    async function fetchPost() {
      setLoading(true);
      setError(null);

      try {
        const res = await fetch(`/api/posts/${postId}`);
        if (!res.ok) throw new Error("Post bulunamadı");
        const data: Post = await res.json();

        if (!cancelled) {
          setPost(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Bilinmeyen hata");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchPost();

    return () => {
      cancelled = true;  // Component unmount olursa fetch sonucunu yok say
    };
  }, [postId]);

  if (loading) return <p>Yükleniyor...</p>;
  if (error) return <p>Hata: {error}</p>;
  if (!post) return null;

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.body}</p>
    </article>
  );
}
:::

:::deha-tip
useEffect içinde async fonksiyon doğrudan kullanamazsın (useEffect callback'i Promise döndüremez). Bunun yerine içeride ayrı bir async fonksiyon tanımlayıp çağır. Ayrıca `cancelled` flag'i ile race condition'ı önle - kullanıcı hızla sayfalar arası geçiş yaparsa eski request'in sonucu yeni component'e yazılmasın.
:::

## useRef: DOM Referansı ve Mutable Değerler

useRef, render'lar arasında değer tutmak için kullanılır ama değiştiğinde re-render tetiklemez. Ayrıca DOM elemanlarına erişmek için kullanılır.

:::code[tsx]{title="useRef Hook Kullanımı"}
import { useRef, useEffect } from "react";

// 1. DOM referansı
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();  // DOM elemanına erişim
  };

  return (
    <div>
      <input ref={inputRef} type="text" placeholder="Adınız" />
      <button onClick={focusInput}>Input'a Odaklan</button>
    </div>
  );
}

// 2. Mutable value (re-render tetiklemez)
function StopWatch() {
  const [seconds, setSeconds] = useState(0);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const start = () => {
    intervalRef.current = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);
  };

  const stop = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  useEffect(() => {
    return () => stop();  // Cleanup
  }, []);

  return (
    <div>
      <p>{seconds} saniye</p>
      <button onClick={start}>Başlat</button>
      <button onClick={stop}>Durdur</button>
    </div>
  );
}

// 3. Önceki değeri tutma
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}
:::

## useId, useMemo, useCallback

:::code[tsx]{title="useId, useMemo ve useCallback"}
import { useId, useMemo, useCallback, useState } from "react";

// useId: SSR-uyumlu benzersiz id üretir
function FormField({ label }: { label: string }) {
  const id = useId();

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} type="text" />
    </div>
  );
}

// useMemo: Ağır hesaplamaları cache'le (değer memoization)
function FilteredList({ items, filter }: { items: string[]; filter: string }) {
  const filteredItems = useMemo(() => {
    console.log("Filtreleme hesaplanıyor...");
    return items.filter((item) =>
      item.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);  // Sadece items veya filter değiştiğinde yeniden hesapla

  return (
    <ul>
      {filteredItems.map((item, i) => (
        <li key={i}>{item}</li>
      ))}
    </ul>
  );
}

// useCallback: Fonksiyon referansını cache'le (referans memoization)
function ParentComponent() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  // Bu fonksiyon her render'da yeniden oluşturulmaz
  const handleIncrement = useCallback(() => {
    setCount((prev) => prev + 1);
  }, []);

  // text değişmediği sürece aynı referansı korur
  const handleSearch = useCallback((query: string) => {
    console.log(`Aranıyor: ${query}, text: ${text}`);
  }, [text]);

  return (
    <div>
      <ExpensiveChild onIncrement={handleIncrement} />
      <SearchBar onSearch={handleSearch} />
    </div>
  );
}
:::

:::tip
React 19 Compiler ile useMemo ve useCallback çoğu durumda otomatik olarak uygulanıyor. Yeni projelerde React Compiler kullanıyorsan bu hook'lara genellikle gerek kalmaz. Ancak kavramları bilmek, compiler'ın ne yaptığını anlamak ve eski projelerde çalışmak için kritik.
:::

## Custom Hooks: Kendi Hook'unu Yaz

Custom hook'lar, component mantığını yeniden kullanılabilir fonksiyonlara çıkarmak için kullanılır. `use` prefix'i ile başlamalıdırlar.

:::code[tsx]{title="Custom Hook Örnekleri"}
import { useState, useEffect, useCallback } from "react";

// 1. useToggle - Boolean state yönetimi
function useToggle(initialValue: boolean = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue((prev) => !prev), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse } as const;
}

// Kullanımı
function Modal() {
  const { value: isOpen, toggle, setFalse: close } = useToggle(false);

  return (
    <div>
      <button onClick={toggle}>Modal Aç/Kapat</button>
      {isOpen && (
        <div className="modal">
          <p>Modal içeriği</p>
          <button onClick={close}>Kapat</button>
        </div>
      )}
    </div>
  );
}

// 2. useDebounce - Geciktirilmiş değer
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);  // Cleanup: önceki timer'ı iptal et
  }, [value, delay]);

  return debouncedValue;
}

// Kullanımı
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState("");
  const debouncedSearch = useDebounce(searchTerm, 500);

  useEffect(() => {
    if (debouncedSearch) {
      // API çağrısı: her tuşa basışta değil, 500ms beklendikten sonra
      fetch(`/api/search?q=${debouncedSearch}`);
    }
  }, [debouncedSearch]);

  return (
    <input
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      placeholder="Ara..."
    />
  );
}

// 3. useLocalStorage - localStorage ile senkronize state
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const valueToStore = value instanceof Function ? value(prev) : value;
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
        return valueToStore;
      });
    },
    [key]
  );

  return [storedValue, setValue] as const;
}

// Kullanımı
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage<"light" | "dark">("theme", "light");

  return (
    <button onClick={() => setTheme((prev) => (prev === "light" ? "dark" : "light"))}>
      Tema: {theme}
    </button>
  );
}

// 4. useFetch - Generic data fetching
interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json: T = await res.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Hata oluştu");
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Kullanımı
function UserList() {
  const { data: users, loading, error, refetch } = useFetch<User[]>("/api/users");

  if (loading) return <p>Yükleniyor...</p>;
  if (error) return <p>Hata: {error} <button onClick={refetch}>Tekrar Dene</button></p>;

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
:::

## React Hooks Kuralları

:::comparison
| Kural | Açıklama | Neden? |
|-------|----------|--------|
| Sadece en üst seviyede çağır | if, for, while, nested function içinde hook kullanma | React hook'ları çağrı sırasına göre takip eder |
| Sadece React fonksiyonlarında çağır | Normal JS fonksiyonlarında hook kullanma | Hook'lar component veya custom hook içinde çalışır |
| `use` prefix'i | Custom hook'lar `use` ile başlamalı | Linter hook kurallarını uygulayabilsin |
| Dependency array doğruluğu | useEffect/useMemo/useCallback'te kullanılan tüm dış değerleri dependency'e ekle | Stale closure (eski değerlere erişim) hatasını önler |
:::

:::beginner-mistake
Yaygın hata: Hook'ları koşullu çağırmak. React, hook'ları çağrı sırasıyla eşleştirir. Bir if bloğu içinde hook kullanırsan, koşul değiştiğinde sıra kayar ve state'ler karışır.

```tsx
// YANLIŞ
if (isLoggedIn) {
  const [user, setUser] = useState(null);  // Koşullu hook!
}

// DOĞRU
const [user, setUser] = useState(null);  // Her zaman çağrılır
// Koşulu kullanırken kontrol et
useEffect(() => {
  if (isLoggedIn) {
    fetchUser();
  }
}, [isLoggedIn]);
```
:::

:::interview
**Mülakat Sorusu:** "useState ve useRef arasındaki fark nedir?"

**Beklenen cevap:**
- **useState**: Değer değiştiğinde component yeniden render olur. React render cycle'ına dahildir. UI'da gösterilecek veriler için kullanılır.
- **useRef**: Değer değiştiğinde re-render tetiklemez. `.current` property'si üzerinden erişilir. DOM referansları, timer ID'leri, önceki değerler gibi render'a etki etmeyecek veriler için kullanılır.
- Kural: Eğer değer ekranda gösteriliyorsa useState, gösterilmiyorsa useRef kullan.
:::

:::knowledge-check
type: multiple_choice
question: "useEffect'in cleanup fonksiyonu ne zaman çalışır?"
options:
  - "Sadece component mount olduğunda"
  - "Sadece component unmount olduğunda"
  - "Component unmount olduğunda ve dependency'ler değişmeden önce"
  - "Her render'dan sonra"
correct: 2
explanation: "Cleanup fonksiyonu iki durumda çalışır: (1) Component unmount olduğunda, (2) Effect yeniden çalışmadan önce (dependency değiştiğinde). Bu sayede eski event listener'lar, timer'lar ve subscription'lar temizlenir."
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdaki kodda handleClick çağrıldığında count değeri ne olur?\n\nconst [count, setCount] = useState(0);\nconst handleClick = () => { setCount(count + 1); setCount(count + 1); setCount(count + 1); };"
options:
  - "3"
  - "1"
  - "0"
  - "Hata verir"
correct: 1
explanation: "Üç setCount çağrısı da aynı render'daki count değerini (0) kullanır. Hepsi setCount(0 + 1) = setCount(1) yapar. React bunları batch'ler ve count 1 olur. Doğru yol: setCount(prev => prev + 1) kullanmaktır."
:::

:::exercise
### Alistirma 1: Counter Component (Kolay)

useState ile bir Counter component'i yaz: artir, azalt ve sifirla butonlari, min/max siniri olsun.

```tsx
import { useState } from "react";

function Counter({ initialValue = 0, step = 1, min = -100, max = 100 }) {
  // TODO: count state'i tanimla
  const [count, setCount] = useState(initialValue);

  // TODO: increment — max'i gecmemeli
  // TODO: decrement — min'in altina dusmemeli
  // TODO: reset — initialValue'ya dondur
  // TODO: count rengini degistir: negatif=kirmizi, pozitif=yesil, sifir=beyaz

  return (
    <div className="p-6 bg-gray-800 rounded-lg text-center">
      <h2 className="text-4xl font-bold mb-4">{count}</h2>
      <div className="flex gap-2 justify-center">
        <button onClick={() => {/* decrement */}}>-{step}</button>
        <button onClick={() => {/* reset */}}>Sifirla</button>
        <button onClick={() => {/* increment */}}>+{step}</button>
      </div>
    </div>
  );
}
```

**Beklenen Sonuc:** Counter min/max sinirlarinda durmali. Sifirla initialValue'ya dondurmeli.
**Ipucu:** `Math.min(max, count + step)` ve `Math.max(min, count - step)` ile sinirlama yap.

---

### Alistirma 2: TodoList ile Liste Yonetimi (Orta)

Input'tan todo ekle, tiklayarak tamamla, silme butonu ile sil. Filtre ve sayac ekle.

```tsx
import { useState } from "react";

interface Todo { id: number; text: string; completed: boolean; }

function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [input, setInput] = useState("");
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");

  // TODO: addTodo — bos input engellensin, id: Date.now()
  // TODO: toggleTodo — completed toggle
  // TODO: deleteTodo — id ile sil
  // TODO: filteredTodos — filter'a gore filtrele

  const activeTodoCount = todos.filter(t => !t.completed).length;

  return (
    <div className="max-w-md mx-auto p-6 bg-gray-800 rounded-lg">
      <div className="flex gap-2 mb-4">
        <input value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && /* addTodo */null}
          placeholder="Yeni gorev..." className="flex-1 bg-gray-700 rounded px-3 py-2" />
        <button className="bg-emerald-600 px-4 py-2 rounded">Ekle</button>
      </div>
      {/* TODO: Filtre butonlari (Tumu, Aktif, Tamamlanan) */}
      {/* TODO: filteredTodos.map ile liste render et */}
      {/* TODO: Tamamlanmis todo'larda line-through stili */}
      <p className="text-gray-400 mt-4">{activeTodoCount} aktif gorev</p>
    </div>
  );
}
```

**Beklenen Sonuc:** Todo eklenip silinebilmeli. Tiklanarak toggle edilebilmeli. Filtre çalışmali. Enter ile ekleme yapilabilmeli.
**Ipucu:** Immutable guncelleme: `setTodos(prev => prev.map(t => t.id === id ? {...t, completed: !t.completed} : t))`

---

### Alistirma 3: useLocalStorage Custom Hook (Zor)

Generic bir useLocalStorage hook'u yaz. useState gibi calissin ama degeri localStorage'a kaydetsin.

```tsx
import { useState, useEffect } from "react";

function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
  // TODO: Lazy initialization — localStorage'dan oku
  const [value, setValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch { return initialValue; }
  });

  // TODO: useEffect ile state degistiginde localStorage'a kaydet
  useEffect(() => {
    // window.localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}

// Test:
function App() {
  const [theme, setTheme] = useLocalStorage("theme", "dark");
  const [todos, setTodos] = useLocalStorage<string[]>("todos", []);

  return (
    <div>
      <button onClick={() => setTheme(t => t === "dark" ? "light" : "dark")}>
        Tema: {theme}
      </button>
      <button onClick={() => setTodos(prev => [...prev, `Todo ${prev.length + 1}`])}>
        Todo Ekle ({todos.length})
      </button>
    </div>
  );
}
```

**Beklenen Sonuc:** Sayfa yenilendiginde degerler korunmali. Farkli tiplerle (string, object, array) çalışmali.
**Ipucu:** Lazy initialization ile ilk render'da localStorage'dan oku. SSR'da `window` undefined olabilir — try/catch ile handle et.
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "React'in Virtual DOM ve reconciliation algoritmasini adim adim acikla. Bir state degistiginde React dahili olarak ne yapar? Fiber mimarisi nedir ve neden eski stack reconciler'dan gecildi? Diffing algoritmasi O(n) karmasikligini nasil basariyor?"

**2. Pratik Uygulama:**
> "useDebounce, useLocalStorage ve useFetch custom hook'larini sifirdan yaz. Her hook icin TypeScript tipleri, edge case yonetimi (race condition, cleanup) ve kullanim örnekleri ver. Ardindan bu hook'lari kullanan bir arama component'i oluştur."
> Takip: "Bu hook'larda stale closure sorunu var mi? Varsa nasil cozulur? useCallback dependency'lerini dogru yonettigimi kontrol et."

**3. Mukemmellik Icin:**
> "React 19 Compiler ile useMemo ve useCallback artik cogunlukla gereksiz. Compiler'in ne yaptigini, hangi durumlarda hala manuel memoization gerektigini ve bir projeyi React 19'a migrate ederken dikkat edilmesi gereken noktalari anlat. Örnek kod ile oncesi-sonrasi karsilastirmasi yap."

### Pair Programming Ipucu
Component yazarken AI'a React DevTools Profiler ciktisini goster ve sor: "Bu component neden 5 kez render oldu? Profiler flame graph'ini analiz et ve gereksiz render'larin kaynagini tespit edip coz."
:::

:::exercise
### Alıştırma 4: Props ile Kart Component'i
**Görev:** TypeScript ile tip güvenli bir `ProductCard` component'i oluştur.
**Başlangıç kodu:**
```tsx
// TODO: ProductCardProps interface'ini tanımla
interface ProductCardProps {
  // title: string (zorunlu)
  // price: number (zorunlu)
  // image?: string (opsiyonel)
  // onSale?: boolean (opsiyonel, varsayılan false)
}

// TODO: Component'i yaz
function ProductCard(/* props */) {
  return (
    <div className="border rounded-lg p-4">
      {/* TODO: image varsa göster, yoksa placeholder */}
      {/* TODO: title'ı h3 ile göster */}
      {/* TODO: price'ı formatlı göster (₺199.99) */}
      {/* TODO: onSale true ise "İndirimde!" badge'i göster */}
    </div>
  );
}
```
**Beklenen çıktı:**
```tsx
interface ProductCardProps {
  title: string;
  price: number;
  image?: string;
  onSale?: boolean;
}

function ProductCard({ title, price, image, onSale = false }: ProductCardProps) {
  return (
    <div className="border rounded-lg p-4">
      {image ? <img src={image} alt={title} /> : <div className="bg-gray-200 h-48" />}
      <h3 className="font-bold mt-2">{title}</h3>
      <p className="text-emerald-500">₺{price.toFixed(2)}</p>
      {onSale && <span className="bg-red-500 text-white px-2 py-1 rounded text-sm">İndirimde!</span>}
    </div>
  );
}
```
**İpucu:** Destructuring ile props al, varsayılan değer için `= false` kullan. Koşullu render için `&&` operatörü.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: useState ile Sayaç ve Toggle
**Görev:** Birden fazla state kullanan bir component yaz: sayaç ve tema toggle.
**Başlangıç kodu:**
```tsx
import { useState } from "react";

function CounterWithTheme() {
  // TODO: count state'i (başlangıç: 0)
  // TODO: isDark state'i (başlangıç: true)

  // TODO: increment fonksiyonu (prev => prev + 1 kullan)
  // TODO: decrement fonksiyonu (0'ın altına düşmesin)
  // TODO: reset fonksiyonu
  // TODO: toggleTheme fonksiyonu

  return (
    <div className={/* TODO: isDark'a göre arka plan */}>
      <h2>Sayaç: {/* TODO */}</h2>
      <button onClick={/* TODO */}>+</button>
      <button onClick={/* TODO */}>-</button>
      <button onClick={/* TODO */}>Sıfırla</button>
      <button onClick={/* TODO */}>
        {/* TODO: isDark ? "☀️ Light" : "🌙 Dark" */}
      </button>
    </div>
  );
}
```
**Beklenen çıktı:**
```tsx
const [count, setCount] = useState(0);
const [isDark, setIsDark] = useState(true);

const increment = () => setCount(prev => prev + 1);
const decrement = () => setCount(prev => Math.max(0, prev - 1));
const reset = () => setCount(0);
const toggleTheme = () => setIsDark(prev => !prev);
```
**İpucu:** `setCount(prev => prev + 1)` updater function'ı batch güncelleme için güvenlidir. `Math.max(0, prev - 1)` negatif değeri engeller.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 6: useEffect ile API Çağrısı
**Görev:** useEffect ile component mount olduğunda API'den veri çek, loading ve error state'lerini yönet.
**Başlangıç kodu:**
```tsx
import { useState, useEffect } from "react";

interface User {
  id: number;
  name: string;
  email: string;
}

function UserList() {
  // TODO: users, loading, error state'lerini tanımla

  useEffect(() => {
    // TODO: fetchUsers async fonksiyonu yaz
    // 1. loading = true yap
    // 2. fetch("https://jsonplaceholder.typicode.com/users")
    // 3. response.ok kontrolü
    // 4. data'yı users state'ine set et
    // 5. hata varsa error state'ine set et
    // 6. finally'de loading = false

    // TODO: cleanup fonksiyonu (AbortController)
  }, []); // Sadece mount'ta çalış

  // TODO: loading, error, empty state render'ları
  // TODO: users listesini render et
}
```
**Beklenen çıktı:**
```tsx
const [users, setUsers] = useState<User[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);

useEffect(() => {
  const controller = new AbortController();

  async function fetchUsers() {
    try {
      setLoading(true);
      const res = await fetch("https://jsonplaceholder.typicode.com/users", {
        signal: controller.signal,
      });
      if (!res.ok) throw new Error("API hatası");
      const data: User[] = await res.json();
      setUsers(data);
    } catch (err) {
      if (err instanceof Error && err.name !== "AbortError") {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  }
  fetchUsers();

  return () => controller.abort();
}, []);
```
**İpucu:** `AbortController` ile unmount olduğunda isteği iptal et. `AbortError`'ı yakalayıp yoksay - bu beklenen bir durum.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: Liste Render ve Key Kullanımı
**Görev:** Bir yapılacaklar listesi oluştur: ekleme, silme ve tamamlama işlevleri olsun.
**Başlangıç kodu:**
```tsx
import { useState } from "react";

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [input, setInput] = useState("");

  // TODO: addTodo - yeni todo ekle (id için Date.now() kullan)
  // TODO: toggleTodo - completed değerini tersle
  // TODO: deleteTodo - id'ye göre sil

  return (
    <div>
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={/* TODO */}>Ekle</button>

      <ul>
        {/* TODO: todos.map ile listele
            - key olarak todo.id kullan (index KULLANMA!)
            - completed ise üzeri çizili göster
            - Tamamla ve Sil butonları ekle */}
      </ul>
    </div>
  );
}
```
**Beklenen çıktı:**
```tsx
const addTodo = () => {
  if (!input.trim()) return;
  setTodos(prev => [...prev, { id: Date.now(), text: input, completed: false }]);
  setInput("");
};

const toggleTodo = (id: number) => {
  setTodos(prev => prev.map(t => t.id === id ? { ...t, completed: !t.completed } : t));
};

const deleteTodo = (id: number) => {
  setTodos(prev => prev.filter(t => t.id !== id));
};

// JSX:
{todos.map(todo => (
  <li key={todo.id} style={{ textDecoration: todo.completed ? "line-through" : "none" }}>
    {todo.text}
    <button onClick={() => toggleTodo(todo.id)}>Tamamla</button>
    <button onClick={() => deleteTodo(todo.id)}>Sil</button>
  </li>
))}
```
**İpucu:** `key` olarak array index kullanma - silme/ekleme işlemlerinde React elementleri karıştırır. Benzersiz `id` kullan.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: useRef ile DOM Manipülasyonu
**Görev:** useRef kullanarak input'a otomatik focus ver ve scroll-to-top butonu oluştur.
**Başlangıç kodu:**
```tsx
import { useRef, useEffect } from "react";

function SearchPage() {
  // TODO: inputRef tanımla (HTMLInputElement)
  // TODO: topRef tanımla (HTMLDivElement)

  // TODO: Sayfa yüklendiğinde input'a focus ver
  useEffect(() => {
    // ???
  }, []);

  const scrollToTop = () => {
    // TODO: topRef'e smooth scroll yap
  };

  return (
    <div>
      <div ref={/* TODO */}>Sayfa Başı</div>
      <input ref={/* TODO */} placeholder="Ara..." />
      {/* Uzun içerik */}
      <div style={{ height: "2000px" }}>İçerik</div>
      <button onClick={scrollToTop}>Yukarı Git</button>
    </div>
  );
}
```
**Beklenen çıktı:**
```tsx
const inputRef = useRef<HTMLInputElement>(null);
const topRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  inputRef.current?.focus();
}, []);

const scrollToTop = () => {
  topRef.current?.scrollIntoView({ behavior: "smooth" });
};
```
**İpucu:** `useRef<HTMLInputElement>(null)` ile tip belirt. `.current?.focus()` optional chaining ile güvenli erişim sağlar.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 9: Custom Hook Yazma
**Görev:** `useLocalStorage` custom hook'u yaz: state'i localStorage ile senkronize etsin.
**Başlangıç kodu:**
```tsx
// TODO: useLocalStorage hook'unu yaz
function useLocalStorage<T>(key: string, initialValue: T) {
  // TODO: useState ile başlangıç değerini localStorage'dan oku
  // Eğer localStorage'da varsa parse et, yoksa initialValue kullan

  // TODO: setValue fonksiyonu - hem state'i hem localStorage'ı güncelle

  // TODO: [value, setValue] döndür (useState gibi)
}

// Kullanım:
function Settings() {
  const [theme, setTheme] = useLocalStorage("theme", "dark");
  const [fontSize, setFontSize] = useLocalStorage("fontSize", 16);

  return (
    <div>
      <select value={theme} onChange={e => setTheme(e.target.value)}>
        <option value="dark">Dark</option>
        <option value="light">Light</option>
      </select>
    </div>
  );
}
```
**Beklenen çıktı:**
```tsx
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    setStoredValue(value);
    localStorage.setItem(key, JSON.stringify(value));
  };

  return [storedValue, setValue];
}
```
**İpucu:** `useState(() => ...)` lazy initializer ile localStorage'ı sadece ilk render'da oku. JSON.parse/stringify ile her tipi destekle.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: Hooks Kuralları Hata Tespiti
**Görev:** Aşağıdaki kodda hooks kurallarını ihlal eden 5 hatayı bul ve düzelt.
**Başlangıç kodu:**
```tsx
function BrokenComponent({ isAdmin }: { isAdmin: boolean }) {
  const [count, setCount] = useState(0);

  // HATA 1: Koşullu hook
  if (isAdmin) {
    const [adminData, setAdminData] = useState(null);
  }

  // HATA 2: Döngü içinde hook
  for (let i = 0; i < 3; i++) {
    useEffect(() => console.log(i), []);
  }

  // HATA 3: İç içe fonksiyon içinde hook
  function handleClick() {
    const [clicked, setClicked] = useState(false);
  }

  // HATA 4: return'dan sonra hook
  if (count > 10) return <p>Limit aşıldı</p>;
  const [extra, setExtra] = useState("");

  // HATA 5: useEffect'te eksik dependency
  const [data, setData] = useState("");
  useEffect(() => {
    fetchData(count).then(setData);
  }, []); // count dependency eksik

  return <div>{count}</div>;
}
```
**Beklenen çıktı:**
```
HATA 1: Hook'lar koşul içinde çağrılamaz → adminData'yı her zaman tanımla, koşulu render'da kullan
HATA 2: Hook'lar döngü içinde çağrılamaz → useEffect'i tek sefer çağır, döngüyü içinde yap
HATA 3: Hook'lar sadece component/custom hook'un en üst seviyesinde çağrılabilir
HATA 4: Hook'lar koşullu return'dan sonra olamaz → return'u en sona taşı
HATA 5: useEffect dependency array'inde count eksik → [count] ekle
```
**İpucu:** Hooks kuralları: 1) Her zaman aynı sırada çağır, 2) Sadece fonksiyon component veya custom hook içinde çağır, 3) Koşul/döngü/iç fonksiyon içinde çağırma.
**Zorluk:** Zor
:::

:::must-note
- React = declarative UI kütüphanesi, Virtual DOM ile sadece değişen kısmı günceller
- JSX kuralları: tek kök element, className (class değil), htmlFor (for değil), {} ile JS ifadesi
- Component = büyük harfle başlayan fonksiyon, Props = component'e dışarıdan verilen parametreler
- useState: state değişimi -> re-render, updater function (prev => prev + 1) batch güncelleme için
- useState lazy init: useState(() => expensiveCalc()) - sadece ilk render'da çalışır
- useEffect dependency array: [] = mount, [dep] = dep değişince, hiç yok = her render
- useEffect cleanup: return () => {} ile event listener/timer temizleme, race condition önleme
- useRef: re-render tetiklemez, DOM referansı ve mutable değerler için (inputRef.current?.focus())
- useMemo = değer cache, useCallback = fonksiyon referansı cache (React 19 Compiler ile çoğunlukla gereksiz)
- useId = SSR-uyumlu benzersiz id (form label-input eşleştirme için)
- Custom hook = use ile başlar, hook mantığını yeniden kullanılabilir yapar
- Hook kuralları: sadece en üst seviyede, sadece React fonksiyonlarında, koşullu çağırma YASAK
- State immutability: obje/array state'te spread operator ile yeni referans oluştur
- Key prop: listede benzersiz id kullan, index kullanma (sıra değişirse bug)
:::

:::senior-learns
Bir Senior Developer veya CTO, React temellerini öğrenirken şu yaklaşımı benimser:

1. **React kaynak kodunu okur** - useState'in nasıl implement edildiğini, fiber mimarisini ve reconciliation algoritmasını React GitHub reposundan inceler. Hook'ların aslında linked list'te tutulduğunu anlar - bu yüzden koşullu çağırma yasaktır.
2. **Render döngüsünü derinlemesine anlar** - React DevTools Profiler ile her render'ın nedenini analiz eder. "Bu component neden 5 kez render oldu?" sorusuna kesin cevap verebilir. Strict Mode'un development'ta neden çift render yaptığını bilir.
3. **Composition over inheritance** prensibini uygular - Derin component hiyerarşileri yerine composition pattern kullanır. children, render props ve custom hook'lar ile mantığı paylaşır.
4. **Production hata pattern'lerini tanır** - Stale closure, infinite re-render loop, memory leak (cleanup'sız useEffect), race condition gibi yaygın hataları anında teşhis eder.
5. **Test-driven component geliştirme yapar** - Component'i yazmadan önce testini yazar. React Testing Library ile kullanıcı perspektifinden test eder, implementation detail'leri test etmez.
6. **Performans sorunlarını sistematik çözer** - React Profiler ile bottleneck'i bulur, gereksiz re-render'ları tespit eder, büyük listelerde virtualization (react-window/tanstack-virtual) kullanır.

**Profesyonel Mindset:** "React'in gücü basitliğinde yatar: state + props = UI. Bu formülü derinlemesine anla. Karmaşık state yönetimi için hemen Redux'a koşma, önce component yapını düzelt. Çoğu 'state management problemi' aslında 'component design problemi'dir."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Component** (kəm-poh-nənt) → Bileşen
   *"React components are the building blocks of the user interface."*

2. **Hook** (hʊk) → Kanca / Hook
   *"Hooks let you use state and other React features in function components."*

3. **State** (steɪt) → Durum
   *"When state changes, React re-renders the component to reflect the new data."*

4. **Props** (prɒps) → Özellikler / Parametreler
   *"Props are read-only values passed from parent to child components."*

5. **Render** (ren-dər) → İşleme / Render etme
   *"React renders the component tree whenever state or props change."*

**Okuma Egzersizi:** React resmi docs'tan "Thinking in React" sayfasını İngilizce oku: https://react.dev/learn/thinking-in-react

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Kullanıcı kartı component'ini ve custom hook'ları ekledim"
-> Örnek: `feat: add user card component and custom hooks`
:::

:::external-resource
- React Resmi Docs: https://react.dev (interaktif, ücretsiz)
- TypeScript + React Cheatsheet: https://react-typescript-cheatsheet.netlify.app
- Josh W. Comeau: "The Joy of React" kursu (kapsamlı, ücretli)
- Kent C. Dodds: "Epic React" (ileri seviye, ücretli)
- Fireship YouTube: "React in 100 Seconds" ve "React Hooks Explained" (ücretsiz)
:::
