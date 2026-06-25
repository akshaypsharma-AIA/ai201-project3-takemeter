# TakeMeter Planning Doc

## Community

**Chosen community:** r/nba (Reddit)

**Why this community:** r/nba has thousands of daily posts from fans with
wildly different levels of basketball knowledge — casual viewers, superfans,
and stat-obsessed analysts all posting in the same place. This creates natural
variance in discourse quality, making it ideal for a classification task.
The distinction between structured argument and emotional reaction is something
regular community members actively debate and care about.

## Labels

**analysis**
A post that takes a structured, evidence-based approach to understanding
a player, team, or game. Uses specific stats, historical comparisons, or
tactical observation. The goal is to uncover or explain something, not
to win an argument. Relatively unbiased — the evidence leads the conclusion.

Examples:
- "Jokic's assist-to-turnover ratio in playoff games since 2021 is 4.2:1,
  higher than any center in the last 20 years. His passing fundamentally
  changes how Denver runs pick-and-roll coverage."
- "The Warriors' net rating drops 14 points when Draymond sits. That's
  not about scoring — it's about defensive positioning and rotations."

**hot_take**
A bold opinion stated confidently with little or no supporting evidence.
Takes no effort to produce — anyone can have one. The conclusion comes
first, the "evidence" (if any) is selected to sound credible, not to
genuinely reason toward an answer.

Examples:
- "LeBron would never survive in the 90s. Jordan would have shut him down
  every single game."
- "Steph Curry is overrated and everyone knows it."

**reaction**
An immediate emotional response to something that just happened — a game,
a trade, an injury. Expressing a feeling in the moment, not making an
argument.

Examples:
- "LET'S GOOOOO NUGGETS ARE CHAMPIONS I CANNOT BELIEVE THIS"
- "I'm actually devastated. That injury just ended our season."

## Hard Edge Cases

**The cherry-picked stat problem:**
The hardest edge case is a post that cites a real stat but uses it
selectively to support an emotional claim rather than to genuinely analyze.

Decision rule: To qualify as `analysis`, the evidence must be complete
and unbiased — it leads the conclusion. If a stat is cherry-picked,
partial, or selected to win an argument rather than uncover truth,
the post is `hot_take` regardless of whether it contains numbers.

Example:
- "LeBron has the most playoff losses of any player in NBA history" → `hot_take`
  (true stat, but misleading — more games played = more losses)

**The reaction + opinion problem:**
Some posts express emotion AND make a claim at the same time.

Decision rule: Ask "what is this post primarily doing?" If the dominant
purpose is expressing a feeling in the moment → `reaction`. If the
dominant purpose is making a claim (even without evidence) → `hot_take`.

Example:
- "I'm so angry, this ref is the worst in the league" → `reaction`
  (anger is the point, the claim is secondary)
  
  ## Data Collection Plan

Source: r/nba Reddit JSON API (no auth required)
Method: Python script hitting reddit.com/r/nba/hot.json and /comments.json
Target: 200 posts/comments total
Distribution goal: 50 analysis, 80 hot_take, 70 reaction
Note: analysis posts are rare — will actively search for stat-heavy threads

## Evaluation Metrics

- Overall accuracy (both models)
- Per-class F1 score (handles imbalanced labels better than accuracy alone)
- Confusion matrix (shows which label pairs get confused)

F1 chosen over accuracy because our labels aren't perfectly balanced —
a model that always predicts hot_take would look 40% accurate but be useless.

## Definition of Success

Fine-tuned model beats zero-shot baseline by at least 10 percentage points
overall accuracy. Per-class F1 above 0.60 for all three labels.

## AI Tool Plan

- Label stress-testing: used Claude to generate edge case posts before annotation
- Annotation assistance: Claude pre-labels batches, human reviews every example
- Failure analysis: paste wrong predictions into Claude to find patterns