"""
Script para criar executável do Analisador de Marcha
"""
import subprocess
import sys
import os

def build_executable():
    """Cria o executável usando PyInstaller"""
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print("✓ PyInstaller encontrado")
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado")
    
    # Configurações do PyInstaller
    app_name = "Analisador_Marcha"
    script_name = "video_processor_gui.py"
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--name=" + app_name,
        "--onefile",  # Um único arquivo executável
        "--windowed",  # Sem console (apenas GUI)
        "--icon=NONE",  # Sem ícone personalizado (pode adicionar depois)
        "--add-data=projetos;projetos",  # Incluir pasta de projetos se existir
        "--hidden-import=PIL._tkinter_finder",  # Imports necessários
        "--hidden-import=tkinter",
        "--hidden-import=cv2",
        "--hidden-import=matplotlib",
        "--hidden-import=numpy",
        "--collect-all=monocular_demos",  # Incluir monocular_demos se disponível
        script_name
    ]
    
    print("\nCriando executável...")
    print(f"Comando: {' '.join(cmd)}\n")
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("✓ EXECUTÁVEL CRIADO COM SUCESSO!")
        print("="*60)
        print(f"\nO executável está em: dist\\{app_name}.exe")
        print("\nVocê pode:")
        print("1. Executar dist\\{}.exe diretamente".format(app_name))
        print("2. Criar um atalho na área de trabalho")
        print("3. Mover o .exe para onde quiser")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Erro ao criar executável: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("="*60)
    print("BUILD DO ANALISADOR DE MARCHA - MOBILE LOCAL")
    print("="*60)
    print()
    
    success = build_executable()
    
    if success:
        input("\nPressione ENTER para fechar...")
    else:
        input("\nOcorreram erros. Pressione ENTER para fechar...")
