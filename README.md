# Campo — Gestão de pecuária
Aplicativo local para TIP e semiconfinamento. Python 3.12+, sem dependências externas.

```sh
cd /workspace/Ribeiro-
python server.py
```

Servidor na porta 8000 (configurável por `PORT`). Os dados ficam em `dados.sqlite3`; faça cópias desse arquivo com o servidor parado. `PECUARIA_DB` permite escolher outro caminho.

Cadastre um lote com peso médio de entrada, registre os tratos em kg e as pesagens em kg por cabeça. Nos abates, registre quantidade, peso vivo total na fazenda e peso total de carcaça do mesmo grupo. Abates parciais são suportados.

GMD = (peso médio final − peso médio de entrada) / dias. Após abates, o indicador usa os grupos abatidos e é ponderado por cabeças. Antes de abates, usa a última pesagem. Rendimento = carcaça / peso vivo de saída × 100. Não é rendimento medido sobre peso vivo no frigorífico. A média geral de rendimento é ponderada pelo peso vivo.

Primeira versão para uso local, sem autenticação ou controle multiusuário. Não exponha o servidor à internet com dados reais. Não estima GMD a partir de ração. A ração exibida é fornecida, sem desconto de sobras. Pesagens de lote após abate parcial não são aceitas nesta versão. Datas futuras não são excluídas dos totais. Mudanças de composição, transferências e mortalidade não são contempladas.

Validação: `python -m unittest discover -s tests -v`.

## Publicação no Render
No Render, use New > Blueprint e selecione este repositório. O render.yaml configura servidor e disco persistente; o plano Starter e o disco têm cobrança, apresentada pelo Render antes da criação. Defina APP_PASSWORD no painel seguro; o usuário inicial é `fazenda`. O navegador pedirá usuário e senha ao abrir o endereço HTTPS. Nenhuma senha deve ser enviada ao GitHub ou pelo chat. Para configurar manualmente: runtime Python, build `python -m compileall -q server.py`, start `python server.py`, health check `/health`, disco em `/var/data`, variável PECUARIA_DB=/var/data/pecuaria.sqlite3.

A proteção de acesso é HTTP Basic via HTTPS (sem cadastro de usuários ou recuperação de senha). APP_PASSWORD ausente mantém o modo local sem autenticação. `/health` é público e não retorna dados da fazenda. O banco continua precisando de backups.
