---
title: "Python ML: NumPy, Pandas, Scikit-learn"
id: mod-15-ml-math/lesson-02
estimated_minutes: 95
order: 2
tags: [numpy, pandas, scikit-learn, data-preprocessing, feature-engineering, model-evaluation, classification, regression, clustering]
prerequisites: [mod-15-ml-math/lesson-01]
---

# Python ML: NumPy, Pandas, Scikit-learn

Matematik temelini öğrendin. Şimdi Python'un ML ekosistemindeki **üç silahı** kullanarak gerçek dünya problemlerini çözeceğiz: NumPy ile hızlı hesaplama, Pandas ile veri manipülasyonu, Scikit-learn ile model eğitimi. Bu ders bittiğinde end-to-end bir ML pipeline kurabileceksin.

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Scikit-learn pipeline'inda veri on işleme adimlari (StandardScaler, OneHotEncoder, SimpleImputer) neden önemlidir? Feature scaling yapmazsan model performansı neden duser? Train-test split'te data leakage nedir ve pipeline ile nasil onlenir?"

**2. Pratik Uygulama:**
> "Pandas ile bir Kaggle dataset'ini yükle, EDA (Exploratory Data Analysis) yap, missing value'lari doldur, feature engineering uygula, scikit-learn ile 3 farklı model (LogisticRegression, RandomForest, XGBoost) egit ve cross-validation ile performanslarini karşılaştır. Classification report ve confusion matrix ile sonuçları yorumla."
> Takip: "En iyi modelin hyperparameter'larini GridSearchCV ile optimize et ve overfitting/underfitting durumunu learning curve ile analiz et."

**3. Mukemmellik Için:**
> "Production'a deploy edilecek bir ML modeli için tam pipeline tasarla: veri toplama, feature store, model training (MLflow ile experiment tracking), model evaluation (A/B testing), model serving (FastAPI ile API), monitoring (data drift, model drift) ve retraining stratejisi."

### Pair Programming Ipucu
ML kodu yazarken AI'a model performans metriklerini göster ve sor: "Bu confusion matrix'i yorumla. Precision mu recall mi daha önemli bu use case'de? F1-score neden düşük? Feature importance'a bakarak hangi feature'lari cikarmali veya eklemeliyim?"
:::

:::interview
## Mülakat Sorulari

**Soru 1: Overfitting nedir ve nasil onlenir?**
- **Junior cevabi:** Overfitting modelin egitim verisini ezberlemesidir, daha fazla veri veya regularization ile onlenir.
- **Senior cevabi:** Overfitting, modelin training set'teki noise'u ogrenip generalize edememesidir. Tespiti: training accuracy yüksek ama validation accuracy düşük. Onleme yöntemleri: 1) Daha fazla veri (data augmentation dahil), 2) Regularization (L1/Lasso sparse model, L2/Ridge küçük weight'ler), 3) Cross-validation (k-fold ile gerçekçi performans tahmini), 4) Early stopping (validation loss artmaya basladiginda dur), 5) Dropout (neural network'lerde), 6) Feature selection (gereksiz feature'lari çıkar), 7) Ensemble methods (bagging variance'i azaltır). Bias-variance tradeoff: basit model = high bias (underfitting), karmaşık model = high variance (overfitting). Sweet spot learning curve analizi ile bulunur.

**Soru 2: Feature engineering nedir ve model performansini nasil etkiler?**
- **Junior cevabi:** Mevcut veriden yeni özellikler olusturmaktir.
- **Senior cevabi:** Feature engineering, domain knowledge kullanarak raw data'dan anlamli özellikler cikarmadir ve model performansini %20-50 artirabilir. Teknikler: one-hot encoding (kategorik veriler), scaling (StandardScaler, MinMaxScaler), polynomial features (non-linear iliskiler), datetime decomposition (yil/ay/gun/saat), text vectorization (TF-IDF, word embeddings), interaction features (A*B). Feature selection: correlation analysis, mutual information, recursive feature elimination. Data leakage riski: test verisinden bilgi sizmasi, örneğin target encoding'de fold-based yapilmazsa leakage olur. Pipeline ile preprocessing + model birlestirilir ve leakage onlenir.
:::

:::must-note
## Defterine Yaz!
1. **NumPy broadcasting**: Shape'ler uyumlu olmalı. (3,4) + (1,4) = OK, (3,4) + (3,) = HATA. Vectorized işlem for loop'tan 100x hızlı.
2. **Pandas**: df.isna().sum() ile missing value bul, df.describe() ile genel bakış al, df.groupby() ile aggregation yap.
3. **Scikit-learn pipeline**: train_test_split --> preprocessing (StandardScaler) --> model.fit(X_train) --> model.predict(X_test) --> evaluation
4. **Cross-validation**: Tek split güvenilir değil. 5-fold CV ile ortalama skor al. GridSearchCV ile hyperparameter tune et.
5. **Evaluation metrikleri**: Imbalanced data'da accuracy YANILTICI. Precision (FP önemli), Recall (FN önemli), F1 (dengeli), ROC-AUC (threshold-bağımsız) kullan.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir
Senior bir ML engineer bu araçları şöyle kullanır:
- **Memory management**: Pandas'ta dtype optimize eder (int64 -> int32), chunk'larla büyük CSV okur
- **Profiling**: Pandas Profiling veya ydata-profiling ile EDA otomatikleştirir
- **Pipeline**: Scikit-learn Pipeline + ColumnTransformer ile production-ready preprocessing yapar
- **Feature store**: Feature engineering'i tekrar kullanılabilir hale getirir (Feast, Feature Store)
- **Experiment tracking**: MLflow ile her deneyin hyperparameter, metric ve artifact'ini saklar
- **Data validation**: Great Expectations veya Pandera ile data quality kontrol eder
:::

