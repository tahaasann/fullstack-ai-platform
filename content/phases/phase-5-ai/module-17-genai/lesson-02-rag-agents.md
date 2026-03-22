---
title: "RAG, AI Agents ve LangChain"
id: mod-17-genai/lesson-02
estimated_minutes: 100
order: 2
tags: [rag, vector-database, embeddings, langchain, ai-agents, pinecone, chroma, faiss, retrieval]
prerequisites: [mod-17-genai/lesson-01]
---

# RAG, AI Agents ve LangChain

LLM'ler güçlü ama sınırlı: **training data'sının dışındaki bilgiyi bilemezler** ve **hallucination** yaparlar. **RAG (Retrieval-Augmented Generation)** bu problemi çözer — LLM'e kendi veri kaynaklarını vererek doğru, güncel ve kaynaklı cevaplar üretmesini sağlarsın. Bu ders, RAG pipeline'ından AI agent'lara kadar modern AI uygulama geliştirmenin temellerini öğretecek.

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "RAG (Retrieval Augmented Generation) pipeline'ini adim adim acikla: dokuman chunking stratejileri, embedding modeli secimi, vector database'e indexleme, semantic search ile retrieval, context window'a yerlestirme ve LLM ile generation. Naive RAG vs Advanced RAG (re-ranking, hybrid search, query expansion) arasindaki farklari goster."

**2. Pratik Uygulama:**
> "LangChain ile bir RAG uygulamasi olustur: PDF dokumanlarini yukle, RecursiveCharacterTextSplitter ile chunk'la, OpenAI embeddings ile vektorlestir, ChromaDB'ye kaydet ve RetrievalQA chain ile soru-cevap sistemi kur. Retrieval kalitesini olcmek icin basit bir evaluation pipeline ekle."
> Takip: "Simdi bu RAG sistemine bir AI Agent ekle: LLM'in araclar (web search, calculator, database query) kullanarak karmasik gorevleri cozebilen bir agent tasarla. ReAct (Reasoning + Acting) pattern'ini uygula."

**3. Mukemmellik Icin:**
> "Production'da bir RAG sistemi deploy ediyorum. Chunking stratejisi optimizasyonu (overlap, semantic chunking), embedding model fine-tuning, hybrid search (dense + sparse retrieval), re-ranking (cross-encoder), evaluation metrikleri (faithfulness, relevancy, answer correctness) ve cost-performance dengesini nasil kurmam gerektigini detayli anlat."

### Pair Programming Ipucu
RAG sistemi gelistirirken AI'a retrieval sonuclarini goster ve sor: "Bu sorgu icin gelen chunk'lar alakali mi? Retrieval kalitesi dusukse chunking stratejimi mi, embedding modelimi mi yoksa search parametrelerimi mi degistirmeliyim? Precision@K ve recall metriklerini hesapla."
:::

:::must-note
## Defterine Yaz!

1. **RAG = Retrieve + Generate.** Önce ilgili dokümanları bul (retrieve), sonra LLM'e bu dokümanlarla birlikte soruyu sor (generate). Bu pattern hallucination'ı dramatik şekilde azaltır.
2. **Embedding = text'in anlamını sayısal vektöre dönüştürmek.** "Kedi" ve "kedicik" birbirine yakın vektörler üretir. Semantic search'ün temeli budur.
3. **Chunking strategy her şeyi değiştirir.** Dokümanları nasıl parçaladığın, RAG kaliteni doğrudan etkiler. Çok küçük chunk = bağlam kaybolur, çok büyük chunk = noise artar.
4. **AI Agent = LLM + Tools + Reasoning Loop.** Agent, plan yapar, araç kullanır, sonucu değerlendirir ve gerekirse tekrarlar — insan gibi problem çözer.
5. **LangChain = AI application framework.** Chain'ler, agent'lar, memory ve tool entegrasyonu için standart arayüz sağlar.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir

Senior developer RAG öğrenirken:

1. **Architecture first**: Hangi vector DB? Embedding model ne? Chunking strategy ne? — Production kararlarını önceden alır
2. **Evaluation-driven**: RAGAS veya benzeri metric'lerle kaliteyi ölçer, "işe yarıyor gibi" demez
3. **Hybrid search**: Sadece semantic değil, keyword search (BM25) + semantic search birleştirerek daha iyi sonuç alır
4. **Security**: Kullanıcının görmemesi gereken dokümanlar retrieval'da nasıl filtrelenir?

**Karar Verme Sureci — Vector DB Secimi:**
- **Pinecone**: Fully managed, olceklenmesi kolay, metadata filtering. Trade-off: Pahali (yuksek hacimde), vendor lock-in, self-hosted opsiyon yok. Kullanim: Hizli baslangic, AWS/GCP entegrasyonu, kucuk-orta olcek.
- **Weaviate**: Open-source, hybrid search (BM25 + vector) built-in, multi-modal. Trade-off: Self-hosted ise ops yuku var, cloud versiyonu Pinecone kadar pahali olabilir. Kullanim: Hybrid search gereken durumlar, multi-modal arama.
- **Qdrant**: Open-source, Rust-based (cok hizli), filtreleme performansi cok iyi. Trade-off: Community Pinecone'dan kucuk, ecosystem daha az olgun. Kullanim: Yuksek performans gereken durumlar, self-hosted tercih.
- **pgvector (PostgreSQL extension)**: Mevcut PostgreSQL'e extension ekle, ayri DB yonetme. Trade-off: 10M+ vector'de dedicated vector DB'lerden yavas, ANN algoritmasi sinirli. Kullanim: Kucuk-orta olcek (<1M vector), zaten PostgreSQL kullaniyorsan, basitlik oncelikliyse.
- **Senior karar agaci**: "1M'den az vector, zaten PostgreSQL var? pgvector. Hybrid search lazim? Weaviate. Managed istiyorum, butce var? Pinecone. Self-hosted, yuksek performans? Qdrant."

**Karar Verme Sureci — Chunking Stratejisi:**
- **Fixed-size chunks (500-1000 token)**: Basit, tahmin edilebilir. Trade-off: Cumle ortasindan keser, anlam kaybi olur.
- **Semantic chunking**: Anlam sinirlarina gore bolme. Trade-off: Daha yavas, implementasyonu karmasik ama retrieval kalitesi cok daha iyi.
- **Recursive character splitting**: LangChain default, paragraf > cumle > kelime sirasinda boler. Trade-off: "Yeterince iyi" cogu durum icin ama domain-specific icerik icin ozel strateji gerekebilir.
- **Senior karar agaci**: "Genel dokuman? Recursive splitting + overlap (200 token). Teknik dokumantasyon? Heading-based splitting. Kod? AST-based splitting."

**Anti-pattern Farkindaligi:**
- **"Chunk and pray" yaklasimi**: Dokumanları rastgele bolerek vector DB'ye atip "is gorecektir" demek. Evaluation olmadan production'a cikmak. RAGAS metrikleri (faithfulness, answer relevancy, context recall) ile sistematik olcum sart.
- **Embedding model secimini gozardi etmek**: Default OpenAI text-embedding-3-small her dilde iyi calismiyor. Turkce icerik icin multilingual model sec (multilingual-e5-large gibi). Yanlis embedding = yanlis retrieval = yanlis cevap.
- **Tek buyuk prompt'a her seyi tikmak**: 50 sayfalik dokumani prompt'a koyup "ozetle" demek. Context window yetse bile "lost in the middle" problemi var. RAG ile sadece ilgili chunk'lari getir.

**Gercek Dunya Deneyimi:** Bir hukuk firmasinin 50K+ sozlesme arsivinde arama sistemi kurduk. Ilk versiyonda fixed-size chunking + OpenAI embedding kullandik. Avukatlar "yanlis maddeleri getiriyor" dedi. Analiz: chunk'lar madde ortasindan bolunuyordu. Heading-based chunking + multilingual-e5-large embedding + hybrid search (BM25 + semantic) gecisinden sonra retrieval accuracy %62'den %91'e cikti. Ders: chunking stratejisi, model seciminden bile daha kritik olabilir.
:::

---

