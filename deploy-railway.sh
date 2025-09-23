#!/bin/bash

echo "🚀 Deploying HH KZ CAD Jobs to Railway from scratch..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway (interactive)
echo "Please login to Railway in the browser that opens..."
railway login

# Create new project
echo "Creating new Railway project..."
railway init

# Set environment variables
echo "Setting environment variables..."
railway variables set ENVIRONMENT=production
railway variables set HH_USER_AGENT="HH-KZ-CAD-Jobs/1.1 (your_email@example.com)"

# Deploy the project
echo "Deploying to Railway..."
railway up

# Get the deployment URL
echo "Getting deployment URL..."
URL=$(railway domain)
echo "✅ Deployment complete!"
echo "🌐 Your app is available at: https://$URL"
echo ""
echo "📋 Next steps:"
echo "1. Test the app: curl https://$URL/"
echo "2. Check cache status: curl https://$URL/standard-cache-status"
echo "3. Trigger standard searches: curl -X POST https://$URL/trigger-standard-searches"
echo ""
echo "🎯 Standard searches will run daily at 06:00 Almaty time"
echo "📊 Cached results available for Kazakhstan and Uzbekistan queries"
