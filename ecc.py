
import cv2
import numpy as np
import random
from tinyec import registry as reg
from helper_ECC import *

# Load the image
image = cv2.imread("image.png", flags=cv2.IMREAD_GRAYSCALE)
# Convert image to 1D list
plaintext = image.flatten().tolist()

print("Plain Text: ", plaintext)
# Convert plaintext to grey scale image
cv2.imshow("Source image", np.array(plaintext).reshape(64, 64).astype(np.uint8))
# Save source image as source.png
cv2.imwrite("ECCoutput/source.png", np.array(plaintext).reshape(64, 64).astype(np.uint8))
cv2.waitKey(0)

# Getting parameters of secp192r1 curve from tinyec library
curve = reg.get_curve("secp192r1")
p = curve.field.p 
a = curve.a
b = curve.b
# Default generator point and its order
generator_point = curve.g
order = curve.field.n

# Number of bytes in each block
n = 16

# Generate public and private keys
private_key = random.randint(1, order)
public_key = private_key * generator_point

# print("Private key: ", private_key)
# print("Public key: ", public_key)

# Convert plaintext to list of n-bit blocks
blocks = to_blocks(plaintext, n)

cipherText = []

def get_point(x):
    # Get point on curve for given (16-byte) integer message x
    y = (expmod(x, 3, p) + a * x + b) % p
    y = sqrt(y, p)
    if y == -1:
        return None
    return (x, y)

def encrypt(blocks, public_key):
    for block in blocks:
        # Get point on curve for given (16-byte) integer message x
        bl = block<<32
        # print("Size of b: ",b.bit_length())
        while get_point(bl) is None:
            bl += 1
            if bl >= (1<<160):
                bl = -1
                break
        (x, y) = get_point(bl)
        message = generator_point
        message.x, message.y = x, y
        if bl == -1:
            # print("No point found for block: ", block)
            continue
        k = random.randint(1, order)
        # Encrypt block
        encrypted_block = [k * generator_point, k * public_key + message]
        cipherText.append(encrypted_block)

encrypt(blocks, public_key)

# 1 dimensional list of cipher text in hex values
ct = [item[0].x >> 32 for item in cipherText] 
ct = from_blocks(ct)

print("\n\nCipher Text: ", ct)
# Convert cipher text to grey scale image
cv2.imshow("Encrypted image", np.array(ct).reshape(64, 64).astype(np.uint8))
# Save encrypted image as encrypted.png
cv2.imwrite("ECCoutput/encrypted.png", np.array(ct).reshape(64, 64).astype(np.uint8))
cv2.waitKey(0)

blocks = cipherText
decryptedText = []

def decrypt(blocks, private_key):
    for block in blocks:
        # Decrypt block
        decrypted_block = block[1] - private_key * block[0]
        decryptedText.append((decrypted_block.x) >> 32)

decrypt(blocks, private_key)

# print("\n\n Size of decrypted text: ", len(decryptedText))

# 1 dimensional list of decrypted text in hex values
decryptedText = from_blocks(decryptedText)

print("\n\n Size of decrypted text: ", len(decryptedText))
print("\n\nDecrypted Text", decryptedText)
# Convert decrypted text to grey scale image
cv2.imshow("Decrypted image", np.array(decryptedText).reshape(64, 64).astype(np.uint8))
# Save decrypted image as decrypted.png
cv2.imwrite("ECCoutput/decrypted.png", np.array(decryptedText).reshape(64, 64).astype(np.uint8))
cv2.waitKey(0)

print("Are the original and decrypted images same? ", plaintext == decryptedText)