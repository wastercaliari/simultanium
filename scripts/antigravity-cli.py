#!/usr/bin/env python3
"""Antigravity PRO CLI Integration - Simultanium Project"""

import os
import sys
import json
import argparse
import subprocess
import time

# Caminho do CLI Antigravity
AGY_PATH = r"C:\Users\waste\AppData\Local\agy\bin\agy.exe"

def check_agy_available():
    """Verifica se o CLI Antigravity está disponível."""
    if not os.path.exists(AGY_PATH):
        print(f"❌ Erro: CLI Antigravity não encontrado em {AGY_PATH}")
        print("   Instale o CLI: irm https://antigravity.google/cli/install.ps1 | iex")
        return False
    return True

def run_agy_command(prompt, model=None, continue_session=False, conversation_id=None):
    """Executa comando via CLI Antigravity."""
    
    # Construir comando
    cmd = [AGY_PATH]
    
    # Adicionar modelo se especificado
    if model:
        cmd.extend(["--model", model])
    
    # Modo interativo/print
    if continue_session or conversation_id:
        cmd.extend(["--conversation", conversation_id] if conversation_id else [])
    
    # Adicionar prompt
    if prompt:
        # Format: agy -p='prompt' --model name
        cmd.extend(["-p=", f"'{prompt}'"])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n--- stderr ---\n{result.stderr}"
        
        return output, result.returncode
        
    except subprocess.TimeoutExpired:
        return "Timeout expirado (60s)", -1
    except Exception as e:
        return f"Erro ao executar agy: {str(e)}", -1

def list_models():
    """Lista modelos disponíveis via CLI Antigravity."""
    cmd = [AGY_PATH, "models"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout, result.returncode
    except Exception as e:
        return f"Erro: {str(e)}", -1

def main():
    parser = argparse.ArgumentParser(description="Chat com Antigravity PRO")
    parser.add_argument("message", nargs="*", help="Mensagem para enviar ao Antigravity")
    parser.add_argument("--model", default=None, help="Modelo Antigravity para usar")
    parser.add_argument("--list-models", action="store_true", help="Listar modelos disponíveis")
    parser.add_argument("--continue", dest="continue_session", action="store_true", 
                        help="Continuar conversa anterior")
    parser.add_argument("--conversation-id", default=None, help="ID da conversa para retomar")
    parser.add_argument("--interativo", action="store_true", help="Modo interativo contínuo")
    
    args = parser.parse_args()
    
    # Verificar se CLI está disponível
    if not check_agy_available():
        sys.exit(1)
    
    # Listar modelos
    if args.list_models:
        output, rc = list_models()
        print(f"Modelos Antigravity disponíveis:\n{output}")
        sys.exit(0)
    
    # Determinar modelo
    model = args.model or os.environ.get('DEFAULT_ANTIGRAVITY_MODEL', 'gemini-4-hydrogen-high')
    
    # Mensagem única
    if not args.message:
        parser.print_help()
        sys.exit(1)
    
    message = " ".join(args.message)
    
    print(f"🛰️  Enviando para Antigravity PRO ({model})...")
    print(f"   (Cota separada da AI Studio - seu plano PRO)")
    
    output, rc = run_agy_command(message, model=model)
    
    print(f"\n🤖 Resposta Antigravity PRO ({model}):")
    print(f"  {output}")
    
    if rc != 0:
        print(f"\n⚠️  Código de saída: {rc}")
        print("   Pode ser problema de login ou cota expirada.")

if __name__ == "__main__":
    main()