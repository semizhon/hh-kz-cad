# GitHub Actions Deployment Setup

## 🚀 Automated Deployment with GitHub Actions

This guide shows how to set up automatic deployment to multiple free platforms using GitHub Actions.

## 📋 Prerequisites

1. Push your code to GitHub repository
2. Choose which platform(s) you want to deploy to
3. Get API tokens/keys from your chosen platform(s)

## 🔧 Platform Setup Instructions

### 1. **Railway** (Recommended)

**Get Railway Token:**
1. Go to [railway.app](https://railway.app)
2. Create account and login
3. Go to Account Settings → Tokens
4. Create new token

**Setup GitHub Secret:**
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add secret: `RAILWAY_TOKEN` with your Railway token

### 2. **Render**

**Get Render API Key:**
1. Go to [render.com](https://render.com)
2. Create account and login
3. Go to Account → API Keys
4. Create new API key

**Get Service ID:**
1. Create a new Web Service in Render
2. Copy the Service ID from the service URL

**Setup GitHub Secrets:**
- `RENDER_API_KEY`: Your Render API key
- `RENDER_SERVICE_ID`: Your service ID

### 3. **Vercel**

**Get Vercel Tokens:**
1. Go to [vercel.com](https://vercel.com)
2. Create account and login
3. Go to Settings → Tokens
4. Create new token

**Get Project/Org IDs:**
```bash
npm install -g vercel
vercel login
vercel link
# This will show your project and org IDs
```

**Setup GitHub Secrets:**
- `VERCEL_TOKEN`: Your Vercel token
- `VERCEL_ORG_ID`: Your organization ID
- `VERCEL_PROJECT_ID`: Your project ID

### 4. **Fly.io**

**Get Fly API Token:**
1. Go to [fly.io](https://fly.io)
2. Create account and login
3. Go to Access Tokens
4. Create new token

**Setup GitHub Secret:**
- `FLY_API_TOKEN`: Your Fly.io API token

## 🎯 Quick Start (Choose One Platform)

### Option A: Railway (Easiest)
1. Get Railway token (see above)
2. Add `RAILWAY_TOKEN` secret to GitHub
3. Push to main branch
4. GitHub Actions will auto-deploy

### Option B: Render (Web Interface)
1. Get Render API key and service ID
2. Add secrets to GitHub
3. Push to main branch
4. Auto-deploy on every push

### Option C: Vercel (Fast)
1. Get Vercel tokens and IDs
2. Add all Vercel secrets to GitHub
3. Push to main branch
4. Auto-deploy with previews

## 📁 Workflow Files Created

- `.github/workflows/test.yml` - Tests app before deployment
- `.github/workflows/deploy-railway.yml` - Deploy to Railway
- `.github/workflows/deploy-render.yml` - Deploy to Render
- `.github/workflows/deploy-vercel.yml` - Deploy to Vercel
- `.github/workflows/deploy-fly.yml` - Deploy to Fly.io

## 🔄 How It Works

1. **Push to main branch** → Triggers GitHub Actions
2. **Test workflow runs** → Validates your code
3. **Deploy workflow runs** → Deploys to your chosen platform(s)
4. **App is live** → Available at your platform's URL

## 🎛️ Customization

### Enable/Disable Platforms
Edit the workflow files to enable/disable specific platforms:

```yaml
# In .github/workflows/deploy-railway.yml
on:
  push:
    branches: [ main, master ]  # Change trigger branches
```

### Environment Variables
Add environment variables to your deployment platforms:

```yaml
# In workflow files
env:
  HH_USER_AGENT: "HH-KZ-CAD-Jobs/1.1 (your_email@example.com)"
```

## 🚨 Troubleshooting

### Common Issues:
1. **Missing secrets** → Add required secrets to GitHub
2. **Authentication errors** → Check API tokens are valid
3. **Build failures** → Check requirements.txt and app.py syntax

### Debug Steps:
1. Check GitHub Actions tab for error logs
2. Verify all secrets are set correctly
3. Test locally: `python app.py`

## 💡 Pro Tips

1. **Start with one platform** - Don't set up all at once
2. **Use Railway first** - Most reliable for Python apps
3. **Monitor deployments** - Check GitHub Actions tab
4. **Set up notifications** - Get notified of deployment status

## 🌐 After Setup

Your app will automatically deploy to:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
- Vercel: `https://your-app-name.vercel.app`
- Fly.io: `https://your-app-name.fly.dev`

**Just push to main branch and your app deploys automatically! 🎉**
