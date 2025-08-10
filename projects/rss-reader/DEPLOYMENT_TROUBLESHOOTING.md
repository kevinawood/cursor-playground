# 🚨 Production Deployment Troubleshooting

## Current Issues

### **1. CORS Errors**
```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource
Reason: CORS header 'Access-Control-Allow-Origin' missing
```

### **2. 502 Bad Gateway Errors**
```
Status code: 502
Error loading categories: Network Error
```

---

## 🔧 Fix 1: CORS Configuration

### **Backend CORS Fix (Already Applied)**
The backend now has proper CORS configuration:

```python
# Configure CORS for production
allowed_origins = [
    'http://localhost:3000',  # Local development
    'http://localhost:5173',  # Vite dev server
    'https://rss-reader-lake-omega.vercel.app',  # Your Vercel frontend
    'https://rss-reader-frontend.vercel.app',    # Alternative Vercel domain
    'https://*.vercel.app',   # Any Vercel subdomain
]

CORS(app, origins=allowed_origins, supports_credentials=True)
```

### **Frontend Environment Configuration**
You need to set the correct backend URL in your Vercel deployment:

#### **Option 1: Vercel Environment Variables**
1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add:
   ```
   Name: VITE_API_URL
   Value: https://rss-reader-production-60e8.up.railway.app
   Environment: Production
   ```

#### **Option 2: Create .env.production File**
Create a file in your frontend directory:
```bash
# frontend/.env.production
VITE_API_URL=https://rss-reader-production-60e8.up.railway.app
```

---

## 🔧 Fix 2: Railway Backend Issues

### **Check Railway Deployment Status**
1. Go to your Railway dashboard
2. Check if the backend service is running
3. Look at the logs for any errors

### **Test Backend Health**
```bash
# Test the health endpoint
curl https://rss-reader-production-60e8.up.railway.app/health

# Test an API endpoint
curl https://rss-reader-production-60e8.up.railway.app/api/stats
```

### **Common Railway Issues**

#### **1. Memory Issues (OOM)**
- **Symptoms**: 502 errors, service restarts
- **Solution**: The memory optimizations we added should fix this

#### **2. Database Connection Issues**
- **Symptoms**: Database errors in logs
- **Solution**: Check Supabase connection string

#### **3. Port Configuration**
- **Symptoms**: Service won't start
- **Solution**: Ensure Railway uses the PORT environment variable

---

## 🔧 Fix 3: Environment Variables

### **Railway Environment Variables**
Make sure these are set in your Railway project:

```bash
# Database
DATABASE_URL=your_supabase_connection_string

# Feed refresh (for egress optimization)
FEED_REFRESH_INTERVAL_MINUTES=30

# Memory optimization
BATCH_SIZE_FOR_FEED_PROCESSING=5
COMMIT_EVERY_N_ARTICLES=5

# API settings
FEEDSEARCH_TIMEOUT=10

# Flask settings
FLASK_ENV=production
FLASK_DEBUG=false

# OpenAI (if using summaries)
OPENAI_API_KEY=your_openai_key
```

### **Vercel Environment Variables**
Set these in your Vercel project:

```bash
# Backend API URL
VITE_API_URL=https://rss-reader-production-60e8.up.railway.app
```

---

## 🔧 Fix 4: Deployment Steps

### **Step 1: Deploy Backend Fixes**
```bash
# Commit and push the CORS fixes
git add .
git commit -m "fix: add proper CORS configuration and health check endpoint"
git push origin reading-time-and-ui-improvements
```

### **Step 2: Check Railway Logs**
1. Go to Railway dashboard
2. Check the backend service logs
3. Look for any startup errors

### **Step 3: Test Backend**
```bash
# Test health endpoint
curl https://rss-reader-production-60e8.up.railway.app/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "database": "connected"
}
```

### **Step 4: Update Frontend Environment**
1. Set `VITE_API_URL` in Vercel environment variables
2. Redeploy frontend if needed

### **Step 5: Test Frontend**
1. Clear browser cache
2. Open your Vercel frontend URL
3. Check browser console for errors

---

## 🔍 Debugging Steps

### **1. Check Railway Logs**
```bash
# In Railway dashboard, look for:
- Application startup messages
- Database connection errors
- Memory usage warnings
- CORS-related errors
```

### **2. Test Backend Endpoints**
```bash
# Health check
curl https://rss-reader-production-60e8.up.railway.app/health

# API endpoints
curl https://rss-reader-production-60e8.up.railway.app/api/stats
curl https://rss-reader-production-60e8.up.railway.app/api/categories
```

### **3. Check Frontend Network Tab**
1. Open browser dev tools
2. Go to Network tab
3. Refresh the page
4. Look for failed requests and their details

### **4. Verify Environment Variables**
```bash
# Check if Railway has the right variables
# Check if Vercel has VITE_API_URL set
```

---

## 🚨 Emergency Fixes

### **If Backend is Completely Down**

#### **1. Restart Railway Service**
1. Go to Railway dashboard
2. Stop the backend service
3. Start it again
4. Check logs for errors

#### **2. Check Database Connection**
```bash
# Test Supabase connection
psql "your_supabase_connection_string" -c "SELECT 1;"
```

#### **3. Rollback to Previous Version**
```bash
# If needed, revert to a working commit
git revert HEAD
git push origin reading-time-and-ui-improvements
```

### **If Frontend Can't Connect**

#### **1. Use Local Backend Temporarily**
```bash
# Update VITE_API_URL to local backend
VITE_API_URL=http://localhost:5001
```

#### **2. Check CORS Headers**
```bash
# Test CORS headers
curl -H "Origin: https://rss-reader-lake-omega.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://rss-reader-production-60e8.up.railway.app/api/stats
```

---

## 📊 Success Indicators

### **Backend Working:**
- ✅ Health endpoint returns 200
- ✅ API endpoints return data
- ✅ No 502 errors in Railway logs

### **Frontend Working:**
- ✅ No CORS errors in console
- ✅ API calls succeed
- ✅ Data loads properly

### **Full System Working:**
- ✅ Articles load from backend
- ✅ Reading times calculate
- ✅ Summaries generate
- ✅ No network errors

---

## 📞 Next Steps

1. **Deploy the CORS fixes** to Railway
2. **Set environment variables** in both Railway and Vercel
3. **Test the health endpoint** to verify backend is working
4. **Check frontend console** for remaining errors
5. **Monitor logs** for any new issues

**The CORS configuration should fix the main issue. The 502 errors suggest the backend might be having startup problems, which the health check endpoint will help diagnose.** 🚀 