## 1. RAG Temelleri — Retrieval-Augmented Generation

### 1.1 RAG Nedir ve Neden Gerekli?

:::concept
## RAG (Retrieval-Augmented Generation)

LLM'lerin iki temel sorunu var:
1. **Knowledge cutoff**: Training verisi belirli bir tarihe kadar — güncel bilgi yok
2. **Hallucination**: Bilmediği konularda "uydurma" cevap verebilir

RAG bu iki sorunu çözer:

```
Kullanıcı Sorusu
       ↓
   [RETRIEVE] → Vector DB'den ilgili dokümanları getir
       ↓
   [AUGMENT]  → Dokümanları prompt'a ekle
       ↓
   [GENERATE] → LLM, dokümanları kullanarak cevap üretir
       ↓
   Kaynaklı Cevap
```

**Neden fine-tuning yerine RAG?**
- Fine-tuning: Pahalı, yavaş, verinin güncellenmesi zor
- RAG: Ucuz, hızlı kurulur, veri güncellemesi kolay, kaynak gösterebilir
:::

### 1.2 RAG Pipeline Architecture

:::concept
## RAG Pipeline — 2 Aşama

### Aşama 1: Indexing (Offline — Bir kere yapılır)
```
Dokümanlar → Load → Chunk → Embed → Store (Vector DB)
```

### Aşama 2: Querying (Online — Her soru için)
```
Soru → Embed → Search (Vector DB) → Top-K Results → LLM + Context → Cevap
```

Her aşamanın kendi best practice'leri ve tradeoff'ları var.
:::

---

## 2. Embeddings — Anlamı Vektöre Dönüştürmek

### 2.1 Embedding Nedir?

:::concept
## Embeddings

**Embedding**, bir text parçasını sabit boyutlu bir sayısal vektöre (float dizisi) dönüştüren işlemdir. Bu vektörler, text'in **anlamsal (semantic) temsilini** yakalar.

```
"kedi"     → [0.12, -0.45, 0.78, ..., 0.33]  (1536 boyut)
"kedicik"  → [0.11, -0.44, 0.79, ..., 0.34]  (çok yakın!)
"araba"    → [0.89, 0.23, -0.56, ..., -0.11]  (çok farklı!)
```

**Cosine similarity** ile iki vektör arasındaki benzerliği ölçeriz:
- 1.0 = identik anlam
- 0.0 = ilgisiz
- -1.0 = zıt anlam (pratikte nadir)
:::

:::code
## Embedding Oluşturma ve Karşılaştırma

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Text'i embedding vektörüne dönüştür"""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """İki vektör arasındaki cosine similarity"""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Test
emb_kedi = get_embedding("kedi")
emb_kedicik = get_embedding("kedicik")
emb_araba = get_embedding("araba")
emb_python = get_embedding("Python programlama dili")
emb_js = get_embedding("JavaScript programlama dili")

print(f"kedi ↔ kedicik:  {cosine_similarity(emb_kedi, emb_kedicik):.4f}")  # ~0.90
print(f"kedi ↔ araba:    {cosine_similarity(emb_kedi, emb_araba):.4f}")    # ~0.20
print(f"Python ↔ JS:     {cosine_similarity(emb_python, emb_js):.4f}")     # ~0.85
print(f"Python ↔ kedi:   {cosine_similarity(emb_python, emb_kedi):.4f}")   # ~0.15

print(f"\nEmbedding boyutu: {len(emb_kedi)}")  # 1536
```
:::

:::comparison
## Embedding Modelleri Karşılaştırması

| Model | Provider | Boyut | Fiyat (per 1M tokens) | Kullanım |
|-------|----------|-------|----------------------|----------|
| text-embedding-3-small | OpenAI | 1536 | $0.02 | Genel amaçlı, ucuz |
| text-embedding-3-large | OpenAI | 3072 | $0.13 | Yüksek kalite |
| voyage-3 | Voyage AI | 1024 | $0.06 | Code retrieval'da iyi |
| BAAI/bge-large-en | Open Source | 1024 | Ücretsiz | Self-host |
| nomic-embed-text | Nomic AI | 768 | Ücretsiz | Lokal çalışır |
:::

---

## 3. Chunking Strategies — Dokümanları Parçalamak

### 3.1 Neden Chunking?

:::concept
## Chunking

Dokümanlar genellikle binlerce kelimedir ama LLM context window'u sınırlı ve büyük text'te relevance düşer. **Chunking**, dokümanları anlamlı parçalara bölme işlemidir.

**Chunking'in altın kuralı**: Her chunk, tek başına anlamlı ve kendine yeterli olmalı.

Temel stratejiler:
1. **Fixed-size chunking**: Sabit karakter/token sayısında böl
2. **Recursive chunking**: Heading, paragraph, sentence sırasıyla böl
3. **Semantic chunking**: Anlam değişikliklerine göre böl
4. **Document-aware chunking**: Doküman yapısına göre böl (Markdown headers, HTML sections)
:::

:::code
## Chunking Stratejileri — Implementasyon

```python
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    MarkdownTextSplitter,
    TokenTextSplitter
)

sample_doc = """
# Python Veri Tipleri

## Sayısal Tipler

Python'da üç temel sayısal tip vardır: int, float ve complex.
Int tipi tam sayıları temsil eder ve boyut sınırı yoktur.
Float tipi ondalıklı sayıları temsil eder.

## String Tipi

String'ler immutable karakter dizileridir.
Tek tırnak, çift tırnak veya üçlü tırnak ile oluşturulabilir.
String interpolation için f-string kullanımı önerilir.

## Liste ve Tuple

Listeler mutable, tuple'lar immutable koleksiyonlardır.
Listeler köşeli parantez, tuple'lar normal parantez ile oluşturulur.
Her ikisi de sıralı (ordered) yapılardır.
"""

# 1. Fixed-size chunking
fixed_splitter = CharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separator="\n"
)
chunks_fixed = fixed_splitter.split_text(sample_doc)
print(f"Fixed-size: {len(chunks_fixed)} chunks")

# 2. Recursive chunking (EN ÇOK ÖNERİLEN)
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30,
    separators=["\n## ", "\n\n", "\n", ". ", " ", ""]  # Hiyerarşik separator'lar
)
chunks_recursive = recursive_splitter.split_text(sample_doc)
print(f"Recursive: {len(chunks_recursive)} chunks")

# 3. Markdown-aware chunking
md_splitter = MarkdownTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)
chunks_md = md_splitter.split_text(sample_doc)
print(f"Markdown: {len(chunks_md)} chunks")

# 4. Token-based chunking (LLM context window'una uygun)
token_splitter = TokenTextSplitter(
    chunk_size=100,  # 100 token
    chunk_overlap=10
)
chunks_token = token_splitter.split_text(sample_doc)
print(f"Token: {len(chunks_token)} chunks")

# Her birini görelim
for i, chunk in enumerate(chunks_recursive):
    print(f"\n--- Chunk {i} ({len(chunk)} chars) ---")
    print(chunk[:100] + "..." if len(chunk) > 100 else chunk)
