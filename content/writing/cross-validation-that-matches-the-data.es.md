---
title: "Validación cruzada que respeta los datos"
description: "Un flujo defendible de selección de modelos: elegir los splits desde el proceso generador, mantener el preprocesamiento dentro de cada fold y separar ajuste de evaluación."
date: 2026-09-06T00:00:00-05:00
translationKey: "cross-validation-that-matches-the-data"
url: "/es/notas/validacion-cruzada-segun-los-datos/"
weight: 2
level: "Intermedio"
topic: "Evaluación de modelos"
repository: "StochasticAITechniquesClass"
repository_url: "https://github.com/sergiomorapardo/StochasticAITechniquesClass"
notebook: "L6_CrossValidation.ipynb"
notebook_url: "https://github.com/sergiomorapardo/StochasticAITechniquesClass/blob/main/Notebooks/L6_CrossValidation.ipynb"
tags: ["Validación cruzada", "Scikit-learn", "Evaluación"]
---

La validación cruzada suele presentarse como una configuración: elegir cinco folds y llamar a `cross_val_score`. La decisión más importante ocurre antes. Un diseño de validación es una afirmación sobre cuáles observaciones pueden representar legítimamente el futuro.

El notebook fuente construye esa afirmación de forma progresiva, desde experimentos repetidos de hold-out hasta validación agrupada, temporal, estratificada y anidada. Esta nota condensa el recorrido en las decisiones que hacen creíble una evaluación.

## Empezar por la fuente de dependencia

Un split aleatorio supone que las observaciones pueden intercambiarse sin cambiar el problema. El supuesto falla cuando varios ejemplos pertenecen al mismo paciente, cliente, dispositivo, documento o periodo. La estrategia de partición debe preservar la frontera que existirá al usar el modelo.

| Situación de los datos | Elección de validación | Qué protege |
| --- | --- | --- |
| Observaciones independientes | K-fold | Reduce la dependencia de un único hold-out arbitrario |
| Clasificación con clases desiguales | K-fold estratificado | Conserva la proporción de clases en cada fold |
| Observaciones repetidas por entidad | Group K-fold | Mantiene cada entidad solo en entrenamiento o validación |
| Pronóstico o eventos ordenados | Split de series de tiempo | Evita entrenar con el futuro |
| Ajuste y reporte final de desempeño | Validación cruzada anidada | Separa selección de evaluación |

La tabla no es un menú de técnicas intercambiables. Es una guía para identificar fuga de información. Si el mismo paciente aparece en entrenamiento y validación, una métrica alta puede premiar el reconocimiento de identidad y no la generalización clínica. Si registros futuros informan predicciones del pasado, el experimento responde una pregunta que el modelo desplegado nunca recibirá.

## Mantener el preprocesamiento dentro del fold

El escalado, la imputación, la codificación y la selección de variables aprenden de los datos. Ajustarlos una sola vez antes de la validación expone cada fold de validación a estadísticas obtenidas al otro lado de la partición. Los pipelines de scikit-learn mantienen esas transformaciones aprendidas dentro de la parte de entrenamiento de cada fold.

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

El pipeline no es solo una forma más ordenada de empacar código. Durante cada fold, `StandardScaler` aprende una media y una desviación únicamente de los datos de entrenamiento de ese fold. Las filas de validación permanecen realmente desconocidas hasta el momento de calcular la métrica.

## Reportar una distribución, no un split afortunado

El notebook entrena primero una regresión logística sobre el dataset de cáncer de mama de scikit-learn usando diez particiones 80/20 diferentes. Las accuracies guardadas van de **0,9649 a 0,9825**, con media de **0,9763** y desviación estándar de **0,0069**. Una ejecución de cinco folds reporta **0,9789 ± 0,0070**.

En esta ejecución particular, la validación de cinco folds no reduce mágicamente la desviación observada. Su valor está en que cada observación participa en validación y el resultado expone la variación entre folds. El artefacto honesto es el conjunto de métricas por fold con su resumen, no la semilla más favorable.

Luego, el notebook crea un dataset sintético de clasificación con 950 ejemplos de la clase mayoritaria y 50 de la minoritaria. La validación estratificada de cinco folds produce **0,9910 de accuracy**, pero el F1 macro es **0,9460** y ROC AUC es **0,9563**. La diferencia es la lección: la estrategia de split y la métrica responden preguntas distintas. La estratificación estabiliza la representación de clases; una métrica sensible a ambas clases evita que la mayoritaria domine el relato.

## Ajustar sin contaminar la estimación

La búsqueda de hiperparámetros reutiliza evidencia de validación para elegir un modelo. Por eso el `best_score_` ganador sirve para seleccionar, pero resulta optimista como estimación final. La validación cruzada anidada crea dos ciclos:

1. El ciclo interno elige hiperparámetros usando únicamente el fold externo de entrenamiento.
2. El ciclo externo evalúa el proceso completo de selección sobre datos que no participaron en esa decisión.

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

En el ejemplo de cáncer de mama, el grid search único reporta una media ROC AUC máxima de **0,9959**. Las métricas externas de la validación anidada promedian **0,9947**, con desviación estándar de **0,0055**. La diferencia es pequeña en este caso, pero el diseño importa incluso cuando la corrección es modesta.

El notebook termina con un pipeline más complejo sobre Titanic que incluye imputación, escalado, one-hot encoding y un random forest. Su grid search interno reporta **0,8678 de ROC AUC**. La estimación anidada es **0,8600 ± 0,0219**. Esa incertidumbre externa informa mejor la planeación que un ganador seleccionado entre 27 combinaciones de hiperparámetros.

## Leer más allá de `best_score_`

`cv_results_` contiene la media, la desviación estándar, el ranking, el tiempo de entrenamiento y la evidencia por fold para cada candidato. En la búsqueda con máquinas de soporte vectorial del notebook, el mejor resultado es un modelo RBF con `C=1` y ROC AUC promedio de 0,995916. Un modelo lineal con `C=0.1` alcanza 0,994856. La diferencia directa es cercana a 0,0011, menor que la desviación entre folds de cualquiera de los dos candidatos.

Eso no demuestra que el modelo simple sea universalmente mejor. Sí muestra por qué el primer lugar del ranking no debería cerrar la decisión. La latencia, la calibración, la interpretabilidad, la memoria y la estabilidad pueden pesar más que una diferencia pequeña frente a la variación experimental.

## Lista de revisión

Antes de aceptar un resultado de selección de modelos, conviene preguntar:

1. ¿Qué unidad debe permanecer independiente entre entrenamiento y evaluación?
2. ¿El tiempo restringe cuáles ejemplos pueden usarse para predecir otros?
3. ¿Las clases poco frecuentes están representadas en cada fold?
4. ¿Todas las transformaciones aprendidas se ajustan dentro de cada fold de entrenamiento?
5. ¿La métrica representa el costo de falsos positivos, falsos negativos y errores de ranking?
6. ¿La estimación final se mantuvo separada de la selección de hiperparámetros?
7. ¿Se reportaron las métricas por fold y su variabilidad junto con la media?
8. ¿Se evaluó un baseline simple usando exactamente las mismas particiones?

Los ejemplos del notebook usan datasets docentes, no evidencia de producción. Su contribución duradera es la lógica de evaluación: respetar dependencias, contener el preprocesamiento aprendido, alinear la métrica y reservar datos intactos para juzgar el proceso completo de selección.

> Límite de la fuente: todos los resultados numéricos de esta nota provienen de las salidas guardadas del notebook. La lista de revisión y la interpretación para despliegue sintetizan esas demostraciones sin afirmar experimentos nuevos.
