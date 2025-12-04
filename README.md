# Gait Analysis - Sistema de Análise de Marcha com Processamento Híbrido (GPU/CPU)

## Introdução

Este projeto foi desenvolvido como parte de um trabalho de estudo médico e reabilitação inteligente, baseado no framework [GaitTransformer](https://github.com/peabody124/GaitTransformer) do grupo [IntelligentSensingAndRehabilitation](https://github.com/IntelligentSensingAndRehabilitation). O sistema oferece uma solução completa para análise biomecânica da marcha humana, combinando processamento em nuvem (GPU) com análise local (CPU) através de uma interface gráfica intuitiva.

O projeto visa democratizar o acesso à análise de marcha avançada, permitindo que profissionais da saúde, fisioterapeutas e pesquisadores realizem avaliações biomecânicas detalhadas utilizando apenas vídeos capturados por câmeras convencionais ou webcams, sem necessidade de equipamentos especializados caros como sistemas de captura de movimento.

## Descrição do Projeto

O sistema é dividido em duas etapas principais de processamento:

### **Processamento em Nuvem (GPU - Google Colab)**
Utiliza o notebook `Mobile_cloud.ipynb` para realizar o processamento pesado com aceleração por GPU:
- Extração de keypoints 2D do vídeo usando modelos de pose estimation
- Reconstrução 3D da marcha através do GaitTransformer
- Geração de modelos biomecânicos (keypoints3d.npz, ang.pkl, dataset.pkl)
- Upload dos resultados para Google Drive para processamento local posterior

### **Processamento Local (CPU - Interface GUI)**
Aplicação desktop desenvolvida em Python com Tkinter que permite:
- Gerenciamento de projetos organizados por vídeo
- Upload de vídeos ou gravação direta pela webcam
- Editor básico para corte/trimming de vídeos
- Integração com Google Colab para processamento GPU
- Análise local completa baseada no notebook `Mobile_Local.ipynb`:
  - Visualização biomecânica 3D com MuJoCo (modelo anatômico realista)
  - Análise de contato com o solo e detecção de ciclos de marcha
  - Cálculo de ângulos articulares (joelhos, tornozelos, quadris)
  - Geração de gráficos e relatórios visuais
  - Reprodução sincronizada de vídeo original e modelo biomecânico

### Objetivos

- Facilitar o acesso à análise biomecânica avançada sem equipamentos caros
- Fornecer métricas objetivas para avaliação clínica e reabilitação
- Permitir monitoramento longitudinal de pacientes
- Gerar visualizações compreensíveis para profissionais e pacientes
- Integrar processamento em nuvem (rápido, GPU) com análise local (privado, CPU)

### Aplicações Clínicas

- **Reabilitação**: Monitoramento de progresso pós-cirúrgico ou lesão
- **Diagnóstico**: Identificação de padrões anormais de marcha
- **Geriatria**: Avaliação de risco de quedas em idosos
- **Neurologia**: Análise de marcha em condições como Parkinson
- **Ortopedia**: Avaliação pré e pós-operatória
- **Pesquisa**: Estudos sobre biomecânica e locomoção humana

### Visão de Alto Nível do Sistema

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Captura de     │      │  Processamento   │      │  Análise        │
│  Vídeo          │─────▶│  GPU (Colab)     │─────▶│  Local (CPU)    │
│                 │      │                  │      │                 │
│ • Webcam        │      │ • Pose 2D        │      │ • Visualização  │
│ • Upload        │      │ • Reconstruct 3D │      │ • Gráficos      │
│ • Trimming      │      │ • Biomechanics   │      │ • Métricas      │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

## Funcionalidades

### 1. Gerenciamento de Projetos
- **Criar novos projetos**: Cada projeto é uma pasta separada dentro de `/projetos`
- **Abrir projetos existentes**: Lista todos os projetos disponíveis
- **Organização automática**: Cada vídeo e seus arquivos ficam isolados por projeto
- **Estrutura de pastas**:
  ```
  projetos/
  └── Nome_do_Projeto/
      ├── video.mp4                    # Vídeo original/editado
      ├── keypoints3d.npz              # Keypoints 3D (do Colab)
      ├── ang.pkl                      # Ângulos articulares (do Colab)
      ├── dataset.pkl                  # Dataset processado (do Colab)
      └── Resultados/
          ├── reconstruction.mp4       # Vídeo MuJoCo biomecânico
          ├── ground_contact.png       # Gráfico de contato com solo
          ├── knee_angles_time.png     # Ângulos dos joelhos no tempo
          ├── knee_left_cycles.png     # Ciclos normalizados (joelho esquerdo)
          └── knee_right_cycles.png    # Ciclos normalizados (joelho direito)
  ```

### 2. Adicionar Vídeos
- **Upload de vídeo**: Formatos suportados: MP4, AVI, MOV, MKV
- **Gravação pela webcam**: 
  - Preview em tempo real com preservação de aspect ratio
  - Controles de iniciar/parar gravação
  - Salvamento automático na pasta do projeto
- **Verificação automática**: Detecta dimensões e FPS do vídeo

### 3. Editor de Vídeo
- **Corte de vídeo**: Defina início e fim com precisão de frame
  - Sliders interativos duplos (início e fim)
  - Preview dos frames selecionados
  - Visualização do tempo em formato HH:MM:SS
  - Informações de duração original vs cortada
- **Otimização para Colab**: Quanto menor o vídeo, mais rápido o processamento GPU

### 4. Processamento no Google Colab (GPU)
- **Notebook**: `Mobile_cloud.ipynb`
- **Link configurável**: Cole a URL do seu notebook no Colab
- **Botão de acesso rápido**: Abre o Colab diretamente do app
- **Instruções claras**: Passo a passo do processo:
  1. Upload do vídeo para o Colab ou Google Drive
  2. Execute todas as células do notebook
  3. Aguarde o processamento (varia conforme duração do vídeo)
  4. Baixe os 3 arquivos gerados: `keypoints3d.npz`, `ang.pkl`, `dataset.pkl`
  5. Coloque os arquivos na pasta do projeto

### 5. Processamento de Resultados Local (CPU)
- **Botão de verificação**: 🔄 Verifica presença dos arquivos necessários
- **Carregamento automático**: Se resultados já processados existirem, carrega automaticamente
- **Processamento completo** (baseado em `Mobile_Local.ipynb`):
  
  #### Visualização Biomecânica
  - **MuJoCo Rendering**: Modelo anatômico 3D realista (requer instalação opcional)
    - Músculos, articulações e segmentos corporais
    - Mesma qualidade do notebook científico
  - **Fallback 2D**: Esqueleto simplificado caso MuJoCo não esteja disponível
  
  #### Análise de Marcha
  - **Contato com o solo**: 
    - Detecção automática de threshold
    - Identificação de step_up (início do ciclo)
    - Gráfico temporal de posição Z dos pés
  - **Ciclos de marcha**:
    - Detecção automática de ciclos completos
    - Normalização 0-100% do ciclo
    - Filtragem de ciclos anômalos (>15% variação)
  - **Ângulos articulares**:
    - Joelhos (esquerdo/direito)
    - Plotagem temporal e por ciclo
    - Curvas média ± desvio padrão

  #### Visualização Integrada
  - **Player de vídeo duplo**: Original + Biomecânico lado a lado (480x360px)
  - **Controles sincronizados**: Play/Pause/Stop
  - **Slider de progresso**: Navegação frame a frame
  - **FPS correto**: Reprodução na velocidade real do vídeo
  - **4 Gráficos estáticos**: Todos os resultados salvos como PNG

- **Barra de progresso**: Feedback detalhado em 11 etapas (0-100%)
- **Resultados salvos**: Pasta `Resultados/` com todos os arquivos gerados

## Instalação

### Pré-requisitos
- **Python**: 3.11, 3.12 ou 3.13 (⚠️ NÃO use Python 3.14 - incompatível!)
- **Sistema Operacional**: Windows, Linux ou macOS
- **GPU (Colab)**: Gratuito via Google Colab (recomendado T4 ou superior)
- **Webcam**: Opcional, apenas se for gravar vídeos

### Instalação Automática (RECOMENDADO - Windows)

1. **Baixe ou clone o repositório**:
```powershell
git clone https://github.com/EduardoPanizzon/Ubiquos-Mobilize-BodyModel.git
cd Ubiquos-Mobilize-BodyModel
```

2. **Execute o instalador automático**:
   - Dê duplo clique em: `INSTALAR_E_CRIAR_EXE.bat`
   - O script irá:
     - ✓ Verificar se Python está instalado (versão compatível)
     - ✓ Instalar todas as bibliotecas necessárias
     - ✓ Instalar monocular-demos para visualização MuJoCo
     - ✓ Criar um atalho "Analisador de Marcha.lnk" na pasta

3. **Aguarde** a instalação (5-10 minutos na primeira vez)

4. **Execute o programa**:
   - Dê duplo clique no atalho "Analisador de Marcha.lnk"

### Instalação Manual (Linux/macOS ou avançado)

1. **Clone o repositório**:
```bash
git clone https://github.com/EduardoPanizzon/Ubiquos-Mobilize-BodyModel.git
cd Ubiquos-Mobilize-BodyModel
```

2. **Instale as dependências principais**:
```bash
pip install numpy>=1.24.0
pip install opencv-python>=4.8.0
pip install matplotlib>=3.7.0
pip install Pillow>=10.0.0
pip install tensorflow
pip install tensorflow-hub
pip install jax jaxlib
pip install warp-lang
pip install mujoco-mjx
```

3. **Instale monocular-demos (opcional, para MuJoCo)**:
```bash
# Opção 1: Via pip diretamente
pip install git+https://github.com/IntelligentSensingAndRehabilitation/monocular-demos.git

# Opção 2: Clone e instale localmente
git clone https://github.com/IntelligentSensingAndRehabilitation/monocular-demos.git
cd monocular-demos
pip install .
cd ..
```

4. **Execute o programa**:
```bash
python video_processor_gui.py
```

⚠️ **Notas Importantes**: 
- A instalação MuJoCo (monocular-demos) é **opcional**
- Se não instalado, o sistema usa automaticamente visualização 2D simplificada
- Todas as outras funcionalidades (análise de marcha, gráficos) continuam funcionando
- A instalação MuJoCo pode demorar e requer ~2GB de espaço
- **Python 3.14 NÃO é compatível** - use 3.11, 3.12 ou 3.13

### Configuração do Google Colab

1. Acesse o [Google Colab](https://colab.research.google.com/)
2. Faça upload do notebook `Mobile_cloud.ipynb`
3. Configure o runtime para usar GPU:
   - Runtime → Change runtime type → Hardware accelerator: **GPU**
4. Copie a URL do notebook para usar no aplicativo

## Como Usar

### Fluxo Completo de Trabalho

#### 1. Iniciar a Aplicação

**Windows (após instalação automática)**:
- Dê duplo clique no atalho "Analisador de Marcha.lnk"

**Ou manualmente (qualquer sistema)**:
```bash
python video_processor_gui.py
```

#### 2. Criar ou Abrir Projeto

**Tela Inicial**:
- **Novo Projeto**: Digite um nome único (ex: "Paciente_001_Avaliacao_Inicial")
- **Abrir Projeto**: Selecione da lista de projetos existentes

#### 3. Adicionar Vídeo (Aba "Vídeo")

**Opção A - Upload**:
1. Clique em "Upload de Vídeo"
2. Selecione arquivo MP4/AVI/MOV/MKV
3. Vídeo copiado para pasta do projeto

**Opção B - Webcam**:
1. Clique em "Gravar pela Webcam"
2. Preview inicia automaticamente
3. Posicione o sujeito na frente da câmera
4. Clique em "Parar Gravação" ao terminar
5. Vídeo salvo automaticamente como `gravado.mp4`

**Dicas de Captura**:
- Vista lateral do sujeito (perfil)
- Corpo completo visível (cabeça aos pés)
- Fundo simples/contrastante
- Boa iluminação
- Pelo menos 2-3 ciclos de marcha completos
- Evite roupas largas que ocultam articulações

#### 4. Editar Vídeo (Aba "Editor") - Opcional

1. Use os sliders para definir início e fim
2. Preview mostra frame selecionado
3. Verifique duração cortada
4. Clique em "Salvar Vídeo Cortado"
5. Vídeo original é substituído pela versão cortada

**Por que cortar?**
- Reduz tempo de processamento no Colab
- Remove partes desnecessárias (preparação, pausa)
- Foca apenas nos ciclos de marcha relevantes

#### 5. Processar no Colab (Aba "Processamento")

1. **Configure URL** (primeira vez):
   - Cole o link do seu `Mobile_cloud.ipynb` no Colab
   - URL é salva automaticamente

2. **Clique em "Abrir Google Colab"**:
   - Notebook abre no navegador

3. **No Google Colab**:
   - Conecte ao runtime GPU (canto superior direito)
   - Faça upload do vídeo do projeto ou use Google Drive
   - Execute todas as células (Runtime → Run all)
   - Aguarde processamento (5-20 min dependendo do vídeo)
   - Baixe os 3 arquivos gerados:
     - `keypoints3d.npz` - Pontos 3D do corpo
     - `ang.pkl` - Ângulos das articulações
     - `dataset.pkl` - Dataset processado

4. **Coloque os arquivos na pasta do projeto**:
   ```
   projetos/Nome_do_Projeto/
   ├── video.mp4
   ├── keypoints3d.npz      ← Baixado do Colab
   ├── ang.pkl              ← Baixado do Colab
   └── dataset.pkl          ← Baixado do Colab
   ```

#### 6. Processar Resultados Localmente (Aba "Resultados")

1. **Verificar arquivos**:
   - Clique em "🔄 Verificar Arquivos"
   - Sistema checa presença de keypoints3d.npz, ang.pkl, dataset.pkl
   - Se existirem, botão "Processar Resultados" é habilitado
   - Se resultados já processados, carrega automaticamente

2. **Clique em "Processar Resultados"**:
   - Barra de progresso mostra andamento (11 etapas)
   - Processamento leva 2-5 minutos dependendo do vídeo
   - Interface permanece responsiva

3. **Visualizar Resultados**:
   - **Vídeos**: Original e biomecânico lado a lado
     - Use Play/Pause/Stop para controlar
     - Arraste slider para navegar
   - **Gráficos** (4 painéis):
     - Contato com o solo (left/right foot)
     - Ângulos dos joelhos ao longo do tempo
     - Ciclos normalizados joelho esquerdo
     - Ciclos normalizados joelho direito

4. **Arquivos Gerados** (pasta `Resultados/`):
   - `reconstruction.mp4` - Vídeo MuJoCo (ou `skeleton.mp4` se 2D)
   - `ground_contact.png`
   - `knee_angles_time.png`
   - `knee_left_cycles.png`
   - `knee_right_cycles.png`

### Interpretação dos Resultados

#### Gráfico de Contato com o Solo
- **Linha vermelha/roxa**: Posição Z do pé esquerdo/direito
- **Linha tracejada preta**: Threshold de contato
- **Marcadores verticais**: Início de cada ciclo (step_up)
- **Interpretação**: Altura do pé indica fase aérea vs apoio

#### Gráficos de Ângulos dos Joelhos
- **Gráfico temporal**: Mostra todos os ciclos ao longo do vídeo
- **Gráficos de ciclos**:
  - Cada ciclo normalizado 0-100%
  - Ciclos individuais (linhas finas)
  - Média ± desvio padrão (linha grossa + área sombreada)
- **Padrão normal**: Flexão (~60-70°) durante swing, extensão (~0-10°) durante stance
- **Assimetrias**: Compare esquerdo vs direito

## Estrutura do Projeto

```
gait-analysis/
├── README.md                           # Este arquivo
├── README_GUI.md                       # Documentação detalhada da GUI
├── requirements_gui.txt                # Dependências Python
├── video_processor_gui.py              # Aplicação principal
├── Mobile_cloud.ipynb                  # Notebook para processamento GPU (Colab)
├── Mobile_Local.ipynb                  # Notebook de referência (análise local)
└── projetos/                           # Diretório de projetos (criado automaticamente)
    └── [Nome_Projeto]/
        ├── video.mp4
        ├── keypoints3d.npz
        ├── ang.pkl
        ├── dataset.pkl
        └── Resultados/
            ├── reconstruction.mp4
            └── [gráficos].png
```

## Base Científica e Metodologia

### GaitTransformer Framework

Este projeto é baseado no trabalho de [Peabody124](https://github.com/peabody124) e do grupo [IntelligentSensingAndRehabilitation](https://github.com/IntelligentSensingAndRehabilitation):

- **Paper**: "GaitTransformer: Monocular 3D Gait Reconstruction with Transformer-based Approach"
- **Tecnologias**:
  - Transformer networks para reconstrução 3D
  - Modelos biomecânicos baseados em MuJoCo
  - Forward kinematics para cálculo de ângulos articulares
  - Detecção automática de eventos de marcha

### Pipeline de Processamento

1. **Pose Estimation 2D**: 
   - Detecção de keypoints 2D usando redes neurais (MediaPipe/OpenPose)
   
2. **Lift to 3D**:
   - GaitTransformer reconstrói keypoints 3D a partir de 2D
   - Preserva coerência temporal e biomecânica

3. **Biomechanical Modeling**:
   - Forward kinematics para calcular ângulos
   - Modelo músculo-esquelético do MuJoCo

4. **Gait Analysis**:
   - Detecção de ciclos baseada em contato com solo
   - Normalização temporal 0-100%
   - Extração de métricas clínicas

### Validação Clínica

O método foi validado em estudos comparando com sistemas gold-standard de captura de movimento (Vicon, Qualisys), mostrando:
- Erro médio de ângulos articulares < 5°
- Detecção de eventos de marcha > 95% acurácia
- Correlação temporal > 0.9 com sistemas de referência

## Solução de Problemas

### Erro ao processar vídeo no Colab
- **GPU não conectada**: Runtime → Change runtime type → GPU
- **Memória insuficiente**: Reduza duração do vídeo (use o editor)
- **Arquivo muito grande**: Comprima o vídeo ou reduza resolução

### "Arquivos faltando" na aba Resultados
- Certifique-se de executar **todo** o notebook `Mobile_cloud.ipynb`
- Baixe os 3 arquivos: `keypoints3d.npz`, `ang.pkl`, `dataset.pkl`
- Coloque na pasta raiz do projeto (não em subpastas)
- Clique em "🔄 Verificar Arquivos"

### Vídeos rodando devagar/rápido
- Sistema detecta FPS automaticamente
- Se incorreto, verifique metadados do vídeo: `ffprobe video.mp4`

### MuJoCo não funciona
- Instalação opcional, não bloqueia outras funcionalidades
- Use visualização 2D simplificada (fallback automático)
- Para instalar: veja seção "Instalação Completa"

### Interface congela durante processamento
- **Corrigido**: Processamento roda em thread separada
- Se ainda ocorrer, atualize para versão mais recente

### Erro ao abrir projeto existente
- Verifique se pasta existe em `projetos/`
- Nome do projeto não pode ter caracteres especiais ( / \ : * ? " < > | )

## Roadmap e Melhorias Futuras

- [ ] Integração direta com Google Drive (upload/download automático)
- [ ] Análise de outras articulações (tornozelos, quadris, ombros)
- [ ] Exportação de relatórios em PDF
- [ ] Gráficos interativos (zoom, pan, seleção de ciclos)
- [ ] Comparação entre múltiplas avaliações (progresso temporal)
- [ ] Detecção automática de padrões anormais (ML)
- [ ] Suporte a múltiplos vídeos por projeto
- [ ] Análise de simetria e métricas clínicas automatizadas
- [ ] Exportação de dados para CSV/Excel
- [ ] Dark mode na interface

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## Licença

Este projeto é baseado no trabalho do [IntelligentSensingAndRehabilitation](https://github.com/IntelligentSensingAndRehabilitation) e utiliza o [GaitTransformer](https://github.com/peabody124/GaitTransformer). Consulte as licenças originais dos projetos base.