```
:::

:::tip
## Chunking Best Practices

| Parameter | Recommended Range | Neden |
|-----------|------------------|-------|
| **chunk_size** | 256-1024 tokens | Çok küçük = bağlam kaybolur, çok büyük = noise artar |
| **chunk_overlap** | chunk_size'ın %10-15'i | Chunk sınırlarındaki bilgi kaybını engeller |
| **Separator** | Document-type'a göre | Markdown → headers, Code → functions, Text → paragraphs |

**Pro tip**: Chunk'lara **metadata** ekle (source file, page number, section title). Retrieval sonrası referans gösterme için kritik!
:::

:::beginner-mistake
## Chunking'de Yapılan Hatalar

**Hata 1: Sabit boyut kullanıp bağlamı koparmak**
"Python'da üç temel sayısal tip vardır:" bir chunk'ta, ": int, float ve complex" diğerinde — anlam kaybolur!

**Hata 2: Overlap kullanmamak**
Chunk sınırlarındaki cümleler ikiye bölünür. %10-15 overlap bu sorunu çözer.

**Hata 3: Tüm doküman tipleri için aynı stratejiyi kullanmak**
Markdown, PDF, kod, tablo — her biri farklı chunking stratejisi gerektirir.

**Hata 4: Chunk'lara metadata eklememek**
"Hangi dokümanın hangi bölümünden geldi?" bilgisi olmadan RAG kalitesi düşer.
:::

---

## 4. Vector Databases — Vektörleri Depolamak ve Aramak

### 4.1 Vector Database Nedir?

:::concept
## Vector Database

**Vector database**, yüksek boyutlu vektörleri depolayan ve **similarity search** (benzerlik araması) yapabilen özelleştirilmiş veritabanıdır.

Normal SQL: `SELECT * FROM products WHERE name = 'laptop'` (exact match)
Vector DB: `SELECT * FROM embeddings ORDER BY similarity(query_vector, doc_vector) LIMIT 5` (semantic match)

**Temel operasyonlar:**
1. **Insert/Upsert**: Vektörleri metadata ile birlikte depola
2. **Search**: En benzer K vektörü bul (KNN / ANN)
3. **Filter**: Metadata'ya göre filtrele + similarity search
4. **Delete**: Vektörleri sil
:::

:::comparison
## Vector Database Karşılaştırması

| DB | Tip | Hosting | Ücretsiz Tier | Best For |
|----|-----|---------|--------------|----------|
| **Chroma** | Open source | Self-host / Cloud | Evet | Prototip, küçük projeler |
| **FAISS** | Library | In-memory | Evet (tamamen) | Research, single-machine |
| **Pinecone** | Managed | Cloud | 1 index free | Production, managed |
| **Weaviate** | Open source | Self-host / Cloud | Evet | GraphQL lovers |
| **Qdrant** | Open source | Self-host / Cloud | Evet | High performance |
| **pgvector** | Extension | PostgreSQL | Evet | Zaten Postgres kullanıyorsan |
:::

### 4.2 Chroma — Local Development

:::code
## Chroma ile RAG Pipeline

```python
import chromadb
from openai import OpenAI

openai_client = OpenAI()

# 1. Chroma client oluştur
chroma_client = chromadb.Client()  # In-memory
# chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Persistent

# 2. Collection oluştur
collection = chroma_client.create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}  # Cosine similarity kullan
)

# 3. Dokümanları ekle
documents = [
    "Python dynamically typed bir programlama dilidir. Guido van Rossum tarafından geliştirilmiştir.",
    "JavaScript web tarayıcılarında çalışan bir programlama dilidir. Brendan Eich tarafından yaratılmıştır.",
    "Docker containerization platformudur. Uygulamaları izole ortamlarda çalıştırır.",
    "Kubernetes container orchestration aracıdır. Docker container'larını yönetir.",
    "PostgreSQL açık kaynak ilişkisel veritabanıdır. ACID compliance sağlar.",
    "MongoDB NoSQL document veritabanıdır. JSON benzeri dokümanlar depolar.",
    "Redis in-memory key-value store'dur. Caching için yaygın kullanılır.",
    "Git distributed version control sistemidir. Linus Torvalds tarafından geliştirilmiştir."
]

metadatas = [
    {"category": "language", "difficulty": "beginner"},
    {"category": "language", "difficulty": "beginner"},
    {"category": "devops", "difficulty": "intermediate"},
    {"category": "devops", "difficulty": "advanced"},
    {"category": "database", "difficulty": "intermediate"},
    {"category": "database", "difficulty": "intermediate"},
    {"category": "database", "difficulty": "intermediate"},
    {"category": "tools", "difficulty": "beginner"},
]

# Chroma kendi embedding'ini oluşturabilir (default: all-MiniLM-L6-v2)
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=[f"doc_{i}" for i in range(len(documents))]
)

print(f"Collection'da {collection.count()} doküman var")

# 4. Semantic Search
results = collection.query(
    query_texts=["container teknolojileri nelerdir?"],
    n_results=3
)

print("\n=== Search Results ===")
for doc, meta, distance in zip(
    results['documents'][0],
    results['metadatas'][0],
    results['distances'][0]
):
    print(f"  [{1-distance:.3f}] ({meta['category']}) {doc[:80]}...")

# 5. Metadata filtrelemesi ile search
results_filtered = collection.query(
    query_texts=["en popüler veritabanı hangisi?"],
    n_results=3,
    where={"category": "database"}  # Sadece database kategorisinde ara
)

