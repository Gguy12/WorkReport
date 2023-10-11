import socket
import hashlib
from SQLORM import User,WR_ORM
from tcp_by_size import recv_by_size,send_with_size,AES_recv_by_size,AES_send_with_size
from threading import Thread
from cryptography.fernet import Fernet
import pickle
import DH
 #initializing the SQL class
exit_all = False
Clients = dict()
thread_count = 1


   
class Client():
    def __init__(self):
        """sets AES_key to false and makes DH_server_public/private_key"""
        self.AES_key = False 
        self.encrypted = False
        self.logged = False
        self.user_name = ""
        self.DH_server_private_key = DH.get_private_key()
        self.DH_server_public_key = DH.get_public_key(self.DH_server_private_key)

    
    def get_AES_key(self,client_public_key : int):
        """returns and sets the AES_key from the DH private and public keys"""
        self.AES_key = Fernet(DH.get_shared_key(client_public_key,self.DH_server_private_key))
        return self.AES_key
    
    


def Hash_Function(ToHash: str):
    """Returns a hashed value from a string"""
    hash_object = hashlib.sha256()
    hash_object.update(ToHash.encode('utf-8'))
    return hash_object.hexdigest()

def is_valid_hash_bytes(hash_bytes : bytes, hash_length=32) -> True:
    """
    Check if the given bytes look like a valid hash.
    Returns:
    - True if the bytes pass all validation checks, False otherwise.
    """
    if len(hash_bytes) != hash_length:
        return False
    try:
        hash_hex = hash_bytes.hex()
    except:
        return False
    valid_chars = set("0123456789abcdef")
    for char in hash_hex:
        if char not in valid_chars:
            return False

    return True

def register(User_Name : str,Password : str) -> bool:
    """returns true if managed to register recived an already hashed password"""
    name = Worm.get_user(User_Name)
    if name != False:
        return False
    
    Worm.add_user(User(User_Name,Password))
    return True

def Login(User_Name : str,Password : str) -> bool:
    """returns true if managed to Login recived an already hashed password"""
    hash = Worm.get_password(User_Name)
    if type(hash) == str:
        if hash == Password:
            return True
    else:
        return False
        
def Delete(User_Name : str,Password : str) -> bool:
    """returns true if managed to Delete"""
    if Password == Worm.get_password(User_Name):
        Worm.remove_user(User_Name)
        return True
    else:
        return False

    

def handl_client(sock : socket, tid):
    global exit_all
    global thread_count
    session = True
    print("New Client num " + str(tid))

    while not exit_all and session:
        try:
            while(session):
                if(Clients[tid].encrypted):
                    data = AES_recv_by_size(sock,Clients[tid].AES_key).decode()
                else:
                    data = recv_by_size(sock).decode()
                if data == "":
                    print(f"Error: Seens Client {tid} DC")
                    break
                try:
                    to_send = do_action(data,Clients[tid],tid)
                except:
                    to_send = "KILL"
                if to_send.startswith("INIT"):
                    send_with_size(sock, to_send.encode())
                else:
                    AES_send_with_size(sock,to_send.encode(),Clients[tid].AES_key)
                if to_send.startswith("KILL"):
                    session = False
                if not session:
                    thread_count -= 1
                    del Clients[tid]
                    print("ending session number :   ", tid)
                
                    

        except socket.error as  err:
            if err.errno == 10054:
                # 'Connection reset by peer'
                print("Error %d Client number %d is Gone. %s reset by peer." % (err.errno,tid, str(sock)))
                thread_count -= 1
                break
            else:
                print("%d General Sock Error Client %d disconnected" % (err.errno, tid))
                break

        except Exception as err:
            print("General Error in client {tid}:", err)
            break
    sock.close()
    


def do_action(data: str,cli : Client,tid : int) -> str:
    """
    check what client ask and fill to send with the answer
    """
    to_send = "Not Set Yet"
    action = data[:4].upper() #gets the first 4 letters/action
    data = data[5:]
    data = data.split('~')
    if cli.encrypted == False:
        if action == "INIT":
            cli.get_AES_key(int(data[0]))
            to_send = "INIT~" + str(cli.DH_server_public_key)
            cli.encrypted = True
    elif not cli.logged:
        if action == "SYNC":
            to_send = "SNAK"
        elif action == "FACK":
            print("Secure connection has been established! with client: ",tid)
            to_send = "ENTR~"
        elif action ==  "REGA":
            registered = register(data[0],data[1])
            if(registered):
                to_send = f"REGS~{data[0]}"
                cli.logged = True
                cli.user_name = data[0]
                print("New registered user :  ",data[0])
            else:
                to_send = "REGF~User name or password not in correct format"
        elif action == "LOGN":
            if(Login(data[0],data[1])):
                to_send = f"REGS~{data[0]}"
                cli.logged = True
                cli.user_name = data[0]
            else:
                to_send = "REGF~User name or password not correct or not in format"
    elif cli.logged:
        if action == "DELT":
            Delete(cli.user_name,data[0])

        
        
    return to_send

Worm = WR_ORM()

def main():
    global exit_all

    exit_all = False
    s = socket.socket()

    s.bind(("0.0.0.0", 33445))

    s.listen(1)
    print("after listen")

    threads = []
    global thread_count
    while True:
        cli_s, addr = s.accept()
        Clients[thread_count] = Client()
        t = Thread(target=handl_client, args=(cli_s, thread_count ))
        t.start()
        thread_count += 1
        threads.append(t);

    exit_all = True
    for t in threads:
        t.join()
    manager.join()

    s.close()


main() 
#DebugLoop()

