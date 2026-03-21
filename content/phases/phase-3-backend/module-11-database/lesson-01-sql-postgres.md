---
title: "SQL Temelleri ve PostgreSQL: İlişkisel Veritabanı Mastery"
id: "mod-11-db/lesson-01"
estimated_minutes: 60
order: 1
tags: ["sql", "postgresql", "database", "joins", "indexing", "transactions"]
prerequisites: ["mod-10-api/lesson-01"]
---

# SQL Temelleri ve PostgreSQL: İlişkisel Veritabanı Mastery

:::realworld
Her backend uygulamasının kalbinde bir veritabanı vardır. Netflix izleme geçmişinden, bankacılık işlemlerine kadar her şey SQL ile yönetilir. Bir e-ticaret sitesinde "Bu ürünü alan kullanıcılar şunları da aldı" önerisi bile arkada karmaşık SQL JOIN'leri ve window function'larla çalışır. Bu derste SQL'i deha seviyesinde öğrenecek, mülakatlarda karşına çıkan her sorguyu yazabilecek hale geleceksin.
:::

## Neden SQL Öğreniyorsun?

İlişkisel veritabanları 1970'lerden beri yazılım dünyasının temel taşı. NoSQL ne kadar popüler olursa olsun, iş dünyasının %80'i hala ilişkisel veritabanı kullanıyor. SQL bilmeden:

- Backend API yazamazsın
- Veri analizi yapamazsın
- Mülakat geçemezsin (SQL soruları %90 oranında soruluyor)
- Production veritabanı sorunlarını debug edemezsin

:::deha-tip
Deha seviyesi geliştiriciler, ORM'e körü körüne güvenmez. Prisma veya Sequelize kullanırken bile arka planda hangi SQL sorgusunun çalıştığını bilir, EXPLAIN ANALYZE ile sorguyu analiz eder. "ORM benim için yazıyor" demek yerine "ORM'un yazdığı sorguyu optimize edebilirim" der.
:::

## PostgreSQL Nedir ve Neden PostgreSQL?

:::concept[PostgreSQL (İng: PostgreSQL)]
PostgreSQL, açık kaynaklı, enterprise-grade ilişkisel veritabanı yönetim sistemidir. ACID uyumlu, extensible ve SQL standardına en yakın veritabanıdır.

**Türkçe karşılığı:** İlişkisel Veritabanı Yönetim Sistemi
**Ne işe yarar:** Verileri yapılandırılmış tablolarda saklar, sorgular ve yönetir
**Gerçek hayat benzetmesi:** Excel tabloları gibi düşün ama milyonlarca satırda bile hızlı çalışan, birden fazla tablonun birbiriyle ilişki kurabildiği bir sistem
:::

:::comparison
| Özellik | PostgreSQL | MySQL | SQLite |
|---------|-----------|-------|--------|
| Tip | Object-relational | Relational | Embedded |
| JSON desteği | JSONB (çok güçlü) | JSON (temel) | JSON (sınırlı) |
| Full-text search | Yerleşik (GIN index) | Yerleşik | FTS5 extension |
| Performans | Karmaşık sorgularda üstün | Basit read'lerde hızlı | Tek kullanıcılı |
| **Ne zaman kullan** | Production API, karmaşık veri | WordPress, basit CRUD | Mobil, test, prototip |
| Şirketler | Instagram, Spotify, Reddit | Facebook, Twitter | Android, iOS, Electron |

**Tavsiye:** Yeni projelerde PostgreSQL kullan. Hem SQL standardına en yakın hem de en fazla özelliğe sahip açık kaynak veritabanı.
:::

## CRUD İşlemleri: SQL'in Temelleri

### SELECT - Veri Sorgulama

:::code[sql]{title="SELECT Temel Kullanımlar"}
-- Tüm sütunları getir
SELECT * FROM users;

-- Belirli sütunları getir
SELECT first_name, last_name, email FROM users;

-- Koşullu sorgulama
SELECT * FROM users WHERE age >= 18 AND city = 'Istanbul';

-- Sıralama
SELECT * FROM products ORDER BY price DESC;

-- Limit ve Offset (pagination)
SELECT * FROM products ORDER BY created_at DESC LIMIT 10 OFFSET 20;

-- Benzersiz değerler
SELECT DISTINCT city FROM users;

-- Alias kullanımı
SELECT first_name AS ad, last_name AS soyad FROM users;

-- LIKE ile pattern matching
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- IN operatörü
SELECT * FROM users WHERE city IN ('Istanbul', 'Ankara', 'Izmir');

-- BETWEEN
SELECT * FROM orders WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- NULL kontrolü
SELECT * FROM users WHERE phone IS NOT NULL;
:::

### INSERT - Veri Ekleme

:::code[sql]{title="INSERT Kullanımları"}
-- Tek satır ekleme
INSERT INTO users (first_name, last_name, email)
VALUES ('Ahmet', 'Yilmaz', 'ahmet@example.com');

-- Çoklu satır ekleme
INSERT INTO users (first_name, last_name, email)
VALUES
  ('Mehmet', 'Kaya', 'mehmet@example.com'),
  ('Ayse', 'Demir', 'ayse@example.com'),
  ('Fatma', 'Celik', 'fatma@example.com');

