---
title: "Transformers ve Modern AI"
id: mod-16-deep-learning/lesson-02
estimated_minutes: 90
order: 2
tags: [transformers, attention, self-attention, bert, gpt, vision-transformer, transfer-learning, fine-tuning, hugging-face]
prerequisites: [mod-16-deep-learning/lesson-01]
---

# Transformers ve Modern AI

2017'de yayınlanan "Attention Is All You Need" paper'ı, AI tarihini değiştirdi. RNN/LSTM'in sequential limitation'larını aşan **Transformer** mimarisi, bugün GPT, BERT, DALL-E, Stable Diffusion ve daha birçok modelin temelini oluşturuyor. Bu derste attention mechanism'dan Hugging Face kullanımına kadar modern AI'ın temellerini öğreneceksin.

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "Transformer mimarisindeki Self-Attention mekanizmasini adim adim acikla. Q (Query), K (Key), V (Value) matrix'leri nasil olusturulur? Scaled Dot-Product Attention formulundeki her islemi (QK^T, scaling, softmax, V carpimi) orneklerle goster. Multi-Head Attention neden tek head'den daha iyi?"

**2. Pratik Uygulama:**
> "Hugging Face Transformers kutuphanesi ile bir metin siniflandirma modeli egit. Pre-trained BERT modelini yukle, kendi dataset'ine fine-tune et (Trainer API ile). Tokenization, padding, attention mask kavramlarini acikla. Model performansini evaluate et ve inference pipeline olustur."
> Takip: "Simdi Vision Transformer (ViT) ile bir goruntu siniflandirma modeli egit. CNN ile performans karsilastirmasi yap."

**3. Mukemmellik Icin:**
> "GPT ve BERT mimarilerini karsilastir: encoder-only vs decoder-only, masked language model vs causal language model, bidirectional vs unidirectional attention. Her birinin hangi gorevler icin uygun oldugunu (text generation, classification, QA, summarization) acikla. Model distillation ve quantization ile model boyutunu nasil kucultursun?"

### Pair Programming Ipucu
Transformer modelleri ile calisirken AI'a Hugging Face model card veya training metriklerini goster ve sor: "Bu fine-tuned modelin overfitting mi yapiyor? Learning rate schedule, warmup steps ve weight decay parametrelerimi optimize et. Tokenizer'im dogru konfigure edilmis mi?"
:::

