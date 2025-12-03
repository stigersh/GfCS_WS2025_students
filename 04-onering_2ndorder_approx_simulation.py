#%% imports
import numpy as np
import matplotlib.pyplot as plt
import igl
from scipy.linalg import solve
%matplotlib widget
import meshplot as mp #https://libigl.github.io/libigl-python-bindings/tut-chapter5/
%matplotlib inline

#%% helper methods

#%% parameters and one-ring construction - play with them, sanity check 
np.random.seed(1)

n_ring      = 40
#TODO: try different n_ring values - affects scale of the mesh around the center vertex
radius      = 1.0*1e-2
noise_sigma = 0.00 #sanity noise level #TODO:try out different noise levels/models

# ground-truth quadratic coefficients
#TODO: play with these values
a_true   = 2.0
b_true   = 0.0
c_true   = -3.0
delta_true = 0.01

# random positive increments that sum to 2π
inc = np.random.rand(n_ring)
inc *= 2.0 * np.pi / inc.sum()
angles = np.cumsum(inc)
angles -= angles[0]  # shift so first angle is 0 (just for nicer orientation)

# one-ring vertices in xy-plane
xs = radius * np.cos(angles)
ys = radius * np.sin(angles)

# heights from quadratic + noise
zs_clean = a_true * xs**2 + b_true * xs * ys + c_true * ys**2 + delta_true
zs_noisy = zs_clean + noise_sigma * np.random.randn(n_ring)

# vertex array: 0 is center, 1..n_ring are neighbors
V = np.zeros((n_ring + 1, 3))
V[0] = ...  # center vertex (don't forget the height)
V[1:, 0] = xs
V[1:, 1] = ys
V[1:, 2] = zs_noisy

# triangle fan faces around vertex 0
F = []
for i in range(1, n_ring + 1):
    j = i
    k = 1 + (i % n_ring)  # wrap
    F.append([0, j, k])
F = np.array(F, dtype=int)


print("V shape:", V.shape)
print("F shape:", F.shape)

#%% plot: fan mesh (just to see the geometry)
p = mp.plot(V, F, c=V[:,2], shading={'wireframe':True})
#%% different plotter for backup
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot triangular faces
for face in F:
    triangle = V[face]
    ax.plot_trisurf(triangle[:, 0], triangle[:, 1], triangle[:, 2], alpha=0.7)

# Plot vertices
ax.scatter(V[:,0], V[:,1], V[:,2], c=V[:,2], s=50, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y') 
ax.set_zlabel('Z')
plt.show()
#%% build A matrix and solve for quadratic coefficients in 2 ways
# Model: z ≈ a x^2 + b x y + c y^2 + δ
xs_all = V[:, 0]
ys_all = V[:, 1]
zs_all = V[:, 2]

A = ...
b = ...

# option 1: np.linalg.lstsq


# option 2: normal equations (A^T A) x = A^T b, solve with scipy.linalg.solve

# compare results from both
...

a_fit, b_fit, c_fit, delta_fit = ...  # unpack fitted parameters

print("Fitted quadratic parameters:")
print(f"a_fit = {a_fit:.6f}, b_fit = {b_fit:.6f}, c_fit = {c_fit:.6f}, delta_fit = {delta_fit:.6f}")
print("Ground truth:")
print(f"a_true = {a_true:.6f}, b_true = {b_true:.6f}, c_true = {c_true:.6f}, delta_true = {delta_true:.6f}")
print("error:")
print(f"a error = {a_fit - a_true:.6f}, b error = {b_fit - b_true:.6f}, c error = {c_fit - c_true:.6f}, delta error = {delta_fit - delta_true:.6f}")

#%% Hessian, principal curvatures, K = k1*k2
H = ... 
H_fit = ...

k1, k2 = ...  # sorted ascending
H_mean = ...
K_from_H = ...

print("\nHessian from fitted quadratic:")
print(H)
print(f"k1 = {k1:.6f} (min), k2 = {k2:.6f} (max)")
print(f"Mean curvature from Hessian: H_mean = {H_mean:.6f}")
print(f"Gaussian curvature from Hessian: K_from_H = {K_from_H:.6f}")

#%% discrete mean curvature and Gaussian curvature at center via libigl 
# (use igl.cotmatrix, igl.massmatrix, igl.per_vertex_normals)

HN = ...       # mean curvature normal (integrated)

# Gaussian curvature integral via angle defect at the center vertex
K_defect = ...

# divide by vertex area to compare to calculating from the Hessian
# caculate surface normal at center vertex to get HN projection
H_disc = ...
K_disc = ...

#%% compare Hessian vs discrete curvatures
print("\nComparison of curvatures from Hessian vs discrete:")
#print values next to each other for easier comparison
print("H_mean (from Hessian) {:.6f} vs H_disc (discrete) {:.6f}".format(H_mean, H_disc))  
print("K_from_H (from Hessian) {:.6f} vs K_disc (discrete) {:.6f}".format(K_from_H, K_disc))
print("\nSanity ratios:")
print(f"H_disc / H_mean    = {H_disc / H_mean:.6f}")
print(f"K_disc / K_from_H  = {K_disc / K_from_H:.6f}")


