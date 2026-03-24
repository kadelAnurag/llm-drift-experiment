from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"

POLICY_PATH = DATA_DIR / "policy.txt"
CUSTOMERS_PATH = DATA_DIR / "customers.json"

MODEL_NAME = "gpt-4.1-mini"
TEMPERATURE = 0.0
NUM_RUNS = 20
MAX_OUTPUT_TOKENS = 400