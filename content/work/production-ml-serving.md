---
title: "Production ML Serving Architecture"
description: "A hybrid batch and real-time architecture turning model scores, live behavior, and campaign rules into low-latency personalization decisions."
translationKey: "production-serving"
weight: 3
category: "ML systems"
metric: "~12M"
metric_label: "monthly users served across the region"
role: "Architecture owner"
scale: "Batch + real time · 8 countries"
period: "2022–2024"
tags: ["MLOps", "BigQuery", "APIs", "Streaming", "Monitoring"]
---

## The problem

Personalized messaging required fresh behavioral context and low-latency decisions, but many useful ML features and scores were most reliable and economical to compute in batch. The serving design needed to connect both worlds without making campaign delivery depend on slow analytical queries.

## My role

I designed the production serving architecture and its decision flow, aligning model computation, storage, APIs, session events, and product rules around the latency and reliability requirements of push and email delivery.

## System design

<div class="system-flow" role="img" aria-label="BigQuery batch scoring flows to a low-latency feature store, prediction APIs, a real-time session engine, and personalized decisions">
  <span>BigQuery<br><small>batch scoring</small></span><b>→</b>
  <span>Key-value store<br><small>low latency</small></span><b>→</b>
  <span>Prediction APIs<br><small>decision access</small></span><b>→</b>
  <span>Session engine<br><small>real-time events</small></span><b>→</b>
  <span>Push & email<br><small>personalized action</small></span>
</div>

- Batch jobs produced stable model scores in BigQuery.
- Scores were loaded into a low-latency key-value store instead of queried from the warehouse at request time.
- Prediction APIs exposed the decision inputs to downstream services.
- A real-time event-streaming session engine combined stored predictions with live behavior to decide audience, timing, and content.

## Operating principles

The architecture separated expensive model computation from latency-sensitive decisioning. It also provided clear boundaries for monitoring data freshness, API availability, decision volume, and model behavior.

## Outcome

The system served personalized push and email decisions to approximately **12 million monthly users across eight countries**, supporting the experimentation and causal measurement program described in the remarketing case study.

> This is a conceptual representation. Infrastructure names, internal schemas, and proprietary implementation details are intentionally omitted.

