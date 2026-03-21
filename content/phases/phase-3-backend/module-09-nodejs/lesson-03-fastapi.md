---
title: "FastAPI ile Modern Python Backend"
id: mod-09-node/lesson-03
estimated_minutes: 75
order: 3
tags: ["fastapi", "python", "pydantic", "sqlalchemy", "async", "backend", "api"]
prerequisites: ["mod-02-python/lesson-03", "mod-09-node/lesson-01"]
---

# FastAPI ile Modern Python Backend

:::realworld
Instagram, Uber, Netflix ve Microsoft gibi devler Python backend kullanyor. FastAPI, 2018'de ortaya çıkan ve kısa surede GitHub'da 75.000+ yıldız toplayan bir framework. Neden? Çünkü type hint'ler sayesinde otomatik API dokümantasyonu üretiyor, async destegi ile Node.js seviyesinde performans sunuyor ve Pydantic ile runtime'da veri doğrulama yapiyor. Spotify, FastAPI ile mikro servislerini yeniden yazdığında geliştirme sürecini %40 kısalttı. Bu derste, FastAPI'yi senior seviyede öğrenecek ve production-ready bir backend yazacaksin.
:::

## Neden FastAPI?

Express.js ve Django ile karsilastiralim:

| Özellik | Express.js | Django | FastAPI |
|---------|-----------|--------|---------|
| Tip güvenliği | Yok (TS ile eklenebilir) | Sınırlı | Native (Python type hints) |
| Async destegi | Dogal | Django 4.1+ ile kismi | Dogal (ASGI) |
| Otomatik dokümantasyon | Swagger eklentisi gerekli | DRF ile mumkun | Dahili (Swagger + ReDoc) |
| Veri doğrulama | express-validator / Zod | Serializer / Forms | Pydantic (çok güçlü) |
| Performans | Yüksek | Orta | Çok yüksek |
| Öğrenme egrisi | Düşük | Yüksek | Düşük-Orta |
| ORM | Prisma, Sequelize, vb. | Django ORM | SQLAlchemy, Tortoise |

:::deha-tip
Deha seviyesi gelisitriciler framework secimini hype'a gore değil, projenin ihtiyaclarina gore yapar. FastAPI'nin gerçek gücü şu üç seyde: (1) Pydantic ile compile-time benzeri tip güvenliği, (2) async/await ile yüksek concurrency, (3) OpenAPI spec'in otomatik uretilmesi. Eger projen CPU-intensive is yapiyorsa (ML model inference gibi), FastAPI + async harika bir kombinasyon. Eger full-stack monolith istiyorsan, Django daha iyi olabilir. Senior mühendis "en iyi framework" aramaz, "bu problem için en uygun arac" arar.
:::

## Kurulum ve Ilk Proje

:::code[bash]{title="FastAPI Projesi Oluşturma (uv ile)"}
# uv ile proje oluştur (pip yerine uv kullanıyoruz - çok daha hızlı)
uv init fastapi-project
cd fastapi-project

# Bağımlılıkları ekle
uv add fastapi uvicorn[standard] pydantic[email] sqlalchemy[asyncio] alembic
uv add --dev pytest httpx pytest-asyncio ruff

# Proje yapısı
mkdir -p app/{routers,services,schemas,models,core,dependencies}
touch app/__init__.py
touch app/{routers,services,schemas,models,core,dependencies}/__init__.py
:::

:::code[python]{title="app/main.py - Minimal FastAPI Uygulaması"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Senior API",
    description="Production-ready FastAPI uygulaması",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
)

# CORS ayarlari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "FastAPI çalışıyor!", "status": "ok"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
:::

:::code[bash]{title="Sunucuyu Başlat"}
# Development modunda çalıştır
uvicorn app.main:app --reload --port 8000

# Tarayicida ac:
# http://localhost:8000/docs    -> Swagger UI (interaktif API dokümantasyonu)
# http://localhost:8000/redoc   -> ReDoc (okunabilir dokümantasyon)
:::

:::beginner-mistake
Yaygin hata: `uvicorn main:app` yazip "module not found" hatasi almak. FastAPI'de app nesnesi hangi dosyadaysa, tam yolunu belirtmelisin: `uvicorn app.main:app`. Ayrica `--reload` flag'ini SADECE development'ta kullan. Production'da bu flag performansı oldurur çünkü her dosya degisikliginde sunucu yeniden baslar.
:::

## Senior-Level Proje Yapısı

:::code[text]{title="Production-Ready Klasor Yapısı"}
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance, middleware, startup/shutdown
│   ├── config.py               # Pydantic Settings (env variables)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py         # SQLAlchemy engine, session
│   │   ├── security.py         # JWT, password hashing
│   │   └── exceptions.py       # Custom exception handlers
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Base SQLAlchemy model
│   │   ├── user.py             # User ORM model
│   │   └── post.py             # Post ORM model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas (Create, Read, Update)
│   │   └── post.py             # Post Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py             # /auth/* endpoints
│   │   ├── users.py            # /users/* endpoints
│   │   └── posts.py            # /posts/* endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py     # User business logic
│   │   └── post_service.py     # Post business logic
│   └── dependencies/
│       ├── __init__.py
│       ├── auth.py             # get_current_user dependency
│       └── database.py         # get_db dependency
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py             # Test fixtures
│   ├── test_auth.py
│   └── test_users.py
├── alembic.ini
├── pyproject.toml
└── .env
:::

