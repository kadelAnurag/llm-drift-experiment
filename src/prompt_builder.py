import json
from typing import Dict


def build_prompt(policy_text: str, customer: Dict) -> str:
    customer_json = json.dumps(customer, indent=2)

    return f"""
You are evaluating customer eligibility for a financial product.

Use the policy document below and the customer data provided.
Make a decision only from the information given.

You must return ONLY valid JSON.
Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.

Choose the most appropriate decision based on your interpretation of the policy.

Use this exact JSON structure:
{{
  "customer_id": "...",
  "product_evaluated": "...",
  "eligibility_decision": "...",
  "risk_band_used": "...",
  "reason": "short explanation"
}}

POLICY DOCUMENT:
{policy_text}

CUSTOMER DATA:
{customer_json}
""".strip()