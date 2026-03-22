---
title: "Next.js ve Framework Karşılaştırma"
id: "mod-07-react/lesson-03"
estimated_minutes: 55
order: 3
tags: ["nextjs", "app-router", "server-components", "ssr", "ssg", "isr", "deployment"]
prerequisites: ["mod-07-react/lesson-01", "mod-07-react/lesson-02"]
---

# Next.js ve Framework Karşılaştırma

:::realworld
Saf React ile bir uygulama yazdığında, SEO desteği yok, ilk yükleme yavaş (tüm JS indirilmeli) ve routing/data fetching gibi her şeyi kendin kurmalısın. Next.js, bu sorunları çözmek için React üzerine inşa edilmiş bir full-stack framework'tür. Vercel tarafından geliştirilen Next.js, günümüzde React ekosisteminin fiili standart framework'üdür. React resmi docs bile "production'da Next.js kullan" der. Bu derste Next.js'in mimarisini, rendering stratejilerini ve deployment sürecini öğreneceksin.
:::

## Next.js Nedir?

Next.js, React tabanlı bir full-stack web framework'üdür. React'in sunmadığı birçok özelliği kutudan çıkar çıkmaz sunar:

:::comparison
| Özellik | Saf React (Vite) | Next.js |
|---------|-------------------|---------|
| Routing | react-router (kendin kur) | File-based routing (otomatik) |
| Server-Side Rendering | Yok | Kutudan çıkar |
| SEO | Zayıf (client-side render) | Güçlü (SSR/SSG ile) |
| API Routes | Ayrı backend gerekir | Built-in API routes |
| Image Optimization | Kendin yap | next/image ile otomatik |
| Code Splitting | Manuel lazy() | Otomatik (sayfa bazlı) |
| Data Fetching | useEffect ile | Server Components, fetch cache |
| Deployment | Manuel konfigürasyon | Vercel ile tek tık |
| **Ne zaman kullan** | SPA, dashboard, internal tool | Web sitesi, e-ticaret, blog, SaaS |
:::

:::code[bash]{title="Next.js Proje Oluşturma"}
# 📌 2026: pnpm önerilen paket yöneticisi
pnpm dlx create-next-app@latest my-app --typescript --tailwind --app --src-dir
cd my-app
pnpm dev  # http://localhost:3000
:::

## App Router vs Pages Router

Next.js'in iki routing sistemi var. **App Router** (Next.js 13.4+) yeni standarttır, **Pages Router** eski projeler için korunur.

:::code[text]{title="App Router Dosya Yapısı"}
src/app/
├── layout.tsx          # Root layout (tüm sayfaları sarar)
├── page.tsx            # Ana sayfa (/)
├── loading.tsx         # Loading UI (otomatik Suspense)
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 sayfası
├── globals.css
├── about/
│   └── page.tsx        # /about
├── blog/
│   ├── page.tsx        # /blog
│   └── [slug]/
│       └── page.tsx    # /blog/:slug (dynamic route)
├── dashboard/
│   ├── layout.tsx      # Dashboard layout (nested)
│   ├── page.tsx        # /dashboard
│   └── settings/
│       └── page.tsx    # /dashboard/settings
└── api/
    └── users/
        └── route.ts    # API: GET/POST /api/users
:::

:::code[tsx]{title="App Router - Layout ve Page"}
// src/app/layout.tsx - Root Layout (HER sayfada çalışır)
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "My App",
  description: "Next.js ile yapılmış uygulama",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr">
      <body>
        <nav>
          <a href="/">Ana Sayfa</a>
          <a href="/blog">Blog</a>
        </nav>
        <main>{children}</main>
        <footer>Footer</footer>
      </body>
    </html>
  );
}

// src/app/page.tsx - Ana Sayfa
export default function Home() {
  return (
    <div>
      <h1>Ana Sayfa</h1>
      <p>Next.js App Router ile!</p>
    </div>
  );
}

// src/app/blog/[slug]/page.tsx - Dynamic Route
interface BlogPostProps {
  params: Promise<{ slug: string }>;
}

