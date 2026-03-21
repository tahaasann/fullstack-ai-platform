---
title: "GraphQL, gRPC ve API Dokümantasyonu"
id: mod-10-api/lesson-02
estimated_minutes: 50
order: 2
tags: ["graphql", "grpc", "openapi", "swagger", "api-testing", "apollo"]
prerequisites: ["mod-10-api/lesson-01"]
---

# GraphQL, gRPC ve API Dokümantasyonu

:::realworld
REST her zaman en iyi çözüm değildir. Facebook, 2012'de mobil uygulamalarının REST API'lerden gereğinden çok veri çektiğini (over-fetching) ve birden fazla istek yapması gerektiğini (under-fetching) fark etti. Çözüm olarak GraphQL'i geliştirdi. Google ise microservice'ler arası hızlı iletişim için gRPC'yi yarattı. Bu derste, REST'in ötesindeki API paradigmalarını ve profesyonel API dokümantasyonunu öğreneceksin.
:::

## GraphQL Nedir?

:::concept[GraphQL (İng: Graph Query Language)]
GraphQL, API'ler için bir sorgu dili ve runtime'dır. Client, tam olarak hangi veriyi istediğini belirtir ve sadece o veriyi alır.

**Türkçe karşılığı:** Graf Sorgu Dili
**Ne işe yarar:** Client'ın ihtiyacı olan veriyi tek istekte, tam olarak istediği formatta almasını sağlar
**Gerçek hayat benzetmesi:** Restoran menüsü yerine "a la carte" sipariş gibi - menüdeki set menüyü (REST) almak yerine, tam olarak istediğin yemekleri seçersin (GraphQL)
:::

:::deha-tip
Deha seviyesi geliştiriciler, "REST mi GraphQL mi?" sorusuna "duruma göre" cevabını verir. REST, basit CRUD operasyonları ve cache'lenebilir public API'ler için idealdir. GraphQL ise ilişkisel veri yapıları, farklı client'lar (web, mobil) ve karmaşık veri gereksinimleri olan uygulamalar için güçlüdür. Doğru araç, doğru problem için kullanılır.
:::

### GraphQL Schema

:::code[graphql]{title="GraphQL Schema Tanımı (SDL)"}
# Type tanımları
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  posts: [Post!]!
  createdAt: String!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
  published: Boolean!
  createdAt: String!
}

type Comment {
  id: ID!
  text: String!
  author: User!
  post: Post!
}

# Input types (mutation parametreleri için)
input CreateUserInput {
  name: String!
  email: String!
  age: Int
}

input CreatePostInput {
  title: String!
  content: String!
  published: Boolean = false
}

# Query - veri okuma
type Query {
  users(limit: Int, offset: Int): [User!]!
  user(id: ID!): User
  posts(published: Boolean): [Post!]!
  post(id: ID!): Post
}

# Mutation - veri değiştirme
type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: CreateUserInput!): User!
  deleteUser(id: ID!): Boolean!
  createPost(input: CreatePostInput!): Post!
}

# Subscription - gerçek zamanlı
type Subscription {
  postCreated: Post!
  commentAdded(postId: ID!): Comment!
}
:::

### GraphQL Queries, Mutations ve Subscriptions

:::code[graphql]{title="GraphQL Sorguları"}
# QUERY - Veri okuma
# Sadece ihtiyacın olan alanları seçersin (no over-fetching)
query {
  user(id: "123") {
    name
    email
    posts {
      title
      createdAt
    }
  }
}

# Yanıt - tam olarak istediğin yapıda gelir
# {
#   "data": {
#     "user": {
#       "name": "Ali",
#       "email": "ali@test.com",
#       "posts": [
#         { "title": "GraphQL Rehberi", "createdAt": "2024-01-15" }
#       ]
#     }
#   }
# }

# MUTATION - Veri değiştirme
mutation {
  createUser(input: {
    name: "Ayşe Demir"
    email: "ayse@test.com"
    age: 28
  }) {
    id
    name
    email
  }
}

