import asyncio
from playwright.async_api import Page


async def realizar_login_linkedin(
    pagina: Page, email_usuario: str, senha_usuario: str
) -> None:
    """Realiza o processo de login na conta do LinkedIn usando o Playwright.

    Args:
        pagina (Page): Instância da página do Playwright.
        email_usuario (str): Endereço de e-mail de login do usuário.
        senha_usuario (str): Senha da conta do usuário.
    """
    print("[Login] Navegando para a página inicial do LinkedIn...", flush=True)

    try:
        await pagina.goto(
            "https://www.linkedin.com/login",
            wait_until="domcontentloaded",
            timeout=30000,
        )
    except Exception as excecao_erro:
        print(f"[Login] Erro ao carregar página de login: {excecao_erro}", flush=True)
        return

    print("[Login] Preenchendo credenciais...", flush=True)

    campo_entrada_email = pagina.locator('#username, input[name="session_key"]').first
    if not await campo_entrada_email.is_visible():
        campo_entrada_email = pagina.get_by_role("textbox", name="E-mail ou telefone").first

    await campo_entrada_email.click()
    await campo_entrada_email.fill(email_usuario)

    campo_entrada_senha = pagina.locator('#password, input[name="session_password"]').first
    if not await campo_entrada_senha.is_visible():
        campo_entrada_senha = pagina.get_by_role("textbox", name="Senha").first

    await campo_entrada_senha.click()
    await campo_entrada_senha.fill(senha_usuario)

    print("[Login] Enviando formulário...", flush=True)
    botao_enviar_formulario = pagina.locator('button[type="submit"]').first
    if await botao_enviar_formulario.is_visible():
        await botao_enviar_formulario.click()
    else:
        await campo_entrada_senha.press("Enter")

    try:
        await pagina.wait_for_url("**/feed**", timeout=30000)
        print("[Login] Login realizado com sucesso!", flush=True)
    except Exception:
        print(
            "[Login] Não foi possível validar o redirecionamento automático para o feed. "
            "Pode ser necessária autenticação em duas etapas (2FA).",
            flush=True,
        )
        await asyncio.sleep(5)


# Alias mantido para retrocompatibilidade
do_login = realizar_login_linkedin
