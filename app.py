import streamlit as st
from groq import Groq
import hashlib
from datetime import datetime
import pandas as pd
from supabase import create_client, Client

# Configuração inicial da página
st.set_page_config(
    page_title="NeuraX Suite Pro",
    page_icon="🚀",
    layout="wide"
)

# Inicialização do Cliente Supabase via Secrets
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Erro ao conectar com o Supabase. Verifique os Secrets: {e}")
    supabase = None

# Estilização visual customizada (Tema NeuraX Pro - Dark Moderno & Elegante com Menu Moderno)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Fundo geral do aplicativo */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Oculta o rodapé padrão do Streamlit */
    footer {visibility: hidden;}
    
    /* Cabeçalhos estilizados */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 700;
    }
    
    /* Sidebar moderna */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
        padding-top: 1rem;
    }
    
    /* Customização moderna para o Menu Radio da Sidebar (Estilo Cards Interativos) */
    [data-testid="stSidebar"] .stRadio > label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #38bdf8 !important;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 8px;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        background-color: #1a2234;
        border: 1px solid #2d3748;
        padding: 10px 14px;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #0284c7;
        border-color: #38bdf8;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
    }
    
    /* Botões com efeito neon e gradiente */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5);
        transform: translateY(-1px);
    }
    
    /* Cards de Métricas */
    [data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #1f2937;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Blocos de expansão personalizados */
    .streamlit-expanderHeader {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Funções de Criptografia e Banco de Dados Supabase
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed_text):
    if make_hash(password) == hashed_text:
        return True
    return False

def add_user(username, password):
    if not supabase:
        st.error("Erro: Supabase não inicializado. Verifique os Secrets.")
        return
    try:
        existing = supabase.table("users").select("username").eq("username", username).execute()
        if existing.data:
            st.warning("Este usuário já existe. Escolha outro nome ou faça login.")
        else:
            supabase.table("users").insert({"username": username, "password": make_hash(password)}).execute()
            st.success("Cadastro realizado com sucesso! Alterne para a aba de Login.")
    except Exception as e:
        st.error(f"Erro ao cadastrar usuário: {e}")

def login_user(username, password):
    if username.strip().lower() == "admin" and password.strip().lower() == "admin":
        return True
    
    if not supabase:
        return False
    try:
        response = supabase.table("users").select("password").eq("username", username).execute()
        data = response.data
        if data:
            if check_hash(password, data[0]["password"]):
                return True
    except Exception as e:
        st.error(f"Erro ao realizar login: {e}")
    return False

def save_history(username, tool_name, content):
    if not supabase:
        return
    try:
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        supabase.table("history").insert({
            "username": username,
            "tool_name": tool_name,
            "content": content,
            "timestamp": timestamp
        }).execute()
    except Exception as e:
        st.error(f"Erro ao salvar histórico: {e}")

def get_history(username):
    if not supabase:
        return []
    try:
        response = supabase.table("history").select("tool_name, content, timestamp").eq("username", username).order("id", desc=True).execute()
        return [(row["tool_name"], row["content"], row["timestamp"]) for row in response.data]
    except Exception:
        return []

def get_all_users():
    if not supabase:
        return []
    try:
        response = supabase.table("users").select("username").execute()
        return [row["username"] for row in response.data]
    except Exception:
        return []

def get_all_history_admin():
    if not supabase:
        return []
    try:
        response = supabase.table("history").select("username, tool_name, timestamp").order("id", desc=True).execute()
        return [(row["username"], row["tool_name"], row["timestamp"]) for row in response.data]
    except Exception:
        return []

# Gerenciamento de Sessão de Login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "generation_count" not in st.session_state:
    st.session_state["generation_count"] = 0

# Tela de Autenticação
if not st.session_state["logged_in"]:
    st.title("🚀 NeuraX Suite Pro")
    st.markdown("### Ecossistema Avançado de Inteligência Artificial")
    st.write("Faça login ou crie sua conta para acessar ferramentas profissionais de alta performance.")
    
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
            else:
                st.warning("Preencha todos os campos.")

else:
    # Painel Principal (Sidebar)
    st.sidebar.title("⚡ NeuraX Control")
    st.sidebar.write(f"Operador: **{st.session_state['username']}**")
    
    st.sidebar.markdown("---")
    st.sidebar.metric(label="Gerações na Sessão", value=st.session_state["generation_count"])
    st.sidebar.markdown("---")
    
    # Sistema de Preferências (Tom de Voz Global)
    st.sidebar.subheader("⚙️ Preferências de IA")
    user_tone = st.sidebar.selectbox(
        "Tom de Voz Padrão",
        [
            "Persuasivo & Direto (Foco em Conversão)",
            "Técnico & Profissional (Autoridade Sênior)",
            "Divertido & Descontraído (Engajamento)",
            "Inspirador & Emocional (Storytelling)"
        ]
    )
    
    st.sidebar.markdown("---")
    
    # Carregamento da API Key da Groq
    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
    
    if not groq_api_key or not groq_api_key.startswith("gsk_"):
        groq_api_key = st.sidebar.text_input("Insira sua Groq API Key (gsk_...)", type="password")

    if not groq_api_key:
        st.warning("⚠️ Insira uma chave válida da Groq no menu lateral para ativar as ferramentas de IA.")
        client = None
    else:
        try:
            client = Groq(api_key=groq_api_key)
        except Exception as e:
            st.error(f"Erro ao inicializar o cliente Groq: {e}")
            client = None

    # MENU DE FERRAMENTAS MODERNO
    menu_options = [
        "🗺️ Arquiteto de Funis de Vendas",
        "💰 Precificação Inteligente",
        "💬 Gerador de Copy WhatsApp",
        "📸 Planejador Instagram",
        "✉️ Gerador de E-mail Comercial",
        "🎬 Gerador de Roteiro para Vídeos",
        "📂 Meu Histórico"
    ]
    
    usuario_logado = st.session_state["username"].strip().lower()
    if usuario_logado == "admin":
        menu_options.insert(0, "🛠️ Painel Administrativo")

    # Substituição do selectbox por um Radio estilizado em formato de cartões modernos
    escolha = st.sidebar.radio("⚡ Menu de Ferramentas", menu_options)
    
    st.sidebar.markdown("---")
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
                        prompt = (
                            f"Atue como um Estrategista de Marketing Digital sênior aplicando o tom de voz: '{user_tone}'.\n"
                            f"Crie um funil de vendas estratégico completo para o produto: '{funil_produto}', com ticket '{funil_ticket}', voltado para o público: '{funil_publico}'.\n"
                            "Sua resposta deve conter obrigatoriamente:\n"
                            "1. A estratégia detalhada por etapas (Tráfego/Atração, Página de Captura/Conversão, Oferta/Checkout, Recuperação/Upsell).\n"
                            "2. Um diagrama de fluxo utilizando a sintaxe nativa do Mermaid. O bloco de código DEVE começar obrigatoriamente com a declaração de direção 'graph TD' na primeira linha interna.\n"
                            "Use apenas setas simples (ex: A --> B) sem textos complexos ou caracteres especiais nas setas."
                        )
                        try:
                            completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                            resultado = completion.choices[0].message.content
                            st.session_state["generation_count"] += 1
                            save_history(st.session_state["username"], "Arquiteto de Funis", resultado)
                            st.success("Arquitetura e Fluxograma gerados com sucesso!")
                            st.markdown(resultado)
                        except Exception as e:
                            st.error(f"Erro ao conectar com a Groq: {e}.")

        elif escolha == "💰 Precificação Inteligente":
            st.header("💰 Calculadora de Precificação Inteligente com IA")
            produto = st.text_input("Nome do Produto ou Serviço")
            custo = st.number_input("Custo (R$)", min_value=0.0, format="%.2f")
            margem = st.slider("Margem de Lucro (%)", min_value=10, max_value=500, value=100)
            
            if st.button("Calcular Preço Ideal"):
                if produto and custo > 0:
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Atue como um Especialista em Finanças e Precificação aplicando o tom de voz: '{user_tone}'.\n"
                            f"Elabore uma análise detalhada e estruturada de precificação para o produto/serviço: '{produto}', com custo de R$ {custo:.2f} e margem de lucro de {margem}%.\n"
                            "Sua resposta deve ser estritamente em Markdown limpo, sem erros matemáticos colados, contendo:\n"
                            "1. O detalhamento claro do custo.\n"
                            "2. A aplicação correta da margem de lucro e o preço de venda final formatado de forma legível (ex: R$ 00,00).\n"
                            "3. A análise de impacto do lucro para o negócio.\n"
                            "4. Orientações estratégicas e uma chamada para ação (CTA) forte para o profissional."
                        )
                        try:
                            completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                            resultado = completion.choices[0].message.content
                            st.session_state["generation_count"] += 1
                            save_history(st.session_state["username"], "Precificação Inteligente", resultado)
                            st.success("Análise concluída!")
                            st.markdown(resultado)
                        except Exception as e:
                            st.error(f"Erro ao conectar com a Groq: {e}.")

        elif escolha == "💬 Gerador de Copy WhatsApp":
            st.header("💬 Gerador de Copy para WhatsApp")
            nicho = st.text_input("Seu nicho/produto")
            publico = st.text_input("Público-alvo")
            oferta = st.text_area("Oferta")
            
            if st.button("Gerar Copy"):
                if nicho and oferta:
                    with st.spinner("Criando..."):
                        prompt = "Com base no tom '{}', crie copy de vendas para WhatsApp. Nicho: {}, Público: {}, Oferta: {}.".format(
                            user_tone, nicho, publico, oferta
                        )
                        try:
                            completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                            resultado = completion.choices[0].message.content
                            st.session_state["generation_count"] += 1
                            save_history(st.session_state["username"], "Copy WhatsApp", resultado)
                            st.success("Gerado!")
                            st.markdown(resultado)
                        except Exception as e:
                            st.error(f"Erro ao conectar com a Groq: {e}.")

        elif escolha == "📸 Planejador Instagram":
            st.header("📸 Planejador Instagram")
            tema = st.text_input("Tema central")
            qtd_dias = st.slider("Dias", 3, 7, 5)
            
            if st.button("Planejar Conteúdo"):
                if tema:
                    with st.spinner("Planejando..."):
                        prompt = "Adotando o tom '{}', planeje conteúdo para Instagram por {} dias sobre: {}.".format(
                            user_tone, qtd_dias, tema
                        )
                        try:
                            completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                            resultado = completion.choices[0].message.content
                            st.session_state["generation_count"] += 1
                            save_history(st.session_state["username"], "Planejador Instagram", resultado)
                            st.success("Planejado!")
                            st.markdown(resultado)
                        except Exception as e:
                            st.error(f"Erro ao conectar com a Groq: {e}.")

        elif escolha == "✉️ Gerador de E-mail Comercial":
            st.header("✉️ Gerador de E-mail Comercial")
            objetivo_email = st.selectbox("Objetivo", ["Prospecção", "Follow-up", "Proposta", "Recuperação"])
            cliente_alvo = st.text_input("Para quem?")
            detalhes_produto = st.text_area("O que vende?")
            
            if st.button("Gerar E-mail"):
                if detalhes_produto:
                    with st.spinner("Redigindo..."):
                        prompt = "Usando o tom '{}', escreva e-mail de {} para {} vendendo {}.".format(
                            user_tone, objetivo_email, cliente_alvo, detalhes_produto
                        )
                        try:
                            completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                            resultado = completion.choices[0].message.content
                            st.session_state["generation_count"] += 1
                            save_history(st.session_state["username"], "E-mail Comercial", resultado)
                            st.success("E-mail gerado!")
                            st.markdown(resultado)
                        except Exception as e:
                            st.error(f"Erro ao conectar com a Groq: {e}.")

        elif escolha == "🎬 Gerador de Roteiro para Vídeos":
            st.header("🎬 Gerador de Roteiro para Vídeos")
            tema_video = st.text_input("Tema principal")
            formato_video = st.selectbox("Formato", ["Reels/TikTok", "YouTube"])
            tom = st.selectbox("Tom Específico", ["Dinâmico", "Educativo", "Polêmico", "Divertido"])
            
            if st.button("Gerar Roteiro"):
                if tema_video:
                    with st.spinner("Escrevendo..."):
                        prompt = "Considerando o tom global '{}' e tom específico '{}', crie um roteiro para {} sobre {}.".format(
                            user_tone, tom, formato_video, tema_video
                        )
                        try:
                            completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                            resultado = completion.choices[0].message.content
                            st.session_state["generation_count"] += 1
                            save_history(st.session_state["username"], "Roteiro para Vídeos", resultado)
                            st.success("Roteiro pronto!")
                            st.markdown(resultado)
                        except Exception as e:
                            st.error(f"Erro ao conectar com a Groq: {e}.")
