from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Database connection configuration
db_config = {
    'user': 'root',             # Use your MySQL username (default is "root")
    'password': '',             # Use your MySQL password (often blank for XAMPP)
    'host': 'localhost',
    'database': 'user_management'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Serve the frontend
@app.route('/')
def home():
    return render_template('index.html')  # Serves the HTML file

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# Get a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    if not name or not email or not age:
        return jsonify({'error': 'Missing data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
        conn.commit()
        user_id = cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500

    cursor.close()
    conn.close()
    return jsonify({'id': user_id, 'name': name, 'email': email, 'age': age}), 201

# Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET name = %s, email = %s, age = %s WHERE id = %s",
            (name, email, age, user_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
    except mysql.connector.Error as err:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(err)}), 500

    cursor.close()
    conn.close()
    return jsonify({'id': user_id, 'name': name, 'email': email, 'age': age})

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    cursor.close()
    conn.close()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Allows access from ngrok
