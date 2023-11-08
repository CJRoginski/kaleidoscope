
from created_ciphers import kaleidoscope
from substitution_ciphers import playfair

omitted_char = "-J"
alphabet = playfair.create_alphabet(omitted_char)
print("ALPHABET:\n   " + alphabet + "")
direction = "inward"
flow = "clockwise"
start = "top-left"
print("SPIRAL:\n   " + direction + ", " + flow + ", " + start)
# print("ALPHABET:\n   " + alphabet + "\nGRID:")
# grid = playfair.create_grid(alphabet)
# playfair.print_grid(grid)

key = "FIREFLY"
print("KEY:\n   " + key + "")

plaintext = "Happiness can be found even in the darkest of times, when one only remembers to turn off the light."
print("PLAINTEXT:\n   " + plaintext + "\n   " + playfair.format_text(plaintext, alphabet) + "\n")

# ciphertext = playfair.encrypt(plaintext, alphabet)
ciphertext = kaleidoscope.encrypt(plaintext, alphabet, omitted_char, key, direction, flow, start, True)
print("CIPHERTEXT:\n   " + ciphertext + "\n")

plaintext_2 = kaleidoscope.decrypt(ciphertext, alphabet, omitted_char, key, direction, flow, start, True)
print("PLAINTEXT:\n   " + plaintext_2 + "\n")

showGrids = False

if showGrids:
    for i in range(25):
        num = i + 65
        if num >= 74:
            num += 1
        char = chr(num)

        shifted_alphabet_1 = kaleidoscope.spiral_shift(alphabet, omitted_char, char, "inward", "clockwise", "top-left")
        print(char + " GRID:")
        shifted_grid_1 = playfair.create_grid(shifted_alphabet_1)
        playfair.print_grid(shifted_grid_1)
