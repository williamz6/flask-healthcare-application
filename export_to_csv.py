# export_to_csv.py

import csv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
from user import User

# Load environment variables from .env file
load_dotenv()

# Get credentials from .env
mongodb_user = os.getenv('MONGODB_USER')
mongodb_password = os.getenv('MONGODB_PASSWORD')
mongodb_cluster = os.getenv('MONGODB_CLUSTER')

if not all([mongodb_user, mongodb_password, mongodb_cluster]):
    raise ValueError("Missing MONGODB_USER, MONGODB_PASSWORD, or MONGODB_CLUSTER in .env file.")

# Encode username and password to handle special characters
encoded_username = quote_plus(mongodb_user)
encoded_password = quote_plus(mongodb_password)

# Construct the URI
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{mongodb_cluster}/?retryWrites=true&w=majority&appName=survey-cluster"

# Create a new client and connect to the server
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')  # Test connection
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Connection failed: {e}")
    raise

# Define database and collection
db = client['survey_db']
users_col = db['users']

# Get the directory of the current script (survey-app folder)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the full path for the CSV file inside survey-app
csv_path = os.path.join(script_dir, 'survey_data.csv')

# Fetch data and create User objects
users = []
try:
    total_records = users_col.count_documents({})  # Count total documents for validation
    print(f"Total records in collection: {total_records}")
    for index, doc in enumerate(users_col.find()):
        print(f"Processing document {index + 1} of {total_records}: {doc}")  # Debug: Print raw document
        # Assuming User class accepts (age, gender, total_income, expenses)
        # Adjust if it expects name or different order
        user = User(
            doc.get('age'),
            doc.get('gender'),
            doc.get('total_income'),
            doc.get('expenses', {})
        )
        users.append(user)  # Append each new User object
        print(f"Appended User {index + 1}: age={user.age}, gender={user.gender}, total_income={user.total_income}, expenses={user.expenses}")  # Debug: Verify append
except Exception as e:
    print(f"Error fetching data: {e}")
    raise

# Validate number of users captured
print(f"Number of users captured: {len(users)}")

# Export to CSV
try:
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['age', 'gender', 'total_income', 'utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for index, user in enumerate(users):
            row = {
                'age': user.age if user.age is not None else 0,
                'gender': user.gender if user.gender is not None else '',
                'total_income': user.total_income if user.total_income is not None else 0.0,
                'utilities': user.expenses.get('utilities', 0),
                'entertainment': user.expenses.get('entertainment', 0),
                'school_fees': user.expenses.get('school_fees', 0),
                'shopping': user.expenses.get('shopping', 0),
                'healthcare': user.expenses.get('healthcare', 0)
            }
            print(f"Writing row {index + 1} of {len(users)}: {row}")  # Debug: Verify row data
            writer.writerow(row)
    print(f"Data exported to {csv_path}")
except Exception as e:
    print(f"Error writing to CSV: {e}")
    raise
finally:
    client.close()  # Ensure the client is closed to free resources