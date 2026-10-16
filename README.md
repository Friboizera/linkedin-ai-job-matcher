# LinkedIn AI Job Matcher 🎯

Pipeline de recrutamento reverso para coleta e avaliação automática de vagas no LinkedIn.

## 🛠️ Arquitetura do Projeto
O sistema é dividido em scripts modulares:
- `renovar_login.py` e `ingestor_manual.py`: Gerenciamento seguro de sessão e ingestão de dados.
- `coletor_linkedin.py`: Automação web rodando com Playwright para varredura e extração inteligente das oportunidades.
- `avaliador_vagas_pro.py`: Orquestração com a API do Gemini para analisar o *stack* técnico e classificar as vagas com base no meu perfil profissional.

## 🚀 Execução
O projeto requer a configuração prévia de um arquivo `.env` com as chaves de API necessárias e a instalação das dependências. Os scripts de coleta e avaliação operam de forma independente, permitindo ajustes rápidos no modelo de avaliação.