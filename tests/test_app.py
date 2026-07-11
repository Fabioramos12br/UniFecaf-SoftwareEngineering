import pytest
from unittest.mock import patch, MagicMock
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_usuario_deslogado_redireciona(client):
    """Garante que qualquer pessoa deslogada tentando acessar a Home seja jogada para o Login"""
    resposta = client.get('/')
    assert resposta.status_code == 302
    assert '/login' in resposta.headers['Location']

@patch('src.app.obter_conexao')
def test_login_com_sucesso(mock_obter_conexao, client):
    """Simula uma resposta positiva do MySQL para validar o fluxo de sucesso no Login"""
    mock_conexao = MagicMock()
    mock_cursor = MagicMock()
    
    mock_cursor.fetchone.return_value = {'id': 1, 'nome': 'Fabio Ramos', 'email': 'fabio.ramos@gmail.com'}
    mock_conexao.cursor.return_value = mock_cursor
    mock_obter_conexao.return_value = mock_conexao

    resposta = client.post('/login', data={'email': 'fabio.ramos@gmail.com', 'password': 'fabio123'})
    assert resposta.status_code == 302  

@patch('src.app.obter_conexao')
def test_login_com_falha(mock_obter_conexao, client):
    """Simula uma falha de autenticação (credenciais erradas)"""
    mock_conexao = MagicMock()
    mock_cursor = MagicMock()
    
    mock_cursor.fetchone.return_value = None
    mock_conexao.cursor.return_value = mock_cursor
    mock_obter_conexao.return_value = mock_conexao

    resposta = client.post('/login', data={'email': 'fabio.ramos@gmail.com', 'password': 'senha_errada'})
    assert resposta.status_code == 200  
    assert b"E-mail ou senha incorretos!" in resposta.data