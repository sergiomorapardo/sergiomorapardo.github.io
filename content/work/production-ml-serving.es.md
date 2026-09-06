---
title: "Arquitectura de serving para ML en producción"
description: "Arquitectura híbrida batch y tiempo real que convierte scores, comportamiento en vivo y reglas en decisiones de personalización de baja latencia."
translationKey: "production-serving"
weight: 3
category: "Sistemas de ML"
metric: "~12M"
metric_label: "de usuarios mensuales atendidos en la región"
role: "Responsable de arquitectura"
scale: "Batch + tiempo real · 8 países"
period: "2022–2024"
tags: ["MLOps", "BigQuery", "APIs", "Streaming", "Monitoreo"]
---

## El problema

La mensajería personalizada requería contexto de comportamiento reciente y decisiones de baja latencia, pero muchas señales y predicciones eran más confiables y económicas de calcular en batch. El diseño debía conectar ambos mundos sin depender de consultas analíticas lentas durante el envío.

## Mi rol

Diseñé la arquitectura de serving y su flujo de decisión, alineando cómputo de modelos, almacenamiento, APIs, eventos de sesión y reglas de producto con los requisitos de latencia y confiabilidad de push y email.

## Diseño del sistema

<div class="system-flow" role="img" aria-label="El scoring batch en BigQuery alimenta un almacén de baja latencia, APIs, un motor de sesión en tiempo real y decisiones personalizadas">
  <span>BigQuery<br><small>scoring batch</small></span><b>→</b>
  <span>Key-value store<br><small>baja latencia</small></span><b>→</b>
  <span>APIs<br><small>acceso a decisiones</small></span><b>→</b>
  <span>Motor de sesión<br><small>eventos en vivo</small></span><b>→</b>
  <span>Push y email<br><small>acción personalizada</small></span>
</div>

- Los jobs batch producían scores estables en BigQuery.
- Los scores se cargaban en un almacén key-value de baja latencia.
- Las APIs exponían las señales de decisión a servicios posteriores.
- Un motor de sesiones basado en eventos combinaba predicciones almacenadas con comportamiento en vivo para decidir audiencia, momento y contenido.

## Principios operativos

La arquitectura separó el cómputo costoso del modelo del proceso de decisión sensible a latencia. También estableció límites claros para monitorear frescura de datos, disponibilidad de APIs, volumen y comportamiento de modelos.

## Resultado

El sistema entregó decisiones personalizadas de push y email para aproximadamente **12 millones de usuarios mensuales en ocho países**, soportando el programa de experimentación y medición causal.

> Esta es una representación conceptual. Se omiten nombres de infraestructura, esquemas internos y detalles propietarios.

