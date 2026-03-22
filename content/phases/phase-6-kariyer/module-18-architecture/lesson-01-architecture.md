---
title: "Yazılım Mimarisi Patterns"
id: mod-18-architecture/lesson-01
estimated_minutes: 95
order: 1
tags: [architecture, microservices, monolith, serverless, event-driven, cqrs, ddd, kafka, rabbitmq, clean-architecture]
prerequisites: [mod-17-genai/lesson-02]
---

# Yazılım Mimarisi Patterns

Yazılım mimarisi, bir sistemin **yüksek seviyeli yapısını** tanımlar: component'ler, aralarındaki ilişkiler ve tasarım prensipleri. Doğru mimari kararları vermek, bir projeyi **ölçeklenebilir, bakımı kolay ve sürdürülebilir** yapar. Yanlış kararlar ise projeyi ileride teknik borç çöplüğüne çevirir. Bu ders, modern yazılım mimarisi pattern'larını, ne zaman hangi mimariyi seçmen gerektiğini ve gerçek dünya trade-off'larını öğretecek.

:::exercise
## Pratik Alistirmalar

### Alistirma 1: Mimari Karar Belgesi (ADR)
Bir e-ticaret uygulamasi icin su karar icin ADR yazin:
"Monolitik mimari yerine microservice mimarisi secildi"
**Format:** Baslik, Baglam, Karar, Sonuclar (trade-off'lar), Durum

### Alistirma 2: Katmanli Mimari Refactoring
Asagidaki "God Controller" kodunu temiz katmanli mimariye donusturun (Controller -> Service -> Repository):
```typescript
app.post('/orders', async (req, res) => {
  const user = await db.query('SELECT * FROM users WHERE id = $1', [req.userId]);
  if (!user) return res.status(404).json({ error: 'User not found' });
  const product = await db.query('SELECT * FROM products WHERE id = $1', [req.body.productId]);
  if (product.stock < req.body.quantity) return res.status(400).json({ error: 'Out of stock' });
  await db.query('UPDATE products SET stock = stock - $1 WHERE id = $2', [req.body.quantity, product.id]);
  const order = await db.query('INSERT INTO orders (user_id, product_id, quantity, total) VALUES ($1, $2, $3, $4) RETURNING *',
    [user.id, product.id, req.body.quantity, product.price * req.body.quantity]);
  await sendEmail(user.email, 'Siparis Onaylandi', `Siparis #${order.id}`);
  res.status(201).json(order);
});
```

### Alistirma 3: Event-Driven Tasarim
Yukaridaki siparis sistemini event-driven mimariye donusturun:
- OrderCreated event'i yayinlayin
- StockService, NotificationService ve AnalyticsService bu event'i dinlesin
- Her service bagimsiz calisabilmeli (loose coupling)
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Monolith, microservice ve serverless mimarileri karsilastir. Her birinin avantaj, dezavantaj ve uygun kullanim alanlarini goster. Bir startup MVP'sinden unicorn'a buyurken mimari nasil evrilir? Monolith-first yaklasimi neden tavsiye edilir? Conway's Law mimari kararlari nasil etkiler?"

**2. Pratik Uygulama:**
> "Bir e-ticaret uygulamasini Event-Driven Architecture ile tasarla. Siparis oluşturma akisini event'lerle modelleyen bir sistem ciz: OrderCreated, PaymentProcessed, InventoryReserved, ShipmentScheduled. Message broker (RabbitMQ/Kafka) secimini ve her event'in handler'ini acikla. Saga pattern ile dagitik transaction yonet."
> Takip: "Simdi CQRS pattern'ini uygula: okuma ve yazma modellerini ayir. Read model icin Elasticsearch, write model icin PostgreSQL kullan. Event sourcing ile veri tutarliligini sagla."

**3. Mukemmellik Icin:**
> "500 developer'lik bir organizasyonda microservice mimarisini yonetiyorum. Service mesh (Istio), API Gateway, distributed tracing (Jaeger), centralized logging (ELK Stack), service discovery ve circuit breaker pattern'ini icereen bir platform engineering stratejisi oluştur. Team Topologies ile takim yapisini mimariyle nasil hizalarim?"

### Pair Programming Ipucu
Mimari karar verirken AI'a mevcut sistem yapisini anlat ve sor: "Bu monolith uygulamayi microservice'lere bolmeli miyim? Hangi bounded context'leri ayirmaliyim? Strangler Fig pattern ile nasil kademeli gecis yaparim? Trade-off analizini yap."
:::

:::must-note
## Defterine Yaz!

1. **"Best architecture" diye bir şey yoktur.** Her mimari kararı bir trade-off'tur. Monolith basit ama ölçeklenemez, microservices ölçeklenebilir ama karmaşık. Context'e göre karar ver.
2. **Monolith First!** Yeni projelere monolith ile başla. Microservices'e geçiş, domain boundary'ler netleştikten SONRA yapılmalı. Premature decomposition en büyük hatadır.
3. **CQRS = Read ve Write'ı ayır.** Okuma ve yazma pattern'leri farklıysa (çoğu real-world app'te öyle), ayrı modeller kullan. Bu performans ve ölçeklenebilirlik kazandırır.
4. **Event-Driven Architecture = Loose coupling.** Service'ler birbirini doğrudan çağırmak yerine event publish/subscribe eder. Bu bağımlılığı azaltır ama debugging'i zorlaştırır.
5. **Domain-Driven Design (DDD) = Business logic'i koda yansıt.** Bounded Context, Aggregate, Entity, Value Object — bu kavramlar büyük projelerde kaosu engeller.
:::

:::senior-learns
## Senior/CTO Böyle Öğrenir

Senior mimari öğrenirken:
- **Trade-off analysis**: Her kararın maliyetini ve faydasını ölçer, "X her zaman doğru" demez
- **Conway's Law**: Organizasyon yapısının mimariyi nasıl şekillendirdiğini bilir
- **ADR (Architectural Decision Records)**: Kararları ve nedenlerini dokümante eder
- **Failure modes**: "Bu sistem nasıl çökebilir?" sorusunu sürekli sorar
- **Evolutionary architecture**: Mimariyi bir kez seçip bırakmaz, sürekli evolve eder
- **Cost of change**: İlk gün doğru seçmenin vs sonradan değiştirmenin maliyetini hesaplar
:::

---

## 1. Mimari Stilleri — Overview

### 1.1 Monolith Architecture

:::concept
## Monolithic Architecture

**Monolith**, tüm uygulamanın **tek bir deployable unit** olarak çalışmasıdır. UI, business logic, data access — hepsi aynı process'te.

```
┌─────────────────────────────────────┐
│           Monolith App              │
│                                     │
│  ┌──────────┐  ┌──────────────────┐ │
│  │    UI     │  │  Business Logic  │ │
│  └──────────┘  └──────────────────┘ │
│  ┌──────────┐  ┌──────────────────┐ │
│  │   Auth   │  │   Data Access    │ │
│  └──────────┘  └──────────────────┘ │
│                                     │
│         Single Database             │
└─────────────────────────────────────┘
```

**Avantajları:**
- Basit development ve deployment
- Kolay debugging (tek process)
- Tek database, transaction kolay
- Yeni projelere ideal

**Dezavantajları:**
- Ölçekleme = tüm uygulamayı ölçeklemek (all-or-nothing)
- Tek bir bug tüm sistemi çökertebilir
- Büyüdükçe development yavaşlar
- Teknoloji değişimi zor (hepsi aynı stack)
:::

### 1.2 Microservices Architecture

:::concept
## Microservices Architecture

**Microservices**, uygulamayı **bağımsız, küçük service'lere** bölme yaklaşımıdır. Her service kendi database'ine sahiptir, bağımsız deploy edilebilir.

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  User    │  │  Order   │  │ Payment  │
│ Service  │  │ Service  │  │ Service  │
│          │  │          │  │          │
│  [DB1]   │  │  [DB2]   │  │  [DB3]   │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
─────┴─────────────┴─────────────┴─────
            Message Bus / API Gateway
```

