"""Generate project-09.json: ML Pipeline & Model Serving Platform"""
import json, os

project = {
    "id": "project-09",
    "title": "ML Pipeline & Model Serving Platformu",
    "difficulty": "Uzman",
    "estimated_days": 18,
    "tech_stack": ["FastAPI", "React", "TypeScript", "PostgreSQL", "MLflow", "Docker", "scikit-learn", "Redis", "Celery"],
    "target_roles": ["AI/ML Engineer", "MLOps Engineer", "Data Engineer"],
    "brief": "Bu projede, veri toplama asamasindan model deployment'a kadar end-to-end bir ML pipeline platformu insa edeceksin. Gercek dunyada Amazon SageMaker, Google Vertex AI veya Databricks'in kucuk ama fonksiyonel bir versiyonunu dusun.\n\nPlatform su asamalari kapsar: veri ingestion, feature engineering, model training, experiment tracking (MLflow), model registry, A/B testing, real-time inference API, model monitoring ve drift detection. Her asama bagimsiz calisabilir ama birlikte orkestre edilebilir.\n\nBu proje MLOps'un temellerini ogretir — sadece model egitmek degil, modeli production'da guvenle calistirmak, monitor etmek ve gerektiginde otomatik olarak yeniden egitmek. Mulakatlarda 'ML modeli nasil production'a alirsiniz?' sorusuna pratik deneyimle cevap vereceksin.",
    "architecture": {
        "overview": "Platform, mikro-servis benzeri bir mimaride tasarlanmis. FastAPI ana API gateway, Celery ile asenkron pipeline orchestration, MLflow ile experiment tracking ve model registry, Redis ile job queue management, PostgreSQL ile metadata storage saglaniyor.",
        "diagram": """
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   React UI   │────►│  FastAPI      │────►│  PostgreSQL  │
│  Dashboard   │     │  API Gateway  │     │  (Metadata)  │
└──────────────┘     └──────┬───────┘     └──────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       ┌──────▼──────┐ ┌───▼────┐ ┌─────▼──────┐
       │   Celery    │ │MLflow  │ │   Redis    │
       │  Workers    │ │Server  │ │  (Queue)   │
       │             │ │        │ │            │
       │ - Training  │ │ - Exp  │ └────────────┘
       │ - Feature   │ │   Track│
       │ - Eval      │ │ - Model│
       └─────────────┘ │   Reg  │
                       └────────┘
        """,
        "decisions": [
            {
                "decision": "Neden MLflow?",
                "reasoning": "MLflow acik kaynak, vendor-agnostic ve kapsamli: experiment tracking, model registry, model serving hep bir arada. Buyuk cloud vendor'lara bagimli kalmadan MLOps yapabilirsin.",
                "alternatives": "Weights & Biases, Neptune.ai, ClearML, kendi cozumun",
                "when_to_choose_alternative": "W&B gorsel dashboard'u cok iyi — takim collaboration onemli ise tercih et. Kendi cozumun sadece cok basit ihtiyaclar icin."
            },
            {
                "decision": "Neden Celery + Redis?",
                "reasoning": "Model training uzun sureli islem — API request icinde yapilamaz. Celery distributed task queue olarak training, evaluation ve feature engineering job'larini asenkron calistirir. Redis hem message broker hem result backend.",
                "alternatives": "RQ (Redis Queue), Dramatiq, Airflow, Prefect",
                "when_to_choose_alternative": "Basit job queue icin RQ yeter. Karmasik DAG orchestration icin Airflow/Prefect daha uygun."
            },
            {
                "decision": "Neden Feature Store ayri?",
                "reasoning": "Feature engineering'i model training'den ayirmak feature reuse saglar. Ayni feature'lari farkli modellerde kullanabilirsin. Online (real-time) ve offline (batch) feature serving farki onemli.",
                "alternatives": "Feature'lari model icinde hesaplamak, Feast, Tecton",
                "when_to_choose_alternative": "Az feature ve tek model varsa ayri store gereksiz. Buyuk olcekte Feast veya Tecton kullan."
            }
        ]
    },
    "what_you_learn": {
        "technical": [
            "End-to-end ML pipeline tasarimi",
            "MLflow experiment tracking ve model registry",
            "Feature engineering ve feature store",
            "Celery ile asenkron task orchestration",
            "Model serving API (real-time inference)",
            "scikit-learn ile model training",
            "Docker ile ML ortam containerization"
        ],
        "architectural": [
            "MLOps pipeline architecture",
            "Separation of training vs serving",
            "Feature store design patterns",
            "Model versioning ve lineage tracking",
            "A/B testing infrastructure"
        ],
        "ai_specific": [
            "Model evaluation ve comparison",
            "Data drift ve model drift detection",
            "Feature importance analysis",
            "Hyperparameter optimization",
            "Model monitoring ve alerting",
            "Auto-retraining triggers"
        ],
        "soft_skills": [
            "ML system documentation",
            "Model card yazimi",
            "Cross-functional collaboration (Data Science + Engineering)",
            "Production ML risk assessment"
        ]
    },
    "requirements": {
        "functional": [
            "CSV/JSON veri yukleme ve preprocessing",
            "Feature engineering pipeline (transform, scale, encode)",
            "Model training job'u baslatma ve takip etme",
            "MLflow ile experiment karsilastirma",
            "Model registry'de model versiyonlama",
            "Real-time inference API endpoint'i",
            "Model performans dashboard'u"
        ],
        "non_functional": [
            "Training job'u iptal edilebilir olmali",
            "Inference latency < 100ms (p95)",
            "Model artifact'leri versiyonlanmali",
            "Pipeline adimları idempotent olmali"
        ],
        "ai_requirements": [
            "En az 3 farkli model tipi desteklemeli",
            "Hyperparameter search (grid/random)",
            "Cross-validation ile model evaluation",
            "Data drift detection (input distribution monitoring)",
            "Model drift detection (prediction quality degradation)"
        ]
    },
    "evaluation_criteria": [
        {"criterion": "ML Pipeline Completeness", "weight": 25, "description": "End-to-end pipeline calisiyor mu? Data -> Training -> Serving akisi tam mi?"},
        {"criterion": "MLflow Integration", "weight": 20, "description": "Experiment tracking, model registry dogru kullaniliyor mu?"},
        {"criterion": "Model Serving & API", "weight": 15, "description": "Inference API performansi ve guvenirligi"},
        {"criterion": "Monitoring & Drift Detection", "weight": 20, "description": "Model ve data drift tespit ediliyor mu?"},
        {"criterion": "Code Quality & DevOps", "weight": 20, "description": "Docker, testing, CI/CD, documentation"}
    ],
    "milestones": [
        {
            "id": "p09-m1",
            "title": "Proje Altyapisi & Veri Pipeline Tasarimi",
            "overview": "Proje yapisini kur, veritabani semaalarini olustur, veri yukleme ve temizleme pipeline'ini implement et.",
            "estimated_hours": 8,
            "concepts_covered": ["project structure", "data ingestion", "data validation", "Pydantic schemas"],
            "steps": [
                {"step": 1, "title": "Proje Yapisi & Docker Setup", "why": "ML projeleri cok bilesenden olusur — temiz yapi bastan sart.", "instructions": "FastAPI + Celery + MLflow + PostgreSQL + Redis icin docker-compose olustur. Her servis ayri container.", "code_snippet": "# Proje yapisi\n/api          # FastAPI app\n/workers      # Celery workers\n/ml           # ML pipeline modules\n/features     # Feature engineering\n/monitoring   # Drift detection\n/frontend     # React dashboard", "checkpoint": "docker-compose up ile tum servisler calisiyor mu?"},
                {"step": 2, "title": "Veri Ingestion Pipeline", "why": "ML pipeline'in ilk adimi veriyi guvenli sekilde sisteme almak.", "instructions": "CSV/JSON upload endpoint'i olustur. Pydantic ile sema validasyonu. Buyuk dosyalar icin streaming upload. Veri profiling (column types, missing values, distributions).", "checkpoint": "CSV yukleyip veri profili goruntuleniyor mu?"},
                {"step": 3, "title": "Data Validation & Cleaning", "why": "Garbage in = garbage out. Model kalitesi veri kalitesine baglidir.", "instructions": "Otomatik veri temizleme:\n1. Missing value handling (drop, mean, median, mode)\n2. Outlier detection (IQR, Z-score)\n3. Type inference ve conversion\n4. Data quality score hesaplama", "checkpoint": "Eksik degerli ve outlier'li veri setinde temizleme dogru calisiyor mu?"},
                {"step": 4, "title": "Dataset Versioning", "why": "Hangi modelin hangi veri ile egitildigini bilmek reproducibility icin kritik.", "instructions": "Her yuklenen dataset'e versiyon ata. Metadata kaydet: boyut, column sayisi, tarih, quality score. Dataset compare ozeligi.", "checkpoint": "Ayni dataset'in 2 versiyonunu karsilastirabiliyor musun?"}
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Veri validasyonu ONCE yap, training SONRA — kirli veri ile model egitme\n2. Dataset versioning model reproducibility icin ZORUNLU\n3. Pydantic schema'lari hem API validasyonu hem veri validasyonu icin kullan\n4. Buyuk veri setleri icin streaming upload kullan — RAM'i patlatma",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nData quality ML basarisinin %80'ini belirler. Model algoritmasi degistirmekten once veri kalitesini iyilestir. Data profiling otomatik olmali — her upload'da calistiR.\n\nProduction'da data contract'lar kullan: schema degisirse pipeline durur, alert atar. Schema drift = potansiyel model failure."
        },
        {
            "id": "p09-m2",
            "title": "Feature Engineering & Feature Store",
            "overview": "Reusable feature'lar olustur, feature store pattern'ini implement et, online ve offline serving ayir.",
            "estimated_hours": 10,
            "concepts_covered": ["feature engineering", "feature store", "transformers", "pipeline"],
            "steps": [
                {"step": 1, "title": "Feature Transformer Pipeline", "why": "Feature engineering'i tekrarlanabilir ve test edilebilir yapmak icin pipeline pattern sart.", "instructions": "scikit-learn Pipeline + ColumnTransformer:\n1. Numeric: StandardScaler, MinMaxScaler\n2. Categorical: OneHotEncoder, LabelEncoder\n3. Text: TF-IDF, CountVectorizer\n4. Custom transformer'lar", "code_snippet": "from sklearn.pipeline import Pipeline\nfrom sklearn.compose import ColumnTransformer\n\npreprocessor = ColumnTransformer([\n    ('num', StandardScaler(), numeric_cols),\n    ('cat', OneHotEncoder(), categorical_cols),\n    ('text', TfidfVectorizer(), text_col)\n])\n\npipeline = Pipeline([\n    ('preprocessor', preprocessor),\n    ('model', model)\n])", "checkpoint": "Pipeline fit_transform dogru calisiyor mu? Farkli column tipleri dogru handle ediliyor mu?"},
                {"step": 2, "title": "Feature Store Implementation", "why": "Feature'lari merkezi depoda tutmak reuse saglar ve training-serving skew'u onler.", "instructions": "Feature store:\n1. Feature tanimlari (isim, tip, transform)\n2. Feature hesaplama (batch mode)\n3. Feature versioning\n4. Feature lineage (hangi raw data'dan geldi)", "checkpoint": "Ayni feature'i 2 farkli modelde kullanabiliyor musun?"},
                {"step": 3, "title": "Feature Importance & Selection", "why": "Cok feature = overfitting riski + yavas inference. Onemli feature'lari secmek model kalitesini arttirir.", "instructions": "Feature analizi:\n1. Correlation matrix\n2. Feature importance (tree-based)\n3. Recursive Feature Elimination (RFE)\n4. Sonuclari dashboard'da goster", "checkpoint": "Feature importance grafigi cikariyor mu?"}
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Training-serving skew en buyuk MLOps sorunu — ayni transform'u ikisinde de kullan\n2. Feature pipeline'ini SERIALIZE et (pickle/joblib) ve model ile birlikte kaydet\n3. Feature store'da metadata ZORUNLU: ne zaman hesaplandi, hangi kaynak, hangi transform\n4. One-hot encoding sonrasi boyut patlamasina dikkat — high cardinality'de target encoding kullan",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nFeature store buyuk takimlarda en onemli MLOps bilesenlerinden biri. Data scientist A'nin olusturdugu feature'i Data scientist B tekrar hesaplamak zorunda kalmamali.\n\nOnline (real-time) vs offline (batch) feature serving farki: online = Redis'ten milisaniyede oku, offline = batch job ile hesapla. Ikisinin tutarli olmasi sart."
        },
        {
            "id": "p09-m3",
            "title": "Model Training Pipeline & MLflow Entegrasyonu",
            "overview": "Celery ile asenkron model training, MLflow ile experiment tracking ve model karsilastirma.",
            "estimated_hours": 12,
            "concepts_covered": ["MLflow", "experiment tracking", "model training", "hyperparameter tuning", "Celery"],
            "steps": [
                {"step": 1, "title": "Celery Training Worker", "why": "Model egitimi dakikalar surer — API request icinde yapilamaz. Asenkron worker ile training job'lari arka planda calisir.", "instructions": "Celery worker:\n1. Training task tanimla\n2. Progress reporting (epoch/step bazli)\n3. Cancellation support\n4. Error handling ve retry\n5. Result storage", "code_snippet": "@celery_app.task(bind=True)\ndef train_model(self, config: dict):\n    self.update_state(state='TRAINING', meta={'progress': 0})\n    \n    with mlflow.start_run():\n        mlflow.log_params(config)\n        model = train(config)\n        mlflow.log_metrics(metrics)\n        mlflow.sklearn.log_model(model, 'model')\n    \n    self.update_state(state='COMPLETED', meta={'progress': 100})", "checkpoint": "Training job'u baslatip progress'i takip edebiliyor musun?"},
                {"step": 2, "title": "MLflow Experiment Tracking", "why": "Her experiment'in parametrelerini, metriklerini ve artifact'larini kaydetmek model secimi ve karsilastirmasi icin sart.", "instructions": "MLflow entegrasyonu:\n1. Experiment olustur\n2. Her run'da: parametreler, metrikler, modeli logla\n3. Artifact'lar: confusion matrix, feature importance plot\n4. Tag'ler: model tipi, dataset versiyonu\n5. Frontend'de experiment comparison", "checkpoint": "MLflow UI'da experiment'leri karsilastirabiliyormusun?"},
                {"step": 3, "title": "Hyperparameter Optimization", "why": "Model performansi hyperparameter secimjne baglidir. Otomatik search manual denemeden cok daha etkili.", "instructions": "Hyperparameter search:\n1. Grid search (az parametre)\n2. Random search (cok parametre)\n3. Her denemeyi MLflow'a logla\n4. En iyi modeli otomatik sec\n5. Search space ve strategy konfigurasyonu", "checkpoint": "Random search ile 10 deneme yapip en iyisini seciyor mu?"},
                {"step": 4, "title": "Model Registry & Versioning", "why": "Production'daki modelin hangi versiyon oldugunu bilmek ve kolayca rollback yapabilmek icin model registry sart.", "instructions": "MLflow Model Registry:\n1. Model kaydi (isim, versiyon, stage)\n2. Stage transitions: Staging -> Production -> Archived\n3. Model metadata: training config, dataset, metrics\n4. Model approval workflow\n5. API ile model yukle", "checkpoint": "Modeli Staging'den Production'a gecirebildin mi?"}
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. HER experiment'i logla — 'sonra loglarim' dersen unutursun\n2. Model artifact'inda feature pipeline'i da kaydet — yoksa inference'da transform uyusmazligi olur\n3. Hyperparameter search'te budget limit koy — sinirsiz arama kaynak israf eder\n4. Model Registry'de approval zorunlulugu koy — test edilmemis model production'a cikmasin",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nMLflow experiment tracking sadece Data Scientist icin degil. Product Manager'a 'son 10 denemede accuracy %3 artti' gostermek buyuk etki yapar.\n\nModel Registry governance onemli: kim promote edebilir? Hangi testlerden gecmeli? CI/CD ile model validation otomatiklestir."
        },
        {
            "id": "p09-m4",
            "title": "Model Serving & API Gateway",
            "overview": "Egitilmis modeli real-time inference icin API olarak sun. Batch prediction destegi ekle.",
            "estimated_hours": 8,
            "concepts_covered": ["model serving", "inference API", "batch prediction", "model loading"],
            "steps": [
                {"step": 1, "title": "Real-time Inference API", "why": "Modeli API olarak sunmak diger sistemlerin kullanmasini saglar.", "instructions": "FastAPI inference endpoint:\n1. Model registry'den aktif modeli yukle\n2. Input validasyonu (Pydantic)\n3. Feature transform uygula\n4. Prediction yap ve dondur\n5. Response'a confidence score ekle", "code_snippet": "@app.post('/api/predict')\nasync def predict(request: PredictionRequest):\n    model = load_production_model()\n    features = transform_input(request.data)\n    prediction = model.predict(features)\n    probability = model.predict_proba(features)\n    return {\n        'prediction': prediction[0],\n        'confidence': float(max(probability[0])),\n        'model_version': model.version\n    }", "checkpoint": "API'ya istek gonderip dogru prediction aliyor musun?"},
                {"step": 2, "title": "Model Caching & Warmup", "why": "Her istekte modeli diskten yuklemek yavas. Cache'te tutmak latency'i dramatik dusurur.", "instructions": "Model cache:\n1. Startup'ta modeli memory'ye yukle\n2. Model degistiginde cache invalidation\n3. Lazy loading: ilk istek geldiginde yukle\n4. Multiple model version support", "checkpoint": "Ilk istekten sonra inference latency < 50ms mi?"},
                {"step": 3, "title": "Batch Prediction Endpoint", "why": "Buyuk veri setleri icin tek tek prediction yapmak verimsiz. Batch endpoint toplu isleme saglar.", "instructions": "Batch prediction:\n1. CSV upload ile toplu prediction\n2. Celery worker'da calistir\n3. Sonuclari indirilebilir CSV olarak sun\n4. Progress tracking", "checkpoint": "1000 satirlik CSV ile batch prediction calisiyor mu?"},
                {"step": 4, "title": "A/B Testing Framework", "why": "Yeni modelin eskisinden iyi oldugunu production'da test etmek gerekir.", "instructions": "A/B testing:\n1. Traffic split (% bazli)\n2. Her model version'a giden istekleri logla\n3. Metric karsilastirma (accuracy, latency)\n4. Otomatik winner selection", "checkpoint": "Trafik %80/%20 bolunup iki model karsilastiriliyor mu?"}
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Model serving'de input validation ZORUNLU — production'da beklenmedik input gelir\n2. Model cache invalidation dogru calismali — eski model ile prediction yapmak tehlikeli\n3. A/B test sonuclarinda istatistiksel anlamlilik kontrol et — az veri ile karar verme\n4. Inference latency'yi MONITOR et — model buyurse latency artar",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nModel serving iki kategori: real-time (< 100ms, API) ve batch (dakikalar, job). Ikisi farkli altyapi gerektirir. Cogu ML sistemi ikisine de ihtiyac duyar.\n\nShadow deployment: yeni modeli production trafige maruz birak ama sonuclari kullanma — sadece logla ve compare et. En guvenli deployment stratejisi."
        },
        {
            "id": "p09-m5",
            "title": "Monitoring, Drift Detection & Auto-retraining",
            "overview": "Model performansini surekli izle. Data ve model drift tespit et. Gerektiginde otomatik retraining tetikle.",
            "estimated_hours": 12,
            "concepts_covered": ["model monitoring", "data drift", "concept drift", "alerting", "retraining"],
            "steps": [
                {"step": 1, "title": "Prediction Logging & Monitoring", "why": "Production'daki model performansini bilmeden iyilestirme yapamazsin.", "instructions": "Her prediction icin logla:\n1. Input features\n2. Prediction + confidence\n3. Latency\n4. Model version\n5. Timestamp\n\nDashboard'da goster: avg confidence, prediction distribution, latency percentiles", "checkpoint": "Son 1 saatin prediction istatistikleri gorunuyor mu?"},
                {"step": 2, "title": "Data Drift Detection", "why": "Input veri dagilimai degisirse model yanlis prediction yapar. Erken tespit etmek kritik.", "instructions": "Data drift:\n1. Training data distribution'ini baseline olarak kaydet\n2. Production input'larinin dagiliminii hesapla\n3. KS test veya PSI ile drift olc\n4. Feature bazinda drift raporu\n5. Threshold asildikiginda alert", "code_snippet": "from scipy.stats import ks_2samp\n\ndef detect_drift(baseline, current, threshold=0.05):\n    statistic, p_value = ks_2samp(baseline, current)\n    return {\n        'drifted': p_value < threshold,\n        'statistic': statistic,\n        'p_value': p_value\n    }", "checkpoint": "Dagiliimi degistirmis veri ile drift algilaniyor mu?"},
                {"step": 3, "title": "Model Performance Degradation", "why": "Model accuracy zamanla duser (concept drift). Ground truth geldikce performansi karsilastir.", "instructions": "Model drift:\n1. Ground truth (gercek sonuclar) toplama mekanizmasi\n2. Periyodik accuracy hesaplama\n3. Baseline accuracy ile karsilastir\n4. Performance drop alert\n5. Trend grafigi", "checkpoint": "Accuracy dusugunde alert tetikleniyor mu?"},
                {"step": 4, "title": "Auto-retraining Pipeline", "why": "Drift tespit edildiginde modeli otomatik yeniden egitmek downtime'i minimuma indirir.", "instructions": "Auto-retraining:\n1. Drift alert -> retraining trigger\n2. Son N gunun verisi ile yeni model egit\n3. Yeni modeli staging'e kaydet\n4. Validation testleri calistir\n5. Testler gecerse auto-promote (opsiyonel) veya insan onayibekle", "checkpoint": "Drift tetikleyip otomatik yeni model egitiliyor mu?"}
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Monitoring OLMADAN model deploy etme — kör ucus gibi\n2. Data drift != model drift — ikisini ayri olc\n3. Auto-retraining'de validation ZORUNLU — yeni model daha kotu olabilir\n4. Alert fatigue'a dikkat — cok fazla false alarm durumunda alert'ler ignore edilir",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nML model'leri yazilimdan farkli: kod zamanla bozulmaz ama model bozulur. Verinin dagiliimi degisir, kullanici davranisi degisir. Monitoring olmadan production ML sistemi zamam bombasi.\n\nMonitoring maliyeti: her prediction'i loglamak storage maliyeti getirir. Sampling stratejisi kullan — her prediction degil, her 10. veya 100. prediction'i logla."
        },
        {
            "id": "p09-m6",
            "title": "Frontend Dashboard & Production Deployment",
            "overview": "ML pipeline'ini yoneten dashboard, experiment comparison ve Docker deployment.",
            "estimated_hours": 10,
            "concepts_covered": ["React dashboard", "data visualization", "Docker", "CI/CD"],
            "steps": [
                {"step": 1, "title": "ML Dashboard — Training & Experiments", "why": "Data scientist'lerin experiment'leri goruntulemesi, karsilastirmasi ve yeni training baslattmasi icin UI sart.", "instructions": "Dashboard sayfalari:\n1. Dataset listesi ve profil\n2. Training job'lari (aktif, tamamlanan, basarisiz)\n3. Experiment comparison (metrik grafikleri)\n4. Model registry (versiyonlar, stage'ler)", "checkpoint": "Training baslatip progress'i dashboard'da takip edebiliyor musun?"},
                {"step": 2, "title": "Monitoring Dashboard", "why": "Prediction istatistikleri, drift alertleri ve model performansini gozlemlemek operasyonel kararlari bilgilendirir.", "instructions": "Monitoring goruntuleri:\n1. Real-time prediction stats (avg confidence, volume)\n2. Data drift heatmap (feature bazli)\n3. Model performance trend (accuracy over time)\n4. Active alerts ve alert gecmisi", "checkpoint": "Drift gerceklestiginde dashboard'da gorunuyor mu?"},
                {"step": 3, "title": "Docker & Production Config", "why": "Tum bilesenleri container olarak paketlemek deployment tutarliligini saglar.", "instructions": "Production:\n1. Multi-stage Dockerfile (API, worker, frontend)\n2. docker-compose.prod.yml\n3. Health checks (her servis)\n4. Environment variables (.env)\n5. Volume mounts (model artifacts, data)", "checkpoint": "docker-compose -f docker-compose.prod.yml up ile her sey calisiyor mu?"},
                {"step": 4, "title": "Model Card & Documentation", "why": "Her modelin ne yaptigi, limitasyonlari ve kullanim kilavuzu dokumante edilmeli.", "instructions": "Model card sablonu:\n1. Model amaci ve kapsam\n2. Training data aciklamasi\n3. Performance metrikleri\n4. Limitasyonlar ve bias'lar\n5. Kullanim talimatlari\n6. Versiyon gecmisi", "checkpoint": "Her model icin model card oluusturulmus mu?"}
            ],
            "must_note": "📝 Bunu Kesinlikle Not Al:\n1. Dashboard'da 'Deploy to Production' butonu koymadan once approval workflow kur\n2. Docker volume mount'lari dogru yapilandir — model artifact'lari kaybolmasin\n3. Model card yazmak sikici ama ZORUNLU — regulatory compliance icin gerekebilir\n4. Health check'ler sadece 200 donmemeli — model'in yuklu oldugunu da dogrulamali",
            "senior_learns": "🎩 Senior/CTO Boyle Ogrenir:\nMLOps maturity model: Level 0 (manual), Level 1 (ML pipeline automation), Level 2 (CI/CD for ML). Bu projede Level 1'e ulasiyorsun. Level 2 icin model validation testleri CI/CD pipeline'ina entegre et.\n\nModel card kavrami Google'dan geliyor. Responsible AI icin her modelin limitasyonlarini ve bias'larini dokumante etmek artik industry standard."
        }
    ],
    "interview_prep": {
        "questions": [
            "ML pipeline'inizi basiden sonra anlatir misiniz?",
            "MLflow'u nasil kullandiniz? Alternatifleri degerlendirdiniz mi?",
            "Feature store nedir ve neden onemli?",
            "Training-serving skew nedir ve nasil onlediniz?",
            "Data drift'i nasil tespit ediyorsunuz?",
            "Model'i production'a nasil deploy ediyorsunuz? Rollback nasil yapilir?",
            "A/B testing framework'unuz nasil calisiyor?",
            "Auto-retraining ne zaman tetiklenir? Guvenlik onlemleri neler?",
            "Model monitoring'de hangi metrikleri takip ediyorsunuz?",
            "Bu pipeline'i 100x veri ile nasil olceklerdiniz?"
        ],
        "talking_points": [
            "End-to-end ML pipeline deneyimi — veri ingestion'dan monitoring'e",
            "MLflow ile experiment tracking ve model registry best practices",
            "Feature engineering pipeline pattern — scikit-learn Pipeline",
            "Data drift detection — KS test ve PSI metrikleri",
            "A/B testing infrastructure — istatistiksel anlamlilik",
            "Auto-retraining ve guvenlik guardrail'leri",
            "Model card ve responsible AI dokumantasyonu"
        ]
    },
    "resources": [
        {"title": "MLflow Documentation", "url": "https://mlflow.org/docs/latest/index.html", "why": "MLflow'un tum ozelliklerini anlamak icin resmi dokuman"},
        {"title": "Made With ML - MLOps", "url": "https://madewithml.com/", "why": "End-to-end MLOps kursu — cok kapsamli ve ucretsiz"},
        {"title": "scikit-learn Pipeline Guide", "url": "https://scikit-learn.org/stable/modules/compose.html", "why": "Feature pipeline olusturmak icin resmi rehber"},
        {"title": "Celery Documentation", "url": "https://docs.celeryq.dev/", "why": "Asenkron task queue icin"},
        {"title": "Google Model Cards", "url": "https://modelcards.withgoogle.com/", "why": "Model card yazmak icin Google'in standart sablonu"}
    ]
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content', 'projects', 'project-09.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(project, f, ensure_ascii=False, indent=2)
print(f"Written to {out_path}: {os.path.getsize(out_path)} bytes")
