# AI Retail Shelf Analyzer

Rasmda ko‘rinadigan obyektlarni YOLO yordamida aniqlaydigan demo loyiha. Backend FastAPI, saqlash PostgreSQL, frontend React va Vite’dan foydalanadi.

## Docker orqali ishga tushirish

Docker va Docker Compose o‘rnatilgan bo‘lishi kerak:

```bash
docker compose up --build
```

Birinchi ishga tushishda Ultralytics `yolov8n.pt` modelini yuklab oladi. Keyin:

- Frontend: http://localhost:5173
- API hujjatlari: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Yuklangan rasmlar `uploads/`, chizilgan natijalar `results/`, PostgreSQL ma’lumotlari Docker volume’da saqlanadi.

## Lokal ishga tushirish

Python 3.10+ va Node.js o‘rnating. PostgreSQL ishlatayotgan bo‘lsangiz `DATABASE_URL` muhit o‘zgaruvchisini sozlang. O‘zgaruvchi berilmasa, lokal demo SQLite ishlatadi.

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Ikkinchi terminalda:

```bash
cd frontend
npm install
npm run dev
```

Frontend `http://localhost:5173` manzilida ochiladi. PostgreSQL uchun misol:

```bash
DATABASE_URL='postgresql+psycopg://user:password@localhost:5432/shelf_analyzer' uvicorn app.main:app --reload
```

## API

- `POST /api/analyses` — `file` nomli multipart rasm maydonini yuborib tahlil qilish.
- `GET /api/analyses?limit=20` — oxirgi tahlillar tarixi.
- `GET /results/{filename}` — chizilgan natija rasmini olish.
- `GET /health` — xizmat holati.

Modelni almashtirish uchun `YOLO_MODEL` o‘zgaruvchisiga Ultralytics model nomi yoki model fayli yo‘lini bering. Model natijalari umumiy COCO sinflariga asoslanadi; mahsulot turlari bo‘yicha aniq hisob uchun javon mahsulotlarida fine-tune qilingan model kerak bo‘ladi.
