"""
FPS API Client - Simple Heroku service with hardcoded values.
"""

import os
from flask import Flask, jsonify
import requests
import logging
from datetime import datetime
import uuid

# Configure logging for Heroku
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Hardcoded values
HARDCODED_RUN_ID = "2915731b-62f7-490f-bc24-2b4c583c7ff2"
HARDCODED_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ6VFhTQTFRR1hrNkhFY2YxclJGVktoZVNmeEVOT3JDLUhBRlBPcmkyWm5NIn0.eyJleHAiOjE3NjAyMDAwNzYsImlhdCI6MTc1NzUyMTY3NiwianRpIjoiMWZmNTQ2ODAtZjk0MS00ZDg0LWI5NTAtZDA0NzBlNDMxYmFlIiwiaXNzIjoiaHR0cHM6Ly9xdWFudHVtay1oYS5mb3VuZGF0aW9uLnBlcmYxLXVzZWFzdDIuYXdzLnNmZGMuY2wvYXV0aC9yZWFsbXMvY2VudHJhbHBlcmZmb3VuZGF0aW9uIiwiYXVkIjoiY3BmLW1lcmxpbi1vaWRjIiwic3ViIjoiZjphMnpyZGZMN1N0NjYzUGpGMlhrQmtROnN5YXRoaXJhanUiLCJ0eXAiOiJJRCIsImF6cCI6ImNwZi1tZXJsaW4tb2lkYyIsInNpZCI6IjdhNWIzOGQ3LTA0ZDEtNDc0OC05MDc0LTMwNTE0MzhlZWFiNCIsImF0X2hhc2giOiJmTXZoSTRyWUk4VVNBUDVoajhYd1JRIiwiZW1wbG95ZWVfdHlwZSI6ImVtcGxveWVlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWNlbnRyYWxwZXJmZm91bmRhdGlvbiIsInVtYV9hdXRob3JpemF0aW9uIl19LCJuYW1lIjoiU2FjaGluIFlhdGhpcmFqdSBzeWF0aGlyYWp1IiwicHJlZmVycmVkX3VzZXJuYW1lIjoic3lhdGhpcmFqdSIsImdpdmVuX25hbWUiOiJTYWNoaW4gWWF0aGlyYWp1IiwiZmFtaWx5X25hbWUiOiJzeWF0aGlyYWp1IiwiZW1haWwiOiJzeWF0aGlyYWp1QHNhbGVzZm9yY2UuY29tIiwiY2xpZW50SWRlbnRpdHkiOiJjcGYtbWVybGluLW9pZGMifQ.na2y_Xo3vwiIBY7PCf_0fLd5RENGB8F-eQV6acwUhrvy5keFlPVtv1RgXPkd5XtvhxASrlnxlmEGlNt1R2KL0BfxF-2_egOPfivsPu2XkywyYB7qmYuEv0ASYmxbh0eGsr1kSuDm2QKSkPEkSkj-gdsWM_7hnC7VpzUTUXYGFBPBMS43uBV2y7lsZwDWok5v7ZCsWjywWiKqwPX6Cspl2Wkja0dnw5IM31dTc9NdPUDVHyrLA2fHRHgyIO36gJTMqXbjZnkykstw-NR1ZbS5ttQ64wkTQvBhGe5REARvpjqj5-itEyaFavbN99WKbj9lwdVd4Zt84UxFym1V5bIn5w"

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "FPS API Client (Hardcoded)",
        "version": "2.0.0",
        "description": "Simple Heroku service with hardcoded FPS API call",
        "endpoints": {
            "health": "/",
            "get_fps_data": "/api/v1/fps",
            "get_fps_fast": "/api/v1/fps/fast", 
            "test": "/api/v1/test",
            "connectivity_test": "/api/v1/connectivity"
        },
        "hardcoded_values": {
            "run_id": HARDCODED_RUN_ID,
            "token_preview": HARDCODED_TOKEN[:50] + "..."
        }
    })

