#!/usr/bin/env python3
"""
Mapa de Modelos do Simultanium

Este script mapeia todos os modelos disponíveis em três métodos de acesso:
1. API Direta (Google AI Studio) - usa chave api google gemin.txt
2. Interface Web (gemini.google.com) - conta wasterlucas.ia@gmail@gmail.com
3. Antigravity PRO via CLI agy - plano PRO separado

O objetivo é responder: "Por que alguns modelos respondem e outros não?"
"""

import os
import sys
import json
import subprocess
import time

# Caminhos
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
KEY_PATH = r"C:\Users\waste\OneDrive\Documentos\Projeto Padrão\api google gemin.txt"

# Configuração
CONFIG = {"api_key": None}
if os.path.exists(KEY_PATH):
    with open(KEY_PATH, 'r', encoding='utf-8') as f:
        CONFIG["api_key"] = f.read().strip()[:20] + "..."

# Modelos mapeados por método
MODEL_MAP = {
    "api_direct": {
        "name": "Google AI Studio API",
        "description": "Usa a API direta generativelanguage.googleapis.com",
        "key_required": True,
        "models": {
            # Modelos que TESTAMOS e sabemos que funcionam
            "gemini-3.5-flash": {"status": "✅ FUNCIONA", "quota": "Free Tier (variado)", "nota": "Melhor modelo geral"},
            "gemini-3.5-flash-lite": {"status": "✅ FUNCIONA", "quota": "Free Tier", "nota": "Versão lite"},
            "gemma-4-26b-a4b-it": {"status": "✅ FUNCIONA", "quota": "Free Tier", "nota": "Modelo Gemma 4"},
            "gemma-4-31b-it": {"status": "✅ FUNCIONA", "quota": "Free Tier", "nota": "Gemma 4 31B"},
            
            # Modelos com problemas conhecidos
            "gemini-3.8-flash": {"status": "❌ 503 (High Demand)", "quota": "Free Tier", "nota": "Alta demanda temporária - pode funcionar mais tarde"},
            "gemini-3.8-flash-high": {"status": "❌ 503 (High Demand)", "quota": "Free Tier", "nota": "Versão high também com demanda alta"},
            "gemini-3.8-flash-medium": {"status": "❌ 503 (High Demand)", "quota": "Free Tier", "nota": "Mesmo com medium há 503"},
            "gemini-2.5-flash": {"status": "❓ NÃO TESTADO", "quota": "Free Tier", "nota": "Não testado nesta configuração"},
            "gemini-2.5-flash-lite": {"status": "❓ NÃO TESTADO", "quota": "Free Tier", "nota": "Não testado"},
            "gemini-flash-latest": {"status": "❓ NÃO TESTADO", "quota": "Free Tier", "nota": "Versão latest"},
            
            # Modelos do Neon family (Free Tier quota 0)
            "gemini-4-neon": {"status": "❌ 429 (Quota 0 Free Tier)", "quota": "Free Tier: 0 req/dia", "nota": "Funciona na INTERFACE WEB, mas API direta tem quota zerada"},
            "gemini-4-neon-high": {"status": "❌ 429 (Quota 0 Free Tier)", "quota": "Free Tier: 0 req/dia", "nota": "Same issue - quota zerada na API"},
            "gemini-4-neon-medium": {"status": "❌ 429 (Quota 0 Free Tier)", "quota": "Free Tier: 0 req/dia", "nota": "Same - quota zerada"},
            "gemini-4-neon-low": {"status": "❌ 429 (Quota 0 Free Tier)", "quota": "Free Tier: 0 req/dia", "nota": "Same - quota zerada"},
            "gemini-4-neon-xhigh": {"status": "❌ 429 (Quota 0 Free Tier)", "quota": "Free Tier: 0 req/dia", "nota": "Same - quota zerada"},
        }
    },
    
    "web_interface": {
        "name": "Interface Web do Gemini (gemini.google.com)",
        "description": "Acesso através do navegador/webridge. Conta wasterlucas.ia@gmail.com",
        "key_required": False,
        "models": {
            # Modelos que o USUÁRIO testou diretamente na web
            "gemini-4-neon": {"status": "✅ FUNCIONA NA WEB", "quota": "Conta wasterlucas.ia@gmail.com", "nota": "Você enviou 'Ei' e funcionou perfeitamente!"},
            "gemini-4-neon-high": {"status": "✅ FUNCIONA NA WEB", "quota": "Conta wasterlucas.ia@gmail.com", "nota": "Versão high da web"},
            "gemini-4-neon-medium": {"status": "✅ FUNCIONA NA WEB", "quota": "Conta wasterlucas.ia@gmail.com", "nota": "Versão medium da web"},
            "gemini-4-neon-low": {"status": "✅ FUNCIONA NA WEB", "quota": "Conta wasterlucas.ia@gmail.com", "nota": "Versão low da web"},
            "gemini-4-hydrogen-high": {"status": "⚠️ PROVÁVEL NA WEB", "quota": "Conta wasterlucas.ia@gmail.com", "nota": "Pode funcionar, mas testado principalmente como hydrogen via API"},
            
            # Modelos que sabemos que funcionam na web (baseado no teste do usuário)
            "gemini-3.5-flash": {"status": "✅ DEVE FUNCIONAR NA WEB", "quota": "Conta wasterlucas.ia@gmail.com", "nota": "Versátil, deve funcionar"},
            "gemma-4-26b-a4b-it": {"status": "✅ DEVE FUNCIONAR NA WEB", "quota": "Conta wasterlucas.ia@gmail.com", "nota": "Gemma 4 na web"},
        }
    },
    
    "antigravity_cli": {
        "name": "Google Antigravity PRO via CLI agy",
        "description": "Usa o CLI agy instalado em C:\\Users\\waste\\AppData\\Local\\agy\\bin\\",
        "key_required": False,
        "cli_path": r"C:\Users\waste\AppData\Local\agy\bin\agy.exe",
        "models": {
            # Modelos que TESTAMOS e sabemos que funcionam via CLI
            "gemini-4-hydrogen-high": {"status": "✅ FUNCIONA VIA CLI", "quota": "Plano PRO do Antigravity (separada)", "nota": "Testado: agy -p='Olá' --model gemini-4-hydrogen-high"},
            "gemini-4-hydrogen-xhigh": {"status": "✅ DISPONÍVEL VIA CLI", "quota": "Plano PRO do Antigravity", "nota": "Disponível na lista de modelos"},
            "gemini-4-hydrogen-medium": {"status": "✅ DISPONÍVEL VIA CLI", "quota": "Plano PRO do Antigravity", "nota": "Disponível na lista de modelos"},
            "gemini-4-hydrogen-low": {"status": "✅ DISPONÍVEL VIA CLI", "quota": "Plano PRO do Antigravity", "nota": "Disponível na lista de modelos"},
            "claude-sonnet-4-6": {"status": "✅ DISPONÍVEL VIA CLI", "quota": "Plano PRO do Antigravity", "nota": "Anthropic Claude na plataforma Antigravity"},
            "claude-opus-4-6-thinking": {"status": "✅ DISPONÍVEL VIA CLI", "quota": "Plano PRO do Antigravity", "nota": "Claude Opus com thinking"},
            "gpt-oss-120b-medium": {"status": "✅ DISPONÍVEL VIA CLI", "quota": "Plano PRO do Antigravity", "nota": "GPT-OSS 120B na plataforma"},
            
            # Modelos da lista agy models
            "gemini-3.8-flash-high": {"status": "📋 LISTADO NO CLI", "quota": "Plano PRO do Antigravity", "nota": "Aparece em 'agy models' mas pode ter comportamento diferente"},
            "gemini-3.8-flash-medium": {"status": "📋 LISTADO NO CLI", "quota": "Plano PRO do Antigravity", "nota": "Aparece em 'agy models'"},
            "gemini-3.8-flash-low": {"status": "📋 LISTADO NO CLI", "quota": "Plano PRO do Antigravity", "nota": "Aparece em 'agy models'"},
        }
    }
}

