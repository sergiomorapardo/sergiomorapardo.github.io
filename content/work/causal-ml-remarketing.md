---
title: "Causal ML Remarketing Engine"
description: "An end-to-end decision engine for audience, timing, and content, evaluated against persistent holdouts across eight countries."
translationKey: "causal-remarketing"
weight: 2
category: "Causal ML"
metric: "~US$1M/mo"
metric_label: "statistically significant incremental GMV"
role: "Senior Data Scientist · ML lead"
scale: "~12M monthly users · 8 countries"
period: "2022–2024"
tags: ["Uplift modeling", "Propensity", "Experimentation", "Recommendation"]
---

## The problem

High-volume remarketing can optimize clicks while still sending messages to users who would have purchased anyway. The product needed to decide **who** should receive a message, **when** it should arrive, and **what** to recommend while measuring true incremental impact rather than correlation.

## My role

I built and led the ML remarketing engine for push and email across eight Latin American countries. The work combined causal modeling, personalization, serving architecture, and a sustained program of controlled experimentation.

## Technical approach

- Causal uplift models with LightGBM and scikit-uplift to target persuadable users.
- Open-propensity audience filtering with XGBoost.
- Send-time models to optimize the moment of delivery.
- Price-aware recommendation ranking for message content.
- Recurring campaign strategies for remarketing, cross-sell, and buy-again use cases.

## Experiment design

Together with partner teams, I co-designed more than **38 factorial 2×2 A/B experiments**. Persistent holdout groups made it possible to distinguish incremental GMV from purchases that would have occurred without the intervention.

The program also treated negative evidence as useful: underperforming triggers were retired instead of being kept alive by vanity metrics.

## Outcome

The ML optimizations drove approximately **US$1 million per month in statistically significant incremental GMV** versus holdout. Audience filtering improved conversion by **25%**, while price-aware ranking improved recommended-item conversion by **19%** versus control.

> Results are rounded and described only at the level already disclosed publicly. No customer-level data or proprietary implementation detail is included.

## What this work reinforced

For intervention systems, prediction accuracy is not the business objective. The key question is whether the decision changes an outcome that would not otherwise have happened.
