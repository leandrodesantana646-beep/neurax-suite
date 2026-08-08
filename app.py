import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="Neurax Business Suite - Pro",
    page_icon="⚡",
    layout="centered"
)

# --- URL DO SEU WEBHOOK ---
WEBHOOK_ASSINATURA_FIXO = "https://hook.us2.make.com/o7y6dcny8eujjx07vorwwj2rur58x971"

# Estilo CSS
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

# Gerenciamento de estado
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

# --- TELAS ---
if not st.session_state.logged_in:
    st.title("⚡ Neurax Business Suite")
    if st.session_state.auth_screen == 'login':
        st.subheader("🔑 Entrar na sua Conta")
        email = st.text_input("E-mail", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar", type="primary"):
            st.session_state.logged_in = True
            st.rerun()
    # (Adicione outras telas aqui se necessário)

else:
    st.title("⚡ Neurax Business Suite")
    menu = st.sidebar.selectbox("Navegação", ["💳 Assinatura & Planos", "💰 Precificação", "🚪 Sair"])

    if menu == "💳 Assinatura & Planos":
        st.header("💳 Assinatura Mensal")
        nome_assinante = st.text_input("Seu Nome")
        email_assinante = st.text_input("Seu E-mail")

        if st.button("Gerar Pix de Assinatura (R$ 19,99)", type="primary"):
            payload_sub = {
                "description": "Assinatura Mensal - Neurax Pro",
                "transaction_amount": 19.99,
                "payer": {"first_name": nome_assinante, "email": email_assinante}
            }
            with st.spinner("Gerando Pix..."):
                try:
                    response = requests.post(WEBHOOK_ASSINATURA_FIXO, json=payload_sub)
                    if response.status_code in [200, 201]:
                        st.success("Cobrança gerada!")
                        texto_res = response.text.strip()
                        if not texto_res or texto_res == "Accepted":
                            st.session_state.pix_data = {
                                "qr_code": "00020126580014br.gov.bcb.pix013612345678-1234-1234-1234-1234567890ab5204000053039865802BR5925Neurax Business6009Sao Paulo62070503***6304A1B2"
                            }
                        else:
                            try:
                                st.session_state.pix_data = response.json()
                            except:
                                st.session_state.pix_data = {"qr_code": texto_res}
                    else:
                        st.error(f"Erro: {response.status_code}")
                except Exception as e:
                    st.error(f"Erro: {e}")

        if st.session_state.pix_data:
            st.subheader("📲 Realize o Pagamento")
            st.code(st.session_state.pix_data.get("qr_code", ""), language="text")
            if st.button("Já paguei! Liberar Conta"):
                st.session_state.is_pro = True
                st.success("Conta Liberada!")
                st.balloons()
