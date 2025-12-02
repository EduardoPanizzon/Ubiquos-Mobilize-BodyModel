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
echo [1/6] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.11, 3.12 ou 3.13:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE:
    echo - Marque "Add Python to PATH" durante a instalacao
    echo - Marque "Add Python tkinter" durante a instalacao
    echo - NAO use Python 3.14 (incompativel)
    echo - Use Python 3.11, 3.12 ou 3.13
    echo.
    pause
)
echo [OK] Python encontrado!
python --version
echo.
echo Verificando versao do Python...
python -c "import sys; v=sys.version_info; exit(0 if (3,11)<=v<(3,14) else 1)" 2>nul
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Versao do Python incompativel!
    echo.
    echo VERSOES COMPATIVEIS: Python 3.11, 3.12 ou 3.13
    echo VERSAO NAO COMPATIVEL: Python 3.14
    echo.
    echo Por favor, instale uma versao compativel:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Versao compativel!
echo.

REM Atualizar pip, setuptools e wheel
echo [2/6] Atualizando pip, setuptools e wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [ERRO] Falha ao atualizar pip!
    pause
    exit /b 1
)
echo [OK] pip atualizado!
echo.

REM Instalar bibliotecas principais UMA POR VEZ (para detectar erros)
echo [3/6] Instalando bibliotecas necessarias...
echo.
echo    Instalando numpy (versao especifica)...
python -m pip install "numpy>=1.24.0"
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar numpy!
    echo Tentando versao alternativa...
    python -m pip install numpy==1.24.0
    if errorlevel 1 (
        echo Tente executar este script como Administrador.
        pause
        exit /b 1
    )
)
echo    [OK] numpy instalado!
echo.

echo    Instalando opencv-python (versao especifica)...
python -m pip install "opencv-python>=4.8.0"
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar opencv-python!
    echo Tentando versao alternativa...
    python -m pip install opencv-python==4.8.0
    if errorlevel 1 (
        pause
        exit /b 1
    )
)
echo    [OK] opencv-python instalado!
echo.

echo    Instalando matplotlib (versao especifica)...
python -m pip install "matplotlib>=3.7.0"
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar matplotlib!
    echo Tentando versao alternativa...
    python -m pip install matplotlib==3.7.0
    if errorlevel 1 (
        pause
        exit /b 1
    )
)
echo    [OK] matplotlib instalado!
echo.

echo    Instalando Pillow (versao especifica)...
python -m pip install "Pillow>=10.0.0"
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar Pillow!
    echo Tentando versao alternativa...
    python -m pip install Pillow==10.0.0
    if errorlevel 1 (
        pause
        exit /b 1
    )
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

echo    Instalando warp-lang...
python -m pip install warp-lang
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar warp-lang!
    pause
    exit /b 1
)
echo    [OK] warp-lang instalado!
echo.

echo    Instalando mujoco-mjx...
python -m pip install mujoco-mjx
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar mujoco-mjx!
    pause
    exit /b 1
)
echo    [OK] mujoco-mjx instalado!
echo.

echo [OK] Bibliotecas principais instaladas!
echo.

REM Instalar monocular-demos
echo [4/6] Instalando monocular-demos...
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
echo [5/6] Instalando PyInstaller...
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
python -c "import tensorflow; print('[OK] tensorflow')" || (echo [ERRO] tensorflow NAO instalado! & pause & exit /b 1)
python -c "import jax; print('[OK] jax')" || (echo [ERRO] jax NAO instalado! & pause & exit /b 1)
python -c "import warp; print('[OK] warp-lang')" || (echo [ERRO] warp-lang NAO instalado! & pause & exit /b 1)
python -c "import mujoco_mjx; print('[OK] mujoco-mjx')" || (echo [ERRO] mujoco-mjx NAO instalado! & pause & exit /b 1)
python -c "import monocular_demos; print('[OK] monocular-demos')" || (echo [ERRO] monocular-demos NAO instalado! & pause & exit /b 1)
python -c "import PyInstaller; print('[OK] PyInstaller')" || (echo [ERRO] PyInstaller NAO instalado! & pause & exit /b 1)
echo.

echo ============================================================
echo TODAS as bibliotecas OBRIGATORIAS foram instaladas!
echo - numpy, opencv-python, matplotlib, Pillow, tkinter
echo - tensorflow, jax, warp-lang, mujoco-mjx
echo - monocular-demos, PyInstaller
echo.
echo O executavel pode ser criado.
echo ============================================================
echo.

echo ============================================================
echo   [6/6] CRIANDO EXECUTAVEL
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

