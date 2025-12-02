@echo off
title CORRECAO - Instalacao de Bibliotecas
color 0E
echo ============================================================
echo   CORRECAO - Reinstalacao de Bibliotecas
echo   Use este script se a instalacao normal falhou
echo ============================================================
echo.
echo Este script vai:
echo - Atualizar pip, setuptools e wheel
echo - Reinstalar cada biblioteca individualmente
echo - Parar se houver erro para voce ver qual biblioteca falhou
echo.
pause
echo.

REM Verificar versao do Python
echo Verificando versao do Python...
python --version
echo.
python -c "import sys; v=sys.version_info; exit(0 if (3,11)<=v<(3,14) else 1)" 2>nul
if errorlevel 1 (
    color 0C
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
echo [OK] Python versao compativel (3.11 - 3.13)
echo.

REM Elevar privilegios se possivel
echo Verificando permissoes...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Executando como Administrador
) else (
    color 0C
    echo [AVISO] NAO esta executando como Administrador
    echo Para melhor resultado, clique direito e "Executar como Administrador"
    echo.
    pause
    color 0E
)
echo.

REM Atualizar ferramentas base
echo ============================================================
echo [PASSO 1] Atualizando ferramentas base
echo ============================================================
echo.
python -m pip install --upgrade pip
if errorlevel 1 goto erro_pip
echo.

python -m pip install --upgrade setuptools
if errorlevel 1 goto erro_pip
echo.

python -m pip install --upgrade wheel
if errorlevel 1 goto erro_pip
echo.

echo [OK] Ferramentas base atualizadas!
echo.
timeout /t 2 >nul

REM Desinstalar e reinstalar bibliotecas problematicas
echo ============================================================
echo [PASSO 2] Reinstalando bibliotecas (uma por vez)
echo ============================================================
echo.

echo --- NUMPY ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall numpy -y >nul 2>&1
echo Instalando numpy (versao 1.24.0 ou superior)...
python -m pip install "numpy>=1.24.0" --no-cache-dir
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Falha ao instalar NUMPY versao recente
    echo Tentando versao especifica 1.24.0...
    python -m pip install numpy==1.24.0 --no-cache-dir
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao instalar NUMPY
        echo.
        echo Possiveis solucoes:
        echo 1. Atualize o Python para a versao mais recente
        echo 2. Instale o Microsoft Visual C++ 14.0 ou superior
        echo    Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
        echo 3. Tente: python -m pip install numpy==1.24.3
        echo.
        pause
        exit /b 1
    )
)
echo [OK] numpy instalado!
timeout /t 1 >nul
echo.

echo --- OPENCV-PYTHON ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall opencv-python opencv-python-headless -y >nul 2>&1
echo Instalando opencv-python (versao 4.8.0 ou superior)...
python -m pip install "opencv-python>=4.8.0" --no-cache-dir
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar OPENCV-PYTHON versao recente
    echo Tentando versao especifica 4.8.0...
    python -m pip install opencv-python==4.8.0 --no-cache-dir
    if errorlevel 1 (
        echo Tentando opencv-python-headless como alternativa...
        python -m pip install "opencv-python-headless>=4.8.0" --no-cache-dir
        if errorlevel 1 (
            echo [ERRO] Todas as versoes falharam!
            pause
            exit /b 1
        )
    )
)
echo [OK] opencv-python instalado!
timeout /t 1 >nul
echo.

echo --- MATPLOTLIB ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall matplotlib -y >nul 2>&1
echo Instalando matplotlib (versao 3.7.0 ou superior)...
python -m pip install "matplotlib>=3.7.0" --no-cache-dir
if errorlevel 1 (
    echo Tentando versao especifica 3.7.0...
    python -m pip install matplotlib==3.7.0 --no-cache-dir
    if errorlevel 1 goto erro_lib
)
echo [OK] matplotlib instalado!
timeout /t 1 >nul
echo.

echo --- PILLOW ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall Pillow -y >nul 2>&1
echo Instalando Pillow (versao 10.0.0 ou superior)...
python -m pip install "Pillow>=10.0.0" --no-cache-dir
if errorlevel 1 (
    echo Tentando versao especifica 10.0.0...
    python -m pip install Pillow==10.0.0 --no-cache-dir
    if errorlevel 1 goto erro_lib
)
echo [OK] Pillow instalado!
timeout /t 1 >nul
echo.

