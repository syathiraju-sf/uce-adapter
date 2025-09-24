# UCE Adapter - FPS Test Executor

A simple, focused Heroku service that submits FPS tests using `authtoken` and `test_payload` parameters.

## 🎯 Features

- ✅ Single API endpoint: `/api/v1/execute`
- ✅ Takes 2 inputs: `authtoken` and `test_payload`
- ✅ Submits HTTP requests to FPS API
- ✅ Comprehensive logging with request tracking
- ✅ SSL verification disabled (equivalent to curl -k)
- ✅ Ready for Heroku deployment

## 📡 API Endpoints

### Health Check
```
GET /
```
Returns service health status and usage instructions.

### 🎯 Execute FPS Test
```
POST /api/v1/execute
Content-Type: application/json

{
  "authtoken": "your_bearer_token",
  "test_payload": {
    "testName": "performance_test",
    "testConfig": {
      "duration": "5m",
      "users": 50,
      "rampUp": "1m"
    }
  }
}
```

**Response:**
```json
{
  "request_id": "abc123-def456-ghi789",
  "timestamp": "2023-12-07T10:30:00.000Z",
  "status": "success",
  "execution_time_ms": 1234,
  "result": {
    "status": "success",
    "status_code": 200,
    "response": {
      // FPS API response data
    }
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
  "result": {
    "status": "error",
    "error": "Authentication failed",
    "status_code": 401
  }
}
```

## Usage Examples

### Using curl:
```bash
# Health check
curl -X GET https://your-app.herokuapp.com/

# Execute FPS test
curl -X POST https://your-app.herokuapp.com/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "authtoken": "your_bearer_token",
    "test_payload": {
      "testName": "load_test",
      "testConfig": {
        "duration": "10m",
        "users": 100,
        "rampUp": "2m"
      }
    }
  }'
```

### Using Python:
```python
import requests

# Your test configuration
data = {
    "authtoken": "your_bearer_token",
    "test_payload": {
        "testName": "performance_test",
        "testConfig": {
            "duration": "5m",
            "users": 50,
            "rampUp": "1m",
            "target": "https://api.example.com"
        },
        "metrics": ["response_time", "throughput"]
    }
}

# Make request
response = requests.post(
    "https://your-app.herokuapp.com/api/v1/execute",
    json=data
)

result = response.json()
print(f"Request ID: {result.get('request_id')}")
print(f"Status: {result.get('status')}")
print(f"Execution Time: {result.get('execution_time_ms')}ms")
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The service will be available at `http://localhost:5000`

## Heroku Deployment

### Prerequisites
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
- Git repository initialized

### Deploy Steps

1. **Login to Heroku:**
```bash
heroku login
```

2. **Create a new Heroku app:**
```bash
heroku create your-app-name
```

3. **Deploy to Heroku:**
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

4. **Open your app:**
```bash
heroku open
```

### Alternative: Deploy Button

You can also deploy directly to Heroku using the button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Environment Variables

The app uses the following environment variables:
- `PORT`: Automatically set by Heroku
- `FLASK_ENV`: Set to "production" by default

### Scaling

To scale your app:
```bash
heroku ps:scale web=1
```

### Logs

To view logs:
```bash
heroku logs --tail
```

## 📁 Project Structure

```
.
├── app.py                    # 🐍 Main Flask application with FPS API logic
├── test_fps_service.py       # 🧪 Test script with examples
├── requirements.txt          # 📦 Python dependencies
├── Procfile                 # ⚙️  Heroku process definition
├── runtime.txt              # 🐍 Python version specification
├── app.json                 # 📋 Heroku app configuration
├── .gitignore               # 🚫 Git ignore patterns
└── README.md                # 📖 This file
```

## 🧪 Testing the Service

### Local Testing:
```bash
# Start the service
python app.py

# In another terminal, test it
python test_fps_service.py
```

### Configure for your environment:
Edit `test_fps_service.py` and replace:
- `authtoken`: Your actual bearer token for FPS API
- `test_payload`: Your actual test configuration data
- `base_url`: Change to your Heroku URL when deployed

## 🔑 Important Notes

- **SSL Verification**: Disabled (equivalent to `curl -k`) for compatibility
- **Authentication**: Uses `bearer` token in Authorization header
- **FPS Endpoint**: `https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns`
- **Logging**: Comprehensive request tracking with unique request IDs

## Dependencies

- Flask 2.3.3 - Web framework
- requests 2.31.0 - HTTP library for API calls
- gunicorn 21.2.0 - WSGI HTTP Server for production

## License

MIT License
