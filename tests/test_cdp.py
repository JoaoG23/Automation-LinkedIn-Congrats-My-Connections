import asyncio
import sys
from playwright.async_api import async_playwright
from send_congrats.send_congrats import send_congrats_to_connections

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def main():
    print("=================== TESTE CDP - LINKEDIN CONGRATS ===================")
    
    cdp_url = "http://localhost:9222"
    
    async with async_playwright() as p:
        try:
            print(f"[CDP] Conectando ao navegador existente em {cdp_url}...")
            browser = await p.chromium.connect_over_cdp(cdp_url)
            context = browser.contexts[0]
            
            # Encontrar a aba do Linkedin
            active_page = None
            for page in context.pages:
                if "linkedin.com" in page.url:
                    active_page = page
                    break
                    
            if not active_page:
                print("[CDP] Aba do LinkedIn não encontrada. Criando nova aba...")
                active_page = await context.new_page()
                
            await active_page.bring_to_front()
            
            # Testa com limite de 2 mensagens para não fazer spam no teste
            print("[CDP] Iniciando teste de envio...")
            await send_congrats_to_connections(active_page, limit=2)
            
            print("[CDP] Teste finalizado.")
            # Não chamamos browser.close() para não fechar o navegador do usuário
            
        except Exception as e:
            print(f"[CDP] Erro ao conectar ou executar: {e}")

if __name__ == "__main__":
    asyncio.run(main())
