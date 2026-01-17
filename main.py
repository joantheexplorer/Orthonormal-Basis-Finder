from nicegui import ui
import sympy
from ortho_logic import gram_schmidt_with_steps
from styles import *

ui.add_head_html('''
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
        },
        svg: {fontCache: 'global'}
    };
    function renderMath() {
        if (window.MathJax?.typesetPromise) {
            MathJax.typesetPromise().catch(err => console.log(err));
        }
    }
</script>
''')

def main():
    ui.add_css('''
        .nicegui-content { 
            padding: 0;
            background-color: #EEF2FF;
            background-image: 
                radial-gradient(at 40% 20%, hsla(266,100%,70%,1) 0px, transparent 50%),
                radial-gradient(at 80% 0%, hsla(189,100%,56%,1) 0px, transparent 50%),
                radial-gradient(at 0% 50%, hsla(340,100%,76%,1) 0px, transparent 50%);}
    ''')
    vector_input_fields = []

    def reset_app():
        num_vecs_input.value = 2
        dim_input.value = 3
        
        vector_input_fields.clear()
        
        input_area.clear()
        input_area.set_visibility(False)
        
        results_area.clear()
        results_area.set_visibility(False)
        
        ui.notify('Application reset.', type='info')

    def create_input_grid():
        try:
            n_vectors = int(num_vecs_input.value)
            n_dim = int(dim_input.value)
        except:
            ui.notify('Please enter valid integers.', type='warning')
            return

        input_area.clear()
        results_area.clear()
        vector_input_fields.clear()
        input_area.set_visibility(True)

        with input_area:
            ui.label('Enter Values').classes(SECTION_HEADER)
            
            with ui.grid(columns=n_vectors).classes(INPUT_GRID):
                for i in range(n_vectors):
                    with ui.column().classes(VECTOR_COLUMN):
                        
                        ui.html(f'<div style="{VECTOR_LABEL}">$$ v_{{{i+1}}} $$</div>', sanitize=False)
                        
                        col_inputs = []
                        for j in range(n_dim):
                            field = ui.input().props('outlined dense input-style="text-align: center"').classes(INPUT_FIELD)
                            col_inputs.append(field)
                        vector_input_fields.append(col_inputs)

            with ui.row().classes(BUTTON_ROW):
                ui.button('Calculate Basis', on_click=run_calculation).classes(BUTTON_CALCULATE)
                ui.button('Reset', on_click=reset_app).classes(BUTTON_RESET)
        
        ui.run_javascript('renderMath();')

    def parse_user_input(user_input):
        normalized = user_input.strip()
        normalized = normalized.replace('√', 'sqrt(')
        
        sqrt_count = user_input.count('√')
        if sqrt_count > 0:
            normalized = normalized.replace('sqrt(', 'sqrt')
            normalized = normalized.replace('sqrt', 'sqrt(')
            parts = []
            i = 0
            while i < len(normalized):
                if normalized[i:i+5] == 'sqrt(':
                    parts.append('sqrt(')
                    i += 5
                    arg_start = i
                    depth = 1
                    while i < len(normalized) and depth > 0:
                        if normalized[i] == '(':
                            depth += 1
                        elif normalized[i] == ')':
                            depth -= 1
                        i += 1
                    if depth == 1:
                        parts.append(normalized[arg_start:i])
                        parts.append(')')
                    else:
                        parts.append(normalized[arg_start:i])
                else:
                    parts.append(normalized[i])
                    i += 1
            normalized = ''.join(parts)
        
        return normalized

    def run_calculation():
        try:
            raw_vectors = []
            for col_inputs in vector_input_fields:
                current_vector = []
                for box in col_inputs:
                    if not box.value:
                        raise ValueError("Fields cannot be empty")
                    
                    try:
                        parsed_input = parse_user_input(box.value)
                        val = sympy.sympify(parsed_input)
                        current_vector.append(val)
                    except:
                        raise ValueError(f"Could not understand input: '{box.value}'")

                raw_vectors.append(current_vector)

            basis, steps = gram_schmidt_with_steps(raw_vectors)

            results_area.clear()
            results_area.set_visibility(True)
            
            with results_area:
                ui.label('Results').classes(SECTION_HEADER)
                
                ui.label("Therefore, the Gram-Schmidt Process produced the following orthonormal basis for the subspace spanned by the given vectors:") \
                    .classes(RESULT_INSTRUCTION)
                
                ui.html(
                    r'''
                    <div class="w-full text-left text-gray-800 mb-8 text-lg leading-relaxed">
                        <p class="mb-2">According to the Gram-Schmidt process:</p>
                        $$ \vec{u}_k = \vec{v}_k - \sum_{j=1}^{k-1} \text{proj}_{\vec{u}_j}(\vec{v}_k) $$
                        <p class="my-4">where the projection is:</p>
                        $$ \text{proj}_{\vec{u}_j}(\vec{v}_k) = \frac{\langle \vec{v}_k, \vec{u}_j \rangle}{||\vec{u}_j||^2} \vec{u}_j $$
                        <p class="mt-4">The normalized vector is:</p>
                        $$ \vec{e}_k = \frac{1}{||\vec{u}_k||} \vec{u}_k $$
                    </div>
                    ''',
                    sanitize=False
                )

                for step in steps:
                    idx = step['index']
                    
                    with ui.column().classes('w-full mb-8'):
                        ui.label(f'Step {idx}').classes('text-xl font-bold text-slate-800 mb-4 border-b pb-2 w-full')
                        
                        v_latex = sympy.latex(step['input_vec'])
                        u_latex = sympy.latex(step['orthogonal_vec'])
                        norm_latex = sympy.latex(step['norm'])
                        e_latex = sympy.latex(step['final_vec'])

                        if idx == 1:
                            ui.html(
                                f'''
                                <div class="w-full overflow-x-auto text-lg">
                                    $$ \\vec{{u}}_1 = \\vec{{v}}_1 = {v_latex} $$
                                </div>
                                <div class="w-full overflow-x-auto mt-6 text-lg">
                                    $$ \\vec{{e}}_1 = \\frac{{1}}{{||\\vec{{u}}_1||}} \\vec{{u}}_1 = \\frac{{1}}{{{norm_latex}}} {u_latex} = {e_latex} $$
                                </div>
                                ''',
                                sanitize=False
                            )
                        
                        else:
                            ui.label('Calculate projections:').classes('text-md font-bold text-gray-600 mb-2')
                            
                            proj_terms_latex = []
                            
                            for p_idx, proj in enumerate(step['projections']):
                                prev_u_latex = sympy.latex(proj['basis_vec'])
                                coeff_latex = sympy.latex(proj['coeff'])
                                proj_res_latex = sympy.latex(proj['projection'])
                                
                                proj_terms_latex.append(proj_res_latex)
                                
                                ui.html(
                                    f'''
                                    <div class="ml-4 mb-4 text-md w-full overflow-x-auto">
                                        $$ \\text{{proj}}_{{\\vec{{u}}_{p_idx+1}}}(\\vec{{v}}_{idx}) = 
                                        {coeff_latex} \\cdot {prev_u_latex} = {proj_res_latex} $$
                                    </div>
                                    ''', 
                                    sanitize=False
                                )

                            subtraction_str = f"{v_latex}"
                            for term in proj_terms_latex:
                                subtraction_str += f" - {term}"

                            ui.label('Calculate orthogonal vector:').classes('text-md font-bold text-gray-600 mt-4 mb-2')
                            
                            ui.html(
                                f'''
                                <div class="w-full overflow-x-auto text-lg">
                                    $$ \\begin{{align*}} 
                                    \\vec{{u}}_{idx} &= \\vec{{v}}_{idx} - \\sum_{{j=1}}^{{{idx-1}}} \\text{{proj}}_{{\\vec{{u}}_j}}(\\vec{{v}}_{idx}) \\\\
                                    &= {subtraction_str} \\\\
                                    &= {u_latex}
                                    \\end{{align*}} $$
                                </div>
                                ''',
                                sanitize=False
                            )

                            ui.label('Normalize:').classes('text-md font-bold text-gray-600 mt-4 mb-2')
                            
                            ui.html(
                                f'''
                                <div class="w-full overflow-x-auto text-lg">
                                    $$ \\vec{{e}}_{idx} = \\frac{{1}}{{||\\vec{{u}}_{idx}||}} \\vec{{u}}_{idx} = 
                                    \\frac{{1}}{{{norm_latex}}} {u_latex} = {e_latex} $$
                                </div>
                                ''',
                                sanitize=False
                            )

                ui.separator()

                ui.label('Exact Form (Symbolic):').classes(SUBSECTION_HEADER)
                
                basis_latex = [sympy.latex(vec) for vec in basis]
                basis_str = ", ".join(basis_latex)
                
                labels_str = ", ".join([f"\\vec{{e}}_{{{k+1}}}" for k in range(len(basis))])

                ui.html(
                    f'''
                    <div class="w-full overflow-x-auto text-lg flex justify-start items-center p-4">
                        $$ \\{{ {labels_str} \\}} = \\left\\{{ {basis_str} \\right\\}} $$
                    </div>
                    ''',
                    sanitize=False
                )

                ui.separator()

                ui.label('Decimal Approximation:').classes(SUBSECTION_HEADER_MARGIN_TOP)

                decimal_latex = []
                for vec in basis:
                    def smart_round(x):
                        f = float(x.evalf())
                        r = round(f, 6)
                        return int(r) if r.is_integer() else r

                    approx_vec = vec.applyfunc(smart_round)
                    decimal_latex.append(sympy.latex(approx_vec))

                decimal_str = ", ".join(decimal_latex)

                ui.html(
                    f'''
                    <div class="w-full overflow-x-auto text-lg flex justify-start items-center p-4">
                        $$ \\{{ {labels_str} \\}} \\approx \\left\\{{ {decimal_str} \\right\\}} $$
                    </div>
                    ''',
                    sanitize=False
                )

                ui.separator()
                ui.label('Export Result').classes(SUBSECTION_HEADER_MARGIN_TOP)
                
                with ui.row().classes('w-full gap-4'):
                    
                    def copy_python_code():
                        code = "import numpy as np\n\n"
                        var_names = []
                        for i, vec in enumerate(basis):
                            vals = [f"{float(v.evalf()):.8f}" for v in vec]
                            vec_str = f"e{i+1} = np.array([{', '.join(vals)}])"
                            code += vec_str + "\n"
                            var_names.append(f"e{i+1}")
                        code += f"\n# Orthonormal Basis Matrix (Columns)\nQ = np.column_stack([{', '.join(var_names)}])"
                        
                        ui.clipboard.write(code)
                        ui.notify('Python/NumPy code copied to clipboard!', type='positive')

                    def copy_latex_code():
                        latex_code = f"\\left\\{{ {basis_str} \\right\\}}"
                        ui.clipboard.write(latex_code)
                        ui.notify('LaTeX code copied to clipboard!', type='positive')

                    ui.button('Copy as Python Code', on_click=copy_python_code, icon='code').classes('!bg-violet-500 text-white')
                    ui.button('Copy as LaTeX', on_click=copy_latex_code, icon='content_copy').classes('!bg-violet-500 text-white')

                n_dim = int(dim_input.value)
                
                if n_dim in [2, 3]:
                    ui.separator()
                    ui.label('Visual Verification (2D/3D)').classes(SUBSECTION_HEADER_MARGIN_TOP)
                    
                    traces = []

                    for i, vec in enumerate(raw_vectors):
                        coords = [float(val.evalf()) for val in vec]
                        if n_dim == 2: coords.append(0.0) 
                        
                        traces.append({
                            'type': 'scatter3d',
                            'mode': 'lines+markers',
                            'x': [0, coords[0]], 'y': [0, coords[1]], 'z': [0, coords[2]],
                            'line': {'color': 'red', 'width': 5, 'dash': 'dash'},
                            'marker': {'size': 4, 'color': 'red'},
                            'name': f'Input v{i+1}'
                        })

                    for i, vec in enumerate(basis):
                        coords = [float(val.evalf()) for val in vec]
                        if n_dim == 2: coords.append(0.0) 
                        
                        traces.append({
                            'type': 'scatter3d',
                            'mode': 'lines+markers',
                            'x': [0, coords[0]], 'y': [0, coords[1]], 'z': [0, coords[2]],
                            'line': {'color': 'green', 'width': 8},
                            'marker': {'size': 6, 'color': 'green'},
                            'name': f'Basis e{i+1}'
                        })

                    ui.plotly({
                        'data': traces,
                        'layout': {
                            'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0},
                            'scene': {
                                'xaxis': {'title': 'X'},
                                'yaxis': {'title': 'Y'},
                                'zaxis': {'title': 'Z'},
                                'aspectmode': 'data' 
                            },
                            'showlegend': True,
                            'height': 500,
                        }
                    }).classes('w-full h-[500px] border rounded bg-slate-50')

                ui.run_javascript('renderMath();')

        except ValueError as e:
            ui.notify(str(e), type='warning')
        except Exception as e:
            ui.notify(f"Error: {e}", type='negative')

    with ui.column().classes(MAIN_CONTAINER):
        
        ui.label('ORTHONORMAL BASIS FINDER').classes(CONFIG_HEADER)
        
        with ui.card().classes(CONFIG_CARD):
            ui.label('Configuration').classes(SECTION_HEADER)
            
            with ui.row().classes(INPUT_ROW):
                num_vecs_input = ui.number('How many vectors?', value=2, min=1, precision=0).classes(INPUT_FIELD_WIDTH)
                dim_input = ui.number('Dimensions per vector?', value=3, min=1, precision=0).classes(INPUT_FIELD_WIDTH)
                
                ui.button('Generate Inputs', on_click=create_input_grid).classes(BUTTON_GENERATE)

        input_area = ui.card().classes(INPUT_AREA_CARD)
        input_area.set_visibility(False)

        results_area = ui.card().classes(RESULTS_AREA_CARD)
        results_area.set_visibility(False)

    ui.run(title="Orthonormal Basis Finder")

if __name__ in {"__main__", "__mp_main__"}:
    main()