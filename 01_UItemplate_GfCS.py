#!/usr/bin/env python3
"""

"""

import polyscope as ps
import polyscope.imgui as psim
import numpy as np
import os.path as osp
from geometry_utils import  center_and_scale_mesh, create_tetrahedron, add_normal_noise
from vis_ui_utils import load_mesh_from_file, scan_mesh_files, on_vertex_click

# Global mesh variables for UI
ps_mesh = None
V = None  # Vertices
F = None  # Faces

    
def reset_UI_state():
    """Reset UI state variables"""
    # Selection state globals
    global selected_vertex
    # UI mode globals  
    global color_click_mode
    # Display state globals
    global show_face_normals
    # Mesh processing globals
    global sigma
    selected_vertex = 0
    color_click_mode = False
    show_face_normals = False
    sigma = 0.0



   

def callback():
    """Polyscope UI callback function"""
    # state globals
    global selected_vertex, color_click_mode, show_face_normals, sigma
    # Mesh data globals
    global ps_mesh, V, F
    # File management globals
    global available_mesh_files, current_mesh_file

    # Set up UI layout
    psim.PushItemWidth(150)
    
    # Title
    psim.TextUnformatted("My First Mesh App")
    psim.Separator()

    # --------------------- Load Mesh Section -----------------------------------------------------
    # Create dropdown/combo for mesh files
    mesh_changed = False  # Track if new mesh is loaded and needs re-registration
    if available_mesh_files:
        # Create display names (just filenames)
        display_names = [osp.basename(f) for f in available_mesh_files]
        current_display = osp.basename(current_mesh_file) if current_mesh_file else "Select mesh file..."
        
        changed = psim.BeginCombo("Mesh Files", current_display)
        if changed:
            for i, (file_path, display_name) in enumerate(zip(available_mesh_files, display_names)):
                _, selected = psim.Selectable(display_name, file_path == current_mesh_file)
                if selected:
                    # Load new mesh from file
                    V,F = load_mesh_from_file(file_path)
                    current_mesh_file = file_path
                    reset_UI_state()
                    mesh_changed = True
            psim.EndCombo()
    
    psim.SameLine()
    if psim.Button("Load Tetrahedron"):
        V, F = create_tetrahedron()     
        current_mesh_file = "simple_tetrahedron"
        reset_UI_state()
        mesh_changed = True

    psim.Separator()
    # Register new mesh only if it changed
    if mesh_changed:
        V = center_and_scale_mesh(V)
        ps_mesh = ps.register_surface_mesh("mesh", V, F)
        ps_mesh.set_edge_width(1.0)
        ps_mesh.set_edge_color([0.0, 0.0, 0.0])
        ps.reset_camera_to_home_view()

    # Mesh info
    psim.TextUnformatted(f"Vertices: {V.shape[0]}")
    psim.TextUnformatted(f"Faces: {F.shape[0]}")
    psim.Separator()
# --------------------- Mouse Event Section ------------------------------------------------------
    # Click mode checkbox
    changed, color_click_mode = psim.Checkbox("Vertex Click Mode", color_click_mode)
    # Handle selection based on active modes
    selection = ps.get_selection()
    if selection.is_hit:
        if selection.structure_data['element_type'] == "vertex" and color_click_mode:
            selected_vertex = selection.local_index
            assert selection.structure_data['index']==selected_vertex
            on_vertex_click(selected_vertex, ps_mesh)
    
# --------------------- Other UI interface code --------------------------------------------------
    # noise parameters
    psim.TextUnformatted("Noise:")
    sigma_changed, sigma = psim.SliderFloat("Sigma", sigma, 0.0, 0.1, "%.4f")

    
    psim.Separator()
    # Face Normals
    changed, show_face_normals = psim.Checkbox("Face Normals", show_face_normals)
    # visualize calculated face normals with ps_mesh.add_vector_quantity(...)
  
    # Camera controls
    if psim.Button("Reset Camera View"):
        ps.reset_camera_to_home_view()
     
# --------------------- run geometry calculations/algorithms  -----------------  

    # Apply noise if either parameter changed
    if sigma_changed:
        # calculate vertex normals
        Nv = None
        V = add_normal_noise(V, Nv, sigma)
        ps_mesh.update_vertex_positions(V)




    psim.PopItemWidth()


if __name__ == "__main__":
    # Scan for available mesh files
    available_mesh_files = scan_mesh_files()
    reset_UI_state()
    # Initialize with simple mesh
    V, F = create_tetrahedron()
    V = center_and_scale_mesh(V)
    current_mesh_file = "tetrahedron"
    
    # Initialize polyscope
    ps.init()
    ps.set_verbosity(0)  # Reduce console output
    # Set up the camera for a nice view
    ps.set_automatically_compute_scene_extents(True)
    # Register mesh
    ps_mesh = ps.register_surface_mesh("mesh", V, F)
    ps_mesh.set_edge_width(1.0)
    ps_mesh.set_edge_color([0.0, 0.0, 0.0])


    # Set UI callback
    ps.set_user_callback(callback)
    
    # Show the interface
    ps.show()
