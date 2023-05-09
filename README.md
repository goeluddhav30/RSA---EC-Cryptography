
## Introduction

This folder consists of the source code for the asymmetric-key encryption technique, RSA.

This code is written for the 16-bit RSA but may be easily scaled to different variants. The reason behind picking this variant was to avoid overflow errors while printing the encrypted and decypted images.

## How to use RSA

To successfully encrypt and decrypt the source image and look at the encrypted and decrypted image using RSA, use the following line:

```
python3 rsa.py
```

You should see 3 new images in the root directory:

- source.png - The greyscale version of the source image
- encrypted.png - The image encrypted via RSA technique
- decrypted.png - The greyscale image decrypted via RSA technique

## How to use ECC

First, install the following library to work with elliptic curves

```
pip install tinyec
```

To run the ECC algorithm on the given source image, run the following command:

```
python3 ecc.py
```

One can also use the Diffie-Hellman analogy for elliptic curves and use symmetric key encryption after defining 2 people who want to communicate (A and B),
and defining the shared key to be the product of **privateKey_A * publicKey_B** or __publicKey_A * privateKey_B__. Then using a symmetric key encryption technique like RSA with the shared key.

For this technique, we can use the built in library for AES via installing the following library.

```
pip install pycryptodome
```

## Bibliography

I used the tinyec library defined [here](https://github.com/alexmgr/tinyec#installation).

I also used the technique to convert a message into a point on the Elliptic Curve described [here](https://crypto.stackexchange.com/questions/76340/how-to-create-an-ec-point-from-a-plaintext-message-for-encryption).

Here's a paper which talks about calculating the square root of a number in a finite integral field (if prime%4 == 3): [Paper](https://www.math.canterbury.ac.nz/~j.booher/expos/sqr_qnr.pdf)