import asyncio
from playwright.async_api import Page, ElementHandle


async def extrair_contexto_do_evento(
    pagina: Page, elemento_botao: ElementHandle
) -> str:
    """Extrai o texto do evento (ex: novo cargo, aniversário, tempo de empresa) para servir de contexto para a IA.
    
    Args:
        pagina (Page): A instância da página ativa no Playwright.
        elemento_botao (ElementHandle): O elemento HTML do botão de parabéns.

    Returns:
        str: Texto do evento formatado e limpo sem quebras de linha.
    """
    texto_contexto = await pagina.evaluate(
        """elemento => {
        // Tenta obter a descrição detalhada do atributo aria-label
        const textoAriaLabel = elemento.getAttribute('aria-label');
        if (textoAriaLabel && textoAriaLabel.trim().length > 0) {
            return textoAriaLabel;
        }
        
        // Fallback: localiza o card pai (li ou div do card) para extrair todo o conteúdo textual
        const containerPai = elemento.closest('li') || 
                             elemento.closest('div.discover-entity-type-card') || 
                             elemento.closest('div');
        return containerPai ? containerPai.innerText : "";
    }""",
        elemento_botao,
    )

    texto_contexto_limpo = texto_contexto.strip().replace("\n", " ")
    return texto_contexto_limpo
