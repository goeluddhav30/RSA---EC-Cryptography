
import random
from helper_RSA import gcd, modinv

def miller_rabin(n, k = 10):
    """ Returns False if n is composite, True if n is probably prime.
        k is the number of rounds of testing to perform.
        The higher k, the more accurate the test.
    """
    if n%2 == 0 or n == 1:
        return False
    if n == 2:
        return True
    
    # Write n-1 as 2^s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while d%2 == 0:
        d //= 2
        s += 1
    
    # Check composite
    def check_composite(a):
        """ Returns True if n is composite, False if n is probably prime.
            a is a witness that n is composite."""
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            return False
        for _ in range(1, s):
            x = pow(x, 2, n)
            if x == n-1:
                return False
        return True

    # Run k tests for primality
    for _ in range(k):
        a = random.randrange(2, n-1)
        if check_composite(a):
            return False        # n is composite
    return True                 # n is probably prime

def generate_prime(bits):
    """ Generate a random prime number of bits length """
    while True:
        n = random.getrandbits(bits)
        # If n is even, make it odd
        if n%2 == 0:   
            n += 1
        if miller_rabin(n):
            return n
        n += 2
    
def generate_key(phi):
    """ Generate the public and private keys for RSA"""

    # Find a random e such that 1 < e < phi and gcd(e, phi) = 1
    e = random.randint(2, phi-1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi-1)

    # Find d such that d*e = 1 mod phi
    d = modinv(e, phi)

    return e, d