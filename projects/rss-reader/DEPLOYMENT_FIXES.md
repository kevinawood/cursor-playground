# 🚀 Deployment Fixes Guide

## Issues Identified

### 1. Railway Memory Errors
- **Problem**: Out of memory errors during deployment
- **Cause**: Web scraping operations consuming too much memory
- **Solution**: Memory-optimized code and configuration

### 2. Supabase 5GB Storage Limit
- **Problem**: Exceeding storage limit despite small database
- **Cause**: Accumulated old articles and logs
- **Solution**: Database cleanup and optimization

---

## 🔧 Railway Memory Fixes

### Step 1: Update Your Code
The following optimizations have been made to `app.py`:

#### Reading Time Calculation Optimizations:
- ✅ **Content size limits**: 1MB max for article content
- ✅ **Text truncation**: 50KB limit for processed text
- ✅ **Word count caps**: 10,000 words maximum
- ✅ **Memory cleanup**: Explicit deletion of large objects
- ✅ **Reduced timeouts**: 5 seconds instead of 10
- ✅ **Graceful fallbacks**: Return estimates instead of errors

#### AI Summary Optimizations:
- ✅ **Content size limits**: 1MB max for article content
- ✅ **Text truncation**: 3,000 characters maximum
- ✅ **Token reduction**: 150 tokens instead of 200
- ✅ **Memory cleanup**: Explicit deletion of objects
- ✅ **Enhanced error handling**: Memory-specific fallbacks

### Step 2: Railway Configuration
The `railway.json` file has been created with:
- ✅ **Single worker**: Prevents memory multiplication
- ✅ **Limited threads**: 2 threads per worker
- ✅ **Request limits**: 100 requests per worker
- ✅ **Timeout settings**: 30 seconds maximum
- ✅ **Restart policy**: Automatic restart on failure

### Step 3: Docker Optimizations
The `Dockerfile` has been updated with:
- ✅ **Alpine Linux**: Lighter base image
- ✅ **Python optimizations**: Memory-efficient settings
- ✅ **Gunicorn**: Production-grade WSGI server
- ✅ **Environment variables**: Memory optimization flags

---

## 🗄️ Supabase Storage Fixes

### Step 1: Run Database Cleanup
```bash
# Navigate to your project directory
cd projects/rss-reader

# Run the cleanup script
python scripts/cleanup-database.py
```

This script will:
- 🗑️ **Delete old articles**: Remove articles older than 30 days (not bookmarked)
- 🗑️ **Clean read articles**: Remove read articles older than 7 days (not bookmarked)
- 🧹 **Vacuum database**: Reclaim storage space
- 📊 **Show statistics**: Before and after cleanup

### Step 2: Monitor Storage Usage
Check your Supabase dashboard:
1. Go to your Supabase project
2. Navigate to **Database** → **Tables**
3. Check the **Storage** tab for usage statistics
4. Monitor **Logs** for any storage-related errors

### Step 3: Set Up Automatic Cleanup
Add this to your Railway deployment to run cleanup weekly:

```bash
# Add to your Railway environment variables
CLEANUP_SCHEDULE=weekly
```

---

## 🚀 Deployment Steps

### Step 1: Commit Your Changes
```bash
git add .
git commit -m "fix: optimize memory usage and add database cleanup"
git push origin main
```

### Step 2: Deploy to Railway
1. **Push to GitHub**: Your changes will auto-deploy
2. **Monitor logs**: Check Railway dashboard for any errors
3. **Verify health**: Ensure the health check passes

### Step 3: Clean Up Database
```bash
# Run cleanup script
python scripts/cleanup-database.py
```

### Step 4: Test the Application
1. **Check Railway URL**: Ensure backend is responding
2. **Test features**: Try reading time and summaries
3. **Monitor memory**: Watch for memory errors

---

## 📊 Monitoring and Maintenance

### Memory Monitoring
- **Railway Dashboard**: Monitor memory usage
- **Application Logs**: Check for memory errors
- **Performance**: Watch response times

### Storage Monitoring
- **Supabase Dashboard**: Check storage usage
- **Database Size**: Monitor table growth
- **Cleanup Schedule**: Run cleanup regularly

### Recommended Maintenance Schedule
- **Daily**: Check application health
- **Weekly**: Run database cleanup
- **Monthly**: Review and optimize feeds

---

## 🔍 Troubleshooting

### Railway Memory Issues
If you still get memory errors:

1. **Check logs**: Look for specific error messages
2. **Reduce feeds**: Temporarily disable some RSS feeds
3. **Increase limits**: Consider upgrading Railway plan
4. **Optimize further**: Review memory-intensive operations

### Supabase Storage Issues
If storage is still high:

1. **Run cleanup**: Execute the cleanup script
2. **Check logs**: Look for large log files
3. **Review data**: Identify what's consuming space
4. **Optimize schema**: Consider archiving old data

### Application Errors
If the app isn't working:

1. **Check Railway**: Ensure backend is running
2. **Verify Supabase**: Confirm database connection
3. **Test endpoints**: Use curl to test API
4. **Review logs**: Check for specific errors

---

## 📈 Performance Optimizations

### Frontend Optimizations
- ✅ **Caching**: Reading time and summary caching
- ✅ **Lazy loading**: Load content as needed
- ✅ **Error handling**: Graceful fallbacks

### Backend Optimizations
- ✅ **Memory limits**: Content size restrictions
- ✅ **Timeouts**: Reduced request timeouts
- ✅ **Garbage collection**: Aggressive memory cleanup
- ✅ **Connection pooling**: Efficient database connections

### Database Optimizations
- ✅ **Cleanup script**: Regular data cleanup
- ✅ **Indexes**: Optimized database queries
- ✅ **Vacuum**: Regular storage reclamation

---

## 🎯 Success Metrics

After implementing these fixes, you should see:

### Railway Performance
- ✅ **No memory errors**: Application stays stable
- ✅ **Fast response times**: Under 5 seconds for most requests
- ✅ **High uptime**: 99%+ availability
- ✅ **Low resource usage**: Efficient memory consumption

### Supabase Storage
- ✅ **Under 5GB**: Storage usage stays within limits
- ✅ **Regular cleanup**: Automated maintenance
- ✅ **Fast queries**: Optimized database performance
- ✅ **No storage errors**: Clean operation

### Application Performance
- ✅ **Reliable features**: Reading time and summaries work
- ✅ **Fast loading**: Quick article display
- ✅ **Error-free operation**: No crashes or failures
- ✅ **Good user experience**: Smooth interaction

---

## 📞 Support

If you continue to experience issues:

1. **Check logs**: Review Railway and Supabase logs
2. **Monitor metrics**: Watch performance indicators
3. **Test locally**: Verify functionality in development
4. **Contact support**: Reach out to Railway/Supabase support

Remember: These optimizations are designed to work within free tier limits while maintaining full functionality! 