---

## 1. NumPy -- ML'in Hesaplama Motoru

NumPy, Python'da **yüksek performanslı sayısal hesaplama** kütüphanesidir. ML'de her şey NumPy array'leri üzerine kurulu.

### 1.1 Array Temelleri

```python
import numpy as np

# Array oluşturma yöntemleri
a = np.array([1, 2, 3, 4, 5])              # 1D array
b = np.array([[1, 2, 3], [4, 5, 6]])       # 2D array (matrix)
c = np.zeros((3, 4))                        # 3x4 sıfır matrisi
d = np.ones((2, 3))                         # 2x3 birler matrisi
e = np.random.randn(3, 3)                   # 3x3 normal dağılım
f = np.arange(0, 10, 0.5)                   # 0'dan 10'a 0.5 adımla
g = np.linspace(0, 1, 100)                  # 0-1 arası 100 eşit nokta
h = np.eye(4)                               # 4x4 birim matris

# Temel özellikler
print(f"Shape: {b.shape}")    # (2, 3)
print(f"Dtype: {b.dtype}")    # int64
print(f"Ndim:  {b.ndim}")     # 2
print(f"Size:  {b.size}")     # 6

# Reshape -- boyut değiştirme
x = np.arange(12)
print(f"Original: {x.shape}")           # (12,)
print(f"Reshaped: {x.reshape(3, 4).shape}")  # (3, 4)
print(f"Auto:     {x.reshape(3, -1).shape}") # (3, 4) -- -1 otomatik hesaplar
print(f"Flatten:  {x.reshape(3, 4).ravel().shape}")  # (12,)
```

### 1.2 Vectorized Operations ve Broadcasting

:::concept
## Vectorized Operations Neden Önemli?

Python for loop'u **yavaş**. NumPy, C ile yazılmış optimized kod kullanarak **vectorized** işlem yapar.

```python
# YAVAŞ (Python loop)
result = []
for i in range(1000000):
    result.append(a[i] * b[i])

# HIZLI (NumPy vectorized) -- 100x+ hızlı
result = a * b
```

**Broadcasting**: Farklı shape'teki array'ler otomatik genişletilir.
- (3, 4) + (1, 4) = (3, 4) -- satır kopyalanır
- (3, 4) + (3, 1) = (3, 4) -- sütun kopyalanır
- (3, 4) + (4,) = (3, 4) -- 1D array satır olarak yayılır
:::

```python
import numpy as np
import time

# Performans karşılaştırması
n = 1_000_000
a = np.random.randn(n)
b = np.random.randn(n)

# Python loop
start = time.time()
result_loop = [a[i] * b[i] for i in range(n)]
loop_time = time.time() - start

# NumPy vectorized
start = time.time()
result_np = a * b
np_time = time.time() - start

print(f"Python loop: {loop_time:.4f}s")
print(f"NumPy:       {np_time:.6f}s")
print(f"Speedup:     {loop_time/np_time:.0f}x")

# Broadcasting örneği
# Her sample'ın feature'larını normalize et
X = np.random.randn(1000, 5) * 10 + 50  # 1000 sample, 5 feature
mean = X.mean(axis=0)   # Her feature'ın ortalaması (5,)
std = X.std(axis=0)     # Her feature'ın std'si (5,)

# Broadcasting: (1000, 5) - (5,) = (1000, 5)
X_normalized = (X - mean) / std  # Z-score normalization
print(f"\nNormalized mean: {X_normalized.mean(axis=0)}")  # ~[0,0,0,0,0]
print(f"Normalized std:  {X_normalized.std(axis=0)}")     # ~[1,1,1,1,1]
```

### 1.3 İleri NumPy İşlemleri

```python
import numpy as np

# Indexing ve slicing
X = np.random.randn(5, 4)

# Fancy indexing
print(X[[0, 2, 4]])          # 0, 2, 4. satırlar
print(X[:, [1, 3]])          # 1, 3. sütunlar

# Boolean indexing (filtering)
mask = X[:, 0] > 0           # İlk sütunu pozitif olanlar
print(X[mask])

# np.where -- koşullu değer atama
labels = np.where(X[:, 0] > 0, "positive", "negative")
print(labels)

# Concatenation
A = np.random.randn(3, 4)
B = np.random.randn(3, 4)
vertical = np.vstack([A, B])    # (6, 4)
horizontal = np.hstack([A, B])  # (3, 8)

# Aggregation
print(f"Sum (all):    {X.sum():.4f}")
print(f"Sum (rows):   {X.sum(axis=1)}")     # Her satırın toplamı
print(f"Sum (cols):   {X.sum(axis=0)}")     # Her sütunun toplamı
print(f"Argmax:       {X.argmax(axis=1)}")  # Her satırda max'ın index'i

# Matrix işlemleri (ML'de sık kullanılan)
A = np.random.randn(3, 3)
print(f"Determinant: {np.linalg.det(A):.4f}")
print(f"Rank: {np.linalg.matrix_rank(A)}")

# Softmax (classification'da kullanılır)
def softmax(x):
    exp_x = np.exp(x - np.max(x))  # numerical stability
    return exp_x / exp_x.sum()

logits = np.array([2.0, 1.0, 0.5])
probs = softmax(logits)
print(f"Softmax: {probs}")   # [0.59, 0.24, 0.16] -- toplam = 1
```

:::beginner-mistake
## NumPy Sık Hatalar

