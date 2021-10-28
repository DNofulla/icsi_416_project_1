import socket as sc
from sys import argv 



def main():
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = sc.socket(sc.AF_INET, sc.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind((sc.gethostbyname(sc.gethostname()), int(argv[1])))

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()
    print("[LISTENING] Server is listening.")
    server, addr = server.accept()
    
    """ Server has accepted the connection from the client. """
    print(f"[NEW CONNECTION] {addr} connected.")
    

    flag = True
    while flag == True:
        """ Receiving the filename from the client. """
        user_input = server.recv(1024).decode("utf-8")
        print(user_input)
        
        split_input = user_input.split();
        print(split_input)
        
        if split_input[0] == 'PUT'.casefold():
            
            print(f"[RECV] Receiving the filename.")
            file = open(split_input[1], "w")
            server.send("Filename received.".encode("utf-8"))
            
            """ Receiving the file data from the client. """
            data = server.recv(int(split_input[2])).decode("utf-8")
            print(f"[RECV] Receiving the file data.")
            file.write(data)
            server.send("File data received".encode("utf-8"))
            """ Closing the file. """
            file.close()
            
            
        elif split_input[0] == "GET".casefold():
            print("GET REQUEST")
            
            
        elif split_input[0] == "KEYWORD".casefold():
            print("KEYWORD REQUEST")
            
            
        elif split_input[0] == "QUIT".casefold():
            """ Closing the connection from the client. """
            server.close()
            print(f"[DISCONNECTED] {addr} disconnected.")
            flag = False
            
        else:
            print("[ERROR]: THIS COMAND DOES NOT EXIST")



if __name__ == "__main__":
    main()