export default async function BlogPost({ params }: BlogPostProps) {
  const { slug } = await params;

  // Server Component: doğrudan fetch (useEffect gerek yok!)
  const res = await fetch(`https://api.example.com/posts/${slug}`);
  const post = await res.json();

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// Dynamic metadata
export async function generateMetadata({ params }: BlogPostProps): Promise<Metadata> {
  const { slug } = await params;
  const post = await fetch(`https://api.example.com/posts/${slug}`).then((r) => r.json());
  return { title: post.title, description: post.excerpt };
}
:::

:::beginner-mistake
Yaygın hata: App Router'da Pages Router syntax'ı kullanmak. App Router'da `getServerSideProps`, `getStaticProps` gibi fonksiyonlar yoktur. Bunun yerine Server Components ile doğrudan async/await kullanırsın. Ayrıca `_app.tsx` ve `_document.tsx` yerine `layout.tsx` kullanılır.
:::

## Server Components vs Client Components

Next.js App Router'da component'ler varsayılan olarak **Server Component**'tir. Tarayıcıda çalışmaz, sunucuda render edilir ve HTML olarak gönderilir.

:::comparison
| Özellik | Server Component (varsayılan) | Client Component ("use client") |
|---------|-------------------------------|----------------------------------|
| Nerede çalışır | Sunucuda | Tarayıcıda (+ SSR) |
| JavaScript gönderir mi | Hayır (sadece HTML) | Evet (JS bundle'a dahil) |
| useState/useEffect | Kullanamaz | Kullanabilir |
| Event handler (onClick) | Kullanamaz | Kullanabilir |
| Veritabanı erişimi | Doğrudan (import prisma) | API üzerinden |
| async/await | Doğrudan (async function) | useEffect ile |
| **Ne zaman kullan** | Data fetch, markdown render, ağır hesaplama | Form, interaktif UI, state gerektiren bölümler |
:::

:::code[tsx]{title="Server vs Client Component Kullanımı"}
// Server Component (varsayılan - "use client" yok)
// Bu component sunucuda çalışır, 0 KB JavaScript gönderir
import { db } from "@/lib/db";

export default async function ProductList() {
  // Doğrudan veritabanı sorgusu (tarayıcıya hiç gitmez!)
  const products = await db.product.findMany({
    orderBy: { createdAt: "desc" },
    take: 20,
  });

  return (
    <div>
      <h1>Ürünler ({products.length})</h1>
      {products.map((product) => (
        <div key={product.id}>
          <h2>{product.name}</h2>
          <p>{product.price} TL</p>
          {/* Client component'i Server component içinde kullanabilirsin */}
          <AddToCartButton productId={product.id} />
        </div>
      ))}
    </div>
  );
}

// Client Component - interaktif kısımlar için
// src/components/AddToCartButton.tsx
"use client";  // Bu satır ZORUNLU - client component olduğunu belirtir

import { useState } from "react";

export function AddToCartButton({ productId }: { productId: number }) {
  const [added, setAdded] = useState(false);

  const handleClick = async () => {
    await fetch("/api/cart", {
      method: "POST",
      body: JSON.stringify({ productId }),
    });
    setAdded(true);
  };

  return (
    <button onClick={handleClick} disabled={added}>
      {added ? "Sepete Eklendi" : "Sepete Ekle"}
    </button>
  );
}
:::

:::deha-tip
Server Component'ler ile Client Component'ler arasındaki sınırı doğru çizmek Next.js'in en kritik tasarım kararıdır. Kural: Mümkün olduğunca Server Component kullan, sadece interaktivite gereken yerlerde Client Component'e geç. Bir sayfanın %80'i Server Component, %20'si Client Component olmalı. "use client" eklediğin component ve altındaki TÜM import'lar client bundle'a dahil olur - bu yüzden "use client"'ı mümkün olduğunca yaprak component'lere koy.
:::

## SSR, SSG, ISR Karşılaştırma

:::concept[Rendering Stratejileri]
Next.js, sayfanın ne zaman render edileceğini belirleyen farklı stratejiler sunar. Doğru stratejiyi seçmek performans ve SEO için kritiktir.

**SSR (Server-Side Rendering):** Her istekte sunucuda render edilir
**SSG (Static Site Generation):** Build zamanında render edilir, CDN'den sunulur
**ISR (Incremental Static Regeneration):** Static + belirli aralıklarla yenilenir
:::

:::comparison
| Strateji | Ne Zaman Render | Performans | Veri Tazeliği | Kullanım Alanı |
|----------|-----------------|------------|---------------|----------------|
| SSG | Build zamanında | En hızlı (CDN) | Build'deki veri | Blog, docs, landing page |
| ISR | Build + interval | Çok hızlı (CDN + revalidate) | Ayarlanabilir | E-ticaret ürün sayfası |
| SSR | Her istekte | Yavaş (sunucu bekler) | Her zaman taze | Dashboard, profil |
| CSR | Tarayıcıda | İlk yükleme yavaş | API'den anlık | SPA, interaktif panel |
:::

:::code[tsx]{title="Next.js App Router - Data Fetching ve Caching"}
// 1. SSG - Static (varsayılan davranış)
// Build zamanında fetch edilir, sonucu cache'lenir
async function StaticPage() {
  const data = await fetch("https://api.example.com/data");
  // cache: "force-cache" varsayılandır (SSG davranışı)
  return <div>{/* render */}</div>;
}

// 2. SSR - Her istekte yeniden fetch
async function DynamicPage() {
  const data = await fetch("https://api.example.com/data", {
    cache: "no-store",  // Her istekte taze veri
  });
  return <div>{/* render */}</div>;
}

// 3. ISR - Belirli aralıklarla yenile
async function ISRPage() {
  const data = await fetch("https://api.example.com/data", {
    next: { revalidate: 60 },  // 60 saniyede bir yenile
  });
  return <div>{/* render */}</div>;
}

// 4. Static params ile dynamic route'lar (SSG)
// src/app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await fetch("https://api.example.com/posts").then((r) => r.json());

  return posts.map((post: { slug: string }) => ({
    slug: post.slug,
  }));
  // Build zamanında her slug için sayfa oluşturulur
}
:::

## API Routes ve Route Handlers

:::code[tsx]{title="API Route Handlers (App Router)"}
// src/app/api/users/route.ts
import { NextRequest, NextResponse } from "next/server";

// GET /api/users
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = searchParams.get("page") || "1";

  const users = await db.user.findMany({
    skip: (Number(page) - 1) * 10,
    take: 10,
  });

  return NextResponse.json(users);
}

// POST /api/users
export async function POST(request: NextRequest) {
  const body = await request.json();

  // Validation
  if (!body.name || !body.email) {
    return NextResponse.json(
      { error: "Name and email required" },
      { status: 400 }
    );
  }

  const user = await db.user.create({
    data: { name: body.name, email: body.email },
  });

  return NextResponse.json(user, { status: 201 });
}

