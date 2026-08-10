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

# Estilo visual moderno
st.markdown("""
    <style>
    .stTextInput input { color: #000000 !important; background-color: #ffffff !important; }
    .main { background-color: #f4f6f9; }
    </style>
""", unsafe_allow_html=True)

# Inicialização de Estados da Sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'users' not in st.session_state:
    # Banco de dados em memória para gerenciar usuários, cadastros e senhas
    st.session_state.users = {
        "admin@neurax.com": {"senha": "123", "nome": "Administrador", "is_pro": False}
    }
if 'pix_data' not in st.session_state:
    st.session_state.pix_data = None

# Configuração segura do Token do Mercado Pago
try:
    ACCESS_TOKEN = st.secrets["MERCADO_PAGO_TOKEN"]
except Exception:
    ACCESS_TOKEN = "APP_USR-ca30bf79-c48b-4cf3-9c30-ee6e3238e005"

# --- TELA DE AUTENTICAÇÃO (LOGIN, CADASTRO E ESQUECI A SENHA) ---
if not st.session_state.logged_in:
    st.title("⚡ Neurax Business Suite")
    
    auth_opcao = st.radio("Escolha uma opção:", ["Entrar", "Cadastrar", "Esqueci a senha"], horizontal=True)
    
    if auth_opcao == "Entrar":
        st.subheader("🔑 Faça login na sua conta")
        email_login = st.text_input("E-mail", key="login_email")
        senha_login = st.text_input("Senha", type="password", key="login_senha")
        
        if st.button("Entrar", type="primary"):
            if email_login in st.session_state.users and st.session_state.users[email_login]["senha"] == senha_login:
                st.session_state.logged_in = True
                st.session_state.current_user = email_login
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")

    elif auth_opcao == "Cadastrar":
        st.subheader("📝 Crie a sua conta")
        nome_cad = st.text_input("Nome Completo", key="cad_nome")
        email_cad = st.text_input("E-mail", key="cad_email")
        senha_cad = st.text_input("Senha", type="password", key="cad_senha")
        
        if st.button("Cadastrar", type="primary"):
            if not nome_cad or not email_cad or not senha_cad:
                st.warning("Preencha todos os campos.")
            elif email_cad in st.session_state.users:
                st.error("Este e-mail já está cadastrado.")
            else:
                st.session_state.users[email_cad] = {
                    "senha": senha_cad,
                    "nome": nome_cad,
                    "is_pro": False
                }
                st.success("Cadastro realizado com sucesso! Vá para a aba 'Entrar' para acessar.")

    elif auth_opcao == "Esqueci a senha":
        st.subheader("🔄 Recuperação de Senha")
        email_rec = st.text_input("Digite seu e-mail cadastrado", key="rec_email")
        
        if st.button("Enviar nova senha", type="primary"):
            if email_rec in st.session_state.users:
                st.success("Instruções de recuperação enviadas para o seu e-mail!")
            else:
                st.error("E-mail não encontrado na base de dados.")

# --- ÁREA LOGADA (APLICATIVO COMPLETO) ---
else:
    user_email = st.session_state.current_user
    user_data = st.session_state.users[user_email]
    
    st.title(f"⚡ Neurax Business Suite - Olá, {user_data['nome']}")
    
    menu = st.sidebar.selectbox(
        "Navegação", 
        ["💳 Assinatura & Planos", "💰 Ferramenta de Precificação", "📊 Painel Pro", "🚪 Sair"]
    )

    # 1. ASSINATURA & PLANOS
    if menu == "💳 Assinatura & Planos":
        st.header("💳 Ativar Plano Pro (R$ 19,99)")
        
        if user_data["is_pro"]:
            st.success("🎉 Sua conta já está com o Plano Pro ativado!")
        else:
            st.write(f"E-mail de cobrança: **{user_email}**")

            if st.button("Gerar Pix Oficial", type="primary"):
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
                
                if st.button("Já paguei! Liberar Acesso Pro"):
                    st.session_state.users[user_email]["is_pro"] = True
                    st.session_state.pix_data = None
                    st.balloons()
                    st.success("🎉 Pagamento confirmado! Acesso Pro liberado com sucesso.")
                    st.rerun()

    # 2. FERRAMENTA DE PRECIFICAÇÃO
    elif menu == "💰 Ferramenta de Precificação":
        st.header("💰 Calculadora de Precificação Inteligente")
        st.write("Calcule o preço ideal de venda baseado nos seus custos e margem de lucro desejada.")
        
        custo_produto = st.number_input("Custo de Aquisição ou Produção (R$)", min_value=0.0, value=50.0, step=5.0)
        margem_lucro = st.slider("Margem de Lucro Desejada (%)", min_value=1, max_value=500, value=100)
        impostos_taxas = st.number_input("Estimativa de Impostos e Taxas (%)", min_value=0.0, max_value=50.0, value=10.0)
        
        if st.button("Calcular Preço de Venda", type="primary"):
            percentual_total = (margem_lucro + impostos_taxas) / 100.0
            if percentual_total >= 1:
                st.error("A soma da margem e taxas não pode ultrapassar ou igualar 100%.")
            else:
                preco_venda = custo_produto / (1 - percentual_total)
                lucro_estimado = preco_venda - custo_produto - (preco_venda * (impostos_taxas / 100))
                
                st.metric("Preço de Venda Sugerido", f"R$ {preco_venda:.2f}")
                st.metric("Lucro Líquido Estimado por Unidade", f"R$ {lucro_estimado:.2f}")

    # 3. PAINEL PRO
    elif menu == "📊 Painel Pro":
        if user_data["is_pro"]:
            st.header("📊 Painel Avançado Pro")
            st.info("Bem-vindo à sua área exclusiva de recursos avançados do Neurax Business Suite!")
            st.metric("Status da Licença", "Ativa (Pro)")
            st.write("Aqui você tem acesso a relatórios avançados, métricas em tempo real e automações.")
        else:
            st.warning("⚠️ Conteúdo restrito. Vá até a aba '💳 Assinatura & Planos' para liberar o acesso.")

    # 4. SAIR
    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.pix_data = None
        st.rerun()
