import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Neurax Master AI", page_icon="⚡", layout="wide")

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect("neurax.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (email TEXT PRIMARY KEY, senha TEXT, nome TEXT, is_pro INTEGER, 
                  casa REAL, lazer REAL, despesas REAL, meta REAL)''')
    conn.commit()
    conn.close()

init_db()

def get_user(email):
    conn = sqlite3.connect("neurax.db")
    df = pd.read_sql(f"SELECT * FROM users WHERE email = '{email}'", conn)
    conn.close()
    return df.iloc[0] if not df.empty else None

def update_user(email, col, val):
    conn = sqlite3.connect("neurax.db")
    conn.execute(f"UPDATE users SET {col} = ? WHERE email = ?", (val, email))
    conn.commit()
    conn.close()

def add_user(email, senha, nome):
    conn = sqlite3.connect("neurax.db")
    try:
        conn.execute("INSERT INTO users VALUES (?,?,?,0,0,0,0,10000)", (email, senha, nome))
        conn.commit()
        success = True
    except:
        success = False
    conn.close()
    return success

def get_all_users():
    conn = sqlite3.connect("neurax.db")
    df = pd.read_sql("SELECT * FROM users", conn)
    conn.close()
    return df

# --- INTERFACE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Centralização
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("⚡ Neurax Master AI")
        st.subheader("Login, Cadastro ou Recuperação")
        
        # A MÁGICA DAS ABAS AQUI
        tab_login, tab_cadastro, tab_recuperar = st.tabs(["🔑 Entrar", "📝 Cadastrar", "🔄 Recuperar"])
        
        with tab_login:
            email = st.text_input("E-mail", key="login_email")
            senha = st.text_input("Senha", type="password", key="login_senha")
            if st.button("Acessar Sistema", use_container_width=True):
                user = get_user(email)
                if user is not None and user['senha'] == senha:
                    st.session_state.logged_in = True
                    st.session_state.user = email
                    st.rerun()
                else: st.error("E-mail ou senha incorretos.")
        
        with tab_cadastro:
            nome = st.text_input("Nome Completo")
            n_email = st.text_input("E-mail para cadastro")
            n_senha = st.text_input("Crie uma senha", type="password")
            if st.button("Criar Conta", use_container_width=True):
                if add_user(n_email, n_senha, nome):
                    st.success("Conta criada! Pode logar na aba 'Entrar'.")
                else: st.error("Erro: E-mail já cadastrado.")
                
        with tab_recuperar:
            st.info("Esqueceu sua senha?")
            st.write("Para sua segurança, a redefinição é feita manualmente.")
            st.link_button("Falar com Suporte (WhatsApp)", "https://wa.me/55SEUNUMERO", use_container_width=True)

else:
    # USUÁRIO LOGADO
    user_data = get_user(st.session_state.user)
    st.sidebar.title(f"Olá, {user_data['nome']}")
    menu = st.sidebar.selectbox("Menu", ["📊 Dashboard", "👑 Assinar Pro", "🚪 Sair"])
    
    # ADMIN PANEL
    if st.session_state.user == "leandrodesantana646@gmail.com":
        if st.sidebar.checkbox("Painel Admin"):
            st.subheader("👑 Painel de Aprovação")
            df_users = get_all_users()
            for idx, row in df_users.iterrows():
                if not row['is_pro']:
                    if st.button(f"Liberar PRO: {row['nome']}"):
                        update_user(row['email'], "is_pro", 1)
                        st.rerun()

    if menu == "📊 Dashboard":
        st.header("📈 Visão Financeira")
        gastos = {"Casa": user_data['casa'], "Lazer": user_data['lazer'], "Despesas": user_data['despesas']}
        fig = px.pie(values=list(gastos.values()), names=list(gastos.keys()), hole=0.4, title="Distribuição de Gastos")
        st.plotly_chart(fig, use_container_width=True)
        
        # Registrar
        cat = st.selectbox("Categoria", ["Casa", "Lazer", "Despesas"])
        valor = st.number_input("Valor", min_value=0.0)
        if st.button("Registrar Gasto"):
            novo_total = user_data[cat.lower()] + valor
            update_user(st.session_state.user, cat.lower(), novo_total)
            st.rerun()

    elif menu == "👑 Assinar Pro":
        st.header("👑 Desbloqueie o Pro")
        st.code("Bea37c42-5f4e-4016-ad9f-6b4f326b6552")
        st.info("Pix copiado! Envie o comprovante para liberação.")

    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.rerun()
