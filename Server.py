import socket
import hashlib
from SQLORM import User,WR_ORM
import tcp_by_size
Worm = WR_ORM()


def Hash_Function(ToHash: str):
    """Returns a hashed value from a string"""
    hash_object = hashlib.sha256()
    hash_object.update(ToHash.encode('utf-8'))
    return hash_object.hexdigest()


def Register(User_Name,Password):
    """returns true if managed to register"""
    name = Worm.get_user(User_Name)
    if name != False:
        return False
    Worm.add_user(User(User_Name,Hash_Function(Password)))
    return True

def Login(User_Name,Password):
    """returns true if managed to Login"""
    hash = Worm.get_password(User_Name)
    if type(hash) == str:
        if hash == Hash_Function(Password):
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
    
DebugLoop()