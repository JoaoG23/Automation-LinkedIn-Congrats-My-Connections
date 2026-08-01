import asyncio
from playwright.async_api import Page, ElementHandle


async def fechar_modais_de_chat(pagina: Page) -> None:
    """Pressiona Escape e clica no botão Descartar caso algum modal ou caixa de rascunho continue aberta.

    Args:
        pagina (Page): Instância da página do Playwright.
    """
    try:
        await pagina.keyboard.press("Escape")
        await asyncio.sleep(1)

        botao_descartar = pagina.locator('button:has-text("Descartar")').last
        if await botao_descartar.is_visible():
            await botao_descartar.click()
            await asyncio.sleep(1)

        await pagina.keyboard.press("Escape")
        await asyncio.sleep(1)
    except Exception as excecao_erro:
        print(f"[Chat] Erro ao fechar modal de chat: {excecao_erro}", flush=True)


async def enviar_mensagem_no_chat_modal(
    pagina: Page, elemento_botao: ElementHandle, mensagem_texto: str
) -> bool:
    """Clica no botão de parabéns, digita a mensagem gerada pela IA na caixa de texto e realiza o envio.

    Args:
        pagina (Page): Instância da página do Playwright.
        elemento_botao (ElementHandle): O botão de ação da pessoa.
        mensagem_texto (str): O texto de parabéns a ser enviado.

    Returns:
        bool: True se a mensagem foi enviada com sucesso, False caso contrário.
    """
    try:
        await elemento_botao.scroll_into_view_if_needed()
        await elemento_botao.click()
        print("[Congrats] Clicou no botão. Aguardando modal de chat...", flush=True)
        await asyncio.sleep(2.5)

        caixa_texto_chat = pagina.locator(
            'div.msg-form__contenteditable, div[role="textbox"][contenteditable="true"]'
        ).last

        if not await caixa_texto_chat.is_visible():
            print("[Congrats] Caixa de chat não visível.", flush=True)
            await fechar_modais_de_chat(pagina)
            return False

        await caixa_texto_chat.click()
        await pagina.keyboard.press("Control+A")
        await pagina.keyboard.press("Backspace")
        await asyncio.sleep(0.5)

        await pagina.keyboard.type(mensagem_texto, delay=10)
        await asyncio.sleep(1)

        botao_enviar = pagina.locator(
            'button.msg-form__send-button, button:has-text("Enviar")'
        ).last

        if await botao_enviar.is_visible() and not await botao_enviar.is_disabled():
            await botao_enviar.click()
            print("[Congrats] Mensagem enviada com sucesso!", flush=True)
            await asyncio.sleep(1)
            await fechar_modais_de_chat(pagina)
            return True
        else:
            print("[Congrats] Botão de enviar não encontrado ou desabilitado.", flush=True)
            await fechar_modais_de_chat(pagina)
            return False

    except Exception as excecao_erro:
        print(f"[Congrats] Erro ao processar envio de mensagem: {excecao_erro}", flush=True)
        await fechar_modais_de_chat(pagina)
        return False
