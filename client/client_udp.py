import socket as sc
import os
from sys import argv


# ALL RESOURCES (For the entire assignment)
# https://docs.python.org/3.7/library/socket.html
# https://stackoverflow.com/questions/15909064/python-implementation-for-stop-and-wait-algorithm
# https://github.com/mj2266/stop-and-wait-protocol
# https://pymotw.com/3/socket/udp.html
# https://www.youtube.com/watch?v=3QiPPX-KeSc&t=2195s&ab_channel=TechWithTim
# https://dev.to/black_strok3/difference-between-udp-and-tcp-example-code-1pg1
# https://wiki.python.org/moin/UdpCommunication
# https://github.com/DNofulla/Battleship-Game/blob/master/Battleship4.c  (My own implementation in C for my ICSI 333 class game assignment)


"""client_udp.py: UDP Implementation of a client socket with Stop and Wait Functionality"""

__author__ = "Daniel Nofulla"
__version__ = "1.0.0"
__email__ = "dnofulla@albany.edu"

"""Main Function

This function runs the python program!
"""


def main():
    """Client starts and Connects to a server

    To run this UDP Client, make sure to use python3 and
    run it like this:

    python3 client_udp.py <server_ip_address> <port>
    """

    print("Creating a UDP Client Socket...")
    client = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
    flag = True
    print("Created UDP Client Socket!")

    while flag:

        """Client Receives input from the user

        The client receives input from the user.
        The client receives up to 1000 bytes of input. The client
        then converts that input to an argument array, for easy
        access to each argument in the user input.
        """

        user_input = input("Enter a command: ")
        arguments = user_input.split()

        if arguments[0].upper() == 'PUT':

            """PUT COMMAND

            This Command is used like this:

            PUT <file>

            When the put command is received, the client sends
            a message to the server with the user input and the size
            of the file to be uploaded. The client then receives a message
            from the server confirming the data was received and then the
            client then sends the data of the file to be uploaded. Finally,
            the client receives a final response from the server saying the
            file has been uploaded.
            """

            file = open(arguments[1], "r")

            while True:
                try:
                    client.settimeout(1)
                    client.sendto(
                        (user_input).encode("utf-8"), (argv[1], int(argv[2])))
                    client.settimeout(1)
                    FIN, address = client.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout:
                    print("Did not receive ACK. Terminating.")

            while True:
                try:
                    client.settimeout(1)
                    client.sendto(
                        ("LEN:" + str(os.path.getsize(arguments[1]))).encode("utf-8"), address)
                    client.settimeout(1)
                    FIN, address = client.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout:
                    print("Did not receive ACK. Terminating.")

            size_read = 0

            while True:
                data = file.read(1000)
                size_read += 1000
                if data == "" or not data:
                    file.close()
                    break
                try:
                    client.settimeout(1)
                    client.sendto(data.encode("utf-8"), address)
                    client.settimeout(1)
                    FIN, address = client.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        continue

                except sc.timeout:
                    print("Did not receive ACK. Terminating.")
                    # Will go back 1000 Bytes, to redo operation if socket times out
                    file.seek(size_read - 1000)

            print("Awaiting server response.")

            while True:
                try:
                    client.settimeout(1)
                    msg, address = client.recvfrom(1000)
                    client.settimeout(1)
                    client.sendto("FIN".encode("utf-8"), address)
                    break
                except sc.timeout:
                    print("Data transmission terminated prematurely.")

            msg = msg.decode("utf-8")
            print(f"Server response: {msg}")

        elif arguments[0].upper() == "GET":

            """GET COMMAND

            This Command is used like this:

            GET <file>

            The client first sends the user input to the server.
            Then the client proceeds to receive the size of the file
            to be downloaded and the file data of the file to be
            downloaded. Them the client copies the data to a new file.
            Finally the client receives a response from the server saying
            that the file has been downloaded.
            """

            file = open(arguments[1], "w+")

            while True:
                try:
                    client.settimeout(1)
                    client.sendto(user_input.encode("utf-8"),
                                  (argv[1], int(argv[2])))
                    client.settimeout(1)
                    FIN, address = client.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout or file.errors:
                    print("Did not receive ACK. Terminating.")

            while True:
                try:
                    client.settimeout(1)
                    size, address = client.recvfrom(1000)
                    client.settimeout(1)
                    client.sendto("FIN".encode("utf-8"), address)
                    break
                except sc.timeout:
                    print("Did not receive data. Terminating.")

            size = int((size.decode("utf-8")).split(':')[1])

            while size:
                try:
                    client.settimeout(1)
                    data, address = client.recvfrom(1000)
                    data = data.decode("utf-8")
                    file.write(data)
                    client.settimeout(1)
                    client.sendto("FIN".encode("utf-8"), address)
                    if len(data) < 1000 and size % 1000 != 0:
                        break
                except sc.timeout:
                    print("Data transmission terminated prematurely.")

            while True:
                try:
                    client.settimeout(1)
                    msg, address = client.recvfrom(1000)
                    client.settimeout(1)
                    client.sendto("FIN".encode("utf-8"), address)
                    break
                except sc.timeout:
                    print("Did not receive data. Terminating.")

            msg = msg.decode("utf-8")
            print(f"{msg}")

            file.close()

        elif arguments[0].upper() == "KEYWORD":

            """KEYWORD COMMAND

            This Command is used like this:

            KEYWORD <keyword_to_be_anonymized> <file>

            The client simply sends the user input to the server.
            When the process is done on the server side, the client
            receives a message from the server that the file requested
            has been anonymized into a new file, and also receives that
            new anonymized file's name in the same message.
            """

            while True:
                try:
                    client.settimeout(1)
                    client.sendto(user_input.encode("utf-8"),
                                  (argv[1], int(argv[2])))
                    client.settimeout(1)
                    FIN, address = client.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout or file.errors:
                    print("Did not receive ACK. Terminating.")

            print("Awaiting server response.")

            while True:
                try:
                    client.settimeout(1)
                    msg, address = client.recvfrom(1000)
                    client.settimeout(1)
                    client.sendto("FIN".encode("utf-8"), address)
                    break
                except sc.timeout:
                    print("Did not receive data. Terminating.")

            msg = msg.decode("utf-8")
            print(f"Server response: {msg}!")

        elif arguments[0].upper() == "QUIT":

            """QUIT COMMAND

            This Command is used like this:

            QUIT <Any extra arguments will be ignored>

            The client simply sends the QUIT command to the server and
            then closes the socket and prints out that its disconnecting
            from the server, and then we set the loop flag to false so
            that the loop quits.
            """

            while True:
                try:
                    client.settimeout(1)
                    client.sendto(user_input.encode("utf-8"),
                                  (argv[1], int(argv[2])))
                    client.settimeout(1)
                    FIN, address = client.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout or file.errors:
                    print("Did not receive ACK. Terminating.")

            client.close()
            print(f"Exiting program!")
            flag = False

        else:

            """Failed Commands

            Failed commands are commands that are not listed above.
            These commands will be ignored by the client and just simply
            go to the next request iteration in the loop.
            """

            print(f"ERROR: COMAND {arguments[0]} DOES NOT EXIST")


if __name__ == "__main__":
    main()
