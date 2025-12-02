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
echo Instalando numpy...
python -m pip install numpy --no-cache-dir
if errorlevel 1 (
    color 0C
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
echo [OK] numpy instalado!
timeout /t 1 >nul
echo.

echo --- OPENCV-PYTHON ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall opencv-python opencv-python-headless -y >nul 2>&1
echo Instalando opencv-python...
python -m pip install opencv-python --no-cache-dir
if errorlevel 1 (
    color 0C
    echo [ERRO] Falha ao instalar OPENCV-PYTHON
    echo Tentando versao alternativa...
    python -m pip install opencv-python-headless --no-cache-dir
    if errorlevel 1 (
        echo [ERRO] Ambas versoes falharam!
        pause
        exit /b 1
    )
)
echo [OK] opencv-python instalado!
timeout /t 1 >nul
echo.

echo --- MATPLOTLIB ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall matplotlib -y >nul 2>&1
echo Instalando matplotlib...
python -m pip install matplotlib --no-cache-dir
if errorlevel 1 goto erro_lib
echo [OK] matplotlib instalado!
timeout /t 1 >nul
echo.

echo --- PILLOW ---
echo Desinstalando versao antiga (se existir)...
python -m pip uninstall Pillow -y >nul 2>&1
echo Instalando Pillow...
python -m pip install Pillow --no-cache-dir
if errorlevel 1 goto erro_lib
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

REM Bibliotecas opcionais
echo ============================================================
echo [PASSO 3] Instalando bibliotecas opcionais
echo ============================================================
echo.

echo Instalando tensorflow (pode demorar, pode falhar sem problema)...
python -m pip install tensorflow 2>nul || python -m pip install tensorflow-cpu 2>nul || echo [AVISO] tensorflow nao instalado (opcional)
echo.

echo Instalando jax e jaxlib...
python -m pip install jax jaxlib 2>nul || echo [AVISO] jax nao instalado (opcional)
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
