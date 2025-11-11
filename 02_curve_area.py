
#%% [markdown]
# # curve area
# - hands on about discrete area from curve integral
# - familiarize with triangle, meshplot, mesh boundary by libigl

#%% [markdown]
# To install meshplot and triangle run the following command:           
# - pip install git+https://github.com/skoch9/meshplot.git
# - pip install triangle
#%%
# vis libraries
from matplotlib import pyplot as plt
import meshplot as mp 

#geometry libraries
import igl
import numpy as np
import triangle as tr

%matplotlib inline
# add markdown instruactions for installation:

shading_options = {"flat":True, # Flat or smooth shading of triangles
           "wireframe":True, "wire_width": 0.05, "wire_color": "black", # Wireframe rendering
           "width": 600, "height": 600, # Size of the viewer canvas
           "antialias": True, # Antialising, might not work on all GPUs
           "scale": 2.0, # Scaling of the model
           "side": "DoubleSide", # FrontSide, BackSide or DoubleSide rendering of the triangles
           "colormap": "viridis", "normalize": [None, None], # Colormap and normalization for colors
           "background": "#ffffff", # Background color of the canvas
           "line_width": 1.0, "line_color": "black", # Line properties of overlay lines
           "bbox": False, # Enable plotting of bounding box
           "point_color": "red", "point_size": 0.01 # Point properties of overlay points
          }
# %%
n = 20
eps = 2*np.pi/n
r = 2.0
x,y =r*np.cos(np.linspace(0,2*np.pi-eps,n)), r*np.sin(np.linspace(0,2*np.pi-eps,n))

print(f"first point: ({x[0]:.3e}, {y[0]:.3e})")
print(f"last point: ({x[-1]:.3e}, {y[-1]:.3e})")

#%%
v_triangle = np.hstack((x[:,np.newaxis], y[:,np.newaxis]))
edges_triangle = np.array([[i, (i+1)%n] for i in range(n)])
A = dict(vertices=v_triangle, segments=edges_triangle)
max_tri_area = np.pi*r*r /60  # adjust as needed
B = tr.triangulate(A, f'pqDa{max_tri_area}')
V = B['vertices']
#make 3d
V = np.hstack((V,np.zeros((V.shape[0],1))))
F = B['triangles']
print(f"Generated mesh with {V.shape[0]} vertices and {F.shape[0]} faces.")
#%%
p = mp.plot(V, F, **shading_options)

#plot mesh boundary
v_bnd = igl.boundary_loop(F)
print("Boundary loop v number:", v_bnd.shape)
plt.figure()
plt.plot(V[v_bnd,0], V[v_bnd,1], '-o')


# %% calcualte the discrete curve integral for area 
# test against discrete sum of triangles area and analytical area of the circle
