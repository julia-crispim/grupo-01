# Matriz de Estilos Aplicada

## Caso 2 — Saúde: rede municipal de atenção à saúde

### Envelope A

Startup contratada para entregar a primeira versão em 6 meses, com 6 desenvolvedores, sem equipe de operação, caixa para seis meses e nuvem pública paga por uso. A exigência dominante é entregar rápido e barato sem se enterrar depois.

| Estilo Arquitetural | Serve para o caso e envelope? | Subdomínio de aplicação | Por quê? | Atributos de qualidade — melhora / piora |
|---|---|---|---|---|
| **1. Monolito em Camadas (Cap. 5)** | **Sim** | Agendamento e Farmácia básica | Organiza o código em faixas técnicas simples em uma única unidade de implantação, ideal para prazos curtos e equipes iniciantes. Conforme a **Seção 5.5**, é indicado para times pequenos sem necessidade de implantação independente por grupo. | **Melhora:** Implantabilidade inicial.<br>**Piora:** Modificabilidade à medida que o negócio cresce. |
| **2. Monolito Modular (Cap. 6)** | **Sim** | Prontuário eletrônico e Farmácia e estoque | Mantém o custo operacional baixo de um único artefato, mas impõe fronteiras lógicas de negócio verificadas por ferramentas de análise estática. Conforme as **Seções 6.1 e 6.5**, é o ponto de partida ideal para domínios que exigem futura extração de serviços. | **Melhora:** Modificabilidade e testabilidade interna.<br>**Piora:** Governança inicial (exige disciplina estrita de pacotes). |
| **3. Hexagonal (Portas e Adaptadores) (Cap. 7)** | **Em parte** | Prontuário eletrônico e Regulação de leitos | Isola as regras de domínio da infraestrutura e de integrações instáveis. Conforme as **Seções 7.1 e 7.5**, permite testar a regra de negócio sem banco de dados e gerenciar o legado com adaptadores dedicados. | **Melhora:** Testabilidade.<br>**Piora:** Custo de desenvolvimento inicial (cerimônia de portas e adaptadores). |
| **4. Microkernel (Núcleo e Plugins) (Cap. 8)** | **Não** | N/A (Descartado) | O sistema não é uma plataforma aberta para terceiros criarem extensões dinâmicas. Conforme a **Seção 8.6**, o estilo deve ser evitado quando a variação de regras é finita e interna à organização, gerando complexidade desnecessária de contratos. | **Melhora:** Modificabilidade por acréscimo de terceiros.<br>**Piora:** Complexidade de versionamento de contratos. |
| **5. Microsserviços (Cap. 9)** | **Não** | N/A (Descartado por incompatibilidade com Envelope A) | Com apenas 6 desenvolvedores e sem equipe de operação, o custo operacional distribuído, a consistência eventual e a complexidade de redes superam os ganhos de autonomia. Conforme a **Seção 9.6**, o estilo não deve ser adotado sem plataforma automatizada madura. | **Melhora:** Implantabilidade independente por time.<br>**Piora:** Custo operacional e testabilidade distribuída. |
| **6. SOA e Barramento de Serviços (ESB) (Cap. 10)** | **Não** | N/A (Descartado) | Concentra lógica de negócio e transformação em um intermediário central pesado e caro. Conforme as **Seções 10.5 e 10.6**, conflita com a agilidade de uma startup e cria um ponto único de falha corporativo. | **Melhora:** Governança centralizada de integrações.<br>**Piora:** Desempenho (latência de salto extra) e manutenibilidade. |
| **7. Arquitetura Orientada a Eventos (Cap. 11)** | **Em parte** | Integração federal e legado / Vigilância epidemiológica | Desacopla produtores e consumidores no tempo por meio de um corretor de mensagens. Conforme a **Seção 11.5**, permite que notificações e integrações externas (como sistemas federais) aguardem a rede voltar sem travar o atendimento presencial na UPA. | **Melhora:** Disponibilidade e resiliência a falhas de rede.<br>**Piora:** Testabilidade e depuração distribuída. |
| **8. Serverless (Cap. 12)** | **Em parte** | Agendamento e cidadão (Campanhas de vacinação) | Executa funções sob demanda sem gerenciamento de servidores, cobrando apenas pelo uso. Conforme a **Seção 12.5**, atende perfeitamente a picos sazonais extremos, como campanhas de vacinação, sem desperdiçar recursos na ociosidade. | **Melhora:** Custo financeiro em ociosidade e escalabilidade automática.<br>**Piora:** Aprisionamento ao fornecedor (vendor lock-in) e depuração. |
| **9. Arquitetura Celular (Cell-based) (Cap. 13)** | **Não** | N/A (Descartado para o Envelope A) | O isolamento completo de instâncias por subconjunto de clientes exige infraestrutura redundante e um plano de controle complexo. Conforme a **Seção 13.6**, é desproporcional para uma equipe inicial de 6 desenvolvedores. | **Melhora:** Disponibilidade (limitação do raio de impacto).<br>**Piora:** Custo de infraestrutura e complexidade operacional. |
| **10. CQRS (Cap. 14)** | **Em parte** | Vigilância epidemiológica e Prontuário eletrônico | Separa o modelo de escrita transacional do modelo de leitura otimizado para relatórios. Conforme a **Seção 14.5**, resolve gargalos de consultas complexas e auditorias analíticas sem sobrecarregar o banco transacional. | **Melhora:** Desempenho de leitura e flexibilidade de consultas.<br>**Piora:** Complexidade de manutenção de dois modelos e consistência eventual. |
| **11. Event Sourcing (Cap. 15)** | **Não** | N/A (Descartado para a primeira versão) | Embora a guarda de 20 anos do prontuário seja exigida, a imutabilidade estrita de eventos e a complexidade de versionamento de esquemas tornam o estilo excessivo para o prazo de 6 meses da startup. Conforme a **Seção 15.6**, o custo de adoção inicial é elevado. | **Melhora:** Auditabilidade completa do histórico.<br>**Piora:** Custo de desenvolvimento e complexidade de reprocessamento. |
| **12. Pipes and Filters (Cap. 16)** | **Em parte** | Vigilância epidemiológica e consolidação de lotes | Organiza o processamento de dados em etapas sequenciais independentes. Conforme a **Seção 16.5**, é ideal para pipelines de consolidação de boletins epidemiológicos e validação de lotes da farmácia. | **Melhora:** Modificabilidade de etapas e testabilidade de fluxos de dados.<br>**Piora:** Latência em fluxos interativos síncronos. |

