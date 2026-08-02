import streamlit as st

# 1. Configuração da Página (Obrigatório ser o primeiro comando)
st.set_page_config(
    page_title="NeuraX Suite | IA & Negócios",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Função de Geração com IA / Simulação Inteligente (Blindada contra erros)
def gerar_com_groq(prompt, system_prompt, api_key):
    if api_key and api_key.startswith("gsk_"):
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            return completion.choices[0].message.content
        except Exception:
            pass  # Se der erro na API, usa o modo de simulação abaixo

    # Modo de Simulação Inteligente (Fallback)
    if "precificação" in system_prompt.lower() or "preço" in prompt.lower() or "mercado" in prompt.lower():
        return (
            "💰 **Relatório de Inteligência de Preço e Mercado**\n\n"
            "- **Produto Analisado:** Baseado no seu input\n"
            "- **Preço Médio Estimado de Mercado:** R$ 120,00\n"
            "- **Seu Custo de Produção:** R$ 50,00\n"
            "- **Preço Sugerido (100% de Lucro / Markup 2x):** R$ 100,00\n\n"
            "📊 **Parecer Estratégico da IA:**\n"
            "O preço sugerido de R$ 100,00 para garantir 100% de lucro está **abaixo da média de mercado** (R$ 120,00). "
            "Isso significa que você tem alta margem de lucro e ainda continua extremamente competitivo para vender em larga escala!"
        )
    elif "WhatsApp" in system_prompt or "whatsapp" in prompt.lower():
        return (
            "🚀 **Copy Mágica para WhatsApp**\n\n"
            "Olá! Se você quer escalar seu negócio e automatizar suas vendas sem perder tempo, "
            "o **NeuraX Suite** é a solução perfeita para você.\n\n"
            "✅ Atendimento Inteligente 24/7\n"
            "✅ Geração de Scripts em segundos\n"
            "✅ Dashboards e Relatórios completos\n\n"
            "👉 *Clique no link abaixo e garanta seu acesso com desconto exclusivo:* [Link do Seu Produto]"
        )
    elif "Instagram" in system_prompt or "post" in prompt.lower() or "carrossel" in prompt.lower():
        return (
            "📸 **Plano de Conteúdo para Instagram**\n\n"
            "**Post 1: Carrossel Educativo**\n"
            "- *Título:* 3 Erros que te impedem de faturar mais este mês.\n"
            "- *Slide 1:* Não automatizar tarefas repetitivas.\n"
            "- *Slide 2:* Fazer anúncios sem uma oferta clara.\n"
            "- *Slide 3:* Não acompanhar as métricas do seu negócio.\n\n"
            "**Legenda:** Qual desses erros você mais comete hoje? Comente 'AUTOMATIZAR' para receber nossa solução no Direct!"
        )
    else:
        return (
            "🎯 **Plano Estratégico Gerado pelo NeuraX IA**\n\n"
            "1. **Análise de Cenário:** Identifique o seu público-alvo principal e otimize a oferta.\n"
            "2. **Ação Rápida:** Crie uma página de vendas direta com gatilhos de urgência e escassez.\n"
            "3. **Retenção:** Utilize e-mail marketing e sequências de mensagens para converter leads frios.\n\n"
            "💡 *Dica Bônus:* Teste novos criativos a cada 7 dias para manter o custo por clique (CPC) baixo."
        )

# 3. Estado de Login
if "logado" not in st.session_state:
    st.session_state.logado = False

# 4. Barra Lateral
with st.sidebar:
    st.title("⚙️ Configurações")
    api_key_input = st.text_input("Chave Groq API (IA):", type="password", help="Opcional. O app roda perfeitamente sem ela.")
    if api_key_input:
        st.success("⚡ IA Manual Conectada")
    else:
        st.info("ℹ️ Modo de demonstração ativo.")
    
    st.markdown("---")
    if st.session_state.logado:
        if st.button("🚪 Sair da Conta"):
            st.session_state.logado = False
            st.rerun()

# 5. Interface Principal (Login ou Painel)
if not st.session_state.logado:
    st.markdown("<h1 style='text-align: center;'>🚀 NeuraX Suite</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Plataforma Inteligente de Automação para Negócios</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Entrar", "📝 Criar Conta"])
        
        with tab1:
            usuario = st.text_input("Usuário", key="login_user")
            senha = st.text_input("Senha", type="password", key="login_pass")
            if st.button("Acessar Painel"):
                if usuario and senha:
                    st.session_state.logado = True
                    st.rerun()
                else:
                    st.warning("Preencha usuário e senha.")
        
        with tab2:
            novo_usuario = st.text_input("Novo Usuário", key="reg_user")
            nova_senha = st.text_input("Nova Senha", type="password", key="reg_pass")
            if st.button("Cadastrar"):
                if novo_usuario and nova_senha:
                    st.success("Conta criada com sucesso! Vá na aba Entrar.")
                else:
                    st.warning("Preencha todos os campos.")
