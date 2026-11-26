#!/usr/bin/env python3
"""
Setup script para o projeto Simultanium.
Quando o usuario clona o repo, esta script roda e pergunta:
1. Qual chave API Google AI Studio usar
2. Qual conta Google para conectar o plano PRO do Antigravity
"""

import os
import sys
import json
import locale

# Force UTF-8 output if possible
if sys.stdout.encoding != 'UTF-8':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except:
        pass

print("=" * 60)
print("BEM-VINDO AO SIMULTANIUM")
print("=" * 60)
print()
print("Este projeto conecta simultaneamente duas cotas Google:")
print("  1. Google AI Studio (modelos Gemini)")
print("  2. Google Antigravity PRO (modelos específicos)")
print()
print("A cota de cada um e SEPARADA. Voce pode usar um ou ambos.")
print()

def configurar_ai_studio():
    """Pergunta e configura a chave da API Google AI Studio."""
    print("--- 1/2: Configuracao Google AI Studio ---")
    print()

    key_path = r"C:\Users\waste\OneDrive\Documentos\Projeto Padrão\api google gemin.txt"

    if os.path.exists(key_path):
        try:
            with open(key_path, 'r', encoding='utf-8') as f:
                chave_existente = f.read().strip()
            print("Chave existente encontrada no projeto:")
            print("  Caminho: " + key_path)
            print("  (Primeiros caracteres: " + chave_existente[:20] + "...)")
            print()
        except Exception as e:
            print("Erro ao ler chave existente: " + str(e))
            chave_existente = None
    else:
        print("Nenhuma chave existente encontrada no projeto.")
        chave_existente = None

    print()
    usar_existente = input("Deseja usar esta chave existente? (S/n): ").strip().lower()
    if usar_existente in ['', 's', 'sim', 'y', 'yes']:
        if chave_existente:
            print("Usando chave existente: " + chave_existente[:20] + "...")
            return chave_existente

    print()
    print("Para obter uma nova chave:")
    print("  1. Acesse: https://aistudio.google.com/")
    print("  2. Faça login com sua conta Google")
    print("  3. Clique em 'API keys' -> 'Create API key'")
    print("  4. Copie a chave gerada")
    print()

    nova_chave = input("Cole aqui sua chave de API Google AI Studio: ").strip()

    if nova_chave:
        try:
            with open(key_path, 'w', encoding='utf-8') as f:
                f.write(nova_chave)
            print("Chave salva em: " + key_path)
            return nova_chave
        except Exception as e:
            print("Erro ao salvar chave: " + str(e))
            return None
    else:
        print("Sem chave fornecida. Usando variavel de ambiente.")
        return None

def configurar_antigravity():
    """Pergunta e configura a conta Antigravity PRO."""
    print()
    print("--- 2/2: Configuracao Google Antigravity PRO ---")
    print()

    agy_path = r"C:\Users\waste\AppData\Local\agy\bin\agy.exe"

    if os.path.exists(agy_path):
        print("CLI Antigravity encontrado em:")
        print("  " + agy_path)
        print()

    print("Conta utilizada anteriormente: wasterlucas.ia@gmail.com")
    print("   (Login via Webridge/CLI ja realizado com sucesso)")
    print()

    usar_anterior = input("Deseja usar esta conta anterior? (S/n): ").strip().lower()
    if usar_anterior in ['', 's', 'sim', 'y', 'yes']:
        print("Usando conta: wasterlucas.ia@gmail.com")
        return "wasterlucas.ia@gmail.com"

    print()
    print("Para logar no Antigravity PRO:")
    print("   O CLI ja foi instalado via: irm https://antigravity.google/cli/install.ps1 | iex")
    print("   O login pode ser feito interativamente ou com credenciais salvas.")
    print()

    cred_path = os.path.expanduser("~/.webridge/credenciais.txt")
    if os.path.exists(cred_path):
        print("Credenciais globais encontradas em: " + cred_path)
        try:
            with open(cred_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            if "[antigravity.google.com]" in conteudo:
                print("   Seção [antigravity.google.com] encontrada")
        except:
            pass

    conta = input("Digite seu e-mail Google para Antigravity PRO: ").strip()

    if conta:
        print("Conta registrada: " + conta)
        print("   Para logar definitivo, rode: agy login (ou use o Webridge)")
        return conta

    return None

def atualizar_configuracao(ai_key, antigravity_account):
    """Atualiza os arquivos de configuração do projeto."""
    print()
    print("--- Atualizando arquivos de configuracao ---")
    print()

    # Atualizar config/ai_studio.env
    env_path = r"Simultanium/config/ai_studio.env"
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            conteudo_atualizado = conteudo.replace(
                'GEMINI_API_KEY=sua-chave-aqui',
                'GEMINI_API_KEY=' + ai_key
            )

            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(conteudo_atualizado)
            print("   Configuracao AI Studio atualizada em: " + env_path)
        except Exception as e:
            print("   Erro ao atualizar AI Studio: " + str(e))

    # Atualizar config/antigravity.json
    antigrav_path = r"Simultanium/config/antigravity.json"
    if os.path.exists(antigrav_path):
        try:
            with open(antigrav_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            config['user_account'] = antigravity_account
            config['last_updated'] = __import__('datetime').datetime.now().strftime('%Y-%m-%d')

            with open(antigrav_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print("   Configuracao Antigravity atualizada em: " + antigrav_path)
        except Exception as e:
            print("   Erro ao atualizar Antigravity: " + str(e))

    print()
    print("=" * 60)
    print("CONFIGURACAO CONCLUIDA!")
    print("=" * 60)
    print()
    print("Resumo da configuracao:")
    print("   • Google AI Studio: " + ("OK" if ai_key else "N/A"))
    print("   • Google Antigravity PRO: " + ("OK" if antigravity_account else "N/A"))
    print()
    print("Proximos passos:")
    print("   1. Testar AI Studio: python scripts/gemini-chat.py 'Olá'")
    print("   2. Testar Antigravity: agy -p='Olá' --model gemini-4-hydrogen-high")
    print("   3. Usar ambos simultaneamente (cotas separadas!)")
    print()

def main():
    try:
        # Etapa 1: Configurar AI Studio
        print("Iniciando configuracao do Simultanium...")
        print()

        ai_key = configurar_ai_studio()
        if not ai_key:
            print("⚠️  AVISO: Sem chave AI Studio, algumas funcionalidades podem nao funcionar.")
            print()

        # Etapa 2: Configurar Antigravity PRO
        antigravity_account = configurar_antigravity()
        if not antigravity_account:
            print("⚠️  AVISO: Sem conta Antigravity configurada, modelo PRO nao disponivel.")
            print()

        # Etapa 3: Salvar configurações
        print()
        atualizar_configuracao(ai_key, antigravity_account)

    except KeyboardInterrupt:
        print()
        print("⚠️  Configuracao interrompida pelo usuario.")
        sys.exit(1)
    except Exception as e:
        print()
        print("❌ Erro durante configuracao: " + str(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()