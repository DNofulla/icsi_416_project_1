import socket as sc
from sys import argv
import os
import re


# ALL RESOURCES (For the entire assignment)
# https://docs.python.org/3.7/library/socket.html
# https://stackoverflow.com/questions/15909064/python-implementation-for-stop-and-wait-algorithm
# https://github.com/mj2266/stop-and-wait-protocol
# https://pymotw.com/3/socket/udp.html
# https://www.youtube.com/watch?v=3QiPPX-KeSc&t=2195s&ab_channel=TechWithTim
# https://dev.to/black_strok3/difference-between-udp-and-tcp-example-code-1pg1
# https://wiki.python.org/moin/UdpCommunication
# https://github.com/DNofulla/Battleship-Game/blob/master/Battleship4.c  (My own implementation in C for my ICSI 333 class game assignment)


"""server_tcp.py: TCP Implementation of a server socket"""

__author__ = "Daniel Nofulla"
__version__ = "1.0.0"
__email__ = "dnofulla@albany.edu"


"""Main Function

This function runs the python program!
"""


def main():
    """Server starts and listens for clients

    To run this TCP Server, make sure to use python3 and
    run it like this:

    python3 server_tcp.py <port>
    """

    server = None
    address = None

    flag = True
    while flag:

        """Setting up socket

        If the server or address variable are equal to None, that means
        that the client had either disconnected or that the server had 
        just started. If that condition is met, then a new server TCP
        socket will be initialized and will listen and wait to accept 
        clients.
        """

        if server == None or address == None:
            print("Server is starting...")
            server = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
            server.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
            server.bind(('', int(argv[1])))
            server.listen()
            print("Server is listening...")
            server, address = server.accept()
            print(f"Client {address} connected!")

        """Server Receives input from the Client

        The server receives the client input from the client.
        The server receives up to 1024 bytes of input. The server
        then converts that client input to an argument array, for easy
        access to each argument in the client input.
        """
        client_input = server.recv(1024).decode("utf-8")
        print(f"Client entered command: {client_input}")
        arguments = client_input.split()
        print(client_input)
        print(arguments)
        server.send("Confirm".encode("utf-8"))

        if arguments[0].upper() == 'PUT':

            """PUT COMMAND

            This Command is used like this:

            PUT <file>

            When the put command is received, the server sends
            a response to the client that it received the file name
            and size (from the command arguments). Then the server proceeds
            to receive the file data with with a buffer the size. After the server receives the data, it
            writes the data to the file, successfully completing the upload.
            The server then lets the client know that the file was uploaded.
            """

            print(f"Client uploading file {arguments[1]}...")
            file = open(arguments[1], "w+")
            size = int(server.recv(1024).decode("utf-8"))
            print(f"Receiving the file data...")
            server.send("Confirm".encode("utf-8"))

            while size:
                data = server.recv(1000)
                data = data.decode("utf-8")
                file.write(data)
                server.send("Confirm".encode("utf-8"))

                if len(data) < 1000 and size % 1000 != 0:
                    break

            server.recv(1024).decode("utf-8")

            file.close()
            print(f"Received and Wrote file data for {arguments[1]}")
            server.send("File uploaded.".encode("utf-8"))

        elif arguments[0].upper() == "GET":

            """GET COMMAND

            This Command is used like this:

            GET <file>

            The Server first opens the file being requested, then
            sends the size of the file to the client, and then proceeds
            to read the data and send it to the client. After that
            it sends a message to the client that says that the file
            has been downloaded.
            """

            print(f"Client downloading file {arguments[1]}...")
            file = open(arguments[1], "r")
            server.recv(1024).decode("utf-8")
            print("Sending file size to the client...")
            server.send(str(os.path.getsize(arguments[1])).encode("utf-8"))
            print(f"Sent file data for {arguments[1]}")
            server.recv(1024).decode("utf-8")
            data = file.read()
            print("Sending file data to the client...")
            server.send(data.encode("utf-8"))
            server.recv(1024).decode("utf-8")
            print("Sent file data to the client!")

            file.close()

            server.send(("File %s downloaded." %
                        arguments[1]).encode("utf-8"))
            server.recv(1024).decode("utf-8")

        elif arguments[0].upper() == "KEYWORD":

            """KEYWORD COMMAND

            This Command is used like this:

            KEYWORD <keyword_to_be_anonymized> <file>

            The server opens the file to be anonymized and creates a name with
            the same name but with a '_anon.txt' ending instead of just '.txt'.
            In the anonymization output file, we copy the data from the original
            file to the anonymization output file, but we replace any occurrence
            the keyword_to_be_anonymized in the file, with 'X's.
            For example, the word 'Project' would turn into 'XXXXXXX'.
            """

            print(
                f"Client anonymizing file {arguments[2]} with keyword {arguments[1]}...")

            old_name = arguments[2]
            print("Opening files...")
            file = open(arguments[2], "r")
            new_name = arguments[2].replace(".txt", "_anon.txt")
            new_file = open(new_name, "w+")
            print("Anonymizing and Writing file...")

            new_file.write(re.compile(re.escape(arguments[1]), re.IGNORECASE).sub(
                "X" * len(arguments[1]), file.read()))

            # new_file.write(file.read().replace(
            #     str(arguments[1]), "X" * len(arguments[1])))

            file.close()
            new_file.close()
            server.recv(1024).decode("utf-8")
            print(
                f"File {old_name} anonymized. Output file is {new_name}!")
            server.send(("File %s anonymized. Output file is %s" %
                        (old_name, new_name)).encode("utf-8"))

        elif arguments[0].upper() == "QUIT":

            """QUIT COMMAND

            This Command is used like this:

            QUIT <Any extra arguments will be ignored>

            The server simply prints out that the client has disconnected.
            """
            print(f"Client {address} disconnected from the server!")
            address = None
            server.close()
            server = None

        else:

            """Failed Commands

            Failed commands are commands that are not listed above.
            These commands will be ignored by the server and just simply
            go to the next request iteration in the loop.
            """

            print(f"ERROR: COMAND {arguments[1]} DOES NOT EXIST")


if __name__ == "__main__":
    main()
