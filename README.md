# LLM Drift vs Decision Stability

> Finding: LLMs are not fully deterministic in language, but highly consistent in decision-making.

---

## 🧪 Overview

This project explores how Large Language Models (LLMs) behave when repeatedly evaluating the same decision task under identical conditions.

The goal was to test whether LLMs produce consistent decisions or exhibit drift across multiple runs.

We simulate a financial eligibility system where:
- A policy document defines rules
- Customer data is provided as input
- An LLM evaluates eligibility multiple times

---

## ⚙️ Experiment Setup

We model a simple decision system for a product: **StarterCard**

Each evaluation includes:
- Policy document (text)
- Customer data (JSON)

The same input is run multiple times (`NUM_RUNS`) through the LLM.

Each run outputs:
- eligibility decision (Approve / Reject / Review)
- reasoning

---

## 🔁 Pipeline
Policy (text) + Customer Data (JSON)
↓
Prompt Builder
↓
LLM Evaluation (repeated runs)
↓
Metrics + Analysis


---

## 📊 Metrics Used

### 1. Decision Consistency
How often the final decision remains the same across runs.

- 1.00 = fully stable  
- < 1.00 = decision drift  

---

### 2. Exact Match Rate
How often the entire JSON output is identical.

- Low → language variation  
- High → deterministic output  

---

### 3. Average Output Drift
Measures textual variation across outputs.

---

## 🔍 Key Findings

### 1. Language is not deterministic

Even with identical inputs, explanations vary:

- "Meets minimum requirements"
- "Income and savings exceed threshold"
- "Customer satisfies eligibility criteria"

This results in low exact match rates.

---

### 2. Decisions are highly stable

Across all customers:

- Decision Consistency = **1.00**
- No decision flips observed

The model consistently produces the same outcome.

---

### 3. Borderline cases still converge

Even ambiguous inputs (near eligibility thresholds) resolve consistently: borderline → Review


The model does not oscillate between decisions.

---

### 4. LLMs stabilize ambiguity

Instead of expressing uncertainty, the model converges to a dominant interpretation.

This suggests:

> Ambiguity is internally resolved into consistent heuristics rather than producing variable outcomes.

---

## 🧠 Conclusion

LLMs exhibit two distinct behaviors:

- **Surface-level variability** → language changes across runs  
- **Deep-level stability** → decisions remain consistent  

This means:

> LLM outputs may look different, but their decision logic is effectively stable.

---

## ⚠️ Key Insight

The issue with LLM-based systems is not randomness.

It is:

> **Implicit reasoning that cannot be directly inspected or controlled.**

---

## 🚀 Next Step

This experiment sets up a comparison with an ontology-based system:

| LLM System        | Ontology System         |
|------------------|------------------------|
| implicit reasoning | explicit rules        |
| hidden logic       | traceable logic       |
| stable but opaque  | stable and auditable  |

---


---

## ▶️ Run the Experiment

### 1. Install dependencies

### 2. Set API key

### 3. Run



---

## 📌 Notes

- This is an exploratory experiment  
- The goal is to understand LLM behavior, not build a production system  
- Results may vary slightly depending on model version  

---

## 🧩 Why this matters

LLMs are increasingly used for decision-making systems.

This experiment shows:

- They are **not textually deterministic**
- But they are **functionally consistent**

Understanding this distinction is critical when designing systems that rely on AI for decisions.


