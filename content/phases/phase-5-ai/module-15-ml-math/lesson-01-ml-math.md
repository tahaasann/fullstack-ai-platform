---
title: "AI/ML Matematik Temelleri"
id: mod-15-ml-math/lesson-01
estimated_minutes: 90
order: 1
tags: [linear-algebra, calculus, probability, statistics, optimization, gradient-descent, machine-learning-math]
prerequisites: [mod-14-ai-fundamentals/lesson-01]
---

# AI/ML Matematik Temelleri

Machine Learning'in arkasındaki **matematik**i anlamadan, gerçek bir AI engineer olamazsın. Bu ders seni "kütüphane çağıran kişi"den "ne yaptığını bilen mühendis"e dönüştürecek. Linear algebra, calculus, probability ve optimization -- hepsini Python koduyla pratiğe dökeceğiz.

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Gradient Descent algoritmasini bir dagdan inis analojisiyle acikla. Learning rate, loss function ve gradient kavramlarini gorsellerle anlat. Stochastic, Mini-batch ve Batch Gradient Descent arasindaki farklari, her birinin avantaj/dezavantajlarini ve ne zaman hangisinin kullanildigini karsilastir."

**2. Pratik Uygulama:**
> "NumPy ile sifirdan basit bir linear regression modeli oluştur. Loss function (MSE) tanimla, gradient'leri elle hesapla ve gradient descent ile parametreleri optimize et. Her iterasyondaki loss degerini ciz. Learning rate'i degistirerek etkisini goster."
> Takip: "Simdi ayni modele L2 regularization ekle. Regularization'in gradient hesabini ve weight'leri nasil etkiledigini matematiksel olarak goster."

**3. Mukemmellik Icin:**
> "Bir ArXiv paper'indaki attention mechanism formulunu (Q, K, V matrix carpimi ve softmax) adim adim acikla. Scaled dot-product attention'daki her matematik isleminin (matrix multiplication, scaling, softmax, weighted sum) ne yaptigini ve neden gerekli oldugunu goster."

### Pair Programming Ipucu
Matematik kavramlarini ogrenirken AI'a kendi cozumunu goster ve sor: "Bu gradient hesabimi kontrol et. Chain rule dogru uygulanmis mi? Backpropagation'daki her adimi dogrula ve hatami bul."
:::

:::must-note
## Defterine Yaz!
1. **Gradient Descent** = Loss function'ın minimum noktasını bulmak için türev yönünde adım atma. Learning rate çok büyükse ıraksama, çok küçükse yavaşlık.
2. **Dot Product** = İki vector'ün benzerliğini ölçer. Cosine similarity'nin temeli. NLP'de embedding comparison'da her yerde kullanılır.
3. **Bayes Theorem**: P(A|B) = P(B|A) * P(A) / P(B) -- Naive Bayes classifier'dan spam filter'a kadar her yerde.
4. **Chain Rule** = Backpropagation'ın matematiksel temeli. Neural network'te gradient'ler bu kuralla hesaplanır.
5. **Matrix Multiplication** = Neural network'teki her layer bir matrix çarpımıdır: output = activation(W @ x + b)
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir
Senior bir AI engineer matematik konusunda şunu yapar:
- **Paper okur**: ArXiv'deki yeni paper'lardaki formülleri anlamak için linear algebra ve calculus bilgisi şart
- **Intuition geliştirir**: Her formülü ezberlemez, ama gradient descent'in "tepedan iniş" olduğunu geometrik olarak kavrar
- **Debugging yapar**: Model converge etmiyorsa, learning rate'i, loss function'ı ve gradient'leri analiz eder
- **Trade-off analizi**: L1 vs L2 regularization'ın matematiksel farkını bilir ve hangi durumda hangisini seçeceğini anlar
- **Scalability düşünür**: Matrix operation'ların computational complexity'sini bilir (O(n^3) vs O(n^2))
:::

---

## 1. Linear Algebra -- ML'in Dili

Machine Learning'de **her şey** vector ve matrix. Bir resim? Pixel matrix'i. Bir cümle? Word embedding vector'ü. Bir dataset? Feature matrix'i.

### 1.1 Vector'ler

:::concept
## Vector Nedir?

Vector, yönü ve büyüklüğü olan matematiksel bir nesnedir. ML'de bir **data point'i** temsil eder.

Bir kullanıcıyı düşün:
- Yaş: 25
- Gelir: 50000
- Kredi skoru: 720

Bu kullanıcı bir **3-boyutlu vector**: [25, 50000, 720]

Her feature bir **dimension** (boyut) ekler. 100 feature'ın varsa, 100 boyutlu uzayda çalışıyorsun.
:::

```python
import numpy as np

# Vector oluşturma
user_a = np.array([25, 50000, 720])
user_b = np.array([35, 75000, 680])

# Vector toplama
combined = user_a + user_b
print(f"Toplam: {combined}")  # [60, 125000, 1400]

# Scalar çarpım (her elemanı 2 ile çarp)
scaled = user_a * 2
print(f"Scaled: {scaled}")  # [50, 100000, 1440]

# Vector büyüklüğü (norm/magnitude)
magnitude = np.linalg.norm(user_a)
print(f"Magnitude: {magnitude:.2f}")  # 50000.01

# Unit vector (normalize)
unit = user_a / np.linalg.norm(user_a)
print(f"Unit vector: {unit}")
```

### 1.2 Dot Product (Skaler Çarpım)

:::concept
## Dot Product Neden Önemli?

Dot product iki vector'ün **ne kadar benzer yönde** olduğunu ölçer.

**Formül**: a . b = a1*b1 + a2*b2 + ... + an*bn

**Geometrik anlam**: a . b = |a| * |b| * cos(theta)

- cos(0) = 1 --> Aynı yön --> Maksimum benzerlik
- cos(90) = 0 --> Dik --> İlişkisiz
- cos(180) = -1 --> Zıt yön --> Tam ters

Bu yüzden **cosine similarity** recommendation system'lerde kullanılır!
:::

```python
import numpy as np

# İki film tercihi (rating vector'leri)
alice = np.array([5, 4, 1, 2, 5])   # Action sevgi, romance sevmez
bob   = np.array([4, 5, 2, 1, 4])   # Alice'e benzer
carol = np.array([1, 2, 5, 5, 1])   # Tam tersi: romance sever

# Dot product
print(f"Alice . Bob = {np.dot(alice, bob)}")     # Yüksek (benzer)
print(f"Alice . Carol = {np.dot(alice, carol)}")  # Düşük (farklı)

# Cosine similarity (daha doğru karşılaştırma)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"Cosine(Alice, Bob) = {cosine_similarity(alice, bob):.4f}")    # ~0.98
print(f"Cosine(Alice, Carol) = {cosine_similarity(alice, carol):.4f}")  # ~0.50
```

:::realworld
## Gerçek Dünyada Dot Product
- **Google Search**: Query ve document embedding'leri arasındaki dot product ile relevance hesaplanır
- **Spotify/Netflix**: Kullanıcı ve item embedding'leri arasındaki similarity ile öneri yapılır
- **ChatGPT**: Attention mechanism'da query ve key vector'lerinin dot product'ı kullanılır
:::

### 1.3 Matrix'ler ve İşlemler

:::concept
## Matrix = Veri Tablosu

Matrix, sayılardan oluşan 2 boyutlu bir tablodur. ML'de:
- **Dataset**: Satırlar = sample'lar, sütunlar = feature'lar
- **Weights**: Neural network'te her layer bir weight matrix'idir
- **Images**: Gri tonlu bir resim = pixel değerleri matrix'i

Boyut gösterimi: (satır x sütun) = (m x n)
:::

```python
import numpy as np

# 3 kullanıcı, 4 feature: [yaş, gelir, kredi_skoru, borç]
X = np.array([
    [25, 50000, 720, 5000],
    [35, 75000, 680, 15000],
    [45, 90000, 750, 8000]
])

print(f"Shape: {X.shape}")      # (3, 4) = 3 sample, 4 feature
print(f"Transpose: {X.T.shape}") # (4, 3) = feature x sample

# Matrix çarpımı: X (3x4) @ W (4x2) = Output (3x2)
# Neural network layer simülasyonu
W = np.array([
    [0.1, 0.2],
    [0.3, 0.4],
    [0.5, 0.6],
    [0.7, 0.8]
])

output = X @ W  # veya np.matmul(X, W)
print(f"Output shape: {output.shape}")  # (3, 2)
print(f"Output:\n{output}")

# Boyut kuralı: (m x n) @ (n x p) = (m x p)
# İç boyutlar eşleşmeli!
```

:::warning
## Matrix Çarpımı Boyut Hatası
En sık ML hatası: **dimension mismatch**

```
ValueError: matmul: Input operand 1 has a mismatch
in its core dimension 0, with signature (n?,k),(k,m?)->(n?,m?)
```

**Kural**: A(m x **n**) @ B(**n** x p) --> iç boyutlar (n) eşleşmeli!

