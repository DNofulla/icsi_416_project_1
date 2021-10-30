import socket as sc
import os
from sys import argv


def main():
    client = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    print("Connecting to Server!")
    client.connect((argv[1], int(argv[2])))
    print(f"Connected to IP: {argv[1]} at Port: {argv[2]}")

    flag = True

    while flag:
        user_input = input("Enter a command: ")
        split_input = user_input.split()

        if split_input[0].upper() == 'PUT':

            file = open(split_input[1], "r")
            data = file.read()
            client.send(
                (user_input + " " + str(os.path.getsize(split_input[1]))).encode("utf-8"))
            message = client.recv(1024).decode("utf-8")
            print(f"Server: {message}")
            client.send(data.encode("utf-8"))
            message = client.recv(1024).decode("utf-8")
            print(f"Server: {message}")
            file.close()

        elif split_input[0].upper() == "GET":

            file = open(split_input[1], "w+")
            client.send(user_input.encode("utf-8"))
            size = client.recv(1024).decode("utf-8")
            print(f"Server: File size is {size}!")
            data = client.recv(int(size)).decode("utf-8")
            print(f"Server: File {split_input[1]} sent!")
            file.write(data)
            file.close()

        elif split_input[0].upper() == "KEYWORD":

            client.send(user_input.encode("utf-8"))
            message = client.recv(1024).decode("utf-8")
            print(f"Server: {message}!")

        elif split_input[0].upper() == "QUIT":

            client.send(split_input[0].encode("utf-8"))
            client.close()
            print(f"DISCONNECTING FROM SERVER")
            flag = False

        else:
            print("[ERROR]: THIS COMAND DOES NOT EXIST")


if __name__ == "__main__":
    main()
