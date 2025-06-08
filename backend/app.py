from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
from openai_utils import get_priority_and_quadrant  # Import GPT helper

app = Flask(__name__)
CORS(app)

# MySQL connection string (your config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:FOMM04122004@localhost/task'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    quadrant = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='To Do')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "quadrant": self.quadrant,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

@app.route('/')
def index():
    return jsonify({"message": "AI Task Prioritization API is running"})

@app.route('/add-task', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        deadline_str = data.get('deadline')

        if not title or not description or not deadline_str:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

        # Call OpenAI GPT for priority & quadrant
        gpt_response = get_priority_and_quadrant(title, description, deadline_str)
        gpt_data = json.loads(gpt_response)

        priority = gpt_data.get('priority', 'Medium')
        quadrant = gpt_data.get('quadrant', 'Important, Not Urgent')

        new_task = Task(
            title=title,
            description=description,
            deadline=deadline,
            priority=priority,
            quadrant=quadrant
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"success": True, "task": new_task.to_dict()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
# Ensure the database is created before running the app