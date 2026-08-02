import streamlit as st
from groq import Groq
import sqlite3
import hashlib
from datetime import datetime
import pandas as pd

# Configuração inicial da página
st.set_page_config(
    page_title="NeuraX Suite",
    page_icon="🚀",
    layout="wide"
)

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
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
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
        st.warning("⚠️ Insira sua chave da API da Groq na barra lateral para liberar as ferramentas de IA.")
        client = None
    else:
        try:
            client = Groq(api_key=groq_api_key)
        except Exception as e:
            st.error(f"Erro ao inicializar o cliente Groq: {e}")
            client = None

    # MONTANDO O MENU PADRÃO (Para os usuários comuns)
    menu_options = [
        "💰 Precificação Inteligente",
        "💬 Gerador de Copy WhatsApp",
        "📸 Planejador Instagram",
        "✉️ Gerador de E-mail Comercial",
        "🎬 Gerador de Roteiro para Vídeos",
        "📂 Meu Histórico"
    ]
    
    # =====================================================================
    # 🔒 SISTEMA DE SEGURANÇA: Só mostra o painel para o dono do sistema!
    # O sistema transforma tudo em minúsculo e tira espaços para não ter erro
    # =====================================================================
    
    USUARIO_DONO = "admin" # <-- SE O SEU LOGIN NÃO FOR ADMIN, ME AVISE PARA EU MUDAR AQUI!
    
    usuario_logado = st.session_state["username"].strip().lower()
    
    if usuario_logado == USUARIO_DONO or usuario_logado == "admin":
        menu_options.append("🛠️ Painel Administrativo")
    
    # =====================================================================

    escolha = st.sidebar.selectbox("Navegue pelas Ferramentas", menu_options)
    
    if st.sidebar.button("Sair da Conta"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    # LÓGICA DO PAINEL ADMINISTRATIVO
    if escolha == "🛠️ Painel Administrativo":
        st.header("🛠️ Painel Administrativo - NeuraX Suite")
        st.write("Área para monitoramento global do sistema e métricas de engajamento.")
        
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
        st.write("Consulte abaixo todas as análises, copies e roteiros salvos no seu perfil.")
        
        user_history = get_history(st.session_state["username"])
        
        if not user_history:
            st.info("Você ainda não gerou nenhum conteúdo nesta conta. Use as ferramentas ao lado para começar!")
        else:
            for idx, (tool, content, timestamp) in enumerate(user_history):
                with st.expander(f"🛠️ [{tool}] - {timestamp}"):
                    st.markdown(content)
                    st.download_button(
                        label=f"📥 Baixar este item (.txt)",
                        data=content,
                        file_name=f"historico_{idx}_{tool.lower().replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"dl_hist_{idx}"
                    )

    # LÓGICA DAS FERRAMENTAS DE IA
    elif client:
        model_name = "llama-3.3-70b-versatile"

        if escolha == "💰 Precificação Inteligente":
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
