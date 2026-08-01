import asyncio
import sys
import os
from unittest.mock import patch

# Garante que o diretório raiz do projeto esteja no sys.path
diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from utils.llm_message import gerar_mensagem_com_inteligencia_artificial


async def executar_teste_geracao_mensagem_sucesso():
    """Testa caso de sucesso da IA retornando uma mensagem válida."""
    with patch("utils.llm_message.ollama.Client.chat") as simulador_chat_ollama:
        simulador_chat_ollama.return_value = {
            "message": {"content": "Parabéns pela promoção!"}
        }

        mensagem_gerada = await gerar_mensagem_com_inteligencia_artificial(
            "Começou em um novo cargo"
        )

        assert mensagem_gerada == "Parabéns pela promoção!"
        print("[Teste Sucesso] Mensagem gerada corretamente.", flush=True)


async def executar_teste_geracao_mensagem_falha_fallback():
    """Testa caso de erro onde a IA falha e deve retornar a mensagem padrão de fallback."""
    with patch("utils.llm_message.ollama.Client.chat") as simulador_chat_ollama:
        simulador_chat_ollama.side_effect = Exception("Erro simulado na chamada da IA")

        mensagem_gerada = await gerar_mensagem_com_inteligencia_artificial(
            "Começou em um novo cargo"
        )

        assert mensagem_gerada == "Parabéns!"
        print("[Teste Fallback] Mensagem padrão retornada corretamente.", flush=True)


def test_geracao_mensagem_sucesso():
    asyncio.run(executar_teste_geracao_mensagem_sucesso())


def test_geracao_mensagem_falha_fallback():
    asyncio.run(executar_teste_geracao_mensagem_falha_fallback())


if __name__ == "__main__":
    test_geracao_mensagem_sucesso()
    test_geracao_mensagem_falha_fallback()
