from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
      email = request.form.get('email')
      password = request.form.get('password')

      user = User.query.filter_by(email=email).first()
      if user:
        if check_password_hash(user.password, password):
          flash('Login feito com sucesso!', category='success')
          login_user(user, remember=True)
          return redirect(url_for('views.home'))
        else:
          flash('Senha incorreta, tente novamente.', category='error')
      else:
        flash('Email não existe', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já existente.', category='error')
        elif len(email) < 4:
            flash('Email muito curto, necessário pelo menos 4 caracteres.',
                  category='error')
        elif len(firstName) < 2:
            flash('Nome muito curto, necessário pelo menos 2 caracteres.',
                  category='error')
        elif len(lastName) < 2:
            flash('Sobrenome muito curto, necessário pelo menos 2 caracteres.',
                  category='error')
        elif password1 != password2:
            flash('As senhas precisam combinar.',
                  category='error')
        elif len(password1) < 6:
            flash('Senha muito curta, necessário ao menos 6 caracteres.',
                  category='error')
        else:
            new_user = User(email=email,
                            first_name=firstName,
                            last_name=lastName,
                            password=generate_password_hash(password1, method='sha256')
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(user)

            flash('Conta criada com sucesso!', category='success')
            return redirect(url_for('views.home'), user=current_user)

    return render_template("sign_up.html", user=current_user)