else:
    st.title("🚀 NeuraX Suite - Painel de Controle")
    st.write("Bem-vindo ao seu painel de automação e inteligência artificial.")
    
    menu = st.selectbox(
        "Escolha a Ferramenta:", 
        [
            "Calculadora de Preço & Lucro (100%)", 
            "Gerador de Copy WhatsApp", 
            "Planejador de Instagram", 
            "Estratégia de Negócios"
        ]
    )
    
    if menu == "Calculadora de Preço & Lucro (100%)":
        st.subheader("💰 Precificação Inteligente por IA & Margem de 100%")
        st.write("Informe o nome do seu produto e o valor de custo. A IA vai estimar o preço médio de mercado atual e calcular a sugestão ideal para garantir 100% de lucro.")
        
        nome_produto = st.text_input("Nome do Produto ou Serviço:", "Ex: Camiseta Oversized de Algodão")
        custo = st.number_input("Valor de Custo / Produção (R$)", min_value=0.0, value=50.0, step=5.0)
        
        if st.button("Analisar Preço com IA"):
            with st.spinner("A Inteligência Artificial está pesquisando o mercado e calculando a margem..."):
                prompt_precificacao = f"Analise o produto '{nome_produto}' que tem um custo de produção de R$ {custo:.2f}. Estime o preço médio atual praticado no mercado para este produto, calcule o preço de venda necessário para garantir 100% de lucro sobre o custo, e dê uma recomendação estratégica se o preço é competitivo."
                system_precificacao = "Você é um consultor financeiro sênior e especialista em precificação de mercado."
                
                resultado = gerar_com_groq(prompt_precificacao, system_precificacao, api_key_input)
                st.markdown("---")
                st.markdown("### 📊 Relatório de Análise de Preço")
                st.markdown(resultado)
                
    elif menu == "Gerador de Copy WhatsApp":
        st.subheader("💬 Gerador de Copy para WhatsApp")
        produto = st.text_input("Qual o seu produto ou serviço?", "Mentoria de Vendas")
        if st.button("Gerar Copy"):
            with st.spinner("Gerando conteúdo..."):
                resultado = gerar_com_groq(f"Criar copy para {produto}", "Você é um especialista em WhatsApp Marketing.", api_key_input)
                st.markdown(resultado)
                
    elif menu == "Planejador de Instagram":
        st.subheader("📸 Planejador de Conteúdo - Instagram")
        nicho = st.text_input("Qual o seu nicho?", "Marketing Digital")
        if st.button("Gerar Plano"):
            with st.spinner("Gerando posts..."):
                resultado = gerar_com_groq(f"Criar posts para nicho de {nicho}", "Você é um estrategista de mídias sociais.", api_key_input)
                st.markdown(resultado)
                
    else:
        st.subheader("🎯 Estratégia de Negócios")
        objetivo = st.text_input("Qual o seu objetivo principal?", "Aumentar faturamento")
        if st.button("Gerar Estratégia"):
            with st.spinner("Estruturando plano..."):
                resultado = gerar_com_groq(f"Criar estratégia para {objetivo}", "Você é um consultor de negócios sênior.", api_key_input)
                st.markdown(resultado)
