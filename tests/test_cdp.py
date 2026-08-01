import asyncio
import sys
import os
from playwright.async_api import async_playwright

# Garante que o diretório raiz do projeto esteja no sys.path
diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from send_congrats.send_congrats import enviar_mensagens_parabens_conexoes

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)


async def executar_teste_conexao_cdp() -> None:
    """Executa um teste de envio de parabéns conectando ao navegador via CDP com limite reduzido."""
    print("=================== TESTE CDP - LINKEDIN CONGRATS ===================", flush=True)

    endereco_conexao_cdp = "http://localhost:9222"

    async with async_playwright() as instancia_playwright:
        try:
            print(
                f"[CDP] Conectando ao navegador existente em {endereco_conexao_cdp}...",
                flush=True,
            )
            instancia_navegador = await instancia_playwright.chromium.connect_over_cdp(
                endereco_conexao_cdp
            )
            contexto_navegador = instancia_navegador.contexts[0]

            pagina_ativa_linkedin = None
            for aba_navegador in contexto_navegador.pages:
                if "linkedin.com" in aba_navegador.url:
                    pagina_ativa_linkedin = aba_navegador
                    break

            if not pagina_ativa_linkedin:
                print(
                    "[CDP] Aba do LinkedIn não encontrada. Criando nova aba...",
                    flush=True,
                )
                pagina_ativa_linkedin = await contexto_navegador.new_page()

            await pagina_ativa_linkedin.bring_to_front()

            print("[CDP] Iniciando teste com limite de 2 mensagens...", flush=True)
            await enviar_mensagens_parabens_conexoes(
                pagina_ativa_linkedin, limite_maximo_mensagens=2
            )

            print("[CDP] Teste finalizado com sucesso.", flush=True)

        except Exception as excecao_erro:
            print(f"[CDP] Erro durante o teste: {excecao_erro}", flush=True)


if __name__ == "__main__":
    asyncio.run(executar_teste_conexao_cdp())
