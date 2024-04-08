from helpers.tools import from_file, generate_prime
from helpers.dh_gamal import deffie_hellman

import socket


def generate_public_and_private_key():
    # read the q , a from agree.txt
    q, a, _, _ = from_file("agree.txt")
    # generate the private key
    x_a = generate_prime(1, q)
    # generate the public key
    y_a = deffie_hellman(q, a, x_a)
    print(f"Private Key: {x_a} , Public Key: {y_a}")
    return y_a


def initiliaze_chat():
    # Sender setup
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connecting to the receiver running on the same machine
    sender_socket.connect(('localhost', 12345))
    # Generate the public and private key

    msg = generate_public_and_private_key()
    sender_socket.send(str(msg).encode())

    # Receive the public key from the receiver
    msg = sender_socket.recv(1024).decode()
    print("Public key from receiver:", msg)

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