**Avantajları:**
- Bağımsız deployment (her service ayrı release)
- Bağımsız ölçekleme (sadece yoğun service'i scale et)
- Technology diversity (her service farklı dil/framework)
- Fault isolation (bir service çökse diğerleri çalışır)
- Küçük takımlara uygun (her takım kendi service'inden sorumlu)

**Dezavantajları:**
- Network complexity (latency, reliability)
- Distributed transactions zor
- Debugging ve tracing karmaşık
- Operational overhead (monitoring, logging, deployment)
- Data consistency challenge
:::

### 1.3 Serverless Architecture

:::concept
## Serverless Architecture

**Serverless**, sunucu yönetimi olmadan sadece function'lar deploy etme yaklaşımıdır. Cloud provider (AWS Lambda, Google Cloud Functions, Azure Functions) altyapıyı yönetir.

```
[API Gateway]
      ↓
┌──────────────────────────┐
│   Lambda Functions       │
│                          │
│  /users  → userHandler() │
│  /orders → orderHandler()│
│  /pay    → payHandler()  │
│                          │
│  Event triggers:         │
│  - S3 upload → resize()  │
│  - SQS msg  → process() │
│  - Cron     → cleanup()  │
└──────────────────────────┘
      ↓
[DynamoDB / S3 / RDS]
```

**Avantajları:**
- Zero server management
- Auto-scaling (0'dan binlerce instance'a)
- Pay-per-use (çalışmadığında para ödemezsin)
- Hızlı prototipleme

**Dezavantajları:**
- Cold start latency (ilk çağrı yavaş)
- Vendor lock-in (AWS Lambda → Google Cloud zor geçiş)
- Stateless constraint (state tutamaz)
- Debugging zorluğu
- Execution time limit (15 dakika max — AWS Lambda)
:::

:::comparison
## Mimari Stilleri Karşılaştırması

| Kriter | Monolith | Microservices | Serverless |
|--------|----------|---------------|------------|
| **Complexity** | Düşük | Yüksek | Orta |
| **Scalability** | Dikey (scale up) | Yatay (scale out) | Otomatik |
| **Deployment** | Tek unit | Her service bağımsız | Function bazlı |
| **Cost (başlangıç)** | Düşük | Yüksek | Çok düşük |
| **Cost (scale)** | Yüksek | Orta | Değişken |
| **Team size** | 1-10 developer | 10+ developer | 1-5 developer |
| **Best for** | Startup MVP | Enterprise scale | Event-driven tasks |
| **Technology** | Tek stack | Mixed | Cloud-native |
| **Debugging** | Kolay | Zor | Zor |
| **Time to market** | Hızlı | Yavaş | Çok hızlı |
:::

:::deha-tip
## Mimari Seçim Rehberi

**Monolith seç eğer:**
- Yeni proje / MVP / startup
- Takım < 10 kişi
- Domain boundary'ler henüz net değil
- Hızlı market entry gerekiyor

**Microservices seç eğer:**
- Farklı bölümlerin farklı ölçeklenmesi gerekiyor
- Büyük organizasyon, birden fazla takım
- Domain boundary'ler net ve stabil
- Bağımsız deployment kritik

**Serverless seç eğer:**
- Event-driven workload (file processing, webhooks)
- Düzensiz traffic (bazen 0, bazen binlerce request)
- Hızlı prototip gerekiyor
- Ops takımı yok
:::

---

## 2. Event-Driven Architecture (EDA)

:::concept
## Event-Driven Architecture

**Event-Driven Architecture**, service'lerin birbirini doğrudan çağırmak yerine **event** üzerinden iletişim kurduğu mimaridir.

```
[Order Service]
     │
     ├──publish──→ "OrderCreated" event
     │                   ↓
     │    ┌──────────────┴───────────────┐
     │    ↓                              ↓
[Payment Service]              [Notification Service]
  "Ödemeyi işle"                 "Email gönder"
     │                              │
     ├──publish──→ "PaymentCompleted"  │
     │                   ↓            │
     │         [Shipping Service]     │
     │          "Kargoyu hazırla"     │
```

**Temel kavramlar:**
- **Event**: Sistemde olan bir şeyin kaydı ("OrderCreated", "UserRegistered")
- **Producer**: Event'i oluşturan service
- **Consumer**: Event'i dinleyen ve işleyen service
- **Event Bus/Broker**: Event'leri taşıyan altyapı (Kafka, RabbitMQ)
:::

:::code
## Event-Driven Architecture — Python Implementasyon

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable
import json
import uuid

# Event base class
@dataclass
class Event:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    data: dict = field(default_factory=dict)

# Event Bus — In-memory implementation
class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        """Event type'a handler register et"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        print(f"  [EventBus] {handler.__name__} subscribed to '{event_type}'")

    def publish(self, event: Event):
        """Event'i tüm subscriber'lara gönder"""
        print(f"\n  [EventBus] Publishing '{event.event_type}' (id: {event.event_id[:8]})")
        handlers = self._handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"  [EventBus] Error in {handler.__name__}: {e}")

# Global event bus
bus = EventBus()

# === Services ===

class OrderService:
    def create_order(self, user_id: str, items: list, total: float):
        order_id = str(uuid.uuid4())[:8]
        print(f"\n[OrderService] Order created: {order_id}")

        # Event publish
        bus.publish(Event(
            event_type="OrderCreated",
            data={"order_id": order_id, "user_id": user_id, "items": items, "total": total}
        ))
        return order_id

class PaymentService:
    def handle_order_created(self, event: Event):
        data = event.data
        print(f"[PaymentService] Processing payment for order {data['order_id']}: {data['total']} TL")

        # Ödeme başarılı
        bus.publish(Event(
            event_type="PaymentCompleted",
            data={"order_id": data["order_id"], "amount": data["total"]}
        ))

class NotificationService:
    def handle_order_created(self, event: Event):
        data = event.data
        print(f"[NotificationService] Sending order confirmation email for order {data['order_id']}")

    def handle_payment_completed(self, event: Event):
        data = event.data
        print(f"[NotificationService] Sending payment receipt for order {data['order_id']}")

class ShippingService:
    def handle_payment_completed(self, event: Event):
        data = event.data
        print(f"[ShippingService] Preparing shipment for order {data['order_id']}")

# === Wiring ===
payment = PaymentService()
notification = NotificationService()
shipping = ShippingService()

bus.subscribe("OrderCreated", payment.handle_order_created)
bus.subscribe("OrderCreated", notification.handle_order_created)
bus.subscribe("PaymentCompleted", notification.handle_payment_completed)
bus.subscribe("PaymentCompleted", shipping.handle_payment_completed)

# === Test ===
order_service = OrderService()
order_service.create_order(
    user_id="user_123",
    items=["laptop", "mouse"],
    total=15000
)
```
:::

---

## 3. Message Queues — RabbitMQ ve Kafka

:::comparison
## RabbitMQ vs Kafka

| Özellik | RabbitMQ | Kafka |
|---------|----------|-------|
| **Model** | Message Queue (push) | Event Log (pull) |
| **Pattern** | Point-to-point, pub/sub | Pub/sub, streaming |
| **Message retention** | Consume edilince silinir | Configurable retention |
| **Throughput** | ~50K msg/sec | ~1M+ msg/sec |
| **Ordering** | Queue başına garanti | Partition başına garanti |
| **Use case** | Task queue, RPC | Event streaming, log aggregation |
| **Complexity** | Orta | Yüksek |
| **Best for** | Geleneksel microservices | Big data, real-time streaming |
:::

:::code
## RabbitMQ — Python ile Message Queue

```python
import pika
import json

# Producer — Mesaj gönder
def send_message(queue: str, message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent
    )

    print(f"[Producer] Sent to '{queue}': {message}")
    connection.close()

# Consumer — Mesaj al ve işle
def consume_messages(queue: str, callback):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    def on_message(ch, method, properties, body):
        message = json.loads(body)
        print(f"[Consumer] Received from '{queue}': {message}")
        callback(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=on_message)

    print(f"[Consumer] Waiting for messages on '{queue}'...")
    channel.start_consuming()

# Kullanım
send_message("order_queue", {
    "order_id": "ord_123",
    "action": "process_payment",
    "amount": 99.99
})
```
:::

:::code
## Kafka — Python ile Event Streaming

```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None
)

def publish_event(topic: str, key: str, event: dict):
    future = producer.send(topic, key=key, value=event)
    result = future.get(timeout=10)
    print(f"[Kafka Producer] Published to {topic} partition {result.partition}")

# Event publish
publish_event("orders", "user_123", {
    "event_type": "OrderCreated",
    "order_id": "ord_456",
    "items": ["laptop"],
    "total": 15000
})
producer.flush()

# Consumer
consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='payment-service',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    print(f"[Kafka Consumer] {event['event_type']}: order {event['order_id']}")
    # Process event...
```
:::

---

## 4. CQRS — Command Query Responsibility Segregation

:::concept
## CQRS

**CQRS**, read (query) ve write (command) operasyonları için **ayrı modeller** kullanma pattern'ıdır.

```
                Traditional (Single Model)
                ┌──────────────────┐
    Read/Write → │   Same Model     │ → Same DB
                └──────────────────┘

                CQRS (Separated Models)
                ┌──────────────────┐
    Commands  → │  Write Model     │ → Write DB
                └──────────────────┘
                        │ (events/sync)
                        ↓
                ┌──────────────────┐
    Queries   → │  Read Model      │ → Read DB (denormalized)
                └──────────────────┘
```

**Ne zaman kullan:**
- Read/write oranı çok farklı (90% read, 10% write)
- Read ve write için farklı optimizasyonlar gerekiyor
- Complex domain logic var (write tarafında)
- Farklı view'lar gerekiyor (aynı veriyi farklı şekillerde oku)
:::

:::code
## CQRS Pattern Implementation

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

# === Command Side (Write) ===

@dataclass
class CreateOrderCommand:
    user_id: str
    items: list[dict]
    shipping_address: str

@dataclass
class CancelOrderCommand:
    order_id: str
    reason: str

class OrderCommandHandler:
    """Write model — business logic burada"""

    def __init__(self):
        self._orders = {}  # Write store
        self._events = []

    def handle_create(self, cmd: CreateOrderCommand) -> str:
        order_id = str(uuid.uuid4())[:8]

        # Business validation
        if not cmd.items:
            raise ValueError("Order must have at least one item")

        total = sum(item["price"] * item["quantity"] for item in cmd.items)

        # Create order (write model)
        order = {
            "order_id": order_id,
            "user_id": cmd.user_id,
            "items": cmd.items,
            "total": total,
            "status": "created",
            "shipping_address": cmd.shipping_address,
            "created_at": datetime.utcnow().isoformat()
        }
        self._orders[order_id] = order

        # Emit event (for read model sync)
        self._events.append({
            "type": "OrderCreated",
            "data": order
        })

        return order_id

    def handle_cancel(self, cmd: CancelOrderCommand):
        order = self._orders.get(cmd.order_id)
        if not order:
            raise ValueError(f"Order {cmd.order_id} not found")
        if order["status"] == "shipped":
            raise ValueError("Cannot cancel shipped order")

        order["status"] = "cancelled"
        order["cancel_reason"] = cmd.reason

        self._events.append({
            "type": "OrderCancelled",
            "data": {"order_id": cmd.order_id, "reason": cmd.reason}
        })

# === Query Side (Read) ===

class OrderQueryHandler:
    """Read model — optimized for queries, denormalized"""

    def __init__(self):
        self._read_store = {}  # Denormalized read store
        self._by_user = {}     # Index by user_id
        self._by_status = {}   # Index by status

    def sync_event(self, event: dict):
        """Write side'dan gelen event'leri read model'e sync et"""
        if event["type"] == "OrderCreated":
            data = event["data"]
            # Denormalized view
            view = {
                "order_id": data["order_id"],
                "user_id": data["user_id"],
                "total": data["total"],
                "item_count": len(data["items"]),
                "status": data["status"],
                "created_at": data["created_at"],
                "summary": f"{len(data['items'])} items, {data['total']} TL"
            }
            self._read_store[data["order_id"]] = view

            # User index
            if data["user_id"] not in self._by_user:
                self._by_user[data["user_id"]] = []
            self._by_user[data["user_id"]].append(data["order_id"])

    def get_order(self, order_id: str) -> Optional[dict]:
        return self._read_store.get(order_id)

    def get_user_orders(self, user_id: str) -> list[dict]:
        order_ids = self._by_user.get(user_id, [])
        return [self._read_store[oid] for oid in order_ids]

    def get_order_count(self) -> int:
        return len(self._read_store)

# === Usage ===
command_handler = OrderCommandHandler()
query_handler = OrderQueryHandler()

# Write
order_id = command_handler.handle_create(CreateOrderCommand(
    user_id="user_001",
    items=[
        {"name": "Laptop", "price": 15000, "quantity": 1},
        {"name": "Mouse", "price": 500, "quantity": 2}
    ],
    shipping_address="Istanbul, Turkey"
))

# Sync events to read model
for event in command_handler._events:
    query_handler.sync_event(event)

# Read (fast, denormalized)
order = query_handler.get_order(order_id)
print(f"Order: {order['summary']}")

user_orders = query_handler.get_user_orders("user_001")
print(f"User has {len(user_orders)} orders")
```
:::

---

## 5. Event Sourcing

:::concept
## Event Sourcing

**Event Sourcing**, uygulamanın durumunu (state) doğrudan saklamak yerine, **duruma yol açan tüm event'leri** saklama yaklaşımıdır.

```
Traditional: Sadece güncel durumu sakla
  Account { balance: 1500 }

Event Sourcing: Tüm event'leri sakla
  1. AccountCreated { initial_balance: 0 }
  2. MoneyDeposited { amount: 2000 }
  3. MoneyWithdrawn { amount: 500 }
  → Güncel durum: balance = 0 + 2000 - 500 = 1500
```

**Avantajları:**
- Complete audit trail (her şeyin kaydı var)
- Time travel (herhangi bir andaki duruma geri dön)
- Event replay (event'leri tekrar oynatarak yeni view oluştur)
- Debugging kolaylığı

**Dezavantajları:**
- Complexity artışı
- Storage gereksinimleri (event sayısı sürekli artar)
- Event versioning zorluğu
- Eventual consistency
:::

:::code
## Event Sourcing — Bank Account Example

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol
import uuid

# Event definitions
@dataclass
class AccountEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class AccountCreated(AccountEvent):
    account_id: str = ""
    owner: str = ""

@dataclass
class MoneyDeposited(AccountEvent):
    account_id: str = ""
    amount: float = 0

@dataclass
class MoneyWithdrawn(AccountEvent):
    account_id: str = ""
    amount: float = 0

# Event Store
class EventStore:
    def __init__(self):
        self._events: dict[str, list[AccountEvent]] = {}

    def append(self, aggregate_id: str, event: AccountEvent):
        if aggregate_id not in self._events:
            self._events[aggregate_id] = []
        self._events[aggregate_id].append(event)

    def get_events(self, aggregate_id: str) -> list[AccountEvent]:
        return self._events.get(aggregate_id, [])

# Account Aggregate — state'i event'lerden rebuild eder
class BankAccount:
    def __init__(self):
        self.account_id = ""
        self.owner = ""
        self.balance = 0.0
        self._version = 0

    @classmethod
    def from_events(cls, events: list[AccountEvent]) -> "BankAccount":
        """Event'lerden account state'i rebuild et"""
        account = cls()
        for event in events:
            account._apply(event)
        return account

    def _apply(self, event: AccountEvent):
        if isinstance(event, AccountCreated):
            self.account_id = event.account_id
            self.owner = event.owner
            self.balance = 0
        elif isinstance(event, MoneyDeposited):
            self.balance += event.amount
        elif isinstance(event, MoneyWithdrawn):
            self.balance -= event.amount
        self._version += 1

    def __repr__(self):
        return f"BankAccount(id={self.account_id}, owner={self.owner}, balance={self.balance}, version={self._version})"

# === Usage ===
store = EventStore()
account_id = "acc_001"

# Event'leri kaydet
store.append(account_id, AccountCreated(account_id=account_id, owner="Ali"))
store.append(account_id, MoneyDeposited(account_id=account_id, amount=5000))
store.append(account_id, MoneyWithdrawn(account_id=account_id, amount=1500))
store.append(account_id, MoneyDeposited(account_id=account_id, amount=3000))
store.append(account_id, MoneyWithdrawn(account_id=account_id, amount=2000))

# State'i event'lerden rebuild et
account = BankAccount.from_events(store.get_events(account_id))
print(f"Current state: {account}")
# balance = 0 + 5000 - 1500 + 3000 - 2000 = 4500

# Time travel — ilk 3 event'ten sonraki durum
account_v3 = BankAccount.from_events(store.get_events(account_id)[:3])
print(f"State at v3: {account_v3}")
# balance = 0 + 5000 - 1500 = 3500

# Audit trail
print("\nAudit Trail:")
for event in store.get_events(account_id):
    print(f"  [{event.timestamp}] {event.__class__.__name__}: {event}")
```
:::

---

## 6. Hexagonal / Clean Architecture

:::concept
## Hexagonal Architecture (Ports and Adapters)

**Hexagonal Architecture**, business logic'i dış dünyadan (database, API, UI) **izole etme** yaklaşımıdır. Core domain'in hiçbir dış bağımlılığı yoktur.

```
              Adapters (Infrastructure)
         ┌─────────────────────────────┐
         │  REST API    CLI    GraphQL  │
         │     │         │       │      │
         │  ┌──┴─────────┴───────┴──┐  │
         │  │     Ports (Interfaces) │  │
         │  │  ┌──────────────────┐  │  │
         │  │  │                  │  │  │
         │  │  │  Domain / Core   │  │  │
         │  │  │  (Business Logic)│  │  │
         │  │  │                  │  │  │
         │  │  └──────────────────┘  │  │
         │  │     Ports (Interfaces) │  │
         │  └──┬─────────┬───────┬──┘  │
         │     │         │       │      │
         │  Postgres   Redis   Email   │
         └─────────────────────────────┘
```

**Kurallar:**
1. **Domain core**, hiçbir dış kütüphaneye bağımlı olmamalı
2. **Ports** = interface/abstract class (domain'in beklediği contract)
3. **Adapters** = port'ların implementasyonları (database, API, email)
4. **Dependency yönü**: Dışarıdan içeriye doğru (adapter → port → domain)
:::

:::code
## Clean Architecture — Python Implementation

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

# === DOMAIN LAYER (innermost — no external dependencies) ===

@dataclass
class User:
    """Domain Entity"""
    id: str
    email: str
    name: str
    is_active: bool = True

    def deactivate(self):
        self.is_active = False

    def change_email(self, new_email: str):
        if "@" not in new_email:
            raise ValueError("Invalid email format")
        self.email = new_email

# === PORTS (interfaces — domain defines what it needs) ===

class UserRepository(ABC):
    """Port — Domain'in beklediği contract"""
    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: ...

class EmailService(ABC):
    """Port — Email gönderme interface'i"""
    @abstractmethod
    def send_welcome_email(self, to: str, name: str) -> None: ...

# === USE CASES (Application Layer) ===

class RegisterUserUseCase:
    """Application service — business rules orchestration"""

    def __init__(self, user_repo: UserRepository, email_service: EmailService):
        self._user_repo = user_repo
        self._email_service = email_service

    def execute(self, user_id: str, email: str, name: str) -> User:
        # Business rule: email unique olmalı
        existing = self._user_repo.find_by_email(email)
        if existing:
            raise ValueError(f"Email '{email}' is already registered")

        # Create domain entity
        user = User(id=user_id, email=email, name=name)

        # Persist
        self._user_repo.save(user)

        # Side effect
        self._email_service.send_welcome_email(to=email, name=name)

        return user

# === ADAPTERS (outermost — infrastructure implementations) ===

class InMemoryUserRepository(UserRepository):
    """Adapter — In-memory implementation (test/development)"""
    def __init__(self):
        self._store: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._store[user.id] = user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._store.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._store.values():
            if user.email == email:
                return user
        return None

class ConsoleEmailService(EmailService):
    """Adapter — Console'a yazdıran email service (development)"""
    def send_welcome_email(self, to: str, name: str) -> None:
        print(f"[Email] Welcome email sent to {to}: 'Hoş geldin {name}!'")

# === COMPOSITION ROOT (wiring) ===

# Development
user_repo = InMemoryUserRepository()
email_service = ConsoleEmailService()
register_use_case = RegisterUserUseCase(user_repo, email_service)

# Use it
user = register_use_case.execute("u1", "ali@test.com", "Ali")
print(f"User created: {user}")

# Production'da sadece adapter'ları değiştirirsin:
# user_repo = PostgresUserRepository(db_connection)
# email_service = SendGridEmailService(api_key)
# register_use_case = RegisterUserUseCase(user_repo, email_service)
```
:::

---

## 7. Domain-Driven Design (DDD)

:::concept
## DDD Temel Kavramları

| Kavram | Açıklama | Örnek |
|--------|----------|-------|
| **Bounded Context** | Domain'in belirli bir alt bölümü, kendi ubiquitous language'ı olan sınır | Order Context, Payment Context |
| **Entity** | Kimliği (ID) olan domain object | User, Order, Product |
| **Value Object** | Kimliği olmayan, değeriyle tanımlanan object | Money, Address, Email |
| **Aggregate** | Birlikte değişen entity kümesi, tek root entity üzerinden erişilir | Order (root) + OrderItems |
| **Repository** | Aggregate'leri persist eden arayüz | OrderRepository |
| **Domain Event** | Domain'de olan önemli bir şey | OrderPlaced, PaymentReceived |
| **Domain Service** | Tek entity'e ait olmayan business logic | PricingService, ShippingCalculator |
:::

:::code
## DDD — Value Object ve Entity

```python
from dataclasses import dataclass
from typing import Optional

# Value Object — immutable, identity yok, değerle karşılaştırılır
@dataclass(frozen=True)  # frozen = immutable
class Money:
    amount: float
    currency: str = "TRY"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract {self.currency} and {other.currency}")
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Insufficient funds")
        return Money(result, self.currency)

    def multiply(self, factor: int) -> "Money":
        return Money(self.amount * factor, self.currency)

@dataclass(frozen=True)
class Address:
    street: str
    city: str
    country: str
    postal_code: str

# Entity — mutable, ID ile tanımlanır
@dataclass
class OrderItem:
    product_id: str
    product_name: str
    unit_price: Money
    quantity: int

    @property
    def total_price(self) -> Money:
        return self.unit_price.multiply(self.quantity)

# Aggregate Root
class Order:
    """Order Aggregate Root — tüm iç state değişiklikleri buradan geçer"""

    def __init__(self, order_id: str, customer_id: str, shipping_address: Address):
        self._order_id = order_id
        self._customer_id = customer_id
        self._shipping_address = shipping_address
        self._items: list[OrderItem] = []
        self._status = "draft"
        self._events: list[dict] = []

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def total(self) -> Money:
        if not self._items:
            return Money(0)
        total = Money(0)
        for item in self._items:
            total = total.add(item.total_price)
        return total

    def add_item(self, product_id: str, name: str, price: Money, quantity: int):
        """Invariant: draft durumunda item eklenebilir"""
        if self._status != "draft":
            raise ValueError(f"Cannot add items to {self._status} order")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self._items.append(OrderItem(product_id, name, price, quantity))

    def place(self):
        """Invariant: en az 1 item olmalı"""
        if not self._items:
            raise ValueError("Cannot place empty order")
        if self._status != "draft":
            raise ValueError(f"Cannot place {self._status} order")

        self._status = "placed"
        self._events.append({
            "type": "OrderPlaced",
            "order_id": self._order_id,
            "total": self.total.amount
        })

    def cancel(self, reason: str):
        if self._status not in ("draft", "placed"):
            raise ValueError(f"Cannot cancel {self._status} order")
        self._status = "cancelled"
        self._events.append({
            "type": "OrderCancelled",
            "order_id": self._order_id,
            "reason": reason
        })

    @property
    def domain_events(self) -> list[dict]:
        return self._events.copy()

# === Usage ===
address = Address("Istiklal Cad. No:1", "Istanbul", "Turkey", "34000")
order = Order("ord_001", "cust_001", address)

order.add_item("prod_1", "Laptop", Money(15000), 1)
order.add_item("prod_2", "Mouse", Money(500), 2)

print(f"Total: {order.total}")  # Money(amount=16000, currency='TRY')

order.place()
print(f"Events: {order.domain_events}")
```
:::

---

## 8. API Gateway Pattern

:::concept
## API Gateway

**API Gateway**, tüm client request'lerinin geçtiği **tek giriş noktasıdır**. Client'lar doğrudan microservice'lere bağlanmak yerine gateway üzerinden iletişim kurar.

```
[Mobile App]  [Web App]  [3rd Party]
      │           │          │
      └───────────┴──────────┘
              │
       [API Gateway]
       ├─ Authentication
       ├─ Rate Limiting
       ├─ Load Balancing
       ├─ Request Routing
       ├─ Response Caching
       ├─ Protocol Translation
       └─ Logging/Monitoring
              │
    ┌─────────┼──────────┐
    ↓         ↓          ↓
[User API] [Order API] [Product API]
```

**Popular API Gateways:**
- **Kong**: Open source, plugin-based
- **AWS API Gateway**: Managed, serverless
- **Nginx**: Reverse proxy + gateway
- **Traefik**: Container-native, auto-discovery
:::

:::architecture[API Gateway ile Microservice Routing]
```
                    ┌──────────────────────────────────────┐
                    │         API Gateway (Kong/Nginx)      │
                    │                                       │
                    │  ┌─────────┐ ┌──────────┐ ┌────────┐ │
                    │  │  Auth   │ │  Rate    │ │  Log   │ │
                    │  │ Plugin  │ │ Limiter  │ │ Plugin │ │
                    │  └────┬────┘ └────┬─────┘ └────┬───┘ │
                    │       └───────────┴────────────┘     │
                    └──────────────┬────────────────────────┘
                                  │
                    ┌─────────────┼─────────────────┐
                    │             │                  │
              /api/users    /api/orders      /api/products
                    │             │                  │
              ┌─────▼────┐ ┌─────▼────┐  ┌──────────▼──┐
              │  User    │ │  Order   │  │  Product    │
              │  Service │ │  Service │  │  Service    │
              │  :8001   │ │  :8002   │  │  :8003      │
              └──────────┘ └──────────┘  └─────────────┘
```
:::

:::code
## API Gateway — Nginx Konfigürasyonu Örneği

```nginx
# /etc/nginx/conf.d/api-gateway.conf
upstream user_service {
    server user-svc:8001;
    server user-svc-2:8001;  # Load balancing
}

upstream order_service {
    server order-svc:8002;
}

upstream product_service {
    server product-svc:8003;
}

server {
    listen 80;
    server_name api.example.com;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;

    # User Service
    location /api/users {
        limit_req zone=api burst=20;
        proxy_pass http://user_service;
        proxy_set_header X-Request-ID $request_id;
    }

    # Order Service
    location /api/orders {
        limit_req zone=api burst=10;
        proxy_pass http://order_service;
    }

    # Product Service
    location /api/products {
        limit_req zone=api burst=50;
        proxy_pass http://product_service;
        proxy_cache api_cache;
        proxy_cache_valid 200 5m;  # GET response 5dk cache
    }

    # Health check endpoint
    location /health {
        return 200 '{"status": "ok"}';
        add_header Content-Type application/json;
    }
}
```
:::

---

## 9. Service Mesh

:::concept
## Service Mesh (Istio Sidecar Pattern)

**Service Mesh**, microservice'ler arası iletişimi yöneten **altyapı katmanıdır**. Her service'in yanına bir **sidecar proxy** (genellikle Envoy) eklenir. Bu proxy tüm gelen ve giden trafiği yakalar.

**API Gateway vs Service Mesh:**
- **API Gateway**: Dış dünya ile microservice'ler arasındaki iletişim (North-South traffic)
- **Service Mesh**: Microservice'ler arası iletişim (East-West traffic)
:::

:::architecture[Service Mesh — Istio Sidecar Pattern]
```
                    ┌──────────────────────────────────────┐
                    │          Control Plane (istiod)       │
                    │   ┌─────────┐ ┌──────┐ ┌──────────┐ │
                    │   │ Config  │ │ Cert │ │ Telemetry│ │
                    │   │ Manager │ │  CA  │ │ Collector│ │
                    │   └─────────┘ └──────┘ └──────────┘ │
                    └──────────┬───────────────────────────┘
                               │ (config push)
                    ┌──────────┼───────────────────────────┐
                    │          │   Data Plane               │
                    │  ┌───────▼────────┐  ┌──────────────┐│
                    │  │   Pod A        │  │   Pod B      ││
                    │  │ ┌────────────┐ │  │ ┌──────────┐ ││
                    │  │ │ User       │ │  │ │ Order    │ ││
                    │  │ │ Service    │ │  │ │ Service  │ ││
                    │  │ └─────┬──────┘ │  │ └────┬─────┘ ││
                    │  │       │        │  │      │       ││
                    │  │ ┌─────▼──────┐ │  │ ┌────▼─────┐ ││
                    │  │ │  Envoy     │◄├──┤►│  Envoy   │ ││
                    │  │ │  Sidecar   │ │  │ │  Sidecar │ ││
                    │  │ └────────────┘ │  │ └──────────┘ ││
                    │  └────────────────┘  └──────────────┘│
                    └──────────────────────────────────────┘
```
:::

:::comparison
## API Gateway vs Service Mesh

| Kriter | API Gateway | Service Mesh |
|--------|-------------|--------------|
| **Trafik yönü** | North-South (dış → iç) | East-West (iç → iç) |
| **Konum** | Sistemin girişinde | Her service'in yanında |
| **Sorumluluk** | Routing, auth, rate limit | mTLS, retry, circuit breaker |
| **Örnek araçlar** | Kong, Nginx, AWS API GW | Istio, Linkerd, Consul Connect |
| **Karmaşıklık** | Orta | Yüksek |
| **Ne zaman** | Her microservice projede | 10+ service olduğunda |
:::

:::realworld
## Netflix — Service Mesh Kullanımı

Netflix, yüzlerce microservice'i yönetmek için kendi service mesh altyapısını geliştirdi. Zuul (API Gateway) ile dış trafiği yönetir, dahili iletişimde ise Envoy proxy kullanır. Her service çağrısında otomatik retry, circuit breaking ve load balancing sağlanır. Bu sayede bir service'in yavaşlaması tüm sistemi etkilemez.
:::

---

## 10. Observability Trio: Logs + Metrics + Traces

:::concept
## Observability Nedir?

**Observability**, bir sistemin dış çıktılarına bakarak iç durumunu anlama yeteneğidir. Üç temel sütunu vardır:

1. **Logs** (Ne oldu?): Event kayıtları — hata mesajları, info logları
2. **Metrics** (Ne kadar?): Sayısal ölçümler — CPU, latency, request count
3. **Traces** (Nasıl aktı?): Bir request'in tüm service'lerden geçiş yolculuğu
:::

:::architecture[Observability Stack]
```
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │ User Service│  │Order Service│  │Payment Svc  │
  │             │  │             │  │             │
  │ app.log()   │  │ app.log()   │  │ app.log()   │  ← LOGS
  │ metrics.inc │  │ metrics.inc │  │ metrics.inc │  ← METRICS
  │ span.start  │  │ span.start  │  │ span.start  │  ← TRACES
  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
         │                │                │
    ┌────▼────┐     ┌─────▼────┐     ┌─────▼────┐
    │Filebeat │     │Filebeat  │     │Filebeat  │
    │Prom exp.│     │Prom exp. │     │Prom exp. │
    │OTel SDK │     │OTel SDK  │     │OTel SDK  │
    └────┬────┘     └────┬─────┘     └────┬─────┘
         │               │                │
    ┌────▼───────────────▼────────────────▼────┐
    │            Collection Layer               │
    │  ┌────────────┐ ┌───────────┐ ┌────────┐ │
    │  │ELK Stack   │ │Prometheus │ │ Jaeger │ │
    │  │(Logs)      │ │(Metrics)  │ │(Traces)│ │
    │  └─────┬──────┘ └─────┬─────┘ └───┬────┘ │
    └────────┼──────────────┼────────────┼──────┘
             │              │            │
    ┌────────▼──────────────▼────────────▼──────┐
    │              Grafana Dashboard             │
    │  ┌──────────┐ ┌──────────┐ ┌────────────┐ │
    │  │ Log      │ │ Metric   │ │ Trace      │ │
    │  │ Panel    │ │ Graphs   │ │ Waterfall  │ │
    │  └──────────┘ └──────────┘ └────────────┘ │
    └────────────────────────────────────────────┘
```
:::

:::code
## Observability — Python Implementasyon

```python
import logging
import time
import uuid
from functools import wraps

# ============================================
# 1. STRUCTURED LOGGING (ELK Stack ile)
# ============================================
import json

class StructuredLogger:
    """JSON formatında structured log"""

    def __init__(self, service_name: str):
        self.service = service_name
        self.logger = logging.getLogger(service_name)

    def _log(self, level: str, message: str, **kwargs):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "service": self.service,
            "level": level,
            "message": message,
            **kwargs
        }
        print(json.dumps(log_entry))

    def info(self, msg, **kwargs):
        self._log("INFO", msg, **kwargs)

    def error(self, msg, **kwargs):
        self._log("ERROR", msg, **kwargs)

    def warn(self, msg, **kwargs):
        self._log("WARN", msg, **kwargs)

# Kullanim
log = StructuredLogger("order-service")
log.info("Order created", order_id="ord_123", user_id="u_456")
# {"timestamp": "...", "service": "order-service", "level": "INFO",
#  "message": "Order created", "order_id": "ord_123", "user_id": "u_456"}


# ============================================
# 2. METRICS (Prometheus compatible)
# ============================================
class MetricsCollector:
    """Basit Prometheus-uyumlu metrics collector"""

    def __init__(self):
        self._counters: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = {}

    def increment(self, name: str, labels: dict = None, value: float = 1):
        key = f"{name}_{labels}" if labels else name
        self._counters[key] = self._counters.get(key, 0) + value

    def observe(self, name: str, value: float):
        if name not in self._histograms:
            self._histograms[name] = []
        self._histograms[name].append(value)

    def get_counter(self, name: str) -> float:
        return self._counters.get(name, 0)

metrics = MetricsCollector()

def track_request(func):
    """Request metric decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            metrics.increment("http_requests_total",
                            {"method": "GET", "status": "200"})
            return result
        except Exception as e:
            metrics.increment("http_requests_total",
                            {"method": "GET", "status": "500"})
            raise
        finally:
            duration = time.time() - start
            metrics.observe("http_request_duration_seconds", duration)
    return wrapper


# ============================================
# 3. DISTRIBUTED TRACING (Jaeger/OpenTelemetry)
# ============================================
class Span:
    """Basit trace span"""

    def __init__(self, name: str, trace_id: str = None, parent_id: str = None):
        self.name = name
        self.trace_id = trace_id or str(uuid.uuid4())[:8]
        self.span_id = str(uuid.uuid4())[:8]
        self.parent_id = parent_id
        self.start_time = time.time()
        self.end_time = None
        self.tags: dict = {}

    def set_tag(self, key: str, value):
        self.tags[key] = value
        return self

    def finish(self):
        self.end_time = time.time()
        duration_ms = (self.end_time - self.start_time) * 1000
        print(f"[TRACE] {self.trace_id} | {self.name} "
              f"({duration_ms:.1f}ms) tags={self.tags}")

    def child(self, name: str) -> "Span":
        return Span(name, trace_id=self.trace_id, parent_id=self.span_id)

# Kullanim — request'in tum service'lerden gecis yolculugu
root = Span("POST /api/orders")
root.set_tag("user_id", "u_123")

db_span = root.child("db.query")
db_span.set_tag("query", "INSERT INTO orders")
time.sleep(0.01)  # simule
db_span.finish()

cache_span = root.child("redis.set")
cache_span.set_tag("key", "order:456")
time.sleep(0.002)
cache_span.finish()

root.finish()
# [TRACE] a1b2c3d4 | db.query (10.1ms)
# [TRACE] a1b2c3d4 | redis.set (2.0ms)
# [TRACE] a1b2c3d4 | POST /api/orders (12.5ms)
```
:::

:::realworld
## Uber — Observability ile Sorun Tespiti

Uber, Jaeger adlı distributed tracing aracını geliştirdi (open source). Bir kullanicinin ride request'i 20+ microservice'den gecer. Jaeger ile her request'in hangi service'te ne kadar zaman harcadigini gorebilirler. Bir service yavaslayinca dakikalar icinde bottleneck tespit edilir. Prometheus + Grafana ile CPU, memory, request rate gibi metrikleri izler ve anomali durumunda otomatik alert oluşturur.
:::

---

## 11. Architectural Decision Records (ADR)

:::concept
## ADR — Mimari Kararları Dokümante Et

**ADR**, mimari kararları ve nedenlerini kaydeden kısa dokümanlarıdır. Her ADR şu yapıdadır:

```markdown
# ADR-001: Use PostgreSQL as Primary Database

## Status: Accepted

## Context
E-ticaret uygulamamız için veritabanı seçmemiz gerekiyor.
ACID compliance, complex queries ve JSON desteği kritik.

## Decision
PostgreSQL kullanacağız.

## Consequences
### Positive
- ACID compliance ile data integrity
- jsonb ile flexible schema
- Mature ecosystem, community desteği

### Negative
- Horizontal scaling MongoDB kadar kolay değil
- DBA expertise gerekebilir

## Alternatives Considered
- MongoDB: Schema flexibility iyi ama ACID zayıf
- MySQL: Olgunluk iyi ama JSON desteği zayıf
```

**ADR yazma alışkanlığı**, seni junior'dan senior'a taşıyan önemli bir pratiktir.
:::

:::tip
## Ne Zaman ADR Yaz?

- Database seçimi
- Framework/library seçimi
- Mimari style değişikliği (monolith → microservices)
- Authentication stratejisi
- Deployment stratejisi
- API versioning yaklaşımı

Kural: "Bu kararı 6 ay sonra sorgulayabilir miyiz?" → Evet ise, ADR yaz.
:::

---

## 12. Real-World Architecture Örneği

:::realworld
## E-Commerce System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    E-Commerce Platform                        │
│                                                               │
│  [CDN] → [Next.js Frontend] → [API Gateway (Kong)]          │
│                                      │                        │
│           ┌──────────────────────────┼──────────────┐         │
│           ↓                          ↓              ↓         │
│    [User Service]           [Product Service]  [Order Service]│
│    - Auth (JWT)             - CRUD             - Cart          │
│    - Profile                - Search (ES)      - Checkout     │
│    - Permissions            - Inventory        - Status       │
│    [PostgreSQL]             [PostgreSQL+ES]    [PostgreSQL]   │
│           │                          │              │         │
│           └──────────────────────────┼──────────────┘         │
│                                      │                        │
│                             [Kafka Event Bus]                 │
│                                      │                        │
│           ┌──────────────────────────┼──────────────┐         │
│           ↓                          ↓              ↓         │
│    [Payment Service]        [Notification Svc] [Analytics]    │
│    - Stripe/iyzico          - Email (SES)      - Clickstream │
│    - Refunds                - SMS              - Reports      │
│    [PostgreSQL]             [Redis queue]       [ClickHouse]  │
│                                                               │
│  [Observability]: Prometheus + Grafana + Jaeger              │
│  [Infrastructure]: Kubernetes + Terraform                     │
└──────────────────────────────────────────────────────────────┘
```
:::

:::interview
## Mülakat Soruları — Junior vs Senior Cevap Karşılaştırması

**S1**: "Monolith vs Microservices — yeni bir projeye hangisiyle başlarsın?"

**Junior cevap**: "Microservices ile başlarım çünkü daha modern ve ölçeklenebilir."

**Senior cevap**: "Monolith ile başlarım. Domain boundary'ler henüz net değilken microservices'e bölmek premature decomposition'dır. Monolith-first yaklaşımını tercih ederim. Domain netleştikçe modüler monolith'e, ardından Strangler Fig pattern ile kademeli microservices geçişi yaparım. Conway's Law gereği takım yapısı da mimariyi belirler — 3 kişilik takımda microservices overhead'dir."

---

**S2**: "CQRS ne zaman kullanılır?"

**Junior cevap**: "Read ve write ayrı olsun diye her projede kullanırım."

**Senior cevap**: "Read/write pattern'leri çok farklı olduğunda. Mesela e-ticaret'te ürün katalog okuma çok yoğun ama ürün güncelleme nadir. Read model'i Elasticsearch'te denormalize edip cache'leyerek okuma performansını artırabilirim, write model'i PostgreSQL'de domain logic'e odaklandırabilirim. Ancak basit CRUD uygulamalarında CQRS gereksiz karmaşıklık ekler — trade-off'u iyi değerlendirmek lazım."

---

**S3**: "Event Sourcing'in dezavantajları neler?"

**Junior cevap**: "Biraz daha fazla kod yazmak gerekiyor."

**Senior cevap**: "Dört temel zorluk var: (1) Event versioning — schema değiştiğinde eski event'leri nasıl okuyacaksın? (2) Storage büyümesi — event'ler asla silinmez, snapshot mekanizması lazım. (3) Eventual consistency — read model her zaman güncel olmayabilir. (4) Debugging zorluğu — state'i görmek için event'leri replay etmen gerekir. Basit CRUD uygulamalarında kesinlikle kullanılmamalı."

---

**S4**: "Service Mesh nedir ve ne zaman kullanılır?"

**Junior cevap**: "Bilmiyorum / Istio kullanırız."

**Senior cevap**: "Service mesh, microservice'ler arası iletişimi yöneten altyapı katmanıdır. Her pod'a sidecar proxy (Envoy) eklenir. mTLS ile servisler arası güvenli iletişim, otomatik retry, circuit breaking ve distributed tracing sağlar. API Gateway North-South trafiği yönetirken, service mesh East-West trafiği yönetir. 10+ service olduğunda değer katmaya başlar, altında operational overhead'i haklı çıkarmaz."

---

**S5**: "Observability ve monitoring arasındaki fark nedir?"

**Junior cevap**: "İkisi de aynı şey — sistemi izlemek."

**Senior cevap**: "Monitoring bilinen sorunları tespit eder: CPU %90'ın üstünde mi? Request latency threshold'u aştı mı? Observability ise bilinmeyen sorunları teşhis etmeyi sağlar: Logs, metrics ve traces birlikte kullanılarak daha önce görülmemiş bir hatanın kök nedenine ulaşılır. Monitoring 'ne oldu?' sorusunu cevaplar, observability 'neden oldu?' sorusunu cevaplar."
:::

:::exercise
## Ek Pratik Alıştırmalar

### Alıştırma 4: Service Mesh Tasarımı
3 microservice'ten oluşan bir e-ticaret sistemi için service mesh konfigürasyonu tasarlayın:
- **User Service**, **Order Service**, **Payment Service**
- Service'ler arası iletişimde mutual TLS (mTLS) aktif olmalı
- Payment Service'e yapılan çağrılarda circuit breaker tanımlayın (5 ardışık hata → devre açık, 30sn sonra half-open)
- Order Service → Payment Service arasında retry policy tanımlayın (max 3 retry, exponential backoff)
- Tüm service'lerden gelen metrikler Prometheus'a gönderilmeli

### Alıştırma 5: Observability Stack Kurulumu
Bir Node.js uygulaması için observability stack planlayın:
1. **Logging**: Structured JSON log formatı tasarlayın (hangi field'lar olmalı?)
2. **Metrics**: Hangi metrikleri toplamalısınız? (RED method: Rate, Errors, Duration)
3. **Tracing**: Bir sipariş oluşturma akışının trace waterfall'ını çizin (hangi span'ler olacak?)
4. **Alerting**: Hangi durumlar için alert kurarsınız? (SLO: %99.9 availability, p99 latency < 500ms)

### Alıştırma 6: Mimari Evrim Senaryosu
Bir startup'ın büyüme aşamalarına göre mimari evrim planı yazın:
- **0-1K kullanıcı**: Monolith + single DB
- **1K-100K kullanıcı**: Hangi değişiklikler gerekir?
- **100K-1M kullanıcı**: Hangi component'ler ayrılmalı?
- **1M+ kullanıcı**: Full microservices'e geçiş stratejisi nedir?
Her aşamada trade-off'ları ve geçiş maliyetlerini belirtin.

---

### Alıştırma 7: Strangler Fig Pattern ile Modernizasyon (Orta)

Legacy monolith'ten microservices'e adim adim gecis plani yazin.

1. Mevcut monolith'teki module sinirlarini belirleyin
2. Ilk ayrilacak servisi secin (en az bagimliligi olan)
3. Strangler Fig pattern ile yeni servisin monolith'in onune nasil konacagini cizelgelleyin
4. API Gateway ile trafik yonlendirme stratejisi yazin
5. Veri migrasyon plani oluşturun (shared DB → service-per-DB)

**Beklenen Sonuc:** Migrasyon plani risk bazli onceliklendirme icermeli. Her adimda rollback stratejisi tanimlanmali. Veri tutarliligi icin eventual consistency deseni aciklanmali.

---

### Alıştırma 8: Event Storming Workshop Simulasyonu (Orta)

Bir e-ticaret sistemi icin Event Storming oturumu simulasyonu yapin.

1. Domain event'leri tanimlayin (OrderPlaced, PaymentProcessed, ItemShipped...)
2. Command'lari belirleyin (PlaceOrder, ProcessPayment, ShipItem...)
3. Aggregate'leri tanimlayin (Order, Payment, Shipment...)
4. Bounded context'leri cizin (Ordering, Payment, Fulfillment, Inventory)
5. Context Map oluşturun (context'ler arasi iliskiler)

**Beklenen Sonuc:** En az 15 domain event, 10 command ve 5 aggregate tanimlanmali. Bounded context'ler arasindaki bagimlilklar net olmali. Context Map'te upstream/downstream iliskileri gosterilmeli.

---

### Alıştırma 9: API Versioning ve Backward Compatibility (Zor)

API versioning stratejisi tasarlayin ve breaking change yonetim plani oluşturun.

1. URL versioning (`/v1/users`), header versioning (`Accept: application/vnd.api.v1+json`) ve query parameter versioning (`?version=1`) arasinda secim yapin ve nedenleri aciklayin
2. Deprecation policy yazin (ne zaman eski versiyon kapatilir, nasil bildirilir)
3. Breaking change örneği: `User.name` → `User.firstName + User.lastName` icin migration plani
4. SDK/client library versioning stratejisi

**Beklenen Sonuc:** Versioning stratejisi secimi ve gerekceleri aciklanmali. Deprecation timeline'i net olmali (örnek: 6 ay uyari → 3 ay sunset → kaldirma). Migration guide örneği hazirlanmali.

---

### Alıştırma 10: Disaster Recovery ve Business Continuity Plani (Zor)

Bir SaaS urunun icin disaster recovery plani oluşturun.

1. **RPO (Recovery Point Objective):** Maksimum ne kadar veri kaybi kabul edilebilir? (örnek: 1 saat)
2. **RTO (Recovery Time Objective):** Sistemin ne kadar surede ayaga kalkmasi gerekir? (örnek: 15 dakika)
3. Multi-region deployment stratejisi cizelgelleyin (active-active vs active-passive)
4. Failover suresci tanimlayin (otomatik vs manuel)
5. Backup ve restore prosedurlerini yazin (DB, file storage, config)
6. DR drill plani oluşturun (yilda 2 kez test senaryosu)

**Beklenen Sonuc:** RPO ve RTO hedefleri net olmali. Multi-region mimarisi diyagrami cizilebilmeli. DR drill senaryolari tanimlanmali. Maliyet analizi yapilmali (active-active vs active-passive).
:::

:::exercise
### Alistirma 11: Monolith vs Microservices Karsilastirmasi (Kolay)

Monolith ve microservices mimarilerini karsilastir.

```markdown
# TODO: Karsilastirma tablosu doldur

| Kriter             | Monolith         | Microservices      |
|--------------------|------------------|--------------------|
| Deployment         | Tek birim        | Bagimsiz servisler |
| Olcekleme          | Dikey (vertical) | Yatay (horizontal) |
| Teknoloji Secimi   | Tek stack        | ?                  |
| Takim Yapisi       | Tek takim        | ?                  |
| Debugging          | Kolay            | ?                  |
| Data Consistency   | ACID             | ?                  |
| Iletisim           | In-process       | ?                  |
| Ilk Gelistirme     | Hizli            | ?                  |

# TODO: Ne zaman monolith, ne zaman microservices secilmeli?
# TODO: Monolith -> Microservices gecis stratejisi yaz (Strangler Fig Pattern)
# TODO: Gerçek dünyadan 3 ornek ver (Netflix, Uber, vb.)
```

**Beklenen Sonuc:** Tablo eksiksiz doldurulmali. Secim kriterleri net aciklanmali. Gecis stratejisi tanimlanmali.
**Ipucu:** Cogu startup monolith ile baslamali. Microservices'a erken gecis "distributed monolith" tehlikesi tasir. Conway's Law'u unutma.
:::

:::exercise
### Alistirma 12: Clean Architecture Katmanlarini Tasarla (Kolay)

Clean Architecture prensipleriyle bir uygulamanin katmanlarini tanimla.

```typescript
// TODO: Katmanlari tanimla ve bagimliliklari ciz

// 1. Domain Layer (Entity + Value Object)
// interface User { id: string; email: string; name: string; }
// class Email { constructor(private value: string) { /* validation */ } }

// 2. Use Case Layer (Application Business Rules)
// interface CreateUserUseCase { execute(input: CreateUserDTO): Promise<User>; }

// 3. Interface Adapters (Controllers, Presenters, Gateways)
// class UserController { constructor(private createUser: CreateUserUseCase) {} }

// 4. Frameworks & Drivers (Express, PostgreSQL, etc.)
// class PostgresUserRepository implements UserRepository {}

// TODO: Her katmanin bagimlilk yonunu belirle (iceridien disariya)
// TODO: Dependency Inversion prensibini acikla
// TODO: Bu yapinin test edilebilirligini goster
```

**Beklenen Sonuc:** 4 katman tanimlanmali. Bagimlilik yonu iceeri dogru olmali. Test edilebilirlik aciklanmali.
**Ipucu:** Dependency Rule: ic katmanlar dis katmanlari bilmez. UseCase PostgreSQL'i bilmez — sadece UserRepository interface'ini bilir.
:::

:::exercise
### Alistirma 13: API Tasarimi ve REST Best Practices (Kolay)

RESTful API tasarim prensiplerini uygula.

```markdown
# TODO: Bir e-ticaret API'si icin endpoint tasarla

# Urunler
GET    /api/v1/products              # Liste (pagination, filter, sort)
GET    /api/v1/products/:id          # Detay
POST   /api/v1/products              # Olustur
PUT    /api/v1/products/:id          # Guncelle
DELETE /api/v1/products/:id          # Sil

# TODO: Siparisler endpoint'lerini tasarla
# TODO: Kullanici endpoint'lerini tasarla
# TODO: Nested resources (urunun yorumlari)

# TODO: Pagination response formati
# { "data": [...], "meta": { "total": 100, "page": 1, "limit": 20 } }

# TODO: Error response formati
# { "error": { "code": "NOT_FOUND", "message": "...", "details": [...] } }

# TODO: API versioning stratejisi sec (URL vs Header)
# TODO: HATEOAS ornegi yaz
```

**Beklenen Sonuc:** Tum CRUD endpoint'leri tanimlanmali. Tutarli response formati olmali. Versioning stratejisi belirlenmeli.
**Ipucu:** Resource isimleri cogul (products, orders), HTTP metotlari eylem belirtir. Nested resource 2 seviyeyi gecmemeli.
:::

:::exercise
### Alistirma 14: Event-Driven Architecture Tasarimi (Orta)

Event-driven mimari ile bir siparis sistemi tasarla.

```typescript
// TODO: Event tanimla
// interface OrderCreatedEvent {
//   type: 'ORDER_CREATED';
//   payload: { orderId: string; userId: string; items: Item[]; total: number; };
//   metadata: { timestamp: Date; correlationId: string; };
// }

// TODO: Event producer
// class OrderService {
//   async createOrder(data: CreateOrderDTO) {
//     const order = await this.repository.save(data);
//     await this.eventBus.publish({ type: 'ORDER_CREATED', payload: order });
//   }
// }

// TODO: Event consumers tanimla
// 1. PaymentService: ORDER_CREATED -> odeme baslat
// 2. InventoryService: ORDER_CREATED -> stok dusur
// 3. NotificationService: ORDER_CREATED -> email gonder
// 4. AnalyticsService: ORDER_CREATED -> metrikleri guncelle

// TODO: Event sourcing vs event notification farki
// TODO: Idempotency sagla (ayni event'i tekrar isleme)
// TODO: Dead letter queue stratejisi yaz
```

**Beklenen Sonuc:** Event akisi tanimlanmali. Her consumer'in gorevi acik olmali. Idempotency ve hata yonetimi saglanmali.
**Ipucu:** Event-driven'da servisler birbirini bilmez — loose coupling. Ama eventual consistency kabul etmelisin. Idempotency key ile duplike islemeyi onle.
:::

:::exercise
### Alistirma 15: Database Secimi ve Data Modeling (Orta)

Farkli veritabani turlerini karsilastir ve dogru secimi yap.

```markdown
# TODO: Veritabani secim matrisi olustur

| Senaryo              | En Uygun DB      | Neden?              |
|----------------------|-------------------|---------------------|
| E-ticaret (ACID)     | PostgreSQL        | Relational, ACID    |
| Sosyal ag (graph)    | Neo4j             | ?                   |
| Oturum yonetimi      | Redis             | ?                   |
| Log depolama         | Elasticsearch     | ?                   |
| IoT sensor verisi    | TimescaleDB       | ?                   |
| Icerik yonetimi      | MongoDB           | ?                   |
| Mesajlasma kuyruğu   | Kafka             | ?                   |

# TODO: Her DB icin data model ornegi ciz
# TODO: CAP teoremini acikla: Consistency, Availability, Partition Tolerance
# TODO: SQL vs NoSQL ne zaman secilmeli karar agaci olustur
```

**Beklenen Sonuc:** Tablo doldurulmali. Her senaryo icin DB secimi gerekcelendirilmeli. CAP teoremi aciklanmali.
**Ipucu:** CAP: dagitik sistemde 3 garantiden en fazla 2'si saglanabilir. PostgreSQL = CP, Cassandra = AP, MongoDB = CP (default).
:::

:::exercise
### Alistirma 16: CQRS Pattern Implementasyonu (Orta)

Command Query Responsibility Segregation pattern'ini uygula.

```typescript
// TODO: Command (yazma) tarafi
// interface CreateOrderCommand {
//   userId: string;
//   items: { productId: string; quantity: number }[];
// }
// class OrderCommandHandler {
//   async handle(command: CreateOrderCommand): Promise<string> {
//     // Validate, create order, publish event
//   }
// }

// TODO: Query (okuma) tarafi
// interface OrderQueryService {
//   getOrderById(id: string): Promise<OrderReadModel>;
//   getOrdersByUser(userId: string): Promise<OrderSummary[]>;
// }

// TODO: Read model'i write model'den farkli tasarla
// Write: normalized (3NF), ACID
// Read: denormalized, hizli okuma icin optimize

// TODO: Sync mekanizmasi (event ile read model guncelleme)
// TODO: Ne zaman CQRS kullanmali, ne zaman kullanmamali?
```

**Beklenen Sonuc:** Command ve Query ayrilmali. Read model okuma icin optimize edilmeli. Sync mekanizmasi tanimlanmali.
**Ipucu:** CQRS her yerde gerekli degil. Okuma/yazma oranlari cok farkli ise (1000:1 okuma:yazma) veya read model farkli optimize edilecekse kullan.
:::

:::exercise
### Alistirma 17: Caching Stratejileri (Orta)

Farkli caching stratejilerini tasarla ve uygula.

```typescript
// TODO: Cache-Aside (Lazy Loading)
// async function getUser(id: string) {
//   let user = await cache.get(`user:${id}`);
//   if (!user) {
//     user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
//     await cache.set(`user:${id}`, user, { ttl: 3600 });
//   }
//   return user;
// }

// TODO: Write-Through
// TODO: Write-Behind (Write-Back)
// TODO: Cache invalidation stratejileri
// - TTL-based
// - Event-based (veri degisince cache temizle)
// - Version-based (ETag)

// TODO: Cache stampede (thundering herd) problemi ve cozumu
// TODO: Multi-layer cache (L1: memory, L2: Redis, L3: CDN)
// TODO: Her stratejinin avantaj/dezavantaj tablosu
```

**Beklenen Sonuc:** 3 cache stratejisi implement edilmeli. Invalidation yontemleri tanimlanmali. Cache stampede cozumu aciklanmali.
**Ipucu:** "There are only two hard things in CS: cache invalidation and naming things." Cache TTL + event-based invalidation birlestir.
:::

:::exercise
### Alistirma 18: Disaster Recovery Plani (Zor)

Bir uygulama icin disaster recovery plani olustur.

```markdown
# TODO: DR Plan sablonu

## 1. RTO ve RPO Hedefleri
- RTO (Recovery Time Objective): Maksimum kabul edilebilir kesinti suresi
- RPO (Recovery Point Objective): Maksimum kabul edilebilir veri kaybi

## 2. Backup Stratejisi
- Full backup: Haftalik
- Incremental backup: Gunluk
- WAL archiving: Surekli
- TODO: 3-2-1 kurali (3 kopya, 2 farkli medya, 1 offsite)

## 3. Failover Mekanizmasi
- TODO: Active-passive vs active-active karsilastir
- TODO: DNS failover, load balancer failover
- TODO: Database replication (sync vs async)

## 4. DR Drill Plani
- TODO: Aylik test senaryolari tanimla
- TODO: Rollback proseduru yaz
- TODO: Iletisim plani (kim kime haber verir)

## 5. Maliyet Analizi
- TODO: Active-active vs active-passive maliyet karsilastirmasi
```

**Beklenen Sonuc:** RPO ve RTO hedefleri net olmali. Backup stratejisi tanimlanmali. DR drill senaryolari yazilmali.
**Ipucu:** DR plani yazilip rafta durmamalai — duzanli drill yapmadan gercek afette plan calismaz. "Untested backup is not a backup."
:::


:::knowledge-check
## Bilgi Kontrolü

1. Monolith, microservices ve serverless arasındaki temel farklar neler?
2. Event-driven architecture'da producer ve consumer nedir?
3. CQRS'in read model ve write model'i neden ayırır?
4. Event sourcing'de state nasıl hesaplanır?
5. Hexagonal architecture'da port ve adapter ne anlama gelir?
6. DDD'de entity ve value object arasındaki fark nedir?
7. API Gateway hangi sorunları çözer?
8. ADR neden önemlidir?
:::

:::english
## Key Terms

| Term | Pronunciation | Turkish | Description |
|------|--------------|---------|-------------|
| Monolith | /ˈmɑː.nə.lɪθ/ | Monolitik | Tek parça uygulama |
| Microservice | /ˈmaɪ.kroʊ.sɝː.vɪs/ | Mikro servis | Bağımsız küçük servis |
| Serverless | /ˈsɝː.vɚ.ləs/ | Sunucusuz | Sunucu yönetimi olmadan çalıştırma |
| Event-driven | /ɪˈvent ˈdrɪv.ən/ | Olay güdümlü | Event'lerle iletişim kuran mimari |
| Aggregate | /ˈæɡ.rɪ.ɡeɪt/ | Küme | Birlikte değişen entity grubu |
| Bounded Context | /ˈbaʊn.dɪd ˈkɑːn.tekst/ | Sınırlı bağlam | Domain'in alt bölümü |
| Orchestration | /ˌɔːr.kɪˈstreɪ.ʃən/ | Orkestrasyon | Merkezi koordinasyon |
| Choreography | /ˌkɔːr.iˈɑːɡ.rə.fi/ | Koreografi | Dağıtık koordinasyon |
:::

:::external-resource
## Ek Kaynaklar

- [Martin Fowler — Microservices](https://martinfowler.com/microservices/)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Event Sourcing — Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/)
- [ADR GitHub Template](https://github.com/joelparkerhenderson/architecture-decision-record)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
:::
