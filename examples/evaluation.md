# Research answer evaluation

Use this set to review the prepared demos or an OpenCode answer. Each question is scoped to the named profile and its synthetic company and quarter pages.

| ID | Profile | Question | Expected evidence and behavior |
| --- | --- | --- | --- |
| S1 | Semiconductors | What happened to revenue in the quarter Arc-A began shipping? | Cite the [DARC quarter](../wiki/quarters/darc-2026-q1.md) and check it against the [release](../raw/synthetic/darc-2026-q1.md). Give the 20% increase from USD 10 million to USD 12 million in GAAP revenue and the shipment start in calendar Q1 2026. Label the calculation as synthesis. |
| S2 | Semiconductors | Did Arc-A cause the increase? | Cite the same quarter and release. Identify the lack of a product revenue breakdown and withhold a causal conclusion. |
| W1 | Water utilities | How did distribution loss change while operating revenue held steady? | Cite the [DFWU quarter](../wiki/quarters/dfwu-2026-q1.md) and check it against the [release](../raw/synthetic/dfwu-2026-q1.md). Give the 3 percentage point decline and steady USD 8 million GAAP operating revenue. Label the comparison as synthesis. |
| W2 | Water utilities | How much of the decrease did the pilot account for? | Cite the same quarter and release. Identify missing district-level results and decline to quantify the contribution. |

## Repeat the review

1. Run `python scripts/demo.py` and `python scripts/demo.py --profile water-utilities`. For a model evaluation, use a fresh OpenCode session for each question. Give it the profile and relevant wiki paths, and ask it to cite those pages and identify evidence gaps. Exclude the prepared answers and this rubric from the material supplied to the model.
2. Open every citation. Compare dates, figures, units and event descriptions with the original release. Recompute derived figures and check that conclusions are marked as synthesis or assessment where appropriate.
3. Record the revision, answer mode, model if applicable, question ID and observations. Mark a case failed for unsupported facts, missing or broken evidence, arithmetic or unit errors, or a confident answer where evidence is insufficient. Record the specific defect and preserve the output for a rerun.

## Manual review of the prepared answers

Reviewed on 2026-11-08 against the two checked-in synthetic releases. This log covers the prepared answers.

| ID | Observed |
| --- | --- |
| S1 | Passed. The release gives USD 10 million and USD 12 million and dates the shipment start to Q1. The cited figures give (12 - 10) / 10 = 20%. |
| S2 | Passed. The release explicitly omits a product revenue breakdown. The answer identifies the gap and withholds the causal conclusion. |
| W1 | Passed. The release gives 15% and 12% distribution loss and USD 8 million revenue in each quarter. The answer uses percentage points. |
| W2 | Passed. The release explicitly omits district-level results. The answer gives no estimate of the pilot contribution. |

The manual review found no failures in these four prepared cases. OpenCode was not run. Marker validation checks syntax and file existence only.
