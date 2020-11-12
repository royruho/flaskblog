from flask import Blueprint, flash, redirect, url_for, render_template, abort, \
    request
from flask_login import login_required, current_user

from flaskblog import db
from flaskblog.models import Reminder, User
from flaskblog.remainders.forms import ReminderForm

reminders = Blueprint('remainders', __name__)


@reminders.route('/reminder/remainders')
@login_required
def user_reminders():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    reminders = Reminder.query.filter_by(author=user).order_by(
        Reminder.date_created.desc()).paginate(per_page=5, page=page)
    return render_template('user_reminders.html', reminders=reminders, user=user,
                           num_registered=User.get_num_registered())


@reminders.route('/reminder/new', methods=['GET', 'POST'])
@login_required
def new_reminder():
    form = ReminderForm()
    if form.validate_on_submit():
        reminder_object = Reminder(title=form.title.data,
                               duration_sec=form.duration_sec.data,
                               author=current_user)
        db.session.add(reminder_object)
        db.session.commit()
        flash('reminder was created', 'success')
        return redirect(url_for('remainders.reminder',
                                reminder_id=reminder_object.id))
    return render_template('create_reminder.html', title='New reminder',
                           form=form, legend='New reminder',
                           num_registered=User.get_num_registered())


@reminders.route('/reminder/<int:reminder_id>', methods=['GET', 'POST'])
def reminder(reminder_id):
    reminder_object = Reminder.query.get_or_404(reminder_id)
    return render_template('reminder.html', title=reminder_object.title,
                           reminder=reminder_object,
                           num_registered=User.get_num_registered())


@reminders.route('/reminder/<int:reminder_id>/update', methods=['GET', 'POST'])
@login_required
def update_reminder(reminder_id):
    reminder_object = Reminder.query.get_or_404(reminder_id)
    if reminder_object.author != current_user:
        abort(403)
    form = ReminderForm()
    if form.validate_on_submit():
        reminder_object.title = form.title.data
        reminder_object.duration_sec = form.duration_sec.data
        db.session.commit()
        flash('reminder was updated', 'success')
        return redirect(url_for('remainders.reminder', reminder_id=reminder_object.id))
    elif request.method == 'GET':
        form.title.data = reminder_object.title
        form.duration_sec.data = reminder_object.duration_sec
    return render_template('create_reminder.html', title='Update reminder',
                           form=form, legend='Update reminder',
                           num_registered=User.get_num_registered())


@reminders.route('/reminder/<int:reminder_id>/delete', methods=['POST'])
@login_required
def delete_reminder(reminder_id):
    reminder_object = Reminder.query.get_or_404(reminder_id)
    if reminder_object.author != current_user:
        abort(403)
    db.session.delete(reminder_object)
    db.session.commit()
    flash('reminder was deleted', category="success")
    return redirect(url_for('remainders.user_reminders'))


@reminders.route('/reminder/<int:reminder_id>/run', methods=['POST'])
@login_required
def run_reminder(reminder_id):
    reminder_object = Reminder.query.get_or_404(reminder_id)
    if reminder_object.author != current_user:
        abort(403)
    if reminder_object.set_reminder():
        db.session.commit()
        flash('Reminder submitted. You will receive an email in the '
              'near future',
              category="success")
    else:
        flash('reminder already sent', category="warning")

    return redirect(url_for('remainders.user_reminders'))