# SUBSCRIPTION - Gerçek zamanlı veri (WebSocket)
subscription {
  postCreated {
    id
    title
    author {
      name
    }
  }
}
:::

### Apollo Server ile GraphQL API

:::code[javascript]{title="Apollo Server Kurulumu"}
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');
const express = require('express');

// Type definitions (schema)
const typeDefs = `#graphql
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
    posts: [Post!]!
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
    createPost(title: String!, content: String!, authorId: ID!): Post!
  }
`;

// Resolvers - Her alan nasıl çözümlenir?
const resolvers = {
  Query: {
    users: async (_, __, { dataSources }) => {
      return dataSources.userAPI.getAll();
    },
    user: async (_, { id }, { dataSources }) => {
      return dataSources.userAPI.getById(id);
    },
    posts: async (_, __, { dataSources }) => {
      return dataSources.postAPI.getAll();
    },
  },

  Mutation: {
    createUser: async (_, { name, email }, { dataSources }) => {
      return dataSources.userAPI.create({ name, email });
    },
    createPost: async (_, args, { dataSources }) => {
      return dataSources.postAPI.create(args);
    },
  },

  // İlişkisel çözümleme
  User: {
    posts: async (user, _, { dataSources }) => {
      return dataSources.postAPI.getByAuthor(user.id);
    },
  },

  Post: {
    author: async (post, _, { dataSources }) => {
      return dataSources.userAPI.getById(post.authorId);
    },
  },
};

// Server oluşturma
async function startServer() {
  const app = express();
  const server = new ApolloServer({ typeDefs, resolvers });

  await server.start();

  app.use('/graphql', express.json(), expressMiddleware(server, {
    context: async ({ req }) => ({
      token: req.headers.authorization,
      dataSources: {
        userAPI: new UserAPI(),
        postAPI: new PostAPI(),
      },
    }),
  }));

  app.listen(4000, () => {
    console.log('GraphQL API: http://localhost:4000/graphql');
  });
}

startServer();
:::

### REST vs GraphQL

:::comparison
| Özellik | REST | GraphQL |
|---------|------|---------|
| **Veri alma** | Endpoint başına sabit yapı | Client istediği alanları seçer |
| **Over-fetching** | Sık yaşanır | Yok (sadece istenen alanlar) |
| **Under-fetching** | Birden fazla istek gerekir | Tek istekte ilişkisel veri |
| **Endpoint sayısı** | Kaynak başına endpoint | Tek endpoint (/graphql) |
| **Caching** | HTTP caching kolay (GET URL) | Karmaşık (POST, Apollo Client cache) |
| **Dosya upload** | Kolay (multipart/form-data) | Karmaşık (ek kütüphane gerekli) |
| **Öğrenme eğrisi** | Düşük | Orta-Yüksek |
| **Gerçek zamanlı** | WebSocket/SSE (ayrı impl.) | Subscriptions (built-in) |
| **Hata yönetimi** | HTTP status codes | 200 + errors array |
| **Araçlar** | Postman, curl | GraphQL Playground, Apollo Studio |

