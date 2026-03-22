---
title: "State Patterns, Routing ve Performance"
id: "mod-07-react/lesson-02"
estimated_minutes: 60
order: 2
tags: ["useReducer", "context", "zustand", "react-router", "react-hook-form", "performance", "memo"]
prerequisites: ["mod-07-react/lesson-01"]
---

# State Patterns, Routing ve Performance

:::realworld
Gerçek projelerde state yönetimi, routing ve performans optimizasyonu en çok zaman harcadığın konular olacak. Bir e-ticaret sitesi düşün: kullanıcı giriş bilgisi global state'te tutulmalı, ürün listesi sayfalanmalı, sepet her yerden erişilebilir olmalı ve binlerce ürün listelenirken sayfa kasmamalı. Bu derste, bu sorunların her birine profesyonel çözümler öğreneceksin.
:::

## useReducer: Karmaşık State Yönetimi

useReducer, useState'in alternatifidir. State geçişleri karmaşık olduğunda, birden fazla alt değer içerdiğinde veya bir sonraki state öncekine bağlı olduğunda useReducer tercih edilir.

:::concept[Reducer Pattern (İng: Reducer Pattern)]
Reducer, mevcut state ve bir action alıp yeni state döndüren saf (pure) bir fonksiyondur: `(state, action) => newState`. Redux'tan ilham alan bu pattern, state değişikliklerini öngörülebilir ve test edilebilir yapar.

**Türkçe karşılığı:** İndirgeyici Pattern
**Ne işe yarar:** Karmaşık state mantığını tek bir yerde toplar, debug kolaylaştırır
**Gerçek hayat benzetmesi:** Bir banka hesabı: "para yatır", "para çek", "faiz ekle" gibi action'lar var, her biri mevcut bakiyeye göre yeni bakiyeyi hesaplar
:::

:::code[tsx]{title="useReducer - Kapsamlı Örnek"}
import { useReducer } from "react";

// State tipi
interface TodoState {
  todos: { id: number; text: string; completed: boolean }[];
  filter: "all" | "active" | "completed";
  nextId: number;
}

// Action tipleri (discriminated union)
type TodoAction =
  | { type: "ADD_TODO"; payload: string }
  | { type: "TOGGLE_TODO"; payload: number }
  | { type: "DELETE_TODO"; payload: number }
  | { type: "SET_FILTER"; payload: TodoState["filter"] }
  | { type: "CLEAR_COMPLETED" };

// Initial state
const initialState: TodoState = {
  todos: [],
  filter: "all",
  nextId: 1,
};

// Reducer fonksiyonu (pure function - yan etkisi yok!)
function todoReducer(state: TodoState, action: TodoAction): TodoState {
  switch (action.type) {
    case "ADD_TODO":
      return {
        ...state,
        todos: [
          ...state.todos,
          { id: state.nextId, text: action.payload, completed: false },
        ],
        nextId: state.nextId + 1,
      };

    case "TOGGLE_TODO":
      return {
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === action.payload
            ? { ...todo, completed: !todo.completed }
            : todo
        ),
      };

    case "DELETE_TODO":
      return {
        ...state,
        todos: state.todos.filter((todo) => todo.id !== action.payload),
      };

    case "SET_FILTER":
      return { ...state, filter: action.payload };

    case "CLEAR_COMPLETED":
      return {
        ...state,
        todos: state.todos.filter((todo) => !todo.completed),
      };

    default:
      return state;
  }
}

// Component
function TodoApp() {
  const [state, dispatch] = useReducer(todoReducer, initialState);

  const filteredTodos = state.todos.filter((todo) => {
    if (state.filter === "active") return !todo.completed;
    if (state.filter === "completed") return todo.completed;
    return true;
  });

  return (
    <div>
      <input
        onKeyDown={(e) => {
          if (e.key === "Enter" && e.currentTarget.value.trim()) {
            dispatch({ type: "ADD_TODO", payload: e.currentTarget.value });
            e.currentTarget.value = "";
          }
        }}
        placeholder="Yeni görev ekle..."
      />

      <ul>
        {filteredTodos.map((todo) => (
          <li key={todo.id}>
            <span
              onClick={() => dispatch({ type: "TOGGLE_TODO", payload: todo.id })}
              style={{ textDecoration: todo.completed ? "line-through" : "none" }}
            >
              {todo.text}
            </span>
            <button onClick={() => dispatch({ type: "DELETE_TODO", payload: todo.id })}>
              Sil
            </button>
          </li>
        ))}
      </ul>

      <div>
        <button onClick={() => dispatch({ type: "SET_FILTER", payload: "all" })}>Tümü</button>
        <button onClick={() => dispatch({ type: "SET_FILTER", payload: "active" })}>Aktif</button>
        <button onClick={() => dispatch({ type: "SET_FILTER", payload: "completed" })}>Tamamlanan</button>
        <button onClick={() => dispatch({ type: "CLEAR_COMPLETED" })}>Tamamlananları Temizle</button>
      </div>
    </div>
  );
}
:::

:::comparison
| Özellik | useState | useReducer |
|---------|----------|------------|
| Basit state (boolean, string, number) | Tercih et | Gereksiz karmaşıklık |
| Birbirine bağlı state'ler | Birden fazla useState karışır | Tek reducer'da topla |
| Karmaşık state geçişleri | Setter fonksiyonlar karmaşıklaşır | switch/case ile okunabilir |
| Test edilebilirlik | Zor | Reducer pure function - kolayca test edilir |
| **Kural:** | 1-2 basit state | 3+ ilişkili state veya karmaşık geçişler |
:::

## useContext: Global State

Context API, prop drilling (derinlere prop geçirme) sorununu çözer. Tema, kullanıcı bilgisi, dil gibi verileri tüm component ağacında paylaşır.

