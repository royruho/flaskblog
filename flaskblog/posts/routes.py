from flask import Blueprint, flash, redirect, url_for, render_template, abort, \
    request
from flask_login import login_required, current_user

from flaskblog import db
from flaskblog.models import Post, User
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, content=post_form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post was created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=post_form, legend='New Post',
                           num_registered=User.get_num_registered())


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post_object = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post_object.title,
                           post=post_object,
                           num_registered=User.get_num_registered())


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post_object = Post.query.get_or_404(post_id)
    if post_object.author != current_user:
        abort(403)
    post_form = PostForm()
    if post_form.validate_on_submit():
        post_object.title = post_form.title.data
        post_object.content = post_form.content.data
        db.session.commit()
        flash('Post was updated', 'success')
        return redirect(url_for('posts.post', post_id=post_object.id))
    elif request.method == 'GET':
        post_form.title.data = post_object.title
        post_form.content.data = post_object.content
    return render_template('create_post.html', title='Update Post',
                           form=post_form, legend='Update Post',
                           num_registered=User.get_num_registered())


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post_object = Post.query.get_or_404(post_id)
    if post_object.author != current_user:
        abort(403)
    db.session.delete(post_object)
    db.session.commit()
    flash('Post was deleted', category="success")
    return redirect(url_for('main.home'))