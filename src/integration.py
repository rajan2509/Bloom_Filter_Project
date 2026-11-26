
import sqlite3
from pathlib import Path
from bloom_filter import BloomFilter

# Database location
DB_PATH = Path("data/bloom_filter.db")

# Bloom Filter configuration
FILTER_SIZE = 16000
HASH_COUNT = 6


def load_bloom_filter():
    """Load all database records into the Bloom Filter."""

    bloom = BloomFilter(size=FILTER_SIZE, hash_count=HASH_COUNT)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT item_type, item_value FROM checked_items")
    records = cursor.fetchall()

    for item_type, item_value in records:
        key = f"{item_type}:{item_value}"
        bloom.add(key)

    conn.close()

    return bloom, len(records)


def check_membership(item_type, item_value, bloom):
    """Check an item using Bloom Filter and SQLite."""

    key = f"{item_type}:{item_value}"

    # Step 1: Check Bloom Filter
    if not bloom.might_contain(key):
        return False, "Database lookup skipped (definitely absent)"

    # Step 2: Verify possible match in SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1 FROM checked_items
        WHERE item_type = ? AND item_value = ?
        """,
        (item_type, item_value)
    )

    result = cursor.fetchone()
    conn.close()

    return result is not None, "SQLite database verification completed"


def main():
    print("\n" + "=" * 50)
    print("INTERACTIVE BLOOM FILTER MEMBERSHIP CHECKER")
    print("=" * 50)

    if not DB_PATH.exists():
        print("\nDatabase not found!")
        print("Please run: python src/database.py")
        return

    bloom, total_records = load_bloom_filter()

    print("\nBloom Filter loaded successfully!")
    print(f"Total database records: {total_records}")

    while True:
        print("\n" + "-" * 50)
        print("1. Check Username")
        print("2. Check URL")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "3":
            print("\nThank you for using the checker!")
            break

        if choice == "1":
            item_type = "username"
            item_value = input("Enter username: ").strip()

        elif choice == "2":
            item_type = "url"
            item_value = input("Enter URL: ").strip()

        else:
            print("Invalid choice! Please enter 1, 2, or 3.")
            continue

        if not item_value:
            print("Input cannot be empty. Please try again.")
            continue

        print("\nChecking Bloom Filter...")

        found, message = check_membership(
            item_type,
            item_value,
            bloom
        )

        print(message)

        if found:
            print("\nRESULT: FOUND in database")
        else:
            print("\nRESULT: NOT FOUND in database")


if __name__ == "__main__":
    main()
