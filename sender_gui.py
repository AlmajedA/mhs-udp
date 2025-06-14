import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from sender import Sender

class SenderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Message Sender")
        self.geometry("600x450")
        self.configure(bg="#2c3e50")
        self.sender = Sender()
        self.setup_styles()
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="#2c3e50")
        self.style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Arial", 11))
        self.style.configure("TButton", font=("Arial", 10), padding=6)
        self.style.map("TButton", 
                      background=[("active", "#3498db"), ("pressed", "#2980b9")],
                      foreground=[("active", "white"), ("pressed", "white")])
        
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(header_frame, text="MESSAGE SENDER", font=("Arial", 14, "bold")).pack()
        ttk.Label(header_frame, text="Send messages to all receivers via forwarder").pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Status: Ready to send")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")
        
        # Main content
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Message entry
        ttk.Label(main_frame, text="Enter Message:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.message_entry = ttk.Entry(main_frame, width=50)
        self.message_entry.grid(row=1, column=0, padx=(0, 10), sticky="we")
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=1, column=1, sticky="w")
        
        send_btn = ttk.Button(btn_frame, text="Send", command=self.send_message)
        send_btn.pack(side="left", padx=(0, 5))
        
        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_entry)
        clear_btn.pack(side="left")
        
        # Conversation history
        ttk.Label(main_frame, text="Message History:").grid(row=2, column=0, sticky="w", pady=(10, 5))
        self.history_text = scrolledtext.ScrolledText(
            main_frame, 
            width=60, 
            height=12, 
            wrap="word",
            bg="#34495e",
            fg="#ecf0f1",
            insertbackground="white",
            font=("Arial", 10)
        )
        self.history_text.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.history_text.config(state="disabled")
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Set focus to entry
        self.message_entry.focus_set()

    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
            
        # Add to history
        self.update_history(f"You: {message}", "sent")
        
        # Send via network
        result = self.sender.send(message)
        if result is not True:
            self.status_var.set(f"Status: {result}")
            self.update_history(f"Failed to send: {message}", "error")
        
        self.clear_entry()

    def clear_entry(self):
        self.message_entry.delete(0, "end")

    def update_history(self, message, tag):
        self.history_text.config(state="normal")
        self.history_text.insert("end", message + "\n", tag)
        self.history_text.config(state="disabled")
        self.history_text.see("end")
        
    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to close the sender?"):
            self.sender.close()
            self.destroy()

if __name__ == "__main__":
    app = SenderApp()
    app.mainloop()