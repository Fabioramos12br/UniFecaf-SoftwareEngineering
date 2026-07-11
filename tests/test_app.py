import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Configura o caminho do Python para encontrar a pasta src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Importa a aplicação Flask
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_usuario_deslogado_redireciona(client):
    """Usuário deslogado deve ser redirecionado para o login."""

    resposta = client.get("/")

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


@patch("app.obter_conexao")
def test_login_com_sucesso(mock_obter_conexao, client):
    """Simula um login válido."""

    mock_conexao = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = {
        "id": 1,
        "nome": "Fabio Ramos",
        "email": "fabio.ramos@gmail.com",
    }

    mock_conexao.cursor.return_value = mock_cursor
    mock_obter_conexao.return_value = mock_conexao

    resposta = client.post(
        "/login",
        data={
            "email": "fabio.ramos@gmail.com",
            "password": "fabio123",
        },
        follow_redirects=False,
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/")


@patch("app.obter_conexao")
def test_login_com_falha(mock_obter_conexao, client):
    """Simula login com credenciais inválidas."""

    mock_conexao = MagicMock()
    mock_cursor = MagicMock()

    # Nenhum usuário encontrado
    mock_cursor.fetchone.return_value = None

    mock_conexao.cursor.return_value = mock_cursor
    mock_obter_conexao.return_value = mock_conexao

    resposta = client.post(
        "/login",
        data={
            "email": "fabio.ramos@gmail.com",
            "password": "senha_errada",
        },
    )

    assert resposta.status_code == 200
    assert "E-mail ou senha incorretos!" in resposta.get_data(as_text=True)