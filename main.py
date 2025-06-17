import cv2
import mediapipe as mp
import numpy as np

from utils import calculate_angle # Importa nossa função de cálculo de ângulo

# Inicializa os módulos de desenho e pose do MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Configura a captura de vídeo da webcam.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera. Verifique se ela está conectada e não está em uso.")
    exit()

# --- NOVO: Variáveis para feedback e contagem de repetições ---
# Definir a faixa de ângulo alvo para um agachamento (exemplo: joelho entre 70 e 160 graus)
# Estes valores são arbitrários e devem ser ajustados para o exercício real.
TARGET_ANGLE_MIN = 70
TARGET_ANGLE_MAX = 160

# Variáveis para contagem de repetições
counter = 0
stage = None # 'down' ou 'up' para controlar o ciclo da repetição
# --- FIM NOVO ---

# Configura o modelo de detecção de pose do MediaPipe.
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Erro: Falha ao ler o frame do frame da câmera. Fim do stream ou problema na câmera.")
            break

        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Cor padrão para os landmarks (verde)
        landmark_color = (0, 255, 0) # BGR: Green
        connection_color = (0, 255, 0) # BGR: Green

        # Variáveis para armazenar os ângulos
        angle_left = None
        angle_right = None

        if results.pose_landmarks:
            try:
                # --- NOVO: Extração de landmarks para ambos os joelhos ---
                # Lado ESQUERDO do corpo do paciente (direito na tela invertida)
                hip_left = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value]
                knee_left = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value]
                ankle_left = results.pose_landmarks.landmark[mp_pose.PoseLandland.LEFT_ANKLE.value]

                # Lado DIREITO do corpo do paciente (esquerdo na tela invertida)
                hip_right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value]
                knee_right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value]
                ankle_right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

                h, w, c = image.shape # Altura, Largura, Canais

                # Converte coordenadas normalizadas para pixels
                p_hip_left = np.array([hip_left.x * w, hip_left.y * h])
                p_knee_left = np.array([knee_left.x * w, knee_left.y * h])
                p_ankle_left = np.array([ankle_left.x * w, ankle_left.y * h])

                p_hip_right = np.array([hip_right.x * w, hip_right.y * h])
                p_knee_right = np.array([knee_right.x * w, knee_right.y * h])
                p_ankle_right = np.array([ankle_right.x * w, ankle_right.y * h])

                # Calcula os ângulos
                angle_left = calculate_angle(p_hip_left, p_knee_left, p_ankle_left)
                angle_right = calculate_angle(p_hip_right, p_knee_right, p_ankle_right)

                # --- NOVO: Lógica de Feedback Visual e Contagem de Repetições ---
                # Usaremos o ângulo do joelho esquerdo como referência para o feedback e contagem
                # Você pode adaptar para usar a média dos dois joelhos, ou monitorar apenas um.
                
                # Feedback de Cor: Se o ângulo estiver fora da faixa alvo, mude para vermelho.
                if angle_left is not None:
                    if TARGET_ANGLE_MIN <= angle_left <= TARGET_ANGLE_MAX:
                        landmark_color = (0, 255, 0) # Verde: Correto
                        connection_color = (0, 255, 0)
                    else:
                        landmark_color = (0, 0, 255) # Vermelho: Fora da faixa
                        connection_color = (0, 0, 255)

                    # Lógica de Contagem de Repetições (Exemplo para Agachamento)
                    # Assumimos que a pessoa começa em pé (ângulo próximo a 180)
                    # e desce (ângulo diminui), depois sobe (ângulo aumenta).
                    
                    # Estágio 'down': se o ângulo diminuiu e está abaixo de um certo limiar (ex: 100 graus)
                    # Isso marca o ponto mais baixo do agachamento.
                    if angle_left < 100: # Limiar para considerar "agachado"
                        stage = "down"
                    
                    # Estágio 'up': se o ângulo aumentou e está acima de um certo limiar (ex: 160 graus)
                    # E se o estágio anterior foi "down", significa que uma repetição foi completada.
                    if angle_left > 160 and stage == 'down': # Limiar para considerar "em pé"
                        stage = "up"
                        counter += 1 # Incrementa a contagem de repetições
                        print(f"Repetições: {counter}") # Para ver no console também

            except Exception as e:
                print(f"Erro ao calcular ou processar ângulos/landmarks: {e}")

            # --- NOVO: Desenha os landmarks com cores dinâmicas ---
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=landmark_color, thickness=2, circle_radius=2), # Cor dinâmica
                mp_drawing.DrawingSpec(color=connection_color, thickness=2, circle_radius=2)  # Cor dinâmica
            )

            # --- NOVO: Exibe os ângulos e o contador de repetições na tela ---
            if angle_left is not None:
                cv2.putText(image, f'Joelho E: {angle_left:.0f} deg',
                            tuple(np.array(p_knee_left + [-50, -30]).astype(int)), # Posição ajustada
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            if angle_right is not None:
                cv2.putText(image, f'Joelho D: {angle_right:.0f} deg',
                            tuple(np.array(p_knee_right + [10, -30]).astype(int)), # Posição ajustada
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # Exibe o contador de repetições no canto superior esquerdo
            cv2.putText(image, f'Reps: {counter}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA) # Amarelo vibrante
            # --- FIM NOVO ---

        cv2.imshow('MyRehabVision - Pressione ESC para Sair', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()