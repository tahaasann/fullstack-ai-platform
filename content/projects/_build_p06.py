import json

data = {
  "id": "project-06",
  "title": "AI Content Platform — LLM Entegrasyonu & Fine-tuning",
  "difficulty": "advanced",
  "estimated_days": 14,
  "tech_stack": ["Python", "FastAPI", "TypeScript", "Next.js", "OpenAI API", "Anthropic API", "Google Gemini API", "Hugging Face Transformers", "PEFT/LoRA", "PostgreSQL", "Redis", "Docker", "LangChain", "Pydantic"],
  "target_roles": ["AI Engineer", "LLM Engineer"],
  "brief": "Bu projede, birden fazla LLM provider'ı (OpenAI, Anthropic, Gemini) entegre eden, prompt mühendisliği yapan ve custom model fine-tune eden profesyonel bir AI content platformu oluşturacaksın. Blog yazıları, sosyal medya içerikleri ve email'ler otomatik üretecek, kalite değerlendirmesi yapacak ve maliyet optimizasyonu uygulayacaksın. Bu proje seni gerçek bir LLM Engineer yapacak.",
  "architecture": {
    "overview": "Provider Abstraction Layer üzerinden birden fazla LLM'e bağlanan, prompt versioning ile içerik üreten, fine-tuning pipeline'ı ile özelleştirilmiş modeller eğiten ve evaluation framework ile kalite ölçen katmanlı bir mimari. FastAPI backend, Next.js frontend, PostgreSQL veri tabanı, Redis cache ve rate limiting.",
    "diagram": "┌─────────────────────────────────────────────────────────────────┐\n│                        Next.js Frontend                         │\n│              (Content Dashboard, Prompt Editor, Analytics)       │\n├─────────────────────────────────────────────────────────────────┤\n│                        FastAPI Backend                           │\n│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐     │\n│  │ Content API   │  │  Prompt API  │  │ Fine-tune API      │     │\n│  └──────┬───────┘  └──────┬───────┘  └────────┬───────────┘     │\n│         │                 │                    │                 │\n│  ┌──────┴─────────────────┴────────────────────┴───────────┐     │\n│  │              Provider Abstraction Layer                  │     │\n│  │   ┌────────┐  ┌─────────┐  ┌────────────┐               │     │\n│  │   │ OpenAI │  │Anthropic│  │Google Gemini│               │     │\n│  │   └────────┘  └─────────┘  └────────────┘               │     │\n│  └─────────────────────────────────────────────────────────┘     │\n│         │                                                       │\n│  ┌──────┴──────────────────────────────────────────────────┐     │\n│  │           Evaluation & Quality Layer                     │     │\n│  │   AI-as-Judge │ BLEU/ROUGE │ Human Feedback │ A/B Test   │     │\n│  └─────────────────────────────────────────────────────────┘     │\n│         │                                                       │\n│  ┌──────┴──────────────────────────────────────────────────┐     │\n│  │  PostgreSQL (prompts, content, evals) │ Redis (cache)    │     │\n│  └─────────────────────────────────────────────────────────┘     │\n└─────────────────────────────────────────────────────────────────┘",
    "decisions": [
      {
        "decision": "Neden Provider Abstraction Layer?",
        "reasoning": "Her LLM provider farklı API formatı, pricing modeli ve capability'ye sahip. Abstraction layer ile provider değişikliği tek satırda yapılır, fallback mekanizması otomatik çalışır ve maliyet karşılaştırması kolaylaşır. Strategy Pattern kullanarak yeni provider eklemek mevcut kodu bozmaz (Open-Closed Principle).",
        "alternatives": "LangChain doğrudan kullanımı, LiteLLM, her provider için ayrı servis",
        "when_to_choose_alternative": "LangChain: Hızlı prototipleme ve chain kurulumu gerekiyorsa. LiteLLM: Sadece API uyumluluğu yeterliyse. Ayrı servisler: Her provider farklı takımlar tarafından yönetiliyorsa."
      },
      {
        "decision": "Neden Prompt Versioning?",
        "reasoning": "Production'da prompt değişiklikleri output kalitesini dramatik şekilde etkiler. Git benzeri versioning ile her prompt değişikliği izlenir, A/B test yapılabilir ve kötü bir değişiklik anında geri alınabilir. Bu, MLOps'un temel prensibidir — reproducibility.",
        "alternatives": "Git ile dosya bazlı yönetim, Prompt management SaaS (PromptLayer, Humanloop), Hardcoded prompts",
        "when_to_choose_alternative": "Git: Küçük ekiplerde basit yönetim. SaaS: Enterprise düzeyinde collaboration gerekiyorsa. Hardcoded: MVP aşamasında hız öncelikliyse."
      },
      {
        "decision": "Neden LoRA Fine-tuning?",
        "reasoning": "Full fine-tuning milyarlarca parametre günceller — çok pahalı ve çok yavaş. LoRA, modelin sadece küçük bir bölümünü günceller (%1-2 parametre), böylece consumer GPU'da bile fine-tuning mümkün olur. Adapter'lar birleştirilebilir ve base model korunur.",
        "alternatives": "Full fine-tuning, QLoRA, Prompt tuning, OpenAI fine-tuning API",
        "when_to_choose_alternative": "Full fine-tuning: Sınırsız GPU kaynağı varsa. QLoRA: Daha da az GPU belleği gerekiyorsa. OpenAI API: Kendi altyapını kurmak istemiyorsan."
      },
      {
        "decision": "Neden AI-as-Judge Evaluation?",
        "reasoning": "İnsan değerlendirmesi yavaş ve pahalı. Güçlü bir LLM (GPT-4, Claude) ile üretilen içeriği otomatik değerlendirmek, hızlı iterasyon sağlar. BLEU/ROUGE gibi metrikler semantik kaliteyi yakalayamaz, ama AI judge bağlam, ton ve doğruluk değerlendirebilir.",
        "alternatives": "Sadece insan değerlendirmesi, otomatik metrikler (BLEU/ROUGE), kullanıcı feedback'i",
        "when_to_choose_alternative": "İnsan değerlendirmesi: Yüksek riskli içeriklerde (tıp, hukuk). BLEU/ROUGE: Çeviri ve özetleme gibi referans tabanlı görevlerde. Kullanıcı feedback'i: Production'da gerçek kullanıcı memnuniyeti ölçümü için."
      }
    ]
  },
  "what_you_learn": {
    "technical": [
      "OpenAI, Anthropic ve Google Gemini API entegrasyonu",
      "Provider abstraction pattern ile çoklu LLM yönetimi",
      "Prompt engineering: system prompts, few-shot, chain-of-thought",
      "Prompt versioning ve A/B testing altyapısı",
      "LoRA/PEFT ile model fine-tuning (Hugging Face Transformers)",
      "Dataset hazırlama ve veri temizleme pipeline'ı",
      "BLEU, ROUGE ve custom metrikler ile evaluation",
      "AI-as-Judge pattern ile otomatik kalite değerlendirmesi",
      "Token kullanımı izleme ve maliyet optimizasyonu",
      "Streaming response handling (SSE)",
      "Redis ile LLM response caching",
      "Rate limiting ve API quota yönetimi"
    ],
    "architectural": [
      "Strategy Pattern ile provider abstraction",
      "Pipeline pattern ile içerik üretim akışı",
      "Event-driven evaluation pipeline",
      "Repository pattern ile prompt yönetimi",
      "Adapter pattern ile farklı model formatları",
      "Circuit breaker pattern ile API dayanıklılığı"
    ],
    "ai_specific": [
      "LLM API'lerinin iç çalışma mantığı (tokenization, temperature, top-p)",
      "Fine-tuning vs prompt engineering karar mekanizması",
      "Model evaluation ve benchmark oluşturma",
      "Hallucination detection temelleri",
      "Cost-per-token analizi ve bütçe planlama",
      "Responsible AI: bias tespiti ve güvenlik filtreleri"
    ],
    "soft_skills": [
      "AI ürün tasarımı ve kullanıcı deneyimi",
      "LLM maliyet analizi ve raporlama",
      "Teknik blog yazımı: AI çözümlerini anlatma",
      "Prompt iteration süreci ve dokümantasyon",
      "Model performansı için metrik seçimi ve yorumlama"
    ]
  },
  "requirements": {
    "functional": [
      "Çoklu LLM provider desteği: OpenAI (GPT-4), Anthropic (Claude), Google (Gemini)",
      "Provider fallback: Bir provider başarısız olursa otomatik diğerine geçiş",
      "İçerik türleri: Blog yazısı, sosyal medya postu, email, ürün açıklaması",
      "Ton kontrolü: Profesyonel, samimi, akademik, pazarlama odaklı",
      "Prompt versioning: Her prompt değişikliği kaydedilir, geri alınabilir",
      "Few-shot learning: Örnek içerikler ile kalite artırma",
      "Fine-tuning pipeline: Dataset yükleme, eğitim, değerlendirme",
      "AI-as-Judge: Üretilen içeriği otomatik puanlama",
      "A/B testing: Farklı prompt versiyonlarını karşılaştırma",
      "İçerik geçmişi: Tüm üretilen içerikler saklanır ve aranabilir",
      "Kullanıcı feedback'i: İçerik beğeni/beğenmeme ve düzenleme takibi"
    ],
    "non_functional": [
      "Streaming yanıt: SSE ile token-by-token gösterim (UX)",
      "Response caching: Aynı prompt için Redis cache (maliyet tasarrufu)",
      "Rate limiting: Provider API limitlerini aşmama (429 koruması)",
      "Latency < 2s TTFT (Time to First Token) — cache hit durumunda < 100ms",
      "Maliyet dashboard'u: Provider bazında token kullanımı ve harcama",
      "API key rotation: Güvenli key yönetimi",
      "Docker Compose ile tüm servislerin tek komutla başlatılması",
      "Minimum %80 test coverage (unit + integration)"
    ],
    "ai_requirements": [
      "Model karşılaştırma: Aynı prompt'u farklı modellerde çalıştırıp sonuçları kıyaslama",
      "Token optimizasyonu: Gereksiz token kullanımını minimize etme",
      "Prompt injection koruması: Kullanıcı girdilerini sanitize etme",
      "Hallucination check: Üretilen içerikte tutarsızlık tespiti",
      "Fine-tuned model evaluation: Base model vs fine-tuned model karşılaştırması",
      "Responsible AI: İçerik güvenlik filtreleri ve bias kontrolü"
    ]
  },
  "evaluation_criteria": [
    "Provider abstraction layer doğru çalışıyor mu — yeni provider eklemek mevcut kodu bozmuyor mu?",
    "Fallback mekanizması güvenilir mi — bir provider çökünce diğerine geçiş süresi kabul edilebilir mi?",
    "Prompt versioning sistemi çalışıyor mu — eski versiyona geri dönülebiliyor mu?",
    "İçerik kalitesi tutarlı mı — farklı ton ayarları doğru yansıyor mu?",
    "Fine-tuning pipeline uçtan uca çalışıyor mu — dataset'ten trained model'e kadar?",
    "Evaluation metrikleri anlamlı mı — AI-as-Judge puanları insan değerlendirmesiyle tutarlı mı?",
    "Maliyet tracking doğru mu — her API çağrısının maliyeti hesaplanıyor mu?",
    "Streaming response düzgün çalışıyor mu — kullanıcı deneyimi akıcı mı?",
    "Cache mekanizması etkili mi — tekrarlanan istekler için maliyet düşüyor mu?",
    "Kod kalitesi ve test coverage yeterli mi — edge case'ler kapsanıyor mu?"
  ],
  "milestones": []
}

# Will be filled by subsequent scripts
with open("C:/Users/tahaa/Desktop/egitimü/content/projects/project-06.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Base written OK")
