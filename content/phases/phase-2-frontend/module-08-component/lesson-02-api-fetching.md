---
title: "API & Data Fetching Patterns"
id: "mod-08-api/lesson-02"
estimated_minutes: 50
order: 2
tags: ["fetch", "axios", "tanstack-query", "swr", "data-fetching", "websocket"]
prerequisites: ["mod-08-api/lesson-01"]
---

# API & Data Fetching Patterns

:::realworld
Her modern web uygulaması sunucudan veri çekmek zorundadır. Bir e-ticaret sitesinde ürün listesi, bir sosyal medya uygulamasında post akışı, bir dashboard'da analitik verileri - hepsi API çağrıları ile gelir. Ancak veri çekmek sadece bir fetch() yazmak değildir. Loading state yönetimi, hata yönetimi, cache'leme, optimistic update'ler, pagination ve gerçek zamanli veri senkronizasyonu gibi onlarca problemi cozmek gerekir. Bu derste, production seviyesinde data fetching pattern'larını öğreneceksin. Mülakatlarda "Veri çekme stratejinizi nasıl tasarlarsınız?" sorusuna kapsamli cevap verebilecek seviyeye geleceksin.
:::

## Neden Data Fetching Strategy Önemlidir?

Yanlış data fetching stratejisi ile:

- Kullanıcı her sayfa geçişinde loading spinner görür (kötü UX)
- Aynı veriyi gereksiz yere tekrar tekrar çekersin (bant genişliği israfı)
- Bir hata oluştuğunda uygulama çöker veya kullanıcı ne olduğunu anlamaz
- State yönetimi karışır (loading, error, data üçlemeyi her component'te tekrarlarsın)
- Race condition bug'ları ortaya çıkar

:::deha-tip
Deha seviyesi geliştiriciler her API çağrısında şu soruyu sorar: "Bu veri ne sıklıkla değişiyor ve ne kadar 'stale' (bayat) olması kabul edilebilir?" Bir kullanıcı profili dakikada bir değişebilir ama ürün kategorileri ayda bir degisir. Her veri tipi için farklı cache ve refetch stratejisi uygulamak, hem performansi hem de UX'i optimize eder.
:::

## fetch API vs Axios

### Native fetch API

:::code[javascript]{title="fetch API Temelleri"}
// Basit GET istegi
async function getUsers() {
  const response = await fetch("https://api.example.com/users");

  // fetch 404 ve 500 icin reject ETMEZ, kontrol etmelisin
  if (!response.ok) {
    throw new Error(`HTTP Error: ${response.status}`);
  }

  return response.json();
}

// POST istegi
async function createUser(userData) {
  const response = await fetch("https://api.example.com/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || "Kullanici oluşturulamadi");
  }

  return response.json();
}

// Timeout ekleme (fetch native olarak desteklemez)
async function fetchWithTimeout(url, options = {}, timeout = 5000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    return response;
  } finally {
    clearTimeout(id);
  }
}
:::

### Axios

:::code[javascript]{title="Axios Temelleri"}
import axios from "axios";

// Axios instance oluştur (base config)
const api = axios.create({
  baseURL: "https://api.example.com",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
});

// GET istegi - response.data otomatik parse edilir
const { data: users } = await api.get("/users");

// POST istegi
const { data: newUser } = await api.post("/users", {
  name: "Ahmet",
  email: "ahmet@example.com",
});

// Axios otomatik olarak 4xx/5xx icin reject eder
// response.ok kontrolune gerek yok
:::

### Axios Interceptors

