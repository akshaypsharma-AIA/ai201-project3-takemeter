# TakeMeter — NBA Discourse Classifier

## Community
r/nba — Reddit's NBA discussion community. Posts range from stat-heavy 
analysis to emotional reactions to bold opinions, making it ideal for 
discourse quality classification.

## Label Taxonomy

**analysis** — A structured, evidence-based argument using specific stats, 
historical comparisons, or tactical observations. Evidence leads the conclusion.
- "Jokic's assist-to-turnover ratio in playoff games since 2021 is 4.2:1, 
  higher than any center in the last 20 years."
- "The Warriors net rating drops 14 points when Draymond sits."

**hot_take** — A bold opinion stated confidently with little or no supporting 
evidence. Any stats used are cherry-picked or misleading.
- "LeBron would never survive in the 90s."
- "Steph Curry is overrated and everyone knows it."

**reaction** — An immediate emotional response to a game, trade, or injury. 
Expressing a feeling, not making an argument.
- "LET'S GOOOOO NUGGETS ARE CHAMPIONS I CANNOT BELIEVE THIS"
- "I'm actually devastated. That injury just ended our season."

## Data Collection
- **Source:** AI-generated synthetic posts (Claude) — disclosed in AI Usage section
- **Total examples:** 250
- **Split:** 70% train / 15% validation / 15% test

**Label distribution:**
| Label | Count | % |
|---|---|---|
| analysis | 80 | 32% |
| hot_take | 80 | 32% |
| reaction | 90 | 36% |

**3 difficult-to-label examples:**
1. "LeBron has the most playoff losses in NBA history" → hot_take (true stat but cherry-picked — more games = more losses)
2. "Draymond gets away with dirty plays because he plays for the Warriors" → hot_take (emotional but making a claim, not reacting to a specific event)
3. Posts containing specific stats written in emotional tone → borderline analysis/reaction — labeled by dominant intent

## Fine-Tuning Approach
- **Base model:** distilbert-base-uncased (66M parameters)
- **Training:** 3 epochs, learning rate 2e-5, batch size 16
- **Key decision:** Used default hyperparameters — appropriate for 250 examples. 
  Increasing epochs risked overfitting on small dataset.

## Baseline
- **Model:** Groq llama-3.3-70b-versatile (zero-shot)
- **Approach:** Provided label definitions and one example per label in system prompt
- **No training data used**

## Evaluation Report

### Results Comparison
| Model | Accuracy |
|---|---|
| Zero-shot baseline (Groq) | 0.921 |
| Fine-tuned DistilBERT | 0.842 |
| Difference | -0.079 (baseline wins) |

### Per-Class Metrics

**Fine-tuned DistilBERT:**
| Label | Precision | Recall | F1 |
|---|---|---|---|
| analysis | 0.80 | 1.00 | 0.89 |
| hot_take | 1.00 | 0.67 | 0.80 |
| reaction | 0.80 | 0.86 | 0.83 |

**Zero-shot baseline (Groq):**
| Label | Precision | Recall | F1 |
|---|---|---|---|
| analysis | 0.86 | 1.00 | 0.92 |
| hot_take | 0.92 | 1.00 | 0.96 |
| reaction | 1.00 | 0.79 | 0.88 |

### Confusion Matrix (Fine-Tuned Model)

|  | Predicted: analysis | Predicted: hot_take | Predicted: reaction |
|---|---|---|---|
| **True: analysis** | 12 | 0 | 0 |
| **True: hot_take** | 2 | 4 | 6 |
| **True: reaction** | 2 | 0 | 12 |

### Error Analysis

**Pattern 1 — Hot_takes predicted as reaction (6 of 12 hot_takes missed):**
Posts using assertive emotional language ("Period.", "Book it.", "will never") 
were called reaction. The model uses tone as a proxy for label — it hasn't 
learned that hot_takes can be emotionally charged opinions, not just reactions.

**Pattern 2 — Reaction predicted as analysis (2 cases):**
Stat-heavy posts labeled reaction were called analysis. Likely a labeling 
inconsistency in synthetic data — these posts read more like analysis than reaction.

**Pattern 3 — Hot_take predicted as analysis (2 cases):**
"Shaq would average 42 points today" was called analysis. The model sees a 
specific number and treats it as evidence — it cannot distinguish real stats 
from made-up ones used as ammunition.

### Sample Classifications
| Post | True Label | Predicted | Confidence |
|---|---|---|---|
| "Jokic's WAR per season leads second place by more than Durant leads fifth" | analysis | analysis | 0.42 |
| "LET'S GOOOOO NUGGETS ARE CHAMPIONS" | reaction | reaction | high |
| "Kobe was more skilled than Jordan. Jordan more athletic." | hot_take | reaction | 0.37 |
| "Zion is most physically gifted since prime Shaq. Period." | hot_take | reaction | 0.35 |
| "Boston fans are most insufferable fanbase in sports" | hot_take | analysis | 0.36 |

The analysis prediction is reasonable — the post cites specific WAR statistics 
in a comparative structure, exactly matching the analysis definition.

### What the Model Learned vs. What I Intended

**Intended:** Distinguish evidence-based arguments from opinions from emotional reactions.

**Actual:** The model learned surface signals — numbers = analysis, emotional 
language = reaction, leaving hot_take as a residual category it's uncertain about. 
It never learned the deeper distinction: intent and epistemic quality of the argument.

## Reflection on Spec

**Where the spec helped:** The hard edge case requirement in Milestone 1 forced 
me to define the cherry-picked stat decision rule before annotating. That rule 
directly predicted the model's biggest failure mode.

**Where I diverged:** Used synthetic AI-generated data instead of real Reddit 
posts due to Reddit API restrictions. This likely explains why the baseline 
outperformed fine-tuning — LLaMA classifies AI-generated text better than a 
small fine-tuned model.

## AI Usage

1. **Data generation:** Asked Claude to generate 250 realistic NBA posts across 
   three labels. Reviewed all 250 for label accuracy before using. Disclosed 
   as synthetic data throughout.

2. **Failure analysis:** Pasted wrong predictions into Claude to identify patterns. 
   Claude identified the emotional-language-as-reaction pattern. Verified by 
   manually re-reading all 10 wrong predictions — pattern confirmed.