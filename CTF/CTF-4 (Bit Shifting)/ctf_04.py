def shift_circular_shemal(string, num_shifts):
    return string[num_shifts-1:] + string[:num_shifts]


if __name__ == "__main__":

    with open('bits.txt', 'rb') as file:
        text = file.readline()

    text_file_all_binary = ''
    for letter in text:
        text_file_all_binary += '{0:08b}'.format(letter)

    for i in range(2, 3):
        shifted = shift_circular_shemal(text_file_all_binary, i)
    try:
        shifted = [chr(int(shifted[j:j+8], 2))
                   for j in range(0, len(shifted), 8)]
        with open("flag.txt", "w") as f:
            f.write(''.join(shifted))
            f.write("\n")
    except ValueError:
        pass
