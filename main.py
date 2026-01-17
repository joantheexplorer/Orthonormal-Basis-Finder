from nicegui import ui
import sympy
from ortho_logic import gram_schmidt_symbolic
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
            ui.label('2. Enter Values').classes(SECTION_HEADER)
            
            with ui.grid(columns=n_vectors).classes(INPUT_GRID):
                for i in range(n_vectors):
                    with ui.column().classes(VECTOR_COLUMN):
                        
                        ui.html(f'<div style="{VECTOR_LABEL}">vector v{i+1}</div>', sanitize=False)
                        
                        col_inputs = []
                        for j in range(n_dim):
                            field = ui.input().props('outlined dense input-style="text-align: center"').classes(INPUT_FIELD)
                            col_inputs.append(field)
                        vector_input_fields.append(col_inputs)

            with ui.row().classes(BUTTON_ROW):
                ui.button('Calculate Basis', on_click=run_calculation).classes(BUTTON_CALCULATE)
                ui.button('Reset', on_click=reset_app).classes(BUTTON_RESET)

    def format_plain_text(val):
        return sympy.latex(val)

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

            basis = gram_schmidt_symbolic(raw_vectors)

            results_area.clear()
            results_area.set_visibility(True)
            
            with results_area:
                ui.label('3. Results').classes(SECTION_HEADER)
                
                ui.label("Therefore, the Gram-Schmidt Process produced the following orthonormal basis for the subspace spanned by the given vectors:") \
                    .classes(RESULT_INSTRUCTION)

                box_style = RESULT_BOX

                ui.label('Exact Form (Symbolic):').classes(SUBSECTION_HEADER)

                with ui.row().classes(VECTOR_NOTATION_ROW):
                    
                    indices = [str(k+1) for k in range(len(basis))]
                    v_labels = ", ".join([f"vector v{k}" for k in indices])
                    
                    ui.label(f"{{ {v_labels} }} = {{").classes(VECTOR_OPENING_BRACE)

                    for i, sym_vec in enumerate(basis):
                        
                        with ui.column().classes(RESULT_COLUMN):
                            for val in sym_vec:
                                latex_str = sympy.latex(val)
                                
                                with ui.card().classes(box_style):
                                    ui.html(f'<div style="text-align: center;">$${latex_str}$$</div>', sanitize=False)
                        
                        if i < len(basis) - 1:
                            ui.label(',').classes(VECTOR_COMMA)

                    ui.element('div').classes(VECTOR_CLOSING_BRACKET)
                    ui.label('}').classes(VECTOR_CLOSING_BRACE)

                ui.run_javascript('renderMath();')

                ui.separator()

                ui.label('Decimal Approximation:').classes(SUBSECTION_HEADER_MARGIN_TOP)

                with ui.row().classes(VECTOR_NOTATION_ROW):
                    
                    ui.label(f"{{ {v_labels} }} ≈ {{").classes(VECTOR_OPENING_BRACE)

                    for i, sym_vec in enumerate(basis):
                        with ui.column().classes(RESULT_COLUMN):
                            
                            for val in sym_vec:
                                approx = val.evalf()
                                try:
                                    f_val = float(approx)
                                    rounded_val = round(f_val, 6)
                                    if rounded_val.is_integer():
                                        display_str = f"{rounded_val:.0f}"
                                    else:
                                        display_str = f"{rounded_val:.6f}"
                                
                                except TypeError:
                                    display_str = str(approx)

                                with ui.card().classes(box_style):
                                    ui.html(f'<div style="text-align: center;">$${display_str}$$</div>', sanitize=False)
                        
                        if i < len(basis) - 1:
                             ui.label(',').classes(VECTOR_COMMA)

                    ui.element('div').classes(VECTOR_CLOSING_BRACKET)
                    ui.label('}').classes(VECTOR_CLOSING_BRACE)

                ui.run_javascript('renderMath();')

        except ValueError as e:
            ui.notify(str(e), type='warning')
        except Exception as e:
            ui.notify(f"Error: {e}", type='negative')

    with ui.column().classes(MAIN_CONTAINER):
        
        with ui.card().classes(CONFIG_CARD):
            ui.label('1. Configuration').classes(CONFIG_HEADER)
            
            with ui.row().classes(INPUT_ROW):
                num_vecs_input = ui.number('How many vectors?', value=2, min=1, precision=0).classes(INPUT_FIELD_WIDTH)
                dim_input = ui.number('Dimensions per vector?', value=3, min=1, precision=0).classes(INPUT_FIELD_WIDTH)
                
                ui.button('Generate Inputs', on_click=create_input_grid).classes(BUTTON_GENERATE)

        input_area = ui.card().classes(INPUT_AREA_CARD)
        input_area.set_visibility(False)

        results_area = ui.card().classes(RESULTS_AREA_CARD)
        results_area.set_visibility(False)

    ui.run(title="Exact Basis Finder")

if __name__ in {"__main__", "__mp_main__"}:
    main()