// src/app/api/users/[id]/route.ts
// GET /api/users/:id
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const user = await db.user.findUnique({ where: { id: Number(id) } });

  if (!user) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  return NextResponse.json(user);
}
:::

## Middleware

Middleware, her istekten ONCE calisan kodtur. Authentication, redirect, rate limiting gibi cross-cutting concern'ler icin kullanilir.

:::code[tsx]{title="Next.js Middleware"}
// src/middleware.ts (proje kökünde!)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("session-token")?.value;
  const { pathname } = request.nextUrl;

  // 1. Auth kontrolü
  if (pathname.startsWith("/dashboard") && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // 2. Locale redirect
  if (pathname === "/") {
    const locale = request.headers.get("accept-language")?.split(",")[0] || "tr";
    if (locale.startsWith("en")) {
      return NextResponse.redirect(new URL("/en", request.url));
    }
  }

  // 3. Header ekleme
  const response = NextResponse.next();
  response.headers.set("x-custom-header", "my-value");

  return response;
}

// Hangi path'lerde çalışacağını belirt
export const config = {
  matcher: ["/dashboard/:path*", "/api/:path*", "/"],
};
:::

## Data Fetching Patterns

:::code[tsx]{title="Modern Data Fetching (App Router)"}
// 1. Parallel data fetching (Promise.all ile)
async function Dashboard() {
  // Her ikisi paralel çalışır - toplam süre en yavaş olanın süresi kadar
  const [user, orders] = await Promise.all([
    fetch("/api/user").then((r) => r.json()),
    fetch("/api/orders").then((r) => r.json()),
  ]);

  return (
    <div>
      <h1>Merhaba, {user.name}</h1>
      <p>Sipariş sayısı: {orders.length}</p>
    </div>
  );
}

// 2. Streaming ile progressive loading
// layout.tsx'te loading.tsx otomatik Suspense boundary oluşturur

// src/app/dashboard/loading.tsx
export default function Loading() {
  return <div className="skeleton">Yükleniyor...</div>;
}

// 3. Server Actions (form submission)
// src/app/contact/page.tsx
export default function ContactPage() {
  async function submitForm(formData: FormData) {
    "use server";  // Server Action

    const name = formData.get("name") as string;
    const email = formData.get("email") as string;
    const message = formData.get("message") as string;

    await db.contact.create({
      data: { name, email, message },
    });

    // revalidatePath("/contact");  // Cache'i yenile
  }

  return (
    <form action={submitForm}>
      <input name="name" required />
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit">Gönder</button>
    </form>
  );
}
:::

## Deployment

:::comparison
| Platform | Avantaj | Dezavantaj | Fiyat |
|----------|---------|-----------|-------|
| **Vercel** | Next.js'in yapımcısı, en iyi destek, Edge Functions | Vendor lock-in riski, pahalı olabilir | Hobby: Ücretsiz, Pro: $20/ay |
| **Netlify** | Kolay, CDN, serverless functions | Next.js desteği tam değil | Starter: Ücretsiz |
| **AWS Amplify** | AWS ekosistemi, ölçeklenebilir | Kurulum karmaşık | Kullanıma göre |
| **Docker + VPS** | Tam kontrol, ucuz | Her şeyi kendin yönet | ~$5-20/ay |
| **Railway** | Kolay deployment, database dahil | Küçük free tier | Kullanıma göre |
:::

:::code[bash]{title="Vercel Deployment"}
# 1. Vercel CLI ile
pnpm add -g vercel
vercel  # İlk deployment (guided setup)
vercel --prod  # Production deployment

# 2. GitHub entegrasyonu (önerilen)
# GitHub'a push et -> Vercel otomatik deploy eder
# Her PR için preview deployment oluşturur

# 3. Docker ile self-hosted
# Dockerfile
# FROM node:20-alpine AS builder
# WORKDIR /app
# COPY package*.json pnpm-lock.yaml ./
# RUN corepack enable && pnpm install --frozen-lockfile
# COPY . .
# RUN pnpm build
#
# FROM node:20-alpine
# WORKDIR /app
# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/node_modules ./node_modules
# COPY --from=builder /app/package.json ./
# EXPOSE 3000
# CMD ["node", "server.js"]
:::

## Framework Karşılaştırma: React vs Vue vs Angular vs Svelte

:::comparison
| Özellik | React + Next.js | Vue + Nuxt | Angular | Svelte + SvelteKit |
|---------|----------------|------------|---------|-------------------|
| Öğrenme eğrisi | Orta | Kolay | Zor (çok kavram) | Kolay |
| Ekosistem | En büyük | Büyük | Büyük (enterprise) | Büyüyen |
| İş ilanı | En çok | Orta | Orta-çok (enterprise) | Az (büyüyor) |
| Bundle boyutu | Orta (~40KB) | Küçük (~33KB) | Büyük (~65KB) | En küçük (~2KB) |
| Yaklaşım | Library + ekosistem | Progressive framework | Full framework (opinionated) | Compiler (no virtual DOM) |
| TypeScript | Çok iyi (JSX/TSX) | Çok iyi (Vue 3) | Native (TypeScript zorunlu) | İyi |
| State yönetimi | Zustand, Redux, Jotai | Pinia (built-in) | NgRx, Signals | Stores (built-in) |
| SSR framework | Next.js | Nuxt | Angular Universal | SvelteKit |
| Şirket desteği | Meta | Evan You + sponsors | Google | Rich Harris + Vercel |
| **Tavsiye** | Genel amaçlı, iş bulmak için en iyi | Vue severlere, hızlı prototip | Enterprise, büyük ekipler | Performans odaklı, yeni projeler |
:::

