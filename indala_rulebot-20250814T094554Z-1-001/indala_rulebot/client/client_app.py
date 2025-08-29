from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"   # Make sure FastAPI is running here

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["message"]

    # Call FastAPI /chat endpoint
    try:
        response = requests.post(
            f"{FASTAPI_URL}/chat",
            json={"text": user_input},
            timeout=5   # prevent hanging if backend is down
        )
        response.raise_for_status()  # raise error for non-200
        data = response.json()
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Chatbot backend not reachable: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)

