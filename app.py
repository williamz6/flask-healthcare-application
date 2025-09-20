from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

app = Flask(__name__)

# load environment variablees from .env file
load_dotenv()

# get credentials from .env

mongodb_user = os.getenv('MONGODB_USER')
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_cluster = os.getenv('MONGODB_CLUSTER')

if not all([mongodb_user, mongodb_password, mongodb_cluster]):
    raise ValueError("Missing one or more required environment variables: MONGODB_USER, MONGODB_PASSWORD, MONGODB_CLUSTER")

# encode username and password to handle special characters
encoded_username = quote_plus(mongodb_user)
encoded_password = quote_plus(mongodb_password)

# Construct the url
url = f"mongodb+srv://{encoded_username}:{encoded_password}@{mongodb_cluster}/?retryWrites=true&w=majority&appName=survey-cluster"

# Create a new client and connect to the server
client = MongoClient(url, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# define database and collection
db = client.survey_db

# collections:users_col

users_col = db['users']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        total_income = request.form.get('total_income')
        expenses = {}
        expense_categories = ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']

        for category in expense_categories:
            if request.form.get(category + '_checkbox'):
                amount = request.form.get(category + '_amount', 0)
                expenses[category] = float(amount) if amount else 0.0
        
        user_data = {
            'age': int(age) if age else None,
            'gender': gender,
            'total_income': float(total_income) if total_income else 0.0,
            'expenses': expenses
        }

        users_col.insert_one(user_data)
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
