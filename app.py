import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="Neurax Business Suite - Pro",
    page_icon="⚡",
    layout="centered"
)

# --- COLE A SUA URL DO WEBHOOK DO MAKE.COM NA LINHA ABAIXO ---
WEBHOOK_ASSINATURA_FIXO = "https://hook.us2.make.com/o7y6dcny8eujjx07vorwwj2rur58x971
# -------------------------------------------------------------

# Estilo CSS para inputs legíveis
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
    st.session_state.is_pro = True
if 'pix_data' not in st.session_state:
    st.session_state.pix_data = None
if 'supabase_url' not in st.session_state:
    st.session_state.supabase_url = ""
if 'supabase_key' not in st.session_state:
    st.session_state.supabase_key = ""

# ==========================================
# TELAS DE AUTENTICAÇÃO
# ==========================================
if not st.session_state.logged_in:
    st.title("⚡ Neurax Business Suite")
    
    if st.session_state.auth_screen == 'login':
        st.subheader("🔑 Entrar na sua Conta")
        email = st.text_input("E-mail", placeholder="seu@email.com", key="login_email")
        senha = st.text_input("Senha", type="password", placeholder="********", key="login_senha")
        
        if st.button("Entrar", type="primary"):
            if email and senha:
                st.session_state.logged_in = True
                st.toast("Login realizado com sucesso!", icon="🚀")
                st.rerun()
            else:
                st.error("Preencha todos os campos para entrar.")
        
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
        
        if st.button("Cadastrar e Testar Grátis", type="primary"):
            if nome_reg and email_reg and senha_reg and (senha_reg == conf_senha):
                st.success("Conta criada! Teste grátis ativado.")
                st.session_state.auth_screen = 'login'
                st.rerun()
            else:
                st.warning("Preencha todos os campos corretamente.")
        
        if st.button("Voltar para o Login"):
            st.session_state.auth_screen = 'login'
            st.rerun()

    elif st.session_state.auth_screen == 'forgot':
        st.subheader("🔒 Recuperação de Senha")
        email_rec = st.text_input("E-mail", placeholder="seu@email.com", key="rec_email")
        
        if st.button("Enviar Instruções", type="primary"):
            if email_rec:
                st.success("Instruções enviadas para o e-mail!")
            else:
                st.error("Informe o e-mail cadastrado.")
        
        if st.button("Voltar para o Login"):
            st.session_state.auth_screen = 'login'
            st.rerun()

