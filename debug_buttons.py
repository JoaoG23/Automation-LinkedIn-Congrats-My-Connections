import asyncio
from playwright.async_api import async_playwright

async def main():
    cdp_url = "http://localhost:9222"
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0]
        
        active_page = None
        for page in context.pages:
            if "linkedin.com" in page.url:
                active_page = page
                break
                
        if active_page:
            elements = await active_page.evaluate('''() => {
                const nodes = Array.from(document.querySelectorAll('[id*="send-privately"]'));
                return nodes.map(n => {
                    let parent = n.parentElement;
                    let grandpa = parent ? parent.parentElement : null;
                    return {
                        node_tag: n.tagName,
                        node_id: n.id,
                        parent_tag: parent ? parent.tagName : '',
                        parent_role: parent ? parent.getAttribute('role') : '',
                        parent_text: parent ? parent.innerText.trim() : '',
                        grandpa_tag: grandpa ? grandpa.tagName : '',
                        grandpa_role: grandpa ? grandpa.getAttribute('role') : '',
                        grandpa_aria: grandpa ? grandpa.getAttribute('aria-label') : '',
                    };
                });
            }''')
            
            print(f"Total de elementos send-privately: {len(elements)}")
            for i, el in enumerate(elements):
                print(f"[{i}] {el['node_tag']}#{el['node_id']} | Pai: {el['parent_tag']} (role={el['parent_role']}, text='{el['parent_text']}') | Avô: {el['grandpa_tag']} (role={el['grandpa_role']}, aria='{el['grandpa_aria']}')")

if __name__ == "__main__":
    asyncio.run(main())
