from typing import List, Union, Tuple
import numpy as np
import base64
import os


def is_prime(n: int) -> bool:
    """
    Check if a number is prime
    param n: int
    return: bool
    """
    if n <= 1:
        return False
    else:
        return all([n % i != 0 for i in range(2, int(n/2)+1)])


def generate_prime(low: int, high: int) -> Union[int, List[int]]:
    """
    Generate a prime number between low and high
    param low: int
    param high: int
    param how_many: int
    return: int or List[int]
    """
    prime_num = np.random.randint(low=low, high=high)
    while not is_prime(prime_num):
        prime_num = np.random.randint(low=low, high=high)
    return prime_num


def enforce_message_encoding(message: str, n: int, encoding: str = 'utf-8') -> Union[int, List[int]]:
    """
    Encode a message to a number
    param message: str
    param n: int
    return: int or List[int]
    """
    # try encoding the whole message
    message_bytes = message.encode('utf-8')
    if int.from_bytes(message_bytes, 'little') > n:
        # split the message into blocks and encode each block
        message_blocks = [message[i:i+2] for i in range(0, len(message), 2)]
        utf_8_blocks = [block.encode('utf-8') for block in message_blocks]
        if encoding == 'base85':
            utf_8_blocks = [base64.b85encode(block) for block in utf_8_blocks]
        int_blocks = [int.from_bytes(block, 'little')
                      for block in utf_8_blocks]
    else:
        if encoding == 'base85':
            message_bytes = base64.b85encode(message_bytes)
        int_blocks = int.from_bytes(message_bytes, 'little')
    return int_blocks


def from_file(file_path: str) -> Tuple[int]:
    """
    Read the contents of a file
    param file_path: str
    return: str
    """
    q_dh = 0
    a_dh = 0
    q_gamal = 0
    a_gamal = 0
    with open(file_path, 'r') as f:
        sender_keys = f.readlines()
    for key in sender_keys:
        if 'q_dh' in key:
            q_dh = int(key.split('=')[-1])
        elif 'a_dh' in key:
            a_dh = int(key.split('=')[-1])
        elif 'q_gamal' in key:
            q_gamal = int(key.split('=')[-1])
        elif 'a_gamal' in key:
            a_gamal = int(key.split('=')[-1])
    return q_dh, a_dh, q_gamal, a_gamal


def generate_params_file(file_path: str) -> None:
    """
    Write the contents to a file
    param file_path: str
    param content: str
    """
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as file:
        # radomly generate the prime numbers
        q_dh = generate_prime(100, 1000)
        a_dh = np.random.randint(2, q_dh)
        q_gamal = generate_prime(100, 1000)
        a_gamal = np.random.randint(2, q_gamal)

        file.write(f'q_dh={q_dh}\n')
        file.write(f'a_dh={a_dh}\n')
        file.write(f'q_gamal={q_gamal}\n')
        file.write(f'a_gamal={a_gamal}\n')
    return None
