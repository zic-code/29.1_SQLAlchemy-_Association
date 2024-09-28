from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User, Post


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY']='JISOO'
debug = DebugToolbarExtension(app)

#set database
connect_db(app)
db.create_all()

#Basic setting
#####################################################################
@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    # posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    # return render_template("posts/homepage.html", posts=posts)
    return redirect('/users')

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

# Users List Page
#####################################################################
@app.route('/users',methods=['GET'])
def list():

  """"Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form. """
  users= User.query.all()

  return render_template('users/list.html',users = users)

@app.route('/users/new',methods=['GET'])
def add_button():
  """Link to the addform"""
  return render_template('users/newUser.html')
  
@app.route('/users/new',methods=['POST'])
def addUser():
  """Show an add form for users"""
  first_name= request.form.get("first_name")
  last_name= request.form.get("last_name")
  image_url = request.form.get("image_url")

  if not image_url:
      image_url = 'https://blog.kakaocdn.net/dn/bCXLP7/btrQuNirLbt/N30EKpk07InXpbReKWzde1/img.png'

  new_user = User(first_name=first_name,last_name=last_name, image_url=image_url)
  
  db.session.add(new_user)
  db.session.commit()

  return redirect('/users')

#User Detail page
#####################################################################  
@app.route('/users/<int:user_id>',methods=['GET'])
def detail(user_id):
  user= User.query.get_or_404(user_id)
  posts=Post.query.filter_by(user_id = user_id).all()
  return render_template('users/details.html', user=user, posts=posts)
  
@app.route('/users/<int:user_id>/edit',methods=['GET'])
def edit_page(user_id):
  user= User.query.get_or_404(user_id)
  return render_template('users/edit.html',user=user)


#User Detail Edit Page
#####################################################################
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form.get("user.first_name","").strip()
    user.last_name = request.form.get("last_name","").strip()
    
    image_url = request.form.get("image_url")  
    if not image_url:
        image_url = 'https://blog.kakaocdn.net/dn/bCXLP7/btrQuNirLbt/N30EKpk07InXpbReKWzde1/img.png'

    user.image_url = image_url  

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete',methods=['POST'])

def delete_user(user_id):
    """Delete User from list"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

#Post

#################################################################
@app.route('/users/<int:user_id>/posts/new',methods=["GET"])
def post_form(user_id):
  """ Show form to add a post for that user."""
  user = User.query.get_or_404(user_id)    
  return render_template('post/post.html',user = user)

@app.route('/users/<int:user_id>/posts/new',methods=["POST"])
def create_post(user_id):
  """Handle add form; add post and redirect to the user detail page."""
  user = User.query.get_or_404(user_id)
  new_post = Post(title=request.form.get('title'),
                    content=request.form.get('content'),
                    user_id=user.id)
  db.session.add(new_post)
  db.session.commit()
  return redirect(f'/users/{user_id}')

@app.route('/post/<int:post_id>')
def post_detail(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post/post_detail.html',post= post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")
    return redirect(f"/users/{post.user_id}")

if __name__ == "__main__":
    app.run(debug=True)
  