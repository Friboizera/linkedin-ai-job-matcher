import os
import csv
import re
import shutil
import time
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

# Puxa a chave de segurança de forma invisível
CHAVE_API = os.getenv("GEMINI_API_KEY")

if not CHAVE_API:
    raise ValueError("⚠️ Chave da API não encontrada! Verifique se o arquivo .env existe e possui a variável GEMINI_API_KEY.")

genai.configure(api_key=CHAVE_API)
modelo = genai.GenerativeModel('models/gemini-flash-lite-latest')

PERFIL_CANDIDATO = """
O candidato é um Cientista de Dados nível Pleno (5 anos de experiência), residente no Brasil.
Núcleo de Especialidade: Estatística, Precificação (Pricing), Modelagem de Risco/Crédito, Inferência Causal, Python e SQL Avançado.
Objetivo: Transição prática para IA Generativa e LLMs.

REGRAS DE RIGOR E PUNIÇÃO EXTREMA (SCORE 0 a 100):
Avalie a vaga e defina um Score. Seja implacável nas punições abaixo:

1. REPROVAÇÃO AUTOMÁTICA (Score < 60 | FIT: NÃO):
- Vagas operacionais focadas apenas em Excel e planilhas.
- Vagas de nível STAFF, PRINCIPAL ou HEAD (Exigem 8+ anos de experiência, o candidato tem 5).
- Vagas que exigem stack pesada de Engenharia de Dados/MLOps (Databricks, PySpark, Kafka, Azure ML).
- Vagas onde a linguagem principal seja C# ou Java.
- Vagas genéricas com jargões vazios que não explicam o problema real de negócio.

2. APROVAÇÃO E RECOMPENSA (Score 85 a 100 | FIT: SIM):
- Match Perfeito (Score 95+): Vagas internacionais remotas, vagas estritamente focadas em Precificação/Seguros/Crédito, ou vagas que exigem desenvolvimento prático com LLMs/Python/SQL.
- Match Bom (Score 85-94): Vagas nacionais nível Pleno/Sênior que focam na stack core (Estatística, Python, Machine Learning tabular) mas sem exigências de infraestrutura pesada.

INSTRUÇÃO DE SAÍDA EXATA:
FIT: [SIM ou NÃO]
SCORE: [Número]
MOTIVO: [1 frase curta e direta justificando o score com base nas regras acima]
"""

def avaliar_com_gemini(texto_vaga):
    prompt = f"{PERFIL_CANDIDATO}\n\nTEXTO DA VAGA:\n{texto_vaga[:4000]}"
    try:
        resposta = modelo.generate_content(prompt)
        return resposta.text.strip()
    except Exception as e:
        return f"FIT: ERRO\nSCORE: 0\nMOTIVO: Falha na API ({e})"

def processar_caixa_de_entrada():
    pasta_entrada = os.path.join("dados_vagas", "caixa_de_entrada")
    pasta_arquivados = os.path.join("dados_vagas", "arquivados")
    caminho_planilha = os.path.join("dados_vagas", "planilha_gestao_vagas.csv")
    
    os.makedirs(pasta_entrada, exist_ok=True)
    os.makedirs(pasta_arquivados, exist_ok=True)
    
    arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith(".txt")]
    
    if not arquivos:
        print("📭 A caixa de entrada está vazia. Nenhuma vaga nova para avaliar.")
        return
        
    print(f"🚀 Iniciando avaliação cega de {len(arquivos)} vaga(s) na caixa de entrada...\n")
    
    arquivo_existe = os.path.exists(caminho_planilha)
    
    with open(caminho_planilha, "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        if not arquivo_existe:
            writer.writerow(["Data", "Score", "Fit", "Motivo", "Link da Vaga", "Status de Aplicação"])

        for i, nome_arquivo in enumerate(arquivos):
            caminho_arquivo = os.path.join(pasta_entrada, nome_arquivo)
            print(f"[{i+1}/{len(arquivos)}] Lendo documento: {nome_arquivo}")
            
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read()
                
            # Extrai o link que o Ingestor salvou na primeira linha
            link = "Sem Link"
            match_link = re.search(r'LINK:\s*(.+)', conteudo)
            if match_link:
                link = match_link.group(1).strip()
            
            print("🧠 Consultando o cérebro (Gemini)...")
            resposta = avaliar_com_gemini(conteudo)
            print(resposta + "\n")
            
            # Tratamento da resposta
            fit, score, motivo = "NÃO", "0", resposta
            match_fit = re.search(r'FIT:\s*(SIM|NÃO|ERRO)', resposta, re.IGNORECASE)
            match_score = re.search(r'SCORE:\s*(\d+)', resposta, re.IGNORECASE)
            match_motivo = re.search(r'MOTIVO:\s*(.+)', resposta, re.IGNORECASE | re.DOTALL)
            
            if match_fit: fit = match_fit.group(1).upper()
            if match_score: score = match_score.group(1)
            if match_motivo: motivo = match_motivo.group(1).strip()
            
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            writer.writerow([data_hoje, score, fit, motivo, link, "[ ] Pendente"])
            
            # Move a vaga processada para a pasta de arquivos para não avaliar duas vezes
            shutil.move(caminho_arquivo, os.path.join(pasta_arquivados, nome_arquivo))
            
            # Respeita o limite da API (apenas se houver mais de uma vaga)
            if i < len(arquivos) - 1:
                print("⏳ Pausa de segurança de 10s...")
                time.sleep(10)

    print(f"✅ Processamento concluído! Planilha atualizada em: {caminho_planilha}")

if __name__ == "__main__":
    processar_caixa_de_entrada()