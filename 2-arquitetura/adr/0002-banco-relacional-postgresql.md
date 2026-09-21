# ADR 0002: armazenar dados em banco relacional (PostgreSQL)

**Status:** aceito

**Contexto:** O prontuário clínico é um dado altamente sensível sob a LGPD, exige retenção legal de 20 anos e auditoria completa de quem acessou ou alterou cada registro.

**Decisão:** Utilizar um Banco de Dados Relacional Gerenciado (PostgreSQL na nuvem) com esquemas lógicos separados por módulo. A tabela de prontuários contará com colunas de trilha de auditoria (criado_por, alterado_por, timestamp) para registrar quem acessou ou alterou cada registro. O desenho preserva a retenção legal de 20 anos e os controles de acesso aos dados, em conformidade com os requisitos do caso.

**Alternativas consideradas:**
- Event Sourcing (Cap. 15): descartado pelo custo inicial elevado de desenvolvimento e complexidade de versionamento de esquemas em um projeto de 6 meses.
- Bancos NoSQL: descartados por dificultar a garantia de consistência transacional forte exigida na dispensação de farmácia e regulação de leitos.

**Consequências:**
- **Positivas:** garantia de consistência ACID onde o negócio exige, facilidade de relatórios e de implementação de trilhas de auditoria.
- **Negativas:** escalabilidade do banco é vertical; consultas analíticas pesadas podem concorrer com o transacional (mitigado pelo CQRS pontual).
