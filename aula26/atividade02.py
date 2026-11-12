import subprocess
import pandas as pd
import polars as pl
from datetime import datetime

pl.Config.set_tbl_cols(-1)
pl.Config.set_tbl_width_chars(250)

subprocess.run('cls', shell=True)

ENDERECO_DADOS = './../DADOS/AUXILIO/'


try:
    inicio = datetime.now()
    print('Obtendo dados parquet...')

    df_auxilio_brasil = pl.scan_parquet(ENDERECO_DADOS + 'auxilio_brasil.parquet')

    df_auxilio_brasil = df_auxilio_brasil.collect()
    print(df_auxilio_brasil.head())

    fim = datetime.now()
    print(f'Tempo total{fim - inicio}')
    
    # Tempo total: 0:00:16.86

except Exception as e:
    print(f'Erro ao obter dados parquet - {e}')
    print(f'Linha: {e.__traceback__.tb_lineno}')