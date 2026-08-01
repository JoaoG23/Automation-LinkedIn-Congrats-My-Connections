import asyncio
from playwright.async_api import Page
from utils.llm_message import generate_message_with_ai
from utils.scroll_by import scroll_page


async def extract_event_context(page: Page, target_btn) -> str:
    """Extrai o texto do evento (ex: novo cargo, aniversário) para usar como contexto."""
    context_text = await page.evaluate(
        """btn => {
        // O aria-label do link/botão contém um texto perfeito se existir
        const ariaContext = btn.getAttribute('aria-label');
        if (ariaContext) {
            return ariaContext;
        }
        
        // Fallback: pega todo o texto do container pai (o card da pessoa)
        let container = btn.closest('li') || btn.closest('div.discover-entity-type-card') || btn.closest('div');
        return container ? container.innerText : "";
    }""",
        target_btn,
    )

    return context_text.strip().replace("\n", " ")


async def send_congrats_to_connections(page: Page, limit: int = 1000) -> None:
    """Navega para a tela de conexões e envia as congratulações para todos encontrados."""
    print("[Congrats] Navegando para a página de Catch-up (Catch-up / All)...")
    await page.goto(
        "https://www.linkedin.com/mynetwork/catch-up/all/",
        wait_until="domcontentloaded",
    )
    await asyncio.sleep(5)

    print("[Congrats] Iniciando busca e envio de mensagens...")

    processed_labels = set()
    processed_count = 0
    scroll_down_retries = 0

    # Limite de 3 tentativas seguidas de scroll sem encontrar novos cards
    max_scroll_retries = 5
    while scroll_down_retries < max_scroll_retries:
        if processed_count >= limit:
            break

        selector = (
            'main button:has([id*="send-privately"]), '
            'main a:has([id*="send-privately"]), '
            'main [role="button"]:has([id*="send-privately"]), '
            'main button:has-text("Parabéns"), '
            'main button:has-text("Feliz"), '
            'main button:has-text("Comemore"), '
            'main [role="button"]:has-text("Parabéns"), '
            'main [role="button"]:has-text("Feliz"), '
            'main [role="button"]:has-text("Comemore"), '
            'main button[aria-label*="mensagem" i], '
            'main a[aria-label*="mensagem" i], '
            'div.scaffold-layout__main button, '
            'div.scaffold-layout__main a'
        )
        current_buttons = await page.query_selector_all(selector)

        button_to_process = None
        target_label = None

        # Encontra o primeiro botão que ainda não processamos
        for btn in current_buttons:
            try:
                if not await btn.is_visible():
                    continue

                # Ignora botões dentro do painel/overlay de mensagens (chat no canto inferior)
                is_in_chat = await btn.evaluate(
                    "el => !!el.closest('.msg-overlay-container, .msg-overlay-bubble-header')"
                )
                if is_in_chat:
                    continue

                label = await btn.get_attribute("aria-label")
                if not label:
                    card_text = await btn.evaluate(
                        "el => { let c = el.closest('li') || el.closest('div.discover-entity-type-card') || el.closest('div'); return c ? c.innerText : null }"
                    )
                    label = card_text.strip() if card_text else ""

                if label and label not in processed_labels:
                    if "Responder" in label and is_in_chat:
                        continue
                    button_to_process = btn
                    target_label = label
                    break
            except Exception:
                continue

        if button_to_process and target_label:
            scroll_down_retries = 0  # Resetamos pois achamos um botão
            try:
                context = await extract_event_context(page, button_to_process)
                print(f"[Congrats] Contexto identificado: {context[:60]}...", flush=True)

                message = await generate_message_with_ai(context)

                await button_to_process.scroll_into_view_if_needed()
                await button_to_process.click()
                print(f"[Congrats] Clicou no botão. Aguardando modal de chat...", flush=True)
                await asyncio.sleep(2.5)  # Aguarda modal abrir

                chat_box = page.locator(
                    'div.msg-form__contenteditable, div[role="textbox"][contenteditable="true"]'
                ).last

                if await chat_box.is_visible():
                    await chat_box.click()

                    # Limpa a caixa de texto
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await asyncio.sleep(0.5)

                    await page.keyboard.type(message, delay=10)
                    await asyncio.sleep(1)

                    # Clica em enviar
                    send_btn = page.locator(
                        'button.msg-form__send-button, button:has-text("Enviar")'
                    ).last
                    if await send_btn.is_visible() and not await send_btn.is_disabled():
                        await send_btn.click()
                        print(f"[Congrats] Mensagem enviada com sucesso!", flush=True)
                        processed_count += 1
                        await asyncio.sleep(1)
                    else:
                        print(
                            "[Congrats] Botão de enviar não encontrado ou desabilitado.",
                            flush=True
                        )
                else:
                    print("[Congrats] Caixa de chat não visível.", flush=True)

                # Fecha o modal
                await page.keyboard.press("Escape")
                await asyncio.sleep(1)

                discard_btn = page.locator('button:has-text("Descartar")').last
                if await discard_btn.is_visible():
                    await discard_btn.click()
                    await asyncio.sleep(1)

                await page.keyboard.press("Escape")
                await asyncio.sleep(1)

            except Exception as e:
                print(f"[Congrats] Erro ao processar: {e}", flush=True)
                await page.keyboard.press("Escape")
                await asyncio.sleep(1)

            # Adiciona ao set para nunca mais tentar processar este mesmo elemento nesta execução
            processed_labels.add(target_label)

        else:
            # Tenta clicar em botões como 'Exibir mais' ou 'Ver mais' se existirem
            show_more_btn = page.locator(
                'button:has-text("Exibir mais"), button:has-text("Carregar mais"), button:has-text("Ver mais"), button:has-text("Show more")'
            ).first
            try:
                if await show_more_btn.is_visible():
                    print("[Congrats] Encontrado botão 'Exibir mais'. Clicando...", flush=True)
                    await show_more_btn.click()
                    await asyncio.sleep(2)
            except Exception:
                pass

            # Rola a página usando simulação de roda do mouse e scroll de DOM
            await scroll_page(page, scroll_times=2, delay_seconds=2.0)

            # Verifica se surgiram novos botões visíveis não processados
            new_buttons = await page.query_selector_all(selector)
            found_new = False
            for btn in new_buttons:
                try:
                    if not await btn.is_visible():
                        continue
                    is_in_chat = await btn.evaluate(
                        "el => !!el.closest('.msg-overlay-container, .msg-overlay-bubble-header')"
                    )
                    if is_in_chat:
                        continue
                    lbl = await btn.get_attribute("aria-label")
                    if not lbl:
                        card_text = await btn.evaluate(
                            "el => { let c = el.closest('li') || el.closest('div.discover-entity-type-card') || el.closest('div'); return c ? c.innerText : null }"
                        )
                        lbl = card_text.strip() if card_text else ""
                    if lbl and lbl not in processed_labels:
                        found_new = True
                        break
                except Exception:
                    continue

            if not found_new:
                scroll_down_retries += 1
                print(
                    f"[Scroll] Nenhum novo card encontrado. Tentativa {scroll_down_retries}/{max_scroll_retries}...",
                    flush=True
                )
            else:
                scroll_down_retries = 0

    print(
        f"[Congrats] Não há mais pessoas para enviar mensagens ou o limite foi atingido.",
        flush=True
    )
    print(
        f"[Congrats] Processo finalizado com sucesso. Total de mensagens enviadas: {processed_count}",
        flush=True
    )



