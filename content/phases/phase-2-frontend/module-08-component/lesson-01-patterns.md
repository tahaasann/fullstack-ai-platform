---
title: "Component Architecture & Design Patterns"
id: "mod-08-api/lesson-01"
estimated_minutes: 50
order: 1
tags: ["component-patterns", "atomic-design", "hoc", "render-props", "composition"]
prerequisites: ["mod-07/lesson-01"]
---

# Component Architecture & Design Patterns

:::realworld
Bir startup'ta tek başına geliştirici olarak çalışırken 20-30 component yeterli olabilir. Ama büyük bir SaaS ürününde 500+ component ile çalışırsın. Bu noktada doğru mimari olmadan proje bir spagetti koduna döner. Her yeni özellik eklediğinde 10 farklı dosyayı değiştirmek zorunda kalırsın. Bu derste, dünyanın en büyük şirketlerinin (Airbnb, Shopify, Meta) kullandığı component pattern'larını öğreneceksin. Mülakatlarda "Component mimarinizi nasıl tasarlarsınız?" sorusuna profesyonel cevap verebilecek seviyeye geleceksin.
:::

## Neden Component Architecture Önemlidir?

Modern frontend uygulamalarında her şey component'tir. Bir buton, bir form, bir sayfa hepsi component. Ama component'leri nasıl organize ettiğin, nasıl birleştirdiğin ve nasıl iletişim kurdurdugun uygulamanın başarısını belirler.

Yanlış mimari ile:

- Aynı kodu 15 farklı yerde tekrarlarsın (DRY ihlali)
- Bir component'i değiştirdiğinde beklenmedik yerler kırılır
- Yeni takım üyesi projeyi anlamak için haftalarca uğraşır
- Test yazmak imkansız hale gelir
- Performance sorunları ortaya çıkar (gereksiz re-render)

:::deha-tip
Deha seviyesi geliştiriciler component tasarlarken şu soruyu sorar: "Bu component'i 6 ay sonra ilk kez görecek bir geliştirici kolayca anlayabilir mi?" Kod yazmak kolay, okunabilir kod yazmak zordur. Component API'si ne kadar açık ve tutarlıysa, takım o kadar hızlı hareket eder.
:::

## Atomic Design: Sistematik Component Hiyerarşisi

:::concept[Atomic Design (Ing: Atomic Design)]
Atomic Design, Brad Frost tarafından oluşturulan bir UI tasarım metodolojisidir. Kimyadaki atom-molekul benzetmesinden yola çıkarak, UI component'lerini 5 seviyeye ayırır.

**Türkçe karşılığı:** Atomik Tasarım
**Ne ise yarar:** Component'leri mantıksal bir hiyerarşiye oturtur, tutarlı ve ölçeklenebilir UI sistemleri oluşturmayı sağlar
**Gerçek hayat benzetmesi:** Lego parçaları gibi düşün - küçük parçalar (atoms) birleşiyor, daha büyük yapılar oluşuyor
:::

### 1. Atoms (Atomlar)

En küçük, bölünemeyen UI birimleridir. Tek başına bir anlam ifade etmeyebilirler ama sistemin temel yapı taşlarını oluştururlar.

:::code[jsx]{title="Atom Örnekleri"}
// Button Atom
function Button({ variant = "primary", size = "md", children, ...props }) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      {...props}
    >
      {children}
    </button>
  );
}

// Input Atom
function Input({ label, error, ...props }) {
  return (
    <div className="input-wrapper">
      {label && <label>{label}</label>}
      <input {...props} />
      {error && <span className="error">{error}</span>}
    </div>
  );
}

// Avatar Atom
function Avatar({ src, alt, size = 40 }) {
  return (
    <img
      src={src}
      alt={alt}
      width={size}
      height={size}
      className="avatar"
    />
  );
}
:::

### 2. Molecules (Moleküller)

Birden fazla atom'un bir araya gelerek anlamlı bir birim oluşturduğu yapidir.

:::code[jsx]{title="Molecule Örnekleri"}
// SearchBar Molecule (Input atom + Button atom)
function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  return (
    <div className="search-bar">
      <Input
        placeholder="Ara..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button onClick={() => onSearch(query)}>
        Ara
      </Button>
    </div>
  );
}

// UserCard Molecule (Avatar atom + Text atoms)
function UserCard({ user }) {
  return (
    <div className="user-card">
      <Avatar src={user.avatar} alt={user.name} />
      <div>
        <h4>{user.name}</h4>
        <span>{user.role}</span>
      </div>
    </div>
  );
}
:::

### 3. Organisms (Organizmalar)

Moleküller ve atomların birleşimiyle oluşan karmaşık UI bloklarıdır. Kendi başına bir anlam taşır.

:::code[jsx]{title="Organism Örneği"}
// Header Organism
function Header({ user, onSearch, onLogout }) {
  return (
    <header className="header">
      <Logo />
      <Navigation items={navItems} />
      <SearchBar onSearch={onSearch} />
      <UserCard user={user} />
      <Button variant="ghost" onClick={onLogout}>
        Cikis
      </Button>
    </header>
  );
}
:::