:::must-note
## Defterine Yaz!
1. **Self-Attention**: Her token diğer tüm token'lara bakarak context anlam kazanır. Q(query) * K(key) / sqrt(d_k) ile attention score hesapla, softmax uygula, V(value) ile çarp.
2. **Transformer = Encoder + Decoder**. BERT = sadece encoder (anlama). GPT = sadece decoder (üretme). T5 = encoder + decoder (her ikisi).
3. **Transfer Learning**: Büyük model'i genel veri ile pre-train et, sonra küçük domain-specific veri ile fine-tune et. ImageNet pre-trained CNN veya BERT pre-trained NLP modeli gibi.
4. **Hugging Face pipeline**: `from transformers import pipeline; pipe = pipeline("task"); result = pipe("input")` -- 3 satırda production-ready model.
5. **Positional Encoding**: Transformer sıra bilgisi bilmez (RNN'den farklı). Sin/cos bazlı pozisyon vektörleri eklenerek sıra bilgisi verilir.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir
Senior bir AI/ML engineer transformer konusunda:

1. **Model selection**: Task'a göre doğru model ailesi seçer (BERT for understanding, GPT for generation, T5 for seq2seq, ViT for vision)
2. **Efficient fine-tuning**: LoRA, QLoRA, prefix tuning gibi parameter-efficient yöntemleri bilir -- tüm modeli fine-tune etmek pahalı
3. **Inference optimization**: Quantization (INT8/INT4), KV-cache, speculative decoding, distillation ile latency düşürür
4. **Cost analysis**: API vs self-hosted, GPU maliyeti, token pricing hesaplar
5. **Evaluation**: BLEU, ROUGE, perplexity, human evaluation ile model kalitesini ölçer
6. **Safety**: Prompt injection, hallucination, bias farkındalığı -- guardrails ekler

**Karar Verme Sureci — API vs Self-Hosted vs Fine-Tuned:**
- **API (OpenAI, Anthropic, Google)**: Sifir infra maliyeti, aninda baslama, surekli guncellenen modeller. Trade-off: Token basina maliyet yuksek olabilir (yuksek hacimde), veri gizliligi endisesi (verini 3. parti servise gonderiyorsun), rate limit ve downtime riski. Kullanim: Prototip, dusuk-orta hacim, genel amacli NLP tasklari.
- **Self-hosted open-source (LLaMA, Mistral, Qwen)**: Veri gizliligi tam kontrol, yuksek hacimde API'den ucuz, fine-tuning imkani. Trade-off: GPU maliyeti ($1-10/saat), infra yonetimi (CUDA, driver, model serving), model guncelleme manuel. Kullanim: Hassas veri (saglik, finans), yuksek hacim (1M+ token/gun), ozel domain.
- **Fine-tuned model**: Domain-specific performans cok daha iyi, kucuk model buyuk modelden iyi sonuc verebilir. Trade-off: Egitim verisi hazirlama maliyeti, overfitting riski, model bakimi (veri degistikce retrain). Kullanim: Spesifik task (sentiment, NER, classification), tutarli format gereken ciktilar.
- **Senior karar agaci**: "Genel amacli, dusuk hacim, hemen lazim? API. Hassas veri veya yuksek hacim? Self-hosted. Spesifik task, tutarli cikti? Fine-tune. Oncelikle API ile prototiple, sonra optimize et."

**Anti-pattern Farkindaligi:**
- **"En buyuk model en iyidir" yanilgisi**: GPT-4o'yu sentiment analysis icin kullanmak 1000x gereksiz pahali. BERT-base veya DistilBERT bu is icin yeterli ve 10ms'de cevap verir (GPT-4o 500ms+). Her zaman task complexity'ye gore model sec.
- **Evaluation'siz production'a cikmak**: "Ciktilara baktim iyi gorunuyor" yeterli degil. BLEU, ROUGE, F1 gibi metriklerle sistematik olcum yap. A/B test ile kullanici memnuniyetini karsilastir. Human evaluation ile edge case'leri yakala.
- **Context window'u doldurma**: 128K token destekliyor diye her seyi prompt'a tıkmak. "Lost in the middle" problemi — model ortadaki bilgiyi kacirir. Chunking + retrieval (RAG) ile sadece ilgili bilgiyi ver.

**Gercek Dunya Deneyimi:** Bir musteri destek chatbot'u icin baslangicta GPT-4 kullandik. Aylik API maliyeti $12K'ya ulasti. Analiz yaptik: sorularin %80'i 50 kategoriden birine ait basit sorular. Bu %80 icin fine-tuned GPT-4o-mini gecirdik (maliyet %95 dustu), kalan %20 karmasik sorulari GPT-4o'ya yonlendirdik. Toplam maliyet $800'a dustu, musteri memnuniyeti ayni kaldi. Ders: model routing, tek model her sey yapmaktan hem ucuz hem hizli.
:::

---

## 1. Attention Mechanism -- Neden Devrim?

### 1.1 RNN'in Problemi

:::concept
## RNN'den Transformer'a Geçiş

**RNN/LSTM'in sorunları**:
1. **Sequential processing**: Token'ları sırayla işler, paralelize edilemez. GPU'yu tam kullanamaz.
2. **Long-range dependencies**: 1000 token'lık bir cümlede 1. token ile 999. token arasındaki ilişkiyi öğrenmek zor (gradient vanishing).
3. **Bottleneck**: Encoder'ın tüm cümleyi tek bir fixed-size vector'e sıkıştırması gerekir.

**Attention çözümü**: Her output token, input'taki **tüm token'lara doğrudan bakabilir**. Hangi token'a ne kadar "dikkat" edeceğini öğrenir.

Örnek: "Kedi minderin üstünde uyuyordu" -> "The cat was sleeping on the cushion"
- "cat" çevirirken "kedi"ye yüksek attention
- "sleeping" çevirirken "uyuyordu"ya yüksek attention
- Uzak token'lar bile doğrudan bağlanabilir!
:::

```python
import numpy as np

def basic_attention(query, keys, values):
    """
    Basit attention mekanizması (Bahdanau attention benzeri)
    query: (1, d) -- decoder hidden state
    keys:  (seq_len, d) -- encoder hidden states
    values: (seq_len, d) -- encoder hidden states (genellikle keys ile aynı)
    """
    # 1. Attention scores: her key ile query'nin benzerliği
    scores = keys @ query.T  # (seq_len, 1)
    scores = scores.flatten()

    # 2. Softmax: normalize et (olasılık dağılımı)
    attention_weights = np.exp(scores - np.max(scores))
    attention_weights = attention_weights / attention_weights.sum()

    # 3. Context vector: weighted sum of values
    context = attention_weights.reshape(-1, 1) * values  # (seq_len, d)
    context = context.sum(axis=0, keepdims=True)  # (1, d)

    return context, attention_weights

# Demo: Çeviri attention
np.random.seed(42)

# Encoder output (4 token: "kedi minderde uyuyor .")
encoder_hidden = np.random.randn(4, 8)  # 4 tokens, 8 dim
tokens = ["kedi", "minderde", "uyuyor", "."]

# Decoder query ("cat" kelimesini üretirken)
decoder_hidden = encoder_hidden[0:1] + np.random.randn(1, 8) * 0.1  # "kedi"ye benzer

context, weights = basic_attention(decoder_hidden, encoder_hidden, encoder_hidden)

print("Attention Weights (translating 'cat'):")
for token, weight in zip(tokens, weights):
    bar = "█" * int(weight * 40)
    print(f"  {token:>10}: {weight:.4f} {bar}")
print(f"\nContext vector shape: {context.shape}")
```

### 1.2 Scaled Dot-Product Attention

:::concept
## Scaled Dot-Product Attention

Transformer'ın temel attention mekanizması:

**Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V**

- **Q (Query)**: "Neyi arıyorum?" -- Her token'ın sorgusı
- **K (Key)**: "Ben neyi sunuyorum?" -- Her token'ın anahtar bilgisi
- **V (Value)**: "Benim içeriğim ne?" -- Her token'ın gerçek değeri

**Neden sqrt(d_k) ile bölüyoruz?**
- d_k büyüdükçe dot product'lar da büyür
- Büyük değerler softmax'ı **saturate** eder (neredeyse one-hot olur)
- sqrt(d_k) ile scale edince gradient'ler daha sağlıklı olur
:::

```python
import numpy as np

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Transformer'ın core attention mekanizması.

    Q: (seq_len_q, d_k) -- queries
    K: (seq_len_k, d_k) -- keys
    V: (seq_len_k, d_v) -- values
    mask: (seq_len_q, seq_len_k) -- optional mask (decoder'da causal mask)
    """
    d_k = K.shape[-1]

    # 1. Attention scores
    scores = Q @ K.T / np.sqrt(d_k)  # (seq_len_q, seq_len_k)

    # 2. Masking (optional -- decoder'da future token'ları gizle)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)

    # 3. Softmax
    attention_weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    attention_weights = attention_weights / attention_weights.sum(axis=-1, keepdims=True)

    # 4. Weighted sum of values
    output = attention_weights @ V  # (seq_len_q, d_v)

    return output, attention_weights


# Demo: Self-attention
np.random.seed(42)

# 4 token'lık bir cümle, her biri 6-dim embedding
seq_len = 4
d_model = 6
d_k = 4

# Token embeddings
X = np.random.randn(seq_len, d_model)
tokens = ["the", "cat", "sat", "down"]

# Q, K, V projection matrices (öğrenilen parametreler)
W_Q = np.random.randn(d_model, d_k) * 0.1
W_K = np.random.randn(d_model, d_k) * 0.1
W_V = np.random.randn(d_model, d_k) * 0.1

# Project
Q = X @ W_Q
K = X @ W_K
V = X @ W_V

# Self-attention
output, weights = scaled_dot_product_attention(Q, K, V)

print("Self-Attention Weights:")
print(f"{'':>8}", end="")
for t in tokens:
    print(f"{t:>8}", end="")
print()

for i, token in enumerate(tokens):
    print(f"{token:>8}", end="")
    for j in range(seq_len):
        print(f"{weights[i, j]:8.4f}", end="")
    print()

print(f"\nOutput shape: {output.shape}")  # (4, d_k)

# Causal mask (decoder: sadece önceki token'lara bak)
causal_mask = np.tril(np.ones((seq_len, seq_len)))
print(f"\nCausal mask:\n{causal_mask}")

output_masked, weights_masked = scaled_dot_product_attention(Q, K, V, mask=causal_mask)
print(f"\nCausal attention weights:")
for i, token in enumerate(tokens):
    print(f"  {token}: {weights_masked[i].round(4)}")
```

### 1.3 Multi-Head Attention

:::concept
## Multi-Head Attention -- Birden Fazla Perspektif

Tek bir attention "head" bir tür ilişki yakalar. Ama dilde birden fazla ilişki türü var:
- **Syntactic**: Özne-yüklem ilişkisi
- **Semantic**: Anlam benzerliği
- **Positional**: Yakınlık ilişkisi

**Multi-head attention**: Birden fazla attention head paralel çalıştır, sonuçları birleştir.

**MultiHead(Q, K, V) = Concat(head_1, ..., head_h) @ W_O**

Her head_i = Attention(Q @ W_Q_i, K @ W_K_i, V @ W_V_i)

Tipik: 8 veya 12 head. d_model=512 ise her head d_k = 512/8 = 64 boyutlu çalışır.
:::

```python
import numpy as np

class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        # Projection matrices for each head
        self.W_Q = np.random.randn(d_model, d_model) * 0.1
        self.W_K = np.random.randn(d_model, d_model) * 0.1
        self.W_V = np.random.randn(d_model, d_model) * 0.1
        self.W_O = np.random.randn(d_model, d_model) * 0.1

    def split_heads(self, X):
        """(seq_len, d_model) -> (num_heads, seq_len, d_k)"""
        seq_len = X.shape[0]
        X = X.reshape(seq_len, self.num_heads, self.d_k)
        return X.transpose(1, 0, 2)  # (num_heads, seq_len, d_k)

    def forward(self, X, mask=None):
        # Project Q, K, V
        Q = X @ self.W_Q
        K = X @ self.W_K
        V = X @ self.W_V

        # Split into heads
        Q = self.split_heads(Q)  # (num_heads, seq_len, d_k)
        K = self.split_heads(K)
        V = self.split_heads(V)

        # Attention for each head
        all_heads = []
        all_weights = []

        for h in range(self.num_heads):
            output, weights = scaled_dot_product_attention(Q[h], K[h], V[h], mask)
            all_heads.append(output)
            all_weights.append(weights)

        # Concatenate heads
        concat = np.hstack(all_heads)  # (seq_len, d_model)

        # Final projection
        output = concat @ self.W_O

        return output, all_weights


# Demo
np.random.seed(42)
d_model = 16
num_heads = 4
seq_len = 5

X = np.random.randn(seq_len, d_model)
mha = MultiHeadAttention(d_model=d_model, num_heads=num_heads)

output, weights = mha.forward(X)
print(f"Input shape:  {X.shape}")      # (5, 16)
print(f"Output shape: {output.shape}")  # (5, 16)
print(f"Num heads:    {len(weights)}")   # 4

for h in range(num_heads):
    print(f"\nHead {h} attention (first token attends to):")
    print(f"  weights: {weights[h][0].round(3)}")
```

---

## 2. Transformer Architecture

:::concept
## "Attention Is All You Need" Mimarisi

```
INPUT TOKENS
    |
[Embedding + Positional Encoding]
    |
====== ENCODER (Nx) ======
|  Multi-Head Self-Attention  |
|  Add & Norm                 |
|  Feed-Forward Network       |
|  Add & Norm                 |
============================
    |
====== DECODER (Nx) ======
|  Masked Multi-Head Self-Attn |
|  Add & Norm                  |
|  Cross-Attention (enc output)|
|  Add & Norm                  |
|  Feed-Forward Network        |
|  Add & Norm                  |
=============================
    |
[Linear + Softmax]
    |
OUTPUT TOKENS
```

**Key components**:
1. **Positional Encoding**: Token sırasını bildir (sin/cos)
2. **Multi-Head Self-Attention**: Token'lar arası ilişki
3. **Feed-Forward Network**: Her position'a bağımsız MLP (genişlet->daralt)
4. **Add & Norm**: Residual connection + Layer normalization
5. **Cross-Attention**: Decoder, encoder output'una attend eder
:::

### 2.1 Positional Encoding

```python
import numpy as np

def positional_encoding(max_len, d_model):
    """
    Sin/cos bazlı positional encoding.
    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """
    PE = np.zeros((max_len, d_model))
    position = np.arange(max_len).reshape(-1, 1)
    div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))

    PE[:, 0::2] = np.sin(position * div_term)  # Çift indeksler
    PE[:, 1::2] = np.cos(position * div_term)  # Tek indeksler

    return PE

# Demo
PE = positional_encoding(max_len=10, d_model=8)
print("Positional Encoding (10 positions, 8 dims):")
print(PE.round(3))

# Her pozisyon benzersiz bir pattern
print(f"\nPosition 0 vs 1 similarity: {np.dot(PE[0], PE[1]) / (np.linalg.norm(PE[0]) * np.linalg.norm(PE[1])):.4f}")
print(f"Position 0 vs 5 similarity: {np.dot(PE[0], PE[5]) / (np.linalg.norm(PE[0]) * np.linalg.norm(PE[5])):.4f}")
# Yakın pozisyonlar daha benzer!
```

### 2.2 Feed-Forward Network ve Layer Norm

```python
import numpy as np

class FeedForward:
    """Position-wise Feed-Forward Network"""
    def __init__(self, d_model, d_ff):
        # Genişlet: d_model -> d_ff (genellikle 4x)
        self.W1 = np.random.randn(d_model, d_ff) * np.sqrt(2.0 / d_model)
        self.b1 = np.zeros(d_ff)
        # Daralt: d_ff -> d_model
        self.W2 = np.random.randn(d_ff, d_model) * np.sqrt(2.0 / d_ff)
        self.b2 = np.zeros(d_model)

    def forward(self, x):
        # ReLU(x @ W1 + b1) @ W2 + b2
        hidden = np.maximum(0, x @ self.W1 + self.b1)  # ReLU
        return hidden @ self.W2 + self.b2

class LayerNorm:
    """Layer Normalization"""
    def __init__(self, d_model, eps=1e-6):
        self.gamma = np.ones(d_model)
        self.beta = np.zeros(d_model)
        self.eps = eps

    def forward(self, x):
        mean = x.mean(axis=-1, keepdims=True)
        std = x.std(axis=-1, keepdims=True)
        return self.gamma * (x - mean) / (std + self.eps) + self.beta

# Transformer Encoder Block (simplified)
class TransformerEncoderBlock:
    def __init__(self, d_model, num_heads, d_ff):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.ff = FeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)

    def forward(self, x):
        # 1. Multi-Head Self-Attention + Residual + Norm
        attn_output, _ = self.attention.forward(x)
        x = self.norm1.forward(x + attn_output)  # Residual connection

        # 2. Feed-Forward + Residual + Norm
        ff_output = self.ff.forward(x)
        x = self.norm2.forward(x + ff_output)  # Residual connection

        return x

# Demo
np.random.seed(42)
d_model = 16
block = TransformerEncoderBlock(d_model=d_model, num_heads=4, d_ff=64)

X = np.random.randn(5, d_model)  # 5 tokens
output = block.forward(X)
print(f"Encoder block: input={X.shape}, output={output.shape}")
print(f"Output normalized: mean={output.mean():.4f}, std={output.std():.4f}")
```

---

## 3. BERT -- Understanding Model

:::concept
## BERT (Bidirectional Encoder Representations from Transformers)

BERT, 2018'de Google tarafından geliştirildi. **Sadece encoder** kullanır.

**Pre-training görevleri**:
1. **Masked Language Model (MLM)**: Cümledeki rastgele kelimeleri gizle, tahmin et
   - "The [MASK] sat on the mat" -> "cat"
2. **Next Sentence Prediction (NSP)**: İki cümle birbirini takip ediyor mu?

**Fine-tuning**: Pre-trained BERT'i task-specific data ile eğit
- Sentiment analysis, NER, question answering, text classification

**Variants**: BERT-base (110M param), BERT-large (340M param), DistilBERT (66M, %60 daha hızlı)
:::

:::realworld
## BERT Gerçek Dünya Uygulamaları

1. **Google Search**: 2019'dan beri arama sorgularını anlamak için BERT kullanıyor
2. **Spam Detection**: Email içeriğini anlayarak spam tespiti
3. **Sentiment Analysis**: Müşteri yorumlarından duygu analizi
4. **Named Entity Recognition**: Metinden isim, tarih, organizasyon çıkarma
5. **Question Answering**: Bir passage'dan soruya cevap bulma
6. **Text Classification**: Belge kategorizasyonu, intent detection
:::

---

## 4. GPT -- Generation Model

:::concept
## GPT Evrimi

GPT (Generative Pre-trained Transformer), OpenAI tarafından geliştirildi. **Sadece decoder** kullanır.

**GPT-1** (2018): 117M parametre. Concept proof.
**GPT-2** (2019): 1.5B parametre. "Too dangerous to release" iddiası.
**GPT-3** (2020): 175B parametre. Few-shot learning devrimi.
**GPT-4** (2023): Multimodal (text + image). Reasoning yeteneği.
**GPT-4o** (2024): Omni-modal. Ses, görüntü, text birlikte.

**Çalışma prensibi**: Autoregressive -- önceki token'lara bakarak sonraki token'ı tahmin et.
- Input: "The cat sat on the"
- Output: "mat" (en yüksek olasılıklı sonraki token)

**Causal masking**: Decoder'da her token sadece kendinden **önceki** token'lara bakabilir (gelecek gizli).
:::

:::comparison
## BERT vs GPT Karşılaştırması

| Özellik | BERT | GPT |
|---------|------|-----|
| **Mimari** | Encoder-only | Decoder-only |
| **Yön** | Bidirectional (iki yönlü) | Autoregressive (soldan sağa) |
| **Pre-training** | MLM + NSP | Next token prediction |
| **Güçlü olduğu** | Understanding (NLU) | Generation (NLG) |
| **Kullanım** | Classification, NER, QA | Text generation, chatbot, code |
| **Input/Output** | Input -> label/span | Prompt -> continuation |
| **Fine-tuning** | Task-specific head ekle | Prompt engineering veya fine-tune |
:::

---

## 5. Vision Transformers (ViT)

:::concept
## ViT -- CNN'siz Görüntü İşleme

Vision Transformer (2020), resmi **patch'lere** böler ve her patch'i bir token gibi işler.

**Nasıl çalışır?**
1. 224x224 resmi 16x16 patch'lere böl -> 196 patch
2. Her patch'i linear projection ile embedding'e dönüştür
3. Positional encoding ekle
4. Transformer encoder'dan geçir
5. [CLS] token'ının output'unu classification head'e ver

**Avantaj**: Büyük veri setlerinde CNN'den daha iyi performans (ViT-L on ImageNet)
**Dezavantaj**: Küçük veri setlerinde CNN'den kötü (inductive bias eksikliği)

**Hybrid**: CNN + Transformer en iyi sonuçları verir (ConvNeXt, Swin Transformer)
:::

```python
import numpy as np

def image_to_patches(image, patch_size):
    """
    Resmi patch'lere böl.
    image: (H, W, C)
    Returns: (num_patches, patch_size * patch_size * C)
    """
    H, W, C = image.shape
    assert H % patch_size == 0 and W % patch_size == 0

    num_patches_h = H // patch_size
    num_patches_w = W // patch_size
    num_patches = num_patches_h * num_patches_w

    patches = []
    for i in range(num_patches_h):
        for j in range(num_patches_w):
            patch = image[i*patch_size:(i+1)*patch_size,
                         j*patch_size:(j+1)*patch_size, :]
            patches.append(patch.flatten())

    return np.array(patches)

# Demo: 8x8 RGB image -> 4 patches (4x4 each)
image = np.random.randn(8, 8, 3)  # 8x8 RGB
patches = image_to_patches(image, patch_size=4)

print(f"Image shape: {image.shape}")      # (8, 8, 3)
print(f"Patches shape: {patches.shape}")   # (4, 48) = 4 patches, each 4*4*3=48 dim

# Linear projection to d_model
d_model = 16
W_proj = np.random.randn(48, d_model) * 0.1
patch_embeddings = patches @ W_proj

# Add CLS token
cls_token = np.random.randn(1, d_model) * 0.01
sequence = np.vstack([cls_token, patch_embeddings])  # (5, 16) = CLS + 4 patches

# Add positional encoding
PE = positional_encoding(max_len=5, d_model=d_model)
sequence = sequence + PE

print(f"Final sequence: {sequence.shape}")  # (5, 16) - ready for transformer
```

---

## 6. Transfer Learning ve Fine-Tuning

:::concept
## Transfer Learning -- Öğrenileni Aktar

**Neden önemli?**
- GPT-3 eğitmek: ~$4.6M, yüzlerce GPU, haftalarca süre
- Fine-tuning: Birkaç yüz dolar, 1 GPU, saatler

**Strateji**:
1. **Feature Extraction**: Pre-trained modeli dondur, sadece son layer'ı eğit
2. **Fine-tuning**: Son birkaç layer'ı "açarak" domain-specific data ile eğit
3. **Full fine-tuning**: Tüm modeli düşük lr ile eğit (büyük veri gerekir)
4. **LoRA**: Low-Rank Adaptation -- sadece küçük matrisler ekleyerek adapt et (çok verimli)

**Kural**: Veri az -> Feature extraction. Veri çok -> Fine-tuning. Veri çok büyük -> Full fine-tuning.
:::

```python
# PyTorch ile Transfer Learning örneği (pseudo-code pattern)

"""
import torch
import torch.nn as nn
from torchvision import models

# 1. Pre-trained model yükle
model = models.resnet50(weights='IMAGENET1K_V2')

# 2. Feature extraction: Tüm layer'ları dondur
for param in model.parameters():
    param.requires_grad = False

# 3. Son layer'ı değiştir (ImageNet 1000 class -> bizim 10 class)
model.fc = nn.Sequential(
    nn.Linear(2048, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 10)  # 10 sınıf
)

# 4. Sadece yeni layer eğitilecek
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)
"""

# Fine-tuning strategy pattern
strategies = {
    "Feature Extraction": {
        "frozen_layers": "Tüm model",
        "trainable": "Sadece son classification head",
        "lr": "0.001",
        "data_needed": "Az (~100-1K sample)",
        "training_time": "Dakikalar"
    },
    "Partial Fine-tuning": {
        "frozen_layers": "İlk layer'lar (genel features)",
        "trainable": "Son birkaç layer + head",
        "lr": "0.0001",
        "data_needed": "Orta (~1K-10K sample)",
        "training_time": "Saatler"
    },
    "Full Fine-tuning": {
        "frozen_layers": "Hiçbiri",
        "trainable": "Tüm model",
        "lr": "0.00001 (çok küçük!)",
        "data_needed": "Çok (~10K+)",
        "training_time": "Günler"
    },
    "LoRA": {
        "frozen_layers": "Tüm original model",
        "trainable": "Küçük rank-decomposition matrisleri",
        "lr": "0.0001-0.001",
        "data_needed": "Az-orta",
        "training_time": "Saatler (memory efficient!)"
    }
}

for name, info in strategies.items():
    print(f"\n{'='*50}")
    print(f"Strategy: {name}")
    for key, val in info.items():
        print(f"  {key}: {val}")
```

:::code
## Hugging Face Pipeline ile Pratik NLP Gorevleri

```python
from transformers import pipeline

# 1. Sentiment Analysis (Duygu Analizi)
sentiment = pipeline("sentiment-analysis")
print(sentiment("I love this product!"))
# [{'label': 'POSITIVE', 'score': 0.9998}]

# 2. Named Entity Recognition (Varlik Tanima)
ner = pipeline("ner", grouped_entities=True)
print(ner("Elon Musk, Tesla CEO'su, San Francisco'da yasiyyor."))
# [{'entity_group': 'PER', 'word': 'Elon Musk'}, {'entity_group': 'ORG', 'word': 'Tesla'}, ...]

# 3. Zero-Shot Classification (Etiket olmadan siniflandirma)
classifier = pipeline("zero-shot-classification")
result = classifier(
    "Bu urun cok pahali ama kalitesi harika",
    candidate_labels=["fiyat sikayeti", "kalite ovgusu", "teslimat sorunu"]
)
print(result['labels'][0])  # "kalite ovgusu"

# 4. Text Generation
generator = pipeline("text-generation", model="gpt2")
print(generator("The future of AI is", max_length=50, num_return_sequences=1))

# 5. Translation
translator = pipeline("translation_en_to_fr")
print(translator("Hello, how are you?"))
```
:::

:::exercise
## Pratik: Hugging Face Model Fine-tuning

### Alistirma 1: Sentiment Fine-tuning
Google Colab'da (ucretsiz T4 GPU):
1. `datasets` kutuphanesinden `yelp_review_full` dataset'ini yukle
2. `distilbert-base-uncased` modelini 5-sinifli sentiment icin fine-tune et
3. Training: 1000 ornek, Eval: 200 ornek, 2 epoch
4. Accuracy'yi raporla

**Beklenen sonuc:** 2 epoch'ta ~55-60% accuracy (5 sinif icin iyi)

### Alistirma 2: Custom NER
1. Kendi veri setini olustur: 50 cumle, icerisinde URUN, SIRKET, FIYAT entity'leri isaretli
2. `bert-base-uncased` modelini NER icin fine-tune et
3. Yeni cumleler üzerinde test et

**Ipucu:** Hugging Face `datasets` kutuphanesinin `Dataset.from_dict()` ile kendi verini olusturabilirsin.
:::

---

## 7. Hugging Face -- Modern AI Toolkit

### 7.1 Pipeline API (En Kolay Yol)

```python
# Hugging Face Transformers -- 3 satırda AI modeli kullan
from transformers import pipeline

# === 1. SENTIMENT ANALYSIS ===
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product! It's amazing!")
print(f"Sentiment: {result}")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Türkçe sentiment (multilingual model)
classifier_multi = pipeline("sentiment-analysis",
                             model="nlptown/bert-base-multilingual-uncased-sentiment")
result = classifier_multi("Bu ürün harika, çok memnunum!")
print(f"Turkish sentiment: {result}")

# === 2. TEXT GENERATION ===
generator = pipeline("text-generation", model="gpt2")
result = generator("Machine learning is", max_length=50, num_return_sequences=1)
print(f"\nGenerated: {result[0]['generated_text']}")

# === 3. NAMED ENTITY RECOGNITION ===
ner = pipeline("ner", grouped_entities=True)
result = ner("Elon Musk founded SpaceX in Hawthorne, California in 2002.")
print(f"\nNER results:")
for entity in result:
    print(f"  {entity['entity_group']}: {entity['word']} (score: {entity['score']:.4f})")

# === 4. QUESTION ANSWERING ===
qa = pipeline("question-answering")
result = qa(
    question="What is the capital of France?",
    context="France is a country in Western Europe. Its capital city is Paris, which is known for the Eiffel Tower."
)
print(f"\nQA: {result['answer']} (score: {result['score']:.4f})")

# === 5. SUMMARIZATION ===
summarizer = pipeline("summarization")
text = """
Artificial intelligence has made remarkable progress in recent years.
Large language models like GPT-4o can understand and generate human-like text.
These models are trained on vast amounts of data and use transformer architectures.
The technology has applications in healthcare, education, and many other fields.
"""
result = summarizer(text, max_length=50, min_length=20)
print(f"\nSummary: {result[0]['summary_text']}")

# === 6. ZERO-SHOT CLASSIFICATION ===
zero_shot = pipeline("zero-shot-classification")
result = zero_shot(
    "This movie was absolutely fantastic, the best I've seen this year!",
    candidate_labels=["positive review", "negative review", "neutral review"]
)
print(f"\nZero-shot: {result['labels'][0]} ({result['scores'][0]:.4f})")

# === 7. TRANSLATION ===
translator = pipeline("translation_en_to_fr")
result = translator("Machine learning is changing the world.")
print(f"\nTranslation: {result[0]['translation_text']}")
```

### 7.2 Model ve Tokenizer Kullanımı

```python
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
import torch
import numpy as np

# === Tokenizer: Text -> Tokens -> IDs ===
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

text = "Machine learning is fascinating!"
tokens = tokenizer.tokenize(text)
ids = tokenizer.encode(text)
decoded = tokenizer.decode(ids)

print(f"Text:    {text}")
print(f"Tokens:  {tokens}")
print(f"IDs:     {ids}")
print(f"Decoded: {decoded}")

# Batch tokenization (padding + truncation)
texts = [
    "I love AI",
    "Natural language processing is a subfield of artificial intelligence"
]

encoded = tokenizer(texts, padding=True, truncation=True,
                     max_length=20, return_tensors="pt")

print(f"\nBatch encoding:")
print(f"  input_ids shape: {encoded['input_ids'].shape}")
print(f"  attention_mask:  {encoded['attention_mask']}")

# === Model: Embeddings çıkar ===
model = AutoModel.from_pretrained("bert-base-uncased")
model.eval()

with torch.no_grad():
    outputs = model(**encoded)
    # outputs.last_hidden_state: (batch, seq_len, 768)
    # CLS token embedding (cümle temsili)
    cls_embeddings = outputs.last_hidden_state[:, 0, :]

print(f"\nCLS embeddings shape: {cls_embeddings.shape}")  # (2, 768)

# Cosine similarity between sentences
cos_sim = torch.nn.functional.cosine_similarity(cls_embeddings[0:1], cls_embeddings[1:2])
print(f"Similarity: {cos_sim.item():.4f}")

# === Fine-tuning for Classification ===
"""
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

# 1. Dataset yükle
dataset = load_dataset("imdb")

# 2. Tokenize
def tokenize_fn(example):
    return tokenizer(example["text"], truncation=True, max_length=512)

tokenized = dataset.map(tokenize_fn, batched=True)

# 3. Model
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=2
)

# 4. Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    learning_rate=2e-5,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# 5. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
)

# 6. Train!
trainer.train()

# 7. Evaluate
results = trainer.evaluate()
print(f"Eval accuracy: {results['eval_accuracy']:.4f}")
"""
```

### 7.3 Sentence Transformers (Embedding)

```python
# Sentence Transformers -- Semantik benzerlik için
"""
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# Cümleleri embed et
sentences = [
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks",
    "I like to eat pizza",
    "Artificial intelligence is transforming technology"
]

embeddings = model.encode(sentences)
print(f"Embeddings shape: {embeddings.shape}")  # (4, 384)

# Similarity matrix
cos_sim = util.cos_sim(embeddings, embeddings)
print(f"Similarity matrix:\n{cos_sim.numpy().round(3)}")

# Semantic search
query = "What is artificial intelligence?"
query_embedding = model.encode(query)

scores = util.cos_sim(query_embedding, embeddings)[0]
for i, (sent, score) in enumerate(zip(sentences, scores)):
    print(f"  {score:.4f}: {sent}")
"""
```

---

## 8. Modern AI Trendleri

:::concept
## 2025-2027 AI Trendleri

1. **Multimodal Models**: Text + Image + Audio + Video tek modelde (GPT-4o, Gemini)
2. **Small Language Models**: Phi-4, Llama 3.3, Gemma 3 -- mobil cihazlarda çalışan küçük modeller
3. **Retrieval-Augmented Generation (RAG)**: LLM + vektör veritabanı ile hallucination azaltma
4. **Agents**: LLM'lerin tool kullanarak otonom görev yapması (function calling)
5. **Mixture of Experts (MoE)**: Mixtral -- dev model ama her input için sadece bir kısım aktif
6. **Edge AI**: Modelleri telefon/tarayıcıda çalıştırma (WebGPU, ONNX Runtime)
7. **Synthetic Data**: AI ile veri üretip AI eğitme
8. **Safety & Alignment**: RLHF, Constitutional AI, red teaming
:::

:::interview
## Mülakat Sorusu: Transformer Attention

**Soru**: "Self-attention'ın time complexity'si nedir ve neden bu bir problem?"

**Beklenen cevap**: "Self-attention O(n^2 * d) complexity'ye sahip, burada n = sequence length, d = dimension. 1000 token'lık bir input için 1M attention score hesaplanır. Bu yüzden uzun document'lar için sorun olur. Çözümler: Sparse attention (Longformer), Linear attention (Linformer), Sliding window (Mistral), veya chunked attention. GPT-4o 128K context window destekler ama bu optimizasyonlar sayesinde."

**Neden sorulur**: Model seçimi ve optimizasyon bilgisini ölçer. Production'da latency ve memory constraint'lerini anlamak kritik.
:::

:::beginner-mistake
## Sık Yapılan Hatalar -- Transformers

**Hata 1**: "Her problem için en büyük modeli kullanayım"
- GPT-4o her zaman gerekli değil. Sentiment analysis için BERT-base yeterli ve 1000x ucuz.

**Hata 2**: "Fine-tuning yapmadan direkt kullanayım"
- Domain-specific task'larda fine-tuning dramatik fark yaratır. Medical text'te BERT vs BioBERT.

**Hata 3**: "Tokenizer'ı görmezden geleyim"
- Farklı model farklı tokenizer kullanır. BERT wordpiece, GPT BPE. Yanlış tokenizer = anlamsız sonuç.

**Hata 4**: "Tüm modeli fine-tune edeyim"
- 1000 sample ile 175B parametreli modeli fine-tune etmek overfit ve kaynak israfı. LoRA veya prompt tuning kullan.
:::

:::english
## Technical Terms Glossary

| English | Türkçe Açıklama |
|---------|-----------------|
| **Attention** | Her token'ın diğer token'lara ne kadar dikkat ettiğini ölçen mekanizma |
| **Self-Attention** | Token'ların aynı sequence içindeki diğer token'lara attend etmesi |
| **Multi-Head Attention** | Birden fazla attention head ile farklı ilişki türlerini yakalama |
| **Query/Key/Value** | Attention'ın üç bileşeni: ne arıyorum / ne sunuyorum / gerçek içerik |
| **Positional Encoding** | Token sıra bilgisini sin/cos ile encode etme |
| **Encoder** | Input'u anlama (BERT tarzı, bidirectional) |
| **Decoder** | Output üretme (GPT tarzı, autoregressive) |
| **Pre-training** | Büyük genel veri ile model eğitme |
| **Fine-tuning** | Pre-trained modeli küçük task-specific veri ile adapte etme |
| **Transfer Learning** | Bir task'ta öğrenileni başka task'a aktarma |
| **LoRA** | Parameter-efficient fine-tuning (düşük rank adaptasyon) |
| **Tokenizer** | Metni token'lara (alt kelimelere) ayıran araç |
| **Embedding** | Token'ı yoğun vektör temsile dönüştürme |
| **Causal Masking** | Decoder'da gelecek token'ları gizleme |
| **Hallucination** | LLM'in uydurma bilgi üretmesi |
| **RAG** | Retrieval-Augmented Generation -- dış bilgi ile zenginleştirme |
:::

:::knowledge-check
## Bilgi Kontrolü

1. Self-attention'da Q, K, V ne anlama gelir ve nasıl hesaplanır?
2. BERT neden bidirectional, GPT neden autoregressive?
3. Positional encoding neden gerekli? RNN'de neden gerekmez?
4. LoRA'nın full fine-tuning'e göre avantajı nedir?
5. Vision Transformer resmi nasıl token'lara dönüştürür?
:::

:::exercise
## Alıştırma: Hugging Face ile Sentiment Analysis Pipeline

1. Hugging Face'ten Türkçe destekleyen bir sentiment model yükle
2. 10 Türkçe yorum hazırla (5 pozitif, 5 negatif)
3. Pipeline ile tahmin yap
4. Accuracy hesapla
5. Yanlış tahmin edilen yorumları analiz et
6. **Bonus**: Kendi dataset'in ile BERT fine-tune yap (Trainer API)

```python
from transformers import pipeline

# Model önerisi: "savasy/bert-base-turkish-sentiment-cased"
# veya multilingual: "nlptown/bert-base-multilingual-uncased-sentiment"

# Yorumlar
yorumlar = [
    {"text": "Bu ürün harika, çok memnunum!", "label": "positive"},
    {"text": "Berbat bir deneyimdi, asla tavsiye etmem.", "label": "negative"},
    # ... 8 tane daha ekle
]

# Pipeline oluştur ve tahmin yap
# ...
```

---

### Alıştırma 2: Attention Mekanizmasını Görselleştir (Orta)

Scaled Dot-Product Attention'ı sıfırdan implement et ve attention weight'leri görselleştir:

```python
import numpy as np
import matplotlib.pyplot as plt

def scaled_dot_product_attention(Q, K, V):
    """
    Scaled Dot-Product Attention implementasyonu

    Args:
        Q: Query matrix (seq_len, d_k)
        K: Key matrix (seq_len, d_k)
        V: Value matrix (seq_len, d_v)

    Returns:
        output: Attention output (seq_len, d_v)
        weights: Attention weights (seq_len, seq_len)
    """
    d_k = Q.shape[-1]
    # TODO: 1. Q ve K^T'nin dot product'ını hesapla
    # TODO: 2. sqrt(d_k) ile scale et
    # TODO: 3. Softmax uygula (attention weights)
    # TODO: 4. Weights ile V'yi çarp
    pass

def visualize_attention(weights, tokens):
    """Attention weight'lerini heatmap olarak göster"""
    # TODO: matplotlib ile heatmap çiz
    # x-axis: Key tokens, y-axis: Query tokens
    # Her hücredeki değer attention weight'i göstermeli
    pass

# Test:
tokens = ["Ben", "bugün", "çok", "mutluyum"]
seq_len, d_k = 4, 8

np.random.seed(42)
Q = np.random.randn(seq_len, d_k)
K = np.random.randn(seq_len, d_k)
V = np.random.randn(seq_len, d_k)

output, weights = scaled_dot_product_attention(Q, K, V)
visualize_attention(weights, tokens)

# Doğrulama:
# - weights her satırının toplamı 1.0 olmalı (softmax)
# - output shape == V shape olmalı
print(f"Weights row sums: {weights.sum(axis=1)}")  # [1.0, 1.0, 1.0, 1.0]
print(f"Output shape: {output.shape}")  # (4, 8)
```

**Beklenen sonuç:** Attention heatmap'i oluşmalı. Her satır toplamı 1.0 olmalı. Hangi token'ın hangi token'a daha çok "dikkat ettiğini" yorumla.

---

### Alıştırma 3: Hugging Face ile Multi-Task NLP Pipeline (Zor)

Birden fazla NLP görevini tek bir script'te çöz:

```python
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

# Görev 1: Text Classification (Zero-Shot)
# Bir haber metnini kategorize et: "spor", "teknoloji", "ekonomi", "sağlık"
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

haberler = [
    "Tesla'nın yeni modeli 1000km menzile ulaştı",
    "Galatasaray şampiyonluk kupasını kaldırdı",
    "Merkez Bankası faiz oranını değiştirmedi",
]
# TODO: Her haberi kategorize et ve confidence score'ları yazdır

# Görev 2: Named Entity Recognition (NER)
# Türkçe metinden kişi, yer, kuruluş isimlerini çıkar
ner = pipeline("ner", model="akdeniz27/bert-base-turkish-cased-ner", aggregation_strategy="simple")

metin = "Mustafa Kemal Atatürk 1881'de Selanik'te doğdu ve Türkiye Cumhuriyeti'ni kurdu."
# TODO: Entity'leri çıkar, her birinin tipini ve confidence score'unu göster

# Görev 3: Semantic Similarity
# İki cümle arasındaki anlamsal benzerliği ölç
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

cumle_ciftleri = [
    ("Bugün hava çok güzel", "Güneşli bir gün"),         # Benzer
    ("Bugün hava çok güzel", "Python programlama dili"),  # Farklı
]
# TODO: Her çift için cosine similarity hesapla
# Hint: Mean pooling → cosine similarity

# Bonus: Sonuçları bir tablo halinde yazdır
```

**Beklenen sonuç:** Zero-shot classification doğru kategoriler vermeli. NER en az 3 entity bulmalı. Semantic similarity benzer cümleler için >0.7, farklı cümleler için <0.3 olmalı.

---

### Alıştırma 4: Tokenizer Derinlemesine Analiz (Kolay)

Farkli tokenizer'larin ayni metni nasil parcaladigini incele.

```python
from transformers import AutoTokenizer

models = ["bert-base-uncased", "gpt2", "xlm-roberta-base"]
text = "Transformer modelleri NLP'yi devrimleştirdi. Self-attention mekanizması çok güçlü!"

for model_name in models:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    ids = tokenizer.encode(text)
    decoded = tokenizer.decode(ids)

    print(f"\n=== {model_name} ===")
    print(f"Token sayisi: {len(tokens)}")
    print(f"Tokens: {tokens[:20]}")
    print(f"Vocab size: {tokenizer.vocab_size}")

    # TODO: Turkce metin ile token sayisini karsilastir
    # TODO: Subword tokenization'in nadir kelimeleri nasil paredaladigini gozlemle
    # TODO: Special token'lari incele ([CLS], [SEP], <s>, </s>)
    # TODO: max_length ve padding/truncation etkisini test et
```

**Beklenen Sonuc:** BERT WordPiece, GPT-2 BPE, XLM-RoBERTa SentencePiece kullanir. Türkçe metin daha fazla token uretir. Nadir kelimeler subword'lere parcalanir.
**Ipucu:** Token sayisi = islem maliyeti. Türkçe gibi aglutine dillerde token sayisi Ingilizce'nin 1.5-2x'i olabilir.

---

### Alıştırma 5: Text Embedding ve Semantic Search (Orta)

Sentence-BERT ile metin embedding'leri olustur ve anlamsal arama yap.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

# Dokuman koleksiyonu
documents = [
    "Python programlama dili web gelistirme icin kullanilir",
    "Machine learning algoritmalari veriyi analiz eder",
    "React ile modern kullanici arayuzleri olusturulur",
    "Docker container'lari uygulama dagitimini kolaylastirir",
    "PostgreSQL iliskisel veritabani yonetimidir",
    "Neural network'ler derin ogrenmenin temelidir",
    "Git versiyon kontrol sistemi kod yonetimi saglar",
    "Kubernetes container orchestration platformudur",
]

# Embedding'leri olustur
doc_embeddings = model.encode(documents)

def semantic_search(query, top_k=3):
    query_embedding = model.encode([query])
    similarities = np.dot(doc_embeddings, query_embedding.T).flatten()
    top_indices = np.argsort(similarities)[::-1][:top_k]
    for idx in top_indices:
        print(f"Score: {similarities[idx]:.4f} | {documents[idx]}")

semantic_search("yapay zeka ve derin ogrenme")
semantic_search("web uygulamasi gelistirme")

# TODO: 50+ dokuman ile daha buyuk bir koleksiyon olustur
# TODO: FAISS ile hizli nearest neighbor aramasi yap
# TODO: Turkce model dene (sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
# TODO: Cosine similarity vs dot product karsilastir
```

**Beklenen Sonuc:** Anlamca benzer dokumanlar en yuksek skor almali. "yapay zeka" sorgusu neural network ve ML dokumanlarini bulmali. FAISS ile buyuk veri setlerinde milisaniyede arama yapilabilmeli.
**Ipucu:** Sentence-BERT cumlyeleri sabit boyutlu vektorlere cevirir. FAISS milyonlarca vektorde milisaniyede arama yapar.

---

### Alıştırma 6: Positional Encoding Implementasyonu (Orta)

Transformer'in pozisyon bilgisini nasil kodladigini sifirdan implement et.

```python
import numpy as np
import matplotlib.pyplot as plt

def positional_encoding(max_len, d_model):
    pe = np.zeros((max_len, d_model))
    position = np.arange(max_len)[:, np.newaxis]
    div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))

    pe[:, 0::2] = np.sin(position * div_term)  # cift indeksler: sin
    pe[:, 1::2] = np.cos(position * div_term)  # tek indeksler: cos
    return pe

