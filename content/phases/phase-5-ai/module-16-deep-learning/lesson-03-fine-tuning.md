---
title: "Fine-tuning ve Model Optimizasyonu"
description: "Pre-trained modelleri ozel gorevler için uyarlama: LoRA, QLoRA, PEFT, OpenAI Fine-tuning"
id: mod-16-deep-learning/lesson-03
order: 3
estimated_minutes: 120
tags: [fine-tuning, lora, qlora, peft, hugging-face, openai, transfer-learning]
prerequisites: [mod-16-deep-learning/lesson-02]
---

# Fine-tuning ve Model Optimizasyonu

Milyarlarca parametre ile eğitilmiş bir model düşün — GPT-4, LLaMA, BERT. Bu modeller genel dil anlayışına sahip ama **senin spesifik problemini** çözmek için tasarlanmadı. Fine-tuning, bu devasa modelleri alıp **senin verine, senin domain'ine, senin görevine** uyarlamak demek. Bu ders, modern AI mühendisliğinin en kritik becerilerinden birini öğretecek.

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Fine-tuning ile transfer learning arasindaki farki açıkla. LoRA ve QLoRA'nin matematiksel intuitionini ver. Neden tam fine-tuning yerine PEFT tercih ederiz? r (rank) parametresi ne anlama gelir ve nasil seçilir? Overfitting riskini azaltmak için hangi teknikler kullanılır?"

**2. Pratik Uygulama:**
> "Hugging Face Transformers ve PEFT kutuphaneleri ile bir text classification modeli fine-tune et. DistilBERT veya LLaMA modeli kullan. Dataset hazırlama, tokenization, LoRA config, training loop, evaluation ve model kaydetme adimlarini göster. Sonra ayni modeli QLoRA ile 4-bit quantization yaparak tekrar fine-tune et."
> Takip: "Şimdi bu fine-tuned modeli Hugging Face Hub'a push et ve vLLM ile inference optimize et."

**3. Mukemmellik Için:**
> "Production ortaminda fine-tuning pipeline tasarliyorum. Dataset curation (veri kalitesi, deduplication, contamination check), hyperparameter tuning (learning rate schedule, warmup, rank secimi), evaluation (perplexity, task-specific metrics, A/B testing), deployment (ONNX export, quantization, serving) ve monitoring (drift detection, performance degradation) konularini kapsayan end-to-end bir pipeline oluştur."

### Pair Programming Ipucu
Fine-tuning yaparken AI'a training loglarini göster ve sor: "Bu loss curve'de overfitting var mi? Learning rate çok mu yüksek? Early stopping ne zaman yapmaliyim? Rank'i artirmali miyim? Veri kalitesini nasil iyilestirebilirim?"
:::

:::must-note
## Defterine Yaz!

1. **Fine-tuning = transfer learning'in en güçlü hali.** Pre-trained model + senin verin = domain expert model. Sifirdan egitmekten 10-100x daha ucuz ve hızlı.
2. **LoRA mantrasi: "Büyük matrisi iki küçük matrisin carpimiyla yaklasiklastir."** 7B parametreli modelde sadece %0.06 parametre egitirsin, geri kalan döndürülür.
3. **Veri kalitesi > veri miktari.** 100 mükemmel örnek, 10.000 gürültülü örnekten daha iyi sonuç verir. Fine-tuning'de garbage in = garbage out kurali 10x daha geçerli.
4. **Learning rate çok kritik.** Pre-trained modelde büyük learning rate = catastrophic forgetting (model her seyi unutur). Genellikle 1e-5 ile 5e-5 arası kullan.
5. **Eval set olmadan fine-tuning yapma.** Overfitting'i farketmenin tek yolu eval loss'u izlemek. Train/eval split mutlaka yap.
:::

:::senior-learns
## Senior/CTO Boyle Öğrenir

Senior developer fine-tuning ogrenirken sunlara odaklanir:
- **Build vs buy karari**: Fine-tuning mi, prompt engineering mi, RAG mi? Hangi durumda hangisi?
- **Cost modeling**: GPU saati, veri hazırlama maliyeti, inference maliyeti — toplam TCO hesabi
- **Data flywheel**: Production'dan gelen veriyi fine-tuning'e geri besleme döngüsü
- **Evaluation rigor**: Sadece loss'a bakma — task-specific metrikler, human evaluation, A/B test
- **Reproducibility**: Seed, config, data versioning — ayni sonucu tekrar alabilmek
- **Risk assessment**: Catastrophic forgetting, data leakage, benchmark contamination

Senior, Colab'da denemez — hemen **pipeline** kurar, MLflow ile experiment tracking yapar, CI/CD'ye entegre eder.
:::

:::must-note
## Defterine Yaz — Karar Agaci!

```
Gorevine ozel model mi lazim?
├── Hayir → Prompt engineering ile coz (en ucuz, en hizli)
├── Evet, ama verin az (<100 ornek)
│   ├── Few-shot prompting dene
│   └── RAG (Retrieval Augmented Generation) kullan
├── Evet, verin var (100-10K ornek)
│   ├── Compute butcen sinirli → LoRA / QLoRA
│   ├── Compute butcen var → Full fine-tuning
│   └── API kullaniyorsan → OpenAI fine-tuning
└── Evet, cok verin var (10K+)
    ├── Domain-specific model → Full fine-tuning + continued pretraining
    └── Task-specific → LoRA genellikle yeterli
```
:::

---

## 1. Neden Fine-tuning?

:::realworld
## Gerçek Dunya: Fine-tuning Nerede Kullaniliyor?

### Shopify — Urun Kategorizasyonu
Shopify, milyonlarca urunu otomatik kategorize etmek için BERT modelini fine-tune etti. Sonuç: prompt-based yaklasima gore **10x daha düşük latency**, %15 daha yüksek accuracy. Çünkü fine-tuned model tek bir forward pass'te sonuç veriyor — prompt engineering'deki gibi uzun context yok.

### Bloomberg — FinBERT
Bloomberg, finans haberlerini analiz etmek için BERT'i finansal text üzerinde fine-tune ederek **FinBERT**'i olusturdu. Genel BERT sentiment analizinde %80 accuracy verirken, FinBERT finansal sentiment'te %95+ accuracy verdi. Domain-specific veri, genel modeli uzman yapti.

### Bir Startup Hikayesi
Küçük bir Turkiye'deki e-ticaret startup'i, musteri destek chatbot'u için GPT-4o-mini'yi fine-tune etti. 200 örnek conversation ile egitim yaptilar. Sonuç: musteri memnuniyeti %40 artti, çünkü model sirketin urun isimleri, iade politikasi ve uslubunu ogrenip tutarli cevaplar verdi. Maliyet: sadece $5 egitim + $0.0006/1K token inference.

