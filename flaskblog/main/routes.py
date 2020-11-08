from flask import Blueprint, request, render_template

from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).\
        paginate(per_page=4, page=page)
    # git
    return render_template('home.html', posts=posts, title='Main Home Page')


@main.route('/about')
def about():
    abouts = [
        {
            'author': 'Roy Ruach',
            'title': 'FlaskBlog home page',
            'content': 'This page was created by Roy Ruach using python and '
                       'flask',
            'date_posted': 'October 26, 2020'
        }
    ]
    return render_template('about.html', posts=abouts, title='About Page')
