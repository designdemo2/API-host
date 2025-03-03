from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace with your actual MongoDB connection string
MONGO_URI = "mongodb+srv://spello:spello100@spellodb.8zvmy.mongodb.net/?retryWrites=true&w=majority&appName=spelloDB&ssl=true&ssl_cert_reqs=CERT_NONE"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["spello_database"]  # Replace with your database name
collection = db["sp1"]  # Replace with your collection name


@app.route("/")
def home():
    return jsonify({"message": "Connected to MongoDB successfully!"})


# Route to store user details in the database
@app.route("/store_user", methods=["POST"])
def store_user():
    data = request.json

    # Validate required fields
    required_fields = ["name", "email", "age", "gender"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields (name, email, age, gender) are required"}), 400

    user = {
        "name": data["name"],
        "email": data["email"],
        "age": data["age"],
        "gender": data["gender"]
    }

    # Insert user data into the database
    result = collection.insert_one(user)

    # Convert ObjectId to string for JSON serialization
    user_response = user.copy()
    user_response["_id"] = str(result.inserted_id)

    return jsonify({"message": "User data stored successfully!", "user": user_response})


# Route to get all stored users from the database
@app.route("/get_users", methods=["GET"])
def get_users():
    # Retrieve all users from the database
    users = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's default "_id" field
    return jsonify({"users": users})


# Get one user based on email
@app.route("/get_user", methods=["GET"])
def get_user():
    email = request.args.get("email")  # Get email from query parameters

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Find user by email, exclude MongoDB "_id" field from response
    user = collection.find_one({"email": email}, {"_id": 0})

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)