# 6. RAG — Search sonuçlarını LLM'e gönder
def rag_query(question: str, n_results: int = 3) -> str:
    # Retrieve
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    # Context oluştur
    context = "\n\n".join([
        f"[Kaynak {i+1}]: {doc}"
        for i, doc in enumerate(results['documents'][0])
    ])

    # Generate
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Sen yardımcı bir asistansın. Soruları SADECE verilen kaynaklardan cevapla.
Eğer kaynaklar yeterli bilgi içermiyorsa, "Bu konuda yeterli bilgim yok" de.
Her cevabın sonunda kullandığın kaynak numaralarını belirt."""
            },
            {
                "role": "user",
                "content": f"Kaynaklar:\n{context}\n\nSoru: {question}"
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content

# Test
print("\n=== RAG Query ===")
print(rag_query("Docker ve Kubernetes arasındaki fark nedir?"))
print("\n" + rag_query("React nedir?"))  # Kaynakta yok — "bilgim yok" demeli
```
:::

### 4.3 FAISS — High-Performance Search

:::code
## FAISS ile Hızlı Similarity Search

```python
import faiss
import numpy as np
from openai import OpenAI

client = OpenAI()

class FAISSIndex:
    """FAISS-based vector search"""

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        # L2 distance index (cosine similarity için normalize et)
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product = cosine (normalized)
        self.documents = []
        self.metadatas = []

    def add_documents(self, texts: list[str], metadatas: list[dict] = None):
        """Dokümanları embed et ve index'e ekle"""
        # Batch embedding
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )

        embeddings = np.array([e.embedding for e in response.data], dtype=np.float32)

        # Normalize (cosine similarity için gerekli)
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.documents.extend(texts)
        self.metadatas.extend(metadatas or [{}] * len(texts))

    def search(self, query: str, k: int = 5) -> list[dict]:
        """Semantic search"""
        # Query'yi embed et
        response = client.embeddings.create(
            input=[query],
            model="text-embedding-3-small"
        )
        query_vec = np.array([response.data[0].embedding], dtype=np.float32)
        faiss.normalize_L2(query_vec)

        # Search
        scores, indices = self.index.search(query_vec, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:  # -1 = not found
                results.append({
                    "document": self.documents[idx],
                    "metadata": self.metadatas[idx],
                    "score": float(score)
                })

        return results

    def save(self, path: str):
        faiss.write_index(self.index, path)

    def load(self, path: str):
        self.index = faiss.read_index(path)

# Kullanım
index = FAISSIndex()
index.add_documents(
    texts=[
        "Python is a high-level programming language",
        "FastAPI is a modern Python web framework",
        "Docker containers isolate applications",
        "Kubernetes orchestrates Docker containers",
    ],
    metadatas=[
        {"topic": "python"}, {"topic": "python"},
        {"topic": "devops"}, {"topic": "devops"}
    ]
)

results = index.search("web development with Python", k=2)
for r in results:
    print(f"[{r['score']:.3f}] {r['document']}")
```
:::

---

## 5. LangChain Framework

### 5.1 LangChain Nedir?

:::concept
## LangChain

**LangChain**, LLM-powered uygulamalar geliştirmek için bir framework'tür. Temel bileşenleri:

1. **Models**: LLM ve Embedding model abstraction'ları
2. **Prompts**: Prompt template'leri ve management
3. **Chains**: Birden fazla adımı sıralı çalıştırma
4. **Agents**: LLM'in araç kullanarak karar vermesi
5. **Memory**: Konuşma geçmişi yönetimi
6. **Retrievers**: RAG için document retrieval
7. **Tools**: Harici araç entegrasyonları

LangChain, bu bileşenleri **composable** (birleştirilebilir) hale getirir.
:::

### 5.2 LangChain Chains

:::code
## LangChain ile RAG Pipeline

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Components
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 2. Dokümanları hazırla
documents = [
    "FastAPI, Python için modern ve hızlı bir web framework'üdür. Otomatik API documentation sağlar.",
    "Django, Python'ın en popüler full-stack web framework'üdür. ORM, admin panel ve authentication içerir.",
    "Flask, Python için minimal bir web framework'üdür. Microservices için idealdir.",
    "Express.js, Node.js için minimal web framework'üdür. Middleware tabanlı mimari kullanır.",
    "Next.js, React tabanlı full-stack framework'üdür. SSR ve SSG desteği sağlar.",
    "NestJS, Node.js için enterprise-grade framework'üdür. TypeScript ile yazılmıştır.",
]

# 3. Chunk (bu örnekte dokümanlar zaten kısa, gerçekte chunking gerekir)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# 4. Vector Store oluştur
vectorstore = Chroma.from_texts(
    texts=documents,
    embedding=embeddings,
    collection_name="frameworks"
)

# 5. Retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 6. RAG Prompt
rag_prompt = ChatPromptTemplate.from_template("""
Aşağıdaki bağlam bilgilerini kullanarak soruyu cevapla.
Eğer bağlamda yeterli bilgi yoksa, "Bu konuda bilgim yok" de.

Bağlam:
{context}

Soru: {question}

Cevap:""")

# 7. RAG Chain (LCEL - LangChain Expression Language)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 8. Kullan!
answer = rag_chain.invoke("Python'da API geliştirmek için en iyi framework hangisi?")
print(answer)

answer2 = rag_chain.invoke("TypeScript ile backend geliştirmek için ne kullanmalıyım?")
print(answer2)
```
:::

### 5.3 LangChain Memory

:::code
## Conversation Memory

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Prompt with message history
prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen yardımcı bir Python tutoring asistanısın. Öğrenciye sabırla öğret."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

# Session-based memory store
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Memory ile chain
with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Konuşma
config = {"configurable": {"session_id": "student_001"}}

r1 = with_memory.invoke({"input": "Python'da decorator ne demek?"}, config=config)
print(f"AI: {r1.content}\n")

r2 = with_memory.invoke({"input": "Bir örnek gösterir misin?"}, config=config)
print(f"AI: {r2.content}\n")

r3 = with_memory.invoke({"input": "Bunu class-based yapabilir miyiz?"}, config=config)
print(f"AI: {r3.content}\n")

# Memory'de ne var?
history = get_session_history("student_001")
print(f"\nToplam {len(history.messages)} mesaj hafızada")
```
:::

---

## 6. AI Agents — LLM + Tools + Reasoning

### 6.1 AI Agent Nedir?

:::concept
## AI Agent

**AI Agent**, bir LLM'in araçlar kullanarak **otonom şekilde** problem çözmesidir. Normal LLM çağrısından farkı:

| Normal LLM Call | AI Agent |
|----------------|----------|
| Tek soru → tek cevap | Soruyu analiz → plan yap → araç kullan → değerlendir → tekrarla |
| Stateless | Stateful (önceki adımları hatırlar) |
| Sadece text üretir | Text + action üretir |
| İnsan yönlendirir | Kendi kendine karar verir |

**Agent Loop:**
```
1. THINK: Problemi analiz et, plan yap
2. ACT: Uygun aracı seç ve kullan
3. OBSERVE: Sonucu gözlemle
4. REPEAT: Gerekirse 1'e dön
5. RESPOND: Final cevabı ver
```
:::

### 6.2 LangChain ile Agent Oluşturma

:::code
## Tool-Using Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from datetime import datetime
import requests

# 1. Tool'ları tanımla
@tool
def get_current_time() -> str:
    """Şu anki tarih ve saati döndürür"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculate(expression: str) -> str:
    """Matematik ifadesini hesaplar. Örnek: '2 + 3 * 4'"""
    try:
        # Güvenli eval (sadece math operasyonları)
        allowed_names = {"__builtins__": {}}
        result = eval(expression, allowed_names)
        return str(result)
    except Exception as e:
        return f"Hesaplama hatası: {e}"

@tool
def search_knowledge_base(query: str) -> str:
    """Bilgi bankasında arama yapar. Teknik sorular için kullan."""
    # Gerçek uygulamada RAG pipeline burada olur
    knowledge = {
        "python": "Python dynamically typed, interpreted bir programlama dilidir.",
        "docker": "Docker, uygulamaları containerlar içinde çalıştıran bir platformdur.",
        "kubernetes": "Kubernetes, container orchestration aracıdır.",
    }

    query_lower = query.lower()
    results = []
    for key, value in knowledge.items():
        if key in query_lower:
            results.append(value)

    return "\n".join(results) if results else "Bilgi bulunamadı."

# 2. Agent'ı oluştur
tools = [get_current_time, calculate, search_knowledge_base]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Sen yardımcı bir AI asistansın. Soruları cevaplamak için
araçlarını kullanabilirsin. Emin olmadığın konularda bilgi bankasında ara.
Matematik soruları için calculate aracını kullan."""),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,     # Düşünme sürecini göster
    max_iterations=5  # Sonsuz döngüyü engelle
)

# 3. Test
result = agent_executor.invoke({"input": "Şu an saat kaç?"})
print(f"\nCevap: {result['output']}\n")

result = agent_executor.invoke({"input": "125 * 48 + 73 kaç eder?"})
print(f"\nCevap: {result['output']}\n")

result = agent_executor.invoke({"input": "Docker nedir ve Kubernetes'ten farkı ne?"})
print(f"\nCevap: {result['output']}\n")
```
:::

### 6.3 Multi-Agent Systems

:::concept
## Multi-Agent Architecture

**Multi-agent system**, birden fazla specialized agent'ın birlikte çalışmasıdır.

```
User Query
    ↓
[Router Agent] → Hangi agent'a yönlendirilecek?
    ↓
┌─────────────────────────────────┐
│ [Research Agent]  → Web search  │
│ [Code Agent]      → Code gen   │
│ [Analysis Agent]  → Data anal. │
│ [Writing Agent]   → Content    │
└─────────────────────────────────┘
    ↓
[Orchestrator] → Sonuçları birleştir
    ↓
Final Response
```

Her agent kendi:
- **System prompt'una** sahip (uzmanlık alanı)
- **Tool set'ine** sahip (kullanabileceği araçlar)
- **Memory'sine** sahip (kendi context'i)
:::

:::code
## Basit Multi-Agent System

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Specialized Agent'lar (basit chain olarak)
code_agent = (
    ChatPromptTemplate.from_messages([
        ("system", "Sen uzman bir Python developer'sın. Sadece kod yaz, açıklama yapma."),
        ("human", "{input}")
    ])
    | llm | StrOutputParser()
)

review_agent = (
    ChatPromptTemplate.from_messages([
        ("system", """Sen bir senior code reviewer'sın. Verilen kodu analiz et ve şu açılardan değerlendir:
1. Correctness (Doğruluk)
2. Performance (Performans)
3. Security (Güvenlik)
4. Best Practices
Her madde için puan ver (1-10) ve iyileştirme önerileri sun."""),
        ("human", "Bu kodu review et:\n\n{code}")
    ])
    | llm | StrOutputParser()
)

refactor_agent = (
    ChatPromptTemplate.from_messages([
        ("system", "Sen bir refactoring uzmanısın. Review feedback'ine göre kodu iyileştir."),
        ("human", "Orijinal kod:\n{code}\n\nReview feedback:\n{review}\n\nKodu iyileştir:")
    ])
    | llm | StrOutputParser()
)

# Multi-agent pipeline
def multi_agent_code_pipeline(task: str) -> dict:
    """Code → Review → Refactor pipeline"""
    print("🔧 Code Agent çalışıyor...")
    code = code_agent.invoke({"input": task})
    print(f"Kod üretildi.\n")

    print("🔍 Review Agent çalışıyor...")
    review = review_agent.invoke({"code": code})
    print(f"Review tamamlandı.\n")

    print("♻️ Refactor Agent çalışıyor...")
    improved_code = refactor_agent.invoke({"code": code, "review": review})
    print(f"Refactoring tamamlandı.\n")

    return {
        "original_code": code,
        "review": review,
        "improved_code": improved_code
    }

