---
title: "Neural Networks ve Deep Learning"
id: mod-16-deep-learning/lesson-01
estimated_minutes: 95
order: 1
tags: [neural-networks, deep-learning, perceptron, backpropagation, activation-functions, cnn, rnn, lstm, pytorch, tensorflow]
prerequisites: [mod-15-ml-math/lesson-02]
---

# Neural Networks ve Deep Learning

Klasik ML algoritmaları (Random Forest, SVM) iyi çalışır ama **complex patterns** yakalamakta sınırlıdır. Neural network'ler, insan beyninden esinlenerek katmanlar halinde **non-linear** ilişkileri öğrenebilir. Bu ders seni perceptron'dan CNN ve RNN'e kadar götürecek.

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Backpropagation algoritmasini bir neural network örneği üzerinde adim adim acikla. Forward pass'te her layer'da ne hesaplaniyor? Loss hesaplandiktan sonra chain rule ile gradient'ler nasil geriye yayiliyor? Vanishing gradient problemi nedir ve ReLU activation neden bunu azaltiyor?"

**2. Pratik Uygulama:**
> "PyTorch ile sifirdan bir CNN (Convolutional Neural Network) oluştur ve MNIST dataset'inde el yazisi rakam tanima yap. Conv2d, MaxPool2d, ReLU, Fully Connected layer'lari kullan. Training loop, validation, early stopping ve model kaydetme islemlerini goster. Her layer'in ne ogrendigini gorsellestir."
> Takip: "Simdi ayni modeli transfer learning ile pre-trained ResNet kullanarak tekrar egit. Accuracy farkini karsilastir ve fine-tuning stratejisini acikla."

**3. Mukemmellik Icin:**
> "CNN, RNN, LSTM ve GRU mimarilerini karsilastir. Her birinin hangi problem tipi icin uygun oldugunu (goruntu siniflandirma, zaman serisi, dogal dil isleme) acikla. Attention mekanizmasinin RNN'lerin sequential limitation'ini nasil cozdugununu ve Transformer mimarisine gecisi anlat."

### Pair Programming Ipucu
Model egitirken AI'a training log ciktisini goster ve sor: "Loss azalmiyor, model converge etmiyor. Learning rate, batch size, model mimarisi ve data preprocessing adimlarimdaki potansiyel sorunlari analiz et. Debugging checklist'i oluştur."
:::

:::interview
## Mulakat Sorulari

**Soru 1: Backpropagation nasil calisir? Vanishing gradient problemi nedir?**
- **Junior cevabi:** Backpropagation hatalari geriye dogru yayarak weight'leri gunceller. Vanishing gradient derin aglarda gradient'lerin sifira yaklasmasidir.
- **Senior cevabi:** Backpropagation, chain rule kullanarak loss fonksiyonunun her weight'e gore partial derivative'ini hesaplar. Forward pass'te her layer'in ciktisi hesaplanir, backward pass'te gradient'ler output'tan input'a dogru yayilir. Vanishing gradient: sigmoid/tanh activation'larda gradient 0-1 arasinda oldugu icin derin aglarda katman sayisi arttikca gradient ust katmanlara ulasana kadar sifira yaklasir. Cozumler: ReLU activation (positive bolge icin gradient=1), residual connections (skip connections, ResNet), batch normalization (her layer'da normalizasyon), proper weight initialization (He, Xavier). Exploding gradient ise gradient clipping ile cozulur.

**Soru 2: CNN ve RNN arasindaki temel farklar nelerdir? Hangi problemlerde hangisi kullanilir?**
- **Junior cevabi:** CNN goruntu isleme, RNN metin ve zaman serisi icindir.
- **Senior cevabi:** CNN: convolutional layer'lar spatial hierarchy ogrenilir (edge -> texture -> object part -> object). Weight sharing ve local connectivity sayesinde parametre sayisi azdir. Kullanim: goruntu siniflandirma, object detection, segmentation, hatta 1D convolution ile metin siniflandirma. RNN: sequential data'da temporal dependency ogrenilir, hidden state önceki adimlarin bilgisini tasir. Ancak long-term dependency'de vanishing gradient sorunu yasanir. LSTM (gate mekanizmasiyla hangi bilgiyi unutacagina karar verir) ve GRU (simplified LSTM) bu sorunu cozer. Modern yaklasim: Transformer mimarisi (self-attention) hem CNN hem RNN'in yerini almasiyla NLP'de devrim yapti, Vision Transformer (ViT) ile goruntu islemede de kullanilmaya baslandi.
:::

:::code
## Google Colab ile Ucretsiz GPU Egitimi

Colab'da ucretsiz T4 GPU ile model egitebilirsin:

```python
# Google Colab'da calistir
# Runtime > Change runtime type > T4 GPU

!pip install torch torchvision

import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"Memory: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB")

# MNIST ile basit CNN egitimi
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Veri
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
train_data = datasets.MNIST('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)

# Model
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = self.dropout(self.relu(self.fc1(x)))
        return self.fc2(x)

model = SimpleCNN().cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Egitim
for epoch in range(5):
    model.train()
    total_loss = 0
    for batch_x, batch_y in train_loader:
        batch_x, batch_y = batch_x.cuda(), batch_y.cuda()
        optimizer.zero_grad()
        output = model(batch_x)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}: Loss = {total_loss/len(train_loader):.4f}")

# Sonuc: ~99% accuracy, 2-3 dakikada egitilir
```
:::

:::code
## Hugging Face ile Pre-trained Model Kullanimi

Sifirdan egitmek yerine, Hugging Face Hub'dan hazir model kullan:

```python
# Goruntu siniflandirma
from transformers import pipeline

classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
result = classifier("test_image.jpg")
print(result)  # [{'label': 'golden retriever', 'score': 0.98}]

# Metin ozetleme
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer("Uzun metin burada...", max_length=100, min_length=30)
print(summary[0]['summary_text'])

# Soru cevaplama
qa = pipeline("question-answering", model="deepset/roberta-base-squad2")
result = qa(question="Turkiye'nin baskenti neresi?", context="Turkiye'nin baskenti Ankara'dir.")
print(result)  # {'answer': 'Ankara', 'score': 0.99}
```

**Senior Ipucu:** Production'da kendi modelini egitmeden once, mutlaka pre-trained modelleri dene. Cogu zaman yeterli olur ve haftalarca egitim sürecinden kurtulursun.
:::

:::must-note
## Defterine Yaz!
1. **Neural Network = Linear transform + Non-linear activation + Backpropagation**. Her layer: output = activation(W @ input + bias)
2. **Activation fonksiyonları**: ReLU = max(0, x) default hidden layer seçimi. Sigmoid = output'ta binary classification. Softmax = output'ta multi-class classification.
3. **Backpropagation** = Chain rule ile her weight'in loss'a etkisini hesapla, sonra gradient descent ile güncelle. Forward --> Loss --> Backward --> Update döngüsü.
4. **CNN** = Convolutional layer'lar ile spatial pattern'ları yakalar. Image, video, spatial data. **RNN/LSTM** = Sequential data (text, time series, audio).
5. **Overfitting silahları**: Dropout (rastgele nöron kapat), Batch Normalization (layer çıktısını normalize et), Early Stopping (validation loss artınca dur), Data Augmentation.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir
Senior bir deep learning engineer şunları yapar:
- **Architecture selection**: Problem tipine göre doğru mimariyi seçer (CNN for vision, Transformer for NLP, GNN for graphs)
- **Training debugging**: Gradient'leri, loss curve'ü ve activation distribution'ları monitor eder (TensorBoard/W&B)
- **Scaling**: Distributed training (Data Parallel, Model Parallel), mixed precision (FP16) ve gradient accumulation bilir
- **Paper implementation**: ArXiv'den yeni paper okuyup PyTorch'ta implement edebilir
- **Trade-off analizi**: Model size vs latency vs accuracy -- production constraint'lerine göre karar verir
- **MLOps**: Model versioning, A/B testing, canary deployment, model monitoring
:::

---

## 1. Perceptron -- Her Şeyin Başlangıcı

### 1.1 Biyolojik Nörondan Yapay Nörona

:::concept
## Perceptron Nedir?

Perceptron, yapay sinir ağlarının en basit yapı taşıdır (1957, Frank Rosenblatt):