@app.route('/api/v1/test', methods=['GET'])
def test_endpoint():
    """Quick test endpoint that doesn't call external APIs."""
    return jsonify({
        "status": "success",
        "message": "Test endpoint working!",
        "timestamp": datetime.now().isoformat(),
        "hardcoded_values": {
            "run_id": HARDCODED_RUN_ID,
            "token_length": len(HARDCODED_TOKEN)
        }
    })

@app.route('/api/v1/connectivity', methods=['GET'])
def test_connectivity():
    """
    Test connectivity to FPS API without making the full request.
    This helps diagnose if the issue is connectivity or API response time.
    """
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    logger.info(f"🔍 [REQUEST:{request_id}] Testing FPS API connectivity")
    
    try:
        import socket
        from urllib.parse import urlparse
        
        # Test 1: DNS Resolution
        url = f"https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns/{HARDCODED_RUN_ID}"
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        
        dns_start = datetime.now()
        ip_address = socket.gethostbyname(hostname)
        dns_time = int((datetime.now() - dns_start).total_seconds() * 1000)
        
        # Test 2: TCP Connection
        tcp_start = datetime.now()
        sock = socket.create_connection((hostname, 443), timeout=5)
        tcp_time = int((datetime.now() - tcp_start).total_seconds() * 1000)
        sock.close()
        
        # Test 3: HTTP HEAD (quick test)
        head_start = datetime.now()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"bearer {HARDCODED_TOKEN}"
        }
        
        response = requests.head(
            url=url,
            headers=headers,
            verify=False,
            timeout=(3, 5)
        )
        head_time = int((datetime.now() - head_start).total_seconds() * 1000)
        
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        logger.info(f"✅ [REQUEST:{request_id}] Connectivity test successful")
        
        return jsonify({
            "request_id": request_id,
            "timestamp": start_time.isoformat(),
            "status": "success",
            "total_time_ms": total_time,
            "tests": {
                "dns_resolution": {
                    "hostname": hostname,
                    "ip_address": ip_address,
                    "time_ms": dns_time
                },
                "tcp_connection": {
                    "host": f"{hostname}:443",
                    "time_ms": tcp_time
                },
                "http_head": {
                    "status_code": response.status_code,
                    "time_ms": head_time
                }
            },
            "diagnosis": "API endpoint is reachable from this server"
        }), 200
        
    except Exception as e:
        total_time = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.error(f"❌ [REQUEST:{request_id}] Connectivity test failed: {str(e)}")
        
        return jsonify({
            "request_id": request_id,
            "timestamp": start_time.isoformat(),
            "status": "error",
            "total_time_ms": total_time,
            "error": str(e),
            "diagnosis": "API endpoint is not reachable from this server"
        }), 500

@app.route('/api/v1/fps/fast', methods=['GET'])
def get_fps_data_fast():
    """
    Fast endpoint that returns sample data when the real API is slow.
    Use this when you need immediate response.
    """
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    logger.info(f"🚀 [REQUEST:{request_id}] Fast FPS endpoint called")
    
    # Sample data based on your actual API structure
    sample_fps_data = {
        "perfruns": [{
            "request_id": HARDCODED_RUN_ID,
            "status": "SAMPLE_DATA",
            "note": "This is sample data - the real API was too slow",
            "end_time": "2025-09-23T09:25:44.103558Z",
            "perfrun_duration": "43m48s",
            "result_status": "PASSED",
            "perfrun_tasks": [
                {"name": "Env Config", "status": "FINISHED", "duration": "5m18s"},
                {"name": "Perf Run Execution", "status": "FINISHED", "duration": "27m21s"},
                {"name": "Metric Collection", "status": "FINISHED", "duration": "15m42s"}
            ]
        }],
        "total_count": 1
    }
    
    execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
    
    return jsonify({
        "request_id": request_id,
        "timestamp": start_time.isoformat(),
        "status": "success",
        "execution_time_ms": execution_time_ms,
        "data_type": "sample",
        "note": "This is sample data returned quickly. Use /api/v1/fps for real data (slower).",
        "hardcoded_values": {
            "run_id": HARDCODED_RUN_ID,
            "token_used": "✓ Not needed for sample data"
        },
        "fps_data": sample_fps_data
    }), 200

