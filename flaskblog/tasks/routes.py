from flask import Blueprint, flash, redirect, url_for, render_template, abort, \
    request
from flask_login import login_required, current_user

from flaskblog import db
from flaskblog.models import Task, User
from flaskblog.tasks.forms import TaskForm

tasks = Blueprint('tasks', __name__)


@tasks.route('/task/tasks')
@login_required
def user_tasks():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    tasks = Task.query.filter_by(author=user).order_by(
        Task.date_created.desc()).paginate(per_page=5, page=page)
    return render_template('user_tasks.html', tasks=tasks, user=user,
                           num_registered=User.get_num_registered())


@tasks.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task_object = Task(title=form.title.data,
                           duration_sec=form.duration_sec.data,
                           author=current_user)
        db.session.add(task_object)
        db.session.commit()
        flash('Task was created', 'success')
        return redirect(url_for('tasks.user_tasks'))
    return render_template('create_task.html', title='New Task',
                           form=form, legend='New Task',
                           num_registered=User.get_num_registered())


@tasks.route('/task/<int:task_id>', methods=['GET', 'POST'])
def task(task_id):
    task_object = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task_object.title,
                           task=task_object,
                           num_registered=User.get_num_registered())


@tasks.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task_object = Task.query.get_or_404(task_id)
    if task_object.author != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task_object.title = form.title.data
        task_object.duration_sec = form.duration_sec.data
        db.session.commit()
        flash('Task was updated', 'success')
        return redirect(url_for('tasks.task', task_id=task_object.id))
    elif request.method == 'GET':
        form.title.data = task_object.title
        form.duration_sec.data = task_object.duration_sec
    return render_template('create_task.html', title='Update task',
                           form=form, legend='Update task',
                           num_registered=User.get_num_registered())


@tasks.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task_object = Task.query.get_or_404(task_id)
    if task_object.author != current_user:
        abort(403)
    db.session.delete(task_object)
    db.session.commit()
    flash('Task was deleted', category="success")
    return redirect(url_for('tasks.user_tasks'))


@tasks.route('/task/<int:task_id>/run', methods=['POST'])
@login_required
def run_task(task_id):
    task_object = Task.query.get_or_404(task_id)
    if task_object.author != current_user:
        abort(403)
    if task_object.run_task():
        db.session.commit()
        flash('Task submitted to run', category="success")
    else:
        flash('task already run', category="warning")

    return redirect(url_for('tasks.user_tasks'))
