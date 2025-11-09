import streamlit as st
import pandas as pd
import joblib

modelo = joblib.load(r"C:\Users\pedro\OneDrive\Documentos\fraude\1\fraud_detection_pipeline.pkl")  # seu modelo salvo

# Interface
st.title("💳 Detecção de Fraudes em Transações")
st.write("Cole abaixo a linha de dados (valores separados por vírgula) conforme a ordem do modelo:")

st.code("Exemplo:\n-0.26064780489439815,-0.46964845005363426,2.4962660826315637,...,17982.1,0")

input_text = st.text_area("Cole os valores aqui:", height=100, placeholder="Cole a linha de dados aqui...")

# Colunas do modelo
colunas = [
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14",
    "V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28",
    "Amount","Class"
]

# Fazer previsão
if st.button("🔍 Verificar se é Fraude"):
    try:
        # Converter a linha em lista de floats
        valores = [float(x.strip()) for x in input_text.split(",")]

        # Validar o número de colunas
        if len(valores) != len(colunas):
            st.error(f"Número incorreto de valores! Esperado {len(colunas)}, recebido {len(valores)}.")
        else:
            # Criar DataFrame (sem a coluna 'Class', pois ela é o rótulo)
            df = pd.DataFrame([valores[:-1]], columns=colunas[:-1])

            previsao = modelo.predict(df)[0]
            prob = modelo.predict_proba(df)[0][1] if hasattr(modelo, "predict_proba") else None

            if previsao == 1:
                st.error(f"🚨 Fraude detectada! (Probabilidade: {prob:.2%}" if prob else "🚨 Fraude detectada!")
            else:
                st.success(f"✅ Transação segura. (Probabilidade de fraude: {prob:.2%}" if prob else "✅ Transação segura.")

    except Exception as e:
        st.error(f"Erro ao processar entrada: {e}")
