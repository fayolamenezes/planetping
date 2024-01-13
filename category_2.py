from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Define the URL of your Flask server with the specific IP address and port
server_url = "http://192.168.19.59:5000/classify"  # Replace with the IP address and port of your Flask app

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amazon_url = request.form["amazon_url"] 
        if not amazon_url:
            return jsonify({"error": "Invalid Amazon URL provided"})

        # Create a JSON payload with the Amazon URL
        payload = {"amazon_url": amazon_url}

        # Send a POST request to the Flask server
        try:
            response = requests.post(server_url, json=payload)
            response_data = response.json()
            return render_template("result.html", response=response_data)
        except requests.exceptions.RequestException as e:
            return jsonify({"error": "Failed to connect to the Flask server. Check the server URL."})

    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    response = requests.post(server_url, json=request.json)
    response_data = response.json()
                                            
    return jsonify({"amazon_url": response_data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)  # Set the host and port for your Flask app