1. **Input'ları al**: x1, x2, ..., xn
2. **Weight'lerle çarp ve topla**: z = w1*x1 + w2*x2 + ... + wn*xn + bias
3. **Activation uygula**: output = activation(z)

Bu aslında **weighted sum + non-linearity** -- tüm neural network'lerin temeli.

Perceptron tek başına sadece **linearly separable** problemleri çözebilir (XOR çözemez!). Ama katmanlar halinde birleştirildiğinde (Multi-Layer Perceptron) her fonksiyonu approximate edebilir (**Universal Approximation Theorem**).
:::

```python
import numpy as np

class Perceptron:
    """Tek nöron - binary classification"""

    def __init__(self, n_features, learning_rate=0.01):
        self.weights = np.random.randn(n_features) * 0.01
        self.bias = 0.0
        self.lr = learning_rate

    def predict(self, x):
        """Forward pass"""
        z = np.dot(x, self.weights) + self.bias
        return 1 if z >= 0 else 0

    def train(self, X, y, epochs=100):
        """Perceptron learning rule"""
        for epoch in range(epochs):
            errors = 0
            for xi, yi in zip(X, y):
                prediction = self.predict(xi)
                error = yi - prediction

                if error != 0:
                    # Weight update: w += lr * error * x
                    self.weights += self.lr * error * xi
                    self.bias += self.lr * error
                    errors += 1

            if epoch % 20 == 0:
                accuracy = 1 - errors / len(y)
                print(f"Epoch {epoch}: accuracy = {accuracy:.4f}")

            if errors == 0:
                print(f"Converged at epoch {epoch}")
                break

# AND gate (linearly separable)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1])

print("=== AND Gate ===")
p = Perceptron(n_features=2, learning_rate=0.1)
p.train(X, y_and)

for xi, yi in zip(X, y_and):
    pred = p.predict(xi)
    print(f"  {xi} -> pred: {pred}, actual: {yi}")

# XOR gate (NOT linearly separable -- perceptron ÇÖZEMEZ!)
y_xor = np.array([0, 1, 1, 0])
print("\n=== XOR Gate (Perceptron ile çözülemez!) ===")
p_xor = Perceptron(n_features=2, learning_rate=0.1)
p_xor.train(X, y_xor, epochs=100)

for xi, yi in zip(X, y_xor):
    pred = p_xor.predict(xi)
    status = "OK" if pred == yi else "WRONG"
    print(f"  {xi} -> pred: {pred}, actual: {yi} [{status}]")
```

---

## 2. Activation Functions

:::concept
## Neden Activation Function Gerekli?

Activation function olmadan neural network sadece linear transformation yapar:
- Layer 1: y1 = W1 @ x + b1
- Layer 2: y2 = W2 @ y1 + b2
- Birleştir: y2 = W2 @ (W1 @ x + b1) + b2 = (W2@W1) @ x + (W2@b1 + b2)

Bu sadece **başka bir linear transform**! Kaç layer eklersen ekle, sonuç linear kalır.

Activation function **non-linearity** ekler ve model'in karmaşık pattern'ları öğrenmesini sağlar.
:::

```python
import numpy as np

# === Activation Functions ===

def sigmoid(z):
    """Range: (0, 1) -- Output layer'da binary classification"""
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1 - s)

def tanh(z):
    """Range: (-1, 1) -- Sigmoid'den daha iyi (zero-centered)"""
    return np.tanh(z)

def tanh_derivative(z):
    return 1 - np.tanh(z) ** 2

def relu(z):
    """Range: [0, inf) -- Hidden layer default. Hızlı, gradient vanishing yok."""
    return np.maximum(0, z)

def relu_derivative(z):
    return (z > 0).astype(float)

def leaky_relu(z, alpha=0.01):
    """ReLU'nun 'dying neuron' problemini çözer"""
    return np.where(z > 0, z, alpha * z)

def softmax(z):
    """Range: (0,1), toplam=1 -- Output layer'da multi-class classification"""
    exp_z = np.exp(z - np.max(z))  # numerical stability
    return exp_z / exp_z.sum(axis=-1, keepdims=True)

# Test
z = np.array([-3, -1, 0, 1, 3])
print("z:       ", z)
print("Sigmoid: ", np.round(sigmoid(z), 4))
print("Tanh:    ", np.round(tanh(z), 4))
print("ReLU:    ", relu(z))
print("LeakyReLU:", np.round(leaky_relu(z), 4))

# Softmax (multi-class)
logits = np.array([2.0, 1.0, 0.5, -1.0])
probs = softmax(logits)
print(f"\nSoftmax: {np.round(probs, 4)}, sum={probs.sum():.4f}")
```

:::comparison
## Activation Function Karşılaştırması

| Fonksiyon | Range | Kullanım | Avantaj | Dezavantaj |
|-----------|-------|----------|---------|------------|
| **ReLU** | [0, inf) | Hidden layers (default) | Hızlı, gradient vanishing yok | Dying neuron (negatifler hep 0) |
| **Leaky ReLU** | (-inf, inf) | Hidden layers | Dying neuron çözer | Ekstra hyperparameter (alpha) |
| **Sigmoid** | (0, 1) | Binary output | Olasılık çıktısı | Gradient vanishing, yavaş |
| **Tanh** | (-1, 1) | Hidden (bazen) | Zero-centered | Gradient vanishing |
| **Softmax** | (0, 1) sum=1 | Multi-class output | Olasılık dağılımı | Sadece output'ta |
| **GELU** | ~(-0.17, inf) | Transformers | Smooth ReLU, BERT/GPT | Hesaplama maliyeti |

**Pratik kural**: Hidden'da **ReLU**, binary output'ta **sigmoid**, multi-class output'ta **softmax** kullan.
:::

:::warning
## Gradient Vanishing Problem

Sigmoid ve tanh'ın türevi maksimum 0.25 ve 1.0. Derin ağlarda (10+ layer) chain rule ile çarpıla çarpıla gradient **neredeyse sıfır** olur.

Sonuç: İlk layer'lar hiçbir şey öğrenemez!

**Çözümler**:
1. ReLU kullan (türevi 1 veya 0)
2. Residual connections (ResNet) -- skip connection ile gradient akışı
3. Batch normalization -- her layer'ın çıktısını normalize et
4. Proper initialization (Xavier/He init)
:::

---

## 3. Multi-Layer Perceptron (MLP) -- Sıfırdan

### 3.1 Forward Pass

```python
import numpy as np

class NeuralNetwork:
    """2-layer neural network from scratch"""

    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):
        # Xavier initialization
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, output_size))
        self.lr = learning_rate

    def relu(self, z):
        return np.maximum(0, z)

    def relu_derivative(self, z):
        return (z > 0).astype(float)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def forward(self, X):
        """Forward pass: input -> hidden -> output"""
        # Hidden layer
        self.z1 = X @ self.W1 + self.b1         # Linear
        self.a1 = self.relu(self.z1)              # Activation

        # Output layer
        self.z2 = self.a1 @ self.W2 + self.b2   # Linear
        self.a2 = self.sigmoid(self.z2)           # Sigmoid for binary

        return self.a2

    def compute_loss(self, y_true, y_pred):
        """Binary cross-entropy loss"""
        eps = 1e-15
        y_pred = np.clip(y_pred, eps, 1 - eps)
        loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        return loss

    def backward(self, X, y_true):
        """Backward pass: gradients via chain rule
        NOT: Asagidaki formullerin sezgisel anlamini kavramak, ezberlemekten cok daha onemlidir.
        Framework'ler (PyTorch, TensorFlow) bu hesaplamalari autograd ile otomatik yapar.
        """
        m = X.shape[0]

        # Output layer gradients
        dz2 = self.a2 - y_true                    # dL/dz2
        dW2 = (1/m) * self.a1.T @ dz2            # dL/dW2
        db2 = (1/m) * np.sum(dz2, axis=0, keepdims=True)  # dL/db2

        # Hidden layer gradients (chain rule!)
        da1 = dz2 @ self.W2.T                     # dL/da1
        dz1 = da1 * self.relu_derivative(self.z1)  # dL/dz1
        dW1 = (1/m) * X.T @ dz1                   # dL/dW1
        db1 = (1/m) * np.sum(dz1, axis=0, keepdims=True)  # dL/db1

        # Gradient descent update
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1

    def train(self, X, y, epochs=1000, print_every=100):
        """Training loop"""
        y = y.reshape(-1, 1) if y.ndim == 1 else y
        losses = []

        for epoch in range(epochs):
            # Forward
            y_pred = self.forward(X)
            loss = self.compute_loss(y, y_pred)
            losses.append(loss)

            # Backward
            self.backward(X, y)

            if epoch % print_every == 0:
                accuracy = np.mean((y_pred >= 0.5) == y)
                print(f"Epoch {epoch}: loss={loss:.4f}, accuracy={accuracy:.4f}")

        return losses

    def predict(self, X):
        probs = self.forward(X)
        return (probs >= 0.5).astype(int)


# === XOR Problem -- MLP Çözer! ===
print("=== XOR with Neural Network ===")
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

nn = NeuralNetwork(input_size=2, hidden_size=8, output_size=1, learning_rate=0.5)
losses = nn.train(X, y, epochs=5000, print_every=1000)

print("\nXOR Results:")
for xi, yi in zip(X, y):
    pred = nn.forward(xi.reshape(1, -1))
    print(f"  {xi} -> {pred[0, 0]:.4f} (actual: {yi[0]})")

# === Daha Büyük Problem ===
print("\n=== Binary Classification ===")
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=500, noise=0.2, random_state=42)
y = y.reshape(-1, 1)

# Train/test split
split = 400
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

nn2 = NeuralNetwork(input_size=2, hidden_size=32, output_size=1, learning_rate=0.1)
losses = nn2.train(X_train, y_train, epochs=3000, print_every=500)

# Test accuracy
y_pred = nn2.predict(X_test)
accuracy = np.mean(y_pred == y_test)
print(f"\nTest accuracy: {accuracy:.4f}")
```

