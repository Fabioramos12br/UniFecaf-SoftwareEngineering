import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          
    'password': 'SUA_SENHA',  # <- mude sua senha aqui para conectar ao SEU banco de dados
    'database': 'db_SEunifecaf'
}

def obter_conexao():
    return mysql.connector.connect(**DB_CONFIG)