# Mapa de Restrições e Decisões

| Restrição (Envelope) / Requisito (Caso) | Decisão Arquitetural Adotada | Justificativa / Como a Decisão Atende ao Ponto |
|---|---|---|
| Envelope A: Equipe pequena (apenas 6 desenvolvedores) e totalmente sem equipe de operações/DevOps dedicada. | Monolito Modular (Núcleo da Aplicação) | Elimina a sobrecarga operacional de gerenciar infraestrutura distribuída (microsserviços). Garante produtividade com um único deploy, mas mantém o código organizado por domínios. |
| Envelope A + Caso: Orçamento apertado para 6 meses em nuvem pública (paga por uso) + Necessidade de suportar picos de campanhas de vacinação. | Arquitetura Serverless (AWS Lambda / Cloud Functions) | Permite absorver os picos da vacinação com escala sob demanda e reduzir o custo de infraestrutura ociosa, mantendo o uso restrito ao cenário de carga intermitente previsto para as campanhas. |
| Caso: Obrigatoriedade de integrar e conviver com o sistema legado instável da Central de Regulação de Leitos. | Arquitetura Hexagonal (Portas e Adaptadores / Camada Anticorrupção) | Cria uma blindagem ao redor do núcleo. Se o legado governamental cair, mudar de contrato ou ficar lento, a regra de negócio do município continua intacta e isolada. |
| Caso: Quedas de internet constantes nas UBSs, porém o atendimento médico não pode parar de forma alguma. | Padrão Orientado a Eventos (Message Broker) + PWA | O app (PWA) funciona offline. Quando a internet volta, as filas de mensagens (RabbitMQ/SQS) garantem que os dados do atendimento cheguem ao servidor central de forma assíncrona e resiliente, com processamento idempotente para evitar duplicidades. |
| Caso: Exigência legal de manter os prontuários dos pacientes salvos de forma íntegra e segura por 20 anos. | Banco de Dados Relacional (PostgreSQL) | Garante consistência transacional forte (ACID) para não misturar remédios ou prontuários, oferecendo uma tecnologia madura e estável para retenção segura de dados em longo prazo. |


## Respostas às cinco perguntas obrigatórias do caso

### 1. Como a UPA continua triando e atendendo com a internet fora do ar, e o que acontece quando ela volta?

A aplicação utilizada na UBS/UPA funciona em modo offline-first, mantendo os dados do atendimento em armazenamento local. Quando a conexão é restabelecida, um worker envia os eventos acumulados para o servidor central por meio de uma fila assíncrona, permitindo a sincronização sem interromper o atendimento. O processamento utiliza identificador único dos eventos e idempotência para evitar duplicações.

**Sustentação:** ADR 0005 — Sincronização assíncrona nas UBSs; C4 de Contêineres — comunicação assíncrona e Message Broker; C4 de Componentes — módulos e persistência.

### 2. Como duas unidades disputando o mesmo leito nunca conseguem reservá-lo ao mesmo tempo, com o sistema legado ainda no circuito?

A reserva de leitos permanece sob controle transacional do núcleo da aplicação, utilizando o banco relacional para garantir consistência forte na operação. A integração com o sistema legado é isolada por portas e adaptadores, evitando que a instabilidade do legado contamine a regra de negócio da reserva. Assim, a operação de reserva deve ser confirmada dentro da transação do módulo de regulação, garantindo que a mesma reserva não seja confirmada simultaneamente para dois pacientes.

**Sustentação:** ADR 0002 — Banco Relacional PostgreSQL; ADR 0003 — Integração com o sistema legado; C4 de Componentes — módulo de integração e banco relacional.

### 3. Como o prontuário garante que se saiba quem acessou cada registro, e como convive a guarda de 20 anos com os direitos do paciente sob a LGPD?

O prontuário é armazenado em banco relacional, com informações de auditoria que registram quem criou ou alterou cada registro e em qual momento. A solução mantém a retenção obrigatória de 20 anos e aplica controles de acesso e tratamento de dados conforme as necessidades de privacidade do caso, evitando eliminar registros cuja retenção legal seja obrigatória.

**Sustentação:** ADR 0002 — Banco Relacional PostgreSQL; C4 de Componentes — módulo de prontuário e banco de dados.

### 4. Como a notificação compulsória chega à vigilância em até 24 horas mesmo se o sistema federal estiver indisponível?

A comunicação com sistemas externos utiliza processamento assíncrono, permitindo que a notificação seja colocada em uma fila enquanto o sistema federal estiver indisponível. Quando a comunicação for restabelecida, o consumidor processa os eventos pendentes, evitando que a indisponibilidade externa interrompa o fluxo interno. Dessa forma, as notificações podem continuar sendo processadas mesmo durante a indisponibilidade temporária do sistema federal.

**Sustentação:** ADR 0005 — Sincronização assíncrona; ADR 0003 — Integração com sistemas externos; C4 de Contêineres — Message Broker; C4 de Contexto — Sistemas Federais de Saúde.

### 5. Como o sistema legado de regulação é substituído aos poucos sem interromper o serviço?

O sistema novo não acessa diretamente as estruturas do legado. A integração é isolada por uma porta de negócio e por adaptadores específicos, permitindo alterar ou substituir a tecnologia do legado sem modificar o núcleo da aplicação. Dessa forma, a migração pode ocorrer gradualmente enquanto o sistema legado permanece ativo durante o período de transição.

**Sustentação:** ADR 0003 — Integração com o sistema legado via Portas e Adaptadores; C4 de Componentes — módulo de integração com o legado.
