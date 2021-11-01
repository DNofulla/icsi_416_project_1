import socket as sc
from sys import argv
import os


# ALL RESOURCES (For the entire assignment)
# https://docs.python.org/3.7/library/socket.html
# https://stackoverflow.com/questions/15909064/python-implementation-for-stop-and-wait-algorithm
# https://github.com/mj2266/stop-and-wait-protocol
# https://pymotw.com/3/socket/udp.html
# https://www.youtube.com/watch?v=3QiPPX-KeSc&t=2195s&ab_channel=TechWithTim
# https://dev.to/black_strok3/difference-between-udp-and-tcp-example-code-1pg1
# https://wiki.python.org/moin/UdpCommunication
# https://github.com/DNofulla/Battleship-Game/blob/master/Battleship4.c  (My own implementation in C for my ICSI 333 class game assignment)


"""server_udp.py: UDP Implementation of a server socket with Stop and Wait Functionality"""

__author__ = "Daniel Nofulla"
__version__ = "1.0.0"
__email__ = "dnofulla@albany.edu"


"""STOP AND WAIT PROTOCOL

Sender: Every time there is a packet sent, there needs to be an 
acknowledgement received from the receiver of the original message.

Receiver: The receiver sends a FIN message back to the Sender after receiving
the data from the sender first. The FIN message works like an acknowledgement.

Every Request has a timeout duration of 1 second (except for the receiver that
receives the actual client input).
"""

"""Main Function

This function runs the python program!
"""


def main():
    """Server starts and listens for clients

    To run this UDP Server, make sure to use python3 and
    run it like this:

    python3 server_udp.py <port>
    """

    print("Server is starting...")
    server = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
    server.bind(('', int(argv[1])))
    print("Server is listening...")

    flag = True
    while flag:

        """Server Receives input from the Client

        The server receives the client input from the client.
        The server receives up to 1000 bytes of input. The server
        then converts that client input to an argument array, for easy
        access to each argument in the client input.
        """
        while True:
            try:
                # If the user does not input a command and send it
                # to the server for 1000 seconds, it will timeout.
                server.settimeout(1000)
                client_input, address = server.recvfrom(1000)
                server.settimeout(1)
                server.sendto("FIN".encode("utf-8"), address)
                break
            except sc.timeout:
                print("Did not receive data. Terminating.")

        client_input = client_input.decode("utf-8")
        print(f"Client entered command: {client_input}")
        arguments = client_input.split()

        if arguments[0].upper() == 'PUT':

            """PUT COMMAND

            This Command is used like this:

            PUT <file>

            When the put command is received, the server sends
            a response to the client that it received the file name
            and size (from the command arguments). Then the server proceeds
            to receive the file data with with a buffer the size that was
            collected from the command arguments (it is attached as the third
            argument as arguments[2]). After the server receives the data, it
            writes the data to the file, successfully completing the upload.
            The server then lets the client know that the file was uploaded.
            """

            print(f"Client uploading file {arguments[1]}...")
            file = open(arguments[1], "w+")

            while True:
                try:
                    server.settimeout(1)
                    remaining_size, address = server.recvfrom(1000)
                    server.settimeout(1)
                    server.sendto("FIN".encode("utf-8"), address)
                    break
                except sc.timeout:
                    print("Data transmission terminated prematurely.")

            remaining_size = int(
                (remaining_size.decode("utf-8")).split(':')[1])

            print(f"Receiving the file data...")

            while remaining_size:
                try:
                    server.settimeout(1)
                    data, address = server.recvfrom(1000)
                    data = data.decode("utf-8")
                    file.write(data)
                    server.settimeout(1)
                    server.sendto("FIN".encode("utf-8"), address)
                    if len(data) < 1000 and remaining_size % 1000 != 0:
                        break
                except sc.timeout:
                    print("Data transmission terminated prematurely.")

            print(f"Received and Wrote file data for {arguments[1]}")
            print(f"Data written to file {arguments[1]}")
            file.close()

            while True:
                try:
                    server.settimeout(1)
                    server.sendto(
                        "File uploaded.".encode("utf-8"),
                        address)
                    server.settimeout(1)
                    FIN, address = server.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout:
                    print("Did not receive ACK. Terminating.")

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

            print("Sending file size to the client...")

            while True:
                try:
                    server.settimeout(1)
                    server.sendto(
                        ("LEN:" + str(os.path.getsize(arguments[1]))).encode("utf-8"), address)
                    server.settimeout(1)
                    FIN, address = server.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout:
                    print("Did not receive ACK. Terminating.")

            print(f"Sent file data for {arguments[1]}")
            print("Sending file data to the client...")

            size_read = 0

            while True:
                data = file.read(1000)
                size_read += 1000
                if data == "" or not data:
                    file.close()
                    break
                try:
                    server.settimeout(1)
                    server.sendto(data.encode("utf-8"), address)
                    server.settimeout(1)
                    FIN, address = server.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        continue

                except sc.timeout:
                    print("Did not receive ACK. Terminating.")
                    # Will go back 1000 Bytes, to redo operation if socket times out
                    file.seek(size_read - 1000)

            print("Sent file data to the client!")

            while True:
                try:
                    server.settimeout(1)
                    server.sendto(
                        ("File %s downloaded." %
                         arguments[1]).encode("utf-8"), address)
                    server.settimeout(1)
                    FIN, address = server.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout:
                    print("Did not receive ACK. Terminating.")

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

            new_file.write(file.read().replace(
                arguments[1], "X" * len(arguments[1])))

            file.close()
            new_file.close()

            print(f"File {old_name} anonymized. Output file is {new_name}!")

            while True:
                try:
                    server.settimeout(1)
                    server.sendto(("File %s anonymized. Output file is %s" %
                                   (old_name, new_name)).encode("utf-8"), address)
                    server.settimeout(1)
                    FIN, address = server.recvfrom(1000)

                    if FIN.decode("utf-8") == "FIN":
                        break
                except sc.timeout or file.errors:
                    print("Did not receive ACK. Terminating.")

        elif arguments[0].upper() == "QUIT":

            """QUIT COMMAND

            This Command is used like this:

            QUIT <Any extra arguments will be ignored>

            The server simply prints out that the client has disconnected.
            """

            print(f"Client {address} disconnected from the server!")

        else:

            """Failed Commands

            Failed commands are commands that are not listed above.
            These commands will be ignored by the server and just simply
            go to the next request iteration in the loop.
            """
            print(f"ERROR: COMAND {arguments[0]} DOES NOT EXIST")


if __name__ == "__main__":
    main()
