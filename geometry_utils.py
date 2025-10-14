#!/usr/bin/env python3
"""
Geometryic methods
"""

import numpy as np
import igl

def create_tetrahedron():
    """Create a simple tetrahedron"""
    V = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0], 
        [0.5, 1.0, 0.0],
        [0.5, 0.5, 1.0]
    ])
    #fix the orrientation!
    F = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ])
    
    return V, F



def add_normal_noise(V, Nv, s):
    """Add noise to the vertices
    
    Args:
        V: numpy array of mesh vertices
        Nv: vertex normals
        s: noise scale
        
    Returns:
        numpy array of noisy vertices
    """
    # create a vector of noise scala values and multiply with normals
    # add to the vertices of the mesh

    return V 

def center_and_scale_mesh(V):
    """Center mesh at origin and scale to unit bounding box
    
    Args:
        V: numpy array of mesh vertices
        
    Returns:
        numpy array of centered and scaled vertices
    """
    # Center at origin
    center = np.mean(V, axis=0)
    V_centered = V - center
    
    # Scale to unit bounding box
    bbox_size = np.max(V_centered, axis=0) - np.min(V_centered, axis=0)
    max_extent = np.max(bbox_size)
    if max_extent > 0:
        V_scaled = V_centered / max_extent
    else:
        V_scaled = V_centered
    
    return V_scaled