**Hata 1**: Copy vs View
```python
a = np.array([1, 2, 3])
b = a       # VIEW! b değişirse a da değişir
c = a.copy()  # COPY! bağımsız
b[0] = 99
print(a)  # [99, 2, 3] -- a da değişti!
```

**Hata 2**: Shape mismatch
```python
X = np.random.randn(100, 5)
w = np.random.randn(4)  # 5 olmalı!
# X @ w --> ValueError!
```

**Hata 3**: Integer division
```python
a = np.array([1, 2, 3])
print(a / 2)    # [0.5, 1.0, 1.5] -- float
print(a // 2)   # [0, 1, 1] -- integer division
```
:::

---

## 2. Pandas -- Veri Manipülasyonu

Pandas, **tabular veri** (CSV, Excel, SQL) ile çalışmak için standart araçtır.

### 2.1 DataFrame Temelleri

```python
import pandas as pd
import numpy as np

# DataFrame oluşturma
df = pd.DataFrame({
    'isim': ['Ali', 'Ayşe', 'Mehmet', 'Zeynep', 'Can'],
    'yas': [25, 30, 35, 28, 42],
    'maas': [50000, 75000, 90000, 65000, 110000],
    'departman': ['IT', 'HR', 'IT', 'Marketing', 'IT'],
    'deneyim_yil': [2, 5, 10, 3, 15]
})

print(df.head())
print(f"\nShape: {df.shape}")
print(f"\nInfo:")
print(df.info())
print(f"\nDescribe:")
print(df.describe())

# CSV okuma/yazma
# df = pd.read_csv('data.csv')
# df.to_csv('output.csv', index=False)

# Sütun erişimi
print(df['maas'])          # Series
print(df[['isim', 'maas']]) # DataFrame

# Filtering
it_workers = df[df['departman'] == 'IT']
high_salary = df[df['maas'] > 70000]
combined = df[(df['departman'] == 'IT') & (df['maas'] > 60000)]
print(f"\nIT çalışanları:\n{it_workers}")
```

### 2.2 Data Cleaning (Veri Temizleme)

:::concept
## Gerçek Veri Kirlidir!

Production'daki verinin %80'i temizleme gerektirir:
- **Missing values** (NaN): Sensör arızası, kullanıcı boş bıraktı
- **Duplicates**: Aynı kayıt birden fazla girmiş
- **Outliers**: Yaş = 250, maaş = -5000
- **Inconsistent formats**: "istanbul", "İstanbul", "ISTANBUL"
- **Wrong types**: Tarih string olarak, sayı text olarak

Kural: **Garbage in, garbage out** -- Kirli veri, kötü model.
:::

```python
import pandas as pd
import numpy as np

# Kirli veri oluştur
df = pd.DataFrame({
    'isim': ['Ali', 'Ayşe', 'Mehmet', None, 'Can', 'Ali'],
    'yas': [25, 30, 350, 28, None, 25],
    'maas': [50000, None, 90000, 65000, 110000, 50000],
    'sehir': ['istanbul', 'İstanbul', 'ANKARA', 'ankara', 'izmir', 'istanbul'],
    'tarih': ['2024-01-15', '15/01/2024', '2024-01-20', None, '2024-02-01', '2024-01-15']
})

print("Kirli veri:")
print(df)

# 1. Missing values kontrol
print(f"\nMissing values:\n{df.isna().sum()}")
print(f"Missing %:\n{(df.isna().sum() / len(df) * 100).round(2)}")

# 2. Missing value stratejileri
df['maas'].fillna(df['maas'].median(), inplace=True)  # Median ile doldur
df['isim'].fillna('Bilinmiyor', inplace=True)          # Sabit değer
df.dropna(subset=['yas'], inplace=True)                 # Satırı sil

# 3. Outlier tespiti ve temizleme
def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return (series < lower) | (series > upper)

outliers = detect_outliers_iqr(df['yas'])
print(f"\nOutlier yaşlar: {df.loc[outliers, 'yas'].values}")
df.loc[outliers, 'yas'] = df['yas'].median()  # Median ile değiştir

# 4. Tutarsız format düzeltme
df['sehir'] = df['sehir'].str.lower().str.strip()

# 5. Duplicate temizleme
print(f"\nDuplicate sayısı: {df.duplicated().sum()}")
df.drop_duplicates(inplace=True)

# 6. Type dönüşümü
df['tarih'] = pd.to_datetime(df['tarih'], format='mixed', errors='coerce')

print(f"\nTemiz veri:")
print(df)
print(f"\nDtype'lar:\n{df.dtypes}")
```

### 2.3 Feature Engineering

:::concept
## Feature Engineering -- ML'in %80'i

**İyi feature'lar kötü modeli yener, kötü feature'lar iyi modeli yenmez.**

Feature engineering teknikleri:
1. **Encoding**: Kategorik --> Sayısal (One-hot, Label, Target encoding)
2. **Scaling**: Farklı ölçekleri normalize etme (StandardScaler, MinMaxScaler)
3. **Binning**: Sürekli değişkeni kategorik yapma (yaş --> genç/orta/yaşlı)
4. **Interaction**: Feature'lar arası etkileşim (alan = boy * en)
5. **Time features**: Tarihten gün, ay, hafta sonu, tatil çıkarma
6. **Text features**: Kelime sayısı, ortalama kelime uzunluğu, TF-IDF
7. **Aggregation**: Grup bazlı istatistikler (müşterinin ortalama harcaması)
:::

