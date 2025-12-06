import json, hashlib, os
from dataclasses import dataclass, asdict

@dataclass
class Block:
    index: int
    filename: str
    filehash: str
    prev_hash: str
    timestamp: float = 0.0    # FIXED for consensus

    def to_json(self):
        return json.dumps(asdict(self), sort_keys=True)

    def compute_hash(self):
        return hashlib.sha256(self.to_json().encode()).hexdigest()


class Blockchain:

    @staticmethod
    def init_chain(path):
        """Create ledger with deterministic genesis."""
        genesis = Block(
            index=0,
            filename="__GENESIS__",
            filehash="",
            prev_hash="0" * 64,
            timestamp=0.0
        )

        with open(path, "w") as f:
            f.write(genesis.to_json() + "\n")

        print(f"[OK] Initialized: {path}")

    @staticmethod
    def append_block(path, filename, filehash):
        """Append deterministic block to chain."""
        # Load last block
        with open(path, "r") as f:
            last = None
            for line in f:
                if line.strip():
                    last = json.loads(line)

        prev_hash = hashlib.sha256(json.dumps(last, sort_keys=True).encode()).hexdigest()
        new_index = last["index"] + 1

        new_block = Block(
            index=new_index,
            filename=filename,
            filehash=filehash,
            prev_hash=prev_hash,
            timestamp=0.0
        )

        with open(path, "a") as f:
            f.write(new_block.to_json() + "\n")

        print(f"[OK] Added Block #{new_index} → {path}")

    @staticmethod
    def validate_chain(path):
        """Ensure prev_hash chain is correct."""
        with open(path, "r") as f:
            prev_hash = "0" * 64
            index = 0

            for line in f:
                block = json.loads(line)

                if index > 0 and block["prev_hash"] != prev_hash:
                    print(f"[FAIL] Corruption at block #{index} in {path}")
                    return False

                block_json = json.dumps(block, sort_keys=True)
                prev_hash = hashlib.sha256(block_json.encode()).hexdigest()
                index += 1

        print(f"[OK] Valid: {path}")
        return True

    @staticmethod
    def head_hash(path):
        """Return hash of last block."""
        last = None
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    last = json.loads(line)

        return hashlib.sha256(json.dumps(last, sort_keys=True).encode()).hexdigest()
