import tkinter as tk
from tkinter import Label
from sympy import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PIL import Image, ImageTk
import io

# Initialize the main application window
root = tk.Tk()
root.title("Function Composition")

# Error message and readme text constants
ERROR_MESSAGE = (
    "Input for {} is not properly formatted.\n"
    "Multiplication: Use 2*x instead of 2x.\n"
    "Exponents: For complex expressions,\n"
    "use x**3 instead of x^3."
)
README_TEXT = "f(x) and g must be valid SymPy expressions.\n"

# Function to check if an input string can be parsed by sympy
def sympify_input(string):
    try:
        sympify(string)
        return True
    except Exception:
        return False

# Function to display error messages
def display_error_message(input_label):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, ERROR_MESSAGE.format(input_label))

# Function to display the output using LaTeX rendering
def display_output(expression):
    output_text.delete(1.0, tk.END)
    
    # Convert sympy expression to LaTeX string
    solution_latex = latex(expression)  # Do not use equation environment
    full_latex_expression = "f(g)=" + solution_latex
    
    # Generate an image from the LaTeX string
    fig, ax = plt.subplots(figsize=(6,2))
    # Place the LaTeX string in the middle of the axis and render it
    ax.text(0.5, 0.5, f"${full_latex_expression}$", fontsize=40, ha='center', va='center')
    # Hide the axis
    ax.axis('off')
    # Save the figure to a BytesIO buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    
    # Open the image and convert to a format Tkinter can use
    img = Image.open(buf)
    photo = ImageTk.PhotoImage(image=img)
    
    # Update the label's image or create one if it doesn't exist
    if hasattr(display_output, 'label'):
        display_output.label.config(image=photo)
    else:
        display_output.label = Label(root, image=photo)
        display_output.label.image = photo  # Keep a reference to the image
        display_output.label.pack()

# Create the label for displaying the output and pack it
output_label = Label(root)
output_label.pack()

# Function to handle the composition of functions
def compose_functions():
    f_string = input_f_text.get("1.0", "end-1c")
    g_string = input_g_text.get("1.0", "end-1c")
    x = symbols('x')
    
    if not sympify_input(f_string):
        display_error_message('f(x)')
        return
    if not sympify_input(g_string):
        display_error_message('g')
        return
    
    f_expression = sympify(f_string)
    g_expression = sympify(g_string)
    composed_expression = f_expression.subs(x, g_expression)
    
    display_output(composed_expression)

# Function to open a window with readme information
def open_readme_window():
    readme_window = tk.Toplevel(root)
    readme_window.title("Readme")
    tk.Label(readme_window, text=README_TEXT).pack()
    
# UI setup for function input
input_f_label = tk.Label(root, text="f(x)=")
input_f_label.pack()
input_f_text = tk.Text(root, height=3, width=30)
input_f_text.pack()

input_g_label = tk.Label(root, text="g=")
input_g_label.pack()
input_g_text = tk.Text(root, height=3, width=30)
input_g_text.pack()

# Buttons to compose functions and open readme
compose_button = tk.Button(root, text="Compose Functions", command=compose_functions)
compose_button.pack()
readme_button = tk.Button(root, text="Open Readme", command=open_readme_window)
readme_button.pack()

# Text widget to display output
output_text = tk.Text(root, height=4, width=50)
output_text.pack()

# Start the main loop of the application
root.mainloop()
