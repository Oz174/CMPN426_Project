import numpy as np


def deffie_hellman(prime: int, generator: int, private_key: int) -> int:
    """
    Generate the public key for the Diffie-Hellman key exchange
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


def secret_key_from_dh(prime: int, public_key: int, private_key: int) -> int:
    """
    Generate the secret key for the Diffie-Hellman key exchange
    param prime: int
    param public_key: int
    param private_key: int
    return: int
    """
    # the secret key is the public key raised to the power of the private key modulo the prime number
    secret_key = (public_key
                  ** private_key) % prime
    return secret_key


def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_euclidean(b % a, a)
        return g, y - (b // a) * x, x


def send_signature(public_dh, public_gamal, generator, prime):
    if public_dh >= prime:
        return None
    # generate random K
    k = np.random.randint(2, prime-1)
    # calculate K
    key = pow(public_gamal, k, prime)
    c1 = pow(generator, k, prime)
    c2 = (key*public_dh) % prime
    return c1, c2


def verify_signature(public_dh, private_gamal, prime, C1, C2):
    key = pow(C1, private_gamal, prime)
    if public_dh == (C2 * extended_euclidean(key, prime)[1]) % prime:
        return True
    return False