:::deha-tip
Bir framework'ü "en iyi" ilan etmek anlamsızdır - her birinin güçlü olduğu alan farklıdır. Ancak Türkiye ve dünya iş piyasası açısından bakıldığında, React bilmek en çok kapıyı açar. Vue daha kolay öğrenilir ama iş ilanı daha az, Angular enterprise'da güçlü ama öğrenme eğrisi dik, Svelte ise performans canavarı ama ekosistem henüz küçük. Kariyer stratejin: React'i ana silahın yap, sonra bir tane daha öğren (Vue veya Svelte).
:::

:::interview
**Mülakat Sorusu:** "SSR, SSG ve CSR arasındaki farkları açıklayın. Hangisini ne zaman kullanırsınız?"

**Beklenen cevap:**
- **SSR (Server-Side Rendering):** Her istekte sunucuda HTML oluşturulur. Avantaj: her zaman taze veri, SEO uyumlu. Dezavantaj: sunucu yükü, TTFB yüksek. Kullanım: dashboard, profil sayfası.
- **SSG (Static Site Generation):** Build zamanında HTML oluşturulur, CDN'den sunulur. Avantaj: en hızlı, sunucu yükü yok. Dezavantaj: veri eski kalabilir. Kullanım: blog, docs, landing page.
- **CSR (Client-Side Rendering):** Tarayıcıda JavaScript ile render edilir. Avantaj: interaktif, API-driven. Dezavantaj: ilk yükleme yavaş, SEO zayıf. Kullanım: SPA, admin panel.
- **ISR (Incremental Static Regeneration):** SSG + belirli aralıklarla yenileme. Avantaj: hızlı + güncel. Kullanım: e-ticaret ürün sayfası.
- Kural: SEO önemliyse SSR/SSG, interaktivite önemliyse CSR, ikisi de önemliyse ISR.
:::

:::knowledge-check
type: multiple_choice
question: "Next.js App Router'da bir component varsayılan olarak nedir?"
options:
  - "Client Component"
  - "Server Component"
  - "Hybrid Component"
  - "Static Component"
correct: 1
explanation: "App Router'da tüm component'ler varsayılan olarak Server Component'tir. Client Component yapmak için dosyanın başına 'use client' direktifi eklemelisin. Server Component'ler sunucuda çalışır, 0 KB JavaScript gönderir ve doğrudan veritabanına erişebilir."
:::

:::knowledge-check
type: multiple_choice
question: "Bir blog sayfası için en uygun rendering stratejisi hangisidir?"
options:
  - "CSR - çünkü her zaman taze olmalı"
  - "SSR - çünkü SEO önemli"
  - "SSG - çünkü içerik nadiren değişir ve CDN'den çok hızlı sunulur"
  - "ISR - çünkü blog her saniye güncellenir"
correct: 2
explanation: "Blog yazıları nadiren değişir ve SEO kritiktir. SSG ile build zamanında HTML oluşturulur ve CDN'den sunulur - en hızlı stratejidir. İçerik güncellendiğinde yeniden build yapılır veya ISR ile revalidate süresi ayarlanır."
:::

:::exercise
### Alistirma 1: Next.js App Router ile Blog Sayfalari (Kolay)

Next.js App Router kullanarak 3 sayfali bir blog uygulamasi olustur: ana sayfa, blog listesi ve dinamik blog detay.

```tsx
// app/page.tsx — Ana Sayfa (Server Component)
export default function HomePage() {
  return (
    <main>
      <h1>Blogum</h1>
      <p>Hosgeldiniz!</p>
      {/* TODO: Link component'i ile /blog sayfasina yonlendir */}
    </main>
  );
}

// app/blog/page.tsx — Blog Listesi (Server Component)
// TODO: Fetch ile blog listesi cek (JSONPlaceholder veya mock data)
const posts = [
  { slug: "nextjs-giris", title: "Next.js Giris", excerpt: "Next.js nedir?" },
  { slug: "react-hooks", title: "React Hooks", excerpt: "Hooks rehberi" },
  { slug: "typescript", title: "TypeScript", excerpt: "TS temelleri" },
];

export default function BlogPage() {
  return (
    <div>
      <h1>Blog Yazilari</h1>
      {/* TODO: posts.map ile kart listesi render et */}
      {/* Her kart Link ile /blog/[slug] sayfasina yonlendirmeli */}
    </div>
  );
}

// app/blog/[slug]/page.tsx — Blog Detay (Dynamic Route)
// TODO: params'dan slug al ve ilgili yaziyi goster
export default function BlogPost({ params }: { params: { slug: string } }) {
  // TODO: slug'a gore yaziyi bul (veya fetch et)
  return (
    <article>
      <h1>{params.slug}</h1>
      {/* TODO: Yazi icerigi */}
    </article>
  );
}
```

**Beklenen Sonuc:** / ana sayfa, /blog liste, /blog/nextjs-giris detay sayfasi gorunmeli. Dynamic routing calismali. Server Component'te veri fetch edilmeli.
**Ipucu:** `npx create-next-app@latest --typescript --tailwind --app` ile proje olustur. Link icin `import Link from "next/link"`.

---

### Alistirma 2: Server ve Client Component Ayrimi (Orta)

Ayni sayfada Server Component (veri cekme) ve Client Component (interaktivite) birlikte kullan.

