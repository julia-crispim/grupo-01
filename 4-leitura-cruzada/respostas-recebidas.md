# Respostas às objeções recebidas — Grupo 10

## 1. Complexidade desnecessária com funções Serverless avulsas

### Objeção recebida

O Grupo 10 questiona a utilização de Serverless no ADR 0001 exclusivamente para o agendamento de campanhas. Segundo a objeção, considerando o Envelope A, com apenas 6 desenvolvedores, nenhuma equipe de operações e orçamento limitado, a utilização de dois modelos arquiteturais poderia aumentar a complexidade de CI/CD, monitoramento e roteamento.

O grupo também argumenta que o Cloud Run já possui escalabilidade automática e poderia absorver os picos das campanhas sem a necessidade de separar o agendamento em Functions.

### Nossa resposta

**Aceitamos parcialmente a objeção.**

A crítica é válida em relação ao custo de manter um modelo Serverless separado apenas para o agendamento. Como o Cloud Run já oferece escalabilidade automática, não é necessário introduzir uma segunda infraestrutura somente para atender aos picos de campanhas.

### Mudança

Vamos ajustar o ADR 0001 para manter o **Agendamento dentro do Monolito Modular**, utilizando o autoscaling da própria plataforma PaaS.

O uso de Serverless deixa de ser uma decisão obrigatória da arquitetura.

Com isso, reduzimos a quantidade de componentes operacionais e mantemos a arquitetura mais simples para o Envelope A, sem perder a capacidade de lidar com períodos de maior demanda.

---

## 2. Trilha de auditoria incompleta e inconsistente com LGPD

### Objeção recebida

O Grupo 10 questiona a utilização de `criado_por`, `alterado_por` e `timestamp` como trilha de auditoria. A objeção aponta que somente essas colunas não preservariam todas as alterações intermediárias de um registro.

Também foi levantada a questão da relação entre retenção de prontuários por 20 anos e os requisitos de proteção de dados da LGPD.

O Grupo 10 sugere Event Sourcing associado a Crypto-Shredding.

### Nossa resposta

**Aceitamos parcialmente a objeção.**

Concordamos que somente manter os campos `criado_por`, `alterado_por` e `timestamp` não representa um histórico completo de todas as alterações realizadas no registro.

Porém, não adotaremos Event Sourcing para todo o prontuário. O Envelope A possui apenas 6 desenvolvedores, orçamento limitado e necessidade de entrega rápida. A adoção de Event Sourcing aumentaria significativamente a complexidade inicial da solução.

### Mudança

Vamos complementar o ADR 0002 especificando que os registros sensíveis devem possuir uma **trilha de auditoria separada**, preservando histórico de alterações relevantes, usuário responsável e data/hora da operação.

O banco PostgreSQL continua sendo utilizado como armazenamento principal, aproveitando suas características transacionais e relacionais.

Também serão considerados controles de acesso e proteção dos dados para que a retenção exigida pelo caso seja compatível com os requisitos de privacidade.

A mudança melhora a auditoria sem introduzir a complexidade de Event Sourcing em toda a aplicação.

---

## 3. Sobrecarga operacional nas UBSs com infraestrutura local

### Objeção recebida

O Grupo 10 questiona a utilização de workers e filas para sincronização das UBSs, argumentando que isso poderia transferir uma complexidade operacional excessiva para as unidades, especialmente porque o Envelope A não possui equipe dedicada de operações.

O grupo sugere utilizar armazenamento local do navegador, como IndexedDB, juntamente com Service Workers e Background Sync.

### Nossa resposta

**Aceitamos parcialmente a objeção.**

A necessidade de manter o atendimento funcionando mesmo com internet instável continua sendo obrigatória. Porém, a arquitetura não exige a instalação de um RabbitMQ ou outro broker completo em cada UBS.

A fila local apresentada no ADR 0005 deve ser entendida como uma **fila de eventos da própria aplicação**, e não como uma infraestrutura de mensageria completa instalada fisicamente em cada unidade.

### Mudança

Vamos deixar essa distinção explícita no ADR 0005 e na documentação da arquitetura.

A aplicação local poderá utilizar armazenamento persistente no dispositivo/navegador para registrar operações pendentes. Quando a conectividade retornar, um worker da própria aplicação realizará a sincronização com o backend.

