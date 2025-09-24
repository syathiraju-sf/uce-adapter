"""
Flask web application for UCE Adapter - Test Run Executor service.
"""

import os
from flask import Flask, request, jsonify
import json
import logging

# Import the TestRunExecutor from the same directory
from testrunexecutor import TestRunExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the TestRunExecutor
executor = TestRunExecutor()

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "UCE Adapter - Test Run Executor",
        "version": "1.0.0",
        "endpoints": {
            "fps_test": "/api/v1/submit/fps",
            "rafi_test": "/api/v1/submit/rafi",
            "execute_test": "/api/v1/execute"
        }
    })

@app.route('/api/v1/execute', methods=['POST'])
def execute_test():
    """
    Main endpoint to execute test with authtoken and test_payload.
    
    Expected JSON payload:
    {
        "authtoken": "your_bearer_token",
        "test_payload": {
            // Your test configuration
        },
        "framework": "fps" // optional, defaults to "fps"
    }
    
    Returns:
    {
        "status": "success" | "error",
        "status_code": 200,
        "response": {...} | "error": "error message"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            logger.error("No JSON payload provided")
            return jsonify({
                "status": "error",
                "error": "No JSON payload provided",
                "required_fields": ["authtoken", "test_payload"]
            }), 400
        
        # Extract required parameters
        authtoken = data.get('authtoken')
        test_payload = data.get('test_payload')
        framework = data.get('framework', 'fps').lower()
        
        # Validate required parameters
        if not authtoken:
            return jsonify({
                "status": "error",
                "error": "authtoken is required",
                "example": {
                    "authtoken": "your_bearer_token_here",
                    "test_payload": {"key": "value"}
                }
            }), 400
        
        if not test_payload:
            return jsonify({
                "status": "error",
                "error": "test_payload is required",
                "example": {
                    "authtoken": "your_bearer_token_here",
                    "test_payload": {"key": "value"}
                }
            }), 400
        
        logger.info(f"Executing {framework} test with payload keys: {list(test_payload.keys())}")
        
        # Execute based on framework
        if framework == 'fps':
            result = executor.submitFPSTest(test_payload, authtoken)
        elif framework == 'rafi':
            result = executor.submitRAFITest(test_payload)
        else:
            return jsonify({
                "status": "error",
                "error": f"Unsupported framework: {framework}",
                "supported_frameworks": ["fps", "rafi"]
            }), 400
        
        # Log result status
        logger.info(f"Test execution result: {result.get('status', 'unknown')}")
        
        # Return appropriate status code based on result
        if result and result.get('status') == 'success':
            return jsonify(result), 200
        elif result and result.get('status') == 'error':
            status_code = result.get('status_code', 500)
            return jsonify(result), status_code
        else:
            return jsonify({
                "status": "error",
                "error": "No result returned from test execution"
            }), 500
    
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/v1/submit/fps', methods=['POST'])
def submit_fps_test():
    """
    Submit test to FPS framework.
    
    Expected JSON payload:
    {
        "test_payload": {...},
        "authtoken": "bearer_token"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        test_payload = data.get('test_payload')
        authtoken = data.get('authtoken')
        
        if not test_payload:
            return jsonify({"error": "test_payload is required"}), 400
        
        if not authtoken:
            return jsonify({"error": "authtoken is required"}), 400
        
        # Submit test to FPS
        result = executor.submitFPSTest(test_payload, authtoken)
        
        # Return appropriate status code based on result
        if result.get('status') == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), result.get('status_code', 500)
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/v1/submit/rafi', methods=['POST'])
def submit_rafi_test():
    """
    Submit test to RAFI framework.
    
    Expected JSON payload:
    {
        "test_payload": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        test_payload = data.get('test_payload')
        
        if not test_payload:
            return jsonify({"error": "test_payload is required"}), 400
        
        # Submit test to RAFI
        result = executor.submitRAFITest(test_payload)
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({
                "status": "error",
                "error": "RAFI test submission not implemented yet"
            }), 501
    
    except Exception as e:
        return jsonify({
            "status": "error",
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
