# AI Retail Shelf Analyzer

Rasmda ko‘rinadigan obyektlarni YOLO yordamida aniqlaydigan demo loyiha. Backend FastAPI, saqlash PostgreSQL, frontend React va Vite’dan foydalanadi.

## Docker orqali ishga tushirish

Docker va Docker Compose o‘rnatilgan bo‘lishi kerak:

```bash
docker compose up --build
```

Birinchi tahlilda javon mahsulotlariga mos SKU-110K YOLO modeli Hugging Face’dan yuklanadi; buning uchun internet kerak. Keyin:

- Frontend: http://localhost:5173
- API hujjatlari: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Yuklangan tahlil rasmlari `uploads/`, chizilgan natijalar `results/`, katalog etalonlari `catalog_images/`, PostgreSQL ma’lumotlari Docker volume’da saqlanadi.

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
- `GET /api/products` — etalon mahsulotlar katalogi.
- `POST /api/products` — `name`, `category`, ixtiyoriy `brand`/`package_size` va `reference_image` multipart maydonlari bilan katalogga mahsulot qo‘shish.
- `DELETE /api/products/{id}` — katalog mahsulotini o‘chirish.
- `GET /results/{filename}` — chizilgan natija rasmini olish.
- `GET /catalog-images/{filename}` — katalog etalon rasmini olish.

## Test rasmlari

`test_images/` ichida to‘liq, bo‘sh joyli va zich mahsulotli javon uchun uchta sintetik test rasmi bor. Tavsif va API misoli papkadagi README’da berilgan.
- `GET /health` — xizmat holati.

Standart model javondagi mahsulotlarni alohida `mahsulot` obyektlari sifatida aniqlaydi, lekin SKU/brend nomlarini tanimaydi. Muayyan mahsulot nomi yoki turini aniqlash uchun o‘z mahsulotlaringiz bilan o‘qitilgan model kerak. Boshqa lokal Ultralytics vazn faylini ishlatish uchun `YOLO_MODEL=/path/to/model.pt` deb belgilang.

Deteksiya parametrlarini muhit o‘zgaruvchilari bilan sozlash mumkin: `YOLO_CONFIDENCE` (standart `0.35`), `YOLO_IMAGE_SIZE` (standart `960`) va `YOLO_MAX_DETECTIONS` (standart `1000`). Confidence — model balli, aniqlik foizi emas. Haqiqiy inventar sonini tasdiqlash uchun modelni maqsadli javon rasmlarida baholash kerak.

## Keyingi bosqichlar

1. Object detection va qutilarni sanash — hozir: javondagi mahsulot qutilari aniqlanadi, API/UI sonini ko‘rsatadi.
2. Mahsulot klassifikatsiyasi — SKU/brend katalogi yoki mahsulot rasmlari bilan ulash.
3. Inventory hisoboti — aniqlangan SKU bo‘yicha sonlarni guruhlash va tarix bilan solishtirish.
4. Bo‘sh javon joylari — shelf qatorlarini belgilash va bandlik xaritasini hisoblash.
5. Planogramma — kutilgan SKU/joylashuv jadvali bilan aniqlangan javonni solishtirish.

Mahsulot katalogi va etalon planogramma bo‘lmagani uchun 2–5 bosqichlar hozircha ma’lumot talab qiladi; tizimda hozircha faqat umumiy mahsulot qutilari sanaladi.
