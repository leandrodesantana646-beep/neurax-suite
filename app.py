import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import urllib.parse
import time
import random

# Configuração da página
st.set_page_config(
    page_title="Neurax IA", 
    page_icon="⚡", 
    layout="wide"
)

# Estilização Avançada e Moderna
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main { background-color: #f8fafc; }
    
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
    
    /* Menu Lateral */
    [data-testid="stSidebar"] { 
        background-color: #0d1322; 
        color: #ffffff; 
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] .stMarkdown { color: #94a3b8; }
    
    /* Botões */
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
    
    /* Barras de digitação com borda azul e texto azul */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #3b82f6 !important;
        background-color: #ffffff !important;
        color: #2563eb !important;
        padding: 10px;
        font-weight: 600;
    }
    
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        color: #2563eb !important;
        border-color: #1d4ed8 !important;
    }
    
    .stTextInput>div>div>input::placeholder { color: #94a3b8 !important; font-weight: 400; }
    
    /* Card Destacado */
    .highlight-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        margin: 15px 0;
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

# --- FUNÇÕES SIMULADAS DE IA ---
def gerar_consultoria_ia(nicho, produto):
    # Simula uma chamada de API para o Gemini/OpenAI
    return f"""
    **Análise de Mercado Neurax IA:** O nicho de **{nicho}** está em expansão, mas a maioria dos concorrentes foca apenas em preço baixo. 
    O seu produto, **{produto}**, tem potencial para se destacar se você focar na 'experiência do cliente'. 
    Sugiro criar pacotes ou combos, melhorando a apresentação visual. Isso justifica a margem alta e atrai um público que não chora por desconto.
    """

def gerar_copy_vendas(produto):
    return f"""
    🔥 **Script para WhatsApp:** 
    "Olá! Vi que você se interessou pelo nosso {produto}. Diferente do que tem no mercado, o nosso é focado em [Benefício Principal]. Tenho apenas mais 2 unidades com uma condição especial hoje. Posso reservar o seu?"
    
    📸 **Copy para Instagram:**
    "Cansado de [Problema comum do nicho]? 😩 Nós também estávamos. Por isso desenvolvemos o {produto}. Com ele, você não apenas resolve isso, mas também ganha [Benefício extra]. Clique no link da bio e garanta antes que o estoque zere! 🚀"
    """

# --- TELA DE AUTENTICAÇÃO ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #0f172a, #1e293b); border-radius: 16px; color: white; margin-bottom: 20px;">
                <h2 style="margin: 0; color: #38bdf8; font-size: 24px;">⚡ NEURAX IA</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>🔑 Acesso ao Sistema</h2>", unsafe_allow_html=True)
        
        tab_login, tab_cadastro = st.tabs(["🔑 Entrar", "📝 Cadastrar"])
        
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
            n_email = st.text_input("E-mail", key="cad_email")
            n_senha = st.text_input("Senha", type="password", key="cad_senha")
            if st.button("Criar Conta", use_container_width=True):
                if add_user(n_email, n_senha, nome):
                    st.success("Conta criada! Vá para a aba 'Entrar'.")
                else: 
                    st.error("Erro: E-mail já cadastrado.")

else:
    # --- FLUXO PRINCIPAL LOGADO ---
    user_email = st.session_state.user
    user_data = get_user(user_email)
    
    st.sidebar.markdown("<h2 style='color: #38bdf8; text-align: center;'>⚡ NEURAX IA</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**Usuário:** {user_data['nome']}")
    
    menu = st.sidebar.selectbox("Menu Principal", ["📊 Dashboard", "🚀 IA & Escalador de Lucro", "👑 Assinar Pro", "🚪 Sair"])
    
    st.markdown("## ⚡ NEURAX IA")
    st.markdown("---")

    if menu == "📊 Dashboard":
        st.header("📈 Controle de Caixa")
        # (Código original do dashboard mantido enxuto para focar na nova IA)
        gastos = {"Casa": user_data['casa'], "Lazer": user_data['lazer'], "Despesas": user_data['despesas']}
        df_gastos = pd.DataFrame(list(gastos.items()), columns=['Categoria', 'Valor'])
        fig = px.pie(df_gastos, values='Valor', names='Categoria', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "🚀 IA & Escalador de Lucro":
        st.header("🧠 Neurax IA: Máquina de Vendas & Lucro")
        st.markdown("Descubra seu posicionamento, corte custos inúteis, crie copies que vendem e simule o retorno dos seus anúncios antes mesmo de gastar 1 real.")
        
        col_inp1, col_inp2, col_inp3 = st.columns([2, 2, 1.5])
        with col_inp1:
            nicho_input = st.text_input("Nicho (Ex: Roupas, Consultoria):", key="nicho")
        with col_inp2:
            produto_input = st.text_input("Produto/Serviço Principal:", key="produto")
        with col_inp3:
            custo_unitario = st.number_input("Custo de Produção (R$):", min_value=1.0, value=30.0, step=5.0)
            
        margem_desejada = st.select_slider(
            "Margem de Lucro desejada:",
            options=[100, 150, 200, 300, 400, 500],
            value=200,
            format_func=lambda x: f"{x}%"
        )
        
        if st.button("⚡ Executar Inteligência Total", use_container_width=True):
            if not nicho_input or not produto_input:
                st.warning("Preencha o Nicho e o Produto para a IA funcionar.")
            else:
                with st.spinner('A IA está analisando o mercado, precificando e criando a estratégia...'):
                    time.sleep(2) # Simula o delay de uma API de IA
                
                preco_sugerido = custo_unitario * (1 + (margem_desejada / 100))
                lucro_bruto_unitario = preco_sugerido - custo_unitario
                
                # --- 1. CONSULTORIA DA IA ---
                st.markdown("### 🤖 1. Consultoria Estratégica IA")
                st.markdown(f"<div class='highlight-card'>{gerar_consultoria_ia(nicho_input, produto_input)}</div>", unsafe_allow_html=True)
                
                # --- 2. RAIO-X DE CUSTOS (EFEITO CHOQUE) ---
                st.markdown("### 🔪 2. Raio-X de Custos: Por que você vai lucrar mais?")
                df_corte = pd.DataFrame({
                    "Profissional/Serviço": ["Gestor de Tráfego", "Social Media (Posts)", "Atendimento/Vendedor", "Softwares Soltos"],
                    "Modelo Antigo (Mensal)": ["R$ 1.500", "R$ 1.200", "R$ 1.800", "R$ 350"],
                    "Com Neurax IA": ["R$ 0 (Você faz)", "R$ 0 (IA Gera)", "R$ 0 (Automação)", "R$ 0 (Tudo em 1)"]
                })
                st.table(df_corte)
                st.success("💰 **Economia Imediata Mensal: R$ 4.850,00.** Dinheiro que vai direto para o seu lucro líquido.")
                
                # --- 3. MÁQUINA DE VENDAS ---
                st.markdown("### 📢 3. Sua Máquina de Vendas Pronta")
                with st.expander("Ver Scripts de Vendas (WhatsApp e Instagram)"):
                    st.write(gerar_copy_vendas(produto_input))
                
                # --- 4. SIMULADOR DE TRÁFEGO ---
                st.markdown("### 🎯 4. Simulador de Tráfego Pago (ROI Seguro)")
                st.info("Vamos simular quanto de lucro você tem se colocar dinheiro no Facebook/Google Ads hoje.")
                
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    verba_ads = st.number_input("Verba para Anúncios Hoje (R$):", value=50.0)
                with col_t2:
                    conversao_estimada = st.slider("Taxa de Conversão Esperada (%)", 1, 10, 2)
                
                cpc_estimado = 1.20 # Custo por clique fictício
                cliques = int(verba_ads / cpc_estimado)
                vendas_ads = int(cliques * (conversao_estimada / 100))
                
                if vendas_ads == 0: vendas_ads = 1 # Garante pelo menos 1 para não frustrar o simulador
                
                faturamento_ads = vendas_ads * preco_sugerido
                lucro_ads = faturamento_ads - (vendas_ads * custo_unitario) - verba_ads
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Pessoas no site", cliques)
                m2.metric("Vendas Feitas", vendas_ads)
                m3.metric("Faturamento", f"R$ {faturamento_ads:,.2f}")
                m4.metric("Seu Lucro Limpo", f"R$ {lucro_ads:,.2f}", f"{margem_desejada}% de Margem")
                
        # --- 5. ROTA ANTI-FALÊNCIA GAMIFICADA ---
        st.markdown("---")
        st.markdown("### 🛡️ 5. Checklist Anti-Falência")
        st.write("Marque as caixinhas conforme você aplica as estratégias no seu negócio. Blinde sua empresa contra a quebra!")
        
        c1 = st.checkbox("Cortei custos fixos desnecessários com a tabela do Raio-X.")
        c2 = st.checkbox("Ajustei o preço do meu produto com a margem recomendada.")
        c3 = st.checkbox("Copiei os scripts de vendas gerados pela IA.")
        c4 = st.checkbox("Fiz minha primeira simulação de tráfego pago sem medo.")
        
        if c1 and c2 and c3 and c4:
            st.balloons()
            st.success("🏆 PARABÉNS! Você garantiu o Selo de Negócio Blindado. Sua mentalidade agora é de um empresário focado em escala e lucro extremo!")

    elif menu == "👑 Assinar Pro":
        st.header("👑 Assinatura PRO")
        st.markdown("Acesse a IA sem limites e tenha a plataforma completa.")
        st.link_button("Assinar por R$ 49,99/mês", "https://mpago.la/2WjVnvA")

    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.rerun()