```tsx
// app/blog/[slug]/page.tsx — Server Component
import { LikeButton } from "@/components/LikeButton";

async function getPost(slug: string) {
  // TODO: Fetch ile blog yazisini cek
  // Server Component icinde dogrudan await kullanabilirsin
  const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${slug}`, {
    next: { revalidate: 60 }, // ISR: 60 saniyede bir yenile
  });
  return res.json();
}

export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.body}</p>
      {/* Client Component — interaktif */}
      <LikeButton postId={post.id} />
    </article>
  );
}

// components/LikeButton.tsx — Client Component
"use client";
import { useState } from "react";

export function LikeButton({ postId }: { postId: number }) {
  const [likes, setLikes] = useState(0);
  const [liked, setLiked] = useState(false);

  // TODO: Begeni toggle et
  // TODO: Begenmis ise kalp dolu, degilse bos goster
  // TODO: Animasyonlu transition ekle

  return (
    <button onClick={() => {/* TODO */}}>
      {liked ? "❤️" : "🤍"} {likes}
    </button>
  );
}
```

**Beklenen Sonuc:** Sayfa Server Component olarak render edilmeli (JavaScript bundle'a eklenmemeli). Sadece LikeButton client-side calismali. ISR ile 60 saniyede bir yenilenmeli.
**Ipucu:** "use client" direktifi sadece interaktif component'lere ekle. Veri cekme islemlerini Server Component'te yap.

---

### Alistirma 3: API Route ve Middleware (Zor)

Next.js API route ile REST endpoint olustur ve middleware ile auth kontrolu ekle.

```tsx
// app/api/posts/route.ts — API Route
import { NextResponse } from "next/server";

const posts = [
  { id: 1, title: "Next.js Giris", content: "...", author: "Ahmet" },
  { id: 2, title: "React Hooks", content: "...", author: "Ayse" },
];

export async function GET(request: Request) {
  // TODO: Query parametrelerini oku (?search=next&limit=10)
  // TODO: Filtreleme ve pagination uygula
  return NextResponse.json({ posts, total: posts.length });
}

export async function POST(request: Request) {
  // TODO: Body'den yeni post verisini oku
  // TODO: Basit validasyon yap (title ve content zorunlu)
  // TODO: Yeni post'u ekle ve 201 dondur
  const body = await request.json();
  // ...
  return NextResponse.json({ post: newPost }, { status: 201 });
}

// middleware.ts — Auth Middleware
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // TODO: /dashboard ile baslayan route'larda auth kontrolu yap
  // TODO: Cookie veya header'dan token kontrol et
  // TODO: Token yoksa /login'e yonlendir
  const token = request.cookies.get("auth-token");

  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    if (!token) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

**Beklenen Sonuc:** GET /api/posts filtreleme ve pagination ile calismali. POST /api/posts yeni yazi eklemeli. /dashboard'a token olmadan erismeye calisinca /login'e yonlendirmeli.
**Ipucu:** `new URL(request.url).searchParams` ile query parametrelerini oku. Middleware sadece edge runtime'da calisir.
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "Next.js App Router'da Server Components ve Client Components arasindaki siniri nasil cizersin? 'use client' direktifini nereye koydugun bundle size'i nasil etkiler? Bir sayfada %80 Server Component, %20 Client Component olmasi icin component agacini nasil tasarlarim? Gercek orneklerle acikla."

**2. Pratik Uygulama:**
> "Next.js App Router ile bir blog uygulamasi olustur: SSG ile blog listesi (generateStaticParams), ISR ile blog detay (revalidate: 60), Server Component'te dogrudan fetch, Client Component ile begeni butonu (useState), dynamic metadata ve loading.tsx ile skeleton UI. Tum dosya yapisini ve kodlari ver."
> Takip: "Simdi bu blog'a Server Actions ile yorum ekleme ozelligi ekle. API route yerine 'use server' kullan ve optimistic update ile UI'i aninda guncelle."

**3. Mukemmellik Icin:**
> "Bir e-ticaret sitesinde farkli sayfalarda farkli rendering stratejileri kullanmam gerekiyor: ana sayfa SSG, urun listesi ISR (30s), urun detay ISR (60s), sepet CSR, profil SSR. Next.js App Router'da bu hybrid stratejiyi nasil implemente ederim? Cache katmanlarini (browser, CDN, data cache, full route cache) nasil yonetirim?"

### Pair Programming Ipucu
Next.js projelerinde AI'a build output veya deployment loglarini goster ve sor: "Build ciktisinda hangi sayfalar static, hangisi dynamic render ediliyor? Bekledigim stratejiyle uyusuyor mu? Yanlis render edilen sayfalari nasil duzeltirim?"
:::

