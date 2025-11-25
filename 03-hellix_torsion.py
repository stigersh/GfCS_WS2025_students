#%% imports
import numpy as np
import matplotlib.pyplot as plt
%matplotlib widget

#%% params
a, b, c = 2.0, 1.0, 3.0
n = 2000
#%% parameter t - initial parameterization
t = np.linspace(0, 2*np.pi, n)
dt = t[1]-t[0]

#%% curve
g  = np.column_stack((a*np.cos(t),  b*np.sin(t),      c*t)) #gamma(t)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(g[:,0], g[:,1], g[:,2])
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title("Elliptic helix")

#%% derivatives 
g1 = np.column_stack((-a*np.sin(t), b*np.cos(t),      np.full_like(t,c)))   #gamma'(t)
g2 = np.column_stack((-a*np.cos(t),-b*np.sin(t),      np.zeros_like(t)))    #gamma''(t)
g3 = np.column_stack(( a*np.sin(t),-b*np.cos(t),      np.zeros_like(t)))    #gamma'''(t)

#%% calculate unit tangent T, Frenet Nomral *note: N is not parallel to gamma''(t)!
T = g1 / np.linalg.norm(g1,axis=1)[:,None] # gamma'(t) normalized
N = ...

#%% calculate speed (by t initial parameterization), ds, arclength parameterization - s§
speed   = ...
ds      = ...
s       = ...

#%% torsion τ(s) and total torsion Θ(s) = ∫ τ ds
tau_analytic = ...
Theta_analytic = ...

#%% build RMF (Bishop frame) T (already calcualted), U, V
U = np.zeros_like(T)
V = np.zeros_like(T)

# initialize e1(0) = Frenet normal at 0

U[0] = ...
V[0] = ...

for i in range(n-1):
    # RMF propagation via projection + normalization 
    # project e1(i) onto plane normal to T(i+1) and normalize
    U[i+1] = ...
    V[i+1] = ...



#%% RMF torsion angle = angle between N(s) and e1(s) for all s
angle = np.arctan2( (np.cross(U,N)*T).sum(1), (U*N).sum(1) )
Theta_RMF = np.unwrap(angle) #makes it continuous (no jumps at ±π)

#%% compare analytic vs RMF total torsion
plt.figure()
plt.plot(s, Theta_analytic, label='analytic')
plt.plot(s, Theta_RMF, '--', label='RMF')
plt.xlabel("arclength s")
plt.ylabel("total torsion Θ(s)")
plt.legend()
plt.title("Total torsion: analytic vs RMF")
plt.show()

