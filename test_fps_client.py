#!/usr/bin/env python3
"""
Test script for FPS API Client service.
"""

import requests
import json

def test_fps_client():
    """Test the FPS API Client service."""
    
    # Configuration
    base_url = "http://localhost:5000"  # Change to your Heroku URL when deployed
    
    # Your FPS API details
    run_id = "2915731b-62f7-490f-bc24-2b4c583c7ff2"
    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6VFhTQTFRR1hrNkhFY2YxclJGVktoZVNmeEVOT3JDLUhBRlBPcmkyWm5NIn0.eyJleHAiOjE3NjAyMDAwNzYsImlhdCI6MTc1NzUyMTY3NiwianRpIjoiMWZmNTQ2ODAtZjk0MS00ZDg0LWI5NTAtZDA0NzBlNDMxYmFlIiwiaXNzIjoiaHR0cHM6Ly9xdWFudHVtay1oYS5mb3VuZGF0aW9uLnBlcmYxLXVzZWFzdDIuYXdzLnNmZGMuY2wvYXV0aC9yZWFsbXMvY2VudHJhbHBlcmZmb3VuZGF0aW9uIiwiYXVkIjoiY3BmLW1lcmxpbi1vaWRjIiwic3ViIjoiZjphMnpyZGZMN1N0NjYzUGpGMlhrQmtROnN5YXRoaXJhanUiLCJ0eXAiOiJJRCIsImF6cCI6ImNwZi1tZXJsaW4tb2lkYyIsInNpZCI6IjdhNWIzOGQ3LTA0ZDEtNDc0OC05MDc0LTMwNTE0MzhlZWFiNCIsImF0X2hhc2giOiJmTXZoSTRyWUk4VVNBUDVoajhYd1JRIiwiZW1wbG95ZWVfdHlwZSI6ImVtcGxveWVlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWNlbnRyYWxwZXJmZm91bmRhdGlvbiIsInVtYV9hdXRob3JpemF0aW9uIl19LCJuYW1lIjoiU2FjaGluIFlhdGhpcmFqdSBzeWF0aGlyYWp1IiwicHJlZmVycmVkX3VzZXJuYW1lIjoic3lhdGhpcmFqdSIsImdpdmVuX25hbWUiOiJTYWNoaW4gWWF0aGlyYWp1IiwiZmFtaWx5X25hbWUiOiJzeWF0aGlyYWp1IiwiZW1haWwiOiJzeWF0aGlyYWp1QHNhbGVzZm9yY2UuY29tIiwiY2xpZW50SWRlbnRpdHkiOiJjcGYtbWVybGluLW9pZGMifQ.na2y_Xo3vwiIBY7PCf_0fLd5RENGB8F-eQV6acwUhrvy5keFlPVtv1RgXPkd5XtvhxASrlnxlmEGlNt1R2KL0BfxF-2_egOPfivsPu2XkywyYB7qmYuEv0ASYmxbh0eGsr1kSuDm2QKSkPEkSkj-gdsWM_7hnC7VpzUTUXYGFBPBMS43uBV2y7lsZwDWok5v7ZCsWjywWiKqwPX6Cspl2Wkja0dnw5IM31dTc9NdPUDVHyrLA2fHRHgyIO36gJTMqXbjZnkykstw-NR1ZbS5ttQ64wkTQvBhGe5REARvpjqj5-itEyaFavbN99WKbj9lwdVd4Zt84UxFym1V5bIn5w"
    
    print("🚀 Testing FPS API Client Service")
    print("="*60)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: GET perfrun via query parameter
    print(f"\n2. Testing GET perfrun via query parameter...")
    try:
        response = requests.get(f"{base_url}/api/v1/perfruns/{run_id}?token={token}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Request ID: {data.get('request_id')}")
            print(f"Status: {data.get('status')}")
            print(f"Execution Time: {data.get('execution_time_ms')}ms")
            print(f"FPS Data Keys: {list(data.get('fps_data', {}).keys())}")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: POST proxy endpoint
    print(f"\n3. Testing POST proxy endpoint...")
    try:
        payload = {
            "run_id": run_id,
            "token": token
        }
        response = requests.post(
            f"{base_url}/api/v1/fps/get",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Request ID: {data.get('request_id')}")
            print(f"Status: {data.get('status')}")
            print(f"Execution Time: {data.get('execution_time_ms')}ms")
            print(f"FPS Data Keys: {list(data.get('fps_data', {}).keys())}")
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def print_curl_examples():
    """Print example curl commands."""
    print("\n📋 Example CURL commands for deployed app:")
    print("="*60)
    
    print("\n1. Health Check:")
    print("curl -X GET https://your-app.herokuapp.com/")
    
    print(f"\n2. GET Performance Run (Query Parameter):")
    print(f"""curl -X GET "https://your-app.herokuapp.com/api/v1/perfruns/2915731b-62f7-490f-bc24-2b4c583c7ff2?token=your_token_here" \\
  -H "accept: application/json" \\
  -H "Content-Type: application/json" """)
    
    print(f"\n3. GET Performance Run (POST Proxy):")
    print(f"""curl -X POST https://your-app.herokuapp.com/api/v1/fps/get \\
  -H "Content-Type: application/json" \\
  -d '{{
    "run_id": "2915731b-62f7-490f-bc24-2b4c583c7ff2",
    "token": "your_token_here"
  }}'""")

if __name__ == "__main__":
    print("🎯 FPS API Client - Test & Examples")
    print("Note: Make sure the service is running before executing tests")
    print("To run locally: python app.py")
    
    choice = input("\nChoose option:\n1. Run tests\n2. Show curl examples\n3. Both\nEnter (1/2/3): ")
    
    if choice in ['1', '3']:
        test_fps_client()
    
    if choice in ['2', '3']:
        print_curl_examples()