pe = positional_encoding(100, 64)

# Gorsellestir
plt.figure(figsize=(12, 6))
plt.imshow(pe, aspect="auto", cmap="RdBu")
plt.colorbar()
plt.xlabel("Embedding Dimension")
plt.ylabel("Position")
plt.title("Positional Encoding")
plt.show()

# TODO: Farkli pozisyonlardaki encoding vektorlerinin cosine similarity'sini hesapla
# TODO: Yakin pozisyonlarin benzer encoding'e sahip oldugunu dogrula
# TODO: RoPE (Rotary Position Embedding) implementasyonu yap
# TODO: Learned vs sinusoidal positional encoding karsilastir
```

**Beklenen Sonuc:** Yakin pozisyonlarin encoding'leri birbirine benzer olmali. Uzak pozisyonlarin encoding'leri farkli olmali. Heatmap'te periyodik patern gorunmeli.
**Ipucu:** Sin/cos farkli frekanslarda, farkli pozisyon ciftlerini ayirt etmeyi saglar. PE(pos+k) lineer olarak PE(pos)'tan elde edilebilir.

---

### Alıştırma 7: Model Distillation — Buyuk Modeli Kucult (Zor)

Knowledge distillation ile buyuk bir modelin bilgisini kucuk modele aktar.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class TeacherModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 512), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(512, 256), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256, 10)
        )
    def forward(self, x): return self.net(x)

class StudentModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(784, 64), nn.ReLU(),
            nn.Linear(64, 10)
        )
    def forward(self, x): return self.net(x)

def distillation_loss(student_logits, teacher_logits, labels, temperature=4.0, alpha=0.7):
    # Soft target loss (teacher'dan ogrenme)
    soft_loss = F.kl_div(
        F.log_softmax(student_logits / temperature, dim=1),
        F.softmax(teacher_logits / temperature, dim=1),
        reduction="batchmean"
    ) * (temperature ** 2)

    # Hard target loss (gercek etiketlerden ogrenme)
    hard_loss = F.cross_entropy(student_logits, labels)

    return alpha * soft_loss + (1 - alpha) * hard_loss

# TODO: Teacher modeli normal sekilde egit
# TODO: Student modeli distillation_loss ile egit
# TODO: Student'i distillation olmadan egit ve karsilastir
# TODO: Temperature ve alpha parametrelerinin etkisini analiz et
# TODO: Model boyutlarini ve inference hizlarini karsilastir
```

