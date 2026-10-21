# Causal Inference interview question bank (DS + Economist)

Based on the uploaded `Causal Inference Notion(1).docx` (154 pages). The main concepts were reorganized and edited for accuracy. Added questions are labeled in the webpage.

**Count:** 130 questions, 6 topic tabs; 260 collapsible answer sections; 47 questions marked as interview additions (including 15 dedicated DML deep-dive questions).

## Installation in WeiToLearning

1. Copy `causal_inference_interview_question_bank_double_ml.qmd` to `WeiToLearning/knowledge/question-bank/`.
2. Open your root `index.qmd` in VS Code and link the Causal Inference category to `knowledge/question-bank/causal_inference_interview_question_bank_double_ml.qmd`.
3. From the WeiToLearning project folder run `quarto preview`; check the six Tabs, callout accordions, MathJax and Python blocks.
4. Run `quarto render`, then commit/push through GitHub Desktop.

The input `.docx` includes some formulas and diagrams that were embedded as images; this source file is a curated interview-oriented rewrite and does not reproduce all embedded diagrams. See the original document for those figures.

## Topic counts

| Tab | Easy | Medium | Hard | Total |
|---|---:|---:|---:|---:|
| Causal Foundations & Regression | 9 | 16 | 8 | 33 |
| Matching & Propensity Scores | 2 | 6 | 8 | 16 |
| IV & Regression Discontinuity | 2 | 6 | 9 | 17 |
| Panel Data, DiD & Synthetic Control | 3 | 7 | 10 | 20 |
| Double ML & Causal ML | 4 | 7 | 12 | 23 |
| Interview Case Studies & Traps | 2 | 6 | 13 | 21 |

**Key corrections:** FWL doesn't remove unobserved confounding; heteroskedasticity-robust vs cluster-robust inference; mediator/collider bias; correct LATE interpretation; conditional parallel trends and heterogeneous staggered-treatment effects; matching SE caveats; DML cross-fitting and orthogonal moments. The original notes are a source, not a guarantee of correctness.

**QA:** Markdown parse / structural checks and the displayed Python code were validated. Native Quarto browser rendering should also be checked on your Mac with `quarto preview`.
