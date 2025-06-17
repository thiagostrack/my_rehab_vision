import numpy as np

def calculate_angle(a, b, c):
    """
    Calcula o ângulo em graus entre três pontos (landmarks).
    Os pontos devem ser arrays numpy (x, y).

    Args:
        a (np.array): Coordenadas do primeiro ponto (ex: quadril).
        b (np.array): Coordenadas do ponto do vértice (ex: joelho).
        c (np.array): Coordenadas do terceiro ponto (ex: tornozelo).

    Returns:
        float: O ângulo em graus.
    """
    # Converte os pontos para arrays numpy para facilitar as operações
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # Calcula os vetores BA e BC
    ba = a - b
    bc = c - b

    # Calcula o cosseno do ângulo usando o produto escalar e as magnitudes dos vetores
    # Adiciona um pequeno epsilon para evitar divisão por zero se o vetor tiver magnitude zero
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)

    # Garante que o valor esteja dentro do domínio de arccos [-1, 1]
    # Isso evita erros de floating point para valores muito próximos de -1 ou 1
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    # Calcula o ângulo em radianos e depois converte para graus
    angle_radians = np.arccos(cosine_angle)
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees

if __name__ == '__main__':
    # Exemplo de uso da função calculate_angle
    # Imagine 3 pontos: A=(0,0), B=(1,0) e C=(1,1)
    # Isso formaria um ângulo de 90 graus no ponto B
    point_a = (0, 0)
    point_b = (1, 0)
    point_c = (1, 1)

    angle = calculate_angle(point_a, point_b, point_c)
    print(f"O ângulo entre A, B e C é: {angle:.2f} graus")

    # Outro exemplo: A=(0,0), B=(0,1), C=(0,2) (linha reta)
    # Ângulo esperado: 180 graus
    point_a_straight = (0, 0)
    point_b_straight = (0, 1)
    point_c_straight = (0, 2)
    angle_straight = calculate_angle(point_a_straight, point_b_straight, point_c_straight)
    print(f"O ângulo entre A, B e C (reta) é: {angle_straight:.2f} graus")

    # Exemplo com pontos reais que seriam retornados pelo MediaPipe
    # Estes são apenas valores fictícios para demonstrar o uso
    # Lembre-se que MediaPipe retorna x,y normalizados entre 0 e 1
    hip_x, hip_y = 0.5, 0.6
    knee_x, knee_y = 0.5, 0.4
    ankle_x, ankle_y = 0.5, 0.2

    # Precisamos das coordenadas x,y para calcular no plano 2D da imagem
    hip = np.array([hip_x, hip_y])
    knee = np.array([knee_x, knee_y])
    ankle = np.array([ankle_x, ankle_y])

    angle_knee = calculate_angle(hip, knee, ankle)
    print(f"O ângulo simulado do joelho é: {angle_knee:.2f} graus")