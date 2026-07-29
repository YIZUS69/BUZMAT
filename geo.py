# -*- coding: utf-8 -*-
"""
geo.py
------
Funciones geográficas: distancia de Haversine y búsqueda de la parada
más cercana dentro del diccionario PARADAS.
"""

import math

from paradas_data import PARADAS

RADIO_TIERRA_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia en kilómetros entre dos puntos (lat, lon) usando Haversine."""
    lat1_r, lon1_r, lat2_r, lon2_r = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return RADIO_TIERRA_KM * c


def parada_mas_cercana(lat_usuario: float, lon_usuario: float) -> str:
    """
    Recorre PARADAS y devuelve el nombre de la parada más cercana
    a las coordenadas del usuario.
    """
    mejor_nombre = None
    mejor_distancia = float("inf")

    for nombre, datos in PARADAS.items():
        distancia = haversine_km(lat_usuario, lon_usuario, datos["lat"], datos["lon"])
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_nombre = nombre

    return mejor_nombre


def paradas_alternativas(origen: str, destino: str, max_opciones: int = 3):
    """
    Cuando no hay ruta directa entre origen y destino, busca otras paradas
    (distintas al origen y al destino) que:
      1) Tengan al menos una ruta en común con el destino.
      2) Estén razonablemente cerca del origen (para que el usuario pueda
         caminar hasta allá y tomar el bus correcto desde ahí).

    Devuelve una lista de hasta `max_opciones` tuplas
    (nombre_parada, distancia_km, rutas_en_comun_con_destino),
    ordenadas de la parada más cercana al origen a la más lejana.
    """
    if origen not in PARADAS or destino not in PARADAS:
        return []

    rutas_destino = set(PARADAS[destino]["rutas"])
    lat_origen = PARADAS[origen]["lat"]
    lon_origen = PARADAS[origen]["lon"]

    candidatas = []
    for nombre, datos in PARADAS.items():
        if nombre in (origen, destino):
            continue

        rutas_comunes = set(datos["rutas"]) & rutas_destino
        if not rutas_comunes:
            continue

        distancia = haversine_km(lat_origen, lon_origen, datos["lat"], datos["lon"])
        candidatas.append((nombre, distancia, sorted(rutas_comunes)))

    candidatas.sort(key=lambda item: item[1])
    return candidatas[:max_opciones]