```python
import pandas as pd
import numpy as np

# Örnek e-ticaret verisi
df = pd.DataFrame({
    'user_id': [1, 1, 1, 2, 2, 3, 3, 3, 3, 4],
    'product_category': ['Electronics', 'Books', 'Electronics', 'Clothing',
                         'Books', 'Electronics', 'Clothing', 'Books', 'Electronics', 'Books'],
    'price': [299.99, 15.99, 49.99, 89.99, 25.99, 599.99, 45.99, 12.99, 199.99, 9.99],
    'purchase_date': pd.date_range('2024-01-01', periods=10, freq='3D'),
    'rating': [4.5, 3.0, 4.0, 5.0, 2.5, 4.0, 3.5, 4.5, 5.0, 1.0],
    'review_text': ['Great product!', 'OK', 'Good quality, fast delivery',
                    'Love it!', 'Not bad', 'Amazing performance!',
                    'Fits well', 'Nice book', 'Best purchase ever!', 'Terrible']
})

print("Original data:")
print(df.head())

# 1. One-Hot Encoding
category_dummies = pd.get_dummies(df['product_category'], prefix='cat')
print(f"\nOne-hot encoding:\n{category_dummies.head()}")

# 2. Time features
df['day_of_week'] = df['purchase_date'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['month'] = df['purchase_date'].dt.month

# 3. Text features
df['review_length'] = df['review_text'].str.len()
df['review_word_count'] = df['review_text'].str.split().str.len()
df['has_exclamation'] = df['review_text'].str.contains('!').astype(int)

# 4. Aggregation features (user bazlı)
user_stats = df.groupby('user_id').agg(
    total_spend=('price', 'sum'),
    avg_spend=('price', 'mean'),
    purchase_count=('price', 'count'),
    avg_rating=('rating', 'mean'),
    category_diversity=('product_category', 'nunique')
).reset_index()

print(f"\nUser statistics:\n{user_stats}")

# 5. Binning
df['price_tier'] = pd.cut(df['price'],
                           bins=[0, 20, 100, 500, float('inf')],
                           labels=['budget', 'mid', 'premium', 'luxury'])

# 6. Log transform (skewed distribution düzeltme)
df['log_price'] = np.log1p(df['price'])  # log(1 + x) sıfır için güvenli

print(f"\nEnriched features:")
print(df[['price', 'price_tier', 'log_price', 'review_length',
          'review_word_count', 'day_of_week', 'is_weekend']].head())
```

### 2.4 Groupby ve Aggregation

```python
import pandas as pd
import numpy as np

# Satış verisi
np.random.seed(42)
df = pd.DataFrame({
    'sehir': np.random.choice(['Istanbul', 'Ankara', 'Izmir'], 1000),
    'kategori': np.random.choice(['Elektronik', 'Giyim', 'Gida'], 1000),
    'satis': np.random.exponential(200, 1000).round(2),
    'adet': np.random.randint(1, 10, 1000),
    'tarih': pd.date_range('2024-01-01', periods=1000, freq='8H')
})

# Temel groupby
sehir_stats = df.groupby('sehir')['satis'].agg(['mean', 'sum', 'count', 'std'])
print(f"Şehir bazlı satış:\n{sehir_stats}\n")

# Multi-level groupby
cross = df.groupby(['sehir', 'kategori'])['satis'].mean().unstack()
print(f"Şehir x Kategori:\n{cross}\n")

# Pivot table
pivot = pd.pivot_table(df, values='satis', index='sehir',
                        columns='kategori', aggfunc=['mean', 'sum'])
print(f"Pivot table:\n{pivot}\n")

# Time-based aggregation
df['ay'] = df['tarih'].dt.to_period('M')
monthly = df.groupby('ay')['satis'].sum()
print(f"Aylık satış:\n{monthly}")
```

---

## 3. Scikit-learn -- ML Pipeline

Scikit-learn, Python'un **standart ML kütüphanesi**. Consistent API'si ile classification, regression, clustering ve preprocessing yapabilirsin.

### 3.1 Temel Workflow

:::concept
## Scikit-learn API Felsefesi

Her model aynı pattern'ı takip eder:

```python
from sklearn.some_module import SomeModel

model = SomeModel(hyperparameters)   # 1. Oluştur
model.fit(X_train, y_train)          # 2. Eğit
predictions = model.predict(X_test)   # 3. Tahmin
score = model.score(X_test, y_test)   # 4. Değerlendir
```

Bu consistency sayesinde model değiştirmek **tek satır** sürer!
:::

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Veri oluştur (veya gerçek veri yükle)
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=5,
    n_redundant=2,
    random_state=42
)

print(f"Dataset: X={X.shape}, y={y.shape}")
print(f"Class distribution: {np.bincount(y)}")

# 1. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,        # %20 test
    random_state=42,       # Tekrar edilebilirlik
    stratify=y             # Sınıf oranlarını koru
)

print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# 2. Preprocessing (Feature Scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform
X_test_scaled = scaler.transform(X_test)          # SADECE transform!

# 3. Model Training
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_scaled, y_train)

# 4. Prediction
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)  # Olasılıklar

