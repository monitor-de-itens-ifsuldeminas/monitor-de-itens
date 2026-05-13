# Branch: `gael` — Rotas `POST /itens` e `GET /ler-uid`

> **Projeto:** Sistema de Monitoramento de Itens Pessoais via RFID
>
> **Instituição:** IFSULDEMINAS – Campus Inconfidentes | Curso Técnico em Informática

---

## O que você vai construir

Você ficará responsável pelas rotas que compõem o fluxo de **cadastro de novos objetos** no sistema. Essas rotas permitem que o aplicativo identifique o que o leitor RFID está captando e salve essas informações:

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | `/ler-uid` | Retorna o último ID capturado pelo leitor RFID |
| POST | `/itens` | Salva um novo item (nome, UID e configurações) |

Sem essas rotas, o usuário não consegue registrar seus pertences no sistema, tornando o monitoramento impossível.

---

## Por que existe uma "lista padrão" (mock)?

No sistema final, o Raspberry Pi lerá a porta serial para obter o UID e salvará os itens em um banco de dados. Entretanto, **a integração com o hardware e o banco de dados ainda está em desenvolvimento**.

Para que você possa avançar agora, você usará **dados simulados (mocks)**. Eles funcionam como um "tapa-buraco": sua rota finge que leu o sensor ou que consultou o banco, usando uma lista fixa no código. Quando o hardware estiver pronto, basta trocar a fonte dos dados e sua lógica continuará intacta.

**Utilize estas variáveis no seu código:**

```python
# Simula o último UID que o leitor capturou
UID_LIDO_MOCK = "E2003412B802011833303699"

# Simula a tabela de itens já cadastrados no banco
ITENS_MOCK = [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa",  "obrigatorio": True,  "usuario_id": 1},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",       "obrigatorio": True,  "usuario_id": 1},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",   "obrigatorio": True,  "usuario_id": 1},
]

```

---

## Rota `GET /ler-uid`

Informa ao app qual é o UID da etiqueta que está encostada no leitor no momento.

### Respostas

**✅ UID disponível (Simulado) → `200 OK`**

```json
{
  "uid": "E2003412B802011833303699",
  "status": "disponivel"
}

```

**✅ Nenhum UID no leitor → `200 OK`**

```json
{
  "uid": null,
  "status": "aguardando"
}

```

---

## Rota `POST /itens`

Recebe os detalhes do item preenchidos no app e os "salva" na lista.

**Body esperado (JSON):**

```json
{
  "uid": "E2003412B802011833303699",
  "nome": "Chave do Armário",
  "obrigatorio": true,
  "usuario_id": 1
}

```

### Respostas

**Item cadastrado com sucesso → `201 Created`**

```json
{
  "mensagem": "Item cadastrado com sucesso.",
  "item": { "uid": "...", "nome": "...", "obrigatorio": true, "usuario_id": 1 }
}

```

**UID já existe na lista → `409 Conflict`**

```json
{
  "erro": "Já existe um item cadastrado com este UID."
}

```

**Campos faltando no body → `400 Bad Request`**

```json
{
  "erro": "Campos 'uid', 'nome', 'obrigatorio' e 'usuario_id' são obrigatórios."
}

```

---

## Como testar com o Rest Client (VS Code)

O **Rest Client** é uma extensão do VS Code que permite disparar requisições HTTP direto do editor, sem precisar de nenhuma outra ferramenta.

### 1. Instale a extensão

Na aba de extensões do VS Code (`Ctrl+Shift+X`), pesquise por **REST Client** (autor: Huachao Mao) e instale.

### 2. Crie o arquivos de testes

Na raiz do projeto, crie um arquivo chamado `testes.http`. O Rest Client reconhece arquivos `.http` automaticamente e habilita o botão de envio.

### 3. Copie os testes abaixos para o arquivo

```http
### Teste 1 — Verificar UID disponível no leitor
GET http://localhost:5000/ler-uid

###

### Teste 2 — Cadastrar um novo item
POST http://localhost:5000/itens
Content-Type: application/json

{
  "uid": "E2003412B802011833303699",
  "nome": "Chave do Armário",
  "obrigatorio": true,
  "usuario_id": 1
}

###

### Teste 3 — Tentar cadastrar UID duplicado (já existente no mock)
POST http://localhost:5000/itens
Content-Type: application/json

{
  "uid": "E2003412B802011833303632",
  "nome": "Item Repetido",
  "obrigatorio": false,
  "usuario_id": 1
}

###

### Teste 4 — Cadastro com erro (faltando campo)
POST http://localhost:5000/itens
Content-Type: application/json

{
  "nome": "Item Sem UID"
}

```

### 4. Execute

Acima de cada bloco `###` aparece o link **Send Request** — clique nele para disparar a requisição. A resposta abre em um painel lateral com o status HTTP e o JSON retornado.

> ⚠️ Sua API precisa estar rodando localmente (`flask run` ou `python app.py`) antes de clicar em Send Request.
