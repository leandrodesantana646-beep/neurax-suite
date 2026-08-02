import streamlit as st
from google import genai
import sqlite3
import hashlib

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

# Gerenciamento de Sessão de Login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Tela de Autenticação
if not st.session_state["logged_in"]:
    st.title("🚀 NeuraX Suite - Acesso ao Sistema")
    st.write("Faça login ou crie sua conta para acessar o ecossistema de inteligência artificial.")
    
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
    # Painel Principal do SaaS
    st.sidebar.title(f"Painel NeuraX")
    st.sidebar.write(f"Logado como: **{st.session_state['username']}**")
    
    # Configuração da Chave da API do Google Gemini
    gemini_api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")
    if not gemini_api_key:
        try:
            gemini_api_key = st.secrets["GEMINI_API_KEY"]
        except:
            pass

    if not gemini_api_key:
        st.warning("⚠️ Insira sua chave da API do Google Gemini na barra lateral para liberar as ferramentas de IA.")
        client = None
    else:
        try:
            client = genai.Client(api_key=gemini_api_key)
        except Exception as e:
            st.error(f"Erro ao inicializar o cliente Gemini: {e}")
            client = None

    # Menu de Navegação Completo
    escolha = st.sidebar.selectbox(
        "Navegue pelas Ferramentas",
        [
            "💰 Precificação Inteligente",
            "💬 Gerador de Copy WhatsApp",
            "📸 Planejador Instagram",
            "✉️ Gerador de E-mail Comercial"
        ]
    )
    
    if st.sidebar.button("Sair da Conta"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    if client:
        if escolha == "💰 Precificação Inteligente":
            st.header("💰 Calculadora de Precificação Inteligente com IA")
            st.write("Analise custos, margem de lucro e o preço médio praticado pelo mercado.")
            
            produto = st.text_input("Nome do Produto ou Serviço")
            custo = st.number_input("Custo de Produção / Aquisição (R$)", min_value=0.0, format="%.2f")
            margem = st.slider("Margem de Lucro Desejada (%)", min_value=10, max_value=500, value=100)
            
            if st.button("Calcular Preço Ideal"):
                if produto and custo > 0:
                    with st.spinner("Analisando mercado e calculando..."):
                        prompt = f"""
                        Atue como um consultor financeiro especialista em precificação de negócios e SaaS.
                        Produto: {produto}
                        Custo de produção: R$ {custo}
                        Margem de lucro desejada: {margem}%
                        
                        Retorne uma análise detalhada contendo:
                        1. Preço de venda sugerido com base no markup.
                        2. Estimativa do preço médio praticado no mercado para esse tipo de item.
                        3. Lucro líquido estimado por unidade.
                        4. Dicas estratégicas para otimizar as vendas.
                        """
                        try:
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt
                            )
                            st.success("Análise de precificação concluída!")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Erro na IA: {e}")
                else:
                    st.warning("Insira o nome do produto e um custo válido.")

        elif escolha == "💬 Gerador de Copy WhatsApp":
            st.header("💬 Gerador de Copy para WhatsApp")
            st.write("Crie mensagens de vendas persuasivas de alta conversão em segundos.")
            
            nicho = st.text_input("Qual o seu nicho ou produto?")
            publico = st.text_input("Quem é o público-alvo?")
            oferta = st.text_area("Detalhes da oferta ou chamada")
            
            if st.button("Gerar Copy para WhatsApp"):
                if nicho and oferta:
                    with st.spinner("Criando copy de alta conversão..."):
                        prompt = f"""
                        Crie uma mensagem de vendas persuasiva para WhatsApp.
                        Nicho/Produto: {nicho}
                        Público: {publico}
                        Oferta: {oferta}
                        A mensagem deve ser direta, usar emojis estratégicos e ter uma chamada para ação clara.
                        """
                        try:
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt
                            )
                            st.success("Copy gerada com sucesso!")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Erro na IA: {e}")
                else:
                    st.warning("Preencha o nicho e os detalhes da oferta.")

        elif escolha == "📸 Planejador Instagram":
            st.header("📸 Planejador de Conteúdo para Instagram")
            st.write("Estruture sua grade de postagens para engajar sua audiência.")
            
            tema = st.text_input("Tema central ou nicho do perfil")
            qtd_dias = st.slider("Quantos dias de conteúdo planejar?", 3, 7, 5)
            
            if st.button("Planejar Conteúdo"):
                if tema:
                    with st.spinner("Planejando grade de conteúdo..."):
                        prompt = f"""
                        Crie um planejamento de conteúdo para o Instagram com duração de {qtd_dias} dias focado no tema: {tema}.
                        Para cada dia, forneça:
                        - Formato (Reels, Carrossel, Story)
                        - Ideia de título/gancho
                        - Legenda completa com hashtags
                        """
                        try:
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt
                            )
                            st.success("Planejamento concluído!")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Erro na IA: {e}")
                else:
                    st.warning("Informe o tema central.")

        elif escolha == "✉️ Gerador de E-mail Comercial":
            st.header("✉️ Gerador de E-mails Comerciais por IA")
            st.write("Crie e-mails de prospecção, follow-up ou propostas comerciais profissionais.")
            
            objetivo_email = st.selectbox(
                "Qual o objetivo do e-mail?",
                ["Prospecção a Frio (Primeiro Contato)", "Follow-up de Vendas", "Envio de Proposta Comercial", "Recuperação de Cliente Inativo"]
            )
            
            cliente_alvo = st.text_input("Para quem é o e-mail? (Ex: Gerente de Compras, Dono de E-commerce)")
            detalhes_produto = st.text_area("O que você está vendendo ou oferecendo? (Descreva brevemente)")
            
            if st.button("Gerar E-mail Profissional"):
                if detalhes_produto:
                    with st.spinner("A IA está redigindo o e-mail estratégico..."):
                        prompt = f"""
                        Escreva um e-mail comercial altamente persuasivo e profissional.
                        Objetivo do e-mail: {objetivo_email}
                        Público-alvo / Destinatário: {cliente_alvo}
                        Detalhes do produto/serviço: {detalhes_produto}
                        
                        O e-mail deve ter um assunto chamativo, uma abertura cordial, uma proposta de valor clara e um Call to Action (CTA) forte no final.
                        """
                        try:
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt
                            )
                            st.success("E-mail gerado com sucesso!")
                            st.markdown("---")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Erro ao gerar e-mail: {e}")
                else:
                    st.warning("Por favor, preencha os detalhes do produto ou serviço.")
