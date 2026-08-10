import streamlit as st
import json
import os
import datetime
import pandas as pd
import re

# Configuração da página
st.set_page_config(
    page_title="Neurax Master AI", 
    page_icon="⚡", 
    layout="wide"
)

# Estilização Avançada e Moderna (UI/UX de Alto Padrão)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main { 
        background-color: #f8fafc; 
    }
    
    h1, h2, h3 { 
        color: #0f172a; 
        font-weight: 800; 
        letter-spacing: -0.025em; 
    }
    
    /* Cartões Modernos com Sombra Suave */
    .stMetric { 
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); 
        padding: 20px; 
        border-radius: 14px; 
        border: 1px solid #e2e8f0; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02); 
    }
    
    /* Menu Lateral Escuro e Elegante */
    [data-testid="stSidebar"] { 
        background-color: #0f172a; 
        color: #ffffff; 
        border-right: 1px solid #1e293b;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #94a3b8;
    }
    
    /* Botões Modernos com Gradiente */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
        transform: translateY(-1px);
    }
    
    /* Caixas de Texto Arredondadas */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
        padding: 10px;
    }
    
    /* Cabeçalho Customizado */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

USERS_FILE = "users_neural_final.json"
mes_atual = datetime.datetime.now().strftime("%m/%Y")

# Funções auxiliares
def carregar_usuarios():
    usuarios_padrao = {
        "leandrodesantana646@gmail.com": {
            "senha": "leandro1996", "nome": "Leandro (Dono)", "is_pro": True,
            "dias_pro_ganhos": 0, "amigos_indicados": 0, "codigo_indicacao": "LEANDRO99",
            "ultimo_mes": mes_atual, "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
            "meta": {"alvo": 10000.0}
        }
    }
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return usuarios_padrao
    return usuarios_padrao

def salvar_usuarios(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=4)

def verificar_acesso_pro(user_data):
    return user_data.get("is_pro", False) or user_data.get("dias_pro_ganhos", 0) > 0

def processar_consulta(query, user_email, users_dict):
    query = query.lower()
    if any(p in query for p in ["gastei", "paguei", "gasto"]):
        numeros = re.findall(r'\d+', query)
        valor = float(numeros[0]) if numeros else 0
        cat = "lazer" if "lazer" in query else "casa" if "casa" in query else "despesas"
        users_dict[user_email]["gastos_atuais"][cat] += valor
        salvar_usuarios(users_dict)
        return f"✅ **Registrado:** R$ {valor:,.2f} em {cat}."
    return "💼 **Diagnóstico:** Para escalar, foque em reduzir custos fixos. Como posso te ajudar hoje?"

# --- FLUXO PRINCIPAL ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
users = carregar_usuarios()
ref_code = st.query_params.get("ref")

# --- CAPTURA DE RETORNO DO PAGAMENTO AUTOMÁTICO ---
status_pagamento = st.query_params.get("status")
if status_pagamento == "sucesso" and st.session_state.get('logged_in'):
    user_email = st.session_state.current_user
    if user_email in users and not users[user_email].get("is_pro", False):
        users[user_email]["is_pro"] = True
        salvar_usuarios(users)
        st.balloons()
        st.success("🎉 Pagamento confirmado com sucesso! Seu acesso PRO foi liberado automaticamente.")

