# 📡 Monitor de Itens

Sistema embarcado com leitor UHF RFID e Raspberry Pi que detecta itens esquecidos na saída de casa, com API REST em Python/Flask, banco de dados SQL e notificações push via aplicativo mobile desenvolvido no Kodular.

---

## 🧩 Sobre o projeto

No cotidiano, esquecer itens essenciais como chaves, carteira ou crachá ao sair de casa é um problema comum. Este sistema monitora automaticamente os itens do usuário no momento da saída, identificando ausências por meio de etiquetas RFID e enviando alertas em tempo real ao smartphone.

---

## 🏗️ Arquitetura

```
Etiquetas RFID
      ↓
Leitor UHF RFID IN-R200
      ↓ (serial via Micro USB)
Raspberry Pi 3  →  Python lê os UIDs
      ↓ (HTTP POST via Wi-Fi)
API Flask (nuvem)
      ↓
Banco de dados SQL
      ↓ (notificação push)
OneSignal  →  App Kodular (smartphone)
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Hardware | Raspberry Pi 3 + Leitor UHF RFID IN-R200 |
| Firmware | Python + pyserial |
| Backend | Python + Flask |
| Banco de dados | SQL |
| App mobile | Kodular |
| Notificações | OneSignal |
| Comunicação | HTTP REST |

---

## 🌿 Branches

| Branch | Responsável | Descrição |
|---|---|---|
| `main` | Carlos Eduardo | Monitoramento geral do projeto |
| `dev/gael` | Gael Chicaro | Área de desenvolvimento individual |
| `dev/heitor` | Heitor Castilho | Área de desenvolvimento individual |
| `dev/caua` | Cauã Lessa | Área de desenvolvimento individual |
| `dev/gustavo` | Gustavo Feitoza | Área de desenvolvimento individual |

---

## 👥 Equipe

- Carlos Eduardo
- Gael Chicaro
- Heitor Castilho
- Cauã Lessa
- Gustavo Feitoza

---

## 🏛️ Instituição

**Instituto Federal de Educação, Ciência e Tecnologia do Sul de Minas Gerais**
Campus Inconfidentes · Curso Técnico em Informática Integrado · Turma 3° Info B · 2026