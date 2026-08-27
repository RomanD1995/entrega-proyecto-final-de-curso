# Sistema de Análisis y Procesamiento para Rampas de Alineado Vehicular (SMA)

Este repositorio contiene el proyecto final para el curso universitario de **Análisis de Datos con Python**. El sistema permite procesar registros y datos operacionales de rampas de alineación automotriz, calcular métricas técnicas de rendimiento y capacidad, generar visualizaciones gráficas operativas y exportar datos limpios.

---

## 📋 Estructura del Repositorio

* `ejecutable_principal.py`: Punto de entrada e interfaz de menú interactivo en consola para dirigir la ejecución de los módulos.
* `carga_de_datos.py`: Módulo encargo de la lectura, validación, limpieza y normalización del dataset.
* `capacidad_operativa.py`: Módulo para el cálculo de capacidad teórica diaria, meta operativa y tiempos de rampa.
* `calculo_de_salud.py`: Análisis de diagnósticos cruzados y estado de salud general vehicular.
* `servicios_secundarios.py`: Análisis de demanda de servicios complementarios (llantas nuevas, balanceo y pinchaduras).
* `graficos_e_indicadores.py`: Generación de reportes gráficos e indicadores clave con **Matplotlib**.
* `base_datos_taller.xlsx`: Dataset original con los registros del taller.
* `registros_taller_procesado.csv`: Archivo generado automáticamente con los datos limpios tras el procesamiento.
* `LEEME ANTES DE ANALIZAR.txt`: Manual completo de uso, documentación del sistema y solución de errores comunes.
* `Plantilla IteraFlex_AvanceProyecto terminado.pdf`: Reporte y avance formal del proyecto.

---

## 🛠️ Requisitos del Sistema y Dependencias

* **Lenguaje:** Python (versiones 3.11 a 3.14 "dep versión").
* **Librerías principales:**
  * `pandas` (procesamiento y análisis de datos)
  * `matplotlib` (generación de gráficos e indicadores)
  * `openpyxl` (lectura de archivos Excel `.xlsx`)

### Instalación de dependencias

Ejecuta el siguiente comando en PowerShell o en la terminal integrada de VS Code:

```bash
py -m pip install pandas openpyxl matplotlib

(Si el comando py no está disponible, utiliza python -m pip install pandas openpyxl matplotlib).
​🚀 Instrucciones de Ejecución
​Clonar o descargar este repositorio en tu equipo.
​Abrir la terminal en la carpeta principal del proyecto.
​Iniciar el programa principal ejecutando:
py ejecutable_principal.py
El sistema cargará automáticamente base_datos_taller.xlsx (o registros_taller_procesado.csv en su ausencia) y mostrará el menú interactivo para realizar consultas y generar gráficos.
​
👤 Autor : Adonis Eloy Román Dinarte
Proyecto Final - Universidad