### Prompt Engineering vs Fine-tuning Karsilastirmasi

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Ne Zaman Hangisini Kullan?                       │
├─────────────────────┬───────────────────────┬───────────────────────┤
│                     │  Prompt Engineering    │  Fine-tuning          │
├─────────────────────┼───────────────────────┼───────────────────────┤
│ Veri ihtiyaci       │  0 (sadece talimat)   │  50-10.000+ ornek     │
│ Baslangic suresi    │  Dakikalar            │  Saatler/gunler       │
│ Inference maliyeti  │  Yuksek (uzun prompt) │  Dusuk (kisa prompt)  │
│ Inference latency   │  Yuksek               │  Dusuk                │
│ Tutarlilik          │  Degisken             │  Yuksek               │
│ Domain bilgisi      │  Sinirli              │  Derin                │
│ Guncelleme kolayligi│  Aninda               │  Yeniden egitim lazim │
│ Compute ihtiyaci    │  Yok                  │  GPU gerekli          │
└─────────────────────┴───────────────────────┴───────────────────────┘
```
:::

---

## 2. Transfer Learning Stratejileri

Bir modeli kendi görevine uyarlamanin birden fazla yolu var. Her stratejinin avantajlari, dezavantajlari ve kullanım alanlari farklı.

:::code
## Strateji Karşılaştırma Tablosu

```python
"""
Transfer Learning Stratejileri — Karsilastirma

┌──────────────────────┬──────────────┬───────────────┬───────────────────┐
│ Strateji             │ Egitilen     │ GPU Bellek    │ Ne Zaman Kullan?  │
│                      │ Parametre %  │ Ihtiyaci      │                   │
├──────────────────────┼──────────────┼───────────────┼───────────────────┤
│ Feature Extraction   │ ~1-5%        │ Dusuk         │ Az veri, hizli    │
│ (Son katman)         │              │               │ prototip          │
├──────────────────────┼──────────────┼───────────────┼───────────────────┤
│ Partial Fine-tuning  │ ~10-30%      │ Orta          │ Orta veri,        │
│ (Son N katman)       │              │               │ domain shift az   │
├──────────────────────┼──────────────┼───────────────┼───────────────────┤
│ Full Fine-tuning     │ 100%         │ Cok yuksek    │ Cok veri,         │
│ (Tum katmanlar)      │              │               │ domain shift fazla│
├──────────────────────┼──────────────┼───────────────┼───────────────────┤
│ LoRA / QLoRA         │ ~0.01-1%     │ Dusuk-Orta    │ Buyuk LLM'ler,   │
│ (Low-rank adapters)  │              │               │ sinirli GPU       │
└──────────────────────┴──────────────┴───────────────┴───────────────────┘
"""
```
:::

:::code
## Feature Extraction — Sadece Son Katmani Egit

```python
from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn as nn

# Pre-trained model yukle — tum agirliklar dondurulur
base_model = AutoModel.from_pretrained("distilbert-base-uncased")

# Tum parametreleri dondur (freeze)
for param in base_model.parameters():
    param.requires_grad = False

# Sadece classification head egitilecek
class SentimentClassifier(nn.Module):
    def __init__(self, base_model, num_classes=2):
        super().__init__()
        self.base = base_model
        self.classifier = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes),
        )

    def forward(self, input_ids, attention_mask):
        # Base model frozen — sadece feature extractor olarak kullan
        with torch.no_grad():
            outputs = self.base(input_ids=input_ids, attention_mask=attention_mask)
        # [CLS] token'inin hidden state'i
        cls_output = outputs.last_hidden_state[:, 0, :]
        return self.classifier(cls_output)

model = SentimentClassifier(base_model)

# Kac parametre egitiliyor?
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"Egitilen: {trainable:,} / {total:,} ({trainable/total*100:.2f}%)")
# Output: Egitilen: 197,378 / 66,762,754 (0.30%)
```
:::

:::code
## Partial Fine-tuning — Son N Katmani Ac

```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
)

# Oncelikle tum parametreleri dondur
for param in model.parameters():
    param.requires_grad = False

# Son 2 transformer katmanini ac
for param in model.distilbert.transformer.layer[-2:].parameters():
    param.requires_grad = True

# Classification head'i ac
for param in model.classifier.parameters():
    param.requires_grad = True
for param in model.pre_classifier.parameters():
    param.requires_grad = True

# Kontrol
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"Egitilen: {trainable:,} / {total:,} ({trainable/total*100:.2f}%)")
# Output: Egitilen: ~14.5M / 66.9M (21.7%)
```
:::

:::code
## Strateji Seçim Rehberi

```python
"""
Karar Agaci — Hangi Strateji?

Verin ne kadar?
│
├── < 1.000 ornek
│   ├── Domain benzer (genel NLP) → Feature Extraction
│   └── Domain farkli (tip, hukuk) → LoRA (r=8)
│
├── 1.000 - 10.000 ornek
│   ├── Model kucuk (<1B param) → Full Fine-tuning
│   ├── Model buyuk (1B-10B) → LoRA (r=16-32)
│   └── Model cok buyuk (>10B) → QLoRA (4-bit + LoRA)
│
└── > 10.000 ornek
    ├── Compute butcen var → Full Fine-tuning
    ├── Compute butcen sinirli → LoRA / QLoRA
    └── Cloud API kullaniyorsan → OpenAI Fine-tuning API
"""
```
:::

---

## 3. Hugging Face ile Pratik Fine-tuning

Şimdi elleri kirletme zamani. Hugging Face Transformers kutuphanesi ile **DistilBERT** modelini **IMDB film yorumlari** üzerinde sentiment analizi için fine-tune edecegiz.

:::code
## Ortam Kurulumu

```bash
# uv ile hizli kurulum
uv pip install transformers datasets accelerate scikit-learn tensorboard
uv pip install torch  # GPU varsa: uv pip install torch --index-url https://download.pytorch.org/whl/cu121
```
:::

:::code
## Adim 1: Dataset Hazirlama

```python
from datasets import load_dataset

# IMDB dataset — 50K film yorumu (25K train, 25K test)
dataset = load_dataset("imdb")

print(dataset)
# DatasetDict({
#     train: Dataset({features: ['text', 'label'], num_rows: 25000})
#     test: Dataset({features: ['text', 'label'], num_rows: 25000})
# })

# Bir ornege bakalim
print(dataset["train"][0]["text"][:200])
print(f"Label: {dataset['train'][0]['label']}")  # 0 = negative, 1 = positive

# Hizli deneme icin alt kume alalim (tam egitim icin tamamini kullan)
small_train = dataset["train"].shuffle(seed=42).select(range(5000))
small_test = dataset["test"].shuffle(seed=42).select(range(1000))
```
:::

:::code
## Adim 2: Tokenization

```python
from transformers import AutoTokenizer

# DistilBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Tokenization fonksiyonu
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512,  # IMDB yorumlari uzun olabilir
    )

# Tum dataseti tokenize et (batched=True ile hizli)
tokenized_train = small_train.map(tokenize_function, batched=True)
tokenized_test = small_test.map(tokenize_function, batched=True)

# Gereksiz kolonlari kaldir, format ayarla
tokenized_train.set_format("torch", columns=["input_ids", "attention_mask", "label"])
tokenized_test.set_format("torch", columns=["input_ids", "attention_mask", "label"])

print(f"Tokenized ornek shape: {tokenized_train[0]['input_ids'].shape}")
# Output: torch.Size([512])
```
:::

:::code
## Adim 3: Model Yukleme ve Training

```python
from transformers import AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# Pre-trained DistilBERT + classification head
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2,
    id2label={0: "NEGATIVE", 1: "POSITIVE"},
    label2id={"NEGATIVE": 0, "POSITIVE": 1},
)

# Metrik hesaplama fonksiyonu
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, predictions),
        "f1": f1_score(labels, predictions, average="weighted"),
        "precision": precision_score(labels, predictions, average="weighted"),
        "recall": recall_score(labels, predictions, average="weighted"),
    }

# Training arguments
training_args = TrainingArguments(
    output_dir="./results/distilbert-imdb",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    learning_rate=2e-5,           # Pre-trained model icin dusuk LR!
    warmup_steps=500,             # Ilk 500 adim LR yavas artar
    weight_decay=0.01,            # Regularization
    logging_dir="./logs",
    logging_steps=100,
    eval_strategy="epoch",        # Her epoch sonunda evaluate et
    save_strategy="epoch",
    load_best_model_at_end=True,  # En iyi modeli yukle
    metric_for_best_model="f1",   # F1'e gore en iyi modeli sec
    report_to="tensorboard",      # TensorBoard'da gorsellestir
    fp16=True,                    # Mixed precision — 2x hizli egitim
)

# Trainer olustur
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
    compute_metrics=compute_metrics,
)

# Egitimi baslat!
train_result = trainer.train()

# Sonuclari yazdir
print(f"\nEgitim suresi: {train_result.metrics['train_runtime']:.1f} saniye")
print(f"Train loss: {train_result.metrics['train_loss']:.4f}")