# 5. Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
```

:::warning
## Data Leakage -- En Tehlikeli Hata!

**Data leakage**: Test verisinin bilgisinin training'e sızması.

```python
# YANLIŞ -- test verisi de fit'e dahil oluyor!
scaler.fit(X)  # Tüm veri ile fit
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# DOĞRU -- sadece training verisi ile fit
scaler.fit(X_train)  # Sadece train ile fit
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Train'in mean/std'si ile transform
```

**Sonuç**: Leakage varsa model gerçekte olduğundan iyi görünür. Production'da başarısız olur.
:::

### 3.2 Preprocessing Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np

# Karma veri (sayısal + kategorik)
df = pd.DataFrame({
    'yas': [25, 30, None, 28, 42, 35, None, 50],
    'maas': [50000, 75000, 90000, None, 110000, 80000, 60000, 95000],
    'deneyim': [2, 5, 10, 3, 15, 8, 4, 12],
    'departman': ['IT', 'HR', 'IT', 'Marketing', 'IT', 'HR', None, 'Marketing'],
    'egitim': ['lisans', 'yukseklisans', 'doktora', 'lisans',
               'yukseklisans', 'lisans', 'lisans', 'doktora'],
    'terfi': [0, 1, 1, 0, 1, 1, 0, 1]  # Target
})

X = df.drop('terfi', axis=1)
y = df['terfi']

# Sütun tipleri
numeric_features = ['yas', 'maas', 'deneyim']
categorical_features = ['departman', 'egitim']

# Sayısal pipeline: missing -> scale
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Kategorik pipeline: missing -> encode
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Birleştir
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Tam pipeline (preprocessing + model)
from sklearn.linear_model import LogisticRegression

full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(random_state=42))
])

# Tek satırda fit!
full_pipeline.fit(X, y)
predictions = full_pipeline.predict(X)
print(f"Pipeline predictions: {predictions}")
print(f"Pipeline accuracy: {full_pipeline.score(X, y):.4f}")
```

### 3.3 Classification Algoritmaları

:::comparison
## Classification Algoritmaları Karşılaştırması

| Algoritma | Avantaj | Dezavantaj | Ne Zaman? |
|-----------|---------|------------|-----------|
| **Logistic Regression** | Hızlı, yorumlanabilir, baseline | Non-linear ilişkileri yakalar zor | İlk deneme, linear veri |
| **Decision Tree** | Yorumlanabilir, feature importance | Overfitting'e eğilimli | Explainability gerektiğinde |
| **Random Forest** | Overfit etmez, robust | Yavaş (çok ağaç), black box | Çoğu durumda iyi performans |
| **Gradient Boosting** | En yüksek accuracy | Overfit riski, tune etmek zor | Yarışma/production (XGBoost) |
| **SVM** | Yüksek boyutlarda iyi | Yavaş (büyük veri), tune gerekir | Text classification |
| **KNN** | Basit, non-parametrik | Yavaş (inference), curse of dim. | Küçük veri, baseline |
:::

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Veri
X, y = make_classification(n_samples=2000, n_features=20,
                           n_informative=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tüm modelleri dene
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(max_depth=10),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf'),
    'KNN': KNeighborsClassifier(n_neighbors=5)
}

print("Model Karşılaştırması:")
print(f"{'Model':<25} {'Train Acc':<12} {'Test Acc':<12} {'CV Mean':<12}")
print("-" * 61)

for name, model in models.items():
    model.fit(X_train, y_train)
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"{name:<25} {train_acc:<12.4f} {test_acc:<12.4f} {cv_scores.mean():<12.4f}")
```

### 3.4 Regression Algoritmaları

```python
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# Veri
X, y = make_regression(n_samples=1000, n_features=10,
                        n_informative=5, noise=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Linear Regression': LinearRegression(),
    'Ridge (L2)': Ridge(alpha=1.0),
    'Lasso (L1)': Lasso(alpha=1.0),
    'Elastic Net': ElasticNet(alpha=1.0, l1_ratio=0.5),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

print("Regression Model Karşılaştırması:")
print(f"{'Model':<25} {'RMSE':<12} {'MAE':<12} {'R2':<12}")
print("-" * 61)

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"{name:<25} {rmse:<12.4f} {mae:<12.4f} {r2:<12.4f}")

# Feature importance (Tree-based modeller)
rf = models['Random Forest']
importances = rf.feature_importances_
for i, imp in enumerate(importances):
    bar = "█" * int(imp * 50)
    print(f"  Feature {i}: {imp:.4f} {bar}")
```

### 3.5 Clustering

```python
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score
import numpy as np

# Veri
X, y_true = make_blobs(n_samples=500, n_features=2,
                         centers=4, cluster_std=1.0, random_state=42)

# K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels_kmeans = kmeans.fit_predict(X)
sil_kmeans = silhouette_score(X, labels_kmeans)
print(f"K-Means silhouette: {sil_kmeans:.4f}")
print(f"K-Means inertia:    {kmeans.inertia_:.4f}")
print(f"Cluster centers:\n{kmeans.cluster_centers_}")

# Elbow method -- optimal k bulma
inertias = []
sil_scores = []
K_range = range(2, 10)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X, km.labels_))

print(f"\nElbow Method:")
for k, inertia, sil in zip(K_range, inertias, sil_scores):
    bar = "█" * int(sil * 40)
    print(f"  k={k}: inertia={inertia:.0f}, silhouette={sil:.4f} {bar}")

# DBSCAN (density-based -- k belirtmeye gerek yok)
dbscan = DBSCAN(eps=1.0, min_samples=5)
labels_dbscan = dbscan.fit_predict(X)
n_clusters = len(set(labels_dbscan)) - (1 if -1 in labels_dbscan else 0)
n_noise = (labels_dbscan == -1).sum()
print(f"\nDBSCAN: {n_clusters} cluster, {n_noise} noise points")
```

### 3.6 Cross-Validation ve Hyperparameter Tuning

:::concept
## Cross-Validation Neden Gerekli?

Tek train/test split güvenilir değil. Veri farklı bölünse farklı sonuç çıkar.

**K-Fold Cross-Validation**:
1. Veriyi K parçaya böl
2. Her seferinde 1 parça test, geri kalan K-1 training
3. K farklı skor al, ortalamasını hesapla

**Sonuç**: Model performansının daha güvenilir tahmini.

**GridSearchCV**: Tüm hyperparameter kombinasyonlarını dene + CV ile değerlendir.
**RandomizedSearchCV**: Rastgele örnekleme -- daha hızlı ama tüm kombinasyonları denemez.
:::

```python
from sklearn.model_selection import (
    cross_val_score, GridSearchCV, RandomizedSearchCV,
    StratifiedKFold
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=1000, n_features=20,
                           n_informative=10, random_state=42)

