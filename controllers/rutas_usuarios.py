from crypt import methods
from __init__ import app,bcrypt
from flask import render_template,redirect,request,session,flash
from models.usuario import Usuario

@app.route('/')
def inicio():
    return render_template('home.html')

@app.route('/process1',methods=['POST'])
def process1():
    if not Usuario.validacion(request.form):
        return redirect('/')
    if request.form['password'] == request.form['confirm_password']:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
    else:
        flash('Las contraseñas no coinciden','error')
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    Usuario.save(data)
    flash('Usuario creado correctamente','success')
    return redirect('/')

@app.route('/process2',methods=['POST'])
def process2():
    data = {
        "email": request.form['email']
    }
    user_data = Usuario.get_user_by_email(data)
    if not user_data:
        flash('Usuario invalido','error')
        return redirect('/')
    if not bcrypt.check_password_hash(user_data[0].password,request.form['password']):
        flash('Email/Contraseña invalidos','error')
        return redirect('/')
    session['user_id'] = user_data[0].id
    return redirect('/inicio_sesion')

@app.route('/inicio_sesion')
def inicio_sesion():
    if not 'user_id' in session:
        flash('Debes primero iniciar sesion','error')
        return redirect('/')
    flash('Sesion iniciada','success')
    return render_template('user.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    flash('Sesion cerrada','info')
    return redirect('/')
    