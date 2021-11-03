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
# https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
# https://github.com/nikhilroxtomar/Large-File-Transfer-using-TCP-Socket-in-Python3


"""client_tcp.py: TCP Implementation of a client socket"""

__author__ = "Daniel Nofulla"
__version__ = "1.0.0"
__email__ = "dnofulla@albany.edu"

"""Main Function

This function runs the python program!
"""


def main():

    if len(argv) != 3:
        print(
            "Number of command line arguments MUST be 3. The python file name, the server's ip address and the port")
        print("Example:")
        print("python3 client_tcp.py <server_ip_address> <port>")
        exit(1)

    """Client starts and Connects to a server

    To run this TCP Client, make sure to use python3 and
    run it like this:

    python3 client_tcp.py <server_ip_address> <port>
    """

    client = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    print("Connecting to Server...")
    client.connect((argv[1], int(argv[2])))
    print(f"Connected to IP: {argv[1]} at Port: {argv[2]}!")

    flag = True

    while flag:

        """Client Receives input from the user

        The client receives input from the user.
        The client receives up to 1024 bytes of input. The client
        then converts that input to an argument array, for easy
        access to each argument in the user input.
        """

        user_input = input("Enter a command: ")
        arguments = user_input.split()

        if len(arguments) > 3 or len(arguments) < 1:
            arguments[0] = "Invalid number of arguments"

        client.send((user_input).encode("utf-8"))
        client.recv(1024).decode("utf-8")

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

            if len(arguments) != 2:
                print("Incorrect number of arguments")
                print("How to execute a PUT command:")
                print("PUT <file_name>")
            else:
                file = open(arguments[1], "r")

                client.send(
                    (str(os.path.getsize(arguments[1]))).encode("utf-8"))
                client.recv(1024).decode("utf-8")

                while True:
                    data = file.read(1000)
                    if data == "" or not data:
                        file.close()
                        break
                    client.send(data.encode("utf-8"))
                    client.recv(1000).decode("utf-8")

                client.send("Confirm".encode("utf-8"))

                print("Awaiting server response.")
                message = client.recv(1024).decode("utf-8")
                print(f"Server response: {message}")

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

            if len(arguments) != 2:
                print("Incorrect number of arguments")
                print("How to execute a GET command:")
                print("GET <file_name>")
            else:
                file = open(arguments[1], "w+")
                client.send("Confirm".encode("utf-8"))
                size = client.recv(1024).decode("utf-8")
                client.send("Confirm".encode("utf-8"))
                data = client.recv(int(size)).decode("utf-8")
                file.write(data)
                client.send("Confirm".encode("utf-8"))
                response = client.recv(1024).decode("utf-8")
                client.send("Confirm".encode("utf-8"))
                print(f"{response}")
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

            if len(arguments) != 3:
                print("Incorrect number of arguments")
                print("How to execute a KEYWORD command:")
                print("KEYWORD <keyword> <file_name>")
            else:
                print("Awaiting server response.")
                client.send("Confirm".encode("utf-8"))
                message = client.recv(1024).decode("utf-8")
                print(f"Server response: {message}!")

        elif arguments[0].upper() == "QUIT":

            """QUIT COMMAND

            This Command is used like this:

            QUIT <Any extra arguments will be ignored>

            The client simply sends the QUIT command to the server and
            then closes the socket and prints out that its disconnecting
            from the server, and then we set the loop flag to false so
            that the loop quits.
            """

            if len(arguments) != 1:
                print("Incorrect number of arguments")
                print("How to execute a QUIT command:")
                print("QUIT")
            else:
                client.close()
                print(f"Exiting program!")
                flag = False

        else:

            """Failed Commands

            Failed commands are commands that are not listed above.
            These commands will be ignored by the client and just simply
            go to the next request iteration in the loop.
            """

            print(f"{arguments[0]}")


if __name__ == "__main__":
    main()
