from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from app.forms import LoginForm, SignUpForm
from flask import render_template, flash, redirect, url_for
from app.firestore_service import get_user, user_put
from ..models import UserData, UserModel


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        user_id = login_form.userid.data
        password = login_form.password.data

        user_doc = get_user(user_id)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if check_password_hash(password_from_db, password):
                user_data = UserData(user_id, user_doc.to_dict()['username'], password)
                user = UserModel(user_data)
                login_user(user)

                flash('Bienvenido de nuevo', 'success')

                redirect(url_for('hello'))
            else:
                flash('Los datos ingresados no coinciden', 'danger')
        else:
            flash('El usuario no existe', 'warning')

        return redirect(url_for('index'))
    return render_template('login.html', **context)


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        userid = signup_form.userid.data
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(userid)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(userid, username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido!', 'success')
            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe!', 'warning')

    return render_template('signup.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
