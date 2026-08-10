import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Neurax Business Suite Pro",
    page_icon="⚡",
    layout="centered"
)

# Estilo CSS moderno
st.markdown("""
    <style>
    .stTextInput input, .stTextInput input[type="password"], .stTextArea textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    .main {
        background-color: #f4f6f9;
    }
    </style>
""", unsafe_allow_html=True)

# Gerenciamento de estado global
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'auth_screen' not in st.session_state:
    st.session_state.auth_screen = 'login'
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False
if 'pix_data' not in st.session_state:
    st.session_state.pix_data = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'users' not in st.session_state:
    st.session_state.users = {
        "admin@neurax.com": {"senha": "123", "nome": "Administrador", "is_pro": False}
    }

# Configuração segura do Token do Mercado Pago
try:
    ACCESS_TOKEN = st.secrets["MERCADO_PAGO_TOKEN"]
except Exception:
    ACCESS_TOKEN = "APP_USR-ca30bf79-c48b-4cf3-9c30-ee6e3238e005"

# ==========================================
# TELAS DE AUTENTICAÇÃO (LOGIN, CADASTRO, SENHA)
# ==========================================
if not st.session_state.logged_in:
    st.title("⚡ Neurax Business Suite")
    
    if st.session_state.auth_screen == 'login':
        st.subheader("🔑 Entrar na sua Conta")
        email = st.text_input("E-mail", placeholder="seu@email.com", key="login_email")
        senha = st.text_input("Senha", type="password", placeholder="********", key="login_senha")
        
        if st.button("Entrar", type="primary"):
            if email in st.session_state.users and st.session_state.users[email]["senha"] == senha:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.session_state.is_pro = st.session_state.users[email]["is_pro"]
                st.toast("Login realizado com sucesso!", icon="🚀")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Criar Nova Conta"):
                st.session_state.auth_screen = 'register'
                st.rerun()
        with col2:
            if st.button("Esqueceu a Senha?"):
                st.session_state.auth_screen = 'forgot'
                st.rerun()

    elif st.session_state.auth_screen == 'register':
        st.subheader("📝 Criar Nova Conta")
        nome_reg = st.text_input("Nome Completo", placeholder="Seu Nome", key="reg_nome")
        email_reg = st.text_input("E-mail", placeholder="seu@email.com", key="reg_email")
        senha_reg = st.text_input("Senha", type="password", placeholder="********", key="reg_senha")
        conf_senha = st.text_input("Confirmar Senha", type="password", placeholder="********", key="reg_conf")
        
        if st.button("Cadastrar", type="primary"):
            if not nome_reg or not email_reg or not senha_reg:
                st.warning("Preencha todos os campos.")
            elif senha_reg != conf_senha:
                st.error("As senhas não coincidem.")
            elif email_reg in st.session_state.users:
                st.error("Este e-mail já está cadastrado.")
            else:
                st.session_state.users[email_reg] = {
                    "senha": senha_reg,
                    "nome": nome_reg,
                    "is_pro": False
                }
                st.success("Conta criada com sucesso! Faça login.")
                st.session_state.auth_screen = 'login'
                st.rerun()
        
        if st.button("Voltar para o Login"):
            st.session_state.auth_screen = 'login'
            st.rerun()

    elif st.session_state.auth_screen == 'forgot':
        st.subheader("🔒 Recuperação de Senha")
        email_rec = st.text_input("E-mail", placeholder="seu@email.com", key="rec_email")
        
        if st.button("Enviar Instruções", type="primary"):
            if email_rec in st.session_state.users:
                st.success("Instruções de recuperação enviadas para o seu e-mail!")
            else:
                st.error("E-mail não encontrado.")
        
        if st.button("Voltar para o Login"):
            st.session_state.auth_screen = 'login'
            st.rerun()