echo --- PYINSTALLER ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall pyinstaller -y >nul 2>&1
echo Instalando PyInstaller...
python -m pip install pyinstaller --no-cache-dir
if errorlevel 1 goto erro_lib
echo [OK] PyInstaller instalado!
timeout /t 1 >nul
echo.

REM Bibliotecas adicionais obrigatorias
echo ============================================================
echo [PASSO 3] Instalando bibliotecas adicionais obrigatorias
echo ============================================================
echo.

echo --- TENSORFLOW ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall tensorflow tensorflow-cpu -y >nul 2>&1
echo Instalando tensorflow...
python -m pip install tensorflow --no-cache-dir
if errorlevel 1 (
    echo Tentando tensorflow-cpu...
    python -m pip install tensorflow-cpu --no-cache-dir
    if errorlevel 1 goto erro_lib
)
echo [OK] tensorflow instalado!
timeout /t 1 >nul
echo.

echo --- JAX e JAXLIB ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall jax jaxlib -y >nul 2>&1
echo Instalando jax e jaxlib...
python -m pip install jax jaxlib --no-cache-dir
if errorlevel 1 goto erro_lib
echo [OK] jax e jaxlib instalados!
timeout /t 1 >nul
echo.

echo --- WARP-LANG ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall warp-lang -y >nul 2>&1
echo Instalando warp-lang...
python -m pip install warp-lang --no-cache-dir
if errorlevel 1 goto erro_lib
echo [OK] warp-lang instalado!
timeout /t 1 >nul
echo.

echo --- MUJOCO-MJX ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall mujoco-mjx -y >nul 2>&1
echo Instalando mujoco-mjx...
python -m pip install mujoco-mjx --no-cache-dir
if errorlevel 1 goto erro_lib
echo [OK] mujoco-mjx instalado!
timeout /t 1 >nul
echo.

REM Testar instalacoes
echo ============================================================
echo [PASSO 4] TESTANDO INSTALACOES
echo ============================================================
echo.

python -c "import numpy; print('[OK] numpy - versao', numpy.__version__)" || goto erro_teste
python -c "import cv2; print('[OK] cv2 - versao', cv2.__version__)" || goto erro_teste
python -c "import matplotlib; print('[OK] matplotlib - versao', matplotlib.__version__)" || goto erro_teste
python -c "import PIL; print('[OK] PIL - versao', PIL.__version__)" || goto erro_teste
python -c "import tkinter; print('[OK] tkinter')" || goto erro_teste
python -c "import tensorflow; print('[OK] tensorflow - versao', tensorflow.__version__)" || goto erro_teste
python -c "import jax; print('[OK] jax - versao', jax.__version__)" || goto erro_teste
python -c "import warp; print('[OK] warp-lang - versao', warp.__version__)" || goto erro_teste
python -c "import mujoco_mjx; print('[OK] mujoco-mjx')" || goto erro_teste
python -c "import PyInstaller; print('[OK] PyInstaller - versao', PyInstaller.__version__)" || goto erro_teste

echo.
color 0A
echo ============================================================
echo   SUCESSO! TODAS AS BIBLIOTECAS FORAM INSTALADAS!
echo ============================================================
echo.
echo Agora voce pode:
echo 1. Executar: INSTALAR_E_CRIAR_EXE.bat (para criar o executavel)
echo 2. Ou executar: Executar_Analisador_Marcha.bat (para testar o programa)
echo.
pause
exit /b 0

:erro_pip
color 0C
echo.
echo [ERRO] Falha ao atualizar pip/setuptools/wheel
echo.
echo Execute este comando manualmente:
echo python -m pip install --upgrade pip setuptools wheel
echo.
pause
exit /b 1

:erro_lib
color 0C
echo.
echo [ERRO] Falha ao instalar biblioteca
echo Veja a mensagem de erro acima.
echo.
pause
exit /b 1

:erro_teste
color 0C
echo.
echo [ERRO] Uma ou mais bibliotecas nao foram instaladas corretamente!
echo Execute este script novamente ou instale manualmente.
echo.
pause
exit /b 1