:::code[tsx]{title="useContext - Provider Pattern"}
import { createContext, useContext, useReducer, ReactNode } from "react";

// 1. Tipleri tanımla
interface AuthState {
  user: { id: number; name: string; email: string } | null;
  isAuthenticated: boolean;
  loading: boolean;
}

type AuthAction =
  | { type: "LOGIN_SUCCESS"; payload: { id: number; name: string; email: string } }
  | { type: "LOGOUT" }
  | { type: "SET_LOADING"; payload: boolean };

interface AuthContextType {
  state: AuthState;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

// 2. Context oluştur
const AuthContext = createContext<AuthContextType | null>(null);

// 3. Reducer
function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case "LOGIN_SUCCESS":
      return { user: action.payload, isAuthenticated: true, loading: false };
    case "LOGOUT":
      return { user: null, isAuthenticated: false, loading: false };
    case "SET_LOADING":
      return { ...state, loading: action.payload };
    default:
      return state;
  }
}

// 4. Provider component
function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    isAuthenticated: false,
    loading: false,
  });

  const login = async (email: string, password: string) => {
    dispatch({ type: "SET_LOADING", payload: true });
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      const user = await res.json();
      dispatch({ type: "LOGIN_SUCCESS", payload: user });
    } catch {
      dispatch({ type: "SET_LOADING", payload: false });
    }
  };

  const logout = () => dispatch({ type: "LOGOUT" });

  return (
    <AuthContext.Provider value={{ state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// 5. Custom hook ile erişim (her seferinde null check yapmamak için)
function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

// 6. Kullanımı
function Navbar() {
  const { state, logout } = useAuth();

  return (
    <nav>
      {state.isAuthenticated ? (
        <>
          <span>Merhaba, {state.user?.name}</span>
          <button onClick={logout}>Çıkış Yap</button>
        </>
      ) : (
        <a href="/login">Giriş Yap</a>
      )}
    </nav>
  );
}

// App'te Provider ile sar
function App() {
  return (
    <AuthProvider>
      <Navbar />
      {/* Diğer component'ler */}
    </AuthProvider>
  );
}
:::

:::beginner-mistake
Yaygın hata: Context'i her şey için kullanmak. Context değiştiğinde, onu kullanan TÜM component'ler re-render olur. Sık değişen veriler (input değerleri, mouse pozisyonu) için Context uygun değildir. Bu durumlar için Zustand veya Jotai tercih et.
:::

## State Management Karşılaştırma

:::comparison
| Özellik | Context API | Zustand | Redux Toolkit | Jotai |
|---------|-------------|---------|---------------|-------|
| Boyut | 0 KB (built-in) | ~1 KB | ~11 KB | ~3 KB |
| Öğrenme eğrisi | Kolay | Çok kolay | Orta-zor | Kolay |
| Boilerplate | Orta | Minimal | Orta (eskiye göre az) | Minimal |
| DevTools | React DevTools | Kendi DevTools | Redux DevTools | Jotai DevTools |
| Re-render optimizasyonu | Zayıf (tüm consumer'lar) | Selector ile güçlü | Selector ile güçlü | Atom bazlı (güçlü) |
| **Ne zaman kullan** | Tema, dil, auth gibi nadir değişenler | Orta-büyük projeler, basit API | Büyük ekipler, karmaşık state | Atom bazlı state, React'e yakın |
| Async işlemler | Manuel | Kolay | createAsyncThunk | Kolay |

**Tavsiye:** Yeni projelerde **Zustand** ile başla. Basit, performanslı ve öğrenmesi kolay. Context API'yi sadece tema/auth gibi nadir değişen veriler için kullan.
:::

:::code[tsx]{title="Zustand - Modern State Management"}
import { create } from "zustand";

// Store tanımla (tek dosyada, basit)
interface CartStore {
  items: { id: number; name: string; price: number; quantity: number }[];
  totalItems: number;
  addItem: (item: { id: number; name: string; price: number }) => void;
  removeItem: (id: number) => void;
  clearCart: () => void;
}

const useCartStore = create<CartStore>((set, get) => ({
  items: [],
  totalItems: 0,

  addItem: (item) =>
    set((state) => {
      const existing = state.items.find((i) => i.id === item.id);
      if (existing) {
        return {
          items: state.items.map((i) =>
            i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
          ),
          totalItems: state.totalItems + 1,
        };
      }
      return {
        items: [...state.items, { ...item, quantity: 1 }],
        totalItems: state.totalItems + 1,
      };
    }),

  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((i) => i.id !== id),
      totalItems: state.items
        .filter((i) => i.id !== id)
        .reduce((sum, i) => sum + i.quantity, 0),
    })),

  clearCart: () => set({ items: [], totalItems: 0 }),
}));

// Kullanımı - herhangi bir component'te, Provider gerekmez!
function CartIcon() {
  const totalItems = useCartStore((state) => state.totalItems); // Selector: sadece bu değişince re-render
  return <span>Sepet ({totalItems})</span>;
}

function ProductCard({ product }: { product: { id: number; name: string; price: number } }) {
  const addItem = useCartStore((state) => state.addItem);
  return (
    <div>
      <h3>{product.name}</h3>
      <button onClick={() => addItem(product)}>Sepete Ekle</button>
    </div>
  );
}
:::

## React Router v6+

:::code[tsx]{title="React Router v6 - Nested Routes ve Navigation"}
import {
  createBrowserRouter,
  RouterProvider,
  Outlet,
  Link,
  NavLink,
  useParams,
  useNavigate,
  useSearchParams,
  useLoaderData,
} from "react-router-dom";

// Loader: Route yüklenmeden önce data fetch et
async function userLoader({ params }: { params: { userId: string } }) {
  const res = await fetch(`/api/users/${params.userId}`);
  if (!res.ok) throw new Response("User not found", { status: 404 });
  return res.json();
}

// Layout component
function RootLayout() {
  return (
    <div>
      <nav>
        <NavLink to="/" className={({ isActive }) => (isActive ? "active" : "")}>
          Ana Sayfa
        </NavLink>
        <NavLink to="/products">Ürünler</NavLink>
        <NavLink to="/about">Hakkında</NavLink>
      </nav>
      <main>
        <Outlet />  {/* Alt route'lar burada render olur */}
      </main>
    </div>
  );
}

// Sayfa component'leri
function Home() {
  return <h1>Ana Sayfa</h1>;
}

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();
  const category = searchParams.get("category") || "all";

  return (
    <div>
      <h1>Ürünler - {category}</h1>
      <button onClick={() => setSearchParams({ category: "electronics" })}>
        Elektronik
      </button>
      <Outlet />  {/* Nested route'lar */}
    </div>
  );
}

