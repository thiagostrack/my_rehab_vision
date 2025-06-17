MyRehabVision: Fisioterapia Conectada e Otimizada por Visão Computacional
Visão Geral do Projeto
O MyRehabVision é uma aplicação inovadora desenvolvida para revolucionar o acompanhamento de sessões de fisioterapia e reabilitação. Utilizando conceitos avançados de processamento de imagens e visão computacional, a aplicação permite a análise e quantificação de movimentos em tempo real, fornecendo feedback instantâneo ao paciente e dados objetivos ao profissional de saúde, tudo isso utilizando apenas uma câmera comum (webcam).

Este projeto tem como objetivo resolver o problema da avaliação subjetiva e da falta de feedback imediato na reabilitação, promovendo uma recuperação mais eficaz, segura e engajadora.

Funcionalidades Principais
Rastreamento de Pose em Tempo Real: Detecção precisa de 33 pontos-chave (landmarks) do corpo humano.
Cálculo de Ângulos Articulares: Quantificação em graus dos ângulos de articulações específicas (ex: joelhos, cotovelos).
Feedback Visual Dinâmico: Alteração da cor do esqueleto da pose (e texto do ângulo) para indicar se o movimento está dentro ou fora de uma faixa de execução correta (verde para correto, vermelho para incorreto).
Contagem Automatizada de Repetições: Reconhecimento e contagem automática das repetições de um exercício específico.
Interface Intuitiva: Exibição clara de ângulos, feedback e contador de repetições diretamente na tela de vídeo.
Demonstração em Vídeo
Assista ao vídeo abaixo para ver o MyRehabVision em ação e entender suas funcionalidades:

[]([Link do seu Vídeo no YouTube/Vimeo])

(Substitua [ID_DO_VIDEO] pelo ID real do seu vídeo do YouTube e [Link do seu Vídeo no YouTube/Vimeo] pelo link completo do seu vídeo. O ID do vídeo é a parte da URL depois de v= ou /).

Tecnologias Utilizadas
Python: Linguagem de programação principal.
OpenCV: Biblioteca de visão computacional para captura e processamento de imagens.
MediaPipe: Framework de aprendizado de máquina (Google) para detecção e rastreamento de pose humana.
Numpy: Biblioteca para operações numéricas, essencial para cálculos de vetores e ângulos.
Como Configurar e Executar
Siga os passos abaixo para colocar o MyRehabVision em funcionamento no seu ambiente local.

Pré-requisitos
Python 3.8+ instalado.
Uma webcam conectada ao seu computador.
1. Clonar o Repositório
Abra seu terminal ou prompt de comando e clone o repositório:

Bash

git clone [https://github.com/](https://github.com/)[Seu Usuário GitHub]/my-rehab-vision.git
cd my-rehab-vision
2. Configurar o Ambiente Virtual
É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto:

Bash

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
3. Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias usando o requirements.txt:

Bash

pip install -r requirements.txt
4. Executar a Aplicação
Navegue até a pasta src e execute o script principal:

Bash

python src/main.py
A janela da sua webcam deve aparecer com a detecção de pose em tempo real, ângulos e contador de repetições. Pressione ESC para sair da aplicação.

Exercício Demonstrado (Exemplo: Agachamento)
A lógica de feedback e contagem de repetições na implementação atual está configurada para monitorar um agachamento.
Os limiares de ângulo para feedback e contagem de repetições podem ser ajustados no arquivo src/main.py para adaptar-se a outros exercícios.

Estrutura do Projeto
my-rehab-vision/
├── src/
│   ├── main.py             # Código principal da aplicação (captura, detecção, feedback, contagem)
│   └── utils.py            # Funções auxiliares (ex: cálculo de ângulo)
├── assets/                 # (Opcional) Imagens, vídeos de exemplo, etc.
├── requirements.txt        # Lista de dependências do Python
└── README.md               # Este arquivo de documentação
Contribuição (Opcional, se o projeto for além do trabalho individual)
Este é um projeto acadêmico desenvolvido individualmente.

Licença
Este projeto está licenciado sob a Licença MIT.