---

## 4. Loss Functions ve Optimizers

### 4.1 Loss Functions

```python
import numpy as np

# === Common Loss Functions ===

def mse_loss(y_true, y_pred):
    """Regression -- Mean Squared Error"""
    return np.mean((y_true - y_pred) ** 2)

def binary_cross_entropy(y_true, y_pred):
    """Binary Classification"""
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

def categorical_cross_entropy(y_true_onehot, y_pred):
    """Multi-class Classification"""
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(np.sum(y_true_onehot * np.log(y_pred), axis=1))

# Örnekler
y_true = np.array([1, 0, 1, 1])
y_pred_good = np.array([0.9, 0.1, 0.8, 0.95])  # İyi tahmin
y_pred_bad = np.array([0.2, 0.8, 0.3, 0.4])     # Kötü tahmin

print("Binary Cross-Entropy:")
print(f"  Good predictions: {binary_cross_entropy(y_true, y_pred_good):.4f}")
print(f"  Bad predictions:  {binary_cross_entropy(y_true, y_pred_bad):.4f}")

# Multi-class
y_true_multi = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # One-hot
y_pred_multi = np.array([[0.8, 0.1, 0.1], [0.1, 0.7, 0.2], [0.05, 0.15, 0.8]])
print(f"\nCategorical CE: {categorical_cross_entropy(y_true_multi, y_pred_multi):.4f}")
```

### 4.2 Optimizers

:::concept
## SGD vs Adam -- Hangisini Seç?

**SGD (Stochastic Gradient Descent)**:
- w = w - lr * gradient
- Basit ama yavaş, manual lr tuning gerekir

**SGD + Momentum**:
- Velocity = beta * velocity - lr * gradient
- w = w + velocity
- Oscillation'ı azaltır, "yuvarlanma" etkisi

**Adam (Adaptive Moment Estimation)**:
- Her weight için **ayrı learning rate** tutar
- Momentum (1st moment) + RMSprop (2nd moment)
- **Default seçim**: Çoğu durumda en iyi performans
- lr=0.001 ile başla

**AdamW**: Adam + Weight Decay (L2 regularization düzeltmesi)
- Transformer'larda standart optimizer
:::

```python
import numpy as np

class SGD:
    def __init__(self, lr=0.01):
        self.lr = lr

    def update(self, params, grads):
        for p, g in zip(params, grads):
            p -= self.lr * g

class SGDMomentum:
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.velocities = None

    def update(self, params, grads):
        if self.velocities is None:
            self.velocities = [np.zeros_like(p) for p in params]

        for i, (p, g) in enumerate(zip(params, grads)):
            self.velocities[i] = self.momentum * self.velocities[i] - self.lr * g
            p += self.velocities[i]

class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None  # 1st moment (mean)
        self.v = None  # 2nd moment (variance)
        self.t = 0

    def update(self, params, grads):
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]

        self.t += 1

        for i, (p, g) in enumerate(zip(params, grads)):
            # Update moments
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g**2

            # Bias correction
            m_hat = self.m[i] / (1 - self.beta1**self.t)
            v_hat = self.v[i] / (1 - self.beta2**self.t)

            # Update
            p -= self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)

# Demo: Optimizer karşılaştırması
def rosenbrock(x, y):
    """Meşhur optimizasyon test fonksiyonu"""
    return (1 - x)**2 + 100 * (y - x**2)**2

def rosenbrock_grad(x, y):
    dx = -2 * (1 - x) - 400 * x * (y - x**2)
    dy = 200 * (y - x**2)
    return np.array([dx, dy])

for opt_name, optimizer in [("SGD", SGD(lr=0.0001)),
                             ("Momentum", SGDMomentum(lr=0.0001, momentum=0.9)),
                             ("Adam", Adam(lr=0.01))]:
    params = [np.array([-1.0, -1.0])]
    for step in range(1000):
        grad = rosenbrock_grad(params[0][0], params[0][1])
        optimizer.update(params, [grad])

    x, y = params[0]
    loss = rosenbrock(x, y)
    print(f"{opt_name:>10}: x={x:.4f}, y={y:.4f}, loss={loss:.6f}")
```

---

## 5. Regularization Teknikleri

### 5.1 Dropout

:::concept
## Dropout -- Basit ama Etkili

Training sırasında her step'te rastgele nöronları **kapat** (çıktılarını 0 yap).

**Neden çalışır?**
- Model tek bir nöron yoluna bağımlı olmaz (co-adaptation önlenir)
- Ensemble etkisi: Her step farklı bir "sub-network" eğitilir
- Test'te tüm nöronlar açılır, ama çıktılar dropout oranıyla çarpılır (veya inverted dropout)

**Typical rate**: 0.2 - 0.5 (hidden layers), 0 (output layer)
:::

```python
import numpy as np

def dropout_forward(A, keep_prob=0.8, training=True):
    """
    Inverted dropout: Training'de 1/keep_prob ile çarp,
    test'te hiçbir şey yapma.
    """
    if not training or keep_prob == 1.0:
        return A, None

    mask = (np.random.rand(*A.shape) < keep_prob).astype(float)
    A_dropped = A * mask / keep_prob  # Inverted dropout
    return A_dropped, mask

# Demo
np.random.seed(42)
A = np.random.randn(3, 5)
print(f"Original:\n{A.round(3)}")

A_dropped, mask = dropout_forward(A, keep_prob=0.5, training=True)
print(f"\nAfter dropout (keep_prob=0.5):\n{A_dropped.round(3)}")
print(f"Mask:\n{mask}")
print(f"Active neurons: {mask.sum()}/{mask.size}")
```

### 5.2 Batch Normalization

:::concept
## Batch Normalization

Her layer'ın çıktısını **normalize** et (mean=0, std=1), sonra öğrenilebilir gamma ve beta ile scale/shift et.

**Faydaları**:
1. Training'i **hızlandırır** (daha büyük learning rate kullanılabilir)
2. **Internal covariate shift**'i azaltır
3. Hafif **regularization** etkisi (mini-batch istatistikleri gürültülü)
4. Initialization'a daha az hassas

**Formül**:
- mu = mean(x), sigma^2 = var(x) (batch üzerinden)
- x_hat = (x - mu) / sqrt(sigma^2 + eps)
- y = gamma * x_hat + beta (learnable parameters)
:::

