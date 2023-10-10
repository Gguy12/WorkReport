# WorkReport
The goal of this project is to make an app to report work hours, requiring verification and location verification 


#Protocol:

4 letter action like ACKE SYNC etc followed by ~ as barriers for other data

INIT~PublicKey - Initializing the encryption using DH sending public key to client (cliend side)

INIT~PublicKey~RandomSTR - Initializing the encryption using DH sending public key to client (server side)

CHECK~RandomSTR - sending a random string encrypted to see if the encryption was properly set up (client side)


WAIT~ - server telling client that everything works and its waiting for input (server side)

KILL~ErrorMsg - server closing client due to a problem (server side)





