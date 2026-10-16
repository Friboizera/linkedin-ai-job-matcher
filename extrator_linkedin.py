import asyncio
from playwright.async_api import async_playwright
import os
import re
from datetime import datetime

async def extrair_descricoes():
    pasta_dados = "dados_vagas"
    caminho_links = os.path.join(pasta_dados, "links_extraidos.txt")
    pasta_entrada = os.path.join(pasta_dados, "caixa_de_entrada")
    
    os.makedirs(pasta_entrada, exist_ok=True)
    
    if not os.path.exists(caminho_links):
        print("Arquivo de links não encontrado. Rode o coletor_linkedin.py primeiro.")
        return

    with open(caminho_links, "r", encoding="utf-8") as f:
        links = [linha.strip() for linha in f if linha.strip()]
        
    if not links:
        print("A lista de links está vazia.")
        return

    print(f"🚀 Iniciando a extração de texto de {len(links)} vagas do LinkedIn...")

    async with async_playwright() as p:
        pasta_perfil = os.path.join(os.getcwd(), "perfil_linkedin_bot")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=pasta_perfil, headless=False, no_viewport=True, args=["--start-maximized"]
        )
        page = await context.new_page()

        for i, url in enumerate(links):
            print(f"[{i+1}/{len(links)}] Extraindo: {url}")
            try:
                await page.goto(url)
                await asyncio.sleep(4) # Pausa para o JavaScript da página carregar o texto
                
                # Extrai todo o texto visível da página
                texto_vaga = await page.evaluate("document.body.innerText")
                
                # Tenta extrair o ID da vaga para o nome do arquivo
                vaga_id = "desconhecido"
                match_id = re.search(r'/view/(\d+)', url)
                if match_id:
                    vaga_id = match_id.group(1)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"linkedin_{vaga_id}_{timestamp}.txt"
                caminho_arquivo = os.path.join(pasta_entrada, nome_arquivo)
                
                # Salva no mesmo padrão do ingestor manual
                with open(caminho_arquivo, "w", encoding="utf-8") as f:
                    f.write(f"LINK: {url}\n")
                    f.write("-" * 50 + "\n")
                    f.write(texto_vaga)
                    
                print(f"✔️ Texto salvo na caixa de entrada: {nome_arquivo}")
                
            except Exception as e:
                print(f"❌ Erro ao extrair a vaga {url}: {e}")
            
            # Pausa humana para não acionar bloqueios do LinkedIn
            await asyncio.sleep(5) 
            
        await context.close()

    # Limpa o arquivo de links após extrair para não repetir o trabalho amanhã
    open(caminho_links, 'w').close()
    print("\n✅ Extração concluída! Arquivo links_extraidos.txt foi zerado.")
    print("👉 Próximo passo: Rodar o avaliador_vagas_pro.py para processar a caixa de entrada.")

if __name__ == "__main__":
    asyncio.run(extrair_descricoes())