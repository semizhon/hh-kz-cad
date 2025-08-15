#!/bin/bash

echo "🚀 Redeploying to Railway with clean build..."

# Force a new commit to trigger deployment
git add .
git commit -m "Clean Railway deployment - remove Docker references"

# Push to trigger Railway deployment
git push origin main

echo "✅ Deployment triggered!"
echo "📊 Check your Railway dashboard for deployment status"
echo "🌐 Your app will be available at: https://your-app-name.railway.app"
