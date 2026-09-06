---
title: "De co-likes a candidatos con Node2Vec"
description: "Una ruta práctica desde interacciones de MovieLens hasta embeddings de grafos, con la evidencia y los límites necesarios antes de llamarlo un recomendador."
date: 2026-09-06T00:00:00-05:00
translationKey: "node2vec-recommendations"
url: "/es/notas/recomendaciones-node2vec/"
weight: 1
level: "Intermedio"
topic: "Sistemas de recomendación"
repository: "AdvancedTopicsAnalytics"
repository_url: "https://github.com/sergiomorapardo/AdvancedTopicsAnalytics"
notebook: "L25-Node2Vec-RecSys.ipynb"
notebook_url: "https://github.com/sergiomorapardo/AdvancedTopicsAnalytics/blob/main/notebooks/L25-Node2Vec-RecSys.ipynb"
tags: ["Node2Vec", "Graph ML", "Recomendación"]
---

Un catálogo puede convertirse en un grafo antes de convertirse en un recomendador. En el notebook fuente, dos películas se conectan cuando las mismas personas califican positivamente a ambas. Node2Vec transforma luego esos vecindarios en vectores, de modo que las películas cercanas pueden recuperarse mediante una consulta de similitud coseno.

Es un patrón útil para generar candidatos. No es, por sí solo, un sistema de recomendación completo. Esta nota separa lo que demuestra el notebook de la evaluación y el serving que todavía necesitaría un sistema de producción.

## Definir la señal

El notebook usa los datos MovieLens 100K cargados desde GroupLens. La tabla original contiene **100.000 calificaciones** y 1.682 registros de películas. La primera decisión editorial consiste en tratar únicamente las calificaciones de cuatro o cinco como preferencia positiva. El resultado ejecutado conserva **55.375 interacciones positivas**.

```python
ratings = pd.read_csv(
    "ml-100k/u.data",
    sep="\t",
    names=["user_id", "movie_id", "rating", "unix_timestamp"],
)

positive = ratings[ratings.rating >= 4]
```

Este umbral facilita la explicación del grafo: una arista representa co-preferencia repetida, no solo co-calificación. También elimina información. Una calificación de uno y una calificación inexistente se convierten en la ausencia de una arista positiva, aunque significan cosas diferentes. El intercambio es razonable para un ejemplo docente compacto, pero debe quedar explícito.

## Construir el grafo de películas

Para cada usuario, el notebook enumera los pares entre las películas que calificó positivamente. Cada par recibe un conteo igual al número de personas que prefirieron ambos títulos. Solo los pares observados al menos 20 veces se convierten en aristas.

```python
from collections import defaultdict

pairs = defaultdict(int)
for _, user_ratings in positive.groupby("user_id"):
    user_movies = list(user_ratings["movie_id"])
    for i in range(len(user_movies)):
        for j in range(i + 1, len(user_movies)):
            pairs[(user_movies[i], user_movies[j])] += 1

graph = nx.Graph()
for (movie_a, movie_b), count in pairs.items():
    if count >= 20:
        graph.add_edge(movie_a, movie_b, weight=count)
```

El notebook ejecutado reporta **410 nodos y 14.936 aristas** después del filtro. El umbral reduce ruido y costo computacional, pero también favorece los títulos populares. Las películas de cola larga que no acumulan 20 usuarios positivos compartidos desaparecen antes de iniciar Node2Vec.

El ciclo sencillo oculta otro problema de escala: producir todos los pares por usuario crece de forma cuadrática con el número de películas preferidas por esa persona. Para un flujo de eventos mayor harían falta operaciones con matrices dispersas, historiales acotados, muestreo o agregación distribuida.

## Aprender vecindarios locales

Node2Vec genera caminatas aleatorias sesgadas sobre el grafo y entrena un modelo similar a Word2Vec con esas secuencias. Las películas que aparecen en contextos de grafo parecidos reciben vectores similares. El notebook usa 64 dimensiones, caminatas de longitud 20, 200 caminatas por nodo y una ventana de contexto de 10.

```python
from node2vec import Node2Vec

walker = Node2Vec(
    graph,
    dimensions=64,
    walk_length=20,
    num_walks=200,
    p=2,
    q=1,
    workers=1,
)
model = walker.fit(window=10, min_count=1, batch_words=4)
```

Los parámetros `p` y `q` controlan el balance entre regresar a un nodo y explorar vecindarios más lejanos. En este caso, `p=2` hace menos probable un retorno inmediato que `p=1`, mientras `q=1` mantiene neutral la exploración hacia afuera. Son decisiones de modelado, no valores universales. Su utilidad debería juzgarse con calidad de recuperación, no con la apariencia ordenada de una proyección bidimensional.

## Recuperar candidatos

La recomendación es una consulta de vecinos cercanos en el espacio aprendido. A partir de una película semilla, el notebook encuentra los cinco embeddings más similares y convierte sus identificadores en títulos.

```python
def recommend(title, top_n=5):
    movie_id = str(movies.loc[movies.title == title, "movie_id"].iloc[0])
    neighbors = model.wv.most_similar(movie_id, topn=top_n)
    return [
        (movies.loc[movies.movie_id == int(node_id), "title"].iloc[0], score)
        for node_id, score in neighbors
    ]
```

Para **Star Wars (1977)**, la salida guardada comienza con *Raiders of the Lost Ark* en 0,59 y *Return of the Jedi* en 0,55. Para **Toy Story (1995)**, empieza con *Return of the Jedi* en 0,77 y *Twelve Monkeys* en 0,75. Estos ejemplos muestran que el pipeline genera vecinos inspeccionables. No demuestran que los usuarios prefieran esas listas frente a un baseline de popularidad u otro método colaborativo.

El notebook también proyecta los embeddings de 64 dimensiones con t-SNE. Esa vista ayuda a inspeccionar vecindarios locales, pero t-SNE distorsiona distancias globales. Debe tratarse como una visualización diagnóstica, no como evidencia de alta calidad de recomendación.

## Convertir la lección en sistema

Una versión de producción separaría recuperación, ranking, evaluación y serving:

1. **Recuperación:** usar el embedding de grafo para generar algunos cientos de candidatos desde las interacciones positivas recientes.
2. **Filtrado:** retirar ítems no disponibles, ya consumidos, inseguros o no elegibles.
3. **Ranking:** combinar variables de usuario, ítem, contexto y frescura en un modelo alineado con el objetivo del producto.
4. **Evaluación offline:** dividir las interacciones por tiempo y reportar recall@K, precision@K, cobertura, novedad y sesgo de popularidad frente a baselines claros.
5. **Evaluación online:** probar la experiencia completa con métricas de protección, no solo los clics en el módulo de recomendación.
6. **Serving:** versionar embeddings, definir fallbacks para cold start y monitorear cobertura del catálogo y drift de vecindarios.

El notebook merece convertirse en nota técnica porque su abstracción central es sólida: la co-preferencia se vuelve estructura de grafo y esa estructura se vuelve un espacio reutilizable de recuperación. El siguiente paso de ingeniería es conservar esa idea elegante y añadir evaluación honesta y restricciones operativas.

> Límite de la fuente: los conteos del dataset, las dimensiones del grafo, los hiperparámetros y los vecinos de ejemplo provienen de la salida guardada del notebook. Las extensiones de producción son próximos pasos propuestos, no resultados atribuidos al notebook.
