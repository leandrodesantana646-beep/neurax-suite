import streamlit as st
import sqlite3
import hashlib

# Tenta importar o cliente Groq
try:
    from groq import Groq
    TEM_GROQ = True
except ImportError:
    TEM_GROQ = False

# Configuração da Página
st.set_page_config(
    page_title="NeuraX Suite - Painel SaaS",
    page_icon="🚀",
    layout="centered"
)

# =========================================================
# BANCO DE DADOS & AUTENTICAÇÃO (SQLITE)
# =========================================================
def init_db():
    conn = sqlite3.connect('neurax_suite.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, item TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    return conn

conn = init_db()

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_login(username, password):
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    data = c.fetchone()
    if data and data[0] == make_hash(password):
        return True
    return False

def register_user(username, password):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, make_hash(password)))
        conn.commit()
        return True
    except:
        return False

def salvar_historico_db(username, item):
    c = conn.cursor()
    c.execute("INSERT INTO history (username, item) VALUES (?, ?)", (username, item))
    conn.commit()

def carregar_historico_db(username):
    c = conn.cursor()
    c.execute("SELECT item FROM history WHERE username = ? ORDER BY id DESC LIMIT 5", (username,))
    return [row[0] for row in c.fetchall()]

def limpar_historico_db(username):
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE username = ?", (username,))
    conn.commit()

# Controle de Sessão de Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Tela de Login e Cadastro se não estiver logado
if not st.session_state.logged_in:
    st.title("🔐 NeuraX Suite - Acesso ao Sistema")
    st.markdown("Faça login ou crie sua conta para acessar o painel inteligente de e-commerce.")
    
    tab_login, tab_reg = st.tabs(["🔑 Entrar", "📝 Criar Conta"])
    
    with tab_login:
        l_user = st.text_input("Usuário", key="l_user")
        l_pass = st.text_input("Senha", type="password", key="l_pass")
        if st.button("Entrar no Sistema", key="btn_login"):
            if check_login(l_user, l_pass):
                st.session_state.logged_in = True
                st.session_state.username = l_user
                st.success("Login realizado com sucesso! Carregando painel...")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
                
    with tab_reg:
        r_user = st.text_input("Escolha um Usuário", key="r_user")
        r_pass = st.text_input("Escolha uma Senha", type="password", key="r_pass")
        if st.button("Cadastrar Conta", key="btn_reg"):
            if r_user and r_pass:
                if register_user(r_user, r_pass):
                    st.success("Conta criada com sucesso! Vá para a aba 'Entrar'.")
                else:
                    st.error("Este nome de usuário já existe.")
            else:
                st.warning("Preencha todos os campos.")
    st.stop()

# =========================================================
# PAINEL PRINCIPAL (APÓS O LOGIN)
# =========================================================

# Customização Visual de Elite & Efeito Cards
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stButton>button {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff8f4b 100%);
        color: white; border-radius: 12px; font-weight: 600; padding: 0.6rem 1.2rem;
        border: none; box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3); transition: all 0.3s ease; width: 100%;
    }
    .stButton>button:hover { opacity: 0.95; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(255, 75, 75, 0.4); }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 10px; border: 1px solid #30363d; background-color: #0d1117;
    }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #30363d; background-color: #0d1117; color: #58a6ff; }
    </style>