function ProductDetail() {
  const { productId } = useParams<{ productId: string }>();
  const navigate = useNavigate();

  return (
    <div>
      <h2>Ürün #{productId}</h2>
      <button onClick={() => navigate(-1)}>Geri Dön</button>
      <button onClick={() => navigate("/products")}>Ürünlere Dön</button>
    </div>
  );
}

function UserProfile() {
  const user = useLoaderData() as { id: number; name: string };
  return <h1>{user.name}</h1>;
}

// Router tanımı
const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <Home /> },
      {
        path: "products",
        element: <ProductList />,
        children: [
          { path: ":productId", element: <ProductDetail /> },
        ],
      },
      {
        path: "users/:userId",
        element: <UserProfile />,
        loader: userLoader,
      },
      { path: "about", element: <About /> },
    ],
  },
]);

// App
function App() {
  return <RouterProvider router={router} />;
}
:::

## Form Handling: React Hook Form + Zod

:::code[tsx]{title="React Hook Form + Zod Validation"}
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

// 1. Zod schema tanımla (validation kuralları)
const registerSchema = z
  .object({
    name: z
      .string()
      .min(2, "Ad en az 2 karakter olmalı")
      .max(50, "Ad en fazla 50 karakter olmalı"),
    email: z.string().email("Geçerli bir email adresi girin"),
    age: z
      .number({ invalid_type_error: "Yaş sayı olmalı" })
      .min(18, "18 yaşından büyük olmalısınız")
      .max(120, "Geçerli bir yaş girin"),
    password: z
      .string()
      .min(8, "Şifre en az 8 karakter olmalı")
      .regex(/[A-Z]/, "En az bir büyük harf içermeli")
      .regex(/[0-9]/, "En az bir rakam içermeli"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Şifreler eşleşmiyor",
    path: ["confirmPassword"],
  });

// Schema'dan TypeScript tipi çıkar
type RegisterFormData = z.infer<typeof registerSchema>;

function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: "",
      email: "",
      age: undefined,
      password: "",
      confirmPassword: "",
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    try {
      await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      reset();
      alert("Kayıt başarılı!");
    } catch {
      alert("Bir hata oluştu");
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <div>
        <label>Ad</label>
        <input {...register("name")} />
        {errors.name && <span className="error">{errors.name.message}</span>}
      </div>

      <div>
        <label>Email</label>
        <input type="email" {...register("email")} />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </div>

      <div>
        <label>Yaş</label>
        <input type="number" {...register("age", { valueAsNumber: true })} />
        {errors.age && <span className="error">{errors.age.message}</span>}
      </div>

      <div>
        <label>Şifre</label>
        <input type="password" {...register("password")} />
        {errors.password && <span className="error">{errors.password.message}</span>}
      </div>

      <div>
        <label>Şifre Tekrar</label>
        <input type="password" {...register("confirmPassword")} />
        {errors.confirmPassword && (
          <span className="error">{errors.confirmPassword.message}</span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Kaydediliyor..." : "Kayıt Ol"}
      </button>
    </form>
  );
}
:::

:::deha-tip
React Hook Form, controlled input yerine uncontrolled input yaklaşımı kullanır. Bu sayede her tuşa basışta re-render olmaz ve büyük formlarda performans çok daha iyi olur. Zod ile birlikte kullanıldığında, hem runtime validation hem de compile-time type safety sağlar - schema'dan TypeScript tipi otomatik çıkar.
:::

## Performance Optimizasyonu

:::code[tsx]{title="React.memo, Lazy Loading ve Suspense"}
import { memo, lazy, Suspense, useState, useCallback, useMemo } from "react";

// 1. React.memo: Props değişmedikçe re-render'ı engelle
interface ExpensiveListProps {
  items: string[];
  onItemClick: (item: string) => void;
}

const ExpensiveList = memo(function ExpensiveList({
  items,
  onItemClick,
}: ExpensiveListProps) {
  console.log("ExpensiveList render oldu");
  return (
    <ul>
      {items.map((item) => (
        <li key={item} onClick={() => onItemClick(item)}>
          {item}
        </li>
      ))}
    </ul>
  );
});

// 2. Parent'ta useCallback + useMemo ile referans sabitliği
function Dashboard() {
  const [query, setQuery] = useState("");
  const [selectedItems, setSelectedItems] = useState<string[]>([]);

  const allItems = ["React", "Vue", "Angular", "Svelte", "Next.js"];

  // useMemo: filteredItems sadece query veya allItems değişince yeniden hesaplanır
  const filteredItems = useMemo(
    () => allItems.filter((item) => item.toLowerCase().includes(query.toLowerCase())),
    [query]
  );

  // useCallback: handleClick referansı sabit kalır -> ExpensiveList gereksiz render olmaz
  const handleClick = useCallback((item: string) => {
    setSelectedItems((prev) => [...prev, item]);
  }, []);

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <ExpensiveList items={filteredItems} onItemClick={handleClick} />
    </div>
  );
}

// 3. Lazy loading + Suspense: Code splitting
const HeavyChart = lazy(() => import("./components/HeavyChart"));
const AdminPanel = lazy(() => import("./pages/AdminPanel"));

function App() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Grafiği Göster</button>

      {showChart && (
        <Suspense fallback={<div>Grafik yükleniyor...</div>}>
          <HeavyChart />
        </Suspense>
      )}

      <Suspense fallback={<div>Sayfa yükleniyor...</div>}>
        <AdminPanel />
      </Suspense>
    </div>
  );
}
:::

