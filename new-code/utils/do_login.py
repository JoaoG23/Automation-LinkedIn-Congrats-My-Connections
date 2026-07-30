import asyncio
from playwright.async_api import Page

async def do_login(page: Page, email: str, password: str) -> None:
    """Realiza o login na conta do LinkedIn usando o Playwright."""
    print("[Login] Navegando para a página inicial do LinkedIn...")
    
    try:
        await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        print(f"[Login] Erro ao carregar página de login: {e}")
        return

    print("[Login] Preenchendo credenciais...")
    
    email_input = page.locator('#username, input[name="session_key"]').first
    if not await email_input.is_visible():
        email_input = page.get_by_role("textbox", name="E-mail ou telefone").first
    
    await email_input.click()
    await email_input.fill(email)
    
    password_input = page.locator('#password, input[name="session_password"]').first
    if not await password_input.is_visible():
        password_input = page.get_by_role("textbox", name="Senha").first
        
    await password_input.click()
    await password_input.fill(password)
    
    print("[Login] Enviando formulário...")
    submit_button = page.locator('button[type="submit"]').first
    if await submit_button.is_visible():
        await submit_button.click()
    else:
        await password_input.press("Enter")
        
    try:
        # Espera a página redirecionar para o feed
        await page.wait_for_url("**/feed**", timeout=30000)
        print("[Login] Login realizado com sucesso!")
    except Exception:
        print("[Login] Não foi possível validar o redirecionamento para o feed. O login pode exigir autenticação adicional (2FA).")
        await asyncio.sleep(5)
