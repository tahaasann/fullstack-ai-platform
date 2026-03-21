"""Generate project-08.json: Multi-Agent Customer Support System"""
import json, os

project = {
    "id": "project-08",
    "title": "Multi-Agent Musteri Destek Sistemi",
    "difficulty": "Zor",
    "estimated_days": 14,
    "tech_stack": ["React", "TypeScript", "Node.js", "FastAPI", "LangChain", "LangGraph", "PostgreSQL", "WebSocket", "Redis"],
    "target_roles": ["AI Engineer", "LLM Engineer", "Full Stack Developer"],
    "brief": "Bu projede, birden fazla AI agent'in koordineli calisarak musteri destek taleplerini yonettigi kapsamli bir sistem insa edeceksin. Gercek dunyada Zendesk, Intercom gibi platformlarin AI versiyonunu dusun — ama senin sisteminDE her agent'in belirli bir uzmanlik alani var ve LangGraph ile state machine mantigi kullanarak birbirleriyle iletisim kuruyorlar.\n\nModern musteri destek sistemleri artik tek bir chatbot'tan cok daha fazlasi. Router agent gelen mesaji analiz edip dogru uzman agent'a yonlendiriyor. FAQ agent sik sorulan sorulari aninda cevapliyor. Technical support agent karmasik teknik sorunlari cozerken knowledge base'den bilgi cekiyor. Escalation agent ise durumu insana aktarmasi gerektiginde tum context'i koruyarak handoff yapiyor.\n\nBu proje seni AI agent mimarisi, state management, real-time iletisim ve production-ready AI sistemleri konularinda derinlemesine egitecek. Mulakatlarda 'multi-agent sistem tasarladiniz mi?' sorusuna gercek deneyimle cevap verebileceksin.",
    "architecture": {
        "overview": "Sistem, LangGraph ile orkestre edilen multi-agent mimarisi uzerine kurulu. Her agent bagimsiz bir LLM chain olarak calisir, ancak paylasilan state uzerinden koordine olurlar. WebSocket ile real-time iletisim, Redis ile session management ve caching, PostgreSQL ile kalici veri depolama saglaniyor.",
        "diagram": """
┌─────────────┐     WebSocket      ┌──────────────┐
│   React UI  │◄──────────────────►│  Node.js WS  │
│  (Chat UI)  │                    │   Gateway     │
└─────────────┘                    └──────┬───────┘
                                          │
                                   ┌──────▼───────┐
                                   │  FastAPI      │
                                   │  Orchestrator │
                                   └──────┬───────┘
                                          │
                        ┌─────────────────┼─────────────────┐
                        │                 │                   │
                 ┌──────▼──────┐  ┌──────▼──────┐  ┌───────▼──────┐
                 │   Router    │  │  Knowledge  │  │    Redis     │
                 │   Agent     │  │   Base      │  │  (Sessions)  │
                 └──────┬──────┘  │  (RAG)      │  └──────────────┘
                        │         └─────────────┘
          ┌─────────────┼─────────────┐
          │             │             │
   ┌──────▼──────┐ ┌───▼────┐ ┌─────▼──────┐
   │  FAQ Agent  │ │ Tech   │ │ Escalation │
   │             │ │ Agent  │ │   Agent    │
   └─────────────┘ └────────┘ └────────────┘
        """,
        "decisions": [
            {
                "decision": "Neden LangGraph?",
                "reasoning": "LangGraph, stateful agent workflow'lari icin tasarlanmis. Her agent arasindaki gecisleri graph olarak modelleyebiliyoruz — hangi agent'tan hangisine ne zaman gecilecegi net ve debug edilebilir. State machine mantigi ile agent'lar arasi veri akisi kontrol altinda.",
                "alternatives": "CrewAI, AutoGen, sade LangChain chains",
                "when_to_choose_alternative": "Basit, sirasal agent islemleri icin LangChain chains yeterli. CrewAI daha yuksek seviye ama daha az kontrol sagliyor."
            },
            {
                "decision": "Neden WebSocket + Node.js Gateway?",
                "reasoning": "Real-time chat icin WebSocket sart. Node.js event-driven yapisi ile binlerce concurrent baglanti verimli yonetilebilir. FastAPI ise AI orchestration tarafinda kalir — separation of concerns.",
                "alternatives": "FastAPI WebSocket, Socket.io, Server-Sent Events",
                "when_to_choose_alternative": "Tek yonlu streaming yeterliyse SSE daha basit. Kucuk olcekli projede FastAPI WebSocket yeter."
            },
            {
                "decision": "Neden Redis session management?",
                "reasoning": "Conversation state'i bellekte tutmak horizontal scaling'i engeller. Redis ile her server instance ayni session'a erisebilir. Ayrica agent arasi gecici veri paylasimi ve rate limiting icin de kullanilir.",
                "alternatives": "In-memory state, PostgreSQL, Memcached",
                "when_to_choose_alternative": "Tek server'da calisiyorsan in-memory yeterli. Kalici session gerekiyorsa PostgreSQL."
            },
            {
                "decision": "Neden ayri Router Agent?",
                "reasoning": "Intent classification'i ayri bir agent'a vermek, diger agent'larin sadece kendi uzmanlik alanina odaklanmasini saglar. Router agent lightweight olabilir — kucuk model ile hizli siniflandirma yapar, agir isler uzman agent'lara kalir.",
                "alternatives": "Tek buyuk agent, keyword-based routing, classification model",
                "when_to_choose_alternative": "Az sayida kategori varsa keyword-based routing daha hizli ve ucuz. Cok spesifik domain'lerde fine-tuned classification model daha dogru."
            }
        ]
    },
    "what_you_learn": {
        "technical": [
            "LangGraph ile stateful multi-agent workflow tasarimi",
            "WebSocket real-time bidirectional iletisim",
            "Redis session management ve caching",
            "RAG (Retrieval Augmented Generation) entegrasyonu",
            "Conversation memory ve context management",
            "PostgreSQL ile chat history ve analytics"
        ],
        "architectural": [
            "Multi-agent system design patterns",
            "Event-driven architecture",
            "State machine design",
            "Service separation (WS gateway vs AI orchestrator)",
            "Graceful degradation ve fallback stratejileri"
        ],
        "ai_specific": [
            "Agent routing ve intent classification",
            "Prompt engineering for specialized agents",
            "Context window management",
            "Human-in-the-loop patterns",
            "Sentiment analysis ve conversation quality scoring",
            "LLM response streaming"
        ],
        "soft_skills": [
            "Complex system architecture documentation",
            "Multi-component debugging",
            "Performance monitoring ve optimization",
            "User experience design for AI interactions"
        ]
    },
    "requirements": {
        "functional": [
            "Kullanici mesaj gonderdiginde Router Agent otomatik siniflandirma yapmali",
            "FAQ Agent: Sik sorulan sorulari knowledge base'den cevaplayabilmeli",
            "Tech Agent: Teknik sorunlari adim adim cozebilmeli",
            "Escalation Agent: Gerektiginde insana aktarabilmeli",
            "Tum konusma gecmisi kaydedilmeli ve aranabilmeli",
            "Real-time mesajlasma (WebSocket)",
            "Agent performans dashboard'u"
        ],
        "non_functional": [
            "Ilk agent yaniti < 2 saniye",
            "Concurrent 100+ aktif konusma destegi",
            "Mesaj kaybi olmamali (at-least-once delivery)",
            "Agent gecisleri kullaniciya seffaf olmali"
        ],
        "ai_requirements": [
            "Router Agent %90+ dogru siniflandirma orani",
            "Context window limiti asildikinda conversation summarization",
            "Hallucination detection icin confidence scoring",
            "Fallback: AI cevaplayamazsa insan agent'a yonlendirme"
        ]
    },
    "evaluation_criteria": [
        {"criterion": "Multi-Agent Orchestration", "weight": 25, "description": "LangGraph workflow dogru calisiyormu, agent gecisleri duzgun mu"},
        {"criterion": "Real-time Communication", "weight": 15, "description": "WebSocket baglantisi stabil mi, mesajlar aninda iletiyor mu"},
        {"criterion": "Knowledge Base & RAG", "weight": 20, "description": "RAG pipeline dogru dokuman ceziyor mu, cevaplar alakali mi"},
        {"criterion": "Human Handoff", "weight": 15, "description": "Escalation akisi tam context ile calisiyormu"},
        {"criterion": "Analytics & Monitoring", "weight": 10, "description": "Agent performansi olculebiliyor mu"},
        {"criterion": "Code Quality & Testing", "weight": 15, "description": "Clean code, test coverage, error handling"}
    ],
    "milestones": [
        {
            "id": "p08-m1",
            "title": "Proje Altyapisi & Agent Mimari Tasarimi",
            "overview": "Monorepo yapisini kur, temel servisleri ayaga kaldir, LangGraph ile ilk agent graph'ini olustur.",
            "estimated_hours": 10,
            "concepts_covered": ["monorepo", "Docker Compose", "LangGraph basics", "agent design"],
            "steps": [
                {
                    "step": 1,
                    "title": "Monorepo & Docker Compose Setup",
                    "why": "Multi-service projeler icin tekrarlanabilir ortam sart. docker-compose ile tum servisleri tek komutla ayaga kaldirabilmek gelistirme hizini artirir.",
                    "instructions": "Proje yapisini olustur:\n- /frontend (React + TypeScript)\n- /gateway (Node.js WebSocket server)\n- /orchestrator (FastAPI + LangGraph)\n- /shared (ortak tipler ve config)\n\ndocker-compose.yml ile PostgreSQL, Redis, gateway ve orchestrator servislerini tanimla.",
                    "code_snippet": "# docker-compose.yml\nservices:\n  postgres:\n    image: postgres:16\n    environment:\n      POSTGRES_DB: support\n      POSTGRES_PASSWORD: dev123\n    ports: ['5432:5432']\n  redis:\n    image: redis:7-alpine\n    ports: ['6379:6379']\n  orchestrator:\n    build: ./orchestrator\n    ports: ['8000:8000']\n    depends_on: [postgres, redis]",
                    "checkpoint": "docker-compose up ile tum servisler hatasiz ayaga kalkiyor mu?"
                },
                {
                    "step": 2,
                    "title": "LangGraph Agent Graph Tasarimi",
                    "why": "Agent'lar arasi gecis mantigi basinda dogru tasarlanmazsa sonradan degistirmek cok zor olur. Graph-based yaklasimayla agent workflow'u gorunur ve test edilebilir hale gelir.",
                    "instructions": "LangGraph ile temel agent graph'ini olustur:\n1. State schema tanimla (messages, current_agent, metadata)\n2. Router node: intent classification\n3. FAQ node: knowledge base lookup\n4. Tech Support node: step-by-step troubleshooting\n5. Escalation node: human handoff\n6. Conditional edges: router'dan diger agent'lara gecis kurallari",
                    "code_snippet": "from langgraph.graph import StateGraph, END\nfrom typing import TypedDict, List\n\nclass AgentState(TypedDict):\n    messages: List[dict]\n    current_agent: str\n    intent: str\n    confidence: float\n    context: dict\n\ngraph = StateGraph(AgentState)\ngraph.add_node('router', router_agent)\ngraph.add_node('faq', faq_agent)\ngraph.add_node('tech', tech_agent)\ngraph.add_node('escalation', escalation_agent)\n\ngraph.add_conditional_edges('router', route_decision, {\n    'faq': 'faq',\n    'technical': 'tech',\n    'escalation': 'escalation'\n})",
                    "checkpoint": "Graph compile edip basit bir mesajla router -> faq akisi calisiyor mu?"
                },
                {
                    "step": 3,
                    "title": "Router Agent Implementation",
                    "why": "Router agent tum sistemin giris noktasi — dogru siniflandirma yapmasi kritik. Yanlis yonlendirme kullanici deneyimini dogrudan etkiler.",
                    "instructions": "Router agent icin:\n1. Intent categories tanimla (faq, technical, billing, escalation)\n2. Few-shot prompt ile LLM-based classification\n3. Confidence threshold — dusukse clarification sor\n4. Fallback: siniflandirma yapalamazsa escalation'a yonlendir",
                    "code_snippet": "ROUTER_PROMPT = '''\nSen bir musteri destek router'isin. Gelen mesaji siniflandir.\n\nKategoriler:\n- faq: Sik sorulan sorular, genel bilgi\n- technical: Teknik sorun, hata, bug\n- billing: Odeme, fatura, abonelik\n- escalation: Kizgin musteri, karmasik sorun\n\nMesaj: {message}\n\nJSON formatinda yanit ver:\n{{\"intent\": \"...\", \"confidence\": 0.0-1.0, \"reason\": \"...\"}}\n'''",
                    "checkpoint": "5 farkli mesaj tipi ile test et — dogru siniflandirma yapiyor mu?"
                },
                {
                    "step": 4,
                    "title": "Temel API Endpoints",
                    "why": "Frontend ile iletisim icin REST API gerekli. WebSocket henuz yok — once REST ile temel akisi dogrula, sonra real-time ekle.",
                    "instructions": "FastAPI endpoints:\n- POST /api/conversations — yeni konusma baslat\n- POST /api/conversations/{id}/messages — mesaj gonder\n- GET /api/conversations/{id} — konusma detayi\n- GET /api/conversations — liste",
                    "checkpoint": "Postman/curl ile mesaj gonderip agent cevabi aliyor musun?"
                }
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. LangGraph'te state IMMUTABLE olmali — her node yeni state dondurur\n2. Router agent'in confidence threshold'u cok onemli — 0.7 altinda clarification sor\n3. Agent graph'ini once kagit uzerinde ciz, sonra koda dok\n4. Her agent'in fallback davranisi OLMALI — hata durumunda sistem cokmemeli",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nMulti-agent sistemlerde en buyuk hata: agent'lari cok akilli yapmaya calismak. Her agent TEK BIR IS yapmali — Unix felsefesi. Router siniflandirir, FAQ cevaplar, Tech cozer. Bir agent hem siniflandirip hem cozmeye calisirsa debug cehennem olur.\n\nProduction'da agent routing'i A/B test et. Bazen basit keyword matching, LLM-based routing'den daha hizli ve guvenilir olabilir. Hybrid approach: once keyword match, eslesme yoksa LLM'e sor."
        },
        {
            "id": "p08-m2",
            "title": "Temel Agent'lar & LangGraph Workflow",
            "overview": "FAQ Agent ve Tech Support Agent'i implement et. Her agent'in kendi prompt'u, tool'lari ve davranis kurallari olacak.",
            "estimated_hours": 12,
            "concepts_covered": ["prompt engineering", "tool use", "agent specialization", "chain-of-thought"],
            "steps": [
                {
                    "step": 1,
                    "title": "FAQ Agent — Knowledge Base Lookup",
                    "why": "FAQ'lar musterilerin %60-70'ini kapsar. Bu agent'i iyi yapmak toplam destek kalitesini dramatik artirir.",
                    "instructions": "FAQ Agent icin:\n1. FAQ veritabani olustur (soru-cevap ciftleri)\n2. Semantic search ile en alakali FAQ'lari bul\n3. Bulunan FAQ'larla LLM'e cevap urettir\n4. Cevap bulunamazsa Tech Agent'a yonlendir",
                    "code_snippet": "async def faq_agent(state: AgentState) -> AgentState:\n    query = state['messages'][-1]['content']\n    \n    # Semantic search in FAQ database\n    relevant_faqs = await search_faqs(query, top_k=3)\n    \n    if not relevant_faqs or relevant_faqs[0].score < 0.7:\n        return {**state, 'current_agent': 'tech', 'intent': 'needs_escalation'}\n    \n    context = '\\n'.join([f.answer for f in relevant_faqs])\n    response = await llm.ainvoke(FAQ_PROMPT.format(\n        question=query, context=context\n    ))\n    \n    return {**state, 'messages': state['messages'] + [{'role': 'assistant', 'content': response}]}",
                    "checkpoint": "3 farkli FAQ sorusu ile dogru cevap donuyor mu?"
                },
                {
                    "step": 2,
                    "title": "Tech Support Agent — Step-by-Step Troubleshooting",
                    "why": "Teknik sorunlar adim adim cozum gerektirir. Agent multi-turn konusmada onceki adimlari hatirlamali ve bir sonraki adimi onermelidir.",
                    "instructions": "Tech Agent:\n1. Sorun tespiti icin soru sor (diagnostic questions)\n2. Knowledge base'den ilgili troubleshooting guide'i cek\n3. Adim adim cozum sun\n4. Her adimda kullanicidan feedback al\n5. Cozulemezse escalation'a yonlendir",
                    "checkpoint": "Bir teknik sorunu 3 adimda cozebildi mi? Cozemezse escalation'a yonlendirdi mi?"
                },
                {
                    "step": 3,
                    "title": "Agent Gecis Mantigi (Conditional Edges)",
                    "why": "Agent'lar arasi gecis kurallari sistemin beynini olusturur. Yanlis gecis = yanlis agent = mutsuz musteri.",
                    "instructions": "LangGraph conditional edges:\n1. Router -> FAQ: confidence > 0.8 ve intent='faq'\n2. Router -> Tech: intent='technical'\n3. FAQ -> Tech: FAQ cevap bulamadiysa\n4. Tech -> Escalation: 3 adim sonra cozulemediyse\n5. Any -> Escalation: kullanici kizginlik seviyesi yuksekse",
                    "checkpoint": "Tum gecis senaryolarini test et — dogru agent'a yonleniyor mu?"
                },
                {
                    "step": 4,
                    "title": "Conversation State Management",
                    "why": "Multi-turn konusmalarda context kaybi en buyuk sorun. Her agent, onceki agent'in ne yaptigini bilmeli.",
                    "instructions": "State'e metadata ekle:\n- conversation_summary: uzun konusmalarda ozet\n- attempted_solutions: denenimis cozumler\n- customer_sentiment: musteri duygu durumu\n- escalation_reason: neden eskale edildi",
                    "checkpoint": "5 mesajlik bir konusmada context korunuyor mu? Agent onceki mesajlari hatirlıyor mu?"
                }
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Her agent'in system prompt'u KISA ve ODAKLI olmali — 500 token'dan fazla olmasin\n2. Agent gecislerinde TÜÜM context aktarilmali — kullanici kendini tekrarlamak zorunda kalmamali\n3. Sentiment analysis basit olabilir: LLM'e 'musteri kizgin mi?' diye sor, 1-5 skor al\n4. Tech agent max 5 adim denemeli — sonra insan devralmali",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nAgent prompt'larini versiyon kontrol et — Git'te tutmak test ve rollback icin kritik. Her prompt degisikligini A/B test et. Production'da prompt degisikligi = kod degisikligi kadar riskli.\n\nConversation state boyutunu monitor et. LLM context window'u dolunca ya summarization yap ya da eski mesajlari kirp. Token maliyeti cok hizli artar."
        },
        {
            "id": "p08-m3",
            "title": "Knowledge Base & RAG Entegrasyonu",
            "overview": "Agent'larin dogru bilgiye erismesi icin RAG pipeline kur. Dogrudan FAQ veritabani + vektorel arama.",
            "estimated_hours": 10,
            "concepts_covered": ["RAG", "embeddings", "vector search", "ChromaDB", "document processing"],
            "steps": [
                {
                    "step": 1,
                    "title": "Document Processing Pipeline",
                    "why": "Knowledge base'e girecek dokumanlar (FAQ, troubleshooting guide, product docs) islenip chunk'lanmali. Dogru chunking = dogru retrieval.",
                    "instructions": "1. Markdown/text dokumanlar icin parser yaz\n2. Semantic chunking uygula (heading-based)\n3. Her chunk'a metadata ekle (source, category, last_updated)\n4. ChromaDB'ye embedding ile kaydet",
                    "checkpoint": "10 dokuman yukleyip semantic search ile dogru chunk donuyor mu?"
                },
                {
                    "step": 2,
                    "title": "Hybrid Retrieval (Dense + Sparse)",
                    "why": "Sadece embedding-based arama bazen keyword match'i kacirır. Hybrid approach ikisinin gucunu birlestirir.",
                    "instructions": "1. Dense retrieval: embedding similarity\n2. Sparse retrieval: BM25 keyword matching\n3. Reciprocal Rank Fusion ile sonuclari birlesir\n4. Top-K sonucu agent'a context olarak ver",
                    "checkpoint": "Keyword-agirlikli ve semantic-agirlikli sorularda ikisi de iyi sonuc veriyor mu?"
                },
                {
                    "step": 3,
                    "title": "Citation & Source Tracking",
                    "why": "Agent'in verdigi cevapın kaynagini gostermek guveni artirir. 'Bu bilgiyi nereden aldin?' sorusuna cevap verebilmeli.",
                    "instructions": "Her RAG cevabina:\n1. Kaynak dokuman adi ve bolum\n2. Confidence score\n3. Son guncelleme tarihi ekle\n4. Frontend'de citation goruntulemesi",
                    "checkpoint": "Agent cevaplarinda kaynak bilgisi gorunuyor mu?"
                }
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Chunk boyutu 200-500 token arasi optimal\n2. Chunk overlap %10-20 olmali — bilgi kaybi onlenir\n3. Metadata ZORUNLU: category, source, date — filtreleme icin kullanacaksin\n4. RAG pipeline'da retrieval kalitesini OLCMELISIN — rasgele sorularla test et",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nRAG'in en buyuk sorunu: retrieval kalitesi. Embedding model secimi cok onemli — OpenAI ada-002 genel amacli iyi ama domain-specific model daha iyi olabilir. Evaluation framework kur: precision@k, recall@k, MRR olc.\n\nKnowledge base guncel tutmak operasyonel zorluk. Stale docs = yanlis cevaplar = mutsuz musteriler. Auto-expiry mekanizmasi kur."
        },
        {
            "id": "p08-m4",
            "title": "Multi-turn Conversation & Memory Yonetimi",
            "overview": "Uzun konusmalarda context'i verimli yonet. Conversation summarization ve sliding window memory implement et.",
            "estimated_hours": 8,
            "concepts_covered": ["conversation memory", "summarization", "context window", "token management"],
            "steps": [
                {
                    "step": 1,
                    "title": "Sliding Window + Summary Memory",
                    "why": "LLM context window sinirli. 20+ mesajlik konusmada tum mesajlari gondermek hem yavas hem pahali.",
                    "instructions": "Memory stratejisi:\n1. Son 5 mesaji tam gonder (recent context)\n2. Onceki mesajlari ozetlerle (rolling summary)\n3. Onemli bilgileri ayri key-value store'da tut\n4. Agent gecislerinde summary otomatik guncelle",
                    "checkpoint": "20 mesajlik bir konusmada agent hala ilk mesajihatirliyor mu (summary uzerinden)?"
                },
                {
                    "step": 2,
                    "title": "Redis Session Store",
                    "why": "Conversation state Redis'te tutmak server restart ve horizontal scaling'e dayanikli yapar.",
                    "instructions": "Redis'e kaydet:\n- conversation_id: tum state\n- TTL: 24 saat (otomatik temizlik)\n- Agent gecislerinde state guncelle\n- Reconnect durumunda state'i Redis'ten yukle",
                    "checkpoint": "Server restart sonrasi konusma kaldigi yerden devam ediyor mu?"
                },
                {
                    "step": 3,
                    "title": "Context-Aware Agent Handoff",
                    "why": "Agent degistiginde kullanici 'tekrar anlatmak zorunda kalmamali'. Onceki agent'in ozeti yeni agent'a aktarilmali.",
                    "instructions": "Handoff protocol:\n1. Cikan agent: conversation summary olustur\n2. Transfer metadata: neden gecis yapildi, ne denendi\n3. Giren agent: summary'yi oku ve 'Anliyorum, [ozet]. Simdi [yeni yaklasiM]' de\n4. Kullaniciya seffaf gecis bildirimi",
                    "checkpoint": "FAQ -> Tech gecisinde Tech agent onceki konusmayi biliyor mu?"
                }
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Token sayma ZORUNLU — her LLM cagrisinda kac token kullandigini bil\n2. Summary prompt'u kisa tut — summary icin cok token harcama\n3. Redis TTL'ini kullanim pattern'ine gore ayarla — 24 saat cok olabilir\n4. Context window dolmadan ONCE summarize et — son anda yapmak riskli",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nMemory management LLM uygulamalarinin gizli karmasikligidir. Context window ne kadar buyuk olursa olsun, maliyet lineeer artar. Akilli summarization = maliyet optimizasyonu.\n\nProduction'da her conversation'in token maliyetini track et. Dashboard'da ortalama maliyet/konusma goster. Budget alert kur — bir konusma $5'i gecerse otomatik escalation yap."
        },
        {
            "id": "p08-m5",
            "title": "Human Handoff & Escalation Sistemi",
            "overview": "AI agent cozemediginde insana aktarma mekanizmasi. Tam context transferi ile sifirsiz gecis.",
            "estimated_hours": 10,
            "concepts_covered": ["human-in-the-loop", "escalation logic", "queue management", "priority routing"],
            "steps": [
                {
                    "step": 1,
                    "title": "Escalation Karar Mantigi",
                    "why": "Ne zaman insana aktarilacagi kritik bir karar. Cok erken = AI'in faydasiz olmasi. Cok gec = mutsuz musteri.",
                    "instructions": "Escalation triggers:\n1. Musteri acikca insan talep etti\n2. Sentiment score < 2/5 (kizgin musteri)\n3. Agent 3+ denemede cozemedi\n4. Confidence score surekli dusuk\n5. Hassas konu (guvenlik, odeme sorunlari)",
                    "checkpoint": "Tum escalation trigger'lari calisiyor mu? False positive orani kabul edilebilir mi?"
                },
                {
                    "step": 2,
                    "title": "Context Transfer & Queue",
                    "why": "Insan agent'a geciste tum bilgi aktarilmali. 'Tekrar anlatir misiniz?' demek kabul edilemez.",
                    "instructions": "Handoff package:\n1. Konusma ozeti (AI tarafindan olusturulmus)\n2. Musteri bilgileri\n3. Denenmis cozumler listesi\n4. Escalation nedeni\n5. Oncelik seviyesi (P1-P4)\n\nQueue sistemi:\n- Priority queue (P1 once)\n- Agent skill-based routing\n- Estimated wait time",
                    "checkpoint": "Insan agent handoff'u aldiginda tum context'i goruyor mu?"
                },
                {
                    "step": 3,
                    "title": "Real-time Agent Dashboard",
                    "why": "Insan agent'larin aktif konusmalari, kuyrugu ve agent performansini gormesi operasyonel verimlilik icin sart.",
                    "instructions": "Dashboard:\n1. Aktif konusmalar listesi (AI + insan)\n2. Kuyruk durumu ve bekleme sureleri\n3. Agent musaitlik durumu\n4. Quick actions: devral, ata, kapat",
                    "checkpoint": "Dashboard real-time gunceleniyor mu? Konusma devralma calisiyor mu?"
                }
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Escalation HER ZAMAN mumkun olmali — AI'i zorla kullandirma\n2. Context transfer'de PII (kisisel bilgi) filtreleme gerekebilir\n3. Kuyruk bosken bile tahmini bekleme suresi goster\n4. Insan agent AI ozetini duzenleyebilmeli — AI yanlis ozetlerse",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nHuman handoff'un kalitesi AI sisteminin basarisini belirler. 'AI bana yardimci olamadi' deneyimi, 'hemen bir insanla konustum' deneyiminden cok daha kotu. Escalation hizli ve sorunsuz olmali.\n\nMetrikler: escalation rate, resolution after escalation, customer satisfaction before/after handoff. Bu metrikleri izleyerek AI agent'lari surekli iyilestir."
        },
        {
            "id": "p08-m6",
            "title": "Analytics Dashboard & Production Deployment",
            "overview": "Agent performans metrikleri, konusma analitikleri ve production-ready deployment.",
            "estimated_hours": 10,
            "concepts_covered": ["analytics", "monitoring", "Docker", "CI/CD", "observability"],
            "steps": [
                {
                    "step": 1,
                    "title": "Agent Performance Metrics",
                    "why": "Olcemezsen iyilestiremezsin. Her agent'in ne kadar etkili oldugunu bilmek optimizasyon icin sart.",
                    "instructions": "Metrikler:\n1. Resolution rate (agent basina)\n2. Average response time\n3. Customer satisfaction score\n4. Escalation rate\n5. Token usage per conversation\n6. Intent classification accuracy",
                    "checkpoint": "Dashboard'da tum metrikler gorunuyor mu?"
                },
                {
                    "step": 2,
                    "title": "Conversation Analytics",
                    "why": "Pattern analizi ile en sik sorulan sorular, sik escalation edilen konular ve iyilestirme firsatlarini tespit et.",
                    "instructions": "Analitikler:\n1. En sik intent categorileri\n2. Ortalama konusma suresi (tur sayisi)\n3. Peak saatleri\n4. Unresolved conversation pattern'leri\n5. Haftalik/aylik trend grafikleri",
                    "checkpoint": "Son 7 gunun analitikleri dogru gosteriliyor mu?"
                },
                {
                    "step": 3,
                    "title": "WebSocket Integration",
                    "why": "Production chat deneyimi icin real-time iletisim sart. REST polling kabul edilemez.",
                    "instructions": "WebSocket:\n1. Node.js WS gateway\n2. Connection lifecycle (connect, auth, disconnect)\n3. Message format standardization\n4. Reconnection logic (client-side)\n5. Heartbeat/ping-pong",
                    "checkpoint": "Chat mesajlari aninda iletiyor mu? Baglanti kopunca reconnect calisiyor mu?"
                },
                {
                    "step": 4,
                    "title": "Docker & Production Hardening",
                    "why": "Tum servislerin container'da calismasi deployment tutarliligini ve olceklenebilirligini saglar.",
                    "instructions": "Production checklist:\n1. Multi-stage Dockerfile (her servis)\n2. docker-compose.prod.yml\n3. Environment variable management\n4. Health checks\n5. Logging (structured JSON)\n6. Rate limiting\n7. Error tracking (Sentry)",
                    "checkpoint": "docker-compose -f docker-compose.prod.yml up ile tum sistem hatasiz calisiyor mu?"
                }
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Her LLM cagrisini logla — maliyet takibi icin kritik\n2. WebSocket reconnection client'ta ZORUNLU — mobilde baglanti sik kopar\n3. Production'da her zaman structured logging kullan — JSON format\n4. Rate limiting hem API hem WebSocket icin ayri ayri kur",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nAI destek sistemlerinin ROI'si net olmali: AI ile resolve edilen konusma basina X TL tasarruf. Bu metrik yoneticiyi ikna eder.\n\nObservability stack: logs (ne oldu), metrics (ne kadar oldu), traces (neden oldu). Production AI sistemi icin ucune de ihtiyacin var. OpenTelemetry ile vendor-agnostic observability kur."
        }
    ],
    "interview_prep": {
        "questions": [
            "Multi-agent sisteminizde agent'lar arasi iletisimi nasil yonettiniz?",
            "LangGraph'i neden sectiniz? Alternatifleri degerlendirdiniz mi?",
            "Conversation memory yonetiminde ne yaklasim kullandiniz?",
            "Human handoff surecinde context kaybi yasanmamasi icin ne yaprtiniz?",
            "Agent routing'de accuracy'yi nasil olctunuz ve iyilestirdiniz?",
            "WebSocket baglantisi koptiginda ne oluyor?",
            "Token maliyetini nasil optimize ettiniz?",
            "Bu sistemi 10x trafik icin nasil olceklerdiniz?",
            "RAG pipeline'indan retrieval kalitesini nasil olcuyorsunuz?",
            "Production'da bir agent hatali cevap verdikdiginde ne olur?"
        ],
        "talking_points": [
            "LangGraph ile stateful workflow — neden state machine mantigi onemli",
            "Router agent'in klasifikasyon accuracy'si ve iyilestirme sureci",
            "Redis session management ile horizontal scaling hazirrligi",
            "Human-in-the-loop pattern — AI limitlerini kabul etmenin onemi",
            "Token maliyet optimizasyonu — summarization stratejisi",
            "Real-time WebSocket vs polling karsilastirmasi",
            "Analytics-driven agent iyilestirme dongusu"
        ]
    },
    "resources": [
        {"title": "LangGraph Documentation", "url": "https://python.langchain.com/docs/langgraph", "why": "Resmi LangGraph dokuamni — agent graph tasarimi icin temel kaynak"},
        {"title": "Building Multi-Agent Systems", "url": "https://blog.langchain.dev/langgraph-multi-agent-workflows/", "why": "LangChain blog — multi-agent pattern'leri ve best practices"},
        {"title": "WebSocket API (MDN)", "url": "https://developer.mozilla.org/en-US/docs/Web/API/WebSocket", "why": "WebSocket protokolunu anlamak icin MDN referansi"},
        {"title": "Redis Documentation", "url": "https://redis.io/docs/", "why": "Redis session management ve caching icin"},
        {"title": "Anthropic Prompt Engineering Guide", "url": "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering", "why": "Agent prompt'larini optimize etmek icin"}
    ]
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'projects', 'project-08.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(project, f, ensure_ascii=False, indent=2)
print(f"Written to {out_path}: {os.path.getsize(out_path)} bytes")