:::comparison
| Teknik | Ne Yapar | Ne Zaman Kullan |
|--------|----------|-----------------|
| React.memo | Props değişmedikçe re-render engeller | Ağır child component'ler |
| useMemo | Hesaplama sonucunu cache'ler | Ağır filtreleme/sıralama/dönüşüm |
| useCallback | Fonksiyon referansını sabit tutar | memo'lu child'a callback geçerken |
| lazy + Suspense | Component'i ayrı bundle'a ayırır | Büyük sayfalar, nadir kullanılan özellikler |
| React.startTransition | Düşük öncelikli güncelleme | Ağır arama/filtreleme |
| Virtualization | Sadece görünen elemanları render eder | 100+ elemanlı listeler |
:::

## React DevTools Kullanımı

:::tip
React DevTools, Chrome/Firefox extension olarak yüklenir. İki ana tab sunar:

1. **Components tab**: Component ağacını görüntüle, props ve state'i incele, değiştir
2. **Profiler tab**: Render performansını ölç, hangi component'in kaç kez neden render olduğunu gör

Profiler'da "Highlight updates when components render" seçeneğini aç. Sayfada bir şey yaptığında hangi component'lerin gereksiz render olduğunu görsel olarak takip edebilirsin. Sarı/kırmızı yanıp sönen kutular gereksiz re-render'ları gösterir.
:::

:::interview
**Mülakat Sorusu:** "React'te performans optimizasyonu nasıl yaparsınız?"

**Beklenen cevap:**
1. Önce Profiler ile problemi tespit et (premature optimization yapma)
2. Gereksiz re-render'ları React.memo ile engelle
3. useCallback/useMemo ile referans sabitliği sağla
4. Büyük component'leri lazy loading ile böl (code splitting)
5. Uzun listelerde virtualization kullan (react-window veya tanstack-virtual)
6. State'i mümkün olduğunca aşağıda tut (state colocation)
7. React 19 Compiler kullanıyorsan, manuel memo'ya çoğunlukla gerek yok
:::

:::knowledge-check
type: multiple_choice
question: "Zustand'ın Context API'ye göre en büyük avantajı nedir?"
options:
  - "Zustand daha büyük bir kütüphanedir"
  - "Zustand Provider gerektirmez"
  - "Zustand selector ile sadece kullanılan state değişince re-render tetikler"
  - "Zustand sadece TypeScript ile çalışır"
correct: 2
explanation: "Context API'de context değiştiğinde tüm consumer'lar re-render olur. Zustand'da ise selector kullanarak sadece ilgilendiğin state parçası değiştiğinde component re-render olur. Bu, büyük uygulamalarda ciddi performans avantajı sağlar."
:::

:::knowledge-check
type: multiple_choice
question: "React.memo ne zaman etkisizdir?"
options:
  - "Component'in props'u yoksa"
  - "Her render'da yeni bir obje/fonksiyon referansı props olarak geçilirse"
  - "Component bir hook kullanıyorsa"
  - "Component TypeScript ile yazılmışsa"
correct: 1
explanation: "React.memo shallow comparison yapar. Her render'da yeni obje ({ }) veya fonksiyon (() => {}) oluşturulursa, referanslar farklı olacağı için memo etkisiz kalır. Bu durumda useMemo ve useCallback ile referansları sabit tutmalısın."
:::

:::exercise
### Alistirma 1: useReducer ile Alisveris Sepeti (Kolay)

useReducer kullanarak bir alisveris sepeti uygulamasi yaz. Urun ekleme, cikarma, miktar guncelleme ve sepeti temizleme action'lari olmali.

```tsx
import { useReducer } from "react";

// State tipi
interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
}

// TODO: Action tiplerini tanimla (ADD_ITEM, REMOVE_ITEM, UPDATE_QUANTITY, CLEAR_CART)
type CartAction = // ...

// TODO: cartReducer fonksiyonunu yaz
function cartReducer(state: CartState, action: CartAction): CartState {
  // ...
}

// TODO: ShoppingCart component'ini yaz
// - Urunleri listele (isim, fiyat, miktar, toplam)
// - Her urunde +/- butonlari ve sil butonu
// - Sepeti temizle butonu
// - Genel toplam goster
```

**Beklenen Sonuc:** Sepete urun eklendiginde miktar artmali, ayni urun tekrar eklendiginde quantity artmali (duplicate olmamali). Toplam fiyat dogru hesaplanmali.
**Ipucu:** ADD_ITEM action'inda mevcut urunleri kontrol et, varsa quantity'yi artir.

---

### Alistirma 2: Context + useReducer ile Tema Yonetimi (Orta)

Context API ve useReducer birlestirerek bir tema yonetim sistemi olustur. light/dark tema degisimi, custom renk paleti ve font boyutu ayarlari olmali.

```tsx
import { createContext, useContext, useReducer, ReactNode } from "react";

interface ThemeState {
  mode: "light" | "dark";
  primaryColor: string;
  fontSize: "small" | "medium" | "large";
}

// TODO: ThemeAction tiplerini tanimla
// - TOGGLE_MODE: light <-> dark
// - SET_PRIMARY_COLOR: renk degistir
// - SET_FONT_SIZE: font boyutu degistir
// - RESET: varsayilana don

// TODO: ThemeContext olustur
// TODO: ThemeProvider component'i yaz (useReducer ile)
// TODO: useTheme custom hook yaz (null check ile)

// TODO: ThemeDemo component'i yaz:
// - Mevcut tema bilgisini goster
// - Tema toggle butonu
// - Renk secici (3-4 secenekli butonlar)
// - Font boyutu secici
// - Tum ayarlari sifirla butonu
// - Arka plan ve yazi rengi temaya gore degismeli
```

