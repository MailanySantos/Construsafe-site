
# Projeto Construsafe

## Visão Geral
Sistema web desenvolvido para auxiliar a gestão de Segurança do Trabalho na construção civil. Inclui registro e análise de ocorrências, entrega de EPIs, e painel administrativo com níveis de acesso.

## Tecnologias Utilizadas
- Python + Flask (backend)
- SQLite (banco de dados)
- HTML/CSS/Bootstrap (frontend)
- Chart.js (gráficos)
- FPDF / Pandas (exportação PDF/Excel)

## Funcionalidades
- Cadastro/login com níveis de acesso (admin, funcionário)
- Registro de ocorrências e EPIs entregues
- Dashboard com gráficos por tipo de ocorrência
- Exportação de relatórios (PDF e Excel)
- Painel administrativo com filtros
- Sistema pronto para hospedagem online

## Como Executar Localmente
1. Instale os requisitos: `pip install flask pandas fpdf openpyxl`
2. Execute: `python app.py`
3. Acesse: `http://localhost:5000`

## Para Hospedar Online
- Use plataformas como [Render](https://render.com) ou [Railway](https://railway.app)
- Adicione um arquivo `requirements.txt` e `Procfile` como exemplo na pasta `deploy/`

## Acesso Inicial
- Usuário: admin  
- Senha: admin  
- Papel: admin

## Estrutura do Projeto
- `/app`: código-fonte do sistema
- `/docs`: documentação técnica
- `/deploy`: arquivos para subir online

---
Sistema desenvolvido como projeto integrador de Segurança do Trabalho - 2025.
