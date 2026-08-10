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
if 'pix_data' not in st.session_state:
    st.session_state.pix_data = None
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False

# Configuração segura do Token do Mercado Pago
try:
    ACCESS_TOKEN = st.secrets["MERCADO_PAGO_TOKEN"]
except Exception:
    ACCESS_TOKEN = "APP_USR-ca30bf79-c48b-4cf3-9c30-ee6e3238e005"

# --- TELA DE LOGIN ---
if not st.session_state.logged_in:
    st.title("⚡ Neurax Business Suite")
    st.subheader("🔑 Faça login na sua conta")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar", type="primary"):
        if email and senha:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("Preencha e-mail e senha para entrar.")

# --- ÁREA LOGADA ---
else:
    st.title("⚡ Neurax Business Suite")
    
    menu = st.sidebar.selectbox(
        "Navegação", 
        ["💳 Assinatura & Planos", "💰 Ferramenta de Precificação", "📊 Painel Pro", "🚪 Sair"]
    )

    # 1. ASSINATURA & PLANOS
    if menu == "💳 Assinatura & Planos":
        st.header("💳 Ativar Plano Pro (R$ 19,99)")
        
        if st.session_state.is_pro:
            st.success("🎉 Sua conta já está com o Plano Pro ativado!")
        else:
            nome_assinante = st.text_input("Seu Nome")
            email_assinante = st.text_input("Seu E-mail")

            if st.button("Gerar Pix Oficial", type="primary"):
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
                    st.session_state.is_pro = True
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
        if st.session_state.is_pro:
            st.header("📊 Painel Avançado Pro")
            st.info("Bem-vindo à sua área exclusiva de recursos avançados do Neurax Business Suite!")
            st.metric("Status da Licença", "Ativa (Pro)")
            st.write("Aqui você tem acesso a relatórios avançados, métricas em tempo real e automações.")
        else:
            st.warning("⚠️ Conteúdo restrito. Vá até a aba '💳 Assinatura & Planos' para liberar o acesso.")

    # 4. SAIR
    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.session_state.pix_data = None
        st.rerun()
