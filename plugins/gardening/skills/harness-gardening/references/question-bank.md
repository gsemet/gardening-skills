# Harness Gardening — Question Bank

Questions are organized by **harness dimension**. Each question is designed to
surface a tension or unexamined assumption — not to collect facts.

**Never ask a question whose answer is already in the harness snapshot.**
Never ask questions whose answers are obvious (e.g. "do you have tests?").
The goal is to surface what the user has NOT thought about.

A good question has this property: the user's answer reveals a trade-off
they have not yet consciously made.

## Dimension 1: The Preflight Contract

Questions about what "done" actually means inside the agent loop.

- When the preflight target fails on step 3 of 6, does the agent know to
  rerun only step 3 after a fix — or does it restart from step 1? What is
  the practical cost of that restart?
- Is "preflight passes" the actual completion signal you want agents to use,
  or is there something preflight does NOT check that still matters for correctness?
- If two agents work on different modules in parallel, can they each run preflight independently without interfering?
- What is the expected response time of your harness? Is there a threshold above which agents stop waiting?
- Has anyone deliberately broken the preflight to test whether agents respect the failure signal?

## Dimension 2: Feedback Fidelity

Questions about whether harness failures are informative enough to drive correction.

- When your lint step fails, does the output tell the agent exactly which file, line, and rule to fix?
- If a test fails due to an environment issue, is the error distinguishable from a real code failure?
- What is the worst error message your harness produces today — the one that requires the most human interpretation?
- After a fix, does the agent know which sub-step to rerun, or does it always rerun everything?

## Dimension 3: Harness Granularity

Questions about decomposition within the single preflight target.

- If you could run only one check before declaring "probably fine to commit", which check would it be?
- Are there checks that catch different classes of error? Do agents need a different subset by change type?
- What is the longest-running step in your preflight? Is it always necessary?
- Could your harness express "this file changed → these checks are relevant"?
- Do you have checks that fail for reasons unrelated to the current change?

## Dimension 4: Harness Scalability

Questions about what happens as the project grows.

- At current growth rate, when will your preflight exceed the time budget where agents reliably wait?
- Which step will likely become a bottleneck as the codebase doubles? Is it parallelizable?
- Is there a part of your harness that was fast when the project started but has quietly become slow?
- If you added 10 new modules tomorrow, would the harness automatically cover them?

## Dimension 5: Agent-Harness Alignment

Questions specific to coding agents operating inside the loop.

- When an agent makes a change and the harness fails, what is the maximum retry count before it should ask for help?
- Does your harness distinguish between "the code is wrong" and "the harness configuration is wrong"?
- If an agent modifies a test to make it pass instead of fixing the code, does the harness catch that?
- What happens when an agent runs the harness mid-refactor while the code is intentionally broken?
- Does any part of your harness have side effects? What happens when an agent runs it repeatedly?

## Dimension 6: Harness Discoverability

Questions about whether agents and new humans can find and use the harness.

- If a fresh coding agent cloned this repository, what is the first thing it would do to understand validation?
- Is the preflight command documented in the same file an agent reads first?
- Does anything tell an agent WHEN to run the harness, not just how?
- If the preflight command changed tomorrow, how many files would need updating?

## Dimension 7: Harness Trust

Questions about whether the harness result is a reliable signal.

- How often does preflight pass locally and fail in CI, or vice versa? What causes the divergence?
- Is there a known class of error the harness consistently misses?
- When was the last time code passed preflight but caused a real problem? What did the harness miss?
- Is the harness currently over-checking or under-checking? What evidence supports that?

## Dimension 8: Guide Coverage

Questions about whether inferential guides are backed by computational sensors.
Use the Guide Catalog from the snapshot when it shows sensor gaps.

- Which rule in `AGENTS.md` or `CONSTITUTION.md` have agents violated most recently?
- If an agent silently ignored one rule and the problem only surfaced during human review, which rule was it?
- Do rules that exist because an agent previously broke something now have a computational sensor?

## How to Pick the Next Question

1. Start with Dimension 1 (the preflight contract) — always.
2. After the user's first answer, pick the dimension most likely to reveal a tension based on what was learned.
3. Do not work through a dimension exhaustively — pick the single most probing question.
4. Track which dimensions have been explored in `log.md`.
5. If the snapshot shows sensor gaps, prioritize Dimension 8 early.

## When to Load This Document

Load `question-bank.md` when:
- Choosing the next question in a loop iteration
- Needing to shift dimension after a surprising user answer
- Planning the sequence of a new harness-gardening session
- Keywords: "next question", "what should I ask", "question bank",
  "which dimension", "what to probe next", "question catalog"
