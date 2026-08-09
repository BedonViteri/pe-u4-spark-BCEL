"""
Verificacion de equivalencia entre resultados de pandas y PySpark (criterio 1.4
de la rubrica GA-SUM-05 / PE-U4, 4% del total).

La guia exige verificar la equivalencia mediante:
    (a) cardinalidad (mismo numero de filas)
    (b) agregados de control (sumas, promedios y conteos por clave)
para cada una de las cinco transformaciones T1-T5.

Este script asume que ya se ejecutaron ambas implementaciones y produce un
reporte tabular con el resultado de cada verificacion. Se ejecuta DESPUES de
correr transformaciones_pandas.py y transformaciones_spark.py sobre el mismo
dataset (OULAD), dentro del notebook de Colab.

Uso tipico dentro del notebook:

    import transformaciones_pandas as tp
    import transformaciones_spark as ts
    from verificar_equivalencia import verificar_todas, guardar_reporte

    # --- pandas ---
    sv_p, si_p, v_p = tp.cargar_datos(path_sv, path_si, path_v)
    r1_p = tp.t1_filtrado_seleccion(sv_p)
    r2_p = tp.t2_agrupacion_agregacion(sv_p)
    r3_p = tp.t3_join(sv_p, si_p, v_p)
    r4_p = tp.t4_columna_derivada(r3_p)
    r5_p = tp.t5_orden_topn(r4_p)

    # --- spark ---
    spark = ts.crear_sesion_spark(n_executors=4)
    sv_s, si_s, v_s = ts.cargar_datos(spark, path_sv, path_si, path_v)
    r1_s = ts.t1_filtrado_seleccion(sv_s)
    r2_s = ts.t2_agrupacion_agregacion(sv_s)
    r3_s = ts.t3_join(sv_s, si_s, v_s)
    r4_s = ts.t4_columna_derivada(r3_s)
    r5_s = ts.t5_orden_topn(r4_s)

    resultados = verificar_todas(
        {"T1": (r1_p, r1_s), "T2": (r2_p, r2_s), "T3": (r3_p, r3_s),
         "T4": (r4_p, r4_s), "T5": (r5_p, r5_s)},
        columna_agregado="sum_click",
        columna_clave="id_student",
    )
    guardar_reporte(resultados, "../resultados/equivalencia_pandas_spark.csv")
"""
import pandas as pd


def _es_spark_df(df) -> bool:
    """Distingue un DataFrame de PySpark de uno de pandas sin importar pyspark
    a nivel de modulo (para que este script no dependa de tener pyspark
    instalado si solo se usa para inspeccionar resultados de pandas)."""
    return hasattr(df, "count") and not hasattr(df, "shape")


def _cardinalidad(df) -> int:
    if _es_spark_df(df):
        return df.count()
    return len(df)


def _agregados_control(df, columna_agregado: str, columna_clave: str) -> dict:
    """Calcula suma, promedio y conteo por clave de una columna numerica,
    tanto para un DataFrame de pandas como de PySpark. Si la columna no
    existe en el resultado (p. ej. T5 tras un top-N que no la conserva),
    devuelve None en los tres campos en lugar de fallar."""
    if _es_spark_df(df):
        from pyspark.sql import functions as F

        if columna_agregado not in df.columns:
            return {"suma": None, "promedio": None, "conteo_por_clave": None}
        agregado = df.agg(
            F.sum(columna_agregado).alias("suma"),
            F.avg(columna_agregado).alias("promedio"),
        ).collect()[0]
        conteo_por_clave = None
        if columna_clave in df.columns:
            conteo_por_clave = df.groupBy(columna_clave).count().count()
        return {
            "suma": agregado["suma"],
            "promedio": agregado["promedio"],
            "conteo_por_clave": conteo_por_clave,
        }
    else:
        if columna_agregado not in df.columns:
            return {"suma": None, "promedio": None, "conteo_por_clave": None}
        conteo_por_clave = None
        if columna_clave in df.columns:
            conteo_por_clave = df[columna_clave].nunique()
        return {
            "suma": float(df[columna_agregado].sum()),
            "promedio": float(df[columna_agregado].mean()),
            "conteo_por_clave": conteo_por_clave,
        }


