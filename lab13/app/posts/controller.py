import os
import secrets
from PIL import Image
from flask_login import current_user, login_required
from flask import url_for, render_template, redirect,\
    flash, current_app
from . import posts
from .form import PostForm
from .models import Post
from .. import db, App


@posts.route('/')
def index():
    all_posts = Post.query.all()
    image = url_for('static', filename='post_pics')
    return render_template('index.html', all_posts=all_posts,
                           image=image, menu=App.getMenu())


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            image = save_picture(form.image.data)
        else:
            image = 'default.png'

        post = Post(title=form.title.data,
                    text=form.text.data,
                    type=form.type.data,
                    image=image,
                    user_id=current_user.id)

        db.session.add(post)
        db.session.commit()

        flash('Post created!', category='success')

        return redirect(url_for('posts.index'))

    return render_template('create.html', form=form, menu=App.getMenu())


@posts.route('/<id>', methods=['GET', 'POST'])
def view(id):
    post = Post.query.get_or_404(id)
    image = url_for('static', filename='post_pics/' + post.image)
    return render_template('post.html', post=post,
                           menu=App.getMenu(), image=image)


@posts.route('/<id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    if current_user.id != post.user_id:
        flash('This post not related to you!', category='warning')
        return redirect(url_for('posts.view', post=post))

    form = PostForm()

    if form.validate_on_submit():
        if form.image.data:
            image = save_picture(form.image.data)
            post.image = image

        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data

        db.session.commit()

        flash('Post updated', category='success')
        return redirect(url_for('posts.view', id=post.id))

    form.title.data = post.title
    form.text.data = post.text
    form.type.data = post.type

    return render_template('update.html', form=form, menu=App.getMenu())


@posts.route('/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('posts.index'))

    flash('This post not related to you!', category='warning')
    return redirect(url_for('posts.view', id=post.id))


@posts.route('/<id>/toggle_enabled', methods=['GET', 'POST'])
def toggle_enabled(id):
    post = Post.query.get_or_404(id)
    post.is_enabled = not post.is_enabled
    db.session.commit()
    flash('Post ' + ('enabled' if post.is_enabled else 'disabled'), category='success')
    return redirect(url_for('posts.view', id=post.id))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static\\post_pics', picture_filename)
    image = Image.open(form_picture)
    image.save(picture_path)
    return picture_filename
