"""
Transformaciones T1-T5 en PySpark (implementacion distribuida)
Equivalente exacto de src/transformaciones_pandas.py, mismo dominio BCEL/OULAD.
"""
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def crear_sesion_spark(n_executors: int = 4) -> SparkSession:
    spark = (
        SparkSession.builder.appName("PE-U4-BCEL-SGA")
        .config("spark.executor.instances", str(n_executors))
        .getOrCreate()
    )
    return spark


def cargar_datos(spark: SparkSession, path_studentvle, path_studentinfo, path_vle):
    studentVle = spark.read.csv(path_studentvle, header=True, inferSchema=True)
    studentInfo = spark.read.csv(path_studentinfo, header=True, inferSchema=True)
    vle = spark.read.csv(path_vle, header=True, inferSchema=True)
    return studentVle, studentInfo, vle


def t1_filtrado_seleccion(studentVle: DataFrame) -> DataFrame:
    return (
        studentVle.filter((F.col("date") >= 0) & (F.col("sum_click") > 5))
        .select("id_student", "code_module", "code_presentation", "id_site", "date", "sum_click")
    )


def t2_agrupacion_agregacion(studentVle: DataFrame) -> DataFrame:
    return studentVle.groupBy("id_student", "code_module", "code_presentation").agg(
        F.sum("sum_click").alias("total_clicks"),
        F.avg("sum_click").alias("promedio_clicks"),
        F.count("sum_click").alias("interacciones"),
        F.max("sum_click").alias("max_click_dia"),
    )


def t3_join(studentVle: DataFrame, studentInfo: DataFrame, vle: DataFrame) -> DataFrame:
    paso1 = studentVle.join(
        studentInfo, on=["id_student", "code_module", "code_presentation"], how="inner"
    )
    resultado = paso1.join(
        vle, on=["id_site", "code_module", "code_presentation"], how="inner"
    )
    return resultado


def t4_columna_derivada(df_join: DataFrame) -> DataFrame:
    peso_riesgo_intentos = F.col("num_of_prev_attempts").cast("double") * 8.0
    peso_disability = F.when(F.col("disability") == "Y", 5.0).otherwise(0.0)
    peso_actividad = F.greatest(
        F.lit(0.0), F.least(F.lit(50.0), 50.0 - (F.col("sum_click").cast("double") * 0.5))
    )
    return df_join.withColumn(
        "indice_riesgo_academico",
        (peso_riesgo_intentos + peso_disability + peso_actividad)
        / F.col("studied_credits").cast("double")
        * 100,
    )


def t5_orden_topn(df_derivado: DataFrame, n: int = 20) -> DataFrame:
    return (
        df_derivado.dropDuplicates(["id_student", "code_module", "code_presentation"])
        .orderBy(F.col("indice_riesgo_academico").desc())
        .limit(n)
    )


if __name__ == "__main__":
    spark = crear_sesion_spark(n_executors=1)  # local: 1,2,4 se controlan via spark-submit --num-executors
    sv, si, v = cargar_datos(
        spark,
        "../data/studentVle_sample.csv",
        "../data/studentInfo_sample.csv",
        "../data/vle_sample.csv",
    )
    r1 = t1_filtrado_seleccion(sv)
    r2 = t2_agrupacion_agregacion(sv)
    r3 = t3_join(sv, si, v)
    r4 = t4_columna_derivada(r3)
    r5 = t5_orden_topn(r4)

    print("T1:", r1.count())
    print("T2:", r2.count())
    print("T3:", r3.count())
    print("T4:", r4.count())
    print("T5:", r5.count())
    r5.select("id_student", "code_module", "indice_riesgo_academico").show(5)
    spark.stop()
