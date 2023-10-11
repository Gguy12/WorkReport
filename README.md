# WorkReport
The goal of this project is to make an app to report work hours, requiring verification and location verification 


#Protocol:

4 letter action like ACKE SYNC etc followed by ~ as barriers for other data
S2C - Server -> Client
C2S - Client -> Server

KILL~ErrorMsg - server closing client due to a problem (S2C)

INIT~PublicKey - Initializing the encryption using DH sending public key to client (C2S, S2C)


SYNC~ - Start 3 way hand shake to see if encryption was set up properly (C2S)

SNAK~  Syn Ack continue 3 way hand shake (S2C)

FACK~ Final Ack three way handshake is done (C2S)

ENTR~ Server requesting for user to enter a login command (S2C)

REGA~USERNAME~HASHED-PASSWORD - Register attempt from user, one of the two commands a user can do not logged in (C2S)

REGS~USERNAME - Registered user succssesfully (S2C)

REGF~Error Message -  Failed to register user because of error (S2C)

LOGN~USERNAME~HASHED PASSWORD - Login attempt from user, second of the two commands a user can do not logged in (C2S)

LOGS~USERNAME - user login succssesfully (S2C)

LOGF~Error Message -  Failed to login user because of error (S2C)



