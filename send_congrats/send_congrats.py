import asyncio
from typing import Set
from playwright.async_api import Page

from send_congrats.context_extractor import extrair_contexto_do_evento
from send_congrats.button_finder import (
    encontrar_proximo_botao_para_processar,
    verificar_se_existem_novos_botoes,
)
from send_congrats.chat_messenger import enviar_mensagem_no_chat_modal
from utils.llm_message import generate_message_with_ai
from utils.scroll_by import rolar_pagina_para_carregar_conteudo, scroll_page



async def clicar_botao_carregar_mais_se_existir(pagina: Page) -> None:
    """Procura e clica em botões de 'Exibir mais' ou 'Ver mais' na página do LinkedIn caso estejam visíveis.

    Args:
        pagina (Page): Instância da página do Playwright.
    """
    localizador_botao = pagina.locator(
        'button:has-text("Exibir mais"), button:has-text("Carregar mais"), button:has-text("Ver mais"), button:has-text("Show more")'
    ).first

    try:
        if await localizador_botao.is_visible():
            print("[Congrats] Encontrado botão 'Exibir mais'. Clicando...", flush=True)
            await localizador_botao.click()
            await asyncio.sleep(2)
    except Exception:
        pass


async def enviar_mensagens_parabens_conexoes(
    pagina: Page, limite_maximo_mensagens: int = 1000
) -> None:
    """Navega para a tela de conexões (Catch-Up) do LinkedIn e envia felicitações usando IA.

    Args:
        pagina (Page): Instância da página do Playwright.
        limite_maximo_mensagens (int): Quantidade máxima de mensagens a enviar nesta sessão. Defaults to 1000.
    """
    print("[Congrats] Navegando para a página de Catch-up (Catch-up / All)...", flush=True)
    await pagina.goto(
        "https://www.linkedin.com/mynetwork/catch-up/all/",
        wait_until="domcontentloaded",
    )
    await asyncio.sleep(5)

    print("[Congrats] Iniciando busca e envio de mensagens...", flush=True)

    conjunto_rotulos_processados: Set[str] = set()
    quantidade_mensagens_enviadas: int = 0
    contador_tentativas_scroll: int = 0
    limite_tentativas_scroll_sem_novos_cards: int = 5

    while contador_tentativas_scroll < limite_tentativas_scroll_sem_novos_cards:
        if quantidade_mensagens_enviadas >= limite_maximo_mensagens:
            break

        elemento_botao, rotulo_identificador = await encontrar_proximo_botao_para_processar(
            pagina, conjunto_rotulos_processados
        )

        if elemento_botao and rotulo_identificador:
            contador_tentativas_scroll = 0
            try:
                texto_contexto_evento = await extrair_contexto_do_evento(pagina, elemento_botao)
                print(
                    f"[Congrats] Contexto identificado: {texto_contexto_evento[:60]}...",
                    flush=True,
                )

                mensagem_gerada_ia = await generate_message_with_ai(texto_contexto_evento)

                sucesso_envio = await enviar_mensagem_no_chat_modal(
                    pagina, elemento_botao, mensagem_gerada_ia
                )

                if sucesso_envio:
                    quantidade_mensagens_enviadas += 1

            except Exception as excecao_erro:
                print(f"[Congrats] Erro ao processar card: {excecao_erro}", flush=True)

            conjunto_rotulos_processados.add(rotulo_identificador)

        else:
            await rolar_pagina_para_carregar_conteudo(
                pagina, quantidade_rolagens=2, tempo_espera_segundos=2.0
            )


            existem_novos_cards = await verificar_se_existem_novos_botoes(
                pagina, conjunto_rotulos_processados
            )

            if not existem_novos_cards:
                contador_tentativas_scroll += 1
                print(
                    f"[Scroll] Nenhum novo card encontrado. Tentativa {contador_tentativas_scroll}/{limite_tentativas_scroll_sem_novos_cards}...",
                    flush=True,
                )
            else:
                contador_tentativas_scroll = 0

    print(
        "[Congrats] Não há mais pessoas para enviar mensagens ou o limite foi atingido.",
        flush=True,
    )
    print(
        f"[Congrats] Processo finalizado com sucesso. Total de mensagens enviadas: {quantidade_mensagens_enviadas}",
        flush=True,
    )


# Alias mantido para retrocompatibilidade com chamadas de outros módulos
send_congrats_to_connections = enviar_mensagens_parabens_conexoes
