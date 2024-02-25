from flask import Flask, redirect, render_template, request, session
from models import db, connect_db, Users
from forms import RegisterForm
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
        session['user_id'] = user.id
        
        return redirect('/users/<username>')
    else:
        return render_template('register.html', form=form)
    
@app.route('/users/<username>')
def user_dashboard(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = Users.query.get_or_404(session['user_id'])
    return render_template('/users/dashboard.html', user=user)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()