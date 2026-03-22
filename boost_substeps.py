#!/usr/bin/env python3
"""Boost substeps to reach 400+ total."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('content/projects/project-01.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def find_milestone(mid):
    for i, m in enumerate(data['milestones']):
        if m.get('id') == mid:
            return i
    return None

# Need ~60 more substeps to reach 400. Add 2-3 per step across the board.

# M1 S1 (10 -> 13)
m1_idx = find_milestone('p01-m1')
s = data['milestones'][m1_idx]['steps'][0]['substeps']
s.insert(5, {"order":"1.5b","action":"next.config.mjs dosyasını aç ve yapısını incele","type":"file_open","file":"next.config.mjs","why":"1.3'te create-next-app'in oluşturduğu Next.js konfigürasyon dosyası. İleride image optimizasyonu, security header'ları ve diğer ayarları buraya ekleyeceğiz."})
s.insert(7, {"order":"1.7b","action":"tailwind.config.ts dosyasını kontrol et — Tailwind v4 mü?","type":"file_open","file":"tailwind.config.ts","why":"Tailwind versiyonunu doğrulamak önemli. v4 ise CSS-first konfigürasyon kullanacağız (Step 3'te). v3 ise farklı yaklaşım gerekir."})
s.insert(9, {"order":"1.8b","action":"DevTools Console'da hata olmadığını doğrula","type":"validate","validation":"Tarayıcıda F12 ile DevTools aç, Console sekmesinde kırmızı hata olmamalı. Warning'ler olabilir — bunlar şimdilik önemli değil.","why":"1.8'de dev server'ı başlattık. Console hataları varsa temel kurulumda sorun var demektir."})

# M1 S2 (11 -> 13)
s = data['milestones'][m1_idx]['steps'][1]['substeps']
s.insert(6, {"order":"2.5b","action":"Prettier'ın Tailwind class sıralamasını doğrula","type":"validate","validation":"Bir .tsx dosyasında Tailwind class'larını rastgele sırada yaz (örn: 'text-white bg-blue-500 p-4'). Kaydet — Prettier 'bg-blue-500 p-4 text-white' şeklinde yeniden sıralamalı.","why":"2.5'te eklediğimiz prettier-plugin-tailwindcss'in doğru çalıştığını somut bir örnekle doğruluyoruz."})
s.insert(8, {"order":"2.7b","action":"ESLint'in çalıştığını doğrula","type":"terminal","command":"pnpm lint","expected_output":"✔ No ESLint warnings or errors","why":"2.8'de ESLint config'i güncelledik. lint komutunun hatasız çalışması, ESLint ve Prettier'ın uyumlu olduğunu kanıtlar."})

# M1 S3 (11 -> 13)
s = data['milestones'][m1_idx]['steps'][2]['substeps']
s.insert(4, {"order":"3.4b","action":"Tailwind v4 CSS-first yaklaşımını anla","type":"explain","why":"Tailwind v4'te konfigürasyon CSS dosyasında yapılır — tailwind.config.ts yerine @theme ve @plugin direktifleri kullanılır. Bu yaklaşım build tooling'den bağımsızdır ve daha hızlı build süreleri sağlar. v3'ten v4'e geçişte en büyük fark budur."})
s.insert(9, {"order":"3.8b","action":"@theme bloğunun son halini kontrol et","type":"validate","validation":"globals.css'te @theme bloğu içinde primary renk paleti (50-900), dark mode renkleri (dark-bg, dark-card, dark-text) ve font tanımları olmalı. Toplam 16+ CSS custom property.","why":"3.6-3.8'de eklediğimiz tüm design token'ların @theme bloğunda düzgün tanımlandığını doğruluyoruz."})

# M1 S4 (12 -> 14)
s = data['milestones'][m1_idx]['steps'][3]['substeps']
s.insert(6, {"order":"4.6b","action":"İki font'un birlikte çalıştığını test et","type":"validate","validation":"page.tsx'te geçici olarak <code className='font-mono'>test</code> ekle. JetBrains Mono fontu görünmeli. Normal metin Inter ile render edilmeli. Test sonrası kodu sil.","why":"4.4'te Inter'ı, 4.6'da JetBrains Mono'yu tanımladık. İkisinin birlikte çalıştığını doğruluyoruz."})
s.insert(10, {"order":"4.9b","action":"Title template'inin çalıştığını doğrula","type":"validate","validation":"Tarayıcı sekmesinde 'Adın Soyadın | Full Stack Developer' yazmalı. Bu, 4.9'da tanımladığımız default title.","why":"4.9'daki metadata tanımının browser tab'ında doğru görünüp görünmediğini kontrol ediyoruz."})

# M2 S4 (10 -> 13)
m2_idx = find_milestone('p01-m2')
s = data['milestones'][m2_idx]['steps'][3]['substeps']
s.insert(3, {"order":"4.3b","action":"TypeScript'in Project interface'ini doğru uyguladığını kontrol et","type":"terminal","command":"pnpm tsc --noEmit","expected_output":"(hata yoksa çıktı boş)","why":"4.2-4.3'te yazdığımız interface ve verilerin uyumlu olduğunu TypeScript derleyicisi ile doğruluyoruz."})
s.insert(7, {"order":"4.7b","action":"Projeler sayfasında hover efektini test et","type":"validate","validation":"Proje kartına hover et. border rengi değişmeli ve shadow belirmeli (hover:border-primary-300 hover:shadow-lg). Geçiş yumuşak olmalı.","why":"4.7'de eklediğimiz transition-all class'ının çalıştığını doğruluyoruz."})
s.insert(9, {"order":"4.8b","action":"About sayfasının prose tipografisini kontrol et","type":"validate","validation":"/about sayfasında paragraflar arası boşluk düzgün olmalı, font boyutu okunabilir olmalı. prose class'ı @tailwindcss/typography'den geliyor — M1 Step 3'te kurmuştuk.","why":"4.8'de eklediğimiz prose class'ının çalıştığını doğruluyoruz. M1'deki @plugin tanımına bağımlı."})

# M3 S2 (12 -> 14)
m3_idx = find_milestone('p01-m3')
s = data['milestones'][m3_idx]['steps'][1]['substeps']
s.insert(7, {"order":"2.7b","action":"Menü açıkken scroll'u kontrol et","type":"validate","validation":"Mobil menü açıkken sayfayı kaydırmayı dene. Menü sabit kalmalı, arka plan kaymalı. Menünün içeriğin arkasına düşmemesi için z-index doğru olmalı.","why":"2.7'de eklediğimiz shadow-lg ve absolute positioning'in farklı sayfa uzunluklarında düzgün çalışıp çalışmadığını test ediyoruz."})
s.insert(10, {"order":"2.9b","action":"Header'ın tüm breakpoint'lerde düzgün göründüğünü doğrula","type":"validate","validation":"DevTools'ta tarayıcıyı yavaş yavaş daralt ve genişlet. 768px geçişinde hamburger <-> desktop linkleri geçişi pürüzsüz olmalı. İkisi aynı anda görünmemeli.","why":"2.9'da eklediğimiz hidden md:flex ve md:hidden class'larının breakpoint geçişinde düzgün çalışıp çalışmadığını kontrol ediyoruz."})

# M3 S4 (11 -> 13)
s = data['milestones'][m3_idx]['steps'][3]['substeps']
s.insert(7, {"order":"4.7b","action":"Focus-visible stilinin çalıştığını test et","type":"validate","validation":"Tab tuşu ile sayfadaki elementler arasında gezin. Her odaklanan elementte mavi outline (2px solid primary-500) görünmeli. Mouse ile tıklayınca outline görünmemeli.","why":"4.7'de eklediğimiz focus-visible stilinin düzgün çalışıp çalışmadığını test ediyoruz."})
s.insert(9, {"order":"4.8b","action":"Blog ve projeler sayfalarına da animasyon class'ları ekle","type":"code_modify","file":"src/app/blog/page.tsx","code":"<main className=\"mx-auto max-w-3xl px-4 py-16 animate-fade-in\">","why":"4.8'de ana sayfaya eklediğimiz animasyonu diğer sayfalara da ekliyoruz. Tutarlı animasyon deneyimi tüm sayfaları kapsamalı."})

# M4 S4 (12 -> 14)
m4_idx = find_milestone('p01-m4')
s = data['milestones'][m4_idx]['steps'][3]['substeps']
s.insert(3, {"order":"4.3b","action":"SkipNav'ı ThemeProvider'dan ÖNCE konumlandır","type":"explain","why":"Tab sıralamasında SkipNav ilk odaklanan element olmalı. ThemeProvider'dan bile önce gelmeli — aksi halde kullanıcı önce tema butonuna Tab'lar ve skip link amacını kaybeder."})
s.insert(8, {"order":"4.7b","action":"Tüm img elementlerinde alt attribute'u kontrol et","type":"validate","validation":"DevTools > Elements'te tüm img tag'lerini ara. Her birinde anlamlı alt attribute'u olmalı. Dekoratif görsellerde alt='' (boş string) olmalı — screen reader bunları atlar.","why":"WCAG 1.1.1 zorunluluğu: her görselin metin alternatifi olmalı. alt='resim' veya alt='image' gibi anlamsız değerler kabul edilmez."})

# M4 S5 (12 -> 14)
s = data['milestones'][m4_idx]['steps'][4]['substeps']
s.insert(3, {"order":"5.3b","action":"CSP header'ını test et — inline script/style çalışıyor mu?","type":"validate","validation":"Sayfayı aç ve DevTools Console'da CSP ile ilgili hata olup olmadığını kontrol et. 'Refused to execute inline script' hatası varsa script-src'ye 'unsafe-inline' eklenmeli.","why":"5.3'te eklediğimiz CSP header'ı çok kısıtlayıcı olabilir. Next.js inline script/style kullanır — bunları engellemediğinden emin olmalıyız."})
s.insert(8, {"order":"5.7b","action":"Lighthouse'u Incognito mode'da çalıştır","type":"validate","validation":"Incognito pencerede (Ctrl+Shift+N) Lighthouse audit çalıştır. Extension'lar ve cache olmadan daha doğru sonuç verir. Her kategori 95+ olmalı.","why":"5.8'deki audit'i extension'lar etkileyebilir. Incognito mode daha temiz bir ortam sağlar."})

# M5 S3 (12 -> 14)
m5_idx = find_milestone('p01-m5')
s = data['milestones'][m5_idx]['steps'][2]['substeps']
s.insert(5, {"order":"3.5b","action":"SEO meta tag'lerini production URL'de doğrula","type":"validate","validation":"Production URL'de View Page Source (Ctrl+U) ile HTML'i aç. og:title, og:image, description meta tag'lerinin var olduğunu doğrula. Client-side değil server-side render edilmeli.","why":"M4'te eklediğimiz SEO meta tag'lerinin production'da da doğru çalıştığını kontrol ediyoruz."})
s.insert(8, {"order":"3.7b","action":"Sitemap.xml'i production URL'de kontrol et","type":"validate","validation":"https://your-domain.vercel.app/sitemap.xml adresini aç. Tüm sayfalar ve blog yazıları listelenmiş olmalı.","why":"M4'te oluşturduğumuz sitemap'in production'da da düzgün çalıştığını doğruluyoruz."})

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
