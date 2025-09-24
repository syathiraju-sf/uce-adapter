"""
Flask web application for UCE Adapter - Test Run Executor service.
"""

import os
from flask import Flask, request, jsonify
import json
import logging
import uuid
from datetime import datetime
import requests

# Configure logging for Heroku
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Disable SSL warnings for Heroku deployment
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def submit_fps_test(test_payload, authtoken):
    """
    Submit test to FPS framework.
    
    Args:
        test_payload (dict): The test payload prepared for FPS framework
        authtoken (str): Authentication token for FPS framework
        
    Returns:
        dict: Response from FPS test submission
    """
    try:
        # FPS API endpoint
        url = "https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns"
        
        # Headers
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"bearer {authtoken}"
        }
        
        # Make POST request with SSL verification disabled (equivalent to -k flag)
        response = requests.post(
            url=url,
            headers=headers,
            json=test_payload,
            verify=False  # Equivalent to curl -k flag
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Return JSON response
        return {
            "status": "success",
            "status_code": response.status_code,
            "response": response.json()
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "UCE Adapter - FPS Test Executor",
        "version": "2.0.0",
        "description": "Heroku service to submit FPS tests with authtoken and test_payload",
        "endpoints": {
            "health": "/",
            "execute_fps": "/api/v1/execute"
        },
        "usage": {
            "method": "POST",
            "url": "/api/v1/execute",
            "payload": {
                "authtoken": "your_bearer_token",
                "test_payload": {"your": "test_data"}
            }
        }
    })

@app.route('/api/v1/execute', methods=['POST'])
def execute_test():
    """
    🎯 Execute FPS Test with authtoken and test_payload
    
    Expected JSON payload:
    {
        "authtoken": "your_bearer_token",
        "test_payload": {
            // Your FPS test configuration
        }
    }
    
    Returns:
    {
        "request_id": "uuid",
        "timestamp": "2023-...",
        "status": "success" | "error",
        "execution_time_ms": 1234,
        "result": {...}
    }
    """
    # Generate unique request ID for tracking
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    logger.info(f"🚀 [REQUEST:{request_id}] FPS Execute API called")
    
    try:
        # Parse request data
        data = request.get_json()
        logger.info(f"📥 [REQUEST:{request_id}] Received request data")
        
        if not data:
            logger.error(f"❌ [REQUEST:{request_id}] No JSON payload provided")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "error": "No JSON payload provided",
                "required_fields": ["authtoken", "test_payload"],
                "example": {
                    "authtoken": "your_bearer_token",
                    "test_payload": {"test_name": "sample", "config": {}}
                }
            }), 400
        
        # Extract parameters
        authtoken = data.get('authtoken')
        test_payload = data.get('test_payload')
        
        # Log request parameters (without sensitive data)
        logger.info(f"🔑 [REQUEST:{request_id}] Auth token: {'✓ Present' if authtoken else '✗ Missing'}")
        logger.info(f"📋 [REQUEST:{request_id}] Test payload: {'✓ Present' if test_payload else '✗ Missing'}")
        
        if test_payload:
            payload_keys = list(test_payload.keys()) if isinstance(test_payload, dict) else []
            logger.info(f"📊 [REQUEST:{request_id}] Payload keys: {payload_keys}")
        
        # Validate required parameters
        if not authtoken:
            logger.error(f"❌ [REQUEST:{request_id}] Missing authtoken")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "error": "authtoken is required"
            }), 400
        
        if not test_payload:
            logger.error(f"❌ [REQUEST:{request_id}] Missing test_payload")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "error": "test_payload is required"
            }), 400
        
        # Execute FPS test
        logger.info(f"⚡ [REQUEST:{request_id}] Executing FPS test submission...")
        execution_start = datetime.now()
        
        result = submit_fps_test(test_payload, authtoken)
        
        execution_end = datetime.now()
        execution_time_ms = int((execution_end - execution_start).total_seconds() * 1000)
        
        # Log execution result
        result_status = result.get('status', 'unknown') if result else 'no_result'
        logger.info(f"📈 [REQUEST:{request_id}] Execution completed - Status: {result_status}, Time: {execution_time_ms}ms")
        
        if result and result.get('status') == 'success':
            logger.info(f"✅ [REQUEST:{request_id}] FPS test submitted successfully")
            response_data = {
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "success",
                "execution_time_ms": execution_time_ms,
                "result": result
            }
            return jsonify(response_data), 200
        
        elif result and result.get('status') == 'error':
            logger.error(f"❌ [REQUEST:{request_id}] FPS test failed: {result.get('error', 'Unknown error')}")
            status_code = result.get('status_code', 500)
            response_data = {
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "execution_time_ms": execution_time_ms,
                "result": result
            }
            return jsonify(response_data), status_code
        
        else:
            logger.error(f"❌ [REQUEST:{request_id}] No valid result returned")
            return jsonify({
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "status": "error",
                "execution_time_ms": execution_time_ms,
                "error": "No valid result returned from test execution"
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
