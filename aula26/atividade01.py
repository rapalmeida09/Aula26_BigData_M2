import subprocess
import pandas as pd
import polars as pl
from datetime import datetime
import os


subprocess.run('cls', shell=True)

ENDERECO_DADOS = './../DADOS/AUXILIO/'

try:
    inicio = datetime.now()
    print('Obtendo dados do Auxilio Brasil...')

    df_auxilio_brasil = None
    lista_arquivos = []

    lista_dir_arquivos = os.listdir(ENDERECO_DADOS)

    for arquivo in lista_dir_arquivos:
        if arquivo.endswith('.csv'):
            lista_arquivos.append(arquivo)

    for arquivo in lista_arquivos:
        print(f'\nProcessando o arquivo {arquivo}...')

        df = pl.read_csv(  
            ENDERECO_DADOS + arquivo,
            separator=';',
            encoding='iso8859-1'
    ) 
        if df_auxilio_brasil is None:
                df_auxilio_brasil = df
        else:
            df_auxilio_brasil = pl.concat([df_auxilio_brasil, df])

        del df

        print(df_auxilio_brasil.head())
        print(f'\nArquivo {arquivo} processado com sucesso!')

    print(f'Dados concatenados com sucesso!!!')
    print(df_auxilio_brasil)

    fim = datetime.now()
    print(f'Tempo total{fim - inicio}')

except Exception as e:
    print(f'Erro ao obter dados - {e}')
    print(f'Linha: {e.__traceback__.tb_lineno}')

try:
    df_auxilio_brasil = df_auxilio_brasil.with_columns(
        pl.col('VALOR PARCELA')
        .str.replace(',', '.')
        .cast(pl.Float64)
    )

    print(df_auxilio_brasil)

    print(f'\nSalvando arquivo parquet...')
    df_auxilio_brasil.write_parquet('./../DADOS/AUXILIO/auxilio_brasil.parquet')
    print('Arquivo parquet criado com sucesso!!!')
     
except Exception as e:
    print(f'Erro ao salvar arquivo - {e}')
    print(f'Linha: {e.__traceback__.tb_lineno}')