```python
import numpy as np

class BatchNorm:
    def __init__(self, num_features, momentum=0.9, eps=1e-5):
        self.gamma = np.ones(num_features)    # Scale (learnable)
        self.beta = np.zeros(num_features)     # Shift (learnable)
        self.eps = eps
        self.momentum = momentum

        # Running stats for inference
        self.running_mean = np.zeros(num_features)
        self.running_var = np.ones(num_features)

    def forward(self, x, training=True):
        if training:
            batch_mean = x.mean(axis=0)
            batch_var = x.var(axis=0)

            # Normalize
            x_hat = (x - batch_mean) / np.sqrt(batch_var + self.eps)

            # Update running stats
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * batch_mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * batch_var
        else:
            # Use running stats for inference
            x_hat = (x - self.running_mean) / np.sqrt(self.running_var + self.eps)

        # Scale and shift
        return self.gamma * x_hat + self.beta

# Demo
np.random.seed(42)
x = np.random.randn(32, 10) * 5 + 3  # Batch of 32, 10 features

bn = BatchNorm(num_features=10)

# Before BN
print(f"Before BN: mean={x.mean(axis=0)[:3].round(3)}, std={x.std(axis=0)[:3].round(3)}")

# After BN
x_normalized = bn.forward(x, training=True)
print(f"After BN:  mean={x_normalized.mean(axis=0)[:3].round(3)}, std={x_normalized.std(axis=0)[:3].round(3)}")
```

---

## 6. Convolutional Neural Networks (CNN)

:::concept
## CNN -- Görüntü İşlemenin Kralı

CNN, spatial pattern'ları yakalamak için tasarlanmıştır. Normal MLP'den farkı:

1. **Convolutional Layer**: Küçük filtreler (kernel) resim üzerinde kayar, local pattern'ları (kenar, köşe, doku) öğrenir
2. **Pooling Layer**: Spatial boyutu küçültür (downsampling), computation azaltır
3. **Parameter Sharing**: Aynı filter tüm resmi tarar -- çok daha az parametre

**Mimari**: [Conv -> ReLU -> Pool] x N -> Flatten -> FC -> Output

**Uygulamalar**: Image classification, object detection, face recognition, medical imaging, autonomous driving
:::

```python
import numpy as np

def conv2d(image, kernel, stride=1, padding=0):
    """2D convolution (basitleştirilmiş)"""
    if padding > 0:
        image = np.pad(image, padding, mode='constant')

    h, w = image.shape
    kh, kw = kernel.shape
    out_h = (h - kh) // stride + 1
    out_w = (w - kw) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = image[i*stride:i*stride+kh, j*stride:j*stride+kw]
            output[i, j] = np.sum(region * kernel)  # Element-wise multiply + sum

    return output

def max_pool2d(image, pool_size=2, stride=2):
    """Max pooling"""
    h, w = image.shape
    out_h = (h - pool_size) // stride + 1
    out_w = (w - pool_size) // stride + 1

    output = np.zeros((out_h, out_w))

    for i in range(out_h):
        for j in range(out_w):
            region = image[i*stride:i*stride+pool_size, j*stride:j*stride+pool_size]
            output[i, j] = np.max(region)

    return output

# Demo: Edge detection
image = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
])

# Vertical edge detection kernel
vertical_kernel = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
])

# Horizontal edge detection kernel
horizontal_kernel = np.array([
    [-1, -1, -1],
    [ 0,  0,  0],
    [ 1,  1,  1]
])

vertical_edges = conv2d(image, vertical_kernel)
horizontal_edges = conv2d(image, horizontal_kernel)

print("Original image (7x7):")
print(image)
print(f"\nVertical edges (5x5):")
print(vertical_edges.astype(int))
print(f"\nHorizontal edges (5x5):")
print(horizontal_edges.astype(int))

# Max pooling
pooled = max_pool2d(vertical_edges, pool_size=2, stride=2)
print(f"\nAfter max pooling (2x2):")
print(pooled.astype(int))
```

### 6.1 CNN Parametreleri

:::tip
## CNN Boyut Hesaplama

**Conv layer output boyutu**:
- Output_size = (Input_size - Kernel_size + 2*Padding) / Stride + 1

**Örnek**: 28x28 input, 3x3 kernel, stride=1, padding=1
- Output = (28 - 3 + 2*1) / 1 + 1 = 28 (aynı boyut: "same" padding)

**Parametre sayısı hesaplama**:
- Conv layer: (kernel_h * kernel_w * in_channels + 1) * out_channels
- FC layer: (in_features + 1) * out_features

**Örnek**: 3x3 kernel, 32 input channel, 64 output channel
- Parameters = (3 * 3 * 32 + 1) * 64 = 18,496
:::

---

## 7. Recurrent Neural Networks (RNN) ve LSTM

:::concept
## RNN -- Sequential Veri İçin

RNN, **sıralı veri** (text, time series, audio) için tasarlanmıştır. Her adımda:
1. Mevcut input'u al (x_t)
2. Önceki hidden state'i al (h_{t-1})
3. Yeni hidden state hesapla: h_t = tanh(W_hh @ h_{t-1} + W_xh @ x_t + b)
4. Output hesapla: y_t = W_hy @ h_t + b_y

**Problem**: Vanilla RNN uzun bağımlılıkları öğrenemez (gradient vanishing/exploding).

**LSTM (Long Short-Term Memory)**: Gate mekanizması ile bu sorunu çözer:
- **Forget gate**: Neyi unutayım?
- **Input gate**: Neyi öğreneyim?
- **Output gate**: Neyi çıktı vereyim?
- **Cell state**: Uzun vadeli hafıza (gradient highway)
:::

```python
import numpy as np

class SimpleRNN:
    """Vanilla RNN implementation"""

    def __init__(self, input_size, hidden_size, output_size):
        # Xavier init
        scale = np.sqrt(2.0 / (input_size + hidden_size))
        self.Wxh = np.random.randn(input_size, hidden_size) * scale
        self.Whh = np.random.randn(hidden_size, hidden_size) * scale
        self.Why = np.random.randn(hidden_size, output_size) * scale
        self.bh = np.zeros((1, hidden_size))
        self.by = np.zeros((1, output_size))
        self.hidden_size = hidden_size

    def forward(self, X_seq):
        """
        X_seq: (seq_len, input_size)
        Returns: outputs (seq_len, output_size), hidden_states
        """
        seq_len = X_seq.shape[0]
        h = np.zeros((1, self.hidden_size))  # Initial hidden state
        outputs = []
        hidden_states = [h]

        for t in range(seq_len):
            x_t = X_seq[t:t+1]  # (1, input_size)

            # h_t = tanh(x_t @ Wxh + h_{t-1} @ Whh + bh)
            h = np.tanh(x_t @ self.Wxh + h @ self.Whh + self.bh)
            hidden_states.append(h)

            # y_t = h_t @ Why + by
            y = h @ self.Why + self.by
            outputs.append(y)

        return np.vstack(outputs), hidden_states

# Demo: Sequence pattern
print("=== Simple RNN Demo ===")
rnn = SimpleRNN(input_size=3, hidden_size=8, output_size=2)

# Simulated sequence (5 timesteps, 3 features)
X_seq = np.random.randn(5, 3)
outputs, hidden_states = rnn.forward(X_seq)

print(f"Input shape:  {X_seq.shape}")        # (5, 3)
print(f"Output shape: {outputs.shape}")       # (5, 2)
print(f"Hidden states: {len(hidden_states)}")  # 6 (including initial)

for t in range(5):
    print(f"  t={t}: hidden_norm={np.linalg.norm(hidden_states[t+1]):.4f}, "
          f"output={outputs[t].round(3)}")
```

```python
import numpy as np

class SimpleLSTM:
    """Simplified LSTM cell"""

    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        n = input_size + hidden_size

        # Gates: forget, input, cell_candidate, output
        self.Wf = np.random.randn(n, hidden_size) * 0.1
        self.Wi = np.random.randn(n, hidden_size) * 0.1
        self.Wc = np.random.randn(n, hidden_size) * 0.1
        self.Wo = np.random.randn(n, hidden_size) * 0.1

        self.bf = np.zeros((1, hidden_size))
        self.bi = np.zeros((1, hidden_size))
        self.bc = np.zeros((1, hidden_size))
        self.bo = np.zeros((1, hidden_size))

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def forward(self, X_seq):
        """Forward pass through sequence"""
        seq_len = X_seq.shape[0]
        h = np.zeros((1, self.hidden_size))
        c = np.zeros((1, self.hidden_size))  # Cell state (long-term memory)

        outputs = []

        for t in range(seq_len):
            x_t = X_seq[t:t+1]
            combined = np.hstack([h, x_t])  # Concatenate hidden + input

            # Forget gate: ne kadarını unutayım?
            f = self.sigmoid(combined @ self.Wf + self.bf)

            # Input gate: ne kadarını öğreneyim?
            i = self.sigmoid(combined @ self.Wi + self.bi)

            # Cell candidate: neyi öğreneyim?
            c_candidate = np.tanh(combined @ self.Wc + self.bc)

            # Cell state update
            c = f * c + i * c_candidate  # Unutulanı sil + yeniyi ekle

            # Output gate: neyi çıktı vereyim?
            o = self.sigmoid(combined @ self.Wo + self.bo)

            # Hidden state
            h = o * np.tanh(c)
            outputs.append(h)

        return np.vstack(outputs), h, c

# Demo
print("=== LSTM Demo ===")
lstm = SimpleLSTM(input_size=3, hidden_size=8)
X_seq = np.random.randn(10, 3)  # 10 timestep, 3 feature

outputs, final_h, final_c = lstm.forward(X_seq)
print(f"Output shape: {outputs.shape}")   # (10, 8)
print(f"Final hidden: {final_h.shape}")   # (1, 8)
print(f"Cell state:   {final_c.shape}")   # (1, 8)
```

