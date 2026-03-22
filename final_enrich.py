#!/usr/bin/env python3
"""Final enrichment pass to reach 400+ substeps."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('content/projects/project-01.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def find_milestone(mid):
    for i, m in enumerate(data['milestones']):
        if m.get('id') == mid:
            return i
    return None

# ============================================================================
# ENRICHMENTS: Add 3-5 substeps to each step that needs it
# Target: ~400 total from current 308 = need ~92 more substeps
# ============================================================================

# M2 S1 (Hero) - add 4 more substeps (9 -> 13)
m2_idx = find_milestone('p01-m2')
m2_s1 = data['milestones'][m2_idx]['steps'][0]['substeps']
# Insert at various positions
m2_s1.insert(3, {
    "order":"1.3b","action":"HomePage'i async yaparak Server Component avantajını hazırla","type":"code_modify","file":"src/app/page.tsx","code":"export default async function HomePage() {","why":"async anahtar kelimesini ekliyoruz çünkü ileride (M2 Step 6) getRecentPosts çağıracağız. Server Component olduğu için async/await doğrudan kullanılabilir — bu React hook'larından farklıdır."
})
m2_s1.insert(7, {
    "order":"1.6b","action":"CTA butonlarının hover efektini test et","type":"validate","validation":"İki CTA butonuna mouse ile hover et. Birincil butonun rengi koyulaşmalı (bg-primary-700), ikincil butonun arka planı hafifçe grileşmeli. Geçiş yumuşak olmalı (transition-colors).","why":"1.5'te eklediğimiz transition-colors class'ının çalıştığını doğruluyoruz. Hover efekti olmayan butonlar tıklanabilir görünmez."
})
m2_s1.insert(9, {
    "order":"1.8b","action":"Semantic HTML kontrolü yap","type":"validate","validation":"DevTools > Elements'te sayfa yapısını kontrol et: main > section > div > h1, h2, p hiyerarşisi doğru olmalı. h1 sadece bir tane olmalı.","why":"Screen reader'lar heading hiyerarşisine göre sayfa yapısını anlar. h1 atlamak veya birden fazla h1 kullanmak erişilebilirlik ve SEO sorunlarına yol açar."
})
m2_s1.append({
    "order":"1.10","action":"Hero section'ı farklı içeriklerle doldur — kendi bilgilerini yaz","type":"explain","why":"Placeholder 'Adın Soyadın' ve açıklama metinlerini kendi bilgilerinle değiştir. Gerçek bilgilerle doldurmak, portfolio'nun sahici ve profesyonel görünmesini sağlar."
})

# M2 S5 (Contact) - add 3 more (9 -> 12)
m2_s5 = data['milestones'][m2_idx]['steps'][4]['substeps']
m2_s5.insert(6, {
    "order":"5.6b","action":"Loading state'ini test et — buton 'Gönderiliyor...' göstermeli","type":"validate","validation":"Formu doldurup gönder butonuna tıkla. Buton metni geçici olarak 'Gönderiliyor...' olmalı ve disabled görünmeli (opacity azalmış). Bu, çift tıklamayı önler.","why":"5.5'te tanımladığımız status state'inin 'loading' değerinin doğru çalıştığını doğruluyoruz."
})
m2_s5.insert(7, {
    "order":"5.7b","action":"Form validation'ı test et — boş form gönderilemememeli","type":"validate","validation":"Hiçbir alan doldurmadan 'Gönder' butonuna tıkla. Tarayıcı 'Bu alan zorunludur' gibi bir uyarı göstermeli. required attribute'u çalışıyor olmalı.","why":"5.7'de eklediğimiz required attribute'ünün browser-native validation'ı tetiklediğini doğruluyoruz."
})
m2_s5.append({
    "order":"5.10","action":"Formspree hesabı oluştur ve gerçek form ID'yi ekle","type":"explain","why":"formspree.io'da ücretsiz hesap oluştur. Yeni form ekle ve verilen ID'yi YOUR_FORM_ID yerine yaz. Ücretsiz plan ayda 50 submission destekler. Test gönderimi yap ve e-postanı kontrol et."
})

# M4 S1 (SEO) - add 2 more (10 -> 12)
m4_idx = find_milestone('p01-m4')
m4_s1 = data['milestones'][m4_idx]['steps'][0]['substeps']
m4_s1.insert(7, {
    "order":"1.7b","action":"Blog detay sayfalarında da dinamik OG meta'yı kontrol et","type":"validate","validation":"/blog/nextjs-portfolio-rehberi sayfasında DevTools > Elements > head'de og:title'ın blog yazısının başlığı olduğunu doğrula. Her yazının kendi meta'sı olmalı.","why":"M2 Step 3'te yazdığımız generateMetadata'nın çalıştığını doğruluyoruz. Statik metadata yerine her yazıya özel dinamik metadata oluşturulmalı."
})
m4_s1.append({
    "order":"1.11","action":"JSON-LD structured data eklemeyi düşün (opsiyonel gelişmiş SEO)","type":"explain","why":"JSON-LD, arama motorlarına sayfanın içeriğini yapılandırılmış formatta bildirir. Google'ın zengin snippet'ler (yıldız, tarih, yazar) göstermesini sağlar. Bu adım opsiyonel ama SEO'yu bir üst seviyeye taşır."
})

# M4 S2 (Sitemap) - add 2 more (10 -> 12)
m4_s2 = data['milestones'][m4_idx]['steps'][1]['substeps']
m4_s2.insert(5, {
    "order":"2.5b","action":"Sitemap'in dev server'da çalıştığını hızlıca kontrol et","type":"validate","validation":"http://localhost:3000/sitemap.xml adresini aç. XML formatında URL listesi görünmeli. Hata varsa import'ları kontrol et.","why":"2.5'te yazdığımız fonksiyonun doğru çalıştığını erken doğruluyoruz — hataları erken yakalamak önemli."
})
m4_s2.append({
    "order":"2.11","action":"Yeni blog yazısı eklendiğinde sitemap'in otomatik güncelleneceğini doğrula","type":"explain","why":"getAllPosts dinamik olarak dosyaları okuduğu için yeni .mdx dosyası eklediğinde sitemap otomatik güncellenir. Bu, file-based CMS yaklaşımının avantajıdır — ayrı bir sitemap güncelleme adımı gerekmez."
})

# M4 S3 (Image) - add 2 more (10 -> 12)
m4_s3 = data['milestones'][m4_idx]['steps'][2]['substeps']
m4_s3.insert(4, {
    "order":"3.4b","action":"priority prop'unun ne zaman kullanılacağını anla","type":"explain","why":"priority={true} SADECE above-the-fold (ilk ekran) görseller için kullanılır — preload hint ekler ve lazy loading'i devre dışı bırakır. Tüm görsellere priority vermek, hiçbirine vermemekle aynı etkiyi yapar — önceliklendirmenin anlamını kaybettirir."
})
m4_s3.append({
    "order":"3.11","action":"Commit yap — image optimizasyonu tamamlandı","type":"terminal","command":"git add -A && git commit -m \"feat: add image optimization with next/image wrapper component\"","expected_output":"[main ...] feat: add image optimization...","why":"Image optimizasyonu tamamlandı — WebP/AVIF format dönüşümü, lazy loading ve priority preload."
})

# M4 S4 (A11y) - add 2 more (10 -> 12)
m4_s4 = data['milestones'][m4_idx]['steps'][3]['substeps']
m4_s4.insert(5, {
    "order":"4.5b","action":"Screen reader ile test etmeyi düşün","type":"explain","why":"Windows'ta NVDA (ücretsiz), Mac'te VoiceOver (built-in) ile siteyi gezmeyi dene. Heading'ler arası gezinme (H tuşu), link listesi (K tuşu) ve landmark navigasyonu (D tuşu) çalışmalı. Bu deneyim, erişilebilirlik konusundaki anlayışını derinleştirir."
})
m4_s4.append({
    "order":"4.11","action":"Lighthouse Accessibility audit çalıştır ve skoru kontrol et","type":"validate","validation":"Chrome DevTools > Lighthouse > Accessibility kategorisinde 95+ skor hedefle. Her uyarıyı oku ve düzelt. Özellikle renk kontrastı, ARIA attribute'ları ve heading hiyerarşisi kontrol edilmeli.","why":"4.1-4.10'da yaptığımız tüm erişilebilirlik çalışmasının Lighthouse tarafından doğrulanması gerekiyor."
})

# M4 S5 (Lighthouse) - add 2 more (10 -> 12)
m4_s5 = data['milestones'][m4_idx]['steps'][4]['substeps']
m4_s5.insert(5, {
    "order":"5.5b","action":"images.formats ayarını kontrol et","type":"validate","validation":"next.config.mjs'te images: { formats: ['image/avif', 'image/webp'] } tanımlı olmalı. M4 Step 3'te eklediğimiz bu ayar AVIF desteğini aktifleştirir.","why":"M4 Step 3'te yapılandırdığımız image format desteğinin hâlâ doğru olduğunu doğruluyoruz."
})
m4_s5.append({
    "order":"5.11","action":"Tüm skorları not al ve Milestone 4'ü commit'le","type":"terminal","command":"git add -A && git commit -m \"feat: achieve Lighthouse 95+ scores with security headers and performance optimizations\"","expected_output":"[main ...] feat: achieve Lighthouse 95+...","why":"Milestone 4 tamamlandı — SEO, performans ve erişilebilirlik production seviyesinde."
})

# M5 S1 (GitHub) - add 2 more (10 -> 12)
m5_idx = find_milestone('p01-m5')
m5_s1 = data['milestones'][m5_idx]['steps'][0]['substeps']
m5_s1.insert(4, {
    "order":"1.4b","action":"Staging'deki dosyalarda hassas bilgi olmadığını kontrol et","type":"terminal","command":"git status | grep -i env","expected_output":"(Sonuç boş olmalı — env dosyası staging'de olmamalı)","why":"1.4'te tüm dosyaları staging'e ekledik. .env dosyalarının yanlışlıkla eklenmediğini kontrol etmek güvenlik açısından zorunlu."
})
m5_s1.append({
    "order":"1.11","action":"GitHub repo'nun public olduğunu ve düzgün göründüğünü doğrula","type":"validate","validation":"GitHub repo sayfasında dosyalar görünmeli. .env dosyası olmamalı. Commit history temiz olmalı.","why":"Recruiter'lar GitHub profilini kontrol eder — temiz repo profesyonellik göstergesidir."
})

# M5 S2 (Vercel) - add 2 more (10 -> 12)
m5_s2 = data['milestones'][m5_idx]['steps'][1]['substeps']
m5_s2.insert(4, {
    "order":"2.4b","action":"Preview URL'de tüm sayfaları gez","type":"validate","validation":"Preview URL'yi aç. Ana sayfa, hakkımda, projeler, blog, iletişim sayfalarını tek tek kontrol et. Görseller yükleniyor mu, dark mode çalışıyor mu bak.","why":"2.4'te alınan preview deploy, production'dan önce son test fırsatı. Burada bulunan hatalar production'a sızmadan düzeltilebilir."
})
m5_s2.append({
    "order":"2.11","action":"GitHub entegrasyonunu ve auto-deploy'u doğrula","type":"validate","validation":"Vercel Dashboard > Project > Settings > Git'te GitHub repo bağlı olmalı. 'Auto deploy on push' aktif olmalı. Artık git push = otomatik deploy.","why":"CI/CD pipeline'ı sıfır konfigürasyonla hazır. Her push otomatik deploy tetikler."
})

# M5 S3 (Checklist) - add 2 more (10 -> 12)
m5_s3 = data['milestones'][m5_idx]['steps'][2]['substeps']
m5_s3.insert(4, {
    "order":"3.4b","action":"Loading state'lerini kontrol et","type":"validate","validation":"Yavaş ağ simülasyonunda (DevTools > Network > Slow 3G) sayfaların yüklenmesi sırasında beyaz ekran olmamalı. Font'lar display:swap ile yüklendiğinden sistem fontu geçici olarak görünmeli.","why":"Gerçek dünyada tüm kullanıcılar hızlı internet kullanmıyor. Yavaş bağlantıda da iyi deneyim sağlamak profesyonel kaliteyi gösterir."
})
m5_s3.append({
    "order":"3.11","action":"Production kontrol listesini tamamla ve Milestone 5'i commit'le","type":"terminal","command":"git add -A && git commit -m \"feat: complete production checklist with 404 page and final validations\"","expected_output":"[main ...] feat: complete production checklist...","why":"Production kontrol listesi tamamlandı. Site canlıya çıkmaya hazır."
})

# M5 S4 (README) - add 2 more (11 -> 13)
m5_s4 = data['milestones'][m5_idx]['steps'][3]['substeps']
m5_s4.insert(2, {
    "order":"4.2b","action":"Canlı demo linkini README'nin en üstüne ekle","type":"code_add","file":"README.md","position":"top","code":"[Canlı Demo](https://portfolio-site.vercel.app) | [GitHub Repo](https://github.com/username/portfolio-site)","why":"Recruiter'lar önce projeyi görmek ister, sonra kodu inceler. Demo linki en üstte olmalı."
})
m5_s4.insert(8, {
    "order":"4.6b","action":"'Öğrendiklerim' bölümünü ekle","type":"code_add","file":"README.md","position":"after_structure","code":"## Öğrendiklerim\n\n- Next.js App Router ve Server Components mimarisi\n- Static Site Generation ile performans optimizasyonu\n- MDX ile interaktif blog sistemi kurulumu\n- Core Web Vitals ve Lighthouse optimizasyonu\n- WCAG 2.1 AA erişilebilirlik standartları","why":"'Öğrendiklerim' bölümü growth mindset'i gösterir. Recruiter'lar sadece ne yaptığını değil, ne öğrendiğini de merak eder."
})

# Deployment milestone - add more to each step
dep_idx = len(data['milestones']) - 1

# Production Build - add 2 more (10 -> 12)
dep_s1 = data['milestones'][dep_idx]['steps'][0]['substeps']
dep_s1.insert(3, {
    "order":"1.3b","action":"Prettier ile tüm dosyaları formatla","type":"terminal","command":"pnpm dlx prettier --write src/","expected_output":"src/... (tüm dosyalar formatlandı)","why":"Build öncesi tüm dosyaların tutarlı formatta olduğundan emin oluyoruz. Format hataları code review'da dikkat dağıtır."
})
dep_s1.insert(5, {
    "order":"1.4b","action":"Build çıktısında her route'un boyutunu incele","type":"validate","validation":"Build çıktısında her route'un First Load JS boyutu < 100KB olmalı. Kırmızı renkle işaretlenen büyük sayfalar varsa optimize edilmeli.","why":"100KB üzeri First Load JS mobil kullanıcılar için ciddi performans sorunu yaratır."
})

# Deploy - add 2 more (10 -> 12)
dep_s2 = data['milestones'][dep_idx]['steps'][1]['substeps']
dep_s2.insert(6, {
    "order":"2.6b","action":"İletişim formunu production'da test et","type":"validate","validation":"İletişim formunu test verisiyle doldur ve gönder. Formspree'den e-posta geldiğini doğrula.","why":"Form submission production'da farklı davranabilir — özellikle CORS ayarları lokal ile farklı olabilir."
})
dep_s2.insert(7, {
    "order":"2.7b","action":"Gerçek telefonda test et","type":"validate","validation":"Gerçek bir telefonda production URL'yi aç. Navigation, görseller ve form çalışmalı.","why":"Gerçek mobil cihazda test, emülatörden daha güvenilir sonuç verir."
})

# README - add 2 more (10 -> 12)
dep_s3 = data['milestones'][dep_idx]['steps'][2]['substeps']
dep_s3.insert(3, {
    "order":"3.3b","action":"Screenshot'ları docs/ klasörüne ekle","type":"explain","why":"Siteyi 3 farklı açıdan screenshot al: ana sayfa (desktop), blog yazısı ve mobil görünüm. docs/ klasörüne kaydet ve README'ye bağla."
})
dep_s3.insert(8, {
    "order":"3.7b","action":"GitHub repo topics ve description ekle","type":"explain","why":"GitHub repo > Settings'ten Description alanını doldur ve Topics ekle: nextjs, typescript, tailwindcss, portfolio, blog. Bu bilgiler GitHub arama sonuçlarında görünür."
})

# Demo Video - add 2 more (10 -> 12)
dep_s4 = data['milestones'][dep_idx]['steps'][3]['substeps']
dep_s4.insert(2, {
    "order":"4.2b","action":"Demo senaryosunu planla — 2-3 dakikalık script","type":"explain","why":"Senaryo: 1) Ana sayfa hero, 2) Sayfalar arası gezinti, 3) Dark mode toggle, 4) Mobil görünüm (DevTools), 5) Blog yazısı, 6) İletişim formu. Plansız video dağınık ve uzun olur."
})
dep_s4.insert(5, {
    "order":"4.4b","action":"Mimari kararları kısa açıkla","type":"explain","why":"Video'nun son 30 saniyesinde: 'Next.js App Router tercih ettim çünkü SSG ile performans avantajı sağlıyor. MDX ile blog sistemi kurdum. Lighthouse 95+ skor elde ettim.' Bu, teknik iletişim becerisini gösterir."
})

# Save
with open('content/projects/project-01.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Count
total = 0
for m in data['milestones']:
    for s in m.get('steps', []):
        n = len(s.get('substeps', []))
        total += n
        step_id = s.get('step', s.get('title', '?'))
        print(f'{m.get("id", "?")} step {step_id}: {n} substeps')
print(f'\nFINAL TOTAL: {total}')
