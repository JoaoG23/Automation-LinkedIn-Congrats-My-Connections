import asyncio
import sys
from playwright.async_api import async_playwright
from config import config
from utils.do_login import realizar_login_linkedin
from send_congrats.send_congrats import enviar_mensagens_parabens_conexoes

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)


async def iniciar_automacao_linkedin() -> None:
    """Função principal de orquestração do bot de felicitações no LinkedIn."""
    print("=================== LINKEDIN CONGRATS BOT (PLAYWRIGHT) ===================", flush=True)

    email_usuario = config.get("EMAIL")
    senha_usuario = config.get("PASSWORD")

    if not email_usuario or not senha_usuario:
        print("[Erro] Credenciais não encontradas. Verifique seu arquivo .env.", flush=True)
        return

    endereco_conexao_cdp = "http://localhost:9222"

    async with async_playwright() as instancia_playwright:
        instancia_navegador = None
        pagina_ativa = None
        conexao_cdp_bem_sucedida = False

        # 1. Tenta conectar via CDP a um navegador já aberto pelo usuário
        try:
            print(
                f"[Main] Tentando conectar ao navegador existente em {endereco_conexao_cdp}...",
                flush=True,
            )
            instancia_navegador = await instancia_playwright.chromium.connect_over_cdp(
                endereco_conexao_cdp
            )
            contexto_navegador = instancia_navegador.contexts[0]

            for aba_navegador_existente in contexto_navegador.pages:
                if "linkedin.com" in aba_navegador_existente.url:
                    pagina_ativa = aba_navegador_existente
                    break

            if not pagina_ativa:
                print(
                    "[Main] Aba do LinkedIn não encontrada no navegador via CDP. Criando nova aba...",
                    flush=True,
                )
                pagina_ativa = await contexto_navegador.new_page()

            await pagina_ativa.bring_to_front()
            conexao_cdp_bem_sucedida = True
            print("[Main] Sucesso ao conectar no navegador existente (CDP).", flush=True)

        except Exception as excecao_erro:
            print(f"[Main] Não foi possível conectar via CDP ({excecao_erro}).", flush=True)

        # 2. Fallback: abre um novo navegador caso a conexão CDP falhe
        if not conexao_cdp_bem_sucedida:
            print("[Main] Abrindo novo navegador isolado...", flush=True)
            instancia_navegador = await instancia_playwright.chromium.launch(
                headless=False, args=["--start-maximized"]
            )
            contexto_navegador = await instancia_navegador.new_context(
                viewport={"width": 1280, "height": 800}
            )
            pagina_ativa = await contexto_navegador.new_page()

            await realizar_login_linkedin(pagina_ativa, email_usuario, senha_usuario)

        # 3. Executa a rotina de envio de parabéns às conexões
        await enviar_mensagens_parabens_conexoes(pagina_ativa)

        if not conexao_cdp_bem_sucedida:
            print("[Main] Fechando navegador...", flush=True)
            await instancia_navegador.close()
        else:
            print(
                "[Main] Processo finalizado no navegador via CDP. O navegador permanece aberto.",
                flush=True,
            )


if __name__ == "__main__":
    asyncio.run(iniciar_automacao_linkedin())
