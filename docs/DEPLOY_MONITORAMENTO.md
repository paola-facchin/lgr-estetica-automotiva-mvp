# Publicação no Render e monitoramento (Experiência Prática IV)

## Aviso: ambiente acadêmico, somente dados fictícios
A opção gratuita do Render é uma demonstração, não é infraestrutura adequada para
dados reais de clientes. Os serviços gratuitos podem hibernar após 15 minutos de
inatividade e o PostgreSQL gratuito expira em 30 dias, sem backups automáticos.
Para a LGR utilizar o sistema comercialmente, contratar banco persistente com
backups, configurar recuperação de desastres, política de acesso, privacidade e
monitoramento adequado.

## Antes de começar
1. Integrar à branch `main` a Pull Request de melhorias visuais e deploy,
   somente depois de verificar os testes em GitHub Actions.
2. Entrar na sua conta em https://dashboard.render.com e conectar o GitHub.
3. NUNCA colocar senha, dados de clientes ou chave secreta no repositório ou
   no texto do DreamShaper.

## Deploy pela configuração pronta (`render.yaml`)
1. No Render Dashboard, escolha **New > Blueprint** (ou **New Blueprint Instance**).
2. Escolha o repositório `paola-facchin/lgr-estetica-automotiva-mvp`
   na branch `main`.
3. Render reconhecerá `render.yaml` com um Web Service Django e um PostgreSQL 16.
   Confirme se o plano escolhido é `Free` (ambiente de demonstração).
4. Quando o Render solicitar `DJANGO_SUPERUSER_USERNAME` e
   `DJANGO_SUPERUSER_PASSWORD`, crie seu usuário e uma senha exclusiva
   e forte, com ao menos 12 caracteres. **Não compartilhe a senha no chat**.
   O Render gerará automaticamente a `DJANGO_SECRET_KEY` e a conexão
   `DATABASE_URL` do banco.
5. Clique em **Apply / Deploy**. A primeira compilação instala os pacotes
   Python, reúne os arquivos CSS (`collectstatic`), executa migrações e cria
   uma única conta inicial de administrador. Em deploys futuros a conta
   existente é preservada sem alterar a senha.
6. Quando o Render indicar **Live**, abra o endereço HTTPS que ele EXIBIR no
   painel (`https://...onrender.com`). **Não invente URL por antecipação**.
7. Abra `<URL_REAL>/health/`: com banco operacional, o sistema responde
   `{"status": "ok"}` e HTTP 200. Acesse também `<URL_REAL>/contas/login/`,
   faça login com a sua conta e confirme que o painel e estilos carregaram.
   Use apenas dados fictícios na demonstração.
8. Capture um print do NAVEGADOR INTEIRO com barra de endereços visível,
   URL HTTPS e tela do painel inicial do Django autenticado (não apenas o
   painel da nuvem ou GitHub Actions).

## Monitoramento automatizado com GitHub Actions
O repositório inclui `.github/workflows/monitoramento.yml`:
- Verifica aproximadamente a cada hora `GET /health/` na URL pública.
- A aplicação consulta o banco com `SELECT 1` e responde 200 apenas se
  servidor e banco estão disponíveis.
- Se houver indisponibilidade, erro de rede, HTTP != 200 ou falta do
  corpo `{"status": "ok"}`, o job falha (ícone vermelho) e registra erro.
- Os históricos verde/vermelho ficam em **GitHub > Actions > Monitoramento**.
  As notificações de falha dependem das preferências de notificações do GitHub
  da conta; não considere envio de e-mail configurado sem verificar.

**Ativação obrigatória após conseguir a URL pública real:**
1. GitHub > repositório > Settings > Secrets and variables > Actions > Variables.
2. Clique **New repository variable**:
   - Name: `LGR_PUBLIC_URL`
   - Value: a URL HTTPS REAL do Render, sem barra final.
3. GitHub > **Actions** > **Monitoramento - LGR online** > **Run workflow**.
4. Abra a execução e confira se aparece `UP: HTTP 200 e banco operacional.`
5. Faça print mostrando o run com status verde e o passo de verificação.
   Se ficar vermelho, abra os logs, corrija a falha e rode novamente.
6. Monitore as próximas execuções e acompanhe **Logs** e **Events** no Render.

## Evidências para o DreamShaper
- **URL pública:** somente a URL verificada no Render depois de publicada.
- **Infraestrutura:** Django + Gunicorn + WhiteNoise + PostgreSQL no Render,
  com segredos em variáveis de ambiente, migrações e health check.
- **Print do deploy:** navegador inteiro com a URL HTTPS e a interface real.
- **Monitoramento:** GitHub Actions agendado + `/health/` e painel Logs do Render.
- **Print do monitoramento:** execução verde do workflow configurado com a
  variável `LGR_PUBLIC_URL`, comprovando a checagem real da URL publicada.

## Limites operacionais
O serviço gratuito pode ficar inativo e demorar a responder no primeiro acesso,
mesmo sem erro de aplicação. O `curl` do monitoramento possui timeout estendido
para acomodar a inicialização. O plano gratuito não é garantia de disponibilidade
24/7; não invente índices de uptime. O banco gratuito pode expirar e perder dados:
não use com informações verdadeiras de clientes ou da empresa.
