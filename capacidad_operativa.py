"""
==============================================================================
CAPACIDAD OPERATIVA Y CARGA DE RAMPA
==============================================================================
"""
import pandas as pd

# Usa los minutos disponibles y los servicios registrados para medir la carga diaria del taller.
# Para hacerlo, divide el tiempo productivo entre 35 minutos y compara el resultado con la meta del 80%.
def calcular_capacidad_y_desempeno_puesto(datos_flota, factor_eficiencia_meta=0.80):
    # Guarda los minutos de la jornada, resta los descansos y define cuanto dura un servicio normal.
    TIEMPO_ESTANDAR_POR_SERVICIO_MINUTOS = 35.0
    MINUTOS_TOTALES_JORNADA_BRUTA = 600.0
    MINUTOS_PAUSAS_DESCANSO = 90.0
    MINUTOS_NETOS_PRODUCTIVOS = MINUTOS_TOTALES_JORNADA_BRUTA - MINUTOS_PAUSAS_DESCANSO

    print("\n" + "="*75)
    print("   ANÁLISIS DE CAPACIDAD OPERATIVA Y NIVEL DE SATURACIÓN DE RAMPA")
    print("="*75)

    # Cuenta las filas y obtiene los dias distintos usando la columna fecha; si no hay fechas usa 1 dia.
    total_vehiculos = len(datos_flota)
    dias_operativos = datos_flota['fecha'].dt.date.nunique() if 'fecha' in datos_flota.columns and datos_flota['fecha'].notna().any() else 1

    # Divide los minutos productivos entre 35 minutos y aplica el 80% para obtener la meta recomendada.
    capacidad_teorica_diaria = MINUTOS_NETOS_PRODUCTIVOS / TIEMPO_ESTANDAR_POR_SERVICIO_MINUTOS
    capacidad_meta_diaria = capacidad_teorica_diaria * factor_eficiencia_meta

    promedio_vehiculos_diarios = total_vehiculos / dias_operativos if dias_operativos > 0 else total_vehiculos

    # Filtra los tiempos mayores que cero y calcula su promedio; si no hay ninguno usa 35 minutos.
    registros_con_tiempo = datos_flota[datos_flota['tiempo_rampa_minutos'] > 0]
    if not registros_con_tiempo.empty:
        tiempo_promedio_real_rampa = registros_con_tiempo['tiempo_rampa_minutos'].mean()
    else:
        tiempo_promedio_real_rampa = TIEMPO_ESTANDAR_POR_SERVICIO_MINUTOS

    porcentaje_desempeno_tiempo = (tiempo_promedio_real_rampa / TIEMPO_ESTANDAR_POR_SERVICIO_MINUTOS) * 100
    porcentaje_cumplimiento_carga = (promedio_vehiculos_diarios / capacidad_meta_diaria) * 100

    print(f"[-] Horario Laboral del Taller:          7:00 AM - 5:00 PM (10 horas brutas)")
    print(f"[-] Tiempo de Descansos Reglamentarios:  90 min (1h almuerzo, 15m desayuno, 15m café)")
    print(f"[-] Tiempo Neto Productivo Disponible:   {MINUTOS_NETOS_PRODUCTIVOS:.0f} min / día (8.5 horas netas)")
    print(f"[-] Tiempo Estándar por Servicio:       {TIEMPO_ESTANDAR_POR_SERVICIO_MINUTOS} minutos / vehículo")
    print("-" * 75)
    print(f"[=] Capacidad Teórica Máxima (100%):     {capacidad_teorica_diaria:.2f} vehículos / día")
    print(f"[=] Capacidad Meta Operativa (80%):      {capacidad_meta_diaria:.2f} vehículos / día")
    print("-" * 75)
    print(f"[+] Promedio Diario Observado en Datos: {promedio_vehiculos_diarios:.2f} vehículos / día")
    print(f"[+] Tiempo Promedio Real Registrado:    {tiempo_promedio_real_rampa:.2f} minutos / vehículo")
    print("-" * 75)
    print(f"--> DESEMPEÑO DE TIEMPO EN RAMPA:       {porcentaje_desempeno_tiempo:.1f}% respecto al óptimo (35 min)")
    print(f"--> NIVEL DE CUMPLIMIENTO DE CARGA:     {porcentaje_cumplimiento_carga:.1f}% respecto a la Meta del 80%")
    print("="*75)

    # Compara la carga calculada con 110% y 80% para mostrar el estado de la capacidad.
    if porcentaje_cumplimiento_carga > 110:
        print("[ALERTA] Rampa sobrecargada por encima del límite recomendado.")
    elif porcentaje_cumplimiento_carga >= 80:
        print("[ESTADO ÓPTIMO] El puesto trabaja a alta eficiencia y cumple metas.")
    else:
        print("[DISPONIBILIDAD OCIOSA] Capacidad disponible para atender más unidades.")