No servidor central, a infraestrutura de mensageria permanece responsável pelo processamento assíncrono.

Também manteremos identificadores únicos e processamento idempotente para evitar duplicação quando uma operação for reenviada após uma falha de comunicação.

---

## 4. Falsa proteção do legado focando apenas em código

### Objeção recebida

O Grupo 10 argumenta que a Arquitetura Hexagonal e o uso de Adaptadores/ACL isolam o código do legado, mas não resolvem sozinhos a indisponibilidade do sistema legado.

Caso o sistema de regulação de leitos esteja indisponível, uma chamada síncrona ainda poderia falhar e afetar a operação.

O grupo sugere o uso de mensageria e uma abordagem assíncrona com estado pendente.

### Nossa resposta

**Aceitamos a objeção.**

A separação por Ports and Adapters e ACL resolve principalmente o acoplamento estrutural entre o novo sistema e o legado. Ela não garante, sozinha, resiliência contra indisponibilidade ou falhas de comunicação.

Portanto, a crítica identifica uma lacuna importante na decisão arquitetural.

### Mudança

Vamos complementar o ADR 0003 com mecanismos de resiliência para a integração com o legado.

Quando uma operação puder ser processada de forma assíncrona, ela poderá ser registrada inicialmente como **pendente**, sendo posteriormente processada por uma fila e submetida a novas tentativas em caso de falha.

Entretanto, a reserva de leito continua exigindo consistência forte. A arquitetura não deve confirmar para o usuário uma reserva definitiva enquanto não houver confirmação da operação necessária.

Dessa forma, a Hexagonal/ACL continua sendo utilizada para reduzir o acoplamento com o legado, enquanto a mensageria e as retentativas complementam a resiliência da integração.

---

## 5. Falta de otimização no fluxo da vigilância epidemiológica

### Objeção recebida

O Grupo 10 questiona o processamento individual das notificações epidemiológicas e aponta que o envio de muitas notificações separadamente pode aumentar o número de chamadas externas, o custo e o risco de atingir limites de requisições do sistema federal.

O grupo sugere utilizar Batch Processing para agrupar notificações.

### Nossa resposta

**Aceitamos parcialmente a objeção.**

Concordamos que o processamento em lote pode reduzir chamadas externas e melhorar a eficiência quando houver grande volume de notificações.

Porém, não podemos depender exclusivamente de um único processamento diário, porque o caso determina que a notificação compulsória deve chegar à vigilância epidemiológica dentro de 24 horas.

Além disso, a indisponibilidade do sistema federal não pode interromper o funcionamento do fluxo interno.

### Mudança

Vamos complementar o fluxo da vigilância com **processamento em lote quando aplicável**, agrupando notificações pendentes para reduzir chamadas externas.

As notificações continuarão sendo registradas de forma durável no sistema municipal e colocadas em uma fila de processamento.

Caso o sistema federal esteja indisponível, os eventos permanecerão pendentes e serão reenviados automaticamente após a recuperação do serviço.

Assim, o processamento em lote reduz o custo e o número de chamadas, enquanto a fila e as retentativas garantem que uma falha externa não cause perda da notificação.

---

# Síntese das alterações realizadas

Após a revisão do Grupo 10, foram identificadas as seguintes melhorias na arquitetura:

1. O **Agendamento permanece no Monolito Modular**, utilizando o autoscaling da plataforma PaaS, evitando uma separação Serverless desnecessária.
2. O **ADR 0002 passa a explicitar uma trilha de auditoria mais completa**, sem adotar Event Sourcing para todo o prontuário.
3. O **ADR 0005 esclarece que não haverá um broker de mensageria completo instalado nas UBSs**. A aplicação mantém os eventos pendentes localmente e sincroniza quando a conectividade retorna.
4. O **ADR 0003 passa a considerar resiliência da integração com o legado**, utilizando processamento assíncrono e retentativas quando aplicável.
5. O fluxo de **vigilância epidemiológica passa a permitir processamento em lote**, mantendo fila, persistência e retentativas para garantir o processamento dentro do prazo exigido pelo caso.

As objeções contribuíram para tornar explícitos alguns mecanismos de resiliência, auditoria e operação que estavam implícitos na arquitetura inicial.
