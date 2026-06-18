import tkinter as tk
from tkinter import ttk
import threading
import requests
from pynput import keyboard  # Safe global hotkey reader

class OmniTaskUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OmniTask-OS Prompt")
        self.root.geometry("550x220")
        self.root.configure(bg="#211c38")
        
        title_label = tk.Label(
            root, 
            text="⚡ OmniTask-OS Command Input", 
            font=("Segoe UI", 14, "bold"), 
            bg="#211c38", 
            fg="#ffffff"
        )
        title_label.pack(pady=20)
        
        frame = tk.Frame(root, bg="#211c38")
        frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.entry = tk.Entry(
            frame, 
            font=("Segoe UI", 12), 
            bg="#312b4f", 
            fg="#ffffff", 
            insertbackground="white", 
            bd=0,
            highlightthickness=1,
            highlightbackground="#4a3f78"
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=5)
        
        # Enter key executes
        self.entry.bind("<Return>", lambda event: self.trigger_execution())
        
        self.btn = tk.Button(
            frame, 
            text="Execute", 
            font=("Segoe UI", 11, "bold"), 
            bg="#5e81f4", 
            fg="#ffffff", 
            activebackground="#4a6be2",
            activeforeground="#ffffff",
            bd=0, 
            command=self.trigger_execution,
            cursor="hand2"
        )
        self.btn.pack(side=tk.RIGHT, padx=10, ipady=4, ipadx=10)
        
        self.status_label = tk.Label(
            root, 
            text="💡 Enter to execute | Ctrl+Q (anywhere) to Hide / Show!", 
            font=("Segoe UI", 10, "italic"), 
            bg="#211c38", 
            fg="#a5a1b8"
        )
        self.status_label.pack(pady=15)

        # Visibility states
        self.is_visible = True
        self.entry.focus_force()

        # Start the safe background key listener
        threading.Thread(target=self.start_global_listener, daemon=True).start()

    def start_global_listener(self):
        # Listens for Ctrl + Q globally across Windows without requiring Admin rights
        with keyboard.GlobalHotKeys({'<ctrl>+q': self.toggle_vanish}) as h:
            h.join()

    def toggle_vanish(self):
        if self.is_visible:
            # Hide completely from view
            self.root.after(0, self.root.withdraw)
            self.is_visible = False
        else:
            # Show it back, pop it to front, and refocus text box automatically
            self.root.after(0, self.root.deiconify)
            self.root.after(0, lambda: self.root.attributes("-topmost", True))
            self.root.after(10, lambda: self.root.attributes("-topmost", False))
            self.root.after(20, self.entry.focus_set)
            self.is_visible = True

    def trigger_execution(self):
        user_input = str(self.entry.get()).strip()
        if not user_input:
            return
            
        self.status_label.config(text="🤖 Running command...", fg="#5e81f4")
        self.btn.config(state=tk.DISABLED)
        
        threading.Thread(target=self.worker_thread, args=(user_input,), daemon=True).start()

    def worker_thread(self, cmd_text):
        try:
            requests.post(
                "http://127.0.0.1:8080/execute",
                json={"objective": str(cmd_text)},
                timeout=10
            )
            self.root.after(0, lambda: self.status_label.config(text="✅ Command executed successfully!", fg="#27ae60"))
        except Exception:
            self.root.after(0, lambda: self.status_label.config(text="❌ Failed to connect to server.", fg="#ff5c5c"))
        finally:
            self.root.after(0, lambda: self.entry.delete(0, tk.END))
            self.root.after(0, lambda: self.btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.entry.focus_set())

if __name__ == "__main__":
    root = tk.Tk()
    app = OmniTaskUI(root)
    root.mainloop()