**Ne zaman REST?**
- Public API (basit, cache'lenebilir)
- Dosya upload/download ağırlıklı
- Basit CRUD operasyonları
- Microservice'ler arası iletişim

**Ne zaman GraphQL?**
- Farklı client'lar (web, mobil, tablet) farklı veri istiyor
- Derin ilişkisel veri yapıları
- Tek sayfada birden fazla kaynaktan veri gerekiyor
- Hızlı iterasyon ve esneklik öncelikli
:::

:::beginner-mistake
Yaygın hata: "GraphQL REST'ten daha iyi, her yerde kullanalım" demek. GraphQL, over-fetching ve under-fetching sorunlarını çözer ama kendi karmaşıklıklarını getirir: N+1 query problemi, cache zorlukları, dosya upload karmaşıklığı ve daha dik öğrenme eğrisi. Doğru araç doğru iş içindir.
:::

## gRPC Basics

:::concept[gRPC (İng: Google Remote Procedure Call)]
gRPC, Google tarafından geliştirilen yüksek performanslı bir RPC framework'üdür. Protocol Buffers (protobuf) ile binary serialization kullanır.

**Türkçe karşılığı:** Google Uzak Prosedür Çağrısı
**Ne işe yarar:** Microservice'ler arası düşük gecikme süreli, yüksek performanslı iletişim sağlar
**Gerçek hayat benzetmesi:** REST mektup göndermek (okunabilir, yavaş) ise, gRPC telgraf göndermek (kısa, hızlı, kodlanmış) gibidir
:::

:::code[protobuf]{title="Protocol Buffers Tanımı (.proto dosyası)"}
syntax = "proto3";

package user;

// Service tanımı
service UserService {
  // Unary RPC - tek istek, tek yanıt
  rpc GetUser (GetUserRequest) returns (User);
  rpc CreateUser (CreateUserRequest) returns (User);

  // Server streaming - tek istek, çoklu yanıt
  rpc ListUsers (ListUsersRequest) returns (stream User);

  // Client streaming - çoklu istek, tek yanıt
  rpc UploadUsers (stream CreateUserRequest) returns (UploadResponse);

  // Bidirectional streaming - çoklu istek, çoklu yanıt
  rpc Chat (stream ChatMessage) returns (stream ChatMessage);
}

// Message tanımları
message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
  int32 age = 4;
  repeated string tags = 5;
}

message GetUserRequest {
  int32 id = 1;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
  int32 age = 3;
}

message ListUsersRequest {
  int32 page = 1;
  int32 limit = 2;
}

message UploadResponse {
  int32 count = 1;
  bool success = 2;
}
:::

:::code[text]{title="REST vs GraphQL vs gRPC Karşılaştırması"}
┌─────────────┬──────────────┬──────────────┬──────────────┐
│  Özellik    │    REST      │   GraphQL    │    gRPC      │
├─────────────┼──────────────┼──────────────┼──────────────┤
│ Format      │ JSON (text)  │ JSON (text)  │ Protobuf     │
│             │              │              │ (binary)     │
│ Transport   │ HTTP/1.1     │ HTTP/1.1     │ HTTP/2       │
│ Performans  │ Orta         │ Orta         │ Çok yüksek   │
│ Streaming   │ Yok/SSE      │ Subscriptions│ 4 tür stream │
│ Tarayıcı    │ Tam destek   │ Tam destek   │ grpc-web ile │
│ Contract    │ OpenAPI      │ SDL Schema   │ .proto dosya │
│ Kullanım    │ Public API   │ Frontend API │ Microservice │
│             │ Web/Mobil    │ BFF          │ dahili       │
└─────────────┴──────────────┴──────────────┴──────────────┘
:::

:::tip
gRPC genellikle microservice'ler arası dahili iletişim için kullanılır. Public-facing API'ler için REST veya GraphQL daha uygun. Ancak grpc-web ile tarayıcıdan da gRPC kullanılabilir. Büyük şirketler genellikle dahili = gRPC, harici = REST/GraphQL şeklinde hybrid mimari kullanır.
:::

## OpenAPI / Swagger Dokümantasyonu

:::concept[OpenAPI Specification (İng: OpenAPI Specification)]
OpenAPI (eski adıyla Swagger), RESTful API'leri tanımlamak için standart bir spesifikasyondur. API'nin endpoint'lerini, parametrelerini, yanıtlarını ve güvenlik şemalarını YAML veya JSON formatında tanımlar.

**Türkçe karşılığı:** Açık API Spesifikasyonu
**Ne işe yarar:** API dokümantasyonunu otomatik oluşturur, client SDK'ları generate eder, API test'i kolaylaştırır
**Gerçek hayat benzetmesi:** Bir binanın mimari planı gibi - bina yapılmadan önce tüm odaların, kapıların ve pencerelerin yerini gösterir
:::

:::code[yaml]{title="OpenAPI 3.0 Spec Örneği"}
openapi: 3.0.3
info:
  title: My API
  description: E-ticaret API dokümantasyonu
  version: 1.0.0

