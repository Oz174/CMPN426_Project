# CTF Problems Approaches

## CTF - 1 (Cryptanalysis)

    1. Letters statistics 
    2. bigrams and trigrams statistics (tracing words like the , of , so)
    3. The rest of letters came by trials and errors by looking to deciphered text at each iteration

## CTF - 2 (Packet Analysis)

    1. Opened the .pcapng file in Wireshark App for packet analysis
    2. Filtered all the data coming from http protocols 
    3. Filtered the text/plaintext files till found something looked like flag structure but encrypted
    4. Used Online ROT-14 deciphering to get the flag as shown

## CTF - 3

    1. Read the images , view the pixel values 
    2. By Observation , You can find the summation of corresponding to 255
    3. Add the two images and the flag was there as shown

## CTF - 4

    1. Each ascii letter is represented in 8 bits , so brute-force circular shifts (right and left) was made for every 8 bits 
    *but some letters weren't clear enough , but it was enough to know that left circular shift is used* 
    2. We circle left shifted the whole bitstream of the text by 1 and Voila ! 

## CTF - 5

    1. Used Powershell commands that looks for string inside a text , used the pattern : ctf

## CTF - 6

    1. Traced the encoding of the flag using , Traced the ciphering shift 
    2. Created their reverse operation 
        a. For the b16_decode function , concatenated the binary indices of each two letters back to original letter 
        b. For the decipher , I minused the shift and used the end letter of the charset instead of start and it worked 
    3. Brute forcing the one letter key (as mentioned in the hint) to get the encoded flag , then decoding the flag to get the original text
    4. Two letters give the same answer 

## CTF - 7

    1. Up till now , Using file analysis we notice there's an audio file embedded

## CTF - 8

    1. Used Morse Code Audio Decoder online to get the key (RUSSIAN)
    2. Used Hex Editor for the audio file to get the keyword (POLYBIUS) and cipher text and cipher method (Nhilist)
    3. Used an online Nhilist decoder with the alphabet (looks like playfair matrix construction) and provided the ciphertext letters provided in the hex-file 
    4. The letter is represented by concatenation of row_index and col_index 
        So for example, Letter R with index [2,3] is 23 
    5. Deciphering is just subtracting the key value from cipher value then map the result back to the matrix to get original letter
