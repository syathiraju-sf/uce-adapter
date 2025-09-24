# UCE Adapter - Test Run Executor

A Flask web service for submitting test runs to different testing frameworks (FPS and RAFI).

## Features

- REST API for submitting tests to FPS framework
- REST API for submitting tests to RAFI framework (placeholder)
- Health check endpoint
- Error handling and validation
- Ready for Heroku deployment

## API Endpoints

### Health Check
```
GET /
```
Returns service health status and available endpoints.

### 🎯 Main Execute Endpoint (Recommended)
```
POST /api/v1/execute
Content-Type: application/json

{
  "authtoken": "your_bearer_token",
  "test_payload": {
    "test_name": "sample_test",
    "test_config": {
      "duration": "5m",
      "users": 10
    }
  },
  "framework": "fps"  // optional, defaults to "fps"
}
```

**Response:**
```json
{
  "status": "success",
  "status_code": 200,
  "response": {
    // FPS API response data
  }
}
```

### Submit FPS Test (Direct)
```
POST /api/v1/submit/fps
Content-Type: application/json

{
  "test_payload": {...},
  "authtoken": "your_bearer_token"
}
```

### Submit RAFI Test (Direct)
```
POST /api/v1/submit/rafi
Content-Type: application/json

{
  "test_payload": {...}
}
```

## Usage Examples

### Using curl:
```bash
# Health check
curl -X GET https://your-app.herokuapp.com/

# Execute test with authtoken and test_payload
curl -X POST https://your-app.herokuapp.com/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "authtoken": "your_bearer_token",
    "test_payload": {
      "test_name": "performance_test",
      "config": {"users": 50, "duration": "10m"}
    }
  }'
```

### Using Python:
```python
import requests

# Your test data
data = {
    "authtoken": "your_bearer_token",
    "test_payload": {
        "test_name": "load_test",
        "config": {"users": 100}
    }
}

# Make request
response = requests.post(
    "https://your-app.herokuapp.com/api/v1/execute",
    json=data
)

print(response.json())
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

## Project Structure

```
.
├── app.py                 # Main Flask application with REST API
├── testrunexecutor.py     # Test execution logic (FPS/RAFI)
├── test_service.py        # Test script for service validation
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku process definition
├── runtime.txt           # Python version specification
├── app.json              # Heroku app configuration
├── .gitignore            # Git ignore patterns
└── README.md             # This file
```

## Testing the Service

### Local Testing:
```bash
# Start the service
python app.py

# In another terminal, run tests
python test_service.py
```

### Test with real data:
Replace the example values in `test_service.py` with your actual:
- `authtoken`: Your bearer token for FPS API
- `test_payload`: Your actual test configuration

## Dependencies

- Flask 2.3.3 - Web framework
- requests 2.31.0 - HTTP library for API calls
- gunicorn 21.2.0 - WSGI HTTP Server for production

## License

MIT License
