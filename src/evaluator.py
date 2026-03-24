import json
from collections import Counter
from typing import Dict, List

from src.prompt_builder import build_prompt
from src.llm_client import get_llm_decision
from src.metrics import exact_match_rate, consistency_rate, average_pairwise_drift


def evaluate_customer(policy_text: str, customer: Dict, num_runs: int) -> Dict:
    raw_outputs: List[str] = []
    parsed_outputs: List[Dict] = []

    prompt = build_prompt(policy_text, customer)

    for _ in range(num_runs):
        result = get_llm_decision(prompt)
        parsed_outputs.append(result)
        raw_outputs.append(json.dumps(result, sort_keys=True))

    decisions = [x.get("eligibility_decision", "") for x in parsed_outputs]
    risk_bands = [x.get("risk_band_used", "") for x in parsed_outputs]
    reasons = [x.get("reason", "") for x in parsed_outputs]

    reason_counts = Counter(reasons)
    decision_counts = Counter(decisions)

    return {
        "customer_id": customer["customer_id"],
        "product": customer["product_to_evaluate"],
        "runs": num_runs,
        "outputs": parsed_outputs,
        "summary": {
            "exact_match_rate": exact_match_rate(raw_outputs),
            "decision_consistency_rate": consistency_rate(decisions),
            "risk_band_consistency_rate": consistency_rate(risk_bands),
            "average_output_drift": average_pairwise_drift(raw_outputs),
            "decision_flip": len(set(decisions)) > 1,
            "unique_decisions": list(set(decisions)),
            "unique_reasons": list(set(reasons)),
            "decision_counts": dict(decision_counts),
            "reason_counts": dict(reason_counts),
        },
    }