:::senior-learns
Senior/CTO bu yapiyi şöyle değerlendirir: "Separation of Concerns" prensibi tam uygulanmis. Router'lar sadece HTTP katmani, service'ler is mantigi, schema'lar veri doğrulama, model'ler veritabanı. Yeni bir geliştirici geldiginde nereye bakacagini hemen anlar. Bu yapı monolith için yeterli; mikroservis gecisinde her service dosyasi kendi servisine donusebilir.

**Karar Verme Sureci — FastAPI vs Django vs Flask:**
- **FastAPI**: Async-native, otomatik OpenAPI docs, Pydantic validation. Trade-off: Django'nun admin panel, ORM, auth gibi "batteries-included" ozelliklerini sunmaz. Kullanim: API-first projeler, microservice'ler, yuksek performans.
- **Django + DRF**: Admin panel, ORM, auth, migrations hazir. Trade-off: Async destegi sinirli, monolith yapisina yonlendirir. Kullanim: Content-heavy siteler, admin panel gereken projeler, hizli MVP.
- **Flask**: Minimalist, ogrenmesi kolay. Trade-off: Async yok, buyuk projelerde yapi dayatmadigi icin spagetti koda yol acar. Kullanim: Cok kucuk API'ler, legacy projeler.
- **Senior karar agaci**: "Admin panel lazim mi? Django. Sadece API + yuksek performans? FastAPI. Hepsi icin: FastAPI + SQLAlchemy."

**Anti-pattern Farkindaligi:**
- **Router'da is mantigi**: Endpoint icerisinde dogrudan database sorgusu, email gonderimi yapmak. Test edilmesi imkansiz, tekrar kullanilmasi olanaksiz kod uretir. Cozum: service layer pattern.
- **Global state**: Modul seviyesinde `db = get_db()` gibi global degiskenler. Test'lerde mock'lanamaz, race condition riski var. Cozum: Dependency Injection ile `Depends()`.
- **Tek schema her is icin**: Ayni Pydantic model'i hem create, hem update, hem response icin kullanmak. Cozum: UserCreate, UserUpdate, UserResponse ayir.

**Gercek Dunya Deneyimi:** Bir fintech projesinde baslangicta Flask ile basladik. 50 endpoint'e ulasinca test yazmak kabusa dondu — dependency injection yok, her endpoint icinde global DB baglantiSI, mock'lamak icin monkey-patching. FastAPI'ye gecis 2 hafta surdu ama sonrasinda test coverage %30'dan %85'e cikti. Depends() sistemi sayesinde her endpoint izole test edilebilir hale geldi.
:::

## Pydantic v2 ile Veri Doğrulama

Pydantic, FastAPI'nin belkemigi. Runtime'da type checking ve veri doğrulama yapar.

:::code[python]{title="app/schemas/user.py - Pydantic Schemas"}
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field


class UserBase(BaseModel):
    """Tüm User schema'larinin temel sınıfı."""
    email: EmailStr
    username: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Kullanıcı adi (sadece harf, rakam ve alt cizgi)",
        examples=["john_doe"],
    )


class UserCreate(UserBase):
    """Kullanıcı oluşturma için schema."""
    password: str = Field(min_length=8, max_length=128)
    password_confirm: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("En az bir büyük harf olmali")
        if not any(c.isdigit() for c in v):
            raise ValueError("En az bir rakam olmali")
        if not any(c in "!@#$%^&*()_+-=" for c in v):
            raise ValueError("En az bir ozel karakter olmali")
        return v

    @field_validator("password_confirm")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Sifreler eslesmiyor")
        return v


class UserRead(UserBase):
    """Kullanıcı okuma için schema (API response)."""
    id: int
    is_active: bool
    created_at: datetime

    @computed_field
    @property
    def display_name(self) -> str:
        """Username'den goruntu adi uret."""
        return self.username.replace("_", " ").title()

    model_config = {
        "from_attributes": True,  # ORM model'den dönüşüm için (eski orm_mode)
    }


class UserUpdate(BaseModel):
    """Kullanıcı güncelleme için schema (partial update)."""
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=30)
    bio: str | None = Field(default=None, max_length=500)


class UserList(BaseModel):
    """Sayfalanmis kullanıcı listesi."""
    items: list[UserRead]
    total: int
    page: int
    per_page: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return (self.total + self.per_page - 1) // self.per_page
:::

:::code[python]{title="Pydantic Kullanımı - Örnekler"}
# Schema'yi kullanma
user_data = {
    "email": "test@example.com",
    "username": "john_doe",
    "password": "MyPass123!",
    "password_confirm": "MyPass123!",
}

user = UserCreate(**user_data)
print(user.model_dump())  # dict'e cevir
print(user.model_dump(exclude={"password", "password_confirm"}))  # hassas alanlari çıkar
print(user.model_dump_json())  # JSON string

# Hatali veri
try:
    bad_user = UserCreate(
        email="gecersiz-email",
        username="ab",  # çok kısa
        password="zayif",
        password_confirm="farklı",
    )
except Exception as e:
    print(e.errors())
    # [
    #   {"type": "value_error", "loc": ["email"], "msg": "..."},
    #   {"type": "string_too_short", "loc": ["username"], "msg": "..."},
    #   ...
    # ]
