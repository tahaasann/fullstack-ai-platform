# Lessons Learned — Proje Substep Kalitesi

## Ders 1: Ajanlar "böl" değil "öğret" olarak yönlendirilmeli
- **Hata:** Ajanlara "kodu böl" dedim, "öğret" demedim
- **Sonuç:** Mekanik a/b/c bölme, template why'lar
- **Kural:** Ajan prompt'unda "her substep bir DERS olmalı" vurgulanmalı

## Ders 2: Ajan çıktısı commit etmeden ÖNCE doğrulanmalı
- **Hata:** Ajan "done" deyince commit ettim, kontrol etmedim
- **Sonuç:** Kırık substep'ler, syntax hataları, why-code uyumsuzlukları
- **Kural:** Her ajan sonrası şu script çalışmalı:
  - broken: 0 (order/action/type eksik)
  - boilerplate: 0 (template why)
  - over8: 0 (>8 satır kod)
  - brace: 0 (kapanış-parantez tek substep)
  - letter_suffix: 0 (a/b/c suffix)
  - mid_expression: 0 (açılıp kapatılmamış brace)
  - code_write_dup: 0 (aynı dosyaya tekrar code_write)
  - broken_syntax: 0 (fazla kapanış parantezi)

## Ders 3: İyi substep'lere DOKUNMA
- **Hata:** "Tüm substep'leri yeniden yaz" dedim, iyi olanları da bozdu
- **Sonuç:** Puanlar her turda düştü (7.9 → 7.6 → 6.0 → 5.3)
- **Kural:** "SADECE sorunlu substep'leri düzelt, geri kalanına DOKUNMA"

## Ders 4: Bir şey ters giderse DUR, körü körüne devam etme
- **Hata:** Puanlar düşerken aynı stratejiyle devam ettim
- **Sonuç:** 6 tur düzeltme, her biri daha kötü
- **Kural:** Puan düşerse stratejiyi değiştir, aynı şeyi tekrarlama

## Ders 5: Doğrulama otomatik olmalı
- **Hata:** Manuel kontrol yaptım, gözden kaçanlar oldu
- **Kural:** Her commit öncesi doğrulama scriptini çalıştır, 0 olmayan metriklerde commit ETME

## Ders 6: Küçük, cerrahi müdahaleler büyük yeniden yazımlardan iyidir
- **Hata:** "Tüm milestone'ları yeniden yaz" → yeni sorunlar
- **Sonuç:** Cerrahi script (34 type fix + 24 syntax fix) en etkili çözüm oldu
- **Kural:** Sorunlu substep'leri tespit et, sadece onları düzelt, geri kalanına dokunma
