# UniFecaf-SoftwareEngineering (TechFlow)

Sistema web para **autenticação e gestão de acessos** desenvolvido em **Python com Flask**, integrado com **MySQL**.

O projeto entrega um fluxo simples:
- Usuário **se cadastra**
- Usuário **faz login**
- Usuário logado acessa a **Home (painel)**
- Usuário pode **deslogar**

Também possui **testes automatizados com Pytest**, com mocking da camada de banco.

> Observação: o HTML e o texto do dashboard mencionam “Kanban”, porém o código atual do projeto implementa principalmente autenticação e página protegida.

---

## Tecnologias e dependências

- **Flask**: servidor web e rotas
- **mysql-connector-python**: conexão com MySQL
- **Pytest**: testes
- **Jinja2** (via Flask): renderização de templates em `src/templates`

Dependências instaláveis via:
```bash
pip install -r requirements.txt
```

---

## Estrutura do projeto

- `src/app.py`
  - Define as rotas Flask e a lógica de autenticação.
- `src/database.py`
  - Mantém a configuração de conexão com o MySQL e a função `obter_conexao()`.
- `src/templates/`
  - `login.html` (login)
  - `cadastro.html` (cadastro)
  - `home.html` (home/dashboard)
- `tests/test_app.py`
  - Testes do fluxo de login e proteção da rota `/`.

---

## Rotas e fluxo de funcionamento

### 1) Página Home (rota `/`)
- Rota: **GET `/`**
- Comportamento:
  - Se **não** existir `session['usuario']`, redireciona para **`/login`**.
  - Se existir, renderiza `home.html` passando `usuario=session['usuario']`.

### 2) Login (rota `/login`)
- Rota: **GET `/login`**
  - Renderiza `login.html`.
- Rota: **POST `/login`**
  - Recebe:
    - `email`
    - `password`
  - Consulta no MySQL:
    ```sql
    SELECT * FROM tbl_login
    WHERE email = %s AND senha = MD5(%s)
    ```
  - Se autenticado:
    - grava `session['usuario'] = user['nome']`
    - redireciona para `/`
  - Se falhar:
    - exibe erro em `login.html`: **"E-mail ou senha incorretos!"**

### 3) Cadastro (rota `/cadastro`)
- Rota: **GET `/cadastro`**
  - Renderiza `cadastro.html`.
- Rota: **POST `/cadastro`**
  - Recebe:
    - `nome`
    - `data_nascimento`
    - `email`
    - `password`
  - Insere no MySQL:
    ```sql
    INSERT INTO tbl_login (nome, data_nascimento, email, senha)
    VALUES (%s, %s, %s, MD5(%s))
    ```
  - Em caso de erro (ex.: e-mail duplicado), mostra em `cadastro.html`:
    - **"Erro: Este e-mail já está cadastrado no sistema."**
  - Em sucesso, mostra:
    - **"Cadastro realizado com sucesso! Faça o login."**

### 4) Logout (rota `/logout`)
- Rota: **GET `/logout`**
  - Remove `session['usuario']`
  - Redireciona para `/login`

---

## Banco de dados MySQL

### Configuração
A conexão está definida em `src/database.py`:

- `DB_CONFIG` (ajuste obrigatoriamente):
  - `host`
  - `user`
  - `password`  ✅ **substitua** `SUA_SENHA`
  - `database`

Função utilizada na aplicação:
- `obter_conexao()` → retorna `mysql.connector.connect(**DB_CONFIG)`

### Tabela esperada: `tbl_login`
O código supõe que existe uma tabela chamada **`tbl_login`** com, no mínimo, as colunas:
- `id` (não é explicitado no INSERT, mas é retornado no SELECT e usado nos testes)
- `nome`
- `data_nascimento`
- `email`
- `senha`

Além disso, o login usa `senha = MD5(password)`, então a coluna `senha` deve armazenar o **MD5** da senha no formato que o MySQL retorna ao executar `MD5(%s)`.

> Recomendação técnica: o uso de MD5 para senhas não é seguro para produção. Para um projeto real, use hashing adequado (ex.: `bcrypt`, `scrypt`, `argon2`) e migrações.

### Criando o banco e a tabela (modelo)
O projeto não traz scripts SQL prontos. Abaixo vai um exemplo **base** (ajuste conforme seu padrão):

```sql
CREATE DATABASE db_SEunifecaf;
USE db_SEunifecaf;

CREATE TABLE tbl_login (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(200) NOT NULL,
  data_nascimento DATE NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  senha VARCHAR(64) NOT NULL
);
```

---

## Como rodar o projeto localmente

### Pré-requisitos
- Python instalado
- MySQL instalado e com o banco/tabela criados

### 1) Instalar dependências
```bash
pip install -r requirements.txt
```

### 2) Ajustar credenciais do MySQL
Edite `src/database.py` e ajuste:
- `DB_CONFIG['password']`
- `DB_CONFIG['database']`

### 3) Rodar a aplicação
```bash
python src/app.py
```

Por padrão, o Flask inicia em:
- `http://127.0.0.1:5000/`

### 4) Testar manualmente
- Acesse `http://127.0.0.1:5000/` e verifique que redireciona para `/login` se não estiver logado.
- Faça cadastro em `/cadastro`.
- Faça login em `/login`.
- Veja o dashboard em `/`.
- Use `/logout` para encerrar a sessão.

---

## Como executar os testes

Os testes ficam em `tests/test_app.py`.

### Rodar com Pytest
```bash
pytest
```

### O que é testado
- **Proteção da home**: se o usuário estiver deslogado, `GET /` deve redirecionar para `/login`.
- **Login com sucesso**: usa `unittest.mock.patch` para simular que o MySQL retornou um usuário.
- **Login com falha**: simula `fetchone()` retornando `None` e valida a mensagem de erro exibida na resposta.

---

## Pontos de atenção (boas práticas)

- **Segurança de senhas**: atualmente o projeto usa `MD5` no banco.
  - Para produção, substitua por hashing seguro (bcrypt/argon2) e atualize o fluxo de autenticação.
- **Configuração sensível**: `DB_CONFIG['password']` está hardcoded.
  - Em projetos reais, use variáveis de ambiente (ex.: `os.environ`).
- **Tratamento de exceções**: o cadastro captura `mysql.connector.Error` para sinalizar e-mail duplicado.
  - Em um refinamento, trate códigos de erro específicos do MySQL.

---

## Próximos passos (se quiser evoluir o projeto)

- Adicionar scripts de migração e seed (ex.: com Alembic).
- Criar uma camada de persistência (Repository/DAO) separada da rota Flask.
- Implementar páginas adicionais (ex.: Kanban real) com base na sessão do usuário.
- Ajustar validações de formulário (ex.: tamanho de senha, validação de e-mail).

---

## Autor
Projeto desenvolvido para fins acadêmicos/estudo em **Engenharia de Software**.