**Beklenen Sonuc:** Distilled student, normal student'tan daha yuksek accuracy vermeli. Student model teacher'in %90+ performansini yakalamali. Student model 4-8x daha kucuk olmali.
**Ipucu:** Temperature arttikca soft target'lar daha informatif olur (siniflar arasi iliski bilgisi). Alpha dengesini ayarla: cok yuksekse student teacher'a aşiri bagimli olur.

---

### Alıştırma 8: Transformer Blogu Sifirdan (Zor)

Minimal bir Transformer decoder blogu sifirdan implement et.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        self.d_k = d_model // num_heads
        self.num_heads = num_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        B, T, C = x.shape
        Q = self.W_q(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(B, T, self.num_heads, self.d_k).transpose(1, 2)

        # Scaled dot-product attention
        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))
        attn = F.softmax(scores, dim=-1)
        out = (attn @ V).transpose(1, 2).contiguous().view(B, T, C)
        return self.W_o(out)

class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attn = MultiHeadAttention(d_model, num_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(), nn.Linear(d_ff, d_model)
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        x = x + self.dropout(self.attn(self.norm1(x), mask))
        x = x + self.dropout(self.ff(self.norm2(x)))
        return x

# TODO: 4 katmanli mini GPT modeli olustur
# TODO: Causal mask (otoregresif) implement et
# TODO: Shakespeare metni uzerinde karakter bazli egit
# TODO: Olusturulan metni temperature sampling ile uret
```

**Beklenen Sonuc:** Model Shakespeare tarzinda tutarli metin uretebilmeli. Attention pattern'leri gorsellestirildiginde diyagonal ve yakin kelimelere yoğunlasma gorunmeli. 4 katmanli model 100 epoch'ta anlamli cikti uretmeli.
**Ipucu:** Causal mask ile her token sadece önceki token'lari gorebilir (autoregressive). Pre-norm (LayerNorm once) modern transformer'larda tercih edilir.
:::

:::external-resource
## Ek Kaynaklar

- [Attention Is All You Need (Original Paper)](https://arxiv.org/abs/1706.03762) -- Transformer paper'ı
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) -- Görsel Transformer açıklaması
- [Hugging Face Course](https://huggingface.co/course/) -- Ücretsiz NLP kursu
- [Andrej Karpathy - Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) -- Sıfırdan GPT implementasyonu
- [The Illustrated BERT](https://jalammar.github.io/illustrated-bert/) -- BERT görsel rehber
- [Hugging Face Model Hub](https://huggingface.co/models) -- 500K+ hazır model
- [LoRA Paper](https://arxiv.org/abs/2106.09685) -- Efficient fine-tuning
:::
