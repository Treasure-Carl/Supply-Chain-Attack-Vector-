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

