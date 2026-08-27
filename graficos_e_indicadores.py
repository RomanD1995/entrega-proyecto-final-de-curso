"""
==============================================================================
GRÁFICOS E INDICADORES (MATPLOTLIB)
==============================================================================
"""
import matplotlib.pyplot as plt
import pandas as pd


# Revisa dos nombres posibles y devuelve el primero que exista en la tabla.
# Para hacerlo, recorre una lista de nombres y comprueba cada uno dentro de las columnas.
def obtener_columna_evaluacion(datos_flota):
    for columna in ['alineacion_exitosa', 'estatus_suspension']:
        if columna in datos_flota.columns:
            return columna
    return None


# Limpia el texto recibido y lo compara con listas de estados buenos, malos o desconocidos.
# Para hacerlo, quita espacios, pasa el valor a minusculas y lo busca en las listas de estados.
def normalizar_estado(valor):
    valor = str(valor).strip().lower()
    if valor in ['si', 'aprobado', 'apto', 'optimo', 'bueno', 'saludable', 'ok', 'exitoso']:
        return 'Saludable / en buen estado'
    if valor in ['no', 'rechazado', 'dañado', 'defectuoso', 'malo', 'en mal estado', 'fallo', 'reparar']:
        return 'En mal estado'
    return 'No especificado'


# Agrupa los estados de la tabla y usa sus cantidades para crear un grafico circular.
# Para hacerlo, cuenta los estados normalizados y entrega esas cantidades a plt.pie.
def graficar_salud_general(datos_flota):
    """Pie chart para composición del estado general de la flota."""
    # Busca la columna de evaluacion y detiene el grafico si la tabla no tiene ninguna.
    columna = obtener_columna_evaluacion(datos_flota)
    if columna is None:
        print("[AVISO] No existe una columna de diagnóstico para graficar salud general.")
        return False

    serie = datos_flota[columna].fillna('no_especificado').apply(normalizar_estado)
    conteo = serie.value_counts()
    if conteo.empty:
        print("[AVISO] No hay datos para construir este gráfico.")
        return False

    # Crea una porcion y muestra su porcentaje para cada estado contado.
    fig, ax = plt.subplots(figsize=(8, 6))
    colores = ['#2ca02c', '#d62728', '#7f7f7f']
    wedges, texts, autotexts = ax.pie(
        conteo.values,
        labels=[label for label in conteo.index],
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        colors=colores[:len(conteo)]
    )
    ax.set_title('Estado general de salud vehicular', fontweight='bold')
    ax.axis('equal')
    plt.tight_layout()
    plt.show()
    return True


