from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  return render_template("login.html")

@auth.route('/logout')
def logout():
  return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if len(email) < 4:
      flash('Email muito curto, necessário pelo menos 4 caracteres.', category='error')
    elif len(firstName) < 2:
      flash('Nome muito curto, necessário pelo menos 2 caracteres.', category='error')
    elif len(lastName) < 2:
      flash('Sobrenome muito curto, necessário pelo menos 2 caracteres.', category='error')
    elif password1 != password2:
      flash('As senhas precisam combinar.', category='error')
    elif len(password1) < 6:
      flash('Senha muito curta, necessário ao menos 6 caracteres.', category='error')
    else:
      flash('Conta criada com sucesso!', category='success')

  return render_template("sign_up.html")