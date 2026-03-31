# LLM Drift vs Decision Stability

> Finding: LLMs are highly consistent in decision-making but exhibit systematic rule comprehension gaps and occasional numerical hallucinations.

---

## 🧪 Overview

This project explores how Large Language Models (LLMs) behave when repeatedly evaluating the same decision task under identical conditions.

The goal is to test whether LLMs produce consistent decisions or exhibit drift across multiple runs — and to understand *what kind* of errors occur when they do fail.

We simulate a financial eligibility system where:
- A policy document defines explicit rules per product
- Customer data is provided as input
- An LLM evaluates eligibility multiple times

This experiment is the first phase of a broader comparison between LLM-based and ontology-based decision systems.

---

## ⚙️ Experiment Setup

We evaluate three financial products: **StarterCard**, **FlexiCard**, and **PersonalLoan**

The policy defines separate rules per product, including:
- Income and savings thresholds (exclusive — applicant must exceed, not meet)
- Allowed risk bands (Low Risk, Medium Risk only)
- Employment type constraints (Salaried, Freelancer, Self-Employed, Gig Worker)
- Income pattern, cashflow consistency, and documentation requirements

Each evaluation includes:
- Policy document (text)
- Customer data (JSON) including employment type

The same input is run `NUM_RUNS` times through the LLM.

Each run outputs:
- Eligibility decision (Approve / Reject / Review)
- Reasoning

---

## 🔁 Pipeline

```
Policy (text) + Customer Data (JSON)
        ↓
   Prompt Builder
        ↓
LLM Evaluation (repeated runs)
        ↓
  Metrics + Analysis
```

---

## 🎯 Test Case Design

Test cases were deliberately designed to stress-test the model's decision stability. Rather than using clear-cut profiles, each case targets a specific failure mode:

| Customer | Strategy | Expected Decision |
|---|---|---|
| DRIFT_01 | Income and savings just barely above thresholds | Approve |
| DRIFT_02 | Employment type not defined in policy ("Contract Worker") | Reject |
| DRIFT_03 | Freelancer with income exactly at alt rule threshold (15,000) | Reject (strict >) |
| DRIFT_04 | Income below threshold but very high savings (250,000) | Reject |
| DRIFT_05 | Gig Worker applying for StarterCard — no rule covers this | Reject |
| DRIFT_06 | High Risk band with exceptional income and savings | Reject |
| DRIFT_07 | PersonalLoan: passes income/savings check but expenses exceed income | Reject |
| DRIFT_08 | Freelancer with income between alt threshold (15k) and main threshold (20k) | Approve via Rule 2 |

---

## 📊 Metrics Used

### 1. Decision Consistency
How often the final decision remains the same across runs.
- 1.00 = fully stable
- < 1.00 = decision drift

### 2. Exact Match Rate
How often the entire JSON output is identical.
- Low → language variation
- High → deterministic output

### 3. Average Output Drift
Measures textual variation across outputs using normalised edit distance.

---

## 🔍 Key Findings

### 1. Decisions are highly stable — but not perfectly so

Across 8 adversarial test cases (20 runs each):
- Average Decision Consistency: **0.98**
- Customers with decision flip: **1 out of 8**
- The one flip (DRIFT_07) had consistency of 0.85 (17 Approve, 3 Reject)

The model is remarkably stable even under adversarial conditions.

---

### 2. Language is not deterministic

Even when the decision is identical across all 20 runs, the wording of the reasoning varies considerably. Average Exact Match Rate: **0.52**

Examples from DRIFT_01 (all Approve, different wording):
- *"Salaried applicant with monthly income exceeding 20,000, savings exceeding 50,000, medium risk band, stable income, monthly recurring income pattern..."*
- *"Salaried applicant meeting all StarterCard Rule 1 criteria."*

Surface variation is consistent — deep decision logic is stable.

---

### 3. Hard disqualifiers are respected unconditionally

Cases with a single, unambiguous disqualifier showed the strongest stability:

| Case | Disqualifier | Consistency | Exact Match |
|---|---|---|---|
| DRIFT_04 | Income below threshold | 1.00 | **1.00** |
| DRIFT_06 | High Risk band | 1.00 | 0.80 |
| DRIFT_02 | Unknown employment type | 1.00 | 0.75 |

