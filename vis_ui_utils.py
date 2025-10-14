import os
import os.path as osp
import igl
"""
ui and visualization methods
"""

def load_mesh_from_file(mesh_file_path):
    """Load mesh from specific file path """
    try:
        vertices, faces = igl.read_triangle_mesh(mesh_file_path)
        return vertices, faces
    except Exception as e:
        print(f"Failed to load {mesh_file_path}: {e}")
        return None, None
    
def scan_mesh_files():
    """Scan data folder for available mesh files (.obj and .off)"""
    mesh_files = []
    data_dir = "data"
    
    if osp.exists(data_dir):
        # Scan main data directory
        for file in os.listdir(data_dir):
            if file.lower().endswith(('.obj', '.off')):
                mesh_files.append(osp.join(data_dir, file))
    
    # Sort files for consistent ordering
    mesh_files.sort()
    return mesh_files


def on_vertex_click(selected_vertex, ps_mesh):
    """Handle vertex click event - called from callback only"""
    # add other inputs as needed

    print(f"Vertex {selected_vertex}")
    # create a numpy array of #vertices and assign 1 to the selected vertex
    # visualize it using ps_mesh.add_scalar_quantity

