from flask import Flask, redirect, render_template, request, session
from models import db, connect_db, Users, Feedback
from forms import FeedbackForm, LoginForm, RegisterForm
from werkzeug.exceptions import Unauthorized
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhhh. its a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = True

connect_db(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(f'/users/{session["username"]}')
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Get all form data and validate
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        # push validated data to database
        user = Users.register(username, password, email, first_name, last_name)
        
        db.session.commit()
        session['username'] = user.username
        
        return redirect('/users/<username>')
    else:
        return render_template('register.html', form=form)
    
@app.route('/users/<username>')
def user_dashboard(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = Users.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(username=username).all()
    return render_template('/users/dashboard.html', user=user , feedback=feedback)

@app.route('/login', methods=['GET', 'POST'])   
def login():
    if "username" in session:
        return redirect(f'/users/{session["username"]}')
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = Users.authenticate(username, password)
        
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('/users/login.html', form=form)
    return render_template('/users/login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

# ***************FEEDBACK ROUTES****************

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    return render_template('/feedback/add_feedback.html', form=form) 

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])  
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    return render_template('/feedback/update_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=['GET', 'POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{session["username"]}')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()