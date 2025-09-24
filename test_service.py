#!/usr/bin/env python3
"""
Test script to demonstrate how to use the UCE Adapter service.
"""

import requests
import json

# Example test data
def test_service():
    """Test the UCE Adapter service locally or on Heroku."""
    
    # Configuration
    base_url = "http://localhost:5000"  # Change to your Heroku URL when deployed
    
    # Example test payload (replace with your actual test data)
    test_payload = {
        "test_name": "sample_fps_test",
        "test_config": {
            "duration": "5m",
            "users": 10,
            "ramp_up": "1m"
        },
        "metrics": ["response_time", "throughput"]
    }
    
    # Example auth token (replace with your actual token)
    authtoken = "your_actual_bearer_token_here"
    
    # Test data for the main execute endpoint
    request_data = {
        "authtoken": authtoken,
        "test_payload": test_payload,
        "framework": "fps"  # optional, defaults to "fps"
    }
    
    print("🚀 Testing UCE Adapter Service")
    print("="*50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Main execute endpoint
    print("\n2. Testing main execute endpoint...")
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
    
    # Test 3: Direct FPS endpoint
    print("\n3. Testing direct FPS endpoint...")
    try:
        fps_data = {
            "authtoken": authtoken,
            "test_payload": test_payload
        }
        response = requests.post(
            f"{base_url}/api/v1/submit/fps",
            json=fps_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def example_curl_commands():
    """Print example curl commands for testing."""
    print("\n📋 Example CURL commands:")
    print("="*50)
    
    print("\n1. Health Check:")
    print("curl -X GET https://your-app.herokuapp.com/")
    
    print("\n2. Execute Test (Main Endpoint):")
    print("""curl -X POST https://your-app.herokuapp.com/api/v1/execute \\
  -H "Content-Type: application/json" \\
  -d '{
    "authtoken": "your_bearer_token",
    "test_payload": {
      "test_name": "sample_test",
      "config": {"users": 10}
    },
    "framework": "fps"
  }'""")
    
    print("\n3. Direct FPS Submission:")
    print("""curl -X POST https://your-app.herokuapp.com/api/v1/submit/fps \\
  -H "Content-Type: application/json" \\
  -d '{
    "authtoken": "your_bearer_token",
    "test_payload": {
      "test_name": "sample_test",
      "config": {"users": 10}
    }
  }'""")

if __name__ == "__main__":
    print("UCE Adapter Service Test Script")
    print("Note: Make sure the service is running before executing tests")
    print("To run locally: python app.py")
    print("To test: python test_service.py")
    
    choice = input("\nChoose option:\n1. Run tests\n2. Show curl examples\n3. Both\nEnter (1/2/3): ")
    
    if choice in ['1', '3']:
        test_service()
    
    if choice in ['2', '3']:
        example_curl_commands()
