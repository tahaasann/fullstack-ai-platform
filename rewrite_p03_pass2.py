#!/usr/bin/env python3
"""Second pass: fix remaining large code dumps in project-03.json."""

import json

def main():
    with open('content/projects/project-03.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    milestones = data['milestones']

    # ==========================================
    # M1 Step 2: MongoDB Model Tanımları
    # Substeps 2.4 (21 lines), 2.7 (22 lines), 2.8 (23 lines)
    # Break 2.4, 2.7, 2.8 into smaller pieces
    # ==========================================
    m1 = milestones[0]
    m1_step2 = m1['steps'][1]
    m1_step2['substeps'] = [
        {
            "order": "2.1",
            "action": "server/src/models/user.model.ts dosyasını aç — İSKELET yaz",
            "type": "code_write",
            "file": "server/src/models/user.model.ts",
            "code": "export {};  // placeholder",
            "why": "Her zaman iskelet ile başlıyoruz. Dosyayı oluşturup TypeScript'in tanımasını sağlıyoruz."
        },
        {
            "order": "2.2",
            "action": "ÜSTE ÇIK — mongoose import'unu ekle",
            "type": "code_write",
            "file": "server/src/models/user.model.ts",
            "code": "import mongoose, { Schema, Document } from 'mongoose';",
            "why": "Mongoose'u kullanacağız çünkü şimdi schema tanımlayacağız. Import'u KULLANMADAN ÖNCE ekliyoruz."
        },
        {
            "order": "2.3",
            "action": "Import'un altına — IUser interface'ini tanımla",
            "type": "code_add",
            "file": "server/src/models/user.model.ts",
            "position": "after:import",
            "code": "\nexport interface IUser extends Document {\n  email: string;\n  name: string;\n  password: string;\n  avatar?: string;\n  isOnline: boolean;\n  lastSeen: Date;\n}",
            "why": "TypeScript interface ile User modelinin şemasını tanımlıyoruz. Document'ı extend ediyoruz çünkü Mongoose doküman metodlarına erişmek istiyoruz."
        },
        {
            "order": "2.4",
            "action": "Interface'in altına — userSchema tanımla",
            "type": "code_add",
            "file": "server/src/models/user.model.ts",
            "position": "after:interface",
            "code": "\nconst userSchema = new Schema<IUser>({\n  email: { type: String, required: true, unique: true, lowercase: true },\n  name: { type: String, required: true, minlength: 2 },\n  password: { type: String, required: true, select: false },\n  avatar: String,\n  isOnline: { type: Boolean, default: false },\n  lastSeen: { type: Date, default: Date.now },\n}, { timestamps: true });",
            "why": "select: false ile password varsayılan sorgularda dönmez — güvenlik için ŞART. timestamps: true otomatik createdAt ve updatedAt ekler."
        },
        {
            "order": "2.5",
            "action": "Schema'nın altına — model export'unu ekle",
            "type": "code_add",
            "file": "server/src/models/user.model.ts",
            "position": "after:schema",
            "code": "\nexport const User = mongoose.model<IUser>('User', userSchema);",
            "why": "Schema'yı Mongoose model'ine çeviriyoruz. IUser generic tipi ile model metodları TypeScript tip güvenliğine sahip olur."
        },
        {
            "order": "2.6",
            "action": "BAŞKA DOSYAYA GEÇ — server/src/models/conversation.model.ts aç — import yaz",
            "type": "code_write",
            "file": "server/src/models/conversation.model.ts",
            "code": "import mongoose, { Schema, Document } from 'mongoose';",
            "why": "Az önce user.model.ts'de mongoose import pattern'ını öğrendik. Aynı pattern'ı burada da kullanıyoruz."
        },
        {
            "order": "2.7",
            "action": "Import'un altına — IConversation interface'ini tanımla",
            "type": "code_add",
            "file": "server/src/models/conversation.model.ts",
            "position": "after:import",
            "code": "\nexport interface IConversation extends Document {\n  type: 'direct' | 'group';\n  name?: string;\n  participants: mongoose.Types.ObjectId[];\n  lastMessage?: mongoose.Types.ObjectId;\n  lastActivity: Date;\n}",
            "why": "type: 'direct' | 'group' ile birebir ve grup sohbetlerini ayırıyoruz. participants ObjectId dizisi — User modeline referans veriyor."
        },
        {
            "order": "2.8",
            "action": "Interface'in altına — conversationSchema'yı tanımla",
            "type": "code_add",
            "file": "server/src/models/conversation.model.ts",
            "position": "after:interface",
            "code": "\nconst conversationSchema = new Schema<IConversation>({\n  type: { type: String, enum: ['direct', 'group'], required: true },\n  name: String,\n  participants: [{ type: Schema.Types.ObjectId, ref: 'User', required: true }],\n  lastMessage: { type: Schema.Types.ObjectId, ref: 'Message' },\n  lastActivity: { type: Date, default: Date.now },\n}, { timestamps: true });",
            "why": "enum ile type sadece 'direct' veya 'group' olabilir. ref: 'User' ile participants alanı User modeline REFERANS verir — populate ile doldurulabilir."
        },
        {
            "order": "2.9",
            "action": "Schema'nın altına — index'leri ve model export'unu ekle",
            "type": "code_add",
            "file": "server/src/models/conversation.model.ts",
            "position": "after:schema",
            "code": "\nconversationSchema.index({ participants: 1 });\nconversationSchema.index({ lastActivity: -1 });\n\nexport const Conversation = mongoose.model<IConversation>('Conversation', conversationSchema);",
            "why": "Index'leri AYRI adımda ekliyoruz çünkü schema yazıldıktan sonra 'bu alanları nasıl sorgulayacağım?' diye düşünüyoruz. participants index'i kullanıcının konuşmalarını hızlı bulmayı sağlar."
        },
        {
            "order": "2.10",
            "action": "BAŞKA DOSYAYA GEÇ — server/src/models/message.model.ts aç — import ve interface yaz",
            "type": "code_write",
            "file": "server/src/models/message.model.ts",
            "code": "import mongoose, { Schema, Document } from 'mongoose';\n\nexport interface IMessage extends Document {\n  conversationId: mongoose.Types.ObjectId;\n  sender: mongoose.Types.ObjectId;\n  content: string;\n  type: 'text' | 'image' | 'file' | 'ai_response';\n  readBy: mongoose.Types.ObjectId[];\n  metadata?: Record<string, any>;\n}",
            "why": "Artık pattern'ı biliyoruz — import ve interface'i birlikte yazabiliyoruz. 'ai_response' tipi M4'te AI asistan için kullanılacak."
        },
        {
            "order": "2.11",
            "action": "Interface'in altına — messageSchema'yı tanımla",
            "type": "code_add",
            "file": "server/src/models/message.model.ts",
            "position": "after:interface",
            "code": "\nconst messageSchema = new Schema<IMessage>({\n  conversationId: { type: Schema.Types.ObjectId, ref: 'Conversation', required: true, index: true },\n  sender: { type: Schema.Types.ObjectId, ref: 'User', required: true },\n  content: { type: String, required: true },\n  type: { type: String, enum: ['text', 'image', 'file', 'ai_response'], default: 'text' },\n  readBy: [{ type: Schema.Types.ObjectId, ref: 'User' }],\n  metadata: Schema.Types.Mixed,\n}, { timestamps: true });",
            "why": "index: true ile conversationId alanında indeks oluşturulur — mesaj sorgulama hızlanır. Schema.Types.Mixed farklı mesaj tiplerinin metadata'sını esnek şekilde saklar."
        },
        {
            "order": "2.12",
            "action": "Schema'nın altına — compound index ve model export ekle",
            "type": "code_add",
            "file": "server/src/models/message.model.ts",
            "position": "after:schema",
            "code": "\nmessageSchema.index({ conversationId: 1, createdAt: -1 });\n\nexport const Message = mongoose.model<IMessage>('Message', messageSchema);",
            "why": "Compound index { conversationId: 1, createdAt: -1 } bir konuşmanın mesajlarını tarih sırasına göre ÇOK hızlı sorgular. M2'deki cursor-based pagination bu index'e DAYANIR."
        },
        {
            "order": "2.13",
            "action": "Terminale geç — TypeScript derleme kontrolü yap",
            "type": "terminal",
            "command": "cd server && pnpm dlx tsc --noEmit",
            "expected_output": "Hata olmamalı",
            "why": "Az önce yazdığımız 3 model dosyasının TypeScript hatası olmadığını doğruluyoruz. Bu alışkanlık her dosya yazdıktan sonra yapılmalı."
        },
        {
            "order": "2.14",
            "action": "Model'lerin hatasız derlenmesini doğrula",
            "type": "validate",
            "validation": "tsc --noEmit komutu hata vermemeli. 3 model dosyası oluşturulmuş olmalı: user.model.ts, conversation.model.ts, message.model.ts",
            "why": "TypeScript derleme kontrolü, tip hatalarını erken yakalamak için önemlidir."
        }
    ]

    # ==========================================
    # M3 Step 2: Chat Page — substep 2.4 dumps 46 lines
    # ==========================================
    m3 = milestones[2]
    m3_step2 = m3['steps'][1]
    m3_step2['substeps'] = [
        {
            "order": "2.1",
            "action": "client/src/lib/api.ts dosyasını aç — İSKELET axios instance yaz",
            "type": "code_write",
            "file": "client/src/lib/api.ts",
            "code": "import axios from 'axios';\n\nexport const api = axios.create({\n  baseURL: (import.meta.env.VITE_API_URL || 'http://localhost:3001') + '/api',\n  headers: { 'Content-Type': 'application/json' },\n});",
            "why": "baseURL ile her istekte tam URL yazmak zorunda kalmayız. Vite environment variable'ı ile farklı ortamlarda farklı URL kullanılabilir."
        },
        {
            "order": "2.2",
            "action": "api instance'ının altına — interceptor ekle (otomatik JWT token)",
            "type": "code_add",
            "file": "client/src/lib/api.ts",
            "position": "after:api",
            "code": "\napi.interceptors.request.use((config) => {\n  const token = localStorage.getItem('token');\n  if (token) {\n    config.headers.Authorization = `Bearer ${token}`;\n  }\n  return config;\n});",
            "why": "Interceptor her istekte OTOMATİK olarak JWT token'ı header'a ekler — M2 4.5'te yazdığımız auth middleware bu token'ı kontrol edecek."
        },
        {
            "order": "2.3",
            "action": "BAŞKA DOSYAYA GEÇ — client/src/pages/chat.tsx aç — İSKELET component yaz",
            "type": "code_write",
            "file": "client/src/pages/chat.tsx",
            "code": "export function ChatPage() {\n  return (\n    <div className=\"flex h-screen\">\n      <div className=\"w-80 border-r border-gray-800\">\n        <p className=\"p-4 text-gray-400\">Konuşmalar</p>\n      </div>\n      <div className=\"flex-1 flex items-center justify-center text-gray-400\">\n        Bir konuşma seçin\n      </div>\n    </div>\n  );\n}",
            "why": "İskelet layout ile başlıyoruz — master-detail pattern. Sol panel sabit genişlik (w-80 = 320px), sağ panel kalan alanı kaplar (flex-1)."
        },
        {
            "order": "2.4",
            "action": "ÜSTE ÇIK — useEffect import'unu ekle",
            "type": "code_add",
            "file": "client/src/pages/chat.tsx",
            "position": "top",
            "code": "import { useEffect } from 'react';",
            "why": "useEffect ile konuşma listesini yükleyip socket event'lerini dinleyeceğiz."
        },
        {
            "order": "2.5",
            "action": "ÜSTE ÇIK — store ve api import'larını ekle",
            "type": "code_add",
            "file": "client/src/pages/chat.tsx",
            "position": "after:react",
            "code": "import { useSocketStore } from '../stores/socket-store';\nimport { useChatStore } from '../stores/chat-store';\nimport { api } from '../lib/api';",
            "why": "1.5-1.9'da yazdığımız socket store, 1.12-1.15'teki chat store ve 2.1'deki api helper'ı import ediyoruz."
        },
        {
            "order": "2.6",
            "action": "GERİ DÖN component içine — store bağlantılarını ekle",
            "type": "code_add",
            "file": "client/src/pages/chat.tsx",
            "position": "inside:component",
            "code": "  const { socket } = useSocketStore();\n  const { activeConversation, setConversations, addMessage, setTyping } = useChatStore();",
            "why": "Store'lardan socket bağlantısını ve chat state fonksiyonlarını çekiyoruz. Bunları birazdan useEffect'lerde KULLANACAĞIZ."
        },
        {
            "order": "2.7",
            "action": "Store bağlantılarının altına — konuşma listesini yükleyen useEffect ekle",
            "type": "code_add",
            "file": "client/src/pages/chat.tsx",
            "position": "after:stores",
            "code": "  useEffect(() => {\n    api.get('/conversations').then(({ data }) => {\n      setConversations(data.data);\n    });\n  }, []);",
            "why": "M2 4.9'da yazdığımız GET /api/conversations endpoint'inden konuşma listesini çekiyor. Boş dependency array ile SADECE ilk render'da çalışır."
        },
        {
            "order": "2.8",
            "action": "Yükleme useEffect'inin altına — socket event listener useEffect ekle",
            "type": "code_add",
            "file": "client/src/pages/chat.tsx",
            "position": "after:load-effect",
            "code": "  useEffect(() => {\n    if (!socket) return;\n    socket.on('message:received', (message) => {\n      addMessage(message.conversationId, message);\n    });\n    socket.on('typing:update', ({ userId, conversationId, isTyping }) => {\n      setTyping(conversationId, userId, isTyping);\n    });\n    return () => {\n      socket.off('message:received');\n      socket.off('typing:update');\n    };\n  }, [socket]);",
            "why": "M1 4.8'de emit ettiğimiz message:received ve 4.10-4.11'deki typing:update event'lerini DİNLİYORUZ. return'daki cleanup memory leak ÖNLER."
        },
        {
            "order": "2.9",
            "action": "JSX'e GERİ DÖN — activeConversation kontrolü ekle",
            "type": "code_modify",
            "file": "client/src/pages/chat.tsx",
            "code": "      <div className=\"flex-1\">\n        {activeConversation ? (\n          <p className=\"p-4\">Chat Window - {activeConversation}</p>\n        ) : (\n          <div className=\"flex h-full items-center justify-center text-gray-400\">\n            Bir konuşma seçin\n          </div>\n        )}\n      </div>",
            "position": "inside:right-panel",
            "why": "Konuşma seçildiyse içerik göster, seçilmediyse placeholder göster. ChatWindow component'ini M3 Adım 3'te yazacağız."
        },
        {
            "order": "2.10",
            "action": "Chat sayfasının render edildiğini doğrula",
            "type": "validate",
            "validation": "Browser'da chat sayfası açıldığında sol panel ve sağ panel görünmeli. Console'da Socket bağlantı logları görülmeli.",
            "why": "Layout'un doğru çalışması, sonraki component'lerin yerleştirilmesi için temeldir."
        }
    ]

    # ==========================================
    # M3 Step 4: Message Bubble — substep 4.2 dumps 45 lines
    # ==========================================
    m3_step4 = m3['steps'][3]
    m3_step4['substeps'] = [
        {
            "order": "4.1",
            "action": "client/src/components/message-bubble.tsx dosyasını aç — İSKELET component yaz",
            "type": "code_write",
            "file": "client/src/components/message-bubble.tsx",
            "code": "export function MessageBubble({ message }: { message: any }) {\n  return (\n    <div>\n      <p>{message.content}</p>\n    </div>\n  );\n}",
            "why": "İskelet ile başlıyoruz — önce mesaj içeriğinin GÖRÜNDÜğünü doğrulayacağız, sonra stili ekleyeceğiz."
        },
        {
            "order": "4.2",
            "action": "İskeletin içine — isOwn ve isAI kontrol değişkenlerini tanımla",
            "type": "code_add",
            "file": "client/src/components/message-bubble.tsx",
            "position": "inside:component",
            "code": "  const isOwn = false; // TODO: auth context'ten user.id ile karşılaştır\n  const isAI = message.type === 'ai_response';",
            "why": "isOwn kendi mesajımız mı kontrolü — M1 2.8'deki 'ai_response' tipi burada KULLANILIYOR. Auth context entegrasyonu sonra yapılacak."
        },
        {
            "order": "4.3",
            "action": "Return JSX'ini güncelle — flex yönünü isOwn'a göre ayarla",
            "type": "code_write",
            "file": "client/src/components/message-bubble.tsx",
            "code": "  return (\n    <div className={`flex ${isOwn ? 'justify-end' : 'justify-start'}`}>\n      <div className=\"flex max-w-[70%] gap-2\">\n      </div>\n    </div>\n  );",
            "why": "Kendi mesajlarımız SAĞDA (justify-end), karşıdakiler SOLDA (justify-start). max-w-[70%] ile balon ekranın %70'inden fazla genişlemez."
        },
        {
            "order": "4.4",
            "action": "flex div'in içine — avatar göster (sadece karşıdakinin mesajlarında)",
            "type": "code_add",
            "file": "client/src/components/message-bubble.tsx",
            "position": "inside:flex-div",
            "code": "        {!isOwn && (\n          <div className=\"flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gray-700 text-sm font-medium text-gray-300\">\n            {isAI ? 'AI' : message.sender?.name?.[0]?.toUpperCase()}\n          </div>\n        )}",
            "why": "Kendi mesajlarımızda avatar GÖSTERMEZ. AI mesajlarında 'AI' yazar, normal mesajlarda ismin ilk harfi. flex-shrink-0 ile avatar sıkışmaz."
        },
        {
            "order": "4.5",
            "action": "Avatar'ın altına — gönderici adı ve mesaj baloncuğu ekle",
            "type": "code_add",
            "file": "client/src/components/message-bubble.tsx",
            "position": "after:avatar",
            "code": "        <div>\n          {!isOwn && (\n            <p className=\"mb-1 text-xs text-gray-500\">\n              {isAI ? 'AI Asistan' : message.sender?.name}\n            </p>\n          )}\n          <div\n            className={`rounded-2xl px-4 py-2 ${\n              isOwn\n                ? 'bg-blue-600 text-white'\n                : isAI\n                ? 'border border-purple-800 bg-purple-900/20 text-gray-200'\n                : 'bg-gray-700 text-gray-200'\n            }`}\n          >\n            <p className=\"whitespace-pre-wrap text-sm\">{message.content}</p>\n          </div>",
            "why": "Kendi mesajlar MAVİ, AI mesajları MOR, karşıdakiler GRİ. whitespace-pre-wrap ile satır sonları korunur. Üç farklı renk şeması ile mesaj tiplerini GÖRSEL olarak ayırıyoruz."
        },
        {
            "order": "4.6",
            "action": "Balon div'inin altına — zaman damgası ve okundu tikleri ekle",
            "type": "code_add",
            "file": "client/src/components/message-bubble.tsx",
            "position": "after:bubble",
            "code": "          <div className={`mt-1 flex items-center gap-1 text-xs text-gray-500 ${isOwn ? 'justify-end' : ''}`}>\n            <span>\n              {new Date(message.createdAt).toLocaleTimeString('tr-TR', {\n                hour: '2-digit',\n                minute: '2-digit',\n              })}\n            </span>\n            {isOwn && (\n              <span>{message.readBy?.length > 1 ? '\\u2713\\u2713' : '\\u2713'}</span>\n            )}\n          </div>\n        </div>",
            "why": "readBy.length > 1 ise çift tik — karşı taraf okumuş demek (M1 2.8'de tanımladığımız readBy alanı). Saat formatı Türkçe locale ile 24 saat formatında."
        },
        {
            "order": "4.7",
            "action": "chat-window.tsx dosyasına GERİ DÖN — MessageBubble'ı import et ve placeholder'ı değiştir",
            "type": "code_modify",
            "file": "client/src/components/chat-window.tsx",
            "code": "import { MessageBubble } from './message-bubble';\n\n// Mesaj listesindeki placeholder div'i MessageBubble ile değiştir:\n<MessageBubble key={msg._id} message={msg} />",
            "position": "top",
            "why": "3.10'da yazdığımız placeholder mesaj div'ini az önce oluşturduğumuz stilize MessageBubble component'i ile DEĞİŞTİRİYORUZ."
        },
        {
            "order": "4.8",
            "action": "Mesaj bubble stillerini doğrula",
            "type": "validate",
            "validation": "Mesajlar baloncuk şeklinde görünmeli. Zaman damgası doğru formatta olmalı. Farklı mesaj tipleri farklı renklerde olmalı.",
            "why": "Chat arayüzünün profesyonel görünmesi, portfolio projesi olarak sunulabilmesi için kritiktir."
        }
    ]

    # ==========================================
    # M3 Step 5: Infinite Scroll — substep 5.3 dumps 50 lines
    # ==========================================
    m3_step5 = m3['steps'][4]
    m3_step5['substeps'] = [
        {
            "order": "5.1",
            "action": "client/src/hooks/use-infinite-messages.ts dosyasını aç — İSKELET hook yaz",
            "type": "code_write",
            "file": "client/src/hooks/use-infinite-messages.ts",
            "code": "export function useInfiniteMessages(conversationId: string) {\n  return { isLoadingMore: false, hasMore: true, observerRef: null, loadMore: async () => {} };\n}",
            "why": "Custom hook'u iskelet olarak oluşturuyoruz. Return tipini ŞIMDI belirliyoruz — ChatWindow bu değerleri kullanacak."
        },
        {
            "order": "5.2",
            "action": "ÜSTE ÇIK — React hook'ları ve api import'larını ekle",
            "type": "code_write",
            "file": "client/src/hooks/use-infinite-messages.ts",
            "code": "import { useState, useCallback, useRef, useEffect } from 'react';\nimport { api } from '../lib/api';\nimport { useChatStore } from '../stores/chat-store';",
            "why": "2.1'de yazdığımız api helper'ı ve 1.12'deki chat store'u import ediyoruz. useRef ile cursor değerini re-render'lar arasında KORUYACAĞIZ."
        },
        {
            "order": "5.3",
            "action": "GERİ DÖN hook içine — state ve ref tanımlarını yaz",
            "type": "code_add",
            "file": "client/src/hooks/use-infinite-messages.ts",
            "position": "inside:hook",
            "code": "  const [hasMore, setHasMore] = useState(true);\n  const [isLoadingMore, setIsLoadingMore] = useState(false);\n  const cursorRef = useRef<string | null>(null);\n  const { messages, setMessages } = useChatStore();\n  const observerRef = useRef<HTMLDivElement>(null);",
            "why": "hasMore: daha fazla mesaj var mı. cursorRef: son çekilen mesajın zamanı — state DEĞİŞİKLİĞİ tetiklemeden saklanır. observerRef: IntersectionObserver'ın izleyeceği div."
        },
        {
            "order": "5.4",
            "action": "State'lerin altına — loadMore fonksiyonunu yaz (API çağrısı)",
            "type": "code_add",
            "file": "client/src/hooks/use-infinite-messages.ts",
            "position": "after:state",
            "code": "  const loadMore = useCallback(async () => {\n    if (isLoadingMore || !hasMore) return;\n    setIsLoadingMore(true);\n    try {\n      const params = cursorRef.current\n        ? `?cursor=${cursorRef.current}&limit=50`\n        : '?limit=50';\n      const { data } = await api.get(\n        `/conversations/${conversationId}/messages${params}`\n      );",
            "why": "İlk kontrol: zaten yüklüyorsak veya daha fazla mesaj yoksa ÇIK. M2 4.10'da yazdığımız /messages endpoint'ini cursor parametresiyle çağırıyoruz."
        },
        {
            "order": "5.5",
            "action": "API çağrısının altına — mesajları state'e ekle ve cursor'ı güncelle",
            "type": "code_add",
            "file": "client/src/hooks/use-infinite-messages.ts",
            "position": "after:api-call",
            "code": "      const newMessages = data.data.messages;\n      const existing = messages[conversationId] || [];\n      setMessages(conversationId, [...newMessages, ...existing]);\n      setHasMore(data.data.hasMore);\n      cursorRef.current = data.data.nextCursor;\n    } catch (error) {\n      console.error('Mesaj yükleme hatası:', error);\n    } finally {\n      setIsLoadingMore(false);\n    }\n  }, [conversationId, isLoadingMore, hasMore]);",
            "why": "Yeni mesajlar mevcut mesajların BAŞINA eklenir çünkü eski mesajlar üstte gösterilir. M2 2.3'teki cursor-based pagination'ın döndürdüğü nextCursor ve hasMore burada KULLANILIYOR."
        },
        {
            "order": "5.6",
            "action": "loadMore'un altına — IntersectionObserver useEffect ekle",
            "type": "code_add",
            "file": "client/src/hooks/use-infinite-messages.ts",
            "position": "after:loadMore",
            "code": "  useEffect(() => {\n    const observer = new IntersectionObserver(\n      (entries) => {\n        if (entries[0].isIntersecting && hasMore && !isLoadingMore) {\n          loadMore();\n        }\n      },\n      { threshold: 0.1 }\n    );\n    if (observerRef.current) {\n      observer.observe(observerRef.current);\n    }\n    return () => observer.disconnect();\n  }, [loadMore, hasMore, isLoadingMore]);",
            "why": "IntersectionObserver scroll event listener'dan DAHA performanslıdır. threshold: 0.1 ile element %10 görünür olduğunda tetiklenir. return'da observer TEMİZLENİR."
        },
        {
            "order": "5.7",
            "action": "useEffect'in altına — return statement yaz",
            "type": "code_add",
            "file": "client/src/hooks/use-infinite-messages.ts",
            "position": "after:observer",
            "code": "  return { isLoadingMore, hasMore, observerRef, loadMore };",
            "why": "Hook'un dışarıya sunduğu değerler: yükleme durumu, daha fazla var mı, observer referansı ve manuel yükleme fonksiyonu."
        },
        {
            "order": "5.8",
            "action": "chat-window.tsx dosyasına GERİ DÖN — hook'u import et ve entegre et",
            "type": "code_modify",
            "file": "client/src/components/chat-window.tsx",
            "code": "import { useInfiniteMessages } from '../hooks/use-infinite-messages';\n\n// Component içinde:\nconst { isLoadingMore, hasMore, observerRef } = useInfiniteMessages(conversationId);\n\n// Mesaj listesinin en üstüne ekle:\n{hasMore && <div ref={observerRef} className=\"text-center text-gray-400 py-2\">{isLoadingMore ? 'Yükleniyor...' : ''}</div>}",
            "position": "top",
            "why": "observerRef mesaj listesinin EN ÜSTÜNE yerleştirilir — kullanıcı yukarı scroll yapıp bu element'i GÖRDÜĞÜNDE otomatik olarak eski mesajlar yüklenir."
        },
        {
            "order": "5.9",
            "action": "Infinite scroll'un çalıştığını doğrula",
            "type": "validate",
            "validation": "60+ mesajı olan bir konuşmada yukarı scroll yapıldığında eski mesajlar otomatik yüklenmeli. Tüm mesajlar yüklendiğinde loadMore çağrılmamalı.",
            "why": "Infinite scroll, chat uygulamasının temel UX özelliğidir."
        }
    ]

    # ==========================================
    # M4 Step 1: AI Service — substeps 1.4 (33 lines), 1.5 (34 lines)
    # ==========================================
    m4 = milestones[3]
    m4_step1 = m4['steps'][0]
    m4_step1['substeps'] = [
        {
            "order": "1.1",
            "action": "server/src/services/ai.service.ts dosyasını aç — İSKELET class yaz",
            "type": "code_write",
            "file": "server/src/services/ai.service.ts",
            "code": "export class AIService {\n  // AI metotları buraya gelecek\n}",
            "why": "AI mantığı ayrı service'te yönetilecek. İskelet ile başlıyoruz — önce class yapısını oluşturuyoruz."
        },
        {
            "order": "1.2",
            "action": "ÜSTE ÇIK — OpenAI import'unu ve config'i ekle",
            "type": "code_add",
            "file": "server/src/services/ai.service.ts",
            "position": "top",
            "code": "import OpenAI from 'openai';\nimport { config } from '../utils/config';\n\nconst openai = new OpenAI({ apiKey: config.openaiApiKey });",
            "why": "M1 1.2'de kurduğumuz openai paketini import ediyoruz. M1 3.3'te config'e eklediğimiz openaiApiKey burada KULLANILIYOR."
        },
        {
            "order": "1.3",
            "action": "OpenAI client'ın altına — system prompt tanımla",
            "type": "code_add",
            "file": "server/src/services/ai.service.ts",
            "position": "after:client",
            "code": "const SYSTEM_PROMPT = `Sen yardımsever bir AI asistansın. Chat uygulamasında kullanıcılara yardım ediyorsun.\nKurallar:\n- Kısa ve öz cevaplar ver (maksimum 500 kelime)\n- Kod sorularında syntax highlighting için markdown kullan\n- Türkçe cevap ver (teknik terimler İngilizce kalabilir)\n- Zararlı veya uygunsuz içerik üretme\n- Emin olmadığın konularda bunu belirt`;",
            "why": "System prompt AI'ın DAVRANIŞINI belirler. Kurallar ile yanıt kalitesi ve güvenliği kontrol altına alınır."
        },
        {
            "order": "1.4",
            "action": "GERİ DÖN class içine — generateResponse için message dizisi hazırla",
            "type": "code_add",
            "file": "server/src/services/ai.service.ts",
            "position": "inside:class",
            "code": "  private buildMessages(userMessage: string, conversationHistory: any[] = []) {\n    return [\n      { role: 'system' as const, content: SYSTEM_PROMPT },\n      ...conversationHistory.slice(-10).map((msg) => ({\n        role: msg.type === 'ai_response' ? 'assistant' as const : 'user' as const,\n        content: msg.content,\n      })),\n      { role: 'user' as const, content: userMessage },\n    ];\n  }",
            "why": "Son 10 mesaj context olarak gönderilir — token limitini aşmamak için SINIRLANDIRILIR. M1 2.8'de tanımladığımız 'ai_response' tipi burada role belirleme için KULLANILIYOR. Private helper metot ile DRY — generateResponse ve streaming ikisi de bunu kullanır."
        },
        {
            "order": "1.5",
            "action": "buildMessages'ın altına — generateResponse metodunu yaz",
            "type": "code_add",
            "file": "server/src/services/ai.service.ts",
            "position": "after:buildMessages",
            "code": "  async generateResponse(userMessage: string, conversationHistory: any[] = []) {\n    const completion = await openai.chat.completions.create({\n      model: 'gpt-4o-mini',\n      messages: this.buildMessages(userMessage, conversationHistory),\n      max_tokens: 1000,\n      temperature: 0.7,\n    });\n    return completion.choices[0].message.content || 'Yanıt oluşturulamadı.';\n  }",
            "why": "gpt-4o-mini hız ve maliyet açısından chat uygulamaları için ideal. temperature: 0.7 yaratıcılık ve tutarlılık arasında denge sağlar. 1.4'te yazdığımız buildMessages'ı KULLANIYORUZ."
        },
        {
            "order": "1.6",
            "action": "generateResponse'un altına — streaming response metodunun İSKELETİNİ yaz",
            "type": "code_add",
            "file": "server/src/services/ai.service.ts",
            "position": "after:generateResponse",
            "code": "  async generateStreamingResponse(\n    userMessage: string,\n    conversationHistory: any[] = [],\n    onToken: (token: string) => void\n  ) {",
            "why": "Streaming versiyonu onToken callback alır — her token geldiğinde Socket.io ile client'a emit edecek. Bu BAĞLANTIYI M4 Adım 2'de kuracağız."
        },
        {
            "order": "1.7",
            "action": "Streaming fonksiyonunun içine — OpenAI stream çağrısını yaz",
            "type": "code_add",
            "file": "server/src/services/ai.service.ts",
            "position": "inside:streaming",
            "code": "    const stream = await openai.chat.completions.create({\n      model: 'gpt-4o-mini',\n      messages: this.buildMessages(userMessage, conversationHistory),\n      max_tokens: 1000,\n      temperature: 0.7,\n      stream: true,\n    });",
            "why": "stream: true ile OpenAI token token yanıt döndürür. 1.5'teki ile AYNI parametreler, tek fark stream: true."
        },
        {
            "order": "1.8",
            "action": "Stream'in altına — token'ları oku ve fonksiyonu kapat",
            "type": "code_add",
            "file": "server/src/services/ai.service.ts",
            "position": "after:stream-create",
            "code": "    let fullResponse = '';\n    for await (const chunk of stream) {\n      const token = chunk.choices[0]?.delta?.content || '';\n      if (token) {\n        fullResponse += token;\n        onToken(token);\n      }\n    }\n    return fullResponse;\n  }",
            "why": "for await...of ile async iterator olarak okunur. Her token geldiğinde onToken callback'i tetiklenir VE fullResponse'a eklenir. Tam yanıt döndürülür — veritabanına kaydedilmek için."
        },
        {
            "order": "1.9",
            "action": "AI service'in çalıştığını doğrula",
            "type": "validate",
            "validation": "OPENAI_API_KEY .env'de tanımlı olmalı. Test amaçlı generateResponse çağrıldığında yanıt dönmeli.",
            "why": "API key olmadan AI servisi çalışmaz. Key'in geçerli olduğunu ERKEN doğrulamak önemli."
        }
    ]

    # ==========================================
    # M4 Step 3: AI Stream hook — substep 3.3 dumps 38 lines
    # ==========================================
    m4_step3 = m4['steps'][2]
    m4_step3['substeps'] = [
        {
            "order": "3.1",
            "action": "client/src/hooks/use-ai-stream.ts dosyasını aç — İSKELET hook yaz",
            "type": "code_write",
            "file": "client/src/hooks/use-ai-stream.ts",
            "code": "export function useAIStream() {\n  return { streamingMessages: {} };\n}",
            "why": "AI streaming state'i AYRI hook'ta yönetilecek. İskelet ile başlıyoruz — return tipini şimdi belirliyoruz."
        },
        {
            "order": "3.2",
            "action": "ÜSTE ÇIK — React hook'ları ve socket store import'unu ekle",
            "type": "code_add",
            "file": "client/src/hooks/use-ai-stream.ts",
            "position": "top",
            "code": "import { useEffect, useState } from 'react';\nimport { useSocketStore } from '../stores/socket-store';",
            "why": "M3 1.5-1.9'da yazdığımız socket store'u import ediyoruz. useEffect ile socket event'lerini dinleyeceğiz."
        },
        {
            "order": "3.3",
            "action": "GERİ DÖN hook içine — state ve socket bağlantısını kur",
            "type": "code_add",
            "file": "client/src/hooks/use-ai-stream.ts",
            "position": "inside:hook",
            "code": "  const { socket } = useSocketStore();\n  const [streamingMessages, setStreamingMessages] = useState<Record<string, string>>({});",
            "why": "streamingMessages: aktif streaming mesajları messageId bazında izler. Record<string, string> — key: messageId, value: biriken token'lar."
        },
        {
            "order": "3.4",
            "action": "State'in altına — ai:stream:start event listener ekle",
            "type": "code_add",
            "file": "client/src/hooks/use-ai-stream.ts",
            "position": "after:state",
            "code": "  useEffect(() => {\n    if (!socket) return;\n\n    socket.on('ai:stream:start', ({ messageId }) => {\n      setStreamingMessages((prev) => ({ ...prev, [messageId]: '' }));\n    });",
            "why": "M4 2.8'de backend'de emit ettiğimiz ai:stream:start event'ini DİNLİYORUZ. Yeni streaming mesaj için BOŞ string ile başlatıyoruz."
        },
        {
            "order": "3.5",
            "action": "stream:start listener'ının altına — ai:stream:token listener ekle",
            "type": "code_add",
            "file": "client/src/hooks/use-ai-stream.ts",
            "position": "after:stream-start",
            "code": "    socket.on('ai:stream:token', ({ messageId, token }) => {\n      setStreamingMessages((prev) => ({\n        ...prev,\n        [messageId]: (prev[messageId] || '') + token,\n      }));\n    });",
            "why": "M4 2.9'da her token geldiğinde emit edilen event'i dinliyoruz. İlgili mesajın content'ine token EKLENİR — ChatGPT'nin yazıyor efekti."
        },
        {
            "order": "3.6",
            "action": "stream:token listener'ının altına — ai:stream:end listener ekle",
            "type": "code_add",
            "file": "client/src/hooks/use-ai-stream.ts",
            "position": "after:stream-token",
            "code": "    socket.on('ai:stream:end', ({ messageId }) => {\n      setStreamingMessages((prev) => {\n        const next = { ...prev };\n        delete next[messageId];\n        return next;\n      });\n    });",
            "why": "Streaming bittiğinde mesaj bu state'ten SİLİNİR. Normal mesaj listesine message:received event'i ile eklenecek. Geçici streaming → kalıcı mesaj dönüşümü."
        },
        {
            "order": "3.7",
            "action": "stream:end listener'ının altına — cleanup fonksiyonunu yaz ve useEffect'i kapat",
            "type": "code_add",
            "file": "client/src/hooks/use-ai-stream.ts",
            "position": "after:stream-end",
            "code": "    return () => {\n      socket.off('ai:stream:start');\n      socket.off('ai:stream:token');\n      socket.off('ai:stream:end');\n    };\n  }, [socket]);",
            "why": "Cleanup fonksiyonu ile listener'lar TEMİZLENİR — memory leak önlenir. socket bağımlılığı ile socket değiştiğinde yeniden bağlanır."
        },
        {
            "order": "3.8",
            "action": "useEffect'in altına — return statement ekle",
            "type": "code_add",
            "file": "client/src/hooks/use-ai-stream.ts",
            "position": "after:effect",
            "code": "  return { streamingMessages };",
            "why": "Hook'un dışarıya sunduğu tek değer: aktif streaming mesajları. ChatWindow bu değeri kullanarak streaming UI render edecek."
        },
        {
            "order": "3.9",
            "action": "BAŞKA DOSYAYA GEÇ — client/src/components/streaming-message.tsx aç ve component'i yaz",
            "type": "code_write",
            "file": "client/src/components/streaming-message.tsx",
            "code": "export function StreamingMessage({ content }: { content: string }) {\n  return (\n    <div className=\"rounded-2xl border border-purple-800 bg-purple-900/20 px-4 py-2\">\n      <p className=\"mb-1 text-xs text-purple-400\">AI Asistan</p>\n      <p className=\"whitespace-pre-wrap text-sm text-gray-200\">\n        {content}\n        <span className=\"inline-block h-4 w-1 animate-pulse bg-purple-500\" />\n      </p>\n    </div>\n  );\n}",
            "why": "animate-pulse ile blinking cursor efekti AI'ın HALA yazdığını gösterir. M3 4.5'te mesaj bubble'da kullandığımız mor tema AYNI — tutarlı tasarım."
        },
        {
            "order": "3.10",
            "action": "chat-window.tsx dosyasına GERİ DÖN — streaming hook ve component'i entegre et",
            "type": "code_modify",
            "file": "client/src/components/chat-window.tsx",
            "code": "import { useAIStream } from '../hooks/use-ai-stream';\nimport { StreamingMessage } from './streaming-message';\n\n// Component içinde:\nconst { streamingMessages } = useAIStream();\n\n// Mesaj listesinin sonuna, typing indicator'dan önce ekle:\n{Object.entries(streamingMessages).map(([id, content]) => (\n  <StreamingMessage key={id} content={content} />\n))}",
            "position": "top",
            "why": "Hook ve component'i ChatWindow'a BAĞLIYORUZ. Streaming mesajlar normal mesaj listesinin SONUNDA gösterilir."
        },
        {
            "order": "3.11",
            "action": "AI streaming UI'ın çalıştığını doğrula",
            "type": "validate",
            "validation": "AI'a soru sorulduğunda yanıt karakter karakter ekranda görünmeli. Streaming sırasında blinking cursor olmalı. Streaming bitince normal mesaj olarak kalmalı.",
            "why": "Streaming UI, AI entegrasyonunun en GÖRSEL ve ETKİLEYİCİ parçasıdır."
        }
    ]

    # ==========================================
    # M5 Step 2: File Upload Button — substep 2.3 dumps 55 lines
    # ==========================================
    m5 = milestones[4]
    m5_step2 = m5['steps'][1]
    m5_step2['substeps'] = [
        {
            "order": "2.1",
            "action": "client/src/components/file-upload-button.tsx dosyasını aç — İSKELET component yaz",
            "type": "code_write",
            "file": "client/src/components/file-upload-button.tsx",
            "code": "export function FileUploadButton({ conversationId }: { conversationId: string }) {\n  return (\n    <button className=\"rounded-lg p-2 text-gray-500 hover:bg-gray-700\" title=\"Dosya ekle\">\n      Dosya\n    </button>\n  );\n}",
            "why": "İskelet buton ile başlıyoruz — görsel olarak DOĞRULUYORUZ, sonra dosya seçme ve yükleme mantığını ekleyeceğiz."
        },
        {
            "order": "2.2",
            "action": "ÜSTE ÇIK — useRef, api ve socket store import'larını ekle",
            "type": "code_add",
            "file": "client/src/components/file-upload-button.tsx",
            "position": "top",
            "code": "import { useRef } from 'react';\nimport { api } from '../lib/api';\nimport { useSocketStore } from '../stores/socket-store';",
            "why": "useRef hidden file input'u referans etmek için, M3 2.1'deki api dosya yüklemek için, M3 1.5-1.9'daki socket store mesaj göndermek için gerekli."
        },
        {
            "order": "2.3",
            "action": "GERİ DÖN component içine — ref ve socket tanımlarını ekle",
            "type": "code_add",
            "file": "client/src/components/file-upload-button.tsx",
            "position": "inside:component",
            "code": "  const fileInputRef = useRef<HTMLInputElement>(null);\n  const { socket } = useSocketStore();",
            "why": "fileInputRef ile hidden file input'a erişeceğiz. socket ile dosya yüklendikten sonra mesaj göndereceğiz."
        },
        {
            "order": "2.4",
            "action": "Ref tanımlarının altına — handleFileSelect fonksiyonunu yaz (dosya yükleme)",
            "type": "code_add",
            "file": "client/src/components/file-upload-button.tsx",
            "position": "after:refs",
            "code": "  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {\n    const file = e.target.files?.[0];\n    if (!file) return;\n\n    const formData = new FormData();\n    formData.append('file', file);",
            "why": "FormData ile multipart/form-data formatında dosya gönderilecek — JSON'da binary veri taşınamaz."
        },
        {
            "order": "2.5",
            "action": "FormData'nın altına — API çağrısı ve socket mesaj gönderme",
            "type": "code_add",
            "file": "client/src/components/file-upload-button.tsx",
            "position": "after:formdata",
            "code": "    try {\n      const { data } = await api.post('/upload', formData, {\n        headers: { 'Content-Type': 'multipart/form-data' },\n      });\n      socket?.emit('message:send', {\n        conversationId,\n        content: data.data.url,\n        type: file.type.startsWith('image/') ? 'image' : 'file',\n        metadata: {\n          originalName: data.data.originalName,\n          size: data.data.size,\n          mimetype: data.data.mimetype,\n        },\n      });\n    } catch (error) {\n      console.error('Dosya yükleme hatası:', error);\n    }\n  };",
            "why": "1.6'da yazdığımız /api/upload endpoint'ine dosyayı yüklüyoruz. Sonra M1 4.6'daki message:send event'ini tetikliyoruz — dosya URL'i mesaj content'i olarak gönderiliyor."
        },
        {
            "order": "2.6",
            "action": "Return JSX'ini güncelle — SVG ikon ve hidden file input ekle",
            "type": "code_write",
            "file": "client/src/components/file-upload-button.tsx",
            "code": "  return (\n    <>\n      <button\n        onClick={() => fileInputRef.current?.click()}\n        className=\"rounded-lg p-2 text-gray-500 hover:bg-gray-700\"\n        title=\"Dosya ekle\"\n      >\n        <svg className=\"h-5 w-5\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\">\n          <path strokeLinecap=\"round\" strokeLinejoin=\"round\" strokeWidth={2} d=\"M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13\" />\n        </svg>\n      </button>\n      <input\n        ref={fileInputRef}\n        type=\"file\"\n        onChange={handleFileSelect}\n        accept=\"image/*,.pdf,.txt,.csv\"\n        className=\"hidden\"\n      />\n    </>\n  );",
            "why": "Hidden file input + button pattern'ı ile özel stilize edilmiş dosya seçici oluşturulur. accept attribute'u dosya seçim dialogunda gösterilen tipleri filtreler."
        },
        {
            "order": "2.7",
            "action": "chat-window.tsx dosyasına GERİ DÖN — FileUploadButton'ı import et",
            "type": "code_modify",
            "file": "client/src/components/chat-window.tsx",
            "code": "import { FileUploadButton } from './file-upload-button';\n\n// Input alanının soluna ekle:\n<FileUploadButton conversationId={conversationId} />",
            "position": "top",
            "why": "Az önce yazdığımız dosya yükleme butonunu ChatWindow'un input alanına BAĞLIYORUZ — WhatsApp'taki ataç ikonu gibi."
        },
        {
            "order": "2.8",
            "action": "Dosya gönderiminin çalıştığını doğrula",
            "type": "validate",
            "validation": "Ataç ikonuna tıklayıp dosya seçildiğinde dosya yüklenmeli ve mesaj olarak gönderilmeli.",
            "why": "Dosya paylaşımı, modern chat uygulamalarının standart özelliğidir."
        }
    ]

    # ==========================================
    # M5 Step 3: File Message — substep 3.2 dumps 39 lines
    # ==========================================
    m5_step3 = m5['steps'][2]
    m5_step3['substeps'] = [
        {
            "order": "3.1",
            "action": "client/src/components/file-message.tsx dosyasını aç — İSKELET component yaz",
            "type": "code_write",
            "file": "client/src/components/file-message.tsx",
            "code": "export function FileMessage({ message }: { message: any }) {\n  return <p>Dosya: {message.content}</p>;\n}",
            "why": "İskelet ile başlıyoruz — dosya URL'inin GÖRÜNDÜğünü doğrulayacağız."
        },
        {
            "order": "3.2",
            "action": "İskeletin içine — değişken tanımlarını ekle",
            "type": "code_add",
            "file": "client/src/components/file-message.tsx",
            "position": "inside:component",
            "code": "  const isImage = message.type === 'image';\n  const metadata = message.metadata || {};\n  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:3001';",
            "why": "Resim ve dosya tiplerini ayırt edecek değişkenler. baseUrl ile server'daki dosyalara erişeceğiz."
        },
        {
            "order": "3.3",
            "action": "Return JSX'ini güncelle — resim tipiyse inline göster",
            "type": "code_write",
            "file": "client/src/components/file-message.tsx",
            "code": "  if (isImage) {\n    return (\n      <div className=\"max-w-sm\">\n        <img\n          src={`${baseUrl}${message.content}`}\n          alt=\"Paylaşılan resim\"\n          className=\"rounded-lg cursor-pointer hover:opacity-90 transition-opacity\"\n          loading=\"lazy\"\n          onClick={() => window.open(`${baseUrl}${message.content}`, '_blank')}\n        />\n      </div>\n    );\n  }",
            "why": "loading='lazy' ile resimler viewport'a girene kadar YÜKLENMEZ — performans optimizasyonu. Tıklayınca yeni sekmede tam boyut açılır."
        },
        {
            "order": "3.4",
            "action": "Resim kontrolünün altına — dosya tipiyse indirme linki göster",
            "type": "code_add",
            "file": "client/src/components/file-message.tsx",
            "position": "after:image-check",
            "code": "  return (\n    <a\n      href={`${baseUrl}${message.content}`}\n      download={metadata.originalName}\n      className=\"flex items-center gap-3 rounded-lg border p-3 transition-colors border-gray-600 hover:bg-gray-700\"\n    >\n      <div className=\"flex h-10 w-10 items-center justify-center rounded-lg bg-blue-900 text-blue-300\">\n        <svg className=\"h-5 w-5\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\">\n          <path strokeLinecap=\"round\" strokeLinejoin=\"round\" strokeWidth={2} d=\"M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z\" />\n        </svg>\n      </div>\n      <div>\n        <p className=\"text-sm font-medium text-gray-200\">{metadata.originalName || 'Dosya'}</p>\n        <p className=\"text-xs text-gray-500\">\n          {metadata.size ? `${(metadata.size / 1024).toFixed(1)} KB` : ''}\n        </p>\n      </div>\n    </a>\n  );",
            "why": "download attribute'u dosya indirmeyi TETİKLER. 1.6'da yazdığımız upload endpoint'in döndürdüğü metadata burada GÖSTERİLİYOR."
        },
        {
            "order": "3.5",
            "action": "message-bubble.tsx dosyasına GERİ DÖN — FileMessage'ı import et ve tip kontrolü ekle",
            "type": "code_modify",
            "file": "client/src/components/message-bubble.tsx",
            "code": "import { FileMessage } from './file-message';\n\n// content render kısmında tip kontrolü ekle:\n{message.type === 'image' || message.type === 'file'\n  ? <FileMessage message={message} />\n  : <p className=\"whitespace-pre-wrap text-sm\">{message.content}</p>\n}",
            "position": "top",
            "why": "M3 4.5'te yazdığımız MessageBubble'da mesaj tipine göre FARKLI component render ediliyor."
        },
        {
            "order": "3.6",
            "action": "Resim ve dosya gösterimini doğrula",
            "type": "validate",
            "validation": "Resim mesajları inline önizleme göstermeli. PDF/dosya mesajlarında indirme linki çalışmalı.",
            "why": "Dosya paylaşım deneyiminin eksiksiz çalışması, profesyonel chat uygulaması izlenimi verir."
        }
    ]

    # Write result
    with open('content/projects/project-03.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Validate
    with open('content/projects/project-03.json', 'r', encoding='utf-8') as f:
        validated = json.load(f)

    total = 0
    over8 = 0
    for m in validated['milestones']:
        for step in m['steps']:
            n = len(step.get('substeps', []))
            total += n
            for sub in step.get('substeps', []):
                code = sub.get('code', '')
                if code:
                    lines = code.count('\n') + 1
                    if lines > 8:
                        over8 += 1
                        if lines > 15:
                            print(f"  BIG: M{validated['milestones'].index(m)+1} S{step['step']} sub {sub['order']} = {lines} lines")

    print(f"\nTotal substeps: {total}")
    print(f"Substeps with >8 lines of code: {over8}")
    print("JSON validated successfully!")


if __name__ == '__main__':
    main()
