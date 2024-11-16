from flask import Blueprint , render_template , request , url_for , flash , redirect
from . import db
from .models import Task , User
from flask_login import current_user , login_required

tasks = Blueprint("tasks",__name__)


@tasks.route('/tasks', methods=["POST" , "GET"])
@login_required
def task():
    if request.method == ('POST'):
        task = request.form.get('task')

        
        new_task = Task(task_text=task, status="In Progress" , user_id = current_user.id)


        db.session.add(new_task)
        db.session.commit()
        flash("Task Added", category='success')
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('todolist.html', tasks=user_tasks)

@tasks.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    if request.method == "POST":
        task = Task.query.get_or_404(task_id)
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()
            flash("Task Deleted", category='success')
        return redirect(url_for('tasks.task'))
    
@tasks.route('/complete_task/<int:task_id>', methods=["POST","GET"])
@login_required
def complete_task(task_id):
    if request.method == "POST":
        task = Task.query.get_or_404(task_id)
        if task.user_id == current_user.id:
            task.status = 'Complete'
            db.session.commit()
            flash("Task Completed", category='success')
        return redirect(url_for('tasks.task'))