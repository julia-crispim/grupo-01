# ADR 0006: Manter o Agendamento no Monolito Modular

Status: substitui o ADR 0001

## Contexto

Após a leitura cruzada realizada pelo Grupo 10, foi identificada uma complexidade desnecessária na utilização de Serverless exclusivamente para o subdomínio de Agendamento.

O Envelope A possui apenas 6 desenvolvedores, não possui equipe dedicada de operações e possui orçamento limitado para os primeiros seis meses.

Além disso, a arquitetura já utiliza uma plataforma PaaS com escalabilidade automática. Dessa forma, separar o Agendamento em funções Serverless criaria mais componentes para desenvolvimento, monitoramento e implantação sem uma necessidade arquitetural suficiente que justifique essa separação.

## Decisão

O subdomínio de Agendamento permanecerá dentro do Monolito Modular.

Os picos de demanda, especialmente os relacionados às campanhas de vacinação, serão tratados pelo autoscaling da plataforma PaaS utilizada pela aplicação.

O Serverless deixa de ser utilizado como componente obrigatório para o Agendamento.

## Consequências

### Positivas

- Redução da complexidade operacional.
- Menor quantidade de componentes para desenvolver e monitorar.
- CI/CD mais simples.
- Menor esforço para uma equipe de apenas 6 desenvolvedores.
- Aproveitamento da escalabilidade automática da plataforma PaaS.

### Negativas

- O Agendamento permanece compartilhando a estrutura principal da aplicação.
- Picos de demanda serão tratados pela infraestrutura compartilhada do Monolito Modular.
- Uma separação futura poderá ser necessária caso o subdomínio apresente requisitos que justifiquem sua extração.

## Alternativas consideradas

### Manter Serverless no Agendamento

Descartada após a leitura cruzada porque adicionaria complexidade operacional para um benefício que pode ser obtido pelo autoscaling da plataforma PaaS.

### Criar um microsserviço de Agendamento

Descartada devido ao tamanho reduzido da equipe e ao custo operacional de uma arquitetura distribuída no Envelope A.
