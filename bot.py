# -*- coding: utf-8 -*-
"""
bot.py (botv2)
---------------
Bot de Telegram para ayudar a los usuarios en Maturín, Venezuela a:
  1. Compartir su ubicación.
  2. Elegir a dónde quieren ir (menú paginado, ya que Telegram limita a
     100 botones inline por mensaje y aquí hay más de 130 paradas).
  3. El bot calcula desde cuál parada cercana conviene arrancar (buscando
     entre las paradas más próximas la que sí tenga una ruta directa hacia
     el destino, sin alejarse más de una distancia razonable para caminar).
  4. Ver qué rutas conectan origen y destino, y el costo del pasaje en Bs.

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
from geo import paradas_mas_cercanas
from paradas_data import PARADAS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Telegram permite máximo 100 botones inline por mensaje. Con más de 130
# paradas, mostramos el menú de destinos en páginas para no toparnos con
# ese límite (y de paso, el menú se ve mucho más limpio).
COLUMNAS = 2
DESTINOS_POR_PAGINA = 30  # 15 filas de 2 columnas + fila de navegación

# Al elegir destino, el bot busca entre las paradas más cercanas al usuario
# cuál conviene usar como origen. Evalúa hasta PARADAS_CANDIDATAS_A_EVALUAR
# paradas cercanas, pero solo considera "caminables" las que estén a menos
# de RADIO_MAXIMO_KM (distancia razonable a pie).
PARADAS_CANDIDATAS_A_EVALUAR = 8
RADIO_MAXIMO_KM = 1.0  # ~1 km, distancia razonable para caminar


# ---------------------------------------------------------------------------
# Utilidades de teclado
# ---------------------------------------------------------------------------
def _etiqueta(nombre_parada: str) -> str:
    """Recorta nombres muy largos para que el botón se vea bien."""
    return nombre_parada if len(nombre_parada) <= 28 else nombre_parada[:25] + "..."


def elegir_mejor_origen(candidatos, destino: str):
    """
    Recibe una lista de tuplas (nombre_parada, distancia_km) ya filtradas a
    una distancia razonable para caminar, ordenadas de más cerca a más
    lejos, y el nombre de la parada destino.

    Devuelve (nombre_origen, distancia_km, tiene_ruta_directa):
    - Recorre los candidatos de más cerca a más lejos y elige el primero
      que comparta una ruta directa con el destino.
    - Si ninguno comparte ruta, hace fallback a la parada candidata más
      cercana (para al menos indicar cuál está más a la mano), marcando
      tiene_ruta_directa=False.
    - Si no hay candidatos, devuelve (None, None, False).
    """
    rutas_destino = set(PARADAS[destino]["rutas"])

    candidatos_validos = [(n, d) for n, d in candidatos if n != destino]
    if not candidatos_validos:
        return None, None, False

    for nombre, distancia in candidatos_validos:
        rutas_origen = set(PARADAS[nombre]["rutas"])
        if rutas_origen & rutas_destino:
            return nombre, distancia, True

    # Ninguna parada cercana tiene ruta directa: usamos la más cercana igual.
    nombre_mas_cercano, distancia_mas_cercana = candidatos_validos[0]
    return nombre_mas_cercano, distancia_mas_cercana, False


def _formatear_distancia(distancia_km: float) -> str:
    distancia_m = distancia_km * 1000
    if distancia_m < 1000:
        return f"~{distancia_m:.0f} m"
    return f"~{distancia_km:.1f} km"


def construir_teclado_destinos(pagina: int) -> InlineKeyboardMarkup:
    """
    Construye el teclado inline paginado con todas las paradas, en
    cuadrícula de COLUMNAS columnas, más una fila de navegación
    (Anterior / Siguiente) cuando corresponde.
    """
    nombres_destino = list(PARADAS.keys())
    total_paginas = max(1, (len(nombres_destino) + DESTINOS_POR_PAGINA - 1) // DESTINOS_POR_PAGINA)
    pagina = max(0, min(pagina, total_paginas - 1))

    inicio = pagina * DESTINOS_POR_PAGINA
    fin = inicio + DESTINOS_POR_PAGINA
    nombres_pagina = nombres_destino[inicio:fin]

    filas = []
    fila_actual = []
    for nombre_parada in nombres_pagina:
        # Prefijo "D|" para distinguir estos botones de los de paginación.
        fila_actual.append(InlineKeyboardButton(_etiqueta(nombre_parada), callback_data=f"D|{nombre_parada}"))
        if len(fila_actual) == COLUMNAS:
            filas.append(fila_actual)
            fila_actual = []
    if fila_actual:
        filas.append(fila_actual)

    # Fila de navegación
    nav = []
    if pagina > 0:
        nav.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"P|{pagina - 1}"))
    nav.append(InlineKeyboardButton(f"Pág. {pagina + 1}/{total_paginas}", callback_data="NOOP"))
    if pagina < total_paginas - 1:
        nav.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"P|{pagina + 1}"))
    filas.append(nav)

    return InlineKeyboardMarkup(filas)


# ---------------------------------------------------------------------------
# /start
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Da la bienvenida y pide al usuario que comparta su ubicación."""
    boton_ubicacion = KeyboardButton(text="📍 Compartir mi ubicación", request_location=True)
    teclado = ReplyKeyboardMarkup([[boton_ubicacion]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "¡Hola! 🚌 Soy tu asistente de transporte en Maturín.\n\n"
        "Comparte tu ubicación actual con el botón de abajo, luego dime a "
        "dónde quieres ir y te diré desde cuál parada cercana conviene "
        "arrancar.",
        reply_markup=teclado,
    )


# ---------------------------------------------------------------------------
# /help
# ---------------------------------------------------------------------------
async def help_comando(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía el enlace con la guía de paradas para orientar al usuario."""
    await update.message.reply_text(
        "ℹ️ Puedes consultar las paradas en https://www.instagram.com/p/CllnkElrJuL/"
    )


# ---------------------------------------------------------------------------
# Recepción de ubicación -> calcular origen y mostrar destinos posibles
# ---------------------------------------------------------------------------
async def recibir_ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ubicacion = update.message.location

    # Guardamos la ubicación y reiniciamos la página en el estado del usuario
    context.user_data["ubicacion"] = (ubicacion.latitude, ubicacion.longitude)
    context.user_data["pagina"] = 0

    teclado = construir_teclado_destinos(0)

    await update.message.reply_text(
        "📍 Ubicación recibida "
        f"_({ubicacion.latitude:.5f}, {ubicacion.longitude:.5f})_\n\n"
        "¿A qué parada o sector deseas ir?",
        reply_markup=teclado,
        parse_mode="Markdown",
    )


# ---------------------------------------------------------------------------
# Botón de paginación (Anterior / Siguiente) -> solo cambia el teclado
# ---------------------------------------------------------------------------
async def cambiar_pagina(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    ubicacion = context.user_data.get("ubicacion")
    if ubicacion is None:
        await query.edit_message_text(
            "⚠️ No encontré tu ubicación. Envía /start de nuevo y "
            "comparte tu ubicación."
        )
        return

    nueva_pagina = int(query.data.split("|", 1)[1])
    context.user_data["pagina"] = nueva_pagina

    teclado = construir_teclado_destinos(nueva_pagina)
    await query.edit_message_reply_markup(reply_markup=teclado)


# ---------------------------------------------------------------------------
# Selección de destino (botón inline) -> calcular rutas y tarifa
# ---------------------------------------------------------------------------
async def recibir_destino(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    destino = query.data.split("|", 1)[1]
    ubicacion = context.user_data.get("ubicacion")

    if ubicacion is None:
        await query.edit_message_text(
            "⚠️ No encontré tu ubicación. Envía /start de nuevo y "
            "comparte tu ubicación."
        )
        return

    lat_usuario, lon_usuario = ubicacion
    candidatos = paradas_mas_cercanas(lat_usuario, lon_usuario, PARADAS_CANDIDATAS_A_EVALUAR)
    candidatos_caminables = [(n, d) for n, d in candidatos if d <= RADIO_MAXIMO_KM]

    # Si ninguna parada cae dentro del radio "razonable", igual usamos la
    # más cercana de todas para no dejar al usuario sin respuesta.
    if not candidatos_caminables:
        candidatos_caminables = candidatos[:1]

    origen, distancia_origen, tiene_ruta_directa = elegir_mejor_origen(candidatos_caminables, destino)

    if origen is None:
        await query.edit_message_text(
            "⚠️ No encontré ninguna parada cercana a tu ubicación. Intenta "
            "compartir tu ubicación de nuevo con /start."
        )
        return

    texto_distancia = _formatear_distancia(distancia_origen)

    rutas_origen = set(PARADAS[origen]["rutas"])
    rutas_destino = set(PARADAS[destino]["rutas"])
    rutas_comunes = sorted(rutas_origen & rutas_destino)

    if tiene_ruta_directa:
        texto_buses = ", ".join(rutas_comunes)
    else:
        texto_buses = (
            "No encontré una ruta directa entre esas paradas 😕, pero en tu "
            "parada más cercana puedes tomar: " + ", ".join(sorted(rutas_origen)) + " para acercarte.\n\n"
            "Puedes consultar las paradas en https://www.instagram.com/p/CllnkElrJuL/"
        )

    tasa_bcv = obtener_tasa_bcv()
    costo_bs = PRECIO_PASAJE_USD * tasa_bcv

    mensaje = (
        f"🚶 *Camina hasta:* {origen} ({texto_distancia})\n"
        f"🏁 *Destino:* {destino}\n"
        f"🚌 *Buses directos que puedes tomar:* {texto_buses}\n"
        f"💵 *Costo máximo del pasaje:* {PRECIO_PASAJE_USD:.2f} USD "
        f"(~ {costo_bs:.2f} Bs.) según tasa oficial BCV."
    )

    await query.edit_message_text(mensaje, parse_mode="Markdown")


# ---------------------------------------------------------------------------
# Botón "Pág. X/Y" (no hace nada, solo informa) -> evita el reloj de carga
# ---------------------------------------------------------------------------
async def noop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()


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
    app.add_handler(CommandHandler("help", help_comando))
    app.add_handler(MessageHandler(filters.LOCATION, recibir_ubicacion))
    # Los callback_data llevan un prefijo ("D|", "P|", "NOOP") para saber
    # qué manejador debe atenderlos.
    app.add_handler(CallbackQueryHandler(cambiar_pagina, pattern=r"^P\|"))
    app.add_handler(CallbackQueryHandler(recibir_destino, pattern=r"^D\|"))
    app.add_handler(CallbackQueryHandler(noop, pattern=r"^NOOP$"))

    logger.info("Bot iniciado. Presiona Ctrl+C para detenerlo.")
    app.run_polling()


if __name__ == "__main__":
    main()