:::code[javascript]{title="Axios Interceptors - Request & Response"}
// Request Interceptor - her istege token ekle
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor - 401'de token yenile
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Token suresi dolmussa yenile
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const { data } = await axios.post("/auth/refresh", {
          refreshToken: localStorage.getItem("refreshToken"),
        });

        localStorage.setItem("accessToken", data.accessToken);
        originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;

        return api(originalRequest); // Istegi tekrarla
      } catch (refreshError) {
        // Refresh de basarisizsa logout yap
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
:::

:::comparison
| Özellik | fetch API | Axios |
|---------|----------|-------|
| Kurulum | Native, kurulum yok | pnpm add axios |
| JSON parse | Manuel (.json() çağır) | Otomatik |
| Error handling | 4xx/5xx reject etmez | Otomatik reject eder |
| Timeout | Manuel (AbortController) | Built-in |
| Interceptors | Yok | Built-in |
| Request iptal | AbortController | CancelToken / AbortController |
| Browser desteği | Modern browserlar | Tüm browserlar |
| Bundle boyutu | 0 KB (native) | ~13 KB (gzipped) |

**Tavsiye:** Küçük projelerde fetch yeterli. Büyük projelerde interceptor, timeout ve otomatik retry ihtiyacı varsa axios tercih et. TanStack Query ile kullanirken fetch de gayet yeterli olur.
:::

:::beginner-mistake
Yaygın hata: fetch API'nin 404 veya 500 hataları için Promise reject ettiğini sanmak. fetch sadece NETWORK hataları için reject eder (sunucuya ulasilamadi). HTTP hata kodları (4xx, 5xx) için response.ok kontrolu senin sorumluluğun.

```javascript
// YANLIS - hata yakalanamaz
try {
  const data = await fetch("/api/users").then(r => r.json());
} catch (e) {
  // 404 buraya DUSMEZ!
}

// DOGRU
const response = await fetch("/api/users");
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const data = await response.json();
```
:::

## TanStack Query (React Query)

:::concept[TanStack Query (Ing: TanStack Query / React Query)]
Server state yönetimi için tasarlanmis bir kütüphane. Veri çekme, cache'leme, senkronizasyon ve güncelleme işlemlerini otomatikleştirir.

**Türkçe karşılığı:** Sunucu Durum Yönetimi Kutuphanesi
**Ne ise yarar:** API çağrılarını, loading/error state'lerini, cache'i ve refetch stratejilerini yönetir
**Gerçek hayat benzetmesi:** Bir arastirma asistani gibi - bilgiyi senin için toplar, dosyalar, güncel tutar ve sorduğun anda hemen sunar
:::

### Temel Kurulum

:::code[javascript]{title="TanStack Query Kurulumu"}
// main.jsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,      // 5 dakika - veri "fresh" kabul edilir
      gcTime: 10 * 60 * 1000,         // 10 dakika - cache'te tutulur (eski cacheTime)
      retry: 3,                        // Basarisiz istegi 3 kez dene
      refetchOnWindowFocus: true,      // Tab'a geri donunce refetch
      refetchOnReconnect: true,        // Internet bağlantısi gelince refetch
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
:::

### useQuery - Veri Çekme

:::code[jsx]{title="useQuery Kullanimi"}
import { useQuery } from "@tanstack/react-query";

function UserList() {
  const {
    data: users,
    isLoading,      // Ilk yukleme
    isFetching,     // Herhangi bir fetch (arka plan dahil)
    isError,
    error,
    refetch,        // Manuel refetch
  } = useQuery({
    queryKey: ["users"],              // Benzersiz cache anahtari
    queryFn: () => api.get("/users").then(r => r.data),
    staleTime: 30 * 1000,            // 30 saniye fresh
    select: (data) => data.filter(u => u.active), // Veriyi donustur
    enabled: true,                    // false ise sorgu çalışmaz
  });

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorMessage error={error} />;

  return (
    <div>
      {isFetching && <RefreshIndicator />}
      {users.map(user => <UserCard key={user.id} user={user} />)}
    </div>
  );
}

// Parametreli query
function UserProfile({ userId }) {
  const { data: user } = useQuery({
    queryKey: ["users", userId],      // userId degisince yeniden fetch eder
    queryFn: () => api.get(`/users/${userId}`).then(r => r.data),
    enabled: !!userId,                // userId yoksa çalışma
  });

  return user ? <Profile user={user} /> : null;
}
:::

### useMutation - Veri Güncelleme

:::code[jsx]{title="useMutation Kullanimi"}
import { useMutation, useQueryClient } from "@tanstack/react-query";

function CreateUserForm() {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: (newUser) => api.post("/users", newUser),

    onMutate: async (newUser) => {
      // Optimistic update icin mevcut cache'i kaydet
      await queryClient.cancelQueries({ queryKey: ["users"] });
      const previous = queryClient.getQueryData(["users"]);

      // Cache'e iyimser olarak ekle
      queryClient.setQueryData(["users"], (old) => [
        ...old,
        { id: "temp-id", ...newUser },
      ]);

      return { previous }; // Rollback icin
    },

    onError: (err, newUser, context) => {
      // Hata olursa eski haline dondur
      queryClient.setQueryData(["users"], context.previous);
      toast.error("Kullanici oluşturulamadi: " + err.message);
    },

    onSuccess: () => {
      // Basarili olursa cache'i tamamen yenile
      queryClient.invalidateQueries({ queryKey: ["users"] });
      toast.success("Kullanici oluşturuldu!");
    },

    onSettled: () => {
      // Her durumda (basari veya hata) calisir
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const handleSubmit = (formData) => {
    createMutation.mutate(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* form alanlari */}
      <button
        type="submit"
        disabled={createMutation.isPending}
      >
        {createMutation.isPending ? "Kaydediliyor..." : "Kaydet"}
      </button>
    </form>
  );
}
:::

### Cache Invalidation

:::code[javascript]{title="Cache Invalidation Stratejileri"}
const queryClient = useQueryClient();

// Tek bir query'yi invalidate et
queryClient.invalidateQueries({ queryKey: ["users"] });

// Belirli bir user'i invalidate et
queryClient.invalidateQueries({ queryKey: ["users", userId] });

// "users" ile baslayan tum query'leri invalidate et
queryClient.invalidateQueries({ queryKey: ["users"], exact: false });

// Cache'i dogrudan guncelle (refetch olmadan)
queryClient.setQueryData(["users", userId], updatedUser);

// Cache'i tamamen temizle
queryClient.clear();

// Prefetch - kullanici tiklamadan once veriyi hazirla
queryClient.prefetchQuery({
  queryKey: ["users", nextUserId],
  queryFn: () => api.get(`/users/${nextUserId}`).then(r => r.data),
});
:::

:::deha-tip
Cache invalidation, bilgisayar biliminin en zor problemlerinden biridir. TanStack Query'de altın kural: "Mutation sonrası ilgili tüm query'leri invalidate et." Çok agresif invalidation (her seyi yenile) gereksiz network isteklerine, yetersiz invalidation (az seyi yenile) stale data'ya yol acar. Dengeyi bulmak deneyim gerektirir.
:::

## SWR vs TanStack Query

:::comparison
| Özellik | TanStack Query | SWR |
|---------|---------------|-----|
| Geliştirici | TanStack (Tanner Linsley) | Vercel |
| Bundle boyutu | ~39 KB | ~12 KB |
| DevTools | Resmi DevTools | Topluluk |
| Mutations | Kapsamli (onMutate, rollback) | Basit |
| Offline desteği | Gelişmiş | Temel |
| Infinite scroll | useInfiniteQuery | useSWRInfinite |
| Cache control | Çok detayli | Daha basit |
| Ogrenme eğrisi | Orta-Zor | Kolay |
| Proje boyutu | Büyük projeler | Küçük-orta projeler |
| SSR desteği | Next.js, Remix, vb. | Next.js odakli |

**Tavsiye:** Büyük projeler, karmaşık mutation'lar, offline destek ve detayli cache kontrolu gerekiyorsa TanStack Query. Basit data fetching, küçük proje ve Vercel/Next.js ekosistemindeysen SWR. Ikisi de mükemmel kütüphaneler, yanlış secim diye bir şey yok.
:::

## Loading / Error / Success State Yönetimi

:::code[jsx]{title="State Yonetimi Pattern'lari"}
// Pattern 1: Inline kontrol
function UserList() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
  });

  if (isLoading) return <Skeleton count={5} />;
  if (isError) return <ErrorCard error={error} onRetry={() => refetch()} />;
  if (!data?.length) return <EmptyState message="Kullanici bulunamadi" />;

  return data.map(user => <UserCard key={user.id} user={user} />);
}

