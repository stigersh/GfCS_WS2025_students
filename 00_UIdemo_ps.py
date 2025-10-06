import polyscope as ps
import polyscope.imgui as psim
import numpy as np



# track state
my_val = 10
points = None

def my_other_function():
    print("hello")

def reset_UI_state():
    global my_val, points
    my_val = 0
    points = np.random.rand(100, 3)

def callback():
    # Executed every frame

    # state variables
    global my_val, points
   
    # Set up UI layout
    psim.PushItemWidth(150)

    if psim.Button("Reset"):
        reset_UI_state()

    # Update content in the scene
    ps.register_point_cloud("this frame point", points)

    # Build a UI element to edit a parameter, which will 
    # appear in the onscreen panel
    _, my_val = psim.InputInt("my val", my_val)

    if psim.Button("run subroutine"):
        my_other_function()

if __name__ == "__main__":
    ps.init()
    reset_UI_state()
    ps.set_user_callback(callback)
    ps.show()