---
title: Human Factors in Computer Security
date: 2024-02-09
author:
  - "0x42697262"
  - Jinx
  - Orochi
---

# Human Factors in Computer Security

Humans (or the human element) are the weakest link when it comes to security[^1]. Talk about how their day goes, empathize with them, share some of your experiences that relates with theirs, and then you get to achieve their trust by validating their feelings. That's not exactly how it works in computer security however there are some similarities. Take for example old websites that uses secret questions to recover your password or account. What's the name of your pet? Who's your favorite teacher? Which school did you study? And the list goes on. These personal information can all be taken online or by simply talking to the _human_. This is what they usually consider as a Social Engineering attack. Computer Security does not only contain software implementations and hardware designs, but also the human using the device. However, human mind is difficult to comprehend as it involves a lot of phenomena. Hence, the triggers and cause-effect events are heavily focused.

## Identifying the Threat Actor

Identifying the threat actors[^2] to a certain individual or organization may pose a challenge, however it is easy to guess; it's **you**.

![pika face](./pikaface.png)

Okay, no, not literally you but the "user" itself. However, isn't the definition of a threat actor an external entity that poses a threat to an individual or organization? Well, yeah, but consider a situation where the user is guillible to the technology it possess. They do not understand the concept of keeping one's self safe from the internet (internet because they're more likely to face threats there than their local network).

The user figures that it is safe clicking on web URLs and downloading strange executables does not pose much as a threat. These actions introduces risks to the individual or organization. Hence the user is the threat to its self. The risks could be mitigated with proper training and decent knowledge.

![self sabotage](./selfsabotage.png)

The action that the user performed allowed "indiscriminate attacks" and these always happen on the wild, the internet. A notable destructive instance of such attacks is the WannaCry ransomware, which occurred on May 12, 2017[^3].

![WannaCry Ransomware](./wannacry.png)

On the event that there are certain threat actors targeting an individual or organization, they would do everything they are capable of in order to execute an attack successfully. Even with the most secure software, completely locked down devices, and proper authority and control, it would still be possible to successfully launch an attack, albeit small a chance.

## Attack in Progress

```
suggest a better title lol, Human Factor? hmmm Factoring Humans! HAH! just kidding...
do describe what happens here based on the security principles
- 2. Consider Human Factor (should be the biggest one here in the writeup)
    - mention about:
        - user awareness and understanding (also level of knowledge)
        - human psychology (https://www.interaction-design.org/literature/book/the-glossary-of-human-computer-interaction/human-factors, https://apps.dtic.mil/sti/pdfs/ADA535944.pdf)
            - this includes behavior, bias, emotions, critical thinking, actions, habits, beliefs, motivation, familiary, intent, etc (https://www.sciencedirect.com/science/article/pii/S1877042814040440/pdf)
        - credential management (https://blog.checkpoint.com/security/the-human-factor-of-cyber-security/)
        - tools they are using
        - organizational structure
- 3. Security is economics

end conclusion should assume that the attack has failed. but what if the attack succeeds? proceed to next section
```

## You Have Been Pwned

```
*play all your base are belong to us* jk

maybe mention that cia triad has been broken
```

## suggestions/mitigations/etc

```
do these sections:
- 4. Detect if you can't prevent
- 5. Defense in depth
- 6. Least privilege
- 7. Separation of responsibility
- 8. Ensure complete mediation
- 9. Shannon's Maxim
- 10. Use fail-safe defaults
- 11. Design security from the start
- 12. Trusted Computing Base
- 13. TOCTTOU Vulnerabilities
```

## conclusion ig

here

# Extra

## IT'S JOEVER. JOEWARI DA.

**CAN YOU TRUST YOUR COMPILER?**

```
check out
https://www.cs.cmu.edu/~rdriley/487/papers/Thompson_1984_ReflectionsonTrustingTrust.pdf

basically, can you trust your compiler won't include malware to your compiled code? can you trust the compiler of the compiler that it won't contain malicious code? can you trust your processor that it does not contain malicious code?
```

## References

[^1]: https://www.kuppingercole.com/events/csls2022/blog/human-factor-in-cybersecurity-the-weakest-link
[^2]: https://www.ibm.com/topics/threat-actor
[^3]: https://www.cloudflare.com/learning/security/ransomware/wannacry-ransomware/