### 4. Templates (Şablonlar)

Sayfa düzeni ve yerleşim tanımlar. Gerçek veri yerine placeholder kullanir.

### 5. Pages (Sayfalar)

Template'lere gerçek verinin enjekte edildiği son haldir.

:::beginner-mistake
Yaygın hata: "Her component mutlaka Atomic Design'a uymalı" diye düşünmek. Atomic Design bir rehberdir, katı bir kural değil. Küçük projelerde atoms/molecules/pages yeterli olabilir. Önemli olan tutarlılık ve takım ici anlaşmadır.
:::

## Presentational vs Container Components

:::concept[Presentational Component (Ing: Presentational Component)]
Presentational component yalnızca görüntülemeden sorumludur. Veriyi props ile alir, işlem yapmaz, sadece render eder.

**Türkçe karşılığı:** Sunum Componenti
**Ne ise yarar:** UI ve is mantığını ayırır, test ve yeniden kullanimi kolaylaştırır
**Gerçek hayat benzetmesi:** Bir vitrin mankeni gibi - kendisi hareket etmez, sadece üzerine konulanı gösterir
:::

:::code[jsx]{title="Presentational vs Container"}
// Presentational Component - SADECE gosterim
function UserList({ users, onDelete }) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>
          {user.name}
          <button onClick={() => onDelete(user.id)}>Sil</button>
        </li>
      ))}
    </ul>
  );
}

// Container Component - is mantigi + veri yonetimi
function UserListContainer() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers().then(data => {
      setUsers(data);
      setLoading(false);
    });
  }, []);

  const handleDelete = async (id) => {
    await deleteUser(id);
    setUsers(prev => prev.filter(u => u.id !== id));
  };

  if (loading) return <Spinner />;
  return <UserList users={users} onDelete={handleDelete} />;
}
:::

:::tip
Modern React'te (hooks sonrası) container/presentational ayrımı eskisi kadar katı uygulanmıyor. Custom hook'lar is mantığını component dışına çıkararak aynı amaci daha esnek şekilde karşılar. Yine de kavram olarak bu ayrımı bilmek önemlidir.
:::

## Compound Components Pattern

:::concept[Compound Components (Ing: Compound Components)]
Birbirine bağımlı component'lerin bir parent altında birlikte çalışma pattern'idir. HTML'deki select/option ilişkisine benzer.

**Türkçe karşılığı:** Bileşik Componentler
**Ne ise yarar:** Esnek API sunarken component'ler arasi iletişimi yönetir
**Gerçek hayat benzetmesi:** Bir saat mekanizması - her dişli bağımsız görünür ama birlikte çalışarak anlam üretir
:::

:::code[jsx]{title="Compound Components Pattern"}
// Context ile Compound Components
const TabsContext = createContext();

function Tabs({ children, defaultTab }) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabList({ children }) {
  return <div className="tab-list" role="tablist">{children}</div>;
};

Tabs.Tab = function Tab({ value, children }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  return (
    <button
      role="tab"
      className={activeTab === value ? "active" : ""}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function TabPanel({ value, children }) {
  const { activeTab } = useContext(TabsContext);
  if (activeTab !== value) return null;
  return <div role="tabpanel">{children}</div>;
};

// Kullanim - cok temiz API
<Tabs defaultTab="genel">
  <Tabs.List>
    <Tabs.Tab value="genel">Genel</Tabs.Tab>
    <Tabs.Tab value="güvenlik">Güvenlik</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="genel">Genel ayarlar...</Tabs.Panel>
  <Tabs.Panel value="güvenlik">Güvenlik ayarlari...</Tabs.Panel>
</Tabs>
:::

## Render Props Pattern

:::concept[Render Props (Ing: Render Props)]
Bir component'e render fonksiyonu geçirerek, içeriğinin nasıl render edilecegini dışarıdan kontrol etme pattern'idir.

**Türkçe karşılığı:** Render Fonksiyon Geçirme
**Ne ise yarar:** Aynı is mantığıni farklı görünümlerle paylaşmayı sağlar
**Gerçek hayat benzetmesi:** Bir çerçeve (frame) gibi - çerçeve sabittir ama içine farklı resimler koyabilirsin
:::

:::code[jsx]{title="Render Props Pattern"}
// Mouse pozisyonunu takip eden component
function MouseTracker({ render }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMove = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, []);

  return render(position);
}

// Farkli gorunumlerle kullanim
<MouseTracker render={({ x, y }) => (
  <div>Fare pozisyonu: {x}, {y}</div>
)} />

<MouseTracker render={({ x, y }) => (
  <div
    className="cursor-dot"
    style={{ left: x, top: y, position: "fixed" }}
  />
)} />
:::

:::tip
Render props pattern'i modern React'te çoğunlukla custom hook'lar ile değiştirilmiştir. Ancak bazı kütüphaneler (örneğin React Router'in eski versiyonları, Formik) hala bu pattern'i kullanir. Mülakatlarda bilmen beklenir.
:::

## Higher-Order Components (HOC)

