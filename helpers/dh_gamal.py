import numpy as np
import hashlib


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


# def extended_euclidean(a, b):
#     if a == 0:
#         return b, 0, 1
#     else:
#         g, x, y = extended_euclidean(b % a, a)
#         return g, y - (b // a) * x, x


# def send_signature(public_dh, public_gamal, generator, prime):
#     if public_dh >= prime:
#         return None
#     # generate random K
#     k = np.random.randint(2, prime-1)
#     # calculate K
#     key = pow(public_gamal, k, prime)
#     c1 = pow(generator, k, prime)
#     c2 = (key*public_dh) % prime
#     return c1, c2


# def verify_signature(public_dh, private_gamal, prime, C1, C2):
#     key = pow(C1, private_gamal, prime)
#     if public_dh == (C2 * extended_euclidean(key, prime)[1]) % prime:
#         return True
#     return False

def gcd(num1, num2):
    assert num1 > num2, "First Number should be greater"
    _, r = divmod(num1, num2)
    return num2 if r == 0 else gcd(num2, r)


def generate_random_k(prime):
    k = np.random.randint(2, prime-2)
    while gcd(prime-1, k) != 1:
        k = np.random.randint(2, prime-2)
    return k


def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_euclidean(b % a, a)
        return g, y - (b // a) * x, x


def send_signature_sha1(public_dh, private_gamal, generator, prime):
    m = hashlib.sha1(str(public_dh).encode()).hexdigest()
    # take last 8 bits
    m = int(m[-1:], 16)
    assert 0 < m < prime, "m doesn't satisfy the condition 0 < m < prime"
    # generate random K

    r, s = 0, 0  # in the unlikely event of s = 0 , you will have to regenerate the k
    while s == 0:
        k = generate_random_k(prime)
        r = pow(generator, k, prime)
        s = (m - private_gamal*r) * \
            extended_euclidean(k, prime-1)[1] % (prime-1)
    # print(f"m: {m}, r: {r}, s: {s} , k: {k} ")
    return r, s


def verify_signature_sha1(public_dh, public_gamal, generator, prime, r, s):
    assert 0 < r < prime, "r not in permissible range"
    assert 0 < s < prime - 1, "s not in permissble range"
    # to verify then
    # g**m = (public_dh**r * r**s) mod prime
    m = hashlib.sha1(str(public_dh).encode()).hexdigest()
    m = int(m[-1:], 16)
    left = pow(generator, m, prime)
    # print(f"left : {left}")
    right = (pow(public_gamal, r) * pow(r, s)) % prime
    # print(f"right = {right}")
    # print(f"m: {m}, r: {r}, s: {s} ")
    return left == right
