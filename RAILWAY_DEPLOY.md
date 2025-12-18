# 🚂 Railway Deployment Guide - Super Easy!

## **What is Railway?**

-   Free $5 credit per month
-   Deploy directly from GitHub
-   Auto-deploy on git push
-   Built-in domain & SSL

---

## **STEP 1: Push Your Code to GitHub**

```bash
cd /home/zidunn/Desktop/self-learning-AI-assistant

# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for Railway deployment"

# Push to GitHub (replace with your repo)
git remote add origin https://github.com/YOUR_USERNAME/self-learning-ai-backend.git
git branch -M main
git push -u origin main
```

---

## **STEP 2: Deploy on Railway**

### 2.1: Sign Up

1. Go to https://railway.app
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway

### 2.2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `self-learning-ai-backend`
4. Railway will auto-detect your Dockerfile

### 2.3: Add Environment Variables

1. In your Railway project, click **"Variables"** tab
2. Add these variables (use your actual values from .env file):

```
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
PORT=5000
```

### 2.4: Deploy!

1. Click **"Deploy"**
2. Wait 2-3 minutes ⏳
3. Railway will give you a URL like: `https://your-app.up.railway.app`

---

## **STEP 3: Get Your Public URL**

1. In Railway dashboard, go to **"Settings"**
2. Click **"Generate Domain"**
3. Copy your domain: `https://your-app-production.up.railway.app`

---

## **STEP 4: Test Your API**

```bash
# Replace with your Railway URL
API_URL="https://your-app-production.up.railway.app"

# Test health
curl $API_URL/

# Test AI reply
curl -X POST $API_URL/generate-reply \
  -H "Content-Type: application/json" \
  -d '{"clientSequence": "I need help with DTV visa", "chatHistory": []}'
```

---

## **✅ You're Live!**

Your API is now:

-   ✅ Running on Railway
-   ✅ Auto-deploys on git push
-   ✅ Has HTTPS/SSL
-   ✅ Free (with $5/month credit)

---

## **Update Your App**

Just push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push

# Railway auto-deploys! 🚀
```

---

## **Monitor Usage**

1. Go to Railway dashboard
2. Check **"Metrics"** tab
3. See your credit usage

**$5 credit typically covers:**

-   ~500-1000 requests/day
-   24/7 uptime for small apps

---

## **Troubleshooting**

### Build fails

-   Check Railway logs in **"Deployments"** tab
-   Verify environment variables are set

### App crashes

-   Check **"Logs"** in Railway dashboard
-   Make sure PORT variable is set

### Need more credit

-   Add payment method for $5/month
-   Or optimize to stay within free tier

---

## **What Railway Automatically Does:**

✅ Detects Dockerfile and builds it
✅ Assigns a public URL
✅ Provides SSL/HTTPS
✅ Auto-restarts on failure
✅ Shows logs and metrics
✅ Auto-deploys from GitHub

**Total setup time: ~10 minutes!** 🎉
