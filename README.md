<div align="center">

# Outlook Fusion

### *Terminal-First Calendar Management for Developers*

[![Rust](https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Microsoft Graph](https://img.shields.io/badge/Microsoft_Graph-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://developer.microsoft.com/graph)

**Outlook Fusion** é uma ferramenta de linha de comando poderosa e eficiente para desenvolvedores que desejam gerenciar seus calendários do Outlook diretamente do terminal.

[Features](#features) • [Arquitetura](#arquitetura) • [Instalação](#instalação) • [Configuração](#configuração) • [Uso](#uso) • [Licença](#licença)

</div>

---

## Features

- **Performance**: Core em Rust para máxima velocidade
- **Interface Intuitiva**: TUI (Terminal User Interface) em Python
- **Seguro**: Integração direta com Microsoft Graph API
- **Gestão Completa**: Crie e gerencie eventos no Outlook Calendar
- **Developer-First**: Perfeito para workflows de terminal

---

## Arquitetura

```
┌─────────────────────────────────────────────┐
│                                             │
│              Usuário                        │
│                                             │
└──────────────────┬──────────────────────────┘
                   │
                   │  Interação via Terminal
                   │
        ┌──────────▼─────────────┐
        │                        │
        │    Python TUI          │
        │    (src/TUI/)          │
        │                        │
        │  • Interface amigável  │
        │  • Validação de dados  │
        │  • Menus interativos   │
        │                        │
        └──────────┬─────────────┘
                   │
                   │  Chamadas de Processo
                   │
        ┌──────────▼─────────────┐
        │                        │
        │    Rust Core           │
        │    (src/core/)         │
        │                        │
        │  • API Controller      │
        │  • Calendar Service    │
        │  • Validação de datas  │
        │                        │
        └──────────┬─────────────┘
                   │
                   │  HTTP Requests (Bearer Token)
                   │
        ┌──────────▼─────────────┐
        │                        │
        │   Microsoft Graph      │
        │       API              │
        │                        │
        │  • Autenticação OAuth  │
        │  • Outlook Calendar    │
        │                        │
        └────────────────────────┘
```

### Componentes

#### **Rust Core** (`src/core/`)
O núcleo da aplicação, responsável por:
- Comunicação direta com a Microsoft Graph API
- Parsing de argumentos CLI com `clap`
- Criação e gerenciamento de eventos no calendário
- Validação de datas e fusos horários

#### **Python TUI** (`src/TUI/`)
Interface de usuário no terminal que:
- Fornece uma experiência interativa e amigável
- Gerencia módulos e dependências
- Chama o core Rust com os parâmetros corretos

---

## Instalação

### Pré-requisitos

- **Rust** (1.70+): [Instalar Rust](https://rustup.rs/)
- **Python** (3.8+): [Instalar Python](https://www.python.org/downloads/)
- **Cargo**: Incluído com Rust
- **Conta Microsoft**: Com acesso ao Outlook

### Clone o Repositório

```bash
git clone https://github.com/seu-usuario/OutlookFusion.git
cd OutlookFusion
```

### Build do Core Rust

```bash
cd src/core
cargo build --release
```

### Dependências Python

```bash
cd ../TUI
pip install -r requirements/requirements.txt
```

---

## Configuração

### Obtendo o Token Microsoft Graph

Para usar o Outlook Fusion, você precisa de um token de acesso da Microsoft Graph API:

1. **Acesse o [Microsoft Graph Explorer](https://developer.microsoft.com/graph/graph-explorer)**

2. **Faça login** com sua conta Microsoft/Office 365

3. **Obtenha o Access Token**:
   - Clique no seu perfil no canto superior direito
   - Selecione "Access token"
   - Copie o token gerado

   > **Importante**: Este token expira após algum tempo. Para uso em produção, configure um [Azure App Registration](https://learn.microsoft.com/graph/auth-register-app-v2) para obter tokens de longa duração.

### Configurando o arquivo `.env`

Crie um arquivo `.env` no diretório `src/core/src/`:

```bash
cd src/core/src
touch .env
```

Adicione seu token ao arquivo:

```env
OUTLOOK_TOKEN=seu_token_aqui
```

**Estrutura esperada**:
```
OutlookFusion/
└── src/
    └── core/
        └── src/
            └── .env  ← Seu arquivo aqui
```

> **Segurança**: Nunca commite o arquivo `.env` no git. Ele já está no `.gitignore`.

---

## Uso

### Via Core Rust (CLI Direto)

```bash
cd src/core
cargo run -- \
  --subject "Reunião de Planning" \
  --descr "Discutir sprint goals" \
  --content "Participantes: Time Dev" \
  --date-start "2026-02-10T14:00:00-03:00" \
  --date-end "2026-02-10T15:00:00-03:00" \
  --timezone "America/Sao_Paulo" \
  --location "Online"
```

### Via Python TUI (Interface Interativa)

```bash
cd src/TUI
python index.py
```

### Parâmetros Disponíveis

| Parâmetro | Flag | Descrição | Obrigatório |
|-----------|------|-----------|-------------|
| Subject | `-s, --subject` | Assunto do evento | Sim |
| Description | `-d, --descr` | Descrição detalhada | Não |
| Content | `-c, --content` | Conteúdo do evento | Sim |
| Date Start | `--date-start` | Data/hora início (ISO8601) | Sim |
| Date End | `--date-end` | Data/hora fim (ISO8601) | Sim |
| Timezone | `-t, --timezone` | Fuso horário (default: America/Sao_Paulo) | Não |
| Location | `-l, --location` | Local (default: Online) | Não |

### Exemplos de Formato de Data

```bash
# Com timezone explícito
--date-start "2026-02-15T09:00:00-03:00"

# UTC
--date-start "2026-02-15T12:00:00Z"

# Outros formatos ISO8601
--date-start "2026-02-15T09:00:00-03:00"
```

---

## Desenvolvimento

### Estrutura do Projeto

```
OutlookFusion/
├── src/
│   ├── core/                    # Rust backend
│   │   ├── src/
│   │   │   ├── main.rs         # Entry point
│   │   │   ├── api_controller.rs
│   │   │   └── services/
│   │   │       └── calendar_service.rs
│   │   └── Cargo.toml
│   │
│   └── TUI/                     # Python frontend
│       ├── index.py             # Entry point
│       ├── data.py
│       ├── tool.py
│       └── requirements/
│           └── requirements.txt
│
├── README.md
└── LICENSE
```

### Tecnologias Utilizadas

**Rust Core**:
- `clap` - Argument parsing
- `reqwest` - HTTP client
- `tokio` - Async runtime
- `serde_json` - JSON serialization
- `chrono` - Date/time handling
- `dotenvy` - Environment variables

**Python TUI**:
- `asyncio` - Async operations
- Standard library modules

---

## Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:

1. Fork o projeto
2. Criar uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abrir um Pull Request

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Troubleshooting

### Erro: "OUTLOOK_TOKEN environment variable not found"
- Verifique se o arquivo `.env` existe em `src/core/src/.env`
- Confirme que a variável está definida: `OUTLOOK_TOKEN=seu_token`

### Erro de Autenticação
- Seu token pode ter expirado. Gere um novo no Graph Explorer
- Verifique se sua conta tem permissões para criar eventos no calendário

### Erro de Compilação Rust
```bash
cargo clean
cargo build --release
```

---

<div align="center">

**Feito para desenvolvedores que vivem no terminal**

*"E tudo o que fizerem, seja em palavra ou em ação, façam em nome do Senhor Jesus."*  
— Colossenses 3:17

[⬆ Voltar ao topo](#outlook-fusion)

</div>
