# Branch: `caua` — Rotas `GET /itens` e `DELETE /itens/{uid}`

> **Projeto:** Sistema de Monitoramento de Itens Pessoais via RFID
>
> **Instituição:** IFSULDEMINAS – Campus Inconfidentes | Curso Técnico em Informática

---

## O que você vai construir

Você ficará responsável pelas rotas de **gerenciamento e visualização de itens** — são as funcionalidades que permitem ao usuário ver o que ele tem cadastrado e organizar sua lista:

| Método | Rota | O que faz |
| --- | --- | --- |
| GET | `/itens` | Lista todos os itens de um usuário específico |
| DELETE | `/itens/<uid>` | Remove um item do sistema permanentemente |

Essas rotas são fundamentais para a interface do aplicativo, permitindo que o usuário tenha controle total sobre seus pertences monitorados.

---

## Por que existe uma "lista padrão" (mock)?

No sistema real, os itens cadastrados ficam salvos no banco de dados. Porém, **a integração com o banco ainda está sendo finalizada**.

Para que você consiga desenvolver e testar sua lógica agora, você usará uma **lista fixa no próprio código** que simula os dados do banco. Sua rota deve consultar essa lista, filtrar as informações (no caso do GET) ou remover entradas (no caso do DELETE). Quando o banco estiver pronto, basta trocar o acesso à lista pela consulta real.

**Essa é a lista que você deve declarar no seu arquivo:**

```python
ITENS_MOCK = [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa",    "obrigatorio": True,  "usuario_id": 1},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",         "obrigatorio": True,  "usuario_id": 1},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",     "obrigatorio": True,  "usuario_id": 1},
    {"uid": "E2003412B802011833303635", "nome": "Chave do Carro",   "obrigatorio": False, "usuario_id": 1},
    {"uid": "E2003412B802011833303636", "nome": "Cartão do Ônibus", "obrigatorio": True,  "usuario_id": 2},
]
```

---

## Rota `GET /itens`

Retorna os itens pertencentes a um usuário específico. O ID do usuário deve ser enviado via URL como query parameter.

**Método:** `GET` | **Rota:** `/itens?usuario_id=1`

### Respostas

**Lista retornada com sucesso → `200 OK`**

```json
{
  "itens": [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa", "obrigatorio": true},
    {"uid": "E2003412B802011833303633", "nome": "Carteira", "obrigatorio": true}
  ],
  "total": 2
}
```

**Usuário não informado ou inválido → `400 Bad Request`**

```json
{
  "erro": "O parâmetro 'usuario_id' é obrigatório e deve ser um número."
}
```

---

## Rota `DELETE /itens/<uid>`

Remove um item da lista utilizando o código único (UID) dele.

**Método:** `DELETE` | **Rota:** `/itens/E2003412B802011833303633`

### Respostas

**Item removido com sucesso → `200 OK`**

```json
{
  "mensagem": "Item removido com sucesso.",
  "uid": "E2003412B802011833303633"
}
```

**UID não encontrado na lista → `404 Not Found`**

```json
{
  "erro": "Item com UID 'E2003412B802011833303633' não encontrado."
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
### Teste 1 — Listar itens do usuário 1
GET http://localhost:5000/itens?usuario_id=1

###

### Teste 2 — Tentar listar sem informar o usuário
GET http://localhost:5000/itens

###

### Teste 3 — Remover um item existente
DELETE http://localhost:5000/itens/E2003412B802011833303633

###

### Teste 4 — Tentar remover um item que não existe
DELETE http://localhost:5000/itens/UID_INEXISTENTE
```

### 4. Execute

Acima de cada bloco `###` aparece o link **Send Request** — clique nele para disparar a requisição. A resposta abre em um painel lateral com o status HTTP e o JSON retornado.

> ⚠️ Sua API precisa estar rodando localmente (`flask run` ou `python app.py`) antes de clicar em Send Request.
>
> 💡 **Atenção ao testar o DELETE:** como a lista existe apenas na memória enquanto o servidor está rodando, ela volta ao estado original toda vez que a API for reiniciada. Se você deletar um item e quiser testá-lo novamente, basta reiniciar o servidor.

---

## Checklist — suas rotas estão prontas quando:

- [ ] Teste 1 retorna apenas os itens do `usuario_id=1` com o campo `total` correto
- [ ] Teste 2 retorna erro `400` (parâmetro ausente)
- [ ] Teste 3 retorna `200` confirmando a remoção
- [ ] Teste 4 retorna erro `404` (UID inexistente)
- [ ] Após o Teste 3, o Teste 1 não exibe mais o item removido (até reiniciar o servidor)