**Beklenen Sonuc:** Tema degisiklikleri tum component agacinda aninda yansimali. Provider disinda useTheme kullanildiginda hata firlatmali.
**Ipucu:** CSS variable'lari veya inline style ile tema renklerini uygula.

---

### Alistirma 3: Zustand + React Hook Form + Zod Entegrasyonu (Zor)

Zustand store ile global state yonetimi, React Hook Form ile form handling ve Zod ile validation birlestirerek bir "Kullanici Profil Yonetim" uygulamasi yap.

```tsx
import { create } from "zustand";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

// 1. Zod schema
const profileSchema = z.object({
  displayName: z.string().min(2, "En az 2 karakter").max(30),
  email: z.string().email("Gecerli email girin"),
  bio: z.string().max(200, "En fazla 200 karakter").optional(),
  website: z.string().url("Gecerli URL girin").optional().or(z.literal("")),
  notifications: z.object({
    email: z.boolean(),
    push: z.boolean(),
    sms: z.boolean(),
  }),
});

type ProfileFormData = z.infer<typeof profileSchema>;

// TODO: Zustand store olustur
// - user: ProfileFormData | null
// - isEditing: boolean
// - updateProfile: (data: ProfileFormData) => void
// - toggleEditing: () => void
// - history: ProfileFormData[] (onceki profilleri tut)
// - undo: () => void (son degisikligi geri al)

// TODO: ProfilePage component'i yaz:
// - Profili goruntuleme modu (isEditing=false)
// - Profili duzenleme modu (React Hook Form + Zod validation)
// - Kaydet butonunda Zustand store'u guncelle
// - Geri al (undo) butonu
// - Zustand selector ile sadece gerekli state'i kullan (gereksiz re-render onle)
```

**Beklenen Sonuc:** Form validation hatalari aninda gosterilmeli. Profil guncellemesi store'a kaydedilmeli. Undo ile önceki profil geri yuklenebilmeli. Selector kullanarak CartIcon gibi bagimsiz component'ler gereksiz re-render olmamali.
**Ipucu:** Zustand'da `persist` middleware ile localStorage'a kaydetmeyi dene.
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "Context API'de neden context degistiginde TUM consumer'lar re-render oluyor? Bu sorunu Zustand selector pattern'i nasil cozuyor? React internal'da useSyncExternalStore hook'u Zustand'da nasil kullaniliyor? Zustand'in source code'undaki temel mekanizmayi acikla."

**2. Pratik Uygulama:**
> "Zustand ile bir e-ticaret sepet yonetim sistemi kur. Urun ekleme, cikarma, miktar guncelleme, toplam fiyat hesaplama ve sepeti temizleme islevleri olsun. Persist middleware ile localStorage'a kaydet. Selector pattern ile gereksiz re-render'lari onle. TypeScript tipleri ile yaz."
> Takip: "Simdi React Hook Form + Zod ile bir adres formu ekle ve form submit'te sepet verisiyle birlikte API'ye gonder. Optimistic update uygula."

**3. Mukemmellik Icin:**
> "50+ developer'lik bir takimda state management stratejisi tasarliyorum. Hangi state nerede tutulmali (local, lifted, context, Zustand, URL)? State colocation prensibini, derived state anti-pattern'ini ve state machine yaklasimini (XState) karsilastir. Gercek bir SaaS urununde state mimarisini nasil planlarim?"

### Pair Programming Ipucu
Performance sorunlarinda AI'a component kodunu ve Profiler ciktisini ver: "Bu Dashboard component'inde 3 farkli Zustand store'dan veri cekiyorum ama her state degisiminde tum component re-render oluyor. Selector'larimi ve component yapisini optimize et."
:::