:::

:::must-note
Pydantic v2'de önemli değişiklikler:
- `orm_mode = True` yerine `from_attributes = True` kullanılıyor
- `@validator` yerine `@field_validator` kullanılıyor
- `@root_validator` yerine `@model_validator` kullanılıyor
- `Config` inner class yerine `model_config` dict kullanılıyor
- v2, Rust ile yazilmis core sayesinde v1'den 5-50x daha hızlı
:::

## Dependency Injection Sistemi

FastAPI'nin en güçlü özelliklerinden biri Dependency Injection (DI) sistemidir. Spring Boot'taki DI'ya benzer ama çok daha basit.

:::code[python]{title="app/core/database.py - Veritabanı Baglantisi"}
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/mydb"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,        # SQL loglarini kapat (production)
    pool_size=20,      # Connection pool boyutu
    max_overflow=10,   # Ekstra bağlantı sayisi
    pool_timeout=30,   # Bağlantı bekleme süresi (saniye)
    pool_recycle=1800, # Bağlantıları 30 dakikada yenile
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
:::

:::code[python]{title="app/dependencies/database.py - get_db Dependency"}
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Her request için bir veritabanı oturumu oluşturur.
    Request bittiginde oturumu kapatir.
    Hata olursa rollback yapar.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
:::

:::code[python]{title="app/dependencies/auth.py - Authentication Dependency"}
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.models.user import User
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    JWT token'dan kullanıcıyı çıkarır.
    Depends() zinciri: token -> user -> endpoint
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Gecersiz kimlik bilgileri",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Aktif kullanıcı kontrolu - zincirleme dependency örneği."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hesap devre disi",
        )
    return current_user


def require_role(required_role: str):
    """
    Rol bazli yetkilendirme - fabrika pattern.
    Kullanım: Depends(require_role("admin"))
    """
    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"'{required_role}' rolu gerekli",
            )
        return current_user
    return role_checker
:::

:::code[python]{title="app/routers/users.py - Router'da Dependency Kullanımı"}
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user, require_role
from app.schemas.user import UserRead, UserUpdate, UserList
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
):
    """Kendi profilini getir."""
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Kendi profilini güncelle (partial update)."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    await db.flush()
    await db.refresh(current_user)
    return current_user


@router.get("/", response_model=UserList)
async def list_users(
    page: int = Query(1, ge=1, description="Sayfa numarasi"),
    per_page: int = Query(20, ge=1, le=100, description="Sayfa basi kayıt"),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_role("admin")),  # Sadece admin erişebilir
):
    """Tüm kullanıcıları listele (sadece admin)."""
    offset = (page - 1) * per_page

    total = await db.scalar(select(func.count(User.id)))
    result = await db.execute(
        select(User).offset(offset).limit(per_page).order_by(User.created_at.desc())
    )
    users = result.scalars().all()

    return UserList(items=users, total=total, page=page, per_page=per_page)
:::

:::beginner-mistake
Yaygin hata: Dependency'lerde `Depends(get_db())` yazmak (parantez ile fonksiyonu cagirmak). Doğru kullanım `Depends(get_db)` seklinde fonksiyon referansi vermektir. FastAPI, fonksiyonu kendi çağırır. Parantez koyarsan generator hemen çalışır ve her request'te ayni session'i paylasirsin — bu da veri tutarsizligina ve connection leak'e yol acar.
:::

## Async Endpoints

:::code[python]{title="async def vs def - Ne Zaman Hangisi?"}
# ✅ async def - I/O bound isler için (veritabanı, HTTP istekleri, dosya okuma)
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadi")
    return user


# ✅ def (sync) - CPU bound isler için veya sync kutuphaneler kullanırken
# FastAPI bunu otomatik olarak thread pool'da çalıştırır
@router.get("/report")
def generate_report():
    # Örneğin: pandas ile veri analizi (sync kutuphane)
    import pandas as pd
    df = pd.read_csv("data.csv")
    return {"total_rows": len(df)}


# ❌ YANLIS - async endpoint içinde sync (blocking) işlem
@router.get("/bad-example")
async def bad_blocking():
    import time
    time.sleep(5)  # Bu Tüm diger istekleri 5 saniye bloklar!
    return {"result": "kotu"}


# ✅ Doğru - async endpoint'te bekleme gerekiyorsa asyncio.sleep
import asyncio

@router.get("/good-example")
async def good_async():
    await asyncio.sleep(5)  # Diger istekler etkilenmez
    return {"result": "iyi"}


# ✅ Birden fazla async işlem paralel çalıştırma
import httpx

@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db)):
    # 3 işlem PARALEL çalışır - toplam süre en yavas islemin süresi kadar
    user_count, post_count, external_data = await asyncio.gather(
        db.scalar(select(func.count(User.id))),
        db.scalar(select(func.count(Post.id))),
        fetch_external_api("https://api.example.com/stats"),
    )
    return {
        "users": user_count,
        "posts": post_count,
        "external": external_data,
    }


