# 🌐 YT Helper Frontend (Vercel Ready)

This directory contains the standalone, responsive dark-mode web application for **YT Helper**, ready for zero-config deployment to [Vercel](https://vercel.com).

---

## 🚀 Quick Deployment to Vercel

### Method 1: Vercel Web Dashboard (Easiest)

1. Push your repository to GitHub.
2. Go to [Vercel Dashboard](https://vercel.com/new) and click **"Add New Project"**.
3. Import your repository.
4. In the configuration settings:
   - **Root Directory**: Select `Tube-AI-API/frontend` (or click Edit and select the folder).
   - **Framework Preset**: Select **Other**.
5. Click **Deploy**!

---

### Method 2: Vercel CLI

From this directory (`Tube-AI-API/frontend`):
```bash
npx vercel
```
Follow the prompts to deploy to production:
```bash
npx vercel --prod
```

---

## 🔗 Connecting to your Render Backend

You have two easy ways to point the frontend to your Render backend:

### Option A: In `config.js` (Before Deploying)
Open `config.js` and set your Render URL:
```javascript
window.CONFIG = {
  API_BASE_URL: "https://your-service-name.onrender.com"
};
```

### Option B: Via the In-App UI (Zero Rebuild Required)
Once deployed on Vercel:
1. Open your Vercel URL (e.g. `https://your-app.vercel.app`).
2. Click the **"API Config"** button in the topbar.
3. Enter your Render backend URL (e.g. `https://your-service-name.onrender.com`).
4. Click **"Save & Connect"**!
5. Your setting is saved in `localStorage` in your browser.
