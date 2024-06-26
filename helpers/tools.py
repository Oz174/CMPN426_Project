from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from typing import Tuple


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


def encryptString(plaintext: str, key: bytes) -> bytes:
    """
    Encrypt a string using AES
    param plaintext: str
    param key: bytes
    return: bytes
    """
    cipher = AES.new(key, AES.MODE_ECB)
    # pad used to ensure that the plaintext is a multiple of 16 bytes
    # 16 bytes is the block size of AES
    ciphertext = cipher.encrypt(pad(plaintext, 16))
    print(ciphertext.hex())
    return ciphertext


def decryptString(ciphertext: str, key: bytes) -> str:
    """
    Decrypt a string using AES
    param ciphertext: str
    param key: bytes
    return: str
    """
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), 16)
    return plaintext
