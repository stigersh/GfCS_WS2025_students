import numpy as np

def generate_torus_sampling(R, r, nX, nY):
    """
    Generate parameter samples for a ring torus

        X(theta, phi) = ((R + r cos theta) cos phi,
                         (R + r cos theta) sin phi,
                         r sin theta)

    Parameters
    ----------
    R : float
        Major radius
    r : float
        Minor radius
    nX : int
        Number of samples along the theta direction
    nY : int
        Number of samples along the phi direction

    Returns
    -------
    theta, phi : ndarray of shape (nX,), (nY,)
        Parameter samples along theta and phi directionsß
    T, P : ndarray of shape (nX, nY)
        Meshgrid of theta and phi samples
    Tcs : ndarray of shape (nX*nY,)
        Flattened theta samples
    Pcs : ndarray of shape (nX*nY,)
        Flattened phi samples
    """
    theta = np.linspace(0.0, 2.0*np.pi, nX, endpoint=False)
    phi   = np.linspace(0.0, 2.0*np.pi, nY, endpoint=False)
    # meshgrid with theta along rows (j) and phi along cols (i)
    T, P = np.meshgrid(theta, phi, indexing='ij')
    #  (row-major to match j*nY + i indexing in C++)
    Tcs = T.ravel(order='C')
    Pcs = P.ravel(order='C')
    return theta, phi, T, P, Tcs, Pcs


def generate_from_sampling(T, P, R, r):
    nX, nY = T.shape  # theta samples, phi samples

    # torus embedding
    X = (R + r*np.cos(T)) * np.cos(P)
    Y = (R + r*np.cos(T)) * np.sin(P)
    Z =  r*np.sin(T)

    # vertices (row-major to match j*nY + i indexing)
    V = np.column_stack([
        X.ravel(order='C'),
        Y.ravel(order='C'),
        Z.ravel(order='C')
    ]).astype(np.float64)

    # index grid
    j = np.arange(nX)
    i = np.arange(nY)
    J, I = np.meshgrid(j, i, indexing='ij')  # J: theta index, I: phi index

    # flatten base indices
    I_tl = (J * nY + I).ravel(order='C')                    # (j,   i)
    I_tr = (((J + 1) % nX) * nY + I).ravel(order='C')       # (j+1, i)
    I_bl = (J * nY + (I + 1) % nY).ravel(order='C')         # (j,   i+1)
    I_br = (((J + 1) % nX) * nY + (I + 1) % nY).ravel(order='C')  # (j+1, i+1)

    # two triangles per quad
    F = np.vstack([
        np.column_stack([I_tl, I_bl, I_tr]),
        np.column_stack([I_bl, I_br, I_tr])
    ]).astype(np.int32)

    return V, F

def generate_torus(R, r, nX, nY):
    #old interface compatibility function
    _, _, T, P, _, _ = generate_torus_sampling(R, r, nX, nY)
    V, F = generate_from_sampling(T, P, R, r)
    return V, F