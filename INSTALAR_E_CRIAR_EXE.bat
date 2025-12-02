@echo off
title Instalador Completo - Analisador de Marcha
color 0A
echo ============================================================
echo   INSTALADOR COMPLETO - ANALISADOR DE MARCHA
echo   Mobile Local - Video Processor
echo ============================================================
echo.
echo Este script ira:
echo 1. Verificar se Python esta instalado
echo 2. Instalar todas as bibliotecas necessarias
echo 3. Instalar monocular-demos
echo 4. Criar o executavel (.exe)
echo.
echo Isso pode levar alguns minutos...
echo.
pause
echo.

REM Verificar se Python esta instalado
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo Certifique-se de marcar "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)
echo [OK] Python encontrado!
echo.

REM Atualizar pip, setuptools e wheel
echo [2/5] Atualizando pip, setuptools e wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [ERRO] Falha ao atualizar pip!
    pause
    exit /b 1
)
echo [OK] pip atualizado!
echo.

REM Instalar bibliotecas principais UMA POR VEZ (para detectar erros)
echo [3/5] Instalando bibliotecas necessarias...
echo.
echo    Instalando numpy...
python -m pip install numpy
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar numpy!
    echo Tente executar este script como Administrador.
    pause
    exit /b 1
)
echo    [OK] numpy instalado!
echo.

echo    Instalando opencv-python...
python -m pip install opencv-python
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar opencv-python!
    pause
    exit /b 1
)
echo    [OK] opencv-python instalado!
echo.

echo    Instalando matplotlib...
python -m pip install matplotlib
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar matplotlib!
    pause
    exit /b 1
)
echo    [OK] matplotlib instalado!
echo.

echo    Instalando Pillow...
python -m pip install Pillow
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar Pillow!
    pause
    exit /b 1
)
echo    [OK] Pillow instalado!
echo.

echo    Instalando tensorflow (pode demorar)...
python -m pip install tensorflow
if errorlevel 1 (
    echo [AVISO] tensorflow falhou, tentando versao CPU...
    python -m pip install tensorflow-cpu
)
echo    [OK] tensorflow instalado!
echo.

echo    Instalando tensorflow-hub...
python -m pip install tensorflow-hub
echo    [OK] tensorflow-hub instalado!
echo.

echo    Instalando jax...
python -m pip install jax
echo    [OK] jax instalado!
echo.

echo    Instalando jaxlib...
python -m pip install jaxlib
echo    [OK] jaxlib instalado!
echo.

echo [OK] Bibliotecas principais instaladas!
echo.

REM Instalar monocular-demos
echo [4/5] Instalando monocular-demos...
echo    Verificando se ja esta instalado...
python -c "import monocular_demos" >nul 2>&1
if errorlevel 1 (
    echo    monocular-demos nao encontrado. Instalando...
    
    REM Verificar se ja foi clonado
    if exist "monocular-demos" (
        echo    Pasta monocular-demos ja existe. Atualizando...
        cd monocular-demos
        git pull >nul 2>&1
    ) else (
        echo    Clonando repositorio...
        git clone https://github.com/IntelligentSensingAndRehabilitation/monocular-demos.git >nul 2>&1
        if errorlevel 1 (
            echo    [AVISO] Nao foi possivel clonar com git.
            echo    Tentando instalacao direta...
            python -m pip install git+https://github.com/IntelligentSensingAndRehabilitation/monocular-demos.git --quiet
            goto skip_local_install
        )
        cd monocular-demos
    )
    
    echo    Instalando monocular-demos...
    python -m pip install . --quiet
    cd ..
    
    :skip_local_install
    echo [OK] monocular-demos instalado!
) else (
    echo    [OK] monocular-demos ja instalado!
)
echo.

REM Instalar PyInstaller
echo [5/5] Instalando PyInstaller...
python -m pip install pyinstaller --quiet
echo [OK] PyInstaller instalado!
echo.

REM Verificar instalacoes
echo ============================================================
echo   VERIFICANDO INSTALACOES
echo ============================================================
echo.
echo Testando imports OBRIGATORIOS...

python -c "import numpy; print('[OK] numpy')" || (echo [ERRO] numpy NAO instalado! & pause & exit /b 1)
python -c "import cv2; print('[OK] opencv-python')" || (echo [ERRO] opencv-python NAO instalado! & pause & exit /b 1)
python -c "import matplotlib; print('[OK] matplotlib')" || (echo [ERRO] matplotlib NAO instalado! & pause & exit /b 1)
python -c "import PIL; print('[OK] Pillow')" || (echo [ERRO] Pillow NAO instalado! & pause & exit /b 1)
python -c "import tkinter; print('[OK] tkinter')" || (echo [ERRO] tkinter NAO instalado! & pause & exit /b 1)
python -c "import PyInstaller; print('[OK] PyInstaller')" || (echo [ERRO] PyInstaller NAO instalado! & pause & exit /b 1)

echo.
echo Testando imports OPCIONAIS...
python -c "import tensorflow; print('[OK] tensorflow')" 2>nul || echo [AVISO] tensorflow (opcional)
python -c "import jax; print('[OK] jax')" 2>nul || echo [AVISO] jax (opcional)
python -c "import monocular_demos; print('[OK] monocular-demos')" 2>nul || echo [AVISO] monocular-demos (opcional)
echo.

echo ============================================================
echo Todas as bibliotecas OBRIGATORIAS foram instaladas!
echo O executavel pode ser criado.
echo ============================================================
echo.

echo ============================================================
echo   CRIANDO EXECUTAVEL
echo ============================================================
echo.
echo Gerando Analisador_Marcha.exe...
echo Este processo pode levar alguns minutos...
echo.

REM Limpar builds anteriores
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "Analisador_Marcha.spec" del /q "Analisador_Marcha.spec"

REM Criar executavel com todas as dependencias explicitas
pyinstaller ^
    --name=Analisador_Marcha ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=cv2 ^
    --hidden-import=matplotlib ^
    --hidden-import=matplotlib.pyplot ^
    --hidden-import=matplotlib.backends.backend_agg ^
    --hidden-import=numpy ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageTk ^
    --collect-data cv2 ^
    --noconfirm ^
    video_processor_gui.py

if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Falha ao criar executavel!
    echo Verifique os erros acima.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   SUCESSO!
echo ============================================================
echo.
color 0A
echo O executavel foi criado com sucesso!
echo.
echo Localizacao: dist\Analisador_Marcha.exe
echo.
echo Voce pode:
echo 1. Executar dist\Analisador_Marcha.exe diretamente
echo 2. Copiar o .exe para qualquer lugar
echo 3. Criar um atalho na area de trabalho
echo 4. Distribuir para outras pessoas
echo.
echo IMPORTANTE: 
echo - O executavel NAO precisa de Python instalado para rodar
echo - Os projetos ficam salvos na pasta "projetos"
echo - Mantenha a pasta "projetos" junto com o .exe se for mover
echo.
pause
