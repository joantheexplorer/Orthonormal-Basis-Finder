import sympy

def gram_schmidt_symbolic(raw_vectors):
    vectors = [sympy.Matrix(v) for v in raw_vectors]

    matrix_check = sympy.Matrix(raw_vectors)
    
    if matrix_check.rank() < len(vectors):
        raise ValueError("Vectors are linearly dependent. Please ensure they are unique and not multiples of each other.")

    basis = sympy.GramSchmidt(vectors, orthonormal=True)
    
    return basis