import socket

# Sender setup
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connecting to the receiver running on the same machine
sender_socket.connect(('localhost', 12345))

# Send addition/subtraction problems to the receiver
while True:
    msg = input("Type Here: ")
    # problem = input(
    #     "Enter an addition/subtraction problem (e.g., '2+3' or '5-2'): ")

    # # Break if the user enters an empty string
    # if not problem:
    #     break

    if not msg:
        break

    sender_socket.send(msg.encode())

    # Receive the result from the receiver
    # result = sender_socket.recv(1024).decode()
    reply = sender_socket.recv(1024).decode()
    print("Receiver Sent :", reply)


# Close the sender socket
sender_socket.close()
