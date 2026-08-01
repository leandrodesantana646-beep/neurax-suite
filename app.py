import streamlit as st

# Tenta importar o cliente Groq
try:
    from groq import Groq
    TEM_GROQ = True
except ImportError:
    TEM_GROQ = False

# Configuração da Página
st.set_page_config(
    page_title="NeuraX Suite - Painel Inteligente",
    page_icon="🚀",
    layout="centered"
)

# Customização Visual de Elite & Efeito Cards
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Estilização dos botões principais com gradiente moderno */
    .stButton>button {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff8f4b 100%);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255, 75, 75, 0.4);
    }

    /* Campos de entrada com bordas refinadas */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 10px;
        border: 1px solid #30363d;
        background-color: #0d1117;
    }
    
    /* Efeito de destaque nas caixas de texto de resultado */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #30363d;
        background-color: #0d1117;
        color: #58a6ff;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar Histórico na Sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

st.title("🚀 NeuraX Suite - Painel Inteligente")
st.markdown("O ecossistema definitivo de automação para e-commerce com Inteligência Artificial.")

# Configuração da Chave da API na Barra Lateral
st.sidebar.subheader("🔑 Configuração de IA")
groq_key_input = st.sidebar.text_input("Chave Groq API (Opcional):", type="password", help="Cole sua chave gratuita de console.groq.com para ativar IA real.")

if groq_key_input:
    st.sidebar.success("⚡ IA Real Ativada!")
else:
    st.sidebar.info("💡 Usando Modo Inteligente Padrão (Cole sua chave Groq para ativar IA completa).")

# Exibir Histórico na Barra Lateral
st.sidebar.markdown("---")
st.sidebar.subheader("📜 Histórico da Sessão")
if st.session_state.historico:
    for item in st.session_state.historico[-5:]:
        st.sidebar.text(f"• {item}")
    if st.sidebar.button("Limpar Histórico", key="btn_limpar"):
        st.session_state.historico = []
        st.rerun()
else:
    st.sidebar.info("Nenhuma geração recente.")

# Função central para chamar a IA do Groq
def gerar_resposta_ia(prompt_sistema, prompt_usuario):
    if not groq_key_input or not TEM_GROQ:
        return None
    try:
        client = Groq(api_key=groq_key_input)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Erro ao conectar com a IA: {e}")
        return None

# Organização por Abas Principais (st.tabs)
tab1, tab2, tab3 = st.tabs(["⚡ Vendas & Conversão", "✍️ Conteúdo & Marketing", "📊 Finanças & Precificação"])