Neural network'te layer'lar tanımlarken her zaman önceki layer'ın output dimension'ını sonraki layer'ın input dimension'ı olarak kullanmalısın.
:::

### 1.4 Özel Matrix'ler

```python
import numpy as np

# Identity matrix (birim matris)
I = np.eye(3)
print(f"Identity:\n{I}")
# A @ I = A (çarpma identity'si)

# Inverse (ters matris) - Linear regression'da kullanılır
A = np.array([[2, 1], [5, 3]])
A_inv = np.linalg.inv(A)
print(f"A @ A_inv = \n{A @ A_inv}")  # Identity matrix olmalı

# Determinant
det = np.linalg.det(A)
print(f"Determinant: {det}")  # 0 ise inverse yok (singular matrix)

# Eigenvalues & Eigenvectors (PCA'nın temeli)
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"Eigenvalues: {eigenvalues}")
print(f"Eigenvectors:\n{eigenvectors}")
```

:::tip
## PCA ve Eigenvalues
**Principal Component Analysis (PCA)** feature reduction tekniğidir. 1000 feature'ı 50'ye düşürmek istersen:
1. Covariance matrix hesapla
2. Eigenvalue'ları bul
3. En büyük eigenvalue'lara karşılık gelen eigenvector'leri seç
4. Data'yı bu yeni "principal component" uzayına project et

**Eigenvalue** = O yöndeki variance miktarı. Büyükse, o yön önemli.
:::

---

## 2. Calculus -- Öğrenmenin Motoru

Neural network nasıl "öğrenir"? Calculus ile! Derivative (türev) ve gradient, model'in hatalarını azaltmasının anahtarıdır.

### 2.1 Derivative (Türev) Temelleri

:::concept
## Türev = Değişim Hızı

Türev, bir fonksiyonun belirli bir noktadaki **anlık değişim hızını** verir.

**ML'deki anlam**: Loss function'ın weight'lere göre türevi = "Weight'i biraz değiştirirsem loss ne kadar değişir?"

- Türev pozitif --> Weight artınca loss artıyor --> Weight'i **azalt**
- Türev negatif --> Weight artınca loss azalıyor --> Weight'i **artır**
- Türev sıfır --> Minimum (veya maximum) noktadasın

Bu gradient descent'in temelidir!
:::

```python
import numpy as np
import matplotlib.pyplot as plt

# Basit fonksiyon: f(x) = x^2
# Türevi: f'(x) = 2x
def f(x):
    return x ** 2

def f_derivative(x):
    return 2 * x

# Numerical derivative (bilgisayarla türev hesaplama)
def numerical_derivative(func, x, h=1e-7):
    return (func(x + h) - func(x - h)) / (2 * h)

x = 3.0
print(f"Analitik türev f'(3) = {f_derivative(x)}")           # 6.0
print(f"Numerical türev f'(3) = {numerical_derivative(f, x):.6f}")  # ~6.0

# Gradient descent ile minimum bulma
x = 10.0  # Başlangıç noktası
learning_rate = 0.1
history = [x]

for i in range(20):
    gradient = f_derivative(x)
    x = x - learning_rate * gradient  # Gradient'in tersine git!
    history.append(x)
    if i % 5 == 0:
        print(f"Step {i}: x = {x:.4f}, f(x) = {f(x):.4f}")

# x, 0'a yakınsar (minimum nokta)
```

### 2.2 Partial Derivatives ve Gradient

:::concept
## Gradient = Tüm Partial Derivative'lerin Vektörü

Birden fazla variable'ın olduğu fonksiyonlarda, **her variable'a göre ayrı ayrı** türev alırsın.

f(x, y) = x^2 + y^2 ise:
- df/dx = 2x (y sabit tutularak)
- df/dy = 2y (x sabit tutularak)

**Gradient**: nabla f = [df/dx, df/dy] = [2x, 2y]

Gradient, fonksiyonun **en hızlı arttığı yönü** gösterir.
Gradient descent'te **gradient'in tersine** gideriz (en hızlı azalma yönü).

Neural network'te yüzlerce weight var --> gradient, her weight'e göre partial derivative içerir.
:::

```python
import numpy as np

# f(w1, w2) = w1^2 + 2*w2^2 + w1*w2
# df/dw1 = 2*w1 + w2
# df/dw2 = 4*w2 + w1

def loss(w):
    return w[0]**2 + 2*w[1]**2 + w[0]*w[1]

def gradient(w):
    dw1 = 2*w[0] + w[1]
    dw2 = 4*w[1] + w[0]
    return np.array([dw1, dw2])

# Gradient Descent
w = np.array([5.0, 3.0])  # Başlangıç weight'leri
lr = 0.1

print(f"Start: w = {w}, loss = {loss(w):.4f}")

for i in range(50):
    grad = gradient(w)
    w = w - lr * grad
    if i % 10 == 0:
        print(f"Step {i}: w = [{w[0]:.4f}, {w[1]:.4f}], loss = {loss(w):.6f}")

print(f"Final: w = {w}, loss = {loss(w):.8f}")
# w = [0, 0] minimum noktasına yakınsar
```

### 2.3 Chain Rule -- Backpropagation'ın Temeli

:::concept
## Chain Rule (Zincir Kuralı)

İç içe fonksiyonların türevi:

y = f(g(x)) ise dy/dx = f'(g(x)) * g'(x)

**Neural network örneği**:
- Layer 1: z1 = W1 @ x + b1
- Activation: a1 = sigmoid(z1)
- Layer 2: z2 = W2 @ a1 + b2
- Loss: L = (z2 - y)^2

Loss'un W1'e göre türevi:
dL/dW1 = dL/dz2 * dz2/da1 * da1/dz1 * dz1/dW1

Her zincir halkası bir layer! Bu **backpropagation** algoritmasıdır.
:::

```python
import numpy as np

# Chain rule örneği: f(x) = (2x + 3)^4
# g(x) = 2x + 3, f(g) = g^4
# f'(x) = 4*(2x+3)^3 * 2 = 8*(2x+3)^3

def f(x):
    return (2*x + 3)**4

def f_chain_derivative(x):
    return 8 * (2*x + 3)**3  # chain rule ile

x = 1.0
print(f"Chain rule: f'(1) = {f_chain_derivative(x)}")  # 8 * 125 = 1000

# Numerical doğrulama
h = 1e-7
numerical = (f(x+h) - f(x-h)) / (2*h)
print(f"Numerical:  f'(1) = {numerical:.2f}")  # ~1000

# Mini neural network ile backpropagation
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1 - s)

# Forward pass
x = np.array([1.0, 2.0])
w1 = np.array([0.5, -0.3])
b1 = 0.1
w2 = 0.7
b2 = -0.2
y_true = 1.0

z1 = np.dot(w1, x) + b1      # Linear: 0.5*1 + (-0.3)*2 + 0.1 = 0.0
a1 = sigmoid(z1)               # Activation: sigmoid(0.0) = 0.5
z2 = w2 * a1 + b2             # Output: 0.7*0.5 - 0.2 = 0.15
loss = (z2 - y_true) ** 2     # Loss: (0.15 - 1)^2 = 0.7225

print(f"Forward: z1={z1:.4f}, a1={a1:.4f}, z2={z2:.4f}, loss={loss:.4f}")

# Backward pass (chain rule)
dL_dz2 = 2 * (z2 - y_true)          # dLoss/dz2
dz2_da1 = w2                         # dz2/da1
da1_dz1 = sigmoid_derivative(z1)     # da1/dz1
dz1_dw1 = x                          # dz1/dw1

# Chain: dL/dw1 = dL/dz2 * dz2/da1 * da1/dz1 * dz1/dw1
dL_dw1 = dL_dz2 * dz2_da1 * da1_dz1 * dz1_dw1
print(f"Gradients for w1: {dL_dw1}")
```

:::beginner-mistake
## Sık Yapılan Hatalar -- Calculus

**Hata 1**: "Türev bilmeme gerek yok, framework halleder"
- Framework gradient hesaplar ama debug edemezsin. Gradient exploding/vanishing olduğunda ne olduğunu anlamazsın.

**Hata 2**: "Learning rate'i rastgele seçerim"
- Learning rate gradient ile çarpılır. Gradient büyükse lr küçük olmalı, gradient küçükse lr büyük olmalı. Adaptive optimizer'lar (Adam) bunu otomatik yapar ama neden yaptığını bilmelisin.

**Hata 3**: "Loss azalmıyor, daha çok epoch atayım"
- Belki gradient vanishing var (sigmoid kullanıyorsan). Belki learning rate çok büyük ve oscillation yapıyor. Gradient'leri logla!
:::

---

## 3. Probability ve Statistics -- Belirsizliği Modelleme

ML, özünde **belirsizlik altında karar verme**dir. Probability ve statistics bu belirsizliği anlamamızı sağlar.

### 3.1 Temel Olasılık Kavramları

