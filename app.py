import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="Neurax Business Suite",
    page_icon="⚡",
    layout="centered"
)

# Estilo CSS para garantir letras pretas e fundo legível nos inputs
st.markdown("""
    <style>
    .stTextInput input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    .main {
        background-color: #f4f6f9;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Neurax Business Suite")
st.write("Sua plataforma completa de lucro, automação e vendas via Pix.")

# Menu de navegação lateral para alternar entre as ferramentas
menu = st.sidebar.radio("Ferramentas", ["💳 Gerar Pix", "📊 Relatório de Vendas", "🚀 Indicação & Parcerias"])

if menu == "💳 Gerar Pix":
    st.header("Gerador de Cobrança Pix")
    st.write("Integração direta com o Make e Mercado Pago.")
    
    webhook_url = st.text_input("URL do Webhook do Make", placeholder="https://hook.us2.make.com/...")
    descricao = st.text_input("Descrição do Produto", placeholder="Ex: Consultoria Neurax")
    valor = st.text_input("Valor (R$)", placeholder="Ex: 10.00")
    nome = st.text_input("Nome do Cliente", placeholder="Ex: João Silva")
    email = st.text_input("E-mail do Cliente", placeholder="Ex: cliente@email.com")

    if st.button("Gerar Cobrança Pix", type="primary"):
        if not webhook_url:
            st.error("Insira a URL do Webhook do Make.")
        elif not descricao or not valor or not nome:
            st.warning("Preencha todos os campos obrigatórios.")
        else:
            try:
                valor_tratado = float(valor.replace(",", "."))
            except ValueError:
                st.error("O valor deve ser numérico (ex: 10.00).")
                st.stop()

            payload = {
                "description": descricao,
                "transaction_amount": valor_tratado,
                "payer": {
                    "first_name": nome,
                    "email": email if email else "cliente@email.com"
                }
            }

            with st.spinner("Enviando dados para o Make..."):
                try:
                    response = requests.post(webhook_url, json=payload)
                    if response.status_code in [200, 201]:
                        st.success("Cobrança gerada e integrada com sucesso!")
                        st.json(response.json() if response.text else {"status": "Sucesso"})
                    else:
                        st.error(f"Erro na comunicação: Status {response.status_code}")
                        st.text(response.text)
                except Exception as e:
                    st.error(f"Não foi possível conectar ao webhook: {e}")

elif menu == "📊 Relatório de Vendas":
    st.header("Relatório Automático de Vendas")
    st.write("Acompanhe o faturamento e o fluxo de caixa em tempo real.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Faturamento Hoje", value="R$ 230,00", delta="+15%")
    with col2:
        st.metric(label="Pix Gerados", value="4", delta="1 pendente")

    st.markdown("### Últimas Transações")
    dados_vendas = [
        {"Cliente": "João Silva", "Valor": "R$ 150,00", "Status": "Aprovado"},
        {"Cliente": "Maria Souza", "Valor": "R$ 80,00", "Status": "Pendente"},
    ]
    st.table(dados_vendas)

elif menu == "🚀 Indicação & Parcerias":
    st.header("Sistema de Indicação e Crescimento")
    st.write("Emplaque pessoas e negócios compartilhando o ecossistema Neurax.")
    
    st.info("Compartilhe seu link exclusivo e ajude outras empresas a lucrarem mais com Pix automatizado.")
    
    link_indicacao = "https://neurax.app/convite/NEURAX-LUCRO2026"
    st.text_input("Seu Link de Parceria", value=link_indicacao, disabled=True)
    
    if st.button("Copiar Link de Parceria"):
        st.success("Link pronto para divulgar e expandir seus negócios!")
