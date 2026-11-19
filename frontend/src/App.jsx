import { useEffect, useState } from 'react';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function loadHistory() {
    try {
      const response = await fetch(`${API}/api/analyses`);
      if (response.ok) setHistory(await response.json());
    } catch { /* API may still be starting */ }
  }
  useEffect(() => { loadHistory(); }, []);

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
    {result && <section className="card result"><div><span className="eyebrow">NATIJA</span><h2>{result.detections.length} ta obyekt topildi</h2><p>{result.filename}</p></div><img className="result-image" src={`${API}${result.result_image_url}`} alt="Aniqlangan obyektlar" /><div className="detections">{result.detections.map((d, i) => <div className="detection" key={i}><strong>{d.label}</strong><span>{(d.confidence * 100).toFixed(1)}%</span></div>)}</div></section>}
    <section className="history"><div className="section-heading"><div><span className="eyebrow">LOYIHA TARIXI</span><h2>So‘nggi tahlillar</h2></div><button className="refresh" onClick={loadHistory}>Yangilash</button></div>
      {history.length ? <div className="history-grid">{history.map(item => <article className="history-item" key={item.id}><img src={`${API}${item.result_image_url}`} alt="Tahlil natijasi" /><div><strong>{item.filename}</strong><span>{item.detections_count} ta obyekt</span></div></article>)}</div> : <p className="empty">Hozircha tahlillar yo‘q.</p>}
    </section>
    <footer>AI Retail Shelf Analyzer · FastAPI + YOLO</footer>
  </main>;
}
