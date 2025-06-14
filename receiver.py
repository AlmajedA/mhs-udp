import socket
import threading
import os

class Receiver:
    def __init__(self, message_callback):
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 9001
        self.address = (self.ip, self.port)
        self.receiver_socket.bind(self.address)
        self.receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_message = b'pfg_ip_broadcast_rec'
        
        # Get broadcast address from environment variable
        broadcast_target = os.environ.get('FORWARDER_BROADCAST', 'auto')
        if broadcast_target == 'auto':
            network_part = '.'.join(self.ip.split('.')[:3])
            self.forwarder_broadcast_address = (f"{network_part}.255", 9000)
        else:
            self.forwarder_broadcast_address = (broadcast_target, 9000)
            
        self.message_callback = message_callback
        self.running = True

    def register(self):
        self.receiver_socket.sendto(self.broadcast_message, self.forwarder_broadcast_address)

    def start_receiving(self):
        self.register()
        self.receive_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.receive_thread.start()

    def receive_loop(self):
        while self.running:
            try:
                payload, forwarder_address = self.receiver_socket.recvfrom(1024)
                message = payload.decode()
                self.message_callback(f"{forwarder_address}: {message}")
            except OSError as e:
                if self.running:
                    self.message_callback(f"Error: {str(e)}")
                break

    def stop(self):
        self.running = False
        # Unblock socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as temp_socket:
            temp_socket.sendto(b"", ("127.0.0.1", self.port))
        if self.receive_thread:
            self.receive_thread.join(timeout=1.0)
        self.receiver_socket.close()