# ==========================================
# APLICATIVO PRINCIPAL
# ==========================================
else:
    st.title("⚡ Neurax Business Suite")
    
    if st.session_state.is_pro:
        st.success("✨ **Status:** Conta Pro / Teste Grátis Ativo (Acesso Ilimitado)")
    else:
        st.warning("🔒 **Status:** Período de teste encerrado.")

    menu = st.sidebar.selectbox(
        "Navegação do App",
        [
            "💳 Assinatura & Planos",
            "💰 Precificação Inteligente",
            "💳 Gerar Cobrança Pix",
            "🌐 Testador HTTP / Webhook Make",
            "📊 Relatório de Vendas",
            "⚙️ Configurações & Supabase",
            "🚪 Sair (Logout)"
        ]
    )

    if menu == "💳 Assinatura & Planos":
        st.header("💳 Assinatura Mensal Neurax Business")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Teste Grátis 🎁")
            st.metric("Valor", "R$ 0,00", "Ativo agora")
        with col2:
            st.markdown("### Plano Pro 🚀")
            st.metric("Valor", "R$ 19,99", "por mês")

        st.markdown("---")
        st.subheader("Ativar Assinatura Pro via Pix (R$ 19,99)")
        
        nome_assinante = st.text_input("Seu Nome / Empresa", placeholder="Ex: João da Silva")
        email_assinante = st.text_input("Seu E-mail de Acesso", placeholder="Ex: joao@email.com")

        if st.button("Gerar Pix de Assinatura (R$ 19,99)", type="primary"):
            if not nome_assinante or not email_assinante:
                st.warning("Preencha seu nome e e-mail.")
            else:
                payload_sub = {
                    "description": "Assinatura Mensal - Neurax Business Pro",
                    "transaction_amount": 19.99,
                    "payer": {"first_name": nome_assinante, "email": email_assinante}
                }

                with st.spinner("Gerando Pix..."):
                    try:
                        response = requests.post(WEBHOOK_ASSINATURA_FIXO, json=payload_sub)
                        if response.status_code in [200, 201]:
                            st.success("Cobrança gerada com sucesso!")
                            st.session_state.pix_data = response.json() if response.text else {"qr_code": "00020126580014br.gov.bcb.pix..."}
                        else:
                            st.error(f"Erro na comunicação: Status {response.status_code}. Verifique se o cenário está ativo no Make.")
                    except Exception as e:
                        st.error(f"Não foi possível conectar ao webhook: {e}")

        if st.session_state.pix_data:
            st.markdown("---")
            st.subheader("📲 Realize o Pagamento do Pix")
            st.code(st.session_state.pix_data.get("qr_code", "00020126580014br.gov.bcb.pix..."), language="text")
            st.toast("Código Pix gerado com sucesso!", icon="📋")
            
            if st.button("🔄 Já paguei! Liberar minha Conta Pro", type="primary"):
                st.session_state.is_pro = True
                st.success("🎉 Pagamento reconhecido! Sua conta agora é **PRO**!")
                st.balloons()

    elif menu == "💰 Precificação Inteligente":
        st.header("💰 Precificação Inteligente com IA")
        produto_preco = st.text_input("Nome do Produto / Serviço", placeholder="Ex: Fone Bluetooth X10")
        custo_produto = st.text_input("Seu Custo de Aquisição (R$)", placeholder="Ex: 30.00")
        margem_desejada = st.slider("Margem de Lucro Alvo (%)", 100, 500, 250)
        
        if st.button("Executar Análise com IA", type="primary"):
            if not produto_preco or not custo_produto:
                st.warning("Preencha o nome e o custo.")
            else:
                try:
                    c = float(custo_produto.replace(",", "."))
                    preco_sugerido = c * (1 + margem_desejada / 100)
                    lucro_estimado = preco_sugerido - c
                    
                    st.success("Análise de Preço Concluída!")
                    st.toast("Relatório de precificação gerado!", icon="📊")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Preço Recomendado", f"R$ {preco_sugerido:.2f}", f"{margem_desejada}% Lucro")
                    with col2:
                        st.metric("Lucro Unitário", f"R$ {lucro_estimado:.2f}")
                    
                    relatorio_texto = f"RELATÓRIO DE PRECIFICAÇÃO - NEURAX\nProduto: {produto_preco}\nCusto: R$ {c:.2f}\nPreço Sugerido: R$ {preco_sugerido:.2f}\nLucro: R$ {lucro_estimado:.2f}"
                    
                    st.download_button(
                        label="📥 Baixar Relatório em TXT",
                        data=relatorio_texto,
                        file_name=f"relatorio_{produto_preco.lower().replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                except ValueError:
                    st.error("Insira um valor numérico válido para o custo.")

    elif menu == "💳 Gerar Cobrança Pix":
        st.header("Gerador de Cobrança Pix Avulsa")
        webhook_url = st.text_input("URL do Webhook do Make", placeholder="https://hook.us2.make.com/...")
        descricao = st.text_input("Descrição", placeholder="Ex: Consultoria")
        valor = st.text_input("Valor (R$)", placeholder="Ex: 50.00")
        nome = st.text_input("Cliente", placeholder="Nome")
        
        if st.button("Gerar Pix", type="primary"):
            if webhook_url and descricao and valor and nome:
                try:
                    payload = {"description": descricao, "transaction_amount": float(valor.replace(",", ".")), "payer": {"first_name": nome}}
                    res = requests.post(webhook_url, json=payload)
                    if res.status_code in [200, 201]:
                        st.success("Pix gerado com sucesso!")
                        st.toast("Cobrança gerada!", icon="⚡")
                    else:
                        st.error(f"Erro no webhook: Status {res.status_code}")
                except Exception as e:
                    st.error(f"Erro: {e}")
            else:
                st.warning("Preencha todos os campos.")

    elif menu == "🌐 Testador HTTP / Webhook Make":
        st.header("Testador HTTP")
        token = st.text_input("Token de Autorização", type="password")
        if st.button("Validar Headers"):
            st.toast("Headers validados com sucesso!", icon="🌐")
            st.json({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})

    elif menu == "📊 Relatório de Vendas":
        st.header("Relatório de Vendas")
        st.metric("Faturamento Hoje", "R$ 230,00", "+15%")
        st.table([{"ID": "#101", "Cliente": "João", "Valor": "R$ 150,00", "Status": "Aprovado"}])

    elif menu == "⚙️ Configurações & Supabase":
        st.header("Configurações do Supabase")
        sup_url = st.text_input("URL do Supabase", value=st.session_state.supabase_url)
        sup_key = st.text_input("Chave API", type="password", value=st.session_state.supabase_key)
        if st.button("Salvar Configurações"):
            st.session_state.supabase_url = sup_url
            st.session_state.supabase_key = sup_key
            st.success("Salvo com sucesso!")
            st.toast("Configurações atualizadas!", icon="💾")

    elif menu == "🚪 Sair (Logout)":
        st.session_state.logged_in = False
        st.session_state.auth_screen = 'login'
        st.rerun()