---

## 8. PyTorch ve TensorFlow Temelleri

### 8.1 PyTorch

```python
# PyTorch ile neural network (en popüler research framework)
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Veri hazırla
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np

X, y = make_classification(n_samples=1000, n_features=20, n_informative=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# NumPy -> PyTorch Tensor
X_train_t = torch.FloatTensor(X_train)
y_train_t = torch.FloatTensor(y_train).unsqueeze(1)
X_test_t = torch.FloatTensor(X_test)
y_test_t = torch.FloatTensor(y_test).unsqueeze(1)

# DataLoader (mini-batch)
train_dataset = TensorDataset(X_train_t, y_train_t)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Model tanımla
class BinaryClassifier(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.3),

            nn.Linear(64, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Dropout(0.2),

            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)

# Model, loss, optimizer
model = BinaryClassifier(input_size=20)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
print("=== PyTorch Training ===")
for epoch in range(50):
    model.train()
    epoch_loss = 0

    for X_batch, y_batch in train_loader:
        # Forward pass
        y_pred = model(X_batch)
        loss = criterion(y_pred, y_batch)

        # Backward pass
        optimizer.zero_grad()  # Gradient'leri sıfırla
        loss.backward()        # Backpropagation
        optimizer.step()       # Weight update

        epoch_loss += loss.item()

    if epoch % 10 == 0:
        # Evaluation
        model.eval()
        with torch.no_grad():
            y_test_pred = model(X_test_t)
            test_loss = criterion(y_test_pred, y_test_t)
            accuracy = ((y_test_pred >= 0.5) == y_test_t).float().mean()
            print(f"Epoch {epoch}: train_loss={epoch_loss/len(train_loader):.4f}, "
                  f"test_loss={test_loss:.4f}, accuracy={accuracy:.4f}")
```

### 8.2 TensorFlow/Keras

```python
# TensorFlow/Keras ile aynı model (production ve deployment favori)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# Aynı veriyi kullan (sklearn'den)
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000, n_features=20, n_informative=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model tanımla (Sequential API)
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(20,)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),

    layers.Dense(32, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.2),

    layers.Dense(1, activation='sigmoid')
])

# Compile
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Model summary
model.summary()

# Training
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=1
)

# Evaluation
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"\nTest Accuracy: {test_accuracy:.4f}")
```

:::comparison
## PyTorch vs TensorFlow

| Özellik | PyTorch | TensorFlow/Keras |
|---------|---------|-----------------|
| **Approach** | Dynamic graph (eager) | Static graph (Keras: eager) |
| **Research** | Akademik standart | Azalıyor |
| **Production** | TorchServe, ONNX | TF Serving, TF Lite, TF.js |
| **Debugging** | Kolay (Python debugger) | Orta |
| **Mobile** | PyTorch Mobile | TF Lite (daha olgun) |
| **Öğrenme** | Pythonic, anlaşılır | Keras ile kolay |
| **Community** | Hızla büyüyor | Büyük ama yavaşlıyor |
| **Tavsiye** | Yeni projeler, araştırma | Existing TF projeleri, edge |
:::

---

## 9. Tüm Kavramları Birleştiren Özet

:::deha-tip
## Deha İpucu: Deep Learning Debugging Checklist

Model çalışmıyorsa sırayla kontrol et:

1. **Veri doğru mu?** Bir batch'i gözle kontrol et. Label'lar doğru mu?
2. **Loss düşüyor mu?** İlk birkaç epoch'ta loss azalmalı. Azalmıyorsa lr çok büyük/küçük.
3. **Overfit yapabiliyor mu?** Küçük bir veri parçasına overfit yap (train loss ~0). Yapamazsa model yetersiz veya bug var.
4. **Gradient'ler sağlıklı mı?** `grad.norm()` çok büyük (exploding) veya sıfır (vanishing) mı?
5. **Learning rate doğru mu?** LR finder ile optimal aralığı bul.
6. **Batch size etkisi?** Küçük batch: gürültülü ama generalize eder. Büyük batch: stabil ama local minima'ya takılabilir.
7. **Regularization?** Train iyi, test kötü --> overfit --> Dropout artır, data augmentation ekle.
:::

:::english
## Technical Terms Glossary

| English | Türkçe Açıklama |
|---------|-----------------|
| **Perceptron** | Tek nöronluk yapay sinir ağı, binary classification |
| **Activation Function** | Non-linearity ekleyen fonksiyon (ReLU, sigmoid, softmax) |
| **Backpropagation** | Chain rule ile gradient'lerin geriye yayılması |
| **Forward Pass** | Input'tan output'a hesaplama |
| **Loss Function** | Tahmin hatası ölçüm fonksiyonu |
| **Optimizer** | Weight'leri güncelleyen algoritma (SGD, Adam) |
| **Dropout** | Rastgele nöron kapatarak regularization |
| **Batch Normalization** | Layer çıktılarını normalize etme |
| **Convolutional Layer** | Spatial pattern yakalayan filtre tabanlı layer |
| **Pooling** | Spatial boyut küçültme (max/average) |
| **Kernel/Filter** | CNN'de kullanılan küçük ağırlık matrisi |
| **Hidden State** | RNN'de adımlar arası taşınan bilgi |
| **Cell State** | LSTM'de uzun vadeli hafıza |
| **Gate** | LSTM'de bilgi akışını kontrol eden mekanizma |
| **Gradient Vanishing** | Derin ağlarda gradient'in sıfıra yaklaşması |
| **Weight Initialization** | Ağırlıkların başlangıç değeri (Xavier, He) |
:::

:::knowledge-check
## Bilgi Kontrolü

1. Activation function olmazsa birden fazla layer'ın avantajı ne olur?
2. ReLU'nun sigmoid'e göre en büyük avantajı nedir?
3. Dropout training'de 0.5 oranıyla uygulanıyorsa, test'te ne yapılır?
4. CNN'de bir 5x5 kernel, 1 stride, 0 padding ile 28x28 image'a convolution yapılırsa output boyutu ne olur?
5. LSTM'in vanilla RNN'e göre avantajı nedir?
:::

:::exercise
### Alistirma 1: NumPy ile Basit Neural Network (Kolay)

Sadece NumPy kullanarak 2 katmanli bir neural network implement et ve XOR problemini coz.

```python
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# XOR dataset
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# TODO: Rastgele agirliklar baslat
np.random.seed(42)
weights_input_hidden = np.random.randn(2, 4) * 0.5  # 2 input -> 4 hidden
weights_hidden_output = np.random.randn(4, 1) * 0.5  # 4 hidden -> 1 output
bias_hidden = np.zeros((1, 4))
bias_output = np.zeros((1, 1))

learning_rate = 0.5

for epoch in range(10000):
    # TODO: Forward pass
    hidden = sigmoid(X @ weights_input_hidden + bias_hidden)
    output = sigmoid(hidden @ weights_hidden_output + bias_output)

    # TODO: Loss hesapla (MSE)
    loss = np.mean((y - output) ** 2)

    # TODO: Backward pass (gradient hesapla)
    output_error = y - output
    output_delta = output_error * sigmoid_derivative(output)

    hidden_error = output_delta @ weights_hidden_output.T
    hidden_delta = hidden_error * sigmoid_derivative(hidden)

    # TODO: Agirliklari guncelle
    weights_hidden_output += hidden.T @ output_delta * learning_rate
    weights_input_hidden += X.T @ hidden_delta * learning_rate

    if epoch % 1000 == 0:
        print(f"Epoch {epoch}: Loss = {loss:.6f}")

# Test
print(f"\nTahminler:")
for i in range(4):
    print(f"  {X[i]} -> {output[i][0]:.4f} (beklenen: {y[i][0]})")
```

