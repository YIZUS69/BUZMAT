# Bot de Autobuses - Maturín (v2)

Bot de Telegram que ayuda a encontrar la parada más cercana, elegir destino
y calcular la tarifa en bolívares. Esta versión usa una base de datos de
paradas mucho más amplia (más de 100 paradas y rutas reales de Maturín).

## Archivos

| Archivo             | Qué hace                                                        |
|----------------------|-------------------------------------------------------------------|
| `bot.py`             | Bot principal (ejecútalo con `python bot.py`)                    |
| `config.py`          | Aquí pones tu TOKEN y ajustas precios/tasas de respaldo           |
| `paradas_data.py`    | "Base de datos" de paradas (diccionario Python, no requiere SQL)  |
| `bcv.py`              | Obtiene la tasa del dólar del BCV con caché de 6 horas            |
| `geo.py`              | Cálculo de distancias (Haversine) y parada más cercana            |
| `requirements.txt`   | Dependencias a instalar                                           |
| `bcv_cache.json`      | Se crea solo la primera vez que corre el bot (caché de la tasa)   |

## Pasos para correrlo

1. Instala Python 3.10 o superior.
2. Abre una terminal en esta carpeta e instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
   (usa `python -m pip install -r requirements.txt` si tienes varias
   versiones de Python instaladas, para asegurarte de instalar en la
   correcta).
3. Abre `config.py` y reemplaza:
   ```python
   TELEGRAM_TOKEN = "TU_TOKEN_DE_TELEGRAM_AQUI"
   ```
   por el token que te da [@BotFather](https://t.me/BotFather) en Telegram.
4. Corre el bot:
   ```
   python bot.py
   ```
5. En Telegram, busca tu bot y envía `/start`.

## Notas

- No necesitas instalar ninguna base de datos (MySQL, MongoDB, etc.): las
  paradas están en `paradas_data.py` como un diccionario normal de Python.
- El menú de destinos se muestra en cuadrícula de 2 columnas para que no
  rompa el chat, ya que esta versión tiene muchas más paradas que la v1.
- Si la página del BCV cambia su estructura HTML o no responde, el bot usa
  automáticamente la tasa de respaldo definida en `config.py`
  (`TASA_RESPALDO_BCV`) y lo indica en los logs de la consola.
- Para agregar o editar paradas, solo modifica el diccionario `PARADAS` en
  `paradas_data.py` (cada parada necesita `lat`, `lon` y una lista `rutas`).
- Requiere `python-telegram-bot>=22.8` para ser compatible con versiones
  recientes de Python (3.13/3.14). Si ves un error tipo
  `AttributeError: 'Updater' object has no attribute ...`, es porque tienes
  una versión vieja de la librería instalada: corre
  `pip uninstall python-telegram-bot -y` y luego
  `pip install -r requirements.txt` de nuevo.
