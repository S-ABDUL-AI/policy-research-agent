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
Evidence from multiple states shows that ML-driven benefit eligibility tools
systematically underestimate need in majority-Black and majority-Hispanic
zip codes, primarily through proxy variables that encode historical
underservice patterns...
```

**Behavioral audit (behavioral_audit.json):**
```json
{
  "total_steps": 9,
  "total_input_tokens": 14823,
  "total_output_tokens": 1204,
  "output_length_drift_cv": 0.38,
  "position_change_signals": 1,
  "tool_distribution": {
    "web_search": 3,
    "fetch_url": 3,
    "take_note": 2,
    "write_brief": 1
  },
  "flags": {
    "high_compression": false,
    "high_length_drift": false,
    "position_instability": false,
    "tool_overuse": false
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

```
run.py                   # CLI entry point
agent.py                 # ReAct orchestrator loop
tools/
  definitions.py         # Anthropic tool schemas
  executor.py            # Tool side-effects (search, fetch, notes)
behavioral/
  logger.py              # Per-step behavioral logging + metrics
prompts/
  system.py              # Agent system prompt
```

The agent runs a standard [ReAct](https://arxiv.org/abs/2210.03629) loop using Anthropic's tool use API. Each iteration, the model decides which tool to call; the executor runs it; the behavioral logger records token counts, output lengths, and tool choices for that step.

---

## Model

Default: `claude-haiku-5-5` (same as sycophancy-probe, for cost efficiency and cross-project comparability)

Change in `agent.py` → `MODEL = "claude-sonnet-5-5"` for higher-quality briefs.

---

## Why this matters

Autonomous AI agents operating in high-stakes institutional contexts (benefits eligibility, resource allocation, public health triage) make sequences of decisions under real-world constraints. The behavioral signals tracked here — compression, drift, position instability — are early indicators of the same failure modes that cause downstream harm in those deployments.

This project is a proof-of-concept for **runtime behavioral auditing**: monitoring not just what an agent outputs, but how its behavior changes as it works.

---

*Part of an ongoing research series on constraint-induced behavioral divergence and sycophancy in LLM systems.*
