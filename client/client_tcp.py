import socket as sc
import os
from sys import argv 


def main():
    client = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    print(argv)
    print(sc.gethostbyname(sc.gethostname()))
    client.connect((argv[1], int(argv[2])))
    
    flag = True
    
    while flag:
        user_input = input("Please enter a command: ")
    
        split_input = user_input.split()
        
            
        if split_input[0] == 'PUT'.casefold():

            file = open(split_input[1], "r")
            data = file.read()
            
            client.send((user_input + " " + str(os.path.getsize(split_input[1]))).encode("utf-8"))
            msg = client.recv(1024).decode("utf-8")
            print(f"[SERVER]: {msg}")

            client.send(data.encode("utf-8"))
            msg = client.recv(1024).decode("utf-8")
            print(f"[SERVER]: {msg}")
            file.close()
            
        elif split_input[0] == "GET".casefold():
            
            file = open(split_input[1], "w+")
            
            client.send(user_input.encode("utf-8"))

            size = client.recv(1024).decode("utf-8")
            print(f"[SERVER]: File size is {size}!")
            data = client.recv(int(size)).decode("utf-8")
            print(f"[SERVER]: File {split_input[1]} sent!")
            file.write(data)
            file.close()
            
            
            
        elif split_input[0] == "KEYWORD".casefold():
            
            client.send(user_input.encode("utf-8"))

            msg = client.recv(1024).decode("utf-8")
            print(f"[SERVER]: {msg}!")
            
            
            
        elif split_input[0] == "QUIT".casefold():
            
            
            client.send(split_input[0].encode("utf-8")) 
            client.close()
            print(f"DISCONNECTING FROM SERVER")
            flag = False
            
        else:
            print("[ERROR]: THIS COMAND DOES NOT EXIST")

            


if __name__ == "__main__":
    main()
