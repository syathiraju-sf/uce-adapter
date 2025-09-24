#!/usr/bin/env python3
"""
Test connectivity to FPS API endpoint to diagnose timeout issues.
"""

import requests
import time
import socket
from urllib.parse import urlparse

# Your FPS API details
FPS_URL = "https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns/2915731b-62f7-490f-bc24-2b4c583c7ff2"
TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6VFhTQTFRR1hrNkhFY2YxclJGVktoZVNmeEVOT3JDLUhBRlBPcmkyWm5NIn0.eyJleHAiOjE3NjAyMDAwNzYsImlhdCI6MTc1NzUyMTY3NiwianRpIjoiMWZmNTQ2ODAtZjk0MS00ZDg0LWI5NTAtZDA0NzBlNDMxYmFlIiwiaXNzIjoiaHR0cHM6Ly9xdWFudHVtay1oYS5mb3VuZGF0aW9uLnBlcmYxLXVzZWFzdDIuYXdzLnNmZGMuY2wvYXV0aC9yZWFsbXMvY2VudHJhbHBlcmZmb3VuZGF0aW9uIiwiYXVkIjoiY3BmLW1lcmxpbi1vaWRjIiwic3ViIjoiZjphMnpyZGZMN1N0NjYzUGpGMlhrQmtROnN5YXRoaXJhanUiLCJ0eXAiOiJJRCIsImF6cCI6ImNwZi1tZXJsaW4tb2lkYyIsInNpZCI6IjdhNWIzOGQ3LTA0ZDEtNDc0OC05MDc0LTMwNTE0MzhlZWFiNCIsImF0X2hhc2giOiJmTXZoSTRyWUk4VVNBUDVoajhYd1JRIiwiZW1wbG95ZWVfdHlwZSI6ImVtcGxveWVlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWNlbnRyYWxwZXJmZm91bmRhdGlvbiIsInVtYV9hdXRob3JpemF0aW9uIl19LCJuYW1lIjoiU2FjaGluIFlhdGhpcmFqdSBzeWF0aGlyYWp1IiwicHJlZmVycmVkX3VzZXJuYW1lIjoic3lhdGhpcmFqdSIsImdpdmVuX25hbWUiOiJTYWNoaW4gWWF0aGlyYWp1IiwiZmFtaWx5X25hbWUiOiJzeWF0aGlyYWp1IiwiZW1haWwiOiJzeWF0aGlyYWp1QHNhbGVzZm9yY2UuY29tIiwiY2xpZW50SWRlbnRpdHkiOiJjcGYtbWVybGluLW9pZGMifQ.na2y_Xo3vwiIBY7PCf_0fLd5RENGB8F-eQV6acwUhrvy5keFlPVtv1RgXPkd5XtvhxASrlnxlmEGlNt1R2KL0BfxF-2_egOPfivsPu2XkywyYB7qmYuEv0ASYmxbh0eGsr1kSuDm2QKSkPEkSkj-gdsWM_7hnC7VpzUTUXYGFBPBMS43uBV2y7lsZwDWok5v7ZCsWjywWiKqwPX6Cspl2Wkja0dnw5IM31dTc9NdPUDVHyrLA2fHRHgyIO36gJTMqXbjZnkykstw-NR1ZbS5ttQ64wkTQvBhGe5REARvpjqj5-itEyaFavbN99WKbj9lwdVd4Zt84UxFym1V5bIn5w"

def test_dns_resolution():
    """Test DNS resolution for the FPS API domain."""
    print("🔍 Testing DNS Resolution...")
    try:
        parsed_url = urlparse(FPS_URL)
        hostname = parsed_url.hostname
        ip_address = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution successful: {hostname} -> {ip_address}")
        return True
    except Exception as e:
        print(f"❌ DNS Resolution failed: {e}")
        return False

def test_tcp_connection():
    """Test TCP connection to the FPS API server."""
    print("\n🔌 Testing TCP Connection...")
    try:
        parsed_url = urlparse(FPS_URL)
        hostname = parsed_url.hostname
        port = 443 if parsed_url.scheme == 'https' else 80
        
        start_time = time.time()
        sock = socket.create_connection((hostname, port), timeout=10)
        connect_time = (time.time() - start_time) * 1000
        sock.close()
        
        print(f"✅ TCP Connection successful: {hostname}:{port} in {connect_time:.2f}ms")
        return True
    except Exception as e:
        print(f"❌ TCP Connection failed: {e}")
        return False