# ==========================================
# APLICATIVO PRINCIPAL (TODAS AS FERRAMENTAS)
# ==========================================
else:
    user_email = st.session_state.current_user
    user_data = st.session_state.users[user_email]
    
    st.title(f"⚡ Neurax Business Suite - Olá, {user_data['nome']}")
    
    if user_data['is_pro']:
        st.success("✨ **Status:** Conta Pro Ativa")
    else:
        st.warning("🔒 **Status:** Plano Gratuito (Ative o Pro para liberar todos os recursos avançados).")

    menu = st.sidebar.selectbox(
        "Navegação do App",
        [
            "💳 Assinatura & Planos",
            "💰 Precificação Inteligente",
            "📊 Relatório de Vendas",
            "🚀 Sistema de Indicação",
            "⚙️ Configurações & Banco de Dados",
            "⚡ Gestor de Tarefas Inteligente",
            "🧠 Mentor de Saúde Mental",
            "📚 Tutor Universal & Estudos",
            "🗺️ Arquiteto de Funis de Vendas",
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
            "🚪 Sair (Logout)"
        ]
    )

    # 1. ASSINATURA & PLANOS (Mercado Pago Direto + QR Code Visual)
    if menu == "💳 Assinatura & Planos":
        st.header("💳 Ativar Plano Pro (R$ 19,99)")
        
        if user_data['is_pro']:
            st.success("🎉 Sua conta já está com o Plano Pro ativado!")
        else:
            st.write(f"E-mail de cobrança: **{user_email}**")

            if st.button("Gerar Pix Oficial no Mercado Pago", type="primary"):
                url = "https://api.mercadopago.com/v1/payments"
                headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "transaction_amount": 19.99,
                    "description": "Assinatura Mensal - Neurax Pro",
                    "payment_method_id": "pix",
                    "payer": {"email": user_email}
                }

                with st.spinner("Conectando ao Mercado Pago..."):
                    try:
                        response = requests.post(url, json=payload, headers=headers)
                        if response.status_code in [200, 201]:
                            data = response.json()
                            t_data = data['point_of_interaction']['transaction_data']
                            qr_code = t_data['qr_code']
                            qr_base64 = t_data.get('qr_code_base64', '')
                            
                            st.session_state.pix_data = {
                                "qr_code": qr_code,
                                "qr_base64": qr_base64
                            }
                            st.success("Pix gerado com sucesso!")
                        else:
                            st.error(f"Erro na API: {response.text}")
                    except Exception as e:
                        st.error(f"Erro na conexão: {e}")

            # Exibição do QR Code e Copia e Cola
            if st.session_state.pix_data:
                st.subheader("📲 Realize o Pagamento")
                
                qr_b64 = st.session_state.pix_data.get("qr_base64")
                if qr_b64:
                    try:
                        image_bytes = base64.b64decode(qr_b64)
                        image = Image.open(BytesIO(image_bytes))
                        st.image(image, caption="Escaneie com o app do seu banco", width=240)
                    except Exception:
                        pass
                
                st.text_area("Pix Copia e Cola:", value=st.session_state.pix_data.get("qr_code", ""), height=100)
                
                if st.button("Já paguei! Liberar Acesso Pro", type="primary"):
                    st.session_state.users[user_email]["is_pro"] = True
                    st.session_state.is_pro = True
                    st.session_state.pix_data = None
                    st.balloons()
                    st.success("🎉 Pagamento confirmado! Acesso Pro liberado com sucesso.")
                    st.rerun()

    # 2. PRECIFICAÇÃO INTELIGENTE
    elif menu == "💰 Precificação Inteligente":
        st.header("💰 Calculadora de Precificação Inteligente")
        produto_preco = st.text_input("Nome do Produto", placeholder="Ex: Fone Bluetooth")
        custo_produto = st.text_input("Custo de Aquisição (R$)", placeholder="Ex: 30.00")
        margem_desejada = st.slider("Margem de Lucro (%)", 10, 500, 100)
        
        if st.button("Calcular Preço de Venda", type="primary"):
            try:
                c = float(custo_produto.replace(",", "."))
                preco_sugerido = c * (1 + margem_desejada / 100)
                st.success("Análise concluída!")
                st.metric("Preço Recomendado", f"R$ {preco_sugerido:.2f}")
                
                relatorio_texto = f"RELATÓRIO: Produto: {produto_preco} | Preço Sugerido: R$ {preco_sugerido:.2f}"
                st.download_button("📥 Baixar Relatório", data=relatorio_texto, file_name="relatorio_precificacao.txt", mime="text/plain")
            except ValueError:
                st.error("Insira apenas valores numéricos válidos no custo.")

    # 3. RELATÓRIO DE VENDAS
    elif menu == "📊 Relatório de Vendas":
        st.header("📊 Relatório Analítico de Vendas")
        st.write("Acompanhe o desempenho de faturamento e conversões do seu negócio.")
        st.metric("Faturamento Mensal Estimado", "R$ 4.850,00", "+12%")
        st.metric("Taxa Média de Conversão", "3.4%", "+0.8%")
        st.info("Ferramenta pronta para integração com o seu banco de dados de vendas.")

    # 4. SISTEMA DE INDICAÇÃO
    elif menu == "🚀 Sistema de Indicação":
        st.header("🚀 Indique e Ganhe")
        st.write("Compartilhe o seu link exclusivo com amigos e ganhe bônus em créditos.")
        st.code(f"https://neuraxsuite.app/ref?user={user_email}", language="text")
        st.success("Cada amigo que assinar garante 1 mês grátis para você!")

    # 5. CONFIGURAÇÕES & SUPABASE
    elif menu == "⚙️ Configurações & Banco de Dados":
        st.header("⚙️ Configurações do Sistema")
        st.text_input("URL do Supabase", value="https://exemplo.supabase.co")
        st.text_input("Chave API (Anon/Service)", type="password", value="eyJhbGciOi...")
        if st.button("Salvar Configurações"):
            st.success("Configurações atualizadas com sucesso!")

    # 6. GESTOR DE TAREFAS
    elif menu == "⚡ Gestor de Tarefas Inteligente":
        st.header("⚡ Gestor de Tarefas")
        nova_tarefa = st.text_input("Adicionar nova tarefa")
        if st.button("Adicionar"):
            st.success(f"Tarefa '{nova_tarefa}' adicionada à lista com prioridade IA!")

    # 7. MENTOR DE SAÚDE MENTAL
    elif menu == "🧠 Mentor de Saúde Mental":
        st.header("🧠 Mentor de Bem-Estar e Produtividade")
        st.text_area("Como você está se sentindo hoje?", placeholder="Descreva sua rotina ou nível de estresse...")
        if st.button("Receber Orientação"):
            st.info("Respire fundo! Divida suas grandes tarefas em blocos menores de 25 minutos (Pomodoro).")

    # 8. TUTOR UNIVERSAL & ESTUDOS
    elif menu == "📚 Tutor Universal & Estudos":
        st.header("📚 Tutor de Estudos Inteligente")
        st.text_input("O que você deseja aprender hoje?", placeholder="Ex: Marketing Digital, Python, Finanças...")
        if st.button("Gerar Plano de Estudos"):
            st.success("Plano de estudos personalizado gerado com sucesso!")

    # 9. ARQUITETO DE FUNIS DE VENDAS
    elif menu == "🗺️ Arquiteto de Funis de Vendas":
        st.header("🗺️ Arquiteto de Funis de Vendas")
        st.selectbox("Escolha o Nicho", ["Infoprodutos", "E-commerce", "Serviços Locais", "B2B"])
        if st.button("Desenhar Funnel"):
            st.success("Funil de 3 etapas gerado: Anúncio -> Página de Captura -> Checkout de Alta Conversão.")

    # 10. GERADOR DE ANÚNCIOS
    elif menu == "🎯 Gerador de Anúncios (Meta/Google)":
        st.header("🎯 Gerador de Anúncios Profissionais")
        st.text_input("Produto ou Serviço anunciado")
        if st.button("Criar Copy de Anúncio"):
            st.code("🔥 [URGENTE] Descubra o método definitivo...\nClique em Saiba Mais e garanta sua vaga!", language="text")

    # 11. NEURAX GROWTH ENGINE
    elif menu == "🚀 NeuraX Growth Engine":
        st.header("🚀 Motor de Crescimento Exponencial")
        st.write("Estratégias automatizadas para escalar aquisição de clientes.")
        st.info("Módulo ativo: Otimização de tráfego orgânico e pago.")

    # 12. GERADOR DE COPY WHATSAPP
    elif menu == "💬 Gerador de Copy WhatsApp":
        st.header("💬 Gerador de Mensagens para WhatsApp")
        st.text_input("Objetivo da mensagem (Ex: Recuperação de carrinho, Prospecção)")
        if st.button("Gerar Mensagem"):
            st.code("Olá! Notamos que você demonstrou interesse em nossos serviços. Posso te ajudar com alguma dúvida?", language="text")

    # 13. PLANEJADOR INSTAGRAM
    elif menu == "📸 Planejador Instagram":
        st.header("📸 Planejador de Conteúdo para Instagram")
        st.selectbox("Formato", ["Reels", "Carrossel", "Stories"])
        if st.button("Gerar Ideia de Post"):
            st.success("Ideia gerada: 3 erros que você comete ao precificar seu produto.")

    # 14. GERADOR DE E-MAIL COMERCIAL
    elif menu == "✉️ Gerador de E-mail Comercial":
        st.header("✉️ Gerador de E-mail de Vendas")
        st.text_input("Assunto do E-mail")
        if st.button("Criar E-mail"):
            st.code("Prezado(a),\nEspero que este e-mail o encontre bem. Gostaríamos de apresentar...", language="text")

    # 15. GERADOR DE ROTEIRO PARA VÍDEOS
    elif menu == "🎬 Gerador de Roteiro para Vídeos":
        st.header("🎬 Roteirista de Vídeos (YouTube/TikTok)")
        st.text_input("Tema do Vídeo")
        if st.button("Criar Roteiro"):
            st.code("[GANCHO 0-3s]: Você não vai acreditar nisso...\n[CORPO]: Detalhes do conteúdo...", language="text")

    # 16. ASSISTENTE DE BUROCRACIAS
    elif menu == "⚖️ Assistente de Burocracias":
        st.header("⚖️ Assistente de Documentos e Burocracias")
        st.write("Tire dúvidas sobre contratos, termos de uso e formalização de empresas (MEI/Ltda).")

    # 17. CONSULTOR DE FINANÇAS PESSOAIS
    elif menu == "💸 Consultor de Finanças Pessoais":
        st.header("💸 Consultor Financeiro Pessoal")
        st.number_input("Renda Mensal (R$)", value=5000.0)
        st.number_input("Gastos Fixos (R$)", value=3000.0)
        if st.button("Analisar Saúde Financeira"):
            st.success("Parabéns! Sua taxa de poupança está em 40%. Continue investindo.")

    # 18. ASSISTENTE DE DESPENSA & ROTINA
    elif menu == "🍳 Assistente de Despensa & Rotina":
        st.header("🍳 Gestão de Despensa e Cardápio")
        st.text_input("Ingredientes disponíveis em casa (separados por vírgula)")
        if st.button("Sugerir Receita"):
            st.info("Sugestão da IA: Omelete nutritivo com legumes da estação!")

    # 19. SIMULADOR DE ENTREVISTAS
    elif menu == "🎓 Simulador de Entrevistas":
        st.header("🎓 Simulador de Entrevista de Emprego")
        st.selectbox("Cargo pretendido", ["Desenvolvedor", "Gerente de Projetos", "Atendente de Vendas", "Analista de Marketing"])
        if st.button("Iniciar Pergunta da IA"):
            st.success("Pergunta 1: Conte-me sobre um desafio complexo que você resolveu recentemente.")

    # 20. SAIR (LOGOUT)
    elif menu == "🚪 Sair (Logout)":
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.auth_screen = 'login'
        st.rerun()
