# LinkedIn AI Job Matcher 🎯

Pipeline de "Recrutamento Reverso" impulsionado por Inteligência Artificial. Este sistema coleta, padroniza e avalia automaticamente vagas de emprego, cruzando os requisitos da posição com o perfil do candidato através de análise semântica estruturada e um sistema de pontuação (Score 0-100).

## 🛠️ Arquitetura Desacoplada (Agentic Workflow)

O sistema utiliza uma arquitetura modular baseada no conceito de "Caixa de Entrada". A extração web é totalmente separada da avaliação da IA, o que garante imunidade a bloqueios do LinkedIn, economia de requisições de API e permite uma atuação *Omnichannel* (vagas de qualquer site).

O fluxo é dividido nestes módulos principais:

*   **`coletor_linkedin.py`**: Automação web (Playwright) que varre as buscas do LinkedIn e captura apenas as URLs das vagas (driblando o Virtual DOM e Lazy Loading), criando uma lista de alvos.
*   **`extrator_linkedin.py`**: Consome a lista de URLs, abre página por página, extrai o texto bruto da descrição e salva os documentos em uma pasta local (`caixa_de_entrada`).
*   **`ingestor_manual.py`**: Interface de linha de comando (CLI) que permite colar textos de vagas encontradas em outras plataformas (Gupy, Glassdoor, indicação) diretamente na `caixa_de_entrada`.
*   **`avaliador_vagas_pro.py`**: O "Cérebro" da operação (Google Gemini). Lê cegamente todos os arquivos de texto acumulados na `caixa_de_entrada`, aplica um *Mega-Prompt* com regras de negócio rigorosas de carreira, gera o veredito e exporta os resultados para um *dashboard* em `planilha_gestao_vagas.csv`, movendo os arquivos lidos para arquivamento.
*   **`renovar_login.py`**: Script utilitário para gerenciamento seguro da sessão persistente do navegador.

## ⚙️ Pré-requisitos e Configuração

O projeto requer a configuração prévia de um arquivo `.env` para segurança das credenciais e a instalação das bibliotecas base.

1. Instale as dependências:
   ```bash
   pip install playwright google-generativeai python-dotenv
   playwright install```

   Crie um arquivo .env na raiz do projeto com a sua chave:

Snippet de código
GEMINI_API_KEY=sua_chave_de_api_aqui
(Nota: O arquivo .env e a pasta local de dados são protegidos via .gitignore).

## Como Executar o Pipeline (Fluxo Diário)
O pipeline opera de forma sequencial. Abra o terminal e execute:

Fase 1: Alimentar a Caixa de Entrada

Buscar links: python coletor_linkedin.py

Extrair textos do LinkedIn: python extrator_linkedin.py

(Opcional) Inserir vaga externa manualmente: python ingestor_manual.py

Fase 2: Curadoria de IA
4. Avaliar fila de espera: python avaliador_vagas_pro.py

## Gestão de Resultados
O avaliador consolida as aprovações e reprovações no arquivo dados_vagas/planilha_gestao_vagas.csv no formato:
Data | Score (0-100) | Fit (SIM/NÃO) | Motivo da Decisão | Link | Status de Aplicação