DRIFT_04 is particularly notable: despite savings being 250,000 (5x the threshold), the model gave *identical output* across all 20 runs once it identified the income failure. Compensating signals had zero effect.

---

### 4. The alt income rule is systematically ignored

The policy defines two rules for StarterCard:
- **Rule 1** (Salaried): income > 20,000
- **Rule 2** (Freelancer/Self-Employed): income > 15,000

In both freelancer test cases (DRIFT_03 and DRIFT_08), the model consistently applied Rule 1's threshold of 20,000 — ignoring Rule 2 entirely. DRIFT_08 (income=17,000, Freelancer) should have been Approved via Rule 2 but was Rejected 20/20 times.

This is not random drift. It is a **systematic rule comprehension gap** — the model defaults to the primary rule and fails to route applicants to the applicable alternative rule.

---

### 5. The only decision flip was caused by numerical hallucination

DRIFT_07 was designed to trigger drift via negative disposable income (expenses=52,000 > income=45,000). The 3 rejections did not cite repayment capacity. Instead they stated: *"Monthly income does not exceed INR 40,000"* — which is factually incorrect (income is 45,000).

The model misread the income figure in 3 out of 20 runs. The intended drift signal (repayment capacity) was ignored in all 20 runs. Two failure modes in one case:
- **Numerical hallucination**: misreading a value present in the input
- **Signal blindness**: ignoring the repayment capacity clause entirely

---

### 6. Borderline thresholds do not cause oscillation

DRIFT_01 (barely above thresholds) produced 100% Approve consistency. The model does not oscillate at margins — once it determines a threshold is exceeded, it commits.

---

## 🧠 Conclusion

LLMs exhibit three distinct behaviours in policy-based decision tasks:

- **Surface-level variability** → language and reasoning phrasing changes across runs
- **Deep-level stability** → decisions remain consistent even under adversarial inputs
- **Systematic comprehension gaps** → multi-rule policies are partially misread in a consistent, directional way

The issue with LLM-based decision systems is not randomness. It is:

> **Implicit reasoning that cannot be directly inspected or controlled — and that may systematically misapply rules in ways that are stable but wrong.**

---

## ⚠️ Failure Mode Taxonomy

From this experiment, three distinct failure modes were identified:

| Failure Mode | Example | Nature |
|---|---|---|
| Numerical hallucination | DRIFT_07: income=45,000 read as not exceeding 40,000 | Stochastic — appeared in 3/20 runs |
| Rule comprehension gap | DRIFT_03, DRIFT_08: alt freelancer rule ignored | Systematic — appeared in 20/20 runs |
| Signal blindness | DRIFT_07: repayment capacity clause ignored | Systematic — appeared in 20/20 runs |

---

## 🚀 Next Steps

### Phase 2 — Ontology Comparison

This experiment sets up a direct comparison with an ontology-based decision system encoding identical rules:

| Dimension | LLM System | Ontology System |
|---|---|---|
| Decision consistency | High but imperfect | Deterministic |
| Rule application | Implicit, may skip rules | Explicit, traceable |
| Failure mode | Hallucination + gaps | None (rules always fire) |
| Auditability | Low | High |

The policy and customer data have been aligned with the ontology to enable identical inputs across both systems.

### Phase 3 — Multi-model testing

Testing across model sizes to validate whether smaller models (7-8B) show different drift patterns compared to larger models, following findings from the attached research paper (Khatchadourian & Franco, 2025).

---

## 📌 Notes

- This is an exploratory experiment
- The goal is to understand LLM behaviour, not build a production system
- Results may vary depending on model version and temperature settings
- All test cases were designed adversarially — results are not representative of typical use

---

## 🧩 Why this matters

LLMs are increasingly used for financial and regulatory decision-making. This experiment shows that:

- They are **not textually deterministic** — wording varies even when the decision does not
- They are **functionally consistent** for clear-cut cases
- They **systematically misapply complex multi-rule policies** in ways that are stable and therefore hard to detect
- They can **hallucinate numerical values** present in the input

Understanding these failure modes is critical before deploying LLMs in any system where decisions must be auditable, reproducible, or legally defensible.
