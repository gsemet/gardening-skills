# Harness Gardening — Synthesis Guide

Use this only when the user asks for synthesis or says "what should I change?"
**Do not produce this output prematurely.** It requires at least 3 loop iterations
with substantive user answers to be meaningful.

## What a Good Synthesis Is NOT

- Not a list of well-known best practices
- Not "add a linter" or "split your tests into fast and slow"
- Not a generic maturity model scorecard

## What a Good Synthesis IS

A **Tensions Map**: a precise articulation of the trade-offs this specific
project faces, derived from evidence gathered in the loop, with the decision
space laid out — but no recommendation. The user decides.

## Tensions Map Structure

For each tension discovered, fill in this structure:

### Tension N: `<Short name>`

**What was observed** (from snapshot + user answers):
> _[Specific evidence: file path, duration, quote, or explicit user statement]_

**The friction it creates**:
> _[What slows down, breaks, misleads, or fails — for agents specifically]_

**The tension**:
> _[Two legitimate values or goals in conflict — not one right and one wrong]_

**Decision space**:

| Path A | Path B |
|--------|--------|
| What it optimizes for | What it optimizes for |
| What it sacrifices | What it sacrifices |
| What it requires to implement | What it requires to implement |

**Leverage estimate**: High / Medium / Low
_(How much does resolving this improve the agent loop, relative to effort?)_

## Example Tensions (for reference only — do not copy-paste into output)

### Example: Monolithic vs Decomposed Preflight

**Tension**: A single `just preflight` is discoverable and simple for agents,
but as it grows it forces full re-runs for small changes.

**Decision space**:
| Keep monolithic | Decompose into sub-targets |
|---|---|
| One command, no agent confusion | Finer-grained retry after fix |
| Easy to document | Requires agents to select the relevant target |
| Accumulates cost silently | Requires an explicit dependency graph |

### Example: Harness Coverage vs Speed

**Tension**: Adding e2e or performance checks improves correctness signal
but pushes total time past the threshold where agents reliably wait.

**Decision space**:
| Full suite in preflight | Fast path + deferred checks |
|---|---|
| Single completion signal | Two classes of "done" |
| Slower loop | Faster loop with higher deferred-failure risk |
| Simpler to document | Requires an explicit full-check contract |

## Output Format

After stating each tension, ask the user:

> "Does this tension match your reality? Is there context that changes how you see it?"

Only after confirming each tension is accurate, ask:

> "Which of these tensions has the highest cost for you right now?"

That answer drives the next loop iteration or ends the session.

## Upgrade Candidates Appendix

**Only produce this section if the Guide Catalog contains rules with no computational
sensor backup that are classified as `structural` (formalizable).**

This appendix is separate from the tensions map. It does not present trade-offs — it
presents direct opportunities to harden inferential controls into computational ones.

### Format

For each candidate, fill in this structure:

### Upgrade Candidate N: `<Rule Snippet>`

**Source**: `<guide file path>` (line X / section Y)
**Gap**: This rule is currently enforced only as an inferential guide. No step in the
Sensor Catalog catches violations computationally.
**Judgment**: `structural` — the rule is precise enough to be formalized.
**Candidate tool**: `<specific tool name>`

## Output Ordering

After confirming the tensions map is accurate, present the Upgrade Candidates appendix
as a separate section. Say:

> "In addition to the tensions above, I found N upgrade candidates — inferential guide
> rules that are precise enough to be enforced by a computational sensor. These are not
> trade-offs: adding the sensor removes a blind spot at low cost."

Then list each candidate.

## When to Load This Document

Load `synthesis-guide.md` when:
- The user asks "what should I change?", "give me a plan", or "summarize findings"
- At least 3 loop iterations have produced substantive answers
- Preparing to present the Tensions Map
- Keywords: "synthesis", "findings", "tensions map", "what to change",
  "improvement plan", "trade-offs", "decisions", "summarize"