servers:
  - url: https://api.myapp.com/v1
    description: Production
  - url: http://localhost:3000/api/v1
    description: Development

paths:
  /users:
    get:
      summary: Tüm kullanıcıları listele
      tags: [Users]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Başarılı
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: Yeni kullanıcı oluştur
      tags: [Users]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
      responses:
        '201':
          description: Kullanıcı oluşturuldu
        '400':
          description: Validation hatası
        '409':
          description: Email zaten kayıtlı

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
    CreateUser:
      type: object
      required: [name, email, password]
      properties:
        name:
          type: string
          minLength: 2
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 8
    Pagination:
      type: object
      properties:
        currentPage:
          type: integer
        totalPages:
          type: integer
        totalItems:
          type: integer

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
:::

:::code[javascript]{title="Express'te Swagger UI Kurulumu"}
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.0.3',
    info: {
      title: 'My API',
      version: '1.0.0',
    },
  },
  apis: ['./src/routes/*.js'], // JSDoc comment'larından oku
};

const specs = swaggerJsdoc(options);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

// Route'larda JSDoc ile dokümantasyon
/**
 * @openapi
 * /api/v1/users:
 *   get:
 *     summary: Tüm kullanıcıları listele
 *     tags: [Users]
 *     responses:
 *       200:
 *         description: Başarılı
 */
router.get('/users', userController.getAll);
:::

## API Testing Tools

:::comparison
| Araç | Tür | Fiyat | Öne Çıkan Özellik |
|------|-----|-------|-------------------|
| **Postman** | GUI + CLI (Newman) | Freemium | En yaygın, collection/environment, test script |
| **Bruno** | GUI (offline-first) | Açık kaynak | Git-friendly, dosya tabanlı, privacy-focused |
| **Hoppscotch** | Web-based | Açık kaynak | Tarayıcıdan kullan, PWA, hızlı |
| **Thunder Client** | VS Code extension | Freemium | VS Code içinden test, lightweight |
| **Insomnia** | GUI | Freemium | GraphQL desteği güçlü, temiz arayüz |
| **curl** | CLI | Ücretsiz | Her yerde var, script'lenebilir, CI/CD |
| **HTTPie** | CLI | Ücretsiz | curl alternatifi, insan dostu söz dizimi |

**Tavsiye:** Postman veya Bruno ile başla. Bruno açık kaynak ve git-friendly olması nedeniyle takım çalışması için idealdir. curl'ü CI/CD pipeline'larında ve script'lerde kullan.
:::

:::code[bash]{title="curl ile API Test Örnekleri"}
# GET isteği
curl -X GET http://localhost:3000/api/v1/users \
  -H "Authorization: Bearer eyJhbG..." \
  -H "Accept: application/json"

# POST isteği (JSON body)
curl -X POST http://localhost:3000/api/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbG..." \
  -d '{"name": "Ali", "email": "ali@test.com", "password": "Secure123!"}'

# PUT isteği
curl -X PUT http://localhost:3000/api/v1/users/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Ali Yılmaz", "email": "ali@test.com"}'

# DELETE isteği
curl -X DELETE http://localhost:3000/api/v1/users/123 \
  -H "Authorization: Bearer eyJhbG..."

# Response header'larını göster
curl -I http://localhost:3000/api/v1/users

# Verbose mode (debug için)
curl -v http://localhost:3000/api/v1/users
:::

## Pratik Uygulama

:::exercise
### Alistirma 1: GraphQL Schema ve Resolver (Kolay)

Apollo Server ile User ve Post type'larini tanimlayip Query ve Mutation resolver'lari yaz.

```javascript
const { ApolloServer } = require("@apollo/server");
const { startStandaloneServer } = require("@apollo/server/standalone");

// TODO: Schema tanimla
const typeDefs = `#graphql
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
    createdAt: String!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
    posts: [Post!]!
    post(id: ID!): Post
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
    createPost(title: String!, content: String!, authorId: ID!): Post!
    # TODO: updatePost ve deletePost mutation'lari ekle
  }
