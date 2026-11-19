"""
Script Principal - Projeto 2: Análise e Previsão de Séries Temporais (C11)
Instituto Nacional de Telecomunicações (Inatel)
Docente: Prof. Dr. Renzo Mesquita Paranaíba

Executa o pipeline completo:
1. Carregamento e limpeza do timestamp (PJME_hourly.csv -> média semanal).
2. Gráfico 1: Série temporal original.
3. Gráfico 2: Decomposição aditiva (seasonal_decompose, model='additive', period=52).
4. Gráfico 3: Previsão de 52 semanas via Holt-Winters (trend='add', seasonal='add',
   seasonal_periods=52) e cálculo exclusivo do MAPE.
"""

from pathlib import Path
from src.analises import (
    carregar_e_limpar_serie,
    plotar_serie_original,
    decompor_e_plotar_serie,
    prever_holt_winters_e_plotar,
)


def main() -> None:
    pasta_saida = Path(__file__).resolve().parent / "slides"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("PROJETO 2 - C11: ANÁLISE E PREVISÃO DE SÉRIES TEMPORAIS (INATEL)")
    print("Dataset: PJME_hourly.csv (Consumo de Energia - PJM East)")
    print("=" * 72)

    # 1. Carregamento e limpeza do timestamp
    serie_semanal = carregar_e_limpar_serie()
    print(f"\n[1/4] Série carregada e reamostrada para média semanal ('W'):")
    print(f"      - Período: {serie_semanal.index.min().strftime('%d/%m/%Y')} a {serie_semanal.index.max().strftime('%d/%m/%Y')}")
    print(f"      - Total de semanas: {len(serie_semanal)}")
    print(f"      - Consumo médio histórico: {serie_semanal.mean():,.2f} MW".replace(",", "X").replace(".", ",").replace("X", "."))

    # 2. Gráfico 1: Série temporal original
    caminho_g1 = pasta_saida / "grafico1_serie_original.png"
    plotar_serie_original(serie_semanal, salvar_em=caminho_g1, mostrar=False)
    print(f"\n[2/4] Gráfico 1 (Série Original) salvo em: {caminho_g1}")

    # 3. Gráfico 2: Decomposição da série (model='additive', period=52)
    caminho_g2 = pasta_saida / "grafico2_decomposicao.png"
    decompor_e_plotar_serie(serie_semanal, salvar_em=caminho_g2, mostrar=False)
    print(f"[3/4] Gráfico 2 (Decomposição Aditiva - 52 semanas) salvo em: {caminho_g2}")

    # 4. Gráfico 3: Previsão de 52 semanas (Holt-Winters) e MAPE
    caminho_g3 = pasta_saida / "grafico3_previsao_holt_winters.png"
    resultado_hw = prever_holt_winters_e_plotar(
        serie_semanal, salvar_em=caminho_g3, mostrar=False
    )
    print(f"[4/4] Gráfico 3 (Previsão Holt-Winters - 52 semanas) salvo em: {caminho_g3}")
    print(f"\n>>> Resultado da Avaliação (Apenas MAPE): {resultado_hw['mape']:.2f}%")
    print("=" * 72)


if __name__ == "__main__":
    main()
