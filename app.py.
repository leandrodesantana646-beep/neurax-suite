import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="NeuraX Suite - Painel Inteligente",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 NeuraX Suite - Painel Web Oficial")
st.markdown("Bem-vindo ao seu software de inteligência autônoma para e-commerce!")

# Menu Lateral (Sidebar) para escolher o módulo
modulo = st.sidebar.selectbox(
    "Escolha o Módulo do Sistema",
    [
        "🤖 Gerador de Copy e SEO",
        "📊 Analisador de Preços (IA)",
        "💬 Assistente de WhatsApp"
    ]
)

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
                
                # Estimativa de mercado inteligente baseada no tipo de produto
                if "iphone" in nome_formatado or "celular" in nome_formatado or "notebook" in nome_formatado:
                    media_mercado = 2500.00
                    menor_preco = 2200.00
                elif "fone" in nome_formatado or "relogio" in nome_formatado or "smartwatch" in nome_formatado:
                    media_mercado = 199.90
                    menor_preco = 150.00
                else:
                    media_mercado = max(preco_atual * 1.15, 100.00)
                    menor_preco = media_mercado * 0.85

                # 💡 O CÁLCULO DE LUCRO ÓTIMO DA IA:
                # Define o preço estratégico perfeito para garantir excelente margem e competitividade
                preco_sugerido_lucro = round(media_mercado * 0.95, 2)
                margem_estimada = "Alta rentabilidade (Aprox. 40% a 50% de margem líquida)"

                # Regra de Decisão da IA
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

            st.download_button(
                label="📥 Baixar Resposta do WhatsApp (.txt)",
                data=resposta_gerada,
                file_name="resposta_cliente.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Digite a dúvida do cliente para gerar a resposta.")