```python
import numpy as np
from collections import Counter

# Simülasyon ile olasılık
np.random.seed(42)

# Zar atma simülasyonu
rolls = np.random.randint(1, 7, size=100000)
counts = Counter(rolls)

print("Zar olasılıkları (100K atış):")
for face in sorted(counts):
    prob = counts[face] / len(rolls)
    print(f"  {face}: {prob:.4f} (teorik: {1/6:.4f})")

# Conditional Probability
# P(A|B) = P(A ve B) / P(B)
# Örnek: Email spam filtresi
# P(spam | "kazandınız" kelimesi var) = ?

total_emails = 10000
spam_emails = 3000     # P(spam) = 0.30
ham_emails = 7000      # P(ham) = 0.70

# "kazandınız" kelimesini içeren email sayıları
spam_with_word = 2700   # Spam'lerin %90'ında var
ham_with_word = 70      # Ham'lerin %1'inde var

# P(kazandınız) = (2700 + 70) / 10000
p_word = (spam_with_word + ham_with_word) / total_emails

# P(spam | kazandınız) = P(kazandınız | spam) * P(spam) / P(kazandınız)
p_spam_given_word = (spam_with_word / spam_emails) * (spam_emails / total_emails) / p_word
print(f"\nP(spam | 'kazandınız') = {p_spam_given_word:.4f}")  # ~0.975
```

### 3.2 Bayes Theorem

:::concept
## Bayes Theorem -- ML'in Felsefi Temeli

**P(A|B) = P(B|A) * P(A) / P(B)**

- **P(A)**: Prior -- Önceki bilgimiz (data görmeden)
- **P(B|A)**: Likelihood -- A doğruysa B'yi görme olasılığı
- **P(B)**: Evidence -- B'nin genel olasılığı
- **P(A|B)**: Posterior -- Data'yı gördükten sonraki güncelllenmiş inanç

ML uygulaması: Naive Bayes Classifier
- Spam filter: P(spam | email metni)
- Sentiment analysis: P(pozitif | yorum metni)
- Medical diagnosis: P(hastalık | semptomlar)
:::

```python
import numpy as np

# Bayes Theorem ile hastalık testi
# Hastalık prevalansı: %1 (nadir)
# Test doğruluğu:
#   - Hasta kişiyi hasta buluyor: %99 (sensitivity)
#   - Sağlam kişiyi sağlam buluyor: %95 (specificity)

# Soru: Test pozitif çıktı. Gerçekten hasta olma olasılığı?

p_disease = 0.01       # Prior: P(hasta)
p_healthy = 0.99       # P(sağlam)
p_pos_given_disease = 0.99  # Sensitivity: P(pozitif | hasta)
p_pos_given_healthy = 0.05  # False positive rate: P(pozitif | sağlam)

# P(pozitif) = P(pos|hasta)*P(hasta) + P(pos|sağlam)*P(sağlam)
p_positive = p_pos_given_disease * p_disease + p_pos_given_healthy * p_healthy

# Bayes: P(hasta | pozitif test)
p_disease_given_positive = (p_pos_given_disease * p_disease) / p_positive

print(f"P(hasta | pozitif test) = {p_disease_given_positive:.4f}")
# ~0.167 = %16.7 -- Çoğu kişi bunu %99 sanır!
# Base rate fallacy: Nadir hastalıkta pozitif test bile güvenilir değil
```

:::interview
## Mülakat Sorusu: Base Rate Fallacy

**Soru**: "Test accuracy'si %99 olan bir hastalık testi pozitif çıktı. Hastanın gerçekten hasta olma olasılığı nedir?"

**Beklenen cevap**: "Yeterli bilgi yok. Hastalığın prevalansı (base rate) bilinmeli. Eğer hastalık %1 prevalanslıysa, pozitif test'e rağmen hasta olma olasılığı sadece ~%17. Bu Bayes Theorem ile hesaplanır."

**Neden sorulur**: ML model'lerin gerçek dünya performansını değerlendirirken base rate çok önemli. Imbalanced dataset'lerde accuracy yanıltıcıdır -- %99 accuracy, %1 pozitif sınıfı hiç tahmin etmeden elde edilebilir.
:::

### 3.3 Dağılımlar (Distributions)

```python
import numpy as np
from scipy import stats

# Normal (Gaussian) Distribution
# Doğadaki çoğu şey normal dağılır: boy, IQ, hata payları
mu, sigma = 170, 10  # Ortalama boy 170cm, std 10cm
samples = np.random.normal(mu, sigma, 10000)

print(f"Normal Distribution (boy):")
print(f"  Mean: {np.mean(samples):.2f}")
print(f"  Std:  {np.std(samples):.2f}")
print(f"  P(boy > 190) = {np.mean(samples > 190):.4f}")  # ~%2.3

# Bernoulli Distribution (iki sonuçlu deney)
# Spam mı değil mi, click mı değil mi
p_click = 0.05  # CTR = %5
clicks = np.random.binomial(1, p_click, 10000)
print(f"\nBernoulli (click): CTR = {np.mean(clicks):.4f}")

# Uniform Distribution (eşit olasılık)
uniform = np.random.uniform(0, 1, 10000)
print(f"Uniform: Mean = {np.mean(uniform):.4f}")  # ~0.5

# Poisson Distribution (birim zamandaki olay sayısı)
# Saatte ortalama 3 hata alıyoruz, 5+ hata gelme olasılığı?
lambda_val = 3  # Ortalama hata/saat
errors = np.random.poisson(lambda_val, 10000)
print(f"\nPoisson (hatalar): P(5+ hata/saat) = {np.mean(errors >= 5):.4f}")
```

### 3.4 Statistical Testing

:::concept
## Hypothesis Testing -- A/B Test'in Temeli

**H0 (Null Hypothesis)**: "İki grup arasında fark yok"
**H1 (Alternative Hypothesis)**: "Fark var"

**p-value**: H0 doğruyken gözlenen sonucu (veya daha ekstremini) elde etme olasılığı.

- p < 0.05 --> "İstatistiksel olarak anlamlı" --> H0 red, H1 kabul
- p >= 0.05 --> "Anlamlı fark yok" --> H0 reddedilemez

ML'deki kullanım: Model A, Model B'den **gerçekten** daha iyi mi, yoksa rastlantı mı?
:::

```python
import numpy as np
from scipy import stats

# A/B Test örneği: Yeni buton rengi conversion'ı artırdı mı?
np.random.seed(42)

# Kontrol grubu (mavi buton): 1000 kişi, 50 conversion
control = np.random.binomial(1, 0.050, 1000)  # ~%5 conversion

# Test grubu (yeşil buton): 1000 kişi, 65 conversion
test = np.random.binomial(1, 0.065, 1000)     # ~%6.5 conversion

# t-test
t_stat, p_value = stats.ttest_ind(control, test)
print(f"Control conversion: {control.mean():.4f}")
print(f"Test conversion:    {test.mean():.4f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("SONUÇ: İstatistiksel olarak anlamlı fark VAR (p < 0.05)")
    print("Yeşil butonu kullanabilirsin!")
else:
    print("SONUÇ: Anlamlı fark YOK. Daha fazla veri topla.")

# Chi-square test (kategorik veriler için)
# Observed vs Expected
observed = np.array([50, 30, 20])  # Gerçek dağılım
expected = np.array([33.3, 33.3, 33.4])  # Beklenen (eşit)
chi2, p = stats.chisquare(observed, expected)
print(f"\nChi-square: chi2={chi2:.2f}, p={p:.4f}")
```

:::comparison
## Hangi Test Ne Zaman?

| Test | Kullanım | Veri Tipi |
|------|----------|-----------|
| **t-test** | İki grubun ortalamasını karşılaştırma | Sürekli (continuous) |
| **Chi-square** | Kategorik değişkenler arası ilişki | Kategorik |
| **ANOVA** | 3+ grubun ortalamasını karşılaştırma | Sürekli |
| **Mann-Whitney U** | Non-parametrik iki grup karşılaştırma | Sıralı (ordinal) |
| **Kolmogorov-Smirnov** | Dağılım testi | Sürekli |

**ML'de en çok kullanılan**: t-test (model karşılaştırma), Chi-square (feature selection)
:::

---

## 4. Optimization -- Modeli Eğitmenin Yolu

### 4.1 Loss Functions

:::concept
## Loss Function = Hata Ölçümü

Loss function, model'in tahminlerinin gerçek değerlerden ne kadar **uzak** olduğunu ölçer. Amacımız bu loss'u **minimize** etmek.

**Regression Loss'ları:**
- **MSE** (Mean Squared Error): L = (1/n) * SUM(y_pred - y_true)^2
  - Büyük hataları cezalandırır (karesel)
- **MAE** (Mean Absolute Error): L = (1/n) * SUM(|y_pred - y_true|)
  - Outlier'lara daha dayanıklı

**Classification Loss'ları:**
- **Binary Cross-Entropy**: L = -[y*log(p) + (1-y)*log(1-p)]
  - Yanlış ve emin tahminleri çok cezalandırır
