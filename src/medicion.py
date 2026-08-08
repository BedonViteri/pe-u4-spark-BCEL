"""
Protocolo de medicion: 5 repeticiones por transformacion, mediana,
descartando explicitamente la primera ejecucion (calentamiento).
"""
import time
import statistics
import csv


def medir(func, *args, repeticiones=5, **kwargs):
    """Ejecuta func(*args, **kwargs) `repeticiones` veces + 1 de calentamiento.
    Fuerza materializacion via `resultado_materializar` (count()/len()) para
    no medir solo la construccion perezosa del DAG en Spark.
    Devuelve (mediana_segundos, lista_tiempos_crudos, resultado_ultima_ejecucion).
    """
    # Calentamiento (descartado)
    _ = func(*args, **kwargs)

    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        # materializacion: si es DataFrame de Spark, .count(); si es pandas, len()
        if hasattr(resultado, "count") and not hasattr(resultado, "shape"):
            resultado.count()
        else:
            len(resultado)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)

    mediana = statistics.median(tiempos)
    return mediana, tiempos, resultado


def guardar_tiempos_crudos(registros, path="../resultados/tiempos_crudos.csv"):
    """registros: lista de dicts con claves
    transformacion, motor, n_executors, repeticion, tiempo_segundos
    """
    campos = ["transformacion", "motor", "n_executors", "repeticion", "tiempo_segundos"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for r in registros:
            writer.writerow(r)


def guardar_resumen(resumen, path="../resultados/tiempos_resumen.csv"):
    """resumen: lista de dicts con claves
    transformacion, motor, n_executors, mediana_segundos, speedup
    """
    campos = ["transformacion", "motor", "n_executors", "mediana_segundos", "speedup"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for r in resumen:
            writer.writerow(r)