-- INSERT ... RETURNING (PostgreSQL)
INSERT INTO users (first_name, email)
VALUES ('Ali', 'ali@example.com')
RETURNING id, first_name, created_at;

-- INSERT ... ON CONFLICT (Upsert)
INSERT INTO users (email, first_name)
VALUES ('ahmet@example.com', 'Ahmet')
ON CONFLICT (email)
DO UPDATE SET first_name = EXCLUDED.first_name;
:::

### UPDATE - Veri Güncelleme

:::code[sql]{title="UPDATE Kullanımları"}
-- Tek satır güncelleme
UPDATE users SET last_name = 'Ozturk' WHERE id = 1;

-- Birden fazla sütun güncelleme
UPDATE users
SET first_name = 'Ahmet', city = 'Ankara', updated_at = NOW()
WHERE id = 1;

-- Koşullu güncelleme
UPDATE products
SET price = price * 1.10
WHERE category = 'electronics' AND price < 1000;

-- Subquery ile güncelleme
UPDATE orders
SET status = 'cancelled'
WHERE user_id IN (SELECT id FROM users WHERE is_banned = true);
:::

:::beginner-mistake
Yaygın hata: UPDATE veya DELETE sorgusunda WHERE koşulu yazmayı unutmak. `UPDATE users SET role = 'admin'` yazarsan TÜM kullanıcılar admin olur! Her zaman önce SELECT ile kontrol et, sonra UPDATE/DELETE yaz.
:::

### DELETE - Veri Silme

:::code[sql]{title="DELETE Kullanımları"}
-- Tek satır silme
DELETE FROM users WHERE id = 1;

-- Koşullu silme
DELETE FROM sessions WHERE expires_at < NOW();

-- Tüm tabloyu temizleme (dikkatli ol!)
TRUNCATE TABLE logs;  -- DELETE'den çok daha hızlı, auto-increment sıfırlanır

-- Soft delete (önerilen yaklaşım)
UPDATE users SET deleted_at = NOW() WHERE id = 1;
-- Sorgularda: SELECT * FROM users WHERE deleted_at IS NULL;
:::

:::tip
Production'da fiziksel DELETE yerine soft delete kullan. deleted_at sütunu ekleyerek veriyi "silinmiş" olarak işaretle. Bu sayede yanlışlıkla silinen veriyi kurtarabilirsin.
:::

## Aggregation Fonksiyonları

:::code[sql]{title="Aggregation Fonksiyonları"}
-- COUNT: Satır sayısı
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT city) FROM users;

-- SUM, AVG, MIN, MAX
SELECT
  SUM(amount) AS toplam_satis,
  AVG(amount) AS ortalama_satis,
  MIN(amount) AS en_dusuk,
  MAX(amount) AS en_yuksek,
  COUNT(*) AS siparis_sayisi
FROM orders
WHERE status = 'completed';

-- GROUP BY ile gruplama
SELECT city, COUNT(*) AS kullanici_sayisi
FROM users
GROUP BY city
ORDER BY kullanici_sayisi DESC;

-- HAVING: GROUP BY sonrası filtreleme
SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 100
ORDER BY avg_price DESC;
:::

## JOINs Derinlemesine

JOIN'ler SQL'in en güçlü özelliğidir. Farklı tablolardaki verileri birleştirmeni sağlar.

:::concept[JOIN (İng: Join)]
JOIN, iki veya daha fazla tabloyu ortak bir sütun üzerinden birleştiren SQL operasyonudur.

**Türkçe karşılığı:** Birleştirme
**Ne işe yarar:** İlişkili tablolardaki verileri tek bir sonuç setinde birleştirir
**Gerçek hayat benzetmesi:** İki Excel tablosunu ortak sütuna (örn: müşteri ID) göre birleştirmek
:::

:::code[sql]{title="Örnek Tablolar"}
-- users tablosu
-- | id | name    | city_id |
-- |----|---------|---------|
-- | 1  | Ahmet   | 1       |
-- | 2  | Ayse    | 2       |
-- | 3  | Mehmet  | NULL    |

-- cities tablosu
-- | id | name      |
-- |----|-----------|
-- | 1  | Istanbul  |
-- | 2  | Ankara    |
-- | 3  | Izmir     |
:::

### INNER JOIN

İki tabloda da eşleşen satırları getirir. Eşleşmeyen satırlar sonuçta yer almaz.

:::code[sql]{title="INNER JOIN"}
SELECT u.name, c.name AS city
FROM users u
INNER JOIN cities c ON u.city_id = c.id;

-- Sonuç:
-- | name  | city     |
-- |-------|----------|
-- | Ahmet | Istanbul |
-- | Ayse  | Ankara   |
-- Mehmet (city_id NULL) ve Izmir (kullanıcısı yok) sonuçta YOK
:::

### LEFT JOIN (LEFT OUTER JOIN)

Sol tablodaki TÜM satırları getirir. Sağ tabloda eşleşme yoksa NULL döner.

:::code[sql]{title="LEFT JOIN"}
SELECT u.name, c.name AS city
FROM users u
LEFT JOIN cities c ON u.city_id = c.id;

