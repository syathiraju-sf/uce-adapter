# 🚀 FPS API Client - Simple Heroku Service

A super simple Heroku-deployed Flask service with **hardcoded values** - no inputs required! Just call the endpoint and get your FPS performance data.

## 🎯 Features

- ✅ **Zero Configuration**: All values are hardcoded (run ID + auth token)
- ✅ **Single Endpoint**: Just `GET /api/v1/fps` - that's it!
- ✅ **Direct FPS API Call**: Executes your exact curl command
- ✅ **Request Tracking**: Unique request IDs and execution time logging
- ✅ **SSL Verification Disabled**: For internal API compatibility
- ✅ **Heroku Ready**: All deployment files included

## 📡 API Endpoints

### Health Check
```
GET /
```
Returns service status and available endpoints.

### Get Performance Run (Query Parameter)
```
GET /api/v1/perfruns/{run_id}?token={bearer_token}
```

**Example:**
```bash
curl -X GET "https://your-app.herokuapp.com/api/v1/perfruns/2915731b-62f7-490f-bc24-2b4c583c7ff2?token=your_bearer_token"
```

### Get Performance Run (JSON Body)
```
POST /api/v1/fps/get
Content-Type: application/json

{
  "run_id": "performance_run_uuid",
  "token": "bearer_token"
}
```

**Example:**
```bash
curl -X POST https://your-app.herokuapp.com/api/v1/fps/get \
  -H "Content-Type: application/json" \
  -d '{
    "run_id": "2915731b-62f7-490f-bc24-2b4c583c7ff2",
    "token": "your_bearer_token"
  }'
```

## 🚀 Deploy to Heroku

### Method 1: Heroku CLI
```bash
# Login to Heroku
heroku login

# Create app
heroku create fps-api-client-$(date +%s)

# Deploy
git push heroku main

# Open app
heroku open
```

### Method 2: Heroku Dashboard
1. Go to https://dashboard.heroku.com/
2. Click "New" → "Create new app"
3. App name: `fps-api-client-your-name`
4. Deploy via GitHub or manual upload

### Method 3: Deploy Button
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## 🧪 Test Your Deployment

### Health Check:
```bash
curl https://your-app.herokuapp.com/
```

### Get Performance Run Data:
```bash
# Method 1: Query Parameter
curl -X GET "https://your-app.herokuapp.com/api/v1/perfruns/2915731b-62f7-490f-bc24-2b4c583c7ff2?token=YOUR_TOKEN"

# Method 2: JSON Body
curl -X POST https://your-app.herokuapp.com/api/v1/fps/get \
  -H "Content-Type: application/json" \
  -d '{
    "run_id": "2915731b-62f7-490f-bc24-2b4c583c7ff2",
    "token": "YOUR_TOKEN"
  }'
```

## 📋 Expected Response Format

**Success Response:**
```json
{
  "request_id": "abc123-def456-ghi789",
  "timestamp": "2023-12-07T10:30:00.000Z",
  "status": "success",
  "execution_time_ms": 1234,
  "fps_data": {
    // Complete FPS API response data
    "runId": "2915731b-62f7-490f-bc24-2b4c583c7ff2",
    "status": "completed",
    "metrics": {...},
    "results": {...}
  }
}
```

**Error Response:**
```json
{
  "request_id": "abc123-def456-ghi789",
  "timestamp": "2023-12-07T10:30:00.000Z",
  "status": "error",
  "execution_time_ms": 567,
  "fps_error": {
    "status_code": 401,
    "message": "Authentication failed"
  }
}
```

## 🔧 Local Development

1. **Install dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Run the app:**
```bash
python app.py
```

3. **Test locally:**
```bash
python test_fps_client.py
```

## 📁 Project Structure

```
.
├── app.py                    # 🐍 Main Flask application
├── test_fps_client.py        # 🧪 Test script with examples
├── requirements.txt          # 📦 Python dependencies
├── Procfile                 # ⚙️  Heroku process definition
├── runtime.txt              # 🐍 Python version specification
├── app.json                 # 📋 Heroku app metadata
└── README.md                # 📖 This file
```

## 🔑 Environment Variables

The service automatically handles:
- `PORT`: Set by Heroku for web process
- Authentication tokens passed via API calls

## 🛡️ Security Notes

- SSL verification is disabled for internal API compatibility
- Bearer tokens are logged as "Present/Missing" only (not the actual token)
- All requests are tracked with unique request IDs for debugging

## 🆘 Troubleshooting

1. **401 Authentication Error**: Check your bearer token is valid and not expired
2. **404 Not Found**: Verify the performance run ID exists
3. **500 Internal Error**: Check Heroku logs for detailed error information
4. **Connection Timeout**: Ensure FPS API endpoint is accessible

## 📞 Support

- **Heroku Logs**: `heroku logs --tail -a your-app-name`
- **Local Testing**: Use `test_fps_client.py` to verify functionality
- **API Documentation**: Check `/` endpoint for service information

## 🎯 Original Curl Command Equivalent

Your original curl command:
```bash
curl -X GET "https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns/2915731b-62f7-490f-bc24-2b4c583c7ff2" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: bearer YOUR_TOKEN"
```

**Becomes:**
```bash
curl -X GET "https://your-app.herokuapp.com/api/v1/perfruns/2915731b-62f7-490f-bc24-2b4c583c7ff2?token=YOUR_TOKEN"
```

The service acts as a proxy, handling the internal FPS API call and returning the results with additional metadata and error handling.
