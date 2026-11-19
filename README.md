# Projeto 2 - C11: Análise e Previsão de Séries Temporais
**Instituto Nacional de Telecomunicações (Inatel)**  
**Docente:** Prof. Dr. Renzo Mesquita Paranaíba  

---

## Integrantes do Grupo
| Nome                   | Matrícula | Curso |
|:-----------------------|:----------|:------|
| *Igor Araujo*          | *479*     | GES   |
| *Kevin Lopes do Vale*  | *1955*    | GEC   |
| *Felipe Fróes Pereira* | *566*     | GES   |

---

## Sobre o Projeto

Este projeto consiste na aplicação prática dos conceitos de **Análise e Previsão de Séries Temporais (Time Series)** estudados na disciplina **C11 (Ciência de Dados)**. A partir de dados históricos reais de consumo de energia elétrica da região leste dos Estados Unidos (**PJM East**), o trabalho realiza o tratamento temporal dos registros, reamostragem para média semanal, decomposição clássica da série em suas componentes fundamentais e previsão para um horizonte de 52 semanas utilizando **Suavização Exponencial de Holt-Winters**, avaliada de forma direta pelo **MAPE (Erro Percentual Absoluto Médio)**.

---

## Dataset Selecionado

- **Nome:** [Hourly Energy Consumption (PJM East - `PJME_hourly.csv`)](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)
- **Autor(a):** Rob Mulla / PJM Interconnection LLC (Kaggle)
- **Formato:** Arquivo CSV (`c11-2-data/PJME_hourly.csv`)
- **Volume:** 145.366 registros horários brutos entre janeiro de 2002 e agosto de 2018 (145.362 horas únicas após ordenação e remoção de 4 timestamps duplicados de horário de verão), consolidados em **866 observações semanais** via reamostragem pela média semanal (`resample('W').mean()`)
- **Licença:** CC0 / Domínio Público para uso acadêmico

### Contextualização do Problema
A **PJM Interconnection** é uma organização de transmissão regional (RTO) que coordena a movimentação de eletricidade no atacado em 13 estados da costa leste dos Estados Unidos. Como a energia elétrica em larga escala precisa ser gerada no exato momento em que é consumida, compreender o comportamento temporal da demanda e prever o consumo futuro com antecedência de 1 ano (52 semanas) é essencial para evitar apagões, dimensionar reservas operacionais e programar manutenções da rede elétrica nos períodos de menor carga.

### Variáveis do Dataset

| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| **`Datetime`** | `datetime64[ns]` (Índice Temporal) | Data e hora da medição original, convertida, ordenada cronologicamente e reamostrada em janelas semanais (`W`). |
| **`PJME_MW`** | `float64` (Numérica Contínua) | Consumo de energia elétrica na região PJM East, medido em **Megawatts (MW)**. Média histórica semanal de **32.082,36 MW**. |

---

## Respostas Objetivas às Perguntas Fundamentais

### 1. Tendência — *A série possui Tendência? Se sim, que tipo?*
- **Sim.** A componente de tendência extraída na decomposição mostra duas fases distintas no longo prazo:
  1. **Crescimento moderado (2002 a 2007):** O patamar médio anual subiu de **~31.571 MW** (2002) para o pico de **~33.618 MW** (2007).
  2. **Leve queda e estabilização (2008 a 2018):** Após 2008, a série apresenta uma **tendência suave de retração e estabilização** na faixa de **~31.000 MW a 32.000 MW**. Esse comportamento deve-se à adoção em massa de tecnologias de eficiência energética (iluminação LED, climatização e eletrodomésticos mais eficientes) e ao crescimento de geração solar distribuída.

