"""
Transformaciones T1-T5 en pandas (implementación secuencial de referencia)
Dominio: BCEL - Sistema de Gestion Academica (SGA)
Dataset: OULAD (Open University Learning Analytics Dataset)

Justificacion de mapeo al dominio BCEL:
    studentVle    ~ tabla de interacciones/bitacora de actividad del SGA
                    (equivalente a registros de acceso al aula virtual, entregas, etc.)
    studentInfo   ~ tabla de matricula/expediente del estudiante
    vle           ~ tabla de recursos/actividades del curso
Estas tres tablas, unidas por claves (id_student, code_module, code_presentation,
id_site), reproducen exactamente el patron relacional de un SGA real: estudiante -
matricula - curso - actividad - interaccion.
"""
import pandas as pd
import numpy as np


def cargar_datos(path_studentvle, path_studentinfo, path_vle):
    studentVle = pd.read_csv(path_studentvle)
    studentInfo = pd.read_csv(path_studentinfo)
    vle = pd.read_csv(path_vle)
    return studentVle, studentInfo, vle


def t1_filtrado_seleccion(studentVle: pd.DataFrame) -> pd.DataFrame:
    """T1: filtrado por condicion compuesta + seleccion de columnas.
    Interpretacion SGA: interacciones "activas" durante el periodo lectivo
    (date >= 0, es decir dentro del semestre, no en induccion previa) y con
    un nivel minimo de interaccion (sum_click > 5), quedandonos solo con las
    columnas relevantes para el reporte de actividad academica.
    """
    condicion = (studentVle["date"] >= 0) & (studentVle["sum_click"] > 5)
    resultado = studentVle.loc[
        condicion,
        ["id_student", "code_module", "code_presentation", "id_site", "date", "sum_click"],
    ]
    return resultado


def t2_agrupacion_agregacion(studentVle: pd.DataFrame) -> pd.DataFrame:
    """T2: groupby + al menos 3 funciones de agregacion.
    Interpretacion SGA: resumen de actividad por estudiante y curso, similar
    a un reporte de asistencia/participacion del docente.
    """
    resultado = (
        studentVle.groupby(["id_student", "code_module", "code_presentation"])
        .agg(
            total_clicks=("sum_click", "sum"),
            promedio_clicks=("sum_click", "mean"),
            interacciones=("sum_click", "count"),
            max_click_dia=("sum_click", "max"),
        )
        .reset_index()
    )
    return resultado


def t3_join(studentVle: pd.DataFrame, studentInfo: pd.DataFrame, vle: pd.DataFrame) -> pd.DataFrame:
    """T3: join de al menos dos DataFrames.
    Interpretacion SGA: cruce de la bitacora de interacciones con el
    expediente del estudiante y con el catalogo de recursos del curso -
    equivalente a un reporte academico consolidado.
    """
    paso1 = studentVle.merge(
        studentInfo, on=["id_student", "code_module", "code_presentation"], how="inner"
    )
    resultado = paso1.merge(
        vle, on=["id_site", "code_module", "code_presentation"], how="inner", suffixes=("", "_recurso")
    )
    return resultado


def t4_columna_derivada(df_join: pd.DataFrame) -> pd.DataFrame:
    """T4: columna derivada compleja (expresion sobre varias columnas).
    Interpretacion SGA: indice de riesgo academico compuesto, combinando
    actividad (clicks), historial (intentos previos) y carga academica.
    """
    df = df_join.copy()
    peso_riesgo_intentos = df["num_of_prev_attempts"].astype(float) * 8.0
    peso_disability = np.where(df["disability"] == "Y", 5.0, 0.0)
    peso_actividad = np.clip(50.0 - (df["sum_click"].astype(float) * 0.5), 0, 50)
    df["indice_riesgo_academico"] = (
        peso_riesgo_intentos + peso_disability + peso_actividad
    ) / df["studied_credits"].astype(float) * 100
    return df


def t5_orden_topn(df_derivado: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """T5: ordenamiento + top-N.
    Interpretacion SGA: listado de los N estudiantes con mayor indice de
    riesgo academico, para priorizar tutorias / alertas tempranas.
    """
    resultado = (
        df_derivado.sort_values("indice_riesgo_academico", ascending=False)
        .drop_duplicates(subset=["id_student", "code_module", "code_presentation"])
        .head(n)
    )
    return resultado


if __name__ == "__main__":
    sv, si, v = cargar_datos(
        "../data/studentVle_sample.csv",
        "../data/studentInfo_sample.csv",
        "../data/vle_sample.csv",
    )
    r1 = t1_filtrado_seleccion(sv)
    r2 = t2_agrupacion_agregacion(sv)
    r3 = t3_join(sv, si, v)
    r4 = t4_columna_derivada(r3)
    r5 = t5_orden_topn(r4)
    print("T1:", r1.shape)
    print("T2:", r2.shape)
    print("T3:", r3.shape)
    print("T4:", r4.shape)
    print("T5:", r5.shape)
    print(r5[["id_student", "code_module", "indice_riesgo_academico"]].head())