# 1. Basit Cross-Validation
rf = RandomForestClassifier(n_estimators=100, random_state=42)
cv_scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
print(f"CV Scores: {cv_scores}")
print(f"Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# 2. Stratified K-Fold (imbalanced data için)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(rf, X, y, cv=skf, scoring='f1')
print(f"\nStratified CV F1: {scores.mean():.4f} (+/- {scores.std():.4f})")

# 3. GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,      # Tüm CPU'ları kullan
    verbose=1
)

grid_search.fit(X, y)

print(f"\nEn iyi parametreler: {grid_search.best_params_}")
print(f"En iyi skor: {grid_search.best_score_:.4f}")

# 4. RandomizedSearchCV (daha hızlı)
from scipy.stats import randint, uniform

param_distributions = {
    'n_estimators': randint(50, 300),
    'max_depth': randint(3, 30),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': uniform(0.1, 0.9)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions,
    n_iter=50,       # 50 rastgele kombinasyon dene
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X, y)
print(f"\nRandomized en iyi: {random_search.best_params_}")
print(f"Randomized en iyi skor: {random_search.best_score_:.4f}")
```

---

## 4. Model Evaluation -- Doğru Metriği Seç

### 4.1 Classification Metrics

:::concept
## Confusion Matrix ve Metrikler

```
                Predicted
                Pos    Neg
Actual  Pos     TP     FN
        Neg     FP     TN
```

- **Accuracy** = (TP + TN) / Total -- Genel doğruluk
- **Precision** = TP / (TP + FP) -- "Pozitif dediklerimin kaçı gerçekten pozitif?"
- **Recall (Sensitivity)** = TP / (TP + FN) -- "Gerçek pozitiflerin kaçını yakaladım?"
- **F1 Score** = 2 * (P * R) / (P + R) -- Precision-Recall dengesi
- **ROC-AUC** = Threshold'dan bağımsız performans

**Ne zaman hangisi?**
- **Spam filter**: Precision önemli (normal email'i spam yapma!)
- **Kanser tespiti**: Recall önemli (hiçbir hastayı kaçırma!)
- **Genel**: F1 Score (denge)
- **Model karşılaştırma**: ROC-AUC
:::

```python
from sklearn.metrics import (
    confusion_matrix, classification_report,
    precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve,
    precision_recall_curve, average_precision_score
)
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np

# Imbalanced veri oluştur
X, y = make_classification(n_samples=1000, n_features=20,
                           weights=[0.9, 0.1],  # %90 class 0, %10 class 1
                           random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                      stratify=y, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix:\n{cm}")
print(f"  TN={cm[0,0]}, FP={cm[0,1]}")
print(f"  FN={cm[1,0]}, TP={cm[1,1]}")

# Tüm metrikler
print(f"\nAccuracy:  {(y_pred == y_test).mean():.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1:        {f1_score(y_test, y_pred):.4f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}")

# Classification Report
print(f"\n{classification_report(y_test, y_pred)}")

# ROC Curve data
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
print(f"\nROC Curve thresholds (ilk 5): {thresholds[:5]}")
print(f"FPR: {fpr[:5]}")
print(f"TPR: {tpr[:5]}")
```

:::tip
## Threshold Ayarlama

Default threshold 0.5'tir ama her zaman optimal değildir.

```python
# Threshold'u 0.3'e düşürmek: daha çok pozitif tahmin, recall artar, precision düşer
# Threshold'u 0.7'ye çıkarmak: daha az pozitif tahmin, precision artar, recall düşer

best_f1 = 0
best_threshold = 0.5

for threshold in np.arange(0.1, 0.9, 0.05):
    y_pred_t = (y_prob >= threshold).astype(int)
    f1 = f1_score(y_test, y_pred_t)
    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold

print(f"Optimal threshold: {best_threshold:.2f} (F1: {best_f1:.4f})")
```
:::

### 4.2 Regression Metrics

```python
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error,
    r2_score, mean_absolute_percentage_error
)
import numpy as np

# Örnek tahminler
y_true = np.array([100, 200, 300, 400, 500])
y_pred = np.array([110, 190, 280, 420, 480])

# Metrikler
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
mape = mean_absolute_percentage_error(y_true, y_pred)

print(f"MSE:  {mse:.2f}")
print(f"RMSE: {rmse:.2f}")   # Aynı birimde (orijinal scale)
print(f"MAE:  {mae:.2f}")
print(f"R2:   {r2:.4f}")     # 1.0 = mükemmel, 0 = ortalama kadar
print(f"MAPE: {mape:.4f}")   # Yüzde cinsinden hata

