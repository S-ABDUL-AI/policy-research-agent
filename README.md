# Policy Research Agent

An autonomous AI agent that researches policy questions and **monitors its own behavior** while doing so.

Built as a natural extension of two prior projects:
- [`constraint-divergence-eval`](https://github.com/S-ABDUL-AI/constraint-divergence-eval) — measuring how token constraints alter AI outputs
- [`sycophancy-probe`](https://github.com/S-ABDUL-AI/sycophancy-probe) — measuring position reversals under social pressure

Those projects measured LLM behavior from the outside. This one instruments an agent from the inside.

---

## What it does

1. Takes a public-policy question as input
2. Autonomously breaks it into sub-questions, searches the web, reads sources, and takes notes
3. Produces a structured policy brief (executive summary, findings, recommendations, evidence gaps)
4. Simultaneously logs a **behavioral audit** of its own research process

## Behavioral signals tracked

| Signal | Method | Prior work |
|--------|--------|------------|
| Token compression per step | output_tokens / input_tokens | constraint-divergence-eval |
| Output length drift | coefficient of variation across steps | constraint-divergence-eval |
| Position change signals | revision markers in notes | sycophancy-probe |
| Tool overuse | step count threshold | — |

The audit report flags runs that exhibit high compression, high length drift, or position instability — the same failure modes studied in the eval projects, now observable inside a live agent loop.

---

## Example output

**Input question:**
> What is the evidence on algorithmic benefit-eligibility tools and racial equity?

**Policy brief excerpt:**
```markdown
## Executive Summary
Direct evidence on how algorithmic benefit-eligibility tools affect racial
groups is thin. The best-documented cases show serious harm — due process
violations and wrongful benefit cuts — but sources do not report racial
breakdowns. Stronger racial-bias evidence comes from adjacent health
risk-prediction algorithms. Policymakers should treat racial equity as an
unverified risk requiring explicit auditing.
```

**Behavioral audit (behavioral_audit.json):**
```json
{
  "total_steps": 16,
  "total_input_tokens": 86410,
  "total_output_tokens": 6355,
  "output_length_drift_cv": 1.09,
  "position_change_signals": 0,
  "tool_distribution": {
    "web_search": 6,
    "fetch_url": 5,
    "take_note": 4,
    "get_notes": 1
  },
  "flags": {
    "high_compression": true,
    "high_length_drift": true,
    "position_instability": false,
    "tool_overuse": true
  }
}
```

---

## Setup

```bash
git clone https://github.com/S-ABDUL-AI/policy-research-agent
cd policy-research-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
python run.py "What is the evidence on SNAP benefit cliffs and work disincentives?"

python run.py "What are equity implications of AI-driven Medicaid eligibility tools?" \
  --output results/medicaid
```

Outputs are saved to `output/` (or `--output` path):
- `policy_brief.md` — the research brief
- `behavioral_audit.json` — step-by-step behavioral log with flags

---

## Architecture
