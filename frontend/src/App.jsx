import { useEffect, useState } from 'react';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [products, setProducts] = useState([]);
  const [productImage, setProductImage] = useState(null);
  const [catalogBusy, setCatalogBusy] = useState(false);
  const [catalogMessage, setCatalogMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function loadHistory() {
    try {
      const response = await fetch(`${API}/api/analyses`);
      if (response.ok) setHistory(await response.json());
    } catch { /* API may still be starting */ }
  }
  async function loadProducts() {
    try {
      const response = await fetch(`${API}/api/products`);
      if (response.ok) setProducts(await response.json());
    } catch { /* API may still be starting */ }
  }
  useEffect(() => { loadHistory(); loadProducts(); }, []);

  async function analyze(event) {
    event.preventDefault();
    if (!file) return;
    setBusy(true); setError(''); setResult(null);
    const data = new FormData(); data.append('file', file);
    try {
      const response = await fetch(`${API}/api/analyses`, { method: 'POST', body: data });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || 'Tahlil amalga oshmadi');
      setResult(body); await loadHistory();
    } catch (err) { setError(err.message || 'Server bilan bog‘lanib bo‘lmadi'); }
    finally { setBusy(false); }
  }

  async function addProduct(event) {
    event.preventDefault();
    if (!productImage) return;
    const form = event.currentTarget;
    setCatalogBusy(true); setCatalogMessage('');
    try {
      const data = new FormData(form);
      const response = await fetch(`${API}/api/products`, { method: 'POST', body: data });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || 'Mahsulot saqlanmadi');
      form.reset(); setProductImage(null);
      setCatalogMessage('Mahsulot katalogga qo‘shildi.'); await loadProducts();
    } catch (err) { setCatalogMessage(err.message || 'Server bilan bog‘lanib bo‘lmadi'); }
    finally { setCatalogBusy(false); }
  }

  async function removeProduct(id) {
    const response = await fetch(`${API}/api/products/${id}`, { method: 'DELETE' });
    if (response.ok) await loadProducts();
  }

  return <main className="layout">
    <header><span className="eyebrow">COMPUTER VISION</span><h1>AI Shelf Analyzer</h1><p>Javon rasmini yuklang va mahsulotlarni avtomatik aniqlang.</p></header>
    <section className="card">
      <form onSubmit={analyze}>
        <label className="drop"><span className="upload-icon">↑</span><strong>{file ? file.name : 'Rasmni tanlang'}</strong><small>JPEG, PNG yoki WebP · 15 MB gacha</small><input type="file" accept="image/jpeg,image/png,image/webp" onChange={e => setFile(e.target.files?.[0] || null)} /></label>
        {file && <div className="preview"><img src={URL.createObjectURL(file)} alt="Tanlangan rasm" /></div>}
        <button disabled={!file || busy}>{busy ? 'Tahlil qilinmoqda…' : 'Tahlil qilish'}</button>
        {error && <p className="error">{error}</p>}
      </form>
    </section>
    {result && <section className="card result"><div><span className="eyebrow">NATIJA</span><h2>{result.detections.length} ta mahsulot qutisi aniqlandi</h2><p>{result.filename}</p><p className="note">Bu model aniqlagan qutilar soni. Confidence balli aniqlik kafolati yoki mahsulot turi emas.</p></div><img className="result-image" src={`${API}${result.result_image_url}`} alt="Javondagi aniqlangan mahsulot qutilari" /></section>}
    <section className="catalog">
      <div className="section-heading"><div><span className="eyebrow">MAHSULOT KATALOGI</span><h2>Etalon mahsulotlar</h2></div><span className="catalog-count">{products.length} ta</span></div>
      <div className="card catalog-card">
        <p className="note">Mahsulot nomi, kategoriya va old tomondan olingan etalon rasm qo‘shing. Hozircha katalog yig‘iladi; rasm bilan avtomatik moslashtirish keyingi bosqichda ulanadi.</p>
        <form className="product-form" onSubmit={addProduct}>
          <input name="name" placeholder="Mahsulot nomi / SKU" required maxLength="255" />
          <input name="category" placeholder="Kategoriya (masalan: ichimlik)" required maxLength="120" />
          <input name="brand" placeholder="Brend (ixtiyoriy)" maxLength="120" />
          <input name="package_size" placeholder="Hajmi (masalan: 1 L)" maxLength="120" />
          <label className="reference-upload">{productImage ? productImage.name : 'Etalon rasm tanlang'}<input type="file" name="reference_image" accept="image/jpeg,image/png,image/webp" required onChange={e => setProductImage(e.target.files?.[0] || null)} /></label>
          <button disabled={catalogBusy || !productImage}>{catalogBusy ? 'Saqlanmoqda…' : 'Katalogga qo‘shish'}</button>
        </form>
        {catalogMessage && <p className="catalog-message">{catalogMessage}</p>}
        {products.length > 0 && <div className="product-grid">{products.map(product => <article className="product-item" key={product.id}><img src={`${API}${product.reference_image_url}`} alt={product.name} /><div><strong>{product.name}</strong><span>{[product.brand, product.category, product.package_size].filter(Boolean).join(' · ')}</span><button type="button" className="delete-product" onClick={() => removeProduct(product.id)}>O‘chirish</button></div></article>)}</div>}
      </div>
    </section>
    <section className="history"><div className="section-heading"><div><span className="eyebrow">LOYIHA TARIXI</span><h2>So‘nggi tahlillar</h2></div><button className="refresh" onClick={loadHistory}>Yangilash</button></div>
      {history.length ? <div className="history-grid">{history.map(item => <article className="history-item" key={item.id}><img src={`${API}${item.result_image_url}`} alt="Tahlil natijasi" /><div><strong>{item.filename}</strong><span>{item.detections_count} ta obyekt</span></div></article>)}</div> : <p className="empty">Hozircha tahlillar yo‘q.</p>}
    </section>
    <footer>AI Retail Shelf Analyzer · FastAPI + YOLO</footer>
  </main>;
}
