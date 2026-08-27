"""
==============================================================================
SERVICIOS SECUNDARIOS
==============================================================================
"""
import pandas as pd

# Filtra los vehiculos por categoria y cuenta las solicitudes de cada servicio adicional.
# Para hacerlo, compara el tipo elegido con la columna tipo_vehiculo y cuenta las respuestas iguales a si.
def analizar_servicios_secundarios_por_tipo(datos_flota):
    print("\n" + "="*70)
    print("   DEMANDA POR TIPO DE VEHÍCULO Y SERVICIOS COMPLEMENTARIOS")
    print("="*70)

    # Guarda en una lista las categorias permitidas para comparar la respuesta del usuario.
    tipos_validos = ["sedan", "suv", "4x4", "pick_up"]
    print("Categorías disponibles: sedan, suv, 4x4, pick_up (O presione ENTER para 'todos')")
    tipo_seleccionado = input("Ingrese la categoría a analizar: ").strip().lower()

    # Mantiene la pregunta activa mientras la respuesta no sea una categoria valida.
    while tipo_seleccionado and tipo_seleccionado not in tipos_validos and tipo_seleccionado != 'todos':
        print("[AVISO] Categoría no válida. Opciones: sedan, suv, 4x4, pick_up o todos.")
        tipo_seleccionado = input("Ingrese una categoría válida: ").strip().lower()

    # Compara la columna tipo_vehiculo con la respuesta y conserva las filas coincidentes.
    if tipo_seleccionado and tipo_seleccionado != 'todos':
        flota_filtrada = datos_flota[datos_flota['tipo_vehiculo'] == tipo_seleccionado]
    else:
        flota_filtrada = datos_flota.copy()

    total_filtrados = len(flota_filtrada)
    if total_filtrados == 0:
        print(f"No hay registros para '{tipo_seleccionado}'.")
        return

    servicios_evaluar = ['llantas_nuevas', 'balanceo', 'pinchadura']
    print(f"\nVolumen de Servicios Complementarios [{tipo_seleccionado.upper() if tipo_seleccionado else 'TODOS'}] (Total: {total_filtrados} vehículos):")
    print("-" * 65)
    print(f"{'Servicio Adicional':<25} | {'Vehículos':<10} | {'Tasa de Conversión':<15}")
    print("-" * 65)

    # Cuenta los valores iguales a si y divide esa cantidad entre el total filtrado.
    for servicio_clave in servicios_evaluar:
        if servicio_clave in flota_filtrada.columns:
            cantidad = (flota_filtrada[servicio_clave] == 'si').sum()
            tasa = round((cantidad / total_filtrados) * 100, 2)
            nombre_fmt = servicio_clave.replace('_', ' ').capitalize()
            print(f"{nombre_fmt:<25} | {cantidad:<10} | {tasa}%")

    print(f"\nTop 5 Marcas con mayor representación:")
    # Cuenta las marcas, las ordena de mayor a menor y conserva solo las cinco primeras.
    top_marcas = flota_filtrada['marca'].value_counts().head(5)
    for marca_nombre, conteo in top_marcas.items():
        porcentaje_m = round((conteo / total_filtrados) * 100, 2)
        print(f" -> {marca_nombre.upper()}: {conteo} unidades ({porcentaje_m}%)")