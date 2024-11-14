from flask import Blueprint , render_template , request , url_for , redirect , flash
from flask_login import current_user , login_required
from .models import User , Comment , Post
from . import db

posts = Blueprint('posts',__name__)

@posts.route("/create_post",methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        post_title = request.form.get('post_title')
        post_disc = request.form.get('post_disc')


        new_post = Post(post_title=post_title , post_disc=post_disc , user_id=current_user.id )
        db.session.add(new_post)
        db.session.commit()

@posts.route("/delete_post/<int:post_id>",methods=["POST", "GET"])
def delete_post(post_id):
    if request.method == "POST":
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!", category="success")


@posts.route("/add_comment/<int:user_id>/<int:post_id>",methods=["POST","GET"])
def add_comment(user_id , post_id):
    if request.method == "POST":
        cmnt = request.form.get('cmnt')
        user = User.query.get_or_404(user_id)
        post = Post.query.get_or_404(post_id)

        new_comment = Comment(cmnt=cmnt , user_id = user.id, post_id = post.id)
        db.session.add(new_comment)
        db.session.commit()

@posts.route("/replay_comment/<int:user_id>/<int:post_id>/<int:parent_comment_id>",methods=["POST","GET"])
def replay_comment(user_id,post_id,parent_comment_id):
    if request.method == "POST":
        cmnt = request.form.get('cmnt')
        user = User.query.get_or_404(user_id)
        post = Post.query.get_or_404(post_id)
        parent_comment = Comment.query.get_or_404(parent_comment_id)

        new_replay = Comment(cmnt=cmnt , user_id=user.id ,post_id=post.id, parent_comment_id=parent_comment.id )