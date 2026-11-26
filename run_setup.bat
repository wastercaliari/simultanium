@echo off
chcp 65001 >nul
cd /d "C:\Users\waste\OneDrive\Documentos\Projeto Padrão\Simultanium"
echo.
echo ==========================================
echo  INICIANDO SETUP SIMULTANIUM
echo ==========================================
echo.
rem Etapa 1: Configurar AI Studio
echo.
D:\Progra~1\Python\python.exe setup_simultanium.py
echo.
echo.
rem Etapa 2: Mapear modelos automaticamente
echo.
echo ==========================================
echo  MApeando modelos disponíveis...
echo.
python scripts\map_models_after_setup.py
echo.
echo.
echo ==========================================
echo  CONFIGURACAO E MAPEAMENTO CONCLUIDOS
echo ==========================================
echo.
echo  Os seguintes arquivos foram atualizados/criados:
echo.
echo   - config/ai_studio.env          (chave AI Studio + método)
echo   - config/antigravity.json       (conta PRO Antigravity)
echo   - scripts/gemini-chat.py        (script principal)
echo   - scripts/map_models_after_setup.py (mapeador automático)
echo   - config/mapa_modelos.json      (mapa de modelos em JSON)
echo.
echo  Voce pode agora usar o Simultanium da seguinte forma:
echo.
echo  1. Auto (testa os 3 métodos): python scripts\gemini-chat.py "Olá!"
echo  2. API Direta:          python scripts\gemini-chat.py --method api_direct "Olá!"
echo  3. Interface Web:       python scripts\gemini-chat.py --method web_interface "Olá!"
echo  4. Antigravity CLI:     python scripts\gemini-chat.py --method antigravity_cli "Olá!"
echo.
pause >nul