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
                            field = ui.input().props('outlined dense input-style="text-align: center"').classes('w-28')
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
                    if not box.value:
                        raise ValueError("Fields cannot be empty")
                    
                    try:
                        val = sympy.sympify(box.value)
                        current_vector.append(val)
                    except:
                        raise ValueError(f"Could not understand input: '{box.value}'")

                raw_vectors.append(current_vector)

            basis = gram_schmidt_symbolic(raw_vectors)

            results_area.clear()
            results_area.set_visibility(True)
            
            with results_area:
                ui.label('3. Results').classes('text-xl font-bold mb-4')

                box_style = 'min-w-[7rem] max-w-[15rem] w-auto min-h-[2.5rem] p-4 flex items-center justify-center border border-gray-300 rounded shadow-none bg-gray-50'

                ui.label('Exact Form (Symbolic):').classes('text-lg text-slate-600 font-bold mb-2')

                with ui.row().classes('items-center gap-0 flex-nowrap overflow-x-auto p-4 w-full min-w-0'):
                    
                    indices = [str(k+1) for k in range(len(basis))]
                    v_labels = ", ".join([f"vector v{k}" for k in indices])
                    
                    ui.label(f"{{ {v_labels} }} = {{").classes('text-2xl font-bold whitespace-nowrap flex-none mr-4')

                    for i, sym_vec in enumerate(basis):
                        
                        with ui.column().classes('gap-1 flex-none'):
                            for val in sym_vec:
                                text_str = format_plain_text(val)
                                
                                with ui.card().classes(box_style):
                                    ui.label(text_str).classes('text-sm break-all text-center leading-tight')
                        
                        if i < len(basis) - 1:
                            ui.label(',').classes('text-4xl font-bold -mt-2 flex-none mx-2')

                    ui.element('div').classes('w-8 shrink-0')

                    ui.label('}').classes('text-2xl font-bold flex-none')

                ui.separator()

                ui.label('Decimal Approximation:').classes('text-lg text-slate-600 font-bold mt-4 mb-2')

                with ui.row().classes('items-center gap-0 flex-nowrap overflow-x-auto p-4 w-full min-w-0'):
                    
                    ui.label(f"{{ {v_labels} }} ≈ {{").classes('text-2xl font-bold whitespace-nowrap flex-none mr-4')

                    for i, sym_vec in enumerate(basis):
                        with ui.column().classes('gap-1 flex-none'):
                            
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
                                    ui.label(display_str).classes('text-sm break-all text-center leading-tight')
                        
                        if i < len(basis) - 1:
                             ui.label(',').classes('text-4xl font-bold -mt-2 flex-none mx-2')

                    ui.element('div').classes('w-8 shrink-0')
                    
                    ui.label('}').classes('text-2xl font-bold flex-none')

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