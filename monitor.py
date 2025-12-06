import hashlib, sys
from blockchain import Blockchain

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def add_file(filepath, chainfile):
    filehash = sha256_file(filepath)
    Blockchain.append_block(chainfile, filepath, filehash)

if __name__ == "__main__":
    action = sys.argv[1]
    file = sys.argv[2]
    chain = sys.argv[3]

    if action == "add":
        add_file(file, chain)
