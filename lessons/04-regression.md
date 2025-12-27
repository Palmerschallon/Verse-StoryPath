The Tale of the Line Through the Scatter

One summer, the villagers came to Mira with a simple wish:

“Help us guess tomorrow — not in words, but in numbers.”

So Mira built a learning machine that listened to many paired stories where one number followed another. Temperature and cones sold. Size of a house and price. Weight of a car and miles-per-gallon.

These stories were supervised, because the answers were known.

But before teaching the machine, Mira did something curious:
she set some stories aside.

“These will be for later,” she said.
“For truth must be tested.”

Drawing the line

With the remaining stories, the machine searched for a pattern — a line through the scattered points of life — a way to turn x into y as faithfully as possible.

In the ice-cream shop, it learned:

“As the day grows warmer, cones grow many.”

This was regression — teaching a model to predict a number.

Testing the line

When the machine was ready, Mira brought out the stories she had held back.

She fed the model new x values and listened as it replied with ŷ — its predicted y.

Then she compared ŷ to y —
what was whispered, and what was real.

Sometimes the model was close.
Sometimes it missed.
Every miss was measured.

Mira gave these misses names:

Mean Absolute Error — the average size of the mistakes, ignoring whether they were too high or too low.

Mean Squared Error — where greater mistakes weighed heavier, because some errors matter more than others.

Root Mean Squared Error — returning those weighted errors back to the language of the real world.

And finally,

R² — the proportion of the world that the line had truly captured.
The closer to 1, the more of the story the model understood — and the less was chaos and chance.

The long craft of improvement

Mira did not stop after one attempt.

She changed which features she used.
She tried different algorithms.
She tuned the settings with patience.

Again and again, the cycle repeated:

train
test
measure
refine

until the model’s voice was steady enough to trust.

Not perfect.
Just honest.

The moral

Regression is the craft of teaching a model to predict numbers drawn from life — and the humility to measure how wrong it is, again and again, until the errors become small enough to live with.

Good models are not built once.
They are tended.

For more detail, see the official Microsoft Learn lesson:
https://learn.microsoft.com/en-us/training/modules/fundamentals-machine-learning/4-regression
