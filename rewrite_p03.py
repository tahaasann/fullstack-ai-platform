#!/usr/bin/env python3
"""Rewrite project-03.json substeps to match gold standard quality."""

import json
import copy

def main():
    with open('content/projects/project-03.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # We need to rewrite substeps for ALL milestones/steps
    # Key problems:
    # 1. M1 Step 3 (index.ts): substeps 3.5-3.7 dump 20-50 lines each
    # 2. M1 Step 4 (socket-handler.ts): substep 4.3-4.4 dump 20-30 lines
    # 3. M2 Step 4 (conversation.routes.ts): substep 4.6 dumps 52 lines
    # 4. M3 Step 1 (socket-store + chat-store): substeps 1.3=42 lines, 1.4=53 lines
    # 5. M4 Step 2 (ai-handler.ts): substep 2.3 dumps 71 lines

    milestones = data['milestones']

    # ==========================================
    # M1 Step 3: Socket.io Server Kurulumu
    # ==========================================
    m1 = milestones[0]
    m1_step3 = m1['steps'][2]  # step 3
    m1_step3['substeps'] = [
        {
            "order": "3.1",
            "action": "server/src/utils/config.ts dosyasını aç — İSKELET export yaz",
            "type": "code_write",
            "file": "server/src/utils/config.ts",
            "code": "export const config = {\n  // config değerleri buraya gelecek\n};",
            "why": "Konfigürasyonu tek dosyada toplamak, değerlerin dağılmasını önler. İskelet ile başlayıp sonra dolduracağız."
        },
        {
            "order": "3.2",
            "action": "ÜSTE ÇIK — dotenv import'unu ekle (config'i doldurmadan ÖNCE)",
            "type": "code_write",
            "file": "server/src/utils/config.ts",
            "code": "import dotenv from 'dotenv';\ndotenv.config();",
            "why": "dotenv .env dosyasını okur ve process.env'e yükler. Bu import'u ŞİMDİ ekliyoruz çünkü birazdan environment variable'ları okuyacağız."
        },
        {
            "order": "3.3",
            "action": "GERİ DÖN config nesnesine — temel değerleri doldur",
            "type": "code_write",
            "file": "server/src/utils/config.ts",
            "code": "import dotenv from 'dotenv';\ndotenv.config();\n\nexport const config = {\n  port: parseInt(process.env.PORT || '3001'),\n  mongoUri: process.env.MONGO_URI || 'mongodb://localhost:27017/chatapp',\n  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',\n  jwtSecret: process.env.JWT_SECRET || 'dev-secret-change-in-production',\n  clientUrl: process.env.CLIENT_URL || 'http://localhost:5173',\n  openaiApiKey: process.env.OPENAI_API_KEY || '',\n};",
            "why": "Her config değerinin varsayılanı var — .env dosyası olmadan bile çalışır. parseInt() ile port'u string'den number'a çeviriyoruz. Default değerler geliştirme ortamı için."
        },
        {
            "order": "3.4",
            "action": "BAŞKA DOSYAYA GEÇ — server/.env dosyasını oluştur",
            "type": "code_write",
            "file": "server/.env",
            "code": "PORT=3001\nMONGO_URI=mongodb://localhost:27017/chatapp\nREDIS_URL=redis://localhost:6379\nJWT_SECRET=your-super-secret-jwt-key-change-this\nCLIENT_URL=http://localhost:5173\nOPENAI_API_KEY=sk-your-openai-api-key",
            "why": "3.3'te config.ts'i yazdık, şimdi o dosyanın okuyacağı .env dosyasını oluşturuyoruz. Hassas bilgiler burada saklanır ve git'e commit EDİLMEZ."
        },
        {
            "order": "3.5",
            "action": "BAŞKA DOSYAYA GEÇ — server/src/index.ts aç — İSKELET yaz",
            "type": "code_write",
            "file": "server/src/index.ts",
            "code": "const app = {};\nconsole.log('Server placeholder');",
            "why": "Uygulamanın giriş noktasını İSKELET olarak oluşturuyoruz. İlk önce 'çalışıyor mu?' diye doğrulayacağız, sonra import'ları ekleyeceğiz."
        },
        {
            "order": "3.6",
            "action": "ÜSTE ÇIK — express import'unu ekle ve app oluştur",
            "type": "code_write",
            "file": "server/src/index.ts",
            "code": "import express from 'express';\n\nconst app = express();",
            "why": "İlk import — Express framework. İskelet'teki placeholder'ı gerçek Express uygulaması ile değiştiriyoruz."
        },
        {
            "order": "3.7",
            "action": "ÜSTE ÇIK — http ve Socket.io import'larını ekle",
            "type": "code_write",
            "file": "server/src/index.ts",
            "code": "import express from 'express';\nimport { createServer } from 'http';\nimport { Server } from 'socket.io';",
            "why": "Socket.io, Express'in HTTP server'ı üzerinden WebSocket upgrade yapar — bu yüzden createServer gerekli. Server Socket.io'nun ana sınıfı."
        },
        {
            "order": "3.8",
            "action": "Import'ların altına httpServer ve io oluştur",
            "type": "code_write",
            "file": "server/src/index.ts",
            "code": "import express from 'express';\nimport { createServer } from 'http';\nimport { Server } from 'socket.io';\n\nconst app = express();\nconst httpServer = createServer(app);",
            "why": "createServer(app) ile Express uygulaması HTTP server'a sarılıyor. Socket.io bu HTTP server üzerinden WebSocket bağlantısı kuracak."
        },
        {
            "order": "3.9",
            "action": "httpServer'ın altına Socket.io server'ını CORS ile oluştur",
            "type": "code_add",
            "file": "server/src/index.ts",
            "position": "after:httpServer",
            "code": "\nimport { config } from './utils/config';\n\nconst io = new Server(httpServer, {\n  cors: {\n    origin: config.clientUrl,\n    methods: ['GET', 'POST'],\n    credentials: true,\n  },\n});",
            "why": "3.3'te yazdığımız config'i import edip clientUrl'i CORS ayarına veriyoruz. credentials: true ile cookie/auth header gönderimi sağlanır."
        },
        {
            "order": "3.10",
            "action": "io'nun altına Express middleware'lerini ekle",
            "type": "code_add",
            "file": "server/src/index.ts",
            "position": "after:io",
            "code": "\nimport cors from 'cors';\n\napp.use(cors({ origin: config.clientUrl, credentials: true }));\napp.use(express.json());",
            "why": "cors middleware'i frontend'den gelen isteklere izin verir. express.json() request body'yi parse eder. Bunları io'dan SONRA yazıyoruz çünkü sıralı ekliyoruz."
        },
        {
            "order": "3.11",
            "action": "Middleware'lerin altına Socket.io auth middleware'ini ekle",
            "type": "code_add",
            "file": "server/src/index.ts",
            "position": "after:middleware",
            "code": "\nio.use(async (socket, next) => {\n  try {\n    const token = socket.handshake.auth.token;\n    if (!token) return next(new Error('Authentication required'));\n    const jwt = require('jsonwebtoken');\n    const payload = jwt.verify(token, config.jwtSecret);\n    socket.data.userId = payload.userId;\n    next();\n  } catch (error) {\n    next(new Error('Invalid token'));\n  }\n});",
            "why": "io.use() middleware HER yeni socket bağlantısından önce çalışır. Client bağlanırken auth: { token } gönderir — biz burada JWT'yi doğruluyoruz. Token geçersizse bağlantı REDDEDİLİR."
        },
        {
            "order": "3.12",
            "action": "Auth middleware'inin altına connection event handler'ını ekle",
            "type": "code_add",
            "file": "server/src/index.ts",
            "position": "after:auth",
            "code": "\nio.on('connection', (socket) => {\n  console.log(`User connected: ${socket.data.userId}`);\n  socket.on('disconnect', () => {\n    console.log(`User disconnected: ${socket.data.userId}`);\n  });\n});",
            "why": "Placeholder connection handler — gerçek event handler'ları M1 Adım 4'te AYRI dosyada yazacağız. Şimdilik bağlantının ÇALIŞTIĞINI doğruluyoruz."
        },
        {
            "order": "3.13",
            "action": "ÜSTE ÇIK — mongoose import'unu ekle",
            "type": "code_add",
            "file": "server/src/index.ts",
            "position": "top",
            "code": "import mongoose from 'mongoose';",
            "why": "MongoDB bağlantısı için mongoose'u import ediyoruz. 1.5'te Docker ile başlattığımız MongoDB'ye bağlanacağız."
        },
        {
            "order": "3.14",
            "action": "Dosyanın ALTINA MongoDB bağlantısını ve server başlatmayı ekle",
            "type": "code_add",
            "file": "server/src/index.ts",
            "position": "bottom",
            "code": "\nmongoose.connect(config.mongoUri)\n  .then(() => console.log('MongoDB connected'))\n  .catch((err) => console.error('MongoDB error:', err));\n\nhttpServer.listen(config.port, () => {\n  console.log(`Server running on port ${config.port}`);\n});\n\nexport { io };",
            "why": "MongoDB bağlantısını 1.5'te Docker ile başlattığımız veritabanına kuruyoruz. httpServer.listen ile server'ı başlatıyoruz. io'yu export ediyoruz çünkü başka dosyalardan erişeceğiz."
        },
        {
            "order": "3.15",
            "action": "Server'ı başlatıp MongoDB bağlantısını doğrula",
            "type": "validate",
            "validation": "cd server && pnpm run dev çalıştırıldığında 'Server running on port 3001' ve 'MongoDB connected' mesajları görülmeli.",
            "why": "Server'ın MongoDB'ye başarıyla bağlandığını ve Socket.io'nun hazır olduğunu doğrulamak, sonraki adımlara geçmeden önce kritiktir."
        }
    ]

    # ==========================================
    # M1 Step 4: Temel Socket Event Handler'ları
    # ==========================================
    m1_step4 = m1['steps'][3]  # step 4
    m1_step4['substeps'] = [
        {
            "order": "4.1",
            "action": "server/src/events/socket-handler.ts dosyasını aç — İSKELET fonksiyon yaz",
            "type": "code_write",
            "file": "server/src/events/socket-handler.ts",
            "code": "import { Server, Socket } from 'socket.io';\n\nexport function setupSocketHandlers(io: Server) {\n  io.on('connection', async (socket: Socket) => {\n    console.log('Handler connected:', socket.data.userId);\n  });\n}",
            "why": "İskelet ile başlıyoruz — fonksiyonun ÇALIŞTIĞINI doğrulayacağız, sonra event handler'ları ekleyeceğiz. Socket.io Server ve Socket tiplerini import ediyoruz çünkü parametre tiplerinde KULLANACAĞIZ."
        },
        {
            "order": "4.2",
            "action": "ÜSTE ÇIK — Model import'larını ekle (birazdan kullanacağız)",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "top",
            "code": "import { Message } from '../models/message.model';\nimport { Conversation } from '../models/conversation.model';\nimport { User } from '../models/user.model';",
            "why": "2. adımda yazdığımız modelleri import ediyoruz — birazdan connection event'inde User'ı online yapacağız ve mesaj event'inde Message oluşturacağız."
        },
        {
            "order": "4.3",
            "action": "GERİ DÖN fonksiyon içine — userId'yi al ve kullanıcıyı online yap",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "inside:connection",
            "code": "    const userId = socket.data.userId;\n\n    // Kullanıcıyı online yap\n    await User.findByIdAndUpdate(userId, { isOnline: true });",
            "why": "3.11'de auth middleware'inde socket.data.userId'yi SET ettik — şimdi KULLANIYORUZ. 2.4'te tanımladığımız isOnline alanını true yapıyoruz."
        },
        {
            "order": "4.4",
            "action": "Online yapmanın altına — kullanıcıyı konuşma odalarına katıl",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:online",
            "code": "    // Kullanıcının konuşma odalarına katıl\n    const conversations = await Conversation.find({ participants: userId });\n    conversations.forEach((conv) => {\n      socket.join(conv.id);\n    });",
            "why": "socket.join(roomId) ile kullanıcı, tüm konuşma odalarına katılır. Bu sayede io.to(roomId).emit() ile odadaki herkese mesaj gönderebileceğiz."
        },
        {
            "order": "4.5",
            "action": "Room katılımının altına — online durumunu diğer kullanıcılara bildir",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:rooms",
            "code": "    // Online durumunu bildir\n    socket.broadcast.emit('user:online', { userId });",
            "why": "socket.broadcast.emit gönderen HARİÇ herkese mesaj yollar. Diğer kullanıcılar 'bu kişi online oldu' bilgisini alır."
        },
        {
            "order": "4.6",
            "action": "Broadcast'in altına — message:send event handler'ını ekle (BAŞLANGIÇ)",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:broadcast",
            "code": "    // Mesaj gönderme\n    socket.on('message:send', async (data, callback) => {\n      try {\n        const { conversationId, content, type = 'text' } = data;",
            "why": "Mesaj gönderme event handler'ını AÇIYORUZ. data'dan conversationId, content ve type'ı destructure ediyoruz. callback ile gönderene onay döneceğiz."
        },
        {
            "order": "4.7",
            "action": "message:send içinde — mesajı veritabanına kaydet",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "inside:message:send",
            "code": "        const message = await Message.create({\n          conversationId,\n          sender: userId,\n          content,\n          type,\n          readBy: [userId],\n        });",
            "why": "2.8'de tanımladığımız Message modeliyle mesajı kaydediyoruz. readBy'a göndereni ekliyoruz — kendi mesajını 'okumuş' sayıyoruz."
        },
        {
            "order": "4.8",
            "action": "Mesaj kaydının altına — konuşmayı güncelle ve emit et",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:message-create",
            "code": "        await Conversation.findByIdAndUpdate(conversationId, {\n          lastMessage: message.id,\n          lastActivity: new Date(),\n        });\n        const populated = await message.populate('sender', 'name avatar');\n        io.to(conversationId).emit('message:received', populated);\n        callback({ status: 'ok', messageId: message.id });",
            "why": "2.6'da tanımladığımız lastMessage alanını güncelliyoruz. populate ile gönderici bilgisini ekleyip odadaki HERKESE emit ediyoruz. callback ile gönderene 'mesaj alındı' onayı — WhatsApp'taki tek tik."
        },
        {
            "order": "4.9",
            "action": "message:send'in catch bloğunu ve kapanış süslü parantezini ekle",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:emit",
            "code": "      } catch (error) {\n        callback({ status: 'error', message: 'Mesaj gönderilemedi' });\n      }\n    });",
            "why": "Hata durumunda callback ile client'a bilgi dönüyoruz. try/catch ile veritabanı hatası veya network sorunu yakalanır."
        },
        {
            "order": "4.10",
            "action": "message:send'in altına — typing indicator event'lerini ekle",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:message-handler",
            "code": "    // Yazıyor bildirimi\n    socket.on('typing:start', (data) => {\n      socket.to(data.conversationId).emit('typing:update', {\n        userId,\n        conversationId: data.conversationId,\n        isTyping: true,\n      });\n    });",
            "why": "socket.to() mesajı gönderen HARİÇ odadaki herkese iletir. Typing event'leri veritabanına KAYDEDİLMEZ — anlık, geçici bilgidir."
        },
        {
            "order": "4.11",
            "action": "typing:start'ın altına — typing:stop event'ini ekle",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:typing-start",
            "code": "    socket.on('typing:stop', (data) => {\n      socket.to(data.conversationId).emit('typing:update', {\n        userId,\n        conversationId: data.conversationId,\n        isTyping: false,\n      });\n    });",
            "why": "Start/stop ikili yapısı ile typing durumu yönetilir. isTyping: false ile karşı taraf 'artık yazmıyor' bilgisini alır."
        },
        {
            "order": "4.12",
            "action": "Typing'in altına — mesaj okundu event'ini ekle",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:typing-stop",
            "code": "    // Mesaj okundu\n    socket.on('message:read', async (data) => {\n      await Message.updateMany(\n        {\n          conversationId: data.conversationId,\n          sender: { $ne: userId },\n          readBy: { $nin: [userId] },\n        },\n        { $addToSet: { readBy: userId } }\n      );\n      socket.to(data.conversationId).emit('message:read:update', {\n        conversationId: data.conversationId,\n        userId,\n      });\n    });",
            "why": "$ne kendi mesajlarını hariç tutar. $nin zaten okunmuş mesajları hariç tutar. $addToSet duplicate eklemeden readBy'a kullanıcı ekler. 2.8'de tanımladığımız readBy alanı burada KULLANILIYOR."
        },
        {
            "order": "4.13",
            "action": "Okundu event'inin altına — disconnect handler'ını ekle",
            "type": "code_add",
            "file": "server/src/events/socket-handler.ts",
            "position": "after:message-read",
            "code": "    // Bağlantı kopma\n    socket.on('disconnect', async () => {\n      await User.findByIdAndUpdate(userId, {\n        isOnline: false,\n        lastSeen: new Date(),\n      });\n      socket.broadcast.emit('user:offline', { userId });\n    });",
            "why": "Disconnect'te 4.3'teki online yapma işleminin TAM TERSİNİ yapıyoruz: isOnline false, lastSeen güncelle, herkese 'offline oldum' de. WhatsApp'taki 'son görülme' özelliği."
        },
        {
            "order": "4.14",
            "action": "index.ts dosyasına GERİ DÖN — socket handler'ı import et ve kullan",
            "type": "code_modify",
            "file": "server/src/index.ts",
            "code": "import { setupSocketHandlers } from './events/socket-handler';\n\n// Mevcut io.on('connection'...) bloğunu kaldır ve yerine ekle:\nsetupSocketHandlers(io);",
            "position": "top",
            "why": "3.12'de yazdığımız placeholder io.on('connection') bloğunu kaldırıp, az önce yazdığımız socket handler modülünü bağlıyoruz. Ana dosya temiz kalır."
        },
        {
            "order": "4.15",
            "action": "Server'ı yeniden başlat ve bağlantıyı test et",
            "type": "validate",
            "validation": "Server loglarında 'User connected' mesajları görülmeli. Bir client mesaj gönderdiğinde diğer client'ta 'message:received' event'i tetiklenmeli.",
            "why": "Real-time iletişimin çalıştığını iki client ile doğrulamak, Socket.io kurulumunun doğru yapıldığını kanıtlar."
        }
    ]

    # ==========================================
    # M1 Step 5: Redis - already OK (5 substeps, reasonable sizes)
    # ==========================================
    # Keep as is - substep 5.3 is large but it's a utility file, acceptable

    # ==========================================
    # M2 Step 1: Conversation Service - already OK-ish
    # ==========================================
    # Keep as is

    # ==========================================
    # M2 Step 4: REST API Endpoint'leri (conversation.routes.ts)
    # Substep 4.6 dumps 52 lines
    # ==========================================
    m2 = milestones[1]
    m2_step4 = m2['steps'][3]  # step 4
    m2_step4['substeps'] = [
        {
            "order": "4.1",
            "action": "server/src/middleware/auth.ts dosyasını aç — İSKELET fonksiyon yaz",
            "type": "code_write",
            "file": "server/src/middleware/auth.ts",
            "code": "import { Request, Response, NextFunction } from 'express';\n\nexport function authenticate(req: Request, res: Response, next: NextFunction) {\n  // TODO: JWT doğrulama\n  next();\n}",
            "why": "İskelet middleware ile başlıyoruz. Express tiplerini import ediyoruz çünkü parametre tiplerinde KULLANACAĞIZ."
        },
        {
            "order": "4.2",
            "action": "ÜSTE ÇIK — jwt ve config import'larını ekle",
            "type": "code_add",
            "file": "server/src/middleware/auth.ts",
            "position": "top",
            "code": "import jwt from 'jsonwebtoken';\nimport { config } from '../utils/config';",
            "why": "M1 3.3'te yazdığımız config'i ve jsonwebtoken'ı import ediyoruz. jwt.verify ile token doğrulaması yapacağız."
        },
        {
            "order": "4.3",
            "action": "GERİ DÖN fonksiyon ÜSTÜne — TypeScript tip genişletme ekle",
            "type": "code_add",
            "file": "server/src/middleware/auth.ts",
            "position": "before:function",
            "code": "declare global {\n  namespace Express {\n    interface Request {\n      userId?: string;\n    }\n  }\n}",
            "why": "TypeScript'te Request tipini genişletiyoruz — req.userId kullanabilmek için. Bu OLMADAN TypeScript 'userId property does not exist' hatası verir."
        },
        {
            "order": "4.4",
            "action": "GERİ DÖN fonksiyon içine — token'ı header'dan çıkar",
            "type": "code_write",
            "file": "server/src/middleware/auth.ts",
            "code": "export function authenticate(req: Request, res: Response, next: NextFunction) {\n  const token = req.headers.authorization?.split(' ')[1];\n  if (!token) {\n    return res.status(401).json({ status: 'error', message: 'Token gerekli' });\n  }",
            "why": "Bearer token'ı Authorization header'dan çıkarıyoruz. split(' ')[1] 'Bearer TOKEN' formatından token kısmını alır. Token yoksa 401 dönüyoruz."
        },
        {
            "order": "4.5",
            "action": "Token kontrolünün altına — JWT doğrulama mantığını ekle",
            "type": "code_add",
            "file": "server/src/middleware/auth.ts",
            "position": "after:token-check",
            "code": "  try {\n    const payload = jwt.verify(token, config.jwtSecret) as { userId: string };\n    req.userId = payload.userId;\n    next();\n  } catch (error) {\n    res.status(401).json({ status: 'error', message: 'Geçersiz token' });\n  }\n}",
            "why": "jwt.verify token'ı doğrular ve payload'ı döner. 4.3'te eklediğimiz userId'ye erişim sayesinde req.userId'ye atayabiliyoruz. M1 3.11'de Socket.io için de benzer JWT doğrulaması yapmıştık."
        },
        {
            "order": "4.6",
            "action": "BAŞKA DOSYAYA GEÇ — server/src/routes/conversation.routes.ts aç — İSKELET yaz",
            "type": "code_write",
            "file": "server/src/routes/conversation.routes.ts",
            "code": "import { Router } from 'express';\n\nconst router = Router();\n\nexport default router;",
            "why": "Route dosyasını iskelet olarak oluşturuyoruz. Router() Express'in modüler routing mekanizması."
        },
        {
            "order": "4.7",
            "action": "ÜSTE ÇIK — service ve middleware import'larını ekle",
            "type": "code_add",
            "file": "server/src/routes/conversation.routes.ts",
            "position": "top",
            "code": "import { authenticate } from '../middleware/auth';\nimport { ConversationService } from '../services/conversation.service';\nimport { MessageService } from '../services/message.service';",
            "why": "4.5'te yazdığımız auth middleware'i, 1.3'teki ConversationService'i ve 2.3'teki MessageService'i import ediyoruz."
        },
        {
            "order": "4.8",
            "action": "Import'ların altına — service instance'ları oluştur ve auth middleware'i uygula",
            "type": "code_add",
            "file": "server/src/routes/conversation.routes.ts",
            "position": "after:imports",
            "code": "const conversationService = new ConversationService();\nconst messageService = new MessageService();\n\nrouter.use(authenticate);",
            "why": "Service instance'larını dosya seviyesinde oluşturuyoruz. router.use(authenticate) TÜM route'lara auth uygulanmasını sağlar — her endpoint korunmuş olur."
        },
        {
            "order": "4.9",
            "action": "Auth middleware'inin altına — GET / konuşma listesi endpoint'ini yaz",
            "type": "code_add",
            "file": "server/src/routes/conversation.routes.ts",
            "position": "after:auth",
            "code": "router.get('/', async (req, res, next) => {\n  try {\n    const conversations = await conversationService.getUserConversations(req.userId!);\n    const unreadCounts = await messageService.getUnreadCounts(req.userId!);\n    const enriched = conversations.map((conv: any) => ({\n      ...conv,\n      unreadCount: unreadCounts[conv._id.toString()] || 0,\n    }));\n    res.json({ status: 'success', data: enriched });\n  } catch (error) {\n    next(error);\n  }\n});",
            "why": "Konuşma listesine unread count ekleniyor — 3.2'de yazdığımız getUnreadCounts burada KULLANILIYOR. Enrichment pattern ile API response'u kullanılabilir hale getiriyoruz."
        },
        {
            "order": "4.10",
            "action": "GET / endpoint'inin altına — mesaj geçmişi endpoint'ini ekle",
            "type": "code_add",
            "file": "server/src/routes/conversation.routes.ts",
            "position": "after:get-conversations",
            "code": "router.get('/:id/messages', async (req, res, next) => {\n  try {\n    const { cursor, limit } = req.query;\n    const result = await messageService.getMessages(\n      req.params.id,\n      cursor as string,\n      parseInt(limit as string) || 50\n    );\n    res.json({ status: 'success', data: result });\n  } catch (error) {\n    next(error);\n  }\n});",
            "why": "2.3'teki cursor-based pagination'ı KULLANIYOR. cursor query parameter'ı opsiyonel — ilk yüklemede gönderilmez, sonraki sayfalarda gönderilir."
        },
        {
            "order": "4.11",
            "action": "Mesaj endpoint'inin altına — arama endpoint'ini ekle",
            "type": "code_add",
            "file": "server/src/routes/conversation.routes.ts",
            "position": "after:get-messages",
            "code": "router.get('/:id/search', async (req, res, next) => {\n  try {\n    const messages = await messageService.searchMessages(\n      req.params.id,\n      req.query.q as string\n    );\n    res.json({ status: 'success', data: messages });\n  } catch (error) {\n    next(error);\n  }\n});",
            "why": "2.4'teki searchMessages'ı KULLANIYOR. HER endpoint aynı pattern: try/catch + next(error). Bu tutarlılık kodun okunurluğunu artırır."
        },
        {
            "order": "4.12",
            "action": "index.ts dosyasına GERİ DÖN — route'u import et ve kaydet",
            "type": "code_modify",
            "file": "server/src/index.ts",
            "code": "import conversationRoutes from './routes/conversation.routes';\n\napp.use('/api/conversations', conversationRoutes);",
            "position": "top",
            "why": "Az önce yazdığımız route dosyasını ana server'a bağlıyoruz. /api/conversations prefix'i altındaki TÜM istekler conversation router'a yönlendirilir."
        },
        {
            "order": "4.13",
            "action": "API endpoint'lerini test et",
            "type": "validate",
            "validation": "curl veya Postman ile GET /api/conversations isteği yapıldığında konuşma listesi dönmeli. Authorization header'sız isteklerde 401 hatası alınmalı.",
            "why": "REST API'nin doğru çalışması, frontend'in veri çekebilmesi için ön koşuldur."
        }
    ]

    # ==========================================
    # M3 Step 1: Socket.io Client ve Global State
    # socket-store.ts (42 lines) and chat-store.ts (53 lines)
    # ==========================================
    m3 = milestones[2]
    m3_step1 = m3['steps'][0]  # step 1
    m3_step1['substeps'] = [
        {
            "order": "1.1",
            "action": "client/src/stores/ klasörünü oluştur (yoksa)",
            "type": "terminal",
            "command": "mkdir -p client/src/stores",
            "expected_output": "Klasör oluşturuldu",
            "why": "Frontend state yönetimi dosyaları bu klasörde yaşayacak. Zustand store'ları burada olacak."
        },
        {
            "order": "1.2",
            "action": "client/src/stores/socket-store.ts dosyasını aç — İSKELET interface yaz",
            "type": "code_write",
            "file": "client/src/stores/socket-store.ts",
            "code": "export {};  // placeholder",
            "why": "Frontend tarafına geçtik. İlk önce dosyayı oluşturuyoruz, sonra Zustand store'unu adım adım inşa edeceğiz."
        },
        {
            "order": "1.3",
            "action": "ÜSTE ÇIK — zustand ve socket.io-client import'larını ekle",
            "type": "code_write",
            "file": "client/src/stores/socket-store.ts",
            "code": "import { create } from 'zustand';\nimport { io, Socket } from 'socket.io-client';",
            "why": "M1 1.4'te kurduğumuz zustand ve socket.io-client'ı import ediyoruz. create ile Zustand store oluşturacağız, io ile Socket.io bağlantısı kuracağız."
        },
        {
            "order": "1.4",
            "action": "Import'ların altına — SocketStore interface'ini tanımla",
            "type": "code_add",
            "file": "client/src/stores/socket-store.ts",
            "position": "after:imports",
            "code": "\ninterface SocketStore {\n  socket: Socket | null;\n  isConnected: boolean;\n  connect: (token: string) => void;\n  disconnect: () => void;\n}",
            "why": "TypeScript ile store'un ŞEKLİNİ önce tanımlıyoruz. Socket null olabilir çünkü bağlantı kurulmadan önce null. connect token alır, disconnect parametre almaz."
        },
        {
            "order": "1.5",
            "action": "Interface'in altına — store iskeletini oluştur (state kısmı)",
            "type": "code_add",
            "file": "client/src/stores/socket-store.ts",
            "position": "after:interface",
            "code": "\nexport const useSocketStore = create<SocketStore>((set, get) => ({\n  socket: null,\n  isConnected: false,",
            "why": "Zustand store'unun STATE kısmını yazıyoruz. Başlangıçta socket null ve bağlantı yok. set ile state güncelleyeceğiz, get ile okuyacağız."
        },
        {
            "order": "1.6",
            "action": "State'in altına — connect fonksiyonunu yaz (bağlantı oluşturma)",
            "type": "code_add",
            "file": "client/src/stores/socket-store.ts",
            "position": "after:state",
            "code": "\n  connect: (token: string) => {\n    const socket = io(import.meta.env.VITE_API_URL || 'http://localhost:3001', {\n      auth: { token },\n      reconnection: true,\n      reconnectionAttempts: 10,\n      reconnectionDelay: 1000,\n    });",
            "why": "auth: { token } ile M1 3.11'de yazdığımız Socket.io auth middleware'ine JWT gönderiyoruz. reconnection: true ile bağlantı koptuğunda OTOMATİK yeniden bağlanır."
        },
        {
            "order": "1.7",
            "action": "Socket oluşturmanın altına — event listener'ları ekle",
            "type": "code_add",
            "file": "client/src/stores/socket-store.ts",
            "position": "after:socket-create",
            "code": "    socket.on('connect', () => {\n      set({ isConnected: true });\n    });\n\n    socket.on('disconnect', () => {\n      set({ isConnected: false });\n    });\n\n    socket.on('connect_error', (error) => {\n      console.error('Connection error:', error.message);\n    });",
            "why": "Bağlantı durumu değiştiğinde Zustand state'i güncelleniyor. connect_error ile hata loglanır — debug için önemli."
        },
        {
            "order": "1.8",
            "action": "Event listener'ların altına — socket'i state'e kaydet ve connect fonksiyonunu kapat",
            "type": "code_add",
            "file": "client/src/stores/socket-store.ts",
            "position": "after:listeners",
            "code": "    set({ socket });\n  },",
            "why": "Oluşturduğumuz socket'i Zustand state'ine kaydediyoruz. Artık useSocketStore().socket ile her component'ten erişilebilir."
        },
        {
            "order": "1.9",
            "action": "Connect'in altına — disconnect fonksiyonunu yaz ve store'u kapat",
            "type": "code_add",
            "file": "client/src/stores/socket-store.ts",
            "position": "after:connect",
            "code": "\n  disconnect: () => {\n    get().socket?.disconnect();\n    set({ socket: null, isConnected: false });\n  },\n}));",
            "why": "get() ile mevcut socket'e erişip disconnect() çağırıyoruz. State'i sıfırlıyoruz — socket null, bağlantı yok."
        },
        {
            "order": "1.10",
            "action": "BAŞKA DOSYAYA GEÇ — client/src/stores/chat-store.ts aç — İSKELET interface yaz",
            "type": "code_write",
            "file": "client/src/stores/chat-store.ts",
            "code": "import { create } from 'zustand';",
            "why": "İkinci store dosyasına geçiyoruz. Zustand pattern'ını 1.3-1.9'da öğrendik — aynı pattern'ı tekrarlayacağız."
        },
        {
            "order": "1.11",
            "action": "Import'un altına — ChatStore interface'ini tanımla",
            "type": "code_add",
            "file": "client/src/stores/chat-store.ts",
            "position": "after:import",
            "code": "\ninterface ChatStore {\n  conversations: any[];\n  activeConversation: string | null;\n  messages: Record<string, any[]>;\n  typingUsers: Record<string, string[]>;\n  setConversations: (conversations: any[]) => void;\n  setActiveConversation: (id: string | null) => void;\n  addMessage: (conversationId: string, message: any) => void;\n  setMessages: (conversationId: string, messages: any[]) => void;\n  setTyping: (conversationId: string, userId: string, isTyping: boolean) => void;\n}",
            "why": "Chat state'i: konuşma listesi, aktif konuşma, mesajlar (conversationId bazında) ve typing kullanıcılar. Record<string, any[]> ile her konuşmanın mesajları AYRI AYRI saklanır."
        },
        {
            "order": "1.12",
            "action": "Interface'in altına — store'u oluştur (basit setter'lar)",
            "type": "code_add",
            "file": "client/src/stores/chat-store.ts",
            "position": "after:interface",
            "code": "\nexport const useChatStore = create<ChatStore>((set, get) => ({\n  conversations: [],\n  activeConversation: null,\n  messages: {},\n  typingUsers: {},\n\n  setConversations: (conversations) => set({ conversations }),\n  setActiveConversation: (id) => set({ activeConversation: id }),",
            "why": "Basit setter fonksiyonları: setConversations tüm listeyi değiştirir, setActiveConversation seçili konuşmayı belirler."
        },
        {
            "order": "1.13",
            "action": "Setter'ların altına — addMessage fonksiyonunu ekle",
            "type": "code_add",
            "file": "client/src/stores/chat-store.ts",
            "position": "after:setters",
            "code": "\n  addMessage: (conversationId, message) => {\n    set((state) => ({\n      messages: {\n        ...state.messages,\n        [conversationId]: [\n          ...(state.messages[conversationId] || []),\n          message,\n        ],\n      },\n    }));\n  },",
            "why": "Yeni mesaj ilgili konuşmanın dizisinin SONUNA eklenir. spread ile mevcut mesajlar korunur. conversationId bazında ayrı diziler kullanmak, farklı konuşmalar arası karışmayı ÖNLER."
        },
        {
            "order": "1.14",
            "action": "addMessage'ın altına — setMessages fonksiyonunu ekle",
            "type": "code_add",
            "file": "client/src/stores/chat-store.ts",
            "position": "after:addMessage",
            "code": "\n  setMessages: (conversationId, messages) => {\n    set((state) => ({\n      messages: { ...state.messages, [conversationId]: messages },\n    }));\n  },",
            "why": "Tüm mesaj listesini değiştirir — ilk yüklemede veya pagination'da kullanılır. addMessage tek mesaj ekler, setMessages TÜM listeyi set eder."
        },
        {
            "order": "1.15",
            "action": "setMessages'ın altına — setTyping fonksiyonunu ekle ve store'u kapat",
            "type": "code_add",
            "file": "client/src/stores/chat-store.ts",
            "position": "after:setMessages",
            "code": "\n  setTyping: (conversationId, userId, isTyping) => {\n    set((state) => {\n      const current = state.typingUsers[conversationId] || [];\n      const updated = isTyping\n        ? [...new Set([...current, userId])]\n        : current.filter((id) => id !== userId);\n      return {\n        typingUsers: { ...state.typingUsers, [conversationId]: updated },\n      };\n    });\n  },\n}));",
            "why": "Set ile typing users'da duplicate ÖNLENIR. isTyping true ise kullanıcıyı ekle, false ise çıkar. M1 4.10-4.11'deki typing event'leri bu fonksiyonu TETİKLEYECEK."
        },
        {
            "order": "1.16",
            "action": "Store'ların import edilip kullanılabildiğini doğrula",
            "type": "validate",
            "validation": "Client dev server çalışıyorken browser console'da hata olmamalı. useSocketStore ve useChatStore import edilebilmeli.",
            "why": "Store'ların doğru çalışması, TÜM frontend'in temelini oluşturur. Hatalı store tanımı uygulamayı tamamen kırar."
        }
    ]

    # ==========================================
    # M3 Step 3: Chat Window - already has skeleton approach, but substep 3.4 has too many lines
    # ==========================================
    m3_step3 = m3['steps'][2]  # step 3
    m3_step3['substeps'] = [
        {
            "order": "3.1",
            "action": "client/src/components/chat-window.tsx dosyasını aç — İSKELET component yaz",
            "type": "code_write",
            "file": "client/src/components/chat-window.tsx",
            "code": "export function ChatWindow({ conversationId }: { conversationId: string }) {\n  return (\n    <div className=\"flex h-full flex-col\">\n      <div className=\"border-b px-4 py-3\">\n        <h2 className=\"font-semibold\">Konuşma</h2>\n      </div>\n      <div className=\"flex-1 p-4\">\n        <p className=\"text-gray-400\">Mesajlar yüklenecek...</p>\n      </div>\n      <div className=\"border-t p-4\">\n        <p className=\"text-gray-400\">Input alanı gelecek...</p>\n      </div>\n    </div>\n  );\n}",
            "why": "İskelet ile LAYOUT'u kuruyoruz: üstte header, ortada mesaj alanı (flex-1 ile genişler), altta input. İlk önce yapıyı görüp DOĞRULUYORUZ."
        },
        {
            "order": "3.2",
            "action": "ÜSTE ÇIK — React hook'ları import et",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "top",
            "code": "import { useState, useEffect, useRef, useCallback } from 'react';",
            "why": "useState input değeri için, useEffect veri çekme için, useRef scroll target için, useCallback fonksiyon memoization için gerekli."
        },
        {
            "order": "3.3",
            "action": "ÜSTE ÇIK — store ve api import'larını ekle",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "after:react-imports",
            "code": "import { useSocketStore } from '../stores/socket-store';\nimport { useChatStore } from '../stores/chat-store';\nimport { api } from '../lib/api';",
            "why": "1.5-1.9'da yazdığımız socket store, 1.12-1.15'teki chat store ve 2.1'deki api helper'ı import ediyoruz."
        },
        {
            "order": "3.4",
            "action": "GERİ DÖN component içine — state tanımlarını ve store bağlantılarını ekle",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "inside:component-top",
            "code": "  const [input, setInput] = useState('');\n  const [isLoading, setIsLoading] = useState(false);\n  const messagesEndRef = useRef<HTMLDivElement>(null);\n  const { socket } = useSocketStore();\n  const { messages, typingUsers, setMessages } = useChatStore();",
            "why": "input: kullanıcının yazdığı metin. isLoading: mesaj yüklenirken spinner. messagesEndRef: otomatik scroll için div referansı. Store'lardan socket ve mesaj state'i çekiliyor."
        },
        {
            "order": "3.5",
            "action": "State'lerin altına — mesaj ve typing verilerini conversationId'ye göre filtrele",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "after:state",
            "code": "  const conversationMessages = messages[conversationId] || [];\n  const typing = typingUsers[conversationId] || [];",
            "why": "1.13-1.15'te tanımladığımız Record<string, any[]> yapısından aktif konuşmanın verilerini çekiyoruz. || [] ile undefined durumunda boş dizi."
        },
        {
            "order": "3.6",
            "action": "Filtrelemenin altına — mesaj geçmişini yükleyen useEffect ekle",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "after:filter",
            "code": "  useEffect(() => {\n    setIsLoading(true);\n    api.get(`/conversations/${conversationId}/messages`)\n      .then(({ data }) => setMessages(conversationId, data.data.messages))\n      .finally(() => setIsLoading(false));\n    socket?.emit('message:read', { conversationId });\n  }, [conversationId]);",
            "why": "M2 4.10'da yazdığımız /messages endpoint'inden mesaj geçmişini çekiyor. conversationId DEĞİŞTİĞİNDE yeniden yüklenir. message:read ile mesajları okundu işaretliyoruz."
        },
        {
            "order": "3.7",
            "action": "Yükleme useEffect'inin altına — otomatik scroll useEffect ekle",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "after:load-effect",
            "code": "  useEffect(() => {\n    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });\n  }, [conversationMessages.length]);",
            "why": "Yeni mesaj geldiğinde en alta scroll yapılır. behavior: 'smooth' ile yumuşak kaydırma. conversationMessages.length DEĞİŞTİĞİNDE tetiklenir."
        },
        {
            "order": "3.8",
            "action": "Scroll useEffect'inin altına — sendMessage fonksiyonunu yaz",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "after:scroll-effect",
            "code": "  const sendMessage = useCallback(() => {\n    if (!input.trim() || !socket) return;\n    socket.emit('message:send', {\n      conversationId,\n      content: input.trim(),\n      type: 'text',\n    }, (response: any) => {\n      if (response.status !== 'ok') console.error('Mesaj gönderilemedi');\n    });\n    setInput('');\n    socket.emit('typing:stop', { conversationId });\n  }, [input, socket, conversationId]);",
            "why": "M1 4.6-4.9'da yazdığımız message:send event'ini tetikliyor. callback ile gönderim onayı alınır. Mesaj gönderildikten sonra input TEMİZLENİR ve typing durdurulur."
        },
        {
            "order": "3.9",
            "action": "sendMessage'ın altına — handleTyping fonksiyonunu yaz",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "after:sendMessage",
            "code": "  const handleTyping = useCallback(() => {\n    socket?.emit('typing:start', { conversationId });\n  }, [socket, conversationId]);",
            "why": "M1 4.10'daki typing:start event'ini tetikliyor. Her tuş basımında çağrılır — production'da throttle/debounce eklenmeli."
        },
        {
            "order": "3.10",
            "action": "Fonksiyonların altına — mesaj listesi JSX'ini yaz (header + mesajlar)",
            "type": "code_write",
            "file": "client/src/components/chat-window.tsx",
            "code": "  return (\n    <div className=\"flex h-full flex-col\">\n      <div className=\"border-b px-4 py-3\">\n        <h2 className=\"font-semibold\">Konuşma</h2>\n      </div>\n      <div className=\"flex-1 overflow-y-auto p-4 space-y-3\">\n        {isLoading ? (\n          <div className=\"text-center text-gray-400\">Yükleniyor...</div>\n        ) : (\n          conversationMessages.map((msg: any) => (\n            <div key={msg._id} className=\"p-2 bg-gray-800 rounded\">\n              <p className=\"text-sm text-gray-300\">{msg.content}</p>\n            </div>\n          ))\n        )}",
            "why": "3.1'deki iskelet layout'u DOLDURUYORUZ. isLoading sırasında spinner, değilse mesaj listesi. overflow-y-auto ile mesajlar ekrandan taşınca scroll yapılır."
        },
        {
            "order": "3.11",
            "action": "Mesaj listesinin altına — typing indicator ve scroll div ekle",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "after:messages",
            "code": "        {typing.length > 0 && (\n          <div className=\"text-sm text-gray-400 italic\">\n            {typing.length === 1 ? 'Yazıyor...' : `${typing.length} kişi yazıyor...`}\n          </div>\n        )}\n        <div ref={messagesEndRef} />\n      </div>",
            "why": "1.15'te tanımladığımız setTyping ile güncellenen typing state'i burada GÖSTERİLİYOR. messagesEndRef ile 3.7'deki scrollIntoView ÇALIŞIR."
        },
        {
            "order": "3.12",
            "action": "Scroll div'in altına — input alanı ve gönder butonunu ekle",
            "type": "code_add",
            "file": "client/src/components/chat-window.tsx",
            "position": "after:typing",
            "code": "      <div className=\"border-t p-4\">\n        <div className=\"flex gap-2\">\n          <textarea\n            value={input}\n            onChange={(e) => { setInput(e.target.value); handleTyping(); }}\n            onKeyDown={(e) => {\n              if (e.key === 'Enter' && !e.shiftKey) {\n                e.preventDefault();\n                sendMessage();\n              }\n            }}\n            placeholder=\"Mesajınızı yazın... (@ai ile AI asistanı kullanın)\"\n            className=\"flex-1 resize-none rounded-lg border p-2 focus:border-blue-500 focus:outline-none border-gray-700 bg-gray-800\"\n            rows={1}\n          />\n          <button\n            onClick={sendMessage}\n            disabled={!input.trim()}\n            className=\"rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50\"\n          >\n            Gönder\n          </button>\n        </div>\n      </div>\n    </div>\n  );\n}",
            "why": "Enter ile gönderme, Shift+Enter ile yeni satır standart chat UX'i. disabled={!input.trim()} boş mesaj göndermeyi engeller. 3.8'deki sendMessage ve 3.9'daki handleTyping burada BAĞLANIYOR."
        },
        {
            "order": "3.13",
            "action": "chat.tsx dosyasına GERİ DÖN — ChatWindow'u import et ve placeholder'ı değiştir",
            "type": "code_modify",
            "file": "client/src/pages/chat.tsx",
            "code": "import { ChatWindow } from '../components/chat-window';\n\n// Placeholder <p> tag'ini şununla değiştir:\n{activeConversation && <ChatWindow conversationId={activeConversation} />}",
            "position": "top",
            "why": "2.4'te yazdığımız placeholder'ı az önce oluşturduğumuz ChatWindow component'i ile DEĞİŞTİRİYORUZ."
        },
        {
            "order": "3.14",
            "action": "Mesaj gönderme ve alma işlevini doğrula",
            "type": "validate",
            "validation": "Mesaj yazıp Enter'a basıldığında mesaj gönderilmeli ve ekranda görünmeli. Typing indicator yazarken görünmeli.",
            "why": "Chat uygulamasının TEMEL işlevi olan mesaj gönderme ve almanın çalışması, MVP için en kritik doğrulamadır."
        }
    ]

    # ==========================================
    # M4 Step 2: AI Socket Event Handler
    # Substep 2.3 dumps 71 lines
    # ==========================================
    m4 = milestones[3]
    m4_step2 = m4['steps'][1]  # step 2
    m4_step2['substeps'] = [
        {
            "order": "2.1",
            "action": "server/src/events/ai-handler.ts dosyasını aç — İSKELET fonksiyon yaz",
            "type": "code_write",
            "file": "server/src/events/ai-handler.ts",
            "code": "import { Socket, Server } from 'socket.io';\n\nexport function setupAIHandler(io: Server, socket: Socket) {\n  // ai:ask event handler buraya gelecek\n}",
            "why": "AI event handler'ı AYRI dosyada yönetilir — M1 4.1'deki socket-handler.ts ile aynı pattern. Modülerlik sayesinde AI özelliğini BAĞIMSIZ olarak geliştirebilir ve test edebiliriz."
        },
        {
            "order": "2.2",
            "action": "ÜSTE ÇIK — AI service import'unu ekle",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "top",
            "code": "import { AIService } from '../services/ai.service';\n\nconst aiService = new AIService();",
            "why": "1.4'te yazdığımız AIService'i import ediyoruz. Instance'ı dosya seviyesinde oluşturuyoruz — her event'te yeniden oluşturmaya gerek yok."
        },
        {
            "order": "2.3",
            "action": "ÜSTE ÇIK — Message ve Conversation model import'larını ekle",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "top",
            "code": "import { Message } from '../models/message.model';\nimport { Conversation } from '../models/conversation.model';",
            "why": "M1'de yazdığımız modelleri import ediyoruz — AI yanıtını veritabanına KAYDEDECEĞİZ ve konuşma geçmişini OKUYACAĞIZ."
        },
        {
            "order": "2.4",
            "action": "GERİ DÖN fonksiyon içine — ai:ask event handler'ını aç",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "inside:function",
            "code": "  socket.on('ai:ask', async (data, callback) => {\n    const { conversationId, question } = data;\n    const userId = socket.data.userId;\n\n    try {",
            "why": "Event handler'ı AÇIYORUZ. data'dan conversationId ve question'ı destructure ediyoruz. userId'yi M1 3.11'deki auth middleware'den alıyoruz."
        },
        {
            "order": "2.5",
            "action": "try bloğunun içine — kullanıcı mesajını veritabanına kaydet",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "inside:try",
            "code": "      // Kullanıcı mesajını kaydet\n      const userMessage = await Message.create({\n        conversationId,\n        sender: userId,\n        content: question,\n        type: 'text',\n        readBy: [userId],\n      });\n      io.to(conversationId).emit('message:received',\n        await userMessage.populate('sender', 'name avatar')\n      );",
            "why": "Önce kullanıcının sorusunu normal mesaj olarak kaydedip odadaki herkese gönderiyoruz. M1 4.7-4.8'deki mesaj kaydetme pattern'ının AYNISI."
        },
        {
            "order": "2.6",
            "action": "Kullanıcı mesajının altına — konuşma geçmişini context olarak al",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "after:user-message",
            "code": "      // Son mesajları context olarak al\n      const history = await Message.find({ conversationId })\n        .sort({ createdAt: -1 })\n        .limit(10)\n        .lean();",
            "why": "AI'ın konuşmanın bağlamını ANLAMası için son 10 mesajı çekiyoruz. 1.4'te tanımladığımız generateStreamingResponse bu history'yi kullanacak."
        },
        {
            "order": "2.7",
            "action": "History'nin altına — placeholder AI mesajı oluştur",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "after:history",
            "code": "      // AI yanıtı için placeholder mesaj oluştur\n      const aiMessage = await Message.create({\n        conversationId,\n        sender: userId,\n        content: '',\n        type: 'ai_response',\n        readBy: [userId],\n      });",
            "why": "BOŞ bir AI mesajı oluşturuyoruz — streaming sırasında token'lar gelecek, sonunda tam içerik ile GÜNCELLENECEK. M1 2.8'de tanımladığımız 'ai_response' tipi burada KULLANILIYOR."
        },
        {
            "order": "2.8",
            "action": "Placeholder'ın altına — streaming başladı bildirimi gönder",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "after:placeholder",
            "code": "      // Streaming başladı bildirimi\n      io.to(conversationId).emit('ai:stream:start', {\n        messageId: aiMessage.id,\n        conversationId,\n      });",
            "why": "Client'a 'streaming başlıyor' sinyali gönderiyoruz. Frontend bu event'i alınca cursor animasyonu gösterecek."
        },
        {
            "order": "2.9",
            "action": "Bildirimin altına — streaming yanıtı başlat",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "after:stream-start",
            "code": "      // Streaming yanıt\n      const fullResponse = await aiService.generateStreamingResponse(\n        question,\n        history.reverse(),\n        (token) => {\n          io.to(conversationId).emit('ai:stream:token', {\n            messageId: aiMessage.id,\n            token,\n          });\n        }\n      );",
            "why": "1.5'te yazdığımız generateStreamingResponse'un onToken callback'i HER token geldiğinde Socket.io ile emit eder — ChatGPT'nin yazıyor efektini replike eder."
        },
        {
            "order": "2.10",
            "action": "Streaming'in altına — final mesajı güncelle ve tamamlandı bildirimi gönder",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "after:streaming",
            "code": "      // Final mesajı güncelle\n      await Message.findByIdAndUpdate(aiMessage.id, { content: fullResponse });\n\n      io.to(conversationId).emit('ai:stream:end', {\n        messageId: aiMessage.id,\n        fullContent: fullResponse,\n      });",
            "why": "2.7'de oluşturduğumuz BOŞ placeholder mesajı tam yanıtla güncelliyoruz. ai:stream:end ile client'a 'streaming bitti' sinyali gönderiyoruz."
        },
        {
            "order": "2.11",
            "action": "Stream end'in altına — konuşmayı güncelle ve handler'ı kapat",
            "type": "code_add",
            "file": "server/src/events/ai-handler.ts",
            "position": "after:stream-end",
            "code": "      await Conversation.findByIdAndUpdate(conversationId, {\n        lastMessage: aiMessage.id,\n        lastActivity: new Date(),\n      });\n\n      callback({ status: 'ok' });\n    } catch (error) {\n      console.error('AI error:', error);\n      callback({ status: 'error', message: 'AI yanıt veremedi' });\n    }\n  });\n}",
            "why": "Konuşmanın lastMessage ve lastActivity alanlarını güncelliyoruz. callback ile client'a onay gönderiyoruz. catch bloğunda hata durumu yakalanıp client'a bildirilir."
        },
        {
            "order": "2.12",
            "action": "socket-handler.ts dosyasına GERİ DÖN — AI handler'ı import et ve bağla",
            "type": "code_modify",
            "file": "server/src/events/socket-handler.ts",
            "code": "import { setupAIHandler } from './ai-handler';\n\n// io.on('connection') callback'inin içine ekle:\nsetupAIHandler(io, socket);",
            "position": "top",
            "why": "M1 4.1'de yazdığımız socket-handler'a AI handler'ı BAĞLIYORUZ. Her socket bağlantısında AI handler da kurulur."
        },
        {
            "order": "2.13",
            "action": "AI streaming'in çalıştığını doğrula",
            "type": "validate",
            "validation": "Client'tan ai:ask event'i gönderildiğinde ai:stream:start, ardından ai:stream:token event'leri ve son olarak ai:stream:end event'i gelmeli.",
            "why": "Streaming akışının doğru sırada çalışması, kullanıcıya kesintisiz AI deneyimi sunmak için kritiktir."
        }
    ]

    # Write the result
    with open('content/projects/project-03.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Validate
    with open('content/projects/project-03.json', 'r', encoding='utf-8') as f:
        validated = json.load(f)

    # Count substeps
    total = 0
    for m in validated['milestones']:
        for step in m['steps']:
            n = len(step.get('substeps', []))
            total += n
            # Check max code lines
            for sub in step.get('substeps', []):
                code = sub.get('code', '')
                if code:
                    lines = code.count('\n') + 1
                    if lines > 12:
                        print(f"  WARNING: {sub['order']} has {lines} lines of code")

    print(f"\nTotal substeps: {total}")
    print("JSON validated successfully!")


if __name__ == '__main__':
    main()
