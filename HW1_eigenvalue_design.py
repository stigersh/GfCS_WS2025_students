import numpy as np
# Helper code for power and inverse power iteration assignment
n = 5
# Step 1: design eigenvalues
D_vals = np.array([5, 4, 2, 1, 0.5])
D = np.diag(D_vals)

# Step 2: generate orthogonal V
X = np.random.randn(n, n)
V, _ = np.linalg.qr(X)

# Step 3: build symmetric matrix
A = V @ D @ V.T

# Step 4: verify
eigvals, _ = np.linalg.eigh(A)
print("Designed eigenvalues:", D_vals)
print("Computed eigenvalues:", np.round(eigvals, 3))