from numpy.linalg import eigh
import numpy as np

# Define units
m = 1
kg = 1
sec = 1
J = 1
nm = 1E-9 * (m)
eV = 1.60218E-19 * (J)
mass_e = 9.10938E-31 * (kg)
h_bar = (6.62607E-34) / (2 * np.pi) * (J * sec)

def solve(z, V, mass, dz):
    n_points=len(z)
    H_matrix = np.zeros((n_points, n_points))
    for i in range(n_points):
        for j in range(n_points):
            # Kinetic energy term
            Tij = (-(h_bar ** 2) / (2 * mass)) * (1 / (dz) ** 2) * (
                -2 if i == j else 1 if abs(i - j) == 1 else 0
            )
            # Potential energy term
            Vij = V[i] * (1 if i == j else 0)
            # Hamiltonian matrix elements
            H_matrix[i, j] = Tij + Vij

    
    E, psis = eigh(H_matrix)
    return (E, psis)


