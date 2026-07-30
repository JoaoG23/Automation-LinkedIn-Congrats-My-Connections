import asyncio
import pytest
from unittest.mock import patch, AsyncMock
from utils.llm_message import generate_message_with_ai

@pytest.mark.asyncio
async def test_generate_message_success():
    """Testa caso de sucesso da IA retornando uma mensagem."""
    # Como não temos um mock simples para o ollama síncrono dentro do executor, 
    # mockamos a função inteira de request se necessário, 
    # mas para simplificar, mockaremos o retorno.
    with patch('utils.llm_message.ollama.Client.chat') as mock_chat:
        mock_chat.return_value = {"message": {"content": "Parabéns pela promoção!"}}
        
        message = await generate_message_with_ai("Começou em um novo cargo")
        
        assert message == "Parabéns pela promoção!"

@pytest.mark.asyncio
async def test_generate_message_error_fallback():
    """Testa caso de erro onde a IA falha e retorna o fallback."""
    with patch('utils.llm_message.ollama.Client.chat') as mock_chat:
        mock_chat.side_effect = Exception("Erro simulado do Ollama")
        
        message = await generate_message_with_ai("Começou em um novo cargo")
        
        assert message == "Parabéns!"
