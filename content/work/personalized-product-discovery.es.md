---
title: "Descubrimiento personalizado y ranking de productos"
description: "Reemplazo de una landing estática de afiliados por un feed continuo y personalizado, medido mediante un experimento controlado multinacional."
translationKey: "personalized-discovery"
weight: 1
category: "Ranking"
metric: "+20–26%"
metric_label: "de aumento en engagement a lo largo del funnel"
role: "Líder técnico"
scale: "~5,2M de sesiones · 4 países"
period: "2024–2026"
tags: ["Recomendación", "Ranking", "Pruebas A/B", "Descubrimiento"]
---

## El problema

El descubrimiento de productos para afiliados dependía de una experiencia estática y curada. Esto limitaba la cantidad de productos explorables y la capacidad de adaptar la relevancia a cada sesión.

La oportunidad no consistía solamente en entrenar un modelo de ranking. Era necesario rediseñar el sistema de descubrimiento y demostrar, bajo condiciones controladas, que la personalización generaba valor incremental a lo largo del funnel.

## Mi rol

Lideré el diseño de ML para ranking y descubrimiento, trabajando con producto e ingeniería para evolucionar de una landing curada a un feed continuo y personalizado. Mi contribución incluyó definición del problema, señales de ranking, diseño experimental, revisión técnica e interpretación de resultados.

## Enfoque técnico

- Creación de un flujo continuo de candidatos y scoring en lugar de una colección fija.
- Incorporación de señales de propensión de compra y ranking por precio.
- Conexión de enlaces compartidos con órdenes posteriores en web y app mediante una capa consistente de atribución.
- Uso del pipeline de atribución como fuente analítica de verdad para experimentos controlados en diferentes placements.

## Diseño experimental

La nueva experiencia se evaluó contra el control estático mediante una prueba A/B con aproximadamente **5,2 millones de sesiones en cuatro países**. La evaluación cubrió clics, intención, compartidos y conversión de nuevos enlaces de afiliados.

## Resultado

El feed personalizado aumentó el engagement entre **20% y 26% a lo largo del funnel** y mejoró **17% la conversión de nuevos enlaces de afiliados frente al control**.

> Caso público basado en información de alto nivel previamente divulgada. Los detalles internos y datos propietarios se excluyen intencionalmente.

## Aprendizaje

Un sistema de ranking solo resulta útil cuando su objetivo, atribución, serving y unidad experimental están alineados. La arquitectura de medición fue tan importante como el propio modelo.

