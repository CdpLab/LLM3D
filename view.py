import open3d as o3d
import numpy as np
import os

def render_paper_figure(scene_id):
    base_dir = r"/media/asus/SATA2/ds/sceond/3D-MoRe/3D-MoRe-master/data/scannet/scannet_data"
    
    # Try to load the original mesh
    p2 = os.path.join(base_dir, f"{scene_id}_vh_clean_2.ply")
    p1 = os.path.join(base_dir, f"{scene_id}_vh_clean.ply")
    
    mesh_path = p2 if os.path.exists(p2) else p1
    
    if not os.path.exists(mesh_path):
        print(f"Error: Could not find mesh for {scene_id} at {base_dir}")
        return
        
    print(f"Loading {mesh_path}...")
    mesh = o3d.io.read_triangle_mesh(mesh_path)
    
    if mesh.is_empty():
        print("Error: Mesh is empty!")
        return

    # Critical Step 1: Compute normals for solid lighting
    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()
    
    # Critical Step 2: Handle Colors properly
    if mesh.has_vertex_colors():
        colors = np.asarray(mesh.vertex_colors)
        if colors.max() > 1.0:
            colors = colors / 255.0
            mesh.vertex_colors = o3d.utility.Vector3dVector(colors)
    else:
        # If no colors, paint it light gray to see the structure
        mesh.paint_uniform_color([0.8, 0.8, 0.8])

    print("Rendering... Use mouse to rotate, scroll to zoom. Press 'Q' or close window to exit.")
    
    # Create visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=f"Paper Visualization: {scene_id}", width=1920, height=1080)
    vis.add_geometry(mesh)
    
    # Critical Step 3: Setup Render Options for Paper Quality
    opt = vis.get_render_option()
    opt.background_color = np.array([1.0, 1.0, 1.0])  # Pure white background
    opt.mesh_show_back_face = True                    # Ensure inside walls are visible
    opt.mesh_show_wireframe = False                   # NO wireframe, we want a solid look
    opt.light_on = True                               # Enable shading/lighting
    
    # Run the visualizer
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    scenes = ["scene0030_00", "scene0088_00", "scene0086_00"]
    for s in scenes:
        render_paper_figure(s)
