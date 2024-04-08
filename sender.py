from helpers.tools import from_file, generate_prime
from helpers.dh_gamal import deffie_hellman, al_gamal

import socket


def DH_keys():
    # read the q , a from agree.txt
    q, a, _, _ = from_file("agree.txt")
    # generate the private key
    x_a = generate_prime(1, q)
    # generate the public key
    y_a = deffie_hellman(q, a, x_a)
    return x_a, y_a


def AlGamal_keys():
    # read the q , a from agree.txt
    _, _, q, a = from_file("agree.txt")
    # generate the private key
    x_a2 = generate_prime(1, q-1)
    # generate the public key
    y_a2 = al_gamal(q, a, x_a2)

    return x_a2, y_a2


def verify_signature(msg, signature, public_key):
    pass


def initiliaze_chat():
    # Sender setup
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connecting to the receiver running on the same machine
    sender_socket.connect(('localhost', 12345))
    # Generate the public and private key

    print("DH stage")
    x_A, y_A = DH_keys()
    print(f"Public Key: {y_A} , Private Key: {x_A}")

    print("Al Gamal stage")
    x_A2, y_A2 = AlGamal_keys()
    print(f"Public Key: {y_A2} , Private Key {x_A2}")

    sender_socket.send(str(y_A2).encode())

    # Receive the public key from the receiver
    msg = sender_socket.recv(1024).decode()
    print("Public key from receiver:", msg)

    print("Verifying the signature...")
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
