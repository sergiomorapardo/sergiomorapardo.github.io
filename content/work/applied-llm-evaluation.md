---
title: "Applied LLM Evaluation for Recommendations"
description: "An offline evaluation methodology for retrieval and LLM-assisted recommendation systems, built around ground truth and uncertainty."
translationKey: "llm-evaluation"
weight: 4
category: "Applied LLMs"
metric: "P/R@K"
metric_label: "retrieval quality with bootstrap confidence intervals"
role: "Applied research lead"
scale: "Personalized recommendation systems"
period: "2024–2026"
tags: ["LLMs", "Evaluation", "Retrieval", "MCP", "Bootstrap"]
---

## The problem

LLM prototypes can appear persuasive without being reliable. For personalized recommendations, the team needed an evaluation method that could separate candidate-retrieval quality from generation quality and make regressions visible before a live experiment.

## My role

I led applied research on LLM systems for personalized recommendations and established the team’s initial offline evaluation methodology. I also guided the design of an MCP-based tool layer for supplying recommendation context to LLM-generated notifications.

## Evaluation approach

- Built ground-truth harnesses for repeatable offline comparisons.
- Evaluated candidate retrieval with **Precision@K and Recall@K**.
- Used bootstrap confidence intervals to express uncertainty instead of reporting a single unstable score.
- Separated retrieval failures from generation failures so changes could be diagnosed at the right layer.
- Structured the tool boundary so the LLM received controlled, observable recommendation inputs.

## System boundary

The MCP-based layer was designed to expose recommendation tools and contextual data through a stable contract. This kept product logic outside the prompt, made tool calls observable, and provided a clearer path to evaluation and governance.

## Outcome

The work established a reusable methodology for evaluating LLM-assisted recommendation systems before online testing and informed the technical design of personalized, LLM-generated push notifications.

> This case describes methodology and system boundaries only. Prompts, internal datasets, and proprietary components are not disclosed.

## What this work reinforced

An LLM evaluation should identify *where* a system failed, quantify uncertainty, and remain close enough to the product decision that offline improvement has a credible path to online value.

