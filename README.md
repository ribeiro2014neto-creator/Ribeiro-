# Campo — Gestão de pecuária
Aplicativo local para TIP e semiconfinamento. Python 3.12+. Execução local com SQLite não requer dependências externas; PostgreSQL usa requirements.txt.

```sh
cd /workspace/Ribeiro-
python server.py
```

Servidor na porta 8000 (configurável por `PORT`). Os dados ficam em `dados.sqlite3`; faça cópias desse arquivo com o servidor parado. `PECUARIA_DB` permite escolher outro caminho.

Cadastre um lote com peso médio de entrada, registre os tratos em kg e as pesagens em kg por cabeça. Nos abates, registre quantidade, peso vivo total na fazenda e peso total de carcaça do mesmo grupo. Abates parciais são suportados.

GMD = (peso médio final − peso médio de entrada) / dias. Após abates, o indicador usa os grupos abatidos e é ponderado por cabeças. Antes de abates, usa a última pesagem. Rendimento = carcaça / peso vivo de saída × 100. Não é rendimento medido sobre peso vivo no frigorífico. A média geral de rendimento é ponderada pelo peso vivo.

Primeira versão para uso local, sem autenticação ou controle multiusuário. Não exponha o servidor à internet com dados reais. Não estima GMD a partir de ração. A ração exibida é fornecida, sem desconto de sobras. Pesagens de lote após abate parcial não são aceitas nesta versão. Datas futuras não são excluídas dos totais. Mudanças de composição, transferências e mortalidade não são contempladas.

Validação: `python -m unittest discover -s tests -v`.

## Publicação gratuita para testes
Use um Web Service Free do Render e um projeto Free no Neon (PostgreSQL), sujeitos aos limites e condições vigentes dos provedores. O render.yaml não contrata disco nem plano pago. O serviço pode dormir e demorar no primeiro acesso.

1. Crie um projeto gratuito em neon.tech. Em Connect, copie a connection string PostgreSQL com SSL exigido (sslmode=require ou mais estrito); não publique nem envie essa credencial pelo chat.
2. No Render, New > Blueprint, selecione o repositório e main. Se a tela exigir contratação ou método de pagamento, pare e use New > Web Service com o plano Free.
3. Defina DATABASE_URL com a conexão do Neon e APP_PASSWORD com uma senha forte, no painel seguro do Render. APP_USER é fazenda. Confira plano Free e ausência de disco antes de criar.
4. Para criação manual: Python, build `pip install -r requirements.txt`, start `python server.py`, health check `/health`, as mesmas variáveis.
5. Aguarde o deploy e abra a URL HTTPS. O navegador solicitará usuário e senha.

O app cria as tabelas no banco vazio ao iniciar. No Render, recusa iniciar sem banco externo e senha. SQLite continua disponível para execução local; os dados locais existentes não são migrados automaticamente para o Neon.

A proteção é HTTP Basic via HTTPS, sem cadastro de usuários ou recuperação de senha. `/health` é público e não retorna dados da fazenda. Faça backups do banco. Esta configuração não foi publicada nem validada com uma conta Neon real até que a conexão seja cadastrada pelo usuário.