# =========================================================
# ABA 1: VENDAS & CONVERSÃO
# =========================================================
with tab1:
    st.subheader("Ferramentas de Vendas")
    escolha_tab1 = st.selectbox("Escolha a ferramenta:", ["⚡ Campanha Flash Sale Instantânea", "💬 Assistente de WhatsApp"], key="sub_tab1")
    
    if escolha_tab1 == "⚡ Campanha Flash Sale Instantânea":
        st.write("Crie uma estratégia relâmpago completa (WhatsApp + Instagram + E-mail) gerada por IA.")
        prod_flash = st.text_input("📦 Nome do produto em promoção:", key="flash_prod")
        preco_original = st.number_input("💰 Preço original (R$):", min_value=0.0, value=200.0, step=1.0, key="flash_orig")
        preco_flash = st.number_input("🔥 Preço promocional relâmpago (R$):", min_value=0.0, value=149.0, step=1.0, key="flash_desc")
        tempo_limite = st.selectbox("⏳ Duração da Oferta", ["Apenas hoje (24 horas)", "48 horas", "Enquanto durar o estoque (Poucas unidades)"], key="flash_tempo")

        if st.button("Gerar Campanha Multicanal", key="btn_flash"):
            if prod_flash:
                economia = preco_original - preco_flash
                desconto_calc = int((economia / preco_original) * 100) if preco_original > 0 else 0

                # Tenta usar IA se houver chave
                prompt_ia = f"Crie uma campanha flash sale completa contendo: 1. Mensagem de WhatsApp persuasiva, 2. Sequência de 3 Stories para Instagram e 3. E-mail de vendas para o produto '{prod_flash}', vendido de R$ {preco_original:.2f} por R$ {preco_flash:.2f} ({desconto_calc}% de desconto), com duração de {tempo_limite}."
                kit_campanha = gerar_resposta_ia("Você é um especialista em copywriting e estratégias de vendas para e-commerce.", prompt_ia)

                # Fallback se não tiver chave
                if not kit_campanha:
                    kit_campanha = f"""========================================
⚡ KIT DE CAMPANHA FLASH SALE - {prod_flash.upper()}
========================================

1. 📱 MENSAGEM PARA GRUPO / VIP DO WHATSAPP:
----------------------------------------
🚨 ALERTA DE OFERTA RELÂMPAGO! 🚨
Galera, conseguimos liberar uma condição absurda para o {prod_flash} por tempo limitado ({tempo_limite})!
De: R$ {preco_original:.2f} | Por apenas: R$ {preco_flash:.2f} 😱 ({desconto_calc}% de desconto)
Clica aqui para garantir o seu antes que acabe: [INSERIR_LINK] 🛒✨

2. 📸 SEQUÊNCIA DE STORIES (INSTAGRAM):
- Story 1: "ALERTA DE QUEDA DE PREÇO! 🚨"
- Story 2: De R$ {preco_original:.2f} por R$ {preco_flash:.2f}! ({desconto_calc}% OFF)
- Story 3: "Últimas unidades! Corre no link."

3. 📧 E-MAIL MARKETING:
Assunto: ⏰ Corre! {prod_flash} com {desconto_calc}% de desconto ({tempo_limite})
Olá! O {prod_flash} saiu de R$ {preco_original:.2f} por R$ {preco_flash:.2f} por tempo limitado. Garanta o seu!
========================================"""

                st.success("🔥 Campanha relâmpago gerada com sucesso!")
                st.text_area("Pacote de Campanha Completo:", kit_campanha, height=300, key="txt_flash")
                st.session_state.historico.append(f"Flash Sale: {prod_flash}")
                st.download_button(label="📥 Baixar Campanha (.txt)", data=kit_campanha, file_name=f"campanha_{prod_flash.lower().replace(' ', '_')}.txt", mime="text/plain", key="dl_flash")
            else:
                st.warning("⚠️ Digite o nome do produto.")

    elif escolha_tab1 == "💬 Assistente de WhatsApp":
        st.write("Gere respostas profissionais e focadas em fechamento para o WhatsApp.")
        duvida_cliente = st.text_input("❓ Dúvida ou objeção do cliente (ex: 'É original?'):", key="wpp_duvida")
        nome_loja = st.text_input("🏷️ Nome da sua loja:", value="Nossa Loja", key="wpp_loja")

        if st.button("Gerar Resposta", key="btn_wpp"):
            if duvida_cliente:
                prompt_ia = f"Escreva uma resposta de WhatsApp amigável e persuasiva para uma loja chamada '{nome_loja}', respondendo à seguinte dúvida do cliente: '{duvida_cliente}'. A resposta deve gerar confiança e incentivar o fechamento da compra."
                resposta_gerada = gerar_resposta_ia("Você é um assistente de atendimento ao cliente de alta conversão para e-commerce.", prompt_ia)

                if not resposta_gerada:
                    resposta_gerada = f"""Olá! Tudo bem? 😃 Obrigado pelo contato com a {nome_loja}!
Referente à sua dúvida ("{duvida_cliente}"): Trabalhamos apenas com produtos originais e com garantia. Posso separar o seu pedido por aqui? ✨"""

                st.success("💬 Resposta gerada com sucesso!")
                st.text_area("Mensagem:", resposta_gerada, height=180, key="txt_wpp")
                st.session_state.historico.append(f"WhatsApp: {duvida_cliente[:15]}...")
                st.download_button(label="📥 Baixar Resposta (.txt)", data=resposta_gerada, file_name="resposta_whatsapp.txt", mime="text/plain", key="dl_wpp")
            else:
                st.warning("⚠️ Digite a dúvida do cliente.")