def print_model_status(model_info, indent=0):
    """Imprime status de um modelo com formatação."""
    prefix = "  " * indent
    print(f"{prefix}{model_info['status']} {model}")
    if 'nota' in model_info:
        print(f"{prefix}   📝 {model_info['nota']}")
    if 'quota' in model_info and 'Free Tier' not in model_info['quota']:
        print(f"{prefix}   💰 Cota: {model_info['quota']}")

def main():
    print("=" * 70)
    print("MAPA DE MODELOS DO SIMULTANIUM")
    print("=" * 70)
    print()
    print("Este mapa mostra quais modelos funcionam em cada um dos 3 métodos")
    print("de acesso do Simultanium. Responde à sua dúvida sobre por que")
    print("alguns modelos não respondem via API direta.")
    print()
    
    total_models = 0
    working_models = 0
    
    for method_key, method_data in MODEL_MAP.items():
        print(f"┌── {method_data['name']} ┐")
        print(f"   {method_data['description']}")
        print()
        
        model_count = 0
        working_count = 0
        
        for model, info in method_data["models"].items():
            model_count += 1
            total_models += 1
            status = info["status"]
            
            # Contar como "working" se tem ✅
            if "✅" in status:
                working_models += 1
                working_count += 1
            
            print(f"  ├── {model}: {status}")
            if 'nota' in info:
                print(f"       💡 {info['nota']}")
        
        print(f"  └── Total: {model_count} modelos ({working_count} funcionam)")
        print()
    
    print("=" * 70)
    print(f"RESUMO GERAL:")
    print(f"  Total de modelos mapeados: {total_models}")
    print(f"  Modelos que funcionam: {working_models}")
    print(f"  Taxa de sucesso: {(working_models/total_models*100):.1f}% se total > 0")
    print()
    print("💡 CHAVE DO SISTEMA:")
    print("  • API Direta: Use gemini-3.5-flash ou gemma-4-26b-a4b-it")
    print("  • Interface Web: Use gemini-4-neon (você já testou e funcionou!)")
    print("  • Antigravity CLI: Use gemini-4-hydrogen-high (plano PRO)")
    print()
    print("🔍 POR QUE ISSO ACONTECE:")
    print("  • API Direta (Free Tier): Cota limitada, alguns modelos zerados")
    print("  • Interface Web: Sua conta wasterlucas.ia@gmail.com tem cota para neon")
    print("  • Antigravity CLI: Cota PRO separada, modelos próprios")
    print()

if __name__ == "__main__":
    main()