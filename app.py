"""
FPS API Client - Heroku service for accessing FPS performance data.
"""

import os
from flask import Flask, request, jsonify
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

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "FPS API Client",
        "version": "1.0.0",
        "description": "Heroku service for accessing FPS performance API",
        "endpoints": {
            "health": "/",
            "get_perfrun": "/api/v1/perfruns/<run_id>",
            "get_perfrun_proxy": "/api/v1/fps/get"
        },
        "usage": {
            "get_perfrun": "GET /api/v1/perfruns/{run_id}?token=your_bearer_token",
            "get_perfrun_proxy": "POST /api/v1/fps/get with JSON body"
        }
    })

@app.route('/api/v1/perfruns/<run_id>', methods=['GET'])
def get_perfrun(run_id):
    """
    Get performance run data by ID.
    
    Usage: GET /api/v1/perfruns/{run_id}?token=your_bearer_token
    """
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    logger.info(f"🚀 [REQUEST:{request_id}] GET perfrun: {run_id}")
    
    try:
        # Get token from query parameter
        token = request.args.get('token')
        
        if not token:
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "error": "Missing 'token' query parameter",
                "usage": "GET /api/v1/perfruns/{run_id}?token=your_bearer_token"
            }), 400
        
        # FPS API endpoint
        url = f"https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns/{run_id}"
        
        # Headers
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"bearer {token}"
        }
        
        logger.info(f"📡 [REQUEST:{request_id}] Calling FPS API: {url}")
        
        # Make GET request
        response = requests.get(
            url=url,
            headers=headers,
            verify=False
        )
        
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Log response
        logger.info(f"📈 [REQUEST:{request_id}] FPS API responded: {response.status_code}, Time: {execution_time_ms}ms")
        
        if response.status_code == 200:
            logger.info(f"✅ [REQUEST:{request_id}] Success")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "success",
                "execution_time_ms": execution_time_ms,
                "fps_data": response.json()
            }), 200
        else:
            logger.error(f"❌ [REQUEST:{request_id}] FPS API error: {response.status_code}")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "execution_time_ms": execution_time_ms,
                "fps_error": {
                    "status_code": response.status_code,
                    "message": response.text
                }
            }), response.status_code
    
    except requests.exceptions.RequestException as e:
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        logger.error(f"💥 [REQUEST:{request_id}] Request error: {str(e)}")
        return jsonify({
            "request_id": request_id,
            "timestamp": start_time.isoformat(),
            "status": "error",
            "execution_time_ms": execution_time_ms,
            "error": f"Request failed: {str(e)}"
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

@app.route('/api/v1/fps/get', methods=['POST'])
def fps_get_proxy():
    """
    Proxy endpoint for FPS API GET requests.
    
    Expected JSON payload:
    {
        "run_id": "2915731b-62f7-490f-bc24-2b4c583c7ff2",
        "token": "your_bearer_token"
    }
    """
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    logger.info(f"🚀 [REQUEST:{request_id}] FPS GET Proxy called")
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "error": "No JSON payload provided",
                "expected": {
                    "run_id": "performance_run_uuid",
                    "token": "bearer_token"
                }
            }), 400
        
        run_id = data.get('run_id')
        token = data.get('token')
        
        if not run_id:
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "error": "Missing 'run_id' in JSON payload"
            }), 400
        
        if not token:
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "error": "Missing 'token' in JSON payload"
            }), 400
        
        # FPS API endpoint
        url = f"https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns/{run_id}"
        
        # Headers
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"bearer {token}"
        }
        
        logger.info(f"📡 [REQUEST:{request_id}] Calling FPS API for run_id: {run_id}")
        
        # Make GET request
        response = requests.get(
            url=url,
            headers=headers,
            verify=False
        )
        
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Log response
        logger.info(f"📈 [REQUEST:{request_id}] FPS API responded: {response.status_code}, Time: {execution_time_ms}ms")
        
        if response.status_code == 200:
            logger.info(f"✅ [REQUEST:{request_id}] Success")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "success",
                "execution_time_ms": execution_time_ms,
                "fps_data": response.json()
            }), 200
        else:
            logger.error(f"❌ [REQUEST:{request_id}] FPS API error: {response.status_code}")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "execution_time_ms": execution_time_ms,
                "fps_error": {
                    "status_code": response.status_code,
                    "message": response.text
                }
            }), response.status_code
    
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
