# Branch: `gustavo` — Rota `POST /processar`

> **Projeto:** Sistema de Monitoramento de Itens Pessoais via RFID
>
> **Instituição:** IFSULDEMINAS – Campus Inconfidentes | Curso Técnico em Informática

---

## O que você vai construir

Essa é a **rota principal do sistema**. É ela que recebe do Raspberry Pi a lista de UIDs lidos pelo leitor RFID quando o usuário sai de casa, verifica quais itens obrigatórios estão faltando e retorna essa informação para que a notificação possa ser disparada.

Resumindo o fluxo:

```
Raspberry Pi lê as etiquetas RFID
        ↓
Envia os UIDs lidos via POST para /processar
        ↓
A API compara com os itens obrigatórios cadastrados
        ↓
Retorna quais itens estão faltando
```

---

## Por que existe uma "lista padrão" (mock)?

No sistema real, os itens obrigatórios de cada usuário ficam salvos no banco de dados. Porém, **o banco ainda está sendo configurado**.

Para que você consiga desenvolver e testar sua rota agora, sem depender do banco, você vai usar uma **lista fixa no próprio código** que imita exatamente o que viria do banco. Quando o banco estiver pronto, o responsável substitui essa lista pela consulta real — e sua rota continua funcionando sem nenhuma outra mudança.

**Essa é a lista que você deve declarar no seu arquivo:**

```python
ITENS_MOCK = [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa",  "obrigatorio": True},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",       "obrigatorio": True},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",   "obrigatorio": True},
    {"uid": "E2003412B802011833303635", "nome": "Chave do Carro", "obrigatorio": False},
]
```

> 💡 Note que `"Chave do Carro"` tem `obrigatorio: False`. Isso significa que, mesmo que ela não seja detectada pelo leitor, **não deve gerar alerta**. Sua rota deve verificar **somente** os itens marcados como `True`.

---

## O que a rota recebe

**Método:** `POST`
**Rota:** `/processar`
**Content-Type:** `application/json`

O Raspberry Pi vai enviar um JSON com o ID do usuário e a lista de UIDs que o leitor conseguiu captar na saída:

```json
{
  "usuario_id": 1,
  "uids_lidos": [
    "E2003412B802011833303632",
    "E2003412B802011833303634"
  ]
}
```

No exemplo acima, a Carteira (`...3633`) **não aparece** na lista — ou seja, o usuário saiu sem ela e precisa ser alertado.

---

## O que a rota deve retornar

### Quando algum item obrigatório estiver faltando → `200 OK`

```json
{
  "status": "alerta",
  "itens_faltando": [
    {"uid": "E2003412B802011833303633", "nome": "Carteira"}
  ],
  "mensagem": "1 item obrigatório não foi encontrado."
}
```

### Quando todos os itens obrigatórios estiverem presentes → `200 OK`

```json
{
  "status": "ok",
  "itens_faltando": [],
  "mensagem": "Todos os itens obrigatórios estão presentes."
}
```

### Quando o corpo da requisição estiver errado ou incompleto → `400 Bad Request`

```json
{
  "erro": "Campos 'usuario_id' e 'uids_lidos' são obrigatórios."
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
### Teste 1 — Item faltando (Carteira não está entre os UIDs enviados)
POST http://localhost:5000/processar
Content-Type: application/json

{
  "usuario_id": 1,
  "uids_lidos": [
    "E2003412B802011833303632",
    "E2003412B802011833303634"
  ]
}

###

### Teste 2 — Todos os itens obrigatórios presentes
POST http://localhost:5000/processar
Content-Type: application/json

{
  "usuario_id": 1,
  "uids_lidos": [
    "E2003412B802011833303632",
    "E2003412B802011833303633",
    "E2003412B802011833303634"
  ]
}

###

### Teste 3 — Body inválido (campo uids_lidos ausente)
POST http://localhost:5000/processar
Content-Type: application/json

{
  "usuario_id": 1
}
```

### 4. Execute

Acima de cada bloco `###` aparece o link **Send Request** — clique nele para disparar a requisição. A resposta abre em um painel lateral com o status HTTP e o JSON retornado.

> ⚠️ Sua API precisa estar rodando localmente (`flask run` ou `python app.py`) antes de clicar em Send Request.

---

## Checklist — sua rota está pronta quando:

- [ ] Teste 1 retorna `status: "alerta"` com a Carteira listada em `itens_faltando`
- [ ] Teste 2 retorna `status: "ok"` com `itens_faltando` vazio
- [ ] Teste 3 retorna erro `400`
- [ ] Itens com `obrigatorio: False` nunca aparecem em `itens_faltando`