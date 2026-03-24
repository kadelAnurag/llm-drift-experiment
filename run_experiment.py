from datetime import datetime

from src.config import POLICY_PATH, CUSTOMERS_PATH, RESULTS_DIR, NUM_RUNS
from src.evaluator import evaluate_customer
from src.utils import load_json, load_text, save_json


def print_summary(all_results):
    print("\n" + "=" * 60)
    print("FINAL INSIGHTS")
    print("=" * 60)

    for result in all_results:
        summary = result["summary"]

        print(f"\nCustomer: {result['customer_id']}")
        print(f"Product: {result['product']}")
        print(f"Runs: {result['runs']}")
        print(f"Decision Consistency: {summary['decision_consistency_rate']:.2f}")
        print(f"Risk Band Consistency: {summary['risk_band_consistency_rate']:.2f}")
        print(f"Exact Match Rate: {summary['exact_match_rate']:.2f}")
        print(f"Average Output Drift: {summary['average_output_drift']:.4f}")
        print(f"Decision Flip: {summary['decision_flip']}")

        print("\nDecision Counts:")
        for decision, count in summary["decision_counts"].items():
            print(f"  {decision}: {count}")

        print("\nDifferent Reasons:")
        for reason, count in summary["reason_counts"].items():
            print(f"  {count}x - {reason}")

        print("-" * 60)


def print_global_insights(all_results):
    print("\n" + "=" * 60)
    print("GLOBAL LEARNINGS")
    print("=" * 60)

    total_customers = len(all_results)
    customers_with_decision_flip = sum(
        1 for r in all_results if r["summary"]["decision_flip"]
    )

    avg_exact_match = sum(
        r["summary"]["exact_match_rate"] for r in all_results
    ) / total_customers

    avg_decision_consistency = sum(
        r["summary"]["decision_consistency_rate"] for r in all_results
    ) / total_customers

    print(f"Total Customers Evaluated: {total_customers}")
    print(f"Customers with Decision Drift: {customers_with_decision_flip}")
    print(f"Average Exact Match Rate: {avg_exact_match:.2f}")
    print(f"Average Decision Consistency: {avg_decision_consistency:.2f}")

    print("\nWhat we are learning:")
    print("- Exact wording often changes even when the final decision stays the same.")
    print("- Borderline cases tend to show more variation in reasoning.")
    print("- The model often converges on a stable decision pattern even under ambiguity.")


def main() -> None:
    policy_text = load_text(POLICY_PATH)
    customers = load_json(CUSTOMERS_PATH)

    all_results = []

    for customer in customers:
        result = evaluate_customer(policy_text, customer, NUM_RUNS)
        all_results.append(result)
        print(
            f"{customer['customer_id']} | "
            f"decision consistency: {result['summary']['decision_consistency_rate']:.2f} | "
            f"exact match: {result['summary']['exact_match_rate']:.2f}"
        )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = RESULTS_DIR / f"experiment_runs{NUM_RUNS}_{timestamp}.json"
    save_json(output_path, all_results)

    print(f"\nSaved results to: {output_path}")
    print_summary(all_results)
    print_global_insights(all_results)


if __name__ == "__main__":
    main()