# Branch: `caua` — Rotas `GET /itens` e `DELETE /itens/<uid>`

> **Projeto:** Sistema de Monitoramento de Itens Pessoais via RFID
>
> **Instituição:** IFSULDEMINAS – Campus Inconfidentes | Curso Técnico em Informática

---

## O que você vai construir

Você ficará responsável pelas rotas de **visualização e remoção de itens** — são as funcionalidades que permitem ao usuário ver o que tem cadastrado e remover o que não usa mais:

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | `/itens` | Lista todos os itens cadastrados |
| DELETE | `/itens/<uid>` | Remove um item pelo seu UID |

---

## Por que existe uma "lista padrão" (mock)?

No sistema real, os itens ficam salvos no banco de dados. Porém, **a integração com o banco ainda está sendo finalizada**.

Para que você consiga desenvolver e testar agora, você usará uma **lista fixa no próprio código** que simula os dados do banco. Sua rota consulta essa lista, retorna os itens (GET) ou remove entradas (DELETE). Quando o banco estiver pronto, basta trocar o acesso à lista pela consulta real — sua lógica continua intacta.

**Essa é a lista que você deve declarar no seu arquivo:**

```python
ITENS_MOCK = [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa",    "obrigatorio": True},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",         "obrigatorio": True},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",     "obrigatorio": True},
    {"uid": "E2003412B802011833303635", "nome": "Chave do Carro",   "obrigatorio": False},
    {"uid": "E2003412B802011833303636", "nome": "Cartão do Ônibus", "obrigatorio": True},
]
```

> 💡 Como o sistema é pensado para uma única residência, não existe mais `usuario_id`. A lista é global — todos os itens cadastrados convivem juntos e as rotas operam sobre ela inteira.

---

## Rota `GET /itens`

Retorna todos os itens cadastrados no sistema.

**Método:** `GET` | **Rota:** `/itens`

### Respostas

**Lista retornada com sucesso → `200 OK`**
```json
{
  "itens": [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa",  "obrigatorio": true},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",       "obrigatorio": true},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",   "obrigatorio": true},
    {"uid": "E2003412B802011833303635", "nome": "Chave do Carro", "obrigatorio": false},
    {"uid": "E2003412B802011833303636", "nome": "Cartão do Ônibus", "obrigatorio": true}
  ],
  "total": 5
}
```

**Nenhum item cadastrado → `200 OK`**
```json
{
  "itens": [],
  "total": 0
}
```

---

## Rota `DELETE /itens/<uid>`

Remove um item da lista pelo seu UID, informado diretamente na URL.

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
### Teste 1 — Listar todos os itens
GET http://localhost:5000/itens

###

### Teste 2 — Remover um item existente
DELETE http://localhost:5000/itens/E2003412B802011833303633

###

### Teste 3 — Listar novamente (Carteira não deve aparecer mais)
GET http://localhost:5000/itens

###

### Teste 4 — Tentar remover um UID que não existe
DELETE http://localhost:5000/itens/UID_INEXISTENTE
```

### 4. Execute

Acima de cada bloco `###` aparece o link **Send Request** — clique nele para disparar a requisição. A resposta abre em um painel lateral com o status HTTP e o JSON retornado.

> ⚠️ Sua API precisa estar rodando localmente (`flask run` ou `python app.py`) antes de clicar em Send Request.
>
> 💡 **Atenção ao testar o DELETE:** a lista existe apenas na memória enquanto o servidor está rodando, então ela volta ao estado original toda vez que a API for reiniciada. Se quiser repetir o Teste 2, basta reiniciar o servidor.

---

## Checklist — suas rotas estão prontas quando:

- [ ] Teste 1 retorna todos os itens do mock com o campo `total` correto
- [ ] Teste 2 retorna `200` confirmando a remoção da Carteira
- [ ] Teste 3 lista os itens sem a Carteira (removida no Teste 2)
- [ ] Teste 4 retorna erro `404` (UID inexistente)