import socket
import threading
import struct
import os

class Receiver:
    def __init__(self, message_callback):
        self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.ip = ''
        self.port = 9001
        self.address = (self.ip, self.port)
        self.receiver_socket.bind(self.address)

        # Join group
        multicast_group = '224.1.1.1'
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        try:
            self.receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except socket.error as e:
            print(f"Multicast join error: {e}")        

        self.running = True

        # For GUI
        self.message_callback = message_callback


    def start_receiving(self):
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
        self.receiver_socket.close()