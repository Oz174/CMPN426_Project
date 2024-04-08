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


def al_gamal(prime: int, generator: int, private_key: int):
    """
    Generate the public key for the Al-Gamal key exchange
    param prime: int
    param generator: int
    param private_key: int
    return: int
    """
    public_key = (generator
                  ** private_key) % prime
    return (prime, generator, public_key)
