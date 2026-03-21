#!/bin/bash
# Full setup script for the education platform

echo "🔧 Eğitim Platformu Kurulumu"
echo "=========================="

cd "$(dirname "$0")/.."

# Backend setup
echo ""
echo "📦 Backend kurulumu..."
cd backend
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
pip install -r requirements.txt
echo "✅ Backend bağımlılıkları yüklendi"

# Initialize database
python -c "
from database import engine, Base
from models import *
Base.metadata.create_all(bind=engine)
print('✅ Veritabanı oluşturuldu')

from database import SessionLocal
from services.content_indexer import index_content
db = SessionLocal()
index_content(db)
db.close()
print('✅ İçerik indekslendi')
"

cd ..

# Frontend setup
echo ""
echo "🎨 Frontend kurulumu..."
cd frontend
npm install
echo "✅ Frontend bağımlılıkları yüklendi"

echo ""
echo "🎉 Kurulum tamamlandı!"
echo "   Başlatmak için: bash scripts/dev.sh"
