
import cv2
import numpy as np
from prime import generate_prime, generate_key
from helper_RSA import *

# Load the image
image = cv2.imread("image.png", flags=cv2.IMREAD_GRAYSCALE)
# Convert image to 1D list
plaintext = image.flatten().tolist()

print("Plain Text: ", plaintext)
# Convert plaintext to grey scale image
cv2.imshow("Source image", np.array(plaintext).reshape(64, 64).astype(np.uint8))
# Save source image as source.png
cv2.imwrite("RSAoutput/source.png", np.array(plaintext).reshape(64, 64).astype(np.uint8))
cv2.waitKey(0)

# Key/ message packet length in bytes
n = 2

# Generate random prime numbers of n bytes
p = generate_prime(n*8)
q = generate_prime(n*8)

phi = (p-1)*(q-1)

# Generate public and private keys
e, d = generate_key(phi)
public_key = (e, p*q)
private_key = (d, p*q)

# Convert plaintext to list of n-bit blocks
blocks = to_blocks(plaintext, n)

cipherText = []

def encrypt(blocks, public_key):
    for block in blocks:
        # Encrypt block
        block = expmod(block, public_key[0], public_key[1])
        cipherText.append(block)

encrypt(blocks, public_key)

# 1 dimensional list of cipher text in hex values
cipherText = from_blocks(cipherText)

print("\n\nCipher Text: ", cipherText)
# Convert cipher text to grey scale image
cv2.imshow("Encrypted image", np.array(cipherText).reshape(64, 64).astype(np.uint8))
# Save encrypted image as encrypted.png
cv2.imwrite("RSAoutput/encrypted.png", np.array(cipherText).reshape(64, 64).astype(np.uint8))
cv2.waitKey(0)

blocks = to_blocks(cipherText, n)

decryptedText = []

def decrypt(blocks, private_key):
    for block in blocks:
        # Decrypt block
        block = expmod(block, private_key[0], private_key[1])
        decryptedText.append(block)

decrypt(blocks, private_key)

# 1 dimensional list of decrypted text in hex values
decryptedText = from_blocks(decryptedText)

print("\n\nDecrypted Text", decryptedText)
# Convert decrypted text to grey scale image
cv2.imshow("Decrypted image", np.array(decryptedText).reshape(64, 64).astype(np.uint8))
# Save decrypted image as decrypted.png
cv2.imwrite("RSAoutput/decrypted.png", np.array(decryptedText).reshape(64, 64).astype(np.uint8))
cv2.waitKey(0)

print("Are the original and decrypted images same? ", plaintext == decryptedText)