from datetime import datetime
from flask_mail import Message
from flaskblog import mail, executor


def async_run_reminder(reminder, user):
    print("get future from pool")
    res = executor.submit(reminder)
    print("got future")
    executor.submit(email_result, (reminder.title, user.email, res))
    print("wait for future result submitted")


def email_result(tup):
    title, email, res = tup
    print('waiting for result')
    result = res.result()
    print(f'sending mail to {email}')

    msg = Message('Here is the result of your reminder',
                  sender='REMINDER@royruach.com',
                  recipients=[email])
    msg.body = f'''here is the result of reminder {title}:
{result}
run ended at {datetime.utcnow()}
Thanks!
'''
    mail.send(msg)
    print(f'mail was sent to {email}')
