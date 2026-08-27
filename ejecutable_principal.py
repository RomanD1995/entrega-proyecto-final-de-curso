"""
==============================================================================
EJECUTABLE PRINCIPAL - SISTEMA ALINEADORA HUNTER
==============================================================================
"""
import carga_de_datos as carga
import capacidad_operativa as capacidad
import calculo_de_salud as salud
import servicios_secundarios as servicios
import graficos_e_indicadores as graficos

# Carga la tabla una vez y dirige cada respuesta del usuario al analisis correspondiente.
# Para hacerlo, lee la opcion escrita y llama a la funcion del modulo que corresponde.
def menu_principal():
    # Llama a la funcion de carga; si devuelve None, detiene el programa para evitar analisis sin datos.
    datos_flota = carga.cargar_y_limpiar_base_de_datos()
    if datos_flota is None:
        print("\n[ERROR] No se pudo iniciar el programa.")
        return

    # Repite la impresion del menu y la lectura de opciones mientras el usuario no elija salir.
    while True:
        print("\n" + "="*65)
        print(f"  {carga.NOMBRE_DEL_PROYECTO.upper()}")
        print(f"  Versión: {carga.VERSION_DEL_SISTEMA} | Autor: {carga.AUTOR_DEL_PROYECTO}")
        print("="*65)
        print("[1] Capacidad Operativa y Carga de Rampa")
        print("[2] Resumen General de Salud Vehicular (% Aprobados vs Rechazados)")
        print("[3] Diagnóstico de Salud Cruzado por Marca")
        print("[4] Análisis por Tipo de Vehículo y Servicios Secundarios")
        print("[5] Generar Gráficos de Indicadores Clave")
        print("[6] Salir")
        print("="*65)

        opcion = input("Seleccione una opción (1-6): ").strip()

        # Compara el texto escrito con cada opcion y ejecuta la funcion del modulo seleccionado.
        if opcion == '1':
            capacidad.calcular_capacidad_y_desempeno_puesto(datos_flota)
        elif opcion == '2':
            salud.analizar_salud_vehicular_general(datos_flota)
        elif opcion == '3':
            salud.analizar_salud_por_marca(datos_flota)
        elif opcion == '4':
            servicios.analizar_servicios_secundarios_por_tipo(datos_flota)
        elif opcion == '5':
            graficos.generar_graficos_indicadores(datos_flota)
        elif opcion == '6':
            print(f"\n¡Gracias por utilizar el sistema, {carga.AUTOR_DEL_PROYECTO}!")
            break
        else:
            print("\nOpción no válida. Ingrese un número entre el 1 y el 6.")

        # Lee una respuesta y solo repite el menu cuando el usuario escribe la letra s.
        continuar = input("\n¿Desea realizar otra consulta? (s/n): ").strip().lower()
        if continuar != 's':
            print("\nEjecución finalizada con éxito.")
            break

if __name__ == "__main__":
    menu_principal()