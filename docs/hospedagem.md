# Hospedagem do dashboard

O dashboard precisa de um servidor Python: GitHub Pages não executa Streamlit.
O túnel temporário usado na revisão depende do computador local e não é a publicação definitiva.

## Streamlit Community Cloud

Em https://share.streamlit.io/, entre com a conta GitHub e crie um app com:

- Repositório: `Ceistutis/Guardi-o-H-drico`
- Branch: `feat/reformulacao-dashboard`
- Arquivo principal: `app/main.py`
- Python: `3.12` (configuração da hospedagem; testes locais executados em 3.14)
- Dependências: `app/requirements.txt`, detectadas junto ao arquivo principal
- Visibilidade: pública, para permitir o teste pelo grupo

Não são necessários secrets, banco de dados ou credenciais de hardware.
A configuração visual é lida de `.streamlit/config.toml` na raiz.
O endereço definitivo só deve ser divulgado após a conclusão e validação do deploy.

Cada conexão mantém sua própria simulação. Recarregar ou reiniciar o servidor pode
reiniciar a sessão; os dados não são persistidos. O histórico é ilustrativo.

O serviço gratuito pode suspender apps após 12 horas sem tráfego. O link permanece,
mas pode ser necessário reativar o app ao acessar. Abra-o antes da apresentação e
confira visão geral, cenário de vazamento, válvula, histórico e download do CSV.
Disponibilidade contínua sem suspensão exige um plano de hospedagem adequado;
não há garantia de disponibilidade ininterrupta no Community Cloud.

Documentação oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
e https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app.
