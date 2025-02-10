from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://task_user:grizzly7@localhost/task_manager"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Create the database tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.String(120), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.title}>"