// Pattern 2: Wrapper component (Suspense + Error Boundary)
function UsersPage() {
  return (
    <ErrorBoundary fallback={<ErrorCard />}>
      <Suspense fallback={<Skeleton count={5} />}>
        <UserList />
      </Suspense>
    </ErrorBoundary>
  );
}

// Pattern 3: Custom hook ile soyutlama
function useApiState(queryResult) {
  const { data, isLoading, isError, error, isFetching } = queryResult;

  return {
    data,
    isLoading,
    isError,
    error,
    isEmpty: !isLoading && !isError && (!data || data.length === 0),
    isRefreshing: !isLoading && isFetching,
  };
}
:::

## Optimistic Updates

:::concept[Optimistic Update (Ing: Optimistic Update)]
Sunucu yanıtını beklemeden UI'i hemen guncellemektir. Başarısız olursa eski haline dondurulur (rollback).

**Türkçe karşılığı:** İyimser Güncelleme
**Ne ise yarar:** Kullanıcıya anında geri bildirim vererek UX'i iyileştirir
**Gerçek hayat benzetmesi:** Bir mesaj uygulamasında "Gonderildi" tikini hemen göstermek - aslında henuz sunucuya ulasmamis olabilir ama kullanıcı beklemesin diye hemen gösterirsin
:::

:::code[jsx]{title="Optimistic Update - Like Butonu Örneği"}
function LikeButton({ postId, initialLikes, isLiked }) {
  const queryClient = useQueryClient();

  const likeMutation = useMutation({
    mutationFn: () => api.post(`/posts/${postId}/like`),

    onMutate: async () => {
      // 1. Devam eden fetch'leri iptal et
      await queryClient.cancelQueries({ queryKey: ["posts", postId] });

      // 2. Mevcut veriyi kaydet (rollback icin)
      const previousPost = queryClient.getQueryData(["posts", postId]);

      // 3. UI'i iyimser olarak guncelle
      queryClient.setQueryData(["posts", postId], (old) => ({
        ...old,
        likes: old.isLiked ? old.likes - 1 : old.likes + 1,
        isLiked: !old.isLiked,
      }));

      return { previousPost };
    },

    onError: (err, variables, context) => {
      // 4. Hata olursa geri al
      queryClient.setQueryData(["posts", postId], context.previousPost);
      toast.error("Islem basarisiz oldu");
    },

    onSettled: () => {
      // 5. Her durumda sunucudan guncel veriyi al
      queryClient.invalidateQueries({ queryKey: ["posts", postId] });
    },
  });

  return (
    <button onClick={() => likeMutation.mutate()}>
      {isLiked ? "Begenildi" : "Begen"} ({initialLikes})
    </button>
  );
}
:::

## Pagination Patterns

:::code[jsx]{title="Cursor-Based Infinite Scroll"}
import { useInfiniteQuery } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";

function InfinitePostList() {
  const { ref, inView } = useInView();

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteQuery({
    queryKey: ["posts"],
    queryFn: ({ pageParam }) =>
      api.get("/posts", {
        params: { cursor: pageParam, limit: 20 },
      }).then(r => r.data),
    initialPageParam: null,
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
  });

  // Kullanici son elemana scroll edince otomatik yukle
  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  if (isLoading) return <Skeleton count={10} />;

  return (
    <div>
      {data.pages.map((page, i) => (
        <Fragment key={i}>
          {page.items.map(post => (
            <PostCard key={post.id} post={post} />
          ))}
        </Fragment>
      ))}

      {/* Gorunur olunca fetchNextPage tetiklenir */}
      <div ref={ref}>
        {isFetchingNextPage && <Spinner />}
        {!hasNextPage && <p>Tum postlar yuklendi</p>}
      </div>
    </div>
  );
}
:::

:::code[jsx]{title="Offset-Based Pagination"}
function PaginatedTable() {
  const [page, setPage] = useState(1);
  const pageSize = 20;

  const { data, isLoading, isPlaceholderData } = useQuery({
    queryKey: ["products", page, pageSize],
    queryFn: () => api.get("/products", {
      params: { page, limit: pageSize },
    }).then(r => r.data),
    placeholderData: keepPreviousData, // Sayfa degisirken önceki veriyi goster
  });

  return (
    <div>
      <Table
        data={data?.items || []}
        style={{ opacity: isPlaceholderData ? 0.5 : 1 }}
      />
      <div className="pagination">
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Onceki
        </button>
        <span>Sayfa {page} / {data?.totalPages}</span>
        <button
          onClick={() => setPage(p => p + 1)}
          disabled={!data?.hasNextPage}
        >
          Sonraki
        </button>
      </div>
    </div>
  );
}
:::

