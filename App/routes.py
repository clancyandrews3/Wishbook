########################################
# This file is designed to add backend functionality
# to the website through page routing and functionality
#
#
########################################

import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from App import app, db
from App.forms import LoginForm, RegistrationForm
from App.models import User



@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    App routing and functionality for the 
    homepage

    Will be routed to from login and home button
    on the navigation panel

    This is the default landing page for the website
    as a whole
    """
    return render_template('index.html', title='Home')



@app.route('/login', methods = ['GET', 'POST'])
def login():
    """
    App routing and functionality for
    login

    Routed any page if user is not authenticated,
    uses flask-login package to login the user
    from the session

    Returns:
    Redirection to the homepage or any page they were
    trying to access prior for login prompt
    """

    # If user is already authenticated,
    # will take them back to the homepage
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))

        # Checks for bad password
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password.')
            return redirect(url_for('login'))
        
        login_user(user, remember = form.remember_me.data)

        # Redirects back to the page user was trying to reach
        # before they were logged in, otherwise, homepage
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title = 'Sign In', form = form)



@app.route('/logout')
def logout():
    """
    App routing and functionality for
    logout

    Routed from the navigation panel,
    uses flask-login package to logout the user
    from the session

    Returns:
    Redirection to the homepage; however,
    they will be reprompted to login from there
    """

    logout_user()

    return redirect(url_for('index'))



@app.route('/register', methods = ['GET', 'POST'])
def register():
    """
    App routing and functionality
    for the registration page

    User's will have the option to register from
    the login page, and will redirect here when the 
    button is selected

    Returns:
    Once the user has registered, they will be 
    redirected to the login page to login with
    their new credentials
    """

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    username=form.username.data, 
                    email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Congratulations, you have now registered!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title = 'Register', form = form)