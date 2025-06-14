import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from receiver import Receiver

class ReceiverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Message Receiver")
        self.geometry("600x450")
        self.configure(bg="#2c3e50")
        self.receiver = None
        self.setup_styles()
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.start_receiver()

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
        
        ttk.Label(header_frame, text="MESSAGE RECEIVER", font=("Arial", 14, "bold")).pack()
        ttk.Label(header_frame, text="Receiving messages from forwarder").pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Status: Starting receiver...")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")
        
        # Main content
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Conversation display
        ttk.Label(main_frame, text="Received Messages:").pack(anchor="w", pady=(0, 5))
        self.message_text = scrolledtext.ScrolledText(
            main_frame, 
            width=60, 
            height=20, 
            wrap="word",
            bg="#34495e",
            fg="#ecf0f1",
            insertbackground="white",
            font=("Arial", 10)
        )
        self.message_text.pack(fill="both", expand=True)
        self.message_text.config(state="disabled")
        
        # Button frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10, fill="x")
        
        clear_btn = ttk.Button(btn_frame, text="Clear Messages", command=self.clear_messages)
        clear_btn.pack(side="left", padx=5)
        
        self.toggle_btn = ttk.Button(btn_frame, text="Stop Receiver", command=self.toggle_receiver)
        self.toggle_btn.pack(side="right", padx=5)
        
        # Configure tag colors
        self.message_text.tag_config("received", foreground="#2ecc71")
        self.message_text.tag_config("status", foreground="#3498db")
        self.message_text.tag_config("error", foreground="#e74c3c")

    def start_receiver(self):
        if self.receiver and self.receiver.running:
            return
            
        self.receiver = Receiver(self.handle_message)
        self.receiver.start_receiving()
        self.status_var.set(f"Status: Receiving on {self.receiver.ip}:{self.receiver.port}")
        self.toggle_btn.config(text="Stop Receiver")
        self.update_message("Receiver started. Waiting for messages...", "status")

    def stop_receiver(self):
        if self.receiver:
            self.receiver.stop()
        self.status_var.set("Status: Receiver stopped")
        self.toggle_btn.config(text="Start Receiver")
        self.update_message("Receiver stopped", "status")

    def toggle_receiver(self):
        if self.receiver and self.receiver.running:
            self.stop_receiver()
        else:
            self.start_receiver()

    def handle_message(self, message):
        self.update_message(message, "received")

    def update_message(self, message, tag="received"):
        self.message_text.config(state="normal")
        self.message_text.insert("end", message + "\n", tag)
        self.message_text.config(state="disabled")
        self.message_text.see("end")

    def clear_messages(self):
        self.message_text.config(state="normal")
        self.message_text.delete(1.0, "end")
        self.message_text.config(state="disabled")
        self.update_message("Message history cleared", "status")

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to close the receiver?"):
            self.stop_receiver()
            self.destroy()

if __name__ == "__main__":
    app = ReceiverApp()
    app.mainloop()