# Test
result = multi_agent_code_pipeline(
    "Python'da thread-safe bir singleton pattern implement et"
)
print("=== Final Code ===")
print(result["improved_code"])
```
:::

---

## 7. Advanced RAG Techniques

### 7.1 Hybrid Search

:::code
## Hybrid Search — BM25 + Semantic

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# Dokümanlar
docs = [
    Document(page_content="FastAPI uses async/await for high performance web APIs",
             metadata={"source": "fastapi_docs"}),
    Document(page_content="Django REST Framework provides serializers for API development",
             metadata={"source": "django_docs"}),
    Document(page_content="Flask is a lightweight WSGI web application framework",
             metadata={"source": "flask_docs"}),
    Document(page_content="Express.js is a minimal Node.js web framework",
             metadata={"source": "express_docs"}),
    Document(page_content="NestJS provides a modular architecture with decorators",
             metadata={"source": "nestjs_docs"}),
]

# BM25 Retriever (keyword-based)
bm25_retriever = BM25Retriever.from_documents(docs, k=3)

# Semantic Retriever (embedding-based)
vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Hybrid = BM25 + Semantic (weighted)
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.4, 0.6]  # Semantic'e daha fazla ağırlık
)

# Test
results = hybrid_retriever.invoke("async API development")
for doc in results:
    print(f"  [{doc.metadata['source']}] {doc.page_content[:60]}...")
```
:::

### 7.2 Query Transformation

:::code
## Query Transformation Techniques

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 1. Query Rewriting — Soruyu daha iyi hale getir
rewrite_prompt = ChatPromptTemplate.from_template("""
Kullanıcının sorusunu, bir bilgi bankasında arama yapmak için daha uygun hale getir.
Orijinal anlamı koru ama daha açıklayıcı ve aranabilir yap.

Orijinal soru: {question}
Yeniden yazılmış soru:""")

rewriter = rewrite_prompt | llm | StrOutputParser()

original = "python hızlı api"
rewritten = rewriter.invoke({"question": original})
print(f"Original: {original}")
print(f"Rewritten: {rewritten}")

# 2. Multi-Query — Tek sorudan birden fazla arama sorgusu üret
multi_query_prompt = ChatPromptTemplate.from_template("""
Verilen soruyu farklı açılardan ele alan 3 arama sorgusu oluştur.
Her sorguyu yeni satıra yaz.

Soru: {question}
Sorgular:""")

multi_query = multi_query_prompt | llm | StrOutputParser()

queries = multi_query.invoke({"question": "Python'da web geliştirme nasıl yapılır?"})
print(f"\nMulti-queries:\n{queries}")

# 3. HyDE — Hypothetical Document Embeddings
# Soruya cevap veren varsayımsal bir doküman üret, sonra O dokümanın embedding'i ile ara
hyde_prompt = ChatPromptTemplate.from_template("""
Aşağıdaki soruya cevap veren kısa bir paragraf yaz (gerçek bilgi olması gerekmez,
sadece doğru terminoloji ve bağlamı kullan):

Soru: {question}
Cevap paragrafı:""")

hyde_chain = hyde_prompt | llm | StrOutputParser()

hypothetical_doc = hyde_chain.invoke({"question": "Kubernetes pod nedir?"})
print(f"\nHyDE document:\n{hypothetical_doc}")
# Bu dokümanın embedding'ini kullanarak search yaparsın
```
:::

---

## 8. RAG Evaluation — RAGAS

:::concept
## RAG Evaluation Metrics

RAG pipeline'ının kalitesini ölçmek için standart metric'ler:

| Metric | Ne Ölçer | Neye Bakar |
|--------|---------|-----------|
| **Faithfulness** | Cevap, kaynaklara sadık mı? | LLM uydurma bilgi eklememiş mi? |
| **Answer Relevancy** | Cevap, soruyla ilgili mi? | Konu dışına çıkılmamış mı? |
| **Context Precision** | Alınan dokümanlar ilgili mi? | Retrieval kalitesi |
| **Context Recall** | Tüm ilgili dokümanlar alınmış mı? | Retrieval coverage |

**RAGAS** framework'ü bu metric'leri otomatik hesaplar.
:::

:::code
## RAGAS ile RAG Evaluation

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset

# Evaluation dataset hazırla
eval_data = {
    "question": [
        "Python'da web geliştirme için hangi framework kullanılır?",
        "Docker nedir?",
    ],
    "answer": [
        "Python'da web geliştirme için Django, Flask ve FastAPI kullanılır.",
        "Docker, uygulamaları container'lar içinde çalıştıran bir platformdur.",
    ],
    "contexts": [
        [
            "Django full-stack Python web framework'üdür.",
            "Flask minimal Python web framework'üdür.",
            "FastAPI modern Python API framework'üdür."
        ],
        [
            "Docker containerization platformudur.",
            "Docker, uygulamaları izole ortamlarda çalıştırır."
        ]
    ],
    "ground_truth": [
        "Django, Flask ve FastAPI Python'un popüler web framework'leridir.",
        "Docker bir container platformudur."
    ]
}

dataset = Dataset.from_dict(eval_data)

# Evaluate
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
)

print(result)
# {'faithfulness': 0.95, 'answer_relevancy': 0.92,
#  'context_precision': 0.88, 'context_recall': 0.90}
```
:::

---

## 9. Production RAG Deployment

:::realworld
## Production RAG Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      Production RAG System                       │
│                                                                  │
│  [User Query]                                                    │
│       ↓                                                          │
│  [API Gateway] → Rate limiting, auth                             │
│       ↓                                                          │
│  [Query Processor] → Rewrite, multi-query, guardrails            │
│       ↓                                                          │
│  [Hybrid Retriever] → BM25 + Semantic search                    │
│       │                                                          │
│       ├── [Vector DB] (Pinecone/Qdrant)                         │
│       ├── [Keyword Index] (Elasticsearch)                       │
│       └── [Metadata Filter] (category, date, access)            │
│       ↓                                                          │
│  [Reranker] → Cross-encoder ile sonuçları rerank et              │
│       ↓                                                          │
│  [Context Builder] → Top-K docs + metadata + citations           │
│       ↓                                                          │
│  [LLM] → Generate response with citations                       │
│       ↓                                                          │
│  [Output Guardrails] → PII filter, hallucination check           │
│       ↓                                                          │
│  [Response + Sources]                                            │
│                                                                  │
│  [Background Jobs]:                                              │
│  - Document ingestion pipeline                                   │
│  - Embedding refresh                                             │
│  - Evaluation metrics (RAGAS)                                    │
│  - Cost & latency monitoring                                     │
└──────────────────────────────────────────────────────────────────┘
```
:::

:::code
## Production RAG Service

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import chromadb
import time
import logging

logger = logging.getLogger(__name__)

app = FastAPI()
client = OpenAI()

# Singleton vector store
chroma = chromadb.PersistentClient(path="./prod_chroma_db")
collection = chroma.get_or_create_collection("knowledge_base")

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    category_filter: str | None = None

class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]
    latency_ms: float
    tokens_used: int

@app.post("/api/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    start = time.time()

    # 1. Input validation
    if len(request.question) > 500:
        raise HTTPException(400, "Question too long")

    # 2. Retrieve
    search_kwargs = {"n_results": request.top_k}
    if request.category_filter:
        search_kwargs["where"] = {"category": request.category_filter}

    results = collection.query(
        query_texts=[request.question],
        **search_kwargs
    )

    if not results["documents"][0]:
        raise HTTPException(404, "No relevant documents found")

    # 3. Build context
    context_parts = []
    sources = []
    for i, (doc, meta) in enumerate(zip(
        results["documents"][0], results["metadatas"][0]
    )):
        context_parts.append(f"[{i+1}] {doc}")
        sources.append({"index": i+1, "text": doc[:100], "metadata": meta})

    context = "\n\n".join(context_parts)

    # 4. Generate
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """Soruları verilen kaynaklardan cevapla.
Her bilginin sonuna kaynak numarası ekle [1], [2] gibi.
Kaynaklarda olmayan bilgiyi ekleme."""
            },
            {"role": "user", "content": f"Kaynaklar:\n{context}\n\nSoru: {request.question}"}
        ],
        temperature=0,
        max_tokens=500
    )

    elapsed = (time.time() - start) * 1000

    logger.info(f"RAG query completed in {elapsed:.0f}ms, {response.usage.total_tokens} tokens")

    return QueryResponse(
        answer=response.choices[0].message.content,
        sources=sources,
        latency_ms=round(elapsed, 2),
        tokens_used=response.usage.total_tokens
    )
```
:::