if not st.session_state.logged_in:
    # --- LOGOTIPO OU FALLBACK MODERNO NA TELA DE LOGIN ---
    col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
    with col_c2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown("""
                <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #0f172a, #1e293b); border-radius: 16px; color: white; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: #38bdf8; font-size: 24px;">⚡ NEURAX</h2>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: #94a3b8;">MASTER AI</p>
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<h2 style='text-align: center; margin-bottom: 25px;'>🔑 Acesse o Motor de Lucros</h2>", unsafe_allow_html=True)
        
    email = st.text_input("E-mail corporativo ou pessoal")
    senha = st.text_input("Senha de acesso", type="password")
    
    if st.button("Entrar no Sistema", use_container_width=True):
        if email in users and users[email]["senha"] == senha:
            st.session_state.logged_in = True
            st.session_state.current_user = email
            st.rerun()
        else: 
            st.error("E-mail ou senha incorretos.")
            
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>📝 Criar Conta Gratuita</h3>", unsafe_allow_html=True)
    nome_r = st.text_input("Nome Completo")
    email_r = st.text_input("E-mail para Cadastro")
    telefone_r = st.text_input("WhatsApp (com DDD, ex: 5511999999999)")
    senha_r = st.text_input("Crie uma Senha", type="password")
    
    if st.button("Cadastrar Gratuitamente", use_container_width=True):
        if email_r not in users:
            codigo = f"NRX-{nome_r[:3].upper()}{len(users)}"
            users[email_r] = {
                "senha": senha_r, "nome": nome_r, "telefone": telefone_r, "is_pro": False, 
                "dias_pro_ganhos": 0, "amigos_indicados": 0, "codigo_indicacao": codigo,
                "ultimo_mes": mes_atual,
                "limites": {"casa": 1000.0, "lazer": 300.0, "despesas": 500.0},
                "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
                "meta": {"alvo": 10000.0}
            }
            if ref_code:
                for mail, data in users.items():
                    if data["codigo_indicacao"] == ref_code:
                        users[mail]["amigos_indicados"] += 1
                        users[mail]["dias_pro_ganhos"] += 7
            salvar_usuarios(users)
            st.success("Conta criada com sucesso! Faça login acima.")
        else:
            st.warning("Este e-mail já está cadastrado.")
else:
    user_email = st.session_state.current_user
    user_data = users[user_email]
    
    # Reset automático de mês
    if user_data.get("ultimo_mes") != mes_atual:
        user_data["gastos_atuais"] = {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}
        user_data["ultimo_mes"] = mes_atual
        salvar_usuarios(users)
        st.toast("📅 Novo mês detectado! Seus gastos foram zerados automaticamente.")

    is_admin = (user_email == "leandrodesantana646@gmail.com")

    # UI Lateral
    if os.path.exists("logo.png"): 
        st.sidebar.image("logo.png", use_container_width=True)
    else: 
        st.sidebar.markdown("<h2 style='color: #38bdf8; text-align: center;'>⚡ NEURAX AI</h2>", unsafe_allow_html=True)
    
    st.sidebar.markdown(f"**Usuário:** {user_data['nome']}")
    
    menu_options = ["📊 Painel de Lucros", "⚡ Consultoria IA", "🎁 Indique e Ganhe"]
    if not verificar_acesso_pro(user_data): menu_options.append("👑 Assinar Plano Pro")
    menu_options.append("🚪 Sair")
    if is_admin: menu_options.append("👑 Admin")
    
    menu = st.sidebar.selectbox("Menu Principal", menu_options)

    # Cabeçalho Principal Moderno
    if os.path.exists("logo.png"):
        hc1, hc2 = st.columns([1, 12])
        with hc1:
            st.image("logo.png", width=45)
        with hc2:
            st.markdown("## Neurax Master AI")
    else:
        st.markdown("## ⚡ Neurax Master AI")
    st.markdown("---")

    # Páginas
    if menu == "📊 Painel de Lucros":
        st.header("📈 Projeção de Crescimento Corporativo")
        col1, col2 = st.columns(2)
        col1.metric("Gasto Atual Registrado", f"R$ {sum(user_data['gastos_atuais'].values()):,.2f}")
        col2.metric("Meta de Lucro/Reserva", f"R$ {user_data['meta']['alvo']:,.2f}")

    elif menu == "⚡ Consultoria IA":
        st.header("⚡ Consultoria Estratégica de Negócios")
        if verificar_acesso_pro(user_data):
            prompt = st.chat_input("Ex: 'Gastei 400 com lazer' ou 'Como posso aumentar meu lucro?'")
            if prompt:
                res_texto = processar_consulta(prompt, user_email, users)
                st.markdown(res_texto)
        else:
            st.warning("🔒 Esta funcionalidade é exclusiva para membros **PRO**.")
            st.info("Assine o plano Pro no menu ao lado para desbloquear análises completas.")

    elif menu == "👑 Assinar Plano Pro":
        st.header("👑 Desbloqueie o Potencial Máximo")
        st.markdown("""
        - 🤖 **Consultoria IA Ilimitada** para otimizar seu negócio.
        - 📈 **Projeções de Crescimento** e controle avançado.
        - 🚀 **Suporte Prioritário** via plataforma.
        
        **Valor:** R$ 49,99 / mês
        """)
        st.link_button("Assinar R$ 49,99/mês (PIX / Cartão)", "https://mpago.la/2WjVnvA", use_container_width=True)
        st.info("💡 Após concluir o pagamento, você retornará ao app e seu acesso PRO será liberado automaticamente.")

    elif menu == "🎁 Indique e Ganhe":
        st.header("🎁 Programa de Embaixadores")
        link = f"https://neurax-suite.streamlit.app/?ref={user_data['codigo_indicacao']}"
        st.info(f"**Seu link exclusivo de indicação:**\n`{link}`")
        st.metric("Amigos Convertidos pelo seu Link", user_data["amigos_indicados"])

    elif menu == "👑 Admin":
        st.header("👑 Painel de Gestão e Controle")
        st.dataframe(pd.DataFrame(users).T, use_container_width=True)

    elif menu == "🚪 Sair":
        st.session_state.logged_in = False
        st.rerun()
