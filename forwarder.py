import socket

class Forwarder:
    def __init__(self):
        self.forwarder_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = '0.0.0.0'
        self.forwarder_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.port = 9000
        self.address = (self.ip, self.port)
        self.forwarder_socket.bind(self.address)
        self.receivers_address = []
        self.broadcast_message = 'pfg_ip_broadcast_rec'

    def forward(self):
        print(f"Forwarder running with ip address: {self.ip}, and port: {self.port}")
        while True:
            payload, sender_address = self.forwarder_socket.recvfrom(1024)
            message = payload.decode()

            if message == self.broadcast_message:
                print(f"Registered receiver at: {sender_address}")
                self.receivers_address.append(sender_address) 
                continue
            
            for rec_addr in self.receivers_address:
                self.forwarder_socket.sendto(payload, rec_addr)
                
if __name__ == "__main__":
    forwarder = Forwarder()
    forwarder.forward()