# =========================================================
# ABA 2: CONTEÚDO & MARKETING
# =========================================================
with tab2:
    st.subheader("Ferramentas de Conteúdo & Copywriting")
    escolha_tab2 = st.selectbox("Escolha a ferramenta:", ["🤖 Gerador de Copy e SEO", "🎬 Gerador de Roteiros (Reels/TikTok)"], key="sub_tab2")

    if escolha_tab2 == "🤖 Gerador de Copy e SEO":
        st.write("Crie títulos otimizados, descrições de alto impacto e hashtags.")
        nome_produto = st.text_input("📦 Digite o nome do produto:", key="copy_prod")
        publico = st.text_input("🎯 Para quem é esse produto? (ex: lojistas, jovens, mães):", key="copy_pub")

        if st.button("Gerar Copy", key="btn_copy"):
            if nome_produto and publico:
                prompt_ia = f"Crie um título otimizado para SEO, uma descrição de vendas persuasiva e hashtags relevantes para o produto '{nome_produto}' voltado para o público '{publico}'."
                resultado = gerar_resposta_ia("Você é um especialista em copywriting e SEO para e-commerce.", prompt_ia)

                if not resultado:
                    resultado = f"""--- 🎯 RESULTADO GERADO PELO SISTEMA ---
[Título SEO]: {nome_produto} Original | Oferta Imperdível | Frete Grátis
[Descrição de Vendas]: O novo {nome_produto} foi desenvolvido especialmente para o público {publico}. Alta qualidade e durabilidade para o seu dia a dia.
[Hashtags]: #{nome_produto.lower().replace(' ', '')} #ecommerce #oferta"""

                st.success("✨ Copy gerada com sucesso!")
                st.text_area("Resultado:", resultado, height=200, key="txt_copy")
                st.session_state.historico.append(f"Copy: {nome_produto}")
                st.download_button(label="📥 Baixar Copy (.txt)", data=resultado, file_name=f"copy_{nome_produto.lower().replace(' ', '_')}.txt", mime="text/plain", key="dl_copy")
            else:
                st.warning("⚠️ Preencha todos os campos.")

    elif escolha_tab2 == "🎬 Gerador de Roteiros (Reels/TikTok)":
        st.write("Crie roteiros virais e estruturados para engajar no Reels, TikTok e Shorts.")
        prod_video = st.text_input("📦 Produto em destaque:", key="vid_prod")
        dor = st.text_input("🎯 Qual dor o produto resolve? (ex: 'Cabelo frizzado'):", key="vid_dor")

        if st.button("Gerar Roteiro", key="btn_vid"):
            if prod_video and dor:
                prompt_ia = f"Crie um roteiro de vídeo curto (Reels/TikTok) dividido em Gancho (0-3s), Desenvolvimento/Solução (3-15s) e Chamada para Ação/CTA (15-25s) para o produto '{prod_video}' que resolve a dor: '{dor}'."
                roteiro = gerar_resposta_ia("Você é um criador de conteúdo especialista em vídeos virais e retenção.", prompt_ia)

                if not roteiro:
                    roteiro = f"""--- 🎬 ROTEIRO DE VÍDEO VIRAL ---
[Produto]: {prod_video}
1. GANCHO: "Cansado de sofrer com {dor}? Olha o que acabou de chegar!"
2. SOLUÇÃO: "O novo {prod_video} resolve isso de forma prática e rápida."
3. CTA: "Clica no link da bio para garantir o seu!" """

                st.success("🎬 Roteiro gerado com sucesso!")
                st.text_area("Estrutura do Vídeo:", roteiro, height=220, key="txt_vid")
                st.session_state.historico.append(f"Roteiro: {prod_video}")
                st.download_button(label="📥 Baixar Roteiro (.txt)", data=roteiro, file_name=f"roteiro_{prod_video.lower().replace(' ', '_')}.txt", mime="text/plain", key="dl_vid")
            else:
                st.warning("⚠️ Preencha os campos.")

