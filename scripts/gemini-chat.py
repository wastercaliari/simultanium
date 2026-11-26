#!/usr/bin/env python3
"""Google AI Studio Gemini Chat - Simultanium Project.

Tries three methods automatically:
1. API Direta (Google AI Studio) - gemini-3.5-flash
2. Interface Web via Webridge - gemini-4-neon  
3. Antigravity PRO via CLI agy - gemini-4-hydrogen-high

Cotas separadas: AI Studio, Web (conta Google), Antigravity PRO (plano PRO).
"""

import os
import sys
import json
import argparse
import time
import urllib.request
import urllib.parse

# Caminhos e configurações
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config")
KEY_PATH = r"C:\Users\waste\OneDrive\Documentos\Projeto Padrão\api google gemin.txt"

# Configurações carregadas
CONFIG = {
    "api_key": None,
    "access_method": "auto",  # auto, api_direct, web_interface, antigravity_cli
    "api_direct_model": "gemini-3.5-flash",
    "web_interface_model": "gemini-4-neon",
    "antigravity_model": "gemini-4-hydrogen-high",
}

def load_config():
    """Carrega configurações do projeto."""
    global CONFIG
    
    # Carregar chave da API
    key_paths = [
        KEY_PATH,
        os.path.join(CONFIG_DIR, "ai_studio.env"),
    ]
    
    for path in key_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Parse simples do .env
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('GEMINI_API_KEY='):
                        CONFIG["api_key"] = line.split('=', 1)[1].strip('"').strip("'")
                    elif line.startswith('ACCESS_METHOD='):
                        CONFIG["access_method"] = line.split('=', 1)[1].strip()
                    elif line.startswith('API_DIRECT_MODEL='):
                        CONFIG["api_direct_model"] = line.split('=', 1)[1].strip()
                    elif line.startswith('WEB_INTERFACE_MODEL='):
                        CONFIG["web_interface_model"] = line.split('=', 1)[1].strip()
                    elif line.startswith('ANTIGRAVITY_MODEL='):
                        CONFIG["antigravity_model"] = line.split('=', 1)[1].strip()
            except:
                pass
    
    # Se não carregou do arquivo, tenta variável de ambiente
    if not CONFIG["api_key"]:
        CONFIG["api_key"] = os.environ.get('GEMINI_API_KEY', '')
    
    print(f"Configuração carregada: API_key={'SIM' if CONFIG['api_key'] else 'NÃO'}, ")
    print(f"   Método: {CONFIG['access_method']}")


