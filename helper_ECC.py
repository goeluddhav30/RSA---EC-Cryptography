
import numpy as np

def to_blocks(plaintext, n):
    blocks = []
    cur = 0
    for i in range(0, len(plaintext)):
        cur <<= 8
        cur += plaintext[i]
        if (i+1) % n == 0:
            # print(cur.bit_length())
            blocks.append(cur)
            cur = 0
    return blocks

def from_blocks(blocks):
    plaintext = []
    for block in blocks:
        block >>= 32
        # print(block.bit_length())
        for _ in range(16):
            plaintext.append(block >> max((block.bit_length() - 8), 0))
            block &= (1 << max((block.bit_length() - 8), 0)) - 1
    return plaintext


def expmod(block, exponent, m):
    b = np.array(block)
    if exponent == 0:
        return b * 0 + 1
    if exponent % 2 == 0:
        return expmod((b**2) % m, exponent // 2, m)
    else:
        return (b * expmod((b**2) % m, (exponent - 1) // 2, m)) % m
    
def sqrt(n, p):
    x = expmod(n, (p + 1) // 4, p)
    if (x**2) % p == n:
        return x
    x = (p-x) % p
    if (x**2) % p == n:
        return x
    return -1