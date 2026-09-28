# 🌐 ARA-1 Research Terminal — Complete Sharing & Deployment Guide

This guide details all methods for running, sharing, and deploying the **ARA-1 (Autonomous Financial Research Agent)** web application and research suite with evaluators, teammates, and stakeholders.

---

## ⚡ Quick Start: 4 Ways to Share & Run ARA-1

| Method | Target Audience | Setup Required | Output / URL |
| :--- | :--- | :--- | :--- |
| **1. Standalone Single-File Bundle** | Evaluators, Executives, Offline Review | **Zero Setup** (open in browser) | `results/ARA1_Research_Suite_Standalone.html` |
| **2. One-Click Local Server** | Local development, interactive ReAct | Python 3.9+ (`./run_app.sh`) | `http://localhost:8080` |
| **3. Live Public URL (Tunneling)** | Remote evaluators, live demo | 1 command (`cloudflared`/`ngrok`) | `https://your-custom-subdomain.trycloudflare.com` |
| **4. Cloud Hosting (Render/Vercel)** | Permanent public deployment | Git Push | `https://ara1-research-agent.onrender.com` |

---

## 📦 Method 1: Standalone Single-File Bundle (Zero Setup Required)

The standalone bundle packages the complete visual terminal, all 8 pre-computed benchmark research reports, the 20+ quality metrics radar charts, and the interactive DCF valuation studio into a **single portable HTML file**.

### How to use:
1. Compile the latest bundle (or use the pre-built version):
   ```bash
   python3 export_standalone.py
   ```
2. Locate the output file:
   ```
   results/ARA1_Research_Suite_Standalone.html
   ```
3. **Share via Email, Slack, Teams, or Google Drive:**
   - The recipient does **not need Python, pip, or a local server**.
   - Simply double-click to open in Google Chrome, Apple Safari, Mozilla Firefox, or Microsoft Edge.
   - All interactive calculators, charts, and report previews work 100% offline.

---

## 💻 Method 2: Run Locally with Live ReAct Reasoning Loop

To execute live dynamic research queries against the full 12-tool cognitive architecture and 3-layer memory:

### Option A: One-Click Bash Script
```bash
./run_app.sh
```

### Option B: Manual Launch
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start server
python3 web/server.py --port 8080

# 3. Open browser
open http://localhost:8080
```

---

## 🌐 Method 3: Share Live Public URL via Secure Tunneling

You can expose your running local server to any remote evaluator with an instant secure HTTPS URL without firewall configuration.

### Option A: Cloudflare Quick Tunnel (Free, No Account Needed)
```bash
# Start your local server in one terminal:
./run_app.sh

# In a second terminal, launch the Cloudflare tunnel:
npx cloudflared tunnel --url http://localhost:8080
```
*Cloudflare will print a temporary public HTTPS link (e.g. `https://random-words.trycloudflare.com`) that anyone can open worldwide.*

### Option B: ngrok
```bash
ngrok http 8080
```

### Option C: Localtunnel
```bash
npx localtunnel --port 8080
```

---

## ☁️ Method 4: Permanent Cloud Deployment

### 1. Deploy to Render (Web Service)
1. Push this repository to GitHub.
2. In [Render Dashboard](https://dashboard.render.com), click **New + > Web Service**.
3. Connect your repository.
4. Set the build and start commands:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt && python3 export_standalone.py`
   - **Start Command:** `python3 web/server.py --port $PORT --host 0.0.0.0`
5. Click **Deploy**.

### 2. Deploy to GitHub Pages (Static Standalone Mode)
1. Rename or copy `results/ARA1_Research_Suite_Standalone.html` to `docs/index.html`.
2. In your GitHub repository settings, go to **Pages**.
3. Select **Deploy from a branch** -> `main` branch -> `/docs` folder.
4. Your standalone research terminal is now live at `https://<your-username>.github.io/<repo-name>/`.

---

## 📡 REST API Reference

The local server also exposes high-performance JSON endpoints:

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/status` | `GET` | Health status, active tools, and memory readiness |
| `/api/challenges` | `GET` | Retrieve pre-computed benchmark memos (C1 through C8) |
| `/api/metrics` | `GET` | Full 20+ quality metrics taxonomy and scorecard |
| `/api/research` | `POST` | Execute autonomous research loop for a query string |
| `/api/calculate` | `POST` | Run deterministic DCF, CAGR, or financial ratio calculations |
| `/api/search_memory` | `POST` | Search ChromaDB vector store with cosine similarity |

---

## ⚖️ Verification & Test Suite

Before sharing, verify that all 13 unit and integration tests pass:
```bash
pytest -v
```
*Pass rate: 100% (13 passed).*
