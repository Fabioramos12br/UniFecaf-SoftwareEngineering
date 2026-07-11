from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from database import obter_conexao

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

@app.route('/cadastro', methods=['GET', 'POST'])

def cadastro():
    erro = None
    sucesso = None
    if request.method == 'POST':
        nome = request.form.get('nome')
        data_nasc = request.form.get('data_nascimento')
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()
            
            query = """INSERT INTO tbl_login (nome, data_nascimento, email, senha) 
                       VALUES (%s, %s, %s, MD5(%s))"""
            cursor.execute(query, (nome, data_nasc, email, password))
            conexao.commit()
            
            cursor.close()
            conexao.close()
            sucesso = "Cadastro realizado com sucesso! Faça o login."
        except mysql.connector.Error:
            erro = "Erro: Este e-mail já está cadastrado no sistema."
            
    return render_template('cadastro.html', erro=erro, sucesso=sucesso)

@app.route('/logout')

def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)