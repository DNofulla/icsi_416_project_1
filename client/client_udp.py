import socket as sc
import os
from sys import argv


def main():
    client = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
    print(argv)
    print(sc.gethostbyname(sc.gethostname()))
    flag = True

    while flag:
        user_input = input("Enter a command: ")
        split_input = user_input.split()

        if split_input[0].upper() == 'PUT':

            file = open(split_input[1], "r")
            data = file.read()
            client.sendto(
                (user_input + " " + str(os.path.getsize(split_input[1]))).encode("utf-8"), (argv[1], int(argv[2])))
            msg, address = client.recvfrom(1024)
            msg = msg.decode("utf-8")
            print(f"[SERVER]: {msg}")
            client.sendto(data.encode("utf-8"), address)
            msg, address = client.recvfrom(1024)
            msg = msg.decode("utf-8")
            print(f"[SERVER]: {msg}")
            file.close()

        elif split_input[0].upper() == "GET":

            file = open(split_input[1], "w+")
            client.sendto(user_input.encode("utf-8"), (argv[1], int(argv[2])))
            size, address = client.recvfrom(1024)
            size = size.decode("utf-8")
            print(f"[SERVER]: File size is {size}!")
            data, address = client.recvfrom(int(size))
            data = data.decode("utf-8")
            print(f"[SERVER]: File {split_input[1]} sent!")
            file.write(data)
            file.close()

        elif split_input[0].upper() == "KEYWORD":

            client.sendto(user_input.encode("utf-8"), (argv[1], int(argv[2])))
            msg, address = client.recvfrom(1024)
            msg = msg.decode("utf-8")
            print(f"[SERVER]: {msg}!")

        elif split_input[0].upper() == "QUIT":
            client.sendto(split_input[0].encode(
                "utf-8"), (argv[1], int(argv[2])))
            client.close()
            print(f"DISCONNECTING FROM SERVER")
            flag = False

        else:
            print("[ERROR]: THIS COMAND DOES NOT EXIST")


if __name__ == "__main__":
    main()