-- Sonuç:
-- | name   | city     |
-- |--------|----------|
-- | Ahmet  | Istanbul |
-- | Ayse   | Ankara   |
-- | Mehmet | NULL     |  ← city_id NULL olduğu için
:::

### RIGHT JOIN (RIGHT OUTER JOIN)

Sağ tablodaki TÜM satırları getirir. Sol tabloda eşleşme yoksa NULL döner.

:::code[sql]{title="RIGHT JOIN"}
SELECT u.name, c.name AS city
FROM users u
RIGHT JOIN cities c ON u.city_id = c.id;

-- Sonuç:
-- | name  | city     |
-- |-------|----------|
-- | Ahmet | Istanbul |
-- | Ayse  | Ankara   |
-- | NULL  | Izmir    |  ← Kullanıcısı yok ama şehir gösteriliyor
:::

### FULL OUTER JOIN

Her iki tablodaki TÜM satırları getirir. Eşleşme yoksa karşı taraf NULL olur.

:::code[sql]{title="FULL OUTER JOIN"}
SELECT u.name, c.name AS city
FROM users u
FULL OUTER JOIN cities c ON u.city_id = c.id;

-- Sonuç:
-- | name   | city     |
-- |--------|----------|
-- | Ahmet  | Istanbul |
-- | Ayse   | Ankara   |
-- | Mehmet | NULL     |
-- | NULL   | Izmir    |
:::

### SELF JOIN

Bir tabloyu kendisiyle birleştirir. Hiyerarşik verilerde (çalışan-yönetici) kullanılır.

:::code[sql]{title="SELF JOIN"}
-- employees tablosu
-- | id | name    | manager_id |
-- |----|---------|------------|
-- | 1  | Ali     | NULL       |  (CEO)
-- | 2  | Veli    | 1          |
-- | 3  | Zeynep  | 1          |
-- | 4  | Can     | 2          |

SELECT
  e.name AS calisan,
  m.name AS yonetici
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Sonuç:
-- | calisan | yonetici |
-- |---------|----------|
-- | Ali     | NULL     |
-- | Veli    | Ali      |
-- | Zeynep  | Ali      |
-- | Can     | Veli     |
:::

### CROSS JOIN

İki tablonun kartezyen çarpımını üretir. Her satır diğer tablodaki her satırla eşleşir.

:::code[sql]{title="CROSS JOIN"}
SELECT colors.name, sizes.name
FROM colors CROSS JOIN sizes;

-- colors: Kırmızı, Mavi  |  sizes: S, M, L
-- Sonuç: 2 × 3 = 6 satır
-- Kırmızı-S, Kırmızı-M, Kırmızı-L, Mavi-S, Mavi-M, Mavi-L
:::

### Çoklu JOIN

:::code[sql]{title="Birden Fazla Tablo JOIN'leme"}
-- Sipariş detaylarını kullanıcı ve ürün bilgisiyle getir
SELECT
  u.name AS musteri,
  p.name AS urun,
  oi.quantity AS adet,
  oi.unit_price AS birim_fiyat,
  o.created_at AS siparis_tarihi
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.status = 'completed'
ORDER BY o.created_at DESC;
:::

## Subqueries, CTEs ve Window Functions

### Subqueries (Alt Sorgular)

:::code[sql]{title="Subquery Örnekleri"}
-- Scalar subquery: Ortalama fiyatın üstündeki ürünler
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- IN subquery: En az 1 sipariş veren kullanıcılar
SELECT name, email
FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders);

-- EXISTS subquery: Sipariş veren kullanıcılar (daha performanslı)
SELECT u.name, u.email
FROM users u
WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id
);

-- Correlated subquery: Her kategorideki en pahalı ürün
SELECT p.name, p.price, p.category
FROM products p
WHERE p.price = (
  SELECT MAX(p2.price) FROM products p2
  WHERE p2.category = p.category
);
:::

### CTEs (Common Table Expressions) - WITH Clause

:::concept[CTE (Common Table Expression)]
CTE, bir SQL sorgusunda geçici bir isimlendirilmiş sonuç kümesi tanımlar. Karmaşık sorguları okunabilir parçalara böler.

**Türkçe karşılığı:** Ortak Tablo İfadesi
**Ne işe yarar:** Karmaşık sorguları modüler, okunabilir hale getirir
**Gerçek hayat benzetmesi:** Bir matematik problemini ara adımlarla çözmek gibi
:::

:::code[sql]{title="CTE Örnekleri"}
-- Basit CTE
WITH active_users AS (
  SELECT id, name, email
  FROM users
  WHERE is_active = true AND last_login > NOW() - INTERVAL '30 days'
)
SELECT au.name, COUNT(o.id) AS order_count
FROM active_users au
LEFT JOIN orders o ON au.id = o.user_id
GROUP BY au.name;

-- Birden fazla CTE
WITH monthly_sales AS (
  SELECT
    DATE_TRUNC('month', created_at) AS month,
    SUM(total_amount) AS revenue
  FROM orders
  WHERE status = 'completed'
  GROUP BY DATE_TRUNC('month', created_at)
),
sales_growth AS (
  SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
      (revenue - LAG(revenue) OVER (ORDER BY month))
      / LAG(revenue) OVER (ORDER BY month) * 100, 2
    ) AS growth_pct
  FROM monthly_sales
)
SELECT * FROM sales_growth ORDER BY month DESC;

