import numpy as np

def rotation_matrix(i, raan, argp):
    i = np.radians(i)
    raan = np.radians(raan)
    argp = np.radians(argp)

    Rz_raan = np.array([
        [np.cos(raan), -np.sin(raan), 0],
        [np.sin(raan),  np.cos(raan), 0],
        [0,             0,            1]
    ])

    Rx_i = np.array([
        [1, 0,           0],
        [0, np.cos(i), -np.sin(i)],
        [0, np.sin(i),  np.cos(i)]
    ])

    Rz_argp = np.array([
        [np.cos(argp), -np.sin(argp), 0],
        [np.sin(argp),  np.cos(argp), 0],
        [0,             0,            1]
    ])

    return Rz_raan @ Rx_i @ Rz_argp

def generate_orbit(a, e, i, raan, argp, nu_start):
    if e < 1:
        theta = np.linspace(0, 2 * np.pi, 800)
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
    elif abs(e - 1.0) < 1e-3:
        theta = np.linspace(-np.radians(89), np.radians(89), 800)
        p = 2 * a
        r = p / (1 + np.cos(theta))
    else:
        theta = np.linspace(-np.radians(60), np.radians(60), 800)
        r = a * (e**2 - 1) / (1 + e * np.cos(theta))

    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros_like(x)

    pos_orb = np.vstack((x, y, z))  # (3, N)
    R = rotation_matrix(i, raan, argp)
    pos_eci = R @ pos_orb

    return pos_eci.T  # (N, 3)
