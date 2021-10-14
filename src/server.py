from flask import request, Response, Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/bd_ventas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'

db = SQLAlchemy(app)


class clientes(db.Model):
    idCliente= db.Column(db.Integer, primary_key=True)
    Dni = db.Column(db.String(80))
    Nombres = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    Direccion = db.column(db.String(80))

db.create_all()
#RUTAS DEl WEB APP---------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('index.html')
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['Usuario']
        password = request.form['password']
        cliente = clientes.query.filter_by(email=email, password=password).first()
        if cliente:
            session['logged_in'] = True
            flash('Bienvenido!')
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrectos'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)