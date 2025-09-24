"""
Simplified Flask app for debugging Heroku deployment.
"""

import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "UCE Adapter - FPS Test Executor",
        "version": "2.0.0",
        "python_version": f"{os.sys.version}",
        "endpoints": {
            "health": "/",
            "execute_fps": "/api/v1/execute"
        }
    })

@app.route('/api/v1/execute', methods=['POST'])
def execute_test():
    """Execute FPS Test"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "error": "No JSON payload provided"
            }), 400
        
        authtoken = data.get('authtoken')
        test_payload = data.get('test_payload')
        
        if not authtoken:
            return jsonify({
                "status": "error",
                "error": "authtoken is required"
            }), 400
        
        if not test_payload:
            return jsonify({
                "status": "error",
                "error": "test_payload is required"
            }), 400
        
        # FPS API call
        try:
            url = "https://performance.sfproxy.core1.perf1-useast2.aws.sfdc.cl/api/v1/perfruns"
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"bearer {authtoken}"
            }
            
            response = requests.post(
                url=url,
                headers=headers,
                json=test_payload,
                verify=False
            )
            
            return jsonify({
                "status": "success",
                "status_code": response.status_code,
                "response": response.json()
            }), 200
            
        except requests.exceptions.RequestException as e:
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": f"Internal server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
