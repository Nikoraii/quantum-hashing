import qsharp
from qsharp import Result


class QuantumEncrypt:
    def __init__(self, hash_length: int = 256, project_root: str = "../../QuantumHash"):
        # Initialize Q# project in order to call Q# operations
        qsharp.init(project_root=project_root)
        # Helper mapping of Q# Result to integer
        self.mapping = {
            Result.Zero: 0,
            Result.One: 1,
        }
        self.hash_length = hash_length

    def generate_quantum_bits(self, n: int) -> list[Result]:
        # Call GenerateQuantumBits from QuantumHash
        results: list[Result] = qsharp.eval(
            f"QuantumProjects.QuantumHash.GenerateQuantumBits({n})"
        )
        return results

    def generate_bitstring(self, n: int) -> str:
        results: list[Result] = self.generate_quantum_bits(n)

        # Convert Q# Result to integer
        int_list: list[int] = [self.mapping[r] for r in results]

        # Convert integer list to bit string
        bit_string: str = "".join(str(i) for i in int_list)

        return bit_string

    def compute_hash(self, message: str) -> str:
        # Generate random quantum bitstream, twice the hash size for folding
        qbitstream: list[Result] = self.generate_quantum_bits(self.hash_length * 2)

        # Generate quantum salt
        salt: list[Result] = self.generate_quantum_bits(self.hash_length)

        # Convert message to bits
        message_bits: str = "".join(format(ord(char), "08b") for char in message)

        # Mix quantum randomness, salt, and message bits using XOR
        mixed_bits: str = "".join(
            str(int(a) ^ int(b) ^ int(s))
            for a, b, s in zip(
                qbitstream,
                message_bits * (len(qbitstream) // len(message_bits) + 1),
                salt * (len(qbitstream) // len(salt) + 1),
            )
        )

        # XOR folding to reduce to final hash size
        folded_hash: int = int(mixed_bits[: self.hash_length], 2) ^ int(
            mixed_bits[self.hash_length : 2 * self.hash_length], 2
        )

        # Convert to hex for readability, 4 bits per hex char
        return hex(folded_hash)[2:].zfill(self.hash_length // 4)


def main():
    msg: str = input("Enter a message to hash: ")
    print(f"Message: {msg}")

    quantum_hasher: QuantumEncrypt = QuantumEncrypt()
    hashed_value: str = quantum_hasher.compute_hash(msg)

    print(f"Encrypted Message: {hashed_value}")


if __name__ == "__main__":
    main()
