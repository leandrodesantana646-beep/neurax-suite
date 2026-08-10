import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Neurax Business Suite", page_icon="⚡", layout="centered")

# Estilo para manter o input legível
st.markdown("""
    <style>
    .stTextInput input { color: #000000 !important; background-color: #ffffff !important; }
    .main { background-color: #f4f6f9; }
    </style>
""", unsafe_allow_html=True)

# Inicialização de Estados
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'pix_data' not in st.session_state: st.session_state.pix_data = None

# SEU TOKEN (Coloque seu token aqui)
ACCESS_TOKEN = "APP_USR-ca30bf79-c48b-4cf3-9c30-ee6e3238e005"

# --- TELA DE LOGIN ---
if not st.session_state.logged_in:
    st.title("⚡ Neurax Business Suite")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar", type="primary"):
        st.session_state.logged_in = True
        st.rerun()

# --- ÁREA LOGADA ---
else:
    st.title("⚡ Neurax Business Suite")
    menu = st.sidebar.selectbox("Navegação", ["💳 Assinatura & Planos", "🚪 Sair"])

    if menu == "💳 Assinatura & Planos":
        st.header("💳 Ativar Plano Pro (R$ 19,99)")
        nome_assinante = st.text_input("Seu Nome")
        email_assinante = st.text_input("Seu E-mail")

        if st.button("Gerar Pix de Assinatura Real", type="primary"):
            if not email_assinante:
                st.warning("Preencha o campo e-mail.")
            else:
                url = "https://api.mercadopago.com/v1/payments"
                headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "transaction_amount": 19.99,
                    "description": "Assinatura Mensal - Neurax Pro",
                    "payment_method_id": "pix",
                    "payer": {"email": email_assinante}
                }

                with st.spinner("Conectando ao Mercado Pago..."):
                    try:
                        response = requests.post(url, json=payload, headers=headers)
                        
                        if response.status_code in [200, 201]:
                            data = response.json()
                            # Extração correta do QR Code da resposta da API
                            qr_code = data['point_of_interaction']['transaction_data']['qr_code']
                            st.session_state.pix_data = {"qr_code": qr_code}
                            st.success("Pix gerado com sucesso!")
                        else:
                            st.error(f"Erro na API: {response.text}")
                    except Exception as e:
                        st.error(f"Erro na conexão: {e}")

        # Exibição do Pix
        if st.session_state.pix_data:
            st.subheader("📲 Código Copia e Cola")
            st.code(st.session_state.pix_data.get("qr_code", ""), language="text")
            st.info("Copie o código acima e cole no seu banco.")
            
            if st.button("Já paguei! Liberar Acesso"):
                st.balloons()
                st.success("🎉 Pagamento confirmado! Acesso Pro liberado.")
                st.session_state.pix_data = None # Limpa para gerar novo se precisar

    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.session_state.pix_data = None
        st.rerun()
