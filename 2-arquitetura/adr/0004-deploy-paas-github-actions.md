# ADR 0004: automatizar deploy via PaaS e GitHub Actions

**Status:** aceito

**Contexto:** Com 6 desenvolvedores e nenhuma equipe de operações (DevOps), o processo de build, testes e deploy para a nuvem pública precisa ser 100% automatizado e de baixo atrito.

**Decisão:** Utilizar plataforma PaaS gerenciada (ex: Render / Heroku / AWS App Runner / Vercel para frontend e Cloud Run para backend) integrada com GitHub Actions para pipeline de CI/CD contínuo. A observabilidade será feita via logs centralizados na nuvem e ferramentas nativas de monitoramento de erro de baixo custo.

**Alternativas consideradas:**
- Gerenciamento manual de servidores (VPS / EC2 crua): descartado pelo risco operacional e tempo gasto pela equipe configurando Linux e segurança.
- Kubernetes: descartado por completo devido à complexidade desproporcional para o tamanho do time e escopo do projeto.

**Consequências:**
- **Positivas:** deploy automatizado a cada merge na branch principal, zerando o tempo da equipe com infraestrutura manual.
- **Negativas:** dependência do provedor de nuvem escolhido (vendor lock-in moderado).
