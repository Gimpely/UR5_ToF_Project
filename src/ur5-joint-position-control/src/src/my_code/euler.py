import numpy as np

def rotation_x(alpha):
    return np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
    ])

def rotation_y(beta):
    return np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])

def rotation_z(gamma):
    return np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])

def matrix_to_euler(matrix):
    sy = np.sqrt(matrix[0, 0] * matrix[0, 0] + matrix[1, 0] * matrix[1, 0])
    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(matrix[2, 1], matrix[2, 2])
        y = np.arctan2(-matrix[2, 0], sy)
        z = np.arctan2(matrix[1, 0], matrix[0, 0])
    else:
        x = np.arctan2(-matrix[1, 2], matrix[1, 1])
        y = np.arctan2(-matrix[2, 0], sy)
        z = 0

    return x, y, z

# Definirajte rotacije okoli osi x, y in z
alpha_x = np.radians(30)
alpha_y = np.radians(45)
alpha_z = np.radians(60)

# Izrasunajte rotacije za posamezne osi
R_x = rotation_x(alpha_x)
R_y = rotation_y(alpha_y)
R_z = rotation_z(alpha_z)

# Izrasunajte kombinirano rotacijo
R_combined = np.dot(np.dot(R_z, R_y), R_x)

# Pretvorite rotacijsko matriko v Eulerjeve kote (RPY)
roll, pitch, yaw = np.degrees(matrix_to_euler(R_combined))

# Izpis Eulerjevih kotov
print(roll, pitch, yaw)

