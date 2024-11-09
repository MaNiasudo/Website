from flask import Blueprint , render_template

tasks = Blueprint("tasks",__name__)


@tasks.route('/tasks')
def task():
    render_template('tasks.html')