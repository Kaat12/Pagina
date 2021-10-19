from flask import request, Response, Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/bd_ventas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'

db = SQLAlchemy(app)


class Cliente(db.Model):
    idCliente= db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    direccion = db.Column(db.String(80))

db.create_all()
#RUTAS DEl WEB APP---------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('index.html')
    return render_template('login.html')

@app.route('/dama')
def dama():
    return render_template('dama.html')

@app.route('/rebajas')
def rebajas():
    return render_template('rebajas.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')
#-----------CONTROL DE SESION Y CREACION DE USUARIOS-----------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            email = request.form['email']
            cliente = Cliente.query.filter_by(email=email).first()
            if cliente:
                if werkzeug.security.check_password_hash(cliente.password, request.form['password']):
                    session['logged_in'] = True
                    flash('Bienvenido!')
                    return redirect(url_for('index'))
                error = 'Contraseña incorrecta'
                return render_template('login.html', error=error)
            else:
                error = 'El usuario no existe!'
                return render_template('login.html', error=error)
        return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            email = request.form['email']
            hashed_psswd = werkzeug.security.generate_password_hash(request.form['password'], method='sha256')
            cliente = Cliente(nombre="empty", email=email, password=hashed_psswd, direccion="empty")
            db.session.add(cliente)
            db.session.commit()
            flash('Usuario registrado con exito')
            return render_template('login.html')
        return render_template('registro.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)