# Agrupa los tiempos por tipo, obtiene sus promedios y los representa con barras.
# Para hacerlo, usa groupby y mean, ordena los promedios y los entrega a ax.bar.
def graficar_tiempo_rampa_por_tipo(datos_flota):
    """Bar chart para comparar tiempos promedio por tipo de vehículo."""
    columnas_requeridas = ['tipo_vehiculo', 'tiempo_rampa_minutos']
    if not all(columna in datos_flota.columns for columna in columnas_requeridas):
        print("[AVISO] Faltan columnas para graficar tiempo en rampa por tipo de vehículo.")
        return False

    # Usa groupby y mean para obtener un promedio por tipo y sort_values para ordenarlos.
    tiempos_promedio = datos_flota.groupby('tipo_vehiculo', dropna=False)['tiempo_rampa_minutos'].mean().sort_values(ascending=False)
    if tiempos_promedio.empty:
        print("[AVISO] No hay datos de tiempo en rampa para graficar.")
        return False

    fig, ax = plt.subplots(figsize=(9, 5.5))
    barras = ax.bar(
        tiempos_promedio.index.str.upper(),
        tiempos_promedio.values,
        color='#1f77b4',
        edgecolor='black',
        alpha=0.9
    )
    ax.set_title('Tiempo promedio en rampa por tipo de vehículo', fontweight='bold')
    ax.set_xlabel('Tipo de vehículo')
    ax.set_ylabel('Minutos promedio')
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    for barra, valor in zip(barras, tiempos_promedio.values):
        ax.text(barra.get_x() + barra.get_width()/2, valor + 0.5, f'{valor:.1f} min', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.show()
    return True


# Calcula dos cantidades diarias y las dibuja juntas para facilitar su comparacion.
# Para hacerlo, obtiene la meta y la carga observada, las guarda en una lista y crea barras con ax.bar.
def graficar_capacidad_operativa(datos_flota):
    """Bar chart con línea de meta para comparar carga frente a capacidad."""
    if 'tiempo_rampa_minutos' not in datos_flota.columns:
        print("[AVISO] No hay datos de tiempo de rampa para capacidad operativa.")
        return False

    # Divide los minutos productivos entre el tiempo estandar y aplica el 80% de meta.
    minutos_netos = 510.0
    tiempo_estandar = 35.0
    capacidad_meta = (minutos_netos / tiempo_estandar) * 0.80

    total_vehiculos = len(datos_flota)
    dias_operativos = 1
    if 'fecha' in datos_flota.columns and pd.api.types.is_datetime64_any_dtype(datos_flota['fecha']):
        dias_operativos = datos_flota['fecha'].dt.date.nunique() or 1

    carga_observada = total_vehiculos / dias_operativos if dias_operativos > 0 else total_vehiculos

    fig, ax = plt.subplots(figsize=(7, 5))
    categorias = ['Meta de capacidad', 'Carga observada']
    valores = [capacidad_meta, carga_observada]
    colores = ["#255cf5", "#a4f71f"]
    barras = ax.bar(categorias, valores, color=colores, edgecolor='black', alpha=0.8)
    ax.set_title('Capacidad operativa frente a la carga real', fontweight='bold')
    ax.set_ylabel('Vehículos por día')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.axhline(capacidad_meta, color="#fac249", linestyle='--', linewidth=1.5, label='Meta objetivo')
    ax.legend(loc='upper left')

    for barra, valor in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width()/2, valor + 0.5, f'{valor:.1f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.show()
    return True


# Cuenta los estados por marca y crea dos barras para comparar aptos y no aptos.
# Para hacerlo, agrupa la tabla por marca y estado, separa los conteos y dibuja ambos grupos.
def graficar_salud_por_marca(datos_flota):
    """Compara vehículos aptos y no aptos por marca con barras lado a lado."""
    if 'marca' not in datos_flota.columns:
        print("[AVISO] No hay datos de marca para este gráfico.")
        return False

    columna = obtener_columna_evaluacion(datos_flota)
    if columna is None:
        print("[AVISO] No existe una columna de diagnóstico para cruzar por marca.")
        return False

    # Copia las columnas usadas para no cambiar los datos originales mientras prepara el grafico.
    datos = datos_flota[['marca', columna]].copy()
    datos[columna] = datos[columna].fillna('no').astype(str).str.lower()

    datos['estado'] = datos[columna].map({'si': 'Apto / óptimo', 'no': 'No apto'}).fillna('No especificado')
    resumen = datos.groupby('marca')['estado'].value_counts().unstack(fill_value=0)

    if resumen.empty:
        print("[AVISO] No hay registros suficientes para este gráfico.")
        return False

    if 'Apto / óptimo' not in resumen.columns:
        resumen['Apto / óptimo'] = 0
    if 'No apto' not in resumen.columns:
        resumen['No apto'] = 0

    # Toma de la tabla resumida las marcas y las dos columnas que se convertiran en barras.
    marcas = resumen.index
    aptos = resumen['Apto / óptimo'].astype(int)
    no_aptos = resumen['No apto'].astype(int)

    x = range(len(marcas))
    ancho = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    barras_aptos = ax.bar([i - ancho/2 for i in x], aptos.values, width=ancho, label='Apto / óptimo', color='#2ca02c', edgecolor='black')
    barras_no_aptos = ax.bar([i + ancho/2 for i in x], no_aptos.values, width=ancho, label='No apto', color='#d62728', edgecolor='black')

    ax.set_title('Vehículos en buen estado vs no aptos por marca', fontweight='bold')
    ax.set_xlabel('Marca')
    ax.set_ylabel('Cantidad de vehículos')
    ax.set_xticks(list(x))
    ax.set_xticklabels(marcas, rotation=45)
    ax.legend(loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    for barras in [barras_aptos, barras_no_aptos]:
        for barra in barras:
            altura = barra.get_height()
            ax.text(
                barra.get_x() + barra.get_width()/2,
                altura + 1,
                f'{int(altura)}',
                ha='center',
                va='bottom',
                fontweight='bold'
            )

    plt.tight_layout()
    plt.show()
    return True


# Cuenta las respuestas afirmativas de cada servicio y las muestra en barras horizontales.
# Para hacerlo, revisa cada columna de servicio, suma los valores si y los representa con ax.barh.
def graficar_servicios_secundarios(datos_flota):
    """Horizontal bar chart para comparar servicios solicitados por cantidad."""
    servicios_relevantes = ['llantas_nuevas', 'balanceo', 'pinchadura']
    disponibles = [servicio for servicio in servicios_relevantes if servicio in datos_flota.columns]
    if not disponibles:
        print("[AVISO] No existen servicios secundarios para construir el gráfico.")
        return False

    # Recorre los servicios disponibles y suma las filas cuyo valor, en minusculas, es si.
    conteo = {}
    for servicio in disponibles:
        conteo[servicio.replace('_', ' ').title()] = (datos_flota[servicio].astype(str).str.lower() == 'si').sum()

    fig, ax = plt.subplots(figsize=(9, 5))
    nombres = list(conteo.keys())
    valores = list(conteo.values())
    barras = ax.barh(nombres, valores, color='#ff7f0e', edgecolor='black', alpha=0.9)
    ax.set_title('Servicios secundarios solicitados', fontweight='bold')
    ax.set_xlabel('Cantidad de vehículos')
    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.3)

    for barra, valor in zip(barras, valores):
        ax.text(valor + 0.4, barra.get_y() + barra.get_height()/2, str(valor), va='center', ha='left', fontweight='bold')

    plt.tight_layout()
    plt.show()
    return True


# Convierte las fechas en periodos y cuenta cuantos vehiculos corresponden a cada periodo.
# Para hacerlo, transforma las fechas a mes o semana, cuenta los registros y los ordena antes de graficar.
def graficar_movimiento_mensual(datos_flota, frecuencia='M'):
    """Bar chart para mostrar el movimiento vehicular por mes o por semana."""
    # Relaciona M con mes y W con semana para elegir etiquetas y titulo del grafico.
    configuracion = {
        'M': ('mes', 'meses', 'Movimiento vehicular por mes'),
        'W': ('semana', 'semanas', 'Movimiento vehicular por semana')
    }
    periodo, periodos, titulo = configuracion.get(frecuencia, configuracion['M'])

    if 'fecha' not in datos_flota.columns:
        print(f"[AVISO] No existe la columna 'fecha' para analizar movimiento por {periodo}.")
        return False

    # Convierte las fechas, elimina las que no se pudieron leer y conserva las validas.
    datos = datos_flota[['fecha']].copy()
    datos['fecha'] = pd.to_datetime(datos['fecha'], errors='coerce')
    datos = datos.dropna(subset=['fecha'])
    if datos.empty:
        print("[AVISO] No hay fechas válidas para generar este gráfico.")
        return False

    # Agrupa las fechas por periodo, cuenta los registros y ordena los periodos cronologicamente.
    movimiento = datos['fecha'].dt.to_period(frecuencia).value_counts().sort_index()
    if movimiento.empty:
        print(f"[AVISO] No hay movimiento suficiente para construir el historial por {periodo}.")
        return False

    etiquetas = [str(periodo_actual) for periodo_actual in movimiento.index]
    cantidades = movimiento.values
    x = range(len(etiquetas))
    ancho = 0.6

    fig, ax = plt.subplots(figsize=(12, 6))
    barras = ax.bar(x, cantidades, width=ancho, color='#1f77b4', edgecolor='black', alpha=0.9)

    ax.set_title(titulo, fontweight='bold')
    ax.set_xlabel(periodo.capitalize())
    ax.set_ylabel('Vehículos atendidos')
    ax.set_xticks(list(x))
    ax.set_xticklabels(etiquetas, rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    for barra, valor in zip(barras, cantidades):
        ax.text(
            barra.get_x() + barra.get_width()/2,
            valor + 1,
            f'{int(valor)}',
            ha='center',
            va='bottom',
            fontweight='bold'
        )

    plt.tight_layout()
    plt.show()
    return True


# Presenta un segundo menu y ejecuta la funcion del grafico que el usuario elige.
# Para hacerlo, compara la opcion escrita y llama al grafico indicado o a todos en orden.
def generar_graficos_indicadores(datos_flota):
    print("\n[MATPLOTLIB] Panel de métricas y gráficos del sistema.")

    # Repite las opciones graficas hasta que el usuario escribe 0 para regresar.
    while True:
        print("\n=== MENÚ DE GRÁFICOS ===")
        print("[1] Salud general")
        print("[2] Tiempo en rampa por tipo de vehículo")
        print("[3] Capacidad operativa")
        print("[4] Diagnóstico por marca")
        print("[5] Servicios secundarios")
        print("[6] Movimiento del taller por mes o por semana")
        print("[7] Generar todos los gráficos")
        print("[0] Volver")

        opcion = input("Seleccione una opción: ").strip()

        # Compara la opcion escrita y llama a una funcion grafica especifica o a todas.
        if opcion == '0':
            print("[SALIR] Regresando al menú principal.")
            break
        elif opcion == '1':
            graficar_salud_general(datos_flota)
        elif opcion == '2':
            graficar_tiempo_rampa_por_tipo(datos_flota)
        elif opcion == '3':
            graficar_capacidad_operativa(datos_flota)
        elif opcion == '4':
            graficar_salud_por_marca(datos_flota)
        elif opcion == '5':
            graficar_servicios_secundarios(datos_flota)
        elif opcion == '6':
            print("\n=== PERIODO DEL MOVIMIENTO ===")
            print("[1] Por mes")
            print("[2] Por semana")
            print("[0] Cancelar")
            periodo = input("Seleccione una opción: ").strip()
            if periodo == '1':
                graficar_movimiento_mensual(datos_flota, 'M')
            elif periodo == '2':
                graficar_movimiento_mensual(datos_flota, 'W')
            elif periodo != '0':
                print("[AVISO] Opción no válida. Intente nuevamente.")
        elif opcion == '7':
            graficar_salud_general(datos_flota)
            graficar_tiempo_rampa_por_tipo(datos_flota)
            graficar_capacidad_operativa(datos_flota)
            graficar_salud_por_marca(datos_flota)
            graficar_servicios_secundarios(datos_flota)
            graficar_movimiento_mensual(datos_flota)
        else:
            print("[AVISO] Opción no válida. Intente nuevamente.")