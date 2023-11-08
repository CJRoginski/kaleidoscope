
from substitution_ciphers import caesar as shift

def decrypt(ciphertext, key):
    # Length of text
    length = len(ciphertext)
    # Length of key
    key_length = len(key)

    plaintext = ""
    current_keyindex = 0
    for i in range(length):
        char = ord(ciphertext[i])

        if ((char >= 65) and (char <= 90)) or ((char >= 97) and (char <= 122)):
            plaintext += shift.right(ciphertext[i], (ord(key[current_keyindex].casefold()) - 97))

            current_keyindex += 1
            if current_keyindex >= key_length:
                current_keyindex = 0
        else:
            plaintext += ciphertext[i]

    return plaintext

def encrypt(plaintext, key):
    # Length of text
    length = len(plaintext)
    # Length of key
    key_length = len(key)

    ciphertext = ""
    current_keyindex = 0
    for i in range(length):
        char = ord(plaintext[i])

        if ((char >= 65) and (char <= 90)) or ((char >= 97) and (char <= 122)):
            ciphertext += shift.left(plaintext[i], (ord(key[current_keyindex].casefold()) - 97))

            current_keyindex += 1
            if current_keyindex >= key_length:
                current_keyindex = 0
        else:
            ciphertext += plaintext[i]

    return ciphertext

