from flask import request, Response, Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import werkzeug.security 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/bd_ventas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'

db = SQLAlchemy(app)

class Cliente(db.Model):
    idCliente= db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(140))
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

@app.route('/contacto', methods=['GET', 'POST'])
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
                db.session.add(cliente)
                if werkzeug.security.check_password_hash(cliente.password, request.form['password']):
                    session['logged_in'] = True
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
            if Cliente.query.filter_by(email=email).first():
                error = 'Este email ya esta registrado!'
                return render_template('registro.html', error=error)
            else:
                db.session.add(Cliente(nombre="empty", email=email, password=werkzeug.security.generate_password_hash(request.form['password'], method='sha256'), direccion="empty"))
                db.session.commit()
                flash('Usuario registrado con exito')
                return render_template('login.html')
        return render_template('registro.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

#-------------------codigo para PWA---------------------------
@app.route('/offline')
def offline():
    return app.send_static_file('offline.html')

@app.route('/serviceWorker.js')
def sw():
    return app.send_static_file('serviceWorker.js')

#-------------------inicializar servidor------------------------------
if __name__ == '__main__':
    app.run()