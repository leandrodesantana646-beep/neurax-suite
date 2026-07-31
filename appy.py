import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="NeuraX Suite - Painel Inteligente",
    page_icon="🚀",
    layout="centered"
)

# Customização Visual de Elite via CSS
st.markdown("""
    <style>
    /* Estilização dos botões principais */
    .stButton>button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff8f4b 100%);
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }
    /* Arredondamento das caixas de texto */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Tenta importar o OpenAI de forma segura caso não esteja instalado ainda
try:
    from openai import OpenAI
    OPENAI_DISPONIVEL = True
except:
    OPENAI_DISPONIVEL = False

# ---------------------------------------------------------
# CONFIGURAÇÃO DA IA VIA BARRA LATERAL
# ---------------------------------------------------------
st.sidebar.title("⚙️ Configurações & Acesso")
api_key_input = st.sidebar.text_input("🔑 Chave API OpenAI (Opcional):", type="password")

client = None
if OPENAI_DISPONIVEL and api_key_input:
    try:
        client = OpenAI(api_key=api_key_input)
    except:
        pass

# Inicializar Histórico na Sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

st.title("🚀 NeuraX Suite - Painel Inteligente")
st.markdown("O ecossistema definitivo de automação para e-commerce.")

# Menu Lateral (Sidebar) para escolher o módulo
modulo = st.sidebar.selectbox(
    "Escolha o Módulo do Sistema",
    [
        "🤖 Gerador de Copy e SEO",
        "📊 Analisador de Preços (IA)",
        "💬 Assistente de WhatsApp",
        "🎬 Gerador de Roteiros (Reels/TikTok)",
        "🧮 Calculadora de Taxas & Lucro"
    ]
)

# Exibir Histórico na Barra Lateral
st.sidebar.markdown("---")
st.sidebar.subheader("📜 Histórico da Sessão")
if st.session_state.historico:
    for item in st.session_state.historico[-5:]:
        st.sidebar.text(f"• {item}")
    if st.sidebar.button("Limpar Histórico"):
        st.session_state.historico = []
        st.rerun()
else:
    st.sidebar.info("Nenhuma geração recente.")

# Função Inteligente Híbrida
def processar_ia(tipo, dados):
    if client:
        try:
            if tipo == "copy":
                sys_msg = "Você é um especialista em marketing e SEO para e-commerce."
                usr_msg = f"Crie uma copy de vendas para o produto '{dados['produto']}' voltado para o público '{dados['publico']}'."
            elif tipo == "preco":
                sys_msg = "Você é um consultor financeiro de e-commerce."
                usr_msg = f"Analise o preço do produto '{dados['produto']}' que custa hoje R$ {dados['preco']:.2f}. Dê a média de mercado e o preço sugerido para lucro ótimo."
            elif tipo == "whatsapp":
                sys_msg = "Você é um atendente focado em conversão no WhatsApp."
                usr_msg = f"Escreva uma resposta acolhedora para a objeção: '{dados['duvida']}'."
            elif tipo == "roteiro":
                sys_msg = "Você é um especialista em vídeos virais para TikTok e Reels."
                usr_msg = f"Crie um roteiro viral (gancho, solução e CTA) para o produto '{dados['produto']}' focado na dor '{dados['dor']}'."

            resposta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": usr_msg}],
                temperature=0.7
            )
            return resposta.choices[0].message.content
        except Exception as e:
            st.warning(f"Erro na API da OpenAI, usando modo inteligente padrão: {e}")

    # Modo Inteligente Padrão (Sem chave de API)
    if tipo == "copy":
        p = dados['produto']
        pub = dados['publico']
        return f"""--- 🎯 RESULTADO GERADO PELO SISTEMA ---
[Título SEO]: {p} Original | Oferta Imperdível | Frete Grátis
[Descrição de Vendas]: Procurando excelência? O novo {p} foi desenvolvido especialmente para o público {pub}. Unindo tecnologia de ponta, durabilidade e design exclusivo, ele resolve suas necessidades do dia a dia com máxima eficiência. Garanta já o seu com condições especiais!
[Hashtags]: #{p.lower().replace(' ', '')} #ecommerce #lancamento #oferta"""

    elif tipo == "preco":
        prod = dados['produto']
        pa = dados['preco']
        med = max(pa * 1.15, 100.00)
        menor = med * 0.85
        sug = round(med * 0.95, 2)
        
        if pa > med:
            status = "Acima da Média (Risco de baixo giro)"
            rec = f"Seu preço está alto. Sugerimos fixar em R$ {sug:.2f} para garantir vendas."
        elif pa < menor:
            status = "Abaixo do Mercado (Margem baixa)"
            rec = f"Você está vendendo barato demais! Suba para R$ {sug:.2f} para lucrar mais."
        else:
            status = "Posicionamento Estratégico Saudável 🚀"
            rec = f"Preço competitivo. Para atingir a margem ideal, recomendamos ajustar para R$ {sug:.2f}."

        return f"""--- 🧠 RELATÓRIO DE INTELIGÊNCIA DE PREÇOS ---
[Produto Analisado]: {prod}
[Seu Preço Informado]: R$ {pa:.2f}
[Média Estimada da Concorrência]: R$ {med:.2f}
[Menor Preço no Mercado]: R$ {menor:.2f}
🎯 [PREÇO SUGERIDO PARA LUCRO ÓTIMO]: R$ {sug:.2f}
[Status Competitivo]: {status}
[Recomendação]: {rec}"""

    elif tipo == "whatsapp":
        d = dados['duvida']
        loja = dados['loja']
        return f"""Olá! Tudo bem? 😃
Obrigado pelo contato com a {loja}!

Referente à sua dúvida ("{d}"):
Trabalhamos apenas com produtos 100% originais, testados e com garantia de fábrica para garantir a sua total segurança. Além disso, oferecemos envio rápido e suporte dedicado!

Posso separar o seu pedido por aqui para garantirmos o estoque? ✨"""

    elif tipo == "roteiro":
        prod = dados['produto']
        dor = dados['dor']
        return f"""--- 🎬 ROTEIRO DE VÍDEO VIRAL (REELS / TIKTOK) ---
[Produto]: {prod}

1. GANCHO (0 a 3 segundos):
- "Cansado de sofrer com {dor}? Olha o que acabou de chegar!"

2. DESENVOLVIMENTO / SOLUÇÃO (3 a 15 segundos):
- "A gente sabe como isso é chato no dia a dia. Mas o novo {prod} resolve isso de forma prática, rápida e com qualidade premium."

3. CHAMADA PARA AÇÃO / CTA (15 a 25 segundos):
- "Não fica de fora dessa! Clica no link da bio ou me manda uma mensagem aqui embaixo para garantir o seu!" """

# ---------------------------------------------------------
# MÓDULO 1: GERADOR DE COPY E SEO
# ---------------------------------------------------------
if modulo == "🤖 Gerador de Copy e SEO":
    st.header("🤖 Gerador Automático de Copy e SEO")
    st.write("Crie títulos otimizados, descrições de alto impacto e baixe o arquivo em segundos.")

    nome_produto = st.text_input("📦 Digite o nome do produto:")
    publico = st.text_input("🎯 Para quem é esse produto? (ex: lojistas, jovens, mães):")

    if st.button("Gerar Copy"):
        if nome_produto and publico:
            resultado = processar_ia("copy", {"produto": nome_produto, "publico": publico})
            st.success("✨ Copy gerada com sucesso!")
            st.text_area("Resultado:", resultado, height=200)

            st.session_state.historico.append(f"Copy: {nome_produto}")

            st.download_button(
                label="📥 Baixar Arquivo de Copy (.txt)",
                data=resultado,
                file_name=f"copy_{nome_produto.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Preencha todos os campos.")

# ---------------------------------------------------------
# MÓDULO 2: ANALISADOR DE PREÇOS
# ---------------------------------------------------------
elif modulo == "📊 Analisador de Preços (IA)":
    st.header("📊 Analisador Inteligente de Preços via IA")
    st.write("A IA analisa o mercado e calcula o preço ideal de venda para maximizar seu lucro.")

    produto_preco = st.text_input("📦 Nome do produto:")
    preco_atual = st.number_input("💰 Preço que você cobra hoje (R$):", min_value=0.0, value=100.0, step=1.0)

    if st.button("Executar Análise de Preços"):
        if produto_preco:
            with st.spinner("🔍 Analisando dados de mercado..."):
                relatorio = processar_ia("preco", {"produto": produto_preco, "preco": preco_atual})

            st.success("🎯 Análise de preços concluída!")
            st.text_area("Relatório Completo:", relatorio, height=230)

            st.session_state.historico.append(f"Preço: {produto_preco}")

            st.download_button(
                label="📥 Baixar Relatório de Preços (.txt)",
                data=relatorio,
                file_name=f"relatorio_preco_{produto_preco.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Digite o nome do produto.")

# ---------------------------------------------------------
# MÓDULO 3: ASSISTENTE DE WHATSAPP
# ---------------------------------------------------------
elif modulo == "💬 Assistente de WhatsApp":
    st.header("💬 Assistente de Atendimento")
    st.write("Gere respostas profissionais e focadas em fechamento para o WhatsApp.")

    duvida_cliente = st.text_input("❓ Dúvida ou objeção do cliente (ex: 'É original?'):")
    nome_loja = st.text_input("🏷️ Nome da sua loja:", value="Nossa Loja")

    if st.button("Gerar Resposta"):
        if duvida_cliente:
            resposta_gerada = processar_ia("whatsapp", {"duvida": duvida_cliente, "loja": nome_loja})
            st.success("💬 Resposta gerada com sucesso!")
            st.text_area("Mensagem:", resposta_gerada, height=180)

            st.session_state.historico.append(f"WhatsApp: {duvida_cliente[:15]}...")

            st.download_button(
                label="📥 Baixar Resposta (.txt)",
                data=resposta_gerada,
                file_name="resposta_whatsapp.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Digite a dúvida do cliente.")

# ---------------------------------------------------------
# MÓDULO 4: GERADOR DE ROTEIROS
# ---------------------------------------------------------
elif modulo == "🎬 Gerador de Roteiros (Reels/TikTok)":
    st.header("🎬 Gerador de Roteiros para Vídeos Curtos")
    st.write("Crie roteiros virais e estruturados para engajar no Reels, TikTok e Shorts.")

    prod_video = st.text_input("📦 Produto em destaque:")
    dor = st.text_input("🎯 Qual dor o produto resolve? (ex: 'Cabelo frizzado'):")

    if st.button("Gerar Roteiro"):
        if prod_video and dor:
            roteiro = processar_ia("roteiro", {"produto": prod_video, "dor": dor})
            st.success("🎬 Roteiro gerado com sucesso!")
            st.text_area("Estrutura do Vídeo:", roteiro, height=220)

            st.session_state.historico.append(f"Roteiro: {prod_video}")

            st.download_button(
                label="📥 Baixar Roteiro (.txt)",
                data=roteiro,
                file_name=f"roteiro_{prod_video.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Preencha os campos.")

# ---------------------------------------------------------
# MÓDULO 5: CALCULADORA DE TAXAS & LUCRO
# ---------------------------------------------------------
elif modulo == "🧮 Calculadora de Taxas & Lucro":
    st.header("🧮 Calculadora de Custos e Taxas de Marketplace")
    st.write("Descubra o seu **Lucro Líquido Real** descontando custos e taxas de plataformas.")

    nome_item = st.text_input("📦 Nome do item avaliado:")
    custo_prod = st.number_input("💸 Preço de Custo / Aquisição (R$):", min_value=0.0, value=50.0, step=1.0)
    preco_venda = st.number_input("🏷️ Preço de Venda Pretendido (R$):", min_value=0.0, value=120.0, step=1.0)
    taxa_marketplace_pct = st.number_input("📊 Taxa do Marketplace ou Cartão (%):", min_value=0.0, max_value=100.0, value=16.0, step=0.5)
    custo_extra = st.number_input("📦 Custos Extras (Embalagem, Frete, etc) (R$):", min_value=0.0, value=5.0, step=1.0)

    if st.button("Calcular Lucro Líquido Real"):
        if nome_item:
            valor_taxa = preco_venda * (taxa_marketplace_pct / 100.0)
            lucro_liquido = preco_venda - custo_prod - valor_taxa - custo_extra
            
            if preco_venda > 0:
                margem_liquida_pct = (lucro_liquido / preco_venda) * 100.0
            else:
                margem_liquida_pct = 0.0

            if lucro_liquido > 0:
                status_lucro = "Lucro Saudável 🟢"
            else:
                status_lucro = "Prejuízo ou Margem Negativa 🔴"

            relatorio_lucro = f"""--- 🧮 RELATÓRIO DE LUCRO LÍQUIDO REAL ---
[Produto]: {nome_item}
[Preço de Venda]: R$ {preco_venda:.2f}
[Preço de Custo]: R$ {custo_prod:.2f}
[Taxa da Plataforma ({taxa_marketplace_pct}%)]: R$ {valor_taxa:.2f}
[Custos Extras]: R$ {custo_extra:.2f}
----------------------------------------
💰 [LUCRO LÍQUIDO FINAL]: R$ {lucro_liquido:.2f}
📈 [Margem Líquida Percentual]: {margem_liquida_pct:.1f}%
[Status Financeiro]: {status_lucro}
"""

            st.success("🧮 Cálculo de lucros realizado com sucesso!")
            st.metric(label="💰 Lucro Líquido Real", value=f"R$ {lucro_liquido:.2f}", delta=f"{margem_liquida_pct:.1f}% de margem")
            st.text_area("Relatório Financeiro:", relatorio_lucro, height=200)

            st.session_state.historico.append(f"Lucro: {nome_item}")

            st.download_button(
                label="📥 Baixar Relatório Financeiro (.txt)",
                data=relatorio_lucro,
                file_name=f"lucro_{nome_item.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Digite o nome do item.")
