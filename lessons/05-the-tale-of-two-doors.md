## The Tale of Two Doors

![The Tale of Two Doors](../images/05-two-doors.png)

One autumn, the villagers came to Mira with a more pointed request.

"We don't need a number this time," they said.
"We need a **decision**. Yes or no. Safe or at risk. One door or the other."

Mira nodded.

"This is still supervised learning," she said.
"But now the answer is a **class** — one of two possibilities."

This was **binary classification**.

### Learning the shape of yes and no

The villagers brought many examples.

Blood glucose and diagnosis.
Transactions and fraud.
Signals and danger.

Each story ended in one of two outcomes:
1 or 0.
True or false.
Yes or no.

Mira trained a model — not to predict a number —
but to estimate the **probability** that a case belonged to the "yes" door.

The model spoke probability, from 0 to 1.

And Mira said,

"When the probability rises above a chosen line — the **threshold** — we will call it yes.
Below it, no."

The line was often set at 0.5 — but it could be moved, depending on what mattered most.

### Holding truth aside

As always, Mira held back some stories whose answers she already knew.
Later, she would test the model against them.

For each case, the model whispered either:

"Yes — the door opens."

or

"No — it does not."

Then Mira compared what the model predicted (ŷ)
to what was real (y).

### Four kinds of truth

She arranged the outcomes into a small square — a **confusion matrix**.

* When the model said "no" — and reality agreed — it was a **true negative**.
* When it said "yes" — and reality agreed — a **true positive**.

Truth formed the diagonal.

But sometimes the model was wrong.

* A **false positive** — it cried "yes" when the truth was "no."
* A **false negative** — it whispered "no" when the truth was "yes."

These errors mattered — sometimes terribly so.

So Mira measured carefully.

### More than one kind of "good"

First, she counted **accuracy** — the proportion of all predictions that were correct.

Useful, but incomplete.

"Imagine," she said,
"if illness is rare — a model that always predicts 'no' will look accurate,
while being blind to those most in need."

So she looked deeper.

**Recall** asked:

"Of all the real 'yes' cases,
how many did the model actually catch?"

**Precision** asked:

"Of all the 'yes' cases the model predicted,
how many were truly yes?"

Sometimes recall mattered most — like finding illness early.
Sometimes precision mattered most — like avoiding false accusation.

To balance the two, Mira used the **F1-score**,
a single number that honored both.

### The curve of every possibility

Then Mira did one more thing —
she slid the threshold up and down,
watching recall and false alarms change together.

She traced these across a chart — a **ROC curve** —
and measured the **Area Under the Curve (AUC)**.

A model that guessed at random would score 0.5.
A perfect one, 1.0.

Most real ones lived humbly between.

### And still — the work continues

As with regression, Mira repeated the dance:

train
validate
measure
refine

because in real life, decisions carry weight —
and binary choices deserve careful thought.

---

## The moral

Binary classification is the craft of teaching a model to choose between two doors —
not just by guessing,
but by weighing uncertainty,
honoring risk,
and measuring every mistake with honesty.

Good judgment, like good models,
is rarely simple —
but it can be made wise.

---

For more detail, see the official Microsoft Learn lesson:
[Binary Classification](https://learn.microsoft.com/en-us/training/modules/fundamentals-machine-learning/5-binary-classification)
