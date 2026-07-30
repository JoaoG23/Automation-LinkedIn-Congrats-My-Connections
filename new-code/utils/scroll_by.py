import asyncio
from playwright.async_api import Page

async def scroll_page(page: Page, scroll_times: int = 1, delay_seconds: float = 2.0) -> None:
    """Rola a página para carregar novos elementos dinâmicos."""
    print(f"[Scroll] Rolando a página {scroll_times} vezes...")
    for _ in range(scroll_times):
        await page.keyboard.press("PageDown")
    await asyncio.sleep(delay_seconds)
