# Branch: `gael` — Rota `POST /itens`

> **Projeto:** Sistema de Monitoramento de Itens Pessoais via RFID
>
> **Instituição:** IFSULDEMINAS – Campus Inconfidentes | Curso Técnico em Informática

---

## O que você vai construir

Você ficará responsável pela rota que **salva um novo item** no sistema após o usuário confirmar o cadastro pelo app:

| Método | Rota | O que faz |
|--------|------|-----------|
| POST | `/itens` | Salva um novo item com nome e configurações |

Essa rota é o passo final do fluxo de cadastro. Antes dela, o Raspberry Pi já leu a etiqueta e o app já exibiu o UID para o usuário — agora só falta salvar.

---

## Entendendo o fluxo antes de começar

```
Raspberry Pi lê etiqueta  →  POST /cadastrar-uid  →  backend guarda o UID
                                                              ↓
                                        App consulta GET /ler-uid e exibe o UID
                                                              ↓
                                        Usuário digita o nome do item no app
                                                              ↓
                                        App chama POST /itens  ←  (sua rota)
                                                              ↓
                                                       Item salvo na lista
```

---

## Por que existe uma "lista padrão" (mock)?

No sistema real, os itens ficam salvos no banco de dados. Porém, **a integração com o banco ainda está sendo finalizada**.

Para que você consiga desenvolver e testar agora, você usará uma **lista fixa no próprio código** que simula os dados já cadastrados. Sua rota deve verificar se o UID já existe nessa lista antes de salvar, e adicionar o novo item caso não exista. Quando o banco estiver pronto, basta trocar a lista pela consulta real.

**Essa é a lista que você deve declarar no seu arquivo:**

```python
ITENS_MOCK = [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa", "obrigatorio": True},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",      "obrigatorio": True},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",  "obrigatorio": True},
]
```

> 💡 Como o sistema é pensado para uma única residência, não existe `usuario_id`. A lista é global — qualquer item cadastrado entra nela diretamente.

---

## O que a rota recebe

**Método:** `POST` | **Rota:** `/itens` | **Content-Type:** `application/json`

```json
{
  "uid": "E2003412B802011833303699",
  "nome": "Chave do Armário",
  "obrigatorio": true
}
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `uid` | `string` | UID da etiqueta RFID lida pelo leitor |
| `nome` | `string` | Nome que o usuário deu ao item |
| `obrigatorio` | `boolean` | Se `true`, a ausência do item gera alerta |

---

## O que a rota deve retornar

### Item cadastrado com sucesso → `201 Created`

```json
{
  "mensagem": "Item cadastrado com sucesso.",
  "item": {
    "uid": "E2003412B802011833303699",
    "nome": "Chave do Armário",
    "obrigatorio": true
  }
}
```

### UID já existe na lista → `409 Conflict`

```json
{
  "erro": "Já existe um item cadastrado com este UID."
}
```

### Campos faltando no body → `400 Bad Request`

```json
{
  "erro": "Campos 'uid', 'nome' e 'obrigatorio' são obrigatórios."
}
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
### Teste 1 — Cadastrar um novo item
POST http://localhost:5000/itens
Content-Type: application/json

{
  "uid": "E2003412B802011833303699",
  "nome": "Chave do Armário",
  "obrigatorio": true
}

###

### Teste 2 — Tentar cadastrar o mesmo UID novamente
POST http://localhost:5000/itens
Content-Type: application/json

{
  "uid": "E2003412B802011833303699",
  "nome": "Nome Diferente",
  "obrigatorio": false
}

###

### Teste 3 — Tentar cadastrar UID já existente no mock
POST http://localhost:5000/itens
Content-Type: application/json

{
  "uid": "E2003412B802011833303632",
  "nome": "Item Repetido",
  "obrigatorio": false
}

###

### Teste 4 — Body com campo faltando
POST http://localhost:5000/itens
Content-Type: application/json

{
  "nome": "Item Sem UID"
}
```

### 4. Execute

Acima de cada bloco `###` aparece o link **Send Request** — clique nele para disparar a requisição. A resposta abre em um painel lateral com o status HTTP e o JSON retornado.

> ⚠️ Sua API precisa estar rodando localmente (`flask run` ou `python app.py`) antes de clicar em Send Request.
>
> 💡 Os Testes 2 e 3 testam a mesma situação por caminhos diferentes: o Teste 2 usa um UID que você mesmo acabou de cadastrar, e o Teste 3 usa um UID que já estava no mock. Os dois devem retornar `409`.

---

## Checklist — sua rota está pronta quando:

- [ ] Teste 1 retorna o item cadastrado com status `201`
- [ ] Teste 2 retorna erro `409` (UID recém-cadastrado não pode ser duplicado)
- [ ] Teste 3 retorna erro `409` (UID do mock também não pode ser duplicado)
- [ ] Teste 4 retorna erro `400` (campo faltando)