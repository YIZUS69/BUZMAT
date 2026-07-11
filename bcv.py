# -*- coding: utf-8 -*-
"""
bcv.py
------
Obtiene la tasa oficial del dólar (BCV) con caché local en JSON.

Regla:
- Si el archivo de caché no existe, o tiene más de HORAS_CACHE_BCV horas,
  se intenta raspar la página del BCV.
- Si el scraping falla por cualquier motivo (web caída, cambio de HTML,
  sin internet, etc.), se usa TASA_RESPALDO_BCV y se avisa por log.
- Si el scraping funciona, se guarda el nuevo valor en el archivo de caché
  junto con la fecha/hora de la actualización.
"""

import json
import logging
import os
import time

import requests
from bs4 import BeautifulSoup

from config import ARCHIVO_CACHE_BCV, HORAS_CACHE_BCV, TASA_RESPALDO_BCV

logger = logging.getLogger(__name__)

BCV_URL = "https://www.bcv.org.ve/"
SEGUNDOS_CACHE = HORAS_CACHE_BCV * 3600


def _leer_cache():
    """Lee el archivo de caché si existe. Devuelve dict o None."""
    if not os.path.exists(ARCHIVO_CACHE_BCV):
        return None
    try:
        with open(ARCHIVO_CACHE_BCV, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("No se pudo leer la caché del BCV (%s). Se ignorará.", e)
        return None


def _guardar_cache(tasa: float):
    """Guarda la tasa y la marca de tiempo actual en el archivo de caché."""
    data = {"tasa": tasa, "timestamp": time.time()}
    try:
        with open(ARCHIVO_CACHE_BCV, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except OSError as e:
        logger.warning("No se pudo escribir la caché del BCV (%s).", e)


def _cache_vigente(cache: dict) -> bool:
    """True si la caché existe y no ha expirado."""
    if not cache or "timestamp" not in cache:
        return False
    return (time.time() - cache["timestamp"]) < SEGUNDOS_CACHE


def _raspar_tasa_bcv() -> float:
    """
    Intenta extraer la tasa oficial del dólar desde la web del BCV.
    Lanza una excepción si algo falla (red, parsing, valor no numérico, etc.)
    para que el llamador decida usar la tasa de respaldo.
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MaturinBusBot/1.0)"}
    resp = requests.get(BCV_URL, headers=headers, timeout=15, verify=False)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # El BCV suele mostrar el dólar en un contenedor con id="dolar"
    contenedor = soup.find(id="dolar")
    if contenedor is None:
        raise ValueError("No se encontró el contenedor 'dolar' en el HTML del BCV.")

    texto = contenedor.get_text(strip=True)
    # El texto suele venir con formato "36,50" (coma decimal, estilo venezolano)
    texto = texto.replace(".", "").replace(",", ".")
    numero = "".join(c for c in texto if c.isdigit() or c == ".")
    if not numero:
        raise ValueError("No se pudo extraer un número válido del contenedor 'dolar'.")

    return float(numero)


def obtener_tasa_bcv() -> float:
    """
    Punto de entrada público: devuelve la tasa actual del dólar,
    usando la caché cuando es posible y raspando la web cuando es necesario.
    """
    cache = _leer_cache()

    if _cache_vigente(cache):
        logger.info("Usando tasa BCV desde caché: %.2f Bs.", cache["tasa"])
        return cache["tasa"]

    try:
        tasa = _raspar_tasa_bcv()
        logger.info("Tasa BCV obtenida por scraping: %.2f Bs.", tasa)
        _guardar_cache(tasa)
        return tasa
    except Exception as e:
        logger.warning(
            "Fallo al raspar la tasa del BCV (%s). Usando tasa de respaldo: %.2f Bs.",
            e,
            TASA_RESPALDO_BCV,
        )
        # Si había una caché vieja, mejor usar ese último valor conocido
        # que un valor de respaldo genérico.
        if cache and "tasa" in cache:
            logger.info("Usando último valor conocido en caché: %.2f Bs.", cache["tasa"])
            return cache["tasa"]
        return TASA_RESPALDO_BCV
