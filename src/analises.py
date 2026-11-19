"""
Módulo de Análise e Previsão de Séries Temporais - Projeto 2 (C11)
Instituto Nacional de Telecomunicações (Inatel)
Docente: Prof. Dr. Renzo Mesquita Paranaíba

Dataset: PJME_hourly.csv (Hourly Energy Consumption - PJM East)
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing


# Configurações visuais globais para gráficos prontos para slides (apresentação de 5 min)
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#F8FAFC",
    "axes.edgecolor": "#CBD5E1",
    "axes.grid": True,
    "grid.color": "#E2E8F0",
    "grid.linestyle": "--",
    "grid.alpha": 0.8,
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "axes.labelweight": "bold",
    "legend.fontsize": 10,
    "legend.frameon": True,
    "legend.facecolor": "white",
    "legend.edgecolor": "#CBD5E1",
})


def localizar_dataset(caminho_csv: str | Path | None = None) -> Path:
    """Localiza o arquivo PJME_hourly.csv na pasta c11-2-data do projeto."""
    if caminho_csv is not None:
        caminho = Path(caminho_csv)
        if caminho.exists():
            return caminho

    raiz_projeto = Path(__file__).resolve().parent.parent
    candidatos = [
        raiz_projeto / "c11-2-data" / "PJME_hourly.csv",
        raiz_projeto / "data" / "PJME_hourly.csv",
        Path("c11-2-data/PJME_hourly.csv"),
        Path("../c11-2-data/PJME_hourly.csv"),
    ]
    for candidato in candidatos:
        if candidato.exists():
            return candidato

    raise FileNotFoundError(
        "Arquivo 'PJME_hourly.csv' não encontrado na pasta 'c11-2-data/'."
    )


def carregar_e_limpar_serie(caminho_csv: str | Path | None = None) -> pd.Series:
    """
    Etapa 1: Carregamento, limpeza do timestamp e reamostragem semanal.
    - Converte a coluna Datetime para o tipo datetime.
    - Ordena cronologicamente os registros.
    - Remove timestamps duplicados (transições de horário de verão).
    - Reamostra a série horária para média semanal: resample('W').mean().
    """
    caminho = localizar_dataset(caminho_csv)
    df = pd.read_csv(caminho)

    # Conversão e limpeza de timestamp
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df = df.sort_values("Datetime")
    df = df.drop_duplicates(subset=["Datetime"], keep="first")
    df = df.set_index("Datetime")

    # Reamostragem para média semanal (52 semanas por ano)
    serie_semanal = df["PJME_MW"].resample("W").mean().dropna()
    serie_semanal.name = "Consumo_Semanal_MW"

    return serie_semanal


def plotar_serie_original(
    serie_semanal: pd.Series,
    salvar_em: str | Path | None = None,
    mostrar: bool = False,
) -> plt.Figure:
    """
    Gráfico 1: Série Temporal Original (Consumo Médio Semanal de Energia em MW).
    """
    fig, ax = plt.subplots(figsize=(13, 5.5))

    media_historica = serie_semanal.mean()

    ax.plot(
        serie_semanal.index,
        serie_semanal.values,
        color="#1D4ED8",
        linewidth=1.5,
        label="Consumo Médio Semanal (MW)",
    )
    ax.axhline(
        media_historica,
        color="#DC2626",
        linestyle="--",
        linewidth=1.8,
        label=f"Média Histórica ({media_historica:,.0f} MW)".replace(",", "."),
    )

    ax.set_title(
        "Gráfico 1: Série Temporal Original — Consumo Médio Semanal de Energia (PJM East: 2002–2018)",
        pad=14,
    )
    ax.set_xlabel("Data (Anos)")
    ax.set_ylabel("Consumo Médio de Energia (MW)")
    ax.set_ylim(23500, 49500)

    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper right")

    fig.tight_layout()

    if salvar_em:
        caminho_saida = Path(salvar_em)
        caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(caminho_saida, dpi=300, bbox_inches="tight")

    if mostrar:
        plt.show()

    return fig


def decompor_e_plotar_serie(
    serie_semanal: pd.Series,
    salvar_em: str | Path | None = None,
    mostrar: bool = False,
):
    """
    Gráfico 2: Decomposição da série temporal com seasonal_decompose
    (model='additive', period=52) e rótulos integralmente em português.
    """
    decomposicao = seasonal_decompose(
        serie_semanal,
        model="additive",
        period=52,
    )

    fig, axes = plt.subplots(4, 1, figsize=(13, 10), sharex=True)

    componentes = [
        (
            decomposicao.observed,
            "1. Série Original (Observada)",
            "Consumo (MW)",
            "#1D4ED8",
            "Consumo Médio Semanal Observado",
        ),
        (
            decomposicao.trend,
            "2. Tendência (Comportamento de Longo Prazo)",
            "Tendência (MW)",
            "#D97706",
            "Tendência Suavizada (Janela de 52 Semanas)",
        ),
        (
            decomposicao.seasonal,
            "3. Sazonalidade (Ciclo Anual Repetitivo — Período = 52 Semanas)",
            "Efeito Sazonal (MW)",
            "#059669",
            "Variação Sazonal Aditiva (Picos de Verão/Inverno)",
        ),
        (
            decomposicao.resid,
            "4. Resíduo (Flutuações Aleatórias / Ruído)",
            "Resíduo (MW)",
            "#64748B",
            "Resíduo (Variações Climáticas Atípicas)",
        ),
    ]

    for ax, (dados, titulo, ylabel, cor, legenda) in zip(axes, componentes):
        ax.plot(dados.index, dados.values, color=cor, linewidth=1.4, label=legenda)
        if titulo.startswith("3.") or titulo.startswith("4."):
            ax.axhline(0, color="#94A3B8", linestyle=":", linewidth=1.0)
        d_min, d_max = float(dados.min()), float(dados.max())
        margem = (d_max - d_min) * 0.22
        ax.set_ylim(d_min - margem * 0.35, d_max + margem)
        ax.set_title(titulo, fontsize=12, loc="left", pad=6)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.legend(loc="upper right", fontsize=9)

    axes[-1].set_xlabel("Data (Anos)")
    axes[-1].xaxis.set_major_locator(mdates.YearLocator(1))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    fig.suptitle(
        "Gráfico 2: Decomposição Aditiva da Série Temporal — Consumo de Energia PJM East (Período = 52 Semanas)",
        fontsize=14,
        fontweight="bold",
        y=0.995,
    )
    fig.tight_layout()

    if salvar_em:
        caminho_saida = Path(salvar_em)
        caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(caminho_saida, dpi=300, bbox_inches="tight")

    if mostrar:
        plt.show()

    return decomposicao, fig


def prever_holt_winters_e_plotar(
    serie_semanal: pd.Series,
    salvar_em: str | Path | None = None,
    mostrar: bool = False,
):
    """
    Gráfico 3: Previsão de 52 semanas usando Suavização Exponencial de Holt-Winters
    (ExponentialSmoothing com trend='add', seasonal='add', seasonal_periods=52)
    e cálculo exclusivo do MAPE (Erro Percentual Absoluto Médio).
    """
    horizonte = 52

    # Separação em Treino e Teste (últimas 52 semanas) para validação e cálculo do MAPE
    treino = serie_semanal.iloc[:-horizonte]
    teste = serie_semanal.iloc[-horizonte:]

    modelo_validacao = ExponentialSmoothing(
        treino,
        trend="add",
        seasonal="add",
        seasonal_periods=52,
    ).fit()

    previsao_teste = modelo_validacao.forecast(horizonte)

    # Cálculo exclusivo do MAPE (%)
    mape = float(np.mean(np.abs((teste - previsao_teste) / teste)) * 100)

    # Ajuste com toda a série para projetar as próximas 52 semanas futuras (2018–2019)
    modelo_futuro = ExponentialSmoothing(
        serie_semanal,
        trend="add",
        seasonal="add",
        seasonal_periods=52,
    ).fit()
    previsao_futura = modelo_futuro.forecast(horizonte)

    # Gráfico focado a partir de 2014 para visualização nítida nos slides + contexto histórico
    serie_recorte = treino.loc["2014-01-01":]

    fig, ax = plt.subplots(figsize=(13, 6))

    ax.plot(
        serie_recorte.index,
        serie_recorte.values,
        color="#1E3A8A",
        linewidth=1.6,
        label="Série Histórica de Treino (Observada)",
    )
    ax.plot(
        teste.index,
        teste.values,
        color="#0284C7",
        linewidth=2.0,
        label="Dados Reais — Últimas 52 Semanas (Validação)",
    )
    ax.plot(
        previsao_teste.index,
        previsao_teste.values,
        color="#EA580C",
        linestyle="--",
        linewidth=2.2,
        label=f"Previsão Holt-Winters — 52 Semanas de Validação (MAPE = {mape:.2f}%)",
    )
    ax.plot(
        previsao_futura.index,
        previsao_futura.values,
        color="#16A34A",
        linestyle="-.",
        linewidth=2.2,
        label="Previsão Futura Holt-Winters (+52 Semanas: Ago/2018 a Ago/2019)",
    )

    ax.axvline(
        teste.index[0],
        color="#64748B",
        linestyle=":",
        linewidth=1.3,
        label="Início da Janela de Previsão (52 Semanas)",
    )

    ax.set_title(
        f"Gráfico 3: Previsão de 52 Semanas com Suavização Exponencial de Holt-Winters (MAPE = {mape:.2f}%)",
        pad=14,
    )
    ax.set_xlabel("Data (Anos)")
    ax.set_ylabel("Consumo Médio Semanal de Energia (MW)")
    ax.set_ylim(23500, 48500)

    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper left")

    fig.tight_layout()

    if salvar_em:
        caminho_saida = Path(salvar_em)
        caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(caminho_saida, dpi=300, bbox_inches="tight")

    if mostrar:
        plt.show()

    return {
        "mape": mape,
        "treino": treino,
        "teste": teste,
        "previsao_teste": previsao_teste,
        "previsao_futura": previsao_futura,
        "figura": fig,
    }
