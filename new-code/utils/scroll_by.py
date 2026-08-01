import asyncio
from playwright.async_api import Page


async def scroll_page(
    page: Page, scroll_times: int = 3, delay_seconds: float = 2.5
) -> None:
    """Rola a página e containers roláveis para garantir o carregamento de novas conexões."""
    print(f"[Scroll] Rolando a página para carregar mais itens...", flush=True)
    
    # Posiciona o mouse no centro da página para garantir que o evento de roda de mouse atinja o container correto
    viewport = page.viewport_size or {'width': 1280, 'height': 800}
    center_x = viewport['width'] // 2
    center_y = viewport['height'] // 2
    await page.mouse.move(center_x, center_y)

    for _ in range(scroll_times):
        # 1. Simula a roldana do mouse (wheel) que ativa o Infinite Scroll do LinkedIn
        await page.mouse.wheel(0, 1200)
        await asyncio.sleep(0.5)

        # 2. Encontra o último card/item na página e rola até ele
        try:
            items = await page.query_selector_all(
                "main li, main div.discover-entity-type-card, main section, .scaffold-layout__main li"
            )
            if items:
                await items[-1].scroll_into_view_if_needed(timeout=2000)
        except Exception:
            pass

        # 3. Rola containers com overflow:auto/scroll + janela via JS
        await page.evaluate("""() => {
            window.scrollBy(0, 1000);
            window.scrollTo(0, document.body.scrollHeight);
            if (document.scrollingElement) {
                document.scrollingElement.scrollTop = document.scrollingElement.scrollHeight;
            }
            
            const scrollables = Array.from(document.querySelectorAll('*')).filter(el => {
                const style = window.getComputedStyle(el);
                return (style.overflowY === 'auto' || style.overflowY === 'scroll') && el.scrollHeight > el.clientHeight;
            });
            scrollables.forEach(el => {
                el.scrollTop += 1000;
            });
        }""")

        await page.keyboard.press("PageDown")
        await asyncio.sleep(0.8)

    await asyncio.sleep(delay_seconds)