### 2. Sazonalidade — *A série possui Sazonalidade? Se sim, qual o período que ela acontece?*
- **Sim.** A série apresenta uma **forte sazonalidade anual aditiva com período de 52 semanas (1 ano)**.
- Dentro de cada ciclo anual de 52 semanas ocorrem dois picos recorrentes de consumo e dois vales:
  - **Pico Principal no Verão (Julho/Agosto):** Causado pelo acionamento intensivo de sistemas de ar-condicionado (chegando a somar **+7.413 MW** acima da tendência).
  - **Pico Secundário no Inverno (Janeiro/Fevereiro):** Causado pela demanda de aquecimento residencial e comercial nos meses frios.
  - **Vales na Primavera (Abril/Maio) e Outono (Outubro/Novembro):** Temperaturas amenas reduzem a necessidade de climatização (chegando a **-4.853 MW** abaixo da tendência).
- A sazonalidade é **aditiva** porque a amplitude entre picos e vales mantém-se estável ao longo de todo o período de 2002 a 2018.

### 3. Ciclo — *A série apresenta um Ciclo? Se sim, por qual razão?*
- **Sim.** Além da sazonalidade fixa de 52 semanas, a curva de tendência exibe **oscilações cíclicas plurianuais** sem período fixo (duração variável de 2 a 4 anos).
- **Razões:**
  1. **Ciclos Macroeconômicos e Industriais:** A queda acentuada entre 2008 e 2009 reflete diretamente a retração da atividade industrial norte-americana durante a crise financeira global.
  2. **Fenômenos Climáticos Plurianuais:** Anos com ondas de calor ou invernos atipicamente rigorosos/amenos (influenciados por fenômenos como *El Niño* e *La Niña*) deslocam temporariamente o patamar médio anual de consumo.

### 4. Método de Previsão Escolhido e Avaliação (MAPE)
- **Método Escolhido:** **Suavização Exponencial Tripla de Holt-Winters Aditivo** (`ExponentialSmoothing` com `trend='add'`, `seasonal='add'` e `seasonal_periods=52`).
- **Justificativa:** É o método estudado em aula especificamente projetado para séries que combinam **nível**, **tendência** e **sazonalidade periódica de amplitude constante (aditiva)**.
- **Resultado da Previsão de 52 Semanas:**
  - **MAPE (Erro Percentual Absoluto Médio):** **`7,35%`** na janela de validação de 52 semanas.
  - Um erro médio inferior a 8% confirma que o modelo reproduz com fidelidade tanto os picos de verão e inverno quanto os vales de meia-estação ao longo de um ano inteiro de previsão.

### 5. Insights de Negócio
1. **Planejamento de Despacho e Compra Antecipada de Energia:** Sabendo com 52 semanas de antecedência que a média semanal nos picos de verão (julho/agosto) supera **38.000 MW**, a operadora elétrica pode firmar contratos futuros e preparar usinas de reserva com antecedência, evitando compras emergenciais a preços elevados no mercado *spot* e prevenindo blecautes.
2. **Janelas Ótimas para Manutenção Preventiva:** Os vales sazonais altamente previsíveis de **primavera (abril/maio)** e **outono (outubro/novembro)** — quando o consumo médio cai para a faixa de **25.000 a 27.000 MW** — constituem os momentos ideais para desligamento programado e manutenção preventiva de geradores, transformadores e linhas de transmissão, com risco mínimo para a segurança energética.
3. **Direcionamento de Investimentos em Infraestrutura:** Como a tendência de longo prazo encontra-se estabilizada/levemente decrescente, o setor elétrico não precisa expandir agressivamente a capacidade basal com novas usinas fósseis, podendo priorizar investimentos na resiliência da rede para suportar os picos sazonais de verão/inverno e na transição para fontes renováveis.

---

## Visualizações Geradas (Prontas para os Slides)

Todos os gráficos são gerados automaticamente em alta resolução (300 DPI) na pasta `slides/` com títulos, eixos e legendas em português:

1. **`slides/grafico1_serie_original.png`** — Série Temporal Original do Consumo Médio Semanal de Energia (2002–2018) e Média Histórica.
2. **`slides/grafico2_decomposicao.png`** — Decomposição Aditiva (`seasonal_decompose`, `model='additive'`, `period=52`) nas 4 componentes: Série Original, Tendência, Sazonalidade e Resíduo.
3. **`slides/grafico3_previsao_holt_winters.png`** — Previsão de 52 Semanas via Suavização Exponencial de Holt-Winters (`trend='add'`, `seasonal='add'`, `seasonal_periods=52`) com **MAPE = 7,35%**.

