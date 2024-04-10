import socket
from helpers.tools import from_file
from helpers.dh_gamal import deffie_hellman, send_signature, verify_signature
import time
import numpy as np
# Receiver setup

q, a, q2, a2 = from_file("agree.txt")


def generate_all_keys():
    global q, a, q2, a2
    x_A = np.random.randint(2, q-1)
    x_A2 = np.random.randint(2, q2 - 1)
    y_A = deffie_hellman(q, a, x_A)
    y_A2 = deffie_hellman(q2, a2, x_A2)
    return x_A, y_A, x_A2, y_A2


def initiliaze_chat():
    global q, a, q2, a2
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(('localhost', 12345))
    receiver_socket.listen(1)

    print("Waiting for connection from sender...")

    # Accept connection from the sender
    sender_socket, sender_address = receiver_socket.accept()
    print("Connected to sender:", sender_address)

    time.sleep(2)
    # Receive the public key from the sender
    msg = sender_socket.recv(1024).decode()
    y_A = int(msg)
    msg = sender_socket.recv(1024).decode()
    y_A2 = int(msg)
    # Generate the public and private key

    x_B, y_B, x_B2, y_B2 = generate_all_keys()

    sender_socket.send(str(y_B).encode())
    time.sleep(1)
    sender_socket.send(str(y_B2).encode())

    print("Receiving signature from sender...")
    c1 = int(sender_socket.recv(1024).decode())
    c2 = int(sender_socket.recv(1024).decode())
    print("Signature received from sender")
    print("Verifying signature...")
    if verify_signature(y_B, x_B2, q2, c1, c2):
        print("Signature verified")
    else:
        print("Signature not verified")
        exit()
    print("Sending receiver signature...")
    c1, c2 = send_signature(y_A, y_A2, a2, q2)
    sender_socket.send(str(c1).encode())
    time.sleep(1)
    sender_socket.send(str(c2).encode())
    return sender_socket, receiver_socket


def handle_messages(sender_socket, receiver_socket):
    # Receive addition/subtraction problems from the sender and send back results
    while True:
        msg = sender_socket.recv(1024).decode()
        print("Message from sender:", msg)

        if not msg:
            print("Sender has left the chat , do you want to leave too? (y/n)")
            ans = input(">")
            if ans.lower() == "y":
                print("Exiting ... ")
                time.sleep(1)
                exit()

        reply = input("Type Here: ")

        if not reply:
            break

        # Send the result back to the sender
        sender_socket.send(reply.encode())

    # Close the sockets
    sender_socket.close()
    receiver_socket.close()


if __name__ == "__main__":
    sender_socket, receiver_socket = initiliaze_chat()
    handle_messages(sender_socket, receiver_socket)