-- Recursive CTE: Kategori hiyerarşisi
WITH RECURSIVE category_tree AS (
  -- Base case: Üst kategoriler
  SELECT id, name, parent_id, 0 AS depth
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  -- Recursive case: Alt kategoriler
  SELECT c.id, c.name, c.parent_id, ct.depth + 1
  FROM categories c
  INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY depth, name;
:::

### Window Functions

:::concept[Window Function (İng: Window Function)]
Window function, satır grupları (window) üzerinde hesaplama yapar ancak GROUP BY gibi satırları birleştirmez. Her satır korunur ve yanına hesaplanan değer eklenir.

**Türkçe karşılığı:** Pencere Fonksiyonu
**Ne işe yarar:** Sıralama, kümülatif toplam, önceki/sonraki değer gibi analitik hesaplamalar
**Gerçek hayat benzetmesi:** Sınav sonuçlarında hem kendi notunu hem sıralamam hem de sınıf ortalamasını görmek
:::

:::code[sql]{title="Window Functions"}
-- ROW_NUMBER: Her satıra sıra numarası ata
SELECT
  name,
  category,
  price,
  ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rank_in_category
FROM products;

-- RANK vs DENSE_RANK
SELECT
  name,
  score,
  RANK() OVER (ORDER BY score DESC) AS rank,        -- 1, 2, 2, 4 (boşluk bırakır)
  DENSE_RANK() OVER (ORDER BY score DESC) AS dense   -- 1, 2, 2, 3 (boşluk bırakmaz)
FROM students;

-- LEAD / LAG: Sonraki/önceki satır değeri
SELECT
  date,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY date) AS prev_day,
  LEAD(revenue, 1) OVER (ORDER BY date) AS next_day,
  revenue - LAG(revenue, 1) OVER (ORDER BY date) AS daily_change
FROM daily_sales;

-- SUM() OVER: Kümülatif toplam (running total)
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) AS running_total,
  SUM(amount) OVER (PARTITION BY category ORDER BY date) AS category_running_total
FROM transactions;

-- NTILE: N eşit gruba böl
SELECT
  name,
  salary,
  NTILE(4) OVER (ORDER BY salary DESC) AS quartile
FROM employees;

-- Mülakat klasiği: Her departmandan en yüksek maaşlı 3 kişi
SELECT * FROM (
  SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
  FROM employees
) ranked
WHERE rn <= 3;
:::

:::interview
**Mülakat Sorusu:** "Her kategorideki en çok satan 3 ürünü getir."

**Beklenen cevap:**
```sql
WITH ranked_products AS (
  SELECT
    p.name,
    p.category,
    SUM(oi.quantity) AS total_sold,
    DENSE_RANK() OVER (
      PARTITION BY p.category
      ORDER BY SUM(oi.quantity) DESC
    ) AS rank
  FROM products p
  JOIN order_items oi ON p.id = oi.product_id
  GROUP BY p.name, p.category
)
SELECT name, category, total_sold, rank
FROM ranked_products
WHERE rank <= 3;
```
ROW_NUMBER yerine DENSE_RANK kullanarak aynı satış sayısına sahip ürünlerin eşit sıralanmasını sağlıyoruz.
:::

## Indexing (İndeksleme)

:::concept[Index (İng: Index)]
Index, veritabanında sorgu performansını artırmak için oluşturulan veri yapısıdır. Kitabın sonundaki indeks gibi çalışır.

**Türkçe karşılığı:** İndeks / Dizin
**Ne işe yarar:** Milyonlarca satırda bile hızlı arama yapılmasını sağlar
**Gerçek hayat benzetmesi:** Bir kitapta belirli konuyu bulmak için sayfa sayfa bakmak yerine indekse bakmak
:::

### Index Türleri

:::code[sql]{title="PostgreSQL Index Türleri"}
-- B-tree Index (varsayılan, en yaygın)
-- Eşitlik ve sıralama sorguları için ideal
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_city_name ON users(city, last_name); -- Composite index

-- Hash Index
-- Sadece eşitlik (=) sorguları için, B-tree'den biraz hızlı
CREATE INDEX idx_users_email_hash ON users USING HASH (email);

-- GIN Index (Generalized Inverted Index)
-- Array, JSONB ve full-text search için
CREATE INDEX idx_products_tags ON products USING GIN (tags);
CREATE INDEX idx_users_profile ON users USING GIN (profile_data jsonb_path_ops);

-- GiST Index (Generalized Search Tree)
-- Geometrik veriler, range types, full-text search için
CREATE INDEX idx_locations_coords ON locations USING GiST (coordinates);

-- Partial Index: Sadece belirli koşulu karşılayan satırlar
CREATE INDEX idx_orders_pending ON orders(created_at)
WHERE status = 'pending';

-- Unique Index: Benzersizlik garantisi
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Expression Index: Hesaplanmış değer üzerinde index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
:::

### EXPLAIN ANALYZE

:::code[sql]{title="EXPLAIN ANALYZE ile Sorgu Optimizasyonu"}
-- Sorgunun çalışma planını gör
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'ahmet@example.com';