:::warning
## Production RAG'da Dikkat Edilecekler

1. **Document access control**: Kullanıcının görmemesi gereken dokümanlar retrieval'da filtrelenmeli
2. **Stale data**: Dokümanlar güncellendiğinde embedding'ler de güncellenmeli
3. **Chunking quality**: Kötü chunking = kötü RAG. Doküman tipine göre strateji belirle
4. **Cost monitoring**: Her query için embedding + LLM cost'u takip et
5. **Latency budget**: Retrieval + LLM = toplam latency. SLA'ına uygun mu?
6. **Fallback**: Vector DB down olursa ne olacak? Graceful degradation planla
:::

---

## 10. Hands-On Exercise

:::exercise
## Mini Proje: Knowledge Base RAG System

Bir company knowledge base RAG sistemi oluştur:

### Requirements:
1. **Document Ingestion Pipeline**:
   - Markdown dosyalarını yükle
   - RecursiveCharacterTextSplitter ile chunk'la
   - OpenAI embeddings ile embed et
   - Chroma'ya kaydet

2. **Query Pipeline**:
   - Kullanıcı sorusu → embedding → similarity search
   - Top-5 sonuçları al
   - LLM ile kaynaklı cevap üret

3. **API Layer** (FastAPI):
   - `POST /ingest` — Doküman yükle
   - `POST /query` — Soru sor
   - `GET /stats` — Doküman sayısı, query sayısı

4. **Evaluation**:
   - 5 test sorusu hazırla
   - Faithfulness ve relevancy ölç

### Skeleton:
```python
from fastapi import FastAPI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

class KnowledgeBase:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            collection_name="company_kb",
            embedding_function=self.embeddings,
            persist_directory="./kb_data"
        )
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def ingest(self, text: str, metadata: dict) -> int:
        """Dokümanı chunk'la ve vector store'a ekle"""
        # TODO: Implement
        pass

    def query(self, question: str, k: int = 5) -> dict:
        """RAG query — retrieve + generate"""
        # TODO: Implement
        pass

app = FastAPI()
kb = KnowledgeBase()

@app.post("/ingest")
async def ingest_document(text: str, source: str):
    # TODO: Implement
    pass

@app.post("/query")
async def query_kb(question: str):
    # TODO: Implement
    pass
```

---

### Alıştırma 2: Chunking Stratejileri Karşılaştırması (Orta)

Aynı dokümanı farklı chunking stratejileriyle parçala ve retrieval kalitesini karşılaştır:

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

# Test dokümanı (en az 2000 kelimelik bir markdown dosyası kullan)
document = open("test_document.md").read()

# Strateji 1: Fixed-size chunking (naive)
splitter_fixed = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0,
    separator="\n"
)

# Strateji 2: Recursive chunking (overlap ile)
splitter_recursive = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# Strateji 3: Semantic chunking (header-based)
headers = [("#", "H1"), ("##", "H2"), ("###", "H3")]
splitter_semantic = MarkdownHeaderTextSplitter(headers_to_split_on=headers)

# TODO: Her strateji ile chunk'la
# TODO: Chunk sayısı, ortalama chunk boyutu, min/max boyut istatistiklerini yazdır
# TODO: 3 test sorusu hazırla ve her strateji ile retrieval yap
# TODO: Hangi strateji hangi soru için daha iyi sonuç veriyor? Neden?

# Değerlendirme tablosu:
# | Strateji    | Chunk Sayısı | Ort. Boyut | Soru 1 Doğru? | Soru 2 Doğru? | Soru 3 Doğru? |
# |-------------|-------------|------------|---------------|---------------|---------------|
# | Fixed       |             |            |               |               |               |
# | Recursive   |             |            |               |               |               |
# | Semantic    |             |            |               |               |               |
```

**Beklenen sonuç:** Overlap'li recursive chunking genelde en iyi sonucu verir. Semantic chunking bölüm bazlı sorularda daha iyi performans gösterir. Chunk boyutunun retrieval kalitesine etkisini raporla.

---

### Alıştırma 3: ReAct Agent — Tool-Calling Agent Oluştur (Zor)

Bir ReAct (Reasoning + Acting) agent oluştur:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool, tool
from langchain import hub

# Tool 1: Hesap makinesi
@tool
def calculator(expression: str) -> str:
    """Matematiksel ifadeyi hesaplar. Örnek: '2 + 3 * 4'"""
    # TODO: eval() KULLANMA! ast.literal_eval veya güvenli parser yaz
    pass

# Tool 2: Tarih bilgisi
@tool
def get_date_info(query: str) -> str:
    """Bugünün tarihi, günü, haftanın kaçıncı günü gibi bilgileri verir"""
    # TODO: datetime ile implement et
    pass

# Tool 3: Basit veritabanı sorgusu (mock)
@tool
def query_database(sql_description: str) -> str:
    """Doğal dil ile veritabanı sorgusu yapar. Örnek: 'en pahalı 3 ürün'"""
    # TODO: Mock data döndür (gerçek DB bağlantısı gerekmiyor)
    mock_products = [
        {"name": "Laptop", "price": 25000},
        {"name": "Telefon", "price": 15000},
        {"name": "Tablet", "price": 8000},
    ]
    pass

# Agent oluştur
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [calculator, get_date_info, query_database]

# TODO: ReAct prompt template al ve agent oluştur
# TODO: AgentExecutor ile çalıştır

# Test sorguları:
# 1. "En pahalı ürünün fiyatına %18 KDV ekle, sonucu söyle"
#    → Agent: query_database → calculator → cevap
# 2. "Bugün hangi gün? Haftasonuna kaç gün var?"
#    → Agent: get_date_info → calculator → cevap
# 3. "Veritabanındaki ürünlerin toplam değeri nedir?"
#    → Agent: query_database → calculator → cevap
```

**Beklenen sonuç:** Agent doğru tool'ları doğru sırada çağırmalı. Thought-Action-Observation döngüsünü console'da göster. En az 3 test sorusunun tamamını doğru cevaplamalı.

---

### Alıştırma 4: Embedding Model Karsilastirmasi (Kolay)

Farkli embedding modelleriyle retrieval kalitesini karsilastir.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

models = {
    "all-MiniLM-L6-v2": SentenceTransformer("all-MiniLM-L6-v2"),
    "multilingual": SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2"),
}

documents = [
    "Python ile web gelistirme icin Django ve FastAPI kullanilir",
    "React component lifecycle ve hooks kullanimi",
    "PostgreSQL indeks optimizasyonu ve query planlama",
    "Docker container'lari ile uygulama paketleme",
    "Machine learning model egitimi ve evaluation",
]

queries = [
    "web uygulamasi nasil yapilir",
    "veritabani performansi nasil arttirilir",
    "yapay zeka modeli nasil egitilir",
]

for model_name, model in models.items():
    doc_embeddings = model.encode(documents)
    print(f"\n=== {model_name} ===")
    for query in queries:
        query_emb = model.encode([query])
        scores = np.dot(doc_embeddings, query_emb.T).flatten()
        best_idx = np.argmax(scores)
        print(f"Q: {query}")
        print(f"A: {documents[best_idx]} (score: {scores[best_idx]:.4f})")