@app.route('/api/v1/fps', methods=['GET'])
def get_fps_data():
    """
    Simple endpoint that executes the hardcoded curl command.
    No inputs required - everything is hardcoded.
    """
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    logger.info(f"🚀 [REQUEST:{request_id}] FPS API call with hardcoded values")
    
    try:
        # FPS API endpoint with hardcoded run ID
        url = f"https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns/{HARDCODED_RUN_ID}"
        
        # Headers with hardcoded token
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"bearer {HARDCODED_TOKEN}"
        }
        
        logger.info(f"📡 [REQUEST:{request_id}] Calling FPS API: {url}")
        
        # Check if we're already approaching timeout limit
        elapsed_time = (datetime.now() - start_time).total_seconds()
        if elapsed_time > 25:
            logger.error(f"⏰ [REQUEST:{request_id}] Pre-request timeout check failed - already {elapsed_time:.1f}s elapsed")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "execution_time_ms": int(elapsed_time * 1000),
                "error": "Request aborted - approaching Heroku timeout limit",
                "error_type": "pre_timeout"
            }), 504
        
        # Make GET request with aggressive timeouts (equivalent to your curl command)
        response = requests.get(
            url=url,
            headers=headers,
            verify=False,  # Equivalent to curl -k flag
            timeout=(5, 20)  # (connect_timeout=5s, read_timeout=20s) = max 25s total
        )
        
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Double-check we haven't exceeded time limit
        if execution_time_ms > 28000:  # 28 seconds
            logger.error(f"⏰ [REQUEST:{request_id}] Post-request timeout - took {execution_time_ms}ms")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "execution_time_ms": execution_time_ms,
                "error": "Request completed but exceeded safe time limit",
                "error_type": "post_timeout"
            }), 504
        
        # Log response
        logger.info(f"📈 [REQUEST:{request_id}] FPS API responded: {response.status_code}, Time: {execution_time_ms}ms")
        
        if response.status_code == 200:
            logger.info(f"✅ [REQUEST:{request_id}] Success - Retrieved FPS data")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "success",
                "execution_time_ms": execution_time_ms,
                "hardcoded_values": {
                    "run_id": HARDCODED_RUN_ID,
                    "token_used": "✓ Hardcoded token"
                },
                "fps_data": response.json()
            }), 200
        else:
            logger.error(f"❌ [REQUEST:{request_id}] FPS API error: {response.status_code}")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "execution_time_ms": execution_time_ms,
                "hardcoded_values": {
                    "run_id": HARDCODED_RUN_ID,
                    "token_used": "✓ Hardcoded token"
                },
                "fps_error": {
                    "status_code": response.status_code,
                    "message": response.text
                }
            }), response.status_code
    
    except requests.exceptions.Timeout as e:
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.error(f"⏰ [REQUEST:{request_id}] Request timeout after {execution_time_ms}ms")
        return jsonify({
            "request_id": request_id,
            "timestamp": start_time.isoformat(),
            "status": "error",
            "execution_time_ms": execution_time_ms,
            "error": "FPS API request timed out after 25 seconds",
            "error_type": "timeout",
            "suggestion": "The FPS API is taking longer than expected. Try again later."
        }), 504  # Gateway Timeout
        
    except requests.exceptions.RequestException as e:
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.error(f"💥 [REQUEST:{request_id}] Request error: {str(e)}")
        return jsonify({
            "request_id": request_id,
            "timestamp": start_time.isoformat(),
            "status": "error",
            "execution_time_ms": execution_time_ms,
            "error": f"Request failed: {str(e)}",
            "error_type": "request_error"
        }), 500
    
    except Exception as e:
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.error(f"💥 [REQUEST:{request_id}] Unexpected error: {str(e)}")
        return jsonify({
            "request_id": request_id,
            "timestamp": start_time.isoformat(),
            "status": "error",
            "execution_time_ms": execution_time_ms,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
