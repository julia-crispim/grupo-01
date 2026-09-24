Objeções ao Grupo 04

Objeção 1 — Microsserviços não se encaixam perfeitamente no envelope

Decisão/trecho atacado:
Matriz de estilos arquiteturais / Microsserviços, Cap. 9, Seção 9.5: “Encaixa-se perfeitamente na capacidade do consórcio BB (40 desenvolvedores, 5 times, nuvem pública).”

Argumento:
A quantidade de desenvolvedores e times justifica a possibilidade de adoção de microsserviços, mas não significa que o estilo se encaixe “perfeitamente” no envelope. O sistema ainda precisa operar em 70 UBSs/UPAs com conectividade instável, o que aumenta significativamente a complexidade de descoberta de serviços, observabilidade, sincronização, implantação e tratamento de falhas distribuídas. O custo operacional de dezenas de serviços distribuídos pode superar o ganho de escalabilidade seletiva, principalmente nos subdomínios que não apresentam o mesmo pico de demanda.

O que nosso grupo faria no lugar:
Usaríamos microsserviços apenas nos subdomínios que realmente apresentam necessidade de escalabilidade e autonomia de implantação, mantendo os demais componentes mais consolidados. Dessa forma, reduziríamos a quantidade de comunicação distribuída sem perder a capacidade de escalar especificamente Agendamento e Vacinação.

⸻

Objeção 2 — Arquitetura celular não garante, por si só, consistência para recursos compartilhados

Decisão/trecho atacado:
Matriz de estilos arquiteturais / Arquitetura celular, Cap. 13, Seção 13.5: “Permite que a UPA funcione como uma ‘célula local’ com banco próprio durante a queda da internet e sincronize assincronamente ao reconectar.”

Argumento:
A autonomia local resolve a disponibilidade, mas cria um problema justamente no caso mais crítico do envelope: duas unidades podem tentar modificar simultaneamente o mesmo recurso compartilhado, como um leito. Bancos independentes por célula não conseguem, isoladamente, garantir exclusão mútua entre 70 unidades desconectadas. Assim, a decisão melhora a disponibilidade, mas transfere o problema para a reconciliação de conflitos e pode comprometer a consistência exigida pela regulação.

O que nosso grupo faria no lugar:
Manteríamos a autonomia das células para os dados locais, mas centralizaríamos ou coordenaríamos explicitamente os recursos realmente globais, como leitos. Para esses recursos, usaríamos uma autoridade transacional única ou um mecanismo de reserva distribuída com identificador de versão, expiração e reconciliação de conflitos.

⸻

Objeção 3 — A resposta sobre reserva de leitos apresenta uma garantia maior do que a arquitetura demonstrada

Decisão/trecho atacado:
Perguntas e respostas / “Como duas unidades disputando o mesmo leito nunca conseguem reservá-lo ao mesmo tempo, com o sistema legado ainda no circuito?”

Argumento:
A resposta afirma que “duas reservas concorrentes não conseguem ser aceitas ao mesmo tempo”, mas o restante da arquitetura descreve bancos locais independentes e sincronização posterior. Um controle transacional local impede conflitos dentro de uma célula, mas não necessariamente entre células que estão desconectadas. O envelope possui exatamente a condição que torna o problema difícil: várias unidades podem continuar operando enquanto a rede está indisponível.

O que nosso grupo faria no lugar:
Não afirmaríamos “nunca” sem especificar o mecanismo de coordenação. Definiríamos explicitamente que a reserva de leitos é um recurso compartilhado, com uma autoridade de decisão central ou um protocolo de concessão de reserva, deixando claro o comportamento quando uma célula perde conectividade.

⸻

Objeção 4 — Event Sourcing não garante sozinho uma auditoria completa

Decisão/trecho atacado:
Matriz de estilos arquiteturais / Event Sourcing, Cap. 15, Seção 15.5: “Garante a auditoria exata de quem acessou, modificou ou visualizou cada dado sensível do prontuário.”

Argumento:
Event Sourcing registra a evolução do estado por eventos de domínio, mas isso não significa automaticamente que toda visualização ou acesso ao prontuário será registrado. Uma consulta de leitura pode não alterar o estado do domínio e, portanto, precisa de eventos de auditoria próprios. Além disso, armazenar todo esse histórico por 20 anos gera um custo considerável de armazenamento, retenção, projeções e gerenciamento de dados sensíveis.

O que nosso grupo faria no lugar:
Separaríamos claramente os eventos de domínio do log de auditoria. Registraríamos explicitamente acessos, alterações, consultas e ações autorizadas, aplicando políticas específicas de retenção e proteção aos eventos de auditoria e utilizando Event Sourcing somente onde o histórico completo de mudanças realmente trouxesse valor.

⸻

Objeção 5 — A guarda de 20 anos e a LGPD não são resolvidas apenas pela arquitetura

Decisão/trecho atacado:
Perguntas e respostas / “Como o prontuário garante que se saiba quem acessou cada registro, e como convive a guarda de 20 anos com os direitos do paciente sob a LGPD?”

Argumento:
A arquitetura pode fornecer rastreabilidade e mecanismos de controle, mas não determina sozinha a base legal, o prazo de retenção aplicável a cada categoria de dado ou a forma como os direitos do titular serão operacionalizados. A afirmação de que a retenção de 20 anos “aplica-se ao histórico de auditoria e aos eventos de domínio relevantes” também precisa ser fundamentada juridicamente e não apenas arquiteturalmente. Nesse envelope, segurança, retenção e privacidade representam requisitos independentes que precisam de políticas próprias.

O que nosso grupo faria no lugar:
Separaríamos a decisão arquitetural da decisão de governança de dados. A arquitetura implementaria autenticação, autorização, trilha de auditoria, criptografia e controles de retenção configuráveis, enquanto os prazos e hipóteses de tratamento seriam definidos pelas regras legais e institucionais aplicáveis.

⸻

Objeção 6 — EDA melhora a disponibilidade, mas pode entrar em conflito com requisitos de consistência

Decisão/trecho atacado:
Matriz de estilos arquiteturais / Arquitetura orientada a eventos, Cap. 11, Seção 11.5: “As UBSs e UPAs registram e publicam os fatos locais que serão enfileirados e consumidos na nuvem assim que a conectividade for restabelecida.”

Argumento:
O mecanismo é adequado para notificações e alertas que podem ser processados de forma assíncrona, mas o envelope também contém operações cujo resultado pode depender do estado atual de outro recurso. Se o mesmo padrão assíncrono for aplicado indiscriminadamente, haverá atrasos entre o estado local e o central. Isso é especialmente problemático para informações operacionais que precisam refletir uma situação atual, e não apenas eventual convergência.

O que nosso grupo faria no lugar:
Usaríamos EDA principalmente para notificações, vigilância e integração assíncrona. Para operações críticas e transacionais, definiríamos explicitamente quais dados precisam de consistência forte e quais podem aceitar consistência eventual.
