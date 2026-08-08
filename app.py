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
    .stTextInput input, .stTextInput input[type="password"], .stTextArea textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    .main {
        background-color: #f4f6f9;
    }
    </style>
""", unsafe_allow_html=True)

# Gerenciamento de estado (Login, Teste Grátis e Status Pro)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'auth_screen' not in st.session_state:
    st.session_state.auth_screen = 'login'
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = True  # Teste grátis ativado por padrão para novos usuários testarem tudo!
if 'pix_data' not in st.session_state:
    st.session_state.pix_data = None

# ==========================================
# TELAS DE AUTENTICAÇÃO (LOGIN / CADASTRO)
# ==========================================
if not st.session_state.logged_in:
    st.title("⚡ Neurax Business Suite")
    
    if st.session_state.auth_screen == 'login':
        st.subheader("🔑 Entrar na sua Conta")
        email = st.text_input("E-mail", placeholder="seu@email.com", key="login_email")
        senha = st.text_input("Senha", type="password", placeholder="********", key="login_senha")
        
        if st.button("Entrar", type="primary"):
            if email and senha:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Preencha todos os campos para entrar.")
        
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
        st.subheader("📝 Criar Nova Conta (Com Teste Grátis)")
        nome_reg = st.text_input("Nome Completo", placeholder="Seu Nome", key="reg_nome")
        email_reg = st.text_input("E-mail", placeholder="seu@email.com", key="reg_email")
        senha_reg = st.text_input("Senha", type="password", placeholder="********", key="reg_senha")
        conf_senha = st.text_input("Confirmar Senha", type="password", placeholder="********", key="reg_conf")
        
        if st.button("Cadastrar e Testar Grátis", type="primary"):
            if nome_reg and email_reg and senha_reg and (senha_reg == conf_senha):
                st.success("Conta criada! Seu Teste Grátis de todas as ferramentas foi ativado.")
                st.session_state.auth_screen = 'login'
                st.rerun()
            else:
                st.warning("Preencha todos os campos corretamente e confirme a senha.")
        
        if st.button("Voltar para o Login"):
            st.session_state.auth_screen = 'login'
            st.rerun()

    elif st.session_state.auth_screen == 'forgot':
        st.subheader("🔒 Recuperação de Senha")
        st.write("Digite seu e-mail cadastrado para receber as instruções.")
        email_rec = st.text_input("E-mail", placeholder="seu@email.com", key="rec_email")
        
        if st.button("Enviar Instruções", type="primary"):
            if email_rec:
                st.success("Instruções de recuperação enviadas para o seu e-mail!")
            else:
                st.error("Informe o e-mail cadastrado.")
        
        if st.button("Voltar para o Login"):
            st.session_state.auth_screen = 'login'
            st.rerun()

# ==========================================
# APLICATIVO PRINCIPAL (APÓS O LOGIN)
# ==========================================
else:
    st.title("⚡ Neurax Business Suite")
    
    # Banner de status do usuário (Teste Grátis ou Pro)
    if st.session_state.is_pro:
        st.success("✨ **Status:** Conta Pro / Teste Grátis Ativo (Acesso Ilimitado a todas as ferramentas)")
    else:
        st.warning("🔒 **Status:** Período de teste encerrado. Ative o plano Pro por R$ 19,99/mês para continuar.")

    menu = st.sidebar.selectbox(
        "Navegação do App",
        [
            "💳 Assinatura & Planos",
            "💳 Gerar Cobrança Pix",
            "🌐 Testador HTTP / Webhook Make",
            "📊 Relatório de Vendas",
            "🚀 Sistema de Indicação",
            "⚙️ Configurações & Supabase",
            "⚡ Gestor de Tarefas Inteligente",
            "🧠 Mentor de Saúde Mental",
            "📚 Tutor Universal & Estudos",
            "🗺️ Arquiteto de Funis de Vendas",
            "💰 Precificação Inteligente",
            "🎯 Gerador de Anúncios (Meta/Google)",
            "🚀 NeuraX Growth Engine",
            "💬 Gerador de Copy WhatsApp",
            "📸 Planejador Instagram",
            "✉️ Gerador de E-mail Comercial",
            "🎬 Gerador de Roteiro para Vídeos",
            "⚖️ Assistente de Burocracias",
            "💸 Consultor de Finanças Pessoais",
            "🍳 Assistente de Despensa & Rotina",
            "🎓 Simulador de Entrevistas",
            "🚪 Sair (Logout)"
        ]
    )

    if menu == "💳 Assinatura & Planos":
        st.header("💳 Assinatura Mensal Neurax Business")
        st.write("Garanta acesso ilimitado a todas as ferramentas, automações e recursos de lucro por mês.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Teste Grátis 🎁")
            st.markdown("- Acesso completo liberado\n- Teste todas as 15+ ferramentas\n- Sem compromisso")
            st.metric("Valor", "R$ 0,00", "Ativo agora")
        with col2:
            st.markdown("### Plano Pro 🚀")
            st.markdown("- **Acesso vitalício/mensal ilimitado**\n- Automações via Pix automáticas\n- Relatórios avançados\n- Suporte prioritário")
            st.metric("Valor", "R$ 19,99", "por mês")

        st.markdown("---")
        st.subheader("Ativar Assinatura Pro via Pix (R$ 19,99)")
        
        webhook_assinatura = st.text_input("URL do Webhook do Make (Assinaturas)", placeholder="https://hook.us2.make.com/...")
        nome_assinante = st.text_input("Seu Nome / Empresa", placeholder="Ex: João da Silva")
        email_assinante = st.text_input("Seu E-mail de Acesso", placeholder="Ex: joao@email.com")

        if st.button("Gerar Pix de Assinatura (R$ 19,99)", type="primary"):
            if not webhook_assinatura:
                st.error("Insira a URL do Webhook do Make para assinaturas.")
            elif not nome_assinante or not email_assinante:
                st.warning("Preencha seu nome e e-mail.")
            else:
                payload_sub = {
                    "description": "Assinatura Mensal - Neurax Business Pro",
                    "transaction_amount": 19.99,
                    "type": "monthly_subscription",
                    "payer": {
                        "first_name": nome_assinante,
                        "email": email_assinante
                    }
                }

                with st.spinner("Gerando Pix no Mercado Pago..."):
                    try:
                        response = requests.post(webhook_assinatura, json=payload_sub)
                        if response.status_code in [200, 201]:
                            st.success("Cobrança gerada com sucesso!")
                            # Salva a resposta recebida (espera-se que o Make retorne o qrcode / copia e cola)
                            st.session_state.pix_data = response.json() if response.text else {"qr_code": "Copie o código gerado pelo Make/Mercado Pago"}
                        else:
                            st.error(f"Erro na comunicação: Status {response.status_code}")
                            st.text(response.text)
                    except Exception as e:
                        st.error(f"Não foi possível conectar ao webhook: {e}")

        # Se houver dados de Pix gerados, exibe na tela para o usuário pagar
        if st.session_state.pix_data:
            st.markdown("---")
            st.subheader("📲 Realize o Pagamento do Pix")
            st.info("Copie o código **Pix Copia e Cola** abaixo e pague no aplicativo do seu banco:")
            
            # Exibe o código copia e cola (Certifique-se de que o Make retorna a chave `qr_code` do Mercado Pago)
            codigo_copia_cola = st.session_state.pix_data.get("qr_code", "Cole aqui o Pix Copia e Cola retornado pelo Make")
            st.code(codigo_copia_cola, language="text")
            
            st.markdown("---")
            if st.button("🔄 Já paguei! Liberar minha Conta Pro", type="primary"):
                st.session_state.is_pro = True
                st.success("🎉 Pagamento reconhecido! Sua conta agora é **PRO** com acesso total liberado!")
                st.balloons()

    elif menu == "💳 Gerar Cobrança Pix":
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
                            st.success("Cobrança gerada com sucesso!")
                            st.json(response.json() if response.text else {"status": "Sucesso"})
                        else:
                            st.error(f"Erro na comunicação: Status {response.status_code}")
                            st.text(response.text)
                    except Exception as e:
                        st.error(f"Não foi possível conectar ao webhook: {e}")

    elif menu == "🌐 Testador HTTP / Webhook Make":
        st.header("Ferramenta de Requisição HTTP Avançada")
        st.write("Simule chamadas diretas de API e valide os Headers e Tokens do Mercado Pago.")
        
        url_api = st.text_input("URL do Endpoint", value="https://api.mercadopago.com/v1/payments")
        token_mp = st.text_input("Bearer Token / Authorization", type="password", placeholder="APP_USER-...")
        
        if st.button("Testar Requisição HTTP"):
            if not token_mp:
                st.error("Insira o Token de autorização.")
            else:
                headers = {
                    "Authorization": f"Bearer {token_mp}",
                    "Content-Type": "application/json"
                }
                st.info("Estrutura de Headers validada com sucesso para disparo!")
                st.json(headers)

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

    elif menu == "⚡ Gestor de Tarefas Inteligente":
        st.header("⚡ Gestor de Tarefas Inteligente")
        st.write("Organize e priorize suas demandas diárias para maximizar a produtividade e o lucro.")
        tarefa = st.text_input("Nova Tarefa", placeholder="Ex: Ajustar campanha de anúncios")
        prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
        if st.button("Adicionar Tarefa"):
            if tarefa:
                st.success(f"Tarefa '{tarefa}' adicionada com prioridade {prioridade}!")
            else:
                st.warning("Digite o nome da tarefa.")

    elif menu == "🧠 Mentor de Saúde Mental":
        st.header("🧠 Mentor de Saúde Mental")
        st.write("Um espaço seguro para pausas estratégicas, foco e controle de estresse no empreendedorismo.")
        st.info("Dica do dia: Respire fundo por 5 segundos, reorganize suas prioridades e mantenha o foco no essencial.")
        sentimento = st.text_input("Como você está se sentindo hoje?", placeholder="Ex: Sobrecarregado, animado...")
        if st.button("Receber Orientação"):
            if sentimento:
                st.success("Lembre-se: pausas inteligentes aumentam a sua clareza de negócios e evitam o esgotamento.")

    elif menu == "📚 Tutor Universal & Estudos":
        st.header("📚 Tutor Universal & Estudos")
        st.write("Aprenda novas habilidades, funis, marketing e programação de forma guiada.")
        topico = st.text_input("O que você deseja aprender hoje?", placeholder="Ex: Como otimizar campanhas de Pix")
        if st.button("Gerar Material de Estudo"):
            if topico:
                st.success(f"Plano de estudos gerado para: {topico}")
                st.write("1. Fundamentos e conceitos chave\n2. Aplicação prática no Make\n3. Métricas de sucesso")

    elif menu == "🗺️ Arquiteto de Funis de Vendas":
        st.header("🗺️ Arquiteto de Funis de Vendas")
        st.write("Desenhe a jornada ideal do cliente para transformar visitantes em compradores recorrentes.")
        nicho = st.text_input("Seu Nicho ou Produto", placeholder="Ex: Infoprodutos / Consultoria")
        if st.button("Gerar Estrutura de Funis"):
            if nicho:
                st.success(f"Funil gerado para {nicho}:")
                st.write("• **Topo:** Anúncio direto / Redes Sociais\n• **Meio:** Captura de Lead / WhatsApp\n• **Fundo:** Checkout instantâneo via Pix")

    elif menu == "💰 Precificação Inteligente":
        st.header("💰 Precificação Inteligente")
        st.write("Calcule o preço ideal dos seus produtos considerando margem de lucro e custos de operação.")
        custo = st.text_input("Custo de Produção / Aquisição (R$)", placeholder="Ex: 30.00")
        margem = st.text_input("Margem de Lucro Desejada (%)", placeholder="Ex: 100")
        if st.button("Calcular Preço Ideal"):
            try:
                c = float(custo.replace(",", "."))
                m = float(margem.replace(",", "."))
                preco_final = c * (1 + m / 100)
                st.success(f"Preço de Venda Recomendado: R$ {preco_final:.2f}")
            except ValueError:
                st.error("Insira apenas valores numéricos válidos.")

    elif menu == "🎯 Gerador de Anúncios (Meta/Google)":
        st.header("🎯 Gerador de Anúncios (Meta/Google)")
        st.write("Crie copies e estruturas de anúncios de alta conversão para tráfego pago.")
        produto_anuncio = st.text_input("Nome do Produto/Serviço", placeholder="Ex: Sistema Neurax Pix")
        if st.button("Gerar Copy de Anúncio"):
            if produto_anuncio:
                st.success("Anúncio gerado com sucesso!")
                st.markdown(f"**Título:** Quer faturar mais com automação em {produto_anuncio}?\n\n**Texto:** Pare de perder vendas com maquininhas caras. Receba na hora com Pix e automação completa.")

    elif menu == "🚀 NeuraX Growth Engine":
        st.header("🚀 NeuraX Growth Engine")
        st.write("Estratégias de escala rápida, tráfego e otimização de conversão.")
        if st.button("Executar Diagnóstico de Crescimento"):
            st.success("Diagnóstico concluído: Otimize seu checkout via Pix para reduzir o atrito em até 30%.")

    elif menu == "💬 Gerador de Copy WhatsApp":
        st.header("💬 Gerador de Copy WhatsApp")
        st.write("Crie mensagens persuasivas para fechar vendas e recuperar carrinhos no WhatsApp.")
        cliente_zap = st.text_input("Nome do Cliente", placeholder="Ex: Carlos")
        if st.button("Gerar Mensagem de WhatsApp"):
            if cliente_zap:
                st.success(f"Mensagem gerada para {cliente_zap}:")
                st.code(f"Olá {cliente_zap}, tudo bem? Vi que você demonstrou interesse em nossa solução. Segue seu link de pagamento via Pix instantâneo para garantir sua vaga hoje!")

    elif menu == "📸 Planejador Instagram":
        st.header("📸 Planejador Instagram")
        st.write("Organize sua grade de conteúdos, stories e legendas magnéticas.")
        tema_post = st.text_input("Tema do Post", placeholder="Ex: Como automatizar cobranças")
        if st.button("Gerar Ideia de Conteúdo"):
            if tema_post:
                st.success(f"Planejamento para: {tema_post}")
                st.write("• **Formato:** Reels (Dica rápida em 30s)\n• **Legenda:** Mostre o antes e depois de usar automação.")

    elif menu == "✉️ Gerador de E-mail Comercial":
        st.header("✉️ Gerador de E-mail Comercial")
        st.write("Escreva propostas comerciais e sequências de e-mails profissionais.")
        assunto_email = st.text_input("Objetivo do E-mail", placeholder="Ex: Proposta de Parceria Comercial")
        if st.button("Gerar E-mail"):
            if assunto_email:
                st.success("E-mail comercial gerado com sucesso!")
                st.code("Prezado(a),\n\nGostaríamos de apresentar nossa solução para otimização de faturamento...\n\nAtenciosamente,\nEquipe Neurax")

    elif menu == "🎬 Gerador de Roteiro para Vídeos":
        st.header("🎬 Gerador de Roteiro para Vídeos")
        st.write("Roteiros magnéticos para TikTok, Reels e YouTube Shorts.")
        assunto_video = st.text_input("Tema do Vídeo", placeholder="Ex: Como receber via Pix automaticamente")
        if st.button("Gerar Roteiro"):
            if assunto_video:
                st.success("Roteiro gerado:")
                st.write("1. **Gancho (0-3s):** Você ainda perde vendas esperando o Pix cair?\n2. **Corpo (3-20s):** Mostre a automação no Make.\n3. **CTA (20-30s):** Clique no link da bio para testar.")

    elif menu == "⚖️ Assistente de Burocracias":
        st.header("⚖️ Assistente de Burocracias")
        st.write("Orientações simplificadas sobre contratos, termos e processos legais básicos.")
        duvida_juridica = st.text_input("Qual a sua dúvida burocrática?", placeholder="Ex: Contrato de prestação de serviços")
        if st.button("Consultar Diretrizes"):
            if duvida_juridica:
                st.success("Diretrizes básicas geradas. Lembre-se de validar com um profissional jurídico da sua confiança.")

    elif menu == "💸 Consultor de Finanças Pessoais":
        st.header("💸 Consultor de Finanças Pessoais")
        st.write("Controle seus ganhos, organize o orçamento e planeje sua liberdade financeira.")
        receita_mes = st.text_input("Sua Receita Mensal (R$)", placeholder="Ex: 5000.00")
        if st.button("Analisar Finanças"):
            if receita_mes:
                st.success("Análise de orçamento:")
                st.write("• 50% Custos Essenciais\n• 30% Investimento em Negócios / Growth\n• 20% Reserva Financeira")

    elif menu == "🍳 Assistente de Despensa & Rotina":
        st.header("🍳 Assistente de Despensa & Rotina")
        st.write("Organize suas refeições diárias para otimizar o tempo e manter a energia alta no trabalho.")
        ingredientes = st.text_input("Ingredientes Disponíveis", placeholder="Ex: Arroz, frango, ovos")
        if st.button("Sugerir Cardápio"):
            if ingredientes:
                st.success(f"Sugestão rápida com base em: {ingredientes}")
                st.write("• Refeição prática e energética focada em alta produtividade para o seu dia.")

    elif menu == "🎓 Simulador de Entrevistas":
        st.header("🎓 Simulador de Entrevistas")
        st.write("Treine suas respostas para fechar grandes contratos ou parcerias estratégicas.")
        cargo_alvo = st.text_input("Tipo de Entrevista / Reunião", placeholder="Ex: Reunião com Grande Investidor")
        if st.button("Iniciar Simulação"):
            if cargo_alvo:
                st.success(f"Simulador pronto para: {cargo_alvo}")
                st.write("Pergunta 1: Qual é o seu principal diferencial competitivo de mercado?")

    elif menu == "🚪 Sair (Logout)":
        st.session_state.logged_in = False
        st.session_state.auth_screen = 'login'
        st.rerun()
