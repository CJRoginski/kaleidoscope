
def create_alphabet(alphabet, key="~"):
    # Set up the base alphabets
    base_alphabet = "ABCDEFGHI"
    if alphabet == "-J":
        base_alphabet += "KLMNOPQRSTUVWXYZ"
    elif alphabet == "-Q":
        base_alphabet += "JKLMNOPRSTUVWXYZ"
    elif alphabet == "-V":
        base_alphabet += "JKLMNOPQRSTUWXYZ"
    elif alphabet == "-W":
        base_alphabet += "JKLMNOPQRSTUVXYZ"
    elif alphabet == "-Z":
        base_alphabet += "JKLMNOPQRSTUVWXY"
    else:
        # Check for custom alphabets
        if len(alphabet) >= 25:
            base_alphabet = alphabet.upper()
        else:
            # In case the custom alphabet is too short, use the -j alphabet
            base_alphabet += "KLMNOPQRSTUVWXYZ"

    # Create a keyed alphabet if there is a key given
    keyed_alphabet = ""
    if key != "~" or key != "":
        for k in range(len(key)):
            char = ord(key[k].upper())

            duplicate = False

            if k > 0:
                for i in range(k):
                    # Check and omit any duplicate letters
                    if key[k].upper() == keyed_alphabet[i]:
                        duplicate = True

                if not duplicate and ((char >= 65) and (char <= 90)):
                    keyed_alphabet += key[k].upper()
            else:
                if (char >= 65) and (char <= 90):
                    keyed_alphabet += key[k].upper()

        # Add the base alphabet onto the end of the key, omitting any duplicate letters
        keyed_length = len(keyed_alphabet)
        for a in range(25):
            duplicate = False

            for i in range(keyed_length):
                # Check and omit any duplicate letters
                if base_alphabet[a] == keyed_alphabet[i]:
                    duplicate = True

            if not duplicate:
                keyed_alphabet += base_alphabet[a]

            # Break if the alphabet will get too long
            if len(keyed_alphabet) == 25:
                break
    else:
        keyed_alphabet = base_alphabet

    return keyed_alphabet


# Put the alphabet into the grid
def create_grid(alphabet):
    grid = [['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', ''],
            ['', '', '', '', '']]

    # Put the alphabet into the grid
    index = 0
    for row in range(5):
        for column in range(5):
            grid[row][column] = alphabet[index]
            index += 1

    return grid


def decrypt(ciphertext, alphabet):
    # Create the grid
    grid = create_grid(alphabet)

    # Format the text and put it into bigrams
    stripped_ciphertext = format_text(ciphertext, alphabet)
    cipher_bigrams = create_bigrams(stripped_ciphertext)

    # Number of bigrams
    num = len(cipher_bigrams)

    plain_bigrams = []
    for i in range(num):
        plain_bigrams.append(algorithm(-1, grid, cipher_bigrams[i]))

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


    # Fully remove padding between double letters
    return plaintext.replace("~", "")


def encrypt(plaintext, alphabet):
    # Create the grid
    grid = create_grid(alphabet)

    # Format the text and put it into bigrams
    stripped_plaintext = format_text(plaintext, alphabet)
    padded_plaintext = pad_doubles(stripped_plaintext, alphabet)
    plain_bigrams = create_bigrams(padded_plaintext)

    # Number of bigrams
    num = len(plain_bigrams)

    cipher_bigrams = []
    for i in range(num):
        cipher_bigrams.append(algorithm(1, grid, plain_bigrams[i]))

    ciphertext = ""
    for i in range(num):
        for p in range(2):
            ciphertext += cipher_bigrams[i][p]

    return ciphertext


# process = -1 is decryption
# process = 1 is encryption
def algorithm(process, grid, bigram):
    index_a = find_letter(grid, bigram[0])
    a_row = index_a[0]
    a_column = index_a[1]

    index_b = find_letter(grid, bigram[1])
    b_row = index_b[0]
    b_column = index_b[1]

    # If the letters are in the same row
    shifted_a = [a_row, a_column]
    shifted_b = [b_row, b_column]
    if index_a[0] == index_b[0]:
        shifted_a[1] = (a_column + process) % 5

        shifted_b[1] = (b_column + process) % 5
    elif index_a[1] == index_b[1]:
        shifted_a[0] = (a_row + process) % 5

        shifted_b[0] = (b_row + process) % 5
    else:
        shifted_a[1] = b_column

        shifted_b[1] = a_column

    return [grid[shifted_a[0]][shifted_a[1]], grid[shifted_b[0]][shifted_b[1]]]

# Find a letter in the grid
def find_letter(grid, char):
    index = [0, 0]

    for row in range(5):
        for column in range(5):
            if grid[row][column] == char:
                index[0] = row
                index[1] = column

    return index

def format_text(text, alphabet):
    # Length of text
    length = len(text)

    # Remove all non-letter characters and make all letters capital
    formatted_text = ""
    for i in range(length):
        char = ord(text[i].upper())

        if (char >= 65) and (char <= 90):
            if text[i].upper() not in alphabet:
                if "J" not in alphabet:
                    formatted_text += "I"
                elif "V" not in alphabet:
                    formatted_text += "W"
                elif "W" not in alphabet:
                    formatted_text += "V"
                else:
                    formatted_text += "X"
            else:
                formatted_text += text[i].upper()

    return formatted_text


# Add padding in between double letters
def pad_doubles(text, alphabet):
    # Length of text
    length = len(text)

    # Loop through the text to find double letters
    formatted_text = ""
    for i in range(length):
        if len(formatted_text) < 1:
            formatted_text += text[i]
        else:
            if formatted_text.endswith(text[i]):
                if text[i] == "X":
                    if "Q" in alphabet:
                        formatted_text += "Q" + text[i]
                    else:
                        formatted_text += "Y" + text[i]
                else:
                    formatted_text += "X" + text[i]
            else:
                formatted_text += text[i]

    new_length = len(formatted_text)

    if (new_length % 2) != 0:
        if formatted_text.endswith("X"):
            if "Q" in alphabet:
                formatted_text += "Q"
            else:
                formatted_text += "Y"
        else:
            formatted_text += "X"

        new_length += 1

    return formatted_text


# Separate the formatted text into bigrams
def create_bigrams(text):
    bigrams = []
    for index in range(0, len(text), 2):
        bigrams.append([text[index], text[index + 1]])

    return bigrams


def print_grid(grid):
    for row in range(5):
        for column in range(5):
            print(grid[row][column], end=" ")
        print()
    print()
