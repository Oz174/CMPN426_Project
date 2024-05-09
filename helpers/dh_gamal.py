import numpy as np
import hashlib
from typing import TypeVar, Tuple


prime = TypeVar('prime', bound=int)
k = TypeVar('k', bound=int)


def dh_gamal(prime: int, generator: int, private_key: int) -> int:
    """
    Generate the public key for the Diffie-Hellman or El-Gamal key exchange
    param prime: int
    param generator: int
    param private_key: int
    return: int
    """
    # generator is the primitive root of the prime number
    # private_key is the private key of the user
    # public key is the generator raised to the power of the private key modulo the prime number
    public_key = (generator
                  ** private_key) % prime
    return public_key


def generate_aes_key(prime: int, public_key: int, private_key: int) -> int:
    """
    Generate the secret key for the Diffie-Hellman key exchange
    param prime: int
    param public_key: int (Deffie_Hellman Public Key)
    param private_key: int (Deffie_Hellman Private Key)
    return: int
    """
    # the secret key is the public key raised to the power of the private key modulo the prime number
    secret_key = (public_key
                  ** private_key) % prime
    return hashlib.sha256(str(secret_key).encode())


def gcd(num1: int, num2: int) -> int:
    """
    Calculate the greatest common divisor of two numbers
    param num1: int
    param num2: int
    return: int
    """
    _, r = divmod(num1, num2)
    return num2 if r == 0 else gcd(num2, r)


def extended_euclidean(a: k, b: prime) -> Tuple[int]:
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_euclidean(b % a, a)
        return g, y - (b // a) * x, x


def generate_random_k(p: prime) -> int:
    # k belongs to {2,...,p-2} wikipedia algamal signature
    k = np.random.randint(2, p-1)
    while gcd(p-1, k) != 1:
        k = np.random.randint(2, p-1)
    return k


def send_signature_sha1(public_dh: int, private_gamal: int, generator: int, prime: int) -> Tuple[int, int, int]:

    m = hashlib.sha1(str(public_dh).encode()).hexdigest()
    # take last 8 bits
    m = int(m[-1:], 16)
    try:
        assert 0 < m < prime, "m doesn't satisfy the condition 0 < m < prime"
    except AssertionError:
        return None
    # generate random K

    # in the unlikely event of s = 0 , you will have to regenerate the k (wikipedia algamal signature)
    r, s = 0, 0
    while s == 0:
        k = generate_random_k(prime)
        r = pow(generator, k, prime)
        s = (m - private_gamal*r) * \
            extended_euclidean(k, prime-1)[1] % (prime-1)
    # print(f"m: {m}, r: {r}, s: {s} , k: {k} ")
    return public_dh, r, s


def verify_signature_sha1(public_dh: int, public_gamal: int, generator: int, prime: int, r: int, s: int) -> bool:
    # r , s are S1 and S2 in wikipedia algamal signature
    try:
        assert 0 < r < prime, "r not in permissible range"
        assert 0 < s < prime - 1, "s not in permissble range"
    except AssertionError:
        return False
    # to verify then
    # g**m = (public_dh**r * r**s) mod prime (i.e : m = m')
    m = hashlib.sha1(str(public_dh).encode()).hexdigest()
    m = int(m[-1:], 16)
    left = pow(generator, m, prime)  # m
    # print(f"left : {left}")
    right = (pow(public_gamal, r) * pow(r, s)) % prime  # m'
    # print(f"right = {right}")
    # print(f"m: {m}, r: {r}, s: {s} ")
    return True if left == right else False
