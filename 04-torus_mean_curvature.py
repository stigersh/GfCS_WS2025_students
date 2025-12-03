#%% imports
import numpy as np
import matplotlib.pyplot as plt
import igl
from scipy.linalg import solve
%matplotlib widget
import meshplot as mp #https://libigl.github.io/libigl-python-bindings/tut-chapter5/
%matplotlib inline
from HW2_torus import generate_torus_sampling, generate_from_sampling
#%% discrete mean curvature and Gaussian curvature at center via libigl

def torus_normal(theta, phi):
    ...
    return N

# Gaussian curvature integral via angle defects
def K_by_angle_defects(V, F):
    ...
    return K_defect


# %% torus analytical curvaturesß

def torus_curvatures(theta, R, r):
    """
    Principal, mean, and Gaussian curvature on a ring torus

        X(theta, phi) = ((R + r cos theta) cos phi,
                         (R + r cos theta) sin phi,
                         r sin theta)

    Parameters
    ----------
    theta : float or np.ndarray
        Poloidal angle (around the tube).
    R : float
        Major radius (distance from tube center to z-axis).
    r : float
        Minor radius (tube radius).

    Returns
    -------
    K : float or np.ndarray
        Gaussian curvature.
    H : float or np.ndarray
        Mean curvature (with the normal convention used in the referenced link).
    k1 : float or np.ndarray
        Principal curvature in the theta-direction.
    k2 : float
        Principal curvature in the phi-direction (constant in theta).
    """

    # principal curvatures (matching the reference)
    k1 = -np.cos(theta) / (R + r * np.cos(theta))  # varies with theta
    k2 = -1.0 / r                                  # constant

    # Gaussian curvature
    K = k1 * k2  # = cos(theta) / (r * (R + r cos(theta)))

    # Mean curvature
    H = 0.5 * (k1 + k2)  # = -(R + 2 r cos(theta)) / (2 r (R + r cos(theta)))

    return K, H, k1, k2

nX = 40
nY = 40
r = 0.3
R = 1.0
# get samped torus along with its parameters
# theta and phi are angles, T,P are their meshgrid versions, Tcs,Pcs are flattened T,P
theta, phi, T, P, Tcs, Pcs = generate_torus_sampling(R, r, nX, nY)
#fixed closed torus mesh
V_torus, F_torus = generate_from_sampling(T, P, R, r)
N_torus = torus_normal(Tcs, Pcs)
#%%
K, H, k1, k2 = torus_curvatures(Tcs, R, r)

K_defect_torus = K_by_angle_defects(V_torus, F_torus)

#%%
#plot the torus colored by Gaussian curvature
plotter = mp.plot(V_torus, F_torus, c=K, shading={"wireframe":True})
#%%
H_vec_disc_torus = ...
# project on the normals and divide by vertex area
H_disc_torus = ...
# divide by vertex area for at point values
K_disc_torus = ...
#%%
#TODO compare the analytical vs discrete curvatures at different lolcations and other metricsß


# %%
#%% total integrated Gaussian curvature and Euler characteristic
E_torus = igl.edges(F_torus)               # unique edges
V_count = V_torus.shape[0]
E_count = E_torus.shape[0]
F_count = F_torus.shape[0]

chi = ...  # Euler characteristic
total_K_int = np.sum(K_defect_torus)
area_weight = r * (R + r * np.cos(Tcs))  # same shape as K
dtheta = 2.0 * np.pi / nX
dphi = 2.0 * np.pi / nY
total_K_int_torus_analytic = ...


print("\nTopology & total Gaussian curvature:")
print(f"V = {V_count}, E = {E_count}, F = {F_count}")
print(f"Euler characteristic chi = {chi}")
print(f"Total integrated Gaussian curvature sum_i K_int[i] = {total_K_int:.6f}")
print(f" Total integrated Gaussian curvature (analytic) = {total_K_int_torus_analytic:.6f}")
print(f" Gauss Bonnet: 2 pi * chi = {2 * np.pi * chi:.6f}")
# %%
