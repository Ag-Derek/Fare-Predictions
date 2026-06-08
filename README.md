# 🚖 Ghana Ride Fare Predictor

A fully **serverless, static web app** that runs a trained **Random Forest model entirely in the browser** — no Python, no backend, no API costs.

Live on Netlify: [![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR-BADGE-ID/deploy-status)](https://app.netlify.com)

---

## ✨ Features

- **AI fare estimation** — 100-tree Random Forest model runs in JavaScript
- **4 Ghanaian cities** — Accra, Kumasi, Takoradi, Tamale with real zone coordinates
- **Auto distance calculation** — Haversine formula from zone coordinates
- **Market Insights** — Charts showing fare trends by city, payment method, and hour of day
- **Trip History** — Persisted in `localStorage`, survives page refresh
- **Zero backend** — Fully static, deployable anywhere

---

## 🗂 Project Structure

```
ghana-ride-predictor/
├── public/
│   ├── index.html     ← The entire app (HTML + CSS + JS)
│   ├── model.json     ← Random Forest exported from sklearn (~2MB, 653KB gzipped)
│   └── stats.json     ← Precomputed chart data from the training dataset
├── netlify.toml       ← Netlify deploy config (publish dir + cache headers)
└── README.md
```

---

## 🚀 Deploy to Netlify (3 steps)

### Option A — Netlify UI (easiest)

1. Push this repo to GitHub
2. Go to [app.netlify.com](https://app.netlify.com) → **Add new site** → **Import an existing project**
3. Connect your GitHub repo, set:
   - **Base directory:** *(leave blank)*
   - **Publish directory:** `public`
   - **Build command:** *(leave blank — no build step needed)*
4. Click **Deploy site** ✅

### Option B — Netlify CLI

```bash
npm install -g netlify-cli
netlify login
netlify deploy --dir=public --prod
```

---

## 🔄 Updating the Model

If you retrain the model with a new `fare_model.pkl` and `encoders.pkl`, regenerate `model.json`:

```python
python scripts/export_model.py
```

Then commit and push — Netlify auto-deploys on every push to `main`.

---

## 🛠 Local Development

No build step required. Just serve the `public/` folder:

```bash
# Python
python -m http.server 8000 --directory public

# Node
npx serve public
```

Then open [http://localhost:8000](http://localhost:8000).

---

## 📊 Model Details

| Property | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Trees | 100 |
| Features | city, pickup_area, dropoff_area, duration_min, distance_km, rating, payment_method |
| Target | fare (GHS) |
| Training data | 1,000 synthetic Ghana ride-sharing trips |

---

## 📁 Regenerating Data Files

```bash
pip install scikit-learn pandas joblib
python scripts/export_model.py   # → public/model.json
python scripts/export_stats.py   # → public/stats.json
```
