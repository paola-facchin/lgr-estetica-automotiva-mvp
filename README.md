# LGR Estética Automotiva — MVP de Gestão

Projeto acadêmico de Software — Experiência Prática III.

## Objetivo

Aplicação web para a **LGR Estética Automotiva**, com cadastro de clientes e veículos, registro de serviços, **consulta de histórico pela placa** e controle básico de receitas e despesas. Projeto construído com **Python 3.12, Django 5.2 LTS e PostgreSQL 16** como banco planejado para hospedagem. O desenvolvimento local e a integração contínua podem utilizar SQLite.

## Funcionalidades implementadas neste código inicial

- Login e logout de usuários cadastrados pelo administrador.
- Cadastro de clientes, veículos e serviços, com validação de placa brasileira.
- Pesquisa pela placa, exibindo os serviços do veículo (RF04).
- Cadastro e resumo de movimentações financeiras, com permissões separadas.
- Templates responsivos com rótulos, foco visível e mensagens textuais.
- Testes automatizados e pipeline GitHub Actions.

**Limitações deste código inicial:** ainda requer validação com o proprietário, configuração de hospedagem, testes reais de usabilidade/performance, política de backup e controles adicionais contra tentativas repetidas de login. O CI executa com SQLite; é necessário testar também a implantação com PostgreSQL. Não utilizar com dados reais de clientes sem executar essas etapas.

## Como executar localmente

Requer Python 3.12 (ou versão compatível com o Django selecionado).

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
```

Defina as variáveis de ambiente necessárias. Para um teste local, por exemplo:

**Windows PowerShell:**
```powershell
$env:DJANGO_DEBUG='true'
```

**Linux/macOS:**
```bash
export DJANGO_DEBUG=true
```

Então execute:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` e faça login com o usuário criado. Os dados de demonstração devem ser fictícios. **Não inclua credenciais no README ou em commits.**

## Perfil financeiro

O Django dispõe de permissões individuais (`core.view_movimentacaofinanceira` e `core.add_movimentacaofinanceira`). Para concedê-las ao proprietário, acesse `/admin/`, abra o usuário correspondente e atribua essas duas permissões. Colaboradores sem elas receberão HTTP 403 nas rotas financeiras.

## Banco PostgreSQL

Ao configurar `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` e `POSTGRES_SSLMODE` no ambiente, o Django utiliza PostgreSQL. Sem `POSTGRES_DB`, utiliza SQLite local para desenvolvimento. Nunca publique as variáveis secretas. Em produção, configure HTTPS corretamente, use `DJANGO_DEBUG=false`, `DJANGO_SECRET_KEY` forte e `DJANGO_ALLOWED_HOSTS`. Rode `python manage.py check --deploy` e configure backup/recovery antes de colocar dados reais.

## Testes automatizados

```bash
python manage.py test -v 2
```

Os testes verificam: validação e unicidade de placa, necessidade de login, separação de históricos por veículo, placa inexistente, restrição financeira, saldo financeiro e proteção CSRF.

## Integração contínua

Workflow `.github/workflows/ci.yml`: executa `manage.py check` e `manage.py test` automaticamente em cada `push` e `pull_request` no GitHub. A evidência da execução poderá ser obtida na aba **Actions** do repositório após publicação.

## Versionamento recomendado

Use commits descritivos: `feat: cadastro de veículos`, `test: cobertura da consulta por placa`, `fix: validação do formato da placa`. Abra uma branch para cada alteração e uma Pull Request para revisar o próprio código, mantendo registro de validação. Não afirme que houve PR, CI ou validação externa antes de executar essas atividades.

## Requisitos

RF01 Cliente; RF02 Veículo; RF03 Serviço; RF04 Consulta por placa; RF05 Movimentação financeira; RF06 Resumo por período. RF07 (exportar PDF) fica fora do MVP.

## ODS

ODS 9 — Indústria, Inovação e Infraestrutura, contribuição local indireta para digitalização de uma pequena empresa.

## Privacidade

O repositório deve ser **público apenas para o código e dados fictícios**. Nunca commitar banco de produção, senhas, CPF, endereços, fotos de clientes ou credenciais reais.

## Protótipos da Experiência Prática II

Capturas com dados fictícios: [Tela 1 — menu](docs/prototipo/Tela_1_Menu_Inicial.png), [Tela 2 — consulta](docs/prototipo/Tela_2_Consulta_Placa.png) e [Tela 3 — histórico](docs/prototipo/Tela_3_Historico_Resultados.png). São evidências de planejamento visual, não comprovam funcionamento ou validação externa.
