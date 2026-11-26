
import csv
from pathlib import Path

import matplotlib.pyplot as plt


# Find project folders
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_FOLDER / "data" / "experiment_results_v2.csv"
OUTPUT_FOLDER = PROJECT_FOLDER / "reports"

OUTPUT_FOLDER.mkdir(exist_ok=True)


def load_results():

    with open(DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        results = []

        for row in reader:
            results.append({
                "m": int(row["filter_size_bits"]),
                "k": int(row["hash_functions"]),
                "observed": float(row["observed_fpr_percent"]),
                "theoretical": float(row["theoretical_fpr_percent"]),
                "ci_lower": float(row["ci95_lower_percent"]),
                "ci_upper": float(row["ci95_upper_percent"])
            })

    return results


def graph_theoretical_vs_observed(results):

    observed = [r["observed"] for r in results]
    theoretical = [r["theoretical"] for r in results]

    lower_errors = [
        r["observed"] - r["ci_lower"] for r in results
    ]

    upper_errors = [
        r["ci_upper"] - r["observed"] for r in results
    ]

    plt.figure(figsize=(9, 6))

    plt.errorbar(
        theoretical,
        observed,
        yerr=[lower_errors, upper_errors],
        fmt="o",
        capsize=4,
        label="Experimental results with 95% CI"
    )

    maximum = max(max(observed), max(theoretical)) * 1.1

    plt.plot(
        [0, maximum],
        [0, maximum],
        linestyle="--",
        label="Perfect agreement"
    )

    plt.xlabel("Theoretical FPR (%)")
    plt.ylabel("Observed FPR (%)")
    plt.title("Theoretical vs Observed False-Positive Rate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "graph1_theoretical_vs_observed.png",
        dpi=300
    )

    plt.close()


def graph_filter_size_effect(results):

    hash_values = sorted(set(r["k"] for r in results))

    plt.figure(figsize=(9, 6))

    for k in hash_values:

        selected = sorted(
            [r for r in results if r["k"] == k],
            key=lambda r: r["m"]
        )

        sizes = [r["m"] for r in selected]
        rates = [r["observed"] for r in selected]

        plt.plot(
            sizes,
            rates,
            marker="o",
            label=f"{k} hash functions"
        )

    plt.xlabel("Bloom Filter Size (bits)")
    plt.ylabel("Observed FPR (%)")
    plt.title("Effect of Filter Size on False-Positive Rate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "graph2_filter_size_effect.png",
        dpi=300
    )

    plt.close()


def graph_hash_function_effect(results):

    size_values = sorted(set(r["m"] for r in results))

    plt.figure(figsize=(9, 6))

    for size in size_values:

        selected = sorted(
            [r for r in results if r["m"] == size],
            key=lambda r: r["k"]
        )

        hashes = [r["k"] for r in selected]
        rates = [r["observed"] for r in selected]

        plt.plot(
            hashes,
            rates,
            marker="o",
            label=f"{size} bits"
        )

    plt.xlabel("Number of Hash Functions (k)")
    plt.ylabel("Observed FPR (%)")
    plt.title("Effect of Hash Functions on False-Positive Rate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_FOLDER / "graph3_hash_function_effect.png",
        dpi=300
    )

    plt.close()


def main():

    print("BLOOM FILTER DATA VISUALIZATION")
    print("=" * 50)

    if not DATA_FILE.exists():
        print("Error: experiment_results_v2.csv not found!")
        return

    results = load_results()

    graph_theoretical_vs_observed(results)
    graph_filter_size_effect(results)
    graph_hash_function_effect(results)

    print("All three graphs created successfully!")

    print("\nSaved graph files:")

    print(OUTPUT_FOLDER / "graph1_theoretical_vs_observed.png")
    print(OUTPUT_FOLDER / "graph2_filter_size_effect.png")
    print(OUTPUT_FOLDER / "graph3_hash_function_effect.png")


if __name__ == "__main__":
    main()
