# Simultanium

Projeto que permite o uso **separado e simultâneo** de duas cotas Google:
1. **Google AI Studio** - Cota da API Gemini (`gemini-3.5-flash`, `gemma-4-26b-a4b-it`, etc.)
2. **Google Antigravity PRO** - Cota separada dos modelos `gemini-4-hydrogen-*` e outros modelos (Claude, GPT-OSS, etc.)

## 🎯 Objetivo

Permitir que o usuário use **ambos os sistemas simultaneamente**, consumindo cotas separadas.
- Se a cota do Antigravity acabar, ainda temos o Gemini (e vice-versa).

## 🛠️ Instalação Rápida

```powershell
# 1. Clonar o repositório
git clone https://github.com/wastercaliari/simultanium.git
cd Simultanium

# 2. Executar setup
.\run_setup.bat
```

## 🚀 Usando o Simultanium

### Opção 1: Auto (testa os 3 métodos)
```powershell
python scripts/gemini-chat.py "Olá! Quem é você?"
```
*O script tentará automaticamente: API Direta → Interface Web → Antigravity CLI*

### Opção 2: Método Específico
```powershell
# API Direta (Google AI Studio)
python scripts/gemini-chat.py --method api_direct "Olá!"

# Interface Web (gemini-4-neon)
python scripts/gemini-chat.py --method web_interface "Olá!"

# Antigravity PRO (cota separada)
python scripts/gemini-chat.py --method antigravity_cli "Olá!"
```

### Opção 3: Listar Modelos
```powershell
python scripts/gemini-chat.py --list-models
```

## 📋 Como Funciona

O projeto tenta **três métodos** automaticamente em ordem:

1. **API Direta** (`api_direct`)
   - Usa sua chave `api google gemin.txt`
   - Modelos: `gemini-3.5-flash`, `gemma-4-26b-a4b-it`
   - ⚠️ Alguns modelos têm quota Free Tier limitada

2. **Interface Web** (`web_interface`)
   - Acesse `gemini.google.com` com sua conta Google
   - Modelos: `gemini-4-neon` (você já testou enviando "Oi"!)
   - ✅ Sua conta tem cota disponível na web

3. **Antigravity CLI** (`antigravity_cli`)
   - CLI `agy` instalado em `%APPDATA%\\Local\\agy\\bin\\`
   - Modelos: `gemini-4-hydrogen-high`, `claude-sonnet-4-6`, etc.
   - ✅ Cota **separada** do seu plano PRO

## 📋 Após o Clone

1. **Executar** `.\\run_setup.bat`
2. **Etapa 1**: Informar a chave AI Studio (ou variável de ambiente `GEMINI_API_KEYS`)
3. **Etapa 2**: Informar conta Antigravity (`SUA_CONTA_AQUI` ou outra)
4. **Pronto!** O sistema mapeará automaticamente todos os modelos disponíveis

## 💡 Principais Lições

- **Cotas separadas**: AI Studio e Antigravity PRO têm cotas independentes
- **Flexibilidade**: Use o método que melhor se adapta à sua necessidade
- **Automação**: O script tenta os métodos automaticamente em ordem
- **Resiliência**: Se uma cota acabar, o outro ainda funciona

## 📞 Suporte

- Problemas com instalação: abuse do `.\\run_setup.bat`
- Dúvidas de modelo: consulte o `mapa_modelos.json` gerado após o setup
- Conta Antigravity: Docs em `https://antigravity.google/cli/install.sh`

---

**Strela: Use o Simultanium para nunca mais ficar sem cota de AI!**