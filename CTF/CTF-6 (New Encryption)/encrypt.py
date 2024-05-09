import string

START = ord("a")
CHARSET = string.ascii_lowercase[:16]
END = ord(CHARSET[15])


def encode_b16(plain):
    encoded = ""
    for c in plain:
        binary = "{0:08b}".format(ord(c))
        encoded += (CHARSET[int(binary[:4], 2)] + CHARSET[int(binary[4:], 2)])
    return encoded


# inverse the operation of encoding
# take each two letters , find their index in binary , concat and retrieve original one
def decode_b16(encoded):
    decoded = ""
    for j in range(0, len(encoded), 2):
        binary = "{:04b}".format(CHARSET.find(
            encoded[j])) + "{:04b}".format(CHARSET.find(encoded[j+1]))
        decoded += chr(int(binary, 2))
    return decoded


def caesar_shift(c, k):
    return CHARSET[(ord(c) + ord(k) - 2 * START) % len(CHARSET)]


def caesar_deshift(c, k):
    return CHARSET[((ord(c) - ord(k) - 2 * END) % len(CHARSET))]


flag = "secretkey"
# hint: key is a single letter
key = "j"
b16 = encode_b16(flag)
print(b16)
enc = ""
for i, c in enumerate(b16):
    enc += caesar_shift(c, key[i % len(key)])
print(enc)

dec = ""
for i, c in enumerate(enc):
    dec += caesar_deshift(c, key[i % len(key)])
print(dec)
print(decode_b16(dec))

# 3ayzeen nwsl ll b16 mn el enc
with open('cipher.txt', 'r') as f:
    enc = f.readline()
    # print(enc)

with open('flag.txt', 'w') as f:
    # from hint , K is only one letter
    for key in string.ascii_lowercase:
        dec = ""
        f.write(f"{key} : ")
        for i, c in enumerate(enc):
            dec += caesar_deshift(c, key)
        try:
            f.write(decode_b16(dec))
            f.write("\n")
        except UnicodeEncodeError:
            # if an error arise , skip the letter
            f.write("\n")
