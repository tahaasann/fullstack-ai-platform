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

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "Monolith, microservice ve serverless mimarileri karsilastir. Her birinin avantaj, dezavantaj ve uygun kullanim alanlarini goster. Bir startup MVP'sinden unicorn'a buyurken mimari nasil evrilir? Monolith-first yaklasimi neden tavsiye edilir? Conway's Law mimari kararlari nasil etkiler?"

**2. Pratik Uygulama:**
> "Bir e-ticaret uygulamasini Event-Driven Architecture ile tasarla. Siparis olusturma akisini event'lerle modelleyen bir sistem ciz: OrderCreated, PaymentProcessed, InventoryReserved, ShipmentScheduled. Message broker (RabbitMQ/Kafka) secimini ve her event'in handler'ini acikla. Saga pattern ile dagitik transaction yonet."
> Takip: "Simdi CQRS pattern'ini uygula: okuma ve yazma modellerini ayir. Read model icin Elasticsearch, write model icin PostgreSQL kullan. Event sourcing ile veri tutarliligini sagla."

**3. Mukemmellik Icin:**
> "500 developer'lik bir organizasyonda microservice mimarisini yonetiyorum. Service mesh (Istio), API Gateway, distributed tracing (Jaeger), centralized logging (ELK Stack), service discovery ve circuit breaker pattern'ini icereen bir platform engineering stratejisi olustur. Team Topologies ile takim yapisini mimariyle nasil hizalarim?"

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

---

## 9. Architectural Decision Records (ADR)

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

## 10. Real-World Architecture Örneği

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
## Mülakat Soruları

**S1**: "Monolith vs Microservices — yeni bir projeye hangisiyle başlarsın?"

**Beklenen cevap**: Monolith ile başlarım. Domain boundary'ler henüz net değilken microservices'e bölmek premature decomposition'dır. Monolith ile başlayıp, darboğazlar oluştuğunda veya domain net ayrıştığında modüler monolith veya microservices'e geçerim.

**S2**: "CQRS ne zaman kullanılır?"

**Beklenen cevap**: Read/write pattern'leri çok farklı olduğunda. Mesela e-ticaret'te ürün katalog okuma çok yoğun ama ürün güncelleme nadir. Read model'i denormalize edip cache'leyerek okuma performansını artırabilirim, write model'i domain logic'e odaklandırabilirim.

**S3**: "Event Sourcing'in dezavantajları neler?"

**Beklenen cevap**: Complexity artışı, event versioning zorluğu, eventual consistency, storage büyümesi, ve event schema evolution'ı yönetme zorluğu. Basit CRUD uygulamalarında gereksiz karmaşıklık ekler.
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
