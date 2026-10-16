import asyncio
from playwright.async_api import async_playwright
import os

async def renovar_login():
    async with async_playwright() as p:
        pasta_perfil = os.path.join(os.getcwd(), "perfil_linkedin_bot")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=pasta_perfil, headless=False, no_viewport=True, args=["--start-maximized"]
        )
        page = await context.new_page()
        
        print("Acessando a página de login...")
        await page.goto("https://www.linkedin.com/login")
        
        print("\n" + "="*60)
        print("🚨 AÇÃO NECESSÁRIA: FAÇA O LOGIN MANUALMENTE NO NAVEGADOR!")
        print("Vá para a janela do robô, digite seu e-mail e senha e faça o login.")
        print("Se o LinkedIn pedir código de verificação (Captcha/Email), resolva-o.")
        print("O robô vai esperar pacientemente por 2 minutos (120 segundos).")
        print("="*60 + "\n")
        
        # Pausa o código por 2 minutos para você ter tempo de fazer o login na tela
        await asyncio.sleep(120)
        
        print("Tempo esgotado. Fechando o navegador e salvando a sessão...")
        await context.close()

if __name__ == "__main__":
    asyncio.run(renovar_login())