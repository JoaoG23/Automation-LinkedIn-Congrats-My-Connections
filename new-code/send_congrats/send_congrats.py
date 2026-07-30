import asyncio
from playwright.async_api import Page
from utils.llm_message import generate_message_with_ai
from utils.scroll_by import scroll_page

async def extract_event_context(page: Page, target_btn) -> str:
    """Extrai o texto do evento (ex: novo cargo, aniversário) para usar como contexto."""
    context_text = await page.evaluate('''btn => {
        // O aria-label do link/botão contém um texto perfeito se existir
        const ariaContext = btn.getAttribute('aria-label');
        if (ariaContext) {
            return ariaContext;
        }
        
        // Fallback: pega todo o texto do container pai (o card da pessoa)
        let container = btn.closest('li') || btn.closest('div.discover-entity-type-card') || btn.closest('div');
        return container ? container.innerText : "";
    }''', target_btn)
    
    return context_text.strip().replace('\n', ' ')

async def send_congrats_to_connections(page: Page, limit: int = 1000) -> None:
    """Navega para a tela de conexões e envia as congratulações para todos encontrados."""
    print("[Congrats] Navegando para a página de Catch-up (Catch-up / All)...")
    await page.goto("https://www.linkedin.com/mynetwork/catch-up/all/", wait_until="domcontentloaded")
    await asyncio.sleep(5)
    
    print("[Congrats] Iniciando busca e envio de mensagens...")

    processed_labels = set()
    processed_count = 0
    scroll_down_retries = 0
    
    # Aumentamos o limite de tentativas de scroll para garantir que chegue mesmo ao fim
    while scroll_down_retries < 20:
        if processed_count >= limit:
            break
            
        selector = (
            'button:has([id*="send-privately"]), '
            'a:has([id*="send-privately"]), '
            '[role="button"]:has([id*="send-privately"]), '
            'button:has-text("Parabéns"), '
            'button:has-text("Feliz"), '
            'button:has-text("Comemore"), '
            '[role="button"]:has-text("Parabéns"), '
            '[role="button"]:has-text("Feliz"), '
            '[role="button"]:has-text("Comemore"), '
            'button[aria-label*="mensagem" i], '
            'a[aria-label*="mensagem" i]'
        )
        current_buttons = await page.query_selector_all(selector)
        
        button_to_process = None
        target_label = None
        
        # Encontra o primeiro botão que ainda não processamos
        for btn in current_buttons:
            # Tenta pegar aria-label, se não tiver usa o texto do card inteiro para identificar univocamente a pessoa
            label = await btn.get_attribute('aria-label')
            if not label:
                card_text = await btn.evaluate("el => { let c = el.closest('li') || el.closest('div.discover-entity-type-card') || el.closest('div'); return c ? c.innerText : null }")
                label = card_text.strip() if card_text else "unknown"
                
            if label and label not in processed_labels and label != "unknown":
                button_to_process = btn
                target_label = label
                break
                
        if button_to_process:
            scroll_down_retries = 0 # Resetamos pois achamos um botão
            try:
                context = await extract_event_context(page, button_to_process)
                print(f"[Congrats] Contexto identificado: {context[:60]}...")
                
                message = await generate_message_with_ai(context)
                
                await button_to_process.scroll_into_view_if_needed()
                await button_to_process.click()
                print(f"[Congrats] Clicou no botão. Aguardando modal de chat...")
                await asyncio.sleep(2.5) # Aguarda modal abrir
                
                chat_box = page.locator('div.msg-form__contenteditable, div[role="textbox"][contenteditable="true"]').last
                
                if await chat_box.is_visible():
                    await chat_box.click()
                    
                    # Limpa a caixa de texto
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await asyncio.sleep(0.5)
                    
                    await page.keyboard.type(message, delay=10)
                    await asyncio.sleep(1)
                    
                    # Clica em enviar
                    send_btn = page.locator('button.msg-form__send-button, button:has-text("Enviar")').last
                    if await send_btn.is_visible() and not await send_btn.is_disabled():
                        await send_btn.click()
                        print(f"[Congrats] Mensagem enviada com sucesso!")
                        processed_count += 1
                        await asyncio.sleep(1)
                    else:
                        print("[Congrats] Botão de enviar não encontrado ou desabilitado.")
                else:
                    print("[Congrats] Caixa de chat não visível.")
                
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
                print(f"[Congrats] Erro ao processar: {e}")
                await page.keyboard.press("Escape")
                await asyncio.sleep(1)
                
            # Adiciona ao set para nunca mais tentar processar este mesmo elemento nesta execução
            processed_labels.add(target_label)
            
        else:
            # Não achou botão novo na tela atual. Rola a página para procurar mais!
            last_height = await page.evaluate("document.body.scrollHeight")
            await scroll_page(page, scroll_times=4, delay_seconds=2)
            new_height = await page.evaluate("document.body.scrollHeight")
            
            if new_height == last_height:
                # Se a altura não mudou, significa que não carregou mais nada
                scroll_down_retries += 1
            else:
                # Se a altura mudou, a página continua crescendo! Resetamos a contagem para continuar varrendo infinitamente
                scroll_down_retries = 0
            
    print(f"[Congrats] Processo finalizado. Total de mensagens enviadas: {processed_count}")