-- Index olmadan (Sequential Scan - KÖTÜ):
-- Seq Scan on users  (cost=0.00..1234.00 rows=1 width=100)
--   (actual time=15.234..45.678 rows=1 loops=1)
-- Planning Time: 0.085 ms
-- Execution Time: 45.721 ms

-- Index ile (Index Scan - İYİ):
-- Index Scan using idx_users_email on users  (cost=0.29..8.30 rows=1 width=100)
--   (actual time=0.025..0.026 rows=1 loops=1)
-- Planning Time: 0.085 ms
-- Execution Time: 0.042 ms

-- JOIN sorgusunu analiz et
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.name
ORDER BY order_count DESC
LIMIT 10;
:::

:::tip
EXPLAIN ANALYZE çıktısında dikkat edilecekler: Seq Scan (index ekle), Nested Loop (büyük tablolarda kötü), Sort (ORDER BY için index düşün), Hash Join (genelde iyi). cost değeri düşük olan plan daha iyidir.
:::

## Transactions ve ACID

:::concept[Transaction (İng: Transaction)]
Transaction, birden fazla SQL işleminin tek bir birim olarak yürütülmesidir. Ya hepsi başarılı olur ya da hiçbiri uygulanmaz.

**Türkçe karşılığı:** İşlem / İşlem Birimi
**Ne işe yarar:** Veri tutarlılığını garanti eder
**Gerçek hayat benzetmesi:** Banka havalesi: Gönderenin hesabından düşülür VE alıcıya eklenir. Biri yapılıp diğeri yapılamazsa, ikisi de geri alınır.
:::

:::code[sql]{title="Transaction Kullanımı"}
-- Banka havalesi örneği
BEGIN;

-- Ali'nin hesabından 1000 TL düş
UPDATE accounts SET balance = balance - 1000
WHERE user_id = 1 AND balance >= 1000;

-- Veli'nin hesabına 1000 TL ekle
UPDATE accounts SET balance = balance + 1000
WHERE user_id = 2;

-- Her iki işlem de başarılıysa onayla
COMMIT;

-- Hata olursa geri al
-- ROLLBACK;

-- SAVEPOINT: Transaction içinde kısmi geri alma
BEGIN;
UPDATE products SET stock = stock - 1 WHERE id = 1;
SAVEPOINT after_stock;
UPDATE orders SET status = 'shipped' WHERE id = 100;
-- Eğer shipping hata verirse sadece bu adımı geri al
ROLLBACK TO after_stock;
-- Stock güncellemesi kalır
COMMIT;
:::

### ACID Prensipleri

:::code[text]{title="ACID Prensipleri"}
A - Atomicity (Bölünmezlik)
    Transaction ya tamamen uygulanır ya da hiç uygulanmaz.
    Örnek: Havale sırasında bir hesaptan düşüldü ama diğerine eklenemedi →
           Her iki işlem de geri alınır.

C - Consistency (Tutarlılık)
    Transaction, veritabanını bir geçerli durumdan başka bir geçerli duruma geçirir.
    Örnek: Hesap bakiyesi negatife düşemez (constraint ihlali) → Transaction reddedilir.

I - Isolation (İzolasyon)
    Eş zamanlı transaction'lar birbirini etkilemez.
    Örnek: İki kişi aynı anda son ürünü satın almaya çalışırsa,
           sadece biri başarılı olur.

D - Durability (Dayanıklılık)
    COMMIT edilen veri kalıcıdır, sistem çökse bile kaybolmaz.
    Örnek: COMMIT sonrası sunucu çökse bile veri diskte güvendedir.
:::

### Isolation Levels

