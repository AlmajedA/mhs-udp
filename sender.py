import socket
import os

class Sender:
    def __init__(self):
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.forwarder_address = ('10.65.121.135', 9000)
    
    def send(self, message):
        try:
            print(message)
            payload = message.encode()
            self.sender_socket.sendto(payload, self.forwarder_address)
            return True
        except Exception as e:
            print(e)
            return f"Error: {str(e)}"
    
    def close(self):
        self.sender_socket.close()