import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import urllib.parse
import time

# Configuração da página
st.set_page_config(
    page_title="Neurax IA - Sócio de Lucros", 
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
    
    [data-testid="stSidebar"] { 
        background-color: #0d1322; 
        color: #ffffff; 
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] .stMarkdown { color: #94a3b8; }
    
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
    
    .highlight-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        margin: 15px 0;
    }
    
    .paywall-box {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        color: white;
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3);
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS SQLITE ---
def init_db():
    conn = sqlite3.connect("neurax.db")
    c = conn.cursor()
    # Criando a tabela com a nova coluna testes_usados
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (email TEXT PRIMARY KEY, senha TEXT, nome TEXT, is_pro INTEGER, 
                  casa REAL, lazer REAL, despesas REAL, meta REAL, testes_usados INTEGER)''')
    
    # Atualizando o banco de dados antigo caso a coluna não exista
    try:
        c.execute("ALTER TABLE users ADD COLUMN testes_usados INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass # A coluna já existe
        
    conn.commit()
    c.execute("INSERT OR IGNORE INTO users (email, senha, nome, is_pro, casa, lazer, despesas, meta, testes_usados) VALUES (?,?,?,1,0,0,0,10000,0)", 
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
        # Inserindo usuário novo com 0 testes usados
        conn.execute("INSERT INTO users (email, senha, nome, is_pro, casa, lazer, despesas, meta, testes_usados) VALUES (?,?,?,0,0,0,0,10000,0)", (email, senha, nome))
        conn.commit()
        success = True
    except:
        success = False
    conn.close()
    return success

# --- FUNÇÕES DE IA ---
def gerar_consultoria_ia(nicho, produto):
    return f"""
    **Análise de Mercado Neurax IA:** O nicho de **{nicho}** está em franca expansão. A maioria dos concorrentes falha ao focar apenas em briga de preços. 
    Seu produto, **{produto}**, tem alto potencial se você criar uma oferta de 'alto valor percebido'. 
    Recomendação: Melhore a embalagem ou adicione um bônus digital (ex: um guia em PDF rápido). Isso justifica uma precificação premium e elimina os clientes que só pedem desconto.
    """

def gerar_copy_vendas(produto):
    return f"Olá! Vi que você se interessou pelo nosso {produto}. Diferente do que tem no mercado, o nosso é focado em qualidade extrema e durabilidade. Tenho apenas mais 2 unidades com uma condição especial hoje. Posso reservar o seu?"

def gerar_pitch_deck(nicho, produto, margem, faturamento):
    return f"""
    **1. O Problema:** O mercado de {nicho} está saturado de soluções amadoras e sem padrão de qualidade.
    **2. A Solução:** Criamos o(a) {produto}, unindo qualidade superior com uma experiência de compra premium.
    **3. Modelo de Negócio:** Operamos com uma margem de segurança agressiva de {margem}%, garantindo caixa livre para reinvestimento imediato.
    **4. Tração & Escala:** Com uma injeção de capital focada em tráfego pago, nossa projeção é escalar o faturamento rapidamente para R$ {faturamento:,.2f}/mês, mantendo o custo de aquisição (CAC) baixo.
    """

def gerar_relatorio_txt(nicho, produto, preco, lucro, custo, margem):
    texto = f"""========================================
RELATÓRIO EXECUTIVO - NEURAX IA
========================================
Nicho: {nicho}
Produto Principal: {produto}

-- PRECIFICAÇÃO PREDITIVA --
Custo Unitário: R$ {custo:.2f}
Margem de Lucro Alvo: {margem}%
Preço Final Sugerido: R$ {preco:.2f}
Lucro Líquido por Unidade: R$ {lucro:.2f}

-- ECONOMIA DE CUSTOS (RAIO-X) --
Tráfego, Social Media e Softwares: R$ 4.850,00 economizados usando a IA.

-- ROTA ANTI-FALÊNCIA --
1. Mantenha os custos fixos próximos de zero.
2. Não dispute preço, dispute valor.
3. Reinvista lucros em automação e tráfego.

Gerado por Neurax IA - O seu Sócio de Lucros
========================================"""
    return texto

# --- VERIFICAÇÃO AUTOMÁTICA DE PAGAMENTO ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

query_params = st.query_params
status_pagamento = query_params.get("status") or query_params.get("collection_status")
if status_pagamento in ["sucesso", "approved"] and st.session_state.get('logged_in'):
    user_email_pag = st.session_state.get('user')
    if user_email_pag:
        update_user(user_email_pag, "is_pro", 1)
        st.balloons()
        st.success("🎉 Pagamento confirmado! Seu acesso PRO ilimitado foi liberado automaticamente.")

# --- TELA DE AUTENTICAÇÃO ---
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
    
    # Exibe badge PRO na lateral
    if user_data['is_pro']:
        st.sidebar.markdown("🏅 **Status:** `PRO Ilimitado`")
    else:
        st.sidebar.markdown("🔓 **Status:** `Conta Gratuita`")
        
    menu = st.sidebar.selectbox("Menu Principal", ["📊 Dashboard Integrado", "🚀 IA & Escalador de Lucro", "👑 Assinar Pro", "🚪 Sair"])
    
    st.markdown("## ⚡ NEURAX IA")
    st.markdown("---")

    if menu == "📊 Dashboard Integrado":
        st.header("📈 Dashboard & Auditoria Financeira")
        
        gastos_totais = user_data['casa'] + user_data['lazer'] + user_data['despesas']
        
        st.markdown("### 🔍 Auditoria em Tempo Real")
        if gastos_totais > 1500:
            st.error(f"⚠️ **Alerta Preditivo:** Identificamos um vazamento financeiro. Seus custos chegaram a R$ {gastos_totais:,.2f}. Recomendamos travar os gastos de 'Lazer' imediatamente.")
        elif gastos_totais > 0:
            st.success(f"✅ **Saúde Financeira:** Seus custos estão em R$ {gastos_totais:,.2f}. O fluxo de caixa está otimizado e saudável.")
        else:
            st.info("💡 **Dica do Sócio:** Você ainda não registrou gastos. Mantenha os custos operacionais baixos para potencializar seu lucro máximo.")
            
        gastos = {"Casa": user_data['casa'], "Lazer": user_data['lazer'], "Despesas": user_data['despesas']}
        df_gastos = pd.DataFrame(list(gastos.items()), columns=['Categoria', 'Valor'])
        fig = px.pie(df_gastos, values='Valor', names='Categoria', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "🚀 IA & Escalador de Lucro":
        st.header("🧠 Neurax IA: Máquina de Vendas & Lucro")
        
        # --- LÓGICA DO PAYWALL (BLOQUEIO) ---
        if user_data['is_pro'] == 0 and user_data['testes_usados'] >= 1:
            st.markdown("""
            <div class="paywall-box">
                <h2 style='color: white; margin-bottom: 10px;'>🔒 Seu teste gratuito terminou!</h2>
                <p style='font-size: 18px; margin-bottom: 20px;'>Você já viu o poder do Neurax IA. Assine agora para liberar a Inteligência Artificial <b>ilimitada</b>, gerar scripts infinitos e ter acesso a todas as simulações de negócio.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.link_button("👑 Assinar R$ 49,99/mês e Desbloquear Agora", "https://mpago.la/2WjVnvA", use_container_width=True)
            st.warning("Após o pagamento, seu acesso será liberado automaticamente em segundos.")
            
        else:
            # Mostra a ferramenta se for PRO ou se ainda tiver o teste grátis (0 usos)
            if user_data['is_pro'] == 0:
                st.info("🎁 **Você tem 1 Teste Gratuito!** Aproveite para ver como a IA pode escalar seu negócio.")
            
            st.markdown("Descubra seu posicionamento, corte custos, gerencie demanda e tenha o controle total do mercado na palma da sua mão.")
            
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
                    # Registra o uso do teste se o usuário não for PRO
                    if user_data['is_pro'] == 0:
                        update_user(user_email, 'testes_usados', user_data['testes_usados'] + 1)
                        
                    # Efeito de Processamento Neural UI
                    status_text = st.empty()
                    progress_bar = st.progress(0)
                    passos = ["Iniciando redes neurais...", "Mapeando concorrência oculta...", "Calculando projeções de lucro extremo...", "Gerando relatórios e scripts executivos..."]
                    
                    for i, passo in enumerate(passos):
                        status_text.markdown(f"**🧠 {passo}**")
                        progress_bar.progress((i + 1) * 25)
                        time.sleep(0.7)
                    
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Cálculos
                    preco_sugerido = custo_unitario * (1 + (margem_desejada / 100))
                    lucro_bruto_unitario = preco_sugerido - custo_unitario
                    
                    # Botão de Download do PDF/TXT
                    relatorio = gerar_relatorio_txt(nicho_input, produto_input, preco_sugerido, lucro_bruto_unitario, custo_unitario, margem_desejada)
                    st.download_button(
                        label="📄 Baixar Relatório Executivo Completo",
                        data=relatorio,
                        file_name="Relatorio_Neurax_IA.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    st.markdown("---")
                    # --- 1. CONSULTORIA ---
                    st.markdown("### 🤖 1. Consultoria Estratégica IA")
                    st.markdown(f"<div class='highlight-card'>{gerar_consultoria_ia(nicho_input, produto_input)}</div>", unsafe_allow_html=True)
                    
                    # --- 2. RAIO-X DE CUSTOS ---
                    st.markdown("### 🔪 2. Raio-X de Custos: Por que você vai lucrar mais?")
                    df_corte = pd.DataFrame({
                        "Profissional/Serviço": ["Gestor de Tráfego", "Social Media", "Vendedor", "Softwares Soltos"],
                        "Modelo Antigo (Mensal)": ["R$ 1.500", "R$ 1.200", "R$ 1.800", "R$ 350"],
                        "Com Neurax IA": ["R$ 0", "R$ 0", "R$ 0", "R$ 0"]
                    })
                    st.table(df_corte)
                    st.success("💰 **Economia Imediata: R$ 4.850,00.** Dinheiro que vai direto para o seu bolso.")
                    
                    # --- 3. MÁQUINA DE VENDAS 1-CLICK ---
                    st.markdown("### 📢 3. Sua Máquina de Vendas (Envio 1-Clique)")
                    copy_pronta = gerar_copy_vendas(produto_input)
                    st.info(f"**Script Validado:**\n\n{copy_pronta}")
                    
                    link_whatsapp = f"https://wa.me/?text={urllib.parse.quote(copy_pronta)}"
                    st.link_button("📲 Abrir WhatsApp e Disparar para Cliente", link_whatsapp)
                    
                    # --- 4. SIMULADOR E GESTÃO PREDITIVA DE ESTOQUE ---
                    st.markdown("### 🎯 4. Simulador de Tráfego & Projeção de Demanda")
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        verba_ads = st.number_input("Verba para Anúncios Hoje (R$):", value=50.0)
                    with col_t2:
                        conversao_estimada = st.slider("Taxa de Conversão Esperada (%)", 1, 10, 2)
                    
                    cpc_estimado = 1.20
                    cliques = int(verba_ads / cpc_estimado)
                    vendas_ads = max(int(cliques * (conversao_estimada / 100)), 1)
                    
                    faturamento_ads = vendas_ads * preco_sugerido
                    lucro_ads = faturamento_ads - (vendas_ads * custo_unitario) - verba_ads
                    
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Vendas Feitas", vendas_ads)
                    m2.metric("Faturamento", f"R$ {faturamento_ads:,.2f}")
                    m3.metric("Lucro Limpo", f"R$ {lucro_ads:,.2f}")
                    
                    # Inteligência de Estoque
                    estoque_necessario = vendas_ads * 30 # Projeção para o mês
                    custo_estoque = estoque_necessario * custo_unitario
                    m4.metric("Estoque Mês", f"{estoque_necessario} unid.", f"R$ {custo_estoque:,.2f} Custo")
                    st.warning(f"📦 **Gestão Preditiva:** Se mantiver essa verba diária, você venderá cerca de {estoque_necessario} unidades por mês. Separe **R$ {custo_estoque:,.2f}** do caixa para garantir a recompra sem quebrar o giro.")
                    
                    # --- 5. PITCH DECK DE INVESTIDORES ---
                    st.markdown("### 💼 5. Pitch Deck Executivo (Captação de Investimento)")
                    with st.expander("Ver Apresentação Oficial Pronta"):
                        st.write(gerar_pitch_deck(nicho_input, produto_input, margem_desejada, faturamento_ads * 30))
                        st.info("💡 Copie este texto e cole nos seus slides para apresentar em rodadas de negócios ou captação de sócios.")
                        
                    if user_data['is_pro'] == 0:
                        st.error("🔒 Este foi o seu teste gratuito. Para realizar novas consultas, assine o plano PRO.")

    elif menu == "👑 Assinar Pro":
        st.header("👑 Assinatura PRO")
        st.markdown("Acesse a IA sem limites e tenha a plataforma completa.")
        st.link_button("Assinar por R$ 49,99/mês", "https://mpago.la/2WjVnvA")

    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.rerun()
