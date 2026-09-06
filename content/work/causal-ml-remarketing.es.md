---
title: "Motor de remarketing con ML causal"
description: "Motor de decisiones de extremo a extremo para audiencia, momento y contenido, evaluado contra holdouts persistentes en ocho países."
translationKey: "causal-remarketing"
weight: 2
category: "ML causal"
metric: "~US$1M/mes"
metric_label: "de GMV incremental estadísticamente significativo"
role: "Senior Data Scientist · ML lead"
scale: "~12M de usuarios mensuales · 8 países"
period: "2022–2024"
tags: ["Uplift", "Propensión", "Experimentación", "Recomendación"]
---

## El problema

El remarketing de gran volumen puede optimizar clics y, aun así, contactar usuarios que habrían comprado sin la intervención. El producto debía decidir **quién** debía recibir un mensaje, **cuándo** enviarlo y **qué** recomendar, midiendo impacto incremental real en lugar de correlación.

## Mi rol

Construí y lideré el motor de remarketing con ML para push y email en ocho países de Latinoamérica. El trabajo combinó modelado causal, personalización, arquitectura de serving y un programa sostenido de experimentación controlada.

## Enfoque técnico

- Modelos de causal uplift con LightGBM y scikit-uplift para identificar usuarios persuadibles.
- Filtro de audiencia mediante propensión de apertura con XGBoost.
- Modelos de send-time para optimizar el momento del envío.
- Ranking sensible al precio para el contenido recomendado.
- Estrategias recurrentes para remarketing, cross-sell y buy-again.

## Diseño experimental

En conjunto con los equipos involucrados, codiseñé más de **38 experimentos A/B factoriales 2×2**. Los grupos holdout persistentes permitieron distinguir GMV incremental de compras que habrían ocurrido sin la intervención.

El programa también trató la evidencia negativa como información útil: los triggers con resultados adversos se retiraron en lugar de sostenerlos mediante métricas de vanidad.

## Resultado

Las optimizaciones generaron aproximadamente **US$1 millón mensual de GMV incremental estadísticamente significativo** frente al holdout. El filtrado de audiencia mejoró la conversión **25%** y el ranking sensible al precio aumentó **19%** la conversión de ítems recomendados frente al control.

> Los resultados están redondeados y descritos únicamente al nivel previamente divulgado. No se incluyen datos de usuarios ni detalles propietarios.

## Aprendizaje

En sistemas de intervención, la precisión predictiva no es el objetivo del negocio. La pregunta importante es si la decisión modifica un resultado que de otro modo no habría ocurrido.