# TODO: OpenAI text-embedding-3-small ile karsilastir
# TODO: Turkce sorularda multilingual modelin avantajini goster
# TODO: Embedding boyutu vs kalite trade-off'unu analiz et
# TODO: Retrieval latency'yi olc (milisaniye bazinda)
```

**Beklenen Sonuc:** Multilingual model Turkce sorgularda daha iyi sonuc vermeli. OpenAI embedding'leri genel olarak en yuksek kaliteyi saglamali ama daha pahali.
**Ipucu:** all-MiniLM-L6-v2 hizli ve ucretiz. Production'da OpenAI embedding'leri daha iyi retrieval kalitesi verir.

---

### Alıştırma 5: Hybrid Search — BM25 + Semantic (Kolay)

Keyword search ve semantic search'u birlestirerek daha iyi sonuclar al.

```python
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import numpy as np

documents = [
    "FastAPI ile RESTful API gelistirme ve Pydantic validation",
    "React hooks: useState, useEffect, useContext kullanimi",
    "PostgreSQL JSONB indeks ve full-text search ozellikleri",
    "Kubernetes pod scaling ve resource management",
    "Transformer attention mechanism ve positional encoding",
]

# BM25 (keyword-based)
tokenized_docs = [doc.lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

# Semantic search
model = SentenceTransformer("all-MiniLM-L6-v2")
doc_embeddings = model.encode(documents)

def hybrid_search(query, alpha=0.5, top_k=3):
    # BM25 scores
    bm25_scores = bm25.get_scores(query.lower().split())
    bm25_norm = bm25_scores / (bm25_scores.max() + 1e-8)

    # Semantic scores
    query_emb = model.encode([query])
    semantic_scores = np.dot(doc_embeddings, query_emb.T).flatten()
    semantic_norm = (semantic_scores - semantic_scores.min()) / (semantic_scores.max() - semantic_scores.min() + 1e-8)

    # Hybrid (weighted combination)
    hybrid_scores = alpha * semantic_norm + (1 - alpha) * bm25_norm
    top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
    return [(documents[i], hybrid_scores[i]) for i in top_indices]

# TODO: "PostgreSQL JSONB" gibi teknik terimlerle test et (BM25 avantajli)
# TODO: "veritabani arama ozellikleri" gibi anlamsal sorgularla test et (semantic avantajli)
# TODO: Farkli alpha degerlerini dene (0.3, 0.5, 0.7)
# TODO: Reciprocal Rank Fusion (RRF) ile karsilastir
```

**Beklenen Sonuc:** Teknik terimler iceren sorgularda BM25 daha iyi, anlamsal sorgularda semantic search daha iyi olmali. Hybrid her iki durumda da makul sonuc vermeli.
**Ipucu:** alpha=0.5 baslangic icin iyi. Domain'e gore ayarla: teknik dokumanlar icin BM25 agirligini artir.

---

### Alıştırma 6: RAG Evaluation — RAGAS ile Kalite Olcumu (Orta)

RAG sisteminin kalitesini RAGAS metrikleriyle degerlendir.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

# Evaluation dataset
eval_data = {
    "question": [
        "Python'da list comprehension nasil kullanilir?",
        "Docker volume nedir?",
        "React useEffect hook'u ne ise yarar?",
    ],
    "answer": [
        "List comprehension [expression for item in iterable] seklinde kullanilir.",
        "Docker volume container verilerini kalici olarak saklar.",
        "useEffect side effect'leri yonetmek icin kullanilir.",
    ],
    "contexts": [
        ["Python'da list comprehension tek satirda liste olusturma yontemidir. [x**2 for x in range(10)] gibi kullanilir."],
        ["Docker volume, container silinse bile verilerin korunmasini saglar. Named volume ve bind mount turleri vardir."],
        ["useEffect hook'u component mount, update ve unmount yasam dongusunde yan etkileri yonetir."],
    ],
    "ground_truth": [
        "List comprehension [expression for item in iterable if condition] formatinda kullanilir.",
        "Docker volume container'larin disinda veri saklama mekanizmasidir.",
        "useEffect React'te side effect yonetimi icin kullanilan bir hook'tur.",
    ],
}

dataset = Dataset.from_dict(eval_data)
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])

# TODO: 20+ soru ile kapsamli evaluation dataset olustur
# TODO: Farkli chunking stratejileriyle RAGAS skorlarini karsilastir
# TODO: Faithfulness ve relevancy arasindaki korelasyonu analiz et
# TODO: Dusuk skorlu sorulari analiz et ve RAG pipeline'i iyilestir
```

**Beklenen Sonuc:** Faithfulness (cevap context'e dayaniyor mu) >0.8 olmali. Answer relevancy (cevap soruyla ilgili mi) >0.7 olmali. Context precision (dogru context getirilmis mi) >0.6 olmali.
**Ipucu:** RAGAS metrikleri LLM-based evaluation yapar. Faithfulness en kritik metrik — dusukse model hallucination yapiyor demektir.

---

### Alıştırma 7: Multi-Document RAG ve Citation (Orta)

Birden fazla kaynaktan bilgi toplayip kaynak gostererek cevap oluştur.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate

# Farkli kaynaklardan dokumanlar
sources = {
    "python_guide.md": "Python programlama rehberi...",
    "docker_docs.md": "Docker containerization...",
    "react_tutorial.md": "React ile frontend gelistirme...",
}

# Chunk'la ve metadata ekle
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_chunks = []
for source_name, content in sources.items():
    chunks = splitter.create_documents([content], metadatas=[{"source": source_name}])
    all_chunks.extend(chunks)

# Vector store
vectorstore = Chroma.from_documents(all_chunks, OpenAIEmbeddings())

# Citation prompt
citation_prompt = PromptTemplate.from_template("""Asagidaki kaynaklara dayanarak soruyu cevapla.
Her ifadenin sonuna kaynak belirt: [Kaynak: dosya_adi]

Kaynaklar:
{context}

Soru: {question}

Cevap (kaynak gostererek):""")

# TODO: Retriever ile top-5 chunk getir
# TODO: Her chunk'in hangi dosyadan geldigini goster
# TODO: Cevaptaki citation'larin dogru oldugunu dogrula
# TODO: Kaynak bulunamazsa "Bu konuda kaynagim yok" dedirt
```

**Beklenen Sonuc:** Cevaplar ilgili kaynaklar ile desteklenmeli. Her kaynak dogru dosyaya isaret etmeli. Kaynaksiz bilgi uretilmemeli.
**Ipucu:** Metadata ile kaynak takibi yap. Citation dogrulama icin cevaptaki bilgiyi kaynak chunk ile karsilastir.

---

### Alıştırma 8: Conversational RAG — Chat History ile (Zor)

Sohbet gecmisini kullanarak baglam-duyarli RAG sistemi olustur.

```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
memory = ConversationBufferWindowMemory(
    k=5,  # Son 5 mesaji hatirla
    memory_key="chat_history",
    return_messages=True,
    output_key="answer",
)

# Standalone question olusturma (chat history'den)
condense_prompt = PromptTemplate.from_template("""Sohbet gecmisine bakarak, son soruyu bagimsiz bir soruya donustur.
Sohbet gecmisi onemli baglam sagliyorsa kullan.

Sohbet Gecmisi: {chat_history}
Son Soru: {question}
Bagimsiz Soru:""")

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory,
    condense_question_prompt=condense_prompt,
)

# Test sohbeti
# User: "Docker nedir?"
# Bot: "Docker containerization platformudur..."
# User: "Peki bunu Python ile nasil kullanabilirim?"  ← "bunu" = Docker
# Bot: Docker Python SDK ile...

# TODO: 5 turlu sohbet senaryosu test et
# TODO: "o", "bunu", "onceki" gibi referanslarin dogru cozumlendigini dogrula
# TODO: Memory window boyutunun cevap kalitesine etkisini test et
# TODO: Sohbet gecmisini asiri uzun yapip context window sorununu gozlemle
```

**Beklenen Sonuc:** "bunu", "o" gibi referanslar dogru cozumlenmeli. Sohbet baglami korunmali. Context window asildiginda uygun truncation yapilmali.
**Ipucu:** Condense question adimi kritik: "bunu nasil yaparim" → "Docker'i Python ile nasil kullanirim" seklinde donusturmeli.

---

### Alıştırma 9: Production RAG Pipeline — End to End (Zor)

Production-ready RAG sistemi olustur: ingestion, retrieval, generation, monitoring.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import logging

app = FastAPI()
logger = logging.getLogger("rag_pipeline")

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    temperature: float = 0.1

class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]
    latency_ms: float
    token_count: int

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    start = time.time()

    # 1. Retrieve
    results = vectorstore.similarity_search_with_score(req.question, k=req.top_k)

    # 2. Filter (minimum similarity threshold)
    filtered = [(doc, score) for doc, score in results if score > 0.3]
    if not filtered:
        raise HTTPException(404, "Ilgili dokuman bulunamadi")

    # 3. Generate
    context = "\n\n".join([doc.page_content for doc, _ in filtered])
    answer = llm.invoke(f"Context: {context}\n\nSoru: {req.question}")

    # 4. Log metrics
    latency = (time.time() - start) * 1000
    logger.info(f"Query: {req.question} | Latency: {latency:.0f}ms | Sources: {len(filtered)}")

    return QueryResponse(
        answer=answer.content,
        sources=[{"content": d.page_content[:100], "metadata": d.metadata} for d, _ in filtered],
        latency_ms=latency,
        token_count=len(answer.content.split()),
    )

# TODO: Caching layer ekle (ayni sorulara hizli cevap)
# TODO: Rate limiting ekle
# TODO: Admin endpoint: dokuman ekleme/silme
# TODO: Feedback endpoint: kullanici cevabi begenip begenemdi
# TODO: Prometheus metrikleri ekle (latency, token count, cache hit rate)
```

**Beklenen Sonuc:** API endpoint'i <2 saniyede cevap vermeli. Kaynak bilgileri response'ta yer almali. Irrelevant sorgularda 404 donmeli.
**Ipucu:** Production'da caching %50+ latency dususu saglar. Redis ile semantic cache (benzer sorulara cache'ten cevap) daha da etkili.

