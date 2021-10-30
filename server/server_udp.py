import socket as sc
from sys import argv
import os


def main():
    print("[STARTING] Server is starting.")
    server = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
    server.bind((sc.gethostbyname(sc.gethostname()), int(argv[1])))

    flag = True
    while flag:
        user_input, address = server.recvfrom(1024)
        user_input = user_input.decode("utf-8")
        print(user_input)
        split_input = user_input.split()
        print(split_input)

        if split_input[0].upper() == 'PUT':

            print(f"[RECV] Receiving the filename.")
            file = open(split_input[1], "w+")
            server.sendto("Filename received.".encode("utf-8"), address)
            data, address = server.recvfrom(
                int(split_input[2]))
            data = data.decode("utf-8")
            print(f"[RECV] Receiving the file data.")
            file.write(data)
            server.sendto("File data received".encode("utf-8"), address)
            file.close()

        elif split_input[0].upper() == "GET":

            file = open(split_input[1], "r")

            server.sendto(
                str(os.path.getsize(split_input[1])).encode("utf-8"), address)

            data = file.read()
            server.sendto(data.encode("utf-8"), address)
            file.close()
            print(f"Sending file {split_input[1]}!")

        elif split_input[0].upper() == "KEYWORD":
            file = open(split_input[2], "r")
            new_name = split_input[2].replace(".txt", "_anon.txt")
            new_file = open(new_name, "w+")

            new_file.write(file.read().replace(
                split_input[1], "X" * len(split_input[1])))
            server.sendto(("File anonymized with name %s!" %
                           new_name).encode("utf-8"), address)
            file.close()
            new_file.close()

        elif split_input[0].upper() == "QUIT":
            server.close()
            print(f"[DISCONNECTED] {address} disconnected.")
            flag = False

        else:
            print("[ERROR]: THIS COMAND DOES NOT EXIST")


if __name__ == "__main__":
    main()
