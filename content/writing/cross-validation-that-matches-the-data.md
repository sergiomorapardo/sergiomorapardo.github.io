---
title: "Cross-validation that matches the data"
description: "A defensible model-selection workflow: choose splits from the data-generating process, keep preprocessing inside each fold, and separate tuning from evaluation."
date: 2026-09-06T00:00:00-05:00
translationKey: "cross-validation-that-matches-the-data"
weight: 2
level: "Intermediate"
topic: "Model evaluation"
repository: "StochasticAITechniquesClass"
repository_url: "https://github.com/sergiomorapardo/StochasticAITechniquesClass"
notebook: "L6_CrossValidation.ipynb"
notebook_url: "https://github.com/sergiomorapardo/StochasticAITechniquesClass/blob/main/Notebooks/L6_CrossValidation.ipynb"
tags: ["Cross-validation", "Scikit-learn", "Evaluation"]
---

Cross-validation is often introduced as a setting: choose five folds and call `cross_val_score`. The more important decision happens earlier. A validation design is a claim about which observations may legitimately stand in for the future.

The source notebook builds that claim progressively, from repeated hold-out experiments to grouped, temporal, stratified, and nested validation. This note condenses the workflow into the decisions that make an evaluation credible.

## Start with the source of dependence

A random split assumes observations can be exchanged without changing the problem. That assumption breaks when examples share a patient, customer, device, document, or time period. The split strategy must preserve the boundary that will exist when the model is used.

| Data situation | Validation choice | What it protects |
| --- | --- | --- |
| Independent observations | K-fold | Reduces dependence on one arbitrary hold-out |
| Classification with uneven classes | Stratified K-fold | Preserves class proportions in each fold |
| Repeated observations by entity | Group K-fold | Keeps each entity in only train or validation |
| Forecasting or ordered events | Time-series split | Prevents training on the future |
| Tuning plus final performance reporting | Nested cross-validation | Separates selection from evaluation |

This table is not a menu of interchangeable techniques. It is a checklist for identifying leakage. If the same patient appears in training and validation, a high score may reward identity recognition rather than clinical generalization. If future records inform past predictions, the experiment answers a question the deployed model will never receive.

## Put preprocessing inside the fold

Scaling, imputation, encoding, and feature selection learn from data. Fitting them once before cross-validation exposes every validation fold to statistics from the other side of the split. Scikit-learn pipelines keep those learned transformations inside the training portion of each fold.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(solver="liblinear")),
])

scores = cross_val_score(
    pipeline,
    X,
    y,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring="roc_auc",
)
```

The pipeline is not just cleaner packaging. During each fold, `StandardScaler` learns a mean and standard deviation only from that fold's training data. The validation rows remain genuinely unseen until scoring.

## Report a distribution, not a lucky split

The notebook first trains logistic regression on the scikit-learn breast-cancer dataset using ten different 80/20 splits. The saved accuracies range from **0.9649 to 0.9825**, with a mean of **0.9763** and a standard deviation of **0.0069**. A five-fold run reports **0.9789 ± 0.0070**.

In this particular execution, five-fold validation does not magically shrink the observed standard deviation. Its value is that every observation participates in validation and the result exposes variation across folds. The honest artifact is the collection of fold scores plus a summary, not the most favorable seed.

The notebook then creates a synthetic classification dataset with 950 majority examples and 50 minority examples. Stratified five-fold validation produces **0.9910 accuracy**, but macro F1 is **0.9460** and ROC AUC is **0.9563**. The gap is the point: the split strategy and the metric answer different questions. Stratification keeps class representation stable; a class-aware metric prevents the majority class from dominating the story.

## Tune without contaminating the estimate

Hyperparameter search reuses validation evidence to choose a model. That makes the winning `best_score_` useful for selection but optimistic as a final estimate. Nested cross-validation creates two loops:

1. The inner loop chooses hyperparameters using only the outer training fold.
2. The outer loop evaluates the complete selection process on data untouched by that choice.

```python
inner_search = GridSearchCV(
    estimator=pipeline_svc,
    param_grid={
        "svc__C": [0.1, 1, 10, 100],
        "svc__kernel": ["linear", "rbf"],
    },
    cv=StratifiedKFold(n_splits=5),
    scoring="roc_auc",
)

outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
nested_scores = cross_val_score(
    inner_search,
    X,
    y,
    cv=outer_cv,
    scoring="roc_auc",
)
```

On the breast-cancer example, the single grid search reports a best mean ROC AUC of **0.9959**. The outer scores from nested validation average **0.9947**, with a standard deviation of **0.0055**. The difference is small here, but the design matters even when the correction is modest.

The notebook closes with a messier Titanic pipeline containing imputation, scaling, one-hot encoding, and a random forest. Its inner grid search reports **0.8678 ROC AUC**. The nested estimate is **0.8600 ± 0.0219**. That outer uncertainty is more informative for planning than a winner selected from 27 hyperparameter combinations.

## Read beyond `best_score_`

`cv_results_` contains the mean, standard deviation, rank, training time, and fold-level evidence for every candidate. In the notebook's support-vector-machine grid, the best result is an RBF model with `C=1` at 0.995916 mean ROC AUC. A linear model with `C=0.1` reaches 0.994856. The raw difference is about 0.0011, smaller than either candidate's fold-to-fold standard deviation.

That does not prove the simpler model is universally better. It does show why the top rank should not end the decision. Latency, calibration, interpretability, memory, and stability can outweigh a difference that is small relative to experimental variation.

## A review checklist

Before accepting a model-selection result, ask:

1. What unit must remain independent between training and evaluation?
2. Does time constrain which examples can be used to predict which others?
3. Are rare classes represented in every fold?
4. Are all learned transformations fitted inside each training fold?
5. Does the metric match the cost of false positives, false negatives, and ranking errors?
6. Was the final estimate kept separate from hyperparameter selection?
7. Are fold scores and variability reported alongside the mean?
8. Was a simple baseline evaluated under the exact same splits?

The notebook examples use teaching datasets, not production evidence. Their durable contribution is the evaluation logic: respect dependence, contain learned preprocessing, align the metric, and reserve untouched data for judging the entire selection process.

> Source boundary: every numeric result in this note comes from the notebook's saved outputs. The review checklist and deployment interpretation synthesize those demonstrations without claiming new experiments.