:::concept[Higher-Order Component / HOC (Ing: Higher-Order Component)]
Bir component alip, onu ek özelliklerle saran ve yeni bir component döndüren fonksiyondur.

**Türkçe karşılığı:** Ust-Düzey Component
**Ne ise yarar:** Cross-cutting concern'leri (auth, logging, theming) birden fazla component'e ekler
**Gerçek hayat benzetmesi:** Hediye paketi gibi - içindeki hediye ne olursa olsun, dışına sueslu kagit sarip kurdele takabilirsin
:::

:::code[jsx]{title="HOC Pattern"}
// Authentication HOC
function withAuth(WrappedComponent) {
  return function AuthenticatedComponent(props) {
    const { user, loading } = useAuth();

    if (loading) return <Spinner />;
    if (!user) return <Navigate to="/login" />;

    return <WrappedComponent {...props} user={user} />;
  };
}

// Loading state HOC
function withLoading(WrappedComponent) {
  return function LoadingComponent({ isLoading, ...props }) {
    if (isLoading) return <Spinner />;
    return <WrappedComponent {...props} />;
  };
}

// Kullanim
const ProtectedDashboard = withAuth(Dashboard);
const UserListWithLoading = withLoading(UserList);
:::

:::beginner-mistake
Yaygın hata: HOC'ları render metodu içinde oluşturmak. Bu her render'da yeni component oluşturur ve tüm state'i kaybettirir. HOC'lar her zaman component DIŞINDA tanımlanmalıdır.

```jsx
// YANLIS - her renderda yeni component olusur
function App() {
  const Enhanced = withAuth(Dashboard); // BUG!
  return <Enhanced />;
}

// DOGRU - component disinda tanimla
const Enhanced = withAuth(Dashboard);
function App() {
  return <Enhanced />;
}
```
:::

## Error Boundaries

:::concept[Error Boundary (Ing: Error Boundary)]
React component ağacında olası hataları yakalayan ve uygulamanın tamamen çökmesini önleyen özel component'tir.

**Türkçe karşılığı:** Hata Sınırı
**Ne ise yarar:** Bir component hata verse bile uygulamanın geri kalanı çalışmaya devam eder
**Gerçek hayat benzetmesi:** Sigortalar gibi - bir devrede kısa devre olursa sadece o sigortanın bağlı olduğu kısım etkilenir, evin elektrik sistemi çökmez
:::

