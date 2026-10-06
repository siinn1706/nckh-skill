# Causal claims and identification

Prediction, association, intervention contrast and mechanism answer different
questions. Accurate rankings, SHAP explanations, topology or correlation do not
by themselves identify a root cause or causal effect.

State the causal estimand and identification logic before causal language.
Describe well-defined intervention/comparator, population, outcome, time horizon,
consistency, exchangeability, positivity/overlap, interference and measurement
assumptions when relevant. Randomization addresses its design conditions; an
estimated intervention effect does not automatically establish a mechanism.

Inspect common-cause confounding, selection/attrition, collider conditioning,
reverse causation, measurement error and time-varying treatment/confounding.
More covariates are not automatically better. Distinguish confounders, mediators
and effect modifiers relative to the specified contrast; document domain knowledge
and sensitivity alternatives instead of treating model adjustments as proof.

Negative-control exposures/outcomes require a defensible exclusion and shared
bias rationale. A control can reveal a problem under assumptions; a null result
does not certify absence of all bias or quantify the target effect's bias.

Calibrate claims to design evidence and uncertainty. Without identification,
report observed association, predictive performance or a root-cause hypothesis.
With a justified design, disclose the assumptions and limitations of an estimated
causal contrast. A lexical claim check or complete reporting checklist cannot
certify design validity, ethics or scientific acceptance.

This independently authored reference uses reviewed K-Dense hypothesis-generation
causal-claim anatomy and retains method/domain review as separate gates. No
upstream linter, causal score or model-generated scientific verdict is imported.
