# PE-U4 — Ley de Amdahl con Apache Spark

**Dominio de referencia:** BCEL — SGA Escuela Provincias Unidas (Microservicio Docente)
**Asignatura:** Aplicaciones Distribuidas (ISR-701) — Unidad 4
**Código de actividad:** GA-SUM-05 / PE-U4
**Período académico:** 2026-2027 PPA

## Equipo

| Integrante | Rol |
|---|---|
| Keyla Bedón | Estructura, repositorio, notebooks, documento (introducción, resumen, pregunta 1, procedimiento, analisis critico, conclusión individual y compilación final |
| Juliana Emanuel | Marco teórico (Amdahl/Gustafson, MapReduce/Hadoop), Pregunta 3, conclusion, analisis critico |
| Harol Vinueza | Marco teórico (Spark, Cloud Computing), Pregunta 4, script de verificación de equivalencia |
| Pedro Castro | Resultados, figuras, Preguntas 2, evidencia, conclusión, analisis critico |

## Cómo ejecutar el notebook (Google Colab, recomendado)

1. Abrir `notebooks/PE_U4_pipeline_spark.ipynb` en Google Colab.
2. Subir la carpeta `src/` al entorno de Colab (o clonar este repo dentro de Colab con `!git clone <URL_DE_ESTE_REPO>` y `%cd pe-u4-spark-bcel`).
3. Ejecutar todas las celdas en orden. La celda de descarga trae el dataset real OULAD (~300 MB) desde `http://schools.stem.open.ac.uk/cdn/files/anonymisedData.zip`.
4. Al llegar a la sección de PySpark, abrir la Spark UI y capturar el DAG/stages del job de T3; guardar la imagen en `evidencia/spark_ui_t3.png`.
5. Verificar que `resultados/figuras/` contiene las figuras a 300 DPI y que `resultados/tiempos_crudos.csv` y `resultados/tiempos_resumen.csv` se generaron.

> **Nota sobre T3 y T4:** los CSV de salida de estas dos transformaciones no se versionan en `data/pandas/` ni `data/spark/` por exceder el límite de tamaño de archivo de GitHub. Los resultados numéricos de T3 y T4 sí están documentados en `resultados/tiempos_resumen.csv` y en el informe; solo se excluyen los CSV crudos de datos.

## Trabajo colaborativo en Overleaf

El equipo redacta y compila el documento en Overleaf mientras trabaja (más cómodo para edición simultánea entre los 4 integrantes). Flujo recomendado:

1. Crear el proyecto en Overleaf subiendo `docs/PE_U4_Informe.tex` y `docs/references_U4.bib`
2. Cada integrante edita su sección asignada directamente en Overleaf
3. Antes de cada commit a GitHub, descargar la versión actualizada desde Overleaf (Menú → Download → Source, o usar Menú → GitHub → Sync si tienen esa integración disponible) y subirla a `docs/` en este repositorio

**Importante:** el docente verifica el piso P2 clonando este repositorio y compilando localmente con los comandos de abajo — no abre Overleaf. Por eso, aunque trabajen en Overleaf, siempre deben sincronizar el `.tex` final aquí y confirmar que compila también con la secuencia local antes de la entrega.

> El PDF compilado (`docs/PE_U4_Informe.pdf`) no se versiona en este repositorio; se regenera localmente con los comandos de abajo antes de la entrega.

## Cómo compilar el documento LaTeX (instrucciones EXACTAS, ya verificadas)

Requisitos del sistema (Ubuntu/Debian):

```bash
sudo apt-get install texlive-latex-extra texlive-bibtex-extra texlive-lang-spanish \
                     texlive-fonts-recommended biber lmodern
```

Comandos de compilación, en este orden exacto, desde la carpeta `docs/`:

```bash
cd docs
pdflatex -interaction=nonstopmode PE_U4_Informe.tex
biber PE_U4_Informe
pdflatex -interaction=nonstopmode PE_U4_Informe.tex
pdflatex -interaction=nonstopmode PE_U4_Informe.tex
```

Esta secuencia (pdflatex → biber → pdflatex → pdflatex) ya fue probada y compila sin errores y sin overfull hbox con la plantilla base. El archivo final se genera en `docs/PE_U4_Informe.pdf`.

## Dataset

OULAD (Open University Learning Analytics Dataset), CC-BY 4.0.
Cita: Kuzilek, J., Hlosta, M., Zdrahal, Z. (2017). "Open University Learning Analytics dataset." Nature Scientific Data 4, 170171. doi: 10.1038/sdata.2017.171
Documentación completa en `data/README_dataset.md`.

## Dominio de referencia (PFC)

BCEL — SGA Escuela Provincias Unidas, específicamente el microservicio Docente (Django REST + gRPC, esquema `sga_docente` en PostgreSQL sobre AWS EC2), responsable de asistencias y evaluaciones/calificaciones. Ver justificación técnica completa en la primera celda del notebook y en `data/README_dataset.md`.

## Estructura del repositorio

```
pe-u4-spark-bcel/
├── README.md
├── LICENSE
├── .gitignore
├── notebooks/
│   ├── PE_U4_pipeline_spark.ipynb   (notebook principal, ejecutado con resultados)
│   └── PE_U4_pipeline_spark.html    (exportado tras ejecutar)
├── src/
│   ├── transformaciones_pandas.py   (T1-T5 secuenciales)
│   ├── transformaciones_spark.py    (T1-T5 distribuidas)
│   ├── medicion.py                  (5 repeticiones, mediana, perf_counter)
│   ├── verificar_equivalencia.py    (verificación de equivalencia pandas vs PySpark, criterio 1.4)
│   └── graficas.py                  (figuras matplotlib 300 DPI + curvas Amdahl teóricas)
├── data/
│   ├── README_dataset.md            (documentación del dataset)
│   ├── pandas/                      (T1.csv, T2.csv, T5.csv — T3/T4 excluidos por límite de tamaño de GitHub)
│   └── spark/
├── resultados/
│   ├── tiempos_crudos.csv
│   ├── tiempos_resumen.csv
│   └── figuras/
│       ├── fig_amdahl_teorico_p.png (curvas p=0.5/0.75/0.9/0.95)
│       ├── fig1_barras.png
│       ├── fig2_speedup.png
│       └── fig3_eficiencia.png
├── evidencia/
│   └── verificacion_equivalencia_pru...  (evidencia del script de verificación; agregar spark_ui_t3.png)
└── docs/
    ├── PE_U4_Informe.tex            (contenido completo, se compila localmente)
    └── PE_U4_Informe.pdf            (Complicación en pdf)
    └── references_U4.bib            (referencias bibliográficas)

```
