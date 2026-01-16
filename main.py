from nicegui import ui
import sympy
from ortho_logic import gram_schmidt_symbolic

def main():
    vector_input_fields = []

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
            ui.label('2. Enter Values').classes('text-xl font-bold mb-2')
            
            with ui.grid(columns=n_vectors).classes('gap-6 mb-4 items-start'):
                for i in range(n_vectors):
                    with ui.column().classes('items-center gap-2'):
                        
                        ui.html(f'<div style="font-size: 1.25rem; font-weight: bold;">vector v{i+1}</div>', sanitize=False)
                        
                        col_inputs = []
                        for j in range(n_dim):
                            field = ui.number(step=1).props('outlined dense input-style="text-align: center"').classes('w-28')
                            col_inputs.append(field)
                        vector_input_fields.append(col_inputs)

            ui.button('Calculate Basis', on_click=run_calculation).classes('bg-green-600 text-white w-full')

    def format_plain_text(val):
        s = str(val)
        s = s.replace('sqrt', '√')
        s = s.replace('*', '')
        return s

    def run_calculation():
        try:
            raw_vectors = []
            for col_inputs in vector_input_fields:
                current_vector = []
                for box in col_inputs:
                    if box.value is None:
                        raise ValueError("Fields cannot be empty")
                    current_vector.append(float(box.value))
                raw_vectors.append(current_vector)

            basis = gram_schmidt_symbolic(raw_vectors)

            results_area.clear()
            results_area.set_visibility(True)
            
            with results_area:
                ui.label('3. Results').classes('text-xl font-bold mb-4')

                box_style = 'w-28 h-10 flex items-center justify-center border border-gray-300 rounded shadow-none bg-gray-50 overflow-hidden'

                ui.label('Exact Form (Symbolic):').classes('text-lg text-slate-600 font-bold mb-2')

                with ui.row().classes('items-center gap-2 flex-nowrap overflow-x-auto p-4'):
                    
                    indices = [str(k+1) for k in range(len(basis))]
                    v_labels = ", ".join([f"vector v{k}" for k in indices])
                    
                    ui.label(f"{{ {v_labels} }} = {{").classes('text-2xl font-bold whitespace-nowrap')

                    for i, sym_vec in enumerate(basis):
                        
                        with ui.column().classes('gap-1'):
                            for val in sym_vec:
                                text_str = format_plain_text(val)
                                
                                with ui.card().classes(box_style):
                                    ui.label(text_str).classes('text-sm')
                        
                        if i < len(basis) - 1:
                            ui.label(',').classes('text-4xl font-bold -mt-2')

                    ui.label('}').classes('text-2xl font-bold')


                ui.separator()

                ui.label('Decimal Approximation:').classes('text-lg text-slate-600 font-bold mt-4 mb-2')

                with ui.row().classes('items-center gap-2 flex-nowrap overflow-x-auto p-4'):
                    
                    ui.label(f"{{ {v_labels} }} ≈ {{").classes('text-2xl font-bold whitespace-nowrap')

                    for i, sym_vec in enumerate(basis):
                        with ui.column().classes('gap-1'):
                            decimal_values = [float(x.evalf()) for x in sym_vec]
                            for val in decimal_values:
                                
                                # --- INTELLIGENT ROUNDING LOGIC ---
                                rounded_val = round(val, 6)
                                
                                # Check if it is a whole number (e.g. 1.0, 0.0)
                                if rounded_val.is_integer():
                                    # Format as integer (0 decimal places)
                                    fmt_string = '%.0f'
                                else:
                                    # Keep 6 decimal places for non-integers
                                    fmt_string = '%.6f'

                                with ui.card().classes(box_style):
                                    ui.number(value=rounded_val, format=fmt_string).props('borderless dense readonly input-style="text-align: center"').classes('w-full bg-transparent')
                        
                        if i < len(basis) - 1:
                             ui.label(',').classes('text-4xl font-bold -mt-2')

                    ui.label('}').classes('text-2xl font-bold')

        except ValueError as e:
            ui.notify(str(e), type='warning')
        except Exception as e:
            ui.notify(f"Error: {e}", type='negative')

    with ui.column().classes('w-full items-center p-10 space-y-4'):
        
        with ui.card().classes('w-full max-w-5xl bg-slate-50'):
            ui.label('1. Configuration').classes('text-xl font-bold text-slate-800')
            with ui.row().classes('w-full gap-4'):
                num_vecs_input = ui.number('How many vectors?', value=2, min=1, precision=0).classes('w-40')
                dim_input = ui.number('Dimensions per vector?', value=3, min=1, precision=0).classes('w-40')
                ui.button('Generate Inputs', on_click=create_input_grid).classes('mt-2 bg-blue-600 text-white')

        input_area = ui.card().classes('w-full max-w-5xl')
        input_area.set_visibility(False)

        results_area = ui.card().classes('w-full max-w-5xl bg-white')
        results_area.set_visibility(False)

    ui.run(title="Exact Basis Finder")

if __name__ in {"__main__", "__mp_main__"}:
    main()