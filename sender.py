from helpers.tools import from_file
from helpers.dh_gamal import deffie_hellman, send_signature, verify_signature
import numpy as np
import socket
import time

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
    # Sender setup
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connecting to the receiver running on the same machine
    sender_socket.connect(('localhost', 12345))
    # Generate the public and private key

    x_A, y_A, x_A2, y_A2 = generate_all_keys()

    sender_socket.send(str(y_A).encode())
    time.sleep(2)
    sender_socket.send(str(y_A2).encode())

    # Receive the public key from the receiver
    msg = sender_socket.recv(1024).decode()
    y_B = int(msg)
    msg = sender_socket.recv(1024).decode()
    y_B2 = int(msg)

    print("Sending the signature...")
    c1, c2 = send_signature(y_A, y_B2, a2, q2)
    sender_socket.send(str(c1).encode())
    time.sleep(1)
    sender_socket.send(str(c2).encode())
    print("Receiving Receiver signature")
    c1 = int(sender_socket.recv(1024).decode())
    c2 = int(sender_socket.recv(1024).decode())
    print("Verifying signature...")
    if verify_signature(y_B, x_A2, q2, c1, c2):
        print("Signature verified")
    else:
        print("Signature not verified")
        exit()
    return sender_socket


# Send addition/subtraction problems to the receiver
def handle_messages(sender_socket):
    while True:
        msg = input("Type Here: ")

        if not msg:
            break
        sender_socket.send(msg.encode())

        # Receive the result from the receiver
        # result = sender_socket.recv(1024).decode()
        reply = sender_socket.recv(1024).decode()
        print("Receiver Sent :", reply)

    # Close the sender socket
    sender_socket.close()


if __name__ == "__main__":
    sender_socket = initiliaze_chat()
    handle_messages(sender_socket)
