import socket as sc
from sys import argv
import os


def main():
    print("Server is starting...")
    server = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    server.bind(('', int(argv[1])))
    server.listen()
    print("Server is listening...")
    server, addr = server.accept()
    print(f"Client {addr} connected!")

    flag = True
    while flag:
        user_input = server.recv(1024).decode("utf-8")
        print(f"Client entered command: {user_input}")
        split_input = user_input.split()

        if split_input[0].upper() == 'PUT':

            print(f"Client uploading file {split_input[1]}...")

            print(f"Receiving the filename...")
            file = open(split_input[1], "w+")
            server.send("Received the filename!".encode("utf-8"))

            print(f"Receiving the file data...")
            data = server.recv(int(split_input[2])).decode("utf-8")
            print(f"Received file data for {split_input[1]}")

            print("Writing data to file...")
            file.write(data)
            print(f"Data written to file {split_input[1]}")
            server.send("File uploaded.".encode("utf-8"))

            file.close()

        elif split_input[0].upper() == "GET":

            print(f"Client downloading file {split_input[1]}...")
            file = open(split_input[1], "r")

            print("Sending file size to the client...")
            server.send(str(os.path.getsize(split_input[1])).encode("utf-8"))
            print(f"Sent file data for {split_input[1]}")

            data = file.read()
            print("Sending file data to the client...")
            server.send(data.encode("utf-8"))
            print("Sent file data to the client!")
            file.close()

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
