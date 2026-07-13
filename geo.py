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


def paradas_mas_cercanas(lat_usuario: float, lon_usuario: float, n: int = 3):
    """
    Devuelve una lista con las 'n' paradas más cercanas a las coordenadas
    del usuario, ordenadas de menor a mayor distancia.

    Cada elemento de la lista es una tupla (nombre_parada, distancia_km).
    Útil cuando la parada geográficamente más cercana no tiene buena
    conexión de rutas y el usuario prefiere caminar un poco más hasta
    otra parada cercana.
    """
    distancias = [
        (nombre, haversine_km(lat_usuario, lon_usuario, datos["lat"], datos["lon"]))
        for nombre, datos in PARADAS.items()
    ]
    distancias.sort(key=lambda item: item[1])
    return distancias[:n]
