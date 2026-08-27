"""
==============================================================================
CÁLCULO DE SALUD VEHICULAR
==============================================================================
"""
import pandas as pd

# Cuenta los resultados de evaluacion y calcula que porcentaje representa cada estado.
# Para hacerlo, cuenta cada respuesta con value_counts y divide su cantidad entre el total de vehiculos.
def analizar_salud_vehicular_general(datos_flota):
    print("\n" + "="*70)
    print("   RESUMEN DE SALUD VEHICULAR (% APROBADOS VS RECHAZADOS)")
    print("="*70)

    # Elige alineacion cuando existe y, si falta, toma estatus_suspension como columna alternativa.
    total_vehiculos = len(datos_flota)
    columna_evaluacion = 'alineacion_exitosa' if 'alineacion_exitosa' in datos_flota.columns else 'estatus_suspension'
    conteo_estados = datos_flota[columna_evaluacion].value_counts().to_dict()

    print(f"Total de evaluaciones en rampa: {total_vehiculos}")
    print("-" * 65)
    print(f"{'vehiculos segun su Estado de Diagnóstico':<28} | {'vehiculos':<8} | {'Porcentaje':<10}")
    print("-" * 65)

    # Recorre cada estado, divide su cantidad entre el total y lo convierte en una etiqueta comprensible.
    for estado_nombre, cantidad in conteo_estados.items():
        porcentaje = round((cantidad / total_vehiculos) * 100, 2)
        if estado_nombre in ['si', 'optimo']:
            etiqueta = "APROBADO (Apto)"
        elif estado_nombre in ['no', 'dañado - decide reparar']:
            etiqueta = "RECHAZADO (Con Daño)"
        else:
            etiqueta = estado_nombre.upper()
        print(f"{etiqueta:<40} | {cantidad:<8} | {porcentaje}%")
    print("\nla metrica anterior nos indica el la cantidad de vehiculos optimos para el servicio ")
    print("y  el porcentaje que representa del el total de los mismos revisados, asi como el")
    print(f"porcentaje de los rechasados los cuales representan un {porcentaje}% de los vehiculo")
    print("revisados representando una amenaza vial")

# Agrupa los vehiculos por marca y cuenta cuantos aparecen en cada estado.
# Para hacerlo, usa una tabla cruzada que coloca las marcas en filas y los estados en columnas.
def analizar_salud_por_marca(datos_flota):
    print("\n" + "="*70)
    print("   DIAGNÓSTICO DE SALUD VEHICULAR CRUZADO POR MARCA")
    print("="*70)
    columna_evaluacion = 'alineacion_exitosa' if 'alineacion_exitosa' in datos_flota.columns else 'estatus_suspension'

    # Usa crosstab para colocar las marcas en filas, los estados en columnas y los totales al final.
    if 'marca' in datos_flota.columns:
        tabla_marcas = pd.crosstab(
            datos_flota['marca'],
            datos_flota[columna_evaluacion],
            margins=True,
            margins_name="Total_General"
        )
        print(tabla_marcas)
    else:
        print("[AVISO] No existe la columna 'marca' para este diagnóstico.")