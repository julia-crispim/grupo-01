# ADR 0001: adotar arquitetura híbrida (Monolito Modular + Serverless)

**Status:** aceito

**Contexto:** Temos apenas 6 desenvolvedores, zero equipe de operações, orçamento de 6 meses e nuvem paga por uso (Envelope A). O sistema precisa lidar com o uso diário constante das UBSs/UPAs e com picos de acesso de até 20x o normal em campanhas de vacinação.

**Decisão:** Adotar um Monolito Modular como núcleo da aplicação para a maioria dos subdomínios (Prontuário, Farmácia, Atendimento UPA), complementado por funções Serverless isoladas exclusivamente para o subdomínio de Agendamento/Campanhas de Vacinação.

**Alternativas consideradas:**
- Microsserviços puros: descartado por exigir uma infraestrutura de rede e operação complexa inviável para 6 pessoas.
- Monolito tradicional em camadas: descartado porque a falta de modularidade rígida geraria forte acoplamento e dificultaria a evolução do código ao longo do tempo.

**Consequências:**
- **Positivas:** baixo custo operacional, facilidade de deploy de um único artefato central e capacidade de absorver os picos de vacinação com recursos sob demanda, reduzindo infraestrutura ociosa.
- **Negativas:** exige disciplina rigorosa da equipe de 6 desenvolvedores para manter os pacotes do monólito estritamente desacoplados.
