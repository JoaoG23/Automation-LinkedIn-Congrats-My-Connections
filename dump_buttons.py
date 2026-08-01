import asyncio
import sys
from playwright.async_api import async_playwright
from config import config
from utils.do_login import do_login

async def dump():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        email = config.get("EMAIL")
        password = config.get("PASSWORD")
        
        print("Logging in...")
        await do_login(page, email, password)
        
        print("Go to catch-up...")
        await page.goto("https://www.linkedin.com/mynetwork/catch-up/all/", wait_until="domcontentloaded")
        await asyncio.sleep(5)
        
        print("Dumping button structures...")
        htmls = await page.evaluate('''() => {
            // Find the list of cards
            const cards = Array.from(document.querySelectorAll('li, div.discover-entity-type-card'));
            let results = [];
            for (let c of cards) {
                // look for the action button which might be a button or an anchor
                let btns = Array.from(c.querySelectorAll('button, a'));
                let actionBtn = btns.find(b => b.innerText.includes('Parabéns') || b.innerText.includes('Feliz') || b.getAttribute('aria-label'));
                if (actionBtn) {
                    results.push(actionBtn.outerHTML);
                }
                if (results.length >= 10) break;
            }
            return results;
        }''')
        
        for idx, h in enumerate(htmls):
            print(f"--- Button {idx} ---")
            print(h)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(dump())
