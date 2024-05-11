# find the flag in encrypted.txt
# encrypted.txt is a file with a long string of characters
# The flag is encrypted with a simple substitution cipher
# The key is in the form of a dictionary

def get_letters_frequency(file):
    with open(file, 'r') as f:
        encrypted = f.read()
    # count the frequency of each letter in the encrypted text
    frequency = {}
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        frequency[char] = encrypted.count(char)
    # sort on values
    frequency = dict(
        sorted(frequency.items(), key=lambda item: item[1], reverse=True))
    return frequency


def find_flag(file):
    """
    Frequency analysis
    {'I': 683, 'K': 518, 'P': 436, 'E': 419, 'H': 361, 'R': 347, 'M': 343, 'V': 322,
    'B': 281, 'C': 261, 'O': 257, 'Y': 154, 'X': 131, 'N': 116, 'S': 114, 'A': 111,
    'T': 91, 'W': 89, 'G': 87, 'U': 83, 'L': 66, 'Q': 40, 'D': 5, 'J': 3, 'Z': 3, 'F': 2}
    """
    with open(file, 'r') as f:
        encrypted = f.read()
    flag = ''
    key = {'I': 'E', 'K': 'T', 'P': 'O', 'E': 'A', 'V': 'S',
           'X': 'U', 'Y': 'W', 'M': 'N', 'O': 'D', 'B': 'R',
           'R': 'I', 'S': 'G', 'C': 'L', 'A': 'C', 'T': 'B',
           'Q': 'V', 'G': 'P', 'W': 'Y', 'L': 'K', 'N': 'F',
           'U': 'M', 'D': 'D', 'Z': 'Z', 'J': 'X', 'F': 'Q', 'H': 'H'}
    for char in encrypted:
        # if the car is a space or newline character, add it to the flag
        if char in [' ', '\n', ',', '.', "'", '"', '!', '?', ':', ';', '-']:
            flag += char
        elif char.isdigit():
            flag += char
        else:
            flag += key[char]
    return flag


def write_flag_to_file(file, flag):
    # delete file if it exists
    import os
    if os.path.exists(file):
        os.remove(file)
    with open(f"{file}.txt", 'w') as f:
        f.write(flag)


if __name__ == '__main__':
    flag = find_flag('Substitution.txt')
    write_flag_to_file('sub_ctflearn', flag)
