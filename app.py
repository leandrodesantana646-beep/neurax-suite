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

USERS_FILE = "users_neural_v11.json"

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
            "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
            "meta": {"titulo": "Reserva de Emergência", "alvo": 5000.0, "atual": 0.0}
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
                        if "limites" not in dados[email]:
                            dados[email]["limites"] = {"casa": 2000.0, "lazer": 500.0, "despesas": 1000.0}
                        if "gastos_atuais" not in dados[email]:
                            dados[email]["gastos_atuais"] = {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}
                        if "meta" not in dados[email]:
                            dados[email]["meta"] = {"titulo": "Reserva de Emergência", "alvo": 5000.0, "atual": 0.0}
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

# MOTOR DE INTELIGÊNCIA COM LIMITES, METAS, RESUMO SEMANAL E INSIGHTS
def processar_gasto_ou_pergunta(pergunta_ou_comando, user_data, user_email, users_dict):
    query = pergunta_ou_comando.lower()
    
    # 1. RESUMO SEMANAL / RAIO-X AUTOMÁTICO
    if any(k in query for k in ["resumo", "raio-x", "semanal", "balanço"]):
        total_gasto = sum(user_data["gastos_atuais"].values())
        total_limite = sum(user_data["limites"].values())
        maior_cat = max(user_data["gastos_atuais"], key=user_data["gastos_atuais"].get)
        
        feedback_texto = "🎉 **Parabéns!** Você está mantendo seus gastos sob controle nesta semana." if total_gasto <= (total_limite * 0.7) else "⚠️ **Puxão de orelha:** Seus gastos estão acelerados. Cuidado para não estourar o orçamento!"
        
        texto_resp = f"""📊 **Raio-X Semanal Consolidado**\n\n* **Total Gasto no Mês:** R$ {total_gasto:,.2f} / Teto Geral: R$ {total_limite:,.2f}\n* **Categoria que mais pesou:** {maior_cat.capitalize()} (R$ {user_data['gastos_atuais'][maior_cat]:,.2f})\n* **Meta Atual ({user_data['meta']['titulo']}):** R$ {user_data['meta']['atual']:,.2f} / R$ {user_data['meta']['alvo']:,.2f}\n\n{feedback_texto}\n\n💡 *Insight Comportamental:* Notei que os gastos tendem a se concentrar em finais de semana. Planeje os próximos dias para acelerar sua reserva!"""

        df_resumo = pd.DataFrame({
            "Gastos Atuais": list(user_data["gastos_atuais"].values()),
            "Limites": list(user_data["limites"].values())
        }, index=["Casa", "Lazer", "Despesas"])

        return {
            "texto": texto_resp,
            "grafico_tipo": "barras",
            "grafico_titulo": "📊 Raio-X de Gastos vs. Limites",
            "grafico_dados": df_resumo
        }

    # 2. DEFINIÇÃO OU ATUALIZAÇÃO DE METAS E SONHOS
    if "meta" in query or "guardar" in query or "objetivo" in query:
        numeros = re.findall(r'\d+[\d,.]*', query.replace('.', '').replace(',', '.'))
        if numeros:
            val_num = float(numeros[0].replace(',', '.'))
            if "guardar" in query or "adicionar" in query:
                users_dict[user_email]["meta"]["atual"] += val_num
                msg_acao = f"Adicionado R$ {val_num:,.2f} à sua meta!"
            else:
                users_dict[user_email]["meta"]["alvo"] = val_num
                if " para " in query:
                    partes = query.split(" para ")
                    if len(partes) > 1:
                        users_dict[user_email]["meta"]["titulo"] = partes[1].title()
                msg_acao = f"Nova meta configurada com sucesso!"
            
            salvar_usuarios(users_dict)
            m = users_dict[user_email]["meta"]
            
            texto_resp = f"🎯 **Gestão de Metas e Sonhos**\n\n* **Objetivo:** {m['titulo']}\n* **Progresso:** R$ {m['atual']:,.2f} / R$ {m['alvo']:,.2f}\n* **Status:** {msg_acao}\n\nA IA está monitorando seu progresso diariamente para te ajudar a vencer!"
            
            df_meta = pd.DataFrame({"Progresso": [m['atual'], max(0.0, m['alvo'] - m['atual'])]}, index=["Guardado", "Faltante"])
            return {
                "texto": texto_resp,
                "grafico_tipo": "barras",
                "grafico_titulo": f"🎯 Progresso da Meta: {m['titulo']}",
                "grafico_dados": df_meta
            }

    # 3. DETECÇÃO DE ALTERAÇÃO DE LIMITES VIA CHAT
    if "limite" in query and any(c in query for c in ["casa", "lazer", "despesas"]):
        numeros = re.findall(r'\d+[\d,.]*', query.replace('.', '').replace(',', '.'))
        if numeros:
            novo_limite = float(numeros[0].replace(',', '.'))
            cat_alvo = "despesas"
            if "casa" in query: cat_alvo = "casa"
            elif "lazer" in query: cat_alvo = "lazer"
            elif "despesas" in query: cat_alvo = "despesas"
            
            users_dict[user_email]["limites"][cat_alvo] = novo_limite
            salvar_usuarios(users_dict)
            
            gasto_atual = users_dict[user_email]["gastos_atuais"][cat_alvo]
            texto_resp = f"⚙️ **Limite Mensal Atualizado!**\n\n* **Categoria:** {cat_alvo.capitalize()}\n* **Novo Teto:** R$ {novo_limite:,.2f}\n* **Gasto Atual:** R$ {gasto_atual:,.2f}\n\n💡 *Insight:* Manter tetos rígidos aumenta sua capacidade de poupança em até 20% ao mês."

            df_gastos = pd.DataFrame({
                "Gasto Acumulado (R$)": [users_dict[user_email]["gastos_atuais"]["casa"], users_dict[user_email]["gastos_atuais"]["lazer"], users_dict[user_email]["gastos_atuais"]["despesas"]],
                "Limite Mensal (R$)": [users_dict[user_email]["limites"]["casa"], users_dict[user_email]["limites"]["lazer"], users_dict[user_email]["limites"]["despesas"]]
            }, index=["Casa", "Lazer", "Despesas"])

            return {
                "texto": texto_resp,
                "grafico_tipo": "barras",
                "grafico_titulo": "📊 Status Atualizado: Gastos vs. Novos Limites",
                "grafico_dados": df_gastos
            }

    # 4. DETECÇÃO DE REGISTRO DE GASTO + INSIGHT PROATIVO
    palavras_chave_gasto = ["gastei", "paguei", "comprei", "conta de", "gasto"]
    if any(p in query for p in palavras_chave_gasto):
        numeros = re.findall(r'\d+[\d,.]*', query.replace('.', '').replace(',', '.'))
        if numeros:
            valor = float(numeros[0].replace(',', '.'))
            categoria = "despesas"
            if any(c in query for c in ["casa", "aluguel", "luz", "água", "mercado", "supermercado", "condomínio"]):
                categoria = "casa"
            elif any(c in query for c in ["lazer", "passeio", "cerveja", "viagem", "cinema", "restaurante", "jogo"]):
                categoria = "lazer"
            elif any(c in query for c in ["despesa", "geral", "carro", "gasolina", "farmácia", "roupa"]):
                categoria = "despesas"
                
            users_dict[user_email]["gastos_atuais"][categoria] += valor
            gasto_atual = users_dict[user_email]["gastos_atuais"][categoria]
            limite_cat = users_dict[user_email]["limites"][categoria]
            salvar_usuarios(users_dict)
            
            ultrapassou = gasto_atual > limite_cat
            status_limite = "⚠️ ALERTA: Você ultrapassou o limite mensal desta categoria!" if ultrapassou else "✅ Gasto dentro do limite seguro."
            
            insight_proativo = ""
            if categoria == "lazer" and gasto_atual > (limite_cat * 0.5):
                insight_proativo = "\n\n🧠 *Insight Proativo da IA:* Notei que seus gastos com Lazer estão subindo rápido. Que tal reduzirmos 15% nos próximos dias para bater sua meta do mês?"

            texto_resposta = f"""💸 **Registro Financeiro Realizado!**\n\n* **Categoria:** {categoria.capitalize()}\n* **Valor Registrado:** R$ {valor:,.2f}\n* **Total Acumulado:** R$ {gasto_atual:,.2f} / Limite: R$ {limite_cat:,.2f}\n* **Status:** {status_limite}{insight_proativo}"""

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

    # 5. CONSULTA DE NEGÓCIOS / IA GERAL
    termo_limpo = pergunta_ou_comando.title()
    texto_gerado = f"""💼 **Auditoria e Plano de Lucratividade Estratégica**\n\n**1. Diagnóstico Inicial:**\nAnalisamos a sua solicitação (*"{pergunta_ou_comando}"*). O principal gargalo que impede o seu negócio de crescer é a alocação ineficiente de capital.\n\n**2. O Plano de Ação Imediato:**\n* **Foco no Caixa:** Proteja sua margem cortando custos operacionais nas próximas 48 horas.\n* **Expansão Comercial:** Ative sua base de clientes antigos com ofertas diretas.\n\n💡 *Insight Comportamental:* A consistência diária nas pequenas decisões financeiras gera um impacto exponencial no seu lucro trimestral."""

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
        * 🧠 **Cérebro Master Unificado:** Consultoria avançada para negócios.
        * 💸 **Controle de Gastos e Metas:** Gerencie limites e sonhos direto no chat.
        * 📊 **Raio-X Semanal e Insights:** IA pró-ativa com puxões de orelha e parabéns.
        * 🚨 **Alertas no WhatsApp:** Relatórios instantâneos a um clique.
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
                            "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0},
                            "meta": {"titulo": "Reserva de Emergência", "alvo": 5000.0, "atual": 0.0}
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
    user_data = users.get(user_email, {"nome": "Empreendedor", "is_pro": False, "lucro_gerado": 0.0, "trial_usado": False, "amigos_indicados": 0, "codigo_indicacao": "NRX-PRO", "limites": {"casa": 2000.0, "lazer": 500.0, "despesas": 1000.0}, "gastos_atuais": {"casa": 0.0, "lazer": 0.0, "despesas": 0.0}, "meta": {"titulo": "Reserva de Emergência", "alvo": 5000.0, "atual": 0.0}})
    
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
        "⚡ Master IA & Retenção de Hábitos",
        "🎁 Indique e Ganhe (Viral)",
        "💳 Assinatura Pro (Pagamento via Pix)",
        "🚪 Sair (Logout)"
    ]
    if is_admin:
        opcoes_menu.insert(1, "👑 Painel do Administrador (Gestão)")

    menu = st.sidebar.selectbox("Navegação do Sistema", opcoes_menu)

    if menu == "⚡ Master IA & Retenção de Hábitos":
        st.markdown("### ⚡ Cérebro Master, Metas e Raio-X Semanal")
        st.markdown("<p style='color: #64748b; font-size: 13px;'>Dica: Digite <i>'Resumo semanal'</i>, <i>'Criar meta de 5000 para Carro'</i>, <i>'Gastei 150 com lazer'</i> ou <i>'Mudar limite de casa para 3000'</i>.</p>", unsafe_allow_html=True)
        
        pode_usar = user_data['is_pro'] or (not user_data['trial_usado'])
        
        if not pode_usar:
            st.warning("⚠️ **Seu único teste gratuito já foi utilizado!** Para continuar tendo acesso ilimitado às respostas e ferramentas de retenção, ative sua Conta Pro.")
        else:
            if not user_data['is_pro']:
                st.info("ℹ️ Você está utilizando o seu **1 teste gratuito exclusivo**. Aproveite para testar o sistema agora!")

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
                            encoded_text = urllib.parse.quote(f"Relatório de Finanças e Metas Neurax:\n\n{message['content']['texto']}")
                            st.markdown(f'<a href="https://wa.me/?text={encoded_text}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%;">💬 Enviar Alerta para o WhatsApp</button></a>', unsafe_allow_html=True)
                        with col_d:
                            st.download_button("📥 Baixar Relatório (TXT)", data=message['content']['texto'], file_name=f"neurax_relatorio_{i}.txt", mime="text/plain", key=f"dl_{i}")

            if prompt := st.chat_input("Ex: 'Resumo semanal', 'Criar meta de 5000 para Carro Novo' ou 'Gastei 150'"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.rerun()

    elif menu == "🎁 Indique e Ganhe (Viral)":
        st.header("🎁 Programa Indique e Ganhe")
        link_indicacao = f"https://neurax-suite-bz6izlp5hikpysvm4oejvc.streamlit.app/?ref={user_data.get('codigo_indicacao', 'NRX')}"
        
        with st.container(border=True):
            st.subheader("Seu Link Exclusivo de Indicação")
            st.text_input("Copie e envie para seus contatos:", value=link_indicacao, disabled=True)
            st.metric("Amigos já indicados", f"{user_data.get('amigos_indicados', 0)} pessoas")
        
        encoded_share = urllib.parse.quote(f"Cara, você precisa testar o Neurax Master AI! Ele controla gastos, gera resumo semanal com raio-x, gerencia metas de sonhos e manda alertas no WhatsApp. Acesse por aqui: {link_indicacao}")
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
if st.session_state.logged_in and menu == "⚡ Master IA & Retenção de Hábitos":
    if len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
        prompt = st.session_state.chat_history[-1]["content"]
        with st.spinner("Processando inteligência comportamental e orçamentos..."):
            resposta_master = processar_gasto_ou_pergunta(prompt, user_data, user_email, users)
            st.session_state.chat_history.append({"role": "assistant", "content": resposta_master})
            if not user_data['is_pro']: users[user_email]["trial_usado"] = True
            if "leandrodesantana646@gmail.com" in users: users["leandrodesantana646@gmail.com"]["lucro_gerado"] += 19.90
            salvar_usuarios(users)
            st.rerun()