- **Categorical Cross-Entropy**: Multi-class versiyonu
:::

```python
import numpy as np

# Regression losses
y_true = np.array([3.0, 5.0, 2.5, 7.0])
y_pred = np.array([2.8, 5.2, 2.0, 6.5])

# MSE
mse = np.mean((y_pred - y_true) ** 2)
print(f"MSE: {mse:.4f}")

# MAE
mae = np.mean(np.abs(y_pred - y_true))
print(f"MAE: {mae:.4f}")

# RMSE (Root MSE - aynı birimde)
rmse = np.sqrt(mse)
print(f"RMSE: {rmse:.4f}")

# Binary Cross-Entropy
def binary_cross_entropy(y_true, y_pred):
    epsilon = 1e-15  # log(0) hatası önleme
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

y_true_class = np.array([1, 0, 1, 1, 0])
y_pred_probs = np.array([0.9, 0.1, 0.8, 0.7, 0.3])  # İyi tahminler
y_pred_bad   = np.array([0.1, 0.9, 0.2, 0.3, 0.8])  # Kötü tahminler

print(f"\nCross-Entropy (iyi): {binary_cross_entropy(y_true_class, y_pred_probs):.4f}")
print(f"Cross-Entropy (kötü): {binary_cross_entropy(y_true_class, y_pred_bad):.4f}")
```

### 4.2 Gradient Descent Variants

:::concept
## Gradient Descent Çeşitleri

