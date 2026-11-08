"""
Policy Research Agent — main orchestrator.
"""

import json
import os
import time
from pathlib import Path

import anthropic

from prompts.system import SYSTEM_PROMPT
from tools.definitions import TOOLS
from tools.executor import ToolExecutor
from behavioral.logger import BehavioralLogger


MODEL = "claude-haiku-5-5"
MAX_STEPS = 20


def run_agent(question: str, output_dir: str = "output") -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    executor = ToolExecutor()
    logger = BehavioralLogger(question)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    messages = [{"role": "user", "content": question}]

    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"{'='*60}\n")

    best_text = ""
    step = 0
    while step < MAX_STEPS and not executor.done:
        step += 1
        t0 = time.perf_counter()

        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        step_duration_ms = (time.perf_counter() - t0) * 1000
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        tool_calls = []
        text_blocks = []

        for block in response.content:
            if block.type == "tool_use":
                tool_calls.append(block)
            elif block.type == "text":
                text_blocks.append(block.text)

        if text_blocks:
            reasoning = " ".join(text_blocks)
            print(f"[Step {step}] {reasoning[:200]}{'...' if len(reasoning) > 200 else ''}")
            if len(reasoning) > len(best_text):
                best_text = reasoning

        if not tool_calls:
            break

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tc in tool_calls:
            tool_name = tc.name
            tool_input = tc.input
            print(f"  → {tool_name}({json.dumps(tool_input)[:80]})")
            result_text, duration_ms = executor.run(tool_name, tool_input)
            if tool_name == "take_note":
                logger.snapshot_notes(executor.notes)
            combined_output = json.dumps(tool_input) + result_text
            logger.log_step(
                tool_called=tool_name,
                tool_input=json.dumps(tool_input),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                output_text=combined_output,
                duration_ms=duration_ms,
            )
            print(f"     ↳ {result_text[:120]}{'...' if len(result_text) > 120 else ''}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": result_text,
            })

        messages.append({"role": "user", "content": tool_results})

        if executor.done:
            break

    if executor._brief is None and best_text:
        executor._brief = best_text
    brief = executor.brief or "[No brief produced]"
    audit = logger.save(f"{output_dir}/behavioral_audit.json")

    brief_path = f"{output_dir}/policy_brief.md"
    with open(brief_path, "w") as f:
        f.write(f"# Policy Brief\n\n**Question:** {question}\n\n---\n\n{brief}\n")

    print(f"\n{'='*60}")
    print("BEHAVIORAL AUDIT SUMMARY")
    print(f"{'='*60}")
    print(f"  Total steps:          {audit['total_steps']}")
    print(f"  Total tokens (in/out):{audit['total_input_tokens']} / {audit['total_output_tokens']}")
    print(f"  Output length drift:  {audit['output_length_drift_cv']} (CV)")
    print(f"  Position change sigs: {audit['position_change_signals']}")
    print(f"  Tool distribution:    {audit['tool_distribution']}")
    print(f"  Flags:                {audit['flags']}")
    print(f"\nBrief saved to:  {brief_path}")
    print(f"Audit saved to:  {output_dir}/behavioral_audit.json")

    return {
        "brief": brief,
        "audit": audit,
        "output_paths": {
            "brief": brief_path,
            "audit": f"{output_dir}/behavioral_audit.json",
        },
    }
