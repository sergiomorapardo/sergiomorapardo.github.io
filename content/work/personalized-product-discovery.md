---
title: "Personalized Product Discovery & Ranking"
description: "Replacing a static affiliate landing page with a continuous, personalized discovery feed, measured through a multi-country controlled experiment."
translationKey: "personalized-discovery"
weight: 1
category: "Ranking"
metric: "+20–26%"
metric_label: "engagement lift across the funnel"
role: "Technical lead"
scale: "~5.2M sessions · 4 countries"
period: "2024–2026"
tags: ["Recommendation", "Ranking", "A/B testing", "Product discovery"]
---

## The problem

Affiliate product discovery depended on a static, curated landing experience. That limited the number of products users could explore and left little room for relevance to adapt to each session.

The product opportunity was not simply to train a ranking model. It was to redesign the discovery system and prove, under controlled conditions, that personalization created incremental value across the funnel.

## My role

I led the ML design for ranking and discovery, partnering across product and engineering to move from a curated landing to a continuous personalized feed. My contribution covered problem framing, ranking signals, experiment design, technical review, and interpretation of the results.

## Technical approach

- Created a continuous candidate and product-scoring flow instead of a fixed collection.
- Incorporated purchase-propensity and price-ranking signals into discovery decisions.
- Connected shared affiliate links to downstream orders across web and app, producing a consistent attribution layer.
- Used the attribution pipeline as the analytical source of truth for controlled experiments across multiple placements.

## Experiment design

The new experience was evaluated against the static control in an A/B test spanning approximately **5.2 million sessions in four countries**. Evaluation covered several stages of the funnel, including clicks, intent, shares, and the conversion of newly generated affiliate links.

## Outcome

The personalized feed increased engagement by **20–26% across the funnel** and improved conversion on newly generated affiliate links by **17% versus control**.

> Public case study based on high-level, previously disclosed information. Internal implementation details and proprietary data are intentionally excluded.

## What this work reinforced

A ranking system is only useful when its objective, attribution, serving path, and experimental unit agree. The measurement architecture was as important as the model itself.