async def fetch_external_api(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        return response.json()
:::

:::warning
`async def` bir endpoint içinde ASLA şu blocking işlemleri yapma:
- `time.sleep()` -> `await asyncio.sleep()` kullan
- `requests.get()` -> `httpx.AsyncClient` kullan
- `open().read()` -> `aiofiles` kullan
- Sync veritabanı sorgusu -> async SQLAlchemy veya `run_in_executor` kullan

Bir tanesi bile tüm event loop'u bloklar ve diger tüm istekler bekler.
:::

## SQLAlchemy 2.0 + Alembic Migrations

:::code[python]{title="app/models/base.py - Temel Model"}
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class TimestampMixin:
    """Her tabloya created_at ve updated_at ekler."""
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
:::

:::code[python]{title="app/models/user.py - User ORM Model"}
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    bio: Mapped[str | None] = mapped_column(String(500), default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(20), default="user")

    # Relationship
    posts: Mapped[list["Post"]] = relationship(back_populates="author", lazy="selectin")

    def __repr__(self) -> str:
        return f"<User {self.username}>"
:::

:::code[python]{title="app/models/post.py - Post ORM Model"}
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    is_published: Mapped[bool] = mapped_column(default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationship
    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post {self.title[:30]}>"
:::

:::code[bash]{title="Alembic ile Migration Yönetimi"}
# Alembic'i başlat
alembic init alembic

# alembic/env.py'yi duzenle: target_metadata = Base.metadata
# alembic.ini'de sqlalchemy.url'i ayarla

# Yeni migration oluştur
alembic revision --autogenerate -m "create users and posts tables"

# Migration'i uygula
alembic upgrade head

# Bir önceki versiyona geri don
alembic downgrade -1

# Migration geçmişini gor
alembic history

# Mevcut versiyonu gor
alembic current
:::

:::code[python]{title="alembic/env.py - Async Alembic Konfigurasyonu"}
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Model'leri import et (metadata için)
from app.core.database import Base
from app.models.user import User  # noqa: F401
from app.models.post import Post  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
:::

## Error Handling

:::code[python]{title="app/core/exceptions.py - Ozel Hata Yönetimi"}
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# Standart hata response formati
class ErrorResponse(BaseModel):
    status: str = "error"
    code: str
    message: str
    details: dict | None = None


# Ozel exception sınıfları
class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: dict | None = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


class NotFoundException(AppException):
    def __init__(self, resource: str, resource_id: int | str):
        super().__init__(
            status_code=404,
            code="NOT_FOUND",
            message=f"{resource} bulunamadi",
            details={"resource": resource, "id": str(resource_id)},
        )


class DuplicateException(AppException):
    def __init__(self, field: str, value: str):
        super().__init__(
            status_code=409,
            code="DUPLICATE",
            message=f"Bu {field} zaten kullanılıyor",
            details={"field": field, "value": value},
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "Bu işlemi yapmaya yetkiniz yok"):
        super().__init__(
            status_code=403,
            code="FORBIDDEN",
            message=message,
        )


def register_exception_handlers(app: FastAPI) -> None:
    """Tüm exception handler'lari kaydet."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code=exc.code,
                message=exc.message,
                details=exc.details,
            ).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code="HTTP_ERROR",
                message=exc.detail,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # Production'da detay gosterme, sadece logla
        import logging
        logging.error(f"Beklenmeyen hata: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                code="INTERNAL_ERROR",
                message="Sunucu hatasi olustu",
            ).model_dump(),
        )
:::

:::code[python]{title="Service'te Exception Kullanımı"}
from app.core.exceptions import NotFoundException, DuplicateException


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, user_id: int) -> User:
        user = await self.db.get(User, user_id)
        if not user:
            raise NotFoundException("Kullanıcı", user_id)
        return user

    async def create_user(self, data: UserCreate) -> User:
        # Email benzersizlik kontrolu
        existing = await self.db.execute(
            select(User).where(User.email == data.email)
        )
        if existing.scalar_one_or_none():
            raise DuplicateException("email", data.email)

        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
:::

## Middleware ve CORS

:::code[python]{title="app/main.py - Middleware Stack"}
import time
import logging
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Her istegi loglar: method, path, status, süre."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())[:8]
        start_time = time.perf_counter()

        # Request ID'yi state'e ekle (endpoint'lerde erişilebilir)
        request.state.request_id = request_id

        response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000  # ms
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"-> {response.status_code} ({duration:.1f}ms)"
        )
        response.headers["X-Request-ID"] = request_id
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Basit in-memory rate limiter (production'da Redis kullan)."""

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Eski kayıtları temizle
        if client_ip in self.requests:
            self.requests[client_ip] = [
                t for t in self.requests[client_ip]
                if now - t < self.window_seconds
            ]
        else:
            self.requests[client_ip] = []

        if len(self.requests[client_ip]) >= self.max_requests:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=429,
                content={"detail": "Çok fazla istek. Lutfen bekleyin."},
            )

        self.requests[client_ip].append(now)
        return await call_next(request)


def create_app() -> FastAPI:
    app = FastAPI(title="Senior API", version="1.0.0")

    # Middleware sirasi önemli! Sondan basa çalışır.
    # 1. CORS (en disttaki)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "https://myapp.com"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )

    # 2. Rate Limiting
    app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)

    # 3. Request Logging (en icteki - ilk çalışır)
    app.add_middleware(RequestLoggingMiddleware)

    return app
:::

:::must-note
Middleware ekleme sirasi SONDAN BASA çalışır! `app.add_middleware(A)` sonra `app.add_middleware(B)` dersen, istek geldiginde önce B, sonra A çalışır. Response donerken önce A, sonra B çalışır. Bu yuzden CORS middleware'ini en sona (yani en disa) eklemelisin.
:::

