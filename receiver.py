import socket
from helpers.tools import from_file, generate_prime
from helpers.dh_gamal import deffie_hellman, al_gamal
import time

# Receiver setup


def DH_Keys():
    # read the q , a from agree.txt
    q, a, _, _ = from_file("agree.txt")
    # generate the private key
    x_b = generate_prime(1, q)
    # generate the public key
    y_b = deffie_hellman(q, a, x_b)

    return x_b, y_b


def AlGamal_keys():
    # read the q , a from agree.txt
    _, _, q, a = from_file("agree.txt")
    # generate the private key
    x_a = generate_prime(1, q-1)
    # generate the public key
    y_a = al_gamal(q, a, x_a)
    return x_a, y_a


def verify_signature(msg, signature, public_key):
    pass


def initiliaze_chat():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(('localhost', 12345))
    receiver_socket.listen(1)

    print("Waiting for connection from sender...")

    # Accept connection from the sender
    sender_socket, sender_address = receiver_socket.accept()
    print("Connected to sender:", sender_address)

    # Receive the public key from the sender
    msg = sender_socket.recv(1024).decode()
    print("Public key from sender using Al Gamal:", msg)
    # Generate the public and private key

    print("DH stage")
    x_A, y_A = DH_Keys()
    print(f"Public Key: {y_A} , Private Key: {x_A}")

    print("Al Gamal stage")
    x_A2, y_A2 = AlGamal_keys()
    print(f"Public Key: {y_A2} , Private Key {x_A2}")

    sender_socket.send(str(y_A2).encode())
    print("Verifying the signature...")
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