:::exercise
### Alıştırma 4: useReducer ile Alışveriş Sepeti
**Görev:** useReducer kullanarak bir alışveriş sepeti yönetimi yaz: ürün ekle, çıkar, miktar güncelle.
**Başlangıç kodu:**
```tsx
interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

type CartAction =
  | { type: "ADD_ITEM"; payload: Omit<CartItem, "quantity"> }
  | { type: "REMOVE_ITEM"; payload: { id: number } }
  | { type: "UPDATE_QUANTITY"; payload: { id: number; quantity: number } }
  | { type: "CLEAR_CART" };

// TODO: cartReducer fonksiyonunu yaz
function cartReducer(state: CartItem[], action: CartAction): CartItem[] {
  switch (action.type) {
    case "ADD_ITEM":
      // Ürün zaten varsa quantity artır, yoksa yeni ekle
    case "REMOVE_ITEM":
      // id'ye göre filtrele
    case "UPDATE_QUANTITY":
      // quantity 0 ise sil, değilse güncelle
    case "CLEAR_CART":
      // Boş array döndür
  }
}
```
**Beklenen çıktı:**
```tsx
case "ADD_ITEM": {
  const existing = state.find(item => item.id === action.payload.id);
  if (existing) {
    return state.map(item =>
      item.id === action.payload.id
        ? { ...item, quantity: item.quantity + 1 }
        : item
    );
  }
  return [...state, { ...action.payload, quantity: 1 }];
}
case "REMOVE_ITEM":
  return state.filter(item => item.id !== action.payload.id);
case "UPDATE_QUANTITY":
  if (action.payload.quantity <= 0) {
    return state.filter(item => item.id !== action.payload.id);
  }
  return state.map(item =>
    item.id === action.payload.id
      ? { ...item, quantity: action.payload.quantity }
      : item
  );
case "CLEAR_CART":
  return [];
```
**İpucu:** Reducer pure function olmalı - state'i doğrudan değiştirme, her zaman yeni array/obje döndür. `Omit<CartItem, "quantity">` ile quantity dışındaki alanları al.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 5: Context API ile Tema Provider
**Görev:** Context API ile uygulamanın her yerinden erişilebilir bir tema sistemi oluştur.
**Başlangıç kodu:**
```tsx
import { createContext, useContext, useState, ReactNode } from "react";

// TODO: ThemeContext tipini tanımla
interface ThemeContextType {
  theme: "light" | "dark";
  toggleTheme: () => void;
}

// TODO: Context oluştur (varsayılan değer null)

// TODO: ThemeProvider component'i yaz
function ThemeProvider({ children }: { children: ReactNode }) {
  // TODO: theme state'i
  // TODO: toggleTheme fonksiyonu
  // TODO: Context.Provider ile children'ı sar
}

// TODO: useTheme custom hook'u yaz (context null kontrolü ile)

// Kullanım:
function Header() {
  const { theme, toggleTheme } = useTheme();
  return (
    <header className={theme === "dark" ? "bg-gray-900" : "bg-white"}>
      <button onClick={toggleTheme}>Tema Değiştir</button>
    </header>
  );
}
```
**Beklenen çıktı:**
```tsx
const ThemeContext = createContext<ThemeContextType | null>(null);

function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<"light" | "dark">("dark");
  const toggleTheme = () => setTheme(prev => prev === "dark" ? "light" : "dark");

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme must be used within ThemeProvider");
  return context;
}
```
**İpucu:** Context null kontrolü yapan custom hook yaz - bu hem tip güvenliği sağlar hem de Provider olmadan kullanmayı engeller.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: React Router ile Sayfa Navigasyonu
**Görev:** React Router v6 ile temel bir sayfa yapısı kur: layout, nested routes ve dynamic route parametresi.
**Başlangıç kodu:**
```tsx
import { BrowserRouter, Routes, Route, Link, Outlet, useParams } from "react-router-dom";

// TODO: Layout component - Navbar + Outlet
function Layout() {
  return (
    <div>
      <nav>
        {/* TODO: Link component'leri ile navigasyon */}
      </nav>
      {/* TODO: Alt route'ların render edileceği yer */}
    </div>
  );
}

// TODO: ProductDetail - URL'den id parametresini al
function ProductDetail() {
  // TODO: useParams ile id'yi al
  return <h1>Ürün #{/* id */}</h1>;
}

// TODO: Route yapısını kur
function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* TODO: Layout içinde nested routes
            /          → HomePage
            /products  → ProductList
            /products/:id → ProductDetail
            *          → NotFound */}
      </Routes>
    </BrowserRouter>
  );
}
```
**Beklenen çıktı:**
```tsx
function Layout() {
  return (
    <div>
      <nav>
        <Link to="/">Ana Sayfa</Link>
        <Link to="/products">Ürünler</Link>
      </nav>
      <Outlet />
    </div>
  );
}

function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  return <h1>Ürün #{id}</h1>;
}

<Routes>
  <Route path="/" element={<Layout />}>
    <Route index element={<HomePage />} />
    <Route path="products" element={<ProductList />} />
    <Route path="products/:id" element={<ProductDetail />} />
    <Route path="*" element={<NotFound />} />
  </Route>
</Routes>
```
**İpucu:** `<Outlet />` nested route'ların render edildiği yerdir. `useParams` ile URL parametrelerini oku. `index` route parent path'te gösterilir.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: React Hook Form ile Kayıt Formu
**Görev:** React Hook Form ve Zod ile doğrulamalı bir kayıt formu oluştur.
**Başlangıç kodu:**
```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

// TODO: Zod schema tanımla
const registerSchema = z.object({
  // name: min 2 karakter
  // email: geçerli email
  // password: min 8 karakter, en az 1 büyük harf, 1 rakam
  // confirmPassword: password ile aynı olmalı
}).refine(/* TODO: password eşleşme kontrolü */);

type RegisterForm = z.infer<typeof registerSchema>;

function RegisterPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = (data: RegisterForm) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* TODO: Her alan için input + hata mesajı */}
    </form>
  );
}
```
**Beklenen çıktı:**
```tsx
const registerSchema = z.object({
  name: z.string().min(2, "Ad en az 2 karakter olmalı"),
  email: z.string().email("Geçerli bir email girin"),
  password: z.string()
    .min(8, "Şifre en az 8 karakter olmalı")
    .regex(/[A-Z]/, "En az 1 büyük harf")
    .regex(/[0-9]/, "En az 1 rakam"),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Şifreler eşleşmiyor",
  path: ["confirmPassword"],
});
```
**İpucu:** `z.infer<typeof schema>` ile Zod schema'dan TypeScript tipi çıkarılır. `.refine()` ile cross-field validation yapılır.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Zustand ile Global State
**Görev:** Zustand kullanarak bir bildirim (notification) store'u oluştur.
**Başlangıç kodu:**
```tsx
import { create } from "zustand";

interface Notification {
  id: string;
  message: string;
  type: "success" | "error" | "info";
}

// TODO: NotificationStore interface
interface NotificationStore {
  notifications: Notification[];
  addNotification: (message: string, type: Notification["type"]) => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
}

// TODO: Zustand store oluştur
const useNotificationStore = create<NotificationStore>((set) => ({
  // TODO: notifications başlangıç değeri
  // TODO: addNotification - benzersiz id ile ekle
  // TODO: removeNotification - id'ye göre sil
  // TODO: clearAll - hepsini temizle
}));

// TODO: 3 saniye sonra otomatik kaldıran addNotification yaz
```
**Beklenen çıktı:**
```tsx
const useNotificationStore = create<NotificationStore>((set) => ({
  notifications: [],
  addNotification: (message, type) => {
    const id = crypto.randomUUID();
    set(state => ({
      notifications: [...state.notifications, { id, message, type }],
    }));
    setTimeout(() => {
      set(state => ({
        notifications: state.notifications.filter(n => n.id !== id),
      }));
    }, 3000);
  },
  removeNotification: (id) =>
    set(state => ({
      notifications: state.notifications.filter(n => n.id !== id),
    })),
  clearAll: () => set({ notifications: [] }),
}));
```
**İpucu:** `set(state => ...)` ile mevcut state'e göre güncelleme yap. `crypto.randomUUID()` benzersiz id üretir.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: React.memo ile Gereksiz Render Engelleme
**Görev:** Gereksiz re-render'ları tespit et ve `React.memo` ile optimize et.
**Başlangıç kodu:**
```tsx
import { useState, memo, useCallback } from "react";

// TODO: Bu component her parent render'da yeniden render oluyor
// React.memo ile sararak sadece props değişince render edilmesini sağla
function ExpensiveList({ items, onItemClick }: {
  items: string[];
  onItemClick: (item: string) => void;
}) {
  console.log("ExpensiveList rendered!");
  return (
    <ul>
      {items.map(item => (
        <li key={item} onClick={() => onItemClick(item)}>{item}</li>
      ))}
    </ul>
  );
}

function Parent() {
  const [count, setCount] = useState(0);
  const [items] = useState(["a", "b", "c"]);

  // TODO: Bu fonksiyon her render'da yeniden oluşuyor
  // useCallback ile memoize et
  const handleItemClick = (item: string) => {
    console.log("Clicked:", item);
  };

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>
      <ExpensiveList items={items} onItemClick={handleItemClick} />
    </div>
  );
}
```
**Beklenen çıktı:**
```tsx
const ExpensiveList = memo(function ExpensiveList({ items, onItemClick }: {
  items: string[];
  onItemClick: (item: string) => void;
}) {
  console.log("ExpensiveList rendered!");
  return (
    <ul>
      {items.map(item => (
        <li key={item} onClick={() => onItemClick(item)}>{item}</li>
      ))}
    </ul>
  );
});

// Parent içinde:
const handleItemClick = useCallback((item: string) => {
  console.log("Clicked:", item);
}, []);
```
**İpucu:** `React.memo` props referansı değişmediyse render'ı atlar. Ama fonksiyon prop'lar her render'da yeni referans olur - `useCallback` ile stabilize et.
**Zorluk:** Zor
:::