:::code[jsx]{title="Error Boundary Implementasyonu"}
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Hata raporlama servisine gonder (Sentry, LogRocket vb.)
    console.error("Error caught by boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-fallback">
          <h2>Bir seyler ters gitti</h2>
          <button onClick={() => this.setState({ hasError: false })}>
            Tekrar Dene
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Kullanim - kritik alanlari izole et
<ErrorBoundary fallback={<p>Widget yuklenemedi</p>}>
  <WeatherWidget />
</ErrorBoundary>

<ErrorBoundary fallback={<p>Grafik gosterilemedi</p>}>
  <AnalyticsChart />
</ErrorBoundary>
:::

:::exercise
## Pratik Alıştırmalar

### Alıştırma 1: Custom Hook Oluşturma
Bir `useLocalStorage` custom hook'u yazın:
- localStorage'dan veri okuyup state olarak döndürün
- State değiştiğinde otomatik olarak localStorage'a kaydetsin
- Generic tip desteklesin

```tsx
// Starter kod
function useLocalStorage<T>(key: string, initialValue: T) {
  // TODO: useState ile localStorage'dan oku
  // TODO: setValue fonksiyonu hem state'i hem localStorage'i guncellesin
  // TODO: window storage event'ini dinleyerek tab'lar arasi senkronizasyon yap
}

// Kullanim
const [theme, setTheme] = useLocalStorage('theme', 'dark');
```

**Beklenen sonuç:** Hook farklı component'lerde aynı key ile kullanıldığında tutarlı değer döndürmeli, sayfa yenilendikten sonra bile veri korunmalı.

### Alıştırma 2: Compound Component Pattern
Bir `Accordion` component'i oluşturun:

```tsx
// Hedef kullanim
<Accordion>
  <Accordion.Item>
    <Accordion.Header>Baslik 1</Accordion.Header>
    <Accordion.Panel>Icerik 1</Accordion.Panel>
  </Accordion.Item>
  <Accordion.Item>
    <Accordion.Header>Baslik 2</Accordion.Header>
    <Accordion.Panel>Icerik 2</Accordion.Panel>
  </Accordion.Item>
</Accordion>
```

**Beklenen sonuç:** Sadece bir panel aynı anda açık olmalı, header'a tıklandığında panel açılıp kapanmalı, Context API ile state yönetimi yapılmalı.

### Alıştırma 3: Higher-Order Component vs Custom Hook
Aynı işlevsellik (authentication kontrolu) için hem HOC hem custom hook versiyonu yazın ve karşılaştırın:

```tsx
// HOC versiyonu
const withAuth = (WrappedComponent) => { /* TODO */ };

// Custom Hook versiyonu
const useAuth = () => { /* TODO */ };
```

**Beklenen sonuç:** Her iki yaklaşımın da avantaj ve dezavantajlarını dokümante edin. Modern React'te neden hook'lar tercih ediliyor açıklayın.
:::

:::interview
**Mülakat Sorusu:** "Error Boundary neden class component olmak zorundadır?"

**Beklenen cevap:** React'te getDerivedStateFromError ve componentDidCatch lifecycle metotlarının functional component karşılığı henuz bulunmuyor. Bu nedenle Error Boundary'ler şu an için class component olmak zorundadır. Ancak react-error-boundary gibi kütüphaneler ile bu class component'i soyutlayıp, hook-tabanlı bir API ile kullanabilirsiniz.
:::

## Composition vs Inheritance

React ekibi resmi olarak composition'i inheritance'a tercih etmeyi öneriyor. Neden?

:::comparison
| Özellik | Composition | Inheritance |
|---------|-------------|-------------|
| Esneklik | Çok yüksek | Sınırlı |
| Bağımlılık | Gevşek bağlı (loose coupling) | Sıkı bağlı (tight coupling) |
| Yeniden kullanım | Component birleştirerek | Class hiyerarşisi ile |
| Test edilebilirlik | Kolay | Zor |
| React tercihi | Resmi öneri | Önerilmez |

**Tavsiye:** React'te hemen hemen hic inheritance kullanmana gerek yok. children prop'u, render props ve custom hook'lar ile her türlü kodu paylaşabilirsin.
:::

:::code[jsx]{title="Composition ile Esnek Tasarim"}
// Specialization - genel component'ten ozel component turetme
function Dialog({ title, children, actions }) {
  return (
    <div className="dialog-overlay">
      <div className="dialog">
        <h2>{title}</h2>
        <div className="dialog-body">{children}</div>
        {actions && <div className="dialog-actions">{actions}</div>}
      </div>
    </div>
  );
}

// Ozel dialog'lar - inheritance DEGIL composition
function ConfirmDialog({ message, onConfirm, onCancel }) {
  return (
    <Dialog
      title="Emin misiniz?"
      actions={
        <>
          <Button variant="ghost" onClick={onCancel}>Iptal</Button>
          <Button variant="danger" onClick={onConfirm}>Onayla</Button>
        </>
      }
    >
      <p>{message}</p>
    </Dialog>
  );
}

function DeleteAccountDialog({ onConfirm, onCancel }) {
  return (
    <ConfirmDialog
      message="Hesabiniz kalici olarak silinecektir. Bu islem geri alinamaz."
      onConfirm={onConfirm}
      onCancel={onCancel}
    />
  );
}
:::

## Folder Structure Best Practices

### Feature-Based (Önerilen)

:::code[text]{title="Feature-Based Klasor Yapisi"}
src/
  features/
    auth/
      components/
        LoginForm.jsx
        RegisterForm.jsx
        AuthGuard.jsx
      hooks/
        useAuth.js
        useLogin.js
      services/
        authApi.js
      utils/
        validators.js
      auth.slice.js
      index.js          # public API (barrel file)
    dashboard/
      components/
        DashboardLayout.jsx
        StatsCard.jsx
        RecentActivity.jsx
      hooks/
        useDashboardData.js
      index.js
    products/
      components/
      hooks/
      services/
      index.js
  shared/
    components/
      Button.jsx
      Input.jsx
      Modal.jsx
      Spinner.jsx
    hooks/
      useFetch.js
      useDebounce.js
    utils/
      formatDate.js
      cn.js
:::

### Type-Based (Küçük Projeler Için)

:::code[text]{title="Type-Based Klasor Yapisi"}
src/
  components/
    Button.jsx
    Input.jsx
    Header.jsx
    UserList.jsx
  hooks/
    useAuth.js
    useFetch.js
  services/
    api.js
    authService.js
  utils/
    helpers.js
  pages/
    Home.jsx
    Dashboard.jsx
:::

:::comparison
| Özellik | Feature-Based | Type-Based |
|---------|--------------|------------|
| Proje boyutu | Büyük (50+ component) | Küçük (20-30 component) |
| Navigasyon | Kolay - ilgili kodlar bir arada | Zor - dosyalar dağınık |
| Takım çalışması | İdeal - takımlar feature üzerinde çalışır | Conflict riski yüksek |
| Ölçeklenebilirlik | Çok iyi | Sınırlı |
| Silme kolaylığı | Feature klasörünü sil | Tek tek dosya bul-sil |

**Tavsiye:** Projeye type-based ile başla, 30+ component'e ulaştığında feature-based'e geçiş yap. Barrel file (index.js) ile her feature'in public API'sini tanımla.
:::

## Component API Design

İyi bir component API tasarımı, component'in nasıl kullanilacagini belirler.

:::code[jsx]{title="Iyi Component API Tasarimi"}
// 1. Props interface acik ve tutarli olmali
// 2. Mantikli default degerler tanimlanmali
// 3. Esnek ama basit olmali

function DataTable({
  // Zorunlu props
  data,
  columns,

  // Gorunum ayarlari (default degerleri ile)
  striped = false,
  bordered = true,
  compact = false,
  emptyMessage = "Veri bulunamadi",

  // Davranis ayarlari
  sortable = false,
  selectable = false,
  onSort = null,
  onSelect = null,

  // Sayfalama
  pagination = false,
  pageSize = 10,
  onPageChange = null,

  // Stilistik
  className = "",
  ...rest // diger HTML attribute'leri
}) {
  // ... implementasyon
}

// Kullanim - basit
<DataTable data={users} columns={cols} />

// Kullanim - tam donanimli
<DataTable
  data={users}
  columns={cols}
  striped
  sortable
  selectable
  pagination
  pageSize={20}
  onSort={handleSort}
  onSelect={handleSelect}
  onPageChange={handlePage}
/>
:::

:::deha-tip
Component API tasarlarken "Progressive Disclosure" prensibini uygula: Basit kullanım için minimum props yeterli olmalı, gelişmiş kullanım için ek props sunulmalı. Kullanıcının %80'i basit API'yi, %20'si gelişmiş API'yi kullanir. API'ni buna göre tasarla.
:::

:::knowledge-check
type: multiple_choice
question: "Atomic Design'da bir SearchBar (Input + Button) hangi seviyeye aittir?"
options:
  - "Atom"
  - "Molecule"
  - "Organism"
  - "Template"
correct: 1
explanation: "SearchBar, birden fazla atom'un (Input ve Button) birleşiminden oluşan anlamlı bir birimdir. Bu tanim molecule seviyesine karşılık gelir. Atom'lar tek başına en küçük birimlerdir, organism'ler ise birden fazla molecule içerir."
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdakilerden hangisi HOC (Higher-Order Component) kullanimi için YANLIŞ bir pratiktir?"
options:
  - "HOC'u component dışında tanimlamak"
  - "HOC'u render metodu içinde oluşturmak"
  - "HOC ile cross-cutting concern eklemek"
  - "HOC'a displayName atamak"
correct: 1
explanation: "HOC'u render içinde oluşturmak her render'da yeni bir component oluşturur, state'i kaybettirir ve performans sorunlarına neden olur. HOC'lar her zaman component tanımının dışında oluşturulmalıdır."
:::

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Compound Components pattern'ini HTML'deki select/option ilişkisiyle karşılaştırarak açıkla. Context API ile compound component'ler arasında nasıl iletişim kurulur? Bu pattern'i Radix UI ve Headless UI gibi kütüphaneler nasıl kullanıyor? Bir Tabs component'i için adım adım implementasyon göster."

**2. Pratik Uygulama:**
> "Atomic Design metodolojisine göre bir e-ticaret UI kit'i tasarla: Atom'lar (Button, Input, Badge, Avatar), Molecule'ler (SearchBar, ProductPrice, Rating), Organism'ler (ProductCard, Header, CartSummary). Her seviye için TypeScript props interface'leri ve Storybook story örnekleri yaz."
> Takip: "Simdi bu component'leri feature-based klasör yapısında organize et ve her feature için barrel file (index.ts) ile public API tanımla."

**3. Mukemmellik Için:**
> "500+ component'li büyük bir SaaS projesinde component architecture nasıl yönetilir? Design system kurma sürecini, component audit yapmayi, API-first tasarımı ve Storybook ile dokumantasyonu kapsayan bir strateji oluştur. Shopify Polaris ve Radix UI gibi production design system'lerinden ilham al."

### Pair Programming Ipucu
Yeni component tasarlarken AI'a önce kullanım örneğini (JSX) göster: "Bu component'i bu şekilde kullanmak istiyorum. Simdi bu API'yi karşılayan implementasyonu yaz. Progressive disclosure prensibini uygula - basit kullanım için minimum props, gelişmiş kullanım için ek props olsun."
:::

:::exercise
### Alıştırma 4: Compound Components Pattern
**Görev:** Tabs component'ini Compound Components pattern'i ile yaz. Context ile iletişim kursun.
**Başlangıç kodu:**
```tsx
// Hedef kullanım:
// <Tabs defaultTab="tab1">
//   <Tabs.List>
//     <Tabs.Tab id="tab1">Genel</Tabs.Tab>
//     <Tabs.Tab id="tab2">Ayarlar</Tabs.Tab>
//   </Tabs.List>
//   <Tabs.Panel id="tab1">Genel içerik</Tabs.Panel>
//   <Tabs.Panel id="tab2">Ayarlar içerik</Tabs.Panel>
// </Tabs>

// TODO: TabsContext oluştur
// TODO: Tabs (parent), Tabs.List, Tabs.Tab, Tabs.Panel component'lerini yaz
```
**Beklenen çıktı:**
```tsx
interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div>{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabList({ children }: { children: ReactNode }) {
  return <div className="flex gap-2 border-b">{children}</div>;
};

Tabs.Tab = function Tab({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useContext(TabsContext)!;
  return (
    <button
      onClick={() => setActiveTab(id)}
      className={activeTab === id ? "border-b-2 border-blue-500" : ""}
    >{children}</button>
  );
};

Tabs.Panel = function TabPanel({ id, children }: { id: string; children: ReactNode }) {
  const { activeTab } = useContext(TabsContext)!;
  return activeTab === id ? <div className="p-4">{children}</div> : null;
};
```
**İpucu:** Parent component Context sağlar, child component'ler Context'ten state okur. Bu pattern React'te Tab, Accordion, Dropdown gibi bileşik component'ler için idealdir.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 5: Polymorphic Component (as prop)
**Görev:** `as` prop'u ile render edilen HTML elementini değiştirebilen bir Button component'i yaz.
**Başlangıç kodu:**
```tsx
// Hedef kullanım:
// <Button>Normal Buton</Button>              → <button>
// <Button as="a" href="/about">Link</Button> → <a>
// <Button as={Link} to="/home">Router</Button> → <Link>

// TODO: ButtonProps tipini tanımla (generic olmalı)
// TODO: Button component'ini yaz
```
**Beklenen çıktı:**
```tsx
type ButtonProps<T extends React.ElementType = "button"> = {
  as?: T;
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  children: ReactNode;
} & Omit<React.ComponentPropsWithoutRef<T>, "as" | "variant" | "size">;

function Button<T extends React.ElementType = "button">({
  as,
  variant = "primary",
  size = "md",
  children,
  ...props
}: ButtonProps<T>) {
  const Component = as || "button";
  const baseStyles = "rounded font-medium transition-colors";
  const variants = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
    ghost: "bg-transparent text-gray-600 hover:bg-gray-100",
  };
  const sizes = { sm: "px-2 py-1 text-sm", md: "px-4 py-2", lg: "px-6 py-3 text-lg" };

  return (
    <Component className={`${baseStyles} ${variants[variant]} ${sizes[size]}`} {...props}>
      {children}
    </Component>
  );
}
```
**İpucu:** `React.ElementType` tüm HTML elementlerini ve React component'lerini kapsar. `Omit` ile çakışan prop'ları çıkar.
**Zorluk:** Zor
:::

:::exercise
### Alıştırma 6: Presentational vs Container Ayrımı
**Görev:** Monolitik bir component'i Presentational ve Container olarak ikiye ayır.
**Başlangıç kodu:**
```tsx
// YANLIŞ: Tek component'te hem iş mantığı hem görünüm
function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/user/me")
      .then(res => res.json())
      .then(data => { setUser(data); setLoading(false); });
  }, []);

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    window.location.href = "/login";
  };

  if (loading) return <p>Yükleniyor...</p>;
  return (
    <div className="p-4 bg-gray-800 rounded">
      <img src={user.avatar} className="w-20 h-20 rounded-full" />
      <h2 className="text-white">{user.name}</h2>
      <p className="text-gray-400">{user.email}</p>
      <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 mt-2">
        Çıkış Yap
      </button>
    </div>
  );
}

// TODO: Presentational component (sadece props alır, UI render eder)
// TODO: Container component (veri çeker, iş mantığı yönetir)
```
**Beklenen çıktı:**
```tsx
// Presentational - sadece görünüm
interface UserProfileViewProps {
  user: { name: string; email: string; avatar: string };
  onLogout: () => void;
}

function UserProfileView({ user, onLogout }: UserProfileViewProps) {
  return (
    <div className="p-4 bg-gray-800 rounded">
      <img src={user.avatar} className="w-20 h-20 rounded-full" />
      <h2 className="text-white">{user.name}</h2>
      <p className="text-gray-400">{user.email}</p>
      <button onClick={onLogout} className="bg-red-500 text-white px-4 py-2 mt-2">
        Çıkış Yap
      </button>
    </div>
  );
}

// Container - iş mantığı
function UserProfileContainer() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/user/me").then(r => r.json()).then(d => { setUser(d); setLoading(false); });
  }, []);

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" });
    window.location.href = "/login";
  };

  if (loading) return <p>Yükleniyor...</p>;
  return <UserProfileView user={user} onLogout={handleLogout} />;
}
```
**İpucu:** Presentational component test etmesi kolaydır (sadece props ver), Storybook'ta gösterilebilir. Container component iş mantığını yönetir.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 7: Error Boundary Component
**Görev:** Hata yakalayan ve kullanıcıya güzel bir hata mesajı gösteren Error Boundary yaz.
**Başlangıç kodu:**
```tsx
// TODO: ErrorBoundary class component'i yaz
// - componentDidCatch ile hatayı logla
// - getDerivedStateFromError ile hata state'ini güncelle
// - fallback prop'u ile özelleştirilebilir hata UI'ı
// - "Tekrar Dene" butonu ile state sıfırlama

// Kullanım:
// <ErrorBoundary fallback={<p>Hata!</p>}>
//   <BuggyComponent />
// </ErrorBoundary>
```
**Beklenen çıktı:**
```tsx
interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Error caught:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-4 bg-red-900 rounded text-center">
          <h2 className="text-red-200">Bir şeyler ters gitti</h2>
          <p className="text-red-300 text-sm">{this.state.error?.message}</p>
          <button onClick={this.handleReset} className="mt-2 bg-red-500 text-white px-4 py-2 rounded">
            Tekrar Dene
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
```
**İpucu:** Error Boundary sadece class component olabilir (React hooks'ta henüz karşılığı yok). `getDerivedStateFromError` render aşamasında, `componentDidCatch` commit aşamasında çalışır.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: HOC (Higher-Order Component) Pattern
**Görev:** Authentication kontrolü yapan bir `withAuth` HOC'u yaz.
**Başlangıç kodu:**
```tsx
// TODO: withAuth HOC'u yaz
// - Kullanıcı giriş yapmamışsa login sayfasına yönlendir
// - Giriş yapmışsa component'e user prop'u ekle
// - Loading durumunu yönet

// Kullanım:
// const ProtectedDashboard = withAuth(Dashboard);
// <ProtectedDashboard /> → giriş yapılmışsa Dashboard, yoksa redirect
```
**Beklenen çıktı:**
```tsx
interface WithAuthProps {
  user: { id: string; name: string; email: string };
}

function withAuth<T extends WithAuthProps>(
  WrappedComponent: React.ComponentType<T>
) {
  return function AuthenticatedComponent(
    props: Omit<T, keyof WithAuthProps>
  ) {
    const [user, setUser] = useState<WithAuthProps["user"] | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      fetch("/api/auth/me")
        .then(res => res.ok ? res.json() : Promise.reject())
        .then(setUser)
        .catch(() => window.location.href = "/login")
        .finally(() => setLoading(false));
    }, []);

    if (loading) return <div>Yükleniyor...</div>;
    if (!user) return null;

    return <WrappedComponent {...(props as T)} user={user} />;
  };
}

// Kullanım:
const ProtectedDashboard = withAuth(Dashboard);
```
**İpucu:** HOC bir fonksiyondur ve component alıp yeni component döndürür. Modern React'te custom hook'lar genellikle tercih edilir ama HOC pattern'ını bilmek legacy kodları anlamak için önemlidir.
**Zorluk:** Zor
:::

:::exercise
### Alıştırma 9: Atomic Design Sınıflandırma
**Görev:** Aşağıdaki component'leri Atomic Design seviyelerine göre sınıflandır.
**Başlangıç kodu:**
```
Verilen component'ler:
1. Avatar (kullanıcı profil resmi)
2. SearchBar (input + buton)
3. ProductCard (resim + başlık + fiyat + sepet butonu)
4. Header (logo + navbar + search + avatar)
5. Badge (bildirim sayısı)
6. Input (text input alanı)
7. LoginForm (email + password + submit)
8. DashboardTemplate (sidebar + header + content area)
9. HomePage (gerçek verilerle dolu sayfa)
10. StarRating (yıldız ikonları + puan)

TODO: Her birini doğru seviyeye yerleştir:
Atoms:
Molecules:
Organisms:
Templates:
Pages:
```
**Beklenen çıktı:**
```
Atoms (en küçük, bölünemez):
  - Avatar, Badge, Input

Molecules (atom kombinasyonları):
  - SearchBar (Input + Button atom'ları)
  - StarRating (Icon atom'ları)

Organisms (molecule + atom grupları):
  - ProductCard (Avatar + Badge + Button)
  - Header (Logo + SearchBar + Avatar)
  - LoginForm (Input + Input + Button)

Templates (sayfa iskeletleri, veri yok):
  - DashboardTemplate (layout yapısı)

Pages (template + gerçek veri):
  - HomePage (DashboardTemplate + API verisi)
```
**İpucu:** Atom = tek HTML elementi gibi basit. Molecule = birkaç atom bir arada. Organism = bağımsız çalışabilen bölüm. Template = yerleşim. Page = gerçek veri.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 10: Folder Structure - Feature-Based Organizasyon
**Görev:** Aşağıdaki dosyaları feature-based klasör yapısına taşı.
**Başlangıç kodu:**
```
YANLIŞ: Tip-bazlı yapı (büyük projelerde sorunlu)
src/
  components/
    Button.tsx, Input.tsx, Modal.tsx, ProductCard.tsx,
    CartItem.tsx, UserAvatar.tsx, LoginForm.tsx
  hooks/
    useAuth.ts, useCart.ts, useProducts.ts
  services/
    authService.ts, cartService.ts, productService.ts
  types/
    auth.ts, cart.ts, product.ts

TODO: Feature-based yapıya dönüştür
```
**Beklenen çıktı:**
```
DOĞRU: Feature-bazlı yapı
src/
  features/
    auth/
      components/LoginForm.tsx, UserAvatar.tsx
      hooks/useAuth.ts
      services/authService.ts
      types/auth.ts
      index.ts          ← barrel export
    cart/
      components/CartItem.tsx
      hooks/useCart.ts
      services/cartService.ts
      types/cart.ts
      index.ts
    products/
      components/ProductCard.tsx
      hooks/useProducts.ts
      services/productService.ts
      types/product.ts
      index.ts
  shared/
    components/Button.tsx, Input.tsx, Modal.tsx
    index.ts

// Barrel export örneği (features/auth/index.ts):
export { LoginForm } from "./components/LoginForm";
export { useAuth } from "./hooks/useAuth";
export type { AuthUser } from "./types/auth";
```
**İpucu:** Feature-based yapıda ilgili dosyalar bir arada. Paylaşılan component'ler `shared/` altında. Barrel export ile temiz import'lar: `import { useAuth } from "@/features/auth"`.
**Zorluk:** Orta
:::

:::must-note
- Atomic Design 5 seviye: Atoms (buton, input) -> Molecules (search bar) -> Organisms (header) -> Templates (layout) -> Pages (gerçek veri)
- Presentational component = sadece gösterim (props alir, render eder), Container component = is mantığı + state yönetimi
- Compound Components = birbiriyle bağlantıli component'ler (Tabs/Tab/Panel gibi), Context ile iletişim kurar
- Render Props = component'e render fonksiyonu geçirme, aynı mantik farklı görünüm. Modern alternatif: custom hooks
- HOC = component alip yeni component döndüren fonksiyon, ASLA render içinde oluşturma (performance bug)
- Error Boundary = React'te hata yakalayan class component, getDerivedStateFromError + componentDidCatch
- Composition > Inheritance: React resmi olarak composition'i önerir, children prop + render props + hooks ile
- Feature-based klasör yapısı büyük projelerde, type-based küçük projelerde tercih edilir
- Component API: zorunlu props az, default degerler mantıklı, progressive disclosure prensibi
- Barrel file (index.js) ile feature'in public API'sini tanımla, iç detayları gizle
:::

:::senior-learns
Bir Senior Developer component architecture konusunu öğrenirken su yaklaşımı benimser:

1. **Açık kaynak kütüphane kodlarını okur** - Radix UI, Headless UI, shadcn/ui gibi kütüphanelerin kaynak kodlarını inceleyerek compound components, render props ve composition pattern'larinin production seviyesinde nasıl uygulandığını görür.

2. **Design System oluşturur** - Sadece component yazmaz, bir design system kurar. Token'lar (renk, spacing, typography), component'ler ve dokümantasyon (Storybook) bir aradadir. Shopify Polaris, Atlassian Design System gibi örnekleri inceler.

3. **Component audit yapar** - Mevcut projede kaç tane benzer component olduğunu, hangilerinin birleştirilebileceğini analiz eder. "Bu projede kaç tane farklı Button component'i var?" sorusuyla baslayip, tekrarları tespit eder.

4. **API-first tasarım yapar** - Implementasyondan önce component'in nasıl KULLANILACAGINI tanımlar. Bos bir dosyada önce kullanım örneklerini (JSX) yazar, sonra implementasyonu gerçekleştirir. "Consumer-first thinking" prensibi.

5. **Performans etkisini ölçer** - React Profiler ile gereksiz re-render'ları tespit eder. React.memo, useMemo, useCallback'i ölçüme dayali kullanir, korkuya dayali değil. "Premature optimization is the root of all evil" - Donald Knuth.

6. **Dokümante eder ve Storybook yazar** - Her component için Storybook story'si yazar. Farklı props kombinasyonlarını, edge case'leri ve accessibility durumlarını dokümante eder.

**Profesyonel Mindset:** "Component architecture, bir uygulamanın iskeletidir. Yanlış iskelet üzerine güzel cephe koyabilirsin ama depremde yıkılır. Doğru pattern'i doğru yerde kullanmak, 100 pattern bilmekten daha değerlidir. Her pattern bir problemi cozer - önce problemi tani, sonra pattern'i uygula."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Composition** (kom-puh-zi-shn) -> Birlestirme / Kompozisyon
   *"React favors composition over inheritance for code reuse between components."*

2. **Higher-Order Component** (hay-er or-der) -> Ust-Düzey Component
   *"A higher-order component is a function that takes a component and returns a new component."*

3. **Render Props** (ren-der props) -> Render Fonksiyon Geçirme
   *"The render props pattern lets you share stateful logic between components."*

4. **Error Boundary** (er-er bawn-duh-ree) -> Hata Sınırı
   *"Error boundaries catch JavaScript errors in their child component tree."*

5. **Atomic Design** (uh-tom-ik dih-zayn) -> Atomik Tasarım
   *"Atomic design provides a methodology for creating design systems."*

**Okuma Egzersizi:** React dokümantasyonunda "Thinking in React" sayfasını İngilizce oku: https://react.dev/learn/thinking-in-react

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Component mimarisini Atomic Design'a göre yeniden düzenleme"
-> Örnek: `refactor: reorganize component architecture following Atomic Design methodology`
:::

:::external-resource
- **React Docs:** "Thinking in React" (resmi dokümantasyon, ücretsiz)
- **Brad Frost:** "Atomic Design" kitabi (atomicdesign.bradfrost.com, ücretsiz)
- **Patterns.dev:** Component pattern'lari (patterns.dev, ücretsiz)
- **Storybook:** Component dokumantasyonu aracı (storybook.js.org)
:::