## Background Tasks ve Celery

:::code[python]{title="Background Tasks - Hafif Isler"}
from fastapi import BackgroundTasks


async def send_welcome_email(email: str, username: str):
    """Email gönderme (uzun suren is)."""
    # Gerçek uygulamada: SMTP, SendGrid, AWS SES vb.
    import asyncio
    await asyncio.sleep(2)  # Email gönderme simulasyonu
    print(f"Hosgeldin emaili gonderildi: {email}")


async def log_user_activity(user_id: int, action: str):
    """Kullanıcı aktivitesini logla."""
    print(f"Aktivite: User {user_id} -> {action}")


@router.post("/register", response_model=UserRead, status_code=201)
async def register_user(
    data: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Kullanıcı kaydi ve arkaplan görevleri."""
    user = await user_service.create_user(data)

    # Bu isler response dondukten SONRA çalışır
    # Kullanıcı beklemez, aninda 201 alir
    background_tasks.add_task(send_welcome_email, user.email, user.username)
    background_tasks.add_task(log_user_activity, user.id, "register")

    return user
:::

:::code[python]{title="Celery - Agir Isler için (Ayrı Worker)"}
# app/worker.py
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Istanbul",
    task_track_started=True,
    task_time_limit=300,  # 5 dakika max
)


@celery_app.task(bind=True, max_retries=3)
def generate_pdf_report(self, user_id: int, report_type: str):
    """PDF rapor oluştur (CPU-intensive is)."""
    try:
        # Uzun suren işlem...
        import time
        time.sleep(10)  # Celery worker'da sync kullanmak OK
        return {"status": "completed", "file": f"report_{user_id}.pdf"}
    except Exception as exc:
        # Hata olursa 60 saniye sonra tekrar dene
        raise self.retry(exc=exc, countdown=60)


@celery_app.task
def process_uploaded_image(image_path: str):
    """Resim işleme (boyutlandirma, optimizasyon)."""
    from PIL import Image
    img = Image.open(image_path)
    img.thumbnail((800, 800))
    img.save(image_path.replace(".", "_thumb."))
    return {"status": "processed"}


# ---- Endpoint'te Celery kullanımı ----
# app/routers/reports.py
from app.worker import generate_pdf_report

@router.post("/reports")
async def create_report(
    report_type: str,
    current_user: User = Depends(get_current_active_user),
):
    """Rapor oluşturma görevi başlat."""
    task = generate_pdf_report.delay(current_user.id, report_type)
    return {"task_id": task.id, "status": "processing"}


@router.get("/reports/{task_id}")
async def get_report_status(task_id: str):
    """Görev durumunu sorgula."""
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,  # PENDING, STARTED, SUCCESS, FAILURE
        "result": result.result if result.ready() else None,
    }
:::

:::senior-learns
**Karar Verme Sureci — BackgroundTasks vs Celery vs Dramatiq:**

**BackgroundTasks kullan:** Email gönderme, log yazma, cache güncelleme, webhook tetikleme gibi hafif ve kısa isler. Ayrı bir servis gerektirmez, ayni process'te çalışır. Trade-off: Worker crash ederse task kaybolur, retry mekanizmasi yok, olceklenmez.

**Celery kullan:** PDF oluşturma, video işleme, ML model inference, büyük veri analizi gibi CPU-intensive veya uzun suren isler. Redis/RabbitMQ broker gerektirir, ayrı worker process'te çalışır, retry mekanizmasi var, görev durumu takip edilebilir. Trade-off: Operasyonel karmasiklik yuksek — broker, worker, beat, flower hepsini ayri yonetmen gerekir.

**Dramatiq (alternatif):** Celery'nin daha modern, daha basit alternatifi. Redis veya RabbitMQ ile calisir, retry ve rate limiting built-in. Trade-off: Celery kadar olgun degil, community daha kucuk.

**Senior karar agaci:** "Is 30 saniyeden kisa ve hafifse BackgroundTasks. Uzun suren ama basit? Dramatiq. Complex workflow, buyuk takim? Celery."

**Gercek Dunya Deneyimi:** Bir SaaS projede baslangicta tum asenkron isleri BackgroundTasks ile yaptik. 6 ay sonra email bazen basarisiz oluyor ama retry yok. PDF uretimi 45 saniye suruyor ve uvicorn worker'i bloke ediyor. Celery'ye gecis sonrasinda retry, dead letter queue ve monitoring ile hic bir task kaybolmadi.
:::

## Konfigürasyon Yönetimi

:::code[python]{title="app/config.py - Pydantic Settings"}
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Tüm konfigurasyonu tek yerden yönet.
    Değerler .env dosyasindan veya environment variable'lardan okunur.
    """
    # Uygulama
    APP_NAME: str = "Senior API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    # Veritabanı
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/mydb"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # JWT
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Singleton pattern - tüm uygulamada ayni instance kullanılır
settings = Settings()
:::

:::code[text]{title=".env - Örnek Environment Dosyasi"}
# Veritabanı
DATABASE_URL=postgresql+asyncpg://postgres:mypassword@localhost:5432/seniordb

# JWT
SECRET_KEY=gerçek-production-da-çok-uzun-rastgele-bir-key-kullan
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
ALLOWED_ORIGINS=["http://localhost:5173","https://myapp.com"]

# Debug
DEBUG=false
:::

## Testing

:::code[python]{title="tests/conftest.py - Test Altyapisi"}
import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.database import Base
from app.dependencies.database import get_db
from app.main import app

# Test veritabanı (SQLite async)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Test oturumu için tek event loop."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Her testten önce veritabanini oluştur, sonra sil."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Test için veritabanı oturumu."""
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Test için HTTP client."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient) -> AsyncClient:
    """Giriş yapmis kullanıcı ile HTTP client."""
    # Kullanıcı oluştur
    await client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
    })
    # Giriş yap
    response = await client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "TestPass123!",
    })
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client
:::