:::comparison
| Özellik | Offset-Based | Cursor-Based |
|---------|-------------|-------------|
| Kullanım | Tablo, admin paneli | Sosyal medya feed, sohbet |
| Syntax | ?page=2&limit=20 | ?cursor=abc123&limit=20 |
| Performans | Büyük offset'lerde yavaş | Her zaman hızlı |
| Sayfa atlama | Mümkün (sayfa 5'e git) | Mümkün değil |
| Yeni veri ekleme | Tekrar eden kayitlar olabilir | Tutarlı sonuçlar |
| Kompleksite | Basit | Daha karmaşık |

**Tavsiye:** Admin paneli, tablo gibi yerlerde offset-based; sosyal medya feed, sohbet, infinite scroll gereken yerlerde cursor-based kullan.
:::

## WebSocket Client Entegrasyonu

:::code[jsx]{title="WebSocket ile Gercek Zamanli Veri"}
import { useEffect, useRef, useCallback } from "react";

function useWebSocket(url) {
  const wsRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const reconnectAttempts = useRef(0);

  const connect = useCallback(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setIsConnected(true);
      reconnectAttempts.current = 0;
      console.log("WebSocket bağlantısi kuruldu");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLastMessage(data);
    };

    ws.onclose = () => {
      setIsConnected(false);
      // Exponential backoff ile yeniden baglan
      const delay = Math.min(
        1000 * Math.pow(2, reconnectAttempts.current),
        30000
      );
      reconnectAttempts.current += 1;
      setTimeout(connect, delay);
    };

    ws.onerror = (error) => {
      console.error("WebSocket hatasi:", error);
    };

    wsRef.current = ws;
  }, [url]);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  const sendMessage = useCallback((data) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  return { isConnected, lastMessage, sendMessage };
}

// TanStack Query ile WebSocket senkronizasyonu
function LiveNotifications() {
  const queryClient = useQueryClient();
  const { lastMessage } = useWebSocket("wss://api.example.com/ws");

  useEffect(() => {
    if (lastMessage?.type === "NEW_NOTIFICATION") {
      // WebSocket'ten gelen veri ile cache'i guncelle
      queryClient.setQueryData(["notifications"], (old) => [
        lastMessage.data,
        ...(old || []),
      ]);
    }

    if (lastMessage?.type === "DATA_UPDATED") {
      // Ilgili query'leri invalidate et
      queryClient.invalidateQueries({
        queryKey: [lastMessage.resource],
      });
    }
  }, [lastMessage, queryClient]);

  return <NotificationList />;
}
:::

## API Error Handling Best Practices

:::code[javascript]{title="Kapsamli Error Handling"}
// 1. Merkezi error handler
class ApiError extends Error {
  constructor(status, message, data = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }

  get isUnauthorized() { return this.status === 401; }
  get isForbidden() { return this.status === 403; }
  get isNotFound() { return this.status === 404; }
  get isValidation() { return this.status === 422; }
  get isServerError() { return this.status >= 500; }
}

// 2. API client wrapper
async function apiRequest(config) {
  try {
    const response = await api(config);
    return response.data;
  } catch (error) {
    if (error.response) {
      // Sunucu yanit verdi (4xx, 5xx)
      throw new ApiError(
        error.response.status,
        error.response.data?.message || "Bir hata olustu",
        error.response.data
      );
    } else if (error.request) {
      // Istek gitti ama yanit gelmedi (network hatasi)
      throw new ApiError(0, "Sunucuya ulasilamiyor. Internet bağlantınizi kontrol edin.");
    } else {
      // Istek oluşturulurken hata
      throw new ApiError(-1, "Beklenmeyen bir hata olustu");
    }
  }
}

// 3. React'te kullanim
function useErrorHandler() {
  return useCallback((error) => {
    if (error instanceof ApiError) {
      if (error.isUnauthorized) {
        // Oturum suresi dolmus, login'e yonlendir
        redirect("/login");
      } else if (error.isValidation) {
        // Form hatalarini goster
        return error.data?.errors;
      } else if (error.isServerError) {
        toast.error("Sunucu hatasi. Lutfen daha sonra tekrar deneyin.");
      } else {
        toast.error(error.message);
      }
    } else {
      toast.error("Beklenmeyen bir hata olustu");
      console.error("Unhandled error:", error);
    }
  }, []);
}
:::

:::code[javascript]{title="Retry Stratejisi"}
// TanStack Query ile retry konfigurasyonu
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        // 4xx hatalarinda retry yapma (client hatasi)
        if (error?.status >= 400 && error?.status < 500) {
          return false;
        }
        // 5xx ve network hatalarinda max 3 kez dene
        return failureCount < 3;
      },
      retryDelay: (attemptIndex) => {
        // Exponential backoff: 1s, 2s, 4s
        return Math.min(1000 * Math.pow(2, attemptIndex), 10000);
      },
    },
  },
});
:::

:::exercise
## Pratik Alıştırmalar

### Alıştırma 1: Custom useFetch Hook
Bir `useFetch` hook'u oluşturun:

```tsx
// Starter kod
function useFetch<T>(url: string) {
  // TODO: data, loading, error state'leri
  // TODO: AbortController ile cleanup (race condition onleme)
  // TODO: retry mekanizmasi (3 deneme, exponential backoff)
  // TODO: cache mekanizmasi (ayni URL'ye tekrar istek atmama)
}

// Kullanim
const { data, loading, error, refetch } = useFetch<User[]>('/api/users');
```

**Beklenen sonuç:** Component unmount olduğunda istek iptal edilmeli, aynı URL için cache'ten dönmeli, hata durumunda otomatik retry yapmalı.

### Alıştırma 2: Infinite Scroll ile Pagination
Bir ürün listesi sayfasi oluşturun:

```tsx
// TODO: Intersection Observer API kullanarak infinite scroll implement edin
// TODO: Her sayfada 20 urun yukleyin
// TODO: Loading spinner gosterin
// TODO: Tum urunler yuklendiyse "Daha fazla urun yok" mesaji gosterin
// TODO: Yukari kaydirma butonu ekleyin
```

**Beklenen sonuç:** Sayfa sonuna yaklasinca otomatik yeni veriler yüklenmeli, gereksiz re-render olmamalı, scroll pozisyonu korunmalı.

### Alıştırma 3: Optimistic Update Pattern
Bir todo uygulamasında optimistic update uygulayınız:

