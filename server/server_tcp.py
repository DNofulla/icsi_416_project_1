import socket as sc
from sys import argv
import os


def main():
    print("[STARTING] Server is starting.")
    server = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    server.bind(('', int(argv[1])))
    server.listen()
    print("[LISTENING] Server is listening.")
    server, addr = server.accept()
    print(f"[NEW CONNECTION] {addr} connected.")

    flag = True
    while flag:
        user_input = server.recv(1024).decode("utf-8")
        print(user_input)
        split_input = user_input.split()
        print(split_input)

        if split_input[0].upper() == 'PUT':

            print(f"[RECV] Receiving the filename.")
            file = open(split_input[1], "w+")
            server.send("Filename received.".encode("utf-8"))
            data = server.recv(int(split_input[2])).decode("utf-8")
            print(f"[RECV] Receiving the file data.")
            file.write(data)
            server.send("File data received".encode("utf-8"))
            file.close()

        elif split_input[0].upper() == "GET":

            file = open(split_input[1], "r")
            server.send(str(os.path.getsize(split_input[1])).encode("utf-8"))
            data = file.read()
            server.send(data.encode("utf-8"))
            file.close()
            print(f"Sending file {split_input[1]}!")

        elif split_input[0].upper() == "KEYWORD":

            file = open(split_input[2], "r")
            new_name = split_input[2].replace(".txt", "_anon.txt")
            new_file = open(new_name, "w+")
            new_file.write(file.read().replace(
                split_input[1], "X" * len(split_input[1])))
            server.send(("File anonymized with name %s!" %
                        new_name).encode("utf-8"))
            file.close()
            new_file.close()

        elif split_input[0].upper() == "QUIT":
            server.close()
            print(f"[DISCONNECTED] {addr} disconnected.")
            flag = False

        else:
            print("[ERROR]: THIS COMAND DOES NOT EXIST")


if __name__ == "__main__":
    main()