:::code[python]{title="tests/test_users.py - Endpoint Testleri"}
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUserEndpoints:
    """Kullanıcı endpoint testleri."""

    async def test_register_user(self, client: AsyncClient):
        response = await client.post("/auth/register", json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "StrongPass1!",
            "password_confirm": "StrongPass1!",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["username"] == "newuser"
        assert "password" not in data  # Şifre response'ta olmamali

    async def test_register_duplicate_email(self, client: AsyncClient):
        user_data = {
            "email": "dup@example.com",
            "username": "user1",
            "password": "StrongPass1!",
            "password_confirm": "StrongPass1!",
        }
        await client.post("/auth/register", json=user_data)

        # Ayni email ile tekrar kayıt
        user_data["username"] = "user2"
        response = await client.post("/auth/register", json=user_data)
        assert response.status_code == 409
        assert response.json()["code"] == "DUPLICATE"

    async def test_register_weak_password(self, client: AsyncClient):
        response = await client.post("/auth/register", json={
            "email": "weak@example.com",
            "username": "weakuser",
            "password": "weak",
            "password_confirm": "weak",
        })
        assert response.status_code == 422  # Validation error

    async def test_get_my_profile(self, auth_client: AsyncClient):
        response = await auth_client.get("/users/me")
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    async def test_get_profile_unauthorized(self, client: AsyncClient):
        response = await client.get("/users/me")
        assert response.status_code == 401

    async def test_update_profile(self, auth_client: AsyncClient):
        response = await auth_client.patch("/users/me", json={
            "bio": "Merhaba dunya!",
        })
        assert response.status_code == 200
        assert response.json()["bio"] == "Merhaba dunya!"

    async def test_list_users_forbidden(self, auth_client: AsyncClient):
        """Normal kullanıcı admin endpoint'ine erisamez."""
        response = await auth_client.get("/users/")
        assert response.status_code == 403
:::

:::code[bash]{title="Testleri Çalıştır"}
# Tüm testleri çalıştır
uv run pytest -v

# Sadece belirli bir dosyayi test et
uv run pytest tests/test_users.py -v

# Coverage raporu ile
uv run pytest --cov=app --cov-report=html

# Sadece başarısız testleri tekrar çalıştır
uv run pytest --lf
:::

## Deployment

:::code[dockerfile]{title="Dockerfile - Production"}
# Multi-stage build - küçük ve güvenli image
FROM python:3.12-slim AS builder

# uv kur
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Dependency'leri önce kopyala (cache katmani)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

# Uygulama kodunu kopyala
COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini .

# Production stage
FROM python:3.12-slim AS production

WORKDIR /app

# Virtual environment'i builder'dan kopyala
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app
COPY --from=builder /app/alembic /app/alembic
COPY --from=builder /app/alembic.ini /app/alembic.ini

# PATH'e venv ekle
ENV PATH="/app/.venv/bin:$PATH"

# Güvenlik: root olmayan kullanıcı
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Gunicorn ile çalıştır (production'da uvicorn değil gunicorn kullan)
CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--access-logfile", "-"]
:::

:::code[yaml]{title="docker-compose.yml"}
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: seniordb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A app.worker worker --loglevel=info
    env_file: .env
    depends_on:
      - redis
      - db

volumes:
  postgres_data:
:::

:::code[bash]{title="Production Deployment Adimlari"}
# 1. Image'i build et
docker compose build

# 2. Veritabanini başlat
docker compose up -d db redis

# 3. Migration'lari çalıştır
docker compose run --rm api alembic upgrade head

# 4. Tüm servisleri başlat
docker compose up -d

# 5. Loglari kontrol et
docker compose logs -f api

# 6. Health check
curl http://localhost:8000/health
:::

:::beginner-mistake
Yaygin hata: Production'da `uvicorn app.main:app --reload` ile çalıştırmak. `--reload` flag'i dosya değişikliklerini izler ve sunucuyu yeniden başlatır - bu development için guzel ama production'da gereksiz overhead yaratir. Production'da gunicorn + uvicorn worker kullan: gunicorn process manager olarak çalışır, her worker bir uvicorn instance'idir. Worker sayisi genelde `(2 * CPU_CORES) + 1` formulu ile hesaplanir.
:::

## Tam Uygulama: main.py

:::code[python]{title="app/main.py - Her Seyi Birleştir"}
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.database import engine, Base
from app.core.exceptions import register_exception_handlers
from app.routers import auth, users, posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç ve bitis olaylari."""
    # Startup
    print(f"🚀 {settings.APP_NAME} v{settings.VERSION} baslatiliyor...")
    # Tablolari oluştur (development için, production'da Alembic kullan)
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()
    print("Uygulama kapatiliyor...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        docs_url="/docs" if settings.DEBUG else None,  # Production'da dokümantasyonu kapat
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    register_exception_handlers(app)

    # Router'lari ekle
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(users.router, tags=["users"])
    app.include_router(posts.router, prefix="/posts", tags=["posts"])

    return app


app = create_app()
:::

---

## Alistirmalar

:::exercise
### Alistirma 1: CRUD API Yaz

Bir "Todo" uygulaması için tam CRUD API yaz:
1. `POST /todos` - Yeni todo oluştur (title, description, priority)
2. `GET /todos` - Tüm todo'lari listele (sayfalama + filtreleme destegi)
3. `GET /todos/{id}` - Tek todo getir
4. `PATCH /todos/{id}` - Todo güncelle (partial update)
5. `DELETE /todos/{id}` - Todo sil

Gereksinimler:
- Pydantic schema'lari (TodoCreate, TodoRead, TodoUpdate, TodoList)
- SQLAlchemy model (priority enum: low, medium, high)
- Service katmani (is mantigi router'da olmasin)
- Hata yonetimi (NotFoundException kullan)
- Sayfalama (page, per_page query parametreleri)

**Beklenen süre:** 45 dakika
**Zorluk:** Orta
:::

:::exercise
### Alistirma 2: Authentication Sistemi

JWT tabanli bir authentication sistemi kur:
1. `POST /auth/register` - Kullanıcı kaydi
2. `POST /auth/login` - Giriş (access token + refresh token dondur)
3. `POST /auth/refresh` - Token yenileme
4. `GET /auth/me` - Mevcut kullanıcı bilgisi

Gereksinimler:
- Şifre hash'leme (passlib + bcrypt)
- JWT token uretimi (python-jose)
- Access token (15dk) + Refresh token (7 gun)
- `get_current_user` dependency
- Hatali giriş denemesi limiti (5 deneme, 15dk kilitleme)

**Beklenen süre:** 60 dakika
**Zorluk:** Zor
:::

:::exercise
### Alistirma 3: File Upload API

Dosya yükleme endpoint'i yaz:
1. `POST /upload` - Tek dosya yükle
2. `POST /upload/multiple` - Coklu dosya yükle
3. `GET /files/{filename}` - Dosya indir

Gereksinimler:
- Dosya boyutu siniri (max 5MB)
- Dosya turu sinirlamasi (sadece jpg, png, pdf)
- Benzersiz dosya isimlendirme (UUID prefix)
- Dosya metadata'sini veritabanina kaydet

**Beklenen süre:** 30 dakika
**Zorluk:** Orta
:::

:::exercise
### Alistirma 4: WebSocket Chat

Basit bir chat uygulaması yaz:
1. `ws://localhost:8000/ws/{room_id}` - WebSocket endpoint
2. Odaya katilma/ayrilma bildirimi
3. Mesaj broadcast (odadaki herkese)
4. Bağlı kullanıcı listesi

Gereksinimler:
- `ConnectionManager` sınıfı (bağlantıları yönet)
- JSON mesaj formati `{"type": "message", "content": "...", "sender": "..."}`
- Oda bazli mesajlasma (farkli room_id'ler izole)

**Beklenen süre:** 45 dakika
**Zorluk:** Zor
:::

:::exercise
### Alistirma 5: Rate Limiting + Caching

API'ye rate limiting ve caching ekle:
1. Redis tabanli rate limiter middleware
2. Response caching (GET endpoint'leri için)
3. Cache invalidation (POST/PUT/DELETE'te cache temizle)

Gereksinimler:
- `slowapi` veya custom Redis rate limiter
- Sliding window rate limiting algoritmasi
- Redis ile response cache
- Cache-Control header'lari

**Beklenen süre:** 45 dakika
**Zorluk:** Zor
:::

---

## Mülakat Sorulari

:::interview
### Soru 1: "FastAPI'de Depends() nasil çalışır? Neden doğrudan fonksiyon cagirmak yerine DI kullanıyoruz?"

**Junior cevap:** "Depends() bir fonksiyonu çağırır ve sonucunu verir."

**Senior cevap:** "FastAPI'nin Dependency Injection sistemi birkac kritik avantaj sağlar:

1. **Testability:** `app.dependency_overrides` ile herhangi bir dependency'yi test sırasında mock'layabilirsin. Örneğin `get_db`'yi override edip test veritabanini kullanabilirsin.

2. **Reusability:** `get_current_user` gibi bir dependency bir kere yaz, yuzlerce endpoint'te kullan. Değişiklik gerektiginde tek yerde değiştir.

3. **Composability:** Dependency'ler birbirine baglanabilir. `get_current_active_user` -> `get_current_user` -> `get_db` zinciri gibi. FastAPI dependency graph'i otomatik çözer.

4. **Lifecycle management:** `yield` ile generator-based dependency'ler kaynak yönetimi sağlar. Veritabanı oturumu açılır, endpoint çalışır, sonra otomatik kapatilir - hata olsa bile.

5. **Auto-documentation:** Depends() ile tanimlanan query/header parametreleri otomatik olarak OpenAPI dokumantasyonunda görünür."
:::

:::interview
### Soru 2: "async def vs def endpoint farki nedir? Yanlis kullanım nasil performans sorununa yol acar?"

**Senior cevap:** "FastAPI'de iki tür endpoint tanimlayabilirsin:

`async def`: ASGI event loop üzerinde çalışır. I/O-bound isler için idealdir (veritabanı sorgusu, HTTP istegi, dosya okuma). AMA içinde blocking işlem yaparsan (time.sleep, sync requests, sync DB), Tüm event loop bloklanir ve diger istekler bekler.

`def` (sync): FastAPI bunu otomatik olarak bir thread pool'da çalıştırır. CPU-bound isler veya sync kutuphaneler (pandas, PIL gibi) için uygundur. Her istek ayrı bir thread'de çalışır, blocking sorun yaratmaz ama thread overhead vardir.

Kural basit: Eger endpoint içinde `await` kullaniyorsan `async def`, kullanmiyorsan `def` yaz. En tehlikeli durum: `async def` içinde sync blocking işlem yapmak - bu tek thread'i kilitler ve tüm sunucu yanit veremez hale gelir."
:::

:::interview
### Soru 3: "Production'da FastAPI uygulamasini nasil deploy edersin? Performans için nelere dikkat edersin?"

**Senior cevap:** "Production deployment için şu adimlari izlerim:

1. **Gunicorn + Uvicorn Workers:** Gunicorn process manager olarak çalışır, her worker bir uvicorn instance'idir. Worker sayisi: `(2 * CPU_CORES) + 1`. Bu multi-process yaklaşım tek process'in crash etmesinden korur.

2. **Docker multi-stage build:** Builder stage'de dependency'leri kur, production stage'de sadece gerekli dosyalari kopyala. Image boyutunu %60-70 kucultur.

3. **Connection pooling:** SQLAlchemy'de pool_size, max_overflow ve pool_recycle parametrelerini ayarla. Veritabanı bağlantı limitlerine dikkat et.

4. **Health check endpoint:** `/health` endpoint'i ile load balancer'in sağlık kontrolu yapmasini sagla. Veritabanı ve Redis baglantisini kontrol et.

5. **Structured logging:** JSON formatinda loglama yap. Request ID ile istekleri izle. ELK stack veya Datadog ile merkezi loglama.

6. **Graceful shutdown:** SIGTERM sinyalinde mevcut istekleri tamamla, yeni istek kabul etme. `lifespan` context manager ile kaynaklari temiz kapat.

7. **Security headers:** CORS, HSTS, X-Content-Type-Options, X-Frame-Options gibi güvenlik header'lari ekle. Swagger UI'i production'da kapat."
:::

---

## Ek Ipuclari

:::deha-tip
FastAPI'nin gizli gucu: OpenAPI spec'i programatik olarak kullanabilirsin. `app.openapi()` ile tam API spec'ini alip, frontend SDK otomatik uretebilir, API test'leri generate edebilir veya baska servislere API kontrati olarak sunabilirsin. Bu, büyük takimlarda frontend-backend paralel geliştirme yapmayi mumkun kilar. Öncelikle schema'lari tasarla, OpenAPI spec'i paylaş, sonra implementasyona başla.
:::

:::must-note
FastAPI projelerinde MUTLAKA bilmen gerekenler:
1. **Pydantic v2 syntax'i:** `from_attributes`, `field_validator`, `model_config` - eski v1 syntax'i artik deprecated
2. **SQLAlchemy 2.0 style:** `Mapped`, `mapped_column` - eski `Column()` syntax'i yerine
3. **Async pattern:** `async with AsyncSessionLocal() as session` - context manager ile session yonetimi
4. **Dependency chain:** Depends içinde Depends kullanılabilir - graf olarak çözer
5. **lifespan:** Eski `@app.on_event("startup")` deprecated - `lifespan` context manager kullan
:::

:::ai-guidance
### Bu Konuyu Derinlestirmek Için AI Prompt'lari

1. "FastAPI'de N+1 query problemini async SQLAlchemy ile nasil cozebilirim? selectin, joinedload ve subqueryload arasindaki farklari ornekle goster."

2. "FastAPI uygulamam 1000 concurrent request'te yavasliyor. Profiling nasil yaparim? asyncio, uvicorn ve SQLAlchemy seviyesinde bottleneck analizi yap."

3. "FastAPI + Celery + Redis ile distributed task queue kur. Task retry, dead letter queue ve task chaining örnekleri goster."

4. "FastAPI'de multi-tenant SaaS uygulaması nasil yapilandiririm? Database-per-tenant vs schema-per-tenant vs row-level security karsilastirmasi yap."
:::

:::warning
**Güvenlik Kontrol Listesi - Production'a Cikmadan Önce:**
- [ ] `.env` dosyasi `.gitignore`'da mi?
- [ ] SECRET_KEY rastgele ve yeterince uzun mu? (en az 32 karakter)
- [ ] CORS origin'leri spesifik mi? (`*` kullanma!)
- [ ] SQL injection'a karsi parametrik sorgular mi kullaniliyor?
- [ ] Rate limiting aktif mi?
- [ ] Swagger UI production'da kapali mi?
- [ ] Password hash'leme bcrypt ile mi yapiliyor?
- [ ] JWT token'larin expiry süresi makul mu?
- [ ] HTTPS zorunlu mu?
- [ ] Input validation tüm endpoint'lerde var mi?
:::