""", unsafe_allow_html=True)

st.title(f"🚀 NeuraX Suite - Bem-vindo, {st.session_state.username}!")
st.markdown("O ecossistema definitivo de automação para e-commerce com IA e Banco de Dados.")

# Barra Lateral Avançada
st.sidebar.subheader("🔑 Configuração de IA")
groq_key_input = st.sidebar.text_input("Chave Groq API (Opcional):", type="password", help="Cole sua chave gratuita para ativar IA avançada.")

if groq_key_input:
    st.sidebar.success("⚡ IA Real Ativada!")
else:
    st.sidebar.info("💡 Modo Inteligente Padrão Ativo.")

st.sidebar.markdown("---")
st.sidebar.subheader("📜 Histórico Salvo (Banco de Dados)")
historico_usuario = carregar_historico_db(st.session_state.username)
if historico_usuario:
    for item in historico_usuario:
        st.sidebar.text(f"• {item}")
    if st.sidebar.button("Limpar Histórico", key="btn_limpar"):
        limpar_historico_db(st.session_state.username)
        st.rerun()
else:
    st.sidebar.info("Nenhum histórico recente salvo.")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Sair da Conta (Logout)", key="btn_logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# Função de IA
def gerar_resposta_ia(prompt_sistema, prompt_usuario):
    if not groq_key_input or not TEM_GROQ:
        return None
    try:
        client = Groq(api_key=groq_key_input)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt_usuario}],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Erro ao conectar com a IA: {e}")
        return None

# Organização por Abas Principais (4 abas profissionais)
tab1, tab2, tab3, tab4 = st.tabs(["⚡ Vendas & Conversão", "✍️ Conteúdo & Marketing", "📊 Finanças & Precificação", "🎯 Tráfego Pago (Novo!)"])

# =========================================================
# ABA 1: VENDAS & CONVERSÃO
# =========================================================
with tab1:
    st.subheader("Ferramentas de Vendas")
    escolha_tab1 = st.selectbox("Escolha a ferramenta:", ["⚡ Campanha Flash Sale Instantânea", "💬 Assistente de WhatsApp"], key="sub_tab1")
    
    if escolha_tab1 == "⚡ Campanha Flash Sale Instantânea":
        prod_flash = st.text_input("📦 Nome do produto em promoção:", key="flash_prod")
        preco_original = st.number_input("💰 Preço original (R$):", min_value=0.0, value=200.0, step=1.0, key="flash_orig")
        preco_flash = st.number_input("🔥 Preço promocional relâmpago (R$):", min_value=0.0, value=149.0, step=1.0, key="flash_desc")
        tempo_limite = st.selectbox("⏳ Duração da Oferta", ["Apenas hoje (24 horas)", "48 horas", "Enquanto durar o estoque"], key="flash_tempo")

        if st.button("Gerar Campanha Multicanal", key="btn_flash"):
            if prod_flash:
                economia = preco_original - preco_flash
                desconto_calc = int((economia / preco_original) * 100) if preco_original > 0 else 0

                prompt_ia = f"Crie uma campanha flash sale completa (WhatsApp, 3 Stories de Instagram e E-mail) para o produto '{prod_flash}', vendido de R$ {preco_original:.2f} por R$ {preco_flash:.2f} ({desconto_calc}% de desconto), duração: {tempo_limite}."
                kit_campanha = gerar_resposta_ia("Você é um especialista em copywriting e vendas.", prompt_ia)

                if not kit_campanha:
                    kit_campanha = f"⚡ KIT FLASH SALE: {prod_flash.upper()}\nDe: R$ {preco_original:.2f} Por: R$ {preco_flash:.2f} ({desconto_calc}% OFF). Corre no link!"

                st.success("🔥 Campanha gerada com sucesso!")
                st.text_area("Resultado:", kit_campanha, height=300, key="txt_flash")
                salvar_historico_db(st.session_state.username, f"Flash: {prod_flash}")
                st.download_button("📥 Baixar Campanha (.txt)", kit_campanha, file_name=f"campanha_{prod_flash}.txt", mime="text/plain", key="dl_flash")
            else:
                st.warning("⚠️ Digite o nome do produto.")

    elif escolha_tab1 == "💬 Assistente de WhatsApp":
        duvida_cliente = st.text_input("❓ Dúvida ou objeção do cliente:", key="wpp_duvida")
        nome_loja = st.text_input("🏷️ Nome da sua loja:", value="Nossa Loja", key="wpp_loja")

        if st.button("Gerar Resposta", key="btn_wpp"):
            if duvida_cliente:
                prompt_ia = f"Escreva uma resposta de WhatsApp amigável para a loja '{nome_loja}', respondendo: '{duvida_cliente}'."
                resposta_gerada = gerar_resposta_ia("Você é um assistente de atendimento de alta conversão.", prompt_ia)

                if not resposta_gerada:
                    resposta_gerada = f"Olá! Obrigado pelo contato com a {nome_loja}! Sobre '{duvida_cliente}': Garantimos total qualidade. Posso separar seu pedido?"

                st.success("💬 Resposta gerada!")
                st.text_area("Mensagem:", resposta_gerada, height=180, key="txt_wpp")
                salvar_historico_db(st.session_state.username, f"WhatsApp: {duvida_cliente[:12]}...")
                st.download_button("📥 Baixar Resposta (.txt)", resposta_gerada, file_name="wpp.txt", mime="text/plain", key="dl_wpp")
            else:
                st.warning("⚠️ Digite a dúvida.")

# =========================================================
# ABA 2: CONTEÚDO & MARKETING
# =========================================================
with tab2:
    st.subheader("Ferramentas de Conteúdo & Copy")
    escolha_tab2 = st.selectbox("Escolha a ferramenta:", ["🤖 Gerador de Copy e SEO", "🎬 Gerador de Roteiros (Reels/TikTok)"], key="sub_tab2")

    if escolha_tab2 == "🤖 Gerador de Copy e SEO":
        nome_produto = st.text_input("📦 Nome do produto:", key="copy_prod")
        publico = st.text_input("🎯 Público-alvo:", key="copy_pub")

        if st.button("Gerar Copy", key="btn_copy"):
            if nome_produto and publico:
                prompt_ia = f"Crie título SEO, descrição persuasiva e hashtags para '{nome_produto}' focado em '{publico}'."
                resultado = gerar_resposta_ia("Especialista em SEO e Copywriting.", prompt_ia)

                if not resultado:
                    resultado = f"[Título SEO]: {nome_produto} Original\n[Descrição]: O melhor para {publico}."

                st.success("✨ Copy gerada!")
                st.text_area("Resultado:", resultado, height=200, key="txt_copy")
                salvar_historico_db(st.session_state.username, f"Copy: {nome_produto}")
                st.download_button("📥 Baixar Copy (.txt)", resultado, file_name="copy.txt", mime="text/plain", key="dl_copy")
            else:
                st.warning("⚠️ Preencha os campos.")

    elif escolha_tab2 == "🎬 Gerador de Roteiros (Reels/TikTok)":
        prod_video = st.text_input("📦 Produto em destaque:", key="vid_prod")
        dor = st.text_input("🎯 Dor que o produto resolve:", key="vid_dor")

        if st.button("Gerar Roteiro", key="btn_vid"):
            if prod_video and dor:
                prompt_ia = f"Crie um roteiro viral (Gancho, Desenvolvimento, CTA) para '{prod_video}' resolvendo '{dor}'."
                roteiro = gerar_resposta_ia("Especialista em vídeos curtos virais.", prompt_ia)

                if not roteiro:
                    roteiro = f"1. GANCHO: Cansado de {dor}?\n2. SOLUÇÃO: Use {prod_video}.\n3. CTA: Compre no link!"

                st.success("🎬 Roteiro gerado!")
                st.text_area("Roteiro:", roteiro, height=220, key="txt_vid")
                salvar_historico_db(st.session_state.username, f"Roteiro: {prod_video}")
                st.download_button("📥 Baixar Roteiro (.txt)", roteiro, file_name="roteiro.txt", mime="text/plain", key="dl_vid")
            else:
                st.warning("⚠️ Preencha os campos.")

# =========================================================
# ABA 3: FINANÇAS & PRECIFICAÇÃO
# =========================================================
with tab3:
    st.subheader("Ferramentas Financeiras")
    escolha_tab3 = st.selectbox("Escolha a ferramenta:", ["📊 Analisador de Preços", "🧮 Calculadora de Taxas & Lucro"], key="sub_tab3")

    if escolha_tab3 == "📊 Analisador de Preços":
        produto_preco = st.text_input("📦 Nome do produto:", key="preco_prod")
        preco_atual = st.number_input("💰 Preço de venda atual (R$):", min_value=0.0, value=100.0, step=1.0, key="preco_val")

        if st.button("Executar Análise", key="btn_preco"):
            if produto_preco:
                med = max(preco_atual * 1.15, 100.00)
                sug = round(med * 0.95, 2)
                relatorio = f"[Produto]: {produto_preco}\n[Preço Atual]: R$ {preco_atual:.2f}\n[Preço Sugerido Ideal]: R$ {sug:.2f}"
                st.success("🎯 Análise concluída!")
                st.text_area("Relatório:", relatorio, height=200, key="txt_preco")
                salvar_historico_db(st.session_state.username, f"Preço: {produto_preco}")
                st.download_button("📥 Baixar Relatório (.txt)", relatorio, file_name="preco.txt", mime="text/plain", key="dl_preco")
            else:
                st.warning("⚠️ Digite o produto.")

    elif escolha_tab3 == "🧮 Calculadora de Taxas & Lucro":
        nome_item = st.text_input("📦 Nome do item:", key="lucro_item")
        custo_prod = st.number_input("💸 Custo (R$):", min_value=0.0, value=50.0, step=1.0, key="lucro_custo")
        preco_venda = st.number_input("🏷️ Venda (R$):", min_value=0.0, value=120.0, step=1.0, key="lucro_venda")
        taxa_mkt = st.number_input("📊 Taxa plataforma (%):", min_value=0.0, value=16.0, step=0.5, key="lucro_taxa")

        if st.button("Calcular Lucro", key="btn_lucro"):
            if nome_item:
                val_taxa = preco_venda * (taxa_mkt / 100.0)
                lucro = preco_venda - custo_prod - val_taxa
                margem = (lucro / preco_venda) * 100 if preco_venda > 0 else 0
                rel_lucro = f"[Item]: {nome_item}\n[Lucro Líquido]: R$ {lucro:.2f}\n[Margem]: {margem:.1f}%"
                st.success("🧮 Cálculo realizado!")
                st.metric("Lucro Líquido Real", f"R$ {lucro:.2f}", f"{margem:.1f}% margem")
                st.text_area("Relatório:", rel_lucro, height=180, key="txt_lucro")
                salvar_historico_db(st.session_state.username, f"Lucro: {nome_item}")
                st.download_button("📥 Baixar Relatório (.txt)", rel_lucro, file_name="lucro.txt", mime="text/plain", key="dl_lucro")
            else:
                st.warning("⚠️ Digite o item.")

# =========================================================
# ABA 4: TRÁFEGO PAGO (NOVO MÓDULO DE ALTO IMPACTO)
# =========================================================
with tab4:
    st.subheader("🎯 Planejador de Tráfego Pago (Meta & Google Ads)")
    st.write("Estruture campanhas de anúncios profissionais focadas em ROI e conversão.")

    produto_trafego = st.text_input("📦 Produto a ser anunciado:", key="tr_prod")
    orcamento_diario = st.number_input("💵 Orçamento Diário Disponível (R$):", min_value=10.0, value=50.0, step=5.0, key="tr_orc")
    nicho = st.text_input("🏷️ Nicho de mercado (ex: Moda Fitness, Eletrônicos):", key="tr_nicho")

    if st.button("Gerar Estratégia de Tráfego", key="btn_trafego"):
        if produto_trafego and nicho:
            prompt_ia = f"Crie uma estratégia de tráfego pago completa (Meta Ads / Google Ads) para o produto '{produto_trafego}' no nicho '{nicho}' com orçamento diário de R$ {orcamento_diario:.2f}. Inclua: 1. Objetivo de campanha recomendado, 2. Segmentação de público detalhada e 3. Sugestão de criativo/copy para os anúncios."
            estrategia_trafego = gerar_resposta_ia("Você é um gestor de tráfego pago especialista em alta escala e ROAS positivo.", prompt_ia)

            if not estrategia_trafego:
                estrategia_trafego = f"""--- 🎯 ESTRATÉGIA DE TRÁFEGO PAGO ---
[Produto]: {produto_trafego} | [Nicho]: {nicho}
[Orçamento Diário]: R$ {orcamento_diario:.2f}
1. Objetivo: Conversão / Vendas diretas no site.
2. Público-Alvo: Interessados em {nicho}, idade 21-45 anos, compradores online.
3. Anúncio: Vídeo demonstrativo do {produto_trafego} com foco em benefício imediato."""

            st.success("🎯 Estratégia de tráfego gerada com sucesso!")
            st.text_area("Plano de Anúncios:", estrategia_trafego, height=280, key="txt_tr")
            salvar_historico_db(st.session_state.username, f"Tráfego: {produto_trafego}")
            st.download_button("📥 Baixar Plano de Tráfego (.txt)", estrategia_trafego, file_name=f"trafego_{produto_trafego}.txt", mime="text/plain", key="dl_tr")
        else:
            st.warning("⚠️ Preencha o produto e o nicho.")
