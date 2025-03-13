from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_session import Session
from datetime import timedelta
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow all domains to access API and Configure CORS to allow credentials

app.config["SESSION_TYPE"] = "filesystem"  # Stores sessions in the server
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)  # Set session expiry  
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
Session(app)

# Secret key for session management
app.config["SECRET_KEY"] = "your_secret_key_here"

# PostgreSQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://task_user:grizzly7@localhost/task_manager"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.String(120), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    #User accounts
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # Nullable for shared tasks
    user = db.relationship("User", backref=db.backref("tasks", lazy=True))

    def __repr__(self):
        return f"<Task {self.title}>"

# Default tasks
DEFAULT_TASKS = [
    {"title": "Wake up", "description": "Start your day", "due_date": "07:00"},
    {"title": "Study", "description": "Work on learning goals", "due_date": "07:30"},
    {"title": "Mindfulness", "description": "Practice mindfulness", "due_date": "09:30"},
    {"title": "Fitness", "description": "Workout", "due_date": "10:00"},
    {"title": "Lunch", "description": "Time for lunch", "due_date": "12:30"},
    {"title": "Recovery", "description": "Relaxation or meditation", "due_date": "01:00"},
    {"title": "Family time", "description": "Spend time with family", "due_date": "01:30"},
    {"title": "Dinner", "description": "Time for dinner", "due_date": "09:00"},
    {"title": "Read", "description": "Read a book", "due_date": "10:00"},
    {"title": "Gratitude", "description": "Write about things you're grateful for", "due_date": "11:00"},
    {"title": "Sleep", "description": "Get some rest", "due_date": "12:00"},
]

# ------------------------ User Authentication Routes -------------------
@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Log the incoming data for debugging
    print(f"Registering user: username={username}, email={email}, password={password}")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    
    # Check if email is already taken
    print(f"Checking if email exists: {email}")
    existing_user = User.query.filter_by(email=email.lower()).first()
    if existing_user:
        print(f"Email already exists: {email}")  # Debug log for existing user
        return jsonify({"error": "Email already in use"}), 400
    
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    print(f"Hashed Password: {hashed_password}")  # Debug log to see hashed password
    new_user = User(username=username, email=email.lower(), password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    print(f"User {username} successfully registered with email: {email}")  # Debug log for successful registration

    return jsonify({"message": "User registered succesfully"}), 201

# Login User
@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email").lower()
    password = data.get("password")

    print(f"Attempting login with email: {email}")  # Debug log for login attempt

    user = User.query.filter_by(email=email.lower()).first()
    
    if not user:
        print(f"User not found for email: {email}")  # Debug log for user not found
        return jsonify({"error": "Invalid credentials"}), 401

    # Check if password is correct
    if not check_password_hash(user.password, password):
        print(f"Invalid password for user: {email}")  # Debug log for incorrect password
        return jsonify({"error": "Invalid credentials"}), 401
    
    session["user_id"] = user.id #Store user session
    print(f"User {user.username} logged in successfully with email: {email}")  # Debug log for successful login

    return jsonify({
        "message": "Logged in successfully",
        "user_id": user.id,
        "username": user.username
    })

# Logout User
@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id", None) # Remove user session
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/check-session", methods=["GET"])
def check_session():
    if "user_id" in session:
        return jsonify({"user_id": session["user_id"]}), 200
    return jsonify({"message": "Not logged in"}), 200

# --------------------- Task Management Routes ------------------------

@app.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = session.get("user_id")

    if user_id:
        tasks = Task.query.filter((Task.user_id == user_id) | (Task.user_id.is_(None))).all()
    else:
        tasks = Task.query.filter(Task.user_id.is_(None)).all()  # Show only default tasks

    print(f"Fetched {len(tasks)} tasks for user_id: {user_id}")  # Debug log for tasks fetched

    task_list = [
        {"id": task.id, "title": task.title, "description": task.description, "due_date": task.due_date, "completed": task.completed, "user_id": task.user_id}
        for task in tasks
    ]
    return jsonify(task_list)

@app.route("/tasks", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    due_date = data.get("due_date", "")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(title=title, description=description, due_date=due_date, completed=False, user_id=session["user_id"])
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task added successfully", "id": new_task.id})

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    print(f"Session user_id: {session.get('user_id')}")
    # Check if session user_id is correctly set.
    user_id = session.get("user_id")

    # Prevent modifications if the user is not logged in
    if not user_id:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    # Fetch the task that belongs to the logged-in user
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Task not found or unauthorized"}), 404

    # Get data from the request
    data = request.get_json()

    # Validate required fields
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Update only the fields provided in the request
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.due_date = data.get("due_date", task.due_date)
    task.completed = data.get("completed", task.completed)

    # Save changes to the database
    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date,
        "completed": task.completed
    })


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    user_id = session.get("user_id")

    # Prevent deletion if the user is not logged in
    if not user_id:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    # Allow deletion only if the task belongs to the logged-in user
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Task not found or unauthorized"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"})

# ------------------------ Helper Functions --------------------------
def add_default_tasks(user_id):
    existing_tasks = Task.query.filter_by(user_id=user_id).all()
    if not existing_tasks:
        for task in DEFAULT_TASKS:
            new_task = Task(
                title=task["title"],
                description=task["description"],
                due_date=task["due_date"],
                user_id=user_id,
                completed=False
            )
            db.session.add(new_task)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
