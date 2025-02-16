from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://task_user:grizzly7@localhost/task_manager"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.String(120), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.title}>"

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

    # Clear existing tasks before adding new ones
    db.session.query(Task).delete()
    db.session.commit()

    # Add the daily tasks to the database
    tasks = [
        {"title": "Wake up", "description": "Start your day", "due_date": "07:00", "completed": False},
        {"title": "Study", "description": "Work on learning goals", "due_date": "07:30", "completed": False},
        {"title": "Mindfulness", "description": "Practice mindfulness", "due_date": "09:30", "completed": False},
        {"title": "Fitness", "description": "Workout", "due_date": "10:00", "completed": False},
        {"title": "Lunch", "description": "Time for lunch", "due_date": "12:30", "completed": False},
        {"title": "Recovery", "description": "Relaxation or meditation", "due_date": "01:00", "completed": False},
        {"title": "Family time", "description": "Spend time with family", "due_date": "01:30", "completed": False},
        {"title": "Dinner", "description": "Time for dinner", "due_date": "09:00", "completed": False},
        {"title": "Read", "description": "Read a book", "due_date": "10:00", "completed": False},
        {"title": "Gratitude", "description": "Write about things you're grateful for", "due_date": "11:00", "completed": False},
        {"title": "Sleep", "description": "Get some rest", "due_date": "12:00", "completed": False}
    ]
    
    # Adding tasks to the database
    for task in tasks:
        # Check if the task already exists
        existing_task = db.session.query(Task).filter_by(title=task['title']).first()
        if not existing_task:
            new_task = Task(title=task['title'], description=task['description'], due_date=task['due_date'], completed=task['completed'])
            db.session.add(new_task)
            db.session.commit()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    task_list = [
        {"id": task.id, "title": task.title, "description": task.description, "due_date": task.due_date, "completed": task.completed}
        for task in tasks
    ]
    return jsonify(task_list)

if __name__ == "__main__":
    app.run(debug=True)
