import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import socket

# Replace with the actual IP or hostname of your backend server
backend_url = 'http://10.0.2.169:8080/api/value'
backend_url = 'http://internal-BackendLB-1038863322.us-east-1.elb.amazonaws.com:8080/api/value'

app = Flask(__name__)
CORS(app)

@app.route('/api/value', methods=['POST'])
def get_value():
    try:
        # log data from the incoming request
        data = request.json
        # print(f"Received data: {data}")

        # Forward the POST request to the backend with the same JSON data
        response = requests.post(backend_url, json=data)

        # Check if the backend request was successful (status 200)
        if response.status_code == 200:
            # Parse the JSON response from the backend
            backend_data = response.json()

            # log data
            # print(f"Backend response: {backend_data}")

            # Return the backend response as a JSON response to the original client
            backend_data['frontendhost'] = socket.gethostname()
            response = jsonify(backend_data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 200

        else:
            # Log the backend's response if it failed
            print(f"Failed with status code {response.status_code}: {response.text}")
            return jsonify({'error': 'Failed to retrieve data from backend', 'details': response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        # Log and return an error if the request to the backend fails
        print(f"Error while making request: {e}")
        return jsonify({'error': 'Request to backend failed', 'details': str(e)}), 500

    except Exception as e:
        # Catch any other exceptions and return a 500 error
        print(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
