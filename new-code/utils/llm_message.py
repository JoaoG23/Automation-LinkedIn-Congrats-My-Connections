import asyncio
import ollama

async def generate_message_with_ai(context_text: str, fallback_message: str = "Parabéns!") -> str:
    """Gera uma mensagem de congratulações usando Ollama local, com timeout de 10 segundos."""
    
    prompt = f"Você é um profissional simpático. Crie uma curta mensagem amigável e profissional (máximo de 50 caracteres, bem curto e objetivo) parabenizando a pessoa no LinkedIn com base no seguinte evento: '{context_text}'. Seja direto. Não use emojis. Se o contexto não for claro, diga 'Parabéns!'."
    
    async def request_llm():
        try:
            loop = asyncio.get_event_loop()
            
            # Executa a chamada do ollama de forma síncrona dentro de um executor assíncrono
            def fetch_from_ollama():
                client = ollama.Client(host='http://127.0.0.1:11434')
                return client.chat(
                    model='llama3.2', # Modelo padrão
                    messages=[{'role': 'user', 'content': prompt}],
                    options={'temperature': 0.3}
                )
                
            response = await loop.run_in_executor(None, fetch_from_ollama)
            
            if response and "message" in response and "content" in response["message"]:
                text = response["message"]["content"].strip().replace('"', '')
                if len(text) > 0:
                    return text
            
            return fallback_message
        except Exception as e:
            print(f"[LLM] Erro ao consultar IA Ollama: {e}")
            return fallback_message

    print("[LLM] Solicitando geração de texto à IA...")
    try:
        # Timeout de 10 segundos
        message = await asyncio.wait_for(request_llm(), timeout=10.0)
        print(f"[LLM] Mensagem gerada: {message}")
        return message
    except asyncio.TimeoutError:
        print("[LLM] Timeout de 10s excedido. Usando mensagem padrão.")
        return fallback_message
