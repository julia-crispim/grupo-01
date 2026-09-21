# ADR 0002: armazenar dados em banco relacional (PostgreSQL)

**Status:** aceito

**Contexto:** O prontuário clínico é um dado altamente sensível sob a LGPD, exige retenção legal de 20 anos e auditoria completa de quem acessou ou alterou cada registro.

**Decisão:** Utilizar um Banco de Dados Relacional Gerenciado (PostgreSQL na nuvem) com esquemas lógicos separados por módulo. A tabela de prontuários contará com colunas de trilha de auditoria imutáveis (criado_por, alterado_por, timestamp) e rotinas programadas de anonimização para atender aos pedidos legítimos de exclusão da LGPD, ressalvada a retenção legal obrigatória de 20 anos.

**Alternativas consideradas:**
- Event Sourcing (Cap. 15): descartado pelo custo inicial elevado de desenvolvimento e complexidade de versionamento de esquemas em um projeto de 6 meses.
- Bancos NoSQL: descartados por dificultar a garantia de consistência transacional forte exigida na dispensação de farmácia e regulação de leitos.

**Consequências:**
- **Positivas:** garantia de consistência ACID onde o negócio exige, facilidade de relatórios e trilhas de auditoria nativas por banco relacional.
- **Negativas:** escalabilidade do banco é vertical; consultas analíticas pesadas podem concorrer com o transacional (mitigado pelo CQRS pontual).
