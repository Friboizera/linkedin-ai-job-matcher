import os
import re
from datetime import datetime

def iniciar_ingestao():
    pasta_entrada = os.path.join("dados_vagas", "caixa_de_entrada")
    os.makedirs(pasta_entrada, exist_ok=True)
    
    print("=== INGESTOR MANUAL DE VAGAS ===")
    print("Use este painel para inserir vagas de qualquer plataforma (Gupy, LinkedIn, Glassdoor, etc.)\n")
    
    link = input("🔗 Cole o Link da vaga (ou digite 'manual' se não tiver link): ").strip()
    if not link:
        link = "Inserção Manual"
        
    print("\n📝 Cole o texto completo da descrição da vaga abaixo.")
    print("⚠️  Quando terminar de colar, digite a palavra FIM em uma nova linha e aperte Enter.\n")
    
    linhas_texto = []
    while True:
        try:
            linha = input()
            # Identifica a palavra de parada para encerrar a captura
            if linha.strip().upper() == "FIM":
                break
            linhas_texto.append(linha)
        except EOFError:
            break
            
    texto_vaga = "\n".join(linhas_texto).strip()
    
    if not texto_vaga:
        print("Nenhum texto foi inserido. Operação cancelada.")
        return
        
    # Gera um ID único baseado na data e hora para não sobrescrever arquivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"vaga_manual_{timestamp}.txt"
    caminho_arquivo = os.path.join(pasta_entrada, nome_arquivo)
    
    # Salva o arquivo no formato padronizado que o nosso Avaliador vai ler
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(f"LINK: {link}\n")
        f.write("-" * 50 + "\n")
        f.write(texto_vaga)
        
    print(f"\n✅ SUCESSO: Vaga empacotada e salva na caixa de entrada!")
    print(f"📁 Arquivo gerado: {caminho_arquivo}")

if __name__ == "__main__":
    iniciar_ingestao()