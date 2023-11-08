import math

from substitution_ciphers import playfair
from transposition_ciphers import columnar_transposition as rotate


# For looping purposes, here are the coordinates for the spirals
# Breaks indicate a 90-degree turn
spirals = {
    "inward": {
        "clockwise": {
            "top-left": {
                "index": [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
                          [1, 4], [2, 4], [3, 4], [4, 4],
                          [4, 3], [4, 2], [4, 1], [4, 0],
                          [3, 0], [2, 0], [1, 0],
                          [1, 1], [1, 2], [1, 3],
                          [2, 3], [3, 3],
                          [3, 2], [3, 1],
                          [2, 1],
                          [2, 2]],
                "visual": [['\u2b58\u2500', '\u2192\u2500', '\u2500\u2500', '\u2500\u2500', '\u2500\u2510'],
                           ['\u250c\u2500', '\u2500\u2500', '\u2500\u2500', '\u2500\u2510', ' \u2502'],
                           ['\u2502 ', '\u250c\u2500', '\u2500x', ' \u2502', ' \u2502'],
                           ['\u2502 ', '\u2514\u2500', '\u2500\u2500', '\u2500\u2518', ' \u2502'],
                           ['\u2514\u2500', '\u2500\u2500', '\u2500\u2500', '\u2500\u2500', '\u2500\u2518']]
            },
            "top-right": {
                "index": [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4],
                          [4, 3], [4, 2], [4, 1], [4, 0],
                          [3, 0], [2, 0], [1, 0], [0, 0],
                          [0, 1], [0, 2], [0, 3],
                          [1, 3], [2, 3], [3, 3],
                          [3, 2], [3, 1],
                          [2, 1], [1, 1],
                          [1, 2],
                          [2, 2]],
                "visual": [['\u250c\u2500', '\u2500\u2500', '\u2500\u2500', '\u2500\u2510', ' \u2b58'],
                           ['\u2502 ', '\u250c\u2500', '\u2500\u2510', ' \u2502', ' \u2193'],
                           ['\u2502 ', '\u2502 ', ' x', ' \u2502', ' \u2502'],
                           ['\u2502 ', '\u2514\u2500', '\u2500\u2500', '\u2500\u2518', ' \u2502'],
                           ['\u2514\u2500', '\u2500\u2500', '\u2500\u2500', '\u2500\u2500', '\u2500\u2518']]
            },
            "bottom-right": {
                "index": [[4, 4], [4, 3], [4, 2], [4, 1], [4, 0],
                          [3, 0], [2, 0], [1, 0], [0, 0],
                          [0, 1], [0, 2], [0, 3], [0, 4],
                          [1, 4], [2, 4], [3, 4],
                          [3, 3], [3, 2], [3, 1],
                          [2, 1], [1, 1],
                          [1, 2], [1, 3],
                          [2, 3],
                          [2, 2]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', 'x', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '\u2b58']]
            },
            "bottom-left": {
                "index": [[4, 0], [3, 0], [2, 0], [1, 0], [0, 0],
                          [0, 1], [0, 2], [0, 3], [0, 4],
                          [1, 4], [2, 4], [3, 4], [4, 4],
                          [4, 3], [4, 2], [4, 1],
                          [3, 1], [2, 1], [1, 1],
                          [1, 2], [1, 3],
                          [2, 3], [3, 3],
                          [3, 2],
                          [2, 2]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', 'x', '', ''],
                           ['', '', '', '', ''],
                           ['\u2b58', '', '', '', '']]
            }
        },
        "counter-clockwise": {
            "top-left": {
                "index": [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0],
                          [4, 1], [4, 2], [4, 3], [4, 4],
                          [3, 4], [2, 4], [1, 4], [0, 4],
                          [0, 3], [0, 2], [0, 1],
                          [1, 1], [2, 1], [3, 1],
                          [3, 2], [3, 3],
                          [2, 3], [1, 3],
                          [1, 2],
                          [2, 2]],
                "visual": [['\u2b58', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', 'x', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
            "top-right": {
                "index": [[0, 4], [0, 3], [0, 2], [0, 1], [0, 0],
                          [1, 0], [2, 0], [3, 0], [4, 0],
                          [4, 1], [4, 2], [4, 3], [4, 4],
                          [3, 4], [2, 4], [1, 4],
                          [1, 3], [1, 2], [1, 1],
                          [2, 1], [3, 1],
                          [3, 2], [3, 3],
                          [2, 3],
                          [2, 2]],
                "visual": [['', '', '', '', '\u2b58'],
                           ['', '', '', '', ''],
                           ['', '', 'x', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
            "bottom-right": {
                "index": [[4, 4], [3, 4], [2, 4], [1, 4], [0, 4],
                          [0, 3], [0, 2], [0, 1], [0, 0],
                          [1, 0], [2, 0], [3, 0], [4, 0],
                          [4, 1], [4, 2], [4, 3],
                          [3, 3], [2, 3], [1, 3],
                          [1, 2], [1, 1],
                          [2, 1], [3, 1],
                          [3, 2],
                          [2, 2]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', 'x', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '\u2b58']]
            },
            "bottom-left": {
                "index": [[4, 0], [4, 1], [4, 2], [4, 3], [4, 4],
                          [3, 4], [2, 4], [1, 4], [0, 4],
                          [0, 3], [0, 2], [0, 1], [0, 0],
                          [1, 0], [2, 0], [3, 0],
                          [3, 1], [3, 2], [3, 3],
                          [2, 3], [1, 3],
                          [1, 2], [1, 1],
                          [2, 1],
                          [2, 2]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', 'x', '', ''],
                           ['', '', '', '', ''],
                           ['\u2b58', '', '', '', '']]
            }
        }
    },
    "outward": {
        "clockwise": {
            "right": {
                "index": [[2, 2], [2, 3],
                          [3, 3],
                          [3, 2], [3, 1],
                          [2, 1], [1, 1],
                          [1, 2], [1, 3], [1, 4],
                          [2, 4], [3, 4], [4, 4],
                          [4, 3], [4, 2], [4, 1], [4, 0],
                          [3, 0], [2, 0], [1, 0], [0, 0],
                          [0, 1], [0, 2], [0, 3], [0, 4]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '\u2b58', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
            "bottom": {
                "index": [[2, 2], [3, 2],
                          [3, 1],
                          [2, 1], [1, 1],
                          [1, 2], [1, 3],
                          [2, 3], [3, 3], [4, 3],
                          [4, 2], [4, 1], [4, 0],
                          [3, 0], [2, 0], [1, 0], [0, 0],
                          [0, 1], [0, 2], [0, 3], [0, 4],
                          [1, 4], [2, 4], [3, 4], [4, 4]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '\u2b58', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
            "left": {
                "index": [[2, 2], [2, 1],
                          [1, 1],
                          [1, 2], [1, 3],
                          [2, 3], [3, 3],
                          [3, 2], [3, 1], [3, 0],
                          [2, 0], [1, 0], [0, 0],
                          [0, 1], [0, 2], [0, 3], [0, 4],
                          [1, 4], [2, 4], [3, 4], [4, 4],
                          [4, 3], [4, 2], [4, 1], [4, 0]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '\u2b58', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
            "up": {
                "index": [[2, 2], [1, 2],
                          [1, 3],
                          [2, 3], [3, 3],
                          [3, 2], [3, 1],
                          [2, 1], [1, 1], [0, 1],
                          [0, 2], [0, 3], [0, 4],
                          [1, 4], [2, 4], [3, 4], [4, 4],
                          [4, 3], [4, 2], [4, 1], [4, 0],
                          [3, 0], [2, 0], [1, 0], [0, 0]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '\u2b58', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
        },
        "counter-clockwise": {
            "right": {
                "index": [[2, 2], [2, 3],
                          [1, 3],
                          [1, 2], [1, 1],
                          [2, 1], [3, 1],
                          [3, 2], [3, 3], [3, 4],
                          [2, 4], [1, 4], [0, 4],
                          [0, 3], [0, 2], [0, 1], [0, 0],
                          [1, 0], [2, 0], [3, 0], [4, 0],
                          [4, 1], [4, 2], [4, 3], [4, 4]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '\u2b58', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
            "bottom": {
                "index": [[2, 2], [3, 2],
                          [3, 3],
                          [2, 3], [1, 3],
                          [1, 2], [1, 1],
                          [2, 1], [3, 1], [4, 1],
                          [4, 2], [4, 3], [4, 4],
                          [3, 4], [2, 4], [1, 4], [0, 4],
                          [0, 3], [0, 2], [0, 1], [0, 0],
                          [1, 0], [2, 0], [3, 0], [4, 0]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '\u2b58', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
            "left": {
                "index": [[2, 2], [2, 1],
                          [3, 1],
                          [3, 2], [3, 3],
                          [2, 3], [1, 3],
                          [1, 2], [1, 1], [1, 0],
                          [2, 0], [3, 0], [4, 0],
                          [4, 1], [4, 2], [4, 3], [4, 4],
                          [3, 4], [2, 4], [1, 4], [0, 4],
                          [0, 3], [0, 2], [0, 1], [0, 0]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '\u2b58', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            },
            "up": {
                "index": [[2, 2], [1, 2],
                          [1, 1],
                          [2, 1], [3, 1],
                          [3, 2], [3, 3],
                          [2, 3], [1, 3], [0, 3],
                          [0, 2], [0, 1], [0, 0],
                          [1, 0], [2, 0], [3, 0], [4, 0],
                          [4, 1], [4, 2], [4, 3], [4, 4],
                          [3, 4], [2, 4], [1, 4], [0, 4]],
                "visual": [['', '', '', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '\u2b58', '', ''],
                           ['', '', '', '', ''],
                           ['', '', '', '', '']]
            }
        }
    }
}


def decrypt(ciphertext, alphabet, omitted, key, direction, flow, start, showProcess=False):
    # Format the text and put it into bigrams
    stripped_ciphertext = playfair.format_text(ciphertext, alphabet)
    cipher_bigrams = playfair.create_bigrams(stripped_ciphertext)

    # Format the key
    extended_key = generate_key(stripped_ciphertext, key, flow)

    # Number of bigrams
    num = len(cipher_bigrams)

    plain_bigrams = []
    for i in range(num):
        # Create the shifted grid
        grid = playfair.create_grid(spiral_shift(alphabet, omitted, extended_key[i], direction, flow, start))
        # playfair.print_grid(grid)

        plain_bigrams.append(playfair.algorithm(-1, grid, cipher_bigrams[i]))

    plaintext = ""
    for i in range(num):
        for p in range(2):
            plaintext += plain_bigrams[i][p]

        length = len(plaintext)
        if (i + 1) != num:
            # Remove padding between double letters
            if (plaintext.endswith("X") or plaintext.endswith("Q") or plaintext.endswith("Y")) and (
                    plaintext[length - 2] == plain_bigrams[i + 1][0]):
                    # and (stripped_ciphertext[length - 2] == stripped_ciphertext[length]):
                # Placeholder to better remove the padding
                plaintext = plaintext[:(length - 1)]
                plaintext += "~"

    if showProcess:
        print("   PROCESS:")
        print("     c: ", end="")
        for i in range(len(cipher_bigrams)):
            print(cipher_bigrams[i][0] + cipher_bigrams[i][1], end=" ")
        print("\n     k: ", end="")
        for j in range(len(extended_key)):
            print(extended_key[j], end="  ")
        print("\n     p: ", end="")
        for i in range(len(plain_bigrams)):
            print(plain_bigrams[i][0] + plain_bigrams[i][1], end=" ")
        print("\n")

    # Fully remove padding between double letters
    return plaintext.replace("~", "")


def encrypt(plaintext, alphabet, omitted, key, direction, flow, start, showProcess=False):
    # Format the text and put it into bigrams
    stripped_plaintext = playfair.format_text(plaintext, alphabet)
    padded_plaintext = playfair.pad_doubles(stripped_plaintext, alphabet)
    plain_bigrams = playfair.create_bigrams(padded_plaintext)

    # Format the key
    extended_key = generate_key(padded_plaintext, key, flow)

    # Number of bigrams
    num = len(plain_bigrams)

    cipher_bigrams = []
    for i in range(num):
        # Create the shifted grid
        grid = playfair.create_grid(spiral_shift(alphabet, omitted, extended_key[i], direction, flow, start))
        # playfair.print_grid(grid)

        cipher_bigrams.append(playfair.algorithm(1, grid, plain_bigrams[i]))

    ciphertext = ""
    for i in range(num):
        for p in range(2):
            ciphertext += cipher_bigrams[i][p]

    if showProcess:
        print("   PROCESS:")
        print("     p: ", end="")
        for i in range(len(plain_bigrams)):
            print(plain_bigrams[i][0] + plain_bigrams[i][1], end=" ")
        print("\n     k: ", end="")
        for j in range(len(extended_key)):
            print(extended_key[j], end="  ")
        print("\n     c: ", end="")
        for i in range(len(cipher_bigrams)):
            print(cipher_bigrams[i][0] + cipher_bigrams[i][1], end=" ")
        print("\n")

    return ciphertext


# Shift the alphabet in a spiral in its grid
def spiral_shift(alphabet, omitted, key, direction, flow, start):
    original_grid = playfair.create_grid(alphabet)
    spiral_grid = [['', '', '', '', ''],
                   ['', '', '', '', ''],
                   ['', '', '', '', ''],
                   ['', '', '', '', ''],
                   ['', '', '', '', '']]

    char = ord(key.upper())

    shift = char - 65
    if ord(omitted[1].upper()) <= char:
        shift -= 1

    for i in range(25):
        old_index = spirals[direction][flow][start]["index"][i]
        new_index = spirals[direction][flow][start]["index"][(i + shift) % 25]

        spiral_grid[new_index[0]][new_index[1]] = original_grid[old_index[0]][old_index[1]]

    # Put a grid into an alphabet
    alphabet = ""

    for row in range(5):
        for column in range(5):
            alphabet += spiral_grid[row][column]

    return alphabet


# Print a visual diagram of what the spiral looks like
def generate_key(text, key, flow):
    # Length of text
    length = int(len(text) / 2)
    # Length of key
    key_length = len(key)

    # How many times the key will repeat (rounding up to account for the key not fully repeating)
    num_key_blocks = math.ceil(length / key_length)

    # Current transposition values of the key
    current_order = []
    for i in range(key_length):
        current_order.append(i + 1)

    # Repeat the key to cover the length of the entire text
    extended_key = ""
    for i in range(num_key_blocks):
        k = key.upper()
        extended_key += rotate.encrypt(k, current_order)

        # Transpose the key for next time
        if flow == "clockwise":
            current_order.insert(0, current_order[key_length - 1])
            current_order.pop()
        elif flow == "counter-clockwise":
            current_order.append(current_order[0])
            current_order.pop(0)

    final_key = extended_key[:length]

    return final_key



# Print a visual diagram of what the spiral looks like
def print_spiral(direction, flow, start):
    for i in range(5):
        for j in range(5):
            print(spirals[direction][flow][start]["visual"][i][j], end="")
        print()
