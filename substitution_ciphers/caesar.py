
"""Used for both encryption and decryption"""
def crypt(ciphertext, key):
    if key > 0:
        return left(ciphertext, key)
    elif key < 0:
        return right(ciphertext, key)
    else:
        return ciphertext


def left(ciphertext, key):
    # Length of text
    length = len(ciphertext)

    plaintext = ""
    for x in range(length):
        letter = ord(ciphertext[x])

        if ((letter >= 65) and (letter <= 90)) or ((letter >= 97) and (letter <= 122)):
            shifted = letter + key

            if (((letter >= 65) and (letter <= 90)) and (shifted > 90)) or (
                    ((letter >= 97) and (letter <= 122)) and (shifted > 122)):
                shifted -= 26

            plaintext += chr(shifted)
        else:
            plaintext += ciphertext[x]

    return plaintext


def right(ciphertext, key):
    # Length of text
    length = len(ciphertext)

    plaintext = ""
    for x in range(length):
        letter = ord(ciphertext[x])

        if ((letter >= 65) and (letter <= 90)) or ((letter >= 97) and (letter <= 122)):
            shifted = letter - key

            if (((letter >= 65) and (letter <= 90)) and (shifted < 65)) or (
                    ((letter >= 97) and (letter <= 122)) and (shifted < 97)):
                shifted += 26

            plaintext += chr(shifted)
        else:
            plaintext += ciphertext[x]

    return plaintext