```tsx
// TODO: Todo eklendiginde UI'da aninda goster (API cevabi beklenmeden)
// TODO: API basarisiz olursa degisikligi geri al (rollback)
// TODO: Kullaniciya hata mesaji goster
// TODO: Retry butonu ekle
```

**Beklenen sonuç:** Kullanıcı ekleme/silme işlemlerini anında görmeli, API hatasi durumunda önceki state'e dönülmeli ve kullanıcıya bilgi verilmeli.
:::

:::interview
**Mülakat Sorusu:** "API çağrılarında race condition nasıl önlersiniz?"

**Beklenen cevap:** Race condition, birden fazla async işlemin beklenmeyen sirada tamamlanmasıyla oluşur. Çözümler:
1. **AbortController** - Yeni istek geldiğinde önceki istegi iptal et (search input için ideal)
2. **TanStack Query queryKey** - Otomatik olarak önceki istegi iptal eder
3. **Debounce** - Kullanıcı yazmayI bitirene kadar bekle (300-500ms)
4. **ID karşılaştırma** - Son istenen ID ile gelen veriyi karşılaştır, uyusmuyorsa at

```javascript
// AbortController ile race condition onleme
function useSearch(query) {
  useEffect(() => {
    const controller = new AbortController();
    fetchResults(query, { signal: controller.signal });
    return () => controller.abort(); // Onceki istegi iptal et
  }, [query]);
}
```
:::

:::knowledge-check
type: multiple_choice
question: "TanStack Query'de staleTime: 60000 ne anlama gelir?"
options:
  - "Veri 60 saniye sonra cache'ten silinir"
  - "Veri 60 saniye boyunca 'fresh' kabul edilir ve refetch yapilmaz"
  - "Her 60 saniyede bir otomatik refetch yapılır"
  - "60 saniye sonra query devre disi kalır"
correct: 1
explanation: "staleTime, verinin ne kadar süre boyunca 'fresh' (taze) kabul edilecegini belirler. Bu süre içinde component yeniden mount olsa bile sunucuya istek yapilmaz, cache'teki veri kullanılır. 60000 ms = 60 saniye."
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdakilerden hangisi optimistic update için YANLIŞ bir adimdir?"
options:
  - "onMutate'te mevcut cache'i kaydet (rollback için)"
  - "onMutate'te UI'i hemen güncelle"
  - "onError'da eski veriyi geri yükle"
  - "Mutation başarılı olana kadar UI'i güncelleme"
correct: 3
explanation: "Optimistic update'in amaci sunucu yanıtını BEKLEMEDEN UI'i hemen guncellemektir. 'Mutation başarılı olana kadar UI'i güncelleme' pessimistic (karamsar) yaklasimdir ve optimistic update'in tam tersidir."
:::

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "TanStack Query'de staleTime, gcTime ve refetchOnWindowFocus kavramlarını bir kütüphane analojisiyle açıkla. Bir query'nin lifecycle'ini (fresh -> stale -> inactive -> garbage collected) adım adım göster. Cache invalidation stratejilerini ve ne zaman hangisini kullanacagimi örneklerle anlat."

**2. Pratik Uygulama:**
> "TanStack Query ile bir sosyal medya feed uygulaması kur: useInfiniteQuery ile sonsuz scroll, useMutation ile optimistic like/unlike (hata durumunda rollback), prefetchQuery ile hover'da sonraki sayfayi önbelleğe al. Tüm loading, error ve empty state'leri yonet. TypeScript ile yaz."
> Takip: "Simdi WebSocket ile gerçek zamanli bildirim ekle ve gelen bildirimlerle TanStack Query cache'ini senkronize et."

**3. Mukemmellik İçin:**
> "Büyük bir e-ticaret uygulamasında farklı veri tipleri için farklı cache stratejileri tasarlıyorum: kullanıcı profili (staleTime: 1dk), ürün kategorileri (staleTime: 1 saat), sepet (staleTime: 0), arama sonuçları (staleTime: 30s). Bu stratejiyi TanStack Query ile nasıl implemente ederim? Offline desteği ve retry politikalarını da dahil et."

### Pair Programming Ipucu
API entegrasyonlarında AI'a Network tab çıktısını yapıştır ve sor: "Bu API response'unu TanStack Query ile nasıl cache'lerim? staleTime ve gcTime ne olmalı? Mutation sonrası hangi query'leri invalidate etmeliyim?"
:::

