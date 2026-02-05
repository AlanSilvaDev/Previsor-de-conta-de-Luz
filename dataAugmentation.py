import numpy as np
import pandas as pd

df = pd.read_csv("data.csv", encoding='latin-1', sep= ';')

# transformar coluna mes em data
df['mes'] = pd.to_datetime(df['mês'])

def aumentar_dados(df, n_copias=70):
    dfs = [df]

    for _ in range(n_copias):
        df_fake = df.copy()

        # ruído no consumo (±8%)
        ruido = np.random.normal(0, 0.08, len(df))
        df_fake['consumo_kwh'] = df_fake['consumo_kwh'] * (1 + ruido)

        # conta segue o consumo (±5%)
        ruido_valor = np.random.normal(0, 0.05, len(df))
        df_fake['valor_reais'] = df_fake['valor_reais'] * (1 + ruido_valor)

        dfs.append(df_fake)

    return pd.concat(dfs, ignore_index=True)

df_aug = aumentar_dados(df, n_copias=70)
df_aug ['consumo_kwh'] = df_aug ['consumo_kwh'].round(2)
df_aug ['valor_reais'] = df_aug ['valor_reais'].round(2)

print("Tamanho original:", len(df))
print("Tamanho aumentado:", len(df_aug))

df_aug.to_csv("data_aumentada.csv", index=False, encoding='latin-1', sep=';')



