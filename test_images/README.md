# Test rasmlari

Bu papkadagi rasmlar AI Retail Shelf Analyzer demo va qo‘lda tekshirish uchun generatsiya qilingan sintetik javon rasmlaridir. Ular real do‘kon tasvirlari yoki belgilangan ground-truth dataset emas.

- `shelf_well_stocked.png` — mahsulotlar to‘liq joylangan javon.
- `shelf_empty_gaps.png` — mahsulotlar orasida katta bo‘sh joylar mavjud.
- `shelf_dense_mixed.png` — turli qadoqlar zich joylashgan murakkab javon.

Frontend’da rasmni tanlab tahlil qiling yoki API orqali yuboring:

```bash
curl -X POST http://localhost:8000/api/analyses \
  -F "file=@test_images/shelf_well_stocked.png"
```

Aniqlash sifatini son jihatdan baholash uchun rasmga haqiqiy bounding-box annotatsiyalari kerak bo‘ladi; bu rasmlarga annotatsiya kiritilmagan.
