# 🔐 Digital Signature Algorithm (DSA) - Python Implementation

This is a simple implementation of the **Digital Signature Algorithm (DSA)** using Python. It demonstrates how digital signatures work in practice — from key generation, signing a message, to verifying its authenticity.

---

## 📚 What is DSA?

**DSA (Digital Signature Algorithm)** is a cryptographic standard for digital signatures. It uses asymmetric keys (public/private key pairs) to ensure:

- **Authentication** – verifying the sender
- **Integrity** – making sure data hasn't been tampered with
- **Non-repudiation** – the sender cannot deny sending it

---

## 🛠️ Features

- Generate public and private keys
- Sign messages using private key
- Verify signatures using public key
- SHA256-based hashing

---

## 🧑‍💻 Tech Stack

- Language: Python 3.x
- Libraries:
  - `random`
  - `hashlib`
  - `Crypto` (if using PyCryptodome)

---
