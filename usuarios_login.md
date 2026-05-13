# Branch: `heitor` — Rotas `POST /usuarios` e `POST /login`

> **Projeto:** Sistema de Monitoramento de Itens Pessoais via RFID
> **Instituição:** IFSULDEMINAS – Campus Inconfidentes | Curso Técnico em Informática

---

## O que você vai construir

Você ficará responsável pelas rotas de **autenticação** do sistema — são as primeiras que qualquer usuário vai usar ao abrir o app:

| Método | Rota        | O que faz                                  |
|--------|-------------|--------------------------------------------|
| POST   | `/usuarios` | Cria uma conta nova                        |
| POST   | `/login`    | Autentica e devolve um token de acesso     |

Sem essas rotas funcionando, o app não consegue criar conta nem acessar nenhum outro recurso da API.

---

## Por que existe uma "lista padrão" (mock)?

No sistema real, os usuários ficam salvos no banco de dados. Porém, **o banco ainda está sendo configurado**.

Para que você consiga desenvolver e testar agora, sem depender do banco, você vai usar uma **lista fixa no próprio código** que imita o que viria do banco. A ideia é simples: sua rota consulta a lista, valida os dados e responde corretamente. Quando o banco estiver pronto, a lista será substituida pela consulta real — e suas rotas continuam funcionando sem mais alterações.

**Essa é a lista que você deve declarar no seu arquivo:**

```python
USUARIOS_MOCK = [
    {"id": 1, "nome": "João Silva",  "email": "joao@email.com",  "senha": "senha123"},
    {"id": 2, "nome": "Maria Souza", "email": "maria@email.com", "senha": "abc456"},
]
```

> 💡 Em produção, a senha nunca seria salva assim — ficaria como um hash criptografado. Por enquanto, texto simples está ótimo para os testes.

---

## Rota `POST /usuarios`

Cria um novo usuário. O app envia nome, e-mail e senha; a rota valida se o e-mail ainda não foi cadastrado e salva o novo usuário na lista.

**Método:** `POST` | **Rota:** `/usuarios` | **Content-Type:** `application/json`

**Body esperado:**
```json
{
  "nome": "Pedro Costa",
  "email": "pedro@email.com",
  "senha": "minhaSenha99"
}
```

### Respostas

**Usuário criado com sucesso → `201 Created`**
```json
{
  "mensagem": "Usuário cadastrado com sucesso.",
  "usuario": {
    "id": 3,
    "nome": "Pedro Costa",
    "email": "pedro@email.com"
  }
}
```

**E-mail já existe na lista → `409 Conflict`**
```json
{
  "erro": "E-mail já cadastrado."
}
```

**Campos faltando no body → `400 Bad Request`**
```json
{
  "erro": "Campos 'nome', 'email' e 'senha' são obrigatórios."
}
```

---

## Rota `POST /login`

Autentica o usuário. O app envia e-mail e senha; a rota verifica se existe alguém com essas credenciais na lista e, se sim, devolve um **token JWT** — uma espécie de "crachá digital" que o app vai usar para provar sua identidade nas próximas requisições.

**Método:** `POST` | **Rota:** `/login` | **Content-Type:** `application/json`

**Body esperado:**
```json
{
  "email": "joao@email.com",
  "senha": "senha123"
}
```

### Respostas

**Login bem-sucedido → `200 OK`**
```json
{
  "mensagem": "Login realizado com sucesso.",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com"
  }
}
```

**Credenciais erradas → `401 Unauthorized`**
```json
{
  "erro": "E-mail ou senha incorretos."
}
```

**Campos faltando no body → `400 Bad Request`**
```json
{
  "erro": "Campos 'email' e 'senha' são obrigatórios."
}
```

---

## Dependência necessária

Para gerar o token JWT, instale a biblioteca:

```bash
pip install PyJWT
```

---

## Como testar com o Rest Client (VS Code)

O **Rest Client** é uma extensão do VS Code que permite disparar requisições HTTP direto do editor, sem precisar de nenhuma outra ferramenta.

### 1. Instale a extensão

Na aba de extensões do VS Code (`Ctrl+Shift+X`), pesquise por **REST Client** (autor: Huachao Mao) e instale.

### 2. Crie o arquivo de testes

Na raiz do projeto, crie um arquivo chamado `testes.http`. O Rest Client reconhece arquivos `.http` automaticamente e habilita o botão de envio.

### 3. Copie os testes abaixo para o arquivo

```http
### Teste 1 — Cadastrar novo usuário
POST http://localhost:5000/usuarios
Content-Type: application/json

{
  "nome": "Pedro Costa",
  "email": "pedro@email.com",
  "senha": "minhaSenha99"
}

###

### Teste 2 — Tentar cadastrar com e-mail já existente
POST http://localhost:5000/usuarios
Content-Type: application/json

{
  "nome": "Outro Nome",
  "email": "joao@email.com",
  "senha": "qualquercoisa"
}

###

### Teste 3 — Cadastro com campo faltando
POST http://localhost:5000/usuarios
Content-Type: application/json

{
  "nome": "Sem Email"
}

###

### Teste 4 — Login com credenciais corretas
POST http://localhost:5000/login
Content-Type: application/json

{
  "email": "joao@email.com",
  "senha": "senha123"
}

###

### Teste 5 — Login com senha errada
POST http://localhost:5000/login
Content-Type: application/json

{
  "email": "joao@email.com",
  "senha": "senhaerrada"
}
```

### 4. Execute

Acima de cada bloco `###` aparece o link **Send Request** — clique nele para disparar a requisição. A resposta abre em um painel lateral com o status HTTP e o JSON retornado.

> ⚠️ Sua API precisa estar rodando localmente (`flask run` ou `python app.py`) antes de clicar em Send Request.