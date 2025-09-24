#!/usr/bin/env python3
"""
Test script for the FPS Test Executor service.
"""

import requests
import json

def test_fps_service():
    """Test the FPS service locally or on Heroku."""
    
    # Configuration
    base_url = "http://localhost:5000"  # Change to your Heroku URL when deployed
    
    # Example test payload (replace with your actual test data)
    test_payload = {
        "testName": "sample_performance_test",
        "testConfig": {
            "duration": "5m",
            "users": 10,
            "rampUp": "1m",
            "target": "https://example.com/api"
        },
        "metrics": ["response_time", "throughput", "error_rate"]
    }
    
    # Example auth token (replace with your actual token)
    authtoken = "your_actual_bearer_token_here"
    
    # Request data
    request_data = {
        "authtoken": authtoken,
        "test_payload": test_payload
    }
    
    print("🚀 Testing FPS Test Executor Service")
    print("="*50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Execute FPS test
    print("\n2. Testing FPS test execution...")
    try:
        response = requests.post(
            f"{base_url}/api/v1/execute",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def print_curl_examples():
    """Print example curl commands for testing."""
    print("\n📋 Example CURL commands:")
    print("="*50)
    
    print("\n1. Health Check:")
    print("curl -X GET https://your-app.herokuapp.com/")
    
    print("\n2. Execute FPS Test:")
    print("""curl -X POST https://your-app.herokuapp.com/api/v1/execute \\
  -H "Content-Type: application/json" \\
  -d '{
    "authtoken": "your_bearer_token",
    "test_payload": {
      "testName": "load_test",
      "testConfig": {
        "duration": "10m",
        "users": 50
      }
    }
  }'""")

def print_python_example():
    """Print Python usage example."""
    print("\n🐍 Python usage example:")
    print("="*50)
    print("""
import requests

# Your configuration
url = "https://your-app.herokuapp.com/api/v1/execute"
data = {
    "authtoken": "your_bearer_token",
    "test_payload": {
        "testName": "performance_test",
        "testConfig": {
            "duration": "5m",
            "users": 100,
            "rampUp": "2m"
        }
    }
}

# Make request
response = requests.post(url, json=data)
result = response.json()

print(f"Status: {response.status_code}")
print(f"Request ID: {result.get('request_id')}")
print(f"Status: {result.get('status')}")
print(f"Execution Time: {result.get('execution_time_ms')}ms")

if result.get('status') == 'success':
    print("✅ Test submitted successfully!")
    print(f"FPS Response: {result.get('result')}")
else:
    print("❌ Test failed:")
    print(f"Error: {result.get('error')}")
""")

if __name__ == "__main__":
    print("🎯 FPS Test Executor Service - Test & Examples")
    print("Note: Make sure the service is running before executing tests")
    print("To run locally: python app.py")
    
    choice = input("\nChoose option:\n1. Run tests\n2. Show curl examples\n3. Show Python example\n4. All\nEnter (1/2/3/4): ")
    
    if choice in ['1', '4']:
        test_fps_service()
    
    if choice in ['2', '4']:
        print_curl_examples()
    
    if choice in ['3', '4']:
        print_python_example()
