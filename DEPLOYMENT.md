# Railway Deployment for HH KZ CAD Jobs

## 🚀 Deploy to Railway (Recommended)

Railway is the easiest and most reliable platform for deploying Python FastAPI apps.

### **Quick Deploy**

#### **Step 1: Get Railway Token**
1. Go to [railway.app](https://railway.app)
2. Create account and login
3. Go to Account Settings → Tokens
4. Create new token

#### **Step 2: Add GitHub Secret**
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Click **New repository secret**
3. Name: `RAILWAY_TOKEN`
4. Value: Your Railway token
5. Click **Add secret**

#### **Step 3: Deploy**
```bash
git add .
git commit -m "Add Railway deployment"
git push origin main
```

**Your app will be live at:** `https://your-app-name.railway.app`

### **Manual Deploy with CLI**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up
```

## 🔧 Troubleshooting

### **If Railway tries to use Dockerfile (500 errors)**

If you see errors like "Using Detected Dockerfile" and healthcheck failures:

1. **Clean deployment files:**
   ```bash
   # Remove any Docker-related files
   rm -f Dockerfile .dockerignore
   
   # Remove non-Railway deployment files
   rm -f fly.toml vercel.json render.yaml Procfile
   ```

2. **Force clean rebuild:**
   ```bash
   # Use the provided script
   ./redeploy-railway.sh
   ```

3. **Or manually trigger:**
   ```bash
   git add .
   git commit -m "Clean Railway deployment"
   git push origin main
   ```

### **Common Issues**

- **500 Internal Server Error**: Usually means Railway is trying to use Docker instead of Python
- **Healthcheck failures**: Check that your app starts correctly with `python app.py`
- **Environment variables**: Make sure `HH_USER_AGENT` is set in Railway dashboard

## 📋 Pre-deployment Checklist

1. ✅ Update `HH_USER_AGENT` in config files with your email
2. ✅ Ensure all files are committed to Git
3. ✅ Test locally: `python app.py`
4. ✅ Remove any Docker-related files
5. ✅ Keep only Railway deployment files

## 🔧 Environment Variables

Railway will automatically set:
- `PORT`: Auto-set by Railway
- `HH_USER_AGENT`: "HH-KZ-CAD-Jobs/1.1 (your_email@example.com)"

## 🌐 After Deployment

Your app will be available at:
- Railway: `https://your-app-name.railway.app`

## 📊 API Endpoints

- `GET /` - Web interface
- `GET /jobs` - API endpoint with query parameters

## 💡 Railway Benefits

- **Free tier**: $5 credit/month (sufficient for small apps)
- **Easy setup**: Just connect GitHub repo
- **Auto-deploy**: Deploys on every push
- **Reliable**: Great uptime and performance
- **Fast**: Quick deployment times