# Final evaluation
eval_results = trainer.evaluate()
print(f"\nEval Accuracy: {eval_results['eval_accuracy']:.4f}")
print(f"Eval F1: {eval_results['eval_f1']:.4f}")
# Beklenen: ~92-93% accuracy (5K ornekle bile!)
```
:::

:::code
## Adim 4: Modeli Kaydet ve Kullan

```python
# Modeli ve tokenizer'i kaydet
trainer.save_model("./my-sentiment-model")
tokenizer.save_pretrained("./my-sentiment-model")

# Kaydedilen modeli yukle ve kullan
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="./my-sentiment-model",
    tokenizer="./my-sentiment-model",
)

# Test et
results = classifier([
    "This movie was absolutely fantastic! Best I've seen in years.",
    "Terrible acting, boring plot. Complete waste of time.",
    "It was okay, nothing special but not bad either.",
])

for r in results:
    print(f"{r['label']}: {r['score']:.4f}")
# POSITIVE: 0.9987
# NEGATIVE: 0.9991
# NEGATIVE: 0.6234  (belirsiz — model dogru sekilde emin degil)
```
:::

:::beginner-mistake
## Hata: Tüm Dataset'i Tokenize Etmeden Önce Bakmamak

```python
# YANLIS — Veri kalitesini kontrol etmeden direkt tokenize etmek
tokenized = dataset.map(tokenize_function, batched=True)
trainer.train()  # Kotu veri varsa model kotu ogrenecek!

# DOGRU — Oncelikle verini tani
print(f"Train boyutu: {len(dataset['train'])}")
print(f"Label dagilimi: {dataset['train'].to_pandas()['label'].value_counts()}")

# Ornek verilere bak
for i in range(5):
    text = dataset["train"][i]["text"]
    label = dataset["train"][i]["label"]
    print(f"[{label}] {text[:100]}...")

# Bos veya cok kisa ornekleri filtrele
dataset = dataset.filter(lambda x: len(x["text"].split()) > 10)
```

**Neden önemli:** Verideki gurultu (spam, bos text, yanlis etiketler) modeli bozar. Fine-tuning'de veri kalitesi her seydir.
:::

---

## 4. LoRA ve PEFT — Büyük Modelleri Küçük Butceyle Fine-tune Et

LoRA (Low-Rank Adaptation), fine-tuning dunyasinda bir devrim. 7 milyar parametreli bir modeli, sadece **4 milyon parametre** egiterek uyarlayabilirsin. Nasil mi?

### 4.1 LoRA Intuition

Bir neural network katmanindaki weight matrisi `W` düşün. Bu matris `d x d` boyutunda (örneğin 4096 x 4096 = 16.7M parametre). Full fine-tuning'de bu matrisin **tüm** elemanlarini güncelliyorsun.

LoRA'nin temel fikri şu: Fine-tuning sırasında weight'lerdeki **değişim** (`ΔW`) aslinda **low-rank** bir matris. Yani bu devasa değişimi, iki küçük matrisin carpimi ile yaklasiklastirabiliriz.

```
Orijinal:  W_yeni = W_eski + ΔW
           (d x d)   (d x d)   (d x d)   ← 16.7M parametre guncellenir

LoRA:      W_yeni = W_eski + A * B
           (d x d)   (d x d)  (d x r)(r x d)  ← sadece 2*d*r parametre
                      frozen   trainable

Ornek (d=4096, r=16):
- Full:  4096 x 4096 = 16,777,216 parametre
- LoRA:  (4096 x 16) + (16 x 4096) = 131,072 parametre
- Kazanc: 128x daha az parametre!
```

:::code
## LoRA Mimarisi — Görsel Açıklama

```python
"""
LoRA Mimarisi — Detayli Gorsel

Input (x)
    │
    ├──────────────────────────────┐
    │                              │
    ▼                              ▼
┌─────────────┐            ┌─────────────┐
│  W (frozen) │            │   A (d→r)   │  ← Trainable, random init
│  d x d      │            │   d x r     │
│  16.7M param│            └──────┬──────┘
│  DONDURULMUS│                   │
└──────┬──────┘                   ▼
       │                  ┌─────────────┐
       │                  │   B (r→d)   │  ← Trainable, zero init
       │                  │   r x d     │
       │                  └──────┬──────┘
       │                         │
       │                         │ × (alpha/r)  ← Scaling factor
       │                         │
       ▼                         ▼
    ┌─────────────────────────────────┐
    │         h = Wx + (α/r)BAx       │
    │         Toplama (merge)          │
    └─────────────────────────────────┘
                   │
                   ▼
              Output (h)

Neden calisiyor?
- B sifir ile baslatilir → baslangicta LoRA etkisi YOK
- Egitim ilerledikce A ve B, goreve ozel adaptasyonu ogrenir
- Inference'da A*B orijinal W'ye eklenir → ek latency YOK
"""
```
:::

:::deha-tip
## Deha Tipi: Rank (r) Secimi

Rank (`r`) LoRA'nin en kritik hyperparameter'i:

- **r = 4-8:** Basit görevler (sentiment, classification). Az parametre, hızlı egitim.
- **r = 16-32:** Orta zorlukta görevler (summarization, QA). Iyi denge.
- **r = 64-128:** Karmaşık görevler (code generation, multi-task). Daha fazla kapasite.

**Pratik kural:** `r=16` ile başla. Eval performansı yetersizse artir, overfitting varsa azalt.

Bir diger trick: `lora_alpha = 2 * r` genellikle iyi çalışır. Alpha, LoRA'nin etkisini ölçekler — çok yüksekse instability, çok düşükse yetersiz adaptasyon.
:::

### 4.2 LoRA ile LLM Fine-tuning

:::code
## LoRA Kurulumu

```bash
# PEFT kutuphanesini kur (Hugging Face'in LoRA implementasyonu)
uv pip install peft bitsandbytes accelerate transformers datasets trl
```
:::

:::code
## LoRA ile Model Hazırlama

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

# Base model yukle
model_name = "meta-llama/Llama-2-7b-hf"  # veya "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",           # GPU'lara otomatik dagit
    torch_dtype=torch.float16,   # Bellek tasarrufu
)

# LoRA konfigurasyonu
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                              # Rank — dusuk = az parametre
    lora_alpha=32,                     # Scaling factor (genellikle 2*r)
    lora_dropout=0.05,                 # Regularization
    target_modules=[
        "q_proj", "v_proj",            # Attention katmanlarinda Q ve V
        # "k_proj", "o_proj",          # Daha fazla kapasite istersen bunlari da ac
        # "gate_proj", "up_proj",      # MLP katmanlari — nadiren gerekli
    ],
    bias="none",                       # Bias terimlerini egitme
)

# PEFT model olustur
peft_model = get_peft_model(model, lora_config)

# Egitilen parametre sayisina bak
peft_model.print_trainable_parameters()
# Output: "trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%"
# 6.7 MILYAR parametreden sadece 4.2 MILYON parametre egitiliyor!
```
:::

:::code
## LoRA Target Module Secimi

```python
"""
Hangi katmanlara LoRA uygulanmali?

Model Mimarisi (Transformer katmani):
┌─────────────────────────────────────┐
│ Self-Attention:                     │
│   q_proj ← LoRA (genellikle)       │
│   k_proj ← LoRA (opsiyonel)        │
│   v_proj ← LoRA (genellikle)       │
│   o_proj ← LoRA (opsiyonel)        │
├─────────────────────────────────────┤
│ MLP (Feed-Forward):                │
│   gate_proj ← LoRA (nadiren)       │
│   up_proj   ← LoRA (nadiren)       │
│   down_proj ← LoRA (nadiren)       │
└─────────────────────────────────────┘

Pratik kurallar:
- Minimum: q_proj + v_proj (en yaygin, cogu gorev icin yeterli)
- Orta:    q_proj + k_proj + v_proj + o_proj (daha iyi performance)
- Maksimum: Tum attention + MLP (en cok parametre, en iyi fit)
"""

# Modeldeki tum lineer katmanlari bul
from peft.utils import TRANSFORMERS_MODELS_TO_LORA_TARGET_MODULES_MAPPING

# Hangi katmanlara LoRA uygulanabilir?
for name, module in model.named_modules():
    if isinstance(module, torch.nn.Linear):
        print(f"  {name}: {module.in_features} x {module.out_features}")
```
:::

