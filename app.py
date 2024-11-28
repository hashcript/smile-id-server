from flask import Flask, jsonify, request
from smile_id_core import WebApi, ServerError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Smile ID configuration
PARTNER_ID = "6482"  # Your Smile ID partner ID
DEFAULT_CALLBACK = "https://f82f-154-159-252-175.ngrok-free.app"
API_KEY = "0c0960f9-5f38-47c8-96c4-5aa229d4410d"  # Your Smile ID API key
SID_SERVER = 0  # Sandbox (use 1 for production)

# Initialize Smile ID connection
connection = WebApi(PARTNER_ID, DEFAULT_CALLBACK, API_KEY, SID_SERVER)

@app.route('/get-token', methods=['POST'])
def get_token():
    try:
        data = request.json
        user_id = data.get("user_id", "default_user")
        job_id = data.get("job_id", "default_job")
        product = data.get("product", "biometric_kyc")  # Updated for biometric API

        # Generate web token for biometric liveness
        response = connection.get_web_token(user_id, job_id, product)
        print(response)
        return jsonify(response), 200
    except ValueError as e:
        return jsonify({"error": "Invalid parameters", "details": str(e)}), 400
    except ServerError as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

# New route to handle callback and print to terminal
@app.route('/callback', methods=['POST'])
def handle_callback():
    try:
        # Get JSON data from the callback request
        callback_data = request.json
        
        # Print callback data to the terminal
        print("Received callback data:")
        print(callback_data)

        # Respond with a success status
        return jsonify({"status": "success", "message": "Callback data received"}), 200

    except Exception as e:
        print(f"Error handling callback: {e}")
        return jsonify({"error": "Error handling callback", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
