import socket
import hashlib
from SQLORM import User,WR_ORM
from tcp_by_size import recv_by_size,send_with_size
from threading import Thread
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.fernet import Fernet
import random
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
Worm = WR_ORM() #initializing the SQL class
exit_all = False
server_private_key = parameters.generate_private_key()
server_public_key = server_private_key.public_key()
Keys = dict()
Rstrings = dict()
Encrypted = dict()

def handl_client(sock : socket, tid):
    global exit_all

    print("New Client num " + str(tid))

    while not exit_all:
        try:
            
            if(Encrypted[tid]):
                AES(tid,recv_by_size(sock),True).decode()
            else:
                data = recv_by_size(sock).decode()
            print("got _>       ", data)
            if data == "":
                print("Error: Seens Client DC")
                break

            print(data)
            to_send = do_action(data,tid)

            send_with_size(sock, to_send.encode())
            if "KILL" in to_send:
                sock.close()
                Keys.pop(tid)
                Encrypted.pop(tid)
                

        except socket.error as  err:
            if err.errno == 10054:
                # 'Connection reset by peer'
                print("Error %d Client is Gone. %s reset by peer." % (err.errno, str(sock)))
                break
            else:
                print("%d General Sock Error Client %s disconnected" % (err.errno, str(sock)))
                break

        except Exception as err:
            print("General Error:", err)
            break
    sock.close()
    
def AES(tid,msg, decrypt_mode = False):
    """gets bytes and encrypts them"""
    if not decrypt_mode:
        return Keys[tid].encrypt(msg)
    return Keys[tid].decrypt(msg)

def do_action(data,tid):
    """
    check what client ask and fill to send with the answer
    """
    
    to_send = "Not Set Yet"
    action = data[:4] #gets the first 4 letters/action
    data = data[5:]
    fields = data.split('~')
    if action == "INIT":
        Rstr = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(10))
        to_send = "INIT~%s~%s" % (server_public_key,Rstr)
        Rstrings[tid] = Rstr
        shared_secret = server_private_key.exchange(data[0]) #making the DH key
        Keys[tid] = Fernet(shared_secret) #making the AES key
    elif action == "CHECK":
        if AES(tid,data[0],True) == Rstr:
            to_send = "WAIT~"
            Rstrings.pop(tid)
            Encrypted[tid] = True
        else:
            to_send = "KILL~"
        
        
    print("did action")
    return to_send.upper

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
   
   
def main():
    global exit_all

    exit_all = False

    s = socket.socket()

    s.bind(("0.0.0.0", 33445))

    s.listen(4)
    print("after listen")

    threads = []
    i = 1
    while True:
        cli_s, addr = s.accept()
        Encrypted[i] = False
        t = Thread(target=handl_client, args=(cli_s, i ))
        t.start()
        i += 1
        threads.append(t);

    exit_all = True
    for t in threads:
        t.join()
    manager.join()

    s.close()


main() 
#DebugLoop()