:::code
## LoRA Training — Instruction Fine-tuning Örneği

```python
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

# Instruction dataset yukle (ornek: Alpaca formati)
dataset = load_dataset("tatsu-lab/alpaca", split="train[:5000]")

# Prompt template
def format_instruction(example):
    if example.get("input", ""):
        text = f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
    else:
        text = f"""### Instruction:
{example['instruction']}

### Response:
{example['output']}"""
    return {"text": text}

# Dataseti formatla
formatted_dataset = dataset.map(format_instruction)

# SFT (Supervised Fine-Tuning) Trainer
sft_config = SFTConfig(
    output_dir="./results/lora-llama",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,     # Effective batch size = 4 * 4 = 16
    learning_rate=2e-4,                # LoRA icin 2e-4 genellikle iyi
    warmup_ratio=0.03,
    logging_steps=25,
    save_strategy="epoch",
    fp16=True,
    max_seq_length=1024,
    dataset_text_field="text",
)

trainer = SFTTrainer(
    model=peft_model,
    train_dataset=formatted_dataset,
    args=sft_config,
    tokenizer=tokenizer,
)

# Egitimi baslat
trainer.train()

# LoRA adapter'larini kaydet (cok kucuk — sadece ~17MB)
peft_model.save_pretrained("./lora-adapters")
```
:::

:::code
## LoRA Adapter'larini Yükleme ve Kullanma

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Base modeli yukle
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    device_map="auto",
    torch_dtype=torch.float16,
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# LoRA adapter'larini yukle
model = PeftModel.from_pretrained(base_model, "./lora-adapters")

# Inference
prompt = "### Instruction:\nTurkiye'nin baskenti neresidir?\n\n### Response:\n"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        do_sample=True,
    )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# --- BONUS: Adapter'lari base modele birlesitir (merge) ---
merged_model = model.merge_and_unload()
# Artik adapter olmadan, tek bir model olarak kaydedebilirsin
merged_model.save_pretrained("./merged-model")
# Bu model normal model gibi yuklenir — ek LoRA dependency yok
```
:::

### 4.3 QLoRA — 4-bit Quantization + LoRA

QLoRA, LoRA'yi bir adim oteye tasir: base modeli **4-bit quantization** ile yükler. Boylece 7B parametreli model **~4GB GPU RAM** ile fine-tune edilebilir — normal sartlarda ~28GB gerekir!

:::code
## QLoRA Implementasyonu

```python
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 4-bit quantization konfigurasyonu
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,                 # 4-bit yukle (16-bit yerine)
    bnb_4bit_quant_type="nf4",         # NormalFloat4 — en iyi 4-bit format
    bnb_4bit_compute_dtype=torch.float16,  # Hesaplama 16-bit'te yapilir
    bnb_4bit_use_double_quant=True,    # Quantization parametrelerini de quantize et
)

# Modeli 4-bit olarak yukle
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto",
)

# 4-bit model icin gradient hazirla
model = prepare_model_for_kbit_training(model)

# LoRA config (QLoRA'da genellikle daha agresif rank kullanilir)
lora_config = LoraConfig(
    r=64,                      # QLoRA'da daha yuksek rank kullanilabilir
    lora_alpha=16,             # alpha/r orani onemli
    lora_dropout=0.1,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",  # Tum attention katmanlari
        "gate_proj", "up_proj", "down_proj",      # MLP katmanlari da
    ],
    bias="none",
    task_type="CAUSAL_LM",
)

peft_model = get_peft_model(model, lora_config)
peft_model.print_trainable_parameters()

# Bellek karsilastirmasi
print(f"""
Bellek Karsilastirmasi (7B model):
┌─────────────────────┬──────────────┐
│ Yontem              │ GPU RAM      │
├─────────────────────┼──────────────┤
│ Full Fine-tuning    │ ~28 GB       │
│ LoRA (16-bit)       │ ~16 GB       │
│ QLoRA (4-bit)       │ ~4 GB        │
└─────────────────────┴──────────────┘
""")
# QLoRA ile 7B model tek bir RTX 3060 (12GB) uzerinde bile calisir!
```
:::

:::code
## QLoRA Training Loop

```python
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# Dataset yukle — Turkce instruction dataseti ornegi
# Gercek projede kendi verinizi kullanin
dataset = load_dataset("tatsu-lab/alpaca", split="train[:2000]")

def format_chat(example):
    return {
        "text": f"<s>[INST] {example['instruction']} [/INST] {example['output']}</s>"
    }

dataset = dataset.map(format_chat)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
tokenizer.pad_token = tokenizer.eos_token

# QLoRA icin optimize edilmis training args
sft_config = SFTConfig(
    output_dir="./results/qlora-llama",
    num_train_epochs=1,                # QLoRA'da 1-3 epoch yeterli
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_ratio=0.03,
    max_grad_norm=0.3,                 # Gradient clipping — stabilite icin
    logging_steps=10,
    save_strategy="steps",
    save_steps=100,
    fp16=True,
    optim="paged_adamw_8bit",          # 8-bit optimizer — bellek tasarrufu
    max_seq_length=512,
    dataset_text_field="text",
    gradient_checkpointing=True,       # Bellek/hiz tradeoff — bellek kazandirir
)

trainer = SFTTrainer(
    model=peft_model,
    train_dataset=dataset,
    args=sft_config,
    tokenizer=tokenizer,
)

trainer.train()

# Adapter'lari kaydet (sadece ~80MB — QLoRA'da rank yuksek olsa bile kucuk)
peft_model.save_pretrained("./qlora-adapters")
```
:::

:::warning
## Dikkat: Compute ve Maliyet Farkindaigi

Fine-tuning **bedava değildir.** GPU saatleri hızla birikir:

```
Maliyet Tahmini (2026 fiyatlari):
┌─────────────────────┬──────────────┬───────────────┬──────────────┐
│ Model               │ GPU          │ Sure          │ Tahmini Ucret│
├─────────────────────┼──────────────┼───────────────┼──────────────┤
│ DistilBERT (66M)    │ T4 (16GB)    │ ~30 dk        │ ~$0.50       │
│ LLaMA-2 7B (LoRA)   │ A100 (40GB)  │ ~2-4 saat     │ ~$8-16       │
│ LLaMA-2 7B (QLoRA)  │ RTX 3090     │ ~3-6 saat     │ ~$0 (kendi)  │
│ LLaMA-2 7B (Full)   │ 4x A100      │ ~8-12 saat    │ ~$80-120     │
│ LLaMA-2 70B (QLoRA) │ 2x A100      │ ~24-48 saat   │ ~$100-200    │
└─────────────────────┴──────────────┴───────────────┴──────────────┘
```

**Altin kurallar:**
1. Her zaman en küçük modelle başla (DistilBERT, GPT-4o-mini, Phi-3)
2. Küçük veri alt kumesiyle hızlı deney yap (sanity check)
3. Gerçek maliyeti hesapla: GPU + veri hazırlama + mühendis saati
4. Google Colab (ücretsiz T4) ile prototip yap, sonra ölçeklendir
:::

:::beginner-mistake
## Hata: Eval Set Kullanmamak

```python
# YANLIS — Tum veriyle egitim, evaluation yok
trainer = Trainer(
    model=model,
    train_dataset=full_dataset,  # Test seti ayirmadin!
    # eval_dataset= ???  ← YOK!
)
trainer.train()
# Sonuc: Model ezberliyor, sen farketmiyorsun

# DOGRU — Train/eval/test split yap
from datasets import DatasetDict

dataset = dataset.train_test_split(test_size=0.2, seed=42)
train_eval = dataset["train"].train_test_split(test_size=0.1, seed=42)

splits = DatasetDict({
    "train": train_eval["train"],       # %72 — egitim
    "validation": train_eval["test"],   # %8  — hyperparameter tuning
    "test": dataset["test"],            # %20 — final degerlendirme
})

