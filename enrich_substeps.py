#!/usr/bin/env python3
"""
Second pass: enrich all remaining steps to have 12-15 substeps each,
following the senior dev flow pattern.
"""
import json

with open('content/projects/project-01.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Helper to find milestone index
def find_milestone(mid):
    for i, m in enumerate(data['milestones']):
        if m.get('id') == mid:
            return i
    # For deployment milestone without proper id
    for i, m in enumerate(data['milestones']):
        if m.get('title', '').startswith('Deployment'):
            return i
    return None

# ============================================================================
# M2 S1: Hero Section - add commit step to reach 10
# ============================================================================
m2_idx = find_milestone('p01-m2')

# M2 S6: Blog yazıları - rewrite with proper flow
m2_s6 = [
    {"order":"6.1","action":"İlk blog yazısı dosyasını oluştur","type":"file_open","file":"content/blog/nextjs-portfolio-rehberi.mdx","why":"Dosya adı URL slug'ı olacak: /blog/nextjs-portfolio-rehberi. Küçük harf ve tire kullan, Türkçe karakter kullanma — URL'lerde özel karakterler sorun çıkarabilir."},
    {"order":"6.2","action":"Önce frontmatter'ı yaz — metadata kısmı","type":"code_write","file":"content/blog/nextjs-portfolio-rehberi.mdx","code":"---\ntitle: 'Next.js 16 App Router ile Portfolio Sitesi Oluşturma'\ndate: '2026-01-15'\nsummary: 'Next.js 16 App Router, Server Components ve MDX kullanarak modern bir portfolio sitesi nasıl oluşturulur?'\ntags: ['Next.js', 'React', 'TypeScript']\n---","why":"Frontmatter (--- arasındaki YAML), M2 Step 2'de yazdığımız gray-matter'ın parse edeceği metadata. title, date, summary ve tags alanları zorunlu — getAllPosts bunlara bağımlı."},
    {"order":"6.3","action":"Frontmatter'ın ALTINA içeriği ekle","type":"code_add","file":"content/blog/nextjs-portfolio-rehberi.mdx","position":"bottom","code":"\n# Next.js 16 App Router ile Portfolio Sitesi Oluşturma\n\nBu yazıda, Next.js 16'ün yeni App Router yapısıyla nasıl bir portfolio sitesi oluşturabileceğini adım adım anlatacağım.\n\n## Neden Next.js?\n\nNext.js, React tabanlı framework'ler arasında en popüleridir. Server Components desteği ile performans avantajı sağlar...\n\n## Kurulum\n\n```bash\npnpm dlx create-next-app@latest my-portfolio --tailwind\n```\n\n## Server Components vs Client Components\n\nApp Router'da tüm component'ler varsayılan olarak Server Component'tir...\n\n## Sonuç\n\nNext.js 16, modern web geliştirme için güçlü araçlar sunar...","why":"İyi blog yazısı: 1) Problemi tanımlar, 2) Çözümü açıklar, 3) Kod örnekleri verir, 4) Sonuç belirtir. ```bash ile syntax highlighting aktifleşir."},
    {"order":"6.4","action":"BAŞKA DOSYAYA geç — ikinci blog yazısını oluştur","type":"file_open","file":"content/blog/typescript-temelleri.mdx","why":"En az 2 blog yazısı olmalı — boş blog kötü izlenim bırakır. Farklı konularda yazmak çeşitlilik gösterir."},
    {"order":"6.5","action":"İkinci yazının frontmatter'ını yaz","type":"code_write","file":"content/blog/typescript-temelleri.mdx","code":"---\ntitle: 'TypeScript Temelleri: Neden ve Nasıl?'\ndate: '2026-01-20'\nsummary: 'TypeScript nedir, neden kullanmalısın ve JavaScript projelerinde nasıl entegre edilir?'\ntags: ['TypeScript', 'JavaScript']\n---","why":"İkinci yazının tarihi ilkinden sonra olmalı — M2 Step 2'deki getAllPosts tarihe göre sıralar, en yeni en üstte görünür."},
    {"order":"6.6","action":"İkinci yazının içeriğini ekle","type":"code_add","file":"content/blog/typescript-temelleri.mdx","position":"bottom","code":"\n# TypeScript Temelleri: Neden ve Nasıl?\n\nTypeScript, JavaScript'in tip güvenli bir süper kümesidir.\n\n## TypeScript Nedir?\n\nTypeScript, Microsoft tarafından geliştirilen, JavaScript'e statik tip sistemi ekleyen bir programlama dilidir...\n\n## Temel Tipler\n\n```typescript\nlet name: string = 'John';\nlet age: number = 25;\nlet isActive: boolean = true;\n```\n\n## Interface ve Type\n\n```typescript\ninterface User {\n  name: string;\n  email: string;\n  age?: number;\n}\n```\n\n## Sonuç\n\nTypeScript, daha güvenilir ve bakımı kolay kod yazmayı sağlar...","why":"```typescript ile dil belirtmek M2 Step 2'de kurduğumuz rehype-highlight'ın doğru syntax highlighting uygulaması için şart."},
    {"order":"6.7","action":"/blog sayfasına dön — blog listesini kontrol et","type":"validate","validation":"/blog sayfasında iki yazı listelenmeli — 'TypeScript Temelleri' üstte (daha yeni tarih), 'Next.js Portfolio Rehberi' altta.","why":"6.1-6.6'da oluşturduğumuz MDX dosyalarının M2 Step 2'deki getAllPosts ve M2 Step 3'teki blog listesi ile düzgün çalıştığını doğruluyoruz."},
    {"order":"6.8","action":"Blog detay sayfasını kontrol et — syntax highlighting çalışıyor mu?","type":"validate","validation":"Blog listesinden bir yazıya tıkla. MDX içerik render edilmeli. Kod blokları syntax highlighting ile renkli görünmeli. prose class'ı ile tipografi düzgün olmalı.","why":"Uçtan uca test: dosya okuma -> parse -> listeleme -> detay render -> syntax highlighting zincirinin tamamı çalışmalı."},
    {"order":"6.9","action":"Ana sayfaya dön — son blog yazılarını göster","type":"code_modify","file":"src/app/page.tsx","code":"// page.tsx'in üstüne getRecentPosts import'unu ekle ve\n// Hero section'dan sonra son yazılar bölümü ekle","why":"M2 Step 2'de yazdığımız getRecentPosts fonksiyonunu ana sayfada kullanarak son 3 yazıyı göstereceğiz."},
    {"order":"6.10","action":"page.tsx'in ÜSTÜNE çık — getRecentPosts import'unu ekle","type":"code_add","file":"src/app/page.tsx","position":"top","code":"import { getRecentPosts } from '@/lib/mdx';","why":"M2 Step 2'de yazdığımız getRecentPosts fonksiyonunu import ediyoruz. Ana sayfada son blog yazılarını göstermek için kullanacağız."},
    {"order":"6.11","action":"HomePage'i async yap ve getRecentPosts'u çağır","type":"code_modify","file":"src/app/page.tsx","code":"export default async function HomePage() {\n  const recentPosts = await getRecentPosts(3);","why":"Server Component olduğu için async/await doğrudan kullanılabilir. 6.10'da import ettiğimiz getRecentPosts ile son 3 yazıyı çekiyoruz."},
    {"order":"6.12","action":"Hero section'dan SONRA son yazılar bölümünü ekle","type":"code_add","file":"src/app/page.tsx","position":"after_hero","code":"      {/* Son Blog Yazıları */}\n      <section className=\"mx-auto max-w-5xl px-4 py-16\">\n        <h2 className=\"mb-8 text-2xl font-bold text-gray-900 dark:text-white\">Son Yazılar</h2>\n        <div className=\"grid gap-6 md:grid-cols-3\">\n          {recentPosts.map((post) => (\n            <article key={post.slug} className=\"rounded-xl border border-gray-200 p-6 transition-shadow hover:shadow-lg dark:border-gray-800\">\n              <time className=\"text-sm text-gray-500\">{post.date}</time>\n              <h3 className=\"mt-2 text-lg font-semibold text-gray-900 dark:text-white\">\n                <Link href={`/blog/${post.slug}`}>{post.title}</Link>\n              </h3>\n              <p className=\"mt-2 text-sm text-gray-600 dark:text-gray-400\">{post.summary}</p>\n            </article>\n          ))}\n        </div>\n      </section>","why":"6.10-6.11'de hazırladığımız recentPosts verisini ve daha önce import ettiğimiz Link component'ini kullanarak blog kartlarını render ediyoruz."},
    {"order":"6.13","action":"Ana sayfada son yazıların göründüğünü doğrula ve commit yap","type":"validate","validation":"Ana sayfada Hero section'dan sonra 'Son Yazılar' bölümü görünmeli. Blog kartları tıklanabilir olmalı.","why":"6.1-6.12'de yaptığımız tüm çalışmayı doğruluyoruz. Milestone 2 tamamlandı."}
]

data['milestones'][m2_idx]['steps'][5]['substeps'] = m2_s6

# ============================================================================
# M3 S2: Mobile Nav - enrich to 13 substeps
# ============================================================================
m3_idx = find_milestone('p01-m3')

m3_s2 = [
    {"order":"2.1","action":"MobileNav component dosyasını oluştur — önce 'use client'","type":"code_write","file":"src/components/mobile-nav.tsx","code":"'use client';","why":"Mobil menü toggle state'i (useState) kullanacak — Client Component zorunlu."},
    {"order":"2.2","action":"State yönetimi için useState lazım — import et","type":"code_add","file":"src/components/mobile-nav.tsx","position":"bottom","code":"\nimport { useState } from 'react';","why":"Menü açık/kapalı durumunu yönetmek için useState gerekli."},
    {"order":"2.3","action":"Link ve usePathname da lazım — import et","type":"code_add","file":"src/components/mobile-nav.tsx","position":"after_useState","code":"import Link from 'next/link';\nimport { usePathname } from 'next/navigation';","why":"Link navigasyon için, usePathname aktif sayfa vurgulama için gerekli. M1'deki Header'da da aynı pattern'ı kullanmıştık."},
    {"order":"2.4","action":"Navigasyon dizisini tanımla — import'ların ALTINA","type":"code_add","file":"src/components/mobile-nav.tsx","position":"after_imports","code":"\nconst navigation = [\n  { name: 'Ana Sayfa', href: '/' },\n  { name: 'Hakkımda', href: '/about' },\n  { name: 'Projeler', href: '/projects' },\n  { name: 'Blog', href: '/blog' },\n  { name: 'İletişim', href: '/contact' },\n];","why":"DRY prensibine uygun — aynı veri yapısı Header'da da var. İleride ortak bir dosyaya taşınabilir."},
    {"order":"2.5","action":"MobileNav iskeletini yaz — md:hidden ile sadece mobilde görünecek","type":"code_add","file":"src/components/mobile-nav.tsx","position":"bottom","code":"\nexport function MobileNav() {\n  const [isOpen, setIsOpen] = useState(false);\n  const pathname = usePathname();\n\n  return (\n    <div className=\"md:hidden\">\n    </div>\n  );\n}","why":"md:hidden ile bu component sadece 768px altında görünür. 2.2'deki useState ile menü durumunu, 2.3'teki usePathname ile aktif sayfayı yönetiyoruz."},
    {"order":"2.6","action":"Hamburger butonunu div içine ekle","type":"code_add","file":"src/components/mobile-nav.tsx","position":"inside_div","code":"      <button onClick={() => setIsOpen(!isOpen)} className=\"rounded-lg p-2 hover:bg-gray-100 dark:hover:bg-gray-800\" aria-label=\"Menüyü aç\" aria-expanded={isOpen}>\n        <svg className=\"h-6 w-6\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\">\n          {isOpen ? (\n            <path strokeLinecap=\"round\" strokeLinejoin=\"round\" strokeWidth={2} d=\"M6 18L18 6M6 6l12 12\" />\n          ) : (\n            <path strokeLinecap=\"round\" strokeLinejoin=\"round\" strokeWidth={2} d=\"M4 6h16M4 12h16M4 18h16\" />\n          )}\n        </svg>\n      </button>","why":"aria-label screen reader'lara butonun amacını söyler. aria-expanded={isOpen} menünün açık mı kapalı mı olduğunu bildirir — WCAG zorunluluğu. 2.5'teki isOpen state'ine göre ikon değişir."},
    {"order":"2.7","action":"Menü dropdown panelini ekle — butonun ALTINA","type":"code_add","file":"src/components/mobile-nav.tsx","position":"after_button","code":"\n      {isOpen && (\n        <div className=\"absolute left-0 right-0 top-full border-b border-gray-200 bg-white p-4 shadow-lg dark:border-gray-800 dark:bg-dark-bg\">\n          <nav className=\"flex flex-col space-y-3\">\n            {navigation.map((item) => (\n              <Link key={item.href} href={item.href} onClick={() => setIsOpen(false)}\n                className={`rounded-lg px-4 py-2 text-sm transition-colors ${\n                  pathname === item.href\n                    ? 'bg-primary-50 font-semibold text-primary-600 dark:bg-primary-900/30 dark:text-primary-400'\n                    : 'text-gray-600 hover:bg-gray-50 dark:text-gray-400 dark:hover:bg-gray-800'\n                }`}>{item.name}</Link>\n            ))}\n          </nav>\n        </div>\n      )}","why":"2.4'teki navigation dizisini map ile dönerek linkleri render ediyoruz. onClick={() => setIsOpen(false)} linke tıklanınca menüyü kapatır. 2.3'teki pathname ile aktif sayfa vurgulanır."},
    {"order":"2.8","action":"header.tsx'e GERİ DÖN — MobileNav import'unu ekle (ÜSTE)","type":"code_add","file":"src/components/header.tsx","position":"top","code":"import { MobileNav } from './mobile-nav';","why":"2.1-2.7'de oluşturduğumuz MobileNav'ı Header'a import ediyoruz."},
    {"order":"2.9","action":"Desktop linklerini mobilde gizle — hidden md:flex ekle","type":"code_modify","file":"src/components/header.tsx","code":"<div className=\"hidden md:flex items-center gap-6\">","why":"hidden md:flex ile desktop linkler 768px altında gizlenir. MobileNav zaten md:hidden olduğundan ikisi birbirini tamamlar."},
    {"order":"2.10","action":"MobileNav'ı nav içine ekle","type":"code_add","file":"src/components/header.tsx","position":"inside_nav","code":"<MobileNav />","why":"2.8'de import ettiğimiz MobileNav'ı Header JSX'ine ekliyoruz. Desktop ve mobil nav hiçbir zaman aynı anda görünmez."},
    {"order":"2.11","action":"Mobil görünümü test et","type":"validate","validation":"1) DevTools responsive mode (Ctrl+Shift+M). 2) 768px altında hamburger ikonu görünmeli. 3) Hamburger'a tıklayınca menü açılmalı. 4) Link'e tıklayınca menü kapanmalı. 5) 768px üstünde desktop linkler görünmeli.","why":"2.1-2.10'da yaptığımız tüm çalışmayı beş farklı senaryoda test ediyoruz."},
    {"order":"2.12","action":"Commit yap","type":"terminal","command":"git add -A && git commit -m \"feat: add mobile responsive hamburger navigation\"","expected_output":"[main ...] feat: add mobile responsive...","why":"Mobil navigasyon tamamlandı."}
]

data['milestones'][m3_idx]['steps'][1]['substeps'] = m3_s2

# M3 S3: Skills/Timeline - enrich to 13
m3_s3 = [
    {"order":"3.1","action":"SkillsSection component dosyasını oluştur","type":"file_open","file":"src/components/skills-section.tsx","why":"Becerileri ayrı component yaparak farklı sayfalarda da kullanılabilir hale getiriyoruz."},
    {"order":"3.2","action":"Önce veri yapısını tanımla — beceri kategorileri","type":"code_write","file":"src/components/skills-section.tsx","code":"const skillCategories = [\n  { title: 'Frontend', skills: ['React', 'Next.js', 'TypeScript', 'Tailwind CSS', 'HTML5/CSS3'] },\n  { title: 'Backend', skills: ['Node.js', 'Express', 'PostgreSQL', 'MongoDB', 'Redis'] },\n  { title: 'DevOps & Araçlar', skills: ['Docker', 'Git', 'GitHub Actions', 'Vercel', 'Linux'] },\n  { title: 'AI & ML', skills: ['Python', 'OpenAI API', 'LangChain', 'Scikit-learn'] },\n];","why":"Senior developer önce veriyi tanımlar, sonra görsel katmanı yazar. Veriyi component dışında tutmak, ileride API'den çekmeye geçişi kolaylaştırır."},
    {"order":"3.3","action":"SkillsSection fonksiyon iskeletini yaz — boş section","type":"code_add","file":"src/components/skills-section.tsx","position":"bottom","code":"\nexport function SkillsSection() {\n  return (\n    <section className=\"py-12\">\n      <h2 className=\"mb-8 text-2xl font-bold text-gray-900 dark:text-white\">Teknik Beceriler</h2>\n    </section>\n  );\n}","why":"Önce boş iskelet. Semantic HTML kullanarak section ve h2 ile bölümü tanımlıyoruz."},
    {"order":"3.4","action":"h2'den sonra grid ve kategori kartlarını ekle — 3.2'deki veriyi kullan","type":"code_add","file":"src/components/skills-section.tsx","position":"after_h2","code":"      <div className=\"grid gap-6 sm:grid-cols-2\">\n        {skillCategories.map((category) => (\n          <div key={category.title} className=\"rounded-xl border border-gray-200 p-6 dark:border-gray-800\">\n            <h3 className=\"mb-4 font-semibold text-gray-900 dark:text-white\">{category.title}</h3>\n            <div className=\"flex flex-wrap gap-2\">\n              {category.skills.map((skill) => (\n                <span key={skill} className=\"rounded-full bg-primary-50 px-3 py-1 text-sm text-primary-700 dark:bg-primary-900/30 dark:text-primary-300\">{skill}</span>\n              ))}\n            </div>\n          </div>\n        ))}\n      </div>","why":"3.2'de tanımladığımız skillCategories dizisini map ile dönerek kartları oluşturuyoruz. sm:grid-cols-2 ile mobile-first responsive grid."},
    {"order":"3.5","action":"BAŞKA DOSYAYA geç — Timeline component'ini oluştur","type":"file_open","file":"src/components/timeline.tsx","why":"Deneyim timeline'ı farklı bir veri yapısı ve farklı görsel sunum içerir — ayrı component olmalı."},
    {"order":"3.6","action":"Deneyim verisi dizisini tanımla","type":"code_write","file":"src/components/timeline.tsx","code":"const experiences = [\n  {\n    period: '2024 - Devam',\n    title: 'Full Stack Developer',\n    company: 'Freelance / Kişisel Projeler',\n    description: 'React, Next.js, Node.js ile modern web uygulamaları geliştirme.',\n  },\n];","why":"Veriyi önce tanımlıyoruz — component yapısından bağımsız. Yeni deneyim eklemek için sadece diziye push yeterli."},
    {"order":"3.7","action":"Timeline fonksiyon iskeletini yaz","type":"code_add","file":"src/components/timeline.tsx","position":"bottom","code":"\nexport function Timeline() {\n  return (\n    <section className=\"py-12\">\n      <h2 className=\"mb-8 text-2xl font-bold text-gray-900 dark:text-white\">Deneyim</h2>\n    </section>\n  );\n}","why":"Boş iskelet. 3.3'teki SkillsSection ile aynı stil kurallarını kullanarak tutarlılık sağlıyoruz."},
    {"order":"3.8","action":"Timeline çizgisi ve kartları ekle — 3.6'daki veriyi kullan","type":"code_add","file":"src/components/timeline.tsx","position":"after_h2","code":"      <div className=\"space-y-8\">\n        {experiences.map((exp, i) => (\n          <div key={i} className=\"relative border-l-2 border-primary-200 pl-6 dark:border-primary-800\">\n            <div className=\"absolute -left-[9px] top-0 h-4 w-4 rounded-full border-2 border-primary-500 bg-white dark:bg-dark-bg\" />\n            <p className=\"text-sm text-gray-500 dark:text-gray-400\">{exp.period}</p>\n            <h3 className=\"mt-1 font-semibold text-gray-900 dark:text-white\">{exp.title}</h3>\n            <p className=\"text-sm text-primary-600 dark:text-primary-400\">{exp.company}</p>\n            <p className=\"mt-2 text-gray-600 dark:text-gray-400\">{exp.description}</p>\n          </div>\n        ))}\n      </div>","why":"3.6'daki experiences dizisini render ediyoruz. border-l-2 ile sol çizgi, absolute ile daire konumlandırması — CSS-only timeline, library dependency yok."},
    {"order":"3.9","action":"about/page.tsx'e GERİ DÖN — SkillsSection import'unu ekle (ÜSTE)","type":"code_add","file":"src/app/about/page.tsx","position":"top","code":"import { SkillsSection } from '@/components/skills-section';","why":"3.1-3.4'te oluşturduğumuz SkillsSection'ı Hakkımda sayfasına import ediyoruz."},
    {"order":"3.10","action":"Timeline import'unu da ekle","type":"code_add","file":"src/app/about/page.tsx","position":"after_skills_import","code":"import { Timeline } from '@/components/timeline';","why":"3.5-3.8'de oluşturduğumuz Timeline'ı da import ediyoruz."},
    {"order":"3.11","action":"About sayfasının JSX'ine her iki component'i ekle","type":"code_add","file":"src/app/about/page.tsx","position":"after_prose","code":"      <SkillsSection />\n      <Timeline />","why":"3.9-3.10'da import ettiğimiz component'leri sayfaya ekliyoruz. Recruiter'lar önce 'ne biliyor' (Skills) sonra 'nerede çalışmış' (Timeline) diye bakar."},
    {"order":"3.12","action":"Responsive ve dark mode kontrolü yap","type":"validate","validation":"1) /about sayfasında beceriler kartlarda görünmeli. 2) Mobilde tek sütun, tablette iki sütun. 3) Timeline'da çizgi ve daireler doğru konumda. 4) Dark mode'da okunabilir.","why":"3.1-3.11'de yaptığımız tüm çalışmayı farklı ekran boyutlarında ve temalarda doğruluyoruz."},
    {"order":"3.13","action":"Commit yap","type":"terminal","command":"git add -A && git commit -m \"feat: add Skills section and Experience timeline to About page\"","expected_output":"[main ...] feat: add Skills section...","why":"İki yeni component tamamlandı."}
]

data['milestones'][m3_idx]['steps'][2]['substeps'] = m3_s3

# M3 S4: Animations - enrich to 12
m3_s4 = [
    {"order":"4.1","action":"globals.css dosyasını aç","type":"file_open","file":"src/app/globals.css","why":"Animasyon tanımlarını global CSS dosyasına ekliyoruz çünkü tüm sayfalarda kullanılacak utility class'lar olacak."},
    {"order":"4.2","action":"@layer utilities bloğunu başlat ve animate-fade-in class'ını tanımla","type":"code_add","file":"src/app/globals.css","position":"bottom","code":"\n@layer utilities {\n  .animate-fade-in {\n    animation: fadeIn 0.5s ease-out;\n  }\n}","why":"@layer utilities, Tailwind'in utility katmanına custom class ekler. Bu katmandaki class'lar purge mekanizmasında korunur."},
    {"order":"4.3","action":"Hmm, slide-up animasyonu da lazım — @layer içine ekle","type":"code_add","file":"src/app/globals.css","position":"inside_layer_utilities","code":"\n  .animate-slide-up {\n    animation: slideUp 0.5s ease-out;\n  }","why":"4.2'de başlattığımız @layer bloğuna ikinci animasyonu ekliyoruz. Kartlar için dikey hareket efekti — görsel hiyerarşi oluşturur."},
    {"order":"4.4","action":"fadeIn keyframe'ini tanımla — @layer bloğunun DIŞINA","type":"code_add","file":"src/app/globals.css","position":"after_layer_utilities","code":"\n@keyframes fadeIn {\n  from { opacity: 0; }\n  to { opacity: 1; }\n}","why":"4.2'deki animate-fade-in class'ının referans ettiği keyframe. opacity GPU-accelerated — layout thrashing yapmaz."},
    {"order":"4.5","action":"slideUp keyframe'ini de tanımla","type":"code_add","file":"src/app/globals.css","position":"after_fadeIn","code":"\n@keyframes slideUp {\n  from { opacity: 0; transform: translateY(20px); }\n  to { opacity: 1; transform: translateY(0); }\n}","why":"4.3'teki animate-slide-up class'ının keyframe'i. transform da GPU-accelerated — performans dostu."},
    {"order":"4.6","action":"Erişilebilirlik için prefers-reduced-motion ekle","type":"code_add","file":"src/app/globals.css","position":"after_keyframes","code":"\n@media (prefers-reduced-motion: reduce) {\n  .animate-fade-in,\n  .animate-slide-up {\n    animation: none;\n  }\n}","why":"WCAG 2.3.3 zorunluluğu: vestibüler bozuklukları olan kullanıcılar için animasyonlar rahatsızlık yaratabilir. 4.2 ve 4.3'te tanımladığımız animasyonları devre dışı bırakıyoruz."},
    {"order":"4.7","action":"Focus-visible stilini de ekle — klavye navigasyonu için","type":"code_add","file":"src/app/globals.css","position":"bottom","code":"\n*:focus-visible {\n  outline: 2px solid var(--color-primary-500);\n  outline-offset: 2px;\n}","why":"focus-visible sadece klavye ile odaklanıldığında outline gösterir. Mouse tıklamasında gereksiz outline olmaz — hem UX hem erişilebilirlik."},
    {"order":"4.8","action":"page.tsx'e GERİ DÖN — Hero section'a animate-fade-in ekle","type":"code_modify","file":"src/app/page.tsx","code":"<section className=\"mx-auto max-w-5xl px-4 py-20 animate-fade-in\">","why":"4.2'de tanımladığımız animate-fade-in class'ını Hero section'a ekliyoruz. Sayfaya giriş hissini yumuşatır."},
    {"order":"4.9","action":"Blog kartları grid'ine animate-slide-up ekle","type":"code_modify","file":"src/app/page.tsx","code":"<div className=\"grid gap-6 md:grid-cols-3 animate-slide-up\">","why":"4.3'teki animate-slide-up'ı kartlara ekliyoruz. Kullanıcının dikkatini doğal olarak aşağıya yönlendirir."},
    {"order":"4.10","action":"Animasyonları ve erişilebilirliği test et","type":"validate","validation":"1) Sayfa açıldığında yumuşak fade-in görünmeli. 2) Kartlar slide-up ile belirmeli. 3) Windows > Erişilebilirlik > Animasyon efektleri'ni kapat — animasyonlar devre dışı kalmalı. 4) Tab ile gezinirken focus göstergesi görünmeli.","why":"4.2-4.9'da yaptığımız tüm çalışmayı hem görsel hem erişilebilirlik açısından doğruluyoruz."},
    {"order":"4.11","action":"Commit yap","type":"terminal","command":"git add -A && git commit -m \"feat: add page animations with accessibility support\"","expected_output":"[main ...] feat: add page animations...","why":"Animasyon sistemi tamamlandı — erişilebilirlik dahil."}
]

data['milestones'][m3_idx]['steps'][3]['substeps'] = m3_s4

# ============================================================================
# M4: SEO, Performance, Accessibility - enrich each step to 12+
# ============================================================================
m4_idx = find_milestone('p01-m4')

# M4 S1: SEO Meta Tags - enrich to 12
m4_s1 = [
    {"order":"1.1","action":"src/app/layout.tsx dosyasını aç","type":"file_open","file":"src/app/layout.tsx","why":"Root layout'taki metadata export'u tüm sayfalar için varsayılan SEO bilgilerini belirler."},
    {"order":"1.2","action":"Metadata objesini bul ve metadataBase ekle","type":"code_modify","file":"src/app/layout.tsx","code":"export const metadata: Metadata = {\n  metadataBase: new URL('https://your-domain.com'),","why":"metadataBase, tüm relative URL'leri absolute URL'e çevirir — bu olmadan sosyal medya kartlarında görsel görünmez."},
    {"order":"1.3","action":"description ve keywords alanlarını zenginleştir","type":"code_modify","file":"src/app/layout.tsx","code":"  description: 'Full Stack Developer. React, Next.js, Node.js ve AI teknolojileriyle modern web uygulamaları geliştiriyorum.',\n  keywords: ['Full Stack Developer', 'React Developer', 'Next.js', 'TypeScript', 'Node.js', 'Portfolio'],\n  authors: [{ name: 'Adın Soyadın' }],\n  creator: 'Adın Soyadın',","why":"description Google arama sonuçlarında görünür — 155 karakter sınırı. keywords modern SEO'da eskisi kadar etkili olmasa da bazı motorlar referans olarak kullanır."},
    {"order":"1.4","action":"Open Graph meta tag'lerini ekle","type":"code_add","file":"src/app/layout.tsx","position":"inside_metadata","code":"  openGraph: {\n    type: 'website',\n    locale: 'tr_TR',\n    url: 'https://your-domain.com',\n    siteName: 'Adın Soyadın',\n    title: 'Adın Soyadın | Full Stack Developer',\n    description: 'Full Stack Developer portfolio ve teknik blog.',\n    images: [{ url: '/og-image.png', width: 1200, height: 630, alt: 'Adın Soyadın Portfolio' }],\n  },","why":"LinkedIn veya Facebook'ta paylaşıldığında büyük görsel kartı oluşturur. 1200x630px tüm platformlarda optimal çalışan standart."},
    {"order":"1.5","action":"Twitter Card meta tag'lerini ekle","type":"code_add","file":"src/app/layout.tsx","position":"after_openGraph","code":"  twitter: {\n    card: 'summary_large_image',\n    title: 'Adın Soyadın | Full Stack Developer',\n    description: 'Full Stack Developer portfolio ve teknik blog.',\n    images: ['/og-image.png'],\n  },","why":"Twitter (X) kendi meta tag formatını kullanır. summary_large_image büyük görsel kartı ile CTR artırır. 1.4'teki og-image.png'yi yeniden kullanıyoruz."},
    {"order":"1.6","action":"robots konfigürasyonunu ekle","type":"code_add","file":"src/app/layout.tsx","position":"after_twitter","code":"  robots: {\n    index: true,\n    follow: true,\n    googleBot: {\n      index: true,\n      follow: true,\n      'max-video-preview': -1,\n      'max-image-preview': 'large',\n      'max-snippet': -1,\n    },\n  },","why":"Google bot'una sayfayı indexlemesi ve linkleri takip etmesi gerektiğini söylüyoruz. max-image-preview: 'large' arama sonuçlarında büyük görsel önizleme gösterilmesine izin verir."},
    {"order":"1.7","action":"public/ klasörüne OG image görseli hakkında not","type":"explain","why":"1200x630px boyutunda bir görsel oluşturup public/og-image.png olarak kaydet. Figma, Canva veya başka bir araçla oluşturulabilir."},
    {"order":"1.8","action":"OG image dosyasının varlığını kontrol et","type":"terminal","command":"ls public/og-image.png 2>/dev/null && echo 'Mevcut' || echo 'YOK - oluşturulmalı'","expected_output":"Dosyanın durumu gösterildi","why":"1.4'te referans verdiğimiz og-image.png'nin var olduğunu doğruluyoruz. Yoksa sosyal medya kartları boş görünür."},
    {"order":"1.9","action":"Meta tag'lerin doğru render edildiğini doğrula","type":"validate","validation":"1) DevTools > Elements > head içinde og:title, og:description, og:image görünmeli. 2) Her sayfada title template çalışmalı. 3) View Page Source ile server-side render doğrulanmalı.","why":"SEO meta tag'leri server-side render edilmeli — arama motorları JavaScript çalıştırmadan HTML'i okur."},
    {"order":"1.10","action":"Commit yap","type":"terminal","command":"git add -A && git commit -m \"feat: add comprehensive SEO metadata with Open Graph and Twitter Cards\"","expected_output":"[main ...] feat: add comprehensive SEO...","why":"SEO altyapısı tamamlandı."}
]

data['milestones'][m4_idx]['steps'][0]['substeps'] = m4_s1

# M4 S2: Sitemap - enrich to 12
m4_s2 = [
    {"order":"2.1","action":"src/app/sitemap.ts dosyasını oluştur","type":"file_open","file":"src/app/sitemap.ts","why":"Next.js, sitemap.ts dosyasını convention olarak tanır ve /sitemap.xml endpoint'ine dönüştürür."},
    {"order":"2.2","action":"Önce fonksiyon iskeletini yaz — boş dizi dönecek","type":"code_write","file":"src/app/sitemap.ts","code":"export default async function sitemap() {\n  return [];\n}","why":"Senior developer önce çalışan iskelet yazar. /sitemap.xml'e gittiğinde boş XML görürsün — hata yok."},
    {"order":"2.3","action":"MetadataRoute tipine ihtiyacımız var — ÜSTE çık, import et","type":"code_add","file":"src/app/sitemap.ts","position":"top","code":"import { MetadataRoute } from 'next';","why":"TypeScript tip güvenliği için. Yanlış alan adı IDE'de anında uyarı verir."},
    {"order":"2.4","action":"Blog yazılarını da eklemek için getAllPosts lazım — import et","type":"code_add","file":"src/app/sitemap.ts","position":"after_metadata_import","code":"import { getAllPosts } from '@/lib/mdx';","why":"M2 Step 2'de yazdığımız getAllPosts ile blog yazılarını dinamik olarak sitemap'e ekleyeceğiz."},
    {"order":"2.5","action":"Fonksiyonun return tipini belirle ve blog yazılarını ekle — geri DÖN","type":"code_modify","file":"src/app/sitemap.ts","code":"export default async function sitemap(): Promise<MetadataRoute.Sitemap> {\n  const posts = await getAllPosts();\n  const baseUrl = 'https://your-domain.com';\n\n  const blogPosts = posts.map((post) => ({\n    url: `${baseUrl}/blog/${post.slug}`,\n    lastModified: new Date(post.date),\n    changeFrequency: 'monthly' as const,\n    priority: 0.7,\n  }));\n\n  const staticPages = [\n    { url: baseUrl, lastModified: new Date(), changeFrequency: 'weekly' as const, priority: 1.0 },\n    { url: `${baseUrl}/about`, lastModified: new Date(), changeFrequency: 'monthly' as const, priority: 0.8 },\n    { url: `${baseUrl}/projects`, lastModified: new Date(), changeFrequency: 'weekly' as const, priority: 0.8 },\n    { url: `${baseUrl}/blog`, lastModified: new Date(), changeFrequency: 'weekly' as const, priority: 0.9 },\n    { url: `${baseUrl}/contact`, lastModified: new Date(), changeFrequency: 'yearly' as const, priority: 0.5 },\n  ];\n\n  return [...staticPages, ...blogPosts];\n}","why":"2.3'teki MetadataRoute.Sitemap tipini, 2.4'teki getAllPosts'u kullanarak tam fonksiyonu yazıyoruz. Ana sayfa priority 1.0, iletişim 0.5."},
    {"order":"2.6","action":"BAŞKA DOSYAYA geç — robots.ts oluştur","type":"file_open","file":"src/app/robots.ts","why":"robots.txt, arama motorlarına hangi bölümleri tarayacağını söyler. Next.js convention'ı ile otomatik /robots.txt endpoint'i oluşur."},
    {"order":"2.7","action":"MetadataRoute import'unu yaz","type":"code_write","file":"src/app/robots.ts","code":"import { MetadataRoute } from 'next';","why":"Tip güvenliği için — 2.3'te sitemap için de aynı modülden import ettik."},
    {"order":"2.8","action":"Robots fonksiyonunu yaz","type":"code_add","file":"src/app/robots.ts","position":"bottom","code":"\nexport default function robots(): MetadataRoute.Robots {\n  return {\n    rules: { userAgent: '*', allow: '/', disallow: '/api/' },\n    sitemap: 'https://your-domain.com/sitemap.xml',\n  };\n}","why":"2.7'deki MetadataRoute.Robots tipini kullanıyoruz. userAgent: '*' tüm botları kapsar. /api/ indexlenmesini engelliyoruz."},
    {"order":"2.9","action":"Sitemap.xml ve robots.txt çıktılarını doğrula","type":"validate","validation":"/sitemap.xml adresinde tüm URL'ler XML formatında görünmeli. /robots.txt adresinde 'User-agent: *' ve 'Sitemap:' satırları olmalı.","why":"2.1-2.8'de yaptığımız tüm çalışmayı doğruluyoruz. Hatalı XML formatı Google'ın sitemap'i reddetmesine neden olur."},
    {"order":"2.10","action":"Commit yap","type":"terminal","command":"git add -A && git commit -m \"feat: add automated sitemap.xml and robots.txt generation\"","expected_output":"[main ...] feat: add automated sitemap...","why":"SEO altyapısı tamamlandı — sitemap ve robots."}
]

data['milestones'][m4_idx]['steps'][1]['substeps'] = m4_s2

# M4 S3 (Image), S4 (A11y), S5 (Lighthouse) - keep existing, they're already 10 each

# M5 S1 and S2 - enrich to 10+
m5_idx = find_milestone('p01-m5')

# Add one more substep to M5 S1 (GitHub) to reach 10
existing_m5_s1 = data['milestones'][m5_idx]['steps'][0]['substeps']
existing_m5_s1.append({
    "order": "1.10",
    "action": "GitHub repository topics ekle",
    "type": "explain",
    "why": "GitHub repo > Settings'ten topics ekle: nextjs, typescript, tailwindcss, portfolio, blog. Topics, GitHub arama sonuçlarında repo'nun bulunmasını sağlar ve projenin teknoloji stack'ini bir bakışta gösterir."
})

# Add substep to M5 S2 (Vercel deploy) to reach 10
existing_m5_s2 = data['milestones'][m5_idx]['steps'][1]['substeps']
existing_m5_s2.append({
    "order": "2.10",
    "action": "Custom domain hakkında not al",
    "type": "explain",
    "why": "Vercel Settings > Domains'den custom domain ekleyebilirsin. DNS A record: 76.76.21.21. Custom domain CV'de çok daha profesyonel görünür — portfolio-site.vercel.app yerine adiniz.dev gibi."
})

# Deployment milestone - enrich Production Build to 10
dep_idx = len(data['milestones']) - 1  # Last milestone

dep_s1 = data['milestones'][dep_idx]['steps'][0]['substeps']
dep_s1.append({
    "order": "1.9",
    "action": "Bundle size analizi yap",
    "type": "terminal",
    "command": "du -sh .next/static/chunks/*.js | sort -rh | head -5",
    "expected_output": "En büyük 5 chunk dosyasının boyutları",
    "why": "Büyük chunk dosyaları sayfa yükleme süresini artırır. 100KB üzeri dosyalar optimize edilmeli — dynamic import veya code splitting ile."
})
dep_s1.append({
    "order": "1.10",
    "action": "Commit yap — production build hazır",
    "type": "terminal",
    "command": "git add -A && git commit -m \"chore: verify production build and Lighthouse scores\"",
    "expected_output": "[main ...] chore: verify production build...",
    "why": "Production build doğrulaması tamamlandı."
})

# Deploy step - add commit
dep_s2 = data['milestones'][dep_idx]['steps'][1]['substeps']
dep_s2.append({
    "order": "2.10",
    "action": "Sitemap'i Google Search Console'a submit etmeyi not al",
    "type": "explain",
    "why": "Deploy sonrası Google Search Console'da 'Sitemap' bölümünden https://your-domain.com/sitemap.xml URL'sini submit et. Bu, Google'ın siteyi hızlıca indexlemesini sağlar."
})

# README step - add one more
dep_s3 = data['milestones'][dep_idx]['steps'][2]['substeps']
dep_s3.append({
    "order": "3.10",
    "action": "Final doğrulama — GitHub profil sayfanı kontrol et",
    "type": "validate",
    "validation": "GitHub profil sayfanda pinned repositories'e bu projeyi ekle. Profile README'de bu projeye link ver. Recruiter'lar GitHub profilini CV'den sonra ilk kontrol ettikleri yerdir.",
    "why": "GitHub profili dijital CV'nin parçasıdır. Pinned repo'lar ilk izlenimi oluşturur."
})

# Demo Video - add 2 more substeps
dep_s4 = data['milestones'][dep_idx]['steps'][3]['substeps']
dep_s4.append({
    "order": "4.9",
    "action": "Video'nun README'ye düzgün embed edildiğini kontrol et",
    "type": "validate",
    "validation": "GitHub repo sayfasında video linki tıklanabilir olmalı. Thumbnail görünüyorsa bonus.",
    "why": "Video linki çalışmazsa hiç eklememek daha iyi — kırık link negatif izlenim bırakır."
})
dep_s4.append({
    "order": "4.10",
    "action": "PROJE TAMAMLANDI — final commit ve push",
    "type": "terminal",
    "command": "git add -A && git commit -m \"docs: add demo video link to README\" && git push origin main",
    "expected_output": "[main ...] docs: add demo video...",
    "why": "Tüm proje tamamlandı. Son push ile Vercel otomatik deploy tetiklenir ve canlı site güncellenir."
})

# Save
with open('content/projects/project-01.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Count
import sys
sys.stdout.reconfigure(encoding='utf-8')
total = 0
for m in data['milestones']:
    for s in m.get('steps', []):
        n = len(s.get('substeps', []))
        total += n
        step_id = s.get('step', s.get('title', '?'))
        print(f'{m.get("id", "?")} step {step_id}: {n} substeps')
print(f'\nNEW TOTAL: {total}')