def verificar_transformacion(
    nombre: str,
    df_pandas,
    df_spark,
    columna_agregado: str = "sum_click",
    columna_clave: str = "id_student",
    tolerancia_relativa: float = 1e-6,
) -> dict:
    """Verifica una transformacion individual: cardinalidad + agregados de
    control. Devuelve un dict con el resultado, listo para tabular."""
    card_pandas = _cardinalidad(df_pandas)
    card_spark = _cardinalidad(df_spark)
    cardinalidad_ok = card_pandas == card_spark

    agg_pandas = _agregados_control(df_pandas, columna_agregado, columna_clave)
    agg_spark = _agregados_control(df_spark, columna_agregado, columna_clave)

    def _cerca(a, b):
        if a is None or b is None:
            return a is None and b is None
        if a == 0 and b == 0:
            return True
        return abs(a - b) / max(abs(a), abs(b), 1e-12) < tolerancia_relativa

    suma_ok = _cerca(agg_pandas["suma"], agg_spark["suma"])
    promedio_ok = _cerca(agg_pandas["promedio"], agg_spark["promedio"])
    conteo_clave_ok = agg_pandas["conteo_por_clave"] == agg_spark["conteo_por_clave"]

    equivalente = cardinalidad_ok and suma_ok and promedio_ok and conteo_clave_ok

    return {
        "transformacion": nombre,
        "filas_pandas": card_pandas,
        "filas_spark": card_spark,
        "cardinalidad_ok": cardinalidad_ok,
        "suma_pandas": agg_pandas["suma"],
        "suma_spark": agg_spark["suma"],
        "suma_ok": suma_ok,
        "promedio_pandas": agg_pandas["promedio"],
        "promedio_spark": agg_spark["promedio"],
        "promedio_ok": promedio_ok,
        "conteo_clave_pandas": agg_pandas["conteo_por_clave"],
        "conteo_clave_spark": agg_spark["conteo_por_clave"],
        "conteo_clave_ok": conteo_clave_ok,
        "equivalente": equivalente,
    }


def verificar_todas(
    pares: dict,
    columna_agregado: str = "sum_click",
    columna_clave: str = "id_student",
) -> pd.DataFrame:
    """pares: dict {"T1": (df_pandas, df_spark), "T2": (...), ...}
    Devuelve un DataFrame de pandas con el resultado de las 5 verificaciones,
    listo para imprimir o exportar a CSV."""
    filas = []
    for nombre, (df_pandas, df_spark) in pares.items():
        filas.append(
            verificar_transformacion(
                nombre, df_pandas, df_spark, columna_agregado, columna_clave
            )
        )
    reporte = pd.DataFrame(filas)

    todas_equivalentes = reporte["equivalente"].all()
    print(f"\n{'=' * 60}")
    print(f"Verificacion de equivalencia pandas vs. PySpark (T1-T5)")
    print(f"{'=' * 60}")
    for _, fila in reporte.iterrows():
        estado = "OK" if fila["equivalente"] else "!!! DIFIERE !!!"
        print(
            f"  {fila['transformacion']}: filas pandas={fila['filas_pandas']}, "
            f"filas spark={fila['filas_spark']} -> {estado}"
        )
    print(f"{'=' * 60}")
    print(
        "RESULTADO GLOBAL: "
        + ("TODAS LAS TRANSFORMACIONES SON EQUIVALENTES"
           if todas_equivalentes
           else "HAY TRANSFORMACIONES QUE NO COINCIDEN -- revisar antes de reportar")
    )
    print(f"{'=' * 60}\n")

    return reporte


def guardar_reporte(reporte: pd.DataFrame, path: str) -> None:
    reporte.to_csv(path, index=False)
    print(f"Reporte de equivalencia guardado en: {path}")


if __name__ == "__main__":
    # Prueba minima con datos sinteticos, sin depender de pyspark instalado,
    # para validar la logica de comparacion en pandas-vs-pandas antes de
    # correrlo contra el notebook real.
    df_a = pd.DataFrame({"id_student": [1, 1, 2, 3], "sum_click": [10, 20, 5, 7]})
    df_b = pd.DataFrame({"id_student": [1, 1, 2, 3], "sum_click": [10, 20, 5, 7]})
    resultado = verificar_todas({"T_PRUEBA": (df_a, df_b)})
    assert resultado.loc[0, "equivalente"], "La prueba minima deberia dar equivalente=True"
    print("Prueba minima OK.")