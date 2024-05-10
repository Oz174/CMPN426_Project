import os
print(os.getcwd())

def string_to_binary(s):
    return ''.join(format(c, '08b') for c in s)

def shift_text(text, shift):
    shifted_text = ""
    #shift the bitstream
    for i in range(len(text)):
        shifted_text += text[(i+shift)%len(text)]
    return shifted_text

def binary_to_string(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))


# test
# read the text from the file
text = open("./CTF/CTF-4 (Bit Shifting)/bits.txt", "rb").read()

# convert string text to binary
binary_text = string_to_binary(text)
print(binary_text)

# shift text by k bit to the left
shifted_text = shift_text(binary_text, 1 ) # here ammount of shift k=1
print(shifted_text)

# convert binary text to string
string_text = binary_to_string(shifted_text)
print(string_text)  

