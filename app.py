import streamlit as st
from groq import Groq
import hashlib
from datetime import datetime
import pandas as pd
from supabase import create_client, Client
import pypdf
import io

# Configuração inicial da página
st.set_page_config(
    page_title="NeuraX Suite Pro - Life OS",
    page_icon="🚀",
    layout="wide"
)

# Inicialização do Cliente Supabase via Secrets
try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    supabase = None

# Estilização visual customizada
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp { background-color: #0b0f19; color: #f3f4f6; }
    footer {visibility: hidden;}
    h1, h2, h3 { color: #38bdf8 !important; font-weight: 700; }
    
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
        padding-top: 1rem;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        font-size: 1.1rem; font-weight: 700; color: #38bdf8 !important; margin-bottom: 12px; letter-spacing: 0.5px;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 8px; }
    [data-testid="stSidebar"] .stRadio label {
        background-color: #1a2234; border: 1px solid #2d3748; padding: 10px 14px; border-radius: 10px;
        transition: all 0.3s ease; cursor: pointer; width: 100%;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #0284c7; border-color: #38bdf8; transform: translateX(4px); box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%); color: white; border-radius: 10px;
        font-weight: 600; padding: 0.6rem 1.2rem; border: none; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3); transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%); box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5); transform: translateY(-1px);
    }
    
    [data-testid="stMetric"] { background: #111827; border: 1px solid #1f2937; padding: 15px; border-radius: 12px; }
    .streamlit-expanderHeader { background-color: #111827; border: 1px solid #1f2937; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Funções de Criptografia e Supabase
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed_text):
    return make_hash(password) == hashed_text

def add_user(username, password):
    if not supabase:
        st.error("Erro: Supabase não inicializado.")
        return
    try:
        if supabase.table("users").select("username").eq("username", username).execute().data:
            st.warning("Este usuário já existe.")
        else:
            supabase.table("users").insert({"username": username, "password": make_hash(password)}).execute()
            st.success("Cadastro realizado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao cadastrar: {e}")

def login_user(username, password):
    if username.strip().lower() == "admin" and password.strip().lower() == "admin":
        return True
    if not supabase:
        return False
    try:
        data = supabase.table("users").select("password").eq("username", username).execute().data
        if data and check_hash(password, data[0]["password"]):
            return True
    except Exception:
        pass
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
    except Exception:
        pass

def get_history(username):
    if not supabase:
        return []
    try:
        data = supabase.table("history").select("tool_name, content, timestamp").eq("username", username).order("id", desc=True).execute().data
        return [(r["tool_name"], r["content"], r["timestamp"]) for r in data]
    except Exception:
        return []

def get_all_users():
    if not supabase:
        return []
    try:
        data = supabase.table("users").select("username").execute().data
        return [r["username"] for r in data]
    except Exception:
        return []

def get_all_history_admin():
    if not supabase:
        return []
    try:
        data = supabase.table("history").select("username, tool_name, timestamp").order("id", desc=True).execute().data
        return [(r["username"], r["tool_name"], r["timestamp"]) for r in data]
    except Exception:
        return []

# Gerenciamento de Sessão
for key in ["logged_in", "username", "generation_count"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else ("" if key == "username" else 0)

# Tela de Autenticação
if not st.session_state["logged_in"]:
    st.title("🚀 NeuraX Suite Pro")
    st.markdown("### O Único Ecossistema Inteligente que Você Precisa")
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
                st.error("Dados incorretos.")
    else:
        if st.button("Criar Conta"):
            if user and pwd:
                add_user(user, pwd)
            else:
                st.warning("Preencha todos os campos.")

else:
    # Sidebar
    st.sidebar.title("⚡ NeuraX OS")
    st.sidebar.write(f"Operador: **{st.session_state['username']}**")
    
    st.sidebar.subheader("⚙️ Preferências de IA")
    user_tone = st.sidebar.selectbox(
        "Tom de Voz", 
        [
            "Persuasivo & Direto", 
            "Técnico & Profissional", 
            "Divertido & Descontraído", 
            "Empático & Acolhedor"
        ]
    )
    
    model_choice = st.sidebar.selectbox("Modelo", ["Llama-3.3-70b-versatile", "Llama-3.1-8b-instant"])
    model_name = "llama-3.3-70b-versatile" if "70b" in model_choice else "llama-3.1-8b-instant"
    
    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
    if not groq_api_key or not groq_api_key.startswith("gsk_"):
        groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

    client = Groq(api_key=groq_api_key) if groq_api_key else None

    # MENU DE FERRAMENTAS COMPLETO
    menu_options = [
        "📊 Meu Painel de Produtividade",
        "📂 Analista de Arquivos & PDFs",
        "⚡ Gestor de Tarefas Inteligente",
        "🧠 Mentor de Saúde Mental",
        "📚 Tutor Universal & Estudos",
        "🗺️ Arquiteto de Funis de Vendas",
        "💰 Precificação Inteligente",
        "🎯 Gerador de Anúncios (Meta/Google)",
        "🚀 NeuraX Growth Engine",
        "💬 Gerador de Copy WhatsApp",
        "📸 Planejador Instagram",
        "✉️ Gerador de E-mail Comercial",
        "🎬 Gerador de Roteiro para Vídeos",
        "⚖️ Assistente de Burocracias",
        "💸 Consultor de Finanças Pessoais",
        "🍳 Assistente de Despensa & Rotina",
        "🎓 Simulador de Entrevistas",
        "📂 Meu Histórico"
    ]
    
    if st.session_state["username"].strip().lower() == "admin":
        menu_options.insert(0, "🛠️ Painel Administrativo")

    escolha = st.sidebar.radio("⚡ Menu de Ferramentas", menu_options)
    
    if st.sidebar.button("Sair da Conta"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    # --- EXECUÇÃO DAS FERRAMENTAS ---

    if escolha == "🛠️ Painel Administrativo":
        st.header("🛠️ Painel Administrativo - NeuraX Suite")
        st.success("Acesso Master Confirmado!")
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

    elif escolha == "📊 Meu Painel de Produtividade":
        st.header(f"📊 Painel de Produtividade de {st.session_state['username']}")
        user_history = get_history(st.session_state["username"])
        st.metric("Total de Conteúdos Gerados", len(user_history))
        
        if user_history:
            tools_list = [item[0] for item in user_history]
            df_tools = pd.DataFrame(tools_list, columns=["Ferramenta"]).value_counts().reset_index()
            df_tools.columns = ["Ferramenta", "Quantidade"]
            st.bar_chart(df_tools.set_index("Ferramenta"))
        else:
            st.info("Você ainda não utilizou nenhuma ferramenta.")

    elif escolha == "📂 Analista de Arquivos & PDFs":
        st.header("📂 Analista de Arquivos e PDFs")
        st.write("Faça o upload de contratos, faturas, artigos científicos ou livros e faça qualquer pergunta para a IA.")
        
        arquivo_pdf = st.file_uploader("Envie seu arquivo PDF", type=["pdf"])
        pergunta = st.text_input("O que você deseja saber ou resumir sobre este documento?")
        
        if st.button("Analisar PDF"):
            if not arquivo_pdf:
                st.warning("⚠️ Por favor, envie um arquivo PDF primeiro.")
            elif not pergunta:
                st.warning("⚠️ Por favor, digite o que você quer saber sobre o documento.")
            elif not client:
                st.warning("⚠️ Insira sua chave da Groq no menu lateral.")
            else:
                with st.spinner("Lendo o documento com segurança..."):
                    try:
                        bytes_arquivo = arquivo_pdf.getvalue()
                        leitor = pypdf.PdfReader(io.BytesIO(bytes_arquivo))
                        
                        if leitor.is_encrypted:
                            st.error("⚠️ Este PDF está protegido por senha. Por favor, envie um arquivo desbloqueado.")
                        else:
                            texto_extraido = ""
                            for pagina in leitor.pages:
                                texto = pagina.extract_text()
                                if texto:
                                    texto_extraido += texto + "\n"
                            
                            if not texto_extraido.strip():
                                st.error("⚠️ Este PDF parece ser uma imagem escaneada (sem texto selecionável).")
                            else:
                                texto_limitado = texto_extraido[:30000]
                                prompt = (
                                    f"Atue como um Especialista em Análise Documental sênior aplicando o tom de voz: '{user_tone}'.\n"
                                    f"Com base estritamente no texto extraído do PDF abaixo:\n\n"
                                    f"--- INÍCIO DO TEXTO ---\n{texto_limitado}\n--- FIM DO TEXTO ---\n\n"
                                    f"Responda detalhadamente e com clareza à seguinte requisição do usuário: '{pergunta}'"
                                )
                                
                                completion = client.chat.completions.create(
                                    model=model_name, 
                                    messages=[{"role": "user", "content": prompt}]
                                )
                                resultado = completion.choices[0].message.content
                                st.session_state["generation_count"] += 1
                                save_history(st.session_state["username"], "Analista de PDF", resultado)
                                
                                st.success("Análise Concluída com Sucesso!")
                                st.markdown(resultado)
                    except Exception as e:
                        st.error(f"Erro ao processar o arquivo PDF: {e}")

    elif escolha == "⚡ Gestor de Tarefas Inteligente":
        st.header("⚡ Gestor de Rotina e Tarefas")
        st.write("Despeje tudo o que você precisa fazer e deixe a IA priorizar seu dia.")
        
        tarefas_brutas = st.text_area("Despeje suas tarefas aqui:")
        horas_disponiveis = st.number_input("Quantas horas livres você tem hoje?", min_value=1, value=8)
        
        if st.button("Organizar Meu Dia"):
            if tarefas_brutas and client:
                with st.spinner("Construindo matriz de produtividade..."):
                    prompt = f"Atue como um Especialista em Produtividade (Tom: '{user_tone}'). O usuário tem {horas_disponiveis} horas livres e as tarefas: '{tarefas_brutas}'. Crie uma organização usando a Matriz de Eisenhower e monte um cronograma realista."
                    completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                    resultado = completion.choices[0].message.content
                    st.session_state["generation_count"] += 1
                    save_history(st.session_state["username"], "Gestor de Tarefas", resultado)
                    st.success("Rotina otimizada!")
                    st.markdown(resultado)

    elif escolha == "🧠 Mentor de Saúde Mental":
        st.header("🧠 Diário Emocional e Bem-Estar")
        st.write("Um espaço seguro para refletir, organizar os pensamentos e receber apoio.")
        
        humor = st.select_slider("Como você está se sentindo hoje?", options=["Péssimo", "Triste", "Neutro", "Bem", "Incrível"], value="Neutro")
        desabafo = st.text_area("Escreva livremente sobre o seu dia (Journaling):")
        
        if st.button("Refletir com o Mentor"):
            if desabafo and client:
                with st.spinner("Processando..."):
                    prompt = f"Atue como um Mentor de Bem-Estar empático e acolhedor (Tom: '{user_tone}'). O usuário está se sentindo '{humor}' e escreveu: '{desabafo}'. Responda validando sentimentos e termine sugerindo um exercício prático de respiração ou foco."
                    completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                    resultado = completion.choices[0].message.content
                    st.session_state["generation_count"] += 1
                    save_history(st.session_state["username"], "Saúde Mental", resultado)
                    st.markdown(resultado)

    elif escolha == "📚 Tutor Universal & Estudos":
        st.header("📚 Tutor Particular e Estudos")
        assunto = st.text_input("O que você precisa aprender ou estudar hoje?")
        tipo_estudo = st.selectbox("Qual o formato?", ["Explicação Simples (Analogias)", "Criar Quiz/Simulado de Prova", "Prática de Idioma", "Gerar Flashcards"])
        
        if st.button("Iniciar Sessão de Estudo"):
            if assunto and client:
                with st.spinner("O Professor NeuraX está preparando a aula..."):
                    prompt = f"Atue como um Professor Universitário genial (Tom: '{user_tone}'). O usuário quer estudar: '{assunto}' no formato: '{tipo_estudo}'. Entregue o conteúdo de forma didática com markdown limpo."
                    completion = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                    resultado = completion.choices[0].message.content
                    st.session_state["generation_count"] += 1
                    save_history(st.session_state["username"], "Tutor Universal", resultado)
                    st.markdown(resultado)

    elif escolha == "🗺️ Arquiteto de Funis de Vendas":
        st.header("🗺️ Arquiteto de Funis de Vendas")
        funil_produto = st.text_input("Qual é o seu produto ou serviço?")
        funil_publico = st.text_input("Quem é o seu público-alvo?")
        if st.button("Gerar Estratégia e Fluxograma"):
            if funil_produto and client:
                with st.spinner("Desenhando a arquitetura..."):
                    prompt = f"Crie um funil de vendas estratégico para '{funil_produto}' e público '{funil_publico}'. Inclua uma descrição passo a passo e um diagrama em Mermaid (graph TD). Tom: {user_tone}."
                    resultado = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]).choices[0].message.content
                    st.session_state["generation_count"] += 1
                    save_history(st.session_state["username"], "Arquiteto de Funis", resultado)
                    st.markdown(resultado)

    elif escolha == "💰 Precificação Inteligente":
        st.header("💰 Calculadora de Precificação Inteligente")
        produto = st.text_input("Nome do Produto ou Serviço")
        custo = st.number_input("Custo (R$)", min_value=0.0, format="%.2f")
        if st.button("Calcular Preço Ideal"):
            if produto and client:
                with st.spinner("Analisando..."):
                    prompt = f"Elabore uma análise detalhada de precificação para '{produto}' com custo de R${custo}. Tom: {user_tone}."
                    resultado = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]).choices[0].message.content
                    st.session_state["generation_count"] += 1
                    save_history(st.session_state["username"], "Precificação Inteligente", resultado)
                    st.markdown(resultado)

    elif escolha == "🎯 Gerador de Anúncios (Meta/Google)":
        st.header("🎯 Gerador de Anúncios de Alta Conversão")
        anuncio_produto = st.text_input("Qual é o produto, serviço ou oferta?")
        if st.button("Gerar Copys de Anúncio"):
            if anuncio_produto and client:
                with st.spinner("Criando estruturas..."):
                    prompt = f"Crie copies de anúncios magnéticas para vender '{anuncio_produto}'. Tom: {user_tone}."
                    resultado = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]).choices[0].message.content
                    st.session_state["generation_count"] += 1
                    save_history(st.session_state["username"], "Gerador de Anúncios", resultado)
                    st.markdown(resultado)

    elif escolha == "🚀 NeuraX Growth Engine":
        st.header("🚀 NeuraX Growth Engine - Simulador")
        orcamento = st.number_input("Orçamento Mensal Ads (R$)", min_value=100.0, value=2000.0)
        meta_fat = st.number_input("Meta de Faturamento Mensal (R$)", min_value=500.0, value=20000.0)
        if st.button("Executar Simulação"):
            if client:
                with st.spinner("Desenhando plano de guerra..."):
                    prompt = f"Crie um plano tático de marketing para transformar R${orcamento} em R${meta_fat}. Tom: {user_tone}."
                    resultado = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]).choices[0].message.content
                    st.session_state["generation_count"] += 1
                    save_history(st.session_state["username"], "NeuraX Growth Engine", resultado)
                    st.markdown(resultado)

    elif escolha in [
        "💬 Gerador de Copy WhatsApp", 
        "📸 Planejador Instagram", 
        "✉️ Gerador de E-mail Comercial", 
        "🎬 Gerador de Roteiro para Vídeos", 
        "⚖️ Assistente de Burocracias", 
        "💸 Consultor de Finanças Pessoais", 
        "🍳 Assistente de Despensa & Rotina", 
        "🎓 Simulador de Entrevistas"
    ]:
        st.header(escolha)
        detalhe = st.text_area("Descreva os detalhes do que você precisa:")
        if st.button("Gerar com IA"):
            if detalhe and client:
                with st.spinner("Processando requisição..."):
                    prompt = f"Atue como um Especialista (Tom: '{user_tone}'). Resolva a demanda da ferramenta '{escolha}': {detalhe}"
                    resultado = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}]).choices[0].message.content
                    st.session_state["generation_count"] += 1
                    save_history(st.session_state["username"], escolha, resultado)
                    st.markdown(resultado)

    elif escolha == "📂 Meu Histórico":
        st.header("📂 Histórico de Gerações")
        user_history = get_history(st.session_state["username"])
        if not user_history:
            st.info("Nenhum histórico encontrado.")
        else:
            for idx, (tool, content, timestamp) in enumerate(user_history):
                with st.expander(f"🛠️ [{tool}] - {timestamp}"):
                    st.markdown(content)
                    st.download_button(
                        label="📥 Baixar (.txt)",
                        data=content,
                        file_name=f"hist_{idx}.txt",
                        mime="text/plain"
                    )
