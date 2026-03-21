import json
import os

OUT = "C:/Users/tahaa/Desktop/egitimü/content/projects/project-08.json"

with open(OUT, "r", encoding="utf-8") as f:
    data = json.load(f)

# ============================================================
# MILESTONE 1: Agent Architecture & Proje Setup
# ============================================================
m1 = {
  "id": "m1",
  "title": "Agent Architecture & Proje Setup",
  "estimated_days": 2,
  "must_note": [
    "Agent = LLM + Prompt + Tools + Memory. Her agent bir 'uzman' gibidir, kendi bilgi alanı ve araçları vardır.",
    "LangGraph state machine'de her node bir işlem, her edge bir karar noktasıdır. Graph'ı çizdikten sonra kod yazmaya başla.",
    "StateGraph'ta TypedDict kullanmak, state shape'ini compile-time'da garanti altına alır — runtime hata riskini azaltır.",
    "Conditional edge = if/else yerine graph-based routing. Debugging'de hangi path'in seçildiğini görebilirsin."
  ],
  "senior_learns": "Senior/CTO seviyesinde bir mühendis, agent mimarisini tasarlarken önce tüm agent'ların sorumluluk sınırlarını (boundary) çizer. Her agent'ın input/output contract'ını belirler. LangGraph graph'ını whiteboard'da tasarlar, edge case'leri (bilinmeyen intent, agent çökmesi, circular routing) önceden planlar. Kodu yazmadan önce state schema'yı finalize eder.",
  "steps": [
    {
      "title": "Proje Yapısını ve Dependency'leri Kur",
      "why": "Temiz bir proje yapısı, multi-agent sistemlerde özellikle kritiktir çünkü her agent'ın kendi modülü, tool'ları ve prompt'ları olacak. Baştan doğru organize etmezsen, agent sayısı arttıkça kod karmaşası kaçınılmaz olur.",
      "instructions": "Python 3.11+ ile yeni bir proje oluştur. Poetry veya pip ile dependency'leri yönet. Proje yapısını agents/, tools/, services/, models/, config/ klasörleri ile organize et. .env dosyasında OpenAI API key ve diğer config'leri sakla.",
      "code_snippet": "# requirements.txt\nlangchain>=0.2.0\nlanggraph>=0.2.0\nlangchain-openai>=0.1.0\nlangchain-community>=0.2.0\nchromadb>=0.5.0\nfastapi>=0.110.0\nuvicorn>=0.29.0\nwebsockets>=12.0\nredis>=5.0.0\nasyncpg>=0.29.0\nsqlalchemy>=2.0.0\npython-dotenv>=1.0.0\npydantic>=2.0.0\nhttpx>=0.27.0\n\n# Proje yapisi:\n# ai-customer-support/\n# +-- agents/\n# |   +-- __init__.py\n# |   +-- router_agent.py\n# |   +-- faq_agent.py\n# |   +-- billing_agent.py\n# |   +-- tech_support_agent.py\n# |   +-- fallback_agent.py\n# +-- tools/\n# |   +-- __init__.py\n# |   +-- kb_search.py\n# |   +-- db_lookup.py\n# |   +-- order_status.py\n# +-- graph/\n# |   +-- __init__.py\n# |   +-- state.py\n# |   +-- workflow.py\n# +-- services/\n# |   +-- __init__.py\n# |   +-- memory_service.py\n# |   +-- analytics_service.py\n# |   +-- sentiment_service.py\n# +-- api/\n# |   +-- __init__.py\n# |   +-- routes.py\n# |   +-- websocket.py\n# +-- config/\n# |   +-- __init__.py\n# |   +-- settings.py\n# +-- tests/\n# +-- .env\n# +-- docker-compose.yml\n# +-- main.py",
      "deep_dive": "LangChain moduler bir framework'tur -- langchain-core temel abstraction'lari (LLM, prompt, chain), langchain-openai OpenAI entegrasyonunu, langchain-community topluluk tool'larini saglar. LangGraph ise LangChain uzerine insa edilmis bir orchestration katmanidir -- agent'lari graph node'lari olarak tanimlar ve aralarindaki gecisleri yonetir.",
      "checkpoint": "python -c \"import langchain, langgraph; print('OK')\" komutu hatasiz calismali. Proje klasor yapisi olusturulmus olmali."
    },
    {
      "title": "LangGraph State Schema Tanımla",
      "why": "State, tüm agent'lar arasında paylaşılan 'ortak hafıza'dır. Hangi agent'ın aktif olduğu, müşteri mesajı, routing kararı, sentiment skoru — hepsi state'te tutulur. Yanlış state tasarımı, agent'lar arası veri kaybına ve hatalı geçişlere yol açar.",
      "instructions": "TypedDict kullanarak AgentState tanımla. messages, current_agent, customer_intent, sentiment_score, needs_human, session_id, metadata alanlarını ekle. Reducer fonksiyonları ile state güncelleme mantığını belirle.",
      "code_snippet": "# graph/state.py\nfrom typing import TypedDict, Annotated, Sequence, Optional\nfrom langchain_core.messages import BaseMessage\nfrom langgraph.graph import add_messages\n\nclass AgentState(TypedDict):\n    \"\"\"Multi-agent sistem icin paylasilan state.\"\"\"\n    # Konusma gecmisi - add_messages reducer ile otomatik merge\n    messages: Annotated[Sequence[BaseMessage], add_messages]\n    \n    # Routing bilgileri\n    current_agent: str  # 'router', 'faq', 'billing', 'tech_support', 'fallback'\n    customer_intent: Optional[str]\n    confidence_score: float  # Router'in intent confidence'i (0-1)\n    \n    # Sentiment tracking\n    sentiment_score: float  # -1.0 (cok olumsuz) ile 1.0 (cok olumlu)\n    sentiment_trend: str  # 'improving', 'stable', 'declining'\n    \n    # Human handoff\n    needs_human: bool\n    escalation_reason: Optional[str]\n    \n    # Session metadata\n    session_id: str\n    customer_id: Optional[str]\n    turn_count: int\n    \n    # Tool results\n    tool_results: Optional[dict]\n    \n    # Routing gecmisi (debugging icin)\n    routing_history: list[str]\n\n\ndef create_initial_state(session_id: str) -> AgentState:\n    \"\"\"Yeni bir konusma icin baslangic state'i.\"\"\"\n    return AgentState(\n        messages=[],\n        current_agent=\"router\",\n        customer_intent=None,\n        confidence_score=0.0,\n        sentiment_score=0.5,\n        sentiment_trend=\"stable\",\n        needs_human=False,\n        escalation_reason=None,\n        session_id=session_id,\n        customer_id=None,\n        turn_count=0,\n        tool_results=None,\n        routing_history=[]\n    )",
      "deep_dive": "Annotated[Sequence[BaseMessage], add_messages] — bu LangGraph'ın reducer pattern'idir. Normal TypedDict'te bir field'ı güncellersen eski değerin üzerine yazılır. Ama add_messages reducer, yeni mesajları mevcut listeye ekler (append). Bu, her agent'ın kendi mesajını ekleyebilmesini sağlar. Reducer pattern, Redux'tan esinlenmiştir — state mutation'ı kontrollü ve öngörülebilir hale getirir.",
      "checkpoint": "AgentState TypedDict hatasız import edilebilmeli. create_initial_state() çağrıldığında tüm alanlar default değerleriyle dönmeli."
    },
    {
      "title": "Temel LangGraph Workflow Graph'ı Oluştur",
      "why": "Graph, agent'lar arasındaki akışı tanımlar — hangi agent'tan sonra hangisi çalışacak, hangi koşulda hangi yola gidilecek. Önce basit bir graph ile başlayıp, milestone'lar ilerledikçe karmaşıklaştıracaksın.",
      "instructions": "StateGraph kullanarak temel workflow'u oluştur: router node -> conditional edge -> specialist agents -> END. Başlangıçta placeholder agent'lar kullan. Graph'ı compile et ve basit bir mesajla end-to-end test yap.",
      "code_snippet": "# graph/workflow.py\nfrom langgraph.graph import StateGraph, END\nfrom graph.state import AgentState\nfrom langchain_core.messages import HumanMessage, AIMessage\n\ndef router_node(state: AgentState) -> dict:\n    \"\"\"Gelen mesaji analiz edip hangi agent'a yonlendirecegine karar verir.\"\"\"\n    last_message = state[\"messages\"][-1].content.lower()\n    \n    if any(word in last_message for word in [\"fatura\", \"odeme\", \"ucret\", \"para\"]):\n        intent = \"billing\"\n    elif any(word in last_message for word in [\"hata\", \"calismiyor\", \"bug\", \"sorun\"]):\n        intent = \"tech_support\"\n    elif any(word in last_message for word in [\"nasil\", \"nedir\", \"ne zaman\"]):\n        intent = \"faq\"\n    else:\n        intent = \"faq\"\n    \n    return {\n        \"current_agent\": intent,\n        \"customer_intent\": intent,\n        \"confidence_score\": 0.8,\n        \"routing_history\": state.get(\"routing_history\", []) + [intent],\n        \"turn_count\": state.get(\"turn_count\", 0) + 1\n    }\n\ndef faq_node(state: AgentState) -> dict:\n    return {\n        \"messages\": [AIMessage(content=\"FAQ Agent: Sorunuzu inceliyorum...\")],\n        \"current_agent\": \"faq\"\n    }\n\ndef billing_node(state: AgentState) -> dict:\n    return {\n        \"messages\": [AIMessage(content=\"Billing Agent: Fatura bilginizi kontrol ediyorum...\")],\n        \"current_agent\": \"billing\"\n    }\n\ndef tech_support_node(state: AgentState) -> dict:\n    return {\n        \"messages\": [AIMessage(content=\"Tech Support Agent: Sorununuzu analiz ediyorum...\")],\n        \"current_agent\": \"tech_support\"\n    }\n\ndef route_to_agent(state: AgentState) -> str:\n    if state.get(\"needs_human\"):\n        return \"human_handoff\"\n    return state[\"current_agent\"]\n\ndef build_graph() -> StateGraph:\n    workflow = StateGraph(AgentState)\n    workflow.add_node(\"router\", router_node)\n    workflow.add_node(\"faq\", faq_node)\n    workflow.add_node(\"billing\", billing_node)\n    workflow.add_node(\"tech_support\", tech_support_node)\n    \n    workflow.set_entry_point(\"router\")\n    workflow.add_conditional_edges(\n        \"router\", route_to_agent,\n        {\"faq\": \"faq\", \"billing\": \"billing\", \"tech_support\": \"tech_support\"}\n    )\n    workflow.add_edge(\"faq\", END)\n    workflow.add_edge(\"billing\", END)\n    workflow.add_edge(\"tech_support\", END)\n    \n    return workflow.compile()\n\nif __name__ == \"__main__\":\n    app = build_graph()\n    result = app.invoke({\n        \"messages\": [HumanMessage(content=\"Faturami gormek istiyorum\")],\n        \"current_agent\": \"router\",\n        \"session_id\": \"test-001\",\n        \"sentiment_score\": 0.5,\n        \"sentiment_trend\": \"stable\",\n        \"needs_human\": False,\n        \"turn_count\": 0,\n        \"routing_history\": []\n    })\n    print(f\"Routed to: {result['current_agent']}\")\n    print(f\"Response: {result['messages'][-1].content}\")",
      "deep_dive": "StateGraph compile edildiğinde bir CompiledGraph nesnesi oluşur. Bu nesne invoke() (senkron), ainvoke() (asenkron) ve stream() (streaming) metodlarını destekler. add_conditional_edges fonksiyonunun üçüncü parametresi bir mapping dict'idir — routing fonksiyonunun döndürdüğü string'i graph node ismiyle eşleştirir.",
      "checkpoint": "python graph/workflow.py çalıştırıldığında 'Faturamı görmek istiyorum' mesajı billing agent'a yönlendirilmeli."
    },
    {
      "title": "Config ve Environment Yönetimi",
      "why": "API key'ler, model seçimi, temperature gibi parametreler hardcode edilmemeli. Environment-based config, development/staging/production ortamları arasında sorunsuz geçiş sağlar.",
      "instructions": "Pydantic Settings ile config sınıfı oluştur. OpenAI API key, model name, temperature, Redis URL, PostgreSQL URL gibi tüm konfigürasyonları .env'den oku. .env.example dosyası oluştur.",
      "code_snippet": "# config/settings.py\nfrom pydantic_settings import BaseSettings\nfrom functools import lru_cache\n\nclass Settings(BaseSettings):\n    openai_api_key: str\n    openai_model: str = \"gpt-4o-mini\"\n    openai_temperature: float = 0.3\n    redis_url: str = \"redis://localhost:6379/0\"\n    session_ttl_seconds: int = 3600\n    database_url: str = \"postgresql+asyncpg://postgres:postgres@localhost:5432/ai_support\"\n    chroma_persist_dir: str = \"./data/chroma\"\n    embedding_model: str = \"text-embedding-3-small\"\n    max_turns_before_escalation: int = 10\n    sentiment_threshold: float = -0.3\n    confidence_threshold: float = 0.6\n    api_host: str = \"0.0.0.0\"\n    api_port: int = 8000\n    cors_origins: list[str] = [\"http://localhost:3000\"]\n    rate_limit_per_minute: int = 30\n    \n    class Config:\n        env_file = \".env\"\n        env_file_encoding = \"utf-8\"\n\n@lru_cache()\ndef get_settings() -> Settings:\n    return Settings()",
      "deep_dive": "Pydantic Settings, environment variable'ları otomatik olarak Python type'larına dönüştürür ve validation yapar. lru_cache decorator'ü, get_settings() fonksiyonunun sonucunu cache'ler — Singleton pattern'in fonksiyonel versiyonudur. Temperature 0.3: müşteri desteğinde tutarlı ve öngörülebilir yanıtlar istiyoruz.",
      "checkpoint": "Settings sınıfı .env dosyasından değerleri okuyabilmeli. Eksik OPENAI_API_KEY durumunda ValidationError fırlatmalı."
    }
  ]
}

data["milestones"] = [m1]

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("M1 done, size:", os.path.getsize(OUT))
