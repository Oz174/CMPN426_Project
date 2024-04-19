import numpy as np
from itertools import cycle
import time

char = "abcdefghiklmnopqrstuvwxyz"  # missing 'j'


def create_matrix(keyword: str) -> np.ndarray:
    keyword: list = list(keyword.replace("j", "i"))
    # create 5x5 matrix with keyword
    keyword.extend([c for c in char if c not in keyword])
    matrix = np.array(keyword, dtype=str)
    return matrix.reshape((5, 5))


def generate_key_array(matrix: np.ndarray, key: str, n: int) -> np.ndarray:
    # key is repeated until it's equal to the cipher length n
    key = key.replace("j", "i")
    cycle_key = cycle(key)
    key_array = np.zeros(n, dtype=int)
    while n:
        row, col = np.where(matrix == next(cycle_key))
        key_array[n-1] = (row[0]*10 + col[0])
        n -= 1
    return np.array(list(reversed(key_array)))


def decipher_message(cipher: list, key_array: list, matrix: np.ndarray) -> str:
    msg = ""
    for a, b in zip(cipher, key_array):
        # -11 is for the indexing of python starts from 0
        row, col = divmod((a-b-11), 10)
        # same for the -1
        msg += matrix[row-1, col-1]
    return msg

# THIS IS FOR FUN ~ NOT REQUIRED


def cipher_message(msg: str, keyword: str, key: str) -> list:
    msg = msg.replace("j", "i")
    matrix = create_matrix(keyword)
    key_arr = generate_key_array(matrix, key, len(msg))
    message_arr = generate_key_array(matrix, msg, len(msg))
    cipher = []

    for a, b in zip(message_arr, key_arr):
        # to mimic the nhilist
        cipher.append(a+b+22)

    return cipher


if __name__ == "__main__":
    # test
    cipher = [96, 57, 47, 66, 62, 38, 55, 67, 55, 35, 68, 44, 48, 95, 66, 65,
              57, 65, 53, 75, 78, 77, 55, 36, 47, 55, 45, 66, 87, 34, 46, 48, 33, 77]
    keyword = "polybius"
    key = "russian"

    start = time.perf_counter()
    matrix = create_matrix(keyword)
    end = time.perf_counter()
    print(f"Matrix Creation took {end-start:.6f} seconds")
    # print(matrix)
    # print(np.where(matrix == "r"))
    start = time.perf_counter()
    key_arr = generate_key_array(matrix, key, len(cipher))
    end = time.perf_counter()
    print(f"Key Array took {end-start:.6f} seconds")
    # print(key_arr)
    start = time.perf_counter()
    msg = decipher_message(cipher, key_arr, matrix)
    end = time.perf_counter()
    print(f"Decipher took {end-start:.6f} seconds")
    print(msg)
