import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import cv2
import webbrowser
from pathlib import Path
import threading
from PIL import Image, ImageTk
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sem interface gráfica
from matplotlib import pyplot as plt


class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Processor - Mobile Local")
        self.root.geometry("900x700")
        
        # Configurações
        self.projects_dir = Path("projetos")
        self.projects_dir.mkdir(exist_ok=True)
        
        self.current_project = None
        self.current_video_path = None
        self.video_capture = None
        self.is_recording = False
        self.recorded_frames = []
        
        # Variáveis para o editor de vídeo
        self.total_frames = 0
        self.fps = 0
        self.start_frame = 0
        self.end_frame = 0
        
        # Iniciar com seleção de projeto
        self.show_project_selection()
    
    def show_project_selection(self):
        """Tela inicial para selecionar ou criar projeto"""
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Gerenciador de Projetos", 
                 font=('Arial', 18, 'bold')).pack(pady=20)
        
        # Botão para novo projeto
        ttk.Button(frame, text="Novo Projeto", 
                  command=self.create_new_project,
                  width=30).pack(pady=10)
        
        # Lista de projetos existentes
        ttk.Label(frame, text="Projetos Existentes:", 
                 font=('Arial', 12)).pack(pady=(20, 10))
        
        # Frame com scroll para lista de projetos
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.projects_listbox = tk.Listbox(list_frame, 
                                          yscrollcommand=scrollbar.set,
                                          font=('Arial', 11))
        self.projects_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.projects_listbox.yview)
        
        # Adicionar duplo clique para abrir projeto
        self.projects_listbox.bind('<Double-Button-1>', lambda e: self.open_selected_project())
        
        # Carregar projetos existentes
        self.load_existing_projects()
        
        ttk.Button(frame, text="Abrir Projeto Selecionado",
                  command=self.open_selected_project,
                  width=30).pack(pady=10)
    
    def load_existing_projects(self):
        """Carrega lista de projetos existentes"""
        self.projects_listbox.delete(0, tk.END)
        
        if self.projects_dir.exists():
            projects = [d.name for d in self.projects_dir.iterdir() if d.is_dir()]
            for project in sorted(projects):
                self.projects_listbox.insert(tk.END, project)
    
    def create_new_project(self):
        """Cria um novo projeto"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Projeto")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nome do Projeto:", 
                 font=('Arial', 11)).pack(pady=10)
        
        name_entry = ttk.Entry(dialog, width=40, font=('Arial', 11))
        name_entry.pack(pady=10)
        name_entry.focus()
        
        def confirm_creation():
            project_name = name_entry.get().strip()
            if not project_name:
                messagebox.showwarning("Aviso", "Por favor, insira um nome para o projeto.")
                return
            
            project_path = self.projects_dir / project_name
            if project_path.exists():
                messagebox.showerror("Erro", "Um projeto com este nome já existe!")
                return
            
            project_path.mkdir(parents=True)
            self.current_project = project_path
            dialog.destroy()
            self.show_main_interface()
        
        ttk.Button(dialog, text="Criar", command=confirm_creation).pack(pady=10)
        
        dialog.bind('<Return>', lambda e: confirm_creation())
    
    def open_selected_project(self):
        """Abre o projeto selecionado"""
        selection = self.projects_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione um projeto.")
            return
        
        project_name = self.projects_listbox.get(selection[0])
        self.current_project = self.projects_dir / project_name
        self.show_main_interface()
    
    def show_main_interface(self):
        """Interface principal com abas"""
        self.clear_window()
        
        # Título com nome do projeto
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(header, text=f"Projeto: {self.current_project.name}", 
                 font=('Arial', 14, 'bold')).pack(side='left')
        
        ttk.Button(header, text="Voltar", 
                  command=self.show_project_selection).pack(side='right')
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Aba 1: Vídeo
        self.video_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.video_tab, text="Vídeo")
        self.setup_video_tab()
        
        # Aba 2: Editor
        self.editor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.editor_tab, text="Editor de Vídeo")
        self.setup_editor_tab()
        
        # Aba 3: Processamento
        self.processing_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.processing_tab, text="Processamento Colab")
        self.setup_processing_tab()
        
        # Aba 4: Resultados
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Resultados")
        self.setup_results_tab()
        
        # Verificar se já existe vídeo no projeto
        self.check_existing_video()
    
    def setup_video_tab(self):
        """Configura aba de vídeo"""
        # Canvas com scrollbar
        canvas = tk.Canvas(self.video_tab)
        scrollbar = ttk.Scrollbar(self.video_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Adicionar Vídeo ao Projeto", 
                 font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Status do vídeo
        self.video_status_label = ttk.Label(frame, text="Nenhum vídeo adicionado", 
                                           font=('Arial', 11))
        self.video_status_label.pack(pady=10)
        
        # Botões de ação
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(pady=20)
        
        self.upload_btn = ttk.Button(buttons_frame, text="Upload de Vídeo",
                                     command=self.upload_video, width=20)
        self.upload_btn.grid(row=0, column=0, padx=10, pady=10)
        
        self.record_btn = ttk.Button(buttons_frame, text="Gravar pela Webcam",
                                     command=self.start_webcam_recording, width=20)
        self.record_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Frame para preview da webcam
        self.webcam_frame = ttk.LabelFrame(frame, text="Preview da Webcam", padding="10")
        self.webcam_frame.pack(pady=20, fill='both', expand=True)
        
        self.webcam_label = ttk.Label(self.webcam_frame, text="Webcam inativa")
        self.webcam_label.pack()
        
        # Controles de gravação
        self.recording_controls = ttk.Frame(frame)
        
        self.stop_record_btn = ttk.Button(self.recording_controls, 
                                         text="Parar Gravação",
                                         command=self.stop_webcam_recording,
                                         state='disabled')
        self.stop_record_btn.pack(side='left', padx=5)
        
        self.save_record_btn = ttk.Button(self.recording_controls,
                                         text="Salvar Gravação",
                                         command=self.save_recorded_video,
                                         state='disabled')
        self.save_record_btn.pack(side='left', padx=5)
    
    def setup_editor_tab(self):
        """Configura aba do editor de vídeo"""
        # Canvas com scrollbar
        canvas = tk.Canvas(self.editor_tab)
        scrollbar = ttk.Scrollbar(self.editor_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Editor de Vídeo - Cortar Início e Fim", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.editor_status_label = ttk.Label(frame, 
                                            text="Carregue um vídeo primeiro",
                                            font=('Arial', 11))
        self.editor_status_label.pack(pady=10)
        
        # Frame para preview do vídeo
        preview_frame = ttk.LabelFrame(frame, text="Preview", padding="10")
        preview_frame.pack(pady=10, fill='both', expand=True)
        
        self.video_preview_label = ttk.Label(preview_frame, 
                                            text="Nenhum frame para exibir")
        self.video_preview_label.pack()
        
        # Controles de corte
        controls_frame = ttk.LabelFrame(frame, text="Controles de Corte", padding="10")
        controls_frame.pack(fill='x', pady=10)
        
        # Slider de início
        ttk.Label(controls_frame, text="Início do Vídeo:").grid(row=0, column=0, sticky='w', pady=5)
        self.start_slider = ttk.Scale(controls_frame, from_=0, to=100, 
                                     orient='horizontal', command=self.update_start_frame)
        self.start_slider.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        self.start_time_label = ttk.Label(controls_frame, text="00:00:00")
        self.start_time_label.grid(row=0, column=2, padx=5)
        
        # Slider de fim
        ttk.Label(controls_frame, text="Fim do Vídeo:").grid(row=1, column=0, sticky='w', pady=5)
        self.end_slider = ttk.Scale(controls_frame, from_=0, to=100, 
                                   orient='horizontal', command=self.update_end_frame)
        self.end_slider.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        self.end_time_label = ttk.Label(controls_frame, text="00:00:00")
        self.end_time_label.grid(row=1, column=2, padx=5)
        
        controls_frame.columnconfigure(1, weight=1)
        
        # Informações do vídeo
        info_frame = ttk.Frame(frame)
        info_frame.pack(pady=10)
        
        self.video_info_label = ttk.Label(info_frame, text="", font=('Arial', 10))
        self.video_info_label.pack()
        
        # Botões de ação
        action_frame = ttk.Frame(frame)
        action_frame.pack(pady=10)
        
        self.preview_cut_btn = ttk.Button(action_frame, text="Visualizar Corte",
                                         command=self.preview_cut, state='disabled')
        self.preview_cut_btn.grid(row=0, column=0, padx=5)
        
        self.save_cut_btn = ttk.Button(action_frame, text="Salvar Vídeo Cortado",
                                      command=self.save_cut_video, state='disabled')
        self.save_cut_btn.grid(row=0, column=1, padx=5)
    
    def setup_processing_tab(self):
        """Configura aba de processamento no Colab"""
        # Canvas com scrollbar
        canvas = tk.Canvas(self.processing_tab)
        scrollbar = ttk.Scrollbar(self.processing_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Processamento no Google Colab", 
                 font=('Arial', 14, 'bold')).pack(pady=20)
        
        ttk.Label(frame, text="Quando o vídeo estiver pronto, clique no botão abaixo\n"
                             "para abrir o notebook do Colab e processar o vídeo.",
                 font=('Arial', 11), justify='center').pack(pady=20)
        
        # URL do Colab (pode ser configurado)
        url_frame = ttk.LabelFrame(frame, text="URL do Notebook Colab", padding="10")
        url_frame.pack(fill='x', pady=20, padx=50)
        
        self.colab_url_var = tk.StringVar(value="https://colab.research.google.com/drive/194MdVlQTAoZEOzl64pkQb28im5bM9PST?usp=sharing")
        url_entry = ttk.Entry(url_frame, textvariable=self.colab_url_var, 
                             font=('Arial', 10))
        url_entry.pack(fill='x', pady=5)
        
        ttk.Label(url_frame, text="Cole aqui o link do seu notebook Mobile_cloud.ipynb",
                 font=('Arial', 9), foreground='gray').pack()
        
        # Botão para abrir Colab
        ttk.Button(frame, text="Abrir Google Colab",
                  command=self.open_colab, width=25).pack(pady=20)
        
        # Instruções
        instructions_frame = ttk.LabelFrame(frame, text="Instruções", padding="10")
        instructions_frame.pack(fill='both', expand=True, pady=10, padx=50)
        
        instructions = """
        PREPARAÇÃO (faça uma vez):
        1. No Google Drive, vincule a pasta local "Ubiquos_Mobilize_BodyModel"
        
        PROCESSAMENTO:
        2. Certifique-se de que o vídeo foi cortado e está pronto
        3. Clique em "Abrir Google Colab" abaixo
        4. No Colab, execute o notebook Mobile_cloud.ipynb
        5. Selecione o número do projeto
        6. Aguarde o processamento na nuvem (pode levar alguns minutos)
        7. Os arquivos processados serão salvos automaticamente no Drive e na pasta local
        
        VISUALIZAÇÃO:
        8. Acesse a aba "Resultados" e clique em "Processar Resultados"
        9. Visualize os gráficos e vídeos de análise de marcha
        """
        
        ttk.Label(instructions_frame, text=instructions, 
                 font=('Arial', 10), justify='left').pack(anchor='w')
    
    def setup_results_tab(self):
        """Configura aba de resultados"""
        # Canvas com scrollbar
        canvas = tk.Canvas(self.results_tab)
        scrollbar = ttk.Scrollbar(self.results_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = ttk.Frame(scrollable_frame, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Processamento de Resultados", 
                 font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Frame para status e botão de reload
        status_frame = ttk.Frame(frame)
        status_frame.pack(pady=10)
        
        self.results_status_label = ttk.Label(status_frame, text="Verificando arquivos...", 
                                             font=('Arial', 11))
        self.results_status_label.pack(side='left', padx=(0, 10))
        
        self.reload_files_btn = ttk.Button(status_frame, text="🔄 Verificar Arquivos",
                                          command=self.check_results_files, width=18)
        self.reload_files_btn.pack(side='left')
        
        # Botão para processar resultados
        self.process_results_btn = ttk.Button(frame, text="Processar Resultados",
                                             command=self.process_results,
                                             state='disabled', width=25)
        self.process_results_btn.pack(pady=10)
        
        # Frame para vídeos lado a lado
        self.videos_frame = ttk.LabelFrame(frame, text="Vídeos Comparativos", padding="10")
        self.videos_frame.pack(pady=20, fill='both', expand=True)
        
        videos_container = ttk.Frame(self.videos_frame)
        videos_container.pack(fill='both', expand=True)
        
        # Vídeo original
        left_frame = ttk.Frame(videos_container)
        left_frame.grid(row=0, column=0, padx=10, sticky='nsew')
        ttk.Label(left_frame, text="Vídeo Original", font=('Arial', 10, 'bold')).pack()
        self.original_video_label = ttk.Label(left_frame, text="Aguardando processamento")
        self.original_video_label.pack()
        
        # Vídeo esqueleto
        right_frame = ttk.Frame(videos_container)
        right_frame.grid(row=0, column=1, padx=10, sticky='nsew')
        ttk.Label(right_frame, text="Vídeo Esqueleto", font=('Arial', 10, 'bold')).pack()
        self.skeleton_video_label = ttk.Label(right_frame, text="Aguardando processamento")
        self.skeleton_video_label.pack()
        
        videos_container.columnconfigure(0, weight=1)
        videos_container.columnconfigure(1, weight=1)
        
        # Controles do player
        self.player_controls = ttk.Frame(frame)
        self.player_controls.pack(pady=10)
        
        self.play_btn = ttk.Button(self.player_controls, text="▶ Play", 
                                   command=self.play_videos, state='disabled')
        self.play_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = ttk.Button(self.player_controls, text="⏸ Pause",
                                    command=self.pause_videos, state='disabled')
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.stop_btn = ttk.Button(self.player_controls, text="⏹ Stop",
                                   command=self.stop_videos, state='disabled')
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        # Slider de progresso
        progress_frame = ttk.Frame(frame)
        progress_frame.pack(fill='x', pady=10, padx=50)
        
        self.video_progress = ttk.Scale(progress_frame, from_=0, to=100,
                                       orient='horizontal', command=self.seek_videos)
        self.video_progress.pack(fill='x')
        
        self.time_label = ttk.Label(progress_frame, text="00:00 / 00:00")
        self.time_label.pack()
        
        # Frame para gráficos
        self.graphs_frame = ttk.LabelFrame(frame, text="Gráficos de Análise", padding="10")
        self.graphs_frame.pack(pady=20, fill='both', expand=True)
        
        self.graphs_container = ttk.Frame(self.graphs_frame)
        self.graphs_container.pack(fill='both', expand=True)
        
        # Barra de progresso (posicionada após os blocos de vídeos e gráficos)
        self.processing_progress_frame = ttk.Frame(frame)
        self.processing_progress_frame.pack(pady=10, fill='x', padx=50)
        
        self.processing_progress = ttk.Progressbar(self.processing_progress_frame, 
                                                   mode='determinate', length=400)
        self.processing_progress.pack(fill='x')
        
        self.processing_progress_label = ttk.Label(self.processing_progress_frame, 
                                                   text="", font=('Arial', 9))
        self.processing_progress_label.pack()
        
        # Esconder inicialmente
        self.processing_progress_frame.pack_forget()
        
        # Inicializar variáveis de vídeo
        self.video_playing = False
        self.video_paused = False
        self.original_cap = None
        self.skeleton_cap = None
        self.current_frame = 0
        self.total_video_frames = 0
        
        # Verificar arquivos ao inicializar
        self.check_results_files()
    
    def check_existing_video(self):
        """Verifica se já existe vídeo no projeto"""
        if self.current_project:
            video_files = list(self.current_project.glob("video.*"))
            if video_files:
                self.current_video_path = video_files[0]
                self.update_video_status()
                self.load_video_for_editing()
    
    def upload_video(self):
        """Faz upload de um vídeo"""
        file_path = filedialog.askopenfilename(
            title="Selecione um Vídeo",
            filetypes=[("Vídeos", "*.mp4 *.avi *.mov *.mkv"), ("Todos", "*.*")]
        )
        
        if file_path:
            # Copiar vídeo para pasta do projeto
            ext = Path(file_path).suffix
            dest_path = self.current_project / f"video{ext}"
            
            try:
                shutil.copy2(file_path, dest_path)
                self.current_video_path = dest_path
                self.update_video_status()
                self.load_video_for_editing()
                messagebox.showinfo("Sucesso", "Vídeo adicionado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao copiar vídeo: {str(e)}")
    
    def start_webcam_recording(self):
        """Inicia gravação pela webcam"""
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a webcam.")
            return
        
        self.is_recording = False
        self.recorded_frames = []
        self.record_btn.config(state='disabled')
        self.upload_btn.config(state='disabled')
        
        # Iniciar thread para exibir webcam
        self.webcam_thread = threading.Thread(target=self.show_webcam, daemon=True)
        self.webcam_thread.start()
        
        # Iniciar gravação automaticamente
        self.is_recording = True
        self.stop_record_btn.config(state='normal')
        self.recording_controls.pack(pady=10)
    
    def show_webcam(self):
        """Exibe preview da webcam respeitando aspect ratio"""
        while self.video_capture and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret:
                if self.is_recording:
                    self.recorded_frames.append(frame.copy())
                
                # Converter para exibição no Tkinter mantendo aspect ratio
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                height, width = frame_rgb.shape[:2]
                max_width = 640
                max_height = 480
                
                scale_w = max_width / width
                scale_h = max_height / height
                scale = min(scale_w, scale_h)
                
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
                img = Image.fromarray(frame_resized)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.webcam_label.imgtk = imgtk
                self.webcam_label.configure(image=imgtk)
            else:
                break
    
    def stop_webcam_recording(self):
        """Para a gravação"""
        self.is_recording = False
        self.stop_record_btn.config(state='disabled')
        self.save_record_btn.config(state='normal')
    
    def save_recorded_video(self):
        """Salva o vídeo gravado"""
        if not self.recorded_frames:
            messagebox.showwarning("Aviso", "Nenhum frame gravado.")
            return
        
        # Liberar webcam
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        
        self.webcam_label.configure(image='', text="Salvando vídeo...")
        
        # Salvar vídeo
        dest_path = self.current_project / "video.mp4"
        
        try:
            height, width, _ = self.recorded_frames[0].shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(dest_path), fourcc, 20.0, (width, height))
            
            for frame in self.recorded_frames:
                out.write(frame)
            
            out.release()
            
            self.current_video_path = dest_path
            self.recorded_frames = []
            
            self.update_video_status()
            self.load_video_for_editing()
            
            self.record_btn.config(state='normal')
            self.upload_btn.config(state='normal')
            self.save_record_btn.config(state='disabled')
            self.recording_controls.pack_forget()
            
            self.webcam_label.configure(text="Webcam inativa")
            
            messagebox.showinfo("Sucesso", "Vídeo gravado e salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar vídeo: {str(e)}")
    
    def update_video_status(self):
        """Atualiza status do vídeo na interface"""
        if self.current_video_path and self.current_video_path.exists():
            size_mb = self.current_video_path.stat().st_size / (1024 * 1024)
            self.video_status_label.config(
                text=f"Vídeo: {self.current_video_path.name} ({size_mb:.2f} MB)"
            )
    
    def load_video_for_editing(self):
        """Carrega vídeo no editor"""
        if not self.current_video_path or not self.current_video_path.exists():
            return
        
        cap = cv2.VideoCapture(str(self.current_video_path))
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        
        self.start_frame = 0
        self.end_frame = self.total_frames - 1
        
        # Atualizar sliders
        self.start_slider.config(to=self.total_frames - 1)
        self.end_slider.config(to=self.total_frames - 1)
        self.start_slider.set(0)
        self.end_slider.set(self.total_frames - 1)
        
        # Mostrar primeiro frame
        ret, frame = cap.read()
        if ret:
            self.show_frame(frame)
        
        cap.release()
        
        # Atualizar informações
        duration = self.total_frames / self.fps if self.fps > 0 else 0
        self.editor_status_label.config(
            text=f"Vídeo carregado: {self.current_video_path.name}"
        )
        self.video_info_label.config(
            text=f"Frames: {self.total_frames} | FPS: {self.fps:.2f} | "
                 f"Duração: {self.format_time(duration)}"
        )
        
        # Ativar botões
        self.preview_cut_btn.config(state='normal')
        self.save_cut_btn.config(state='normal')
        
        self.update_time_labels()
    
    def show_frame(self, frame):
        """Exibe um frame no preview respeitando aspect ratio"""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Calcular dimensões mantendo aspect ratio
        height, width = frame_rgb.shape[:2]
        max_width = 640
        max_height = 480
        
        # Calcular scale factor mantendo aspect ratio
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h)
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        frame_resized = cv2.resize(frame_rgb, (new_width, new_height))
        img = Image.fromarray(frame_resized)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_preview_label.imgtk = imgtk
        self.video_preview_label.configure(image=imgtk, text="")
    
    def update_start_frame(self, value):
        """Atualiza frame de início"""
        self.start_frame = int(float(value))
        if self.start_frame >= self.end_frame:
            self.start_frame = max(0, self.end_frame - 1)
            self.start_slider.set(self.start_frame)
        self.update_time_labels()
        self.preview_frame_at(self.start_frame)
    
    def update_end_frame(self, value):
        """Atualiza frame de fim"""
        self.end_frame = int(float(value))
        if self.end_frame <= self.start_frame:
            self.end_frame = min(self.total_frames - 1, self.start_frame + 1)
            self.end_slider.set(self.end_frame)
        self.update_time_labels()
        self.preview_frame_at(self.end_frame)
    
    def update_time_labels(self):
        """Atualiza labels de tempo"""
        if self.fps > 0:
            start_time = self.start_frame / self.fps
            end_time = self.end_frame / self.fps
            duration = (self.end_frame - self.start_frame) / self.fps
            
            self.start_time_label.config(text=self.format_time(start_time))
            self.end_time_label.config(text=self.format_time(end_time))
            
            self.video_info_label.config(
                text=f"Frames: {self.total_frames} | FPS: {self.fps:.2f} | "
                     f"Duração original: {self.format_time(self.total_frames / self.fps)} | "
                     f"Duração cortada: {self.format_time(duration)}"
            )
    
    def format_time(self, seconds):
        """Formata tempo em HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def preview_frame_at(self, frame_num):
        """Mostra preview de um frame específico"""
        if not self.current_video_path:
            return
        
        cap = cv2.VideoCapture(str(self.current_video_path))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if ret:
            self.show_frame(frame)
        cap.release()
    
    def preview_cut(self):
        """Visualiza o corte (mostra primeiro e último frame)"""
        self.preview_frame_at(self.start_frame)
        messagebox.showinfo("Preview", 
                           f"Frame inicial: {self.start_frame}\n"
                           f"Frame final: {self.end_frame}\n"
                           f"Total de frames no corte: {self.end_frame - self.start_frame + 1}")
    
    def save_cut_video(self):
        """Salva vídeo cortado"""
        if not self.current_video_path:
            return
        
        # Confirmar
        duration = (self.end_frame - self.start_frame) / self.fps if self.fps > 0 else 0
        result = messagebox.askyesno(
            "Confirmar Corte",
            f"Deseja salvar o vídeo cortado?\n\n"
            f"Duração: {self.format_time(duration)}\n"
            f"Frames: {self.end_frame - self.start_frame + 1}\n\n"
            f"O vídeo original será substituído."
        )
        
        if not result:
            return
        
        try:
            # Criar vídeo temporário
            temp_path = self.current_project / "video_temp.mp4"
            
            cap = cv2.VideoCapture(str(self.current_video_path))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(temp_path), fourcc, self.fps, (width, height))
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)
            
            for i in range(self.start_frame, self.end_frame + 1):
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
                else:
                    break
            
            cap.release()
            out.release()
            
            # Substituir vídeo original
            self.current_video_path.unlink()
            temp_path.rename(self.current_video_path)
            
            # Recarregar vídeo
            self.load_video_for_editing()
            
            messagebox.showinfo("Sucesso", "Vídeo cortado e salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cortar vídeo: {str(e)}")
    
    def open_colab(self):
        """Abre o Google Colab no navegador"""
        url = self.colab_url_var.get()
        if url:
            webbrowser.open(url)
            messagebox.showinfo("Google Colab", 
                              "O notebook foi aberto no navegador.\n"
                              "Após processar o vídeo no Colab, "
                              "baixe os modelos para a pasta do projeto.")
        else:
            messagebox.showwarning("Aviso", "Por favor, configure a URL do Colab.")
    
    def check_results_files(self):
        """Verifica se os arquivos necessários estão presentes e carrega resultados se existirem"""
        if not self.current_project:
            return
        
        required_files = ['keypoints3d.npz', 'ang.pkl', 'dataset.pkl']
        missing_files = []
        
        for file in required_files:
            file_path = self.current_project / file
            if not file_path.exists():
                missing_files.append(file)
        
        if missing_files:
            self.results_status_label.config(
                text=f"Arquivos faltando: {', '.join(missing_files)}\n"
                     f"Execute o processamento no Colab primeiro.",
                foreground='red'
            )
            self.process_results_btn.config(state='disabled')
        else:
            self.results_status_label.config(
                text="✓ Todos os arquivos necessários encontrados!",
                foreground='green'
            )
            self.process_results_btn.config(state='normal')
            
            # Verificar se já existem resultados processados
            results_dir = self.current_project / "Resultados"
            if results_dir.exists():
                graph_files = ['ground_contact.png', 'knee_angles_time.png', 
                              'knee_left_cycles.png', 'knee_right_cycles.png']
                video_files = ['reconstruction.mp4', 'skeleton.mp4']
                
                has_graphs = any((results_dir / f).exists() for f in graph_files)
                has_videos = any((results_dir / f).exists() for f in video_files)
                
                if has_graphs or has_videos:
                    # Carregar resultados existentes
                    self.results_status_label.config(
                        text="✓ Resultados já processados! Carregando...",
                        foreground='blue'
                    )
                    if has_graphs:
                        self.load_results_graphs(results_dir)
                    if has_videos:
                        self.load_videos_for_playback(results_dir)
    
    def process_results(self):
        """Processa os resultados baseado no Mobile_Local.ipynb"""
        if not self.current_project:
            return
        
        # Executar processamento em thread separada para não congelar a UI
        processing_thread = threading.Thread(target=self._process_results_thread, daemon=True)
        processing_thread.start()
    
    def _process_results_thread(self):
        """Thread de processamento dos resultados"""
        try:
            import pickle
            from matplotlib import pyplot as plt
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            
            # Criar pasta de resultados
            results_dir = self.current_project / "Resultados"
            results_dir.mkdir(exist_ok=True)
            
            # Mostrar barra de progresso
            self.processing_progress_frame.pack(pady=10, fill='x', padx=50)
            self.processing_progress['value'] = 0
            self.processing_progress_label.config(text="Iniciando processamento...")
            self.process_results_btn.config(state='disabled')
            self.root.update()
            
            # Carregar dados
            self.processing_progress['value'] = 10
            self.processing_progress_label.config(text="Carregando dados...")
            self.root.update()
            
            with open(self.current_project / 'keypoints3d.npz', 'rb') as f:
                pose3d = np.load(f, allow_pickle=True)['arr_0']
            
            with open(self.current_project / 'ang.pkl', 'rb') as f:
                ang = pickle.load(f)
            
            with open(self.current_project / 'dataset.pkl', 'rb') as f:
                dataset = pickle.load(f)
            
            # Processar pose
            self.processing_progress['value'] = 20
            self.processing_progress_label.config(text="Processando dados 3D...")
            self.root.update()
            
            pose = pose3d.copy()
            pose = pose[:, :, [0, 2, 1]]
            pose[:, :, 2] *= -1
            pose /= 1000.0
            pose = pose - np.min(pose, axis=1, keepdims=True)
            
            timestamps = dataset[0]
            
            # Joint names e edges (do notebook)
            joint_names = ['backneck', 'upperback', 'clavicle', 'sternum', 'umbilicus',
                   'lfronthead', 'lbackhead', 'lback', 'lshom', 'lupperarm', 'lelbm',
                   'lforearm', 'lwrithumbside', 'lwripinkieside', 'lfin', 'lasis',
                   'lpsis', 'lfrontthigh', 'lthigh', 'lknem', 'lankm', 'lhee',
                   'lfifthmetatarsal', 'ltoe', 'lcheek', 'lbreast', 'lelbinner',
                   'lwaist', 'lthumb', 'lfrontinnerthigh', 'linnerknee', 'lshin',
                   'lfirstmetatarsal', 'lfourthtoe', 'lscapula', 'lbum', 'rfronthead',
                   'rbackhead', 'rback', 'rshom', 'rupperarm', 'relbm', 'rforearm',
                   'rwrithumbside', 'rwripinkieside', 'rfin', 'rasis', 'rpsis',
                   'rfrontthigh', 'rthigh', 'rknem', 'rankm', 'rhee',
                   'rfifthmetatarsal', 'rtoe', 'rcheek', 'rbreast', 'relbinner',
                   'rwaist', 'rthumb', 'rfrontinnerthigh', 'rinnerknee', 'rshin',
                   'rfirstmetatarsal', 'rfourthtoe', 'rscapula', 'rbum', 'head',
                   'mhip', 'pelv', 'thor', 'lank', 'lelb', 'lhip', 'lhan', 'lkne',
                   'lsho', 'lwri', 'lfoo', 'rank', 'relb', 'rhip', 'rhan', 'rkne',
                   'rsho', 'rwri', 'rfoo']
            
            joint_edges = [[67, 70], [68, 69], [68, 73], [68, 81], [69, 70],
                          [70, 76], [70, 84], [71, 75], [71, 78], [72, 76],
                          [72, 77], [73, 75], [74, 77], [79, 83], [79, 86],
                          [80, 84], [80, 85], [81, 83], [82, 85]]
            
            # Gerar vídeo do esqueleto
            self.processing_progress['value'] = 30
            self.processing_progress_label.config(text="Gerando vídeo do esqueleto MuJoCo...")
            self.root.update()
            
            self.generate_skeleton_video(pose, joint_edges, results_dir)
            
            # Detectar contato com o solo
            self.processing_progress['value'] = 50
            self.processing_progress_label.config(text="Analisando contato com o solo...")
            self.root.update()
            
            lfoot_idx = joint_names.index('lfourthtoe')
            rfoot_idx = joint_names.index('rfourthtoe')
            
            lfoot_z_positions = pose[:, lfoot_idx, 2]
            rfoot_z_positions = pose[:, rfoot_idx, 2]
            
            min_z_l = np.min(lfoot_z_positions)
            min_z_r = np.min(rfoot_z_positions)
            ground_contact_threshold = (min_z_l + min_z_r)/2 + 0.025
            
            step_up_l = self.find_cycle_starts(rfoot_z_positions, ground_contact_threshold)
            step_up_r = self.find_cycle_starts(lfoot_z_positions, ground_contact_threshold)
            
            # Gerar gráficos de ângulos ao longo do tempo
            self.processing_progress['value'] = 60
            self.processing_progress_label.config(text="Analisando ângulos das articulações...")
            self.root.update()
            
            try:
                # Importar ForwardKinematics para obter os índices corretos
                from monocular_demos.biomechanics_mjx.forward_kinematics import ForwardKinematics
                fk = ForwardKinematics()
                
                # Obter índices dos joelhos do objeto fk
                knee_idx = np.array([fk.joint_names.index(n) for n in ['knee_angle_r', 'knee_angle_l']])
                
                time = np.array(dataset[0])
                signal_r = -np.degrees(ang[:, knee_idx[0]])
                signal_l = -np.degrees(ang[:, knee_idx[1]])
                
                # Gerar gráfico de ângulos dos joelhos ao longo do tempo
                self.processing_progress['value'] = 65
                self.processing_progress_label.config(text="Gerando gráfico de ângulos dos joelhos...")
                self.root.update()
                
                self.generate_knee_angle_plot(time, signal_r, signal_l, knee_idx, results_dir)
                
                # Obter índices de tornozelos e quadris
                hip_idx = np.array([fk.joint_names.index(n) for n in ['hip_flexion_r', 'hip_flexion_l']])
                ankle_idx = np.array([fk.joint_names.index(n) for n in ['ankle_angle_r', 'ankle_angle_l']])
                
                ankle_signal_r = np.degrees(ang[:, ankle_idx[0]])
                ankle_signal_l = np.degrees(ang[:, ankle_idx[1]])
                hip_signal_r = np.degrees(ang[:, hip_idx[0]])
                hip_signal_l = np.degrees(ang[:, hip_idx[1]])
                
                # Gerar gráfico de ângulos dos tornozelos ao longo do tempo
                self.processing_progress['value'] = 68
                self.processing_progress_label.config(text="Gerando gráfico de ângulos dos tornozelos...")
                self.root.update()
                
                self.generate_ankle_angle_plot(time, ankle_signal_r, ankle_signal_l, ankle_idx, results_dir)
                
                # Gerar gráfico de ângulos dos quadris ao longo do tempo
                self.processing_progress['value'] = 71
                self.processing_progress_label.config(text="Gerando gráfico de ângulos dos quadris...")
                self.root.update()
                
                self.generate_hip_angle_plot(time, hip_signal_r, hip_signal_l, hip_idx, results_dir)
                
                # Note: step_up_r é usado com signal_l e vice-versa (como no notebook)
                self.processing_progress['value'] = 75
                self.processing_progress_label.config(text="Gerando ciclos de marcha - joelho esquerdo...")
                self.root.update()
                
                self.generate_cycle_plot(time, signal_l, step_up_r, 
                                        "Ângulo do Joelho Esquerdo", results_dir, "knee_left")
                
                self.processing_progress['value'] = 78
                self.processing_progress_label.config(text="Gerando ciclos de marcha - joelho direito...")
                self.root.update()
                
                self.generate_cycle_plot(time, signal_r, step_up_l,
                                        "Ângulo do Joelho Direito", results_dir, "knee_right")
                
                # Gerar ciclos de tornozelo
                self.processing_progress['value'] = 81
                self.processing_progress_label.config(text="Gerando ciclos de marcha - tornozelo esquerdo...")
                self.root.update()
                
                self.generate_cycle_plot(time, ankle_signal_l, step_up_r,
                                        "Ângulo do Tornozelo Esquerdo", results_dir, "ankle_left")
                
                self.processing_progress['value'] = 84
                self.processing_progress_label.config(text="Gerando ciclos de marcha - tornozelo direito...")
                self.root.update()
                
                self.generate_cycle_plot(time, ankle_signal_r, step_up_l,
                                        "Ângulo do Tornozelo Direito", results_dir, "ankle_right", erro=0.1)
                
                # Gerar ciclos de quadril
                self.processing_progress['value'] = 87
                self.processing_progress_label.config(text="Gerando ciclos de marcha - quadril esquerdo...")
                self.root.update()
                
                self.generate_cycle_plot(time, hip_signal_l, step_up_r,
                                        "Ângulo do Quadril Esquerdo", results_dir, "hip_left")
                
                self.processing_progress['value'] = 90
                self.processing_progress_label.config(text="Gerando ciclos de marcha - quadril direito...")
                self.root.update()
                
                self.generate_cycle_plot(time, hip_signal_r, step_up_l,
                                        "Ângulo do Quadril Direito", results_dir, "hip_right")
            except Exception as e:
                print(f"Erro ao gerar gráficos: {e}")
            
            # Carregar gráficos gerados
            self.processing_progress['value'] = 93
            self.processing_progress_label.config(text="Carregando gráficos...")
            self.root.update()
            
            self.load_results_graphs(results_dir)
            
            # Carregar vídeos
            self.processing_progress['value'] = 96
            self.processing_progress_label.config(text="Carregando vídeos...")
            self.root.update()
            
            self.load_videos_for_playback(results_dir)
            
            # Concluído
            self.processing_progress['value'] = 100
            self.processing_progress_label.config(text="✓ Processamento concluído!")
            self.root.update()
            
            self.results_status_label.config(
                text="✓ Processamento concluído com sucesso!",
                foreground='green'
            )
            
            # Reabilitar botão
            self.process_results_btn.config(state='normal')
            
            messagebox.showinfo("Sucesso", 
                              f"Resultados processados e salvos em:\n{results_dir}")
            
            # Esconder barra de progresso após 2 segundos
            self.root.after(2000, lambda: self.processing_progress_frame.pack_forget())
        
        except Exception as e:
            self.processing_progress_frame.pack_forget()
            self.process_results_btn.config(state='normal')
            
            self.results_status_label.config(
                text=f"Erro no processamento: {str(e)}",
                foreground='red'
            )
            messagebox.showerror("Erro", f"Erro ao processar resultados:\n{str(e)}")
    
    def find_cycle_starts(self, foot_z_positions, threshold):
        """Detecta início dos ciclos de marcha - método do notebook"""
        step_up = np.full(foot_z_positions.size, False)
        decrease = False
        got_zero = (foot_z_positions[0] < threshold)
        last_spik = 0
        
        for i in range(foot_z_positions.size - 2):
            if foot_z_positions[i] > foot_z_positions[i + 1] and not (decrease or got_zero):
                last_spik = i
                decrease = True
            if foot_z_positions[i] < foot_z_positions[i + 1] and foot_z_positions[i] > threshold and decrease:
                decrease = False
            if foot_z_positions[i] < threshold:
                got_zero = True
            else:
                got_zero = False
            if decrease and got_zero:
                step_up[last_spik] = True
        
        return step_up
    
    def generate_skeleton_video(self, pose, joint_edges, output_dir):
        """Gera vídeo do esqueleto 3D usando MuJoCo visualization"""
        skeleton_video_path = output_dir / "reconstruction.mp4"
        
        try:
            # Importar módulos necessários do monocular_demos
            from monocular_demos.biomechanics_mjx.visualize import render_trajectory
            from monocular_demos.biomechanics_mjx.forward_kinematics import ForwardKinematics
            
            # Carregar ang.pkl se ainda não foi carregado
            import pickle
            with open(self.current_project / 'ang.pkl', 'rb') as f:
                ang = pickle.load(f)
            
            # Renderizar trajetória usando MuJoCo
            render_trajectory(ang, str(skeleton_video_path), xml_path=None)
            
            return skeleton_video_path
            
        except ImportError as e:
            # Se monocular_demos não estiver disponível, usar método alternativo simples
            print(f"MuJoCo não disponível: {e}")
            messagebox.showwarning(
                "Aviso",
                "Biblioteca monocular_demos não encontrada.\n"
                "Usando visualização simplificada.\n\n"
                "Para usar a visualização MuJoCo completa, instale:\n"
                "pip install git+https://github.com/peabody124/GaitTransformer\n"
                "git clone https://github.com/IntelligentSensingAndRehabilitation/monocular-demos.git\n"
                "cd monocular-demos && pip install ."
            )
            return self.generate_simple_skeleton_video(pose, joint_edges, output_dir)
        except Exception as e:
            print(f"Erro ao gerar vídeo MuJoCo: {e}")
            return self.generate_simple_skeleton_video(pose, joint_edges, output_dir)
    
    def generate_simple_skeleton_video(self, pose, joint_edges, output_dir):
        """Gera vídeo do esqueleto 3D (versão simplificada)"""
        skeleton_video_path = output_dir / "skeleton.mp4"
        
        # Configurações do vídeo
        fps = 30
        width, height = 640, 480
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(skeleton_video_path), fourcc, fps, (width, height))
        
        for frame_idx in range(len(pose)):
            # Criar imagem em branco
            img = np.ones((height, width, 3), dtype=np.uint8) * 255
            
            # Projetar pose 3D em 2D (vista lateral)
            frame_pose = pose[frame_idx]
            
            # Normalizar para caber na tela
            x_coords = frame_pose[:, 0]
            z_coords = frame_pose[:, 2]
            
            x_min, x_max = x_coords.min(), x_coords.max()
            z_min, z_max = z_coords.min(), z_coords.max()
            
            margin = 50
            scale_x = (width - 2 * margin) / (x_max - x_min + 0.001)
            scale_z = (height - 2 * margin) / (z_max - z_min + 0.001)
            scale = min(scale_x, scale_z)
            
            # Converter coordenadas
            points_2d = []
            for point in frame_pose:
                x = int((point[0] - x_min) * scale + margin)
                y = int(height - ((point[2] - z_min) * scale + margin))
                points_2d.append((x, y))
            
            # Desenhar edges
            for edge in joint_edges:
                pt1 = points_2d[edge[0]]
                pt2 = points_2d[edge[1]]
                cv2.line(img, pt1, pt2, (0, 0, 0), 2)
            
            # Desenhar pontos
            for point in points_2d:
                cv2.circle(img, point, 4, (255, 0, 0), -1)
            
            out.write(img)
        
        out.release()
        return skeleton_video_path
    
    def generate_knee_angle_plot(self, time, signal_r, signal_l, knee_idx, output_dir):
        """Gera gráfico de ângulos dos joelhos ao longo do tempo"""
        plt.figure(figsize=(12, 6))
        plt.plot(time, signal_r, label='Joelho Direito', linewidth=2)
        plt.plot(time, signal_l, label='Joelho Esquerdo', linewidth=2)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Ângulo do Joelho (graus)')
        plt.title('Ângulos do Joelho ao Longo do Tempo')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_dir / 'knee_angles_time.png', dpi=150)
        plt.close()
    
    def generate_ankle_angle_plot(self, time, signal_r, signal_l, ankle_idx, output_dir):
        """Gera gráfico de ângulos dos tornozelos ao longo do tempo"""
        plt.figure(figsize=(12, 6))
        plt.plot(time, signal_r, label='Tornozelo Direito', linewidth=2)
        plt.plot(time, signal_l, label='Tornozelo Esquerdo', linewidth=2)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Ângulo do Tornozelo (graus)')
        plt.title('Ângulos do Tornozelo ao Longo do Tempo')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_dir / 'ankle_angles_time.png', dpi=150)
        plt.close()
    
    def generate_hip_angle_plot(self, time, signal_r, signal_l, hip_idx, output_dir):
        """Gera gráfico de ângulos dos quadris ao longo do tempo"""
        plt.figure(figsize=(12, 6))
        plt.plot(time, signal_r, label='Quadril Direito', linewidth=2)
        plt.plot(time, signal_l, label='Quadril Esquerdo', linewidth=2)
        plt.xlabel('Tempo (s)')
        plt.ylabel('Ângulo do Quadril (graus)')
        plt.title('Ângulos do Quadril ao Longo do Tempo')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_dir / 'hip_angles_time.png', dpi=150)
        plt.close()
    
    def generate_cycle_plot(self, time, signal, steps, label, output_dir, filename, erro=0.15):
        """Gera gráfico de ciclos de marcha normalizados - exatamente como no notebook"""
        cycle_starts = np.where(steps)[0]
        
        if len(cycle_starts) < 2:
            return
        
        colors = plt.cm.get_cmap('hsv', len(cycle_starts) + 1)  # +1 como no notebook
        
        cycles = []
        periods = []
        period_mean = 0
        
        for i in range(len(cycle_starts) - 1):
            start = cycle_starts[i]
            end = cycle_starts[i + 1]
            segment = signal[start:end]
            period = time[end] - time[start]
            periods.append(period)
            
            # Reamostrar cada ciclo para o mesmo tamanho (100 pontos)
            normalized = np.interp(
                np.linspace(0, 1, 100),
                np.linspace(0, 1, len(segment)),
                segment
            )
            cycles.append(normalized)
            period_mean += period
        
        if len(cycles) == 0:
            return
        
        period_mean = period_mean / len(cycles)
        
        # Filtrar ciclos com erro - usando a lógica exata do notebook
        filtered_cycles = []
        filtered_periods = []
        
        for i, (c, p) in enumerate(zip(cycles, periods)):
            # Lógica do notebook: excluir se fora da faixa
            if not (p * (1 + erro) < period_mean or p * (1 - erro) > period_mean):
                filtered_cycles.append(c)
                filtered_periods.append(p)
        
        if len(filtered_cycles) == 0:
            filtered_cycles = cycles
        
        mean_cycle = np.mean(filtered_cycles, axis=0)
        std_deviation = np.std(filtered_cycles, axis=0)
        
        plt.figure(figsize=(10, 5))  # (10, 5) como no notebook
        
        # Plotar todos os ciclos com cores diferentes
        for i, c in enumerate(filtered_cycles):
            plt.plot(np.linspace(0, 100, len(c)), c, alpha=0.5, color=colors(i))
        
        # Linha da média
        plt.plot(np.linspace(0, 100, len(mean_cycle)), mean_cycle, 
                color='red', linewidth=3, alpha=0.8, label="Média")
        
        # Linhas do desvio padrão
        plt.plot(np.linspace(0, 100, len(std_deviation)), mean_cycle + std_deviation,
                color='blue', linestyle='dashed', alpha=0.8, label="Desvio Padrão")
        plt.plot(np.linspace(0, 100, len(std_deviation)), mean_cycle - std_deviation,
                color='blue', linestyle='dashed', alpha=0.8)
        
        plt.title("Ciclos de Caminhada Normalizados (0–100%)")
        plt.xlabel("Percentual do Ciclo (%)")
        plt.ylabel(label)
        plt.legend(loc='upper left')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_dir / f'{filename}_cycles.png', dpi=150)
        plt.close()
    
    def load_results_graphs(self, results_dir):
        """Carrega e exibe os gráficos gerados"""
        # Limpar gráficos anteriores
        for widget in self.graphs_container.winfo_children():
            widget.destroy()
        
        graph_files = [
            'knee_angles_time.png',
            'ankle_angles_time.png',
            'hip_angles_time.png',
            'knee_left_cycles.png',
            'knee_right_cycles.png',
            'ankle_left_cycles.png',
            'ankle_right_cycles.png',
            'hip_left_cycles.png',
            'hip_right_cycles.png'
        ]
        
        row = 0
        for graph_file in graph_files:
            graph_path = results_dir / graph_file
            if graph_path.exists():
                img = Image.open(graph_path)
                img.thumbnail((800, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                label = ttk.Label(self.graphs_container, image=photo)
                label.image = photo  # Manter referência
                label.grid(row=row, column=0, pady=10, padx=10)
                row += 1
    
    def load_videos_for_playback(self, results_dir):
        """Carrega vídeos para reprodução sincronizada"""
        # Procurar por reconstruction.mp4 (MuJoCo) ou skeleton.mp4 (fallback)
        skeleton_video_path = results_dir / "reconstruction.mp4"
        if not skeleton_video_path.exists():
            skeleton_video_path = results_dir / "skeleton.mp4"
        
        if not self.current_video_path or not skeleton_video_path.exists():
            return
        
        self.original_cap = cv2.VideoCapture(str(self.current_video_path))
        self.skeleton_cap = cv2.VideoCapture(str(skeleton_video_path))
        
        self.total_video_frames = int(self.original_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_fps = self.original_cap.get(cv2.CAP_PROP_FPS)
        if self.video_fps <= 0 or self.video_fps > 120:
            self.video_fps = 30.0  # fallback para 30 fps
        self.video_progress.config(to=self.total_video_frames - 1)
        
        # Ativar controles
        self.play_btn.config(state='normal')
        self.stop_btn.config(state='normal')
        
        # Mostrar primeiro frame
        self.current_frame = 0
        self.update_video_frames()
    
    def play_videos(self):
        """Reproduz os vídeos sincronizados"""
        if not self.original_cap or not self.skeleton_cap:
            return
        
        self.video_playing = True
        self.video_paused = False
        self.play_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        
        def play_loop():
            import time
            frame_delay = 1.0 / self.video_fps  # delay correto baseado no FPS real
            
            while self.video_playing and not self.video_paused:
                start_time = time.time()
                
                if self.current_frame >= self.total_video_frames - 1:
                    self.stop_videos()
                    break
                
                self.current_frame += 1
                self.update_video_frames()
                self.video_progress.set(self.current_frame)
                
                # Calcular tempo de espera para manter FPS correto
                elapsed = time.time() - start_time
                sleep_time = max(0, frame_delay - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        
        threading.Thread(target=play_loop, daemon=True).start()
    
    def pause_videos(self):
        """Pausa a reprodução"""
        self.video_paused = True
        self.play_btn.config(state='normal')
        self.pause_btn.config(state='disabled')
    
    def stop_videos(self):
        """Para a reprodução e volta ao início"""
        self.video_playing = False
        self.video_paused = False
        self.current_frame = 0
        
        if self.original_cap and self.skeleton_cap:
            self.original_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.skeleton_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update_video_frames()
        
        self.video_progress.set(0)
        self.play_btn.config(state='normal')
        self.pause_btn.config(state='disabled')
    
    def seek_videos(self, value):
        """Navega para um frame específico"""
        if not self.original_cap or not self.skeleton_cap:
            return
        
        frame_num = int(float(value))
        self.current_frame = frame_num
        
        self.original_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        self.skeleton_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        
        self.update_video_frames()
    
    def update_video_frames(self):
        """Atualiza os frames exibidos"""
        if not self.original_cap or not self.skeleton_cap:
            return
        
        ret1, frame1 = self.original_cap.read()
        ret2, frame2 = self.skeleton_cap.read()
        
        if ret1 and ret2:
            # Original - tamanho aumentado para 480x360
            frame1_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            h1, w1 = frame1_rgb.shape[:2]
            scale = min(480 / w1, 360 / h1)
            new_w1 = int(w1 * scale)
            new_h1 = int(h1 * scale)
            frame1_resized = cv2.resize(frame1_rgb, (new_w1, new_h1))
            img1 = Image.fromarray(frame1_resized)
            photo1 = ImageTk.PhotoImage(img1)
            self.original_video_label.photo = photo1
            self.original_video_label.configure(image=photo1, text="")
            
            # Esqueleto - tamanho aumentado para 480x360
            frame2_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            h2, w2 = frame2_rgb.shape[:2]
            scale = min(480 / w2, 360 / h2)
            new_w2 = int(w2 * scale)
            new_h2 = int(h2 * scale)
            frame2_resized = cv2.resize(frame2_rgb, (new_w2, new_h2))
            img2 = Image.fromarray(frame2_resized)
            photo2 = ImageTk.PhotoImage(img2)
            self.skeleton_video_label.photo = photo2
            self.skeleton_video_label.configure(image=photo2, text="")
            
            # Atualizar tempo
            fps = self.original_cap.get(cv2.CAP_PROP_FPS)
            current_time = self.current_frame / fps if fps > 0 else 0
            total_time = self.total_video_frames / fps if fps > 0 else 0
            self.time_label.config(
                text=f"{self.format_time(current_time)} / {self.format_time(total_time)}"
            )
    
    def clear_window(self):
        """Limpa a janela"""
        for widget in self.root.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
