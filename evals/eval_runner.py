#!/usr/bin/env python3
"""
EA Agent Eval Suite

Tests two things:
  1. Routing accuracy  — given a user phrase, does the right skill get invoked?
  2. Behavioral quality — given a scenario, does the EA's response meet the criteria?

Routing uses claude-haiku-4-5 (fast/cheap) for classification.
Behavioral uses claude-haiku-4-5 for the agent response and claude-sonnet-4-6 as the judge.

Usage:
    python evals/eval_runner.py [--pass-threshold 80] [--routing-only] [--behavioral-only]

Exit codes:
    0 — all evals passed threshold
    1 — below threshold or error
"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
ROUTING_MODEL = "claude-haiku-4-5-20251001"   # Cheap classifier
AGENT_MODEL   = "claude-haiku-4-5-20251001"   # Agent-under-test responses
JUDGE_MODEL   = "claude-sonnet-4-6"           # Judge needs stronger reasoning

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT     = Path(__file__).parent.parent
SKILLS_DIR    = REPO_ROOT / "skills"
SCENARIOS_DIR = Path(__file__).parent / "scenarios"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_skill_descriptions() -> dict[str, str]:
    """Return {skill_name: description} from each SKILL.md frontmatter."""
    skills = {}
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        content = skill_file.read_text()
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        frontmatter = parts[1]

        name_match = re.search(r'^name:\s*(.+)', frontmatter, re.MULTILINE)
        # Description may be single or multi-line, quoted or unquoted
        desc_match = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', frontmatter, re.MULTILINE)
        if name_match and desc_match:
            skills[name_match.group(1).strip()] = desc_match.group(1).strip()
    return skills


def load_skill_content(skill_name: str) -> str:
    """Return full SKILL.md text for a given skill name."""
    path = SKILLS_DIR / skill_name / "SKILL.md"
    return path.read_text() if path.exists() else ""


def print_section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


# ---------------------------------------------------------------------------
# Routing evals
# ---------------------------------------------------------------------------

def run_routing_evals(
    client: anthropic.Anthropic,
    scenarios: list[dict],
    skill_descriptions: dict[str, str],
) -> tuple[int, int, list[dict]]:
    """
    For each scenario, ask Claude (with all skill descriptions in context)
    which skill it would invoke. Compare to expected_skill.
    """
    skill_list = "\n".join(
        f"- {name}: {desc[:300]}" for name, desc in skill_descriptions.items()
    )

    system_prompt = (
        "You are an EA agent router. Given a user message, respond with ONLY the "
        "exact skill name you would invoke — nothing else, no punctuation, no explanation.\n\n"
        f"Available skills:\n{skill_list}"
    )

    passed, failed = 0, 0
    results = []

    for scenario in scenarios:
        phrase    = scenario["phrase"]
        expected  = scenario["expected_skill"].strip().lower()

        response = client.messages.create(
            model=ROUTING_MODEL,
            max_tokens=30,
            system=system_prompt,
            messages=[{"role": "user", "content": phrase}],
        )

        actual = response.content[0].text.strip().lower().strip("\"'")
        ok = actual == expected

        if ok:
            passed += 1
        else:
            failed += 1

        results.append({"phrase": phrase, "expected": expected, "actual": actual, "passed": ok})

    return passed, failed, results


# ---------------------------------------------------------------------------
# Behavioral evals
# ---------------------------------------------------------------------------

def judge_response(
    client: anthropic.Anthropic,
    scenario_name: str,
    skill_name: str,
    user_message: str,
    context: str,
    agent_response: str,
    criteria: list[str],
) -> tuple[bool, str]:
    """
    Ask the judge LLM whether the agent_response satisfies ALL criteria.
    Returns (passed: bool, verdict: str).
    """
    criteria_text = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(criteria))

    prompt = (
        f"You are evaluating an EA agent's response to ensure quality.\n\n"
        f"Scenario: {scenario_name}\n"
        f"Skill under test: {skill_name}\n"
        f"Context given to agent: {context}\n"
        f"User message: \"{user_message}\"\n\n"
        f"Agent response:\n---\n{agent_response}\n---\n\n"
        f"Criteria — ALL must be satisfied for a PASS:\n{criteria_text}\n\n"
        "Respond with exactly one of:\n"
        "PASS - <one sentence why it passes>\n"
        "FAIL - <one sentence identifying which criterion failed and why>"
    )

    response = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=120,
        messages=[{"role": "user", "content": prompt}],
    )

    verdict = response.content[0].text.strip()
    return verdict.upper().startswith("PASS"), verdict


def run_behavioral_evals(
    client: anthropic.Anthropic,
    scenarios: list[dict],
) -> tuple[int, int, list[dict]]:
    """
    For each scenario, run the skill as an agent and judge the response.
    """
    passed, failed = 0, 0
    results = []

    for scenario in scenarios:
        name         = scenario["name"]
        skill_name   = scenario["skill"]
        user_message = scenario["user_message"]
        context      = scenario.get("context", "No additional context.")
        criteria     = scenario["criteria"]

        skill_content = load_skill_content(skill_name)
        if not skill_content:
            print(f"  [SKIP] {name} — skill '{skill_name}' not found")
            continue

        system_prompt = (
            f"You are an EA agent. Follow the skill instructions below.\n\n"
            f"IMPORTANT: You have no filesystem or tool access in this evaluation. "
            f"The Context block below is the complete source of truth — treat it as if "
            f"you have already successfully read EA_PROFILE.md and any relevant files. "
            f"Do not attempt to find, read, or write any files. Proceed directly from "
            f"the context provided.\n\n"
            f"Context: {context}\n\n"
            f"{skill_content}"
        )

        agent_resp = client.messages.create(
            model=AGENT_MODEL,
            max_tokens=600,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        response_text = agent_resp.content[0].text.strip()

        ok, verdict = judge_response(
            client, name, skill_name, user_message,
            context, response_text, criteria
        )

        if ok:
            passed += 1
        else:
            failed += 1

        results.append({
            "name": name,
            "skill": skill_name,
            "passed": ok,
            "verdict": verdict,
            "response_preview": response_text[:300] + "…" if len(response_text) > 300 else response_text,
        })

    return passed, failed, results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="EA Agent Eval Suite")
    parser.add_argument("--pass-threshold", type=int, default=80,
                        help="Minimum overall pass rate %% required (default: 80)")
    parser.add_argument("--routing-only",   action="store_true")
    parser.add_argument("--behavioral-only", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    skill_descriptions = load_skill_descriptions()
    print(f"Loaded {len(skill_descriptions)} skills: {', '.join(skill_descriptions.keys())}")

    total_passed = 0
    total_failed = 0

    # ------------------------------------------------------------------
    # Routing evals
    # ------------------------------------------------------------------
    if not args.behavioral_only:
        routing_file = SCENARIOS_DIR / "routing.yaml"
        if routing_file.exists():
            routing_scenarios = yaml.safe_load(routing_file.read_text())
            print_section(f"Routing Evals ({len(routing_scenarios)} scenarios)")

            p, f, results = run_routing_evals(client, routing_scenarios, skill_descriptions)
            total_passed += p
            total_failed += f

            for r in results:
                status = "PASS" if r["passed"] else "FAIL"
                label  = f"\"{r['phrase'][:55]}\""
                print(f"  [{status}] {label}")
                if not r["passed"]:
                    print(f"         expected={r['expected']}  got={r['actual']}")

            print(f"\n  Routing: {p}/{p + f} passed")

    # ------------------------------------------------------------------
    # Behavioral evals
    # ------------------------------------------------------------------
    if not args.routing_only:
        behavioral_file = SCENARIOS_DIR / "behavioral.yaml"
        if behavioral_file.exists():
            behavioral_scenarios = yaml.safe_load(behavioral_file.read_text())
            print_section(f"Behavioral Evals ({len(behavioral_scenarios)} scenarios)")

            p, f, results = run_behavioral_evals(client, behavioral_scenarios)
            total_passed += p
            total_failed += f

            for r in results:
                status = "PASS" if r["passed"] else "FAIL"
                print(f"  [{status}] {r['name']}")
                if not r["passed"]:
                    print(f"         {r['verdict']}")
                    print(f"         Response: {r['response_preview'][:120]}…")

            print(f"\n  Behavioral: {p}/{p + f} passed")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = total_passed + total_failed
    if total == 0:
        print("\nNo evals ran — check that scenario files exist in evals/scenarios/")
        sys.exit(1)

    pass_rate = int((total_passed / total) * 100)

    print_section("Summary")
    print(f"  Total:     {total_passed}/{total} passed ({pass_rate}%)")
    print(f"  Threshold: {args.pass_threshold}%")

    if pass_rate >= args.pass_threshold:
        print(f"  Result:    PASSED\n")
        sys.exit(0)
    else:
        print(f"  Result:    FAILED — below {args.pass_threshold}% threshold\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
