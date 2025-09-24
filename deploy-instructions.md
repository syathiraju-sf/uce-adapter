# 🚀 UCE Adapter - FPS Test Executor Deployment Instructions

## Quick Deploy to Heroku

### Method 1: Heroku Dashboard (Recommended)

1. **Login to Heroku**: https://dashboard.heroku.com/
2. **Create New App**:
   - Click "New" → "Create new app"
   - App name: `uce-adapter-fps-executor` (or your choice)
   - Region: US or Europe
   - Click "Create app"

3. **Deploy via GitHub**:
   - Go to "Deploy" tab
   - Select "GitHub" as deployment method
   - Connect your GitHub account
   - Search for your repository
   - Enable "Automatic deploys" (optional)
   - Click "Deploy Branch"

### Method 2: Heroku CLI

```bash
# Login to Heroku (complete browser authentication)
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Open app
heroku open
```

### Method 3: Manual Upload

1. **Zip the following files**:
   - app.py
   - requirements.txt
   - Procfile
   - runtime.txt
   - app.json

2. **Upload to Heroku**:
   - Go to Heroku Dashboard
   - Create new app
   - Use "Deploy" → "Manual deploy"

## 🧪 Testing Your Deployed App

### Health Check:
```bash
curl https://your-app-name.herokuapp.com/
```

### Test FPS Execution:
```bash
curl -X POST https://your-app-name.herokuapp.com/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "authtoken": "your_bearer_token",
    "test_payload": {
      "testName": "sample_test",
      "testConfig": {
        "duration": "5m",
        "users": 10
      }
    }
  }'
```

## 🔧 Files Included

- **app.py**: Main Flask application with FPS API integration
- **app_simple.py**: Simplified version for debugging
- **requirements.txt**: Python dependencies
- **Procfile**: Heroku process configuration
- **runtime.txt**: Python version specification
- **app.json**: Heroku app metadata

## ✅ Expected Response

**Success Response:**
```json
{
  "request_id": "uuid-here",
  "timestamp": "2023-12-07T...",
  "status": "success",
  "execution_time_ms": 1234,
  "result": {
    "status": "success",
    "status_code": 200,
    "response": { /* FPS API response */ }
  }
}
```

**Error Response:**
```json
{
  "request_id": "uuid-here",
  "timestamp": "2023-12-07T...",
  "status": "error",
  "execution_time_ms": 567,
  "result": {
    "status": "error",
    "error": "error message",
    "status_code": 401
  }
}
```

## 🆘 Troubleshooting

1. **App won't start**: Check logs in Heroku dashboard under "More" → "View logs"
2. **404 errors**: Make sure you're using POST method for `/api/v1/execute`
3. **Authentication issues**: Verify your bearer token is correct
4. **Connection issues**: Check if FPS endpoint is accessible from your network

## 📞 Support

If you encounter issues:
1. Check Heroku logs first
2. Test locally using `python app_simple.py`
3. Verify all files are included in deployment
