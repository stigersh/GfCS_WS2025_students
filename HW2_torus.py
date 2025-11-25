import numpy as np

def generate_torus(nX, nY, r, R):
    """
    - nX: samples along the tube angle (theta)
    - nY: samples along the sweep angle (phi)
    - r:  minor (tube) radius
    - R:  major radius

    Returns
    -------
    V : (nX*nY, 3) 
        Vertex positions.
    F : (2*(nX-1)*(nY-1), 3) 
        Triangle faces
    """
    # parameter grids (includes both 0 and 2π)
    theta = np.linspace(0.0, 2.0*np.pi, nX)
    phi   = np.linspace(0.0, 2.0*np.pi, nY)

    # meshgrid with theta along rows (j) and phi along cols (i)
    T, P = np.meshgrid(theta, phi, indexing='ij')

    # torus embedding
    X = (R + r*np.cos(T)) * np.cos(P)
    Y = (R + r*np.cos(T)) * np.sin(P)
    Z =  r*np.sin(T)

    # vertices 
    V = np.column_stack([X.ravel(order='C'),
                         Y.ravel(order='C'),
                         Z.ravel(order='C')]).astype(np.float64)

    # top-left indices of each quad (exclude last row/col)
    j_idx = np.arange(nX - 1)
    i_idx = np.arange(nY - 1)
    I_tl = (j_idx[:, None] * nY + i_idx[None, :]).ravel(order='C')

    # other corners
    I_tr = I_tl + nY
    I_bl = I_tl + 1
    I_br = I_tl + nY + 1

    # two triangles per quad
    F = np.vstack([
        np.column_stack([I_tl, I_bl, I_tr]),
        np.column_stack([I_bl, I_br, I_tr])
    ]).astype(np.int32)

    return V, F