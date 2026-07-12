# -*- coding: utf-8 -*-
"""
config.py
---------
EDITA AQUÍ tus datos. Es el único archivo que normalmente necesitas tocar.
"""

# 1) Pega aquí el token que te da @BotFather en Telegram
TELEGRAM_TOKEN = "8854341476:AAELHmYxaOEF84g6tylY_k8TxjZWqGrqzKQ"

# 2) Correo de contacto para el User-Agent de Nominatim (geopy) - opcional
NOMINATIM_EMAIL = "jesumrt089@email.com"

# 3) Precio del pasaje en USD
PRECIO_PASAJE_USD = 0.25

# 4) Tasa de respaldo si el BCV no responde (Bs. por USD)
TASA_RESPALDO_BCV = 36.00

# 5) Horas que dura la caché de la tasa BCV antes de volver a raspar la web
HORAS_CACHE_BCV = 6

# 6) Nombre del archivo donde se guarda la caché de la tasa BCV
ARCHIVO_CACHE_BCV = "bcv_cache.json"
