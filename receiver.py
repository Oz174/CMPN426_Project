import socket
import time

# Receiver setup


def initiliaze_chat():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(('localhost', 12345))
    receiver_socket.listen(1)

    print("Waiting for connection from sender...")

    # Accept connection from the sender
    sender_socket, sender_address = receiver_socket.accept()
    print("Connected to sender:", sender_address)
    return sender_socket, receiver_socket


def handle_messages(sender_socket, receiver_socket):
    # Receive addition/subtraction problems from the sender and send back results
    while True:
        msg = sender_socket.recv(1024).decode()
        print("Message from sender:", msg)
        # problem = sender_socket.recv(1024).decode()
        # if not problem:
        #     break

        if not msg:
            print("Sender has left the chat , do you want to leave too? (y/n)")
            ans = input(">")
            if ans.lower() == "y":
                print("Exiting ... ")
                time.sleep(1)
                exit()

        # # Process the problem and compute the result
        # result = str(eval(problem))
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
