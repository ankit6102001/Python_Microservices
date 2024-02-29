from flask import Flask, jsonify, request, make_response
import requests
import os
import jwt
from functools import wraps 
import json 
from jwt.exceptions import DecodeError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
port = int(os.environ.get("PORT", 5000))

BASE_URL = "https://dummyjson.com"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id'] 
        except DecodeError:
            return jsonify({'error': 'Authorization token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated 

with open('users.json','r') as f:
    users= json.load(f)
@app.route('/auth', methods=['POST'])
def authenticate_user():
    # if request.headers.get('Content-Type') == 'application/json':
    #     return jsonify({'error':'Content-Type must be application/x-www-form-urlencoded'}), 415 
    username= request.json.get('username')
    password = request.json.get('password')
    for user in users:
        if user['username'] == username and user['password'] == password:
            token = jwt.encode({'user_id': user['id']},  app.config['SECRET_KEY'], algorithm="HS256")    
            response= make_response(jsonify({'message': 'Login successful', 'token': token}), 200)
            response.set_cookie('token', token)
            return response
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route("/")
def home():
    return "Hello, Flask Microservice!"

@app.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    try:
        headers = {'Authorization': f'Bearer {request.cookies.get("token")}'}
        response = requests.get(f"{BASE_URL}/products", headers=headers)
        response.raise_for_status()

        # Print debugging information
        print(f"External API Response Content: {response.content}")

        products = []
        for product in response.json().get('products', []):
            product_data = {
                'id': product.get('id', ''),
                'title': product.get('title', ''),
                'brand': product.get('brand', ''),
                'price': product.get('price', ''),
                'description': product.get('description', '')
            }
            products.append(product_data)

        return jsonify({'data': products}), 200 if products else 204

    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return jsonify({'error': 'Failed to fetch data from the external API', 'details': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
