import socket
import hashlib
from SQLORM import User,WR_ORM
from tcp_by_size import recv_by_size,send_with_size,AES_recv_by_size,AES_send_with_size
from threading import Thread
from cryptography.fernet import Fernet
import pickle
import DH
Worm = WR_ORM() #initializing the SQL class
exit_all = False
Clients = dict()
thread_count = 1

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
                    print("Error: Seens Client DC")
                    break


                to_send = do_action(data,tid)
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
            print("General Error:", err)
            break
    sock.close()
    


def do_action(data,tid):
    """
    check what client ask and fill to send with the answer
    """
    to_send = "Not Set Yet"
    action = data[:4] #gets the first 4 letters/action
    data = data[5:]
    data = data.split('~')
    if Clients[tid].encrypted == False:
        if action == "INIT":
            Clients[tid].get_AES_key(int(data[0]))
            to_send = "INIT~" + str(Clients[tid].DH_server_public_key)
            Clients[tid].encrypted = True
    elif action == "SYNC":
        to_send = "SNAK"
    elif action == "FACK":
        print("Secure connection has been established!")
        to_send = "KILL~"
    else:
        to_send = "KILL~"
        
        
    return to_send

def Hash_Function(ToHash: str):
    """Returns a hashed value from a string"""
    hash_object = hashlib.sha256()
    hash_object.update(ToHash.encode('utf-8'))
    return hash_object.hexdigest()


def Register(User_Name,Password):
    """returns true if managed to register recived an already hashed password"""
    name = Worm.get_user(User_Name)
    if name != False:
        return False
    Worm.add_user(User(User_Name,Password))
    return True

def Login(User_Name,Password):
    """returns true if managed to Login recived an already hashed password"""
    hash = Worm.get_password(User_Name)
    if type(hash) == str:
        if hash == Password:
            return True
    else:
        return False
        
def Delete(User_Name,Password):
    """returns true if managed to Delete"""
    hash = Worm.get_password(User_Name)
    if type(hash) == str:
        if hash != Hash_Function(Password):
            return False
    else:
        return False
    Worm.remove_user(User_Name)
    return True
    
def DebugLoop():
    while(True):
        fun = input("what func do you want? Log,Reg,Del")    
        if fun == "Reg":
            print(Register(input("what username would you like"),input("what password would you like")))
        elif fun == "Log": 
            print(Login(input("what username would you like"),input("what password would you like")))
        elif fun == "Del":
            print(Delete(input("what username would you like"),input("what password would you like")))
        elif fun == "Quit":
            break
   
class Client():
    def __init__(self):
        """sets AES_key to false and makes DH_server_public/private_key"""
        self.AES_key = False 
        self.encrypted = False
        self.DH_server_private_key = DH.get_private_key()
        self.DH_server_public_key = DH.get_public_key(self.DH_server_private_key)

    
    def get_AES_key(self,client_public_key : int):
        """returns and sets the AES_key from the DH private and public keys"""
        self.AES_key = Fernet(DH.get_shared_key(client_public_key,self.DH_server_private_key))
        return self.AES_key
   

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

