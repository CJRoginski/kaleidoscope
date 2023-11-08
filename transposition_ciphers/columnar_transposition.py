import math


def encrypt(plaintext, key):
    # Length of text
    length = len(plaintext)
    # Length of key
    key_length = len(key)

    blocks = math.ceil(length / key_length)

    # Put plaintext into an array with a row length the same as the key length
    index = 0
    pre_text = []
    for row in range(blocks):
        pre_text.append([])

        for col in range(key_length):
            if index < length:
                pre_text[row].append(plaintext[index].upper())

                index += 1
            else:
                # Add padding to the end if needed
                pre_text[row].append("X")

    # Permutate the columns
    ciphertext = ""
    for i in range(key_length):
        column = key[i] - 1

        for row in range(blocks):
            ciphertext += pre_text[row][column]

    return ciphertext
