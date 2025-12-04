@echo off
title Criar Atalho - Analisador de Marcha
color 0A
echo ============================================================
echo   CRIAR ATALHO - ANALISADOR DE MARCHA
echo   Mobile Local - Video Processor
echo ============================================================
echo.
echo Este script ira criar um atalho na area de trabalho
echo que executa o programa diretamente.
echo.
pause

REM Obter caminho do Python
echo Localizando Python...
where python >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERRO] Python nao encontrado!
    echo Instale Python primeiro.
    pause
    exit /b 1
)

REM Criar atalho usando PowerShell
echo Criando atalho na pasta do projeto...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%~dp0Analisador de Marcha.lnk'); $Shortcut.TargetPath = 'cmd.exe'; $Shortcut.Arguments = '/c python video_processor_gui.py'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Analisador de Marcha - Video Processor'; $Shortcut.Save()"

if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao criar atalho!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   SUCESSO!
echo ============================================================
echo.
color 0A
echo Atalho criado na pasta do projeto!
echo.
echo Nome: "Analisador de Marcha.lnk"
echo.
echo Basta clicar duas vezes no atalho para executar o programa.
echo.
echo IMPORTANTE:
echo - Python deve estar instalado
echo - As bibliotecas devem estar instaladas
echo - Nao mova os arquivos desta pasta
echo.
pause