`;

// Mock data
let users = [{ id: "1", name: "Ahmet", email: "ahmet@test.com" }];
let posts = [{ id: "1", title: "Ilk Yazi", content: "...", authorId: "1", createdAt: new Date().toISOString() }];

// TODO: Resolver'lari yaz
const resolvers = {
  Query: {
    users: () => users,
    // TODO: user, posts, post resolver'lari
  },
  Mutation: {
    // TODO: createUser, createPost resolver'lari
  },
  // TODO: Nested resolver — User.posts ve Post.author
  User: {
    posts: (parent) => posts.filter(p => p.authorId === parent.id),
  },
};

const server = new ApolloServer({ typeDefs, resolvers });
startStandaloneServer(server, { listen: { port: 4000 } })
  .then(({ url }) => console.log(`GraphQL server: ${url}`));
```

**Beklenen Sonuc:** `http://localhost:4000` adresinde Apollo Sandbox acilmali. Query ile kullanicilari ve postlari listeleyebilmeli. Mutation ile yeni kayit ekleyebilmeli.
**Ipucu:** Nested resolver'larda `parent` parametresi ust objeyi temsil eder. `User.posts` resolver'i otomatik cagrilir.

---

### Alistirma 2: Swagger/OpenAPI Dokumantasyonu (Orta)

Express API'ne Swagger dokumantasyonu ekle ve interaktif API explorer olustur.

```javascript
const swaggerJsdoc = require("swagger-jsdoc");
const swaggerUi = require("swagger-ui-express");

const swaggerOptions = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "E-Ticaret API",
      version: "1.0.0",
      description: "E-Ticaret REST API dokumantasyonu",
    },
    servers: [{ url: "http://localhost:3000" }],
  },
  apis: ["./routes/*.js"], // JSDoc yorumlarini tara
};

const specs = swaggerJsdoc(swaggerOptions);
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(specs));

// TODO: En az 3 endpoint'i dokumante et
/**
 * @openapi
 * /api/v1/products:
 *   get:
 *     summary: Tum urunleri listele
 *     tags: [Products]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema: { type: integer, default: 1 }
 *       - in: query
 *         name: limit
 *         schema: { type: integer, default: 20 }
 *     responses:
 *       200:
 *         description: Urun listesi
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 data: { type: array, items: { $ref: '#/components/schemas/Product' } }
 *                 pagination: { $ref: '#/components/schemas/Pagination' }
 */

// TODO: POST /api/v1/products dokumantasyonu (request body ile)
// TODO: GET /api/v1/products/:id dokumantasyonu (path parameter ile)
// TODO: components/schemas altinda Product ve Pagination schemalarini tanimla
```

**Beklenen Sonuc:** `/api-docs` adresinden Swagger UI acilmali. En az 3 endpoint interaktif olarak test edilebilmeli. Schema tanimlari dogru olmali.
**Ipucu:** Swagger JSDoc @openapi yorumlari ile route dosyalarindaki endpoint'leri otomatik tarar.

---

### Alistirma 3: API Testing Koleksiyonu (Zor)

curl, Postman veya Bruno ile kapsamli bir API test koleksiyonu olustur.

```bash
# TODO: Asagidaki test senaryolarini curl ile yaz

# 1. CRUD islemleri
# Urun olustur
curl -X POST http://localhost:3000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","price":15000,"category":"electronics"}'

# Urunleri listele (filtreleme ile)
curl "http://localhost:3000/api/v1/products?category=electronics&sort=-price&page=1&limit=5"

# Urun guncelle
curl -X PUT http://localhost:3000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Gaming Laptop","price":20000}'

# Urun sil
curl -X DELETE http://localhost:3000/api/v1/products/1

# 2. Hata senaryolari
# TODO: 400 — Gecersiz body ile POST (name eksik)
# TODO: 404 — Olmayan urun ID'si ile GET
# TODO: 401 — Token olmadan korunmali endpoint'e erisim
# TODO: 422 — Gecersiz fiyat (negatif sayi) ile POST

# 3. Edge case'ler
# TODO: Pagination — son sayfadan sonraki sayfa
# TODO: Bos arama sonucu
# TODO: Cok buyuk limit degeri (limit=99999)

# GOREV: Her curl komutunun beklenen status code'unu ve response body'sini belirt
# Bir test.sh script'i olarak kaydet ve calistir
```

