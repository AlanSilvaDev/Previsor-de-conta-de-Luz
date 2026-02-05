import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import locale
from datetime import datetime

# =====================
# CONFIGURAÇÕES GERAIS
# =====================
st.set_page_config(
    page_title="Previsor de Conta de Energia",
    page_icon="⚡",
    layout="centered"
)

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

# =====================
# TÍTULO
# =====================
st.title("⚡ Previsor de Conta de Energia")
st.caption("Estimativa inteligente baseada no histórico de consumo")

st.divider()

# =====================
# INPUTS
# =====================
st.subheader("📥 Informe os consumos (kWh)")

consumo1 = st.number_input("Consumo há 3 meses", min_value=0.0)
consumo2 = st.number_input("Consumo há 2 meses", min_value=0.0)
consumo3 = st.number_input("Consumo no último mês", min_value=0.0)

mes_atual = st.selectbox(
    "Mês atual",
    options=list(range(1, 13)),
    format_func=lambda x: datetime(2025, x, 1).strftime("%B").capitalize()
)

# =====================
# BOTÃO
# =====================
if st.button("🔮 Prever Conta de Luz"):

    payload = {
        "consumo1": consumo1,
        "consumo2": consumo2,
        "consumo3": consumo3,
        "mes_atual": mes_atual
    }

    try:
        res = requests.post(
            "http://127.0.0.1:8000/prever",
            json=payload
        )

        previsao = res.json()["previsao_reais"]

        st.success("✅ Previsão realizada com sucesso!")

        # =====================
        # KPI
        # =====================
        st.metric(
            label="💰 Valor estimado da próxima conta",
            value=f"R$ {previsao:.2f}"
        )

        st.divider()

        # =====================
        # GRÁFICO PROFISSIONAL
        # =====================
        meses = [
            "Há 3 meses",
            "Há 2 meses",
            "Mês passado",
            datetime(2025, mes_atual, 1).strftime("%B").capitalize()
        ]

        consumos = [
            consumo1,
            consumo2,
            consumo3,
            consumo3
        ]

        df = pd.DataFrame({
            "Mês": meses,
            "Consumo (kWh)": consumos
        })

        fig = px.line(
            df,
            x="Mês",
            y="Consumo (kWh)",
            markers=True,
            title="📊 Histórico Recente de Consumo de Energia",
        )

        fig.update_layout(
            title_x=0.5,
            template="plotly_white",
            yaxis_title="Consumo (kWh)",
            xaxis_title=""
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "O modelo utiliza o consumo histórico e o mês atual "
            "para estimar o valor da próxima fatura."
        )

    except Exception as e:
        st.error("❌ Erro ao conectar com a API")
        st.exception(e)