1. **Batch Gradient Descent**: Tüm dataset üzerinden gradient hesapla
   - Doğru gradient, ama yavaş (büyük data'da)

2. **Stochastic Gradient Descent (SGD)**: Tek sample ile gradient
   - Hızlı ama gürültülü (noisy)

3. **Mini-Batch Gradient Descent**: Küçük batch (32, 64, 128) ile
   - En çok kullanılan -- iyi denge

4. **Adam (Adaptive Moment Estimation)**: Her weight için ayrı learning rate
   - Pratikte varsayılan optimizer
:::

```python
import numpy as np

# Gradient descent implementasyonu -- Linear Regression
np.random.seed(42)

# Sahte veri oluştur: y = 3x + 7 + noise
X = np.random.randn(100, 1)
y_true = 3 * X + 7 + np.random.randn(100, 1) * 0.5

# Parametreler
w = np.random.randn(1)  # weight başlangıcı
b = np.random.randn(1)  # bias başlangıcı
lr = 0.1
epochs = 100
batch_size = 16

print("=== Gradient Descent ile Linear Regression ===")

# Mini-Batch Gradient Descent
for epoch in range(epochs):
    # Shuffle data
    indices = np.random.permutation(len(X))
    X_shuffled = X[indices]
    y_shuffled = y_true[indices]

    epoch_loss = 0
    for i in range(0, len(X), batch_size):
        X_batch = X_shuffled[i:i+batch_size]
        y_batch = y_shuffled[i:i+batch_size]

        # Forward pass
        y_pred = X_batch * w + b
        loss = np.mean((y_pred - y_batch) ** 2)
        epoch_loss += loss

        # Backward pass (gradient hesaplama)
        dL_dw = 2 * np.mean((y_pred - y_batch) * X_batch)
        dL_db = 2 * np.mean(y_pred - y_batch)

        # Update
        w -= lr * dL_dw
        b -= lr * dL_db

    if epoch % 20 == 0:
        avg_loss = epoch_loss / (len(X) // batch_size)
        print(f"Epoch {epoch}: w={w[0]:.4f}, b={b[0]:.4f}, loss={avg_loss:.4f}")

print(f"\nSonuç: w={w[0]:.4f} (gerçek: 3.0), b={b[0]:.4f} (gerçek: 7.0)")
```

### 4.3 Learning Rate ve Scheduling

:::warning
## Learning Rate Seçimi Kritik!

Learning rate (lr) çok büyükse:
- Gradient step'leri çok büyük olur
- Minimum'u atlayıp **ıraksarsın** (diverge)
- Loss artmaya başlar veya NaN olur

Learning rate çok küçükse:
- Minimum'a çok yavaş yaklaşırsın
- Local minimum'da takılabilirsin
- Eğitim saatler sürer

**Pratik**: Adam optimizer kullan, lr=0.001 ile başla, loss platoya girerse lr'yi düşür.
:::

```python
import numpy as np

# Learning rate karşılaştırması
def gradient_descent_demo(lr, steps=50):
    x = 10.0
    history = []
    for _ in range(steps):
        grad = 2 * x  # f(x) = x^2, f'(x) = 2x
        x = x - lr * grad
        history.append(x)
    return history

# Farklı learning rate'ler
results = {}
for lr in [0.01, 0.1, 0.5, 0.9, 1.01]:
    hist = gradient_descent_demo(lr)
    final = hist[-1] if abs(hist[-1]) < 1e6 else float('inf')
    results[lr] = final
    print(f"lr={lr}: final x = {final:.6f}")

# lr=0.01: Yavaş yakınsar
# lr=0.1:  İyi yakınsar
# lr=0.5:  Hızlı yakınsar
# lr=0.9:  Zıplıyor ama yakınsar
# lr=1.01: IRAKSAR! (diverge)

# Learning Rate Scheduler
def lr_schedule(initial_lr, epoch, decay_rate=0.95):
    """Exponential decay"""
    return initial_lr * (decay_rate ** epoch)

def cosine_annealing(initial_lr, epoch, total_epochs):
    """Cosine annealing"""
    return initial_lr * 0.5 * (1 + np.cos(np.pi * epoch / total_epochs))

print("\nLR Schedule (exponential decay):")
for epoch in [0, 10, 20, 50, 100]:
    print(f"  Epoch {epoch}: lr = {lr_schedule(0.01, epoch):.6f}")

print("\nCosine Annealing:")
for epoch in [0, 25, 50, 75, 100]:
    print(f"  Epoch {epoch}: lr = {cosine_annealing(0.01, epoch, 100):.6f}")
```

### 4.4 Regularization -- Overfitting Önleme

:::concept
## L1 ve L2 Regularization

Regularization, model'in training data'ya aşırı uyum sağlamasını (overfitting) önler.

**L2 Regularization (Ridge/Weight Decay)**:
- Loss = MSE + lambda * SUM(w_i^2)
- Weight'leri küçük tutar (ama sıfır yapmaz)
- Tüm feature'ları kullanır, hepsini küçültür

**L1 Regularization (Lasso)**:
- Loss = MSE + lambda * SUM(|w_i|)
- Bazı weight'leri **tam sıfır** yapar
- Feature selection etkisi var (önemsiz feature'ları eler)

**Elastic Net**: L1 + L2 kombinasyonu
:::

```python
import numpy as np

# L2 Regularization etkisi
def train_with_regularization(X, y, reg_type='none', lambda_val=0.1, epochs=100, lr=0.01):
    n_features = X.shape[1]
    w = np.random.randn(n_features) * 0.1
    b = 0.0

    for epoch in range(epochs):
        # Forward
        y_pred = X @ w + b
        mse_loss = np.mean((y_pred - y) ** 2)

        # Regularization loss
        if reg_type == 'l2':
            reg_loss = lambda_val * np.sum(w ** 2)
            reg_grad = 2 * lambda_val * w
        elif reg_type == 'l1':
            reg_loss = lambda_val * np.sum(np.abs(w))
            reg_grad = lambda_val * np.sign(w)
        else:
            reg_loss = 0
            reg_grad = 0

        total_loss = mse_loss + reg_loss

        # Backward
        dw = (2/len(y)) * X.T @ (y_pred - y) + reg_grad
        db = (2/len(y)) * np.sum(y_pred - y)

        w -= lr * dw
        b -= lr * db

    return w, b, total_loss

# Sahte veri (10 feature, ama sadece 3'ü önemli)
np.random.seed(42)
X = np.random.randn(200, 10)
w_true = np.array([3.0, -2.0, 5.0, 0, 0, 0, 0, 0, 0, 0])
y = X @ w_true + np.random.randn(200) * 0.5

# Karşılaştırma
for reg in ['none', 'l1', 'l2']:
    w, b, loss = train_with_regularization(X, y, reg_type=reg, lambda_val=0.1, epochs=500, lr=0.01)
    print(f"\n{reg.upper():>4}: loss={loss:.4f}")
    print(f"      weights = [{', '.join(f'{wi:.3f}' for wi in w)}]")
    # L1: Sıfıra yakın weight'ler tam 0'a düşer (feature selection)
    # L2: Tüm weight'ler küçülür ama 0 olmaz
```

---

## 5. Her Şeyi Birleştiren Örnek: Mini ML Pipeline

```python
import numpy as np

# ===== COMPLETE EXAMPLE: Math Behind Logistic Regression =====
np.random.seed(42)

# 1. DATA GENERATION (Linear Algebra)
# 2 class, 2 feature
n_samples = 200
X_class0 = np.random.randn(n_samples // 2, 2) + np.array([1, 1])
X_class1 = np.random.randn(n_samples // 2, 2) + np.array([-1, -1])
X = np.vstack([X_class0, X_class1])
y = np.hstack([np.zeros(n_samples // 2), np.ones(n_samples // 2)])

# Shuffle
idx = np.random.permutation(n_samples)
X, y = X[idx], y[idx]

# Train/test split
X_train, X_test = X[:160], X[160:]
y_train, y_test = y[:160], y[160:]

# 2. MODEL: Logistic Regression from scratch
# Sigmoid (calculus: activation function)
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

# Binary cross-entropy loss (probability: likelihood)
def bce_loss(y_true, y_pred):
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# Initialize weights
w = np.zeros(2)
b = 0.0
lr = 0.1
epochs = 100

# 3. TRAINING (Optimization: Gradient Descent)
print("Training Logistic Regression from scratch:")
for epoch in range(epochs):
    # Forward pass (linear algebra: matrix multiplication)
    z = X_train @ w + b
    y_pred = sigmoid(z)

    # Loss (probability: cross-entropy)
    loss = bce_loss(y_train, y_pred)

    # Gradients (calculus: partial derivatives)
    error = y_pred - y_train
    dw = (1 / len(y_train)) * X_train.T @ error  # dL/dw
    db = (1 / len(y_train)) * np.sum(error)       # dL/db

    # Update (optimization: gradient descent)
    w -= lr * dw
    b -= lr * db

    if epoch % 20 == 0:
        print(f"  Epoch {epoch}: loss={loss:.4f}, w=[{w[0]:.3f}, {w[1]:.3f}], b={b:.3f}")

# 4. EVALUATION (Statistics: accuracy, confusion matrix)
y_pred_test = sigmoid(X_test @ w + b)
y_pred_class = (y_pred_test >= 0.5).astype(int)

accuracy = np.mean(y_pred_class == y_test)
tp = np.sum((y_pred_class == 1) & (y_test == 1))
fp = np.sum((y_pred_class == 1) & (y_test == 0))
fn = np.sum((y_pred_class == 0) & (y_test == 1))
tn = np.sum((y_pred_class == 0) & (y_test == 0))

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

print(f"\n=== Test Results ===")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"Confusion Matrix:")
print(f"  TP={tp} FP={fp}")
print(f"  FN={fn} TN={tn}")
```

:::deha-tip
## Deha İpucu: Geometric Intuition

ML matematiğini **görselleştirerek** öğren:

1. **Gradient Descent** = Sisli bir dağda en dik yokuştan inerek vadiye ulaşmak
2. **Dot Product** = İki okun ne kadar "aynı tarafa baktığını" ölçmek
3. **Eigenvalues** = Data'nın en çok "yayıldığı" yönleri bulmak (PCA)
4. **Cross-Entropy** = "Yanlış ve emin olmanın" cezası ("kesinlikle kedi" deyip köpek çıkması)
5. **Regularization** = Model'e "basit ol" demek (Occam's Razor)

**Paper okurken**: Formülü görünce önce "bu ne işe yarıyor?" diye düşün. Sonra "bunun kodu nasıl olur?" diye yaz. Ezberlemek yerine intuition geliştir.
:::

:::english
## Technical Terms Glossary

| English | Türkçe Açıklama |
|---------|-----------------|
| **Vector** | Yön ve büyüklüğü olan matematiksel nesne, ML'de veri noktası |
| **Dot Product** | İki vektörün eleman eleman çarpımlarının toplamı |
| **Matrix Multiplication** | Satır-sütun çarpımı, neural network layer'ının temel işlemi |
| **Derivative** | Fonksiyonun anlık değişim hızı |
| **Gradient** | Tüm partial derivative'lerin vektörü |
| **Chain Rule** | İç içe fonksiyonların türev kuralı, backpropagation'ın temeli |
| **Loss Function** | Model hatasını ölçen fonksiyon |
| **Gradient Descent** | Loss'u minimize etmek için gradient yönünde adım atma |
| **Learning Rate** | Gradient descent'te adım büyüklüğü |
| **Regularization** | Overfitting'i önlemek için weight'leri kısıtlama |
| **Prior/Posterior** | Bayes'te önceki/sonraki inanç |
| **p-value** | Null hypothesis altında gözlenen sonucun olasılığı |
| **Eigenvalue/Eigenvector** | Matrix'in temel bileşenleri, PCA'nın temeli |
| **Convergence** | Gradient descent'in minimum'a ulaşması |
:::

:::knowledge-check
## Bilgi Kontrolü

1. Dot product negatif bir değer veriyorsa, iki vektör hakkında ne söylenebilir?
2. Learning rate'i 2 katına çıkarırsak gradient descent'e etkisi ne olur?
3. L1 ve L2 regularization arasındaki temel fark nedir?
4. p-value 0.03 ise H0 hakkında ne karar veririz (alpha=0.05)?
5. Cross-entropy loss'ta model "kesinlikle 1" deyip gerçek "0" ise ne olur?
:::

:::exercise
### Alistirma 1: Lineer Cebir Temelleri — NumPy ile Matris Islemleri (Kolay)

NumPy kullanarak temel lineer cebir islemlerini uygula ve ML'deki kullanim alanlarini anla.

```python
import numpy as np

# 1. Vektor islemleri
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# TODO: Dot product hesapla (cosine similarity'nin temeli)
dot = np.dot(a, b)
print(f"Dot product: {dot}")  # 32

# TODO: Vektor normu (L2 norm) hesapla
norm_a = np.linalg.norm(a)
print(f"||a|| = {norm_a:.4f}")  # 3.7417

# TODO: Cosine similarity hesapla
cosine_sim = dot / (np.linalg.norm(a) * np.linalg.norm(b))
print(f"Cosine similarity: {cosine_sim:.4f}")

# 2. Matris islemleri
X = np.array([[1, 2], [3, 4], [5, 6]])  # 3x2 matris (3 ornek, 2 feature)
W = np.array([[0.5, -0.3, 0.8], [0.2, 0.7, -0.1]])  # 2x3 weight matrisi

# TODO: Matris carpimi (neural network'un temeli: X @ W)
output = X @ W
print(f"Output shape: {output.shape}")  # (3, 3)
print(f"Output:\n{output}")

# 3. Lineer denklem sistemi cozumu (Ax = b)
A = np.array([[2, 1], [1, 3]])
b = np.array([5, 7])
# TODO: np.linalg.solve ile coz
x = np.linalg.solve(A, b)
print(f"Cozum: x={x[0]:.2f}, y={x[1]:.2f}")
```

**Beklenen Sonuc:** Dot product = 32, cosine similarity yaklasik 0.9746. Matris carpimi (3,3) boyutunda olmali. Lineer denklem cozumu x=1.6, y=1.8 olmali.
**Ipucu:** ML'de feature matrix genelde (n_samples, n_features) formatindadir. Weight matrix ile carpim tahmin uretir.

---

### Alistirma 2: Gradient Descent Implementasyonu (Orta)

Gradient descent algoritmasini sifirdan implement et ve farkli learning rate'lerin etkisini gozlemle.

```python
import numpy as np
import matplotlib.pyplot as plt

# Hedef fonksiyon: f(x, y) = (x - 3)^2 + (y + 2)^2 + 0.5*x*y
def f(x, y):
    return (x - 3)**2 + (y + 2)**2 + 0.5 * x * y

# Gradient (kismi turevler)
def gradient(x, y):
    df_dx = 2 * (x - 3) + 0.5 * y
    df_dy = 2 * (y + 2) + 0.5 * x
    return np.array([df_dx, df_dy])

def gradient_descent(lr=0.1, n_steps=100, start=None):
    """Gradient descent ile minimumu bul."""
    if start is None:
        start = np.random.randn(2) * 5  # Random baslangic

    pos = start.copy()
    history = [pos.copy()]

    for step in range(n_steps):
        grad = gradient(pos[0], pos[1])
        pos = pos - lr * grad  # TODO: Gradient adimi
        history.append(pos.copy())

        if step % 10 == 0:
            loss = f(pos[0], pos[1])
            print(f"Step {step:3d}: x={pos[0]:.4f}, y={pos[1]:.4f}, loss={loss:.4f}")

    return pos, np.array(history)

# TODO: 3 farkli learning rate ile dene ve karsilastir
for lr in [0.01, 0.1, 0.5]:
    print(f"\n--- Learning Rate: {lr} ---")
    result, history = gradient_descent(lr=lr, n_steps=100, start=np.array([8.0, -8.0]))
    print(f"Final: x={result[0]:.4f}, y={result[1]:.4f}, loss={f(result[0], result[1]):.4f}")

# TODO: Convergence grafigi ciz (her lr icin loss vs step)
```

**Beklenen Sonuc:** lr=0.01 yavas yakinsar (100 adimda bitmeyebilir). lr=0.1 stabil yakinsar. lr=0.5 sallanabilir veya diverage edebilir. Minimum nokta yaklasik (3.47, -2.87) civaridir.
**Ipucu:** Learning rate cok buyukse gradient patlar (divergence), cok kucukse yavas yakinsar. Uygun lr bulmak ML'de kritik.

---

### Alistirma 3: Olasilik ve Bayes Teoremi ile Spam Filtresi (Zor)

Bayes teoremini kullanarak basit bir Naive Bayes spam siniflandirici implement et.

```python
import numpy as np
from collections import defaultdict

class NaiveBayesSpamFilter:
    def __init__(self):
        self.word_counts = {"spam": defaultdict(int), "ham": defaultdict(int)}
        self.class_counts = {"spam": 0, "ham": 0}
        self.vocab = set()

    def train(self, texts, labels):
        """Egitim verisinden kelime olasiliklerini ogren."""
        for text, label in zip(texts, labels):
            self.class_counts[label] += 1
            words = text.lower().split()
            for word in words:
                self.word_counts[label][word] += 1
                self.vocab.add(word)

    def predict(self, text):
        """Bayes teoremi ile spam olasligini hesapla."""
        words = text.lower().split()
        total = sum(self.class_counts.values())

        scores = {}
        for label in ["spam", "ham"]:
            # TODO: Prior olasiligi hesapla: P(label)
            log_prob = np.log(self.class_counts[label] / total)

            # TODO: Her kelime icin likelihood hesapla: P(word|label)
            # Laplace smoothing kullan (sifir olasilik problemi)
            total_words = sum(self.word_counts[label].values())
            for word in words:
                word_count = self.word_counts[label].get(word, 0)
                # P(word|label) = (count + 1) / (total_words + vocab_size)
                prob = (word_count + 1) / (total_words + len(self.vocab))
                log_prob += np.log(prob)

            scores[label] = log_prob

        return "spam" if scores["spam"] > scores["ham"] else "ham"

# Egitim verisi
train_texts = [
    "free money click here now", "win lottery prize today",
    "urgent claim your reward", "buy cheap pills online",
    "meeting tomorrow at 10am", "project deadline next week",
    "lunch plans for today", "code review needed please",
    "free trial for premium", "congratulations you won",
]
train_labels = ["spam", "spam", "spam", "spam", "ham", "ham", "ham", "ham", "spam", "spam"]

# TODO: Model egit ve test et
filter = NaiveBayesSpamFilter()
filter.train(train_texts, train_labels)

test_texts = [
    "free money win now",        # Spam
    "meeting agenda for monday", # Ham
    "click here for prize",      # Spam
    "project update attached",   # Ham
]

for text in test_texts:
    prediction = filter.predict(text)
    print(f"{prediction:4s} | {text}")
```

**Beklenen Sonuc:** Spam mesajlari "spam", normal mesajlari "ham" olarak siniflandirilmali. Laplace smoothing ile bilinmeyen kelimeler sifir olasilik vermemeli. Log-space'te hesaplama underflow'u onlemeli.
**Ipucu:** Olasiliklarla carpma yerine log'lari topluyoruz (underflow onleme). Laplace smoothing: her kelimeye +1 ekliyoruz ki hic gorulmemis kelimeler sifir olasilik vermesin.

---

### Alistirma 4: Eigenvalue ve PCA Implementasyonu (Kolay)

Principal Component Analysis'i sifirdan implement ederek boyut indirgeme yap.

```python
import numpy as np
import matplotlib.pyplot as plt

# Sentetik veri olustur (2D)
np.random.seed(42)
mean = [3, 5]
cov = [[2, 1.5], [1.5, 3]]
X = np.random.multivariate_normal(mean, cov, 200)

# PCA sifirdan
def pca_from_scratch(X, n_components):
    # 1. Veriyi merkezle (ortalamayi cikar)
    X_centered = X - np.mean(X, axis=0)

    # 2. Covariance matrix hesapla
    cov_matrix = np.cov(X_centered.T)

    # 3. Eigenvalue ve eigenvector hesapla
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    # 4. En buyuk eigenvalue'lara gore sirala
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # TODO: Explained variance ratio hesapla
    # TODO: n_components kadar eigenvector sec ve project et
    return X_centered @ eigenvectors[:, :n_components], eigenvalues

X_pca, eigenvalues = pca_from_scratch(X, 1)
print(f"Explained variance: {eigenvalues[0]/sum(eigenvalues)*100:.1f}%")

# TODO: 2D veriyi ve principal component'leri ciz
# TODO: sklearn PCA ile sonuclari karsilastir
```

**Beklenen Sonuc:** Ilk principal component varyans'in %70+'ini aciklamali. Sklearn PCA ile ayni sonuclar elde edilmeli.
**Ipucu:** PCA'da eigenvalue ne kadar buyukse, o yon o kadar fazla bilgi tasir. Dimensionality reduction icin kucuk eigenvalue'lu yonleri atiyoruz.

---

### Alistirma 5: Loss Function Karsilastirmasi (Kolay)

Farkli loss function'lari implement et ve davranislarini gorsellestir.

```python
import numpy as np
import matplotlib.pyplot as plt

def mse_loss(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def mae_loss(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def huber_loss(y_true, y_pred, delta=1.0):
    error = y_true - y_pred
    is_small = np.abs(error) <= delta
    squared = 0.5 * error ** 2
    linear = delta * (np.abs(error) - 0.5 * delta)
    return np.mean(np.where(is_small, squared, linear))

def cross_entropy_loss(y_true, y_pred):
    y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# TODO: Her loss function'in gradient'ini hesapla
# TODO: Outlier'lara karsi dayanikliligini karsilastir
# TODO: MSE vs MAE vs Huber'i ayni grafikte ciz
# TODO: Cross-entropy'nin 0 ve 1'deki davranisini incele
```

**Beklenen Sonuc:** MSE outlier'lara duyarli, MAE robust, Huber ikisinin ortasi olmali. Cross-entropy yanlis tahminlerde cok yuksek ceza vermeli.
**Ipucu:** MSE gradient'i 2*(y_pred - y_true), buyuk hatalarda buyuk adimlar atar. MAE gradient'i sabit, kucuk hatalarda yeterli olmayabilir.

---

### Alistirma 6: Activation Function'lari ve Turevleri (Orta)

Neural network activation function'larini ve turevlerini implement et.

```python
import numpy as np
import matplotlib.pyplot as plt

class ActivationFunctions:
    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    @staticmethod
    def sigmoid_derivative(x):
        s = ActivationFunctions.sigmoid(x)
        return s * (1 - s)

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def relu_derivative(x):
        return (x > 0).astype(float)

    @staticmethod
    def tanh(x):
        return np.tanh(x)

    @staticmethod
    def tanh_derivative(x):
        return 1 - np.tanh(x) ** 2

    # TODO: Leaky ReLU implement et (alpha=0.01)
    # TODO: ELU implement et
    # TODO: GELU implement et (Transformer'larda kullanilir)
    # TODO: Softmax implement et (multi-class icin)
    # TODO: Her fonksiyonu ve turevini ayni grafikte ciz

x = np.linspace(-5, 5, 200)
af = ActivationFunctions()
# Gorsellesitirme kodu...
```

**Beklenen Sonuc:** Her activation function ve turevi dogru hesaplanmali. ReLU'nun vanishing gradient problemini cozdugu, sigmoid'in saturasyon bolgesinde gradient'in sifira yaklastigi gorunmeli.
**Ipucu:** GELU = x * Phi(x), Transformer'larda ReLU yerine kullanilir. Softmax ciktilari toplamda 1 yapar (olasilik dagilimi).

---

### Alistirma 7: Regularization Teknikleri Karsilastirmasi (Orta)

L1, L2 ve Dropout regularization'i implement et ve overfitting'e etkisini gozlemle.

```python
import numpy as np

class LinearRegressionWithRegularization:
    def __init__(self, lr=0.01, reg_type=None, reg_lambda=0.1):
        self.lr = lr
        self.reg_type = reg_type
        self.reg_lambda = reg_lambda

    def fit(self, X, y, epochs=1000):
        n, d = X.shape
        self.W = np.random.randn(d) * 0.01
        self.b = 0
        self.losses = []

        for epoch in range(epochs):
            y_pred = X @ self.W + self.b
            loss = np.mean((y - y_pred) ** 2)

            # Regularization penalty
            if self.reg_type == "L2":
                loss += self.reg_lambda * np.sum(self.W ** 2)
                reg_grad = 2 * self.reg_lambda * self.W
            elif self.reg_type == "L1":
                loss += self.reg_lambda * np.sum(np.abs(self.W))
                reg_grad = self.reg_lambda * np.sign(self.W)
            else:
                reg_grad = 0

            self.losses.append(loss)
            grad_W = -(2/n) * X.T @ (y - y_pred) + reg_grad
            grad_b = -(2/n) * np.sum(y - y_pred)
            self.W -= self.lr * grad_W
            self.b -= self.lr * grad_b

        return self

# TODO: Overfitting veri seti olustur (az veri, cok feature)
# TODO: Regularization'siz, L1, L2 ile egit ve karsilastir
# TODO: L1'in sparse weight'ler olusturdugunuu dogrula (feature selection)
# TODO: Dropout simulasyonu yap (training sirasinda rastgele weight'leri sifirla)
```

**Beklenen Sonuc:** Regularization'siz model overfit etmeli. L1 bazi weight'leri sifira cekmeli (feature selection). L2 tum weight'leri kucultmeli.
**Ipucu:** L1 regularization feature selection yapar (sparse model). L2 regularization weight decay yapar (kucuk weight'ler).

---

### Alistirma 8: Cross-Validation Implementasyonu (Orta)

K-Fold Cross Validation'i sifirdan implement et.

```python
import numpy as np

def k_fold_cross_validation(X, y, model_class, k=5, **model_params):
    n = len(X)
    indices = np.random.permutation(n)
    fold_size = n // k
    scores = []

    for i in range(k):
        # Validation indeksleri
        val_start = i * fold_size
        val_end = val_start + fold_size
        val_idx = indices[val_start:val_end]
        train_idx = np.concatenate([indices[:val_start], indices[val_end:]])

        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        # Model egit ve degerlendir
        model = model_class(**model_params)
        model.fit(X_train, y_train)
        score = model.score(X_val, y_val)
        scores.append(score)
        print(f"Fold {i+1}: {score:.4f}")

    print(f"\nOrtalama: {np.mean(scores):.4f} ± {np.std(scores):.4f}")
    return scores

# TODO: Stratified K-Fold implement et (sinif dagilimini koru)
# TODO: Leave-One-Out CV implement et
# TODO: Farkli k degerleri ile (3, 5, 10) sonuclari karsilastir
# TODO: sklearn KFold ile dogrula
```

**Beklenen Sonuc:** Her fold'da farkli skor elde edilmeli. Ortalama ve standart sapma raporlanmali. Stratified versiyonda her fold'da sinif dagilimlari esit olmali.
**Ipucu:** k=5 veya k=10 standart secimlerdir. Kucuk veri setlerinde Leave-One-Out, buyuk veri setlerinde k=5 tercih edilir.

---

### Alistirma 9: Confusion Matrix ve Metrikler (Zor)

Binary classification metrikleri sifirdan implement et.

```python
import numpy as np

class ClassificationMetrics:
    def __init__(self, y_true, y_pred):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.tp = np.sum((y_true == 1) & (y_pred == 1))
        self.tn = np.sum((y_true == 0) & (y_pred == 0))
        self.fp = np.sum((y_true == 0) & (y_pred == 1))
        self.fn = np.sum((y_true == 1) & (y_pred == 0))

    def accuracy(self):
        return (self.tp + self.tn) / len(self.y_true)

    def precision(self):
        return self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0

    def recall(self):
        return self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0

    def f1_score(self):
        p, r = self.precision(), self.recall()
        return 2 * p * r / (p + r) if (p + r) > 0 else 0

    # TODO: Specificity hesapla (TN / (TN + FP))
    # TODO: ROC curve icin farkli threshold'larda TPR ve FPR hesapla
    # TODO: AUC (Area Under Curve) hesapla (trapezoidal rule ile)
    # TODO: Confusion matrix'i gorsel olarak ciz (heatmap)

# Test
y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
y_pred = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]
m = ClassificationMetrics(y_true, y_pred)
print(f"Accuracy: {m.accuracy():.4f}")
print(f"Precision: {m.precision():.4f}")
print(f"Recall: {m.recall():.4f}")
print(f"F1: {m.f1_score():.4f}")
```

**Beklenen Sonuc:** Precision, recall, F1 score dogru hesaplanmali. ROC curve cizilebilmeli. AUC degeri sklearn ile uyumlu olmali.
**Ipucu:** Imbalanced data'da accuracy yaniltici olur. Precision (yanlislikla pozitif deme) vs Recall (pozitifi kacirma) trade-off'unu anla.

---

### Alistirma 10: Optimization Algoritmalari Karsilastirmasi (Zor)

SGD, Momentum, Adam optimizer'larini sifirdan implement et ve karsilastir.

```python
import numpy as np
import matplotlib.pyplot as plt

# Rosenbrock fonksiyonu (zor optimizasyon problemi)
def rosenbrock(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

def rosenbrock_grad(x, y):
    dx = -2*(1 - x) - 400*x*(y - x**2)
    dy = 200*(y - x**2)
    return np.array([dx, dy])

class SGD:
    def __init__(self, lr=0.001):
        self.lr = lr

    def step(self, params, grads):
        return params - self.lr * grads

class Momentum:
    def __init__(self, lr=0.001, beta=0.9):
        self.lr, self.beta = lr, beta
        self.v = None

    def step(self, params, grads):
        if self.v is None:
            self.v = np.zeros_like(params)
        self.v = self.beta * self.v + (1 - self.beta) * grads
        return params - self.lr * self.v

class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr, self.beta1, self.beta2, self.eps = lr, beta1, beta2, eps
        self.m, self.v, self.t = None, None, 0

    def step(self, params, grads):
        if self.m is None:
            self.m = np.zeros_like(params)
            self.v = np.zeros_like(params)
        self.t += 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * grads
        self.v = self.beta2 * self.v + (1 - self.beta2) * grads**2
        m_hat = self.m / (1 - self.beta1**self.t)
        v_hat = self.v / (1 - self.beta2**self.t)
        return params - self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

# TODO: 3 optimizer'i ayni baslangic noktasindan calistir
# TODO: Her birinin izledigi yolu 2D contour plot uzerinde ciz
# TODO: Convergence hizlarini karsilastir (loss vs epoch)
# TODO: Learning rate scheduler ekle (decay)
```

**Beklenen Sonuc:** Adam en hizli converge etmeli. SGD en yavas, Momentum ortada olmali. Contour plot üzerinde izlenen yollar farkli olmali.
**Ipucu:** Adam = Momentum + RMSprop. Bias correction (m_hat, v_hat) ilk adimilardaki sapmayı duzeltir. AdamW = Adam + weight decay (modern standart).
:::

:::exercise
### Alistirma 11: Vektor ve Matris Islemleri Pratikte (Kolay)

NumPy ile temel lineer cebir islemlerini uygula.

```python
import numpy as np

# Vektor islemleri
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

# TODO: Dot product hesapla
# dot = np.dot(v1, v2)

# TODO: Cosine similarity hesapla
# cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# TODO: Matris carpimi
# A = np.array([[1, 2], [3, 4]])
# B = np.array([[5, 6], [7, 8]])
# C = A @ B  # veya np.matmul(A, B)

# TODO: Transpose, determinant, inverse hesapla
# TODO: Bir neural network layer'ini matris carpimi olarak ifade et
# output = activation(W @ x + b)
```

**Beklenen Sonuc:** Dot product, cosine similarity ve matris carpimi dogru hesaplanmali. NN layer'in matris formunu yazabilmeli.
**Ipucu:** Cosine similarity [-1, 1] araligindadir. 1 = ayni yon, 0 = dik, -1 = zit yon. NLP embedding karsilastirmasinda temel metriktir.
:::

:::exercise
### Alistirma 12: Turev ve Gradient Hesaplama (Kolay)

Python ile turev ve gradient hesaplama pratiği yap.

```python
import numpy as np

# Basit fonksiyon: f(x) = x^2 + 3x + 2
# Turevi: f'(x) = 2x + 3

# TODO: Numerik turev hesapla
def numerical_derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

# TODO: f(x) = x^2 + 3x + 2 icin turev hesapla ve analitik sonucla karsilastir
# f = lambda x: x**2 + 3*x + 2
# x = 2.0
# print(f"Numerik: {numerical_derivative(f, x)}")
# print(f"Analitik: {2*x + 3}")

# TODO: Partial derivative (cok degiskenli fonksiyon)
# f(x, y) = x^2 * y + y^3
# df/dx = 2xy, df/dy = x^2 + 3y^2

# TODO: Gradient vektoru hesapla
# grad_f = [df/dx, df/dy]
```

**Beklenen Sonuc:** Numerik ve analitik turev sonuclari eslestirilmeli. Gradient vektoru dogru hesaplanmali.
**Ipucu:** Numerik turev icin merkezi fark (central difference) formulu en dogruyu verir. h = 1e-7 iyi bir secimdir.
:::

:::exercise
### Alistirma 13: Olasilik Dagilim Gorsellemesi (Kolay)

Temel olasilik dagilimlrini gorlsellestir ve anla.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# TODO: Normal (Gauss) dagilim
# mu, sigma = 0, 1
# x = np.linspace(-4, 4, 100)
# plt.plot(x, stats.norm.pdf(x, mu, sigma), label='N(0,1)')
# plt.plot(x, stats.norm.pdf(x, 0, 2), label='N(0,2)')

# TODO: Bernoulli ve Binomial dagilim
# TODO: Poisson dagilim
# TODO: Uniform dagilim

# TODO: Central Limit Theorem gosterimi
# Farkli dagilimlardan orneklem ortalamasi alin
# Orneklem buyudukce normal dagilima yaklastigini gosterin

# TODO: Her dagilimin ML'deki kullanim alanini yaz
```

**Beklenen Sonuc:** 4 farkli dagilim gorsellestirilmeli. CLT etkisi gosterilmeli. Her dagilimin kullanim alani yazilmali.
**Ipucu:** Normal dagilim: regression hatalari. Bernoulli: binary classification. Poisson: event counting. Uniform: random initialization.
:::

:::exercise
### Alistirma 14: Learning Rate Etkisi Deneyimi (Orta)

Farkli learning rate'lerin gradient descent uzerindeki etkisini gozlemle.

```python
import numpy as np
import matplotlib.pyplot as plt

# Basit quadratic loss: L(w) = (w - 3)^2
def loss(w):
    return (w - 3) ** 2

def gradient(w):
    return 2 * (w - 3)

# TODO: 3 farkli learning rate ile gradient descent calistir
# learning_rates = [0.01, 0.1, 0.9]
# w_init = 10.0
# epochs = 50

# TODO: Her lr icin w ve loss degerlerini kaydet
# TODO: Loss vs epoch grafigi ciz (3 lr bir arada)
# TODO: w'nun izledigi yolu goster

# TODO: Cok buyuk lr ile iraksamayi (divergence) goster
# lr = 1.1 ile dene
```

**Beklenen Sonuc:** lr=0.01 yavas, lr=0.1 optimal, lr=0.9 salinimli converge etmeli. lr=1.1 iraksamali.
**Ipucu:** Kural: lr cok buyukse loss artar (diverge), cok kucukse cok yavas azalir. Learning rate scheduler ile baslangicta buyuk, sonra kucult.
:::

:::exercise
### Alistirma 15: Backpropagation Elle Hesaplama (Orta)

Basit bir neural network'te backpropagation'i elle hesapla.

```python
import numpy as np

# 2-layer network: input(2) -> hidden(2) -> output(1)
# Activation: sigmoid
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

# TODO: Forward pass hesapla
# x = np.array([0.5, 0.8])
# W1 = np.array([[0.1, 0.3], [0.2, 0.4]])
# b1 = np.array([0.1, 0.1])
# W2 = np.array([[0.5], [0.6]])
# b2 = np.array([0.1])
# target = np.array([1.0])

# z1 = W1 @ x + b1
# a1 = sigmoid(z1)
# z2 = W2.T @ a1 + b2
# output = sigmoid(z2)

# TODO: Loss hesapla (MSE)
# TODO: Backward pass — her katman icin gradient hesapla (chain rule)
# TODO: Weight'leri guncelle
# TODO: 100 iterasyon calistir ve loss'un azaldigini goster
```

**Beklenen Sonuc:** Forward ve backward pass elle hesaplanmali. 100 iterasyonda loss azalmali. Chain rule dogru uygulanmali.
**Ipucu:** Chain rule: dL/dW1 = dL/doutput * doutput/dz2 * dz2/da1 * da1/dz1 * dz1/dW1. Her adimi ayri hesapla.
:::

:::exercise
### Alistirma 16: Regularization Karsilastirmasi (Orta)

L1, L2 ve Dropout regularization'i karsilastir.

```python
import numpy as np

# TODO: L1 regularization (Lasso) — weight'leri sifira cekmek
# loss_l1 = mse_loss + lambda * sum(abs(w))
# gradient_l1 = gradient + lambda * sign(w)

# TODO: L2 regularization (Ridge) — weight'leri kucultmek
# loss_l2 = mse_loss + lambda * sum(w^2)
# gradient_l2 = gradient + 2 * lambda * w

# TODO: Farkli lambda degerleri ile overfitting etkisini goster
# lambdas = [0, 0.001, 0.01, 0.1, 1.0]
# Her lambda icin train ve test loss'u karsilastir

# TODO: L1 vs L2'nin weight dagilimina etkisini gorsellestir
# L1 sparse weight'ler uretir (feature selection)
# L2 kucuk ama sifir olmayan weight'ler uretir

# TODO: Dropout simulasyonu yaz
```

**Beklenen Sonuc:** L1 sparse, L2 kucuk weight'ler uretmeli. Optimal lambda overfitting'i azaltmali. Dropout etkisi gosterilmeli.
**Ipucu:** L1 = feature selection (gereksiz feature'larin weight'i 0 olur). L2 = genel shrinkage. Dropout = ensemble benzeri etki.
:::

:::exercise
### Alistirma 17: Feature Scaling ve Normalizasyon (Orta)

Farkli feature scaling tekniklerini karsilastir.

```python
import numpy as np

# Ornek veri
data = np.array([
    [25, 50000, 3],
    [30, 80000, 7],
    [22, 35000, 1],
    [45, 120000, 15]
])

# TODO: Min-Max Scaling [0, 1]
# scaled = (x - min) / (max - min)

# TODO: Standard Scaling (Z-score)
# scaled = (x - mean) / std

# TODO: Robust Scaling (outlier'lara dayanikli)
# scaled = (x - median) / IQR

# TODO: Her yontemin ne zaman kullanilacagini acikla
# TODO: Scaling olmadan vs ile gradient descent hizini karsilastir
# TODO: Contour plot ile scaling etkisini gorsellestir
```

**Beklenen Sonuc:** 3 scaling yontemi dogru uygulanmali. Scaling ile gradient descent daha hizli converge etmeli.
**Ipucu:** Feature'lar farkli olceklerdeyse (yas: 20-50, maas: 30K-120K) gradient descent zigzag yapar. Scaling bunu duzeltir.
:::

:::exercise
### Alistirma 18: Bias-Variance Tradeoff Analizi (Zor)

Bias-variance tradeoff'u gorsel olarak goster.

```python
import numpy as np
import matplotlib.pyplot as plt

# Gercek fonksiyon: y = sin(x) + noise
np.random.seed(42)
X = np.linspace(0, 2 * np.pi, 30)
y = np.sin(X) + np.random.normal(0, 0.3, len(X))

# TODO: Farkli karmasiklikta modeller fit et
# degree 1: Underfitting (high bias, low variance)
# degree 4: Just right
# degree 15: Overfitting (low bias, high variance)

# TODO: Her model icin train ve test error hesapla
# TODO: Bias^2 + Variance + Noise ayristirmasi yap
# TODO: Model complexity vs error grafigi ciz (U-curve)

# TODO: Cross-validation ile optimal complexity sec
```

**Beklenen Sonuc:** Underfitting, just-right ve overfitting gorsel olarak gosterilmeli. U-curve cizilmeli.
**Ipucu:** Total Error = Bias^2 + Variance + Irreducible Noise. Model karmasikligi artinca bias azalir, variance artar.
:::

:::exercise
### Alistirma 19: Matematik Kavramlarini ML Pipeline'a Baglama (Zor)

Ogrenilen tum matematik kavramlarini bir ML pipeline'inda uygula.

```python
import numpy as np

# TODO: End-to-end ML pipeline (sifirdan, kutuphane kullanmadan)

# 1. Veri olustur (synthetic classification)
# X: 100 ornek, 3 feature
# y: binary label

# 2. Feature scaling uygula (standard scaling)

# 3. Train/test split (%80/%20)

# 4. Logistic regression modeli yaz
#    - Sigmoid activation
#    - Binary cross-entropy loss
#    - Gradient descent optimizer
#    - L2 regularization

# 5. Egitim dongusu (100 epoch)
#    - Forward pass
#    - Loss hesapla
#    - Backward pass (gradient)
#    - Weight update

# 6. Evaluation
#    - Accuracy, precision, recall, F1
#    - Confusion matrix
#    - Loss vs epoch grafigi

# TODO: Her adimda kullanilan matematik kavramini belirt
```

**Beklenen Sonuc:** Sifirdan logistic regression calismali. Test accuracy %80+ olmali. Her adimda matematik konsepti etiketlenmeli.
**Ipucu:** Bu alistrima tum dersi birlestrir: linear algebra (matris carpimi), calculus (gradient), probability (sigmoid), optimization (GD).
:::


:::external-resource
## Ek Kaynaklar

- [3Blue1Brown - Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) -- Görsel linear algebra serisi
- [3Blue1Brown - Essence of Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) -- Calculus intuition
- [StatQuest - Machine Learning](https://www.youtube.com/c/joshstarmer) -- İstatistik ve ML kavramları basit anlatım
- [Khan Academy - Linear Algebra](https://www.khanacademy.org/math/linear-algebra) -- Başlangıç seviyesi
- [Mathematics for Machine Learning Book](https://mml-book.github.io/) -- Ücretsiz kitap
:::