:::code[sql]{title="PostgreSQL Isolation Levels"}
-- Read Uncommitted → Dirty read mümkün (PostgreSQL'de Read Committed olarak çalışır)
-- Read Committed   → Varsayılan. Sadece COMMIT edilmiş veriyi görür.
-- Repeatable Read  → Transaction boyunca aynı veriyi görür.
-- Serializable     → En katı. Transaction'lar sıralı çalışmış gibi davranır.

SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- Kritik finansal işlem
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE; -- Satırı kilitle
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
:::

## Normalization (Normalizasyon)

:::concept[Normalization (İng: Normalization)]
Normalization, veritabanı tablolarını veri tekrarını (redundancy) azaltmak ve veri bütünlüğünü artırmak için yeniden yapılandırma sürecidir.

**Türkçe karşılığı:** Normalizasyon / Normalleştirme
**Ne işe yarar:** Veri tekrarını önler, güncelleme anomalilerini engeller
**Gerçek hayat benzetmesi:** Adres defterindeki adresleri ayrı bir listeye yazıp sadece referans vermek, her yere tam adresi yazmak yerine
:::

:::code[text]{title="Normalization Formları"}
1NF (First Normal Form - Birinci Normal Form):
  - Her sütun atomik (bölünemez) değer içermeli
  - Tekrarlayan gruplar olmamalı
  ✗ hobbies: "futbol, basketbol, yüzme"
  ✓ Ayrı bir hobbies tablosu oluştur

2NF (Second Normal Form):
  - 1NF + Her non-key sütun PRIMARY KEY'in TAMAMINA bağımlı olmalı
  - Kısmi bağımlılık (partial dependency) olmamalı
  ✗ order_items(order_id, product_id, product_name, quantity)
    → product_name sadece product_id'ye bağımlı, tüm PK'ye değil
  ✓ product_name'i products tablosuna taşı

3NF (Third Normal Form):
  - 2NF + Non-key sütunlar arasında bağımlılık olmamalı (transitive dependency)
  ✗ users(id, city, city_population)
    → city_population, city'ye bağımlı, id'ye değil
  ✓ city_population'ı cities tablosuna taşı

BCNF (Boyce-Codd Normal Form):
  - 3NF'in güçlendirilmiş hali
  - Her belirleyici (determinant) aday anahtar olmalı
  - Pratikte 3NF yeterlidir, BCNF nadir gerekir
:::

:::beginner-mistake
Yaygın hata: "Her zaman en yüksek normal formu uygula." Aşırı normalizasyon JOIN sayısını artırır ve performansı düşürür. Denormalizasyon bazen kasıtlı yapılır. Örneğin, sipariş tablosuna ürün adını kopyalamak (snapshot) iş kuralı gereği olabilir.
:::

## Pratik: E-ticaret Veritabanı Tasarımı

:::exercise
1. PostgreSQL kur (Docker önerilir): `docker run -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres:16`
2. Aşağıdaki tabloları oluştur:
   - users (id, first_name, last_name, email, created_at)
   - products (id, name, price, category, stock, created_at)
   - orders (id, user_id, total_amount, status, created_at)
   - order_items (id, order_id, product_id, quantity, unit_price)
3. Her tabloya 50+ test verisi ekle
4. Şu sorguları yaz:
   - Her kategorideki en pahalı 3 ürün (window function)
   - Son 30 günde sipariş veren ama henüz ödeme yapmamış kullanıcılar
   - Aylık satış trendi (CTE + window function)
   - En çok sipariş veren 10 şehir (JOIN + GROUP BY)
5. EXPLAIN ANALYZE ile sorgularını analiz et, gerekli index'leri ekle

---

### Alıştırma 2: Multi-Table JOIN Challenge (Orta)

Yukarıda oluşturduğun tablolara ek olarak şu tabloları ekle:

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INTEGER REFERENCES categories(id)  -- self-referencing (alt kategori)
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    user_id INTEGER REFERENCES users(id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Görev — Şu sorguları yaz:**

1. Her ürünün ortalama puanı, yorum sayısı ve en son yorum tarihi (LEFT JOIN — yorumu olmayan ürünler de görünmeli)
2. Hiç sipariş vermemiş kullanıcıları bul (LEFT JOIN + IS NULL veya NOT EXISTS — hangisi daha performanslı?)
3. Bir kullanıcının satın aldığı ama henüz yorum yazmadığı ürünler (3 tablo JOIN)
4. Kategori hiyerarşisini recursive CTE ile listele (parent → child ilişkisi)

```sql
-- Örnek: Recursive CTE ile kategori ağacı
WITH RECURSIVE category_tree AS (
    -- TODO: Base case (parent_id IS NULL olan root kategoriler)
    -- TODO: Recursive case (alt kategorileri ekle)
)
SELECT * FROM category_tree;
```

**Beklenen sonuç:** Her sorgu için EXPLAIN ANALYZE çalıştır. Sequential Scan yerine Index Scan kullanılıyorsa doğru index'leri eklemişsin demektir.

---

### Alıştırma 3: Window Functions ile Analytics Dashboard (Zor)

Aşağıdaki analitik sorguları window function'lar kullanarak yaz:

```sql
-- 1. Her kullanıcının siparişlerini sırala ve bir önceki sipariş tutarını göster
SELECT
    user_id,
    created_at,
    total_amount,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS order_number,
    LAG(total_amount) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_order_amount
    -- TODO: Bir önceki siparişe göre yüzde değişimi hesapla
FROM orders;

-- 2. Aylık satışların kümülatif toplamı (running total)
-- TODO: SUM() OVER ile implement et

-- 3. Her kategoride ürünleri fiyata göre sırala ve percentile hesapla
-- TODO: PERCENT_RANK() veya NTILE(4) kullan
-- Hangi ürünler "premium" segmentinde (üst %25)?

-- 4. 7 günlük hareketli ortalama (moving average) sipariş tutarı
-- TODO: AVG() OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) kullan

-- 5. Her kullanıcının ilk ve son sipariş tarihi arasındaki gün farkı (müşteri ömrü)
-- TODO: FIRST_VALUE() ve LAST_VALUE() kullan
```

**Beklenen sonuç:** Tüm sorgular çalışmalı ve doğru sonuç vermeli. Window function'ların GROUP BY'dan farkını açıkla: neden satır sayısı korunuyor?
:::

:::knowledge-check
type: multiple_choice
question: "LEFT JOIN ile INNER JOIN arasındaki temel fark nedir?"
options:
  - "LEFT JOIN daha hızlıdır"
  - "LEFT JOIN sol tablodaki tüm satırları korur, eşleşme yoksa NULL döner"
  - "INNER JOIN sadece sağ tablodaki satırları getirir"
  - "LEFT JOIN sadece NULL olan satırları getirir"
correct: 1
explanation: "LEFT JOIN, sol tablodaki TÜM satırları getirir. Sağ tabloda eşleşme yoksa NULL döner. INNER JOIN ise sadece her iki tabloda da eşleşen satırları getirir."
:::

:::knowledge-check
type: multiple_choice
question: "Aşağıdakilerden hangisi Window Function'dır?"
options:
  - "COUNT() ... GROUP BY"
  - "ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)"
  - "HAVING COUNT(*) > 5"
  - "DISTINCT ON"
correct: 1
explanation: "Window Function'lar OVER() clause ile kullanılır. ROW_NUMBER(), RANK(), DENSE_RANK(), LEAD(), LAG() gibi fonksiyonlar window function'dır. GROUP BY ile kullanılan aggregation'lardan farkı, satırları birleştirmemesidir."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "SQL JOIN turlerini (INNER, LEFT, RIGHT, FULL OUTER, CROSS) Venn diyagramlari ve gercek e-ticaret veritabani ornekleriyle acikla. Her JOIN turunun ne zaman kullanildigini, NULL davranisini ve performans etkisini goster. Self-join ve subquery'leri de ornekle."

**2. Pratik Uygulama:**
> "PostgreSQL ile bir e-ticaret veritabani tasarla: users, products, categories, orders, order_items tablolari. Foreign key iliskileri, uygun index'ler, CHECK constraint'leri ve transaction ornekleri yaz. Urun arama icin full-text search ve GIN index kullan."
> Takip: "EXPLAIN ANALYZE ile yavas sorgulari tespit et. Index'lerin sorgu planini nasil etkiledigini goster ve query optimization stratejileri uygula."

**3. Mukemmellik Icin:**
> "Production PostgreSQL veritabaninda performans sorunlari yasiyorum. pg_stat_statements ile yavas sorgulari bulma, EXPLAIN ANALYZE ciktisini okuma, index stratejisi (B-tree vs GIN vs GiST), connection pooling (PgBouncer), vacuum/analyze ve partitioning konularini pratikte nasil uygularim?"

### Pair Programming Ipucu
SQL yazarken AI'a EXPLAIN ANALYZE ciktisini yapistir ve sor: "Bu sorgunun calisma planini analiz et. Seq Scan neden Index Scan yerine secildi? Hangi index'i eklemeliyim? Estimated rows ile actual rows arasindaki fark neden bu kadar buyuk?"
:::

:::must-note
- CRUD: SELECT (sorgula), INSERT (ekle), UPDATE (güncelle), DELETE (sil)
- JOIN türleri: INNER (sadece eşleşen), LEFT (sol tablo tümü), RIGHT (sağ tablo tümü), FULL (her ikisi tümü), SELF (tablo kendisiyle), CROSS (kartezyen çarpım)
- Window Functions: ROW_NUMBER (sıra no), RANK (boşluklu sıralama), DENSE_RANK (boşluksuz), LEAD (sonraki), LAG (önceki), SUM/AVG OVER (kümülatif)
- CTE (WITH): Karmaşık sorguları okunabilir parçalara böler, recursive CTE hiyerarşik veri için
- Index türleri: B-tree (varsayılan, sıralama+eşitlik), Hash (sadece eşitlik), GIN (JSONB/array/full-text), GiST (geometrik/range)
- EXPLAIN ANALYZE: Seq Scan kötü (index ekle), Index Scan iyi. cost ve actual time'a bak
- ACID: Atomicity (hep/hiç), Consistency (tutarlı durum), Isolation (eş zamanlı izolasyon), Durability (kalıcılık)
- Normalization: 1NF (atomik), 2NF (kısmi bağımlılık yok), 3NF (geçişli bağımlılık yok), BCNF (her determinant aday anahtar)
- Production'da soft delete kullan (deleted_at), UPDATE/DELETE'de WHERE unutma, transaction'larda ROLLBACK planla
- PostgreSQL avantajları: JSONB, CTE, Window Functions, GIN index, RETURNING clause, ON CONFLICT (upsert)
:::

:::senior-learns
Bir Senior Developer veya CTO, SQL ve veritabanı konusunu öğrenirken şu yaklaşımı benimser:

1. **Query execution plan okumayı ustalaşır** - EXPLAIN ANALYZE çıktısını satır satır okur. Seq Scan, Hash Join, Nested Loop, Bitmap Index Scan ne demek bilir. pg_stat_statements extension'ı ile en yavaş sorguları tespit eder.
2. **Index stratejisi geliştirir** - Her sütuna index eklemek yerine, sorgu pattern'lerine göre composite index oluşturur. Covering index (INCLUDE) ile index-only scan sağlar. Partial index ile gereksiz veri indekslemeyi önler.
3. **Connection pooling uygular** - PgBouncer veya pgpool-II ile bağlantı havuzu yönetir. Her request'te yeni connection açmanın production'da nasıl felaket olduğunu bilir.
4. **Migration stratejisi geliştirir** - Schema değişikliklerini versiyon kontrol altında tutar. Zero-downtime migration yapar: önce yeni sütunu ekle, kodu güncelle, eski sütunu kaldır. Lock'lama riskini minimize eder.
5. **Monitoring ve alerting kurar** - pg_stat_activity ile aktif sorguları, pg_stat_user_tables ile table bloat'ı, dead tuple oranını izler. Slow query log'u analiz eder.
6. **Partitioning uygular** - Milyonlarca satırlık tabloları date-based range partitioning ile böler. Archive partition'ları ayrı tablespace'e taşır.

**Karar Verme Sureci — PostgreSQL vs MySQL vs MongoDB:**
- **PostgreSQL**: JSONB, full-text search, CTE, window functions, row-level security, extensions (PostGIS, pgvector). Trade-off: MySQL'e gore baslangicta biraz daha karmasik, cloud managed servislerde MySQL'den pahali olabilir. Kullanim: Neredeyse her sey — ozellikle karmasik sorgular, GIS verileri, AI/ML (pgvector ile embedding storage).
- **MySQL**: Daha basit, daha yaygın hosting, replication kurulumu kolay. Trade-off: JSONB destegi sinirli, CTE performansi dusuk, partial index yok. Kullanim: WordPress, legacy projeler, basit CRUD uygulamalar.
- **MongoDB**: Schema-less, horizontal scaling (sharding) kolay, document model. Trade-off: JOIN yok (lookup var ama yavas), transaction destegi sinirli, data consistency riski (denormalization). Kullanim: Log/event storage, content management, prototipleme. Production'da "MongoDB ile baslayip PostgreSQL'e gecen" cok takım gorduk.
- **Senior karar agaci**: "Verin iliskisel mi? PostgreSQL. Document-oriented ve olceklenmesi mi lazim? MongoDB. Legacy veya WordPress? MySQL. Emin degilsen? PostgreSQL — yanlış gitmez."

**Anti-pattern Farkindaligi:**
- **N+1 sorgu problemi**: 100 kullanicinin siparislerini cekerken 1 (users) + 100 (orders per user) = 101 sorgu. Production'da gorduk: sayfa yukleme 8 saniye suruyordu. JOIN veya ORM'de eager loading ile tek sorguya dusuruldu, 200ms'ye indi.
- **Index olmadan production'a cikmak**: 10K satırda sorun yok, 1M satırda her sorgu 5+ saniye. "Sonra ekleriz" dersen kullanicilar sikayete basladığinda acil index eklemek zorunda kalirsin — ve `CREATE INDEX` buyuk tablolarda tablo lock'lar (CONCURRENTLY kullan!).
- **Over-normalization**: Her sey 6NF'e kadar normalize. 10 tablo join eden sorgular, okunmasi ve bakimi imkansiz. Bazen kasitli denormalization performans icin gereklidir — ozellikle okuma agirlikli sistemlerde. Materialized view ile denormalize veriyi otomatik guncel tut.

**Gercek Dunya Deneyimi:** Bir e-ticaret projesinde urun arama sayfasi 4 saniyede yukleniyordu. EXPLAIN ANALYZE calistirdim: `orders` tablosunda 5M satir, `WHERE status = 'active'` filtresi var ama index yok, Seq Scan yapıyor. `CREATE INDEX CONCURRENTLY idx_orders_status ON orders (status) WHERE status = 'active'` ile partial index ekledim. Sorgu 4 saniyeden 3ms'ye dustu. Partial index sayesinde sadece aktif siparisler indekslendi, index boyutu %90 kucuk kaldi.

**Profesyonel Mindset:** "Veritabanı, uygulamanın temelidir. Application kodu değişir, framework'ler değişir ama veri kalır. İyi tasarlanmış bir schema ve optimize edilmiş sorgular, uygulamanın ölçeklenebilirliğini belirler. Her sorguyu EXPLAIN ANALYZE ile test et, her tablo tasarımını normalization kurallarıyla doğrula, her production değişikliğini migration ile versiyon kontrolünde tut."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Query** (kweer-ee) → Sorgu
   *"This SQL query retrieves all active users from the database."*

2. **Index** (in-deks) → İndeks / Dizin
   *"Adding a B-tree index on the email column improved query performance by 100x."*

3. **Transaction** (tran-zak-shun) → İşlem Birimi
   *"We wrapped the bank transfer in a transaction to ensure atomicity."*

4. **Normalization** (nor-muh-li-zey-shun) → Normalleştirme
   *"The database schema was normalized to third normal form to eliminate data redundancy."*

5. **Join** (joyn) → Birleştirme
   *"Use a LEFT JOIN when you need all records from the left table regardless of matches."*

**Okuma Egzersizi:** PostgreSQL resmi dökümanında "Queries" bölümünü İngilizce oku: https://www.postgresql.org/docs/current/queries.html

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "Ürünler tablosuna kategori index'i ekledim"
→ Örnek: `perf: add B-tree index on products category column`
:::

:::external-resource
- 📺 **freeCodeCamp:** "SQL Tutorial - Full Database Course for Beginners" (4 saat, YouTube, ücretsiz)
- 📖 **PostgreSQL Docs:** "Tutorial" bölümü (resmi, ücretsiz)
- 🎮 **SQLZoo:** sqlzoo.net (interaktif SQL egzersizleri, ücretsiz)
- 🎮 **LeetCode Database:** leetcode.com/problemset/database (SQL mülakat soruları)
- 📖 **Use The Index, Luke:** use-the-index-luke.com (indexing rehberi, ücretsiz)
:::
