from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/test_ping', methods=['POST'])
def hello_with_sleep():
    # Get JSON data from request
    data = request.get_json()
    
    # Validate that sleep parameter exists
    if not data or 'sleep' not in data:
        return jsonify({'error': 'Missing "sleep" parameter in request body'}), 400
    
    try:
        # Convert sleep parameter to float
        sleep_seconds = float(data['sleep'])
        
        # Validate sleep time is non-negative
        if sleep_seconds < 0:
            return jsonify({'error': 'Sleep time must be a non-negative number'}), 400
        
        # Sleep for the specified duration
        time.sleep(sleep_seconds)
        
        # Return success response after sleeping
        return jsonify({
            'message': 'Hello from the server!',
            'slept_for_seconds': sleep_seconds
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Sleep parameter must be a valid number'}), 400

if __name__ == '__main__':
    app.run(debug=True)
    