**Beklenen Sonuc:** En az 10 farkli test senaryosu yazilmis olmali. Her senaryo icin beklenen status code ve response body belirtilmeli. Script olarak kaydedilip otomatik calistirilabilmeli.
**Ipucu:** `curl -w "\n%{http_code}\n"` ile status code'u goster. `-s` flag'i ile progress bar'i gizle. `jq` ile JSON response'u formatla.
:::

:::knowledge-check
type: multiple_choice
question: "GraphQL'in REST'e göre çözdüğü en temel problem hangisidir?"
options:
  - "Güvenlik açıkları"
  - "Over-fetching ve under-fetching"
  - "Veritabanı performansı"
  - "Dosya yükleme"
correct: 1
explanation: "Over-fetching: REST endpoint'i ihtiyacından fazla veri döndürür (tüm user alanları gelir ama sadece name ve email lazım). Under-fetching: Bir sayfadaki veriyi almak için birden fazla REST isteği gerekir (user + posts + comments = 3 istek). GraphQL'de client tam olarak hangi alanları istediğini belirtir ve tek istekte ilişkisel veriyi alır."
:::

:::knowledge-check
type: multiple_choice
question: "gRPC'nin REST ve GraphQL'den daha hızlı olmasının ana nedeni nedir?"
options:
  - "Daha iyi programlama dili kullanması"
  - "HTTP/2 ve Protocol Buffers (binary serialization) kullanması"
  - "Daha az endpoint'e sahip olması"
  - "Cache mekanizması daha iyi olması"
correct: 1
explanation: "gRPC, HTTP/2 üzerinde çalışır (multiplexing, header compression) ve Protocol Buffers ile binary serialization kullanır. JSON text formatı yerine binary format, hem daha küçük payload hem daha hızlı serialize/deserialize sağlar. Ayrıca HTTP/2'nin streaming desteği ile 4 farklı iletişim modeli sunar."
:::

:::ai-guidance
## Bu Derste AI ile Ogren

**Onerilen Model:** Claude Opus 4.6 (derin anlayis icin) veya Sonnet 4.5 (hizli sorular icin)

### Prompt Ornekleri

**1. Derinlemesine Anla:**
> "GraphQL'in N+1 query problemini bir blog uygulamasi ornegi ile acikla. 10 post ve her post'un author'unu cektigimde kac SQL sorgusu calisir? DataLoader pattern bu sorunu nasil cozer? Batch loading mekanizmasini adim adim goster."

**2. Pratik Uygulama:**
> "Apollo Server ile bir GraphQL API olustur: User ve Post type'lari, Query (users, posts, user by ID), Mutation (createUser, createPost) ve iliskisel resolver'lar (User.posts, Post.author). Context'te authentication bilgisi tasi. Input validation ve error handling ekle."
> Takip: "Simdi bu API icin OpenAPI/Swagger dokumantasyonu olustur. swagger-jsdoc ile JSDoc comment'larindan otomatik spec uret ve /api-docs adresinde Swagger UI sun."

**3. Mukemmellik Icin:**
> "Bir mikroservis mimarisinde REST, GraphQL ve gRPC'yi birlikte nasil kullanirim? Public API icin REST, BFF (Backend for Frontend) icin GraphQL, dahili servisler arasi iletisim icin gRPC. Apollo Federation ile birden fazla GraphQL subgraph'i nasil birlestiririm? Bu hybrid mimarinin trade-off'larini analiz et."

### Pair Programming Ipucu
GraphQL schema tasarlarken AI'a schema'ni goster ve sor: "Bu GraphQL schema'sinda N+1 sorgu riski var mi? Resolver'larda DataLoader kullanmam gereken yerler neresi? Query complexity limiti nasil eklerim? Introspection'i production'da kapatmali miyim?"
:::

