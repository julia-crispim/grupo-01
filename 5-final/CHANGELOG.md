# Changelog — Entrega Final

## Revisão após a leitura cruzada com o Grupo 10

Este changelog registra as alterações realizadas no repositório após a análise das objeções recebidas do Grupo 10.

### 1. Agendamento — Serverless

**Objeção:** foi apontada complexidade desnecessária na utilização de Serverless exclusivamente para o Agendamento, considerando as restrições do Envelope A.

**Alteração:** o Agendamento permanece dentro do Monolito Modular e utiliza o autoscaling da plataforma PaaS.

**Motivo:** reduzimos a complexidade operacional e o número de componentes que precisam ser desenvolvidos e monitorados por uma equipe de apenas 6 desenvolvedores.

**ADR relacionado:** o ADR 0001 foi substituído pelo ADR 0006.

---

### 2. Auditoria do prontuário

**Objeção:** os campos `criado_por`, `alterado_por` e `timestamp` não seriam suficientes para manter o histórico completo das alterações.

**Alteração:** a documentação foi complementada para prever uma trilha de auditoria separada, registrando as alterações relevantes, o usuário responsável e a data/hora da operação.

**Motivo:** melhorar a rastreabilidade dos dados sensíveis sem introduzir Event Sourcing em toda a aplicação.

---

### 3. Sincronização offline das UBSs

**Objeção:** a utilização de RabbitMQ/SQS e workers poderia transferir complexidade operacional para as UBSs.

**Alteração:** foi esclarecido que não haverá um broker de mensageria completo instalado nas UBSs. A aplicação mantém localmente as operações pendentes e realiza a sincronização quando a conexão retorna.

A mensageria permanece centralizada no backend.

**Motivo:** manter o funcionamento offline sem criar uma infraestrutura de operação distribuída nas unidades.

---

### 4. Integração com o sistema legado

**Objeção:** a Arquitetura Hexagonal e a ACL reduzem o acoplamento do código, mas não resolvem sozinhas a indisponibilidade do sistema legado.

**Alteração:** a integração foi complementada com mecanismos de resiliência, incluindo processamento assíncrono e retentativas quando aplicável.

Para operações que exigem confirmação do legado, a operação não será considerada definitivamente concluída antes da confirmação necessária.

**Motivo:** separar a proteção estrutural contra acoplamento da proteção contra falhas de comunicação e indisponibilidade.

A reserva de leito continua exigindo consistência forte.

---

### 5. Vigilância epidemiológica

**Objeção:** o processamento individual das notificações poderia aumentar o número de chamadas externas e o custo de comunicação com sistemas federais.

**Alteração:** foi acrescentada a possibilidade de processamento em lote das notificações pendentes quando aplicável.

As notificações continuam sendo registradas de forma persistente e processadas de forma assíncrona. Em caso de indisponibilidade do sistema federal, permanecem pendentes para novas tentativas.

**Motivo:** reduzir chamadas externas e melhorar a eficiência sem comprometer o requisito de processamento dentro de 24 horas.

---

## Resumo das alterações

Após a leitura cruzada, a arquitetura final passou a considerar:

- Monolito Modular como núcleo principal;
- Agendamento dentro do Monolito Modular;
- autoscaling da plataforma PaaS para os picos de demanda;
- PostgreSQL como banco relacional principal;
- trilha de auditoria para dados sensíveis;
- Arquitetura Hexagonal + ACL para integração com o legado;
- mecanismos de processamento assíncrono e retentativas;
- funcionamento offline nas UBSs com armazenamento local e sincronização posterior;
- processamento idempotente dos eventos;
- processamento em lote para notificações epidemiológicas quando aplicável;
- fila e retentativas para evitar perda de notificações durante indisponibilidades externas.

As alterações buscam manter a arquitetura compatível com as restrições do Envelope A, especialmente equipe pequena, ausência de equipe dedicada de operações, orçamento limitado, necessidade de entrega rápida e conectividade instável nas UBSs.