:::exercise
### Alıştırma 4: Next.js Dosya Yapısı ve Routing
**Görev:** Aşağıdaki URL yapısı için gerekli dosya/klasör yapısını oluştur.
**Başlangıç kodu:**
```
Gerekli URL'ler:
/                    → Ana sayfa
/about               → Hakkımızda
/blog                → Blog listesi
/blog/[slug]         → Blog detay
/dashboard           → Dashboard (layout ile sidebar)
/dashboard/settings  → Dashboard ayarlar
/dashboard/profile   → Dashboard profil

TODO: app/ klasörü altında dosya yapısını oluştur
app/
  ???
```
**Beklenen çıktı:**
```
app/
  layout.tsx          ← Genel layout (navbar, footer)
  page.tsx            ← / (Ana sayfa)
  about/
    page.tsx          ← /about
  blog/
    page.tsx          ← /blog (liste)
    [slug]/
      page.tsx        ← /blog/merhaba-dunya
  dashboard/
    layout.tsx        ← Dashboard layout (sidebar)
    page.tsx          ← /dashboard
    settings/
      page.tsx        ← /dashboard/settings
    profile/
      page.tsx        ← /dashboard/profile
```
**İpucu:** Her `page.tsx` bir route oluşturur. `layout.tsx` alt route'ları sarar. `[slug]` dynamic segment'tir.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 5: Server Component vs Client Component
**Görev:** Aşağıdaki component'lerin hangisinin Server, hangisinin Client Component olması gerektiğini belirle ve nedenini açıkla.
**Başlangıç kodu:**
```tsx
// Component 1: Blog yazısı görüntüleme
function BlogPost({ slug }: { slug: string }) {
  // Veritabanından blog yazısını çek
  // Markdown'ı HTML'e çevir
  // Statik içerik göster
}

// Component 2: Beğeni butonu
function LikeButton({ postId }: { postId: string }) {
  // Tıklanınca beğeni sayısını artır
  // Beğeni animasyonu göster
}

// Component 3: Yorum listesi
function CommentList({ postId }: { postId: string }) {
  // Veritabanından yorumları çek
  // Statik liste olarak göster
}

// Component 4: Yorum formu
function CommentForm({ postId }: { postId: string }) {
  // Input state'i yönet
  // Form submit et
}

// Component 5: Navigasyon çubuğu
function Navbar() {
  // Aktif sayfayı vurgula (usePathname)
  // Hamburger menü toggle (useState)
}
```
**Beklenen çıktı:**
```
Component 1: SERVER ✓ - DB erişimi var, state/event yok, async olabilir
Component 2: CLIENT ✓ - onClick event, useState gerekli → "use client"
Component 3: SERVER ✓ - DB erişimi var, interaktivite yok
Component 4: CLIENT ✓ - form state, onSubmit event → "use client"
Component 5: CLIENT ✓ - usePathname hook, useState → "use client"

Kural: State, event handler veya browser API kullanıyorsa → Client
       DB/API erişimi, statik render → Server (varsayılan)
```
**İpucu:** Varsayılan Server Component'tir. Sadece interaktivite gerektiğinde `"use client"` ekle. Server Component içinde Client Component kullanabilirsin ama tersi olmaz.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 6: SSR, SSG ve ISR Seçimi
**Görev:** Her sayfa için doğru rendering stratejisini seç ve Next.js kodunu yaz.
**Başlangıç kodu:**
```tsx
// Senaryo 1: Ürün listesi sayfası (fiyatlar saatte bir güncellenir)
// TODO: Hangi strateji? Kodu yaz.

// Senaryo 2: Blog yazısı (yayınlandıktan sonra nadiren değişir)
// TODO: Hangi strateji? Kodu yaz.

// Senaryo 3: Kullanıcı profil sayfası (her kullanıcı farklı görür)
// TODO: Hangi strateji? Kodu yaz.

// Senaryo 4: Hakkımızda sayfası (hiç değişmez)
// TODO: Hangi strateji? Kodu yaz.
```
**Beklenen çıktı:**
```tsx
// Senaryo 1: ISR (Incremental Static Regeneration) - 1 saat
export default async function ProductList() {
  const products = await fetch("https://api.example.com/products", {
    next: { revalidate: 3600 },
  }).then(res => res.json());
  return <div>{/* render */}</div>;
}

// Senaryo 2: SSG (Static Site Generation)
export async function generateStaticParams() {
  const posts = await fetch("https://api.example.com/posts").then(r => r.json());
  return posts.map((post: any) => ({ slug: post.slug }));
}

// Senaryo 3: SSR (Server-Side Rendering) - her istekte
export const dynamic = "force-dynamic";

// Senaryo 4: SSG (varsayılan - fetch yok veya cache)
// Next.js varsayılan olarak static render eder
```
**İpucu:** Hiç değişmeyen → SSG, Nadiren değişen → ISR (revalidate), Her kullanıcıya farklı → SSR (force-dynamic).
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 7: API Route Handler
**Görev:** Next.js App Router'da RESTful API route handler yaz.
**Başlangıç kodu:**
```tsx
// app/api/todos/route.ts

// TODO: GET - Tüm todo'ları getir
export async function GET(request: Request) {
  // URL'den search params al (?completed=true)
  // Filtrelenmiş todo listesini döndür
}

// TODO: POST - Yeni todo oluştur
export async function POST(request: Request) {
  // Body'den title al
  // Validasyon yap (boş olamaz)
  // Yeni todo oluştur ve döndür
}

// app/api/todos/[id]/route.ts

// TODO: DELETE - Todo sil
export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  // id'ye göre sil
}
```
**Beklenen çıktı:**
```tsx
// app/api/todos/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const completed = searchParams.get("completed");
  let todos = await db.todo.findMany();
  if (completed !== null) {
    todos = todos.filter(t => t.completed === (completed === "true"));
  }
  return Response.json(todos);
}

export async function POST(request: Request) {
  const { title } = await request.json();
  if (!title?.trim()) {
    return Response.json({ error: "Title gerekli" }, { status: 400 });
  }
  const todo = await db.todo.create({ data: { title, completed: false } });
  return Response.json(todo, { status: 201 });
}

// app/api/todos/[id]/route.ts
export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  await db.todo.delete({ where: { id: params.id } });
  return new Response(null, { status: 204 });
}
```
**İpucu:** `Response.json()` ile JSON döndür. URL search params için `new URL(request.url).searchParams` kullan. Status code'ları: 200 başarı, 201 oluşturuldu, 204 içerik yok, 400 hatalı istek.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 8: Next.js Middleware
**Görev:** Middleware ile authentication kontrolü ve redirect yapan bir sistem yaz.
**Başlangıç kodu:**
```tsx
// middleware.ts (proje kökünde)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // TODO 1: /dashboard ile başlayan yollar için token kontrolü
  // Cookie'den "auth-token" oku
  // Token yoksa /login'e yönlendir

  // TODO 2: /login sayfasına gelen kullanıcı zaten giriş yapmışsa
  // /dashboard'a yönlendir

  // TODO 3: Tüm response'lara custom header ekle
}

// TODO: Middleware'in hangi yollarda çalışacağını belirle
export const config = {
  matcher: [/* ? */],
};
```
**Beklenen çıktı:**
```tsx
export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token")?.value;
  const { pathname } = request.nextUrl;

  if (pathname.startsWith("/dashboard") && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (pathname === "/login" && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  const response = NextResponse.next();
  response.headers.set("x-custom-header", "my-app");
  return response;
}

export const config = {
  matcher: ["/dashboard/:path*", "/login"],
};
```
**İpucu:** `request.cookies.get()` ile cookie oku. `NextResponse.redirect()` ile yönlendir. `matcher` ile middleware'in çalışacağı yolları belirle.
**Zorluk:** Orta
:::

