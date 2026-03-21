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

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "Gradient Descent algoritmasini bir dagdan inis analojisiyle acikla. Learning rate, loss function ve gradient kavramlarini gorsellerle anlat. Stochastic, Mini-batch ve Batch Gradient Descent arasindaki farklari, her birinin avantaj/dezavantajlarini ve ne zaman hangisinin kullanildigini karsilastir."

**2. Pratik Uygulama:**
> "NumPy ile sifirdan basit bir linear regression modeli olustur. Loss function (MSE) tanimla, gradient'leri elle hesapla ve gradient descent ile parametreleri optimize et. Her iterasyondaki loss degerini ciz. Learning rate'i degistirerek etkisini goster."
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
:::

:::external-resource
## Ek Kaynaklar

- [3Blue1Brown - Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) -- Görsel linear algebra serisi
- [3Blue1Brown - Essence of Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr) -- Calculus intuition
- [StatQuest - Machine Learning](https://www.youtube.com/c/joshstarmer) -- İstatistik ve ML kavramları basit anlatım
- [Khan Academy - Linear Algebra](https://www.khanacademy.org/math/linear-algebra) -- Başlangıç seviyesi
- [Mathematics for Machine Learning Book](https://mml-book.github.io/) -- Ücretsiz kitap
:::
