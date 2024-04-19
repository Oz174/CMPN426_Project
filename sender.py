import socket
import sys
import numpy as np

from helpers.dh_gamal import (dh_gamal, send_signature_sha1,
                              verify_signature_sha1, generate_aes_key)
from helpers.tools import from_file, encryptString, decryptString

# q : deffie hellman prime number
# a : deffie hellman generator
# q2 : gamal prime number
# a2 : gamal generator
q, a, q2, a2 = from_file("agree.txt")


def generate_all_keys():
    # set the seed
    np.random.seed(42)
    global q, a, q2, a2
    x_A = np.random.randint(2, q-1)
    x_A2 = np.random.randint(2, q2 - 1)
    y_A = dh_gamal(q, a, x_A)
    y_A2 = dh_gamal(q2, a2, x_A2)
    print(f"{sys.argv[0][2:-3]}'s DH (unshared) keys: {x_A}, {y_A}")
    return x_A, y_A, x_A2, y_A2


def initiliaze_chat():
    global q, a, q2, a2
    # Sender setup
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connecting to the receiver running on the same machine
    sender_socket.connect(('localhost', 12345))
    # Generate the public and private key

    x_A, y_A, x_A2, y_A2 = generate_all_keys()

    print(f"Sending the Algamal key {y_A2} to Receiver...")
    sender_socket.send(str(y_A2).encode())

    # Receive the Algamal key from the receiver
    msg = sender_socket.recv(1024).decode()
    y_B2 = int(msg)
    print(f"Received the Algamal key  {y_B2} from Receiver...")

    sig = send_signature_sha1(y_A, x_A2, a2, q2)
    print(f"Sending the signature : {sig}")
    sender_socket.send(str(sig).encode())

    print("Receiving Receiver signature")
    rec_sig = eval(sender_socket.recv(1024).decode())

    print(f"Verifying signature...{rec_sig}")

    if verify_signature_sha1(
            rec_sig[0], y_B2, a2, q2, rec_sig[1], rec_sig[2]):
        print("Signature verified")
        key = generate_aes_key(q2, rec_sig[0], x_A)
        print(f"Shared key: {key.hexdigest().encode()}")
    else:
        print("Signature not verified, Terminating ...")
        exit()
    return sender_socket, key.digest()


# Send addition/subtraction problems to the receiver
def handle_messages(sender_socket, key):
    while True:
        msg = input("Type Here: ")

        if not msg:
            # tell the receiver that sender has left the chat
            msg = "exit"
        sender_socket.send(encryptString(msg.encode(), key))

        if msg == "exit":
            break

        # Receive the result from the receiver
        # result = sender_socket.recv(1024).decode()
        reply = decryptString(sender_socket.recv(1024), key).decode()
        print("Receiver Sent :", reply)

    # Close the sender socket
    sender_socket.close()


if __name__ == "__main__":
    sender_socket, key = initiliaze_chat()
    handle_messages(sender_socket, key)