## Estilos descartados

### 1. Microsserviços — Capítulo 9

**Motivo do descarte:** a startup possui apenas 6 desenvolvedores e nenhuma equipe de operação dedicada. Adotar microsserviços exigiria gerenciar redes, descoberta de serviços, rastreamento distribuído e consistência eventual (sagas), o que inviabiliza a entrega no prazo de 6 meses estipulado no Envelope A.

### 2. Arquitetura Celular / Cell-based — Capítulo 13

**Motivo do descarte:** o particionamento completo da base em células isoladas com roteadores e planos de controle próprios é projetado para sistemas corporativos massivos com alta criticidade de multi-inquilinos (multi-tenant). Para uma startup em estágio inicial, a sobrecarga de operar múltiplas instâncias paralelas é totalmente desproporcional à capacidade da equipe.

## Estilos considerados

### 1. Monolito em Camadas — Capítulo 5

**Motivo da consideração:** foi considerado por organizar o código em faixas técnicas simples dentro de uma única unidade de implantação, sendo adequado ao prazo curto e à equipe pequena. Conforme a **Seção 5.5**, é indicado para times pequenos sem necessidade de implantação independente por grupo.

### 2. Monolito Modular — Capítulo 6

**Motivo da consideração:** foi considerado porque mantém o custo operacional baixo de um único artefato, ao mesmo tempo em que cria fronteiras lógicas de negócio. Conforme as **Seções 6.1 e 6.5**, é um ponto de partida adequado para domínios que podem exigir futura extração de serviços.
