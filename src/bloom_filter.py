
import hashlib
import math


class BloomFilter:

    def __init__(self, size, hash_count):
        if size <= 0:
            raise ValueError("Size must be greater than zero.")

        if hash_count <= 0:
            raise ValueError("Hash count must be greater than zero.")

        self.size = size
        self.hash_count = hash_count

        # Create a bit array using bytes.
        self.bit_array = bytearray((size + 7) // 8)

        # Number of insertion operations.
        self.items_added = 0

    def _get_hash_positions(self, item):

        # Convert the item into bytes.
        item = str(item).encode("utf-8")

        # Generate a SHA-256 digest.
        digest = hashlib.sha256(item).digest()

        # Split the digest into two integer hash values.
        hash1 = int.from_bytes(digest[:16], "big")
        hash2 = int.from_bytes(digest[16:], "big")

        # Avoid a zero second hash.
        if hash2 == 0:
            hash2 = 1

        # Generate positions using double hashing.
        positions = []

        for i in range(self.hash_count):
            position = (hash1 + i * hash2) % self.size
            positions.append(position)

        return positions

    def add(self, item):

        positions = self._get_hash_positions(item)

        for position in positions:

            byte_index = position // 8
            bit_index = position % 8

            self.bit_array[byte_index] |= (1 << bit_index)

        self.items_added += 1

    def might_contain(self, item):

        positions = self._get_hash_positions(item)

        for position in positions:

            byte_index = position // 8
            bit_index = position % 8

            if not (self.bit_array[byte_index] & (1 << bit_index)):
                return False

        return True

    def count_set_bits(self):

        return sum(byte.bit_count() for byte in self.bit_array)

    def memory_usage_bytes(self):

        return len(self.bit_array)

    def theoretical_false_positive_rate(self):

        if self.items_added == 0:
            return 0.0

        probability = (
            1 - math.exp(
                -self.hash_count * self.items_added / self.size
            )
        ) ** self.hash_count

        return probability

    @staticmethod
    def optimal_hash_count(size, item_count):

        if size <= 0 or item_count <= 0:
            raise ValueError("Size and item count must be positive.")

        k = (size / item_count) * math.log(2)

        return max(1, round(k))


# Basic demonstration
if __name__ == "__main__":

    bloom = BloomFilter(size=100, hash_count=3)

    # Insert usernames.
    usernames = ["rajan", "sanidhya", "alex", "john"]

    for username in usernames:
        bloom.add(username)

    print("BLOOM FILTER TEST")
    print("-----------------")

    print("Inserted usernames:", usernames)

    print("\nMembership checks:")

    print("rajan:", bloom.might_contain("rajan"))
    print("sanidhya:", bloom.might_contain("sanidhya"))
    print("unknown_user:", bloom.might_contain("unknown_user"))

    print("\nStatistics:")

    print("Total bits:", bloom.size)
    print("Set bits:", bloom.count_set_bits())
    print("Hash functions:", bloom.hash_count)
    print("Memory usage:", bloom.memory_usage_bytes(), "bytes")

    print(
        "Theoretical FPR:",
        round(bloom.theoretical_false_positive_rate() * 100, 4),
        "%"
    )

    print(
        "Optimal hash count:",
        bloom.optimal_hash_count(100, 4)
    )