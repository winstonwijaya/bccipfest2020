from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, Participant, Storage

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User( username=form.username.data,
                     password=form.password.data)

        # add user to the database
        db.session.add(user)
        db.session.commit()

        participant = Participant(partname=form.username.data,
                                  fcd = 100000.0, usd=0.0, sar=0.0, rub=0.0, yen=0.0)
        db.session.add(participant)
        db.session.commit()

        storage = Storage(storown=form.username.data,
                          stornum=1,
                          current_capacity=0)
        db.session.add(storage)
        db.session.commit()

        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

# Edit the login view to redirect to the admin dashboard if user is an admin

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log employee in
            login_user(user)
            # redirect to the appropriate dashboard page
            if user.is_admin:
                users = User.query.all()
                return redirect(url_for('home.admin_dashboard'))
            else:

                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))