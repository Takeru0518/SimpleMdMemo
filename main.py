
import tkinter as tk
from tkinter import scrolledtext
import markdown
import os

class MemoWindow(tk.Toplevel):
    def __init__(self, master=None, file_path=None):
        super().__init__(master)
        self.file_path = file_path
        self.title(os.path.basename(self.file_path) if self.file_path else "New Memo")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width // 4}x{screen_height // 4}")

        self.html_view = tk.Text(self, wrap=tk.WORD)
        self.html_view.pack(fill=tk.BOTH, expand=True)

        self.md_editor = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.md_editor.pack(fill=tk.BOTH, expand=True)
        self.md_editor.pack_forget()

        self.edit_button = tk.Button(self, text="編集", command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.RIGHT)

        if self.file_path:
            self.load_file()

    def load_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            self.md_editor.delete('1.0', tk.END)
            self.md_editor.insert('1.0', md_content)
            self.render_html()

    def render_html(self):
        md_content = self.md_editor.get('1.0', tk.END)
        html_content = markdown.markdown(md_content)
        # This is a simplified way to display HTML in a Text widget.
        # For full HTML rendering, a more complex widget would be needed.
        self.html_view.config(state=tk.NORMAL)
        self.html_view.delete('1.0', tk.END)
        self.html_view.insert('1.0', html_content)
        self.html_view.config(state=tk.DISABLED)

    def toggle_edit_mode(self):
        if self.md_editor.winfo_ismapped():
            # Save and switch to HTML view
            self.save_file()
            self.render_html()
            self.md_editor.pack_forget()
            self.html_view.pack(fill=tk.BOTH, expand=True)
            self.edit_button.config(text="編集")
        else:
            # Switch to Markdown editor
            self.html_view.pack_forget()
            self.md_editor.pack(fill=tk.BOTH, expand=True)
            self.edit_button.config(text="保存")

    def save_file(self):
        if not self.file_path:
            # Ask for a new file name
            # For simplicity, we'll auto-name it for now.
            i = 0
            while True:
                new_path = os.path.join("notes", f"memo_{i}.md")
                if not os.path.exists(new_path):
                    self.file_path = new_path
                    break
                i += 1
            self.title(os.path.basename(self.file_path))

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(self.md_editor.get('1.0', tk.END))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SimpleNote")
        self.withdraw() # Hide the root window

        self.new_memo_button = tk.Button(self, text="新しいメモ", command=self.create_new_memo)
        self.new_memo_button.pack(pady=10)

        self.load_notes()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_notes(self):
        if not os.path.exists("notes"):
            os.makedirs("notes")

        files = [f for f in os.listdir("notes") if f.endswith(".md")]
        for i, file_name in enumerate(files):
            file_path = os.path.join("notes", file_name)
            memo = MemoWindow(self, file_path=file_path)
            memo.geometry(f"+{i*50}+{i*50}") # Cascade windows

    def create_new_memo(self):
        MemoWindow(self)

    def on_closing(self):
        for widget in self.winfo_children():
            if isinstance(widget, MemoWindow):
                widget.save_file()
        self.destroy()

if __name__ == "__main__":
    app = App()
    # A simple control window to create new notes and close the app
    control_window = tk.Toplevel(app)
    control_window.title("Control")
    new_button = tk.Button(control_window, text="新しいメモ", command=app.create_new_memo)
    new_button.pack(pady=20, padx=50)
    close_button = tk.Button(control_window, text="終了", command=app.on_closing)
    close_button.pack(pady=10)

    app.mainloop()
