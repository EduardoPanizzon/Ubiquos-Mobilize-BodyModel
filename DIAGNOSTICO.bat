@echo off
title Diagnostico - Analisador de Marcha
color 0B
echo ============================================================
echo   DIAGNOSTICO DO SISTEMA
echo   Analisador de Marcha - Mobile Local
echo ============================================================
echo.

REM Verificar Python
echo [1] Verificando Python...
python --version 2>nul
if errorlevel 1 (
    color 0C
    echo [ERRO] Python NAO encontrado!
    echo.
    echo Instale Python em: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante instalacao
    echo.
    goto fim
) else (
    echo [OK] Python encontrado
    python --version
    echo.
    echo Verificando versao do Python...
    python -c "import sys; v=sys.version_info; exit(0 if (3,11)<=v<(3,14) else 1)" 2>nul
    if errorlevel 1 (
        color 0E
        echo [AVISO] Versao do Python pode ser incompativel!
        echo.
        echo VERSOES COMPATIVEIS: Python 3.11, 3.12 ou 3.13
        echo VERSAO NAO COMPATIVEL: Python 3.14
        echo.
        echo Recomenda-se instalar Python 3.11 ou 3.12
        echo Download: https://www.python.org/downloads/
        echo.
        pause
    ) else (
        echo [OK] Versao compativel (3.11 - 3.13)
    )
)
echo.

REM Verificar pip
echo [2] Verificando pip...
python -m pip --version
if errorlevel 1 (
    color 0C
    echo [ERRO] pip NAO encontrado!
    goto fim
)
echo [OK] pip encontrado
echo.

REM Verificar cada biblioteca
echo [3] Verificando bibliotecas instaladas...
echo.

echo Testando numpy...
python -c "import numpy; print('  Versao:', numpy.__version__)" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando opencv-python (cv2)...
python -c "import cv2; print('  Versao:', cv2.__version__)" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando matplotlib...
python -c "import matplotlib; print('  Versao:', matplotlib.__version__)" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando Pillow (PIL)...
python -c "import PIL; print('  Versao:', PIL.__version__)" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando tkinter...
python -c "import tkinter; print('  [OK] Instalado')" 2>nul || echo   [X] NAO INSTALADO - Reinstale Python com tkinter
echo.

echo Testando PyInstaller...
python -c "import PyInstaller; print('  Versao:', PyInstaller.__version__)" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando tensorflow...
python -c "import tensorflow; print('  Versao:', tensorflow.__version__)" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando jax...
python -c "import jax; print('  Versao:', jax.__version__)" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando warp-lang...
python -c "import warp; print('  Versao:', warp.__version__)" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando mujoco-mjx...
python -c "import mujoco_mjx; print('  [OK] Instalado')" 2>nul || echo   [X] NAO INSTALADO
echo.

echo Testando monocular_demos...
python -c "import monocular_demos; print('  [OK] Instalado')" 2>nul || echo   [X] NAO INSTALADO
echo.

echo ============================================================
echo [4] Verificando arquivos do projeto...
echo.

if exist "video_processor_gui.py" (
    echo [OK] video_processor_gui.py encontrado
) else (
    color 0C
    echo [ERRO] video_processor_gui.py NAO encontrado!
    echo Certifique-se de estar na pasta correta.
)
echo.

if exist "projetos" (
    echo [OK] Pasta projetos existe
) else (
    echo [AVISO] Pasta projetos nao existe (sera criada automaticamente)
)
echo.

echo ============================================================
echo   DIAGNOSTICO CONCLUIDO
echo ============================================================
echo.
echo BIBLIOTECAS OBRIGATORIAS:
echo - numpy, opencv-python, matplotlib, Pillow, tkinter
echo - tensorflow, jax, warp-lang, mujoco-mjx
echo - monocular_demos, PyInstaller
echo.
echo Se alguma biblioteca OBRIGATORIA estiver faltando:
echo 1. Execute: CORRIGIR_INSTALACAO.bat como Administrador
echo 2. Ou execute: INSTALAR_E_CRIAR_EXE.bat como Administrador
echo 3. Ou instale manualmente: python -m pip install NOME_DA_BIBLIOTECA
echo.

:fim
pause
