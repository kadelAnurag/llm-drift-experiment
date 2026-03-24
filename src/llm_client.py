import json
import os
from openai import OpenAI

from src.config import MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_llm_decision(prompt: str) -> dict:
    response = client.responses.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "eligibility_decision",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "customer_id": {"type": "string"},
                        "product_evaluated": {"type": "string"},
                        "eligibility_decision": {
                            "type": "string",
                            "enum": ["Approve", "Reject", "Review"]
                        },
                        "risk_band_used": {"type": "string"},
                        "reason": {"type": "string"}
                    },
                    "required": [
                        "customer_id",
                        "product_evaluated",
                        "eligibility_decision",
                        "risk_band_used",
                        "reason"
                    ]
                },
                "strict": True
            }
        }
    )

    text = response.output_text.strip()
    print("\n=== RAW MODEL OUTPUT ===\n")
    print(repr(text))
    print()

    return json.loads(text)