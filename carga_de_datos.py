"""
==============================================================================
CARGA Y LIMPIEZA DE DATOS
==============================================================================
"""
from pathlib import Path

import pandas as pd

NOMBRE_DEL_PROYECTO = "Sistema de Análisis de Salud Vehicular y Taller Hunter"
VERSION_DEL_SISTEMA = "3.0 Modular"
AUTOR_DEL_PROYECTO = "Adonis Eloy Roman Dinarte"
RUTA_EXCEL_INICIAL = "base_datos_taller.xlsx"
RUTA_CSV_PROCESADO = "registros_taller_procesado.csv"
CARPETA_DEL_PROGRAMA = Path(__file__).resolve().parent


# Prueba varias rutas posibles y devuelve la primera que corresponde a un archivo existente.
# Para hacerlo, revisa cada ruta con Path y se detiene cuando encuentra un archivo valido.
def _buscar_archivo(ruta_entrada):
    """Busca el archivo indicado y, si no existe, el CSV procesado."""
    ruta_solicitada = Path(ruta_entrada)
    rutas_posibles = [ruta_solicitada, CARPETA_DEL_PROGRAMA / ruta_solicitada]

    if ruta_solicitada.name == RUTA_EXCEL_INICIAL:
        rutas_posibles.extend([
            CARPETA_DEL_PROGRAMA.parent / ruta_solicitada,
            CARPETA_DEL_PROGRAMA / RUTA_CSV_PROCESADO,
            CARPETA_DEL_PROGRAMA.parent / RUTA_CSV_PROCESADO,
        ])

    for ruta in rutas_posibles:
        if ruta.is_file():
            return ruta

    return None


# Busca el archivo, lo convierte en una tabla, corrige sus datos y guarda una copia limpia.
# Para hacerlo, lee Excel o CSV, revisa columnas, convierte tipos, elimina duplicados y guarda el resultado.
def cargar_y_limpiar_base_de_datos(ruta_entrada=RUTA_EXCEL_INICIAL):
    ruta_final = _buscar_archivo(ruta_entrada)
    if ruta_final is None:
        print(f"\n[ERROR] No se encontró el archivo en '{ruta_entrada}'.")
        return None

    try:
        # Revisa la extension para decidir si pandas debe usar read_excel o read_csv.
        if ruta_final.suffix.lower() == ".xlsx":
            datos_cargados = pd.read_excel(ruta_final)
        elif ruta_final.suffix.lower() == ".csv":
            datos_cargados = pd.read_csv(ruta_final)
        else:
            print("\n[ERROR] El archivo debe tener formato .xlsx o .csv.")
            return None

        if datos_cargados.empty:
            print("\n[ERROR] El archivo no contiene registros.")
            return None

        # Convierte los encabezados a texto, quita espacios al inicio y al final y los pasa a minusculas.
        datos_cargados.columns = (
            datos_cargados.columns.astype(str).str.strip().str.lower()
        )
        diccionario_renombrado = {
            'tipo_vehivulo': 'tipo_vehiculo',
            'categorias_garantia': 'categoria_garantia',
            'obcervaciones': 'observaciones'
        }
        datos_cargados.rename(columns=diccionario_renombrado, inplace=True)

        # Compara las columnas recibidas con las dos que necesitan los calculos principales.
        columnas_requeridas = {'fecha', 'tiempo_rampa_minutos'}
        columnas_faltantes = columnas_requeridas - set(datos_cargados.columns)
        if columnas_faltantes:
            faltantes = ", ".join(sorted(columnas_faltantes))
            print(f"\n[ERROR] Faltan columnas requeridas: {faltantes}.")
            return None

        # Busca filas completamente iguales y conserva solo una copia de cada registro.
        if datos_cargados.duplicated().sum() > 0:
            datos_cargados.drop_duplicates(inplace=True)

        # Intenta convertir cada fecha y reemplaza los valores no reconocidos por una fecha vacia.
        if 'fecha' in datos_cargados.columns:
            datos_cargados['fecha'] = pd.to_datetime(datos_cargados['fecha'], errors='coerce')

        datos_cargados['tiempo_rampa_minutos'] = pd.to_numeric(
            datos_cargados['tiempo_rampa_minutos'], errors='coerce'
        )
        datos_cargados['tiempo_rampa_minutos'] = datos_cargados[
            'tiempo_rampa_minutos'
        ].fillna(0.0)

        if 'anio' in datos_cargados.columns:
            datos_cargados['anio'] = pd.to_numeric(
                datos_cargados['anio'], errors='coerce'
            ).fillna(0).astype(int)

        # Recorre cada columna de texto, llena vacios, quita espacios y convierte todo a minusculas.
        columnas_texto = datos_cargados.select_dtypes(include='object').columns
        for columna in columnas_texto:
            datos_cargados[columna] = (
                datos_cargados[columna]
                .fillna("no_especificado")
                .astype(str)
                .str.strip()
                .str.lower()
            )

        # Escribe la tabla resultante en un CSV nuevo y deja sin cambios el archivo original.
        ruta_salida = CARPETA_DEL_PROGRAMA.parent / RUTA_CSV_PROCESADO
        datos_cargados.to_csv(ruta_salida, index=False)
        print(f"\n[ÉXITO] Base de datos procesada con {len(datos_cargados)} registros.")
        print(f"[ARCHIVO GUARDADO] Se generó '{ruta_salida}'.")
        return datos_cargados

    except (FileNotFoundError, PermissionError) as error_detectado:
        print(f"\n[ERROR] No se pudo acceder al archivo: {error_detectado}")
        return None
    except (pd.errors.EmptyDataError, pd.errors.ParserError, ValueError) as error_detectado:
        print(f"\n[ERROR] El formato de los datos no es válido: {error_detectado}")
        return None
    except OSError as error_detectado:
        print(f"\n[ERROR] No se pudo guardar el archivo procesado: {error_detectado}")
        return None
    except Exception as error_detectado:
        print(f"\n[ERROR] Ocurrió un fallo al procesar los datos: {error_detectado}")
        return None