trainer = Trainer(
    model=model,
    train_dataset=splits["train"],
    eval_dataset=splits["validation"],  # Her epoch sonunda degerlendir
    compute_metrics=compute_metrics,
)
```

**Neden önemli:** Eval set olmadan overfitting'i farkedemezsin. Model train verisini ezberler ama yeni veride başarısız olur.
:::

---

## 5. OpenAI Fine-tuning API

Kendi GPU'n yoksa veya hızlı sonuç istiyorsan, OpenAI'in Fine-tuning API'si en kolay yol.

:::code
## OpenAI Fine-tuning — Dataset Hazirlama

```python
import json

# JSONL formati — OpenAI'in bekledig format
# Her satir bir JSON objesi, "messages" listesi icermeli
training_examples = [
    {
        "messages": [
            {"role": "system", "content": "Sen bir e-ticaret musteri destek asistanisin. Kibarca, net ve cozum odakli cevap ver."},
            {"role": "user", "content": "Siparisim 3 gundur gelmedi, ne oldu?"},
            {"role": "assistant", "content": "Gecikme icin ozur dilerim. Siparis numaranizi paylasir misiniz? Kargo durumunu hemen kontrol edip size bilgi verecegim. Genellikle kargo gecikmeleri hava kosullari veya yogunluktan kaynaklanir."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "Sen bir e-ticaret musteri destek asistanisin. Kibarca, net ve cozum odakli cevap ver."},
            {"role": "user", "content": "Urunu iade etmek istiyorum nasil yapabilirim?"},
            {"role": "assistant", "content": "Iade islemi icin su adimlari takip edebilirsiniz:\n1. Hesabinizdan 'Siparislerim' bolumune gidin\n2. Iade etmek istediginiz urunu secin\n3. 'Iade Talebi Olustur' butonuna tiklayin\n4. Iade nedeninizi secin\n\nUrun 14 gun icinde iade edilebilir. Kargo ucreti tarafimizca karsilanir."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "Sen bir e-ticaret musteri destek asistanisin. Kibarca, net ve cozum odakli cevap ver."},
            {"role": "user", "content": "Indirim kodu calismadi"},
            {"role": "assistant", "content": "Indirim kodunun calismamasi birkaç nedenden kaynaklanabilir:\n- Kodun suresi dolmus olabilir\n- Minimum sepet tutarina ulasilmamis olabilir\n- Kod baska bir sipariste kullanilmis olabilir\n\nKullanmaya calistiginiz kodu paylasir misiniz? Durumunu kontrol edip gerekirse yeni bir kod olusturabilirim."},
        ]
    },
    # ... minimum 10, ideal 50-100 ornek daha ekle
]

# Veri kalitesi kontrol
def validate_training_data(examples):
    errors = []
    for i, ex in enumerate(examples):
        messages = ex.get("messages", [])
        if len(messages) < 2:
            errors.append(f"Ornek {i}: En az 2 mesaj olmali (user + assistant)")
        roles = [m["role"] for m in messages]
        if "assistant" not in roles:
            errors.append(f"Ornek {i}: Assistant mesaji yok")
        if roles[-1] != "assistant":
            errors.append(f"Ornek {i}: Son mesaj assistant olmali")
        for m in messages:
            if len(m["content"]) < 5:
                errors.append(f"Ornek {i}: Cok kisa mesaj — '{m['content']}'")
    return errors

errors = validate_training_data(training_examples)
if errors:
    for e in errors:
        print(f"HATA: {e}")
else:
    print("Veri gecerli!")

# JSONL dosyasina yaz
with open("training_data.jsonl", "w", encoding="utf-8") as f:
    for example in training_examples:
        f.write(json.dumps(example, ensure_ascii=False) + "\n")

print(f"Toplam {len(training_examples)} ornek yazildi.")
```
:::

:::code
## OpenAI Fine-tuning — Egitimi Baslat

```python
from openai import OpenAI

client = OpenAI()  # OPENAI_API_KEY env variable'dan okur

# 1. Training dosyasini yukle
training_file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune",
)
print(f"Dosya yuklendi: {training_file.id}")

# 2. (Opsiyonel) Validation dosyasini yukle
# validation_file = client.files.create(
#     file=open("validation_data.jsonl", "rb"),
#     purpose="fine-tune",
# )

# 3. Fine-tuning job'i baslat
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4o-mini-2024-07-18",    # En ucuz ve hizli secim
    hyperparameters={
        "n_epochs": 3,                  # 3 epoch genellikle yeterli
        # "batch_size": "auto",         # OpenAI otomatik ayarlar
        # "learning_rate_multiplier": 1.0,
    },
    suffix="musteri-destek",            # Model ismine ek: ft:gpt-4o-mini:...:musteri-destek:...
)
print(f"Fine-tuning basladi: {job.id}")

# 4. Durumu izle
import time

while True:
    status = client.fine_tuning.jobs.retrieve(job.id)
    print(f"Durum: {status.status}")
    if status.status in ["succeeded", "failed", "cancelled"]:
        break
    time.sleep(60)  # Her dakika kontrol et

# 5. Basarili ise modeli kullan
if status.status == "succeeded":
    fine_tuned_model = status.fine_tuned_model
    print(f"Model hazir: {fine_tuned_model}")
    # Ornek: "ft:gpt-4o-mini-2024-07-18:my-org::9abc1234"

    # Fine-tuned modeli kullan
    response = client.chat.completions.create(
        model=fine_tuned_model,
        messages=[
            {"role": "system", "content": "Sen bir e-ticaret musteri destek asistanisin."},
            {"role": "user", "content": "Urun degisimi yapabilir miyim?"},
        ],
    )
    print(response.choices[0].message.content)
```
:::

:::code
## OpenAI Fine-tuning — Maliyet Tablosu

```python
"""
OpenAI Fine-tuning Maliyetleri (2026):

┌───────────────────────┬─────────────────┬──────────────────┐
│ Model                 │ Egitim Maliyeti │ Inference        │
│                       │ (per 1K token)  │ (per 1K token)   │
├───────────────────────┼─────────────────┼──────────────────┤
│ gpt-4o-mini (fine-tune) │ $0.003        │ $0.0006 (input)  │
│                       │                 │ $0.0024 (output) │
├───────────────────────┼─────────────────┼──────────────────┤
│ gpt-4o (fine-tune)    │ $0.008          │ $0.00375 (input) │
│                       │                 │ $0.015 (output)  │
└───────────────────────┴─────────────────┴──────────────────┘

Ornek maliyet hesabi:
- 100 ornek × ortalama 500 token × 3 epoch = 150K token egitim
- Egitim maliyeti: 150 × $0.003 = $0.45 (yarim dolardan az!)
- 1000 musteri sorgusu × 200 token = 200K token inference
- Inference maliyeti: 200 × $0.0006 = $0.12

Toplam: $0.57 ile kendi fine-tuned modelini olusturup 1000 sorgu yanıtladin.
"""
```
:::

:::beginner-mistake
## Hata: Çok Az Ornekle Fine-tune Etmek

```python
# YANLIS — 5 ornekle fine-tuning
training_data = [
    {"messages": [...]},  # Ornek 1
    {"messages": [...]},  # Ornek 2
    {"messages": [...]},  # Ornek 3
    {"messages": [...]},  # Ornek 4
    {"messages": [...]},  # Ornek 5
]
# Sonuc: Model ogrenecek kadar veri yok, overfitting garanti

# DOGRU — Yeterli ve cesitli ornek
# OpenAI minimum 10 ornek kabul eder, AMA:
# - Basit gorevler: 50-100 ornek
# - Orta gorevler: 100-500 ornek
# - Karmasik gorevler: 500-5000 ornek
#
# DAHA ONEMLI: Cesitlilik!
# 100 farkli senaryo > 500 benzer ornek
# Edge case'leri, farkli yazim stillerini, hata durumlarini icermeli
```

**Neden önemli:** Az veriyle model genelleme yapamaz. "Siparisim nerede?" sorusunu ogrenebilir ama "Kargomu takip edemiyorum" dediginde cope yanar.
:::

---

## 6. Evaluation — Modelin Gerçekten Iyilesti mi?

Fine-tuning yaptiktan sonra en kritik soru: **Model gerçekten daha mi iyi oldu?** Bunu olcmek için sistematik evaluation yapman gerekiyor.

:::code
## Loss Curve Analizi — Overfitting Tespiti

```python
import matplotlib.pyplot as plt

