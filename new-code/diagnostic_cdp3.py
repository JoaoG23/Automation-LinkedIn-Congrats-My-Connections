import asyncio
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def test_body():
    cdp_url = "http://localhost:9222"
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(cdp_url)
            context = browser.contexts[0]
            
            page = None
            for p_tab in context.pages:
                if "linkedin.com" in p_tab.url:
                    page = p_tab
                    break
                    
            if not page:
                return
            await page.bring_to_front()
            
            print("Verificando innerText do body...")
            
            htmls = await page.evaluate('''() => {
                return document.body.innerText.substring(0, 3000);
            }''')
            
            print(htmls)
                
        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(test_body())