:::exercise
### Alıştırma 10: State Colocation Prensibi
**Görev:** Aşağıdaki kodda state'leri doğru yere taşıyarak refactor et. Her state mümkün olan en yakın component'te olmalı.
**Başlangıç kodu:**
```tsx
// YANLIŞ: Tüm state en üstte
function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState(0);
  const [formName, setFormName] = useState("");
  const [formEmail, setFormEmail] = useState("");
  const [tooltipVisible, setTooltipVisible] = useState(false);

  return (
    <div>
      <SearchBar query={searchQuery} setQuery={setSearchQuery} />
      <TabPanel selectedTab={selectedTab} setSelectedTab={setSelectedTab} />
      <ContactForm name={formName} setName={setFormName}
                   email={formEmail} setEmail={setFormEmail} />
      <Tooltip visible={tooltipVisible} setVisible={setTooltipVisible} />
      <Modal isOpen={isModalOpen} setIsOpen={setIsModalOpen} />
    </div>
  );
}
```
**Beklenen çıktı:**
```tsx
// DOĞRU: Her state kendi component'inde
function App() {
  return (
    <div>
      <SearchBar />      {/* searchQuery state'i SearchBar içinde */}
      <TabPanel />       {/* selectedTab state'i TabPanel içinde */}
      <ContactForm />    {/* formName, formEmail state'i ContactForm içinde */}
      <Tooltip />        {/* tooltipVisible state'i Tooltip içinde */}
      <Modal />          {/* isModalOpen state'i Modal içinde */}
    </div>
  );
}

// Sadece birden fazla component aynı state'i kullanıyorsa yukarı kaldır (lift state up)
```
**İpucu:** State colocation = state'i kullanan en yakın component'te tut. Gereksiz prop drilling'i önler ve performance artırır. Sadece paylaşılan state yukarı taşınır.
**Zorluk:** Kolay
:::

:::must-note
- useReducer: 3+ ilişkili state varsa veya state geçişleri karmaşıksa useState yerine kullan
- Reducer = pure function: (state, action) => newState, yan etkisi olmamalı
- Action type'ları: discriminated union ile TypeScript'te tip güvenliği sağla
- Context API: prop drilling çözer ama değişen context TÜM consumer'ları re-render eder
- Context + useReducer = mini Redux (auth, tema gibi nadir değişen veriler için uygun)
- Custom hook (useAuth) ile context erişimini sarmalayarak null check'i tek yerde yap
- Zustand: selector ile granüler re-render, Provider gerektirmez, ~1KB, yeni projeler için tavsiye
- Redux Toolkit: büyük ekipler ve karmaşık state için, DevTools güçlü, boilerplate azaldı
- React Router v6: createBrowserRouter, Outlet (nested), useParams, useNavigate, loader ile data fetch
- NavLink: isActive prop ile aktif link styling, useSearchParams ile query parametreleri
- React Hook Form: uncontrolled yaklaşım (performanslı), Zod ile schema-based validation
- z.infer<typeof schema> ile schema'dan TypeScript tipi otomatik çıkar
- React.memo: shallow comparison ile props değişmedikçe re-render engeller
- React.memo + useCallback + useMemo = referans sabitliği üçlüsü
- lazy() + Suspense: code splitting, büyük component'leri ayrı bundle'a ayır
- Profiler ile önce problemi tespit et, sonra optimize et (premature optimization yapma)
- State colocation: state'i mümkün olduğunca kullanıldığı yere yakın tut
:::

