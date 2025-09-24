#!/usr/bin/env python3
"""
Test script for FPS API Client service (Hardcoded version).
"""

import requests
import json

def test_fps_client():
    """Test the FPS API Client service with hardcoded values."""
    
    # Configuration
    base_url = "http://localhost:5000"  # Change to your Heroku URL when deployed
    
    print("🚀 Testing FPS API Client Service (Hardcoded)")
    print("="*60)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Simple FPS data retrieval (no inputs needed!)
    print(f"\n2. Testing FPS data retrieval (hardcoded values)...")
    try:
        response = requests.get(f"{base_url}/api/v1/fps")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Request ID: {data.get('request_id')}")
            print(f"Status: {data.get('status')}")
            print(f"Execution Time: {data.get('execution_time_ms')}ms")
            print(f"Hardcoded Run ID: {data.get('hardcoded_values', {}).get('run_id')}")
            fps_data = data.get('fps_data', {})
            if fps_data:
                print(f"FPS Data Keys: {list(fps_data.keys())}")
                print(f"Sample FPS Data: {json.dumps(dict(list(fps_data.items())[:3]), indent=2)}")
            else:
                print("No FPS data returned")
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
    
    print("\n2. Get FPS Data (Hardcoded - No inputs needed!):")
    print("curl -X GET https://your-app.herokuapp.com/api/v1/fps")
    
    print("\n🎯 That's it! The service uses hardcoded values:")
    print("   - Run ID: 2915731b-62f7-490f-bc24-2b4c583c7ff2")
    print("   - Token: Your JWT token (hardcoded)")
    print("   - No query parameters or JSON body required!")

if __name__ == "__main__":
    print("🎯 FPS API Client - Test & Examples")
    print("Note: Make sure the service is running before executing tests")
    print("To run locally: python app.py")
    
    choice = input("\nChoose option:\n1. Run tests\n2. Show curl examples\n3. Both\nEnter (1/2/3): ")
    
    if choice in ['1', '3']:
        test_fps_client()
    
    if choice in ['2', '3']:
        print_curl_examples()