def plot_training_curves(trainer):
    """Training ve eval loss curve'lerini ciz."""
    history = trainer.state.log_history

    train_loss = [(h["step"], h["loss"]) for h in history if "loss" in h]
    eval_loss = [(h["step"], h["eval_loss"]) for h in history if "eval_loss" in h]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Loss curve
    axes[0].plot(*zip(*train_loss), label="Train Loss", color="blue")
    axes[0].plot(*zip(*eval_loss), label="Eval Loss", color="red", marker="o")
    axes[0].set_xlabel("Step")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Training vs Evaluation Loss")
    axes[0].legend()
    axes[0].grid(True)

    # Eval metrikleri
    eval_acc = [(h["step"], h["eval_accuracy"]) for h in history if "eval_accuracy" in h]
    eval_f1 = [(h["step"], h["eval_f1"]) for h in history if "eval_f1" in h]

    axes[1].plot(*zip(*eval_acc), label="Accuracy", color="green", marker="o")
    axes[1].plot(*zip(*eval_f1), label="F1 Score", color="purple", marker="s")
    axes[1].set_xlabel("Step")
    axes[1].set_ylabel("Score")
    axes[1].set_title("Evaluation Metrics")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig("training_curves.png", dpi=150)
    plt.show()

# Kullanim
plot_training_curves(trainer)

"""
Nasil yorumlanir?

1. IYI: Train loss ve eval loss birlikte dusuyor
   → Model ogreniyor VE genelleme yapiyor

2. KOTU — Overfitting:
   Train loss dusuyor AMA eval loss artiyor
   → Model ezberlemeye baslamis. Cozum:
     - Early stopping kullan
     - Veri miktarini artir
     - Dropout artir
     - Learning rate azalt

3. KOTU — Underfitting:
   Train loss bile dusmuyor
   → Model ogrenemiyor. Cozum:
     - Learning rate artir
     - Epoch sayisini artir
     - Model kapasitesini artir (rank'i yukselt)
"""
```
:::

:::code
## Evaluation Metrikleri — BLEU, ROUGE, F1

```python
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# --- Classification Metrikleri ---
def evaluate_classification(trainer, test_dataset):
    """Detayli classification raporu olustur."""
    predictions = trainer.predict(test_dataset)
    preds = np.argmax(predictions.predictions, axis=-1)
    labels = predictions.label_ids

    # Detayli rapor
    report = classification_report(
        labels, preds,
        target_names=["NEGATIVE", "POSITIVE"],
        digits=4,
    )
    print(report)

    # Confusion matrix
    cm = confusion_matrix(labels, preds)
    print(f"\nConfusion Matrix:")
    print(f"                Predicted")
    print(f"                NEG    POS")
    print(f"Actual NEG   [{cm[0][0]:5d}  {cm[0][1]:5d}]")
    print(f"       POS   [{cm[1][0]:5d}  {cm[1][1]:5d}]")

evaluate_classification(trainer, tokenized_test)


# --- Generative Metrikler (LLM'ler icin) ---
# uv pip install rouge-score nltk
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def evaluate_generation(model, tokenizer, test_examples):
    """Generative model icin BLEU ve ROUGE hesapla."""
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    smooth = SmoothingFunction().method1

    all_bleu = []
    all_rouge = {"rouge1": [], "rouge2": [], "rougeL": []}

    for example in test_examples:
        # Model ciktisi
        inputs = tokenizer(example["input"], return_tensors="pt").to("cuda")
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=256)
        prediction = tokenizer.decode(output[0], skip_special_tokens=True)

        reference = example["expected_output"]

        # BLEU (n-gram precision)
        ref_tokens = reference.split()
        pred_tokens = prediction.split()
        bleu = sentence_bleu([ref_tokens], pred_tokens, smoothing_function=smooth)
        all_bleu.append(bleu)

        # ROUGE (recall-based)
        scores = scorer.score(reference, prediction)
        for key in all_rouge:
            all_rouge[key].append(scores[key].fmeasure)

    print(f"BLEU Score: {np.mean(all_bleu):.4f}")
    for key in all_rouge:
        print(f"{key}: {np.mean(all_rouge[key]):.4f}")

"""
Metrik Rehberi:
┌──────────┬──────────────────────────────────────────┐
│ Metrik   │ Ne Olcer?                                │
├──────────┼──────────────────────────────────────────┤
│ Accuracy │ Dogruyanitlanma orani                    │
│ F1       │ Precision/Recall dengesi                 │
│ BLEU     │ n-gram precision (ceviri/generation)     │
│ ROUGE    │ n-gram recall (ozetleme)                 │
│ Perplexity│ Model ne kadar surpriz oluyor           │
└──────────┴──────────────────────────────────────────┘
"""
```
:::

:::code
## A/B Testing: Base Model vs Fine-tuned Model

```python
from transformers import pipeline

def compare_models(base_model_path, finetuned_model_path, test_cases):
    """Base ve fine-tuned modeli yan yana karsilastir."""
    base_pipe = pipeline("text-generation", model=base_model_path, max_new_tokens=200)
    ft_pipe = pipeline("text-generation", model=finetuned_model_path, max_new_tokens=200)

    results = []
    for test in test_cases:
        base_output = base_pipe(test["prompt"])[0]["generated_text"]
        ft_output = ft_pipe(test["prompt"])[0]["generated_text"]

        results.append({
            "prompt": test["prompt"],
            "expected": test.get("expected", "N/A"),
            "base_output": base_output,
            "finetuned_output": ft_output,
        })

        print(f"\n{'='*60}")
        print(f"PROMPT: {test['prompt'][:100]}...")
        print(f"\nBASE MODEL:\n{base_output[:300]}...")
        print(f"\nFINE-TUNED:\n{ft_output[:300]}...")
        if test.get("expected"):
            print(f"\nBEKLENEN:\n{test['expected'][:300]}...")

    return results

# Test cases
test_cases = [
    {
        "prompt": "Siparisim nerede kaldi?",
        "expected": "Siparis numaranizi paylasir misiniz?",
    },
    {
        "prompt": "Urun bozuk cikti ne yapmaliyim?",
        "expected": "Urun fotografi cekin, iade talebi olusturun.",
    },
]

# Karsilastir
# compare_models("base-model", "./my-finetuned-model", test_cases)
```
:::

---

## 7. Production'a Tasima

Fine-tuned modelini egittin ve degerledirdin. Şimdi production'a tasimanin zamani.

:::code
## Model Export — Safetensors ve ONNX

```python
# --- Safetensors (Hugging Face standart formati) ---
# Modern ve guvenli format — pickle yerine safetensors kullan
model.save_pretrained("./production-model", safe_serialization=True)
tokenizer.save_pretrained("./production-model")
# Bu format Hugging Face Hub, vLLM, TGI ile uyumlu

# --- ONNX Export (CPU inference icin optimize) ---
# uv pip install optimum onnx onnxruntime
from optimum.onnxruntime import ORTModelForSequenceClassification

# PyTorch modelini ONNX'e cevir
ort_model = ORTModelForSequenceClassification.from_pretrained(
    "./production-model",
    export=True,  # Otomatik ONNX'e cevir
)
ort_model.save_pretrained("./production-model-onnx")

# ONNX model ile inference (~2-3x daha hizli CPU'da)
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline

ort_model = ORTModelForSequenceClassification.from_pretrained("./production-model-onnx")
tokenizer = AutoTokenizer.from_pretrained("./production-model-onnx")

classifier = pipeline("sentiment-analysis", model=ort_model, tokenizer=tokenizer)
result = classifier("Bu urun harika!")
print(result)  # [{'label': 'POSITIVE', 'score': 0.9982}]
```
:::

:::code
## Hugging Face Hub'a Push

```python
from huggingface_hub import login

