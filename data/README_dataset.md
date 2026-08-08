# Documentación del dataset — OULAD

| Campo | Valor |
|---|---|
| **Fuente** | The Open University (Reino Unido) — Knowledge Media Institute |
| **URL de descarga** | http://schools.stem.open.ac.uk/cdn/files/anonymisedData.zip |
| **Página oficial** | https://research.stem.open.ac.uk/ouanalyse/dataset/ |
| **Licencia** | CC-BY 4.0 |
| **Cita académica** | Kuzilek, J., Hlosta, M., Zdrahal, Z. "Open University Learning Analytics dataset." *Nature Scientific Data* 4, 170171 (2017). doi: 10.1038/sdata.2017.171 |
| **Fecha de descarga** | _(completar con la fecha real en que se ejecutó la celda de descarga)_ |
| **N.° de registros (studentVle.csv)** | 10,655,280 |
| **N.° de columnas (studentVle.csv)** | 6 (code_module, code_presentation, id_student, id_site, date, sum_click) |
| **Tamaño en disco (zip completo)** | ~300 MB |
| **Tablas utilizadas** | `studentVle.csv`, `studentInfo.csv`, `vle.csv` |

## Dominio de referencia (PFC)

**BCEL — SGA Escuela Provincias Unidas**, específicamente el **microservicio Docente**
(Django REST + gRPC, esquema `sga_docente` en PostgreSQL sobre AWS EC2), responsable
de asistencias y evaluaciones/calificaciones.

Ver la justificación técnica completa (>100 palabras) en la primera celda del notebook
`notebooks/PE_U4_pipeline_spark.ipynb`.

## Mapeo de tablas OULAD → dominio BCEL

| Tabla OULAD | Interpretación en el dominio BCEL |
|---|---|
| `studentVle` | Bitácora de interacciones/asistencias del microservicio Docente |
| `studentInfo` | Expediente/matrícula del estudiante |
| `vle` | Catálogo de actividades/recursos del curso |

## Nota sobre el piso de admisibilidad

El piso institucional exige ≥500,000 registros. `studentVle.csv` con 10,655,280
registros lo supera ampliamente (más de 21x el mínimo exigido).