**Beklenen Sonuc:** 10000 epoch'ta loss 0.01'in altina dusmeli. XOR ciktilari 0 ve 1'e yakin olmali (0.05'ten kucuk veya 0.95'ten buyuk).
**Ipucu:** XOR lineer olarak ayrilamaz, bu yuzden en az 1 hidden layer gerekir. Sigmoid aktivasyonu ciktiyi 0-1 arasina sikitirir.

---

### Alistirma 2: PyTorch ile MNIST Classifier (Orta)

PyTorch kullanarak el yazisi rakam siniflandirici egit. CNN mimarisi kullan.

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Data loading
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])

train_dataset = datasets.MNIST("./data", train=True, download=True, transform=transform)
test_dataset = datasets.MNIST("./data", train=False, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000)

# TODO: CNN modeli tanimla
class MNISTClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # TODO: Conv2D(1, 32, 3) -> ReLU -> MaxPool(2)
        # TODO: Conv2D(32, 64, 3) -> ReLU -> MaxPool(2)
        # TODO: Flatten -> Linear(64*5*5, 128) -> ReLU -> Linear(128, 10)
        pass

    def forward(self, x):
        # TODO: Forward pass
        pass

model = MNISTClassifier()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# TODO: Egitim dongusu (5 epoch yeterli)
for epoch in range(5):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    # TODO: Test accuracy hesapla
    model.eval()
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()

    accuracy = 100. * correct / len(test_dataset)
    print(f"Epoch {epoch+1}: Test Accuracy = {accuracy:.2f}%")
```

**Beklenen Sonuc:** 5 epoch'ta test accuracy %98+ olmali. CNN modeli dogru boyutlarda tanimlanmali. Loss her epoch'ta azalmali.
**Ipucu:** Conv2D cikis boyutu: (input_size - kernel_size + 2*padding) / stride + 1. MaxPool boyutu yarilatirir.

---

### Alistirma 3: Model Analizi ve Confusion Matrix (Zor)

Egitilmis modeli analiz et: confusion matrix, yanlis tahminler ve model karmasikligi.

```python
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

# TODO: Test seti uzerinde tum tahminleri topla
model.eval()
all_preds = []
all_targets = []

with torch.no_grad():
    for data, target in test_loader:
        output = model(data)
        preds = output.argmax(dim=1)
        all_preds.extend(preds.numpy())
        all_targets.extend(target.numpy())

# TODO: Classification report yazdir
print(classification_report(all_targets, all_preds))

# TODO: Confusion matrix gorsellistir
cm = confusion_matrix(all_targets, all_preds)
plt.figure(figsize=(10, 8))
plt.imshow(cm, cmap="Blues")
plt.colorbar()
plt.xlabel("Tahmin")
plt.ylabel("Gercek")
plt.title("Confusion Matrix")
# Her hucreye sayiyi yaz
for i in range(10):
    for j in range(10):
        plt.text(j, i, str(cm[i, j]), ha="center", va="center")
plt.show()

# TODO: En cok karistirilan rakam ciftini bul
# Hint: cm'de diagonal disindaki en buyuk deger

# TODO: Yanlis tahmin edilen 10 ornegi goster
wrong_idx = [i for i in range(len(all_preds)) if all_preds[i] != all_targets[i]]
fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for idx, ax in zip(wrong_idx[:10], axes.flatten()):
    img = test_dataset[idx][0].squeeze()
    ax.imshow(img, cmap="gray")
    ax.set_title(f"Gercek: {all_targets[idx]}, Tahmin: {all_preds[idx]}")
    ax.axis("off")
plt.tight_layout()
plt.show()

# TODO: Model parametre sayisini hesapla
total_params = sum(p.numel() for p in model.parameters())
print(f"Toplam parametre: {total_params:,}")
```

**Beklenen Sonuc:** Confusion matrix'te diagonal degerler yuksek olmali. En cok karistirilan cift genelde (3,5) veya (4,9) olur. Yanlis tahmin örneklerinde el yazisinin zor okunabilir oldugu gorulebilir.
**Ipucu:** `classification_report` precision, recall ve F1-score'u sinif bazinda gosterir. Dusuk recall'lu siniflar modelin zorluk cektigi rakamlari gosterir.

---

### Alistirma 4: Backpropagation Sifirdan (Kolay)

Chain rule ile gradient hesaplamasini elle uygula ve autograd ile dogrula.

```python
import numpy as np

# Basit 2-layer network (sifirdan)
class SimpleNet:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros(hidden_size)
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros(output_size)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    def backward(self, X, y, output):
        m = X.shape[0]
        # Output layer gradient
        dz2 = output - y
        dW2 = (1/m) * self.a1.T @ dz2
        db2 = (1/m) * np.sum(dz2, axis=0)

        # Hidden layer gradient (chain rule)
        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.a1 * (1 - self.a1)
        dW1 = (1/m) * X.T @ dz1
        db1 = (1/m) * np.sum(dz1, axis=0)

        return dW1, db1, dW2, db2

    # TODO: Training loop yaz (forward + backward + weight update)
    # TODO: XOR problemini coz (non-linear)
    # TODO: Loss history ciz ve convergence'i gozlemle
    # TODO: PyTorch autograd ile gradient'leri dogrula

net = SimpleNet(2, 4, 1)
```

**Beklenen Sonuc:** XOR problemi %95+ accuracy ile cozulmeli. Elle hesaplanan gradient'ler PyTorch autograd ile uyusmali.
**Ipucu:** XOR lineer olarak ayrilamaz — en az 1 hidden layer gerektirir. Bu derin ogrenmenin temel motivasyonudur.

---

### Alistirma 5: CNN ile Goruntu Siniflandirma (Kolay)

CIFAR-10 üzerinde basit bir CNN modeli egit.

```python
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

# Data augmentation ve normalizasyon
transform_train = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Dropout(0.5), nn.Linear(128, 10)
        )

    def forward(self, x):
        return self.classifier(self.features(x))

# TODO: Model egit (10 epoch, Adam optimizer, CrossEntropyLoss)
# TODO: Train ve validation accuracy grafigi ciz
# TODO: Yanlis siniflandirilan ornekleri gorsellestir
# TODO: Data augmentation olmadan egit ve farki gozlemle
```

**Beklenen Sonuc:** CIFAR-10'da %85+ test accuracy elde edilmeli. Data augmentation ile %3-5 accuracy artisi olmali. BatchNorm training'i hizlandirmali.
**Ipucu:** Conv layer filtreleri kenar, doku gibi low-level feature'lari, derin katmanlar nesne parcalarini ogrenrir.

---

### Alistirma 6: Overfitting Tespiti ve Onleme (Orta)

Kasitli olarak overfit eden bir model oluştur ve duzelltme tekniklerini uygula.

```python
import torch
import torch.nn as nn

# Kucuk veri seti ile kasitli overfitting
X_train = torch.randn(50, 10)
y_train = torch.randint(0, 2, (50,))
X_test = torch.randn(200, 10)
y_test = torch.randint(0, 2, (200,))

# Asiri buyuk model (overfit edecek)
class OverfitNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 256), nn.ReLU(),
            nn.Linear(256, 256), nn.ReLU(),
            nn.Linear(256, 256), nn.ReLU(),
            nn.Linear(256, 2)
        )

    def forward(self, x):
        return self.net(x)

# Regularized model
class RegularizedNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 64), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(64, 32), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        return self.net(x)

# TODO: Her iki modeli 200 epoch egit
# TODO: Train vs Test loss grafigi ciz (overfitting gorsel)
# TODO: Early stopping implement et
# TODO: L2 regularization ekle (weight_decay parametresi)
# TODO: Model boyutu vs overfitting iliskisini analiz et
```

**Beklenen Sonuc:** OverfitNet'te train accuracy %100, test accuracy dusuk olmali. RegularizedNet'te gap cok daha kucuk olmali. Early stopping ile optimal epoch bulunmali.
**Ipucu:** Train loss duserken test loss artiyorsa = overfitting. Dropout, weight decay, early stopping, data augmentation ve daha kucuk model kullan.

---

### Alistirma 7: Transfer Learning ile Ozel Veri Seti (Orta)

Pre-trained ResNet modeli ile kendi veri setinde siniflandirma yap.

```python
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import os