---

### Alıştırma 10: Multi-Agent System — Takim Calismasi (Zor)

Birden fazla agent'in birlikte calisarak karmasik gorevleri cozdugu bir sistem olustur.

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

# Agent roller
researcher_tools = [
    Tool(name="web_search", func=lambda q: f"Arama sonuclari: {q}", description="Web'de arama yapar"),
    Tool(name="read_doc", func=lambda p: f"Dokuman icerigi: {p}", description="Dokuman okur"),
]

coder_tools = [
    Tool(name="write_code", func=lambda spec: f"Kod: {spec}", description="Kod yazar"),
    Tool(name="run_test", func=lambda code: "Testler gecti", description="Test calistirir"),
]

reviewer_tools = [
    Tool(name="review_code", func=lambda code: "Review: LGTM", description="Kod inceler"),
    Tool(name="check_security", func=lambda code: "Guvenli", description="Guvenlik kontrolu"),
]

class MultiAgentOrchestrator:
    def __init__(self):
        self.researcher = self._create_agent("Researcher", researcher_tools)
        self.coder = self._create_agent("Coder", coder_tools)
        self.reviewer = self._create_agent("Reviewer", reviewer_tools)

    def _create_agent(self, role, tools):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        # Agent olusturma kodu...
        return {"role": role, "tools": tools}

    async def solve(self, task):
        # 1. Researcher: konuyu arastir
        research = self.researcher  # .invoke(task)

        # 2. Coder: arastirma sonuclarina gore kod yaz
        code = self.coder  # .invoke(research)

        # 3. Reviewer: kodu incele
        review = self.reviewer  # .invoke(code)

        # TODO: Agent'lar arasi iletisim protokolu tasarla
        # TODO: Supervisor agent ekle (is dagitimi ve kalite kontrolu)
        # TODO: Deadlock ve sonsuz dongu korunmasi ekle (max iteration)
        # TODO: Her agent'in calisma logunu kaydet
        # TODO: Hata durumunda retry mekanizmasi ekle

orchestrator = MultiAgentOrchestrator()
```

**Beklenen Sonuc:** 3 agent sirali olarak calisip gorev tamamlamali. Supervisor agent kalite kontrolu yapmali. Max iteration ile sonsuz dongu onlenmeli.
**Ipucu:** CrewAI veya AutoGen gibi framework'ler multi-agent sistemi kolaylastirir. Agent rolleri net tanimlanmali — overlapping roller tutarsizliga yol acar.
:::

:::interview
## Mülakat Soruları

**S1**: "RAG nedir ve neden fine-tuning yerine tercih edilir?"

**Beklenen cevap**: RAG, LLM'e sorma anında ilgili dokümanları retrieve edip context olarak ekleme tekniğidir. Fine-tuning'e göre avantajları: verinin güncellenebilir olması, daha ucuz olması, kaynak gösterebilmesi ve hallucination'ı azaltması.

**S2**: "Chunking strategy seçerken nelere dikkat edersin?"

**Beklenen cevap**: Doküman tipine göre strateji seçerim. Chunk size genellikle 256-1024 token arası, overlap %10-15. Her chunk kendi başına anlamlı olmalı. Markdown için header-based, kod için function-based chunking. Metadata mutlaka eklerim.

**S3**: "AI Agent ile normal LLM çağrısı arasındaki fark nedir?"

**Beklenen cevap**: Normal LLM çağrısı tek soru-cevap döngüsüdür. Agent ise think-act-observe döngüsünde çalışır, araçlar kullanabilir, kendi kendine karar verir ve multi-step problem solving yapabilir.

**S4**: "Vector database'de cosine similarity nasıl çalışır?"

**Beklenen cevap**: İki vektör arasındaki açının kosinüsünü hesaplar. 1 = aynı yön (benzer anlam), 0 = dik (ilgisiz), -1 = zıt yön. Embedding'ler normalize edildiğinde dot product ile aynı sonucu verir.
:::

:::knowledge-check
## Bilgi Kontrolü

1. RAG'ın üç aşaması nedir?
2. Embedding nedir ve cosine similarity nasıl çalışır?
3. Chunking'de overlap neden kullanılır?
4. Chroma, FAISS ve Pinecone arasındaki farklar neler?
5. LangChain'de chain ve agent arasındaki fark nedir?
6. Hybrid search neden sadece semantic search'ten daha iyi?
7. RAGAS'ın faithfulness metric'i ne ölçer?
8. Production RAG'da access control neden kritik?
:::

:::english
## Key Terms

| Term | Pronunciation | Turkish | Description |
|------|--------------|---------|-------------|
| Retrieval | /rɪˈtriː.vəl/ | Erişim/Getirme | İlgili dokümanları bulma |
| Embedding | /ɪmˈbed.ɪŋ/ | Gömme | Text'i vektöre dönüştürme |
| Vector | /ˈvek.tɚ/ | Vektör | Yönlü büyüklük, sayı dizisi |
| Chunk | /tʃʌŋk/ | Parça | Dokümanın bölünmüş parçası |
| Similarity | /ˌsɪm.əˈler.ə.ti/ | Benzerlik | İki vektör arası mesafe |
| Agent | /ˈeɪ.dʒənt/ | Ajan | Otonom karar veren AI sistemi |
| Orchestration | /ˌɔːr.kɪˈstreɪ.ʃən/ | Orkestrasyon | Birden fazla bileşeni koordine etme |
| Inference | /ˈɪn.fɚ.əns/ | Çıkarım | Model'in tahmin yapması |
| Hallucination | /həˌluː.sɪˈneɪ.ʃən/ | Halüsinasyon | Uydurma bilgi üretme |
| Reranking | /riːˈræŋ.kɪŋ/ | Yeniden sıralama | Sonuçları tekrar sıralama |
:::

:::external-resource
## Ek Kaynaklar

- [LangChain Documentation](https://python.langchain.com/docs/)
- [Chroma Documentation](https://docs.trychroma.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [FAISS — Facebook AI Similarity Search](https://github.com/facebookresearch/faiss)
- [RAGAS — RAG Evaluation](https://docs.ragas.io/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
:::
