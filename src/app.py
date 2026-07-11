from flask import Flask, render_template, request, redirect, session, url_for
from src.database import obter_conexao

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_desafio_logistica'

@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', usuario=session['usuario'])