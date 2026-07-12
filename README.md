# Bot de Autobuses - Maturín (v2)

Bot de Telegram que ayuda a encontrar la parada más cercana, elegir destino
y calcular la tarifa en bolívares. Esta versión usa una base de datos de
paradas mucho más amplia (más de 100 paradas y rutas reales de Maturín).

## Archivos

| Archivo             | Qué hace                                                        |
|----------------------|-------------------------------------------------------------------|
| `bot.py`             | Bot principal (ejecútalo con `python bot.py`)                    |
| `rutas.py`            | Motor de búsqueda de itinerarios (con transbordo si hace falta)   |
| `rutas_oficiales.py`  | Fuente de verdad: cada ruta real (única por código+grupo) y sus paradas, transcrita de los mapas oficiales |
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
- El menú de destinos se muestra **paginado** (30 por página, en cuadrícula
  de 2 columnas, con botones "⬅️ Anterior" / "Siguiente ➡️"). Esto es
  necesario porque Telegram limita a 100 botones inline por mensaje, y esta
  base de datos tiene más de 130 paradas.
- **Transbordos automáticos:** si no existe una ruta directa entre el
  origen y el destino, el bot busca (con un algoritmo BFS sobre el grafo
  parada↔ruta, en `rutas.py`) el itinerario más corto posible con
  transbordo, indicando en qué parada intermedia bajarte y qué otra ruta
  tomar. El costo del pasaje mostrado es por cada bus que debas tomar.
- **Códigos de ruta ambiguos:** los mapas oficiales (Grupos 1 a 5) reusan
  algunos números de ruta para autobuses físicamente distintos (ej. hay
  un "12-14" que va a SAIME/Aeropuerto y otro "12-14" totalmente distinto
  que va a La Libertad). `paradas_data.py` y `rutas_oficiales.py` ya
  distinguen estos casos mostrando el grupo entre paréntesis, ej.
  "12-14 (Grupo 1)" vs "12-14 (Grupo 5)", para que el bot nunca confunda
  una ruta con otra al buscar transbordos.
- **Cobertura real:** con solo estos 5 grupos de rutas, no todas las
  combinaciones de origen/destino tienen conexión directa en bus. Cuando
  esto pasa, el bot busca automáticamente la parada más cercana al
  destino (hasta 2.5 km) a la que sí se pueda llegar en bus, y sugiere
  bajarte ahí y caminar el resto (indicando la distancia aproximada). Si
  ni siquiera así hay conexión, el bot lo dice claramente en vez de
  inventar una ruta que no existe.
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
