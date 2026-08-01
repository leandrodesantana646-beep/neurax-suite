import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="NeuraX Suite - Painel Inteligente",
    page_icon="🚀",
    layout="centered"
)

# Customização Visual de Elite via CSS

import streamlit as st

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
st.markdown("O ecossistema definitivo de automação para e-commerce.")

# Menu Lateral (Sidebar) para escolher o módulo
modulo = st.sidebar.selectbox(
    "Escolha o Módulo do Sistema",
    [
        "⚡ Campanha Flash Sale Instantânea",
        "🤖 Gerador de Copy e SEO",
        "📊 Analisador de Preços",
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

# ---------------------------------------------------------
# MÓDULO 0: CAMPANHA FLASH SALE INSTANTÂNEA
# ---------------------------------------------------------
if modulo == "⚡ Campanha Flash Sale Instantânea":
    st.header("⚡ Campanha Flash Sale Instantânea")
    st.write("Crie uma estratégia relâmpago completa (WhatsApp + Instagram + E-mail) para gerar caixa rápido.")

    prod_flash = st.text_input("📦 Nome do produto em promoção:")
    preco_original = st.number_input("💰 Preço original (R$):", min_value=0.0, value=200.0, step=1.0)
    preco_flash = st.number_input("🔥 Preço promocional relâmpago (R$):", min_value=0.0, value=149.0, step=1.0)
    tempo_limite = st.selectbox("⏳ Duração da Oferta", ["Apenas hoje (24 horas)", "48 horas", "Enquanto durar o estoque (Poucas unidades)"])

    if st.button("Gerar Campanha Multicanal"):
        if prod_flash:
            economia = preco_original - preco_flash
            desconto_calc = int((economia / preco_original) * 100) if preco_original > 0 else 0

            kit_campanha = f"""========================================
⚡ KIT DE CAMPANHA FLASH SALE - {prod_flash.upper()}
========================================

1. 📱 MENSAGEM PARA GRUPO / VIP DO WHATSAPP:
----------------------------------------
🚨 ALERTA DE OFERTA RELÂMPAGO! 🚨

Galera, conseguimos liberar uma condição absurda para o {prod_flash} por tempo limitado ({tempo_limite})!

De: R$ {preco_original:.2f}
Por apenas: R$ {preco_flash:.2f} 😱 ({desconto_calc}% de desconto)

⚠️ ATENÇÃO: Estoque extremamente limitado e o preço volta ao normal daqui a pouco. 

Clica aqui para garantir o seu antes que acabe: [INSERIR_LINK_DE_PAGAMENTO] 🛒✨

---

2. 📸 SEQUÊNCIA DE STORIES (INSTAGRAM):
----------------------------------------
• Story 1 (Abertura/Alerta):
  - Fundo: Foto bonita do produto com efeito de alarme ou cor chamativa.
  - Texto na tela: "ALERTA DE QUEDA DE PREÇO! 🚨"
  - Fala: "Gente, muita gente pediu e conseguimos um lote promocional do {prod_flash} com desconto histórico!"

• Story 2 (A Oportunidade):
  - Fundo: Print do valor de R$ {preco_original} riscado indo para R$ {preco_flash}.
  - Texto na tela: "De R$ {preco_original:.2f} por R$ {preco_flash:.2f}!"
  - Fala: "Olha isso aqui. São {desconto_calc}% de economia real. Mas ó, é válido {tempo_limite.lower()}."

• Story 3 (Fechamento/CTA):
  - Fundo: Link direto para a compra com o botão "EU QUERO".
  - Texto na tela: "Últimas unidades! Corre no link."
  - Fala: "O link tá aqui embaixo nos Stories ou na bio. Acabou o lote, o preço sobe. Garante o seu!"

---

3. 📧 E-MAIL MARKETING / DISPARO RÁPIDO:
----------------------------------------
Assunto: ⏰ Corre! {prod_flash} com {desconto_calc}% de desconto ({tempo_limite})

Olá, tudo bem?

Se você estava esperando o momento certo para garantir o seu {prod_flash}, ele chegou.

A partir de agora e por {tempo_limite.lower()}, o {prod_flash} sai de R$ {preco_original:.2f} por apenas **R$ {preco_flash:.2f}**.

Criamos essa condição exclusiva para recompensar quem acompanha a nossa loja, mas as unidades são limitadas e o sistema vai encerrar a oferta automaticamente.

👉 [CLIQUE AQUI PARA GARANTIR SEU {prod_flash.upper()} COM DESCONTO]

Abraços e boas compras!
========================================"""

            st.success("🔥 Campanha relâmpago gerada com sucesso!")
            st.text_area("Pacote de Campanha Completo:", kit_campanha, height=300)

            st.session_state.historico.append(f"Flash Sale: {prod_flash}")

            st.download_button(
                label="📥 Baixar Campanha Completa (.txt)",
                data=kit_campanha,
                file_name=f"campanha_flash_{prod_flash.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Digite o nome do produto da promoção.")

# ---------------------------------------------------------
# MÓDULO 1: GERADOR DE COPY E SEO
# ---------------------------------------------------------
elif modulo == "🤖 Gerador de Copy e SEO":
    st.header("🤖 Gerador Automático de Copy e SEO")
    st.write("Crie títulos otimizados, descrições de alto impacto e baixe o arquivo em segundos.")

    nome_produto = st.text_input("📦 Digite o nome do produto:")
    publico = st.text_input("🎯 Para quem é esse produto? (ex: lojistas, jovens, mães):")

    if st.button("Gerar Copy"):
        if nome_produto and publico:
            resultado = f"""--- 🎯 RESULTADO GERADO PELO SISTEMA ---
[Título SEO]: {nome_produto} Original | Oferta Imperdível | Frete Grátis
[Descrição de Vendas]: Procurando excelência? O novo {nome_produto} foi desenvolvido especialmente para o público {publico}. Unindo tecnologia de ponta, durabilidade e design exclusivo, ele resolve suas necessidades do dia a dia com máxima eficiência. Garanta já o seu com condições especiais!
[Hashtags]: #{nome_produto.lower().replace(' ', '')} #ecommerce #lancamento #oferta"""
            
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
elif modulo == "📊 Analisador de Preços":
    st.header("📊 Analisador Inteligente de Preços")
    st.write("Analise o mercado e calcule o preço ideal de venda para maximizar seu lucro.")

    produto_preco = st.text_input("📦 Nome do produto:")
    preco_atual = st.number_input("💰 Preço que você cobra hoje (R$):", min_value=0.0, value=100.0, step=1.0)

    if st.button("Executar Análise de Preços"):
        if produto_preco:
            med = max(preco_atual * 1.15, 100.00)
            menor = med * 0.85
            sug = round(med * 0.95, 2)
            
            if preco_atual > med:
                status = "Acima da Média (Risco de baixo giro)"
                rec = f"Seu preço está alto. Sugerimos fixar em R$ {sug:.2f} para garantir vendas."
            elif preco_atual < menor:
                status = "Abaixo do Mercado (Margem baixa)"
                rec = f"Você está vendendo barato demais! Suba para R$ {sug:.2f} para lucrar mais."
            else:
                status = "Posicionamento Estratégico Saudável 🚀"
                rec = f"Preço competitivo. Para atingir a margem ideal, recomendamos ajustar para R$ {sug:.2f}."

            relatorio = f"""--- 🧠 RELATÓRIO DE INTELIGÊNCIA DE PREÇOS ---
[Produto Analisado]: {produto_preco}
[Seu Preço Informado]: R$ {preco_atual:.2f}
[Média Estimada da Concorrência]: R$ {med:.2f}
[Menor Preço no Mercado]: R$ {menor:.2f}
🎯 [PREÇO SUGERIDO PARA LUCRO ÓTIMO]: R$ {sug:.2f}
[Status Competitivo]: {status}
[Recomendação]: {rec}"""

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
            resposta_gerada = f"""Olá! Tudo bem? 😃
Obrigado pelo contato com a {nome_loja}!

Referente à sua dúvida ("{duvida_cliente}"):
Trabalhamos apenas com produtos 100% originais, testados e com garantia de fábrica para garantir a sua total segurança. Além disso, oferecemos envio rápido e suporte dedicado!

Posso separar o seu pedido por aqui para garantirmos o estoque? ✨"""

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
            roteiro = f"""--- 🎬 ROTEIRO DE VÍDEO VIRAL (REELS / TIKTOK) ---
[Produto]: {prod_video}

1. GANCHO (0 a 3 segundos):
- "Cansado de sofrer com {dor}? Olha o que acabou de chegar!"

2. DESENVOLVIMENTO / SOLUÇÃO (3 a 15 segundos):
- "A gente sabe como isso é chato no dia a dia. Mas o novo {prod_video} resolve isso de forma prática, rápida e com qualidade premium."

3. CHAMADA PARA AÇÃO / CTA (15 a 25 segundos):
- "Não fica de fora dessa! Clica no link da bio ou me manda uma mensagem aqui embaixo para garantir o seu!" """

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
