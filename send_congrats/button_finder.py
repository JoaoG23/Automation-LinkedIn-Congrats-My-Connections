from typing import Optional, Tuple, List, Set
from playwright.async_api import Page, ElementHandle


def obter_seletor_botoes_parabens() -> str:
    """Retorna a string do seletor CSS utilizado para encontrar botões de parabéns na página principal.

    Returns:
        str: Seletores CSS combinados focados na área principal do LinkedIn.
    """
    return (
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


async def verificar_se_elemento_esta_no_chat(elemento_botao: ElementHandle) -> bool:
    """Verifica se o botão capturado pertence ao dock/overlay de chat inferior do LinkedIn.

    Args:
        elemento_botao (ElementHandle): O botão a ser verificado.

    Returns:
        bool: True se o botão estiver dentro do painel de chat, False caso contrário.
    """
    return await elemento_botao.evaluate(
        "elemento => !!elemento.closest('.msg-overlay-container, .msg-overlay-bubble-header')"
    )


async def obter_rotulo_identificador_do_card(elemento_botao: ElementHandle) -> str:
    """Obtém um identificador único textual para o card associado ao botão de parabéns.

    Args:
        elemento_botao (ElementHandle): O botão do card.

    Returns:
        str: O atributo aria-label ou o texto contido no card pai.
    """
    rotulo_aria_label = await elemento_botao.get_attribute("aria-label")
    if rotulo_aria_label and rotulo_aria_label.strip():
        return rotulo_aria_label.strip()

    texto_card_pai = await elemento_botao.evaluate(
        """elemento => {
            let container_card = elemento.closest('li') || 
                                 elemento.closest('div.discover-entity-type-card') || 
                                 elemento.closest('div');
            return container_card ? container_card.innerText : null;
        }"""
    )
    return texto_card_pai.strip() if texto_card_pai else ""


async def encontrar_proximo_botao_para_processar(
    pagina: Page, conjunto_rotulos_processados: Set[str]
) -> Tuple[Optional[ElementHandle], Optional[str]]:
    """Busca o próximo botão elegível de parabéns que ainda não tenha sido processado nesta execução.

    Args:
        pagina (Page): Instância da página do Playwright.
        conjunto_rotulos_processados (Set[str]): Conjunto contendo identificadores de cards já processados.

    Returns:
        Tuple[Optional[ElementHandle], Optional[str]]: Tupla com o elemento do botão e seu identificador textual.
    """
    seletor_css = obter_seletor_botoes_parabens()
    lista_botoes_encontrados: List[ElementHandle] = await pagina.query_selector_all(seletor_css)

    for elemento_botao in lista_botoes_encontrados:
        try:
            if not await elemento_botao.is_visible():
                continue

            esta_no_chat = await verificar_se_elemento_esta_no_chat(elemento_botao)
            if esta_no_chat:
                continue

            rotulo_identificador = await obter_rotulo_identificador_do_card(elemento_botao)

            if rotulo_identificador and rotulo_identificador not in conjunto_rotulos_processados:
                if "Responder" in rotulo_identificador and esta_no_chat:
                    continue
                return elemento_botao, rotulo_identificador
        except Exception:
            continue

    return None, None


async def verificar_se_existem_novos_botoes(
    pagina: Page, conjunto_rotulos_processados: Set[str]
) -> bool:
    """Verifica se há pelo menos um novo botão visível não processado após a rolagem da página.

    Args:
        pagina (Page): Instância da página do Playwright.
        conjunto_rotulos_processados (Set[str]): Conjunto de rótulos já processados.

    Returns:
        bool: True se encontrar ao menos um novo botão elegível, False caso contrário.
    """
    seletor_css = obter_seletor_botoes_parabens()
    lista_novos_botoes: List[ElementHandle] = await pagina.query_selector_all(seletor_css)

    for elemento_botao in lista_novos_botoes:
        try:
            if not await elemento_botao.is_visible():
                continue

            esta_no_chat = await verificar_se_elemento_esta_no_chat(elemento_botao)
            if esta_no_chat:
                continue

            rotulo_identificador = await obter_rotulo_identificador_do_card(elemento_botao)

            if rotulo_identificador and rotulo_identificador not in conjunto_rotulos_processados:
                return True
        except Exception:
            continue

    return False
