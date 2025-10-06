#!/bin/bash

# Remove existing virtual environment if it exists
echo "Removing existing virtual environment..."
rm -rf .venv

# Create a clean virtual environment
echo "Creating clean virtual environment..."
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip to latest version
pip install --upgrade pip

# Install packages in proper order to avoid conflicts
echo "Installing packages in clean environment..."

# Core scientific computing
pip install numpy
pip install scipy
pip install matplotlib

# Geometry processing
pip install libigl

# Mesh visualization dependencies
pip install pythreejs

# Mesh visualization (install from GitHub)
pip install git+https://github.com/skoch9/meshplot.git

# 3D visualization
pip install polyscope==2.5.0

# Jupyter and interactive widgets - install together for compatibility
pip install jupyter
pip install notebook
pip install jupyterlab
pip install ipywidgets
pip install ipympl

# Ensure kernel is properly installed
python -m ipykernel install --user --name=venv --display-name="Python (venv)"

echo "Environment setup complete!"
echo "To activate: source .venv/bin/activate"
echo "To deactivate: deactivate"