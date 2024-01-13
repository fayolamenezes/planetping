import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

# Model for classification
class SustainabilityModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = LogisticRegression()
        labeled_data = [
            ("sustainable product", "sustainable"),
            ("eco-friendly item", "sustainable"),
            ("traditional phone", "not sustainable"),
            ("conventional gadget", "not sustainable"),
            ("Jute", "Reuseable"),
        ]
        text_data, labels = zip(*labeled_data)
        x = self.vectorizer.fit_transform(text_data)
        self.classifier.fit(x, labels)

    def classify(self, product_title, product_description):
        input_data = [product_title + " " + product_description]
        input_vector = self.vectorizer.transform(input_data)
        prediction = self.classifier.predict(input_vector)
        return prediction[0]

model = SustainabilityModel()

# Function to scrape product information from Amazon
def scrape_amazon_product(url):
    try:
        headers = {
            'User-Agent': 'Your User Agent Here',
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        product_title = soup.find('span', {'id': 'productTitle'}).get_text().strip()
        product_description = soup.find('meta', {'name': 'description'})['content']
        return product_title, product_description
    except requests.exceptions.RequestException as e:
        return None, None

# Function to save data to a CSV file
def save_to_csv(product_url, product_title, product_description, classification):
    with open('product_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([product_url, product_title, product_description, classification])

@app.route('/classify', methods=['POST'])
def classify_product():
    data = request.json
    amazon_url = data.get('amazon_url')
    
    if amazon_url:
        product_title, product_description = scrape_amazon_product(amazon_url)
        if product_title and product_description:
            label = model.classify(product_title, product_description)
            save_to_csv(amazon_url, product_title, product_description, label)
            return jsonify({"result": label})
    
    return jsonify({"error": "Failed to classify the product"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
