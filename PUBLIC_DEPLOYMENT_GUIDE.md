# Public Deployment Guide - Live API URL

## 🚀 Deploy Your FastAPI App with Public URL

This guide shows how to deploy your FastAPI app to get a **public URL** where your API will be live and accessible.

## 🎯 **Recommended Platforms (Free + Public URL)**

### **1. Railway (Easiest - Recommended)**
- **Free tier**: $5 credit/month
- **Public URL**: `https://your-app-name.railway.app`
- **Setup time**: 5 minutes

### **2. Render (Very Easy)**
- **Free tier**: 750 hours/month
- **Public URL**: `https://your-app-name.onrender.com`
- **Setup time**: 3 minutes

### **3. Vercel (Fast)**
- **Free tier**: Generous limits
- **Public URL**: `https://your-app-name.vercel.app`
- **Setup time**: 5 minutes

## 🔧 **Quick Setup - Choose One Platform**

### **Option A: Railway (Recommended)**

#### **Step 1: Get Railway Token**
1. Go to [railway.app](https://railway.app)
2. Create account and login
3. Go to Account Settings → Tokens
4. Create new token

#### **Step 2: Add GitHub Secret**
1. Go to your GitHub repo: https://github.com/semizhon/hh-kz-cad
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `RAILWAY_TOKEN`
5. Value: Your Railway token
6. Click **Add secret**

#### **Step 3: Deploy**
```bash
git add .
git commit -m "Add Railway deployment"
git push origin main
```

**Your app will be live at:** `https://your-app-name.railway.app`

---

### **Option B: Render (Easiest)**

#### **Step 1: Create Render Account**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Create account

#### **Step 2: Deploy from GitHub**
1. Click **New** → **Web Service**
2. Connect your GitHub repository: `semizhon/hh-kz-cad`
3. Name: `hh-kz-cad-jobs`
4. Environment: `Python 3`
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `python app.py`
7. Click **Create Web Service**

**Your app will be live at:** `https://your-app-name.onrender.com`

---

### **Option C: Vercel (Fastest)**

#### **Step 1: Get Vercel Tokens**
1. Go to [vercel.com](https://vercel.com)
2. Create account and login
3. Go to Settings → Tokens
4. Create new token

#### **Step 2: Get Project IDs**
```bash
npm install -g vercel
vercel login
vercel link
# Note the Project ID and Org ID
```

#### **Step 3: Add GitHub Secrets**
Add these secrets to your GitHub repo:
- `VERCEL_TOKEN`: Your Vercel token
- `VERCEL_ORG_ID`: Your organization ID
- `VERCEL_PROJECT_ID`: Your project ID

#### **Step 4: Deploy**
```bash
git add .
git commit -m "Add Vercel deployment"
git push origin main
```

**Your app will be live at:** `https://your-app-name.vercel.app`

## 🌐 **After Deployment - Your Public URLs**

### **API Endpoints:**
- **Web Interface**: `https://your-app-name.railway.app/`
- **API Endpoint**: `https://your-app-name.railway.app/jobs`
- **API Documentation**: `https://your-app-name.railway.app/docs`

### **Example API Calls:**
```bash
# Search for AutoCAD jobs
curl "https://your-app-name.railway.app/jobs?keywords=AutoCAD&country=Kazakhstan"

# Search for multiple keywords
curl "https://your-app-name.railway.app/jobs?keywords=AutoCAD&keywords=Revit&country=Kazakhstan"

# Filter by products
curl "https://your-app-name.railway.app/jobs?keywords=CAD&products=Fusion 360&country=Kazakhstan"
```

## 🎯 **Recommended: Railway Setup**

Let me guide you through the Railway setup (easiest):

### **Step 1: Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Click **Start a New Project**
3. Sign up with GitHub
4. Authorize Railway

### **Step 2: Deploy Your App**
1. Click **Deploy from GitHub repo**
2. Select your repo: `semizhon/hh-kz-cad`
3. Railway will auto-detect Python
4. Click **Deploy Now**

### **Step 3: Get Your Public URL**
1. Wait for deployment (2-3 minutes)
2. Click on your service
3. Copy the **Public URL**
4. Your app is live! 🎉

## 💡 **Pro Tips**

### **For Railway:**
- Free $5 credit monthly
- Automatic HTTPS
- Custom domains available
- Easy environment variables

### **For Render:**
- 750 free hours/month
- Sleeps after 15 min inactivity
- Automatic HTTPS
- Easy setup

### **For Vercel:**
- Generous free tier
- Fast deployments
- Automatic HTTPS
- Edge functions

## 🚀 **Quick Start Commands**

```bash
# Add deployment files
git add .

# Commit changes
git commit -m "Add public deployment workflows"

# Push to GitHub (triggers deployment)
git push origin main
```

## 📊 **Monitor Deployment**

1. **GitHub Actions**: Check deployment status
2. **Platform Dashboard**: Monitor your app
3. **Test Your API**: Use the public URL

## 🎉 **Success!**

After deployment, you'll have:
- ✅ **Public URL** for your API
- ✅ **Live FastAPI app** accessible worldwide
- ✅ **Automatic HTTPS** security
- ✅ **API documentation** at `/docs`
- ✅ **Web interface** at `/`

**Your FastAPI app will be publicly available and ready to use! 🚀**

Which platform would you like to try first? I recommend **Railway** for the easiest setup!
