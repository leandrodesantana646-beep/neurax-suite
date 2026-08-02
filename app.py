import streamlit as st
from groq import Groq
import sqlite3
import hashlib
from datetime import datetime
import pandas as pd

# Configuração inicial
st.set_page_config(page_title="NeuraX Suite", page_icon="🚀", layout="wide")

# Funções de Banco de Dados
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed_text):
    return make_hash(password) == hashed_text

def init_db():
    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT, tool_name TEXT, content TEXT, timestamp TEXT)''')
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
    if data and check_hash(password, data[0][0]):
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

# Sessão
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "generation_count" not in st.session_state:
    st.session_state["generation_count"] = 0

# Tela de Login
if not st.session_state["logged_in"]:
    st.title("🚀 NeuraX Suite - Acesso ao Sistema")
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
                st.error("Usuário ou senha incorretos.")
    else:
        if st.button("Criar Conta"):
            if user and pwd:
                add_user(user, pwd)
                st.success("Cadastro realizado! Mude para a aba de Login.")
            else:
                st.warning("Preencha todos os campos.")

# Painel Principal
else:
    # SE ISSO AQUI NÃO APARECER NA BARRA LATERAL, O SEU CÓDIGO NÃO ESTÁ SALVANDO!
    st.sidebar.title("🔥 Painel NeuraX Atualizado")
    st.sidebar.write(f"Logado como: **{st.session_state['username']}**")
    
    groq_api_key = st.sidebar.text_input("Insira sua Groq API Key", type="password")
    client = Groq(api_key=groq_api_key) if groq_api_key else None

    # Lista base de ferramentas
    menu_options = [
        "💰 Precificação Inteligente",
        "💬 Gerador de Copy WhatsApp",
        "📸 Planejador Instagram",
        "✉️ Gerador de E-mail Comercial",
        "🎬 Gerador de Roteiro para Vídeos",
        "📂 Meu Histórico"
    ]
    
    # Lógica de segurança para o Admin
    usuario_atual = st.session_state["username"].strip().lower()
    
    # Se o usuário for admin, o Painel Administrativo entra como a PRIMEIRA opção da lista
    if usuario_atual == "admin":
        menu_options.insert(0, "🛠️ Painel Administrativo")
    
    # Caixinha de seleção na barra lateral
    escolha = st.sidebar.selectbox("Navegue pelas Ferramentas", menu_options)
    
    if st.sidebar.button("Sair da Conta"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    # Conteúdo do Painel Admin
    if escolha == "🛠️ Painel Administrativo":
        st.header("🛠️ Painel Administrativo - NeuraX Suite")
        st.success("🎉 Parabéns! Você encontrou o Painel Administrativo com sucesso!")
        
        all_users = get_all_users()
        all_history = get_all_history_admin()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Usuários Cadastrados", len(all_users))
        with col2:
            st.metric("Total de Gerações na Plataforma", len(all_history))
            
        st.markdown("### 👥 Usuários Registrados")
        st.write(all_users)
        
        st.markdown("### 📊 Histórico Geral de Atividades")
        if all_history:
            df = pd.DataFrame(all_history, columns=["Usuário", "Ferramenta", "Data/Hora"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma atividade registrada.")

    # Resto das ferramentas resumidas para caber
    elif escolha == "📂 Meu Histórico":
        st.header("📂 Seu Histórico")
        hist = get_history(st.session_state["username"])
        if hist:
            for tool, content, time in hist:
                with st.expander(f"{tool} - {time}"):
                    st.write(content)
        else:
            st.info("Nenhum histórico encontrado.")
    
    elif client:
        if escolha == "💰 Precificação Inteligente":
             st.header("💰 Precificação")
             st.write("Insira os dados na barra lateral para gerar. (Recurso simplificado para o teste)")
        # As outras ferramentas funcionam exatamente igual, eu ocultei o resto aqui para o código ficar menor no seu teste de tela. 
        # Foque em ver se a opção "Painel Administrativo" aparece na caixinha!
