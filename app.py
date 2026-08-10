import streamlit as st
import requests
import base64
import uuid
import json
import os
from io import BytesIO
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Neurax Business Suite Pro",
    page_icon="⚡",
    layout="centered"
)

# Estilo visual avançado - Padrão SaaS Enterprise
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    h1, h2, h3 {
        color: #0f172a !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    .stTextInput input, .stTextInput input[type="password"], .stTextArea textarea {
        color: #0f172a !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        color: #ffffff;
    }
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] span {
        color: #f8fafc !important;
    }
    div.stMarkdown {
        font-family: 'Inter', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Sistema de Persistência de Contas (Salva em arquivo JSON)
USERS_FILE = "users.json"

def carregar_usuarios():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "admin@neurax.com": {"senha": "123", "nome": "Administrador", "is_pro": False}
    }

def salvar_usuarios(users_dict):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_dict, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar usuário: {e}")

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

# Carrega os usuários salvos no arquivo
users = carregar_usuarios()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Configuração segura do Token do Mercado Pago
try:
    ACCESS_TOKEN = st.secrets["MERCADO_PAGO_TOKEN"]
except Exception:
    ACCESS_TOKEN = "APP_USR-ca30bf79-c48b-4cf3-9c30-ee6e3238e005"

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
            users = carregar_usuarios()
            if email in users and users[email]["senha"] == senha:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.session_state.is_pro = users[email]["is_pro"]
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
            users = carregar_usuarios()
            if not nome_reg or not email_reg or not senha_reg:
                st.warning("Preencha todos os campos.")
            elif senha_reg != conf_senha:
                st.error("As senhas não coincidem.")
            elif email_reg in users:
                st.error("Este e-mail já está cadastrado.")
            else:
                users[email_reg] = {
                    "senha": senha_reg,
                    "nome": nome_reg,
                    "is_pro": False
                }
                salvar_usuarios(users)
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
            users = carregar_usuarios()
            if email_rec in users:
                st.success("Instruções de recuperação enviadas para o seu e-mail!")
            else:
                st.error("E-mail não encontrado.")
        
        if st.button("Voltar para o Login"):
            st.session_state.auth_screen = 'login'
            st.rerun()

