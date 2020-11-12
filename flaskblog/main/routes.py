from flask import Blueprint, request, render_template

from flaskblog.models import Post, User

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).\
        paginate(per_page=4, page=page)
    return render_template('home.html', posts=posts, title='RoyRuach Home',
                           num_registered=User.get_num_registered())


@main.route('/about')
def about():
    abouts = [
        {
            'author': 'Roy Ruach',
            'title': 'Blog and Reminders home page',
            'content': 'This page was created by Roy Ruach using python and '
                       'flask.\nThe site was created in assistance with Corey '
                       'Schafer Youtube flask tutorial.\nUsing this page you '
                       'can register with your email and send yourself future'
                       ' notifications via E-mail',
            'date_posted': 'October 26, 2020'
        }
    ]
    return render_template('about.html', posts=abouts, title='About Page',
                           num_registered=User.get_num_registered())


@main.route('/home/latest_posts')
def latest_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).\
        paginate(per_page=4, page=page)
    return render_template('home.html', posts=posts, title='Latest Posts',
                           num_registered=User.get_num_registered())