---

## Tecnologias e Ferramentas

O projeto é desenvolvido integralmente em **Python**, utilizando as bibliotecas abordadas na disciplina:

- **[Python 3.10+](https://www.python.org/):** Linguagem base do projeto.
- **[Pandas](https://pandas.pydata.org/):** Conversão e limpeza de timestamps, indexação temporal e reamostragem semanal (`resample('W').mean()`).
- **[NumPy](https://numpy.org/):** Operações vetoriais e cálculo do **MAPE**.
- **[Matplotlib](https://matplotlib.org/):** Construção e formatação dos gráficos analíticos em português para apresentação.
- **[Statsmodels](https://www.statsmodels.org/):** Decomposição clássica (`seasonal_decompose`) e Suavização Exponencial de Holt-Winters (`ExponentialSmoothing`).
- **[Jupyter Notebook](https://jupyter.org/):** Ambiente interativo para documentação, código e exibição dos gráficos.

---

## Estrutura do Repositório

```text
├── c11-2-data/
│   └── PJME_hourly.csv                                       # Dataset original do Kaggle (PJM East)
├── notebooks/
│   └── analise_projeto_c11.ipynb                             # Notebook com limpeza, decomposição e Holt-Winters
├── src/
│   └── analises.py                                           # Funções modulares de limpeza, gráficos e previsão
├── slides/
│   ├── grafico1_serie_original.png                           # Gráfico 1: Série temporal original
│   ├── grafico2_decomposicao.png                             # Gráfico 2: Decomposição aditiva (período = 52)
│   └── grafico3_previsao_holt_winters.png                    # Gráfico 3: Previsão Holt-Winters (52 semanas + MAPE)
├── .gitignore
├── main.py                                                   # Script principal para execução direta via terminal
├── README.md
└── requirements.txt                                          # Dependências do projeto
```

---

## Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/Sanak3/Proj-C11-2
cd Proj-C11-2
```

### 2. Criar e ativar um ambiente virtual (recomendado)
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar as análises
Você pode abrir o notebook interativo no Jupyter:
```bash
jupyter notebook notebooks/analise_projeto_c11.ipynb
```
Ou executar o script Python diretamente via terminal (que gera os 3 gráficos na pasta `slides/` e exibe o MAPE no console):
```bash
python main.py
```

---

## Etapas da Análise de Séries Temporais

1. **Carregamento e Limpeza do Timestamp:** Leitura do arquivo `c11-2-data/PJME_hourly.csv`, conversão para `datetime`, ordenação cronológica e remoção de 4 timestamps duplicados de transição de horário de verão.
2. **Reamostragem Semanal:** Agregação dos dados horários pela média semanal (`resample('W').mean()`), resultando em 866 semanas completas de 2002 a 2018.
3. **Traçado da Série Original (Gráfico 1):** Visualização do comportamento global do consumo em MW e da linha de média histórica (32.082 MW).
4. **Decomposição Clássica Aditiva (Gráfico 2):** Separação da série via `seasonal_decompose(model='additive', period=52)` em Série Observada, Tendência, Sazonalidade e Resíduo.
5. **Modelagem e Previsão com Holt-Winters (Gráfico 3):** Aplicação do `ExponentialSmoothing(trend='add', seasonal='add', seasonal_periods=52)` para prever 52 semanas e avaliação exclusiva pelo **MAPE (7,35%)**.
6. **Síntese e Insights de Negócio:** Interpretação prática voltada à gestão de demanda, contratação de energia e manutenção preventiva no setor elétrico.

---

## Licença e Referências

- Dataset original disponibilizado por **Rob Mulla** ([Hourly Energy Consumption - PJM Interconnection](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)) no Kaggle.
- Projeto desenvolvido para fins estritamente acadêmicos na disciplina **C11 - Ciência de Dados** do **Inatel**.
