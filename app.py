import streamlit as st
from groq import Groq
import sqlite3
import hashlib
from datetime import datetime
import pandas as pd

# Estilização visual customizada (Tema NeuraX Pro & Ocultar Branding)
st.markdown("""
    <style>
    /* Oculta o cabeçalho superior (Remove o ícone do GitHub, Share e Menu) */
    header {visibility: hidden;}
    
    /* Oculta o rodapé padrão ("Made with Streamlit") */
    footer {visibility: hidden;}
    
    /* Ajuste de fontes e cores principais */
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Customização dos botões principais */
    .stButton>button {
        background: linear-gradient(90deg, #1f6feb 0%, #388bfd 100%);
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #388bfd 0%, #58a6ff 100%);
        color: #ffffff;
    }
    
    /* Estilização dos blocos de expansão */
    .streamlit-expanderHeader {
        background-color: #161b22;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Funções de Criptografia e Banco de Dados SQLite
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed_text):
    if make_hash(password) == hashed_text:
        return True
    return False

def init_db():
    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            tool_name TEXT,
            content TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def add_user(username, password):
    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users(username, password) VALUES (?, ?)', (username, make_hash(password)))
    conn.commit()
    conn.close()

def login_user(username, password):
    # 🔑 CHAVE MESTRA DE SEGURANÇA
    if username.strip().lower() == "admin" and password.strip().lower() == "admin":
        return True

    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    data = cursor.fetchall()
    conn.close()
    if data:
        if check_hash(password, data[0][0]):
            return True
    return False

def save_history(username, tool_name, content):
    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor.execute('INSERT INTO history (username, tool_name, content, timestamp) VALUES (?, ?, ?, ?)', 
                   (username, tool_name, content, timestamp))
    conn.commit()
    conn.close()

def get_history(username):
    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT tool_name, content, timestamp FROM history WHERE username = ? ORDER BY id DESC', (username,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_users():
    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users')
    data = cursor.fetchall()
    conn.close()
    return [row[0] for row in data]

def get_all_history_admin():
    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT username, tool_name, timestamp FROM history ORDER BY id DESC')
    data = cursor.fetchall()
    conn.close()
    return data

# Gerenciamento de Sessão de Login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "generation_count" not in st.session_state:
    st.session_state["generation_count"] = 0

# Tela de Autenticação
if not st.session_state["logged_in"]:
    st.title("🚀 NeuraX Suite - Acesso ao Sistema")
    st.write("Faça login ou crie sua conta para acessar o ecossistema avançado de inteligência artificial.")
    
    auth_mode = st.selectbox("Escolha a opção", ["Login", "Cadastrar"])
    
    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")
    
    if auth_mode == "Login":
        if st.button("Entrar no Sistema"):
            if login_user(user, pwd):
                st.session_state["logged_in"] = True
                st.session_state["username"] = user
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos. Verifique os dados ou crie uma conta primeiro.")
    else:
        if st.button("Criar Conta"):
            if user and pwd:
                add_user(user, pwd)
                st.success("Cadastro realizado com sucesso! Alterne para a aba de Login.")
            else:
                st.warning("Preencha todos os campos.")

else:
    # Painel Principal
    st.sidebar.title("Painel NeuraX")
    st.sidebar.write(f"Logado como: **{st.session_state['username']}**")
    
    st.sidebar.markdown("---")
    st.sidebar.metric(label="Gerações nesta Sessão", value=st.session_state["generation_count"])
    st.sidebar.markdown("---")
    
    groq_api_key = st.sidebar.text_input("Insira sua Groq API Key", type="password")
    if not groq_api_key:
        try:
            groq_api_key = st.secrets["GROQ_API_KEY"]
        except:
            pass

    if not groq_api_key:
        st.warning("⚠️ Insira sua chave da API da Groq na barra lateral para liberar as ferramentas.")
        client = None
    else:
        try:
            client = Groq(api_key=groq_api_key)
        except Exception as e:
            st.error(f"Erro ao inicializar o cliente Groq: {e}")
            client = None

    # MENU PADRÃO (Para os usuários comuns) com a NOVA FERRAMENTA INOVADORA
    menu_options = [
        "🗺️ Arquiteto de Funis de Vendas",
        "💰 Precificação Inteligente",
        "💬 Gerador de Copy WhatsApp",
        "📸 Planejador Instagram",
        "✉️ Gerador de E-mail Comercial",
        "🎬 Gerador de Roteiro para Vídeos",
        "📂 Meu Histórico"
    ]
    
    # =====================================================================
    # 🔒 SISTEMA DE SEGURANÇA PARA O PAINEL ADMINISTRATIVO
    # =====================================================================
    usuario_logado = st.session_state["username"].strip().lower()
    
    if usuario_logado == "admin":
        menu_options.insert(0, "🛠️ Painel Administrativo")
    # =====================================================================

    escolha = st.sidebar.selectbox("Navegue pelas Ferramentas", menu_options)
    
    if st.sidebar.button("Sair da Conta"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    # CONTEÚDO DO PAINEL ADMINISTRATIVO
    if escolha == "🛠️ Painel Administrativo":
        st.header("🛠️ Painel Administrativo - NeuraX Suite")
        st.success("Acesso Master Confirmado!")
        st.write("Área restrita para monitoramento global do sistema e métricas de engajamento.")
        
        all_users = get_all_users()
        all_history = get_all_history_admin()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Usuários Cadastrados", len(all_users))
        with col2:
            st.metric("Total de Gerações na Plataforma", len(all_history))
            
        st.markdown("---")
        st.markdown("### 👥 Usuários Registrados")
        st.write(all_users)
        
        st.markdown("### 📊 Histórico Geral de Atividades")
        if all_history:
            df_history = pd.DataFrame(all_history, columns=["Usuário", "Ferramenta Utilizada", "Data e Hora"])
            st.dataframe(df_history, use_container_width=True)
        else:
            st.info("Nenhuma atividade registrada na plataforma ainda.")

    elif escolha == "📂 Meu Histórico":
        st.header("📂 Histórico de Gerações")
        st.write("Consulte abaixo todas as análises, copies, funis e roteiros salvos.")
        
        user_history = get_history(st.session_state["username"])
        
        if not user_history:
            st.info("Você ainda não gerou nenhum conteúdo. Use as ferramentas ao lado para começar!")
        else:
            for idx, (tool, content, timestamp) in enumerate(user_history):
                with st.expander(f"🛠️ [{tool}] - {timestamp}"):
                    st.markdown(content)
                    st.download_button(
                        label=f"📥 Baixar (.txt)",
                        data=content,
                        file_name=f"hist_{idx}.txt",
                        mime="text/plain"
                    )

    # FERRAMENTAS DE IA
    elif client:
        model_name = "llama-3.3-70b-versatile"

        if escolha == "🗺️ Arquiteto de Funis de Vendas":
            st.header("🗺️ Arquiteto de Funis de Vendas Inteligente")
            st.write("Projete estratégias comerciais completas combinadas com um diagrama visual interativo.")
            
            funil_produto = st.text_input("Qual é o seu produto ou serviço?")
            funil_ticket = st.selectbox("Qual é o nível de preço (Ticket)?", ["Baixo (Até R$ 100)", "Médio (R$ 100 - R$ 1.000)", "Alto (Acima de R$ 1.000)"])
            funil_publico = st.text_input("Quem é o seu público-alvo?")
            
            if st.button("Gerar Estratégia e Fluxograma"):
                if funil_produto and funil_publico:
                    with st.spinner("Desenhando a arquitetura do funil e o fluxograma visual..."):
                        prompt = f"""
                        Atue como um Estrategista de Marketing Digital sênior. 
                        Crie um funil de vendas estratégico completo para o produto: '{funil_produto}', com ticket '{funil_ticket}', voltado para o público: '{funil_publico}'.
                        Sua resposta deve conter obrigatoriamente:
                        1. A estratégia detalhada por etapas (Tráfego/Atração, Página de Captura/Conversão, Oferta/Checkout, Recuperação/Upsell).
                        2. Um diagrama de fluxo utilizando a sintaxe nativa do Mermaid (começando obrigatoriamente com um bloco de código ```mermaid e terminando com ```) para que o Streamlit possa renderizar o fluxograma visual do funil passo a passo.
                        """
                        completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                        resultado = completion.choices[0].message.content
                        st.session_state["generation_count"] += 1
                        save_history(st.session_state["username"], "Arquiteto de Funis", resultado)
                        st.success("Arquitetura e Fluxograma gerados com sucesso!")
                        st.markdown(resultado)

        elif escolha == "💰 Precificação Inteligente":
            st.header("💰 Calculadora de Precificação Inteligente com IA")
            produto = st.text_input("Nome do Produto ou Serviço")
            custo = st.number_input("Custo (R$)", min_value=0.0, format="%.2f")
            margem = st.slider("Margem de Lucro (%)", min_value=10, max_value=500, value=100)
            
            if st.button("Calcular Preço Ideal"):
                if produto and custo > 0:
                    with st.spinner("Analisando..."):
                        prompt = f"Analise a precificação de: {produto} com custo R${custo} e margem de {margem}%."
                        completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                        resultado = completion.choices[0].message.content
                        st.session_state["generation_count"] += 1
                        save_history(st.session_state["username"], "Precificação Inteligente", resultado)
                        st.success("Análise concluída!")
                        st.markdown(resultado)

        elif escolha == "💬 Gerador de Copy WhatsApp":
            st.header("💬 Gerador de Copy para WhatsApp")
            nicho = st.text_input("Seu nicho/produto")
            publico = st.text_input("Público-alvo")
            oferta = st.text_area("Oferta")
            
            if st.button("Gerar Copy"):
                if nicho and oferta:
                    with st.spinner("Criando..."):
                        prompt = f"Crie copy de vendas para WhatsApp. Nicho: {nicho}, Público: {publico}, Oferta: {oferta}."
                        completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                        resultado = completion.choices[0].message.content
                        st.session_state["generation_count"] += 1
                        save_history(st.session_state["username"], "Copy WhatsApp", resultado)
                        st.success("Gerado!")
                        st.markdown(resultado)

        elif escolha == "📸 Planejador Instagram":
            st.header("📸 Planejador Instagram")
            tema = st.text_input("Tema central")
            qtd_dias = st.slider("Dias", 3, 7, 5)
            
            if st.button("Planejar Conteúdo"):
                if tema:
                    with st.spinner("Planejando..."):
                        prompt = f"Planeje conteúdo para Instagram por {qtd_dias} dias sobre: {tema}."
                        completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                        resultado = completion.choices[0].message.content
                        st.session_state["generation_count"] += 1
                        save_history(st.session_state["username"], "Planejador Instagram", resultado)
                        st.success("Planejado!")
                        st.markdown(resultado)

        elif escolha == "✉️ Gerador de E-mail Comercial":
            st.header("✉️ Gerador de E-mail Comercial")
            objetivo_email = st.selectbox("Objetivo", ["Prospecção", "Follow-up", "Proposta", "Recuperação"])
            cliente_alvo = st.text_input("Para quem?")
            detalhes_produto = st.text_area("O que vende?")
            
            if st.button("Gerar E-mail"):
                if detalhes_produto:
                    with st.spinner("Redigindo..."):
                        prompt = f"Escreva e-mail de {objetivo_email} para {cliente_alvo} vendendo {detalhes_produto}."
                        completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                        resultado = completion.choices[0].message.content
                        st.session_state["generation_count"] += 1
                        save_history(st.session_state["username"], "E-mail Comercial", resultado)
                        st.success("E-mail gerado!")
                        st.markdown(resultado)

        elif escolha == "🎬 Gerador de Roteiro para Vídeos":
            st.header("🎬 Gerador de Roteiro para Vídeos")
            tema_video = st.text_input("Tema principal")
            formato_video = st.selectbox("Formato", ["Reels/TikTok", "YouTube"])
            tom = st.selectbox("Tom", ["Dinâmico", "Educativo", "Polêmico", "Divertido"])
            
            if st.button("Gerar Roteiro"):
                if tema_video:
                    with st.spinner("Escrevendo..."):
                        prompt = f"Crie roteiro para {formato_video} sobre {tema_video} em tom {tom}."
                        completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                        resultado = completion.choices[0].message.content
                        st.session_state["generation_count"] += 1
                        save_history(st.session_state["username"], "Roteiro para Vídeos", resultado)
                        st.success("Roteiro pronto!")
                        st.markdown(resultado)
