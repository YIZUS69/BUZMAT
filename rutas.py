# -*- coding: utf-8 -*-
"""
rutas.py (botv2)
------------------
Motor de búsqueda de itinerarios entre dos paradas, permitiendo
transbordos (cambios de bus) cuando no existe una ruta directa.

CÓMO FUNCIONA
-------------
Modelamos el sistema como un grafo bipartito con dos tipos de nodos:
    - Nodos "Parada" (una por cada parada del diccionario PARADAS)
    - Nodos "Ruta" (una por cada código de ruta, ej. "12-14", "86")

Hay una arista Parada <-> Ruta si esa ruta pasa por esa parada.

Buscar el camino más corto entre la parada de origen y la de destino en
ese grafo (con BFS, búsqueda por anchura) equivale exactamente a
encontrar el itinerario en autobús con la MENOR cantidad de transbordos
posible: cada "Parada -> Ruta -> Parada" representa un tramo de viaje en
un solo bus, y cada vez que el camino pasa por un nuevo nodo "Ruta" es un
transbordo.
"""

from collections import deque

from paradas_data import PARADAS

# Índice invertido: código de ruta -> lista de paradas que sirve.
# Se construye una sola vez al importar el módulo, para no recorrer todo
# el diccionario PARADAS en cada búsqueda (más rápido).
_PARADAS_POR_RUTA: dict[str, list[str]] = {}
for _nombre, _datos in PARADAS.items():
    for _ruta in _datos["rutas"]:
        _PARADAS_POR_RUTA.setdefault(_ruta, []).append(_nombre)


def buscar_itinerario(origen: str, destino: str):
    """
    Busca el camino más corto (en número de tramos/transbordos) entre
    `origen` y `destino` usando BFS sobre el grafo bipartito parada<->ruta.

    Devuelve:
        - [] si origen y destino son la misma parada.
        - Una lista de tramos [(ruta, parada_desde, parada_hasta), ...]
          describiendo el itinerario completo, en orden.
        - None si no existe ninguna conexión (ni directa ni con
          transbordos) entre ambas paradas con los datos actuales.
    """
    if origen == destino:
        return []

    inicio = ("P", origen)
    meta = ("P", destino)

    visitados = {inicio}
    padre = {inicio: None}
    cola = deque([inicio])
    encontrado = False

    while cola:
        nodo = cola.popleft()
        if nodo == meta:
            encontrado = True
            break

        tipo, valor = nodo
        if tipo == "P":
            vecinos = [("R", r) for r in PARADAS[valor]["rutas"]]
        else:  # tipo == "R"
            vecinos = [("P", p) for p in _PARADAS_POR_RUTA.get(valor, [])]

        for vecino in vecinos:
            if vecino not in visitados:
                visitados.add(vecino)
                padre[vecino] = nodo
                cola.append(vecino)

    if not encontrado:
        return None

    # Reconstruimos el camino siguiendo los padres desde la meta al inicio
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padre[nodo]
    camino.reverse()

    # El camino alterna: Parada, Ruta, Parada, Ruta, ..., Parada.
    # Cada tramo de bus va de una parada a la siguiente usando la ruta que
    # está justo en medio de ambas en el camino reconstruido.
    tramos = []
    for i in range(1, len(camino) - 1, 2):
        ruta = camino[i][1]
        parada_desde = camino[i - 1][1]
        parada_hasta = camino[i + 1][1]
        tramos.append((ruta, parada_desde, parada_hasta))

    return tramos


def formatear_itinerario(tramos) -> str:
    """Convierte la lista de tramos devuelta por buscar_itinerario en un
    texto legible y listo para mostrarle al usuario en Telegram."""
    if tramos is None:
        return (
            "No encontré ninguna forma de llegar (ni directa ni con "
            "transbordos) con las rutas registradas actualmente."
        )

    if len(tramos) == 0:
        return "Ya estás en tu destino."

    if len(tramos) == 1:
        ruta, _, _ = tramos[0]
        return f"Ruta directa: {ruta}"

    n_transbordos = len(tramos) - 1
    lineas = [f"No hay ruta directa. Necesitas {n_transbordos} transbordo(s):"]
    for i, (ruta, desde, hasta) in enumerate(tramos, start=1):
        if i < len(tramos):
            lineas.append(f"{i}. Toma la ruta {ruta} desde {desde} hasta {hasta} (bájate y transborda ahí).")
        else:
            lineas.append(f"{i}. Toma la ruta {ruta} desde {desde} hasta tu destino final: {hasta}.")

    return "\n".join(lineas)
