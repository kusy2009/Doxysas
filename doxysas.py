import os
import re
import sys
import json
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import requests
from datetime import datetime

class DoxySASApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DoxySAS - Local Version")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        self.api_key = os.environ.get("OPENROUTER_API_KEY", "")
        self.generated_files = []
        self.current_file_index = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="DoxySAS", font=("Helvetica", 24, "bold")).pack(anchor="w")
        ttk.Label(title_frame, text="Generate Doxygen-style documentation for your SAS macros", 
                 font=("Helvetica", 12)).pack(anchor="w")
        
        # Split view
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (Input)
        left_frame = ttk.Frame(paned_window, padding=5)
        paned_window.add(left_frame, weight=1)
        
        # File upload button
        upload_frame = ttk.Frame(left_frame)
        upload_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(upload_frame, text="Upload SAS File", command=self.upload_file).pack(fill=tk.X)
        
        # Separator
        separator_frame = ttk.Frame(left_frame)
        separator_frame.pack(fill=tk.X, pady=10)
        
        ttk.Separator(separator_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        ttk.Label(separator_frame, text="Or paste your code").pack()
        
        # Code editor
        ttk.Label(left_frame, text="SAS Code:").pack(anchor="w", pady=(10, 5))
        self.code_editor = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, height=20, 
                                                    font=("Courier", 10))
        self.code_editor.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Generate button
        generate_button = ttk.Button(left_frame, text="Generate Documentation", 
                                    command=self.generate_documentation)
        generate_button.pack(fill=tk.X, pady=10)
        
        # Right panel (Output)
        right_frame = ttk.Frame(paned_window, padding=5)
        paned_window.add(right_frame, weight=1)
        
        # Output header
        output_header_frame = ttk.Frame(right_frame)
        output_header_frame.pack(fill=tk.X, pady=5)
        
        self.output_label = ttk.Label(output_header_frame, text="Generated Documentation", 
                                      font=("Helvetica", 12, "bold"))
        self.output_label.pack(side=tk.LEFT)
        
        # File tabs
        self.tab_frame = ttk.Frame(right_frame)
        self.tab_frame.pack(fill=tk.X, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Copy Header", command=self.copy_header).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Download", command=self.download_file).pack(side=tk.LEFT, padx=5)
        
        # Preview area
        self.preview = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=25, 
                                                font=("Courier", 10))
        self.preview.pack(fill=tk.BOTH, expand=True, pady=5)
        self.preview.config(state=tk.DISABLED)
        
        # API Key setup
        api_frame = ttk.LabelFrame(main_frame, text="OpenRouter API Settings", padding=10)
        api_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(api_frame, text="API Key:").pack(side=tk.LEFT, padx=5)
        self.api_key_var = tk.StringVar(value=self.api_key)
        self.api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=50, show="*")
        self.api_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Button(api_frame, text="Save API Key", command=self.save_api_key).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
    
    def update_tabs(self):
        # Clear existing tabs
        for widget in self.tab_frame.winfo_children():
            widget.destroy()
            
        # Create tabs for each generated file
        for i, file in enumerate(self.generated_files):
            btn = ttk.Button(self.tab_frame, text=file["filename"], 
                            command=lambda idx=i: self.show_file(idx))
            if i == self.current_file_index:
                btn.config(style="Selected.TButton")
            btn.pack(side=tk.LEFT, padx=2)
    
    def show_file(self, index):
        if 0 <= index < len(self.generated_files):
            self.current_file_index = index
            self.update_tabs()
            self.update_preview()
    
    def update_preview(self):
        if not self.generated_files:
            return
            
        file = self.generated_files[self.current_file_index]
        self.preview.config(state=tk.NORMAL)
        self.preview.delete(1.0, tk.END)
        self.preview.insert(tk.END, file["generatedDoc"])
        self.preview.config(state=tk.DISABLED)
    
    def save_api_key(self):
        self.api_key = self.api_key_var.get().strip()
        messagebox.showinfo("API Key", "API Key saved successfully")
    
    def upload_file(self):
        file_paths = filedialog.askopenfilenames(
            title="Select SAS Files",
            filetypes=[("SAS Files", "*.sas"), ("All Files", "*.*")]
        )
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.code_editor.delete(1.0, tk.END)
                    self.code_editor.insert(tk.END, content)
                    self.generate_documentation()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
    
    def extract_macro_name(self, code):
        macro_match = re.search(r'%macro\s+([a-zA-Z_][a-zA-Z0-9_]*)', code, re.IGNORECASE)
        return macro_match.group(1) if macro_match else "untitled"
    
    def find_internal_macros(self, code):
        macro_call_pattern = r'%(?!macro\s+)([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        macros = set(re.findall(macro_call_pattern, code, re.IGNORECASE))
        return list(macros)
    
    def clean_generated_doc(self, doc):
        # Remove code block markers and any explanatory text
        cleaned = re.sub(r'```(?:cpp|sas)?\n?', '', doc)
        cleaned = re.sub(r'```\n?', '', cleaned)
        cleaned = cleaned.strip()
        
        # Split header and code
        header_match = re.search(r'/\*\*([\s\S]*?)\*/', cleaned)
        header = header_match.group(0).strip() if header_match else ""
        
        return {
            "header": header,
            "fullDoc": cleaned
        }
    
    def generate_documentation(self):
        code = self.code_editor.get(1.0, tk.END).strip()
        if not code:
            messagebox.showerror("Error", "Please enter some SAS code first")
            return
            
        if not self.api_key:
            messagebox.showerror("Error", "Please enter your OpenRouter API Key")
            return
            
        self.status_var.set("Generating documentation...")
        self.root.update_idletasks()
        
        try:
            macro_name = self.extract_macro_name(code)
            internal_macros = self.find_internal_macros(code)
            
            macros_section = ""
            if internal_macros:
                macros_section = f"\n<h4>SAS Macros</h4>\n" + "\n".join([f"@li {macro}.sas" for macro in internal_macros]) + "\n"
            
            system_prompt = """You are a documentation expert that generates Doxygen-style documentation for SAS macros.

Follow this exact structure for the documentation header:

/**
@file {Macro_name.sas}
@brief {One-sentence functional description}
@details
{Extended markdown-formatted explanation of purpose, key functionalities, and usage context}

Syntax
@code
%macro_name(param1=, param2=, ...);
@endcode

Usage
@code
%macro_name(param1=value1, param2=value2);
/* Example of how the macro is used */
@endcode

@param [in/out] param1 (default_value if exists) Precise description with data type/format constraints
@param [in/out] param2 (default_value if exists) Precise description with data type/format constraints
@return {Explanation of return value/output}
@version <1.0>
@author <Your Name>

/* Only include this exact section if internal macros (not functions) are found otherwise don't include this section at all*/
<h4>SAS Macros</h4>
@li {macro1}.sas
@li {macro2}.sas
*/

Important rules:
1. Do not include any sections beyond those specified above
2. Do not add @ before syntax or usage subsections
3. Use @code and @endcode blocks for all code examples
4. Include placeholders in <> for version and author
5. Keep descriptions clear and concise
6. Analyze the macro code to determine if each parameter is [in] or [out] based on its usage
7. Only include default values in parentheses if they are explicitly defined in the macro
8. For the SAS Macros section:
   - Only include it if internal macro calls are found in the code and dont include macro fucntions
   - Use exact HTML tags <h4>SAS Macros</h4>
   - List each macro with @li followed by the macro name and .sas extension
   - Do not use asterisks or hyphens
9. Remove any markdown formatting or explanatory text from the output, I want only header info in output from /** to */ """

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": f"Generate a Doxygen header for this SAS macro:\n\n{code}\n\nInclude this exact macros section if any internal macros are found:\n{macros_section}"
                        }
                    ]
                }
            )
            
            if not response.ok:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
                
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            doc_result = self.clean_generated_doc(content)
            
            # Create file entry
            file_entry = {
                "filename": f"{macro_name}.sas",
                "originalCode": code,
                "generatedDoc": doc_result["fullDoc"],
                "header": doc_result["header"],
                "timestamp": datetime.now().isoformat()
            }
            
            self.generated_files.append(file_entry)
            self.current_file_index = len(self.generated_files) - 1
            self.update_tabs()
            self.update_preview()
            
            self.status_var.set(f"Documentation generated for {macro_name}.sas")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate documentation: {str(e)}")
            self.status_var.set("Ready")
    
    def copy_header(self):
        if not self.generated_files:
            messagebox.showinfo("Info", "No documentation generated yet")
            return
            
        file = self.generated_files[self.current_file_index]
        self.root.clipboard_clear()
        self.root.clipboard_append(file["header"])
        self.status_var.set("Header copied to clipboard")
    
    def download_file(self):
        if not self.generated_files:
            messagebox.showinfo("Info", "No documentation generated yet")
            return
            
        file = self.generated_files[self.current_file_index]
        save_path = filedialog.asksaveasfilename(
            title="Save Documentation",
            defaultextension=".sas",
            initialfile=file["filename"],
            filetypes=[("SAS Files", "*.sas"), ("All Files", "*.*")]
        )
        
        if save_path:
            try:
                with open(save_path, 'w') as f:
                    f.write(file["generatedDoc"])
                self.status_var.set(f"File saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":
    # Set up the theme for a modern look
    root = tk.Tk()
    
    # Try to use a modern theme if available
    try:
        style = ttk.Style()
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
            
        # Custom style for selected tab buttons
        style.configure("Selected.TButton", background="#4a7dfc", foreground="white")
    except Exception:
        pass
    
    app = DoxySASApp(root)
    root.mainloop()