:::exercise
### Alıştırma 4: fetch vs Axios Karşılaştırma
**Görev:** Aynı API çağrısını hem fetch hem Axios ile yaz ve hata yönetimini karşılaştır.
**Başlangıç kodu:**
```tsx
const API_URL = "https://api.example.com/users";

// TODO 1: fetch ile GET isteği (headers, error handling)
async function fetchUsers_fetch() {
  // - Authorization header ekle
  // - response.ok kontrolü
  // - JSON parse
  // - Network hatası ve HTTP hatası ayrı yönet
}

// TODO 2: Axios ile aynı istek
async function fetchUsers_axios() {
  // - Authorization header ekle
  // - Otomatik JSON parse
  // - Error handling (axios otomatik reject eder)
}
```
**Beklenen çıktı:**
```tsx
// fetch
async function fetchUsers_fetch() {
  try {
    const res = await fetch(API_URL, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    if (err instanceof TypeError) console.error("Network hatası");
    throw err;
  }
}

// Axios
async function fetchUsers_axios() {
  try {
    const { data } = await axios.get(API_URL, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return data; // Otomatik JSON parse
  } catch (err) {
    if (axios.isAxiosError(err)) {
      console.error(`HTTP ${err.response?.status}`);
    }
    throw err;
  }
}
```
**İpucu:** fetch'te 404 bir hata DEĞİLDİR (Promise resolve olur), Axios'ta 404 otomatik reject eder. Bu en önemli fark.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: Axios Interceptor ile Token Yönetimi
**Görev:** Axios interceptor ile otomatik token ekleme ve 401 hatalarında token yenileme yaz.
**Başlangıç kodu:**
```tsx
import axios from "axios";

const api = axios.create({
  baseURL: "https://api.example.com",
});

// TODO: Request interceptor - her isteğe token ekle
api.interceptors.request.use(/* ? */);

// TODO: Response interceptor - 401 hatalarında refresh token ile yenile
api.interceptors.response.use(
  /* success handler */,
  /* error handler - 401 ise token yenile ve isteği tekrarla */
);
```
**Beklenen çıktı:**
```tsx
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const { data } = await axios.post("/auth/refresh", {
          refreshToken: localStorage.getItem("refresh_token"),
        });
        localStorage.setItem("access_token", data.accessToken);
        originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
        return api(originalRequest);
      } catch {
        localStorage.clear();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);
```
**İpucu:** `_retry` flag'i ile sonsuz döngüyü engelle. Refresh token da geçersizse kullanıcıyı login'e yönlendir.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 6: TanStack Query - useQuery Temelleri
**Görev:** TanStack Query ile veri çekme, loading/error yönetimi ve cache yapılandırması yaz.
**Başlangıç kodu:**
```tsx
import { useQuery } from "@tanstack/react-query";

interface Product {
  id: number;
  name: string;
  price: number;
}

// TODO: useProducts hook'u yaz
function useProducts(category?: string) {
  return useQuery({
    // queryKey: category'ye göre farklı cache
    // queryFn: API çağrısı
    // staleTime: 5 dakika
    // retry: 2 kez
    // enabled: ???
  });
}

// TODO: Component'te kullan
function ProductList() {
  const [category, setCategory] = useState("all");
  const { data, isLoading, isError, error, refetch } = useProducts(category);

  // TODO: loading, error, success durumlarını render et
}
```
**Beklenen çıktı:**
```tsx
function useProducts(category?: string) {
  return useQuery<Product[]>({
    queryKey: ["products", category],
    queryFn: async () => {
      const url = category && category !== "all"
        ? `/api/products?category=${category}`
        : "/api/products";
      const res = await fetch(url);
      if (!res.ok) throw new Error("Ürünler yüklenemedi");
      return res.json();
    },
    staleTime: 5 * 60 * 1000,
    retry: 2,
  });
}

// Component:
if (isLoading) return <Skeleton />;
if (isError) return <p>Hata: {error.message} <button onClick={() => refetch()}>Tekrar</button></p>;
if (!data?.length) return <p>Ürün bulunamadı</p>;
return data.map(p => <ProductCard key={p.id} product={p} />);
```
**İpucu:** `queryKey` array olarak cache anahtarıdır - `["products", "electronics"]` ve `["products", "books"]` farklı cache'lenir. `staleTime` milisaniye cinsindendir.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: useMutation ile Optimistic Update
**Görev:** TanStack Query useMutation ile bir todo'yu tamamla ve optimistic update uygula.
**Başlangıç kodu:**
```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

// TODO: useMutation ile toggleTodo yaz
// - API'ye PATCH isteği gönder
// - Optimistic update: UI'ı hemen güncelle
// - Hata durumunda eski state'e geri dön (rollback)
// - Başarıda cache'i invalidate et
```
**Beklenen çıktı:**
```tsx
function useToggleTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (todoId: number) => {
      const res = await fetch(`/api/todos/${todoId}/toggle`, { method: "PATCH" });
      if (!res.ok) throw new Error("Güncelleme başarısız");
      return res.json();
    },
    onMutate: async (todoId) => {
      await queryClient.cancelQueries({ queryKey: ["todos"] });
      const previousTodos = queryClient.getQueryData<Todo[]>(["todos"]);

      queryClient.setQueryData<Todo[]>(["todos"], (old) =>
        old?.map(t => t.id === todoId ? { ...t, completed: !t.completed } : t)
      );

      return { previousTodos };
    },
    onError: (_err, _todoId, context) => {
      queryClient.setQueryData(["todos"], context?.previousTodos);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });
}
```
**İpucu:** `onMutate` API çağrısından ÖNCE çalışır (optimistic). `onError`'da eski veriyi geri yükle. `onSettled` her durumda çalışır ve gerçek veriyi getirir.
**Zorluk:** Zor
:::

:::exercise
### Alıştırma 8: Infinite Scroll ile Sayfalama
**Görev:** TanStack Query `useInfiniteQuery` ile sonsuz scroll uygula.
**Başlangıç kodu:**
```tsx
import { useInfiniteQuery } from "@tanstack/react-query";
import { useRef, useCallback } from "react";

// TODO: useInfiniteQuery ile sayfalı veri çek
// TODO: IntersectionObserver ile son eleman göründüğünde yeni sayfa yükle
```
**Beklenen çıktı:**
```tsx
function useInfiniteProducts() {
  return useInfiniteQuery({
    queryKey: ["products", "infinite"],
    queryFn: async ({ pageParam = 1 }) => {
      const res = await fetch(`/api/products?page=${pageParam}&limit=20`);
      return res.json();
    },
    getNextPageParam: (lastPage) => lastPage.nextPage ?? undefined,
    initialPageParam: 1,
  });
}

function ProductFeed() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteProducts();
  const observerRef = useRef<IntersectionObserver>();

  const lastElementRef = useCallback((node: HTMLDivElement | null) => {
    if (isFetchingNextPage) return;
    if (observerRef.current) observerRef.current.disconnect();
    observerRef.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && hasNextPage) {
        fetchNextPage();
      }
    });
    if (node) observerRef.current.observe(node);
  }, [isFetchingNextPage, hasNextPage, fetchNextPage]);

  return (
    <div>
      {data?.pages.flatMap((page, i) =>
        page.items.map((item: any, j: number) => {
          const isLast = i === data.pages.length - 1 && j === page.items.length - 1;
          return <div ref={isLast ? lastElementRef : null} key={item.id}>{item.name}</div>;
        })
      )}
      {isFetchingNextPage && <p>Yükleniyor...</p>}
    </div>
  );
}
```
**İpucu:** `IntersectionObserver` son elementi izler, görünür olunca `fetchNextPage()` çağrılır. `getNextPageParam` sonraki sayfa numarasını döndürür, yoksa `undefined` dönerek daha fazla sayfa olmadığını belirtir.
**Zorluk:** Zor
:::