# Pre-trained ResNet18 yukle
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# Son katmani degistir (kendi sinif sayina gore)
num_classes = 3  # ornek: kedi, kopek, kus
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Feature extractor olarak kullan (sadece son katmani egit)
for param in model.parameters():
    param.requires_grad = False
model.fc.requires_grad_(True)

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# TODO: Custom Dataset class'i yaz (klasor yapisinden veri yukle)
# TODO: Feature extraction mode ile egit (hizli, 5 epoch yeterli)
# TODO: Fine-tuning mode ile egit (tum katmanlar, dusuk lr)
# TODO: Feature extraction vs fine-tuning performansini karsilastir
# TODO: Grad-CAM ile modelin neye baktigini gorseellestir
```

**Beklenen Sonuc:** Transfer learning ile kucuk veri setinde bile %90+ accuracy elde edilmeli. Feature extraction 10x daha hizli egitilmeli. Fine-tuning %2-5 daha iyi sonuc vermeli.
**Ipucu:** ImageNet'te egitilmis modeller genel gorsel feature'lari (kenar, doku, sekil) zaten ogrenmis. Kendi veri setinde sadece son katmanlari egitmek yeterli.

---

### Alistirma 8: RNN/LSTM ile Metin Siniflandirma (Orta)

LSTM ile sentiment analizi modeli egit.

```python
import torch
import torch.nn as nn
from torchtext.datasets import IMDB
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

tokenizer = get_tokenizer("basic_english")

class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim=128, hidden_dim=256, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=num_layers,
                           batch_first=True, dropout=0.3, bidirectional=True)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, 64),  # bidirectional -> 2x hidden
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # Son hidden state'leri birlestir (forward + backward)
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.classifier(hidden)

# TODO: IMDB dataset'ini yukle ve tokenize et
# TODO: Vocabulary olustur ve text'leri numerik index'lere cevir
# TODO: Padding ile batch olustur (pad_sequence)
# TODO: Model egit ve test accuracy raporla
# TODO: Ornek cumlelerle sentiment tahmini yap
```

**Beklenen Sonuc:** IMDB'de %85+ test accuracy elde edilmeli. Bidirectional LSTM tek yonlu LSTM'den daha iyi sonuc vermeli.
**Ipucu:** LSTM vanishing gradient problemini cozer (forget gate ile). Bidirectional hem soldan saga hem sagdan sola kontekst okur.

---

### Alistirma 9: Hyperparameter Tuning ile Model Optimizasyonu (Zor)

Sistematik hyperparameter arama ile en iyi model konfigurasyonunu bul.

```python
import torch
import torch.nn as nn
import optuna

def objective(trial):
    # Hyperparameter'lari tanimla
    lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)
    hidden_size = trial.suggest_categorical("hidden_size", [64, 128, 256, 512])
    num_layers = trial.suggest_int("num_layers", 1, 4)
    dropout = trial.suggest_float("dropout", 0.1, 0.5)
    batch_size = trial.suggest_categorical("batch_size", [32, 64, 128])
    optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "AdamW", "SGD"])

    # Model olustur
    layers = []
    in_features = 784  # MNIST
    for i in range(num_layers):
        layers.extend([
            nn.Linear(in_features, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
        ])
        in_features = hidden_size
    layers.append(nn.Linear(hidden_size, 10))
    model = nn.Sequential(*layers)

    # Optimizer sec
    if optimizer_name == "Adam":
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    elif optimizer_name == "AdamW":
        optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    else:
        optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9)

    # TODO: Training loop yaz
    # TODO: Validation accuracy'yi return et (Optuna minimize/maximize eder)
    # TODO: Early pruning ekle (trial.report + trial.should_prune)
    # TODO: En iyi 5 trial'i raporla

    return val_accuracy

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
print(f"En iyi parametreler: {study.best_params}")
print(f"En iyi skor: {study.best_value:.4f}")

# TODO: Optuna visualization ile parametre onemini gor
# TODO: En iyi model ile test seti uzerinde final evaluation yap
```

**Beklenen Sonuc:** Optuna 50 trial'da en iyi hyperparameter kombinasyonunu bulmali. Learning rate ve dropout en onemli parametreler olmali. Final model %98+ MNIST accuracy'si elde etmeli.
**Ipucu:** `log=True` ile learning rate logaritmik olcekte aranir (1e-5 ile 1e-2 arasi). Pruning ile kotu trial'lar erken sonlandirilir.

---

### Alistirma 10: Model Deployment — PyTorch to ONNX (Zor)

Egitilmis modeli ONNX formatina cevirip inference pipeline oluştur.

```python
import torch
import torch.nn as nn
import onnx
import onnxruntime as ort
import numpy as np

# Egitilmis model (ornek)
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 10)
        )

    def forward(self, x):
        return self.net(x)

model = SimpleModel()
model.eval()

