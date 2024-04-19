import numpy as np
import hashlib


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
    return hashlib.sha256(str(secret_key).encode()).hexdigest().encode()


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
    return public_dh, r, s


def verify_signature_sha1(public_dh, public_gamal, private_dh, generator, prime, r, s):
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
    return True if left == right else False