:::exercise
### Alıştırma 9: Loading ve Error UI
**Görev:** Next.js'in loading.tsx ve error.tsx dosyalarını kullanarak UX-dostu yükleme ve hata ekranları oluştur.
**Başlangıç kodu:**
```tsx
// app/products/loading.tsx
// TODO: Skeleton loader oluştur (ürün kartları için)

// app/products/error.tsx
// TODO: Error boundary component'i yaz
// "use client" gerekli!
// error ve reset props'larını al
// Kullanıcıya hata mesajı ve "Tekrar Dene" butonu göster

// app/products/not-found.tsx
// TODO: 404 sayfası oluştur
```
**Beklenen çıktı:**
```tsx
// loading.tsx
export default function Loading() {
  return (
    <div className="grid grid-cols-3 gap-4">
      {[1, 2, 3].map(i => (
        <div key={i} className="animate-pulse">
          <div className="bg-gray-700 h-48 rounded-lg" />
          <div className="bg-gray-700 h-4 mt-2 rounded w-3/4" />
          <div className="bg-gray-700 h-4 mt-1 rounded w-1/2" />
        </div>
      ))}
    </div>
  );
}

// error.tsx
"use client";
export default function Error({ error, reset }: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="text-center py-10">
      <h2 className="text-xl text-red-400">Bir hata oluştu</h2>
      <p className="text-gray-400 mt-2">{error.message}</p>
      <button onClick={reset} className="mt-4 bg-blue-500 text-white px-4 py-2 rounded">
        Tekrar Dene
      </button>
    </div>
  );
}

// not-found.tsx
export default function NotFound() {
  return (
    <div className="text-center py-20">
      <h1 className="text-4xl font-bold text-gray-300">404</h1>
      <p className="text-gray-500 mt-2">Sayfa bulunamadı</p>
    </div>
  );
}
```
**İpucu:** `loading.tsx` otomatik Suspense boundary oluşturur. `error.tsx` client component olmalı ve `reset` fonksiyonu ile yeniden deneme sağlar. `animate-pulse` Tailwind ile skeleton efekti.
**Zorluk:** Kolay
:::