# Token ile giris (huggingface.co/settings/tokens)
login(token="hf_...")

# Modeli Hub'a push et
model.push_to_hub("kullanici-adi/sentiment-turkish", private=True)
tokenizer.push_to_hub("kullanici-adi/sentiment-turkish", private=True)

# LoRA adapter'larini push et (cok kucuk — sadece adaptorler)
peft_model.push_to_hub("kullanici-adi/sentiment-turkish-lora", private=True)

# Baskasi nasil kullanir?
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="kullanici-adi/sentiment-turkish",
)
```
:::

:::code
## Inference Optimizasyonu — vLLM

```python
# vLLM — Production icin en hizli LLM inference engine
# uv pip install vllm

# Komut satirindan server baslat:
# python -m vllm.entrypoints.openai.api_server \
#     --model ./merged-model \
#     --port 8000 \
#     --max-model-len 4096

# Python client ile kullan (OpenAI uyumlu API)
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy",  # vLLM icin gerekli degil ama client istiyor
)

response = client.chat.completions.create(
    model="./merged-model",
    messages=[
        {"role": "user", "content": "Siparisimi iade etmek istiyorum"},
    ],
    temperature=0.7,
    max_tokens=256,
)
print(response.choices[0].message.content)

"""
vLLM Avantajlari:
- Continuous batching — birden fazla istegi ayni anda isler
- PagedAttention — KV cache'i verimli yonetir
- ~3-5x daha hizli inference (HuggingFace Transformers'a gore)
- OpenAI uyumlu API — mevcut kodu degistirmene gerek yok
"""
```
:::

---

## Alıştırmalar

:::exercise
## Alıştırma 1: Hugging Face ile Sentiment Fine-tuning

**Görev:** DistilBERT modelini Turkce sentiment analizi için fine-tune et.

**Adimlar:**
1. `tyqiangz/multilingual-sentiments` datasetini yükle (Turkce subset)
2. Tokenize et (max_length=256)
3. TrainingArguments ile egit (3 epoch, lr=2e-5)
4. Eval accuracy ve F1'i raporla
5. 5 Turkce cumle ile test et

**Başlangıç kodu:**
```python
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

# 1. Dataset
dataset = load_dataset("tyqiangz/multilingual-sentiments", "turkish")
# Ipucu: dataset["train"], dataset["validation"], dataset["test"] mevcut

# 2. Tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")

# 3. Tokenize
def tokenize(batch):
    # SENIN KODUN

# 4. Model
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-multilingual-cased",
    num_labels=3,  # positive, negative, neutral
)

# 5. Training
# SENIN KODUN

# 6. Test
test_sentences = [
    "Bu film harikaydı, kesinlikle tavsiye ederim!",
    "Berbat bir deneyimdi, bir daha gitmem.",
    "Fiyatı normal, kalitesi ortalama.",
    "Hayal kırıklığına uğradım, beklentilerimi karşılamadı.",
    "Müthiş bir ürün, çok memnunum!",
]
# SENIN KODUN
```

**Beklenen çıktı:** Eval accuracy > %85, F1 > %83
:::

:::exercise
## Alıştırma 2: LoRA ile Text Generation

**Görev:** Bir LLM'i LoRA ile Turkce soru-cevap formati için fine-tune et.

**Adimlar:**
1. Küçük bir model seç (örneğin `microsoft/phi-2` veya `TinyLlama/TinyLlama-1.1B-Chat-v1.0`)
2. LoRA config oluştur (r=16, alpha=32, target_modules için modele uygun seçim yap)
3. 100+ Turkce soru-cevap cifti hazırla (veya mevcut dataset kullan)
4. SFTTrainer ile 1-2 epoch egit
5. Base model vs fine-tuned model ciktisini karşılaştır

**Ipuclari:**
- `target_modules` modelden modele değişir — `model.named_modules()` ile kontrol et
- QLoRA kullanarak GPU belleginden tasarruf edebilirsin
- `gradient_checkpointing=True` bellek kazandirir
:::

:::exercise
## Alıştırma 3: OpenAI Fine-tuning — Musteri Destek Botu

**Görev:** GPT-4o-mini'yi musteri destek chatbot'u olarak fine-tune et.

**Adimlar:**
1. En az 50 musteri destek conversasyonu hazırla (JSONL format)
2. Şu kategorileri icermeli: sipariş takibi, iade, sikayet, urun bilgisi, odeme
3. Her örnekte system prompt + user + assistant mesaji olmali
4. OpenAI API ile fine-tuning job'i başlat
5. Fine-tuned modeli test et ve base model ile karşılaştır

**Veri hazırlama ipuclari:**
```python
categories = {
    "siparis_takibi": 10,   # ornek
    "iade": 10,
    "sikayet": 10,
    "urun_bilgisi": 10,
    "odeme": 10,
}
# Her kategoriden esit sayida ornek topla
# Edge case'leri unutma: kirik urun, geciken kargo, yanlis urun
```

**Değerlendirme:** Base GPT-4o-mini vs fine-tuned modeli 20 test sorusuyla karşılaştır. Tutarlilik, domain bilgisi ve uslup farklılıklarını raporla.
:::

:::exercise
## Alıştırma 4: Evaluation Pipeline

**Görev:** Fine-tuned modelleri sistematik olarak değerlendiren bir pipeline oluştur.

**Adimlar:**
1. Classification için: accuracy, precision, recall, F1, confusion matrix
2. Generation için: BLEU, ROUGE, human evaluation rubrik
3. Training curves ciz (train vs eval loss)
4. Overfitting detection — train/eval loss farki %10'u gecerse uyar
5. Model karşılaştırma raporu oluştur (tablo formati)

**Başlangıç kodu:**
```python
class EvaluationPipeline:
    def __init__(self, model, tokenizer, test_dataset):
        self.model = model
        self.tokenizer = tokenizer
        self.test_dataset = test_dataset
        self.results = {}

    def evaluate_classification(self):
        """Accuracy, F1, confusion matrix hesapla."""
        # SENIN KODUN

    def evaluate_generation(self, test_prompts):
        """BLEU, ROUGE hesapla."""
        # SENIN KODUN

    def detect_overfitting(self, train_history):
        """Train/eval loss farkini analiz et."""
        # SENIN KODUN

    def generate_report(self):
        """Tum sonuclari tablo formatinda raporla."""
        # SENIN KODUN

