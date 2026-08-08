"""
Genera las 3 figuras exigidas por la guia GA-SUM-05 / PE-U4, exportadas a
300 DPI en resultados/figuras/.
"""
import numpy as np
import matplotlib.pyplot as plt


def fig1_barras_tiempos(transformaciones, t_pandas, t_spark, path="../resultados/figuras/fig1_barras.png"):
    x = np.arange(len(transformaciones))
    ancho = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - ancho / 2, t_pandas, ancho, label="pandas (secuencial)")
    ax.bar(x + ancho / 2, t_spark, ancho, label="PySpark (distribuido)")
    ax.set_xlabel("Transformación")
    ax.set_ylabel("Tiempo mediano (s)")
    ax.set_title("Tiempo de ejecución: pandas vs. PySpark por transformación")
    ax.set_xticks(x)
    ax.set_xticklabels(transformaciones)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def amdahl_speedup(p, N):
    """S(N) = 1 / ((1-p) + p/N)  -- Ecuacion (1) de la guia."""
    return 1.0 / ((1 - p) + p / N)


def fig2_speedup_vs_amdahl(N_medidos, speedup_medido, p_observado, path="../resultados/figuras/fig2_speedup.png"):
    N_teorico = np.linspace(1, max(N_medidos) * 1.5, 200)
    S_teorico = amdahl_speedup(p_observado, N_teorico)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(N_teorico, S_teorico, "--", label=f"Amdahl teórico (p={p_observado:.3f})")
    ax.plot(N_medidos, speedup_medido, "o-", label="Speedup experimental (T3)")
    ax.set_xlabel("Número de executors (N)")
    ax.set_ylabel("Speedup S(N)")
    ax.set_title("Speedup experimental vs. curva teórica de Amdahl (T3 - join)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def fig3_eficiencia(N_medidos, speedup_medido, path="../resultados/figuras/fig3_eficiencia.png"):
    eficiencia = [s / n for s, n in zip(speedup_medido, N_medidos)]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(N_medidos, eficiencia, "o-", color="darkorange")
    ax.axhline(1.0, color="gray", linestyle=":", label="Eficiencia ideal (E=1)")
    ax.set_xlabel("Número de executors (N)")
    ax.set_ylabel("Eficiencia E(N) = S(N)/N")
    ax.set_title("Eficiencia del paralelismo (T3 - join)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def curvas_amdahl_teoricas(path="../resultados/figuras/fig_amdahl_teorico_p.png"):
    """Figura de apoyo para la seccion 5.1 del marco teorico: curvas de
    Amdahl para p = 0.5, 0.75, 0.9, 0.95 (exigidas explicitamente por la guia)."""
    N = np.linspace(1, 64, 200)
    fig, ax = plt.subplots(figsize=(8, 5))
    for p in [0.5, 0.75, 0.9, 0.95]:
        ax.plot(N, amdahl_speedup(p, N), label=f"p={p}")
    ax.set_xlabel("Número de procesadores (N)")
    ax.set_ylabel("Speedup S(N)")
    ax.set_title("Ley de Amdahl: speedup teórico para distintas fracciones paralelizables")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def fraccion_serial_observada(N, S):
    """Forma inversa de Amdahl (ecuacion 4 de la guia) -- Karp-Flatt."""
    if N <= 1:
        raise ValueError("N debe ser > 1 para despejar p")
    return (1 / S - 1 / N) / (1 - 1 / N)
