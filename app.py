import streamlit as st
import json
import os
import datetime
import pandas as pd
import re

# Configuração da página
st.set_page_config(page_title="Neurax Master AI", page_icon="📈", layout="wide")

# Estilização
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    h1, h2 { color: #1e293b; font-weight: 800; font-family: 'Inter', sans-serif; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    [data-testid="stSidebar"] { background-color: #0f172a; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "users_neural_final.json"
mes_atual = datetime.datetime.now().strftime("%m/%Y")

# Funções auxiliares
def carregar_usuarios():
    usuarios_padrao = {
        "leandrodesantana646@gmail.com": {
            "senha": "leandro1996", "nome": "Leandro (Dono)", "is_pro": True,
            "dias_pro_ganhos": 0, "amigos_indicados": 0, "codigo_indicacao": "LEANDRO99",
            "ultimo_mes": mes_atual, "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
            "meta": {"alvo": 10000.0}
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

def verificar_acesso_pro(user_data):
    return user_data.get("is_pro", False) or user_data.get("dias_pro_ganhos", 0) > 0

def processar_consulta(query, user_email, users_dict):
    query = query.lower()
    if any(p in query for p in ["gastei", "paguei", "gasto"]):
        numeros = re.findall(r'\d+', query)
        valor = float(numeros[0]) if numeros else 0
        cat = "lazer" if "lazer" in query else "casa" if "casa" in query else "despesas"
        users_dict[user_email]["gastos_atuais"][cat] += valor
        salvar_usuarios(users_dict)
        return f"✅ **Registrado:** R$ {valor:,.2f} em {cat}."
    return "💼 **Diagnóstico:** Para escalar, foque em reduzir custos fixos. Como posso te ajudar hoje?"

# --- FLUXO PRINCIPAL ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
users = carregar_usuarios()
ref_code = st.query_params.get("ref")

if not st.session_state.logged_in:
    col_l1, col_l2 = st.columns([1, 4])
    with col_l1:
        if os.path.exists("logo.png"): st.image("logo.png", width=100)
    with col_l2:
        st.subheader("🔑 Acesse o Motor de Lucros")
        
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if email in users and users[email]["senha"] == senha:
            st.session_state.logged_in = True
            st.session_state.current_user = email
            st.rerun()
        else: st.error("E-mail ou senha incorretos.")
            
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
                "ultimo_mes": mes_atual,
                "limites": {"casa": 1000.0, "lazer": 300.0, "despesas": 500.0},
                "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
                "meta": {"alvo": 10000.0}
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
    
    # Reset automático de mês
    if user_data.get("ultimo_mes") != mes_atual:
        user_data["gastos_atuais"] = {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}
        user_data["ultimo_mes"] = mes_atual
        salvar_usuarios(users)
        st.toast("📅 Novo mês detectado! Seus gastos foram zerados automaticamente.")

    is_admin = (user_email == "leandrodesantana646@gmail.com")

    # UI Lateral
    if os.path.exists("logo.png"): st.sidebar.image("logo.png", use_container_width=True)
    else: st.sidebar.markdown("### ⚡ NEURAX MASTER AI")
    
    st.sidebar.markdown(f"**Usuário:** {user_data['nome']}")
    
    menu_options = ["📊 Painel de Lucros", "⚡ Consultoria IA", "🎁 Indique e Ganhe"]
    if not verificar_acesso_pro(user_data): menu_options.append("👑 Assinar Plano Pro")
    menu_options.append("🚪 Sair")
    if is_admin: menu_options.append("👑 Admin")
    
    menu = st.sidebar.selectbox("Menu", menu_options)

    # Cabeçalho Principal
    header_c1, header_c2 = st.columns([1, 10])
    with header_c1:
        if os.path.exists("logo.png"): st.image("logo.png", width=50)
    with header_c2: st.markdown("## Neurax Master AI")

    # Páginas
    if menu == "📊 Painel de Lucros":
        st.header("📈 Projeção de Crescimento Corporativo")
        col1, col2 = st.columns(2)
        col1.metric("Gasto Atual Registrado", f"R$ {sum(user_data['gastos_atuais'].values()):,.2f}")
        col2.metric("Meta de Lucro/Reserva", f"R$ {user_data['meta']['alvo']:,.2f}")

    elif menu == "⚡ Consultoria IA":
        st.header("⚡ Consultoria Estratégica de Negócios")
        if verificar_acesso_pro(user_data):
            prompt = st.chat_input("Ex: 'Gastei 400 com lazer' ou 'Como posso aumentar meu lucro?'")
            if prompt:
                res_texto = processar_consulta(prompt, user_email, users)
                st.markdown(res_texto)
        else:
            st.warning("🔒 Esta funcionalidade é exclusiva para membros **PRO**.")
            st.info("Assine o plano Pro no menu ao lado para desbloquear análises completas.")

    elif menu == "👑 Assinar Plano Pro":
        st.header("👑 Desbloqueie o Potencial Máximo")
        st.markdown("""
        - 🤖 **Consultoria IA Ilimitada** para otimizar seu negócio.
        - 📈 **Projeções de Crescimento** e controle avançado.
        - 🚀 **Suporte Prioritário** via plataforma.
        
        **Valor:** R$ 49,99 / mês
        """)
        st.link_button("Assinar R$ 49,99/mês", "https://mpago.la/2WjVnvA")
        st.info("💡 Após a confirmação do pagamento, seu acesso Pro é liberado automaticamente pelo administrador.")

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
