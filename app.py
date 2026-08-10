import streamlit as st
import json
import os
import pandas as pd
import re
import requests

st.set_page_config(
    page_title="Neurax Master AI - Motor de Lucros", 
    page_icon="📈", 
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    h1, h2 { color: #1e293b; font-weight: 800; font-family: 'Inter', sans-serif; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    [data-testid="stSidebar"] { background-color: #0f172a; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "users_neural_final.json"

def carregar_usuarios():
    usuarios_padrao = {
        "leandrodesantana646@gmail.com": {
            "senha": "leandro1996", "nome": "Leandro (Dono)", "is_pro": True,
            "telefone": "5511999999999",
            "dias_pro_ganhos": 0, "amigos_indicados": 0, "codigo_indicacao": "LEANDRO99",
            "limites": {"casa": 1000.0, "lazer": 300.0, "despesas": 500.0},
            "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
            "meta": {"alvo": 10000.0, "atual": 0.0}
        }
    }
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return usuarios_padrao
    return usuarios_padrao

def salvar_usuarios(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=4)

# --- FUNÇÃO DE DISPARO DE WHATSAPP ---
def disparar_whatsapp(telefone, mensagem):
    # Exemplo de integração com API de WhatsApp (substitua pela URL e Token do seu Provedor: Twilio, Z-API, etc.)
    url_api = "https://api.seugatewaywhatsapp.com/send" # Substitua pelo endpoint real do provedor
    payload = {
        "phone": telefone,
        "message": mensagem
    }
    headers = {
        "Authorization": "Bearer SEU_TOKEN_AQUI",
        "Content-Type": "application/json"
    }
    try:
        # response = requests.post(url_api, json=payload, headers=headers)
        # return response.status_code == 200
        pass
    except Exception as e:
        print(f"Erro ao enviar WhatsApp: {e}")
    return True

# --- LÓGICA DE PROCESSAMENTO E GASTOS ---
def processar_consulta(query, user_data, user_email, users_dict):
    query = query.lower()
    
    # Registro de Gastos com Verificação de Limite
    palavras_gasto = ["gastei", "paguei", "gasto"]
    if any(p in query for p in palavras_gasto):
        numeros = re.findall(r'\d+', query)
        valor = float(numeros[0]) if numeros else 0
        cat = "lazer" if "lazer" in query else "casa" if "casa" in query else "despesas"
        
        users_dict[user_email]["gastos_atuais"][cat] += valor
        gasto_atual = users_dict[user_email]["gastos_atuais"][cat]
        limite_cat = users_dict[user_email]["limites"][cat]
        
        alerta_zap = ""
        # Verifica se ultrapassou o limite
        if gasto_atual > limite_cat:
            tel = user_data.get("telefone")
            if tel:
                msg = f"⚠️ ALERTA NEURAX: Você ultrapassou o limite da categoria '{cat.capitalize()}'. Gasto atual: R$ {gasto_atual:,.2f} / Limite: R$ {limite_cat:,.2f}."
                disparar_whatsapp(tel, msg)
                alerta_zap = "\n\n📱 *Aviso:* Um alerta de WhatsApp foi disparado para o seu número devido ao estouro de limite!"

        salvar_usuarios(users_dict)
        return {
            "texto": f"✅ **Registrado:** R$ {valor:,.2f} em {cat}. Total na categoria: R$ {gasto_atual:,.2f} (Limite: R$ {limite_cat:,.2f}).{alerta_zap}",
            "grafico": pd.DataFrame({"Gastos": users_dict[user_email]["gastos_atuais"]}, index=["Casa", "Lazer", "Despesas"])
        }

    return {"texto": "💼 **Diagnóstico:** Para escalar, foque em reduzir custos fixos. Como posso te ajudar hoje?", "grafico": None}

# --- FLUXO PRINCIPAL ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
users = carregar_usuarios()
ref_code = st.query_params.get("ref")

if not st.session_state.logged_in:
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", width=150)
    
    st.subheader("🔑 Acesse o Motor de Lucros")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in users and users[email]["senha"] == senha:
            st.session_state.logged_in = True
            st.session_state.current_user = email
            st.rerun()
            
    st.markdown("---")
    st.subheader("📝 Cadastre-se na Plataforma")
    nome_r = st.text_input("Nome Completo")
    email_r = st.text_input("E-mail para Cadastro")
    telefone_r = st.text_input("WhatsApp (com DDD, ex: 5511999999999)")
    senha_r = st.text_input("Senha de Acesso", type="password")
    
    if st.button("Criar Conta Gratuita"):
        if email_r not in users:
            codigo = f"NRX-{nome_r[:3].upper()}{len(users)}"
            users[email_r] = {
                "senha": senha_r, "nome": nome_r, "telefone": telefone_r, "is_pro": False, 
                "dias_pro_ganhos": 0, "amigos_indicados": 0, "codigo_indicacao": codigo,
                "limites": {"casa": 1000.0, "lazer": 300.0, "despesas": 500.0},
                "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
                "meta": {"alvo": 10000.0, "atual": 0.0}
            }
            if ref_code:
                for mail, data in users.items():
                    if data["codigo_indicacao"] == ref_code:
                        users[mail]["amigos_indicados"] += 1
                        users[mail]["dias_pro_ganhos"] += 7
            salvar_usuarios(users)
            st.success("Conta criada com sucesso! Faça login acima.")
        else:
            st.warning("Este e-mail já está cadastrado.")
else:
    user_email = st.session_state.current_user
    user_data = users[user_email]
    is_admin = (user_email == "leandrodesantana646@gmail.com")
    
    if os.path.exists("logo.png"):
        st.sidebar.image("logo.png", use_container_width=True)
    else:
        st.sidebar.markdown("### ⚡ NEURAX MASTER AI")
    
    st.sidebar.markdown(f"**Usuário:** {user_data['nome']}")
    
    menu = st.sidebar.selectbox("Menu", ["📊 Painel de Lucros", "⚡ Consultoria IA", "🎁 Indique e Ganhe", "🚪 Sair"] + (["👑 Admin"] if is_admin else []))

    if menu == "📊 Painel de Lucros":
        st.header("📈 Projeção de Crescimento Corporativo")
        col1, col2 = st.columns(2)
        col1.metric("Gasto Atual Registrado", f"R$ {sum(user_data['gastos_atuais'].values()):,.2f}")
        col2.metric("Meta de Lucro/Reserva", f"R$ {user_data['meta']['alvo']:,.2f}")

    elif menu == "⚡ Consultoria IA":
        st.header("⚡ Consultoria Estratégica de Negócios")
        prompt = st.chat_input("Ex: 'Gastei 400 com lazer' ou 'Como posso aumentar meu lucro?'")
        if prompt:
            res = processar_consulta(prompt, user_data, user_email, users)
            st.markdown(res["texto"])
            if res.get("grafico") is not None:
                st.bar_chart(res["grafico"])

    elif menu == "🎁 Indique e Ganhe":
        st.header("🎁 Programa de Embaixadores")
        link = f"https://neurax-suite.streamlit.app/?ref={user_data['codigo_indicacao']}"
        st.info(f"**Seu link exclusivo de indicação:**\n`{link}`")
        st.metric("Amigos Convertidos pelo seu Link", user_data["amigos_indicados"])

    elif menu == "👑 Admin":
        st.header("👑 Painel de Gestão e Controle")
        st.dataframe(pd.DataFrame(users).T)

    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.rerun()
