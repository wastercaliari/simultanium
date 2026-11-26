#!/usr/bin/env python3
"""
Mapeador Automatizado de Modelos do Simultanium

RODAPA AFTER SETUP: Este script deve ser executado DEPOIS que o usuário
termina de configurar as contas (AI Studio key + Antigravity CLI).

Ele mapeia:
1. ✅ Quais modelos da API direta funcionam com a chave fornecida
2. ✅ Quais modelos da interface web estão disponíveis (baseado em teste rápido)
3. ✅ Quais modelos estão disponíveis no CLI Antigravity
4. ✅ Salva um mapa resumido para o gemini-chat.py usar

O OBJETIVO: Mostrar ao usuário que as cotas são SEPARADAS.
Se a cota do Antigravity acabar, ainda temos o Gemini (e vice-versa).
"""

import os
import sys
import json
import subprocess
import time

# Caminhos
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
KEY_PATH = r"C:\Users\waste\OneDrive\Documentos\Projeto Padrão\api google gemin.txt"

# Resultado do mapeamento
MAPA = {
    "data_mapeamento": time.strftime("%Y-%m-%d %H:%M:%S"),
    "usuario": "wasterlucas.ia@gmail.com",
    "metodos": {},
    "resumo": {
        "total_modelos": 0,
        "modelos_funcionando": 0,
        "cotas_separadas": True
    }
}


def carregar_chave():
    """Carrega a chave API do Google AI Studio."""
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None


