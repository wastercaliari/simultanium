# Simultanium

Projeto que permite o uso **separado e simultâneo** de duas cotas Google:
1. **Google AI Studio** - Cota gratuita/paga dos modelos Gemini (`gemini-3.5-flash`, `gemma-4-26b-a4b-it`, etc.)
2. **Google Antigravity PRO** - Cota separada dos modelos `gemini-4-hydrogen-*` e outros modelos (Claude, GPT-OSS, etc.)

## Objetivo

Quando o usuário clonar este repositório, a LLM perguntará:
1. Qual chave de API do Google AI Studio deseja usar (ou gerar uma nova)
2. Qual conta Google tem o plano Antigravity PRO ativo

Depois de configurado, você pode usar ambos os modelos simultaneamente, consumindo cotas separadas.

## Estrutura

```
Simultanium/
├── config/
│   ├── ai_studio.env        # Chave da API Google AI Studio
│   └── antigravity.json     # Configuração da conta PRO
├── scripts/
│   ├── gemini-chat.py       # Chat usando AI Studio
│   └── antigravity-cli.py # Integração com CLI Antigravity
├── .webridge/
│   └── credenciais.txt      # Credenciais do Antigravity (já configurado globalmente)
└── README.md                # Este arquivo
```

## Instalação

### 1. Clonar o repositório
```powershell
git clone https://seu-repositorio/Simultanium.git
cd Simultanium
```

### 2. Configurar as APIs

O projeto vai te perguntar duas coisas:

#### A) Chave da API Google AI Studio
- Você já tem uma chave em: `C:\Users\waste\OneDrive\Documentos\Projeto Padrão\api google gemin.txt`
- Ou pode gerar uma nova em: https://aistudio.google.com/
- O projeto vai salvar em `config/ai_studio.env`

#### B) Conta Google Antigravity PRO
- O CLI `agy` já está instalado em: `C:\Users\waste\AppData\Local\agy\bin\agy.exe`
- O projeto vai usar as credenciais salvas globalmente em `~/.webridge/credenciais.txt`
- Ou você pode logar novamente: `agy.exe login`

### 3. Usar o projeto

Após a configuração, você tem dois comandos principais:

#### Usar Google AI Studio (Gemini)
```powershell
python scripts/gemini-chat.py "Sua mensagem aqui"
```
- Consome da cota AI Studio
- Modelos: `gemini-3.5-flash`, `gemma-4-26b-a4b-it`

#### Usar Antigravity PRO
```powershell
# Via CLI direto
agy -p='Sua mensagem aqui' --model gemini-4-hydrogen-high

# Ou via script Python (quando integrado)
python scripts/antigravity-cli.py "Sua mensagem aqui" --model gemini-4-hydrogen-high
```
- Consome da cota PRO do Antigravity
- Modelos: `gemini-4-hydrogen-high`, `gemini-4-hydrogen-low`, etc.

## Configuração Inicial (What the LLM should ask)

Quando você clonar e abrir o projeto, a LLM deve perguntar:

1. **"Qual chave de API do Google AI Studio você deseja usar?"
   - Você já tem em `C:\Users\waste\OneDrive\Documentos\Projeto Padrão\api google gemin.txt`
   - Ou deseja gerar uma nova em https://aistudio.google.com/?
   
2. **"Qual conta Google tem o plano Antigravity PRO ativo?"
   - Já temos `wasterlucas.ia@gmail.com` logado via Webridge/CLI
   - Ou deseja usar outra conta?
   - Lembre-se: a cota do Antigravity é separada da cota AI Studio"

## Comandos Úteis

```powershell
# Ver modelos AI Studio disponíveis
python scripts/gemini-chat.py --list-models

# Ver modelos Antigravity disponíveis
agy models

# Testar AI Studio
python scripts/gemini-chat.py "Olá, quem são você?"

# Testar Antigravity PRO
agy -p='Olá, quem são você?' --model gemini-4-hydrogen-high
```