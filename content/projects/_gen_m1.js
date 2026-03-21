const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, 'project-08.json');
const D = JSON.parse(fs.readFileSync(OUT, 'utf-8'));

D.milestones = [{
  id: "m1",
  title: "Agent Architecture & Proje Setup",
  estimated_days: 2,
  must_note: [
    "Agent = LLM + Prompt + Tools + Memory. Her agent bir 'uzman' gibidir, kendi bilgi alanı ve araçları vardır.",
    "LangGraph state machine'de her node bir işlem, her edge bir karar noktasıdır. Graph'ı çizdikten sonra kod yazmaya başla.",
    "StateGraph'ta TypedDict kullanmak, state shape'ini compile-time'da garanti altına alır — runtime hata riskini azaltır.",
    "Conditional edge = if/else yerine graph-based routing. Debugging'de hangi path'in seçildiğini görebilirsin."
  ],
  senior_learns: "Senior/CTO seviyesinde bir mühendis, agent mimarisini tasarlarken önce tüm agent'ların sorumluluk sınırlarını (boundary) çizer. Her agent'ın input/output contract'ını belirler. LangGraph graph'ını whiteboard'da tasarlar, edge case'leri (bilinmeyen intent, agent çökmesi, circular routing) önceden planlar. Kodu yazmadan önce state schema'yı finalize eder.",
  steps: [
    {
      title: "Proje Yapısını ve Dependency'leri Kur",
      why: "Temiz bir proje yapısı, multi-agent sistemlerde özellikle kritiktir çünkü her agent'ın kendi modülü, tool'ları ve prompt'ları olacak. Baştan doğru organize etmezsen, agent sayısı arttıkça kod karmaşası kaçınılmaz olur.",
      instructions: "Python 3.11+ ile yeni bir proje oluştur. Poetry veya pip ile dependency'leri yönet. Proje yapısını agents/, tools/, services/, models/, config/ klasörleri ile organize et. .env dosyasında OpenAI API key ve diğer config'leri sakla.",
      code_snippet: `# requirements.txt
langchain>=0.2.0
langgraph>=0.2.0
langchain-openai>=0.1.0
langchain-community>=0.2.0
chromadb>=0.5.0
fastapi>=0.110.0
uvicorn>=0.29.0
websockets>=12.0
redis>=5.0.0
asyncpg>=0.29.0
sqlalchemy>=2.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
httpx>=0.27.0

# Proje yapisi:
# ai-customer-support/
# ├── agents/
# │   ├── __init__.py
# │   ├── router_agent.py
# │   ├── faq_agent.py
# │   ├── billing_agent.py
# │   ├── tech_support_agent.py
# │   └── fallback_agent.py
# ├── tools/
# │   ├── __init__.py
# │   ├── kb_search.py
# │   ├── db_lookup.py
# │   └── order_status.py
# ├── graph/
# │   ├── __init__.py
# │   ├── state.py
# │   └── workflow.py
# ├── services/
# │   ├── __init__.py
# │   ├── memory_service.py
# │   ├── analytics_service.py
# │   └── sentiment_service.py
# ├── api/
# │   ├── __init__.py
# │   ├── routes.py
# │   └── websocket.py
# ├── config/
# │   ├── __init__.py
# │   └── settings.py
# ├── tests/
# ├── .env
# ├── docker-compose.yml
# └── main.py`,
      deep_dive: "LangChain modüler bir framework'tür — langchain-core temel abstraction'ları, langchain-openai OpenAI entegrasyonunu, langchain-community topluluk tool'larını sağlar. LangGraph ise LangChain üzerine inşa edilmiş bir orchestration katmanıdır — agent'ları graph node'ları olarak tanımlar ve aralarındaki geçişleri yönetir. Bu separation of concerns, her modülü bağımsız test etmeni sağlar.",
      checkpoint: "python -c \"import langchain, langgraph; print('OK')\" komutu hatasız çalışmalı. Proje klasör yapısı oluşturulmuş olmalı."
    },
    {
      title: "LangGraph State Schema Tanımla",
      why: "State, tüm agent'lar arasında paylaşılan 'ortak hafıza'dır. Hangi agent'ın aktif olduğu, müşteri mesajı, routing kararı, sentiment skoru — hepsi state'te tutulur. Yanlış state tasarımı, agent'lar arası veri kaybına ve hatalı geçişlere yol açar.",
      instructions: "TypedDict kullanarak AgentState tanımla. messages (konuşma geçmişi), current_agent (aktif agent), customer_intent, sentiment_score, needs_human, session_id alanlarını ekle. Reducer fonksiyonları ile state güncelleme mantığını belirle.",
      code_snippet: `# graph/state.py
from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class AgentState(TypedDict):
    """Multi-agent sistem icin paylasilan state."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_agent: str
    customer_intent: Optional[str]
    confidence_score: float
    sentiment_score: float  # -1.0 ile 1.0 arasi
    sentiment_trend: str    # 'improving', 'stable', 'declining'
    needs_human: bool
    escalation_reason: Optional[str]
    session_id: str
    customer_id: Optional[str]
    turn_count: int
    tool_results: Optional[dict]
    routing_history: list[str]

def create_initial_state(session_id: str) -> AgentState:
    return AgentState(
        messages=[], current_agent="router",
        customer_intent=None, confidence_score=0.0,
        sentiment_score=0.5, sentiment_trend="stable",
        needs_human=False, escalation_reason=None,
        session_id=session_id, customer_id=None,
        turn_count=0, tool_results=None, routing_history=[]
    )`,
      deep_dive: "Annotated[Sequence[BaseMessage], add_messages] — bu LangGraph'ın reducer pattern'idir. Normal TypedDict'te bir field'ı güncellersen eski değerin üzerine yazılır. Ama add_messages reducer, yeni mesajları mevcut listeye ekler (append). Bu, her agent'ın kendi mesajını ekleyebilmesini sağlar. Reducer pattern, Redux'tan esinlenmiştir — state mutation'ı kontrollü ve öngörülebilir hale getirir.",
      checkpoint: "AgentState TypedDict hatasız import edilebilmeli. create_initial_state() çağrıldığında tüm alanlar default değerleriyle dönmeli."
    },
    {
      title: "Temel LangGraph Workflow Graph'ı Oluştur",
      why: "Graph, agent'lar arasındaki akışı tanımlar — hangi agent'tan sonra hangisi çalışacak, hangi koşulda hangi yola gidilecek. Önce basit bir graph ile başlayıp, milestone'lar ilerledikçe karmaşıklaştıracaksın.",
      instructions: "StateGraph kullanarak temel workflow'u oluştur: router node -> conditional edge -> specialist agents -> END. Placeholder agent'lar kullan. Graph'ı compile et ve test yap.",
      code_snippet: `# graph/workflow.py
from langgraph.graph import StateGraph, END
from graph.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage

def router_node(state: AgentState) -> dict:
    last_message = state["messages"][-1].content.lower()
    if any(w in last_message for w in ["fatura", "odeme", "ucret", "para"]):
        intent = "billing"
    elif any(w in last_message for w in ["hata", "calismiyor", "bug", "sorun"]):
        intent = "tech_support"
    else:
        intent = "faq"
    return {
        "current_agent": intent, "customer_intent": intent,
        "confidence_score": 0.8,
        "routing_history": state.get("routing_history", []) + [intent],
        "turn_count": state.get("turn_count", 0) + 1
    }

def faq_node(state): return {"messages": [AIMessage(content="FAQ Agent: Sorunuzu inceliyorum...")], "current_agent": "faq"}
def billing_node(state): return {"messages": [AIMessage(content="Billing Agent: Fatura bilginizi kontrol ediyorum...")], "current_agent": "billing"}
def tech_support_node(state): return {"messages": [AIMessage(content="Tech Support Agent: Sorununuzu analiz ediyorum...")], "current_agent": "tech_support"}

def route_to_agent(state):
    if state.get("needs_human"): return "human_handoff"
    return state["current_agent"]

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_node)
    workflow.add_node("faq", faq_node)
    workflow.add_node("billing", billing_node)
    workflow.add_node("tech_support", tech_support_node)
    workflow.set_entry_point("router")
    workflow.add_conditional_edges("router", route_to_agent, {"faq": "faq", "billing": "billing", "tech_support": "tech_support"})
    workflow.add_edge("faq", END)
    workflow.add_edge("billing", END)
    workflow.add_edge("tech_support", END)
    return workflow.compile()

if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({
        "messages": [HumanMessage(content="Faturami gormek istiyorum")],
        "current_agent": "router", "session_id": "test-001",
        "sentiment_score": 0.5, "sentiment_trend": "stable",
        "needs_human": False, "turn_count": 0, "routing_history": []
    })
    print(f"Routed to: {result['current_agent']}")`,
      deep_dive: "StateGraph compile edildiğinde bir CompiledGraph nesnesi oluşur. Bu nesne invoke() (senkron), ainvoke() (asenkron) ve stream() (streaming) metodlarını destekler. add_conditional_edges fonksiyonunun üçüncü parametresi bir mapping dict'idir — routing fonksiyonunun döndürdüğü string'i graph node ismiyle eşleştirir.",
      checkpoint: "python graph/workflow.py çalıştırıldığında 'Faturamı görmek istiyorum' mesajı billing agent'a yönlendirilmeli."
    },
    {
      title: "Config ve Environment Yönetimi",
      why: "API key'ler, model seçimi, temperature gibi parametreler hardcode edilmemeli. Environment-based config, development/staging/production ortamları arasında sorunsuz geçiş sağlar.",
      instructions: "Pydantic Settings ile config sınıfı oluştur. OpenAI API key, model name, temperature, Redis URL, PostgreSQL URL gibi tüm konfigürasyonları .env'den oku. .env.example dosyası oluştur.",
      code_snippet: `# config/settings.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.3
    redis_url: str = "redis://localhost:6379/0"
    session_ttl_seconds: int = 3600
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_support"
    chroma_persist_dir: str = "./data/chroma"
    embedding_model: str = "text-embedding-3-small"
    max_turns_before_escalation: int = 10
    sentiment_threshold: float = -0.3
    confidence_threshold: float = 0.6
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000"]
    rate_limit_per_minute: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()`,
      deep_dive: "Pydantic Settings, environment variable'ları otomatik olarak Python type'larına dönüştürür ve validation yapar. lru_cache decorator'ü, get_settings() sonucunu cache'ler — Singleton pattern'in fonksiyonel versiyonudur. Temperature 0.3: müşteri desteğinde tutarlı yanıtlar istiyoruz.",
      checkpoint: "Settings sınıfı .env dosyasından değerleri okuyabilmeli. Eksik OPENAI_API_KEY durumunda ValidationError fırlatmalı."
    }
  ]
}];

fs.writeFileSync(OUT, JSON.stringify(D, null, 2), 'utf-8');
console.log('M1 done:', fs.statSync(OUT).size);
