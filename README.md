# LinkedIn Congratulations Automation 🎉

<img src="./assets/icon.ico" align="right">

## 1. Introdução / Introduction

Este projeto automatiza o envio de felicitações personalizadas para suas conexões do LinkedIn (novo cargo, aniversário de empresa, aniversário pessoal, etc.). 

Utiliza **Python**, **Playwright** e **Inteligência Artificial (Ollama / llama3.2)** local para gerar mensagens diretas, cordiais e profissionais, com suporte a conexões via **CDP (Chrome DevTools Protocol)** e deploy com **PM2**.

---

## 2. Tecnologias Utilizadas 📲

- **Python 3.12+**
- **Playwright (Async API)** - Automação rápida e resiliente de navegadores
- **Ollama AI (llama3.2)** - Modelo de linguagem local para geração inteligente de felicitações
- **Chrome DevTools Protocol (CDP)** - Conexão direta ao seu navegador já aberto na porta `9222`
- **PM2 Process Manager** - Gerenciamento de processos e deploy em segundo plano (`ecosystem.config.js`)
- **python-dotenv** - Gerenciamento de ambientes (`.env` / `.env.prod`)
- **pytest** - Suíte de testes automatizados

---

## 3. Funcionalidades ✔️

- [x] **Conexão via CDP ou Navegador Isolado**: Conecta-se automaticamente ao seu Chrome já aberto na porta 9222 ou abre uma nova instância de navegador.
- [x] **Geração de Mensagens por IA**: Extrai o contexto de cada evento (ex: *"Parabéns pelo novo cargo na empresa X"*) e gera uma mensagem única usando Ollama local.
- [x] **Infinite Scroll Inteligente**: Simula a roldana do mouse (`mouse.wheel`), scroll de DOM e `scrollIntoView` para carregar cartões dinâmicos no Catch-Up do LinkedIn.
- [x] **Filtro de Overlay de Chat**: Evita cliques incorretos ignorando botões contidos nos painéis de mensagem inferiores do LinkedIn.
- [x] **Arquitetura Clean Code**: Código totalmente refatorado com Princípio de Responsabilidade Única (SRP) e nomes de variáveis descritivos.
- [x] **Suporte a PM2**: Facilidade para rodar em produção através do `ecosystem.config.js`.

---

## 4. Instalação e Configuração 🛠️

### 1. Clonar o repositório:
```bash
git clone https://github.com/JoaoG23/Automation-LinkedIn-Congrats-My-Connections.git
cd Automation-LinkedIn-Congrats-My-Connections
```

### 2. Instalar as dependências:
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configurar os arquivos de ambiente (`.env` ou `.env.prod`):
Crie um arquivo `.env` (desenvolvimento) ou `.env.prod` (produção):
```env
MY_ENV="dev"
USER_LINKEDIN="seu_email_linkedin@exemplo.com"
PASSWORD_LINKEDIN="sua_senha_segura"
```

---

## 5. Como Executar 🚀

### Modo Padrão / CDP (Recomendado):
Abra o Chrome com suporte a depuração remota se quiser usar sua sessão ativa:
```bash
chrome.exe --remote-debugging-port=9222
```

Em seguida, execute a aplicação:
```bash
python main.py
```

### Modo Produção com PM2:
```bash
# Iniciar a automação via PM2 no modo produção
pm2 start ecosystem.config.js --env production

# Acompanhar os logs em tempo real
pm2 logs automation-linkedin-congrats-my-connections
```

---

## 6. Estrutura do Projeto 📁

```
Automation-LinkedIn-Congrats-My-Connections/
├── main.py                             # Ponto de entrada oficial da aplicação
├── config.py                           # Carregador flexível de configurações (.env / .env.prod)
├── ecosystem.config.js                 # Configuração de deploy no PM2
├── send_congrats/                      # Módulo principal de felicitações
│   ├── send_congrats.py               # Orquestrador do fluxo de parabéns
│   ├── button_finder.py               # Localização e filtragem rigorosa de botões
│   ├── context_extractor.py           # Extração de texto e contexto dos cards
│   └── chat_messenger.py              # Interação com a caixa de chat e envio
├── utils/                              # Utilitários do sistema
│   ├── scroll_by.py                   # Algoritmo de rolagem e simulação de mouse
│   ├── llm_message.py                 # Integração assíncrona com IA Ollama
│   └── do_login.py                    # Fluxo de login no LinkedIn
├── tests/                              # Suíte de testes e ferramentas de depuração
│   ├── test_llm_message.py            # Testes unitários do gerador de mensagens IA
│   ├── test_cdp.py                    # Teste de conexão CDP com limite reduzido
│   ├── debug_buttons.py               # Ferramenta de inspeção DOM de botões
│   └── dump_buttons.py                # Dump de estrutura HTML para diagnósticos
├── requirements.txt                    # Dependências Python do projeto
└── README.md                           # Documentação oficial
```

---

## 7. Suíte de Testes 🧪

Para rodar os testes unitários da aplicação:
```bash
pytest tests/test_llm_message.py
```

---

## 8. Autor 👨‍💻

<img style="border-radius:50%;" src="https://avatars.githubusercontent.com/u/80895578?v=4" width="100px;" alt="Joao Guilherme"/>

**Joao Guilherme** 🚀

Desenvolvido com 🤖 por João Guilherme 👋🏽 Entre em contato:

[![Linkedin Badge](https://img.shields.io/badge/-Joao%20Guilherme-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/joaog123/)](https://www.linkedin.com/in/joaog123/)  
[![Email Badge](https://img.shields.io/badge/-joaoguilherme94@live.com-c80?style=flat-square&logo=Microsoft&logoColor=white&link=mailto:joaoguilherme94@live.com)](mailto:joaoguilherme94@live.com)

---

## 9. Licença 📄

[![License](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

---

## 10. Aviso Legal ⚠️

Esta ferramenta de automação destina-se apenas a fins educacionais e uso pessoal. Certifique-se de cumprir os Termos de Serviço do LinkedIn. Os autores não se responsabilizam pelo uso indevido desta ferramenta.
