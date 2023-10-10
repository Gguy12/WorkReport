import socket
from cryptography.fernet import Fernet
from tcp_by_size import send_with_size,recv_by_size,AES_recv_by_size,AES_send_with_size
import pickle
import DH


def adjust_bytes_to_32_bytes(data_bytes):
    # Ensure the input is a bytes object
    if not isinstance(data_bytes, bytes):
        raise TypeError("Input must be a bytes object")

    if len(data_bytes) > 32:
        # Shorten the input bytes to 32 bytes
        return data_bytes[:32]
    elif len(data_bytes) < 32:
        # Expand the input bytes to 32 bytes by padding with zero bytes
        return data_bytes + b'\x00' * (32 - len(data_bytes))
    else:
        # The input is already 32 bytes, no need to change it
        return data_bytes
    

def main():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 33445))
    print("connected to:    ", '0.0.0.0', 33445)
    client_private_key = DH.get_private_key()
    client_public_key = DH.get_public_key(client_private_key)
    
    to_send = "INIT~" + str(client_public_key)
    send_with_size(client_socket, to_send.encode())
    print("sent init ->     %s" % (to_send))
    recv_data = recv_by_size(client_socket).decode()
    print("got ->       ", recv_data)
    recv_parts = recv_data.split("~")    
    
    key = Fernet(DH.get_shared_key(int(recv_parts[1]),client_private_key))
    
    print("Starting three way handshake sending:    SYNC")
    AES_send_with_size(client_socket,"SYNC~".encode(),key)
    data = AES_recv_by_size(client_socket,key)
    print(f"server sent:    {data}")
    if data.decode() != "SNAK":
        print("Three way handshake incoplete, ending session now")
        AES_send_with_size("QUIT~")
        quit()
    else:
        print("sending final ACK to server")
        AES_send_with_size(client_socket,"FACK".encode(),key)
        print("Final ack has been recieved!     Three Way Handshake complete, connenction is secure and has been established")
    print("server sent:     ",AES_recv_by_size(client_socket,key))
    
    
    
main()