:::interview
## Mulakat Sorulari

**Soru 1: GraphQL ve REST arasindaki farklar nelerdir? Ne zaman hangisini secersiniz?**
- **Junior cevabi:** GraphQL tek endpoint kullanir ve client istedigi veriyi secer, REST birden fazla endpoint kullanir.
- **Senior cevabi:** GraphQL avantajlari: over-fetching/under-fetching yok (client ihtiyaci kadar veri alir), strongly typed schema, introspection ile self-documenting, tek request'te iliiskili veriler alinir. Dezavantajlari: caching zorlugu (HTTP cache kullanamaz), N+1 query problemi (DataLoader ile cozulur), query complexity kontrolu gerekir (depth limiting, cost analysis). REST tercih: basit CRUD, public API, HTTP caching onemli ise. GraphQL tercih: kompleks iliiskili veri, mobil uygulamalar (bant genisligi onemli), cok farkli client tipleri. Facebook, GitHub, Shopify GraphQL kullanir.

**Soru 2: GraphQL'de N+1 query problemi nedir ve nasil cozulur?**
- **Junior cevabi:** Her alt sorgu icin ayri veritabani sorgulari yapilmasidir, DataLoader ile cozulur.
- **Senior cevabi:** N+1 problemi: users listesi icin 1 query + her user'in posts'lari icin N ayri query yapilir. DataLoader (Facebook'un kutuphanesi) batch ve cache mekanizmasi saglar: ayni tick'teki tum user ID'lerini toplar ve tek bir `WHERE id IN (...)` sorgusuyla ceker. Per-request DataLoader instance'i olusturulur (request bazli cache). Ayrica: query depth limiting ile recursive sorular engellenir, query cost analysis ile pahali sorgulara limit konur, persisted queries ile sadece izin verilen sorgular calistirilir. APQ (Automatic Persisted Queries) bandwidth tasarrufu saglar.
:::

:::must-note
- GraphQL 3 operasyon tipi: Query (oku), Mutation (değiştir), Subscription (gerçek zamanlı)
- GraphQL avantajları: over-fetching yok, under-fetching yok, tek endpoint, strong typing
- GraphQL dezavantajları: cache zorluğu, N+1 query problemi, dosya upload karmaşıklığı, öğrenme eğrisi
- Apollo Server: Node.js için en popüler GraphQL framework, Express ile entegre
- Resolver: GraphQL'de her alanın nasıl çözümleneceğini tanımlayan fonksiyon
- gRPC: HTTP/2 + Protocol Buffers = yüksek performans, microservice'ler arası ideal
- gRPC 4 iletişim modeli: Unary, Server streaming, Client streaming, Bidirectional streaming
- Protocol Buffers: .proto dosyasında schema tanımla, otomatik kod generate et
- OpenAPI/Swagger: REST API'leri YAML/JSON ile tanımla, otomatik dokümantasyon üret
- swagger-jsdoc: JSDoc comment'larından OpenAPI spec oluşturur
- swagger-ui-express: Swagger UI'ı Express uygulamasına entegre eder
- API testing araçları: Postman (en yaygın), Bruno (git-friendly), Hoppscotch (web-based), curl (CI/CD)
- Hybrid mimari: Public API = REST/GraphQL, Dahili microservice = gRPC
- GraphQL introspection ile API keşfedilebilir (production'da kapatılmalı)
:::

:::senior-learns
Bir Senior Developer veya CTO, GraphQL ve API ekosistemini öğrenirken şu yaklaşımı benimser:

1. **N+1 query problemini çözer** - GraphQL'in en büyük performans tuzağı olan N+1 sorgu problemini DataLoader pattern ile çözer. Batch loading ile veritabanı sorgularını optimize eder. Query complexity analysis yaparak kötü niyetli derinlemesine sorguları engeller (depth limiting, cost analysis).
2. **Schema-first vs Code-first yaklaşımını bilinçli seçer** - Schema-first (SDL yazıp resolver implement et) ile Code-first (TypeGraphQL, Nexus gibi kütüphanelerle koddan schema üret) arasındaki trade-off'ları değerlendirir. TypeScript projelerinde code-first yaklaşımı type safety sağlar.
3. **Federation ve microservice GraphQL mimarisi kurar** - Apollo Federation ile birden fazla GraphQL servisini tek bir gateway altında birleştirir. Her microservice kendi schema'sını yönetir (subgraph). Gateway, query planning ve execution yapar. Schema stitching vs federation trade-off'larını bilir.
4. **API Gateway ve BFF (Backend for Frontend) pattern uygular** - Farklı client'lar (web, mobil, IoT) için farklı BFF katmanları oluşturur. Her BFF, client'ın ihtiyaçlarına göre optimize edilmiş API sunar. API Gateway ile cross-cutting concern'leri merkezi yönetir.
5. **Contract testing ve API evolution yönetir** - Consumer-driven contract testing (Pact) ile API değişikliklerinin tüm client'larla uyumlu olduğunu doğrular. Schema registry ile GraphQL schema değişikliklerini versiyon kontrollü yönetir. Breaking change detection otomatize eder.
6. **gRPC'yi production'da kullanır** - Service mesh (Istio, Linkerd) ile gRPC traffic management yapar. Load balancing, circuit breaking, retry policy'leri konfigüre eder. Protobuf schema evolution kurallarını (backward/forward compatibility) uygular. gRPC-Gateway ile REST ve gRPC'yi birlikte sunar.

**Profesyonel Mindset:** "API paradigması seçimi, teknik bir karar olduğu kadar organizasyonel bir karardır. REST basit ve herkesin bildiği standarttır. GraphQL, frontend ekibine esneklik verir ama backend ekibinin schema ve resolver yönetimini doğru yapması gerekir. gRPC ise dahili iletişimde performans kazanır ama ekibin protobuf ve HTTP/2 bilgisi gerektirir. Doğru seçim, ekibin yetkinlikleri ve projenin gereksinimleriyle uyumlu olandır."
:::

:::english
**Teknik İngilizce - Bu Dersteki Terimler:**

1. **Schema** (skiː-mə) → Şema / Yapı tanımı
   *"The GraphQL schema defines the types, queries, and mutations available in the API."*

2. **Resolver** (rɪ-zɒl-vər) → Çözümleyici
   *"Each field in a GraphQL schema is backed by a resolver function that fetches the data."*

3. **Subscription** (səb-skrɪp-ʃən) → Abonelik
   *"GraphQL subscriptions use WebSocket connections for real-time data updates."*

4. **Protocol Buffers** (proʊ-tə-kɒl bʌf-ərz) → Protokol Tamponları
   *"Protocol Buffers provide efficient binary serialization for gRPC communication."*

5. **Specification** (spɛs-ɪ-fɪ-keɪ-ʃən) → Spesifikasyon / Belirtim
   *"The OpenAPI Specification describes the structure and behavior of a REST API."*

**Okuma Egzersizi:** GraphQL resmi dokümantasyonunda "Introduction" sayfasını oku: https://graphql.org/learn/

**Yazma Pratiği:** Aşağıdaki commit mesajını İngilizce yaz: "GraphQL API ve Swagger dokümantasyonu eklendi"
→ Örnek: `feat: add GraphQL API with Apollo Server and Swagger documentation`
:::

:::external-resource
- 📖 **GraphQL Docs:** graphql.org/learn (resmi öğrenme rehberi, ücretsiz)
- 📖 **Apollo GraphQL:** apollographql.com/docs (Apollo Server/Client, ücretsiz)
- 📖 **gRPC Docs:** grpc.io/docs (resmi dokümantasyon, ücretsiz)
- 📖 **Swagger Editor:** editor.swagger.io (online OpenAPI editor, ücretsiz)
- 📺 **Ben Awad:** "GraphQL + TypeScript" serisi (YouTube, ücretsiz)
- 📖 **Bruno:** usebruno.com (git-friendly API client, açık kaynak)
:::
