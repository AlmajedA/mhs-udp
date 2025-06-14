import socket
import os

class Sender:
    def __init__(self):
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Get forwarder address from environment variable
        forwarder_host = os.environ.get('FORWARDER_HOST', '0.0.0.0')
        self.forwarder_address = (forwarder_host, 9000)
    
    def send(self, message):
        try:
            payload = message.encode()
            self.sender_socket.sendto(payload, self.forwarder_address)
            return True
        except Exception as e:
            return f"Error: {str(e)}"
    
    def close(self):
        self.sender_socket.close()