---
title: "Evaluación de LLMs aplicados a recomendación"
description: "Metodología de evaluación offline para retrieval y recomendación asistida por LLMs, construida alrededor de ground truth e incertidumbre."
translationKey: "llm-evaluation"
weight: 4
category: "LLMs aplicados"
metric: "P/R@K"
metric_label: "calidad de retrieval con intervalos bootstrap"
role: "Líder de investigación aplicada"
scale: "Sistemas personalizados de recomendación"
period: "2024–2026"
tags: ["LLMs", "Evaluación", "Retrieval", "MCP", "Bootstrap"]
---

## El problema

Los prototipos con LLMs pueden parecer convincentes sin ser confiables. Para recomendaciones personalizadas, el equipo necesitaba una metodología que separara la calidad del retrieval de la calidad de generación y permitiera detectar regresiones antes de un experimento online.

## Mi rol

Lideré investigación aplicada en sistemas LLM para recomendaciones personalizadas y establecí la metodología inicial de evaluación offline del equipo. También orienté el diseño de una capa de herramientas basada en MCP para proporcionar contexto de recomendación a notificaciones generadas con LLMs.

## Enfoque de evaluación

- Construcción de ground-truth harnesses para comparaciones offline reproducibles.
- Evaluación del retrieval mediante **Precision@K y Recall@K**.
- Uso de intervalos de confianza bootstrap para expresar incertidumbre.
- Separación de fallas de retrieval y generación para diagnosticar la capa correcta.
- Definición de una frontera controlada y observable para las herramientas utilizadas por el LLM.

## Frontera del sistema

La capa basada en MCP se diseñó para exponer herramientas y contexto mediante un contrato estable. Esto mantuvo la lógica de producto fuera del prompt, volvió observables las llamadas y creó un camino más claro hacia evaluación y gobierno.

## Resultado

El trabajo estableció una metodología reutilizable para evaluar sistemas de recomendación asistidos por LLMs antes de pruebas online e informó el diseño técnico de notificaciones personalizadas generadas mediante LLMs.

> El caso describe únicamente la metodología y las fronteras del sistema. No se divulgan prompts, datasets internos ni componentes propietarios.

## Aprendizaje

Una evaluación de LLMs debe identificar *dónde* falló el sistema, cuantificar la incertidumbre y permanecer lo suficientemente cerca de la decisión de producto para que una mejora offline tenga un camino creíble hacia valor online.
