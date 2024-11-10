# Import necessary modules from Flask and custom models
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

# Flask app configuration
app = Flask(__name__)
# Configure PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# Initialize debug toolbar and database
toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

# Homepage route - shows 5 most recent posts
@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

##############################################################################
# User Routes
##############################################################################

# User listing and management routes
@app.route('/users')
def users_index():
    """Show a page with info on all users"""
    # Order users by last name, then first name
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

# User creation routes (GET shows form, POST handles submission)
@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""
    return render_template('users/new.html')

@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""
    # Create new user from form data
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    # Add to database and notify user
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")
    return redirect("/users")

##############################################################################
# Post Routes
##############################################################################

# Post creation routes
@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Show a form to create a new post for a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post"""
    user = User.query.get_or_404(user_id)
    # Create new post associated with user
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    
    # Add to database and notify user
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")

# Post viewing and editing routes
@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a specific post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle post updates"""
    post = Post.query.get_or_404(post_id)
    # Update post with new data
    post.title = request.form['title']
    post.content = request.form['content']
    
    # Save changes and notify user
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")
    return redirect(f"/users/{post.user_id}")