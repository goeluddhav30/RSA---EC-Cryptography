
import numpy as np

def to_blocks(plaintext, n):
    blocks = []
    for i in range(0, len(plaintext), n):
        blocks.append(plaintext[i:i+n])
    return blocks

def from_blocks(blocks):
    plaintext = []
    for block in blocks:
        plaintext.extend(block)
    return plaintext

def expmod(block, exponent, m):
    b = np.array(block)
    if exponent == 0:
        return b * 0 + 1
    if exponent % 2 == 0:
        return expmod((b**2) % m, exponent // 2, m)
    else:
        return (b * expmod((b**2) % m, (exponent - 1) // 2, m)) % m

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)    
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m