def generate_content_api_direct(api_key, model, message):
    """Envia mensagem via API direta do Google AI Studio."""
    import urllib.request
    import urllib.parse
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
    
    body = json.dumps({
        "contents": [{"parts": [{"text": message}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get("candidates") and len(data["candidates"]) > 0:
                text = data["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
                usage = data.get("usageMetadata", {})
                return text, resp.status, usage
            return "Sem resposta da modelo", resp.status, {}
    except Exception as e:
        return f"Erro: {str(e)}", 0, {}


def generate_content_web_interface(message, model="gemini-4-neon"):
    """Envia mensagem via Interface Web do Gemini (gemini.google.com).
    Usa Webridge para acessar a página e extrair resposta."""
    import subprocess
    
    # Try using the webridge_http.py script if available
    webridge_script = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "..", "..", "..", ".config", "opencode", "skills", "webridge", "scripts", "webridge_http.py"
    )
    
    # Alternative: try direct fetch with proper headers
    # For now, we'll use a simple approach - check if we can access the page
    # and simulate what the user does manually
    
    # NOTE: Full Webridge automation would require the webridge HTTP client
    # This is a simplified version that returns a status indicator
    # In a full implementation, this would use the webridge client
    
    return None, None  # Will be implemented with actual Webridge client


def generate_content_antigravity_cli(message, model="gemini-4-hydrogen-high"):
    """Envia mensagem via CLI Antigravity agy."""
    import subprocess
    
    agy_path = r"C:\Users\waste\AppData\Local\agy\bin\agy.exe"
    
    if not os.path.exists(agy_path):
        return None, None
    
    try:
        # Build the command: agy -p='message' --model model
        cmd = [agy_path, "-p=", f"'{message}'", "--model", model]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout.strip()
        if not output and result.stderr:
            output = result.stderr.strip()
        
        return output, result.returncode
    except Exception as e:
        return f"Erro: {str(e)}", -1


def main():
    load_config()
    
    parser = argparse.ArgumentParser(description="Chat com Google Gemini - Simultanium")
    parser.add_argument("message", nargs="*", help="Mensagem para enviar")
    parser.add_argument("--model", default=None, help="Modelo específico (overrides config)")
    parser.add_argument("--method", default=None, help="Método específico (api_direct, web_interface, antigravity_cli)")
    parser.add_argument("--list-methods", action="store_true", help="Listar métodos disponíveis")
    parser.add_argument("--interativo", action="store_true", help="Modo interativo contínuo")
    
    args = parser.parse_args()
    
    # Listar métodos
    if args.list_methods:
        print("Métodos disponíveis no Simultanium:")
        print("  1. api_direct: Google AI Studio API (gemini-3.5-flash)")
        print("     Cota: Sua chave em api google gemin.txt")
        print("  2. web_interface: Interface Web do Gemini (gemini-4-neon)")
        print("     Cota: Sua conta Google (wasterlucas.ia@gmail.com)")
        print("  3. antigravity_cli: CLI Antigravity (gemini-4-hydrogen-high)")
        print("     Cota: Seu plano PRO (separado)")
        sys.exit(0)
    
    # Determinar método
    method = args.method or CONFIG["access_method"] or "auto"
    
    # Determinar modelo
    model = args.model or {
        "api_direct": CONFIG["api_direct_model"],
        "web_interface": CONFIG["web_interface_model"],
        "antigravity_cli": CONFIG["antigravity_model"]
    }.get(method, CONFIG["api_direct_model"])
    
    # Pegar mensagem
    if not args.message:
        parser.print_help()
        sys.exit(1)
    
    message = " ".join(args.message)
    
    print(f"🔍 Simultanium - Tentando método: {method} com modelo: {model}")
    print(f"📝 Mensagem: {message}")
    print()
    
    # Método 1: API Direta
    if method in ["auto", "api_direct", ""]:
        print(">>> Tentando método 1: API Direta (AI Studio)")
        response, status, usage = generate_content_api_direct(
            CONFIG["api_key"], model, message
        )
        
        if status == 200:
            print(f"✅ API Direta funcionou!")
            print(f"🤖 Resposta ({model}):")
            print(f"  {response}")
            if usage:
                print(f"   Tokens: {usage.get('promptTokenCount', '?')} prompt + {usage.get('candidatesTokenCount', '?')} response")
            sys.exit(0)
        elif status == 429 or status == 503:
            print(f"⚠️ API Direta com problema (status {status}). Tentando próximo método...")
        else:
            print(f"ℹ️ API Direta retornou status {status}. Tentando próximo método...")
    
    # Método 2: Interface Web
    if method in ["auto", "web_interface"]:
        print(">>> Tentando método 2: Interface Web (Gemini Web)")
        # Acesso via Webridge - simplificado
        # Em uma implementação completa, usaria o webridge_http.py
        # Por enquanto, indicamos que esta é a próxima opção
        print("   (Acesso via Webridge - implementação em andamento)")
        print("   Tentando acesso direto à página...")
        
        # Try to access the web interface
        try:
            import urllib.request
            url = "https://gemini.google.com/"
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                }
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='replace')[:1000]
                # Check if page loaded properly
                if "gemini" in html.lower() or "model" in html.lower():
                    print("   ✅ Página do Gemini acessada com sucesso")
                    print("   ⚠️ Para resposta automática, seria necessário Webridge full")
                    print("   💡 Use 'agy -p=\"mensagem\" --model gemini-4-hydrogen-high' para Antigravity PRO")
                else:
                    print("   ⚠️ Página carregada, mas não foi possível extrair resposta")
        except Exception as e:
            print(f"   ❌ Erro ao acessar web: {str(e)[:100]}")
        
        print("   💡 Alternativa: Use o CLI Antigravity para cota PRO separada")
    
    # Método 3: Antigravity CLI
    if method in ["auto", "antigravity_cli"]:
        print(">>> Tentando método 3: Antigravity PRO CLI")
        response, returncode = generate_content_antigravity_cli(message, model)
        
        if returncode == 0 and response:
            print(f"✅ Antigravity PRO funcionou!")
            print(f"🤖 Resposta (modelo {model}):")
            print(f"  {response}")
        else:
            print(f"❌ Antigravity CLI com problema (código: {returncode})")
            if response:
                print(f"   Erro: {response[:200]}")
    
    print()
    print("=" * 60)
    print("💡 Dica: Use --method api_direct para AI Studio, ")
    print("   --method web_interface para interface web,")
    print("   ou --method antigravity_cli para cota PRO separada.")
    print("=" * 60)


if __name__ == "__main__":
    main()