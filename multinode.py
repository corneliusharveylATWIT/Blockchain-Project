from blockchain import Blockchain
from monitor import sha256_file

NODES = ["nodeA_chain.jsonl", "nodeB_chain.jsonl", "nodeC_chain.jsonl"]

def init_all():
    for n in NODES:
        Blockchain.init_chain(n)

def add_to_all(filepath):
    filehash = sha256_file(filepath)
    for n in NODES:
        Blockchain.append_block(n, filepath, filehash)

def validate_all():
    hashes = {}
    print("\n[VALIDATING NODES]")

    for n in NODES:
        Blockchain.validate_chain(n)
        hh = Blockchain.head_hash(n)
        hashes[n] = hh
        print(f"  {n} HEAD HASH: {hh}")

    print("\n[CONSENSUS CHECK]")
    groups = {}
    for node, h in hashes.items():
        groups.setdefault(h, []).append(node)

    majority_hash = max(groups, key=lambda k: len(groups[k]))
    winners = groups[majority_hash]

    if len(winners) >= 2:
        print("[OK] Consensus reached:", winners)
    else:
        print("[FAIL] Blockchain compromised.")
