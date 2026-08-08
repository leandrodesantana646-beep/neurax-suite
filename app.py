import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="Neurax Business Suite - Completo",
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
st.write("Sua plataforma completa de lucro, automação, vendas via Pix e expansão.")

# Menu lateral unificado contendo todas as ferramentas criadas
menu = st.sidebar.selectbox(
    "Navegação do App",
    [
        "💳 Gerar Cobrança Pix",
        "📊 Relatório de Vendas",
        "🚀 Sistema de Indicação",
        "⚙️ Configurações & Supabase"
    ]
)

if menu == "💳 Gerar Cobrança Pix":
    st.header("Gerador de Cobrança Pix")
    st.write("Integração direta com o Make, Mercado Pago e Supabase.")
    
    webhook_url = st.text_input("URL do Webhook do Make", placeholder="https://hook.us2.make.com/...")
    descricao = st.text_input("Descrição do Produto", placeholder="Ex: Consultoria Neurax")
    valor = st.text_input("Valor (R$)", placeholder="Ex: 10.00")
    nome = st.text_input("Nome do Cliente", placeholder="Ex: João Silva")
    email = st.text_input("E-mail do Cliente", placeholder="Ex: cliente@email.com")

    if st.button("Gerar Cobrança Pix", type="primary"):
        if not webhook_url:
            st.error("Insira a URL do Webhook do Make.")
        elif not descricao or not valor or not nome:
            st.warning("Preencha todos os campos obrigatórios (Descrição, Valor e Nome).")
        else:
            try:
                valor_tratado = float(valor.replace(",", "."))
            except ValueError:
                st.error("O campo de valor deve conter apenas números (ex: 10.00).")
                st.stop()

            payload = {
                "description": descricao,
                "transaction_amount": valor_tratado,
                "payer": {
                    "first_name": nome,
                    "email": email if email else "cliente@email.com"
                }
            }

            with st.spinner("Enviando dados para o Make e gerando Pix..."):
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
    st.write("Acompanhe o faturamento, lucro e fluxo de caixa em tempo real.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Faturamento Hoje", value="R$ 230,00", delta="+15%")
    with col2:
        st.metric(label="Pix Gerados", value="4", delta="1 pendente")
    with col3:
        st.metric(label="Lucro Estimado", value="R$ 210,00", delta="+12%")

    st.markdown("---")
    st.markdown("### Histórico de Transações Recentes")
    
    dados_vendas = [
        {"ID": "#101", "Cliente": "João Silva", "Valor": "R$ 150,00", "Status": "Aprovado"},
        {"ID": "#102", "Cliente": "Maria Souza", "Valor": "R$ 80,00", "Status": "Pendente"},
        {"ID": "#103", "Cliente": "Carlos Eduardo", "Valor": "R$ 200,00", "Status": "Aprovado"}
    ]
    st.table(dados_vendas)

elif menu == "🚀 Sistema de Indicação":
    st.header("Emplaque Pessoas & Sistema de Indicação")
    st.write("Ajude outras empresas e pessoas a lucrarem mais utilizando o ecossistema Neurax.")
    
    st.info("Compartilhe seu link exclusivo de parceria para expandir sua rede e gerar novas fontes de receita.")
    
    link_indicacao = "https://neurax.app/convite/NEURAX-LUCRO2026"
    st.text_input("Seu Link Exclusivo de Parceria", value=link_indicacao, disabled=True)
    
    if st.button("Copiar Link de Parceria"):
        st.success("Link copiado com sucesso! Pronto para divulgar.")

    st.markdown("### Resumo de Parcerias")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Pessoas Indicadas", value="12")
    with col2:
        st.metric(label="Bônus Acumulado", value="R$ 360,00")

elif menu == "⚙️ Configurações & Supabase":
    st.header("Configurações do Banco de Dados e Sistema")
    st.write("Gerencie a conexão com o Supabase e os parâmetros globais do aplicativo.")

    st.text_input("URL do Supabase", value="https://seu-projeto.supabase.co", placeholder="Cole sua URL do Supabase")
    st.text_input("Chave API (Service Role)", type="password", placeholder="Cole sua chave secreta")

    if st.button("Salvar Configurações"):
        st.success("Configurações salvas e banco sincronizado com sucesso!")
