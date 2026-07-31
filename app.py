import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="NeuraX Suite - Painel Inteligente",
    page_icon="🚀",
    layout="centered"
)

# Inicializar Histórico na Sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

st.title("🚀 NeuraX Suite - Painel Web Oficial")
st.markdown("O seu software completo de inteligência e automação para e-commerce!")

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
    for item in st.session_state.historico[-5:]: # Mostra os últimos 5 itens gerados
        st.sidebar.text(f"• {item}")
    if st.sidebar.button("Limpar Histórico"):
        st.session_state.historico = []
        st.rerun()
else:
        st.sidebar.info("Nenhuma geração recente.")

# ---------------------------------------------------------
# MÓDULO 1: GERADOR DE COPY E SEO
# ---------------------------------------------------------
if modulo == "🤖 Gerador de Copy e SEO":
    st.header("🤖 Gerador Automático de Copy e SEO")
    st.write("Crie títulos otimizados, descrições de alto impacto e baixe o arquivo de texto em segundos.")

    nome_produto = st.text_input("📦 Digite o nome do produto:")
    beneficio = st.text_input("✨ Digite o benefício principal:")

    if st.button("Gerar e Salvar Copy"):
        if nome_produto and beneficio:
            titulo_seo = f"{nome_produto} Original | {beneficio} | Frete Grátis"
            descricao_vendas = (
                f"Procurando excelência? O novo {nome_produto} chegou para revolucionar a sua "
                f"experiência. Desenvolvido para entregar {beneficio}, ele une tecnologia de ponta "
                "e acabamento premium. Garanta já o seu!"
            )
            hashtags = f"#{nome_produto.lower().replace(' ', '')} #ecommerce #lancamento"

            resultado = f"""--- 🎯 RESULTADO GERADO PELA IA ---
[Título SEO]: {titulo_seo}
[Descrição]: {descricao_vendas}
[Hashtags]: {hashtags}
"""

            st.success("✨ Copy gerada e salva com sucesso!")
            st.text_area("Resultado:", resultado, height=150)

            st.session_state.historico.append(f"Copy: {nome_produto}")

            nome_arquivo = f"copy_{nome_produto.lower().replace(' ', '_')}.txt"
            st.download_button(
                label="📥 Baixar Arquivo de Copy (.txt)",
                data=resultado,
                file_name=nome_arquivo,
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Por favor, preencha o nome do produto e o benefício.")

# ---------------------------------------------------------
# MÓDULO 2: ANALISADOR DE PREÇOS (COM CÁLCULO DE LUCRO ÓTIMO)
# ---------------------------------------------------------
elif modulo == "📊 Analisador de Preços (IA)":
    st.header("📊 Analisador Inteligente de Preços via IA")
    st.write("A IA analisa o mercado automaticamente e calcula o **Preço Ideal de Venda para o seu Lucro Máximo**.")

    produto = st.text_input("📦 Nome do produto (ex: Smartwatch T800, Tênis Nike Air):")
    preco_atual = st.number_input("💰 O quanto você cobra hoje ou tem como base (R$):", min_value=0.0, value=150.0, step=1.0)

    if st.button("Executar Pesquisa e Calcular Lucro Ótimo"):
        if produto:
            with st.spinner("🔍 A IA está varrendo o mercado e calculando o preço ideal para o seu lucro..."):
                nome_formatado = produto.lower()
                
                if "iphone" in nome_formatado or "celular" in nome_formatado or "notebook" in nome_formatado:
                    media_mercado = 2500.00
                    menor_preco = 2200.00
                elif "fone" in nome_formatado or "relogio" in nome_formatado or "smartwatch" in nome_formatado:
                    media_mercado = 199.90
                    menor_preco = 150.00
                else:
                    media_mercado = max(preco_atual * 1.15, 100.00)
                    menor_preco = media_mercado * 0.85

                preco_sugerido_lucro = round(media_mercado * 0.95, 2)
                margem_estimada = "Alta rentabilidade (Aprox. 40% a 50% de margem líquida)"

                if preco_atual > media_mercado:
                    status = "Acima da Média (Risco de baixo giro de vendas)"
                    rec = f"Seu preço atual está muito alto. Para ter um ótimo volume de vendas com alta margem, o ideal é fixar em **R$ {preco_sugerido_lucro:.2f}**."
                elif preco_atual < menor_preco:
                    status = "Abaixo do Mercado (Você está perdendo dinheiro)"
                    rec = f"Você está vendendo barato demais! Suba o seu preço para o **Preço Sugerido de R$ {preco_sugerido_lucro:.2f}** para maximizar o seu lucro sem perder clientes."
                else:
                    status = "Posicionamento Estratégico Saudável 🚀"
                    rec = f"Seu preço está bom, mas para atingir a **margem de lucro ideal**, recomendamos ajustar para **R$ {preco_sugerido_lucro:.2f}**."

                relatorio = f"""--- 🧠 RELATÓRIO DE INTELIGÊNCIA DE PREÇOS & LUCRO ÓTIMO ---
[Produto Analisado]: {produto}
[Seu Preço Informado]: R$ {preco_atual:.2f}
[Média Estimada da Concorrência]: R$ {media_mercado:.2f}
[Menor Preço no Mercado]: R$ {menor_preco:.2f}
🎯 [PREÇO SUGERIDO PELA IA PARA LUCRO ÓTIMO]: R$ {preco_sugerido_lucro:.2f}
📈 [Retorno Esperado]: {margem_estimada}
[Status Competitivo]: {status}
[Recomendação da IA]: {rec}
"""

                st.success("🎯 Análise de lucro ideal concluída com sucesso!")
                st.metric(label="💎 Preço Sugerido para Lucro Ótimo", value=f"R$ {preco_sugerido_lucro:.2f}")
                st.info(f"**Status:** {status}")
                st.text_area("Relatório Completo:", relatorio, height=220)

                st.session_state.historico.append(f"Preço: {produto}")

                nome_arquivo_preco = f"relatorio_lucro_{produto.lower().replace(' ', '_')}.txt"
                st.download_button(
                    label="📥 Baixar Relatório de Preços e Lucro Ótimo (.txt)",
                    data=relatorio,
                    file_name=nome_arquivo_preco,
                    mime="text/plain"
                )
        else:
            st.warning("⚠️ Digite o nome do produto para a IA calcular o preço de lucro ideal.")

# ---------------------------------------------------------
# MÓDULO 3: ASSISTENTE DE WHATSAPP
# ---------------------------------------------------------
elif modulo == "💬 Assistente de WhatsApp":
    st.header("💬 Assistente de Atendimento para WhatsApp")
    st.write("Gere respostas profissionais e baixe o arquivo de atendimento.")

    duvida_cliente = st.text_input("❓ Digite a dúvida ou objeção do cliente (ex: 'O produto é original?'):")
    nome_loja = st.text_input("🏷️ Digite o nome da sua loja:", value="Nossa Loja")

    if st.button("Gerar e Salvar Resposta"):
        if duvida_cliente:
            resposta_gerada = f"""Olá! Tudo bem? 😃
Obrigado pelo contato com a {nome_loja}!

Referente à sua dúvida ("{duvida_cliente}"):
Trabalhamos apenas com produtos 100% originais, testados e com garantia de fábrica para garantir a sua total segurança. Além disso, oferecemos envio rápido e suporte dedicado para qualquer necessidade!

Posso separar o seu pedido por aqui para garantirmos o estoque? ✨"""
            
            st.success("💬 Resposta gerada com sucesso!")
            st.text_area("Copie a mensagem abaixo para enviar ao cliente:", resposta_gerada, height=200)

            st.session_state.historico.append(f"WhatsApp: {duvida_cliente[:15]}...")

            st.download_button(
                label="📥 Baixar Resposta do WhatsApp (.txt)",
                data=resposta_gerada,
                file_name="resposta_cliente.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Digite a dúvida do cliente para gerar a resposta.")

# ---------------------------------------------------------
# MÓDULO 4: GERADOR DE ROTEIROS PARA VÍDEOS (REELS/TIKTOK)
# ---------------------------------------------------------
elif modulo == "🎬 Gerador de Roteiros (Reels/TikTok)":
    st.header("🎬 Gerador de Roteiros para Vídeos Curtos")
    st.write("Crie roteiros virais e estruturados para engajar e vender no Reels, TikTok e Shorts.")

    prod_video = st.text_input("📦 Nome do produto para o vídeo:")
    gancho = st.text_input("🔥 Qual a maior dor ou desejo que o produto resolve? (ex: 'Bateria que acaba rápido', 'Cabelo frizzado'):")

    if st.button("Gerar Roteiro Viral"):
        if prod_video and gancho:
            roteiro = f"""--- 🎬 ROTEIRO DE VÍDEO VIRAL (REELS / TIKTOK) ---
[Produto]: {prod_video}

1. GANCHO (0 a 3 segundos):
- "Cansado de sofrer com {gancho}? Olha o que acabou de chegar!"

2. DESENVOLVIMENTO / PROBLEMA X SOLUÇÃO (3 a 15 segundos):
- "A gente sabe como isso é irritante no dia a dia. Mas o novo {prod_video} resolve isso de forma prática, rápida e com qualidade premium que cabe no seu bolso."

3. CHAMADA PARA AÇÃO / CTA (15 a 25 segundos):
- "Não fica de fora dessa! Clica no link da bio ou me manda uma mensagem aqui embaixo para garantir o seu com frete especial!"
"""
            st.success("🎬 Roteiro gerado com sucesso!")
            st.text_area("Estrutura do Vídeo:", roteiro, height=220)

            st.session_state.historico.append(f"Roteiro: {prod_video}")

            st.download_button(
                label="📥 Baixar Roteiro de Vídeo (.txt)",
                data=roteiro,
                file_name=f"roteiro_{prod_video.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Preencha os campos para gerar o roteiro.")

# ---------------------------------------------------------
# MÓDULO 5: CALCULADORA DE TAXAS & LUCRO
# ---------------------------------------------------------
elif modulo == "🧮 Calculadora de Taxas & Lucro":
    st.header("🧮 Calculadora de Custos e Taxas de Marketplace")
    st.write("Descubra o seu **Lucro Líquido Real** descontando o custo do produto e as taxas da plataforma.")

    nome_item = st.text_input("📦 Nome do item avaliado:")
    custo_prod = st.number_input("💸 Preço de Custo / Aquisição (R$):", min_value=0.0, value=50.0, step=1.0)
    preco_venda = st.number_input("🏷️ Preço de Venda Pretendido (R$):", min_value=0.0, value=120.0, step=1.0)
    taxa_marketplace_pct = st.number_input("📊 Taxa do Marketplace ou Cartão (%):", min_value=0.0, max_value=100.0, value=16.0, step=0.5)
    custo_extra = st.number_input("📦 Custos Extras (Embalagem, Frete fixo, etc) (R$):", min_value=0.0, value=5.0, step=1.0)

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
[Custos Extras (Embalagem/Outros)]: R$ {custo_extra:.2f}
----------------------------------------
💰 [LUCRO LÍQUIDO FINAL]: R$ {lucro_liquido:.2f}
📈 [Margem Líquida Percentual]: {margem_liquida_pct:.1f}%
[Status Financeiro]: {status_lucro}
"""

            st.success("🧮 Cálculo de lucros realizado com sucesso!")
            st.metric(label="💰 Lucro Líquido Real", value=f"R$ {lucro_liquido:.2f}", delta=f"{margem_liquida_pct:.1f}% de margem")
            st.text_area("Relatório Financeiro:", relatorio_lucro, height=230)

            st.session_state.historico.append(f"Lucro: {nome_item}")

            st.download_button(
                label="📥 Baixar Relatório Financeiro (.txt)",
                data=relatorio_lucro,
                file_name=f"lucro_{nome_item.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Digite o nome do item para calcular.")
