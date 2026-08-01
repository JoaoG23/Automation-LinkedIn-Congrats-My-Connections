import asyncio
from playwright.async_api import Page


async def rolar_pagina_para_carregar_conteudo(
    pagina: Page, quantidade_rolagens: int = 3, tempo_espera_segundos: float = 2.5
) -> None:
    """Rola a página e containers roláveis internos para disparar o carregamento dinâmico de novas conexões.

    Args:
        pagina (Page): Instância da página do Playwright.
        quantidade_rolagens (int): Número de vezes que a rolagem será repetida.
        tempo_espera_segundos (float): Tempo de espera em segundos ao final da rolagem.
    """
    print("[Scroll] Rolando a página para carregar mais itens...", flush=True)

    tamanho_viewport = pagina.viewport_size or {"width": 1280, "height": 800}
    posicao_centro_horizontal = tamanho_viewport["width"] // 2
    posicao_centro_vertical = tamanho_viewport["height"] // 2
    await pagina.mouse.move(posicao_centro_horizontal, posicao_centro_vertical)

    for _ in range(quantidade_rolagens):
        # 1. Simula a roldana física do mouse (wheel)
        await pagina.mouse.wheel(0, 1200)
        await asyncio.sleep(0.5)

        # 2. Localiza o último elemento card na página e força scrollIntoView
        try:
            lista_elementos_cards = await pagina.query_selector_all(
                "main li, main div.discover-entity-type-card, main section, .scaffold-layout__main li"
            )
            if lista_elementos_cards:
                await lista_elementos_cards[-1].scroll_into_view_if_needed(timeout=2000)
        except Exception:
            pass

        # 3. Rola containers internos que possuem scrollbar via JavaScript
        await pagina.evaluate(
            """() => {
            window.scrollBy(0, 1000);
            window.scrollTo(0, document.body.scrollHeight);
            if (document.scrollingElement) {
                document.scrollingElement.scrollTop = document.scrollingElement.scrollHeight;
            }
            
            const lista_elementos_rolaveis = Array.from(document.querySelectorAll('*')).filter(elemento => {
                const estilo_computado = window.getComputedStyle(elemento);
                return (estilo_computado.overflowY === 'auto' || estilo_computado.overflowY === 'scroll') 
                        && elemento.scrollHeight > elemento.clientHeight;
            });
            lista_elementos_rolaveis.forEach(elemento => {
                elemento.scrollTop += 1000;
            });
        }"""
        )

        await pagina.keyboard.press("PageDown")
        await asyncio.sleep(0.8)

    await asyncio.sleep(tempo_espera_segundos)


async def scroll_page(
    pagina: Page,
    scroll_times: int = 3,
    delay_seconds: float = 2.5,
    quantidade_rolagens: int = None,
    tempo_espera_segundos: float = None,
) -> None:
    """Wrapper de compatibilidade para rolar_pagina_para_carregar_conteudo."""
    rolagens = quantidade_rolagens if quantidade_rolagens is not None else scroll_times
    tempo = tempo_espera_segundos if tempo_espera_segundos is not None else delay_seconds
    await rolar_pagina_para_carregar_conteudo(
        pagina, quantidade_rolagens=rolagens, tempo_espera_segundos=tempo
    )

