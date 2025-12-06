import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import pathlib
import platform
from datetime import datetime

try:
    import pyperclip
except ImportError:
    pyperclip = None # Gracefully handle if not installed, though it's highly recommended

class CodeToMarkdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code to Markdown Converter")
        self.root.geometry("700x600") # Adjusted size for more content

        self.selected_folders = []
        self.selected_files = []

        # --- Default Output ---
        timestamp = datetime.now().strftime("%Y-%m-%d %H_%M")
        default_filename = f"{timestamp} codebase_file.md"
        
        if platform.system() == "Windows":
            self.output_destination_path = pathlib.Path.home() / "Desktop" / default_filename
        elif platform.system() == "Linux":
            self.output_destination_path = pathlib.Path.home() / "Desktop" / default_filename
            # Check if ~/Desktop exists, otherwise use ~/
            if not (pathlib.Path.home() / "Desktop").exists():
                self.output_destination_path = pathlib.Path.home() / default_filename
        elif platform.system() == "Darwin": # macOS
            self.output_destination_path = pathlib.Path.home() / "Desktop" / default_filename
        else: # Fallback for other OS
            self.output_destination_path = pathlib.Path.cwd() / default_filename

        self.extension_map = {
            ".py": "python",
            ".kt": "kotlin",
            ".java": "java",
            ".js": "javascript",
            ".ts": "typescript",
            ".html": "html",
            ".xml": "xml",
            ".css": "css",
            ".scss": "scss",
            ".sh": "bash",
            ".ps1": "powershell",
            ".rb": "ruby",
            ".go": "go",
            ".c": "c",
            ".h": "c",      # C header files
            ".hpp": "cpp",  # C++ header files
            ".cc": "cpp",   # C++ source files
            ".cpp": "cpp",
            ".cs": "csharp",
            ".css":"css",
            ".swift": "swift",
            ".php": "php",
            ".md": "markdown", # Can be useful for including existing markdown
            ".txt": "text",    # Generic text
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".sql": "sql",
            ".r": "r",
            ".pl": "perl",
            ".xsd": "xml"
        }

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Folder Selection ---
        folder_frame = tk.LabelFrame(main_frame, text="Folders", padx=5, pady=5)
        folder_frame.pack(fill=tk.X, pady=5)

        self.add_folder_button = tk.Button(folder_frame, text="Add Folder(s)", command=self.add_folders)
        self.add_folder_button.pack(fill=tk.X)

        self.folder_listbox = tk.Listbox(folder_frame, selectmode=tk.EXTENDED, height=5)
        self.folder_listbox.pack(fill=tk.X, expand=True, pady=(5,0))
        
        self.remove_folder_button = tk.Button(folder_frame, text="Remove Selected Folder(s)", command=self.remove_selected_folders)
        self.remove_folder_button.pack(fill=tk.X, pady=(0,5))

        # --- File Selection ---
        file_frame = tk.LabelFrame(main_frame, text="Files", padx=5, pady=5)
        file_frame.pack(fill=tk.X, pady=5)

        self.add_file_button = tk.Button(file_frame, text="Add File(s)", command=self.add_files)
        self.add_file_button.pack(fill=tk.X)

        self.file_listbox = tk.Listbox(file_frame, selectmode=tk.EXTENDED, height=5)
        self.file_listbox.pack(fill=tk.X, expand=True, pady=(5,0))
        
        self.remove_file_button = tk.Button(file_frame, text="Remove Selected File(s)", command=self.remove_selected_files)
        self.remove_file_button.pack(fill=tk.X, pady=(0,5))

        # --- Output Destination ---
        output_frame = tk.LabelFrame(main_frame, text="Output Markdown File", padx=5, pady=5)
        output_frame.pack(fill=tk.X, pady=5)

        self.set_output_button = tk.Button(output_frame, text="Set Output Destination", command=self.set_output_destination)
        self.set_output_button.pack(fill=tk.X)

        self.output_path_label = tk.Label(output_frame, text=f"Output to: {self.output_destination_path}", wraplength=650, justify=tk.LEFT)
        self.output_path_label.pack(fill=tk.X, pady=(5,0))

        # --- Generate Button ---
        self.generate_button = tk.Button(main_frame, text="Generate Markdown & Copy to Clipboard", command=self.generate_markdown, bg="lightblue", font=("Arial", 12, "bold"))
        self.generate_button.pack(fill=tk.X, pady=20)

    def add_folders(self):
        folders = filedialog.askdirectory(mustexist=True, title="Select Folder(s)")
        if folders: # askdirectory returns a single string, not a tuple for multiple
            if folders not in self.selected_folders:
                self.selected_folders.append(folders)
                self.folder_listbox.insert(tk.END, folders)
            else:
                messagebox.showinfo("Info", f"Folder '{folders}' already added.")
        self.update_listboxes()

    def remove_selected_folders(self):
        selected_indices = self.folder_listbox.curselection()
        for i in reversed(selected_indices): # Remove from back to avoid index shifting
            folder_path = self.folder_listbox.get(i)
            self.folder_listbox.delete(i)
            if folder_path in self.selected_folders:
                self.selected_folders.remove(folder_path)
        self.update_listboxes()

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select File(s)")
        if files:
            for f_path in files:
                if f_path not in self.selected_files:
                    self.selected_files.append(f_path)
                else:
                    messagebox.showinfo("Info", f"File '{os.path.basename(f_path)}' already added.")
        self.update_listboxes()

    def remove_selected_files(self):
        selected_indices = self.file_listbox.curselection()
        for i in reversed(selected_indices): # Remove from back to avoid index shifting
            file_path = self.file_listbox.get(i)
            self.file_listbox.delete(i)
            if file_path in self.selected_files:
                self.selected_files.remove(file_path)
        self.update_listboxes()

    def update_listboxes(self):
        self.folder_listbox.delete(0, tk.END)
        for folder in self.selected_folders:
            self.folder_listbox.insert(tk.END, folder)

        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, file_path)

    def set_output_destination(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".md",
            initialfile="extracted_code.md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            title="Save Markdown File As"
        )
        if filepath:
            self.output_destination_path = pathlib.Path(filepath)
            self.output_path_label.config(text=f"Output to: {self.output_destination_path}")

    def get_relative_path(self, file_path, base_path):
        """Calculates relative path robustly."""
        try:
            # Ensure both are absolute paths for reliable relative path calculation
            abs_file_path = pathlib.Path(file_path).resolve()
            abs_base_path = pathlib.Path(base_path).resolve()
            
            # If base_path is a file, use its parent directory as the base
            if abs_base_path.is_file():
                abs_base_path = abs_base_path.parent

            # If the file is not under the base path, default to its name
            if not str(abs_file_path).startswith(str(abs_base_path)):
                 return abs_file_path.name # Fallback to just the filename
            
            return os.path.relpath(abs_file_path, abs_base_path)
        except ValueError:
            # This can happen if paths are on different drives on Windows
            return pathlib.Path(file_path).name # Fallback to just the filename

    def generate_markdown(self):
        if not self.selected_folders and not self.selected_files:
            messagebox.showwarning("No Input", "Please add at least one folder or file.")
            return

        all_files_to_process = set() # Use a set to avoid duplicates
        
        # Add directly selected files
        for f_path_str in self.selected_files:
            f_path = pathlib.Path(f_path_str)
            if f_path.is_file():
                 # For directly added files, the "base" is their parent directory
                all_files_to_process.add((str(f_path), str(f_path.parent)))


        # Add files from selected folders
        for folder_path_str in self.selected_folders:
            folder_path = pathlib.Path(folder_path_str)
            if folder_path.is_dir():
                for item in folder_path.rglob('*'): # rglob for recursive
                    if item.is_file():
                        all_files_to_process.add((str(item), str(folder_path))) # File path and its base for rel path

        if not all_files_to_process:
            messagebox.showinfo("No Code Files", "No processable files found in the selected locations or with supported extensions.")
            return

        markdown_content = ["## Code:\n\n"]

        processed_files_count = 0
        # Sort files for consistent output, e.g., by full path
        sorted_files = sorted(list(all_files_to_process), key=lambda x: x[0])

        for file_full_path_str, base_path_str in sorted_files:
            file_path = pathlib.Path(file_full_path_str)
            base_path = pathlib.Path(base_path_str)
            
            file_extension = file_path.suffix.lower()
            language = self.extension_map.get(file_extension)

            if language:
                try:
                    relative_path = self.get_relative_path(file_path, base_path)
                    # Normalize path separators for display
                    display_relative_path = str(pathlib.PurePath(relative_path))

                    markdown_content.append(f"### File: `{display_relative_path}`\n")
                    
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        code = f.read()
                    
                    markdown_content.append(f"```{language}\n{code.strip()}\n```\n\n")
                    processed_files_count += 1
                except Exception as e:
                    markdown_content.append(f"### File: `{display_relative_path}`\n")
                    markdown_content.append(f"```\nError reading file: {e}\n```\n\n")
            # else: # Optionally log skipped files
            #     print(f"Skipping file (unsupported extension): {file_path}")


        if not processed_files_count:
            messagebox.showinfo("No Code Files", "No files with supported extensions were found to process.")
            return

        final_markdown = "".join(markdown_content).strip()

        # Save to file
        try:
            self.output_destination_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
            with open(self.output_destination_path, 'w', encoding='utf-8') as f:
                f.write(final_markdown)
            save_success = True
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save markdown to {self.output_destination_path}:\n{e}")
            save_success = False

        # Copy to clipboard
        clipboard_success = False
        if pyperclip:
            try:
                pyperclip.copy(final_markdown)
                clipboard_success = True
            except Exception as e: # Catch pyperclip specific errors if any
                 messagebox.showwarning("Clipboard Error", f"Could not copy to clipboard: {e}\n(pyperclip might not be configured correctly for your system, e.g., on Linux, xclip or xsel might be needed).")
        else:
            messagebox.showwarning("Clipboard Warning", "pyperclip module not found. Cannot copy to clipboard. Please install it: pip install pyperclip")

        # --- Feedback ---
        if save_success and clipboard_success:
            messagebox.showinfo("Success", f"Markdown generated, saved to:\n{self.output_destination_path}\nand copied to clipboard!")
        elif save_success:
            messagebox.showinfo("Partial Success", f"Markdown generated and saved to:\n{self.output_destination_path}\nClipboard copy failed.")
        elif clipboard_success:
             messagebox.showinfo("Partial Success", "Markdown generated and copied to clipboard!\nFile saving failed.")
        else:
            # Error messages for save/clipboard would have already been shown
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeToMarkdownApp(root)
    root.mainloop()