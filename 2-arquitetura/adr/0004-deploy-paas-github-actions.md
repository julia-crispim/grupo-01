# ADR 0004: automatizar deploy via Cloud Run e GitHub Actions

**Status:** aceito

**Contexto:** Com 6 desenvolvedores e nenhuma equipe de operações (DevOps), o processo de build, testes e deploy para a nuvem pública precisa ser automatizado e de baixo atrito.

**Decisão:** Utilizar **Cloud Run** como plataforma PaaS gerenciada para o backend, integrada ao GitHub Actions para o pipeline de CI/CD contínuo. A observabilidade será feita via logs centralizados e ferramentas nativas de monitoramento de erro de baixo custo.

**Alternativas consideradas:**
- Render / Heroku / AWS App Runner: consideradas como alternativas de PaaS gerenciada, mas não adotadas nesta decisão.
- Gerenciamento manual de servidores (VPS / EC2 crua): descartado pelo risco operacional e tempo gasto pela equipe configurando Linux e segurança.
- Kubernetes: descartado por completo devido à complexidade desproporcional para o tamanho do time e escopo do projeto.

**Consequências:**
- **Positivas:** deploy automatizado a cada merge na branch principal, reduzindo a necessidade de operação manual de infraestrutura.
- **Negativas:** dependência do provedor de nuvem escolhido (vendor lock-in moderado).
