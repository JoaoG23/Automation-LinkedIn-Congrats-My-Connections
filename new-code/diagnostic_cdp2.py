import asyncio
import sys
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def test_find_all():
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
            
            print("Buscando por elementos com texto 'Parabéns' ou 'Feliz' ou 'Mensagem'...")
            
            # Encontra QUALQUER elemento que contenha a string. Como text() retorna todos os ancestrais,
            # vamos usar evaluate para pegar os elementos mais profundos que contenham o texto.
            htmls = await page.evaluate('''() => {
                let results = [];
                let cards = document.querySelectorAll('li');
                for (let c of cards) {
                    if (c.innerText.includes('Parabéns') || c.innerText.includes('Feliz')) {
                        // Get the button-like element inside it
                        let buttons = c.querySelectorAll('button, a, [role="button"]');
                        for (let b of buttons) {
                            if (b.innerText.includes('Parabéns') || b.innerText.includes('Feliz') || b.innerText.includes('Mensagem')) {
                                results.push({
                                    tag: b.tagName,
                                    text: b.innerText.trim(),
                                    classes: b.className,
                                    html: b.outerHTML
                                });
                                break; // get first matching button in card
                            }
                        }
                    }
                }
                return results;
            }''')
            
            print(f"Encontrados {len(htmls)} cards com botões:")
            for item in htmls:
                print(f"Tag: {item['tag']} | Classes: {item['classes']}")
                print(f"Texto: {item['text']}")
                print("-" * 20)
                
        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(test_find_all())
