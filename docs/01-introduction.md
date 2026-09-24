# Insecure Deserialization as a Supply Chain Attack Vector

> Practical exploration of insecure Python deserialization using
> `pickle`
> - as a supply chain attack vector in the serilisation process

## Source Lab

This project is based on the
[TryHackMe Supply Chain Attack Vector] room.

The purpose of this repository is to document my learning process,
analysis, commands, observations, and mitigation strategies while
working through the lab.

---

## Objectives

- Understand serialization and deserialization
- Understand how Python `pickle` works
- Identify insecure deserialization
- Analyze a malicious serialized object
- Understand how `__reduce__()` can influence deserialization
- Understand the security impact
- Explore safer alternatives and mitigations
- Compearing model cards to identify the malicous and bieng models before download for use.

---

## Environment

- OS: Kali Linux
- Python: 3.x
- TryHackMe: Insecure Deserialization
- Tools: Python, Pickletools(safe), Linux terminal

