# -*- coding: utf-8 -*-
"""
bot.py
------
Bot de Telegram para ayudar a los usuarios en Maturín, Venezuela a:
  1. Encontrar su parada de autobús más cercana (compartiendo ubicación).
  2. Elegir un destino entre las demás paradas.
  3. Ver qué rutas conectan origen y destino, y el costo del pasaje en Bs.

CÓMO CORRERLO
-------------
1. pip install -r requirements.txt
2. Edita config.py y pon tu TELEGRAM_TOKEN (te lo da @BotFather).
3. python bot.py

No necesitas instalar ninguna base de datos: los datos de las paradas
viven en paradas_data.py y la caché de la tasa BCV se guarda en un
archivo JSON simple (bcv_cache.json) que se crea solo.
"""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

from bcv import obtener_tasa_bcv
from config import PRECIO_PASAJE_USD, TELEGRAM_TOKEN
from geo import parada_mas_cercana
from paradas_data import PARADAS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# /start
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Da la bienvenida y pide al usuario que comparta su ubicación."""
    boton_ubicacion = KeyboardButton(text="📍 Compartir mi ubicación", request_location=True)
    teclado = ReplyKeyboardMarkup([[boton_ubicacion]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "¡Hola! 🚌 Soy tu asistente de transporte en Maturín.\n\n"
        "Comparte tu ubicación actual con el botón de abajo y te diré "
        "cuál es tu parada de autobús más cercana.",
        reply_markup=teclado,
    )


# ---------------------------------------------------------------------------
# Recepción de ubicación -> calcular origen y mostrar destinos posibles
# ---------------------------------------------------------------------------
async def recibir_ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ubicacion = update.message.location
    origen = parada_mas_cercana(ubicacion.latitude, ubicacion.longitude)

    # Guardamos el origen en el estado de la conversación del usuario
    context.user_data["origen"] = origen

    # Construimos el menú con todas las demás paradas como posibles destinos,
    # organizado en cuadrícula de 2 columnas para que no rompa el chat aunque
    # haya muchas paradas.
    COLUMNAS = 2
    nombres_destino = [nombre for nombre in PARADAS if nombre != origen]

    botones = []
    fila_actual = []
    for nombre_parada in nombres_destino:
        # Los botones inline tienen un límite de texto visible; si el nombre
        # es muy largo lo recortamos para que se vea bien en el teclado.
        etiqueta = nombre_parada if len(nombre_parada) <= 28 else nombre_parada[:25] + "..."
        fila_actual.append(InlineKeyboardButton(etiqueta, callback_data=nombre_parada))
        if len(fila_actual) == COLUMNAS:
            botones.append(fila_actual)
            fila_actual = []
    if fila_actual:
        botones.append(fila_actual)

    teclado = InlineKeyboardMarkup(botones)

    await update.message.reply_text(
        f"📍 Tu parada más cercana detectada es: *{origen}*\n\n"
        "¿A qué parada o sector deseas ir?",
        reply_markup=teclado,
        parse_mode="Markdown",
    )


# ---------------------------------------------------------------------------
# Selección de destino (botón inline) -> calcular rutas y tarifa
# ---------------------------------------------------------------------------
async def recibir_destino(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    destino = query.data
    origen = context.user_data.get("origen")

    if origen is None:
        await query.edit_message_text(
            "⚠️ No encontré tu ubicación de origen. Envía /start de nuevo y "
            "comparte tu ubicación."
        )
        return

    rutas_origen = set(PARADAS[origen]["rutas"])
    rutas_destino = set(PARADAS[destino]["rutas"])
    rutas_comunes = sorted(rutas_origen & rutas_destino)

    if rutas_comunes:
        texto_buses = ", ".join(rutas_comunes)
    else:
        texto_buses = (
            "No hay buses directos de punto a punto, pero en tu origen "
            "puedes tomar: " + ", ".join(sorted(rutas_origen)) + " para acercarte."
        )

    tasa_bcv = obtener_tasa_bcv()
    costo_bs = PRECIO_PASAJE_USD * tasa_bcv

    mensaje = (
        f"📍 *Origen:* {origen}\n"
        f"🏁 *Destino:* {destino}\n"
        f"🚌 *Buses directos que puedes tomar:* {texto_buses}\n"
        f"💵 *Costo máximo del pasaje:* {PRECIO_PASAJE_USD:.2f} USD "
        f"(~ {costo_bs:.2f} Bs.) según tasa oficial BCV."
    )

    await query.edit_message_text(mensaje, parse_mode="Markdown")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    if TELEGRAM_TOKEN == "TU_TOKEN_DE_TELEGRAM_AQUI":
        raise SystemExit(
            "⚠️ Debes configurar tu TELEGRAM_TOKEN en config.py antes de correr el bot."
        )

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, recibir_ubicacion))
    app.add_handler(CallbackQueryHandler(recibir_destino))

    logger.info("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    app.run_polling()


if __name__ == "__main__":
    main()
