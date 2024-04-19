import socket
import sys
import time
import numpy as np

from helpers.dh_gamal import (dh_gamal, send_signature_sha1,
                              verify_signature_sha1, generate_aes_key)
from helpers.tools import from_file

# Receiver setup


# q : deffie hellman prime number
# a : deffie hellman generator
# q2 : gamal prime number
# a2 : gamal generator
q, a, q2, a2 = from_file("agree.txt")


def generate_all_keys():
    # set the seed to 0
    np.random.seed(0)
    global q, a, q2, a2
    x_B = np.random.randint(2, q-1)
    x_B2 = np.random.randint(2, q2 - 1)
    y_B = dh_gamal(q, a, x_B)
    y_B2 = dh_gamal(q2, a2, x_B2)
    print(f"{sys.argv[0][2:-3]}'s DH(unshared) keys: {x_B}, {y_B}")
    return x_B, y_B, x_B2, y_B2


def initiliaze_chat():
    global q, a, q2, a2
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(('localhost', 12345))
    receiver_socket.listen(1)

    print("Waiting for connection from sender...")

    # Accept connection from the sender
    sender_socket, sender_address = receiver_socket.accept()
    print("Connected to sender:", sender_address)

    x_B, y_B, x_B2, y_B2 = generate_all_keys()

    msg = sender_socket.recv(1024).decode()
    y_A2 = int(msg)
    print(f"Received the Algamal key {y_A2} from Receiver...")
    time.sleep(5)
    print(f"Sending the Algamal key {y_B2} to Receiver...")
    sender_socket.send(str(y_B2).encode())
    time.sleep(5)
    sender_sig = eval(sender_socket.recv(1024).decode())
    print(f"Received signature from sender {sender_sig}")
    time.sleep(5)
    print("Verifying signature...")
    if verify_signature_sha1(
            sender_sig[0], y_A2, x_B2, a2, q2, sender_sig[1], sender_sig[2]):
        key = generate_aes_key(q2, sender_sig[0], x_B)
        print("Signature verified")
        print(f"Shared key: {key}")
    else:
        print("Signature not verified, Terminating ...")
        exit()

    rec_sig = send_signature_sha1(y_B, x_B2, a2, q2)
    print(f"Sending receiver signature... {rec_sig}")
    sender_socket.send(str(rec_sig).encode())
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
