from nicegui import ui
import numpy as np
import ast
from ortho_logic import gram_schmidt

def main():
    # Logic Handlers
    def calculate_basis():
        input_str = text_input.value.strip()
        
        if not input_str:
            ui.notify('Please enter vector data.', type='warning')
            return

        try:
            # 1. Parse Input safely
            # We expect input like: [1, 1, 0], [1, 0, 1], [0, 1, 1]
            if not input_str.startswith('['):
                input_str = f"[{input_str}]"
            
            raw_vectors = ast.literal_eval(input_str)
            
            if not isinstance(raw_vectors, (list, tuple)):
                raise ValueError("Input must be a collection of vectors.")

            # 2. Run Calculation
            orthonormal_vectors = gram_schmidt(raw_vectors)
            
            # 3. Output for Display
            results_container.clear()
            with results_container:
                ui.label('Orthonormal Basis Result: ').classes('text-xl font-bold mb-2')
                
                for i, vec in enumerate(orthonormal_vectors):
                    rounded = np.round(vec, 4)
                    
                    latex_str = f"$$u_{i+1} = \\begin{{bmatrix}} {' \\\\ '.join(map(str, rounded))} \\end{{bmatrix}}$$"
                    ui.markdown(latex_str)
                    
            ui.notify('Calculation successful!', type='positive')

        except ValueError as ve:
            ui.notify(f"Math Error: {str(ve)}", type='negative')
        except SyntaxError:
            ui.notify("Format Error: Check your syntax (e.g., use brackets [1,0], [0,1])", type='negative')
        except Exception as e:
            ui.notify(f"Unexpected Error: {str(e)}", type='negative')

    # GUI Layout
    with ui.column().classes('w-full items-center justify-center p-10 space-y-4'):
        
        # Title 
        with ui.card().classes('w-full max-w-2xl p-6 bg-slate-50'):
            ui.label('Orthonormal Basis Finder').classes('text-2xl font-bold text-slate-800')
            ui.label('Enter vectors separated by commas. Example: [1, 1, 0], [1, 0, 1]').classes('text-slate-500 italic')

            # Input
            text_input = ui.textarea(
                label='Input Vectors', 
                placeholder='[1, 1, 0], [1, 0, 1], [0, 1, 1]'
            ).classes('w-full').props('outlined')

            # Action
            ui.button('Calculate Basis', on_click=calculate_basis).classes('w-full bg-blue-600 text-white')

        # Results
        results_container = ui.column().classes('w-full max-w-2xl items-center bg-white p-4 rounded shadow-md')

    # GUI
    ui.run(title="Orthonormal Calculator")

if __name__ in {"__main__", "__mp_main__"}:
    main()