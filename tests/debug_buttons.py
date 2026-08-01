import asyncio
import sys
import os
from playwright.async_api import async_playwright

# Garante que o diretório raiz do projeto esteja no sys.path
diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)


async def depurar_estrutura_botoes_cdp() -> None:
    """Conecta ao navegador via CDP para inspecionar a hierarquia DOM dos botões send-privately."""
    endereco_conexao_cdp = "http://localhost:9222"

    async with async_playwright() as instancia_playwright:
        instancia_navegador = await instancia_playwright.chromium.connect_over_cdp(
            endereco_conexao_cdp
        )
        contexto_navegador = instancia_navegador.contexts[0]

        pagina_ativa_linkedin = None
        for aba_navegador in contexto_navegador.pages:
            if "linkedin.com" in aba_navegador.url:
                pagina_ativa_linkedin = aba_navegador
                break

        if pagina_ativa_linkedin:
            lista_elementos_inspecionados = await pagina_ativa_linkedin.evaluate(
                """() => {
                const elementos_no = Array.from(document.querySelectorAll('[id*="send-privately"]'));
                return elementos_no.map(no => {
                    let elemento_pai = no.parentElement;
                    let elemento_avo = elemento_pai ? elemento_pai.parentElement : null;
                    return {
                        tag_no: no.tagName,
                        id_no: no.id,
                        tag_pai: elemento_pai ? elemento_pai.tagName : '',
                        role_pai: elemento_pai ? elemento_pai.getAttribute('role') : '',
                        texto_pai: elemento_pai ? elemento_pai.innerText.trim() : '',
                        tag_avo: elemento_avo ? elemento_avo.tagName : '',
                        role_avo: elemento_avo ? elemento_avo.getAttribute('role') : '',
                        rotulo_aria_avo: elemento_avo ? elemento_avo.getAttribute('aria-label') : '',
                    };
                });
            }"""
            )

            print(
                f"Total de elementos send-privately encontrados: {len(lista_elementos_inspecionados)}",
                flush=True,
            )
            for indice_posicao, dicionario_elemento in enumerate(
                lista_elementos_inspecionados
            ):
                tag_no = dicionario_elemento["tag_no"]
                id_no = dicionario_elemento["id_no"]
                tag_pai = dicionario_elemento["tag_pai"]
                role_pai = dicionario_elemento["role_pai"]
                texto_pai = dicionario_elemento["texto_pai"]
                tag_avo = dicionario_elemento["tag_avo"]
                role_avo = dicionario_elemento["role_avo"]
                rotulo_aria_avo = dicionario_elemento["rotulo_aria_avo"]

                print(
                    f"[{indice_posicao}] {tag_no}#{id_no} | Pai: {tag_pai} (role={role_pai}, text='{texto_pai}') | Avô: {tag_avo} (role={role_avo}, aria='{rotulo_aria_avo}')",
                    flush=True,
                )


if __name__ == "__main__":
    asyncio.run(depurar_estrutura_botoes_cdp())
