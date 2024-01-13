from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Define the URL of your Flask server with the specific IP address and port
server_url = "http://192.168.19.59:5000/classify"  # Replace with the IP address and port of your Flask app

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amazon_url = request.form["amazon_url"]

        # Create a JSON payload with the Amazon URL
        payload = {"amazon_url": amazon_url}

        # Send a POST request to the Flask server
        response = requests.post(server_url, json=payload)

        # Get the response from the server
        response_data = response.json()

        return render_template("result.html", response=response_data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)  # Set the host and port for your Flask app
