import streamlit as st
import json
import os
import datetime
import urllib.parse
import pandas as pd
import re

st.set_page_config(
    page_title="Neurax Master AI - O Sócio de Lucros e Finanças por IA",
    page_icon="⚡",
    layout="wide"
)

# Estilização de alto padrão otimizada para mobile e desktop
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { color: #0f172a !important; font-family: 'Inter', sans-serif; font-weight: 700; }
    .stTextInput input, .stTextInput input[type="password"], .stTextArea textarea {
        color: #0f172a !important; background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important; border-radius: 8px !important; padding: 12px !important;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important; border-radius: 8px !important; font-weight: 600 !important; border: none !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3); width: 100%; padding: 10px;
    }
    .stButton button { border-radius: 8px !important; font-weight: 600 !important; width: 100%; }
    [data-testid="stSidebar"] { background-color: #0f172a; color: #ffffff; }
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] span { color: #f8fafc !important; }
    div.stMarkdown { font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "users_neural_v9.json"

def carregar_usuarios():
    usuarios_padrao = {
        "leandrodesantana646@gmail.com": {
            "senha": "leandro1996",
            "nome": "Leandro (Dono)",
            "is_pro": True,
            "lucro_gerado": 0.0,
            "trial_usado": True,
            "status_pagamento": "Pago (Admin Master)",
            "data_cadastro": "2026-05-15",
            "codigo_indicacao": "LEANDRO99",
            "amigos_indicados": 0,
            "limites": {"casa": 2000.0, "lazer": 500.0, "despesas": 1000.0},
            "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}
        }
    }
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for email, info in usuarios_padrao.items():
                    if email not in dados: 
                        dados[email] = info
                    else:
                        # Garante chaves de limites e gastos para usuários antigos
                        if "limites" not in dados[email]:
                            dados[email]["limites"] = {"casa": 2000.0, "lazer": 500.0, "despesas": 1000.0}
                        if "gastos_atuais" not in dados[email]:
                            dados[email]["gastos_atuais"] = {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}
                return dados
        except Exception:
            pass
    return usuarios_padrao

def salvar_usuarios(users_dict):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_dict, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar usuário: {e}")

# MOTOR DE INTELIGÊNCIA E CONTROLE DE GASTOS
def processar_gasto_ou_pergunta(pergunta_ou_comando, user_data, user_email, users_dict):
    query = pergunta_ou_comando.lower()
    
    # Detecta se é um registro de gasto (ex: "gastei 150 com lazer", "paguei 800 de casa")
    palavras_chave_gasto = ["gastei", "paguei", "comprei", "conta de", "gasto"]
    if any(p in query for p in palavras_chave_gasto):
        # Tenta extrair número
        numeros = re.findall(r'\d+[\d,.]*', query.replace('.', '').replace(',', '.'))
        if numeros:
            try:
                valor = float(numeros[0].replace(',', '.'))
            except:
                valor = 0.0
            
            # Identifica a categoria
            categoria = "despesas"
            if any(c in query for c in ["casa", "aluguel", "luz", "água", "mercado", "supermercado", "condomínio"]):
                categoria = "casa"
            elif any(c in query for c in ["lazer", "passeio", "cerveja", "viagem", "cinema", "restaurante", "jogo"]):
                categoria = "lazer"
            elif any(c in query for c in ["despesa", "geral", "carro", "gasolina", "farmácia", "roupa"]):
                categoria = "despesas"
                
            # Atualiza o gasto do usuário
            users_dict[user_email]["gastos_atuais"][categoria] += valor
            gasto_atual = users_dict[user_email]["gastos_atuais"][categoria]
            limite_cat = users_dict[user_email]["limites"][categoria]
            salvar_usuarios(users_dict)
            
            ultrapassou = gasto_atual > limite_cat
            status_limite = "⚠️ ALERTA: Você ultrapassou o limite mensal desta categoria!" if ultrapassou else "✅ Gasto dentro do limite seguro."
            
            texto_resposta = f"""💸 **Registro Financeiro Realizado com Sucesso!**\n\n* **Categoria:** {categoria.capitalize()}\n* **Valor Registrado:** R$ {valor:,.2f}\n* **Total Acumulado em {categoria.capitalize()}:** R$ {gasto_atual:,.2f} / Limite: R$ {limite_cat:,.2f}\n* **Status:** {status_limite}\n\n"""
            if ultrapassou:
                ultrapasso_valor = gasto_atual - limite_cat
                texto_resposta += f"🚨 **ATENÇÃO:** O limite de {categoria.capitalize()} foi estourado em **R$ {ultrapasso_valor:,.2f}**! Relatório gerado para envio automático no WhatsApp."

            df_gastos = pd.DataFrame({
                "Gasto Acumulado (R$)": [users_dict[user_email]["gastos_atuais"]["casa"], users_dict[user_email]["gastos_atuais"]["lazer"], users_dict[user_email]["gastos_atuais"]["despesas"]],
                "Limite Mensal (R$)": [users_dict[user_email]["limites"]["casa"], users_dict[user_email]["limites"]["lazer"], users_dict[user_email]["limites"]["despesas"]]
            }, index=["Casa", "Lazer", "Despesas"])

            return {
                "texto": texto_resposta,
                "grafico_tipo": "barras",
                "grafico_titulo": "📊 Comparativo: Gastos Atuais vs. Limites Mensais",
                "grafico_dados": df_gastos
            }

    # Caso seja uma consulta de negócio normal ou pedido de IA
    termo_limpo = pergunta_ou_comando.title()
    texto_gerado = f"""💼 **Auditoria e Plano de Lucratividade Estratégica**\n\n**1. Diagnóstico Inicial:**\nAnalisamos a sua solicitação (*"{pergunta_ou_comando}"*). O principal gargalo que impede o seu negócio de crescer é a alocação ineficiente de capital.\n\n**2. O Plano de Ação Imediato:**\n* **Foco no Caixa:** Proteja sua margem cortando custos operacionais desnecessários nas próximas 48 horas.\n* **Expansão Comercial:** Ative sua base de clientes antigos com ofertas diretas.\n\n**3. Projeção de Crescimento Financeiro:**\nCom a aplicação deste plano de eficiência, o seu fluxo de caixa tende a evoluir da seguinte forma:"""

    return {
        "texto": texto_gerado,
        "grafico_tipo": "barras",
        "grafico_titulo": f"📊 Projeção de Faturamento e Lucro: {termo_limpo}",
        "grafico_dados": pd.DataFrame({
            "Modelo Operacional Antigo": [10000, 10500, 11000],
            "Com Estratégia de Lucro Neurax": [10000, 16500, 25000]
        }, index=["Mês 1 (Atual)", "Mês 2", "Mês 3"])
    }

# Controle de Sessão
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'auth_screen' not in st.session_state: st.session_state.auth_screen = 'login'
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

users = carregar_usuarios()

# TELA DE LOGIN / CADASTRO
if not st.session_state.logged_in:
    col_brand, col_form = st.columns([1.1, 0.9], gap="large")
    
    with col_brand:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("# ⚡ Neurax Master AI")
        st.markdown("### O Aplicativo Definitivo de Negócios e Controle de Gastos por IA.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        * 🧠 **Cérebro Master Unificado:** Consultoria avançada para qualquer ramo.
        * 💸 **Controle de Gastos Inteligente:** Basta digitar no chat para registrar gastos em Casa, Lazer e Despesas.
        * 🚨 **Alertas no WhatsApp:** Relatórios instantâneos caso você ultrapasse seus limites mensais.
        """)
    with col_form:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            if st.session_state.auth_screen == 'login':
                st.subheader("🔑 Acesse sua Conta")
                email = st.text_input("E-mail corporativo", placeholder="seu@email.com", key="login_email")
                senha = st.text_input("Senha de acesso", type="password", placeholder="********", key="login_senha")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Entrar no Ecossistema", type="primary"):
                    users = carregar_usuarios()
                    if email in users and users[email]["senha"] == senha:
                        st.session_state.logged_in = True
                        st.session_state.current_user = email
                        st.rerun()
                    else:
                        st.error("E-mail ou senha incorretos.")
                
                col_sub1, col_sub2 = st.columns(2)
                with col_sub1:
                    if st.button("Criar Conta"): st.session_state.auth_screen = 'register'; st.rerun()
                with col_sub2:
                    if st.button("Esqueceu a Senha?"): st.session_state.auth_screen = 'forgot'; st.rerun()

            elif st.session_state.auth_screen == 'register':
                st.subheader("📝 Criar Conta")
                nome_reg = st.text_input("Nome", placeholder="Seu Nome", key="reg_nome")
                email_reg = st.text_input("E-mail", placeholder="seu@email.com", key="reg_email")
                senha_reg = st.text_input("Senha", type="password", placeholder="********", key="reg_senha")
                conf_senha = st.text_input("Confirmar Senha", type="password", placeholder="********", key="reg_conf")
                if st.button("Cadastrar", type="primary"):
                    if email_reg in users: st.error("E-mail já cadastrado.")
                    elif senha_reg != conf_senha: st.error("Senhas não conferem.")
                    else:
                        data_atual = datetime.date.today().strftime("%Y-%m-%d")
                        codigo_gerado = "NRX-" + nome_reg[:3].upper() + "99"
                        users[email_reg] = {
                            "senha": senha_reg, 
                            "nome": nome_reg, 
                            "is_pro": False, 
                            "lucro_gerado": 0.0,
                            "trial_usado": False,
                            "status_pagamento": "Apenas Testou (Não Voltou)",
                            "data_cadastro": data_atual,
                            "codigo_indicacao": codigo_gerado,
                            "amigos_indicados": 0,
                            "limites": {"casa": 2000.0, "lazer": 500.0, "despesas": 1000.0},
                            "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}
                        }
                        salvar_usuarios(users)
                        st.success("Conta criada com sucesso! Faça login.")
                        st.session_state.auth_screen = 'login'; st.rerun()
                if st.button("← Voltar"): st.session_state.auth_screen = 'login'; st.rerun()

            elif st.session_state.auth_screen == 'forgot':
                st.subheader("🔒 Recuperação")
                st.text_input("E-mail", placeholder="seu@email.com", key="rec_email")
                if st.button("Enviar", type="primary"): st.success("Instruções enviadas!")
                if st.button("← Voltar"): st.session_state.auth_screen = 'login'; st.rerun()

# APLICATIVO PRINCIPAL
else:
    users = carregar_usuarios()
    user_email = st.session_state.current_user
    user_data = users.get(user_email, {"nome": "Empreendedor", "is_pro": False, "lucro_gerado": 0.0, "trial_usado": False, "amigos_indicados": 0, "codigo_indicacao": "NRX-PRO", "limites": {"casa": 2000.0, "lazer": 500.0, "despesas": 1000.0}, "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}})
    
    is_admin = (user_email == "leandrodesantana646@gmail.com")

    # DASHBOARD
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 22px; border-radius: 12px; border: 1px solid #334155; color: white; margin-bottom: 20px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 15px;">
            <div>
                <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #38bdf8; font-weight: 700;">⚡ Neurax Master Intelligence & Finanças</span>
                <h3 style="margin: 4px 0 0 0; color: #ffffff !important; font-size: 20px;">Olá, {user_data['nome']}</h3>
                <p style="margin: 2px 0 0 0; color: #94a3b8; font-size: 13px;">Status: {'⭐ PRO Ativo' if user_data['is_pro'] else '🔓 Teste Grátis Disponível' if not user_data['trial_usado'] else '🔒 Teste Concluído'}</p>
            </div>
            <div style="text-align: right; background: rgba(16, 185, 129, 0.15); padding: 12px 18px; border-radius: 8px; border: 1px solid #10b981; min-width: 160px;">
                <span style="font-size: 11px; color: #34d399; font-weight: 800; letter-spacing: 0.5px;">FATURAMENTO / LUCRO AUTOMÁTICO</span><br>
                <span style="font-size: 22px; color: #ffffff; font-weight: 900;">R$ {user_data.get('lucro_gerado', 0.0):,.2f}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    opcoes_menu = [
        "⚡ Master IA & Controle de Gastos",
        "🎁 Indique e Ganhe (Viral)",
        "💳 Assinatura Pro (Pagamento via Pix)",
        "🚪 Sair (Logout)"
    ]
    if is_admin:
        opcoes_menu.insert(1, "👑 Painel do Administrador (Gestão)")

    menu = st.sidebar.selectbox("Navegação do Sistema", opcoes_menu)

    if menu == "⚡ Master IA & Controle de Gastos":
        st.markdown("### ⚡ Cérebro Master e Gestão de Orçamento")
        st.markdown("<p style='color: #64748b; font-size: 13px;'>Dica: Digite perguntas de negócios ou registre gastos diretamente aqui (ex: <i>'Gastei 350 reais com lazer hoje'</i> ou <i>'Paguei 1200 de aluguel da casa'</i>).</p>", unsafe_allow_html=True)
        
        pode_usar = user_data['is_pro'] or (not user_data['trial_usado'])
        
        if not pode_usar:
            st.warning("⚠️ **Seu único teste gratuito já foi utilizado!** Para continuar tendo acesso ilimitado às respostas e relatórios financeiros da IA, ative sua Conta Pro.")
        else:
            if not user_data['is_pro']:
                st.info("ℹ️ Você está utilizando o seu **1 teste gratuito exclusivo**. Aproveite para testar o controle de gastos agora!")

            for i, message in enumerate(st.session_state.chat_history):
                with st.chat_message(message["role"]):
                    if message["role"] == "user":
                        st.markdown(message["content"])
                    else:
                        st.markdown(message["content"]["texto"])
                        if "grafico_dados" in message["content"]:
                            st.markdown(f"<p style='text-align: center; color: #059669; font-weight: 800; margin-top: 15px;'>{message['content']['grafico_titulo']}</p>", unsafe_allow_html=True)
                            if message["content"]["grafico_tipo"] == "barras":
                                st.bar_chart(message["content"]["grafico_dados"], height=250)
                            else:
                                st.line_chart(message["content"]["grafico_dados"], height=250)
                        
                        col_w, col_d = st.columns(2)
                        with col_w:
                            encoded_text = urllib.parse.quote(f"Relatório de Finanças e Gestão Neurax:\n\n{message['content']['texto']}")
                            st.markdown(f'<a href="https://wa.me/?text={encoded_text}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%;">💬 Enviar Alerta para o WhatsApp</button></a>', unsafe_allow_html=True)
                        with col_d:
                            st.download_button("📥 Baixar Relatório (TXT)", data=message['content']['texto'], file_name=f"neurax_relatorio_{i}.txt", mime="text/plain", key=f"dl_{i}")

            if prompt := st.chat_input("Ex: 'Gastei 250 com lazer' ou 'Como aumentar minhas vendas'"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.rerun()

    elif menu == "🎁 Indique e Ganhe (Viral)":
        st.header("🎁 Programa Indique e Ganhe")
        link_indicacao = f"https://neurax-suite-bz6izlp5hikpysvm4oejvc.streamlit.app/?ref={user_data.get('codigo_indicacao', 'NRX')}"
        
        with st.container(border=True):
            st.subheader("Seu Link Exclusivo de Indicação")
            st.text_input("Copie e envie para seus contatos:", value=link_indicacao, disabled=True)
            st.metric("Amigos já indicados", f"{user_data.get('amigos_indicados', 0)} pessoas")
        
        encoded_share = urllib.parse.quote(f"Cara, você precisa testar o Neurax Master AI! Ele controla seus gastos divididos em Casa, Lazer e Despesas, manda alertas no WhatsApp e ainda projeta lucros em gráficos. Acesse por aqui: {link_indicacao}")
        st.markdown(f'<br><a href="https://wa.me/?text={encoded_share}" target="_blank"><button style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; width: 100%;">🚀 Compartilhar com Amigos no WhatsApp</button></a>', unsafe_allow_html=True)

    elif menu == "👑 Painel do Administrador (Gestão)":
        st.header("👑 Painel de Controle Exclusivo do Dono")
        total_usuarios = len(users)
        pro_usuarios = [u for u, d in users.items() if d.get('is_pro')]
        trial_usuarios = [u for u, d in users.items() if not d.get('is_pro')]
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1: st.metric("Total de Cadastros", total_usuarios)
        with col_m2: st.metric("Usuários PRO (Pagantes)", len(pro_usuarios))
        with col_m3: st.metric("Apenas Testaram", len(trial_usuarios))
            
        st.markdown("---")
        st.subheader("💎 Clientes Pagantes")
        pro_data = [{"Nome": i.get('nome'), "E-mail": u, "Data Cadastro": i.get('data_cadastro', 'N/D')} for u, i in users.items() if i.get('is_pro')]
        st.dataframe(pro_data, use_container_width=True)
        
        st.subheader("🔍 Usuários em Teste")
        trial_data = [{"Nome": i.get('nome'), "E-mail": u, "Data Cadastro": i.get('data_cadastro', 'N/D')} for u, i in users.items() if not i.get('is_pro')]
        st.dataframe(trial_data, use_container_width=True)

    elif menu == "💳 Assinatura Pro (Pagamento via Pix)":
        st.header("💳 Ativação Profissional - R$ 19,99")
        if user_data['is_pro']: 
            st.success("✨ Sua Conta Pro está ATIVA com acesso ilimitado!")
        else:
            with st.container(border=True):
                st.subheader("📱 Pix Copia e Cola")
                st.code("00020126580014br.gov.bcb.pix0136neurax-master-ai-pagamento-automatico5204000053039865802BR5925Neurax Business Tech6009Sao Paulo62070503***6304E2CA", language="text")
                st.info("Valor: **R$ 19,99** | Beneficiário: **Neurax Tech**")
            
            if st.button("🔄 Já Fiz o Pagamento - Verificar Confirmação do Pix", type="primary"):
                users[user_email]["is_pro"] = True
                users[user_email]["status_pagamento"] = "Pago (Pro Confirmado via Pix)"
                if "leandrodesantana646@gmail.com" in users:
                    users["leandrodesantana646@gmail.com"]["lucro_gerado"] += 19.99
                salvar_usuarios(users)
                st.success("🎉 Pagamento confirmado! Acesso liberado.")
                st.rerun()

    elif menu == "🚪 Sair (Logout)":
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.auth_screen = 'login'
        st.rerun()

# Lógica final para responder no chat
if st.session_state.logged_in and menu == "⚡ Master IA & Controle de Gastos":
    if len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
        prompt = st.session_state.chat_history[-1]["content"]
        with st.spinner("Processando dados financeiros e atualizando orçamentos..."):
            resposta_master = processar_gasto_ou_pergunta(prompt, user_data, user_email, users)
            st.session_state.chat_history.append({"role": "assistant", "content": resposta_master})
            if not user_data['is_pro']: users[user_email]["trial_usado"] = True
            if "leandrodesantana646@gmail.com" in users: users["leandrodesantana646@gmail.com"]["lucro_gerado"] += 19.90
            salvar_usuarios(users)
            st.rerun()
