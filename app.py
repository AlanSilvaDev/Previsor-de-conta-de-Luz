from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle
from joblib import load
import pandas as pd

app = FastAPI(
    title='API de Previsão de Conta de Luz',
    description="Previsão do valor de conta de energia com base no consumo (EQUATORIAL)",
    version="1.0"

)

modelo = load ("modelo_conta_luz.joblib")

#entrada
class entrada(BaseModel):
    consumo1: float #mes mais antigo
    consumo2: float
    consumo3: float #mes mais recente
    mes_atual:int



@app.post("/prever")
def prever(dados: entrada):

    consumo_anterior = dados.consumo2
    media_3_messes = (dados.consumo1 + dados.consumo2 + dados.consumo3) / 3
    mes_num = dados.mes_atual

    x = pd.DataFrame([{
        "consumo_anterior": consumo_anterior,
        "media_3_messes": media_3_messes,
        "mes_num": mes_num
    }])

    previsao = modelo.predict(x)

    return {
        "previsao_reais": round(float(previsao[0]), 2)
    }


@app.get("/")
def home():
    return{
        "mesagem":"API de Previão de Conta de Luz da Equatorial-PA",
        "como usar":"POST/prever"
    }