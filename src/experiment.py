
import csv
import math
from pathlib import Path

from bloom_filter import BloomFilter


# Experiment settings
NUMBER_OF_INSERTED_USERS = 1000
NUMBER_OF_TEST_USERS = 5000

# Existing configurations + theoretically optimal configurations
CONFIGURATIONS = [
    (8000, 3),
    (8000, 5),
    (8000, 7),
    (12000, 3),
    (12000, 5),
    (12000, 7),
    (16000, 3),
    (16000, 5),
    (16000, 7),

    # Additional optimal hash-function configurations
    (8000, 6),
    (12000, 8),
    (16000, 11)
]


def create_datasets():

    inserted_users = [
        f"registered_user_{i}"
        for i in range(NUMBER_OF_INSERTED_USERS)
    ]

    test_users = [
        f"unseen_user_{i}"
        for i in range(NUMBER_OF_TEST_USERS)
    ]

    return inserted_users, test_users


def calculate_confidence_interval(successes, total, z=1.96):
    """Calculate a 95% Wilson confidence interval."""

    if total == 0:
        return 0.0, 0.0

    p = successes / total

    denominator = 1 + (z ** 2 / total)

    centre = (
        p + (z ** 2 / (2 * total))
    ) / denominator

    margin = (
        z * math.sqrt(
            (p * (1 - p) / total)
            + (z ** 2 / (4 * total ** 2))
        )
    ) / denominator

    lower = max(0, centre - margin)
    upper = min(1, centre + margin)

    return lower, upper


def run_experiment(inserted_users, test_users):

    results = []

    for size, hash_count in CONFIGURATIONS:

        bloom = BloomFilter(
            size=size,
            hash_count=hash_count
        )

        # Insert usernames
        for username in inserted_users:
            bloom.add(username)

        # Check false negatives
        false_negatives = 0

        for username in inserted_users:
            if not bloom.might_contain(username):
                false_negatives += 1

        # Check false positives
        false_positives = 0

        for username in test_users:
            if bloom.might_contain(username):
                false_positives += 1

        # Calculate observed rates
        observed_fpr = (
            false_positives / len(test_users)
        )

        false_negative_rate = (
            false_negatives / len(inserted_users)
        )

        # Calculate 95% confidence interval
        ci_lower, ci_upper = calculate_confidence_interval(
            false_positives,
            len(test_users)
        )

        # Calculate theoretical optimal hash count
        optimal_k = BloomFilter.optimal_hash_count(
            size,
            len(inserted_users)
        )

        # Collect results
        results.append({
            "filter_size_bits": size,
            "hash_functions": hash_count,
            "optimal_hash_functions": optimal_k,
            "inserted_users": len(inserted_users),
            "tested_unseen_users": len(test_users),
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "observed_fpr_percent": round(
                observed_fpr * 100, 4
            ),
            "theoretical_fpr_percent": round(
                bloom.theoretical_false_positive_rate() * 100,
                4
            ),
            "ci95_lower_percent": round(
                ci_lower * 100, 4
            ),
            "ci95_upper_percent": round(
                ci_upper * 100, 4
            ),
            "false_negative_rate_percent": round(
                false_negative_rate * 100, 4
            ),
            "memory_bytes": bloom.memory_usage_bytes()
        })

    return results


def save_results(results):

    project_folder = Path(__file__).resolve().parent.parent
    output_folder = project_folder / "data"
    output_folder.mkdir(exist_ok=True)

    # Save separately to protect original results
    output_file = output_folder / "experiment_results_v2.csv"

    with open(output_file, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    return output_file


def main():

    print("BLOOM FILTER STATISTICAL EXPERIMENT")
    print("=" * 90)

    inserted_users, test_users = create_datasets()

    print("Inserted usernames:", len(inserted_users))
    print("Unseen test usernames:", len(test_users))
    print("Configurations:", len(CONFIGURATIONS))

    results = run_experiment(
        inserted_users,
        test_users
    )

    print("\nEXPERIMENT RESULTS")
    print("-" * 90)

    for result in results:

        print(
            f"m={result['filter_size_bits']:5} | "
            f"k={result['hash_functions']:2} | "
            f"FP={result['false_positives']:4} | "
            f"FN={result['false_negatives']:2} | "
            f"Observed FPR={result['observed_fpr_percent']:7.4f}% | "
            f"Theoretical FPR={result['theoretical_fpr_percent']:7.4f}%"
        )

        print(
            f"     95% CI: "
            f"{result['ci95_lower_percent']:.4f}% - "
            f"{result['ci95_upper_percent']:.4f}% | "
            f"Memory={result['memory_bytes']} bytes"
        )

    output_file = save_results(results)

    print("\nResults saved successfully!")
    print("File:", output_file)

    total_false_negatives = sum(
        result["false_negatives"]
        for result in results
    )

    if total_false_negatives == 0:
        print("\nPASS: No false negatives detected.")
    else:
        print("\nWARNING: False negatives detected!")


if __name__ == "__main__":
    main()