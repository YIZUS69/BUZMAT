# -*- coding: utf-8 -*-
"""
paradas_data.py
----------------
Base de datos local (exhaustiva) de paradas de autobús en Maturín, Venezuela.
Es un simple diccionario Python: no requiere ninguna base de datos externa
(SQL, MongoDB, etc.), por lo que no hay nada que instalar ni configurar
aparte de este archivo.

Cada parada tiene:
    - lat, lon: coordenadas geográficas (float)
    - rutas: lista de rutas de autobús que pasan por esa parada
"""

PARADAS = {
    # --- PUNTOS CENTRALES Y EJES PRINCIPALES ---
    "Av. Raúl Leoni (Eje Central)": {"lat": 9.7605, "lon": -63.1668, "rutas": ["Ruta 06", "Ruta 20", "Ruta 33", "Ruta 51", "Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58", "Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14", "Ruta 19"]},
    "Farmacia María Vazques (Av. Bicentenario)": {"lat": 9.7445, "lon": -63.1928, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32", "Ruta 33", "Ruta 51"]},
    "Repuesto El Turco": {"lat": 9.7458, "lon": -63.1901, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32", "Ruta 33", "Ruta 51"]},
    "Comercial Colonial (Plaza Piar)": {"lat": 9.7478, "lon": -63.1872, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32", "Ruta 33", "Ruta 51"]},
    "Potente Monagas (Av. Bolívar)": {"lat": 9.7492, "lon": -63.1851, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32", "Ruta 33", "Ruta 51", "Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58"]},
    "Perfumes Factory": {"lat": 9.7503, "lon": -63.1814, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32", "Ruta 33", "Ruta 51"]},
    "Edif. Avon Cosméticos": {"lat": 9.7511, "lon": -63.1785, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32", "Ruta 33", "Ruta 51"]},
    "UBV (Los Godos / Av. Bolívar)": {"lat": 9.7522, "lon": -63.1724, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32", "Ruta 33", "Ruta 51", "Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58"]},
    "Punto de Control DIE": {"lat": 9.7441, "lon": -63.1934, "rutas": ["Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58", "Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14", "Ruta 19"]},
    "Fondo Común": {"lat": 9.7451, "lon": -63.1919, "rutas": ["Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58"]},
    "Ambulatorio Concepción Mariño": {"lat": 9.7468, "lon": -63.1892, "rutas": ["Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58"]},
    "La Preferida": {"lat": 9.7501, "lon": -63.1830, "rutas": ["Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58"]},
    "Antiguo Banco de Venezuela": {"lat": 9.7510, "lon": -63.1802, "rutas": ["Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58"]},
    "Lo Mejor de lo Mejor": {"lat": 9.7450, "lon": -63.1910, "rutas": ["Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14", "Ruta 19"]},
    "Torre Coffel": {"lat": 9.7462, "lon": -63.1888, "rutas": ["Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14", "Ruta 19"]},
    "Farma Center": {"lat": 9.7471, "lon": -63.1870, "rutas": ["Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14", "Ruta 19"]},
    "Farma Paz": {"lat": 9.7480, "lon": -63.1853, "rutas": ["Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14", "Ruta 19"]},
    "C.C. Plaza Mayor": {"lat": 9.7515, "lon": -63.1770, "rutas": ["Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14", "Ruta 19"]},
    "Dragón Chino": {"lat": 9.7531, "lon": -63.1702, "rutas": ["Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14", "Ruta 19"]},

    # --- PARADAS DE RECORRIDOS ESPECÍFICOS (SECTORES) ---
    # Eje Sur y Vía Universidad
    "Univ. Pedagógico / UPEL": {"lat": 9.7420, "lon": -63.1750, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32", "Ruta 33", "Ruta 51"]},
    "Comuna Santa Inés": {"lat": 9.7150, "lon": -63.1620, "rutas": ["Ruta 06", "Ruta 20", "Ruta 32"]},
    "Carretera Vía Al Sur": {"lat": 9.6900, "lon": -63.1680, "rutas": ["Ruta 06"]},
    "Urb. Lomas del Viento": {"lat": 9.6820, "lon": -63.1700, "rutas": ["Ruta 06"]},
    "C.C. La Cascada": {"lat": 9.6975, "lon": -63.1790, "rutas": ["Ruta 20"]},
    "Sector Parare": {"lat": 9.6800, "lon": -63.2050, "rutas": ["Ruta 20"]},

    # Eje Chicharronera y Valenzuela
    "La Chicharronera": {"lat": 9.7350, "lon": -63.1480, "rutas": ["Ruta 33", "Ruta 51"]},
    "San Judas Tadeo": {"lat": 9.7410, "lon": -63.1380, "rutas": ["Ruta 33", "Ruta 51"]},
    "Sector Valenzuela": {"lat": 9.7415, "lon": -63.1350, "rutas": ["Ruta 33", "Ruta 51"]},
    "Parque Andrés Eloy Blanco": {"lat": 9.7480, "lon": -63.1550, "rutas": ["Ruta 33", "Ruta 51"]},

    # Eje Juanico, La Floresta y Sabana Grande
    "Av. Rómulo Gallegos": {"lat": 9.7485, "lon": -63.1710, "rutas": ["Ruta 15", "Ruta 16", "Ruta 46"]},
    "Urb. Juanico": {"lat": 9.7350, "lon": -63.1730, "rutas": ["Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58"]},
    "La Floresta": {"lat": 9.7410, "lon": -63.1580, "rutas": ["Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57", "Ruta 58"]},
    "La Florecita": {"lat": 9.7430, "lon": -63.1510, "rutas": ["Ruta 15", "Ruta 16", "Ruta 18", "Ruta 40", "Ruta 46"]},
    "El Parquecito": {"lat": 9.7460, "lon": -63.1450, "rutas": ["Ruta 15", "Ruta 41", "Ruta 46", "Ruta 55", "Ruta 56", "Ruta 57"]},
    "Sabana Grande": {"lat": 9.7280, "lon": -63.1250, "rutas": ["Ruta 16", "Ruta 18", "Ruta 40", "Ruta 41"]},
    "El Mereyal": {"lat": 9.7150, "lon": -63.1320, "rutas": ["Ruta 18"]},
    "El Nazareno": {"lat": 9.7210, "lon": -63.1180, "rutas": ["Ruta 40"]},
    "Esc. Fe y Alegría": {"lat": 9.7300, "lon": -63.1150, "rutas": ["Ruta 41"]},
    "Brisas del Aeropuerto": {"lat": 9.7520, "lon": -63.1480, "rutas": ["Ruta 55", "Ruta 56", "Ruta 57"]},
    "Las Flores": {"lat": 9.7380, "lon": -63.1610, "rutas": ["Ruta 58"]},
    "Trinitarias": {"lat": 9.7310, "lon": -63.1630, "rutas": ["Ruta 58"]},
    "Los Tapiales II": {"lat": 9.7250, "lon": -63.1650, "rutas": ["Ruta 58"]},

    # Eje Las Cocuizas y Los Cortijos
    "Las Cocuizas": {"lat": 9.7620, "lon": -63.1450, "rutas": ["Ruta 01", "Ruta 05", "Ruta 35", "Ruta 59", "Ruta 84", "Ruta 22", "Ruta 12", "Ruta 14"]},
    "Los Cortijos": {"lat": 9.7910, "lon": -63.1200, "rutas": ["Ruta 01", "Ruta 05", "Ruta 35", "Ruta 47", "Ruta 59", "Ruta 84", "Ruta 22"]},
    "Campo Alegre": {"lat": 9.7750, "lon": -63.1300, "rutas": ["Ruta 01"]},
    "El Silencio": {"lat": 9.8050, "lon": -63.1050, "rutas": ["Ruta 01", "Ruta 05"]},
    "1º de Mayo": {"lat": 9.7680, "lon": -63.1380, "rutas": ["Ruta 05"]},
    "Av. Perimetral de Las Cocuizas": {"lat": 9.7690, "lon": -63.1500, "rutas": ["Ruta 47"]},
    "Psiquiátrico": {"lat": 9.7710, "lon": -63.1120, "rutas": ["Ruta 47"]},
    "Urb. Andrés Eloy Blanco": {"lat": 9.7590, "lon": -63.1530, "rutas": ["Ruta 59"]},
    "La Democracia": {"lat": 9.7820, "lon": -63.1250, "rutas": ["Ruta 84"]},
    "Segundo Retorno de Los Cortijos": {"lat": 9.7980, "lon": -63.1150, "rutas": ["Ruta 22", "Ruta 19"]},
    "SAIME Cocuizas": {"lat": 9.7600, "lon": -63.1490, "rutas": ["Ruta 12", "Ruta 14"]},
    "Aeropuerto / Terminal": {"lat": 9.7490, "lon": -63.1530, "rutas": ["Ruta 12", "Ruta 14"]},
    "Av. Principal de Las Cocuizas": {"lat": 9.7640, "lon": -63.1420, "rutas": ["Ruta 19"]},
}
