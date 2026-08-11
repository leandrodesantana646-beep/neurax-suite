import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import datetime
import os
import urllib.parse

# Configuração da página
st.set_page_config(
    page_title="Neurax Master AI", 
    page_icon="⚡", 
    layout="wide"
)

# Estilização Avançada e Moderna (UI/UX de Alto Padrão)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main { 
        background-color: #f8fafc; 
    }
    
    h1, h2, h3 { 
        color: #0f172a; 
        font-weight: 800; 
        letter-spacing: -0.025em; 
    }
    
    .stMetric { 
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); 
        padding: 20px; 
        border-radius: 14px; 
        border: 1px solid #e2e8f0; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02); 
    }
    
    [data-testid="stSidebar"] { 
        background-color: #0f172a; 
        color: #ffffff; 
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #94a3b8;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
        transform: translateY(-1px);
    }
    
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS SQLITE ---
def init_db():
    conn = sqlite3.connect("neurax.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (email TEXT PRIMARY KEY, senha TEXT, nome TEXT, is_pro INTEGER, 
                  casa REAL, lazer REAL, despesas REAL, meta REAL)''')
    conn.commit()
    # Criar admin padrão se não existir
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,1,0,0,0,10000)", 
              ("leandrodesantana646@gmail.com", "leandro1996", "Leandro (Dono)"))
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

# --- ESTADO E RETORNO DE PAGAMENTO ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

query_params = st.query_params
status_pagamento = query_params.get("status") or query_params.get("collection_status")
if status_pagamento in ["sucesso", "approved"] and st.session_state.get('logged_in'):
    user_email = st.session_state.get('user')
    if user_email:
        update_user(user_email, "is_pro", 1)
        st.balloons()
        st.success("🎉 Pagamento confirmado! Seu acesso PRO foi liberado automaticamente.")

# --- TELA DE AUTENTICAÇÃO UNIFICADA ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown("""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #0f172a, #1e293b); border-radius: 16px; color: white; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: #38bdf8; font-size: 24px;">⚡ NEURAX</h2>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: #94a3b8;">MASTER AI</p>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>🔑 Acesso ao Sistema</h2>", unsafe_allow_html=True)
        
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
                else: 
                    st.error("E-mail ou senha incorretos.")
        
        with tab_cadastro:
            nome = st.text_input("Nome Completo", key="cad_nome")
            n_email = st.text_input("E-mail para cadastro", key="cad_email")
            n_senha = st.text_input("Crie uma senha", type="password", key="cad_senha")
            if st.button("Criar Conta", use_container_width=True):
                if add_user(n_email, n_senha, nome):
                    st.success("Conta criada com sucesso! Vá para a aba 'Entrar'.")
                else: 
                    st.error("Erro: E-mail já cadastrado.")
                
        with tab_recuperar:
            st.info("Esqueceu sua senha? Entre em contato com o suporte para redefinição manual.")
            st.link_button("Falar com Suporte (WhatsApp)", "https://wa.me/5511999999999", use_container_width=True)

else:
    # --- FLUXO PRINCIPAL LOGADO ---
    user_email = st.session_state.user
    user_data = get_user(user_email)
    
    # UI Lateral
    if os.path.exists("logo.png"): 
        st.sidebar.image("logo.png", use_container_width=True)
    else: 
        st.sidebar.markdown("<h2 style='color: #38bdf8; text-align: center;'>⚡ NEURAX AI</h2>", unsafe_allow_html=True)
    
    st.sidebar.markdown(f"**Usuário:** {user_data['nome']}")
    
    menu = st.sidebar.selectbox("Menu Principal", ["📊 Dashboard", "👑 Assinar Pro", "🚪 Sair"])
    
    # PAINEL ADMIN
    if user_email == "leandrodesantana646@gmail.com":
        if st.sidebar.checkbox("Painel Admin"):
            st.sidebar.subheader("👑 Aprovação PRO")
            df_users = get_all_users()
            for idx, row in df_users.iterrows():
                if not row['is_pro']:
                    if st.sidebar.button(f"Liberar: {row['nome']}", key=f"lib_{row['email']}"):
                        update_user(row['email'], "is_pro", 1)
                        st.success(f"Usuário {row['nome']} liberado com sucesso!")
                        st.rerun()

    # Cabeçalho Principal Moderno
    if os.path.exists("logo.png"):
        hc1, hc2 = st.columns([1, 12])
        with hc1:
            st.image("logo.png", width=45)
        with hc2:
            st.markdown("## Neurax Master AI")
    else:
        st.markdown("## ⚡ Neurax Master AI")
    st.markdown("---")

    # PÁGINAS DO APP
    if menu == "📊 Dashboard":
        st.header("📈 Visão Financeira Corporativa")
        
        # Gráfico Plotly
        gastos = {"Casa": user_data['casa'], "Lazer": user_data['lazer'], "Despesas": user_data['despesas']}
        df_gastos = pd.DataFrame(list(gastos.items()), columns=['Categoria', 'Valor'])
        fig = px.pie(df_gastos, values='Valor', names='Categoria', hole=0.4, title="Distribuição de Gastos por Categoria")
        st.plotly_chart(fig, use_container_width=True)
        
        # Limites definidos por categoria
        limites = {"Casa": 1000.0, "Lazer": 300.0, "Despesas": 500.0}
        
        st.subheader("Registrar Novo Gasto")
        cat = st.selectbox("Categoria", ["Casa", "Lazer", "Despesas"])
        valor = st.number_input("Valor do Gasto", min_value=0.0)
        
        if st.button("Registrar Gasto", use_container_width=True):
            cat_key = cat.lower()
            novo_total = user_data[cat_key] + valor
            update_user(user_email, cat_key, novo_total)
            
            limite_maximo = limites.get(cat, 1000.0)
            
            if novo_total > limite_maximo:
                st.toast("🚨 Alerta: Limite de gastos ultrapassado!", icon="⚠️")
                st.error(f"ATENÇÃO: O limite da categoria **{cat}** foi estourado!")
                st.warning(f"Seu limite era R$ {limite_maximo:,.2f}, mas com este lançamento o total foi para **R$ {novo_total:,.2f}**.")
                
                texto_aviso = f"⚠️ Alerta Neurax: Meus gastos na categoria *{cat}* ultrapassaram o limite planejado. Atual: R$ {novo_total:,.2f} (Limite: R$ {limite_maximo:,.2f})."
                link_wpp = f"https://wa.me/5511999999999?text={urllib.parse.quote(texto_aviso)}"
                st.link_button("📲 Enviar Alerta via WhatsApp", link_wpp, use_container_width=True)
            else:
                st.toast("Gasto registrado com sucesso!", icon="✅")
                st.success("✅ Gasto registrado dentro do orçamento planejado!")
                st.rerun()

    elif menu == "👑 Assinar Pro":
        st.header("👑 Desbloqueie o Potencial Máximo")
        st.markdown("""
        - 🤖 **Consultoria IA Ilimitada** para otimizar seu negócio.
        - 📈 **Projeções de Crescimento** e relatórios avançados.
        - 🚀 **Suporte Prioritário** via plataforma.
        
        **Valor:** R$ 49,99 / mês
        """)
        st.link_button("Assinar R$ 49,99/mês (PIX / Cartão Automático)", "https://mpago.la/2WjVnvA", use_container_width=True)
        st.info("💡 Após concluir o pagamento, você retornará ao app e seu acesso PRO será liberado instantaneamente de forma automática.")

    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.rerun()
