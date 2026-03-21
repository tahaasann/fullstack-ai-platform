const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, 'project-08.json');

const D = {
  id: "project-08",
  title: "Multi-Agent AI Customer Support Sistemi",
  difficulty: "advanced",
  estimated_days: 14,
  tech_stack: ["Python","LangChain","LangGraph","FastAPI","OpenAI API","ChromaDB","Redis","PostgreSQL","WebSocket","Docker","React","TypeScript"],
  brief: `Bu projede LangChain + LangGraph kullanarak birden fazla AI agent'ın koordineli çalıştığı akıllı müşteri destek sistemi oluşturacaksın. FAQ agent, teknik destek agent, fatura agent gibi uzmanlaşmış agent'lar router tarafından yönlendirilecek. Human handoff, sentiment analizi ve conversation analytics dahil.

Sistem, gelen müşteri mesajını analiz edip doğru agent'a yönlendiren bir Router Agent içerecek. Her agent kendi tool'larına sahip olacak — FAQ agent knowledge base'den arama yapacak, fatura agent veritabanından fatura bilgisi çekecek, teknik destek agent troubleshooting adımları sunacak. Agent'lar arası geçiş, LangGraph state machine ile yönetilecek.

Müşteri memnuniyetsizliği tespit edildiğinde otomatik human handoff devreye girecek. Tüm konuşmalar loglanacak, agent performansı ve müşteri memnuniyeti dashboard üzerinden izlenecek. Production ortamı için Docker, rate limiting, fallback mekanizmaları ve structured logging eklenecek.

Bu proje, AI Engineer ve LLM Engineer pozisyonları için en güçlü portfolio parçası olacak çünkü multi-agent orchestration, tool calling, RAG ve production deployment konularını tek projede birleştiriyor.`,
  target_roles: ["AI Engineer","LLM Engineer"],
  architecture: {
    overview: "Multi-agent mimarisi: Router Agent gelen mesajı analiz edip uygun specialist agent'a yönlendiriyor. Her agent LangChain ile oluşturulmuş, LangGraph state machine ile orchestrate ediliyor. ChromaDB ile RAG tabanlı knowledge base, Redis ile session/memory yönetimi, PostgreSQL ile conversation logging. FastAPI backend, WebSocket ile real-time human handoff, React dashboard ile analytics.",
    diagram: `┌─────────────────────────────────────────────────────────────────┐
│                        Client (React)                           │
│              Chat UI  |  Admin Dashboard  |  Analytics          │
├─────────────────────────────────────────────────────────────────┤
│                   FastAPI + WebSocket Server                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  LangGraph Orchestrator                  │   │
│  │              (State Machine / Graph Flow)                │   │
│  └──────────────────────┬──────────────────────────────────┘   │
│           ┌─────────────┼─────────────┐                        │
│           ▼             ▼             ▼                        │
│  ┌──────────────┐ ┌──────────┐ ┌────────────┐                  │
│  │ Router Agent │ │ Sentinel │ │  Fallback  │                  │
│  │  (Classify)  │ │(Sentiment│ │   Agent    │                  │
│  └──────┬───────┘ │ Guard)   │ └────────────┘                  │
│    ┌────┼────────────┬──────────────┐                           │
│    ▼    ▼            ▼              ▼                           │
│ ┌─────┐ ┌──────┐ ┌────────┐ ┌───────────┐                     │
│ │ FAQ │ │Billing│ │Tech    │ │  Human    │                     │
│ │Agent│ │Agent  │ │Support │ │  Handoff  │                     │
│ └──┬──┘ └──┬───┘ │Agent   │ └───────────┘                     │
│    ▼       ▼     └───┬────┘                                    │
│ ChromaDB  PostgreSQL  KB Search + Tools                        │
└─────────────────────────────────────────────────────────────────┘`,
    decisions: [
      {decision:"Neden LangGraph (AutoGen/CrewAI yerine)?",reasoning:"LangGraph, agent flow'unu açık bir directed graph olarak tanımlar — her node bir agent veya fonksiyon, her edge bir geçiş koşulu. Bu, debugging ve testing'i çok kolaylaştırır çünkü flow görselleştirilebilir. State machine yapısı sayesinde agent geçişleri deterministiktir, race condition riski yoktur. LangChain ekosistemi ile native entegrasyon sağlar.",alternatives:"AutoGen, CrewAI, custom orchestration",when_to_choose_alternative:"AutoGen: Agent'lar arası serbest konuşma gerekiyorsa. CrewAI: Basit sequential task pipeline'ları için. Custom: Tam kontrol ve minimum dependency isteniyorsa."},
      {decision:"Neden ChromaDB (Pinecone/Weaviate yerine)?",reasoning:"ChromaDB açık kaynaklı ve local olarak çalışır — API key veya cloud hesabı gerektirmez. Development ve test ortamında sıfır maliyet. Production'da Pinecone'a geçiş kolay çünkü LangChain abstraction layer kullanıyoruz.",alternatives:"Pinecone, Weaviate, Qdrant, FAISS",when_to_choose_alternative:"Pinecone: Managed, serverless vector DB gerekiyorsa. Weaviate: Hybrid search. FAISS: Sadece similarity search, metadata gerekmiyorsa. Qdrant: Self-hosted production vector DB."},
      {decision:"Neden Specialist Agent'lar (tek monolitik agent yerine)?",reasoning:"Her agent kendi system prompt'u, tool'ları ve konteksti ile çalışır. FAQ agent sadece knowledge base arar, fatura agent sadece veritabanı sorgular. Bu separation of concerns, her agent'ı bağımsız test etmeyi ve optimize etmeyi kolaylaştırır. Token kullanımı da azalır çünkü her agent sadece kendi bağlamını taşır.",alternatives:"Tek büyük agent, function routing, prompt chaining",when_to_choose_alternative:"Tek agent: Basit chatbot'larda (5'ten az tool). Function routing: Agent mantığı gerekmiyorsa. Prompt chaining: Sequential workflow, paralel agent gerekmiyorsa."},
      {decision:"Neden Redis ile Conversation Memory?",reasoning:"Redis, conversation state'i ve kısa süreli memory'yi hızlıca saklar. TTL ile eski session'lar otomatik temizlenir. LangChain'in RedisChatMessageHistory ile native entegrasyonu vardır. Birden fazla API instance'ı aynı Redis'e bağlanarak horizontal scaling yapabilir.",alternatives:"In-memory (dict), PostgreSQL, MongoDB, DynamoDB",when_to_choose_alternative:"In-memory: Development/test ortamında. PostgreSQL: Uzun süreli conversation archiving. MongoDB: Esnek schema gerekiyorsa. DynamoDB: AWS-native, serverless mimari."},
      {decision:"Neden WebSocket (polling yerine) Human Handoff İçin?",reasoning:"Human handoff anında müşteri ile insan agent arasında real-time iletişim gerekir. WebSocket bidirectional bağlantı sağlar — mesajlar anında iletilir. HTTP polling'de latency ve gereksiz request overhead olur.",alternatives:"Server-Sent Events (SSE), Long polling, gRPC streaming",when_to_choose_alternative:"SSE: Sadece server'dan client'a tek yönlü stream gerekiyorsa. Long polling: WebSocket desteklenmeyen ortamlarda. gRPC: Microservice-to-microservice iletişiminde."}
    ]
  },
  what_you_learn: {
    technical: ["LangChain ile AI agent oluşturma (prompt templates, chains, tools)","LangGraph ile multi-agent orchestration (state machines, graph flow)","RAG (Retrieval Augmented Generation) ile knowledge base arama","ChromaDB ile vector store yönetimi ve semantic search","OpenAI function calling / tool use implementasyonu","Conversation memory yönetimi (buffer, summary, Redis-backed)","Sentiment analizi ile otomatik escalation","WebSocket ile real-time human handoff","FastAPI ile async API geliştirme","PostgreSQL ile conversation logging ve analytics","Docker multi-service orchestration","Structured logging ve observability"],
    architectural: ["Multi-agent system design patterns","Router pattern ile intelligent message dispatching","State machine tabanlı workflow yönetimi","RAG pipeline tasarımı (chunking, embedding, retrieval)","Graceful degradation ve fallback stratejileri","Event-driven architecture (agent transitions)","Horizontal scaling considerations"],
    soft_skills: ["AI system tasarım kararlarını dokümante etme","Prompt engineering ve iteration","Agent performans metrikleri tanımlama ve yorumlama","Trade-off analizi (accuracy vs latency vs cost)","Production incident senaryoları planlama"]
  },
  requirements: {
    functional: ["Router Agent: Gelen mesajı analiz edip doğru specialist agent'a yönlendirme","FAQ Agent: Knowledge base'den semantik arama ile cevap bulma (RAG)","Billing Agent: Veritabanından fatura/sipariş bilgisi sorgulama","Tech Support Agent: Troubleshooting adımları sunma, tool calling ile sistem kontrolü","Conversation memory: Multi-turn konuşma bağlamını koruma","Sentiment analizi: Müşteri memnuniyetsizliğini tespit etme","Human handoff: Otomatik escalation ve WebSocket ile real-time transfer","Conversation logging: Tüm mesajları ve agent kararlarını kaydetme","Analytics dashboard: Agent performansı, response time, resolution rate","Feedback toplama: Müşteri memnuniyet puanı (CSAT)"],
    non_functional: ["Response time: Agent yanıtı <3 saniye (LLM dahil)","Uptime: Fallback agent ile %99.9 availability","Concurrency: En az 50 eşzamanlı konuşma desteği","Memory: Conversation context 20+ mesaj boyunca korunmalı","Security: Input sanitization, rate limiting, API key rotation","Observability: Structured logging, request tracing","Scalability: Stateless API, Redis session store ile horizontal scaling"]
  },
  evaluation_criteria: [
    {criteria:"Multi-Agent Orchestration",description:"LangGraph ile agent routing, state management ve agent geçişlerinin doğru çalışması",weight:20},
    {criteria:"RAG Pipeline Kalitesi",description:"Knowledge base chunking, embedding ve retrieval'ın alakalı sonuçlar döndürmesi",weight:15},
    {criteria:"Tool Calling Implementasyonu",description:"Agent'ların DB lookup, KB search gibi tool'ları doğru kullanması",weight:15},
    {criteria:"Conversation Memory",description:"Multi-turn konuşmalarda bağlamın korunması ve memory stratejisi",weight:10},
    {criteria:"Human Handoff Mekanizması",description:"Sentiment tabanlı escalation ve WebSocket ile seamless transfer",weight:10},
    {criteria:"Error Handling & Fallback",description:"LLM timeout, API hatası, bilinmeyen intent durumlarında graceful degradation",weight:10},
    {criteria:"Analytics & Observability",description:"Conversation metrics, agent performance tracking, structured logging",weight:10},
    {criteria:"Production Readiness",description:"Docker, rate limiting, environment config, health checks",weight:10}
  ]
};

// Write first part
fs.writeFileSync(OUT, JSON.stringify(D, null, 2), 'utf-8');
console.log('Base written:', fs.statSync(OUT).size, 'bytes');
