# Branch: `heitor` — Rotas `POST /cadastrar-uid` e `GET /ler-uid`

> **Projeto:** Sistema de Monitoramento de Itens Pessoais via RFID
>
> **Instituição:** IFSULDEMINAS – Campus Inconfidentes | Curso Técnico em Informática

---

## O que você vai construir

Você ficará responsável pelas rotas que formam a **ponte entre o leitor RFID e o app** durante o cadastro de um novo item:

| Método | Rota | Quem chama | O que faz |
|--------|------|------------|-----------|
| POST | `/cadastrar-uid` | Raspberry Pi | Recebe um UID lido e o guarda em memória |
| GET | `/ler-uid` | App (Kodular) | Retorna o último UID guardado |

---

## Entendendo o fluxo antes de começar

Toda vez que o Raspberry Pi lê uma etiqueta RFID, ele envia o UID para duas rotas ao mesmo tempo: `/processar` (responsabilidade de outro membro) e `/cadastrar-uid` (sua). Sua rota simplesmente guarda esse UID em uma variável no backend chamada `ultimo_uid_lido`.

Enquanto isso, o app fica fazendo requisições periódicas para `GET /ler-uid`. Quando a variável tiver um UID guardado, a rota o retorna e o app exibe para o usuário confirmar o nome do item.

```
Raspberry Pi lê etiqueta
        ↓
POST /cadastrar-uid  ──────→  backend salva em ultimo_uid_lido
                                        ↓
                     GET /ler-uid  ←──  App pergunta a cada X segundos
                                        ↓
                     retorna o UID  ──→  App exibe para o usuário
```

---

## Por que existe uma "variável padrão" (mock)?

No sistema real, o UID chega via `POST /cadastrar-uid` enviado pelo Raspberry Pi. Porém, **o hardware ainda está sendo integrado**.

Para que você consiga testar agora sem precisar do Raspberry Pi físico, declare uma variável fixa no código simulando um UID já recebido. Quando o hardware estiver pronto, essa variável passará a ser atualizada pela rota `/cadastrar-uid` — e o `GET /ler-uid` continuará funcionando sem mudanças.

**Declare esta variável no seu arquivo:**

```python
# Simula o último UID que o Raspberry Pi enviou
ultimo_uid_lido = "E2003412B802011833303699"
```

> 💡 Essa variável precisa ser acessível pelas duas rotas. Em Flask, declará-la no escopo global do arquivo já é suficiente para os testes.

---

## Rota `POST /cadastrar-uid`

Recebida pelo Raspberry Pi. Atualiza a variável `ultimo_uid_lido` com o UID enviado.

**Método:** `POST` | **Rota:** `/cadastrar-uid` | **Content-Type:** `application/json`

**Body esperado:**
```json
{
  "uid": "E2003412B802011833303699"
}
```

### Respostas

**UID recebido com sucesso → `200 OK`**
```json
{
  "mensagem": "UID recebido e armazenado com sucesso.",
  "uid": "E2003412B802011833303699"
}
```

**Campo `uid` ausente no body → `400 Bad Request`**
```json
{
  "erro": "O campo 'uid' é obrigatório."
}
```

---

## Rota `GET /ler-uid`

Chamada pelo app. Retorna o conteúdo atual da variável `ultimo_uid_lido`.

**Método:** `GET` | **Rota:** `/ler-uid`

### Respostas

**UID disponível → `200 OK`**
```json
{
  "uid": "E2003412B802011833303699",
  "status": "disponivel"
}
```

**Nenhum UID recebido ainda → `200 OK`**
```json
{
  "uid": null,
  "status": "aguardando"
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
### Teste 1 — Raspberry Pi envia um UID para o backend
POST http://localhost:5000/cadastrar-uid
Content-Type: application/json

{
  "uid": "E2003412B802011833303699"
}

###

### Teste 2 — App consulta o último UID recebido
GET http://localhost:5000/ler-uid

###

### Teste 3 — Raspberry Pi envia um novo UID (sobrescreve o anterior)
POST http://localhost:5000/cadastrar-uid
Content-Type: application/json

{
  "uid": "E2003412B802011833303700"
}

###

### Teste 4 — App consulta novamente (deve retornar o UID novo)
GET http://localhost:5000/ler-uid

###

### Teste 5 — Body inválido (campo uid ausente)
POST http://localhost:5000/cadastrar-uid
Content-Type: application/json

{}
```

### 4. Execute

Acima de cada bloco `###` aparece o link **Send Request** — clique nele para disparar a requisição. A resposta abre em um painel lateral com o status HTTP e o JSON retornado.

> ⚠️ Sua API precisa estar rodando localmente (`flask run` ou `python app.py`) antes de clicar em Send Request.
>
> 💡 **Dica de ordem:** execute o Teste 1 antes do Teste 2. Assim você simula exatamente o que acontece no sistema real — o Raspberry Pi envia o UID, e só depois o app o consulta. O Teste 3 e 4 mostram que um UID novo sobrescreve o anterior.

---

## Checklist — suas rotas estão prontas quando:

- [ ] Teste 1 retorna `200` confirmando que o UID foi armazenado
- [ ] Teste 2 retorna o UID enviado no Teste 1 com `status: "disponivel"`
- [ ] Teste 4 retorna o UID novo enviado no Teste 3 (sobrescrita funcionando)
- [ ] Teste 5 retorna erro `400` (campo ausente)