# R2 Score yorumu
print(f"\nR2 = {r2:.4f}: Model, varyansın %{r2*100:.1f}'ini açıklıyor")
```

---

## 5. End-to-End ML Pipeline Projesi

```python
"""
Complete ML Pipeline: Kredi Onay Tahmini
Tüm adımları birleştiren gerçekçi bir örnek.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# ===== 1. VERİ OLUŞTURMA (gerçekte CSV'den okursun) =====
np.random.seed(42)
n = 2000

df = pd.DataFrame({
    'yas': np.random.normal(35, 10, n).astype(int).clip(18, 70),
    'gelir': np.random.exponential(50000, n).round(0),
    'kredi_skoru': np.random.normal(650, 80, n).astype(int).clip(300, 850),
    'borc_gelir_orani': np.random.uniform(0, 0.6, n).round(3),
    'calisma_yili': np.random.exponential(5, n).round(1).clip(0, 40),
    'ev_durumu': np.random.choice(['kira', 'ev_sahibi', 'aileyle'], n, p=[0.5, 0.35, 0.15]),
    'egitim': np.random.choice(['lise', 'lisans', 'yukseklisans'], n, p=[0.3, 0.5, 0.2]),
    'kredi_amaci': np.random.choice(['ev', 'arac', 'egitim', 'kisisel'], n)
})

# Target: kredi onayı (kurallara göre)
prob = (
    0.3 +
    0.2 * (df['kredi_skoru'] > 700).astype(float) +
    0.15 * (df['gelir'] > 60000).astype(float) +
    0.1 * (df['borc_gelir_orani'] < 0.3).astype(float) +
    0.1 * (df['calisma_yili'] > 3).astype(float) +
    np.random.normal(0, 0.1, n)
).clip(0, 1)

df['onay'] = (np.random.random(n) < prob).astype(int)

# Missing values ekle (gerçekçi)
for col in ['gelir', 'kredi_skoru', 'calisma_yili']:
    mask = np.random.random(n) < 0.05
    df.loc[mask, col] = np.nan

print("Dataset Genel Bakış:")
print(df.head())
print(f"\nShape: {df.shape}")
print(f"\nMissing:\n{df.isna().sum()}")
print(f"\nTarget distribution:\n{df['onay'].value_counts(normalize=True)}")

# ===== 2. FEATURE VE TARGET AYIRMA =====
X = df.drop('onay', axis=1)
y = df['onay']

# ===== 3. TRAIN/TEST SPLIT =====
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ===== 4. PREPROCESSING PIPELINE =====
numeric_features = ['yas', 'gelir', 'kredi_skoru', 'borc_gelir_orani', 'calisma_yili']
categorical_features = ['ev_durumu', 'egitim', 'kredi_amaci']

numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# ===== 5. MODEL KARŞILAŞTIRMA =====
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

print("\n===== Model Karşılaştırma (5-Fold CV) =====")
best_model_name = None
best_score = 0

for name, model in models.items():
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='roc_auc')
    mean_score = cv_scores.mean()
    print(f"{name:<25}: AUC = {mean_score:.4f} (+/- {cv_scores.std():.4f})")

    if mean_score > best_score:
        best_score = mean_score
        best_model_name = name

print(f"\nEn iyi model: {best_model_name} (AUC: {best_score:.4f})")

# ===== 6. HYPERPARAMETER TUNING =====
best_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(random_state=42))
])

param_grid = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [3, 5, 7],
    'classifier__learning_rate': [0.05, 0.1, 0.2]
}

grid_search = GridSearchCV(
    best_pipeline, param_grid,
    cv=5, scoring='roc_auc', n_jobs=-1
)

grid_search.fit(X_train, y_train)
print(f"\nGrid Search Best Params: {grid_search.best_params_}")
print(f"Grid Search Best AUC: {grid_search.best_score_:.4f}")

# ===== 7. FINAL EVALUATION =====
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
y_prob = best_model.predict_proba(X_test)[:, 1]

print(f"\n===== Final Test Sonuçları =====")
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
print(f"\n{classification_report(y_test, y_pred)}")
```

:::english
## Technical Terms Glossary

| English | Türkçe Açıklama |
|---------|-----------------|
| **Array** | Aynı tipte elemanlardan oluşan çok boyutlu veri yapısı |
| **Broadcasting** | Farklı boyutlu array'lerin otomatik genişletilmesi |
| **DataFrame** | Tablo formatında veri yapısı (satırlar ve sütunlar) |
| **Feature Engineering** | Ham veriden model için anlamlı özellikler çıkarma |
| **Preprocessing** | Model eğitimi öncesi veri hazırlama (temizleme, dönüştürme) |
| **One-Hot Encoding** | Kategorik değişkeni binary sütunlara dönüştürme |
| **StandardScaler** | Z-score normalization (mean=0, std=1) |
| **Train/Test Split** | Veriyi eğitim ve test setlerine bölme |
| **Cross-Validation** | K parçaya bölerek güvenilir performans tahmini |
| **Hyperparameter Tuning** | Model dışı parametreleri optimize etme |
| **Overfitting** | Eğitim verisine aşırı uyum, test'te kötü performans |
| **Data Leakage** | Test bilgisinin eğitime sızması (büyük hata!) |
| **Pipeline** | Preprocessing ve model adımlarını birleştiren yapı |
| **Confusion Matrix** | Tahmin vs gerçek değerlerin tablosu |
| **ROC-AUC** | Threshold'dan bağımsız classification performans metriği |
:::

:::knowledge-check
## Bilgi Kontrolü

1. `scaler.fit_transform(X_train)` ve `scaler.transform(X_test)` neden farklı kullanılır?
2. Accuracy %98 ama F1 %30 ise ne oluyor? Hangi durum buna neden olur?
3. Random Forest'ta `n_estimators` artırmak overfitting yapar mı?
4. One-hot encoding sütun sayısını nasıl etkiler? 100 kategorili bir sütunda ne olur?
5. Cross-validation ile train/test split arasındaki temel fark nedir?
:::

:::exercise
### Alistirma 1: EDA ve Veri Gorsellestirme (Kolay)

Scikit-learn'in California Housing dataset'ini yukle ve kesfedici veri analizi (EDA) yap.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing

# Veriyi yukle
data = fetch_california_housing(as_frame=True)
df = data.frame

# TODO: Temel istatistikleri incele
print(df.describe())
print(f"\nShape: {df.shape}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# TODO: Hedef degisken (MedHouseVal) dagilimi
# plt.hist(df["MedHouseVal"], bins=50)
# plt.xlabel("Medyan Ev Fiyati ($100K)")
# plt.ylabel("Frekans")
# plt.title("Ev Fiyati Dagilimi")
# plt.show()

# TODO: Korelasyon matrisi
# corr = df.corr()
# Hangi feature hedef degiskenle en yuksek korelasyona sahip?

# TODO: Scatter plot — MedInc (medyan gelir) vs MedHouseVal
# plt.scatter(df["MedInc"], df["MedHouseVal"], alpha=0.1)

# TODO: Feature dagilimlarini boxplot ile goruntule (outlier tespiti)
```

**Beklenen Sonuc:** Dataset 20640 satir, 8 feature icermeli. MedInc (medyan gelir) hedef degiskenle en yuksek korelasyona sahip olmali. Ev fiyatlarinda 5.0'da kesme (capping) gorulmeli.
**Ipucu:** `df.corr()["MedHouseVal"].sort_values(ascending=False)` ile korelasyonlari sirala.

---

### Alistirma 2: Preprocessing Pipeline ve Model Karsilastirma (Orta)

Scikit-learn Pipeline ile veri on-isleme ve 3 farkli modeli cross-validation ile karsilastir.

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Veriyi yukle
from sklearn.datasets import fetch_california_housing
data = fetch_california_housing()
X, y = data.data, data.target

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TODO: Feature engineering — yeni feature'lar ekle
# rooms_per_household = X[:, 3] / X[:, 5]  # AveRooms / Population
# bedrooms_ratio = X[:, 4] / X[:, 3]  # AveBedrms / AveRooms

# TODO: Pipeline'lar olustur
models = {
    "Linear Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression()),
    ]),
    "Ridge": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0)),
    ]),
    "Random Forest": Pipeline([
        # Scaler gerekli mi? (Tree modelleri icin genelde gerekli degil)
        ("model", RandomForestRegressor(n_estimators=100, random_state=42)),
    ]),
}

# TODO: 5-fold cross validation ile karsilastir
for name, pipeline in models.items():
    scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="r2")
    print(f"{name:25s} | R2: {scores.mean():.4f} (+/- {scores.std():.4f})")

# TODO: En iyi modeli sec, test set'te degerlendir
# best_model.fit(X_train, y_train)
# y_pred = best_model.predict(X_test)
# print(f"Test RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
# print(f"Test R2: {r2_score(y_test, y_pred):.4f}")
```

**Beklenen Sonuc:** Random Forest veya Gradient Boosting en iyi R2 skoruna sahip olmali. Linear Regression en dusuk performansi gostermeli. Test R2 skoru 0.80+ olmali.
**Ipucu:** `cross_val_score` ile overfitting kontrolu yap. Train ve test skorlari arasinda buyuk fark varsa overfitting var demektir.

---

### Alistirma 3: Hyperparameter Tuning ve Model Kaydetme (Zor)

GridSearchCV ile en iyi hyperparameter'lari bul, feature importance analizi yap ve modeli kaydet.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

# TODO: GradientBoosting icin hyperparameter grid
param_grid = {
    "model__n_estimators": [100, 200, 500],
    "model__max_depth": [3, 5, 7],
    "model__learning_rate": [0.01, 0.1, 0.2],
    "model__min_samples_split": [2, 5, 10],
}

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", GradientBoostingRegressor(random_state=42)),
])

# TODO: GridSearchCV ile en iyi parametreleri bul
grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1,  # Tum CPU core'lari kullan
    verbose=1,
)
# grid_search.fit(X_train, y_train)
# print(f"En iyi parametreler: {grid_search.best_params_}")
# print(f"En iyi CV R2: {grid_search.best_score_:.4f}")

# TODO: Feature importance grafigi ciz
# best_model = grid_search.best_estimator_.named_steps["model"]
# importances = best_model.feature_importances_
# feature_names = data.feature_names
# sorted_idx = np.argsort(importances)[::-1]
#
# plt.barh(range(len(importances)), importances[sorted_idx])
# plt.yticks(range(len(importances)), [feature_names[i] for i in sorted_idx])
# plt.xlabel("Feature Importance")
# plt.title("GradientBoosting Feature Importances")
# plt.tight_layout()
# plt.show()

# TODO: Modeli kaydet ve yukle
# joblib.dump(grid_search.best_estimator_, "best_model.pkl")
# loaded_model = joblib.load("best_model.pkl")
# new_prediction = loaded_model.predict(X_test[:5])
# print(f"Tahminler: {new_prediction}")
```

**Beklenen Sonuc:** GridSearchCV ile en iyi hyperparameter kombinasyonu bulunmali. MedInc (medyan gelir) en onemli feature olmali. Model joblib ile kaydedilip yeniden yuklenebilmeli. Yeni veri ile tahmin yapilabilmeli.
**Ipucu:** `n_jobs=-1` tum CPU core'lari kullanir (GridSearch hizlanir). `verbose=1` ilerleme durumunu gosterir. Buyuk grid'lerde `RandomizedSearchCV` daha hizlidir.
:::

:::external-resource
## Ek Kaynaklar

- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) -- Resmi dökümantasyon
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf) -- Hızlı referans
- [NumPy for MATLAB Users](https://numpy.org/doc/stable/user/numpy-for-matlab-users.html) -- Geçiş rehberi
- [Kaggle Learn](https://www.kaggle.com/learn) -- Ücretsiz interaktif dersler
- [Feature Engineering Book](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/) -- Kapsamlı kitap
:::
