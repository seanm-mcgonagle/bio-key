from flask import Flask, request, jsonify
import db

app = Flask(__name__)

@app.route("/healthz", methods=["GET"])
def health_check():
    """
    Basic health check
    """
    return jsonify({"message": "Healthcheck pass"}), 200

@app.route("/user", methods=["POST"])
def create_user():
    """
    Create a new user in the database.
    Requires username, password, and email in the request body.
    """    
    # Get the request data, check presense and validate it
    data = request.get_json()
    if not data:
        return jsonify({"message": "Bad Request"}), 400
    try:
        username = data["username"]
        password = data["password"]
        email = data["email"]
    except KeyError:
        return jsonify({"message": "Bad Request"}), 400
    if not isinstance(username, str) or not isinstance(password, str) or not isinstance(email, str):
        return jsonify({"message": "Bad Request"}), 400

    # Check if user already exists, return 400 if it does
    existing_user = db.get_username(username)
    if existing_user:
        return jsonify({"message": "User already exists"}), 400
    
    # Check if email is taken
    existing_email = db.get_email(email)
    if existing_email:
        return jsonify({"message": "Email already exists"}), 400

    # Insert user into the database
    db.create_user(username, password, email)

    # Check if the user was created successfully
    new_user = db.get_user(username)
    if not new_user:
        return jsonify({"message": "User creation failed"}), 400
    if new_user[0] != username and new_user[1] != password and new_user[2] != email:
        return jsonify({"message": "User creation failed"}), 400
    else:
        return jsonify({"message": "User created successfully"}), 201

@app.route("/user", methods=["GET"])
def get_user():
    """
    Get user details from the database.
    Requires username in the request body to match an existing user in the database.
    Having an API endopint like this is obviously not a good practice, 
    but it's just for the sake of the exercise.
    """
    # get the request data, check if it's present
    data = request.get_json()
    if not data:
        return jsonify({"message": "Bad Request"}), 400

    # Extract user details from the request data
    try:
        username = data["username"]
    except KeyError:
        return jsonify({"message": "Bad Request"}), 400
    if not isinstance(username, str):
        return jsonify({"message": "Bad Request"}), 400

    # Get user details from the database
    user = db.get_user(username)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Extract user details
    username = user[0]
    password = user[1]
    email = user[2]

    # Return user details as JSON
    return jsonify({"username": username, "password": password, "email": email}), 200

@app.route("/user", methods=["PUT"])
def update_user():
    """
    Update email and password for particular username.
    Requires username, new password, and new email in the request body.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Bad Request"}), 400

    # Extract user details from the request data
    try:
        username = data["username"]
        password = data["password"]
        email = data["email"]
    except KeyError:
        return jsonify({"message": "Bad Request"}), 400
    if not isinstance(username, str) or not isinstance(password, str) or not isinstance(email, str):
        return jsonify({"message": "Bad Request"}), 400
    
    # If user doesn't exists, return 404, otherwise update the user
    existing_user = db.get_username(username)
    if not existing_user:
        return jsonify({"message": "User not found"}), 404
    db.update_user(username, password, email)

    # User sucessfully updated if password and email from the request
    # match the ones in the database
    user = db.get_user(username)
    if not user:
        return jsonify({"message": "User not found"}), 404
    password_db = user[1]
    email_db = user[2]
    if password_db != password or email_db != email:
        return jsonify({"message": "User update failed"}), 400
    else:
        return jsonify({"message": "User updated successfully"}), 200

@app.route("/user", methods=["DELETE"])
def delete_user():
    """
    Delete a user from the database.
    Requires username in the request body to match an existing user in the database.
    This is also bad practice, but it's just for the sake of the exercise.
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Bad Request"}), 400

    # Extract user details from the request data
    try:
        username = data["username"]
    except KeyError:
        return jsonify({"message": "Bad Request"}), 400
    if not isinstance(username, str):
        return jsonify({"message": "Bad Request"}), 400

    # Return 404 if username is not found
    existing_user = db.get_username(username)
    if not existing_user:
        return jsonify({"message": "User not found"}), 404

    # Delete user from the database
    db.delete_user(username)

    # Check if the user was deleted successfully
    if db.get_user(username):
        return jsonify({"message": "User deletion failed"}), 400
    else:
        return jsonify({"message": "User deleted successfully"}), 200

# Note: In a production environment, you would typically use a WSGI server like Gunicorn or Nginx
# and turn debug mode off.
if __name__ == "__main__":
    db.create_table()
    app.run(host="0.0.0.0", port=5001, debug=True)