# ONNX'e cevir
dummy_input = torch.randn(1, 784)
torch.onnx.export(
    model, dummy_input, "model.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)

# ONNX Runtime ile inference
session = ort.InferenceSession("model.onnx")
input_data = np.random.randn(1, 784).astype(np.float32)
result = session.run(None, {"input": input_data})
print(f"Prediction: {np.argmax(result[0])}")

# TODO: PyTorch ve ONNX Runtime ciktilarini karsilastir (fark < 1e-5)
# TODO: Batch inference performansini olc (100 ornek)
# TODO: Quantization uygula (INT8) ve boyut/hiz karsilastirmasi yap
# TODO: FastAPI ile basit inference API olustur
```

**Beklenen Sonuc:** ONNX modeli PyTorch ile ayni sonuclari vermeli. ONNX Runtime inference %30-50 daha hizli olmali. INT8 quantization ile model boyutu %50-75 kuculmeli.
**Ipucu:** ONNX platform bagimsizdir — PyTorch modeli TensorFlow, C++ veya JavaScript'te çalıştırilabilir. Production'da ONNX Runtime tercih edilir.
:::

:::exercise
### Alistirma 11: Perceptron'dan MLP'ye (Kolay)

Sifirdan basit bir perceptron ve MLP yaz.

```python
import numpy as np

class Perceptron:
    def __init__(self, n_features):
        self.weights = np.random.randn(n_features)
        self.bias = 0.0
        self.lr = 0.01

    def predict(self, x):
        return 1 if np.dot(self.weights, x) + self.bias > 0 else 0

    # TODO: fit metodunu yaz (perceptron learning rule)
    # TODO: AND, OR, XOR gate'leri ogren
    # TODO: XOR'un neden ogrenilemedigini acikla (linear separability)
    # TODO: 2-layer MLP ile XOR'u coz
```

**Beklenen Sonuc:** Perceptron AND ve OR'u ogrenmeli ama XOR'u ogrenmemeli. MLP ile XOR cozulmeli.
**Ipucu:** XOR linearly separable degildir — tek katman cozmez. Hidden layer ekleyince non-linear karar siniri olusur.
:::

:::exercise
### Alistirma 12: Activation Function Karsilastirmasi (Kolay)

Farkli activation function'lari gorsel olarak karsilastir.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 100)

# TODO: Asagidaki activation'lari implement et ve ciz
# 1. Sigmoid: 1 / (1 + exp(-x))
# 2. Tanh: (exp(x) - exp(-x)) / (exp(x) + exp(-x))
# 3. ReLU: max(0, x)
# 4. Leaky ReLU: max(0.01x, x)
# 5. GELU: x * phi(x) (phi = standard normal CDF)

# TODO: Her birinin turevini de ciz
# TODO: Vanishing gradient problemini sigmoid ile goster
# TODO: Dead neuron problemini ReLU ile goster
# TODO: Her activation'in ne zaman kullanilacagini yaz
```

**Beklenen Sonuc:** 5 activation ve turevleri cizilmeli. Avantaj/dezavantajlari listelemeli.
**Ipucu:** Modern NN'lerde: hidden layer'da ReLU/GELU, output'ta sigmoid (binary) veya softmax (multi-class).
:::

:::exercise
### Alistirma 13: Loss Function Secimi (Kolay)

Farkli loss function'lari anla ve dogru secimi yap.

```python
import numpy as np

# TODO: Binary Cross-Entropy Loss
# BCE = -[y*log(p) + (1-y)*log(1-p)]
def bce_loss(y_true, y_pred):
    eps = 1e-7
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# TODO: Categorical Cross-Entropy Loss
# TODO: Mean Squared Error (MSE)
# TODO: Mean Absolute Error (MAE)

# TODO: Karsilastirma tablosu olustur:
# | Loss Function | Gorev           | Aktivasyon |
# |---------------|-----------------|------------|
# | BCE           | Binary class.   | Sigmoid    |
# | CCE           | Multi class.    | Softmax    |
# | MSE           | Regression      | Linear     |

# TODO: Her loss'un gradient'ini hesapla
```

**Beklenen Sonuc:** 4 loss function implement edilmeli. Karsilastirma tablosu doldurulmali.
**Ipucu:** Yanlis loss secimi model'in ogrenmesini engeller. Classification'da MSE kullanma — gradient cok yavas olur.
:::

:::exercise
### Alistirma 14: PyTorch ile Basit NN Egitimi (Orta)

PyTorch ile basit bir neural network egit.

```python
import torch
import torch.nn as nn
import torch.optim as optim

# TODO: Model tanimla
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x

# TODO: Veri hazirla (synthetic binary classification)
# TODO: Loss function ve optimizer sec
# criterion = nn.BCELoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)

# TODO: Egitim dongusu yaz (100 epoch)
# TODO: Train ve validation loss'u ciz
# TODO: Overfitting kontrolu yap
```

**Beklenen Sonuc:** Model egitilmeli ve loss azalmali. Train/val loss grafigi cizilmeli.
**Ipucu:** `model.train()` ve `model.eval()` modlarini dogru kullan. Eval modda dropout ve batchnorm farkli davranir.
:::

:::exercise
### Alistirma 15: Batch Normalization ve Dropout (Orta)

BatchNorm ve Dropout'un etkisini gozlemle.

```python
import torch.nn as nn

# TODO: BatchNorm'lu ve Dropout'lu model
class RegularizedNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        return self.layers(x)

# TODO: BatchNorm'suz ve Dropout'suz model egit
# TODO: BatchNorm'lu model egit
# TODO: Dropout'lu model egit
# TODO: Her ikisi ile model egit
# TODO: 4 modelin train/val loss grafiklerini karsilastir
```

**Beklenen Sonuc:** BatchNorm egitimi hizlandirmali. Dropout overfitting'i azaltmali. Ikisi birlikte en iyi sonucu vermeli.
**Ipucu:** BatchNorm: her layer'in ciktisini normalize eder (mean=0, std=1). Dropout: rastgele neuron'lari kapatir (ensemble etkisi).
:::

:::exercise
### Alistirma 16: CNN ile Goruntu Siniflandirma (Orta)

Convolutional Neural Network ile MNIST/CIFAR siniflandirmasi yap.

```python
import torch.nn as nn

# TODO: CNN modeli tanimla
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.fc_layers = nn.Sequential(
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        return self.fc_layers(x)

# TODO: MNIST veri setini yukle (torchvision)
# TODO: Data augmentation ekle (RandomRotation, RandomFlip)
# TODO: Modeli egit ve test accuracy hesapla
# TODO: Yanlis siniflandirilan ornekleri gorsellestir
```

**Beklenen Sonuc:** MNIST'te %98+ accuracy elde edilmeli. Data augmentation etkisi gosterilmeli.
**Ipucu:** Conv layer feature extractor, FC layer classifier gorevi gorur. MaxPool spatial boyutu yarisina indirir.
:::

:::exercise
### Alistirma 17: Transfer Learning Uygulama (Orta)

Pre-trained model ile transfer learning yap.

```python
import torchvision.models as models
import torch.nn as nn

# TODO: Pre-trained ResNet yukle
# model = models.resnet18(pretrained=True)

# TODO: Son layer'i degistir (fine-tuning)
# num_features = model.fc.in_features
# model.fc = nn.Linear(num_features, num_classes)

# TODO: Feature extraction (sadece son layer egit)
# for param in model.parameters():
#     param.requires_grad = False
# model.fc.requires_grad_(True)

# TODO: Full fine-tuning (tum model egit, dusuk lr ile)
# TODO: Feature extraction vs fine-tuning performansini karsilastir
# TODO: Learning rate scheduling ekle
```

**Beklenen Sonuc:** Transfer learning az veri ile yuksek accuracy saglamali. Fine-tuning feature extraction'dan daha iyi olmali.
**Ipucu:** Az veri varsa feature extraction, cok veri varsa fine-tuning tercih et. Pre-trained model'in ilk katmanlarini dondurmak (freeze) genellikle yeterli.
:::

:::exercise
### Alistirma 18: RNN/LSTM ile Sequence Modelleme (Zor)

Recurrent Neural Network ile metin veya zaman serisi modelleme yap.

```python
import torch.nn as nn

# TODO: LSTM modeli tanimla
class LSTMModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, output_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)

    def forward(self, x):
        embedded = self.embedding(x)
        output, (hidden, cell) = self.lstm(embedded)
        hidden = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.fc(hidden)

# TODO: Sentiment analysis veri seti hazirla
# TODO: Tokenizer ve vocabulary olustur
# TODO: Modeli egit
# TODO: Vanishing gradient problemini goster (simple RNN vs LSTM)
```

**Beklenen Sonuc:** LSTM sentiment analysis'te %85+ accuracy vermeli. RNN vs LSTM farki gosterilmeli.
**Ipucu:** LSTM'in gate mekanizmasi (forget, input, output) uzun mesafe bagimliligini ogrenebilir. Bidirectional LSTM her iki yonden context yakalar.
:::

:::exercise
### Alistirma 19: Model Optimization ve Deployment (Zor)

Model'i production icin optimize et: quantization, pruning, ONNX export.

```python
import torch
# TODO: Model quantization
# quantized_model = torch.quantization.quantize_dynamic(
#     model, {nn.Linear}, dtype=torch.qint8
# )

# TODO: Model boyutunu karsilastir
# original_size = os.path.getsize('model.pt')
# quantized_size = os.path.getsize('model_quantized.pt')

# TODO: ONNX export
# dummy_input = torch.randn(1, input_size)
# torch.onnx.export(model, dummy_input, 'model.onnx')

# TODO: ONNX Runtime ile inference
# import onnxruntime as ort
# session = ort.InferenceSession('model.onnx')

# TODO: Inference speed karsilastirmasi (PyTorch vs ONNX vs Quantized)
# TODO: Model pruning uygula ve accuracy etkisini olc
```

**Beklenen Sonuc:** Quantization ile model %50-75 kuculmeli. ONNX ile %30+ hizlanma saglanmali. Accuracy kaybi minimal olmali.
**Ipucu:** INT8 quantization accuracy'den cok az kayip ile model boyutunu 4x kucultebilir. ONNX Runtime production'da standart.
:::


:::deha-tip
## Pratik Gerceklik: Senior'lar Backpropagation Formullerini Ezberlemez

Gercek dunyada:
- **Framework'ler** (PyTorch, TensorFlow) otomatik turev hesaplar (autograd)
- **Transfer learning** ile sifirdan model egitmezsin — pre-trained model kullanirsin
- **Onemli olan**: Hangi mimariyi (CNN, RNN, Transformer) hangi problem icin sectigin
- **Pratik skill**: Hyperparameter tuning, overfitting tespiti, data augmentation

Mulakatta "backpropagation'i acikla" sorusuna: "Gradient'lerin chain rule ile geriye yayilmasi. Framework'ler bunu otomatik yapar ama loss fonksiyonunun gradient'inin her katmana nasil aktarildigini anlamak, debugging ve model optimizasyonu icin onemli" de.
:::


:::external-resource
## Ek Kaynaklar

- [3Blue1Brown - Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) -- Görsel deep learning
- [Deep Learning Book (Goodfellow)](https://www.deeplearningbook.org/) -- Ücretsiz kitap, kapsamlı teori
- [PyTorch Official Tutorials](https://pytorch.org/tutorials/) -- Başlangıçtan ileri seviyeye
- [TensorFlow Playground](https://playground.tensorflow.org/) -- Tarayıcıda NN eğit
- [CS231n Stanford - CNN for Visual Recognition](http://cs231n.stanford.edu/) -- Efsane ders
- [Andrej Karpathy - Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) -- YouTube serisi
:::