:::exercise
### Alıştırma 9: API Error Handler Utility
**Görev:** Merkezi bir API error handler fonksiyonu yaz ve tüm hata tiplerini yönet.
**Başlangıç kodu:**
```tsx
// TODO: ApiError class'ı oluştur
// TODO: handleApiError fonksiyonu yaz
// - Network hatası, timeout, 4xx, 5xx ayrımı
// - Kullanıcıya anlamlı mesaj döndür
// - Error tracking (Sentry benzeri) entegrasyonu
```
**Beklenen çıktı:**
```tsx
class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code?: string,
    public details?: Record<string, string[]>
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function handleApiError(error: unknown): string {
  if (error instanceof ApiError) {
    switch (error.statusCode) {
      case 400: return `Geçersiz istek: ${error.message}`;
      case 401: return "Oturum süresi doldu. Lütfen tekrar giriş yapın.";
      case 403: return "Bu işlem için yetkiniz yok.";
      case 404: return "İstenen kaynak bulunamadı.";
      case 409: return "Çakışma: Bu kayıt zaten mevcut.";
      case 422: return `Doğrulama hatası: ${error.message}`;
      case 429: return "Çok fazla istek. Lütfen biraz bekleyin.";
      default:
        if (error.statusCode >= 500) return "Sunucu hatası. Lütfen daha sonra tekrar deneyin.";
        return error.message;
    }
  }
  if (error instanceof TypeError && error.message === "Failed to fetch") {
    return "Bağlantı hatası. İnternet bağlantınızı kontrol edin.";
  }
  return "Beklenmeyen bir hata oluştu.";
}
```
**İpucu:** Custom error class ile hata tiplerini yapılandır. HTTP status code'lara göre kullanıcıya Türkçe anlamlı mesajlar göster.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 10: WebSocket ile Gerçek Zamanlı Bildirim
**Görev:** WebSocket bağlantısı kuran ve TanStack Query cache'ini güncelleyen bir hook yaz.
**Başlangıç kodu:**
```tsx
// TODO: useRealtimeNotifications hook'u yaz
// - WebSocket bağlantısı kur
// - Gelen mesajları parse et
// - TanStack Query cache'ini güncelle
// - Bağlantı koptuğunda yeniden bağlan
// - Cleanup (unmount'ta bağlantıyı kapat)
```
**Beklenen çıktı:**
```tsx
function useRealtimeNotifications() {
  const queryClient = useQueryClient();

  useEffect(() => {
    let ws: WebSocket;
    let reconnectTimer: NodeJS.Timeout;

    function connect() {
      ws = new WebSocket("wss://api.example.com/ws");

      ws.onopen = () => console.log("WebSocket bağlandı");

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);

        switch (message.type) {
          case "NEW_NOTIFICATION":
            queryClient.setQueryData<Notification[]>(
              ["notifications"],
              (old) => [message.payload, ...(old ?? [])]
            );
            break;
          case "DATA_UPDATED":
            queryClient.invalidateQueries({ queryKey: [message.resource] });
            break;
        }
      };

      ws.onclose = () => {
        reconnectTimer = setTimeout(connect, 3000);
      };

      ws.onerror = (err) => console.error("WebSocket hatası:", err);
    }

    connect();

    return () => {
      clearTimeout(reconnectTimer);
      ws?.close();
    };
  }, [queryClient]);
}
```
**İpucu:** WebSocket kapandığında otomatik yeniden bağlanma (reconnect) uygula. Cleanup'ta hem WebSocket'i hem timer'ı temizle. `queryClient.setQueryData` ile cache'i doğrudan güncelle.
**Zorluk:** Zor
:::

:::must-note
- fetch API: 4xx/5xx için reject ETMEZ (response.ok kontrol et), Axios: otomatik reject eder
- Axios interceptors: request'te token ekle, response'ta 401 yakala ve token yenile
- TanStack Query temel kavramlar: queryKey (cache anahtari), queryFn (fetch fonksiyonu), staleTime (fresh süresi), gcTime (cache süresi)
- useQuery = veri çekme (GET), useMutation = veri güncelleme (POST/PUT/DELETE)
- Cache invalidation: mutation sonrası queryClient.invalidateQueries() ile ilgili query'leri yenile
- Optimistic update adımları: 1) Cache kaydet, 2) UI güncelle, 3) Hatada rollback, 4) Basaride invalidate
- SWR = küçük/orta proje, basit API; TanStack Query = büyük proje, karmaşık mutation, offline destek
- Pagination: offset-based = tablo/admin, cursor-based = feed/infinite scroll
- WebSocket: exponential backoff ile reconnect, TanStack Query cache'i ile senkronize et
- Error handling: ApiError class, merkezi error handler, 4xx retry yapma, 5xx için exponential backoff
- Race condition: AbortController, TanStack Query otomatik cancel, debounce
:::

:::senior-learns
Bir Senior Developer data fetching konusunu öğrenirken su yaklaşımı benimser:

1. **Network tab'ini her gun kullanir** - Chrome DevTools Network tab'inda waterfall analizi yapar. Her API çağrısının ne kadar sürdüğünü, kaç KB veri geldiğini ve gereksiz çağrıların olup olmadığını inceler. "Sayfam neden yavaş?" sorusuna veriyle cevap verir.

