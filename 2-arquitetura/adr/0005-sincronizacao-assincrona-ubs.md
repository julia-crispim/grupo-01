# ADR 0005: sincronizar dados assincronamente (Event-Driven) nas UBSs

**Status:** aceito (decisão de risco crítico a ser validada)

**Contexto:** As UBSs possuem internet extremamente instável, com quedas diárias. O atendimento e a triagem não podem parar, e os dados locais precisam sincronizar com o servidor central sem perder nem duplicar registros quando a rede voltar.

**Decisão:** Implementar uma estratégia de Mensageria Assíncrona Local baseada em Fila (Event-Driven / Worker local). A aplicação na UBS mantém um banco de dados local (ex: SQLite embarcado) operando offline de forma transparente. Um worker em segundo plano monitora a conectividade e utiliza filas com retransmissão independente para enviar os eventos ao servidor central assim que a conexão é restabelecida.

**Alternativas consideradas:**
- Sistema estritamente online: descartado, inviabilizaria o uso nas UBSs devido às quedas de internet.
- Replicação bidirecional de banco de dados corporativo: descartada pela complexidade de resolução de conflitos de concorrência em tempo real para 6 desenvolvedores.

**Consequências:**
- **Positivas:** garante autonomia operacional total para as UBSs mesmo durante blecautes de internet.
- **Negativas:** introduz a complexidade de consistência eventual e tratamento de conflitos de sincronização na camada de código.