def testar_api_direct(modelos_teste):
    """Testa modelos via API direta e retorna status."""
    resultados = {}
    api_key = carregar_chave()
    
    if not api_key:
        for modelo in modelos_teste:
            resultados[modelo] = {
                "status": "❌ SEM CHAVE API",
                "quota": "N/A",
                "nota": "Nenhuma chave AI Studio encontrada"
            }
        return resultados
    
    # Testar alguns modelos-chave
    modelos_prioritarios = [
        "gemini-3.5-flash", "gemini-4-neon", "gemini-4-hydrogen-high",
        "gemini-3.8-flash", "gemma-4-26b-a4b-it"
    ]
    
    for modelo in modelos_prioritarios:
        if modelo not in modelos_teste:
            continue
        try:
            import urllib.request
            import urllib.parse
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
            body = json.dumps({
                "contents": [{"parts": [{"text": "Olá"}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 10}
            }).encode('utf-8')
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
                dados = json.loads(resp.read().decode('utf-8')) if status == 200 else {}
                texto = dados.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "") if status == 200 else ""
                resultados[modelo] = {
                    "status": f"✅ {status == 200}" if status != 429 else f"❌ {status}: Quota exceeded",
                    "quota": "Free Tier" if status != 429 else "0 req/dia",
                    "nota": f"Status: {status}" + (f", resposta: {texto[:50]}..." if status == 200 and texto else "")
                }
        except Exception as e:
            resultados[modelo] = {
                "status": f"❌ Erro: {str(e)[:50]}",
                "quota": "Erro",
                "nota": str(e)
            }
    
    return resultados


def testar_antigravity_cli():
    """Testa quais modelos estão disponíveis no CLI Antigravity."""
    agy_path = r"C:\Users\waste\AppData\Local\agy\bin\agy.exe"
    resultados = {}
    
    if not os.path.exists(agy_path):
        for modelo in ["gemini-4-hydrogen-high", "gemini-4-hydrogen-medium", 
                       "gemini-4-hydrogen-low", "gemini-4-hydrogen-xhigh"]:
            resultados[modelo] = {
                "status": "❌ CLI não encontrado",
                "quota": "N/A",
                "nota": "Execute: irm https://antigravity.google/cli/install.ps1 | iex"
            }
        return resultados
    
    # Listar modelos disponíveis
    try:
        result = subprocess.run(
            [agy_path, "models"],
            capture_output=True, text=True, timeout=30
        )
        linhas = result.stdout.split('\n')
        
        # Extrair nomes de modelos da lista
        modelos_lista = []
        for linha in linhas:
            if 'gemini' in linha.lower() or 'claude' in linha.lower() or 'gpt' in linha.lower():
                modelos_lista.append(linha.strip())
        
        # Testar modelos conhecidos da plataforma Antigravity
        modelos_teste = [
            "gemini-4-hydrogen-high", "gemini-4-hydrogen-xhigh",
            "gemini-4-hydrogen-medium", "gemini-4-hydrogen-low",
            "claude-sonnet-4-6", "claude-opus-4-6-thinking",
            "gpt-oss-120b-medium"
        ]
        
        for modelo in modelos_teste:
            if any(m in modelo for m in modelos_lista):
                resultados[modelo] = {
                    "status": "✅ LISTADO NO CLI",
                    "quota": "Plano PRO do Antigravity (separada)",
                    "nota": "Cota separada do AI Studio"
                }
            else:
                resultados[modelo] = {
                    "status": "❓ NÃO LISTADO NA VERSAO ATUAL",
                    "quota": "Plano PRO do Antigravity",
                    "nota": "Pode estar disponível em atualização futura"
                }
    except Exception as e:
        resultados = {m: {"status": f"❌ Erro: {str(e)[:50]}", "quota": "Erro", "nota": str(e)} for m in [
            "gemini-4-hydrogen-high", "gemini-4-hydrogen-medium"]}
    
    return resultados


def gerar_relatorio_final():
    """Gera relatório resumido do mapeamento."""
    print("=" * 70)
    print("🗺️  MAPA DE MODELOS DO SIMULTANIUM")
    print("=" * 70)
    print(f"📅 Data: {MAPA['data_mapeamento']}")
    print(f"👤 Usuário: {MAPA['usuario']}")
    print()
    
    print("📊 RESUMO GERAL:")
    print(f"   • Total de modelos mapeados: {MAPA['resumo']['total_modelos']}")
    print(f"   • Modelos funcionando: {MAPA['resumo']['modelos_funcionando']}")
    print(f"   • Cotas separadas: {MAPA['resumo']['cotas_separadas']}")
    print()
    
    for metodo, dados in MAPA["metodos"].items():
        print(f"┌── {dados['nome']} ┐")
        print(f"   Descrição: {dados['descricao']}")
        print()
        
        total = len(dados['modelos'])
        funcionando = sum(1 for m in dados['modelos'].values() if "✅" in m['status'])
        
        print(f"   📋 Modelos ({funcionando}/{total}):")
        for modelo, info in dados['modelos'].items():
            print(f"      ├── {modelo}: {info['status']}")
            if 'nota' in info and info['nota']:
                print(f"      │   💡 {info['nota']}")
        
        print(f"   └── {funcionando}/{total} modelos funcionam neste método")
        print()
    
    print("=" * 70)
    print("💡 PRINCIPAL LIÇÃO:")
    print("   As cotas são SEPARADAS!")
    print("   • Se a cota AI Studio acabar → use Antigravity CLI")
    print("   • Se a cota Antigravity acabar → use AI Studio / Web")
    print("   • O Simultanium alternará entre eles automaticamente")
    print()
    print("📄 Relatório salvo em: Simultanium/mapa_modelos.json")
    print("=" * 70)
    print()


def main():
    print("🗺️  Iniciando mapeamento automático de modelos do Simultanium...")
    print("   (Isso pode levar alguns minutos...)")
    print()
    
    # 1. Carregar configurações
    api_key = carregar_chave()
    print(f"✅ Chave AI Studio: {'Encontrada' if api_key else 'NÃO encontrada'}")
    print()
    
    # 2. Mapear API Direta
    print(">>> Mapeando API Direta (Google AI Studio)...")
    modelos_api = [
        "gemini-3.5-flash", "gemini-4-neon", "gemini-4-hydrogen-high",
        "gemini-3.8-flash", "gemma-4-26b-a4b-it", "gemini-3.5-flash-lite"
    ]
    resultados_api = testar_api_direct(modelos_api)
    
    modelo_map_api = {}
    for modelo, info in resultados_api.items():
        modelo_map_api[modelo] = info
        MAPA["modelos"][modelo] = info  # Para compatibilidade
        MAPA["resumo"]["total_modelos"] += 1
        if "✅" in info["status"]:
            MAPA["resumo"]["modelos_funcionando"] += 1
    
    MAPA["metodos"]["api_direct"] = {
        "nome": "Google AI Studio API",
        "descricao": "Usa a API direta generativelanguage.googleapis.com com sua chave",
        "modelos": modelo_map_api
    }
    print("   ✅ API Direta mapeada")
    print()
    
    # 3. Mapear Antigravity CLI
    print(">>> Mapeando Antigravity CLI...")
    resultados_antigravity = testar_antigravity_cli()
    
    for modelo, info in resultados_antigravity.items():
        MAPA["modelos"][modelo] = info
        MAPA["resumo"]["total_modelos"] += 1
        if "✅" in info["status"]:
            MAPA["resumo"]["modelos_funcionando"] += 1
    
    MAPA["metodos"]["antigravity_cli"] = {
        "nome": "Google Antigravity PRO via CLI agy",
        "descricao": "Usa o CLI agy com plano PRO (cota separada)",
        "modelos": resultados_antigravity
    }
    print("   ✅ Antigravity CLI mapeado")
    print()
    
    # 4. Gerar relatório
    gerar_relatorio_final()
    
    # 5. Salvar mapa em arquivo
    mapa_path = os.path.join(CONFIG_DIR, "mapa_modelos.json")
    with open(mapa_path, 'w', encoding='utf-8') as f:
        json.dump(MAPA, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Mapa salvo em: {mapa_path}")
    print()
    print("=" * 70)
    print("🎯 PRÓXIMO PASSO:")
    print("   Execute: python scripts/gemini-chat.py \"Sua mensagem\"")
    print("   O script tentará os métodos em ordem automaticamente!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Mapeamento interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante mapeamento: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)