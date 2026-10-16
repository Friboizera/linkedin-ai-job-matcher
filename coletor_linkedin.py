import asyncio
from playwright.async_api import async_playwright
import os
import re

async def coletor_definitivo():
    async with async_playwright() as p:
        pasta_perfil = os.path.join(os.getcwd(), "perfil_linkedin_bot")
        context = await p.chromium.launch_persistent_context(
            user_data_dir=pasta_perfil, headless=False, no_viewport=True, args=["--start-maximized"]
        )
        page = await context.new_page()
        
        print("🚀 Iniciando o Coletor Sniper (1 Vaga por Salto)...")
        job_ids_totais = set()
        
        # Pula de 1 em 1. start=0 (vaga 1), start=1 (vaga 2)... até a vaga 20
        for offset in range(20):
            print(f"\nCarregando link direto para a vaga {offset + 1} da lista...")
            url = f"https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist&location=Worldwide&f_WT=2&start={offset}"
            await page.goto(url)
            
            # Aguarda a vaga carregar no painel da direita
            await asyncio.sleep(4)
            
            html_bruto = await page.content()
            
            # Pega o ID da vaga que está em destaque na URL atual da página
            url_atual = page.url
            match_url = re.search(r'currentJobId=(\d{9,10})', url_atual)
            
            if match_url:
                jid = match_url.group(1)
                job_ids_totais.add(jid)
                print(f"✔️ Capturou a vaga ID: {jid}. Total na sacola: {len(job_ids_totais)}")
            else:
                # Plano B: Procura no código bruto da vaga em destaque
                ids = re.findall(r'"jobId":"(\d{9,10})"', html_bruto)
                if ids:
                    job_ids_totais.add(ids[0])
                    print(f"✔️ Capturou a vaga ID (Plano B): {ids[0]}. Total na sacola: {len(job_ids_totais)}")
        
        lista_final = [f"https://www.linkedin.com/jobs/view/{jid}/" for jid in job_ids_totais]
        
        print(f"\n✅ SUCESSO: Foram separadas {len(lista_final)} vagas únicas para avaliação!")
        
        pasta_destino = "dados_vagas"
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_arquivo = os.path.join(pasta_destino, "links_extraidos.txt")
        
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            for link in lista_final:
                f.write(link + "\n")
                
        print(f"📁 Arquivo salvo em: {caminho_arquivo}")
        await context.close()

if __name__ == "__main__":
    asyncio.run(coletor_definitivo())