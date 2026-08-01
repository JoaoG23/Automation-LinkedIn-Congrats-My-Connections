import asyncio
import sys
import os
from playwright.async_api import async_playwright

# Garante que o diretório raiz do projeto esteja no sys.path
diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from config import config
from utils.do_login import realizar_login_linkedin


async def extrair_estrutura_html_botoes() -> None:
    """Abre um navegador headless, faz login e extrai o HTML dos primeiros botões de ação do Catch-Up."""
    async with async_playwright() as instancia_playwright:
        instancia_navegador = await instancia_playwright.chromium.launch(headless=True)
        contexto_navegador = await instancia_navegador.new_context()
        pagina_ativa = await contexto_navegador.new_page()

        email_usuario = config.get("EMAIL")
        senha_usuario = config.get("PASSWORD")

        print("[Dump] Realizando login...", flush=True)
        await realizar_login_linkedin(pagina_ativa, email_usuario, senha_usuario)

        print("[Dump] Navegando para a página de Catch-Up...", flush=True)
        await pagina_ativa.goto(
            "https://www.linkedin.com/mynetwork/catch-up/all/",
            wait_until="domcontentloaded",
        )
        await asyncio.sleep(5)

        print("[Dump] Extraindo estrutura dos botões de ação...", flush=True)
        lista_html_botoes = await pagina_ativa.evaluate(
            """() => {
            const lista_cards = Array.from(document.querySelectorAll('li, div.discover-entity-type-card'));
            let resultados_html = [];
            for (let card_elemento of lista_cards) {
                let lista_botoes = Array.from(card_elemento.querySelectorAll('button, a'));
                let botao_acao = lista_botoes.find(botao => 
                    botao.innerText.includes('Parabéns') || 
                    botao.innerText.includes('Feliz') || 
                    botao.getAttribute('aria-label')
                );
                if (botao_acao) {
                    resultados_html.push(botao_acao.outerHTML);
                }
                if (resultados_html.length >= 10) break;
            }
            return resultados_html;
        }"""
        )

        for indice_posicao, codigo_html_botao in enumerate(lista_html_botoes):
            print(f"--- Botão [{indice_posicao}] ---", flush=True)
            print(codigo_html_botao, flush=True)

        await instancia_navegador.close()


if __name__ == "__main__":
    asyncio.run(extrair_estrutura_html_botoes())
