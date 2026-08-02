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

# Funções de Criptografia e Banco de Dados SQLite (Usuários + Histórico + Admin)
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hash(password, hashed_text):
    if make_hash(password) == hashed_text:
        return True
    return False

def init_db():
    conn = sqlite3.connect('neurax_users.db', check_same_thread=False)
    cursor = conn.cursor()
    # Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    # Tabela de Histórico de Gerações
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
    # Painel Principal do SaaS
    st.sidebar.title("Painel NeuraX")
    st.sidebar.write(f"Logado como: **{st.session_state['username']}**")
    
    # Estatísticas de Sessão
    st.sidebar.markdown("---")
    st.sidebar.metric(label="Gerações nesta Sessão", value=st.session_state["generation_count"])
    st.sidebar.markdown("---")
    
    # Configuração da Chave da API da Groq
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

    # Montagem Dinâmica do Menu (Admin ganha acesso a opção extra)
    menu_options = [
        "💰 Precificação Inteligente",
        "💬 Gerador de Copy WhatsApp",
        "📸 Planejador Instagram",
        "✉️ Gerador de E-mail Comercial",
        "🎬 Gerador de Roteiro para Vídeos",
        "📂 Meu Histórico"
    ]
    
    # Verificação inteligente para o Admin (ignora espaços e letras maiúsculas/minúsculas)
    if st.session_state["username"].strip().lower() == "admin":
        menu_options.append("🛠️ Painel Administrativo")

    escolha = st.sidebar.selectbox("Navegue pelas Ferramentas", menu_options)
    
    if st.sidebar.button("Sair da Conta"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    if escolha == "🛠️ Painel Administrativo":
        st.header("🛠️ Painel Administrativo - NeuraX Suite")
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

    elif client:
        model_name = "llama-3.3-70b-versatile"

        if escolha == "💰 Precificação Inteligente":
            st.header("💰 Calculadora de Precificação Inteligente com IA")
            st.write("Analise custos, margem de lucro, psicologia do consumidor e testes práticos de mercado.")
            
            produto = st.text_input("Nome do Produto ou Serviço")
            custo = st.number_input("Custo de Produção / Aquisição (R$)", min_value=0.0, format="%.2f")
            margem = st.slider("Margem de Lucro Desejada (%)", min_value=10, max_value=500, value=100)
            
            if st.button("Calcular Preço Ideal"):
                if produto and custo > 0:
                    with st.spinner("Analisando mercado, custos e o fator humano..."):
                        prompt = f"""
                        Atue como um consultor financeiro especialista em precificação estratégica e comportamento do consumidor.
                        Produto: {produto}
                        Custo de produção: R$ {custo}
                        Margem de lucro desejada: {margem}%
                        
                        Leve em conta não apenas os cálculos frios de markup, mas também o fator humano, a percepção de valor do cliente e a validação prática no mundo real.
                        
                        Retorne uma análise detalhada contendo:
                        1. Preço de venda sugerido com base nos custos e na percepção de valor.
                        2. Estimativa do preço médio praticado no mercado.
                        3. Lucro líquido estimado por unidade.
                        4. **Análise do Fator Humano e Psicologia do Consumidor** (como o público enxerga o valor e barreiras de preço).
                        5. **Estratégias de Teste Prático** (sugestões de como testar o preço de forma segura na prática antes de fixá-lo definitivamente).
                        """
                        try:
                            completion = client.chat.completions.create(
                                model=model_name,
                                messages=[{"role": "user", "content": prompt}]
                            )
                            st.session_state["generation_count"] += 1
                            resultado = completion.choices[0].message.content
                            
                            save_history(st.session_state["username"], "Precificação Inteligente", resultado)
                            
                            st.success("Análise estratégica de precificação concluída e salva no histórico!")
                            st.markdown(resultado)
                            
                            st.download_button(
                                label="📥 Baixar Relatório de Precificação (.txt)",
                                data=resultado,
                                file_name=f"precificacao_{produto.lower().replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
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
                            completion = client.chat.completions.create(
                                model=model_name,
                                messages=[{"role": "user", "content": prompt}]
                            )
                            st.session_state["generation_count"] += 1
                            resultado = completion.choices[0].message.content
                            
                            save_history(st.session_state["username"], "Copy WhatsApp", resultado)
                            
                            st.success("Copy gerada e salva no histórico com sucesso!")
                            st.markdown(resultado)
                            
                            st.download_button(
                                label="📥 Baixar Copy do WhatsApp (.txt)",
                                data=resultado,
                                file_name="copy_whatsapp.txt",
                                mime="text/plain"
                            )
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
                            completion = client.chat.completions.create(
                                model=model_name,
                                messages=[{"role": "user", "content": prompt}]
                            )
                            st.session_state["generation_count"] += 1
                            resultado = completion.choices[0].message.content
                            
                            save_history(st.session_state["username"], "Planejador Instagram", resultado)
                            
                            st.success("Planejamento concluído e salvo no histórico!")
                            st.markdown(resultado)
                            
                            st.download_button(
                                label="📥 Baixar Planejamento (.txt)",
                                data=resultado,
                                file_name="planejamento_instagram.txt",
                                mime="text/plain"
                            )
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
                            completion = client.chat.completions.create(
                                model=model_name,
                                messages=[{"role": "user", "content": prompt}]
                            )
                            st.session_state["generation_count"] += 1
                            resultado = completion.choices[0].message.content
                            
                            save_history(st.session_state["username"], "E-mail Comercial", resultado)
                            
                            st.success("E-mail gerado e salvo no histórico com sucesso!")
                            st.markdown("---")
                            st.markdown(resultado)
                            
                            st.download_button(
                                label="📥 Baixar E-mail Comercial (.txt)",
                                data=resultado,
                                file_name="email_comercial.txt",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error(f"Erro ao gerar e-mail: {e}")
                else:
                    st.warning("Por favor, preencha os detalhes do produto ou serviço.")

        elif escolha == "🎬 Gerador de Roteiro para Vídeos":
            st.header("🎬 Gerador de Roteiro para Vídeos (Reels / TikTok / YouTube)")
            st.write("Crie roteiros magnéticos com ganchos fortes para prender a atenção do espectador nos primeiros segundos.")
            
            tema_video = st.text_input("Qual o tema principal do vídeo?")
            formato_video = st.selectbox("Formato do vídeo", ["Reels / TikTok (Curto - Até 1 min)", "YouTube (Longo - 5 a 10 min)"])
            tom_comunicacao = st.selectbox("Tom de voz", ["Dinâmico e Enérgico", "Educativo e Profissional", "Polêmico / Provocativo", "Divertido"])
            
            if st.button("Gerar Roteiro Completo"):
                if tema_video:
                    with st.spinner("Escrevendo roteiro de alto engajamento..."):
                        prompt = f"""
                        Atue como um roteirista profissional de vídeo e criador de conteúdo de sucesso.
                        Tema: {tema_video}
                        Formato: {formato_video}
                        Tom de voz: {tom_comunicacao}
                        
                        Crie um roteiro estruturado contendo:
                        1. **Gancho (Hook)**: Os primeiros 3 segundos cruciais para reter a atenção.
                        2. **Desenvolvimento / Corpo**: Argumentos principais divididos em passos ou tópicos claros.
                        3. **Chamada para Ação (CTA)**: O que o espectador deve fazer no final.
                        4. **Dicas de Edição / B-roll**: Sugestões visuais e de legendas para enriquecer o vídeo.
                        """
                        try:
                            completion = client.chat.completions.create(
                                model=model_name,
                                messages=[{"role": "user", "content": prompt}]
                            )
                            st.session_state["generation_count"] += 1
                            resultado = completion.choices[0].message.content
                            
                            save_history(st.session_state["username"], "Roteiro para Vídeos", resultado)
                            
                            st.success("Roteiro gerado e salvo no histórico com sucesso!")
                            st.markdown("---")
                            st.markdown(resultado)
                            
                            st.download_button(
                                label="📥 Baixar Roteiro (.txt)",
                                data=resultado,
                                file_name=f"roteiro_{tema_video.lower().replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error(f"Erro ao gerar roteiro: {e}")
                else:
                    st.warning("Por favor, informe o tema principal do vídeo.")