:::senior-learns
Bir Senior Developer veya CTO, state patterns ve performance konusunu öğrenirken şu yaklaşımı benimser:

1. **State mimarisini proje başında tasarlar** - Hangi state nerede tutulacak (local, lifted, context, external store) kararını component yapısını çizmeden önce verir. State colocation prensibini uygular: state'i kullanan en yakın ortak ataya koy.
2. **Re-render maliyetini ölçerek optimize eder** - "Hissettim" yerine Profiler verisiyle kanıtlar. React DevTools'un "Why did this render?" özelliğini aktif kullanır. Her optimizasyon bir trade-off'tur: kod karmaşıklığı vs performans kazanımı.
3. **State management kütüphanesi seçimini proje büyüklüğüne göre yapar** - 5 sayfalık bir proje için Redux kurmaz. Zustand veya Jotai ile başlar, ihtiyaç büyüdükçe geçiş yapar.
4. **Form validation'ı backend ile senkronize tutar** - Zod schema'yı backend ile paylaşır (monorepo'da shared package). Frontend ve backend aynı validation kurallarını kullanır.
5. **Routing stratejisini SEO ve UX'e göre belirler** - SPA routing mi, SSR routing mi? Prefetching ne zaman yapılmalı? Code splitting stratejisi nasıl olmalı? Bu kararları data ile verir.
6. **Performance budget koyar** - "Bu sayfa 3 saniyeden fazla yüklenmemeli" gibi metrikler belirler. Lighthouse CI ile her PR'da otomatik ölçüm yapar.

**Karar Verme Sureci — State Nerede Tutulmali?**
- **URL state (searchParams)**: Filtreleme, siralama, sayfalama gibi paylasılabilir olması gereken state. Trade-off: string parse/serialize maliyeti var ama kullanıcı URL'yi paylaşabilir, back button çalışır. Production'da en çok unutulan state türü.
- **Local state (useState)**: Sadece o component'te kullanılan, form input'ları, toggle'lar. Trade-off: basit ama prop drilling başlarsa kırılgan.
- **Lifted state**: İki kardeş component paylaşıyorsa parent'a taşı. Trade-off: parent gereksiz re-render olabilir, ama basit durumlar için yeterli.
- **Context**: Auth, tema, locale gibi nadir değişen global veriler. Trade-off: context değişince TÜM consumer'lar re-render olur.
- **External store (Zustand/Jotai)**: Sık değişen, birden fazla yerde kullanılan veriler. Trade-off: dependency ekleniyor ama selector ile granüler re-render sağlar.
- **Server state (TanStack Query)**: API'den gelen veriler. Trade-off: cache invalidation karmaşıklığı ama stale-while-revalidate ile mükemmel UX.

**Anti-pattern Farkindaligi:**
- **"Her şeyi global store'a koy" anti-pattern'i**: Redux/Zustand store 200+ field, her component tüm store'u dinliyor. Production'da gördüm: bir input'a her harf yazıldığında 47 component re-render oluyordu. Çözüm: state colocation.
- **Premature optimization**: 50 elemanlı bir liste için virtualization eklemek, 3 state'li bir form için useReducer kullanmak. React DevTools Profiler ile önce ölç, sonra optimize et.
- **Derived state'i ayrı state olarak tutmak**: `items` ve `itemCount` ayrı useState. items değişince itemCount'u güncelemeyi unutursun. Çözüm: `const itemCount = items.length` — derive et, store'lama.

**Gercek Dunya Deneyimi:** Bir SaaS dashboard projesinde başlangıçta tüm state'i Context'e koyduk. 30+ component, 15+ context provider, her state değişiminde tüm sayfa titriyordu. Lighthouse performance skoru 35'e düştü. Zustand'a geçiş yaptık, selector pattern ile sadece ilgili component'ler re-render oluyor. Skor 92'ye çıktı. Ders: doğru state mimarisini baştan kur, sonra değiştirmek çok pahalı.

**Profesyonel Mindset:** "State management'ta en iyi araç, en az aracı kullanmaktır. useState yetiyorsa useReducer kullanma. Context yetiyorsa Zustand ekleme. Her eklenen soyutlama katmanı, ekibin anlaması gereken bir kavram daha demektir. Basitlik, sürdürülebilirliğin temelidir."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Reducer** (rɪ-djuː-sər) → İndirgeyici
   *"The reducer function takes the current state and an action, then returns the new state."*

2. **Provider** (prə-vaɪ-dər) → Sağlayıcı
   *"Wrap your app with the AuthProvider to make authentication state available everywhere."*

3. **Memoization** (mem-oh-ɪ-zeɪ-ʃən) → Sonuçları hafızaya alma
   *"React.memo uses memoization to skip re-rendering when props haven't changed."*

4. **Code Splitting** (kohd splɪt-ɪŋ) → Kod bölme
   *"Lazy loading enables code splitting, which reduces the initial bundle size."*

5. **Selector** (sɪ-lek-tər) → Seçici
   *"Use a selector to subscribe to only the part of the store you need."*

**Okuma Egzersizi:** Zustand GitHub README'sini İngilizce oku: https://github.com/pmndrs/zustand

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Zustand ile sepet state management'ı eklendi"
-> Örnek: `feat: add cart state management with Zustand`
:::

:::external-resource
- React Docs - Managing State: https://react.dev/learn/managing-state
- Zustand GitHub: https://github.com/pmndrs/zustand
- React Router Docs: https://reactrouter.com
- React Hook Form Docs: https://react-hook-form.com
- Zod Docs: https://zod.dev
- Kent C. Dodds: "When to useMemo and useCallback": https://kentcdodds.com/blog/usememo-and-usecallback
:::
