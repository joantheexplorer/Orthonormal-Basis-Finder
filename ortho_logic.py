import sympy

def gram_schmidt_symbolic(vectors):

    sympy_vecs = []
    for v in vectors:
        exact_v = [sympy.nsimplify(x) for x in v]
        sympy_vecs.append(sympy.Matrix(exact_v))

    basis = sympy.GramSchmidt(sympy_vecs, orthonormal=True)
    
    return basis