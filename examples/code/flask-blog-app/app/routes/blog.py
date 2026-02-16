"""Blog routes blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.database import db
from app.models import Post
from app.forms import PostForm

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """
    Display list of blog posts with pagination.

    Query Parameters:
        page: Page number (default: 1)
        per_page: Posts per page (default: 10)

    Returns:
        Rendered index template with posts
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    posts = db.get_all(page=page, per_page=per_page)
    total_posts = db.count()
    total_pages = (total_posts + per_page - 1) // per_page

    return render_template(
        'index.html',
        posts=posts,
        page=page,
        total_pages=total_pages,
        total_posts=total_posts
    )


@blog_bp.route('/post/<int:post_id>')
def post_detail(post_id: int):
    """
    Display details of a specific post.

    Args:
        post_id: The post ID

    Returns:
        Rendered post detail template or 404 if not found
    """
    post = db.get_by_id(post_id)
    if post is None:
        flash('Post no encontrado', 'error')
        return redirect(url_for('blog.index'))

    return render_template('post_detail.html', post=post)


@blog_bp.route('/post/new', methods=['GET', 'POST'])
def post_create():
    """
    Create a new blog post.

    GET: Display creation form
    POST: Process form and create post

    Returns:
        Rendered form or redirect to post detail
    """
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data
        )
        created_post = db.create(post)
        flash('Post creado exitosamente', 'success')
        return redirect(url_for('blog.post_detail', post_id=created_post.id))

    return render_template('post_form.html', form=form, mode='create')


@blog_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def post_edit(post_id: int):
    """
    Edit an existing blog post.

    Args:
        post_id: The post ID

    GET: Display edit form with current data
    POST: Process form and update post

    Returns:
        Rendered form or redirect to post detail
    """
    post = db.get_by_id(post_id)
    if post is None:
        flash('Post no encontrado', 'error')
        return redirect(url_for('blog.index'))

    form = PostForm(obj=post)

    if form.validate_on_submit():
        updated_post = Post(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data
        )
        db.update(post_id, updated_post)
        flash('Post actualizado exitosamente', 'success')
        return redirect(url_for('blog.post_detail', post_id=post_id))

    return render_template('post_form.html', form=form, mode='edit', post=post)


@blog_bp.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def post_delete(post_id: int):
    """
    Delete a blog post with confirmation.

    Args:
        post_id: The post ID

    GET: Display confirmation page
    POST: Delete post and redirect to index

    Returns:
        Rendered confirmation or redirect to index
    """
    post = db.get_by_id(post_id)
    if post is None:
        flash('Post no encontrado', 'error')
        return redirect(url_for('blog.index'))

    if request.method == 'POST':
        db.delete(post_id)
        flash('Post eliminado exitosamente', 'success')
        return redirect(url_for('blog.index'))

    return render_template('confirm_delete.html', post=post)
