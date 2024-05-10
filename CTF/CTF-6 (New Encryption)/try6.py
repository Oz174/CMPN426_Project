import string

START = ord("a")
CHARSET = string.ascii_lowercase[:16]
# print(CHARSET)

def encode_b16(plain):
    encoded = ""
    for c in plain:
        binary = "{0:08b}".format(ord(c))
        encoded += (CHARSET[int(binary[:4], 2)] + CHARSET[int(binary[4:], 2)])
    return encoded

def decode_b16(encoded):
    decode=""
    for i in range(0,len(encoded),2):
        c1=CHARSET.index(encoded[i])
        b1="{0:04b}".format(c1)
        c2=CHARSET.index(encoded[i+1])
        b2="{0:04b}".format(c2)
        concat=b1+b2
        decode+=chr(int(concat,2))
    return decode

def caesar_shift(c, k):
    # print(ord(c))
    # print(ord(k))
    # print(ord(c) + ord(k) - 2 * START)
    # print((ord(c) + ord(k) - 2 * START) % len(CHARSET))
    return CHARSET[(ord(c) + ord(k) - 2 * START) % len(CHARSET)]

def reverse_ceaser(c,k):
    return CHARSET[(ord(c)-ord(k))%len(CHARSET)]

# simple plaintext trial
flag = "secretkey"
# hint: key is a single letter
key = "s"

# encode the plaintext
b16 = encode_b16(flag)
print(b16)

# encrypt the encoded 
enc = ""
for i, c in enumerate(b16):
    enc += caesar_shift(c, key[i % len(key)])
print(enc)

# decrypt the ciphertext
decipher=""
for i, c in enumerate(enc):
   decipher+=reverse_ceaser(c,key[i % len(key)])
print(decipher)

#decode the deciphered
flagy = decode_b16(decipher)
print(flagy)

print("\n=========================================\n")
# now we want to test having a ciphertext and trying to get the original message
# read cipher text
encrypted ="jikmkjgekjkckjkbknkjlhgekflgkjgekbkfkpknkcklgekfgekbkdlkkjgcgejlkjgekckjkjkigelikdgekfkhligekkkflhligc"

# try each letter in the alphabet
for key in string.ascii_lowercase:
    print("key is : ",key)
    # decipher the encrypted message
    deciphered=""
    for i, c in enumerate(encrypted):
        deciphered+=reverse_ceaser(c,key)
    # decode 
    print(deciphered)
    decoded=decode_b16(deciphered)
    print(decoded)
    print("===")


    
