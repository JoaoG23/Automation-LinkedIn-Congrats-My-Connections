import asyncio
import ollama


async def gerar_mensagem_com_inteligencia_artificial(
    texto_contexto_evento: str, mensagem_padrao_fallback: str = "Parabéns!"
) -> str:
    """Gera uma mensagem de congratulações personalizada utilizando o modelo Ollama local.

    Args:
        texto_contexto_evento (str): O texto extraído do card no LinkedIn descrevendo o evento.
        mensagem_padrao_fallback (str): Mensagem padrão para utilizar caso a IA falhe ou atinja timeout.

    Returns:
        str: Texto amigável e objetivo de congratulação gerado pela IA ou a mensagem padrão.
    """
    prompt_comando = (
        f"Você é um profissional simpático. Crie uma curta mensagem amigável e profissional "
        f"(máximo de 50 caracteres, bem curto e objetivo) parabenizando a pessoa no LinkedIn "
        f"com base no seguinte evento: '{texto_contexto_evento}'. Seja direto. Não use emojis. "
        f"Se o contexto não for claro, diga 'Parabéns!'."
    )

    async def executar_requisicao_llm() -> str:
        try:
            loop_eventos_asyncio = asyncio.get_event_loop()

            def requisitar_servico_ollama():
                cliente_ollama = ollama.Client(host="http://127.0.0.1:11434")
                return cliente_ollama.chat(
                    model="llama3.2",
                    messages=[{"role": "user", "content": prompt_comando}],
                    options={"temperature": 0.3},
                )

            resposta_ia_ollama = await loop_eventos_asyncio.run_in_executor(
                None, requisitar_servico_ollama
            )

            if (
                resposta_ia_ollama
                and "message" in resposta_ia_ollama
                and "content" in resposta_ia_ollama["message"]
            ):
                texto_resposta_limpo = (
                    resposta_ia_ollama["message"]["content"].strip().replace('"', "")
                )
                if len(texto_resposta_limpo) > 0:
                    return texto_resposta_limpo

            return mensagem_padrao_fallback
        except Exception as excecao_erro:
            print(f"[LLM] Erro ao consultar IA Ollama: {excecao_erro}", flush=True)
            return mensagem_padrao_fallback

    print("[LLM] Solicitando geração de texto à IA...", flush=True)
    try:
        mensagem_gerada = await asyncio.wait_for(
            executar_requisicao_llm(), timeout=10.0
        )
        print(f"[LLM] Mensagem gerada: {mensagem_gerada}", flush=True)
        return mensagem_gerada
    except asyncio.TimeoutError:
        print(
            "[LLM] Timeout de 10s excedido na consulta à IA. Usando mensagem padrão.",
            flush=True,
        )
        return mensagem_padrao_fallback


# Alias mantido para retrocompatibilidade
generate_message_with_ai = gerar_mensagem_com_inteligencia_artificial
