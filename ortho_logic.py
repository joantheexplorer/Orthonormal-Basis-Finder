import sympy

def gram_schmidt_symbolic(raw_vectors):
    if not raw_vectors:
        return []

    cleaned_vectors = []
    for v in raw_vectors:
        try:
            clean_v = sympy.Matrix([sympy.nsimplify(x) for x in v])
            cleaned_vectors.append(clean_v)
        except Exception:
            raise ValueError(f"Invalid vector data: {v}")

    ref_dim = len(cleaned_vectors[0])
    if any(len(v) != ref_dim for v in cleaned_vectors):
        raise ValueError(f"Dimension mismatch: All vectors must have dimension {ref_dim}.")

    matrix_check = sympy.Matrix.hstack(*cleaned_vectors)
    
    if matrix_check.rank() < len(cleaned_vectors):
        raise ValueError("Vectors are linearly dependent.")

    basis = sympy.GramSchmidt(cleaned_vectors, orthonormal=True)
    
    final_basis = [vec.applyfunc(sympy.simplify) for vec in basis]
    
    return final_basis