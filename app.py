import streamlit as st
import json
import os
import datetime
import urllib.parse
import pandas as pd
import re

st.set_page_config(
    page_title="Neurax Master AI - O Ecossistema de Elite",
    page_icon="⚡",
    layout="wide"
)

# Estilização Profissional
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { color: #0f172a !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    .stButton button[kind="primary"] { background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important; color: white !important; }
    [data-testid="stSidebar"] { background-color: #0f172a; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "users_neural_final.json"

def carregar_usuarios():
    # Estrutura inicial do sistema
    usuarios_padrao = {
        "leandrodesantana646@gmail.com": {
            "senha": "leandro1996",
            "nome": "Leandro (Dono)",
            "is_pro": True,
            "dias_pro_ganhos": 0,
            "amigos_indicados": 0,
            "codigo_indicacao": "LEANDRO99",
            "limites": {"casa": 2000.0, "lazer": 500.0, "despesas": 1000.0},
            "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
            "meta": {"titulo": "Reserva de Emergência", "alvo": 5000.0, "atual": 0.0}
        }
    }
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return usuarios_padrao
    return usuarios_padrao

def salvar_usuarios(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=4)

# Lógica do Core IA (Limites, Metas, Resumos, Insights)
def processar_gasto_ou_pergunta(query, user_data, user_email, users_dict):
    query = query.lower()
    
    # RESUMO SEMANAL
    if any(k in query for k in ["resumo", "raio-x", "semanal"]):
        total_gasto = sum(user_data["gastos_atuais"].values())
        maior_cat = max(user_data["gastos_atuais"], key=user_data["gastos_atuais"].get)
        return {
            "texto": f"📊 **Raio-X Semanal:**\n- Gasto Total: R$ {total_gasto:,.2f}\n- Categoria Crítica: {maior_cat.capitalize()}\n- Dica: Foque em reduzir {maior_cat} para atingir sua meta de R$ {user_data['meta']['alvo']}.",
            "grafico_tipo": "barras", "grafico_titulo": "Gastos da Semana",
            "grafico_dados": pd.DataFrame({"Valor": user_data["gastos_atuais"]}, index=["Casa", "Lazer", "Despesas"])
        }

    # METAS
    if "meta" in query or "guardar" in query:
        numeros = re.findall(r'\d+', query)
        if numeros:
            valor = float(numeros[0])
            users_dict[user_email]["meta"]["atual"] += valor
            salvar_usuarios(users_dict)
            return {"texto": f"🎯 **Meta Atualizada!** Você guardou R$ {valor:,.2f}. Progresso total: R$ {users_dict[user_email]['meta']['atual']:,.2f}", "grafico_tipo": "barras", "grafico_titulo": "Progresso da Meta", "grafico_dados": pd.DataFrame({"R$": [users_dict[user_email]['meta']['atual'], users_dict[user_email]['meta']['alvo']]}, index=["Guardado", "Meta"])}

    # GASTOS
    palavras_gasto = ["gastei", "paguei", "gasto"]
    if any(p in query for p in palavras_gasto):
        numeros = re.findall(r'\d+', query)
        valor = float(numeros[0]) if numeros else 0
        cat = "lazer" if "lazer" in query else "casa" if "casa" in query else "despesas"
        users_dict[user_email]["gastos_atuais"][cat] += valor
        salvar_usuarios(users_dict)
        insight = "\n\n🧠 *Insight:* Notei que seus gastos com lazer estão altos. Que tal segurar o próximo final de semana?" if cat == "lazer" else ""
        return {"texto": f"✅ **Registrado:** R$ {valor} em {cat}.{insight}", "grafico_tipo": "barras", "grafico_titulo": "Status Gastos", "grafico_dados": pd.DataFrame({"Gastos": user_data["gastos_atuais"]}, index=["Casa", "Lazer", "Despesas"])}

    return {"texto": "💼 **Diagnóstico:** Para escalar seu lucro, foque em reduzir custos fixos. Como posso te ajudar hoje?", "grafico_tipo": "barras", "grafico_titulo": "Projeção", "grafico_dados": pd.DataFrame({"Lucro": [1000, 2000, 3000]}, index=["Mês 1", "Mês 2", "Mês 3"])}

# --- FLUXO PRINCIPAL ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
users = carregar_usuarios()
ref_code = st.query_params.get("ref")

if not st.session_state.logged_in:
    # LOGIN / REGISTRO
    st.subheader("🔑 Acesse sua Conta")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in users and users[email]["senha"] == senha:
            st.session_state.logged_in = True
            st.session_state.current_user = email
            st.rerun()
    
    st.markdown("---")
    st.subheader("📝 Cadastre-se")
    nome_r = st.text_input("Nome")
    email_r = st.text_input("E-mail para cadastro")
    senha_r = st.text_input("Senha para cadastro", type="password")
    if st.button("Criar Conta"):
        if email_r not in users:
            codigo = f"NRX-{nome_r[:3].upper()}{len(users)}"
            users[email_r] = {"senha": senha_r, "nome": nome_r, "is_pro": False, "dias_pro_ganhos": 0, "amigos_indicados": 0, "codigo_indicacao": codigo, "limites": {"casa": 2000.0, "lazer": 500.0, "despesas": 1000.0}, "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}, "meta": {"titulo": "Reserva", "alvo": 5000.0, "atual": 0.0}}
            
            # Lógica de Indicação Viral
            if ref_code:
                for mail, data in users.items():
                    if data["codigo_indicacao"] == ref_code:
                        users[mail]["amigos_indicados"] += 1
                        users[mail]["dias_pro_ganhos"] += 7
                        st.toast(f"🎉 Você indicou alguém! Seu amigo ganhou bônus e você +7 dias PRO!")
            
            salvar_usuarios(users)
            st.success("Conta criada!")

else:
    # APP LOGADO
    user_email = st.session_state.current_user
    user_data = users[user_email]
    is_active_pro = user_data["is_pro"] or user_data.get("dias_pro_ganhos", 0) > 0
    
    st.sidebar.title(f"Olá, {user_data['nome']}")
    menu = st.sidebar.selectbox("Menu", ["⚡ Cérebro IA", "🎁 Indique e Ganhe", "🚪 Sair"])

    if menu == "⚡ Cérebro IA":
        st.header("⚡ Master IA")
        if not is_active_pro: st.warning("🔓 Você está no modo Grátis. Indique amigos para ganhar dias PRO!")
        
        prompt = st.chat_input("Digite: 'Resumo semanal', 'Gastei 100 com lazer' ou 'Guardar 50 na meta'")
        if prompt:
            res = processar_gasto_ou_pergunta(prompt, user_data, user_email, users)
            st.markdown(res["texto"])
            st.bar_chart(res["grafico_dados"])

    elif menu == "🎁 Indique e Ganhe":
        st.header("🎁 Indique e Ganhe")
        link = f"https://neurax-suite-bz6izlp5hikpysvm4oejvc.streamlit.app/?ref={user_data['codigo_indicacao']}"
        st.metric("Amigos Indicados", user_data["amigos_indicados"])
        st.metric("Dias PRO Conquistados", user_data["dias_pro_ganhos"])
        st.info(f"Seu link: {link}")
        st.write("Copie e mande para seus amigos. Cada um que entrar te dá 7 dias de acesso PRO!")

    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.rerun()
