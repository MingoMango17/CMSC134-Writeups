---
title: Symmetric Key Cryptography
date: 2024-03-04
author:
  - "0x42697262"
  - Jinx
  - Orochi
---

Authors:

- 0x42697262
- Jinx
- Orochi

# Symmetric Key Cryptography

## Semantic Cryptography

### IND-CPA

IND-CPA refers to a game used to check CPA security on any given encryption method.
The game works like this:

1. The encryptor ($Enc$) will give out a public key to the attacker ($A$) while keeping the private key.
2. A will then give two same-length messages $m_0$ and $m_1$ to the $Enc$.
3. $Enc$ will choose a random bit $b \in {0, 1}$ to encrypt both messages.
4. $Enc$ will give out $C_0$ to the $A$.
5. $A$ will guess $\prime b$, and if $\prime b = b$, then $A$ will win.

Another way of referring to the win conditions of this game is the **_Probability of $A$ winning $-1/2 + \varepsilon$_**, where $\varepsilon$ is a very small number.
This means that an encryption method will be CPA secure if the attacker has a very negliglible advantage in winning the IND-CPA game.

The formal definition of having achieved CPA security is:

$$
\text{An encryption method is CPA secure if \forall m_0 and m_1 such that \vert m_0 \vert = \vert m_1 \vert \forall A}
$$

: An encryption method is CPA secure if ∀ m<sub>0</sub> and m<sub>1</sub> such that |m<sub>0</sub>| = |m<sub>1</sub>| ∀ A: <center>A<sup>Enc</sup>(Enc(m<sub>0</sub>)) ≈ A<sup>Enc</sup>(Enc(m<sub>1</sub>))

</center>

### ECB

### Is ECB IND-CPA secure?

## IND-CPA Secure Cryptography
