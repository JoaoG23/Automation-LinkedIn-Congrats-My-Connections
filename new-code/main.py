import asyncio
import sys
from playwright.async_api import async_playwright
from config import config
from utils.do_login import do_login
from send_congrats.send_congrats import send_congrats_to_connections

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)


async def main():
    print("=================== LINKEDIN CONGRATS BOT (PLAYWRIGHT) ===================")
    
    email = config.get("EMAIL")
    password = config.get("PASSWORD")
    
    if not email or not password:
        print("[Erro] Credenciais não encontradas. Verifique seu arquivo .env.")
        return

    cdp_url = "http://localhost:9222"
    
    async with async_playwright() as p:
        browser = None
        page = None
        is_cdp = False
        
        # 1. Tenta conectar via CDP (navegador já aberto)
        try:
            print(f"[Main] Tentando conectar ao navegador existente em {cdp_url}...")
            browser = await p.chromium.connect_over_cdp(cdp_url)
            context = browser.contexts[0]
            
            for p_tab in context.pages:
                if "linkedin.com" in p_tab.url:
                    page = p_tab
                    break
                    
            if not page:
                print("[Main] Aba do LinkedIn não encontrada no CDP. Criando nova aba...")
                page = await context.new_page()
            
            await page.bring_to_front()
            is_cdp = True
            print("[Main] Sucesso ao conectar no navegador já aberto (CDP).")
            
        except Exception as e:
            print(f"[Main] Não foi possível usar CDP ({e}).")
            
        # 2. Fallback para abrir um novo navegador (tradicional) se o CDP falhou
        if not is_cdp:
            print("[Main] Abrindo novo navegador tradicional...")
            browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
            context = await browser.new_context(viewport={'width': 1280, 'height': 800})
            page = await context.new_page()
            
            # Faz o Login
            await do_login(page, email, password)
            
        # 3. Envia as congratulações
        await send_congrats_to_connections(page)
        
        if not is_cdp:
            print("[Main] Fechando navegador...")
            await browser.close()
        else:
            print("[Main] Processo finalizado no navegador do usuário (CDP). O navegador foi mantido aberto.")

if __name__ == "__main__":
    asyncio.run(main())