:::exercise
### Alıştırma 10: Server Actions ile Form İşlemi
**Görev:** Next.js Server Actions kullanarak veritabanına veri ekleyen bir form yaz (API route'a gerek yok).
**Başlangıç kodu:**
```tsx
// app/actions.ts
"use server";

// TODO: Server action fonksiyonu yaz
// FormData alıp veritabanına kaydetsin
// Zod ile validasyon yapsın
// Hata durumunda mesaj döndürsün
// Başarıda revalidatePath çağırsın

// app/contact/page.tsx
// TODO: Server action'ı kullanan form component'i yaz
// useFormStatus ile loading durumu göster
// useFormState ile hata/başarı mesajı göster
```
**Beklenen çıktı:**
```tsx
// app/actions.ts
"use server";
import { revalidatePath } from "next/cache";
import { z } from "zod";

const contactSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  message: z.string().min(10),
});

export async function submitContact(prevState: any, formData: FormData) {
  const parsed = contactSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
    message: formData.get("message"),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  await db.contact.create({ data: parsed.data });
  revalidatePath("/contact");
  return { success: true };
}

// app/contact/page.tsx
"use client";
import { useFormState, useFormStatus } from "react-dom";
import { submitContact } from "../actions";

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? "Gönderiliyor..." : "Gönder"}</button>;
}

export default function ContactPage() {
  const [state, formAction] = useFormState(submitContact, null);
  return (
    <form action={formAction}>
      <input name="name" />
      <input name="email" />
      <textarea name="message" />
      {state?.error && <p className="text-red-400">Hata var</p>}
      {state?.success && <p className="text-emerald-400">Gönderildi!</p>}
      <SubmitButton />
    </form>
  );
}
```
**İpucu:** Server Actions `"use server"` ile işaretlenir. `useFormStatus` form gönderilirken loading gösterir. `revalidatePath` ile cache temizlenir.
**Zorluk:** Zor
:::

:::must-note
- Next.js = React üzerine full-stack framework (routing, SSR, API, optimization kutudan çıkar)
- App Router (yeni standart): file-based routing, layout.tsx, page.tsx, loading.tsx, error.tsx
- Server Component (varsayılan): sunucuda render, 0 JS, async/await direkt, DB erişimi direkt
- Client Component ("use client"): useState/useEffect, onClick, tarayıcı API'leri kullanılabilir
- "use client" eklenen component + altındaki tüm import'lar client bundle'a girer
- SSG: build'de render, CDN'den sun (blog, docs) - fetch() varsayılan
- SSR: her istekte render (dashboard) - fetch({ cache: "no-store" })
- ISR: SSG + interval yenileme (e-ticaret) - fetch({ next: { revalidate: 60 } })
- generateStaticParams(): dynamic route'lar için build zamanında path listesi üret
- API Routes: src/app/api/xxx/route.ts, GET/POST/PUT/DELETE export et
- Middleware: src/middleware.ts, her istekten ONCE çalışır (auth, redirect, header)
- Server Actions: "use server" ile form submission sunucuda işle (API route'a gerek yok)
- metadata export ile sayfa bazlı SEO (title, description, og tags)
- loading.tsx = otomatik Suspense boundary, error.tsx = otomatik Error Boundary
- Deployment: Vercel (en kolay, Next.js yapımcısı), Docker + VPS (tam kontrol)
- Framework seçimi: React (iş piyasası), Vue (kolay), Angular (enterprise), Svelte (performans)
:::

:::senior-learns
Bir Senior Developer veya CTO, Next.js ve framework seçimi konusunu öğrenirken şu yaklaşımı benimser:

1. **Rendering stratejisini veri gereksinimlerine göre seçer** - Her sayfa için ayrı karar verir: ana sayfa SSG, ürün listesi ISR (60s), sepet CSR, profil SSR. Tek bir strateji tüm uygulamaya uygulanmaz.
2. **Server/Client component sınırını mimari seviyede planlar** - Component ağacında "use client" sınırlarını önceden çizer. Leaf component'leri (butonlar, form'lar) client, container component'leri (page, layout) server yapar. Bu karar bundle size'ı doğrudan etkiler.
3. **Cache stratejisini katmanlı düşünür** - Browser cache, CDN cache, Next.js data cache, full route cache. Her katmanı anlar ve revalidation stratejisini buna göre kurar. Stale-while-revalidate pattern'ını uygular.
4. **Framework vendor lock-in riskini değerlendirir** - "Vercel'e bağımlı mıyız? Self-host edebilir miyiz?" sorularını sorar. Docker ile self-hosting opsiyonunu her zaman hazır tutar. Edge Runtime vs Node.js Runtime tercihini bilinçli yapar.
5. **Monitoring ve observability kurar** - Vercel Analytics, Sentry, OpenTelemetry ile production performansını izler. Core Web Vitals (LCP, FID, CLS) metriklerini dashboard'da takip eder.
6. **Framework seçimini ekip yetkinliğine göre yapar** - En iyi framework, ekibin en verimli kullanabildiği framework'tür. Yeni bir teknolojiye geçiş maliyetini (eğitim, refactor, hata riski) hesaplar.

**Profesyonel Mindset:** "Framework seçimi teknik bir karar olduğu kadar iş kararıdır. React + Next.js seçerken sadece 'popüler' olduğu için değil, büyük bir yetenek havuzu, zengin ekosistem ve kanıtlanmış production performansı sunduğu için seçersin. Ancak her zaman alternatifi bil - Vue, Svelte veya hatta plain HTML/CSS+JS bazen doğru cevaptır."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Server-Side Rendering (SSR)** (sɜːr-vər saɪd ren-dər-ɪŋ) → Sunucu taraflı işleme
   *"SSR generates the HTML on each request, ensuring fresh data for every page load."*

2. **Static Site Generation (SSG)** → Statik site oluşturma
   *"SSG pre-renders pages at build time, resulting in extremely fast page loads from the CDN."*

3. **Middleware** (mɪd-əl-weər) → Ara katman yazılımı
   *"Middleware runs before the request is completed, useful for authentication and redirects."*

4. **Route Handler** (ruːt hænd-lər) → Yol işleyici
   *"Route handlers in Next.js allow you to create API endpoints using the Web Request and Response APIs."*

5. **Deployment** (dɪ-plɔɪ-mənt) → Dağıtım / Yayınlama
   *"Vercel provides zero-configuration deployment for Next.js applications."*

**Okuma Egzersizi:** Next.js resmi docs'tan "Getting Started" bölümünü İngilizce oku: https://nextjs.org/docs/getting-started

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Next.js App Router ile blog sayfası oluşturuldu"
-> Örnek: `feat: create blog page with Next.js App Router`
:::

:::external-resource
- Next.js Resmi Docs: https://nextjs.org/docs (interaktif, ücretsiz)
- Next.js Learn: https://nextjs.org/learn (resmi tutorial, ücretsiz)
- Lee Robinson YouTube: Next.js core maintainer'dan videolar
- Vercel Templates: https://vercel.com/templates (hazır projeler)
- Vue.js Docs: https://vuejs.org (karşılaştırma için)
- Svelte Tutorial: https://learn.svelte.dev (karşılaştırma için)
:::
