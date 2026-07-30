import asyncio
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def test_find():
    cdp_url = "http://localhost:9222"
    async with async_playwright() as p:
        print(f"Conectando a {cdp_url}...")
        try:
            browser = await p.chromium.connect_over_cdp(cdp_url)
            context = browser.contexts[0]
            
            page = None
            for p_tab in context.pages:
                if "linkedin.com" in p_tab.url:
                    page = p_tab
                    break
                    
            if not page:
                print("Aba do LinkedIn não encontrada.")
                return
                
            await page.bring_to_front()
            
            selector = (
                'button:has([id*="send-privately"]), '
                'a:has([id*="send-privately"]), '
                'button:has-text("Parabéns"), '
                'button:has-text("Feliz"), '
                'button:has-text("Comemore"), '
                'button[aria-label*="mensagem" i], '
                'a[aria-label*="mensagem" i]'
            )
            
            print(f"Avaliando seletor: {selector}")
            current_buttons = await page.query_selector_all(selector)
            print(f"Total encontrados: {len(current_buttons)}")
            
            for i, btn in enumerate(current_buttons):
                inner = await btn.inner_text()
                aria = await btn.get_attribute('aria-label')
                print(f"Botão {i}: inner_text='{inner.strip() if inner else ''}', aria-label='{aria}'")
                
            print("Tentando scrollar usando scroll_into_view e window.scrollBy...")
            await page.evaluate("window.scrollBy(0, 1000)")
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    asyncio.run(test_find())
