from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os

app = Flask(__name__)
# Use the DATABASE_URL environment variable if it exists (Production), otherwise use sqlite (Local)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todo.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(10), default='Medium')
    date_completed = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Todo {self.id}>'
    
    @property
    def duration(self):
        if self.completed and self.date_completed and self.date_created:
            diff = self.date_completed - self.date_created
            days = diff.days
            hours = diff.seconds // 3600
            return f"{days}d {hours}h"
        return None

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_priority = request.form.get('priority', 'Medium')
        task_due_date_str = request.form.get('due_date')
        
        if not task_content:
            return redirect('/')
            
        task_due_date = None
        if task_due_date_str:
            try:
                task_due_date = datetime.strptime(task_due_date_str, '%Y-%m-%d')
            except ValueError:
                pass
            
        new_task = Todo(title=task_content, priority=task_priority, due_date=task_due_date)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.title = request.form['content']
        task.priority = request.form.get('priority', 'Medium')
        
        task_due_date_str = request.form.get('due_date')
        if task_due_date_str:
            try:
                task.due_date = datetime.strptime(task_due_date_str, '%Y-%m-%d')
            except ValueError:
                task.due_date = None
        else:
            task.due_date = None

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('edit.html', task=task)

@app.route('/update/<int:id>')
def update(id):
    task = Todo.query.get_or_404(id)

    try:
        task.completed = not task.completed
        if task.completed:
            task.date_completed = datetime.utcnow()
        else:
            task.date_completed = None
            
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating your task'

if __name__ == "__main__":
    app.run(debug=True)
