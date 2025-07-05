from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    detail = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(10), default=datetime.utcnow().strftime('%Y-%m-%d'))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'name': task.name,
        'url': task.url,
        'detail': task.detail,
        'date': task.date
    } for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = Task(
        name=data['name'],
        url=data['url'],
        detail=data['detail'],
        date=data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task added", "task": {
        "id": task.id,
        "name": task.name,
        "url": task.url,
        "detail": task.detail,
        "date": task.date
    }}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted", "task_id": task_id}), 200

@app.route('/')
def index():
    return render_template('index.html')
