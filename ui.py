import tkinter as tk
from tkinter import scrolledtext, ttk
from parser import parse,print_ast
from lexer import scan

# Function to run code
def run_code():
    code = code_input.get("1.0", tk.END).strip()
    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)

    output_token_file = 'token-output-ui.txt'
    tokens = scan(code, output_token_file)

    if isinstance(tokens, str): # Lexical error occurred during scanning
        output_area.insert(tk.END, f"Lexical Error:\n{tokens}\n")
    else: # Assume successful lexing (tokens is a list)
        try:
            ast = parse(tokens[:-1])
            print_ast(ast)
            output_area.insert(tk.END, "\nParsing Successfull..syntax is correct!\n")
            # Optional: output_area.insert(tk.END, "\nAbstract Syntax Tree:\n")
            # Optional: output_area.insert(tk.END, str(ast))
        except SyntaxError as e:
            # print("SyntaxError caught in UI:", e) # Keep for debugging
            output_area.insert(tk.END, f"\nParsing Error: {e}\n")
        except Exception as e:
            print("Unexpected error during parsing:", e) # Catch any other parsing issues
            output_area.insert(tk.END, f"\nAn unexpected error occurred during parsing: {e}\n")

    output_area.config(state=tk.DISABLED)

# Function to open manual
def open_manual():
    manual_text.config(state=tk.NORMAL)
    manual_text.delete("1.0", tk.END)
    manual_text.insert(tk.END, "Welcome to the Compiler Manual!\n\nUse 'let' for variable declaration, 'convert' for unit conversion.\n"
    "\nSample code for  testing\n\n"
    "let distance = 10miles;\nconvert (5m + 6km) to miles;\nprint distance;\nlet dis_in_km = miles_to_km(100);\nlet speed = calculate_speed(100miles, 2hours);\nprint speed;")
    manual_text.config(state=tk.DISABLED)

# Main Window
root = tk.Tk()
root.title("Custom Compiler UI")
root.geometry("700x500")

# Create Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Styling
style = ttk.Style()
style.configure("TFrame", background="lightblue")
style.configure("TNotebook.Tab", padding=(20, 7), font=("Times New Roman", 11, "bold"))
style.configure("TButton", font=("Times New Roman", 13), padding=(10, 5), relief=tk.RAISED)

# Code Tab with Horizontal Split
tab_code = ttk.Frame(notebook)
notebook.add(tab_code, text="Code")

# Split the code tab into two horizontal regions
code_frame = tk.PanedWindow(tab_code, orient=tk.VERTICAL)
code_frame.pack(fill=tk.BOTH, expand=True)

# Create two sub-frames
input_frame = tk.Frame(code_frame)
output_frame = tk.Frame(code_frame)

code_frame.add(input_frame, stretch="always")
code_frame.add(output_frame, stretch="always")

# Code Input
code_input = scrolledtext.ScrolledText(input_frame, width=80, height=10)
code_input.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
code_input.insert(tk.END, "# Write your code here...")

# Run Button
run_button = tk.Button(input_frame, text="Compile Code", command=run_code)
run_button.pack(pady=5)

# Output Area
output_area = scrolledtext.ScrolledText(output_frame, width=80, height=10, state=tk.NORMAL)
output_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
output_area.insert(tk.END, "# Output appears here...")
output_area.config(state=tk.DISABLED)

# Manual Tab
tab_manual = ttk.Frame(notebook)
notebook.add(tab_manual, text="Manual")

manual_text = scrolledtext.ScrolledText(tab_manual, width=60, height=20, state=tk.DISABLED)
manual_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
open_manual()

# Start GUI Loop
root.mainloop()
