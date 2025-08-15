# Free Deployment Options for HH KZ CAD Jobs

## 🚀 Quick Deploy Options (All Free)

### 1. **Railway** (Easiest - Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up
```

**Free tier**: $5 credit/month (sufficient for small apps)

### 2. **Render** (Very Easy)
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new Web Service
4. Select your repo
5. Render will auto-detect Python and deploy

**Free tier**: 750 hours/month, sleeps after 15 min inactivity

### 3. **Vercel** (Fast & Reliable)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

**Free tier**: Generous limits, great performance

### 4. **Fly.io** (Global Deployment)
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login and deploy
fly auth login
fly launch
```

**Free tier**: 3 shared-cpu VMs, 3GB storage

### 5. **Heroku** (If you have existing account)
```bash
# Install Heroku CLI
# Deploy
heroku create your-app-name
git push heroku main
```

**Free tier**: Limited (if you have existing account)

## 📋 Pre-deployment Checklist

1. ✅ Update `HH_USER_AGENT` in config files with your email
2. ✅ Ensure all files are committed to Git
3. ✅ Test locally: `python app.py`

## 🔧 Environment Variables

Set these in your deployment platform:
- `HH_USER_AGENT`: "HH-KZ-CAD-Jobs/1.1 (your_email@example.com)"
- `PORT`: Usually auto-set by platform

## 🌐 After Deployment

Your app will be available at:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
- Vercel: `https://your-app-name.vercel.app`
- Fly.io: `https://your-app-name.fly.dev`

## 📊 API Endpoints

- `GET /` - Web interface
- `GET /jobs` - API endpoint with query parameters

## 💡 Recommendation

**Start with Railway** - it's the easiest and most reliable for Python FastAPI apps.
