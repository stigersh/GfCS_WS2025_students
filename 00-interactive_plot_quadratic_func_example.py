#!/usr/bin/env python3
"""
Interactive Plot Quadratic Function Example
==========================================

"""

#%% [markdown]
# # interactive plot example
# learn meshgrid, surface plot, contour plot, quiver plot

#%% [markdown]
# - <span style="color:red">imports</span>

#%%
import numpy as np #for algebra
import matplotlib.pyplot as plt # for plotting
import os #for reading files and paths
# for interactive graphs - use widget backend for ipympl
%matplotlib widget
from ipywidgets import interactive # for figures with user interface code 
import matplotlib.cm as cm # for colorbar



#%% [markdown]
# # quadratic function and gradient
# what happens when you insert X,Y as points? as arrays? as matrices? try it out!

#%%
def f_quad(a,b,c,d,X,Y):
    # a,b,c,d are parameters of the quadratic function - floats
    # X,Y are numpy arrays of same size -
    # returns Z - numpy array of same size as X,Y, the function value at the grid points X,Y
    return a*X**2 + b*Y**2 + c*X*Y + d

def grad_f_quad(a,b,c,X,Y):
    # a,b,c are parameters of the quadratic function, affecting the gradient - floats
    # X,Y are numpy arrays of same size
    # returns fx, fy - numpy arrays of same size as X,Y - the gradient components at the grid points X,Y

    fx = 2*a*X + c*Y
    fy = 2*b*Y + c*X
    return  fx, fy
#%% [markdown]
# a list of useful functions: (type ?function_name in a cell to see the documentation)

# - np.array
# - np.linspace
# - np.meshgrid
# - np.vstack
# - np.hstack
# - np.concatenate
# - np.dot
# - np.cross
# - np.linalg.norm
# - np.linalg.inv
# - np.linalg.det
# - np.linalg.eig
# - np.linalg.svd
# - np.random.rand
# - np.random.randn
# - np.random.normal
# - np.mean
# - np.std
# - np.sum
# - np.min
# - np.max
# - np.clip
# - np.unique
# - np.argsort
# - np.argmin
# - np.argmax
# - np.where
# - np.allclose
# - np.isclose

#%% [markdown]
# # interactive plots

#%%
# create 2 figure 
# first is for surface plot
fig1 = plt.figure(figsize=(6, 4))
#second is for levelsets (plot with the function contour) and gradient (plot with the function quiver)
fig2 = plt.figure(figsize=(6, 4))


def interact_func_quadratic(a,b,c,d):
    # plot the quadratic function and its gradient+levelsets
    # a,b,c,d are parameters of the quadratic function - floats

    # makes f1 the active current figure
    plt.figure(fig1) # figure for surface plot
    # clear figure from last time 
    plt.clf()  
    ax = plt.axes(projection='3d')
    my_cmap = plt.get_cmap('hot')

    # here we create a grid of 100X100 points for the surface plot
    x = np.linspace(-6, 6, 100)
    y = np.linspace(-6, 6, 100)

    X, Y = np.meshgrid(x, y)
    Z = f_quad(a,b,c,d, X, Y)


    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap=my_cmap, edgecolor='none')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(f'f(x,y) = {a:.1f}x² + {b:.1f}y² + {c:.1f}xy + {d:.1f}')

    # figure for levelsets and gradient plot - only for surfaces with non zero (a,b,c)
    # surface of a plane z=d has only one level set, so the contour plot is degenerate and cannot be done.
    if not ((a==0) and (b==0) and (c==0)) : 
        # makes fig2 the active current figure
        plt.figure(fig2)  
        # clear figure from last time 
        plt.clf()  
        plt.contour(X,Y,Z,50,cmap = my_cmap)   
        plt.colorbar()
        plt.title(f'Contours & Gradient: f(x,y) = {a:.1f}x² + {b:.1f}y² + {c:.1f}xy + {d:.1f}')
        plt.xlabel('x')
        plt.ylabel('y')

        # here we create a grid of 15X15 points
        x = np.linspace(-6, 6, 15)
        y = np.linspace(-6, 6, 15)
        Xq, Yq = np.meshgrid(x, y)    
        U,V = grad_f_quad(a,b,c,Xq,Yq) 
        plt.quiver(Xq,Yq, U,V)

interactive_plot = interactive(interact_func_quadratic, a=(-1,1,0.1), b=(-1,1,0.1), c = (-1,1,0.1), d = (-10,10,0.1)) # the range for the sliders syntax is: slider_variable = (start, finish, jump)
interactive_plot

#%%
