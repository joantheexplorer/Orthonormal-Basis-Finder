import sympy

def gram_schmidt_with_steps(raw_vectors):
    cleaned_vectors = []
    for v in raw_vectors:
        cleaned_vectors.append(sympy.Matrix([sympy.nsimplify(x) for x in v]))
        
    if sympy.Matrix.hstack(*cleaned_vectors).rank() < len(cleaned_vectors):
        raise ValueError("Vectors are linearly dependent.")

    orthogonal_basis = []
    orthonormal_basis = []
    steps = []

    for i, v in enumerate(cleaned_vectors):
        step_data = {
            'index': i + 1,
            'input_vec': v,
            'projections': [],
            'orthogonal_vec': None,
            'norm': None,
            'final_vec': None
        }
        
        u = v
        
        for prev_u in orthogonal_basis:
            numerator = v.dot(prev_u)
            denominator = prev_u.dot(prev_u)
            
            coeff = numerator / denominator
            projection = coeff * prev_u
            
            step_data['projections'].append({
                'basis_vec': prev_u,
                'coeff': coeff,
                'projection': projection
            })
            
            u = u - projection

        u = u.applyfunc(sympy.simplify)
        step_data['orthogonal_vec'] = u
        orthogonal_basis.append(u)

        norm = u.norm()
        norm = sympy.simplify(norm)
        step_data['norm'] = norm
        
        e = u / norm
        e = e.applyfunc(sympy.simplify)
        step_data['final_vec'] = e
        orthonormal_basis.append(e)
        
        steps.append(step_data)

    return orthonormal_basis, steps