2. **Cache stratejisini veri tipine göre belirler** - Kullanıcı profili: staleTime 1 dakika. Ürün kategorileri: staleTime 1 saat. Bildirimler: staleTime 0 (her zaman refetch). "Tek bir staleTime tüm uygulamaya uygun olmaz" prensibini bilir.

3. **Optimistic update ile pessimistic update arasındaki dengeyi kurar** - Like butonu: optimistic (anında geri bildirim). Odeme işlemi: pessimistic (sunucu onaylasIn). Risk seviyesine göre strateji belirler.

4. **API contract'larini tanımlar** - Backend ekibi ile API response formatini, error kodlarını ve pagination yapısını önceden belirler. TypeScript ile API tiplerini tanımlar ve otomatik doğrulama yapar.

5. **Offline-first düşünür** - TanStack Query'nin offline mutasyonlarını, service worker ile cache stratejisini ve kullanıcının internet bağlantısı kesildiğindeki UX'i planlar.

6. **Monitoring ve alerting kurar** - API response time'larını izler (Datadog, New Relic). p50, p95, p99 latency metriklerini takip eder. "Ortalama yanıt süresi 200ms" yeterli değildir, p99'un 3 saniye olmadığından emin olur.

**Karar Verme Süreci — Fetch vs Axios vs ky:**
- **Native fetch**: Zero dependency, browser API. Trade-off: interceptor yok, timeout desteği yok (AbortController ile manuel), response.ok kontrolünü unutursan sessizce hata yutarsın. Küçük projeler ve Server Components için yeterli.
- **Axios**: Interceptor, timeout, request/response transform, progress tracking. Trade-off: 13KB bundle ekleniyor, fetch'in yapamadığı çok az şey var artık. Legacy projelerde yaygın ama yeni projelerde fetch+wrapper tercih et.
- **ky (tiny alternative)**: ~3KB, fetch tabanlı, retry, timeout, JSON otomatik. Trade-off: Axios'un tüm özelliklerini sunmaz ama %90 use case'i karşılar.
- **Senior karar agaci**: "Server Component mi? Native fetch. Client Component, basit proje? fetch + küçük wrapper. Interceptor, progress gibi advanced ihtiyaç var mı? Axios veya ky."

**Anti-pattern Farkindaligi:**
- **Waterfall request'ler**: Sıralı bağımlı olmayan 5 API çağrısı birbirini bekliyor. Her biri 200ms, toplam 1 saniye. `Promise.all` ile paralelize edersen toplam 200ms. Production'da bunu düzeltmek tek başına sayfa yükleme süresini %60 düşürdü.
- **useEffect içinde uncontrolled fetch**: Cleanup fonksiyonu olmayan fetch, component unmount olunca "setState on unmounted component" hatası verir. Race condition'lar oluşur — kullanıcı hızlı filtre değiştirdiğinde eski response yeni response'un üstüne yazar. AbortController veya TanStack Query kullan.
- **Over-fetching**: Kullanıcı adı için 50 field'lık user objesini çeken endpoint. Backend'e "bana sadece name ve avatar ver" demenin yolu yok. GraphQL'in çözdüğü ana problem bu. REST'te çözüm: sparse fieldsets veya dedicated endpoint.

**Gercek Dunya Deneyimi:** Bir e-ticaret projesinde ürün listesi sayfası 3.5 saniyede yükleniyordu. Network tab'ı açtığımda gördüm: aynı endpoint'e 4 kez çağrı yapılıyor (farklı component'ler bağımsız fetch ediyor), her response 800KB (tüm ürün detayları geliyor ama sadece isim ve fiyat gösteriliyor). TanStack Query ile deduplicate ettik, backend'e lightweight endpoint ekledik, staleTime ile gereksiz refetch'leri engelledik. Sonuç: 600ms'ye düştü. Ders: önce Network tab'ını aç, sonra kodu yaz.

**Profesyonel Mindset:** "Data fetching, frontend'in en kritik katmanidir. Kullanıcı ne kadar güzel bir UI gorurse görsün, veri 3 saniye gec gelirse veya hata mesaji anlamsizsa uygulama başarısızdır. Network'u anlayan, cache'i doğru kullanan ve hataları gracefully handle eden muhendis, production'da fark yaratan muhendistir."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Stale** (steyl) -> Bayat / Eski
   *"When data becomes stale, TanStack Query will refetch it in the background."*

2. **Cache Invalidation** (kash in-val-ih-day-shn) -> Cache Gecersiz Kilma
   *"After a mutation, we invalidate the related queries to refetch fresh data."*

3. **Optimistic Update** (op-tih-mis-tik up-dayt) -> İyimser Güncelleme
   *"Optimistic updates provide instant feedback by updating the UI before the server responds."*

4. **Race Condition** (rays kun-dish-un) -> Yaris Durumu
   *"AbortController prevents race conditions by canceling previous requests."*

5. **Interceptor** (in-ter-sep-ter) -> Araci / Yakalayici
   *"Axios interceptors can automatically attach auth tokens to every request."*

**Okuma Egzersizi:** TanStack Query resmi dokümantasyonunda "Important Defaults" sayfasını İngilizce oku: https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "API isteklerine TanStack Query entegrasyonu ekle"
-> Örnek: `feat: integrate TanStack Query for API data fetching and caching`
:::

:::external-resource
- **TanStack Query Docs:** Resmi dokümantasyon (tanstack.com/query, ücretsiz)
- **Axios Docs:** Resmi dokümantasyon (axios-http.com, ücretsiz)
- **SWR Docs:** Resmi dokümantasyon (swr.vercel.app, ücretsiz)
- **Patterns.dev:** "Rendering Patterns" bölümü (patterns.dev, ücretsiz)
- **ui.dev:** "React Query" kursu (ücretli, çok kaliteli)
:::