# Kullanim
pipeline = EvaluationPipeline(model, tokenizer, test_dataset)
pipeline.evaluate_classification()
pipeline.generate_report()
```
:::

---

## Mulakat Sorulari

:::interview
## Mulakat: "Fine-tuning ile prompt engineering arasindaki fark nedir? Hangisini ne zaman tercih edersiniz?"

**Guclü Cevap:**

"Fine-tuning ve prompt engineering farkli trade-off'lara sahip iki yaklaşım.

**Prompt engineering**, modeli degistirmeden talimatlar ve örneklerle yonlendirmek. Avantajlari: sifir maliyet, aninda güncelleme, model agnostik. Dezavantajlari: uzun prompt'lar yüksek latency ve maliyet, tutarsiz ciktilar, context window limiti.

**Fine-tuning**, modelin weight'lerini ozel veriyle guncellemek. Avantajlari: düşük inference latency (kisa prompt yeterli), tutarli ciktilar, domain bilgisi icsellesir. Dezavantajlari: GPU maliyeti, veri hazirlama süresi, model guncellenmez (yeniden egitmek lazim).

**Karar agaci:**
- Prototip asamasi veya az veri → prompt engineering
- 50-100+ ornekle tutarli çıktı gerekli → fine-tuning
- Domain-specific dil gerekli (tip, hukuk, finans) → fine-tuning
- Sik degisen gereksinimler → prompt engineering
- Latency kritik → fine-tuning

Pratikte çoğu projede önce prompt engineering ile baslarim. Yetersiz kalirsa (tutarsiz çıktı, yüksek latency, çok uzun prompt) fine-tuning'e gecerim. Bazen ikisini birlikte kullanirim: fine-tuned model + kisa system prompt."
:::

:::interview
## Mulakat: "LoRA nasil çalışır? Neden full fine-tuning yerine tercih edilir?"

**Guclü Cevap:**

"LoRA'nin temel fikri, fine-tuning sirasindaki weight degisiminin low-rank oldugu gozlemine dayanir.

Normal fine-tuning'de W = W_0 + ΔW seklinde tüm weight matrisi guncellenir. LoRA'da ΔW = A × B olarak decompose edilir. A (d×r) ve B (r×d) boyutunda iki küçük matris. r, rank parametresi — genellikle 8, 16 veya 32. Bu sayede d×d yerine 2×d×r parametre egitilir.

Örnek: 4096×4096 matris için full fine-tuning 16.7M parametre gunceller. r=16 LoRA ile sadece 131K parametre — 128x azalma.

**Neden LoRA tercih edilir:**
1. **Bellek:** 7B model full fine-tuning için ~28GB GPU RAM, LoRA ile ~16GB, QLoRA ile ~4GB
2. **Hız:** Daha az parametre = daha hızlı egitim ve convergence
3. **Multi-task:** Ayni base model, farkli gorevler için farkli adapter'lar. Adapter degistirmek saniyeler surar.
4. **Inference:** Adapter'lar base modele merge edilir — ek latency yok
5. **Storage:** Full model ~14GB, LoRA adapter ~17MB

**Ne zaman full fine-tuning:** Çok büyük veri (100K+), ciddi domain shift, compute butcesi sinirli değil."
:::

:::interview
## Mulakat: "Fine-tuning sırasında overfitting'i nasil onlersiniz?"

**Guclü Cevap:**

"Overfitting, modelin training verisini ezberleyip yeni veriye genelleme yapamamasi. Fine-tuning'de bu risk özellikle yüksek çünkü pre-trained modeller zaten çok güçlü.

**Tespit:**
- Train loss dusuyor ama eval loss artiyor — klasik overfitting sinyali
- Train accuracy %99+ ama eval accuracy %80 — arada büyük fark

**Onleme teknikleri:**

1. **Early stopping:** Eval loss artmaya basladiginda dur. `load_best_model_at_end=True` kullan.

2. **Düşük learning rate:** Pre-trained modelde 2e-5 ile 5e-5 arası. Çok yüksek LR catastrophic forgetting'e neden olur.

3. **Weight decay:** L2 regularization. `weight_decay=0.01` standart.

4. **Dropout:** LoRA'da `lora_dropout=0.05-0.1`.

5. **Az epoch:** Fine-tuning'de 1-5 epoch genellikle yeterli. 20 epoch overfitting garantisi.

6. **Veri artirma:** Paraphrasing, back-translation, synonym replacement ile veri cesitliligini artir.

7. **Evaluation set:** Kesinlikle train/eval/test split yap. Eval set olmadan overfitting gormezden gelinir.

8. **LoRA kullan:** Full fine-tuning'den daha az parametre = daha düşük overfitting riski.

Pratikte ilk yaptigim sey: küçük veri alt kumesiyle hızlı bir egitim yapip loss curve'e bakmak. Overfitting gorursem yukardaki teknikleri sirayla uygularim."
:::

---

## Ileri Düzey Konular

:::deha-tip
## Deha Tipi: Veri Kalitesi Her Seydir

Büyük şirketlerin fine-tuning basarisinin sirri model değil, **veri kalitesi.**

```
Veri Kalitesi Kontrol Listesi:
□ Duplicate ornekler temizlendi mi?
□ Yanlis etiketler duzeltildi mi?
□ Veri dengeli mi (class imbalance)?
□ Edge case'ler dahil mi?
□ Veri contamination yok mu (test verisi train'de)?
□ Veri format tutarli mi?
□ PII (kisisel bilgi) temizlendi mi?
```

**Pratik kural:** Fine-tuning butcenin %60'ini veri hazırlama, %20'sini egitim, %20'sini evaluation'a harca. Çoğu mühendis bu orani tersine çevirir — ve başarısız olur.

1000 örnek toplamaktansa, 200 mükemmel örnek hazırla. Her örneği şu sorularla değerlendir:
- Bu örnekten model ne ogreniyor?
- Genel bir pattern mi yoksa edge case mi?
- Tutarli mi (benzer inputlara benzer outputlar)?
:::

:::code
## Hyperparameter Tuning Template

```python
"""
Fine-tuning Hyperparameter Rehberi

Baslangic noktasi (BERT/DistilBERT classification):
─────────────────────────────────────────────────────
learning_rate: 2e-5
batch_size: 16-32
epochs: 3-5
warmup_ratio: 0.06
weight_decay: 0.01

Baslangic noktasi (LoRA LLM):
─────────────────────────────────────────────────────
learning_rate: 2e-4
batch_size: 4-8 (+ gradient accumulation)
epochs: 1-3
warmup_ratio: 0.03
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
target_modules: ["q_proj", "v_proj"]

Baslangic noktasi (QLoRA LLM):
─────────────────────────────────────────────────────
learning_rate: 2e-4
batch_size: 4 (+ gradient accumulation 4)
epochs: 1
warmup_ratio: 0.03
lora_r: 64
lora_alpha: 16
lora_dropout: 0.1
target_modules: all linear layers
optim: "paged_adamw_8bit"
gradient_checkpointing: True
"""

# Optuna ile otomatik hyperparameter arama
# uv pip install optuna
import optuna

def objective(trial):
    lr = trial.suggest_float("learning_rate", 1e-5, 5e-4, log=True)
    batch_size = trial.suggest_categorical("batch_size", [4, 8, 16, 32])
    epochs = trial.suggest_int("epochs", 1, 5)
    warmup = trial.suggest_float("warmup_ratio", 0.0, 0.1)
    wd = trial.suggest_float("weight_decay", 0.0, 0.1)

    training_args = TrainingArguments(
        output_dir=f"./trial-{trial.number}",
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        learning_rate=lr,
        warmup_ratio=warmup,
        weight_decay=wd,
        eval_strategy="epoch",
        save_strategy="no",
        fp16=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=eval_data,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    eval_result = trainer.evaluate()
    return eval_result["eval_f1"]

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=20)

print(f"En iyi F1: {study.best_value:.4f}")
print(f"En iyi parametreler: {study.best_params}")
```
:::

---

## Özet

Bu derste fine-tuning'in temellerinden production deployment'a kadar tüm sureci kapsadik:

```
Fine-tuning Yol Haritasi:
┌──────────────────────────────────────────────────────────────┐
│ 1. Karar Ver                                                 │
│    Prompt engineering yeterli mi? → Evet → Fine-tuning YAPMA │
│    Hayir ↓                                                   │
│                                                              │
│ 2. Veri Hazirla                                              │
│    Kaliteli veri topla → temizle → formatla → split et       │
│                                                              │
│ 3. Strateji Sec                                              │
│    Az veri → Feature Extraction                               │
│    Orta veri + kucuk model → Full Fine-tuning                │
│    Orta veri + buyuk model → LoRA / QLoRA                    │
│    API kullaniyorsan → OpenAI Fine-tuning                    │
│                                                              │
│ 4. Egit                                                      │
│    Kucuk subset ile hizli deney → loss curve kontrol →       │
│    Hyperparameter tune → full egitim                         │
│                                                              │
│ 5. Degerlendir                                               │
│    Metrikler (F1, BLEU, ROUGE) → A/B test →                 │
│    Human evaluation → overfitting kontrolu                   │
│                                                              │
│ 6. Deploy Et                                                 │
│    Export (safetensors/ONNX) → Optimize (vLLM/TRT) →        │
│    Monitor → iterate                                        │
└──────────────────────────────────────────────────────────────┘
```

**Hatirla:** Fine-tuning bir sanat, bilim kadar. Veri kalitesine odaklan, küçük başla, olc ve iterate et. En iyi model, en büyük model değil — en iyi veriye sahip olandir.
