# Aula26_BigData_M2
# Análise de Dados do Auxílio Brasil com Polars

Conjunto de scripts em Python para ler, consolidar, armazenar e analisar os dados do **Auxílio Brasil** usando [Polars](https://pola.rs/). O fluxo parte de vários arquivos CSV, gera um único arquivo Parquet e, a partir dele, executa consultas otimizadas e cálculos estatísticos.

## Estrutura do projeto

```
.
├── atividade01.py      # Lê os CSVs, concatena e salva em Parquet
├── atividade02.py      # Lê o Parquet (scan_parquet) e mede o tempo de carga
├── exemplo01.py        # Consulta lazy + média e mediana (script)
├── exemplo02.ipynb     # Mesmo exemplo em notebook, com quartis e IQR
└── ../DADOS/AUXILIO/   # Pasta de dados (fora do projeto)
    ├── *.csv           # Arquivos originais do Auxílio Brasil
    └── auxilio_brasil.parquet   # Gerado pela atividade01.py
```

> O caminho dos dados é definido pela constante `ENDERECO_DADOS`. Nos scripts `.py` é `./../DADOS/AUXILIO/`; no notebook é `./../../DADOS/AUXILIO/`, pois ele fica uma pasta mais abaixo.

## Requisitos

- Python 3.10 ou superior (o notebook foi executado com Python 3.13.7)
- Bibliotecas:

```bash
pip install polars pandas numpy pyarrow jupyter
```

> `pandas` é importado em todos os arquivos, mas não é utilizado no código atual.

## Dados de entrada

Os arquivos CSV devem estar em `../DADOS/AUXILIO/` com as seguintes características:

| Item | Valor |
|------|-------|
| Separador | `;` |
| Codificação | `iso8859-1` |
| Colunas usadas | `NOME MUNICÍPIO`, `VALOR PARCELA` |

A coluna `VALOR PARCELA` vem como texto com vírgula decimal (ex.: `600,00`) e é convertida para `Float64` na `atividade01.py`.

## Descrição dos scripts

### `atividade01.py` — Consolidação dos CSVs em Parquet

1. Lista todos os arquivos `.csv` da pasta de dados.
2. Lê cada um com `pl.read_csv` (separador `;`, encoding `iso8859-1`).
3. Concatena todos em um único DataFrame com `pl.concat`.
4. Converte `VALOR PARCELA` de texto para `Float64` (troca `,` por `.`).
5. Salva o resultado em `auxilio_brasil.parquet`.
6. Exibe o tempo total de execução.

### `atividade02.py` — Leitura do Parquet

- Usa `pl.scan_parquet` (leitura lazy) seguido de `.collect()`.
- Configura o Polars para exibir todas as colunas (`set_tbl_cols(-1)`) e largura de 250 caracteres.
- Mostra as primeiras linhas e o tempo de carga (comentário no código registra ~16,86 s).

### `exemplo01.py` — Consulta lazy e estatísticas

Monta um plano de execução lazy que:

1. Seleciona `NOME MUNICÍPIO` e `VALOR PARCELA`.
2. Converte o município para `Categorical`.
3. Filtra parcelas **maiores que 2.000**.
4. Agrupa por município e soma os valores.
5. Ordena do maior para o menor total.

Depois converte a coluna de totais para um array NumPy e calcula a **média**, a **mediana** e a **distância percentual** entre elas. Nesta versão do script, apenas a média é impressa.

### `exemplo02.ipynb` — Versão em notebook

Executa a mesma consulta do `exemplo01.py`, dividida em células, e acrescenta:

- Impressão de **média**, **mediana** e **distância percentual** entre ambas;
- Cálculo de **Q1**, **Q3** e **IQR** (amplitude interquartil) com `np.percentile`.

## Como executar

Execute na ordem, a partir da pasta do projeto:

```bash
# 1. Gera o arquivo Parquet a partir dos CSVs
python atividade01.py

# 2. Testa a leitura do Parquet
python atividade02.py

# 3. Consulta agregada e estatísticas
python exemplo01.py

# 4. Ou abra o notebook
jupyter notebook exemplo02.ipynb
```

## Observações

- Os scripts usam `subprocess.run('cls', shell=True)` para limpar o terminal, comando que funciona apenas no **Windows**. No Linux/macOS, troque por `'clear'` ou remova a linha.
- O formato Parquet é colunar e comprimido, por isso a leitura é muito mais rápida e leve do que reler todos os CSVs a cada análise.
- O uso de `scan_parquet` com `.select()` e `.filter()` permite que o Polars leia somente as colunas e linhas necessárias.
- Os blocos `try/except` exibem a mensagem de erro e o número da linha onde a falha ocorreu.
