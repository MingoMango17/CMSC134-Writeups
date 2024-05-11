# Machine problem 2: RSA encryption


Write a program that encrypts and decrypts a message using RSA-OAEP with authenticity.

Use the encrypt-then-sign scheme for authenticated encryption. Use a separate key for encryption and signing.

Do not implement crypto algorithms on your own. Make use of cryptographic libraries in implementing your program.

Your program must be able to:

- separately generate new keypairs for encryption and signing,
- encrypt-then-sign/verify-then-decrypt a short ASCII message (at most 140 chars) using RSA-OAEP.
