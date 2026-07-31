import streamlit as st
import os

# Configuração da Página
st.set_page_config(
    page_title="NeuraX Suite - Painel Inteligente",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 NeuraX Suite - Painel Web Oficial")
st.markdown("Bem-vindo ao seu software de inteligência para e-commerce com salvamento integrado!")

# Menu Lateral (Sidebar) para escolher o módulo
modulo = st.sidebar.selectbox(
    "Escolha o Módulo do Sistema",
    [
        "🤖 Gerador de Copy e SEO",
        "📊 Analisador de Preços",
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

            # Botão de Download do Arquivo
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
# MÓDULO 2: ANALISADOR DE PREÇOS
# ---------------------------------------------------------
elif modulo == "📊 Analisador de Preços":
    st.header("📊 Analisador Inteligente de Preços")
    st.write("Descubra o posicionamento competitivo e baixe o relatório completo.")

    produto = st.text_input("📦 Nome do produto:")
    preco_atual = st.number_input("💰 Preço atual do seu produto (R$):", min_value=0.0, value=100.0, step=1.0)
    precos_input = st.text_input("📊 Preços da concorrência (separados por vírgula, ex: 199.90, 210, 195):")

    if st.button("Analisar e Salvar Relatório"):
        if produto and precos_input:
            try:
                precos_concorrentes = [float(p.strip()) for p in precos_input.split(",")]
                if precos_concorrentes:
                    menor_preco = min(precos_concorrentes)
                    media_mercado = sum(precos_concorrentes) / len(precos_concorrentes)

                    if preco_atual > media_mercado:
                        status = "Acima da Média de Mercado"
                        rec = f"Sugerimos ajustar o preço para próximo de R$ {media_mercado:.2f} ou reforçar diferenciais exclusivos."
                    elif preco_atual < menor_preco:
                        status = "Abaixo do Menor Concorrente"
                        rec = f"Você pode reajustar com segurança para R$ {menor_preco:.2f} e aumentar sua margem de lucro."
                    else:
                        status = "Posicionamento Estratégico Saudável"
                        rec = "Seu preço está perfeitamente alinhado com o mercado atual."

                    relatorio = f"""--- 🧠 RELATÓRIO DE PRECificação ---
[Produto]: {produto}
[Status Competitivo]: {status}
[Preço Atual]: R$ {preco_atual:.2f}
[Média de Mercado]: R$ {media_mercado:.2f}
[Recomendação da IA]: {rec}
"""

                    st.success("📊 Relatório gerado com sucesso!")
                    st.text_area("Relatório:", relatorio, height=180)

                    # Botão de Download do Relatório
                    nome_arquivo_preco = f"preco_{produto.lower().replace(' ', '_')}.txt"
                    st.download_button(
                        label="📥 Baixar Relatório de Preços (.txt)",
                        data=relatorio,
                        file_name=nome_arquivo_preco,
                        mime="text/plain"
                    )
                else:
                    st.warning("⚠️ Informe pelo menos um preço de concorrente.")
            except ValueError:
                st.error("⚠️ Formato inválido nos preços dos concorrentes. Use apenas números separados por vírgula.")
        else:
            st.warning("⚠️ Preencha todos os campos para realizar a análise.")

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

            # Botão de Download da Resposta
            st.download_button(
                label="📥 Baixar Resposta do WhatsApp (.txt)",
                data=resposta_gerada,
                file_name="resposta_cliente.txt",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Digite a dúvida do cliente para gerar a resposta.")
