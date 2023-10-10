import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.fernet import Fernet
from tcp_by_size import send_with_size,recv_by_size

def main():
    server_address = ('localhost', 33445)  # Update with the server's address
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    