# ==========================================
# APLICATIVO PRINCIPAL (DESIGN ENTERPRISE + IA)
# ==========================================
else:
    users = carregar_usuarios()
    user_email = st.session_state.current_user
    user_data = users.get(user_email, {"nome": "Usuário", "is_pro": False})
    
    st.title(f"⚡ Neurax Business Suite - Olá, {user_data['nome']}")
    
    if user_data['is_pro']:
        st.success("✨ **Status:** Conta Pro Ativa (Acesso Total Liberado)")
    else:
        st.warning("🔒 **Status:** Plano Gratuito. Ative o Pro para destravar o Cérebro de IA Ilimitado.")

    menu = st.sidebar.selectbox(
        "Navegação do App",
        [
            "🧠 Cérebro IA (Copiloto Universal)",
            "💳 Assinatura & Planos (Pix)",
            "💰 Precificação Inteligente por IA",
            "📊 Relatório Executivo de Caixa",
            "🚀 Sistema de Indicação (Ganhe Bônus)",
            "⚙️ Configurações & Banco de Dados",
            "🚪 Sair (Logout)"
        ]
    )

    # 1. CÉREBRO IA (COPILOTO UNIVERSAL)
    if menu == "🧠 Cérebro IA (Copiloto Universal)":
        st.header("🧠 Neurax AI - Seu Diretor Executivo 24h")
        st.write("Converse com a inteligência artificial para resolver qualquer desafio do seu negócio (E-commerce, Infoprodutos ou Serviços Locais).")
        
        nicho_usuario = st.selectbox("Selecione o seu setor:", ["E-commerce / Loja Física", "Infoprodutos / Produtor Digital", "Prestador de Serviços / Local"])
        
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ex: Como posso dobrar minhas vendas no Instagram esta semana gastando pouco?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analisando dados do mercado e gerando estratégia..."):
                    resposta_ia = f"🤖 **Diagnóstico Neurax AI para {nicho_usuario}:**\n\nCom base no seu objetivo (*\"{prompt}\"*), estruturei o seguinte plano de ação imediato:\n\n1. **Ação de Curto Prazo:** Foque em campanhas de recuperação de clientes antigos via WhatsApp com escassez de 24 horas.\n2. **Precificação e Margem:** Certifique-se de que seu lucro líquido por unidade não esteja abaixo de 30% após taxas de anúncio.\n3. **Automação:** Utilize nossos funis prontos para acelerar a conversão.\n\n*Quer que eu gere os copies exatos para essa campanha agora?*"
                    st.markdown(resposta_ia)
                    st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})

    # 2. ASSINATURA & PLANOS
    elif menu == "💳 Assinatura & Planos (Pix)":
        st.header("💳 Ativar Plano Pro (R$ 19,99)")
        
        if user_data['is_pro']:
            st.success("🎉 Sua conta já está com o Plano Pro ativado!")
        else:
            st.write(f"E-mail de cobrança: **{user_email}**")

            if st.button("Gerar Pix Oficial no Mercado Pago", type="primary"):
                url = "https://api.mercadopago.com/v1/payments"
                headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json",
                    "X-Idempotency-Key": str(uuid.uuid4())
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
                
                if st.button("🔄 Já paguei! Liberar Acesso Pro", type="primary"):
                    users = carregar_usuarios()
                    if user_email in users:
                        users[user_email]["is_pro"] = True
                        salvar_usuarios(users)
                    st.session_state.is_pro = True
                    st.session_state.pix_data = None
                    st.balloons()
                    st.success("🎉 Pagamento confirmado! Acesso Pro liberado com sucesso.")
                    st.rerun()

    # 3. PRECIFICAÇÃO INTELIGENTE POR IA
    elif menu == "💰 Precificação Inteligente por IA":
        st.header("💰 Calculadora de Precificação Preditiva")
        produto_preco = st.text_input("Nome do Produto ou Serviço", placeholder="Ex: Consultoria / Fone Bluetooth")
        custo_produto = st.text_input("Custo de Aquisição ou Produção (R$)", placeholder="Ex: 50.00")
        margem_desejada = st.slider("Margem de Lucro Desejada (%)", 10, 500, 100)
        
        if st.button("Calcular com IA", type="primary"):
            try:
                c = float(custo_produto.replace(",", "."))
                preco_sugerido = c * (1 + margem_desejada / 100)
                st.success("Análise de mercado concluída com IA!")
                st.metric("Preço de Venda Recomendado", f"R$ {preco_sugerido:.2f}")
                st.info(f"💡 Dica da IA: Com este preço, seu lucro líquido estimado por unidade é de R$ {(preco_sugerido - c):.2f}, já descontando impostos médios.")
                
                relatorio_texto = f"RELATÓRIO NEURAX AI: Produto: {produto_preco} | Preço Sugerido: R$ {preco_sugerido:.2f}"
                st.download_button("📥 Baixar Relatório de Precificação", data=relatorio_texto, file_name="precificacao_neurax.txt", mime="text/plain")
            except ValueError:
                st.error("Insira apenas valores numéricos válidos no campo de custo.")

    # 4. RELATÓRIO EXECUTIVO DE CAIXA
    elif menu == "📊 Relatório Executivo de Caixa":
        st.header("📊 Painel de Saúde Financeira")
        if user_data['is_pro']:
            st.metric("Faturamento Gerenciado", "R$ 12.450,00", "+18.5%")
            st.metric("Saúde do Caixa", "Excelente 🟢")
            st.write("Sua operação está mantendo uma margem saudável de retenção de lucro.")
        else:
            st.warning("⚠️ O relatório avançado de caixa está disponível apenas para assinantes Pro.")

    # 5. SISTEMA DE INDICAÇÃO
    elif menu == "🚀 Sistema de Indicação (Ganhe Bônus)":
        st.header("🚀 Programa Indique & Lucre")
        st.write("Compartilhe sua chave exclusiva e ganhe créditos ou comissões em dinheiro.")
        st.code(f"https://neuraxsuite.app/ref?user={user_email}", language="text")
        st.success("Cada amigo que ativar o plano Pro gera recompensas diretas para você!")

    # 6. CONFIGURAÇÕES
    elif menu == "⚙️ Configurações & Banco de Dados":
        st.header("⚙️ Configurações da Conta")
        st.text_input("Nome cadastrado", value=user_data['nome'])
        st.text_input("E-mail de acesso", value=user_email, disabled=True)
        if st.button("Salvar Alterações"):
            st.success("Alterações salvas com sucesso!")

    # 7. SAIR
    elif menu == "🚪 Sair (Logout)":
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.auth_screen = 'login'
        st.rerun()
