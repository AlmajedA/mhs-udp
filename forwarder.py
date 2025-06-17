import socket
import struct

class Forwarder:
    def __init__(self):
        self.forwarder_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = '10.65.121.135'

        ttl = struct.pack('b', 1) # 1 for local network
        self.forwarder_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        self.port = 9000
        self.address = (self.ip, self.port)
        self.forwarder_socket.bind(self.address)

        # Set up group
        self.group_address = ('224.1.1.1', 9001)

    def forward(self):
        print(f"Forwarder running with ip address: {self.ip}, and port: {self.port}")
        while True:
            payload, sender_address = self.forwarder_socket.recvfrom(1024)
            
            self.forwarder_socket.sendto(payload, self.group_address)
                
if __name__ == "__main__":
    forwarder = Forwarder()
    forwarder.forward()