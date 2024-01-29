from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

                                                                                # signup

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data.title()
            last_name = form.last_name.data.title()
            favorite_liquor = form.favorite_liquor.data
            print(email, first_name, last_name, password)

            user = User(email, first_name, last_name, favorite_liquor, password = password)

            db.session.add(user)
            db.session.commit()



            flash(f'You have successfully created a user account {first_name} {last_name}', 'User-created')
            return redirect(url_for('auth.signin'))
        
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)

                                                                                #signin

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('User identified', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('You do not have access to this content.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form)

                                                                                #Logout

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))