def test_http_head_request():
    """Test HTTP HEAD request (faster than GET)."""
    print("\n📡 Testing HTTP HEAD Request...")
    try:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"bearer {TOKEN}"
        }
        
        start_time = time.time()
        response = requests.head(
            FPS_URL,
            headers=headers,
            verify=False,
            timeout=(5, 10)  # 5s connect, 10s read
        )
        request_time = (time.time() - start_time) * 1000
        
        print(f"✅ HTTP HEAD successful: Status {response.status_code} in {request_time:.2f}ms")
        print(f"   Server: {response.headers.get('Server', 'Unknown')}")
        print(f"   Content-Length: {response.headers.get('Content-Length', 'Unknown')}")
        return True
    except requests.exceptions.Timeout as e:
        print(f"⏰ HTTP HEAD timed out: {e}")
        return False
    except Exception as e:
        print(f"❌ HTTP HEAD failed: {e}")
        return False

def test_http_get_with_timeouts():
    """Test HTTP GET with various timeout values."""
    print("\n🚀 Testing HTTP GET with different timeouts...")
    
    timeouts = [5, 10, 15, 20, 30]
    
    for timeout_val in timeouts:
        print(f"\n⏱️  Testing with {timeout_val}s timeout...")
        try:
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"bearer {TOKEN}"
            }
            
            start_time = time.time()
            response = requests.get(
                FPS_URL,
                headers=headers,
                verify=False,
                timeout=(5, timeout_val)  # 5s connect, variable read
            )
            request_time = (time.time() - start_time) * 1000
            
            print(f"   ✅ SUCCESS: Status {response.status_code} in {request_time:.2f}ms")
            print(f"   📊 Response size: {len(response.text)} characters")
            return True, request_time
            
        except requests.exceptions.Timeout as e:
            print(f"   ⏰ TIMEOUT after {timeout_val}s")
            continue
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            continue
    
    print("❌ All timeout attempts failed")
    return False, None

def test_connectivity_from_heroku_perspective():
    """Simulate what happens on Heroku."""
    print("\n🏗️  Simulating Heroku Environment...")
    
    # Test with similar constraints as Heroku
    try:
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"bearer {TOKEN}",
            "User-Agent": "HerokuApp/1.0"
        }
        
        start_time = time.time()
        response = requests.get(
            FPS_URL,
            headers=headers,
            verify=False,
            timeout=(3, 25),  # Heroku-like constraints
            stream=True  # Don't load full response into memory
        )
        
        # Read response in chunks to simulate streaming
        content_length = 0
        for chunk in response.iter_content(chunk_size=1024):
            content_length += len(chunk)
            elapsed = time.time() - start_time
            if elapsed > 25:  # Heroku timeout simulation
                print(f"   ⏰ Simulated Heroku timeout after {elapsed:.1f}s")
                return False
        
        request_time = (time.time() - start_time) * 1000
        print(f"   ✅ Heroku simulation SUCCESS: {response.status_code} in {request_time:.2f}ms")
        print(f"   📊 Response size: {content_length} bytes")
        return True
        
    except Exception as e:
        print(f"   ❌ Heroku simulation failed: {e}")
        return False

def main():
    """Run all connectivity tests."""
    print("🧪 FPS API Connectivity Diagnostic Tests")
    print("=" * 60)
    
    results = {}
    
    # Test 1: DNS Resolution
    results['dns'] = test_dns_resolution()
    
    # Test 2: TCP Connection
    results['tcp'] = test_tcp_connection()
    
    # Test 3: HTTP HEAD (quick test)
    results['head'] = test_http_head_request()
    
    # Test 4: HTTP GET with timeouts
    results['get'], response_time = test_http_get_with_timeouts()
    
    # Test 5: Heroku simulation
    results['heroku'] = test_connectivity_from_heroku_perspective()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 CONNECTIVITY TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():.<20} {status}")
    
    # Diagnosis
    print("\n🔍 DIAGNOSIS:")
    if all(results.values()):
        print("✅ All connectivity tests passed!")
        print("💡 The API is accessible and working.")
        if response_time and response_time > 25000:
            print(f"⚠️  However, response time ({response_time:.0f}ms) exceeds Heroku's 30s limit.")
            print("💡 This explains the H12 timeout errors on Heroku.")
    elif not results['dns']:
        print("❌ DNS resolution failed - domain name issue")
    elif not results['tcp']:
        print("❌ TCP connection failed - network/firewall issue")
    elif not results['head']:
        print("❌ HTTP HEAD failed - server/authentication issue")
    elif not results['get']:
        print("❌ HTTP GET failed - API is too slow or unresponsive")
    elif not results['heroku']:
        print("❌ Heroku simulation failed - API takes too long for Heroku environment")
    
    print("\n🚀 RECOMMENDATIONS:")
    if not all(results.values()):
        print("• Check network connectivity to performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl")
        print("• Verify the auth token is still valid")
        print("• Try the /api/v1/fps/fast endpoint for immediate response")
    else:
        print("• API is accessible but slow - use timeout handling")
        print("• Consider using the /api/v1/fps/fast endpoint for quick responses")
        print("• The real API may work during off-peak hours")

if __name__ == "__main__":
    main()