# =========================================================
# ABA 3: FINANÇAS & PRECIFICAÇÃO
# =========================================================
with tab3:
    st.subheader("Ferramentas Financeiras & Precificação")
    escolha_tab3 = st.selectbox("Escolha a ferramenta:", ["📊 Analisador de Preços", "🧮 Calculadora de Taxas & Lucro"], key="sub_tab3")

    if escolha_tab3 == "📊 Analisador de Preços":
        st.write("Analise o mercado e calcule o preço ideal de venda.")
        produto_preco = st.text_input("📦 Nome do produto:", key="preco_prod")
        preco_atual = st.number_input("💰 Preço que você cobra hoje (R$):", min_value=0.0, value=100.0, step=1.0, key="preco_val")

        if st.button("Executar Análise de Preços", key="btn_preco"):
            if produto_preco:
                med = max(preco_atual * 1.15, 100.00)
                menor = med * 0.85
                sug = round(med * 0.95, 2)
                status = "Acima da Média" if preco_atual > med else ("Abaixo do Mercado" if preco_atual < menor else "Saudável 🚀")
                
                relatorio = f"""--- 🧠 RELATÓRIO DE INTELIGÊNCIA DE PREÇOS ---
[Produto Analisado]: {produto_preco}
[Seu Preço Informado]: R$ {preco_atual:.2f}
[Média Estimada da Concorrência]: R$ {med:.2f}
🎯 [PREÇO SUGERIDO PARA LUCRO ÓTIMO]: R$ {sug:.2f}
[Status Competitivo]: {status}"""
                st.success("🎯 Análise de preços concluída!")
                st.text_area("Relatório Completo:", relatorio, height=230, key="txt_preco")
                st.session_state.historico.append(f"Preço: {produto_preco}")
                st.download_button(label="📥 Baixar Relatório (.txt)", data=relatorio, file_name=f"relatorio_preco_{produto_preco.lower().replace(' ', '_')}.txt", mime="text/plain", key="dl_preco")
            else:
                st.warning("⚠️ Digite o nome do produto.")

    elif escolha_tab3 == "🧮 Calculadora de Taxas & Lucro":
        st.write("Descubra o seu **Lucro Líquido Real** descontando custos e taxas.")
        nome_item = st.text_input("📦 Nome do item avaliado:", key="lucro_item")
        custo_prod = st.number_input("💸 Preço de Custo / Aquisição (R$):", min_value=0.0, value=50.0, step=1.0, key="lucro_custo")
        preco_venda = st.number_input("🏷️ Preço de Venda Pretendido (R$):", min_value=0.0, value=120.0, step=1.0, key="lucro_venda")
        taxa_marketplace_pct = st.number_input("📊 Taxa do Marketplace ou Cartão (%):", min_value=0.0, max_value=100.0, value=16.0, step=0.5, key="lucro_taxa")
        custo_extra = st.number_input("📦 Custos Extras (Embalagem, Frete, etc) (R$):", min_value=0.0, value=5.0, step=1.0, key="lucro_extra")

        if st.button("Calcular Lucro Líquido Real", key="btn_lucro"):
            if nome_item:
                valor_taxa = preco_venda * (taxa_marketplace_pct / 100.0)
                lucro_liquido = preco_venda - custo_prod - valor_taxa - custo_extra
                margem_liquida_pct = (lucro_liquido / preco_venda) * 100.0 if preco_venda > 0 else 0.0
                status_lucro = "Lucro Saudável 🟢" if lucro_liquido > 0 else "Prejuízo ou Margem Negativa 🔴"

                relatorio_lucro = f"""--- 🧮 RELATÓRIO DE LUCRO LÍQUIDO REAL ---
[Produto]: {nome_item}
[Preço de Venda]: R$ {preco_venda:.2f}
[Preço de Custo]: R$ {custo_prod:.2f}
[Taxa da Plataforma ({taxa_marketplace_pct}%)]: R$ {valor_taxa:.2f}
[Custos Extras]: R$ {custo_extra:.2f}
----------------------------------------
💰 [LUCRO LÍQUIDO FINAL]: R$ {lucro_liquido:.2f}
📈 [Margem Líquida Percentual]: {margem_liquida_pct:.1f}%
[Status Financeiro]: {status_lucro}"""
                st.success("🧮 Cálculo de lucros realizado com sucesso!")
                st.metric(label="💰 Lucro Líquido Real", value=f"R$ {lucro_liquido:.2f}", delta=f"{margem_liquida_pct:.1f}% de margem")
                st.text_area("Relatório Financeiro:", relatorio_lucro, height=200, key="txt_lucro")
                st.session_state.historico.append(f"Lucro: {nome_item}")
                st.download_button(label="📥 Baixar Relatório Financeiro (.txt)", data=relatorio_lucro, file_name=f"lucro_{nome_item.lower().replace(' ', '_')}.txt", mime="text/plain", key="dl_lucro")
            else:
                st.warning("⚠️ Digite o nome do item.")
