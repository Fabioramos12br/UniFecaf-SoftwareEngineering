from flask import Flask, render_template, request, redirect, session, url_for
from src.database import obter_conexao

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_desafio_logistica'

@app.route('/')

def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', usuario=session['usuario'])

@app.route('/login', methods=['GET', 'POST'])

def login():
    erro = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        
        query = "SELECT * FROM tbl_login WHERE email = %s AND senha = MD5(%s)"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        
        cursor.close()
        conexao.close()
        
        if user:
            session['usuario'] = user['nome']  
            return redirect(url_for('home'))
            
        erro = "E-mail ou senha incorretos!"
            
    return render_template('login.html', erro=erro)

@app.route('/logout')

def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))