from flask import Blueprint , render_template , request , url_for , flash , redirect
from . import db
from .models import Task

tasks = Blueprint("tasks",__name__)


@tasks.route('/tasks', methods=["POST" , "GET"])
def task():
    if request.method == ('POST'):
        task = request.form.get('task')

    render_template('tasks.html')