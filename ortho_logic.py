import numpy as np

def gram_schmidt(vectors):
    """
    Takes a list of vectors (lists or numpy arrays) and returns 
    the orthonormal basis using the Gram-Schmidt process.
    """
    basis = []
    
    for v in vectors:
        v = np.array(v, dtype=float)
        
        temp_vec = v.copy()
        for b in basis:
            proj = np.dot(v, b) * b
            temp_vec -= proj
        
        # Check if the resulting vector is zero
        # (This happens if vectors are linearly dependent)
        norm = np.linalg.norm(temp_vec)
        
        if norm < 1e-10: 
            raise ValueError("Vectors are linearly dependent. Cannot form a basis.")
            
        # Normalize the vector
        unit_vec = temp_vec / norm
        basis.append(unit_vec)
        
    return basis