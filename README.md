# PE-U4 — Ley de Amdahl con Apache Spark
## Dominio de referencia: BCEL — SGA Escuela Provincias Unidas (Microservicio Docente)

**Asignatura:** Aplicaciones Distribuidas (ISR-701) — Unidad 4
**Código de actividad:** GA-SUM-05 / PE-U4
**Período académico:** 2026-2027 PPA

## Equipo

| Integrante | Rol |
|---|---|
| Keyla Bedón | Coordinación, repositorio, notebook, compilación final |
| Juliana Emanuel | Marco teórico (Amdahl/Gustafson, MapReduce/Hadoop), Pregunta 1 |
| Harol Vinueza | Marco teórico (Spark, Cloud Computing), Pregunta 4 |
| Pedro Castro | Resultados, figuras, Preguntas 2-3, evidencia y video |

---

## Cómo ejecutar el notebook (Google Colab, recomendado)

1. Abrir `notebooks/PE_U4_pipeline_spark.ipynb` en Google Colab.
2. Subir la carpeta `src/` al entorno de Colab (o clonar este repo dentro de Colab con
   `!git clone <URL_DE_ESTE_REPO>` y `%cd pe-u4-spark-bcel`).
3. Ejecutar todas las celdas en orden. La celda de descarga trae el dataset real OULAD
   (~300 MB) desde `http://schools.stem.open.ac.uk/cdn/files/anonymisedData.zip`.
4. Al llegar a la sección de PySpark, abrir la Spark UI y capturar el DAG/stages del
   job de T3; guardar la imagen en `evidencia/spark_ui_t3.png`.
5. Verificar que `resultados/figuras/` contiene las 3 figuras a 300 DPI y que
   `resultados/tiempos_crudos.csv` y `resultados/tiempos_resumen.csv` se generaron.

## Trabajo colaborativo en Overleaf

El equipo redacta y compila el documento en **Overleaf** mientras trabaja (más cómodo
para edición simultánea entre los 4 integrantes). Flujo recomendado:

1. Crear el proyecto en Overleaf subiendo `docs/PE_U4_Informe.tex` y `docs/references_U4.bib`
2. Cada integrante edita su sección asignada directamente en Overleaf
3. **Antes de cada commit a GitHub**, descargar la versión actualizada desde Overleaf
   (`Menú → Download → Source`, o usar `Menú → GitHub → Sync` si tienen esa integración
   disponible) y subirla a `docs/` en este repositorio

**Importante:** el docente verifica el piso P2 clonando este repositorio y compilando
**localmente** con los comandos de abajo — no abre Overleaf. Por eso, aunque trabajen en
Overleaf, siempre deben sincronizar el `.tex` final aquí y confirmar que compila también
con la secuencia local antes de la entrega.

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

Esta secuencia (`pdflatex → biber → pdflatex → pdflatex`) ya fue probada y compila
**sin errores y sin overfull hbox** con la plantilla base. El archivo final se genera
en `docs/PE_U4_Informe.pdf`.

## Video de ejecución

_(Pedro: agregar aquí el link una vez grabado y subido — YouTube no listado o Drive
público, 2-5 minutos mostrando la ejecución completa del notebook)_

## Dataset

- **OULAD** (Open University Learning Analytics Dataset), CC-BY 4.0.
- Cita: Kuzilek, J., Hlosta, M., Zdrahal, Z. (2017). "Open University Learning Analytics
  dataset." *Nature Scientific Data* 4, 170171. doi: 10.1038/sdata.2017.171
- Documentación completa en `data/README_dataset.md`.

## Dominio de referencia (PFC)

BCEL — SGA Escuela Provincias Unidas, específicamente el **microservicio Docente**
(Django REST + gRPC, esquema `sga_docente` en PostgreSQL sobre AWS EC2), responsable
de asistencias y evaluaciones/calificaciones. Ver justificación técnica completa en
la primera celda del notebook y en `data/README_dataset.md`.

## Estructura del repositorio

```
pe-u4-spark-bcel/
├── README.md
├── LICENSE
├── .gitignore
├── notebooks/
│   ├── PE_U4_pipeline_spark.ipynb   (notebook principal, ejecutar en Colab)
│   └── PE_U4_pipeline_spark.html    (exportar tras ejecutar)
├── src/
│   ├── transformaciones_pandas.py   (T1-T5 secuenciales)
│   ├── transformaciones_spark.py    (T1-T5 distribuidas)
│   ├── medicion.py                  (5 repeticiones, mediana, perf_counter)
│   └── graficas.py                  (3 figuras matplotlib 300 DPI + curvas Amdahl teóricas)
├── data/
│   ├── README_dataset.md            (documentación del dataset)
│   ├── pandas/                      (CSV de salida, se llena al ejecutar)
│   └── spark/                       (CSV de salida, se llena al ejecutar)
├── resultados/
│   ├── tiempos_crudos.csv           (se genera al ejecutar)
│   ├── tiempos_resumen.csv          (se genera al ejecutar)
│   └── figuras/
│       ├── fig_amdahl_teorico_p.png (ya incluida: curvas p=0.5/0.75/0.9/0.95)
│       ├── fig1_barras.png          (se genera al ejecutar)
│       ├── fig2_speedup.png         (se genera al ejecutar)
│       └── fig3_eficiencia.png      (se genera al ejecutar)
├── evidencia/
│   └── spark_ui_t3.png              (agregar manualmente tras correr el notebook)
└── docs/
    ├── PE_U4_Informe.tex            (plantilla lista, con TODO por sección)
    ├── PE_U4_Informe.pdf            (compilado, se regenera con los comandos de arriba)
    └── references_U4.bib            (12 referencias base ya cargadas)
```

## Estado de la entrega

- [x] Estructura del repositorio
- [x] Dataset elegido, justificado y documentado (OULAD)
- [x] Código de las 5 transformaciones (pandas + PySpark), verificado
- [x] Plantilla LaTeX completa, compilación probada sin errores
- [x] Bibliografía base (12 refs con DOI/ISBN)
- [ ] Ejecución del notebook con dataset real en Colab
- [ ] Captura de Spark UI (`evidencia/spark_ui_t3.png`)
- [ ] Video de ejecución (2-5 min)
- [ ] Contenido de las secciones del `.tex` (marcadas con TODO)
- [ ] Conclusiones individuales por integrante
- [ ] Declaración de uso de IA generativa
- [ ] Commits distribuidos entre los 4 integrantes (≥3 c/u, fechas distintas)
